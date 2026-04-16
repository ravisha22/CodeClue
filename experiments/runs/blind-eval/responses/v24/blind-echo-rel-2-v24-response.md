# v2.4 Response: blind-echo-rel-2
Date: 2026-04-16

## Question
How does Echo relate its router, route match types, and middleware ordering?

## Answer

### 1. The Router Interface and DefaultRouter

Echo defines a **`Router`** interface (`Router`, router.go:21 — listed in GAPS as uncovered, meaning its full definition is not available). The concrete implementation is **`DefaultRouter`** (`DefaultRouter`, router.go:60), described as "the registry of all registered routes for an `Echo` instance for request matching and URL path parameter" extraction. Its public methods are `Add`, `Remove`, `Route`, `Routes`, plus internals `insert` and `storeRouteInfo`.

Echo exposes its router via `Echo.Router()` (`Echo.Router`, echo.go:362, snippet: `func (e *Echo) Router() Router`).

A thread-safe wrapper **`concurrentRouter`** exists, whose `Route` method (`concurrentRouter.Route`, router_concurrent.go:21) delegates to `r.router.Route` with `UNWIND(defer)` — indicating mutex-based locking around route lookups.

### 2. Route Registration Flow

All route registrations converge through a layered delegation chain:

1. **HTTP verb methods** — `Echo.GET` (`Echo.GET`, echo.go:449), `Echo.DELETE` (`Echo.DELETE`, echo.go:443), `Echo.POST` (`Echo.POST`, echo.go:473), `Echo.PUT` (`Echo.PUT`, echo.go:479), `Echo.PATCH` (`Echo.PATCH`, echo.go:467), `Echo.HEAD` (`Echo.HEAD`, echo.go:455), `Echo.TRACE` (`Echo.TRACE`, echo.go:485), `Echo.CONNECT` (`Echo.CONNECT`, echo.go:437), `Echo.OPTIONS` (`Echo.OPTIONS`, echo.go:461) — all have behavior `DELEGATE(e.Add -> result)` and call `Echo.Add`.

2. **`Echo.Add`** (`Echo.Add`, echo.go:642, snippet: `func (e *Echo) Add(method, path string, handler HandlerFunc, middleware ...MiddlewareFunc) RouteInfo`) — the central public method. It has `GUARD(err != nil -> panic(err))` and calls the private `Echo.add`. Its `called_by` list confirms it's used by `Any`, `CONNECT`, `DELETE`, `File`, `GET`, `HEAD`, `OPTIONS`, `PATCH`.

3. **`Echo.add`** (`Echo.add`, echo.go:621, snippet: `func (e *Echo) add(route Route) (RouteInfo, error)`) — the private core. Behavior: `GUARD(e.OnAddRoute != nil -> return RouteInfo{},...)` allows an intercept hook; then `PRECEDENCE(e -> err -> paramsCount)`. It calls the router's `Add` method to register the route.

4. **Multi-method registration**: `Echo.Any` (`Echo.Any`, echo.go:504) registers for all HTTP methods by delegating to `Add`. `Echo.Match` (`Echo.Match`, echo.go:510, snippet: `func (e *Echo) Match(methods []string, path string, handler HandlerFunc, middleware ...MiddlewareFunc) Routes`) loops through methods calling `AddRoute` with `ACCUMULATE(AddRoute loop -> errs)` and panics if errors accumulate.

5. **`Echo.AddRoute`** (`Echo.AddRoute`, echo.go:617, snippet: `func (e *Echo) AddRoute(route Route) (RouteInfo, error)`) delegates to `e.add`.

### 3. Route Types

The **`Route`** struct (`Route`, route.go:16, snippet: `type Route struct`) contains information for adding/registering new routes. It has methods `ToRouteInfo` and `WithPrefix` (`Route.WithPrefix`, route.go:40, snippet: `func (r Route) WithPrefix(pathPrefix string, middlewares []MiddlewareFunc) Route`) — note that `WithPrefix` takes a path prefix *and* middlewares, showing that group-level middleware is baked into the route at registration time.

**`RouteInfo`** (`RouteInfo`, route.go:53) is the result of registration, with methods `Clone` (route.go:65) and `Reverse` (`RouteInfo.Reverse`, route.go:75) for URL generation. `Reverse` uses `ACCUMULATE(Fprintf loop -> result)` to substitute path parameters.

**`Routes`** (a collection type) provides query/filter capabilities: `FindByMethodPath` (route.go:127), `FilterByMethod` (route.go:141), `FilterByPath` (route.go:159), `FilterByName` (route.go:177), `Reverse` (`Routes.Reverse`, route.go:117), and `Clone` (route.go:108).

**`AddRouteError`** (`AddRouteError`, router.go:428) is returned when route registration fails, with `Error` and `Unwrap` methods.

### 4. Route Matching Mechanism

`DefaultRouter.Route` (`DefaultRouter.Route`, router.go:791) is the lookup function. Its behavior annotation reveals the matching strategy:
- `PRECEDENCE(cap -> not_r.useEscapedPathForRouting -> currentNode)` — a precedence-based evaluation.
- `ACCUMULATE(len loop -> searchIndex)` — iterative traversal.
- Calls `findStaticChild`, `node`, `find` — indicating a **trie-based router** where static children are checked first.

**`node.findStaticChild`** (`node.findStaticChild`, router.go:709) searches among static child nodes with `ACCUMULATE(loop -> result)`.

**`routeMethods`** (`routeMethods`, router.go:148) stores per-node method handlers with methods `find`, `isHandler`, `set`, `updateAllowHeader`.
- **`routeMethods.find`** (`routeMethods.find`, router.go:213) has `GUARD(r != nil || !fallbackToAny -> return r); DISPATCH(method)` — it dispatches by HTTP method and falls back to an "any" handler if no method-specific one is found.
- **`routeMethods.set`** (`routeMethods.set`, router.go:171) dispatches by method and calls `updateAllowHeader` to maintain the `Allow` header.
- **`routeMethods.updateAllowHeader`** (`routeMethods.updateAllowHeader`, router.go:251) accumulates method names via `WriteString loop`.

**`node.setHandler`** (`node.setHandler`, router.go:731) sets the handler on a trie node, calling `routeMethods.set`.

A **`RouteNotFound`** special-case route (`Echo.RouteNotFound`, echo.go:495) is executed when no other route matches.

### 5. Middleware Ordering

Echo provides **three distinct middleware attachment points** with a clear ordering:

1. **Pre-routing middleware** — `Echo.Pre` (`Echo.Pre`, echo.go:426, snippet: `func (e *Echo) Pre(middleware ...MiddlewareFunc)`) adds middleware "run before router tries to find matching route." Accessible via `Echo.PreMiddlewares()` (`Echo.PreMiddlewares`, echo.go:670).

2. **Post-routing / global middleware** — `Echo.Use` (`Echo.Use`, echo.go:431, snippet: `func (e *Echo) Use(middleware ...MiddlewareFunc)`) adds middleware "run after router has found matching route and before route/request handler." Accessible via `Echo.Middlewares()` (`Echo.Middlewares`, echo.go:678).

3. **Route-level middleware** — every registration method accepts optional `...MiddlewareFunc` (e.g., `Echo.GET` signature: `func (e *Echo) GET(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo`).

**`applyMiddleware`** (`applyMiddleware`, echo.go:785, snippet: `func applyMiddleware(h HandlerFunc, middleware ...MiddlewareFunc) HandlerFunc`) chains middleware around the handler. Its behavior `ACCUMULATE(loop -> result)` indicates it iterates the middleware slice (likely in reverse) to wrap the handler, building an onion-layer chain.

**Group-level middleware**: `Route.WithPrefix` (`Route.WithPrefix`, route.go:40) takes `middlewares []MiddlewareFunc`, suggesting group middleware is prepended to the route's middleware when a group registers routes.

### 6. Group and Router Relationship

`Group.AddRoute` (`Group.AddRoute`, group.go:172) has behavior `DELEGATE(g.echo.add -> result)` — confirming that Group does not maintain a separate router; all routes are registered in the parent Echo's `DefaultRouter`.

### 7. Static File Routes

Static routes are just regular routes registered through the same `Add` mechanism:
- `Echo.Static` (`Echo.Static`, echo.go:533) calls `Add`, `MustSubFS`, and `StaticDirectoryHandler`.
- `Echo.StaticFS` (`Echo.StaticFS`, echo.go:548) calls `Add` and `StaticDirectoryHandler`.
- `Echo.File` (`Echo.File`, echo.go:609) calls `Add` directly.
- `Echo.FileFS` (`Echo.FileFS`, echo.go:591) delegates via `Echo.GET`.

### Cannot Be Determined from the Clue File

- The exact body logic of `DefaultRouter.Route` — how it traverses the trie and the precise priority order among static segments, parameter segments, and wildcards (only the high-level behavior annotation is available).
- The full `Router` interface definition (listed as uncovered in GAPS).
- The `RouterConfig` type (listed as uncovered in GAPS).
- How pre-middleware, post-middleware, and route-level middleware are combined in `Echo.serveHTTP` (the snippet shows only the function signature: `func (e *Echo) serveHTTP(w http.ResponseWriter, r *http.Request)`).
- The exact order of `SecureConfig.ToMiddleware` and `RateLimiterConfig.ToMiddleware` (GAPS uncovered).
