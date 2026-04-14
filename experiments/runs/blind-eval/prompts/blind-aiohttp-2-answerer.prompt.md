# Blind Evaluation Prompt
# Run this in a SEPARATE VS Code Copilot Chat session (fresh chat, no prior context).

You have THREE tasks to complete. Read carefully.

=== TASK 1: ANSWER THE QUESTION ===

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code — it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.
If the clue does not contain enough information to fully answer, say what
you CAN determine and what you CANNOT.

--- CLUE FILE START ---
=CC v2 aiohttp@HEAD 166mod 6741sym
? During application shutdown, how does the server unwind startup resources, and what happens if cleanup only partially initialized or multiple cleanup steps fail?


-- TREE
aiohttp/  (54 files)
  _websocket/
docs/  (2 files)
  code/
examples/  (23 files)
requirements/  (1 files)
tests/  (80 files)
  autobahn/  isolated/
tools/  (5 files)
setup.py

-- INDEX
aiohttp/__init__.py                             258L  
aiohttp/_cookie_helpers.py                      339L  parse_cookie_header, parse_set_cookie_headers, preserve_morsel_with_coded_value
aiohttp/_websocket/__init__.py                    1L  
aiohttp/_websocket/helpers.py                   148L  ws_ext_gen, ws_ext_parse
aiohttp/_websocket/models.py                    167L  WSCloseCode, WSHandshakeError, json, WSMessageBinary, WSMessageClose
aiohttp/_websocket/reader.py                     31L  
aiohttp/_websocket/reader_c.py                  499L  exception, feed_data, feed_eof, is_eof, read
aiohttp/_websocket/reader_py.py                 499L  exception, feed_data, feed_eof, is_eof, read
aiohttp/_websocket/writer.py                    262L  close, send_frame, WebSocketWriter
aiohttp/abc.py                                  266L  enabled, log, AbstractAccessLogger, enabled, log
aiohttp/base_protocol.py                        100L  connected, connection_lost, connection_made, pause_reading, pause_writing
aiohttp/client.py                              1654L  auth, auto_decompress, close, closed, connector
aiohttp/client_exceptions.py                    388L  ClientConnectionError, ClientConnectionResetError, certificate_error, host, port
aiohttp/client_middleware_digest_auth.py        469L  DigestAuthChallenge, H, KD, DigestAuthMiddleware, escape_quotes
aiohttp/client_middlewares.py                    55L  wrapped, make_wrapper, single_middleware_handler, build_client_middlewares
aiohttp/client_proto.py                         371L  abort, close, closed, connection_lost, data_received
  ...and 150 more modules

-- SYM
append                              M aiohttp/multipart.py:948    function append
append_payload                      M aiohttp/multipart.py:963    Adds a new body part to multipart writer.
encode                              M aiohttp/helpers.py:178    Encode credentials.
decode                              M aiohttp/helpers.py:139    Create a BasicAuth object from an Authorization...
prepare                             M aiohttp/web_fileresponse.py:243    async_function prepare
write                               M aiohttp/http_writer.py:167    Writes chunk of data to a stream.
pre_freeze                          M aiohttp/web_app.py:212    function pre_freeze
close                               M aiohttp/web_ws.py:508    Close websocket connection.
release                             M aiohttp/client_reqrep.py:506    function release
_close_transport                    M aiohttp/web_ws.py:574    Close the transport.
_drop_timeout                       M aiohttp/client_proto.py:267    function _drop_timeout
freeze                              M aiohttp/web_app.py:241    function freeze
_cancel_pong_response_cb            M aiohttp/client_ws.py:119    function _cancel_pong_response_cb
_cancel_pong_response_cb            M aiohttp/web_ws.py:142    function _cancel_pong_response_cb
_set_code_close_transport           M aiohttp/web_ws.py:569    Set the close code and close the transport.
read                                M aiohttp/multipart.py:304    Reads body part data.
close                               M aiohttp/web_protocol.py:481    Close connection.
send_frame                          M aiohttp/client_ws.py:279    Send a frame over the websocket.
send_frame                          M aiohttp/web_ws.py:452    Send a frame over the websocket.
_release_connection                 M aiohttp/client_reqrep.py:542    function _release_connection
_cancel_heartbeat                   M aiohttp/client_ws.py:106    function _cancel_heartbeat
_writelines                         M aiohttp/http_writer.py:105    function _writelines
_cleanup_writer                     M aiohttp/client_reqrep.py:563    function _cleanup_writer
_cancel_heartbeat                   M aiohttp/web_ws.py:129    function _cancel_heartbeat
_set_or_restore_start_position      M aiohttp/payload.py:470    Set or restore the start position of the file-l...
_write                              M aiohttp/http_writer.py:94     function _write
force_close                         M aiohttp/web_protocol.py:491    Forcefully close connection.
_get_resource_index_key             M aiohttp/web_urldispatcher.py:1077   Return a key to index the resource in the resou...
_quote_path                         M aiohttp/web_urldispatcher.py:1230   function _quote_path
drain                               M aiohttp/http_writer.py:353    Flush the write buffer.
readline                            M aiohttp/multipart.py:423    Reads body part by line by line.
_available_connections              M aiohttp/connector.py:528    Return number of available connections.
_notify_content                     M aiohttp/client_reqrep.py:568    function _notify_content
_not_modified                       M aiohttp/web_fileresponse.py:150    async_function _not_modified
_precondition_failed                M aiohttp/web_fileresponse.py:161    async_function _precondition_failed
_prepare_open_file                  M aiohttp/web_fileresponse.py:288    async_function _prepare_open_file
get_content_type                    M aiohttp/helpers.py:367    Re-implementation from Message
read_chunk                          M aiohttp/multipart.py:324    Reads body part content chunk of the specified ...
decode_iter                         M aiohttp/multipart.py:524    Async generator that yields decoded data chunks.
LookupError                         C aiohttp/payload.py:50     Raised when no payload factory is found for the...
AsyncStreamIterator                 C aiohttp/streams.py:32     class AsyncStreamIterator
parse_content_type                  M aiohttp/helpers.py:387    Parse Content-Type header.
_refresh_access_token               M examples/token_refresh_middleware.py:50     Refresh the access token using the refresh token.
_encode_credentials                 M examples/basic_auth_middleware.py:39     Encode username and password to base64.
verify_bearer_token                 M examples/token_refresh_middleware.py:191    Verify bearer token and return user data if valid.
index_resource                      M aiohttp/web_urldispatcher.py:1088   Add a resource to the resource index.
_etag_values                        M aiohttp/web_request.py:495    Extract `ETag` objects from raw header.
_notify_waiter_done                 M aiohttp/worker.py:140    function _notify_waiter_done
SSRFError                           C docs/code/client_middleware_cookbook.py:21     A request was made to a blacklisted host.
CleanupError                        C aiohttp/web_app.py:403    class CleanupError
_set_closed                         M aiohttp/client_ws.py:224    Set the connection to closed.
generate_access_token               M examples/token_refresh_middleware.py:135    Generate a secure random access token.
_release_waiter                     M aiohttp/connector.py:720    Iterates over all waiters until one to be relea...
stop                                M aiohttp/web_runner.py:73     async_function stop
write                               M aiohttp/web_response.py:448    async_function write
BasicAuth                           C aiohttp/helpers.py:121    Http basic authentication helper.
log                                 M aiohttp/web_protocol.py:98     async_function log
get                                 M aiohttp/payload.py:98     function get
_reschedule_timeout                 M aiohttp/client_proto.py:272    function _reschedule_timeout
register                            M aiohttp/payload.py:121    function register
_write_websocket_frame              M aiohttp/_websocket/writer.py:124    Write a websocket frame to the transport.
_parse_content_type                 M aiohttp/helpers.py:760    function _parse_content_type
log_exception                       M aiohttp/web_protocol.py:515    function log_exception
_set_closed                         M aiohttp/web_ws.py:250    Set the connection to closed.
close                               M aiohttp/client_ws.py:320    async_function close
handle_error                        M aiohttp/web_protocol.py:752    Handle errors.
read                                M aiohttp/web_request.py:624    Read request body if present.
_reset_heartbeat                    M aiohttp/web_ws.py:164    function _reset_heartbeat
set_exception                       M aiohttp/client_proto.py:204    function set_exception
add_field                           M aiohttp/formdata.py:48     function add_field
reg_handler                         M aiohttp/web_app.py:260    function reg_handler
_decode_content_transfer            M aiohttp/multipart.py:565    function _decode_content_transfer
_send_headers_with_payload          M aiohttp/http_writer.py:131    Send buffered headers with payload, coalescing ...
__new__                             M aiohttp/client_reqrep.py:111    Create a new RequestInfo instance.
H                                   M aiohttp/client_middleware_digest_auth.py:273    RFC 7616 Section 3: Hash function H(data) = hex...
_if_match_or_none_impl              M aiohttp/web_request.py:516    function _if_match_or_none_impl
_write_chunked_payload              M aiohttp/http_writer.py:124    Write a chunk with proper chunked encoding.
  ...and 1859 more symbols

-- FOCUS
_cleanup_server (aiohttp/web_runner.py:452-453)

_cleanup_server (aiohttp/web_runner.py:337-338)
  Run any cleanup steps after the server is shutdown.

_cleanup_server (aiohttp/web_runner.py:376-377)

ServerConnectionError (aiohttp/client_exceptions.py:212-213)
  Server connection errors.
  extends: ClientConnectionError
  imports: asyncio, multidict, typedefs, ssl, client_reqrep

ServerDisconnectedError (aiohttp/client_exceptions.py:216-224)
  Server disconnected.
  extends: ServerConnectionError
  imports: asyncio, multidict, typedefs, ssl, client_reqrep

ServerFingerprintMismatch (aiohttp/client_exceptions.py:239-250)
  SSL certificate does not match expected fingerprint.
  extends: ServerConnectionError
  imports: asyncio, multidict, typedefs, ssl, client_reqrep

ServerTimeoutError (aiohttp/client_exceptions.py:227-228)
  Server timeout error.
  extends: ServerConnectionError, TimeoutError
  imports: asyncio, multidict, typedefs, ssl, client_reqrep

AiohttpRawServer (aiohttp/pytest_plugin.py:57-64)
  extends: Protocol
  imports: asyncio, inspect, warnings, pytest, test_utils

AiohttpServer (aiohttp/pytest_plugin.py:51-54)
  extends: Protocol
  imports: asyncio, inspect, warnings, pytest, test_utils

Application (aiohttp/web_app.py:71-400)
  imports: asyncio, logging, warnings, aiosignal, frozenlist
  calls: _add_subapp, _check_frozen, _prepare_middleware, handler, reg_handler, _reg_subapp_signals, add_routes, freeze
  raises: TypeError, RuntimeError, ValueError

CleanupContext (aiohttp/web_app.py:415-441)
  imports: asyncio, logging, warnings, aiosignal, frozenlist
  calls: CleanupError
  called_by: Application
  raises: CleanupError

CleanupError (aiohttp/web_app.py:403-406)
  extends: RuntimeError
  imports: asyncio, logging, warnings, aiosignal, frozenlist
  called_by: _on_cleanup, CleanupContext

HTTPInternalServerError (aiohttp/web_exceptions.py:463-464)
  extends: HTTPServerError
  attrs: status_code=500
  imports: warnings, http, multidict, yarl, helpers

ServerRunner (aiohttp/web_runner.py:355-377)
  Low-level web server runner
  imports: asyncio, signal, socket, yarl, http_parser

Server (aiohttp/web_server.py:30-126)
  imports: asyncio, warnings, http_parser, streams, web_protocol
  calls: shutdown

AbstractResource (aiohttp/web_urldispatcher.py:101-145)
  extends: Sized
  imports: asyncio, base64, hashlib, html, inspect

DynamicResource (aiohttp/web_urldispatcher.py:402-472)
  extends: Resource
  attrs: GOOD='[^{}/]+'
  imports: asyncio, base64, hashlib, html, inspect
  calls: _quote_path, _requote_path, _unquote_path_safe
  called_by: add_resource, UrlDispatcher
  raises: ValueError

MatchedSubAppResource (aiohttp/web_urldispatcher.py:822-848)
  extends: PrefixedSubAppResource
  imports: asyncio, base64, hashlib, html, inspect
  calls: add_app

PlainResource (aiohttp/web_urldispatcher.py:362-399)
  extends: Resource
  imports: asyncio, base64, hashlib, html, inspect
  called_by: add_resource, UrlDispatcher

PrefixResource (aiohttp/web_urldispatcher.py:475-495)
  extends: AbstractResource
  imports: asyncio, base64, hashlib, html, inspect
  calls: _requote_path

PrefixedSubAppResource (aiohttp/web_urldispatcher.py:707-748)
  extends: PrefixResource
  imports: asyncio, base64, hashlib, html, inspect
  calls: _add_prefix_to_resources, index_resource, resources, routes, unindex_resource, add_app
  raises: RuntimeError

Resource (aiohttp/web_urldispatcher.py:308-357)
  extends: AbstractResource
  imports: asyncio, base64, hashlib, html, inspect
  calls: register_route, ResourceRoute, UrlMappingMatchInfo
  raises: RuntimeError

ResourceRoute (aiohttp/web_urldispatcher.py:851-882)
  A route with resource
  extends: AbstractRoute
  imports: asyncio, base64, hashlib, html, inspect
  called_by: Resource, set_options_route, StaticResource

ResourcesView (aiohttp/web_urldispatcher.py:934-945)
  extends: Sized
  imports: asyncio, base64, hashlib, html, inspect
  called_by: resources, UrlDispatcher

StaticResource (aiohttp/web_urldispatcher.py:500-704)
  extends: PrefixResource
  attrs: VERSION_KEY='v'
  imports: asyncio, base64, hashlib, html, inspect
  calls: ResourceRoute, _directory_as_html, _get_file_hash, UrlMappingMatchInfo, _quote_path, _unquote_path_safe
  called_by: add_static, UrlDispatcher
  raises: ValueError, RuntimeError, HTTPNotFound, HTTPForbidden

_cleanup_writer (aiohttp/client_reqrep.py:563-566)
  called_by: __del__, _response_eof, close, release, ClientResponse

_cleanup (aiohttp/connector.py:380-417)
  Cleanup unused transports.

_cleanup_closed (aiohttp/connector.py:419-440)
  Double confirmation for transport close.
  calls: abort
  called_by: BaseConnector

aiohttp_raw_server (aiohttp/pytest_plugin.py:325-349)
  Factory to create a RawTestServer instance, given a web handler.
  sig: aiohttp_raw_server(loop)
  uses: RawTestServer (test_utils)

aiohttp_server (aiohttp/pytest_plugin.py:296-321)
  Factory to create a TestServer instance, given an app.
  sig: aiohttp_server(loop)
  uses: TestServer (test_utils)

cleanup (aiohttp/web_app.py:351-360)
  Causes on_cleanup signal
  calls: _on_cleanup

cleanup_ctx (aiohttp/web_app.py:326-327)

on_cleanup (aiohttp/web_app.py:322-323)

on_shutdown (aiohttp/web_app.py:318-319)

on_startup (aiohttp/web_app.py:314-315)

shutdown (aiohttp/web_app.py:344-349)
  Causes on_shutdown signal

startup (aiohttp/web_app.py:337-342)
  Causes on_startup signal

_on_cleanup (aiohttp/web_app.py:430-441)
  sig: _on_cleanup(app)
  calls: CleanupError
  called_by: cleanup, Application
  raises: CleanupError

_on_startup (aiohttp/web_app.py:420-428)
  sig: _on_startup(app)

shutdown (aiohttp/web_protocol.py:315-363)
  Do worker process exit preparations.
  sig: shutdown(timeout)
  calls: force_close

_make_server (aiohttp/web_runner.py:421-430)
  uses: Server (web_server)

shutdown (aiohttp/web_runner.py:418-419)

_make_server (aiohttp/web_runner.py:333-334)
  Return a new server for the runner to serve requests.

cleanup (aiohttp/web_runner.py:305-330)
  calls: stop
  called_by: AppRunner

server (aiohttp/web_runner.py:269-270)

shutdown (aiohttp/web_runner.py:302-303)
  Call any shutdown hooks to help server close gracefully.

_make_server (aiohttp/web_runner.py:373-374)

shutdown (aiohttp/web_runner.py:370-371)

pre_shutdown (aiohttp/web_server.py:107-109)

shutdown (aiohttp/web_server.py:111-114)
  sig: shutdown(timeout)
  called_by: Server

resource (aiohttp/web_urldispatcher.py:198-199)

_add_prefix_to_resources (aiohttp/web_urldispatcher.py:717-724)
  sig: _add_prefix_to_resources(prefix)
  calls: index_resource, resources, unindex_resource
  called_by: PrefixedSubAppResource

_get_resource_index_key (aiohttp/web_urldispatcher.py:1077-1086)
  Return a key to index the resource in the resource index.
  sig: _get_resource_index_key(resource)
  called_by: index_resource, unindex_resource, UrlDispatcher

add_resource (aiohttp/web_urldispatcher.py:1101-1115)
  sig: add_resource(path)
  calls: DynamicResource, PlainResource, register_resource
  called_by: add_get, UrlDispatcher
  raises: ValueError

-- GAPS
- Question mentions [happens, initialized, multiple, partially, steps] — not found in focus or symbol index
- Module tools/cleanup_changes.py matches question but has no focus detail
  > drill: tools/cleanup_changes.py
- Module tests/autobahn/server/server.py matches question but has no focus detail
  > drill: tests/autobahn/server/server.py

--- CLUE FILE END ---

QUESTION: During application shutdown, how does the server unwind startup resources, and what happens if cleanup only partially initialized or multiple cleanup steps fail?

Provide a detailed answer covering:
1. Which specific files and symbols are involved (cite from the clue)
2. How the mechanism works (based on what the clue tells you)
3. Any error handling, invariants, or safety properties visible in the clue
4. What the clue does NOT tell you (gaps in your understanding)

=== TASK 2: SCORE YOUR ANSWER ===

After writing your answer above, score it against these gold facts.
For EACH fact, state COVERED (your answer contains or can infer this) or
MISSED (your answer does not contain this). Be strict — vague proximity
is not coverage.

FACT 1: Application.startup and Application.shutdown only send the on_startup and on_shutdown signals; the actual resource enter and exit logic is wired through CleanupContext handlers that were appended to those signals during Application initialization.
FACT 2: Application.cleanup has a fallback path for failed or incomplete startup: if the on_cleanup signal was not frozen yet, it directly calls _cleanup_ctx._on_cleanup so entered cleanup contexts still get unwound.
FACT 3: CleanupContext._on_startup accepts either async context managers or async-generator callbacks, wrapping generator callbacks with asynccontextmanager before entering them and storing the exit handles in order.
FACT 4: CleanupContext._on_cleanup unwinds stored exits in reverse order, re-raises a single failure directly, and raises CleanupError with the collected exception list when multiple cleanup callbacks fail.

=== TASK 3: WRITE RESULTS TO FILE ===

After completing Tasks 1 and 2, create or append to the file:
`experiments/runs/blind-eval/blind-eval-results.jsonl`

Write ONE JSON line (append, do not overwrite) with this exact structure:
```json
{"task_id": "blind-aiohttp-2", "model": "<your model name>", "scores": [{"fact": 1, "verdict": "COVERED_or_MISSED", "reason": "..."}, {"fact": 2, "verdict": "COVERED_or_MISSED", "reason": "..."}, {"fact": 3, "verdict": "COVERED_or_MISSED", "reason": "..."}, {"fact": 4, "verdict": "COVERED_or_MISSED", "reason": "..."}], "total_covered": <count>, "total_facts": <total>, "sufficient": <true or false>}
```

Replace each score entry with your actual COVERED/MISSED judgment.

Also output the scoring block in your response for visibility:

```
=== BLIND SCORING ===
Task: blind-aiohttp-2
Model: [state which model you are]
FACT 1: [COVERED or MISSED] - [brief justification]
FACT 2: [COVERED or MISSED] - [brief justification]
FACT 3: [COVERED or MISSED] - [brief justification]
FACT 4: [COVERED or MISSED] - [brief justification]
Score: [count of COVERED]/[total]
Sufficient: [YES if >= 60%, NO otherwise]
```
