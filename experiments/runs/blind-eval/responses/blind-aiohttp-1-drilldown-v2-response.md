# Response: blind-aiohttp-1 v2 (with drill-down)
Date: 2026-04-15

The provided artifacts show three distinct request-body paths, but they do **not** expose every implementation detail. Below is the strongest answer supportable from the clue file and snippets alone.

## 1) JSON bodies

`request.json()` is a higher-level convenience over the normal text/body path, not a separate streaming JSON reader. The clue file says `json (aiohttp/web_request.py:654-671)` “Return BODY as JSON,” that it **calls `text`**, and that it can raise `HTTPBadRequest` (`uses: HTTPBadRequest`) [Clue FOCUS: `json` (aiohttp/web_request.py:654-671)].

The lower-level body read path is `read (aiohttp/web_request.py:624-643)`, which “Read[s] request body if present,” is called by `text`, and can raise `HTTPRequestEntityTooLarge` [Clue FOCUS: `read` (aiohttp/web_request.py:624-643)]. From that, the supported conclusion is:
- JSON goes through `request.json()` -> `text` -> the normal request body read path [Clue FOCUS: `json` (aiohttp/web_request.py:654-671); Clue FOCUS: `read` (aiohttp/web_request.py:624-643)].
- Size enforcement that is explicitly shown in the provided materials happens in `request.read()`, via `HTTPRequestEntityTooLarge` [Clue FOCUS: `read` (aiohttp/web_request.py:624-643)].

What I **cannot** prove from the provided materials: the exact JSON decoding function/mechanics inside `request.json()` beyond “Return BODY as JSON” and the fact it calls `text` [Clue FOCUS: `json` (aiohttp/web_request.py:654-671)].

## 2) URL-encoded form bodies

The prompt materials do **not** include the implementation of `request.post()`, so I cannot fully reconstruct the top-level URL-encoded form parsing algorithm. What the clue file does show is:
- `request.read()` is called by `post` [Clue FOCUS: `read` (aiohttp/web_request.py:624-643)].
- `request.multipart()` is also called by `post` [Clue FOCUS: `multipart` (aiohttp/web_request.py:673-680)].

That is enough to support a limited conclusion: `post` appears to be the request-level entry point that may use either the regular body-read path or the multipart path, depending on body format, but the exact branch logic is **not present** in the supplied artifacts [Clue FOCUS: `read` (aiohttp/web_request.py:624-643); Clue FOCUS: `multipart` (aiohttp/web_request.py:673-680)].

There is also a form decoder on multipart body parts: `form (aiohttp/multipart.py:475-493)` is described as “Like read(), but assumes that body parts contain form urlencoded data,” it branches on encoding, calls `get_charset` and `read`, and may raise `ValueError` [Clue FOCUS: `form` (aiohttp/multipart.py:475-493)]. That supports this narrower claim:
- For a **multipart part** that itself contains URL-encoded form data, the part reader uses `get_charset` + `read()` and performs encoding-dependent handling [Clue FOCUS: `form` (aiohttp/multipart.py:475-493)].

What I **cannot** prove from the supplied materials: the exact code path for a top-level non-multipart `application/x-www-form-urlencoded` request body, other than that `post` is connected to the normal `read()` path [Clue FOCUS: `read` (aiohttp/web_request.py:624-643)].

## 3) Multipart uploads

For multipart uploads, the request object does **not** appear to parse the whole body into one blob first. Instead, `multipart (aiohttp/web_request.py:673-680)` says “Return async iterator to process BODY as multipart” and its behavior is `DELEGATE(MultipartReader -> result)` [Clue FOCUS: `multipart` (aiohttp/web_request.py:673-680)].

`MultipartReader` is explicitly described as “Multipart body reader” and it handles multipart structure by calling `_get_boundary`, `_get_part_reader`, `_maybe_release_last_part`, `_read_boundary`, `_read_headers`, and `_read_until_first_boundary` [Clue FOCUS: `MultipartReader` (aiohttp/multipart.py:639-854)].

Each yielded part is handled by `BodyPartReader`, which is described as a “Multipart reader for single body part” [Clue FOCUS: `BodyPartReader` (aiohttp/multipart.py:257-599)]. For each part:
- `read()` “Reads body part data,” accumulates in a loop, and calls `decode_iter` and `read_chunk` [Clue FOCUS: `read` (aiohttp/multipart.py:304-322)].
- `read_chunk(size)` reads chunked content and can branch between length-based vs stream-based reading [Clue FOCUS: `read_chunk` (aiohttp/multipart.py:324-366)].
- `text()` assumes text and calls `get_charset` + `read()` [Clue FOCUS: `text` (aiohttp/multipart.py:459-465)].
- `json()` assumes JSON and also calls `get_charset` + `read()` [Clue FOCUS: `json` (aiohttp/multipart.py:467-473)].
- `form()` assumes URL-encoded form data in that part and calls `get_charset` + `read()` with encoding-sensitive behavior [Clue FOCUS: `form` (aiohttp/multipart.py:475-493)].

So the multipart story supported by the artifacts is:
- `request.multipart()` returns an async multipart reader, not a pre-parsed dict/object [Clue FOCUS: `multipart` (aiohttp/web_request.py:673-680); Clue FOCUS: `MultipartReader` (aiohttp/multipart.py:639-854)].
- Multipart is processed part-by-part through `MultipartReader` / `BodyPartReader` [Clue FOCUS: `MultipartReader` (aiohttp/multipart.py:639-854); Clue FOCUS: `BodyPartReader` (aiohttp/multipart.py:257-599)].
- Individual parts can then be consumed as raw bytes, text, JSON, or URL-encoded form data using the part reader helpers [Clue FOCUS: `read` (aiohttp/multipart.py:304-322); Clue FOCUS: `text` (aiohttp/multipart.py:459-465); Clue FOCUS: `json` (aiohttp/multipart.py:467-473); Clue FOCUS: `form` (aiohttp/multipart.py:475-493)].

## 4) Where payload limits are enforced

The only **explicit** payload-limit enforcement shown in the provided materials is in `request.read()`, which raises `HTTPRequestEntityTooLarge` [Clue FOCUS: `read` (aiohttp/web_request.py:624-643)]. Because `request.json()` goes through `text`, and `read()` is called by `text`, the provided evidence supports that JSON bodies inherit that request-body limit path [Clue FOCUS: `json` (aiohttp/web_request.py:654-671); Clue FOCUS: `read` (aiohttp/web_request.py:624-643)].

For form handling, the clue file shows `post` is connected to `read()` and also to `multipart()` [Clue FOCUS: `read` (aiohttp/web_request.py:624-643); Clue FOCUS: `multipart` (aiohttp/web_request.py:673-680)], but it does **not** show where `post` itself checks limits.

For multipart specifically, the supplied `MultipartReader` / `BodyPartReader` clues show parsing and chunk/line reading behavior, but they do **not** show `HTTPRequestEntityTooLarge` or another explicit payload-limit check inside those multipart reader entries [Clue FOCUS: `MultipartReader` (aiohttp/multipart.py:639-854); Clue FOCUS: `BodyPartReader` (aiohttp/multipart.py:257-599); Clue FOCUS: `read_chunk` (aiohttp/multipart.py:324-366); Clue FOCUS: `readline` (aiohttp/multipart.py:423-450)].

So the most defensible answer is:
- The request-level explicit size limit shown by the artifacts is enforced in `web_request.read()` [Clue FOCUS: `read` (aiohttp/web_request.py:624-643)].
- JSON clearly rides that path via `json()` -> `text` -> body read [Clue FOCUS: `json` (aiohttp/web_request.py:654-671); Clue FOCUS: `read` (aiohttp/web_request.py:624-643)].
- Multipart parsing is delegated to `MultipartReader`, but the provided materials do **not** prove whether there are additional multipart-specific or per-part limits beyond the request-level `read()` limit [Clue FOCUS: `multipart` (aiohttp/web_request.py:673-680); Clue FOCUS: `MultipartReader` (aiohttp/multipart.py:639-854); Clue FOCUS: `BodyPartReader` (aiohttp/multipart.py:257-599)].

## Bottom line

From the supplied clues alone, the request object behaves like this:
1. **JSON**: `request.json()` uses the normal text/body-reading pipeline and can fail with `HTTPBadRequest`; the explicit size-limit hook shown is `request.read()` raising `HTTPRequestEntityTooLarge` [Clue FOCUS: `json` (aiohttp/web_request.py:654-671); Clue FOCUS: `read` (aiohttp/web_request.py:624-643)].
2. **URL-encoded forms**: the exact top-level request parser is not shown, but `post` is tied to the normal body-read path, and multipart body parts have a dedicated `form()` helper that uses `get_charset` + `read()` [Clue FOCUS: `read` (aiohttp/web_request.py:624-643); Clue FOCUS: `multipart` (aiohttp/web_request.py:673-680); Clue FOCUS: `form` (aiohttp/multipart.py:475-493)].
3. **Multipart uploads**: `request.multipart()` returns/delegates to an async `MultipartReader`; parts are processed incrementally via `BodyPartReader`, whose helpers can interpret each part as bytes/text/JSON/form data [Clue FOCUS: `multipart` (aiohttp/web_request.py:673-680); Clue FOCUS: `MultipartReader` (aiohttp/multipart.py:639-854); Clue FOCUS: `BodyPartReader` (aiohttp/multipart.py:257-599); Clue FOCUS: `read` (aiohttp/multipart.py:304-322); Clue FOCUS: `json` (aiohttp/multipart.py:467-473); Clue FOCUS: `form` (aiohttp/multipart.py:475-493)].
4. **Payload limits**: the explicit enforcement point visible in the artifacts is `web_request.read()`; anything more specific for multipart is not demonstrated by the provided materials [Clue FOCUS: `read` (aiohttp/web_request.py:624-643); Clue FOCUS: `MultipartReader` (aiohttp/multipart.py:639-854)].
