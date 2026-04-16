# v2.5 Response: blind-gin-mech-1
Date: 2026-04-16

## Question
How does Gin's documented router behavior handle named parameters, catch-all parameters, exact matches, and redirects when routes overlap?

## Answer

The clue file and source snippets reveal a radix-tree-based router with named/catch-all parameter support, handler chain composition, and redirect helpers for trailing slashes and case-insensitive matching.

### 1. Route Registration Pipeline

**`RouterGroup.handle`** (source snippet, `routergroup.go:86`): the internal registration method. Signature: `func (group *RouterGroup) handle(httpMethod, relativePath string, handlers HandlersChain) IRoutes`. Behavior: `DELEGATE(group.returnObj -> result)`. Calls:
- `calculateAbsolutePath` (`routergroup.go:250`): behavior `DELEGATE(joinPaths -> result)`. Joins the group's base path with the relative path, producing the absolute route path.
- `combineHandlers` (`routergroup.go:241`): merges group-level handlers (middleware) with route-level handlers.
- `returnObj` (`routergroup.go:254`): behavior `GUARD(group.root -> return group.engine)` — returns the engine for method chaining.

All HTTP verb shortcuts delegate to `handle`:
- `GET` (`routergroup.go:116`), `POST` (111), `PUT` (131), `DELETE` (121), `PATCH` (126), `HEAD` (141), `OPTIONS` (136) — all `DELEGATE(group.handle -> result)`.
- `Any` (`routergroup.go:147`): "registers a route that matches all the HTTP methods." Loops through all methods calling `handle`.
- `Match` (`routergroup.go:156`): "registers a route that matches the specified methods that you declared." Loops through specified methods.

**`RouterGroup.Handle`** (`routergroup.go:103`): the public registration method. Behavior: `GUARD(matched := regEnLetter.MatchString(httpMethod) -> panic("http method..."))` — validates the HTTP method string with a regex and panics on invalid input.

### 2. Named Parameters and Catch-All Parameters

**`Param`** (INDEX: `tree.go`, line 950): the `tree.go` file (950 lines) contains `Param`, `ByName`, `Get`, `countParams`, `countSections`. This is the radix tree implementation.

**`Params.Get`** (`tree.go:29`): "returns the value of the first Param which key matches the given name." This is how named parameter values are retrieved.

**`RouterGroup.staticFileHandler`** (`routergroup.go:181`): behavior `GUARD(strings.Contains(relativePath, ":") || string... -> panic("URL paramet..."))`. This guard panics if a static file route contains `:` (named parameter) or `*` (catch-all parameter) syntax, confirming that `:param` and `*param` are the parameter syntaxes.

**`RouterGroup.createStaticHandler`** (`routergroup.go:216`): calls `Param` (from tree.go), `Open`, and `calculateAbsolutePath`. Called by `StaticFS`. This demonstrates catch-all parameters in action for static file serving.

**`Context.AddParam`** (`context.go:512`, referenced in blind-gin-rel-1): "adds param to context and replaces path param key with given value for e2e testing purposes. Example Route: '/us...'", showing path parameters are `:key`-based.

### 3. Route Tree and Matching

**`Engine.handleHTTPRequest`** (`gin.go:690`): behavior `PRECEDENCE(engine); ACCUMULATE(getValue loop -> result)`. Calls `Next`, `redirectFixedPath`, `redirectTrailingSlash`, `serveError`. The `PRECEDENCE` and `ACCUMULATE(getValue loop)` indicate the tree is walked per-method to find matching routes, with exact matches taking precedence.

**`node.findCaseInsensitivePath`** (`tree.go:671`, from blind-gin-struct-1): "makes a case-insensitive lookup of the given path and tries to find a handler." Calls `findCaseInsensitivePathRec`. This supports case-insensitive path matching.

**`Engine.updateRouteTrees`** (`gin.go:517`): behavior `ACCUMULATE(updateRouteTree loop -> result)`. Called by `Run` and `ServeHTTP`.

**`updateRouteTree`** (`gin.go:504`): behavior `GUARD(n.children == nil -> return); ACCUMULATE(updateRouteTree loop -> result)`. Recursively updates the route tree nodes.

### 4. Redirect Behavior

**`redirectRequest`** (`gin.go:820`): calls `Context.String` to write a redirect response. Called by `redirectFixedPath` and `redirectTrailingSlash`.

**`Engine.handleHTTPRequest`** calls `redirectFixedPath` and `redirectTrailingSlash` as fallbacks when no exact match is found, showing the redirect priority:
1. Try exact match in the route tree.
2. Try trailing slash redirect.
3. Try fixed (case-insensitive) path redirect.
4. Fall through to `serveError` (404/405).

### 5. 404 and 405 Handling

**`Engine.NoRoute`** (`gin.go:326`, from blind-gin-rel-1): "adds handlers for NoRoute." Calls `rebuild404Handlers`.
**`Engine.NoMethod`** (`gin.go:332`): "sets the handlers called when Engine.HandleMethodNotAllowed = true." Calls `rebuild405Handlers`.
**`Engine.rebuild404Handlers`** (`gin.go:356`) and `Engine.rebuild405Handlers` (`gin.go:360`): called by `Use` as well, confirming global middleware is prepended to 404/405 handler chains.

### 6. Route Inspection

**`Engine.Routes`** (`gin.go:390`): "returns a slice of registered routes, including some useful information, such as: the http method, path, and the handler." Behavior: `ACCUMULATE(iterate loop -> result)`.

**`RouteInfo`** (`gin.go:68`): "represents a request route's specification which contains method and path and its handler."

### What Cannot Be Determined
GAPS lists uncovered: `Engine.LoadHTMLFS`, `Engine.LoadHTMLFiles`, `Engine.LoadHTMLGlob`, `Engine.Delims`. The drill targets show `RouterGroup.handle` and `RouterGroup.HEAD` are only 1-line snippets, so the internal radix tree insertion logic is not exposed. The exact priority between named parameters, catch-all parameters, and static segments when routes overlap (e.g., `/users/:id` vs `/users/admin`) cannot be determined from the clue — only that the tree structure exists in `tree.go` (950 lines). The `redirectFixedPath` and `redirectTrailingSlash` implementations are listed as uncovered in the GAPS from other blind-gin tasks.
