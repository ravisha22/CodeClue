# Cross-Model (Haiku): blind-requests-mech-2
Date: 2026-04-16

## Answer

Requests handles streaming and decoding edge cases on Response objects through integrated content iteration, error handling, and optional decoding:

### Content Streaming: `iter_content()`

Response objects support streaming via `iter_content()` [Lines 152-158 (clue file): "iter_content (src/requests/models.py:801-857)" "Iterates over the response data" "calls: generate" "raises: StreamConsumedError, TypeError, ChunkedEncodingError, ContentDecodingError" "uses: StreamConsumedError (exceptions), ChunkedEncodingError (exceptions), ContentDecodingError (exceptions), ConnectionError (exceptions)"].

This method allows iterating over response content in chunks, which is essential for streaming large responses.

### Content Access & Caching: `content` property

The `content` property [Lines 195-198 (clue file): "content (src/requests/models.py:893-909)" "Content of the response, in bytes" "calls: iter_content" "raises: RuntimeError"] accesses the full response body by consuming all chunks via `iter_content()`. It detects if content was already consumed and raises RuntimeError.

### Edge Cases: Stream Already Consumed

If content is accessed multiple times, Requests raises StreamConsumedError [Line 227-230 (clue file): "StreamConsumedError (src/requests/exceptions.py:128-129)" "The content for this response was already consumed" "extends: RequestException, TypeError"]. The test snippet shows patching [Lines 362-370 (source file)] where `build_response` can be mocked to inject response headers, including "content-encoding": "gzip".

### Decoding with `text` property

Response provides unicode text decoding [Lines 272-273 (clue file): "text (src/requests/models.py:912-947)" "Content of the response, in unicode"]. This delegates to helper functions for encoding detection:
- `get_unicode_from_response()` [Lines 281-284 (clue file)] calls `get_encoding_from_headers()` to detect the correct encoding
- `stream_decode_response_unicode()` [Lines 290-293 (clue file): "Stream decodes an iterator" "behavior: ACCUMULATE(iterator loop -> result)"] handles streaming decoding on-the-fly

### Error Handling During Streaming

Three main exceptions can occur during streaming/decoding:
1. **ChunkedEncodingError** [Lines 137-140 (clue file): "Failed to decode response content" "extends: RequestException, BaseHTTPError"] - when chunked transfer encoding is malformed
2. **ContentDecodingError** [Lines 137-140 (clue file): similar exception type] - when content compression/encoding cannot be decoded
3. **StreamConsumedError** - when trying to read already-consumed content

### Iterator Interface

The Response supports the iterator protocol via `__iter__()` [Lines 190-193 (clue file): "Allows you to use a response as an iterator" "behavior: DELEGATE(iter_content -> result)" "calls: iter_content"], which internally delegates to `iter_content()`.

### Adapter-Level Response Building

The adapter's `build_response()` function [Lines 120-126 (clue file): "Builds a :class:`Response <requests.Response>` object from a urllib3" "sig: build_response(req, resp)" "uses: Response (models), CaseInsensitiveDict (structures)"] constructs Response objects from urllib3 responses, handling URL encoding edge cases [Line 123-124 (clue file): "behavior: BRANCH(isinstance(req.url, bytes) -> req.url.decode('utf-8'), else -> req.url)"].

The architecture ensures that edge cases like pre-consumed content, encoding detection failures, and chunked/compressed transfer are caught and reported with specific exception types, preventing silent data corruption.
