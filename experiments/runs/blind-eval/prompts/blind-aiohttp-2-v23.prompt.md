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

shutdown (aiohttp/web_server.py:111-114)
  sig: shutdown(timeout)
  called_by: Server

pre_shutdown (aiohttp/web_server.py:107-109)
  behavior: ACCUMULATE(self._connections loop -> result)

_make_server (aiohttp/web_runner.py:421-430)
  behavior: DELEGATE(Server -> result)
  uses: Server (web_server)

_on_cleanup (aiohttp/web_app.py:430-441)
  sig: _on_cleanup(app)
  behavior: ACCUMULATE(reversed(self._exits)... -> errors); UNWIND(reversed)
  calls: CleanupError
  called_by: cleanup, Application
  raises: CleanupError

resources (aiohttp/web_urldispatcher.py:1029-1030)
  behavior: DELEGATE(ResourcesView -> result)
  calls: ResourcesView
  called_by: _add_prefix_to_resources, PrefixedSubAppResource

_add_prefix_to_resources (aiohttp/web_urldispatcher.py:717-724)
  sig: _add_prefix_to_resources(prefix)
  behavior: ACCUMULATE(router.resources() loop -> result)
  calls: index_resource, resources, unindex_resource
  called_by: PrefixedSubAppResource

cleanup (aiohttp/web_app.py:351-360)
  Causes on_cleanup signal
  behavior: BRANCH(self.on_cleanup.frozen -> await self.on_cleanup..., else -> await sel...)
  calls: _on_cleanup

aiohttp_raw_server (aiohttp/pytest_plugin.py:325-349)
  Factory to create a RawTestServer instance, given a web handler.
  sig: aiohttp_raw_server(loop)
  uses: RawTestServer (test_utils)

aiohttp_server (aiohttp/pytest_plugin.py:296-321)
  Factory to create a TestServer instance, given an app.
  sig: aiohttp_server(loop)
  uses: TestServer (test_utils)

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

ResourcesView (aiohttp/web_urldispatcher.py:934-945)
  extends: Sized
  imports: asyncio, base64, hashlib, html, inspect
  called_by: resources, UrlDispatcher

Server (aiohttp/web_server.py:30-126)
  imports: asyncio, warnings, http_parser, streams, web_protocol
  calls: shutdown

TestServer (examples/basic_auth_middleware.py:59-116)
  Test server for basic auth endpoints.
  imports: asyncio, base64, binascii, logging, aiohttp
  called_by: run_test_server

TestServer (examples/combined_middleware.py:159-235)
  Test server with stateful endpoints for middleware testing.
  imports: asyncio, base64, binascii, logging, http
  called_by: run_test_server

TestServer (examples/logging_middleware.py:59-84)
  Test server for logging middleware demo.
  imports: asyncio, logging, aiohttp
  called_by: run_test_server

TestServer (examples/retry_middleware.py:91-147)
  Test server with stateful endpoints for retry testing.
  imports: asyncio, logging, http, aiohttp
  called_by: run_test_server

TestServer (examples/token_refresh_middleware.py:121-243)
  Test server with JWT-like token authentication.
  imports: asyncio, hashlib, logging, secrets, http
  calls: _process_token_refresh, generate_access_token, verify_bearer_token
  called_by: run_test_server

cleanup (aiohttp/web_runner.py:305-330)
  behavior: ACCUMULATE(list(self._sites) loop -> result)
  calls: stop
  called_by: AppRunner

run_test_server (examples/basic_auth_middleware.py:119-131)
  Run a simple test server with basic auth endpoints.
  calls: TestServer
  called_by: main

run_test_server (examples/combined_middleware.py:238-252)
  Run a test server with various endpoints.
  calls: TestServer
  called_by: main

run_test_server (examples/logging_middleware.py:87-102)
  Run a simple test server.
  calls: TestServer
  called_by: main

run_test_server (examples/retry_middleware.py:150-164)
  Run a simple test server.
  calls: TestServer
  called_by: main

run_test_server (examples/token_refresh_middleware.py:246-258)
  Run a test server with JWT auth endpoints.
  calls: TestServer
  called_by: main

AiohttpRawServer (aiohttp/pytest_plugin.py:57-64)
  extends: Protocol
  imports: asyncio, inspect, warnings, pytest, test_utils

AiohttpServer (aiohttp/pytest_plugin.py:51-54)
  extends: Protocol
  imports: asyncio, inspect, warnings, pytest, test_utils

HTTPInternalServerError (aiohttp/web_exceptions.py:463-464)
  extends: HTTPServerError
  attrs: status_code=500
  imports: warnings, http, multidict, yarl, helpers

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

_cleanup (aiohttp/connector.py:380-417)
  Cleanup unused transports.

_cleanup_writer (aiohttp/client_reqrep.py:563-566)
  called_by: __del__, _response_eof, close, release, ClientResponse

_make_server (aiohttp/web_runner.py:333-334)
  Return a new server for the runner to serve requests.

_make_server (aiohttp/web_runner.py:373-374)

_on_startup (aiohttp/web_app.py:420-428)
  sig: _on_startup(app)
  behavior: ACCUMULATE(self loop -> exits)

cleanup_ctx (aiohttp/web_app.py:326-327)

named_resources (aiohttp/web_urldispatcher.py:1035-1036)
  behavior: DELEGATE(MappingProxyType -> result)
  uses: MappingProxyType (types)

on_cleanup (aiohttp/web_app.py:322-323)

on_shutdown (aiohttp/web_app.py:318-319)

on_shutdown (examples/background_tasks.py:29-31)
  sig: on_shutdown(app)
  behavior: ACCUMULATE(app[websockets] loop -> result)

on_shutdown (examples/web_ws.py:49-51)
  sig: on_shutdown(app)
  behavior: ACCUMULATE(app[sockets] loop -> result)

on_startup (aiohttp/web_app.py:314-315)

server (aiohttp/web_runner.py:269-270)

shutdown (aiohttp/web_app.py:344-349)
  Causes on_shutdown signal

shutdown (aiohttp/web_runner.py:418-419)

shutdown (aiohttp/web_runner.py:370-371)

startup (aiohttp/web_app.py:337-342)
  Causes on_startup signal

WSServerHandshakeError (aiohttp/client_exceptions.py:106-107)
  websocket server handshake error.
  extends: ClientResponseError
  imports: asyncio, multidict, typedefs, ssl, client_reqrep

AppRunner (aiohttp/web_runner.py:380-453)
  Web Application runner
  imports: asyncio, signal, socket, yarl, http_parser
  calls: cleanup
  raises: TypeError

AppKey (aiohttp/helpers.py:890-891)
  Keys for static typing support in Application.
  imports: asyncio, base64, binascii, enum, inspect

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 15 with behavior annotations
uncovered: __call__, __init__, __init__, __init__
drill: aiohttp/web_runner.py (~2 lines, _cleanup_server)
drill: aiohttp/web_runner.py (~1 lines, _cleanup_server)
drill: aiohttp/web_runner.py (~1 lines, _cleanup_server)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## _cleanup_server  (aiohttp/web_runner.py L376-377)
```
    async def _cleanup_server(self) -> None:
        pass
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

## _make_request  (aiohttp/web_server.py L97-105)
```
    def _make_request(
        self,
        message: RawRequestMessage,
        payload: StreamReader,
        protocol: RequestHandler[BaseRequest],
        writer: AbstractStreamWriter,
        task: "asyncio.Task[None]",
    ) -> BaseRequest:
        return BaseRequest(message, payload, protocol, writer, task, self._loop)
```

## _make_server  (aiohttp/web_runner.py L373-374)
```
    async def _make_server(self) -> Server[BaseRequest]:
        return self._web_server
```

## app  (tests/test_web_websocket.py L31-35)
```
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    ret: web.Application = mock.create_autospec(web.Application, spec_set=True)
    ret.on_response_prepare = aiosignal.Signal(ret)  # type: ignore[misc]
    ret.on_response_prepare.freeze()
    return ret
```

## shutdown  (tests/test_web_runner.py L310-312)
```
    async def shutdown() -> NoReturn:
        spy()
        raise web.GracefulExit()
```

## AppRunner  (aiohttp/web_runner.py L380-453)
```
class AppRunner(BaseRunner[Request]):
    """Web Application runner"""

    __slots__ = ("_app",)

    def __init__(
        self,
        app: Application,
        *,
        handle_signals: bool = False,
        access_log_class: type[AbstractAccessLogger] = AccessLogger,
        **kwargs: Any,
    ) -> None:
        if not isinstance(app, Application):
            raise TypeError(
                f"The first argument should be web.Application instance, got {app!r}"
            )
        kwargs["access_log_class"] = access_log_class

        if app._handler_args:
            for k, v in app._handler_args.items():
                kwargs[k] = v

        if not issubclass(kwargs["access_log_class"], AbstractAccessLogger):
            raise TypeError(
                "access_log_class must be subclass of "
                "aiohttp.abc.AbstractAccessLogger, got {}".format(
                    kwargs["access_log_class"]
                )
            )

        super().__init__(handle_signals=handle_signals, **kwargs)
        self._app = app

    @property
    def app(self) -> Application:
        return self._app

    async def shutdown(self) -> None:
        await self._app.shutdown()

    async def _make_server(self) -> Server[Request]:
        self._app.on_startup.freeze()
        await self._app.startup()
        self._app.freeze()

        return Server(
            self._app._handle,
            request_factory=self._make_request,
            **self._kwargs,
        )

    def _make_request(
        self,
        message: RawRequestMessage,
        payload: StreamReader,
        protocol: RequestHandler[Request],
        writer: AbstractStreamWriter,
        task: "asyncio.Task[None]",
        _cls: type[Request] = Request,
    ) -> Request:
        loop = asyncio.get_running_loop()
        return _cls(
            message,
            payload,
            protocol,
            writer,
            task,
            loop,
            client_max_size=self.app._client_max_size,
        )

    async def _cleanup_server(self) -> None:
        await self._app.cleanup()
```

## _check_site  (aiohttp/web_runner.py L345-347)
```
    def _check_site(self, site: BaseSite) -> None:
        if site not in self._sites:
            raise RuntimeError(f"Site {site} is not registered in runner {self}")
```

## _reg_site  (aiohttp/web_runner.py L340-343)
```
    def _reg_site(self, site: BaseSite) -> None:
        if site in self._sites:
            raise RuntimeError(f"Site {site} is already registered in runner {self}")
        self._sites.append(site)
```

## _unreg_site  (aiohttp/web_runner.py L349-352)
```
    def _unreg_site(self, site: BaseSite) -> None:
        if site not in self._sites:
            raise RuntimeError(f"Site {site} is not registered in runner {self}")
        self._sites.remove(site)
```

## addresses  (aiohttp/web_runner.py L273-282)
```
    def addresses(self) -> list[Any]:
        ret: list[Any] = []
        for site in self._sites:
            server = site._server
            if server is not None:
                sockets = server.sockets
                if sockets is not None:
                    for sock in sockets:
                        ret.append(sock.getsockname())
        return ret
```

## cleanup  (tests/test_payload.py L49-52)
```
def cleanup(
    cleanup_payload_pending_file_closes: None,
) -> None:
    """Ensure all pending file close operations complete during test teardown."""
```

## server  (aiohttp/web_runner.py L269-270)
```
    def server(self) -> Server[_Request] | None:
        return self._server
```

## setup  (aiohttp/web_runner.py L288-299)
```
    async def setup(self) -> None:
        loop = asyncio.get_event_loop()

        if self._handle_signals:
            try:
                loop.add_signal_handler(signal.SIGINT, _raise_graceful_exit)
                loop.add_signal_handler(signal.SIGTERM, _raise_graceful_exit)
            except NotImplementedError:
                # add_signal_handler is not implemented on Windows
                pass

        self._server = await self._make_server()
```

## sites  (aiohttp/web_runner.py L285-286)
```
    def sites(self) -> set[BaseSite]:
        return set(self._sites)
```

## BaseRunner  (aiohttp/web_runner.py L252-352)
```
class BaseRunner(ABC, Generic[_Request]):
    __slots__ = ("_handle_signals", "_kwargs", "_server", "_sites", "_shutdown_timeout")

    def __init__(
        self,
        *,
        handle_signals: bool = False,
        shutdown_timeout: float = 60.0,
        **kwargs: Any,
    ) -> None:
        self._handle_signals = handle_signals
        self._kwargs = kwargs
        self._server: Server[_Request] | None = None
        self._sites: list[BaseSite] = []
        self._shutdown_timeout = shutdown_timeout

    @property
    def server(self) -> Server[_Request] | None:
        return self._server

    @property
    def addresses(self) -> list[Any]:
        ret: list[Any] = []
        for site in self._sites:
            server = site._server
            if server is not None:
                sockets = server.sockets
                if sockets is not None:
                    for sock in sockets:
                        ret.append(sock.getsockname())
        return ret

    @property
    def sites(self) -> set[BaseSite]:
        return set(self._sites)

    async def setup(self) -> None:
        loop = asyncio.get_event_loop()

        if self._handle_signals:
            try:
                loop.add_signal_handler(signal.SIGINT, _raise_graceful_exit)
                loop.add_signal_handler(signal.SIGTERM, _raise_graceful_exit)
            except NotImplementedError:
                # add_signal_handler is not implemented on Windows
                pass

        self._server = await self._make_server()

    @abstractmethod
    async def shutdown(self) -> None:
        """Call any shutdown hooks to help server close gracefully."""

    async def cleanup(self) -> None:
        # The loop over sites is intentional, an exception on gather()
        # leaves self._sites in unpredictable state.
        # The loop guarantees that a site is either deleted on success or
        # still present on failure
        for site in list(self._sites):
            await site.stop()

        if self._server:  # If setup succeeded
            # Yield to event loop to ensure incoming requests prior to stopping the sites
            # have all started to be handled before we proceed to close idle connections.
            await asyncio.sleep(0)
            self._server.pre_shutdown()
            await self.shutdown()
            await self._server.shutdown(self._shutdown_timeout)
        await self._cleanup_server()

        self._server = None
        if self._handle_signals:
            loop = asyncio.get_running_loop()
            try:
                loop.remove_signal_handler(signal.SIGINT)
                loop.remove_signal_handler(signal.SIGTERM)
            except NotImplementedError:
                # remove_signal_handler is not implemented on Windows
                pass

    @abstractmethod
    async def _make_server(self) -> Server[_Request]:
        """Return a new server for the runner to serve requests."""

    @abstractmethod
    async def _cleanup_server(self) -> None:
        """Run any cleanup steps after the server is shutdown."""

    def _reg_site(self, site: BaseSite) -> None:
        if site in self._sites:
            raise RuntimeError(f"Site {site} is already registered in runner {self}")
        self._sites.append(site)

    def _check_site(self, site: BaseSite) -> None:
        if site not in self._sites:
            raise RuntimeError(f"Site {site} is not registered in runner {self}")

    def _unreg_site(self, site: BaseSite) -> None:
        if site not in self._sites:
            raise RuntimeError(f"Site {site} is not registered in runner {self}")
        self._sites.remove(site)
```

## name  (aiohttp/web_urldispatcher.py L894-895)
```
    def name(self) -> str | None:
        return None
```

## start  (tests/test_client_request.py L1698-1707)
```
        async def start(self, connection: Connection) -> ClientResponse:
            nonlocal conn
            conn = connection
            self.status = 123
            self.reason = "Test OK"
            self._headers = CIMultiDictProxy(CIMultiDict())
            self.cookies = SimpleCookie()
            return self

    called = False
```

## stop  (tests/test_run_app.py L1011-1013)
```
    async def stop(self, request: web.Request) -> web.Response:
        asyncio.get_running_loop().call_soon(self.raiser)
        return web.Response()
```

## BaseSite  (aiohttp/web_runner.py L47-78)
```
class BaseSite(ABC):
    __slots__ = ("_runner", "_ssl_context", "_backlog", "_server")

    def __init__(
        self,
        runner: "BaseRunner[Any]",
        *,
        ssl_context: SSLContext | None = None,
        backlog: int = 128,
    ) -> None:
        if runner.server is None:
            raise RuntimeError("Call runner.setup() before making a site")
        self._runner = runner
        self._ssl_context = ssl_context
        self._backlog = backlog
        self._server: asyncio.Server | None = None

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the site (e.g. a URL)."""

    @abstractmethod
    async def start(self) -> None:
        self._runner._reg_site(self)

    async def stop(self) -> None:
        self._runner._check_site(self)
        if self._server is not None:  # Maybe not started yet
            self._server.close()

        self._runner._unreg_site(self)
```

## GracefulExit  (aiohttp/web_runner.py L39-40)
```
class GracefulExit(SystemExit):
    code = 1
```

## NamedPipeSite  (aiohttp/web_runner.py L184-210)
```
class NamedPipeSite(BaseSite):
    __slots__ = ("_path",)

    def __init__(self, runner: "BaseRunner[Any]", path: str) -> None:
        loop = asyncio.get_event_loop()
        if not isinstance(
            loop, asyncio.ProactorEventLoop  # type: ignore[attr-defined]
        ):
            raise RuntimeError(
                "Named Pipes only available in proactor loop under windows"
            )
        super().__init__(runner)
        self._path = path

    @property
    def name(self) -> str:
        return self._path

    async def start(self) -> None:
        await super().start()
        loop = asyncio.get_event_loop()
        server = self._runner.server
        assert server is not None
        _server = await loop.start_serving_pipe(  # type: ignore[attr-defined]
            server, self._path
        )
        self._server = _server[0]
```

## ServerRunner  (aiohttp/web_runner.py L355-377)
```
class ServerRunner(BaseRunner[BaseRequest]):
    """Low-level web server runner"""

    __slots__ = ("_web_server",)

    def __init__(
        self,
        web_server: Server[BaseRequest],
        *,
        handle_signals: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(handle_signals=handle_signals, **kwargs)
        self._web_server = web_server

    async def shutdown(self) -> None:
        pass

    async def _make_server(self) -> Server[BaseRequest]:
        return self._web_server

    async def _cleanup_server(self) -> None:
        pass
```

## SockSite  (aiohttp/web_runner.py L213-249)
```
class SockSite(BaseSite):
    __slots__ = ("_sock", "_name")

    def __init__(
... (truncated)
```
--- END SOURCE SNIPPETS ---

QUESTION: During application shutdown, how does the server unwind startup resources, and what happens if cleanup only partially initialized or multiple cleanup steps fail?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
