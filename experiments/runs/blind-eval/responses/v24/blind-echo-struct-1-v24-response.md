# v2.4 Response: blind-echo-struct-1
Date: 2026-04-16

## Question
How is Echo's public API split between the core framework package and middleware packages?

## Answer

### Core Framework Package (root-level files)

The core package exposes the central **`Echo`** struct, described as "the top-level framework instance" (`Echo`, echo.go:68), which serves as the primary entry point. It is instantiated via **`New`** (`New`, echo.go:333) and provides:

1. **Route registration methods** — a full set of HTTP-verb convenience methods that all delegate to `Echo.Add` (`Echo.Add`, echo.go:642):
   - `Echo.GET` (`Echo.GET`, echo.go:449), `Echo.POST` (`Echo.POST`, echo.go:473), `Echo.PUT` (`Echo.PUT`, echo.go:479), `Echo.DELETE` (`Echo.DELETE`, echo.go:443), `Echo.PATCH` (`Echo.PATCH`, echo.go:467), `Echo.HEAD` (`Echo.HEAD`, echo.go:455), `Echo.TRACE` (`Echo.TRACE`, echo.go:485), and `Echo.Any` (`Echo.Any`, echo.go:504).
   - Lower-level registration via `Echo.AddRoute` (`Echo.AddRoute`, echo.go:617) and `Echo.File` (`Echo.File`, echo.go:609).

2. **Middleware attachment** — two tiers:
   - `Echo.Pre` — middleware run *before* the router finds a matching route (`Echo.Pre`, echo.go:426).
   - `Echo.Use` — middleware run *after* routing but before the handler (`Echo.Use`, echo.go:431).

3. **Route grouping** — `Echo.Group` creates sub-route groups with a prefix and optional group-level middleware (`Echo.Group`, echo.go:659). The **`Group`** struct (`Group`, group.go:14) mirrors all of Echo's route-registration methods (e.g., `Group.GET` at group.go:37, `Group.Add` at group.go:158, `Group.StaticFS` at group.go:122).

4. **Request context** — the **`Context`** struct (`Context`, context.go) provides request/response accessors (`Context.Request`, context.go:129; `Context.Response`, context.go:139), parameter binding (`Context.Bind`, implied from index), data storage (`Context.Get`, context.go:380; `Context.Set`, context.go:387), and response helpers (`Context.String`, context.go:445; `Context.Blob`, context.go:552; `Context.HTMLBlob`, context.go:440; `Context.File`, context.go:571).

5. **Data binding** — spread across three core files:
   - `bind.go` (472L) with functions like `BindBody`, `BindHeaders`, `BindPathValues`, `BindQueryParams` (INDEX, bind.go).
   - `binder.go` (1329L) with the **`ValueBinder`** fluent API offering typed extraction: `int`, `uint`, `float`, `bool`, `time`, `duration`, `unixTime`, and their slice variants (e.g., `ValueBinder.int`, binder.go:515; `ValueBinder.float`, binder.go:1006; `ValueBinder.bool`, binder.go:920).
   - `binder_generic.go` (571L) with generic helpers like `bindValue` (INDEX, binder_generic.go).

6. **HTTP error handling** — `HTTPError` (`HTTPError`, httperror.go:107 from struct-2 FOCUS) and `DefaultHTTPErrorHandler` (`DefaultHTTPErrorHandler`, echo.go:374) provide error-to-response conversion. The helper `StatusCode` extracts status codes from errors (`StatusCode`, httperror.go:45).

7. **Server lifecycle** — `Echo.Start` (`Echo.Start`, echo.go:744) and `StartConfig.start` (`StartConfig.start`, server.go:100) manage HTTP server startup; `gracefulShutdown` (`gracefulShutdown`, server.go:183) handles shutdown.

8. **Interop adapters** — `WrapMiddleware` converts `func(http.Handler) http.Handler` into Echo's `MiddlewareFunc` (`WrapMiddleware`, echo.go:766), and `applyMiddleware` chains middleware around a handler (`applyMiddleware`, echo.go:785).

9. **Testing utilities** — the `echotest/` sub-package (2 files) provides `ContextConfig`, `ToContext`, `ToContextRecorder`, and `ServeWithHandler` for constructing test contexts (`echotest/context.go` INDEX).

### Middleware Package (`middleware/`)

The `middleware/` directory contains **24 files** (TREE section) and houses all optional, pluggable middleware. Each middleware follows a consistent pattern:
- A **Config struct** with a `ToMiddleware()` method that returns `(echo.MiddlewareFunc, error)`.
- A convenience constructor that calls `ToMiddleware` internally.

Middleware identified in the clue file includes:

| Middleware | File | Config/Entry Point |
|---|---|---|
| Gzip compression | middleware/compress.go (235L) | `GzipConfig.ToMiddleware` (middleware/compress.go:69) |
| Reverse proxy | middleware/proxy.go (441L) | `ProxyConfig.ToMiddleware` (middleware/proxy.go:305) |
| Trailing slash | middleware/slash.go (151L) | `AddTrailingSlashConfig.ToMiddleware` (middleware/slash.go:39), `RemoveTrailingSlashConfig.ToMiddleware` (middleware/slash.go:103) |
| CSRF protection | middleware/csrf.go (307L) | `CSRFConfig.ToMiddleware` (middleware/csrf.go:126) |
| Static file serving | middleware/static.go (371L) | `StaticConfig.ToMiddleware` (middleware/static.go:156) |
| Basic auth | middleware/basic_auth.go | `BasicAuthConfig.ToMiddleware` (middleware/basic_auth.go:97) |
| Body dump | middleware/body_dump.go | `BodyDumpConfig.ToMiddleware` (middleware/body_dump.go:73) |
| Body limit | middleware/body_limit.go | `BodyLimitConfig.ToMiddleware` (middleware/body_limit.go:47) |
| CORS | middleware/cors.go | `CORSConfig.ToMiddleware` (middleware/cors.go:145) |
| Context timeout | middleware/context_timeout.go | `ContextTimeoutConfig.ToMiddleware` (middleware/context_timeout.go:38) |
| Key auth | middleware/key_auth.go | `KeyAuthConfig.ToMiddleware` (middleware/key_auth.go:138) |
| Method override | middleware/method_override.go | `MethodOverrideConfig.ToMiddleware` (middleware/method_override.go:46) |
| Recover | middleware/recover.go | `RecoverConfig.ToMiddleware` (middleware/recover.go:53) |
| Redirect | middleware/redirect.go | `RedirectConfig.ToMiddleware` (middleware/redirect.go:119) |
| Request ID | middleware/request_id.go | `RequestIDConfig.ToMiddleware` (middleware/request_id.go:42) |
| Request logger | middleware/request_logger.go | `RequestLoggerConfig.ToMiddleware` (middleware/request_logger.go:246) |
| Rewrite | middleware/rewrite.go | `RewriteConfig.ToMiddleware` (middleware/rewrite.go:53) |
| Secure headers | middleware/secure.go | `SecureConfig.ToMiddleware` (middleware/secure.go:101) |
| Decompression | middleware/decompress.go | `DecompressConfig.ToMiddleware` (middleware/decompress.go:65) |
| Rate limiter | middleware/rate_limiter.go | referenced via `RateLimiterMemoryStore.cleanupStaleVisitors` (middleware/rate_limiter.go:256) |

### Key Architectural Split

The **`MiddlewareConfigurator`** interface (`MiddlewareConfigurator`, echo.go:121) defines the contract: any config struct implementing `ToMiddleware()` can produce middleware. This interface lives in the core package, but all concrete implementations live in `middleware/`.

The core package owns: routing, context, binding, error handling, server lifecycle, and the middleware-attachment API (`Pre`/`Use`). The middleware package provides all cross-cutting concerns as opt-in plugins.

### Cannot Be Determined from the Clue File

- The exact fields of the `Echo` struct, `Config` struct, or any middleware config structs (only method lists are shown).
- The full body logic of `Echo.ServeHTTP` or `Echo.serveHTTP` (listed as uncovered in GAPS).
- Whether there are additional packages beyond `middleware/` and `echotest/` (the INDEX notes "...and 27 more modules").
- The complete list of all 565 symbols (only ~80 are shown in L3 FOCUS, with 483+ truncated).
