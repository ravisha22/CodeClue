# v2.3 Response: struct-aiohttp-1
Date: 2026-04-15

## Summary

The aiohttp codebase is organized into a main `aiohttp/` package (54 files), with supporting directories for documentation, examples, tests, and tools. The project has 166 modules and 6,741 symbols total.

## Top-Level Directory Structure

From the TREE section:
- **`aiohttp/`** (54 files) — The main library package, containing the core implementation.
  - **`_websocket/`** — A sub-package for WebSocket functionality.
- **`docs/`** (2 files) — Documentation.
  - **`code/`** — Code examples for documentation (e.g., `docs/code/client_middleware_cookbook.py` per SYM entry for `SSRFError`).
- **`examples/`** (23 files) — Example scripts and demo applications.
- **`requirements/`** (1 file) — Dependency requirements.
- **`tests/`** (80 files) — Test suite.
  - **`autobahn/`** and **`isolated/`** — Specialized test subdirectories.
- **`tools/`** (5 files) — Utility/build tools.
- **`setup.py`** — Package setup/installation script.

## Main Package: aiohttp/

### Core Modules (from INDEX)

- **`aiohttp/__init__.py`** (258L) — Package initialization and public API exports.
- **`aiohttp/abc.py`** (266L) — Abstract base classes defining interfaces: `AbstractAccessLogger`, `AbstractAsyncAccessLogger`, `AbstractCookieJar`, `AbstractMatchInfo`, `AbstractResolver`, `AbstractRouter`, `AbstractStreamWriter`, `AbstractView` (FOCUS section entries).
- **`aiohttp/base_protocol.py`** (100L) — Base protocol with `connected`, `connection_lost`, `connection_made`, `pause_reading`, `pause_writing`.

### Client-Side Modules

- **`aiohttp/client.py`** (1654L) — The main HTTP client with symbols `auth`, `auto_decompress`, `close`, `closed`, `connector` (INDEX).
- **`aiohttp/client_exceptions.py`** (388L) — Client exception classes: `ClientConnectionError`, `ClientConnectionResetError`, etc. (INDEX).
- **`aiohttp/client_middleware_digest_auth.py`** (469L) — HTTP digest authentication middleware with `DigestAuthChallenge`, `H`, `KD`, `DigestAuthMiddleware`, `escape_quotes` (INDEX). Detailed in FOCUS: implements RFC 7616, parses challenge headers, manages protection spaces.
- **`aiohttp/client_middlewares.py`** (55L) — Client middleware infrastructure: `wrapped`, `make_wrapper`, `single_middleware_handler`, `build_client_middlewares` (INDEX).
- **`aiohttp/client_proto.py`** (371L) — Client protocol handling: `abort`, `close`, `closed`, `connection_lost`, `data_received` (INDEX).
- **`aiohttp/client_reqrep.py`** — Client request/response (SYM entries: `release` at L506, `_release_connection` at L542, `_cleanup_writer` at L563, `_notify_content` at L568, `__new__` at L111).
- **`aiohttp/client_ws.py`** — Client WebSocket support (SYM entries: `_cancel_pong_response_cb` at L119, `_cancel_heartbeat` at L106, `send_frame` at L279, `_set_closed` at L224, `close` at L320).

### Server-Side Web Modules

- **`aiohttp/web_app.py`** — Web application class with `pre_freeze` at L212, `freeze` at L241, `reg_handler` at L260, `CleanupError` class at L403 (SYM/FOCUS entries).
- **`aiohttp/web_fileresponse.py`** — File response handling: `prepare` at L243, `_not_modified` at L150, `_precondition_failed` at L161, `_prepare_open_file` at L288 (SYM entries).
- **`aiohttp/web_protocol.py`** — Web protocol/connection handling: `close` at L481, `force_close` at L491, `log` at L98, `log_exception` at L515, `handle_error` at L752 (SYM entries).
- **`aiohttp/web_request.py`** — Request objects: `_etag_values` at L495, `_if_match_or_none_impl` at L516, `read` at L624 (SYM entries).
- **`aiohttp/web_response.py`** — Response objects: `write` at L448 (SYM entry).
- **`aiohttp/web_runner.py`** — Server runner infrastructure: `stop` at L73 (SYM entry).
- **`aiohttp/web_urldispatcher.py`** — URL routing/dispatch: `_get_resource_index_key` at L1077, `_quote_path` at L1230, `index_resource` at L1088 (SYM entries). Contains `AbstractResource`, `AbstractRoute`, `AbstractRuleMatching` (FOCUS entries).
- **`aiohttp/web_routedef.py`** — Route definition: `AbstractRouteDef` at L36-39 (FOCUS entry).
- **`aiohttp/web_ws.py`** — Server WebSocket: `close` at L508, `_close_transport` at L574, `_cancel_pong_response_cb` at L142, `_set_code_close_transport` at L569, `send_frame` at L452, `_cancel_heartbeat` at L129, `_set_closed` at L250, `_reset_heartbeat` at L164 (SYM entries).

### Infrastructure/Utility Modules

- **`aiohttp/connector.py`** — Connection management: `_available_connections` at L528, `_release_waiter` at L720 (SYM entries).
- **`aiohttp/formdata.py`** — Form data handling: `add_field` at L48 (SYM entry).
- **`aiohttp/helpers.py`** — Utility functions: `decode` at L139, `encode` at L178, `get_content_type` at L367, `parse_content_type` at L387, `_parse_content_type` at L760, `BasicAuth` class at L121 (SYM/FOCUS entries).
- **`aiohttp/http_writer.py`** — HTTP writing: `write` at L167, `_writelines` at L105, `_write` at L94, `drain` at L353, `_send_headers_with_payload` at L131, `_write_chunked_payload` at L124 (SYM entries).
- **`aiohttp/multipart.py`** — Multipart handling: `append` at L948, `append_payload` at L963, `read` at L304, `readline` at L423, `read_chunk` at L324, `decode_iter` at L524, `_decode_content_transfer` at L565 (SYM entries).
- **`aiohttp/payload.py`** — Payload management: `_set_or_restore_start_position` at L470, `LookupError` at L50, `get` at L98, `register` at L121 (SYM entries).
- **`aiohttp/streams.py`** — Stream handling: `AsyncStreamIterator` at L32 (SYM entry).
- **`aiohttp/worker.py`** — Worker process management: `_notify_waiter_done` at L140 (SYM entry).
- **`aiohttp/pytest_plugin.py`** — Pytest integration: `AiohttpClient` at L31-48, `AiohttpRawServer` at L57-64, `AiohttpServer` at L51-54, `aiohttp_client_cls` at L353-376, `aiohttp_client` at L380-431 (FOCUS entries).

### WebSocket Sub-Package

- **`aiohttp/_websocket/__init__.py`** (1L) — Package marker.
- **`aiohttp/_websocket/helpers.py`** (148L) — `ws_ext_gen`, `ws_ext_parse` (INDEX).
- **`aiohttp/_websocket/models.py`** (167L) — `WSCloseCode`, `WSHandshakeError`, `json`, `WSMessageBinary`, `WSMessageClose` (INDEX).
- **`aiohttp/_websocket/reader.py`** (31L) — Reader entry point.
- **`aiohttp/_websocket/reader_c.py`** (499L) — C-optimized reader: `exception`, `feed_data`, `feed_eof`, `is_eof`, `read` (INDEX).
- **`aiohttp/_websocket/reader_py.py`** (499L) — Pure Python reader (same interface as reader_c) (INDEX).
- **`aiohttp/_websocket/writer.py`** (262L) — `close`, `send_frame`, `WebSocketWriter` (INDEX).

### Cookie Handling

- **`aiohttp/_cookie_helpers.py`** (339L) — `parse_cookie_header`, `parse_set_cookie_headers`, `preserve_morsel_with_coded_value` (INDEX).

## Examples Directory

Contains 23 files including (from SYM/FOCUS entries):
- `examples/fake_server.py` — Fake server with `FakeFacebook`, `FakeResolver` (FOCUS: `main`).
- `examples/digest_auth_qop_auth.py` — Digest auth example (FOCUS: `main`).
- `examples/combined_middleware.py` — Combined middleware demo (FOCUS: `main`).
- `examples/logging_middleware.py` — Logging middleware (FOCUS: `main`).
- `examples/retry_middleware.py` — Retry middleware (FOCUS: `main`).
- `examples/token_refresh_middleware.py` — Token refresh middleware with `_refresh_access_token`, `verify_bearer_token`, `generate_access_token` (SYM entries).
- `examples/basic_auth_middleware.py` — Basic auth with `_encode_credentials` (SYM entry).
- `examples/lowlevel_srv.py` — Low-level server (FOCUS: `main`).

## Tools Directory

Contains 5 files including (from FOCUS entries):
- `tools/bench-asyncio-write.py` — Benchmarking tool (FOCUS: `main`).
- `tools/cleanup_changes.py` — Cleanup utility (FOCUS: `main`).
- `tools/check_sum.py` — Checksum tool (FOCUS: `main`).
- `tools/check_changes.py` — Change checking tool (FOCUS: `main`).

## Uncertainty / Limits

- The INDEX shows `...and 150 more modules` beyond the 16 listed, so the full module list is not visible. Only modules with symbols in the SYM/FOCUS sections can be identified.
- The `docs/` directory structure beyond `docs/code/` is not detailed.
- Internal module dependencies and import relationships are partially visible through FOCUS `imports` fields but not comprehensively mapped.
