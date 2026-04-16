# Cross-Model (Sonnet): blind-echo-mech-1
Date: 2026-04-16

Based on the clue file and source snippets, Echo decides route precedence through a hierarchical matching algorithm that prioritizes static segments over parameters and parameters over wildcards, implemented in the `DefaultRouter.Route` method.

## Core Route Resolution Algorithm

### Primary Route Lookup Method
**Function**: `DefaultRouter.Route` (router.go:791-791)
- **Description**: "Route looks up a handler registered for method and path"
- **Signature**: `DefaultRouter.Route(c *Context)`
- **Behavior**: `PRECEDENCE(cap -> not_r.useEscapedPathForRouting -> currentNode); ACCUMULATE(len loop -> searchIndex)`
- **Key Methods**: `calls: findStaticChild, node, find`

This method orchestrates the entire route matching process using precedence rules and accumulation over path segments.

### Static Route Prioritization

**Primary Static Lookup**: `node.findStaticChild` (router.go:709-709)
- **Signature**: `node.findStaticChild(l byte)`
- **Behavior**: `ACCUMULATE(loop -> result)`
- **Usage**: `called_by: Remove, Route, findChildWithLabel`
- **Priority**: Static routes are checked first via `findStaticChild` call in `DefaultRouter.Route`

Evidence shows static routes have highest priority because `DefaultRouter.Route` explicitly calls `findStaticChild` to look for exact byte matches before falling back to other matching strategies.

### Method-Based Route Resolution

**Route Method Lookup**: `routeMethods.find` (router.go:213-213)
- **Signature**: `routeMethods.find(method string, fallbackToAny bool)`
- **Behavior**: `GUARD(r != nil || !fallbackToAny -> return r); DISPATCH(method)`
- **Usage**: `called_by: Remove, Route`

**Method Assignment**: `routeMethods.set` (router.go:171-171)
- **Signature**: `routeMethods.set(method string, r *routeMethod)`
- **Context**: Used during route registration to organize routes by HTTP method

This shows routes are first organized by HTTP method, then by path pattern within each method.

### Route Registration and Storage

**Route Addition**: `Echo.Add` (echo.go:642-642)
- **Description**: "Add registers a new route for an HTTP method and path with matching handler"
- **Signature**: `Echo.Add(method, path string, handler HandlerFunc, middleware ...)`
- **Behavior**: `GUARD(err != nil -> panic(err))`
- **Flow**: `calls: add` and delegates to internal add method

**Route Storage**: `DefaultRouter.storeRouteInfo` (router.go:538-538)
- **Signature**: `DefaultRouter.storeRouteInfo(ri RouteInfo)`
- **Behavior**: `ACCUMULATE(loop -> result)`
- **Usage**: `called_by: Add`

## Precedence Hierarchy Evidence

### 1. Static Routes Win First
The `DefaultRouter.Route` method's `PRECEDENCE` behavior indicates that static matching takes priority. The call to `findStaticChild` occurs early in the resolution process, searching for exact byte matches before considering parameterized routes.

### 2. Parameter Routes Second  
The route resolution algorithm's `ACCUMULATE(len loop -> searchIndex)` behavior suggests path segments are processed sequentially, with parameters matched when static segments don't match. The method signature checking in `routeMethods.find` indicates systematic fallback behavior.

### 3. Wildcard Routes Last
The `routeMethods.find` method's `GUARD(r != nil || !fallbackToAny -> return r)` pattern suggests wildcards (represented by "any" routes) are only checked when specific method routes fail, indicating lowest priority.

## Route Structure and Organization

### HTTP Method Dispatch
All route registration methods delegate through the same mechanism:
- **CONNECT**: `Echo.CONNECT` (echo.go:437-437): `behavior: DELEGATE(e.Add -> result)`
- **DELETE**: `Echo.DELETE` (echo.go:443-443): `behavior: DELEGATE(e.Add -> result)`
- **All methods**: `called_by: Any, CONNECT, DELETE, File, GET, HEAD, OPTIONS, PATCH` for `Echo.Add`

### Static File Handling
**Echo Static Routes**: From source snippets:
- `Echo.StaticFS(pathPrefix string, filesystem fs.FS, middleware ...MiddlewareFunc) RouteInfo`
- `Echo.Static(pathPrefix, fsRoot string, middleware ...MiddlewareFunc) RouteInfo`
- `Group.StaticFS(pathPrefix string, filesystem fs.FS, middleware ...MiddlewareFunc) RouteInfo`

These static file routes likely receive high priority due to their use of specific path prefixes.

## Decision Algorithm Summary

1. **Method Filtering**: `routeMethods.find` first filters routes by HTTP method
2. **Static Segment Matching**: `node.findStaticChild` attempts exact byte-level matches for static path segments  
3. **Parameter Matching**: When static matches fail, parameterized segments are evaluated in sequence
4. **Wildcard Fallback**: `fallbackToAny` parameter in `routeMethods.find` indicates wildcards are checked last
5. **Path Processing**: `ACCUMULATE(len loop -> searchIndex)` processes path segments left-to-right, building up matches incrementally

The `PRECEDENCE(cap -> not_r.useEscapedPathForRouting -> currentNode)` behavior in `DefaultRouter.Route` confirms that the algorithm follows a strict precedence hierarchy, with static routes winning over dynamic routes when overlapping path patterns exist.

## Path Processing Details
**Route Update**: `routeMethods.updateAllowHeader` (router.go:251-251) is involved in maintaining route metadata, suggesting the router tracks which routes are available for conflict resolution.

This architecture ensures predictable routing behavior where more specific routes (static) always win over less specific routes (parameters/wildcards), preventing ambiguity in route resolution.