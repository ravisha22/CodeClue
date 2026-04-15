# v2.2 Response: blind-requests-rel-2
Date: 2026-04-15

## Question

How do `Session` and transport adapters relate to one another when Requests selects a transport for a URL?

## Answer

The clue file reveals a **registry-based adapter selection** pattern where `Session` maintains a collection of transport adapters mapped to URL prefixes, and selects the appropriate adapter at send-time by matching the request URL.

### 1. Transport Adapter Abstraction

The adapter hierarchy is defined in `src/requests/adapters.py`:

- **`BaseAdapter`** (class, `src/requests/adapters.py:114`) — "The Base Transport Adapter." Raises `NotImplementedError`, indicating it defines an abstract interface. Its `send` method (`src/requests/adapters.py:120`) has signature `send(request, stream, timeout, verify, cert...)` and raises `NotImplementedError`.

- **`HTTPAdapter`** (class, `src/requests/adapters.py:144`) — "The built-in HTTP Adapter for urllib3." Extends `BaseAdapter`. This is the concrete implementation that:
  - Calls: `add_headers`, `build_connection_pool_key_attributes`, `build_response`, `cert_verify`, `get_connection_with_tls_context`, `init_poolmanager`, `proxy_headers`, `proxy_manager_for`.
  - Raises: `OSError`, `InvalidURL`, `InvalidProxyURL`, `ConnectionError`.
  - Uses: `Response` (models), `CaseInsensitiveDict` (structures), `InvalidURL` (exceptions), `InvalidProxyURL` (exceptions).

### 2. Session Registers Adapters via `mount`

- **`mount`** (`src/requests/sessions.py:801`) — "Registers a connection adapter to a prefix."
  - `sig: mount(prefix, adapter)`
  - `behavior: ACCUMULATE(loop -> result)` — the ACCUMULATE pattern suggests it iterates over existing entries (likely maintaining sorted order by prefix length).
  - `called_by: __init__, Session` — confirming that `Session.__init__` calls `mount` to register default adapters during session construction.

This means `Session` maintains an internal mapping of URL prefixes (e.g., `"https://"`, `"http://"`) to adapter instances. Users can call `mount` to register custom adapters for specific URL prefixes.

### 3. Session Selects Adapters via `get_adapter`

- **`get_adapter`** (`src/requests/sessions.py:783`) — "Returns the appropriate connection adapter for the given URL."
  - `sig: get_adapter(url)`
  - `behavior: ACCUMULATE(loop -> result)` — it iterates over registered adapters, matching the URL against prefixes.
  - `called_by: send, Session`.
  - `raises: InvalidSchema` — raised when no adapter matches the URL scheme.
  - `uses: InvalidSchema (exceptions)`.

The `ACCUMULATE(loop -> result)` behavior annotation tells us `get_adapter` loops through the registered prefix→adapter pairs. Since `mount` also uses `ACCUMULATE(loop -> result)` and is called from `__init__`, the prefixes are likely ordered (e.g., longest-prefix-first) so that more specific prefixes match before general ones.

### 4. Session.send() Ties It Together

- **`send`** (`src/requests/sessions.py:675`) — "Send a given PreparedRequest."
  - `calls: get, get_adapter, resolve_redirects`.
  - `called_by: request, Session, resolve_redirects, SessionRedirectMixin`.

The flow is: `send` receives a `PreparedRequest`, calls `get_adapter(url)` to find the matching transport adapter, then delegates the actual network I/O to that adapter's `send` method.

### 5. The Adapter Performs the Request and Builds the Response

The selected `HTTPAdapter` performs the actual HTTP call:

- **`HTTPAdapter.send`** (`src/requests/adapters.py:591`) — "Sends PreparedRequest object."
  - `sig: send(request, stream, timeout, verify, cert...)`
  - Raises: `InvalidURL`, `ConnectionError`, `ProxyError`, `ValueError`.
  - Uses: `TimeoutSauce` (urllib3.util), `ConnectionError` (exceptions), `ProxyError` (exceptions).

- **`build_response`** (`src/requests/adapters.py:337`) — "Builds a :class:`Response <requests.Response>` object from a urllib3" response.
  - `uses: Response (models), CaseInsensitiveDict (structures)`.

Additional adapter methods involved in URL and connection handling:
- **`request_url`** (`src/requests/adapters.py:524`) — "Obtain the url to use when making the final request." `called_by: HTTPAdapter`.
- **`get_connection_with_tls_context`** (`src/requests/adapters.py:424`) — "Returns a urllib3 connection for the given request and TLS settings." Branches on proxy presence. Calls `build_connection_pool_key_attributes`, `proxy_manager_for`.
- **`cert_verify`** (`src/requests/adapters.py:281`) — "Verify a SSL certificate." Branches based on URL scheme and verify settings.
- **`init_poolmanager`** (`src/requests/adapters.py:217`) — "Initializes a urllib3 PoolManager."
- **`proxy_manager_for`** (`src/requests/adapters.py:243`) — "Return urllib3 ProxyManager for the given proxy."

### 6. Session.close() Cleans Up All Adapters

- **`close`** (`src/requests/sessions.py:796`) — "Closes all adapters and as such the session."
  - `behavior: ACCUMULATE(loop -> result)` — iterates over all registered adapters and closes each.
  - `called_by: __exit__, Session, resolve_redirects, SessionRedirectMixin`.

### 7. Error Handling for Unmatched Schemes

- **`InvalidSchema`** (`src/requests/exceptions.py:104`) — "The URL scheme provided is either invalid or unsupported." Extends `RequestException`, `ValueError`.

When `get_adapter` cannot find a matching prefix for the URL, it raises `InvalidSchema` (`get_adapter` at `src/requests/sessions.py:783`, raises `InvalidSchema`; `Session` at `src/requests/sessions.py:356`, raises `InvalidSchema`).

### Pipeline Summary

```
Session.__init__()
  └─> mount("https://", HTTPAdapter())   [sessions.py:801]
  └─> mount("http://", HTTPAdapter())

Session.send(prepared_request)            [sessions.py:675]
  └─> get_adapter(url)                   [sessions.py:783]
        └─> loops over prefix→adapter map
        └─> raises InvalidSchema if no match
  └─> adapter.send(request, ...)          [adapters.py:591]
        ├─> get_connection_with_tls_context()  [adapters.py:424]
        ├─> request_url()                 [adapters.py:524]
        ├─> cert_verify()                 [adapters.py:281]
        └─> build_response()             [adapters.py:337]
              └─> returns Response

Session.close()                           [sessions.py:796]
  └─> loops over all adapters, closes each
```

### What Cannot Be Determined

The clue file does not reveal the exact data structure used to store the prefix→adapter mapping (e.g., whether it is an `OrderedDict`, a list of tuples, etc.), nor the precise prefix-matching algorithm beyond the `ACCUMULATE(loop -> result)` annotation. The default prefixes registered in `__init__` are not explicitly listed but can be inferred as the standard URL schemes (`http://`, `https://`) based on `HTTPAdapter`'s name and the `InvalidSchema` exception for unrecognized schemes.
