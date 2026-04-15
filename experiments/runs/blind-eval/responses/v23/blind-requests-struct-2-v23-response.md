# v2.3 Response: blind-requests-struct-2
Date: 2026-04-15

## Summary

Based on the clue file, the Requests library divides into four public layers: (1) a **top-level convenience API** (`api.py`) with stateless HTTP verb functions, (2) a **session orchestration layer** (`sessions.py`) with the `Session` class managing stateful request lifecycles, (3) a **model/data layer** (`models.py`) defining `Request`, `PreparedRequest`, and `Response` objects, and (4) a **transport adapter layer** (`adapters.py`) that bridges the library to urllib3. Supporting modules provide cookies, authentication, exceptions, structures, and utilities.

---

## Layer 1: Top-Level Convenience API (`src/requests/api.py`)

**157 lines.** Contains stateless HTTP verb functions that all delegate to a single `request()` function.

### Objects in this layer:

- **`request`** (src/requests/api.py:14-59, FOCUS): "Constructs and sends a :class:`Request <Request>`." The central function; called by all HTTP verb functions below.
- **`get`** (src/requests/api.py:62-73, FOCUS): `DELEGATE(request -> result)`.
- **`options`** (src/requests/api.py:76-85, FOCUS): `DELEGATE(request -> result)`.
- **`head`** (src/requests/api.py:88-100, FOCUS): `DELEGATE(request -> result)`.
- **`post`** (src/requests/api.py:103-115, FOCUS): `DELEGATE(request -> result)`. Accepts `data` and `json`.
- **`put`** (src/requests/api.py:118-130, FOCUS): `DELEGATE(request -> result)`. Accepts `data`.
- **`patch`** (src/requests/api.py:133-145, FOCUS): `DELEGATE(request -> result)`. Accepts `data`.
- **`delete`** (src/requests/api.py:148-157, FOCUS): `DELEGATE(request -> result)`.

**Pattern**: Pure functions — no classes, no state. Each is a thin wrapper around `request()`.

---

## Layer 2: Session Orchestration (`src/requests/sessions.py`)

**833 lines.** The stateful engine of the library. Manages persistent settings, cookie jars, adapter mounting, and request/response lifecycle.

### Primary objects:

- **`Session`** (src/requests/sessions.py:356-818, FOCUS): "A Requests session." Extends `SessionRedirectMixin`. Imports `adapters`, `auth`, `compat`, `cookies`, `exceptions`. This is the central class with methods:
  - `request`, `prepare_request`, `send` — request lifecycle
  - `get`, `head`, `options`, `post`, `put`, `patch`, `delete` — HTTP verb methods (each delegates to `request`)
  - `get_adapter`, `mount` — adapter management
  - `merge_environment_settings` — environment integration
  - `close` — cleanup
  - Uses: `PreparedRequest` (models), `RequestsCookieJar` (cookies), `Request` (models), `InvalidSchema` (exceptions).

- **`session`** (src/requests/sessions.py:821-833, FOCUS): Factory function; "returns a :class:`Session` for context-management." `DELEGATE(Session -> result)`.

- **`SessionRedirectMixin`** (src/requests/sessions.py:107-353, FOCUS): Mixin providing redirect handling. Contains:
  - `resolve_redirects` — follows redirect chain; `ACCUMULATE(loop -> hist)`; raises `TooManyRedirects`.
  - `get_redirect_target` — extracts redirect URL from response.
  - `rebuild_auth`, `rebuild_method`, `rebuild_proxies` — adjust request for redirects.
  - `should_strip_auth` — decides whether to strip Authorization header.

### Supporting functions:

- **`merge_setting`** (src/requests/sessions.py:62-89, FOCUS): Merges request and session settings; `ACCUMULATE(loop -> result)`.
- **`merge_hooks`** (src/requests/sessions.py:92-104, FOCUS): Merges request and session hooks.
- **`merge_environment_settings`** (src/requests/sessions.py:752, SYM): Merges environment with settings.
- **`prepare_request`** (src/requests/sessions.py:459-500, FOCUS): Constructs `PreparedRequest`; calls `merge_hooks`, `merge_setting`.

---

## Layer 3: Request/Response Models (`src/requests/models.py`)

**1041 lines.** Defines the data types that represent HTTP requests and responses.

### Request hierarchy:

- **`RequestHooksMixin`** (src/requests/models.py:208-229, FOCUS): Mixin for hook registration (`register_hook`). Can raise `ValueError`.
- **`RequestEncodingMixin`** (src/requests/models.py:86-205, FOCUS): Encoding utilities including `_encode_params` and `_encode_files`. Can raise `ValueError`.
- **`Request`** (src/requests/models.py:232-312, FOCUS): "A user-created :class:`Request <Request>` object." Extends `RequestHooksMixin`. Calls `PreparedRequest` and `register_hook`. This is the user-facing, immutable-ish request.
- **`PreparedRequest`** (src/requests/models.py:315-639, FOCUS): "The fully mutable :class:`PreparedRequest <PreparedRequest>` object." Extends both `RequestEncodingMixin` and `RequestHooksMixin`. Methods: `prepare_auth`, `prepare_body`, `prepare_content_length`, `prepare_cookies`, `prepare_headers`, `prepare_hooks`, `copy`, `_get_idna_encoded_host`. Uses `HTTPBasicAuth` (auth), `CaseInsensitiveDict` (structures). Can raise `MissingSchema`, `InvalidURL`, `UnicodeError`, `NotImplementedError`.

### Response:

- **`Response`** (src/requests/models.py:642-1041, FOCUS): "The :class:`Response <Response>` object." Methods:
  - `iter_content` — iterates over response data
  - `json` — decodes JSON body; raises `RequestsJSONDecodeError`
  - `raise_for_status` — raises `HTTPError` if error occurred
  - `close` — releases connection back to pool
  - `generate` — internal generator
  - Can raise `StreamConsumedError`, `HTTPError`, `TypeError`, `RuntimeError`.
  - Uses error classes from `exceptions`: `ChunkedEncodingError`, `ContentDecodingError`, `ConnectionError`, `RequestsSSLError`.

### Multipart encoding:

- **`_encode_files`** (src/requests/models.py:139-205, FOCUS): "Build the body for a multipart/form-data request." `ACCUMULATE(loop -> new_fields)`. Uses `RequestField` from urllib3.

---

## Layer 4: Transport Adapters (`src/requests/adapters.py`)

**697 lines.** Bridges the session layer to the actual HTTP transport (urllib3).

### Objects:

- **`BaseAdapter`** (src/requests/adapters.py, INDEX): Listed with `close` and `send` — the abstract base.
- **`HTTPAdapter`** (src/requests/adapters.py:144-697, FOCUS): "The built-in HTTP Adapter for urllib3." Extends `BaseAdapter`. Methods:
  - `init_poolmanager` — initializes urllib3 PoolManager
  - `proxy_manager_for` — returns ProxyManager for given proxy
  - `build_response` — builds `Response` from urllib3 response; uses `Response` (models), `CaseInsensitiveDict` (structures)
  - `build_connection_pool_key_attributes` — builds pool key attributes
  - `send` — sends PreparedRequest via urllib3
  - `add_headers`, `cert_verify`, `get_connection_with_tls_context`, `proxy_headers`
  - `request_url` — obtains the final request URL
  - Can raise `OSError`, `InvalidURL`, `InvalidProxyURL`, `ConnectionError`.
- **`_urllib3_request_context`** (src/requests/adapters.py:77-111, FOCUS): Builds request context for urllib3.
- **`SOCKSProxyManager`** (src/requests/adapters.py:63, SYM): SOCKS proxy support.

---

## Supporting Modules

### Cookies (`src/requests/cookies.py`, 561 lines)

- **`RequestsCookieJar`** (src/requests/cookies.py:176-437, FOCUS): "Compatibility class; is a http.cookiejar.CookieJar, but exposes a dict interface." Extends `CookieJar` and `MutableMapping`. Methods: `get`, `set`, `iterkeys`, `itervalues`, `iteritems`, `update`, `copy`, `_find`, `_find_no_duplicates`.
- **`MockRequest`** (src/requests/cookies.py:23-100, FOCUS): Wraps `requests.Request` to mimic `urllib2.Request` for cookie handling.
- **`MockResponse`** (referenced by `extract_cookies_to_jar`).
- **`extract_cookies_to_jar`** (src/requests/cookies.py:124-137, FOCUS): Extracts cookies from response.
- **`get_cookie_header`** (src/requests/cookies.py:140-148, FOCUS): Produces Cookie header string.
- **`create_cookie`** (src/requests/cookies.py:455, SYM), **`morsel_to_cookie`** (src/requests/cookies.py:492, SYM).
- **`CookieConflictError`** (src/requests/cookies.py:170, SYM): Exception for duplicate cookies.

### Authentication (`src/requests/auth.py`, 314 lines)

- **`AuthBase`** (SYM): Base authentication class.
- **`HTTPBasicAuth`** (SYM): Basic authentication.
- **`build_digest_header`** (SYM): Digest auth header builder.
- Helper functions: `_basic_auth_str`, `md5_utf8`, `sha256_utf8`, `sha512_utf8`.

### Exceptions (`src/requests/exceptions.py`, 152 lines)

- **`RequestException.__init__`** (src/requests/exceptions.py:18-25, FOCUS): Initializes with `request` and `response` objects.
- **`FileModeWarning`** (FOCUS): Extends `RequestsWarning` and `DeprecationWarning`.
- **`RequestsWarning`** (FOCUS): Base warning.
- **`UnrewindableBodyError`** (FOCUS): Body rewind error.
- Listed in INDEX: `ChunkedEncodingError`, `ConnectTimeout`, `ConnectionError`, `ContentDecodingError`, `FileModeWarning` and more.

### Structures (`src/requests/structures.py`, 99 lines)

- **`CaseInsensitiveDict`** (src/requests/structures.py:13, SYM): "A case-insensitive dict-like object." Used extensively for HTTP headers throughout the library.
- **`LookupDict`** (INDEX): Lookup dictionary utility.
- **`lower_items`** (src/requests/structures.py:63, SYM): "Like iteritems(), but with all lowercase keys."

### Hooks (`src/requests/hooks.py`, 34 lines)

- **`default_hooks`** and **`dispatch_hook`** (INDEX): Hook management.

### Utilities (`src/requests/utils.py`)

- **`default_headers`** (src/requests/utils.py:887-898, FOCUS): Returns `CaseInsensitiveDict` with default headers. Calls `default_user_agent`.
- **`get_netrc_auth`** (src/requests/utils.py:206-247, FOCUS): "Returns the Requests tuple auth for a given url from netrc."
- **`should_bypass_proxies`** (SYM), **`unquote_header_value`** (SYM), **`get_encoding_from_headers`** (SYM), **`unquote_unreserved`** (SYM), **`_parse_content_type_header`** (SYM), **`dotted_netmask`** (SYM), **`proxy_bypass_registry`** (SYM), **`default_user_agent`** (SYM), **`_validate_header_part`** (SYM).

### Other Modules

- **`src/requests/__init__.py`** (183 lines): Package init with `check_compatibility`.
- **`src/requests/__version__.py`** (14 lines): Version info.
- **`src/requests/_internal_utils.py`** (51 lines): `to_native_string`, `unicode_is_ascii`.
- **`src/requests/compat.py`** (106 lines): Compatibility layer.
- **`src/requests/certs.py`** (18 lines): Certificate utilities.
- **`src/requests/status_codes.py`** (128 lines): Status code lookup with `doc` function.
- **`src/requests/help.py`** (131 lines): `info` and `main` for bug reports.
- **`src/requests/packages.py`** (23 lines): Package path management.

---

## Layer Interaction Summary

```
User Code
  │
  ▼
api.py (get/post/put/...) ──delegates──> sessions.py:Session.request()
  │                                           │
  │                                           ├── models.py: Request → PreparedRequest
  │                                           ├── cookies.py: RequestsCookieJar
  │                                           ├── sessions.py: merge_setting, merge_hooks
  │                                           │
  │                                           ▼
  │                                     sessions.py:Session.send()
  │                                           │
  │                                           ├── adapters.py: HTTPAdapter.send()
  │                                           │     └── builds Response from urllib3
  │                                           │
  │                                           └── sessions.py: resolve_redirects()
  │                                                 └── loops with send()
  │
  ▼
models.py: Response (iter_content, json, raise_for_status, close)
```

---

## Uncertainty / Limits

- The `api.py:request()` function body is not shown; the exact mechanism for creating a `Session` from the module-level functions is inferred from the `session` factory and the delegation pattern.
- The `__init__.py` re-exports are not detailed, so the exact public API surface as seen by `import requests` is not fully enumerable.
- 16 more modules and 217 more symbols are not shown, so there may be additional public-facing functionality not captured.
- The `docs/` directory has only `conf.py` and a theme file visible; no actual API documentation structure is shown, so the "API docs" layering is inferred entirely from code structure rather than documentation pages.
- The `tests/` directory (15 files) is listed but not analyzed, so test-implied API boundaries are not considered.
