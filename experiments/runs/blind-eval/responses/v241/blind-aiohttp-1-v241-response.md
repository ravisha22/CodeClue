# v2.4.1 Response: blind-aiohttp-1
Date: 2026-04-16

## How the Request Object Handles JSON, URL-Encoded Forms, and Multipart Uploads; Payload Limit Enforcement

### JSON Body Reading

The server-side `json()` method on the request object (`json`, `aiohttp/web_request.py:654-671`) works by first calling `self.text()` to obtain the full body as a string. It then optionally validates the Content-Type: if a `content_type` parameter is supplied (defaulting to `"application/json"`), it checks `is_expected_content_type(self.content_type, content_type)` and raises `HTTPBadRequest` with an explanatory message if the MIME type does not match (drill-down snippet, `aiohttp/web_request.py:654-671`). Finally, the raw text is decoded via the caller-supplied `loads` function (defaulting to `DEFAULT_JSON_DECODER`) and the result is returned.

### URL-Encoded Form Reading

Multipart-level form reading is handled by `form()` in `BodyPartReader` (`form`, `aiohttp/multipart.py:475-493`). It determines the character encoding -- using `get_charset()` if available, otherwise falling back to a default -- then calls `read()` to consume the body part data entirely. A `ValueError` is raised if encoding resolution fails (`form`, `aiohttp/multipart.py:475-493`). The clue file lists `post` as an uncovered symbol in the GAPS section (`GAPS, uncovered: post`), so the top-level `request.post()` mechanism for URL-encoded forms **cannot be fully determined** from this prompt alone.

### Multipart Upload Reading

The `multipart()` method on `BaseRequest` (`multipart`, `aiohttp/web_request.py:673-680`) delegates to `MultipartReader` to return an async iterator for processing the body as multipart. `MultipartReader` (`MultipartReader`, `aiohttp/multipart.py:639-854`) orchestrates boundary detection and part iteration, calling `_get_boundary`, `_read_until_first_boundary`, `_read_headers`, `_get_part_reader`, and `read_chunk`/`readline` internally.

Each individual part is handled by `BodyPartReader` (`BodyPartReader`, `aiohttp/multipart.py:257-599`, `attrs: chunk_size=8192`). It reads data in chunks via `read_chunk()` (`read_chunk`, `aiohttp/multipart.py:324-366`), which branches on whether a Content-Length is present: if `self._length` is set it calls `_read_chunk_from_length(size)`, otherwise `_read_chunk_from_stream(size)` (drill-down snippet, `aiohttp/multipart.py:324-366`). Special handling exists for base64 Content-Transfer-Encoding, ensuring chunk sizes align to 4-byte boundaries. The `read()` method (`read`, `aiohttp/multipart.py:304-322`) accumulates data from `read_chunk`/`decode_iter` into a complete buffer. Decoding is performed by `decode_iter()` (`decode_iter`, `aiohttp/multipart.py:524-538`), which applies content-transfer decoding and, if content-encoding is set, offloads decompression to an executor for large payloads.

When multipart processing finishes, `_finish()` (`_finish`, `aiohttp/web_request.py:813-823`) releases file descriptors for any `tempfile.TemporaryFile`-backed `FileField` instances uploaded via POST.

### Client-Side Body Preparation

On the client side, `_update_body_from_data()` (`_update_body_from_data`, `aiohttp/client_reqrep.py:1137-1180`) handles body encoding. If `body` is `None`, `_EMPTY_BODY` is used and Content-Length is set to `"0"` for non-GET methods. If `body` is a `FormData` instance, it is called (`body()`) to produce the payload. Otherwise the code attempts `payload.PAYLOAD_REGISTRY.get(body)`, and on `LookupError` falls back to wrapping in `FormData(body)()`. After the body payload is set, Content-Length is derived from `body.size` if available; otherwise chunked encoding is enabled. Payload headers (e.g., Content-Type) are then copied to request headers (drill-down snippet, `aiohttp/client_reqrep.py:1137-1180`).

### Payload Limit Enforcement

The server-side `read()` method (`read`, `aiohttp/web_request.py:624-643`) enforces payload size limits. It raises `HTTPRequestEntityTooLarge` (from `web_exceptions`) if the body exceeds the configured limit. The limit itself is exposed via `client_max_size` property on `BaseRequest`. Both `post` and `text` call `read()`, so the limit applies transitively to JSON and form reads as well (`read called_by: post, text, BaseRequest`).

### What Cannot Be Determined

- The exact implementation of `post()` (listed as uncovered in GAPS) -- how it distinguishes URL-encoded vs multipart, and how it populates `_post`.
- The implementation of `_read_chunk_from_length` and `_read_chunk_from_stream` (listed as uncovered in GAPS).
- The exact Content-Length threshold logic inside `read()` that triggers `HTTPRequestEntityTooLarge`.
- How `text()` on the request decodes bytes to string (its source is not provided).
