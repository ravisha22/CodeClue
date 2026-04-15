# Baseline Evaluation: Raw Source Files
# Task: blind-aiohttp-2

You are a senior software engineer. You have been given raw source code
excerpts from a repository. Answer the question using ONLY the source
code below. Do not use any external knowledge about the framework.

--- SOURCE CODE ---
## tools\cleanup_changes.py (score: 6.0)
```
#!/usr/bin/env python

# Run me after the backport branch release to cleanup CHANGES records
# that was backported and published.

import re
import subprocess
from pathlib import Path

ALLOWED_SUFFIXES = (
    "bugfix",
    "feature",
    "deprecation",
    "breaking",
    "doc",
    "packaging",
    "contrib",
    "misc",
)
PATTERN = re.compile(
    r"(\d+|[0-9a-f]{8}|[0-9a-f]{7}|[0-9a-f]{40})\.("
    + "|".join(ALLOWED_SUFFIXES)
    + r")(\.\d+)?(\.rst)?",
)


def main():
    root = Path(__file__).parent.parent
    delete = []
    changes = (root / "CHANGES.rst").read_text()
    for fname in (root / "CHANGES").iterdir():
        match = PATTERN.match(fname.name)
        if match is not None:
            commit_issue_or_pr = match.group(1)
            tst_issue_or_pr = f":issue:`{commit_issue_or_pr}`"
            tst_commit = f":commit:`{commit_issue_or_pr}`"
            if tst_issue_or_pr in changes or tst_commit in changes:
                subprocess.run(["git", "rm", fname])
                delete.append(fname.name)
    print("Deleted CHANGES records:", " ".join(delete))
    print("Please verify and commit")


if __name__ == "__main__":
    main()

```

## aiohttp\web_server.py (score: 3.0)
```
"""Low level HTTP server."""

import asyncio
import warnings
from collections.abc import Awaitable, Callable
from typing import Any, Generic, TypeVar, overload

from .abc import AbstractStreamWriter
from .http_parser import RawRequestMessage
from .streams import StreamReader
from .web_protocol import RequestHandler
from .web_request import BaseRequest
from .web_response import StreamResponse

__all__ = ("Server",)

_Request = TypeVar("_Request", bound=BaseRequest)
_RequestFactory = Callable[
    [
        RawRequestMessage,
        StreamReader,
        "RequestHandler[_Request]",
        AbstractStreamWriter,
        "asyncio.Task[None]",
    ],
    _Request,
]


class Server(Generic[_Request]):
    request_factory: _RequestFactory[_Request]

    @overload
    def __init__(
        self: "Server[BaseRequest]",
        handler: Callable[[_Request], Awaitable[StreamResponse]],
        *,
        debug: bool | None = None,
        handler_cancellation: bool = False,
        **kwargs: Any,  # TODO(PY311): Use Unpack to define kwargs from RequestHandler
    ) -> None: ...
    @overload
    def __init__(
        self,
        handler: Callable[[_Request], Awaitable[StreamResponse]],
        *,
        request_factory: _RequestFactory[_Request] | None,
        debug: bool | None = None,
        handler_cancellation: bool = False,
        **kwargs: Any,
    ) -> None: ...
    def __init__(
        self,
        handler: Callable[[_Request], Awaitable[StreamResponse]],
        *,
        request_factory: _RequestFactory[_Request] | None = None,
        debug: bool | None = None,
        handler_cancellation: bool = False,
        **kwargs: Any,
    ) -> None:
        if debug is not None:
            warnings.warn(
                "debug argument is no-op since 4.0 and scheduled for removal in 5.0",
                DeprecationWarning,
                stacklevel=2,
            )
        self._loop = asyncio.get_running_loop()
        self._connections: dict[RequestHandler[_Request], asyncio.Transport] = {}
        self._kwargs = kwargs
        # requests_count is the number of requests being processed by the server
        # for the lifetime of the server.
        self.requests_count = 0
        self.request_handler = handler
        self.request_factory = request_factory or self._make_request  # type: ignore[assignment]
        self.handler_cancellation = handler_cancellation

    @property
    def connections(self) -> list[RequestHandler[_Request]]:
        return list(self._connections.keys())

    def connection_made(
        self, handler: RequestHandler[_Request], transport: asyncio.Transport
    ) -> None:
        self._connections[handler] = transport

    def connection_lost(
        self, handler: RequestHandler[_Request], exc: BaseException | None = None
    ) -> None:
        if handler in self._connections:
            if handler._task_handler:
                handler._task_handler.add_done_callback(
                    lambda f: self._connections.pop(handler, None)
                )
            else:
                del self._connections[handler]

    def _make_request(
        self,
        message: RawRequestMessage,
        payload: StreamReader,
        protocol: RequestHandler[BaseRequest],
        writer: AbstractStreamWriter,
        task: "asyncio.Task[None]",
    ) -> BaseRequest:
        return BaseRequest(message, payload, protocol, writer, task, self._loop)

    def pre_shutdown(self) -> None:
        for conn in self._connections:
            conn.close()

    async def shutdown(self, timeout: float | None = None) -> None:
        coros = (conn.shutdown(timeout) for conn in self._connections)
        await asyncio.gather(*coros)
        self._connections.clear()

    def __call__(self) -> RequestHandler[_Request]:
        try:
            return RequestHandler(self, loop=self._loop, **self._kwargs)
        except TypeError:
            # Failsafe creation: remove all custom handler_args
            kwargs = {
                k: v
                for k, v in self._kwargs.items()
                if k in ["debug", "access_log_class"]
            }
            return RequestHandler(self, loop=self._loop, **kwargs)

```

## examples\fake_server.py (score: 3.0)
```
#!/usr/bin/env python3
import asyncio
import pathlib
import socket
import ssl

from aiohttp import ClientSession, TCPConnector, web
from aiohttp.abc import AbstractResolver, ResolveResult
from aiohttp.resolver import DefaultResolver


class FakeResolver(AbstractResolver):
    _LOCAL_HOST = {0: "127.0.0.1", socket.AF_INET: "127.0.0.1", socket.AF_INET6: "::1"}

    def __init__(self, fakes: dict[str, int]) -> None:
        """fakes -- dns -> port dict"""
        self._fakes = fakes
        self._resolver = DefaultResolver()

    async def resolve(
        self,
        host: str,
        port: int = 0,
        family: socket.AddressFamily = socket.AF_INET,
    ) -> list[ResolveResult]:
        fake_port = self._fakes.get(host)
        if fake_port is not None:
            return [
                {
                    "hostname": host,
                    "host": self._LOCAL_HOST[family],
                    "port": fake_port,
                    "family": family,
                    "proto": 0,
                    "flags": socket.AI_NUMERICHOST,
                }
            ]
        else:
            return await self._resolver.resolve(host, port, family)

    async def close(self) -> None:
        await self._resolver.close()


class FakeFacebook:
    def __init__(self) -> None:
        self.app = web.Application()
        self.app.router.add_routes(
            [
                web.get("/v2.7/me", self.on_me),
                web.get("/v2.7/me/friends", self.on_my_friends),
            ]
        )
        self.runner = web.AppRunner(self.app)
        here = pathlib.Path(__file__)
        ssl_cert = here.parent / "server.crt"
        ssl_key = here.parent / "server.key"
        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.ssl_context.load_cert_chain(str(ssl_cert), str(ssl_key))

    async def start(self) -> dict[str, int]:
        await self.runner.setup()
        site = web.TCPSite(
            self.runner, "127.0.0.1", port=0, ssl_context=self.ssl_context
        )
        await site.start()
        return {"graph.facebook.com": site.port}

    async def stop(self) -> None:
        await self.runner.cleanup()

    async def on_me(self, request: web.Request) -> web.StreamResponse:
        return web.json_response({"name": "John Doe", "id": "12345678901234567"})

    async def on_my_friends(self, request: web.Request) -> web.StreamResponse:
        return web.json_response(
            {
                "data": [
                    {"name": "Bill Doe", "id": "233242342342"},
                    {"name": "Mary Doe", "id": "2342342343222"},
                    {"name": "Alex Smith", "id": "234234234344"},
                ],
                "paging": {
                    "cursors": {
                        "before": "QVFIUjRtc2c5NEl0ajN",
                        "after": "QVFIUlpFQWM0TmVuaDRad0dt",
                    },
                    "next": (
                        "https://graph.facebook.com/v2.7/12345678901234567/"
                        "friends?access_token=EAACEdEose0cB"
                    ),
                },
                "summary": {"total_count": 3},
            }
        )


async def main() -> None:
    token = "ER34gsSGGS34XCBKd7u"

    fake_facebook = FakeFacebook()
    info = await fake_facebook.start()
    resolver = FakeResolver(info)
    connector = TCPConnector(resolver=resolver, ssl=False)

    async with ClientSession(connector=connector) as session:
        async with session.get(
            "https://graph.facebook.com/v2.7/me", params={"access_token": token}
        ) as resp:
            print(await resp.json())

        async with session.get(
            "https://graph.facebook.com/v2.7/me/friends", params={"access_token": token}
        ) as resp:
            print(await resp.json())

    await fake_facebook.stop()


asyncio.run(main())

```

## examples\server_simple.py (score: 3.0)
```
# server_simple.py
from aiohttp import web


async def handle(request: web.Request) -> web.StreamResponse:
    name = request.match_info.get("name", "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


async def wshandle(request: web.Request) -> web.StreamResponse:
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type is web.WSMsgType.TEXT:
            await ws.send_str(f"Hello, {msg.data}")
        elif msg.type is web.WSMsgType.BINARY:
            await ws.send_bytes(msg.data)
        elif msg.type is web.WSMsgType.CLOSE:
            break

    return ws


app = web.Application()
app.add_routes(
    [web.get("/", handle), web.get("/echo", wshandle), web.get("/{name}", handle)]
)

web.run_app(app)

```

## tests\autobahn\server\server.py (score: 3.0)
```
#!/usr/bin/env python3

import logging

from aiohttp import WSCloseCode, web

websockets = web.AppKey("websockets", list[web.WebSocketResponse])


async def wshandler(request: web.Request) -> web.WebSocketResponse:
    ws = web.WebSocketResponse(autoclose=False)
    await ws.prepare(request)

    request.app[websockets].append(ws)

    async for msg in ws:
        if msg.type is web.WSMsgType.TEXT:
            await ws.send_str(msg.data)
        elif msg.type is web.WSMsgType.BINARY:
            await ws.send_bytes(msg.data)
        else:
            break

    return ws


async def on_shutdown(app: web.Application) -> None:
    for ws in app[websockets]:
        await ws.close(code=WSCloseCode.GOING_AWAY, message=b"Server shutdown")


if __name__ == "__main__":  # pragma: no branch
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s"
    )

    app = web.Application()
    app[websockets] = []
    app.router.add_route("GET", "/", wshandler)
    app.on_shutdown.append(on_shutdown)
    web.run_app(app, port=9001)

```

## aiohttp\__init__.py (score: 0.0)
```
__version__ = "4.0.0a2.dev0"

from typing import TYPE_CHECKING

from . import hdrs
from .client import (
    BaseConnector,
    ClientConnectionError,
    ClientConnectionResetError,
    ClientConnectorCertificateError,
    ClientConnectorDNSError,
    ClientConnectorError,
    ClientConnectorSSLError,
    ClientError,
    ClientHttpProxyError,
    ClientOSError,
    ClientPayloadError,
    ClientProxyConnectionError,
    ClientRequest,
    ClientResponse,
    ClientResponseError,
    ClientSession,
    ClientSSLError,
    ClientTimeout,
    ClientWebSocketResponse,
    ClientWSTimeout,
    ConnectionTimeoutError,
    ContentTypeError,
    Fingerprint,
    InvalidURL,
    InvalidUrlClientError,
    InvalidUrlRedirectClientError,
    NamedPipeConnector,
    NonHttpUrlClientError,
    NonHttpUrlRedirectClientError,
    RedirectClientError,
    RequestInfo,
    ServerConnectionError,
    ServerDisconnectedError,
    ServerFingerprintMismatch,
    ServerTimeoutError,
    SocketTimeoutError,
    TCPConnector,
    TooManyRedirects,
    UnixConnector,
    WSMessageTypeError,
    WSServerHandshakeError,
    request,
)
from .client_middleware_digest_auth import DigestAuthMiddleware
from .client_middlewares import ClientHandlerType, ClientMiddlewareType
from .compression_utils import set_zlib_backend
from .connector import AddrInfoType, SocketFactoryType
from .cookiejar import CookieJar, DummyCookieJar
from .formdata import FormData
from .helpers import BasicAuth, ChainMapProxy, ETag
from .http import (
    HttpVersion,
    HttpVersion10,
    HttpVersion11,
    WebSocketError,
    WSCloseCode,
    WSMessage,
    WSMsgType,
)
from .multipart import (
    BadContentDispositionHeader,
    BadContentDispositionParam,
    BodyPartReader,
    MultipartReader,
    MultipartWriter,
    content_disposition_filename,
    parse_content_disposition,
)
from .payload import (
    PAYLOAD_REGISTRY,
    AsyncIterablePayload,
    BufferedReaderPayload,
    BytesIOPayload,
    BytesPayload,
    IOBasePayload,
    JsonPayload,
    Payload,
    StringIOPayload,
    StringPayload,
    TextIOPayload,
    get_payload,
    payload_type,
)
from .resolver import AsyncResolver, DefaultResolver, ThreadedResolver
from .streams import EMPTY_PAYLOAD, DataQueue, EofStream, StreamReader
from .tracing import (
    TraceConfig,
    TraceConnectionCreateEndParams,
    TraceConnectionCreateStartParams,
    TraceConnectionQueuedEndParams,
    TraceConnectionQueuedStartParams,
    TraceConnectionReuseconnParams,
    TraceDnsCacheHitParams,
    TraceDnsCacheMissParams,
    TraceDnsResolveHostEndParams,
    TraceDnsResolveHostStartParams,
    TraceRequestChunkSentParams,
    TraceRequestEndParams,
    TraceRequestExceptionParams,
    TraceRequestHeadersSentParams,
    TraceRequestRedirectParams,
    TraceRequestStartParams,
    TraceResponseChunkReceivedParams,
)

if TYPE_CHECKING:
    # At runtime these are lazy-loaded at the bottom of the file.
    from .worker import GunicornUVLoopWebWorker, GunicornWebWorker

__all__: tuple[str, ...] = (
    "hdrs",
    # client
    "AddrInfoType",
    "BaseConnector",
    "ClientConnectionError",
    "ClientConnectionResetError",
    "ClientConnectorCertificateError",
    "ClientConnectorDNSError",
    "ClientConnectorError",
    "ClientConnectorSSLError",
    "ClientError",
    "ClientHttpProxyError",
    "ClientOSError",
    "ClientPayloadError",
    "ClientProxyConnectionError",
    "ClientResponse",
    "ClientRequest",
    "ClientResponseError",
    "ClientSSLError",
    "ClientSession",
    "ClientTimeout",
    "ClientWebSocketResponse",
    "ClientWSTimeout",
    "ConnectionTimeoutError",
    "ContentTypeError",
    "Fingerprint",
    "InvalidURL",
    "InvalidUrlClientError",
    "InvalidUrlRedirectClientError",
    "NonHttpUrlClientError",
    "NonHttpUrlRedirectClientError",
    "RedirectClientError",
    "RequestInfo",
    "ServerConnectionError",
    "ServerDisconnectedError",
    "ServerFingerprintMismatch",
    "ServerTimeoutError",
    "SocketFactoryType",
    "SocketTimeoutError",
    "TCPConnector",
    "TooManyRedirects",
    "UnixConnector",
    "NamedPipeConnector",
    "WSServerHandshakeError",
    "request",
    # client_middleware
    "ClientMiddlewareType",
    "ClientHandlerType",
    # cookiejar
    "CookieJar",
    "DummyCookieJar",
    # formdata
    "FormData",
    # helpers
    "BasicAuth",
    "ChainMapProxy",
    "DigestAuthMiddleware",
    "ETag",
    "set_zlib_backend",
    # http
    "HttpVersion",
    "HttpVersion10",
    "HttpVersion11",
    "WSMsgType",
    "WSCloseCode",
    "WSMessage",
    "WebSocketError",
    # multipart
    "BadContentDispositionHeader",
    "BadContentDispositionParam",
    "BodyPartReader",
    "MultipartReader",
    "MultipartWriter",
    "content_disposition_filename",
    "parse_content_disposition",
    # payload
    "AsyncIterablePayload",
    "BufferedReaderPayload",
    "BytesIOPayload",
    "BytesPayload",
    "IOBasePayload",
    "JsonPayload",
    "PAYLOAD_REGISTRY",
    "Payload",
    "StringIOPayload",
    "StringPayload",
    "TextIOPayload",
    "get_payload",
    "payload_type",
    # resolver
    "AsyncResolver",
    "DefaultResolver",
    "ThreadedResolver",
    # streams
    "DataQueue",
    "EMPTY_PAYLOAD",
    "EofStream",
    "StreamReader",
    # tracing
    "TraceConfig",
    "TraceConnectionCreateEndParams",
    "TraceConnectionCreateStartParams",
    "TraceConnectionQueuedEndParams",
    "TraceConnectionQueuedStartParams",
    "TraceConnectionReuseconnParams",
    "TraceDnsCacheHitParams",
    "TraceDnsCacheMissParams",
    "TraceDnsResolveHostEndParams",
    "TraceDnsResolveHostStartParams",
    "TraceRequestChunkSentParams",
    "TraceRequestEndParams",
    "TraceRequestExceptionParams",
    "TraceRequestHeadersSentParams",
    "TraceRequestRedirectParams",
    "TraceRequestStartParams",
    "TraceResponseChunkReceivedParams",
    # workers (imported lazily with __getattr__)
    "GunicornUVLoopWebWorker",
    "GunicornWebWorker",
    "WSMessageTypeError",
)


def __dir__() -> tuple[str, ...]:
    return __all__ + ("__doc__",)


def __getattr__(name: str) -> object:
    global GunicornUVLoopWebWorker, GunicornWebWorker

    # Importing gunicorn takes a long time (>100ms), so only import if actually needed.
    if name in ("GunicornUVLoopWebWorker", "GunicornWebWorker"):
        try:
            from .worker import GunicornUVLoopWebWorker as guv, GunicornWebWorker as gw
        except ImportError:
            return None

        GunicornUVLoopWebWorker = guv  # type: ignore[misc]
        GunicornWebWorker = gw  # type: ignore[misc]
        return guv if name == "GunicornUVLoopWebWorker" else gw

    raise AttributeError(f"module {__name__} has no attribute {name}")

```

## aiohttp\_cookie_helpers.py (score: 0.0)
```
"""
Internal cookie handling helpers.

This module contains internal utilities for cookie parsing and manipulation.
These are not part of the public API and may change without notice.
"""

import re
from collections.abc import Sequence
from http.cookies import Morsel
from typing import cast

from .log import internal_logger

__all__ = (
    "parse_set_cookie_headers",
    "parse_cookie_header",
    "preserve_morsel_with_coded_value",
)

# Cookie parsing constants
# Allow more characters in cookie names to handle real-world cookies
# that don't strictly follow RFC standards (fixes #2683)
# RFC 6265 defines cookie-name token as per RFC 2616 Section 2.2,
# but many servers send cookies with characters like {} [] () etc.
# This makes the cookie parser more tolerant of real-world cookies
# while still providing some validation to catch obviously malformed names.
_COOKIE_NAME_RE = re.compile(r"^[!#$%&\'()*+\-./0-9:<=>?@A-Z\[\]^_`a-z{|}~]+$")
_COOKIE_KNOWN_ATTRS = frozenset(  # AKA Morsel._reserved
    (
        "path",
        "domain",
        "max-age",
        "expires",
        "secure",
        "httponly",
        "samesite",
        "partitioned",
        "version",
        "comment",
    )
)
_COOKIE_BOOL_ATTRS = frozenset(  # AKA Morsel._flags
    ("secure", "httponly", "partitioned")
)

# SimpleCookie's pattern for parsing cookies with relaxed validation
# Based on http.cookies pattern but extended to allow more characters in cookie names
# to handle real-world cookies (fixes #2683)
_COOKIE_PATTERN = re.compile(
    r"""
    \s*                            # Optional whitespace at start of cookie
    (?P<key>                       # Start of group 'key'
    # aiohttp has extended to include [] for compatibility with real-world cookies
    [\w\d!#%&'~_`><@,:/\$\*\+\-\.\^\|\)\(\?\}\{\[\]]+   # Any word of at least one letter
    )                              # End of group 'key'
    (                              # Optional group: there may not be a value.
    \s*=\s*                          # Equal Sign
    (?P<val>                         # Start of group 'val'
    "(?:[^\\"]|\\.)*"                  # Any double-quoted string (properly closed)
    |                                  # or
    "[^";]*                            # Unmatched opening quote (differs from SimpleCookie - issue #7993)
    |                                  # or
    # Special case for "expires" attr - RFC 822, RFC 850, RFC 1036, RFC 1123
    (\w{3,6}day|\w{3}),\s              # Day of the week or abbreviated day (with comma)
    [\w\d\s-]{9,11}\s[\d:]{8}\s        # Date and time in specific format
    (GMT|[+-]\d{4})                     # Timezone: GMT or RFC 2822 offset like -0000, +0100
                                        # NOTE: RFC 2822 timezone support is an aiohttp extension
                                        # for issue #4493 - SimpleCookie does NOT support this
    |                                  # or
    # ANSI C asctime() format: "Wed Jun  9 10:18:14 2021"
    # NOTE: This is an aiohttp extension for issue #4327 - SimpleCookie does NOT support this format
    \w{3}\s+\w{3}\s+[\s\d]\d\s+\d{2}:\d{2}:\d{2}\s+\d{4}
    |                                  # or
    [\w\d!#%&'~_`><@,:/\$\*\+\-\.\^\|\)\(\?\}\{\=\[\]]*      # Any word or empty string
    )                                # End of group 'val'
    )?                             # End of optional value group
    \s*                            # Any number of spaces.
    (\s+|;|$)                      # Ending either at space, semicolon, or EOS.
    """,
    re.VERBOSE | re.ASCII,
)


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


_unquote_sub = re.compile(r"\\(?:([0-3][0-7][0-7])|(.))").sub


def _unquote_replace(m: re.Match[str]) -> str:
    """
    Replace function for _unquote_sub regex substitution.

    Handles escaped characters in cookie values:
    - Octal sequences are converted to their character representation
    - Other escaped characters are unescaped by removing the backslash
    """
    if m[1]:
        return chr(int(m[1], 8))
    return m[2]


def _unquote(value: str) -> str:
    """
    Unquote a cookie value.

    Vendored from http.cookies._unquote to ensure compatibility.

    Note: The original implementation checked for None, but we've removed
    that check since all callers already ensure the value is not None.
    """
    # If there aren't any doublequotes,
    # then there can't be any special characters.  See RFC 2109.
    if len(value) < 2:
        return value
    if value[0] != '"' or value[-1] != '"':
        return value

    # We have to assume that we must decode this string.
    # Down to work.

    # Remove the "s
    value = value[1:-1]

    # Check for special sequences.  Examples:
    #    \012 --> \n
    #    \"   --> "
    #
    return _unquote_sub(_unquote_replace, value)


def parse_cookie_header(header: str) -> list[tuple[str, Morsel[str]]]:
    """
    Parse a Cookie header according to RFC 6265 Section 5.4.

    Cookie headers contain only name-value pairs separated by semicolons.
    There are no attributes in Cookie headers - even names that match
    attribute names (like 'path' or 'secure') should be treated as cookies.

    This parser uses the same regex-based approach as parse_set_cookie_headers
    to properly handle quoted values that may contain semicolons. When the
    regex fails to match a malformed cookie, it falls back to simple parsing
    to ensure subsequent cookies are not lost
    https://github.com/aio-libs/aiohttp/issues/11632

    Args:
        header: The Cookie header value to parse

    Returns:
        List of (name, Morsel) tuples for compatibility with SimpleCookie.update()
    """
    if not header:
        return []

... (truncated)
```
--- END SOURCE CODE ---

QUESTION: During application shutdown, how does the server unwind startup resources, and what happens if cleanup only partially initialized or multiple cleanup steps fail?

Provide a detailed answer citing specific functions/files from the source.
