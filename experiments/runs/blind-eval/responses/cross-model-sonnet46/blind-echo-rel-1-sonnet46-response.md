# Cross-Model (Sonnet 4.6): blind-echo-rel-1
Date: 2026-04-16

## Question
What are the main relationships among `Echo`, `Group`, `Context`, and handlers during normal request dispatch?

## Answer

The four components interact through a well-defined ownership hierarchy: **Echo** owns the global registry and lifecycle; **Group** is a prefixed view into that same registry; **Context** carries per-request state produced during dispatch; and **handlers** (`HandlerFunc`) are the leaves that the router ultimately resolves to.

---

### 1. Echo — the framework root and HTTP entry point

> `Echo (echo.go:68-68)` — "Echo is the top-level framework instance." Methods include `AcquireContext, Add, AddRoute, Any, CONNECT, DELETE` [FOCUS, Echo echo.go:68].

`Echo` implements `http.Handler` via `Echo.ServeHTTP (echo.go:695)` [SYM]. Incoming HTTP requests arrive here. Under the hood it delegates to the unexported `serveHTTP (echo.go:700)` [source snippet: `func (e *Echo) serveHTTP(w http.ResponseWriter, r *http.Request)`].

Route registration flows through:
- `Echo.Add (echo.go:642)` — calls the internal `Echo.add (echo.go:621)`. `GUARD(err != nil -> panic(err))` [FOCUS, Echo.Add; source snippet: `func (e *Echo) Add(...) RouteInfo`].
- `Echo.add (echo.go:621)` — `GUARD(e.OnAddRoute != nil -> return RouteInfo{},...)`. Calls `Add` (on the Router). Called by `Add, AddRoute` [FOCUS, Echo.add echo.go:621].
- All per-method shortcuts (`Echo.GET`, `Echo.POST`, `Echo.DELETE`, etc.) delegate to `Echo.Add` [FOCUS entries].

Middleware is attached via:
- `Echo.Use (echo.go:431)` — "adds middleware to the chain which is run after router has found matching route and before route/request handler method is executed." `sig: Echo.Use(middleware ...MiddlewareFunc)` [FOCUS, Echo.Use echo.go:431].

---

### 2. Group — a prefixed, sub-scoped view of Echo's router

> `Group (group.go:14)` — "Group is a set of sub-routes for a specified route prefix." [SYM, Group group.go:14; source snippet: `type Group struct`].

`Group` instances are created by `Echo.Group (echo.go:659)` [FOCUS, Echo.Group; source snippet: `func (e *Echo) Group(prefix string, m ...MiddlewareFunc) (g *Group)`].

All `Group` HTTP-method methods ultimately route through the same `echo.add`:

- `Group.GET (group.go:37)` → `g.Add (group.go:158)` → `g.AddRoute (group.go:172)` → `g.echo.add` [FOCUS, Group.GET; Group.Add; source snippet for Group.AddRoute: `func (g *Group) AddRoute(route Route) (RouteInfo, error)`].
- The same chain applies to `Group.POST, DELETE, PATCH, HEAD, OPTIONS, CONNECT, TRACE, RouteNotFound` — all delegate to `Group.Add` [FOCUS entries, e.g. Group.DELETE group.go:32].
- `Group.Any (group.go:72)` — `DELEGATE(g.Add -> result)` [FOCUS, Group.Any group.go:72].
- `Group.Match (group.go:77)` — `GUARD(len(errs) > 0 -> panic(errs)); ACCUMULATE(AddRoute loop -> errs)` [FOCUS, Group.Match group.go:77].

The key link: `Group.AddRoute (group.go:172)` behavior is `DELEGATE(g.echo.add -> result)` [FOCUS, Group.AddRoute group.go:172]. This means all `Group` route registrations go through the parent `Echo` instance's internal router, not a separate one.

`Group.Use (group.go:22)` attaches group-level middleware [source snippet: `func (g *Group) Use(middleware ...MiddlewareFunc)`].

Groups can nest: `Group.Group (group.go:103)` creates sub-groups [source snippet: `func (g *Group) Group(prefix string, middleware ...MiddlewareFunc) (sg *Group)`].

---

### 3. Context — the per-request envelope passed to handlers

> `Context (context.go:40-40)` — "Context represents the context of the current HTTP request." Methods: `Attachment, Bind, Blob, Cookie, Cookies, Echo` [FOCUS, Context context.go:40].

During dispatch, `Echo` acquires a `Context` from a pool:
> `Echo.AcquireContext (echo.go:684)` — "returns an empty Context instance from the pool." `DELEGATE(e.contextPool.Get -> result)` [FOCUS, Echo.AcquireContext echo.go:684; source snippet: `func (e *Echo) AcquireContext() *Context`].

The Context is bound to the incoming request and response:
> `Context.Reset (context.go:107)` — "Reset resets the context after request completes." `sig: Context.Reset(r *http.Request, w http.ResponseWriter)` [FOCUS, Context.Reset context.go:107].

Route information is then injected by the router:
> `Context.InitializeRoute (context.go:263)` — "InitializeRoute sets the route related variables of this request to the context." Calls `setPathValues` [FOCUS, Context.InitializeRoute context.go:263].

Key context accessors relevant to dispatch:
- `Context.Request (context.go:129)` — "Returns `*http.Request`" [SYM; FOCUS].
- `Context.SetRequest (context.go:134)` — Called by `newContext` [FOCUS, Context.SetRequest context.go:134].
- `Context.Response (context.go:139)` — "Returns `*Response`" [SYM].
- `Context.Echo (context.go:665)` — "Returns the Echo instance" [FOCUS] — Context holds a back-reference to Echo.
- `Context.Bind (context.go:399)` — `DELEGATE(c.echo.Binder.Bind -> result)` [FOCUS] — delegates body/path/query binding back to Echo's configured binder.

After the handler returns, the Context is released back to the pool:
> `Echo.ReleaseContext (echo.go:690)` — "Returns the Context instance back to the pool." [FOCUS, Echo.ReleaseContext; source snippet: `func (e *Echo) ReleaseContext(c *Context)`].

---

### 4. Handlers and Middleware — the leaves of the dispatch tree

Handlers have the type `HandlerFunc`. The router resolves the matching handler from the route tree:
> `DefaultRouter.Route (router.go:791)` — "Route looks up a handler registered for method and path." `PRECEDENCE(cap -> not_r.useEscapedPathForRouting -> currentNode); ACCUMULATE(len loop -> searchIndex)`. Calls `findStaticChild, node, find` [FOCUS, DefaultRouter.Route router.go:791].

Middleware is composed around the matched handler:
> `applyMiddleware (echo.go:785)` — wraps `HandlerFunc` with a chain of `MiddlewareFunc` values [SYM, applyMiddleware echo.go:785; source snippet: `func applyMiddleware(h HandlerFunc, middleware ...MiddlewareFunc) HandlerFunc`].

The `DefaultHTTPErrorHandler (echo.go:374)` intercepts errors returned from handlers [SYM; source snippet: `func DefaultHTTPErrorHandler(exposeError bool) HTTPErrorHandler`].

---

### Dispatch Flow Summary

```
HTTP Request
     │
     ▼
Echo.ServeHTTP (echo.go:695)
  └─ Echo.serveHTTP (echo.go:700)
       ├─ AcquireContext() → Context (from pool)
       ├─ DefaultRouter.Route(Context) → resolves handler + sets RouteInfo/PathValues
       ├─ applyMiddleware(handler, echo.middleware...) → wrapped HandlerFunc
       ├─ wrappedHandler(Context)           ← handler executes here
       └─ ReleaseContext(Context)           ← Context returned to pool
```

- **Echo** ↔ **Router**: Echo delegates route lookup to `DefaultRouter`; `DefaultRouter.Route` populates `Context`.
- **Echo** ↔ **Group**: `Group.AddRoute` delegates to `g.echo.add`; Group is a thin routing-prefix abstraction over the same Echo router.
- **Echo** ↔ **Context**: Echo owns the `contextPool`; it acquires/resets/releases Context per request.
- **Context** ↔ **Handler**: Context is the sole argument to every `HandlerFunc`; it exposes request data, response writing, path values, and back-reference to Echo.
