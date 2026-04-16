# v2.5 Response: blind-fastapi-struct-1
Date: 2026-04-16

## Question
In FastAPI's documented bigger-application pattern, what public building blocks are used to split one API across multiple files and packages?

## Answer

Based solely on the clue file, the documented bigger-application pattern relies on three primary public building blocks:

### 1. `FastAPI` — The Root Application
The `FastAPI` class (`fastapi/applications.py:45–4693`) is the main entrypoint. It extends `Starlette` and serves as the top-level application object. It calls `include_router` to absorb routers defined in other modules, as well as `add_api_route`, `add_api_websocket_route`, and HTTP-verb methods (`get`, `delete`, `head`) to register path operations directly.

### 2. `APIRouter` — The Grouping Mechanism
The `APIRouter` class (`fastapi/routing.py:1001–4953`) is explicitly described as "used to group *path operations*, for example to structure." It extends `Router` and provides the same HTTP-verb decorators as `FastAPI` — its `api_route` method (`fastapi/routing.py:1415`) is called by `delete`, `get`, `head`, `options`, `patch`, `post`, `put`, and `trace` (FOCUS entry for `api_route`). Each `APIRouter` can register routes via `add_api_route` (`fastapi/routing.py:1332`), websocket routes via `add_api_websocket_route` (`fastapi/routing.py:1477`), and event handlers via `add_event_handler` (`fastapi/routing.py:4901`).

### 3. `include_router` — The Composition Mechanism
Two variants exist:
- **On `APIRouter`** (`fastapi/routing.py:1574–1827`): "Include another `APIRouter` in the same current `APIRouter`." Its behavior is `BRANCH(prefix -> result, else -> result); ACCUMULATE(router.routes loop -> current tags)`, meaning it iterates the included router's routes and re-registers them, prepending a prefix and merging tags. It calls `add_api_route`, `add_api_websocket_route`, `add_event_handler`, and `_merge_lifespan_context`.
- **On `FastAPI`** (`fastapi/applications.py:1359–1564`): "Include an `APIRouter` in the same app," called by `FastAPI`.

### Package Structure Evidence
The TREE section shows `docs_src/bigger_applications/` exists as a dedicated tutorial directory, and the INDEX shows sub-packages like `docs_src/app_testing/app_b_an_py310/` with `__init__.py` files, demonstrating the multi-file/package pattern. The presence of `__init__.py` files at each level (INDEX entries showing `0L` init files) confirms standard Python package structure is used.

### Supporting Types
- `APIWebSocketRoute` (`fastapi/routing.py:765`) extends `WebSocketRoute` and is called by `add_api_websocket_route` to handle WebSocket routes within routers.
- `Default` from `fastapi.datastructures` is used extensively by routing functions to provide placeholder defaults.

### What Cannot Be Determined
The GAPS section states `include_router` is **uncovered** — its full parameter list (e.g., prefix, tags, dependencies, responses) is not detailed in the clue's behavior annotations. The exact set of configuration knobs passed during `include_router` calls cannot be fully enumerated from this clue alone. The GAPS also notes `delete` and `head` are uncovered, so their full signatures are not confirmed.
