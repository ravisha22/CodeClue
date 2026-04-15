# Response: blind-fiber-1 (with drill-down)
Date: 2026-04-15

Based only on the clue file and drill-down snippets, I can determine the routing behavior at a **mechanistic, partial** level, but not the exact internal restart routine name or full control-flow implementation. The clue file itself marks this area as a mechanistic gap needing body logic (`-- GAPS`, `type: MECHANISTIC`) [Clue File: GAPS].

## What can be determined

1. **Middleware can change the effective request path used for routing.**  
   The request path is exposed through `DefaultCtx.Path(override ...string)`, and its signature explicitly allows an override argument rather than read-only access [Clue File: `DefaultCtx.Path`]. That supports the conclusion that middleware can rewrite the path that later routing decisions will use.

2. **Middleware routes are part of the dispatch pipeline, and the current handler can be identified as middleware.**  
   `App.Use`, `Group.Use`, and `domainRouter.Use` all register “a middleware route” matching a provided prefix [Clue File: `App.Use`, `Group.Use`, `domainRouter.Use`]. `DefaultCtx.IsMiddleware` reports whether the current request handler was registered as middleware [Clue File: `DefaultCtx.IsMiddleware`]. So the scenario in the question—middleware rewriting a path and then wanting routing to happen again—is consistent with the router having both middleware and non-middleware phases.

3. **A re-dispatch would have to re-run route-pattern matching against the updated path.**  
   The clue file names `RoutePatternMatch(path, pattern string, cfg ...Config)` and says it “reports whether path matches the provided Fiber route pattern” [Clue File: `RoutePatternMatch`]. Therefore, if middleware rewrites the request path, the framework’s decision on the second pass must be driven by matching the new path against route patterns again.

4. **A successful second-pass route selection would surface as a normal match.**  
   `DefaultCtx.Matched` returns true if “the current request path was matched by the router” [Clue File: `DefaultCtx.Matched`]. So if re-dispatch after the rewrite finds a route whose pattern matches the rewritten path, the request becomes a normal routed match.

5. **The router tracks both path matching and HTTP-method constraints.**  
   `App.Add`, `Group.Add`, `domainRouter.Add`, and `Registering.Add` all say they allow specifying **multiple HTTP methods** [Clue File: `App.Add`, `Group.Add`, `domainRouter.Add`, `Registering.Add`; Source Snippet: `Group.Add`, `Registering.Add`]. Also, `Registering.All` and the `Register` interface show a route-registration API that can target all methods [Clue File: `Registering.All`; Source Snippet: `Register`, `Registering.All`]. This is enough to conclude that dispatch is not just path-based; method eligibility is a separate part of route resolution.

6. **From that split, the likely 404 vs 405 distinction can be bounded as follows:**  
   - If the rewritten path does **not** match any route pattern on re-dispatch, the result would be “no matched route,” which aligns with a 404 outcome. This is supported by the existence of explicit path-pattern matching (`RoutePatternMatch`) and matched-state reporting (`DefaultCtx.Matched`) [Clue File: `RoutePatternMatch`, `DefaultCtx.Matched`].  
   - If the rewritten path **does** match some route pattern, but the request method is not one of the methods registered for that route, the method dimension becomes the differentiator, which is the only evidence in the prompt that explains how a non-404 failure mode such as 405 could arise [Clue File: `App.Add`, `Group.Add`, `domainRouter.Add`, `Registering.Add`; Source Snippet: `Group.Add`, `Registering.Add`].

## What cannot be determined from the provided material

1. **The exact API or internal function that performs the “restart dispatch.”**  
   The clue file does not show the body of any restart/re-dispatch function, and none of the drill-down snippets include it. The file explicitly says body logic is still needed for a full answer (`type: MECHANISTIC (body logic needed for full answer)`) [Clue File: GAPS].

2. **Whether restart begins from the first route, from the first non-middleware route, or from some saved index/checkpoint.**  
   No clue entry or snippet exposes that control flow.

3. **The exact implementation of the 404/405 decision.**  
   I can infer the likely distinction from the existence of route-pattern matching and multi-method registration, but the prompt does not include the actual responder/error-selection code that would prove the final branching.

## Best-supported answer

So, using only the supplied evidence: if middleware rewrites the request path, the framework can use the overridden path value from `DefaultCtx.Path(...)` [Clue File: `DefaultCtx.Path`] and then re-run routing logic that checks the rewritten path against route patterns via `RoutePatternMatch(...)` [Clue File: `RoutePatternMatch`]. If that second pass finds a route, the request is a normal match, consistent with `DefaultCtx.Matched()` becoming true [Clue File: `DefaultCtx.Matched`]. If no route pattern matches the rewritten path, the request falls into the “no matched route” case, which is the only supportable basis for a 404 from the provided material [Clue File: `RoutePatternMatch`, `DefaultCtx.Matched`]. If the rewritten path matches a route pattern but the request method is not among the methods registered for that route, the method-registration evidence (`Add(methods []string, ...)`, `All(...)`) is the only support in the prompt for the request becoming a 405 rather than a 404 [Clue File: `App.Add`, `Group.Add`, `domainRouter.Add`, `Registering.Add`, `Registering.All`; Source Snippet: `Group.Add`, `Registering.Add`, `Registering.All`, `Register`].

That is the strongest answer the supplied clue file and snippets support without importing any outside knowledge.
