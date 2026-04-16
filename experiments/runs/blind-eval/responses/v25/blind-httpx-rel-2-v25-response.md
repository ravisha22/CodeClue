# v2.5 Response: blind-httpx-rel-2
Date: 2026-04-16

## Question

How do HTTPX's synchronous and asynchronous clients line up for lifecycle management and streaming responses?

## Answer

### 1. Parallel Structure: Client ↔ AsyncClient, Both Extend BaseClient

The clue establishes a clean three-class hierarchy in `httpx/_client.py`:

- **`BaseClient`** (`httpx/_client.py:188-591`): The shared abstract base that both clients extend. It houses all the merging, redirect, and auth-building logic — `build_request`, `_build_redirect_request`, `_build_request_auth`, `_get_proxy_map`, `_set_timeout` — each of which is documented as `called_by AsyncClient, Client` (FOCUS: `build_request … called_by AsyncClient, Client`; FOCUS entries for `_build_redirect_request`, `_build_request_auth`, `_get_proxy_map`, `_set_timeout`).

- **`Client`** (`httpx/_client.py:594-1304`): The synchronous client. Extends `BaseClient`, uses `BoundSyncStream`, and supports `__enter__`/`__exit__` (FOCUS: `Client … extends BaseClient, calls __enter__, __exit__, BoundSyncStream`).

- **`AsyncClient`** (`httpx/_client.py:1307-2019`): The asynchronous client. Extends `BaseClient`, uses `BoundAsyncStream`, and supports `__aenter__`/`__aexit__` (FOCUS: `AsyncClient … extends BaseClient, calls __aenter__, __aexit__, BoundAsyncStream`).

The two clients mirror each other method-for-method: the same request-building, auth-handling, redirect-following, and single-send pipeline exists in both, with the async version using `await` and async iterators.

### 2. Lifecycle Management: Context Managers and ClientState

#### ClientState Enum

`ClientState` (`httpx/_client.py:125-136`) defines three states as an `Enum`: `UNOPENED=1`, `OPENED=2`, `CLOSED=3` (FOCUS: `ClientState`). This enum governs the lifecycle transitions enforced by the context-manager protocol.

#### Synchronous Lifecycle

`Client.__enter__` (`httpx/_client.py:1275-1291`) runs a guard: `GUARD(state != UNOPENED → raise RuntimeError)` (FOCUS: `__enter__`). This ensures a client can only be entered once from the `UNOPENED` state. The corresponding `__exit__` handles teardown.

#### Asynchronous Lifecycle

`AsyncClient.__aenter__` (`httpx/_client.py:1990-2006`) enforces the identical guard: `GUARD(state != UNOPENED → raise RuntimeError)`, then accumulates (opens) all mounted transports via `ACCUMULATE(self._mounts.values())` (FOCUS: `__aenter__`). The corresponding `__aexit__` (`httpx/_client.py:2008-2019`) similarly accumulates over mounts to close them (FOCUS: `__aexit__`).

The lifecycle pattern is symmetric:

| Operation | Client (sync) | AsyncClient (async) |
|---|---|---|
| Enter | `__enter__` | `__aenter__` |
| Exit | `__exit__` | `__aexit__` |
| State guard | `state != UNOPENED → RuntimeError` | `state != UNOPENED → RuntimeError` |
| Transport init | Opens `_mounts` | Opens `_mounts` |

### 3. Streaming Responses: BoundSyncStream vs BoundAsyncStream

#### Bound Stream Wrappers

The client layer wraps raw transport streams in bound wrappers that tie the stream lifecycle to the client:

- **`BoundSyncStream`** (`httpx/_client.py:139-159`): Extends `SyncByteStream`, called by `Client` (FOCUS: `BoundSyncStream`).
- **`BoundAsyncStream`** (`httpx/_client.py:162-182`): Extends `AsyncByteStream`, called by `AsyncClient` (FOCUS: `BoundAsyncStream`).

These wrappers ensure that when a stream is consumed or closed, the underlying transport connection is properly managed within the client's lifecycle.

#### Stream Iteration Methods

The `Response` model exposes paired sync/async iteration methods (SYM entries):

| Sync | Async | Purpose |
|---|---|---|
| `iter_bytes` | `aiter_bytes` | Decoded bytes |
| `iter_text` | `aiter_text` | Decoded text |
| `iter_raw` | `aiter_raw` | Raw bytes from transport |
| `iter_lines` | `aiter_lines` | Line-by-line text (implied by iter_text chain) |
| `close` | `aclose` | Cleanup |

These methods mirror each other exactly, with the async variants using `async for` and `await`.

#### The `stream()` Method

Both clients expose a `stream()` method that provides an alternative to `request()` for streamed consumption:

- **`Client.stream`** (`httpx/_client.py:828-877`): *"Alternative to httpx.request() that streams the response body"* (FOCUS: sync `stream`).
- **`AsyncClient.stream`** (`httpx/_client.py:1543-1592`): The async counterpart (FOCUS: async `stream`).
- **Top-level `stream`** (`httpx/_api.py:124-171`): A module-level convenience version (FOCUS: top-level `stream`).

#### Stream Error Types

Misuse of the streaming API raises specific exceptions:
- `ResponseNotRead`: Raised when accessing content on a streamed response without calling `read()` first (FOCUS: `ResponseNotRead extends StreamError`).
- `RequestNotRead`: The request-body counterpart (FOCUS: `RequestNotRead extends StreamError`).
- Both extend `StreamError`, which itself extends `RuntimeError` (not `HTTPError`).

### 4. Transport Layer: ResponseStream vs AsyncResponseStream

At the transport level, the same sync/async split continues:

- **`ResponseStream`** (`httpx/_transports/default.py:121-132`): Extends `SyncByteStream`. Called by `handle_request` and `HTTPTransport` (FOCUS: `ResponseStream`).
- **`AsyncResponseStream`** (`httpx/_transports/default.py:265-276`): Extends `AsyncByteStream`. Called by `handle_async_request` and `AsyncHTTPTransport` (FOCUS: `AsyncResponseStream`).
- **`ASGIResponseStream`** (`httpx/_transports/asgi.py:55-60`): Extends `AsyncByteStream` — specific to the ASGI test transport (FOCUS: `ASGIResponseStream`).

The data flow for streaming is:

```
Transport (ResponseStream / AsyncResponseStream)
  → Client wrapper (BoundSyncStream / BoundAsyncStream)
    → Response iteration (iter_bytes / aiter_bytes, etc.)
```

#### MultipartStream

`MultipartStream` extends both `SyncByteStream` and `AsyncByteStream` (FOCUS: `MultipartStream extends SyncByteStream, AsyncByteStream`), allowing multipart request bodies to be used with either client type.

### 5. CLI Integration

The command-line client in `_main.py` uses `download_response` (`httpx/_main.py:251-270`) for streaming downloads, called by the `main` entry point (FOCUS: `download_response … called_by main`). This provides a concrete usage example of the streaming infrastructure outside the programmatic API.

### 6. Gaps and Limitations

The clue file reports a **STRUCTURAL** gap: *"coverage: 78 symbols in L3, 21 with behavior annotations"* (GAPS entry). This leaves 57 of 78 symbols (73%) without behavior-level detail. Key areas not fully covered include:

- The internal body of `BoundSyncStream` and `BoundAsyncStream` — the clue shows their class signatures and inheritance but not their iteration/close logic.
- How `Client.__exit__` and `AsyncClient.__aexit__` transition `ClientState` from `OPENED` to `CLOSED` — only `__aexit__`'s accumulate-over-mounts behavior is shown.
- The full set of constructor parameters for `Client`/`AsyncClient`.
- Transport mount registration and selection logic.
