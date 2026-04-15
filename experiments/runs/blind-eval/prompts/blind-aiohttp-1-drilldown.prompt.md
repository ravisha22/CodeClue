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
read (aiohttp/multipart.py:304-322)
  Reads body part data.
  behavior: ACCUMULATE(loop -> data)
  calls: decode_iter, read_chunk
  called_by: _read_chunk_from_length, _read_chunk_from_stream, form, json, read_chunk, text, BodyPartReader

update_body (aiohttp/client_reqrep.py:1199-1259)
  Update request body and close previous payload if needed.
  sig: update_body(body)
  calls: _update_body, close

_update_body_from_data (aiohttp/client_reqrep.py:1137-1180)
  Update request body from data.
  sig: _update_body_from_data(body)
  behavior: BRANCH(isinstance_FormData -> result, else -> result); ACCUMULATE(loop -> result)
  calls: body
  called_by: _update_body, ClientRequest
  uses: FormData (formdata)

json (aiohttp/multipart.py:467-473)
  Like read(), but assumes that body parts contains JSON data.
  calls: get_charset, read

BodyPartReader (aiohttp/multipart.py:257-599)
  Multipart reader for single body part.
  attrs: chunk_size=8192
  imports: base64, binascii, uuid, warnings, types
  calls: _apply_content_transfer_decoding, _decode_content, _decode_content_async, _decode_content_transfer, _needs_content_decoding, _read_chunk_from_length, _read_chunk_from_stream, decode_iter
  raises: RuntimeError, StopAsyncIteration, ValueError
  uses: ZLibDecompressor (compression_utils), CIMultiDict (multidict)

MultipartReader (aiohttp/multipart.py:639-854)
  Multipart body reader.
  imports: base64, binascii, uuid, warnings, types
  calls: read_chunk, readline, _get_boundary, _get_part_reader, _maybe_release_last_part, _read_boundary, _read_headers, _read_until_first_boundary
  raises: ValueError, StopAsyncIteration, BadHttpMessage, RuntimeError
  uses: HeadersParser (http), BadHttpMessage (http_exceptions), CIMultiDict (multidict)

MultipartWriter (aiohttp/multipart.py:860-1146)
  Multipart body writer.
  extends: Payload
  imports: base64, binascii, uuid, warnings, types
  calls: enable_compression, enable_encoding, write_eof, MultipartPayloadWriter, append, append_payload, close
  raises: ValueError, RuntimeError, TypeError
  uses: ZLibCompressor (compression_utils), CIMultiDict (multidict)

append_payload (aiohttp/multipart.py:963-999)
  Adds a new body part to multipart writer.
  sig: append_payload(payload)
  behavior: BRANCH(is_form_data -> result, else -> raise_RuntimeError)
  calls: append
  called_by: append, append_form, append_json, MultipartWriter
  raises: RuntimeError

read_chunk (aiohttp/multipart.py:324-366)
  Reads body part content chunk of the specified size.
  sig: read_chunk(size)
  behavior: BRANCH(length -> result, else -> result)
  calls: _read_chunk_from_length, _read_chunk_from_stream, read, readline
  called_by: read, BodyPartReader, BodyPartReaderPayload, MultipartReader
  raises: ValueError

readline (aiohttp/multipart.py:423-450)
  Reads body part by line by line.
  behavior: BRANCH(unread -> result, else -> result)
  calls: append
  called_by: read_chunk, BodyPartReader, _read_headers, _readline, MultipartReader

start (aiohttp/web_protocol.py:572-709)
  Process incoming request.
  behavior: ACCUMULATE(loop -> manager_requests_count)
  calls: _handle_request, _make_error_handler, close, force_close, log_debug, log_exception
  called_by: connection_made, RequestHandler
  uses: StreamWriter (http)

_update_body (aiohttp/client_reqrep.py:1182-1197)
  Update request body after its already been set.
  sig: _update_body(body)
  calls: _update_body_from_data, _update_transfer_encoding
  called_by: update_body, ClientRequest

strip_auth_from_url (aiohttp/helpers.py:184-190)
  Remove user and password from URL if present and return BasicAuth object.
  sig: strip_auth_from_url(url)
  calls: BasicAuth
  called_by: proxies_from_env

read (aiohttp/web_request.py:624-643)
  Read request body if present.
  called_by: post, text, BaseRequest
  raises: HTTPRequestEntityTooLarge
  uses: HTTPRequestEntityTooLarge (web_exceptions)

_gen_form_data (aiohttp/formdata.py:128-161)
  Encode a list of fields using the multipart/form-data MIME format
  behavior: ACCUMULATE(loop -> result)
  called_by: __call__, FormData
  raises: TypeError

multipart (aiohttp/web_request.py:673-680)
  Return async iterator to process BODY as multipart.
  behavior: DELEGATE(MultipartReader -> result)
  called_by: post, BaseRequest
  uses: MultipartReader (multipart)

BodyPartReaderPayload (aiohttp/multipart.py:603-636)
  extends: Payload
  imports: base64, binascii, uuid, warnings, types
  calls: decode_iter, read_chunk
  raises: TypeError

form (aiohttp/multipart.py:475-493)
  Like read(), but assumes that body parts contain form urlencoded data.
  behavior: BRANCH(encoding -> result, else -> result)
  calls: get_charset, read
  raises: ValueError

text (aiohttp/multipart.py:459-465)
  Like read(), but assumes that body part contains text data.
  calls: get_charset, read

JsonBytesPayload (aiohttp/payload.py:943-963)
  JSON payload for encoders that return bytes directly.
  extends: BytesPayload
  imports: asyncio, enum, io, mimetypes, warnings

JsonPayload (aiohttp/payload.py:924-940)
  extends: BytesPayload
  imports: asyncio, enum, io, mimetypes, warnings

LookupError (aiohttp/payload.py:50-51)
  Raised when no payload factory is found for the given data type.
  extends: Exception
  imports: asyncio, enum, io, mimetypes, warnings
  called_by: get, PayloadRegistry

MultipartPayloadWriter (aiohttp/multipart.py:1149-1204)
  imports: base64, binascii, uuid, warnings, types
  called_by: MultipartWriter

_load_json_data (aiohttp/cookiejar.py:164-195)
  Load cookies from parsed JSON data.
  sig: _load_json_data(data)
  behavior: ACCUMULATE(loop -> result)
  called_by: load, CookieJar
  uses: Morsel (http.cookies)

_read (aiohttp/payload.py:510-526)
  Read a chunk of data from the file-like object.
  sig: _read(remaining_content_len)
  behavior: DELEGATE(_value.read -> result)

_read (aiohttp/payload.py:779-798)
  Read a chunk of data from the text file-like object.
  sig: _read(remaining_content_len)

_write_bytes (aiohttp/client_reqrep.py:1332-1405)
  Write the request body to the connection stream.
  sig: _write_bytes(writer, conn, content_length)
  uses: ClientOSError (client_exceptions), ClientConnectionError (client_exceptions)

as_bytes (aiohttp/multipart.py:1067-1092)
  Return bytes representation of the multipart data.
  sig: as_bytes(encoding, errors)
  behavior: ACCUMULATE(loop -> parts)

body_exists (aiohttp/web_request.py:612-614)
  Return True if request has HTTP BODY, False otherwise.

build_client_middlewares (aiohttp/client_middlewares.py:18-55)
  Apply middlewares to request handler.
  sig: build_client_middlewares(handler, middlewares)
  behavior: ACCUMULATE(loop -> result); UNWIND(reversed)
  calls: make_wrapper

can_read_body (aiohttp/web_request.py:607-609)
  Return True if request's HTTP BODY can be read, False otherwise.

decode (aiohttp/multipart.py:1052-1065)
  Return string representation of the multipart data.
  sig: decode(encoding, errors)
  behavior: DELEGATE(join -> result)

handle_json_data (examples/logging_middleware.py:78-84)
  Endpoint that echoes JSON data.
  sig: handle_json_data(request)

handler (aiohttp/abc.py:55-56)
  Execute matched request handler

json (aiohttp/_websocket/models.py:70-72)
  Return parsed JSON data.
  behavior: DELEGATE(loads -> result)

json (aiohttp/web_request.py:654-671)
  Return BODY as JSON.
  calls: text
  raises: HTTPBadRequest
  uses: HTTPBadRequest (web_exceptions)

json (aiohttp/_websocket/models.py:55-59)
  Return parsed JSON data.
  behavior: DELEGATE(loads -> result)

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 25 with behavior annotations
drill: aiohttp/client_reqrep.py (~72 lines, _write_bytes)
drill: aiohttp/_websocket/writer.py (~71 lines, send_frame)
drill: aiohttp/client_reqrep.py (~65 lines, update_body)
drill: aiohttp/http_writer.py (~43 lines, write)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## _write_bytes  (aiohttp/client_reqrep.py L920-927)
```
    async def _write_bytes(
        self,
        writer: AbstractStreamWriter,
        conn: "Connection",
        content_length: int | None,
    ) -> None:
        # Base class never has a body, this will never be run.
        assert False
```

## send_frame  (aiohttp/web_ws.py L452-460)
```
    async def send_frame(
        self, message: bytes, opcode: WSMsgType, compress: int | None = None
    ) -> None:
        """Send a frame over the websocket."""
        if self._writer is None:
            raise RuntimeError("Call .prepare() first")
        await self._writer.send_frame(message, opcode, compress)

    async def send_str(self, data: str, compress: int | None = None) -> None:
```

## update_body  (aiohttp/client_reqrep.py L1199-1259)
```
    async def update_body(self, body: Any) -> None:
        """
        Update request body and close previous payload if needed.

        This method safely updates the request body by first closing any existing
        payload to prevent resource leaks, then setting the new body.

        IMPORTANT: Always use this method instead of setting request.body directly.
        Direct assignment to request.body will leak resources if the previous body
        contains file handles, streams, or other resources that need cleanup.

        Args:
            body: The new body content. Can be:
                - bytes/bytearray: Raw binary data
                - str: Text data (will be encoded using charset from Content-Type)
                - FormData: Form data that will be encoded as multipart/form-data
                - Payload: A pre-configured payload object
                - AsyncIterable: An async iterable of bytes chunks
                - File-like object: Will be read and sent as binary data
                - None: Clears the body

        Usage:
            # CORRECT: Use update_body
            await request.update_body(b"new request data")

            # WRONG: Don't set body directly
            # request.body = b"new request data"  # This will leak resources!

            # Update with form data
            form_data = FormData()
            form_data.add_field('field', 'value')
            await request.update_body(form_data)

            # Clear body
            await request.update_body(None)

        Note:
            This method is async because it may need to close file handles or
            other resources associated with the previous payload. Always await
            this method to ensure proper cleanup.

        Warning:
            Setting request.body directly is highly discouraged and can lead to:
            - Resource leaks (unclosed file handles, streams)
            - Memory leaks (unreleased buffers)
            - Unexpected behavior with streaming payloads

            It is not recommended to change the payload type in middleware. If the
            body was already set (e.g., as bytes), it's best to keep the same type
            rather than converting it (e.g., to str) as this may result in unexpected
            behavior.

        See Also:
            - update_body_from_data: Synchronous body update without cleanup
            - body property: Direct body access (STRONGLY DISCOURAGED)

        """
        # Close existing payload if it exists and needs closing
        if self._body is not None:
            await self._body.close()
        self._update_body(body)
```

## write  (tests/test_payload.py L1027-1030)
```
        async def write(self, writer: AbstractStreamWriter) -> None:
            """Write implementation is a no-op."""

    # Create instance with specific encoding
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

## close  (tests/test_web_functional.py L2071-2074)
```
        async def close(self) -> None:
            assert False

        async def resolve(
```

## HttpVersion  (aiohttp/http_writer.py L39-41)
```
class HttpVersion(NamedTuple):
    major: int
    minor: int
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

## _send_headers_with_payload  (aiohttp/http_writer.py L131-165)
```
    def _send_headers_with_payload(
        self,
        chunk: Union[bytes, bytearray, "memoryview[int]", "memoryview[bytes]"],
        is_eof: bool,
    ) -> None:
        """Send buffered headers with payload, coalescing into single write."""
        # Mark headers as written
        self._headers_written = True
        headers_buf = self._headers_buf
        self._headers_buf = None

        if TYPE_CHECKING:
            # Safe because callers (write() and write_eof()) only invoke this method
            # after checking that self._headers_buf is truthy
            assert headers_buf is not None

        if not self.chunked:
            # Non-chunked: coalesce headers with body
            if chunk:
                self._writelines((headers_buf, chunk))
            else:
                self._write(headers_buf)
            return

        # Coalesce headers with chunked data
        if chunk:
            chunk_len_pre = f"{len(chunk):x}\r\n".encode("ascii")
            if is_eof:
                self._writelines((headers_buf, chunk_len_pre, chunk, b"\r\n0\r\n\r\n"))
            else:
                self._writelines((headers_buf, chunk_len_pre, chunk, b"\r\n"))
        elif is_eof:
            self._writelines((headers_buf, b"0\r\n\r\n"))
        else:
            self._write(headers_buf)
```

## _write  (aiohttp/http_writer.py L94-103)
```
    def _write(
        self, chunk: Union[bytes, bytearray, "memoryview[int]", "memoryview[bytes]"]
    ) -> None:
        size = len(chunk)
        self.buffer_size += size
        self.output_size += size
        transport = self._protocol.transport
        if transport is None or transport.is_closing():
            raise ClientConnectionResetError("Cannot write to closing transport")
        transport.write(chunk)
```

## _write_chunked_payload  (aiohttp/http_writer.py L124-129)
```
    def _write_chunked_payload(
        self, chunk: Union[bytes, bytearray, "memoryview[int]", "memoryview[bytes]"]
    ) -> None:
        """Write a chunk with proper chunked encoding."""
        chunk_len_pre = f"{len(chunk):x}\r\n".encode("ascii")
        self._writelines((chunk_len_pre, chunk, b"\r\n"))
```

## _writelines  (aiohttp/http_writer.py L105-122)
```
    def _writelines(
        self,
        chunks: Iterable[
            Union[bytes, bytearray, "memoryview[int]", "memoryview[bytes]"]
        ],
    ) -> None:
        size = 0
        for chunk in chunks:
            size += len(chunk)
        self.buffer_size += size
        self.output_size += size
        transport = self._protocol.transport
        if transport is None or transport.is_closing():
            raise ClientConnectionResetError("Cannot write to closing transport")
        if SKIP_WRITELINES or size < MIN_PAYLOAD_FOR_WRITELINES:
            transport.write(b"".join(chunks))
        else:
            transport.writelines(chunks)
```

## drain  (tests/test_payload.py L183-185)
```
    async def drain(self) -> None:
        """Drain implementation - no-op for tests."""

```

## enable_chunking  (tests/test_payload.py L191-193)
```
    def enable_chunking(self) -> None:
        """Enable chunking - no-op for tests."""

```

## enable_compression  (tests/test_payload.py L186-190)
```
    def enable_compression(
        self, encoding: str = "deflate", strategy: int | None = None
    ) -> None:
        """Enable compression - no-op for tests."""

```

## protocol  (tests/test_websocket_writer.py L18-20)
```
def protocol() -> mock.Mock:
    ret = mock.create_autospec(BaseProtocol, spec_set=True, instance=True)
... (truncated)
```
--- END SOURCE SNIPPETS ---

QUESTION: If a handler reads incoming data from different body formats, what does the request object actually do for JSON, URL-encoded forms, and multipart uploads, and where are payload limits enforced?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
