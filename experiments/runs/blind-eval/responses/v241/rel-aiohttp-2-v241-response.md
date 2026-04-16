# v2.4.1 Response: rel-aiohttp-2
Date: 2026-04-16

## Call Relationships Between the Application Class and the Web Server Stack

### Application Core Call Graph

The `Application` class (`Application`, `aiohttp/web_app.py:71-400`) directly calls:
- `_add_subapp` -- mounts sub-applications
- `_check_frozen` -- guards against mutation after freeze
- `_prepare_middleware` -- sets up the middleware chain
- `handler` -- resolves request handlers
- `reg_handler` -- registers handlers (`reg_handler`, `aiohttp/web_app.py:260`)
- `_reg_subapp_signals` -- propagates lifecycle signals to sub-apps
- `add_routes` -- registers URL routes
- `freeze` -- freezes the app configuration (`freeze`, `aiohttp/web_app.py:241`; `pre_freeze`, `aiohttp/web_app.py:212`)

Application raises `TypeError`, `RuntimeError`, `ValueError` (`Application raises`).

### Application -> AppRunner -> Server Chain

**`AppRunner`** (`AppRunner`, `aiohttp/web_runner.py:380-453`) wraps an `Application`. Its key call relationships:

1. **`AppRunner._make_server()`** (`_make_server`, `aiohttp/web_runner.py:421-430`) -- freezes `on_startup`, calls `await self._app.startup()`, freezes the app, then creates a `Server` instance passing `self._app._handle` as the request handler. This is the critical link: `Application._handle` becomes the Server's request handler. It delegates via `DELEGATE(Server -> result)` and uses `Server` from `web_server`.

2. **`AppRunner.shutdown()`** -- calls `await self._app.shutdown()` (`shutdown`, `aiohttp/web_app.py:344-349`), which fires the `on_shutdown` signal.

3. **`AppRunner.cleanup()`** (via `_cleanup_server`) -- calls `await self._app.cleanup()` (`cleanup`, `aiohttp/web_app.py:351-360`), which fires the `on_cleanup` signal.

4. **`AppRunner` calls `cleanup`** (`AppRunner calls: cleanup`).

### Application Lifecycle Signals

The Application exposes four lifecycle signal properties:
- `on_startup` (`on_startup`, `aiohttp/web_app.py:314-315`)
- `on_shutdown` (`on_shutdown`, `aiohttp/web_app.py:318-319`)
- `on_cleanup` (`on_cleanup`, `aiohttp/web_app.py:322-323`)
- `cleanup_ctx` (`cleanup_ctx`, `aiohttp/web_app.py:326-327`)

These connect to `CleanupContext` (`CleanupContext`, `aiohttp/web_app.py:415-441`), which is called_by `Application`. `_on_startup` (`_on_startup`, `aiohttp/web_app.py:420-428`) accumulates exit callbacks. `_on_cleanup` (`_on_cleanup`, `aiohttp/web_app.py:430-441`) unwinds in reverse order and raises `CleanupError` if any step fails.

Application lifecycle methods:
- `startup()` (`startup`, `aiohttp/web_app.py:337-342`) -- fires `on_startup` signal
- `shutdown()` (`shutdown`, `aiohttp/web_app.py:344-349`) -- fires `on_shutdown` signal
- `cleanup()` (`cleanup`, `aiohttp/web_app.py:351-360`) -- fires `on_cleanup`, delegates to `_on_cleanup`

### Server -> RequestHandler -> Application

**`Server`** (`Server`, `aiohttp/web_server.py:30-126`) receives the Application's `_handle` callable. On each connection, `Server.__call__()` creates a `RequestHandler` (`__call__ uses: RequestHandler (web_protocol)`, `aiohttp/web_server.py:116-126`). The server also handles `shutdown` (`shutdown`, `aiohttp/web_server.py:111-114`) and `pre_shutdown` which iterates over connections (`pre_shutdown`, `aiohttp/web_server.py:107-109`).

### BaseRunner Cleanup -> Application

`BaseRunner.cleanup()` (`cleanup`, `aiohttp/web_runner.py:305-330`) stops all sites, calls `self._server.pre_shutdown()`, then `await self.shutdown()`, then `await self._server.shutdown(timeout)`, and finally `await self._cleanup_server()`.

### Application -> Sub-Application

`Application._add_subapp` mounts sub-applications. `add_domain` (`add_domain`, `aiohttp/web_app.py:296-304`) calls `_add_subapp` and uses `Domain`/`MaskDomain` from `web_urldispatcher` for domain-based routing.

### `run_app` -> Application

`run_app()` is called by `main()` (`main`, `aiohttp/web.py:501-565`), which calls `run_app`. This is the top-level entry point that starts the Application.

### Testing Infrastructure -> Application

- `aiohttp_server` (`aiohttp_server`, `aiohttp/pytest_plugin.py:296-321`) creates a `TestServer` from an app
- `aiohttp_client` factory creates test clients
- Example test fixtures create `web.Application()` instances (`__init__`, `tests/test_worker.py:31-38`)

### Example Shutdown Handlers

Example apps register `on_shutdown` callbacks:
- `on_shutdown` in `examples/web_ws.py:49-51` -- closes WebSockets: `ACCUMULATE(app[sockets] loop -> result)`
- `on_shutdown` in `examples/background_tasks.py:29-31` -- closes WebSockets: `ACCUMULATE(app[websockets] loop -> result)`

### WebSocket Interaction

`WebSocketResponse` (`WebSocketResponse`, `aiohttp/web_ws.py:78-773`) extends `StreamResponse` and is used within request handlers. It calls `WebSocketReady` (which is `called_by: can_prepare, WebSocketResponse`).

### What Cannot Be Determined

- The internal implementation of `Application._handle` and how it chains middleware.
- The full `__call__` implementation of `Server` (listed as uncovered in GAPS).
- The `ServerFingerprintMismatch` class (listed as uncovered).
- How `aiohttp_client` connects to Application (listed as uncovered).
- The exact signal dispatch mechanism in `startup()`/`shutdown()`.
