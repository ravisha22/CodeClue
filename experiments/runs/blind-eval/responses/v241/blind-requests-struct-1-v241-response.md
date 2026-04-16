# v2.4.1 Response: blind-requests-struct-1
Date: 2026-04-16

## The public surface is centered on `api.py`, `sessions.py`, and `models.py`

The prompt points to three main public modules for the core request pipeline:

1. **Top-level request API — `src/requests/api.py`**. The INDEX shows `api.py` exporting the verb helpers, and the SYM/FOCUS entries identify `request` plus the delegating helpers `get`, `head`, `options`, `patch`, `post`, `put`, and `delete` (`src/requests/api.py` in INDEX; `request`, `src/requests/api.py:14-59`; `get`, `head`, `options`, `patch`, `post`, `put`, `delete` in FOCUS for `blind-requests-struct-2`).
2. **Session orchestration — `src/requests/sessions.py`**. `Session` lives here and `extends: SessionRedirectMixin`; it calls `prepare_request`, `request`, `send`, `merge_environment_settings`, `get_adapter`, `mount`, and `close`, which makes `sessions.py` the orchestration layer for end-to-end request execution (`Session`, `src/requests/sessions.py:356-818`).
3. **Request/response model types — `src/requests/models.py`**. The model layer contains `Request`, `PreparedRequest`, and `Response` (`Request`, `src/requests/models.py:232-312`; `PreparedRequest`, `src/requests/models.py:315-639`; `Response`, `src/requests/models.py:642-1041`).

Supporting public modules also appear in the clue: `adapters.py` owns transport adapters such as `BaseAdapter` and adapter-side `build_response`; `auth.py` owns `AuthBase` and auth implementations; `cookies.py` owns `RequestsCookieJar`; `exceptions.py` owns the exception hierarchy; and `structures.py` owns `CaseInsensitiveDict` and `LookupDict` (INDEX entries for those modules; `build_response`, `src/requests/adapters.py:337-372`; `RequestsCookieJar`, `src/requests/cookies.py:176-437`; `CaseInsensitiveDict`, `src/requests/structures.py:13-80`).

**What Cannot Be Determined**

- The prompt shows module ownership, but it does not reproduce `src/requests/__init__.py`, so the exact re-exported public API surface cannot be confirmed (`src/requests/__init__.py` in INDEX).
- The clue is truncated after “...and 16 more modules” and “...and 217 more symbols,” so additional public modules may exist beyond the ones explicitly listed (INDEX/SYM truncation markers).
