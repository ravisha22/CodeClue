# Cross-Model (Goldeneye): blind-echo-rel-1
Date: 2026-04-16

During normal dispatch, `Echo` is the central owner, `Group` is a scoped registration layer on top of it, `Context` is the per-request carrier, and handlers/middleware act on that context:

- `Echo` is the top-level framework instance, and it owns request entry points like `ServeHTTP`, route registration, middleware registration, and the context pool (`AcquireContext` / `ReleaseContext`). [Echo, echo.go:68-68; Echo.ServeHTTP, echo.go:695-695; Echo.Use, echo.go:431-431; Echo.AcquireContext, echo.go:684-684; Echo.ReleaseContext, echo.go:690-690]
- `Group` is a sub-router attached to an `Echo`. `Echo.Group` “creates a new router group with prefix and optional group-level middleware,” and the group’s HTTP methods mostly delegate back through `g.Add` / `AddRoute`. [Echo.Group, echo.go:659-659; Group.Add, group.go:158-158; Group.GET, group.go:37-37; Group.Match, group.go:77-77]
- `DefaultRouter` is the registry that matches requests to registered routes for an `Echo` instance. [DefaultRouter, router.go:60-60]
- `Context` represents the current HTTP request and carries the request, response, route info, path values, and a back-reference to the owning `Echo`. [Context, context.go:40-40; Context.Request, context.go:129-129; Context.SetRequest, context.go:134-134; Context.InitializeRoute, context.go:263-263; Context.Echo, context.go:665-665]
- Handlers are registered through `Echo.Add(...)` / group methods and then execute against `Context`; response helpers such as `Context.json(...)` write the response by delegating to `c.echo.JSONSerializer.Serialize`. [Echo.Add, echo.go:642-642; Group.GET, group.go:37-37; Context.json, context.go:464-464]
- Middleware wraps that handler flow. For example, `RequestLogger()` creates middleware using Echo defaults and `Context.Logger()` as the logger. [RequestLogger, middleware/request_logger.go:395-395]
