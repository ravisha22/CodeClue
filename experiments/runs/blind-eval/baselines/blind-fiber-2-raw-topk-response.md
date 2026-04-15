# Response: blind-fiber-2 (raw-topk baseline)
Date: 2026-04-15

The supplied excerpts do not contain Fiber’s panic-recovery path or sub-app mounting logic, so the answer is necessarily limited to what is actually shown.

What is visible:

- `error.go` defines `ErrHandlerExited`, documented as what `App.Test` returns “if a handler panics or calls runtime.Goexit()` (`error.go`, lines 294-295). That tells us panics are recognized at the app/test boundary.
- The same file shows that Fiber has typed HTTP-facing errors created with `NewError(...)`, for example `ErrRedirectBackNoFallback` and `ErrRangeTooLarge` (`error.go`, lines 304 and 310). That implies there is an error-to-status formatting path somewhere else in the framework.
- `client\response.go` exposes the final HTTP status code and status message through `Response.StatusCode()` and `Response.Status()` (`client\response.go`, lines 66-73), i.e. once a response exists, those are the fields that surface it.

What is **not** shown:

- any panic `recover` logic,
- any default server error handler / error formatter,
- any mounted sub-app dispatch code,
- or any mechanism that selects one error formatter versus another for mounted apps.

So, from the supplied source alone, I can only say that Fiber has a notion of handler panics surfacing as an app-level error condition (`ErrHandlerExited`, `error.go`, lines 294-295) and a separate notion of HTTP-oriented errors carrying status information (`NewError(...)`, `lines 304, 310`). The actual conversion from a panic into an HTTP response, and the way mounted sub-apps override or swap the formatter used for that response, are not present in the prompt.
