# Blind Evaluation Prompt - MRLF v2.4
# Task: rel-aiohttp-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 aiohttp@HEAD 166mod 6741sym
? What is the class hierarchy for request and response objects in aiohttp, and which classes extend which base classes?


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
BaseRequest (aiohttp/web_request.py:109-823)
  extends: HeadersMixin
  imports: asyncio, io, socket, string, tempfile
  calls: _etag_values, _if_match_or_none_impl, get_extra_info, multipart, read, text, FileField
  raises: RuntimeError, ValueError, HTTPUnsupportedMediaType, HTTPBadRequest
  uses: ETag (helpers), MultipartReader (multipart), HTTPRequestEntityTooLarge (web_exceptions), HTTPUnsupportedMediaType (web_exceptions)

ClientResponseError (aiohttp/client_exceptions.py:59-99)
  Base class for exceptions that occur after getting a response.
  extends: ClientError
  imports: asyncio, multidict, typedefs, ssl, client_reqrep

_BaseRequestContextManager (aiohttp/client.py:1508-1542)
  imports: asyncio, base64, hashlib, traceback, warnings
  calls: __await__, send, throw

ClientRequest (aiohttp/client_reqrep.py:954-1434)
  extends: ClientRequestBase
  imports: asyncio, codecs, io, traceback, warnings
  calls: _update_auto_headers, _update_body, _update_body_from_data, _update_content_encoding, _update_cookies, _update_expect_continue, _update_proxy, _update_transfer_encoding
  raises: ValueError
  uses: CIMultiDict (multidict), FormData (formdata), SimpleCookie (http.cookies)

Request (aiohttp/web_request.py:826-884)
  extends: BaseRequest
  imports: asyncio, io, socket, string, tempfile

WebSocketResponse (aiohttp/web_ws.py:78-773)
  extends: StreamResponse
  imports: asyncio, base64, binascii, hashlib, multidict
  calls: WebSocketReady, __init__, _cancel_heartbeat, _cancel_pong_response_cb, _close_transport, _handle_ping_pong_exception, _handshake, _ping_task_done
  raises: RuntimeError, HTTPBadRequest, ConnectionResetError, TypeError
  uses: WSMessageError (http_websocket), CIMultiDict (multidict), HTTPBadRequest (web_exceptions), WebSocketReader (http)

Response (aiohttp/web_response.py:535-740)
  extends: StreamResponse
  imports: asyncio, enum, math, warnings, concurrent.futures
  calls: write
  called_by: json_bytes_response, json_response
  raises: RuntimeError, ValueError, TypeError

RequestInfo (aiohttp/client_reqrep.py:109-124)
  extends: _RequestInfo
  imports: asyncio, codecs, io, traceback, warnings
  calls: __new__

ClientResponse (aiohttp/client_reqrep.py:184-683)
  extends: HeadersMixin
  imports: asyncio, codecs, io, traceback, warnings
  calls: _cleanup_writer, _notify_content, _release_connection, _wait_released, close, get_encoding, read, release
  raises: ClientResponseError, RuntimeError, ClientConnectionError, ContentTypeError
  uses: ClientConnectionError (client_exceptions)

StreamResponse (aiohttp/web_response.py:74-532)
  extends: HeadersMixin, CookieMixin
  imports: asyncio, enum, math, warnings, concurrent.futures
  calls: _generate_content_type_header, _prepare_headers, _set_status, _start_compression, _write_headers, drain, enable_compression, write
  raises: RuntimeError, ValueError, TypeError

BaseSite (aiohttp/web_runner.py:47-78)
  extends: ABC
  imports: asyncio, signal, socket, yarl, http_parser
  calls: _check_site, _reg_site, _unreg_site
  raises: RuntimeError

BaseProtocol (aiohttp/base_protocol.py:9-100)
  extends: Protocol
  imports: asyncio, client_exceptions, helpers, tcp_helpers
  calls: pause_reading, resume_reading
  raises: ClientConnectionResetError

BaseRunner (aiohttp/web_runner.py:252-352)
  extends: ABC
  imports: asyncio, signal, socket, yarl, http_parser
  calls: stop
  raises: RuntimeError

ClientRequestArgs (aiohttp/client_reqrep.py:930-951)
  extends: TypedDict
  imports: asyncio, codecs, io, traceback, warnings

DecompressionBaseHandler (aiohttp/compression_utils.py:153-180)
  extends: ABC
  imports: asyncio, zlib, concurrent.futures, brotlicffi, compression.zstd

HTTPBadRequest (aiohttp/web_exceptions.py:288-289)
  extends: HTTPClientError
  attrs: status_code=400
  imports: warnings, http, multidict, yarl, helpers

HTTPMisdirectedRequest (aiohttp/web_exceptions.py:394-395)
  extends: HTTPClientError
  attrs: status_code=421
  imports: warnings, http, multidict, yarl, helpers

HttpBadRequest (aiohttp/http_exceptions.py:55-57)
  extends: BadHttpMessage
  attrs: code=400, message='Bad Request'
  imports: textwrap, multidict

RawRequestMessage (aiohttp/http_parser.py:99-111)
  extends: NamedTuple
  imports: asyncio, string, enum, multidict, yarl
  called_by: HttpRequestParser

RawResponseMessage (aiohttp/http_parser.py:112-123)
  extends: NamedTuple
  imports: asyncio, string, enum, multidict, yarl
  called_by: HttpResponseParser

_RequestInfo (aiohttp/client_reqrep.py:102-106)
  extends: NamedTuple
  imports: asyncio, codecs, io, traceback, warnings

_RequestOptions (aiohttp/client.py:176-203)
  extends: TypedDict
  imports: asyncio, base64, hashlib, traceback, warnings

AiohttpClient (aiohttp/pytest_plugin.py:31-48)
  extends: Protocol
  imports: asyncio, inspect, warnings, pytest, test_utils

AiohttpRawServer (aiohttp/pytest_plugin.py:57-64)
  extends: Protocol
  imports: asyncio, inspect, warnings, pytest, test_utils

AiohttpServer (aiohttp/pytest_plugin.py:51-54)
  extends: Protocol
  imports: asyncio, inspect, warnings, pytest, test_utils

ClientWebSocketResponse (aiohttp/client_ws.py:60-560)
  imports: asyncio, types, client_exceptions, client_reqrep, helpers
  calls: _cancel_heartbeat, _cancel_pong_response_cb, _handle_ping_pong_exception, _ping_task_done, _reset_heartbeat, _set_closed, _set_closing, close
  raises: TypeError, WSMessageTypeError, StopAsyncIteration, RuntimeError
  uses: WSMessageError (http_websocket)

BaseConnector (aiohttp/connector.py:226-793)
  Base connector class.
  imports: asyncio, random, socket, traceback, warnings
  calls: _available_connections, _cleanup_closed, _get, _release_acquired, _release_waiter, _update_proxy_auth_header_and_build_proxy_req, _wait_for_available_connection, Connection
  raises: NotImplementedError, ValueError, ClientConnectionError
  uses: ClientRequestBase (client_reqrep)

BaseKey (aiohttp/helpers.py:837-887)
  Base for concrete context storage key classes.
  imports: asyncio, base64, binascii, enum, inspect
  raises: RuntimeError

BaseTimerContext (aiohttp/helpers.py:649-654)
  imports: asyncio, base64, binascii, enum, inspect

_SessionRequestContextManager (aiohttp/client.py:1549-1578)
  imports: asyncio, base64, hashlib, traceback, warnings

aiohttp_client_cls (aiohttp/pytest_plugin.py:353-376)
  Client class to use in ``aiohttp_client`` factory.
  called_by: aiohttp_client

ResponseHandler (aiohttp/client_proto.py:31-371)
  Helper class to adapt between Protocol and StreamReader.
  extends: BaseProtocol
  imports: asyncio, base_protocol, client_exceptions, helpers, http
  calls: __init__, _drop_timeout, _reschedule_timeout, abort, close, connection_lost, data_received, pause_reading
  uses: ClientOSError (client_exceptions), ServerDisconnectedError (client_exceptions), ClientConnectionError (client_exceptions), ClientPayloadError (client_exceptions)

FileResponse (aiohttp/web_fileresponse.py:79-406)
  A response object can be used to send files.
  extends: StreamResponse
  imports: asyncio, io, enum, mimetypes, stat
  calls: __init__, _etag_match, _get_file_path_stat_encoding, _not_modified, _precondition_failed, _prepare_open_file, _sendfile, _sendfile_fallback
  raises: ConnectionResetError
  uses: S_ISREG (stat)

_FileResponseResult (aiohttp/web_fileresponse.py:61-67)
  The result of the file response.
  extends: Enum
  imports: asyncio, io, enum, mimetypes, stat

_make_request (aiohttp/web_server.py:97-105)
  sig: _make_request(message, payload, protocol, writer, task)
  behavior: DELEGATE(BaseRequest -> result)
  uses: BaseRequest (web_request)

-- GAPS
type: RELATIONAL (answerable from L2-L3 structure)
coverage: 80 symbols in L3, 15 with behavior annotations
uncovered: on_request_start, on_response_chunk_received, on_response_prepare, request

--- CLUE FILE END ---

QUESTION: What is the class hierarchy for request and response objects in aiohttp, and which classes extend which base classes?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
