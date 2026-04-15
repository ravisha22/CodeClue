# Response: blind-aiohttp-1 (with drill-down)
2026-04-15

Based only on the provided clue file and drill-down snippets:

## What the request object does

### 1) JSON bodies
`request.json()` does **not** parse raw bytes directly. It first does `body = await self.text()`, then validates the request content type against the expected JSON type (`"application/json"` by default), raising `HTTPBadRequest` if the mimetype is unexpected, and only then calls `loads(body)`. [Source snippet: `aiohttp/web_request.py L654-671`; Clue: `json (aiohttp/web_request.py:654-671)`]

Because `text()` is listed as calling `read()`, and `read()` is the request-body reader, the JSON path is effectively: **request body -> `read()` -> `text()` -> `json()` -> `loads(...)`**. [Clue: `read (aiohttp/web_request.py:624-643)` with `called_by: post, text, BaseRequest`; Source snippet: `aiohttp/web_request.py L654-671`]

### 2) URL-encoded forms
The provided materials do **not** include the implementation of `request.post()`, so I cannot fully prove the exact top-level behavior for a normal URL-encoded request body (for example, the exact parser used or return shape). What I **can** prove is that `post` relies on the request body reader (`read`) and also has a multipart path (`multipart`), because both `read()` and `multipart()` are marked as `called_by: post`. [Clue: `read (aiohttp/web_request.py:624-643)`; Clue: `multipart (aiohttp/web_request.py:673-680)`]

The clue file also shows a multipart-part helper `form (aiohttp/multipart.py:475-493)`, described as: "Like read(), but assumes that body parts contain form urlencoded data." It uses `get_charset` and `read`, branches on encoding, and can raise `ValueError`. That proves there is a URL-encoded-form decoding helper at the **multipart part** level. [Clue: `form (aiohttp/multipart.py:475-493)`]

So, from the provided evidence alone, the strongest safe conclusion is: top-level form handling goes through `post`, which depends on `read()` for body consumption, but the exact top-level URL-encoded parsing logic is **not shown** in the provided prompt. [Clue: `read (aiohttp/web_request.py:624-643)`; Clue: `multipart (aiohttp/web_request.py:673-680)`]

### 3) Multipart uploads
For multipart uploads, the request object does **not** itself appear to eagerly parse the whole body into one object. Instead, `request.multipart()` is described as: "Return async iterator to process BODY as multipart" and its behavior is `DELEGATE(MultipartReader -> result)`. [Clue: `multipart (aiohttp/web_request.py:673-680)`]

That means the request hands multipart processing off to `MultipartReader`, and actual part consumption happens through multipart reader objects rather than directly in the request method. [Clue: `multipart (aiohttp/web_request.py:673-680)`; Clue: `MultipartReader (aiohttp/multipart.py:639-854)`]

Each multipart part is handled by `BodyPartReader`. Its `read()` method accumulates chunks until EOF, and optionally decodes them via `decode_iter(...)` if `decode=True`. [Source snippet: `aiohttp/multipart.py L478-496`; Clue: `read (aiohttp/multipart.py:304-322)`]

`BodyPartReader.read_chunk()` chooses between two strategies:
- if the part has a known `_length`, it reads from `_read_chunk_from_length(size)`; [Source snippet: `aiohttp/multipart.py L503-507, L542-550`; Clue: `read_chunk (aiohttp/multipart.py:324-366)`]
- otherwise it reads from `_read_chunk_from_stream(size)`, which searches the incoming stream for the multipart boundary. [Source snippet: `aiohttp/multipart.py L507-509, L552-584`; Clue: `read_chunk (aiohttp/multipart.py:324-366)`]

For `subtype == "form-data"`, `BodyPartReader` sets `_is_form_data = True`, and then sets `length = None if self._is_form_data else self.headers.get(CONTENT_LENGTH, None)`. So for form-data parts, part-level `Content-Length` is intentionally not used, which pushes reads onto the boundary-scanning path instead of fixed-length reads. [Source snippet: `aiohttp/multipart.py L452-456`; Source snippet: `aiohttp/multipart.py L503-509`]

The part reader also has convenience methods above the raw read path: the clue file says multipart `json()` is "Like read(), but assumes that body parts contains JSON data" and calls `get_charset` and `read`; multipart `form()` is similarly "Like read(), but assumes that body parts contain form urlencoded data" and also calls `get_charset` and `read`. [Clue: `json (aiohttp/multipart.py:467-473)`; Clue: `form (aiohttp/multipart.py:475-493)`]

So, for multipart uploads, the request object’s role is mainly to return a multipart iterator; the heavy lifting is done later by `MultipartReader`/`BodyPartReader`, which can read parts fully or chunk-by-chunk and can apply per-part helpers such as `.json()` and `.form()`. [Clue: `multipart (aiohttp/web_request.py:673-680)`; Source snippet: `aiohttp/multipart.py L478-540`; Clue: `json (aiohttp/multipart.py:467-473)`; Clue: `form (aiohttp/multipart.py:475-493)`]

## Where payload limits are enforced

The clearest request-level enforcement point shown in the prompt is `request.read()`: the clue file explicitly says `read (aiohttp/web_request.py:624-643)` "Read request body if present" and that it `raises: HTTPRequestEntityTooLarge`. [Clue: `read (aiohttp/web_request.py:624-643)`]

Because `text()` calls `read()`, and `json()` calls `text()`, JSON requests inherit request-size enforcement through `read()`. [Clue: `read (aiohttp/web_request.py:624-643)` with `called_by: post, text, BaseRequest`; Source snippet: `aiohttp/web_request.py L654-671`]

Because `post` is also listed as a caller of `read()`, non-multipart form handling that flows through `post` also appears to inherit request-size enforcement from `read()`. [Clue: `read (aiohttp/web_request.py:624-643)`]

For multipart uploads, the prompt shows `request.multipart()` delegating to `MultipartReader`, but it does **not** show a request-level size check inside that method. So I can say that `request.read()` is an explicit payload-limit enforcement point, while the provided multipart snippet does not expose an equivalent request-level size check in `multipart()`. [Clue: `multipart (aiohttp/web_request.py:673-680)`; Clue: `read (aiohttp/web_request.py:624-643)`]

There is also a multipart-related size control visible in `BodyPartReader.__init__`: it accepts `max_decompress_size` and stores it on `self._max_decompress_size`. However, the provided snippet does **not** show where that value is checked, so I cannot safely claim how or where decompression-size enforcement occurs. [Source snippet: `aiohttp/multipart.py L436-445, L460-461`]

## Bottom line

From the provided evidence only:
- **JSON**: `request.json()` = `await self.text()` -> content-type check -> `loads(body)`. [Source snippet: `aiohttp/web_request.py L654-671`]
- **Top-level URL-encoded forms**: the exact parser is **not shown**, but `post` clearly depends on `read()` and therefore on the standard request-body read path. [Clue: `read (aiohttp/web_request.py:624-643)`; Clue: `multipart (aiohttp/web_request.py:673-680)`]
- **Multipart uploads**: `request.multipart()` delegates to `MultipartReader`; per-part reading/parsing is performed by `BodyPartReader`, which supports full reads, chunked reads, and helper methods like part-level `.json()` / `.form()`. [Clue: `multipart (aiohttp/web_request.py:673-680)`; Source snippet: `aiohttp/multipart.py L478-540`; Clue: `json (aiohttp/multipart.py:467-473)`; Clue: `form (aiohttp/multipart.py:475-493)`]
- **Payload limits**: the explicit request-level limit enforcement shown in the materials is in `request.read()`, which raises `HTTPRequestEntityTooLarge`. [Clue: `read (aiohttp/web_request.py:624-643)`]
