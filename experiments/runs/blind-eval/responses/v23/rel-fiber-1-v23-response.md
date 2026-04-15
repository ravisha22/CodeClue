# v2.3 Response: rel-fiber-1
Date: 2026-04-15

## Summary

The `App` struct is the top-level Fiber application that owns route registration, grouping, and lifecycle. `Router` is an interface that defines the common routing API shared by `App` and `Group`. `Route` is a metadata struct for each registered handler. They connect through a layered system: `App` (and `Group`) implement the `Router` interface, registering `Route` structs via internal methods like `addRoute` and `deleteRoute` in `router.go`. Domain-based routing adds a parallel `domainRouter` that mirrors the same API.

---

## The `App` Struct

- **`App`** (app.go:69): "denotes the Fiber application" with methods: `Add`, `All`, `Config`, `Connect`, `Delete`, `Domain` (FOCUS entry).
- **`App.Add`** (app.go:953, SYM): "allows you to specify multiple HTTP methods" — the core method for registering routes on the application.
- **`App.Head`** (app.go:906, FOCUS): "registers a route for HEAD methods"; behavior is `DELEGATE(app.Add -> result)`, meaning it delegates to `App.Add`.
- **`App.Connect`** (app.go:929, FOCUS): "registers a route for CONNECT methods"; also `DELEGATE(app.Add -> result)`.
- **`App.Route`** (app.go:1024, FOCUS): "used to define routes with a common prefix inside the supplied function"; calls `Group` and `Name`, with `GUARD(fn -> raise_panic)` behavior — panics if `fn` is nil.
- **`DefaultCtx.App`** (ctx.go:102), **`DefaultReq.App`** (req.go:83), **`DefaultRes.App`** (res.go:134): All return `*App` references, showing that `App` is accessible throughout the request lifecycle.

## The `Router` Interface

- **`Router`** (router.go:18-19, FOCUS): "defines all router handle interface, including app and group router." This is the shared interface that both `App` and `Group` implement.
- The existence of identical method signatures across `App`, `Group`, and `domainRouter` (all having `.Add`, `.Connect`, etc.) confirms that `Router` is the common contract.

## The `Route` Struct

- **`Route`** (router.go:45-46, FOCUS): "a struct that holds all metadata for each registered handler" with method `match`.
- **`Route.match`** (router.go:68, FOCUS): `sig: Route.match(detectionPath, path string, params *[maxParams]string)` — performs path matching with behavior `GUARD(r -> value); PRECEDENCE(r -> len)`. Called by `next` and `nextCustom`, indicating it's the core path-matching mechanism in the request dispatch pipeline.
- **`DefaultCtx.Route`** (ctx.go:355-356, FOCUS): "returns the matched Route struct" with `GUARD(c -> Route)` behavior; called by `FullPath`.
- **`DefaultReq.Route`** (req.go:1002, FOCUS): "returns the matched Route struct"; delegates to `r.c.Route` and is called by `Params`.

## How They Connect

### Route Registration Pipeline

1. **HTTP method helpers delegate to `Add`**: `App.Head` → `App.Add` (app.go:906→953); `App.Connect` → `App.Add` (app.go:929→953); same pattern for `Group.Add` (group.go:167) and `Registering.Add` (register.go:111).

2. **`App.addRoute`** (router.go:590, FOCUS): `sig: App.addRoute(method string, route *Route)` — adds a `Route` to the app's internal route table. Called by `register` (the internal registration function). Calls `pruneAutoHeadRouteLocked`. Has `UNWIND(defer)` behavior and can raise panic.

3. **`App.addPrefixToRoute`** (router.go:355, FOCUS): `sig: App.addPrefixToRoute(prefix string, route *Route)` — prefixes a route's path, used when mounting sub-apps or groups.

### Route Deletion Pipeline

- **`App.deleteRoute`** (router.go:443, FOCUS): `sig: App.deleteRoute(methods []string, matchFunc func(r *Route))` — removes routes matching a predicate. Accumulates results in a loop and uses deferred cleanup. Called by three higher-level methods:
  - **`App.RemoveRoute`** (router.go:417, FOCUS): Removes by path; calls `deleteRoute` and `normalizePath`.
  - **`App.RemoveRouteByName`** (router.go:430, FOCUS): Removes by name; calls `deleteRoute`.
  - **`App.RemoveRouteFunc`** (router.go:439, FOCUS): Removes by custom match function; calls `deleteRoute`.

### Auto-HEAD Route Management

- **`App.pruneAutoHeadRouteLocked`** (router.go:491, FOCUS): "removes an automatically generated HEAD route so a later explicit registration can take its place." Called by both `addRoute` and `deleteRoute`, ensuring HEAD routes stay consistent. Calls `normalizePath`.
- **`App.ensureAutoHeadRoutesLocked`** (router.go:629-630, FOCUS): Ensures auto HEAD routes exist; called by `ensureAutoHeadRoutes`. Has `GUARD(app -> none)` and can raise panic.

### Path Normalization

- **`App.normalizePath`** (router.go:398, FOCUS): Delegates to `RemoveEscapeChar`; called by `RemoveRoute` and `pruneAutoHeadRouteLocked`.
- **`RoutePatternMatch`** (path.go:155, FOCUS): "reports whether path matches the provided Fiber route pattern"; calls `RemoveEscapeCharBytes`, `parseRoute`, `getMatch`, `reset`.

### Group-Based Routing

- **`App.Route`** (app.go:1024, FOCUS): Creates a group with a prefix; calls `Group` and `Name`.
- **`Group.Add`** (group.go:167, SYM): Same route registration for groups.
- **`Group.Connect`** (group.go:143, FOCUS): Delegates to `grp.Add`.
- **`Group.mount`** (mount.go:73, FOCUS): Mounts sub-apps within groups; accumulates results with `PRECEDENCE(groupPath -> err)`.

### Mounting / Sub-Applications

- **`App.mount`** (mount.go:42, FOCUS): "Mount attaches another app instance as a sub-router along a routing path." Accumulates routes with prefix adjustment; can raise panic.
- **`App.MountPath`** (mount.go:103-104, FOCUS): "returns the route pattern where the current app instance was mounted."
- **`domainRouter.mount`** (domain.go:403, FOCUS): "mount attaches a sub-app instance to the domain router at the specified prefix"; calls `Name` and `wrapHandlers`.

### Domain-Based Routing (Parallel Hierarchy)

- **`domainRouter.Add`** (domain.go:530, SYM/FOCUS): Same `Add` pattern for domain-scoped routes.
- **`domainRouter.Connect`** (domain.go:506, FOCUS): Delegates to `d.Add`.
- **`domainRouter.Route`** (domain.go:584, FOCUS): Same grouped route pattern as `App.Route`; calls `Group` and `Name`.
- **`domainRouter.RouteChain`** (domain.go:575, FOCUS): Creates a `Registering` instance; calls `registerPath`.
- **`domainRouter.registerPath`** (domain.go:327): Returns the full path for registration.
- **`domainRouter.registerGroup`** (domain.go:336): Returns the group for association.
- **`domainRouter.Name`** (domain.go:602): Assigns name to the most recently registered route.
- **`domainRouter.wrapHandlers`** (domain.go:278): Wraps handlers in the slice with domain-specific logic.
- **`domainRegistering`** (domain.go:623-624, FOCUS): "provides route registration helpers for a specific path on a domain router, implementing the [Register..." with methods `Add`, `All`, `Connect`, `Delete`, `Get`, `Head`.

### Registration Interface

- **`Register`** (register.go:8-9, FOCUS): "defines all router handle interface generate by RouteChain()."
- **`Registering.Add`** (register.go:111, SYM): Route registration on the Registering type.
- **`Registering.Connect`** (register.go:87, FOCUS): Delegates to `r.Add`.
- **`Registering.All`** (register.go:50, FOCUS): "registers a middleware route that will match requests."

### Handler Adaptation

- **`FiberApp`** (middleware/adaptor/adaptor.go:204, FOCUS): "wraps fiber app to net/http handler func" — delegates to `handlerFunc`, showing `App` can be bridged to `net/http`.

### Hooks

- **`Hooks`** (hooks.go:35, FOCUS): "a struct to use it with App" with methods `OnFork`, `OnGroup`, `OnGroupName`, `OnListen`, `OnMount`, `OnName` — lifecycle events tied to App and routing changes.

### Application State

- **`State`** (state.go:21, FOCUS): "a key-value store for Fiber's app" — global storage accessible via `App`.
- **`ListenConfig`** (listen.go:44-45, FOCUS): Startup configuration struct.

---

## Relationship Diagram (textual)

```
Router (interface, router.go:18)
  ├── App (app.go:69) ──implements──> Router
  │     ├── .Add() ──calls──> addRoute(router.go:590) ──creates──> Route (router.go:45)
  │     ├── .Route() ──calls──> Group()
  │     ├── .mount() ──attaches──> sub-App
  │     ├── .deleteRoute() ──removes──> Route
  │     └── .RemoveRoute/ByName/Func ──calls──> deleteRoute
  │
  ├── Group (group.go) ──implements──> Router
  │     ├── .Add() ──route registration
  │     └── .mount() ──sub-app mounting
  │
  └── domainRouter (domain.go) ──parallel hierarchy
        ├── .Add() ──domain-scoped routes
        ├── .Route() ──grouped routes
        └── .mount() ──sub-app mounting

Route (router.go:45)
  └── .match() ──called by──> next, nextCustom (request dispatch)
  └── accessed via DefaultCtx.Route() / DefaultReq.Route()
```

---

## Uncertainty / Limits

- The `Router` interface (router.go:18-19) is described only briefly; its full method set is not enumerated in the clue file.
- The `register` function (called_by entry for `addRoute`) is not shown in FOCUS, so the exact mechanism linking `App.Add` to `addRoute` is inferred but not directly visible.
- The `next` and `nextCustom` functions (called_by for `Route.match`) are not detailed, so the full request dispatch flow from incoming request to matched Route is partially opaque.
- `Colors` (color.go:8-9) and `Bind.URI` (bind.go:352) appear in FOCUS but their relationship to App/Router/Route is tangential.
- 132 more modules and 1400 more symbols are not shown.
