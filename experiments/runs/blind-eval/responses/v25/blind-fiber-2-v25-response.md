# v2.5 Response: blind-fiber-2
Date: 2026-04-16

## Question

When a handler panics in Fiber, how is that turned into an HTTP response, and how can mounted sub-apps change which error formatter gets used?

## Relevant Symbols Identified

- **`DefaultPanicHandler`** (middleware/recover/recover.go:16) — converts panic value to error
- **`App.serverErrorHandler`** (app.go:1411) — top-level error handler wrapper for fasthttp
- **`App.ErrorHandler`** (app.go:1376) — resolves which error handler to invoke, accounting for mounted sub-apps
- **`DefaultErrorHandler`** (app.go:524) — default error-to-response formatter
- **`DefaultErrorHandler`** (middleware/session/config.go:109) — session-specific error handler variant
- **`App.processSubAppsRoutes`** (mount.go:168-169) — wires sub-app routes at startup
- **`App.appendSubAppLists`** (mount.go:139) — supports nested sub-app registration
- **`App.hasMountedApps`** (mount.go:108-109) — checks for mounted apps

## Tracing: Panic to HTTP Response

### Step 1: Catching the Panic — Recover Middleware

The recover middleware provides **`DefaultPanicHandler`** (middleware/recover/recover.go:16, FOCUS). Its behavior annotation is:

> `GUARD(err, ok := r.(error); ok -> return err)`

This means: if the recovered panic value `r` is already an `error`, it is returned directly. Otherwise, it calls **`Errorf`** (which is `fmt.Errorf` per the `calls: Errorf` annotation) to wrap the panic value into an error using the `%v` verb. The recover middleware catches the panic via Go's `recover()` mechanism and converts it into a regular error that can flow through Fiber's error handling chain.

### Step 2: Error Propagation to serverErrorHandler

Errors returned from handlers (including recovered panics) reach **`App.serverErrorHandler`** (app.go:1411, FOCUS). Its description states it is "a wrapper around the application's error handler method used for the fasthttp server configuration." Its behavior annotation is:

> `UNWIND(defer)`

This indicates it uses a deferred function (likely for cleanup/context release). Its calls chain is:

> `calls: next, ErrorHandler, Error, NewError, getMethodInt, setSkipNonUseRoutes, AcquireCtx, ReleaseCtx`

The flow is: `serverErrorHandler` acquires a context (`AcquireCtx`), attempts dispatch (`next`), and when an error occurs, delegates to **`App.ErrorHandler`**. It also calls `NewError` and `Error` — suggesting it may wrap or inspect the error (e.g., checking for `*fiber.Error` types). The context is released afterward (`ReleaseCtx`), and the deferred cleanup (`UNWIND(defer)`) ensures resources are freed even if the error handler itself fails.

### Step 3: Resolving the Error Handler — ErrorHandler with Mounted Sub-App Support

**`App.ErrorHandler`** (app.go:1376, FOCUS) is the critical dispatch point for error formatting. Its behavior annotation is:

> `GUARD(mountedErrHandler != nil -> return mountedErrHa...)`
> `ACCUMULATE(AddTrailingSlashStrin... -> result)`

The GUARD clause is the key mechanism for sub-app error handler resolution: if a `mountedErrHandler` is found (non-nil), it is returned and used instead of the parent app's error handler. The ACCUMULATE pattern with `AddTrailingSlashString` suggests the method walks the request path (it `calls: Path`) to find which mounted sub-app's prefix matches the current request, and retrieves that sub-app's error handler.

Its `called_by` list includes `serverErrorHandler` and `New`, confirming it is invoked both during error handling and at app initialization.

### Step 4: Default Error Formatting

If no mounted sub-app error handler is found, the **`DefaultErrorHandler`** (app.go:524, FOCUS) is used. Its behavior is:

> `DELEGATE(c.Status -> result)`
> `calls: Error, Set, Status`

This handler:
1. Extracts the error message via `Error()`
2. Sets the HTTP status code via `Status()` — if the error is a `*fiber.Error` with a code, that code is used; otherwise a generic status is set
3. Sets response headers via `Set()` (likely Content-Type)
4. Sends the error message as the response body

There is also a separate **`DefaultErrorHandler`** in the session middleware (middleware/session/config.go:109, FOCUS), which "logs the error and sends a 500 status code" via `calls: Status, Errorf`. This is a domain-specific error handler for session-related errors, not the global default.

## How Mounted Sub-Apps Change the Error Formatter

### Sub-App Registration

Sub-apps are mounted using the mount system. **`App.processSubAppsRoutes`** (mount.go:168-169, FOCUS) "adds routes of sub-apps recursively when the server is started" and calls `hasMountedApps` and `addPrefixToRoute`. **`App.appendSubAppLists`** (mount.go:139, FOCUS) "supports nested for sub apps" and accumulates sub-app references via `getGroupPath`.

### Error Handler Resolution at Request Time

When an error occurs during request handling, **`App.ErrorHandler`** (app.go:1376) inspects the request path (via `calls: Path`) and uses the `ACCUMULATE(AddTrailingSlashString...)` logic to walk through registered mount prefixes. It looks up whether any mounted sub-app's prefix matches the current request path. If a match is found and that sub-app has a custom error handler configured (`mountedErrHandler != nil`), that handler is returned and invoked instead of the parent app's default.

This means each mounted sub-app can specify its own error handler (likely via a config option when creating the sub-app's `App` instance), and the framework automatically selects the correct one based on the request path at error time.

### Handler Adapter Panics

The clue also shows that **`handlerFunc`** (middleware/adaptor/adaptor.go:242, FOCUS) and **`acquireResponseChan`** (client/core.go:249, FOCUS) are annotated with `raises: panic`. The adaptor's `handlerFunc` bridges Fiber handlers to `net/http` — panics there would need to be caught by the recover middleware to enter the error handling flow described above.

## Gaps and Uncertainty

Per the GAPS section:

> **type: MECHANISTIC (body logic needed for full answer)**
> **uncovered: isTimeoutError, parserResponseCookie, releaseResponseChan, standardClientTransport.SetStreamResponseBody**

Specific uncertainties:

- **Cannot determine**: The exact mechanism by which sub-apps register their custom error handlers during mounting — whether it is a field on `App`, a config option, or set via `mount()`. The `mount.go` module (INDEX: 227L, symbols `MountPath, appendSubAppLists, generateAppListKeys, hasMountedApps, mount`) contains a `mount` function but its body is not provided.
- **Cannot determine**: How `App.ErrorHandler` builds or traverses the `mountedErrHandler` map — whether it's a prefix trie, a linear scan, or a simple map lookup by path prefix.
- **Cannot determine**: Whether the recover middleware is automatically included or must be explicitly added by the user. The `DefaultPanicHandler` is in `middleware/recover/`, suggesting it is opt-in middleware.
- **Cannot determine**: What happens if a panic occurs *outside* the recover middleware's scope (e.g., in `serverErrorHandler` itself) — the `UNWIND(defer)` annotation on `serverErrorHandler` suggests some deferred protection, but the specifics are uncovered.

## Summary

A handler panic in Fiber is caught by the recover middleware's **`DefaultPanicHandler`** (middleware/recover/recover.go:16), which converts the panic value to an `error` (returning it directly if already an error, or wrapping it via `Errorf`). This error flows to **`App.serverErrorHandler`** (app.go:1411), which acquires a context and delegates to **`App.ErrorHandler`** (app.go:1376). `ErrorHandler` checks the request path and resolves whether a mounted sub-app has a custom error handler (`GUARD(mountedErrHandler != nil)`). If a matching mounted handler exists, it is used; otherwise, **`DefaultErrorHandler`** (app.go:524) formats the response by setting the status code and error message. Mounted sub-apps change the error formatter by registering their own error handler, which `App.ErrorHandler` discovers by matching the request path against mount prefixes at error time.
