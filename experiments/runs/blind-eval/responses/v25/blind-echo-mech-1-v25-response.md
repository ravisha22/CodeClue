# v2.5 Response: blind-echo-mech-1
Date: 2026-04-16

## Question

How does Echo decide which route wins when static segments, parameters, and wildcards overlap?

## Analysis

### 1. The Router Is a Radix Tree with Typed Node Children

The `DefaultRouter` (router.go:60) is described as a "registry of all registered routes for an Echo instance for request matching and URL path parameters." Its core operations — `Add`, `Remove`, `insert`, `Route` — all revolve around a tree of `node` objects. The presence of `node.addStaticChild` (router.go:705) and `node.findStaticChild` (router.go:709) tells us nodes explicitly differentiate between static children (fixed path segments) and other child types.

**Supported by clue:** The node type exposes `addStaticChild` and `findStaticChild` as distinct operations, confirming the tree segregates static children from parameter/wildcard children at the data-structure level.

### 2. Route Registration Builds the Tree via `insert`

When a route is registered through `Echo.Add` (echo.go:642), it delegates to `Echo.add` (echo.go:621), which calls `DefaultRouter.Add` (router.go:447). The `Add` method in turn calls `DefaultRouter.insert` (router.go:548) to place the route into the node tree. During insertion, `node.addStaticChild` is used for literal path segments, and `node.setHandler` (router.go:731) attaches the handler to the terminal node. The `routeMethods.set` (router.go:171) dispatches by HTTP method, storing the handler in the correct method slot.

**Supported by clue:** The call chain `Echo.Add → Echo.add → DefaultRouter.Add → insert → addStaticChild / setHandler` is explicitly documented. The `Echo.add` entry also notes `PRECEDENCE(e → err → paramsCount)`, suggesting the framework tracks parameter count during registration, which is relevant for disambiguation.

### 3. Route Matching: Static Children Are Checked First

The decisive evidence comes from `DefaultRouter.Route` (router.go:791), which "looks up a handler registered for method and path." Its behavior annotation is:

> PRECEDENCE(cap → not_r.useEscapedPathForRouting → currentNode); ACCUMULATE(len loop → searchIndex)

The method calls `findStaticChild` as part of its lookup. The `findStaticChild` function (router.go:709) has behavior `ACCUMULATE(loop → result)` — it iterates over static children looking for a prefix match. Because `Route` invokes `findStaticChild` on the current node, and the node tree separates static children from `paramChild` and `anyChild` (implied by the tree structure), the matching algorithm checks static children **before** falling through to parameter or wildcard children.

**Supported by clue:** `Route` explicitly calls `findStaticChild`. The PRECEDENCE annotation on `Route` lists `currentNode` as part of the priority chain, and the call to `findStaticChild` precedes any parameter/wildcard resolution in the documented call list.

**Uncertain:** The clue does not name `paramChild` or `anyChild` fields explicitly. The existence of these child types is inferred from the fact that the router handles parameters and wildcards, and `findStaticChild` is a *specific* child-lookup (not a generic one). The exact fallback order between paramChild and anyChild is not directly stated.

### 4. The Fallback-to-Any Mechanism in routeMethods

Once a matching node is found, `routeMethods.find` (router.go:213) resolves which handler to invoke. Its behavior is:

> GUARD(r != nil || !fallbackToAny → return r); DISPATCH(method)

This means: if a route method entry exists for the specific HTTP method, return it. If not, and `fallbackToAny` is enabled, fall back to an "any" handler. This is the mechanism behind `Echo.Any()` or method-agnostic routes — they serve as a catch-all when no method-specific handler is registered on that node.

**Supported by clue:** The `fallbackToAny` guard is explicitly annotated. The DISPATCH on method confirms method-level resolution happens after node-level (path) resolution.

### 5. RouteNotFound as a Terminal Fallback

`Echo.RouteNotFound` (echo.go:495) "registers special-case route executed when no other route found." This is the final fallback when the entire tree traversal fails to match any node. It is distinct from wildcard matching — wildcards match path segments during tree traversal, while `RouteNotFound` fires only when no route at all is found.

**Supported by clue:** Directly documented as a "special-case route."

### 6. ConcurrentRouter Delegates Without Altering Precedence

`concurrentRouter.Route` (router_concurrent.go:21) has behavior `DELEGATE(r.router.Route → result); UNWIND(defer)`. It wraps `DefaultRouter.Route` with concurrency safety but does not change the matching logic or precedence rules.

**Supported by clue:** Explicitly a delegation wrapper.

### 7. Static File Handlers Are Regular Routes

`Echo.Static`, `Echo.StaticFS`, `Echo.File`, `Echo.FileFS`, and `StaticDirectoryHandler` (echo.go:559) all register routes through the normal `Add` mechanism. The static middleware (middleware/static.go) is a separate middleware-based approach. Neither introduces special precedence rules — they are just routes in the tree and follow the same static-before-param-before-wildcard ordering.

**Supported by clue:** These are documented as creating handlers/routes, not as modifying router behavior.

## Summary of Precedence Order

Based on the clue evidence, the route resolution order is:

1. **Static segment match** — `findStaticChild` is called first during tree traversal in `DefaultRouter.Route`, checking for exact literal prefix matches among the node's static children.
2. **Parameter segment match** — if no static child matches, the router falls through to parameter children (inferred from tree structure, not explicitly named in the clue).
3. **Wildcard (any) segment match** — the final path-segment fallback (inferred; the `fallbackToAny` in `routeMethods.find` operates at the method level, but an analogous `anyChild` likely exists at the node level).
4. **RouteNotFound** — fires when no route in the tree matches at all.

Within a matched node, `routeMethods.find` resolves method-specific handlers first, then falls back to an "any" handler if `fallbackToAny` is set.

## Confidence Assessment

| Claim | Confidence | Basis |
|---|---|---|
| Router is a radix/prefix tree of nodes | High | `insert`, `addStaticChild`, `findStaticChild` all documented |
| Static children checked before params/wildcards | High | `Route` calls `findStaticChild`; separate child types implied |
| Param children checked before wildcard children | Medium | Inferred from common radix-tree design; not explicitly in clue |
| `fallbackToAny` is method-level, not path-level | High | `routeMethods.find` GUARD annotation is explicit |
| `RouteNotFound` is the terminal fallback | High | Directly documented |
| Static file routes follow same precedence | High | Registered via normal `Add` path |

## Gaps

- The clue does not expose the internal node fields (`paramChild`, `anyChild`, `staticChildren`) by name — only the methods that operate on them.
- `Echo.AcquireContext`, `Echo.NewContext`, `Echo.PreMiddlewares`, `Echo.ReleaseContext` are listed as uncovered; these are context-lifecycle operations and likely do not affect routing precedence.
- The exact algorithm inside `findStaticChild` (longest-prefix-first vs. first-match) is not detailed beyond `ACCUMULATE(loop → result)`.
