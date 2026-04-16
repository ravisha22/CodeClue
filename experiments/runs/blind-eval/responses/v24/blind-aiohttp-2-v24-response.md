# v2.4 Response: blind-aiohttp-2
Date: 2026-04-16

## Question
During application shutdown, how does the server unwind startup resources, and what happens if cleanup only partially initialized or multiple cleanup steps fail?

## Answer

### Shutdown Signal Chain

The shutdown sequence involves three distinct lifecycle signals on the `Application` class (`Application`, `aiohttp/web_app.py:71-400`):

1. **`on_shutdown`** — The `shutdown()` method (`shutdown`, `aiohttp/web_app.py:344-349`) causes the `on_shutdown` signal to fire, notifying handlers that shutdown is beginning.
2. **`cleanup()`** — The `cleanup()` method (`cleanup`, `aiohttp/web_app.py:351-360`) causes the `on_cleanup` signal. Its behavior annotation shows it branches on whether `self.on_cleanup.frozen` is true, then calls `_on_cleanup`.
3. **`on_startup`** / **`startup()`** — The `startup()` method (`startup`, `aiohttp/web_app.py:337-342`) causes `on_startup` signal; this is the startup counterpart that cleanup unwinds.

### AppRunner Orchestrates Shutdown

The `AppRunner` source snippet (`AppRunner`, `aiohttp/web_runner.py:380-453`) shows the full lifecycle:

- **During setup**: `_make_server()` freezes `on_startup`, awaits `self._app.startup()`, freezes the app, then creates a `Server` instance with `self._app._handle` as the request handler.
- **During shutdown**: `AppRunner.shutdown()` delegates to `await self._app.shutdown()`.
- **During cleanup**: `AppRunner._cleanup_server()` calls `await self._app.cleanup()`.

### BaseRunner.cleanup() — The Core Unwinding Logic

The `BaseRunner.cleanup()` source snippet (`BaseRunner`, `aiohttp/web_runner.py:252-352`) reveals a carefully ordered teardown:

1. **Stop all sites individually in a loop** (not via `gather()`): The code comments explicitly state _"The loop over sites is intentional, an exception on gather() leaves self._sites in unpredictable state. The loop guarantees that a site is either deleted on success or still present on failure."_ Each site's `stop()` is called sequentially (`BaseSite.stop source snippet, web_runner.py:47-78`), which closes the server socket and unregisters the site.
2. **Yield to event loop**: `await asyncio.sleep(0)` ensures in-flight requests that arrived before site shutdown have started being handled.
3. **Pre-shutdown on server**: `self._server.pre_shutdown()` is called, which for the `Server` class (`pre_shutdown`, `aiohttp/web_server.py:107-109`) accumulates over `self._connections`.
4. **Shutdown hooks**: `await self.shutdown()` fires application-level shutdown hooks.
5. **Server shutdown with timeout**: `await self._server.shutdown(self._shutdown_timeout)` — the `BaseRunner` is initialized with `shutdown_timeout=60.0` by default (`BaseRunner.__init__ source snippet`).
6. **Cleanup server**: `await self._cleanup_server()` — for `AppRunner`, this calls `await self._app.cleanup()`. For `ServerRunner`, this is a no-op (`ServerRunner._cleanup_server source snippet, web_runner.py:376-377` — just `pass`).
7. **Reset server to None** and optionally remove signal handlers.

### CleanupContext — Handling Partial Initialization and Multiple Failures

The `CleanupContext` class (`CleanupContext`, `aiohttp/web_app.py:415-441`) manages startup/cleanup as paired async generators. The `_on_startup` method (`_on_startup`, `aiohttp/web_app.py:420-428`) accumulates exit callbacks by iterating through the context generators.

The `_on_cleanup` method (`_on_cleanup`, `aiohttp/web_app.py:430-441`) handles teardown with the following critical behaviors:
- It iterates over `reversed(self._exits)` — the behavior annotation says `ACCUMULATE(reversed(self._exits)... -> errors); UNWIND(reversed)`. This means cleanup steps are unwound in **reverse order** of initialization (LIFO).
- **Multiple failures are collected**: Errors are accumulated into an `errors` list rather than failing on the first error. After all exits have been attempted, if any errors occurred, a `CleanupError` is raised (`CleanupError`, `aiohttp/web_app.py:403-406`).
- `CleanupError` extends `RuntimeError` (`CleanupError extends RuntimeError`, `aiohttp/web_app.py:403-406`), and is called by both `_on_cleanup` and `CleanupContext`.

This design means:
- **Partial initialization is safe**: Only exits that were successfully registered (during `_on_startup`) will be unwound. If startup fails partway through, only the already-initialized generators have their cleanup called.
- **All cleanup steps are attempted**: Even if one cleanup step raises an exception, the remaining steps still execute. All errors are gathered and raised together as a single `CleanupError`.

### BaseSite Stop Behavior

`BaseSite.stop()` (`BaseSite source snippet, web_runner.py:47-78`) first checks the site is registered via `self._runner._check_site(self)`, then closes the underlying `asyncio.Server` if it was started (`self._server.close()`), and finally unregisters via `self._runner._unreg_site(self)`. The check methods (`_check_site`, `_reg_site`, `_unreg_site` source snippets) raise `RuntimeError` if sites are not in expected state.

### GracefulExit

The `GracefulExit` class (`GracefulExit`, `aiohttp/web_runner.py:39-40`) extends `SystemExit` with `code = 1`, providing a way to signal graceful termination. The test snippet (`shutdown test, tests/test_web_runner.py:310-312`) shows it can be raised from shutdown hooks.

### Site Types

Three site types are shown in the snippets:
- `SockSite` (`SockSite`, `aiohttp/web_runner.py:213-249`) — binds to a socket.
- `NamedPipeSite` (`NamedPipeSite`, `aiohttp/web_runner.py:184-210`) — Windows named pipes, requires `ProactorEventLoop`.
- Both call `super().start()` which registers the site via `_reg_site`.

### Cannot Be Determined from Clue File

- The exact implementation of `Server.shutdown(timeout)` — only its signature is shown (`shutdown`, `aiohttp/web_server.py:111-114`).
- How `pre_shutdown` interacts with active connections beyond iterating `self._connections`.
- The full behavior of `Application.shutdown()` and `Application.startup()` — only their docstrings ("Causes on_shutdown/on_startup signal") are shown.
- The `__call__` and `__init__` methods of `CleanupContext` are listed as uncovered in GAPS.
- How `FakeFacebook` and `FakeResolver` relate to shutdown (listed as uncovered).
