# Cross-Model (GPT-5.4-mini): blind-echo-struct-2
Date: 2026-04-16

- `Echo` is the top-level framework instance, and it owns the main routing/dispatch entrypoints such as `Add`, `AddRoute`, `Any`, `CONNECT`, `DELETE`, `GET`, `HEAD`, `OPTIONS`, `PATCH`, `POST`, `PUT`, `RouteNotFound`, `ServeHTTP`, and `Group`. (Echo (echo.go:68-68); Echo.ServeHTTP (echo.go:695-695); Echo.Group (echo.go:659-659))
- `Router` is the routing interface, and `DefaultRouter` is the concrete registry used for request matching and URL/path-param handling. (Router (router.go:21-21); DefaultRouter (router.go:60-60))
- `Group` is the sub-route container; its methods delegate route registration back through `Add`/`AddRoute` and related helpers. (Group (group.go:14-14); Group.Add (group.go:158-158); Group.AddRoute (group.go:172-172); Group.GET (group.go:37-37); Group.StaticFS (group.go:122-122))
- `Context` represents the current HTTP request and exposes request-bound helpers like `Request`, `SetRequest`, `Bind`, `Response`, `Cookie`, `Cookies`, `QueryParam`, and `FormValue`. (Context (context.go:40-40); Context.Request (context.go:129-129); Context.SetRequest (context.go:134-134); Context.Bind (context.go:399-399); Context.Response (context.go:139-139))
- Route metadata helpers also exist as `RouteInfo.Reverse` and `Routes.Reverse`, and request-handling errors are represented by `HTTPError`. (RouteInfo.Reverse (route.go:75-75); Routes.Reverse (route.go:117-117); HTTPError (httperror.go:107-107))
