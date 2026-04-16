# Blind Evaluation Prompt - MRLF v2.1 with File 2 Drill-Down
# Task: blind-aiohttp-1

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

--- CLUE FILE (File 1) ---
=CC v2.1 aiohttp@HEAD 166mod 6741sym
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
_update_body_from_data (aiohttp/client_reqrep.py:1137-1180)
  Update request body from data.
  sig: _update_body_from_data(body)
  behavior: BRANCH(isinstance(body, FormData) -> body(), else -> result); ACCUMULATE(body.headers.items()... -> result)
  calls: body
  called_by: _update_body, ClientRequest
  uses: FormData (formdata)

json (aiohttp/multipart.py:467-473)
  Like read(), but assumes that body parts contains JSON data.
  calls: get_charset, read

read (aiohttp/multipart.py:304-322)
  Reads body part data.
  behavior: ACCUMULATE(data.extend loop -> data)
  calls: decode_iter, read_chunk
  called_by: _read_chunk_from_length, _read_chunk_from_stream, form, json, read_chunk, text, BodyPartReader

update_body (aiohttp/client_reqrep.py:1199-1259)
  Update request body and close previous payload if needed.
  sig: update_body(body)
  calls: _update_body, close

BodyPartReaderPayload (aiohttp/multipart.py:603-636)
  extends: Payload
  imports: base64, binascii, uuid, warnings, types
  calls: decode_iter, read_chunk
  raises: TypeError

multipart (aiohttp/web_request.py:673-680)
  Return async iterator to process BODY as multipart.
  behavior: DELEGATE(MultipartReader -> result)
  called_by: post, BaseRequest
  uses: MultipartReader (multipart)

append_payload (aiohttp/multipart.py:963-999)
  Adds a new body part to multipart writer.
  sig: append_payload(payload)
  behavior: BRANCH(self._is_form_data -> result, else -> raise RuntimeError(f'...)
  calls: append
  called_by: append, append_form, append_json, MultipartWriter
  raises: RuntimeError

_load_json_data (aiohttp/cookiejar.py:164-195)
  Load cookies from parsed JSON data.
  sig: _load_json_data(data)
  behavior: ACCUMULATE(data.items() loop -> result)
  called_by: load, CookieJar
  uses: Morsel (http.cookies)

url (aiohttp/web_request.py:423-427)
  The full URL of the request.
  behavior: DELEGATE(URL.build.join -> result)

json (aiohttp/web_request.py:654-671)
  Return BODY as JSON.
  calls: text
  raises: HTTPBadRequest
  uses: HTTPBadRequest (web_exceptions)

BodyPartReader (aiohttp/multipart.py:257-599)
  Multipart reader for single body part.
  attrs: chunk_size=8192
  imports: base64, binascii, uuid, warnings, types
  calls: _apply_content_transfer_decoding, _decode_content, _decode_content_async, _decode_content_transfer, _needs_content_decoding, _read_chunk_from_length, _read_chunk_from_stream, decode_iter
  raises: RuntimeError, StopAsyncIteration, ValueError
  uses: ZLibDecompressor (compression_utils), CIMultiDict (multidict)

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

body_exists (aiohttp/web_request.py:612-614)
  Return True if request has HTTP BODY, False otherwise.

can_read_body (aiohttp/web_request.py:607-609)
  Return True if request's HTTP BODY can be read, False otherwise.

handle_json_data (examples/logging_middleware.py:78-84)
  Endpoint that echoes JSON data.
  sig: handle_json_data(request)

read_chunk (aiohttp/multipart.py:324-366)
  Reads body part content chunk of the specified size.
  sig: read_chunk(size)
  behavior: BRANCH(self._length -> await self._read_chun..., else -> await self._read_ch...)
  calls: _read_chunk_from_length, _read_chunk_from_stream, read, readline
  called_by: read, BodyPartReader, BodyPartReaderPayload, MultipartReader
  raises: ValueError

MultipartReader (aiohttp/multipart.py:639-854)
  Multipart body reader.
  imports: base64, binascii, uuid, warnings, types
  calls: read_chunk, readline, _get_boundary, _get_part_reader, _maybe_release_last_part, _read_boundary, _read_headers, _read_until_first_boundary
  raises: ValueError, StopAsyncIteration, BadHttpMessage, RuntimeError
  uses: HeadersParser (http), BadHttpMessage (http_exceptions), CIMultiDict (multidict)

_update_body (aiohttp/client_reqrep.py:1182-1197)
  Update request body after its already been set.
  sig: _update_body(body)
  calls: _update_body_from_data, _update_transfer_encoding
  called_by: update_body, ClientRequest

MultipartWriter (aiohttp/multipart.py:860-1146)
  Multipart body writer.
  extends: Payload
  imports: base64, binascii, uuid, warnings, types
  calls: enable_compression, enable_encoding, write_eof, MultipartPayloadWriter, append, append_payload, close
  raises: ValueError, RuntimeError, TypeError
  uses: ZLibCompressor (compression_utils), CIMultiDict (multidict)

read (aiohttp/web_request.py:624-643)
  Read request body if present.
  called_by: post, text, BaseRequest
  raises: HTTPRequestEntityTooLarge
  uses: HTTPRequestEntityTooLarge (web_exceptions)

_gen_form_data (aiohttp/formdata.py:128-161)
  Encode a list of fields using the multipart/form-data MIME format
  behavior: ACCUMULATE(self._fields loop -> result, raises TypeError)
  called_by: __call__, FormData
  raises: TypeError

_read (aiohttp/payload.py:510-526)
  Read a chunk of data from the file-like object.
  sig: _read(remaining_content_len)
  behavior: DELEGATE(_value.read -> result)

_read (aiohttp/payload.py:779-798)
  Read a chunk of data from the text file-like object.
  sig: _read(remaining_content_len)

handler (aiohttp/abc.py:55-56)
  Execute matched request handler

json (aiohttp/_websocket/models.py:81-85)
  Return parsed JSON data.
  behavior: DELEGATE(loads -> result)

json (aiohttp/_websocket/models.py:55-59)
  Return parsed JSON data.
  behavior: DELEGATE(loads -> result)

json (aiohttp/_websocket/models.py:70-72)
  Return parsed JSON data.
  behavior: DELEGATE(loads -> result)

must_be_empty_body (aiohttp/helpers.py:1105-1111)
  Check if a request must return an empty body.
  sig: must_be_empty_body(method, code)

send_json_bytes (aiohttp/client_ws.py:306-318)
  Send JSON data using a bytes-returning encoder as a binary frame.
  sig: send_json_bytes(data, compress)
  calls: send_bytes

send_json_bytes (aiohttp/web_ws.py:485-499)
  Send JSON data using a bytes-returning encoder as a binary frame.
  sig: send_json_bytes(data, compress)
  calls: send_bytes

strip_auth_from_url (aiohttp/helpers.py:184-190)
  Remove user and password from URL if present and return BasicAuth object.
  sig: strip_auth_from_url(url)
  calls: BasicAuth
  called_by: proxies_from_env

readline (aiohttp/multipart.py:423-450)
  Reads body part by line by line.
  behavior: BRANCH(self._unread -> self._unread.popleft(), else -> await self._content.r...)
  calls: append
  called_by: read_chunk, BodyPartReader, _read_headers, _readline, MultipartReader

LookupError (aiohttp/payload.py:50-51)
  Raised when no payload factory is found for the given data type.
  extends: Exception
  imports: asyncio, enum, io, mimetypes, warnings
  called_by: get, PayloadRegistry

form (aiohttp/multipart.py:475-493)
  Like read(), but assumes that body parts contain form urlencoded data.
  behavior: BRANCH(encoding is not None -> encoding, else -> self.get_charset(defa...)
  calls: get_charset, read
  raises: ValueError

text (aiohttp/multipart.py:459-465)
  Like read(), but assumes that body part contains text data.
  calls: get_charset, read

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 302 symbols in L3, 77 with behavior annotations
uncovered: RequestHandler, post, _read_headers, _read_chunk_from_length
drill: aiohttp/client_reqrep.py (~41 lines, _update_body_from_data)
drill: aiohttp/multipart.py (~9 lines, json)
drill: aiohttp/multipart.py (~17 lines, read)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## json  (aiohttp/web_request.py L654-671)
```
    async def json(
        self,
        *,
        loads: JSONDecoder = DEFAULT_JSON_DECODER,
        content_type: str | None = "application/json",
    ) -> Any:
        """Return BODY as JSON."""
        body = await self.text()
        if content_type:
            if not is_expected_content_type(self.content_type, content_type):
                raise HTTPBadRequest(
                    text=(
                        "Attempt to decode JSON with "
                        "unexpected mimetype: %s" % self.content_type
                    )
                )

        return loads(body)
```

## read  (tests/test_web_response.py L1185-1189)
```
    def read(self, size: int = -1) -> bytes:
        return self._lines.pop()


@pytest.mark.parametrize(
```

## _update_body_from_data  (aiohttp/client_reqrep.py L1137-1180)
```
    def _update_body_from_data(self, body: Any) -> None:
        """Update request body from data."""
        if body is None:
            self._body = self._EMPTY_BODY
            # Set Content-Length to 0 when body is None for methods that expect a body
            if (
                self.method not in self.GET_METHODS
                and not self.chunked
                and hdrs.CONTENT_LENGTH not in self.headers
            ):
                self.headers[hdrs.CONTENT_LENGTH] = "0"
            return

        # FormData
        if isinstance(body, FormData):
            body = body()
        else:
            try:
                body = payload.PAYLOAD_REGISTRY.get(body, disposition=None)
            except payload.LookupError:
                boundary = None
                if hdrs.CONTENT_TYPE in self.headers:
                    boundary = parse_mimetype(
                        self.headers[hdrs.CONTENT_TYPE]
                    ).parameters.get("boundary")
                body = FormData(body, boundary=boundary)()

        self._body = body

        # enable chunked encoding if needed
        if not self.chunked and hdrs.CONTENT_LENGTH not in self.headers:
            if (size := body.size) is not None:
                self.headers[hdrs.CONTENT_LENGTH] = str(size)
            else:
                self.chunked = True

        # copy payload headers
        assert body.headers
        headers = self.headers
        skip_headers = self._skip_auto_headers
        for key, value in body.headers.items():
            if key in headers or (skip_headers is not None and key in skip_headers):
                continue
            headers[key] = value
```

## body  (aiohttp/web_response.py L610-633)
```
    def body(self, body: Any) -> None:
        if body is None:
            self._body = None
        elif isinstance(body, (bytes, bytearray)):
            self._body = body
        else:
            try:
                self._body = body = payload.PAYLOAD_REGISTRY.get(body)
            except payload.LookupError:
                raise ValueError("Unsupported body type %r" % type(body))

            headers = self._headers

            # set content-type
            if hdrs.CONTENT_TYPE not in headers:
                headers[hdrs.CONTENT_TYPE] = body.content_type

            # copy payload headers
            if body.headers:
                for key, value in body.headers.items():
                    if key not in headers:
                        headers[key] = value

        self._compressed_body = None
```

## text  (aiohttp/web_response.py L645-654)
```
    def text(self, text: str) -> None:
        assert isinstance(text, str), "text argument must be str (%r)" % type(text)

        if self.content_type == "application/octet-stream":
            self.content_type = "text/plain"
        if self.charset is None:
            self.charset = "utf-8"

        self._body = text.encode(self.charset)
        self._compressed_body = None
```

## decode_iter  (aiohttp/multipart.py L524-538)
```
    async def decode_iter(self, data: bytes) -> AsyncIterator[bytes]:
        """Async generator that yields decoded data chunks.

        Decodes data according the specified Content-Encoding
        or Content-Transfer-Encoding headers value.

        This method offloads decompression to an executor for large payloads
        to avoid blocking the event loop.
        """
        data = self._apply_content_transfer_decoding(data)
        if self._needs_content_decoding():
            async for d in self._decode_content_async(data):
                yield d
        else:
            yield data
```

## read_chunk  (aiohttp/multipart.py L324-366)
```
    async def read_chunk(self, size: int = chunk_size) -> bytes:
        """Reads body part content chunk of the specified size.

        size: chunk size
        """
        if self._at_eof:
            return b""
        if self._length:
            chunk = await self._read_chunk_from_length(size)
        else:
            chunk = await self._read_chunk_from_stream(size)

        # For the case of base64 data, we must read a fragment of size with a
        # remainder of 0 by dividing by 4 for string without symbols \n or \r
        encoding = self.headers.get(CONTENT_TRANSFER_ENCODING)
        if encoding and encoding.lower() == "base64":
            stripped_chunk = b"".join(chunk.split())
            remainder = len(stripped_chunk) % 4

            while remainder != 0 and not self.at_eof():
                over_chunk_size = 4 - remainder
                over_chunk = b""

                if self._prev_chunk:
                    over_chunk = self._prev_chunk[:over_chunk_size]
                    self._prev_chunk = self._prev_chunk[len(over_chunk) :]

                if len(over_chunk) != over_chunk_size:
                    over_chunk += await self._content.read(4 - len(over_chunk))

                if not over_chunk:
                    self._at_eof = True

                stripped_chunk += b"".join(over_chunk.split())
                chunk += over_chunk
                remainder = len(stripped_chunk) % 4

        self._read_bytes += len(chunk)
        if self._read_bytes == self._length:
            self._at_eof = True
        if self._at_eof and await self._content.readline() != b"\r\n":
            raise ValueError("Reader did not read all the data or it is malformed")
        return chunk
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

## _close  (aiohttp/payload.py L307-321)
```
    def _close(self) -> None:
        """
        Async safe synchronous close operations for backwards compatibility.

        This method exists only for backwards compatibility with code that
        needs to clean up payloads synchronously. In the future, we will
        drop this method and only support the async close() method.

        WARNING: This method must be safe to call from within the event loop
        without blocking. Subclasses should not perform any blocking I/O here.

        WARNING: This method must be called from within an event loop for
        certain payload types (e.g., IOBasePayload). Calling it outside an
        event loop may raise RuntimeError.
        """
```

## _create_response  (aiohttp/client_reqrep.py L832-844)
```
    def _create_response(self, task: asyncio.Task[None] | None) -> ClientResponse:
        return self.response_class(
            self.method,
            self.original_url,
            writer=task,
            continue100=None,
            timer=TimerNoop(),
            traces=(),
            loop=self.loop,
            session=None,
            request_headers=self.headers,
            original_url=self.original_url,
        )
```

## _create_writer  (aiohttp/client_reqrep.py L846-847)
```
    def _create_writer(self, protocol: BaseProtocol) -> StreamWriter:
        return StreamWriter(protocol, self.loop)
```

## _on_chunk_request_sent  (aiohttp/client_reqrep.py L1426-1428)
```
    async def _on_chunk_request_sent(self, method: str, url: URL, chunk: bytes) -> None:
        for trace in self._traces:
            await trace.send_request_chunk_sent(method, url, chunk)
```

## _on_headers_request_sent  (aiohttp/client_reqrep.py L1430-1434)
```
    async def _on_headers_request_sent(
        self, method: str, url: URL, headers: "CIMultiDict[str]"
    ) -> None:
        for trace in self._traces:
            await trace.send_request_headers(method, url, headers)
```

## _should_write  (aiohttp/client_reqrep.py L849-850)
```
    def _should_write(self, protocol: BaseProtocol) -> bool:
        return protocol.writing_paused
```

## _terminate  (aiohttp/client_reqrep.py L1419-1424)
```
    def _terminate(self) -> None:
        if self._writer_task is not None:
            if not self.loop.is_closed():
                self._writer_task.cancel()
            self._writer_task.remove_done_callback(self._reset_writer)
            self._writer_task = None
```

## _update_auto_headers  (aiohttp/client_reqrep.py L1066-1083)
```
    def _update_auto_headers(self, skip_auto_headers: Iterable[str] | None) -> None:
        if skip_auto_headers is not None:
            self._skip_auto_headers = CIMultiDict(
                (hdr, None) for hdr in sorted(skip_auto_headers)
            )
            used_headers = self.headers.copy()
            used_headers.extend(self._skip_auto_headers)  # type: ignore[arg-type]
        else:
            # Fast path when there are no headers to skip
            # which is the most common case.
            used_headers = self.headers

        for hdr, val in self.DEFAULT_HEADERS.items():
            if hdr not in used_headers:
                self.headers[hdr] = val

        if hdrs.USER_AGENT not in used_headers:
            self.headers[hdrs.USER_AGENT] = SERVER_SOFTWARE
```

## _update_body  (aiohttp/client_reqrep.py L1182-1197)
```
    def _update_body(self, body: Any) -> None:
        """Update request body after its already been set."""
        # Remove existing Content-Length header since body is changing
        if hdrs.CONTENT_LENGTH in self.headers:
            del self.headers[hdrs.CONTENT_LENGTH]

        # Remove existing Transfer-Encoding header to avoid conflicts
        if self.chunked and hdrs.TRANSFER_ENCODING in self.headers:
            del self.headers[hdrs.TRANSFER_ENCODING]

        # Now update the body using the existing method
        self._update_body_from_data(body)

        # Update transfer encoding headers if needed (same logic as __init__)
        if body is not None or self.method not in self.GET_METHODS:
            self._update_transfer_encoding()
```

## _update_content_encoding  (aiohttp/client_reqrep.py L1102-1116)
```
    def _update_content_encoding(self, data: Any, compress: bool | str) -> None:
        """Set request content encoding."""
        self.compress = None
        if not data:
            return

        if self.headers.get(hdrs.CONTENT_ENCODING):
            if compress:
                raise ValueError(
                    "compress can not be set if Content-Encoding header is set"
                )
        elif compress:
            self.compress = compress if isinstance(compress, str) else "deflate"
            self.headers[hdrs.CONTENT_ENCODING] = self.compress
            self.chunked = True  # enable chunked, no need to deal with length
```

## _update_cookies  (aiohttp/client_reqrep.py L1085-1100)
```
    def _update_cookies(self, cookies: BaseCookie[str]) -> None:
        """Update request cookies header."""
        if not cookies:
            return

        c = SimpleCookie()
        if hdrs.COOKIE in self.headers:
            # parse_cookie_header for RFC 6265 compliant Cookie header parsing
            c.update(parse_cookie_header(self.headers.get(hdrs.COOKIE, "")))
            del self.headers[hdrs.COOKIE]

        for name, value in cookies.items():
            # Use helper to preserve coded_value exactly as sent by server
            c[name] = preserve_morsel_with_coded_value(value)

        self.headers[hdrs.COOKIE] = c.output(header="", sep=";").strip()
```

## _update_expect_continue  (aiohttp/client_reqrep.py L1261-1271)
```
    def _update_expect_continue(self, expect: bool = False) -> None:
        if expect:
            self.headers[hdrs.EXPECT] = "100-continue"
        elif (
            hdrs.EXPECT in self.headers
            and self.headers[hdrs.EXPECT].lower() == "100-continue"
        ):
            expect = True

        if expect:
            self._continue = self.loop.create_future()
```

## _update_proxy  (aiohttp/client_reqrep.py L1273-1288)
```
    def _update_proxy(
        self,
        proxy: URL | None,
        proxy_auth: BasicAuth | None,
        proxy_headers: CIMultiDict[str] | None,
    ) -> None:
        self.proxy = proxy
        if proxy is None:
            self.proxy_auth = None
            self.proxy_headers = None
            return

        if proxy_auth and not isinstance(proxy_auth, BasicAuth):
            raise ValueError("proxy_auth must be None or BasicAuth() tuple")
        self.proxy_auth = proxy_auth
        self.proxy_headers = proxy_headers
```

## _update_transfer_encoding  (aiohttp/client_reqrep.py L1118-1135)
```
    def _update_transfer_encoding(self) -> None:
        """Analyze transfer-encoding header."""
... (truncated)
```
--- END SOURCE SNIPPETS ---

QUESTION: If a handler reads incoming data from different body formats, what does the request object actually do for JSON, URL-encoded forms, and multipart uploads, and where are payload limits enforced?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
