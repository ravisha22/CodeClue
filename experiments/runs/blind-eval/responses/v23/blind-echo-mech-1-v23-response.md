# v2.3 Response: blind-echo-mech-1
Date: 2026-04-15

## Summary

Echo uses a radix-tree router (`DefaultRouter` in `router.go`) that prioritizes static segments over parameterized segments over wildcards during route lookup. The routing decision is made at request time by traversing a tree of `node` objects, preferring exact (static) child matches first.

## Detailed Analysis

### Route Registration Pipeline

- **`Echo.Add`** (`echo.go:642`) is the central route registration method. All HTTP method helpers (`GET`, `POST`, `DELETE`, `HEAD`, `OPTIONS`, `PATCH`, `CONNECT`, `TRACE`) delegate to it (FOCUS: `Echo.Add` — `called_by: Any, CONNECT, DELETE, File, GET, HEAD, OPTIONS, PATCH`; behavior: `GUARD(err -> raise_panic)`).
- `Echo.Add` calls the internal **`Echo.add`** (`echo.go:621`), which has behavior `GUARD(e -> RouteInfo); PRECEDENCE(e -> err -> paramsCount)` — indicating it evaluates precedence by parameter count when registering routes (FOCUS: `Echo.add`).
- `Echo.add` calls **`DefaultRouter.Add`** (`router.go`, listed in INDEX as the `Add` method), which inserts the route into the radix tree.
- Routes are stored via **`node.setHandler`** (`router.go:731`, SYM), which sets the handler on a tree node.
- Route metadata is stored with **`DefaultRouter.storeRouteInfo`** (`router.go:538`), behavior: `ACCUMULATE(loop -> result)`.

### Route Lookup / Matching — The Core Decision

- **`DefaultRouter.Route`** (`router.go:791`) is the route lookup function invoked at request time. Its behavior annotation is: `PRECEDENCE(cap -> not_r.useEscapedPathForRouting -> currentNode); ACCUMULATE(loop -> searchIndex)` (FOCUS: `DefaultRouter.Route`).
  - The `PRECEDENCE` annotation reveals the priority ordering: it first considers capacity/static match (`cap`), then whether escaped path routing is in use, then falls back to `currentNode` traversal. The `ACCUMULATE(loop -> searchIndex)` indicates an iterative tree-walk accumulating a search index.
- It calls **`node.findStaticChild`** (`router.go:709`), behavior: `ACCUMULATE(loop -> result)` — this function searches for an exact (static) child node matching the next path byte. The fact that this is called first in the route resolution process indicates **static segments are checked before parameterized or wildcard segments** (FOCUS: `node.findStaticChild`; `called_by: Remove, Route, findChildWithLabel`).

### Priority Order: Static > Param > Wildcard

Based on the clue file evidence:

1. **Static segments win first**: `DefaultRouter.Route` calls `findStaticChild` to look for exact byte-level matches in the radix tree (FOCUS: `DefaultRouter.Route` calls `findStaticChild, node, find`). Static children are tried before any other node type.
2. **Parameterized segments come second**: The `routeMethods` type (`router.go:148`) has methods `find`, `isHandler`, `set`, `updateAllowHeader`. The `routeMethods.find` method (`router.go:213`) has behavior `GUARD(r -> pass_through); DISPATCH(method)` — it dispatches based on method, and is called by `Route` (the lookup function). This suggests that once static matching fails, the router falls through to parameter nodes.
3. **Wildcard segments are lowest priority**: The `PRECEDENCE` annotation on `DefaultRouter.Route` shows a clear ordering of precedence levels, with the tree walk (`currentNode`) as the fallback path.

### Route-Not-Found Handling

- **`Echo.RouteNotFound`** (`echo.go:495`) registers a special-case route executed when no other route matches. Behavior: `DELEGATE(e.Add -> result)` — it registers like a normal route via `Add` but is consulted only when all other matches fail (FOCUS: `Echo.RouteNotFound`).
- **`Group.RouteNotFound`** (`group.go:153`) provides the same capability for sub-routes within a group (FOCUS: `Group.RouteNotFound`).

### Static File Routes

- **`Echo.Static`** (`echo.go:533`) and **`Echo.StaticFS`** (`echo.go:548`) register static file routes via `Add`, meaning they participate in the same radix tree and priority system as all other routes (FOCUS: both show `behavior: DELEGATE(e.Add -> result)`).
- From the source snippet, `Echo.StaticFS` signature is `func (e *Echo) StaticFS(pathPrefix string, filesystem fs.FS, middleware ...MiddlewareFunc) RouteInfo` — it uses `Add` and `StaticDirectoryHandler` (FOCUS + source snippet: `echo.go L548`).
- **`StaticDirectoryHandler`** (`echo.go:559`) creates the handler that serves files, calling `Open` and `sanitizeURI` (FOCUS: `StaticDirectoryHandler`).

### Concurrent Router

- **`concurrentRouter.Route`** (`router_concurrent.go:21`) wraps `DefaultRouter.Route` with behavior `DELEGATE(r.router.Route -> result); UNWIND(defer)`, adding concurrency safety via deferred unlock, but the actual routing logic (and thus priority decisions) is delegated unchanged (FOCUS: `concurrentRouter.Route`).

### Method-Level Dispatch

- **`routeMethods.find`** (`router.go:213`) dispatches based on HTTP method with behavior `DISPATCH(method)`. The `fallbackToAny` parameter suggests that if no method-specific handler is found, a registered "any-method" handler can serve as fallback (SYM/FOCUS: `routeMethods.find`).
- **`routeMethods.set`** (`router.go:171`) stores handlers by method and calls `updateAllowHeader` (`router.go:251`) to maintain the `Allow` response header (SYM: `routeMethods.set`, `routeMethods.updateAllowHeader`).

## Uncertainty / Limits

- **Exact tie-breaking algorithm within parameterized nodes**: The clue file does not provide the full body logic of `DefaultRouter.Route`, so the exact algorithm for choosing between multiple overlapping parameterized segments (e.g., `:id` vs `:name` on the same path position) cannot be determined.
- **Wildcard node structure**: The node type's full field layout (e.g., whether it has separate fields for static children, param child, and wildcard child) is not directly documented in the clue file or source snippets. The GAPS section confirms this is a `MECHANISTIC` gap requiring body logic.
- **`useEscapedPathForRouting` semantics**: Referenced in `DefaultRouter.Route`'s PRECEDENCE annotation but not further elaborated; its exact effect on priority is unclear from the available information.
- **Source snippets are signature-only**: The drill-down snippets for this task only show function signatures, not bodies, limiting mechanistic analysis.
