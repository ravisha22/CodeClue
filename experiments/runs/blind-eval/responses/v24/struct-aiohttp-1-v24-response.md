# v2.4 Response: struct-aiohttp-1
Date: 2026-04-16

## Question
What are the main packages and modules in the aiohttp codebase, and how is the project organized into directories?

## Answer

### Top-Level Directory Structure

The project root contains the following directories and files (TREE section):

- **`aiohttp/`** — Main package with **54 files**, containing a sub-package `_websocket/`.
- **`docs/`** — Documentation with **2 files** and a `code/` subdirectory.
- **`examples/`** — Example scripts with **23 files**.
- **`requirements/`** — Dependency specifications with **1 file**.
- **`tests/`** — Test suite with **80 files**, including `autobahn/` and `isolated/` subdirectories.
- **`tools/`** — Utility scripts with **5 files**.
- **`setup.py`** — Package installation script at the root.

### Core `aiohttp/` Package Modules

The INDEX section reveals the following module organization within `aiohttp/`:

**Package initialization:**
- `aiohttp/__init__.py` (258L) — Main package init, exports public API.

**Client-side modules:**
- `aiohttp/client.py` (1654L) — HTTP client, exports `auth`, `auto_decompress`, `close`, `closed`, `connector` (`client.py`, INDEX).
- `aiohttp/client_exceptions.py` (388L) — Client exception classes: `ClientConnectionError`, `ClientConnectionResetError`, etc. (`client_exceptions.py`, INDEX).
- `aiohttp/client_proto.py` (371L) — Client protocol handling: `abort`, `close`, `closed`, `connection_lost`, `data_received` (`client_proto.py`, INDEX).
- `aiohttp/client_middlewares.py` (55L) — Client middleware infrastructure: `wrapped`, `make_wrapper`, `single_middleware_handler`, `build_client_middlewares` (`client_middlewares.py`, INDEX).
- `aiohttp/client_middleware_digest_auth.py` (469L) — Digest authentication middleware: `DigestAuthChallenge`, `H`, `KD`, `DigestAuthMiddleware`, `escape_quotes` (`client_middleware_digest_auth.py`, INDEX).

**Web server modules (inferred from SYM and FOCUS):**
- `aiohttp/web_app.py` — Application class, lifecycle (`pre_freeze` at line 212, `freeze` at line 241, `reg_handler` at line 260, `CleanupError` at line 403) (`web_app.py`, SYM).
- `aiohttp/web_request.py` — Request handling (`_etag_values` at line 495, `_if_match_or_none_impl` at line 516, `read` at line 624) (`web_request.py`, SYM).
- `aiohttp/web_response.py` — Response classes (`write` at line 448) (`web_response.py`, SYM).
- `aiohttp/web_ws.py` — WebSocket support (`close` at line 508, `_close_transport` at line 574, `send_frame` at line 452, `_cancel_heartbeat` at line 129) (`web_ws.py`, SYM).
- `aiohttp/web_protocol.py` — HTTP protocol handler (`close` at line 481, `force_close` at line 491, `log` at line 98, `log_exception` at line 515, `handle_error` at line 752) (`web_protocol.py`, SYM).
- `aiohttp/web_fileresponse.py` — File response serving (`prepare` at line 243, `_not_modified` at line 150, `_precondition_failed` at line 161, `_prepare_open_file` at line 288) (`web_fileresponse.py`, SYM).
- `aiohttp/web_urldispatcher.py` — URL routing and dispatch (`_get_resource_index_key` at line 1077, `index_resource` at line 1088, `_quote_path` at line 1230) (`web_urldispatcher.py`, SYM).
- `aiohttp/web_runner.py` — Server runners and sites (`stop` at line 73) (`web_runner.py`, SYM).
- `aiohttp/web.py` — Entry point, contains `main` function (`main`, `aiohttp/web.py:501-565`) and `run_app` (`run_app`, `aiohttp/web.py:426-498`) (FOCUS section).

**HTTP parsing and writing:**
- `aiohttp/http_writer.py` — HTTP write operations: `write` at line 167, `_writelines` at line 105, `_write` at line 94, `drain` at line 353, `_send_headers_with_payload` at line 131, `_write_chunked_payload` at line 124 (`http_writer.py`, SYM).

**Data handling modules:**
- `aiohttp/multipart.py` — Multipart body handling: `append` at line 948, `append_payload` at line 963, `read` at line 304, `readline` at line 423, `read_chunk` at line 324, `decode_iter` at line 524 (`multipart.py`, SYM).
- `aiohttp/payload.py` — Payload registry and types: `LookupError` at line 50, `get` at line 98, `register` at line 121, `_set_or_restore_start_position` at line 470 (`payload.py`, SYM).
- `aiohttp/formdata.py` — Form data building: `add_field` at line 48 (`formdata.py`, SYM).
- `aiohttp/helpers.py` — Utilities: `BasicAuth` at line 121, `decode` at line 139, `encode` at line 178, `get_content_type` at line 367, `parse_content_type` at line 387, `_parse_content_type` at line 760 (`helpers.py`, SYM/FOCUS).
- `aiohttp/streams.py` — Async stream primitives: `AsyncStreamIterator` at line 32 (`streams.py`, SYM).
- `aiohttp/compression_utils.py` — Compression handling (referenced in FOCUS via `DecompressionBaseHandler`).
- `aiohttp/connector.py` — Connection pooling: `_available_connections` at line 528, `_release_waiter` at line 720 (`connector.py`, SYM).
- `aiohttp/_cookie_helpers.py` (339L) — Cookie parsing: `parse_cookie_header`, `parse_set_cookie_headers`, `preserve_morsel_with_coded_value` (`_cookie_helpers.py`, INDEX).
- `aiohttp/cookiejar.py` — Cookie storage (referenced in FOCUS via `_is_domain_match` at line 470).

**Abstract base classes:**
- `aiohttp/abc.py` (266L) — Abstract interfaces: `AbstractAccessLogger`, `enabled`, `log` (`abc.py`, INDEX).
- `aiohttp/base_protocol.py` (100L) — Base protocol: `connected`, `connection_lost`, `connection_made`, `pause_reading`, `pause_writing` (`base_protocol.py`, INDEX).

**Worker module:**
- `aiohttp/worker.py` — Gunicorn worker integration: `_notify_waiter_done` at line 140 (`worker.py`, SYM).

**Testing support:**
- `aiohttp/pytest_plugin.py` — Pytest fixtures: `AiohttpClient` at line 31, `AiohttpServer` at line 51, `AiohttpRawServer` at line 57, `aiohttp_client` at line 380, `aiohttp_raw_server` at line 325, `aiohttp_server` at line 296, `aiohttp_unused_port` at line 290 (FOCUS section).

### WebSocket Sub-package (`aiohttp/_websocket/`)

- `aiohttp/_websocket/__init__.py` (1L) — Package init (`INDEX`).
- `aiohttp/_websocket/helpers.py` (148L) — WebSocket extension helpers: `ws_ext_gen`, `ws_ext_parse` (`INDEX`).
- `aiohttp/_websocket/models.py` (167L) — WebSocket models: `WSCloseCode`, `WSHandshakeError`, `json`, `WSMessageBinary`, `WSMessageClose` (`INDEX`).
- `aiohttp/_websocket/reader.py` (31L) — Reader entry point (`INDEX`).
- `aiohttp/_websocket/reader_c.py` (499L) — C-optimized reader: `exception`, `feed_data`, `feed_eof`, `is_eof`, `read` (`INDEX`).
- `aiohttp/_websocket/reader_py.py` (499L) — Pure Python reader (same API as `reader_c.py`) (`INDEX`).
- `aiohttp/_websocket/writer.py` (262L) — WebSocket writer: `close`, `send_frame`, `WebSocketWriter` (`INDEX`).

### `docs/` Directory

Contains 2 files with a `code/` subdirectory. The `docs/code/` directory contains at least `client_middleware_cookbook.py` with `SSRFError` at line 21 (`SYM`).

### `examples/` Directory (23 files)

Includes demonstration scripts such as:
- `examples/token_refresh_middleware.py` — Token refresh/JWT middleware (`_refresh_access_token` at line 50, `generate_access_token` at line 135, `verify_bearer_token` at line 191) (`SYM/FOCUS`).
- `examples/basic_auth_middleware.py` — Basic auth middleware (`_encode_credentials` at line 39) (`SYM/FOCUS`).
- `examples/fake_server.py` — Fake server with `FakeFacebook`, `FakeResolver` (`FOCUS`).
- `examples/digest_auth_qop_auth.py` — Digest auth example (`FOCUS`).
- `examples/combined_middleware.py` — Combined middleware demo (`FOCUS`).
- `examples/logging_middleware.py` — Logging middleware demo (`FOCUS`).
- `examples/retry_middleware.py` — Retry middleware demo (`FOCUS`).
- `examples/lowlevel_srv.py` — Low-level server example (`FOCUS`).

### `tools/` Directory (5 files)

- `tools/bench-asyncio-write.py` — Async I/O write benchmarking (`FOCUS: main at line 97`).
- `tools/check_changes.py` — Changelog validation (`FOCUS: main at line 33`).
- `tools/check_sum.py` — Checksum utility (`FOCUS: main at line 15`).
- `tools/cleanup_changes.py` — Changelog cleanup (`FOCUS: main at line 27`).

### `tests/` Directory (80 files)

Contains test files with `autobahn/` (WebSocket protocol compliance testing) and `isolated/` subdirectories (`TREE`).

### Cannot Be Determined from Clue File

- The INDEX shows `...and 150 more modules` — only a subset of modules in the `aiohttp/` package are listed. Many modules (e.g., `client_ws.py`, `web_routedef.py`, `web_server.py`, `web_exceptions.py`, `http_parser.py`, `http_exceptions.py`, `typedefs.py`) are referenced in SYM/FOCUS entries but not enumerated in the truncated INDEX.
- The GAPS section notes uncovered items: `LoggingMiddleware` (×2), `RetryMiddleware` (×2).
- The exact contents of the `requirements/` directory's single file are not shown.
