# v2.3 Response: blind-echo-struct-2
Date: 2026-04-15

## Summary

Echo's routing and request-handling surface comprises several public types: `Echo` (the top-level instance), `Group` (sub-route grouping), `Context` (per-request state and response helpers), `Router`/`DefaultRouter` (route matching), `Route`/`RouteInfo` (route metadata), `HTTPError` (error representation), `Response` (response writer wrapper), plus binding types (`ValueBinder`) and configuration types. These are spread across the core package's root-level Go files.

## Detailed Analysis

### 1. `Echo` — The Top-Level Framework Instance

- `Echo` (echo.go:68) — "Echo is the top-level framework instance" with methods: `AcquireContext`, `Add`, `AddRoute`, `Any`, `CONNECT`, `DELETE` and more (FOCUS: Echo).
- **Route registration methods**: All HTTP verbs delegate to `Echo.Add`:
  - `Echo.Add` (echo.go:642) — "Add registers a new route for an HTTP method and path" (SYM: Echo.Add).
  - `Echo.AddRoute` (echo.go:617) — "AddRoute registers a new Route with default host Router" with behavior `DELEGATE(e.add -> result)` (FOCUS: Echo.AddRoute).
  - `Echo.Any` (echo.go:504) — registers for all HTTP methods, behavior `DELEGATE(e.Add -> result)` (FOCUS: Echo.Any).
  - `Echo.Match` (echo.go:510) — registers for multiple specified methods with behavior `GUARD(len -> raise_panic); ACCUMULATE(loop -> errs)` (implied from struct-2 prompt context).
- **Internal route handling**: `Echo.add` (echo.go:621) with behavior `GUARD(e -> RouteInfo); PRECEDENCE(e -> err -> paramsCount)` — validates and stores route info (FOCUS: Echo.add).
- **Middleware**: `Echo.Use` (echo.go:431) — "adds middleware to the chain which is run after router has found matching route and before route/request handler" (FOCUS: Echo.Use).
- **Context pooling**: `Echo.AcquireContext` (echo.go:684) with behavior `DELEGATE(e.contextPool.Get -> result)`, `Echo.ReleaseContext` (echo.go:690) (FOCUS entries).
- **Factory**: `New` (echo.go:333) creates instance, calling `DefaultHTTPErrorHandler` and `NewDefaultFS` (FOCUS: New). `NewWithConfig` (echo.go:294) creates with configuration, calling `New` (FOCUS: NewWithConfig).
- **Server**: `Echo.Start` (echo.go:744) "stars HTTP server on given address with Echo as a handler" with behavior `DELEGATE(sc.Start -> result); UNWIND(defer)` (FOCUS: Echo.Start).
- **Interop**: `WrapHandler` (echo.go:752) wraps `http.Handler` into `echo.HandlerFunc`, `WrapMiddleware` (echo.go:766) wraps `func(http.Handler) http.Handler` into `echo.MiddlewareFunc` (FOCUS entries).

### 2. `Group` — Sub-Route Grouping

- `Group` (group.go:14) — "Group is a set of sub-routes for a specified route" (SYM: Group).
- **HTTP method shortcuts** — all delegate to `Group.Add`:
  - `Group.GET` (group.go:37) — behavior `DELEGATE(g.Add -> result)` (FOCUS: Group.GET).
  - `Group.DELETE` (group.go:32), `Group.POST` (group.go:57), `Group.PUT` (group.go:62), `Group.PATCH` (group.go:52), `Group.HEAD` (group.go:42), `Group.OPTIONS` (group.go:47), `Group.CONNECT` (group.go:27), `Group.TRACE` (group.go:67) — all `DELEGATE(g.Add -> result)` (FOCUS entries).
- **Route registration**: `Group.Add` (group.go:158) with behavior `GUARD(err -> raise_panic)`, calls `AddRoute` (FOCUS: Group.Add). `Group.AddRoute` (group.go:172) "registers a new Routable with Router" (SYM: Group.AddRoute).
- **Multi-method**: `Group.Any` (group.go:72) — `DELEGATE(g.Add -> result)` (FOCUS: Group.Any). `Group.Match` (group.go:77) — `GUARD(len -> raise_panic); ACCUMULATE(loop -> errs)` (FOCUS: Group.Match).
- **Static files**: `Group.StaticFS` (group.go:122) — `DELEGATE(g.Add -> result)` (FOCUS: Group.StaticFS). `Group.Static` (group.go:112) — `DELEGATE(g.StaticFS -> result)` (FOCUS: Group.Static). `Group.File` (group.go:143), `Group.FileFS` (group.go:135) (FOCUS entries).
- **Middleware**: `Group.Use` (group.go:22) — "implements `Echo#Use()` for sub-routes" (FOCUS: Group.Use).
- **Not-found**: `Group.RouteNotFound` (group.go:153) — `DELEGATE(g.Add -> result)` (FOCUS: Group.RouteNotFound).

### 3. `Context` — Per-Request State

- `Context` (context.go:40) — "represents the context of the current HTTP request" with methods: `Attachment`, `Bind`, `Blob`, `Cookie`, `Cookies`, `Echo` and more (FOCUS: Context).
- **Request/Response access**: `Context.Request` (context.go:129), `Context.SetRequest` (context.go:134), `Context.Response` (context.go:139), `Context.SetResponse` (context.go:145) (FOCUS/SYM entries).
- **Data binding**: `Context.Bind` (context.go:399) with behavior `DELEGATE(c.echo.Binder.Bind -> result)` (FOCUS: Context.Bind).
- **Response rendering**:
  - `Context.String` (context.go:445), `Context.HTMLBlob` (context.go:440), `Context.Blob` (context.go:552), `Context.File` (context.go:571) (SYM entries).
  - `Context.json` (context.go:464) with behavior `DELEGATE(c.echo.JSONSerializer.Serialize -> result)` (FOCUS: Context.json).
  - `Context.xml` (context.go:517) (SYM entry).
- **Cookie access**: `Context.Cookie` (context.go:364) — `DELEGATE(c.request.Cookie -> result)`, `Context.Cookies` (context.go:374) — `DELEGATE(c.request.Cookies -> result)` (FOCUS entries).
- **Query/Form**: `Context.QueryParam` (context.go:287), `Context.FormValue` (context.go:319) (SYM entries).
- **Key-value store**: `Context.Get` (context.go:380), `Context.Set` (context.go:387) (SYM entries).
- **Route initialization**: `Context.InitializeRoute` (context.go:263) "sets the route related variables" calling `setPathValues` (FOCUS: Context.InitializeRoute).
- **Lifecycle**: `Context.Reset` (context.go:107) "resets the context after request completes" (FOCUS: Context.Reset). `Context.Echo` (context.go:665) "returns the `Echo` instance" (FOCUS: Context.Echo).

### 4. `Router` / `DefaultRouter` — Route Matching

- `Router` (router.go:21) — "Router is interface for routing request contexts to registered routes" (FOCUS: Router). This is the abstract interface.
- `DefaultRouter` (router.go:60) — "DefaultRouter is the registry of all registered routes for an `Echo` instance for request matching and URL path parameter" with methods: `Add`, `Remove`, `Route`, `Routes`, `insert`, `storeRouteInfo` (FOCUS: DefaultRouter).
- Internal types for trie-based routing: `node.findStaticChild` (router.go:709), `node.setHandler` (router.go:731) (SYM entries). `routeMethods` (router.go) with `updateAllowHeader` (SYM: routeMethods.updateAllowHeader).
- `AddRouteError` (router.go:428) — error type for route registration failures with methods `Error`, `Unwrap` (INDEX/implied from router.go).

### 5. `Route` / `RouteInfo` — Route Metadata

- Route registration uses `Route` as input and returns `RouteInfo`:
  - `Echo.AddRoute` accepts `Route` and returns `(RouteInfo, error)` (FOCUS: Echo.AddRoute signature).
  - `Echo.Add` returns `RouteInfo` (FOCUS: Echo.Add, called returns implied by delegate chain).
- `NewVirtualHostHandler` (vhost.go:10) "creates instance of Echo that routes requests to given virtual hosts" (FOCUS: NewVirtualHostHandler).

### 6. `HTTPError` — Error Handling

- `HTTPError` (httperror.go:107) — "HTTPError represents an error that occurred while handling a request" with methods: `Error`, `StatusCode`, `Unwrap`, `Wrap` (FOCUS: HTTPError).
- `StatusCode` (httperror.go:45) "returns status code from error if it is HTTPError type" — works as a standalone function too (SYM: StatusCode).
- `DefaultHTTPErrorHandler` (echo.go:374) creates the default handler (SYM: DefaultHTTPErrorHandler).

### 7. `Response` — Response Writer Wrapper

- `Response.WriteHeader` (response.go:49) "WriteHeader sends an HTTP response header with provided status code" (SYM: Response.WriteHeader).
- `Response.Unwrap` (response.go:105) "Unwrap returns the original http.ResponseWriter" (SYM: Response.Unwrap).

### 8. Binding Types

- `ValueBinder` (binder.go) — extensive type with typed binding methods: `int`, `uint`, `float`, `bool`, `time`, `duration`, `unixTime`, `customFunc`, `bindWithDelimiter`, etc. (SYM: numerous ValueBinder.* entries).
- `BindingError` (binder.go) — error type for binding failures (INDEX: binder.go).
- `FormFieldBinder`, `PathValuesBinder` (binder.go) — specialized binders (INDEX: binder.go).
- `bind.go` provides `BindBody`, `BindHeaders`, `BindPathValues`, `BindQueryParams`, `BindUnmarshaler` (INDEX: bind.go).

### 9. Configuration & Interface Types

- `Config` (echo.go) — framework configuration struct (INDEX: echo.go).
- `MiddlewareConfigurator` (echo.go:121) — interface for middleware configuration (FOCUS: MiddlewareConfigurator).
- `RequestIDConfig` (middleware/request_id.go:11) with `ToMiddleware` method (FOCUS: RequestIDConfig).
- `RequestLoggerConfig` (middleware/request_logger.go:124) with `ToMiddleware` method (FOCUS: RequestLoggerConfig).
- `ContextConfig` (echotest/context.go:20) — test configuration (FOCUS: ContextConfig).

### 10. Testing Utilities (`echotest/`)

- `ContextConfig.ToContext` (echotest/context.go:75), `ContextConfig.ToContextRecorder` (echotest/context.go:81), `ServeWithHandler` — test helpers for creating test contexts (FOCUS entries).

## Uncertainty / Limits

- The clue file lists "...and 483 more symbols" and "...and 27 more modules," so additional public types likely exist beyond what is documented.
- The `HandlerFunc` and `MiddlewareFunc` type definitions are referenced throughout but not shown as FOCUS entries — their exact signatures are not visible.
- Interface types like `Renderer` (renderer.go), `JSONSerializer` (implied), and `Validator` are mentioned in INDEX but lack FOCUS detail.
- Only 42 of 80 L3 symbols have behavior annotations (GAPS section).
