# v2.3 Response: blind-aiohttp-2
Date: 2026-04-15

## Summary

The aiohttp server shutdown follows a multi-phase process orchestrated by `BaseRunner.cleanup()`. It sequentially stops sites, pre-shuts down the server, calls application shutdown hooks, performs a timed server shutdown, then runs cleanup handlers. Partial initialization is handled by guard checks, and multiple cleanup failures are aggregated into a `CleanupError`.

## Shutdown Sequence (BaseRunner.cleanup)

The `BaseRunner.cleanup()` method (`aiohttp/web_runner.py` L252-352, source snippet L632-658) implements the full shutdown sequence:

1. **Stop all sites** — Iterates over `self._sites` in a loop (not `gather()`), calling `await site.stop()` for each. The source comment explains: *"The loop over sites is intentional, an exception on gather() leaves self._sites in unpredictable state. The loop guarantees that a site is either deleted on success or still present on failure."* Each `site.stop()` calls `self._runner._check_site(self)`, closes the server via `self._server.close()`, and unregisters via `self._runner._unreg_site(self)` (source snippet `BaseSite` at L47-78).

2. **Guard on setup success** — `if self._server:` checks whether setup completed. If `_make_server()` was never called (or failed), the shutdown/cleanup steps for the server are skipped entirely.

3. **Yield to event loop** — `await asyncio.sleep(0)` ensures incoming requests that arrived before site shutdown have started being handled.

4. **Pre-shutdown** — `self._server.pre_shutdown()` is called. The `pre_shutdown` method (`aiohttp/web_server.py:107-109`, FOCUS) has behavior `ACCUMULATE(loop -> result)`, iterating over some collection.

5. **Application shutdown hooks** — `await self.shutdown()` is called. For `AppRunner` (source snippet L466-467), this delegates to `await self._app.shutdown()`. The `Application.shutdown()` method (`aiohttp/web_app.py:344-349`, FOCUS) is described as *"Causes on_shutdown signal"*, triggering registered shutdown callbacks.

6. **Server shutdown with timeout** — `await self._server.shutdown(self._shutdown_timeout)` is called. The `shutdown_timeout` defaults to `60.0` seconds (source snippet `BaseRunner.__init__` L582-593). The `Server.shutdown()` method (`aiohttp/web_server.py:111-114`, FOCUS) accepts a timeout parameter.

7. **Cleanup server** — `await self._cleanup_server()` is called. For `AppRunner`, this calls `await self._app.cleanup()` (source snippet L500-501). For `ServerRunner`, this is a no-op `pass` (source snippet L805-806).

8. **Reset state** — `self._server = None` and signal handlers are removed if they were registered.

## Application Cleanup and Partial Failure Handling

- **`Application.cleanup()`** (`aiohttp/web_app.py:351-360`, FOCUS): Described as *"Causes on_cleanup signal"*. Its behavior is `BRANCH(on_cleanup.frozen -> result, else -> result)`, checking whether the cleanup signal is frozen before proceeding. It calls `_on_cleanup`.

- **`_on_cleanup()`** (`aiohttp/web_app.py:430-441`, FOCUS): This is the critical error-aggregation handler. Its behavior is `ACCUMULATE(loop -> errors); UNWIND(reversed)`:
  - It iterates over cleanup handlers **in reversed order** (`UNWIND(reversed)`), meaning cleanup runs in the opposite order of registration/startup — a proper LIFO unwinding of resources.
  - It **accumulates errors** rather than stopping on the first failure (`ACCUMULATE(loop -> errors)`).
  - After the loop, if any errors were collected, it raises `CleanupError` (called_by confirms: `called_by: cleanup, Application`; raises: `CleanupError`).

- **`CleanupError`** (`aiohttp/web_app.py:403-406`, FOCUS): Extends `RuntimeError`. It is called by both `_on_cleanup` and `CleanupContext`, meaning it serves as the aggregated error container for multiple failures.

## CleanupContext

- **`CleanupContext`** (`aiohttp/web_app.py:415-441`, FOCUS): A separate class that also raises `CleanupError`. It is `called_by: Application`, meaning the Application uses CleanupContext objects. This likely provides context-manager-style cleanup registration (startup yields, then cleanup runs on shutdown).

## Startup and _on_startup

- **`_on_startup()`** (`aiohttp/web_app.py:420-428`, FOCUS): Has behavior `ACCUMULATE(loop -> exits)`, suggesting it collects exit/cleanup callbacks during startup to be used during cleanup.

- **`Application.startup()`** (`aiohttp/web_app.py:337-342`, FOCUS): *"Causes on_startup signal"*. Called during `AppRunner._make_server()` (source snippet L470-471): the sequence is `on_startup.freeze()` → `await self._app.startup()` → `self._app.freeze()`.

## AppRunner._make_server (Startup)

From the source snippet (`aiohttp/web_runner.py` L469-478):
1. `self._app.on_startup.freeze()` — Freezes the startup signal (no more handlers can be added).
2. `await self._app.startup()` — Runs all registered startup hooks.
3. `self._app.freeze()` — Freezes the application (no more configuration changes).
4. Returns `Server(self._app._handle, request_factory=self._make_request, **self._kwargs)`.

## ServerRunner vs. AppRunner

- **`ServerRunner`** (`aiohttp/web_runner.py:355-377`, source snippet L782-807): A low-level runner that wraps an already-constructed `Server`. Its `shutdown()` is a no-op (`pass`), its `_make_server()` just returns `self._web_server`, and its `_cleanup_server()` is also a no-op (`pass`). No application-level lifecycle hooks are triggered.

- **`AppRunner`** (`aiohttp/web_runner.py:380-453`, source snippet): The full-featured runner that manages an `Application`. It validates the app type in `__init__`, delegates `shutdown()` to `self._app.shutdown()`, runs the full startup sequence in `_make_server()`, and delegates `_cleanup_server()` to `self._app.cleanup()`.

## Site Lifecycle

- **`BaseSite`** (source snippet L709-743): Requires `runner.server is not None` in `__init__` (raises `RuntimeError` otherwise, ensuring `runner.setup()` was called first). `start()` registers with runner. `stop()` checks site registration, closes the server socket, and unregisters.
- **`NamedPipeSite`** (source snippet L751-780): Windows-specific, requires `ProactorEventLoop`.
- **`SockSite`** (source snippet L809-816): Socket-based site.

## GracefulExit

- **`GracefulExit`** (`aiohttp/web_runner.py:39-40`, source snippet): Extends `SystemExit` with `code = 1`. The test snippet shows it being raised from a shutdown handler to trigger graceful exit from the event loop.

## Uncertainty / Limits

- The exact contents of `CleanupError` (whether it wraps a list of exceptions or just the first) cannot be fully determined — the FOCUS entry shows it is constructed from accumulated errors in `_on_cleanup`, but the class definition at L403-406 is only 4 lines, so details of how multiple errors are stored/reported are not visible.
- The relationship between `CleanupContext` and `_on_cleanup` is partially opaque — `_on_startup` accumulates `exits` which are likely the cleanup halves of context managers, but the exact mechanism is not shown in detail.
- The `Application.freeze()` and `pre_freeze()` methods (`aiohttp/web_app.py:241` and `212`) are referenced but their exact behavior during shutdown is not detailed in the clue file.
