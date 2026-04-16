# v2.5 Response: blind-httpx-mech-2
Date: 2026-04-16

## Question

How do timeouts and streamed response access work in HTTPX according to the public docs?

## Answer

### 1. Timeouts: `Timeout` Configuration

The `Timeout` class exists in `httpx/_config.py` at lines 72-156 (INDEX: `httpx/_config.py (248L - Limits, Proxy, Timeout)`). However, in this clue set, `Timeout` appears only in the INDEX — it is **not** included as a FOCUS entry for this task. Therefore, the following is the extent of what can be determined from the available clue data:

- `Timeout` exists and spans 84 lines of code (lines 72-156).
- It is grouped in `_config.py` alongside `Limits` and `Proxy`.
- It is consumed by clients during transport initialization.

**What cannot be determined from this clue:** The individual timeout fields (e.g., connect, read, write, pool timeouts), default values, how partial timeout overrides work, or the exact `ValueError` conditions. A separate clue with FOCUS on `Timeout` would be needed to document its internal structure.

The `elapsed` property on `Response` (`httpx/_models.py:579-589`) provides timing information: *"Returns the time taken for the complete request/response"* and raises `RuntimeError` if accessed before the response is complete (FOCUS: `elapsed`). This is the only timeout-adjacent mechanism with behavior detail in this clue.

### 2. Streamed Response Access: The `stream()` Method

Three `stream()` entry points exist, all documented as *"Alternative to httpx.request() that streams the response body"*:

- **Top-level** (`httpx/_api.py:124-171`): Module-level convenience function (FOCUS: top-level `stream`).
- **`Client.stream`** (`httpx/_client.py:828-877`): Synchronous client method (FOCUS: sync `stream`).
- **`AsyncClient.stream`** (`httpx/_client.py:1543-1592`): Asynchronous client method (FOCUS: async `stream`).

These methods return a response whose body is consumed incrementally rather than loaded into memory all at once.

### 3. Response Iteration: Sync and Async Pairs

The `Response` class (`httpx/_models.py:515-1076`) exposes a layered set of iteration methods, each with sync/async variants (FOCUS: `Response`):

#### Raw Bytes: `iter_raw` / `aiter_raw`

- **`iter_raw`** (`httpx/_models.py:935-959`): Iterates raw bytes directly from the transport. Uses an accumulation pattern: `ACCUMULATE(chunker.flush() loop)`. On completion, calls `close`. Raises `StreamConsumed`, `StreamClosed`, or `RuntimeError` (FOCUS: `iter_raw`).
- **`aiter_raw`** (`httpx/_models.py:1037-1063`): Async counterpart with the same pattern. Calls `aclose` on completion. Raises the same exceptions (FOCUS: `aiter_raw`).

#### Decoded Bytes: `iter_bytes` / `aiter_bytes`

- **`iter_bytes`** (`httpx/_models.py:884-905`): Applies content decoding (e.g., gzip decompression) on top of raw iteration. Uses a branch pattern: `BRANCH(hasattr(self, '_content') → ..., else → self._...)` — if content is already buffered, it yields from the buffer; otherwise it calls `_get_content_decoder` and delegates to `iter_raw` (FOCUS: `iter_bytes`).
- **`aiter_bytes`** (`httpx/_models.py:982-1005`): Same branch pattern, delegates to `aiter_raw` (FOCUS: `aiter_bytes`).

#### Decoded Text: `iter_text` / `aiter_text`

- **`iter_text`** (`httpx/_models.py:907-924`): Calls `iter_bytes` and decodes to text. Called by `iter_lines` for line-by-line iteration (FOCUS: `iter_text … calls iter_bytes; called_by iter_lines`).
- **`aiter_text`** (`httpx/_models.py:1007-1026`): Calls `aiter_bytes`. Called by `aiter_lines` (FOCUS: `aiter_text … calls aiter_bytes; called_by aiter_lines`).

The iteration layers form a chain:

```
iter_raw / aiter_raw       ← raw transport bytes
  → iter_bytes / aiter_bytes   ← content-decoded bytes
    → iter_text / aiter_text     ← character-decoded text
      → iter_lines / aiter_lines   ← line-split text
```

### 4. Eager Reading vs Streaming

For non-streamed access, `Response` provides:

- **`read`** (`httpx/_models.py:876-882`): *"Read and return the response content."* — eagerly consumes the entire body into memory (FOCUS: `read`).
- **`aread`** (`httpx/_models.py:974-980`): Async counterpart (FOCUS: `aread`).

If a response was obtained via `stream()` and the user accesses `.content` or `.text` without first calling `read()`, the `ResponseNotRead` exception is raised: *"Attempted to access streaming response content, without having called read()."* (FOCUS: `ResponseNotRead (httpx/_exceptions.py:338-351)`). This extends `StreamError`, which extends `RuntimeError` (not `HTTPError`).

### 5. Stream Lifecycle: Close and Cleanup

- **`close`** (`httpx/_models.py:961-972`): Called by `iter_raw` at the end of iteration. Raises `RuntimeError` (FOCUS: `close … called_by iter_raw; raises RuntimeError`).
- **`aclose`** (`httpx/_models.py:1065-1076`): Called by `aiter_raw`. Raises `RuntimeError` (FOCUS: `aclose … called_by aiter_raw; raises RuntimeError`).

Stream error types enforce proper usage:

| Exception | Meaning |
|---|---|
| `ResponseNotRead` | Accessed `.content`/`.text` on a streamed response without calling `read()` |
| `StreamConsumed` | Attempted to iterate a stream that has already been fully consumed |
| `StreamClosed` | Attempted to iterate a stream that has been closed |

(FOCUS: `ResponseNotRead`, FOCUS: `iter_raw … raises StreamConsumed, StreamClosed`, `StreamClosed (httpx/_exceptions.py:327-338)`)

`UnattachedStream` (`httpx/_content.py:92-104`) raises `StreamClosed` — it represents a stream that is not connected to any transport (FOCUS: `UnattachedStream … raises StreamClosed`).

### 6. Bound Stream Wrappers

The client layer wraps transport-level streams in bound wrappers:

- **`BoundSyncStream`** (`httpx/_client.py:139-159`): Extends `SyncByteStream`, used by `Client` (FOCUS: `BoundSyncStream`).
- **`BoundAsyncStream`** (`httpx/_client.py:162-182`): Extends `AsyncByteStream`, used by `AsyncClient` (FOCUS: `BoundAsyncStream`).

At the transport level:
- **`ResponseStream`** (`httpx/_transports/default.py:121-132`): Extends `SyncByteStream` (FOCUS: `ResponseStream`).
- **`AsyncResponseStream`** (`httpx/_transports/default.py:265-276`): Extends `AsyncByteStream` (FOCUS: `AsyncResponseStream`).

The data flow is: `ResponseStream`/`AsyncResponseStream` (transport) → `BoundSyncStream`/`BoundAsyncStream` (client wrapper) → `iter_raw`/`aiter_raw` (response iteration).

### 7. Gaps and Limitations

The clue file reports a **STRUCTURAL** gap: *"coverage: 80 symbols in L3, 16 with behavior annotations"* (GAPS entry). This leaves 64 of 80 symbols (80%) without behavior-level detail.

Critical uncovered areas include:
- **`Timeout` internals**: As noted above, the `Timeout` class is not a FOCUS entry in this clue. Its field structure, default values, per-request override mechanism, and relationship to transport-level timeouts cannot be described (GAPS: `uncovered: BaseClient, Request, multi_items, _build_request_auth`).
- **`BaseClient` construction**: How timeout, limits, and other config are wired into the client at initialization.
- **`Request` model**: Its full structure and role in streaming request bodies.
- **Content decoder details**: `_get_content_decoder` is called by `iter_bytes`/`aiter_bytes` but its behavior is not detailed.
- **Chunker logic**: The `chunker.flush()` accumulation in `iter_raw`/`aiter_raw` is mentioned but the chunker's internal behavior is not shown.
