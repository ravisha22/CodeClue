# v2.5 Response: rel-fiber-1
Date: 2026-04-16

## Question
What is the relationship between the App struct, Router, and Route types in Fiber, and how do they connect?

## Answer

### The Three Core Types

**`App`** (FOCUS: `App` at `app.go:69-69`) — "App denotes the Fiber application." It has methods: `Add`, `All`, `Config`, `Connect`, `Delete`, `Domain`. The App is the central orchestrator, owning routing logic directly via methods defined on it in `router.go`.

**`Router`** (FOCUS: `Router` at `router.go:18-19`) — "Router defines all router handle interface, including app and group router." This is an **interface**, not a struct. It defines the contract that both `App` and `Group` implement.

**`Route`** (FOCUS: `Route` at `router.go:45-46`) — "Route is a struct that holds all metadata for each registered handler." It has a `match` method.

### How App Implements Router

The `App` struct has routing methods that match the `Router` interface pattern:

- **`App.Add`** (SYM: `App.Add` at `app.go:953`) — "Add allows you to specify multiple HTTP methods." This is the primary route registration method.
- **`App.Connect`** (FOCUS: `App.Connect` at `app.go:929`) — Registers CONNECT routes. Behavior: `DELEGATE(app.Add -> result)` — it delegates to `App.Add`.
- **`App.Route`** (FOCUS: `App.Route` at `app.go:1024`) — Defines routes with a common prefix. Takes a function `fn func(router Router)`, calls `Group` and `Name`. Panics if `fn` is nil.
- **`App.Name`** (SYM: `App.Name` at `app.go:783`) — Assigns name to specific route.

### Route Registration Chain: App → register → addRoute

The registration flow is:

1. **`App.Add`** and other HTTP method shortcuts (like `App.Connect`) ultimately call **`App.register`** (FOCUS: `App.register` at `router.go:513`):
   - Signature: `App.register(methods []string, pathRaw string, group *Group, handlers...)`
   - Behavior: Panics if no handlers and no group. Iterates methods, calls `methodInt` and `addRoute`.
   - Called by: `Add`, `Group`, `Use`, `All`, `mount` (FOCUS `called_by`).

2. **`App.addRoute`** (FOCUS: `App.addRoute` at `router.go:590`):
   - Signature: `App.addRoute(method string, route *Route)`
   - Called by: `register`.
   - Calls: `methodInt`, `pruneAutoHeadRouteLocked`.
   - Can panic.

3. **`App.pruneAutoHeadRouteLocked`** (FOCUS: `App.pruneAutoHeadRouteLocked` at `router.go:491`):
   - Removes automatically generated HEAD routes so explicit registrations can replace them.
   - Calls: `methodInt`, `normalizePath`.
   - Called by: `addRoute`, `deleteRoute`.

### Route Deletion Chain

- **`App.RemoveRoute`** (FOCUS: `App.RemoveRoute` at `router.go:417`) — Removes route by path. Calls `deleteRoute` and `normalizePath`.
- **`App.RemoveRouteByName`** (FOCUS: `App.RemoveRouteByName` at `router.go:430`) — Removes route by name. Calls `deleteRoute`.
- **`App.RemoveRouteFunc`** (FOCUS: `App.RemoveRouteFunc` at `router.go:439`) — Removes route by custom match function. Calls `deleteRoute`.
- **`App.deleteRoute`** (FOCUS: `App.deleteRoute` at `router.go:443`) — The shared implementation. Behavior: iterates methods via `ToUpper`, calls `methodInt` and `pruneAutoHeadRouteLocked`. Called by all three removal methods.

### Request Dispatch: App.next / App.nextCustom

When a request arrives, the App dispatches it through:

- **`App.next`** (FOCUS: `App.next` at `router.go:115`) — Dispatches for `*DefaultCtx`. Behavior: `PRECEDENCE(not_ok -> c -> exists); ACCUMULATE(match loop -> result)`. Calls `Next`, `Append`, `match`. Called by: `Retry`, `serverErrorHandler`, `Next`, `RestartRouting`, `requestHandler`.

- **`App.nextCustom`** (FOCUS: `App.nextCustom` at `router.go:216`) — Dispatches for `CustomCtx`. Behavior: similar precedence/accumulate pattern. Calls `Next`, `Path`, `getDetectionPath`, `getIndexRoute`, `getMatched`, `getMethodInt`, `getSkipNonUseRoutes`, `getTreePathHash`. Called by: `serverErrorHandler`, `Next`, `RestartRouting`, `requestHandler`.

Both methods iterate through routes using `match` to find matching handlers.

### Route.match

The `Route` struct's `match` method (FOCUS: `Route` at `router.go:45-46`, methods: `match`) is called during dispatch by `App.next` to determine if a route matches the current request.

### App.ensureAutoHeadRoutesLocked

**`App.ensureAutoHeadRoutesLocked`** (FOCUS: `App.ensureAutoHeadRoutesLocked` at `router.go:629-630`) — Auto-generates HEAD routes unless `DisableHeadAutoRegister` is set. Calls `methodInt`. Called by `startupProcess` and `ensureAutoHeadRoutes`. Can panic.

### Group as Another Router Implementation

**`Group`** also implements the `Router` interface pattern:
- `Group.Add` (SYM: `Group.Add` at `group.go:167`) — "Add allows you to specify multiple HTTP methods."
- `Group.Connect` (FOCUS: `Group.Connect` at `group.go:143`) — Delegates to `grp.Add`.
- `Group.Name` (SYM: `Group.Name` at `group.go:27`) — Names a route or group.

Groups are created via `App.Route` (FOCUS: `App.Route` at `app.go:1024`) which calls `Group`.

### domainRouter as Domain-Scoped Router

**`domainRouter`** provides domain-based routing:
- `domainRouter.Add` (SYM: `domain.go:530`) — "Add allows you to specify multiple HTTP methods."
- `domainRouter.Connect` (FOCUS: `domain.go:506`) — Delegates to `d.Add`.
- `domainRouter.Route` (FOCUS: `domain.go:584`) — Defines routes with common prefix, same pattern as `App.Route`.
- `domainRouter.Use` (FOCUS: `domain.go:350`) — Registers middleware. Calls `register`.
- `domainRouter.mount` (FOCUS: `domain.go:403`) — Mounts sub-apps at a prefix.
- `domainRouter.RouteChain` (FOCUS: `domain.go:575`) — Creates a `Registering` instance.

### Registering Type

**`Registering`** (SYM: `Registering.Add` at `register.go:111`) provides a chainable registration API:
- `Registering.Add` — "Add allows you to specify multiple HTTP methods."
- `Registering.Connect` (FOCUS: `register.go:87`) — Delegates to `r.Add`.

### Sub-App Mounting

**`App.mount`** (FOCUS: `App.mount` at `mount.go:42`) — Attaches another app instance as a sub-router. Calls `register`. Called by `Use`. Can panic.

**`App.addPrefixToRoute`** (FOCUS: `App.addPrefixToRoute` at `router.go:355`) — Adds prefix to route. Called by `processSubAppsRoutes`.

**`App.MountPath`** (FOCUS: `App.MountPath` at `mount.go:103-104`) — Returns the pattern where the app was mounted.

### Context → Route Access

- `DefaultCtx.Route` (FOCUS: `DefaultCtx.Route` at `ctx.go:355-356`) — Returns the matched `Route` struct. Behavior: `GUARD(c.route == nil -> return &Route{)` — returns empty route if none matched.
- `DefaultReq.Route` (FOCUS: `DefaultReq.Route` at `req.go:1002`) — Delegates to `r.c.Route`.
- `Redirect.Route` (FOCUS: `Redirect.Route` at `redirect.go:339`) — Redirects to a named route.
- `DefaultCtx.App` / `DefaultReq.App` / `DefaultRes.App` (FOCUS entries) — All provide access back to the App from the context.

### RoutePatternMatch

`RoutePatternMatch` (FOCUS: `RoutePatternMatch` at `path.go:155`) — Standalone function to check if a path matches a Fiber route pattern.

### Adaptor Integration

`FiberApp` (FOCUS: `FiberApp` at `middleware/adaptor/adaptor.go:204`) — Wraps a `fiber.App` to a `net/http` handler func, bridging the routing to standard Go HTTP.

### Summary Relationship Diagram

```
Router (interface, router.go:18-19)
├── App (app.go:69) — owns routing methods
│   ├── App.register → App.addRoute → Route
│   ├── App.next / App.nextCustom → Route.match (dispatch)
│   ├── App.mount (mount.go) → register
│   └── App.Route → Group
├── Group (group.go) — scoped route registration
│   └── Group.Add → (delegates to App.register)
├── domainRouter (domain.go) — domain-scoped routing
│   └── domainRouter.Add, Use, mount → register
└── Registering (register.go) — chainable API
    └── Registering.Add

Route (router.go:45-46) — metadata struct
├── Created by register/addRoute
├── Matched by App.next via Route.match
└── Accessed via DefaultCtx.Route
```

### What Cannot Be Determined

Per GAPS: "uncovered: DefaultCtx.RestartRouting, domainRouter.Head, domainRouter.Options, domainRouter.Patch." The full implementations of `Head`, `Options`, `Patch` and other HTTP method shortcuts on `domainRouter` are not in the clue. The internal structure of the routing tree (`RebuildTree` internals) is listed in the INDEX but not in FOCUS.
