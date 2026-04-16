# v2.4.1 Response: rel-fiber-2
Date: 2026-04-16

## Middleware ↔ Request-Handling Pipeline Call Relationships

### Pipeline Entry Point

The request handling pipeline is driven by `App.next` (`router.go:115`) and `App.nextCustom` (`router.go:216`), both called by `requestHandler`. They iterate through registered routes calling `Route.match` to find a handler [listed in GAPS as uncovered — their bodies are not provided, but their role is established by the call graph].

### Middleware Registration

Middleware is registered via `App.Use` (not in FOCUS but referenced implicitly). The adaptor layer converts between handler types: `toFiberHandler` (`adapter.go:13`) dispatches to `adaptFiberHandler`, `adaptFastHTTPHandler`, `adaptFiberHandler`, `adaptHTTPHandler`. It is called by `collectHandlers` [referenced from struct-fiber-1 context; not in this FOCUS but part of the codebase].

### Middleware → Pipeline Interactions

1. **Skip Middleware**: `skip.New` (`middleware/skip/skip.go:10`) takes a handler and a predicate. If `exclude` is nil, the original handler is returned directly (GUARD). Otherwise, the predicate is called per-request to decide whether to skip [FOCUS §New skip].

2. **Session Middleware**: `session.New` (`middleware/session/middleware.go:56`) creates session middleware, calling `NewWithStore` [FOCUS §New session]. `NewWithStore` (`middleware/session/middleware.go:77`) calls `initialize`, `saveSession`, `acquireMiddleware`, and `releaseMiddleware` [FOCUS §NewWithStore]. `Middleware.initialize` (`middleware/session/middleware.go:111`) sets up middleware for each request; it panics on error and uses `UNWIND(defer)` [FOCUS §Middleware.initialize]. `FromContext` (`middleware/session/middleware.go:179`) extracts the session middleware from the Fiber context using `fiber.ValueFromContext` [FOCUS §FromContext session].

3. **Early Data**: `IsEarly` (`middleware/earlydata/earlydata.go:16`) reads from `c.Locals` to check if the request used early data [FOCUS §IsEarly].

4. **Idempotency**: `IsFromCache` (`middleware/idempotency/idempotency.go:29`) checks `c.Locals` to see if the response was served from cache. `WasPutToCache` (`middleware/idempotency/idempotency.go:35`) similarly checks if the response was stored in cache [FOCUS §IsFromCache, §WasPutToCache].

5. **Request ID**: `sanitizeRequestID` (`middleware/requestid/requestid.go:43`) validates and optionally regenerates request IDs by calling `isValidRequestID` in a loop (up to three generator attempts) [FOCUS §sanitizeRequestID]. `isValidRequestID` (`middleware/requestid/requestid.go:61`) checks for visible ASCII characters [FOCUS §isValidRequestID]. `DefaultCtx.RequestID` (`ctx.go:311`) reads the ID from response or request headers [FOCUS §DefaultCtx.RequestID].

6. **Cache Middleware**: `parseRequestCacheControl` (`middleware/cache/cache.go:1104`) parses cache-control directives by calling `parseCacheControlDirectives` and `parseUintDirective`. It is called by both `New` and `parseRequestCacheControlString` [FOCUS §parseRequestCacheControl]. `parseRequestCacheControlString` (`middleware/cache/cache.go:1139`) is a string-based wrapper [FOCUS §parseRequestCacheControlString].

### Adaptor Layer (net/http ↔ Fiber)

The adaptor module establishes bidirectional call relationships:

- **net/http → Fiber**: `HTTPHandler` (`middleware/adaptor/adaptor.go:56`) wraps a `http.Handler` as a `fiber.Handler`. `HTTPHandlerFunc` (`adaptor.go:51`) delegates to `HTTPHandler`. `HTTPMiddleware` (`adaptor.go:162`) wraps `net/http` middleware to Fiber middleware, calling both `CopyContextToFiberContext` and `HTTPHandler` [FOCUS §HTTPHandler, §HTTPHandlerFunc, §HTTPMiddleware].

- **Fiber → net/http**: `FiberHandler` (`adaptor.go:194`) wraps a Fiber handler as `http.Handler` by delegating to `FiberHandlerFunc` (`adaptor.go:199`), which calls `handlerFunc` [FOCUS §FiberHandler, §FiberHandlerFunc]. `FiberApp` (`adaptor.go:204`) wraps an entire Fiber app as `http.HandlerFunc` [FOCUS §FiberApp].

- **Context Bridging**: `CopyContextToFiberContext` (`adaptor.go:101`) copies `context.Context` values to `fasthttp.RequestCtx`, called by `HTTPMiddleware` [FOCUS §CopyContextToFiberContext]. `HTTPHandlerWithContext` (`adaptor.go:65`) stores Fiber's user context in the request context, calling `LocalContextFromHTTPRequest` [FOCUS §HTTPHandlerWithContext]. `ConvertRequest` (`adaptor.go:89`) converts `fiber.Ctx` to `*http.Request` [FOCUS §ConvertRequest].

### Client-Side Pipeline

The client module has its own middleware-like pipeline:

- `core` (`client/core.go:48`) stores middleware/plugin definitions and defines the request execution process [FOCUS §core].
- `Request.Send` (`client/request.go:673`) executes a request. All HTTP verb methods (`Get`, `Put`, `Delete`, `Custom`, `Head`, `Options`, `Patch`, `Post`) call `Send`, `SetMethod`, and `SetURL` [FOCUS §Request.Send, §Request.Get, §Request.Put, §Request.Delete, §Request.Custom].
- `setConfigToRequest` (`client/client.go:672`) applies client-level configuration to requests, calling `SetCookies`, `SetHeaders`, `SetParams`, etc. [FOCUS §setConfigToRequest].
- `AcquireRequest` (`client/request.go:983`) returns pooled request objects; panics on type assertion failure [FOCUS §AcquireRequest].

### Context Inspection by Middleware

`DefaultCtx.IsMiddleware` (`ctx.go:380`) returns whether the current handler was registered as middleware, guarding on `c.route == nil` [FOCUS §DefaultCtx.IsMiddleware]. `StoreInContext` (`helpers.go:83`) stores values in both Fiber locals and request context [FOCUS §StoreInContext].

### Error Handling in Pipeline

`Error` (`app.go:62`) represents errors during request handling, called by `serverErrorHandler` and `DefaultErrorHandler` [FOCUS §Error].

### What Cannot Be Determined

- The bodies of `App.next`/`App.nextCustom` — how the dispatch loop iterates through middleware and route handlers [GAPS: uncovered].
- The body of `Request.resetBody` and `Request.checkClient` [GAPS: uncovered].
- `Middleware.saveSession` and `Middleware.Get` internals [GAPS: uncovered].
- How middleware ordering is enforced (FIFO vs priority) — not described in the clue file.
- Whether `c.Next()` exists and how it advances through the middleware chain — not referenced in any FOCUS or SYM entry.
