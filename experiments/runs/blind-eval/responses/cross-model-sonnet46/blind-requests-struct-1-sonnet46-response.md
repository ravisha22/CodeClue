# Cross-Model (Sonnet 4.6): blind-requests-struct-1
Date: 2026-04-16

## Question
Which public modules in Requests own the top-level request API, session orchestration, and the request/response model types?

## Answer

Three modules divide this responsibility cleanly.

---

### 1. Top-level Request API — `src/requests/api.py`

The INDEX lists `api.py` (157L) with exports `delete, get, head, options, patch` [INDEX, api.py]. The FOCUS section confirms:

> `request (src/requests/api.py:14-59)` — "Constructs and sends a `Request <Request>`." `sig: request(method, url)` — `called_by: delete, get, head, options, patch, post, put`

Every named convenience function (`get`, `post`, `put`, `patch`, `delete`, `head`, `options`) is a thin delegate that calls `request` in this module [FOCUS, request api.py:14]. This is the public surface that end-users call; it does not own session state.

---

### 2. Session Orchestration — `src/requests/sessions.py`

The INDEX lists `sessions.py` (833L) with exports `close, delete, get, get_adapter, head` [INDEX, sessions.py]. Several FOCUS entries collaborate here:

- **`Session (src/requests/sessions.py:356-818)`** — "A Requests session." Extends `SessionRedirectMixin`. Calls `close, get, get_adapter, merge_environment_settings, mount, prepare_request, request, send`. Uses `PreparedRequest (models)`, `RequestsCookieJar (cookies)`, `Request (models)` [FOCUS, Session sessions.py:356].
- **`request (src/requests/sessions.py:502-593)`** — "Constructs a `Request <Request>`, prepares it and sends it." `sig: request(method, url, params, data, headers...)`. Calls `merge_environment_settings, prepare_request, send`. Uses `Request (models)` [FOCUS, request sessions.py:502].
- **`prepare_request (src/requests/sessions.py:459-500)`** — "Constructs a `PreparedRequest <PreparedRequest>`." Calls `merge_hooks, merge_setting`. Uses `PreparedRequest (models), RequestsCookieJar (cookies)` [FOCUS, prepare_request sessions.py:459].
- **`send (src/requests/sessions.py:675-750)`** — "Send a given PreparedRequest." `BRANCH(allow_redirects -> self.resolve_redirects..., else -> [])`. Calls `get, get_adapter, resolve_redirects` [FOCUS, send sessions.py:675].
- **`session (src/requests/sessions.py:821-833)`** — Returns a `Session` for context-management. `DELEGATE(Session -> result)` [FOCUS, session sessions.py:821].
- **`SessionRedirectMixin (src/requests/sessions.py:107-353)`** — Handles redirect logic, raises `TooManyRedirects` [FOCUS, SessionRedirectMixin sessions.py:107].

The SYM table further lists `merge_setting (sessions.py:62)`, `merge_hooks (sessions.py:92)`, `get_adapter (sessions.py:783)`, `mount (sessions.py:801)`, and `close (sessions.py:796)` as key orchestration helpers [SYM].

---

### 3. Request/Response Model Types — `src/requests/models.py`

The INDEX lists `models.py` (1041L) with exports `copy, prepare, prepare_auth, prepare_body, prepare_content_length` [INDEX, models.py]. The FOCUS section defines the three core model classes:

- **`Request (src/requests/models.py:232-312)`** — "A user-created `Request <Request>` object." Extends `RequestHooksMixin`. Calls `PreparedRequest, register_hook` [FOCUS, Request models.py:232].
- **`PreparedRequest (src/requests/models.py:315-639)`** — "The fully mutable `PreparedRequest <PreparedRequest>` object." Extends `RequestEncodingMixin, RequestHooksMixin`. Calls `prepare_auth, prepare_body, prepare_content_length, prepare_cookies, prepare_headers, prepare_hooks, _get_idna_encoded_host`. Raises `MissingSchema, InvalidURL, UnicodeError`. Uses `HTTPBasicAuth (auth), CaseInsensitiveDict (structures)` [FOCUS, PreparedRequest models.py:315].
- **`Response (src/requests/models.py:642-1041)`** — "The `Response <Response>` object." Calls `close, generate, iter_content, raise_for_status`. Raises `StreamConsumedError, HTTPError, TypeError, RuntimeError`. Uses `ChunkedEncodingError, ContentDecodingError, ConnectionError, RequestsSSLError` from exceptions [FOCUS, Response models.py:642].

Supporting types in the same module include `RequestEncodingMixin (models.py:86)` and `RequestHooksMixin (models.py:208)` [FOCUS].

---

### Summary

| Responsibility | Module |
|---|---|
| Top-level request API (`get`, `post`, etc.) | `src/requests/api.py` |
| Session orchestration, redirect handling, adapter dispatch | `src/requests/sessions.py` |
| Core model types (`Request`, `PreparedRequest`, `Response`) | `src/requests/models.py` |
