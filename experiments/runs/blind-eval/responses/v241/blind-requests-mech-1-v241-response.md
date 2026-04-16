# v2.4.1 Response: blind-requests-mech-1
Date: 2026-04-16

## Precedence is implemented by `merge_setting`, with environment injection happening before the final merge

The core rule lives in `merge_setting`. The source snippet shows:

- if the session value is `None`, return the request value;
- if the request value is `None`, return the session value;
- if both values are **not** mappings, return the request value directly;
- if both are mappings, start from the session mapping, `update` it with the request mapping, then delete keys whose merged value is `None`

(source snippet `merge_setting`, `src/requests/sessions.py L62-89`).

That gives a precise precedence model:

- **Scalar / non-dict settings:** per-call request value wins over session value whenever it is not `None`; otherwise the session value fills in (source snippet `merge_setting`, `src/requests/sessions.py L62-89`).
- **Dict settings:** session values provide the base; request values override matching keys; and a per-call key set to `None` removes that key entirely from the merged result (same snippet).

`merge_hooks` adds one special rule for hook dicts. If `session_hooks` is missing or has `{"response": []}`, it returns `request_hooks`; if `request_hooks` is missing or has `{"response": []}`, it returns `session_hooks`; otherwise it falls back to `merge_setting` (source snippet `merge_hooks`, `src/requests/sessions.py L92-104`). So hook precedence is still request-over-session, but an explicit empty `response` hook list disables normal dict merging and hands control to the non-empty side (`merge_hooks`, `src/requests/sessions.py:92-104` and snippet).

Environment-derived settings are injected in `merge_environment_settings` **before** the final call to `merge_setting`. The source snippet shows:

- environment logic only runs when `self.trust_env` is true;
- for proxies, `get_environ_proxies(url, no_proxy=no_proxy)` is called and each env proxy is inserted with `proxies.setdefault(k, v)`;
- for certificate verification, environment bundles are only considered when `verify is True or verify is None`, and then `REQUESTS_CA_BUNDLE` wins over `CURL_CA_BUNDLE`, which wins over the prior `verify` value;
- after that, `proxies`, `stream`, `verify`, and `cert` are each merged with the session via `merge_setting`

(source snippet `merge_environment_settings`, `src/requests/sessions.py L752-781`).

From that implementation, the supported precedence rules are:

- **Proxies:** start with per-call `proxies`; fill missing keys from environment via `setdefault`; then merge that result over `self.proxies`, so per-call keys win, env fills only missing per-call keys, and session is the fallback base (source snippet `merge_environment_settings`, `src/requests/sessions.py L752-781`; source snippet `merge_setting`, `src/requests/sessions.py L62-89`).
- **Verify:** if the caller passed `False`, environment CA bundles are skipped entirely because the env branch only runs when `verify is True or verify is None`; otherwise `REQUESTS_CA_BUNDLE` overrides `CURL_CA_BUNDLE`, and that env-derived value is then merged over `self.verify`, so explicit per-call `verify` beats session, but trusted env can replace `True`/`None` before the session fallback merge (same snippet).
- **Stream and cert:** there is no environment injection shown; they simply go through `merge_setting`, so explicit per-call value beats session value, with session as fallback (same snippets).

**What Cannot Be Determined**

- The prompt does not show `to_key_val_list`, so the exact accepted mapping-like inputs for dict merges are not fully specified (source snippet `merge_setting` calls `to_key_val_list`).
- The defaults of `self.proxies`, `self.stream`, `self.verify`, and `self.cert` inside `Session.__init__` are not shown.
- `get_environ_proxies` itself is not expanded here, so no finer proxy-precedence rules beyond “env fills missing keys before the final merge” can be asserted from this prompt.
