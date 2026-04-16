# v2.5 Response: blind-fastapi-rel-2
Date: 2026-04-16

## Question
How do router-level options and path-level options combine when FastAPI builds a larger application from routers?

## Answer

The clue file and source snippets reveal a layered delegation model: `FastAPI` delegates to its internal `APIRouter`, which in turn merges router-level options with each route's path-level options during `include_router`.

### 1. FastAPI Delegates Everything to Its Internal Router

Every HTTP method on `FastAPI` delegates to the corresponding method on its internal router:
- `get` (`fastapi/applications.py:1564–1937`): `DELEGATE(router.get -> result)`
- `post` (`fastapi/applications.py:2315–2693`): `DELEGATE(router.post -> result)`
- `delete` (`fastapi/applications.py:2693–3066`): `DELEGATE(router.delete -> result)`
- `options` (`fastapi/applications.py:3066–3439`): `DELEGATE(router.options -> result)`
- `head`, `patch`, `put`, `trace` follow the same pattern.

Similarly, `include_router` on `FastAPI` (`fastapi/applications.py:1359–1564`) delegates to the internal router's version, confirming the `FastAPI` class itself is a thin wrapper over `APIRouter`.

### 2. `include_router` Merges Router-Level Options into Path-Level Routes

`include_router` on `APIRouter` (`fastapi/routing.py:1574–1827`) is the core merging function:
- **Behavior**: `BRANCH(prefix -> result, else -> result); ACCUMULATE(router.routes loop -> current tags)`
- It iterates over every route in the included router and re-registers each one via `add_api_route` and `add_api_websocket_route`, applying the router-level prefix and tags.
- The `BRANCH(prefix ...)` shows that if a prefix is provided, it is prepended to each route's path; otherwise the route's original path is used.
- The `ACCUMULATE(... -> current tags)` shows that tags are merged per-route during the loop.

It also calls:
- `add_event_handler` — merging startup/shutdown handlers from the included router.
- `_merge_lifespan_context` (`fastapi/routing.py:205–219`) — combining lifespan contexts from the parent and child routers.

It raises `FastAPIError` when invalid configurations are detected, using `FastAPIError` from `fastapi.exceptions`.

### 3. Path-Level Route Registration

`add_api_route` (`fastapi/routing.py:1332–1415`) is called by both `api_route` (the decorator) and `include_router`. It uses `Default` from `fastapi.datastructures`, indicating it supports configurable parameters with placeholder defaults that can be overridden at the path level or inherited from the router level.

`api_route` (`fastapi/routing.py:1415–1477`) is the decorator used by `get`, `post`, `delete`, `options`, `patch`, `put`, `head`, `trace`. It calls `add_api_route`, passing through path-level options.

### 4. OpenAPI Schema Reflects the Merged Configuration

`get_openapi_path` (source snippet, `fastapi/openapi/utils.py:263–481`) processes each `route` object after merging. The snippet shows:
- It reads `route.methods`, `route.response_class`, `route.include_in_schema`, `route.status_code`, `route.response_description`, `route.responses`, `route.callbacks`, `route.response_field`, `route.is_json_stream`, `route.is_sse_stream`, `route.stream_item_field`, and `route.body_field`.
- It calls `get_flat_dependant(route.dependant)` to extract parameters from the dependency tree.
- Security definitions are extracted via `get_openapi_security_definitions(flat_dependant=flat_dependant)`.
- Required parameter definitions take precedence: `all_parameters.update(required_parameters)`.

This confirms that by the time the OpenAPI schema is generated, router-level and path-level options have already been merged into the route objects.

### 5. Body Field Combination

`get_body_field` (`fastapi/dependencies/utils.py:998–1049`, source snippet) combines body parameters from the dependency graph into a single model field for OpenAPI generation. It checks whether to embed body fields, creates a composite `BodyModel` via `create_body_model`, and selects the appropriate `FieldInfo` type (`params.File`, `params.Form`, or `params.Body`).

### What Cannot Be Determined
GAPS notes `type: MECHANISTIC` and lists uncovered symbols: `_async_stream_raw`, `_build_response_args`, `_shutdown`, `_sse_producer_cm`. The drill targets indicate the full body logic of `options` methods on both `fastapi/routing.py` and `fastapi/applications.py` is not included. The exact precedence rules for how path-level options override router-level defaults (e.g., does a path-level `tags` replace or append to router-level `tags`?) cannot be fully determined from the clue and snippets alone — the ACCUMULATE annotation on `include_router` suggests merging/appending rather than replacement, but the precise semantics are not confirmed.
