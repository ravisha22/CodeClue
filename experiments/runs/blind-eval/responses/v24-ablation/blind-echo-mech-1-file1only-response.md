# v2.4 Ablation (File 1 Only): blind-echo-mech-1
Date: 2026-04-16

The clue strongly supports that static path segments get an explicit, dedicated lookup during routing: `DefaultRouter.Route` traverses router state and directly calls `findStaticChild`, and `node.findStaticChild` exists specifically to search static children. [DefaultRouter.Route (router.go:791-791); node.findStaticChild (router.go:709-709)]

After path traversal, method resolution is separate. `routeMethods.find` returns the method-specific handler if present, or dispatches with fallback behavior when `fallbackToAny` is enabled. [routeMethods.find (router.go:213-213)]

Registered route methods are stored through `routeMethods.set`, which dispatches by HTTP method and updates the Allow header. That means “which route wins” is not only a path-shape question; method-specific storage and fallback also matter after the path search. [routeMethods.set (router.go:171-171); routeMethods.updateAllowHeader (router.go:251-251)]

If nothing else matches, Echo also has an explicit `RouteNotFound` special-case route. [Echo.RouteNotFound (echo.go:495-495); Group.RouteNotFound (group.go:153-153)]

What I cannot determine exactly from this clue file is the precise ordering between parameter nodes and wildcard nodes when both could match the same remaining path. The clue exposes static-child lookup and generic router traversal (`currentNode`, `searchIndex`, `node`, `find`), but not the internal branch order for parameter vs wildcard children. [DefaultRouter.Route (router.go:791-791); GAPS]
