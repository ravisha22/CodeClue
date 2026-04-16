# Cross-Model (Haiku): blind-requests-struct-1
Date: 2026-04-16

## Answer

Based on the clue file, the following public modules own the three key areas:

### Top-Level Request API
**`src/requests/api.py`** owns the top-level request API. It exports the primary HTTP verb functions that delegate to the core request handler [Line 153-266: functions `delete()`, `get()`, `head()`, `options()`, `patch()`, `post()`, `put()` all reference `request()` at line 14 in `src/requests/api.py`].

### Session Orchestration  
**`src/requests/sessions.py`** owns session orchestration. It contains the `Session` class [Line 128-135: "Session (src/requests/sessions.py:356-818)" which "extends: SessionRedirectMixin" and "calls: close, get, get_adapter, merge_environment_settings, mount, prepare_request, request, send"]. The module also contains the `session()` function for context management [Line 165-168].

### Request/Response Model Types
**`src/requests/models.py`** owns the request/response model types:
- **Request** type [Line 191-195: "Request (src/requests/models.py:232-312)" described as "A user-created :class:`Request <Request>` object"]
- **PreparedRequest** type [Line 182-189: "PreparedRequest (src/requests/models.py:315-639)" described as "The fully mutable :class:`PreparedRequest <PreparedRequest>` object"]
- **Response** type [Line 197-202: "Response (src/requests/models.py:642-1041)" described as "The :class:`Response <Response>` object"]

These three modules collectively provide Requests' entire public API surface: the simple verb-based interface, session stateful management, and the core domain model objects.
