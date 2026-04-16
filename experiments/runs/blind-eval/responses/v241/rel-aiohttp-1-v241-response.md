# v2.4.1 Response: rel-aiohttp-1
Date: 2026-04-16

## Class Hierarchy for Request and Response Objects

### Server-Side Request Hierarchy

```
HeadersMixin
  +-- BaseRequest  (aiohttp/web_request.py:109-823)
        +-- Request  (aiohttp/web_request.py:826-884)
```

- **`BaseRequest`** extends `HeadersMixin` (`BaseRequest`, `aiohttp/web_request.py:109-823`, `extends: HeadersMixin`). It provides core request functionality: body reading (`read`), multipart handling, ETag processing, and uses `MultipartReader`, `HTTPRequestEntityTooLarge`, `HTTPUnsupportedMediaType`, and `ETag` from helpers.
- **`Request`** extends `BaseRequest` (`Request`, `aiohttp/web_request.py:826-884`, `extends: BaseRequest`).

### Client-Side Request/Response Hierarchy

```
NamedTuple
  +-- _RequestInfo  (aiohttp/client_reqrep.py:102-106)
        +-- RequestInfo  (aiohttp/client_reqrep.py:109-124)

TypedDict
  +-- ClientRequestArgs  (aiohttp/client_reqrep.py:930-951)

ClientRequestBase (uncovered)
  +-- ClientRequest  (aiohttp/client_reqrep.py:954-1434)

HeadersMixin
  +-- ClientResponse  (aiohttp/client_reqrep.py:184-683)
```

- **`_RequestInfo`** extends `NamedTuple` (`_RequestInfo`, `aiohttp/client_reqrep.py:102-106`, `extends: NamedTuple`).
- **`RequestInfo`** extends `_RequestInfo` (`RequestInfo`, `aiohttp/client_reqrep.py:109-124`, `extends: _RequestInfo`).
- **`ClientRequestArgs`** extends `TypedDict` (`ClientRequestArgs`, `aiohttp/client_reqrep.py:930-951`, `extends: TypedDict`).
- **`ClientRequest`** extends `ClientRequestBase` (`ClientRequest`, `aiohttp/client_reqrep.py:954-1434`, `extends: ClientRequestBase`). Note: `ClientRequestBase` is listed as uncovered in GAPS.
- **`ClientResponse`** extends `HeadersMixin` (`ClientResponse`, `aiohttp/client_reqrep.py:184-683`, `extends: HeadersMixin`).

### Server-Side Response Hierarchy

```
HeadersMixin, CookieMixin
  +-- StreamResponse  (aiohttp/web_response.py:74-532)
        +-- Response  (aiohttp/web_response.py:535-740)
        +-- WebSocketResponse  (aiohttp/web_ws.py:78-773)
```

- **`StreamResponse`** extends `HeadersMixin` and `CookieMixin` (`StreamResponse`, `aiohttp/web_response.py:74-532`, `extends: HeadersMixin, CookieMixin`).
- **`Response`** extends `StreamResponse` (`Response`, `aiohttp/web_response.py:535-740`, `extends: StreamResponse`).
- **`WebSocketResponse`** extends `StreamResponse` (`WebSocketResponse`, `aiohttp/web_ws.py:78-773`, `extends: StreamResponse`).

### HTTP Message Parsing

```
NamedTuple
  +-- RawRequestMessage  (aiohttp/http_parser.py:99-111)
  +-- RawResponseMessage  (aiohttp/http_parser.py:112-123)
```

- **`RawRequestMessage`** extends `NamedTuple`, called by `HttpRequestParser` (`RawRequestMessage`, `aiohttp/http_parser.py:99-111`).
- **`RawResponseMessage`** extends `NamedTuple`, called by `HttpResponseParser` (`RawResponseMessage`, `aiohttp/http_parser.py:112-123`).

### Exception Hierarchy for Responses

```
Exception
  +-- ClientError  (aiohttp/client_exceptions.py:55-56)
        +-- ClientResponseError  (aiohttp/client_exceptions.py:59-99)
        +-- ClientConnectionError  (aiohttp/client_exceptions.py:123-124)
              +-- ServerConnectionError  (aiohttp/client_exceptions.py:212-213)
                    +-- ServerDisconnectedError  (aiohttp/client_exceptions.py:216-224)
                    +-- ServerTimeoutError  (aiohttp/client_exceptions.py:227-228)
                          [also extends TimeoutError]
```

### HTTP Exception Hierarchy

```
HTTPException (not fully visible)
  +-- HTTPSuccessful  (aiohttp/web_exceptions.py:180-181)
  +-- HTTPRedirection  (aiohttp/web_exceptions.py:176-177)
  +-- HTTPError  (aiohttp/web_exceptions.py:172-173)
        +-- HTTPClientError (not directly shown)
              +-- HTTPBadRequest  (aiohttp/web_exceptions.py:288-289, status_code=400)
              +-- HTTPMisdirectedRequest  (aiohttp/web_exceptions.py:394-395, status_code=421)
```

### Protocol and Infrastructure

```
Protocol (asyncio)
  +-- BaseProtocol  (aiohttp/base_protocol.py:9-100)

ABC
  +-- BaseRunner  (aiohttp/web_runner.py:252-352)
  +-- BaseSite  (aiohttp/web_runner.py:47-78)
  +-- DecompressionBaseHandler  (aiohttp/compression_utils.py:153-180)
```

### Other Notable Classes

- **`ClientWebSocketResponse`** -- no explicit parent shown in clue (`ClientWebSocketResponse`, `aiohttp/client_ws.py:60-560`).
- **`BaseKey`** -- base for context storage keys (`BaseKey`, `aiohttp/helpers.py:837-887`).
- **`BaseTimerContext`** (`BaseTimerContext`, `aiohttp/helpers.py:649-654`).

### What Cannot Be Determined

- The base class(es) of `ClientRequestBase` (listed as uncovered in GAPS).
- The base class of `HTTPException` (not shown in the clue).
- The base class of `HTTPClientError` (intermediate between `HTTPError` and `HTTPBadRequest`).
- Whether `ClientWebSocketResponse` has an explicit parent class.
- Full details of `RequestHandler` and `MultipartResponseWrapper` (listed as uncovered).
- The `HeadersMixin` and `CookieMixin` definitions themselves.
