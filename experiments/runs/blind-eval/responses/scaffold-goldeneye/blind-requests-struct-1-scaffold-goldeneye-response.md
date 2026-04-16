# Scaffold (Goldeneye): blind-requests-struct-1
Date: 2026-04-16

## Relevant symbols traced
- The verb-level API lives in `src/requests/api.py`, where `request()` constructs and sends a `Request`, and helpers like `get`, `delete`, `head`, `options`, `patch`, `post`, and `put` all delegate to it. [request (src/requests/api.py:14-59); get (src/requests/api.py:62-73); delete (src/requests/api.py:148-157); post (src/requests/api.py:103-115)]
- Session coordination lives in `src/requests/sessions.py`, centered on `Session`, `session()`, `request()`, `prepare_request()`, `send()`, and `resolve_redirects()`. [Session (src/requests/sessions.py:356-818); session (src/requests/sessions.py:821-833); request (src/requests/sessions.py:502-593); prepare_request (src/requests/sessions.py:459-500); send (src/requests/sessions.py:675-750); resolve_redirects (src/requests/sessions.py:160-280)]
- The request/response model objects themselves live in `src/requests/models.py`: `Request`, `PreparedRequest`, and `Response`, plus their supporting mixins. [Request (src/requests/models.py:232-312); PreparedRequest (src/requests/models.py:315-639); Response (src/requests/models.py:642-1041); RequestHooksMixin (src/requests/models.py:208-229); RequestEncodingMixin (src/requests/models.py:86-205)]

## Answer
The public ownership split is fairly clean:

1. **Top-level request API:** `src/requests/api.py` owns the convenience entrypoints. Its `request()` function is explicitly described as constructing and sending a `Request`, and the HTTP verb helpers delegate into that API layer. [request (src/requests/api.py:14-59); get (src/requests/api.py:62-73); post (src/requests/api.py:103-115)]
2. **Session orchestration:** `src/requests/sessions.py` owns the orchestration layer. `Session` calls `prepare_request`, `request`, `send`, `get_adapter`, `merge_environment_settings`, and `mount`, which makes it the coordinating surface for configuration, preparation, transport, and redirects. [Session (src/requests/sessions.py:356-818); request (src/requests/sessions.py:502-593); prepare_request (src/requests/sessions.py:459-500); send (src/requests/sessions.py:675-750)]
3. **Request/response models:** `src/requests/models.py` owns the actual public data-model types: `Request` (user-created request), `PreparedRequest` (fully mutable prepared form), and `Response` (returned result). [Request (src/requests/models.py:232-312); PreparedRequest (src/requests/models.py:315-639); Response (src/requests/models.py:642-1041)]
4. **Transport boundary:** `src/requests/adapters.py` contributes the lower-level handoff by `build_response()`, which constructs a `Response` object from the transport layer, but the model type still belongs to `models.py`. [build_response (src/requests/adapters.py:337-372); Response (src/requests/models.py:642-1041)]

## Gaps / uncertainty
The clue is sufficient to identify module ownership, but not every low-level transport detail; the GAPS section explicitly leaves some adapter internals uncovered. [GAPS]
