# v2.2 Response: blind-echo-mech-1
Date: 2026-04-15

## Question
How does Echo decide which route wins when static segments, parameters, and wildcards overlap?

## Answer

### 1. The Core Route-Matching Function

Route matching is performed by **`DefaultRouter.Route`** (router.go:791) — "looks up a handler registered for method and path." Its behavior annotation is:

```
GUARD(child -> result); PRECEDENCE(cap -> not_r.useEscapedPathForRouting -> previous); ACCUMULATE(loop -> result)
```

This reveals three key mechanisms:

1. **GUARD(child -> result)** — The router checks child nodes in its tree structure. If a child matches, it produces a result. This suggests a tree-based routing structure where the router traverses child nodes for each path segment.

2. **PRECEDENCE(cap -> not_r.useEscapedPathForRouting -> previous)** — There is a priority/precedence system. The annotation shows precedence decisions involving:
   - `cap` — likely "capacity" or a node capability indicator, suggesting different node types (static, param, wildcard) have different priorities.
   - `not_r.useEscapedPathForRouting` — a configuration flag that affects whether escaped paths are used for routing.
   - `previous` — fallback to a previously matched result when the current path doesn't produce a better match.

3. **ACCUMULATE(loop -> result)** — The router iterates through path segments in a loop, accumulating the match result segment by segment.

### 2. Route Types Visible in the Codebase

From the clue and source snippets, routes can be registered as:

**Static routes (exact paths):**
- `Echo.GET` (echo.go:449) — `func (e *Echo) GET(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo`
- All other HTTP method shortcuts follow the same pattern.

**Static file routes:**
- `Echo.Static` (echo.go:533) — "registers a new route with path prefix to serve static files." Calls `Add`, `MustSubFS`, `StaticDirectoryHandler`.
- `Echo.StaticFS` (echo.go:548) — registers route for filesystem serving. Calls `Add`, `StaticDirectoryHandler`.
- `Echo.File` (echo.go:609) — registers a single static file route.
- `Group.Static` (group.go:112) — delegates to `Group.StaticFS`.
- `Group.StaticFS` (group.go:122) — delegates to `Group.Add`.

**Parameterized and wildcard routes:**
- Route reversal logic in `RouteInfo.Reverse` (route.go:75) — "reverses route to URL string by replacing path parameters with given params values." Behavior: `ACCUMULATE(loop -> result)`. This confirms the router supports parameterized routes with named path parameters.
- `PathValue` (router.go:1051) — "tuple of path parameter name and its value in request path." This data structure stores matched parameter values.
- `Context.InitializeRoute` (context.go:263) — "sets the route related variables of this request to the context." Calls `PathValues` and `setPathValues`.

**Not-found routes:**
- `Echo.RouteNotFound` (echo.go:495) — "registers a special-case route which is executed when no other route is found." Uses `RouteNotFound` method constant as the HTTP method.

### 3. Internal Tree Structure

**`routeMethods`** (router.go:148) — has methods `find`, `isHandler`, `set`, `updateAllowHeader`.
- `routeMethods.set` (router.go:171) — behavior: `DISPATCH(method)` — dispatches based on HTTP method string, suggesting each tree node stores handlers indexed by HTTP method.
- `routeMethods.isHandler` (router.go:301) — checks if a node has a handler, called by `setHandler`.
- `routeMethods.find` — locates the handler for a given method.

**`routeMethod`** (router.go:142) — internal type representing a single method's route entry.

**`DefaultRouter.insert`** — listed in DefaultRouter's methods (router.go:60), this builds the tree.

### 4. Matching Precedence Analysis

Based on the `PRECEDENCE` annotation in `DefaultRouter.Route` (router.go:791), the router uses a priority system when multiple routes could match:

- The `GUARD(child -> result)` pattern suggests the router first tries to match children — likely trying the most specific (static) child first before falling back to parameter or wildcard children.
- The `PRECEDENCE` with `previous` suggests a backtracking mechanism: if a more specific match fails, the router falls back to a less specific previous match.
- The `cap` term in the precedence likely represents the type/capability of the node, with static segments having higher priority than parameterized segments, which in turn have higher priority than wildcard segments.

**Inferred priority order (from behavioral annotations):**
1. **Static segments** — exact literal matches (highest priority)
2. **Parameter segments** — named path parameters (`:param` style)
3. **Wildcard/catch-all segments** — matches remaining path (lowest priority)

### 5. Escaped Path Routing

The `not_r.useEscapedPathForRouting` in the PRECEDENCE annotation of `DefaultRouter.Route` (router.go:791) indicates a configuration option that controls whether URL-encoded paths are used for matching. Similarly, `StaticDirectoryHandler` (echo.go:559) has behavior `PRECEDENCE(not_disablePathUnescaping -> err)`, confirming path escaping is a routing concern.

### 6. Concurrent Access

**`concurrentRouter.Route`** (router_concurrent.go:21) — behavior: `DELEGATE(r.router.Route -> result); UNWIND(defer)`. The concurrent router wraps the default router's `Route` method with locking (defer suggests deferred unlock), ensuring thread-safe route matching.

### 7. Route Search Helpers

**`Routes.FindByMethodPath`** (route.go:127) — "searched for matching route info by method and path." Behavior: `GUARD(r -> RouteInfo); PRECEDENCE(r -> rr); ACCUMULATE(loop -> result)`. This is a post-registration lookup that searches registered route info.

**`Routes.FilterByPath`** (route.go:159) — "searched for matching route info by path." Behavior: `GUARD(r -> errors.New); PRECEDENCE(r -> rr -> len); ACCUMULATE(loop -> result)`.

### 8. What Cannot Be Determined

The clue file and source snippets do **not** provide:

- The exact tree data structure (radix tree, trie, or other) — only behavioral patterns are visible.
- The specific algorithm for backtracking between static/param/wildcard nodes — only the `PRECEDENCE` and `GUARD` patterns hint at this.
- Whether wildcard routes use `*` syntax, `:param` syntax, or something else — only `PathValue` (router.go:1051) confirms named parameters exist.
- The exact priority rules when two parameterized routes or two wildcard routes conflict at the same tree level.
- The full body of `DefaultRouter.Route` (router.go:791) — only the behavior summary and 1074 total lines in router.go are known.
