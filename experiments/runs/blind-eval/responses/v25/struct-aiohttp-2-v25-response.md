# v2.5 Response: struct-aiohttp-2
Date: 2026-04-16

## Question
What modules handle HTTP request and response processing in aiohttp, and which files contain the core web application logic?

## Answer

### Core Web Application Logic

**`aiohttp/web_app.py`** — Contains the `Application` class (FOCUS: `Application` at `aiohttp/web_app.py:71-400`), the central web application object. It calls `_add_subapp`, `_check_frozen`, `_prepare_middleware`, `handler`, `reg_handler`, `_reg_subapp_signals`, `add_routes`, and `freeze`. It also defines `CleanupError` (SYM: `aiohttp/web_app.py:403`). The `_handle` method (FOCUS: `_handle` at `aiohttp/web_app.py:366-390`) dispatches requests by calling `handler`, `freeze`, and `_build_middlewares`. The `pre_freeze` and `freeze` methods (SYM: `aiohttp/web_app.py:212` and `:241`) manage the application lifecycle.

**`aiohttp/web.py`** — Provides the `main` entry point (FOCUS: `main` at `aiohttp/web.py:501-565`) which calls `run_app` (FOCUS: `run_app` at `aiohttp/web.py:426-498`). `run_app` calls `_cancel_tasks` and `_run_app` to start the server.

### HTTP Request Processing

**`aiohttp/web_request.py`** — Defines the request hierarchy:

- `BaseRequest` (FOCUS: `BaseRequest` at `aiohttp/web_request.py:109-823`) extends `HeadersMixin`. It calls `_etag_values`, `_if_match_or_none_impl`, `get_extra_info`, `multipart`, `read`, `text`, and `FileField`. It raises `HTTPRequestEntityTooLarge` and `HTTPUnsupportedMediaType` for payload limits and content-type validation. Key methods include `read` (SYM: `:624`, "Read request body if present"), `http_range` (FOCUS: `:566-599`), and `_etag_values` (SYM: `:495`).
- `Request` (FOCUS: `Request` at `aiohttp/web_request.py:826-884`) extends `BaseRequest`, adding match info capabilities.

**`aiohttp/web_server.py`** — Contains `_make_request` (FOCUS: `_make_request` at `aiohttp/web_server.py:97-105`) which delegates to `BaseRequest` to create request objects from raw HTTP messages. The source snippet confirms it instantiates `BaseRequest(message, payload, protocol, writer, task, self._loop)`.

### HTTP Response Processing

**`aiohttp/web_response.py`** — Defines the response hierarchy:

- `StreamResponse` (FOCUS: `StreamResponse` at `aiohttp/web_response.py:74-532`) extends `HeadersMixin` and `CookieMixin`. Calls `_generate_content_type_header`, `_prepare_headers`, `_set_status`, `_start_compression`, `_write_headers`, `drain`, `enable_compression`, and `write`.
- `Response` (FOCUS: `Response` at `aiohttp/web_response.py:535-740`) extends `StreamResponse`. Called by `json_bytes_response` and `json_response`. The `write` method (SYM: `:448`) is an async function.

**`aiohttp/web_fileresponse.py`** — Defines `FileResponse` (FOCUS: `FileResponse` at `aiohttp/web_fileresponse.py:79-406`) extending `StreamResponse`. Handles static file serving with methods `prepare` (SYM: `:243`), `_not_modified`, `_precondition_failed`, `_prepare_open_file`, `_make_response` (FOCUS: `:168-222`), and `_resolve_path_to_response` (FOCUS: `aiohttp/web_urldispatcher.py:635-668`) which uses `FileResponse`.

**`aiohttp/web_ws.py`** — Defines `WebSocketResponse` (FOCUS: `:78-773`) extending `StreamResponse` for WebSocket connections.

### HTTP Protocol Handling

**`aiohttp/web_protocol.py`** — Contains `RequestHandler` (FOCUS: `RequestHandler` at `aiohttp/web_protocol.py:119-822`) extending `BaseProtocol`. This is the HTTP protocol implementation. Key methods:

- `_handle_request` (FOCUS: `:535-570`) — Dispatches to the request handler, catches `HTTPException` (converting to `Response`), `TimeoutError` (504), and generic exceptions (500 via `handle_error`). The source snippet shows it calls `finish_response` in all paths.
- `finish_response` (FOCUS: `:711-750`) — Calls `resp.prepare(request)` then `resp.write_eof()`, handles `ConnectionError` gracefully. If the handler returns `None` or a non-response, it logs an exception and creates an `HTTPInternalServerError` response (source snippet confirms).
- `handle_error` (FOCUS: `:752-812`) — Creates error responses, calls `force_close` and `log_exception`.
- `log` (SYM: `:98`), `close` (SYM: `:481`), `force_close` (SYM: `:491`).

### HTTP Parsing

**`aiohttp/http_parser.py`** — Contains:
- `HttpRequestParser` (FOCUS: `:573-676`) — Parses request status lines, produces `RawRequestMessage` (FOCUS: `:99-111`, extends `NamedTuple`).
- `HttpResponseParser` (FOCUS: `:677-760`) — Parses response status lines, produces `RawResponseMessage` (FOCUS: `:112-123`, extends `NamedTuple`).

**`aiohttp/http_writer.py`** — Low-level HTTP writing: `write` (SYM: `:167`), `_write` (SYM: `:94`), `_writelines` (SYM: `:105`), `_write_chunked_payload` (SYM: `:124`), `_send_headers_with_payload` (SYM: `:131`), `drain` (SYM: `:353`).

### HTTP Exceptions

**`aiohttp/http_exceptions.py`** — `HttpProcessingError` (FOCUS: `:10-41`, extends `Exception`) and `HttpBadRequest` (FOCUS: `:55-57`, extends `BadHttpMessage`, code=400).

**`aiohttp/web_exceptions.py`** — `HTTPBadRequest` (FOCUS: `:288-289`, extends `HTTPClientError`, status_code=400), `HTTPMisdirectedRequest` (`:394-395`, status_code=421), `HTTPInternalServerError` (FOCUS: `:463-464`, extends `HTTPServerError`, status_code=500).

### URL Routing

**`aiohttp/web_urldispatcher.py`** — URL dispatch and routing: `_resolve_path_to_response` (FOCUS: `:635-668`), `_handle` (FOCUS: `:623-633`), `index_resource` (SYM: `:1088`), `_get_resource_index_key` (SYM: `:1077`), `_quote_path` (SYM: `:1230`).

### What Cannot Be Determined

Per GAPS: "uncovered: ClientHttpProxyError, ClientRequestArgs, ClientResponseError, GunicornUVLoopWebWorker." The full internal details of the HTTP parser C extensions, and the complete middleware chain execution path are not fully covered by this clue. The drill-down snippets for `_handle_request` and `_handle_ping_pong_exception` have been provided as source and analyzed above.
