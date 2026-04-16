# Cross-Model (Sonnet 4.6): blind-requests-rel-1
Date: 2026-04-16

## Question
What is the relationship between `Request`, `PreparedRequest`, `Session`, and `Response` in Requests' send pipeline?

## Answer

The four types form a strict linear pipeline: **Request → PreparedRequest → (Session orchestration) → Response**. `Session` is the orchestrator that drives the transformation at each stage.

---

### Stage 1 — User input: `Request`

> `Request (src/requests/models.py:232-312)` — "A user-created `Request <Request>` object." Extends `RequestHooksMixin`. Calls `PreparedRequest, register_hook` [FOCUS, Request models.py:232].

`Request` is a plain, user-facing data holder for method, URL, headers, body, auth, hooks, etc. It does not perform I/O itself. It can call `PreparedRequest` to self-prepare, but in the normal `Session`-based flow that step is delegated.

---

### Stage 2 — Construction via top-level API or Session

**Top-level route** (stateless):
> `request (src/requests/api.py:14-59)` — "Constructs and sends a `Request <Request>`." Called by `delete, get, head, options, patch, post, put` [FOCUS, request api.py:14].

This thin function opens a `Session` internally and calls through to the session-based pipeline below.

**Session route** (stateful):
> `request (src/requests/sessions.py:502-593)` — "Constructs a `Request <Request>`, prepares it and sends it." `sig: request(method, url, params, data, headers...)`. Calls `merge_environment_settings, prepare_request, send`. Uses `Request (models)` [FOCUS, request sessions.py:502].

The session's `request` method is called by `delete, get, head, options, patch, post, put, Session` [FOCUS], confirming both the per-method shortcuts and the `Session` itself funnel through this single method.

---

### Stage 3 — Transformation: `Request` → `PreparedRequest`

> `prepare_request (src/requests/sessions.py:459-500)` — "Constructs a `PreparedRequest <PreparedRequest>` for [transmission]." `sig: prepare_request(request)`. Calls `merge_hooks, merge_setting`. Uses `PreparedRequest (models), RequestsCookieJar (cookies)` [FOCUS, prepare_request sessions.py:459].

This step merges session-level settings (auth, cookies, headers, proxies, hooks) with the per-request settings and produces the final, immutable `PreparedRequest`.

> `PreparedRequest (src/requests/models.py:315-639)` — "The fully mutable `PreparedRequest <PreparedRequest>` object." Extends `RequestEncodingMixin, RequestHooksMixin`. Calls `prepare_auth, prepare_body, prepare_content_length, prepare_cookies, prepare_headers, prepare_hooks, _get_idna_encoded_host`. Raises `MissingSchema, InvalidURL, UnicodeError`. Uses `HTTPBasicAuth (auth), CaseInsensitiveDict (structures)` [FOCUS, PreparedRequest models.py:315].

`PreparedRequest` is the wire-ready form: URL encoded, body serialised, headers and cookies set, auth attached.

---

### Stage 4 — Transmission via `Session.send`

> `send (src/requests/sessions.py:675-750)` — "Send a given PreparedRequest." `sig: send(request)`. `BRANCH(allow_redirects -> self.resolve_redirects..., else -> [])`. Calls `get, get_adapter, resolve_redirects`. Called by `request, Session, resolve_redirects, SessionRedirectMixin`. Raises `ValueError` [FOCUS, send sessions.py:675].

`Session.send` locates the correct adapter via `get_adapter (sessions.py:783)` [SYM]:
> `get_adapter (src/requests/sessions.py:783)` — "Returns the appropriate connection adapter for the given URL" [SYM].

The adapter's own `send` method (e.g. `HTTPAdapter.send`) actually performs the network call:
> `send (src/requests/adapters.py:591-697)` — "Sends PreparedRequest object." Raises `InvalidURL, ConnectionError, ProxyError, ValueError` [FOCUS, send adapters.py:591].

`BaseAdapter.send (src/requests/adapters.py:120-137)` defines the abstract contract: it receives a `PreparedRequest` and returns a `Response` [FOCUS, send adapters.py:120].

---

### Stage 5 — Result construction: `Response`

> `build_response (src/requests/adapters.py:337-372)` — "Builds a `Response <requests.Response>` object from a urllib3 [response]." `sig: build_response(req, resp)`. `BRANCH(isinstance(req.url, bytes) -> req.url.decode('utf-8'), else -> req.url)`. Called by `HTTPAdapter`. Uses `Response (models), CaseInsensitiveDict (structures)` [FOCUS, build_response adapters.py:337].

> `Response (src/requests/models.py:642-1041)` — "The `Response <Response>` object." Calls `close, generate, iter_content, raise_for_status`. Raises `StreamConsumedError, HTTPError, TypeError, RuntimeError`. Uses `ChunkedEncodingError, ContentDecodingError, ConnectionError, RequestsSSLError` [FOCUS, Response models.py:642].

`Response` is the terminal object returned to the caller. It wraps the raw urllib3 response and exposes streaming, decoding, status checking, and cookie extraction.

---

### Redirect Loop

After the initial `Response` is obtained, `Session.send` checks for redirects:
> `resolve_redirects (src/requests/sessions.py:160-280)` — "Receives a Response." `ACCUMULATE(req.copy loop -> hist, raises TooManyRedirects)`. Calls `close, send, get_redirect_target, rebuild_auth, rebuild_method, rebuild_proxies`. Called by `send, Session`. Raises `TooManyRedirects` [FOCUS, resolve_redirects sessions.py:160].

Each redirect iteration re-enters `Session.send` with a new `PreparedRequest`, building up a history of `Response` objects.

---

### Session as Orchestrator

> `Session (src/requests/sessions.py:356-818)` — "A Requests session." Extends `SessionRedirectMixin`. Calls `close, get, get_adapter, merge_environment_settings, mount, prepare_request, request, send`. Uses `InvalidSchema (exceptions), PreparedRequest (models), RequestsCookieJar (cookies), Request (models)` [FOCUS, Session sessions.py:356].

`Session` holds persistent state (cookies, auth, headers, adapters, max_redirects) across multiple request/response cycles. `merge_environment_settings (sessions.py:752)` [SYM] merges environment proxy and SSL settings into every request.

---

### Pipeline Diagram

```
User call                Request (models.py:232)
        │
        ▼
Session.request()        (sessions.py:502)
  ├─ merge_environment_settings
  ├─ prepare_request()   → PreparedRequest (models.py:315)
  │     └─ merge_hooks, merge_setting, prepare_auth/body/headers/cookies
  └─ send()              (sessions.py:675)
        ├─ get_adapter() → HTTPAdapter (adapters.py)
        │     └─ adapter.send(PreparedRequest) → urllib3
        ├─ build_response() → Response (models.py:642)
        └─ resolve_redirects() [loop if redirects]
```
