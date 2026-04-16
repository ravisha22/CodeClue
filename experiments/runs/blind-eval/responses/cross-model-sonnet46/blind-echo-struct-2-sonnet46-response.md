# Cross-Model (Sonnet 4.6): blind-echo-struct-2
Date: 2026-04-16

## Question
Which public types and subcomponents make up Echo's routing and request-handling surface?

## Answer

Echo's routing and request-handling surface is composed of several cooperating public types across `echo.go`, `router.go`, `context.go`, and `group.go`.

---

### 1. The Framework Core — `Echo`

> `Echo (echo.go:68-68)` — "Echo is the top-level framework instance." Methods: `AcquireContext, Add, AddRoute, Any, CONNECT, DELETE` [FOCUS, Echo echo.go:68].

`Echo` implements `http.Handler` via `Echo.ServeHTTP (echo.go:695)` [SYM]. Routes are registered through:
- `Echo.Add (echo.go:642)` — "Add registers a new route for an HTTP method and path with matching handler in the router with optional route-level middleware." `GUARD(err != nil -> panic(err))` [SYM, Echo.Add echo.go:642].
- `Echo.AddRoute (echo.go:617)` — "AddRoute registers a new Route with default host Router" [SYM].
- `Echo.Any (echo.go:504)` — "registers a new route for all HTTP methods." `DELEGATE(e.Add -> result)` [FOCUS, Echo.Any echo.go:504].
- Per-method shortcuts `Echo.GET`, `Echo.POST`, `Echo.PUT`, `Echo.DELETE`, `Echo.PATCH`, `Echo.HEAD`, `Echo.OPTIONS`, `Echo.CONNECT`, `Echo.TRACE`, `Echo.RouteNotFound` — all delegate to `Echo.Add` [FOCUS entries].
- `Echo.Use (echo.go:431)` — "Use adds middleware to the chain which is run after router has found matching route and before route/request handler method is executed." [FOCUS, Echo.Use echo.go:431].
- `Echo.Group (echo.go:659)` — "Group creates a new router group with prefix and optional group-level middleware", calls `Use` [FOCUS].

---

### 2. The Router Interface and Default Implementation — `Router`, `DefaultRouter`

> `Router (router.go:21-21)` — "Router is interface for routing request contexts to registered routes." [FOCUS, Router router.go:21].

> `DefaultRouter (router.go:60-60)` — "DefaultRouter is the registry of all registered routes for an Echo instance for request matching and URL path parameter extraction." Methods: `Add, Remove, Route, Routes, insert, storeRouteInfo` [FOCUS, DefaultRouter router.go:60].

---

### 3. Route Sub-grouping — `Group`

> `Group (group.go:14)` — "Group is a set of sub-routes for a specified route prefix." [SYM, Group group.go:14].

All `Group` HTTP-method methods (`Group.GET`, `Group.POST`, `Group.DELETE`, `Group.PATCH`, `Group.HEAD`, `Group.OPTIONS`, `Group.CONNECT`, `Group.TRACE`) delegate to `Group.Add (group.go:158)` [FOCUS entries, e.g. Group.GET group.go:37]. `Group.Any` and `Group.Match` also delegate to `Group.Add` [FOCUS, Group.Any group.go:72; Group.Match group.go:77].

- `Group.Add (group.go:158)` — `GUARD(err != nil -> panic(err))`, calls `AddRoute` [FOCUS, Group.Add group.go:158].
- `Group.AddRoute (group.go:172)` — "AddRoute registers a new Routable with Router" [SYM].
- `Group.StaticFS (group.go:122)` — Implements `Echo#StaticFS()` for sub-routes, delegates to `g.Add` [FOCUS].
- `Group.Use (group.go:22)` — Group-level middleware attachment.

---

### 4. The Per-Request Context — `Context`

> `Context (context.go:40-40)` — "Context represents the context of the current HTTP request." Methods: `Attachment, Bind, Blob, Cookie, Cookies, Echo` [FOCUS, Context context.go:40].

Key accessors on `Context`:
- `Context.Request (context.go:129)` — "Request returns `*http.Request`" [SYM; FOCUS].
- `Context.SetRequest (context.go:134)` — "SetRequest sets `*http.Request`" [SYM; FOCUS].
- `Context.Response (context.go:139)` — "Response returns `*Response`" [SYM].
- `Context.SetResponse (context.go:145)` — "SetResponse sets `*http.ResponseWriter`" [SYM].
- `Context.Get (context.go:380)` — "Get retrieves data from the context" [SYM].
- `Context.Set (context.go:387)` — "Set saves data in the context" [SYM].
- `Context.QueryParam (context.go:287)` — Returns a query param [SYM].
- `Context.FormValue (context.go:319)` — Returns form field value [SYM].
- `Context.Bind (context.go:399)` — "Bind binds path params, query params and the request body." `DELEGATE(c.echo.Binder.Bind -> result)` [FOCUS, Context.Bind context.go:399].
- `Context.Echo (context.go:665)` — "Echo returns the Echo instance" [FOCUS].

---

### 5. Error Handling — `HTTPError`

> `HTTPError (httperror.go:107-107)` — "HTTPError represents an error that occurred while handling a request." Methods: `Error, StatusCode, Unwrap, Wrap` [FOCUS, HTTPError httperror.go:107].

`DefaultHTTPErrorHandler (echo.go:374)` — "creates new default HTTP error handler" [SYM].

---

### 6. Virtual Hosting — `NewVirtualHostHandler`

> `NewVirtualHostHandler (vhost.go:10-10)` — "creates instance of Echo that routes requests to given virtual hosts when hosts in request does not match." `sig: NewVirtualHostHandler(vhosts map[string]*Echo)` [FOCUS].

---

### 7. Testing Support — `echotest` Package

> `ContextConfig (echotest/context.go:20-20)` — "ContextConfig is configuration for creating echo.Context for testing purposes." Methods: `ServeWithHandler, ToContext, ToContextRecorder` [FOCUS, ContextConfig echotest/context.go:20].

---

### Summary

| Type / Symbol | File | Role |
|---|---|---|
| `Echo` | echo.go | Top-level instance, route registry, http.Handler entry point |
| `Router` (interface) | router.go | Route-matching abstraction |
| `DefaultRouter` | router.go | Concrete trie-based router |
| `Group` | group.go | Prefixed sub-router for route grouping |
| `Context` | context.go | Per-request request/response envelope |
| `HTTPError` | httperror.go | Structured error type for handlers |
| `NewVirtualHostHandler` | vhost.go | Virtual-host routing facade |
| `ContextConfig` | echotest/context.go | Test helper for constructing Context |
