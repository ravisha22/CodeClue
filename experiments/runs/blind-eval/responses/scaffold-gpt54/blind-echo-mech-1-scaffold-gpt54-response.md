# Scaffold (GPT-5.4): blind-echo-mech-1
Date: 2026-04-16

## Trace
The overlap question points to `DefaultRouter.Route`, `node.findStaticChild`, `routeMethods.find`, and route registration through `Echo.Add` / `Echo.add` (`DefaultRouter.Route — router.go:791-791`; `node.findStaticChild — router.go:709-709`; `routeMethods.find — router.go:213-213`; `Echo.Add — echo.go:642-642`; `Echo.add — echo.go:621-621`).

## Answer
- **Static matching has an explicit dedicated lookup step.** `DefaultRouter.Route` calls `findStaticChild`, and `node.findStaticChild` exists specifically to search static children. That is the strongest direct evidence that static path segments are checked through a specialized branch rather than only through a generic match path (`DefaultRouter.Route — router.go:791-791`; `node.findStaticChild — router.go:709-709`).
- **Method resolution prefers an exact method handler before falling back to “any-method” handling.** `routeMethods.find(method, fallbackToAny)` has the guard `r != nil || !fallbackToAny -> return r`, which means an already-found method-specific route is kept; only when that is absent and fallback is allowed does method dispatch continue to another branch (`routeMethods.find — router.go:213-213`).
- **Route lookup is incremental and precedence-driven rather than a flat scan.** `DefaultRouter.Route` is annotated with `PRECEDENCE(...)` and `ACCUMULATE(len loop -> searchIndex)`, which shows it walks the path progressively and makes ordered decisions as it searches (`DefaultRouter.Route — router.go:791-791`).
- **Registration tracks path-parameter structure separately.** `Echo.add` has `PRECEDENCE(e -> err -> paramsCount)`, so route insertion records parameter-count-related structure when adding routes; that supports the idea that parameterized routes are treated distinctly during lookup (`Echo.add — echo.go:621-621`).
- **Static file routes do not bypass normal route registration.** `Echo.Static`, `Echo.StaticFS`, `Group.Static`, and `Group.StaticFS` all delegate into `Add` / `GET`, so static-file routes participate in the same router machinery as other registered routes (`Echo.Static — echo.go:533-533`; `Echo.StaticFS — echo.go:548-548`; `Group.Static — group.go:112-112`; `Group.StaticFS — group.go:122-122`; `Echo.Add — echo.go:642-642`; `Echo.GET — echo.go:449-449`).

## Supported conclusion
From the evidence, Echo clearly gives **static-child matching a dedicated lookup path**, and it gives **exact HTTP-method matches precedence over fallback-to-any-method matches** (`DefaultRouter.Route — router.go:791-791`; `node.findStaticChild — router.go:709-709`; `routeMethods.find — router.go:213-213`).

## Unresolved uncertainty
The clue file does **not** expose the body logic that would let us state the exact ordering between **parameter nodes and wildcard nodes** with confidence. The question mentions static/parameter/wildcard overlap, but the provided evidence only directly names static-child lookup and method fallback; it does not show an explicit wildcard node type or a line-by-line param-vs-wildcard tie-break rule (`DefaultRouter.Route — router.go:791-791`; `GAPS`). So the safest evidence-based answer is: static matching is explicitly privileged in lookup, exact-method beats fallback-to-any, but the precise parameter-vs-wildcard winner is not fully recoverable from the supplied clue/snippets alone.
