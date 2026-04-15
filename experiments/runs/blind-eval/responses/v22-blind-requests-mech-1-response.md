# v2.2 Response: blind-requests-mech-1
Date: 2026-04-15

## Question

When session defaults, per-call options, and environment-derived settings all interact in Requests, what precedence rules does the implementation follow?

## Answer

The clue file identifies three distinct merge functions that implement the precedence rules, plus the orchestrating `Session.request` method that sequences their invocation.

### 1. The Three Settings Sources

Based on the clue, three sources of configuration interact:

1. **Session defaults** — stored as attributes on the `Session` object (`src/requests/sessions.py:356`).
2. **Per-call options** — passed as arguments to `Session.request` (`src/requests/sessions.py:502`, sig: `request(method, url, params, data, headers...)`).
3. **Environment-derived settings** — obtained via `merge_environment_settings` (`src/requests/sessions.py:752`).

### 2. `merge_setting` — The Core Merge Primitive

- **`merge_setting`** (`src/requests/sessions.py:62`) — "Determines appropriate setting for a given request, taking into account..."
  - `sig: merge_setting(request_setting, session_setting, dict_class)`
  - `behavior: ACCUMULATE(loop -> result)` — iterates to build a merged result.
  - `called_by: merge_environment_settings, prepare_request, Session, merge_hooks`.

The parameter order is significant: the first argument is `request_setting` (per-call) and the second is `session_setting` (session default). This naming convention strongly implies that **per-call settings take precedence over session defaults** — the function determines the "appropriate setting" by considering the request-level value first, falling back to the session-level value.

### 3. `merge_hooks` — Hook Merging

- **`merge_hooks`** (`src/requests/sessions.py:92`) — "Properly merges both requests and session hooks."
  - `sig: merge_hooks(request_hooks, session_hooks, dict_class)`
  - `calls: get, merge_setting`.
  - `called_by: prepare_request, Session`.

The parameter ordering again places `request_hooks` first and `session_hooks` second, and it delegates to `merge_setting` — confirming the same precedence pattern: per-call hooks override or augment session-level hooks.

### 4. `prepare_request` — Merging Per-Call with Session Defaults

- **`prepare_request`** (`src/requests/sessions.py:459`) — "Constructs a :class:`PreparedRequest <PreparedRequest>`."
  - `calls: merge_hooks, merge_setting`.
  - `called_by: request, Session`.
  - `uses: PreparedRequest (models), RequestsCookieJar (cookies)`.

This method is called by `Session.request` and is where session-level defaults (headers, auth, cookies, hooks) are merged with per-call parameters. It calls `merge_setting` (presumably for headers, auth, params, etc.) and `merge_hooks` (for hooks), applying the per-call-over-session precedence.

### 5. `merge_environment_settings` — Adding Environment as a Third Layer

- **`merge_environment_settings`** (`src/requests/sessions.py:752`) — "Check the environment and merge it with some settings."
  - `sig: merge_environment_settings(url, proxies, stream, verify, cert)`
  - `calls: get, merge_setting`.
  - `called_by: request, Session`.

This function is called by `Session.request` and introduces environment-derived values (e.g., environment variables for proxies, SSL verification). It calls `merge_setting` to combine these with the already-established settings.

Supporting environment functions from `src/requests/utils.py`:
- **`get_environ_proxies`** (`src/requests/utils.py:813`) — "Return a dict of environment proxies." `behavior: BRANCH(should_bypass_proxies -> empty, else -> getproxies)`.
- **`should_bypass_proxies`** (`src/requests/utils.py:752`) — "Returns whether we should bypass proxies or not."
- **`proxy_bypass`** (`src/requests/utils.py:114`) — "Return True, if the host should be bypassed." `behavior: BRANCH(getproxies_environment -> proxy_bypass_environment, else -> proxy_bypass_registry)`.
- **`set_environ`** (`src/requests/utils.py:731`) — "Set the environment variable 'env_name' to 'value'."
- **`get_netrc_auth`** (`src/requests/utils.py:206`) — "Returns the Requests tuple auth for a given url from netrc."

### 6. The Orchestration Sequence in `Session.request`

- **`Session.request`** (`src/requests/sessions.py:502`) — Calls, in order:
  1. `prepare_request` — merges per-call args with session defaults → `PreparedRequest`.
  2. `merge_environment_settings` — merges environment into settings.
  3. `send` — dispatches the prepared request.

This sequencing reveals the precedence chain:

```
Per-call arguments  (highest priority)
       ↓
Session defaults    (medium priority)
       ↓
Environment         (lowest priority / fallback)
```

The rationale: `prepare_request` runs first, giving per-call args priority over session defaults. Then `merge_environment_settings` runs, but since `merge_setting` is called with the already-merged result, environment values only fill in where no explicit per-call or session value was set.

### 7. Precedence Summary

| Priority | Source | Where Merged |
|---|---|---|
| **Highest** | Per-call arguments (`method`, `url`, `params`, `data`, `headers`, etc.) | `prepare_request` (`sessions.py:459`) via `merge_setting` (`sessions.py:62`) |
| **Medium** | Session-level defaults (`Session` attributes) | `prepare_request` (`sessions.py:459`) via `merge_setting` (`sessions.py:62`) |
| **Lowest** | Environment variables (proxies, certs, netrc auth) | `merge_environment_settings` (`sessions.py:752`) via `merge_setting` (`sessions.py:62`) |

### What Cannot Be Fully Determined

The clue file does not contain the **body** of `merge_setting`, so the exact merging logic (e.g., whether dict values are deep-merged or shallow-replaced, how `None` values are treated) cannot be determined. The `ACCUMULATE(loop -> result)` behavior annotation suggests it iterates over dict keys to build a merged result, but the precise semantics (e.g., whether `None` means "use the other source's value" vs. "explicitly set to None") are not visible. The `dict_class` parameter in both `merge_setting` and `merge_hooks` hints that the merge behavior may depend on the type of setting being merged (e.g., `CaseInsensitiveDict` for headers).
