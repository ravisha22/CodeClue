# v2.4 Response: blind-echo-rel-1
Date: 2026-04-16

## Question
What are the main relationships among `Echo`, `Group`, `Context`, and handlers during normal request dispatch?

## Answer

### 1. Echo Owns and Creates Groups

`Echo` is the top-level framework instance (`Echo`, echo.go:68). It creates `Group` instances via `Echo.Group(prefix string, m ...MiddlewareFunc)` (`Echo.Group`, echo.go:659), which immediately calls `Use` to attach any group-level middleware (`Echo.Group` calls: `Use`). The `Group` struct (`Group`, group.go:14) is "a set of sub-routes for a specified route" — it does not exist independently but is always associated with an `Echo` instance.

### 2. Group Delegates Route Registration Back to Echo

Every `Group` route-registration method ultimately delegates back to `Echo`'s internal route registration:

- HTTP-verb methods like `Group.GET` (`Group.GET`, group.go:37), `Group.POST` (`Group.POST`, group.go:57), `Group.DELETE` (`Group.DELETE`, group.go:32), etc. all have behavior `DELEGATE(g.Add -> result)` and call `Group.Add`.
- `Group.Add` (`Group.Add`, group.go:158, signature: `func (g *Group) Add(method, path string, handler HandlerFunc, middleware ...MiddlewareFunc) RouteInfo`) calls `Group.AddRoute`.
- `Group.AddRoute` (`Group.AddRoute`, group.go:172, signature: `func (g *Group) AddRoute(route Route) (RouteInfo, error)`) has behavior `DELEGATE(g.echo.add -> result)` — it delegates directly to the parent Echo's private `add` method.

This means `Group` is purely a convenience layer that prefixes paths and prepends middleware, but all routes are ultimately registered in the `Echo` instance's router.

### 3. Echo Manages the Context Lifecycle

`Echo` manages `Context` objects through a pool pattern:

- `Echo.AcquireContext` (`Echo.AcquireContext`, echo.go:684) retrieves an empty `Context` from the pool via `DELEGATE(e.contextPool.Get -> result)`.
- `Echo.NewContext` (`Echo.NewContext`, echo.go:357, signature: `func (e *Echo) NewContext(r *http.Request, w http.ResponseWriter) *Context`) creates a new Context, delegating to `newContext` (`newContext`, context.go:75).
- `Echo.ReleaseContext` (`Echo.ReleaseContext`, echo.go:690) returns the `Context` back to the pool.
- `Context.Reset` (`Context.Reset`, context.go:107) resets the context after request completion, taking a new `http.Request` and `http.ResponseWriter`.

### 4. Context Holds a Back-Reference to Echo

`Context.Echo` (`Context.Echo`, context.go:665) returns the `Echo` instance, establishing a bidirectional relationship. This allows handlers to access framework-level features through the context.

### 5. Context is the Handler's Primary Interface

Handlers receive a `Context` to interact with the request/response cycle:

- **Input access**: `Context.Request` (`Context.Request`, context.go:129) returns `*http.Request`; `Context.QueryParam` (`Context.QueryParam`, context.go:287), `Context.FormValue` (`Context.FormValue`, context.go:319), `Context.Cookie` (`Context.Cookie`, context.go:364).
- **Data binding**: `Context.Bind` (`Context.Bind`, context.go:399) delegates to `c.echo.Binder.Bind` — the binder is owned by the `Echo` instance, but invoked through the Context.
- **Response writing**: `Context.String` (`Context.String`, context.go:445), `Context.Blob` (`Context.Blob`, context.go:552), `Context.HTMLBlob` (`Context.HTMLBlob`, context.go:440), `Context.File` (`Context.File`, context.go:571).
- **JSON serialization**: `Context.json` (`Context.json`, context.go:464) delegates to `c.echo.JSONSerializer.Serialize` — again using the Echo instance's serializer through the context.
- **Per-request storage**: `Context.Get` (`Context.Get`, context.go:380) and `Context.Set` (`Context.Set`, context.go:387).
- **Response object**: `Context.Response` (`Context.Response`, context.go:139) and `Context.SetResponse` (`Context.SetResponse`, context.go:145).

### 6. Route Initialization Flows Through Context

When a route is matched, `Context.InitializeRoute` (`Context.InitializeRoute`, context.go:263) sets route-related variables by calling `setPathValues` (`Context.setPathValues`, context.go:269). `Context.SetPathValues` (`Context.SetPathValues`, context.go:255) has a `GUARD(pathValues == nil -> panic)` safety check.

### 7. Request Dispatch Flow

Based on the clue entries, the normal request dispatch follows this sequence:

1. **`Echo.ServeHTTP`** (`Echo.ServeHTTP`, echo.go:695) implements `http.Handler` — this is the HTTP entry point.
2. The `DefaultRouter.Route` method (referenced from rel-2 clue) performs route matching.
3. **`applyMiddleware`** (`applyMiddleware`, echo.go:785) wraps the matched handler with middleware, called by `serveHTTP`. Its behavior is `ACCUMULATE(loop -> result)`, iterating middleware in reverse to build a chain.
4. The handler (a `HandlerFunc`) is invoked with the `Context`.

### 8. Middleware Attachment Points

There are three levels at which middleware can be attached:

- **Pre-routing**: `Echo.Pre` (`Echo.Pre`, echo.go:426 — from rel-2 clue) adds middleware run before the router.
- **Post-routing / global**: `Echo.Use` (`Echo.Use`, echo.go:431) adds middleware run after routing, before the handler. Called by `Group` and `main`.
- **Route-level**: every route-registration method accepts optional `...MiddlewareFunc` parameters (e.g., `Echo.GET` signature: `func (e *Echo) GET(path string, h HandlerFunc, m ...MiddlewareFunc)`).
- **Group-level**: `Group.Use` (`Group.Use`, group.go:22) attaches middleware scoped to the group.

### 9. Handler Signature and the main Example

The `main` function (`main`, echo.go:24) demonstrates the typical usage: it calls `New`, then `GET`, then `Start` and `Use` — confirming that `Echo` is created, routes and middleware are registered on it, and then the server is started.

The `hello` handler (from source snippet, echo.go:20) has signature `func hello(c *echo.Context) error`, confirming handlers take a `*Context` and return `error`.

### 10. Virtual Hosting

`NewVirtualHostHandler` (`NewVirtualHostHandler`, vhost.go:10) creates an Echo instance that routes to virtual hosts based on `map[string]*Echo`, showing that multiple `Echo` instances can coexist.

### 11. Context Timeout Middleware

`ContextTimeout` (`ContextTimeout`, middleware/context_timeout.go:28) wraps the dispatch with a timeout, delegating to `ContextTimeoutWithConfig` — demonstrating how middleware interacts with the Context during dispatch.

### Cannot Be Determined from the Clue File

- The exact body logic of `Echo.ServeHTTP` and `Echo.serveHTTP` (not in FOCUS or snippets for this task).
- How the router match result is passed to `applyMiddleware` and the handler.
- The exact mechanism by which `Group` middleware is merged with route-level and global middleware during dispatch.
- The `HandlerFunc` and `MiddlewareFunc` type definitions.
- Whether `Context` is an interface or a concrete struct (the clue shows method receivers on `Context` as a struct type and the `hello` snippet uses `*echo.Context`).
