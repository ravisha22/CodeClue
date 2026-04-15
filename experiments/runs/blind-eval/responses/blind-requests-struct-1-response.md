# Response: blind-requests-struct-1
Date: 2026-04-15

## Answer
- The top-level request API is owned by `src/requests/api.py`. The module index lists public verb helpers there (`delete`, `get`, `head`, `options`, `patch`), and `request` in that module is described as the function that “Constructs and sends a :class:`Request <Request>`,” with the verb helpers calling it. [(`request`, `src/requests/api.py:14-59`); (INDEX, `src/requests/api.py`)]
- Session orchestration is owned by `src/requests/sessions.py`. The `Session` class lives there and calls `prepare_request`, `request`, `send`, `merge_environment_settings`, `get_adapter`, `mount`, and `close`, which makes that module the orchestration hub. [(`Session`, `src/requests/sessions.py:356-818`)]
- The same `sessions.py` module also contains the orchestration methods that move a request through the pipeline: `request` “Constructs a :class:`Request <Request>`, prepares it and sends it,” `send` “Send[s] a given PreparedRequest,” and `resolve_redirects` operates on a `Response`. [(`request`, `src/requests/sessions.py:502-593`); (`send`, `src/requests/sessions.py:675-750`); (`resolve_redirects`, `src/requests/sessions.py:160-280`)]
- The request/response model types are owned by `src/requests/models.py`. `PreparedRequest` is defined there, `Response` is defined there, and `Session` explicitly uses both `PreparedRequest (models)` and `Request (models)`. [(`PreparedRequest`, `src/requests/models.py:315-639`); (`Response`, `src/requests/models.py:642-1041`); (`Session`, `src/requests/sessions.py:356-818`)]
- `Response` being part of the model layer is also reinforced by adapter code: `build_response` in `adapters.py` says it builds a `Response` and explicitly uses `Response (models)`. [(`build_response`, `src/requests/adapters.py:337-372`)]

## What I cannot determine
- I cannot determine the exact package-root re-export surface from the clue file, because `src/requests/__init__.py` is listed in the index but its exported names are not shown. [(INDEX, `src/requests/__init__.py`)]
- I cannot quote a direct `Request` class definition from the clue file, because there is no focused `Request` class entry; I can only place `Request` in `models.py` indirectly through `Session uses: Request (models)` and the `request` method descriptions. [(`Session`, `src/requests/sessions.py:356-818`); (`request`, `src/requests/sessions.py:502-593`)]
