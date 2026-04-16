### struct-aiohttp-1 (1/2)
- F1: **COVERED** — Identifies `aiohttp/` as the core package and explicitly names `web_app.py`, `web_request.py`, and `web_response.py`.
- F2: **MISS** — Mentions `tests/` exists, but does not say it mirrors the main package structure.

### struct-aiohttp-2 (2/2)
- F1: **COVERED** — Says `web_request.py` contains `BaseRequest`/`Request` and separately identifies `web_response.py`.
- F2: **COVERED** — Explicitly identifies `web_app.py` (`Application`), `web_server.py` (`Server`), and `web_urldispatcher.py` for routing.

### rel-aiohttp-1 (2/2)
- F1: **COVERED** — Explicitly states `Request` extends `BaseRequest` in `web_request.py`.
- F2: **COVERED** — Explicitly states `StreamResponse` is the base class and `Response` extends it in `web_response.py`.

### rel-aiohttp-2 (2/2)
- F1: **COVERED** — Describes `Application` lifecycle methods, shows `startup`/`shutdown`/`cleanup`, and explains `AppRunner` creates and uses `Server`.
- F2: **COVERED** — Explicitly says `startup()` fires `on_startup`, `shutdown()` fires `on_shutdown`, and `cleanup()` delegates into `CleanupContext`.

### blind-aiohttp-1 (1/4)
- F1: **MISS** — Notes `read()` raises `HTTPRequestEntityTooLarge`, but does not describe consumption via `readany`.
- F2: **COVERED** — Explicitly says `json()` calls `text()` and rejects mismatched MIME types with `HTTPBadRequest`.
- F3: **MISS** — Says `post()` is uncovered / cannot be determined, so the empty-`MultiDict` behavior is absent.
- F4: **MISS** — Discusses multipart readers generally, but not `post()` writing uploads to `TemporaryFile` via an executor.

### blind-aiohttp-2 (2/4)
- F1: **COVERED** — Describes shutdown signal dispatch and explains `CleanupContext` resource unwinding; startup-side resource registration is also discussed via `_on_startup`.
- F2: **MISS** — Does not mention the `cleanup()` fallback path when `on_cleanup` is not frozen.
- F3: **MISS** — Mentions startup generators yielding exits, but not the acceptance of context managers vs. generators as the mechanism.
- F4: **COVERED** — Explicitly says `_on_cleanup()` unwinds exits in reverse and raises `CleanupError` after collecting multiple failures.

### struct-fiber-1 (2/2)
- F1: **COVERED** — Explicitly identifies root files `app.go` (`App`) and `ctx.go` (request context).
- F2: **COVERED** — Explicitly describes `middleware/` as containing many separate middleware subpackages/subdirectories.

### struct-fiber-2 (0/2)
- F1: **MISS** — Mentions `Ctx` in `ctx_interface_gen.go` and `DefaultCtx` in `ctx.go`; this misses the requested `ctx.go` + `Ctx interface` framing.
- F2: **MISS** — Describes `router.go`, but does not clearly state routing is split between `router.go` and `app.go`.

### rel-fiber-1 (2/2)
- F1: **COVERED** — Explicitly says `App` routes through HTTP method helpers like `Connect`, which delegate to `Add`.
- F2: **COVERED** — Explicitly explains `Router`/`Group` hierarchy and that `App.Route` creates `Group` subrouters.

### rel-fiber-2 (0/2)
- F1: **MISS** — Does not describe middleware chaining via `Ctx.Next()`; it even says `c.Next()` cannot be determined.
- F2: **MISS** — Does not establish registration-order dispatch or short-circuit behavior.

### blind-fiber-1 (0/4)
- F1: **MISS** — Mentions path override, but not mutation of the underlying fasthttp URI.
- F2: **MISS** — Only speculates that `RestartRouting` likely resets an index; no evidence for `indexRoute`.
- F3: **MISS** — Discusses route stacks generically, but not `App.next` scanning `treeStack`.
- F4: **MISS** — Mentions 405 as an expectation, but not the concrete `Allow` header behavior.

### blind-click-1 (1/4)
- F1: **COVERED** — States the decorator creates a `Command` and that earlier parameter metadata is reversed during command creation, which matches the core mechanism.
- F2: **MISS** — Does not state that `group` defaults `cls=Group`.
- F3: **MISS** — Does not describe `add_command` as the registration mechanism.
- F4: **MISS** — Does not provide the `parse_args -> _protected_args -> resolve_command -> invoke` call chain.

### blind-click-2 (1/4)
- F1: **MISS** — Explicitly says the exact precedence among CLI/env/default sources cannot be determined.
- F2: **MISS** — Does not describe `type_cast_value` single/tuple/variadic handling.
- F3: **MISS** — Does not mention `Choice.convert` normalization.
- F4: **COVERED** — Explicitly distinguishes `File` leading to `LazyFile` and `Path` using `coerce_path_result`.

### blind-fiber-2 (1/4)
- F1: **MISS** — Does not describe recover middleware wrapping `c.Next()` in `defer/recover`.
- F2: **COVERED** — Explicitly states `DefaultPanicHandler` preserves `error` values and wraps non-errors.
- F3: **MISS** — Does not say the constructor installs `DefaultErrorHandler` when config leaves it nil.
- F4: **MISS** — Notes mounted-handler precedence, but not the deepest-prefix search mechanism.

### Summary
| task_id | score |
|---|---:|
| struct-aiohttp-1 | 1/2 |
| struct-aiohttp-2 | 2/2 |
| rel-aiohttp-1 | 2/2 |
| rel-aiohttp-2 | 2/2 |
| blind-aiohttp-1 | 1/4 |
| blind-aiohttp-2 | 2/4 |
| struct-fiber-1 | 2/2 |
| struct-fiber-2 | 0/2 |
| rel-fiber-1 | 2/2 |
| rel-fiber-2 | 0/2 |
| blind-fiber-1 | 0/4 |
| blind-click-1 | 1/4 |
| blind-click-2 | 1/4 |
| blind-fiber-2 | 1/4 |
| **Total** | **17/38** |
