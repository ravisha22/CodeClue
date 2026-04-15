# Response: blind-echo-rel-1
Date: 2026-04-15

## Answer
During normal request dispatch, the main relationship appears to be: **`Echo` owns routing and middleware setup, `Group` is a route-registration facade over `Echo`, `Context` carries per-request state, and handlers are the functions attached to routes.**

- `Echo` is the top-level framework instance. Its router side is represented by `DefaultRouter`, which is the registry of all registered routes for an `Echo` instance for request matching and URL path parameters. (Echo, `echo.go:68-68`; DefaultRouter, `router.go:60-60`)
- Handlers are registered on `Echo` through methods like `Add`, `AddRoute`, and `GET`. `Echo.add` calls `AddRoute`, and `Echo.GET` delegates to `Add`. (Echo.Add, `echo.go:642-642`; Echo.AddRoute, `echo.go:617-617`; Echo.add, `echo.go:621-621`; Echo.GET, `echo.go:449-449`)
- `Group` is a sub-routing abstraction layered on top of `Echo`: it is "a set of sub-routes for a specified route," and its route methods (`GET`, `Any`, etc.) delegate back into `Add` / `AddRoute`. (Group, `group.go:14-14`; Group.GET, `group.go:37-37`; Group.Any, `group.go:72-72`; Group.Add, `group.go:158-158`; Group.AddRoute, `group.go:172-172`)
- `Echo.Use` is part of the dispatch relationship because it adds middleware that runs after the router has found the matching route and before the route/request handler method executes. (Echo.Use, `echo.go:431-431`)
- `Context` is the per-request object passed through request handling. It represents the current HTTP request and exposes accessors for request, response, route info, cookies, binding, and response writing. (Context, `context.go:40-40`; Context.Request source snippet, `context.go L129-129`; Context.Response source snippet, `context.go L139-139`; Context.Bind, `context.go:399-399`; Context.RouteInfo source snippet, `context.go L225-225`)
- Route matching feeds data into `Context`: `Context.InitializeRoute` sets route-related variables of the request, taking a `*RouteInfo` and `*PathValues`, and it calls `setPathValues`. (Context.InitializeRoute, `context.go:263-263`; Context.setPathValues source snippet, `context.go L269-269`)
- `Context.Reset` shows the same context object is reset after a request completes, which implies `Context` participates in the request lifecycle rather than being just a passive DTO. (Context.Reset, `context.go:107-107`)
- `Context.Bind` delegates to `c.echo.Binder.Bind`, which directly connects the per-request `Context` back to framework-level services owned by `Echo`. (Context.Bind, `context.go:399-399`)
- The response path also runs through `Context`: methods like `HTML`, `JSON`, `XML`, `Blob`, `String`, and `Redirect` are all on `Context`, so handlers appear to use `Context` both to read request data and produce the response. (Context.HTML source snippet, `context.go L435-435`; Context.JSON source snippet, `context.go L482-482`; Context.XML source snippet, `context.go L531-531`; Context.Blob, `context.go:552-552`; Context.String source snippet, `context.go L445-445`; Context.Redirect, `context.go:642-642`)

## What I cannot determine
- I cannot determine the exact internal call order among router match, middleware application, and handler execution, because the prompt shows the router, middleware hook, and context setup points, but not the full request-dispatch body. (DefaultRouter, `router.go:60-60`; Echo.Use, `echo.go:431-431`; applyMiddleware, `echo.go:785-785`; Context.InitializeRoute, `context.go:263-263`)
- I cannot determine the exact definition of `HandlerFunc`, only that route-registration methods accept it. (Echo.GET, `echo.go:449-449`; Group.Add, `group.go:158-158`)
- I cannot determine whether `Group` owns its own router instance or always delegates to `Echo`'s router beyond the documented delegation points shown here. (Group.AddRoute, `group.go:172-172`; DefaultRouter, `router.go:60-60`)
