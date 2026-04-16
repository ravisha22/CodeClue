# Blind Evaluation Prompt - MRLF v2.1 with File 2 Drill-Down
# Task: struct-aiohttp-2

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

--- CLUE FILE (File 1) ---
=CC v2.1 aiohttp@HEAD 166mod 6741sym
? What modules handle HTTP request and response processing in aiohttp, and which files contain the core web application logic?


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
_handle_request (aiohttp/web_protocol.py:535-570)
  sig: _handle_request(request, start_time, request_handler)
  calls: finish_response, handle_error, log_debug
  called_by: start, RequestHandler
  uses: Response (web_response)

_handle_ping_pong_exception (aiohttp/web_ws.py:240-248)
  Handle exceptions raised during ping/pong processing.
  sig: _handle_ping_pong_exception(exc)
  calls: _set_closed, _set_code_close_transport
  called_by: _ping_task_done, _pong_not_received, WebSocketResponse
  uses: WSMessageError (http_websocket)

WebSocketResponse (aiohttp/web_ws.py:78-773)
  extends: StreamResponse
  imports: asyncio, base64, binascii, hashlib, multidict
  calls: WebSocketReady, __init__, _cancel_heartbeat, _cancel_pong_response_cb, _close_transport, _handle_ping_pong_exception, _handshake, _ping_task_done
  raises: RuntimeError, HTTPBadRequest, ConnectionResetError, TypeError
  uses: WSMessageError (http_websocket), CIMultiDict (multidict), HTTPBadRequest (web_exceptions), WebSocketReader (http)

ClientWebSocketResponse (aiohttp/client_ws.py:60-560)
  imports: asyncio, types, client_exceptions, client_reqrep, helpers
  calls: _cancel_heartbeat, _cancel_pong_response_cb, _handle_ping_pong_exception, _ping_task_done, _reset_heartbeat, _set_closed, _set_closing, close
  raises: TypeError, WSMessageTypeError, StopAsyncIteration, RuntimeError
  uses: WSMessageError (http_websocket)

FileResponse (aiohttp/web_fileresponse.py:79-406)
  A response object can be used to send files.
  extends: StreamResponse
  imports: asyncio, io, enum, mimetypes, stat
  calls: __init__, _etag_match, _get_file_path_stat_encoding, _not_modified, _precondition_failed, _prepare_open_file, _sendfile, _sendfile_fallback
  raises: ConnectionResetError
  uses: S_ISREG (stat)

HttpBadRequest (aiohttp/http_exceptions.py:55-57)
  extends: BadHttpMessage
  attrs: code=400, message='Bad Request'
  imports: textwrap, multidict

request (aiohttp/client.py:464-468)
  Perform HTTP request.
  sig: request(method, url)
  behavior: DELEGATE(_RequestContextManager -> result)

_handle_ping_pong_exception (aiohttp/client_ws.py:213-222)
  Handle exceptions raised during ping/pong processing.
  sig: _handle_ping_pong_exception(exc)
  calls: _set_closed, close
  called_by: _ping_task_done, _pong_not_received, ClientWebSocketResponse
  uses: WSMessageError (http_websocket)

from_response (aiohttp/multipart.py:688-699)
  Constructs reader instance from HTTP response.
  sig: from_response(cls, response)

body_exists (aiohttp/web_request.py:612-614)
  Return True if request has HTTP BODY, False otherwise.

can_read_body (aiohttp/web_request.py:607-609)
  Return True if request's HTTP BODY can be read, False otherwise.

remote (aiohttp/web_request.py:408-420)
  Remote IP of client initiated HTTP request.

version (aiohttp/web_request.py:381-386)
  Read only property for getting HTTP version of request.

AppRunner (aiohttp/web_runner.py:380-453)
  Web Application runner
  imports: asyncio, signal, socket, yarl, http_parser
  calls: cleanup
  raises: TypeError

delete (aiohttp/client.py:1388-1392)
  Perform HTTP DELETE request.
  sig: delete(url)
  behavior: DELEGATE(_RequestContextManager -> result)

get (aiohttp/client.py:1334-1342)
  Perform HTTP GET request.
  sig: get(url)
  behavior: DELEGATE(_RequestContextManager -> result)

head (aiohttp/client.py:1354-1362)
  Perform HTTP HEAD request.
  sig: head(url)
  behavior: DELEGATE(_RequestContextManager -> result)

options (aiohttp/client.py:1344-1352)
  Perform HTTP OPTIONS request.
  sig: options(url)
  behavior: DELEGATE(_RequestContextManager -> result)

patch (aiohttp/client.py:1380-1386)
  Perform HTTP PATCH request.
  sig: patch(url)
  behavior: DELEGATE(_RequestContextManager -> result)

post (aiohttp/client.py:1364-1370)
  Perform HTTP POST request.
  sig: post(url)
  behavior: DELEGATE(_RequestContextManager -> result)

put (aiohttp/client.py:1372-1378)
  Perform HTTP PUT request.
  sig: put(url)
  behavior: DELEGATE(_RequestContextManager -> result)

start (aiohttp/client_reqrep.py:427-474)
  Start response processing.
  sig: start(connection)
  calls: read
  raises: ClientResponseError
  uses: ClientResponseError (client_exceptions)

DigestAuthMiddleware (aiohttp/client_middleware_digest_auth.py:145-469)
  HTTP digest authentication middleware for aiohttp client.
  imports: hashlib, yarl, client_exceptions, client_middlewares, client_reqrep
  calls: _authenticate, H, KD, _encode, _in_protection_space, escape_quotes, parse_header_pairs
  raises: ValueError, ClientError
  uses: URL (yarl), ClientError (client_exceptions)

LoggingMiddleware (examples/combined_middleware.py:38-63)
  Middleware that logs request timing and response status.
  imports: asyncio, base64, binascii, logging, http
  called_by: run_tests

LoggingMiddleware (examples/logging_middleware.py:27-56)
  Middleware that logs request timing and response status.
  imports: asyncio, logging, aiohttp
  called_by: run_tests

__call__ (examples/combined_middleware.py:119-156)
  Execute request with retry logic.
  sig: __call__(request, handler)
  behavior: ACCUMULATE(range(self.max_retrie... -> delay)

__call__ (examples/retry_middleware.py:47-88)
  Execute request with retry logic.
  sig: __call__(request, handler)
  behavior: ACCUMULATE(range(self.max_retrie... -> delay)

handle_error (aiohttp/web_protocol.py:752-812)
  Handle errors.
  sig: handle_error(request, status, exc, message)
  behavior: BRANCH(self._request_count == 1 and... -> self.logger.debug('Er..., else ->...)
  calls: force_close, log_exception
  called_by: _handle_request, handler, _make_error_handler, RequestHandler
  raises: ConnectionError
  uses: Response (web_response)

_make_request (aiohttp/web_server.py:97-105)
  sig: _make_request(message, payload, protocol, writer, task)
  behavior: DELEGATE(BaseRequest -> result)
  uses: BaseRequest (web_request)

http_range (aiohttp/web_request.py:566-599)
  The content of Range HTTP header.
  raises: ValueError

finish_response (aiohttp/web_protocol.py:711-750)
  Prepare the response and write_eof, then log access.
  sig: finish_response(request, resp, start_time)
  calls: log_access, log_exception
  called_by: _handle_request, RequestHandler
  uses: HTTPInternalServerError (web_exceptions), Response (web_response)

_resolve_path_to_response (aiohttp/web_urldispatcher.py:635-668)
  Take the unresolved path and query the file system to form a response.
  sig: _resolve_path_to_response(unresolved_path)
  calls: _directory_as_html
  raises: HTTPNotFound, HTTPForbidden
  uses: FileResponse (web_fileresponse), HTTPNotFound (web_exceptions), HTTPForbidden (web_exceptions), Response (web_response)

_handle (aiohttp/web_urldispatcher.py:623-633)
  sig: _handle(request)
  raises: HTTPNotFound
  uses: HTTPNotFound (web_exceptions)

RequestHandler (aiohttp/web_protocol.py:119-822)
  HTTP protocol implementation.
  extends: BaseProtocol
  imports: asyncio, asyncio.streams, traceback, html, http
  calls: log, AccessLoggerWrapper, _handle_request, _make_error_handler, close, connection_lost, connection_made, finish_response
  raises: ConnectionError
  uses: Response (web_response), HTTPInternalServerError (web_exceptions), StreamWriter (http)

Response (aiohttp/web_response.py:535-740)
  extends: StreamResponse
  imports: asyncio, enum, math, warnings, concurrent.futures
  calls: write
  called_by: json_bytes_response, json_response
  raises: RuntimeError, ValueError, TypeError

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 224 symbols in L3, 49 with behavior annotations
uncovered: RequestPayloadError, ClientRequestBase, ResponseHandler, MultipartResponseWrapper
drill: aiohttp/web_protocol.py (~37 lines, _handle_request)
drill: aiohttp/web_ws.py (~11 lines, _handle_ping_pong_exception)
drill: aiohttp/web_request.py (~11 lines, remote)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## _handle_ping_pong_exception  (aiohttp/web_ws.py L240-248)
```
    def _handle_ping_pong_exception(self, exc: BaseException) -> None:
        """Handle exceptions raised during ping/pong processing."""
        if self._closed:
            return
        self._set_closed()
        self._set_code_close_transport(WSCloseCode.ABNORMAL_CLOSURE)
        self._exception = exc
        if self._waiting and not self._closing and self._reader is not None:
            self._reader.feed_data(WSMessageError(data=exc, extra=None))
```

## remote  (aiohttp/web_request.py L408-420)
```
    def remote(self) -> str | None:
        """Remote IP of client initiated HTTP request.

        The IP is resolved in this order:

        - overridden value by .clone(remote=new_remote) call.
        - peername of opened socket
        """
        if self._transport_peername is None:
            return None
        if isinstance(self._transport_peername, (list, tuple)):
            return str(self._transport_peername[0])
        return str(self._transport_peername)
```

## _handle_request  (aiohttp/web_protocol.py L535-570)
```
    async def _handle_request(
        self,
        request: _Request,
        start_time: float | None,
        request_handler: Callable[[_Request], Awaitable[StreamResponse]],
    ) -> tuple[StreamResponse, bool]:
        self._request_in_progress = True
        try:
            try:
                self._current_request = request
                resp = await request_handler(request)
            finally:
                self._current_request = None
        except HTTPException as exc:
            resp = Response(
                status=exc.status, reason=exc.reason, text=exc.text, headers=exc.headers
            )
            resp._cookies = exc._cookies
            resp, reset = await self.finish_response(request, resp, start_time)
        except asyncio.CancelledError:
            raise
        except asyncio.TimeoutError as exc:
            self.log_debug("Request handler timed out.", exc_info=exc)
            resp = self.handle_error(request, 504)
            resp, reset = await self.finish_response(request, resp, start_time)
        except Exception as exc:
            resp = self.handle_error(request, 500, exc)
            resp, reset = await self.finish_response(request, resp, start_time)
        else:
            resp, reset = await self.finish_response(request, resp, start_time)
        finally:
            self._request_in_progress = False
            if self._handler_waiter is not None:
                self._handler_waiter.set_result(None)

        return resp, reset
```

## finish_response  (aiohttp/web_protocol.py L711-750)
```
    async def finish_response(
        self, request: BaseRequest, resp: StreamResponse, start_time: float | None
    ) -> tuple[StreamResponse, bool]:
        """Prepare the response and write_eof, then log access.

        This has to
        be called within the context of any exception so the access logger
        can get exception information. Returns True if the client disconnects
        prematurely.
        """
        request._finish()
        if self._request_parser is not None:
            self._request_parser.set_upgraded(False)
            self._upgrade = False
            if self._message_tail:
                self._request_parser.feed_data(self._message_tail)
                self._message_tail = b""
        try:
            prepare_meth = resp.prepare
        except AttributeError:
            if resp is None:
                self.log_exception("Missing return statement on request handler")  # type: ignore[unreachable]
            else:
                self.log_exception(
                    f"Web-handler should return a response instance, got {resp!r}"
                )
            exc = HTTPInternalServerError()
            resp = Response(
                status=exc.status, reason=exc.reason, text=exc.text, headers=exc.headers
            )
            prepare_meth = resp.prepare
        try:
            await prepare_meth(request)
            await resp.write_eof()
        except ConnectionError:
            await self.log_access(request, resp, start_time)
            return resp, True

        await self.log_access(request, resp, start_time)
        return resp, False
```

## handle_error  (examples/logging_middleware.py L73-76)
```
    async def handle_error(self, request: web.Request) -> web.Response:
        """Endpoint that returns an error."""
        status = int(request.match_info.get("status", 500))
        return web.Response(status=status, text=f"Error response with status {status}")
```

## log_debug  (aiohttp/web_protocol.py L511-513)
```
    def log_debug(self, *args: Any, **kw: Any) -> None:
        if self._loop.get_debug():
            self.logger.debug(*args, **kw)
```

## _set_closed  (aiohttp/web_ws.py L250-256)
```
    def _set_closed(self) -> None:
        """Set the connection to closed.

        Cancel any heartbeat timers and set the closed flag.
        """
        self._closed = True
        self._cancel_heartbeat()
```

## close  (tests/test_web_functional.py L2071-2074)
```
        async def close(self) -> None:
            assert False

        async def resolve(
```

## __bool__  (aiohttp/web_ws.py L74-75)
```
    def __bool__(self) -> bool:
        return self.ok
```

## __delitem__  (aiohttp/web_response.py L516-517)
```
    def __delitem__(self, key: str | ResponseKey[_T]) -> None:
        del self._state[key]
```

## __eq__  (aiohttp/web_response.py L528-529)
```
    def __eq__(self, other: object) -> bool:
        return self is other
```

## __getitem__  (aiohttp/web_urldispatcher.py L1026-1027)
```
    def __getitem__(self, name: str) -> AbstractResource:
        return self._named_resources[name]
```

## __init__  (tests/test_worker.py L31-38)
```
    def __init__(self) -> None:
        self.servers: dict[object, object] = {}
        self.exit_code = 0
        self._notify_waiter: asyncio.Future[bool] | None = None
        self.cfg = mock.Mock()
        self.cfg.graceful_timeout = 100
        self.pid = "pid"
        self.wsgi = web.Application()
```

## __iter__  (tests/test_client_session.py L801-802)
```
        def __iter__(self) -> Iterator[Any]:
            return iter(self._items)
```

## __len__  (tests/test_client_session.py L798-799)
```
        def __len__(self) -> int:
            return len(self._items)
```

## __repr__  (aiohttp/web_urldispatcher.py L272-273)
```
    def __repr__(self) -> str:
        return f"<MatchInfo {super().__repr__()}: {self._route}>"
```

## __setitem__  (aiohttp/web_response.py L513-514)
```
    def __setitem__(self, key: str | ResponseKey[_T], value: Any) -> None:
        self._state[key] = value
```

## _cancel  (aiohttp/web_ws.py L766-773)
```
    def _cancel(self, exc: BaseException) -> None:
        # web_protocol calls this from connection_lost
        # or when the server is shutting down.
        self._closing = True
        self._cancel_heartbeat()
        if self._reader is not None:
            set_exception(self._reader, exc)
```

## _etag_values  (aiohttp/web_request.py L495-513)
```
    def _etag_values(etag_header: str) -> Iterator[ETag]:
        """Extract `ETag` objects from raw header."""
        if etag_header == ETAG_ANY:
            yield ETag(
                is_weak=False,
                value=ETAG_ANY,
            )
        else:
            for match in LIST_QUOTED_ETAG_RE.finditer(etag_header):
                is_weak, value, garbage = match.group(2, 3, 4)
                # Any symbol captured by 4th group means
                # that the following sequence is invalid.
                if garbage:
                    break

                yield ETag(
                    is_weak=bool(is_weak),
                    value=value,
                )
```

## _finish  (aiohttp/web_request.py L813-823)
```
    def _finish(self) -> None:
        if self._post is None or self.content_type != "multipart/form-data":
            return

        # NOTE: Release file descriptors for the
        # NOTE: `tempfile.Temporaryfile`-created `_io.BufferedRandom`
        # NOTE: instances of files sent within multipart request body
        # NOTE: via HTTP POST request.
        for file_name, file_field_object in self._post.items():
            if isinstance(file_field_object, FileField):
                file_field_object.file.close()
```

## _if_match_or_none_impl  (aiohttp/web_request.py L516-522)
```
    def _if_match_or_none_impl(
        cls, header_value: str | None
    ) -> tuple[ETag, ...] | None:
        if not header_value:
            return None

        return tuple(cls._etag_values(header_value))
```

## _prepare_hook  (aiohttp/web_request.py L878-884)
```
    async def _prepare_hook(self, response: StreamResponse) -> None:
        match_info = self._match_info
        if match_info is None:
            return
        for app in match_info._apps:
            if on_response_prepare := app.on_response_prepare:
                await on_response_prepare.send(self, response)
```

## body_exists  (aiohttp/web_request.py L612-614)
```
    def body_exists(self) -> bool:
        """Return True if request has HTTP BODY, False otherwise."""
        return type(self._payload) is not EmptyStreamReader
```

## can_read_body  (aiohttp/web_request.py L607-609)
```
    def can_read_body(self) -> bool:
        """Return True if request's HTTP BODY can be read, False otherwise."""
        return not self._payload.at_eof()
```

## client_max_size  (aiohttp/web_request.py L252-253)
```
    def client_max_size(self) -> int:
        return self._client_max_size
```

## clone  (aiohttp/web_request.py L830-852)
```
    def clone(
        self,
        *,
        method: str | _SENTINEL = sentinel,
        rel_url: StrOrURL | _SENTINEL = sentinel,
        headers: LooseHeaders | _SENTINEL = sentinel,
        scheme: str | _SENTINEL = sentinel,
        host: str | _SENTINEL = sentinel,
        remote: str | _SENTINEL = sentinel,
        client_max_size: int | _SENTINEL = sentinel,
    ) -> "Request":
        ret = super().clone(
            method=method,
            rel_url=rel_url,
            headers=headers,
            scheme=scheme,
            host=host,
            remote=remote,
            client_max_size=client_max_size,
        )
        new_ret = cast(Request, ret)
        new_ret._match_info = self._match_info
        return new_ret
```

## content  (aiohttp/web_request.py L602-604)
```
    def content(self) -> StreamReader:
        """Return raw payload stream."""
        return self._payload
```

## cookies  (aiohttp/web_request.py L554-563)
```
    def cookies(self) -> Mapping[str, str]:
        """Return request cookies.

        A read-only dictionary-like object.
        """
        # Use parse_cookie_header for RFC 6265 compliant Cookie header parsing
        # that accepts special characters in cookie names (fixes #2683)
        parsed = parse_cookie_header(self.headers.get(hdrs.COOKIE, ""))
        # Extract values from Morsel objects
        return MappingProxyType({name: morsel.value for name, morsel in parsed})
```

## forwarded  (aiohttp/web_request.py L296-354)
```
    def forwarded(self) -> tuple[Mapping[str, str], ...]:
        """A tuple containing all parsed Forwarded header(s).

        Makes an effort to parse Forwarded headers as specified by RFC 7239:

        - It adds one (immutable) dictionary per Forwarded 'field-value', ie
          per proxy. The element corresponds to the data in the Forwarded
          field-value added by the first proxy encountered by the client. Each
          subsequent item corresponds to those added by later proxies.
        - It checks that every value has valid syntax in general as specified
          in section 4: either a 'token' or a 'quoted-string'.
        - It un-escapes found escape sequences.
        - It does NOT validate 'by' and 'for' contents as specified in section
          6.
        - It does NOT validate 'host' contents (Host ABNF).
        - It does NOT validate 'proto' contents for valid URI scheme names.

        Returns a tuple containing one or more immutable dicts
        """
        elems = []
        for field_value in self._message.headers.getall(hdrs.FORWARDED, ()):
            length = len(field_value)
            pos = 0
            need_separator = False
            elem: dict[str, str] = {}
            elems.append(types.MappingProxyType(elem))
            while 0 <= pos < length:
                match = _FORWARDED_PAIR_RE.match(field_value, pos)
                if match is not None:  # got a valid forwarded-pair
                    if need_separator:
                        # bad syntax here, skip to next comma
                        pos = field_value.find(",", pos)
                    else:
                        name, value, port = match.groups()
... (truncated)
```
--- END SOURCE SNIPPETS ---

QUESTION: What modules handle HTTP request and response processing in aiohttp, and which files contain the core web application logic?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
