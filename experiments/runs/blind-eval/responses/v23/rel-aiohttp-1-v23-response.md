# v2.3 Response: rel-aiohttp-1
Date: 2026-04-15

## Summary

The aiohttp codebase has a rich class hierarchy for request and response objects. Server-side requests derive from `HeadersMixin` via `BaseRequest → Request`. Server-side responses derive from `HeadersMixin + CookieMixin` via `StreamResponse → Response/FileResponse/WebSocketResponse`. Client-side responses also derive from `HeadersMixin` via `ClientResponse`. Exception hierarchies follow parallel trees for client errors and HTTP status code errors.

## Server-Side Request Hierarchy

- **`BaseRequest`** (`aiohttp/web_request.py:109-823`, FOCUS) → extends **`HeadersMixin`**. The base request class providing HTTP request data access (URL, headers, body reading, ETag handling, etc.). Raises `RuntimeError`, `ValueError`, `HTTPUnsupportedMediaType`, `HTTPBadRequest`.

- **`Request`** (`aiohttp/web_request.py:826-884`, FOCUS) → extends **`BaseRequest`**. The concrete request class used by the web application framework.

## Server-Side Response Hierarchy

- **`StreamResponse`** (`aiohttp/web_response.py:74-532`, FOCUS) → extends **`HeadersMixin, CookieMixin`** (multiple inheritance). The base response class supporting streaming writes, compression, headers, and cookies. Calls methods like `_generate_content_type_header`, `_prepare_headers`, `_set_status`, `_start_compression`, `_write_headers`, `drain`, `enable_compression`, `write`.

- **`Response`** (`aiohttp/web_response.py:535-740`, FOCUS) → extends **`StreamResponse`**. The standard response class with body content support. Called by `json_bytes_response`, `json_response`.

- **`FileResponse`** (`aiohttp/web_fileresponse.py:79-406`, FOCUS) → extends **`StreamResponse`**. A specialized response for serving files. Handles ETag matching, conditional responses (304, 412), file stat/encoding, and sendfile optimization.

- **`WebSocketResponse`** (`aiohttp/web_ws.py:78-773`, FOCUS) → extends **`StreamResponse`**. Handles WebSocket protocol upgrade, heartbeat, ping/pong, and message framing.

## Client-Side Request/Response Hierarchy

- **`ClientResponse`** (`aiohttp/client_reqrep.py:184-683`, FOCUS) → extends **`HeadersMixin`**. The client-side response object. Manages connection cleanup, content notification, encoding detection, and body reading. Raises `ClientResponseError`, `RuntimeError`, `ClientConnectionError`, `ContentTypeError`.

- **`ClientRequest`** (`aiohttp/client_reqrep.py:954-1434`, FOCUS) → extends **`ClientRequestBase`**. The client-side request object that handles header updates, body encoding, cookies, proxy configuration, and transfer encoding.

- **`RequestInfo`** (`aiohttp/client_reqrep.py:109-124`, FOCUS) → extends **`_RequestInfo`**, which extends **`NamedTuple`** (`aiohttp/client_reqrep.py:102-106`). An immutable record of request metadata.

- **`ClientRequestArgs`** (`aiohttp/client_reqrep.py:930-951`, FOCUS) → extends **`TypedDict`**. Type definition for client request arguments.

## Raw HTTP Message Types

- **`RawRequestMessage`** (`aiohttp/http_parser.py:99-111`, FOCUS) → extends **`NamedTuple`**. Called by `HttpRequestParser`. Raw parsed HTTP request data.

- **`RawResponseMessage`** (`aiohttp/http_parser.py:112-123`, FOCUS) → extends **`NamedTuple`**. Called by `HttpResponseParser`. Raw parsed HTTP response data.

## Client Exception Hierarchy

- **`ClientError`** (`aiohttp/client_exceptions.py:55-56`, FOCUS) → extends **`Exception`**. Base class for all client errors.

- **`ClientResponseError`** (`aiohttp/client_exceptions.py:59-99`, FOCUS) → extends **`ClientError`**. *"Base class for exceptions that occur after getting a response."*

- **`ClientConnectionError`** (`aiohttp/client_exceptions.py:123-124`, FOCUS) → extends **`ClientError`**. *"Base class for client socket errors."*

- **`ServerConnectionError`** (referenced but not in this FOCUS set — appears in other clue files at `aiohttp/client_exceptions.py:212-213`) → extends **`ClientConnectionError`**.

- **`ServerDisconnectedError`** (`aiohttp/client_exceptions.py:216-224`, FOCUS) → extends **`ServerConnectionError`**. *"Server disconnected."*

- **`ServerTimeoutError`** (`aiohttp/client_exceptions.py:227-228`, FOCUS) → extends **`ServerConnectionError, TimeoutError`** (multiple inheritance).

## HTTP Exception Hierarchy (Server-Side)

- **`HTTPException`** (not directly in FOCUS but inferred as parent from):
  - **`HTTPError`** (`aiohttp/web_exceptions.py:172-173`, FOCUS) → extends **`HTTPException`**. *"Base class for exceptions with status codes in the 400s and 500s."*
  - **`HTTPRedirection`** (`aiohttp/web_exceptions.py:176-177`, FOCUS) → extends **`HTTPException`**. *"Base class for exceptions with status codes in the 300s."*
  - **`HTTPSuccessful`** (`aiohttp/web_exceptions.py:180-181`, FOCUS) → extends **`HTTPException`**. *"Base class for exceptions with status codes in the 200s."*

- **`HTTPClientError`** (inferred parent from):
  - **`HTTPBadRequest`** (`aiohttp/web_exceptions.py:288-289`, FOCUS) → extends **`HTTPClientError`**, `status_code=400`.
  - **`HTTPMisdirectedRequest`** (`aiohttp/web_exceptions.py:394-395`, FOCUS) → extends **`HTTPClientError`**, `status_code=421`.

- **`HTTPServerError`** (inferred parent from):
  - (No specific subclass in this FOCUS set, but `HTTPInternalServerError` at `aiohttp/web_exceptions.py:463-464` extends `HTTPServerError` per other FOCUS sets.)

## Low-Level HTTP Exception Hierarchy

- **`BadHttpMessage`** (inferred parent from):
  - **`HttpBadRequest`** (`aiohttp/http_exceptions.py:55-57`, FOCUS) → extends **`BadHttpMessage`**, `code=400`, `message='Bad Request'`.
  - **`PayloadEncodingError`** (`aiohttp/http_exceptions.py:60-61`, FOCUS) → extends **`BadHttpMessage`**. *"Base class for payload errors."*

## Protocol Hierarchy

- **`BaseProtocol`** (`aiohttp/base_protocol.py:9-100`, FOCUS) → extends **`Protocol`** (from asyncio). Handles reading, writing, and connection events.

- **`ResponseHandler`** (`aiohttp/client_proto.py:31-371`, FOCUS) → extends **`BaseProtocol`**. *"Helper class to adapt between Protocol and StreamReader."* Manages client-side protocol with timeout scheduling.

## Runner and Site Hierarchy

- **`BaseRunner`** (`aiohttp/web_runner.py:252-352`, FOCUS) → extends **`ABC`**. Base class for server runners.

- **`BaseSite`** (`aiohttp/web_runner.py:47-78`, FOCUS) → extends **`ABC`**. Base class for server binding sites.

## Enum Types

- **`ContentCoding`** (`aiohttp/web_response.py:57-64`, FOCUS) → extends **`Enum`**. Values: `deflate='deflate'`, `gzip='gzip'`, `identity='identity'`.

- **`_FileResponseResult`** (`aiohttp/web_fileresponse.py:61-67`, FOCUS) → extends **`Enum`**. *"The result of the file response."*

## Utility Class Hierarchies

- **`DecompressionBaseHandler`** (`aiohttp/compression_utils.py:153-180`, FOCUS) → extends **`ABC`**.
  - **`ZLibDecompressor`** (`aiohttp/compression_utils.py:258-285`, FOCUS) → extends **`DecompressionBaseHandler`**. Handles zlib/gzip decompression.

- **`TimerNoop`** (`aiohttp/helpers.py:657-670`, FOCUS) → extends **`BaseTimerContext`**. A no-op timer.

## Testing Protocol Classes

- **`AiohttpClient`** (`aiohttp/pytest_plugin.py:31-48`, FOCUS) → extends **`Protocol`**.
- **`AiohttpServer`** (`aiohttp/pytest_plugin.py:51-54`, FOCUS) → extends **`Protocol`**.
- **`AiohttpRawServer`** (`aiohttp/pytest_plugin.py:57-64`, FOCUS) → extends **`Protocol`**.

## Visual Hierarchy Summary

```
Exception
├── ClientError
│   ├── ClientResponseError
│   └── ClientConnectionError
│       └── ServerConnectionError
│           ├── ServerDisconnectedError
│           └── ServerTimeoutError (+ TimeoutError)
│
HeadersMixin
├── BaseRequest
│   └── Request
├── ClientResponse
└── StreamResponse (+ CookieMixin)
    ├── Response
    ├── FileResponse
    └── WebSocketResponse

Protocol (asyncio)
└── BaseProtocol
    └── ResponseHandler

ABC
├── BaseRunner
├── BaseSite
├── DecompressionBaseHandler
│   └── ZLibDecompressor
└── AbstractRouter, AbstractResource, AbstractRoute, etc.

NamedTuple
├── RawRequestMessage
├── RawResponseMessage
└── _RequestInfo
    └── RequestInfo
```

## Uncertainty / Limits

- The `HeadersMixin` and `CookieMixin` base classes are referenced as parents but their own definitions and inheritance are not visible in the FOCUS entries.
- `ClientRequestBase` (parent of `ClientRequest`) is not defined in the FOCUS section — its own parent class is unknown.
- The full `HTTPException` hierarchy between `HTTPException` → `HTTPError` → `HTTPClientError` → `HTTPBadRequest` has the `HTTPClientError` level inferred but not directly shown.
- Several intermediate classes (e.g., `HTTPServerError`) are inferred from subclass entries but not directly present in this clue file's FOCUS section.
