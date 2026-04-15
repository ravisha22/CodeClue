# v2.3 Response: rel-fiber-2
Date: 2026-04-15

## Summary

The clue file reveals two distinct request-handling domains in Fiber: (1) a **server-side pipeline** where middleware functions intercept incoming requests via the `Ctx` interface, and (2) a **client-side pipeline** in the `client/` package where hooks and a core execution engine manage outbound requests. Middleware connects to the server pipeline through `New()` factory functions that return Fiber handlers, while the adaptor middleware bridges Fiber's pipeline with Go's standard `net/http` ecosystem. The client pipeline uses a hook-based architecture with `preHooks`/`afterHooks` around a central `execFunc`.

---

## Server-Side Middleware → Request Pipeline

### Middleware Registration Pattern

Each middleware exposes a `New()` constructor that returns a Fiber handler, integrating into the request chain:

- **`New`** (middleware/limiter/limiter.go:23): "creates a new middleware handler"; behavior is `DELEGATE(cfg.LimiterMiddleware.New -> result)` — delegates to a configurable limiter strategy.
- **`New`** (middleware/session/middleware.go:56): "New initializes session middleware"; behavior is `GUARD(len -> handler)`; calls `NewWithStore`.
- **`NewWithStore`** (middleware/session/middleware.go:77): Creates session middleware; calls `initialize`, `saveSession`, `acquireMiddleware`, `releaseMiddleware` — showing the full session lifecycle within the middleware.

### Middleware Initialization and Context Access

- **`Middleware.initialize`** (middleware/session/middleware.go:111): "initialize sets up middleware for the request"; sig: `Middleware.initialize(c fiber.Ctx, cfg *Config)` — takes a `fiber.Ctx`, showing middleware directly receives the request context. Has `GUARD(err -> raise_panic)` and `UNWIND(defer)` behavior.
- **`acquireMiddleware`** (middleware/session/middleware.go:141): Pool-based retrieval with `GUARD(not_ok -> raise_panic)`.
- **`releaseMiddleware`** (middleware/session/middleware.go:157): Returns middleware instance to pool after request processing.

### Middleware Querying Context

Several middleware use `FromContext` patterns to retrieve state stored earlier in the pipeline:

- **`FromContext`** (middleware/session/middleware.go:179): "returns the Middleware from the Fiber context"; `GUARD(m -> pass_through)`.
- **`IsEarly`** (middleware/earlydata/earlydata.go:16): "returns true if the request used early data and was accepted by the middleware"; `DELEGATE(c.Locals -> result)` — uses Fiber's `Locals` storage.
- **`IsFromCache`** (middleware/idempotency/idempotency.go:29): "reports whether the middleware served the response from the cache"; `DELEGATE(c.Locals -> result)`.
- **`WasPutToCache`** (middleware/idempotency/idempotency.go:35): "reports whether the middleware stored the response"; `GUARD(wasPut -> pass_through)`.

### Middleware Skipping

- **`New`** (middleware/skip/skip.go:10): "returns a middleware that calls the provided predicate for each request"; sig: `New(handler fiber.Handler, exclude func(c fiber.Ctx))` with `GUARD(exclude -> handler)` — if the `exclude` predicate returns true, the middleware handler is skipped. This shows a meta-middleware pattern for conditional execution.

### Middleware ↔ Context Interaction

- **`DefaultCtx.IsMiddleware`** (ctx.go:380-381): "returns true if the current request handler was registered as middleware"; `GUARD(c -> value); PRECEDENCE(c)` — the context itself tracks whether the current handler is middleware.
- **`StoreInContext`** (helpers.go:83): "stores key/value in both Fiber locals and request context" — the bridge for middleware to persist data across the pipeline.
- **`DefaultCtx.RequestID`** (ctx.go:311-312): "returns the request identifier from the response header or request header"; calls `Get` and `GetRespHeader` — shows middleware (like requestid) can store values retrieved later by context methods.

### Request ID Pipeline

- **`sanitizeRequestID`** (middleware/requestid/requestid.go:43): "returns the provided request ID when it is valid, otherwise it tries up to three values from the config generator"; calls `isValidRequestID`; called by `New`.
- **`isValidRequestID`** (middleware/requestid/requestid.go:61): "reports whether the request ID contains only visible ASCII characters (0x20–0x7E) and is non-empty"; called by `sanitizeRequestID`.

### Error Handling in the Pipeline

- **`Error`** (app.go:62-63): "represents an error that occurred while handling a request" with method `Error`; called by `serverErrorHandler` and `DefaultErrorHandler` — the framework-level error type for the request pipeline.

---

## Adaptor: Bridging Fiber ↔ net/http

The adaptor middleware establishes call relationships between Fiber's pipeline and Go's `net/http`:

### net/http → Fiber Direction

- **`HTTPMiddleware`** (middleware/adaptor/adaptor.go:162): "wraps net/http middleware to fiber middleware"; calls `CopyContextToFiberContext` and `HTTPHandler` — converts standard Go middleware into Fiber-compatible handlers.
- **`HTTPHandler`** (middleware/adaptor/adaptor.go:56): "wraps net/http handler to fiber handler"; called by `HTTPHandlerFunc` and `HTTPMiddleware`.
- **`HTTPHandlerFunc`** (middleware/adaptor/adaptor.go:51): Wraps `http.HandlerFunc`; delegates to `HTTPHandler` — `DELEGATE(HTTPHandler -> result)`.
- **`HTTPHandlerWithContext`** (middleware/adaptor/adaptor.go:65): "like HTTPHandler, but additionally stores Fiber's user context in the request context"; calls `LocalContextFromHTTPRequest`.
- **`CopyContextToFiberContext`** (middleware/adaptor/adaptor.go:101): "copies the values of context.Context to a fasthttp.RequestCtx"; called by `HTTPMiddleware`. Behavior: `GUARD(requestContext -> none); PRECEDENCE(requestContext -> not_v.IsValid -> t); ACCUMULATE(loop -> result)`.
- **`ConvertRequest`** (middleware/adaptor/adaptor.go:89): "converts a fiber.Ctx to a http.Request"; `GUARD(err -> pass_through)`.
- **`LocalContextFromHTTPRequest`** (middleware/adaptor/adaptor.go:78): "extracts the Fiber user context previously stored into r.Context()"; `GUARD(r -> pass_through)`.

### Fiber → net/http Direction

- **`FiberHandler`** (middleware/adaptor/adaptor.go:194): "wraps fiber handler to net/http handler"; `DELEGATE(FiberHandlerFunc -> result)`.
- **`FiberHandlerFunc`** (middleware/adaptor/adaptor.go:199): "wraps fiber handler to net/http handler func"; `DELEGATE(handlerFunc -> result)`; called by `FiberHandler`.
- **`FiberApp`** (middleware/adaptor/adaptor.go:204): "wraps fiber app to net/http handler func"; `DELEGATE(handlerFunc -> result)`.

### Call Chain Summary (Adaptor)

```
net/http middleware → HTTPMiddleware → [CopyContextToFiberContext, HTTPHandler] → Fiber handler
net/http handler    → HTTPHandler → Fiber handler
net/http HandlerFunc → HTTPHandlerFunc → HTTPHandler → Fiber handler
Fiber handler → FiberHandlerFunc → net/http HandlerFunc
Fiber handler → FiberHandler → FiberHandlerFunc → net/http Handler
Fiber App     → FiberApp → net/http HandlerFunc
```

---

## Client-Side Request Pipeline

### Core Execution Engine

- **`core`** struct (client/core.go:48): "stores middleware and plugin definitions and defines the request execution process"; methods: `afterHooks`, `execFunc`, `execute`, `getRetryConfig`, `preHooks`, `timeout`.
- **`Request.Send`** (client/request.go:673): "Send executes the Request"; `DELEGATE(newCore -> result)`; calls `Client`, `Context`, `checkClient`. Called by `Custom`, `Delete`, `Get`, `Head`, `Options`, `Patch`, `Post`, `Put` — all HTTP method helpers delegate here.

### Hook-Based Middleware

- **`setConfigToRequest`** (client/client.go:672): "sets the parameters passed via Config to the Request"; calls `SetCookies`, `SetDisablePathNormalizing`, `SetHeaders`, `SetParams`, `SetPathParams`, `SetReferer`, `SetTimeout`, `SetUserAgent`. Called by all HTTP method helpers (`Custom`, `Delete`, `Get`, `Head`, `Options`, `Patch`, `Post`, `Put`).

### HTTP Method Helpers → Send Pipeline

All client HTTP methods follow the same pattern: set method, set URL, apply config, then call `Send`:

- **`Request.Get`** (client/request.go:633): `DELEGATE(r.SetURL -> result)`; calls `Send`, `SetMethod`, `SetURL`.
- **`Request.Put`** (client/request.go:648): Same pattern.
- **`Request.Delete`** (client/request.go:653): Same pattern.
- **`Request.Custom`** (client/request.go:668): Same pattern for custom HTTP methods.
- **`Request.SetMethod`** (client/request.go:82): Called by all HTTP helpers.
- **`Request.SetURL`** (client/request.go:93): Called by all HTTP helpers.

### Cache Control Parsing in Middleware

- **`parseRequestCacheControlString`** (middleware/cache/cache.go:1139): Delegates to `parseRequestCacheControl`.
- **`parseRequestCacheControl`** (middleware/cache/cache.go:1104): Calls `parseCacheControlDirectives` and `parseUintDirective`; called by `New` and `parseRequestCacheControlString`.
- **`requestCacheDirectives`** (middleware/cache/cache.go:61): The type that holds parsed cache directives.

---

## Call Relationship Diagram

```
SERVER-SIDE PIPELINE:
  Incoming Request
    → App routes to matched handler (Route.match → next/nextCustom)
    → Middleware chain (each New() returns fiber.Handler taking fiber.Ctx)
        → Middleware.initialize (session example)
        → StoreInContext / c.Locals (persist data)
        → FromContext / IsFromCache / IsEarly (query pipeline state)
        → DefaultCtx.IsMiddleware (introspect handler type)
    → Handler executes
    → Error → serverErrorHandler / DefaultErrorHandler

CLIENT-SIDE PIPELINE:
  Request.Get/Put/Delete/Custom
    → SetMethod + SetURL + setConfigToRequest
    → Request.Send
        → newCore
            → core.execute
                → preHooks
                → execFunc (send request, receive response)
                → afterHooks
                → timeout management

ADAPTOR BRIDGE:
  HTTPMiddleware → CopyContextToFiberContext + HTTPHandler
  FiberHandler → FiberHandlerFunc → net/http
```

---

## Uncertainty / Limits

- The server-side handler chain mechanism (how `next` is called to advance through middleware) is not directly visible; `Route.match` is called by `next` and `nextCustom` but these functions are not in the FOCUS section.
- The `core.execute` method (client/core.go:209) and its sub-calls (`preHooks`, `execFunc`, `afterHooks`, `timeout`) are referenced but not in this clue file's FOCUS entries, so the detailed hook execution order is inferred from the `calls` list.
- 132 more modules and 1400 more symbols are not shown, so additional middleware and pipeline components likely exist.
- The `CustomCtx` interface (ctx_interface.go:13-14) is mentioned but its exact relationship to the middleware pipeline is not elaborated beyond "extends Ctx with additional methods required by Fiber's internals and middleware helpers."
