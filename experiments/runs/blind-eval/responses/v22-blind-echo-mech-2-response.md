# v2.2 Response: blind-echo-mech-2
Date: 2026-04-15

## Question
What happens inside Echo's centralized HTTP error path when handlers return ordinary errors, HTTP errors, or errors after the response is already committed?

## Answer

### 1. The Centralized Error Handler

**`DefaultHTTPErrorHandler`** (echo.go:374) — "creates new default HTTP error handler implementation." Signature: `func DefaultHTTPErrorHandler(exposeError bool) HTTPErrorHandler`. Behavior annotation:

```
GUARD(r -> code); PRECEDENCE(r -> errors -> tmp); DISPATCH(m)
```

This reveals the error handler's internal logic:

1. **GUARD(r -> code)** — Guards on the response to derive an HTTP status code. This likely checks whether the response has already been committed.
2. **PRECEDENCE(r -> errors -> tmp)** — Applies precedence logic: first checks the response (`r`), then inspects the error chain (`errors`), and uses a temporary variable (`tmp`) — suggesting it unwraps errors to find the most specific type.
3. **DISPATCH(m)** — Dispatches based on some discriminator `m`, likely the HTTP method or message format, to determine how to render the error response.

The `exposeError bool` parameter controls whether internal error details are exposed in responses.

### 2. Error Type Hierarchy

**`HTTPError`** (httperror.go:107) — "represents an error that occurred while handling a request." Methods:
- `HTTPError.StatusCode` (httperror.go:115) — "returns status code for HTTP response."
- `HTTPError.Wrap` (httperror.go:132) — "returns new HTTPError with given errors wrapped inside."
- `HTTPError.Error` — inherited from the error interface.
- `HTTPError.Unwrap` — for error chain traversal.

**`httpError`** (httperror.go:144) — an unexported type with methods:
- `httpError.Error` (httperror.go:152) — behavior: `DELEGATE(http.StatusText -> result)`. This means the unexported error type produces its error message by looking up the standard HTTP status text.
- `httpError.StatusCode` (httperror.go:148) — returns the status code.
- `httpError.Wrap` (httperror.go:156) — wraps another error.

**`HTTPStatusCoder`** (httperror.go:39) — "interface that errors can implement to produce status code for HTTP response." This is the general interface the error handler checks to determine status codes from arbitrary error types.

**`BindingError`** (binder.go:69) — "represents an error that occurred while binding request data." Its `Error` method (binder.go:87) has behavior `DELEGATE(fmt.Sprintf -> result)` and is called by `bool`, `durations`, `float`, `int`, `uint` binding operations.

### 3. How Different Error Types Are Handled

Based on the `PRECEDENCE(r -> errors -> tmp)` in `DefaultHTTPErrorHandler`:

**Ordinary errors (plain `error` interface):**
- The handler receives a plain error that does not implement `HTTPStatusCoder` or is not an `HTTPError`.
- The `PRECEDENCE` pattern suggests the handler first checks if the error can be unwrapped or type-asserted to a more specific type. If not, it likely defaults to HTTP 500 Internal Server Error.
- The `exposeError` parameter controls whether the error message is included in the response body.

**HTTP errors (`HTTPError` or `HTTPStatusCoder` implementors):**
- `HTTPError.StatusCode` (httperror.go:115) provides the status code directly.
- The `HTTPStatusCoder` interface (httperror.go:39) allows any error to provide a status code.
- The PRECEDENCE logic (`errors -> tmp`) suggests the handler walks the error chain (using `Unwrap`) to find the most relevant `HTTPError` or `HTTPStatusCoder`.

**`httpError` (unexported):**
- `httpError.Error` (httperror.go:152) delegates to `http.StatusText`, so its error message is the standard text for its status code.
- `httpError.StatusCode` (httperror.go:148) provides the numeric code.

### 4. Response Already Committed

**`Response.WriteHeader`** (response.go:49) — "sends an HTTP response header with status code." Behavior: `GUARD(r -> result); ACCUMULATE(loop -> result)`. The GUARD pattern suggests it checks whether the response has already been committed (headers already sent) before writing.

**`ResolveResponseStatus`** (httperror.go:66) — "returns the Response and HTTP status code that should be (or has been) sent for rw, given an optional error." Behavior: `GUARD(resp -> result); PRECEDENCE(resp)`. This function:
- Guards on the response object to determine its current state.
- Uses precedence on the response to decide whether to use the already-committed status or derive a new one from the error.

The `GUARD(r -> code)` in `DefaultHTTPErrorHandler` (echo.go:374) likely uses `ResolveResponseStatus` or similar logic to detect committed responses. When the response is already committed, writing a new status code or body would be impossible — the handler likely logs the error but cannot change the response.

**`Response`** (response.go:18) — "wraps an http.ResponseWriter and implements its interface." Methods include `Before` and `After` hooks, `Flush`, `Hijack`, `Unwrap`, `Write`, `WriteHeader`. The `Before`/`After` hooks suggest lifecycle callbacks that fire around response writing.

**`delayedStatusWriter`** (response.go:136) — "a wrapper around http.ResponseWriter that delays writing the status code until first Write is called." Methods: `Flush`, `Hijack`, `Unwrap`, `Write`, `WriteHeader`. This suggests Echo delays committing the response status until actual body content is written, giving the error handler a window to modify the status code even after `WriteHeader` was called, as long as no body bytes have been flushed.

### 5. The Dispatch Flow

The `DISPATCH(m)` in `DefaultHTTPErrorHandler` suggests the error handler dispatches based on a discriminator (likely the request method or content type) to decide the response format. For example, HEAD requests might not include a body, while other methods might render JSON or plain text error messages.

### 6. Error Handler in the Request Lifecycle

**`Echo.serveHTTP`** (echo.go:700) — "implements `http.Handler` interface, which serves HTTP requests." Behavior: `DELEGATE(h1 -> result); UNWIND(defer)`. The `UNWIND(defer)` suggests deferred cleanup, and the handler chain's error return is likely caught and passed to the error handler.

**`Echo.ServeHTTP`** (echo.go:695) — the public entry point that delegates to `serveHTTP`.

### 7. Middleware Error Wrapping

Several middleware create custom response writers that also handle errors:

- `bodyDumpResponseWriter.Hijack` (middleware/body_dump.go:161) — delegates to `http.NewResponseController`.
- `gzipResponseWriter.Hijack` (middleware/compress.go:201) — delegates to `http.NewResponseController`.
- `gzipResponseWriter.WriteHeader` (middleware/compress.go:147) — intercepts status code writing.
- `UnwrapResponse` (response.go:120) — "unwraps given ResponseWriter to return context's original Echo Response." Behavior: `ACCUMULATE(loop -> result); DISPATCH(t)`. This traverses wrapped response writers to find the original.

### 8. What Cannot Be Determined

- **The exact conditional logic** inside `DefaultHTTPErrorHandler` that decides between returning JSON vs. plain text error responses — only `DISPATCH(m)` hints at method/format-based dispatch.
- **Whether the error handler silently drops errors** when the response is committed, or whether it logs them — the clue does not show logging behavior.
- **The full error unwrapping chain** — while `PRECEDENCE(r -> errors -> tmp)` shows unwrapping occurs, the exact depth and types checked are not detailed.
- **How `exposeError` affects the response body** — the parameter name suggests it controls whether internal error messages are shown to clients, but the exact rendering logic is not in the clue.
