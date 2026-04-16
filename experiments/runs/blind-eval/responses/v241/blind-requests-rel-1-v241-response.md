# v2.4.1 Response: blind-requests-rel-1
Date: 2026-04-16

## `Session` turns a `Request` into a `PreparedRequest`, sends it, and returns a `Response`

The send pipeline in the prompt is:

1. **`Session.request(...)` is the orchestration entry point.** It is described as “Constructs a `Request <Request>`, prepares it and sends it,” and it calls `merge_environment_settings`, `prepare_request`, and `send` (`request`, `src/requests/sessions.py:502-593`).
2. **`Request` is the user-facing input object.** The clue describes it as “A user-created `Request` object” that `extends: RequestHooksMixin` (`Request`, `src/requests/models.py:232-312`).
3. **`prepare_request` builds a `PreparedRequest`.** The FOCUS entry says it “Constructs a `PreparedRequest <PreparedRequest>` for transmission” and calls `merge_hooks` and `merge_setting`; `Session` also explicitly `uses: PreparedRequest (models)` (`prepare_request`, `src/requests/sessions.py:459-500`; `Session`, `src/requests/sessions.py:356-818`).
4. **`PreparedRequest` is the wire-ready request object.** It is “The fully mutable `PreparedRequest` object” and performs preparation work such as `prepare_auth`, `prepare_body`, `prepare_content_length`, `prepare_cookies`, `prepare_headers`, and `prepare_hooks` (`PreparedRequest`, `src/requests/models.py:315-639`).
5. **`Session.send` dispatches that prepared request through a transport adapter.** `send` is “Send a given PreparedRequest,” it calls `get_adapter`, and it may branch into `resolve_redirects` (`send`, `src/requests/sessions.py:675-750`).
6. **The adapter builds the final `Response`.** `build_response` “Builds a `Response <requests.Response>` object from a urllib3 response” and `uses: Response (models)` (`build_response`, `src/requests/adapters.py:337-372`).
7. **`Response` is the final result type.** It provides streaming/status helpers such as `iter_content`, `generate`, `raise_for_status`, and `close` (`Response`, `src/requests/models.py:642-1041`).

So the confirmed relationship is: **`Request` is the raw user object, `PreparedRequest` is the normalized/transmittable form, `Session` is the orchestrator that performs the transformation and chooses transport, and `Response` is the adapter-built result** (`Request`, `PreparedRequest`, `Session`, `Response`, and `build_response` FOCUS entries above).

**What Cannot Be Determined**

- The exact body of `api.py`’s top-level `request()` is not shown, so whether it always creates a fresh `Session` is not confirmed from this prompt.
- The prompt shows that `resolve_redirects` accumulates redirect history, but it does not expose the exact re-preparation steps for redirected requests (`resolve_redirects`, `src/requests/sessions.py:160-280`).
