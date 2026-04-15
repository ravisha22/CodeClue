# v23 Dev-Set Scoring

### struct-aiohttp-1 (2/2)
F1: COVERED — Response identifies "aiohttp/" as the main library package and explicitly lists web_app.py, web_request.py, web_response.py as separate server-side web modules.
F2: COVERED — Response identifies "tests/ (80 files) — Test suite" with subdirectories autobahn/ and isolated/.

### struct-aiohttp-2 (2/2)
F1: COVERED — Response details web_request.py with BaseRequest (L109-823) and Request classes, web_response.py with StreamResponse and Response.
F2: COVERED — Response covers web_app.py (Application methods: pre_freeze, freeze, reg_handler, CleanupError), web_server.py (Server, _make_request), and web_urldispatcher.py (UrlDispatcher, route resolution, resources).

### rel-aiohttp-1 (2/2)
F1: COVERED — Response states "Request (aiohttp/web_request.py:826-884) → extends BaseRequest" and "BaseRequest (aiohttp/web_request.py:109-823)"; both in web_request.py.
F2: COVERED — Response states "StreamResponse (aiohttp/web_response.py:74-532)" as base and "Response (aiohttp/web_response.py:535-740) → extends StreamResponse"; both in web_response.py.

### rel-aiohttp-2 (2/2)
F1: COVERED — Response describes Application.startup() "Causes on_startup signal", shutdown() "Causes on_shutdown signal", cleanup() "Causes on_cleanup signal". Also shows AppRunner._make_server() creating Server with self._app._handle.
F2: COVERED — Response identifies startup/shutdown dispatching to signal handlers and cleanup() calling _on_cleanup which connects to CleanupContext. CleanupContext is described as called by Application and raising CleanupError.

### blind-aiohttp-1 (2/4)
F1: COVERED — Response describes read() (L624-643) as the primary body-reading entry point, raising HTTPRequestEntityTooLarge when body exceeds limits. States json(), text(), and post() all flow through read().
F2: COVERED — Response states "json() method... Reads the body as JSON by first calling await self.text()... if the content type does not match, it raises HTTPBadRequest with message 'Attempt to decode JSON with unexpected mimetype: %s'."
F3: MISS — Response does not describe post() returning an empty MultiDict for non-POST methods or unsupported content types. Acknowledges "The exact behavior of post() for distinguishing URL-encoded vs. multipart form submissions... is not fully visible."
F4: MISS — Response describes multipart chunk reading and decoding but does not mention TemporaryFile or executor-based writes for multipart post data.

### blind-aiohttp-2 (3/4)
F1: COVERED — Response states startup "Causes on_startup signal", shutdown "Causes on_shutdown signal" (signals only). CleanupContext is described as providing context-manager-style resource enter/exit.
F2: COVERED — Response states "Application.cleanup()... behavior is BRANCH(on_cleanup.frozen -> result, else -> result), checking whether the cleanup signal is frozen before proceeding."
F3: MISS — Response only states _on_startup "ACCUMULATE(loop -> exits), suggesting it collects exit/cleanup callbacks." Does not identify that it accepts async context managers or generators.
F4: COVERED — Response describes _on_cleanup iterating "in reversed order (UNWIND(reversed))", accumulating errors, and raising CleanupError. Core mechanism of reverse unwinding and error aggregation captured.

### struct-fiber-1 (2/2)
F1: COVERED — Response identifies app.go (1486 lines) as "The central application file. Defines the App type" and references DefaultCtx methods in ctx.go (e.g., DefaultCtx.Reset at ctx.go:662).
F2: COVERED — Response extensively describes "middleware/ directory containing 87 files" with individual subdirectories per middleware (session/, csrf/, cors/, cache/, limiter/, etc.).

### struct-fiber-2 (2/2)
F1: COVERED — Response identifies Ctx interface (ctx_interface_gen.go:18) and DefaultCtx as "The Default Implementation" in ctx.go and req.go. Core components identified.
F2: COVERED — Response states routing managed by App (app.go) with methods in router.go (e.g., App.normalizePath at router.go:398), and App.Add (app.go:953) as core registration.

### rel-fiber-1 (2/2)
F1: COVERED — Response describes App.Add as the core route registration method with HTTP method helpers (Head, Connect) delegating to App.Add. App.addRoute adds Route to internal table.
F2: COVERED — Response describes Router interface (router.go:18-19) shared by App and Group, Group.Add for registration, App.Route creating groups with prefix, and sub-app mounting via mount().

### rel-fiber-2 (0/2)
F1: MISS — Response acknowledges "The server-side handler chain mechanism (how next is called to advance through middleware) is not directly visible." Does not identify Ctx.Next() as the chaining mechanism.
F2: MISS — Response does not describe dispatch calling middleware in registration order or short-circuit capability. Middleware patterns are described but not the execution chain semantics.

### blind-fiber-1 (0/4)
F1: MISS — Response notes DefaultCtx.Path has "override ...string" parameter but does not describe that the override mutates the underlying fasthttp URI.
F2: MISS — Response explicitly states "The exact dispatch restart mechanism is NOT shown... There is no visible Restart(), Next(), or Redirect() method on the context that explicitly re-triggers routing." RestartRouting and indexRoute reset not identified.
F3: MISS — Response mentions Route.match called by next/nextCustom but does not describe App.next scanning treeStack for method+path. States "The main router dispatch loop... is not included in the FOCUS entries."
F4: MISS — Response states "405 Method Not Allowed... there is no direct Fiber-specific 405 handling mechanism visible." No description of path-match-without-method-match producing 405 with Allow header.

### blind-click-1 (2/4)
F1: COVERED — Response describes command decorator (decorators.py:168-255) creating Command with "UNWIND(reversed)" behavior. Also describes _param_memo attaching __click_params__ to functions, confirming the reverse collection mechanism.
F2: MISS — Response describes the Group class but does not describe a @group decorator or its defaulting of cls to Group.
F3: COVERED — Response states "add_command (src/click/core.py:1622-1630): Registers another Command with this group." Registration mechanism identified.
F4: MISS — Response does not describe the parse_args→_protected_args→resolve_command→invoke dispatch chain. Notes "Command.invoke and Group.invoke methods are not shown."

### blind-click-2 (3/4)
F1: COVERED — Response describes the multi-stage fallback: "environment variables, interactive prompting (for options), and default values" via consume_value and process_value. Captures CLI→envvar→default flow (3/4 stages; misses default_map but >50% of chain).
F2: MISS — Response describes convert_type for type inference but does not specifically identify type_cast_value or its single/tuple/variadic dispatch pattern.
F3: COVERED — Response states Choice "Calls _normalized_mapping, get_invalid_choice_message, normalize_choice, fail, convert_type." The normalize_choice mechanism is identified.
F4: COVERED — Response describes File type using LazyFile for deferred opening and Path type calling coerce_path_result. Both conversion mechanisms identified.

### blind-fiber-2 (3/4)
F1: COVERED — Response describes recovery middleware catching panics via recover() and converting them to errors. States "Handler panics → Go runtime unwinds → Recovery middleware catches the panic via recover()."
F2: COVERED — Response states "DefaultPanicHandler... If the recovered value r is already an error, it passes it through directly. Otherwise, it wraps the value into a new error (using %v formatting)."
F3: MISS — Response does not describe the App constructor installing DefaultErrorHandler when Config.ErrorHandler is nil. Only states DefaultErrorHandler is "the fallback" without explaining the installation mechanism.
F4: COVERED — Response describes ErrorHandler checking for "mounted error handler (mountedErrHandler)" with GUARD behavior and "ACCUMULATE(loop -> result)" iterating through mounted app hierarchy. The sub-app prefix search mechanism is identified.

---

## Summary Table

| Task | Covered | Total | Score |
|---|---|---|---|
| struct-aiohttp-1 | 2 | 2 | 100% |
| struct-aiohttp-2 | 2 | 2 | 100% |
| rel-aiohttp-1 | 2 | 2 | 100% |
| rel-aiohttp-2 | 2 | 2 | 100% |
| blind-aiohttp-1 | 2 | 4 | 50% |
| blind-aiohttp-2 | 3 | 4 | 75% |
| struct-fiber-1 | 2 | 2 | 100% |
| struct-fiber-2 | 2 | 2 | 100% |
| rel-fiber-1 | 2 | 2 | 100% |
| rel-fiber-2 | 0 | 2 | 0% |
| blind-fiber-1 | 0 | 4 | 0% |
| blind-fiber-2 | 3 | 4 | 75% |
| blind-click-1 | 2 | 4 | 50% |
| blind-click-2 | 3 | 4 | 75% |
| **TOTAL** | **27** | **40** | **67.5%** |

### By category
| Category | Covered | Total | Score |
|---|---|---|---|
| struct-* | 8 | 8 | 100% |
| rel-* | 6 | 8 | 75% |
| blind-* | 13 | 24 | 54.2% |
