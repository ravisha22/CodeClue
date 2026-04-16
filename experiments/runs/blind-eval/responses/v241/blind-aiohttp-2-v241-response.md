# v2.4.1 Response: blind-aiohttp-2
Date: 2026-04-16

## Application Shutdown: Unwinding Startup Resources and Handling Partial/Multi-Failure Cleanup

### Shutdown Sequence Overview

Shutdown is orchestrated through `BaseRunner.cleanup()` (drill-down snippet, `aiohttp/web_runner.py:252-352`). The sequence is:

1. **Stop all sites** -- iterates over `list(self._sites)` and calls `await site.stop()` for each one. The loop is intentionally sequential (not `asyncio.gather()`) so that on failure a site remains in `_sites` rather than leaving an unpredictable state (comment in `BaseRunner.cleanup`, `aiohttp/web_runner.py:627-632`).

2. **Yield to event loop** -- `await asyncio.sleep(0)` ensures in-flight requests that started before sites were stopped have begun processing (`BaseRunner.cleanup`, `aiohttp/web_runner.py:638`).

3. **Pre-shutdown on the server** -- `self._server.pre_shutdown()` is called, which accumulates over all connections (`pre_shutdown`, `aiohttp/web_server.py:107-109`, `behavior: ACCUMULATE(self._connections loop -> result)`).

4. **Runner-level shutdown** -- `await self.shutdown()` invokes the runner subclass's shutdown hook. For `AppRunner`, this delegates to `await self._app.shutdown()` (`AppRunner.shutdown`, drill-down snippet, `aiohttp/web_runner.py:461-462`), which fires the `on_shutdown` signal on the Application (`shutdown`, `aiohttp/web_app.py:344-349`). Example shutdown handlers close websockets (`on_shutdown`, `examples/web_ws.py:49-51`; `examples/background_tasks.py:29-31`). For `ServerRunner`, the shutdown hook is a no-op (`ServerRunner.shutdown`, drill-down snippet, `aiohttp/web_runner.py:794-795`).

5. **Server transport shutdown** -- `await self._server.shutdown(self._shutdown_timeout)` with a configurable timeout (default 60s) (`shutdown`, `aiohttp/web_server.py:111-114`; `BaseRunner.__init__` sets `_shutdown_timeout`, `aiohttp/web_runner.py:588`).

6. **Cleanup server** -- `await self._cleanup_server()`. For `AppRunner`, this calls `await self._app.cleanup()` (`AppRunner._cleanup_server`, drill-down snippet, `aiohttp/web_runner.py:495-496`). For `ServerRunner`, it is a no-op (`ServerRunner._cleanup_server`, drill-down snippet, `aiohttp/web_runner.py:800-801`).

7. **Reset server and signals** -- `self._server = None`, and signal handlers (SIGINT/SIGTERM) are removed if they were registered (`BaseRunner.cleanup`, `aiohttp/web_runner.py:644-652`).

### Application-Level Cleanup and the CleanupContext

`Application.cleanup()` (`cleanup`, `aiohttp/web_app.py:351-360`) fires the `on_cleanup` signal, which includes the `CleanupContext` machinery. `_on_cleanup()` (`_on_cleanup`, `aiohttp/web_app.py:430-441`) iterates over `reversed(self._exits)` -- unwinding startup resources in reverse order -- and accumulates any errors (`behavior: ACCUMULATE(reversed(self._exits)... -> errors); UNWIND(reversed)`).

### Handling Partial Initialization and Multiple Failures

**Partial initialization:** The startup counterpart `_on_startup()` (`_on_startup`, `aiohttp/web_app.py:420-428`) accumulates exit callbacks as each startup generator yields. If startup fails partway, only the successfully-registered exits will be present in `self._exits`. During cleanup, `_on_cleanup` iterates `reversed(self._exits)`, so only the resources that were actually initialized get cleaned up.

**Multiple cleanup failures:** `_on_cleanup()` collects errors into a list rather than stopping on the first failure (`behavior: ACCUMULATE(... -> errors)`). After all cleanup steps have been attempted, if errors were accumulated, it raises `CleanupError` (`CleanupError`, `aiohttp/web_app.py:403-406`, `extends: RuntimeError`). This ensures that all cleanup steps run even if some fail, and the caller receives a single aggregated exception (`_on_cleanup calls: CleanupError`, `aiohttp/web_app.py:430-441`).

**Site-level resilience:** The `BaseRunner.cleanup()` loop over sites is sequential specifically to handle partial failure -- if stopping a site raises, that site stays registered; sites that were already stopped are removed (`BaseRunner.cleanup`, drill-down snippet comment, `aiohttp/web_runner.py:628-631`).

### `BaseSite.stop()` Mechanics

`BaseSite.stop()` (`BaseSite`, drill-down snippet, `aiohttp/web_runner.py:704-738`) checks that the site is registered (`_check_site`), closes the underlying `asyncio.Server` if it was started, and then unregisters the site from the runner (`_unreg_site`). If the site was never fully started (`self._server is None`), the close is skipped gracefully.

### What Cannot Be Determined

- The exact implementation of `Application.shutdown()` (the `on_shutdown` signal dispatch body).
- How `Server.shutdown(timeout)` waits for or forcefully terminates individual connections.
- The full body of `_on_startup` -- whether it has try/except around individual generators.
- Whether `_on_cleanup` catches arbitrary `BaseException` or only `Exception` subclasses.
- The behavior of sub-applications during shutdown (signal propagation via `_reg_subapp_signals` is referenced but not detailed).
