# v2.4 Response: blind-echo-mech-1
Date: 2026-04-16

## Question
How does Echo decide which route wins when static segments, parameters, and wildcards overlap?

## Answer

### 1. Trie-Based Router Structure

Echo's routing is implemented via a **trie (prefix tree)** structure in the `DefaultRouter` (`DefaultRouter`, router.go:60). The trie is built from **`node`** objects that have children of different types. Key evidence:

- `node.findStaticChild` (`node.findStaticChild`, router.go:709) searches among static children with behavior `ACCUMULATE(loop -> result)` — confirming that each trie node maintains a list of static child nodes.
- `node.setHandler` (`node.setHandler`, router.go:731) sets the handler on a node, calling `routeMethods.set`.
- `routeMethods` (`routeMethods`, router.go:148) stores method-to-handler mappings at each node, with methods `find`, `isHandler`, `set`, `updateAllowHeader`.

### 2. Route Lookup: `DefaultRouter.Route`

The route matching logic is in `DefaultRouter.Route` (`DefaultRouter.Route`, router.go:791). Its behavior annotation reveals:

```
PRECEDENCE(cap -> not_r.useEscapedPathForRouting -> currentNode)
ACCUMULATE(len loop -> searchIndex)
calls: findStaticChild, node, find
```

This tells us:

1. **PRECEDENCE** evaluation occurs — `cap`, then `not_r.useEscapedPathForRouting`, then `currentNode` are evaluated in precedence order. The `cap` likely refers to the capacity/length of the path, and `useEscapedPathForRouting` is a configuration flag affecting whether escaped or raw paths are used for matching.

2. The method **calls `findStaticChild` first**, followed by `node` and `find`. This call order strongly suggests that **static children are checked before parameterized or wildcard children** during traversal — establishing a **static > parameter > wildcard** priority.

3. **ACCUMULATE with a `len loop`** indicates the router iterates through path segments character by character or segment by segment, advancing a `searchIndex`.

### 3. Static Child Lookup Priority

`node.findStaticChild` (`node.findStaticChild`, router.go:709) takes a single byte argument (`l byte`) and loops through static children to find a match. Being called first by `DefaultRouter.Route` confirms that **static segments have highest priority** — when a path segment matches a static child exactly, that branch is preferred.

### 4. Method Dispatch with Fallback to "Any"

Once a node is reached, `routeMethods.find` (`routeMethods.find`, router.go:213) resolves the handler:

```
GUARD(r != nil || !fallbackToAny -> return r)
DISPATCH(method)
```

This reveals:
- It first tries to find a handler for the specific HTTP method via `DISPATCH(method)`.
- If no method-specific handler exists and `fallbackToAny` is true, it falls back to an "any" handler — this is relevant for routes registered via `Echo.Any` (`Echo.Any`, echo.go:504), which registers handlers for all HTTP methods.

### 5. Route Registration and the `RouteNotFound` Fallback

Routes are inserted via `Echo.add` (`Echo.add`, echo.go:621), which calls the router's `Add` method. The behavior `PRECEDENCE(e -> err -> paramsCount)` suggests that parameter count is tracked during registration, which may influence node structure.

A special fallback exists: `Echo.RouteNotFound` (`Echo.RouteNotFound`, echo.go:495) registers a handler "executed when no other route is found." Similarly, `Group.RouteNotFound` (`Group.RouteNotFound`, group.go:153) provides the same for groups. This acts as the lowest-priority catch-all.

### 6. Static File Routes as Regular Routes

Static file serving uses the same routing mechanism:
- `Echo.Static` (`Echo.Static`, echo.go:533) calls `Add`, `MustSubFS`, and `StaticDirectoryHandler`.
- `Echo.StaticFS` (`Echo.StaticFS`, echo.go:548) calls `Add` and `StaticDirectoryHandler`.
- `StaticDirectoryHandler` (`StaticDirectoryHandler`, echo.go:559) creates a handler that calls `Open` and `sanitizeURI` — it sanitizes the URI before filesystem access.

These are registered as normal routes, so they follow the same trie-based priority rules.

### 7. Route Info and Reverse Routing

`RouteInfo.Reverse` (`RouteInfo.Reverse`, route.go:75) can reverse a route to a URL by substituting path parameters with `ACCUMULATE(Fprintf loop -> result)`. The `Routes` collection provides filtering by method, path, and name (`Routes.FilterByMethod`, route.go:141; `Routes.FilterByPath`, route.go:159; `Routes.FilterByName`, route.go:177), and `Routes.FindByMethodPath` (route.go:127) for exact lookup.

### 8. Route Matching with Escaped Paths

The `useEscapedPathForRouting` flag (referenced in `DefaultRouter.Route`'s PRECEDENCE) suggests the router can be configured to match against URL-escaped or unescaped paths, affecting which route wins when segments contain special characters.

### 9. Inferred Priority Order

Based on the clue evidence:

1. **Static segments** — highest priority. `findStaticChild` is called first in `DefaultRouter.Route`, meaning exact literal matches are tried before anything else.
2. **Parameterized segments** — checked when no static child matches. The `node` call in `DefaultRouter.Route` likely traverses parameter nodes.
3. **Wildcard segments** — lowest priority among route types. The `find` call likely handles catch-all/wildcard matching.
4. **RouteNotFound** — absolute fallback when nothing matches.

### Cannot Be Determined from the Clue File

- **The exact body logic of `DefaultRouter.Route`** — the clue provides only behavior annotations and call lists, not the full source code. The precise trie traversal algorithm (backtracking strategy, how parameter vs. wildcard nodes are distinguished in the trie) is not available.
- **The `node` struct definition** — its fields (e.g., `paramChild`, `anyChild`, `staticChildren`) are not shown.
- **The `concurrentRouter` details** — only its `Route` delegation is shown (`concurrentRouter`, listed in GAPS as uncovered).
- **The `Router` interface** and **`RouterConfig`** type — both listed as uncovered in GAPS.
- **How conflicting routes are handled at registration time** — whether duplicate static/param/wildcard routes cause errors or overwrite. `AddRouteError` exists but its triggering conditions are not detailed.
- **The exact meaning of `cap` in the PRECEDENCE annotation** of `DefaultRouter.Route`.
