# Scaffold (GPT-5.4): blind-requests-rel-1
Date: 2026-04-16

## Trace
The send pipeline is anchored in `Session.request`, `prepare_request`, `send`, and `build_response`, plus the model types `Request`, `PreparedRequest`, and `Response` (`request — src/requests/sessions.py:502-593`; `prepare_request — src/requests/sessions.py:459-500`; `send — src/requests/sessions.py:675-750`; `build_response — src/requests/adapters.py:337-372`; `Request` / `PreparedRequest` / `Response` — src/requests/models.py:232-1041).

## Answer
- **`Request` is the user-facing input object.** The clue explicitly calls `Request` “a user-created `Request` object,” and `Session.request` says it “constructs a `Request`, prepares it and sends it” (`Request — src/requests/models.py:232-312`; `request — src/requests/sessions.py:502-593`).
- **`PreparedRequest` is the prepared / mutable form produced from `Request`.** `PreparedRequest` is described as the “fully mutable” prepared object, `Request` calls `PreparedRequest`, and `Session.prepare_request` “constructs a `PreparedRequest` for” the incoming request (`PreparedRequest — src/requests/models.py:315-639`; `Request — src/requests/models.py:232-312`; `prepare_request — src/requests/sessions.py:459-500`).
- **`Session` orchestrates the conversion and send path.** The `Session` class uses both `Request` and `PreparedRequest`, and its methods call `prepare_request`, `request`, `send`, `get_adapter`, and redirect handling. In other words, `Session` is the coordinator that turns a user `Request` into a `PreparedRequest` and pushes it through transport / redirect logic (`Session — src/requests/sessions.py:356-818`; `prepare_request — src/requests/sessions.py:459-500`; `send — src/requests/sessions.py:675-750`; `resolve_redirects — src/requests/sessions.py:160-280`).
- **`send` operates on `PreparedRequest`, not raw `Request`.** The clue for `send` is explicit: “Send a given `PreparedRequest`,” and it calls `get_adapter` and `resolve_redirects` (`send — src/requests/sessions.py:675-750`).
- **`Response` is the output object produced downstream of send.** `build_response` in `adapters.py` “builds a `Response` object” and uses `Response (models)`, so the pipeline’s transport side turns the sent/prepared request into a `Response` instance defined in `models.py` (`build_response — src/requests/adapters.py:337-372`; `Response — src/requests/models.py:642-1041`).
- **`Response` then feeds back into session redirect handling.** `resolve_redirects` explicitly “receives a `Response`,” is called by `send`, and may loop by copying the request and calling `send` again, so `Response` is both the result of one send and the input to redirect orchestration (`resolve_redirects — src/requests/sessions.py:160-280`; `send — src/requests/sessions.py:675-750`).

## Pipeline summary
`Session.request` constructs a user-level `Request`, `Session.prepare_request` turns it into a `PreparedRequest`, `Session.send` sends that prepared object through an adapter, and adapter-side `build_response` materializes the resulting `Response`; redirects can then loop that `Response` back through `Session.resolve_redirects` and additional `send` calls (`request — src/requests/sessions.py:502-593`; `prepare_request — src/requests/sessions.py:459-500`; `send — src/requests/sessions.py:675-750`; `build_response — src/requests/adapters.py:337-372`; `resolve_redirects — src/requests/sessions.py:160-280`).

## Gaps / uncertainty
The clue does **not** expose `HTTPAdapter` itself (`GAPS` says it is uncovered), so the exact adapter-internal mechanics between `send` and `build_response` are not fully determined from the artifact alone (`build_response — src/requests/adapters.py:337-372`; `GAPS`).
