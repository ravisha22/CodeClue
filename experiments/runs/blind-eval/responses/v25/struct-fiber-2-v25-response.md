# v2.5 Response: struct-fiber-2
Date: 2026-04-16

## Question
What modules handle request context and routing in Fiber, and where are the data types for request and response defined?

## Answer

### Request Context Modules

**`ctx.go`** — Defines `DefaultCtx`, the primary request context implementation:
- `DefaultCtx.App` (FOCUS: `DefaultCtx.App` at `ctx.go:102-102`) — Returns the `*App` reference. Called by `Body`, `CBOR`, `Cookie`, `Custom`, `Form`, `Header`, `JSON`, `MsgPack`.
- `DefaultCtx.RequestCtx` (FOCUS: `DefaultCtx.RequestCtx` at `ctx.go:118-118`) — Returns `*fasthttp.RequestCtx`. Called by `adaptFastHTTPHandler`, `wrapHTTPHandler`, `All`, `Body`, `Cookie`, `Form`, `Query`, `ConvertRequest`.
- `DefaultCtx.Next` (SYM: `DefaultCtx.Next` at `ctx.go:243`) — Executes the next method in the handler stack.
- `DefaultCtx.Path` (SYM: `DefaultCtx.Path` at `ctx.go:297`) — Returns the path part of the request URL.
- `DefaultCtx.RequestID` (FOCUS: `DefaultCtx.RequestID` at `ctx.go:311-312`) — Returns request identifier from response/request headers.
- `DefaultCtx.RestartRouting` (FOCUS: `DefaultCtx.RestartRouting` at `ctx.go:265-266`) — Restarts routing instead of going to the next handler. Calls `next` and `nextCustom`.
- `DefaultCtx.String` (SYM: `DefaultCtx.String` at `ctx.go:571`) — Unique string representation.
- `DefaultCtx.configDependentPaths` (SYM: `ctx.go:632`) — Sets paths for route recognition.
- `DefaultCtx.Request` (FOCUS: `DefaultCtx.Request` at `ctx.go:178-178`) — Returns `*fasthttp.Request` object. Behavior: `GUARD(c.fasthttp == nil -> return nil)`.
- `DefaultCtx.IsMiddleware` (FOCUS: `DefaultCtx.IsMiddleware` at `ctx.go:380-381`) — Returns true if handler was registered as middleware.

**`ctx_interface.go`** — Defines `CustomCtx` (FOCUS: `CustomCtx` at `ctx_interface.go:13-14`), which extends `Ctx` with additional methods required by Fiber's internals and middleware helpers.

**Context value retrieval functions** in middleware:
- `FromContext` (FOCUS: `middleware/session/middleware.go:179`) — Gets session Middleware from context via `fiber.ValueFromContext[*Middleware]`.
- `FromContext` (FOCUS: `middleware/requestid/requestid.go:79`) — Gets request ID from context via `fiber.ValueFromContext[string]`.
- `TokenFromContext` (FOCUS: `middleware/keyauth/keyauth.go:99`) — Gets bearer token from context.
- `TokenFromContext` (FOCUS: `middleware/csrf/csrf.go:227`) — Gets CSRF token from context.
- `HandlerFromContext` (FOCUS: `middleware/csrf/csrf.go:238`) — Gets CSRF Handler from context.
- `UsernameFromContext` (FOCUS: `middleware/basicauth/basicauth.go:126`) — Gets username from context.
- `FromContext` (FOCUS: `middleware/paginate/paginate.go:92`) — Gets PageInfo from context.
- `StoreInContext` (FOCUS: `StoreInContext` at `helpers.go:83-83`) — Stores key/value in both Fiber locals and request context. The source snippet confirms: `func StoreInContext(c Ctx, key, value any)`.
- `LocalContextFromHTTPRequest` (FOCUS: `middleware/adaptor/adaptor.go:78-78`) — Extracts Fiber user context from `*http.Request`.

### Routing Modules

**`router.go`** (767L) — Core routing engine (INDEX: `RebuildTree`, `RemoveRoute`, `RemoveRouteByName`, `RemoveRouteFunc`, `addPrefixToRoute`):
- `App.next` (SYM: `router.go:115`) — Core request dispatch function.
- `App.nextCustom` (SYM: `router.go:216`) — Custom context request dispatch.
- `App.register` (SYM: `router.go:513`) — Route registration.
- `App.addRoute` (SYM: `router.go:590`) — Adds route to routing tree.
- `App.normalizePath` (SYM: `router.go:398`) — Path normalization.
- `App.pruneAutoHeadRouteLocked` (SYM: `router.go:491`) — Removes auto-generated HEAD routes.
- `Route` struct (FOCUS: `Route` at `router.go:45-46`) — Holds all metadata for registered handlers. Has a `match` method.

**`path.go`** (844L) — Path matching and constraints: `CheckConstraint`, `Constraint`, `CustomConstraint`, `GetTrimmedParam`, `RemoveEscapeChar` (INDEX). `RoutePatternMatch` (FOCUS: `RoutePatternMatch` at `path.go:155-155`) — Reports whether a path matches a Fiber route pattern.

**`mount.go`** (227L) — Sub-app mounting: `App.MountPath` (SYM: `mount.go:103-104`), `App.mount` (SYM: `mount.go:42-42`, called by `Use`).

**`group.go`** — Route groups: `Group.Add` (SYM: `group.go:167`), `Group.Name` (SYM: `group.go:27`).

**`domain.go`** — Domain-based routing: `domainRouter.Add` (SYM: `domain.go:530`), `domainRouter.Use` (FOCUS: `domain.go:350`), `domainRouter.mount` (FOCUS: `domain.go:403`), `domainRouter.registerGroup` (SYM: `domain.go:336`), `domainRouter.registerPath` (SYM: `domain.go:327`).

**`register.go`** — Registration API: `Registering.Add` (SYM: `register.go:111`).

**`redirect.go`** — `Redirect.Route` (SYM: `redirect.go:339`).

### Request and Response Data Types

**Server-side request (`req.go`):**
- `DefaultReq.Body` (SYM: `req.go:149`) — Raw body from POST request.
- `DefaultReq.Host` (SYM: `req.go:465`) — Host from X-Forwarded headers.
- `DefaultReq.Locals` (SYM: `req.go:672`) — Pass values under request.
- `DefaultReq.App` (SYM: `req.go:83`) — App reference.
- `DefaultReq.Accepts` (SYM: `req.go:51`) — Content negotiation.
- `DefaultReq.RequestCtx` (SYM: `req.go:201`) — Underlying fasthttp context.
- `DefaultReq.Route` (FOCUS: `DefaultReq.Route` at `req.go:1002`) — Returns matched Route struct.
- `DefaultReq.Request` (FOCUS: `DefaultReq.Request` at `req.go:348`) — Returns `*fasthttp.Request`.

**Server-side response (`res.go`, 1153L):**
- `DefaultRes.Append` (SYM: `res.go:140`) — Appends to response header.
- `DefaultRes.Write` (SYM: `res.go:1098`) — Appends bytes to response body.
- `DefaultRes.WriteString` (SYM: `res.go:1110`) — Appends string to response body.
- `DefaultRes.App` (SYM: `res.go:134`) — App reference.
- `DefaultRes.RequestCtx` (SYM: `res.go:248`) — Underlying fasthttp context.
- `DefaultRes.Cookie` (INDEX: `res.go` lists `Cookie`).

**Client-side request (`client/request.go`, 1122L):**
- `Request` struct (FOCUS: `Request` at `client/request.go:46-46`) — Contains all HTTP request data. Methods: `AddFile`, `AddFileWithReader`, `AddFiles`, `AddFormData`, `AddFormDataWithMap`, `AddHeader`.
- `Request.Send` (FOCUS: `client/request.go:673`) — Executes the request.
- `Request.Get` (FOCUS: `client/request.go:633`) — Sends GET request.
- `Request.Context` (FOCUS: `client/request.go:115`) — Returns associated context.
- `Request.SetContext` (FOCUS: `client/request.go:124`) — Sets request context.
- `Request.Reset` (FOCUS: `client/request.go:680`) — Clears the request object.
- `FormData` struct (FOCUS: `FormData` at `client/request.go:874`) — Wraps fasthttp.Args for form data. Methods: `Add`, `AddWithMap`, `DelData`, `Keys`, `Reset`, `Set`.

**Client-side response (`client/response.go`):**
- `Response` struct (FOCUS: `Response` at `client/response.go:19-19`) — Represents result of a request. Methods: `Body`, `BodyStream`, `CBOR`, `Close`, `Cookies`, `Header`.
- `Response.Body` (SYM: `client/response.go:88`) — Returns body as bytes.
- `Response.String` (SYM: `client/response.go:109`) — Returns body as trimmed string.
- `Response.Reset` (SYM: `client/response.go:193`) — Clears the response.
- `Response.Close` (FOCUS: `client/response.go:208`) — Releases Request and Response to pools.
- `Response.setRequest` (FOCUS: `client/response.go:33`) — Links request to response.

**Data binding (`bind.go`, 477L):**
- `Bind.Body` (SYM: `bind.go:385`) — Binds request body into struct.
- `AcquireBind`, `All`, `Body`, `CBOR`, `Cookie` (INDEX).

**Adaptor types** (`middleware/adaptor/adaptor.go`):
- `ConvertRequest` (FOCUS: `middleware/adaptor/adaptor.go:89`) — Converts `fiber.Ctx` to `*http.Request`. Source snippet: `func ConvertRequest(c fiber.Ctx, forServer bool) (*http.Request, error)`.
- `HTTPHandlerWithContext` (FOCUS: `:65`) — Wraps `http.Handler` storing Fiber context. Source snippet: `func HTTPHandlerWithContext(h http.Handler) fiber.Handler`.
- `CopyContextToFiberContext` (FOCUS: `:101`) — Copies `context.Context` values to `fasthttp.RequestCtx`.

**Client hooks (`client/client.go`):**
- `Client.AddRequestHook` (FOCUS: `client/client.go:146`) — Adds request hooks.
- `Client.AddResponseHook` (FOCUS: `client/client.go:160`) — Adds response hooks.

### Helper Types (`helpers.go`)

Source snippets confirm generic type constraints:
- `GenericType` (source: `helpers.go:1104`) — `GenericTypeInteger | GenericTypeFloat | bool | string | []byte`.
- `GenericTypeFloat` — `float32 | float64`.
- `GenericTypeInteger` — `GenericTypeIntegerSigned | GenericTypeIntegerUnsigned`.
- Utility functions: `IsMethodSafe`, `IsMethodIdempotent`, `parseAddr`, `readContent`, `uniqueRouteStack` (source snippets).

### What Cannot Be Determined

Per GAPS: "uncovered: App.nextCustom, App.next, Response.Status, parserRequestBodyFile." The full implementation details of `App.next`/`App.nextCustom` (the core dispatch loop), `Response.Status`, and file body parsing are not provided. The source snippets for `CopyContextToFiberContext`, `HTTPHandlerWithContext`, and `StoreInContext` show only function signatures, not full bodies.
