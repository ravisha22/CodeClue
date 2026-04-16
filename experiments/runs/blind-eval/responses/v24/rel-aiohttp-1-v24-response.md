# v2.4 Response: rel-aiohttp-1
Date: 2026-04-16

## Question
What is the class hierarchy for request and response objects in aiohttp, and which classes extend which base classes?

## Answer

### Server-Side Request Hierarchy

1. **`BaseRequest`** (`BaseRequest`, `aiohttp/web_request.py:109-823`) extends `HeadersMixin`. This is the foundational server-side request class. It imports `asyncio, io, socket, string, tempfile` and calls methods like `_etag_values`, `_if_match_or_none_impl`, `get_extra_info`, `multipart`, `read`, `text`, `FileField`. It raises `RuntimeError`, `ValueError`, `HTTPUnsupportedMediaType`, `HTTPBadRequest` and uses `ETag` from `helpers`, `MultipartReader` from `multipart`, and HTTP exceptions from `web_exceptions`.

2. **`Request`** (`Request`, `aiohttp/web_request.py:826-884`) extends `BaseRequest`. This is the concrete request class used in typical web application handlers.

### Server-Side Response Hierarchy

1. **`StreamResponse`** (`StreamResponse`, `aiohttp/web_response.py:74-532`) extends `HeadersMixin, CookieMixin` (multiple inheritance). It provides streaming response capabilities and calls methods like `_generate_content_type_header`, `_prepare_headers`, `_set_status`, `_start_compression`, `_write_headers`, `drain`, `enable_compression`, `write`.

2. **`Response`** (`Response`, `aiohttp/web_response.py:535-740`) extends `StreamResponse`. This is the standard response class, called by `json_bytes_response` and `json_response`.

3. **`WebSocketResponse`** (`WebSocketResponse`, `aiohttp/web_ws.py:78-773`) extends `StreamResponse`. It handles WebSocket connections and calls `WebSocketReady`, `_cancel_heartbeat`, `_cancel_pong_response_cb`, `_close_transport`, `_handle_ping_pong_exception`, `_handshake`, `_ping_task_done`.

4. **`FileResponse`** (`FileResponse`, `aiohttp/web_fileresponse.py:79-406`) extends `StreamResponse`. Described as "A response object can be used to send files." It calls `_etag_match`, `_get_file_path_stat_encoding`, `_not_modified`, `_precondition_failed`, `_prepare_open_file`, `_sendfile`, `_sendfile_fallback`.

### Client-Side Request/Response Hierarchy

1. **`ClientResponse`** (`ClientResponse`, `aiohttp/client_reqrep.py:184-683`) extends `HeadersMixin`. It calls `_cleanup_writer`, `_notify_content`, `_release_connection`, `_wait_released`, `close`, `get_encoding`, `read`, `release`. It raises `ClientResponseError`, `RuntimeError`, `ClientConnectionError`, `ContentTypeError`.

2. **`_RequestInfo`** (`_RequestInfo`, `aiohttp/client_reqrep.py:102-106`) extends `NamedTuple`.

3. **`RequestInfo`** (`RequestInfo`, `aiohttp/client_reqrep.py:109-124`) extends `_RequestInfo` (which extends `NamedTuple`).

4. **`ClientRequest`** (`ClientRequest`, `aiohttp/client_reqrep.py:954-1434`) extends `ClientRequestBase`. It calls `_update_auto_headers`, `_update_body`, `_update_body_from_data`, `_update_content_encoding`, `_update_cookies`, `_update_expect_continue`, `_update_proxy`, `_update_transfer_encoding`.

5. **`ClientRequestArgs`** (`ClientRequestArgs`, `aiohttp/client_reqrep.py:930-951`) extends `TypedDict`.

### HTTP Exception Hierarchy (Response-Related)

The web exceptions form a hierarchy rooted in `HTTPException`:

- **`HTTPError`** (`HTTPError`, `aiohttp/web_exceptions.py:172-173`) extends `HTTPException` — base for 400s and 500s.
  - **`HTTPClientError`** (inferred parent of `HTTPBadRequest`) for 4xx errors.
    - **`HTTPBadRequest`** (`HTTPBadRequest`, `aiohttp/web_exceptions.py:288-289`) extends `HTTPClientError`, `status_code=400`.
    - **`HTTPMisdirectedRequest`** (`HTTPMisdirectedRequest`, `aiohttp/web_exceptions.py:394-395`) extends `HTTPClientError`, `status_code=421`.
    - **`HTTPRequestEntityTooLarge`** (`HTTPRequestEntityTooLarge`, `aiohttp/web_exceptions.py:366-375`) extends `HTTPClientError`, `status_code=413`.
  - **`HTTPServerError`** (inferred from children):
    - **`HTTPNotExtended`** (`HTTPNotExtended`, `aiohttp/web_exceptions.py:495-496`) extends `HTTPServerError`, `status_code=510`.
- **`HTTPRedirection`** (`HTTPRedirection`, `aiohttp/web_exceptions.py:176-177`) extends `HTTPException` — base for 300s.
- **`HTTPSuccessful`** (`HTTPSuccessful`, `aiohttp/web_exceptions.py:180-181`) extends `HTTPException` — base for 200s.

### Client Exception Hierarchy

- **`ClientError`** (`ClientError`, `aiohttp/client_exceptions.py:55-56`) extends `Exception` — base for client connection errors.
  - **`ClientResponseError`** (`ClientResponseError`, `aiohttp/client_exceptions.py:59-99`) extends `ClientError` — for errors after getting a response.
  - **`ClientConnectionError`** (`ClientConnectionError`, `aiohttp/client_exceptions.py:123-124`) extends `ClientError` — base for client socket errors.

### HTTP Parser Message Types

- **`RawRequestMessage`** (`RawRequestMessage`, `aiohttp/http_parser.py:99-111`) extends `NamedTuple`.
- **`RawResponseMessage`** (`RawResponseMessage`, `aiohttp/http_parser.py:112-123`) extends `NamedTuple`.

### Low-Level HTTP Exception Hierarchy

- **`HttpBadRequest`** (`HttpBadRequest`, `aiohttp/http_exceptions.py:55-57`) extends `BadHttpMessage`, with `code=400, message='Bad Request'`.
- **`PayloadEncodingError`** (`PayloadEncodingError`, `aiohttp/http_exceptions.py:60-61`) extends `BadHttpMessage`.

### Protocol and Runner Hierarchy

- **`BaseProtocol`** (`BaseProtocol`, `aiohttp/base_protocol.py:9-100`) extends `Protocol`.
- **`ResponseHandler`** (`ResponseHandler`, `aiohttp/client_proto.py:31-371`) extends `BaseProtocol`.
- **`BaseSite`** (`BaseSite`, `aiohttp/web_runner.py:47-78`) extends `ABC`.
- **`BaseRunner`** (`BaseRunner`, `aiohttp/web_runner.py:252-352`) extends `ABC`.

### Other Notable Types

- **`IOBasePayload`** (`IOBasePayload`, `aiohttp/payload.py:452-714`) extends `Payload`.
- **`DecompressionBaseHandler`** (`DecompressionBaseHandler`, `aiohttp/compression_utils.py:153-180`) extends `ABC`.
- **`_FileResponseResult`** (`_FileResponseResult`, `aiohttp/web_fileresponse.py:61-67`) extends `Enum`.
- **`CleanupError`** (`CleanupError`, `aiohttp/web_app.py:403-406`) extends `RuntimeError`.
- **`LookupError`** (`LookupError`, `aiohttp/payload.py:50-51`) extends `Exception`.

### Testing Protocol Types

- **`AiohttpClient`** (`AiohttpClient`, `aiohttp/pytest_plugin.py:31-48`) extends `Protocol`.
- **`AiohttpServer`** (`AiohttpServer`, `aiohttp/pytest_plugin.py:51-54`) extends `Protocol`.
- **`AiohttpRawServer`** (`AiohttpRawServer`, `aiohttp/pytest_plugin.py:57-64`) extends `Protocol`.

### Cannot Be Determined from Clue File

- The GAPS section lists `_BaseRequestContextManager`, `BaseConnector`, `ClientWebSocketResponse`, and `BaseKey` as uncovered — their positions in the hierarchy cannot be determined.
- The `HeadersMixin` and `CookieMixin` base classes used by `BaseRequest`, `ClientResponse`, and `StreamResponse` are not detailed in the FOCUS section.
- `ClientRequestBase` (parent of `ClientRequest`) is not described.
- `HTTPClientError` (parent of `HTTPBadRequest`, etc.) is not directly shown in the FOCUS entries but is inferred from child class declarations.
- `HTTPException` itself is not detailed.
