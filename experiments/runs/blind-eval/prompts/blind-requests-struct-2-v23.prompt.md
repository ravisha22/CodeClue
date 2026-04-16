# Blind Evaluation Prompt - MRLF v2.1
# Task: blind-requests-struct-2

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

--- CLUE FILE START ---
=CC v2.1 requests@HEAD 36mod 757sym
? How do the Requests API docs divide the library into public layers, and which kinds of objects appear in each layer?


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
RequestsWarning (src/requests/exceptions.py:143-144)
  Base warning for Requests.
  extends: Warning
  imports: urllib3.exceptions, compat

Session (src/requests/sessions.py:356-818)
  A Requests session.
  extends: SessionRedirectMixin
  imports: adapters, auth, compat, cookies, exceptions
  calls: close, get, get_adapter, merge_environment_settings, mount, prepare_request, request, send
  called_by: session
  raises: InvalidSchema, ValueError
  uses: InvalidSchema (exceptions), PreparedRequest (models), RequestsCookieJar (cookies), Request (models)

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

FileModeWarning (src/requests/exceptions.py:147-148)
  A file was opened in text mode, but Requests determined its binary length.
  extends: RequestsWarning, DeprecationWarning
  imports: urllib3.exceptions, compat

UnrewindableBodyError (src/requests/exceptions.py:136-137)
  Requests encountered an error when trying to rewind a body.
  extends: RequestException
  imports: urllib3.exceptions, compat

__init__ (src/requests/exceptions.py:18-25)
  Initialize RequestException with `request` and `response` objects.

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

get_netrc_auth (src/requests/utils.py:206-247)
  Returns the Requests tuple auth for a given url from netrc.
  sig: get_netrc_auth(url, raise_errors)
  behavior: BRANCH(netrc_file is not None -> (netrc_file,), else -> (f'~/{f}' for f in N...)

RequestsCookieJar (src/requests/cookies.py:176-437)
  Compatibility class; is a http.cookiejar.CookieJar, but exposes a dict
  extends: CookieJar, MutableMapping
  imports: calendar, copy, compat, threading, dummy_threading
  calls: CookieConflictError, __contains__, _find_no_duplicates, copy, get, get_policy, iteritems, iterkeys
  called_by: copy, cookiejar_from_dict
  raises: KeyError, CookieConflictError

RequestsDependencyWarning (src/requests/exceptions.py:151-152)
  An imported dependency doesn't match the expected version range.
  extends: RequestsWarning
  imports: urllib3.exceptions, compat

request (src/requests/api.py:14-59)
  Constructs and sends a :class:`Request <Request>`.
  sig: request(method, url)
  called_by: delete, get, head, options, patch, post, put

delete (src/requests/api.py:148-157)
  Sends a DELETE request.
  sig: delete(url)
  behavior: DELEGATE(request -> result)
  calls: request

get (src/requests/api.py:62-73)
  Sends a GET request.
  sig: get(url, params)
  behavior: DELEGATE(request -> result)
  calls: request

head (src/requests/api.py:88-100)
  Sends a HEAD request.
  sig: head(url)
  behavior: DELEGATE(request -> result)
  calls: request

options (src/requests/api.py:76-85)
  Sends an OPTIONS request.
  sig: options(url)
  behavior: DELEGATE(request -> result)
  calls: request

patch (src/requests/api.py:133-145)
  Sends a PATCH request.
  sig: patch(url, data)
  behavior: DELEGATE(request -> result)
  calls: request

post (src/requests/api.py:103-115)
  Sends a POST request.
  sig: post(url, data, json)
  behavior: DELEGATE(request -> result)
  calls: request

put (src/requests/api.py:118-130)
  Sends a PUT request.
  sig: put(url, data)
  behavior: DELEGATE(request -> result)
  calls: request

prepare_request (src/requests/sessions.py:459-500)
  Constructs a :class:`PreparedRequest <PreparedRequest>` for
  sig: prepare_request(request)
  calls: merge_hooks, merge_setting
  called_by: request, Session
  uses: PreparedRequest (models), RequestsCookieJar (cookies)

get (src/requests/sessions.py:595-604)
  Sends a GET request.
  sig: get(url)
  behavior: DELEGATE(request -> result)
  calls: request
  called_by: merge_environment_settings, send, Session, should_strip_auth, SessionRedirectMixin, merge_hooks

merge_setting (src/requests/sessions.py:62-89)
  Determines appropriate setting for a given request, taking into account
  sig: merge_setting(request_setting, session_setting, dict_class)
  behavior: ACCUMULATE(none_keys loop -> result)
  called_by: merge_environment_settings, prepare_request, Session, merge_hooks

get (src/requests/cookies.py:194-204)
  Dict-like get() that also supports optional domain and path args in
  sig: get(name, default, domain, path)
  calls: _find_no_duplicates
  called_by: get_full_url, get_header, MockRequest, set, RequestsCookieJar, get_cookie_header

request (src/requests/sessions.py:502-593)
  Constructs a :class:`Request <Request>`, prepares it and sends it.
  sig: request(method, url, params, data, headers...)
  calls: merge_environment_settings, prepare_request, send
  called_by: delete, get, head, options, patch, post, put, Session
  uses: Request (models)

resolve_redirects (src/requests/sessions.py:160-280)
  Receives a Response.
  sig: resolve_redirects(resp, req, stream, timeout, verify...)
  behavior: ACCUMULATE(req.copy loop -> hist, raises TooManyRedirects)
  calls: close, send, get_redirect_target, rebuild_auth, rebuild_method, rebuild_proxies
  called_by: send, Session
  raises: TooManyRedirects
  uses: TooManyRedirects (exceptions)

HTTPAdapter (src/requests/adapters.py:144-697)
  The built-in HTTP Adapter for urllib3.
  extends: BaseAdapter
  imports: socket, warnings, urllib3.exceptions, urllib3.poolmanager, urllib3.util
  calls: add_headers, build_connection_pool_key_attributes, build_response, cert_verify, get_connection_with_tls_context, init_poolmanager, proxy_headers, proxy_manager_for
  raises: OSError, InvalidURL, InvalidProxyURL, ConnectionError
  uses: Response (models), CaseInsensitiveDict (structures), InvalidURL (exceptions), InvalidProxyURL (exceptions)

update (src/requests/cookies.py:358-364)
  Updates this jar with cookies from another CookieJar or dict-like
  sig: update(other)
  behavior: BRANCH(isinstance(other, cookielib.C... -> result, else -> super().update(ot...)
  calls: copy, set_cookie
  called_by: __setstate__, copy, RequestsCookieJar, create_cookie, merge_cookies

extract_cookies_to_jar (src/requests/cookies.py:124-137)
  Extract the cookies from the response into a CookieJar.
  sig: extract_cookies_to_jar(jar, request, response)
  calls: MockRequest, MockResponse

get_cookie_header (src/requests/cookies.py:140-148)
  Produce an appropriate Cookie header string to be sent with `request`, or None.
  sig: get_cookie_header(jar, request)
  calls: get_new_headers, MockRequest, get

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 80 symbols in L3, 29 with behavior annotations
uncovered: get_header, get_new_headers, head, host

--- CLUE FILE END ---

QUESTION: How do the Requests API docs divide the library into public layers, and which kinds of objects appear in each layer?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
