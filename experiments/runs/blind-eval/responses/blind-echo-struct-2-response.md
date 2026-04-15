# Response: blind-echo-struct-2
Date: 2026-04-15

## Answer
Echo's routing and request-handling surface is made up of a few central public types plus supporting subcomponents.

- `Echo` is the top-level framework instance and the main entry point for registering routes and starting request handling. Its listed methods include `AcquireContext`, `Add`, `AddRoute`, `Any`, `CONNECT`, and `DELETE`, and the focus section also shows `Use` and `Start`. (Echo, `echo.go:68-68`; Echo.Use, `echo.go:431-431`; Echo.Start, `echo.go:744-744`)
- `Group` is the public sub-routing type. It is described as "a set of sub-routes for a specified route" and exposes route-registration helpers such as `Add`, `AddRoute`, `GET`, `Any`, and `StaticFS`. (Group, `group.go:14-14`; Group.Add, `group.go:158-158`; Group.GET, `group.go:37-37`; Group.StaticFS, `group.go:122-122`)
- The routing backend is represented by the `Router` interface and its concrete/default implementation `DefaultRouter`, which is the registry of all registered routes for an `Echo` instance and supports `Add`, `Remove`, `Route`, and `Routes`. (Router, `router.go:21-21`; DefaultRouter, `router.go:60-60`)
- Route metadata and path-parameter pieces are also part of the surface: `Context.InitializeRoute` takes `*RouteInfo` and `*PathValues`, and `PathValue` is explicitly called out as a path-parameter tuple type. (Context.InitializeRoute, `context.go:263-263`; PathValue, `router.go:1051-1051`)
- `Context` is the per-request public type. It represents the current HTTP request and exposes request/response methods such as `Attachment`, `Bind`, `Blob`, `Cookie`, `Cookies`, `Request`, `Response`, `Redirect`, `SetPathValues`, and `RouteInfo`. (Context, `context.go:40-40`; Context.Bind, `context.go:399-399`; Context.Cookie, `context.go:364-364`; Context.Response, `context.go:139-139`; Context.Redirect, `context.go:642-642`; Context.SetPathValues, `context.go:255-255`; Context.RouteInfo, `context.go:225-225`)
- Request data binding is handled by public binder-related types and functions: `BindBody`, `BindPathValues`, `ValueBinder`, and `BindingError`. `ValueBinder` is described as a utility for binding query/path parameters to built-in types. (BindBody, `bind.go:66-66`; BindPathValues, `bind.go:42-42`; ValueBinder, `binder.go:92-92`; BindingError, `binder.go:69-69`)
- Error handling is also part of the request-handling surface: `HTTPError` represents an error that occurred while handling a request and exposes `Error`, `StatusCode`, `Unwrap`, and `Wrap`. (HTTPError, `httperror.go:107-107`)
- Server startup/configuration participates in the same surface via `StartConfig`, which is used to create configured `http.Server` instances for serving requests with an `Echo` instance. (StartConfig, `server.go:26-26`)
- There are auxiliary public subcomponents around request handling, including `NewVirtualHostHandler` for host-based dispatch and `RequestLogger` / `RequestLoggerConfig` for request-logging middleware tied to `Context.Logger()`. (NewVirtualHostHandler, `vhost.go:10-10`; RequestLogger, `middleware/request_logger.go:395-395`; RequestLoggerConfig, `middleware/request_logger.go:124-124`; RequestLoggerValues, `middleware/request_logger.go:189-189`)
- The testing surface includes `ContextConfig`, which can create test contexts and response recorders. (ContextConfig, `echotest/context.go:20-20`; ContextConfig.ToContextRecorder, `echotest/context.go:81-81`)

## What I cannot determine
- I cannot determine the full shape of hidden types like `RouteInfo`, `PathValues`, `Router`, or `Echo`, because the prompt gives descriptions and method lists, but not their full declarations or fields.
- I cannot determine the exact handler function type definition from this prompt, even though many methods accept `HandlerFunc`. That name appears in signatures, but its definition is not shown. (Group.Add, `group.go:158-158`; Group.GET, `group.go:37-37`; Echo.Add, `echo.go:642-642`)
- I also cannot determine whether the listed middleware/config types are exhaustive for request handling, because the clue file explicitly truncates the symbol list (`...and 487 more symbols`). (SYM summary, line 118)
