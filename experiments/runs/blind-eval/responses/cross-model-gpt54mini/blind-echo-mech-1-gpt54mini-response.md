# Cross-Model (GPT-5.4-mini): blind-echo-mech-1
Date: 2026-04-16

- The only explicit lookup order shown is that `DefaultRouter.Route` calls `findStaticChild`, and `node.findStaticChild` is the lookup helper used by `Route`/`findChildWithLabel`. (DefaultRouter.Route (router.go:791-791); node.findStaticChild (router.go:709-709))
- So the clues directly show a static-child lookup in the route-matching path, but they do not show the full param-vs-wildcard tie-break order. (DefaultRouter.Route (router.go:791-791); node.findStaticChild (router.go:709-709))
- The clues also show route registration and static-route helpers (`Echo.Add`, `Echo.AddRoute`, `Echo.Static`, `Echo.StaticFS`, `Echo.File`), which are part of the routing surface but not the missing precedence logic. (Echo.Add (echo.go:642-642); Echo.AddRoute (echo.go:617-617); Echo.Static (echo.go:533-533); Echo.StaticFS (echo.go:548-548); Echo.File (echo.go:609-609))
