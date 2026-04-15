# Response: blind-requests-rel-2
Date: 2026-04-15

## Answer
- `Session` owns adapter registration and adapter selection. `mount(prefix, adapter)` “Registers a connection adapter to a prefix,” and `get_adapter(url)` “Returns the appropriate connection adapter for the given URL.” [(`mount`, `src/requests/sessions.py:801-810`); (`get_adapter`, `src/requests/sessions.py:783-794`)]
- Because `Session.send()` calls `get_adapter`, transport selection happens as part of session-driven sending. In other words, `Session` chooses the transport adapter before the transport work proceeds. [(`send`, `src/requests/sessions.py:675-750`); (`get_adapter`, `src/requests/sessions.py:783-794`)]
- The adapter interface is formalized in `BaseAdapter`, which is explicitly described as “The Base Transport Adapter.” `HTTPAdapter` is the built-in concrete implementation underneath that interface. [(`BaseAdapter`, `src/requests/adapters.py:114-141`); (`HTTPAdapter`, `src/requests/adapters.py:144-697`)]
- After `Session` selects an adapter, the adapter appears to own the URL-to-connection and response-construction work. `HTTPAdapter` calls `get_connection_with_tls_context`, `proxy_manager_for`, `request_url`, and `build_response`, and `build_response` constructs a `Response`. [(`HTTPAdapter`, `src/requests/adapters.py:144-697`); (`get_connection_with_tls_context`, `src/requests/adapters.py:424-471`); (`request_url`, `src/requests/adapters.py:524-554`); (`build_response`, `src/requests/adapters.py:337-372`)]
- The selection relationship is therefore: `Session` maintains a mapping from prefixes to adapters, `get_adapter(url)` chooses the adapter for a specific URL, and the chosen adapter performs the transport-specific work. [(`mount`, `src/requests/sessions.py:801-810`); (`get_adapter`, `src/requests/sessions.py:783-794`); (`HTTPAdapter`, `src/requests/adapters.py:144-697`)]
- `Session` also manages the adapter lifecycle after selection. Its `close()` method “Closes all adapters and as such the session.” [(`close`, `src/requests/sessions.py:796-799`)]
- If no adapter can handle the URL scheme, the failure surfaces at the session-selection layer: `get_adapter` raises `InvalidSchema`, and `Session` also lists `InvalidSchema` among the exceptions it uses/raises. [(`get_adapter`, `src/requests/sessions.py:783-794`); (`Session`, `src/requests/sessions.py:356-818`); (`InvalidSchema`, `src/requests/exceptions.py:104-105`)]

## What I cannot determine
- I cannot determine the exact prefix-matching algorithm or priority rule used by `get_adapter(url)` beyond the fact that it accumulates over something and returns an adapter for the URL. [(`get_adapter`, `src/requests/sessions.py:783-794`)]
- I cannot determine the default adapters mounted by `Session.__init__`, because the clue says `mount` is called by `__init__`, but the actual constructor body is not included. [(`mount`, `src/requests/sessions.py:801-810`)]
