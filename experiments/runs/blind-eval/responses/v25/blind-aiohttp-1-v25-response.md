# v2.5 Response: blind-aiohttp-1
Date: 2026-04-16

## Question
If a handler reads incoming data from different body formats, what does the request object actually do for JSON, URL-encoded forms, and multipart uploads, and where are payload limits enforced?

## Answer

### JSON Body Handling

**Server-side (`BaseRequest.json`)**: The `json` method (FOCUS: `json` at `aiohttp/web_request.py:654-671`) first calls `self.text()` to read the entire body as text, then validates the content type. The source snippet confirms:

```python
body = await self.text()
if content_type:
    if not is_expected_content_type(self.content_type, content_type):
        raise HTTPBadRequest(text="Attempt to decode JSON with unexpected mimetype: %s" % self.content_type)
return loads(body)
```

It defaults to expecting `"application/json"` and raises `HTTPBadRequest` (FOCUS: `json` uses `HTTPBadRequest` from `web_exceptions`) if the content type doesn't match. The `loads` parameter defaults to `DEFAULT_JSON_DECODER` but is configurable.

**Multipart JSON**: `BodyPartReader.json` (FOCUS: `json` at `aiohttp/multipart.py:467-473`) reads a body part assuming JSON data by calling `get_charset` and `read`.

**Client-side**: `_update_body_from_data` (FOCUS: `_update_body_from_data` at `aiohttp/client_reqrep.py:1137-1180`) handles JSON through the payload registry. The source snippet shows that if the body is not `FormData`, it tries `payload.PAYLOAD_REGISTRY.get(body, disposition=None)`, and if that raises `payload.LookupError`, falls back to wrapping in `FormData`. The `JsonPayload` (FOCUS: `JsonPayload` at `aiohttp/payload.py:924-940`, extends `BytesPayload`) and `JsonBytesPayload` (FOCUS: `JsonBytesPayload` at `aiohttp/payload.py:943-963`, extends `BytesPayload`) handle JSON serialization.

### URL-Encoded Form Handling

**Server-side**: The `BaseRequest` class (FOCUS: `BaseRequest` at `aiohttp/web_request.py:109-823`) has a `post` method (referenced via `called_by: post` on `read` and `multipart`). The `read` method (FOCUS: `read` at `aiohttp/web_request.py:624-643`) reads the raw body, and `post` processes it (though `post` itself is not in FOCUS, `multipart` is `called_by: post`).

**Client-side**: `FormData` (FOCUS: `FormData` uses in `_update_body_from_data`) is central. When `_update_body_from_data` receives a `FormData` instance, it calls `body()` on it (source snippet: `if isinstance(body, FormData): body = body()`). The `__call__` method of `FormData` (referenced at `aiohttp/formdata.py:163-167`) branches: `BRANCH(self._is_multipart -> return self._gen_form_data..., else -> return self._gen_form_urlencoded)` — so `FormData` can produce either multipart or URL-encoded output.

The `_gen_form_data` method (FOCUS: `_gen_form_data` at `aiohttp/formdata.py:128-161`) encodes using multipart/form-data MIME format, accumulating over `self._fields`. The URL-encoded path uses `_gen_form_urlencoded`.

### Multipart Upload Handling

**Server-side**: `BaseRequest.multipart` (FOCUS: `multipart` at `aiohttp/web_request.py:673-680`) delegates to `MultipartReader`: `DELEGATE(MultipartReader -> result)`. It is called by `post`.

`MultipartReader` (FOCUS: `MultipartReader` at `aiohttp/multipart.py:639-854`) is the main multipart body reader. It calls `read_chunk`, `readline`, `_get_boundary`, `_get_part_reader`, `_maybe_release_last_part`, `_read_boundary`, `_read_headers`, `_read_until_first_boundary`. It raises `ValueError`, `StopAsyncIteration`, `BadHttpMessage`, and `RuntimeError`.

`BodyPartReader` (FOCUS: `BodyPartReader` at `aiohttp/multipart.py:257-599`) handles individual body parts with `chunk_size=8192`. It provides:
- `read` (FOCUS: `read` at `aiohttp/multipart.py:304-322`) — accumulates data via `ACCUMULATE(data.extend loop -> data)`, calling `decode_iter` and `read_chunk`.
- `read_chunk` (FOCUS: `read_chunk` at `aiohttp/multipart.py:324-366`) — reads chunks, branching on whether `_length` is known. The source snippet shows it handles base64 content-transfer-encoding by ensuring chunks align to 4-byte boundaries.
- `decode_iter` (source snippet at `aiohttp/multipart.py:524-538`) — applies content-transfer decoding first, then content decoding (decompression) if needed, offloading to an executor for large payloads.
- `json` and `text` methods for reading parts as JSON or text.

**Client-side multipart writing**: `MultipartWriter` (FOCUS: `MultipartWriter` at `aiohttp/multipart.py:860-1146`, extends `Payload`) handles writing multipart bodies. It calls `append`, `append_payload`, `append_form`, `append_json` and uses `MultipartPayloadWriter` (FOCUS: `:1149-1204`).

### Payload Limit Enforcement

**Server-side `read` method**: The `read` method (FOCUS: `read` at `aiohttp/web_request.py:624-643`) is the primary enforcement point. It raises `HTTPRequestEntityTooLarge` (uses: `HTTPRequestEntityTooLarge` from `web_exceptions`). The `BaseRequest` class itself documents this in its `uses:` — `HTTPRequestEntityTooLarge (web_exceptions)`.

**Client-side body size**: In `_update_body_from_data` (source snippet), after setting `self._body = body`, the code checks: `if (size := body.size) is not None: self.headers[hdrs.CONTENT_LENGTH] = str(size)` — otherwise enables chunked transfer encoding (`self.chunked = True`). This manages Content-Length but is not a limit enforcement.

**`AppRunner._make_request`**: The source snippet for `AppRunner._make_request` shows `client_max_size=self.app._client_max_size` is passed to `Request` construction, indicating the Application stores a configurable max size that is enforced during request body reads.

**WebSocket message limits**: `WebSocketReader` (referenced in `WebSocketResponse._post_start`) is configured with `self._max_msg_size` (from the source snippet of `_post_start` at `aiohttp/web_ws.py:376-398`), indicating WebSocket message size limits are also enforced.

### Response Body Setting

The `Response.body` setter (source snippet at `aiohttp/web_response.py:610-633`) accepts `bytes`, `bytearray`, or payloads via `PAYLOAD_REGISTRY.get(body)`. If lookup fails, it raises `ValueError("Unsupported body type")`. It auto-sets Content-Type from the payload if not already set.

The `Response.text` setter (source snippet at `aiohttp/web_response.py:645-654`) encodes text to bytes using the charset (defaulting to utf-8), auto-setting content type to `text/plain` if it was `application/octet-stream`.

### What Cannot Be Determined

Per GAPS: "uncovered: HTTPBadRequest, HTTPMisdirectedRequest, HttpBadRequest, HttpRequestParser." The exact implementation of `HTTPRequestEntityTooLarge` (the threshold value and comparison logic) and the `post` method's full parsing of URL-encoded form data are not directly visible in the clue or snippets. The `_gen_form_urlencoded` implementation details are also not provided.
