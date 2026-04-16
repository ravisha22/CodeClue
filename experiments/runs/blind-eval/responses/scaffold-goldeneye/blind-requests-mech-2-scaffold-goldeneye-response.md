# Scaffold (Goldeneye): blind-requests-mech-2
Date: 2026-04-16

## Relevant symbols traced
- `Response` owns streaming/content APIs like `iter_content`, `iter_lines`, `content`, `text`, `close`, and `raise_for_status`. [Response (src/requests/models.py:642-1041); iter_content (src/requests/models.py:801-857); iter_lines (src/requests/models.py:859-890); content (src/requests/models.py:893-909); text (src/requests/models.py:912-947)]
- Unicode decoding support is separated into `stream_decode_response_unicode()` and `get_unicode_from_response()`. [stream_decode_response_unicode (src/requests/utils.py:551-565); get_unicode_from_response (src/requests/utils.py:578-614)]
- Transport responses become `Response` objects in `build_response()`. [build_response (src/requests/adapters.py:337-372)]

## Answer
Requests handles streaming and decoding edge cases on `Response` objects in a few layers:

1. **Streaming is centralized in `iter_content()`.** That method is the core response-stream iterator, and the clue explicitly says it can raise `StreamConsumedError`, `TypeError`, `ChunkedEncodingError`, and `ContentDecodingError`, while also using `ConnectionError`-family exceptions. [iter_content (src/requests/models.py:801-857); StreamConsumedError (src/requests/exceptions.py:128-129); ChunkedEncodingError (src/requests/exceptions.py:120-121); ContentDecodingError (src/requests/exceptions.py:124-125); ConnectionError (src/requests/exceptions.py:60-61)]
2. **Other response readers build on that same streaming path.** `__iter__` delegates to `iter_content`, `iter_lines` accumulates over `iter_content`, and the `content` property also calls `iter_content`, so the same edge-case handling flows through the common byte-stream path. [__iter__ (src/requests/models.py:752-754); iter_lines (src/requests/models.py:859-890); content (src/requests/models.py:893-909)]
3. **Unicode decoding is treated as a separate step.** `stream_decode_response_unicode()` “stream decodes an iterator,” and `get_unicode_from_response()` gets an encoding from headers before returning unicode. The `text` property is explicitly described as response content “in unicode.” [stream_decode_response_unicode (src/requests/utils.py:551-565); get_unicode_from_response (src/requests/utils.py:578-614); text (src/requests/models.py:912-947)]
4. **The transport layer normalizes into a `Response` first.** `build_response()` constructs the `Response` object from the lower-level transport response and uses a `CaseInsensitiveDict` for headers, which is the foundation that later streaming/decoding logic reads from. [build_response (src/requests/adapters.py:337-372); CaseInsensitiveDict (src/requests/structures.py:13-80)]
5. **On auth-retry edge cases, Requests consumes and closes the original response before resending.** In `handle_401()`, once a digest challenge is recognized, it forces `r.content`, calls `r.close()`, copies the request, carries cookies forward, and resends on the connection; that is explicit resource-handling for a retry path. [handle_401 (src/requests/auth.py:241-283)]
6. **Exceptions keep request/response context attached.** `RequestException.__init__` stores `response` and, when available, derives `request` from it, which preserves context for streaming/decoding failures. [RequestException.__init__ (src/requests/exceptions.py:13-25)]

## Gaps / uncertainty
The clue proves that streaming and decoding errors are surfaced and that unicode decoding uses header-derived encoding, but it does not expose the full fallback logic inside those decoding helpers. The GAPS section explicitly marks this answer as mechanistic and partial. [get_unicode_from_response (src/requests/utils.py:578-614); stream_decode_response_unicode (src/requests/utils.py:551-565); GAPS]
