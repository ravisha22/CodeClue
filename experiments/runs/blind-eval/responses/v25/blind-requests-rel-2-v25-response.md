# v2.5 Response: blind-requests-rel-2
Date: 2026-04-16

## Answer

### 1. The Adapter Registry: `self.adapters` as an Ordered Mapping

A `Session` object (defined at `sessions.py:356–818`) maintains an internal ordered dictionary, `self.adapters`, that maps URL-scheme prefixes (e.g., `"https://"`, `"http://"`) to transport adapter instances [Session clue: `sessions.py:356–818`]. This registry is the sole mechanism by which a `Session` resolves which transport adapter should handle a given request URL. During `Session.__init__`, the `mount()` method is called to seed this dictionary with the default adapters [mount clue: `sessions.py:801–810`, called_by: `__init__`].

### 2. Registering Adapters with `mount()` — Longest-Prefix-First Ordering

The `mount(prefix, adapter)` method (at `sessions.py:801–810`) registers a connection adapter to a given URL prefix [mount docstring: "Registers a connection adapter to a prefix."]. Its implementation is:

```python
def mount(self, prefix, adapter):
    self.adapters[prefix] = adapter
    keys_to_move = [k for k in self.adapters if len(k) < len(prefix)]
    for key in keys_to_move:
        self.adapters[key] = self.adapters.pop(key)
```
[mount source snippet]

After inserting the new prefix–adapter pair, the method identifies every existing key whose length is *shorter* than the newly inserted prefix and re-inserts those keys at the end of the ordered dictionary [mount source snippet: `keys_to_move` loop]. The net effect is that prefixes are maintained in **descending order of length**—the longest (most specific) prefixes appear first. This deliberate ordering is critical because `get_adapter()` performs a first-match scan, so longer prefixes must be checked before shorter ones to ensure the most specific adapter wins.

### 3. Selecting a Transport with `get_adapter()` — First-Match, Case-Insensitive Lookup

When the `Session` needs to dispatch a request, it calls `get_adapter(url)` (at `sessions.py:783–794`) [get_adapter clue: called_by `send`, `Session`]. The method's docstring states it "Returns the appropriate connection adapter for the given URL." [get_adapter docstring]. Its implementation is:

```python
def get_adapter(self, url):
    for prefix, adapter in self.adapters.items():
        if url.lower().startswith(prefix.lower()):
            return adapter
    raise InvalidSchema(f"No connection adapters were found for {url!r}")
```
[get_adapter source snippet]

The method iterates over `self.adapters` in insertion order—which, thanks to `mount()`, is longest-prefix-first [mount source snippet; get_adapter source snippet]. For each entry it performs a **case-insensitive** comparison (`url.lower().startswith(prefix.lower())`) and returns the **first** adapter whose prefix matches the beginning of the URL [get_adapter source snippet]. Because the dictionary is sorted by descending prefix length, this constitutes a longest-prefix-match strategy: a URL like `"https://example.com"` will match `"https://"` before the shorter `"http://"` prefix is ever tested.

### 4. Failure Case: `InvalidSchema`

If no registered prefix matches the URL, `get_adapter()` raises `InvalidSchema` [get_adapter source snippet: `raise InvalidSchema(...)`]. The `InvalidSchema` exception is defined at `exceptions.py:104–105` with the docstring "The URL scheme provided is either invalid or unsupported." [InvalidSchema clue]. This means that any URL whose scheme has not been explicitly mounted (e.g., `"ftp://"`, `"file://"`) will be rejected at adapter-selection time rather than silently failing downstream.

### 5. `send()` as the Integration Point

The `Session.send()` method is the primary caller of `get_adapter()` [get_adapter clue: called_by `send`]. The dispatch flow is:

1. `send()` receives a prepared `PreparedRequest`.
2. It calls `self.get_adapter(url=request.url)` to obtain the appropriate transport adapter for that URL.
3. It delegates the actual network I/O to `adapter.send(request, ...)`, which is the method defined by the adapter's transport implementation.

This two-step indirection—resolve adapter via prefix matching, then call `adapter.send()`—cleanly separates URL-to-transport routing (the `Session`'s responsibility) from the mechanics of making the HTTP connection (the adapter's responsibility) [get_adapter clue; BaseAdapter clue].

### 6. `BaseAdapter` — The Abstract Transport Interface

All transport adapters must conform to the interface defined by `BaseAdapter` (at `adapters.py:114–141`), documented as "The Base Transport Adapter" [BaseAdapter clue]. Its source is:

```python
class BaseAdapter:
    def send(self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None):
        raise NotImplementedError
    def close(self):
        raise NotImplementedError
```
[BaseAdapter source snippet]

Both `send()` and `close()` raise `NotImplementedError`, making `BaseAdapter` an abstract contract [BaseAdapter source snippet]. Concrete adapters (such as `HTTPAdapter`, which provides `build_response` at `adapters.py:337–372` and `request_url` at `adapters.py:524–554`) override these methods to implement actual transport logic [build_response clue; request_url clue]. The `Session` interacts with adapters exclusively through this interface, enabling any custom adapter to be mounted without modifying `Session` internals.

### 7. Lifecycle Management: `close()`

The `Session.close()` method (at `sessions.py:796–799`) is documented as closing "all adapters and as such the session" [close clue]. Its implementation iterates every adapter in the registry and calls its `close()` method:

```python
def close(self):
    for v in self.adapters.values():
        v.close()
```
[close source snippet]

This ensures that all transport-level resources (connection pools, sockets, etc.) held by every mounted adapter are released when the session is torn down [close source snippet; BaseAdapter source snippet: `close` raises `NotImplementedError`].

### 8. Identified Gaps

Several mechanistic details cannot be determined from the available evidence [GAPS clue: type MECHANISTIC]:

- **`build_connection_pool_key_attributes`** — how connection-pool keys are constructed internally is not covered [GAPS: uncovered].
- **`SOCKSProxyManager`** — the SOCKS proxy transport path and its adapter wiring are not described [GAPS: uncovered].
- **`add_headers`** — how transport-level headers are injected by adapters is not visible [GAPS: uncovered].
- **`proxy_headers`** — how proxy-specific headers are generated and attached is not covered [GAPS: uncovered].

These gaps mean that while the *routing* relationship between `Session` and its adapters is fully explained, the internal mechanics of how a selected adapter constructs connections, manages proxy tunnels, and injects transport-layer headers remain outside the scope of the available clues.
