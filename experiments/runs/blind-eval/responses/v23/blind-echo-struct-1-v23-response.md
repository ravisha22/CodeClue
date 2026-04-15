# v2.3 Response: blind-echo-struct-1
Date: 2026-04-15

## Summary

Echo's public API is split into two distinct packages: a **core framework package** (root-level `.go` files) providing the application instance, routing, context, binding, response writing, error handling, and server lifecycle; and a **middleware package** (`middleware/`) providing a large catalog of reusable middleware components, each following a consistent `XxxWithConfig` + `ToMiddleware` pattern.

## Detailed Analysis

### 1. Core Framework Package — Root-Level Files

The core package consists of approximately 15 Go source files at the repository root:

#### 1.1 `echo.go` (865L) — Framework Instance & Routing

- **`Echo`** (echo.go:68) — "Echo is the top-level framework instance" with methods: `AcquireContext`, `Add`, `AddRoute`, `Any`, `CONNECT`, `DELETE` and more (FOCUS: Echo).
- **`New`** (echo.go:333) — "New creates an instance of Echo" calling `DefaultHTTPErrorHandler` and `NewDefaultFS` (FOCUS: New).
- **`Echo.Use`** (echo.go:431) — "Use adds middleware to the chain which is run after router has found matching route and before route/request handler" (FOCUS: Echo.Use).
- **`Echo.ServeHTTP`** (echo.go:695) — "ServeHTTP implements `http.Handler` interface" (SYM: Echo.ServeHTTP).
- **`WrapMiddleware`** (echo.go:766) — "WrapMiddleware wraps `func(http.Handler) http.Handler` into `echo.MiddlewareFunc`" (FOCUS: WrapMiddleware).
- **`MiddlewareConfigurator`** (echo.go:121) — "defines interface for creating middleware handlers with possibility to return configuration error" (FOCUS: MiddlewareConfigurator).
- **`applyMiddleware`** (echo.go:785) — internal middleware chain assembly with behavior `ACCUMULATE(loop -> result)` (FOCUS: applyMiddleware).
- **`DefaultHTTPErrorHandler`** (echo.go:374) — "creates new default HTTP error handler" (SYM: DefaultHTTPErrorHandler).
- **`Config`** (echo.go, INDEX entry) — framework configuration type.

#### 1.2 `context.go` (667L) — Request Context

- **`Context`** (context.go:40) — "represents the context of the current HTTP request" with methods: `Attachment`, `Bind`, `Blob`, `Cookie`, `Cookies`, `Echo` and more (SYM/INDEX: Context).
- Response helpers: `Context.Blob` (context.go:552), `Context.String` (context.go:445), `Context.HTMLBlob` (context.go:440), `Context.File` (context.go:571), `Context.json` (context.go:464), `Context.xml` (context.go:517) (SYM entries).
- Request accessors: `Context.Request` (context.go:129), `Context.SetRequest` (context.go:134), `Context.Response` (context.go:139), `Context.QueryParam` (context.go:287), `Context.FormValue` (context.go:319) (SYM entries).
- Data store: `Context.Get` (context.go:380) "retrieves data from the context", `Context.Set` (context.go:387) "saves data in the context" (SYM entries).

#### 1.3 `group.go` (178L) — Route Grouping

- **`Group`** (group.go:14) — "Group is a set of sub-routes for a specified route" (SYM: Group).
- HTTP method shortcuts: `Group.GET` (group.go:37), `Group.Add` (group.go:158), `Group.AddRoute` (group.go:172), `Group.StaticFS` (group.go:122), `Group.Any` (group.go:72) (SYM entries).

#### 1.4 `router.go` (1074L) — Route Matching

- **`DefaultRouter`** (router.go:60) — "DefaultRouter is the registry of all registered routes for an `Echo` instance for request matching and URL path parameter" with methods: `Add`, `Remove`, `Route`, `Routes`, `insert`, `storeRouteInfo` (FOCUS: DefaultRouter).
- Internal types: `routeMethods` (router.go), `node` types for trie-based matching (SYM: node.findStaticChild, node.setHandler).

#### 1.5 `binder.go` (1329L) & `bind.go` (472L) — Request Binding

- **`ValueBinder`** — extensive type with methods for binding typed values: `int`, `uint`, `float`, `bool`, `time`, `duration`, `unixTime`, `customFunc`, etc. (SYM: numerous ValueBinder.* entries).
- `bind.go` provides `BindBody`, `BindHeaders`, `BindPathValues`, `BindQueryParams`, `BindUnmarshaler` (INDEX: bind.go).
- `bindData` (bind.go:139) "will bind data ONLY fields in destination" (SYM: bindData).

#### 1.6 `response.go` — Response Writer

- `Response.WriteHeader` (response.go:49) "WriteHeader sends an HTTP response header" (SYM: Response.WriteHeader).
- `Response.Unwrap` (response.go:105) "Unwrap returns the original http.ResponseWriter" (SYM: Response.Unwrap).

#### 1.7 `httperror.go` (162L) — Error Handling

- `HTTPError` (httperror.go) with methods `Error`, `StatusCode`, `Unwrap`, `Wrap` (INDEX: httperror.go).
- `StatusCode` (httperror.go:45) "returns status code from error if it is HTTPError type" (SYM: StatusCode).

#### 1.8 `server.go` (202L) — Server Lifecycle

- `Start`, `StartTLS`, `StartConfig` (INDEX: server.go).
- `gracefulShutdown` (server.go:183) — internal shutdown handler (SYM: gracefulShutdown).

#### 1.9 Other Core Files

- `route.go` — Route definition type (INDEX reference).
- `ip.go`, `json.go`, `renderer.go` — utility types (TREE listing).
- `binder_generic.go` (571L), `context_generic.go` (43L) — generic type support (TREE listing).

### 2. Middleware Package — `middleware/`

The `middleware/` directory contains **24 files** (TREE listing), each providing one or more middleware components:

#### 2.1 Consistent Pattern: `XxxWithConfig` + `ToMiddleware`

Every middleware follows the same pattern:
- A convenience function (e.g., `Gzip`, `CSRF`, `BasicAuth`) that delegates to a `WithConfig` variant.
- A `WithConfig` function that accepts a config struct and delegates to `toMiddlewareOrPanic` with behavior `DELEGATE(toMiddlewareOrPanic -> result)`.
- A `ToMiddleware` method on the config struct that performs the actual middleware creation.

Evidence from FOCUS entries:
- `GzipWithConfig` (middleware/compress.go:64) — `DELEGATE(toMiddlewareOrPanic -> result)`, called_by: `Gzip` (FOCUS: GzipWithConfig).
- `CSRFWithConfig` (middleware/csrf.go:121) — same pattern, called_by: `CSRF` (FOCUS: CSRFWithConfig).
- `BasicAuthWithConfig` (middleware/basic_auth.go:92) — same pattern, called_by: `BasicAuth` (FOCUS: BasicAuthWithConfig).
- `CORSWithConfig` (middleware/cors.go:140) — same pattern (FOCUS: CORSWithConfig).
- `RecoverWithConfig` (middleware/recover.go:48) — same pattern (FOCUS: RecoverWithConfig).
- `StaticWithConfig` (middleware/static.go:151) — same pattern (FOCUS: StaticWithConfig).

#### 2.2 Middleware Catalog

From the FOCUS and SYM entries, the middleware package includes:
- **Compression**: `Gzip`/`GzipWithConfig` (middleware/compress.go), `Decompress`/`DecompressWithConfig` (middleware/decompress.go) (FOCUS entries).
- **Security**: `CSRF`/`CSRFWithConfig` (middleware/csrf.go), `BasicAuth`/`BasicAuthWithConfig` (middleware/basic_auth.go), `KeyAuth`/`KeyAuthWithConfig` (middleware/key_auth.go), `Secure`/`SecureWithConfig` (middleware/secure.go) (FOCUS entries).
- **CORS**: `CORS`/`CORSWithConfig` (middleware/cors.go) (FOCUS: CORSWithConfig).
- **Body handling**: `BodyDump`/`BodyDumpWithConfig` (middleware/body_dump.go), `BodyLimit`/`BodyLimitWithConfig` (middleware/body_limit.go) (FOCUS entries).
- **Logging**: `RequestLogger`/`RequestLoggerWithConfig` (middleware/request_logger.go) — this one uses `GUARD(err -> raise_panic)` and then `ToMiddleware` (FOCUS: RequestLoggerWithConfig).
- **Recovery**: `Recover`/`RecoverWithConfig` (middleware/recover.go) (FOCUS: RecoverWithConfig).
- **Proxying**: `Proxy`/`ProxyWithConfig` (middleware/proxy.go) with `NewRandomBalancer`, `NewRoundRobinBalancer` (INDEX: middleware/proxy.go).
- **URL manipulation**: `AddTrailingSlash`/`AddTrailingSlashWithConfig`, `RemoveTrailingSlash`/`RemoveTrailingSlashWithConfig` (middleware/slash.go) (FOCUS entries).
- **Redirects**: `HTTPSRedirect`, `HTTPSNonWWWRedirect`, `HTTPSWWWRedirect`, `NonWWWRedirect`, `WWWRedirect` — all with `WithConfig` variants (middleware/redirect.go) (FOCUS entries).
- **Timeouts**: `ContextTimeout`/`ContextTimeoutWithConfig` (middleware/context_timeout.go) (FOCUS: ContextTimeoutWithConfig).
- **Request ID**: `RequestID`/`RequestIDWithConfig` (middleware/request_id.go) (FOCUS entries).
- **Method Override**: `MethodOverride`/`MethodOverrideWithConfig` (middleware/method_override.go) (FOCUS: MethodOverrideWithConfig).
- **Rewriting**: `Rewrite`/`RewriteWithConfig` (middleware/rewrite.go) (FOCUS: RewriteWithConfig).
- **Static files**: `Static`/`StaticWithConfig` (middleware/static.go) (FOCUS: StaticWithConfig).
- **Rate limiting**: `RateLimiterMemoryStore` (middleware/rate_limiter.go) (SYM entry).

### 3. Test Utilities — `echotest/`

- `echotest/` contains 2 files (TREE listing): `context.go` and `reader.go`.
- `ContextConfig` (echotest/context.go:20) provides test helpers: `ServeWithHandler`, `ToContext`, `ToContextRecorder` (INDEX/SYM entries).
- `LoadBytes`, `TrimNewlineEnd` (echotest/reader.go) — test data utilities (INDEX: echotest/reader.go).

## Uncertainty / Limits

- The clue file lists "...and 27 more modules" and "...and 483 more symbols," so additional core types and middleware may exist beyond what is documented.
- The internal architecture of individual middleware (e.g., how rate limiting stores state) is not detailed in L3 focus entries.
- Whether middleware is in the same Go module or a separate importable package cannot be confirmed from the clue file alone, though the directory structure suggests it is a sub-package.
