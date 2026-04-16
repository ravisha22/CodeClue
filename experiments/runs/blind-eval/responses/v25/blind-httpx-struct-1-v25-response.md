# v2.5 Response: blind-httpx-struct-1
Date: 2026-04-16

## Question

How do the HTTPX docs divide the library between one-off helper functions and client objects?

## Answer

### 1. One-Off Helper Functions in `_api.py`

The clue file shows that `httpx/_api.py` (438 lines) houses a set of top-level, module-level convenience functions: `delete`, `get`, `head`, `options`, `patch`, and others (INDEX: `httpx/_api.py (438L - delete, get, head, options, patch)`). At the center of these helpers is the `request` function (SYM: `request (httpx/_api.py:39): "Sends an HTTP request."`), which serves as the single dispatch point — every shorthand verb delegates into it (SYM: shorthand methods all have `DELEGATE(request -> result)`).

A companion top-level function, `stream`, provides an alternative entry point: `stream (httpx/_api.py:124-171): "Alternative to httpx.request() that streams the response body"`. Together, `request` and `stream` form the complete set of top-level send primitives in `_api.py`.

These functions are designed for one-off, stateless HTTP calls where no connection pooling, cookie persistence, or other session-level behavior is needed.

### 2. Client Objects: BaseClient → Client, BaseClient → AsyncClient

The client layer lives in `httpx/_client.py` (2019 lines) and is organized as a three-class hierarchy (INDEX: `httpx/_client.py (2019L)`):

- **`BaseClient`** (`httpx/_client.py:188-591`): The shared foundation. It houses merging logic for request construction — `_build_auth`, `_merge_cookies`, `_merge_headers`, `_merge_queryparams`, `_merge_url`, `_redirect_headers` (FOCUS: `BaseClient … calls _build_auth, _merge_cookies, _merge_headers, _merge_queryparams, _merge_url, _redirect_headers`). It also contains `build_request` (`httpx/_client.py:340-389`), which both `Client` and `AsyncClient` call (FOCUS: `build_request … called_by AsyncClient, Client`).

- **`Client`** (`httpx/_client.py:594-1304`): The synchronous client. Its docstring reads: *"An HTTP client, with connection pooling, HTTP/2, redirects, cookie persistence, etc."* (FOCUS: `Client`). It extends `BaseClient`, uses `BoundSyncStream` for streaming (FOCUS: `BoundSyncStream (httpx/_client.py:139-159): extends SyncByteStream, called_by Client`), and supports context-manager lifecycle via `__enter__`/`__exit__` (FOCUS: `__enter__ (httpx/_client.py:1275-1291)`).

- **`AsyncClient`** (`httpx/_client.py:1307-2019`): The asynchronous mirror. It extends `BaseClient`, uses `BoundAsyncStream` (FOCUS: `BoundAsyncStream (httpx/_client.py:162-182): extends AsyncByteStream, called_by AsyncClient`), and supports `__aenter__`/`__aexit__` (FOCUS: `__aenter__ (httpx/_client.py:1990-2006)`).

Both enter/exit guards enforce lifecycle state via the `ClientState` enum (FOCUS: `ClientState (httpx/_client.py:125-136): extends Enum, attrs: UNOPENED=1, OPENED=2, CLOSED=3`). On entry, a `GUARD(state != UNOPENED → raise RuntimeError)` check runs (FOCUS: `__aenter__` and `__enter__` entries).

A sentinel class, `UseClientDefault` (`httpx/_client.py:94-111`), bridges the two layers: *"For some parameters such as auth=... and timeout=..."* — it lets the top-level helpers defer to client-level defaults when a `Client` is used internally (FOCUS: `UseClientDefault`).

### 3. Configuration Objects: Timeout, Limits, Proxy

Separate from both the helpers and the clients, `httpx/_config.py` (248 lines) defines three configuration types (INDEX: `httpx/_config.py (248L - Limits, Proxy, Timeout)`):

- **`Timeout`** (`httpx/_config.py:72-156`): *"Timeout configuration"*; raises `ValueError` on invalid input (FOCUS: `Timeout`).
- **`Limits`** (`httpx/_config.py:159-198`): *"Configuration for limits to various client behaviors."* (FOCUS: `Limits`).
- **`Proxy`**: Listed in the INDEX alongside `Timeout` and `Limits` but not given a dedicated FOCUS entry.

These objects are injected into `Client`/`AsyncClient` at construction time and govern connection-pool sizing, per-request timeouts, and proxy routing.

### 4. Structural Division Summary

The division is a three-tier architecture:

| Layer | File(s) | Purpose |
|---|---|---|
| **One-off helpers** | `_api.py` | Stateless verb functions (`get`, `post`, `request`, `stream`) for single calls |
| **Client objects** | `_client.py` | Stateful session objects with pooling, cookies, redirects, auth |
| **Configuration** | `_config.py` | Declarative config values (`Timeout`, `Limits`, `Proxy`) consumed by clients |

Supporting modules round out the package: `_models.py` (1277 lines) holds `Request`/`Response` models, `_exceptions.py` (377 lines) holds the error hierarchy, and `_main.py` (506 lines) provides a command-line client (FOCUS: `main (httpx/_main.py:452-506): "An HTTP command line client."`) (INDEX entries for each).

The top-level helpers in `_api.py` create a temporary `Client` under the hood — they exist purely as ergonomic shortcuts. The `Client`/`AsyncClient` objects are the full-featured entry points offering connection reuse and session-level state. Both share implementation via `BaseClient`.

### 5. Gaps and Limitations

The clue file reports a **STRUCTURAL** gap: *"coverage: 75 symbols in L3, 28 with behavior annotations"* (GAPS entry). This means roughly 63% of the L3 symbols (47 of 75) lack behavior-level annotations. Specific uncovered areas likely include internal transport wiring, proxy resolution details, and the full set of `_redirect_*` helper behaviors. The `Proxy` configuration class, while listed in the INDEX, has no FOCUS entry and therefore its internal structure cannot be described from this clue data alone.
