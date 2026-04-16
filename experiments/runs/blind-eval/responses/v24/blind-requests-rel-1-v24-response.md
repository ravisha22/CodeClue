# v2.4 Response: blind-requests-rel-1
Date: 2026-04-16

## Question
What is the relationship between `Request`, `PreparedRequest`, `Session`, and `Response` in Requests' send pipeline?

## Answer

The four core types form a linear pipeline: **`Request` → `PreparedRequest` → (via `Session`) → `Response`**. Each type plays a distinct role in the lifecycle of an HTTP request.

### 1. `Request` — The User-Facing Input

`Request` (class, `src/requests/models.py:232-312`) is described as "A user-created :class:`Request <Request>` object." It extends `RequestHooksMixin` (`src/requests/models.py:208-229`) and is the initial, user-specified representation of an HTTP request. It holds raw, unprocessed parameters.

- It calls `PreparedRequest` and `register_hook` (`Request`, `src/requests/models.py:232-312`), indicating that a `Request` can produce a `PreparedRequest`.
- `Session.request()` creates a `Request` object — it "Constructs a :class:`Request <Request>`, prepares it and sends it" and `uses: Request (models)` (`request`, `src/requests/sessions.py:502-593`).

### 2. `PreparedRequest` — The Normalized, Wire-Ready Form

`PreparedRequest` (class, `src/requests/models.py:315-639`) is "The fully mutable :class:`PreparedRequest <PreparedRequest>` object." It extends `RequestEncodingMixin` and `RequestHooksMixin`.

- It is produced from a `Request` by `Session.prepare_request()`, which "Constructs a :class:`PreparedRequest <PreparedRequest>`" (`prepare_request`, `src/requests/sessions.py:459-500`). This method merges session-level settings (headers, params, auth, cookies, hooks) into the request via `merge_setting` and `merge_hooks`, then calls `p.prepare(...)` with all merged values (`prepare_request`, `src/requests/sessions.py:459-500`).
- `PreparedRequest` calls its own preparation methods: `prepare_auth`, `prepare_body`, `prepare_content_length`, `prepare_cookies`, `prepare_headers`, `prepare_hooks` (`PreparedRequest`, `src/requests/models.py:315-639`).
- It uses `HTTPBasicAuth` (auth), `CaseInsensitiveDict` (structures) for headers, and can raise `MissingSchema`, `InvalidURL`, `UnicodeError`, `NotImplementedError` (`PreparedRequest`, `src/requests/models.py:315-639`).
- `called_by: copy, Request` — confirming it is instantiated by `Request` and can also be copied during redirect handling.

### 3. `Session` — The Orchestrator

`Session` (class, `src/requests/sessions.py:356-818`) is "A Requests session." It extends `SessionRedirectMixin` (`src/requests/sessions.py:107-353`).

The `Session` orchestrates the entire pipeline:

1. **`Session.request()`** (`src/requests/sessions.py:502-593`) — Creates a `Request` object, then calls `prepare_request` to convert it to a `PreparedRequest`, then calls `merge_environment_settings` to gather environment-derived settings, and finally calls `send()`.
2. **`Session.prepare_request()`** (`src/requests/sessions.py:459-500`) — Converts `Request` → `PreparedRequest` with merged session settings. `uses: PreparedRequest (models), RequestsCookieJar (cookies)`.
3. **`Session.send(request)`** (`src/requests/sessions.py:675-750`) — "Send a given PreparedRequest." It locates the appropriate transport adapter via `get_adapter()` (`src/requests/sessions.py:783`) and delegates to it. Its behavior is `BRANCH(allow_redirects -> self.resolve_redirect..., else -> [])`, meaning it optionally handles redirects.
4. **`resolve_redirects()`** (`src/requests/sessions.py:160-280`) — Loops through redirect responses using `behavior: ACCUMULATE(req.copy loop -> hist, raises TooManyRedirects)`. It calls `close`, `send`, `get_redirect_target`, `rebuild_auth`, `rebuild_method`, `rebuild_proxies` on each iteration.

The `Session` also manages adapter registration via `mount()` (`src/requests/sessions.py:801`) and cleanup via `close()` (`src/requests/sessions.py:796`).

A `session()` factory function (`src/requests/sessions.py:821-833`) with `behavior: DELEGATE(Session -> result)` returns a `Session` for context-management use.

### 4. `Response` — The Output

`Response` (class, `src/requests/models.py:642-1041`) is "The :class:`Response <Response>` object, which contains a [server's response]."

- It is **constructed by the adapter layer**: `build_response(req, resp)` (`src/requests/adapters.py:337-372`) "Builds a :class:`Response <requests.Response>` object from a urllib3" response. It `uses: Response (models), CaseInsensitiveDict (structures)`.
- `Response` provides data access methods: `iter_content` for streaming (`iter_content`, `src/requests/models.py:801`), `json` for JSON decoding (`json`, `src/requests/models.py:949-982`), and `raise_for_status` (`raise_for_status`, `src/requests/models.py:1001`).
- It calls `close` (`close`, `src/requests/models.py:1030`) to release the connection back to the pool.
- It can raise `StreamConsumedError`, `HTTPError`, `TypeError`, `RuntimeError` and uses exception types `ChunkedEncodingError`, `ContentDecodingError`, `ConnectionError`, `RequestsSSLError` (`Response`, `src/requests/models.py:642-1041`).

### Pipeline Flow Summary

```
User code
  → api.request() / Session.request()
    → creates Request (models.py:232)
    → Session.prepare_request()
      → creates PreparedRequest (models.py:315) with merged settings
    → Session.merge_environment_settings()
    → Session.send(PreparedRequest)
      → Session.get_adapter(url) → selects HTTPAdapter
        → HTTPAdapter.build_response() → creates Response (models.py:642)
      → Session.resolve_redirects() (if allow_redirects)
        → loops: copies PreparedRequest, re-sends, accumulates history
  → returns Response
```

### Relationship Directionality

- `Request` **creates** `PreparedRequest` (`Request` calls `PreparedRequest`, `src/requests/models.py:232-312`).
- `Session` **consumes** `Request` and **produces** `PreparedRequest` via `prepare_request` (`prepare_request`, `src/requests/sessions.py:459-500`).
- `Session.send()` **consumes** `PreparedRequest` and **produces** `Response` (indirectly via the adapter's `build_response`).
- `Response` is the **terminal output** of the pipeline, returned to the caller.

### What Cannot Be Determined

- The exact implementation of how `Session.send()` invokes the adapter's `send` method is not fully detailed in the FOCUS section (the adapter's `send` symbol is listed in the INDEX for `adapters.py` but `HTTPAdapter` is noted as uncovered in the GAPS).
- The detailed behavior of `stream_decode_response_unicode` and `get_unicode_from_response` and how they interact with `Response` are listed in GAPS as uncovered (`stream_decode_response_unicode`, `ChunkedEncodingError`, `ConnectionError`).
- The internal details of how `Request.__init__` populates its fields before conversion to `PreparedRequest` are not expanded in the FOCUS section.
