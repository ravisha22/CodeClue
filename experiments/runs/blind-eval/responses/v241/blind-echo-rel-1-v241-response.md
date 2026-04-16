# v2.4.1 Response: blind-echo-rel-1
Date: 2026-04-16

## Relationships Among `Echo`, `Group`, `Context`, and Handlers During Request Dispatch

### 1. Echo → Group: Creation and Delegation

`Echo.Group` (`echo.go:659`) creates a new router group with a prefix and optional group-level middleware, calling `Use` to attach the middleware [FOCUS: Echo.Group]. `Group` (`group.go:14`) is described as "a set of sub-routes for a specified route" [SYM: Group, group.go:14].

The `Group` type mirrors every route-registration method on `Echo`. Each Group HTTP-method shortcut (e.g., `Group.GET` at `group.go:37`, `Group.POST` at `group.go:57`, `Group.DELETE` at `group.go:32`, etc.) delegates to `Group.Add` (`group.go:158`) [FOCUS entries and snippets for each]. `Group.Add` in turn calls `Group.AddRoute` (`group.go:172`), which delegates to `g.echo.add` — the *Echo instance's* internal `add` method (`echo.go:621`) [FOCUS: Group.AddRoute — "DELEGATE(g.echo.add -> result)"]. This means **Group does not maintain its own router**; it forwards all route registrations back to the parent `Echo` instance's router.

Groups can also nest: `Group.Group` (`group.go:103`, snippet: `func (g *Group) Group(prefix string, middleware ...MiddlewareFunc) (sg *Group)`) creates sub-groups [snippet: Group.Group].

`Group.Use` (`group.go:22`) attaches middleware scoped to that group [snippet: Group.Use]. `Echo.Use` (`echo.go:431`) attaches middleware globally, and is itself called by `Echo.Group` during group creation [FOCUS: Echo.Use — "called_by: Group, main"].

### 2. Echo → Context: Pooling and Lifecycle

`Echo.AcquireContext` (`echo.go:684`) obtains an empty `Context` from a pool ("DELEGATE(e.contextPool.Get -> result)"), and `Echo.ReleaseContext` (`echo.go:690`) returns it [FOCUS: Echo.AcquireContext, Echo.ReleaseContext]. `Echo.NewContext` (`echo.go:357`) creates a fresh Context via `newContext` (`context.go:75`) [FOCUS: Echo.NewContext].

`Context.Reset` (`context.go:107`) resets the context after a request completes, taking a new `*http.Request` and `http.ResponseWriter` [FOCUS: Context.Reset]. This pool-and-reset cycle means Contexts are **reused across requests** rather than allocated each time.

### 3. Context ↔ Echo: Back-Reference

`Context.Echo` (`context.go:665`) returns the `Echo` instance that owns the context [FOCUS: Context.Echo]. This back-reference enables the Context to delegate operations to Echo-level components — for example, `Context.Bind` (`context.go:399`) delegates to `c.echo.Binder.Bind` [FOCUS: Context.Bind — "DELEGATE(c.echo.Binder.Bind -> result)"], and `Context.json` (`context.go:464`) delegates to `c.echo.JSONSerializer.Serialize` [FOCUS: Context.json].

### 4. Context → Handlers: The Request-Handling Surface

`Context` (`context.go:40`) "represents the context of the current HTTP request" with methods for reading inputs and writing responses [FOCUS: Context — "methods: Attachment, Bind, Blob, Cookie, Cookies, Echo"]. Handlers receive a `*Context` and return `error` (as seen in the `main` example and the `hello` handler pattern) [FOCUS: main — "calls: GET, Start, Use, New"].

Input access: `Context.Request` (`context.go:129`), `Context.QueryParam` (`context.go:287`), `Context.FormValue` (`context.go:319`), `Context.Cookie` (`context.go:364` — delegates to `c.request.Cookie`), `Context.Cookies` (`context.go:374` — delegates to `c.request.Cookies`), `Context.SetPathValues` (`context.go:255`) [FOCUS/SYM entries for each].

Response writing: `Context.String` (`context.go:445`), `Context.Blob` (`context.go:552`), `Context.HTMLBlob` (`context.go:440`), `Context.json` (`context.go:464`), `Context.xml` (`context.go:517`), `Context.File` (`context.go:571`) [SYM entries]. The `Response` object is accessed via `Context.Response` (`context.go:139`) [SYM: Context.Response].

Route information: `Context.InitializeRoute` (`context.go:263`) sets route-related variables, calling `setPathValues` [FOCUS: Context.InitializeRoute].

### 5. Echo → Router → Handler: Dispatch Chain

The `main` function demonstrates the typical flow: `New` → `Use` (middleware) → `GET` (route) → `Start` [FOCUS: main — "calls: GET, Start, Use, New"]. `Echo.ServeHTTP` (`echo.go:695`) implements the `http.Handler` interface [SYM: Echo.ServeHTTP]. `DefaultRouter` (`router.go:60`) is the registry for all routes with methods `Add`, `Remove`, `Route`, `Routes` [FOCUS: DefaultRouter].

`NewVirtualHostHandler` (`vhost.go:10`) creates an Echo instance that routes requests to virtual hosts based on the request's host header [FOCUS: NewVirtualHostHandler].

### 6. Middleware Attachment Points

There are two middleware chains on `Echo`: `Echo.Pre` (`echo.go:426` — not in rel-1 FOCUS but referenced through the common SYM/clue) for middleware run before routing, and `Echo.Use` (`echo.go:431`) for middleware run after the router matches [FOCUS: Echo.Use — "adds middleware to the chain which is run after router has found matching route and before route/request handler met"]. Group-level middleware is attached via `Group.Use` (`group.go:22`) [snippet].

`ContextTimeout` middleware (`middleware/context_timeout.go:28`) shows the middleware-to-handler relationship: it returns an error (503) to the client when the underlying handler times out [FOCUS: ContextTimeout].

### 7. Testing Relationships

The `echotest` package provides `ContextConfig` (`echotest/context.go:20`) which can produce test Contexts via `ToContext` (`echotest/context.go:75`) and `ToContextRecorder` (`echotest/context.go:81` — also called by `ServeWithHandler` at `echotest/context.go:167`) [FOCUS/snippet entries for each]. These testing helpers create real `echo.Context` instances tied to `httptest.ResponseRecorder` [snippet: ContextConfig.ToContextRecorder returns `(*echo.Context, *httptest.ResponseRecorder)`].

### What Cannot Be Determined

- The **exact dispatch logic inside `Echo.ServeHTTP`** and the unexported `Echo.serveHTTP` are listed as uncovered in GAPS [GAPS: uncovered: Group.AddRoute, Context.FormValues, Context.FormValue, Context.RealIP]. The source snippets only show function signatures, not bodies.
- How **pre-middleware interacts with the router** at runtime (the `Echo.Pre` chain's exact execution relative to `DefaultRouter.Route`) is not detailed in this prompt's FOCUS section.
- The **`applyMiddleware`** function (`echo.go:785`) is referenced in other tasks but not focused here, so the middleware wrapping/chaining mechanism is not fully visible.
- Whether `Group` stores its own middleware list separately or merges into Echo's list is not specified — only that `Group.Use` exists and `Echo.Group` calls `Use` [FOCUS: Echo.Group, Group.Use].
- The **`Response` type's lifecycle** (creation, field semantics, committed state) is only partially visible through `Context.Response` and `Response.WriteHeader` [SYM entries].
- `Context.FormValues` and `Context.RealIP` are listed as uncovered [GAPS].
