# v2.5 Response: struct-aiohttp-1
Date: 2026-04-16

## Question
What are the main packages and modules in the aiohttp codebase, and how is the project organized into directories?

## Answer

### Top-Level Directory Structure

The aiohttp repository is organized into six top-level directories plus a root `setup.py` (TREE entry):

1. **`aiohttp/`** (54 files) — The core library package. Contains a sub-package `_websocket/`.
2. **`docs/`** (2 files) — Documentation, with a `code/` subdirectory.
3. **`examples/`** (23 files) — Example applications and middleware demos.
4. **`requirements/`** (1 file) — Dependency specification.
5. **`tests/`** (80 files) — Test suite, with `autobahn/` and `isolated/` subdirectories.
6. **`tools/`** (5 files) — Utility scripts.

### Core Package: `aiohttp/`

The main `aiohttp/` package (54 files) contains the following key modules, identified from the INDEX:

- **`__init__.py`** (258L) — Package root/public API surface (INDEX: `aiohttp/__init__.py`).
- **`client.py`** (1654L) — HTTP client implementation with symbols `auth`, `auto_decompress`, `close`, `closed`, `connector` (INDEX: `aiohttp/client.py`).
- **`web_app.py`** — Web application class with `pre_freeze`, `freeze`, `reg_handler` and `CleanupError` (SYM entries for `aiohttp/web_app.py`).
- **`web_request.py`** — Request processing: `_etag_values`, `_if_match_or_none_impl`, `read` (SYM: `aiohttp/web_request.py`).
- **`web_response.py`** — Response handling: `write` (SYM: `aiohttp/web_response.py:448`).
- **`web_fileresponse.py`** — File response serving: `prepare`, `_not_modified`, `_precondition_failed`, `_prepare_open_file` (SYM: `aiohttp/web_fileresponse.py`).
- **`web_ws.py`** — Server-side WebSocket support: `close`, `send_frame`, `_close_transport`, `_cancel_heartbeat`, `_cancel_pong_response_cb` (SYM: `aiohttp/web_ws.py`).
- **`web_protocol.py`** — HTTP protocol handling: `close`, `force_close`, `log`, `log_exception`, `handle_error` (SYM: `aiohttp/web_protocol.py`).
- **`web_urldispatcher.py`** — URL routing: `_get_resource_index_key`, `_quote_path`, `index_resource` (SYM: `aiohttp/web_urldispatcher.py`).
- **`web_runner.py`** — Server lifecycle: `stop` (SYM: `aiohttp/web_runner.py:73`).
- **`web.py`** — Entry point with `main` and `run_app` (FOCUS: `main` at `aiohttp/web.py:501-565`, `run_app` at `aiohttp/web.py:426-498`).
- **`client_reqrep.py`** — Client request/response: `release`, `_release_connection`, `_cleanup_writer`, `_notify_content`, `__new__` (SYM: `aiohttp/client_reqrep.py`).
- **`client_ws.py`** — Client-side WebSocket: `send_frame`, `_cancel_heartbeat`, `_cancel_pong_response_cb`, `close` (SYM: `aiohttp/client_ws.py`).
- **`client_proto.py`** (371L) — Client protocol: `abort`, `close`, `closed`, `connection_lost`, `data_received`, `_drop_timeout`, `_reschedule_timeout`, `set_exception` (INDEX + SYM: `aiohttp/client_proto.py`).
- **`client_exceptions.py`** (388L) — Exception classes: `ClientConnectionError`, `ClientConnectionResetError` (INDEX: `aiohttp/client_exceptions.py`).
- **`client_middleware_digest_auth.py`** (469L) — Digest auth middleware: `DigestAuthMiddleware`, `H`, `KD`, `escape_quotes`, `parse_header_pairs` (INDEX + FOCUS: `aiohttp/client_middleware_digest_auth.py`).
- **`client_middlewares.py`** (55L) — Client middleware framework: `wrapped`, `make_wrapper`, `single_middleware_handler`, `build_client_middlewares` (INDEX: `aiohttp/client_middlewares.py`).
- **`abc.py`** (266L) — Abstract base classes: `AbstractAccessLogger` (INDEX: `aiohttp/abc.py`).
- **`base_protocol.py`** (100L) — Base protocol: `connected`, `connection_lost`, `connection_made`, `pause_reading`, `pause_writing` (INDEX: `aiohttp/base_protocol.py`).
- **`connector.py`** — Connection management: `_available_connections`, `_release_waiter` (SYM: `aiohttp/connector.py`).
- **`helpers.py`** — Utility functions: `BasicAuth`, `decode`, `encode`, `basicauth_from_netrc`, `proxies_from_env`, `get_content_type`, `parse_content_type`, `_parse_content_type` (SYM + FOCUS: `aiohttp/helpers.py`).
- **`multipart.py`** — Multipart handling: `append`, `append_payload`, `read`, `readline`, `read_chunk`, `decode_iter` (SYM: `aiohttp/multipart.py`).
- **`payload.py`** — Payload abstraction: `LookupError`, `get`, `register`, `_set_or_restore_start_position` (SYM: `aiohttp/payload.py`).
- **`streams.py`** — Stream classes: `AsyncStreamIterator` (SYM: `aiohttp/streams.py:32`).
- **`http_writer.py`** — HTTP output: `write`, `_write`, `_writelines`, `_write_chunked_payload`, `_send_headers_with_payload`, `drain` (SYM: `aiohttp/http_writer.py`).
- **`formdata.py`** — Form data building: `add_field` (SYM: `aiohttp/formdata.py:48`).
- **`_cookie_helpers.py`** (339L) — Cookie parsing: `parse_cookie_header`, `parse_set_cookie_headers`, `preserve_morsel_with_coded_value` (INDEX: `aiohttp/_cookie_helpers.py`).
- **`pytest_plugin.py`** — Test fixtures: `AiohttpClient`, `AiohttpRawServer`, `AiohttpServer`, `aiohttp_client`, `aiohttp_server`, `aiohttp_raw_server`, `aiohttp_unused_port` (FOCUS: `aiohttp/pytest_plugin.py`).
- **`worker.py`** — Worker support: `_notify_waiter_done` (SYM: `aiohttp/worker.py:140`).

The INDEX notes "...and 150 more modules" beyond the 16 explicitly listed, indicating substantial additional modules.

### WebSocket Sub-Package: `aiohttp/_websocket/`

A dedicated sub-package (TREE: `_websocket/`) containing:

- **`__init__.py`** (1L) — Package marker (INDEX).
- **`helpers.py`** (148L) — WebSocket extension helpers: `ws_ext_gen`, `ws_ext_parse` (INDEX).
- **`models.py`** (167L) — Data models: `WSCloseCode`, `WSHandshakeError`, `WSMessageBinary`, `WSMessageClose` (INDEX).
- **`reader.py`** (31L) — Reader entry point (INDEX).
- **`reader_c.py`** (499L) — C-optimized reader: `exception`, `feed_data`, `feed_eof`, `is_eof`, `read` (INDEX).
- **`reader_py.py`** (499L) — Python reader (same API as reader_c): `exception`, `feed_data`, `feed_eof`, `is_eof`, `read` (INDEX).
- **`writer.py`** (262L) — WebSocket writing: `close`, `send_frame`, `WebSocketWriter`, `_write_websocket_frame` (INDEX + SYM).

### Examples Package

The `examples/` directory (23 files) contains middleware demos and sample applications, including:

- `fake_server.py` — Fake server with `FakeResolver` (FOCUS: `FakeResolver` at `examples/fake_server.py:12-42`).
- `basic_auth_middleware.py` — Basic auth: `_encode_credentials`, `run_tests`, `run_test_server` (SYM + FOCUS).
- `token_refresh_middleware.py` — Token refresh: `_refresh_access_token`, `generate_access_token`, `verify_bearer_token` (SYM + FOCUS).
- `retry_middleware.py`, `logging_middleware.py`, `combined_middleware.py` — Additional middleware examples (FOCUS entries).
- `digest_auth_qop_auth.py`, `lowlevel_srv.py` — Other demos (FOCUS entries).

### Tools Package

The `tools/` directory (5 files) contains utility scripts:

- `bench-asyncio-write.py` — Performance benchmarking (FOCUS: `main` at `tools/bench-asyncio-write.py:97-126`).
- `check_sum.py` — Checksum utility (FOCUS: `main` at `tools/check_sum.py:15-46`).
- `cleanup_changes.py` — Changelog cleanup (FOCUS: `main` at `tools/cleanup_changes.py:27-41`).
- `check_changes.py` — Change validation (FOCUS: `main` at `tools/check_changes.py:33-55`).

### Documentation

The `docs/` directory (2 files) with a `code/` subdirectory contains at least `client_middleware_cookbook.py` which defines `SSRFError` (SYM: `docs/code/client_middleware_cookbook.py:21`).

### What Cannot Be Determined

Per GAPS: "coverage: 80 symbols in L3, 20 with behavior annotations" and "uncovered: AbstractAccessLogger, AbstractAsyncAccessLogger, AbstractCookieJar, AbstractMatchInfo" — the full details of these abstract base classes and 150+ additional modules beyond those shown in the INDEX are not available from this clue file.
