# v2.3 Response: blind-fiber-2
Date: 2026-04-15

## Summary

When a handler panics in Fiber, the panic is caught by a recovery middleware that converts it into an error, which then flows through the application's error handler chain. Mounted sub-apps can influence which error handler is used via `App.ErrorHandler`, which checks for mounted error handlers before falling back. A `DefaultErrorHandler` and a `DefaultPanicHandler` provide the baseline behavior.

## Panic Recovery: DefaultPanicHandler

- **`DefaultPanicHandler`** (`middleware/recover/recover.go:16`, FOCUS): *"DefaultPanicHandler returns r directly if it's an error, and creates a new one with the %v verb otherwise."*
  - Signature: `DefaultPanicHandler(_ fiber.Ctx, r any)`
  - Behavior: `GUARD(err -> pass_through)` — If the recovered value `r` is already an `error`, it passes it through directly. Otherwise, it wraps the value into a new error (using `%v` formatting).
  - This is the first step: converting a raw panic value into a proper Go `error`.

## Error Handler Chain

### App.serverErrorHandler (app.go:1411)

- **`App.serverErrorHandler`** (`app.go:1411`, FOCUS): *"serverErrorHandler is a wrapper around the application's error handler method used for the fasthttp server configuration."*
  - Signature: `App.serverErrorHandler(fctx *fasthttp.RequestCtx, err error)`
  - Behavior: `UNWIND(defer)` — Uses deferred execution (likely for panic recovery at the server level).
  - Calls: `ErrorHandler`, `Error`, `NewError`
  - This is the entry point from the underlying fasthttp server into Fiber's error handling. It wraps the call to `ErrorHandler` and likely catches any panics in the error handler itself via `UNWIND(defer)`.

### App.ErrorHandler (app.go:1376)

- **`App.ErrorHandler`** (`app.go:1376`, FOCUS): *"ErrorHandler is the application's method in charge of finding the appropriate handler for the given request."*
  - Signature: `App.ErrorHandler(ctx Ctx, err error)`
  - Behavior: `GUARD(mountedErrHandler -> wrap_mountedErrHandler); ACCUMULATE(loop -> result)`
  - Called by: `serverErrorHandler`
  - **Key mechanism for sub-apps**: The `GUARD(mountedErrHandler -> wrap_mountedErrHandler)` behavior indicates that the method first checks whether a **mounted error handler** exists for the current request context. If one is found (`mountedErrHandler` is truthy), it wraps and uses that handler instead. The `ACCUMULATE(loop -> result)` suggests it may iterate through a chain or hierarchy of mounted apps to find the appropriate error handler.

### DefaultErrorHandler (app.go:524)

- **`DefaultErrorHandler`** (`app.go:524`, FOCUS): *"DefaultErrorHandler that process return errors from handlers."*
  - Signature: `DefaultErrorHandler(c Ctx, err error)`
  - Behavior: `DELEGATE(c.Status -> result)` — Sets the HTTP status code on the response.
  - Calls: `Error` — Likely calls `err.Error()` to get the error message string, then sends it as the response body.
  - This is the **fallback** error handler used when no custom or mounted error handler is configured.

### DefaultErrorHandler in Session Middleware (middleware/session/config.go:109)

- **`DefaultErrorHandler`** (`middleware/session/config.go:109`, FOCUS): *"DefaultErrorHandler logs the error and sends a 500 status code."*
  - Signature: `DefaultErrorHandler(c fiber.Ctx, err error)`
  - This is a **separate** default error handler specific to the session middleware, not the application-level one. It shows that individual middleware can define their own default error handlers.

### CSRF Default Error Handler (middleware/csrf/config.go:142)

- **`defaultErrorHandler`** (`middleware/csrf/config.go:142`, FOCUS): *"defaultErrorHandler is the default error handler that processes errors from fiber.Handler."*
  - Signature: `defaultErrorHandler(_ fiber.Ctx, _ error)`
  - Another middleware-specific error handler, used by the CSRF middleware.

## How Mounted Sub-Apps Change the Error Handler

### Mounting Infrastructure

- **`App.mountStartupProcess`** (`mount.go:113-114`, FOCUS): *"mountStartupProcess Handles the startup process of mounted apps by appending sub-app routes, generating app list keys, and processing sub-app routes."*
  - Calls: `appendSubAppLists`, `generateAppListKeys`, `hasMountedApps`, `processSubAppsRoutes`
  - This establishes the sub-app hierarchy at startup.

- **`App.appendSubAppLists`** (`mount.go:139`, FOCUS): *"appendSubAppLists supports nested for sub apps."*
  - Signature: `App.appendSubAppLists(appList map[string]*App, parent ...string)`
  - Behavior: `ACCUMULATE(loop -> result)`
  - This builds a map of mounted sub-apps keyed by path prefix, supporting nested sub-apps.

- **`App.hasMountedApps`** (`mount.go:108-109`, FOCUS): Checks if any sub-apps are mounted. Behavior: `DELEGATE(len -> result)`.

- **`App.processSubAppsRoutes`** (`mount.go:168-169`, FOCUS): *"processSubAppsRoutes adds routes of sub-apps recursively when the server is started."*
  - Behavior: `ACCUMULATE(loop -> result)`
  - Calls: `hasMountedApps`
  - Called by: `mountStartupProcess`
  - Recursively integrates sub-app routes into the main routing table.

### Error Handler Resolution for Sub-Apps

The `App.ErrorHandler` behavior `GUARD(mountedErrHandler -> wrap_mountedErrHandler)` reveals the mechanism:

1. When an error occurs during request handling, `serverErrorHandler` (`app.go:1411`) is called.
2. `serverErrorHandler` calls `App.ErrorHandler` (`app.go:1376`).
3. `ErrorHandler` checks if a **mounted error handler** (`mountedErrHandler`) exists for the current request context. This likely uses the app list built by `appendSubAppLists` to look up which sub-app (if any) owns the matched route.
4. If a mounted error handler is found, it is **wrapped** (`wrap_mountedErrHandler`) and used to process the error.
5. If no mounted error handler is found, the `ACCUMULATE(loop -> result)` behavior suggests iteration — possibly falling back through the mount hierarchy until a handler is found or the root app's error handler (e.g., `DefaultErrorHandler`) is used.

## Response Generation

- **`DefaultRes.SendStatus`** (`res.go:979`, FOCUS): *"SendStatus sets the HTTP status code and if the response body is empty, it sets the correct status message in the body."*
  - Behavior: `GUARD(statusDisallowsBody -> none); PRECEDENCE(statusDisallowsBody -> len)`
  - Calls: `SendString`, `Status`, `statusDisallowsBody`
  - This is likely used by error handlers to set status codes like 500.

- **`DefaultRes.Status`** (`res.go:1032`, FOCUS): *"Status sets the HTTP status for the response."*

- **`DefaultRes.SendString`** (`res.go:997`, FOCUS): *"SendString sets the HTTP response body for string types."*

- **`DefaultErrorHandler`** calls `Error` (to get the error message) and `c.Status` (to set the status code), then the error message becomes the response body.

## The Full Panic-to-Response Flow

1. **Handler panics** → Go runtime unwinds the stack.
2. **Recovery middleware** catches the panic via `recover()`.
3. **`DefaultPanicHandler`** (`middleware/recover/recover.go:16`) converts the panic value to an `error`: if already an error, passes through; otherwise wraps with `%v`.
4. **The error propagates** back through the handler chain.
5. **`App.serverErrorHandler`** (`app.go:1411`) receives the error from fasthttp. It calls `ErrorHandler` within a deferred recovery (`UNWIND(defer)`).
6. **`App.ErrorHandler`** (`app.go:1376`) checks for a mounted sub-app error handler. If found, wraps and uses it. Otherwise falls through.
7. **`DefaultErrorHandler`** (`app.go:524`) sets the HTTP status code and sends the error message as the response body.

## Uncertainty / Limits

- **The exact recovery middleware implementation** (the `New()` function in `middleware/recover/`) is not shown in the FOCUS entries. Only `DefaultPanicHandler` is visible. The middleware that actually calls `recover()` and invokes `DefaultPanicHandler` is not detailed.
- **How `mountedErrHandler` is resolved** — The exact lookup mechanism (by request path prefix? by matched route's app?) is not shown. The `appList map[string]*App` from `appendSubAppLists` suggests path-prefix-based lookup, but the resolution logic is not in the clue file.
- **Whether sub-apps can override the panic handler** (as opposed to just the error handler) is not clear from the clue file. The `DefaultPanicHandler` is in `middleware/recover/`, suggesting it is a configurable middleware, but the configuration options are not shown.
- **The `NewError` function** called by `serverErrorHandler` is not detailed — it likely creates a `*fiber.Error` with a status code, but its implementation is not shown.
