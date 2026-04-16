# v2.5 Response: blind-httpx-struct-2
Date: 2026-04-16

## Question

What public configuration and error surfaces do the HTTPX API docs expose around clients?

## Answer

### 1. Configuration Surfaces

#### Timeout

`Timeout` (`httpx/_config.py:72-156`) is described as *"Timeout configuration"* and raises `ValueError` on invalid input (FOCUS: `Timeout`). The source snippets show that `_init_transport`/`_init_proxy_transport` accept SSL, HTTP/2, and limits configuration, indicating that `Timeout` is one of several config objects threaded into transport initialization (source snippet: `_init_transport/_init_proxy_transport show SSL/HTTP2/limits config`). Beyond its existence, line range, and the `ValueError` guard, the clue does not detail `Timeout`'s individual fields.

#### Limits

`Limits` (`httpx/_config.py:159-198`) is documented as *"Configuration for limits to various client behaviors."* (FOCUS: `Limits`). It is consumed during transport initialization alongside SSL and HTTP/2 settings (source snippet reference above).

#### Proxy

`Proxy` appears in the INDEX for `_config.py` (INDEX: `httpx/_config.py (248L - Limits, Proxy, Timeout)`) but receives no dedicated FOCUS entry in this clue. Its internal structure cannot be described from the available data.

#### ClientState

`ClientState` (`httpx/_client.py:125-136`) is an `Enum` with three values: `UNOPENED=1`, `OPENED=2`, `CLOSED=3` (FOCUS: `ClientState`). It governs lifecycle guards on context-manager entry — both `__enter__` and `__aenter__` check `state != UNOPENED` and raise `RuntimeError` if violated (FOCUS: `__aenter__`, `__enter__` entries).

#### UseClientDefault

`UseClientDefault` (`httpx/_client.py:94-111`) is a sentinel used *"For some parameters such as auth=... and timeout=..."* to let call sites defer to whatever default the client instance has configured (FOCUS: `UseClientDefault`).

#### Transport Initialization

The source snippets reveal that `_init_transport` and `_init_proxy_transport` wire together SSL settings, HTTP/2 enablement, and `Limits` into the underlying transport layer (source snippet: `_init_transport/_init_proxy_transport show SSL/HTTP2/limits config`). This implies `Client`/`AsyncClient` constructors accept `ssl`, `cert`, `trust_env`, `http1`, and `http2` parameters, though the clue does not enumerate constructor signatures explicitly.

### 2. Error Hierarchy

The clue documents a detailed exception tree rooted at two independent bases (FOCUS: exception hierarchy entry):

```
HTTPError (extends Exception)
├── RequestError (extends HTTPError)
│   ├── TransportError
│   │   ├── NetworkError
│   │   │   ├── ConnectError
│   │   │   ├── CloseError
│   │   │   ├── ReadError
│   │   │   └── WriteError
│   │   └── ProtocolError
│   │       ├── LocalProtocolError
│   │       └── RemoteProtocolError
│   └── DecodingError
└── HTTPStatusError

StreamError (extends RuntimeError)
├── ResponseNotRead
├── RequestNotRead
└── StreamClosed  (implied from other clue tasks)
```

Key distinctions:

- **`RequestError`** covers problems that occur *during* the request — transport failures, network issues, protocol violations, and decoding errors (FOCUS: hierarchy).
- **`HTTPStatusError`** covers problems detected *after* a response is received — it is raised by `raise_for_status` when the response indicates an error status (FOCUS: `raise_for_status`).
- **`StreamError`** extends `RuntimeError` (not `HTTPError`) and covers misuse of the streaming API — e.g., accessing content before calling `read()` (FOCUS: `StreamError (extends RuntimeError)`).

### 3. Response Error-Checking Methods

The `Response` class (`httpx/_models.py:515-1076`) exposes several error-surface methods (FOCUS: `Response`):

- **`is_client_error`** (`httpx/_models.py:751-755`): delegates to `codes.is_client_error` — returns `True` for 4xx status codes (FOCUS: `is_client_error`).
- **`is_server_error`**: delegates to `codes.is_server_error` — returns `True` for 5xx (FOCUS: `is_server_error`).
- **`is_error`**: delegates to `codes.is_error` — covers both 4xx and 5xx (FOCUS: `is_error`).
- **`raise_for_status`** (`httpx/_models.py:794-829`): branches on `has_redirect_location`, categorizes the status code into 1xx informational, 3xx redirect, 4xx client error, or 5xx server error bands, formats an appropriate message, and raises `HTTPStatusError` (FOCUS: `raise_for_status`, source snippet: `raise_for_status checks is_success, formats message with status code, raises HTTPStatusError`).

The `Response` object itself can also raise `RuntimeError`, `ResponseNotRead`, and `ValueError` in various access paths (FOCUS: `Response … raises HTTPStatusError, RuntimeError, ResponseNotRead, ValueError`).

### 4. Stream Lifecycle

The top-level `stream()` function (`httpx/_api.py:124-171`) demonstrates the canonical stream lifecycle: it builds a request, sends it with `stream=True`, yields the response for consumption, and calls `response.close()` in a `finally` block (source snippet: `stream() builds request then sends with stream=True, yields response, finally response.close()`).

This pattern ensures that streaming connections are always cleaned up, even if the consumer raises an exception. The `ResponseNotRead` exception guards against accessing `.content` or `.text` on a streamed response that hasn't been eagerly read (FOCUS: `ResponseNotRead`).

### 5. Additional Surfaces: URL and QueryParams

The clue mentions `QueryParams` and `URL` with mutation methods: `copy_with`, `add`, `merge`, `remove`, `set`, `join` (FOCUS: `QueryParams, URL, copy_with, add, merge, remove, set, join`). These are immutable-style value objects that return modified copies, used for URL and query-string construction throughout the client.

### 6. Internal Send Pipeline (from Source Snippets)

The source snippets reveal the internal send pipeline structure:

- **`_send_handling_auth`**: runs an auth-flow loop, allowing authentication challenges to be retried (source snippet: `_send_handling_auth shows auth flow loop`).
- **`_send_handling_redirects`**: runs a redirect-following loop governed by `max_redirects`, invoking `event_hooks` at each step (source snippet: `_send_handling_redirects shows redirect loop with max_redirects and event_hooks`).
- **`_send_single_request`**: selects the appropriate transport and wraps the response body in a `BoundSyncStream` (source snippet: `_send_single_request shows transport selection and BoundSyncStream wrapping`).

### 7. Gaps and Limitations

The clue file reports a **MECHANISTIC** gap: *"coverage: 50 symbols in L3, 17 with behavior annotations"* (GAPS entry). This means 33 of 50 L3 symbols (66%) lack behavior-level detail. Notable absences include: `Proxy` internals, `Timeout` field structure, constructor parameter lists for `Client`/`AsyncClient`, `URL` internal parsing, the full `QueryParams` API, and event-hook registration details. The `has_redirect_location` property referenced by `raise_for_status` is mentioned but not given its own FOCUS entry.
