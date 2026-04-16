# v2.4.1 Response: blind-fiber-2
Date: 2026-04-16

## Panic-to-Response Pipeline and Sub-App Error Formatters

### Recover Middleware

Fiber provides `DefaultPanicHandler` (`middleware/recover/recover.go:16`) which converts a recovered value to an error: if the value is already an `error` it returns it directly, otherwise it wraps it with the `%v` verb [FOCUS §DefaultPanicHandler]. This is the entry point that converts panics into error values.

### Error Handler Chain

`App.serverErrorHandler` (`app.go:1411`) is a wrapper used for fasthttp server configuration. It calls `App.ErrorHandler` and also invokes `Error` and `NewError` [FOCUS §App.serverErrorHandler]. Its behavior annotation includes `UNWIND(defer)`, indicating it uses defer for cleanup.

`App.ErrorHandler` (`app.go:1376`) is the application's method for finding the appropriate error handler. Its behavior is:
- `GUARD(mountedErrHandler != nil -> return mountedErrHandler...)` — if a mounted error handler exists, it is used instead of the default [FOCUS §App.ErrorHandler].
- `ACCUMULATE(AddTrailingSlashStrin... -> result)` — it iterates to find the right handler.
- It is called by `serverErrorHandler` [FOCUS §App.ErrorHandler, called_by].

### Default Error Handler

`DefaultErrorHandler` (`app.go:524`) processes return errors from handlers by delegating to `c.Status` and calling `Error` [FOCUS §DefaultErrorHandler, app.go:524]. A separate `DefaultErrorHandler` exists in the session middleware (`middleware/session/config.go:109`) that logs the error and sends a 500 status code [FOCUS §DefaultErrorHandler, middleware/session/config.go:109].

The CSRF middleware also has a `defaultErrorHandler` (`middleware/csrf/config.go:142`) whose source signature is `func defaultErrorHandler(_ fiber.Ctx, _ error) error` — it discards both context and error arguments [Source Snippet §defaultErrorHandler].

### The Error Type

`Error` (`app.go:62`) represents an error during request handling and has an `Error()` method. It is referenced by both `serverErrorHandler` and `DefaultErrorHandler` [FOCUS §Error].

### Mounted Sub-Apps and Error Handler Override

Sub-apps are mounted via `App.mount` (`mount.go`) with `App.mountStartupProcess` (`mount.go:113`) handling the startup process by calling `appendSubAppLists`, `generateAppListKeys`, `hasMountedApps`, and `processSubAppsRoutes` [FOCUS §App.mountStartupProcess]. `App.processSubAppsRoutes` (`mount.go:168`) recursively adds routes of sub-apps [FOCUS §App.processSubAppsRoutes].

The critical line is in `App.ErrorHandler`: the guard `mountedErrHandler != nil -> return mountedErrHandler...` [FOCUS §App.ErrorHandler] shows that when a request hits a mounted sub-app that has its own error handler configured, that handler takes precedence over the parent app's error handler.

### Adaptor Layer

`FiberHandler` (`middleware/adaptor/adaptor.go:194`) wraps a Fiber handler as a `net/http` handler, delegating to `FiberHandlerFunc` (`middleware/adaptor/adaptor.go:199`) which in turn calls `handlerFunc` (`middleware/adaptor/adaptor.go:242`) [FOCUS §FiberHandler, §FiberHandlerFunc; Source Snippets]. `FiberApp` (`middleware/adaptor/adaptor.go:204`) wraps an entire Fiber app as `http.HandlerFunc` [FOCUS §FiberApp]. These adaptors allow Fiber apps to be served in net/http contexts where different error-handling conventions may apply.

### What Cannot Be Determined

- The exact mechanism inside `serverErrorHandler` for catching panics (the `defer`/`recover` wiring between the fasthttp handler and the recover middleware) — only the signature-level `UNWIND(defer)` is shown [FOCUS §App.serverErrorHandler].
- How a sub-app's custom `ErrorHandler` is **configured** at app-creation time (the `Config` struct fields for error handling are not detailed) [GAPS].
- The full bodies of `Handler.DeleteToken`, `response.DecodeMsg`, `response.EncodeMsg`, and `response.MarshalMsg` [GAPS: uncovered].
- Whether `DefaultPanicHandler` is automatically registered or must be opted-in via `middleware/recover` [only the function signature is shown].
