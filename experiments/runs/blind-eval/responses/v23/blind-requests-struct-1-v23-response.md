# v2.3 Response: blind-requests-struct-1
Date: 2026-04-15

## Summary

The Requests library organizes its public API across three key modules: `src/requests/api.py` provides the top-level convenience functions (e.g., `get`, `post`), `src/requests/sessions.py` houses the `Session` class that orchestrates request preparation, sending, and redirect handling, and `src/requests/models.py` defines the core `Request`, `PreparedRequest`, and `Response` data types. A transport adapter layer in `src/requests/adapters.py` bridges sessions to the underlying HTTP library.

---

## Top-Level Request API: `src/requests/api.py`

This module provides stateless convenience functions that each delegate to a central `request()` function:

- **`request`** (src/requests/api.py:14-59, FOCUS): "Constructs and sends a :class:`Request <Request>`." This is the single entry point; called by all HTTP method functions below.
- **`get`** (src/requests/api.py:62-73, FOCUS): "Sends a GET request." Signature: `get(url, params)`. Behavior: `DELEGATE(request -> result)`. Calls `request`.
- **`options`** (src/requests/api.py:76-85, FOCUS): "Sends an OPTIONS request." Behavior: `DELEGATE(request -> result)`. Calls `request`.
- **`head`** (src/requests/api.py:88-100, FOCUS): "Sends a HEAD request." Behavior: `DELEGATE(request -> result)`. Calls `request`.
- **`post`** (src/requests/api.py:103-115, FOCUS): "Sends a POST request." Signature: `post(url, data, json)`. Behavior: `DELEGATE(request -> result)`. Calls `request`.
- **`put`** (src/requests/api.py:118-130, FOCUS): "Sends a PUT request." Signature: `put(url, data)`. Behavior: `DELEGATE(request -> result)`. Calls `request`.
- **`patch`** (src/requests/api.py:133-145, FOCUS): "Sends a PATCH request." Signature: `patch(url, data)`. Behavior: `DELEGATE(request -> result)`. Calls `request`.
- **`delete`** (src/requests/api.py:148-157, FOCUS): "Sends a DELETE request." Behavior: `DELEGATE(request -> result)`. Calls `request`.

**Key pattern**: Every function in `api.py` delegates to `request()`, which in turn (based on the Session's `request` description) creates a `Session`, prepares the request, and sends it.

---

## Session Orchestration: `src/requests/sessions.py`

### `Session` Class

- **`Session`** (src/requests/sessions.py:356-818, FOCUS): "A Requests session." Extends `SessionRedirectMixin`. Imports: `adapters`, `auth`, `compat`, `cookies`, `exceptions`. Calls: `close`, `get`, `get_adapter`, `merge_environment_settings`, `mount`, `prepare_request`, `request`, `send`. Called by: `session`. Can raise `InvalidSchema`, `ValueError`. Uses: `InvalidSchema` (exceptions), `PreparedRequest` (models), `RequestsCookieJar` (cookies), `Request` (models).

  The Session is the central orchestrator — it:
  1. Prepares requests via `prepare_request`
  2. Merges environment settings via `merge_environment_settings`
  3. Sends via `send`
  4. Manages adapters via `get_adapter` and `mount`
  5. Handles cookies via `RequestsCookieJar`

### `session` Factory

- **`session`** (src/requests/sessions.py:821-833, FOCUS): "Returns a :class:`Session` for context-management." Behavior: `DELEGATE(Session -> result)`. Calls `Session`.

### Session HTTP Methods

The Session mirrors the top-level API with instance methods that all delegate to `Session.request`:

- **`Session.request`** (src/requests/sessions.py:502-593, FOCUS): "Constructs a :class:`Request <Request>`, prepares it and sends it." Signature: `request(method, url, params, data, headers...)`. Calls: `merge_environment_settings`, `prepare_request`, `send`. Called by: `delete`, `get`, `head`, `options`, `patch`, `post`, `put`, and `Session`. Uses: `Request` (models).
- **`Session.get`** (src/requests/sessions.py:595-604, FOCUS): Behavior: `DELEGATE(request -> result)`.
- **`Session.options`** (src/requests/sessions.py:606-615, FOCUS): Same pattern.
- **`Session.head`** (src/requests/sessions.py:617-626, FOCUS): Same pattern.
- **`Session.post`** (src/requests/sessions.py:628-639, FOCUS): Same pattern.
- **`Session.put`** (src/requests/sessions.py:641-651, FOCUS): Same pattern.
- **`Session.patch`** (src/requests/sessions.py:653-663, FOCUS): Same pattern.
- **`Session.delete`** (src/requests/sessions.py:665-673, FOCUS): Same pattern.

### Request Preparation

- **`prepare_request`** (src/requests/sessions.py:459-500, FOCUS): "Constructs a :class:`PreparedRequest <PreparedRequest>`." Calls: `merge_hooks`, `merge_setting`. Uses: `PreparedRequest` (models), `RequestsCookieJar` (cookies). Called by: `request` and `Session`.

### Settings Merging

- **`merge_setting`** (src/requests/sessions.py:62-89, FOCUS): "Determines appropriate setting for a given request, taking into account the session settings." Behavior: `ACCUMULATE(loop -> result)`. Called by: `merge_environment_settings`, `prepare_request`, `Session`, `merge_hooks`.
- **`merge_hooks`** (src/requests/sessions.py:92-104, FOCUS): "Properly merges both requests and session hooks." Calls: `get`, `merge_setting`. Called by: `prepare_request`, `Session`.
- **`merge_environment_settings`** (src/requests/sessions.py:752, SYM): "Check the environment and merge it with some settings."

### Sending and Redirect Handling

- **`send`** (src/requests/sessions.py:675, SYM): "Send a given PreparedRequest."
- **`SessionRedirectMixin`** (src/requests/sessions.py:107-353, FOCUS): Mixin handling redirects. Calls: `close`, `get`, `send`, `get_redirect_target`, `rebuild_auth`, `rebuild_method`, `rebuild_proxies`, `should_strip_auth`. Can raise `TooManyRedirects`.
- **`resolve_redirects`** (src/requests/sessions.py:160-280, FOCUS): "Receives a Response." Behavior: `ACCUMULATE(loop -> hist)`. Calls: `close`, `send`, `get_redirect_target`, `rebuild_auth`, `rebuild_method`, `rebuild_proxies`. Can raise `TooManyRedirects`.
- **`get_redirect_target`** (src/requests/sessions.py:108, SYM): "Receives a Response" — extracts redirect target.
- **`should_strip_auth`** (src/requests/sessions.py:128, SYM): "Decide whether Authorization header should be removed."

### Adapter Management

- **`get_adapter`** (src/requests/sessions.py:783, SYM): "Returns the appropriate connection adapter for a given URL."
- **`mount`** (src/requests/sessions.py:801, SYM): "Registers a connection adapter to a prefix."
- **`close`** (src/requests/sessions.py:796, SYM): "Closes all adapters and as such the session."

---

## Request/Response Model Types: `src/requests/models.py`

### `Request`

- **`Request`** (src/requests/models.py:232-312, FOCUS): "A user-created :class:`Request <Request>` object." Extends `RequestHooksMixin`. Calls: `PreparedRequest`, `register_hook`. This is the high-level, user-facing request object.

### `PreparedRequest`

- **`PreparedRequest`** (src/requests/models.py:315-639, FOCUS): "The fully mutable :class:`PreparedRequest <PreparedRequest>` object." Extends `RequestEncodingMixin`, `RequestHooksMixin`. Calls: `_get_idna_encoded_host`, `copy`, `prepare_auth`, `prepare_body`, `prepare_content_length`, `prepare_cookies`, `prepare_headers`, `prepare_hooks`. Can raise `MissingSchema`, `InvalidURL`, `UnicodeError`, `NotImplementedError`. Uses: `HTTPBasicAuth` (auth), `InvalidJSONError` (exceptions), `CaseInsensitiveDict` (structures), `MissingSchema` (exceptions).

  This is the processed, ready-to-send request object with explicit preparation methods for each part of the HTTP request.

### `Response`

- **`Response`** (src/requests/models.py:642-1041, FOCUS): "The :class:`Response <Response>` object, which contains a server's response." Calls: `close`, `generate`, `iter_content`, `raise_for_status`. Can raise `StreamConsumedError`, `HTTPError`, `TypeError`, `RuntimeError`. Uses: `ChunkedEncodingError`, `ContentDecodingError`, `ConnectionError`, `RequestsSSLError` (all from exceptions).

  Key methods:
  - **`iter_content`** (src/requests/models.py:801, SYM): "Iterates over the response data."
  - **`generate`** (src/requests/models.py:818, SYM): Internal generator function.
  - **`raise_for_status`** (src/requests/models.py:1001, SYM): "Raises :class:`HTTPError`, if one occurred."
  - **`json`** (src/requests/models.py:949-982, FOCUS): "Decodes the JSON response body." Can raise `RequestsJSONDecodeError`.
  - **`close`** (src/requests/models.py:1030, SYM): "Releases the connection back to the pool."

### Mixin Classes

- **`RequestEncodingMixin`** (src/requests/models.py:86-205, FOCUS): Provides encoding utilities. Can raise `ValueError`.
- **`RequestHooksMixin`** (src/requests/models.py:208-229, FOCUS): Provides hook registration (`register_hook`). Can raise `ValueError`.
- **`_encode_files`** (src/requests/models.py:139-205, FOCUS): "Build the body for a multipart/form-data request." Behavior: `ACCUMULATE(loop -> new_fields)`. Uses `RequestField` from urllib3.

### Encoding and Preparation

- **`prepare_content_length`** (src/requests/models.py:574, SYM): "Prepare Content-Length header based on request body."
- **`_encode_params`** (src/requests/models.py:109, SYM): "Encode parameters in a piece of data."
- **`register_hook`** (src/requests/models.py:209, SYM): "Properly register a hook."

---

## Supporting Modules

### Transport Adapter: `src/requests/adapters.py`

- **`build_response`** (src/requests/adapters.py:337-372, FOCUS): "Builds a :class:`Response <requests.Response>` object from a urllib3 response." Uses `Response` (models) and `CaseInsensitiveDict` (structures). Called by `HTTPAdapter`.
- **`_urllib3_request_context`** (src/requests/adapters.py:77-111, FOCUS): Builds urllib3 request context. Called by `build_connection_pool_key_attributes` and `HTTPAdapter`.
- **`request_url`** (src/requests/adapters.py:524-554, FOCUS): "Obtain the url to use when making the final request." Called by `HTTPAdapter`.

### Cookie Management: `src/requests/cookies.py`

- **`MockRequest`** (src/requests/cookies.py:23-100, FOCUS): "Wraps a `requests.Request` to mimic a `urllib2.Request`." Called by `extract_cookies_to_jar` and `get_cookie_header`.
- **`RequestsCookieJar`** (src/requests/cookies.py:176, SYM): "Compatibility class; is a http.cookiejar.CookieJar, but exposes a dict interface."

### Hooks: `src/requests/hooks.py`

- Listed in INDEX (34 lines): `default_hooks`, `dispatch_hook`.

---

## Uncertainty / Limits

- The `api.py:request()` function's body is not shown in the source snippets; based on the call chain, it likely creates a `Session` and calls `Session.request`, but this is inferred from the `session` factory and the pattern of delegation.
- The `send` method (sessions.py:675) is referenced but not detailed in FOCUS, so the exact sending mechanism (how it calls adapters) is partially opaque.
- The INDEX shows "...and 16 more modules" and SYM shows "...and 217 more symbols," so utility modules (`utils.py`, `compat.py`, etc.) are only partially visible.
- The `__init__.py` file (183 lines) with `check_compatibility` is listed but its re-exports are not detailed — the public API surface as exposed to end users is not fully enumerable from the clue file alone.
