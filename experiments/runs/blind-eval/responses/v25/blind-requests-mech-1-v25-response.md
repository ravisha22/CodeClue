# v2.5 Response: blind-requests-mech-1
Date: 2026-04-16

## Answer

When session defaults, per-call options, and environment-derived settings all interact in the Requests library, the implementation enforces a layered precedence system anchored around the `merge_setting` helper, the `prepare_request` method, and the `merge_environment_settings` method. The overall resolution order is: **per-call request values > environment-derived values (for proxies and verify) > session-level defaults**. Below is a detailed mechanistic walkthrough of how this precedence is established.

---

### 1. `merge_setting` — The Core Precedence Primitive

The function `merge_setting(request_setting, session_setting, dict_class=OrderedDict)` (`src/requests/sessions.py:62-89`) is the fundamental building block that nearly every other merge operation delegates to. Its precedence logic is:

- **If `session_setting` is `None`**, the per-call `request_setting` is returned unconditionally (`src/requests/sessions.py:62-89`, early return branch). This means a per-call value always survives when there is no session default.
- **If `request_setting` is `None`**, the `session_setting` is returned (`src/requests/sessions.py:62-89`, second early return). This allows session defaults to serve as fallbacks when the caller supplies nothing.
- **For non-dict scalar values** (e.g., `verify`, `stream`, `cert`): if neither argument is `None` and at least one is not a `Mapping`, the function returns `request_setting` directly (`src/requests/sessions.py:62-89`, bypass branch: `if not (isinstance(session_setting, Mapping) and isinstance(request_setting, Mapping)): return request_setting`). This means **per-call scalars always win over session scalars**.
- **For dict values** (e.g., `headers`, `params`, `proxies`): the session setting is used as the base dictionary, and the request setting is overlaid on top via `merged_setting.update(to_key_val_list(request_setting))` (`src/requests/sessions.py:62-89`). After merging, any keys whose value is `None` are deleted from the result (`none_keys` loop, `src/requests/sessions.py:62-89`, behavior: `ACCUMULATE(none_keys loop -> result)`). This means per-call dict entries override same-keyed session entries, and a caller can explicitly remove a session-level key by setting it to `None`.

**Summary**: In all cases — scalar or dict — the per-call `request_setting` takes precedence over `session_setting`. For dicts, the session provides the base and the request overlays; for scalars, the request value simply replaces the session value.

---

### 2. `prepare_request` — Merging Per-Call Request Fields Against Session Defaults

The method `prepare_request(self, request)` (`src/requests/sessions.py:459-500`) is responsible for assembling a `PreparedRequest` from a `Request` object and the session's stored defaults. It calls `merge_setting` for each field:

- **Headers**: `merge_setting(request.headers, self.headers, dict_class=CaseInsensitiveDict)` (`src/requests/sessions.py:459-500`). Per-call headers overlay session headers; session headers fill in any gaps.
- **Params**: `merge_setting(request.params, self.params)` (`src/requests/sessions.py:459-500`). Same precedence — per-call params override session params.
- **Auth**: `merge_setting(auth, self.auth)` (`src/requests/sessions.py:459-500`). The per-call auth wins over the session-level `self.auth`.
- **Cookies**: Handled separately via `RequestsCookieJar` merging (`src/requests/sessions.py:459-500`, uses `RequestsCookieJar` from cookies).
- **Hooks**: Delegated to `merge_hooks(request.hooks, self.hooks)` (`src/requests/sessions.py:459-500`), discussed below.

In every case, `merge_setting` guarantees that per-call request values override session-level defaults.

---

### 3. Environment-Derived Settings via `merge_environment_settings`

The method `merge_environment_settings(self, url, proxies, stream, verify, cert)` (`src/requests/sessions.py:752-781`) introduces environment-derived values into the resolution chain, but only when `self.trust_env` is truthy. The precedence interactions here are nuanced:

#### 3a. Proxies

When `trust_env` is enabled, environment proxies are fetched via `get_environ_proxies(url, no_proxy=no_proxy)` (`src/requests/utils.py:813-822`). The function `get_environ_proxies` first checks whether the URL should bypass proxies entirely; if so, it returns an empty dict (`src/requests/utils.py:813-822`, behavior: `BRANCH(should_bypass_proxies -> return {}, else -> return getprox...)`).

The environment proxy entries are then merged into the per-call `proxies` dict using `proxies.setdefault(k, v)` (`src/requests/sessions.py:752-781`). Crucially, `setdefault` does **not** overwrite existing keys — it only fills in keys that are absent. This means **explicitly provided per-call proxy entries are never overridden by environment proxies**; the environment only supplies defaults for proxy schemes not already specified.

After environment injection, the combined proxies dict is merged against the session's `self.proxies` via `merge_setting(proxies, self.proxies)` (`src/requests/sessions.py:752-781`). Since the per-call+environment proxies are passed as `request_setting` and session proxies as `session_setting`, the per-call/environment values overlay session defaults per `merge_setting`'s dict-merge logic.

**Proxy precedence**: per-call explicit > environment (`setdefault`) > session defaults (`merge_setting`).

#### 3b. Verify (CA Bundle)

When `trust_env` is enabled and `verify is True or verify is None`, the implementation substitutes the value of `os.environ.get("REQUESTS_CA_BUNDLE")` or `os.environ.get("CURL_CA_BUNDLE")`, falling back to the original `verify` value (`src/requests/sessions.py:752-781`). This means:

- If the caller explicitly passes `verify=False` or `verify="/path/to/bundle"`, the environment variables are **not consulted** (the condition `verify is True or verify is None` fails).
- If `verify` is left at its default (`True` or `None`), the environment CA bundle paths can override it.
- `REQUESTS_CA_BUNDLE` takes precedence over `CURL_CA_BUNDLE` due to the `or`-chain short-circuit (`src/requests/sessions.py:752-781`).

After this conditional substitution, `verify` is merged against `self.verify` via `merge_setting(verify, self.verify)` (`src/requests/sessions.py:752-781`). Since `verify` is a scalar (string or bool), `merge_setting` returns the per-call value when both are non-`None` (`src/requests/sessions.py:62-89`).

**Verify precedence**: explicit per-call path/False > `REQUESTS_CA_BUNDLE` > `CURL_CA_BUNDLE` > session `self.verify`.

#### 3c. Stream and Cert

Both `stream` and `cert` are merged directly against their session counterparts without environment variable involvement: `merge_setting(stream, self.stream)` and `merge_setting(cert, self.cert)` (`src/requests/sessions.py:752-781`). Per-call values win over session defaults via `merge_setting`'s scalar precedence rule.

---

### 4. Auth Fallback — Netrc as Last Resort

In `prepare_request` (`src/requests/sessions.py:459-500`), authentication has a special three-tier fallback:

1. If `request.auth` is set, it is used (per-call wins).
2. If `request.auth` is not set but `self.auth` (session-level) is set, `merge_setting(auth, self.auth)` returns `self.auth` since `auth` would be `None` at that point (`src/requests/sessions.py:62-89`, second early return).
3. If **neither** `request.auth` nor `self.auth` is set, and `self.trust_env` is truthy, then `get_netrc_auth(request.url)` (`src/requests/utils.py:206-247`) is consulted to extract credentials from the user's `.netrc` file (`src/requests/sessions.py:459-500`, conditional: `if self.trust_env and not auth and not self.auth`).

**Auth precedence**: per-call `request.auth` > session `self.auth` > netrc (environment, only when `trust_env` is true and both prior sources are absent).

---

### 5. Hooks — `merge_hooks` Behavior

The function `merge_hooks(request_hooks, session_hooks, dict_class=OrderedDict)` (`src/requests/sessions.py:92-104`) has its own short-circuit logic before delegating to `merge_setting`:

- If `session_hooks` is `None` or its `"response"` key is an empty list, `request_hooks` is returned directly (`src/requests/sessions.py:92-104`). This ensures that an empty session hook list does not suppress per-call hooks.
- Conversely, if `request_hooks` is `None` or its `"response"` key is an empty list, `session_hooks` is returned (`src/requests/sessions.py:92-104`).
- Otherwise, the function delegates to `merge_setting(request_hooks, session_hooks, dict_class)` (`src/requests/sessions.py:92-104`), which applies standard dict-merge precedence: session hooks form the base, request hooks overlay.

Note that because hooks are dicts of lists, `merge_setting`'s `update()` call means per-call hooks for a given event type (e.g., `"response"`) **replace** rather than append to session-level hooks for that same event type.

---

### 6. The `request` Method — Orchestration of All Merges

The `Session.request` method (`src/requests/sessions.py:502-593`) orchestrates the full pipeline:

1. It calls `prepare_request` (`src/requests/sessions.py:502-593`) to merge per-call request fields (headers, params, auth, cookies, hooks) against session defaults.
2. It then calls `merge_environment_settings(url, proxies, stream, verify, cert)` (`src/requests/sessions.py:502-593`) to fold in environment variables and merge the result against session-level transport settings.
3. Finally, it passes all resolved settings to `send` (`src/requests/sessions.py:502-593`).

This two-phase approach means that `prepare_request` handles request-content-level merges (headers, auth, etc.) while `merge_environment_settings` handles transport-level merges (proxies, TLS, streaming).

---

### 7. Overall Precedence Summary

Combining all of the above, the complete precedence order is:

| Setting   | Precedence (highest → lowest)                                                                                   |
|-----------|----------------------------------------------------------------------------------------------------------------|
| Headers   | Per-call `request.headers` > Session `self.headers` (`merge_setting`, `src/requests/sessions.py:459-500`)       |
| Params    | Per-call `request.params` > Session `self.params` (`merge_setting`, `src/requests/sessions.py:459-500`)         |
| Auth      | Per-call `request.auth` > Session `self.auth` > Netrc (`get_netrc_auth`, `src/requests/utils.py:206-247`)       |
| Hooks     | Per-call `request.hooks` > Session `self.hooks` (`merge_hooks`, `src/requests/sessions.py:92-104`)              |
| Proxies   | Per-call explicit > Environment proxies (`setdefault`) > Session `self.proxies` (`src/requests/sessions.py:752-781`) |
| Verify    | Per-call explicit path/False > `REQUESTS_CA_BUNDLE` > `CURL_CA_BUNDLE` > Session `self.verify` (`src/requests/sessions.py:752-781`) |
| Stream    | Per-call > Session `self.stream` (`merge_setting`, `src/requests/sessions.py:752-781`)                          |
| Cert      | Per-call > Session `self.cert` (`merge_setting`, `src/requests/sessions.py:752-781`)                            |

**General rule**: Per-call options always win. Environment-derived values (proxies, CA bundles, netrc) act as a middle tier that fills in gaps left by per-call options but never overrides them. Session defaults provide the baseline that everything else overlays.

---

### 8. Gaps and Limitations

This analysis is based on the clue evidence provided and has the following known gaps (gap type: **MECHANISTIC** — body logic needed for full answer):

- **`address_in_network`**: Not covered. This utility likely participates in proxy bypass logic (related to `should_bypass_proxies` within `get_environ_proxies` at `src/requests/utils.py:813-822`), but its internal precedence behavior is not available.
- **`build_digest_header`**: Not covered. This is relevant to digest authentication flows but does not directly affect the merge-precedence hierarchy analyzed here.
- **`cert_verify`**: Not covered. This likely implements the downstream consumption of the merged `verify` and `cert` values, but its interaction with the precedence chain is not observable from the provided evidence.
- **`delete`**: Not covered. As an HTTP-method convenience wrapper, it presumably delegates to `Session.request` and inherits all precedence rules described above, but this is not directly confirmed.

Without these symbols, the analysis cannot fully trace how merged values are consumed downstream (e.g., whether `cert_verify` applies additional overrides after `merge_environment_settings` returns). The precedence rules described above are accurate for the merge phase but may be subject to further transformation during request execution.
