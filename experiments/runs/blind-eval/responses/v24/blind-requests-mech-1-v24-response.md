# v2.4 Response: blind-requests-mech-1
Date: 2026-04-16

## Question
When session defaults, per-call options, and environment-derived settings all interact in Requests, what precedence rules does the implementation follow?

## Answer

The Requests library uses a three-tier precedence system where **per-call options override session defaults**, and **environment variables provide fallbacks only when higher-priority values are absent**. The mechanics differ depending on whether the setting is a scalar or a dictionary. The implementation is spread across `merge_setting`, `merge_hooks`, `prepare_request`, `merge_environment_settings`, and the `request` method.

### 1. Core Merge Logic: `merge_setting()`

`merge_setting(request_setting, session_setting, dict_class=OrderedDict)` (`src/requests/sessions.py:62-89`) is the foundational merge function. The source snippet reveals the exact precedence rules:

```python
if session_setting is None:
    return request_setting

if request_setting is None:
    return session_setting

# Bypass if not a dictionary (e.g. verify)
if not (isinstance(session_setting, Mapping) and isinstance(request_setting, Mapping)):
    return request_setting

merged_setting = dict_class(to_key_val_list(session_setting))
merged_setting.update(to_key_val_list(request_setting))

none_keys = [k for (k, v) in merged_setting.items() if v is None]
for key in none_keys:
    del merged_setting[key]

return merged_setting
```
(Source: `merge_setting`, `src/requests/sessions.py L62-89`)

**Precedence rules for `merge_setting`:**

1. **If session_setting is `None`:** Per-call value wins unconditionally — return `request_setting`.
2. **If request_setting is `None`:** Session default wins — return `session_setting`.
3. **For non-dictionary scalars (e.g., `verify`, `stream`, `cert`):** The per-call value always wins — `return request_setting`. This is because the `isinstance(Mapping)` check fails and the function immediately returns the request-level value.
4. **For dictionary-type settings (e.g., headers, params):** A merged dictionary is produced. Session values form the base (`dict_class(to_key_val_list(session_setting))`), and per-call values are layered on top via `.update()`. This means **per-call keys override session keys**, but session keys not present in the per-call dictionary are preserved.
5. **None-value deletion:** After merging dictionaries, any key with a `None` value is deleted. This allows callers to explicitly remove a session-level key by setting it to `None` in the per-call options.

### 2. Hook Merging: `merge_hooks()`

`merge_hooks(request_hooks, session_hooks, dict_class=OrderedDict)` (`src/requests/sessions.py:92-104`) handles the special case of hooks. The source snippet shows:

```python
if session_hooks is None or session_hooks.get("response") == []:
    return request_hooks

if request_hooks is None or request_hooks.get("response") == []:
    return session_hooks

return merge_setting(request_hooks, session_hooks, dict_class)
```
(Source: `merge_hooks`, `src/requests/sessions.py L92-104`)

**Hook precedence rules:**
1. If session hooks are `None` or have an empty `"response"` list: per-call hooks win entirely.
2. If request hooks are `None` or have an empty `"response"` list: session hooks win entirely.
3. Otherwise: falls through to `merge_setting()`, which merges as a dictionary (per-call keys overlay session keys).

The docstring explains this is "necessary because when request_hooks == {'response': []}, the merge breaks Session hooks entirely" — i.e., an empty hook list is treated as "not set" rather than "set to nothing."

### 3. Request Preparation: `prepare_request()`

`Session.prepare_request(request)` (`src/requests/sessions.py:459-500`) is where per-call and session settings are actually merged. The source snippet shows the merge calls:

```python
p = PreparedRequest()
p.prepare(
    method=request.method.upper(),
    url=request.url,
    files=request.files,
    data=request.data,
    json=request.json,
    headers=merge_setting(request.headers, self.headers, dict_class=CaseInsensitiveDict),
    params=merge_setting(request.params, self.params),
    auth=merge_setting(auth, self.auth),
    cookies=merged_cookies,
    hooks=merge_hooks(request.hooks, self.hooks),
)
```
(Source: `prepare_request`, `src/requests/sessions.py L459-500`)

**Settings merged at this stage and their precedence:**

| Setting    | Per-call source        | Session source   | Merge function       | Behavior |
|------------|------------------------|------------------|----------------------|----------|
| `headers`  | `request.headers`      | `self.headers`   | `merge_setting` (dict) | Dictionary merge; per-call keys override, session keys preserved |
| `params`   | `request.params`       | `self.params`    | `merge_setting` (dict) | Dictionary merge |
| `auth`     | `auth` (see below)     | `self.auth`      | `merge_setting` (scalar) | Per-call wins if set |
| `hooks`    | `request.hooks`        | `self.hooks`     | `merge_hooks`        | Special empty-list handling |
| `cookies`  | `request.cookies`      | `self.cookies`   | `merge_cookies` (twice) | Double-merge: session cookies first, then request cookies layered on |

**Auth has an additional fallback:** Before merging, if `self.trust_env` is true and neither `request.auth` nor `self.auth` is set, the method falls back to `get_netrc_auth(request.url)` (`get_netrc_auth`, `src/requests/utils.py:206-247`). This function checks the `NETRC` environment variable for a custom netrc file path, then falls back to standard netrc file locations (`~/.netrc`, etc.). So the auth precedence is: **per-call auth > session auth > netrc (environment)**.

**Cookies have a special merge:** Cookies are merged by first creating a new `RequestsCookieJar`, merging session cookies into it, then merging per-call cookies on top. This ensures per-call cookies override session cookies for the same name.

### 4. Environment Settings: `merge_environment_settings()`

`Session.merge_environment_settings(url, proxies, stream, verify, cert)` (`src/requests/sessions.py:752-781`) is called from `Session.request()` *after* `prepare_request()` and handles environment-derived settings. The source snippet shows:

```python
if self.trust_env:
    no_proxy = proxies.get("no_proxy") if proxies is not None else None
    env_proxies = get_environ_proxies(url, no_proxy=no_proxy)
    for k, v in env_proxies.items():
        proxies.setdefault(k, v)

    if verify is True or verify is None:
        verify = (
            os.environ.get("REQUESTS_CA_BUNDLE")
            or os.environ.get("CURL_CA_BUNDLE")
            or verify
        )

proxies = merge_setting(proxies, self.proxies)
stream = merge_setting(stream, self.stream)
verify = merge_setting(verify, self.verify)
cert = merge_setting(cert, self.cert)
```
(Source: `merge_environment_settings`, `src/requests/sessions.py L752-781`)

**Environment precedence rules (only active when `self.trust_env` is True):**

1. **Proxies:** Environment proxies (from `get_environ_proxies`) are added via `setdefault`, meaning they only fill in keys *not already present* in the per-call `proxies` dict. Then `merge_setting(proxies, self.proxies)` merges with session proxies. So: **per-call proxies > environment proxies > session proxies**.

2. **Verify (TLS CA bundle):** Only overridden by environment if `verify is True or verify is None` — i.e., if the caller hasn't explicitly set it to a specific path or `False`. It checks `REQUESTS_CA_BUNDLE` first, then `CURL_CA_BUNDLE`, then falls back to the existing value. After this, `merge_setting(verify, self.verify)` applies: since `verify` is a scalar, per-call wins. So: **explicit per-call verify path/False > `REQUESTS_CA_BUNDLE` > `CURL_CA_BUNDLE` > session verify**.

3. **Stream and Cert:** No environment variable handling — simply `merge_setting(stream, self.stream)` and `merge_setting(cert, self.cert)`. Per-call wins over session.

### 5. The Full Orchestration in `Session.request()`

`Session.request()` (`src/requests/sessions.py:502-593`) ties everything together. It:
1. Creates a `Request` object from per-call arguments.
2. Calls `prepare_request(req)` — merges headers, params, auth, cookies, hooks (per-call vs. session).
3. Builds `settings` dict from per-call kwargs (proxies, stream, verify, cert).
4. Calls `merge_environment_settings(url, **settings)` — layers in environment variables and session defaults for transport settings.
5. Calls `send(prep, **settings)` — dispatches the prepared request with final merged settings.

### Complete Precedence Summary

| Setting   | Highest Priority | → | → | Lowest Priority |
|-----------|-----------------|---|---|----------------|
| headers   | Per-call keys   | Session keys (preserved if not overridden) | — | — |
| params    | Per-call keys   | Session keys | — | — |
| auth      | Per-call auth   | Session auth | netrc (env) | — |
| cookies   | Per-call cookies | Session cookies | — | — |
| hooks     | Per-call hooks (if non-empty) | Session hooks (if non-empty) | Dictionary merge via `merge_setting` | — |
| proxies   | Per-call proxies | Env proxies (setdefault) | Session proxies | — |
| verify    | Explicit per-call (path/False) | `REQUESTS_CA_BUNDLE` | `CURL_CA_BUNDLE` | Session verify |
| stream    | Per-call        | Session default | — | — |
| cert      | Per-call        | Session default | — | — |

### What Cannot Be Determined

- The full `Session.request()` source is truncated in the snippet, so we cannot see the exact lines where `merge_environment_settings` is called or confirm every kwarg passed to `send()`.
- How `get_environ_proxies()` discovers environment proxies (the underlying `getproxies` call) is referenced only via `get_environ_proxies` behavior (`BRANCH(should_bypass_proxies -> return {}, else -> return getprox...)`), but the full implementation is not provided.
- The behavior of `merge_cookies` (used for cookie merging in `prepare_request`) is listed as uncovered in the GAPS section.
- Whether `Session.__init__` sets default values for `trust_env`, `stream`, `verify`, `cert`, `proxies` etc. is not shown in the clue file or snippets.
