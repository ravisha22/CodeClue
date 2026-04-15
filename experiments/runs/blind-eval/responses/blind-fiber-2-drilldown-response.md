# Response: blind-fiber-2 (with drill-down)
2026-04-15

The provided drill-down source snippets are all from `client/transport.go`, so they do not add direct evidence about panic handling or mounted sub-app error selection; the relevant evidence is in the clue file entries for `DefaultPanicHandler`, `App.serverErrorHandler`, `App.ErrorHandler`, and the mount-related functions. [Source snippets: `standardClientTransport`, `hostClientTransport`, `lbClientTransport`, `composeRedirectURL`, `doRedirectsWithClient`; Clue file `-- GAPS` / `drill: client/transport.go`]

## What I can determine

1. **A recovered panic is normalized into an `error` value before normal error handling continues.** The strongest direct clue is `DefaultPanicHandler`, whose summary says it "returns `r` directly if it's an error, and creates a new one with the `%v` verb otherwise." That means the panic payload is converted into an `error`-shaped value that the rest of the error pipeline can consume. [Clue: `DefaultPanicHandler (middleware/recover/recover.go:16-16)`]

2. **Fiber has an application-level error-handling stage that chooses the handler for the current request.** `App.ErrorHandler` is described as "the application's method in charge of finding the appropriate handler for the given request." Because the clue annotates it with `PRECEDENCE(if_chain); ACCUMULATE(loop)`, the selection is not trivial; it likely evaluates request/app context and may iterate over candidates before picking the handler. [Clue: `App.ErrorHandler (app.go:1376-1376)`]

3. **There is also a server-facing wrapper that converts server/request errors into the app's error pipeline.** `App.serverErrorHandler` is "a wrapper around the application's error handler method used for the fasthttp server configuration." Its signature takes `(*fasthttp.RequestCtx, error)`, and the clue says it has `UNWIND(defer); DISPATCH(switch)` behavior and calls `Error` and `NewError`. That tells me server-level failures are funneled through this wrapper and then expressed as Fiber/app errors before a response is emitted. [Clue: `App.serverErrorHandler (app.go:1411-1411)`]

4. **Once the panic has become an `error`, the selected error handler is what formats the HTTP response.** The clue for `DefaultErrorHandler` says it is the default handler "that process[es] return errors from handlers." So, if no more specific/custom handler is chosen, the default application error handler is the formatter that turns the error into the final HTTP response. [Clue: `DefaultErrorHandler (app.go:524-524)`]

Putting those together, the evidence-supported pipeline is:

- a panic is recovered and turned into an `error` (`DefaultPanicHandler`), [Clue: `DefaultPanicHandler`]
- the app/server error path receives that error (`App.serverErrorHandler` / `App.ErrorHandler`), [Clue: `App.serverErrorHandler`, `App.ErrorHandler`]
- the chosen error handler formats the HTTP response, with `DefaultErrorHandler` acting as the fallback/default formatter. [Clue: `DefaultErrorHandler (app.go)`]

## How mounted sub-apps can change the error formatter used

The clue file strongly suggests that mounted apps participate in request-scoped handler selection:

1. **Mounted apps are tracked explicitly and recursively at startup.** `App.mountStartupProcess` handles mounted apps by "appending sub-app routes, generating app list keys," and calling `appendSubAppLists`, `generateAppListKeys`, `hasMountedApps`, and `processSubAppsRoutes`. [Clue: `App.mountStartupProcess (mount.go:113-114)`]

2. **Mounted app relationships are stored recursively.** `appendSubAppLists` "supports nested for sub apps," and `processSubAppsRoutes` "adds routes of sub-apps recursively when the server is started." [Clue: `App.appendSubAppLists (mount.go:139-139)`, `App.processSubAppsRoutes (mount.go:168-169)`]

3. **Each app knows where it was mounted.** `App.MountPath` returns "the route pattern where the current app instance was mounted as a sub-application." [Clue: `App.MountPath (mount.go:103-104)`]

4. **Error-handler selection is request-specific.** Since `App.ErrorHandler` finds "the appropriate handler for the given request," and the mount system builds recursive sub-app structures keyed by mount location, the reasonable evidence-based conclusion is that a request matching a mounted sub-app can cause Fiber to choose that sub-app's error handler/formatter instead of the parent app's one. [Clue: `App.ErrorHandler`, `App.mountStartupProcess`, `App.appendSubAppLists`, `App.processSubAppsRoutes`, `App.MountPath`]

So the answer, constrained to the provided evidence, is: **mounted sub-apps can change the error formatter by changing which app is considered the relevant app for the current request; once the request resolves into a mounted sub-app, `App.ErrorHandler` can select that sub-app's handler rather than the parent app's default/custom handler.** [Clue: `App.ErrorHandler`, `App.MountPath`, `App.mountStartupProcess`]

## What I cannot determine from the provided material

The prompt material is not enough to prove several lower-level details:

- I **cannot** show the exact recovery site for panics (for example, whether recovery always happens in recover middleware, in `serverErrorHandler`, or in both), because the clue file gives only summaries and no function bodies for those symbols. [Clue coverage note: `-- GAPS`, `type: MECHANISTIC (body logic needed for full answer)`]
- I **cannot** state the exact HTTP status code/body/headers produced for an arbitrary panic by the app-level default handler, because the body of `DefaultErrorHandler (app.go)` is not included. [Clue: `DefaultErrorHandler (app.go:524-524)`]
- I **cannot** prove the precise algorithm `App.ErrorHandler` uses to map a request to a parent app vs. mounted sub-app; I can only say the clue explicitly indicates request-based handler selection plus recursive mounted-app bookkeeping. [Clue: `App.ErrorHandler`, `App.mountStartupProcess`, `App.appendSubAppLists`, `App.processSubAppsRoutes`]
- The File 2 drill-down snippets do **not** close these gaps, because they only expose signatures/types from `client/transport.go`, not panic/error/mount logic. [Source snippets: all listed entries under `client/transport.go`]

## Bottom line

From the provided clues alone: **a handler panic is turned into an `error` via panic handling (`DefaultPanicHandler`), then routed through Fiber's app/server error-handling path (`App.serverErrorHandler` and `App.ErrorHandler`), and the ultimately selected error handler formats the HTTP response (`DefaultErrorHandler` if no more specific one is chosen). Mounted sub-apps can change which formatter is used because Fiber maintains recursive mount metadata and `App.ErrorHandler` chooses the appropriate handler for the current request, which can resolve to the mounted sub-app instead of the parent app.** [Clue: `DefaultPanicHandler`, `App.serverErrorHandler`, `App.ErrorHandler`, `DefaultErrorHandler`, `App.MountPath`, `App.mountStartupProcess`, `App.appendSubAppLists`, `App.processSubAppsRoutes`]
