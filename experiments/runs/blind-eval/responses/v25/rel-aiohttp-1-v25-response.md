# v2.5 Response: rel-aiohttp-1
Date: 2026-04-16

## Question
What is the class hierarchy for request and response objects in aiohttp, and which classes extend which base classes?

## Answer

### Request Class Hierarchy

1. **`BaseRequest`** (FOCUS: `BaseRequest` at `aiohttp/web_request.py:109-823`)
   - **extends: `HeadersMixin`**
   - The foundational server-side request class. Imports from `asyncio`, `io`, `socket`, `string`, `tempfile`. Calls `_etag_values`, `_if_match_or_none_impl`, `get_extra_info`, `multipart`, `read`, `text`, `FileField`. Uses `ETag` (helpers), `MultipartReader` (multipart), `HTTPRequestEntityTooLarge` and `HTTPUnsupportedMediaType` (web_exceptions).

2. **`Request`** (FOCUS: `Request` at `aiohttp/web_request.py:826-884`)
   - **extends: `BaseRequest`**
   - The concrete server-side request class used by the application layer.

3. **`_make_request`** (FOCUS: `_make_request` at `aiohttp/web_server.py:97-105`)
   - Factory function that creates `BaseRequest` instances. Behavior: `DELEGATE(BaseRequest -> result)`.

### Client-Side Request Types

4. **`_RequestInfo` (NamedTuple)** (FOCUS: `_RequestInfo` at `aiohttp/client_reqrep.py:102-106`)
   - **extends: `NamedTuple`**
   - Base named tuple for request metadata.

5. **`RequestInfo`** (FOCUS: `RequestInfo` at `aiohttp/client_reqrep.py:109-124`)
   - **extends: `_RequestInfo`**
   - Wraps `_RequestInfo` with a custom `__new__` constructor.

6. **`ClientRequest`** (FOCUS: `ClientRequest` at `aiohttp/client_reqrep.py:954-1434`)
   - **extends: `ClientRequestBase`**
   - The client-side HTTP request. Calls `_update_auto_headers`, `_update_body`, `_update_body_from_data`, `_update_content_encoding`, `_update_cookies`, `_update_expect_continue`, `_update_proxy`, `_update_transfer_encoding`. Uses `CIMultiDict` (multidict), `FormData` (formdata), `SimpleCookie` (http.cookies).

7. **`ClientRequestArgs`** (FOCUS: `ClientRequestArgs` at `aiohttp/client_reqrep.py:930-951`)
   - **extends: `TypedDict`**
   - Type specification for client request arguments.

8. **`_RequestOptions`** (FOCUS: `_RequestOptions` at `aiohttp/client.py:176-203`)
   - **extends: `TypedDict`**
   - Configuration options for requests.

### Response Class Hierarchy

9. **`StreamResponse`** (FOCUS: `StreamResponse` at `aiohttp/web_response.py:74-532`)
   - **extends: `HeadersMixin`, `CookieMixin`**
   - Base server-side response. Calls `_generate_content_type_header`, `_prepare_headers`, `_set_status`, `_start_compression`, `_write_headers`, `drain`, `enable_compression`, `write`.

10. **`Response`** (FOCUS: `Response` at `aiohttp/web_response.py:535-740`)
    - **extends: `StreamResponse`**
    - The standard HTTP response with body. Called by `json_bytes_response` and `json_response`.

11. **`WebSocketResponse`** (FOCUS: `WebSocketResponse` at `aiohttp/web_ws.py:78-773`)
    - **extends: `StreamResponse`**
    - Server-side WebSocket response. Calls `_cancel_heartbeat`, `_cancel_pong_response_cb`, `_close_transport`, `_handle_ping_pong_exception`, `_handshake`, etc.

12. **`FileResponse`** (FOCUS: `FileResponse` at `aiohttp/web_fileresponse.py:79-406`)
    - **extends: `StreamResponse`**
    - Response for serving files. Calls `_etag_match`, `_get_file_path_stat_encoding`, `_not_modified`, `_precondition_failed`, `_prepare_open_file`, `_sendfile`, `_sendfile_fallback`.

### Client-Side Response

13. **`ClientResponse`** (FOCUS: `ClientResponse` at `aiohttp/client_reqrep.py:184-683`)
    - **extends: `HeadersMixin`**
    - Client-side HTTP response. Calls `_cleanup_writer`, `_notify_content`, `_release_connection`, `_wait_released`, `close`, `get_encoding`, `read`, `release`. Raises `ClientResponseError`, `ClientConnectionError`.

14. **`ClientWebSocketResponse`** (FOCUS: `ClientWebSocketResponse` at `aiohttp/client_ws.py:60-560`)
    - No explicit `extends:` listed in the FOCUS entry, making its base class **indeterminate from the clue**. Calls `_cancel_heartbeat`, `_cancel_pong_response_cb`, `_handle_ping_pong_exception`, etc.

### Raw Message Types

15. **`RawRequestMessage`** (FOCUS: `RawRequestMessage` at `aiohttp/http_parser.py:99-111`)
    - **extends: `NamedTuple`**
    - Produced by `HttpRequestParser`.

16. **`RawResponseMessage`** (FOCUS: `RawResponseMessage` at `aiohttp/http_parser.py:112-123`)
    - **extends: `NamedTuple`**
    - Produced by `HttpResponseParser`.

### Error Response Classes

17. **`ClientResponseError`** (FOCUS: `ClientResponseError` at `aiohttp/client_exceptions.py:59-99`)
    - **extends: `ClientError`**
    - Base for exceptions occurring after getting a response.

18. **`HTTPBadRequest`** (FOCUS: `HTTPBadRequest` at `aiohttp/web_exceptions.py:288-289`)
    - **extends: `HTTPClientError`**, status_code=400.

19. **`HTTPMisdirectedRequest`** (FOCUS: `HTTPMisdirectedRequest` at `aiohttp/web_exceptions.py:394-395`)
    - **extends: `HTTPClientError`**, status_code=421.

20. **`HttpBadRequest`** (FOCUS: `HttpBadRequest` at `aiohttp/http_exceptions.py:55-57`)
    - **extends: `BadHttpMessage`**, code=400.

### Protocol and Infrastructure Base Classes

21. **`BaseProtocol`** (FOCUS: `BaseProtocol` at `aiohttp/base_protocol.py:9-100`)
    - **extends: `Protocol`**

22. **`ResponseHandler`** (FOCUS: `ResponseHandler` at `aiohttp/client_proto.py:31-371`)
    - **extends: `BaseProtocol`**

23. **`BaseSite`** (FOCUS: `BaseSite` at `aiohttp/web_runner.py:47-78`)
    - **extends: `ABC`**

24. **`BaseRunner`** (FOCUS: `BaseRunner` at `aiohttp/web_runner.py:252-352`)
    - **extends: `ABC`**

25. **`DecompressionBaseHandler`** (FOCUS: `DecompressionBaseHandler` at `aiohttp/compression_utils.py:153-180`)
    - **extends: `ABC`**

26. **`_FileResponseResult`** (FOCUS: `_FileResponseResult` at `aiohttp/web_fileresponse.py:61-67`)
    - **extends: `Enum`**

### Summary Hierarchy Diagram

```
HeadersMixin
├── BaseRequest (web_request.py)
│   └── Request (web_request.py)
├── ClientResponse (client_reqrep.py)
└── (also mixed into StreamResponse)

HeadersMixin + CookieMixin
└── StreamResponse (web_response.py)
    ├── Response (web_response.py)
    ├── WebSocketResponse (web_ws.py)
    └── FileResponse (web_fileresponse.py)

Protocol
└── BaseProtocol (base_protocol.py)
    └── ResponseHandler (client_proto.py)

ClientError
└── ClientResponseError (client_exceptions.py)

NamedTuple
├── _RequestInfo → RequestInfo (client_reqrep.py)
├── RawRequestMessage (http_parser.py)
└── RawResponseMessage (http_parser.py)
```

### What Cannot Be Determined

Per GAPS: "uncovered: on_request_start, on_response_chunk_received, on_response_prepare, request." The base class of `ClientWebSocketResponse` is not stated in the clue. The parent classes `HeadersMixin`, `CookieMixin`, `ClientError`, `HTTPClientError`, `HTTPServerError`, `BadHttpMessage`, and `ClientRequestBase` are referenced but their own definitions are not in the FOCUS section.
