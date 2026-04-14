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
? If a handler reads incoming data from different body formats, what does the request object actually do for JSON, URL-encoded forms, and multipart uploads, and where are payload limits enforced?


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
FormData (aiohttp/formdata.py:16-167)
  Helper class for form body generation.
  imports: io, urllib.parse, multidict, helpers, payload
  calls: _gen_form_data, _gen_form_urlencoded, add_field, add_fields
  raises: TypeError, ValueError
  uses: MultiDict (multidict)

BodyPartReaderPayload (aiohttp/multipart.py:603-636)
  extends: Payload
  imports: base64, binascii, uuid, warnings, types
  calls: decode_iter, read_chunk
  raises: TypeError

MultipartPayloadWriter (aiohttp/multipart.py:1149-1204)
  imports: base64, binascii, uuid, warnings, types
  called_by: MultipartWriter

JsonBytesPayload (aiohttp/payload.py:943-963)
  JSON payload for encoders that return bytes directly.
  extends: BytesPayload
  imports: asyncio, enum, io, mimetypes, warnings

JsonPayload (aiohttp/payload.py:924-940)
  extends: BytesPayload
  imports: asyncio, enum, io, mimetypes, warnings

RequestHandler (aiohttp/web_protocol.py:119-822)
  HTTP protocol implementation.
  extends: BaseProtocol
  imports: asyncio, asyncio.streams, traceback, html, http
  calls: log, AccessLoggerWrapper, _handle_request, _make_error_handler, close, connection_lost, connection_made, finish_response
  raises: ConnectionError
  uses: Response (web_response), HTTPInternalServerError (web_exceptions), StreamWriter (http)

RequestPayloadError (aiohttp/web_protocol.py:75-76)
  Payload parsing error.
  extends: Exception
  imports: asyncio, asyncio.streams, traceback, html, http

_update_body_from_data (aiohttp/client_reqrep.py:1137-1180)
  Update request body from data.
  sig: _update_body_from_data(body)
  calls: body
  called_by: _update_body, ClientRequest
  uses: FormData (formdata)

_load_json_data (aiohttp/cookiejar.py:164-195)
  Load cookies from parsed JSON data.
  sig: _load_json_data(data)
  called_by: load, CookieJar
  uses: Morsel (http.cookies)

_gen_form_data (aiohttp/formdata.py:128-161)
  Encode a list of fields using the multipart/form-data MIME format
  called_by: __call__, FormData
  raises: TypeError

get_read_buffer_limits (aiohttp/streams.py:176-177)

can_read_body (aiohttp/web_request.py:607-609)
  Return True if request's HTTP BODY can be read, False otherwise.

handle_json_data (examples/logging_middleware.py:78-84)
  Endpoint that echoes JSON data.
  sig: handle_json_data(request)

WebSocketDataQueue (aiohttp/_websocket/reader_c.py:60-138)
  WebSocketDataQueue resumes and pauses an underlying stream.
  imports: asyncio, builtins, base_protocol, compression_utils, helpers
  calls: _read_from_buffer, _release_waiter, set_exception
  raises: EofStream

WebSocketDataQueue (aiohttp/_websocket/reader_py.py:60-138)
  WebSocketDataQueue resumes and pauses an underlying stream.
  imports: asyncio, builtins, base_protocol, compression_utils, helpers
  calls: _read_from_buffer, _release_waiter, set_exception
  raises: EofStream

_BaseRequestContextManager (aiohttp/client.py:1508-1542)
  imports: asyncio, base64, hashlib, traceback, warnings
  calls: __await__, send, throw

_RequestOptions (aiohttp/client.py:176-203)
  extends: TypedDict
  imports: asyncio, base64, hashlib, traceback, warnings

_SessionRequestContextManager (aiohttp/client.py:1549-1578)
  imports: asyncio, base64, hashlib, traceback, warnings

ClientPayloadError (aiohttp/client_exceptions.py:253-254)
  Response payload error.
  extends: ClientError
  imports: asyncio, multidict, typedefs, ssl, client_reqrep

InvalidURL (aiohttp/client_exceptions.py:257-291)
  Invalid URL.
  extends: ClientError, ValueError
  imports: asyncio, multidict, typedefs, ssl, client_reqrep

InvalidUrlClientError (aiohttp/client_exceptions.py:294-295)
  Invalid URL client error.
  extends: InvalidURL
  imports: asyncio, multidict, typedefs, ssl, client_reqrep

InvalidUrlRedirectClientError (aiohttp/client_exceptions.py:306-307)
  Invalid URL redirect client error.
  extends: InvalidUrlClientError, RedirectClientError
  imports: asyncio, multidict, typedefs, ssl, client_reqrep

NonHttpUrlClientError (aiohttp/client_exceptions.py:302-303)
  Non http URL client error.
  extends: ClientError
  imports: asyncio, multidict, typedefs, ssl, client_reqrep

NonHttpUrlRedirectClientError (aiohttp/client_exceptions.py:310-311)
  Non http URL redirect client error.
  extends: NonHttpUrlClientError, RedirectClientError
  imports: asyncio, multidict, typedefs, ssl, client_reqrep

ResponseHandler (aiohttp/client_proto.py:31-371)
  Helper class to adapt between Protocol and StreamReader.
  extends: BaseProtocol
  imports: asyncio, base_protocol, client_exceptions, helpers, http
  calls: __init__, _drop_timeout, _reschedule_timeout, abort, close, connection_lost, data_received, pause_reading
  uses: ClientOSError (client_exceptions), ServerDisconnectedError (client_exceptions), ClientConnectionError (client_exceptions), ClientPayloadError (client_exceptions)

_Payload (aiohttp/client_proto.py:27-28)
  extends: ErrorableProtocol, Protocol
  imports: asyncio, base_protocol, client_exceptions, helpers, http

ClientRequest (aiohttp/client_reqrep.py:954-1434)
  extends: ClientRequestBase
  imports: asyncio, codecs, io, traceback, warnings
  calls: _update_auto_headers, _update_body, _update_body_from_data, _update_content_encoding, _update_cookies, _update_expect_continue, _update_proxy, _update_transfer_encoding
  raises: ValueError
  uses: CIMultiDict (multidict), FormData (formdata), SimpleCookie (http.cookies)

ClientRequestArgs (aiohttp/client_reqrep.py:930-951)
  extends: TypedDict
  imports: asyncio, codecs, io, traceback, warnings

ClientRequestBase (aiohttp/client_reqrep.py:686-927)
  An internal class for proxy requests.
  attrs: auth=None, method='GET'
  imports: asyncio, codecs, io, traceback, warnings
  calls: _get_content_length, _update_auth, _update_headers, _update_host, is_ssl, __new__
  raises: ValueError, TypeError, InvalidURL
  uses: CIMultiDict (multidict), InvalidURL (client_exceptions), BasicAuth (helpers)

RequestInfo (aiohttp/client_reqrep.py:109-124)
  extends: _RequestInfo
  imports: asyncio, codecs, io, traceback, warnings
  calls: __new__

_RequestInfo (aiohttp/client_reqrep.py:102-106)
  extends: NamedTuple
  imports: asyncio, codecs, io, traceback, warnings

DecompressionBaseHandler (aiohttp/compression_utils.py:153-180)
  extends: ABC
  imports: asyncio, zlib, concurrent.futures, brotlicffi, compression.zstd

RequestKey (aiohttp/helpers.py:894-895)
  Keys for static typing support in Request.
  imports: asyncio, base64, binascii, enum, inspect

HttpBadRequest (aiohttp/http_exceptions.py:55-57)
  extends: BadHttpMessage
  attrs: code=400, message='Bad Request'
  imports: textwrap, multidict

PayloadEncodingError (aiohttp/http_exceptions.py:60-61)
  Base class for payload errors
  extends: BadHttpMessage
  imports: textwrap, multidict

HttpPayloadParser (aiohttp/http_parser.py:761-966)
  imports: asyncio, string, enum, multidict, yarl
  calls: begin_http_chunk_receiving, end_http_chunk_receiving, set_exception, DeflateBuffer
  called_by: HttpParser
  raises: ContentLengthError, TransferEncodingError, LineTooLong, BadHttpMessage

HttpRequestParser (aiohttp/http_parser.py:573-676)
  Read request status line.
  imports: asyncio, string, enum, multidict, yarl
  calls: RawRequestMessage
  raises: BadHttpMessage, BadHttpMethod, BadStatusLine, InvalidURLError

RawRequestMessage (aiohttp/http_parser.py:99-111)
  extends: NamedTuple
  imports: asyncio, string, enum, multidict, yarl
  called_by: HttpRequestParser

-- GAPS
- Question mentions [actually, data, different, encoded, enforced] — not found in focus or symbol index
- Module tests/test_web_request_handler.py matches question but has no focus detail
  > drill: tests/test_web_request_handler.py
- Module tests/test_websocket_data_queue.py matches question but has no focus detail
  > drill: tests/test_websocket_data_queue.py

--- CLUE FILE END ---

QUESTION: If a handler reads incoming data from different body formats, what does the request object actually do for JSON, URL-encoded forms, and multipart uploads, and where are payload limits enforced?

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

FACT 1: BaseRequest.read consumes the payload incrementally with readany, accumulates bytes in memory, and raises HTTPRequestEntityTooLarge as soon as the accumulated body exceeds client_max_size.
FACT 2: BaseRequest.json first calls text, then rejects unexpected mimetypes by raising HTTPBadRequest when content_type checking is enabled instead of blindly decoding any body as JSON.
FACT 3: BaseRequest.post returns an empty MultiDict for non-POST-like methods or unsupported content types, rather than attempting to parse arbitrary request bodies.
FACT 4: For multipart file parts, BaseRequest.post writes decoded chunks into a TemporaryFile via the executor, enforces the same size limit while streaming, and stores the result as a FileField with application/octet-stream as the fallback content type.

=== TASK 3: WRITE RESULTS TO FILE ===

After completing Tasks 1 and 2, create or append to the file:
`experiments/runs/blind-eval/blind-eval-results.jsonl`

Write ONE JSON line (append, do not overwrite) with this exact structure:
```json
{"task_id": "blind-aiohttp-1", "model": "<your model name>", "scores": [{"fact": 1, "verdict": "COVERED_or_MISSED", "reason": "..."}, {"fact": 2, "verdict": "COVERED_or_MISSED", "reason": "..."}, {"fact": 3, "verdict": "COVERED_or_MISSED", "reason": "..."}, {"fact": 4, "verdict": "COVERED_or_MISSED", "reason": "..."}], "total_covered": <count>, "total_facts": <total>, "sufficient": <true or false>}
```

Replace each score entry with your actual COVERED/MISSED judgment.

Also output the scoring block in your response for visibility:

```
=== BLIND SCORING ===
Task: blind-aiohttp-1
Model: [state which model you are]
FACT 1: [COVERED or MISSED] - [brief justification]
FACT 2: [COVERED or MISSED] - [brief justification]
FACT 3: [COVERED or MISSED] - [brief justification]
FACT 4: [COVERED or MISSED] - [brief justification]
Score: [count of COVERED]/[total]
Sufficient: [YES if >= 60%, NO otherwise]
```
