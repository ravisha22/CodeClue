# v2.4 Response: struct-aiohttp-2
Date: 2026-04-16

## Question
What modules handle HTTP request and response processing in aiohttp, and which files contain the core web application logic?

## Answer

### Core Web Application Logic

**`aiohttp/web_app.py`** — Contains the `Application` class, the central web application object. Key symbols include `pre_freeze` (line 212), `freeze` (line 241), `reg_handler` (line 260), and `CleanupError` (line 403) (`pre_freeze`, `freeze`, `reg_handler`, `CleanupError`, `aiohttp/web_app.py`, SYM/FOCUS).

**`aiohttp/web.py`** — Contains the top-level entry points:
- `run_app()` (`run_app`, `aiohttp/web.py:426-498`) — runs the application locally, calling `_cancel_tasks` and `_run_app`.
- `main()` (`main`, `aiohttp/web.py:501-565`) — CLI entry point that branches on `args.path` and `args.hostname`, calls `run_app`, and uses `ArgumentParser`.

### HTTP Request Processing

**`aiohttp/web_request.py`** — Server-side request handling. Key classes and methods:
- `BaseRequest` (`BaseRequest`, `aiohttp/web_request.py:109-823`) extends `HeadersMixin`. Provides `read()` (line 624, reads request body, raises `HTTPRequestEntityTooLarge`), `_etag_values()` (line 495), `_if_match_or_none_impl()` (line 516), `multipart()`, `text()`, and `get_extra_info()`. Uses `MultipartReader` from `multipart` and HTTP exceptions from `web_exceptions`.
- `body_exists()` (`body_exists`, `aiohttp/web_request.py:612-614`) — checks for HTTP body presence.
- `can_read_body()` (`can_read_body`, `aiohttp/web_request.py:607-609`) — checks if body is readable.
- `remote()` (`remote`, `aiohttp/web_request.py:408-420`) — remote IP of client.
- `version()` (`version`, `aiohttp/web_request.py:381-386`) — HTTP version property.
- `http_range()` (`http_range`, `aiohttp/web_request.py:566-599`) — parses Range header.

### HTTP Response Processing

**`aiohttp/web_response.py`** — Server-side response classes:
- `StreamResponse` (`StreamResponse`, `aiohttp/web_response.py:74-532`) extends `HeadersMixin, CookieMixin`. Provides streaming capabilities via `_generate_content_type_header`, `_prepare_headers`, `_set_status`, `_start_compression`, `_write_headers`, `drain`, `enable_compression`, `write` (line 448).
- `Response` (`Response`, `aiohttp/web_response.py:535-740`) extends `StreamResponse`. The standard response class, called by `json_bytes_response` and `json_response`.

**`aiohttp/web_fileresponse.py`** — File serving responses:
- `FileResponse` (`FileResponse`, `aiohttp/web_fileresponse.py:79-406`) extends `StreamResponse`. Described as "A response object can be used to send files." Calls `_etag_match`, `_get_file_path_stat_encoding`, `_not_modified` (line 150), `_precondition_failed` (line 161), `_prepare_open_file` (line 288), `_sendfile`, `_sendfile_fallback`. Has a `prepare()` async method (line 243).

**`aiohttp/web_ws.py`** — WebSocket response handling:
- `WebSocketResponse` (`WebSocketResponse`, `aiohttp/web_ws.py:78-773`) extends `StreamResponse`. Manages WebSocket connections with `_handshake` (lines 270-354, validates Upgrade/Connection headers, negotiates protocol and compression), `_handle_ping_pong_exception` (lines 240-248, sets closed state on exceptions), `_cancel_heartbeat`, `_close_transport`, `send_frame` (line 452), `close` (line 508).
- `WebSocketReady` (`WebSocketReady`, `aiohttp/web_ws.py:70-75`) — a dataclass-like with `ok` and `protocol` fields.

### HTTP Protocol Handler

**`aiohttp/web_protocol.py`** — The HTTP protocol implementation:
- `RequestHandler` (`RequestHandler`, `aiohttp/web_protocol.py:119-822`) extends `BaseProtocol`. This is the core HTTP protocol handler that calls `log`, `AccessLoggerWrapper`, `_handle_request`, `_make_error_handler`, `close` (line 481), `connection_lost`, `connection_made`, `finish_response`. Uses `Response`, `HTTPInternalServerError`, `StreamWriter`.
- `_handle_request()` (`_handle_request`, `aiohttp/web_protocol.py:535-570`) — The source snippet shows it dispatches to `request_handler(request)`, catches `HTTPException` (converts to `Response`), `asyncio.TimeoutError` (returns 504 via `handle_error`), and general `Exception` (returns 500 via `handle_error`). In all paths, it calls `finish_response`.
- `finish_response()` (`finish_response`, `aiohttp/web_protocol.py:711-750`) — Prepares the response and writes EOF. Validates the handler returned a proper response (logs error and creates `HTTPInternalServerError` if not). Handles `ConnectionError` for premature disconnects.
- `handle_error()` (`handle_error`, `aiohttp/web_protocol.py:752-812`) — Error response construction, calls `force_close` and `log_exception`.
- `log()` (line 98), `log_exception()` (line 515), `log_debug()` — Logging methods.
- `force_close()` (line 491) — Forcefully closes the connection.

### HTTP Writing

**`aiohttp/http_writer.py`** — Low-level HTTP write operations:
- `write()` (line 167) — writes chunk of data to a stream.
- `_write()` (line 94), `_writelines()` (line 105) — internal write methods.
- `_write_chunked_payload()` (line 124) — chunked transfer encoding.
- `_send_headers_with_payload()` (line 131) — coalesces headers with payload.
- `drain()` (line 353) — flushes the write buffer.

### Web Server Module

**`aiohttp/web_server.py`** — Server factory:
- `Server` (`Server`, `aiohttp/web_server.py:30-126`) — creates request handlers, calls `shutdown`.
- `_make_request()` (`_make_request`, `aiohttp/web_server.py:97-105`) — creates `BaseRequest` instances from raw messages. The source snippet shows it constructs `BaseRequest(message, payload, protocol, writer, task, self._loop)`.
- `pre_shutdown()` (`pre_shutdown`, `aiohttp/web_server.py:107-109`) — iterates over connections during pre-shutdown.
- `shutdown()` (`shutdown`, `aiohttp/web_server.py:111-114`) — shuts down the server.

### Runner Infrastructure

**`aiohttp/web_runner.py`** — Server lifecycle management:
- `BaseRunner` (`BaseRunner`, `aiohttp/web_runner.py:252-352`) extends `ABC`. Manages setup, shutdown, cleanup, and site registration. The source snippet shows `cleanup()` stops all sites sequentially (intentionally not via `gather()`), then calls `pre_shutdown`, `shutdown`, `_cleanup_server`, and resets state.
- `AppRunner` (`AppRunner`, `aiohttp/web_runner.py:380-453`) — The application runner. Its `_make_server()` freezes `on_startup`, awaits `app.startup()`, freezes the app, then creates `Server` with `self._app._handle`. Its `_cleanup_server()` calls `await self._app.cleanup()`.
- `ServerRunner` (`ServerRunner`, `aiohttp/web_runner.py:355-377`) — Low-level runner with no-op `shutdown()` and `_cleanup_server()`.
- `BaseSite` (`BaseSite`, `aiohttp/web_runner.py:47-78`) — Abstract site class managing socket binding. `stop()` closes the server and unregisters the site.
- `SockSite`, `NamedPipeSite` — Concrete site types.
- `GracefulExit` (`GracefulExit`, `aiohttp/web_runner.py:39-40`) — extends `SystemExit` for graceful shutdown signaling.

### URL Routing

**`aiohttp/web_urldispatcher.py`** — URL dispatch and routing:
- `UrlDispatcher` (referenced via `_get_resource_index_key` at line 1077, `index_resource` at line 1088, `_quote_path` at line 1230) (`SYM`).

### Client-Side Request/Response

**`aiohttp/client.py`** (1654L) — Client session with HTTP methods: `request()` (line 464), `get()` (line 1334), `post()` (line 1364), `put()` (line 1372), `delete()` (line 1388), `head()` (line 1354), `options()` (line 1344), `patch()` (line 1380). All delegate to `_RequestContextManager` (`client.py`, FOCUS).

**`aiohttp/client_reqrep.py`** — Client request and response objects. Contains `start()` (line 427) for response processing.

**`aiohttp/client_ws.py`** — Client WebSocket response: `ClientWebSocketResponse` (`ClientWebSocketResponse`, `aiohttp/client_ws.py:60-560`).

### Supporting Modules

- **`aiohttp/base_protocol.py`** (100L) — `BaseProtocol` extends `Protocol`, providing `connected`, `connection_lost`, `connection_made`, `pause_reading`, `pause_writing` (`INDEX`).
- **`aiohttp/abc.py`** (266L) — Abstract interfaces like `AbstractAccessLogger` (`INDEX`).
- **`aiohttp/helpers.py`** — Utilities: `BasicAuth`, content type parsing (`SYM`).
- **`aiohttp/multipart.py`** — Multipart body handling (`SYM`).
- **`aiohttp/payload.py`** — Payload type registry (`SYM`).
- **`aiohttp/streams.py`** — `AsyncStreamIterator` at line 32 (`SYM`).

### Cannot Be Determined from Clue File

- The GAPS section lists `TraceRequestHeadersSentParams`, `TraceRequestRedirectParams`, `TraceRequestStartParams`, `TraceResponseChunkReceivedParams` as uncovered — the request/response tracing infrastructure is not detailed.
- The INDEX is truncated (`...and 150 more modules`), so some modules are not enumerated.
- The full middleware dispatch pipeline within `Application._handle` is not shown.
- `aiohttp/web_exceptions.py` is referenced by many classes but its full contents are not in the INDEX or FOCUS.
