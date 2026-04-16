# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: struct-aiohttp-2

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.

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

Application (aiohttp/web_app.py:71-400)
  imports: asyncio, logging, warnings, aiosignal, frozenlist
  calls: _add_subapp, _check_frozen, _prepare_middleware, handler, reg_handler, _reg_subapp_signals, add_routes, freeze
  raises: TypeError, RuntimeError, ValueError

RequestHandler (aiohttp/web_protocol.py:119-822)
  HTTP protocol implementation.
  extends: BaseProtocol
  imports: asyncio, asyncio.streams, traceback, html, http
  calls: log, AccessLoggerWrapper, _handle_request, _make_error_handler, close, connection_lost, connection_made, finish_response
  raises: ConnectionError
  uses: Response (web_response), HTTPInternalServerError (web_exceptions), StreamWriter (http)

StreamResponse (aiohttp/web_response.py:74-532)
  extends: HeadersMixin, CookieMixin
  imports: asyncio, enum, math, warnings, concurrent.futures
  calls: _generate_content_type_header, _prepare_headers, _set_status, _start_compression, _write_headers, drain, enable_compression, write
  raises: RuntimeError, ValueError, TypeError

BaseRequest (aiohttp/web_request.py:109-823)
  extends: HeadersMixin
  imports: asyncio, io, socket, string, tempfile
  calls: _etag_values, _if_match_or_none_impl, get_extra_info, multipart, read, text, FileField
  raises: RuntimeError, ValueError, HTTPUnsupportedMediaType, HTTPBadRequest
  uses: ETag (helpers), MultipartReader (multipart), HTTPRequestEntityTooLarge (web_exceptions), HTTPUnsupportedMediaType (web_exceptions)

Response (aiohttp/web_response.py:535-740)
  extends: StreamResponse
  imports: asyncio, enum, math, warnings, concurrent.futures
  calls: write
  called_by: json_bytes_response, json_response
  raises: RuntimeError, ValueError, TypeError

_cancel_pong_response_cb (aiohttp/web_ws.py:142-145)
  called_by: _cancel_heartbeat, _reset_heartbeat, _send_heartbeat, WebSocketResponse

_handle (aiohttp/web_app.py:366-390)
  sig: _handle(request)
  calls: handler, freeze, _build_middlewares

_make_response (aiohttp/web_fileresponse.py:168-222)
  Return the response result, io object, stat result, and encoding.
  sig: _make_response(request, accept_encoding)
  calls: _etag_match, _get_file_path_stat_encoding

HTTPBadRequest (aiohttp/web_exceptions.py:288-289)
  extends: HTTPClientError
  attrs: status_code=400
  imports: warnings, http, multidict, yarl, helpers

HTTPMisdirectedRequest (aiohttp/web_exceptions.py:394-395)
  extends: HTTPClientError
  attrs: status_code=421
  imports: warnings, http, multidict, yarl, helpers

HttpProcessingError (aiohttp/http_exceptions.py:10-41)
  HTTP error.
  extends: Exception
  attrs: code=0, message='', headers=None
  imports: textwrap, multidict

HttpRequestParser (aiohttp/http_parser.py:573-676)
  Read request status line.
  imports: asyncio, string, enum, multidict, yarl
  calls: RawRequestMessage
  raises: BadHttpMessage, BadHttpMethod, BadStatusLine, InvalidURLError

HttpResponseParser (aiohttp/http_parser.py:677-760)
  Read response status line and headers.
  imports: asyncio, string, enum, multidict, yarl
  calls: RawResponseMessage
  raises: BadStatusLine

RawRequestMessage (aiohttp/http_parser.py:99-111)
  extends: NamedTuple
  imports: asyncio, string, enum, multidict, yarl
  called_by: HttpRequestParser

RawResponseMessage (aiohttp/http_parser.py:112-123)
  extends: NamedTuple
  imports: asyncio, string, enum, multidict, yarl
  called_by: HttpResponseParser

Request (aiohttp/web_request.py:826-884)
  extends: BaseRequest
  imports: asyncio, io, socket, string, tempfile

_FileResponseResult (aiohttp/web_fileresponse.py:61-67)
  The result of the file response.
  extends: Enum
  imports: asyncio, io, enum, mimetypes, stat

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 16 with behavior annotations
uncovered: ClientHttpProxyError, ClientRequestArgs, ClientResponseError, GunicornUVLoopWebWorker
drill: aiohttp/web_protocol.py (~37 lines, _handle_request)
drill: aiohttp/web_ws.py (~11 lines, _handle_ping_pong_exception)

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

## WebSocketReady  (aiohttp/web_ws.py L70-75)
```
class WebSocketReady:
    ok: bool
    protocol: str | None

    def __bool__(self) -> bool:
        return self.ok
```

## __aiter__  (aiohttp/web_ws.py L742-745)
```
    def __aiter__(self) -> Self:
        return self

    @overload
```

## __anext__  (aiohttp/web_ws.py L760-766)
```
    async def __anext__(self) -> WSMessageDecodeText | WSMessageNoDecodeText:
        msg = await self.receive()
        if msg.type in (WSMsgType.CLOSE, WSMsgType.CLOSING, WSMsgType.CLOSED):
            raise StopAsyncIteration
        return msg

    def _cancel(self, exc: BaseException) -> None:
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

## _cancel_heartbeat  (aiohttp/web_ws.py L129-140)
```
    def _cancel_heartbeat(self) -> None:
        self._cancel_pong_response_cb()
        if self._heartbeat_reset_handle is not None:
            self._heartbeat_reset_handle.cancel()
            self._heartbeat_reset_handle = None
        self._need_heartbeat_reset = False
        if self._heartbeat_cb is not None:
            self._heartbeat_cb.cancel()
            self._heartbeat_cb = None
        if self._ping_task is not None:
            self._ping_task.cancel()
            self._ping_task = None
```

## _cancel_pong_response_cb  (aiohttp/web_ws.py L142-145)
```
    def _cancel_pong_response_cb(self) -> None:
        if self._pong_response_cb is not None:
            self._pong_response_cb.cancel()
            self._pong_response_cb = None
```

## _close_transport  (aiohttp/web_ws.py L574-579)
```
    def _close_transport(self) -> None:
        """Close the transport."""
        if self._req is not None and self._req.transport is not None:
            self._req.transport.close()

    @overload
```

## _flush_heartbeat_reset  (aiohttp/web_ws.py L157-162)
```
    def _flush_heartbeat_reset(self) -> None:
        self._heartbeat_reset_handle = None
        if not self._need_heartbeat_reset:
            return
        self._reset_heartbeat()
        self._need_heartbeat_reset = False
```

## _handshake  (aiohttp/web_ws.py L270-354)
```
    def _handshake(
        self, request: BaseRequest
    ) -> tuple["CIMultiDict[str]", str | None, int, bool]:
        headers = request.headers
        if "websocket" != headers.get(hdrs.UPGRADE, "").lower().strip():
            raise HTTPBadRequest(
                text=(
                    f"No WebSocket UPGRADE hdr: {headers.get(hdrs.UPGRADE)}\n Can "
                    '"Upgrade" only to "WebSocket".'
                )
            )

        if "upgrade" not in headers.get(hdrs.CONNECTION, "").lower():
            raise HTTPBadRequest(
                text=f"No CONNECTION upgrade hdr: {headers.get(hdrs.CONNECTION)}"
            )

        # find common sub-protocol between client and server
        protocol: str | None = None
        if hdrs.SEC_WEBSOCKET_PROTOCOL in headers:
            req_protocols = [
                str(proto.strip())
                for proto in headers[hdrs.SEC_WEBSOCKET_PROTOCOL].split(",")
            ]

            for proto in req_protocols:
                if proto in self._protocols:
                    protocol = proto
                    break
            else:
                # No overlap found: Return no protocol as per spec
                ws_logger.warning(
                    "%s: Client protocols %r don’t overlap server-known ones %r",
                    request.remote,
                    req_protocols,
                    self._protocols,
                )

        # check supported version
        version = headers.get(hdrs.SEC_WEBSOCKET_VERSION, "")
        if version not in ("13", "8", "7"):
            raise HTTPBadRequest(text=f"Unsupported version: {version}")

        # check client handshake for validity
        key = headers.get(hdrs.SEC_WEBSOCKET_KEY)
        try:
            if not key or len(base64.b64decode(key)) != 16:
                raise HTTPBadRequest(text=f"Handshake error: {key!r}")
        except binascii.Error:
            raise HTTPBadRequest(text=f"Handshake error: {key!r}") from None

        accept_val = base64.b64encode(
            hashlib.sha1(key.encode() + WS_KEY).digest()
        ).decode()
        response_headers = CIMultiDict(
            {
                hdrs.UPGRADE: "websocket",
                hdrs.CONNECTION: "upgrade",
                hdrs.SEC_WEBSOCKET_ACCEPT: accept_val,
            }
        )

        notakeover = False
        compress = 0
        if self._compress:
            extensions = headers.get(hdrs.SEC_WEBSOCKET_EXTENSIONS)
            # Server side always get return with no exception.
            # If something happened, just drop compress extension
            compress, notakeover = ws_ext_parse(extensions, isserver=True)
            if compress:
                enabledext = ws_ext_gen(
                    compress=compress, isserver=True, server_notakeover=notakeover
                )
                response_headers[hdrs.SEC_WEBSOCKET_EXTENSIONS] = enabledext

        if protocol:
            response_headers[hdrs.SEC_WEBSOCKET_PROTOCOL] = protocol
        return (
            response_headers,
            protocol,
            compress,
            notakeover,
        )

    def _pre_start(self, request: BaseRequest) -> tuple[str | None, WebSocketWriter]:
```

## _on_data_received  (aiohttp/web_ws.py L147-155)
```
    def _on_data_received(self) -> None:
        if self._heartbeat is None or self._need_heartbeat_reset:
            return
        loop = self._loop
        assert loop is not None
        # Coalesce multiple chunks received in the same loop tick into a single
        # heartbeat reset. Resetting immediately per chunk increases timer churn.
        self._need_heartbeat_reset = True
        self._heartbeat_reset_handle = loop.call_soon(self._flush_heartbeat_reset)
```

## _ping_task_done  (aiohttp/web_ws.py L226-230)
```
    def _ping_task_done(self, task: "asyncio.Task[None]") -> None:
        """Callback for when the ping task completes."""
        if not task.cancelled() and (exc := task.exception()):
            self._handle_ping_pong_exception(exc)
        self._ping_task = None
```

## _pong_not_received  (aiohttp/web_ws.py L232-238)
```
    def _pong_not_received(self) -> None:
        if self._req is not None and self._req.transport is not None:
            self._handle_ping_pong_exception(
                asyncio.TimeoutError(
                    f"No PONG received after {self._pong_heartbeat} seconds"
                )
            )
```

## _post_start  (aiohttp/web_ws.py L376-398)
```
    def _post_start(
        self, request: BaseRequest, protocol: str | None, writer: WebSocketWriter
    ) -> None:
        self._ws_protocol = protocol
        self._writer = writer

        self._reset_heartbeat()

        loop = self._loop
        assert loop is not None
        self._reader = WebSocketDataQueue(request._protocol, 2**16, loop=loop)
        parser = WebSocketReader(
            self._reader,
            self._max_msg_size,
            compress=bool(self._compress),
            decode_text=self._decode_text,
        )
        cb = None if self._heartbeat is None else self._on_data_received
        request.protocol.set_parser(parser, data_received_cb=cb)
        # disable HTTP keepalive for WebSocket
        request.protocol.keep_alive(False)

    def can_prepare(self, request: BaseRequest) -> WebSocketReady:
```

## _pre_start  (aiohttp/web_ws.py L354-376)
```
    def _pre_start(self, request: BaseRequest) -> tuple[str | None, WebSocketWriter]:
        self._loop = request._loop

        headers, protocol, compress, notakeover = self._handshake(request)

... (truncated)
```
--- END SOURCE SNIPPETS ---

QUESTION: What modules handle HTTP request and response processing in aiohttp, and which files contain the core web application logic?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
