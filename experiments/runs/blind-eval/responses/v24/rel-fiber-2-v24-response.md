# v2.4 Response: rel-fiber-2
Date: 2026-04-16

## Question
What are the call relationships between middleware and the request handling pipeline in Fiber?

## Answer

### The Request Handling Pipeline

The server-side request handling pipeline is not fully exposed in the FOCUS section (notably `App.requestHandler`, `DefaultCtx.Request`, and `DefaultCtx.RequestCtx` are listed as uncovered in GAPS), but the clue file reveals the following call relationships.

### Middleware ↔ Handler Adaptor Layer

The `middleware/adaptor` package provides bidirectional conversion between Fiber handlers and `net/http` handlers:

**net/http → Fiber direction:**
- `HTTPHandlerFunc` (`HTTPHandlerFunc`, middleware/adaptor/adaptor.go:51) wraps `http.HandlerFunc` to `fiber.Handler` via `DELEGATE(HTTPHandler -> result)`, calling `HTTPHandler`.
- `HTTPHandler` (`HTTPHandler`, middleware/adaptor/adaptor.go:56) wraps `http.Handler` to `fiber.Handler`. It is called by `HTTPHandlerFunc` and `HTTPMiddleware`.
- `HTTPMiddleware` (`HTTPMiddleware`, middleware/adaptor/adaptor.go:162) wraps `net/http` middleware to Fiber middleware. It calls `CopyContextToFiberContext` and `HTTPHandler`.
- `CopyContextToFiberContext` (`CopyContextToFiberContext`, middleware/adaptor/adaptor.go:101) copies `context.Context` values to `fasthttp.RequestCtx`. Called by `HTTPMiddleware`.
- `HTTPHandlerWithContext` (`HTTPHandlerWithContext`, middleware/adaptor/adaptor.go:65) is like `HTTPHandler` but additionally stores Fiber's user context. It calls `LocalContextFromHTTPRequest`.

**Fiber → net/http direction:**
- `FiberHandler` (`FiberHandler`, middleware/adaptor/adaptor.go:194) wraps Fiber handler to `net/http` handler via `DELEGATE(FiberHandlerFunc -> result)`.
- `FiberHandlerFunc` (`FiberHandlerFunc`, middleware/adaptor/adaptor.go:199) wraps Fiber handler to `net/http` handler func. Called by `FiberHandler`.
- `FiberApp` (`FiberApp`, middleware/adaptor/adaptor.go:204) wraps a Fiber app to `net/http` handler func via `DELEGATE(handlerFunc -> result)`.

Call chain summary:
```
HTTPMiddleware → CopyContextToFiberContext + HTTPHandler
HTTPHandlerFunc → HTTPHandler
FiberHandler → FiberHandlerFunc → handlerFunc
FiberApp → handlerFunc
```

### Middleware as Context Inspectors

- `DefaultCtx.IsMiddleware` (`DefaultCtx.IsMiddleware`, ctx.go:380-381) returns true if the current handler was registered as middleware. Behavior: `GUARD(c.route == nil -> return false)`.
- `FromContext` (session) (`FromContext`, middleware/session/middleware.go:179) extracts the session `Middleware` from Fiber context using `fiber.ValueFromContext`.
- `IsEarly` (`IsEarly`, middleware/earlydata/earlydata.go:16) checks early data via `DELEGATE(c.Locals -> result)`.
- `IsFromCache` (`IsFromCache`, middleware/idempotency/idempotency.go:29) checks cache status via `DELEGATE(c.Locals -> result)`.
- `WasPutToCache` (`WasPutToCache`, middleware/idempotency/idempotency.go:35) checks cache write via guard on `val.(bool)`.

These middleware utility functions read request state through `c.Locals` or `fiber.ValueFromContext`, establishing a data-flow relationship with the pipeline context.

### Session Middleware Pipeline

The session middleware has an internal pipeline:
- `New` (session) (`New`, middleware/session/middleware.go:56) initializes session middleware and calls `NewWithStore`.
- `NewWithStore` (`NewWithStore`, middleware/session/middleware.go:77) calls `initialize`, `saveSession`, `acquireMiddleware`, and `releaseMiddleware`.
- `Middleware.initialize` (`Middleware.initialize`, middleware/session/middleware.go:111) sets up middleware for the request. It panics on error and is called by `NewWithStore`.
- `acquireMiddleware` (`acquireMiddleware` — referenced in NewWithStore's calls) retrieves a middleware instance from the pool.

### Client-Side Request Pipeline

The client package has its own request pipeline:
- `Request.Send` (`Request.Send`, client/request.go:673) executes the request via `DELEGATE(newCore -> result)`, calling `Client`, `Context`, `checkClient`.
- All HTTP verb methods delegate to `Send`: `Request.Get` → `Send` + `SetMethod` + `SetURL` (`Request.Get`, client/request.go:633); same for `Put` (client/request.go:648), `Delete` (client/request.go:653), `Custom` (client/request.go:668).
- `setConfigToRequest` (`setConfigToRequest`, client/client.go:672) applies client-level config to the request. Called by all HTTP verb methods on the Client.
- The `core` struct (`core`, client/core.go:48) stores middleware and plugin definitions: methods include `afterHooks`, `execFunc`, `execute`, `preHooks`, `timeout`.

### Cache Middleware Pipeline

- `parseRequestCacheControl` (`parseRequestCacheControl`, middleware/cache/cache.go:1104) parses cache-control directives, calling `parseCacheControlDirectives` and `parseUintDirective`. Called by `New` and `parseRequestCacheControlString`.
- `parseRequestCacheControlString` (`parseRequestCacheControlString`, middleware/cache/cache.go:1139) delegates to `parseRequestCacheControl`.

### Skip Middleware

- `New` (skip) (`New`, middleware/skip/skip.go:10) creates middleware with a predicate. Behavior: `GUARD(exclude == nil -> return handler)` — if no predicate, returns the handler directly without wrapping.

### Error Handling in the Pipeline

- `Error` (`Error`, app.go:62-63) represents request handling errors. Called by `serverErrorHandler` and `DefaultErrorHandler`.
- `CustomCtx` (`CustomCtx`, ctx_interface.go:13-14) extends `Ctx` with methods required by Fiber's internals and middleware helpers.

### Request Data Flow

- `ConvertRequest` (`ConvertRequest`, middleware/adaptor/adaptor.go:89) converts `fiber.Ctx` to `http.Request`, bridging between Fiber's request pipeline and `net/http`.
- `StoreInContext` (`StoreInContext`, helpers.go:83) stores key/value in both Fiber locals and request context, enabling middleware to share data through the pipeline.
- `DefaultCtx.RequestID` (`DefaultCtx.RequestID`, ctx.go:311-312) retrieves the request ID from response or request headers, calling `Get` and `GetRespHeader`.
- `sanitizeRequestID` (`sanitizeRequestID`, middleware/requestid/requestid.go:43) validates request IDs, calling `isValidRequestID` (`isValidRequestID`, middleware/requestid/requestid.go:61).

### What Cannot Be Determined

- The full call chain from `App.requestHandler` through `next`/`nextCustom` to handler invocation is not in the FOCUS section. `App.requestHandler`, `DefaultCtx.Request`, `DefaultCtx.RequestCtx`, and `DefaultReq.Request` are listed as **uncovered** in GAPS.
- How middleware ordering is enforced (the stack iteration order) is not detailed.
- The exact mechanism by which `c.Next()` advances to the next middleware in the chain is not described in the clue file.
