# v2.4 Ablation (File 1 Only): blind-fiber-1
Date: 2026-04-16

If middleware wants Fiber to route again, the explicit API is `DefaultCtx.RestartRouting`, whose documented role is to “restart routing instead of going to the next handler.” [DefaultCtx.RestartRouting (ctx.go:265-266)]

The main request path re-enters `App.requestHandler`, which calls `next` and `nextCustom`; that makes the reroute a full dispatch pass, not just a continuation of the current middleware chain. [App.requestHandler (router.go:315-315)]

Normal matching then depends on the usual route matcher: `Route.match` is called by `next` / `nextCustom`, and route-pattern parsing ultimately uses `routeParser.getMatch`, which walks the path, applies constraints, and can reject the match. [Route.match (router.go:68-68); routeParser.getMatch (path.go:507-507)]

A successful reroute is externally observable through `DefaultCtx.Matched`, which reports whether the current request path was matched by the router. [DefaultCtx.Matched (ctx.go:375-376)]

What I cannot determine from this clue file is the exact branch that turns an unmatched reroute into a 404 versus a 405. The prompt itself points at `App.next` / `App.nextCustom` as uncovered, and those are precisely the routines that `requestHandler` delegates to for dispatch. [App.requestHandler (router.go:315-315); GAPS]
