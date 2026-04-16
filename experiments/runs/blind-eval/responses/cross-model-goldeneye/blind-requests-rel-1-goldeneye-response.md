# Cross-Model (Goldeneye): blind-requests-rel-1
Date: 2026-04-16

In the send pipeline, the relationship is layered and sequential:

1. `Request` is the user-facing starting point: it is the “user-created `Request` object,” and it calls into `PreparedRequest`. [Request, src/requests/models.py:232-312]
2. `PreparedRequest` is the normalized/sendable form: it is the “fully mutable `PreparedRequest` object” and contains the preparation logic for auth, body, content length, cookies, headers, and hooks. [PreparedRequest, src/requests/models.py:315-639]
3. `Session` is the orchestrator. Its `request(...)` method “constructs a `Request`, prepares it and sends it,” and it does so by calling `merge_environment_settings`, `prepare_request`, and `send`. [request, src/requests/sessions.py:502-593]
4. `Session.prepare_request(...)` is the handoff point from `Request` to `PreparedRequest`: it explicitly “constructs a `PreparedRequest`” and uses both `PreparedRequest` and `RequestsCookieJar`. [prepare_request, src/requests/sessions.py:459-500]
5. `Session.send(...)` takes the prepared form, not the original request: it is defined as “Send a given `PreparedRequest`,” and it coordinates adapter lookup plus redirect handling. [send, src/requests/sessions.py:675-750]
6. `Response` is the result object that comes back out of that pipeline. The adapter layer’s `build_response(req, resp)` explicitly “builds a `Response` object,” and the public `Response` type then exposes content iteration, closing, and status/error helpers. [build_response, src/requests/adapters.py:337-372; Response, src/requests/models.py:642-1041]

So the flow is: `Session.request(...)` creates a `Request`, `Session.prepare_request(...)` turns it into a `PreparedRequest`, `Session.send(...)` dispatches that prepared object, and the adapter builds the resulting `Response`. [request, src/requests/sessions.py:502-593; prepare_request, src/requests/sessions.py:459-500; send, src/requests/sessions.py:675-750; build_response, src/requests/adapters.py:337-372]
