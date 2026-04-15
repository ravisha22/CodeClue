# v2.3 Response: struct-fiber-1
Date: 2026-04-15

## Summary

The Fiber framework is organized around a root application file (`app.go`), core request/response modules, a rich `client/` sub-package, a `middleware/` directory containing 87 files spanning dozens of middleware types, and supporting packages for binding, logging, and internal storage. Middleware follows a consistent pattern: each middleware lives in its own sub-directory under `middleware/`, exposes a `New()` constructor, and is configured via a per-middleware `Config` struct.

---

## Main Source Files and Packages

### Root-Level Core Files

- **`app.go`** (1486 lines): The central application file. Defines the `App` type and its methods such as `App.Add` (app.go:953), `All`, `Config`, `Connect`, `Delete` (INDEX, line 34). This is the largest file in the repository and the entry point for application setup.
- **`bind.go`** (477 lines): Provides the `Bind` struct (bind.go:40, SYM line 102) with helper methods for binding request data to Go values, including `All`, `Body`, `CBOR`, `Cookie` methods. Also contains `Bind.validateStruct` (bind.go:183) and `Bind.returnBindErr` (bind.go:171).
- **`path.go`** (844 lines): Handles URL path matching and constraints — exports `CheckConstraint`, `Constraint`, `CustomConstraint`, `GetTrimmedParam`, `RemoveEscapeChar` (INDEX).
- **`res.go`** (1153 lines): Response-related functionality including `Cookie`, `App`, `Append`, `Attachment`, `AutoFormat` (INDEX).
- **`domain.go`** (688 lines): Domain-based routing with types like `DomainParam`, `domainCheckResult`, `domainMatcher` and methods such as `domainRouter.Add` (domain.go:530), `domainRouter.registerGroup` (domain.go:336), `domainRouter.registerPath` (domain.go:327), and `domainRouter.Name` (domain.go:602).
- **`redirect.go`** (433 lines): Redirect handling with `AcquireRedirect`, `FlashMessage`, `OldInputData`, `Back`, `Message` (INDEX).
- **`hooks.go`**: Application lifecycle hooks — `PreStartupMessageData.addEntry` (hooks.go:164).
- **`group.go`**: Route grouping — `Group.Add` (group.go:167).
- **`register.go`**: Route registration — `Registering.Add` (register.go:111).
- **`adapter.go`**: Handler adaptation — `toFiberHandler` (adapter.go:13) which dispatches to `adaptExpressHandler`, `adaptFastHTTPHandler`, `adaptFiberHandler`, `adaptHTTPHandler`; and `adaptFiberHandler` (adapter.go:32).
- **`ctx_interface.go`**: Defines the `CustomCtx` interface (ctx_interface.go:13-14), which extends `Ctx` with additional methods for Fiber's internals and middleware helpers.
- **`req.go`**: Request accessor methods — `DefaultReq.Get` (req.go:427), `DefaultReq.Accepts` (req.go:51), `DefaultReq.Body` (req.go:149), `DefaultReq.IsProxyTrusted` (req.go:1080), `DefaultCtx.MediaType` (req.go:244).

### `client/` Sub-Package (8 files)

- **`client/client.go`** (863 lines): HTTP client implementation — `C` function returns the default client (client/client.go:810), TLS configuration via `Client.SetTLSConfig` (client/client.go:249) and `Client.TLSConfig` (client/client.go:236), dial customization via `Client.SetDial` (client/client.go:606).
- **`client/request.go`** (1122 lines): Request construction and sending — `Request.Send` (client/request.go:673), `Request.SetMethod` (client/request.go:82), `Request.SetURL` (client/request.go:93), `Request.Reset` (client/request.go:680), cookie management via `Cookie.Add`/`Cookie.Del`/`Cookie.All`.
- **`client/transport.go`** (377 lines): Transport layer with redirect handling (`composeRedirectURL`, `doRedirectsWithClient`), load balancing (`walkBalancingClient` at client/transport.go:239, `walkBalancingClientWithBreak` at client/transport.go:268, `forEachHostClient` at client/transport.go:231).
- **`client/cookiejar.go`** (334 lines): Cookie jar implementation — `AcquireCookieJar`, `CookieJar.cookiesForRequest` (client/cookiejar.go:103), `CookieJar.SetByHost` (client/cookiejar.go:154).
- **`client/response.go`** (241 lines): Response handling — `AcquireResponse`, `ReleaseResponse`, `Response.Body` (client/response.go:88).
- **`client/core.go`** (304 lines): Core execution pipeline — `execFunc`, `afterHooks`, `acquireErrChan`, `acquireResponseChan`.

### Other Packages

- **`binder/`** (12 files): Data binding implementations, e.g. `binder/form.go` (124 lines) with `Bind`, `Reset`, `bindMultipart`, `FormBinding`.
- **`log/`** (3 files): Logging — `defaultLogger.privateLog` (log/default.go:24), `defaultLogger.privateLogf` (log/default.go:47), `defaultLogger.privateLogw` (log/default.go:74).
- **`internal/`** (4 files): Internal utilities — `internal/storage/memory/memory.go` (233 lines) with in-memory storage (`Entry`, `New`, `Close`, `Conn`, `Delete`).
- **`extractors/`** (1 file): Data extraction helpers.
- **`addon/`** (2 files): Add-on functionality.

---

## Middleware Organization

The `middleware/` directory contains **87 files** (TREE section) organized into sub-directories, each representing a distinct middleware concern. Key observations:

### Pattern: `New()` Constructor + `Config` Struct

Each middleware follows a consistent pattern of exposing:
1. A **`New()` function** that creates the middleware handler, typically accepting variadic `Config` parameters.
2. A **`Config` struct** defined in a separate config file within the same sub-directory.

Evidence for individual middleware:

| Middleware | `New()` Location | `Config` Location | Notes |
|---|---|---|---|
| **session** | `middleware/session/middleware.go:56` | `middleware/session/config.go:13` | `New` calls `NewWithStore`; `NewWithStore` (middleware.go:77) calls `initialize`, `saveSession`, `acquireMiddleware`, `releaseMiddleware` |
| **csrf** | `middleware/csrf/csrf.go:50` | `middleware/csrf/config.go:15` | Handles token creation/deletion, origin validation; raises panic |
| **cors** | `middleware/cors/cors.go:28` | — | Calls `isOriginSerializedOrNull`, `setPreflightHeaders`, `setSimpleHeaders`; raises panic |
| **cache** | `middleware/cache/cache.go:109` | `middleware/cache/config.go:11` | Complex caching with `allowsSharedCacheDirectives`, `appendWarningHeaders`, `cachedResponseAge`, etc. |
| **limiter** | `middleware/limiter/limiter.go:23` | `middleware/limiter/config.go:12` | Delegates to `cfg.LimiterMiddleware.New` |
| **basicauth** | `middleware/basicauth/basicauth.go:27` | `middleware/basicauth/config.go:22` | Calls `containsCTL`, `containsInvalidHeaderChars` |
| **compress** | `middleware/compress/compress.go:54` | `middleware/compress/config.go:8` | Dispatches based on config; calls `appendVaryAcceptEncoding`, `shouldSkip` |
| **static** | `middleware/static/static.go:121` | `middleware/static/config.go:11` | Calls `isFile`, `sanitizePath` |
| **redirect** | `middleware/redirect/redirect.go:13` | `middleware/redirect/config.go:10` | Accumulates loop with `captureTokens` |
| **rewrite** | `middleware/rewrite/rewrite.go:12` | — | Also uses `captureTokens` (both reference echo's rewrite middleware) |
| **recover** | — | `middleware/recover/config.go:8` | Recovery middleware |
| **idempotency** | — | `middleware/idempotency/config.go:15` | Uses `MemoryLock.Lock`/`Unlock` (middleware/idempotency/locker.go:25,41) |
| **proxy** | — | `middleware/proxy/config.go:12` | `Do` function (middleware/proxy/proxy.go:146) performs HTTP proxying |
| **encryptcookie** | — | `middleware/encryptcookie/config.go:8` | `decodeKey` utility (middleware/encryptcookie/utils.go:20) |
| **envvar** | — | `middleware/envvar/config.go:4` | Environment variable middleware |
| **requestid** | — | `middleware/requestid/config.go:9` | Request ID middleware |
| **favicon** | — | `middleware/favicon/config.go:10` | Favicon middleware |
| **responsetime** | — | `middleware/responsetime/config.go:8` | Response time middleware |
| **paginate** | — | `middleware/paginate/page_info.go:121` | Pagination with `NewPageInfo`, `buildPaginationURL`, cursor-based navigation |

### Adaptor Middleware (middleware/adaptor/)

A special middleware sub-package for interoperability between Fiber and Go's standard `net/http`:
- **`HTTPMiddleware`** (middleware/adaptor/adaptor.go:162): Wraps `net/http` middleware to Fiber middleware; calls `CopyContextToFiberContext` and `HTTPHandler`.
- **`HTTPHandler`** (middleware/adaptor/adaptor.go:56): Wraps `net/http` handler to Fiber handler.
- **`HTTPHandlerFunc`** (middleware/adaptor/adaptor.go:51): Wraps `net/http` handler func; delegates to `HTTPHandler`.
- **`HTTPHandlerWithContext`** (middleware/adaptor/adaptor.go:65): Like `HTTPHandler` but stores Fiber's user context; calls `LocalContextFromHTTPRequest`.
- **`FiberHandler`** (middleware/adaptor/adaptor.go:194): Wraps Fiber handler to `net/http` handler; delegates to `FiberHandlerFunc`.
- **`FiberHandlerFunc`** (middleware/adaptor/adaptor.go:199): Wraps Fiber handler to `net/http` handler func.
- **`FiberApp`** (middleware/adaptor/adaptor.go:204): Wraps entire Fiber app to `net/http` handler func.
- **`CopyContextToFiberContext`** (middleware/adaptor/adaptor.go:101): Copies `context.Context` values to `fasthttp.RequestCtx`.
- **`LocalContextFromHTTPRequest`** (middleware/adaptor/adaptor.go:78): Extracts Fiber user context from HTTP request.

### Session Middleware Architecture

The session middleware has a more elaborate structure:
- **`Middleware`** struct (middleware/session/middleware.go:13): Holds session data and configuration with methods `Delete`, `Destroy`, `Fresh`, `Get`, `ID`, `Keys`.
- **`FromContext`** (middleware/session/middleware.go:179): Retrieves middleware from Fiber context with a guard pattern.
- **`acquireMiddleware`** (middleware/session/middleware.go:141): Pool-based retrieval with panic guard.
- **`releaseMiddleware`** (middleware/session/middleware.go:157): Returns middleware to pool.
- **`Session.Get`** (middleware/session/session.go:74), **`Session.Reset`** (middleware/session/session.go:247), **`Session.refresh`** (middleware/session/session.go:278).

---

## Uncertainty / Limits

- The INDEX shows "...and 132 more modules" and the SYM section shows "...and 1400 more symbols", so only a fraction of the full codebase is visible. There may be additional middleware packages and core files not represented here.
- The GAPS section notes "80 symbols in L3, 28 with behavior annotations," meaning many symbols lack detailed behavioral documentation.
- The `router.go` file is referenced by symbols like `App.normalizePath` (router.go:398) and `App.pruneAutoHeadRouteLocked` (router.go:491) but does not appear explicitly in the INDEX, so its full contents are not captured.
- Some middleware (e.g., `recover`, `responsetime`, `envvar`, `requestid`, `favicon`) only have `Config` structs visible; their `New()` constructors may exist but are not in the focused symbols.
