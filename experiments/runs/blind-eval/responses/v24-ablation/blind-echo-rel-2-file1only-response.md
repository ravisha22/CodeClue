# v2.4 Ablation (File 1 Only): blind-echo-rel-2
Date: 2026-04-16

Echo’s public registration APIs all funnel into the router. `GET`, `POST`, `DELETE`, `PATCH`, `PUT`, `TRACE`, `CONNECT`, `OPTIONS`, `Any`, and `FileFS` delegate to `Add`/`GET`; `Match` accumulates `AddRoute`; `AddRoute` delegates to `e.add`; and `Group.AddRoute` delegates to `g.echo.add`. [Echo.GET (echo.go:449-449); Echo.POST (echo.go:473-473); Echo.DELETE (echo.go:443-443); Echo.Any (echo.go:504-504); Echo.Match (echo.go:510-510); Echo.AddRoute (echo.go:617-617); Group.AddRoute (group.go:172-172); Echo.add (echo.go:621-621)]

The concrete router behind that is `DefaultRouter`, described as the registry of all registered routes for request matching and URL path parameters. It exposes `Add`, `Remove`, `Route`, `Routes`, `insert`, and `storeRouteInfo`. [DefaultRouter (router.go:60-60)]

Runtime matching goes through `DefaultRouter.Route`, which looks up a handler for the current method and path and traverses router state via `findStaticChild`, `node`, and `find`. [DefaultRouter.Route (router.go:791-791)]

Method-specific matching is represented by `routeMethods`: `set` dispatches by method and updates the Allow header, and `find` can either return the method-specific route or, when `fallbackToAny` is enabled, dispatch again to find an `Any` handler. [routeMethods (router.go:148-148); routeMethods.set (router.go:171-171); routeMethods.find (router.go:213-213); routeMethods.updateAllowHeader (router.go:251-251)]

Middleware ordering is explicit: `Pre` runs before the router tries to find a match, while `Use` runs after the router has found the matching route and before the route/request handler chain executes. Groups can introduce group-level middleware and `Group` itself calls `Use`. [Echo.Pre (echo.go:426-426); Echo.Use (echo.go:431-431); Echo.Group (echo.go:659-659)]

`RouteNotFound` is a dedicated special-case route executed when no other route is found, and `concurrentRouter.Route` is just a wrapper that delegates to the underlying router’s `Route`. [Echo.RouteNotFound (echo.go:495-495); Group.RouteNotFound (group.go:153-153); concurrentRouter.Route (router_concurrent.go:21-21)]

What I cannot determine from this clue file: the exact internal route-match-type taxonomy beyond static-child traversal and method/Any dispatch, because the node internals are not exposed here. [DefaultRouter.Route (router.go:791-791); GAPS]
