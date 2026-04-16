# v2.4.1 Response: struct-aiohttp-2
Date: 2026-04-16

## Modules Handling HTTP Request/Response Processing and Core Web Application Logic

### Request Processing Modules

**`aiohttp/web_request.py`** -- The primary request module. Contains `BaseRequest` (extended by `Request`) with methods for body access (`read`, `aiohttp/web_request.py:624`; `body_exists`, `aiohttp/web_request.py:612-614`; `can_read_body`, `aiohttp/web_request.py:607-609`), content introspection (`content` returns `StreamReader`, drill-down `aiohttp/web_request.py:661-663`), cookies (`cookies`, drill-down `aiohttp/web_request.py:668-677`), ETag handling (`_etag_values`, `aiohttp/web_request.py:495-513`; `_if_match_or_none_impl`, `aiohttp/web_request.py:516-522`), client IP resolution (`remote`, drill-down `aiohttp/web_request.py:408-420`), HTTP range parsing (`http_range`, `aiohttp/web_request.py:566-599`), Forwarded header parsing (`forwarded`, drill-down `aiohttp/web_request.py:296-354`), multipart cleanup (`_finish`, drill-down `aiohttp/web_request.py:813-823`), and request cloning (`clone`, drill-down `aiohttp/web_request.py:830-852`). The `client_max_size` property exposes the configured payload limit (`client_max_size`, drill-down `aiohttp/web_request.py:252-253`).

**`aiohttp/web_protocol.py`** -- The HTTP protocol handler containing `RequestHandler` (`RequestHandler`, `aiohttp/web_protocol.py:119-822`, `extends: BaseProtocol`). It orchestrates request dispatch via `_handle_request()` (drill-down `aiohttp/web_protocol.py:535-570`), which invokes the request handler, catches `HTTPException` (converting to `Response`), `TimeoutError` (returning 504), and general `Exception` (returning 500 via `handle_error`). `finish_response()` (drill-down `aiohttp/web_protocol.py:711-750`) prepares and writes the response, handles missing return statements, and logs access. Other functions include `close`/`force_close` (`close`, `aiohttp/web_protocol.py:481`; `force_close`, `aiohttp/web_protocol.py:491`), `log`/`log_exception`/`log_debug` (`log`, `aiohttp/web_protocol.py:98`; `log_debug`, drill-down `aiohttp/web_protocol.py:511-513`), and `handle_error` (`handle_error`, `aiohttp/web_protocol.py:752-812`).

### Response Processing Modules

**`aiohttp/web_response.py`** -- Contains `StreamResponse` (extends `HeadersMixin, CookieMixin`) and `Response` (extends `StreamResponse`) (`Response`, `aiohttp/web_response.py:535-740`). The `write` async function sends data (`write`, `aiohttp/web_response.py:448`). The `body` setter (drill-down `aiohttp/web_response.py:610-633`) accepts `bytes`, `bytearray`, or payload-registry-resolved objects, setting Content-Type from payload headers. The `text` setter (drill-down `aiohttp/web_response.py:645-654`) encodes string data, defaulting to `text/plain; charset=utf-8`.

**`aiohttp/web_fileresponse.py`** -- `FileResponse` (extends `StreamResponse`) for serving files (`FileResponse`, `aiohttp/web_fileresponse.py:79-406`). Includes `prepare`, `_not_modified`, `_precondition_failed`, `_prepare_open_file`, `_sendfile`, and `_sendfile_fallback`.

**`aiohttp/http_writer.py`** -- Low-level HTTP writing: `write` for data chunks (`write`, `aiohttp/http_writer.py:167`), `_write`/`_writelines` for transport-level operations, `_write_chunked_payload` for chunked encoding (`aiohttp/http_writer.py:124`), `_send_headers_with_payload` for coalescing headers with body (`aiohttp/http_writer.py:131`), and `drain` for flushing (`drain`, `aiohttp/http_writer.py:353`).

### Core Web Application Logic

**`aiohttp/web_app.py`** -- The `Application` class (`Application`, `aiohttp/web_app.py:71-400`) is the central web application object. It manages lifecycle signals, app freezing (`pre_freeze`, `aiohttp/web_app.py:212`; `freeze`, `aiohttp/web_app.py:241`), handler registration (`reg_handler`, `aiohttp/web_app.py:260`), middleware preparation (`_prepare_middleware`), sub-application mounting (`_add_subapp`), and route management (`add_routes`). `CleanupError` (extends `RuntimeError`) handles cleanup failures (`CleanupError`, `aiohttp/web_app.py:403`).

**`aiohttp/web_runner.py`** -- Server runner infrastructure. `BaseRunner` manages sites and server lifecycle (`stop`, `aiohttp/web_runner.py:73`). `AppRunner` (extends `BaseRunner`) wraps an `Application` (`AppRunner`, `aiohttp/web_runner.py:380-453`).

**`aiohttp/web.py`** -- Top-level entry: `run_app()` for running locally; `main()` CLI entry point parsing args and calling `run_app` (`main`, `aiohttp/web.py:501-565`).

**`aiohttp/web_server.py`** -- The `Server` class that creates `RequestHandler` instances (`_make_request`, drill-down `aiohttp/web_server.py:97-105`).

### URL Routing

**`aiohttp/web_urldispatcher.py`** -- URL dispatch with `AbstractResource`, `AbstractRoute`, `Domain`, `MaskDomain`, `_resolve_path_to_response` (`_resolve_path_to_response`, `aiohttp/web_urldispatcher.py:635-668`; resolves paths, raises `HTTPNotFound`/`HTTPForbidden`, returns `FileResponse`), and `_handle` (`_handle`, `aiohttp/web_urldispatcher.py:623-633`).

### WebSocket Processing

- **`aiohttp/web_ws.py`** -- Server-side `WebSocketResponse` (`WebSocketResponse`, `aiohttp/web_ws.py:78-773`, `extends: StreamResponse`). Handles ping/pong exceptions (drill-down `aiohttp/web_ws.py:240-248`), heartbeat management, and connection cancellation (`_cancel`, drill-down `aiohttp/web_ws.py:766-773`).
- **`aiohttp/client_ws.py`** -- Client-side `ClientWebSocketResponse` (`ClientWebSocketResponse`, `aiohttp/client_ws.py:60-560`) with similar heartbeat and close logic.

### Client-Side Request/Response

- **`aiohttp/client.py`** -- `ClientSession` with HTTP verb methods: `get`, `post`, `put`, `delete`, `head`, `options`, `patch` (all delegate to `_RequestContextManager`) (`get`, `aiohttp/client.py:1334-1342`; `request`, `aiohttp/client.py:464-468`).
- **`aiohttp/client_reqrep.py`** -- `ClientRequest`/`ClientResponse`; response processing via `start()` (`start`, `aiohttp/client_reqrep.py:427-474`).

### Supporting Modules

- **`aiohttp/web_exceptions.py`** -- HTTP exception hierarchy: `HTTPInternalServerError` (status 500) used by `finish_response` and `handle_error` (`HTTPInternalServerError`, `aiohttp/web_exceptions.py:463-464`).
- **`aiohttp/multipart.py`** -- Multipart reading/writing (`from_response`, `aiohttp/multipart.py:688-699`).
- **`aiohttp/base_protocol.py`** -- Base protocol for connection management (`INDEX: aiohttp/base_protocol.py 100L`).

### What Cannot Be Determined

- Full contents of uncovered symbols: `RequestPayloadError`, `ClientRequestBase`, `ResponseHandler`, `MultipartResponseWrapper` (GAPS section).
- The internal middleware chain execution within `Application._handle`.
- Full details of `aiohttp/client_proto.py`'s protocol state machine.
