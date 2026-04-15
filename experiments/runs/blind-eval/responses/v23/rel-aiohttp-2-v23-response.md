# v2.3 Response: rel-aiohttp-2
Date: 2026-04-15

## Summary

The `Application` class (`aiohttp/web_app.py`) is central to aiohttp's web server stack, connecting to the URL dispatcher, runner infrastructure, server, request handling, and lifecycle management. While the `Application` class itself is not detailed with a full FOCUS entry in this clue file, its call relationships to other components are extensively documented through the surrounding class entries.

## Application Class Overview

The `Application` class is defined in `aiohttp/web_app.py:71-400` (FOCUS). It:
- **Imports**: `asyncio`, `logging`, `warnings`, `aiosignal`, `frozenlist`.
- **Calls**: `_add_subapp`, `_check_frozen`, `_prepare_middleware`, `handler`, `reg_handler`, `_reg_subapp_signals`, `add_routes`, `freeze`.
- **Raises**: `TypeError`, `RuntimeError`, `ValueError`.

## Application → URL Dispatcher (UrlDispatcher)

- **`UrlDispatcher`** (`aiohttp/web_urldispatcher.py:965-1227`, FOCUS) → extends `AbstractRouter`. The Application calls `add_routes` (listed in Application's calls), which registers routes with the dispatcher.
- The dispatcher calls `DynamicResource`, `MatchInfoError`, `PlainResource`, `ResourcesView`, `RoutesView`, `StaticResource`, `_get_resource_index_key`, `add_resource`.
- **`ResourcesView`** (`aiohttp/web_urldispatcher.py:934-945`, FOCUS) — called by `resources` and `UrlDispatcher`, extends `Sized`.
- **`RoutesView`** (`aiohttp/web_urldispatcher.py:948-962`, FOCUS) — called by `routes` and `UrlDispatcher`, extends `Sized`.
- **Route definitions**: `RouteDef` (`aiohttp/web_routedef.py:46-67`, FOCUS) extends `AbstractRouteDef`, called by `inner` and `RouteTableDef`.

## Application → Runner (AppRunner)

- **`AppRunner`** (`aiohttp/web_runner.py:380-453`, FOCUS) — wraps the Application. Its `shutdown()` delegates to `await self._app.shutdown()`. Its `_make_server()` calls `self._app.on_startup.freeze()`, `await self._app.startup()`, `self._app.freeze()`, then creates a `Server` with `self._app._handle`. Its `_cleanup_server()` calls `await self._app.cleanup()`.
- **`BaseRunner`** (`aiohttp/web_runner.py:252-352`, FOCUS) → extends `ABC`. The abstract base that `AppRunner` inherits from. Calls `stop`. Manages sites, server lifecycle, and signal handlers.

## Application → Server

- The `AppRunner._make_server()` creates a `Server` object passing `self._app._handle` as the request handler. This means the Application provides the main request handler function (`_handle`) to the low-level server.
- **`Server`** (`aiohttp/web_server.py:30-126`, from other entries) — receives the Application's handler.

## Application → Lifecycle Signals

The Application exposes several lifecycle signals (from FOCUS/SYM entries in `aiohttp/web_app.py`):
- **`on_startup`** (L314-315) — Startup signal, frozen during `AppRunner._make_server()`.
- **`on_shutdown`** (L318-319) — Shutdown signal, triggered during `Application.shutdown()` (L344-349: *"Causes on_shutdown signal"*).
- **`on_cleanup`** (L322-323) — Cleanup signal, triggered during `Application.cleanup()` (L351-360: *"Causes on_cleanup signal"*).
- **`cleanup_ctx`** (L326-327) — Cleanup context registration.
- **`startup()`** (L337-342) — *"Causes on_startup signal"*.
- **`shutdown()`** (L344-349) — *"Causes on_shutdown signal"*.
- **`cleanup()`** (L351-360) — Calls `_on_cleanup`.

## Application → CleanupContext / CleanupError

- **`CleanupContext`** (`aiohttp/web_app.py:415-441`, FOCUS) — called by `Application`. Raises `CleanupError`.
- **`CleanupError`** (`aiohttp/web_app.py:403-406`, FOCUS) → extends `RuntimeError`. Called by `_on_cleanup` and `CleanupContext`.
- **`_on_cleanup()`** (`aiohttp/web_app.py:430-441`, from other entries) — called by `cleanup` and `Application`. Behavior: `ACCUMULATE(loop -> errors); UNWIND(reversed)`.
- **`_on_startup()`** (`aiohttp/web_app.py:420-428`, from other entries) — behavior: `ACCUMULATE(loop -> exits)`.

## Application → Freezing and Middleware

- **`freeze()`** (`aiohttp/web_app.py:241`, SYM) — Freezes the application configuration. Called during `AppRunner._make_server()` after startup.
- **`pre_freeze()`** (`aiohttp/web_app.py:212`, SYM) — Pre-freeze preparation step.
- **`_prepare_middleware`** — Called by Application (listed in its `calls`), prepares the middleware chain.
- **`reg_handler()`** (`aiohttp/web_app.py:260`, SYM) — Registers handlers.
- **`handler`** — Called by Application (listed in its `calls`), the main request handler.

## Application → Sub-Applications

- **`_add_subapp`** — Called by Application to add sub-applications.
- **`_reg_subapp_signals`** — Called by Application to register sub-app lifecycle signals.
- **`PrefixedSubAppResource`** (`aiohttp/web_urldispatcher.py:707-748`, FOCUS) → extends `PrefixResource`. Calls `_add_prefix_to_resources`, `index_resource`, `resources`, `routes`, `unindex_resource`, `add_app`. This is the resource type used when mounting sub-apps at a prefix.

## Application → Request Handling Chain

The full request handling chain based on the clue entries:
1. **`Server`** receives raw HTTP connections.
2. **`RequestHandler`** (in `aiohttp/web_protocol.py`) manages the protocol level.
3. **`_handle_request()`** (`aiohttp/web_protocol.py:535-570`, from other entries) — calls `finish_response`, `handle_error`, uses `Response`.
4. The Application's `handler` (registered via `reg_handler`) processes the request through middleware.
5. **`BaseRequest`** (`aiohttp/web_request.py:109-823`, FOCUS) — the request object passed to handlers.

## Application → Static Resources

- **`StaticResource`** (`aiohttp/web_urldispatcher.py:500-704`, FOCUS) → extends `PrefixResource`. Called by `add_static` and `UrlDispatcher`. Handles static file serving with version keys, directory listing, and file hashing.

## Application → Views

- **`View`** (`aiohttp/web_urldispatcher.py:915-931`, FOCUS) → extends `AbstractView`. Provides class-based view support with method dispatching. Raises `HTTPMethodNotAllowed`.

## Application → Domain Routing

- **`Domain`** (`aiohttp/web_urldispatcher.py:766-803`, FOCUS) → extends `AbstractRuleMatching`. Provides domain-based routing with validation.

## Application → Worker Integration

- **`GunicornWebWorker`** (`aiohttp/worker.py:33-234`, FOCUS) → extends `Worker`. Integrates with Gunicorn for production deployment.
- **`GunicornUVLoopWebWorker`** (`aiohttp/worker.py:237-246`, FOCUS) → extends `GunicornWebWorker`. Adds uvloop support.

## Application → Testing

- **`AiohttpClient`** (`aiohttp/pytest_plugin.py:31-48`, FOCUS) → extends `Protocol`.
- **`AiohttpServer`** (`aiohttp/pytest_plugin.py:51-54`, FOCUS) → extends `Protocol`.
- **`AiohttpRawServer`** (`aiohttp/pytest_plugin.py:57-64`, FOCUS) → extends `Protocol`.

## Application → Sites

- **`BaseSite`** (`aiohttp/web_runner.py:47-78`, FOCUS) → extends `ABC`. Calls `_check_site`, `_reg_site`, `_unreg_site` on the runner.
- **`GracefulExit`** (`aiohttp/web_runner.py:39-40`, FOCUS) → extends `SystemExit` with `code=1`. Used for graceful shutdown signaling.

## Uncertainty / Limits

- The `Application` class's full attribute list (e.g., `_client_max_size`, `_handler_args`, `_handle`) is not visible in the FOCUS entry. These are referenced indirectly (e.g., `self.app._client_max_size` in `AppRunner._make_request`, `self._app._handle` in `AppRunner._make_server`).
- The exact middleware chain execution order and how `_prepare_middleware` constructs it is not detailed.
- The `handler` method called by `Application` is listed but its implementation is not shown — it likely wraps the middleware chain around the matched route handler.
- The `AbstractRouter` interface that `UrlDispatcher` implements is defined in `aiohttp/abc.py` but its method signatures are not fully detailed in this clue file.
