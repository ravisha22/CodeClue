# v2.3 Response: blind-requests-mech-2
Date: 2026-04-15

## Summary

Requests handles streaming and decoding on `Response` objects through a layered system: `iter_content` is the core streaming primitive, `generate` performs low-level chunk reading with error translation, and several properties (`content`, `text`, `json`) build on top. Edge cases include stream-already-consumed guards, chunked encoding errors, content decoding failures, and redirect-time content consumption. Source snippets reveal precise error-handling patterns.

## Detailed Analysis

### 1. `iter_content` — The Core Streaming Method

- `iter_content` (src/requests/models.py:801-857) "Iterates over the response data" with signature `iter_content(chunk_size, decode_unicode)` (FOCUS: iter_content).
- It calls `generate` internally (FOCUS: iter_content, calls field).
- It is called by `__iter__`, `content`, `iter_lines`, and `Response` (FOCUS: iter_content, called_by field), making it the single entry point for all content consumption.
- **Edge-case exceptions it raises**: `StreamConsumedError`, `TypeError`, `ChunkedEncodingError`, `ContentDecodingError` (FOCUS: iter_content, raises field).
- It uses the exception classes: `StreamConsumedError (exceptions)`, `ChunkedEncodingError (exceptions)`, `ContentDecodingError (exceptions)`, `ConnectionError (exceptions)` (FOCUS: iter_content, uses field).

### 2. `generate` — Low-Level Chunk Generator

- `generate` (src/requests/models.py:818-839) is the internal generator that actually reads from the underlying stream (FOCUS: generate).
- Behavior: `BRANCH(hasattr_stream -> result, else -> result)` (FOCUS: generate, behavior field) — it checks whether the raw response has a `stream` attribute and branches accordingly.
- **Error translation**: It raises `ChunkedEncodingError`, `ContentDecodingError`, `ConnectionError`, `RequestsSSLError` (FOCUS: generate, raises field). These are mapped from urllib3 exceptions: it uses `ChunkedEncodingError (exceptions)`, `ContentDecodingError (exceptions)`, `ConnectionError (exceptions)`, `RequestsSSLError (exceptions)` (FOCUS: generate, uses field).
- Called by `iter_content` and `Response` (FOCUS: generate, called_by field).

### 3. `StreamConsumedError` — The Once-Only Guard

- `StreamConsumedError` (src/requests/exceptions.py:128-129) "The content for this response was already consumed" and extends `RequestException, TypeError` (FOCUS: StreamConsumedError).
- This is raised by `iter_content` when a user attempts to iterate over response content that has already been consumed, enforcing a consume-once semantic on streaming responses.

### 4. Content Access Properties

- **`content`** (src/requests/models.py:893-909) "Content of the response, in bytes." It calls `iter_content` and can raise `RuntimeError` (FOCUS: content). This property eagerly consumes the entire stream into bytes.
- **`text`** (src/requests/models.py:912-947) "Content of the response, in unicode" (FOCUS: text). It builds on `content` to decode bytes into a string.
- **`json`** (src/requests/models.py:949-982) "Decodes the JSON response body (if any) as a Python object" and raises `RequestsJSONDecodeError` (FOCUS: json).
- **`__iter__`** (src/requests/models.py:752-754) "Allows you to use a response as an iterator" with behavior `DELEGATE(iter_content -> result)` (FOCUS: __iter__), delegating directly to `iter_content`.
- **`iter_lines`** (src/requests/models.py:859-890) "Iterates over the response data, one line at a time" with behavior `ACCUMULATE(loop -> chunk)` (FOCUS: iter_lines). It calls `iter_content` and splits by delimiter.

### 5. Unicode Stream Decoding

- `stream_decode_response_unicode` (src/requests/utils.py:551-565) "Stream decodes an iterator" with behavior `ACCUMULATE(loop -> result)` (FOCUS: stream_decode_response_unicode). This handles incremental Unicode decoding of streamed chunks.
- `get_unicode_from_response` (src/requests/utils.py:578-614) "Returns the requested content back in unicode" and calls `get_encoding_from_headers` (FOCUS: get_unicode_from_response).
- `get_encoding_from_headers` (src/requests/utils.py:526) "Returns encodings from given HTTP Header Dict" (SYM: get_encoding_from_headers) — used to detect the charset.

### 6. Content Decoding Errors

- `ContentDecodingError` (src/requests/exceptions.py:124-125) "Failed to decode response content" extends `RequestException, BaseHTTPError` (FOCUS: ContentDecodingError). This is raised when the response body cannot be decoded (e.g., corrupted gzip).
- `ChunkedEncodingError` (src/requests/exceptions.py) is used when chunked transfer encoding fails during streaming.

### 7. Redirect-Time Content Consumption (Source Snippet: `resolve_redirects`)

The source snippet for `resolve_redirects` (src/requests/sessions.py:160-280) reveals critical streaming edge-case handling during redirects:

- **Eager consumption before redirect**: Lines 456-458 show:
  ```python
  try:
      resp.content  # Consume socket so it can be released
  except (ChunkedEncodingError, ContentDecodingError, RuntimeError):
      resp.raw.read(decode_content=False)
  ```
  The response body is consumed via `resp.content` to free the connection. If that fails due to `ChunkedEncodingError`, `ContentDecodingError`, or `RuntimeError`, it falls back to `resp.raw.read(decode_content=False)` — reading raw bytes without decoding (source snippet: resolve_redirects, lines ~456-458).

- **Connection release**: After consuming, `resp.close()` is called (source snippet: resolve_redirects, line ~466) to release the connection back to the pool.

- **Header purging on non-permanent redirects**: For status codes other than 307/308, `Content-Length`, `Content-Type`, and `Transfer-Encoding` headers are purged and `body` is set to `None` (source snippet: resolve_redirects, lines ~494-502).

- **Body rewinding**: Lines 521-527 handle body position rewinding for file-like bodies:
  ```python
  rewindable = prepared_request._body_position is not None and (
      "Content-Length" in headers or "Transfer-Encoding" in headers
  )
  if rewindable:
      rewind_body(prepared_request)
  ```
  (source snippet: resolve_redirects, lines ~521-527).

### 8. Digest Auth and Content Consumption (Source Snippet: `handle_401`)

- `handle_401` (src/requests/auth.py:241-283) shows another streaming edge case (source snippet: handle_401):
  - Line ~409: `r.content` — consumes the response content to release the connection before retrying with digest auth.
  - Line ~410: `r.close()` — explicitly closes the response after consumption.
  - Line ~399: `r.request.body.seek(self._thread_local.pos)` — rewinds the request body for re-sending.
  - This demonstrates the pattern: consume content → close response → prepare new request.

### 9. `build_response` — Response Construction

- `build_response` (src/requests/adapters.py:337-372) "Builds a :class:`Response <requests.Response>` object from a urllib3" response (FOCUS: build_response). Its behavior `BRANCH(isinstance_bytes -> result, else -> result)` shows it handles both bytes and non-bytes raw responses differently.
- The test snippet (tests/test_requests.py:2081-2088) shows a patched `build_response` that injects `content-encoding: gzip` into raw headers, simulating a decoding edge case for testing corrupted gzip responses (source snippet: build_response in test_requests.py).

### 10. Response Lifecycle

- `Response.close` (src/requests/models.py:1030) "Releases the connection back to the pool" (SYM: close at models.py:1030).
- `raise_for_status` (src/requests/models.py:1001) "Raises :class:`HTTPError`, if one occurred" (SYM: raise_for_status).
- `is_redirect` (src/requests/models.py:772-776) and `is_permanent_redirect` (src/requests/models.py:779-784) provide redirect detection properties.
- `links` (src/requests/models.py:985-999) "Returns the parsed header links of the response, if any" (FOCUS: links).

## Uncertainty / Limits

- The exact chunk-size handling logic within `iter_content` and `generate` is not visible in the clue file — only the behavior annotations are available.
- How `decode_unicode` parameter in `iter_content` interacts with `stream_decode_response_unicode` is not explicitly linked in the clue file, only inferred from the presence of both functions.
- The clue file has only 23 of 80 L3 symbols with behavior annotations (GAPS section), so some secondary streaming behaviors may be undocumented.
- The `text` property's encoding detection logic (whether it uses `get_encoding_from_headers` or content sniffing) is not detailed in the clue file.
