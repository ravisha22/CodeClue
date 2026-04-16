# v2.5 Response: struct-fiber-1
Date: 2026-04-16

## Question
What are the main source files and packages in the Fiber framework, and how is the middleware organized?

## Answer

### Top-Level Package Structure

The Fiber framework (148 modules, 1472 symbols per the header `=CC v2.1 fiber@HEAD`) is organized into these top-level directories (TREE):

1. **Root package** — Core framework files (no directory prefix in INDEX).
2. **`addon/`** (2 files) — Add-on functionality like retry logic.
3. **`binder/`** (12 files) — Data binding.
4. **`client/`** (8 files) — HTTP client.
5. **`extractors/`** (1 file) — Request data extraction.
6. **`internal/`** (4 files) — Internal utilities.
7. **`log/`** (3 files) — Logging infrastructure.
8. **`middleware/`** (87 files) — The largest package, containing all middleware.

The INDEX lists 14 key modules explicitly, noting "...and 133 more modules."

### Core Framework Files (Root Package)

- **`app.go`** — Defines the `App` struct (FOCUS: `App` at `app.go:69-69`, "App denotes the Fiber application") with methods `Add`, `All`, `Config`, `Connect`, `Delete`, `Domain`, `Name` (SYM: `App.Name` at `app.go:783`, `App.Add` at `app.go:953`).
- **`router.go`** (767L) — Routing engine: `RebuildTree`, `RemoveRoute`, `RemoveRouteByName`, `RemoveRouteFunc`, `addPrefixToRoute` (INDEX). Contains `App.register` (SYM: `router.go:513`), `App.addRoute` (SYM: `router.go:590`), `App.next` (SYM: `router.go:115`), `App.nextCustom` (SYM: `router.go:216`), `App.normalizePath` (SYM: `router.go:398`), `App.pruneAutoHeadRouteLocked` (SYM: `router.go:491`), and the `Route` struct (FOCUS: `Route` at `router.go:45-46`).
- **`ctx.go`** — Request context: `DefaultCtx.Next` (SYM: `ctx.go:243`), `DefaultCtx.App` (SYM: `ctx.go:102`), `DefaultCtx.Path` (SYM: `ctx.go:297`), `DefaultCtx.String` (SYM: `ctx.go:571`), `DefaultCtx.RequestCtx` (SYM: `ctx.go:118`), `DefaultCtx.IsMiddleware` (FOCUS: `ctx.go:380-381`).
- **`ctx_interface.go`** — Defines `CustomCtx` (FOCUS: `CustomCtx` at `ctx_interface.go:13-14`), extending `Ctx` with additional methods.
- **`req.go`** — Request helpers: `DefaultReq.Body` (SYM: `req.go:149`), `DefaultReq.Host` (SYM: `req.go:465`), `DefaultReq.Locals` (SYM: `req.go:672`), `DefaultReq.App` (SYM: `req.go:83`), `DefaultReq.Accepts` (SYM: `req.go:51`).
- **`res.go`** (1153L) — Response helpers: `DefaultRes.Append` (SYM: `res.go:140`), `DefaultRes.Write` (SYM: `res.go:1098`), `DefaultRes.WriteString` (SYM: `res.go:1110`), `DefaultRes.App` (SYM: `res.go:134`), `DefaultRes.RequestCtx` (SYM: `res.go:248`).
- **`path.go`** (844L) — Path constraints: `CheckConstraint`, `Constraint`, `CustomConstraint`, `GetTrimmedParam`, `RemoveEscapeChar` (INDEX).
- **`helpers.go`** (1126L) — Utility functions: `isEtagStale`, `method`, `methodInt`, `quoteRawString`, `quoteString` (INDEX). `App.methodInt` (SYM: `helpers.go:923`).
- **`bind.go`** (477L) — Data binding: `AcquireBind`, `All`, `Body`, `CBOR`, `Cookie` (INDEX). `Bind.Body` (SYM: `bind.go:385`).
- **`mount.go`** (227L) — Sub-app mounting: `MountPath`, `appendSubAppLists`, `generateAppListKeys`, `hasMountedApps`, `mount` (INDEX).
- **`group.go`** — Route groups: `Group.Add` (SYM: `group.go:167`), `Group.Name` (SYM: `group.go:27`).
- **`domain.go`** — Domain-based routing: `domainRouter.Name` (SYM: `domain.go:602`), `domainRouter.Add` (SYM: `domain.go:530`), `domainRouter.wrapHandlers` (SYM: `domain.go:278`), `domainRouter.registerGroup` (SYM: `domain.go:336`), `domainRouter.Use` (FOCUS: `domain.go:350-350`).
- **`register.go`** — Route registration: `Registering.Add` (SYM: `register.go:111`).
- **`redirect_msgp.go`** (301L) — MessagePack for redirects (INDEX).
- **`adapter.go`** — Handler adaptation: `toFiberHandler` (FOCUS: `adapter.go:13-13`), `adaptFiberHandler` (FOCUS: `adapter.go:32-32`).

### Client Package (`client/`)

- **`client.go`** (863L) — HTTP client: `C`, `AddHeader`, `AddHeaders`, `AddParam`, `AddParams` (INDEX). `Client.LBClient` (SYM: `client/client.go:128`), `newClient` (SYM: `client/client.go:783`).
- **`request.go`** (1122L) — Request building: `AcquireFile`, `AcquireRequest`, `Add`, `All`, `Del` (INDEX). `Request.Send` (SYM: `client/request.go:673`), `Request.Get` (SYM: `client/request.go:633`), `Request.Reset` (SYM: `client/request.go:680`).
- **`response.go`** — Response handling: `Response.String` (SYM: `client/response.go:109`), `Response.Body` (SYM: `client/response.go:88`), `Response.Reset` (SYM: `client/response.go:193`).
- **`transport.go`** (377L) — Transport layer: `composeRedirectURL`, `doRedirectsWithClient`, `extractTLSConfig`, `forEachHostClient` (INDEX).
- **`cookiejar.go`** — Cookie management: `CookieJar.SetByHost` (SYM: `client/cookiejar.go:154`).
- **`hooks.go`** — Client hooks.

### Logging Package (`log/`)

- **`log.go`** (121L) — Logger interface: `CommonLogger`, `FormatLogger`, `Logger`, `WithLogger` (INDEX). `Level.toString` (SYM: `log/log.go:116`).
- **`default.go`** — Default logger: `defaultLogger.privateLog` (SYM: `log/default.go:24`), `defaultLogger.privateLogf` (SYM: `:47`), `defaultLogger.privateLogw` (SYM: `:74`), `defaultLogger.Errorf` (SYM: `:174`), `defaultLogger.Warnf` (SYM: `:169`).

### Add-on Package (`addon/`)

- **`addon/retry/exponential_backoff.go`** — `ExponentialBackoff.next` (SYM: `addon/retry/exponential_backoff.go:62`).

### Middleware Organization (`middleware/`, 87 files)

The middleware package is the largest, organized into sub-packages by functionality. Each middleware typically follows a `New(config ...Config)` factory pattern:

**Adaptor middleware** (`middleware/adaptor/`):
- `HTTPMiddleware` (FOCUS: `middleware/adaptor/adaptor.go:162`) — Wraps net/http middleware to Fiber middleware.
- `FiberHandler` (FOCUS: `:194`) — Wraps Fiber handler to net/http handler.
- `FiberHandlerFunc` (FOCUS: `:199`) — Wraps Fiber handler to net/http handler func.
- `FiberApp` (FOCUS: `:204`) — Wraps Fiber app to net/http handler func.
- `CopyContextToFiberContext` (FOCUS: `:101`) — Copies context.Context to fasthttp.RequestCtx.

**Session middleware** (`middleware/session/`):
- `Middleware` struct (FOCUS: `Middleware` at `middleware/session/middleware.go:13-13`) with methods `Delete`, `Destroy`, `Fresh`, `Get`, `ID`, `Keys`.
- `Middleware.initialize` (FOCUS: `:111`), `Middleware.Get` (FOCUS: `:214`), `Middleware.Set` (FOCUS: `:196`), `Middleware.Delete` (FOCUS: `:229`), `Middleware.Destroy` (FOCUS: `:259`), `Middleware.Reset` (FOCUS: `:300`), `Middleware.Regenerate` (FOCUS: `:318`), `Middleware.saveSession` (FOCUS: `:128`).
- `Session.Get` (SYM: `middleware/session/session.go:74`), `Session.Reset` (SYM: `:247`).
- `FromContext` (FOCUS: `middleware/session/middleware.go:179`) — Retrieves Middleware from Fiber context.

**Other middleware sub-packages** (each following the `New(config ...Config)` pattern):
- **Cache** (`middleware/cache/`) — `New` (FOCUS: `middleware/cache/cache.go:109`), with `manager_msgp.go` (945L, INDEX).
- **CORS** (`middleware/cors/`) — `New` (FOCUS: `middleware/cors/cors.go:28`).
- **CSRF** (`middleware/csrf/`) — `New` (FOCUS: `middleware/csrf/csrf.go:50`), with `storage_manager_msgp.go` (92L, INDEX).
- **Basic Auth** (`middleware/basicauth/`) — `New` (FOCUS: `middleware/basicauth/basicauth.go:27`).
- **Rate Limiter** (`middleware/limiter/`) — `New` (FOCUS: `middleware/limiter/limiter.go:23`), delegates to `cfg.LimiterMiddleware.New`.
- **Idempotency** (`middleware/idempotency/`) — `New` (FOCUS: `middleware/idempotency/idempotency.go:45`), with `MemoryLock` (SYM: `middleware/idempotency/locker.go`), `response_msgp.go` (282L, INDEX).
- **Request ID** (`middleware/requestid/`) — `New` (FOCUS: `middleware/requestid/requestid.go:18`).
- **Static files** (`middleware/static/`) — `New` (FOCUS: `middleware/static/static.go:121`).
- **Favicon** (`middleware/favicon/`) — `New` (FOCUS: `middleware/favicon/favicon.go:21`).
- **Paginate** (`middleware/paginate/`) — `buildPaginationURL` (SYM: `middleware/paginate/page_info.go:121`).

Many middleware sub-packages include `*_msgp.go` files (MessagePack serialization) with `DecodeMsg`, `EncodeMsg`, `MarshalMsg`, `Msgsize`, `UnmarshalMsg` methods (INDEX entries for cache, csrf, idempotency, limiter).

### What Cannot Be Determined

Per GAPS: "uncovered: Middleware.Fresh, Middleware.ID, Middleware.Keys, Middleware.Store." The full list of all 87 middleware files is not enumerated, and the internal session store implementation details are not covered.
