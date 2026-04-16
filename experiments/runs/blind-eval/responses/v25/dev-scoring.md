### struct-aiohttp-1 (1/2)
- F1: COVERED — Identifies `aiohttp/` as the core package and specifically lists `web_app.py`, `web_request.py`, and `web_response.py`.
- F2: MISS — Mentions `tests/` exists, but does not say it mirrors the main package structure.

### struct-aiohttp-2 (2/2)
- F1: COVERED — Explicitly says `web_request.py` defines `BaseRequest` and `Request`, and `web_response.py` defines the response hierarchy.
- F2: COVERED — Identifies `web_app.py` with `Application`, `web_urldispatcher.py` for routing, and places `web_server.py` in the core web stack.

### rel-aiohttp-1 (2/2)
- F1: COVERED — States `Request` extends `BaseRequest`.
- F2: COVERED — States `StreamResponse` is the base response class and `Response` extends it.

### rel-aiohttp-2 (1/2)
- F1: COVERED — Describes `startup`, `shutdown`, and `cleanup`, and notes `AppRunner._make_server()` creates a `Server`.
- F2: MISS — Says `startup`/`shutdown` trigger signals, but does not specifically say cleanup delegates to `CleanupContext`.

### blind-aiohttp-1 (1/4)
- F1: MISS — Notes `HTTPRequestEntityTooLarge`, but does not describe `read()` consuming via `readany`.
- F2: COVERED — Explicitly says `json()` calls `text()` and raises `HTTPBadRequest` for unexpected mimetypes.
- F3: MISS — Does not say `post()` returns an empty `MultiDict` for non-POST requests.
- F4: MISS — Does not describe multipart form handling writing uploads to `TemporaryFile` via an executor.

### blind-aiohttp-2 (4/4)
- F1: COVERED — Describes shutdown signals and says `CleanupContext` manages paired startup/cleanup resources.
- F2: COVERED — Quotes the `cleanup()` branch on whether `on_cleanup` is frozen, capturing the fallback path.
- F3: COVERED — Describes `_on_startup` registering cleanup exits via async generators in `CleanupContext`.
- F4: COVERED — Explicitly says `_on_cleanup` unwinds exits in reverse order and raises `CleanupError` after accumulating multiple failures.

### struct-fiber-1 (2/2)
- F1: COVERED — Identifies `app.go` with `App` and `ctx.go` as core root files.
- F2: COVERED — Describes `middleware/` as a large package organized into separate subdirectories.

### struct-fiber-2 (0/2)
- F1: MISS — Mentions `DefaultCtx`, but does not place the `Ctx` interface in `ctx.go`; instead it points to `ctx_interface.go`.
- F2: MISS — Describes routing in `router.go`, but does not tie routing as split between `router.go` and `app.go`.

### rel-fiber-1 (2/2)
- F1: COVERED — Says `App` owns routing and uses HTTP method helpers such as `Add`, `Connect`, etc.
- F2: COVERED — Explains `Router`/`Group` relationships and hierarchical routing via `App.Route -> Group`.

### rel-fiber-2 (2/2)
- F1: COVERED — Explicitly says middleware continues the chain via `DefaultCtx.Next()`.
- F2: COVERED — Describes ordered middleware execution (`Middleware 1 -> c.Next() -> Middleware 2 -> ...`) and implies short-circuiting when `Next()` is not called.

### blind-fiber-1 (0/4)
- F1: MISS — Says path override updates routing state, but not that it mutates the underlying fasthttp URI.
- F2: MISS — Does not state that `RestartRouting()` resets `indexRoute`; it explicitly says that internal reset logic cannot be confirmed.
- F3: MISS — Does not mention `App.next()` scanning `treeStack`.
- F4: MISS — Mentions 405 on method mismatch, but not the `Allow` header behavior.

### blind-click-1 (2/4)
- F1: COVERED — Clearly explains decorator accumulation into `__click_params__` and reversal when `command()` builds a `Command`.
- F2: MISS — Discusses the `Group` class, but not the `group` decorator defaulting `cls=Group`.
- F3: COVERED — Says `add_command` registers/stores child commands in the group's command map.
- F4: MISS — Does not describe the `parse_args -> _protected_args -> resolve_command -> invoke` dispatch sequence.

### blind-click-2 (1/4)
- F1: MISS — Gives a general fallback story, but does not capture the specific `CLI -> envvar -> default_map -> default` order.
- F2: MISS — Mentions cardinality handling, but not the specific single/tuple/variadic behavior of `type_cast_value`.
- F3: MISS — Does not discuss `Choice.convert()` normalization.
- F4: COVERED — Explicitly says `File` can yield `LazyFile` and `Path` calls `coerce_path_result`.

### blind-fiber-2 (2/4)
- F1: MISS — Explains panic conversion, but not the specific `c.Next()` wrapped in `defer/recover`.
- F2: COVERED — Explicitly says `DefaultPanicHandler` returns an existing `error` unchanged and wraps non-errors with `fmt.Errorf`.
- F3: MISS — Does not say the constructor installs `DefaultErrorHandler` when config provides nil.
- F4: COVERED — Explains that `ErrorHandler` walks mounted prefixes and selects a mounted sub-app handler based on path matching.

## Summary

| task_id | score |
|---|---:|
| struct-aiohttp-1 | 1/2 |
| struct-aiohttp-2 | 2/2 |
| rel-aiohttp-1 | 2/2 |
| rel-aiohttp-2 | 1/2 |
| blind-aiohttp-1 | 1/4 |
| blind-aiohttp-2 | 4/4 |
| struct-fiber-1 | 2/2 |
| struct-fiber-2 | 0/2 |
| rel-fiber-1 | 2/2 |
| rel-fiber-2 | 2/2 |
| blind-fiber-1 | 0/4 |
| blind-click-1 | 2/4 |
| blind-click-2 | 1/4 |
| blind-fiber-2 | 2/4 |
| **Total** | **22/40** |
