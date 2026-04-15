# v2.2 Response: blind-echo-rel-2
Date: 2026-04-15

## Question
How does Echo relate its router, route match types, and middleware ordering?

## Answer

### 1. Router Architecture

**`Router` interface** (router.go:21 — from struct-2 FOCUS) — the abstraction for routing request contexts to registered routes.

**`DefaultRouter`** (router.go:60) — "the registry of all registered routes for an `Echo` instance for request matching and URL path parameters." Methods: `Add`, `Remove`, `Route`, `Routes`, `insert`, `storeRouteInfo`.

**`concurrentRouter`** (router_concurrent.go:16, source snippet) — a wrapper struct that provides thread-safe access. Its `Route` method (router_concurrent.go:21) has behavior `DELEGATE(r.router.Route -> result); UNWIND(defer)`, meaning it delegates to the underlying `DefaultRouter.Route` while holding a lock (the `UNWIND(defer)` suggests deferred unlock).

- `NewConcurrentRouter` (router_concurrent.go:9, source snippet): `func NewConcurrentRouter(r Router) Router` — wraps any Router in a concurrent-safe wrapper.
- `concurrentRouter.Add` (router_concurrent.go:35): `func (r *concurrentRouter) Add(routable Route) (RouteInfo, error)` — thread-safe route addition.
- `concurrentRouter.Remove` (router_concurrent.go:42): `func (r *concurrentRouter) Remove(method string, path string) error` — thread-safe route removal.
- `concurrentRouter.Routes` (router_concurrent.go:28): `func (r *concurrentRouter) Routes() Routes` — thread-safe route listing.

**`Echo.Router`** (echo.go:362, source snippet): `func (e *Echo) Router() Router` — returns the default router.

### 2. Route Registration Chain

The route registration flows through a well-defined chain:

1. **HTTP method shortcuts** (`Echo.GET`, `Echo.POST`, `Echo.DELETE`, etc.) — all delegate to `Echo.Add`.
   - `Echo.GET` (echo.go:449): behavior `DELEGATE(e.Add -> result)`, calls `Add`. Source snippet confirms: `func (e *Echo) GET(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo`.
   - Same pattern for `Echo.DELETE` (echo.go:443), `Echo.HEAD` (echo.go:455), `Echo.PATCH` (echo.go:467), `Echo.POST` (echo.go:473), `Echo.PUT` (echo.go:479), `Echo.TRACE` (echo.go:485), `Echo.CONNECT` (echo.go:437).

2. **`Echo.Add`** (echo.go:642): "registers a new route for an HTTP method and path with matching handler in the router with optional route-level middleware." Called by all HTTP method shortcuts. Calls `add`. Raises `panic`.

3. **`Echo.add`** (echo.go:621): private implementation. Behavior: `GUARD(e -> RouteInfo); PRECEDENCE(e -> err)`. Calls `AddRoute`. Called by `Add` and `AddRoute`.

4. **`Echo.AddRoute`** (echo.go:617): "registers a new Route with default host Router." Behavior: `DELEGATE(e.add -> result)`. Calls `add`. Called by `Match` and `add`.

5. **`Echo.Any`** (echo.go:504): "registers a new route for all HTTP methods." Behavior: `DELEGATE(e.Add -> result)`. Calls `Add`.

6. **`Echo.Match`** (echo.go:510): "registers a new route for multiple HTTP methods." Behavior: `ACCUMULATE(loop -> errs)`. Calls `AddRoute`. Source snippet: `func (e *Echo) Match(methods []string, path string, handler HandlerFunc, middleware ...MiddlewareFunc) Routes`.

### 3. Route Types and Data Structures

**`Route`** (route.go:16) — "contains information to adding/registering new route with the router." Methods: `ToRouteInfo`, `WithPrefix`.

**`RouteInfo`** (route.go:53 — from FOCUS in mech-1 clue) — "contains information about registered Route." Methods: `Clone`, `Reverse`.

**`routeMethods`** (router.go:148) — internal type. Methods: `find`, `isHandler`, `set`, `updateAllowHeader`.
- `routeMethods.set` (router.go:171) — behavior: `DISPATCH(method)` — dispatches based on HTTP method. Called by `setHandler`.
- `routeMethods.isHandler` (router.go:301) — called by `setHandler`.

**`routeMethod`** (router.go:142) — internal type for a single method's route data.

**`AddRouteError`** (router.go:428) — error returned when `Router.Add` fails. Methods: `Error`, `Unwrap`. Called by `Add`.

**`DefaultRouter.storeRouteInfo`** (router.go:538) — behavior: `GUARD(ri -> result); ACCUMULATE(loop -> result)`. Stores route info in the router's registry.

### 4. Route Matching at Request Time

**`DefaultRouter.Route`** (router.go:791) — "looks up a handler registered for method and path." Behavior: `GUARD(child -> result); PRECEDENCE(cap -> not_r.useEscapedPathForRouting -> previous); ACCUMULATE(loop -> result)`.

This behavior annotation reveals:
- **GUARD**: checks child nodes in the routing tree.
- **PRECEDENCE**: the matching considers capacity (`cap`), whether escaped path routing is used (`not_r.useEscapedPathForRouting`), and previous matches — suggesting a priority-based matching strategy.
- **ACCUMULATE(loop)**: iterates through path segments to find the match.

### 5. Special Route Types

**`Echo.RouteNotFound`** (echo.go:495) — "registers a special-case route which is executed when no other route is found." Behavior: `DELEGATE(e.Add -> result)`. Calls `Add`.

**`Group.RouteNotFound`** (group.go:153) — the Group equivalent. Behavior: `DELEGATE(g.Add -> result)`.

**Static file routes:**
- `Echo.Static` (echo.go:533) — "registers a new route with path prefix to serve static files from the provided root directory." Calls `Add`, `MustSubFS`, `StaticDirectoryHandler`.
- `Echo.StaticFS` (echo.go:548) — registers route for an `fs.FS` filesystem. Calls `Add`, `StaticDirectoryHandler`.
- `Echo.File` (echo.go:609) — registers route to serve a single static file.
- `StaticDirectoryHandler` (echo.go:559) — creates handler for directory serving. Behavior: `PRECEDENCE(not_disablePathUnescaping -> err)`.
- `StaticFileHandler` (echo.go:599) — creates handler for single file serving. Calls `File`. Called by `FileFS`.

### 6. Middleware Ordering

The clue reveals two distinct middleware insertion points with different ordering:

**Pre-router middleware:**
- **`Echo.Pre`** (echo.go:426) — "adds middleware to the chain which is run **before** router tries to find matching route." Source snippet: `func (e *Echo) Pre(middleware ...MiddlewareFunc)`.
- `Echo.PreMiddlewares` (echo.go:670, source snippet) — returns pre-router middleware list.

**Post-router middleware:**
- **`Echo.Use`** (echo.go:431) — "adds middleware to the chain which is run **after** router has found matching route and **before** route/request handler method is called." Source snippet: `func (e *Echo) Use(middleware ...MiddlewareFunc)`.
- `Echo.Middlewares` (echo.go:678, source snippet) — returns post-router middleware list.

**Route-level middleware:**
- Every route registration method accepts optional `...MiddlewareFunc` parameters (e.g., `Echo.GET` signature: `func (e *Echo) GET(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo`). These are route-specific middleware.

**Middleware application:**
- **`applyMiddleware`** (echo.go:785, source snippet): `func applyMiddleware(h HandlerFunc, middleware ...MiddlewareFunc) HandlerFunc`. Behavior: `ACCUMULATE(loop -> result)`. Called by `serveHTTP`. This wraps the handler with each middleware in sequence.

- **`WrapMiddleware`** (echo.go:766) — wraps `func(http.Handler) http.Handler` into `echo.MiddlewareFunc`. Behavior: `ACCUMULATE(loop -> result)`.

**Group-level middleware:**
- `Echo.Group` (echo.go:659) — "creates a new router group with prefix and optional group-level middleware." Calls `Use`.
- `Group.Use` (group.go:22, source snippet): `func (g *Group) Use(middleware ...MiddlewareFunc)`.

**Slash-manipulation middleware (pre-router):**
- `AddTrailingSlash` (middleware/slash.go:29) — "returns a root level (**before router**) middleware which adds a trailing slash to the request `URL#Path`."
- `RemoveTrailingSlash` (middleware/slash.go:93) — "returns a root level (**before router**) middleware which removes a trailing slash from the request URI."

### 7. Middleware Execution Order Summary

Based on the clue evidence, the execution order during request dispatch is:

1. **Pre-router middleware** (registered via `Echo.Pre`) — runs before route matching.
2. **Route matching** — `DefaultRouter.Route` (router.go:791) finds the matching handler.
3. **Post-router middleware** (registered via `Echo.Use`) — runs after matching, before handler.
4. **Route-level middleware** — passed directly to route registration methods.
5. **Handler execution** — the matched `HandlerFunc` runs with the `Context`.

The `applyMiddleware` function (echo.go:785) accumulates middleware in a loop, wrapping the handler to form the final chain. The `serveHTTP` method calls `applyMiddleware` to compose the full chain.

### 8. Uncertainties

- The exact internal structure of how `DefaultRouter.Route` (router.go:791) traverses its tree (radix tree, trie, etc.) is not fully determinable from the clue — only the behavior annotation `GUARD/PRECEDENCE/ACCUMULATE` is available.
- The precise interaction between route-level middleware and post-router middleware ordering (whether route-level is innermost or outermost relative to `Use` middleware) cannot be fully confirmed from the clue alone, though the wrapping pattern in `applyMiddleware` suggests route-level middleware is innermost (closest to handler).
