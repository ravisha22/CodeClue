# v2.4 Response: blind-aiohttp-1
Date: 2026-04-16

## Question
If a handler reads incoming data from different body formats, what does the request object actually do for JSON, URL-encoded forms, and multipart uploads, and where are payload limits enforced?

## Answer

### JSON Body Reading

The server-side request object provides `json()` as an async method (`json`, `aiohttp/web_request.py:654-671`). The source snippet shows it first calls `await self.text()` to read the full body as a string, then validates the content type: if the caller passes a `content_type` parameter (defaulting to `"application/json"`), it checks via `is_expected_content_type(self.content_type, content_type)` and raises `HTTPBadRequest` with the message `"Attempt to decode JSON with unexpected mimetype: %s"` if the content type doesn't match (`json source snippet, web_request.py:654-671`). On success, it calls `loads(body)` with a configurable `JSONDecoder` (defaulting to `DEFAULT_JSON_DECODER`). The `text()` method itself calls `read()` (`read`, `aiohttp/web_request.py:624-643`), which is the common raw-body reader.

On the multipart side, `BodyPartReader` also has a `json()` method (`json`, `aiohttp/multipart.py:467-473`) that calls `get_charset` and `read` to read the body part data and parse it as JSON.

### URL-Encoded Form Data

The `form()` method on `BodyPartReader` (`form`, `aiohttp/multipart.py:475-493`) assumes the body part contains form-urlencoded data. It determines encoding by either calling `get_charset` or using a provided default, then calls `read()` to obtain the raw bytes. If encoding cannot be determined, it raises `ValueError` (`form`, `aiohttp/multipart.py:475-493`).

Server-side form POST data is accessed via `post` on `BaseRequest`, which is listed as a caller of both `read` and `multipart` (`BaseRequest`, `aiohttp/web_request.py:109-823`). The `post` method delegates to `multipart()` for multipart bodies and calls `read()` for standard form bodies.

### Multipart Uploads

The `multipart()` method on `BaseRequest` (`multipart`, `aiohttp/web_request.py:673-680`) delegates to `MultipartReader` to return an async iterator for processing multipart body parts. `MultipartReader` (`MultipartReader`, `aiohttp/multipart.py:639-854`) handles boundary parsing, header reading, and part iteration by calling `read_chunk`, `readline`, `_get_boundary`, `_get_part_reader`, `_maybe_release_last_part`, `_read_boundary`, `_read_headers`, and `_read_until_first_boundary`. It raises `ValueError`, `StopAsyncIteration`, `BadHttpMessage`, and `RuntimeError` on malformed input. It uses `HeadersParser` from `http` and `BadHttpMessage` from `http_exceptions`.

Individual parts are read via `BodyPartReader` (`BodyPartReader`, `aiohttp/multipart.py:257-599`), which has a default `chunk_size=8192`. The `read_chunk()` method (`read_chunk`, `aiohttp/multipart.py:324-366`) branches: if `_length` is set, it delegates to `_read_chunk_from_length`; otherwise to `_read_chunk_from_stream`. The source snippet shows special handling for base64 content-transfer-encoding, padding reads to multiples of 4 bytes. The `read()` method (`read`, `aiohttp/multipart.py:304-322`) accumulates data via `decode_iter` and `read_chunk`.

Content decoding happens through `decode_iter` (`decode_iter`, `aiohttp/multipart.py:524-538`), which first applies content-transfer decoding (`_apply_content_transfer_decoding`), then conditionally decompresses via `_decode_content_async` if content-encoding headers indicate it. The docstring notes decompression is offloaded to an executor for large payloads.

### Client-Side Body Handling

On the client side, `_update_body_from_data` (`_update_body_from_data`, `aiohttp/client_reqrep.py:1137-1180`) handles body serialization. The source snippet shows:
- If `body is None`, sets `_body` to empty and sets `Content-Length: 0` for non-GET methods.
- If `body` is `FormData`, it calls `body()` to generate the payload (`FormData`, `formdata`).
- Otherwise, it attempts `payload.PAYLOAD_REGISTRY.get(body, disposition=None)`. On `payload.LookupError`, it wraps the body in `FormData(body, boundary=...)()` as fallback.
- After setting the body, it sets `Content-Length` if the payload size is known, or enables chunked encoding if not.
- It copies payload headers (e.g., Content-Type) into request headers, skipping any already-set or skip-listed headers.

### Payload Limit Enforcement

Payload size limits are enforced in `read()` on `BaseRequest` (`read`, `aiohttp/web_request.py:624-643`): it raises `HTTPRequestEntityTooLarge` (from `web_exceptions`) when the body exceeds the configured limit. The `AppRunner` source snippet shows `client_max_size` is passed when constructing `Request` objects (`AppRunner._make_request source snippet, web_runner.py:476-494`), indicating the limit is configured at the application/runner level.

The `HTTPRequestEntityTooLarge` class (`HTTPRequestEntityTooLarge`, `aiohttp/web_exceptions.py:366-375`) has `status_code=413` and extends `HTTPClientError`.

### Cannot Be Determined from Clue File

- The exact default value of `client_max_size` is not specified in the clue file.
- The internal implementation of `text()` on `BaseRequest` (called by `json()`) is not shown.
- The full implementation of `post()` on `BaseRequest` is not in the FOCUS or source snippets.
- `HttpRequestParser` and `PayloadRegistry` are listed as uncovered in the GAPS section, so how the raw HTTP body is parsed from the wire and how payload types are registered cannot be fully determined.
- `BufferedReaderPayload` behavior is uncovered.
