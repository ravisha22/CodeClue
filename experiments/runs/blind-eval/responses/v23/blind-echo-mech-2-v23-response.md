# v2.3 Response: blind-echo-mech-2
Date: 2026-04-15

## Summary

Echo's centralized HTTP error path is managed by `DefaultHTTPErrorHandler` (`echo.go:374`), which is wired up during framework initialization. It handles ordinary errors, HTTP-typed errors (via `HTTPError` and the `HTTPStatusCoder` interface), and must account for already-committed responses. The `Response` wrapper tracks whether headers have already been sent.

## Detailed Analysis

### The Default HTTP Error Handler

- **`DefaultHTTPErrorHandler`** (`echo.go:374`) creates the default error handler implementation. Its signature is `DefaultHTTPErrorHandler(exposeError bool)`, taking a boolean that controls whether error details are exposed to the client (FOCUS: `DefaultHTTPErrorHandler`).
- It is called by **`New`** (`echo.go:333`), meaning every new Echo instance automatically gets this handler (FOCUS: `DefaultHTTPErrorHandler` — `called_by: New`).

### HTTP Error Types and Status Code Resolution

- **`HTTPError`** (`httperror.go`) is the structured error type with methods:
  - **`HTTPError.StatusCode`** (`httperror.go:115`) — returns the HTTP status code for the response (FOCUS: `HTTPError.StatusCode`).
  - **`HTTPError.Wrap`** (`httperror.go:132`) — returns a new `HTTPError` with given errors wrapped inside, enabling error chaining (FOCUS: `HTTPError.Wrap`).
- **`httpError`** (lowercase, `httperror.go:144`) is a concrete type with methods `Error`, `StatusCode`, and `Wrap` (FOCUS: `httpError`):
  - **`httpError.Error`** (`httperror.go:152`) delegates to `http.StatusText` — behavior: `DELEGATE(http.StatusText -> result)`, meaning for this error type the error message is derived from the standard HTTP status text (FOCUS: `httpError.Error`).
  - **`httpError.StatusCode`** (`httperror.go:148`) returns the status code directly (FOCUS: `httpError.StatusCode`).
  - **`httpError.Wrap`** (`httperror.go:156`) wraps another error (FOCUS: `httpError.Wrap`).

- **`HTTPStatusCoder`** (`httperror.go:39`) is an interface that any error can implement to produce a status code for the HTTP response (FOCUS: `HTTPStatusCoder`). This is the abstraction that allows the error handler to extract status codes from arbitrary error types.

- **`StatusCode`** function (`httperror.go:45`) is a standalone helper that returns a status code from an error if it implements the appropriate interface (SYM: `StatusCode`).

### Status Code Resolution Logic

- **`ResolveResponseStatus`** (`httperror.go:66`) determines what HTTP status code should be (or has been) sent. Its signature is `ResolveResponseStatus(rw http.ResponseWriter, err error)` (FOCUS: `ResolveResponseStatus`).
  - Behavior: `GUARD(resp -> pass_through); PRECEDENCE(resp -> err)` — this means:
    1. It first checks the response (`resp`); if the response already has a status, it passes through (guard).
    2. The `PRECEDENCE(resp -> err)` indicates the response's existing status takes precedence over the error's status code.
  - It calls **`StatusCode`** to extract the status from the error (FOCUS: `ResolveResponseStatus` — `calls: StatusCode`).

### Response Commitment Detection

- **`Response`** (`response.go:18`) wraps `http.ResponseWriter` and tracks response state (FOCUS: `Response`).
- **`Response.WriteHeader`** (`response.go:49`) sends the HTTP response header with a status code. Its behavior is `GUARD(r -> none); ACCUMULATE(loop -> result)` (FOCUS: `Response.WriteHeader`):
  - The `GUARD(r -> none)` suggests it checks whether the response is already committed — if so, it does nothing (returns none).
  - `called_by: Write, WriteHeader` indicates it's invoked both directly and by the `Write` method, ensuring the status header is always sent before body data.
- **`delayedStatusWriter`** (`response.go:136`) is a wrapper that delays writing the status code until the first `Write` call. It has methods `Flush, Hijack, Unwrap, Write, WriteHeader` (FOCUS: `delayedStatusWriter`). This enables the error handler to potentially modify the status before any bytes are written.

### Request Lifecycle and Error Handling Flow

- **`Echo.ServeHTTP`** (`echo.go:695`) implements the `http.Handler` interface (FOCUS: `Echo.ServeHTTP`).
- **`Echo.serveHTTP`** (`echo.go:700`) is the internal implementation with behavior `GUARD(e -> h1); DELEGATE(h1 -> result); UNWIND(defer)` (FOCUS: `Echo.serveHTTP`):
  - `GUARD(e -> h1)` — constructs the handler chain.
  - `DELEGATE(h1 -> result)` — executes the handler chain.
  - `UNWIND(defer)` — indicates deferred cleanup (likely including error handling) after the handler chain completes.
  - It calls `applyMiddleware` to build the middleware chain (FOCUS: `Echo.serveHTTP` — `calls: applyMiddleware`).

### What Happens for Each Error Type

**1. Ordinary errors (non-HTTP errors)**:
- When a handler returns a plain `error` (not implementing `HTTPStatusCoder`), `StatusCode` (`httperror.go:45`) would fail to extract a status code. `ResolveResponseStatus` would then fall through from its `PRECEDENCE(resp -> err)` logic — if the response has no status yet, the error handler likely defaults to HTTP 500 (Internal Server Error). The `httpError.Error` behavior of `DELEGATE(http.StatusText -> result)` supports this — ordinary errors without a code map to a generic status text.

**2. HTTP errors (implementing HTTPStatusCoder)**:
- Errors implementing `HTTPStatusCoder` (`httperror.go:39`) or typed as `HTTPError` provide a `StatusCode()` method. `ResolveResponseStatus` calls `StatusCode` to extract the code (FOCUS: `ResolveResponseStatus` — `calls: StatusCode`).
- The `exposeError` parameter of `DefaultHTTPErrorHandler` (`echo.go:374`) controls whether the error's message/details are included in the response body.

**3. Errors after response is already committed**:
- `Response.WriteHeader` (`response.go:49`) has `GUARD(r -> none)` — if headers are already sent, subsequent `WriteHeader` calls are no-ops.
- `ResolveResponseStatus` has `GUARD(resp -> pass_through)` — if the response already has a status, it passes through without modification.
- This means once a response is committed (headers written), the error handler cannot change the status code. The error is effectively swallowed at the HTTP response level, though it may still be logged.

### Response Unwrapping

- **`Response.Unwrap`** (`response.go:105`) returns the original `http.ResponseWriter` (FOCUS: `Response.Unwrap`).
- **`UnwrapResponse`** (`response.go:120`) unwraps a given `ResponseWriter` to return the context's original Echo `Response`, using an accumulation loop that calls `Unwrap` repeatedly (FOCUS: `UnwrapResponse` — behavior: `ACCUMULATE(loop -> result)`). This is relevant for middleware like gzip that wrap the response writer.

## Uncertainty / Limits

- **Exact body of `DefaultHTTPErrorHandler`**: The clue file does not provide the full implementation body. The specific logic for choosing response content type (JSON vs plain text), logging behavior, and exact fallback status code for non-HTTP errors cannot be confirmed from the available data.
- **Error logging**: Whether and how errors are logged when the response is already committed is not documented in the clue file.
- **`delayedStatusWriter` integration**: How exactly this interacts with the error handler flow (whether the error handler uses it or it's only for normal responses) is not fully specified.
- **GAPS annotation** confirms this is a `STRUCTURAL` gap type with "80 symbols in L3, 39 with behavior annotations" — substantial but not complete behavioral coverage.
