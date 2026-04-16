# v2.5 Response: blind-requests-struct-1
Date: 2026-04-16

## Answer

The Requests library distributes its public surface across three principal modules, each owning a distinct architectural concern: **`api.py`** owns the top-level request API, **`sessions.py`** owns session orchestration, and **`models.py`** owns the request/response model types. The clue index confirms these are among the largest and most symbol-rich modules in the package (`=CC v2.1 requests@HEAD 36mod 757sym`).

---

### 1. `src/requests/api.py` — Top-Level Request API

This module (157 lines) provides the public convenience functions that most callers interact with. Its exported symbols include `delete`, `get`, `head`, `options`, and `patch` (INDEX: `src/requests/api.py`). Each of these is a thin wrapper that delegates to a single internal entry-point:

- **`request(method, url)`** (`src/requests/api.py:14-59`) — described as "Constructs and sends a :class:`Request <Request>`." It is the sole target to which every convenience function delegates (FOCUS: `called_by: delete, get, head, options, patch, post, put`).
- **`get`** (`src/requests/api.py:62-73`), **`head`** (`src/requests/api.py:88-100`), **`options`** (`src/requests/api.py:76-85`), **`post`** (`src/requests/api.py:103-115`), **`put`** (`src/requests/api.py:118-130`), **`patch`** (`src/requests/api.py:133-145`), and **`delete`** (`src/requests/api.py:148-157`) are all listed with behavior `DELEGATE to request` (FOCUS: API module functions).

In summary, `api.py` is the user-facing façade: callers invoke `requests.get(...)`, which calls `api.request(...)`, which in turn creates a `Session` and hands off the real work to the session layer.

---

### 2. `src/requests/sessions.py` — Session Orchestration

This is the largest of the three modules (833 lines) and owns the stateful orchestration of every HTTP transaction. Its key symbols, per the INDEX, include `close`, `delete`, `get`, `get_adapter`, and `head` (`src/requests/sessions.py`).

#### The `Session` class

- **`Session`** (`src/requests/sessions.py:356-818`) — documented as "A Requests session." It extends `SessionRedirectMixin` and is the central orchestrator. The FOCUS entry shows it `calls: close, get, get_adapter, merge_environment_settings, mount, prepare_request, request, send` and `uses: InvalidSchema (exceptions), PreparedRequest (models), RequestsCookieJar (cookies), Request (models)`. This confirms that `Session` depends on model types from `models.py` and cookie utilities from `cookies.py`.

#### Core session methods

- **`Session.request(…)`** (`src/requests/sessions.py:502-593`) — "Constructs a :class:`Request <Request>`, prepares it and sends it." It `calls: merge_environment_settings, prepare_request, send` and is `called_by: delete, get, head, options, patch, post, put, Session`. It `uses: Request (models)` — creating a `Request` model object, then delegating preparation and transport.
- **`Session.prepare_request(…)`** (`src/requests/sessions.py:459-500`) — "Constructs a :class:`PreparedRequest <PreparedRequest>` for…" It `calls: merge_hooks, merge_setting` and `uses: PreparedRequest (models), RequestsCookieJar (cookies)`. This method transforms the user-facing `Request` into a wire-ready `PreparedRequest`.
- The HTTP-verb convenience methods on `Session` mirror those in `api.py` and all delegate to `Session.request`: **`get`** (`sessions.py:595-604`), **`head`** (`sessions.py:617-626`), **`options`** (`sessions.py:606-615`), **`post`** (`sessions.py:628-639`), **`put`** (`sessions.py:641-651`), **`patch`** (`sessions.py:653-663`), **`delete`** (`sessions.py:665-673`) (FOCUS: Session methods, all `DELEGATE to request`).

#### The `session()` factory

- **`session()`** (`src/requests/sessions.py:821-833`) — "Returns a :class:`Session` for context-management." Its behavior is listed as `DELEGATE(Session -> result)`, meaning it simply instantiates and returns a `Session`.

---

### 3. `src/requests/models.py` — Request/Response Model Types

At 1,041 lines, this is the single largest module in the package and owns the data-model layer. Its INDEX symbols include `copy`, `prepare`, `prepare_auth`, `prepare_body`, and `prepare_content_length` (`src/requests/models.py`).

#### `Request`

- **`Request`** (`src/requests/models.py:232-312`) — "A user-created :class:`Request <Request>` object." It extends `RequestHooksMixin` and `calls: PreparedRequest, register_hook`. This is the high-level, user-facing request representation that callers populate before handing it to a `Session`.

#### `PreparedRequest`

- **`PreparedRequest`** (`src/requests/models.py:315-639`) — "The fully mutable :class:`PreparedRequest <PreparedRequest>` object." It extends both `RequestEncodingMixin` and `RequestHooksMixin`. This is the wire-ready form produced by `Session.prepare_request()` (`sessions.py:459-500`, FOCUS) and ultimately consumed by `Session.send()`.

#### `Response`

- **`Response`** (`src/requests/models.py:642-1041`) — "The :class:`Response <Response>` object, which contains a…" server reply. Spanning roughly 400 lines, it is the primary return type of every request cycle.

---

### 4. How They Relate: The Delegation Chain

The three modules form a clean layered architecture:

1. **`api.py` → `sessions.py`**: Every top-level convenience function in `api.py` (e.g., `get` at `api.py:62-73`) delegates to `api.request()` (`api.py:14-59`), which in turn creates a `Session` and calls `Session.request()` (`sessions.py:502-593`).
2. **`sessions.py` → `models.py`**: `Session.request()` instantiates a `Request` (`models.py:232-312`) and passes it to `Session.prepare_request()` (`sessions.py:459-500`), which builds a `PreparedRequest` (`models.py:315-639`). The prepared request is then dispatched via `Session.send()`, which returns a `Response` (`models.py:642-1041`).
3. **`sessions.py` → `adapters.py`**: Transport is handled by adapter classes. The INDEX shows `src/requests/adapters.py` (697 lines) exports `BaseAdapter`, `close`, `send`, `add_headers`, and `build_connection_pool_key_attributes` (`src/requests/adapters.py`). `Session.get_adapter()` (called by `Session`, FOCUS) selects the correct adapter, and `Session.send()` delegates to the adapter's `send()` method.

This gives the overall call-path:

```
api.get() → api.request() → Session.request() → Session.prepare_request()
                                                    → [Request → PreparedRequest]
                                                 → Session.send()
                                                    → adapter.send()
                                                    → Response
```

---

### 5. Supporting Modules

Beyond the three principal modules, the clue evidence reveals several supporting pieces:

- **`src/requests/adapters.py`** (697 lines) — owns transport adapters (`BaseAdapter`, `send`, `close`, `add_headers`, `build_connection_pool_key_attributes`) (INDEX: `src/requests/adapters.py`). The `Session` class calls `get_adapter` and `send` to route prepared requests through the appropriate adapter (FOCUS: `Session` calls list).
- **`src/requests/__init__.py`** (183 lines) — the package entry-point, exporting `check_compatibility` among other symbols (INDEX: `src/requests/__init__.py`). It wires the public API together.
- **Cookies** — `Session` and `prepare_request` both use `RequestsCookieJar` from the cookies module (FOCUS: `Session` uses `RequestsCookieJar (cookies)`; `prepare_request` uses `RequestsCookieJar (cookies)`).
- **Exceptions** — `Session` uses `InvalidSchema` from the exceptions module (FOCUS: `Session` uses `InvalidSchema (exceptions)`).

---

### Summary Table

| Concern | Module | Key Symbols | Evidence |
|---|---|---|---|
| Top-level API | `src/requests/api.py` (157L) | `request`, `get`, `head`, `options`, `post`, `put`, `patch`, `delete` | INDEX + FOCUS `api.py:14-59`, `api.py:62-157` |
| Session orchestration | `src/requests/sessions.py` (833L) | `Session`, `Session.request`, `Session.prepare_request`, `session` | INDEX + FOCUS `sessions.py:356-818`, `sessions.py:502-593`, `sessions.py:459-500`, `sessions.py:821-833` |
| Model types | `src/requests/models.py` (1041L) | `Request`, `PreparedRequest`, `Response` | INDEX + FOCUS `models.py:232-312`, `models.py:315-639`, `models.py:642-1041` |
| Transport | `src/requests/adapters.py` (697L) | `BaseAdapter`, `send`, `close` | INDEX `adapters.py` |
| Package init | `src/requests/__init__.py` (183L) | `check_compatibility` | INDEX `__init__.py` |

All claims above are grounded exclusively in the `=CC v2.1 requests@HEAD` clue set (INDEX entries, FOCUS entries, and structural GAPS notation).
