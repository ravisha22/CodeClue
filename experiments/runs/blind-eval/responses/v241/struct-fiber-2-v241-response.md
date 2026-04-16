# v2.4.1 Response: struct-fiber-2
Date: 2026-04-16

## Request Context, Routing Modules, and Request/Response Data Types

### Context Modules

- **`Ctx`** (`ctx_interface_gen.go:18`): The main interface representing the HTTP request and response context [FOCUS §Ctx].
- **`CustomCtx`** (`ctx_interface.go:13`): Extends `Ctx` with additional methods required by Fiber's internals and middleware helpers [FOCUS §CustomCtx].
- **`ctx.go`**: Contains `DefaultCtx` implementations — `DefaultCtx.Get` (`ctx.go:200`), `DefaultCtx.RequestID` (`ctx.go:311`) which checks `GetRespHeader(HeaderXRequestID)` then falls back to `Get` [FOCUS §DefaultCtx.RequestID; SYM §DefaultCtx.Get].
- **`StoreInContext`** (`helpers.go:83`): Stores key/value in both Fiber locals and the request context, with source signature `func StoreInContext(c Ctx, key, value any)` [FOCUS §StoreInContext; Source Snippet §StoreInContext].

### Context-from-Request Patterns

- **`FromContext`** (session, `middleware/session/middleware.go:179`): Extracts `*Middleware` from Fiber context via `fiber.ValueFromContext` [FOCUS §FromContext session].
- **`FromContext`** (requestid, `middleware/requestid/requestid.go:79`): Extracts request ID string from context [FOCUS §FromContext requestid].
- **`TokenFromContext`** (`middleware/keyauth/keyauth.go:99`): Extracts bearer token from context [FOCUS §TokenFromContext].
- **`FromContext`** (paginate, `middleware/paginate/paginate.go:92`): Returns `PageInfo` from context [FOCUS §FromContext paginate].

### Routing Modules

- **`router.go`**: Core routing — `App.normalizePath` (`router.go:398`), `App.pruneAutoHeadRouteLocked` (`router.go:491`) [SYM §App.normalizePath, §App.pruneAutoHeadRouteLocked]. `App.next` and `App.nextCustom` are listed as uncovered in GAPS.
- **`path.go`** (844 lines): Path matching and constraint checking — `CheckConstraint`, `Constraint`, `CustomConstraint`, `GetTrimmedParam`, `RemoveEscapeChar` [INDEX §path.go].
- **`domain.go`** (688 lines): Domain-based routing — `domainMatcher.match` (`domain.go:139`), `domainRouter` methods [SYM §domainMatcher.match; INDEX §domain.go].
- **`group.go`**: Route groups — `Group.Add` (`group.go:167`) [SYM §Group.Add].
- **`register.go`**: Registration interface — `Registering.Add` (`register.go:111`) [SYM §Registering.Add].
- **`redirect.go`** (433 lines): Redirect handling — `AcquireRedirect`, `Back`, `Message` [INDEX §redirect.go].

### Server-Side Request Data Types

- **`req.go`** (1,140+ lines): `DefaultReq` methods — `DefaultReq.Get` (`req.go:427`), `DefaultReq.Accepts` (`req.go:51`), `DefaultReq.Body` (`req.go:149`), `DefaultReq.IsProxyTrusted` (`req.go:1080`), `DefaultReq.MediaType` (`req.go:244`) [SYM §DefaultReq.*].
- **`bind.go`** (477 lines): `Bind` struct (`bind.go:40`) providing binding helpers (`All`, `Body`, `CBOR`, `Cookie`, `Custom`, `Form`) [FOCUS §Bind; INDEX §bind.go].
- **`binder/form.go`** (124 lines): `FormBinding` with `Bind`, `Reset`, `bindMultipart` [INDEX §binder/form.go].

### Server-Side Response Data Types

- **`res.go`** (1,153 lines): `DefaultRes` methods — `DefaultRes.Render` (`res.go:691`), `DefaultRes.SendString` (`res.go:997`), plus `Cookie`, `Append`, `Attachment`, `AutoFormat` [INDEX §res.go; FOCUS §DefaultRes.Render, §DefaultRes.SendString].

### Client-Side Request & Response Types

- **`Request`** (`client/request.go:46`, 1,122 lines): HTTP request with methods `AddFile`, `AddFormData`, `AddHeader`, `Get`, `Put`, `Send`, etc. [FOCUS §Request; INDEX §client/request.go]. `Request.Context` (`client/request.go:115`) returns the associated context, guarding against nil [FOCUS §Request.Context].
- **`Response`** (`client/response.go:19`, 241 lines): HTTP response with methods `Body`, `BodyStream`, `CBOR`, `Close`, `Cookies`, `Header` [FOCUS §Response; INDEX §client/response.go]. `Response.Close` (`client/response.go:208`) releases both request and response to pools [FOCUS §Response.Close].
- **`Client`** (`client/client.go:37`, 863 lines): High-level HTTP API delegating transport to fasthttp [INDEX §client/client.go]. Hook registration via `Client.AddRequestHook` (`client/client.go:146`) and `Client.AddResponseHook` (`client/client.go:160`) [FOCUS §Client.AddRequestHook, §Client.AddResponseHook].

### Adaptor Module

The `middleware/adaptor/` module bridges Fiber and `net/http` types [FOCUS; Source Snippets]:
- `ConvertRequest` (`adaptor.go:89`): Converts `fiber.Ctx` to `*http.Request` [FOCUS §ConvertRequest].
- `CopyContextToFiberContext` (`adaptor.go:101`): Copies `context.Context` values to `fasthttp.RequestCtx` [FOCUS §CopyContextToFiberContext].
- `HTTPHandler`/`HTTPHandlerFunc` (`adaptor.go:56`/`:51`): Wrap `net/http` handlers to Fiber handlers [FOCUS §HTTPHandler, §HTTPHandlerFunc].
- `HTTPHandlerWithContext` (`adaptor.go:65`): Like `HTTPHandler` but additionally stores Fiber's user context; calls `LocalContextFromHTTPRequest` [FOCUS §HTTPHandlerWithContext].

### Execution Pipeline

`core.execute` (`client/core.go:209`) runs all hooks, applies timeouts, sends the request, and runs response hooks — guarding on `preHooks` errors and calling `afterHooks`, `execFunc`, `timeout` [FOCUS §core.execute]. `core.execFunc` (`client/core.go:74`) is the core send logic [FOCUS §core.execFunc].

### What Cannot Be Determined

- The bodies of `App.next` and `App.nextCustom` (server-side dispatch logic) [GAPS: uncovered].
- `FormData.Set` and `FormData.SetWithStruct` internals [GAPS: uncovered].
- How `Ctx` interface methods are generated (the `ctx_interface_gen.go` file is referenced but not included) [FOCUS §Ctx].
- The exact fields of the `Request` and `Response` structs (only method signatures are in the source snippets) [Source Snippets].
