# v2.4.1 Response: struct-fiber-1
Date: 2026-04-16

## Main Source Files, Packages, and Middleware Organization

### Top-Level Directory Structure

The Fiber framework at HEAD contains **148 modules** and **1,472 symbols** (`=CC v2.1 fiber@HEAD 148mod 1472sym`) [Header]. The TREE section shows these top-level packages [TREE]:

| Directory | Files | Purpose |
|-----------|-------|---------|
| `addon/` | 2 | Add-on functionality |
| `binder/` | 12 | Request data binding |
| `client/` | 8 | HTTP client |
| `extractors/` | 1 | Value extraction |
| `internal/` | 4 | Internal utilities |
| `log/` | 3 | Logging |
| `middleware/` | 87 | Middleware modules |

### Core Source Files

- **`app.go`** (1,486 lines): Defines `App`, the Fiber application struct, with methods `Add`, `All`, `Config`, `Connect`, `Delete`, etc. [INDEX §app.go; FOCUS §App is not shown but SYM §App.Add at app.go:953 confirms it].
- **`router.go`**: Contains routing logic including `App.normalizePath` (`router.go:398`), `App.pruneAutoHeadRouteLocked` (`router.go:491`) [SYM §App.normalizePath, §App.pruneAutoHeadRouteLocked].
- **`ctx.go`**: Request context — `DefaultCtx.Get` (`ctx.go:200`), `DefaultCtx.IsMiddleware` (`ctx.go:380`) [SYM §DefaultCtx.Get; FOCUS §DefaultCtx.IsMiddleware].
- **`ctx_interface.go`**: Defines `CustomCtx` which extends `Ctx` with methods required by Fiber's internals and middleware helpers [FOCUS §CustomCtx, ctx_interface.go:13].
- **`req.go`** (1,140+ lines): Request helpers — `DefaultReq.Get` (`req.go:427`), `DefaultReq.Accepts` (`req.go:51`), `DefaultReq.Body` (`req.go:149`) [SYM §DefaultReq.Get, §DefaultReq.Accepts, §DefaultReq.Body].
- **`res.go`** (1,153 lines): Response helpers — `Cookie`, `App`, `Append`, `Attachment`, `AutoFormat` [INDEX §res.go].
- **`bind.go`** (477 lines): `Bind` struct providing request data binding methods (`AcquireBind`, `All`, `Body`, `CBOR`, `Cookie`) [INDEX §bind.go; FOCUS §Bind, bind.go:40].
- **`path.go`** (844 lines): Route path parsing — `CheckConstraint`, `Constraint`, `CustomConstraint`, `GetTrimmedParam`, `RemoveEscapeChar` [INDEX §path.go].
- **`redirect.go`** (433 lines): Redirect handling — `AcquireRedirect`, `FlashMessage`, `Back`, `Message` [INDEX §redirect.go].
- **`domain.go`** (688 lines): Domain-based routing — `DomainParam`, `domainMatcher`, `domainRouter` methods [INDEX §domain.go; SYM §domainRouter.Add, domain.go:530].
- **`group.go`**: Route groups — `Group.Add` (`group.go:167`) [SYM §Group.Add].
- **`register.go`**: Route registration — `Registering.Add` (`register.go:111`) [SYM §Registering.Add].
- **`hooks.go`**: Lifecycle hooks — `PreStartupMessageData.addEntry` (`hooks.go:164`) [SYM §PreStartupMessageData.addEntry].
- **`adapter.go`**: Handler type adaptation — `toFiberHandler` (`adapter.go:13`), `adaptFiberHandler` (`adapter.go:32`) [FOCUS §toFiberHandler, §adaptFiberHandler].

### Client Package (`client/`)

- **`client/client.go`** (863 lines): HTTP client `C` singleton (`client.go:810`), TLS config, dial settings [INDEX §client/client.go; SYM §C, §Client.SetTLSConfig].
- **`client/request.go`** (1,122 lines): `Request` type with methods `Send`, `Get`, `Put`, etc. [INDEX §client/request.go; FOCUS §Request.AddFiles, §Request.Files].
- **`client/response.go`** (241 lines): `Response` type — `Body`, `BodyStream`, `CBOR` [INDEX §client/response.go].
- **`client/transport.go`** (377 lines): Transport abstraction [INDEX §client/transport.go].
- **`client/cookiejar.go`** (334 lines): Cookie management — `CookieJar`, `Set`, `SetByHost` [INDEX §client/cookiejar.go].
- **`client/core.go`** (304 lines): Core execution pipeline — `execFunc`, `afterHooks` [INDEX §client/core.go].

### Middleware Organization

The `middleware/` directory contains **87 files** [TREE §middleware]. Each middleware follows a consistent pattern: a `Config` struct in a `config.go` file and a `New` constructor. Identified middleware packages include:

| Middleware | Config Location | Constructor |
|---|---|---|
| adaptor | `middleware/adaptor/adaptor.go` | `HTTPMiddleware`, `HTTPHandler`, `FiberHandler`, `FiberApp` [FOCUS §HTTPMiddleware, §FiberHandler, §FiberApp] |
| basicauth | `middleware/basicauth/config.go:22` | [FOCUS §Config basicauth] |
| cache | `middleware/cache/config.go:11` | [FOCUS §Config cache] |
| compress | `middleware/compress/config.go:8` | [FOCUS §Config compress] |
| cors | `middleware/cors/config.go:8` | [FOCUS §Config cors] |
| csrf | `middleware/csrf/config.go:15` | `New`, `DeleteToken`, `Handler`, `TokenFromContext` [INDEX §middleware/csrf/csrf.go; FOCUS §Config csrf] |
| earlydata | `middleware/earlydata/config.go:13` | [FOCUS §Config earlydata] |
| encryptcookie | `middleware/encryptcookie/config.go:8` | [FOCUS §Config encryptcookie] |
| envvar | `middleware/envvar/config.go:4` | [FOCUS §Config envvar] |
| etag | `middleware/etag/config.go:8` | [FOCUS §Config etag] |
| expvar | `middleware/expvar/config.go:8` | [FOCUS §Config expvar] |
| favicon | `middleware/favicon/config.go:10` | [FOCUS §Config favicon] |
| healthcheck | `middleware/healthcheck/config.go:24` | [FOCUS §Config healthcheck] |
| helmet | `middleware/helmet/config.go:8` | [FOCUS §Config helmet] |
| idempotency | `middleware/idempotency/config.go:15` | `MemoryLock.Lock`/`Unlock` [SYM; FOCUS §Config idempotency] |
| keyauth | `middleware/keyauth/config.go:19` | [FOCUS §Config keyauth] |
| limiter | `middleware/limiter/config.go:12` | `New` delegates to `cfg.LimiterMiddleware.New` [FOCUS §New limiter; §Config limiter] |
| logger | `middleware/logger/config.go:12` | [FOCUS §Config logger] |
| paginate | `middleware/paginate/config.go:10` | `NewPageInfo`, `buildPaginationURL` [INDEX §middleware/paginate; FOCUS §Config paginate] |
| pprof | `middleware/pprof/config.go:8` | [FOCUS §Config pprof] |
| proxy | `middleware/proxy/config.go:12` | `Do` [SYM §Do; FOCUS §Config proxy] |
| recover | `middleware/recover/config.go:8` | [FOCUS §Config recover] |
| redirect | `middleware/redirect/config.go:10` | `New` using `captureTokens` [FOCUS §New redirect; §Config redirect] |
| rewrite | `middleware/rewrite/rewrite.go:12` | `New` using `captureTokens` [FOCUS §New rewrite] |
| session | `middleware/session/` | `New`, `NewWithStore`, `Middleware`, `FromContext` [FOCUS §New session, §NewWithStore, §Middleware, §FromContext] |
| skip | `middleware/skip/skip.go:10` | `New` returns handler or skips based on predicate [FOCUS §New skip] |

### Internal and Logging

- **`internal/storage/memory/memory.go`** (233 lines): In-memory key-value store with `New`, `Close`, `Conn`, `Delete`, `Get` [INDEX §internal/storage/memory/memory.go].
- **`log/default.go`**: Default logger with `privateLog` (`log/default.go:24`), `privateLogf` (`log/default.go:47`), `privateLogw` (`log/default.go:74`) [SYM §defaultLogger.*].

### What Cannot Be Determined

- The full list of all 148 modules (INDEX shows 16 and notes "132 more") [INDEX].
- The full list of all 1,472 symbols (SYM shows ~72 and notes "1400 more") [SYM].
- The bodies of `Middleware.saveSession`, `Middleware.Get`, `Middleware.Delete`, `Middleware.Destroy` [GAPS: uncovered].
- How the remaining ~60 middleware files in `middleware/` are organized beyond the 26 Config entries shown [TREE vs FOCUS mismatch].
