# v2.4.1 Response: blind-requests-struct-2
Date: 2026-04-16

## The “public layers” can only be inferred from module structure, not from explicit docs text

The prompt does **not** include the prose of the API docs: `docs/conf.py` is listed only by filename and length, and there are no narrative documentation pages in the clue. So the layer split below is an inference from the code layout, not a direct quote from Requests’ docs (`docs/conf.py` in INDEX).

An evidence-based public layering is:

1. **Convenience API layer** — `src/requests/api.py`, containing the stateless verb helpers and the top-level `request()` entry point (`request`, `src/requests/api.py:14-59`; `get`, `head`, `options`, `patch`, `post`, `put`, `delete` FOCUS entries).
2. **Session/orchestration layer** — `src/requests/sessions.py`, containing `Session`, `SessionRedirectMixin`, `session()`, `prepare_request`, `send`, `merge_environment_settings`, `get_adapter`, and `mount` (`Session`, `src/requests/sessions.py:356-818`; `session`, `src/requests/sessions.py:821-833`; `prepare_request`, `src/requests/sessions.py:459-500`; `send`, `src/requests/sessions.py:675-750`).
3. **Model layer** — `src/requests/models.py`, containing `Request`, `PreparedRequest`, `Response`, and their supporting mixins (`Request`, `PreparedRequest`, `Response`, and `RequestEncodingMixin` / `RequestHooksMixin` FOCUS entries).
4. **Transport layer** — `src/requests/adapters.py`, containing `BaseAdapter`, adapter helpers, and adapter-side response construction (`BaseAdapter`, `src/requests/adapters.py:114-141`; `build_response`, `src/requests/adapters.py:337-372`).
5. **Support layers** — auth (`src/requests/auth.py`), cookies (`src/requests/cookies.py`), exceptions (`src/requests/exceptions.py`), structures (`src/requests/structures.py`), hooks (`src/requests/hooks.py`), and status-code helpers (`src/requests/status_codes.py`) (INDEX entries plus FOCUS entries such as `RequestsCookieJar`, `CaseInsensitiveDict`, and the various exception classes).

The kinds of objects in each inferred layer match that split: verb functions in `api.py`; long-lived orchestration objects in `sessions.py`; data model types in `models.py`; transport strategy objects in `adapters.py`; and focused helper/object families in auth, cookies, exceptions, and structures.

**What Cannot Be Determined**

- The exact headings or terminology used by the Requests API docs cannot be determined, because the prompt does not include those docs’ content (`docs/conf.py` is listed but not expanded).
- The public/private boundary of helper functions inside those modules is not explicit in the clue; the prompt shows symbol ownership, not a stability policy.
