# CodeClue Blind Evaluation — Requests Scoring

Total: **17 / 24**

---

### blind-requests-struct-1 (3/4)
F1: COVERED — Response identifies verb helpers (`delete`, `get`, `head`, `patch`) and `request` in `src/requests/api.py`.
F2: COVERED — Response lists `Session` with `prepare_request`, `request`, `send`, `resolve_redirects`, and `merge_environment_settings` all in `sessions.py`.
F3: COVERED — Response explicitly places `PreparedRequest`, `Response`, and `Request` (indirectly) all in `src/requests/models.py`.
F4: MISS — Response mentions `adapters.py` only in passing for `build_response`; never identifies `BaseAdapter`/`HTTPAdapter` as transport abstractions or the exception hierarchy from dedicated modules.

### blind-requests-struct-2 (3/4)
F1: COVERED — Response identifies a request-function layer (api.py), session-orchestration layer (sessions.py), transport-adapter layer, and model/object layer, demonstrating multi-layer organization.
F2: COVERED — Response identifies "public verb helpers" and `api.request()` as the top public layer, matching the convenience-function claim. Return type (`Response`) is not stated explicitly but the role is clear.
F3: COVERED — Response describes `Session` coordinating `prepare_request`, `request`, `send`, `get_adapter`, `mount`, and `close`, covering adapter registration and session-centric orchestration.
F4: MISS — Response groups `Request`, `PreparedRequest`, and `Response` together in `models.py` without noting the conceptual separation between `Request`/`Response` and the transport-ready `PreparedRequest`.

### blind-requests-rel-1 (3/4)
F1: COVERED — Response shows `Request` is "the initial high-level request object" converted to `PreparedRequest` ("the transmission-ready form") via `prepare_request`.
F2: COVERED — Response states `prepare_request` is "where request-level and session-level state are combined" and the `PreparedRequest` has "settings merged from the `Request` instance and the `Session`."
F3: COVERED — Response explicitly says "`Session.send()` operates on the prepared form, not the original high-level one" with description "Send a given PreparedRequest."
F4: MISS — Response never mentions the `response.request` attribute that back-references the `PreparedRequest`. Exception coupling is noted but not the `Response`→`PreparedRequest` link.

### blind-requests-rel-2 (3/4)
F1: COVERED — Response quotes `mount(prefix, adapter)` as "Registers a connection adapter to a prefix," directly matching prefix-based registration.
F2: MISS — Response explicitly states in "What I cannot determine" that it cannot determine the prefix-matching priority rule.
F3: COVERED — Response describes `get_adapter(url)` as returning "the appropriate connection adapter for the given URL" and identifies `BaseAdapter` as the interface.
F4: COVERED — Response identifies `HTTPAdapter` as "the built-in concrete implementation" and describes its transport role (connection management, `build_response` constructing a `Response`).

### blind-requests-mech-1 (2/4)
F1: COVERED — Response demonstrates method-level priority: `proxies.setdefault(k, v)` preserves per-call entries; cookie merge applies request cookies after session cookies; `merge_setting` called with method-level first.
F2: MISS — `None`-suppression behavior is never mentioned; response admits it cannot prove the exact conflict-resolution rule inside `merge_setting`.
F3: MISS — `Request.prepare()` as a standalone path that skips session state is never discussed; only `Session.prepare_request()` is covered.
F4: COVERED — Response shows `merge_environment_settings` is a separate call after `prepare_request`, handling `REQUESTS_CA_BUNDLE`/`CURL_CA_BUNDLE`, confirming preparation alone does not consult environment settings.

### blind-requests-mech-2 (3/4)
F1: COVERED — Response states `stream=True` "avoids reading the full body into memory" and `stream=False` returns "content as a single chunk," implying immediate download.
F2: COVERED — Response explicitly describes differing `iter_content(None)` behavior: streaming yields as-it-arrives chunks; non-streaming yields the full body as one chunk.
F3: MISS — Response explicitly says it "cannot determine the exact charset-selection behavior of `self.text`."
F4: COVERED — Response states "`JSONDecodeError` is caught and re-raised as `RequestsJSONDecodeError`" in both codec paths.
