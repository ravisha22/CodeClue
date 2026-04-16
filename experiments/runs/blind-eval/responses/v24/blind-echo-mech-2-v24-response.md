# v2.4 Response: blind-echo-mech-2
Date: 2026-04-16

## Question
What happens inside Echo's centralized HTTP error path when handlers return ordinary errors, HTTP errors, or errors after the response is already committed?

## Answer

### 1. The Error Handling Entry Point

Echo's centralized error handling is driven by `DefaultHTTPErrorHandler` (`DefaultHTTPErrorHandler`, echo.go:374, snippet: `func DefaultHTTPErrorHandler(exposeError bool) HTTPErrorHandler`). This function is a factory that creates an error handler, and it is called during `New` (`New`, echo.go:333, `called_by: New`). The `exposeError bool` parameter controls whether error details are exposed in the HTTP response.

The error handler is invoked from `Echo.serveHTTP` (`Echo.serveHTTP`, echo.go:700, snippet: `func (e *Echo) serveHTTP(w http.ResponseWriter, r *http.Request)`) when a handler or middleware returns a non-nil error.

### 2. Error Type Hierarchy

Echo distinguishes between several error types:

#### a. `HTTPError` (Public, exported)

`HTTPError` (`HTTPError`, httperror.go:107, snippet: `type HTTPError struct`) "represents an error that occurred while handling a request." It provides:

- `HTTPError.StatusCode` (`HTTPError.StatusCode`, httperror.go:115, snippet: `func (he *HTTPError) StatusCode() int`) — returns the HTTP status code.
- `HTTPError.Error` (`HTTPError.Error`, httperror.go:120, snippet: `func (he *HTTPError) Error() string`) — returns the error message.
- `HTTPError.Unwrap` (`HTTPError.Unwrap`, httperror.go:140, snippet: `func (he *HTTPError) Unwrap() error`) — supports Go's error unwrapping chain.
- `HTTPError.Wrap` (`HTTPError.Wrap`, httperror.go:132, snippet: `func (he HTTPError) Wrap(err error) error`) — "returns new HTTPError with given errors wrapped inside."
- Created via `NewHTTPError` (`NewHTTPError`, httperror.go:99, snippet: `func NewHTTPError(code int, message string) *HTTPError`).

#### b. `httpError` (Private, unexported)

`httpError` (`httpError`, httperror.go:144, snippet: `type httpError struct`) is an unexported error type with methods:

- `httpError.StatusCode` (`httpError.StatusCode`, httperror.go:148, snippet: `func (he httpError) StatusCode() int`) — returns a status code.
- `httpError.Error` (`httpError.Error`, httperror.go:152) — behavior `DELEGATE(http.StatusText -> result)`, meaning it returns the standard HTTP status text for its code.
- `httpError.Wrap` (`httpError.Wrap`, httperror.go:156, snippet: `func (he httpError) Wrap(err error) error`).

#### c. `HTTPStatusCoder` Interface

`HTTPStatusCoder` (`HTTPStatusCoder`, httperror.go:39, snippet: `type HTTPStatusCoder interface`) is an interface that "errors can implement to produce status code for HTTP response." Both `HTTPError` and `httpError` implement this interface.

### 3. Status Code Extraction

The standalone function `StatusCode` (`StatusCode`, httperror.go:45, snippet: `func StatusCode(err error) int`) extracts a status code from any error. It works by checking if the error implements the `HTTPStatusCoder` interface.

### 4. Response Commitment Detection: `ResolveResponseStatus`

`ResolveResponseStatus` (`ResolveResponseStatus`, httperror.go:66, snippet: `func ResolveResponseStatus(rw http.ResponseWriter, err error) (resp *Response, status int)`) is the key function that determines what to do based on response state. Its behavior annotation reveals:

```
GUARD(resp != nil && resp.Committed -> return resp, http.S...)
PRECEDENCE(resp -> err)
```

This tells us:

1. **If the response is already committed** (`resp.Committed` is true), the function returns early with the response and an HTTP status (likely `http.StatusOK` or the already-written status — the annotation is truncated at `http.S...`). This means **no further status code can be written** once the response is committed.

2. **Otherwise**, it evaluates with `PRECEDENCE(resp -> err)` — first checking the response object, then the error — and calls `StatusCode` to extract the appropriate HTTP status from the error.

### 5. Response Commitment Mechanism

The **`Response`** struct (`Response`, response.go:18, snippet: `type Response struct`) wraps `http.ResponseWriter`. It tracks commitment through `Response.WriteHeader` (`Response.WriteHeader`, response.go:49):

```
GUARD(r.Committed -> return)
ACCUMULATE(fn loop -> result)
```

This reveals:
- **Once committed, `WriteHeader` is a no-op** — the `GUARD(r.Committed -> return)` prevents writing headers twice.
- Before writing, it runs accumulated `Before` functions (`Response.Before`, response.go:36, snippet: `func (r *Response) Before(fn func())`).
- `Response.After` (`Response.After`, response.go:41, snippet: `func (r *Response) After(fn func())`) registers post-write callbacks.

`Response.Write` (`Response.Write`, response.go:63) has behavior `ACCUMULATE(fn loop -> result)` and calls `WriteHeader` — meaning writing body data also triggers header commitment if not already done.

### 6. The `delayedStatusWriter`

A `delayedStatusWriter` (`delayedStatusWriter`, response.go:136, snippet: `type delayedStatusWriter struct`) wraps the response writer with delayed header writing:

- `delayedStatusWriter.WriteHeader` (response.go:142) — stores the status code without immediately writing it.
- `delayedStatusWriter.Write` (response.go:148) — writes data, presumably flushing the delayed status first.
- It also implements `Flush` (response.go:159), `Hijack` (response.go:166), and `Unwrap` (response.go:170).

This mechanism likely allows the error handler to modify the status code before it's actually sent to the client.

### 7. Response Unwrapping

`UnwrapResponse` (`UnwrapResponse`, response.go:120, snippet: `func UnwrapResponse(rw http.ResponseWriter) (*Response, error)`) unwraps a `ResponseWriter` to find the original Echo `Response`. Its behavior `ACCUMULATE(loop -> result)` with call to `Unwrap` suggests it iterates through wrapper layers (e.g., middleware wrappers like `gzipResponseWriter`) to find the underlying `Response`. This is used by the error handler to access commitment state.

`Response.Unwrap` (`Response.Unwrap`, response.go:105) returns the original `http.ResponseWriter`, called by `UnwrapResponse`.

### 8. Error Flow Summary

Based on the clue evidence, the error path works as follows:

1. **Handler returns an error** → `Echo.serveHTTP` receives it.
2. **Error handler is invoked** — the `DefaultHTTPErrorHandler` (or a custom one).
3. **`ResolveResponseStatus` is called** to determine the appropriate action:
   - **If response is already committed** → returns early; the error handler cannot change the status code or write a new response body. The error is effectively swallowed (or logged).
   - **If response is not committed** → extracts the status code:
     - **For `HTTPError`** — uses `HTTPError.StatusCode` directly (e.g., 404, 500).
     - **For ordinary errors** (not implementing `HTTPStatusCoder`) — `StatusCode` likely returns a default (presumably 500 Internal Server Error, though the exact default is not shown in the clue).
     - **For `httpError`** (private) — uses `httpError.StatusCode` and `httpError.Error` returns `http.StatusText`.
4. **Response is written** — the error handler sends the error response with the determined status code, using `Response.WriteHeader` which commits the response.
5. **The `exposeError` flag** controls whether the error message/details are included in the response body.

### 9. Middleware Interaction with Error Path

Middleware wrappers like `gzipResponseWriter` (`gzipResponseWriter.WriteHeader`, middleware/compress.go:147) and `bodyDumpResponseWriter` (`bodyDumpResponseWriter.Write`, middleware/body_dump.go:150) wrap the response writer. When errors occur after such wrapping, `UnwrapResponse` traverses the wrapper chain to find the original `Response` and check its committed state.

The `isIgnorableOpenFileError` function (`isIgnorableOpenFileError`, middleware/static_other.go:13) has behavior `GUARD(os.IsNotExist(err) -> return true)` — static middleware ignores file-not-found errors so that other route handlers can match, rather than sending an error response.

### Cannot Be Determined from the Clue File

- **The full body of `DefaultHTTPErrorHandler`** — only the signature and that it's called by `New` are known. The exact logic for formatting error responses (JSON vs. plain text, message construction) is not available.
- **The full body of `Echo.serveHTTP`** — how exactly it invokes the error handler and what happens with the error after the handler returns is not shown.
- **The default status code for non-`HTTPStatusCoder` errors** — whether `StatusCode` returns 500 by default is not explicitly stated.
- **The truncated return value in `ResolveResponseStatus`'s GUARD** — `http.S...` is cut off; the exact status returned when the response is already committed is unknown.
- **Whether the error handler logs errors** — no logging behavior is described in the clue entries.
- **The `bodyDumpResponseWriter.WriteHeader`** behavior — listed as uncovered in GAPS.
