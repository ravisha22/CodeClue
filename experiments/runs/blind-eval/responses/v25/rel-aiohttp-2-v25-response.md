# v2.5 Response: rel-aiohttp-2
Date: 2026-04-16

## Question
What are the main call relationships between the Application class and other components in aiohttp's web server stack?

## Answer

### The Application Class

`Application` (FOCUS: `Application` at `aiohttp/web_app.py:71-400`) is the central orchestrating class. It directly calls:
- `_add_subapp` — sub-application mounting
- `_check_frozen` — state guard
- `_prepare_middleware` — middleware setup
- `handler` — request handler dispatch
- `reg_handler` (SYM: `aiohttp/web_app.py:260`) — handler registration
- `_reg_subapp_signals` — signal propagation to sub-apps
- `add_routes` — route registration
- `freeze` (SYM: `aiohttp/web_app.py:241`) — freezes the application state

It raises `TypeError`, `RuntimeError`, and `ValueError`.

### Application → Server Stack (Downward Calls)

**Application → Server via AppRunner:**

The `AppRunner` (FOCUS: `AppRunner` at `aiohttp/web_runner.py:380-453`) wraps the Application. Its key methods connect Application to the server infrastructure:
- `AppRunner.shutdown()` calls `self._app.shutdown()` (FOCUS: `shutdown` at `aiohttp/web_runner.py:418-419`).
- `AppRunner._make_server()` freezes `on_startup`, calls `self._app.startup()`, then `self._app.freeze()`, and creates a `Server` using `self._app._handle` as the request handler (FOCUS: `_make_server` at `aiohttp/web_runner.py:421-430`, uses `Server` from `web_server`).
- `AppRunner._cleanup_server()` calls `self._app.cleanup()` (FOCUS: `_cleanup_server` at `aiohttp/web_runner.py:452-453`).
- `AppRunner.cleanup()` calls `stop` on each site, then `self._server.pre_shutdown()`, `self.shutdown()`, `self._server.shutdown()`, and `self._cleanup_server()` (FOCUS: `cleanup` at `aiohttp/web_runner.py:305-330`).

**Server class:**

`Server` (FOCUS: `Server` at `aiohttp/web_server.py:30-126`) calls `shutdown` internally. Its `__call__` method (FOCUS: `__call__` at `aiohttp/web_server.py:116-126`) uses `RequestHandler` from `web_protocol` to handle incoming connections. The `_make_server` factory (FOCUS: `_make_server` at `aiohttp/web_runner.py:421-430`) delegates creation to `Server`.

### Application → Request Handling

The `Application._handle` method (not explicitly in FOCUS but referenced) is passed to `Server` as the request handler. The server-side flow is:

1. `Server.__call__` creates `RequestHandler` instances (FOCUS: `__call__` at `aiohttp/web_server.py:116-126`, uses `RequestHandler` from `web_protocol`).
2. `RequestHandler` dispatches to Application's handler for each request.

### Application → Runner → Site Hierarchy

**BaseRunner** (FOCUS: `BaseRunner` at `aiohttp/web_runner.py:252-352`, extends `ABC`) is the abstract base:
- `setup()` calls `_make_server()` to create the server.
- `cleanup()` iterates sites calling `stop`, then calls `pre_shutdown`, `shutdown`, `server.shutdown(timeout)`, and `_cleanup_server`.

**ServerRunner** (FOCUS: `ServerRunner` at `aiohttp/web_runner.py:355-377`) is a simpler runner that wraps a pre-made `Server`. Its `shutdown` and `_cleanup_server` are no-ops.

**BaseSite** (FOCUS: `BaseSite` at `aiohttp/web_runner.py:47-78`, extends `ABC`) calls `_check_site`, `_reg_site`, `_unreg_site` on the runner.

### Application → Entry Point

`main` (FOCUS: `main` at `aiohttp/web.py:501-565`) calls `run_app` (FOCUS: `run_app` at `aiohttp/web.py:426-498`), which calls `_cancel_tasks` and `_run_app`. This is the CLI entry point.

### Application → Worker Integration

`GunicornWebWorker` (FOCUS: `GunicornWebWorker` at `aiohttp/worker.py:33-234`, extends `Worker`) calls `__init__`, `_create_ssl_context`, `_get_valid_log_format`, `_notify_waiter_done`, `_run`, `_wait_next_notify`. `GunicornUVLoopWebWorker` (FOCUS: `:237-246`) extends `GunicornWebWorker`.

### Application → WebSocket Components

`WebSocketResponse` (FOCUS: `WebSocketResponse` at `aiohttp/web_ws.py:78-773`, extends `StreamResponse`) is used within the application context. `WebSocketReady` (FOCUS: `WebSocketReady` at `aiohttp/web_ws.py:70-75`) is called by `can_prepare` and `WebSocketResponse`. `WebSocketReader` (FOCUS: `aiohttp/_websocket/reader_c.py:141-499` and `reader_py.py:141-499`) and `WebSocketWriter` (FOCUS: `WebSocketWriter` at `aiohttp/_websocket/writer.py:40-262`) handle low-level WebSocket I/O.

### Application → Testing Infrastructure

- `AiohttpClient` (FOCUS: `aiohttp/pytest_plugin.py:31-48`, extends `Protocol`)
- `AiohttpServer` (FOCUS: `:51-54`, extends `Protocol`)
- `AiohttpRawServer` (FOCUS: `:57-64`, extends `Protocol`)
- `aiohttp_server` (FOCUS: `:296-321`) — factory using `TestServer` from `test_utils`
- `aiohttp_raw_server` (FOCUS: `:325-349`) — factory using `RawTestServer`
- `aiohttp_client_cls` (FOCUS: `:353-376`) — called by `aiohttp_client`

### Application → Error Handling

`HTTPInternalServerError` (FOCUS: `aiohttp/web_exceptions.py:463-464`, extends `HTTPServerError`, status_code=500) is used by the server stack when handlers fail.

Error classes in the client stack: `ServerConnectionError` → `ServerDisconnectedError`, `ServerTimeoutError` (FOCUS entries in `aiohttp/client_exceptions.py`).

### Application Lifecycle Signals

The Application has lifecycle signal properties (FOCUS entries):
- `on_startup` (FOCUS: `aiohttp/web_app.py:314-315`)
- `on_shutdown` (FOCUS: `:318-319`)
- `on_cleanup` (FOCUS: `:322-323`)
- `cleanup_ctx` (FOCUS: `:326-327`)
- `startup` (FOCUS: `:337-342`) — triggers `on_startup`
- `shutdown` (FOCUS: `:344-349`) — triggers `on_shutdown`
- `cleanup` (FOCUS: `cleanup` at `aiohttp/web_app.py:351-360`) — calls `_on_cleanup`

### What Cannot Be Determined

Per GAPS: "uncovered: __call__, ServerFingerprintMismatch, __call__, __call__." The full `__call__` implementations and some error-handling paths are not fully detailed. The complete middleware chain construction (`_prepare_middleware`) internals are not covered.
