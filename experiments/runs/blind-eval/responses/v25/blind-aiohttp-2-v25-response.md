# v2.5 Response: blind-aiohttp-2
Date: 2026-04-16

## Question
During application shutdown, how does the server unwind startup resources, and what happens if cleanup only partially initialized or multiple cleanup steps fail?

## Answer

### Shutdown Sequence Overview

The shutdown process follows a multi-phase sequence orchestrated by `BaseRunner.cleanup()` (source snippet at `aiohttp/web_runner.py:252-352`). The full sequence is:

1. **Stop all sites** (one by one, not gathered)
2. **Yield to event loop** (`await asyncio.sleep(0)`)
3. **Pre-shutdown** (`self._server.pre_shutdown()`)
4. **Shutdown hooks** (`await self.shutdown()`)
5. **Server shutdown** (`await self._server.shutdown(self._shutdown_timeout)`)
6. **Cleanup server** (`await self._cleanup_server()`)
7. **Null the server** (`self._server = None`)
8. **Remove signal handlers** (if configured)

### Phase 1: Stopping Sites

From the `BaseRunner.cleanup()` source snippet:
```python
for site in list(self._sites):
    await site.stop()
```

The code explicitly uses a loop rather than `asyncio.gather()`. The source comment explains: *"The loop over sites is intentional, an exception on gather() leaves self._sites in unpredictable state. The loop guarantees that a site is either deleted on success or still present on failure."*

`BaseSite.stop()` (source snippet at `aiohttp/web_runner.py:47-78`) calls `self._runner._check_site(self)`, closes the underlying `asyncio.Server` if it exists (`self._server.close()`), then unregisters via `self._runner._unreg_site(self)`.

**Partial failure handling**: If a site's `stop()` raises an exception, the loop will abort, but sites already stopped have been unregistered. Sites not yet processed remain in `self._sites`, preserving a consistent state.

### Phase 2: Pre-Shutdown

`Server.pre_shutdown()` (FOCUS: `pre_shutdown` at `aiohttp/web_server.py:107-109`) has behavior `ACCUMULATE(self._connections loop -> result)`, iterating over all active connections to prepare them for shutdown.

### Phase 3: Application Shutdown Hooks

For `AppRunner`, `shutdown()` delegates to `self._app.shutdown()` (source snippet shows `async def shutdown(self) -> None: await self._app.shutdown()`). The Application's `shutdown` method (FOCUS: `shutdown` at `aiohttp/web_app.py:344-349`) triggers the `on_shutdown` signal, allowing registered handlers to run cleanup logic.

For `ServerRunner`, `shutdown()` is a no-op (source snippet: `async def shutdown(self) -> None: pass`).

### Phase 4: Server Connection Shutdown

`Server.shutdown(timeout)` (FOCUS: `shutdown` at `aiohttp/web_server.py:111-114`) gracefully shuts down remaining connections with the configured `_shutdown_timeout` (default 60.0 seconds per `BaseRunner.__init__`).

### Phase 5: Cleanup Server

For `AppRunner`, `_cleanup_server()` calls `await self._app.cleanup()` (source snippet: `async def _cleanup_server(self) -> None: await self._app.cleanup()`).

For `ServerRunner`, `_cleanup_server()` is a no-op (source snippet: `async def _cleanup_server(self) -> None: pass`).

### Phase 6: Conditional Server Cleanup

The `BaseRunner.cleanup()` source shows a guard:
```python
if self._server:  # If setup succeeded
    ...
```
This means if `setup()` never ran (or `_make_server()` failed), the pre-shutdown, shutdown, and server shutdown phases are skipped entirely. Only `_cleanup_server()` runs, and `self._server` is set to `None`.

### Application-Level Cleanup and Error Accumulation

`Application.cleanup()` (FOCUS: `cleanup` at `aiohttp/web_app.py:351-360`) triggers the `on_cleanup` signal:
```
behavior: BRANCH(self.on_cleanup.frozen -> await self.on_cleanup..., else -> await sel...)
```
It calls `_on_cleanup`.

**`_on_cleanup`** (FOCUS: `_on_cleanup` at `aiohttp/web_app.py:430-441`) is the critical error-accumulation mechanism:
```
behavior: ACCUMULATE(reversed(self._exits)... -> errors); UNWIND(reversed)
```

This iterates through `self._exits` in **reversed order** (LIFO unwinding), collecting errors into an `errors` list. If any errors accumulate, it raises `CleanupError` (FOCUS: `CleanupError` at `aiohttp/web_app.py:403-406`, extends `RuntimeError`).

This means: **multiple cleanup step failures do not abort early** — all cleanup handlers are attempted, errors are collected, and a single `CleanupError` is raised containing all failures.

### CleanupContext and Startup/Cleanup Pairing

`CleanupContext` (FOCUS: `CleanupContext` at `aiohttp/web_app.py:415-441`) manages paired startup/cleanup operations. Its `_on_startup` method (FOCUS: `_on_startup` at `aiohttp/web_app.py:420-428`) accumulates `exits` during startup via `ACCUMULATE(self loop -> exits)`. The `_on_cleanup` then unwinds these exits in reverse order.

This provides the key pairing: resources initialized during startup (via async generators in `CleanupContext`) are unwound in reverse order during cleanup, ensuring LIFO resource deallocation.

### What Happens with Partial Initialization

1. **If `setup()` never completes**: `BaseRunner.cleanup()` checks `if self._server:` and skips the server shutdown phases. Only `_cleanup_server()` runs (which for `AppRunner` calls `self._app.cleanup()`).

2. **If only some `CleanupContext` generators yielded**: `_on_cleanup` iterates `reversed(self._exits)`, so only exits that were actually registered during partial startup will be unwound. Generators that never yielded won't have registered exit handlers.

3. **If multiple cleanup steps fail**: All are attempted; errors are accumulated into a list, then bundled into a single `CleanupError` (FOCUS: `_on_cleanup` calls `CleanupError`).

### Signal Handlers

`BaseRunner.setup()` registers `SIGINT` and `SIGTERM` handlers (source snippet):
```python
loop.add_signal_handler(signal.SIGINT, _raise_graceful_exit)
loop.add_signal_handler(signal.SIGTERM, _raise_graceful_exit)
```

These raise `GracefulExit` (source snippet: `class GracefulExit(SystemExit): code = 1`). During cleanup, these handlers are removed if they were registered.

### What Cannot Be Determined

Per GAPS: "uncovered: FakeFacebook, FakeResolver, __call__, __init__." The full internal implementation of `Server.shutdown(timeout)` — specifically how it handles per-connection timeouts and force-closing — is not detailed. The exact mechanism by which `_on_cleanup` catches and accumulates individual handler exceptions (try/except within the loop) is implied by the `ACCUMULATE...errors` behavior annotation but the source snippet for the `_on_cleanup` body is not provided.
