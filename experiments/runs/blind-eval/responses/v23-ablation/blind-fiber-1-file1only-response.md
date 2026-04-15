# v2.3 Ablation (File 1 Only): blind-fiber-1
Date: 2026-04-15

File 1 does not expose the exact “restart routing” API, but it does show the pieces that determine what a re-dispatch would do after middleware rewrites the path.

- The actual route lookup engine is `DefaultRouter.Route(c *Context)`, which “looks up a handler registered for method and path.” Its behavior uses precedence and an accumulating search, and it calls `findStaticChild`, `node`, and `find`. So any “match again” step has to run the normal router lookup against the current context path. (clue: `DefaultRouter.Route (router.go:791-791)`, `node.findStaticChild (router.go:709-709)`)
- Middleware can change the effective path visible to routing because `DefaultCtx.Path(override ...string)` takes an optional override and returns the request path. That is the clearest File-1 hook showing that middleware can rewrite the path Fiber will use. (clue: `DefaultCtx.Path (ctx.go:297-297)`)
- After routing, Fiber exposes whether the request matched through `DefaultCtx.Matched()`, which delegates to `getMatched`. So a re-dispatch can be observed as either matched or not matched on the context. (clue: `DefaultCtx.Matched (ctx.go:375-376)`)
- Method resolution is handled separately from path-tree traversal. `routeMethods.find(method string, fallbackToAny bool)` dispatches by method, and `routeMethods` also owns `updateAllowHeader`, which is called from `set`. That is strong evidence that once a path node is found, Fiber distinguishes “matching path but wrong method” from “no route at all,” and prepares Allow-header information for the former case. (clue: `routeMethods.find (router.go:213-213)`, `routeMethods.updateAllowHeader (router.go:251-251)`, `routeMethods.set (router.go:171-171)`)
- Based on those pieces, the best File-1-only reading is:
  1. middleware rewrites the path via the context path override surface, (clue: `DefaultCtx.Path (ctx.go:297-297)`)
  2. Fiber re-runs normal router lookup through `DefaultRouter.Route`, (clue: `DefaultRouter.Route (router.go:791-791)`)
  3. if `routeMethods.find` finds a handler for the current method (or a fallback such as “any”), the request becomes a normal matched route, (clue: `routeMethods.find (router.go:213-213)`, `DefaultCtx.Matched (ctx.go:375-376)`)
  4. if the path structure matches but the method-specific dispatch fails while Allow data exists, the result is the 405-style case, (clue: `routeMethods.find (router.go:213-213)`, `routeMethods.updateAllowHeader (router.go:251-251)`)
  5. and if no path/handler is found at all, the request remains unmatched, which is the 404-style case. (clue: `DefaultCtx.Matched (ctx.go:375-376)`, `DefaultRouter.Route (router.go:791-791)`)
- Middleware routes themselves are prefix-driven via `App.Use` / `Group.Use`, so path-rewriting middleware can sit in front of final route selection. But File 1 still does not reveal the exact public method Fiber uses to “restart” dispatch after a rewrite, only the underlying matching pieces that govern the outcome. (clue: `App.Use (app.go:860-860)`, `Group.Use (group.go:70-70)`, `DefaultRouter.Route (router.go:791-791)`)
