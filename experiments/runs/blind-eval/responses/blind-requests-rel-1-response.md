# Response: blind-requests-rel-1
Date: 2026-04-15

## Answer
- In the send pipeline, `Session` is the coordinator. Its `request` method says it “Constructs a :class:`Request <Request>`, prepares it and sends it,” and the `Session` class itself calls `prepare_request`, `request`, and `send`. [(`request`, `src/requests/sessions.py:502-593`); (`Session`, `src/requests/sessions.py:356-818`)]
- `Request` is the initial high-level request object in that pipeline. `Session.request()` explicitly uses `Request (models)`, and the method description says it constructs a `Request` before doing anything else. [(`Session`, `src/requests/sessions.py:356-818`); (`request`, `src/requests/sessions.py:502-593`)]
- `PreparedRequest` is the transmission-ready form. `prepare_request` says it “Constructs a :class:`PreparedRequest <PreparedRequest>` for transmission,” and `PreparedRequest` is defined in `src/requests/models.py` as the “fully mutable” object. [(`prepare_request`, `src/requests/sessions.py:459-500`); (`PreparedRequest`, `src/requests/models.py:315-639`)]
- `prepare_request` is also where request-level and session-level state are combined before sending: it is called by `request`, and its description says the `PreparedRequest` has settings merged from the `Request` instance and the `Session`. [(`prepare_request`, `src/requests/sessions.py:459-500`)]
- `Session.send()` operates on the prepared form, not the original high-level one. Its signature is `send(request)`, and its description is “Send a given PreparedRequest.” [(`send`, `src/requests/sessions.py:675-750`)]
- During sending, `Session.send()` may do more than one network step because it calls `get_adapter` and `resolve_redirects`; `resolve_redirects` itself receives a `Response` and can call `send` again. [(`send`, `src/requests/sessions.py:675-750`); (`resolve_redirects`, `src/requests/sessions.py:160-280`)]
- `Response` is the output side of the same pipeline. `Response` is defined in `src/requests/models.py`, and adapter code says `build_response` “Builds a :class:`Response <requests.Response>` object” and uses `Response (models)`. [(`Response`, `src/requests/models.py:642-1041`); (`build_response`, `src/requests/adapters.py:337-372`)]
- Once produced, `Response` feeds back into session logic: `resolve_redirects` receives a `Response`, and `Response` itself exposes downstream consumption helpers like `iter_content` and `raise_for_status`. [(`resolve_redirects`, `src/requests/sessions.py:160-280`); (`Response`, `src/requests/models.py:642-1041`)]
- The coupling between the two ends of the pipeline is strong enough that request exceptions can carry both objects: `RequestException.__init__` initializes with `request` and `response` objects. [(`__init__`, `src/requests/exceptions.py:18-25`)]

## What I cannot determine
- I cannot determine the exact internal fields copied from `Request` into `PreparedRequest`, because the clue gives only the high-level `prepare_request` summary, not its full body. [(`prepare_request`, `src/requests/sessions.py:459-500`)]
- I cannot determine the exact lower-level transport steps between `Session.send()` and `build_response()` (for example, the full adapter `send` flow), because those method bodies are not included in the clue. [(`send`, `src/requests/sessions.py:675-750`); (`build_response`, `src/requests/adapters.py:337-372`)]
