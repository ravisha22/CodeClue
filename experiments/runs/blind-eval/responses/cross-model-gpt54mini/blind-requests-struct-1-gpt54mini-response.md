# Cross-Model (GPT-5.4-mini): blind-requests-struct-1
Date: 2026-04-16

- The top-level request API lives in `src/requests/api.py`, where `request` “constructs and sends a `Request`,” and the verb helpers (`delete`, `get`, `head`, `options`, `patch`, `post`, `put`) delegate to it. (request (src/requests/api.py:14-59); delete (src/requests/api.py:148-157); get (src/requests/api.py:62-73); head (src/requests/api.py:88-100); options (src/requests/api.py:76-85); patch (src/requests/api.py:133-145); post (src/requests/api.py:103-115); put (src/requests/api.py:118-130))
- Session orchestration lives in `src/requests/sessions.py`, where `Session` owns `request`, `prepare_request`, `send`, `get_adapter`, `merge_environment_settings`, and `mount`. (Session (src/requests/sessions.py:356-818); request (src/requests/sessions.py:502-593); prepare_request (src/requests/sessions.py:459-500); send (src/requests/sessions.py:675-750))
- The request/response model types live in `src/requests/models.py`: `Request`, `PreparedRequest`, and `Response`. (Request (src/requests/models.py:232-312); PreparedRequest (src/requests/models.py:315-639); Response (src/requests/models.py:642-1041))
