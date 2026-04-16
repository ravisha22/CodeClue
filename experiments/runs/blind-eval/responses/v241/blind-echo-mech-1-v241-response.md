# v2.4.1 Response: blind-echo-mech-1
Date: 2026-04-16

## How Echo Decides Which Route Wins When Static, Parameter, and Wildcard Segments Overlap

### The Route Lookup Entry Point

`DefaultRouter.Route` (`router.go:791`) is the method that looks up a handler registered for a given method and path [FOCUS: DefaultRouter.Route — "Route looks up a handler registered for method and path"]. Its behavior annotation reads: **`PRECEDENCE(cap -> not_r.useEscapedPathForRouting -> currentNode); ACCUMULATE(len loop -> searchIndex)`** [FOCUS: DefaultRouter.Route]. This PRECEDENCE annotation indicates an ordered priority evaluation: first a capacity/allocation step (`cap`), then a check on `useEscapedPathForRouting` (which likely determines whether the raw or escaped URI is used for matching), and then traversal starting from `currentNode`. The ACCUMULATE pattern over a length-based loop with `searchIndex` suggests the router walks through the path **segment by segment**, advancing an index through the URI.

The method calls three key functions: `findStaticChild`, `node`, and `find` [FOCUS: DefaultRouter.Route — "calls: findStaticChild, node, find"].

### Static Segment Priority

`node.findStaticChild` (`router.go:709`) searches for a static child node matching a given byte: **`ACCUMULATE(loop -> result)`** [FOCUS: node.findStaticChild]. It is called by `Route`, `Remove`, and `findChildWithLabel` [FOCUS: node.findStaticChild — "called_by: Remove, Route, findChildWithLabel"]. The fact that `DefaultRouter.Route` calls `findStaticChild` **as its first listed call target** strongly suggests that **static segments are checked before parameter or wildcard segments**. The loop-based accumulation implies iterating over the node's static children to find an exact byte match.

### Method Dispatch and Fallback-to-Any

Once a node is reached, `routeMethods.find` (`router.go:213`) resolves which handler to use for the matched HTTP method: **`GUARD(r != nil || !fallbackToAny -> return r); DISPATCH(method)`** [FOCUS: routeMethods.find]. This reveals two important mechanics:
1. The `DISPATCH(method)` pattern indicates a switch/map on the HTTP method (GET, POST, etc.).
2. The `GUARD` with `fallbackToAny` means: if no method-specific handler is found (`r == nil`) **and** `fallbackToAny` is true, the lookup falls through to an "any"-method handler. This corresponds to routes registered via `Echo.Any` (`echo.go:504`) [FOCUS: Echo.Any].

`routeMethods.set` (`router.go:171`) stores handlers per method and calls `updateAllowHeader` (`router.go:251`) to maintain the `Allow` header for 405 responses [FOCUS: routeMethods.set, routeMethods.updateAllowHeader].

### Route Registration and the Node Tree

All routes are inserted through `Echo.add` (`echo.go:621`) → `DefaultRouter.Add` [FOCUS: Echo.add — "calls: Add"]. `DefaultRouter` has an `insert` method (listed in its methods: `Add, Remove, Route, Routes, insert, storeRouteInfo`) [FOCUS: DefaultRouter], suggesting a trie/tree insertion. `DefaultRouter.storeRouteInfo` (`router.go:538`) accumulates route metadata after insertion [FOCUS: DefaultRouter.storeRouteInfo — "called_by: Add"].

The `Echo.add` behavior — `GUARD(e.OnAddRoute != nil -> return RouteInfo{},...); PRECEDENCE(e -> err -> paramsCount)` — shows that `paramsCount` is part of the precedence evaluation during registration, meaning the router is aware of how many parameters a route pattern contains [FOCUS: Echo.add].

### Special Route Types

- **Static file routes**: `Echo.Static` (`echo.go:533`) and `Echo.StaticFS` (`echo.go:548`) both delegate to `Echo.Add` with a `StaticDirectoryHandler` (`echo.go:559`), which serves from a filesystem and calls `Open` and `sanitizeURI` [FOCUS: Echo.Static, Echo.StaticFS, StaticDirectoryHandler]. `Echo.File` (`echo.go:609`) and `Echo.FileFS` (`echo.go:591`, delegates to `Echo.GET` + `StaticFileHandler`) register exact-path file serving [FOCUS: Echo.File, Echo.FileFS].
- **Not-found routes**: `Echo.RouteNotFound` (`echo.go:495`) registers a special-case handler "executed when no other route is found" [FOCUS: Echo.RouteNotFound]. This acts as a catch-all fallback *after* the normal tree traversal fails.
- **Route reversal**: `RouteInfo.Reverse` (`route.go:75`) and `Routes.Reverse` (`route.go:117`) reconstruct URLs from path parameters [FOCUS: RouteInfo.Reverse, Routes.Reverse].
- **`Context.RouteInfo`** (`context.go:225`) retrieves current request route information with `GUARD(c.route != nil -> return c.route.Clone())` [FOCUS: Context.RouteInfo].

### Concurrent Access

`concurrentRouter.Route` (`router_concurrent.go:21`) wraps `DefaultRouter.Route` with deferred unlock semantics — `DELEGATE(r.router.Route -> result); UNWIND(defer)` — ensuring thread-safe lookups [FOCUS: concurrentRouter.Route].

### Inferred Priority Order

Based on the `DefaultRouter.Route` PRECEDENCE annotation and its call sequence (`findStaticChild` → `node` → `find`), the priority is:
1. **Static segments** — matched first via `findStaticChild`.
2. **Parameter segments** — implied by the `node` call after static child lookup (the tree traversal continues if no static match is found).
3. **Any-method fallback** — `routeMethods.find` falls back to an any-method handler if `fallbackToAny` is true.
4. **RouteNotFound** — the catch-all executed when no other route matches.

### What Cannot Be Determined

- The **exact algorithm for parameter vs. wildcard priority** is not visible. The source snippets provide only function signatures, not bodies. The clue's FOCUS does not describe a `findParamChild` or `findWildcardChild` method, so the relative priority between `:param` and `*wildcard` segments **cannot be confirmed** from this artifact [GAPS: type MECHANISTIC — "body logic needed for full answer"].
- The **`node` type's full structure** (how children are organized — static vs. param vs. wildcard arrays/maps) is not detailed. Only `node.findStaticChild` and `node.setHandler` are shown [SYM: node.findStaticChild, node.setHandler].
- **`Echo.ServeHTTP`** and **`Echo.serveHTTP`** are listed as uncovered [GAPS: "uncovered: Echo.ServeHTTP, Echo.Group, Echo.AcquireContext, Echo.NewContext"], so the full dispatch flow from HTTP request to router invocation is not fully traceable.
- The **`useEscapedPathForRouting`** flag's precise semantics (whether it affects matching priority or just URI encoding) are not explained beyond appearing in the PRECEDENCE annotation.
- The behavior of **overlapping wildcard routes** at the same tree depth (e.g., `/users/:id` vs. `/users/*`) is not determinable without the router's body logic.
- The **middleware static file middleware** (`Static` at `middleware/static.go:144`) is separate from `Echo.Static` and its interaction with the router's own static-path matching is not clarified [FOCUS: Static middleware/static.go:144 vs. Echo.Static echo.go:533].
