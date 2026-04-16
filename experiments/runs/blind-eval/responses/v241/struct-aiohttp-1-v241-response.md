# v2.4.1 Response: struct-aiohttp-1
Date: 2026-04-16

## Main Packages, Modules, and Directory Organization

### Top-Level Directory Structure

The project is organized into six top-level directories plus a root `setup.py` (TREE section):

| Directory | Contents |
|-----------|----------|
| `aiohttp/` | 54 source files -- the core library (`TREE: aiohttp/ (54 files)`) |
| `aiohttp/_websocket/` | WebSocket sub-package (`TREE: _websocket/`) |
| `docs/` | 2 files, with a `code/` subdirectory (`TREE: docs/ (2 files), code/`) |
| `examples/` | 23 example scripts (`TREE: examples/ (23 files)`) |
| `requirements/` | 1 dependency file (`TREE: requirements/ (1 files)`) |
| `tests/` | 80 test files, with `autobahn/` and `isolated/` subdirectories (`TREE: tests/ (80 files)`) |
| `tools/` | 5 utility scripts (`TREE: tools/ (5 files)`) |

### Core `aiohttp/` Package -- Key Modules

**Web Application & Server:**
- `aiohttp/web_app.py` -- Application class with lifecycle (`pre_freeze`, `freeze`, `reg_handler`, `CleanupError`; `Application`, `aiohttp/web_app.py:71-400`)
- `aiohttp/web.py` -- Entry point with `main()` and `run_app()` (`main`, `aiohttp/web.py:501-565`; `run_app`, `aiohttp/web.py:426-498`)
- `aiohttp/web_runner.py` -- Server runner/site management (`stop`, `aiohttp/web_runner.py:73`)

**Request/Response:**
- `aiohttp/web_request.py` -- Request handling: `read()`, `_etag_values()`, `_if_match_or_none_impl()` (`read`, `aiohttp/web_request.py:624`)
- `aiohttp/web_response.py` -- Response writing (`write`, `aiohttp/web_response.py:448`)
- `aiohttp/web_fileresponse.py` -- File responses with `prepare`, `_not_modified`, `_precondition_failed`, `_prepare_open_file` (`prepare`, `aiohttp/web_fileresponse.py:243`)
- `aiohttp/web_protocol.py` -- HTTP protocol handler: `close`, `force_close`, `log`, `log_exception`, `handle_error` (`close`, `aiohttp/web_protocol.py:481`)

**URL Routing:**
- `aiohttp/web_urldispatcher.py` -- URL dispatch with `Domain`, `MaskDomain`, `AbstractResource`, `AbstractRoute`, `index_resource`, `_quote_path` (`Domain`, `aiohttp/web_urldispatcher.py:766-803`; `AbstractResource`, `aiohttp/web_urldispatcher.py:101-145`)

**Client:**
- `aiohttp/client.py` -- 1654 lines, the main client module (`INDEX: aiohttp/client.py 1654L`)
- `aiohttp/client_reqrep.py` -- Request/response representations: `release`, `_release_connection`, `_cleanup_writer` (`release`, `aiohttp/client_reqrep.py:506`)
- `aiohttp/client_exceptions.py` -- Exception hierarchy: `ClientConnectionError`, `ClientConnectionResetError` (`INDEX: aiohttp/client_exceptions.py 388L`)
- `aiohttp/client_middlewares.py` -- Middleware composition: `build_client_middlewares`, `single_middleware_handler` (`INDEX: aiohttp/client_middlewares.py 55L`)
- `aiohttp/client_middleware_digest_auth.py` -- Digest auth middleware (`DigestAuthMiddleware`, `aiohttp/client_middleware_digest_auth.py:145-469`)
- `aiohttp/client_proto.py` -- Client protocol: `abort`, `close`, `data_received`, `_drop_timeout`, `_reschedule_timeout` (`INDEX: aiohttp/client_proto.py 371L`)

**Data Handling:**
- `aiohttp/multipart.py` -- Multipart reading/writing: `BodyPartReader`, `MultipartReader`, `MultipartWriter`, `append`, `append_payload`, `read`, `readline`, `read_chunk` (`append`, `aiohttp/multipart.py:948`)
- `aiohttp/payload.py` -- Payload registry and types: `LookupError`, `get`, `register` (`LookupError`, `aiohttp/payload.py:50`)
- `aiohttp/formdata.py` -- Form data building: `add_field` (`add_field`, `aiohttp/formdata.py:48`)
- `aiohttp/streams.py` -- Async stream primitives: `AsyncStreamIterator` (`AsyncStreamIterator`, `aiohttp/streams.py:32`)

**HTTP Internals:**
- `aiohttp/http_writer.py` -- Low-level writing: `write`, `_write`, `_writelines`, `_write_chunked_payload`, `_send_headers_with_payload`, `drain` (`write`, `aiohttp/http_writer.py:167`)
- `aiohttp/base_protocol.py` -- Base protocol: `connected`, `connection_lost`, `connection_made`, `pause_reading` (`INDEX: aiohttp/base_protocol.py 100L`)

**Helpers & Utilities:**
- `aiohttp/helpers.py` -- `BasicAuth`, `basicauth_from_netrc`, `proxies_from_env`, `get_content_type`, `parse_content_type` (`BasicAuth`, `aiohttp/helpers.py:121`)
- `aiohttp/abc.py` -- Abstract base classes: `AbstractAccessLogger`, `AbstractAsyncAccessLogger`, `AbstractCookieJar`, `AbstractMatchInfo`, `AbstractResolver` (`AbstractCookieJar`, `aiohttp/abc.py:153-187`)
- `aiohttp/cookiejar.py` -- Cookie handling: `_is_domain_match`, `clear_domain` (`_is_domain_match`, `aiohttp/cookiejar.py:470-483`)
- `aiohttp/_cookie_helpers.py` -- Cookie parsing: `parse_cookie_header`, `parse_set_cookie_headers` (`INDEX: aiohttp/_cookie_helpers.py 339L`)

**WebSocket Sub-Package** (`aiohttp/_websocket/`):
- `writer.py` -- `WebSocketWriter`, `send_frame`, `close`, `_write_websocket_frame` (`WebSocketWriter focus`)
- `reader_c.py` / `reader_py.py` -- Two reader implementations (C/Python): `feed_data`, `feed_eof`, `read` (`INDEX: aiohttp/_websocket/reader_c.py 499L`)
- `models.py` -- `WSCloseCode`, `WSHandshakeError`, `WSMessageBinary`, `WSMessageClose` (`INDEX: aiohttp/_websocket/models.py 167L`)
- `helpers.py` -- `ws_ext_gen`, `ws_ext_parse` (`INDEX: aiohttp/_websocket/helpers.py 148L`)

**Server-Side WebSocket:**
- `aiohttp/web_ws.py` -- `WebSocketResponse` with heartbeat, close, send_frame (`close`, `aiohttp/web_ws.py:508`)
- `aiohttp/client_ws.py` -- Client WebSocket: `close`, `send_frame`, `_cancel_heartbeat` (`close`, `aiohttp/client_ws.py:320`)

**Testing Support:**
- `aiohttp/pytest_plugin.py` -- Pytest fixtures: `AiohttpClient`, `AiohttpServer`, `AiohttpRawServer`, `aiohttp_client`, `aiohttp_server`, `aiohttp_raw_server` (`AiohttpClient`, `aiohttp/pytest_plugin.py:31-48`)

**Worker:**
- `aiohttp/worker.py` -- Gunicorn worker: `_notify_waiter_done` (`_notify_waiter_done`, `aiohttp/worker.py:140`)

### Other Directories

- **`examples/`** -- 23 example scripts demonstrating middleware patterns (basic auth, digest auth, retry, logging, token refresh, combined middleware), fake servers, and WebSocket usage (`main`, `examples/basic_auth_middleware.py:179-186`; `main`, `examples/digest_auth_qop_auth.py:34-64`)
- **`tools/`** -- 5 utility scripts: benchmarking (`bench-asyncio-write.py`), changelog management (`check_changes.py`, `check_sum.py`, `cleanup_changes.py`) (`main`, `tools/bench-asyncio-write.py:97-126`)
- **`docs/code/`** -- Documentation code samples, e.g., `SSRFError` (`SSRFError`, `docs/code/client_middleware_cookbook.py:21`)
- **`tests/`** -- 80 test files with `autobahn/` (WebSocket conformance) and `isolated/` subdirectories (`TREE: tests/ (80 files)`)

### What Cannot Be Determined

- The full list of all 54 `aiohttp/` modules (INDEX is truncated at ~16 entries with "...and 150 more modules").
- The full symbol table (truncated at ~78 entries with "...and 1859 more symbols").
- Contents of `aiohttp/__init__.py` -- the public API surface and re-exports (258 lines but no symbols listed).
- Modules listed as uncovered in GAPS: `LoggingMiddleware`, `RetryMiddleware`.
