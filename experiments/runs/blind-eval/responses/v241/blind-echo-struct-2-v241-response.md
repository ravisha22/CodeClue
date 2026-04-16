# v2.4.1 Response: blind-echo-struct-2
Date: 2026-04-16

## Public Types and Subcomponents of Echo's Routing and Request-Handling Surface

### Top-Level Framework Type

**`Echo`** (`echo.go:68`) is the top-level framework instance [FOCUS: Echo]. It is created via `New` (`echo.go:333`, calls `DefaultHTTPErrorHandler` and `NewDefaultFS`) or `NewWithConfig` (`echo.go:294`, calls `New`) [FOCUS: New, NewWithConfig]. It exposes route registration, middleware attachment, context management, and server lifecycle.

### Routing Types

1. **`Router`** (`router.go:21`) – an interface for routing request contexts to registered routes [FOCUS: Router].
2. **`DefaultRouter`** (`router.go:60`) – the concrete registry of all registered routes for an `Echo` instance, responsible for request matching and URL path parameter extraction. Methods: `Add`, `Remove`, `Route`, `Routes`, `insert`, `storeRouteInfo` [FOCUS: DefaultRouter].
3. **`Route`** – referenced throughout as the data object passed to `Echo.AddRoute` (`echo.go:617`) and `Group.AddRoute` (`group.go:172`). `Echo.add` (`echo.go:621`) accepts a `Route` and calls `DefaultRouter.Add` [FOCUS: Echo.add, Echo.AddRoute].
4. **`RouteInfo`** – the return type of registration methods (e.g., `Echo.Add` returns `RouteInfo` per snippet `func (e *Echo) Add(...) RouteInfo`). Used by `Context.RouteInfo` to retrieve current request route information [FOCUS: Context.Bind — mentions RouteInfo; SYM: Echo.Add].
5. **`Group`** (`group.go:14`) – "a set of sub-routes for a specified route" [SYM: Group, group.go:14]. Created by `Echo.Group` (`echo.go:659`, calls `Use`). It mirrors every `Echo` route-registration method for sub-routes:
   - HTTP method shortcuts: `GET` (`group.go:37`), `POST` (`group.go:57`), `PUT` (`group.go:62`), `DELETE` (`group.go:32`), `HEAD` (`group.go:42`), `PATCH` (`group.go:52`), `OPTIONS` (`group.go:47`), `CONNECT` (`group.go:27`), `TRACE` (`group.go:67`) – all DELEGATE to `g.Add` [FOCUS entries for each].
   - `Add` (`group.go:158`) – GUARD(err != nil -> panic(err)), calls `AddRoute` [FOCUS: Group.Add].
   - `AddRoute` (`group.go:172`) – DELEGATE(g.echo.add), called_by `Add` and `Match` [FOCUS: Group.AddRoute].
   - `Any` (`group.go:72`), `Match` (`group.go:77`) – for bulk registration [FOCUS: Group.Any, Group.Match].
   - `StaticFS` (`group.go:122`), `Static` (`group.go:112`), `File` (`group.go:143`), `FileFS` (`group.go:135`), `RouteNotFound` (`group.go:153`) [FOCUS entries for each].
   - `Use` (`group.go:22`) – attaches group-level middleware [snippet: Group.Use].
   - Nested groups via `Group.Group` (`group.go:103`) [snippet].

### Route Registration on Echo

`Echo` provides the same HTTP-method shortcuts: `GET` (`echo.go:449`), `POST` (`echo.go:473`), `PUT` (`echo.go:479`), `DELETE` (`echo.go:443`), `HEAD` (`echo.go:455`), `PATCH` (`echo.go:467`), `TRACE` (`echo.go:485`), `CONNECT` implied by `Echo.Any` [FOCUS entries]. All DELEGATE to `Echo.Add` (`echo.go:642`) which calls `Echo.add` (`echo.go:621`) [FOCUS: Echo.Add, Echo.add]. Additional registration: `Any` (`echo.go:504`), `Match` (`echo.go:510`), `RouteNotFound` (`echo.go:495`), `AddRoute` (`echo.go:617`) [FOCUS entries].

Static file serving: `Echo.File` (`echo.go:609`), `Echo.FileFS` via `GET` + `StaticFileHandler` [FOCUS: not in struct-2 but referenced via Group.StaticFS].

### Request-Handling Types

1. **`Context`** (`context.go:40`) – "represents the context of the current HTTP request" with methods: `Attachment`, `Bind`, `Blob`, `Cookie`, `Cookies`, `Echo`, and many more [FOCUS: Context]. Key methods:
   - `Bind` (`context.go:399`) – DELEGATE(c.echo.Binder.Bind) [FOCUS: Context.Bind].
   - `Cookie`/`Cookies` (`context.go:364`/`374`) – DELEGATE to `c.request.Cookie`/`c.request.Cookies` [FOCUS].
   - `Request` (`context.go:129`), `SetRequest` (`context.go:134`), `Echo` (`context.go:665`) [FOCUS entries].
2. **`Response`** (`response.go`) – wraps `http.ResponseWriter`; methods include `WriteHeader` (`response.go:49`), `Unwrap` (`response.go:105`). Accessible via `Context.Response` (`context.go:139`) [SYM entries].
3. **`HTTPError`** (`httperror.go:107`) – "represents an error that occurred while handling a request", with methods `Error`, `StatusCode`, `Unwrap`, `Wrap` [FOCUS: HTTPError]. The standalone `StatusCode` function (`httperror.go:45`) extracts status codes from errors [SYM: StatusCode].
4. **`DefaultJSONSerializer`** – implements `Deserialize` (`json.go:24`) to decode request bodies [FOCUS: DefaultJSONSerializer.Deserialize].

### Middleware Infrastructure

- `Echo.Use` (`echo.go:431`) – attaches middleware run after route matching [FOCUS: Echo.Use].
- `Echo.Pre` (`echo.go:426`) – attaches middleware run before route matching [FOCUS: Echo.Pre] (in struct-2 this is not in FOCUS but referenced via struct-1; it is in the SYM section of the shared clue).
- `WrapMiddleware` (`echo.go:766`) and `WrapHandler` (`echo.go:752`) bridge standard `http.Handler` types [FOCUS: WrapMiddleware, WrapHandler].
- `MiddlewareConfigurator` (`echo.go:121`) – interface for config-to-middleware conversion [referenced in INDEX top symbols].

### Testing Support

- `ContextConfig` (`echotest/context.go:20`) – configuration for creating `echo.Context` for testing. Methods: `ServeWithHandler`, `ToContext` (`echotest/context.go:75`), `ToContextRecorder` (`echotest/context.go:81`) [FOCUS entries for each].

### Middleware-Package Types (middleware/)

The middleware package (24 files) provides pluggable behaviors, each with a config struct and `ToMiddleware` method [TREE; INDEX]. Examples in FOCUS: `RequestLoggerConfig` (`middleware/request_logger.go:124`), `RequestIDConfig` (`middleware/request_id.go:11`), `RequestLoggerValues` (`middleware/request_logger.go:189`). Convenience constructors like `RequestLogger` (`middleware/request_logger.go:395`) and `RequestID` (`middleware/request_id.go:30`) wrap the config pattern [FOCUS entries].

### What Cannot Be Determined

- The **full list of `Echo` methods** is truncated ("methods: AcquireContext, Add, AddRoute, Any, CONNECT, DELETE" with implicit continuation) [FOCUS: Echo].
- The **full list of `Context` methods** is similarly truncated ("methods: Attachment, Bind, Blob, Cookie, Cookies, Echo") [FOCUS: Context].
- **Internal router node types** (e.g., `node`, `routeMethods`) are mentioned in SYM but not in FOCUS for this task, so their role in the public surface is unclear [SYM: node.findStaticChild, routeMethods.updateAllowHeader].
- The **483 additional symbols** and **27 additional modules** are not enumerated [SYM/INDEX truncation markers].
- `Echo.Match` and `Echo.DELETE`/`Echo.File`/`Echo.HEAD` are listed as uncovered in GAPS, so their full behavior annotations are not available [GAPS section].
- The relationship between `NewVirtualHostHandler` (`vhost.go:10`) and the main routing surface is described only as creating an Echo instance for virtual hosts [FOCUS: NewVirtualHostHandler].
- Whether `HandlerFunc` and `MiddlewareFunc` are type aliases or distinct types is not detailed in the clue.
