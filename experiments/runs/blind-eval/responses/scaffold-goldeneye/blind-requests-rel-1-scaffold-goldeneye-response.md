# Scaffold (Goldeneye): blind-requests-rel-1
Date: 2026-04-16

## Traced pipeline
- `Request` is the user-created object. [Request (src/requests/models.py:232-312)]
- `Session.request()` constructs that `Request`, prepares it, and sends it. [request (src/requests/sessions.py:502-593)]
- `prepare_request()` turns it into a `PreparedRequest`. [prepare_request (src/requests/sessions.py:459-500); PreparedRequest (src/requests/models.py:315-639)]
- `send()` accepts a `PreparedRequest` and drives adapter selection and redirects. [send (src/requests/sessions.py:675-750); Session (src/requests/sessions.py:356-818)]
- `build_response()` constructs the final `Response`. [build_response (src/requests/adapters.py:337-372); Response (src/requests/models.py:642-1041)]

## Answer
The relationship is a staged pipeline:

1. **`Request` is the user-facing input object.** The clue explicitly describes `Request` as “a user-created `Request` object.” [Request (src/requests/models.py:232-312)]
2. **`Session` is the orchestrator.** A `Session` uses `request`, `prepare_request`, `send`, `get_adapter`, and `merge_environment_settings`, so it is the component that coordinates the send pipeline. [Session (src/requests/sessions.py:356-818)]
3. **`Session.request()` builds and advances the pipeline.** Its description says it “constructs a `Request`, prepares it and sends it,” and it calls `merge_environment_settings`, `prepare_request`, and `send`. [request (src/requests/sessions.py:502-593)]
4. **`PreparedRequest` is the normalized outbound form.** `prepare_request()` constructs a `PreparedRequest`, and the `PreparedRequest` type itself owns preparation steps such as auth, body, cookies, headers, hooks, and content length. [prepare_request (src/requests/sessions.py:459-500); PreparedRequest (src/requests/models.py:315-639)]
5. **`send()` operates on the prepared form and manages follow-on behavior.** It is explicitly defined as “Send a given `PreparedRequest`,” and it can call `get_adapter` and `resolve_redirects`. [send (src/requests/sessions.py:675-750)]
6. **`Response` is the result object produced at the transport boundary.** `build_response()` “builds a `Response` object from a urllib3” response, and `Response` is the returned container that exposes streaming, content, closing, and status behavior. [build_response (src/requests/adapters.py:337-372); Response (src/requests/models.py:642-1041)]
7. **Redirect handling loops the pipeline back through `Session`.** `resolve_redirects()` receives a `Response`, copies the request, and can call `send` again, so `Response` can feed another prepared send cycle. [resolve_redirects (src/requests/sessions.py:160-280); SessionRedirectMixin (src/requests/sessions.py:107-353)]

## Gaps / uncertainty
The clue establishes the relationships clearly, but lower-level adapter I/O details remain partially uncovered. [GAPS]
