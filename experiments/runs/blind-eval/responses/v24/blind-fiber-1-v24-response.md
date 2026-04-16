# v2.4 Response: blind-fiber-1
Date: 2026-04-16

## Question
If middleware rewrites the request path and wants Fiber to match routes again, how does the framework restart dispatch and decide whether the request becomes a normal match, a 404, or a 405?

## Answer

### Restarting Dispatch via RestartRouting

Fiber provides a mechanism for middleware to restart the routing dispatch after rewriting the request path. The `DefaultCtx.RestartRouting` method (`DefaultCtx.RestartRouting`, ctx.go:265-266) is the entry point for this. Its behavior annotation shows `GUARD(c.handlerCtx != nil -> return err)`, indicating it checks for an existing handler context before proceeding. When a middleware modifies the path (e.g., via `DefaultCtx.Path`, ctx.go:297, which accepts an `override ...string` parameter), calling `RestartRouting` causes the framework to re-enter the dispatch loop rather than continuing to the next handler in the current chain.

### The Request Handler Entry Point

The top-level dispatch function is `App.requestHandler` (`App.requestHandler`, router.go:315). Its behavior is `GUARD(d, isDefault := ctx.(*DefaultCtx); isDefault -> return); PRECEDENCE(d -> err); UNWIND(defer)`. It calls either `next` or `nextCustom` to walk the route stack (`App.requestHandler` calls: `next`, `nextCustom`).

### Route Matching: Normal Match, 404, or 405

The matching loop is implemented in `App.next` (`App.next`, router.go:115) and `App.nextCustom` (`App.nextCustom`, router.go:216). Both share the same behavioral pattern: `PRECEDENCE(not_ok -> c -> exists); ACCUMULATE(match loop -> result)`. This indicates an accumulation loop that iterates over registered routes, calling the `Route.match` method for each.

`Route.match` (`Route.match`, router.go:68) has the signature `Route.match(detectionPath, path string, params *[maxParams]string)` and behavior `GUARD(r.root && len(detectionPath) == 1 && detectio... -> return true); PRECEDENCE(r -> len)`. It is called by both `next` and `nextCustom`. For a root route, if the detection path has length 1 (i.e., "/"), it returns `true` immediately. Otherwise, it applies the route's pattern against the detection path.

Under the hood, pattern matching uses `routeParser.getMatch` (`routeParser.getMatch`, path.go:507) which has behavior `GUARD(detectionPath != "" -> return false); ACCUMULATE(len loop -> result)` and calls `CheckConstraint`, `findParamLen`, and `hasPartialMatchBoundary` (path.go:486) to determine partial-match boundaries.

The `PRECEDENCE(not_ok -> c -> exists)` pattern in `next`/`nextCustom` suggests the following decision flow:
1. **Normal match**: If `Route.match` returns true for a route whose HTTP method matches the request method, the corresponding handler is invoked — a normal match.
2. **405 (Method Not Allowed)**: The `not_ok -> c -> exists` precedence suggests that if a path matches but the method does not, the framework can distinguish this case (the path "exists" but is "not_ok" for the current method), resulting in a 405 response.
3. **404 (Not Found)**: If no route's pattern matches the detection path at all, the loop exhausts without finding a match, resulting in a 404.

### Path Normalization

Before matching, the path may be normalized. `App.normalizePath` (`App.normalizePath`, router.go:398) is available for path normalization. The `RoutePatternMatch` function (`RoutePatternMatch`, path.go:155) also calls `RemoveEscapeCharBytes` (`RemoveEscapeCharBytes`, path.go:659), `parseRoute` (`parseRoute`, path.go:245), and `getMatch` during pattern evaluation.

### What Cannot Be Determined

- The **exact mechanism** by which `RestartRouting` re-enters the `next`/`nextCustom` loop (e.g., whether it resets an index counter, returns a sentinel error, or uses a goto) is not detailed in the clue file. The `App.next` and `App.nextCustom` symbols are listed as **uncovered** in the GAPS section.
- Whether the 404/405 distinction is made inside `next`/`nextCustom` or in `requestHandler` after the loop completes cannot be definitively determined — only the behavioral precedence pattern hints at it.
- The interaction between `DefaultCtx.Path` override and the detection path used by `Route.match` is not explicitly described, though `DefaultCtx.Path` calling `configDependentPaths` (`DefaultCtx.Path`, ctx.go:297) suggests path variants are recalculated.
- `DefaultCtx.Matched` (`DefaultCtx.Matched`, ctx.go:375-376) provides a way to check if the current path was matched by the router, calling `getMatched`, but the internal state it reads is not fully described.
