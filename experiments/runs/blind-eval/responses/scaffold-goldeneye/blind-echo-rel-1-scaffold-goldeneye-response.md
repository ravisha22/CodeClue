# Scaffold (Goldeneye): blind-echo-rel-1
Date: 2026-04-16

## Relevant symbols traced
- `Echo` is the top-level instance and owns routing, middleware, and context pooling. [Echo (echo.go:68-68); Echo.Use (echo.go:431-431); Echo.AcquireContext (echo.go:684-684); Echo.ReleaseContext (echo.go:690-690)]
- `Group` is a prefixed sub-route wrapper that delegates back into `Echo`'s routing. [Group (group.go:14-14); Group.Add (group.go:158-158); Group.AddRoute (group.go:172-172); Echo.Group (echo.go:659-659)]
- `Context` is the current request object and carries route/request/response state. [Context (context.go:40-40); Context.InitializeRoute (context.go:263-263); Context.Request (context.go:129-129); Context.Echo (context.go:665-665)]

## Answer
During normal dispatch, the relationship looks like this:

1. **`Echo` owns the application-level dispatch machinery.** It is the “top-level framework instance,” implements `ServeHTTP`, and exposes `Use` for middleware and `Group`/`Add` for route registration. [Echo (echo.go:68-68); Echo.ServeHTTP (echo.go:695-695); Echo.Use (echo.go:431-431); Echo.Add (echo.go:642-642); Echo.Group (echo.go:659-659)]
2. **`Group` is a thin sub-routing facade over `Echo`.** Its verb helpers (`GET`, `POST`, `Any`, etc.) all delegate to `Add`, `Add` calls `AddRoute`, and `AddRoute` delegates to `g.echo.add`, which shows that groups contribute prefixed routes into the same underlying router owned by `Echo`. [Group.GET (group.go:37-37); Group.Any (group.go:72-72); Group.Add (group.go:158-158); Group.AddRoute (group.go:172-172)]
3. **`DefaultRouter` is the registry that matches incoming requests.** The clue states that `DefaultRouter` stores all registered routes for request matching and URL path-parameter handling. [DefaultRouter (router.go:60-60)]
4. **`Context` is the per-request object handed through the pipeline to handlers.** It represents the current HTTP request, can expose the associated `Echo`, request, and response, and it is where route/path state is initialized. [Context (context.go:40-40); Context.Echo (context.go:665-665); Context.Request (context.go:129-129); Context.Response (context.go:139-139); Context.InitializeRoute (context.go:263-263)]
5. **`Echo` allocates and recycles that `Context`.** `AcquireContext` gets one from the pool, `newContext`/`SetRequest` establish request state, and `ReleaseContext` returns it after handling. [Echo.AcquireContext (echo.go:684-684); Context.SetRequest (context.go:134-134); Echo.ReleaseContext (echo.go:690-690)]
6. **Middleware sits between route matching and the handler.** `Echo.Use` explicitly says its middleware runs after the router has found a matching route and before the route/request handler, and `RequestLogger` is one example middleware built on the `Context`. [Echo.Use (echo.go:431-431); RequestLogger (middleware/request_logger.go:395-395)]

## Gaps / uncertainty
The evidence is strong on the object relationships, but the exact body-level order inside `ServeHTTP` is not fully shown; the prompt itself marks this as mechanistic and notes uncovered areas. [GAPS]
