# v2.3 Response: blind-echo-rel-2
Date: 2026-04-15

## Summary

Echo relates its router, route match types, and middleware ordering through a layered system: `DefaultRouter` performs trie-based route matching with static-child and parameterized-node lookups; routes are registered via `Echo.Add`/`Echo.AddRoute` (which delegate to the internal `Echo.add`); middleware is split into "pre-router" (`Echo.Pre`) and "post-router" (`Echo.Use`) chains; and the `applyMiddleware` function assembles the handler chain at dispatch time. Source snippets confirm that all HTTP verb methods share the same signature pattern, returning `RouteInfo`.

## Detailed Analysis

### 1. Router Architecture

#### 1.1 `Router` Interface and `DefaultRouter` Implementation

- `Router` (router.go:21) — "Router is interface for routing request contexts to registered routes" (implied from FOCUS listing). This is the abstract contract.
- `DefaultRouter` (router.go:60) — "DefaultRouter is the registry of all registered routes for an `Echo` instance for request matching and URL path parameter" with methods: `Add`, `Remove`, `Route`, `Routes`, `insert`, `storeRouteInfo` (FOCUS: DefaultRouter).
- `concurrentRouter.Route` (router_concurrent.go:21) wraps `DefaultRouter.Route` with behavior `DELEGATE(r.router.Route -> result); UNWIND(defer)` (FOCUS: concurrentRouter.Route), adding concurrency safety.

#### 1.2 Route Matching: `DefaultRouter.Route`

- `DefaultRouter.Route` (router.go:791) — "Route looks up a handler registered for method and path" (FOCUS: DefaultRouter.Route).
- Behavior: `PRECEDENCE(cap -> not_r.useEscapedPathForRouting -> currentNode); ACCUMULATE(loop -> searchIndex)` (FOCUS: DefaultRouter.Route). This reveals:
  - **PRECEDENCE**: It first checks capacity/configuration (`cap`), then whether to use escaped path for routing, then starts from `currentNode`.
  - **ACCUMULATE(loop -> searchIndex)**: It iterates through the trie in a loop, advancing a search index.
- Internal trie operations:
  - `node.findStaticChild` (router.go:709) — finds a static child node in the routing trie (SYM: node.findStaticChild).
  - `node.setHandler` (router.go:731) — sets a handler on a trie node (SYM: node.setHandler).

#### 1.3 Route Method Dispatch: `routeMethods`

- `routeMethods` (router.go:148) — internal type with methods: `find`, `isHandler`, `set`, `updateAllowHeader` (FOCUS: routeMethods).
- `routeMethods.find` (router.go:213) — behavior: `GUARD(r -> pass_through); DISPATCH(method)` (FOCUS: routeMethods.find). It dispatches based on the HTTP method string, and is called by `Remove` and `Route` (FOCUS: routeMethods.find, called_by field).
- `routeMethods.set` (router.go:171) — behavior: `DISPATCH(method)`, calls `updateAllowHeader` (FOCUS: routeMethods.set). Called by `setHandler`.
- `routeMethods.updateAllowHeader` (router.go:251) — behavior: `ACCUMULATE(loop -> result)` (FOCUS: routeMethods.updateAllowHeader). Maintains the `Allow` header for OPTIONS responses.

#### 1.4 Route Storage

- `DefaultRouter.storeRouteInfo` (router.go:538) — behavior: `ACCUMULATE(loop -> result)` (FOCUS: DefaultRouter.storeRouteInfo), called by `Add`. Stores route metadata after registration.
- `AddRouteError` (router.go:428) — "error returned by Router.Add containing information what actual route adding failed" with methods `Error`, `Unwrap` (FOCUS: AddRouteError).

### 2. Route Registration

#### 2.1 `Echo.Add` and `Echo.add`

- `Echo.Add` (echo.go:642) — "registers a new route for an HTTP method and path with matching handler in the router with optional route-level middleware" (FOCUS: Echo.Add).
  - Behavior: `GUARD(err -> raise_panic)` — panics on registration errors (FOCUS: Echo.Add).
  - Called by: `Any`, `CONNECT`, `DELETE`, `File`, `GET`, `HEAD`, `OPTIONS`, `PATCH` (FOCUS: Echo.Add, called_by field).
  - Source snippet confirms signature: `func (e *Echo) Add(method, path string, handler HandlerFunc, middleware ...MiddlewareFunc) RouteInfo` (source snippet: Echo.Add, echo.go L642).

- `Echo.add` (echo.go:621) — internal implementation: `func (e *Echo) add(route Route) (RouteInfo, error)` (source snippet: Echo.add, echo.go L621).
- `Echo.AddRoute` (echo.go:617) — `func (e *Echo) AddRoute(route Route) (RouteInfo, error)` delegates to `Echo.add` (source snippet: Echo.AddRoute, echo.go L617; FOCUS: behavior `DELEGATE(e.add -> result)`).

#### 2.2 HTTP Verb Methods — Uniform Pattern

Source snippets confirm all verb methods share the identical signature pattern, returning `RouteInfo`:
- `Echo.GET`: `func (e *Echo) GET(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo` (source snippet: echo.go L449).
- `Echo.DELETE`: `func (e *Echo) DELETE(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo` (source snippet: echo.go L443).
- `Echo.PATCH`: `func (e *Echo) PATCH(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo` (source snippet: echo.go L467).
- `Echo.TRACE`: `func (e *Echo) TRACE(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo` (source snippet: echo.go L485).
- `Echo.POST`: `func (e *Echo) POST(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo` (source snippet: echo.go L473).
- `Echo.PUT`: `func (e *Echo) PUT(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo` (source snippet: echo.go L479).
- `Echo.CONNECT`: `func (e *Echo) CONNECT(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo` (source snippet: echo.go L437).
- `Echo.HEAD`: `func (e *Echo) HEAD(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo` (source snippet: echo.go L455).
- `Echo.OPTIONS`: `func (e *Echo) OPTIONS(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo` (source snippet: echo.go L461).

All delegate to `Echo.Add` with behavior `DELEGATE(e.Add -> result)` (FOCUS entries for each).

#### 2.3 Multi-Method Registration

- `Echo.Match` (echo.go:510) — `func (e *Echo) Match(methods []string, path string, handler HandlerFunc, middleware ...MiddlewareFunc) Routes` (source snippet: echo.go L510). Returns `Routes` (plural), not `RouteInfo`.
  - Behavior: `GUARD(len -> raise_panic); ACCUMULATE(loop -> errs)` (FOCUS: Echo.Match) — panics if no methods, loops over methods to register.
- `Echo.Any` (echo.go:504) — `func (e *Echo) Any(path string, handler HandlerFunc, middleware ...MiddlewareFunc) RouteInfo` (source snippet: echo.go L504). Registers for all supported HTTP methods.

#### 2.4 Special Routes

- `Echo.RouteNotFound` (echo.go:495) — "registers a special-case route which is executed when no other route is found" with `DELEGATE(e.Add -> result)` (FOCUS: Echo.RouteNotFound). Source snippet: `func (e *Echo) RouteNotFound(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo` (echo.go L495).
- `Echo.File` (echo.go:609) — registers a static file route (FOCUS: Echo.File). Source snippet: `func (e *Echo) File(path, file string, middleware ...MiddlewareFunc) RouteInfo` (echo.go L609).
- `Echo.Static` (echo.go:533), `Echo.StaticFS` (echo.go:548), `Echo.FileFS` (echo.go:591) — static file serving variants (source snippets).

#### 2.5 Group Registration

- `Group.AddRoute` (group.go:172) — behavior `DELEGATE(g.echo.add -> result)` (FOCUS: Group.AddRoute) — groups delegate registration to their parent Echo instance.
- `Group.Match` (group.go:77) — same `GUARD`+`ACCUMULATE` pattern as `Echo.Match` (FOCUS: Group.Match).

### 3. Middleware Ordering

#### 3.1 Two Middleware Phases

- **Pre-router middleware**: `Echo.Pre` (echo.go:426) — "adds middleware to the chain which is run **before** router tries to find matching route" (FOCUS: Echo.Pre). Source snippet: `func (e *Echo) Pre(middleware ...MiddlewareFunc)` (echo.go L426).
- **Post-router middleware**: `Echo.Use` (echo.go:431) — "adds middleware to the chain which is run **after** router has found matching route and before route/request handler" (FOCUS: Echo.Use). Source snippet: `func (e *Echo) Use(middleware ...MiddlewareFunc)` (echo.go L431).

This establishes two distinct phases:
1. **Pre-router** (`Pre`): runs before routing — can modify the request path/method before route matching.
2. **Post-router** (`Use`): runs after routing but before the handler — standard middleware position.

#### 3.2 Middleware Access Methods

- `Echo.PreMiddlewares` (echo.go:670) — `func (e *Echo) PreMiddlewares() []MiddlewareFunc` (source snippet: echo.go L670) — returns the pre-router middleware list.
- `Echo.Middlewares` (echo.go:678) — `func (e *Echo) Middlewares() []MiddlewareFunc` (source snippet: echo.go L678) — returns the post-router middleware list.

#### 3.3 Route-Level Middleware

- Every route registration method accepts optional `middleware ...MiddlewareFunc` parameters (confirmed by all source snippets). This allows per-route middleware in addition to global middleware.
- `Group.Use` applies middleware at the group scope (FOCUS: implied from group.go structure).

#### 3.4 `applyMiddleware` — Chain Assembly

- `applyMiddleware` (echo.go:785) — `func applyMiddleware(h HandlerFunc, middleware ...MiddlewareFunc) HandlerFunc` (source snippet: echo.go L785).
  - Behavior: `ACCUMULATE(loop -> result)` (FOCUS: applyMiddleware) — iterates over middleware in reverse to build a nested handler chain.
  - Called by `serveHTTP` (FOCUS: applyMiddleware, called_by: `serveHTTP`).

#### 3.5 Middleware Interop

- `WrapMiddleware` (echo.go:766) — `func WrapMiddleware(m func(http.Handler) http.Handler) MiddlewareFunc` (source snippet: echo.go L766) — adapts standard `http.Handler` middleware to Echo's format.
- `WrapHandler` (echo.go:752) — `func WrapHandler(h http.Handler) HandlerFunc` (source snippet: echo.go L752) — adapts `http.Handler` to Echo's `HandlerFunc`.

### 4. Slash Middleware — Pre-Router Examples

- `AddTrailingSlash` (middleware/slash.go:29) — "returns a root level (before router) middleware which adds a trailing slash to the request `URL#Path`" (FOCUS: AddTrailingSlash). The "root level (before router)" description confirms this is designed for use with `Echo.Pre`.
- `RemoveTrailingSlash` (middleware/slash.go:93) — "returns a root level (before router) middleware which removes a trailing slash from the request URI" (FOCUS: RemoveTrailingSlash). Same pre-router design.

### 5. The `Route` Type

- `Route` (route.go:16) — "contains information to adding/registering new route with the router" with methods `ToRouteInfo`, `WithPrefix` (FOCUS: Route).
- This is the input type for `Echo.AddRoute` and `Echo.add`, while `RouteInfo` is the output type returned after successful registration.

## Dispatch Flow (Synthesized)

1. `Echo.ServeHTTP` → `Echo.serveHTTP` (source snippet: echo.go L695, L700).
2. Pre-router middleware chain runs (`Echo.Pre` middleware).
3. `DefaultRouter.Route` performs trie-based matching with `PRECEDENCE` + `ACCUMULATE(loop)` (FOCUS: DefaultRouter.Route).
4. `routeMethods.find` dispatches based on HTTP method (FOCUS: routeMethods.find).
5. Post-router middleware chain runs (`Echo.Use` middleware).
6. Route-level middleware runs (passed via `Add`/verb methods).
7. `applyMiddleware` assembles the full chain (FOCUS: applyMiddleware).
8. Handler executes with `Context`.

## Uncertainty / Limits

- The source snippets for verb methods are single-line signatures only, so the internal delegation to `Echo.Add` is confirmed by FOCUS behavior annotations, not by visible source code.
- How pre-router middleware, post-router middleware, and route-level middleware are combined within `serveHTTP` is not fully visible — only `applyMiddleware.called_by: serveHTTP` is shown.
- The exact trie structure (how parameterized segments like `:id` or wildcard `*` are handled) is not detailed beyond `node.findStaticChild` and `node.setHandler`.
- 60 of 80 L3 symbols have behavior annotations (GAPS section), providing good but not complete coverage.
