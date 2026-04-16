# Scaffold (Goldeneye): blind-echo-mech-1
Date: 2026-04-16

## Relevant symbols traced
- Route lookup happens in `DefaultRouter.Route`, which calls `findStaticChild`, `node`, and `find`. [DefaultRouter.Route (router.go:791-791)]
- Static-child lookup is explicit via `node.findStaticChild`. [node.findStaticChild (router.go:709-709)]
- Final method selection happens in `routeMethods.find`. [routeMethods.find (router.go:213-213)]
- Route registration for static assets still goes through `Add`/`AddRoute`. [Echo.Static (echo.go:533-533); Echo.StaticFS (echo.go:548-548); Group.StaticFS (group.go:122-122); Echo.Add (echo.go:642-642)]

## Answer
From the provided evidence, Echo decides route winners by walking the router's internal route tree and resolving the most specific visible match in stages:

1. **Matching is centralized in `DefaultRouter.Route()`.** That function is the route-lookup entrypoint for a request, and its behavior summary shows an ordered traversal (`PRECEDENCE(...)`) plus iterative path searching, rather than a flat map lookup. [DefaultRouter.Route (router.go:791-791)]
2. **Static-segment matching is the strongest explicitly visible precedence rule.** `DefaultRouter.Route()` explicitly calls `findStaticChild`, and `node.findStaticChild()` performs a looped child lookup by label, which is direct evidence that static-child matches are checked during lookup. [DefaultRouter.Route (router.go:791-791); node.findStaticChild (router.go:709-709)]
3. **Parameterized paths are part of the same routing process.** `Echo.add()` tracks `paramsCount`, and `Context.InitializeRoute()` / `Context.SetPathValues()` install matched path values into the request context, showing that parameterized routes are resolved through the router and then bound onto the request context. [Echo.add (echo.go:621-621); Context.InitializeRoute (context.go:263-263); Context.SetPathValues (context.go:255-255)]
4. **Once a path node is chosen, HTTP-method resolution is a separate step.** `routeMethods.find()` returns the route if it is already present, otherwise it dispatches by method and can optionally fall back to an “any” route when `fallbackToAny` is enabled. [routeMethods.find (router.go:213-213)]
5. **Static-file helpers do not bypass the routing rules.** `Echo.Static`, `Echo.StaticFS`, and `Group.StaticFS` all delegate into `Add` / `AddRoute`, so static file routes enter the same router and therefore participate in the same precedence mechanism. [Echo.Static (echo.go:533-533); Echo.StaticFS (echo.go:548-548); Group.StaticFS (group.go:122-122); Echo.Add (echo.go:642-642); Group.AddRoute (group.go:172-172)]

## Gaps / uncertainty
What the prompt does **not** expose is the exact tie-break rule between parameter nodes and wildcard nodes after static lookup misses. The router bodies are not shown, and the GAPS section explicitly says body logic is needed for the full mechanistic answer. So the supported conclusion is “static lookup is explicitly first; exact param-vs-wildcard ordering is unresolved from this evidence alone.” [DefaultRouter.Route (router.go:791-791); node.findStaticChild (router.go:709-709); GAPS]
