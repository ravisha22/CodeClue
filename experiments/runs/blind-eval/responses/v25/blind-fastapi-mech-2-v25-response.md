# v2.5 Response: blind-fastapi-mech-2
Date: 2026-04-16

## Question
How does FastAPI turn raised exceptions and validation failures into HTTP responses?

## Answer

The clue file and source snippets reveal a structured exception handling system with dedicated exception classes, registered handlers, and customization hooks.

### 1. Exception Class Hierarchy

FastAPI defines a clear exception hierarchy in `fastapi/exceptions.py`:

- **`ValidationException`** (line 174–209): extends `Exception`. Calls `_format_endpoint_context` to include endpoint file/line context in error messages.
- **`RequestValidationError`** (line 212–221): extends `ValidationException`. Raised when incoming request data fails validation.
- **`ResponseValidationError`** (line 234–243): extends `ValidationException`. Raised when outgoing response data fails serialization validation.
- **`WebSocketRequestValidationError`** (line 224–231): extends `ValidationException`. Raised for invalid WebSocket requests.
- **`HTTPException`** (line 17–83): extends `StarletteHTTPException`. An HTTP exception users can raise in their own code to show errors to the client.

`_format_endpoint_context` (`fastapi/exceptions.py:193–202`) has behavior `GUARD(not (self.endpoint_file and self.endpoint_line ...) -> return ...)`, meaning it only adds endpoint context when file/line information is available.

### 2. Default Exception Handlers

FastAPI registers default handlers in `fastapi/exception_handlers.py`:

- **`http_exception_handler`** (line 11–17): handles `HTTPException` instances. Uses `JSONResponse` or `Response` from `starlette.responses` to produce the HTTP response.
- **`request_validation_exception_handler`** (line 20–26): handles `RequestValidationError`. Behavior: `DELEGATE(JSONResponse -> result)`. It serializes validation errors into a JSON response (the source snippet from tests confirms: `JSONResponse({"exception": "request-validation"})`).
- **`websocket_request_validation_exception_handler`** (source snippet, `fastapi/exception_handlers.py:29–34`): handles `WebSocketRequestValidationError` by closing the WebSocket with code `WS_1008_POLICY_VIOLATION` and the encoded errors as the reason.

The `FastAPI` class (`fastapi/applications.py:45–4693`) imports `fastapi.exception_handlers`, confirming these handlers are registered at application startup.

### 3. Validation Failures During Request Processing

**`_serialize_data`** (`fastapi/routing.py:467–490`) handles response serialization with behavior: `BRANCH(stream_item_field -> raise ResponseValidat..., else -> return json.du...)`. When response data fails serialization, it raises `ResponseValidationError` using `EndpointContext` for location info.

**`get_validation_alias`** (source snippet, `fastapi/dependencies/utils.py:1052–1054`): resolves field aliases for validation error location reporting: `va = getattr(field, "validation_alias", None); return va or field.alias`.

### 4. Security-Related Exceptions

Multiple security modules raise `HTTPException` via `make_not_authenticated_error`:

- **API Key** (`fastapi/security/api_key.py:29–43`): behavior `DELEGATE(HTTPException -> result)`. Called by `check_api_key` when no API key is provided (behavior: `GUARD(not api_key -> raise ...)`). Used by `APIKeyQuery`, `APIKeyHeader`, `APIKeyCookie`.
- **OAuth2** (`fastapi/security/oauth2.py:401–421`): similar delegation to `HTTPException`, used by `OAuth2`, `OAuth2AuthorizationCodeBearer`, `OAuth2PasswordBearer`.
- **HTTP auth** (`fastapi/security/http.py:87`): used by `HTTPBasic`, `HTTPBearer`, `HTTPDigest` — all of which raise `make_not_authenticated_error` and use `HTTPException` from `fastapi.exceptions`.

### 5. Custom Exception Handling (Documented Tutorials)

The `docs_src/handling_errors/` tutorials show user-customizable patterns:

- `custom_http_exception_handler` (`tutorial006_py310.py:13`): behavior `DELEGATE(http_exception_handler -> result)` — wraps the default handler.
- `http_exception_handler` (`tutorial004_py310.py:10`): behavior `DELEGATE(PlainTextResponse -> result)` — replaces JSON with plain text.
- `validation_exception_handler` (`tutorial005_py310.py:11`): behavior `DELEGATE(JSONResponse -> result)` — custom JSON formatting.
- `validation_exception_handler` (`tutorial004_py310.py:15`): behavior `ACCUMULATE(exc.errors() loop -> message)` — iterates errors to build a plain-text message.

`ValidationErrorLoggingRoute` (`docs_src/custom_request_and_route/tutorial002_py310.py:8–20`) extends `APIRoute` and calls `get_route_handler`, raising `HTTPException` — demonstrating route-level exception customization.

### 6. `SolvedDependency` Error Accumulation

`SolvedDependency` (source snippet, `fastapi/dependencies/utils.py:587–592`) contains an `errors: list[Any]` field, showing that dependency resolution collects all validation errors before they are converted to a response.

### What Cannot Be Determined
GAPS states `type: MECHANISTIC` with uncovered symbols: `DependencyScopeError`, `EndpointContext`, `ORJSONResponse`, `PydanticV1NotSupportedError`. The exact mechanism by which `FastAPI` registers exception handlers at startup (the `__call__` chain) and how the ASGI middleware catches exceptions before they reach these handlers is not fully traceable from the clue. The `ParamDetails` and `_get_signature` internal mechanics are also not fully covered.
