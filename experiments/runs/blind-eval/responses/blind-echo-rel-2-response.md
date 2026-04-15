# Response: blind-echo-rel-2
Date: 2026-04-15

## Answer
The provided material ties together **route registration**, **router-owned match state**, and **three middleware layers/orderings**.

- `Echo` owns route registration through helpers like `GET`, `DELETE`, `POST`, `PUT`, `PATCH`, `TRACE`, `Any`, `Match`, `File`, and `Static`; these methods all feed into `Add` or `AddRoute`. (Echo.GET, `echo.go:449-449`; Echo.DELETE, `echo.go:443-443`; Echo.POST, `echo.go:473-473`; Echo.PUT, `echo.go:479-479`; Echo.PATCH, `echo.go:467-467`; Echo.TRACE, `echo.go:485-485`; Echo.Any, `echo.go:504-504`; Echo.Match, `echo.go:510-510`; Echo.File, `echo.go:609-609`; Echo.Static, `echo.go:533-533`; Echo.Add, `echo.go:642-642`; Echo.AddRoute, `echo.go:617-617`)
- The router side is represented by `DefaultRouter`, which is the registry of all registered routes for an `Echo` instance and exposes `Add`, `Remove`, `Route`, `Routes`, `insert`, and `storeRouteInfo`. That means route matching and route lookup live in the router layer, not in the individual route helper methods. (DefaultRouter, `router.go:60-60`; DefaultRouter.storeRouteInfo, `router.go:538-538`)
- Registered routes are represented by `Route` when being added and `RouteInfo` once stored/exposed. `Route` contains information for registering a route; `RouteInfo` contains information about a registered route. (Route, `route.go:16-16`; RouteInfo, `route.go:53-53`)
- The match result is pushed into request state through `Context.InitializeRoute`, which sets route-related variables and path values on the `Context`, and `Context.RouteInfo()` exposes the matched route info later. (Context.InitializeRoute, `context.go:263-263`; Context.RouteInfo source snippet, `context.go L225-225`; Context.SetPathValues source snippet, `context.go L255-255`)
- There is also method-specific route state inside `routeMethods`; the clues show `routeMethods` has `find`, `isHandler`, `set`, and `updateAllowHeader`, and `routeMethods.isHandler` is called by `setHandler`. That indicates the router tracks method-level handler presence as part of matching/registration. (routeMethods, `router.go:148-148`; routeMethods.isHandler, `router.go:301-301`; routeMethods.set, `router.go:171-171`)

### Middleware ordering
- `Echo.Pre` is the earliest layer: it runs **before** the router tries to find a matching route. (Echo.Pre, `echo.go:426-426`)
- `Echo.Use` is the next framework-level layer: it runs **after** the router has found the matching route and **before** the route/request handler method executes. (Echo.Use, `echo.go:431-431`)
- Route registration methods also take optional route-level middleware (`middleware ...MiddlewareFunc` in `Add`, `GET`, `Any`, etc.), so there is a route-specific middleware layer in addition to `Pre` and `Use`. (Echo.Add, `echo.go:642-642`; Echo.GET, `echo.go:449-449`; Echo.Any, `echo.go:504-504`)
- The slash middlewares reinforce the ordering distinction: `AddTrailingSlash` and `RemoveTrailingSlash` are explicitly root-level middlewares that run before router matching. (AddTrailingSlash, `middleware/slash.go:29-29`; RemoveTrailingSlash, `middleware/slash.go:93-93`)
- `WrapMiddleware` shows Echo can adapt standard `func(http.Handler) http.Handler` middleware into its own `MiddlewareFunc`, so middleware ordering is part of the core framework orchestration. (WrapMiddleware, `echo.go:766-766`)

## What I cannot determine
- I cannot determine the exact list of "route match types" (for example, concrete categories or enums) from the provided material. The prompt shows router structures and route metadata, but not a taxonomy of match kinds.
- I cannot determine the precise execution order between `Use` middleware and route-level middleware beyond the fact that `Use` is after routing and route methods accept route-level middleware; the exact nesting/composition is not shown. (Echo.Use, `echo.go:431-431`; Echo.Add, `echo.go:642-642`; applyMiddleware source snippet not provided in this prompt)
- I cannot determine the detailed path-matching precedence rules (for example, static vs parameter vs wildcard) from this prompt alone; that is not described here. (DefaultRouter, `router.go:60-60`; routeMethods.isHandler, `router.go:301-301`)
