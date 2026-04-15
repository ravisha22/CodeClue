# v2.2 Response: blind-requests-struct-2
Date: 2026-04-15

## Question

How do the Requests API docs divide the library into public layers, and which kinds of objects appear in each layer?

## Answer

The clue file does not contain the actual API documentation text (e.g., Sphinx-rendered doc pages). However, the INDEX, SYM, and FOCUS sections reveal a clear layered architecture with distinct object kinds at each level. The following layers can be inferred:

### Layer 1: Stateless Convenience API (`src/requests/api.py`, 157 L)

This is the simplest public surface. It exposes **module-level functions** — one per HTTP verb:

- `request` (`src/requests/api.py:14`) — "Constructs and sends a :class:`Request <Request>`." Called by `delete`, `get`, `head`, `options`, `patch`, `post`, `put`.
- `get` (`src/requests/api.py:62`), `head` (`src/requests/api.py:88`), `options` (`src/requests/api.py:76`), `post` (`src/requests/api.py:103`), `put` (`src/requests/api.py:118`), `patch` (`src/requests/api.py:133`), `delete` (`src/requests/api.py:148`).

**Object kinds in this layer:** Only plain functions. All have `DELEGATE(request -> result)` behavior, meaning they forward directly to the `request` function.

### Layer 2: Session Layer (`src/requests/sessions.py`, 833 L)

This layer provides **stateful session orchestration** via classes and their methods:

- **`Session`** (class, `src/requests/sessions.py:356`) — "A Requests session." Extends `SessionRedirectMixin`. Uses `PreparedRequest` (models), `RequestsCookieJar` (cookies), `Request` (models), `InvalidSchema` (exceptions). Calls `close`, `get`, `get_adapter`, `merge_environment_settings`, `mount`, `prepare_request`, `request`, `send`.
- **`session`** (factory function, `src/requests/sessions.py:821`) — "Returns a :class:`Session` for context-management." Behavior: `DELEGATE(Session -> result)`.
- **`SessionRedirectMixin`** (mixin class, `src/requests/sessions.py:107`) — Handles redirect logic. Calls `get_redirect_target`, `rebuild_auth`, `rebuild_method`, `rebuild_proxies`, `should_strip_auth`.

Session-level **utility functions** for merging settings:
- `merge_setting` (`src/requests/sessions.py:62`) — "Determines appropriate setting for a given request."
- `merge_hooks` (`src/requests/sessions.py:92`) — "Properly merges both requests and session hooks."
- `merge_environment_settings` (`src/requests/sessions.py:752`) — "Check the environment and merge it with some settings."

**Object kinds in this layer:** A primary class (`Session`), a mixin class (`SessionRedirectMixin`), a factory function (`session`), instance methods mirroring HTTP verbs (`get`, `post`, `put`, `delete`, `head`, `options`, `patch` — all at lines 595–673), and merge utility functions.

### Layer 3: Model / Data Types (`src/requests/models.py`, 1041 L)

This layer defines the **request and response data model classes**:

- **`Request`** (class, `src/requests/models.py:232`) — "A user-created :class:`Request <Request>` object." Extends `RequestHooksMixin`. Calls `PreparedRequest`, `register_hook`.
- **`PreparedRequest`** (class, `src/requests/models.py:315`) — "The fully mutable :class:`PreparedRequest <PreparedRequest>` object." Extends `RequestEncodingMixin`, `RequestHooksMixin`. Calls `prepare_auth`, `prepare_body`, `prepare_content_length`, `prepare_cookies`, `prepare_headers`, `prepare_hooks`.
- **`Response`** (class, `src/requests/models.py:642`) — "The :class:`Response <Response>` object." Calls `close`, `generate`, `iter_content`, `raise_for_status`. Raises `StreamConsumedError`, `HTTPError`, `TypeError`, `RuntimeError`.
- **`RequestEncodingMixin`** (mixin, `src/requests/models.py:86`) — Encoding helper mixin.
- **`RequestHooksMixin`** (mixin, `src/requests/models.py:208`) — Hook registration mixin with `register_hook` (`src/requests/models.py:209`).

**Object kinds in this layer:** Data-model classes (`Request`, `PreparedRequest`, `Response`), mixin classes (`RequestEncodingMixin`, `RequestHooksMixin`), and their instance methods (e.g., `iter_content`, `raise_for_status`, `close`, `prepare_body`).

### Layer 4: Transport Adapters (`src/requests/adapters.py`, 697 L)

This layer provides the **transport adapter abstraction**:

- **`BaseAdapter`** (class, from INDEX: `src/requests/adapters.py`) — Abstract base for transport adapters.
- **`HTTPAdapter`** (class, `src/requests/adapters.py:144`) — "The built-in HTTP Adapter for urllib3." Extends `BaseAdapter`. Calls `build_response`, `cert_verify`, `get_connection_with_tls_context`, `init_poolmanager`, `proxy_manager_for`, `proxy_headers`. Uses `Response` (models), `CaseInsensitiveDict` (structures).
- `build_response` (`src/requests/adapters.py:337`) — "Builds a :class:`Response <requests.Response>` object from a urllib3" response. Uses `Response` (models), `CaseInsensitiveDict` (structures).

**Object kinds in this layer:** An abstract base class (`BaseAdapter`), a concrete adapter class (`HTTPAdapter`), and their methods.

### Supporting Modules

Additional modules provide specialized object kinds used across layers:

| Module | Object Kinds | Key Symbols |
|---|---|---|
| `src/requests/auth.py` (314 L) | Auth handler classes | `AuthBase`, `HTTPBasicAuth` (classes); `build_digest_header` (method) |
| `src/requests/cookies.py` (561 L) | Cookie jar classes, cookie helpers | `RequestsCookieJar` (class, extends `CookieJar` + `MutableMapping`), `MockRequest` (class), `CookieConflictError` (exception class) |
| `src/requests/exceptions.py` (152 L) | Exception classes | `ConnectionError`, `ConnectTimeout`, `ChunkedEncodingError`, `ContentDecodingError`, `FileModeWarning` (extends `RequestsWarning`, `DeprecationWarning`) |
| `src/requests/structures.py` (99 L) | Utility data structures | `CaseInsensitiveDict` (class), `LookupDict` (class) |
| `src/requests/hooks.py` (34 L) | Hook functions | `default_hooks`, `dispatch_hook` |
| `src/requests/status_codes.py` (128 L) | Status code lookup | `doc` (function), and presumably `LookupDict` usage |

### Limitations

The clue file does not include the rendered Sphinx API documentation from `docs/`, so the exact headings and groupings used in the official API docs **cannot be determined**. The `docs/` tree shows only `docs/conf.py` (385 L) and `docs/_themes/flask_theme_support.py` (86 L), neither of which reveals documentation page structure. The layer decomposition above is inferred entirely from module structure, class hierarchy, and call relationships in the INDEX, SYM, and FOCUS sections.
