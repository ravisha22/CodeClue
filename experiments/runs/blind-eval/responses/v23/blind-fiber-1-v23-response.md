# v2.3 Response: blind-fiber-1
Date: 2026-04-15

## Summary

The clue file and source snippets provide extensive information about Fiber's route pattern matching infrastructure (`path.go`) and client-side cookie path matching, but they provide **limited direct evidence** about the server-side dispatch restart mechanism (how middleware re-triggers routing after path rewriting). The question about restarting dispatch, 404, and 405 outcomes must be answered from the available clues with explicit uncertainty noted.

## Route Pattern Matching Infrastructure

### RoutePatternMatch (path.go:155)

- **`RoutePatternMatch`** (`path.go:155`, FOCUS): *"RoutePatternMatch reports whether path matches the provided Fiber route pattern."*
  - Signature: `func RoutePatternMatch(path, pattern string, cfg ...Config) bool`
  - Behavior: `PRECEDENCE(len -> path -> pattern); UNWIND(defer)`
  - Calls: `RemoveEscapeCharBytes`, `parseRoute`, `getMatch`, `reset`
  - This is a standalone function that takes a path and pattern, parses the route pattern, and runs the match. It accepts an optional `Config` parameter.

### Route Parsing Pipeline

- **`parseRoute`** (`path.go:245`, source snippet): `func parseRoute(pattern string, customConstraints ...CustomConstraint) routeParser` — Parses a route pattern string into a `routeParser` struct containing parsed segments.
- **`routeParser`** (`path.go:27`, source snippet): Contains `segs []*routeSegment` — the parsed segments of the route.
- **`routeSegment`** (`path.go:40-41`, source snippet): `type routeSegment struct` — represents a single segment of a route pattern.
- **`routeParser.getMatch`** (`path.go:507`, source snippet): `func (parser *routeParser) getMatch(detectionPath, path string, params *[maxParams]string, partialCheck bool) bool` — The core matching function. Takes `detectionPath`, `path`, a params array, and a `partialCheck` flag. Returns a boolean match result.
- **`routeParser.reset`** (`path.go:213`, source snippet): Resets parser segments: `parser.segs = parser.segs[:0]`.
- **`routeParser.analyseParameterPart`** (`path.go:342`, source snippet): Parses parameter segments with custom constraints.

### Constraints

- **`Constraint`** (`path.go:80`, source snippet): Has `RegexCompiler *regexp.Regexp` — supports regex-based route constraints.
- **`Constraint.CheckConstraint`** (`path.go:707`): `func (c *Constraint) CheckConstraint(param string) bool` — Validates a parameter against the constraint.
- **`CustomConstraint`** (`path.go:88-89`, source snippet): An interface with a `Name()` method — supports user-defined route constraints.

### Path Utilities

- **`RemoveEscapeChar`** (`path.go:639`): Removes escape characters from route strings.
- **`RemoveEscapeCharBytes`** (`path.go:659`): Byte-level version.
- **`GetTrimmedParam`** (`path.go:623`): Trims a route parameter.
- **`findNextParamPosition`** (`path.go:305`): Locates the next parameter in a pattern.
- **`findParamLen`** (`path.go:563`), **`findGreedyParamLen`** (`path.go:607`), **`findParamLenForLastSegment`** (`path.go:596`): Calculate parameter lengths.
- **`hasPartialMatchBoundary`** (`path.go:486`): Checks for partial match boundaries.
- **`splitNonEscaped`** (`path.go:473`): Splits strings respecting escape characters.
- **`findNextNonEscapedCharPosition`** (`path.go:462`): Finds unescaped characters.

## Path Normalization

- **`App.normalizePath`** (`router.go:398`, SYM): Normalizes the request path. This is likely called during route matching to standardize paths before matching.
- **`Request.DisablePathNormalizing`** (`client/request.go:614`, source snippet): Reports whether path normalizing is disabled for a client request. The client-side equivalent.
- **`Client.DisablePathNormalizing`** (`client/client.go:437`, FOCUS): Reports whether path normalizing is disabled for the client.
- **`Request.SetDisablePathNormalizing`** (`client/request.go:619`, FOCUS): Configures path normalizing on/off.

## Middleware and Route Registration

- **`App.Use`** (`app.go:860`, FOCUS): *"Use registers a middleware route that will match requests with the provided prefix (which is optional and defaults to '/')."* Behavior: `ACCUMULATE(loop -> handlers)`. Raises `panic`.
- **`Group.Use`** (`group.go:70`, FOCUS): Same for groups. Behavior: `PRECEDENCE(len -> not_grp.anyRouteDefined); ACCUMULATE(loop -> handlers)`.
- **`App.Add`** (`app.go:953`, SYM): *"Add allows you to specify multiple HTTP methods..."*
- **`Group.Add`** (`group.go:167`, SYM): Same for groups.
- **`App.Group`** (`app.go:969`, FOCUS): *"Group is used for Routes with common prefix to define a new sub-router with optional middleware."* Raises `panic`.

## Context Path Access

- **`DefaultCtx.Path`** (`ctx.go:297`, FOCUS): *"Path returns the path part of the request URL."*
  - Signature: `DefaultCtx.Path(override ...string)`
  - Behavior: `DELEGATE(c.app.toString -> result)`
  - Calls `configDependentPaths`
  - **Key observation**: The `override ...string` parameter suggests middleware can provide an override path, which would be used instead of the original request path.

- **`DefaultCtx.Matched`** (`ctx.go:375-376`, FOCUS): *"Matched returns true if the current request path was matched by the router."*
  - Behavior: `DELEGATE(c.getMatched -> result)`
  - Calls `getMatched`
  - Called by `OverrideParam`
  - **This directly indicates the framework tracks whether a path was matched**, which is relevant for distinguishing 404 from matched routes.

- **`DefaultCtx.IsMiddleware`** (`ctx.go:380-381`, FOCUS): *"IsMiddleware returns true if the current request handler was registered as middleware."*

## How Dispatch Restart Might Work

Based on the available evidence, here is what can be inferred:

1. **Path override mechanism**: `DefaultCtx.Path(override ...string)` (FOCUS, `ctx.go:297`) allows middleware to set an override path. This is the likely mechanism for middleware to rewrite the request path.

2. **Route matching**: After path rewriting, the framework would need to re-run `routeParser.getMatch()` (`path.go:507`) against the new path. The `getMatch` function takes `detectionPath` and `path` as separate parameters, suggesting it can match against a modified detection path.

3. **404 vs. 405 determination**: `DefaultCtx.Matched()` (`ctx.go:375-376`) tracks whether matching succeeded. The `App.pruneAutoHeadRouteLocked` (`router.go:491`, SYM) — *"pruneAutoHeadRouteLocked removes an automatically generated HEAD route"* — suggests the framework auto-generates HEAD routes, implying method-level matching is separate from path matching.

4. **The `partialCheck` parameter** in `getMatch(detectionPath, path string, params *[maxParams]string, partialCheck bool) bool` suggests the matcher can do partial prefix matching (for middleware routes) vs. full matching (for endpoint routes).

## Uncertainty / Limits

- **The exact dispatch restart mechanism is NOT shown** in the clue file or source snippets. There is no visible `Restart()`, `Next()`, or `Redirect()` method on the context that explicitly re-triggers routing. The mechanism by which middleware causes re-dispatch after path rewriting is not documented in these artifacts.

- **405 Method Not Allowed**: While `HTTPMethodNotAllowed` is referenced in the `View` class (`aiohttp/web_urldispatcher.py:915-931` — but this is from the aiohttp clue, not Fiber), there is no direct Fiber-specific 405 handling mechanism visible. The Fiber router likely checks method matching separately from path matching, but the specific code path is not shown.

- **404 Not Found**: No explicit 404 generation logic is visible in the clue file. The `DefaultCtx.Matched()` method tracks whether matching occurred, but how an unmatched request becomes a 404 response is not shown.

- The `configDependentPaths` function called by `DefaultCtx.Path()` is referenced but not detailed — it likely handles path normalization based on app configuration (e.g., case sensitivity, trailing slashes).

- The main router dispatch loop (likely in `app.go` or `router.go`) that iterates over registered routes and calls `getMatch` is not included in the FOCUS entries or source snippets.
