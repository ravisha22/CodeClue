# v2.5 Response: rel-fiber-2
Date: 2026-04-16

## Question
What are the call relationships between middleware and the request handling pipeline in Fiber?

## Answer

### Core Request Handling Pipeline

The request handling pipeline is driven by the App's dispatch methods:

**`App.next`** (SYM: `App.next` at `router.go:115`) — The primary dispatch function for `*DefaultCtx`. Called by: `Retry`, `serverErrorHandler`, `Next`, `RestartRouting`, `requestHandler`. It calls `Next`, `Append`, `match` to iterate through the handler/middleware stack.

**`App.nextCustom`** (SYM: `App.nextCustom` at `router.go:216`) — Dispatch for `CustomCtx`. Called by: `serverErrorHandler`, `Next`, `RestartRouting`, `requestHandler`. Calls `Next`, `Path`, `getDetectionPath`, `getIndexRoute`, `getMatched`, `getMethodInt`, `getSkipNonUseRoutes`, `getTreePathHash`.

Both are invoked by `requestHandler` (the entry point for each request) and can be re-invoked via `RestartRouting`.

### Middleware Registration

Middleware is registered through `Use`:

**`domainRouter.Use`** (FOCUS: `domainRouter.Use` at `domain.go:350`) — Registers middleware routes. Behavior: `PRECEDENCE(len -> d); ACCUMULATE(toFiberHandler loop -> handlers, raises fmt.Sprintf("use:...))`. It calls `Name`, `mount`, `registerGroup`, `registerPath`, `wrapHandlers`, `register`. This shows that `Use` converts handler arguments to Fiber handlers via `toFiberHandler`, then registers them as routes.

**`App.mount`** (SYM: `mount.go:42`, called_by: `Use`) and **`App.register`** (SYM: `router.go:513`, called_by: `Add`, `Group`, `Use`, `All`, `mount`) — Both `Use` and `mount` flow into `register` to add middleware routes to the routing tree.

### Handler Adaptation: toFiberHandler

**`toFiberHandler`** (FOCUS: `toFiberHandler` at `adapter.go:13`) — Converts supported handler types to Fiber handlers. Behavior: `GUARD(handler == nil -> return nil, false); DISPATCH(handler)`. Calls:
- `adaptExpressHandler`
- `adaptFastHTTPHandler`
- `adaptFiberHandler` (FOCUS: `adapter.go:32`)
- `adaptHTTPHandler`

Called by: `collectHandlers`. This is how various handler types (net/http, fasthttp, express-style, Fiber-native) are normalized into the Fiber handler signature.

### Middleware Execution: DefaultCtx.Next

**`DefaultCtx.Next`** (SYM: `DefaultCtx.Next` at `ctx.go:243`) — "Next executes the next method in the stack that matches the current route." This is the method middleware calls to pass control to the next handler in the chain.

**`DefaultCtx.IsMiddleware`** (FOCUS: `DefaultCtx.IsMiddleware` at `ctx.go:380-381`) — Returns true if the current handler was registered as middleware. Behavior: `GUARD(c.route == nil -> return false)`.

**`DefaultCtx.RestartRouting`** (FOCUS: `DefaultCtx.RestartRouting` at `ctx.go:265-266`) — Restarts routing instead of continuing. Calls `next` and `nextCustom`.

### Net/HTTP ↔ Fiber Middleware Adaptor

The `middleware/adaptor/` package provides bidirectional adaptation:

**`HTTPMiddleware`** (FOCUS: `HTTPMiddleware` at `middleware/adaptor/adaptor.go:162`) — "Wraps net/http middleware to fiber middleware." Calls: `Context`, `Next`, `Request`, `RequestCtx`, `CopyContextToFiberContext`, `HTTPHandler`. This allows standard Go `func(http.Handler) http.Handler` middleware to work in Fiber's pipeline.

**`CopyContextToFiberContext`** (FOCUS: `middleware/adaptor/adaptor.go:101`) — Copies `context.Context` values to `fasthttp.RequestCtx`. Behavior: `GUARD(requestContext == nil -> return)`. Called by `HTTPMiddleware`.

**`ConvertRequest`** (FOCUS: `ConvertRequest` at `middleware/adaptor/adaptor.go:89`) — Converts `fiber.Ctx` to `*http.Request`. Called by adaptor middleware to bridge contexts.

**`FiberHandler`** (FOCUS: `middleware/adaptor/adaptor.go:194`) — Wraps Fiber handler to `net/http` handler. Delegates to `FiberHandlerFunc` (FOCUS: `:199`).

**`FiberApp`** (FOCUS: `middleware/adaptor/adaptor.go:204`) — Wraps entire Fiber app to `net/http` handler func.

### Specific Middleware → Pipeline Call Relationships

Each middleware follows a consistent pattern: a `New(config ...Config)` factory returns a Fiber handler that calls `c.Next()` to continue the chain. Evidence from FOCUS entries:

**Cache middleware** (`middleware/cache/cache.go:109`):
- `New` calls: `Set`, `Context`, `Method`, `Next`, `Request`, `Response`, `Errorf`, `allowsSharedCacheDirectives`.
- Also interacts with `parseRequestCacheControl` (FOCUS: `middleware/cache/cache.go:1104`) and `parseRequestCacheControlString` (FOCUS: `:1139`).

**CORS middleware** (`middleware/cors/cors.go:28`):
- `New` calls: `Get`, `Set`, `Method`, `Next`, `Warn`, `isOriginSerializedOrNull`, `setPreflightHeaders`, `setSimpleHeaders`.

**CSRF middleware** (`middleware/csrf/csrf.go:50`):
- `New` calls: `ErrorHandler`, `Cookies`, `Method`, `Next`, `createOrExtendTokenInStorage`, `deleteTokenFromStorage`, `expireCSRFCookie`, `getRawFromStorage`.

**Basic Auth middleware** (`middleware/basicauth/basicauth.go:27`):
- `New` calls: `Get`, `App`, `Next`, `containsCTL`, `containsInvalidHeaderChars`, `SendStatus`.

**Request ID middleware** (`middleware/requestid/requestid.go:18`):
- `New` calls: `Get`, `Set`, `Next`, `sanitizeRequestID`.
- `sanitizeRequestID` (FOCUS: `:43`) validates request IDs via `isValidRequestID` (FOCUS: `:61`).

**Static files middleware** (`middleware/static/static.go:121`):
- `New` calls: `Route`, `Method`, `App`, `Next`, `Path`, `RequestCtx`, `isFile`, `sanitizePath`.

**Favicon middleware** (`middleware/favicon/favicon.go:21`):
- `New` calls: `Set`, `Method`, `Close`, `Status`, `Next`, `Path`, `readLimited`, `SendStatus`.

**Idempotency middleware** (`middleware/idempotency/idempotency.go:45`):
- `New` calls: `Get`, `Bind`, `Send`, `Status`, `App`, `Next`, `RequestCtx`, `Response`.
- Uses `MemoryLock.Lock` / `MemoryLock.Unlock` (SYM: `middleware/idempotency/locker.go`).

**Limiter middleware** (`middleware/limiter/limiter.go:23`):
- `New` delegates to `cfg.LimiterMiddleware.New`.

### Session Middleware Pipeline Integration

**`Middleware.initialize`** (FOCUS: `middleware/session/middleware.go:111`) — Sets up middleware for the request. Called by `NewWithStore`. Uses `Lock`/`Unlock`.

**`Middleware.saveSession`** (FOCUS: `:128`) — Saves session after response. Called by `NewWithStore` and `Save`.

**`releaseMiddleware`** (FOCUS: `:157`) — Returns middleware to pool after request. Called by `NewWithStore`.

**`acquireMiddleware`** (FOCUS: `:141`) — Gets middleware from pool. Called by `NewWithStore`.

The flow: `NewWithStore` → `acquireMiddleware` → `initialize` → handler chain → `saveSession` → `releaseMiddleware`.

### Domain Router Handler Wrapping

**`domainRouter.wrapHandlers`** (SYM: `domainRouter.wrapHandlers` at `domain.go:278`) — "Wraps every handler in the slice." Called during route registration to apply domain-scoped middleware wrapping.

### Request Context Access from Middleware

All middleware accesses request/response via context methods:
- `DefaultCtx.RequestCtx` (FOCUS: `ctx.go:118`) — Returns `*fasthttp.RequestCtx`. Called by adaptor middleware.
- `DefaultReq.RequestCtx` (FOCUS: `req.go:201`) — Same, from request interface.
- `DefaultRes.RequestCtx` (FOCUS: `res.go:248`) — Same, from response interface.
- `DefaultCtx.Request` (FOCUS: `ctx.go:178`) — Returns `*fasthttp.Request`.
- `DefaultReq.Request` (FOCUS: `req.go:348`) — Same, from request interface.

### Client-Side Request Hooks

The client package has its own hook pipeline:
- `Request.Send` (FOCUS: `client/request.go:673`) — Delegates to `newCore`. Called by `Custom`, `Delete`, `Get`, `Head`, `Options`, `Patch`, `Post`, `Put`.
- `setConfigToRequest` (FOCUS: `client/client.go:672`) — Applies config to request before sending.
- `Request.Context` (FOCUS: `client/request.go:115`) — Returns context. Called by `Send`, `HTTPMiddleware`, `handlerFunc`, etc.

### Cookie Handling in Pipeline

**`CookieJar.cookiesForRequest`** (FOCUS: `client/cookiejar.go:103`) — Filters cookies for a request by host, path, and security. Calls `domainMatch`, `pathMatch`, `Path`, `Secure`, `Lock`, `Unlock`.

### Summary Call Flow

```
Incoming Request
  → requestHandler
    → App.next / App.nextCustom
      → Route.match (find matching route)
      → Execute handler stack:
        → Middleware 1 (e.g., CORS New)
          → c.Next()
            → Middleware 2 (e.g., Auth New)
              → c.Next()
                → Final handler
        ← Response flows back up

Middleware Registration:
  App.Use / domainRouter.Use
    → toFiberHandler (adapter.go) — normalize handler types
    → App.register (router.go) — add to route tree
    → App.addRoute — store Route with middleware flag
```

### What Cannot Be Determined

Per GAPS: "uncovered: Middleware.Get, Middleware.Set, Request.Cookies, Middleware.Reset." The full implementations of session middleware's `Get`/`Set` operations, the `Request.Cookies` method, and `Middleware.Reset` are not detailed. The exact mechanism by which `requestHandler` invokes `App.next` (the HTTP server integration point with fasthttp) is referenced but not shown in the clue.
