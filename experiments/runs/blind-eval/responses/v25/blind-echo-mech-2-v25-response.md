# v2.5 Response: blind-echo-mech-2
Date: 2026-04-16

## Question

What happens inside Echo's centralized HTTP error path when handlers return ordinary errors, HTTP errors, or errors after the response is already committed?

## Analysis

### 1. The Request Lifecycle: serveHTTP as the Entry Point

`Echo.ServeHTTP` (echo.go:695) implements `http.Handler` and is the outermost entry point. It delegates to `Echo.serveHTTP` (echo.go:700), whose behavior is:

> GUARD(e.premiddleware == nil → return h1(cc)); DELEGATE(h1 → result); UNWIND(defer)

This tells us that the handler chain (`h1`) is invoked, and its return value — an `error` or `nil` — flows back through `serveHTTP`. The `UNWIND(defer)` indicates deferred cleanup runs after the handler chain completes, regardless of whether an error occurred.

**Supported by clue:** The GUARD/DELEGATE/UNWIND pattern is explicitly annotated.

### 2. DefaultHTTPErrorHandler: The Centralized Error Processor

`DefaultHTTPErrorHandler` (echo.go:374) is the function that processes errors returned from the handler chain. The source snippet confirms its signature:

```go
func DefaultHTTPErrorHandler(exposeError bool) HTTPErrorHandler {
```

It returns an `HTTPErrorHandler` — a function that takes the error and the `Context` to produce an HTTP response. The `exposeError` parameter controls whether internal error details are exposed to the client.

**Supported by clue:** Source snippet directly confirms signature and the `exposeError` parameter.

### 3. Error Type Discrimination: HTTPError vs. Ordinary Errors

The error-handling path discriminates between error types using the `HTTPError` and related interfaces:

#### HTTPError (httperror.go:107)
"Represents an error that occurred while handling a request." It exposes `StatusCode()` (httperror.go:115) and `Error()`, plus `Unwrap()` for error chain traversal and `Wrap()` for adding context. The `StatusCode` method "returns status code for HTTP response."

#### HTTPStatusCoder (httperror.go:39)
An interface that "errors can implement to produce status code for HTTP response." This means any error implementing `StatusCode() int` can participate in status-code resolution — not just `HTTPError`.

#### httpError (httperror.go:144)
An unexported type with `Error()` (which `DELEGATE(http.StatusText → result)` — it returns the standard HTTP status text) and `StatusCode()` (httperror.go:148). This is called by `DefaultHTTPErrorHandler`.

#### StatusCode function (httperror.go:45)
A standalone function with source: `func StatusCode(err error) int {`. This extracts the status code from any error, likely by checking if the error implements `HTTPStatusCoder`.

**Supported by clue:** All types, methods, and the standalone `StatusCode` function are documented. The call chain from `DefaultHTTPErrorHandler` to `httpError.StatusCode` is confirmed.

**How this produces behavior for each error type:**

- **HTTPError returned:** `DefaultHTTPErrorHandler` can directly call `.StatusCode()` to get the HTTP status code and `.Error()` to get the message. If `exposeError` is true, the full error message is sent to the client; otherwise, a generic message is used.
- **Ordinary error returned:** The `StatusCode` function (httperror.go:45) is used to extract a status code. If the error does not implement `HTTPStatusCoder`, the status defaults to 500 (inferred — the clue does not state the default explicitly, but this is the standard behavior for untyped errors).
- **Error implementing HTTPStatusCoder:** The `StatusCode` function detects the interface and returns the custom status code.

**Uncertain:** The exact branching logic inside `DefaultHTTPErrorHandler` (how it decides between `HTTPError`, `HTTPStatusCoder`, and plain errors) is not fully detailed in the clue. The 500-default for plain errors is inferred.

### 4. The Committed Response Guard

The most mechanistically clear part of the clue concerns what happens when the response is already committed:

#### Response.WriteHeader (response.go:49)
> GUARD(r.Committed → return); ACCUMULATE(fn loop → result)

Once `r.Committed` is true, `WriteHeader` returns immediately without writing. The `ACCUMULATE(fn loop → result)` suggests that before writing the header, it runs a loop of callback functions (the `Before` callbacks).

#### Response.Write (response.go:63)
Writes response body data. Once `WriteHeader` has been called (setting `Committed`), subsequent writes append to the body but cannot change the status code.

#### ResolveResponseStatus (httperror.go:66)
> GUARD(resp != nil && resp.Committed → return resp, http.S...); PRECEDENCE(resp → err)

This is critical: when `resp.Committed` is true, this function short-circuits and returns the already-committed response status (the truncated `http.S...` likely refers to `http.StatusOK` or the already-written status). It does **not** attempt to override the committed status with the error's status code.

The `PRECEDENCE(resp → err)` annotation confirms that the response's current state takes priority over the error when determining the final status.

**Supported by clue:** The Committed guard in `WriteHeader` and `ResolveResponseStatus` are both explicitly annotated. The behavior is mechanistically clear: once committed, the error handler cannot change the HTTP status code.

**What this means for "error after commit":**

1. Handler writes part of the response (e.g., calls `c.String()` or `c.JSON()`), which triggers `Response.WriteHeader` and sets `Committed = true`.
2. Handler then returns an error.
3. `DefaultHTTPErrorHandler` is invoked with the error.
4. It calls `ResolveResponseStatus`, which detects `resp.Committed` and short-circuits — returning the already-written status.
5. Any attempt to call `Response.WriteHeader` again is silently ignored due to the `GUARD(r.Committed → return)`.
6. The error is effectively swallowed from the client's perspective — the client sees the original (pre-error) response.

### 5. Response Callbacks and Wrapping

#### Response.Before and Response.After
The clue mentions these as callbacks on the `Response` type. `Before` callbacks run inside `WriteHeader` (the `ACCUMULATE(fn loop → result)` in `WriteHeader`'s behavior) — they execute just before the status code is written. `After` callbacks (listed in GAPS as uncovered) presumably run after the response is written.

#### delayedStatusWriter (response.go:136)
An additional response wrapper with its own `WriteHeader`, `Write`, `Flush`, `Hijack`, and `Unwrap` methods. This wrapper likely defers the status-code write, allowing middleware or error handlers to adjust the status before it is actually sent to the client. This is relevant to the error path: if a `delayedStatusWriter` is in use, the error handler may still be able to set the status code even after `Write` has been called, as long as the delayed writer hasn't flushed.

**Uncertain:** The exact semantics of `delayedStatusWriter` are not fully described in the clue. Its interaction with the `Committed` flag is not specified — it may set `Committed` only upon flush rather than upon the first `Write`.

#### Response.Unwrap (response.go:105)
Returns the original `http.ResponseWriter`. Called by `DefaultHTTPErrorHandler` and `UnwrapResponse` (response.go:120). This suggests the error handler may need to unwrap layered response writers to access the underlying Echo `Response` and check `Committed` status.

**Supported by clue:** `Unwrap` being called by `DefaultHTTPErrorHandler` is explicitly documented.

### 6. NewHTTPError: Error Construction

`NewHTTPError` (httperror.go:99) has source: `func NewHTTPError(code int, message string) *HTTPError {`. This is the constructor for creating HTTP errors with a specific status code and message. Handlers use this to signal specific HTTP error responses (e.g., `NewHTTPError(404, "not found")`).

**Supported by clue:** Source snippet directly confirms.

### 7. Context and Route Integration

`Context.SetResponse` (context.go:145) is called by `json`, `WrapMiddleware`, and `ToMiddleware`, confirming that the response object is set on the context and accessible throughout the handler chain. `Context.RouteInfo` (context.go:225) provides route metadata but is guarded by `GUARD(c.route != nil → return c.route.Clone())` — it clones the route info to prevent mutation.

**Supported by clue:** Directly documented.

## Summary of the Error Path

| Scenario | Mechanism | Outcome |
|---|---|---|
| Handler returns `*HTTPError` | `DefaultHTTPErrorHandler` reads `.StatusCode()` and `.Error()` | HTTP response with the specified status code and message (filtered by `exposeError`) |
| Handler returns ordinary `error` | `StatusCode()` function checks for `HTTPStatusCoder` interface; falls back to 500 | HTTP 500 (or custom code if `HTTPStatusCoder` is implemented) |
| Handler returns error after response committed | `ResolveResponseStatus` detects `resp.Committed` and short-circuits; `WriteHeader` guard prevents status override | Client sees the original response; error is not reflected in HTTP status |
| `delayedStatusWriter` in use | Status write is deferred; error handler may still adjust status before flush | Status may be changeable until flush (uncertain — details not in clue) |
| No route matched | `RouteNotFound` handler fires | Custom 404 behavior if registered; otherwise default error handling |

## Confidence Assessment

| Claim | Confidence | Basis |
|---|---|---|
| `DefaultHTTPErrorHandler` is the centralized error processor | High | Directly documented with source snippet |
| `HTTPError.StatusCode()` provides the HTTP status for HTTP errors | High | Explicitly documented |
| `StatusCode()` standalone function extracts code from any error | High | Source snippet confirmed |
| Plain errors default to 500 | Medium | Inferred — not explicitly stated in clue |
| Committed response prevents status override via `WriteHeader` guard | High | `GUARD(r.Committed → return)` is explicit |
| `ResolveResponseStatus` short-circuits on committed response | High | GUARD annotation is explicit |
| `delayedStatusWriter` defers status writes | Medium | Type and methods documented; exact semantics not detailed |
| `Response.Unwrap` is used by error handler to access underlying writer | High | Call relationship explicitly documented |
| `exposeError` controls error detail visibility | High | Parameter in source snippet |

## Gaps

- `Response.After` and `Response.Before` callback semantics are not fully detailed (listed as uncovered in GAPS).
- `Response.reset` is uncovered — likely used for context pooling, not error handling.
- `newAddRouteError` is uncovered — related to route registration errors, not runtime error handling.
- The exact branching logic inside `DefaultHTTPErrorHandler` (type-switch or interface checks) is not described in the clue.
- How the error is logged or reported (beyond the HTTP response) is not covered.
- Interaction between `delayedStatusWriter` and the `Committed` flag is not specified.
