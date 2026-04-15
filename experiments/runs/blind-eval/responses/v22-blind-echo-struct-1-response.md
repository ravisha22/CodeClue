# v2.2 Response: blind-echo-struct-1
Date: 2026-04-15

## Question
How is Echo's public API split between the core framework package and middleware packages?

## Answer

### 1. Package Layout

The repository is split into two main areas visible from the TREE section:

- **Core framework** – 15 top-level `.go` files (e.g. `echo.go`, `context.go`, `router.go`, `group.go`, `bind.go`, `binder.go`, `binder_generic.go`, `httperror.go`, `ip.go`, `json.go`, `renderer.go`, `response.go`, `route.go`, `router_concurrent.go`, `context_generic.go`) plus a `echotest/` helper directory with 2 files.
- **Middleware package** – a `middleware/` subdirectory containing 24 files (TREE: `middleware/ (24 files)`).

### 2. Core Framework Package — Public API Surface

The core package exposes the following major areas:

**Application lifecycle & configuration:**
- `New` (echo.go:333) — creates an `Echo` instance; called by `NewWithConfig` and `main`.
- `Echo` (echo.go:68) — the top-level framework instance with methods: `AcquireContext`, `Add`, `AddRoute`, `Any`, `CONNECT`, `DELETE`, etc.
- `Echo.Start` (echo.go:744) — starts the HTTP server.
- `Echo.Use` (echo.go:431) — adds middleware to the chain, run after router has found a matching route and before the handler.
- `Config` (INDEX: echo.go) — configuration type.
- `MiddlewareConfigurator` (echo.go:121) — interface for creating middleware handlers with the possibility of returning a configuration error.

**Routing:**
- `Echo.Add` (echo.go:642) — registers a new route for an HTTP method and path.
- `Echo.AddRoute` (echo.go:617) — registers a new Route with default host Router.
- `Echo.GET` (echo.go:449) — registers a GET route; delegates to `e.Add`.
- `Echo.File` (echo.go:609) — registers a route to serve a static file.
- `Group` (group.go:14) — a set of sub-routes for a specified route prefix.
- `Group.Add` (group.go:158) — implements `Echo#Add()` for sub-routes.
- `Group.AddRoute` (group.go:172) — registers a new Routable with Router.
- `Group.GET` (group.go:37) — implements `Echo#GET()` for sub-routes.
- `Group.StaticFS` (group.go:122) — implements `Echo#StaticFS()` for sub-routes.

**Request context & response helpers:**
- `Context` (context.go, 667 lines) — extensive public API including: `Bind`, `Blob`, `Cookie`, `Cookies`, `File`, `FormValue`, `Get`, `Set`, `IsTLS`, `Response`, `json`, `xml`, `contentDisposition`, etc.
- `Context.Get` (context.go:380) — retrieves data from the context.
- `Context.Set` (context.go:387) — saves data in the context.
- `Context.Blob` (context.go:552) — sends a blob response.
- `Context.File` (context.go:571) — sends a response with file content.
- `Context.Response` (context.go:139) — returns `*Response`.

**Data binding:**
- `BindPathValues` (bind.go:42) — binds path parameter values.
- `BindBody`, `BindHeaders`, `BindQueryParams` (INDEX: bind.go) — bind various request data sources.
- `ValueBinder` (binder.go) — provides utility methods for binding to Go built-in types (int, float, bool, time, duration, etc.).
- `BindingError` (binder.go) — represents binding errors.

**Error handling:**
- `HTTPError` (httperror.go:107) — represents an error that occurred while handling a request; methods: `Error`, `StatusCode`, `Unwrap`, `Wrap`.
- `DefaultHTTPErrorHandler` (INDEX: echo.go) — default error handler.

**IP extraction:**
- `ExtractIPDirect`, `ExtractIPFromRealIPHeader`, `ExtractIPFromXFFHeader`, `LegacyIPExtractor`, `TrustIPRange` (INDEX: ip.go).

**JSON serialization:**
- `DefaultJSONSerializer` (INDEX: json.go) — with `Serialize` and `Deserialize`.

**Interop helpers:**
- `WrapMiddleware` (echo.go:766) — wraps `func(http.Handler) http.Handler` into `echo.MiddlewareFunc`.
- `WrapHandler` (echo.go:752 in the struct-2 clue) — wraps `http.Handler` into `echo.HandlerFunc`.
- `NewDefaultFS` (echo.go:804) — returns a new defaultFS instance.
- `applyMiddleware` (echo.go:785) — applies middleware; called by `serveHTTP`.

**Testing helpers (echotest/):**
- `ServeWithHandler`, `ToContext`, `ToContextRecorder` (echotest/context.go) — test context creation.
- `LoadBytes`, `TrimNewlineEnd` (echotest/reader.go) — test data helpers.

### 3. Middleware Package — Public API Surface

Every middleware follows a consistent dual-function pattern: a convenience constructor and a `WithConfig` variant. All `WithConfig` functions exhibit `DELEGATE(toMiddlewareOrPanic -> result)` behavior. Observed middleware (each in its own file under `middleware/`):

| Middleware | Convenience Function | WithConfig Function | File |
|---|---|---|---|
| BasicAuth | `BasicAuth` | `BasicAuthWithConfig` (middleware/basic_auth.go:92) | basic_auth.go |
| BodyDump | `BodyDump` | `BodyDumpWithConfig` (middleware/body_dump.go:68) | body_dump.go |
| BodyLimit | `BodyLimit` | `BodyLimitWithConfig` (middleware/body_limit.go:42) | body_limit.go |
| Gzip | `Gzip` | `GzipWithConfig` (middleware/compress.go:64) | compress.go |
| ContextTimeout | `ContextTimeout` | `ContextTimeoutWithConfig` (middleware/context_timeout.go:33) | context_timeout.go |
| CSRF | `CSRF` | `CSRFWithConfig` (middleware/csrf.go:121) | csrf.go |
| Decompress | `Decompress` | `DecompressWithConfig` (middleware/decompress.go:60) | decompress.go |
| KeyAuth | `KeyAuth` | `KeyAuthWithConfig` (middleware/key_auth.go:133) | key_auth.go |
| MethodOverride | `MethodOverride` | `MethodOverrideWithConfig` (middleware/method_override.go:41) | method_override.go |
| Proxy | `Proxy` | `ProxyWithConfig` (middleware/proxy.go:300) | proxy.go |
| RateLimiter | — | `RateLimiterWithConfig` (middleware/rate_limiter.go:104) | rate_limiter.go |
| Recover | `Recover` | `RecoverWithConfig` (middleware/recover.go:48) | recover.go |
| HTTPSRedirect | `HTTPSRedirect` | `HTTPSRedirectWithConfig` (middleware/redirect.go:57) | redirect.go |
| WWWRedirect | `WWWRedirect` | `WWWRedirectWithConfig` (middleware/redirect.go:99) | redirect.go |
| NonWWWRedirect | `NonWWWRedirect` | `NonWWWRedirectWithConfig` (middleware/redirect.go:113) | redirect.go |
| HTTPSNonWWWRedirect | — | `HTTPSNonWWWRedirectWithConfig` (middleware/redirect.go:85) | redirect.go |
| HTTPSWWWRedirect | — | `HTTPSWWWRedirectWithConfig` (middleware/redirect.go:71) | redirect.go |
| RequestID | `RequestID` | `RequestIDWithConfig` (middleware/request_id.go:37) | request_id.go |
| RequestLogger | `RequestLogger` | `RequestLoggerWithConfig` (middleware/request_logger.go:237) | request_logger.go |
| Rewrite | `Rewrite` | `RewriteWithConfig` (middleware/rewrite.go:48) | rewrite.go |
| Secure | `Secure` | `SecureWithConfig` (middleware/secure.go:96) | secure.go |
| Static | `Static` | `StaticWithConfig` (middleware/static.go:151) | static.go |
| AddTrailingSlash | `AddTrailingSlash` | `AddTrailingSlashWithConfig` (middleware/slash.go:34) | slash.go |
| RemoveTrailingSlash | `RemoveTrailingSlash` | `RemoveTrailingSlashWithConfig` (middleware/slash.go:98) | slash.go |
| CORS | — | `CORSWithConfig` (middleware/cors.go:140) | cors.go |

Middleware configs also expose a `ToMiddleware` method (e.g. `RequestLoggerConfig.ToMiddleware` at middleware/request_logger.go:246, `BasicAuthConfig` at middleware/basic_auth.go).

### 4. Design Pattern Summary

- The **core package** owns the application struct (`Echo`), routing (`Group`, `DefaultRouter`), request context (`Context`), data binding (`ValueBinder`, `Bind*` functions), error types (`HTTPError`, `BindingError`), response writing, IP extraction, JSON serialization, and interop adapters (`WrapHandler`, `WrapMiddleware`).
- The **middleware package** is purely compositional: each middleware is a self-contained file exposing a convenience function, a `WithConfig` variant, and a config struct. The convenience function always delegates to the `WithConfig` variant, which delegates to an internal `toMiddlewareOrPanic` helper. Middleware is plugged into the core via `Echo.Use` (echo.go:431).
- The `MiddlewareConfigurator` interface (echo.go:121) bridges the two: middleware config structs in the middleware package implement this interface so the core framework can uniformly instantiate them.
