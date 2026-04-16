# v2.4 Response: struct-fiber-1
Date: 2026-04-16

## Question
What are the main source files and packages in the Fiber framework, and how is the middleware organized?

## Answer

### Repository Structure

The clue file header (`=CC v2.1 fiber@HEAD 148mod 1472sym`) indicates the Fiber repository contains **148 modules** and **1472 symbols**.

The top-level TREE shows these packages:
- `addon/` (2 files) — add-on functionality
- `binder/` (12 files) — request data binding
- `client/` (8 files) — HTTP client implementation
- `extractors/` (1 file) — data extraction utilities
- `internal/` (4 files) — internal/private utilities
- `log/` (3 files) — logging infrastructure
- `middleware/` (87 files) — the largest package by file count

### Main Source Files (Root Package)

The INDEX section reveals the core root-level files:

| File | Lines | Key Symbols |
|------|-------|-------------|
| `app.go` | 1486L | `Add`, `All`, `Config`, `Connect`, `Delete` — the main application struct (`App`, app.go:69) |
| `bind.go` | 477L | `AcquireBind`, `All`, `Body`, `CBOR`, `Cookie` — request binding (`Bind`, bind.go:40) |
| `res.go` | 1153L | `Cookie`, `App`, `Append`, `Attachment`, `AutoFormat` — response handling |
| `path.go` | 844L | `CheckConstraint`, `Constraint`, `CustomConstraint`, `GetTrimmedParam`, `RemoveEscapeChar` — route pattern matching |
| `redirect.go` | 433L | `AcquireRedirect`, `FlashMessage`, `OldInputData`, `Back`, `Message` — redirect handling |
| `domain.go` | 688L | `DomainParam`, `domainCheckResult`, `domainLocalsKeyType`, `match`, `domainMatcher` — domain-based routing |

Additional root files referenced in FOCUS:
- `router.go` — contains `Route` (router.go:45-46), `Router` interface, and routing logic like `App.normalizePath` (router.go:398) and `App.pruneAutoHeadRouteLocked` (router.go:491)
- `ctx.go` — context implementation: `DefaultCtx.IsMiddleware` (ctx.go:380-381), `DefaultCtx.Get` (ctx.go:200)
- `ctx_interface.go` — `CustomCtx` (ctx_interface.go:13-14) extends `Ctx`
- `hooks.go` — `PreStartupMessageData.addEntry` (hooks.go:164)
- `req.go` — request helpers: `DefaultReq.Get` (req.go:427), `DefaultReq.Accepts` (req.go:51), `DefaultReq.Body` (req.go:149), `DefaultReq.MediaType` (req.go:244)
- `register.go` — `Register` (register.go:8-9) and `Registering.Add` (register.go:111)
- `adapter.go` — `toFiberHandler` (adapter.go:13) converts handler types to Fiber handlers
- `group.go` — `Group.Add` (group.go:167)
- `mount.go` — mounting sub-apps
- `helpers.go` — `StoreInContext` (helpers.go:83) and utility functions
- `state.go` — `State` (state.go:21) key-value store for app dependencies
- `listen.go` — `ListenConfig` (listen.go:44-45) for server startup

### Client Package (`client/`)

| File | Lines | Key Symbols |
|------|-------|-------------|
| `client/client.go` | 863L | `C`, `AddHeader`, `AddHeaders`, `AddParam`, `AddParams` |
| `client/request.go` | 1122L | `AcquireFile`, `AcquireRequest`, `Add`, `All`, `Del` — `Request` struct (client/request.go:46) |
| `client/transport.go` | 377L | `composeRedirectURL`, `doRedirectsWithClient`, `extractTLSConfig`, `forEachHostClient` |
| `client/cookiejar.go` | 334L | `AcquireCookieJar`, `Get`, `Release`, `Set`, `SetByHost` |
| `client/core.go` | 304L | `acquireErrChan`, `acquireResponseChan`, `addMissingPort`, `afterHooks`, `execFunc` — the `core` struct |
| `client/response.go` | 241L | `AcquireResponse`, `ReleaseResponse`, `Body`, `BodyStream`, `CBOR` — `Response` struct (client/response.go:19) |

### Internal Package (`internal/`)

- `internal/storage/memory/memory.go` (233L) — in-memory storage with `Entry`, `New`, `Close`, `Conn`, `Delete`

### Log Package (`log/`)

- `log/default.go` — `defaultLogger.privateLog` (log/default.go:24), `privateLogf` (log/default.go:47), `privateLogw` (log/default.go:74)

### Middleware Organization

The `middleware/` directory contains **87 files** organized into sub-packages by functionality. From the INDEX and FOCUS sections, the following middleware modules are identified:

**Adaptor** (`middleware/adaptor/`):
- `adaptor.go` — bidirectional handler conversion between Fiber and `net/http`
- Key functions: `HTTPHandler` (adaptor.go:56), `HTTPHandlerFunc` (adaptor.go:51), `HTTPMiddleware` (adaptor.go:162), `HTTPHandlerWithContext` (adaptor.go:65), `FiberHandler` (adaptor.go:194), `FiberHandlerFunc` (adaptor.go:199), `FiberApp` (adaptor.go:204), `CopyContextToFiberContext` (adaptor.go:101), `ConvertRequest` (adaptor.go:89), `LocalContextFromHTTPRequest` (adaptor.go:78)

**Session** (`middleware/session/`):
- `session.go` — `Session.Get` (session.go:74), `Session.Reset` (session.go:247), `Session.refresh` (session.go:278)
- `middleware.go` — `Middleware` struct (middleware.go:13), `New` (middleware.go:56), `NewWithStore` (middleware.go:77), `Middleware.initialize` (middleware.go:111), `FromContext` (middleware.go:179), `acquireMiddleware` (middleware.go:141), `releaseMiddleware` (middleware.go:157)
- `config.go` — `DefaultErrorHandler` (config.go:109)

**Cache** (`middleware/cache/`):
- `cache.go` (403+ lines) — `New` (cache.go:109), `parseUintDirective` (cache.go:937), `parseRequestCacheControl` (cache.go:1104)
- `manager.go` — `manager.logKey` (manager.go:210)

**CSRF** (`middleware/csrf/`):
- `csrf.go` (403L) — `DeleteToken`, `Handler`, `HandlerFromContext`, `New` (csrf.go:50), `TokenFromContext`
- `config.go` — `defaultErrorHandler` (config.go:142)

**Other middleware modules** (identified by `New` constructors and Config types in FOCUS):
- **CORS** — `New` (middleware/cors/cors.go:28) with origin validation
- **Static** — `New` (middleware/static/static.go:121) with `isFile`, `sanitizePath`
- **BasicAuth** — `New` (middleware/basicauth/basicauth.go:27) with `containsCTL`, `containsInvalidHeaderChars`; `Config` (middleware/basicauth/config.go:22)
- **Compress** — `New` (middleware/compress/compress.go:54) with `appendVaryAcceptEncoding`, `shouldSkip`
- **Limiter** — `New` (middleware/limiter/limiter.go:23) delegates to `cfg.LimiterMiddleware.New`
- **Redirect** — `New` (middleware/redirect/redirect.go:13) with `captureTokens`
- **Rewrite** — `New` (middleware/rewrite/rewrite.go:12) with `captureTokens`
- **Skip** — `New` (middleware/skip/skip.go:10) with predicate guard
- **Idempotency** — `MemoryLock.Lock` (idempotency/locker.go:25), `MemoryLock.Unlock` (idempotency/locker.go:41), `IsFromCache` (idempotency.go:29), `WasPutToCache` (idempotency.go:35)
- **EarlyData** — `IsEarly` (middleware/earlydata/earlydata.go:16)
- **EncryptCookie** — `decodeKey` (middleware/encryptcookie/utils.go:20)
- **RequestID** — `sanitizeRequestID` (middleware/requestid/requestid.go:43), `isValidRequestID` (requestid.go:61)
- **Proxy** — `Do` (middleware/proxy/proxy.go:146)
- **Paginate** — `NewPageInfo` (middleware/paginate/page_info.go), `buildPaginationURL` (page_info.go:121)
- **Recover** — implied by the existence of the middleware directory
- **ETag** — `Config` (middleware/etag/config.go:8)
- **Favicon** — `Config` (middleware/favicon/config.go:10)

### Middleware Pattern

Each middleware follows a consistent factory pattern: a `New(config ...Config)` constructor that returns a `fiber.Handler`. Configuration is provided via a `Config` struct specific to each middleware. Many middleware modules use `c.Locals` to store/retrieve per-request state (e.g., `IsEarly`, `IsFromCache`, `WasPutToCache`).

The `toFiberHandler` function (`toFiberHandler`, adapter.go:13) converts various handler types to Fiber handlers by dispatching on type, calling `adaptExpressHandler`, `adaptFastHTTPHandler`, `adaptFiberHandler`, or `adaptHTTPHandler`. This is used by `collectHandlers` (adapter.go:262).

### What Cannot Be Determined

- The complete list of all middleware sub-packages within the 87 files cannot be enumerated — the INDEX shows "...and 132 more modules."
- The `Middleware.saveSession`, `Middleware.Get`, `Middleware.Delete`, and `Middleware.Destroy` methods are listed as uncovered in GAPS.
- The exact file organization within each middleware sub-package (how many files per middleware) is not detailed.
