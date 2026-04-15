# v2.2 Response: blind-requests-struct-1
Date: 2026-04-15

## Question

Which public modules in Requests own the top-level request API, session orchestration, and the request/response model types?

## Answer

Based solely on the clue file, three public modules clearly own these responsibilities:

### 1. Top-Level Request API — `src/requests/api.py` (157 L)

This module contains the top-level, stateless HTTP verb functions that serve as the primary public entry points:

- **`request`** (`src/requests/api.py:14`) — "Constructs and sends a :class:`Request <Request>`." This is the central dispatcher.
- **`get`** (`src/requests/api.py:62`) — "Sends a GET request." Signature: `get(url, params)`. Behavior: `DELEGATE(request -> result)`.
- **`head`** (`src/requests/api.py:88`) — "Sends a HEAD request." Behavior: `DELEGATE(request -> result)`.
- **`options`** (`src/requests/api.py:76`) — "Sends an OPTIONS request." Behavior: `DELEGATE(request -> result)`.
- **`post`** (`src/requests/api.py:103`) — "Sends a POST request." Signature: `post(url, data, json)`. Behavior: `DELEGATE(request -> result)`.
- **`put`** (`src/requests/api.py:118`) — "Sends a PUT request." Behavior: `DELEGATE(request -> result)`.
- **`patch`** (`src/requests/api.py:133`) — "Sends a PATCH request." Behavior: `DELEGATE(request -> result)`.
- **`delete`** (`src/requests/api.py:148`) — "Sends a DELETE request." Behavior: `DELEGATE(request -> result)`.

All seven HTTP-verb convenience functions delegate to `request` (`src/requests/api.py:14`), which is confirmed by their `called_by` / `calls` annotations and their uniform `DELEGATE(request -> result)` behavior.

### 2. Session Orchestration — `src/requests/sessions.py` (833 L)

This module owns session lifecycle, request preparation, sending, and redirect handling:

- **`Session`** (class, `src/requests/sessions.py:356`) — "A Requests session." Extends `SessionRedirectMixin`. Calls: `close`, `get`, `get_adapter`, `merge_environment_settings`, `mount`, `prepare_request`, `request`, `send`. Uses: `PreparedRequest` (models), `RequestsCookieJar` (cookies), `Request` (models), `InvalidSchema` (exceptions).
- **`session`** (function, `src/requests/sessions.py:821`) — "Returns a :class:`Session` for context-management." Behavior: `DELEGATE(Session -> result)`.
- **`Session.request`** (`src/requests/sessions.py:502`) — "Constructs a :class:`Request <Request>`, prepares it and sends it." Calls `merge_environment_settings`, `prepare_request`, `send`.
- **`prepare_request`** (`src/requests/sessions.py:459`) — "Constructs a :class:`PreparedRequest <PreparedRequest>`." Calls `merge_hooks`, `merge_setting`. Uses `PreparedRequest` (models), `RequestsCookieJar` (cookies).
- **`send`** (`src/requests/sessions.py:675`) — "Send a given PreparedRequest." Calls `get`, `get_adapter`, `resolve_redirects`.
- **`SessionRedirectMixin`** (`src/requests/sessions.py:107`) — Handles redirect resolution. Calls `close`, `get`, `send`, `get_redirect_target`, `rebuild_auth`, `rebuild_method`, `rebuild_proxies`, `should_strip_auth`.
- **`resolve_redirects`** (`src/requests/sessions.py:160`) — "Receives a Response." Behavior: `ACCUMULATE(loop -> hist)`. Raises `TooManyRedirects`.
- **`merge_setting`** (`src/requests/sessions.py:62`) — "Determines appropriate setting for a given request."
- **`merge_hooks`** (`src/requests/sessions.py:92`) — "Properly merges both requests and session hooks."
- **`merge_environment_settings`** (`src/requests/sessions.py:752`) — "Check the environment and merge it with some settings."
- **`get_adapter`** (`src/requests/sessions.py:783`) — "Returns the appropriate connection adapter for the given URL."
- **`mount`** (`src/requests/sessions.py:801`) — "Registers a connection adapter to a prefix."
- **`close`** (`src/requests/sessions.py:796`) — "Closes all adapters and as such the session."

The session module also mirrors the same HTTP-verb methods (`get`, `post`, `put`, `patch`, `delete`, `head`, `options`) as instance methods on `Session`, each delegating to `Session.request` (confirmed by their `DELEGATE(request -> result)` behavior annotations at lines 595, 606, 617, 628, 641, 653, 665).

### 3. Request/Response Model Types — `src/requests/models.py` (1041 L)

This module defines the core data-model classes:

- **`Request`** (class, `src/requests/models.py:232`) — "A user-created :class:`Request <Request>` object." Extends `RequestHooksMixin`. Calls `PreparedRequest`, `register_hook`.
- **`PreparedRequest`** (class, `src/requests/models.py:315`) — "The fully mutable :class:`PreparedRequest <PreparedRequest>` object." Extends `RequestEncodingMixin`, `RequestHooksMixin`. Calls `prepare_auth`, `prepare_body`, `prepare_content_length`, `prepare_cookies`, `prepare_headers`, `prepare_hooks`, `_get_idna_encoded_host`, `copy`.
- **`Response`** (class, `src/requests/models.py:642`) — "The :class:`Response <Response>` object." Calls `close`, `generate`, `iter_content`, `raise_for_status`. Raises `StreamConsumedError`, `HTTPError`, `TypeError`, `RuntimeError`.
- **`RequestEncodingMixin`** (`src/requests/models.py:86`) — Mixin providing encoding utilities.
- **`RequestHooksMixin`** (`src/requests/models.py:208`) — Mixin providing hook registration (`register_hook` at line 209).

Supporting methods on these classes include `iter_content` (`src/requests/models.py:801`), `raise_for_status` (`src/requests/models.py:1001`), `close` (`src/requests/models.py:1030`), `prepare_content_length` (`src/requests/models.py:574`), and `_encode_params` (`src/requests/models.py:109`).

### Summary

| Responsibility | Module | Key Symbols |
|---|---|---|
| Top-level request API | `src/requests/api.py` | `request`, `get`, `post`, `put`, `patch`, `delete`, `head`, `options` |
| Session orchestration | `src/requests/sessions.py` | `Session`, `session`, `send`, `prepare_request`, `resolve_redirects`, `merge_setting`, `merge_hooks`, `get_adapter`, `mount` |
| Request/Response models | `src/requests/models.py` | `Request`, `PreparedRequest`, `Response`, `RequestEncodingMixin`, `RequestHooksMixin` |
