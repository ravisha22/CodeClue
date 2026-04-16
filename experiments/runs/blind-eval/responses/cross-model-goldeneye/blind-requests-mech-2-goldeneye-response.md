# Cross-Model (Goldeneye): blind-requests-mech-2
Date: 2026-04-16

Requests handles `Response` streaming and decoding edge cases through a small set of explicit choke points:

- `iter_content(chunk_size, decode_unicode)` is the core streaming primitive. It is what `__iter__`, `content`, and `iter_lines` all build on, so streamed reads and buffered reads converge through the same path. [iter_content, src/requests/models.py:801-857; __iter__, src/requests/models.py:752-754; content, src/requests/models.py:893-909; iter_lines, src/requests/models.py:859-890]
- The clue file explicitly names the edge-case failures for that path: `iter_content` can raise `StreamConsumedError`, `TypeError`, `ChunkedEncodingError`, and `ContentDecodingError`, and it also uses `ConnectionError`. [iter_content, src/requests/models.py:801-857; StreamConsumedError, src/requests/exceptions.py:128-129; ContentDecodingError, src/requests/exceptions.py:124-125]
- On top of that, `content` returns the body “in bytes” and can raise `RuntimeError`, while `text` exposes the body “in unicode,” and `json()` decodes the body and can raise `RequestsJSONDecodeError`. [content, src/requests/models.py:893-909; text, src/requests/models.py:912-947; json, src/requests/models.py:949-982]
- Response construction also normalizes a URL edge case: `build_response(req, resp)` branches on whether `req.url` is `bytes`, decoding it as UTF-8 before building the public `Response`. [build_response, src/requests/adapters.py:337-372]
- In the digest-auth 401 retry path, Requests explicitly consumes and closes the original response before resending: `handle_401` forces `r.content`, then `r.close()`, copies the prepared request, and resends it so the connection can be reused. [handle_401, src/requests/auth.py:241-283]

So the practical behavior is: stream through `iter_content`, surface decoding/consumption failures as dedicated exceptions, and eagerly consume/close a response when a retry flow needs to reuse the connection. [iter_content, src/requests/models.py:801-857; handle_401, src/requests/auth.py:241-283]
