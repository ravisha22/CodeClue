# Cross-Model (Sonnet 4.6): blind-requests-mech-2
Date: 2026-04-16

## Question
How does Requests handle streaming and decoding edge cases on `Response` objects?

## Answer

Streaming and decoding on `Response` (src/requests/models.py:642-1041) is layered across several methods and exception types, with distinct handling for chunked encoding errors, content decoding failures, stream-consumed re-read attempts, and unicode decoding.

---

### 1. Core streaming entry point — `iter_content`

> `iter_content (src/requests/models.py:801-857)` — "Iterates over the response data." `sig: iter_content(chunk_size, decode_unicode)`. Calls `generate`. Called by `__iter__, content, iter_lines, Response`. Raises `StreamConsumedError, TypeError, ChunkedEncodingError, ContentDecodingError`. Uses `StreamConsumedError (exceptions), ChunkedEncodingError (exceptions), ContentDecodingError (exceptions), ConnectionError (exceptions)` [FOCUS, iter_content models.py:801].

`iter_content` is the foundational iterator. All higher-level access methods delegate to it:
- `content` (bytes access) calls `iter_content` [FOCUS, content models.py:893].
- `__iter__` (response-as-iterator) delegates to `iter_content` [FOCUS, __iter__ models.py:752]: `DELEGATE(iter_content -> result)`.
- `iter_lines` accumulates `iter_content` chunks [FOCUS, iter_lines models.py:859].

The internal `generate (src/requests/models.py:818)` [SYM] is the raw urllib3-level generator that `iter_content` calls to pull bytes from the network.

---

### 2. Error types raised during streaming

#### StreamConsumedError — re-reading a consumed stream
> `StreamConsumedError (src/requests/exceptions.py:128-129)` — "The content for this response was already consumed." Extends `RequestException, TypeError` [FOCUS, StreamConsumedError exceptions.py:128].

`iter_content` raises this when the stream has already been fully consumed and the caller tries to iterate again. It also extends `TypeError`, which means it is caught by a `TypeError` handler as well.

#### ChunkedEncodingError — broken chunked transfer
The `Response` uses `ChunkedEncodingError (exceptions)` as a dependency [FOCUS, Response models.py:642: `uses: ChunkedEncodingError (exceptions)`]. `iter_content` lists it as a possible raise [FOCUS, iter_content]. This error is raised when the underlying urllib3 chunked-transfer stream delivers malformed data.

#### ContentDecodingError — failed content-encoding decompression
> `ContentDecodingError (src/requests/exceptions.py:124-125)` — "Failed to decode response content." Extends `RequestException, BaseHTTPError` [FOCUS, ContentDecodingError exceptions.py:124].

`Response` lists it as a dependency [FOCUS, Response models.py:642: `uses: ContentDecodingError (exceptions)`] and `iter_content` can raise it when decompressing a compressed body (e.g. gzip) fails [FOCUS, iter_content].

#### ConnectionError during streaming
`Response` also uses `ConnectionError (exceptions)` [FOCUS, Response models.py:642]. `iter_content` lists `ConnectionError (exceptions)` among its uses, covering the case where the network connection drops mid-stream.

#### RuntimeError — re-consuming `.content`
> `content (src/requests/models.py:893-909)` — Calls `iter_content`. Raises `RuntimeError` [FOCUS, content models.py:893].

The `content` property raises `RuntimeError` when the response was streamed and the content has already been consumed, preventing double-reading without the explicit streaming flag.

---

### 3. Line-oriented streaming — `iter_lines`

> `iter_lines (src/requests/models.py:859-890)` — "Iterates over the response data, one line at a time." `sig: iter_lines(chunk_size, decode_unicode, delimiter)`. `ACCUMULATE(self.iter_content(chu... -> chunk)`. Calls `iter_content` [FOCUS, iter_lines models.py:859].

`iter_lines` buffers chunks from `iter_content` and splits on newlines (or a custom `delimiter`). It inherits all the same exception surface from `iter_content`.

---

### 4. Text decoding — `text`

> `text (src/requests/models.py:912-947)` — "Content of the response, in unicode." [FOCUS, text models.py:912].

This property reads the bytes from `content` and decodes them. The utility `get_unicode_from_response (src/requests/utils.py:578-614)` — "Returns the requested content back in unicode", calls `get_encoding_from_headers` [FOCUS, get_unicode_from_response utils.py:578]. `get_encoding_from_headers (src/requests/utils.py:526)` [SYM] reads the `Content-Type` header to determine encoding.

---

### 5. JSON decoding — `json`

> `json (src/requests/models.py:949-982)` — "Decodes the JSON response body (if any) as a Python object." Raises `RequestsJSONDecodeError`. Uses `RequestsJSONDecodeError (exceptions)` [FOCUS, json models.py:949].

JSON decoding raises its own exception class (`RequestsJSONDecodeError`) rather than the generic `ContentDecodingError`, so callers can distinguish JSON parse failures from transport-level decompression failures.

---

### 6. Connection release — `close`

> `close (src/requests/models.py:1030)` — "Releases the connection back to the pool." [SYM, close models.py:1030].

`Response` calls `close` internally [FOCUS, Response models.py:642: `calls: close, generate, iter_content, raise_for_status`]. This is the point at which the urllib3 connection is returned to the pool after streaming is complete.

---

### 7. Response construction and the gzip edge case

> `build_response (src/requests/adapters.py:337-372)` — "Builds a `Response <requests.Response>` object from a urllib3 [response]." `BRANCH(isinstance(req.url, bytes) -> req.url.decode('utf-8'), else -> req.url)`. Uses `Response (models), CaseInsensitiveDict (structures)` [FOCUS, build_response adapters.py:337].

The source snippet in the drill-down (tests/test_requests.py:2081-2088) illustrates a concrete decoding edge case: the test patches `build_response` to inject a `content-encoding: gzip` header on the raw response, which then exercises the decompression path in `iter_content`.

---

### 8. Re-authentication consuming the stream

The drill-down source snippet for `handle_401 (src/requests/auth.py:241-283)` shows an important streaming interaction:

```python
r.content    # fully consumes and closes the original response body
r.close()
prep = r.request.copy()
...
_r = r.connection.send(prep, **kwargs)
```

When a 401 is received and Digest authentication is required, `handle_401` explicitly calls `r.content` (consuming the response stream entirely) and `r.close()` before resending. This is necessary to release the connection before the retry [source snippet, handle_401 auth.py:241-283].

---

### Summary of streaming/decoding edge cases

| Edge case | Mechanism | Exception raised |
|---|---|---|
| Stream already consumed | `iter_content` guards re-iteration | `StreamConsumedError` |
| Chunked transfer corruption | `iter_content` → urllib3 | `ChunkedEncodingError` |
| Compression decompression failure | `iter_content` decode path | `ContentDecodingError` |
| Connection drop mid-stream | `iter_content` / `generate` | `ConnectionError` |
| Re-reading `.content` after streaming | `content` property guard | `RuntimeError` |
| JSON parse failure | `json` property | `RequestsJSONDecodeError` |
| SSL error during response reading | `Response` uses | `RequestsSSLError` |
| URL bytes vs str at build time | `build_response` BRANCH | (url decoded, no exception) |
