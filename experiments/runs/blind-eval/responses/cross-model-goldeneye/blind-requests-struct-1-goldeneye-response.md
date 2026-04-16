# Cross-Model (Goldeneye): blind-requests-struct-1
Date: 2026-04-16

The public ownership splits cleanly across three main modules:

- `src/requests/api.py` owns the top-level convenience API: its `request` function “constructs and sends a Request,” and the verb helpers (`get`, `head`, `options`, `post`, `put`, `patch`, `delete`) all delegate to that API surface. [request, src/requests/api.py:14-59; get, src/requests/api.py:62-73; head, src/requests/api.py:88-100; options, src/requests/api.py:76-85; post, src/requests/api.py:103-115; put, src/requests/api.py:118-130; patch, src/requests/api.py:133-145; delete, src/requests/api.py:148-157]
- `src/requests/sessions.py` owns session orchestration: `Session` is defined there and calls `prepare_request`, `request`, `send`, `merge_environment_settings`, `mount`, `get_adapter`, and `close`, so that module coordinates setup, dispatch, adapter selection, redirects, and lifecycle. [Session, src/requests/sessions.py:356-818; request, src/requests/sessions.py:502-593; send, src/requests/sessions.py:675-750]
- `src/requests/models.py` owns the core request/response model types: `Request` is the “user-created” request object, `PreparedRequest` is the “fully mutable” prepared form, and `Response` is the returned response object. [Request, src/requests/models.py:232-312; PreparedRequest, src/requests/models.py:315-639; Response, src/requests/models.py:642-1041]
- `src/requests/adapters.py` is the transport-side bridge that constructs the public `Response` object from the lower-level response via `build_response`. [build_response, src/requests/adapters.py:337-372]
