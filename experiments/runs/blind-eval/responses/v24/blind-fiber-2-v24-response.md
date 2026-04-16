# v2.4 Response: blind-fiber-2
Date: 2026-04-16

## Question
When a handler panics in Fiber, how is that turned into an HTTP response, and how can mounted sub-apps change which error formatter gets used?

## Answer

### Panic Recovery

Fiber provides a `DefaultPanicHandler` (`DefaultPanicHandler`, middleware/recover/recover.go:16) with signature `DefaultPanicHandler(_ fiber.Ctx, r any)` and behavior `GUARD(err, ok := r.(error); ok -> return err)`. This function checks if the recovered panic value `r` is already an `error`; if so, it returns it directly. Otherwise, it creates a new error using the `%v` verb. This converts a raw panic value into a Go `error` that can flow through the error-handling pipeline.

### The Error Type

The `Error` struct (`Error`, app.go:62-63) represents an error that occurred while handling a request. It has an `Error` method and is referenced by `serverErrorHandler` and `DefaultErrorHandler` (called_by annotation). The `NewError` function (`NewError`, app.go:1046) creates a new `Error` instance with a status code and optional message, and is called by `serverErrorHandler`.

### Server Error Handler

`App.serverErrorHandler` (`App.serverErrorHandler`, app.go:1411) is a wrapper around the application's error handler used for the fasthttp server configuration. Its signature is `App.serverErrorHandler(fctx *fasthttp.RequestCtx, err error)` with behavior `UNWIND(defer)`. It calls three things:
1. `ErrorHandler` — the application-level error handler
2. `Error` — the error type's method
3. `NewError` — to create structured error instances

The `UNWIND(defer)` behavior indicates it uses deferred cleanup, likely for panic recovery at the server level.

### The Application Error Handler

`App.ErrorHandler` (`App.ErrorHandler`, app.go:1376) is the application's method for finding the appropriate handler for the given request error. Its behavior is `GUARD(mountedErrHandler != nil -> return mountedErrHa...); ACCUMULATE(AddTrailingSlashStrin... -> result)`. This is the critical piece for mounted sub-apps:

- **GUARD(mountedErrHandler != nil -> ...)**: The method first checks whether a `mountedErrHandler` exists. If a sub-app has registered its own error handler, this guard clause causes that handler to be used instead of the parent app's handler. This is how mounted sub-apps change which error formatter is used.
- **ACCUMULATE(AddTrailingSlashStrin... -> result)**: If no mounted error handler is found, it accumulates results involving trailing-slash string operations, likely walking up the mount path to find an appropriate handler.

`App.ErrorHandler` is called by `serverErrorHandler` (`App.ErrorHandler` called_by: `serverErrorHandler`).

### The Default Error Handler

`DefaultErrorHandler` (`DefaultErrorHandler`, app.go:524) processes return errors from handlers. Its behavior is `DELEGATE(c.Status -> result)` and it calls `Error`. This sets the HTTP status code on the response context based on the error. There is also a separate `DefaultErrorHandler` in the session middleware (`DefaultErrorHandler`, middleware/session/config.go:109) that logs the error and sends a 500 status code, and a `defaultErrorHandler` in the CSRF config (`defaultErrorHandler`, middleware/csrf/config.go:142).

### Mounted Sub-Apps and Error Handler Selection

The mounting system processes sub-app routes through `App.processSubAppsRoutes` (`App.processSubAppsRoutes`, mount.go:168-169), which accumulates via `hasMountedApps` loop. `App.hasMountedApps` (`App.hasMountedApps`, mount.go:108-109) checks if there are any mounted apps. The `App.appendSubAppLists` (`App.appendSubAppLists`, mount.go:139) supports nested sub-apps, accumulating group paths.

When an error occurs during request handling, `serverErrorHandler` delegates to `ErrorHandler`, which checks if the current request's mount path has a `mountedErrHandler`. If the sub-app registered its own error handler (via configuration), that handler processes the error and formats the response. If not, the parent app's default error handler is used.

### Handler Adaptation and Panic Propagation

The `handlerFunc` in the adaptor package (`handlerFunc`, middleware/adaptor/adaptor.go:242) with signature `handlerFunc(app *fiber.App, h ...fiber.Handler)` has a `raises: panic` annotation, meaning it can propagate panics. The `toFiberHandler` (`toFiberHandler`, adapter.go:13) and `collectHandlers` (`collectHandlers`, adapter.go:262) also have `raises: panic` annotations, indicating panics propagate through the handler conversion chain until caught by the recover middleware or the server error handler.

### What Cannot Be Determined

- The **exact mechanism** by which the recover middleware intercepts the panic (e.g., the full `New` function in `middleware/recover/`) is not in the FOCUS section. Only `DefaultPanicHandler` is shown.
- How `mountedErrHandler` is populated during the mount process (the precise field assignment) is not visible — only that `ErrorHandler` checks for it.
- The symbols `DefaultCtx.setIndexHandler`, `PreStartupMessageData.AddError`, and `beforeHandlerFunc` are listed as uncovered in GAPS and may contain relevant error-flow logic.
- Whether the panic recovery wraps around each individual handler or the entire handler chain is not explicitly stated.
