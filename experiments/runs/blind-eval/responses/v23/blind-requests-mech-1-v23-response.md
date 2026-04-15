# v2.3 Response: blind-requests-mech-1
Date: 2026-04-15

## Summary

The Requests library uses a layered merging strategy where per-call options, session-level defaults, and environment-derived settings are combined through dedicated functions: `merge_setting`, `merge_hooks`, `merge_environment_settings`, and `prepare_request`. The general precedence is: per-call options override session defaults, and environment settings are merged in afterward — but the specifics depend on each setting type.

## Detailed Analysis

### 1. `merge_setting` — The Core Merging Primitive

- `merge_setting` (src/requests/sessions.py:62-89) "Determines appropriate setting for a given request, taking into account" (with truncated description) (FOCUS: merge_setting).
- Signature: `merge_setting(request_setting, session_setting, dict_class)` (FOCUS: merge_setting, sig field).
- Behavior: `ACCUMULATE(loop -> result)` (FOCUS: merge_setting, behavior field) — it iterates and accumulates merged values.
- It is called by: `merge_environment_settings`, `prepare_request`, `Session`, and `merge_hooks` (FOCUS: merge_setting, called_by field). This makes it the foundational merging primitive used throughout the pipeline.
- The parameter ordering (`request_setting` first, `session_setting` second) strongly implies that per-call (request-level) settings take precedence over session defaults, since the function name says it "determines appropriate setting" — the request-level value would typically override when present.

### 2. `merge_hooks` — Hook-Specific Merging

- `merge_hooks` (src/requests/sessions.py:92-104) "Properly merges both requests and session hooks" (FOCUS: merge_hooks).
- Signature: `merge_hooks(request_hooks, session_hooks, dict_class)` (FOCUS: merge_hooks, sig field).
- It internally calls `get` and `merge_setting` (FOCUS: merge_hooks, calls field), so hook merging reuses the same core `merge_setting` logic.
- Called by `prepare_request` and `Session` (FOCUS: merge_hooks, called_by field).

### 3. `prepare_request` — Merging During Request Preparation

- `prepare_request` (src/requests/sessions.py:459-500) "Constructs a :class:`PreparedRequest <PreparedRequest>`" (FOCUS: prepare_request).
- It calls `merge_hooks` and `merge_setting` (FOCUS: prepare_request, calls field), meaning that during preparation, both hooks and regular settings (headers, auth, etc.) are merged between the per-call request and the session defaults.
- Called by `request` and `Session` (FOCUS: prepare_request, called_by field).
- Uses `PreparedRequest (models)` and `RequestsCookieJar (cookies)` (FOCUS: prepare_request, uses field), indicating cookie merging also occurs here.

### 4. `merge_environment_settings` — Environment Integration

- `merge_environment_settings` (src/requests/sessions.py:752-781) "Check the environment and merge it with some settings" (FOCUS: merge_environment_settings).
- Signature: `merge_environment_settings(url, proxies, stream, verify, cert)` (FOCUS: merge_environment_settings, sig field).
- It calls `get` and `merge_setting` (FOCUS: merge_environment_settings, calls field), applying the same `merge_setting` primitive to blend environment variables with existing settings.
- Called by `request` and `Session` (FOCUS: merge_environment_settings, called_by field).

### 5. The Ordering in `Session.request`

- `Session.request` (src/requests/sessions.py:502-593) "Constructs a :class:`Request <Request>`, prepares it and sends it" (FOCUS: request at sessions.py:502).
- It calls, in order: `merge_environment_settings`, `prepare_request`, `send` (FOCUS: request at sessions.py:502, calls field).
- This reveals the sequencing:
  1. **`prepare_request`** is called to merge per-call options with session defaults (headers, auth, hooks, cookies).
  2. **`merge_environment_settings`** is called to incorporate environment-derived settings (proxies, verify, cert, stream) with the already-merged values.
  3. **`send`** dispatches the fully-merged `PreparedRequest`.

### 6. Environment-Specific Helpers

- `get_environ_proxies` (src/requests/utils.py:813-822) "Return a dict of environment proxies" with behavior `BRANCH(should_bypass_proxies -> empty, else -> getproxies)` (FOCUS: get_environ_proxies). It checks whether proxies should be bypassed before returning environment proxies.
- `should_bypass_proxies` (src/requests/utils.py:752) "Returns whether we should bypass proxies or not" (SYM: should_bypass_proxies).
- `get_netrc_auth` (src/requests/utils.py:206-247) "Returns the Requests tuple auth for a given url from netrc" with behavior `BRANCH(netrc_file -> result, else -> result)` (FOCUS: get_netrc_auth) — environment auth from `.netrc` files.
- `set_environ` (src/requests/utils.py:731-749) "Set the environment variable 'env_name' to 'value'" (FOCUS: set_environ), used by proxy bypass checks.

### 7. Session-Level Defaults

- `Session` (src/requests/sessions.py:356-818) itself stores defaults and calls all the merging functions: `close, get, get_adapter, merge_environment_settings, mount, prepare_request, request, send` (FOCUS: Session, calls field).
- The session imports `adapters, auth, compat, cookies, exceptions` (FOCUS: Session, imports field) and uses `PreparedRequest`, `RequestsCookieJar`, `Request` (FOCUS: Session, uses field).

### 8. Adapter-Level Settings

- `HTTPAdapter` (src/requests/adapters.py:144-697) also has its own settings scope. It calls `build_connection_pool_key_attributes`, `cert_verify`, `get_connection_with_tls_context`, etc. (FOCUS: HTTPAdapter, calls field).
- `_urllib3_request_context` (src/requests/adapters.py:77-111) is called by `build_connection_pool_key_attributes` and `HTTPAdapter` (FOCUS: _urllib3_request_context), providing low-level per-connection settings.

## Inferred Precedence Rules

Based on the merge function signatures and call ordering:

1. **Per-call request options** (passed to `session.get(url, headers=...)`) are the `request_setting` parameter to `merge_setting` and take highest precedence.
2. **Session-level defaults** (set on `session.headers`, `session.auth`, etc.) are the `session_setting` parameter and serve as fallbacks.
3. **Environment settings** (proxies from env vars, auth from `.netrc`, CA bundles from env) are merged in via `merge_environment_settings`, which also uses `merge_setting` — likely filling in values not already set by the above two layers.
4. **Hooks** follow the same pattern via `merge_hooks`, combining request-level and session-level hooks.

## Uncertainty / Limits

- The exact internal logic of `merge_setting` is not shown in the clue file (only its behavior annotation `ACCUMULATE(loop -> result)`). The precise override semantics (e.g., whether `None` request settings fall through to session defaults, or whether dict settings are deeply merged) cannot be confirmed.
- The relative ordering of `prepare_request` vs `merge_environment_settings` within `Session.request` is listed from the `calls` field but the exact sequencing within the function body is not visible.
- Only 24 of 80 L3 symbols have behavior annotations (GAPS section), so some secondary merging interactions may be undocumented.
