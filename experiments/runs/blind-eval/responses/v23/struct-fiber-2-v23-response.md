# v2.3 Response: struct-fiber-2
Date: 2026-04-15

## Summary

Request context in Fiber centers on the `Ctx` interface (defined in `ctx_interface_gen.go`) and its default implementation `DefaultCtx` (in `ctx.go` and `req.go`). Routing is managed by `App` (in `app.go`) and its methods in `router.go`. Request and response data types are split across two domains: server-side types in the root package (`req.go`, `res.go`, `ctx.go`, `bind.go`) and client-side types in the `client/` sub-package (`client/request.go`, `client/response.go`).

---

## Modules Handling Request Context

### `Ctx` Interface (`ctx_interface_gen.go:18`)
- **`Ctx`** "represents the Context which hold the HTTP request and response" (FOCUS, Ctx entry). This is the primary context abstraction for the framework.

### `CustomCtx` Interface (`ctx_interface.go:13-14`)
- **`CustomCtx`** "extends Ctx with the additional methods required by Fiber's internals and middleware helpers" (FOCUS, CustomCtx entry). This is used for custom context implementations.

### `DefaultCtx` — The Default Implementation
Core methods spread across `ctx.go` and `req.go`:
- **`DefaultCtx.Get`** (ctx.go:200): "returns the HTTP request header specified by field" — retrieves request headers.
- **`DefaultCtx.RequestID`** (ctx.go:311-312): "returns the request identifier from the response header or request header"; calls `Get` and `GetRespHeader` with a GUARD behavior pattern.
- **`DefaultCtx.Reset`** (ctx.go:662): "Reset is a method to reset context fields by given request when to use server handlers"; accepts `*fasthttp.RequestCtx` and calls `configDependentPaths`.
- **`DefaultCtx.MediaType`** (req.go:244): "returns the MIME type from the Content-Type header."
- **`DefaultReq.Get`** (req.go:427): "returns the HTTP request header specified by field."
- **`DefaultReq.Accepts`** (req.go:51): "checks if the specified extensions or content types are acceptable."
- **`DefaultReq.Body`** (req.go:149): "contains the raw body submitted in a POST request."
- **`DefaultReq.IsProxyTrusted`** (req.go:1080): "checks trustworthiness of remote IP."
- **`DefaultReq.getBody`** (req.go:1140): Internal body retrieval.
- **`DefaultReq.Route`** (req.go:1002): "returns the matched Route struct"; delegates to `r.c.Route`, called by `Params`.
- **`DefaultReq.App`** (req.go:83): "returns the *App reference to the instance of the Fiber application."

### Context Accessor Methods
- **`DefaultCtx.App`** (ctx.go:102): "returns the *App reference to the instance of the Fiber application."
- **`DefaultCtx.Route`** (ctx.go:355-356): "returns the matched Route struct" with `GUARD(c -> Route)` behavior; called by `FullPath`.
- **`DefaultRes.App`** (res.go:134): Same App accessor from the response side.

### Context Interoperability (Adaptor)
- **`StoreInContext`** (helpers.go:83): "stores key/value in both Fiber locals and request context" — bridges Fiber locals and Go's `context.Context`.
- **`CopyContextToFiberContext`** (middleware/adaptor/adaptor.go:101): "copies the values of context.Context to a fasthttp.RequestCtx"; called by `HTTPMiddleware`.
- **`HTTPHandlerWithContext`** (middleware/adaptor/adaptor.go:65): "like HTTPHandler, but additionally stores Fiber's user context in the request context"; calls `LocalContextFromHTTPRequest`.
- **`LocalContextFromHTTPRequest`** (middleware/adaptor/adaptor.go:78): "extracts the Fiber user context previously stored into r.Context() by the adaptor."
- **`ConvertRequest`** (middleware/adaptor/adaptor.go:89): "converts a fiber.Ctx to a http.Request."

### Custom Context Creation
- **`NewWithCustomCtx`** (app.go:667): "creates a new Fiber instance and applies the provided function to generate a custom context type"; calls `setCtxFunc` and `New`.

### Middleware Context Access
- **`FromContext`** (middleware/session/middleware.go:179): "returns the Middleware from the Fiber context."
- **`FromContext`** (middleware/requestid/requestid.go:79): "returns the request ID from context."
- **`FromContext`** (middleware/paginate/paginate.go:92): "returns the PageInfo from the request context."
- **`TokenFromContext`** (middleware/keyauth/keyauth.go:99): "returns the bearer token from the request context."

---

## Modules Handling Routing

### `App` Struct (`app.go:69`)
- **`App`** "denotes the Fiber application" with methods: `Add`, `All`, `Config`, `Connect`, `Delete`, `Domain` (FOCUS, App entry at app.go:69). The primary router.
- **`App.Head`** (app.go:906): "registers a route for HEAD methods"; delegates via `app.Add`.
- **`App.normalizePath`** (router.go:398): Normalizes paths; delegates to `RemoveEscapeChar`.

### Route Registration
- **`App.Add`** (app.go:953): "allows you to specify multiple HTTP methods" — the core route registration method.
- **`Group.Add`** (group.go:167): Same for route groups.
- **`Registering.Add`** (register.go:111): Same for the Registering interface.
- **`domainRouter.Add`** (domain.go:530): Same for domain-specific routing.

### Proxy Routing
- **`Do`** (middleware/proxy/proxy.go:146): "performs the given http request and fills the given http response"; called by `Balancer`, `BalancerForward`, `DomainForward`, `Forward`.
- **`Forward`** (middleware/proxy/proxy.go:138): Calls `Do`.
- **`DomainForward`** (middleware/proxy/proxy.go:239): Calls `Do`.

---

## Request Data Types

### Server-Side Request
- **`DefaultReq`** methods in `req.go`: `Get`, `Accepts`, `Body`, `IsProxyTrusted`, `getBody`, `Route`, `App`, `MediaType` — these form the server-side request abstraction accessed through `Ctx`.

### Client-Side Request (`client/request.go`)
- **`Request`** struct (client/request.go:46): "contains all data related to an HTTP request" with methods: `AddFile`, `AddFileWithReader`, `AddFiles`, `AddFormData`, `AddFormDataWithMap`, `AddHeader`.
- **`Request.Context`** (client/request.go:115): "returns the context associated with the Request" with GUARD behavior returning `context.Background` as default.
- **`Request.SetContext`** (client/request.go:124): "sets the context for the Request, allowing request cancellation if ctx is done."
- **`Request.Send`** (client/request.go:673): "Send executes the Request."
- **`Request.Get`** (client/request.go:633): "sends a GET request to the given URL."
- **`Request.Put`** (client/request.go:648): "sends a PUT request to the given URL."
- **`Request.SetMethod`** (client/request.go:82), **`Request.SetURL`** (client/request.go:93), **`Request.Reset`** (client/request.go:680), **`Request.resetBody`** (client/request.go:438).
- **`Request.AddFormData`** (client/request.go:493), **`Request.AddFormDataWithMap`** (client/request.go:507).
- **`WithStruct`** interface (client/request.go:24): "implemented by types that allow data to be stored from a struct via reflection."

### Data Binding
- **`Bind`** struct (bind.go:40): "provides helper methods for binding request data to Go values" with methods `All`, `Body`, `CBOR`, `Cookie`, `Custom`, `Form`; called by CBOR, Cookie, Form, Header, JSON, MsgPack, Query, RespHeader.

---

## Response Data Types

### Server-Side Response
- **`res.go`** (1153 lines): Contains response methods including:
  - **`DefaultRes.Render`** (res.go:691): "Render a template with data and sends a text/html response."
  - **`DefaultRes.SendString`** (res.go:997): "sets the HTTP response body for string types"; called by `AutoFormat` and `SendStatus`.
  - **`DefaultRes.App`** (res.go:134): App accessor.

### Client-Side Response (`client/response.go`)
- **`Response`** struct (client/response.go:19): "represents the result of a request" with methods: `Body`, `BodyStream`, `CBOR`, `Close`, `Cookies`, `Header`.
- **`Response.Body`** (client/response.go:88): "returns the HTTP response body as a byte slice."
- **`Response.Close`** (client/response.go:208): "releases both the Request and Response objects back to their pools"; calls `ReleaseResponse`, called by `Save`.
- **`Response.setRequest`** (client/response.go:33): "sets the request object in the response."

### Idempotency Response
- **`response`** struct (middleware/idempotency/response.go:9): "represents the response of a request" — used internally by the idempotency middleware.

### Client Hooks for Request/Response
- **`logger`** (client/hooks.go:345): "a response hook that logs request and response data if debug mode is enabled"; guarded by `not_c.debug`.
- **`parserRequestHeader`** (client/hooks.go:122): "merges client and request headers, and sets headers automatically based on the request data."
- **`Client.AddRequestHook`** (client/client.go:146), **`Client.AddResponseHook`** (client/client.go:160): Add user-defined hooks.
- **`Client.RequestHook`** (client/client.go:141), **`Client.ResponseHook`** (client/client.go:155): Retrieve hooks.

### Core Execution
- **`core.execute`** (client/core.go:209): "runs all hooks, applies timeouts, sends the request, and runs response hooks"; calls `afterHooks`, `execFunc`, `preHooks`, `timeout`.
- **`core.execFunc`** (client/core.go:74): "the core logic to send the request and receive the response."

---

## Uncertainty / Limits

- The clue file shows "...and 132 more modules" and "...and 1400 more symbols," so significant portions of the codebase are not visible.
- The `Ctx` interface (ctx_interface_gen.go:18) is described briefly; its full method set is not enumerated in the clue file.
- The relationship between `DefaultCtx`, `DefaultReq`, and `DefaultRes` is inferred from shared accessor patterns (e.g., both have `.App()` methods, `DefaultReq.Route` delegates to `r.c.Route`), but the exact composition is not explicitly stated.
- `router.go` is referenced by several symbols but not listed in the INDEX, so its complete contents and the full `Router` interface definition are not available.
