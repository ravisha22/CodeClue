# v2.4 Response: blind-requests-rel-2
Date: 2026-04-16

## Question
How do `Session` and transport adapters relate to one another when Requests selects a transport for a URL?

## Answer

The `Session` and transport adapters have a **registry-based delegation relationship**: `Session` maintains an ordered mapping of URL prefixes to adapter instances, selects the appropriate adapter by matching a URL against those prefixes, and delegates the actual network I/O to the matched adapter.

### 1. The Adapter Abstraction

Transport adapters are rooted in `BaseAdapter` (class, `src/requests/adapters.py:114-141`), described as "The Base Transport Adapter." It raises `NotImplementedError` for its methods, establishing an abstract interface that concrete adapters must implement (`BaseAdapter`, `src/requests/adapters.py:114-141`).

The built-in concrete adapter is `HTTPAdapter` (class, `src/requests/adapters.py:144-697`), described as "The built-in HTTP Adapter for urllib3." It extends `BaseAdapter` and provides the actual HTTP transport implementation. It calls `build_response`, `cert_verify`, `get_connection_with_tls_context`, `init_poolmanager`, `proxy_manager_for`, `proxy_headers`, `request_url`, and `add_headers` (`HTTPAdapter`, `src/requests/adapters.py:144-697`).

### 2. Adapter Registration via `mount()`

`Session.mount(prefix, adapter)` (`src/requests/sessions.py:801-810`) "Registers a connection adapter to a prefix." The source snippet reveals the exact mechanism:

```python
def mount(self, prefix, adapter):
    self.adapters[prefix] = adapter
    keys_to_move = [k for k in self.adapters if len(k) < len(prefix)]
    for key in keys_to_move:
        self.adapters[key] = self.adapters.pop(key)
```
(Source: `mount`, `src/requests/sessions.py L801-810`)

This shows that:
- Adapters are stored in `self.adapters`, a dictionary keyed by URL prefix strings.
- After insertion, keys shorter than the new prefix are re-ordered to appear later, ensuring **adapters are sorted in descending order by prefix length** (as stated in the docstring: "Adapters are sorted in descending order by prefix length").
- This ordering is critical for correct prefix matching: longer, more specific prefixes are checked first.

### 3. Adapter Selection via `get_adapter()`

`Session.get_adapter(url)` (`src/requests/sessions.py:783-794`) "Returns the appropriate connection adapter for the given URL." The source snippet shows:

```python
def get_adapter(self, url):
    for prefix, adapter in self.adapters.items():
        if url.lower().startswith(prefix.lower()):
            return adapter
    raise InvalidSchema(f"No connection adapters were found for {url!r}")
```
(Source: `get_adapter`, `src/requests/sessions.py L783-794`)

Key behaviors:
- The method iterates through `self.adapters.items()` in insertion order (which is descending by prefix length due to `mount()`).
- It performs a **case-insensitive prefix match** (`url.lower().startswith(prefix.lower())`).
- The **first match wins** — because prefixes are sorted longest-first, the most specific adapter is always selected.
- If no prefix matches, it raises `InvalidSchema` (`InvalidSchema`, `src/requests/exceptions.py:104-105`): "The URL scheme provided is either invalid or unsupported."
- The return type is `requests.adapters.BaseAdapter` (per the docstring).

### 4. How `Session` Uses the Selected Adapter

The `Session.send()` method (`src/requests/sessions.py:675-750`) "Send a given PreparedRequest." Its clue entry shows it `calls: get, get_adapter, resolve_redirects` (`send`, `src/requests/sessions.py:675-750`). The flow is:

1. `Session.request()` (`src/requests/sessions.py:502-593`) calls `merge_environment_settings` and then `send`.
2. `Session.send()` calls `get_adapter(url)` to look up the correct adapter for the request URL.
3. The adapter's `send()` method is invoked to perform the actual HTTP transfer (the adapter's `send` is listed in the INDEX: `send`, `src/requests/adapters.py`).
4. The adapter's `build_response(req, resp)` (`src/requests/adapters.py:337-372`) constructs a `Response` object from the urllib3 response, using `Response` (models) and `CaseInsensitiveDict` (structures).
5. If redirects are enabled, `resolve_redirects()` (`src/requests/sessions.py:160-280`) loops and may call `send()` again (which re-invokes `get_adapter()` for each redirect URL).

### 5. Session Closure and Adapters

`Session.close()` (`src/requests/sessions.py:796-799`) "Closes all adapters and as such the session." The source snippet confirms:

```python
def close(self):
    for v in self.adapters.values():
        v.close()
```
(Source: `close`, `src/requests/sessions.py L796-799`)

This iterates through all registered adapters and calls `close()` on each, releasing their connection pools. The `close` method on `Session` is called by `__exit__`, confirming `Session` supports context-manager usage (`close called_by: __exit__, Session, resolve_redirects, SessionRedirectMixin`).

### 6. Adapter Capabilities

The `HTTPAdapter` provides rich transport functionality:
- **Connection pooling:** `init_poolmanager()` (`src/requests/adapters.py:217`) initializes a urllib3 `PoolManager`.
- **Proxy support:** `proxy_manager_for()` (`src/requests/adapters.py:243`) returns a urllib3 `ProxyManager` for a given proxy. `proxy_headers()` (`src/requests/adapters.py:570`) returns headers to add for proxy requests.
- **TLS:** `get_connection_with_tls_context()` (`src/requests/adapters.py:424-471`) returns a connection with TLS settings, branching on whether a proxy is present.
- **URL construction:** `request_url(request, proxies)` (`src/requests/adapters.py:524-554`) obtains the final URL for the request.
- **Pool key management:** `build_connection_pool_key_attributes()` (`src/requests/adapters.py:374`) builds PoolKey attributes for urllib3.
- **SOCKS support:** `SOCKSProxyManager` is referenced (`src/requests/adapters.py:63`).

### Relationship Summary

```
Session
  ├── mount(prefix, adapter)     → registers adapter to self.adapters[prefix]
  ├── get_adapter(url)           → prefix-match lookup → returns BaseAdapter
  ├── send(PreparedRequest)      → get_adapter() → adapter.send() → Response
  ├── close()                    → adapter.close() for all adapters
  └── adapters: OrderedDict[prefix → BaseAdapter]
         ├── "https://" → HTTPAdapter instance
         └── "http://"  → HTTPAdapter instance
```

### What Cannot Be Determined

- The default set of adapters registered in `Session.__init__()` is not shown in the clue file or source snippets (though standard practice would be "https://" and "http://" mapped to `HTTPAdapter` instances).
- The full signature and implementation of `HTTPAdapter.send()` are not provided in the FOCUS section (it is listed in the GAPS as partially uncovered).
- Whether custom adapter subclasses are used anywhere in the codebase is not determinable.
- The `_urllib3_request_context` function (`src/requests/adapters.py:77-111`) is called by `HTTPAdapter` but its exact role in transport selection is not fully detailed.
