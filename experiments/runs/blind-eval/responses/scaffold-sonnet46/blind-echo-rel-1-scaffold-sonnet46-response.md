# Scaffold (Sonnet 4.6): blind-echo-rel-1
Date: 2026-04-16

## Question

What are the main relationships among `Echo`, `Group`, `Context`, and handlers during normal request dispatch?

## Reasoning Scaffold

### 1. Identify Relevant Symbols

From FOCUS, SYM, and INDEX the core participants are:

- **Echo** (echo.go:68) — "the top-level framework instance" [FOCUS Echo]
- **Group** (group.go:14) — "a set of sub-routes for a specified route prefix" [FOCUS Group from SYM]
- **Context** (context.go:40) — "represents the context of the current HTTP request" [FOCUS Context]
- **DefaultRouter** (router.go:60) — "the registry of all registered routes for an `Echo` instance for request matching and URL path parameters" [FOCUS DefaultRouter]
- **HandlerFunc** — the user-provided request handler, accepted by `Echo.Add`, `Group.Add`, and all HTTP-method helpers [SOURCE Echo.Add echo.go L642; SOURCE Group.Add group.go L158]
- **MiddlewareFunc** — middleware functions accepted by `Echo.Use` and `Group.Use` [FOCUS Echo.Use; SOURCE Group.Use group.go L22]
- **applyMiddleware** (echo.go:785) — assembles the middleware chain around a handler [FOCUS applyMiddleware]

### 2. Relationship: Echo owns and creates Groups

`Echo.Group` (echo.go:659) creates a new `Group` bound to the Echo instance. Its behavior annotation shows it `calls: Use`, meaning group-level middleware is installed at creation time [FOCUS Echo.Group]. The `Group` struct (group.go:14) holds a back-reference to its parent Echo, evidenced by the delegation pattern: `Group.AddRoute` has behavior `DELEGATE(g.echo.add -> result)` — it forwards directly to `Echo.add` [FOCUS Group.AddRoute]. Groups can also nest: `Group.Group` (group.go L103) creates sub-groups [SOURCE Group.Group].

**Summary:** Echo → creates → Group; Group → holds reference to → Echo. Groups are organizational wrappers, not independent dispatchers.

### 3. Relationship: Route Registration (Echo ↔ Group ↔ Router)

**Echo-level registration chain:**

1. `Echo.Add(method, path, handler, middleware...)` [SOURCE echo.go L642] and all HTTP-verb shortcuts (`Echo.Any`, `Echo.GET`, etc.) delegate to `Echo.add` (private) [FOCUS Echo.Any: `calls: Add`; FOCUS Echo.add: `called_by: Add, AddRoute`].
2. `Echo.add` (echo.go:621) forwards to `DefaultRouter.Add` [FOCUS Echo.add: `calls: Add`], which inserts the route into the radix tree.

**Group-level registration chain:**

1. Every HTTP-verb method on Group (`Group.GET`, `Group.POST`, `Group.DELETE`, etc.) has behavior `DELEGATE(g.Add -> result)` and `calls: Add` [FOCUS Group.GET, Group.POST, Group.DELETE, etc.].
2. `Group.Add` (group.go:158) is the single convergence point. Its behavior is `GUARD(err != nil -> panic(err))` and it `calls: AddRoute` [FOCUS Group.Add].
3. `Group.AddRoute` (group.go:172) has behavior `DELEGATE(g.echo.add -> result)` [FOCUS Group.AddRoute], meaning it forwards to the *Echo instance's* private `add` method, which then registers with the router.

**Full chain:** `Group.GET → Group.Add → Group.AddRoute → Echo.add → DefaultRouter.Add` [FOCUS Group.GET, Group.Add, Group.AddRoute, Echo.add].

This means Group never talks to the router directly — it always goes through Echo as the central coordinator.

### 4. Relationship: Middleware Attachment

- `Echo.Use` adds middleware "which is run after router has found matching route and before route/request handler method is executed" [FOCUS Echo.Use]. It is `called_by: Group, main` — notably, Group's own initialization invokes it.
- `Group.Use` (group.go:22) installs group-scoped middleware [SOURCE Group.Use].
- `applyMiddleware` (echo.go:785) wraps a `HandlerFunc` with middleware functions, building a chain [FOCUS applyMiddleware]. This is the mechanism by which middleware and handlers are composed into a single callable.

**Summary:** Middleware is a decoration layer. `applyMiddleware` composes `MiddlewareFunc` around `HandlerFunc` to produce a final `HandlerFunc` that the router invokes.

### 5. Relationship: Request Dispatch (Echo → Router → Context → Handler)

During an incoming HTTP request, the dispatch flow is:

1. **`Echo.ServeHTTP`** (echo.go:695) implements `http.Handler` [FOCUS Echo.ServeHTTP from SYM; SOURCE echo.go L695]. This is the entry point for every request.

2. **Context acquisition:** `Echo.AcquireContext` (echo.go:684) pulls a `*Context` from a sync pool [FOCUS Echo.AcquireContext: `DELEGATE(e.contextPool.Get -> result)`]. This reuses Context objects to reduce allocations.

3. **Route lookup:** `DefaultRouter.Route` (router.go:791) looks up the handler registered for the method and path [FOCUS DefaultRouter.Route: `calls: findStaticChild, node, find`]. Once found, the matched route info is set on the Context via `Context.InitializeRoute` (context.go:263), which `calls: setPathValues` to populate path parameters [FOCUS Context.InitializeRoute].

4. **Handler execution:** The matched handler (wrapped with middleware via `applyMiddleware`) is invoked with the `Context` as its argument. The Context provides the handler with access to:
   - The request: `Context.Request()` [FOCUS Context.Request]
   - The response writer: `Context.Response()` [FOCUS Context.Response]
   - The Echo instance: `Context.Echo()` [FOCUS Context.Echo]
   - Data binding: `Context.Bind()` delegates to `c.echo.Binder.Bind` [FOCUS Context.Bind: `DELEGATE(c.echo.Binder.Bind -> result)`]
   - Serialization: `Context.json()` delegates to `c.echo.JSONSerializer.Serialize` [FOCUS Context.json]

5. **Context release:** After the handler returns, `Echo.ReleaseContext` (echo.go:690) returns the Context to the pool [FOCUS Echo.ReleaseContext]. `Context.Reset` (context.go:107) "resets the context after request completes" [FOCUS Context.Reset].

### 6. Relationship: Context as the Bridge

Context is the central mediator between the framework and user code:

- **Context → Echo:** `Context.Echo()` returns the Echo instance [FOCUS Context.Echo], and Context delegates binding and serialization back to Echo-owned components (`Context.Bind → c.echo.Binder.Bind`; `Context.json → c.echo.JSONSerializer.Serialize`) [FOCUS Context.Bind; FOCUS Context.json].
- **Echo → Context:** Echo creates Contexts via `NewContext` [FOCUS Echo.NewContext: `DELEGATE(newContext -> result)`] or acquires them from the pool via `AcquireContext` [FOCUS Echo.AcquireContext].
- **Context → Request/Response:** Context wraps the raw `*http.Request` and `*Response`, exposing them through `Request()`, `SetRequest()`, `Response()`, `SetResponse()` [FOCUS Context.Request, Context.SetRequest, Context.Response, Context.SetResponse].
- **Router → Context:** The router populates the Context with route information via `InitializeRoute` and path values via `SetPathValues` [FOCUS Context.InitializeRoute; FOCUS Context.SetPathValues].

### 7. Walk the extends / composition hierarchies

There are no explicit `extends` relationships here (this is Go, using composition). The key compositional relationships are:

| Owner | Owns | Evidence |
|-------|------|----------|
| Echo | DefaultRouter | Echo.add `calls: Add` on router [FOCUS Echo.add] |
| Echo | Context pool | AcquireContext/ReleaseContext [FOCUS Echo.AcquireContext, Echo.ReleaseContext] |
| Echo | Groups | Echo.Group creates Group [FOCUS Echo.Group] |
| Group | reference to Echo | Group.AddRoute `DELEGATE(g.echo.add)` [FOCUS Group.AddRoute] |
| Context | reference to Echo | Context.Echo() [FOCUS Context.Echo]; Context.Bind delegates to echo.Binder [FOCUS Context.Bind] |

### 8. GAPS Assessment

The GAPS section states the question type is `RELATIONAL (answerable from L2-L3 structure)` with 80% symbol coverage [GAPS]. Uncovered symbols include `Group.AddRoute` full body, `Context.FormValues`, `Context.FormValue`, and `Context.RealIP` [GAPS uncovered]. These are peripheral to the dispatch question. The drill targets (`middleware/request_logger.go`, `group.go Group.Add`, `echotest/context.go`) would add detail but are not essential for understanding the core relationships.

Notably, `Echo.ServeHTTP` has only a SYM-level entry without full behavior annotation [FOCUS Echo.ServeHTTP], so the exact internal dispatch steps (context acquisition → route lookup → middleware chain invocation → context release) are inferred from the surrounding evidence rather than directly annotated. This is the main area of uncertainty.

## Synthesis

The four entities participate in a layered architecture during normal request dispatch:

```
  Registration Phase                    Dispatch Phase
  ──────────────────                    ──────────────
  Group.GET/POST/...                    HTTP Request
       │                                     │
       ▼                                     ▼
  Group.Add ──► Group.AddRoute          Echo.ServeHTTP
                    │                        │
                    ▼                   ┌────┴────┐
               Echo.add                 │         │
                    │              AcquireContext  DefaultRouter.Route
                    ▼                   │         │
            DefaultRouter.Add           ▼         ▼
                                   Context ◄── InitializeRoute
                                       │
                                       ▼
                                 applyMiddleware(handler)
                                       │
                                       ▼
                                  Handler(Context)
                                       │
                                       ▼
                                 ReleaseContext
```

**Key relationships summarized:**

1. **Echo is the central orchestrator.** It owns the router, context pool, and creates Groups. All route registrations ultimately pass through `Echo.add` [FOCUS Echo.add, Group.AddRoute].

2. **Group is a delegation facade.** It provides organizational grouping with a shared prefix and group-level middleware, but every registration delegates through to `Echo.add` via `Group.Add → Group.AddRoute → Echo.add` [FOCUS Group.Add, Group.AddRoute].

3. **Context is the per-request mediator.** It is acquired from a pool by Echo at the start of dispatch [FOCUS Echo.AcquireContext], populated with route info by the router [FOCUS Context.InitializeRoute], passed to the handler as the sole argument, and returned to the pool after completion [FOCUS Echo.ReleaseContext, Context.Reset].

4. **Handlers are wrapped by middleware.** The `applyMiddleware` function composes middleware around the handler into a single chain [FOCUS applyMiddleware]. Middleware registered via `Echo.Use` runs after routing but before the handler [FOCUS Echo.Use docstring].

5. **Context delegates back to Echo for cross-cutting concerns.** Binding uses `c.echo.Binder` [FOCUS Context.Bind] and JSON serialization uses `c.echo.JSONSerializer` [FOCUS Context.json], keeping these pluggable at the Echo level.
