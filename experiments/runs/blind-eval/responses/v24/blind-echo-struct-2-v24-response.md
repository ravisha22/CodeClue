# v2.4 Response: blind-echo-struct-2
Date: 2026-04-16

## Question
Which public types and subcomponents make up Echo's routing and request-handling surface?

## Answer

### 1. `Echo` — The Top-Level Framework Instance

The **`Echo`** struct (`Echo`, echo.go:68) is described as "the top-level framework instance." Its public methods that form the routing and request-handling surface include:

- **Route registration**: `Echo.Add` (`Echo.Add`, echo.go:642) is the central route-registration method. HTTP-verb convenience methods — `Echo.GET` (echo.go:449), `Echo.DELETE` (echo.go:443 — listed in GAPS as uncovered but present in SYM), `Echo.HEAD` (echo.go:455 — GAPS), `Echo.Any` (echo.go:504) — all delegate to `Add` with behavior `DELEGATE(e.Add -> result)`.
- **`Echo.AddRoute`** (`Echo.AddRoute`, echo.go:617) registers a `Route` with the default host router, delegating to the private `Echo.add` (`Echo.add`, echo.go:621).
- **`Echo.Match`** (`Echo.Match`, echo.go:510 — listed in GAPS as uncovered) registers a route for multiple HTTP methods via an `ACCUMULATE(AddRoute loop)` pattern.
- **Middleware attachment**: `Echo.Use` (`Echo.Use`, echo.go:431) adds middleware run after routing but before the handler. `Echo.Pre` (echo.go:426 — from struct-1) adds pre-routing middleware.
- **Grouping**: `Echo.Group` (`Echo.Group`, echo.go:659) creates sub-route groups with a prefix, calling `Use` to attach group-level middleware.
- **Instantiation**: `New` (`New`, echo.go:333) creates an Echo instance, calling `DefaultHTTPErrorHandler` and `NewDefaultFS`. `NewWithConfig` (`NewWithConfig`, echo.go:294) creates an instance from a given `Config`.
- **HTTP serving**: `Echo.ServeHTTP` (`Echo.ServeHTTP`, echo.go:695) implements the `http.Handler` interface. `Echo.Start` (`Echo.Start`, echo.go:744) starts the HTTP server.
- **Context management**: `Echo.AcquireContext` (`Echo.AcquireContext`, echo.go:684) gets a context from the pool; `Echo.NewContext` (`Echo.NewContext`, echo.go:357) creates a new one; `Echo.ReleaseContext` (`Echo.ReleaseContext`, echo.go:690) returns it to the pool.
- **Interop**: `WrapHandler` (`WrapHandler`, echo.go:752) wraps `http.Handler` into `echo.HandlerFunc`; `WrapMiddleware` (`WrapMiddleware`, echo.go:766) wraps `func(http.Handler) http.Handler` into `echo.MiddlewareFunc`.

### 2. `Router` Interface and `DefaultRouter`

The **`Router`** interface (`Router`, router.go:21) defines the contract for routing request contexts to registered routes.

**`DefaultRouter`** (`DefaultRouter`, router.go:60) is the concrete implementation, described as "the registry of all registered routes for an `Echo` instance for request matching and URL path parameters." Its public methods include: `Add`, `Remove`, `Route`, `Routes` (plus internal `insert`, `storeRouteInfo`).

A **`concurrentRouter`** variant exists (router_concurrent.go) whose `Route` method delegates to `r.router.Route` with `UNWIND(defer)` — presumably for thread-safety.

### 3. `Group` — Route Grouping

The **`Group`** struct (`Group`, group.go:14) is "a set of sub-routes for a specified route." It mirrors the full Echo routing API:

- HTTP verb methods: `Group.GET` (group.go:37), `Group.DELETE` (group.go:32), `Group.POST` (group.go:57), `Group.PUT` (group.go:62), `Group.PATCH` (group.go:52), `Group.HEAD` (group.go:42), `Group.OPTIONS` (group.go:47), `Group.CONNECT` (group.go:27), `Group.TRACE` (group.go:67) — all with behavior `DELEGATE(g.Add -> result)`.
- `Group.Add` (`Group.Add`, group.go:158) — the central method, with `GUARD(err != nil -> panic(err))`, calling `AddRoute`.
- `Group.AddRoute` (`Group.AddRoute`, group.go:172) — delegates to `g.echo.add`, registering with the parent Echo's router.
- `Group.Any` (`Group.Any`, group.go:72), `Group.Match` (`Group.Match`, group.go:77) — multi-method registration.
- `Group.Use` (`Group.Use`, group.go:22) — group-scoped middleware.
- Static file serving: `Group.Static` (group.go:112), `Group.StaticFS` (group.go:122), `Group.File` (group.go:143), `Group.FileFS` (group.go:135).
- `Group.RouteNotFound` (`Group.RouteNotFound`, group.go:153) — fallback handler.

### 4. `Context` — Per-Request State

The **`Context`** struct (`Context`, context.go:40) "represents the context of the current HTTP request." Key methods:

- **Request/Response access**: `Context.Request` (context.go:129), `Context.SetRequest` (context.go:134), `Context.Response` (context.go:139), `Context.SetResponse` (context.go:145), `Context.Echo` (context.go:665).
- **Data binding**: `Context.Bind` (`Context.Bind`, context.go:399) — delegates to `c.echo.Binder.Bind`.
- **Input extraction**: `Context.QueryParam` (context.go:287), `Context.FormValue` (context.go:319), `Context.Cookie` (context.go:364), `Context.Cookies` (context.go:374).
- **Data storage**: `Context.Get` (context.go:380), `Context.Set` (context.go:387).
- **Response writing**: `Context.String` (context.go:445), `Context.Blob` (context.go:552), `Context.HTMLBlob` (context.go:440), `Context.File` (context.go:571), plus internal helpers `Context.json` (context.go:464), `Context.xml` (context.go:517).
- **Route info**: `Context.InitializeRoute` (`Context.InitializeRoute`, context.go:263) sets route-related variables; `Context.SetPathValues` (`Context.SetPathValues`, context.go:255) sets path parameters with a guard against nil.
- **Lifecycle**: `Context.Reset` (`Context.Reset`, context.go:107) resets the context after request completion.

### 5. `HTTPError` — Error Representation

**`HTTPError`** (`HTTPError`, httperror.go:107) "represents an error that occurred while handling a request." Methods: `Error`, `StatusCode` (httperror.go:115), `Unwrap`, `Wrap` (httperror.go:132). The standalone function `StatusCode` (`StatusCode`, httperror.go:45) extracts status codes from arbitrary errors.

### 6. `Response` — Response Writer Wrapper

**`Response`** (`Response`, response.go:18 — from SYM) wraps `http.ResponseWriter`. Methods include `WriteHeader` (`Response.WriteHeader`, response.go:49), `Unwrap` (`Response.Unwrap`, response.go:105).

### 7. Supporting Types

- **`Config`** (echo.go:237 — INDEX) — framework configuration struct.
- **`MiddlewareConfigurator`** interface (echo.go:121) — defines `ToMiddleware()` for config-to-middleware conversion.
- **`RequestLoggerConfig`** (`RequestLoggerConfig`, middleware/request_logger.go:124) and **`RequestLoggerValues`** (`RequestLoggerValues`, middleware/request_logger.go:189) — middleware-level types.
- **`RequestIDConfig`** (`RequestIDConfig`, middleware/request_id.go:11) — middleware config.
- **`DefaultJSONSerializer`** (`DefaultJSONSerializer.Deserialize`, json.go:24) — JSON deserialization.
- **`NewVirtualHostHandler`** (`NewVirtualHostHandler`, vhost.go:10) — creates an Echo instance routing to virtual hosts.

### 8. Testing Subcomponents (`echotest/`)

- **`ContextConfig`** (`ContextConfig`, echotest/context.go:20) — configuration for test contexts, with methods `ToContext` (echotest/context.go:75), `ToContextRecorder` (echotest/context.go:81), and `ServeWithHandler` (echotest/context.go:167).

### Cannot Be Determined from the Clue File

- The exact struct fields of `Echo`, `Group`, `Context`, `Config`, `Router`, or `DefaultRouter` (only method lists provided).
- The full body logic of `Echo.ServeHTTP` and `Echo.serveHTTP` (uncovered in GAPS).
- The complete `Echo.Match` and `Echo.File` implementations (listed as uncovered).
- The `HandlerFunc` and `MiddlewareFunc` type definitions (referenced but not shown).
- The routing algorithm details inside `DefaultRouter.Route`.
