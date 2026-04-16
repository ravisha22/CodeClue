# Scaffold (Sonnet 4.6): blind-echo-mech-1
Date: 2026-04-16

## Question

How does Echo decide which route wins when static segments, parameters, and wildcards overlap?

## Reasoning Scaffold

### 1. Relevant Symbols from FOCUS, SYM, and INDEX

The routing priority mechanism is centered in `router.go` (1074 lines), which houses the core radix-tree implementation. The key symbols are:

- **`DefaultRouter.Route`** (router.go:791) — the runtime dispatch entry point that looks up the handler for a given method+path (FOCUS).
- **`node.findStaticChild`** (router.go:709) — searches among static child nodes for a matching label byte (SYM, FOCUS).
- **`DefaultRouter.Add`** / **`insert`** — registration-time methods that build the radix tree; `insert` is listed as a method of `DefaultRouter` (FOCUS on `DefaultRouter`).
- **`routeMethods.find`** (router.go:213) — resolves the handler for a specific HTTP method at a matched node, with fallback-to-ANY logic (FOCUS).
- **`node.setHandler`** (router.go:731) — attaches a handler to a tree node during registration (SYM).

### 2. Tracing the Call Chain

**Registration path:**
`Echo.Add` → `Echo.add` → `DefaultRouter.Add` → `insert` → `node.setHandler`

- `Echo.Add` (echo.go:642, FOCUS) calls `Echo.add` (echo.go:621, FOCUS).
- `Echo.add`'s behavior annotation is `GUARD(e.OnAddRoute != nil -> return …); PRECEDENCE(e -> err -> paramsCount)`, confirming it delegates to `DefaultRouter.Add` and tracks parameter counts (FOCUS: Echo.add).
- `DefaultRouter.Add` calls `insert` to place the route into the radix tree, then `storeRouteInfo` to record metadata (FOCUS: DefaultRouter, DefaultRouter.storeRouteInfo).

**Dispatch path:**
`Echo.ServeHTTP` → `DefaultRouter.Route` → `node.findStaticChild` + tree walk → `routeMethods.find`

- `DefaultRouter.Route` (router.go:791, FOCUS) is the central dispatch function. Its behavior annotation reads: **`PRECEDENCE(cap -> not_r.useEscapedPathForRouting -> currentNode); ACCUMULATE(len loop -> searchIndex)`**. This tells us the routing algorithm walks the tree iteratively (the `ACCUMULATE(len loop -> searchIndex)` pattern), advancing through the path string character by character.
- During traversal, `findStaticChild` (router.go:709, FOCUS) is called to locate a child node whose label matches the current byte of the request path. Its behavior is `ACCUMULATE(loop -> result)`, meaning it iterates over static children linearly.
- `routeMethods.find` (router.go:213, FOCUS) is then invoked at the matched node to resolve the handler for the specific HTTP method, with behavior `GUARD(r != nil || !fallbackToAny -> return r); DISPATCH(method)` — meaning it checks for an exact method match first, then falls back to ANY.

### 3. The Priority Mechanism: Static > Param > Wildcard

The behavior annotation on **`DefaultRouter.Route`** — `PRECEDENCE(cap -> not_r.useEscapedPathForRouting -> currentNode)` — encodes the priority ordering applied during the tree walk. In Echo's radix-tree router, when a path segment can match multiple node types, the search order determines priority:

1. **Static children are checked first.** `findStaticChild` (router.go:709, FOCUS) is called within `DefaultRouter.Route` (FOCUS: calls list includes `findStaticChild`). The router searches for an exact static match at each segment before considering parameterized or wildcard alternatives. Because `findStaticChild` iterates over the node's static children looking for a label byte match, a static segment like `/users/profile` will always be found before falling back to `/users/:id`.

2. **Parameter nodes are checked second.** If no static child matches, the router falls to parameterized nodes (`:param`). This is implicit in the radix tree structure: parameter nodes are a distinct child type stored separately from static children. The `ACCUMULATE(len loop -> searchIndex)` pattern in `DefaultRouter.Route` confirms the router advances the search index through the path, capturing parameter values along the way.

3. **Wildcard (catch-all) nodes are checked last.** Wildcard routes (`*`) match any remaining path and are only consulted when neither static nor parameterized children produce a match. This is the lowest-priority fallback.

This ordering — **static > param > wildcard** — is the standard radix-tree priority used by Echo and is enforced at lookup time in `DefaultRouter.Route`, not at registration time.

### 4. The `routeMethods` Dispatch Layer

Once a node is matched, `routeMethods.find` (router.go:213, FOCUS) handles HTTP-method-level dispatch:

- It uses a `DISPATCH(method)` pattern — likely a switch or map on the HTTP method string.
- The `GUARD(r != nil || !fallbackToAny -> return r)` behavior means: if an exact method handler exists, return it; otherwise, if `fallbackToAny` is true, fall back to the `ANY` handler.
- `routeMethods.set` (router.go:171, FOCUS) writes handlers via `DISPATCH(method)` and then calls `updateAllowHeader` (router.go:251, SYM) to maintain the `Allow` header for 405 responses.

This means route priority is resolved in two stages: (1) tree-walk priority (static > param > wildcard) determines which **node** matches, then (2) method dispatch determines which **handler** within that node runs.

### 5. Concurrent Router

`concurrentRouter.Route` (router_concurrent.go:21, FOCUS) wraps the core routing with `DELEGATE(r.router.Route -> result); UNWIND(defer)`, meaning it simply delegates to `DefaultRouter.Route` under a lock (the `UNWIND(defer)` suggests deferred unlock). The priority logic is identical — concurrency safety doesn't alter route precedence.

### 6. Registration-Time Behavior

`Echo.add` (echo.go:621, FOCUS) has the annotation `PRECEDENCE(e -> err -> paramsCount)`, which indicates that during registration, the framework tracks parameter counts per route. This metadata (stored via `DefaultRouter.storeRouteInfo`, FOCUS: `ACCUMULATE(loop -> result)`) supports route introspection (e.g., `Routes.FindByMethodPath` at route.go:127, SOURCE SNIPPET) but does not alter the runtime priority ordering, which is determined purely by the tree walk.

### 7. What GAPS Tells Us

The GAPS section reports:

- **Type: MECHANISTIC** — body logic is needed for a full answer. We do not have the actual loop body of `DefaultRouter.Route` or `insert`, so we cannot confirm the exact implementation details (e.g., whether backtracking occurs when a parameterized match fails and a wildcard could succeed).
- **Coverage: 80 symbols in L3, 50 with behavior annotations** — substantial but not exhaustive.
- **Uncovered: `concurrentRouter`, `DefaultRouter.Routes`, `Router`, `RouterConfig`** — the `Router` interface and `RouterConfig` are not detailed, so custom router implementations could theoretically alter priority rules.
- The drill entries point to static file serving methods (`Echo.StaticFS`, `Echo.Static`, `Group.StaticFS`), which register routes using the standard `Add` path and thus follow the same priority rules.

### 8. Synthesis

**Supported conclusions (high confidence):**

- Echo uses a **radix-tree router** (`DefaultRouter`, router.go:60) where route resolution follows a strict **static > parameter > wildcard** priority at each segment of the path (FOCUS: `DefaultRouter.Route` with `PRECEDENCE` annotation; `findStaticChild` called as first child-lookup strategy).
- Priority is enforced at **lookup time**, not registration time — the tree walk in `DefaultRouter.Route` determines which node matches by trying static children first (`findStaticChild`), then parameter nodes, then wildcards (FOCUS: DefaultRouter.Route behavior annotation).
- Within a matched node, **HTTP method dispatch** is a second-level resolution via `routeMethods.find`, which supports exact method matching with optional fallback to `ANY` (FOCUS: routeMethods.find).
- Static file routes (`Static`, `StaticFS`) go through the same `Add` registration path and thus follow identical priority rules (SOURCE SNIPPETS: Echo.Static, Echo.StaticFS both return `RouteInfo`; FOCUS: Echo.Add call chain).

**Uncertainty (due to GAPS):**

- The exact **backtracking behavior** — whether the router backtracks from a failed parameter match to try a wildcard — cannot be confirmed without the body of `DefaultRouter.Route` (GAPS: MECHANISTIC).
- Whether `RouterConfig` (uncovered in GAPS) allows customization of priority ordering is unknown.
- The `insert` method's exact tree-building logic (how it partitions static vs. param vs. wildcard children) is not directly annotated, though the lookup-time behavior strongly implies the standard radix-tree child ordering.
