# v2.3 Response: blind-requests-rel-2
Date: 2026-04-15

## Summary

`Session` maintains a registry of transport adapters mapped to URL prefixes. When sending a request, `Session.send` calls `get_adapter` to look up the appropriate adapter for a given URL. Adapters are registered via `mount`, and `Session.close` iterates over all adapters to close them. The adapter hierarchy is `BaseAdapter` → `HTTPAdapter`, with `HTTPAdapter` handling the actual HTTP transport via urllib3.

## Detailed Analysis

### 1. Adapter Registration: `Session.mount`

- `mount` (src/requests/sessions.py:801) "Registers a connection adapter to a prefix" (SYM: mount). This means `Session` stores adapters keyed by URL prefix strings (e.g., `"https://"`, `"http://"`).
- `Session` calls `mount` as part of its API (FOCUS: Session, calls field includes `mount`).

### 2. Adapter Lookup: `Session.get_adapter`

- `get_adapter` (src/requests/sessions.py:783-794) "Returns the appropriate connection adapter for the given URL" (FOCUS: get_adapter).
- Its behavior is `ACCUMULATE(loop -> result)` (FOCUS: get_adapter, behavior field), indicating it iterates over registered adapters to find the matching one — likely by prefix matching against the URL.
- It is called by `send` and `Session` (FOCUS: get_adapter, called_by: `send, Session`).
- If no adapter matches, it raises `InvalidSchema` (FOCUS: get_adapter, raises: `InvalidSchema`; also FOCUS: Session, raises: `InvalidSchema`). `InvalidSchema` (src/requests/exceptions.py:104-105) means "The URL scheme provided is either invalid or unsupported" (FOCUS: InvalidSchema).

### 3. The Send Flow: `Session.send` Uses Adapters

- `Session.send` (src/requests/sessions.py:675-750) "Send a given PreparedRequest" — it calls `get_adapter` to select the transport adapter, then delegates actual sending to that adapter (FOCUS: send at sessions.py:675, calls: `get, get_adapter, resolve_redirects`).
- The behavior is `BRANCH(allow_redirects -> result, else -> result)` (FOCUS: send at sessions.py:675), meaning it conditionally invokes redirect resolution after the adapter completes.

### 4. The Adapter Hierarchy

- **`BaseAdapter`** (src/requests/adapters.py:114-141) is "The Base Transport Adapter." It raises `NotImplementedError` (FOCUS: BaseAdapter), meaning it defines the abstract interface but does not implement transport logic.
- **`HTTPAdapter`** (src/requests/adapters.py:144-697) is "The built-in HTTP Adapter for urllib3" and extends `BaseAdapter` (FOCUS: HTTPAdapter). It provides the concrete implementation.
- `HTTPAdapter` calls: `add_headers`, `build_connection_pool_key_attributes`, `build_response`, `cert_verify`, `get_connection_with_tls_context`, `init_poolmanager`, `proxy_headers`, `proxy_manager_for` (FOCUS: HTTPAdapter, calls field).

### 5. HTTPAdapter's Key Responsibilities

- **Sending**: `send` in adapters.py (src/requests/adapters.py:591-697) "Sends PreparedRequest object" and can raise `InvalidURL`, `ConnectionError`, `ProxyError`, `ValueError` (FOCUS: send at adapters.py:591).
- **Building Responses**: `build_response` (src/requests/adapters.py:337-372) "Builds a :class:`Response <requests.Response>` object from a urllib3" response. It uses `Response (models)` and `CaseInsensitiveDict (structures)` (FOCUS: build_response).
- **Connection Pooling**: `init_poolmanager` (src/requests/adapters.py:217) "Initializes a urllib3 PoolManager" (SYM: init_poolmanager). `build_connection_pool_key_attributes` (src/requests/adapters.py:374) "Build the PoolKey attributes used by urllib3" (SYM: build_connection_pool_key_attributes).
- **TLS**: `get_connection_with_tls_context` (src/requests/adapters.py:424-471) "Returns a urllib3 connection for the given request and TLS settings" with behavior `BRANCH(proxy -> raise_InvalidProxyURL, else -> result)` (FOCUS: get_connection_with_tls_context).
- **Proxy Support**: `proxy_manager_for` (src/requests/adapters.py:243) "Return urllib3 ProxyManager for the given proxy" (SYM: proxy_manager_for). `proxy_headers` (src/requests/adapters.py:570) "Returns a dictionary of the headers to add to any request sent through a proxy" (SYM: proxy_headers).
- **URL Construction**: `request_url` (src/requests/adapters.py:524-554) "Obtain the url to use when making the final request" (FOCUS: request_url, called_by: HTTPAdapter).

### 6. Session Lifecycle and Adapter Cleanup

- `Session.close` (src/requests/sessions.py:796-799) "Closes all adapters and as such the session" with behavior `ACCUMULATE(loop -> result)` (FOCUS: close at sessions.py:796). This confirms `Session` iterates over all mounted adapters and closes each one.
- `close` is called by `__exit__`, `Session`, `resolve_redirects`, and `SessionRedirectMixin` (FOCUS: close, called_by field).

### 7. SOCKS Proxy Support

- `SOCKSProxyManager` (src/requests/adapters.py:63) is referenced in the SYM table (SYM: SOCKSProxyManager), suggesting the adapter layer also supports SOCKS proxies, though details are limited in the clue file.

## Uncertainty / Limits

- The clue file does not show the exact prefix-matching algorithm used by `get_adapter`. The `ACCUMULATE(loop -> result)` behavior suggests iteration, but whether it uses longest-prefix matching or first-match is not determinable.
- The clue file does not reveal what default adapters `Session.__init__` mounts (e.g., the conventional `"https://"` and `"http://"` prefixes are not explicitly shown).
- Only 28 of 80 L3 symbols have behavior annotations (GAPS section), so some secondary adapter interactions may be missing.
