# Response: blind-echo-mech-1 (with drill-down)
Date: 2026-04-15

## Answer
From the provided clues, I can say **Echo uses a router-owned matching system that stores route metadata and method-specific handler state, but the exact winner rule among static segments, parameters, and wildcards is not explicitly exposed in the supplied material.**

What the prompt does support:
- Route registration flows through `Echo.Add` / `Echo.AddRoute` into router registration, and `DefaultRouter.Add` is the component that actually registers a route for a method/path. (Echo.Add, `echo.go:642-642`; Echo.AddRoute, `echo.go:617-617`; DefaultRouter.Add, `router.go:447-447`)
- `DefaultRouter` is the registry used for request matching, and it stores route information through `storeRouteInfo`. (DefaultRouter, `router.go:60-60`; DefaultRouter.storeRouteInfo, `router.go:538-538`)
- Matching appears to be method-aware as well as path-aware, because `routeMethods` has `find`, `isHandler`, `set`, and `updateAllowHeader`, and `routeMethods.isHandler` participates in handler setup. (routeMethods, `router.go:148-148`; routeMethods.isHandler, `router.go:301-301`; routeMethods.set, `router.go:171-171`)
- Once a route is selected, the chosen `RouteInfo` and `PathValues` are written into the request `Context` by `Context.InitializeRoute`. (Context.InitializeRoute, `context.go:263-263`; RouteInfo, `route.go:53-53`)
- Static-file helpers (`Static`, `StaticFS`, `File`, `FileFS`) are not special out-of-band systems; they still register routes through `Add` or `GET`. (Echo.Static, `echo.go:533-533`; Echo.StaticFS, `echo.go:548-548`; Echo.File, `echo.go:609-609`; Echo.FileFS, `echo.go:591-591`; Group.StaticFS, `group.go:122-122`)

## What I cannot determine
- I **cannot determine the exact precedence rule** among static segments, named/path parameters, and wildcards from the supplied clue file and snippets. No provided entry states an ordering such as "static beats param" or "param beats wildcard," and the drill-down for `routeMethods.isHandler` contains only the signature, not the body. (routeMethods.isHandler source snippet, `router.go L301-301`; DefaultRouter, `router.go:60-60`)
- I also cannot determine whether overlap resolution happens during trie descent, backtracking, or some other router algorithm, because the relevant router bodies (`Route`, `find`, `insert`) are not shown. (DefaultRouter, `router.go:60-60`; routeMethods, `router.go:148-148`; concurrentRouter.Route, `router_concurrent.go:21-21`)
- I cannot determine whether method-specific states (for example, `405`/allow-header behavior) affect the path winner in overlapping cases; the clues only show that `routeMethods` tracks method handlers and allow-header updates. (routeMethods, `router.go:148-148`; routeMethods.set, `router.go:171-171`)

So the safest evidence-based conclusion is: **Echo definitely centralizes overlap resolution inside the router, produces a winning `RouteInfo` plus `PathValues`, and tracks handlers per method, but the provided material does not reveal the actual precedence order between static, parameter, and wildcard matches.** (DefaultRouter, `router.go:60-60`; Context.InitializeRoute, `context.go:263-263`; routeMethods, `router.go:148-148`)
