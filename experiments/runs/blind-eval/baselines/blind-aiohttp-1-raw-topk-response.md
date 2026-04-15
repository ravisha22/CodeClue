# Response: blind-aiohttp-1 (raw-topk baseline)
Date: 2026-04-15

From the provided prompt, the only parsing code shown is in `aiohttp\multipart.py`; `aiohttp\formdata.py` is an encoder for outgoing form bodies, not the request parser.

- **JSON:** `BodyPartReader.json` reads the entire part with `read(decode=True)`, returns `None` for an empty body, picks the charset from `Content-Type` (default `utf-8`), then calls `json.loads(...)` (`aiohttp\multipart.py`, lines 649-655 in the prompt).
- **URL-encoded forms:** `BodyPartReader.form` also reads the whole part, returns `[]` when empty, decodes using the supplied encoding or the part charset, then parses with `parse_qsl(..., keep_blank_values=True)` (`aiohttp\multipart.py`, lines 657-675). For comparison, `FormData._gen_form_urlencoded` is clearly the **write** path: it builds `urlencode(...)` bytes for `application/x-www-form-urlencoded` (`aiohttp\formdata.py`, lines 118-136).
- **Multipart uploads:** multipart bodies are streamed as parts. `BodyPartReader.read` and `read_chunk` consume data until the boundary (`aiohttp\multipart.py`, lines 486-603), and the convenience helpers (`text`, `json`, `form`) sit on top of that part reader (`lines 641-675`). `FormData._gen_form_data` is again the outbound multipart builder, not inbound request parsing (`aiohttp\formdata.py`, lines 138-171).
- **Limits:** the only explicit payload limit visible here is the decompression cap. `BodyPartReader.__init__` stores `max_decompress_size` (`aiohttp\multipart.py`, lines 444-470), and `_decode_content` / `_decode_content_async` pass it to `ZLibDecompressor(...).decompress...(..., max_length=self._max_decompress_size)` (`lines 722-743`). Also, `BodyPartReaderPayload.as_bytes` intentionally refuses to buffer a body part in memory and requires streaming via `write()` (`lines 804-818`).

What is **not** shown in this prompt is any `Request.json()`, `Request.post()`, or global request-body limit logic. So, based only on the supplied source, I can describe multipart/body-part parsing and the decompression limit above, but I cannot attribute any broader request-level size enforcement to code that is not in the prompt.
