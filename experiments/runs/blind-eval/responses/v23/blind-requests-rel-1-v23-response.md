# v2.3 Response: blind-requests-rel-1
Date: 2026-04-15

## Summary

The `Request`, `PreparedRequest`, `Session`, and `Response` classes form a linear pipeline: user-facing `Request` is transformed into `PreparedRequest`, which `Session` dispatches via `send`, ultimately producing a `Response`. Each class has a distinct role in this flow.

## Detailed Analysis

### 1. `Request` — The User-Facing Object

- `Request` (src/requests/models.py:232-312) is described as "A user-created :class:`Request <Request>` object." It extends `RequestHooksMixin` (FOCUS entry for Request).
- Its primary role is to capture user intent. It calls `PreparedRequest` and `register_hook` (FOCUS: Request, calls field), meaning its job is to produce a `PreparedRequest` and attach lifecycle hooks.
- `Request` is used by `Session` (FOCUS: Session, uses field: `Request (models)`).

### 2. `PreparedRequest` — The Fully Prepared, Mutable Object

- `PreparedRequest` (src/requests/models.py:315-639) is described as "The fully mutable :class:`PreparedRequest <PreparedRequest>` object" and extends `RequestEncodingMixin, RequestHooksMixin` (FOCUS entry for PreparedRequest).
- It is responsible for encoding and preparing all aspects of the request. It calls: `_get_idna_encoded_host`, `copy`, `prepare_auth`, `prepare_body`, `prepare_content_length`, `prepare_cookies`, `prepare_headers`, `prepare_hooks` (FOCUS: PreparedRequest, calls field).
- It is created from `Request` — its `called_by` field includes `copy, Request` (FOCUS: PreparedRequest), confirming that `Request` produces a `PreparedRequest`.
- `PreparedRequest` is also used by `Session` (FOCUS: Session, uses field: `PreparedRequest (models)`).

### 3. `Session` — The Orchestrator

- `Session` (src/requests/sessions.py:356-818) is "A Requests session" that extends `SessionRedirectMixin` (FOCUS: Session).
- It orchestrates the entire pipeline by calling: `close`, `get`, `get_adapter`, `merge_environment_settings`, `mount`, `prepare_request`, `request`, `send` (FOCUS: Session, calls field).
- **`Session.request`** (src/requests/sessions.py:502-593) "Constructs a :class:`Request <Request>`, prepares it and sends it." It calls `merge_environment_settings`, `prepare_request`, and `send` (FOCUS: request at sessions.py:502). This shows the three-step pipeline: build Request, prepare it, send it.
- **`Session.prepare_request`** (src/requests/sessions.py:459-500) "Constructs a :class:`PreparedRequest <PreparedRequest>`" — it converts the user `Request` into a `PreparedRequest`, merging session-level settings via `merge_hooks` and `merge_setting` (FOCUS: prepare_request).
- **`Session.send`** (src/requests/sessions.py:675-750) "Send a given PreparedRequest." It takes the `PreparedRequest`, selects an adapter via `get_adapter`, and handles redirects via `resolve_redirects` (FOCUS: send at sessions.py:675).

### 4. `Response` — The Result Object

- `Response` (src/requests/models.py:642-1041) is "The :class:`Response <Response>` object, which contains a..." (FOCUS: Response).
- It is produced by the adapter layer: `build_response` (src/requests/adapters.py:337-372) "Builds a :class:`Response <requests.Response>` object from a urllib3" response, using `Response (models)` (FOCUS: build_response, uses field).
- `Response` provides content access via `iter_content`, `generate`, `close`, and `raise_for_status` (FOCUS: Response, calls field).
- It can raise `StreamConsumedError`, `HTTPError`, `TypeError`, `RuntimeError` (FOCUS: Response, raises field).

### 5. The Full Pipeline Flow

1. **User calls** a convenience method like `Session.get` (src/requests/sessions.py:595) which delegates to `Session.request` (FOCUS: get, behavior: `DELEGATE(request -> result)`).
2. **`Session.request`** creates a `Request`, calls `prepare_request` to produce a `PreparedRequest`, merges environment settings, then calls `send` (FOCUS: request at sessions.py:502, calls field).
3. **`Session.send`** uses `get_adapter` to select the right transport adapter, dispatches the `PreparedRequest`, and optionally follows redirects via `resolve_redirects` (FOCUS: send at sessions.py:675, calls: `get, get_adapter, resolve_redirects`).
4. **The adapter** (e.g., `HTTPAdapter`) performs the network call and calls `build_response` to construct a `Response` (FOCUS: build_response, called_by: HTTPAdapter).
5. **`resolve_redirects`** (src/requests/sessions.py:160) handles redirect chains by receiving `Response` objects and re-issuing requests via `send` (FOCUS: resolve_redirects, calls: `close, send, get_redirect_target, rebuild_auth, rebuild_method, rebuild_proxies`).

### 6. Module-Level API

- The module-level `api.py` functions (`get`, `delete`, etc.) also delegate to a `request` function (src/requests/api.py:14) which "Constructs and sends a :class:`Request <Request>`" (SYM: request at api.py:14). These are called by `delete, get, head, options, patch, post, put` (FOCUS: request at api.py:14, called_by field).
- The `session` factory function (src/requests/sessions.py:821-833) creates `Session` instances, with behavior `DELEGATE(Session -> result)` (FOCUS: session).

### 7. Supporting Relationships

- `SessionRedirectMixin` (src/requests/sessions.py:107-353) provides redirect handling, calling `close, get, send, get_redirect_target, rebuild_auth, rebuild_method, rebuild_proxies, should_strip_auth` (FOCUS: SessionRedirectMixin). `Session` inherits from it.
- `MockRequest` (src/requests/cookies.py:23-100) wraps a `requests.Request` to interface with cookie handling (FOCUS: MockRequest, called_by: `extract_cookies_to_jar, get_cookie_header`).

## Uncertainty / Limits

- The clue file does not include the full source code, so the exact internal mechanism by which `Request.prepare()` produces a `PreparedRequest` is inferred from the `called_by` field rather than observed directly.
- The relationship between the module-level `api.request` and `Session` is not fully detailed — it is unclear from the clue file alone whether `api.request` creates a temporary `Session` internally.
- Behavior annotations cover only 27 of 80 L3 symbols (GAPS section), so some secondary interactions may be missing.
