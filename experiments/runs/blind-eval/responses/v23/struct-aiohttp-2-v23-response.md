# v2.3 Response: struct-aiohttp-2
Date: 2026-04-15

## Summary

HTTP request and response processing in aiohttp is distributed across several modules. The core web application logic resides in `aiohttp/web_app.py`, `aiohttp/web_protocol.py`, `aiohttp/web_request.py`, `aiohttp/web_response.py`, `aiohttp/web_fileresponse.py`, `aiohttp/web_runner.py`, `aiohttp/web_server.py`, and `aiohttp/web_urldispatcher.py`. Client-side request/response processing lives in `aiohttp/client.py` and `aiohttp/client_reqrep.py`.

## Server-Side Request Processing Modules

### aiohttp/web_request.py — Request Objects
- Contains `BaseRequest` (FOCUS, L109-823), which extends `HeadersMixin`. Provides request data access methods including:
  - `read()` (SYM L624) — *"Read request body if present"*, called by `post`, `text`. Raises `HTTPRequestEntityTooLarge`.
  - `body_exists()` (FOCUS L612-614) — *"Return True if request has HTTP BODY"*.
  - `can_read_body()` (FOCUS L607-609) — *"Return True if request's HTTP BODY can be read"*.
  - `remote()` (FOCUS L408-420) — *"Remote IP of client initiated HTTP request"*.
  - `version()` (FOCUS L381-386) — *"Read only property for getting HTTP version of request"*.
  - `scheme()` (FOCUS L357-370) — Determines `https` or `http` based on `transport_sslcontext`.
  - `http_range()` (FOCUS L566-599) — *"The content of Range HTTP header"*, raises `ValueError`.
  - `if_modified_since()`, `if_unmodified_since()`, `if_range()` (FOCUS L479-546) — Conditional request headers, all delegate to `parse_http_date`.
  - `_etag_values()` (SYM L495) — *"Extract ETag objects from raw header"*.
  - `_if_match_or_none_impl()` (SYM L516) — ETag matching implementation.

### aiohttp/web_protocol.py — Connection/Protocol Handling
- Contains `RequestHandler` which manages the HTTP connection lifecycle:
  - `_handle_request()` (FOCUS L535-570) — Core request handling: calls `finish_response`, `handle_error`, `log_debug`. Called by `start`. Uses `Response` from `web_response`.
  - `handle_error()` (FOCUS L752-812) — *"Handle errors"*: branches based on request count and exception type. Calls `force_close`, `log_exception`. Called by `_handle_request`, `handler`, `_make_error_handler`. Raises `ConnectionError`. Uses `Response`.
  - `finish_response()` (FOCUS L711-750) — *"Prepare the response and write_eof, then log access"*. Calls `log_access`, `log_exception`. Uses `HTTPInternalServerError`, `Response`.
  - `close()` (SYM L481) — *"Close connection"*.
  - `force_close()` (SYM L491) — *"Forcefully close connection"*.
  - `log()` (SYM L98) — Async access logging.
  - `log_exception()` (SYM L515) — Exception logging.

### aiohttp/web_response.py — Response Objects
- `StreamResponse` (FOCUS L74-532) — Base response class extending `HeadersMixin, CookieMixin`. Calls `_generate_content_type_header`, `_prepare_headers`, `_set_status`, `_start_compression`, `_write_headers`, `drain`, `enable_compression`, `write`. Raises `RuntimeError`, `ValueError`, `TypeError`.
- `Response` (FOCUS L535-740) — Extends `StreamResponse`. Calls `write`. Called by `json_bytes_response`, `json_response`. Raises `RuntimeError`, `ValueError`, `TypeError`.
- `write()` (SYM L448) — Async function for writing response data.
- `last_modified()` (FOCUS L253-258) — Parses `Last-Modified` header.

### aiohttp/web_fileresponse.py — File Responses
- `FileResponse` (FOCUS L79-406) — *"A response object can be used to send files"*. Extends `StreamResponse`. Calls `_etag_match`, `_get_file_path_stat_encoding`, `_not_modified`, `_precondition_failed`, `_prepare_open_file`, `_sendfile`, `_sendfile_fallback`. Raises `ConnectionResetError`.
- `prepare()` (SYM L243) — Async function for preparing the file response.
- `_not_modified()` (SYM L150) — Handles 304 Not Modified responses.
- `_precondition_failed()` (SYM L161) — Handles 412 Precondition Failed.
- `_prepare_open_file()` (SYM L288) — Prepares an open file for sending.

### aiohttp/web_ws.py — WebSocket Responses
- `WebSocketResponse` (FOCUS L78-773) — Extends `StreamResponse`. Handles WebSocket upgrade, heartbeat, ping/pong, close, and frame sending. Raises `RuntimeError`, `HTTPBadRequest`, `ConnectionResetError`, `TypeError`.
- `_handle_ping_pong_exception()` (FOCUS L240-248) — Handles ping/pong exceptions.

## Core Web Application Logic

### aiohttp/web_app.py — Application Class
- `pre_freeze()` (SYM L212) — Prepares the application before freezing.
- `freeze()` (SYM L241) — Freezes the application configuration.
- `reg_handler()` (SYM L260) — Registers a handler.
- `CleanupError` (SYM L403) — Error class for cleanup failures.

### aiohttp/web_runner.py — Server Runner
- `AppRunner` (FOCUS L380-453) — *"Web Application runner"*. Calls `cleanup`. Raises `TypeError`.
- `stop()` (SYM L73) — Async function to stop the runner.

### aiohttp/web_server.py — Low-Level Server
- `_make_request()` (FOCUS L97-105) — Creates `BaseRequest` objects from raw HTTP messages. Delegates to `BaseRequest(message, payload, protocol, writer, task, self._loop)`.

### aiohttp/web_urldispatcher.py — URL Routing
- `_resolve_path_to_response()` (FOCUS L635-668) — *"Take the unresolved path and query the file system to form a response"*. Calls `_directory_as_html`. Raises `HTTPNotFound`, `HTTPForbidden`. Uses `FileResponse`, `Response`.
- `index_resource()` (SYM L1088) — *"Add a resource to the resource index"*.
- `_get_resource_index_key()` (SYM L1077) — *"Return a key to index the resource"*.

## Client-Side Request/Response Processing

### aiohttp/client.py — HTTP Client Session
- `request()` (FOCUS L464-468) — *"Perform HTTP request"*, delegates to `_RequestContextManager`.
- Convenience methods (FOCUS): `get()` L1334, `options()` L1344, `head()` L1354, `post()` L1364, `put()` L1372, `patch()` L1380, `delete()` L1388 — all delegate to `_RequestContextManager`.

### aiohttp/client_reqrep.py — Client Request/Response
- `ClientRequest` (not in this FOCUS but referenced) and `ClientResponse` (referenced).
- `start()` (FOCUS L427-474) — *"Start response processing"*. Raises `ClientResponseError`.
- `release()` (SYM L506) — Releases the connection.
- `_release_connection()` (SYM L542), `_cleanup_writer()` (SYM L563), `_notify_content()` (SYM L568) — Connection management methods.
- `__new__()` (SYM L111) — *"Create a new RequestInfo instance"*.

### aiohttp/client_proto.py — Client Protocol
- Handles connection-level protocol details: `abort`, `close`, `closed`, `connection_lost`, `data_received` (INDEX).
- `_drop_timeout()` (SYM L267), `_reschedule_timeout()` (SYM L272), `set_exception()` (SYM L204).

## Supporting Modules

### aiohttp/http_writer.py — HTTP Writing
- `write()` (SYM L167) — *"Writes chunk of data to a stream"*.
- `_write()` (SYM L94), `_writelines()` (SYM L105), `drain()` (SYM L353) — *"Flush the write buffer"*.
- `_send_headers_with_payload()` (SYM L131) — *"Send buffered headers with payload, coalescing..."*.
- `_write_chunked_payload()` (SYM L124) — *"Write a chunk with proper chunked encoding"*.

### aiohttp/multipart.py — Multipart Processing
- `from_response()` (FOCUS L688-699) — *"Constructs reader instance from HTTP response"*.
- Various reading methods: `read()` L304, `read_chunk()` L324, `readline()` L423, `decode_iter()` L524, `append()` L948, `append_payload()` L963.

### Middleware
- `DigestAuthMiddleware` (FOCUS L145-469) — Client-side digest auth.
- `LoggingMiddleware` (FOCUS, `examples/logging_middleware.py` L27-56 and `examples/combined_middleware.py` L38-63) — Request timing and status logging.
- Retry logic in `examples/retry_middleware.py` and `examples/combined_middleware.py`.

## Uncertainty / Limits

- The INDEX shows `...and 150 more modules` beyond the first 16 listed, so many modules (e.g., `aiohttp/web.py`, `aiohttp/cookiejar.py`, `aiohttp/compression_utils.py`) are not directly listed in the INDEX but are referenced in SYM/FOCUS entries.
- The `aiohttp/http_parser.py` module is referenced (e.g., `RawRequestMessage`) but not in the visible INDEX listing.
- The exact module for HTTP exception classes (`aiohttp/web_exceptions.py`, `aiohttp/http_exceptions.py`) is only visible through FOCUS entries like `HttpBadRequest` and `HTTPInternalServerError`.
