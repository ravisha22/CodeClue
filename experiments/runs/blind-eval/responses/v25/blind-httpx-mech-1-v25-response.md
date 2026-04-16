# v2.5 Response: blind-httpx-mech-1
Date: 2026-04-16

## Question

What request-body encoding and redirect-following behavior does HTTPX document for normal client calls?

## Answer

### 1. Request-Body Encoding: `encode_request` Dispatch

The core encoding logic lives in `encode_request` (`httpx/_content.py:186-218`), documented as *"Handles encoding the given content, data, files, and json"* (FOCUS: `encode_request`). It dispatches to one of four specialized encoders based on which parameter the caller provides:

| Parameter | Encoder Called | Purpose |
|---|---|---|
| `content` (raw) | `encode_content` → `ByteStream` | Raw bytes or byte-iterators |
| `json` | `encode_json` | JSON serialization |
| `data` | `encode_urlencoded_data` | URL-encoded form data |
| `data` + `files` | `encode_multipart_data` | Multipart form data |

(FOCUS: `encode_request … calls ByteStream, encode_content, encode_json, encode_multipart_data, encode_urlencoded_data`)

Supporting types for multipart encoding include `DataField` and `FileField` in `_multipart.py`, and `ByteStream` and `encode_content` in `_content.py` (SYM: `DataField, FileField in _multipart.py; ByteStream, encode_content in _content.py`).

The top-level `post` function (`httpx/_api.py:282-320`) and client-level `post` methods (`httpx/_client.py:1123-1158` sync, `1838-1873` async) all delegate to `request` via `DELEGATE(request -> result)` (FOCUS: `post` entries). The `request` method in turn calls `build_request`, which invokes `encode_request` to handle body encoding.

### 2. `build_request`: Merging Client Defaults

Before encoding, `build_request` (`httpx/_client.py:340-389`) merges caller-provided values with the client's configured defaults (FOCUS: `build_request`):

- **`_merge_url`**: Combines base URL with the request path.
- **`_merge_headers`**: Merges per-request headers with client-level default headers.
- **`_merge_queryparams`**: Combines per-request query parameters with client defaults.
- **`_merge_cookies`**: Merges per-request cookies with the client's cookie jar.

(FOCUS: `build_request … calls _merge_cookies, _merge_headers, _merge_queryparams, _merge_url`)

This method is called by both `AsyncClient` and `Client` (FOCUS: `build_request … called_by AsyncClient, Client`). The resulting `Request` object (`httpx/_models.py:382-512`) encapsulates the fully-merged URL, headers, cookies (via `set_cookie_header`), and encoded body (FOCUS: `Request … calls set_cookie_header, Cookies, items, Headers`).

### 3. Redirect Following: `_send_handling_redirects`

Once a request is sent, redirect following is managed by `_send_handling_redirects`:

- **Sync version** (`httpx/_client.py:964-999`): Uses an accumulation loop — `ACCUMULATE(_send_single_request → history, raises TooManyRedirects)` (FOCUS: sync `_send_handling_redirects`).
- **Async version** (`httpx/_client.py:1679-1715`): Same pattern — `ACCUMULATE(len loop → history, raises TooManyRedirects)` (FOCUS: async `_send_handling_redirects`).

The loop repeatedly calls `_send_single_request` for each hop, building up a `history` list of intermediate responses. When the redirect chain exceeds the client's `max_redirects` limit, a `TooManyRedirects` exception is raised.

Each individual request in the chain is dispatched by `_send_single_request` (`httpx/_client.py:1001-1034` sync, `1717-1749` async), documented as *"Sends a single request, without handling any redirections."* It raises `RuntimeError` on failure (FOCUS: `_send_single_request`).

### 4. Redirect Request Building

When a redirect response is received, a new request must be constructed for the next hop. This is handled by `_build_redirect_request` (`httpx/_client.py:475-492`), which orchestrates four sub-functions (FOCUS: `_build_redirect_request … calls _redirect_headers, _redirect_method, _redirect_stream, _redirect_url; called_by AsyncClient, Client`):

#### `_redirect_url` (`httpx/_client.py:517-544`)
*"Return the URL for the redirect to follow."* Resolves the `Location` header against the current request URL. Raises `RemoteProtocolError` if the redirect URL is invalid (FOCUS: `_redirect_url … raises RemoteProtocolError`).

#### `_redirect_method` (`httpx/_client.py:494-515`)
*"When being redirected we may want to change the method of the request"* — implements the standard HTTP redirect method-change rules (e.g., POST → GET for 303, or for 301/302 in common practice) (FOCUS: `_redirect_method`).

#### `_redirect_headers` (`httpx/_client.py:546-571`)
Filters and adjusts headers for the redirect. Calls `_is_https_redirect` and `_same_origin` to determine which headers are safe to forward (FOCUS: `_redirect_headers … calls _is_https_redirect, _same_origin`).

#### `_redirect_stream` (`httpx/_client.py:573-582`)
*"Return the body that should be used for the redirect request."* Determines whether the original request body should be forwarded or dropped on redirect (FOCUS: `_redirect_stream`).

### 5. Security Checks in Redirect Handling

Two helper functions enforce security boundaries during redirects:

- **`_is_https_redirect`** (`httpx/_client.py:62-74`): *"Return True if location is a HTTPS upgrade of url"* — detects when a redirect upgrades from HTTP to HTTPS (FOCUS: `_is_https_redirect`).

- **`_same_origin`** (`httpx/_client.py:83-91`): *"Return True if the given URLs share the same origin."* — checks scheme, host, and port equality (FOCUS: `_same_origin`).

These are used by `_redirect_headers` to strip sensitive headers (e.g., `Authorization`) when redirecting across origins or downgrading from HTTPS to HTTP. This prevents credential leakage during cross-origin redirects.

### 6. End-to-End Flow Summary

A normal `client.post(url, json=data)` call traverses:

```
post()
  → request()                    # DELEGATE
    → build_request()            # merge URL/headers/cookies/params + encode_request
      → _build_request_auth()    # resolve auth
        → _send_handling_auth()  # auth flow loop
          → _send_handling_redirects()  # redirect loop
            → _send_single_request()    # single transport call
              → transport.handle_request()
            ← response
            → if redirect: _build_redirect_request()
              → _redirect_url()     # resolve Location
              → _redirect_method()  # adjust HTTP method
              → _redirect_headers() # filter headers (security checks)
              → _redirect_stream()  # forward or drop body
            → loop until done or TooManyRedirects
```

### 7. Gaps and Limitations

The clue file reports a **RELATIONAL** gap: *"coverage: 80 symbols in L3, 21 with behavior annotations"* (GAPS entry). This leaves 59 of 80 symbols (74%) without behavior-level detail. Specifically uncovered symbols include `UseClientDefault`, `has_redirect_location`, `is_client_error`, and `is_redirect` (GAPS: `uncovered: UseClientDefault, has_redirect_location, is_client_error, is_redirect`).

Key unknowns from the clue data:
- The exact dispatch logic inside `encode_request` — which parameter takes precedence when multiple are provided is not shown.
- The specific HTTP status codes that trigger `_redirect_method` to change the method (e.g., whether 307/308 preserve the method).
- How `event_hooks` integrate with the redirect loop.
- The `max_redirects` default value.
