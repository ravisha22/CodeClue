You are a senior software engineer performing a development task.
You have access to a CodeClue artifact — a compact comprehension file.

## Task
Add request body size limiting middleware to FastAPI. Which files define middleware registration and where should the new middleware be inserted?

## CodeClue Artifact
```json
{
  "task": {
    "id": "trace-fixed-reproject",
    "repo": "",
    "family": "OF3",
    "question": "Add request body size limiting middleware to FastAPI. Which files define middleware registration and where should the new middleware be inserted?"
  },
  "summary": "get_request_handler: Async Error handler; produces _async_stream_raw, _serialize_data, _serialize_data; exceptions are swallowed. request_response: Function request_response. build_middleware_stack: Function build_middleware_stack.",
  "entities": [
    {
      "id": "n1",
      "class": "error_handler",
      "name": "get_request_handler",
      "file": "fastapi/routing.py",
      "lines": [
        347,
        727
      ],
      "confidence": 0.92,
      "purpose": "function get_request_handler",
      "behavior": "Async Error handler; produces _async_stream_raw, _serialize_data, _serialize_data; exceptions are swallowed.",
      "sig": "async def app(request: Request) -> Response:",
      "calls": [
        "get",
        "_build_response_args",
        "_extract_endpoint_context",
        "_async_stream_jsonl",
        "n11",
        "n12",
        "_serialize_item",
        "_serialize_sse_item",
        "_sse_producer_cm",
        "_sse_with_checkpoints",
        "n14",
        "run_endpoint_function",
        "serialize_response"
      ],
      "called_by": [
        "get_route_handler"
      ],
      "risks": [
        "exception_swallowed"
      ]
    },
    {
      "id": "n2",
      "class": "utility",
      "name": "request_response",
      "file": "fastapi/routing.py",
      "lines": [
        95,
        132
      ],
      "confidence": 0.92,
      "purpose": "function request_response",
      "behavior": "Function request_response.",
      "sig": "def request_response( func: Callable[[Request], Awaitable[Response] | Response], ) -> ASGIApp:"
    },
    {
      "id": "n3",
      "class": "utility",
      "name": "build_middleware_stack",
      "file": "fastapi/applications.py",
      "lines": [
        1021,
        1069
      ],
      "confidence": 0.92,
      "purpose": "function build_middleware_stack",
      "behavior": "Function build_middleware_stack.",
      "sig": "def build_middleware_stack(self) -> ASGIApp:"
    },
    {
      "id": "n4",
      "class": "utility",
      "name": "middleware",
      "file": "fastapi/applications.py",
      "lines": [
        4601,
        4647
      ],
      "confidence": 0.92,
      "purpose": "function middleware",
      "behavior": "Async Function middleware.",
      "sig": "async def add_process_time_header( request: Request, call_next: Callable[[Request], Awaitable[Response]] ) -> Response:"
    },
    {
      "id": "n5",
      "class": "middleware",
      "name": "middleware",
      "file": "tests/test_dependency_contextmanager.py",
      "lines": [
        207,
        210
      ],
      "confidence": 0.92,
      "purpose": "async_function middleware",
      "behavior": "Async Middleware between middleware and middleware. [returns response]",
      "sig": "async def middleware(request, call_next):",
      "calls": [
        "n5"
      ],
      "called_by": [
        "n5"
      ]
    },
    {
      "id": "n6",
      "class": "utility",
      "name": "websocket_middleware",
      "file": "tests/test_ws_router.py",
      "lines": [
        188,
        207
      ],
      "confidence": 0.92,
      "purpose": "function websocket_middleware",
      "behavior": "Function websocket_middleware. [returns await app(scope, receive, send)  # pragma: no cover; returns await app(scope, receive, send); returns await middleware_func(websocket, call_next); returns wrapped_app; returns middleware_constructor]",
      "sig": "def websocket_middleware(middleware_func):"
    },
    {
      "id": "n7",
      "class": "utility",
      "name": "run_middleware",
      "file": "tests/test_custom_middleware_exception.py",
      "lines": [
        57,
        58
      ],
      "confidence": 0.92,
      "purpose": "function run_middleware",
      "behavior": "Function run_middleware. [returns {\"message\": \"OK\"}]"
    },
    {
      "id": "n8",
      "class": "utility",
      "name": "middleware_constructor",
      "file": "tests/test_ws_router.py",
      "lines": [
        193,
        205
      ],
      "confidence": 0.92,
      "purpose": "function middleware_constructor",
      "behavior": "Function middleware_constructor. [returns await app(scope, receive, send)  # pragma: no cover; returns await app(scope, receive, send); returns await middleware_func(websocket, call_next); returns wrapped_app]",
      "sig": "def middleware_constructor(app):"
    },
    {
      "id": "n9",
      "class": "utility",
      "name": "custom_middleware",
      "file": "tests/test_dependency_contextvars.py",
      "lines": [
        23,
        28
      ],
      "confidence": 0.92,
      "purpose": "async_function custom_middleware",
      "behavior": "Async Async_function custom_middleware. [returns response]",
      "sig": "async def custom_middleware( request: Request, call_next: Callable[[Request], Awaitable[Response]] ):"
    },
    {
      "id": "n10",
      "class": "utility",
      "name": "FastAPI",
      "file": "fastapi/applications.py",
      "lines": [
        45,
        4693
      ],
      "confidence": 0.92,
      "purpose": "class FastAPI",
      "behavior": "Async Class FastAPI.",
      "sig": "async def read_items():"
    },
    {
      "id": "n11",
      "class": "handler",
      "name": "_async_stream_raw",
      "file": "fastapi/routing.py",
      "lines": [
        654,
        663
      ],
      "confidence": 0.92,
      "purpose": "async_function _async_stream_raw",
      "behavior": "Async Leaf handler invoked by get_request_handler. [is a generator]",
      "sig": "async def _async_stream_raw( async_gen: AsyncIterator[Any], ) -> AsyncIterator[Any]:",
      "called_by": [
        "n1"
      ]
    },
    {
      "id": "n12",
      "class": "validator",
      "name": "_serialize_data",
      "file": "fastapi/routing.py",
      "lines": [
        467,
        490
      ],
      "confidence": 0.92,
      "purpose": "function _serialize_data",
      "behavior": "Validates input before processing. [raises ResponseValidationError; returns stream_item_field.serialize_json(]",
      "sig": "def _serialize_data(data: Any) -> bytes:",
      "called_by": [
        "_serialize_item",
        "_serialize_sse_item",
        "n1"
      ]
    },
    {
      "id": "n13",
      "class": "utility",
      "name": "_producer",
      "file": "fastapi/routing.py",
      "lines": [
        552,
        557
      ],
      "confidence": 0.92,
      "purpose": "async_function _producer",
      "behavior": "Async Async_function _producer.",
      "sig": "async def _producer() -> None:",
      "calls": [
        "_serialize_sse_item"
      ]
    },
    {
      "id": "n14",
      "class": "handler",
      "name": "_sync_stream_jsonl",
      "file": "fastapi/routing.py",
      "lines": [
        637,
        641
      ],
      "confidence": 0.92,
      "purpose": "function _sync_stream_jsonl",
      "behavior": "Leaf handler invoked by get_request_handler. [is a generator]",
      "sig": "def _sync_stream_jsonl() -> Iterator[bytes]:",
      "calls": [
        "_serialize_item"
      ],
      "called_by": [
        "n1"
      ]
    },
    {
      "id": "n15",
      "class": "utility",
      "name": "ContentSizeLimitMiddleware",
      "file": "tests/test_custom_middleware_exception.py",
      "lines": [
        12,
        53
      ],
      "confidence": 0.92,
      "purpose": "class ContentSizeLimitMiddleware",
      "behavior": "Class ContentSizeLimitMiddleware; may return None implicitly. [returns message  # pragma: no cover]",
      "sig": "def __init__(self, app: APIRouter, max_content_size: int | None = None):",
      "risks": [
        "implicit_none_return"
      ]
    }
  ],
  "uncertainty": {
    "confidence": 0.7,
    "hint": "targeted_lookup",
    "gaps": []
  }
}
```

## Required Output
- List every file that must be modified
- List every function/class involved (cite entity IDs)
- Explain the execution/impact path
- Identify what additional source you would need