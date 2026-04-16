# Cross-Model (Haiku): blind-echo-mech-1
Date: 2026-04-16

## Answer

Echo's route matching algorithm prioritizes routes in this order: **static segments** > **parameters** > **wildcards**. The mechanism is implemented via a trie-based router that processes path segments with precedence rules.

### Route Registration & Node Structure

When routes are added via `Echo.Add()` [Lines 242-248: "Add registers a new route for an HTTP method and path with matching handler in the router" "sig: Echo.Add(method, path string, handler HandlerFunc, middleware ...)" "behavior: GUARD(err != nil -> panic(err))" "calls: add"], the router constructs a trie of nodes where each segment can be:
- **Static**: exact match (highest priority) like `/users/profile`
- **Parameter**: path parameter like `/users/:id` (medium priority)
- **Wildcard**: catch-all like `/files/*` (lowest priority)

### Route Lookup: DefaultRouter.Route()

During request dispatch, `DefaultRouter.Route()` [Lines 254-258 (clue file): "Route looks up a handler registered for method and path" "sig: DefaultRouter.Route(c *Context)" "behavior: PRECEDENCE(cap -> not_r.useEscapedPathForRouting -> currentNode); ACCUMULATE(len loop -> searchIndex)" "calls: findStaticChild, node, find"] walks the request path and searches for matching routes.

The behavior pattern `PRECEDENCE(cap -> not_r.useEscapedPathForRouting -> currentNode)` indicates priority-based evaluation. The function calls `findStaticChild()` first [Lines 278-281 (clue file): "sig: node.findStaticChild(l byte)" "behavior: ACCUMULATE(loop -> result)" "called_by: Remove, Route, findChildWithLabel"], which searches for exact static child node matches before falling back to parameter/wildcard nodes.

### Static Segment Prioritization

`node.findStaticChild()` iterates through child nodes to find exact byte matches [behavior: ACCUMULATE(loop -> result)], implementing O(1) or O(n) lookup depending on node branching. This ensures static segments are evaluated first.

### Parameter Handling

After checking static children, the router checks parameter nodes (`:paramName` format). These are distinct nodes that capture URL segments and store them for access via path values.

### Wildcard Fallback

If neither static nor parameter nodes match, wildcard nodes (`*path`) match remaining path segments as a catch-all.

### HTTP Method Matching

`routeMethods.find()` [Lines 273-276 (clue file): "sig: routeMethods.find(method string, fallbackToAny bool)" "behavior: GUARD(r != nil || !fallbackToAny -> return r); DISPATCH(method)" "called_by: Remove, Route"] implements method matching with fallback-to-ANY support, allowing routes registered with `Echo.Any()` to match any HTTP method [Line 152-156 (clue file): "Echo.Any registers a new route for all HTTP methods" "behavior: DELEGATE(e.Add -> result)" "calls: Add"].

### Storage & Lookup

The `DefaultRouter.storeRouteInfo()` method [Lines 283-286 (clue file): "sig: DefaultRouter.storeRouteInfo(ri RouteInfo)" "behavior: ACCUMULATE(loop -> result)"] accumulates route information for reverse URL generation and introspection.

In summary: **Static routes win** when an exact path segment matches, **parameters are checked next** if no static child exists, and **wildcards match last** as a fallback. This ensures deterministic, predictable routing where more specific routes take precedence over generic ones.
