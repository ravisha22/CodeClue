# Scaffold (Sonnet 4.6): blind-requests-struct-1
Date: 2026-04-16

## Question

Which public modules in Requests own the top-level request API, session orchestration, and the request/response model types?

## Reasoning Scaffold

### 1. Identify Relevant Modules from INDEX and TREE

The INDEX lists 9 key modules under `src/requests/`. Three stand out for the responsibilities asked about:

| Responsibility | Module | Size |
|---|---|---|
| Top-level request API | `src/requests/api.py` | 157 L |
| Session orchestration | `src/requests/sessions.py` | 833 L |
| Request/response model types | `src/requests/models.py` | 1041 L |

### 2. Top-Level Request API — `api.py`

`api.py` is the public convenience layer. It exposes seven HTTP-verb functions and one generic dispatcher:

- **`request(method, url)`** (`api.py:14`): "Constructs and sends a :class:`Request <Request>`." This is the central dispatcher. Every verb function delegates to it (FOCUS: `called_by: delete, get, head, options, patch, post, put`).
- **`get(url, params)`** (`api.py:62`): behavior `DELEGATE(request -> result)`, calls `request`.
- **`head(url)`** (`api.py:88`): behavior `DELEGATE(request -> result)`, calls `request`.
- **`options(url)`** (`api.py:76`): behavior `DELEGATE(request -> result)`, calls `request`.
- **`post(url, data, json)`** (`api.py:103`): behavior `DELEGATE(request -> result)`, calls `request`.
- **`put(url, data)`** (`api.py:118`): behavior `DELEGATE(request -> result)`, calls `request`.
- **`patch(url, data)`** (`api.py:133`): behavior `DELEGATE(request -> result)`, calls `request`.
- **`delete(url)`** (`api.py:148`): behavior `DELEGATE(request -> result)`, calls `request`.

All seven verb functions share the identical DELEGATE pattern: they forward to `request()` and return its result. This makes `api.py` a thin, stateless façade — it owns no session state and carries no redirect or adapter logic itself.

### 3. Session Orchestration — `sessions.py`

`sessions.py` is the largest of the three modules (833 L) and owns all stateful orchestration. Key symbols:

- **`Session` class** (`sessions.py:356`): "A Requests session." Extends `SessionRedirectMixin`. The FOCUS entry shows it imports from `adapters`, `auth`, `compat`, `cookies`, and `exceptions`, and it uses `PreparedRequest` and `Request` from `models` as well as `RequestsCookieJar` from `cookies`. It calls `close`, `get`, `get_adapter`, `merge_environment_settings`, `mount`, `prepare_request`, `request`, and `send`. It raises `InvalidSchema` and `ValueError`.

- **`Session.request(method, url, …)`** (`sessions.py:502`): "Constructs a :class:`Request <Request>`, prepares it and sends it." This is the full-lifecycle method: it calls `prepare_request` → `merge_environment_settings` → `send`. It is itself called by the seven verb methods on Session (`called_by: delete, get, head, options, patch, post, put, Session`).

- **`Session.prepare_request(request)`** (`sessions.py:459`): Builds a `PreparedRequest` from a user-level `Request`, merging hooks and settings via `merge_hooks` and `merge_setting`.

- **`Session.send(prepared_request)`** (`sessions.py:675`): "Send a given PreparedRequest." Behavior annotation: `BRANCH(allow_redirects -> self.resolve_redirect..., else -> [])`. Calls `get_adapter` to select the transport adapter, and `resolve_redirects` for redirect chains.

- **`SessionRedirectMixin`** (`sessions.py:107`): The redirect-handling base class. Imports from `adapters`, `auth`, `compat`, `cookies`, `exceptions`. Calls `close`, `get`, `send`, `get_redirect_target`, `rebuild_auth`, `rebuild_method`, `rebuild_proxies`, `should_strip_auth`. Raises `TooManyRedirects`.

- **`session()` factory** (`sessions.py:821`): "Returns a :class:`Session` for context-management." Behavior: `DELEGATE(Session -> result)`.

Supporting module-level helpers:
- **`merge_setting`** (`sessions.py:62`): "Determines appropriate setting for a given request."
- **`merge_hooks`** (`sessions.py:92`): "Properly merges both requests and session hooks." Calls `merge_setting`.
- **`merge_environment_settings`** (`sessions.py:752`): "Check the environment and merge it with some settings."
- **`resolve_redirects`** (`sessions.py:160`): "Receives a Response." Used by `send` for redirect chains.
- **`get_adapter`** (`sessions.py:783`): "Returns the appropriate connection adapter."
- **`mount`** (`sessions.py:801`): "Registers a connection adapter to a prefix."
- **`close`** (`sessions.py:796`): "Closes all adapters and as such the session."

### 4. Request/Response Model Types — `models.py`

`models.py` is the largest module (1041 L) and defines the data-carrying types:

- **`Request` class** (`models.py:232`): "A user-created :class:`Request <Request>` object." Extends `RequestHooksMixin`. Calls `PreparedRequest` and `register_hook`. This is the high-level, user-facing request object.

- **`PreparedRequest` class** (`models.py:315`): "The fully mutable :class:`PreparedRequest <PreparedRequest>` object." Extends both `RequestEncodingMixin` and `RequestHooksMixin`. Provides the full prepare pipeline: `prepare_auth`, `prepare_body`, `prepare_content_length`, `prepare_cookies`, `prepare_headers`, `prepare_hooks`. Raises `MissingSchema`, `InvalidURL`, `UnicodeError`, `NotImplementedError`. Uses `HTTPBasicAuth` (auth), `CaseInsensitiveDict` (structures), and exception types from `exceptions`.

- **`Response` class** (`models.py:642`): "The :class:`Response <Response>` object, which contains a server's response to an HTTP request." Calls `close`, `generate`, `iter_content`, `raise_for_status`. Raises `StreamConsumedError`, `HTTPError`, `TypeError`, `RuntimeError`. Uses exception types from `exceptions` (`ChunkedEncodingError`, `ContentDecodingError`, `ConnectionError`, `RequestsSSLError`).

- **`RequestEncodingMixin`** (`models.py:86`): Encoding utility base. Raises `ValueError`.

- **`RequestHooksMixin`** (`models.py:208`): Hook-registration base. Raises `ValueError`. Shared by both `Request` and `PreparedRequest`.

### 5. Call-Chain Summary

The canonical call chain, traced from FOCUS entries:

```
api.get()  ──DELEGATE──▶  api.request()
                              │
                              ▼
                     Session.request()          [sessions.py:502]
                       ├─▶ prepare_request()    [sessions.py:459]
                       │     ├─▶ merge_hooks()
                       │     └─▶ merge_setting()
                       │     └─▶ uses PreparedRequest (models)
                       ├─▶ merge_environment_settings()
                       └─▶ send()               [sessions.py:675]
                             ├─▶ get_adapter()
                             └─▶ resolve_redirects()
                                   └─▶ send() (recursive for redirects)
```

The adapter layer (`adapters.py`) sits below `send()`. Its `build_response()` function (`adapters.py:337`) constructs a `Response` object from `models` and wraps the urllib3 response, closing the loop back to model types.

### 6. Gaps and Uncertainty

Per the GAPS section:
- **Coverage**: 80 symbols at L3 detail; only 28 have behavior annotations.
- **Uncovered symbols**: `RequestsDependencyWarning`, `build_connection_pool_key_attributes`, `generate`, `HTTPAdapter` — these lack full FOCUS entries.
- **Gap type**: STRUCTURAL — answerable from L0–L2 data, meaning the module-ownership question is fully determinable from the clue set.
- The internal implementation of `api.request()` delegating to `Session` is implied by its docstring ("Constructs and sends a :class:`Request`") and by the parallel `Session.request` entry, but the exact bridging code (whether `api.request` instantiates a `Session` internally) is not explicitly annotated in the FOCUS entries. However, the `session()` factory (`sessions.py:821`) and the structural pattern strongly suggest `api.request` creates a one-off `Session`.

### 7. Synthesis

| Responsibility | Owning Module | Key Public Symbols |
|---|---|---|
| **Top-level request API** | `src/requests/api.py` | `request`, `get`, `head`, `options`, `post`, `put`, `patch`, `delete` — all stateless DELEGATE wrappers |
| **Session orchestration** | `src/requests/sessions.py` | `Session` (class), `session` (factory), plus methods `request`, `prepare_request`, `send`, `resolve_redirects`, `get_adapter`, `mount`, `close`, `merge_setting`, `merge_hooks`, `merge_environment_settings`; base class `SessionRedirectMixin` |
| **Request/response model types** | `src/requests/models.py` | `Request`, `PreparedRequest`, `Response` (classes); mixins `RequestEncodingMixin`, `RequestHooksMixin` |

These three modules form a clean layered architecture: **`api.py`** (stateless convenience) → **`sessions.py`** (stateful orchestration) → **`models.py`** (data types), with `adapters.py` handling transport below them.
