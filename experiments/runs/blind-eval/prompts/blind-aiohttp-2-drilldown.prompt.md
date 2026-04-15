# Blind Evaluation Prompt - MRLF v2.1 with File 2 Drill-Down
# Task: blind-aiohttp-2

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

--- CLUE FILE (File 1) ---
=CC v2.1 aiohttp@HEAD 166mod 6741sym
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
_cleanup_server (aiohttp/web_runner.py:337-338)
  Run any cleanup steps after the server is shutdown.

_cleanup_server (aiohttp/web_runner.py:452-453)

_cleanup_server (aiohttp/web_runner.py:376-377)

shutdown (aiohttp/web_runner.py:302-303)
  Call any shutdown hooks to help server close gracefully.

Application (aiohttp/web_app.py:71-400)
  imports: asyncio, logging, warnings, aiosignal, frozenlist
  calls: _add_subapp, _check_frozen, _prepare_middleware, handler, reg_handler, _reg_subapp_signals, add_routes, freeze
  raises: TypeError, RuntimeError, ValueError

TestServer (examples/token_refresh_middleware.py:121-243)
  Test server with JWT-like token authentication.
  imports: asyncio, hashlib, logging, secrets, http
  calls: _process_token_refresh, generate_access_token, verify_bearer_token
  called_by: run_test_server

_on_cleanup (aiohttp/web_app.py:430-441)
  sig: _on_cleanup(app)
  behavior: ACCUMULATE(loop -> errors); UNWIND(reversed)
  calls: CleanupError
  called_by: cleanup, Application
  raises: CleanupError

_cleanup_writer (aiohttp/client_reqrep.py:563-566)
  called_by: __del__, _response_eof, close, release, ClientResponse

run_test_server (examples/token_refresh_middleware.py:246-258)
  Run a test server with JWT auth endpoints.
  calls: TestServer
  called_by: main

CleanupContext (aiohttp/web_app.py:415-441)
  imports: asyncio, logging, warnings, aiosignal, frozenlist
  calls: CleanupError
  called_by: Application
  raises: CleanupError

ResourcesView (aiohttp/web_urldispatcher.py:934-945)
  extends: Sized
  imports: asyncio, base64, hashlib, html, inspect
  called_by: resources, UrlDispatcher

resources (aiohttp/web_urldispatcher.py:1029-1030)
  behavior: DELEGATE(ResourcesView -> result)
  calls: ResourcesView
  called_by: _add_prefix_to_resources, PrefixedSubAppResource

cleanup (aiohttp/web_runner.py:305-330)
  behavior: ACCUMULATE(loop -> result)
  calls: stop
  called_by: AppRunner

_add_prefix_to_resources (aiohttp/web_urldispatcher.py:717-724)
  sig: _add_prefix_to_resources(prefix)
  behavior: ACCUMULATE(loop -> result)
  calls: index_resource, resources, unindex_resource
  called_by: PrefixedSubAppResource

run_test_server (examples/retry_middleware.py:150-164)
  Run a simple test server.
  calls: TestServer
  called_by: main

run_test_server (examples/combined_middleware.py:238-252)
  Run a test server with various endpoints.
  calls: TestServer
  called_by: main

run_test_server (examples/basic_auth_middleware.py:119-131)
  Run a simple test server with basic auth endpoints.
  calls: TestServer
  called_by: main

run_test_server (examples/logging_middleware.py:87-102)
  Run a simple test server.
  calls: TestServer
  called_by: main

CleanupError (aiohttp/web_app.py:403-406)
  extends: RuntimeError
  imports: asyncio, logging, warnings, aiosignal, frozenlist
  called_by: _on_cleanup, CleanupContext

AiohttpRawServer (aiohttp/pytest_plugin.py:57-64)
  extends: Protocol
  imports: asyncio, inspect, warnings, pytest, test_utils

AiohttpServer (aiohttp/pytest_plugin.py:51-54)
  extends: Protocol
  imports: asyncio, inspect, warnings, pytest, test_utils

AppKey (aiohttp/helpers.py:890-891)
  Keys for static typing support in Application.
  imports: asyncio, base64, binascii, enum, inspect

AppRunner (aiohttp/web_runner.py:380-453)
  Web Application runner
  imports: asyncio, signal, socket, yarl, http_parser
  calls: cleanup
  raises: TypeError

HTTPInternalServerError (aiohttp/web_exceptions.py:463-464)
  extends: HTTPServerError
  attrs: status_code=500
  imports: warnings, http, multidict, yarl, helpers

NotAppKeyWarning (aiohttp/web_exceptions.py:75-76)
  Warning when not using AppKey in Application.
  extends: UserWarning
  imports: warnings, http, multidict, yarl, helpers

Server (aiohttp/web_server.py:30-126)
  imports: asyncio, warnings, http_parser, streams, web_protocol
  calls: shutdown

ServerConnectionError (aiohttp/client_exceptions.py:212-213)
  Server connection errors.
  extends: ClientConnectionError
  imports: asyncio, multidict, typedefs, ssl, client_reqrep

ServerDisconnectedError (aiohttp/client_exceptions.py:216-224)
  Server disconnected.
  extends: ServerConnectionError
  imports: asyncio, multidict, typedefs, ssl, client_reqrep

ServerRunner (aiohttp/web_runner.py:355-377)
  Low-level web server runner
  imports: asyncio, signal, socket, yarl, http_parser

ServerTimeoutError (aiohttp/client_exceptions.py:227-228)
  Server timeout error.
  extends: ServerConnectionError, TimeoutError
  imports: asyncio, multidict, typedefs, ssl, client_reqrep

TestServer (examples/retry_middleware.py:91-147)
  Test server with stateful endpoints for retry testing.
  imports: asyncio, logging, http, aiohttp
  called_by: run_test_server

TestServer (examples/basic_auth_middleware.py:59-116)
  Test server for basic auth endpoints.
  imports: asyncio, base64, binascii, logging, aiohttp
  called_by: run_test_server

TestServer (examples/logging_middleware.py:59-84)
  Test server for logging middleware demo.
  imports: asyncio, logging, aiohttp
  called_by: run_test_server

TestServer (examples/combined_middleware.py:159-235)
  Test server with stateful endpoints for middleware testing.
  imports: asyncio, base64, binascii, logging, http
  called_by: run_test_server

WSServerHandshakeError (aiohttp/client_exceptions.py:106-107)
  websocket server handshake error.
  extends: ClientResponseError
  imports: asyncio, multidict, typedefs, ssl, client_reqrep

_cleanup (aiohttp/connector.py:380-417)
  Cleanup unused transports.

_create_ssl_context (aiohttp/worker.py:205-220)
  Creates SSLContext instance for usage in asyncio.create_server.
  sig: _create_ssl_context(cfg)
  called_by: _run, GunicornWebWorker
  raises: RuntimeError

_make_server (aiohttp/web_runner.py:333-334)
  Return a new server for the runner to serve requests.

_make_server (aiohttp/web_runner.py:373-374)

_make_server (aiohttp/web_runner.py:421-430)
  behavior: DELEGATE(Server -> result)
  uses: Server (web_server)

_on_startup (aiohttp/web_app.py:420-428)
  sig: _on_startup(app)
  behavior: ACCUMULATE(loop -> exits)

add_app (aiohttp/abc.py:84-85)
  Add application to the nested apps stack.
  sig: add_app(app)

aiohttp_raw_server (aiohttp/pytest_plugin.py:325-349)
  Factory to create a RawTestServer instance, given a web handler.
  sig: aiohttp_raw_server(loop)
  uses: RawTestServer (test_utils)

aiohttp_server (aiohttp/pytest_plugin.py:296-321)
  Factory to create a TestServer instance, given an app.
  sig: aiohttp_server(loop)
  uses: TestServer (test_utils)

app (aiohttp/web_request.py:862-866)
  Application instance.

cleanup (aiohttp/web_app.py:351-360)
  Causes on_cleanup signal
  behavior: BRANCH(on_cleanup.frozen -> result, else -> result)
  calls: _on_cleanup

cleanup_ctx (aiohttp/web_app.py:326-327)

close (aiohttp/payload.py:325-335)
  Close the payload if it holds any resources.

close (aiohttp/payload.py:681-689)
  Close the payload if it holds any resources.

iter_chunks (aiohttp/streams.py:84-90)
  Yield chunks of data as they are received by the server.
  behavior: DELEGATE(ChunkTupleAsyncStreamIterator -> result)
  calls: ChunkTupleAsyncStreamIterator

named_resources (aiohttp/web_urldispatcher.py:1035-1036)
  behavior: DELEGATE(MappingProxyType -> result)
  uses: MappingProxyType (types)

on_cleanup (aiohttp/web_app.py:322-323)

on_shutdown (aiohttp/web_app.py:318-319)

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 13 with behavior annotations
drill: examples/token_refresh_middleware.py (~39 lines, _process_token_refresh)
drill: aiohttp/connector.py (~35 lines, _cleanup)
drill: aiohttp/_cookie_helpers.py (~29 lines, preserve_morsel_with_coded_value)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## _process_token_refresh  (examples/token_refresh_middleware.py L139-181)
```
    async def _process_token_refresh(self, data: dict[str, str]) -> web.Response:
        """Process the token refresh request."""
        refresh_token = data.get("refresh_token")

        if not refresh_token:
            return web.json_response({"error": "refresh_token required"}, status=400)

        # Hash the refresh token to look it up
        refresh_token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()

        if refresh_token_hash not in self.refresh_tokens_db:
            return web.json_response({"error": "Invalid refresh token"}, status=401)

        user_data = self.refresh_tokens_db[refresh_token_hash]

        # Generate new access token
        access_token = self.generate_access_token()
        expires_in = 300  # 5 minutes for demo

        # Store the access token with expiry
        token_hash = hashlib.sha256(access_token.encode()).hexdigest()
        self.tokens_db[token_hash] = {
            "user_id": user_data["user_id"],
            "username": user_data["username"],
            "expires_at": time.time() + expires_in,
            "issued_at": time.time(),
        }

        # Clean up expired tokens periodically
        current_time = time.time()
        self.tokens_db = {
            k: v
            for k, v in self.tokens_db.items()
            if isinstance(v["expires_at"], float) and v["expires_at"] > current_time
        }

        return web.json_response(
            {
                "access_token": access_token,
                "token_type": "Bearer",
                "expires_in": expires_in,
            }
        )
```

## _cleanup  (aiohttp/connector.py L380-417)
```
    def _cleanup(self) -> None:
        """Cleanup unused transports."""
        if self._cleanup_handle:
            self._cleanup_handle.cancel()
            # _cleanup_handle should be unset, otherwise _release() will not
            # recreate it ever!
            self._cleanup_handle = None

        now = monotonic()
        timeout = self._keepalive_timeout

        if self._conns:
            connections = defaultdict(deque)
            deadline = now - timeout
            for key, conns in self._conns.items():
                alive: deque[tuple[ResponseHandler, float]] = deque()
                for proto, use_time in conns:
                    if proto.is_connected() and use_time - deadline >= 0:
                        alive.append((proto, use_time))
                        continue
                    transport = proto.transport
                    proto.close()
                    if not self._cleanup_closed_disabled and key.is_ssl:
                        self._cleanup_closed_transports.append(transport)

                if alive:
                    connections[key] = alive

            self._conns = connections

        if self._conns:
            self._cleanup_handle = helpers.weakref_handle(
                self,
                "_cleanup",
                timeout,
                self._loop,
                timeout_ceil_threshold=self._timeout_ceil_threshold,
            )
```

## preserve_morsel_with_coded_value  (aiohttp/_cookie_helpers.py L85-112)
```
def preserve_morsel_with_coded_value(cookie: Morsel[str]) -> Morsel[str]:
    """
    Preserve a Morsel's coded_value exactly as received from the server.

    This function ensures that cookie encoding is preserved exactly as sent by
    the server, which is critical for compatibility with old servers that have
    strict requirements about cookie formats.

    This addresses the issue described in https://github.com/aio-libs/aiohttp/pull/1453
    where Python's SimpleCookie would re-encode cookies, breaking authentication
    with certain servers.

    Args:
        cookie: A Morsel object from SimpleCookie

    Returns:
        A Morsel object with preserved coded_value

    """
    mrsl_val = cast("Morsel[str]", cookie.get(cookie.key, Morsel()))
    # We use __setstate__ instead of the public set() API because it allows us to
    # bypass validation and set already validated state. This is more stable than
    # setting protected attributes directly and unlikely to change since it would
    # break pickling.
    mrsl_val.__setstate__(  # type: ignore[attr-defined]
        {"key": cookie.key, "value": cookie.value, "coded_value": cookie.coded_value}
    )
    return mrsl_val
```

## __aenter__  (aiohttp/test_utils.py L505-507)
```
    async def __aenter__(self) -> Self:
        await self.start_server()
        return self
```

## __aexit__  (aiohttp/test_utils.py L509-515)
```
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.close()
```

## __del__  (aiohttp/connector.py L130-143)
```
    def __del__(self, _warnings: Any = warnings) -> None:
        if self._protocol is not None:
            _warnings.warn(
                f"Unclosed connection {self!r}", ResourceWarning, source=self
            )
            if self._loop.is_closed():
                return

            self._connector._release(self._key, self._protocol, should_close=True)

            context = {"client_connection": self, "message": "Unclosed connection"}
            if self._source_traceback is not None:
                context["source_traceback"] = self._source_traceback
            self._loop.call_exception_handler(context)
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

## _available_connections  (aiohttp/connector.py L528-551)
```
    def _available_connections(self, key: "ConnectionKey") -> int:
        """
        Return number of available connections.

        The limit, limit_per_host and the connection key are taken into account.

        If it returns less than 1 means that there are no connections
        available.
        """
        # check total available connections
        # If there are no limits, this will always return 1
        total_remain = 1

        if self._limit and (total_remain := self._limit - len(self._acquired)) <= 0:
            return total_remain

        # check limit per host
        if host_remain := self._limit_per_host:
            if acquired := self._acquired_per_host.get(key):
                host_remain -= len(acquired)
            if total_remain > host_remain:
                return host_remain

        return total_remain
```

## _cleanup_closed  (aiohttp/connector.py L419-440)
```
    def _cleanup_closed(self) -> None:
        """Double confirmation for transport close.

        Some broken ssl servers may leave socket open without proper close.
        """
        if self._cleanup_closed_handle:
            self._cleanup_closed_handle.cancel()

        for transport in self._cleanup_closed_transports:
            if transport is not None:
                transport.abort()

        self._cleanup_closed_transports = []

        if not self._cleanup_closed_disabled:
            self._cleanup_closed_handle = helpers.weakref_handle(
                self,
                "_cleanup_closed",
                self._cleanup_closed_period,
                self._loop,
                timeout_ceil_threshold=self._timeout_ceil_threshold,
            )
```

## _close_immediately  (aiohttp/connector.py L1013-1025)
```
    def _close_immediately(self, *, abort_ssl: bool = False) -> list[Awaitable[object]]:
        for fut in chain.from_iterable(self._throttle_dns_futures.values()):
            fut.cancel()

        waiters = super()._close_immediately(abort_ssl=abort_ssl)

        for t in self._resolve_host_tasks:
            t.cancel()
            waiters.append(t)

        return waiters

    @property
```

## _create_connection  (tests/test_client_middleware.py L878-882)
```
        async def _create_connection(
            self, req: ClientRequest, traces: list["Trace"], timeout: "ClientTimeout"
        ) -> ResponseHandler:
            self.connection_attempts += 1
            return await super()._create_connection(req, traces, timeout)
```

## _get  (aiohttp/connector.py L678-718)
```
    async def _get(
        self, key: "ConnectionKey", traces: list["Trace"]
    ) -> Connection | None:
        """Get next reusable connection for the key or None.

        The connection will be marked as acquired.
        """
        if (conns := self._conns.get(key)) is None:
            return None

        t1 = monotonic()
        while conns:
            proto, t0 = conns.popleft()
            # We will we reuse the connection if its connected and
            # the keepalive timeout has not been exceeded
            if proto.is_connected() and t1 - t0 <= self._keepalive_timeout:
                if not conns:
... (truncated)
```
--- END SOURCE SNIPPETS ---

QUESTION: During application shutdown, how does the server unwind startup resources, and what happens if cleanup only partially initialized or multiple cleanup steps fail?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
