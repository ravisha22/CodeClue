### struct-aiohttp-1 (1/2)
F1: COVERED — Identifies `aiohttp/` as the main package and explicitly names `web_app.py`, `web_request.py`, and `web_response.py` inside it.
F2: MISS — Mentions `tests/` exists, but does not describe it as mirroring the main package structure.

### struct-aiohttp-2 (2/2)
F1: COVERED — Explicitly says `web_request.py` contains `BaseRequest` and `Request`, and `web_response.py` contains response classes.
F2: COVERED — Explicitly identifies `web_app.py`/`Application`, `web_server.py`/`Server`, and `web_urldispatcher.py` for routing.

### rel-aiohttp-1 (2/2)
F1: COVERED — States `Request` extends `BaseRequest` in `web_request.py`.
F2: COVERED — States `StreamResponse` is the base class and `Response` extends it in `web_response.py`.

### rel-aiohttp-2 (2/2)
F1: COVERED — Describes `Application.startup()`, `shutdown()`, and `cleanup()` firing lifecycle hooks/signals, and connects app startup to `Server` creation through runner/server flow.
F2: COVERED — States `startup()`/`shutdown()` cause the signals and explains cleanup is handled through `CleanupContext` / `_on_cleanup` resource unwinding.

### blind-aiohttp-1 (1/4)
F1: MISS — Mentions size-limit enforcement and `HTTPRequestEntityTooLarge`, but does not describe `read()` consuming via `readany`.
F2: COVERED — Explicitly says `json()` calls `text()` and rejects unexpected mimetypes with `HTTPBadRequest`.
F3: MISS — Does not state that `post()` returns an empty `MultiDict` for non-POST requests.
F4: MISS — Describes multipart readers generally, but not `post()` writing uploads to `TemporaryFile` via an executor.

### blind-aiohttp-2 (2/4)
F1: COVERED — Explicitly states `startup()`/`shutdown()` send signals and `CleanupContext` manages paired startup/cleanup resources.
F2: MISS — Notes branching on `on_cleanup.frozen`, but does not clearly capture the fallback behavior when `on_cleanup` is not frozen.
F3: MISS — Does not state `_on_startup` accepts context managers or async generators specifically.
F4: COVERED — Explicitly says `_on_cleanup` unwinds `reversed(self._exits)` and raises `CleanupError` after collecting multiple failures.

### struct-fiber-1 (2/2)
F1: COVERED — Identifies root-level `app.go` (`App`) and `ctx.go` (context implementation).
F2: COVERED — Explicitly describes `middleware/` as a large directory organized into separate middleware subpackages/subdirectories.

### struct-fiber-2 (0/2)
F1: MISS — Mentions `DefaultCtx` in `ctx.go`, but places the `Ctx` interface in `ctx_interface_gen.go` rather than `ctx.go`.
F2: MISS — Describes routing modules, but does not specifically capture the split of routing logic between `router.go` and `app.go`.

### rel-fiber-1 (2/2)
F1: COVERED — States `App` exposes HTTP method helpers (`Add`, `Connect`, `All`, etc.) for routing.
F2: COVERED — Explains that `Router` is implemented by both `App` and `Group`, and that `App.Route` creates hierarchical grouped routes.

### rel-fiber-2 (0/2)
F1: MISS — Does not describe middleware chaining through `Ctx.Next()`; it explicitly says that mechanism is not described.
F2: MISS — Does not capture registration-order dispatch or middleware short-circuit behavior.

### blind-fiber-1 (0/4)
F1: MISS — Mentions path override, but not that it mutates the underlying `fasthttp` URI.
F2: MISS — Does not state `RestartRouting` resets `indexRoute` to `-1`.
F3: MISS — Describes route iteration abstractly, but not `App.next` scanning `treeStack`.
F4: MISS — Mentions possible 405 behavior, but not the concrete `Allow` header behavior.

### blind-click-1 (2/4)
F1: COVERED — Explicitly says the `command` decorator creates a `Command` and reverses `__click_params__`.
F2: MISS — Does not state that the `group` decorator defaults `cls=Group`.
F3: COVERED — Says `add_command` stores subcommands in the group’s internal dict/map.
F4: MISS — Mentions `resolve_command`, but not the full `parse_args` → `_protected_args` → `resolve_command` → `invoke` runtime chain.

### blind-click-2 (1/4)
F1: MISS — Gives a loose fallback story, but does not capture the specific `consume_value` precedence `CLI → envvar → default_map → default`.
F2: MISS — Does not describe `type_cast_value` handling single, tuple, and variadic values.
F3: MISS — Does not mention `Choice.convert`, `normalize_choice`, or case-folding.
F4: COVERED — Explicitly says `File` may yield `LazyFile` and `Path` uses `coerce_path_result`.

### blind-fiber-2 (1/4)
F1: MISS — Does not describe recover middleware wrapping `c.Next()` in `defer/recover`; it says the exact mechanism is not shown.
F2: COVERED — Explicitly says `DefaultPanicHandler` returns existing errors unchanged and wraps non-errors as new errors.
F3: MISS — Does not state the constructor installs `DefaultErrorHandler` when config error handler is nil.
F4: MISS — Mentions mounted error handlers, but not the specific deepest-prefix search behavior.

## Summary table
| Task | Score |
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
| blind-click-1 | 2/4 |
| blind-click-2 | 1/4 |
| blind-fiber-2 | 1/4 |
| **Total** | **18/40** |
