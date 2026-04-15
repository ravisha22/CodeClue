# v2.3 Response: blind-echo-rel-1
Date: 2026-04-15

## Summary

During normal request dispatch, `Echo` serves as the top-level instance that owns the router, creates `Context` objects, and applies middleware. `Group` provides a sub-routing mechanism that delegates route registration back to `Echo`. `Context` is the per-request carrier passed to handlers and middleware. Handlers are `HandlerFunc` values wrapped with middleware via `applyMiddleware`. The flow is: `Echo.ServeHTTP` → router match → middleware chain → handler, with `Context` threaded throughout.

## Detailed Analysis

### 1. `Echo` — Owns Everything

- `Echo` (echo.go:68) is "the top-level framework instance" (FOCUS: Echo). It is the central owner of the router, context pool, and middleware chain.
- `Echo.ServeHTTP` (echo.go:695) "implements `http.Handler` interface" (SYM: Echo.ServeHTTP) — this is the entry point for every HTTP request.
- `Echo` creates `Context` instances via `Echo.NewContext` (echo.go:357) with behavior `DELEGATE(newContext -> result)` (FOCUS: Echo.NewContext) and manages a context pool via `Echo.AcquireContext` (echo.go:684) with `DELEGATE(e.contextPool.Get -> result)` and `Echo.ReleaseContext` (echo.go:690) (FOCUS entries).

### 2. `Echo` → Router Relationship

- `Echo` uses `DefaultRouter` (router.go:60) "the registry of all registered routes for an `Echo` instance for request matching and URL path parameter" (FOCUS: DefaultRouter).
- Routes are registered through `Echo.Add` (echo.go:642), which internally calls `Echo.add` (echo.go:621) with behavior `GUARD(e -> RouteInfo); PRECEDENCE(e -> err -> paramsCount)` (FOCUS: Echo.add). `Echo.add` calls the router's `Add` method (FOCUS: Echo.add, calls: `Add`).
- All HTTP verb methods delegate to `Echo.Add`:
  - `Echo.GET` → `DELEGATE(e.Add -> result)` (implied from pattern).
  - Similarly for DELETE, POST, PUT, PATCH, HEAD, OPTIONS, CONNECT, TRACE (SYM entries in echo.go).
- `Echo.AddRoute` (echo.go:617) provides a lower-level alternative with `DELEGATE(e.add -> result)` (FOCUS: Echo.AddRoute).

### 3. `Echo` → `Group` Relationship

- `Echo.Group` (echo.go:659) "creates a new router group with prefix and optional group-level middleware" calling `Use` (FOCUS: Echo.Group).
- `Group` (group.go:14) is "a set of sub-routes for a specified route" (SYM: Group).
- `Group`'s HTTP method shortcuts all delegate back to `Group.Add`:
  - `Group.GET` (group.go:37) — `DELEGATE(g.Add -> result)` (FOCUS: Group.GET).
  - `Group.DELETE` (group.go:32), `Group.POST` (group.go:57), `Group.PUT` (group.go:62), etc. — all same pattern (FOCUS entries).
- `Group.Add` (group.go:158) calls `Group.AddRoute` (FOCUS: Group.Add, calls: `AddRoute`).
- `Group.AddRoute` (group.go:172) "registers a new Routable with Router" — its behavior is `DELEGATE(g.echo.add -> result)` (from the echo-rel-2 prompt's FOCUS), meaning it delegates route registration back to the `Echo` instance's internal `add` method.
- `Group.Use` (group.go:22) "implements `Echo#Use()` for sub-routes within the Group" (FOCUS: Group.Use) — groups can have their own middleware.
- `Group.RouteNotFound` (group.go:153) registers a not-found handler for the group (FOCUS: Group.RouteNotFound).

### 4. `Context` — Per-Request Carrier

- `Context` (context.go:40) "represents the context of the current HTTP request" with methods including `Attachment`, `Bind`, `Blob`, `Cookie`, `Cookies`, `Echo` (FOCUS: Context).
- **Created per request**: `newContext` (context.go:75) is the internal constructor, called by `Echo.NewContext` (FOCUS: NewContext, calls: `newContext`). Also `NewContext` (context.go:64) as a package-level function with behavior `DELEGATE(newContext -> result); ACCUMULATE(loop -> result)` (FOCUS: NewContext at context.go:64).
- **Request/Response access**: `Context.Request` (context.go:129) returns `*http.Request`, `Context.SetRequest` (context.go:134) sets it (called by `newContext`) (FOCUS entries). `Context.Response` (context.go:139) returns `*Response` (SYM entry).
- **Back-reference to Echo**: `Context.Echo` (context.go:665) "returns the `Echo` instance" (FOCUS: Context.Echo) — the context holds a reference to its parent Echo.
- **Route initialization**: `Context.InitializeRoute` (context.go:263) "sets the route related variables of this request to the context" calling `setPathValues` (FOCUS: Context.InitializeRoute).
- **Lifecycle**: `Context.Reset` (context.go:107) "resets the context after request completes" (FOCUS: Context.Reset).

### 5. Context ↔ Handlers

- Handlers receive `Context` and interact with it for:
  - **Input binding**: `Context.Bind` (context.go:399) — `DELEGATE(c.echo.Binder.Bind -> result)` (FOCUS: Context.Bind). Note it delegates to `c.echo.Binder`, showing the Echo→Context→Binder chain.
  - **Response rendering**: `Context.json` (context.go:464) — `DELEGATE(c.echo.JSONSerializer.Serialize -> result)` (FOCUS: Context.json). Also `Context.String`, `Context.Blob`, `Context.File`, `Context.HTMLBlob` (SYM entries).
  - **Data sharing**: `Context.Get`/`Context.Set` (context.go:380/387) for per-request key-value storage (SYM entries).
  - **Cookies**: `Context.Cookie` — `DELEGATE(c.request.Cookie -> result)`, `Context.Cookies` — `DELEGATE(c.request.Cookies -> result)` (FOCUS entries).

### 6. Middleware Ordering and Application

- `Echo.Use` (echo.go:431) "adds middleware to the chain which is run after router has found matching route and before route/request handler" (FOCUS: Echo.Use). This is a critical detail: middleware runs **after** route matching but **before** the handler.
- `applyMiddleware` (echo.go:785) assembles the middleware chain with behavior `ACCUMULATE(loop -> result)` and is called by `serveHTTP` (FOCUS: applyMiddleware, called_by: `serveHTTP`). The accumulation pattern means middleware is wrapped in reverse order, creating a chain where the first registered middleware runs first.
- `Group.Use` (group.go:22) applies middleware at the group level (FOCUS: Group.Use).
- The `main` example (echo.go:24) shows the typical usage: `calls: GET, Start, Use, New` (FOCUS: main) — create Echo, add middleware, register routes, start server.

### 7. Virtual Host Routing

- `NewVirtualHostHandler` (vhost.go:10) "creates instance of Echo that routes requests to given virtual hosts when hosts in request does not" (FOCUS: NewVirtualHostHandler). This allows multiple `Echo` instances to handle different virtual hosts.

### 8. Context Timeout Middleware

- `ContextTimeout` (middleware/context_timeout.go:28) "returns a middleware which returns error (503 Service Unavailable error) to client when underlying method" — this middleware interacts with `Context` by wrapping it with a deadline (FOCUS: ContextTimeout).

### 9. Testing Utilities

- `ContextConfig` (echotest/context.go:20) provides test helpers for creating `Context` objects: `ToContext`, `ToContextRecorder`, `ServeWithHandler` (FOCUS: ContextConfig). `ToContextRecorder` is called by `ServeWithHandler` and `ToContext` (FOCUS: ContextConfig.ToContextRecorder, called_by field).

## Request Dispatch Flow (Synthesized)

1. HTTP request arrives at `Echo.ServeHTTP` (echo.go:695).
2. A `Context` is acquired from the pool (`AcquireContext`) or created.
3. The router (`DefaultRouter.Route`) matches the request to a registered handler.
4. Route info is set on the context via `Context.InitializeRoute`.
5. `applyMiddleware` wraps the handler with the middleware chain (global + route-level).
6. The middleware chain executes, with each middleware receiving `Context` and calling the next.
7. The handler receives `Context`, reads input, writes output.
8. After completion, the context is released back to the pool (`ReleaseContext`).

## Uncertainty / Limits

- The exact `serveHTTP` internal implementation (echo.go) is not shown in FOCUS — the relationship between `ServeHTTP` and the router dispatch is inferred from `applyMiddleware.called_by: serveHTTP`.
- How route-level middleware (passed to `Echo.Add` or `Group.Add`) interacts with global middleware (`Echo.Use`) in the chain ordering is not fully detailed.
- `HandlerFunc` and `MiddlewareFunc` type definitions are not shown as FOCUS entries.
- 45 of 80 L3 symbols have behavior annotations (GAPS section); some dispatch details may be missing.
