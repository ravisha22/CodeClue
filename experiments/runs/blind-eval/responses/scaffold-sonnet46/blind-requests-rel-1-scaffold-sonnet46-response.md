# Scaffold (Sonnet 4.6): blind-requests-rel-1
Date: 2026-04-16

## Question

What is the relationship between `Request`, `PreparedRequest`, `Session`, and `Response` in Requests' send pipeline?

## Answer

### Overview

The four classes form a linear pipeline: **Request → PreparedRequest → (Session orchestrates send) → Response**. A user-facing `Request` is transformed into a fully-prepared `PreparedRequest`, which `Session.send()` dispatches through an adapter, producing a `Response`. The `Session` is the orchestrator that owns and drives every stage of this pipeline.

---

### 1. Entry Point: The Public API

The top-level convenience functions (`get`, `post`, `delete`, etc.) all delegate to `request()` in `src/requests/api.py` (lines 14–59). Its signature is `request(method, url)` and it is `called_by: delete, get, head, options, patch, post, put` (INDEX: `src/requests/api.py`). This function creates a `Session` (via the `session()` factory) and delegates to `Session.request()`.

The `session()` factory function (`src/requests/sessions.py:821–833`) has behavior `DELEGATE(Session -> result)` and `calls: Session`, confirming it simply instantiates and returns a `Session`.

### 2. `Request` — The User-Facing Object

`Request` (`src/requests/models.py:232–312`) is described as *"A user-created Request object."* It extends `RequestHooksMixin` and its `calls` list shows it invokes `PreparedRequest` and `register_hook`. This means `Request` is a **simple data-holder** that the user (or `Session.request()`) populates with method, URL, headers, data, etc. Its primary structural role is to be **consumed** downstream — it carries user intent but is not sent directly.

### 3. `Request` → `PreparedRequest` Transformation

`Session.request()` (`src/requests/sessions.py:502–593`) is described as *"Constructs a Request, prepares it and sends it."* Its `calls` field shows the sequence: `merge_environment_settings, prepare_request, send`. Its `uses` field confirms `Request (models)` — it instantiates a `Request` from the caller's parameters.

`Session.prepare_request()` (`src/requests/sessions.py:459–500`) is described as *"Constructs a PreparedRequest for…"* and `uses: PreparedRequest (models), RequestsCookieJar (cookies)`. It `calls: merge_hooks, merge_setting`, meaning it merges session-level defaults (cookies, headers, auth) with per-request settings and produces a `PreparedRequest`.

`PreparedRequest` (`src/requests/models.py:315–639`) is described as *"The fully mutable PreparedRequest object."* It extends both `RequestEncodingMixin` and `RequestHooksMixin`, giving it encoding utilities and hook registration that the simpler `Request` lacks. Its `calls` list — `prepare_auth, prepare_body, prepare_content_length, prepare_cookies, prepare_headers, prepare_hooks, _get_idna_encoded_host, copy` — reveals a suite of `prepare_*` methods that normalize and finalize every aspect of the request (encoding the host via IDNA, setting content-length, attaching auth via `HTTPBasicAuth` from its `uses` field, etc.). The `Request` object's `calls: PreparedRequest` confirms that `Request` itself can produce a `PreparedRequest`, but in the session pipeline it is `prepare_request()` that performs this transformation with merged session state.

**Key structural distinction:** `Request` extends only `RequestHooksMixin`; `PreparedRequest` extends both `RequestEncodingMixin` and `RequestHooksMixin`. This two-phase design separates user-facing simplicity (Request) from wire-ready completeness (PreparedRequest).

### 4. `Session.send()` — Dispatching the `PreparedRequest`

`Session.send()` (`src/requests/sessions.py:675–750`) is described as *"Send a given PreparedRequest."* Its signature `send(request)` accepts a `PreparedRequest`. It `calls: get, get_adapter, resolve_redirects` and `raises: ValueError`. The `get_adapter` call selects the appropriate transport adapter (looked up by URL scheme), and the adapter's `send()` method performs the actual network I/O.

`Session` (`src/requests/sessions.py:356–818`) extends `SessionRedirectMixin` and its `uses` field lists all four key types: `PreparedRequest (models), Request (models), RequestsCookieJar (cookies), InvalidSchema (exceptions)`. This confirms `Session` is the **central hub** that touches every pipeline stage.

### 5. Adapter Layer → `Response` Construction

`HTTPAdapter.send()` (from INDEX: `src/requests/adapters.py`, which lists `send` and `BaseAdapter`) performs the network call via urllib3. After receiving a urllib3 response, `build_response()` (`src/requests/adapters.py:337–372`) constructs the `Response`. Its description is *"Builds a Response object from a urllib3…"*, its signature is `build_response(req, resp)`, and its `uses: Response (models), CaseInsensitiveDict (structures)`. The behavior annotation `BRANCH(isinstance(req.url, bytes) -> req.url.decode('utf-8'), else -> req.url)` shows it normalizes the URL on the PreparedRequest before attaching it to the Response.

### 6. `Response` — The Result Object

`Response` (`src/requests/models.py:642–1041`) is described as *"The Response object, which contains a…"* It does **not** extend any of the request mixins — it is a standalone class. It `calls: close, generate, iter_content, raise_for_status` and can raise `StreamConsumedError, HTTPError, TypeError, RuntimeError`. Its `uses` field references several exception types (`ChunkedEncodingError, ContentDecodingError, ConnectionError, RequestsSSLError`), indicating it handles various failure modes during response body consumption (streaming, decoding).

The `Response` is the **terminal product** of the pipeline — it flows back through `Session.send()` to the caller.

### 7. Redirect Handling — The Pipeline Recurses

`resolve_redirects()` (`src/requests/sessions.py:160–280`) is described as *"Receives a Response"* and has behavior `ACCUMULATE(req.copy loop -> hist, raises TooManyRedirects)`. It `calls: close, send, get_redirect_target, rebuild_auth, rebuild_method, rebuild_proxies` and is `called_by: send, Session`. This reveals that on redirects, the pipeline **recurses**: `send()` calls `resolve_redirects()`, which calls `send()` again with a copied `PreparedRequest` (`req.copy`). The `PreparedRequest.copy()` method (in its `calls` list) enables this re-entrant loop. Each iteration may rebuild auth and proxies, and the loop accumulates a redirect history, guarding against infinite loops via `TooManyRedirects`.

### 8. Full Pipeline Summary

```
User code
  │
  ▼
api.request()                    [src/requests/api.py:14-59]
  │ creates Session via session() [src/requests/sessions.py:821-833]
  ▼
Session.request()                [src/requests/sessions.py:502-593]
  │ constructs Request            [src/requests/models.py:232-312]
  │ calls prepare_request()       [src/requests/sessions.py:459-500]
  │   └─► merges session defaults, produces PreparedRequest
  │                                [src/requests/models.py:315-639]
  │       └─► prepare_headers, prepare_body, prepare_auth,
  │           prepare_cookies, prepare_content_length, prepare_hooks
  ▼
Session.send(PreparedRequest)    [src/requests/sessions.py:675-750]
  │ calls get_adapter() to select HTTPAdapter
  │ adapter.send() performs I/O   [src/requests/adapters.py]
  │ adapter.build_response()      [src/requests/adapters.py:337-372]
  │   └─► constructs Response     [src/requests/models.py:642-1041]
  │
  ├── if redirects ──► resolve_redirects()
  │                     [src/requests/sessions.py:160-280]
  │                     copies PreparedRequest, calls send() again
  │                     accumulates history, guards TooManyRedirects
  ▼
Response returned to caller
```

### 9. Class Hierarchy Summary

| Class | Extends | Role |
|---|---|---|
| `Request` | `RequestHooksMixin` | User-facing data container |
| `PreparedRequest` | `RequestEncodingMixin`, `RequestHooksMixin` | Wire-ready, fully normalized request |
| `Session` | `SessionRedirectMixin` | Pipeline orchestrator; merges defaults, dispatches, handles redirects |
| `Response` | *(none from request hierarchy)* | Terminal result; wraps urllib3 response with consumption/error APIs |

### 10. Gaps and Limitations

Per the GAPS section, coverage is 80 symbols at L3 with 27 behavior annotations. The gap type is `RELATIONAL (answerable from L2-L3 structure)`, meaning the structural relationships above are well-supported. Uncovered symbols (`get_unicode_from_response`, `stream_decode_response_unicode`, `ChunkedEncodingError`, `ConnectionError`) are peripheral to the core send pipeline — they relate to response body decoding and error types that `Response` references in its `uses` field but whose internal implementations are not detailed in the clue file. The exact mechanism by which `api.request()` invokes `Session.request()` (the bridging code inside `api.py`) is implied by the calling relationships but not explicitly annotated with a behavior entry.
