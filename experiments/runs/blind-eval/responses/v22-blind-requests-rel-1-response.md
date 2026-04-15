# v2.2 Response: blind-requests-rel-1
Date: 2026-04-15

## Question

What is the relationship between `Request`, `PreparedRequest`, `Session`, and `Response` in Requests' send pipeline?

## Answer

The clue file reveals a clear four-stage pipeline: **Request → PreparedRequest → (Session sends) → Response**. Each object plays a distinct role, and the call-graph annotations make the relationships explicit.

### 1. `Request` — The User-Facing Input

- **`Request`** (class, `src/requests/models.py:232`) — "A user-created :class:`Request <Request>` object."
- Extends `RequestHooksMixin` (`src/requests/models.py:208`).
- Calls `PreparedRequest` and `register_hook` (`src/requests/models.py:209`).
- This is the starting object that users create (or that is created on their behalf). It holds user-provided parameters but is not directly sent over the wire.

### 2. `PreparedRequest` — The Wire-Ready Representation

- **`PreparedRequest`** (class, `src/requests/models.py:315`) — "The fully mutable :class:`PreparedRequest <PreparedRequest>` object."
- Extends `RequestEncodingMixin` (`src/requests/models.py:86`) and `RequestHooksMixin`.
- Calls: `_get_idna_encoded_host`, `copy`, `prepare_auth`, `prepare_body`, `prepare_content_length`, `prepare_cookies`, `prepare_headers`, `prepare_hooks`.
- `called_by: copy, Request` — confirming that `Request` creates a `PreparedRequest`.
- Uses `HTTPBasicAuth` (auth), `InvalidJSONError` (exceptions), `CaseInsensitiveDict` (structures), `MissingSchema` (exceptions).
- Raises: `MissingSchema`, `InvalidURL`, `UnicodeError`, `NotImplementedError`.

The `Request` → `PreparedRequest` transition is a **preparation step** where the raw user input is encoded, validated, and normalized into a form ready for transmission.

### 3. `Session` — The Orchestrator

`Session` (`src/requests/sessions.py:356`) ties the pipeline together. The send pipeline within `Session` works as follows:

#### Step A: `Session.request()` creates a `Request` and prepares it

- **`Session.request`** (`src/requests/sessions.py:502`) — "Constructs a :class:`Request <Request>`, prepares it and sends it."
  - `sig: request(method, url, params, data, headers...)`
  - `calls: merge_environment_settings, prepare_request, send`
  - `uses: Request (models)` — it creates a `Request` object from caller arguments.

#### Step B: `Session.prepare_request()` converts `Request` → `PreparedRequest`

- **`prepare_request`** (`src/requests/sessions.py:459`) — "Constructs a :class:`PreparedRequest <PreparedRequest>`."
  - `calls: merge_hooks, merge_setting`
  - `uses: PreparedRequest (models), RequestsCookieJar (cookies)` — confirming it instantiates a `PreparedRequest` and merges session-level settings (headers, cookies, auth, hooks) into it.

#### Step C: `Session.send()` dispatches the `PreparedRequest`

- **`send`** (`src/requests/sessions.py:675`) — "Send a given PreparedRequest."
  - `sig: send(request)` — takes a `PreparedRequest`.
  - `behavior: BRANCH(allow_redirects -> result, else -> result)`.
  - `calls: get, get_adapter, resolve_redirects`.
  - `called_by: request, Session, resolve_redirects, SessionRedirectMixin`.

`send` uses **`get_adapter`** (`src/requests/sessions.py:783`) — "Returns the appropriate connection adapter for the given URL" — to select a transport adapter, which actually executes the network call.

#### Step D: The adapter builds a `Response`

- **`build_response`** (`src/requests/adapters.py:337`) — "Builds a :class:`Response <requests.Response>` object from a urllib3" response.
  - `uses: Response (models), CaseInsensitiveDict (structures)`.
  - `called_by: HTTPAdapter`.

The adapter's `send` method (`src/requests/adapters.py:591`) takes a `PreparedRequest` and returns a `Response` built via `build_response`.

### 4. `Response` — The Output

- **`Response`** (class, `src/requests/models.py:642`) — "The :class:`Response <Response>` object."
- Calls: `close`, `generate`, `iter_content`, `raise_for_status`.
- Raises: `StreamConsumedError`, `HTTPError`, `TypeError`, `RuntimeError`.
- Uses: `ChunkedEncodingError`, `ContentDecodingError`, `ConnectionError`, `RequestsSSLError` (all from exceptions).

The `Response` is returned to the caller and provides access to status, headers, body content (via `iter_content` at `src/requests/models.py:801`), and error checking (via `raise_for_status` at `src/requests/models.py:1001`).

### 5. Redirect Handling Feeds Back Into the Pipeline

- **`resolve_redirects`** (`src/requests/sessions.py:160`) — "Receives a Response."
  - `behavior: ACCUMULATE(loop -> hist)` — it loops, accumulating redirect history.
  - `calls: close, send, get_redirect_target, rebuild_auth, rebuild_method, rebuild_proxies`.
  - `called_by: send, Session`.
  - Raises `TooManyRedirects`.

On redirects, `resolve_redirects` calls `send` again (creating a loop: `send` → `resolve_redirects` → `send`), each time producing a new `Response`. The `SessionRedirectMixin` (`src/requests/sessions.py:107`) provides the redirect methods including `should_strip_auth` (`src/requests/sessions.py:128`).

### 6. The Top-Level API Delegates to `Session`

The module-level functions in `src/requests/api.py` serve as the entry point:

- **`request`** (`src/requests/api.py:14`) — "Constructs and sends a :class:`Request <Request>`."
  - `called_by: delete, get, head, options, patch, post, put`.

Each HTTP-verb function (e.g., `get` at `src/requests/api.py:62`, `post` at `src/requests/api.py:103`) delegates to `api.request`, which implicitly creates a `Session` (the `session` factory at `src/requests/sessions.py:821` confirms this pattern).

### Pipeline Summary

```
User calls api.get() / api.post() / etc.
  └─> api.request()  [src/requests/api.py:14]
        └─> Session.request()  [src/requests/sessions.py:502]
              ├─> creates Request  [src/requests/models.py:232]
              ├─> prepare_request() → PreparedRequest  [src/requests/sessions.py:459]
              ├─> merge_environment_settings()  [src/requests/sessions.py:752]
              └─> send(PreparedRequest)  [src/requests/sessions.py:675]
                    ├─> get_adapter(url)  [src/requests/sessions.py:783]
                    ├─> adapter.send() → builds Response  [src/requests/adapters.py:337]
                    └─> resolve_redirects() (loops back to send)  [src/requests/sessions.py:160]
                          └─> returns Response  [src/requests/models.py:642]
```
