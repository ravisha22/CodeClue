# Scaffold (Goldeneye): blind-echo-struct-2
Date: 2026-04-16

## Relevant symbols traced
- `Echo` is the top-level framework instance and exposes route-registration methods such as `Add`, `AddRoute`, `Any`, and the verb helpers. [Echo (echo.go:68-68); Echo.Add (echo.go:642-642); Echo.AddRoute (echo.go:617-617); Echo.Any (echo.go:504-504)]
- `Router` is the routing interface, and `DefaultRouter` is the concrete route registry for matching requests and URL path parameters. [Router (router.go:21-21); DefaultRouter (router.go:60-60)]
- `Group` is the sub-routing surface for prefixed route sets. [Group (group.go:14-14); Group.Add (group.go:158-158); Group.GET (group.go:37-37)]
- `Context` is the per-request handling surface. [Context (context.go:40-40); Context.Bind (context.go:399-399); Context.Request (context.go:129-129); Context.Response (context.go:139-139)]

## Answer
Echo's routing and request-handling surface is made up of a small set of public types and subcomponents:

1. **Top-level app and route registration:** `Echo` is the main public framework object, and it owns route registration (`Add`, `AddRoute`, `Any`, plus method helpers), middleware registration (`Use`), server startup (`Start`), and wrapper helpers (`WrapHandler`, `WrapMiddleware`). [Echo (echo.go:68-68); Echo.Add (echo.go:642-642); Echo.Use (echo.go:431-431); Echo.Start (echo.go:744-744); WrapHandler (echo.go:752-752); WrapMiddleware (echo.go:766-766)]
2. **Routing registry:** the routing subsystem is represented by the public `Router` interface and the `DefaultRouter` implementation, which the clue describes as the registry of all registered routes used for request matching and URL path-parameter handling. [Router (router.go:21-21); DefaultRouter (router.go:60-60)]
3. **Sub-routing groups:** `Group` is the public way to define sub-routes under a prefix. Its methods (`GET`, `Any`, `Add`, `AddRoute`, `StaticFS`, etc.) mirror the top-level `Echo` surface for nested route trees. [Group (group.go:14-14); Group.GET (group.go:37-37); Group.Any (group.go:72-72); Group.Add (group.go:158-158); Group.AddRoute (group.go:172-172); Group.StaticFS (group.go:122-122)]
4. **Per-request context:** `Context` is the core request/response object passed through handling. It exposes request access (`Request`), response access (`Response`), binding (`Bind`), cookies and query/form access, and response writers such as `String`, `Blob`, `HTMLBlob`, `json`, and `xml`. [Context (context.go:40-40); Context.Request (context.go:129-129); Context.Response (context.go:139-139); Context.Bind (context.go:399-399); Context.QueryParam (context.go:287-287); Context.String (context.go:445-445); Context.Blob (context.go:552-552); Context.HTMLBlob (context.go:440-440); Context.json (context.go:464-464); Context.xml (context.go:517-517)]
5. **Errors and middleware-facing request utilities:** `HTTPError` is the public request-error type, while `RequestLoggerConfig`, `RequestLoggerValues`, `RequestIDConfig`, and their constructors expose middleware/configuration pieces of the request-handling surface. [HTTPError (httperror.go:107-107); RequestLoggerConfig (middleware/request_logger.go:124-124); RequestLoggerValues (middleware/request_logger.go:189-189); RequestLogger (middleware/request_logger.go:395-395); RequestIDConfig (middleware/request_id.go:11-11); RequestID (middleware/request_id.go:30-30)]

## Gaps / uncertainty
The clue is structural rather than exhaustive. It explicitly notes some uncovered `Echo` methods (`DELETE`, `File`, `HEAD`, `Match`), so the broad surface is clear even though not every public endpoint is expanded in equal detail. [GAPS]
