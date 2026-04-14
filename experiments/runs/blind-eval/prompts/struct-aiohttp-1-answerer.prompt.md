# Blind Evaluation Prompt - MRLF v2.1 (Structural/Relational)
# Task: struct-aiohttp-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

--- CLUE FILE START ---
=CC v2.1 aiohttp@HEAD 166mod 6741sym
? What are the main packages and modules in the aiohttp codebase, and how is the project organized into directories?


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
decode                              M aiohttp/helpers.py:139    Create a BasicAuth object from an Authorization...
encode                              M aiohttp/helpers.py:178    Encode credentials.
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
DigestAuthMiddleware (aiohttp/client_middleware_digest_auth.py:145-469)
  HTTP digest authentication middleware for aiohttp client.
  imports: hashlib, yarl, client_exceptions, client_middlewares, client_reqrep
  calls: _authenticate, H, KD, _encode, _in_protection_space, escape_quotes, parse_header_pairs
  raises: ValueError, ClientError
  uses: URL (yarl), ClientError (client_exceptions)

main (examples/fake_server.py:98-117)
  calls: start, stop, FakeFacebook, FakeResolver
  uses: TCPConnector (aiohttp), ClientSession (aiohttp)

basicauth_from_netrc (aiohttp/helpers.py:244-270)
  Return :py:class:`~aiohttp.BasicAuth` credentials for ``host`` from ``netrc_obj``.
  sig: basicauth_from_netrc(netrc_obj, host)
  calls: BasicAuth
  called_by: proxies_from_env
  raises: LookupError

main (examples/combined_middleware.py:308-316)
  calls: run_test_server, run_tests

main (examples/logging_middleware.py:157-166)
  calls: run_test_server, run_tests

main (examples/basic_auth_middleware.py:179-186)
  calls: run_test_server, run_tests

main (examples/token_refresh_middleware.py:326-333)
  calls: run_test_server, run_tests

main (examples/retry_middleware.py:234-241)
  calls: run_test_server, run_tests

main (tools/bench-asyncio-write.py:97-126)
  sig: main(loop)
  behavior: ACCUMULATE(loop -> result)
  calls: fm_time, bench, time

AiohttpClient (aiohttp/pytest_plugin.py:31-48)
  extends: Protocol
  imports: asyncio, inspect, warnings, pytest, test_utils

AiohttpRawServer (aiohttp/pytest_plugin.py:57-64)
  extends: Protocol
  imports: asyncio, inspect, warnings, pytest, test_utils

AiohttpServer (aiohttp/pytest_plugin.py:51-54)
  extends: Protocol
  imports: asyncio, inspect, warnings, pytest, test_utils

aiohttp_client_cls (aiohttp/pytest_plugin.py:353-376)
  Client class to use in ``aiohttp_client`` factory.
  called_by: aiohttp_client

main (tools/check_changes.py:33-55)
  sig: main(argv)
  behavior: BRANCH(failed -> result, else -> result); ACCUMULATE(loop -> result)
  calls: get_root

main (examples/digest_auth_qop_auth.py:34-64)
  uses: DigestAuthMiddleware (aiohttp.client_middleware_digest_auth), ClientSession (aiohttp), URL (yarl)

main (aiohttp/web.py:501-565)
  sig: main(argv)
  behavior: BRANCH(args.path_and_args.hostname -> result, else -> result)
  calls: run_app
  uses: ArgumentParser (argparse)

main (tools/check_sum.py:15-46)
  sig: main(argv)
  behavior: BRANCH(dst.exists -> result, else -> result)

main (tools/cleanup_changes.py:27-41)
  behavior: ACCUMULATE(loop -> delete)

main (examples/lowlevel_srv.py:10-17)
  sig: main(loop)

proxies_from_env (aiohttp/helpers.py:273-296)
  behavior: ACCUMULATE(loop -> result)
  calls: ProxyInfo, basicauth_from_netrc, netrc_from_env, strip_auth_from_url
  called_by: get_env_proxy_for_url
  uses: URL (yarl)

BasicAuth (aiohttp/helpers.py:121-181)
  Http basic authentication helper.
  imports: asyncio, base64, binascii, enum, inspect
  calls: __new__, decode, encode
  called_by: basicauth_from_netrc, strip_auth_from_url
  raises: ValueError, TypeError

run_tests (examples/combined_middleware.py:255-305)
  Run all the middleware tests.
  calls: BasicAuthMiddleware, LoggingMiddleware, RetryMiddleware
  called_by: main
  uses: ClientSession (aiohttp)

FakeResolver (examples/fake_server.py:12-42)
  extends: AbstractResolver
  imports: asyncio, socket, ssl, aiohttp, aiohttp.abc
  calls: close, resolve
  called_by: main

parse_header_pairs (aiohttp/client_middleware_digest_auth.py:118-142)
  Parse key-value pairs from WWW-Authenticate or similar HTTP headers.
  sig: parse_header_pairs(header)
  calls: unescape_quotes
  called_by: _authenticate, DigestAuthMiddleware

strip_auth_from_url (aiohttp/helpers.py:184-190)
  Remove user and password from URL if present and return BasicAuth object.
  sig: strip_auth_from_url(url)
  calls: BasicAuth
  called_by: proxies_from_env

run_test_server (examples/combined_middleware.py:238-252)
  Run a test server with various endpoints.
  calls: TestServer
  called_by: main

_encode (aiohttp/client_middleware_digest_auth.py:202-361)
  Build digest authorization header for the current challenge.
  sig: _encode(method, url, body)
  behavior: BRANCH(nonce_bytes_eq_last_nonce -> result, else -> result); ACCUMULATE(loop -> pairs)
  calls: H, KD, escape_quotes
  called_by: __call__, DigestAuthMiddleware
  raises: ClientError
  uses: ClientError (client_exceptions), URL (yarl)

run_app (aiohttp/web.py:426-498)
  Run an app locally
  sig: run_app(app)
  calls: _cancel_tasks, _run_app
  called_by: main

run_test_server (examples/retry_middleware.py:150-164)
  Run a simple test server.
  calls: TestServer
  called_by: main

run_test_server (examples/basic_auth_middleware.py:119-131)
  Run a simple test server with basic auth endpoints.
  calls: TestServer
  called_by: main

run_test_server (examples/token_refresh_middleware.py:246-258)
  Run a test server with JWT auth endpoints.
  calls: TestServer
  called_by: main

run_test_server (examples/logging_middleware.py:87-102)
  Run a simple test server.
  calls: TestServer
  called_by: main

run_tests (examples/basic_auth_middleware.py:134-176)
  Run all basic auth middleware tests.
  calls: BasicAuthMiddleware
  called_by: main
  uses: ClientSession (aiohttp)

run_tests (examples/retry_middleware.py:167-231)
  Run all retry middleware tests.
  calls: RetryMiddleware
  called_by: main
  uses: ClientSession (aiohttp)

run_tests (examples/token_refresh_middleware.py:261-323)
  Run all token refresh middleware tests.
  calls: TokenRefreshMiddleware
  called_by: main
  uses: ClientSession (aiohttp)

run_tests (examples/logging_middleware.py:105-154)
  Run all the middleware tests.
  calls: LoggingMiddleware
  called_by: main
  uses: ClientSession (aiohttp)

_authenticate (aiohttp/client_middleware_digest_auth.py:383-440)
  Takes the given response and tries digest-auth, if needed.
  sig: _authenticate(response)
  behavior: BRANCH(namedexpr -> result, else -> result); ACCUMULATE(loop -> result)
  calls: parse_header_pairs
  called_by: __call__, DigestAuthMiddleware
  uses: URL (yarl)

__call__ (aiohttp/client_middleware_digest_auth.py:442-469)
  Run the digest auth middleware.
  sig: __call__(request, handler)
  behavior: ACCUMULATE(loop -> result)
  calls: _authenticate, _encode, _in_protection_space

bench (tools/bench-asyncio-write.py:106-119)
  sig: bench(job_title, w, body, base)
  calls: fm_time, time
  called_by: main

_in_protection_space (aiohttp/client_middleware_digest_auth.py:363-381)
  Check if the given URL is within the current protection space.
  sig: _in_protection_space(url)
  behavior: ACCUMULATE(loop -> result)
  called_by: __call__, DigestAuthMiddleware

BasicAuthMiddleware (examples/basic_auth_middleware.py:31-56)
  Middleware that adds Basic Authentication to all requests.
  imports: asyncio, base64, binascii, logging, aiohttp
  calls: _encode_credentials
  called_by: run_tests

BasicAuthMiddleware (examples/combined_middleware.py:66-92)
  Middleware that adds Basic Authentication to all requests.
  imports: asyncio, base64, binascii, logging, http
  calls: _encode_credentials
  called_by: run_tests

FakeFacebook (examples/fake_server.py:45-95)
  imports: asyncio, socket, ssl, aiohttp, aiohttp.abc
  calls: start
  called_by: main

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 73 symbols in L3, 21 with behavior annotations
drill: aiohttp/client_middleware_digest_auth.py (~306 lines, DigestAuthMiddleware)
drill: examples/fake_server.py (~16 lines, main)
drill: aiohttp/helpers.py (~27 lines, basicauth_from_netrc)

--- CLUE FILE END ---

QUESTION: What are the main packages and modules in the aiohttp codebase, and how is the project organized into directories?

Provide a detailed answer based solely on the clue file above.
For each claim, cite the specific clue entry that supports it.
