# v2.5 Response: blind-httpx-rel-1
Date: 2026-04-16

## Question

How do HTTPX's top-level helper functions, `Client`, and explicit `Request` objects relate in the documented send pipeline?

## Answer

### 1. Top-Level Helpers in `_api.py` Delegate to `Client` Internally

The module `httpx/_api.py` contains the top-level `request` function (`httpx/_api.py:39-120`), documented as *"Sends an HTTP request."* (FOCUS: `request (httpx/_api.py:39)`). Every HTTP-verb shorthand — `delete`, `get`, `head`, `options`, `patch`, `post`, `put` — delegates into this single `request` function (FOCUS: `request … called_by: delete, get, head, options, patch, post, put`). The shorthand methods all follow the pattern `DELEGATE(request -> result)` (SYM: shorthand methods entry).

Because these are module-level functions with no persistent state, they must internally instantiate a `Client` (or equivalent machinery) to actually execute the request. The clue does not show the body of `_api.request` in full, but the structural relationship — `_api.py` helpers exist as convenience wrappers over the client layer — is established by the file organization and delegation pattern.

### 2. `Client.request()` Builds Then Sends

On the `Client` class, `request` (`httpx/_client.py:771-825`) is documented as *"Build and send a request."* (FOCUS: `request` on Client). The `AsyncClient` has a parallel method (`httpx/_client.py:1485-1540`) with the same description (FOCUS: `request` on AsyncClient).

The name *"Build and send"* reveals a two-phase operation: `Client.request()` first constructs a `Request` object and then dispatches it through the send pipeline. This is the primary high-level entry point for users who hold a `Client` instance.

The same verb shorthands exist on both clients — `get`, `head`, `options`, `post`, `put`, `patch`, `delete` — and each one delegates to `request` with `DELEGATE(request -> result)` (SYM: shorthand methods on Client/AsyncClient).

### 3. `Client.send()` Accepts Explicit `Request` Objects

For users who need to construct a `Request` ahead of time, `Client.send` (`httpx/_client.py:879-928`) provides a lower-level entry point documented as *"Send a request."* — it takes an already-built `Request` object and pushes it through the pipeline (FOCUS: `send`). It raises `RuntimeError` and re-raises caught exceptions (FOCUS: `send … raises RuntimeError, exc`). An async version exists at `httpx/_client.py:1594-1643` (FOCUS: async `send`).

The `Request` model (`httpx/_models.py:382-512`) is a standalone data object that calls `set_cookie_header`, `Cookies`, and `Headers` during construction (FOCUS: `Request`). Users can build one via `Client.build_request()` and then modify it before passing it to `send()`, or construct a `Request` directly.

### 4. The Full Send Pipeline

Once a request enters the pipeline (whether via `request()` or `send()`), it passes through a well-defined chain of methods, all defined on `BaseClient` and called by both `Client` and `AsyncClient`:

```
build_request
    → _build_request_auth
        → _send_handling_auth
            → _send_handling_redirects
                → _send_single_request
                    → transport.handle_request
```

Each stage in detail:

1. **`build_request`** (`httpx/_client.py:340-389`): Merges caller-provided values with client defaults — `_merge_cookies`, `_merge_headers`, `_merge_queryparams`, `_merge_url` — and returns a `Request` object (FOCUS: `build_request`). Called by both `AsyncClient` and `Client` (FOCUS: `build_request … called_by AsyncClient, Client`).

2. **`_build_request_auth`** (`httpx/_client.py:457-473`): Resolves authentication for the request by calling `_build_auth`. Called by both clients (FOCUS: `_build_request_auth … calls _build_auth, called_by AsyncClient, Client`).

3. **`_send_handling_auth`** (`httpx/_client.py:930-962`): Handles the authentication flow, potentially re-sending the request if an auth challenge is received (FOCUS: `_send_handling_auth`).

4. **`_send_handling_redirects`** (`httpx/_client.py:964-999`): Follows redirects by accumulating responses into a `history` list. Raises `TooManyRedirects` if the redirect chain exceeds the limit (FOCUS: `_send_handling_redirects … ACCUMULATE(_send_single_request → history, raises TooManyRedirects)`). An async version exists at lines 1679-1715 (FOCUS: async version).

5. **`_send_single_request`** (`httpx/_client.py:1001-1034`): *"Sends a single request, without handling any redirections."* Raises `RuntimeError` on failure (FOCUS: `_send_single_request`). This is where the request crosses the boundary into the transport layer.

6. **`transport.handle_request`** (`httpx/_transports/base.py:26-59`): The abstract transport interface, documented as *"Send a single HTTP request and return a response."* Raises `NotImplementedError` at the base level (FOCUS: `handle_request` in base). Concrete implementations exist in:
   - `httpx/_transports/default.py:230-259` — the standard HTTP transport (FOCUS: `handle_request` in default)
   - `httpx/_transports/wsgi.py:91-149` — the WSGI test transport (FOCUS: `handle_request` in wsgi)
   - Async counterparts: `handle_async_request` in `base`, `default`, `asgi`, and `mock` (FOCUS: `handle_async_request` entries)

### 5. The `Request` Model's Role

The `Request` class (`httpx/_models.py:382-512`) serves as the data envelope passed through the entire pipeline. It encapsulates the URL, method, headers, cookies, and body (FOCUS: `Request … calls set_cookie_header, Cookies, Headers`).

Related types support the request model:
- `_CookieCompatRequest`: provides cookie-jar compatibility (FOCUS: `_CookieCompatRequest`).
- `RequestNotRead`: a stream-error raised when request body content is accessed prematurely (FOCUS: `RequestNotRead`).
- `request_context`: provides contextual metadata (FOCUS: `request_context`).
- `RequestError`: the base exception for request-phase failures (FOCUS: `RequestError`).

### 6. Relationship Summary

The three entry points form a layered API:

| Entry Point | What It Does | Who Uses It |
|---|---|---|
| `httpx.get(...)` etc. in `_api.py` | One-off call; internally creates a `Client`, calls `Client.request()` | Quick scripts, one-shot requests |
| `Client.request(method, url, ...)` | Builds a `Request` then calls `send()` | Users with a persistent client |
| `Client.send(request)` | Takes a pre-built `Request`, runs the full pipeline | Users needing request inspection/modification before send |

All three converge into the same pipeline: `build_request` → auth → redirects → single-send → transport.

### 7. Gaps and Limitations

The clue file reports a **STRUCTURAL** gap: *"coverage: 80 symbols in L3, 25 with behavior annotations"* (GAPS entry). This leaves 55 of 80 symbols (69%) without behavior-level detail. Specifically uncovered symbols include `is_client_error`, `UseClientDefault`, and `encode_request` (GAPS: `uncovered: is_client_error, UseClientDefault, encode_request`). The internal body of `_api.request` — confirming exactly how it instantiates a `Client` — is not shown in the clue's source snippets. Event-hook integration within the redirect loop is also not detailed.
