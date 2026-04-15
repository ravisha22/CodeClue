# Response: rel-fiber-1
Date: 2026-04-15

From the clue file, the clearest supported model is:

1. `App` is the top-level application object. It is explicitly "the Fiber application," and it exposes route/middleware registration methods such as `Add`, `Use`, and `Group`. (`App`, `app.go:69-69`; `App.Add`, `app.go:953`; `App.Use`, `app.go:860-860`; `App.Group`, `app.go:969-969`)

2. The routing layer is surfaced through router-like objects beneath `App`. The clue excerpt does not show a standalone `Router` type definition, but it does show two router-shaped constructs:
   - `Group`, which "represents a collection of routes that share middleware and a common path prefix," and can itself `Add`, `Use`, and create another `Group`. (`Group`, `group.go:14-15`; `Group.Use`, `group.go:70-70`; `Group.Group`, `group.go:187-187`; `Group.Add`, `group.go:167`)
   - `domainRouter`, which can `Add`, `Use`, `Group`, `Name`, and has helpers such as `registerPath` and `registerGroup`. (`domainRouter.Add`, `domain.go:530`; `domainRouter.Use`, `domain.go:350-350`; `domainRouter.Group`, `domain.go:552`; `domainRouter.Name`, `domain.go:602`; `domainRouter.registerPath`, `domain.go:327`; `domainRouter.registerGroup`, `domain.go:336`)

3. So the connection from `App` to routing is that `App` is where route registration starts, and `App.Group(...)` creates sub-router structures for common prefixes and middleware. Those sub-routers can themselves keep registering more routes or nested groups. (`App.Group`, `app.go:969-969`; `Group`, `group.go:14-15`; `Group.Group`, `group.go:187-187`; `domainRouter.Group`, `domain.go:552`)

4. A `Route` appears to be the individual registered route entry managed by that routing layer. The excerpt does not include a direct `Route` type definition, but routes are clearly treated as concrete registration units because:
   - `Use` and `All` say they "register a middleware route." (`App.Use`, `app.go:860-860`; `Group.Use`, `group.go:70-70`; `domainRouter.Use`, `domain.go:350-350`; `Registering.All`, `register.go:50-50`)
   - `domainRouter.Name` assigns a name to "the most recently registered route." (`domainRouter.Name`, `domain.go:602`)
   - `App.printRoutesMessage` prints all routes with method, path, name, and handlers. (`App.printRoutesMessage`, `listen.go:516-517`)
   - Request matching is described in router/route terms: `DefaultCtx.Matched` says the request path was matched by "the router," and `RoutePatternMatch` checks whether a path matches a Fiber route pattern. (`DefaultCtx.Matched`, `ctx.go:375-376`; `RoutePatternMatch`, `path.go:155-155`)

5. Putting that together, the supported relationship is: `App` is the top-level application and entry point; the "Router" role is carried by router-like registration objects (`App` itself at the top, plus `Group`/`domainRouter` for nested scopes); and `Route` is the per-endpoint registration record produced by `Add`/`Use`/`All`, which can then be named, listed, and matched. (`App`, `app.go:69-69`; `App.Add`, `app.go:953`; `App.Use`, `app.go:860-860`; `App.Group`, `app.go:969-969`; `Group`, `group.go:14-15`; `domainRouter.registerPath`, `domain.go:327`; `domainRouter.registerGroup`, `domain.go:336`; `domainRouter.Name`, `domain.go:602`; `App.printRoutesMessage`, `listen.go:516-517`; `DefaultCtx.Matched`, `ctx.go:375-376`; `RoutePatternMatch`, `path.go:155-155`)