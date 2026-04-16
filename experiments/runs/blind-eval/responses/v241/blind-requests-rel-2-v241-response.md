# v2.4.1 Response: blind-requests-rel-2
Date: 2026-04-16

## `Session` owns adapter selection; adapters own transport execution

The prompt shows a clean division of responsibility between `Session` and transport adapters.

**`Session` is the coordinator.** Its FOCUS entry says `Session` calls `get_adapter`, `mount`, `request`, `send`, and `close`, so adapter management is part of the session object rather than a separate global registry (`Session`, `src/requests/sessions.py:356-818`). The SYM entry for `mount` says it “Registers a connection adapter to a prefix,” which confirms that the session stores adapters under URL-prefix keys (`mount`, `src/requests/sessions.py:801`).

**Adapter selection happens in `get_adapter(url)`.** The FOCUS entry for `get_adapter` says it “Returns the appropriate connection adapter for the given URL,” has behavior `ACCUMULATE(self.adapters.items()... -> result)`, is `called_by: send, Session`, and raises `InvalidSchema` if no suitable adapter exists (`get_adapter`, `src/requests/sessions.py:783-794`). From that, the strongest supported claim is that `Session` walks its registered adapters in `self.adapters.items()` and returns the first one that counts as appropriate for the URL (`get_adapter`, `src/requests/sessions.py:783-794`).

**The transport side is abstracted behind `BaseAdapter`.** `BaseAdapter` is explicitly “The Base Transport Adapter” and raises `NotImplementedError`, so it defines the contract but not the implementation (`BaseAdapter`, `src/requests/adapters.py:114-141`). The INDEX and SYM entries show that `adapters.py` also owns `send`, `add_headers`, `build_connection_pool_key_attributes`, and `proxy_manager_for`, which indicates that concrete adapters encapsulate transport details (`src/requests/adapters.py` in INDEX; SYM entries in `adapters.py`).

**Concrete adapters produce model responses.** Even though the prompt does not include a full `HTTPAdapter` FOCUS entry here, it does include `build_response`, which is `called_by: HTTPAdapter` and “Builds a `Response <requests.Response>` object from a urllib3 response” (`build_response`, `src/requests/adapters.py:337-372`). That ties the adapter layer back into the model layer: the selected adapter performs transport work and then converts the transport response into a `Response` object (`build_response`, `src/requests/adapters.py:337-372`).

**Lifecycle ownership also stays with `Session`.** `close` on `Session` “Closes all adapters and as such the session,” with behavior `ACCUMULATE(self.adapters.values(... -> result)`; the source snippet confirms it loops over `self.adapters.values()` and calls `v.close()` on each one (`close`, `src/requests/sessions.py:796-799`; source snippet `close`, `src/requests/sessions.py L796-799`).

In short, the supported relationship is: **`Session` maintains and selects from a prefix-registered adapter set; `get_adapter` chooses the adapter for a URL; the chosen adapter performs transport work and uses adapter-side helpers such as `build_response`; and the session later closes all adapters it owns** (`Session`, `get_adapter`, `mount`, `close`, `BaseAdapter`, `build_response`).

**What Cannot Be Determined**

- The exact matching rule inside `get_adapter` is not shown beyond “iterate `self.adapters.items()` and return the appropriate adapter,” so longest-prefix behavior or case-normalization cannot be claimed from this prompt.
- The default adapters installed by `Session.__init__` are not shown.
- The full behavior of concrete adapters such as `HTTPAdapter.send` is not included in this specific prompt; only the abstract `BaseAdapter` and the adapter-side `build_response` hook are directly supported.
- `proxy_manager_for` is listed in GAPS as uncovered, so proxy-specific transport selection details cannot be reconstructed here (GAPS).
