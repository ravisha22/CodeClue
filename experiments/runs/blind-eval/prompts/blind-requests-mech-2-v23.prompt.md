# Blind Evaluation Prompt - MRLF v2.1 with File 2 Drill-Down
# Task: blind-requests-mech-2

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

--- CLUE FILE (File 1) ---
=CC v2.1 requests@HEAD 36mod 757sym
? How does Requests handle streaming and decoding edge cases on `Response` objects?


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
build_response (src/requests/adapters.py:337-372)
  Builds a :class:`Response <requests.Response>` object from a urllib3
  sig: build_response(req, resp)
  behavior: BRANCH(isinstance_bytes -> result, else -> result)
  called_by: HTTPAdapter
  uses: Response (models), CaseInsensitiveDict (structures)

__init__ (src/requests/exceptions.py:18-25)
  Initialize RequestException with `request` and `response` objects.

Response (src/requests/models.py:642-1041)
  The :class:`Response <Response>` object, which contains a
  imports: encodings.idna, io, urllib3.exceptions, urllib3.fields, urllib3.filepost
  calls: close, generate, iter_content, raise_for_status
  raises: StreamConsumedError, HTTPError, TypeError, RuntimeError
  uses: ChunkedEncodingError (exceptions), ContentDecodingError (exceptions), ConnectionError (exceptions), RequestsSSLError (exceptions)

ContentDecodingError (src/requests/exceptions.py:124-125)
  Failed to decode response content.
  extends: RequestException, BaseHTTPError
  imports: urllib3.exceptions, compat

handle_401 (src/requests/auth.py:241-283)
  Takes the given response and tries digest-auth, if needed.
  sig: handle_401(r)
  calls: build_digest_header

iter_content (src/requests/models.py:801-857)
  Iterates over the response data.
  sig: iter_content(chunk_size, decode_unicode)
  calls: generate
  called_by: __iter__, content, iter_lines, Response
  raises: StreamConsumedError, TypeError, ChunkedEncodingError, ContentDecodingError
  uses: StreamConsumedError (exceptions), ChunkedEncodingError (exceptions), ContentDecodingError (exceptions), ConnectionError (exceptions)

json (src/requests/models.py:949-982)
  Decodes the JSON response body (if any) as a Python object.
  raises: RequestsJSONDecodeError
  uses: RequestsJSONDecodeError (exceptions)

Session (src/requests/sessions.py:356-818)
  A Requests session.
  extends: SessionRedirectMixin
  imports: adapters, auth, compat, cookies, exceptions
  calls: close, get, get_adapter, merge_environment_settings, mount, prepare_request, request, send
  called_by: session
  raises: InvalidSchema, ValueError
  uses: InvalidSchema (exceptions), PreparedRequest (models), RequestsCookieJar (cookies), Request (models)

resolve_redirects (src/requests/sessions.py:160-280)
  Receives a Response.
  sig: resolve_redirects(resp, req, stream, timeout, verify...)
  behavior: ACCUMULATE(loop -> hist)
  calls: close, send, get_redirect_target, rebuild_auth, rebuild_method, rebuild_proxies
  called_by: send, Session
  raises: TooManyRedirects
  uses: TooManyRedirects (exceptions)

MockRequest (src/requests/cookies.py:23-100)
  Wraps a `requests.Request` to mimic a `urllib2.Request`.
  imports: calendar, copy, compat, threading, dummy_threading
  calls: get_host, get_origin_req_host, is_unverifiable, get
  called_by: extract_cookies_to_jar, get_cookie_header
  raises: NotImplementedError

extract_cookies_to_jar (src/requests/cookies.py:124-137)
  Extract the cookies from the response into a CookieJar.
  sig: extract_cookies_to_jar(jar, request, response)
  calls: MockRequest, MockResponse

merge_hooks (src/requests/sessions.py:92-104)
  Properly merges both requests and session hooks.
  sig: merge_hooks(request_hooks, session_hooks, dict_class)
  calls: get, merge_setting
  called_by: prepare_request, Session

get_redirect_target (src/requests/sessions.py:108-126)
  Receives a Response.
  sig: get_redirect_target(resp)
  called_by: resolve_redirects, SessionRedirectMixin

__iter__ (src/requests/models.py:752-754)
  Allows you to use a response as an iterator.
  behavior: DELEGATE(iter_content -> result)
  calls: iter_content

content (src/requests/models.py:893-909)
  Content of the response, in bytes.
  calls: iter_content
  raises: RuntimeError

iter_lines (src/requests/models.py:859-890)
  Iterates over the response data, one line at a time.
  sig: iter_lines(chunk_size, decode_unicode, delimiter)
  behavior: ACCUMULATE(loop -> chunk)
  calls: iter_content

copy (src/requests/cookies.py:428-433)
  Return a copy of this RequestsCookieJar.
  calls: get_policy, update, RequestsCookieJar
  called_by: __getstate__, update, RequestsCookieJar, _copy_cookie_jar

FileModeWarning (src/requests/exceptions.py:147-148)
  A file was opened in text mode, but Requests determined its binary length.
  extends: RequestsWarning, DeprecationWarning
  imports: urllib3.exceptions, compat

RequestsWarning (src/requests/exceptions.py:143-144)
  Base warning for Requests.
  extends: Warning
  imports: urllib3.exceptions, compat

StreamConsumedError (src/requests/exceptions.py:128-129)
  The content for this response was already consumed.
  extends: RequestException, TypeError
  imports: urllib3.exceptions, compat

UnrewindableBodyError (src/requests/exceptions.py:136-137)
  Requests encountered an error when trying to rewind a body.
  extends: RequestException
  imports: urllib3.exceptions, compat

__init__ (src/requests/cookies.py:110-115)
  Make a MockResponse for `cookiejar` to read.
  sig: __init__(headers)

_find (src/requests/cookies.py:366-384)
  Requests uses this method internally to get cookie values.
  sig: _find(name, domain, path)
  behavior: ACCUMULATE(loop -> result)
  raises: KeyError

default_headers (src/requests/utils.py:887-898)
  :rtype: requests.structures.CaseInsensitiveDict
  behavior: DELEGATE(CaseInsensitiveDict -> result)
  calls: default_user_agent
  uses: CaseInsensitiveDict (structures)

get_netrc_auth (src/requests/utils.py:206-247)
  Returns the Requests tuple auth for a given url from netrc.
  sig: get_netrc_auth(url, raise_errors)
  behavior: BRANCH(netrc_file -> result, else -> result)

is_permanent_redirect (src/requests/models.py:779-784)
  True if this Response one of the permanent versions of redirect.

is_redirect (src/requests/models.py:772-776)
  True if this Response is a well-formed HTTP redirect that could have

links (src/requests/models.py:985-999)
  Returns the parsed header links of the response, if any.

text (src/requests/models.py:912-947)
  Content of the response, in unicode.

MockResponse (src/requests/cookies.py:103-121)
  Wraps a `httplib.HTTPMessage` to mimic a `urllib.addinfourl`.
  imports: calendar, copy, compat, threading, dummy_threading
  calls: getheaders
  called_by: extract_cookies_to_jar

get_unicode_from_response (src/requests/utils.py:578-614)
  Returns the requested content back in unicode.
  sig: get_unicode_from_response(r)
  calls: get_encoding_from_headers

handle_redirect (src/requests/auth.py:236-239)
  Reset num_401_calls counter on redirects.
  sig: handle_redirect(r)

stream_decode_response_unicode (src/requests/utils.py:551-565)
  Stream decodes an iterator.
  sig: stream_decode_response_unicode(iterator, r)
  behavior: ACCUMULATE(loop -> result)

generate (src/requests/models.py:818-839)
  behavior: BRANCH(hasattr_stream -> result, else -> result)
  called_by: iter_content, Response
  raises: ChunkedEncodingError, ContentDecodingError, ConnectionError, RequestsSSLError
  uses: ChunkedEncodingError (exceptions), ContentDecodingError (exceptions), ConnectionError (exceptions), RequestsSSLError (exceptions)

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

send (src/requests/sessions.py:675-750)
  Send a given PreparedRequest.
  sig: send(request)
  behavior: BRANCH(allow_redirects -> result, else -> result)
  calls: get, get_adapter, resolve_redirects
  called_by: request, Session, resolve_redirects, SessionRedirectMixin
  raises: ValueError

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 23 with behavior annotations
drill: src/requests/adapters.py (~33 lines, build_response)
drill: src/requests/exceptions.py (~10 lines, __init__)
drill: src/requests/auth.py (~39 lines, handle_401)
drill: src/requests/sessions.py (~117 lines, resolve_redirects)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
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

## build_response  (tests/test_requests.py L2081-2088)
```
        def build_response(*args, **kwargs):
            resp = org_build_response(*args, **kwargs)
            if not self._patched_response:
                resp.raw.headers["content-encoding"] = "gzip"
                self._patched_response = True
            return resp

        adapter.build_response = build_response
```

## handle_401  (src/requests/auth.py L241-283)
```
    def handle_401(self, r, **kwargs):
        """
        Takes the given response and tries digest-auth, if needed.

        :rtype: requests.Response
        """

        # If response is not 4xx, do not auth
        # See https://github.com/psf/requests/issues/3772
        if not 400 <= r.status_code < 500:
            self._thread_local.num_401_calls = 1
            return r

        if self._thread_local.pos is not None:
            # Rewind the file position indicator of the body to where
            # it was to resend the request.
            r.request.body.seek(self._thread_local.pos)
        s_auth = r.headers.get("www-authenticate", "")

        if "digest" in s_auth.lower() and self._thread_local.num_401_calls < 2:
            self._thread_local.num_401_calls += 1
            pat = re.compile(r"digest ", flags=re.IGNORECASE)
            self._thread_local.chal = parse_dict_header(pat.sub("", s_auth, count=1))

            # Consume content and release the original connection
            # to allow our new request to reuse the same one.
            r.content
            r.close()
            prep = r.request.copy()
            extract_cookies_to_jar(prep._cookies, r.request, r.raw)
            prep.prepare_cookies(prep._cookies)

            prep.headers["Authorization"] = self.build_digest_header(
                prep.method, prep.url
            )
            _r = r.connection.send(prep, **kwargs)
            _r.history.append(r)
            _r.request = prep

            return _r

        self._thread_local.num_401_calls = 1
        return r
```

## resolve_redirects  (src/requests/sessions.py L160-280)
```
    def resolve_redirects(
        self,
        resp,
        req,
        stream=False,
        timeout=None,
        verify=True,
        cert=None,
        proxies=None,
        yield_requests=False,
        **adapter_kwargs,
    ):
        """Receives a Response. Returns a generator of Responses or Requests."""

        hist = []  # keep track of history

        url = self.get_redirect_target(resp)
        previous_fragment = urlparse(req.url).fragment
        while url:
            prepared_request = req.copy()

            # Update history and keep track of redirects.
            resp.history = hist[:]
            hist.append(resp)

            try:
                resp.content  # Consume socket so it can be released
            except (ChunkedEncodingError, ContentDecodingError, RuntimeError):
                resp.raw.read(decode_content=False)

            if len(resp.history) >= self.max_redirects:
                raise TooManyRedirects(
                    f"Exceeded {self.max_redirects} redirects.", response=resp
                )

            # Release the connection back into the pool.
            resp.close()

            # Handle redirection without scheme (see: RFC 1808 Section 4)
            if url.startswith("//"):
                parsed_rurl = urlparse(resp.url)
                url = ":".join([to_native_string(parsed_rurl.scheme), url])

            # Normalize url case and attach previous fragment if needed (RFC 7231 7.1.2)
            parsed = urlparse(url)
            if parsed.fragment == "" and previous_fragment:
                parsed = parsed._replace(fragment=previous_fragment)
            elif parsed.fragment:
                previous_fragment = parsed.fragment
            url = parsed.geturl()

            # Facilitate relative 'location' headers, as allowed by RFC 7231.
            # (e.g. '/path/to/resource' instead of 'http://domain.tld/path/to/resource')
            # Compliant with RFC3986, we percent encode the url.
            if not parsed.netloc:
                url = urljoin(resp.url, requote_uri(url))
            else:
                url = requote_uri(url)

            prepared_request.url = to_native_string(url)

            self.rebuild_method(prepared_request, resp)

            # https://github.com/psf/requests/issues/1084
            if resp.status_code not in (
                codes.temporary_redirect,
                codes.permanent_redirect,
            ):
                # https://github.com/psf/requests/issues/3490
                purged_headers = ("Content-Length", "Content-Type", "Transfer-Encoding")
                for header in purged_headers:
                    prepared_request.headers.pop(header, None)
                prepared_request.body = None

            headers = prepared_request.headers
            headers.pop("Cookie", None)

            # Extract any cookies sent on the response to the cookiejar
            # in the new request. Because we've mutated our copied prepared
            # request, use the old one that we haven't yet touched.
            extract_cookies_to_jar(prepared_request._cookies, req, resp.raw)
            merge_cookies(prepared_request._cookies, self.cookies)
            prepared_request.prepare_cookies(prepared_request._cookies)

            # Rebuild auth and proxy information.
            proxies = self.rebuild_proxies(prepared_request, proxies)
            self.rebuild_auth(prepared_request, resp)

            # A failed tell() sets `_body_position` to `object()`. This non-None
            # value ensures `rewindable` will be True, allowing us to raise an
            # UnrewindableBodyError, instead of hanging the connection.
            rewindable = prepared_request._body_position is not None and (
                "Content-Length" in headers or "Transfer-Encoding" in headers
            )

            # Attempt to rewind consumed file-like object.
            if rewindable:
                rewind_body(prepared_request)

            # Override the original request.
            req = prepared_request

            if yield_requests:
                yield req
            else:
                resp = self.send(
                    req,
                    stream=stream,
                    timeout=timeout,
                    verify=verify,
                    cert=cert,
                    proxies=proxies,
                    allow_redirects=False,
                    **adapter_kwargs,
                )

                extract_cookies_to_jar(self.cookies, prepared_request, resp.raw)

                # extract redirect url, if any, for the next loop
                url = self.get_redirect_target(resp)
                yield resp
```

## build_digest_header  (src/requests/auth.py L126-234)
```
    def build_digest_header(self, method, url):
        """
        :rtype: str
        """

        realm = self._thread_local.chal["realm"]
        nonce = self._thread_local.chal["nonce"]
        qop = self._thread_local.chal.get("qop")
        algorithm = self._thread_local.chal.get("algorithm")
        opaque = self._thread_local.chal.get("opaque")
        hash_utf8 = None

        if algorithm is None:
            _algorithm = "MD5"
        else:
            _algorithm = algorithm.upper()
        # lambdas assume digest modules are imported at the top level
        if _algorithm == "MD5" or _algorithm == "MD5-SESS":

            def md5_utf8(x):
                if isinstance(x, str):
                    x = x.encode("utf-8")
                return hashlib.md5(x).hexdigest()

            hash_utf8 = md5_utf8
        elif _algorithm == "SHA":

            def sha_utf8(x):
                if isinstance(x, str):
                    x = x.encode("utf-8")
                return hashlib.sha1(x).hexdigest()

            hash_utf8 = sha_utf8
        elif _algorithm == "SHA-256":

            def sha256_utf8(x):
                if isinstance(x, str):
                    x = x.encode("utf-8")
                return hashlib.sha256(x).hexdigest()

            hash_utf8 = sha256_utf8
        elif _algorithm == "SHA-512":

            def sha512_utf8(x):
                if isinstance(x, str):
                    x = x.encode("utf-8")
                return hashlib.sha512(x).hexdigest()

            hash_utf8 = sha512_utf8

        KD = lambda s, d: hash_utf8(f"{s}:{d}")  # noqa:E731

        if hash_utf8 is None:
            return None

        # XXX not implemented yet
        entdig = None
        p_parsed = urlparse(url)
        #: path is request-uri defined in RFC 2616 which should not be empty
        path = p_parsed.path or "/"
        if p_parsed.query:
            path += f"?{p_parsed.query}"

        A1 = f"{self.username}:{realm}:{self.password}"
        A2 = f"{method}:{path}"

        HA1 = hash_utf8(A1)
        HA2 = hash_utf8(A2)

        if nonce == self._thread_local.last_nonce:
            self._thread_local.nonce_count += 1
        else:
            self._thread_local.nonce_count = 1
        ncvalue = f"{self._thread_local.nonce_count:08x}"
        s = str(self._thread_local.nonce_count).encode("utf-8")
        s += nonce.encode("utf-8")
        s += time.ctime().encode("utf-8")
        s += os.urandom(8)

        cnonce = hashlib.sha1(s).hexdigest()[:16]
        if _algorithm == "MD5-SESS":
            HA1 = hash_utf8(f"{HA1}:{nonce}:{cnonce}")

        if not qop:
            respdig = KD(HA1, f"{nonce}:{HA2}")
        elif qop == "auth" or "auth" in qop.split(","):
            noncebit = f"{nonce}:{ncvalue}:{cnonce}:auth:{HA2}"
            respdig = KD(HA1, noncebit)
        else:
            # XXX handle auth-int.
            return None

        self._thread_local.last_nonce = nonce

        # XXX should the partial digests be encoded too?
        base = (
            f'username="{self.username}", realm="{realm}", nonce="{nonce}", '
            f'uri="{path}", response="{respdig}"'
        )
        if opaque:
            base += f', opaque="{opaque}"'
        if algorithm:
            base += f', algorithm="{algorithm}"'
        if entdig:
            base += f', digest="{entdig}"'
        if qop:
            base += f', qop="auth", nc={ncvalue}, cnonce="{cnonce}"'

        return f"Digest {base}"
```

## close  (src/requests/sessions.py L796-799)
```
    def close(self):
        """Closes all adapters and as such the session"""
        for v in self.adapters.values():
            v.close()
```

## send  (tests/test_requests.py L2576-2580)
```
        self.calls.append(SendCall(args, kwargs))
        return self.build_response()

    def build_response(self):
        request = self.calls[-1].args[0]
```

## get_redirect_target  (tests/test_requests.py L2270-2279)
```
                # default behavior
                if resp.is_redirect:
                    return resp.headers["location"]
                # edge case - check to see if 'location' is in headers anyways
                location = resp.headers.get("location")
                if location and (location != resp.url):
                    return location
                return None

        session = CustomRedirectSession()
```

## rebuild_auth  (src/requests/sessions.py L282-300)
```
    def rebuild_auth(self, prepared_request, response):
        """When being redirected we may want to strip authentication from the
        request to avoid leaking credentials. This method intelligently removes
        and reapplies authentication where possible to avoid credential loss.
        """
        headers = prepared_request.headers
        url = prepared_request.url

        if "Authorization" in headers and self.should_strip_auth(
            response.request.url, url
        ):
            # If we get redirected to a new host, we should strip out any
            # authentication headers.
            del headers["Authorization"]

        # .netrc might have more auth for us on our new host.
        new_auth = get_netrc_auth(url) if self.trust_env else None
        if new_auth is not None:
            prepared_request.prepare_auth(new_auth)
```

## rebuild_method  (src/requests/sessions.py L333-353)
```
    def rebuild_method(self, prepared_request, response):
        """When being redirected we may want to change the method of the request
        based on certain specs or browser behavior.
        """
        method = prepared_request.method

        # https://tools.ietf.org/html/rfc7231#section-6.4.4
        if response.status_code == codes.see_other and method != "HEAD":
            method = "GET"

... (truncated)
```
--- END SOURCE SNIPPETS ---

QUESTION: How does Requests handle streaming and decoding edge cases on `Response` objects?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
