# Cross-Model (Haiku): blind-requests-rel-1
Date: 2026-04-16

## Answer

The relationship between `Request`, `PreparedRequest`, `Session`, and `Response` forms Requests' complete send pipeline:

### Pipeline Flow & Responsibilities

**`Request` → `PreparedRequest`**: User-created Request objects are transformed into PreparedRequest objects. [Line 191-195: "Request (src/requests/models.py:232-312)" is "A user-created :class:`Request <Request>` object" and "calls: PreparedRequest, register_hook". Line 182-189: "PreparedRequest (src/requests/models.py:315-639)" is "The fully mutable :class:`PreparedRequest <PreparedRequest>` object" that "calls: _get_idna_encoded_host, copy, prepare_auth, prepare_body, prepare_content_length, prepare_cookies, prepare_headers, prepare_hooks".]

**`Session` orchestrates the pipeline**: The Session class manages the entire request-send-response cycle. [Line 128-135: "Session (src/requests/sessions.py:356-818)" "extends: SessionRedirectMixin" and "calls: close, get, get_adapter, merge_environment_settings, mount, prepare_request, request, send" and "uses: InvalidSchema (exceptions), PreparedRequest (models), RequestsCookieJar (cookies), Request (models)".]

**Core Pipeline Operations**:
- `prepare_request()` transforms Request → PreparedRequest [Line 158-163: "prepare_request (src/requests/sessions.py:459-500)" "calls: merge_hooks, merge_setting" and "uses: PreparedRequest (models), RequestsCookieJar (cookies)"].
- `request()` orchestrates preparation and sending [Line 170-175: "request (src/requests/sessions.py:502-593)" "calls: merge_environment_settings, prepare_request, send" and "uses: Request (models)"].
- `send()` dispatches the PreparedRequest and handles redirect logic [Line 137-143: "send (src/requests/sessions.py:675-750)" "Send a given PreparedRequest" "calls: get, get_adapter, resolve_redirects" "calls: resolve_redirects"].

**`Response` is the pipeline output**: The Response object is built from urllib3 responses [Line 197-202: "Response (src/requests/models.py:642-1041)" "calls: close, generate, iter_content, raise_for_status" "raises: StreamConsumedError, HTTPError, TypeError, RuntimeError"]. The adapter's `build_response()` creates Response objects [Line 120-126: "build_response (src/requests/adapters.py:337-372)" "sig: build_response(req, resp)" "uses: Response (models), CaseInsensitiveDict (structures)"].

### Redirect Handling
The `resolve_redirects()` method [Line 324-331: "resolve_redirects (src/requests/sessions.py:160-280)" "Receives a Response" "calls: close, send, get_redirect_target, rebuild_auth, rebuild_method, rebuild_proxies" "raises: TooManyRedirects" "uses: TooManyRedirects (exceptions)"] integrates Request/PreparedRequest/Response objects to transparently handle HTTP redirects by building new PreparedRequest objects from redirect responses.

This forms a cycle: Request → PreparedRequest → send() → Response → (optionally) new PreparedRequest for redirects.
