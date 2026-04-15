# Response: struct-fiber-2
Date: 2026-04-15

Based only on the clue file, Fiber’s **request context** appears to be handled primarily by the context-related modules:

- `ctx.go` is a main request-context module because `DefaultCtx` exposes operations on the current request context such as `Get`, `GetHeaders`, `Matched`, `IsMiddleware`, `Path`, and `String`. [DefaultCtx.Get — `ctx.go:200`; DefaultCtx.GetHeaders — `ctx.go:207`; DefaultCtx.Matched — `ctx.go:375-376`; DefaultCtx.IsMiddleware — `ctx.go:380-381`; DefaultCtx.Path — `ctx.go:297-297`; DefaultCtx.String — `ctx.go:571`]
- `ctx_interface.go` is also part of request-context handling because `CustomCtx` is described as extending `Ctx` with additional methods required by Fiber internals and middleware helpers. [CustomCtx — `ctx_interface.go:13-14`]
- `helpers.go` participates in request-context handling through `StoreInContext`, which explicitly stores key/value pairs in both Fiber locals and request context. [StoreInContext — `helpers.go:83-83`]
- `middleware/adaptor/adaptor.go` bridges request context between Fiber and HTTP/context types through `HTTPHandlerWithContext`, `ConvertRequest`, and `CopyContextToFiberContext`. [HTTPHandlerWithContext — `middleware/adaptor/adaptor.go:65-65`; ConvertRequest — `middleware/adaptor/adaptor.go:89-89`; CopyContextToFiberContext — `middleware/adaptor/adaptor.go:101-101`]

Fiber’s **routing** appears to be handled by these routing modules:

- `app.go` defines `App`, the application type, and provides route registration/grouping entry points such as `Add`, `Group`, and `Use`. [App — `app.go:69-69`; App.Add — `app.go:953`; App.Group — `app.go:969-969`; App.Use — `app.go:860-860`]
- `group.go` defines `Group`, described as “a collection of routes that share middleware and a common path prefix,” and provides grouped routing methods including `Add`, `Group`, and `Use`. [Group — `group.go:14-15`; Group.Add — `group.go:167`; Group.Group — `group.go:187-187`; Group.Use — `group.go:70-70`]
- `domain.go` defines `domainRouter`, which handles route registration and grouping at the domain level via `Add`, `Group`, `Use`, `registerPath`, and `registerGroup`. [domainRouter.Add — `domain.go:530`; domainRouter.Group — `domain.go:552`; domainRouter.Use — `domain.go:350-350`; domainRouter.registerPath — `domain.go:327`; domainRouter.registerGroup — `domain.go:336`]
- `register.go` contributes to routing registration through `Registering.Add` and `Registering.All`. [Registering.Add — `register.go:111`; Registering.All — `register.go:50-50`]
- `path.go` supports routing behavior through `RoutePatternMatch`, which reports whether a path matches a Fiber route pattern. [RoutePatternMatch — `path.go:155-155`]

For the **request and response data types**:

- The clue file explicitly defines `Request` in `client/request.go` and says it “contains all data related to an HTTP request.” [Request — `client/request.go:46-46`]
- The response type is located in `client/response.go`, as shown by response methods such as `Response.Body`. [Response.Body — `client/response.go:88`]
- Request-oriented top-level API is also present in `req.go`, where request-facing members such as `DefaultReq.Body`, `DefaultReq.Get`, `DefaultCtx.MediaType`, and `DefaultCtx.HasHeader` are located. [DefaultReq.Body — `req.go:149`; DefaultReq.Get — `req.go:427`; DefaultCtx.MediaType — `req.go:244`; DefaultCtx.HasHeader — `req.go:239`]
