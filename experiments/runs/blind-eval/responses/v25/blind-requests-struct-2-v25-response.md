# v2.5 Response: blind-requests-struct-2
Date: 2026-04-16

## Answer

The Requests library (CC v2.1 requests@HEAD, 36 modules, 757 symbols — per =CC clue header) organizes its public surface into five distinct architectural layers, each living in its own module. Below is a detailed account of every layer, the kinds of objects each contains, and how they interconnect.

---

### 1. Top-level API layer — `api.py`

The outermost layer is a collection of **stateless convenience functions** that serve as the simplest entry point for callers. The INDEX entry for `src/requests/api.py` (157 lines) lists these public names: `delete`, `get`, `head`, `options`, `patch` (INDEX: api.py). The FOCUS entry for `request` (api.py:14–59) confirms that this single orchestrating function is `called_by: delete, get, head, options, patch, post, put` (FOCUS: request, api.py:14–59). Each verb-named function is therefore a thin wrapper that delegates to `request()`.

Critically, these functions are **stateless**: they do not maintain cookies, connection pools, or other persistent state across calls. Every invocation constructs a fresh context internally. The `request()` function in `api.py` creates a one-shot `Session`, calls its own `request()` method, and tears it down — bridging the API layer to the Session layer below.

**Object kinds in this layer:** pure functions only (`request`, `get`, `post`, `put`, `delete`, `head`, `options`, `patch`). No classes are defined here.

---

### 2. Session layer — `sessions.py`

The second layer introduces **statefulness**. The INDEX entry for `src/requests/sessions.py` (833 lines) lists methods such as `close`, `delete`, `get`, `get_adapter`, `head` (INDEX: sessions.py). The FOCUS entry for `Session` (sessions.py:356–818) reveals that it `extends SessionRedirectMixin` and `uses PreparedRequest (models), RequestsCookieJar (cookies), Request (models)` (FOCUS: Session, sessions.py:356–818).

The `Session` class mirrors the top-level API verbs (`get`, `post`, `put`, `delete`, `head`, `options`, `patch`) but retains cookies, default headers, authentication, and transport adapters across calls. Beyond the HTTP-verb methods, it exposes **session-orchestration machinery**:

- `prepare_request` — converts a high-level `Request` into a `PreparedRequest` (FOCUS: request, sessions.py:502–593, which lists `calls: … prepare_request`).
- `send` — dispatches a `PreparedRequest` through a transport adapter (FOCUS: request, sessions.py:502–593, which lists `calls: … send`).
- `merge_environment_settings` — folds environment-level proxy/cert configuration into per-request settings (FOCUS: request, sessions.py:502–593, which lists `calls: merge_environment_settings`).
- `get_adapter` — selects the appropriate transport adapter for a URL (INDEX: sessions.py lists `get_adapter`).
- `resolve_redirects` — inherited from `SessionRedirectMixin` and responsible for following redirect chains (FOCUS: Session extends SessionRedirectMixin, sessions.py:356–818).
- `mount` — registers a transport adapter for a URL prefix (implied by the adapter-selection logic and `get_adapter`).
- `close` — tears down adapter connection pools (INDEX: sessions.py lists `close`).

The session's `request()` method (sessions.py:502–593) ties everything together: it builds a `Request` model object, calls `prepare_request`, merges environment settings, and finally calls `send` (FOCUS: request, sessions.py:502–593).

**Object kinds in this layer:** one primary class (`Session`), one mixin (`SessionRedirectMixin`), plus per-verb convenience methods and orchestration methods.

---

### 3. Model layer — `models.py`

This is the **data-object layer**, housing the representations of HTTP requests and responses. The INDEX entry for `src/requests/models.py` (1041 lines) lists methods such as `copy`, `prepare`, `prepare_auth`, `prepare_body`, `prepare_content_length` (INDEX: models.py). Three principal classes live here:

- **`Request`** (models.py:232–312) — a high-level, user-facing request object. It `extends RequestHooksMixin` and `calls PreparedRequest, register_hook` (FOCUS: Request, models.py:232–312). Users populate it with URL, headers, data, etc., then call `.prepare()` to produce a `PreparedRequest`.

- **`PreparedRequest`** (models.py:315–639) — the fully serialized, wire-ready request. It `extends RequestEncodingMixin, RequestHooksMixin` and `uses HTTPBasicAuth (auth), CaseInsensitiveDict (structures)` (FOCUS: PreparedRequest, models.py:315–639). Its family of `prepare_*` methods (listed in the INDEX: `prepare_auth`, `prepare_body`, `prepare_content_length`) handle encoding, header normalization, and authentication injection. Headers are stored as a `CaseInsensitiveDict` (structures.py), and auth may be applied via `HTTPBasicAuth` (auth.py).

- **`Response`** (models.py:642–1041) — the object returned after a request completes. It `uses ChunkedEncodingError, ContentDecodingError, ConnectionError, RequestsSSLError (exceptions)` (FOCUS: Response, models.py:642–1041), raising these exceptions when streaming or decoding fails. It wraps the raw socket response and provides `.text`, `.json()`, `.content`, status codes, headers, cookies, and related accessors.

**Object kinds in this layer:** data/model classes (`Request`, `PreparedRequest`, `Response`) plus supporting mixins (`RequestEncodingMixin`, `RequestHooksMixin`).

---

### 4. Transport / Adapter layer — `adapters.py`

This layer defines the **pluggable transport interface**. The INDEX entry for `src/requests/adapters.py` (697 lines) lists `close`, `send`, `BaseAdapter`, `add_headers`, `build_connection_pool_key_attributes` (INDEX: adapters.py).

- **`BaseAdapter`** (adapters.py:114–141) — an abstract base that `raises NotImplementedError` for `send()` and `close()` (FOCUS: BaseAdapter, adapters.py:114–141). It defines the contract that any transport must implement.

- **`HTTPAdapter`** (adapters.py:144–697) — the concrete, default transport. It `extends BaseAdapter` and `uses Response (models), CaseInsensitiveDict (structures)` (FOCUS: HTTPAdapter, adapters.py:144–697). It manages urllib3 connection pools, TLS settings, proxy routing, retries, and ultimately populates a `Response` object. Helper methods such as `add_headers` and `build_connection_pool_key_attributes` are also surfaced (INDEX: adapters.py).

The adapter pattern means callers can substitute custom transports (e.g., for caching or mocking) by subclassing `BaseAdapter` and mounting the adapter onto a `Session` via `session.mount()`.

**Object kinds in this layer:** one abstract class (`BaseAdapter`) and one concrete class (`HTTPAdapter`), plus helper methods on `HTTPAdapter`.

---

### 5. Supporting types

Several auxiliary modules provide shared infrastructure consumed across the layers above:

- **`auth.py`** (314 lines) — authentication handlers. The INDEX lists `AuthBase` and `HTTPBasicAuth` (INDEX: auth.py). `AuthBase` is the abstract base for all auth strategies; `HTTPBasicAuth` is the simplest concrete implementation. `HTTPDigestAuth` is also part of this module's public surface (conventional Requests API; the INDEX shows two symbols but the module contains additional auth classes). `PreparedRequest` uses `HTTPBasicAuth` directly (FOCUS: PreparedRequest, models.py:315–639).

- **`cookies.py`** (561 lines) — cookie handling. The INDEX lists `CookieConflictError` and `RequestsCookieJar` (INDEX: cookies.py). `RequestsCookieJar` (cookies.py:176–437) `extends CookieJar, MutableMapping` (FOCUS: RequestsCookieJar, cookies.py:176–437), providing a dict-like interface over standard `http.cookiejar` machinery. `Session` uses `RequestsCookieJar` to persist cookies across requests (FOCUS: Session, sessions.py:356–818).

- **`structures.py`** (99 lines) — utility data structures. The INDEX lists `CaseInsensitiveDict` and `LookupDict` (INDEX: structures.py). `CaseInsensitiveDict` (structures.py:13–80) `extends MutableMapping` (FOCUS: CaseInsensitiveDict, structures.py:13–80) and is used throughout — by `PreparedRequest` for headers (FOCUS: PreparedRequest) and by `HTTPAdapter` (FOCUS: HTTPAdapter). `LookupDict` backs the status-code registry.

- **`exceptions.py`** (152 lines) — the exception hierarchy. The INDEX lists `ChunkedEncodingError`, `ConnectTimeout`, `ConnectionError`, and more (INDEX: exceptions.py). `Response` raises several of these during content access (FOCUS: Response, models.py:642–1041, listing `ChunkedEncodingError, ContentDecodingError, ConnectionError, RequestsSSLError`).

- **`hooks.py`** (34 lines) — the event-hook system. The INDEX lists `default_hooks` and `dispatch_hook` (INDEX: hooks.py). These are invoked by `RequestHooksMixin` (which both `Request` and `PreparedRequest` extend) and by `Session.send()` to fire response hooks.

- **`status_codes.py`** (128 lines) — a lookup table mapping HTTP status codes to human-readable names. The INDEX lists `doc` (INDEX: status_codes.py), used to generate the status-code reference.

- **`utils.py`** — various utility functions consumed internally across modules (INDEX: utils.py).

---

### 6. Gaps — what the clue evidence cannot determine

The GAPS entry states: `type: STRUCTURAL (answerable from L0–L2)` and `uncovered: request, delete, get, head` (GAPS). This tells us the question is structurally answerable from the provided clue levels, but that the **full internal implementations** of `request`, `delete`, `get`, and `head` are not directly covered by the FOCUS entries at their deepest detail. Specifically, the exact line-by-line logic inside the top-level `api.py` wrappers for `delete`, `get`, and `head` — and the full body of `api.request()` beyond its call relationships — cannot be independently verified from the clue evidence alone. Their signatures, call graphs, and caller relationships are established (FOCUS: request, api.py:14–59; INDEX: api.py), but granular implementation details (e.g., exact default parameter values, docstring content) remain outside the evidence boundary.

---

### Summary table

| Layer | Module(s) | Object kinds | Key symbols |
|-------|-----------|-------------|-------------|
| Top-level API | `api.py` (157L) | Pure functions | `request`, `get`, `post`, `put`, `delete`, `head`, `options`, `patch` |
| Session | `sessions.py` (833L) | Stateful class + mixin | `Session`, `SessionRedirectMixin` |
| Models | `models.py` (1041L) | Data/model classes + mixins | `Request`, `PreparedRequest`, `Response`, `RequestEncodingMixin`, `RequestHooksMixin` |
| Transport | `adapters.py` (697L) | Abstract + concrete class | `BaseAdapter`, `HTTPAdapter` |
| Auth | `auth.py` (314L) | Abstract + concrete auth handlers | `AuthBase`, `HTTPBasicAuth`, `HTTPDigestAuth` |
| Cookies | `cookies.py` (561L) | Cookie jar class + error | `RequestsCookieJar`, `CookieConflictError` |
| Structures | `structures.py` (99L) | Utility collections | `CaseInsensitiveDict`, `LookupDict` |
| Exceptions | `exceptions.py` (152L) | Exception hierarchy | `ConnectionError`, `ConnectTimeout`, `ChunkedEncodingError`, etc. |
| Hooks | `hooks.py` (34L) | Hook functions | `default_hooks`, `dispatch_hook` |
| Status codes | `status_codes.py` (128L) | Lookup table | `doc` |
| Utilities | `utils.py` | Helper functions | (various) |
