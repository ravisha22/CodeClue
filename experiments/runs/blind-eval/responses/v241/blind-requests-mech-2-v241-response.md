# v2.4.1 Response: blind-requests-mech-2
Date: 2026-04-16

## Response streaming errors are surfaced at iteration/materialization boundaries, and some auth retries explicitly consume and close the original response

The core streaming API is `iter_content`. Its FOCUS entry says it “Iterates over the response data,” calls `generate`, is `called_by: __iter__, content, iter_lines, Response`, and raises `StreamConsumedError`, `TypeError`, `ChunkedEncodingError`, and `ContentDecodingError` while also using `ConnectionError` (`iter_content`, `src/requests/models.py:801-857`). That is the strongest direct evidence for how Requests exposes streaming/decoding edge cases:

- **already-consumed stream** → `StreamConsumedError` (`StreamConsumedError`, `src/requests/exceptions.py:128-129`; `iter_content`, `src/requests/models.py:801-857`);
- **malformed chunked transfer** → `ChunkedEncodingError` (`ChunkedEncodingError` in INDEX; `iter_content`, `src/requests/models.py:801-857`);
- **decode failure** → `ContentDecodingError` (`ContentDecodingError`, `src/requests/exceptions.py:124-125`; `iter_content`, `src/requests/models.py:801-857`);
- **other streaming/network problems** can surface as `ConnectionError`, because `iter_content` explicitly uses that exception family (`iter_content`, `src/requests/models.py:801-857`).

Materialization helpers build on top of that same mechanism. `__iter__` delegates directly to `iter_content` (`__iter__`, `src/requests/models.py:752-754`), `iter_lines` accumulates over `self.iter_content(...)` (`iter_lines`, `src/requests/models.py:859-890`), and `content` calls `iter_content` and can raise `RuntimeError` (`content`, `src/requests/models.py:893-909`). So the same low-level streaming faults propagate whether the caller iterates bytes, iterates lines, or forces the whole body into memory (`__iter__`, `iter_lines`, `content`, and `iter_content` FOCUS entries).

Unicode and JSON decoding are surfaced separately. `text` is the unicode view of the body (`text`, `src/requests/models.py:912-947`), `stream_decode_response_unicode` “stream decodes an iterator” and accumulates over it (`stream_decode_response_unicode`, `src/requests/utils.py:551-565`), `get_unicode_from_response` gets a unicode string using header-derived encoding (`get_unicode_from_response`, `src/requests/utils.py:578-614`), and `json` raises `RequestsJSONDecodeError` if JSON decoding fails (`json`, `src/requests/models.py:949-982`).

One concrete retry edge case is shown in `HTTPDigestAuth.handle_401`. When a digest-auth retry is needed, it:

- rewinds the request body if a remembered position exists;
- forces `r.content` to be read;
- calls `r.close()` to release the original connection;
- copies the request, prepares cookies, adds a new `Authorization` header, and resends through `r.connection.send(...)`

(source snippet `handle_401`, `src/requests/auth.py L241-283`). That snippet shows Requests sometimes **intentionally consumes and closes** the original response body before a retry so the underlying connection can be reused (`handle_401`, `src/requests/auth.py L241-283`).

Adapter-side response construction is separate from those streaming behaviors. `build_response` constructs a `Response` object from a urllib3 response and normalizes `req.url` if it is bytes (`build_response`, `src/requests/adapters.py:337-372`). The prompt also includes a test snippet that monkey-patches `adapter.build_response` to inject `content-encoding: gzip`, which is evidence that compressed-response handling is exercised through the normal response-building path (test snippet `build_response`, `tests/test_requests.py L2081-2088`).

**What Cannot Be Determined**

- The prompt does not include the body of `generate`, so the exact point where urllib3 exceptions are caught and translated into `ChunkedEncodingError`, `ContentDecodingError`, or `ConnectionError` cannot be traced.
- The precise conditions under which `content` raises `RuntimeError` are not shown; only the possibility is listed (`content`, `src/requests/models.py:893-909`).
- The concrete decoding algorithm for `text` is not expanded here beyond the existence of `get_unicode_from_response` and `stream_decode_response_unicode`.
