# v2.4 Response: blind-requests-struct-2
Date: 2026-04-16

## Question
How do the Requests API docs divide the library into public layers, and which kinds of objects appear in each layer?

## Answer

Based on the clue file, the Requests library can be divided into the following public layers, each containing distinct kinds of objects:

### Layer 1: Convenience API (Stateless Functions) — `src/requests/api.py`

This is the simplest, highest-level entry point. It consists of pure functions, each delegating to a single central `request()` dispatcher:

- **`request(method, url)`** — "Constructs and sends a :class:`Request <Request>`" (`request`, `src/requests/api.py:14-59`).
- **`get(url, params)`** — `DELEGATE(request -> result)` (`get`, `src/requests/api.py:62-73`).
- **`options(url)`** — `DELEGATE(request -> result)` (`options`, `src/requests/api.py:76-85`).
- **`head(url)`** — `DELEGATE(request -> result)` (`head`, `src/requests/api.py:88-100`).
- **`post(url, data, json)`** — `DELEGATE(request -> result)` (`post`, `src/requests/api.py:103-115`).
- **`put(url, data)`** — `DELEGATE(request -> result)` (`put`, `src/requests/api.py:118-130`).
- **`patch(url, data)`** — `DELEGATE(request -> result)` (`patch`, `src/requests/api.py:133-145`).
- **`delete(url)`** — `DELEGATE(request -> result)` (`delete`, `src/requests/api.py:148-157`).

**Object kinds in this layer:** Module-level functions only. All are called_by the specific HTTP verb functions and delegate downward. No classes are defined here.

### Layer 2: Session Orchestration (Stateful Controller) — `src/requests/sessions.py`

This layer provides a persistent, stateful session that manages configuration, cookies, adapters, and the full request lifecycle:

- **`Session`** (class, `src/requests/sessions.py:356-818`) — "A Requests session." Extends `SessionRedirectMixin`. Calls `close`, `get`, `get_adapter`, `merge_environment_settings`, `mount`, `prepare_request`, `request`, `send` (`Session`, `src/requests/sessions.py:356-818`). Uses `PreparedRequest` (models), `Request` (models), `RequestsCookieJar` (cookies), `InvalidSchema` (exceptions).
- **`SessionRedirectMixin`** (mixin class, `src/requests/sessions.py:107-353`) — handles redirect logic via `resolve_redirects`, `get_redirect_target`, `rebuild_auth`, `rebuild_method`, `rebuild_proxies`, `should_strip_auth`.
- **`session()`** (factory, `src/requests/sessions.py:821-833`) — "Returns a :class:`Session` for context-management." `DELEGATE(Session -> result)`.
- **Helper functions:** `merge_setting(request_setting, session_setting, dict_class)` (`src/requests/sessions.py:62-89`) — merges per-request and session settings. `merge_hooks(request_hooks, session_hooks, dict_class)` (`src/requests/sessions.py:92-104`) — merges request and session hooks.
- **Session HTTP methods:** `Session.get`, `Session.post`, `Session.put`, `Session.delete`, `Session.head`, `Session.options`, `Session.patch` — all delegate to `Session.request()`.

**Object kinds in this layer:** One primary class (`Session`), one mixin (`SessionRedirectMixin`), one factory function, and several merge/helper functions. The `Session` mirrors the Layer 1 verb functions but in a stateful context.

### Layer 3: Request/Response Models (Data Objects) — `src/requests/models.py`

This layer defines the data types that flow through the pipeline:

- **`Request`** (class, `src/requests/models.py:232-312`) — "A user-created :class:`Request <Request>` object." Extends `RequestHooksMixin`. Calls `PreparedRequest` and `register_hook`.
- **`PreparedRequest`** (class, `src/requests/models.py:315-639`) — "The fully mutable :class:`PreparedRequest <PreparedRequest>` object." Extends `RequestEncodingMixin`, `RequestHooksMixin`. Has preparation methods: `prepare_auth`, `prepare_body`, `prepare_content_length`, `prepare_cookies`, `prepare_headers`, `prepare_hooks`.
- **`Response`** (class, `src/requests/models.py:642-1041`) — contains the server's response. Provides `iter_content`, `json`, `raise_for_status`, `close`. Raises `StreamConsumedError`, `HTTPError`, `TypeError`, `RuntimeError`.
- **`RequestEncodingMixin`** (mixin, `src/requests/models.py:86-205`) — provides `_encode_params` and `_encode_files`.
- **`RequestHooksMixin`** (mixin, `src/requests/models.py:208-229`) — provides `register_hook`.

**Object kinds in this layer:** Model/data classes (`Request`, `PreparedRequest`, `Response`) and mixin classes.

### Layer 4: Transport Adapters (Network I/O) — `src/requests/adapters.py`

This layer handles actual HTTP transport:

- **`BaseAdapter`** (abstract class, `src/requests/adapters.py:114-141`) — "The Base Transport Adapter." Raises `NotImplementedError` (`BaseAdapter`, `src/requests/adapters.py:114-141`).
- **`HTTPAdapter`** (class, `src/requests/adapters.py:144-697`) — "The built-in HTTP Adapter for urllib3." Extends `BaseAdapter`. Provides `send`, `build_response`, `init_poolmanager`, `proxy_manager_for`, `cert_verify`, `get_connection_with_tls_context`, `request_url`, `add_headers`, `proxy_headers` (`HTTPAdapter`, `src/requests/adapters.py:144-697`).
- **`build_response(req, resp)`** (`src/requests/adapters.py:337-372`) — "Builds a :class:`Response <requests.Response>` object from a urllib3" response. Uses `Response` (models), `CaseInsensitiveDict` (structures).

**Object kinds in this layer:** Abstract base class and concrete adapter implementation.

### Layer 5: Supporting Infrastructure

Several modules provide cross-cutting types used across the layers above:

- **Structures** (`src/requests/structures.py`) — `CaseInsensitiveDict` (class, `src/requests/structures.py:13`) — "A case-insensitive ``dict``-like object." `LookupDict` (class).
- **Cookies** (`src/requests/cookies.py`) — `RequestsCookieJar` (class, `src/requests/cookies.py:176-437`) — "Compatibility class; is a http.cookiejar.CookieJar, but exposes a dict" interface. Extends `CookieJar`, `MutableMapping`. Also `MockRequest` (class, `src/requests/cookies.py:23-100`) — "Wraps a `requests.Request` to mimic a `urllib2.Request`." Internal helper functions: `extract_cookies_to_jar`, `get_cookie_header`, `create_cookie`, `morsel_to_cookie`.
- **Auth** (`src/requests/auth.py`) — `AuthBase` (abstract class), `HTTPBasicAuth` (class, extends `AuthBase`), `HTTPDigestAuth` (class), `HTTPProxyAuth` (class).
- **Exceptions** (`src/requests/exceptions.py`) — Hierarchy rooted at `RequestException` (extends `IOError`, `src/requests/exceptions.py:13-25`). Includes `ConnectionError`, `HTTPError`, `URLRequired`, `TooManyRedirects`, `MissingSchema`, `InvalidSchema`, `InvalidURL`, `ChunkedEncodingError`, `ContentDecodingError`, `StreamConsumedError`, `ConnectTimeout`, `ReadTimeout`, `Timeout`, `UnrewindableBodyError`. Warnings: `RequestsWarning` (extends `Warning`), `FileModeWarning` (extends `RequestsWarning, DeprecationWarning`), `RequestsDependencyWarning` (extends `RequestsWarning`).
- **Hooks** (`src/requests/hooks.py`) — `default_hooks`, `dispatch_hook` (functions).
- **Status codes** (`src/requests/status_codes.py`) — `doc` function; `LookupDict` used here.
- **Utilities** (`src/requests/utils.py`) — many helper functions including `get_netrc_auth`, `default_headers`, `default_user_agent`, `get_encoding_from_headers`, `should_bypass_proxies`, etc.

**Object kinds in this layer:** Utility classes, exception hierarchies, authentication classes, cookie jar classes, and helper functions.

### What Cannot Be Determined

- The clue file does not include the contents of `src/requests/__init__.py` beyond noting it has 183 lines and a `check_compatibility` symbol. The exact set of symbols re-exported as the official public API cannot be confirmed.
- The INDEX notes "...and 16 more modules" — those modules' roles in the public API layering are unknown.
- The GAPS section notes `get_header`, `get_new_headers`, `head`, and `host` are uncovered, so some cookie-layer internal details are incomplete.
- Whether the library's own documentation explicitly names these "layers" or uses different terminology cannot be determined from the clue file alone.
