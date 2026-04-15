# Response: blind-fiber-1 (summary baseline)
Date: 2026-04-15

Based solely on the summary, I cannot recover Fiber's exact redispatch API or internal control flow, but I can infer the likely responsibilities from the file layout.

What the summary strongly suggests:
- `app.go` probably owns the high-level request handling pipeline.
- `router.go` likely performs route matching and dispatch decisions.
- `path.go` likely contains path normalization or matching helpers.
- `middleware/` being very large indicates requests can pass through middleware before final route resolution.
- `register.go`, `group.go`, and `mount.go` suggest the router maintains structured route registrations.
- `router_test.go`, `path_test.go`, and `app_test.go` likely verify the behaviors asked about.

From that structure, the most reasonable inference is:
1. Middleware can modify the request path in the request context.
2. If middleware wants Fiber to match routes again, control likely returns to routing logic in `app.go`/`router.go` rather than simply continuing with the old matched handler.
3. The router then re-runs path and method matching against the registered routes.
4. If the rewritten path now matches a route for the current HTTP method, dispatch proceeds as a normal match.
5. If the rewritten path matches no route at all, the framework likely produces a 404.
6. If the rewritten path matches a path pattern but not for the current method, the router likely produces a 405.

What I cannot determine from the summary:
- The exact method/function used to restart dispatch.
- Whether the middleware/handler index is reset.
- Whether route parameters are recomputed from scratch.
- How the framework distinguishes 404 from 405 internally.
- Whether any flags on the context suppress or force rematching.

So the summary supports the general conclusion that path-rewrite redispatch is handled by re-entering the app/router matching flow, with `router.go` deciding between normal match, 404, and 405 based on the rewritten path and HTTP method. The exact mechanism is not visible from the summary alone.
