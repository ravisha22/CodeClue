# Baseline Evaluation: Raw Source Files
# Task: blind-fiber-2

You are a senior software engineer. You have been given raw source code
excerpts from a repository. Answer the question using ONLY the source
code below. Do not use any external knowledge about the framework.

--- SOURCE CODE ---
## client\errors.go (score: 3.0)
```
package client

import (
	"errors"
)

var (
	errResponseChanTypeAssertion = errors.New("failed to type-assert to *Response")
	errChanErrorTypeAssertion    = errors.New("failed to type-assert to chan error")
	errRequestTypeAssertion      = errors.New("failed to type-assert to *Request")
	errFileTypeAssertion         = errors.New("failed to type-assert to *File")
	errCookieJarTypeAssertion    = errors.New("failed to type-assert to *CookieJar")
	errSyncPoolBuffer            = errors.New("failed to retrieve buffer from a sync.Pool")
)

```

## client\response.go (score: 3.0)
```
package client

import (
	"bytes"
	"errors"
	"fmt"
	"io"
	"io/fs"
	"iter"
	"os"
	"path/filepath"
	"sync"

	"github.com/gofiber/utils/v2"
	"github.com/valyala/fasthttp"
)

// Response represents the result of a request. It provides access to the response data.
type Response struct {
	client  *Client
	request *Request

	RawResponse *fasthttp.Response
	cookie      []*fasthttp.Cookie
}

// setClient sets the client instance in the response. The client object is used by core functionalities.
func (r *Response) setClient(c *Client) {
	r.client = c
}

// setRequest sets the request object in the response. The request is released when Response.Close is called.
func (r *Response) setRequest(req *Request) {
	r.request = req
}

// Status returns the HTTP status message of the executed request.
func (r *Response) Status() string {
	return string(r.RawResponse.Header.StatusMessage())
}

// StatusCode returns the HTTP status code of the executed request.
func (r *Response) StatusCode() int {
	return r.RawResponse.StatusCode()
}

// Protocol returns the HTTP protocol used for the request.
func (r *Response) Protocol() string {
	return string(r.RawResponse.Header.Protocol())
}

// Header returns the value of the specified response header field.
func (r *Response) Header(key string) string {
	return utils.UnsafeString(r.RawResponse.Header.Peek(key))
}

// Headers returns all headers in the response using an iterator.
// Use maps.Collect() to gather them into a map if needed.
//
// The returned values are valid only until the response object is released.
// Do not store references to returned values; make copies instead.
func (r *Response) Headers() iter.Seq2[string, []string] {
	return func(yield func(string, []string) bool) {
		keys := r.RawResponse.Header.PeekKeys()
		for _, key := range keys {
			vals := r.RawResponse.Header.PeekAll(utils.UnsafeString(key))
			valsStr := make([]string, len(vals))
			for i, v := range vals {
				valsStr[i] = utils.UnsafeString(v)
			}

			if !yield(utils.UnsafeString(key), valsStr) {
				return
			}
		}
	}
}

// Cookies returns all cookies set by the response.
//
// The returned values are valid only until the response object is released.
// Do not store references to returned values; make copies instead.
func (r *Response) Cookies() []*fasthttp.Cookie {
	return r.cookie
}

// Body returns the HTTP response body as a byte slice.
func (r *Response) Body() []byte {
	return r.RawResponse.Body()
}

// BodyStream returns the response body as a stream reader.
// Note: When using BodyStream(), the response body is not copied to memory,
// so calling Body() afterwards may return an empty slice.
func (r *Response) BodyStream() io.Reader {
	if stream := r.RawResponse.BodyStream(); stream != nil {
		return stream
	}
	// If streaming is not enabled, return a bytes.Reader from the regular body
	return bytes.NewReader(r.RawResponse.Body())
}

// IsStreaming returns true if the response body is being streamed.
func (r *Response) IsStreaming() bool {
	return r.RawResponse.BodyStream() != nil
}

// String returns the response body as a trimmed string.
func (r *Response) String() string {
	return utils.TrimSpace(string(r.Body()))
}

// JSON unmarshal the response body into the given interface{} using JSON.
func (r *Response) JSON(v any) error {
	if r.client == nil {
		return ErrClientNil
	}

	return r.client.jsonUnmarshal(r.Body(), v)
}

// CBOR unmarshal the response body into the given interface{} using CBOR.
func (r *Response) CBOR(v any) error {
	if r.client == nil {
		return ErrClientNil
	}

	return r.client.cborUnmarshal(r.Body(), v)
}

// XML unmarshal the response body into the given interface{} using XML.
func (r *Response) XML(v any) error {
	if r.client == nil {
		return ErrClientNil
	}

	return r.client.xmlUnmarshal(r.Body(), v)
}

// Save writes the response body to a file or io.Writer.
// If a string path is provided, it creates directories if needed, then writes to a file.
// If an io.Writer is provided, it writes directly to it.
// When streaming is enabled, the body is read directly from the stream.
func (r *Response) Save(v any) error {
	switch p := v.(type) {
	case string:
		file := filepath.Clean(p)
		dir := filepath.Dir(file)

		// Create directory if it doesn't exist
		if _, err := os.Stat(dir); err != nil {
			if !errors.Is(err, fs.ErrNotExist) {
				return fmt.Errorf("failed to check directory: %w", err)
			}

			if err = os.MkdirAll(dir, 0o750); err != nil {
				return fmt.Errorf("failed to create directory: %w", err)
			}
		}

		// Create and write to file
		outFile, err := os.Create(file)
		if err != nil {
			return fmt.Errorf("failed to create file: %w", err)
		}
		defer func() { _ = outFile.Close() }() //nolint:errcheck // not needed

		// Use BodyStream() which handles both streaming and non-streaming cases
		if _, err = io.Copy(outFile, r.BodyStream()); err != nil {
			return fmt.Errorf("failed to write response body to file: %w", err)
		}

		return nil

	case io.Writer:
		// Use BodyStream() which handles both streaming and non-streaming cases
		if _, err := io.Copy(p, r.BodyStream()); err != nil {
			return fmt.Errorf("failed to write response body to writer: %w", err)
		}
		// Close the writer if it implements io.WriteCloser
		if pc, ok := p.(io.WriteCloser); ok {
			_ = pc.Close() //nolint:errcheck // not needed
		}

		return nil

	default:
		return ErrNotSupportSaveMethod
	}
}

// Reset clears the Response object, making it ready for reuse.
func (r *Response) Reset() {
	r.client = nil
	r.request = nil

	for len(r.cookie) != 0 {
		t := r.cookie[0]
		r.cookie = r.cookie[1:]
		fasthttp.ReleaseCookie(t)
	}

	r.RawResponse.Reset()
}

// Close releases both the Request and Response objects back to their pools.
// After calling Close, do not use these objects.
func (r *Response) Close() {
	if r.request != nil {
		tmp := r.request
		r.request = nil
		ReleaseRequest(tmp)
	}
	ReleaseResponse(r)
}

var responsePool = &sync.Pool{
	New: func() any {
		return &Response{
			cookie:      []*fasthttp.Cookie{},
			RawResponse: fasthttp.AcquireResponse(),
		}
	},
}

// AcquireResponse returns a new (pooled) Response object.
// When done, release it with ReleaseResponse to reduce GC load.
func AcquireResponse() *Response {
	resp, ok := responsePool.Get().(*Response)
	if !ok {
		panic("unexpected type from responsePool.Get()")
	}
	return resp
}

// ReleaseResponse returns the Response object to the pool.
// Do not use the released Response afterward to avoid data races.
func ReleaseResponse(resp *Response) {
	resp.Reset()
	responsePool.Put(resp)
}

```

## error.go (score: 3.0)
```
package fiber

import (
	"encoding/json"
	"errors"

	"github.com/gofiber/schema"
)

// Wrap and return this for unreachable code if panicking is undesirable (i.e., in a handler).
// Unexported because users will hopefully never need to see it.
var errUnreachable = errors.New("fiber: unreachable code, please create an issue at github.com/gofiber/fiber")

// General errors
var (
	ErrGracefulTimeout = errors.New("shutdown: graceful timeout has been reached, exiting")
	// ErrNotRunning indicates that a Shutdown method was called when the server was not running.
	ErrNotRunning = errors.New("shutdown: server is not running")
	// ErrHandlerExited is returned by App.Test if a handler panics or calls runtime.Goexit().
	ErrHandlerExited = errors.New("runtime.Goexit() called in handler or server panic")
	// ErrNoViewEngineConfigured indicates that a helper requiring a view engine was invoked without one configured.
	ErrNoViewEngineConfigured = errors.New("fiber: no view engine configured")
	// ErrAutoCertWithCertFile indicates AutoCertManager cannot be used with CertFile/CertKeyFile.
	ErrAutoCertWithCertFile = errors.New("tls: AutoCertManager cannot be combined with CertFile/CertKeyFile")
)

// Fiber redirection errors
var (
	ErrRedirectBackNoFallback = NewError(StatusInternalServerError, "Referer not found, you have to enter fallback URL for redirection.")
)

// Range errors
var (
	ErrRangeMalformed     = errors.New("range: malformed range header string")
	ErrRangeTooLarge      = NewError(StatusRequestedRangeNotSatisfiable, "range: too many ranges")
	ErrRangeUnsatisfiable = errors.New("range: unsatisfiable range")
)

// Binder errors
var ErrCustomBinderNotFound = errors.New("binder: custom binder not found, please be sure to enter the right name")

// Format errors
var (
	// ErrNoHandlers is returned when c.Format is called with no arguments.
	ErrNoHandlers = errors.New("format: at least one handler is required, but none were set")
)

// gofiber/schema errors
type (
	// ConversionError Conversion error exposes the internal schema.ConversionError for public use.
	ConversionError = schema.ConversionError
	// UnknownKeyError error exposes the internal schema.UnknownKeyError for public use.
	UnknownKeyError = schema.UnknownKeyError
	// EmptyFieldError error exposes the internal schema.EmptyFieldError for public use.
	EmptyFieldError = schema.EmptyFieldError
	// MultiError error exposes the internal schema.MultiError for public use.
	MultiError = schema.MultiError
)

// encoding/json errors
type (
	// InvalidUnmarshalError describes an invalid argument passed to Unmarshal.
	// (The argument to Unmarshal must be a non-nil pointer.)
	InvalidUnmarshalError = json.InvalidUnmarshalError

	// MarshalerError represents an error from calling a MarshalJSON or MarshalText method.
	MarshalerError = json.MarshalerError

	// SyntaxError is a description of a JSON syntax error.
	SyntaxError = json.SyntaxError

	// UnmarshalTypeError describes a JSON value that was
	// not appropriate for a value of a specific Go type.
	UnmarshalTypeError = json.UnmarshalTypeError

	// UnsupportedTypeError is returned by Marshal when attempting
	// to encode an unsupported value type.
	UnsupportedTypeError = json.UnsupportedTypeError

	// UnsupportedValueError exposes json.UnsupportedValueError to describe unsupported values encountered during encoding.
	UnsupportedValueError = json.UnsupportedValueError
)

```

## errors_internal.go (score: 3.0)
```
package fiber

import (
	"errors"
)

var (
	errBindPoolTypeAssertion  = errors.New("failed to type-assert to *Bind")
	errCustomCtxTypeAssertion = errors.New("failed to type-assert to CustomCtx")
	errInvalidEscapeSequence  = errors.New("invalid escape sequence")
	errRedirectTypeAssertion  = errors.New("failed to type-assert to *Redirect")
)

```

## log\fiberlog.go (score: 3.0)
```
package log

import (
	"context"
	"io"
)

// Fatal calls the default logger's Fatal method and then os.Exit(1).
func Fatal(v ...any) {
	logger.Fatal(v...)
}

// Error calls the default logger's Error method.
func Error(v ...any) {
	logger.Error(v...)
}

// Warn calls the default logger's Warn method.
func Warn(v ...any) {
	logger.Warn(v...)
}

// Info calls the default logger's Info method.
func Info(v ...any) {
	logger.Info(v...)
}

// Debug calls the default logger's Debug method.
func Debug(v ...any) {
	logger.Debug(v...)
}

// Trace calls the default logger's Trace method.
func Trace(v ...any) {
	logger.Trace(v...)
}

// Panic calls the default logger's Panic method.
func Panic(v ...any) {
	logger.Panic(v...)
}

// Fatalf calls the default logger's Fatalf method and then os.Exit(1).
func Fatalf(format string, v ...any) {
	logger.Fatalf(format, v...)
}

// Errorf calls the default logger's Errorf method.
func Errorf(format string, v ...any) {
	logger.Errorf(format, v...)
}

// Warnf calls the default logger's Warnf method.
func Warnf(format string, v ...any) {
	logger.Warnf(format, v...)
}

// Infof calls the default logger's Infof method.
func Infof(format string, v ...any) {
	logger.Infof(format, v...)
}

// Debugf calls the default logger's Debugf method.
func Debugf(format string, v ...any) {
	logger.Debugf(format, v...)
}

// Tracef calls the default logger's Tracef method.
func Tracef(format string, v ...any) {
	logger.Tracef(format, v...)
}

// Panicf calls the default logger's Tracef method.
func Panicf(format string, v ...any) {
	logger.Panicf(format, v...)
}

// Tracew logs a message with some additional context. The variadic key-value
// pairs are treated as they are privateLog With.
func Tracew(msg string, keysAndValues ...any) {
	logger.Tracew(msg, keysAndValues...)
}

// Debugw logs a message with some additional context. The variadic key-value
// pairs are treated as they are privateLog With.
func Debugw(msg string, keysAndValues ...any) {
	logger.Debugw(msg, keysAndValues...)
}

// Infow logs a message with some additional context. The variadic key-value
// pairs are treated as they are privateLog With.
func Infow(msg string, keysAndValues ...any) {
	logger.Infow(msg, keysAndValues...)
}

// Warnw logs a message with some additional context. The variadic key-value
// pairs are treated as they are privateLog With.
func Warnw(msg string, keysAndValues ...any) {
	logger.Warnw(msg, keysAndValues...)
}

// Errorw logs a message with some additional context. The variadic key-value
// pairs are treated as they are privateLog With.
func Errorw(msg string, keysAndValues ...any) {
	logger.Errorw(msg, keysAndValues...)
}

// Fatalw logs a message with some additional context. The variadic key-value
// pairs are treated as they are privateLog With.
func Fatalw(msg string, keysAndValues ...any) {
	logger.Fatalw(msg, keysAndValues...)
}

// Panicw logs a message with some additional context. The variadic key-value
// pairs are treated as they are privateLog With.
func Panicw(msg string, keysAndValues ...any) {
	logger.Panicw(msg, keysAndValues...)
}

// WithContext binds the default logger to the provided context and returns the
// contextualized logger.
func WithContext(ctx context.Context) CommonLogger {
	return logger.WithContext(ctx)
}

// SetLogger sets the default logger and the system logger.
// Note that this method is not concurrent-safe and must not be called
// after the use of DefaultLogger and global functions from this package.
func SetLogger[T any](v AllLogger[T]) {
	logger = v
}

// SetOutput sets the output of default logger and system logger. By default, it is stderr.
func SetOutput(w io.Writer) {
	logger.SetOutput(w)
}

// SetLevel sets the level of logs below which logs will not be output.
// The default logger is LevelTrace.
// Note that this method is not concurrent-safe.
func SetLevel(lv Level) {
	logger.SetLevel(lv)
}

```

## middleware\idempotency\response.go (score: 3.0)
```
package idempotency

// response is a struct that represents the response of a request.
// generation tool `go install github.com/tinylib/msgp@latest`
//
// Idempotency payloads are stored in backing storage, so keep headers/bodies bounded.
//
//go:generate msgp -o=response_msgp.go -tests=true -unexported
type response struct {
	Headers map[string][]string `msg:"hs,limit=1024"` // HTTP header count norms are well below this.

	Body       []byte `msg:"b"` // Idempotency bodies are bounded by storage policy, not msgp limits.
	StatusCode int    `msg:"sc"`
}

```

## middleware\idempotency\response_msgp.go (score: 3.0)
```
// Code generated by github.com/tinylib/msgp DO NOT EDIT.

package idempotency

import (
	"github.com/tinylib/msgp/msgp"
)

// DecodeMsg implements msgp.Decodable
func (z *response) DecodeMsg(dc *msgp.Reader) (err error) {
	var field []byte
	_ = field
	var zb0001 uint32
	zb0001, err = dc.ReadMapHeader()
	if err != nil {
		err = msgp.WrapError(err)
		return
	}
	for zb0001 > 0 {
		zb0001--
		field, err = dc.ReadMapKeyPtr()
		if err != nil {
			err = msgp.WrapError(err)
			return
		}
		switch msgp.UnsafeString(field) {
		case "hs":
			var zb0002 uint32
			zb0002, err = dc.ReadMapHeader()
			if err != nil {
				err = msgp.WrapError(err, "Headers")
				return
			}
			if zb0002 > 1024 {
				err = msgp.ErrLimitExceeded
				return
			}
			if z.Headers == nil {
				z.Headers = make(map[string][]string, zb0002)
			} else if len(z.Headers) > 0 {
				clear(z.Headers)
			}
			for zb0002 > 0 {
				zb0002--
				var za0001 string
				za0001, err = dc.ReadString()
				if err != nil {
					err = msgp.WrapError(err, "Headers")
					return
				}
				var za0002 []string
				var zb0003 uint32
				zb0003, err = dc.ReadArrayHeader()
				if err != nil {
					err = msgp.WrapError(err, "Headers", za0001)
					return
				}
				if zb0003 > 1024 {
					err = msgp.ErrLimitExceeded
					return
				}
				if cap(za0002) >= int(zb0003) {
					za0002 = (za0002)[:zb0003]
				} else {
					za0002 = make([]string, zb0003)
				}
				for za0003 := range za0002 {
					za0002[za0003], err = dc.ReadString()
					if err != nil {
						err = msgp.WrapError(err, "Headers", za0001, za0003)
						return
					}
				}
				z.Headers[za0001] = za0002
			}
		case "b":
			z.Body, err = dc.ReadBytes(z.Body)
			if err != nil {
				err = msgp.WrapError(err, "Body")
				return
			}
		case "sc":
			z.StatusCode, err = dc.ReadInt()
			if err != nil {
				err = msgp.WrapError(err, "StatusCode")
				return
			}
		default:
			err = dc.Skip()
			if err != nil {
				err = msgp.WrapError(err)
				return
			}
		}
	}
	return
}

// EncodeMsg implements msgp.Encodable
func (z *response) EncodeMsg(en *msgp.Writer) (err error) {
	// map header, size 3
	// write "hs"
	err = en.Append(0x83, 0xa2, 0x68, 0x73)
	if err != nil {
		return
	}
	err = en.WriteMapHeader(uint32(len(z.Headers)))
	if err != nil {
		err = msgp.WrapError(err, "Headers")
		return
	}
	for za0001, za0002 := range z.Headers {
		err = en.WriteString(za0001)
		if err != nil {
			err = msgp.WrapError(err, "Headers")
			return
		}
		err = en.WriteArrayHeader(uint32(len(za0002)))
		if err != nil {
			err = msgp.WrapError(err, "Headers", za0001)
			return
		}
		for za0003 := range za0002 {
			err = en.WriteString(za0002[za0003])
			if err != nil {
				err = msgp.WrapError(err, "Headers", za0001, za0003)
				return
			}
		}
	}
	// write "b"
	err = en.Append(0xa1, 0x62)
	if err != nil {
		return
	}
	err = en.WriteBytes(z.Body)
	if err != nil {
		err = msgp.WrapError(err, "Body")
		return
	}
	// write "sc"
	err = en.Append(0xa2, 0x73, 0x63)
	if err != nil {
		return
	}
	err = en.WriteInt(z.StatusCode)
	if err != nil {
		err = msgp.WrapError(err, "StatusCode")
		return
	}
	return
}

// MarshalMsg implements msgp.Marshaler
func (z *response) MarshalMsg(b []byte) (o []byte, err error) {
	o = msgp.Require(b, z.Msgsize())
	// map header, size 3
	// string "hs"
	o = append(o, 0x83, 0xa2, 0x68, 0x73)
	o = msgp.AppendMapHeader(o, uint32(len(z.Headers)))
	for za0001, za0002 := range z.Headers {
		o = msgp.AppendString(o, za0001)
		o = msgp.AppendArrayHeader(o, uint32(len(za0002)))
		for za0003 := range za0002 {
			o = msgp.AppendString(o, za0002[za0003])
		}
	}
	// string "b"
	o = append(o, 0xa1, 0x62)
	o = msgp.AppendBytes(o, z.Body)
	// string "sc"
	o = append(o, 0xa2, 0x73, 0x63)
	o = msgp.AppendInt(o, z.StatusCode)
	return
}

// UnmarshalMsg implements msgp.Unmarshaler
func (z *response) UnmarshalMsg(bts []byte) (o []byte, err error) {
	var field []byte
	_ = field
	var zb0001 uint32
	zb0001, bts, err = msgp.ReadMapHeaderBytes(bts)
	if err != nil {
		err = msgp.WrapError(err)
		return
	}
	for zb0001 > 0 {
		zb0001--
		field, bts, err = msgp.ReadMapKeyZC(bts)
		if err != nil {
			err = msgp.WrapError(err)
			return
		}
		switch msgp.UnsafeString(field) {
		case "hs":
			var zb0002 uint32
			zb0002, bts, err = msgp.ReadMapHeaderBytes(bts)
			if err != nil {
				err = msgp.WrapError(err, "Headers")
				return
			}
			if zb0002 > 1024 {
				err = msgp.ErrLimitExceeded
				return
			}
			if z.Headers == nil {
				z.Headers = make(map[string][]string, zb0002)
			} else if len(z.Headers) > 0 {
				clear(z.Headers)
			}
			for zb0002 > 0 {
				var za0002 []string
				zb0002--
				var za0001 string
				za0001, bts, err = msgp.ReadStringBytes(bts)
				if err != nil {
					err = msgp.WrapError(err, "Headers")
					return
				}
				var zb0003 uint32
				zb0003, bts, err = msgp.ReadArrayHeaderBytes(bts)
				if err != nil {
					err = msgp.WrapError(err, "Headers", za0001)
					return
				}
				if zb0003 > 1024 {
					err = msgp.ErrLimitExceeded
					return
				}
				if cap(za0002) >= int(zb0003) {
					za0002 = (za0002)[:zb0003]
				} else {
					za0002 = make([]string, zb0003)
				}
				for za0003 := range za0002 {
					za0002[za0003], bts, err = msgp.ReadStringBytes(bts)
					if err != nil {
						err = msgp.WrapError(err, "Headers", za0001, za0003)
						return
					}
				}
				z.Headers[za0001] = za0002
			}
		case "b":
			z.Body, bts, err = msgp.ReadBytesBytes(bts, z.Body)
			if err != nil {
				err = msgp.WrapError(err, "Body")
				return
			}
		case "sc":
			z.StatusCode, bts, err = msgp.ReadIntBytes(bts)
			if err != nil {
				err = msgp.WrapError(err, "StatusCode")
				return
			}
		default:
			bts, err = msgp.Skip(bts)
			if err != nil {
				err = msgp.WrapError(err)
				return
			}
		}
	}
	o = bts
	return
}

// Msgsize returns an upper bound estimate of the number of bytes occupied by the serialized message
func (z *response) Msgsize() (s int) {
	s = 1 + 3 + msgp.MapHeaderSize
	if z.Headers != nil {
		for za0001, za0002 := range z.Headers {
			_ = za0002
			s += msgp.StringPrefixSize + len(za0001) + msgp.ArrayHeaderSize
			for za0003 := range za0002 {
				s += msgp.StringPrefixSize + len(za0002[za0003])
			}
		}
	}
	s += 2 + msgp.BytesPrefixSize + len(z.Body) + 3 + msgp.IntSize
	return
}

```

## middleware\session\data_msgp.go (score: 0.0)
```
// Code generated by github.com/tinylib/msgp DO NOT EDIT.

package session

```
--- END SOURCE CODE ---

QUESTION: When a handler panics in Fiber, how is that turned into an HTTP response, and how can mounted sub-apps change which error formatter gets used?

Provide a detailed answer citing specific functions/files from the source.
