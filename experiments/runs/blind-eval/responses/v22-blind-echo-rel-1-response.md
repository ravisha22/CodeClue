# v2.2 Response: blind-echo-rel-1
Date: 2026-04-15

## Question
What are the main relationships among `Echo`, `Group`, `Context`, and handlers during normal request dispatch?

## Answer

### 1. Echo → Group: Ownership & Delegation

`Echo` is the top-level framework instance (echo.go:68). It creates `Group` instances via:

- **`Echo.Group`** (echo.go:659) — "creates a new router group with prefix and optional group-level middleware." It calls `Use` to attach group-level middleware.

`Group` (group.go:14) is described as "a set of sub-routes for a specified route prefix." Every `Group` method mirrors an `Echo` method and delegates back to the `Echo` instance:

- `Group.Add` (group.go:158) — "implements `Echo#Add()` for sub-routes." It calls `AddRoute` (group.go:172), which in turn has behavior `DELEGATE(g.echo.add -> result)` — meaning the Group delegates route registration back to the parent Echo instance's private `add` method.
- All HTTP method shortcuts on Group (`GET`, `POST`, `PUT`, `DELETE`, `HEAD`, `OPTIONS`, `PATCH`, `CONNECT`, `TRACE`) delegate to `Group.Add` (group.go:158), which is called by: `Any`, `CONNECT`, `DELETE`, `GET`, `HEAD`, `OPTIONS`, `PATCH`, `POST` (group.go:158 called_by).
- `Group.Use` (group.go:22) — "implements `Echo#Use()` for sub-routes."
- `Group.StaticFS` (group.go:122), `Group.Static` (group.go:112), `Group.File` (group.go:143), `Group.RouteNotFound` (group.go:153) — all mirror `Echo` counterparts.

**Key relationship:** Group is a thin facade over Echo. Route registration always flows back to `Echo.add` (echo.go:621).

### 2. Echo → Context: Creation, Pooling & Lifecycle

Echo manages the lifecycle of `Context` objects:

- **`Echo.AcquireContext`** (echo.go:684) — "returns an empty `Context` instance from the pool." Behavior: `DELEGATE(e.contextPool.Get -> result)`.
- **`Echo.ReleaseContext`** (echo.go:690) — "returns the `Context` instance back to the pool."
- **`Echo.NewContext`** (echo.go:357) — "returns a new Context instance." Delegates to `newContext`.
- **`Context.Reset`** (context.go:107) — "resets the context after request completes."

There is also a standalone factory: **`NewContext`** (context.go:64) which delegates to `newContext` and accepts variadic options.

### 3. Context ↔ Echo: Bidirectional Reference

- **`Context.Echo`** (context.go:665) — "returns the `Echo` instance." This means every Context holds a back-reference to its owning Echo instance.
- **`Context.Bind`** (context.go:399) — "binds path params, query params and the request body." Behavior: `DELEGATE(c.echo.Binder.Bind -> result)` — the context delegates binding to a Binder owned by Echo.
- **`Context.json`** (context.go:464) — behavior: `DELEGATE(c.echo.JSONSerializer.Serialize -> result)` — serialization is also delegated to an Echo-owned serializer.

### 4. Context ↔ Request/Response: Wrapping HTTP Primitives

Context wraps the raw HTTP request and response:

- **`Context.Request`** (context.go:129) — "returns `*http.Request`."
- **`Context.SetRequest`** (context.go:134) — "sets `*http.Request`."
- **`Context.Response`** (context.go:139) — "returns `*Response`."
- **`Context.Cookie`** (context.go:364) — delegates to `c.request.Cookie`.
- **`Context.Cookies`** (context.go:374) — delegates to `c.request.Cookies`.

### 5. Context ↔ Route: Initialization

- **`Context.InitializeRoute`** (context.go:263) — "sets the route related variables of this request to the context." Calls `PathValues` and `setPathValues`. This is how the matched route information is injected into the context during dispatch.

### 6. Echo → Handlers: Route Registration

Handlers (of type `HandlerFunc`) are registered through:

- **`Echo.Add`** (echo.go:642) — "registers a new route for an HTTP method and path with matching handler." All HTTP shortcuts (`GET`, `POST`, `DELETE`, etc.) delegate to this.
- **`Echo.add`** (echo.go:621) — the private implementation. Behavior: `GUARD(e -> RouteInfo); PRECEDENCE(e -> err)`. Calls `AddRoute`. Called by both `Add` and `AddRoute`.
- **`Echo.GET`** (echo.go:449) — "registers a new GET route for a path with matching handler in the router with optional route-level middleware." Behavior: `DELEGATE(e.Add -> result)`.

### 7. Middleware: Chaining & Execution Order

- **`Echo.Use`** (echo.go:431) — "adds middleware to the chain which is run after router has found matching route and before route/request handler method is called." Called by `Group` and `main`.
- **`applyMiddleware`** (echo.go:785) — behavior: `ACCUMULATE(loop -> result)`. Called by `serveHTTP`. This wraps the handler in the middleware chain.
- Middleware functions have type `MiddlewareFunc` and are accepted at both the Echo level (via `Echo.Use`) and per-route (every route registration method accepts `...MiddlewareFunc`).

### 8. Request Dispatch Flow (from `main` example)

The `main` function (echo.go:24) shows the canonical usage: calls `New`, `GET`, `Use`, and `Start`. The dispatch flow is:

1. **`Echo.ServeHTTP`** / **`Echo.serveHTTP`** (not directly in this clue's FOCUS but referenced via `applyMiddleware`'s `called_by: serveHTTP`) — entry point for HTTP requests.
2. The router finds a matching route and handler.
3. **`applyMiddleware`** (echo.go:785) wraps the matched handler with the middleware chain.
4. **`Context`** is acquired from the pool (`AcquireContext`), initialized with route info (`InitializeRoute`), and passed to the handler chain.
5. The handler receives the `Context` and uses its methods (`Bind`, `json`, `Response`, etc.) to process the request.
6. After the request completes, `Context.Reset` (context.go:107) cleans up, and the context is returned to the pool via `ReleaseContext`.

### 9. Testing Relationship

- **`ContextConfig`** (echotest/context.go:20) — "configuration for creating echo.Context for testing purposes."
- **`ContextConfig.ServeWithHandler`** (echotest/context.go:167) — "serves ContextConfig with given handler and returns httptest.ResponseRecorder." Calls `ToContextRecorder`.
- **`ContextConfig.ToContext`** (echotest/context.go:75) — converts to `echo.Context`. Calls `ToContextRecorder`.
- **`ContextConfig.ToContextRecorder`** (echotest/context.go:81) — converts to `echo.Context` and `httptest.ResponseRecorder`. Called by `ServeWithHandler` and `ToContext`.

### Summary Diagram

```
Echo (echo.go:68)
 ├── owns → Router (routes registered via Echo.add → AddRoute)
 ├── creates → Group (Echo.Group, echo.go:659)
 │    └── delegates route registration → Echo.add (group.go:172 behavior: DELEGATE(g.echo.add))
 ├── pools → Context (AcquireContext / ReleaseContext)
 │    ├── wraps → http.Request, *Response
 │    ├── back-references → Echo (Context.Echo)
 │    ├── delegates binding → Echo.Binder (Context.Bind)
 │    ├── delegates serialization → Echo.JSONSerializer (Context.json)
 │    └── initialized with → RouteInfo (Context.InitializeRoute)
 └── serves requests via:
      serveHTTP → applyMiddleware(handler, middleware...) → handler(Context)
```
