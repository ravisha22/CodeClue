# Cross-Model (Sonnet): blind-requests-struct-1
Date: 2026-04-16

Based on the clue file, I can identify three main public modules that own Requests' key functionality:

## Top-Level Request API
**Module: `src/requests/api.py` (157L)**

This module owns the top-level request functions that form the public API:
- `request` (src/requests/api.py:14): "Constructs and sends a :class:`Request <Request>`" - the core request function
- `delete`, `get`, `head`, `options`, `patch`, `post`, `put` (src/requests/api.py): All HTTP method functions that delegate to the main `request` function

Evidence from FOCUS section shows these are all delegates:
- `delete` (src/requests/api.py:148-157): "behavior: DELEGATE(request -> result)"
- `get` (src/requests/api.py:62-73): "behavior: DELEGATE(request -> result)"
- `head` (src/requests/api.py:88-100): "behavior: DELEGATE(request -> result)"
- `options` (src/requests/api.py:76-85): "behavior: DELEGATE(request -> result)"
- `patch` (src/requests/api.py:133-145): "behavior: DELEGATE(request -> result)"
- `post` (src/requests/api.py:103-115): "behavior: DELEGATE(request -> result)"
- `put` (src/requests/api.py:118-130): "behavior: DELEGATE(request -> result)"

## Session Orchestration
**Module: `src/requests/sessions.py` (833L)**

This module owns session management and orchestration:
- `Session` class (src/requests/sessions.py:356): "A Requests session" - the main session class
- `session` function (src/requests/sessions.py:821-833): "Returns a :class:`Session` for context-management" 
- Session-level request methods that mirror the API module
- Key orchestration functions:
  - `request` (src/requests/sessions.py:502): "Constructs a :class:`Request <Request>`, prepares it and sends it"
  - `prepare_request` (src/requests/sessions.py:459): "Constructs a :class:`PreparedRequest <PreparedRequest>` for"
  - `send` (src/requests/sessions.py:675): "Send a given PreparedRequest"
  - `merge_environment_settings` and other session management functions

The FOCUS section shows Session "uses: InvalidSchema (exceptions), PreparedRequest (models), RequestsCookieJar (cookies), Request (models)" confirming it orchestrates between different components.

## Request/Response Model Types
**Module: `src/requests/models.py` (1041L)**

This module owns the core data types:
- `Request` class (src/requests/models.py:232-312): "A user-created :class:`Request <Request>` object"
- `PreparedRequest` class (src/requests/models.py:315-639): "The fully mutable :class:`PreparedRequest <PreparedRequest>` object"
- `Response` class (src/requests/models.py:642-1041): "The :class:`Response <Response>` object, which contains a"

Evidence from FOCUS section shows these are the core model types:
- Request "calls: PreparedRequest, register_hook"
- PreparedRequest "extends: RequestEncodingMixin, RequestHooksMixin" with many prepare methods
- Response includes methods like "close, generate, iter_content, raise_for_status"

The INDEX confirms this module's size (1041L) and importance with symbols like "copy, prepare, prepare_auth, prepare_body, prepare_content_length".

These three modules form the core public interface: `api.py` provides the simple function-based API, `sessions.py` handles stateful session management and request orchestration, and `models.py` defines the fundamental data types that flow through the system.