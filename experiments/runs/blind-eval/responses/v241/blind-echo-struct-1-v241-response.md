# v2.4.1 Response: blind-echo-struct-1
Date: 2026-04-16

## How Echo's Public API Is Split Between Core and Middleware Packages

### Core Framework Package (root-level `.go` files)

The core package contains 15 source files including `echo.go` (865L), `router.go` (1074L), `context.go` (667L), `binder.go` (1329L), `bind.go` (472L), `group.go` (178L), `server.go` (202L), `response.go`, `httperror.go` (162L), and others [TREE section; INDEX section]. These files supply the foundational types and entry points:

1. **`Echo` – the top-level framework instance** (`echo.go:68`) with methods for route registration (`Add` at `echo.go:642`; per-method shortcuts `GET` at `echo.go:449`, `POST` at `echo.go:473`, `PUT` at `echo.go:479`, `DELETE` at `echo.go:443`, `HEAD` at `echo.go:455`, `PATCH` at `echo.go:467`, `TRACE` at `echo.go:485`, `CONNECT` not listed in FOCUS but implied by `Echo.Any` at `echo.go:504`), bulk registration (`Any` at `echo.go:504`, `AddRoute` at `echo.go:617`), static-file serving (`File` at `echo.go:609`), and server lifecycle (`Start` at `echo.go:744`) [FOCUS entries for each].
2. **Middleware attachment** is a core responsibility: `Echo.Use` adds middleware run *after* the router matches a route (`echo.go:431`), while `Echo.Pre` adds middleware run *before* the router attempts matching (`echo.go:426`) [FOCUS: Echo.Use, Echo.Pre].
3. **`Group`** (`group.go:14`) enables sub-route namespacing with a prefix and optional group-level middleware. It mirrors every HTTP-method shortcut on `Echo` (e.g., `Group.GET` at `group.go:37`, `Group.StaticFS` at `group.go:122`, `Group.Add` at `group.go:158`) [SYM: Group, group.go:14; FOCUS entries for Group methods].
4. **`Context`** (`context.go`) carries per-request state and exposes response helpers: `Blob` (`context.go:552`), `String` (`context.go:445`), `HTMLBlob` (`context.go:440`), `json` (`context.go:464`), `xml` (`context.go:517`), `File` (`context.go:571`), plus accessors like `Request` (`context.go:129`), `Response` (`context.go:139`), `QueryParam` (`context.go:287`), `FormValue` (`context.go:319`), and the generic `Get`/`Set` store (`context.go:380`, `context.go:387`) [SYM entries for each].
5. **Request binding** lives in core across three files: `bind.go` exposes `BindBody`, `BindHeaders`, `BindPathValues`, `BindQueryParams` [INDEX: bind.go]; `binder.go` (1329L) provides `ValueBinder` with typed extractors (`int`, `uint`, `float`, `bool`, `time`, `duration`, `unixTime`, etc.) and `FormFieldBinder`, `PathValuesBinder` [INDEX: binder.go; SYM entries]; `binder_generic.go` adds `bindValue` and `TimeOpts` [INDEX: binder_generic.go].
6. **Routing internals** are in `router.go` (1074L) with `DefaultRouter` and node-tree traversal, plus `router_concurrent.go` for concurrent access [TREE; INDEX: router.go].
7. **HTTP errors** are core: `HTTPError` and helper `StatusCode` in `httperror.go` (162L), and `DefaultHTTPErrorHandler` in `echo.go:374` [INDEX: httperror.go; FOCUS: DefaultHTTPErrorHandler].
8. **Server lifecycle** is in `server.go` (202L) with `Start`, `StartTLS`, `StartConfig`, and `gracefulShutdown` [INDEX: server.go; SYM: gracefulShutdown, server.go:183].
9. **Adapter functions** `WrapMiddleware` (`echo.go:766`) and `applyMiddleware` (`echo.go:785`) bridge standard `http.Handler` middleware into Echo's `MiddlewareFunc` type, and `MiddlewareConfigurator` (`echo.go:121`) defines the config-to-middleware interface [FOCUS entries].
10. **Testing helpers** in the `echotest/` sub-package (2 files) provide `ContextConfig`, `ToContext`, `ToContextRecorder`, and `ServeWithHandler` [INDEX: echotest/context.go; TREE: echotest/].

### Middleware Package (`middleware/` – 24 files)

All optional, cross-cutting HTTP behaviors are isolated in the `middleware/` sub-directory [TREE: middleware/ (24 files)]. Each middleware follows a consistent `Config` + `ToMiddleware` pattern [FOCUS entries]:

| Middleware | Config Type → Method | File |
|---|---|---|
| Gzip compression | `GzipConfig.ToMiddleware` | `middleware/compress.go` (235L) |
| CSRF protection | `CSRFConfig.ToMiddleware` | `middleware/csrf.go` (307L) |
| Static file serving (middleware variant) | `StaticConfig.ToMiddleware` | `middleware/static.go` (371L) |
| Reverse proxy | `ProxyConfig.ToMiddleware` | `middleware/proxy.go` (441L) |
| Trailing-slash manipulation | `AddTrailingSlashConfig.ToMiddleware`, `RemoveTrailingSlashConfig.ToMiddleware` | `middleware/slash.go` (151L) |
| Basic auth | `BasicAuthConfig.ToMiddleware` | `middleware/basic_auth.go` |
| Body dump | `BodyDumpConfig.ToMiddleware` | `middleware/body_dump.go` |
| Body limit | `BodyLimitConfig.ToMiddleware` | `middleware/body_limit.go` |
| CORS | `CORSConfig.ToMiddleware` | `middleware/cors.go` |
| Context timeout | `ContextTimeoutConfig.ToMiddleware` | `middleware/context_timeout.go` |
| Decompression | `DecompressConfig.ToMiddleware` | `middleware/decompress.go` |
| Key auth | `KeyAuthConfig.ToMiddleware` | `middleware/key_auth.go` |
| Method override | `MethodOverrideConfig.ToMiddleware` | `middleware/method_override.go` |
| Panic recovery | `RecoverConfig.ToMiddleware` | `middleware/recover.go` |
| Redirect | `RedirectConfig.ToMiddleware` | `middleware/redirect.go` |
| Request ID | `RequestIDConfig.ToMiddleware` | `middleware/request_id.go` |
| Request logger | `RequestLoggerConfig.ToMiddleware` | `middleware/request_logger.go` |
| URL rewrite | `RewriteConfig.ToMiddleware` | `middleware/rewrite.go` |
| Security headers | `SecureConfig.ToMiddleware` | `middleware/secure.go` |

[All from FOCUS section entries for each `*.ToMiddleware`]

Middleware configs commonly use a `PRECEDENCE(config)` behavior pattern and some add guards (e.g., `BasicAuthConfig.ToMiddleware`: `GUARD(config.Validator == nil -> return nil, errors....)` ; `BodyDumpConfig.ToMiddleware`: `GUARD(config.Handler == nil -> ...)`) [FOCUS behavior annotations].

### Design Boundary Summary

The core package owns **instance lifecycle** (`New`, `Start`), **routing** (`Add`, `AddRoute`, `Group`), **context/request/response plumbing** (`Context`, `Response`, binding), and **error handling** (`HTTPError`, `DefaultHTTPErrorHandler`). The middleware package provides **optional, pluggable behaviors** that consume the `MiddlewareConfigurator` interface (`echo.go:121`) and are attached via `Echo.Use` or `Echo.Pre` [FOCUS: MiddlewareConfigurator, Echo.Use, Echo.Pre].

### What Cannot Be Determined

- The clue file's SYM section is truncated ("...and 483 more symbols") and the INDEX lists "...and 27 more modules" [SYM line 125; INDEX line 40], so the **complete list of middleware packages** and **all core symbols** cannot be enumerated.
- The internal structure of `Echo` (its fields and unexported members) is not detailed; only its public methods are listed [FOCUS: Echo, echo.go:68 — methods list only].
- Whether the middleware package has sub-packages or just flat files cannot be confirmed beyond the 24-file count [TREE].
- The exact signatures and bodies of uncovered symbols (`Echo.Add`, `Echo.ServeHTTP`, `Echo.FileFS`, `Echo.serveHTTP`) are not available [GAPS section].
- How the `echotest/` package relates to the middleware package (if at all) is not stated.
