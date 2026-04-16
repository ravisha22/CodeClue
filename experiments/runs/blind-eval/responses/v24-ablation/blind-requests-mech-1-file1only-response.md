# v2.4 Ablation (File 1 Only): blind-requests-mech-1
Date: 2026-04-16

The request pipeline has three relevant merge stages: `request()` calls `merge_environment_settings`, `prepare_request`, and then `send`. So environment-derived settings are folded in during request execution, while request/session preparation happens in `prepare_request`. [request (src/requests/sessions.py:502-593)]

The generic merge primitive is `merge_setting(request_setting, session_setting, dict_class)`. Its name/signature and behavior annotation show it combines request-level and session-level settings, then removes `None` keys. [merge_setting (src/requests/sessions.py:62-89)]

Hooks use the same precedence machinery: `merge_hooks` “properly merges both requests and session hooks” and calls `merge_setting`. [merge_hooks (src/requests/sessions.py:92-104)]

Environment inputs are merged by `merge_environment_settings(url, proxies, stream, verify, cert)`, which checks the environment and also calls `merge_setting`. The visible environment helper for proxies is `get_environ_proxies`, which either returns `{}` when proxies should be bypassed or returns proxy settings from the environment. [merge_environment_settings (src/requests/sessions.py:752-781); get_environ_proxies (src/requests/utils.py:813-822)]

Other defaults/sources visible in the clue are default headers and netrc auth: `default_headers` builds a `CaseInsensitiveDict` using `default_user_agent`, and `get_netrc_auth` returns auth for a URL from netrc. [default_headers (src/requests/utils.py:887-898); get_netrc_auth (src/requests/utils.py:206-247)]

What I can support confidently is this precedence shape: request-level values and session-level values are merged via `merge_setting`; hooks follow the same pattern; and environment-specific transport settings are merged in `merge_environment_settings` during `request()`. What I cannot determine exactly is the final winner for every conflicting field (for example, explicit auth vs netrc, or explicit proxy/verify/cert vs environment), because the clue does not expose the body of `prepare_request` or the detailed merge branches inside `merge_environment_settings`. [request (src/requests/sessions.py:502-593); merge_setting (src/requests/sessions.py:62-89); merge_environment_settings (src/requests/sessions.py:752-781); GAPS]
