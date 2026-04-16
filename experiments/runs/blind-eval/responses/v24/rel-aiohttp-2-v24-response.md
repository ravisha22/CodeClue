# v2.4 Response: rel-aiohttp-2
Date: 2026-04-16

## Question
What are the main call relationships between the Application class and other components in aiohttp's web server stack?

## Answer

### Application Class Overview

The `Application` class (`Application`, `aiohttp/web_app.py:71-400`) is the central orchestrator of aiohttp's web server stack. It imports `asyncio, logging, warnings, aiosignal, frozenlist` and calls: `_add_subapp`, `_check_frozen`, `_prepare_middleware`, `handler`, `reg_handler`, `_reg_subapp_signals`, `add_routes`, `freeze`. It raises `TypeError`, `RuntimeError`, `ValueError`.

### Application → Lifecycle Signals

The Application exposes lifecycle hooks as signal properties:

- **`on_startup`** (`on_startup`, `aiohttp/web_app.py:314-315`) — signal fired during application startup.
- **`on_shutdown`** (`on_shutdown`, `aiohttp/web_app.py:318-319`) — signal fired during shutdown.
- **`on_cleanup`** (`on_cleanup`, `aiohttp/web_app.py:322-323`) — signal fired during cleanup.
- **`cleanup_ctx`** (`cleanup_ctx`, `aiohttp/web_app.py:326-327`) — context for paired startup/cleanup generators.

The Application lifecycle methods that fire these signals:
- **`startup()`** (`startup`, `aiohttp/web_app.py:337-342`) — causes the `on_startup` signal.
- **`shutdown()`** (`shutdown`, `aiohttp/web_app.py:344-349`) — causes the `on_shutdown` signal.
- **`cleanup()`** (`cleanup`, `aiohttp/web_app.py:351-360`) — branches on `on_cleanup.frozen` and calls `_on_cleanup`.

### Application → Freeze/Pre-freeze

- **`pre_freeze()`** (`pre_freeze`, `aiohttp/web_app.py:212`) — called before freezing the application.
- **`freeze()`** (`freeze`, `aiohttp/web_app.py:241`) — freezes the application configuration, making it immutable. Called by Application itself and by `AppRunner._make_server`.

### Application → Route Registration

- **`reg_handler()`** (`reg_handler`, `aiohttp/web_app.py:260`) — registers a handler, called by Application.
- **`add_routes()`** — called by Application to add routes to the URL dispatcher.
- **`add_domain()`** (`add_domain`, `aiohttp/web_app.py:296-304`) — registers a domain-based sub-application, calling `_add_subapp` and raising `TypeError`. Uses `MaskDomain` and `Domain` from `web_urldispatcher`.

### Application → Sub-applications

- **`_add_subapp()`** — called by Application (and `add_domain`) to attach sub-applications.
- **`_reg_subapp_signals()`** — called by Application to propagate lifecycle signals to sub-apps.

### Application → Middleware

- **`_prepare_middleware()`** — called by Application to prepare the middleware chain.
- **`_check_frozen()`** — called by Application to verify the app is not frozen before modifications.

### Application → CleanupContext / CleanupError

- **`CleanupContext`** (`CleanupContext`, `aiohttp/web_app.py:415-441`) is called by Application and manages paired startup/cleanup async generators. It calls `CleanupError` on failures.
- **`CleanupError`** (`CleanupError`, `aiohttp/web_app.py:403-406`) extends `RuntimeError` and is called by `_on_cleanup` and `CleanupContext`.
- **`_on_cleanup()`** (`_on_cleanup`, `aiohttp/web_app.py:430-441`) iterates `reversed(self._exits)` to unwind cleanup, accumulating errors.

### AppRunner → Application

The `AppRunner` is not directly in the FOCUS section but is referenced. The GAPS section lists `Application` as uncovered at the detail level, but we can infer relationships from other entries:

- `AppRunner` (`AppRunner`, mentioned in `cleanup called_by`) calls `cleanup()` on the runner, which invokes site stopping and eventually `self._app.cleanup()`.

### Application → URL Dispatcher Components

The Application interacts with URL dispatch through:

- **`UrlDispatcher`** (`UrlDispatcher`, `aiohttp/web_urldispatcher.py:965-1227`) extends `AbstractRouter` and calls `DynamicResource`, `MatchInfoError`, `PlainResource`, `ResourcesView`, `RoutesView`, `StaticResource`, `_get_resource_index_key`, `add_resource`.
- **`Resource`** (`Resource`, `aiohttp/web_urldispatcher.py:308-357`) extends `AbstractResource`, calls `register_route`, `ResourceRoute`, `UrlMappingMatchInfo`.
- **`PlainResource`** (`PlainResource`, `aiohttp/web_urldispatcher.py:362-399`) extends `Resource`, called by `add_resource` and `UrlDispatcher`.
- **`DynamicResource`** (`DynamicResource`, `aiohttp/web_urldispatcher.py:402-472`) extends `Resource`, called by `add_resource` and `UrlDispatcher`.
- **`StaticResource`** (`StaticResource`, `aiohttp/web_urldispatcher.py:500-704`) extends `PrefixResource`, called by `add_static` and `UrlDispatcher`.
- **`PrefixedSubAppResource`** (`PrefixedSubAppResource`, `aiohttp/web_urldispatcher.py:707-748`) extends `PrefixResource`, calls `_add_prefix_to_resources`, `index_resource`, `resources`, `routes`, `unindex_resource`, `add_app`.

### Application → Request/Response Pipeline

- **`BaseRequest`** (`BaseRequest`, `aiohttp/web_request.py:109-823`) extends `HeadersMixin`, the server-side request object.
- **`Request`** (extends `BaseRequest`) is the concrete type used in handlers.
- **`StreamResponse`** (`StreamResponse`, `aiohttp/web_response.py:74-532`) extends `HeadersMixin, CookieMixin`.
- **`Response`** (`Response`, `aiohttp/web_response.py:535-740`) extends `StreamResponse`, called by `json_bytes_response` and `json_response`.
- **`WebSocketResponse`** (`WebSocketResponse`, `aiohttp/web_ws.py:78-773`) extends `StreamResponse`.

### Application → Server Infrastructure

- **`Server`** (`Server`, `aiohttp/web_server.py:30-126`) calls `shutdown`. The `_make_server` method (`_make_server`, `aiohttp/web_runner.py:421-430`) delegates to `Server`.
- **`BaseSite`** (`BaseSite`, `aiohttp/web_runner.py:47-78`) extends `ABC`, calls `_check_site`, `_reg_site`, `_unreg_site`.
- **`BaseRunner`** (`BaseRunner`, `aiohttp/web_runner.py:252-352`) extends `ABC`, calls `stop`.

### Application → Worker Integration

- **`GunicornWebWorker`** (`GunicornWebWorker`, `aiohttp/worker.py:33-234`) extends `Worker` and calls `_create_ssl_context`, `_notify_waiter_done`, `_run`, etc.
- **`GunicornUVLoopWebWorker`** (`GunicornUVLoopWebWorker`, `aiohttp/worker.py:237-246`) extends `GunicornWebWorker`.

### Application → View Handling

- **`View`** (`View`, `aiohttp/web_urldispatcher.py:915-931`) extends `AbstractView`, calls `method`, `__await__`, `_iter`, `_raise_allowed_methods`. Raises `HTTPMethodNotAllowed`.
- **`RouteDef`** (`RouteDef`, `aiohttp/web_routedef.py:46-67`) extends `AbstractRouteDef`, called by `RouteTableDef`.

### Application → Domain-Based Routing

- **`Domain`** (`Domain`, `aiohttp/web_urldispatcher.py:766-803`) extends `AbstractRuleMatching`, calls `validation`.
- **`MaskDomain`** (`MaskDomain`, `aiohttp/web_urldispatcher.py:806-819`) extends `Domain`.

### Cannot Be Determined from Clue File

The GAPS section explicitly lists these as **uncovered**: `Application`, `Server`, `ServerRunner`, `aiohttp_raw_server`. This means:
- The full internal implementation and call graph of `Application.__init__`, `Application._handle`, and how the Application connects to middleware dispatch cannot be fully traced.
- The exact relationship between `Application` and `Server` creation (typically done via `AppRunner`) is only partially visible.
- How `Application.handler` works internally is not detailed beyond being called by Application.
