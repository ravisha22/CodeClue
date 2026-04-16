# v2.4.1 Response: blind-fiber-1
Date: 2026-04-16

## Path Rewriting, Route Re-dispatch, and 404/405 Outcomes

### Route Matching Infrastructure

Fiber uses `RoutePatternMatch` (`path.go:155`) to test whether a path matches a given route pattern. Internally it calls `parseRoute` (`path.go:245`), `getMatch` (`path.go:507`), `RemoveEscapeCharBytes` (`path.go:659`), and `reset` (`path.go:213`) [FOCUS §RoutePatternMatch, path.go:155]. The route parser decomposes patterns into `routeSegment` structs (`path.go:40`) and supports parameter constraints via `Constraint.CheckConstraint` (`path.go:707`) and `CustomConstraint` (`path.go:88`) [Source Snippets §routeSegment, §Constraint, §CustomConstraint].

### Path Access and Manipulation

`DefaultCtx.Path` (`ctx.go:297`) returns the request path and calls `configDependentPaths` [FOCUS §DefaultCtx.Path]. A middleware can override the path by passing a new value via `DefaultCtx.Path(override ...string)`. The companion method `DefaultCtx.Matched` (`ctx.go:375`) delegates to `getMatched` and reports whether the router matched the current request; it is called by `OverrideParam` [FOCUS §DefaultCtx.Matched].

### Dispatch Pipeline (what can be inferred)

The clue file's GAPS section lists `App.next` and `App.nextCustom` as **uncovered** [GAPS]. These are the core dispatch functions — they iterate through route stacks, calling `Route.match` to find a matching handler. Because their behavior annotations are absent, **the exact mechanism by which middleware triggers a re-dispatch (e.g., whether it resets an index and re-calls `App.next`) cannot be fully determined from the prompt**.

### Middleware Registration

`App.Use` (`app.go:860`) registers middleware routes via `toFiberHandler` (`adapter.go:13`), which dispatches to `adaptFiberHandler`, `adaptHTTPHandler`, etc. [FOCUS §App.Use, §toFiberHandler]. Groups (`Group.Use`, `group.go:70`) and domain routers (`domainRouter.Use`, `domain.go:350`) follow the same pattern [FOCUS §Group.Use, §domainRouter.Use].

### Restart-Routing Signal

`DefaultCtx.RestartRouting` is listed in the GAPS uncovered list [GAPS], confirming the method exists but its body logic is not provided. Based on its name and the surrounding dispatch context (`App.next`/`App.nextCustom` iterate `Route.match` in a loop [GAPS]), it likely resets the route-matching index so `App.next` re-evaluates all routes from the beginning with the rewritten path.

### 404 vs 405 Decision

The clue does **not** contain explicit logic for generating 404 or 405 responses. However:
- The route stack is keyed by HTTP method (`App.Add` at `app.go:953` registers by method) [SYM §App.Add].
- `App.pruneAutoHeadRouteLocked` (`router.go:491`) handles auto-generated HEAD routes [FOCUS §App.pruneAutoHeadRouteLocked].
- If `App.next` exhausts all routes for the matched method, a 404 results. If the path matches a route but under a different method, a 405 is expected. **The exact branching logic cannot be confirmed** because `App.next` and `App.nextCustom` bodies are uncovered [GAPS].

### What Cannot Be Determined

- The exact body of `App.next` / `App.nextCustom` (how the match loop works, how 404 vs 405 is decided) [GAPS: uncovered].
- The body of `DefaultCtx.RestartRouting` (the mechanism to restart dispatch) [GAPS: uncovered].
- Whether path normalizing (`App.normalizePath`, `router.go:398`) is re-applied on a rewritten path [SYM §App.normalizePath — no behavior annotation].
- How `Request.DisablePathNormalizing` (`client/request.go:614`) interacts with server-side re-dispatch (it appears to be a client-side setting) [Source Snippet §Request.DisablePathNormalizing].
