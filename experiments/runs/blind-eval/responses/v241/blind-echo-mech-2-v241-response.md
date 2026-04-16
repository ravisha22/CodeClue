# v2.4.1 Response: blind-echo-mech-2
Date: 2026-04-16

## Echo's Centralized HTTP Error Path

### The Error Handler Entry Point

`DefaultHTTPErrorHandler` (`echo.go:374`) creates the default HTTP error handler implementation and is called during `New` (`echo.go:333`) [FOCUS: DefaultHTTPErrorHandler — "called_by: New"; snippet: `func DefaultHTTPErrorHandler(exposeError bool) HTTPErrorHandler`]. The `exposeError` parameter controls whether error details are exposed in responses.

The error handler is invoked from `Echo.serveHTTP` (`echo.go:700`), which has behavior: **`GUARD(e.premiddleware == nil -> return h1(cc)); DELEGATE(h1 -> result); UNWIND(defer)`** [FOCUS: Echo.serveHTTP]. The `UNWIND(defer)` indicates that cleanup (and likely error handler invocation) happens in a deferred function after the handler chain completes.

### Error Type Discrimination

Echo provides a layered error type system for categorizing errors:

1. **`HTTPError`** (`httperror.go:107`) — the primary structured error type, "represents an error that occurred while handling a request" [FOCUS: HTTPError]. It has methods:
   - `StatusCode` (`httperror.go:115`) — returns the HTTP status code for the response [FOCUS: HTTPError.StatusCode; snippet: `func (he *HTTPError) StatusCode() int`].
   - `Error` (`httperror.go:120`) — returns the error string [snippet: `func (he *HTTPError) Error() string`].
   - `Wrap` (`httperror.go:132`) — "returns new HTTPError with given errors wrapped inside" [FOCUS: HTTPError.Wrap; snippet: `func (he HTTPError) Wrap(err error) error`].
   - `Unwrap` (`httperror.go:140`) — for error chain unwrapping [snippet: `func (he *HTTPError) Unwrap() error`].
   - Created via `NewHTTPError` (`httperror.go:99`): `func NewHTTPError(code int, message string) *HTTPError` [snippet].

2. **`httpError`** (`httperror.go:144`) — a separate unexported error type with methods `Error`, `StatusCode`, `Wrap` [FOCUS: httpError]. Its `Error` method delegates to `http.StatusText` — **`DELEGATE(http.StatusText -> result)`** — meaning it produces standard HTTP status text (e.g., "Not Found") rather than custom messages [FOCUS: httpError.Error]. Its `StatusCode` method (`httperror.go:148`) returns the code [snippet: `func (he httpError) StatusCode() int`].

3. **`HTTPStatusCoder`** (`httperror.go:39`) — an interface that "errors can implement to produce status code for HTTP response" [FOCUS: HTTPStatusCoder; snippet: `type HTTPStatusCoder interface`]. This allows any error type to participate in status code resolution.

### Status Code Resolution

The standalone `StatusCode` function (`httperror.go:45`) extracts a status code from any error [SYM: StatusCode — "returns status code from error if it..."; snippet: `func StatusCode(err error) int`].

**`ResolveResponseStatus`** (`httperror.go:66`) is the key function for determining what status code to send. Its behavior: **`GUARD(resp != nil && resp.Committed -> return resp, http.S...); PRECEDENCE(resp -> err)`** [FOCUS: ResolveResponseStatus]. This reveals:
- **Committed response guard**: If the response is already committed (`resp.Committed` is true), the function **short-circuits** and returns the response with its already-sent status (likely `http.StatusOK` or whatever was already written). It does *not* attempt to change the status code.
- **Precedence**: When the response is not committed, it evaluates `resp` first, then `err` — meaning the response's state takes priority, and the error is used to determine the status code only if the response hasn't been partially written.

It calls `StatusCode` to extract the code from the error [FOCUS: ResolveResponseStatus — "calls: StatusCode"].

### Response Commitment Mechanics

`Response` (`response.go:18`) wraps `http.ResponseWriter` with methods: `After`, `Before`, `Flush`, `Hijack`, `Unwrap`, `Write`, `WriteHeader` [FOCUS: Response].

`Response.WriteHeader` (`response.go:49`) has critical behavior: **`GUARD(r.Committed -> return); ACCUMULATE(fn loop -> result)`** [FOCUS: Response.WriteHeader]. This means:
- Once `Committed` is true, subsequent `WriteHeader` calls are **silently ignored**.
- Before writing the header, it runs accumulated `Before` callback functions (the ACCUMULATE pattern over `fn loop`).

`Response.Before` (`response.go:36`) and `Response.After` (`response.go:41`) register callbacks that run before/after the header is written [snippets: `func (r *Response) Before(fn func())`, `func (r *Response) After(fn func())`].

`Response.Flush` (`response.go:81`) panics if flushing is not supported — `GUARD(err != nil && errors.Is(err, http.ErrNotSuppo... -> panic(fmt.Errorf("...")))` [FOCUS: Response.Flush]. `Response.Hijack` (`response.go:92`) delegates to `http.NewResponseController` for connection takeover [FOCUS: Response.Hijack].

### The `delayedStatusWriter` Wrapper

`delayedStatusWriter` (`response.go:136`) is "a wrapper around http.ResponseWriter that delays writing the status code until first Write is called" [FOCUS: delayedStatusWriter]. It has methods: `Flush`, `Hijack`, `Unwrap`, `Write`, `WriteHeader` [FOCUS: delayedStatusWriter; snippets for each]. This means the error handler can potentially set a status code via `WriteHeader`, but the actual write to the network is deferred until response body data is written — allowing the error handler to modify the status before any bytes are sent.

### Unwrapping Response Writers

`UnwrapResponse` (`response.go:120`) unwraps a `ResponseWriter` to find the original Echo `Response` — **`ACCUMULATE(loop -> result)`**, calling `Unwrap` [FOCUS: UnwrapResponse]. `Response.Unwrap` (`response.go:105`) returns the original `http.ResponseWriter` [FOCUS: Response.Unwrap]. This unwrapping chain is necessary because middleware may wrap the response writer (e.g., `gzipResponseWriter` in `middleware/compress.go`).

### Error Flow Summary

1. A handler returns an `error` (ordinary Go error, `*HTTPError`, or any `HTTPStatusCoder` implementor).
2. `Echo.serveHTTP` catches the error in its deferred cleanup [FOCUS: Echo.serveHTTP — "UNWIND(defer)"].
3. `ResolveResponseStatus` checks if the response is already committed [FOCUS: ResolveResponseStatus — committed guard].
4. If **committed**: the error handler cannot change the status code — `Response.WriteHeader` is a no-op [FOCUS: Response.WriteHeader — "GUARD(r.Committed -> return)"].
5. If **not committed**: the error's status code is extracted via `StatusCode`/`HTTPStatusCoder` interface [FOCUS: StatusCode, HTTPStatusCoder]. For `HTTPError`, the code comes from `HTTPError.StatusCode` (`httperror.go:115`); for `httpError`, from `httpError.StatusCode` (`httperror.go:148`); for ordinary errors without `HTTPStatusCoder`, the default behavior is implied by the PRECEDENCE annotation.
6. `DefaultHTTPErrorHandler` (configured with `exposeError`) formats and sends the error response.
7. `delayedStatusWriter` ensures the status code is not flushed to the network until actual body bytes are written [FOCUS: delayedStatusWriter].

### What Cannot Be Determined

- The **full body of `DefaultHTTPErrorHandler`** is not provided — only its signature (`func DefaultHTTPErrorHandler(exposeError bool) HTTPErrorHandler`) [snippet]. The exact formatting logic (JSON vs. plain text, what fields are included when `exposeError` is true vs. false) is not visible.
- The **full body of `Echo.serveHTTP`** is not provided — only the behavior annotation. The exact point at which the error handler is called (and whether it's in a `defer` or in-line after handler return) cannot be confirmed with certainty [GAPS: uncovered includes Echo.AddRoute, Echo.RouteNotFound, Echo.Use, Echo.AcquireContext].
- The **default status code for ordinary (non-HTTP) errors** is not explicitly stated. The `StatusCode` function's full logic is not shown — only that it "returns status code from error if it..." (truncated) [SYM: StatusCode, httperror.go:45].
- Whether the error handler **logs** the error or only sends it to the client is not determinable from the clue [no logging references in FOCUS for error handling].
- The interaction between `RecoverConfig.ToMiddleware` (which catches panics) and the error handler path is not detailed here — only that `RecoverConfig.ToMiddleware` "raises: panic" is noted in the struct-1 clue but not in this mech-2 prompt's FOCUS [not in mech-2 FOCUS].
- Whether `delayedStatusWriter` is used in the error path specifically, or only for normal responses, cannot be confirmed — its description is general [FOCUS: delayedStatusWriter description].
- The `ValueExtractorError.Error` (`middleware/extractor.go:42`) "returns errors text" is mentioned but its relationship to the centralized error handler is not clarified [FOCUS: ValueExtractorError.Error].
