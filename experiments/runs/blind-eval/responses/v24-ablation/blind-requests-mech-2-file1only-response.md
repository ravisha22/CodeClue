# v2.4 Ablation (File 1 Only): blind-requests-mech-2
Date: 2026-04-16

A `Response` is built from the adapter layer. `build_response` constructs the `Response`, and one visible edge case is that it decodes `req.url` from bytes to UTF-8 when necessary before storing it. [build_response (src/requests/adapters.py:337-372)]

Streaming is centered on `iter_content`, which calls `generate` and is the basis for both `Response.__iter__` and `iter_lines`. [iter_content (src/requests/models.py:801-857); __iter__ (src/requests/models.py:752-754); iter_lines (src/requests/models.py:859-890)]

The important streaming edge cases are explicit in `iter_content`: it can raise `StreamConsumedError`, `TypeError`, `ChunkedEncodingError`, and `ContentDecodingError`, and it also uses `ConnectionError`. [iter_content (src/requests/models.py:801-857); StreamConsumedError (src/requests/exceptions.py:128-129); ContentDecodingError (src/requests/exceptions.py:124-125)]

Buffered access layers on top of that same machinery. `content` obtains bytes via `iter_content` and can raise `RuntimeError`; `iter_lines` accumulates chunks coming from `iter_content`. [content (src/requests/models.py:893-909); iter_lines (src/requests/models.py:859-890)]

Unicode/decoded views are also layered: `stream_decode_response_unicode` stream-decodes an iterator, and `get_unicode_from_response` derives unicode output using `get_encoding_from_headers`. `text` is the unicode body view, while `json` decodes the body as JSON and can raise `RequestsJSONDecodeError`. [stream_decode_response_unicode (src/requests/utils.py:551-565); get_unicode_from_response (src/requests/utils.py:578-614); text (src/requests/models.py:912-947); json (src/requests/models.py:949-982)]

What I cannot determine from this clue file: the exact buffering/caching policy for `content`/`text`, the full body of `generate`, or the exact close/connection-release timing for every streaming path. [Response (src/requests/models.py:642-1041); GAPS]
