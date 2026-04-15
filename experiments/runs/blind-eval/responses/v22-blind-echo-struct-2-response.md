# v2.2 Response: blind-echo-struct-2
Date: 2026-04-15

## Question
Which public types and subcomponents make up Echo's routing and request-handling surface?

## Answer

### 1. Top-Level Application Type

**`Echo`** (echo.go:68) — "the top-level framework instance." It exposes methods covering the full routing and request-handling surface: `AcquireContext`, `Add`, `AddRoute`, `Any`, `CONNECT`, `DELETE`, and more.

Key methods on `Echo`:

| Method | Location | Purpose |
|---|---|---|
| `New` | echo.go:333 | Creates an Echo instance; calls `NewDefaultFS`; called by `NewWithConfig`, `main` |
| `NewWithConfig` | echo.go:294 | Creates Echo with given `Config` |
| `Echo.Use` | echo.go:431 | Adds middleware run after route matching, before handler |
| `Echo.Add` | echo.go:642 | Registers a route for HTTP method+path; called by `Any`, `CONNECT`, `DELETE`, `GET`, `HEAD`, `OPTIONS`, `PATCH`, `POST` |
| `Echo.AddRoute` | echo.go:617 | Registers a `Route` with the default host Router |
| `Echo.Any` | echo.go:504 | Registers a route for all HTTP methods |
| `Echo.Match` | echo.go:510 | Registers route for multiple specified HTTP methods |
| `Echo.Start` | echo.go:744 | Starts the HTTP server |
| `Echo.File` | echo.go:609 | Registers route to serve a static file |

### 2. Routing Types

**`Router` interface** (router.go:21) — "interface for routing request contexts to registered routes." This is the abstraction the rest of the framework programs against.

**`DefaultRouter`** (router.go:60) — "the registry of all registered routes for an `Echo` instance for request matching and URL path parameters." Methods: `Add`, `Remove`, `Route`, `Routes`, `insert`, `storeRouteInfo`.

**`Route`** (route.go:16 — from rel-2 clue FOCUS) — contains information for adding/registering a new route. Methods: `ToRouteInfo`, `WithPrefix`.

**`RouteInfo`** (route.go:53 — from mech-1 FOCUS) — contains information about a registered route. Methods: `Clone`, `Reverse`.

**`PathValue`** (router.go:1051) — "tuple of path parameter name and its value in request path."

**`AddRouteError`** (router.go:428) — error returned by `Router.Add` with information about what route addition failed. Methods: `Error`, `Unwrap`.

**`routeMethods`** (router.go:148) — internal type with methods: `find`, `isHandler`, `set`, `updateAllowHeader`.

**`routeMethod`** (router.go:142) — internal type representing a single route method entry.

### 3. Route Grouping

**`Group`** (group.go:14) — "a set of sub-routes for a specified route prefix." It mirrors the `Echo` routing surface:

| Method | Location | Purpose |
|---|---|---|
| `Group.Add` | group.go:158 | Implements `Echo#Add()` for sub-routes; calls `AddRoute`; called by `Any`, `CONNECT`, `DELETE`, `GET`, `HEAD`, `OPTIONS`, `PATCH`, `POST`; raises panic |
| `Group.AddRoute` | group.go:172 | Registers a Routable with Router |
| `Group.GET` | group.go:37 | `Echo#GET()` for sub-routes |
| `Group.Any` | group.go:72 | `Echo#Any()` for sub-routes |
| `Group.Match` | group.go:77 | `Echo#Match()` for sub-routes |
| `Group.StaticFS` | group.go:122 | `Echo#StaticFS()` for sub-routes |
| `Group.Static` | group.go:112 | `Echo#Static()` for sub-routes |
| `Group.File` | group.go:143 | `Echo#File()` for sub-routes |
| `Group.RouteNotFound` | group.go:153 | `Echo#RouteNotFound()` for sub-routes |
| `Group.Use` | group.go:22 — from rel-1 FOCUS | `Echo#Use()` for sub-routes |

All HTTP-method shortcuts (`CONNECT`, `DELETE`, `GET`, `HEAD`, `OPTIONS`, `PATCH`, `POST`, `PUT`, `TRACE`) delegate to `Group.Add` (group.go:158).

### 4. Request Context

**`Context`** (context.go:40) — "represents the context of the current HTTP request." Methods include: `Attachment`, `Bind`, `Blob`, `Cookie`, `Cookies`, `Echo`, and many more across 667 lines.

Key context methods:

| Method | Location | Purpose |
|---|---|---|
| `Context.Request` | context.go:129 | Returns `*http.Request` |
| `Context.SetRequest` | context.go:134 | Sets `*http.Request` |
| `Context.Response` | context.go:139 | Returns `*Response` |
| `Context.Echo` | context.go:665 | Returns the `Echo` instance |
| `Context.Bind` | context.go:399 | Binds path params, query params and body; delegates to `c.echo.Binder.Bind` |
| `Context.Cookie` | context.go:364 | Returns named cookie from request |
| `Context.Cookies` | context.go:374 | Returns all HTTP cookies |
| `Context.Get` | context.go:380 | Retrieves data from context |
| `Context.Set` | context.go:387 | Saves data in context |
| `Context.InitializeRoute` | context.go:263 | Sets route-related variables; calls `PathValues`, `setPathValues` |
| `Context.Reset` | context.go:107 | Resets context after request completes |
| `Context.IsTLS` | context.go:150 | Returns true if HTTP connection is TLS |

**Context pooling:**
- `Echo.AcquireContext` (echo.go:684) — returns an empty `Context` from the pool; delegates to `e.contextPool.Get`.
- `Echo.ReleaseContext` (echo.go:690) — returns `Context` back to the pool.
- `Echo.NewContext` (echo.go:357) — returns a new Context instance; delegates to `newContext`.

### 5. Error Handling Types

**`HTTPError`** (httperror.go:107) — "represents an error that occurred while handling a request." Methods: `Error`, `StatusCode`, `Unwrap`, `Wrap`.

**`HTTPStatusCoder`** (httperror.go:39 — from mech-2 FOCUS) — interface that errors can implement to produce a status code for HTTP response.

**`BindingError`** (binder.go:69) — "represents an error that occurred while binding request data." Method: `Error`.

### 6. Data Binding Types

**`ValueBinder`** (binder.go:92) — "provides utility methods for binding query or path parameter to various Go built-in types." Methods: `BindError`, `BindErrors`, `BindUnmarshaler`, `BindWithDelimiter`, `Bool`, `Bools`, and many type-specific binders (int, uint, float, time, duration, etc.).

### 7. Server & Response Types

**`StartConfig`** (server.go:26) — "for creating configured http.Server instance to start serve http(s) requests." Methods: `Start`, `StartTLS`, `start`.

**`Response`** (response.go:18 — from mech-2 FOCUS) — wraps `http.ResponseWriter`. Methods: `After`, `Before`, `Flush`, `Hijack`, `Unwrap`, `Write`, `WriteHeader`.

### 8. Middleware Configuration Interface

**`MiddlewareConfigurator`** (echo.go:121) — "defines interface for creating middleware handlers with possibility to return configuration error." This is the bridge between middleware config types and the core framework.

Middleware config types that implement this (visible in clue):
- `RequestLoggerConfig` (middleware/request_logger.go:124) — methods: `ToMiddleware`
- `RequestIDConfig` (middleware/request_id.go:11) — methods: `ToMiddleware`
- `AddTrailingSlashConfig` (middleware/slash.go:15) — methods: `ToMiddleware`
- `RemoveTrailingSlashConfig` (middleware/slash.go:80) — methods: `ToMiddleware`

### 9. Testing Subcomponents

**`ContextConfig`** (echotest/context.go:20) — "configuration for creating echo.Context for testing purposes." Methods: `ServeWithHandler`, `ToContext`, `ToContextRecorder`.

### 10. Virtual Hosting

**`NewVirtualHostHandler`** (vhost.go:10) — "creates instance of Echo that routes requests to given virtual hosts." Signature: `NewVirtualHostHandler(vhosts map[string]*Echo)`. Behavior: `GUARD(vh -> result)`.

### 11. Request Logger Values

**`RequestLoggerValues`** (middleware/request_logger.go:189) — "contains extracted values from logger."
