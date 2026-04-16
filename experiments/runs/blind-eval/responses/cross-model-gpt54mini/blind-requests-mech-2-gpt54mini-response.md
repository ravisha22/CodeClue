# Cross-Model (GPT-5.4-mini): blind-requests-mech-2
Date: 2026-04-16

- Streaming on `Response` centers on `iter_content(chunk_size, decode_unicode)`, which is called by `__iter__`, `content`, `iter_lines`, and `Response`; it can raise `StreamConsumedError`, `TypeError`, `ChunkedEncodingError`, and `ContentDecodingError`. (iter_content (src/requests/models.py:801-857); __iter__ (src/requests/models.py:752-754); content (src/requests/models.py:893-909); iter_lines (src/requests/models.py:859-890); Response (src/requests/models.py:642-1041))
- `content` is backed by `iter_content` and can raise `RuntimeError` if the response body has already been consumed. (content (src/requests/models.py:893-909))
- `iter_lines` streams line-by-line by accumulating chunks from `iter_content`. (iter_lines (src/requests/models.py:859-890))
- Unicode/decoding helpers include `stream_decode_response_unicode(iterator, r)` for stream decoding and `get_unicode_from_response(r)` for returning content in unicode. (stream_decode_response_unicode (src/requests/utils.py:551-565); get_unicode_from_response (src/requests/utils.py:578-614))
- The `Response` model also exposes `json()` for JSON decoding, which raises `RequestsJSONDecodeError` on failure. (json (src/requests/models.py:949-982))
- At response construction time, `build_response` decodes `req.url` from bytes with UTF-8 before building the `Response`. (build_response (src/requests/adapters.py:337-372))
