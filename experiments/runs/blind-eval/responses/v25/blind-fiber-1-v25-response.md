# v2.5 Response: blind-fiber-1
Date: 2026-04-16

## Question

If middleware rewrites the request path and wants Fiber to match routes again, how does the framework restart dispatch and decide whether the request becomes a normal match, a 404, or a 405?

## Relevant Symbols Identified

The key symbols are:

- **`DefaultCtx.RestartRouting`** (ctx.go:265-266) — the entry point for restarting dispatch
- **`App.next`** (router.go:115) — main route-matching dispatch loop
- **`App.nextCustom`** (router.go:216) — alternative dispatch path
- **`DefaultCtx.Path`** (ctx.go:297) — reads/overrides the request path
- **`DefaultCtx.configDependentPaths`** (ctx.go:632) — sets paths for route recognition
- **`App.normalizePath`** (router.go:398) — normalizes path before matching
- **`routeParser.getMatch`** (path.go:507) — tries to match a URL against route segments

## Tracing the Restart Dispatch Flow

### 1. Path Rewriting by Middleware

A middleware can override the request path using **`DefaultCtx.Path`** (ctx.go:297, FOCUS). Its signature is `DefaultCtx.Path(override ...string)`, meaning it accepts an optional override string. When called with an argument, it sets the path. Its behavior annotation is `DELEGATE(c.app.toString -> result)` and it calls **`configDependentPaths`** (ctx.go:632, SYM), which is described as "set paths for route recognition." This means the overridden path is propagated into the internal detection/routing path used by the matching engine.

### 2. Triggering RestartRouting

After rewriting the path, the middleware calls **`DefaultCtx.RestartRouting`** (ctx.go:265-266, FOCUS). Its behavior annotation is:

> `GUARD(c.handlerCtx != nil -> return err)`

This guard checks that `c.handlerCtx` is not nil (i.e., the context is valid and has an active handler context). If the guard condition fails (handlerCtx is nil), it returns an error.

When the guard passes, `RestartRouting` calls **`App.next`** (router.go:115, SYM) and **`App.nextCustom`** (router.go:216, SYM). This effectively re-enters the framework's dispatch loop from scratch with the newly rewritten path, rather than proceeding to the next handler in the current middleware chain.

### 3. Route Matching Decision (Normal Match, 404, or 405)

The dispatch functions `App.next` and `App.nextCustom` are responsible for iterating over registered routes and determining the outcome. Based on the clue evidence:

- **`App.next`** (router.go:115) is the primary matching function. Per the INDEX, router.go (767 lines) also contains `RebuildTree`, `RemoveRoute`, `addPrefixToRoute`, and `App.addRoute` — indicating it houses the core routing tree logic.

- **`App.normalizePath`** (router.go:398, SYM) normalizes the path before matching begins.

- The actual pattern matching is done by **`routeParser.getMatch`** (path.go:507, FOCUS), which "parses the passed url and tries to match it against the route segments and determine the parameter positions." Its behavior is `GUARD(detectionPath != "" -> return false); ACCUMULATE(len loop -> result)`. It calls **`CheckConstraint`**, **`findParamLen`**, and **`hasPartialMatchBoundary`** (path.go:486, FOCUS) to validate segment boundaries.

- **`App.methodInt`** (helpers.go:923, SYM) converts HTTP methods to unique integers — this is used during dispatch to filter routes by method.

The outcome determination follows this logic (inferred from the routing structure):

1. **Normal match**: `getMatch` returns `true` for a route whose method matches the request method. The associated handlers execute.

2. **404 (Not Found)**: No route pattern matches the rewritten path for *any* HTTP method. The dispatch loop exhausts all candidates and falls through without a match.

3. **405 (Method Not Allowed)**: A route pattern matches the rewritten path, but the HTTP method does not match any registered method for that path. The framework detects that the path exists but the method is wrong, via the method integer comparison (`App.methodInt`).

### 4. What Happens After RestartRouting Returns

Since `RestartRouting` re-enters `next`/`nextCustom`, the result of the new dispatch determines what error (if any) propagates. If no route matches, the error flows to the error handler chain. **`DefaultCtx.Path`** is listed as `called_by: ErrorHandler` (FOCUS), confirming the error handler inspects the path when formatting the error response.

## Gaps and Uncertainty

Per the GAPS section:

> **uncovered: App.nextCustom, App.next, Request.AddFile, App.processSubAppsRoutes**

The body logic of `App.next` and `App.nextCustom` is explicitly listed as uncovered. This means:

- **Cannot determine**: The exact internal mechanism by which `next`/`nextCustom` distinguish a 404 from a 405 — whether it uses a two-pass approach (first match path, then check method), a flag, or a separate method-checking loop.
- **Cannot determine**: Whether `RestartRouting` resets the handler index or any other context state before re-entering `next`/`nextCustom`.
- **Cannot determine**: How `nextCustom` differs from `next` — its name suggests custom/domain-based routing, but its body is uncovered.

The GAPS type is `MECHANISTIC (body logic needed for full answer)`, confirming that the internal dispatch mechanics are not fully traceable from the available evidence.

## Summary

Middleware rewrites the path via **`DefaultCtx.Path`** (ctx.go:297), which updates internal detection paths through **`configDependentPaths`** (ctx.go:632). It then calls **`DefaultCtx.RestartRouting`** (ctx.go:265-266), which guards on `handlerCtx != nil` and re-enters the dispatch loop via **`App.next`** (router.go:115) and **`App.nextCustom`** (router.go:216). These functions use **`routeParser.getMatch`** (path.go:507) for pattern matching and **`App.methodInt`** (helpers.go:923) for method filtering to determine whether the result is a normal match, a 404 (no path match), or a 405 (path matches but method does not). However, the exact internal logic of `next` and `nextCustom` is explicitly uncovered in the clue (GAPS), so the precise mechanism for distinguishing 404 vs. 405 cannot be fully confirmed from the available evidence.
