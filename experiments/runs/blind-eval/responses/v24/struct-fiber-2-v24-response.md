# v2.4 Response: struct-fiber-2
Date: 2026-04-16

## Question
What modules handle request context and routing in Fiber, and where are the data types for request and response defined?

## Answer

### Request Context Modules

**Core Context Types (`ctx_interface_gen.go`, `ctx.go`):**
- `Ctx` (`Ctx`, ctx_interface_gen.go:18) — "represents the Context which hold the HTTP request and response." This is the primary interface for request context in Fiber.
- `CustomCtx` (`CustomCtx`, ctx_interface.go:13-14) — "extends Ctx with the additional methods required by Fiber's internals and middleware helpers."
- `DefaultCtx` is the concrete implementation, providing methods such as:
  - `DefaultCtx.Get` (`DefaultCtx.Get`, ctx.go:200) — returns HTTP request header
  - `DefaultCtx.RequestID` (`DefaultCtx.RequestID`, ctx.go:311-312) — returns request identifier from response/request headers, calls `Get` and `GetRespHeader`
  - `DefaultCtx.MediaType` (`DefaultCtx.MediaType`, req.go:244) — returns MIME type from Content-Type header

**Request Helpers (`req.go`):**
- `DefaultReq.Get` (`DefaultReq.Get`, req.go:427) — returns HTTP request header
- `DefaultReq.Accepts` (`DefaultReq.Accepts`, req.go:51) — checks accepted extensions/content types
- `DefaultReq.Body` (`DefaultReq.Body`, req.go:149) — raw body from POST request
- `DefaultReq.IsProxyTrusted` (`DefaultReq.IsProxyTrusted`, req.go:1080) — checks proxy trustworthiness
- `DefaultReq.getBody` (`DefaultReq.getBody`, req.go:1140) — internal body retrieval

**Response Helpers (`res.go`, 1153 lines):**
- Contains response methods like `Cookie`, `App`, `Append`, `Attachment`, `AutoFormat`
- `DefaultRes.Render` (`DefaultRes.Render`, res.go:691) — renders templates with data
- `DefaultRes.SendString` (`DefaultRes.SendString`, res.go:997) — sets HTTP response body for string types

**Context Data Sharing:**
- `StoreInContext` (`StoreInContext`, helpers.go:83) — "stores key/value in both Fiber locals and request context." Source snippet confirms: `func StoreInContext(c Ctx, key, value any)`. This bridges Fiber's locals and Go's `context.Context`.
- `FromContext` patterns are used by multiple middleware:
  - Session: `FromContext` (middleware/session/middleware.go:179) uses `fiber.ValueFromContext[*Middleware]`
  - RequestID: `FromContext` (middleware/requestid/requestid.go:79) uses `fiber.ValueFromContext[string]`
  - KeyAuth: `TokenFromContext` (middleware/keyauth/keyauth.go:99) uses `fiber.ValueFromContext[string]`
  - Paginate: `FromContext` (middleware/paginate/paginate.go:92)

**Application Context Access:**
- `DefaultCtx.App` (`DefaultCtx.App`, ctx.go:102) — returns `*App` reference
- `DefaultReq.App` (`DefaultReq.App`, req.go:83) — returns `*App` reference
- `DefaultRes.App` (`DefaultRes.App`, res.go:134) — returns `*App` reference

**Custom Context Creation:**
- `NewWithCustomCtx` (`NewWithCustomCtx`, app.go:667) — creates a Fiber instance with a custom context type via `func(app *App)` callback, calling `setCtxFunc` and `New`.

### Routing Modules

**Router (`router.go`):**
- Contains the `Router` interface, `Route` struct, and core dispatch logic
- `App.normalizePath` (`App.normalizePath`, router.go:398) — path normalization
- `App.pruneAutoHeadRouteLocked` (`App.pruneAutoHeadRouteLocked`, router.go:491) — removes auto-generated HEAD routes

**Path Matching (`path.go`, 844 lines):**
- `CheckConstraint`, `Constraint`, `CustomConstraint`, `GetTrimmedParam`, `RemoveEscapeChar` — route constraint and parameter handling

**Domain Routing (`domain.go`, 688 lines):**
- `domainMatcher.match` (`domainMatcher.match`, domain.go:139) — hostname matching
- `domainRouter.registerGroup` (`domainRouter.registerGroup`, domain.go:336) — group registration
- `domainRouter.registerPath` (`domainRouter.registerPath`, domain.go:327) — path registration

**Redirect Routing (`redirect.go`, 433 lines):**
- `AcquireRedirect`, `FlashMessage`, `OldInputData`, `Back`, `Message`

**Mounting (`mount.go`):**
- Sub-app mounting for routing hierarchy

### Request and Response Data Types

**Server-Side Request/Response:**
- `Ctx` (`Ctx`, ctx_interface_gen.go:18) holds both the HTTP request and response.
- `Bind` (`Bind`, bind.go:40) — "provides helper methods for binding request data to Go values." Methods: `All`, `Body`, `CBOR`, `Cookie`, `Custom`, `Form`. Called by `CBOR`, `Cookie`, `Form`, `Header`, `JSON`, `MsgPack`, `Query`, `RespHeader`.
- `BindError` (`BindError.Error`, bind.go:65) — error type for binding failures

**Client-Side Request (`client/request.go`, 1122 lines):**
- `Request` (`Request`, client/request.go:46) — "contains all data related to an HTTP request." Methods include: `AddFile`, `AddFileWithReader`, `AddFiles`, `AddFormData`, `AddFormDataWithMap`, `AddHeader`, and many more.
- Sub-types within `Request`:
  - `Header` (`Header`, client/request.go:708) — request headers
  - `QueryParam` (`QueryParam`, client/request.go:742) — query parameters
  - `Cookie` (`Cookie`) — cookie management: `Add` (client/request.go:781), `Del` (786), `SetCookie` (791), `All` (816)
  - `PathParam` — path parameters: `Add` (client/request.go:829), `Del` (834), `SetParam` (839)
  - `FormData` (`FormData`, client/request.go:874) — form data
  - `File` (`File`, client/request.go:932) — file uploads
- `WithStruct` (`WithStruct`, client/request.go:24) — interface for storing data from struct via reflection
- `Request.Context` (`Request.Context`, client/request.go:115) — returns associated context with guard: `GUARD(r.ctx == nil -> return context.Back...)`
- `Request.SetContext` (`Request.SetContext`, client/request.go:124) — sets context for request cancellation

**Client-Side Response (`client/response.go`, 241 lines):**
- `Response` (`Response`, client/response.go:19) — "represents the result of a request." Methods: `Body`, `BodyStream`, `CBOR`, `Close`, `Cookies`, `Header`.
- `Response.Body` (`Response.Body`, client/response.go:88) — returns body as byte slice via `DELEGATE(r.RawResponse.Body -> result)`
- `Response.StatusCode` — HTTP status code (referenced in GAPS as uncovered)
- `Response.Protocol` (`Response.Protocol`, client/response.go:48) — HTTP protocol used
- `Response.Close` (`Response.Close`, client/response.go:208) — releases objects back to pools
- `Response.JSON` (`Response.JSON`, client/response.go:114) / `Response.CBOR` (`Response.CBOR`, client/response.go:123) — deserialization methods with guard `GUARD(r.client == nil -> return ErrClientNil)`
- `Response.Save` (`Response.Save`, client/response.go:144) — writes response body to file or writer
- `Response.setRequest` (`Response.setRequest`, client/response.go:33) — links response to its request

**Pooling:**
- `AcquireRequest` / `ReleaseRequest` (`AcquireRequest`, client/request.go:983; `ReleaseRequest`, client/request.go:993) — request object pooling
- `AcquireResponse` / `ReleaseResponse` (`ReleaseResponse`, client/response.go:238) — response object pooling
- `AcquireFile` / `ReleaseFile` (`AcquireFile`, client/request.go:1032; `ReleaseFile`, client/request.go:1053) — file object pooling

### Adaptor Module (middleware/adaptor/)

This module bridges Fiber's context/request model with `net/http`:
- `ConvertRequest` (`ConvertRequest`, middleware/adaptor/adaptor.go:89) — converts `fiber.Ctx` to `http.Request`
- `CopyContextToFiberContext` (`CopyContextToFiberContext`, middleware/adaptor/adaptor.go:101) — copies `context.Context` to `fasthttp.RequestCtx`. Source snippet: `func CopyContextToFiberContext(src any, requestContext *fasthttp.RequestCtx)`
- `HTTPHandlerWithContext` (`HTTPHandlerWithContext`, middleware/adaptor/adaptor.go:65) — preserves Fiber user context. Source snippet: `func HTTPHandlerWithContext(h http.Handler) fiber.Handler`
- `LocalContextFromHTTPRequest` (`LocalContextFromHTTPRequest`, middleware/adaptor/adaptor.go:78) — extracts Fiber user context from `http.Request`. Source snippet: `func LocalContextFromHTTPRequest(r *http.Request) (context.Context, bool)`

### Client Hooks (`client/hooks.go`)

- `logger` (`logger`, client/hooks.go:345) — response hook for debug logging with guard `GUARD(!c.debug -> return nil)`
- `parserRequestHeader` (`parserRequestHeader`, client/hooks.go:122) — merges client/request headers

### Client Core (`client/core.go`)

- `core.execute` (`core.execute`, client/core.go:209) — runs all hooks, applies timeouts, sends request, and runs response hooks
- `core.execFunc` (`core.execFunc`, client/core.go:74) — core send/receive logic calling `acquireErrChan`, `acquireResponseChan`, `getRetryConfig`

### What Cannot Be Determined

- The full set of methods on the `Ctx` interface is not enumerated in the clue file.
- `App.next`, `App.nextCustom`, `Client.StreamResponseBody`, and `Response.StatusCode` are listed as uncovered in GAPS.
- The internal fields of the `Ctx` implementation (`DefaultCtx`) and how it wraps `fasthttp.RequestCtx` are not detailed.
- The complete `binder/` package organization (12 files) beyond `binder/form.go` is not shown in the FOCUS section.
