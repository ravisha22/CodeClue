# v2.5 Response: blind-requests-rel-1
Date: 2026-04-16

## Answer

The Requests library's send pipeline is a four-object choreography—`Request`, `PreparedRequest`, `Session`, and `Response`—each with a distinct responsibility in transforming user intent into an HTTP exchange. Below is a detailed walkthrough of how they relate, cited entirely from the clue evidence.

### 1. `Request`: Capturing User Intent

`Request` (src/requests/models.py:232-312) is described as "A user-created :class:`Request <Request>` object." It extends `RequestHooksMixin` and its constructor calls `register_hook`, meaning it is the place where the caller declares *what* they want: method, URL, headers, body, auth, etc. Crucially, `Request` also calls `PreparedRequest` (FOCUS: Request calls list), establishing the first link in the pipeline: a `Request` knows how to yield a `PreparedRequest`.

`Request` is not sent directly. Instead, it serves as a declarative specification of the user's intent that the `Session` will later consume and transform.

### 2. `PreparedRequest`: The Fully Resolved, Wire-Ready Message

`PreparedRequest` (src/requests/models.py:315-639) is "The fully mutable :class:`PreparedRequest <PreparedRequest>` object." It extends both `RequestEncodingMixin` and `RequestHooksMixin`. Its preparation surface is broad: it calls `prepare_auth`, `prepare_body`, `prepare_content_length`, `prepare_cookies`, `prepare_headers`, and `prepare_hooks`—each method resolving one dimension of the outgoing HTTP message into its final form. It also calls `_get_idna_encoded_host` for internationalized domain names and `copy` for cloning itself during redirect handling.

`PreparedRequest` is called by both `copy` (self-cloning) and `Request` (FOCUS: called_by list), and it raises `MissingSchema`, `InvalidURL`, `UnicodeError`, and `NotImplementedError` when inputs are malformed. It uses `HTTPBasicAuth` for default auth, `CaseInsensitiveDict` for header storage, and `InvalidJSONError` / `MissingSchema` from the exceptions module.

The key design insight is the separation between `Request` (user-friendly, high-level) and `PreparedRequest` (low-level, fully encoded). This split lets the `Session` inject its own defaults (cookies, auth, proxy settings) *between* construction and sending.

### 3. `Session`: The Orchestrator

`Session` (src/requests/sessions.py:356-818) is described as "A Requests session." It extends `SessionRedirectMixin` and is the central coordinator of the entire pipeline. It uses both `Request` and `PreparedRequest` from models, and `RequestsCookieJar` from cookies (FOCUS: Session uses list).

The pipeline unfolds through three key methods on `Session`:

**a) `Session.request()` — Entry Point**

`Session.request()` (src/requests/sessions.py:502-593) is documented as: "Constructs a :class:`Request <Request>`, prepares it and sends it." Its calls list shows the exact sequence: it uses `Request` (from models) to build the user-intent object, then calls `prepare_request` to convert it, then calls `merge_environment_settings` to fold in environment-level configuration (proxies, certs, etc.), and finally calls `send` to dispatch the prepared request.

**b) `Session.prepare_request()` — Request → PreparedRequest Transformation**

`Session.prepare_request()` (src/requests/sessions.py:459-500) is documented as: "Constructs a :class:`PreparedRequest <PreparedRequest>` for…" It uses `PreparedRequest` (from models) and `RequestsCookieJar` (from cookies), and calls `merge_hooks` and `merge_setting` to blend per-request parameters with session-level defaults. This is where the `Session`'s persistent state (cookies, headers, auth) gets merged into the outgoing request.

**c) `Session.send()` — Dispatching the PreparedRequest**

`Session.send()` (src/requests/sessions.py:675-750) is documented as: "Send a given PreparedRequest." It calls `get_adapter` to look up the appropriate transport adapter for the request's URL scheme, then delegates actual I/O to the adapter. Its behavior annotation shows a branch: `BRANCH(allow_redirects -> self.resolve_redirect..., else -> [])`, meaning it conditionally enters redirect resolution. `send` is called by `request`, `Session`, and `resolve_redirects` (FOCUS: send called_by list), confirming that both the initial dispatch and each redirect iteration re-enter through `send`.

### 4. `Response`: The Server's Reply

`Response` (src/requests/models.py:642-1041) is the object returned to the caller. It is *not* constructed by `Session` directly; instead, the transport adapter builds it. Specifically, `build_response` (src/requests/adapters.py:337-372) is documented as: "Builds a :class:`Response <requests.Response>` object from a urllib3" response. It uses `Response` (from models) and `CaseInsensitiveDict` (from structures) to translate urllib3's low-level response into the Requests-level `Response` object.

`Response` itself calls `iter_content` for streamed reading, `raise_for_status` for HTTP-error checking, `close` for resource cleanup, and `generate` for internal iteration. It raises `StreamConsumedError`, `HTTPError`, `TypeError`, and `RuntimeError`, and uses `ChunkedEncodingError`, `ContentDecodingError`, `ConnectionError`, and `RequestsSSLError` to surface transport-layer failures.

### 5. The Transport Adapter Bridge

The adapter layer sits between `Session.send()` and the network. `Session.send()` calls `get_adapter` (FOCUS: send calls list) to resolve the correct adapter. The abstract `BaseAdapter.send()` (src/requests/adapters.py:120-137) is documented as: "Sends PreparedRequest object." The concrete `send` (src/requests/adapters.py:591-697) likewise: "Sends PreparedRequest object." After performing the I/O, the adapter calls `build_response` to wrap the urllib3 response in a `Response` object and return it up to `Session.send()`.

### 6. Redirect Handling: `resolve_redirects` and `req.copy`

When `allow_redirects` is true, `Session.send()` enters redirect resolution via `SessionRedirectMixin` (src/requests/sessions.py:107-353). The mixin calls `get_redirect_target`, `rebuild_auth`, `rebuild_method`, `rebuild_proxies`, `should_strip_auth`, and—critically—`send` again for each hop. It raises `TooManyRedirects` when the redirect chain is exhausted.

`resolve_redirects` (src/requests/sessions.py:160-280) has behavior annotated as: `ACCUMULATE(req.copy loop -> hist, raises TooManyRedirects)`. This means it loops by calling `PreparedRequest.copy()` (FOCUS: PreparedRequest calls list includes `copy`) to clone the current request, modifies it for the new target, and accumulates the intermediate responses into a history list. Each iteration re-enters `Session.send()`, which again calls `get_adapter` and the adapter's `send` / `build_response`, producing a new `Response` for each redirect.

### 7. The Public API: Thin Wrappers via `api.py`

The module-level convenience functions (`get`, `post`, `put`, `delete`, `head`, `options`, `patch`) are documented at `request` (src/requests/api.py:14-59): "Constructs and sends a :class:`Request <Request>`." The FOCUS entry confirms that `request` in api.py is called by `delete, get, head, options, patch, post, put`—each verb function is a thin wrapper.

These wrappers do not manage sessions themselves. The `session` factory function (src/requests/sessions.py:821-833) has behavior `DELEGATE(Session -> result)`, meaning it simply instantiates and returns a `Session`. The api-level `request` function creates a one-shot `Session`, calls `Session.request()`, and tears it down—giving callers the full pipeline without explicit session management.

### 8. End-to-End Pipeline Summary

Combining all evidence, the full send pipeline is:

1. **User** calls `requests.get(url)` → `api.request()` (src/requests/api.py:14-59)
2. `api.request()` creates a `Session` via `session()` (src/requests/sessions.py:821-833)
3. `Session.request()` (src/requests/sessions.py:502-593) creates a `Request` (src/requests/models.py:232-312)
4. `Session.prepare_request()` (src/requests/sessions.py:459-500) transforms it into a `PreparedRequest` (src/requests/models.py:315-639), merging session defaults
5. `Session.send()` (src/requests/sessions.py:675-750) calls `get_adapter()` and delegates to `Adapter.send()` (src/requests/adapters.py:591-697)
6. The adapter performs I/O and calls `build_response` (src/requests/adapters.py:337-372) to create a `Response` (src/requests/models.py:642-1041)
7. If redirects are enabled, `resolve_redirects` (src/requests/sessions.py:160-280) loops via `PreparedRequest.copy()`, re-entering `send()` for each hop
8. The final `Response` is returned to the caller

### 9. GAPS and Limitations

The GAPS annotation identifies this as a `RELATIONAL` gap type, answerable from L2-L3 structure. The uncovered entities are: `get_unicode_from_response`, `stream_decode_response_unicode`, `HTTPAdapter`, and `build_connection_pool_key_attributes`. Notably, `HTTPAdapter` is the concrete adapter class that would fill in details about connection pooling and retry logic between `Session.send()` and urllib3, and `build_connection_pool_key_attributes` would clarify how connection reuse is keyed. Their absence means this analysis covers the *logical* pipeline but not the full *transport-layer* mechanics. The response-decoding utilities (`get_unicode_from_response`, `stream_decode_response_unicode`) would add detail to how `Response` content is decoded, complementing the `iter_content` and streaming paths already visible in the `Response` FOCUS entry.
