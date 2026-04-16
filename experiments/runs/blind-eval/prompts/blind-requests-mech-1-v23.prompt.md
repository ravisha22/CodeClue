# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: blind-requests-mech-1

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.

--- CLUE FILE (File 1) ---
=CC v2.1 requests@HEAD 36mod 757sym
? When session defaults, per-call options, and environment-derived settings all interact in Requests, what precedence rules does the implementation follow?


-- TREE
docs/  (2 files)
  _themes/
src/  (18 files)
  requests/
tests/  (15 files)
  testserver/
setup.py

-- INDEX
docs/_themes/flask_theme_support.py              86L  FlaskyStyle
docs/conf.py                                    385L  
setup.py                                          9L  
src/requests/__init__.py                        183L  check_compatibility
src/requests/__version__.py                      14L  
src/requests/_internal_utils.py                  51L  to_native_string, unicode_is_ascii
src/requests/adapters.py                        697L  close, send, BaseAdapter, add_headers, build_connection_pool_key_attributes
src/requests/api.py                             157L  delete, get, head, options, patch
src/requests/auth.py                            314L  AuthBase, HTTPBasicAuth, md5_utf8, sha256_utf8, sha512_utf8
src/requests/certs.py                            18L  
src/requests/compat.py                          106L  
src/requests/cookies.py                         561L  CookieConflictError, add_header, add_unredirected_header, get_full_url, get_header
src/requests/exceptions.py                      152L  ChunkedEncodingError, ConnectTimeout, ConnectionError, ContentDecodingError, FileModeWarning
src/requests/help.py                            131L  info, main
src/requests/hooks.py                            34L  default_hooks, dispatch_hook
src/requests/models.py                         1041L  copy, prepare, prepare_auth, prepare_body, prepare_content_length
src/requests/packages.py                         23L  
src/requests/sessions.py                        833L  close, delete, get, get_adapter, head
src/requests/status_codes.py                    128L  doc
src/requests/structures.py                       99L  copy, lower_items, CaseInsensitiveDict, get, LookupDict
  ...and 16 more modules

-- SYM
request                             M src/requests/sessions.py:502    Constructs a :class:`Request <Request>`, prepar...
get                                 M src/requests/sessions.py:595    Sends a GET request.
merge_setting                       M src/requests/sessions.py:62     Determines appropriate setting for a given requ...
request                             M src/requests/api.py:14     Constructs and sends a :class:`Request <Request>`.
CookieConflictError                 C src/requests/cookies.py:170    There are two cookies that meet the criteria sp...
_find_no_duplicates                 M src/requests/cookies.py:386    Both ``__get_item__`` and ``get`` call this fun...
update                              M src/requests/cookies.py:358    Updates this jar with cookies from another Cook...
send                                M src/requests/sessions.py:675    Send a given PreparedRequest.
set_cookie                          M src/requests/cookies.py:349    function set_cookie
copy                                M src/requests/cookies.py:428    Return a copy of this RequestsCookieJar.
merge_environment_settings          M src/requests/sessions.py:752    Check the environment and merge it with some se...
prepare_request                     M src/requests/sessions.py:459    Constructs a :class:`PreparedRequest <PreparedR...
generate                            M src/requests/models.py:818    function generate
get                                 M src/requests/cookies.py:194    Dict-like get() that also supports optional dom...
get_host                            M src/requests/cookies.py:43     function get_host
iter_content                        M src/requests/models.py:801    Iterates over the response data.
create_cookie                       M src/requests/cookies.py:455    Make a cookie from underspecified parameters.
set                                 M src/requests/cookies.py:206    Dict-like set() that also supports optional dom...
lower_items                         M src/requests/structures.py:63     Like iteritems(), but with all lowercase keys.
resolve_redirects                   M src/requests/sessions.py:160    Receives a Response.
RequestsCookieJar                   C src/requests/cookies.py:176    Compatibility class; is a http.cookiejar.Cookie...
_basic_auth_str                     M src/requests/auth.py:25     Returns a Basic Auth string.
unquote_header_value                M src/requests/utils.py:432    Unquotes a header value.
remove_cookie_by_name               M src/requests/cookies.py:151    Unsets a cookie by name, by default over all do...
should_bypass_proxies               M src/requests/utils.py:752    Returns whether we should bypass proxies or not.
_implementation                     M src/requests/help.py:34     Return a dict with the Python implementation an...
_parse_content_type_header          M src/requests/utils.py:504    Returns content type and parameters from given ...
prepare_content_length              M src/requests/models.py:574    Prepare Content-Length header based on request ...
register_hook                       M src/requests/models.py:209    Properly register a hook.
get_policy                          M src/requests/cookies.py:435    Return the CookiePolicy instance used.
close                               M src/requests/sessions.py:796    Closes all adapters and as such the session
proxy_manager_for                   M src/requests/adapters.py:243    Return urllib3 ProxyManager for the given proxy.
build_digest_header                 M src/requests/auth.py:126    :rtype: str
PreparedRequest                     C src/requests/models.py:315    The fully mutable :class:`PreparedRequest <Prep...
should_strip_auth                   M src/requests/sessions.py:128    Decide whether Authorization header should be r...
_urllib3_request_context            M src/requests/adapters.py:77     function _urllib3_request_context
CaseInsensitiveDict                 C src/requests/structures.py:13     A case-insensitive ``dict``-like object.
getheaders                          M src/requests/cookies.py:120    function getheaders
dotted_netmask                      M src/requests/utils.py:684    Converts mask from /xx format to xxx.xxx.xxx.xxx
proxy_bypass_registry               M src/requests/utils.py:76     function proxy_bypass_registry
get_adapter                         M src/requests/sessions.py:783    Returns the appropriate connection adapter for ...
proxy_headers                       M src/requests/adapters.py:570    Returns a dictionary of the headers to add to a...
SOCKSProxyManager                   M src/requests/adapters.py:63     function SOCKSProxyManager
close                               M src/requests/models.py:1030   Releases the connection back to the pool.
get_origin_req_host                 M src/requests/cookies.py:46     function get_origin_req_host
is_unverifiable                     M src/requests/cookies.py:69     function is_unverifiable
_encode_params                      M src/requests/models.py:109    Encode parameters in a piece of data.
merge_hooks                         M src/requests/sessions.py:92     Properly merges both requests and session hooks.
get_redirect_target                 M src/requests/sessions.py:108    Receives a Response.
init_poolmanager                    M src/requests/adapters.py:217    Initializes a urllib3 PoolManager.
raise_for_status                    M src/requests/models.py:1001   Raises :class:`HTTPError`, if one occurred.
iteritems                           M src/requests/cookies.py:259    Dict-like iteritems() that returns an iterator ...
iterkeys                            M src/requests/cookies.py:225    Dict-like iterkeys() that returns an iterator o...
itervalues                          M src/requests/cookies.py:242    Dict-like itervalues() that returns an iterator...
mount                               M src/requests/sessions.py:801    Registers a connection adapter to a prefix.
__reduce__                          M src/requests/exceptions.py:45     The __reduce__ method called when pickling the ...
info                                M src/requests/help.py:66     Generate information for a bug report.
Session                             C src/requests/sessions.py:356    A Requests session.
doc                                 M src/requests/status_codes.py:116    function doc
get                                 M src/requests/structures.py:98     function get
_validate_header_part               M src/requests/utils.py:1032   function _validate_header_part
default_user_agent                  M src/requests/utils.py:878    Return a string representing the default user a...
get_encoding_from_headers           M src/requests/utils.py:526    Returns encodings from given HTTP Header Dict.
unquote_unreserved                  M src/requests/utils.py:623    Un-escape any percent-escape sequences in a URI...
MockRequest                         C src/requests/cookies.py:23     Wraps a `requests.Request` to mimic a `urllib2....
morsel_to_cookie                    M src/requests/cookies.py:492    Convert a Morsel object into a Cookie containin...
_get_idna_encoded_host              M src/requests/models.py:402    function _get_idna_encoded_host
build_connection_pool_key_attributes M src/requests/adapters.py:374    Build the PoolKey attributes used by urllib3 to...
  ...and 217 more symbols

-- FOCUS
merge_environment_settings (src/requests/sessions.py:752-781)
  Check the environment and merge it with some settings.
  sig: merge_environment_settings(url, proxies, stream, verify, cert)
  calls: get, merge_setting
  called_by: request, Session

Session (src/requests/sessions.py:356-818)
  A Requests session.
  extends: SessionRedirectMixin
  imports: adapters, auth, compat, cookies, exceptions
  calls: close, get, get_adapter, merge_environment_settings, mount, prepare_request, request, send
  called_by: session
  raises: InvalidSchema, ValueError
  uses: InvalidSchema (exceptions), PreparedRequest (models), RequestsCookieJar (cookies), Request (models)

session (src/requests/sessions.py:821-833)
  Returns a :class:`Session` for context-management.
  behavior: DELEGATE(Session -> result)
  calls: Session

SessionRedirectMixin (src/requests/sessions.py:107-353)
  imports: adapters, auth, compat, cookies, exceptions
  calls: close, get, send, get_redirect_target, rebuild_auth, rebuild_method, rebuild_proxies, should_strip_auth
  raises: TooManyRedirects

__call__ (src/requests/auth.py:72-73)
  sig: __call__(r)
  raises: NotImplementedError

__call__ (src/requests/auth.py:285-303)
  sig: __call__(r)

__call__ (src/requests/auth.py:102-104)
  sig: __call__(r)

__call__ (src/requests/auth.py:94-96)
  sig: __call__(r)

_implementation (src/requests/help.py:34-63)
  Return a dict with the Python implementation and version.
  called_by: info

init_per_thread_state (src/requests/auth.py:116-124)
  called_by: HTTPDigestAuth

options (src/requests/api.py:76-85)
  Sends an OPTIONS request.
  sig: options(url)
  behavior: DELEGATE(request -> result)
  calls: request

options (src/requests/sessions.py:606-615)
  Sends a OPTIONS request.
  sig: options(url)
  behavior: DELEGATE(request -> result)
  calls: request

RequestsWarning (src/requests/exceptions.py:143-144)
  Base warning for Requests.
  extends: Warning
  imports: urllib3.exceptions, compat

RequestsCookieJar (src/requests/cookies.py:176-437)
  Compatibility class; is a http.cookiejar.CookieJar, but exposes a dict
  extends: CookieJar, MutableMapping
  imports: calendar, copy, compat, threading, dummy_threading
  calls: CookieConflictError, __contains__, _find_no_duplicates, copy, get, get_policy, iteritems, iterkeys
  called_by: copy, cookiejar_from_dict
  raises: KeyError, CookieConflictError

merge_hooks (src/requests/sessions.py:92-104)
  Properly merges both requests and session hooks.
  sig: merge_hooks(request_hooks, session_hooks, dict_class)
  calls: get, merge_setting
  called_by: prepare_request, Session

MockRequest (src/requests/cookies.py:23-100)
  Wraps a `requests.Request` to mimic a `urllib2.Request`.
  imports: calendar, copy, compat, threading, dummy_threading
  calls: get_host, get_origin_req_host, is_unverifiable, get
  called_by: extract_cookies_to_jar, get_cookie_header
  raises: NotImplementedError

copy (src/requests/cookies.py:428-433)
  Return a copy of this RequestsCookieJar.
  calls: get_policy, update, RequestsCookieJar
  called_by: __getstate__, update, RequestsCookieJar, _copy_cookie_jar

_find_no_duplicates (src/requests/cookies.py:386-413)
  Both ``__get_item__`` and ``get`` call this function: it's never
  sig: _find_no_duplicates(name, domain, path)
  behavior: ACCUMULATE(iter(self) loop -> result, raises CookieConflictError)
  calls: CookieConflictError
  called_by: __getitem__, get, RequestsCookieJar
  raises: KeyError, CookieConflictError

close (src/requests/sessions.py:796-799)
  Closes all adapters and as such the session
  behavior: ACCUMULATE(self.adapters.values(... -> result)
  called_by: __exit__, Session, resolve_redirects, SessionRedirectMixin

get_connection_with_tls_context (src/requests/adapters.py:424-471)
  Returns a urllib3 connection for the given request and TLS settings.
  sig: get_connection_with_tls_context(request, verify, proxies, cert)
  behavior: BRANCH(proxy -> raise InvalidProxyURL..., else -> self.poolmanager.conn...)
  calls: build_connection_pool_key_attributes, proxy_manager_for
  called_by: HTTPAdapter
  raises: InvalidURL, InvalidProxyURL
  uses: InvalidURL (exceptions), InvalidProxyURL (exceptions)

FileModeWarning (src/requests/exceptions.py:147-148)
  A file was opened in text mode, but Requests determined its binary length.
  extends: RequestsWarning, DeprecationWarning
  imports: urllib3.exceptions, compat

UnrewindableBodyError (src/requests/exceptions.py:136-137)
  Requests encountered an error when trying to rewind a body.
  extends: RequestException
  imports: urllib3.exceptions, compat

_find (src/requests/cookies.py:366-384)
  Requests uses this method internally to get cookie values.
  sig: _find(name, domain, path)
  behavior: ACCUMULATE(iter(self) loop -> result)
  raises: KeyError

build_response (src/requests/adapters.py:337-372)
  Builds a :class:`Response <requests.Response>` object from a urllib3
  sig: build_response(req, resp)
  behavior: BRANCH(isinstance(req.url, bytes) -> req.url.decode('utf-8'), else -> req.url)
  called_by: HTTPAdapter
  uses: Response (models), CaseInsensitiveDict (structures)

default_headers (src/requests/utils.py:887-898)
  :rtype: requests.structures.CaseInsensitiveDict
  behavior: DELEGATE(CaseInsensitiveDict -> result)
  calls: default_user_agent
  uses: CaseInsensitiveDict (structures)

get_environ_proxies (src/requests/utils.py:813-822)
  Return a dict of environment proxies.
  sig: get_environ_proxies(url, no_proxy)
  behavior: BRANCH(should_bypass_proxies(url, no... -> return {}, else -> return getprox...)
  calls: should_bypass_proxies
  called_by: resolve_proxies

get_netrc_auth (src/requests/utils.py:206-247)
  Returns the Requests tuple auth for a given url from netrc.
  sig: get_netrc_auth(url, raise_errors)
  behavior: BRANCH(netrc_file is not None -> (netrc_file,), else -> (f'~/{f}' for f in N...)

set_environ (src/requests/utils.py:731-749)
  Set the environment variable 'env_name' to 'value'
  sig: set_environ(env_name, value)
  called_by: should_bypass_proxies

RequestsDependencyWarning (src/requests/exceptions.py:151-152)
  An imported dependency doesn't match the expected version range.
  extends: RequestsWarning
  imports: urllib3.exceptions, compat

get (src/requests/sessions.py:595-604)
  Sends a GET request.
  sig: get(url)
  behavior: DELEGATE(request -> result)
  calls: request
  called_by: merge_environment_settings, send, Session, should_strip_auth, SessionRedirectMixin, merge_hooks

HTTPError (src/requests/exceptions.py:56-57)
  An HTTP error occurred.
  extends: RequestException
  imports: urllib3.exceptions, compat

is_permanent_redirect (src/requests/models.py:779-784)
  True if this Response one of the permanent versions of redirect.

super_len (src/requests/utils.py:135-203)
  sig: super_len(o)

request (src/requests/sessions.py:502-593)
  Constructs a :class:`Request <Request>`, prepares it and sends it.
  sig: request(method, url, params, data, headers...)
  calls: merge_environment_settings, prepare_request, send
  called_by: delete, get, head, options, patch, post, put, Session
  uses: Request (models)

merge_setting (src/requests/sessions.py:62-89)
  Determines appropriate setting for a given request, taking into account
  sig: merge_setting(request_setting, session_setting, dict_class)
  behavior: ACCUMULATE(none_keys loop -> result)
  called_by: merge_environment_settings, prepare_request, Session, merge_hooks

prepare_request (src/requests/sessions.py:459-500)
  Constructs a :class:`PreparedRequest <PreparedRequest>` for
  sig: prepare_request(request)
  calls: merge_hooks, merge_setting
  called_by: request, Session
  uses: PreparedRequest (models), RequestsCookieJar (cookies)

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 24 with behavior annotations
uncovered: address_in_network, build_digest_header, cert_verify, delete
drill: src/requests/sessions.py (~30 lines, merge_environment_settings)
drill: src/requests/sessions.py (~12 lines, merge_hooks)
drill: src/requests/help.py (~33 lines, _implementation)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## merge_hooks  (src/requests/sessions.py L92-104)
```
def merge_hooks(request_hooks, session_hooks, dict_class=OrderedDict):
    """Properly merges both requests and session hooks.

    This is necessary because when request_hooks == {'response': []}, the
    merge breaks Session hooks entirely.
    """
    if session_hooks is None or session_hooks.get("response") == []:
        return request_hooks

    if request_hooks is None or request_hooks.get("response") == []:
        return session_hooks

    return merge_setting(request_hooks, session_hooks, dict_class)
```

## merge_environment_settings  (src/requests/sessions.py L752-781)
```
    def merge_environment_settings(self, url, proxies, stream, verify, cert):
        """
        Check the environment and merge it with some settings.

        :rtype: dict
        """
        # Gather clues from the surrounding environment.
        if self.trust_env:
            # Set environment's proxies.
            no_proxy = proxies.get("no_proxy") if proxies is not None else None
            env_proxies = get_environ_proxies(url, no_proxy=no_proxy)
            for k, v in env_proxies.items():
                proxies.setdefault(k, v)

            # Look for requests environment configuration
            # and be compatible with cURL.
            if verify is True or verify is None:
                verify = (
                    os.environ.get("REQUESTS_CA_BUNDLE")
                    or os.environ.get("CURL_CA_BUNDLE")
                    or verify
                )

        # Merge all the kwargs.
        proxies = merge_setting(proxies, self.proxies)
        stream = merge_setting(stream, self.stream)
        verify = merge_setting(verify, self.verify)
        cert = merge_setting(cert, self.cert)

        return {"proxies": proxies, "stream": stream, "verify": verify, "cert": cert}
```

## _implementation  (src/requests/help.py L34-63)
```
def _implementation():
    """Return a dict with the Python implementation and version.

    Provide both the name and the version of the Python implementation
    currently running. For example, on CPython 3.10.3 it will return
    {'name': 'CPython', 'version': '3.10.3'}.

    This function works best on CPython and PyPy: in particular, it probably
    doesn't work for Jython or IronPython. Future investigation should be done
    to work out the correct shape of the code for those platforms.
    """
    implementation = platform.python_implementation()

    if implementation == "CPython":
        implementation_version = platform.python_version()
    elif implementation == "PyPy":
        pypy = sys.pypy_version_info
        implementation_version = f"{pypy.major}.{pypy.minor}.{pypy.micro}"
        if sys.pypy_version_info.releaselevel != "final":
            implementation_version = "".join(
                [implementation_version, sys.pypy_version_info.releaselevel]
            )
    elif implementation == "Jython":
        implementation_version = platform.python_version()  # Complete Guess
    elif implementation == "IronPython":
        implementation_version = platform.python_version()  # Complete Guess
    else:
        implementation_version = "Unknown"

    return {"name": implementation, "version": implementation_version}
```

## get  (src/requests/structures.py L98-99)
```
    def get(self, key, default=None):
        return self.__dict__.get(key, default)
```

## merge_setting  (src/requests/sessions.py L62-89)
```
def merge_setting(request_setting, session_setting, dict_class=OrderedDict):
    """Determines appropriate setting for a given request, taking into account
    the explicit setting on that request, and the setting in the session. If a
    setting is a dictionary, they will be merged together using `dict_class`
    """

    if session_setting is None:
        return request_setting

    if request_setting is None:
        return session_setting

    # Bypass if not a dictionary (e.g. verify)
    if not (
        isinstance(session_setting, Mapping) and isinstance(request_setting, Mapping)
    ):
        return request_setting

    merged_setting = dict_class(to_key_val_list(session_setting))
    merged_setting.update(to_key_val_list(request_setting))

    # Remove keys that are set to None. Extract keys first to avoid altering
    # the dictionary during iteration.
    none_keys = [k for (k, v) in merged_setting.items() if v is None]
    for key in none_keys:
        del merged_setting[key]

    return merged_setting
```

## __enter__  (tests/testserver/server.py L117-121)
```
    def __enter__(self):
        self.start()
        if not self.ready_event.wait(self.WAIT_EVENT_TIMEOUT):
            raise RuntimeError("Timeout waiting for server to be ready.")
        return self.host, self.port
```

## __exit__  (tests/testserver/server.py L123-135)
```
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.stop_event.wait(self.WAIT_EVENT_TIMEOUT)
        else:
            if self.wait_to_close_event:
                # avoid server from waiting for event timeouts
                # if an exception is found in the main thread
                self.wait_to_close_event.set()

        # ensure server thread doesn't get stuck waiting for connections
        self._close_server_sock_ignore_errors()
        self.join()
        return False  # allow exceptions to propagate
```

## __getstate__  (src/requests/sessions.py L812-814)
```
    def __getstate__(self):
        state = {attr: getattr(self, attr, None) for attr in self.__attrs__}
        return state
```

## __init__  (tests/testserver/server.py L139-169)
```
    def __init__(
        self,
        *,
        handler=None,
        host="localhost",
        port=0,
        requests_to_handle=1,
        wait_to_close_event=None,
        cert_chain=None,
        keyfile=None,
        mutual_tls=False,
        cacert=None,
    ):
        super().__init__(
            handler=handler,
            host=host,
            port=port,
            requests_to_handle=requests_to_handle,
            wait_to_close_event=wait_to_close_event,
        )
        self.cert_chain = cert_chain
        self.keyfile = keyfile
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.ssl_context.load_cert_chain(self.cert_chain, keyfile=self.keyfile)
        self.mutual_tls = mutual_tls
        self.cacert = cacert
        if mutual_tls:
            # For simplicity, we're going to assume that the client cert is
            # issued by the same CA as our Server certificate
            self.ssl_context.verify_mode = ssl.CERT_OPTIONAL
            self.ssl_context.load_verify_locations(self.cacert)
```

## __setstate__  (src/requests/sessions.py L816-818)
```
    def __setstate__(self, state):
        for attr, value in state.items():
            setattr(self, attr, value)
```

## close  (src/requests/sessions.py L796-799)
```
    def close(self):
        """Closes all adapters and as such the session"""
        for v in self.adapters.values():
            v.close()
```

## delete  (src/requests/sessions.py L665-673)
```
    def delete(self, url, **kwargs):
        r"""Sends a DELETE request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        return self.request("DELETE", url, **kwargs)
```

## get_adapter  (src/requests/sessions.py L783-794)
```
    def get_adapter(self, url):
        """
        Returns the appropriate connection adapter for the given URL.

        :rtype: requests.adapters.BaseAdapter
        """
        for prefix, adapter in self.adapters.items():
            if url.lower().startswith(prefix.lower()):
                return adapter

        # Nothing matches :-/
        raise InvalidSchema(f"No connection adapters were found for {url!r}")
```

## head  (src/requests/sessions.py L617-626)
```
    def head(self, url, **kwargs):
        r"""Sends a HEAD request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        kwargs.setdefault("allow_redirects", False)
        return self.request("HEAD", url, **kwargs)
```

## mount  (src/requests/sessions.py L801-810)
```
    def mount(self, prefix, adapter):
        """Registers a connection adapter to a prefix.

        Adapters are sorted in descending order by prefix length.
        """
        self.adapters[prefix] = adapter
        keys_to_move = [k for k in self.adapters if len(k) < len(prefix)]

        for key in keys_to_move:
            self.adapters[key] = self.adapters.pop(key)
```

## options  (src/requests/sessions.py L606-615)
```
    def options(self, url, **kwargs):
        r"""Sends a OPTIONS request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        kwargs.setdefault("allow_redirects", True)
        return self.request("OPTIONS", url, **kwargs)
```

## patch  (src/requests/sessions.py L653-663)
```
    def patch(self, url, data=None, **kwargs):
        r"""Sends a PATCH request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        return self.request("PATCH", url, data=data, **kwargs)
```

## post  (src/requests/sessions.py L628-639)
```
    def post(self, url, data=None, json=None, **kwargs):
        r"""Sends a POST request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        return self.request("POST", url, data=data, json=json, **kwargs)
```

## prepare_request  (src/requests/sessions.py L459-500)
```
    def prepare_request(self, request):
        """Constructs a :class:`PreparedRequest <PreparedRequest>` for
        transmission and returns it. The :class:`PreparedRequest` has settings
        merged from the :class:`Request <Request>` instance and those of the
        :class:`Session`.

        :param request: :class:`Request` instance to prepare with this
            session's settings.
        :rtype: requests.PreparedRequest
        """
        cookies = request.cookies or {}

        # Bootstrap CookieJar.
        if not isinstance(cookies, cookielib.CookieJar):
            cookies = cookiejar_from_dict(cookies)

        # Merge with session cookies
        merged_cookies = merge_cookies(
            merge_cookies(RequestsCookieJar(), self.cookies), cookies
        )

        # Set environment's basic authentication if not explicitly set.
        auth = request.auth
        if self.trust_env and not auth and not self.auth:
            auth = get_netrc_auth(request.url)

        p = PreparedRequest()
        p.prepare(
            method=request.method.upper(),
            url=request.url,
            files=request.files,
            data=request.data,
            json=request.json,
            headers=merge_setting(
                request.headers, self.headers, dict_class=CaseInsensitiveDict
            ),
            params=merge_setting(request.params, self.params),
            auth=merge_setting(auth, self.auth),
            cookies=merged_cookies,
            hooks=merge_hooks(request.hooks, self.hooks),
        )
        return p
```

## put  (src/requests/sessions.py L641-651)
```
    def put(self, url, data=None, **kwargs):
        r"""Sends a PUT request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        return self.request("PUT", url, data=data, **kwargs)
```

## request  (src/requests/sessions.py L502-593)
```
    def request(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
    ):
        """Constructs a :class:`Request <Request>`, prepares it and sends it.
        Returns :class:`Response <Response>` object.

        :param method: method for the new :class:`Request` object.
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary or bytes to be sent in the query
... (truncated)
```
--- END SOURCE SNIPPETS ---

QUESTION: When session defaults, per-call options, and environment-derived settings all interact in Requests, what precedence rules does the implementation follow?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
