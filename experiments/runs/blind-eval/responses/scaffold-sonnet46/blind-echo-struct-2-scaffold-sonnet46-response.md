# Scaffold (Sonnet 4.6): blind-echo-struct-2
Date: 2026-04-16

## Question

Which public types and subcomponents make up Echo's routing and request-handling surface?

## Reasoning Scaffold

### 1. Identifying Relevant Modules and Symbols

From TREE and INDEX, the routing and request-handling surface spans these key source files:

- **echo.go** (865L): Core framework type and route registration — `Config`, `DefaultHTTPErrorHandler`, `AcquireContext`, `Add`, `AddRoute` (INDEX echo.go).
- **router.go** (1074L): Route matching engine — `Add`, `Remove`, `AddRouteError` (INDEX router.go).
- **context.go** (667L): Per-request context — `Bind`, `Blob`, `Cookie`, `Cookies`, response helpers (INDEX context.go).
- **group.go** (178L): Sub-route grouping — `Add`, `AddRoute`, `Any`, `CONNECT`, `DELETE` (INDEX group.go).
- **response.go**: HTTP response writer wrapper (TREE).
- **route.go**: Route metadata type (TREE).
- **httperror.go** (162L): Error representation — `HTTPError`, `StatusCode`, `Unwrap`, `Wrap` (INDEX httperror.go).
- **bind.go** (472L) / **binder.go** (1329L) / **binder_generic.go** (571L): Request data binding subsystem (INDEX bind.go, binder.go, binder_generic.go).

### 2. Public Types — Core Routing Surface

#### `Echo` (echo.go:68)
FOCUS describes Echo as *"the top-level framework instance"* (FOCUS Echo, echo.go:68). It is the central orchestrator for route registration and HTTP serving. Key public methods on Echo for routing and request handling:

- **`New`** (echo.go:333, SYM/FOCUS): *"Creates an instance of Echo."* Calls `DefaultHTTPErrorHandler` and `NewDefaultFS` (FOCUS New). Entry point for bootstrapping.
- **`NewWithConfig`** (echo.go:294, FOCUS): *"Creates an instance of Echo with given configuration."* Delegates to `New` (FOCUS NewWithConfig).
- **`Echo.Add`** (echo.go:642, SYM): *"Registers a new route for an HTTP method and path."* This is the primary route registration method.
- **`Echo.add`** (echo.go:621, FOCUS): Internal route addition. Behavior: `GUARD(e.OnAddRoute != nil -> return RouteInfo{},…); PRECEDENCE(e -> err -> paramsCount)`. Called by both `Add` and `AddRoute` (FOCUS Echo.add).
- **`Echo.Any`** (echo.go:504, FOCUS): *"Registers a new route for all HTTP methods."* Delegates to `e.Add` (FOCUS Echo.Any, behavior: `DELEGATE(e.Add -> result)`).
- **`Echo.Use`** (echo.go:431, SYM/FOCUS): *"Adds middleware to the chain which is run after router has found matching route and before route/request handler method is executed."* Signature: `Echo.Use(middleware ...MiddlewareFunc)`. Called by `Group` and `main` (FOCUS Echo.Use).
- **`Echo.ServeHTTP`** (echo.go:695, SYM): *"Implements `http.Handler` interface."* This is the dispatch entry point that makes Echo usable as a standard `http.Handler`.
- **`Echo.Start`** (echo.go:744, FOCUS): *"Starts HTTP server on given address with Echo as a handler."* Behavior: `DELEGATE(sc.Start -> result); UNWIND(defer)` (FOCUS Echo.Start).
- **`Echo.AcquireContext`** (INDEX echo.go): Context pool management for request handling.
- **HTTP verb methods**: `Echo.CONNECT`, `Echo.DELETE` listed in FOCUS Echo methods. GAPS notes that `Echo.DELETE`, `Echo.File`, `Echo.HEAD`, `Echo.Match` are uncovered but structurally inferrable — they follow the same `DELEGATE(e.Add -> result)` pattern as `Echo.Any`.

#### `Router` (router.go:21)
FOCUS describes Router as *"interface for routing request contexts to registered routes"* (FOCUS Router, router.go:21). This is the routing contract that allows pluggable router implementations.

#### `DefaultRouter` (router.go:60)
FOCUS: *"The registry of all registered routes for an `Echo` instance for request matching and URL path parameter parsing"* (FOCUS DefaultRouter, router.go:60). Public methods: `Add`, `Remove`, `Route`, `Routes` plus internal `insert`, `storeRouteInfo`. This is the concrete radix-tree router implementation backing Echo's route matching.

Supporting router internals visible in SYM:
- **`node.findStaticChild`** (router.go:709, SYM): Internal trie traversal for static path segments.
- **`routeMethods.updateAllowHeader`** (router.go:251, SYM): Manages the Allow header for OPTIONS/405 responses.

#### `Group` (group.go:14)
SYM/FOCUS: *"A set of sub-routes for a specified route prefix"* (SYM Group, group.go:14). Group mirrors Echo's route registration API for prefixed sub-routes:

- **`Group.Add`** (group.go:158, FOCUS): *"Implements `Echo#Add()` for sub-routes within the Group."* Behavior: `GUARD(err != nil -> panic(err))`. Calls `AddRoute`. Called by `Any`, `CONNECT`, `DELETE`, `File`, `GET`, `HEAD`, `OPTIONS`, `PATCH` (FOCUS Group.Add). Note the `panic` on error — this is a fail-fast design.
- **`Group.AddRoute`** (group.go:172, SYM): *"Registers a new Routable with Router."*
- **`Group.GET`** (group.go:37, FOCUS): *"Implements `Echo#GET()` for sub-routes."* Delegates to `g.Add`. Called by `FileFS` (FOCUS Group.GET).
- **`Group.Any`** (group.go:72, FOCUS): *"Implements `Echo#Any()` for sub-routes."* Delegates to `g.Add`.
- **`Group.Match`** (group.go:77, FOCUS): Behavior: `GUARD(len(errs) > 0 -> panic(errs)); ACCUMULATE(AddRoute loop -> errs)`. Raises panic on accumulated errors.
- **`Group.StaticFS`** (group.go:122, FOCUS): *"Implements `Echo#StaticFS()` for sub-routes."* Delegates to `g.Add`. Called by `Static`.

### 3. Public Types — Request-Handling Surface

#### `Context` (context.go:40)
FOCUS: *"Represents the context of the current HTTP request"* (FOCUS Context, context.go:40). This is the primary request-handling interface, providing access to request data, response writing, and data binding. Key methods:

**Request access:**
- **`Context.Request`** (context.go:129, SYM): *"Returns `*http.Request`."*
- **`Context.SetRequest`** (context.go:134, SYM): *"Sets `*http.Request`."*
- **`Context.QueryParam`** (context.go:287, SYM): *"Returns the query param for the provided name."*
- **`Context.FormValue`** (context.go:319, SYM): *"Returns the form field value for the provided name."*
- **`Context.Cookie`** (context.go:364, FOCUS): *"Returns the named cookie provided in the request."* Behavior: `DELEGATE(c.request.Cookie -> result)`.
- **`Context.Cookies`** (context.go:374, FOCUS): *"Returns the HTTP cookies sent with the request."* Behavior: `DELEGATE(c.request.Cookies -> result)`.

**Response writing:**
- **`Context.Response`** (context.go:139, SYM): *"Returns `*Response`."*
- **`Context.SetResponse`** (context.go:145, SYM): *"Sets `*http.ResponseWriter`."*
- **`Context.String`** (context.go:445, SYM): *"Sends a string response with status code."*
- **`Context.Blob`** (context.go:552, SYM): *"Sends a blob response with status code."*
- **`Context.HTMLBlob`** (context.go:440, SYM): *"Sends an HTTP blob response with status code."*
- **`Context.File`** (context.go:571, SYM): *"Sends a response with the content of the file."*
- **`Context.Attachment`** (INDEX context.go): File download with Content-Disposition header.
- **`Context.json`** (context.go:464, FOCUS): Internal JSON serialization. Behavior: `DELEGATE(c.echo.JSONSerializer.Serialize -> result)`. Calls `Response`, `SetResponse`, `writeContentType`. Called by `JSON` and `JSONPretty`.

**Data binding:**
- **`Context.Bind`** (context.go:399, FOCUS): *"Binds path params, query params and the request body into provided type `i`."* Behavior: `DELEGATE(c.echo.Binder.Bind -> result)`. This delegates to the Echo instance's configured Binder.
- **`Context.Get`** (context.go:380, SYM): *"Retrieves data from the context."*
- **`Context.Set`** (context.go:387, SYM): *"Saves data in the context."*

#### `Response` (response.go)
SYM entries confirm this wraps `http.ResponseWriter`:
- **`Response.WriteHeader`** (response.go:49, SYM): *"Sends an HTTP response header with the provided status code."*
- **`Response.Unwrap`** (response.go:105, SYM): *"Returns the original http.ResponseWriter."*

#### `HTTPError` (httperror.go:107)
FOCUS: *"Represents an error that occurred while handling a request"* (FOCUS HTTPError, httperror.go:107). Methods: `Error`, `StatusCode`, `Unwrap`, `Wrap`.
- **`StatusCode`** (httperror.go:45, SYM): *"Returns status code from error if it is an HTTPError."* Standalone function for error introspection.
- **`DefaultHTTPErrorHandler`** (echo.go:374, SYM/FOCUS): *"Creates new default HTTP error handler."* Called by `New` during bootstrap.

### 4. Binding Subsystem

The binding surface spans three files:

- **bind.go** (472L, INDEX): Top-level binding functions — `BindBody`, `BindHeaders`, `BindPathValues`, `BindQueryParams`, `BindUnmarshaler`.
- **binder.go** (1329L, INDEX): Fluent binder API — `BindingError`, `FormFieldBinder`, `NewBindingError`, `PathValuesBinder`. The `BindingError` type (SYM binder.go) provides structured error reporting for binding failures.
- **binder_generic.go** (571L, INDEX): Generic binding utilities — `TimeOpts`, `bindValue`.

`Context.Bind` (FOCUS) delegates to `c.echo.Binder.Bind`, making the Binder interface a pluggable extension point. `DefaultJSONSerializer.Deserialize` (FOCUS, json.go:24) handles JSON body parsing with behavior: `GUARD(err := json.NewDecoder(c.Request().Body).Decode... -> return ErrBadRequest...)`.

### 5. Adapter/Wrapper Utilities

- **`WrapHandler`** (echo.go:752, FOCUS): *"Wraps `http.Handler` into `echo.HandlerFunc`."* Calls `ServeHTTP`. Enables interop with standard library handlers.
- **`WrapMiddleware`** (echo.go:766, FOCUS): *"Wraps `func(http.Handler) http.Handler` into `echo.MiddlewareFunc`."* Calls `ServeHTTP`. Enables interop with standard library middleware.
- **`applyMiddleware`** (echo.go:785, SYM): Internal function that chains middleware before route handler execution.

### 6. Testing Support

- **`ContextConfig`** (echotest/context.go:20, FOCUS): *"Configuration for creating echo.Context for testing purposes."* Methods: `ServeWithHandler`, `ToContext`, `ToContextRecorder` (SYM echotest/context.go). This is the public testing API for constructing test contexts.

### 7. Virtual Hosting

- **`NewVirtualHostHandler`** (vhost.go:10, FOCUS): *"Creates instance of Echo that routes requests to given virtual hosts."* Signature: `NewVirtualHostHandler(vhosts map[string]*Echo)`. Composes multiple Echo instances keyed by hostname.

### 8. Call Chain Summary

The primary routing call chain:

```
New/NewWithConfig → Echo instance (with DefaultHTTPErrorHandler)
    ↓
Echo.Add / Echo.Any / Echo.GET... → Echo.add → DefaultRouter.Add
    ↓
Group.Add / Group.GET... → Group.AddRoute → Echo.add (same path)
    ↓
Echo.Use → middleware chain registration
    ↓
Echo.Start → HTTP server → Echo.ServeHTTP → router match → applyMiddleware → HandlerFunc
    ↓
HandlerFunc receives Context → Context.Request/Bind/QueryParam → Context.String/JSON/Blob/File
```

### 9. Gaps and Uncertainties

Per GAPS: coverage is 80 symbols at L3 with 44 behavior-annotated. The following are structurally inferable but lack explicit behavior annotations:

- **`Echo.DELETE`**, **`Echo.HEAD`**, **`Echo.File`**, **`Echo.Match`** — listed as uncovered (GAPS). By structural analogy with `Echo.Any` (which delegates to `Echo.Add`), these almost certainly follow the same `DELEGATE(e.Add -> result)` pattern, but this cannot be confirmed from the clue data alone.
- **`Response`** internals beyond `WriteHeader` and `Unwrap` are not detailed in FOCUS/SYM.
- **`Route`** (route.go) appears in TREE but has no INDEX, SYM, or FOCUS entries — its public fields/methods are unknown from the clue data.
- **`router_concurrent.go`** appears in TREE with no further detail — likely contains concurrency-safe router operations but this is speculative.
- The full list of `Context` methods beyond those in SYM/FOCUS (e.g., `JSON`, `JSONPretty`, `Redirect`, `NoContent`) can be inferred as callers of `Context.json` but are not individually documented.
- The `middleware/` directory (24 files) is largely outside the clue scope except for `RequestLogger` (middleware/request_logger.go) and `Static`/`StaticConfig` (middleware/static.go).

## Summary

Echo's routing and request-handling surface is composed of **seven primary public types** organized in a layered architecture:

| Type | File | Role |
|------|------|------|
| `Echo` | echo.go:68 | Top-level framework instance; route registration, middleware, server lifecycle |
| `Router` (interface) | router.go:21 | Pluggable routing contract |
| `DefaultRouter` | router.go:60 | Concrete radix-tree router with `Add`/`Remove`/`Route`/`Routes` |
| `Group` | group.go:14 | Prefixed sub-route grouping mirroring Echo's registration API |
| `Context` | context.go:40 | Per-request context: request access, response writing, data binding |
| `Response` | response.go | `http.ResponseWriter` wrapper with status tracking |
| `HTTPError` | httperror.go:107 | Structured error with HTTP status code, wrapping, and unwrapping |

Supporting subcomponents include the **binding subsystem** (`BindBody`/`BindHeaders`/`BindPathValues`/`BindQueryParams` in bind.go; `FormFieldBinder`/`PathValuesBinder` in binder.go), **adapter utilities** (`WrapHandler`, `WrapMiddleware` in echo.go), **JSON serialization** (`DefaultJSONSerializer` in json.go), **virtual hosting** (`NewVirtualHostHandler` in vhost.go), and **test helpers** (`ContextConfig` in echotest/context.go).
