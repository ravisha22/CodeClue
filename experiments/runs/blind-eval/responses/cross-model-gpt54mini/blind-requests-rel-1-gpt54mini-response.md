# Cross-Model (GPT-5.4-mini): blind-requests-rel-1
Date: 2026-04-16

- `Request` is the user-created request object, and the top-level API/session code constructs it before sending. (Request (src/requests/models.py:232-312); request (src/requests/api.py:14-59); request (src/requests/sessions.py:502-593))
- `Session.request` “constructs a `Request`, prepares it and sends it,” so the pipeline is `Request -> PreparedRequest -> send`. (request (src/requests/sessions.py:502-593))
- `prepare_request` builds the `PreparedRequest` used by the send path. (prepare_request (src/requests/sessions.py:459-500); PreparedRequest (src/requests/models.py:315-639))
- `Session.send` accepts a `PreparedRequest`, may resolve redirects, and is the path that returns the response object. (send (src/requests/sessions.py:675-750); resolve_redirects (src/requests/sessions.py:160-280))
- `Response` is the response-side model produced/used by this flow; `build_response` builds a `Response` from the transport response. (Response (src/requests/models.py:642-1041); build_response (src/requests/adapters.py:337-372))
