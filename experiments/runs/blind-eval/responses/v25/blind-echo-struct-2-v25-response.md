# v2.5 Response: blind-echo-struct-2
Date: 2026-04-16

## Question

Which public types and subcomponents make up Echo's routing and request-handling surface?

---

## Answer

Echo's routing and request-handling surface is composed of a set of interrelated public types — `Echo`, `DefaultRouter`/`Router`, `Group`, `Context`, `Response`, `HTTPError`, and several supporting constructs — spread across a small number of core source files. Below is a detailed inventory, citing only the clue entries provided.

---

### 1. `Echo` — Top-Level Framework Instance

**Source:** `echo.go:68`
**FOCUS description:** "top-level framework instance"

`Echo` is the central orchestrator. Its routing and request-handling surface includes:

#### 1.1 Instance Creation

- **`New`** (echo.go:333) — creates a new `Echo` instance. This is the primary public constructor.

#### 1.2 Route Registration — Verb Methods

All HTTP-verb methods DELEGATE to a single canonical registrar:

| Method | Location | Behavior |
|---|---|---|
| `Echo.Add` | echo.go:642 | "registers route for HTTP method"; calls internal `add`; **panics on error**. Called by: `Any`, `CONNECT`, `DELETE`, `File`, `GET`, `HEAD`, `OPTIONS`, `PATCH`. |
| `Echo.AddRoute` | echo.go:617 | Registers a `Route` with the default host Router; calls `add`. |
| `Echo.add` | echo.go:621 | Internal helper. Behavior: GUARD(`e.OnAddRoute != nil`), PRECEDENCE; calls `Add` on `DefaultRouter`. |
| `Echo.GET` | echo.go | DELEGATES to `e.Add` |
| `Echo.POST` | echo.go | DELEGATES to `e.Add` |
| `Echo.PUT` | echo.go | DELEGATES to `e.Add` |
| `Echo.DELETE` | echo.go | DELEGATES to `e.Add` |
| `Echo.PATCH` | echo.go | DELEGATES to `e.Add` |
| `Echo.HEAD` | echo.go | DELEGATES to `e.Add` |
| `Echo.TRACE` | echo.go | DELEGATES to `e.Add` |
| `Echo.CONNECT` | echo.go | DELEGATES to `e.Add` |
| `Echo.Any` | echo.go:504 | Registers a route for **all** HTTP methods. |
| `Echo.Match` | echo.go | Registers a route for a caller-specified set of methods; DELEGATES to `e.Add`. |

The delegation chain is: **verb method → `Echo.Add` → `Echo.add` → `DefaultRouter.Add`**.

#### 1.3 Middleware

- **`Echo.Use`** (echo.go:431) — "adds middleware to the chain which is run after router." This is the primary middleware attachment point.
- **`WrapMiddleware`** (echo.go:766) — wraps a standard `http.Handler` middleware for use with Echo.
- **`applyMiddleware`** (echo.go:785) — internal: applies registered middleware chain.
- **`MiddlewareConfigurator`** (echo.go:121) — "defines interface for creating middleware handlers."

#### 1.4 Server & HTTP Handler

- **`Echo.Start`** (echo.go:744) — starts the HTTP server.
- **`Echo.ServeHTTP`** (echo.go:695) — public method implementing `http.Handler`.
- **`Echo.serveHTTP`** (echo.go:700) — internal implementation of request dispatch.

#### 1.5 Grouping

- **`Echo.Group`** (echo.go:659) — creates a `Group` for sub-route scoping.

---

### 2. `Router` Interface and `DefaultRouter`

#### 2.1 `Router` Interface

**Source:** `router.go:21`
**FOCUS description:** "interface for routing request contexts"

This is the abstract contract that any router implementation must satisfy. It decouples the `Echo` type from a specific routing algorithm.

#### 2.2 `DefaultRouter`

**Source:** `router.go:60`
**FOCUS description:** "registry of all registered routes"

`DefaultRouter` is the concrete implementation of `Router`. Its public/internal methods include:

| Method | Behavior |
|---|---|
| `Add` | Registers a route in the tree (called by `Echo.add`) |
| `Remove` | Removes a registered route |
| `Route` | Looks up a single route |
| `Routes` | Returns all registered routes |
| `insert` | Internal tree insertion |
| `storeRouteInfo` | Internal route metadata storage |

`router.go` is the **largest core file at 1074 lines**, reflecting the complexity of the trie-based route matching.

#### 2.3 `PathValues.Get`

**Source:** `router.go:1057`
**FOCUS description:** Returns a path parameter value.

This type provides access to captured path parameters (e.g., `:id` segments) after route matching.

---

### 3. `Group` — Sub-Route Grouping

**Source:** `group.go` (178 lines)

`Group` mirrors the `Echo` top-level API for defining routes under a common prefix or shared middleware. Key methods:

| Method | Source | Behavior |
|---|---|---|
| `Group.Add` | group.go:158 | "implements Echo#Add() for sub-routes" |
| `Group.AddRoute` | group.go | Registers a `Route` for the group |
| `Group.Any` | group.go | All-methods registration for the group |
| `Group.CONNECT`, `Group.DELETE`, etc. | group.go | Verb methods mirroring `Echo`'s API |
| `Group.Match` | group.go:77 | GUARD/ACCUMULATE pattern — validates and collects routes |

The `Group` type does not have its own router; it delegates to the parent `Echo` instance's `DefaultRouter`, prefixing paths and layering group-scoped middleware.

---

### 4. `Context` — Per-Request State

**Source:** `context.go` (667 lines)
**FOCUS description:** "represents current HTTP request"

`Context` is the carrier for all per-request state. Its public methods span:

#### 4.1 Request & Response Access

| Method | Source | Purpose |
|---|---|---|
| `Context.Request` | context.go:129 | Returns the underlying `*http.Request` |
| `Context.Response` | context.go:139 | Returns the `Response` wrapper |
| `Context.Echo` | context.go | Returns the parent `Echo` instance |

#### 4.2 Parameter & Query Access

- `Context.Param` — retrieves a named path parameter
- `Context.QueryParam` — retrieves a query-string parameter

#### 4.3 State Storage

- `Context.Set` / `Context.Get` — key-value store scoped to the request

#### 4.4 Response Helpers

- `Context.Attachment` — sends a file as a download attachment
- `Context.Blob` — sends a binary blob response
- `Context.Cookie` / `Context.Cookies` — cookie access

#### 4.5 Binding

- `Context.Bind` — binds request data to a struct (leverages `binder.go`, 1329 lines)

---

### 5. `Response` — Response Writer Wrapper

**Source:** `response.go`
**FOCUS description:** "wraps http.ResponseWriter"

`Response` wraps the standard `http.ResponseWriter` to add Echo-specific tracking (e.g., status code, bytes written). It is accessed via `Context.Response` (context.go:139).

---

### 6. `HTTPError` — Structured Error Type

**Source:** `httperror.go:107`
**FOCUS description:** "represents error during request handling"

Public methods:

| Method | Purpose |
|---|---|
| `Error` | Returns the error message string |
| `StatusCode` | Returns the HTTP status code |
| `Unwrap` | Supports Go error unwrapping |
| `Wrap` | Wraps an inner error with HTTP semantics |

`HTTPError` is the canonical error type returned by handlers and consumed by error handlers such as `DefaultHTTPErrorHandler` (echo.go, INDEX).

---

### 7. Virtual Hosting

- **`NewVirtualHostHandler`** (vhost.go:10) — "routes to virtual hosts." This allows a single server to dispatch requests to different `Echo` instances based on the `Host` header.

---

### 8. Request-Handling Middleware (Selected)

While the full middleware catalog is in the `middleware/` subdirectory, two middleware types are directly relevant to the **request-handling surface** and are cited in the clues:

| Config | Purpose |
|---|---|
| `RequestLoggerConfig` | Structured per-request logging; implements `ToMiddleware` |
| `RequestIDConfig` | Injects a unique request ID; implements `ToMiddleware` |

Both satisfy the `MiddlewareConfigurator` interface (echo.go:121) and are attached via `Echo.Use`.

---

### 9. Component Relationship Map

```
New (echo.go:333)
 └─► Echo (echo.go:68)
      ├── .GET/.POST/.PUT/... ──DELEGATE──► .Add (echo.go:642)
      │                                       └──► .add (echo.go:621)
      │                                              └──► DefaultRouter.Add (router.go:60)
      ├── .AddRoute (echo.go:617) ──────────► .add ──► DefaultRouter.Add
      ├── .Any (echo.go:504) ──────────────► .Add
      ├── .Match ──────────────────────────► .Add
      ├── .Group (echo.go:659) ──► Group (group.go)
      │                              ├── .Add (group.go:158) ──► Echo.Add
      │                              ├── .Match (group.go:77)
      │                              └── verb methods ──► Group.Add
      ├── .Use (echo.go:431) ──► middleware chain
      │                           └── applyMiddleware (echo.go:785)
      ├── .ServeHTTP (echo.go:695)
      │    └── .serveHTTP (echo.go:700)
      │         ├── Router (router.go:21) match
      │         ├── Context (context.go)
      │         │    ├── .Request (context.go:129)
      │         │    ├── .Response (context.go:139) ──► Response (response.go)
      │         │    ├── .Param, .QueryParam
      │         │    ├── .Bind ──► binder.go
      │         │    └── .Set/.Get
      │         └── HTTPError (httperror.go:107)
      ├── .Start (echo.go:744) ──► server.go
      └── WrapMiddleware (echo.go:766)

NewVirtualHostHandler (vhost.go:10) ──► routes across Echo instances

PathValues.Get (router.go:1057) ──► path parameter access

MiddlewareConfigurator (echo.go:121) ◄── RequestLoggerConfig, RequestIDConfig, etc.
```

---

### 10. Gaps and Uncertainties

The GAPS entry flags the following as **uncovered**:

| Symbol | What We Know | What Is Uncertain |
|---|---|---|
| `Echo.AcquireContext` | Listed in INDEX and FOCUS method list for `Echo`. | Detailed behavior is not described in any FOCUS entry. Likely a pool-based context acquisition method, but this is inferred, not confirmed. |
| `Echo.Middlewares` | Not described in any FOCUS entry. | Unknown whether this is a getter returning the middleware slice or has other semantics. |
| `Echo.NewContext` | Not described in any FOCUS entry. | Likely a factory method for creating `Context` instances, but specifics are absent. |
| `Echo.Pre` | Not described in any FOCUS entry. | The name suggests middleware that runs **before** the router (in contrast to `Echo.Use` which runs "after router"), but this is speculative. If it exists, it would represent a separate middleware insertion point not documented in the clues. |

These gaps mean that the **context lifecycle** (creation, pooling, reuse) and the **pre-router middleware layer** cannot be fully characterized from the provided evidence.

---

### 11. Summary

Echo's routing and request-handling surface comprises:

1. **`Echo`** (echo.go:68) — the central instance owning route registration (verb methods → `Add` → `add` → `DefaultRouter.Add`), middleware management (`Use`, `applyMiddleware`), grouping (`Group`), and server lifecycle (`Start`, `ServeHTTP`).
2. **`Router`** (router.go:21) / **`DefaultRouter`** (router.go:60) — the routing interface and its concrete trie-based implementation (1074 lines).
3. **`Group`** (group.go) — sub-route scoping that mirrors `Echo`'s verb API and delegates to the same `DefaultRouter`.
4. **`Context`** (context.go) — per-request state carrier with access to `Request`, `Response`, path/query params, binding, and key-value storage.
5. **`Response`** (response.go) — `http.ResponseWriter` wrapper accessed through `Context`.
6. **`HTTPError`** (httperror.go:107) — structured error type with status codes and unwrapping.
7. **`PathValues.Get`** (router.go:1057) — path parameter retrieval.
8. **`NewVirtualHostHandler`** (vhost.go:10) — multi-host dispatch.
9. **`MiddlewareConfigurator`** (echo.go:121) — the interface bridging core and middleware packages.

All verb methods delegate through a single chain to `DefaultRouter.Add`, giving the framework a unified registration path. Request handling flows through `ServeHTTP` → `serveHTTP` → router match → middleware chain → handler → `Context`/`Response`.
