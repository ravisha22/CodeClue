When a handler panic becomes an HTTP response in Fiber, the clue file suggests a two-step path:

1. **The panic is first normalized into an `error`.** The only panic-specific hook named in the clue is `DefaultPanicHandler`, which belongs to `middleware/recover` and "returns `r` directly if it's an error, and creates a new one with the `%v` verb otherwise" (`DefaultPanicHandler`, `middleware/recover/recover.go:16`). That means a recovered panic value is converted into an ordinary `error` object before normal error handling continues.

2. **That `error` is then rendered through the app's error-handling path into the HTTP response.** The clue says `App.serverErrorHandler` is "a wrapper around the application's error handler method ... for the fasthttp server configuration" and that it calls `Error` and `NewError` (`App.serverErrorHandler`, `app.go:1411`). Separately, `App.ErrorHandler` is "the application's method in charge of finding the appropriate handler for the given request" (`App.ErrorHandler`, `app.go:1376`). Finally, the app-level `DefaultErrorHandler` "process[es] return errors from handlers" (`DefaultErrorHandler`, `app.go:524`). Taken together, the supported conclusion is: once the panic has been turned into an `error`, Fiber routes it through the app's error-handler selection logic, and the chosen error handler produces the HTTP response (`DefaultPanicHandler`, `middleware/recover/recover.go:16`; `App.serverErrorHandler`, `app.go:1411`; `App.ErrorHandler`, `app.go:1376`; `DefaultErrorHandler`, `app.go:524`).

On the second part of the question — **how mounted sub-apps can change which error formatter gets used** — the clue strongly indicates that mounted apps can affect error-handler selection on a per-request basis:

- `App.ErrorHandler` does not just run one global formatter; it is specifically responsible for "finding the appropriate handler for the given request" (`App.ErrorHandler`, `app.go:1376`).
- Fiber has explicit mounted-sub-app infrastructure: `App.mountStartupProcess` handles startup for mounted apps by appending sub-app routes, generating app-list keys, and processing sub-app routes (`App.mountStartupProcess`, `mount.go:113-114`).
- Mounted apps are tracked recursively: `App.appendSubAppLists` "supports nested for sub apps" (`App.appendSubAppLists`, `mount.go:139`).
- A sub-app knows where it is mounted because `App.MountPath` returns "the route pattern where the current app instance was mounted as a sub-application" (`App.MountPath`, `mount.go:103-104`).

From those entries, the best clue-grounded answer is: when a request lands under a mounted sub-app's mount path, Fiber's request-specific error-handler lookup can choose that sub-app's handler/formatter instead of the parent app's one, because mounted apps are registered and tracked separately during startup and `App.ErrorHandler` selects the appropriate handler for the request (`App.ErrorHandler`, `app.go:1376`; `App.mountStartupProcess`, `mount.go:113-114`; `App.appendSubAppLists`, `mount.go:139`; `App.MountPath`, `mount.go:103-104`).

## What the clue lets us say confidently

- Panic values can be converted into `error` values by the recover middleware's panic handler (`DefaultPanicHandler`, `middleware/recover/recover.go:16`).
- Fiber has an app error-handling pipeline that ultimately turns handler errors into HTTP responses (`App.serverErrorHandler`, `app.go:1411`; `App.ErrorHandler`, `app.go:1376`; `DefaultErrorHandler`, `app.go:524`).
- Mounted sub-apps are explicitly indexed and associated with mount paths, and error-handler selection is request-specific, so sub-app mounting can change which formatter handles a given error (`App.ErrorHandler`, `app.go:1376`; `App.mountStartupProcess`, `mount.go:113-114`; `App.appendSubAppLists`, `mount.go:139`; `App.MountPath`, `mount.go:103-104`).

## What the clue does **not** fully expose

The clue does **not** show the exact body logic of `App.ErrorHandler` or `mount.go`, so it does not prove the precise matching algorithm or the exact precedence rules among parent app vs. nested sub-app handlers. It also does not show the concrete HTTP body/status formatting performed by the app-level `DefaultErrorHandler`; it only tells us that it processes handler errors (`App.ErrorHandler`, `app.go:1376`; `DefaultErrorHandler`, `app.go:524`; GAPS section, lines 317-323).
