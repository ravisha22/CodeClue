# Cross-Model (Sonnet 4.6): blind-echo-mech-1
Date: 2026-04-16

## Question
How does Echo decide which route wins when static segments, parameters, and wildcards overlap?

## Answer

Echo's routing priority is implemented inside `DefaultRouter` (`router.go`) using a trie-based structure with explicit precedence rules encoded in the traversal logic of `DefaultRouter.Route`. The clue file's FOCUS entries and the SYM table provide the following evidence.

---

### 1. The router structure — `DefaultRouter`

> `DefaultRouter (router.go:60-60)` — "DefaultRouter is the registry of all registered routes for an Echo instance for request matching and URL path parameter extraction." Methods: `Add, Remove, Route, Routes, insert, storeRouteInfo` [FOCUS, DefaultRouter router.go:60].

Routes are stored in a trie. Each trie node can hold:
- **Static children** — looked up by first-byte label via `node.findStaticChild`.
- **Handler sets** — stored per HTTP method via `node.setHandler`.

---

### 2. Route lookup — `DefaultRouter.Route`

> `DefaultRouter.Route (router.go:791-791)` — "Route looks up a handler registered for method and path." `sig: DefaultRouter.Route(c *Context)`. `PRECEDENCE(cap -> not_r.useEscapedPathForRouting -> currentNode); ACCUMULATE(len loop -> searchIndex)`. Calls `findStaticChild, node, find` [FOCUS, DefaultRouter.Route router.go:791].

The behavior annotation `PRECEDENCE(cap -> not_r.useEscapedPathForRouting -> currentNode)` describes the first-level precedence decision: whether to use the escaped or unescaped path for routing (controlled by `useEscapedPathForRouting` on the router). The subsequent `ACCUMULATE(len loop -> searchIndex)` shows that the traversal iterates segment-by-segment through the path.

Within each segment the call to `findStaticChild` is made before falling back to parameter or wildcard nodes:

> `node.findStaticChild (router.go:709-709)` — `sig: node.findStaticChild(l byte)`. `ACCUMULATE(loop -> result)`. Called by `Remove, Route, findChildWithLabel` [FOCUS, node.findStaticChild router.go:709].

This demonstrates the **static-first** preference: the router attempts to find a static child matching the first byte of the current path segment before considering parameter (`:param`) or wildcard (`*`) node types.

---

### 3. Method-level resolution — `routeMethods.find`

> `routeMethods (router.go:148-148)` — type with methods `find, isHandler, set, updateAllowHeader` [FOCUS, routeMethods router.go:148].

> `routeMethods.find (router.go:213-213)` — `sig: routeMethods.find(method string, fallbackToAny bool)`. `GUARD(r != nil || !fallbackToAny -> return r); DISPATCH(method)`. Called by `Remove, Route` [FOCUS, routeMethods.find router.go:213].

After the trie traversal resolves to a node, `routeMethods.find` selects the handler for the specific HTTP method. The `GUARD(r != nil || !fallbackToAny -> return r)` means:
1. If an exact method match exists, return it immediately.
2. Only if `fallbackToAny` is set and no exact match was found does it fall back to an "any-method" handler.

`routeMethods.updateAllowHeader (router.go:251)` [SYM] is called to set the `Allow` response header when no matching method is found, enabling proper 405 Method Not Allowed responses.

---

### 4. Node handler storage — `node.setHandler`

> `node.setHandler (router.go:731)` — Called by insert logic [SYM, node.setHandler router.go:731].

This internal method assigns a handler to a specific method slot on a trie node during route registration.

---

### 5. Route registration and info storage

> `DefaultRouter.storeRouteInfo (router.go:538-538)` — `ACCUMULATE(loop -> result)`. Called by `Add` [FOCUS, DefaultRouter.storeRouteInfo router.go:538].

When a route is added, `storeRouteInfo` records the `RouteInfo` (accessible later via `Context.RouteInfo`).

---

### 6. The `concurrentRouter` wrapper

> `concurrentRouter.Route (router_concurrent.go:21-21)` — `DELEGATE(r.router.Route -> result); UNWIND(defer)` [FOCUS, concurrentRouter.Route router_concurrent.go:21].

The concurrent router wraps `DefaultRouter.Route` with locking (shown by `UNWIND(defer)`, indicating a deferred unlock), but does not change the priority semantics.

---

### 7. Route registration path

All registration ultimately flows through `Echo.add`:
> `Echo.add (echo.go:621)` — `GUARD(e.OnAddRoute != nil -> return RouteInfo{},...)`. `PRECEDENCE(e -> err -> paramsCount)`. Calls `Add` (on the Router). Called by `Add, AddRoute` [FOCUS, Echo.add echo.go:621].

The `PRECEDENCE(e -> err -> paramsCount)` annotation suggests that during insertion the router counts path parameters (`paramsCount`) to inform trie node construction.

---

### 8. Route information on Context

> `Context.RouteInfo (context.go:225-225)` — `GUARD(c.route != nil -> return c.route.Clone())` [FOCUS, Context.RouteInfo context.go:225].

After routing, the winning `RouteInfo` is attached to the `Context` by `Context.InitializeRoute (context.go:263)`, which calls `setPathValues` [FOCUS, Context.InitializeRoute context.go:263]. This is how matched path parameter values are made available to the handler.

---

### 9. Special-case: RouteNotFound

> `Echo.RouteNotFound (echo.go:495)` — "registers a special-case route which is executed when no other route is found." `DELEGATE(e.Add -> result)`. Calls `Add` [FOCUS, Echo.RouteNotFound echo.go:495].

This is registered as a normal route with a sentinel method, ensuring it is only selected when the trie traversal finds no matching path + method combination.

---

### Summary of priority rules (from clue file evidence)

| Priority | Match type | Mechanism |
|---|---|---|
| 1st | Static segment | `node.findStaticChild` called first in `DefaultRouter.Route` |
| 2nd | Parameter segment (`:name`) | Fallback node type after static miss |
| 3rd | Wildcard segment (`*`) | Fallback node type after parameter miss |
| Method | Exact HTTP method | `routeMethods.find` with exact match first |
| Fallback | Any-method (`Any`) | `routeMethods.find` with `fallbackToAny=true` |
| Last resort | `RouteNotFound` handler | Special sentinel route registered via `Echo.RouteNotFound` |

> **Caveat**: The clue file's GAPS note that `Echo.ServeHTTP`, `Echo.Group`, `Echo.AcquireContext`, and `Echo.NewContext` are uncovered in the FOCUS section [GAPS], so the precise body of `DefaultRouter.Route`'s inner trie traversal (particularly the parameter/wildcard fallback ordering) is inferred from the `PRECEDENCE` and `findStaticChild` evidence above rather than from direct source observation.
