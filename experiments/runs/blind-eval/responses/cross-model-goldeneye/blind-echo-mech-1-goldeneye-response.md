# Cross-Model (Goldeneye): blind-echo-mech-1
Date: 2026-04-16

From the provided evidence, Echo resolves overlaps by walking the router tree inside `DefaultRouter.Route(...)`, which has explicit precedence/search-order logic over the current node and calls `findStaticChild(...)` during lookup. [DefaultRouter.Route, router.go:791-791; node.findStaticChild, router.go:709-709]

That means literal/static-path matches are an explicit first-class part of route resolution, rather than being treated the same as every other match type. [DefaultRouter.Route, router.go:791-791; node.findStaticChild, router.go:709-709]

Once the path match is determined, handler selection is method-aware: `routeMethods.find(method, fallbackToAny)` returns the method-specific handler when present and only falls back when `fallbackToAny` allows it. [routeMethods.find, router.go:213-213]

Route registration also tracks parameter count (`paramsCount`) when `Echo.add(...)` inserts a route, which shows that parameterized routes are part of the router’s decision structure. [Echo.add, echo.go:621-621]

If no route wins, Echo exposes an explicit last-resort route-not-found hook via `Echo.RouteNotFound(...)` / `Group.RouteNotFound(...)`. [Echo.RouteNotFound, echo.go:495-495; Group.RouteNotFound, group.go:153-153]

The clues do not expose the full internal branch body for parameter-vs-wildcard ordering, so the strongest supportable conclusion is: Echo’s router explicitly searches static children during traversal, then resolves the matched node’s method handler (with possible `Any` fallback), and falls back to route-not-found behavior only if nothing matches. [DefaultRouter.Route, router.go:791-791; node.findStaticChild, router.go:709-709; routeMethods.find, router.go:213-213]
