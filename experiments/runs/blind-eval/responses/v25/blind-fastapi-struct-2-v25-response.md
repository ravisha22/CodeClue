# v2.5 Response: blind-fastapi-struct-2
Date: 2026-04-16

## Question
Which shared configuration knobs does FastAPI document on `APIRouter` for shaping a whole group of endpoints?

## Answer

The clue file reveals `APIRouter`'s group-level configuration through its own definition and, more importantly, through `include_router`, which is where router-level options are applied to every route in the group.

### 1. `APIRouter` Definition
`APIRouter` (`fastapi/routing.py:1001–4953`) is described as "used to group *path operations*, for example to structure." It extends `Router` and uses `Default` from `fastapi.datastructures`, which indicates configurable parameters with placeholder defaults. Its constructor calls `_DefaultLifespan`, `_merge_lifespan_context`, and `_wrap_gen_lifespan_context` (FOCUS: `APIRouter`), indicating a **lifespan** configuration knob.

### 2. Configuration via `include_router`
The primary mechanism for applying group-wide knobs is `include_router`:

- **On `APIRouter`** (`fastapi/routing.py:1574–1827`): behavior is `BRANCH(prefix -> result, else -> result); ACCUMULATE(router.routes loop -> current tags)`. This reveals two explicit knobs:
  - **`prefix`**: The BRANCH on prefix shows it conditionally prepends a URL prefix to all included routes.
  - **`tags`**: The ACCUMULATE annotation shows tags are merged into "current tags" for each route in the loop.

- **On `FastAPI`** (`fastapi/applications.py:1359–1564`): called by `FastAPI`, also uses `Default` and `Doc` from `annotated_doc`, confirming documented parameters.

- Both variants call `add_api_route` (`fastapi/routing.py:1332`), `add_api_websocket_route` (`fastapi/routing.py:1477`), and `add_event_handler` (`fastapi/routing.py:4901`), indicating that **event handlers** (startup/shutdown) are also merged at the group level. The `add_event_handler` behavior `BRANCH(event_type == 'startup' -> ..., else -> ...)` confirms startup and shutdown handlers are group-configurable.

- `include_router` raises `FastAPIError` (`fastapi/exceptions.py:161–164`), indicating validation of configuration.

### 3. HTTP Verb Methods as Decorators
The `api_route` method (`fastapi/routing.py:1415–1477`) is called by `delete`, `get`, `head`, `options`, `patch`, `post`, `put`, `trace` (FOCUS: `api_route`). Each verb decorator calls `add_api_route`, which uses `Default`, suggesting each path operation can override or inherit group defaults.

### 4. `get` Method Signature Clue
The `get` method on `APIRouter` (`fastapi/routing.py:1827–2204`) uses both `Default` and `Doc`, and the `delete` method (`fastapi/routing.py:2968–3345`) has the same pattern. The common parameters surfaced through `Doc` annotations likely include `response_model`, `status_code`, `tags`, `dependencies`, `summary`, `description`, `response_description`, `responses`, `deprecated`, and similar — but the clue does not enumerate them individually.

### What Cannot Be Determined
The GAPS section notes coverage of 79 symbols in L3 with 40 behavior annotations but does not list specific uncovered knobs. The full parameter list of `APIRouter.__init__` and `include_router` — including parameters like `dependencies`, `responses`, `default_response_class`, `callbacks`, `deprecated`, `generate_unique_id_function` — **cannot be determined** from the clue alone. The clue confirms **prefix**, **tags**, **lifespan/event handlers**, and **Default-based configurable parameters** exist, but the exhaustive list is not enumerable.
