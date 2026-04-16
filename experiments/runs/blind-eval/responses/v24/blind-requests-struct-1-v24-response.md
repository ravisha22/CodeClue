# v2.4 Response: blind-requests-struct-1
Date: 2026-04-16

## Question
Which public modules in Requests own the top-level request API, session orchestration, and the request/response model types?

## Answer

Based on the clue file, three public modules own these responsibilities:

### 1. Top-Level Request API — `src/requests/api.py`

This module provides the stateless, convenience HTTP-verb functions that serve as the top-level entry points. It contains:

- `request(method, url)` — the core dispatcher that "Constructs and sends a :class:`Request <Request>`" (`request`, `src/requests/api.py:14`).
- `get(url, params)` — delegates to `request` (`get`, `src/requests/api.py:62-73`).
- `head(url)` — delegates to `request` (`head`, `src/requests/api.py:88-100`).
- `options(url)` — delegates to `request` (`options`, `src/requests/api.py:76-85`).
- `post(url, data, json)` — delegates to `request` (`post`, `src/requests/api.py:103-115`).
- `put(url, data)` — delegates to `request` (`put`, `src/requests/api.py:118-130`).
- `patch(url, data)` — delegates to `request` (`patch`, `src/requests/api.py:133-145`).
- `delete(url)` — delegates to `request` (`delete`, `src/requests/api.py:148-157`).

All seven HTTP-verb functions use `behavior: DELEGATE(request -> result)`, confirming they simply forward to the central `request()` function.

### 2. Session Orchestration — `src/requests/sessions.py`

This module owns session lifecycle and orchestration. Key symbols:

- **`Session`** (class, `src/requests/sessions.py:356-818`) — "A Requests session." It extends `SessionRedirectMixin` and orchestrates the full send pipeline by calling `prepare_request`, `merge_environment_settings`, `send`, `get_adapter`, `mount`, and `close` (`Session`, `src/requests/sessions.py:356-818`). It uses model types `PreparedRequest` (models), `Request` (models), and `RequestsCookieJar` (cookies).
- **`SessionRedirectMixin`** (`src/requests/sessions.py:107-353`) — handles redirect resolution via `resolve_redirects`, `get_redirect_target`, `rebuild_auth`, `rebuild_method`, `rebuild_proxies`, and `should_strip_auth` (`SessionRedirectMixin`, `src/requests/sessions.py:107-353`).
- **`session()`** (factory function, `src/requests/sessions.py:821-833`) — "Returns a :class:`Session` for context-management" with `behavior: DELEGATE(Session -> result)` (`session`, `src/requests/sessions.py:821-833`).
- **`Session.request()`** (`src/requests/sessions.py:502-593`) — "Constructs a :class:`Request <Request>`, prepares it and sends it." It calls `merge_environment_settings`, `prepare_request`, and `send` (`request`, `src/requests/sessions.py:502-593`).
- **`Session.send()`** (`src/requests/sessions.py:675`) — "Send a given PreparedRequest" (`send`, `src/requests/sessions.py:675`).
- **`prepare_request()`** (`src/requests/sessions.py:459-500`) — "Constructs a :class:`PreparedRequest <PreparedRequest>`" by merging session and request settings via `merge_hooks` and `merge_setting` (`prepare_request`, `src/requests/sessions.py:459-500`).
- **`merge_setting()`** (`src/requests/sessions.py:62`) and **`merge_hooks()`** (`src/requests/sessions.py:92-104`) — merge per-request and session-level configuration.
- **`merge_environment_settings()`** (`src/requests/sessions.py:752`) — merges environment variables into settings.
- **`get_adapter()`** (`src/requests/sessions.py:783`) — selects the appropriate connection adapter for a URL.
- **`mount()`** (`src/requests/sessions.py:801`) — registers a connection adapter to a URL prefix.
- **`close()`** (`src/requests/sessions.py:796`) — "Closes all adapters and as such the session."

The sessions module also mirrors the HTTP-verb convenience methods (`get`, `post`, `put`, `delete`, `head`, `options`, `patch`) on the `Session` class, each delegating to `Session.request()`.

### 3. Request/Response Model Types — `src/requests/models.py`

This 1041-line module defines the core data model classes:

- **`Request`** (class, `src/requests/models.py:232-312`) — "A user-created :class:`Request <Request>` object." Extends `RequestHooksMixin` and calls `PreparedRequest` and `register_hook` (`Request`, `src/requests/models.py:232-312`).
- **`PreparedRequest`** (class, `src/requests/models.py:315-639`) — "The fully mutable :class:`PreparedRequest <PreparedRequest>` object." Extends `RequestEncodingMixin` and `RequestHooksMixin`. Calls `prepare_auth`, `prepare_body`, `prepare_content_length`, `prepare_cookies`, `prepare_headers`, `prepare_hooks`, and `_get_idna_encoded_host` (`PreparedRequest`, `src/requests/models.py:315-639`).
- **`Response`** (class, `src/requests/models.py:642-1041`) — "The :class:`Response <Response>` object, which contains a [server's response]." Calls `close`, `generate`, `iter_content`, and `raise_for_status`. Can raise `StreamConsumedError`, `HTTPError`, `TypeError`, and `RuntimeError` (`Response`, `src/requests/models.py:642-1041`).
- **`RequestEncodingMixin`** (`src/requests/models.py:86-205`) — provides encoding utilities like `_encode_params` and `_encode_files`.
- **`RequestHooksMixin`** (`src/requests/models.py:208-229`) — provides `register_hook`.

### Supporting Modules (not primary owners but tightly coupled)

- **`src/requests/adapters.py`** (697L) — owns the transport adapter layer (`BaseAdapter`, `HTTPAdapter`) that `Session` delegates actual network I/O to. `build_response()` constructs `Response` objects from urllib3 responses (`build_response`, `src/requests/adapters.py:337-372`).
- **`src/requests/structures.py`** — provides `CaseInsensitiveDict` (`src/requests/structures.py:13`) used by both `PreparedRequest` and `build_response`.
- **`src/requests/cookies.py`** — provides `RequestsCookieJar` (`src/requests/cookies.py:176`) used by `Session` and `prepare_request`.
- **`src/requests/exceptions.py`** — provides exception types like `InvalidSchema`, `MissingSchema`, `TooManyRedirects`, `HTTPError`, etc.
- **`src/requests/auth.py`** — provides `AuthBase` and `HTTPBasicAuth` (`src/requests/auth.py:76`) used by `PreparedRequest`.
- **`src/requests/hooks.py`** — provides `default_hooks` and `dispatch_hook` (`src/requests/hooks.py:34`).

### What Cannot Be Determined

- The clue file's INDEX notes "...and 16 more modules" beyond those listed; their ownership roles cannot be assessed.
- The GAPS section notes that `HTTPAdapter`, `RequestsDependencyWarning`, `build_connection_pool_key_attributes`, and `generate` are uncovered, so full detail on adapter internals is not available.
- The contents of `src/requests/__init__.py` (183L) are not fully enumerated, so we cannot confirm exactly which symbols are re-exported as the public API surface.
