You have TWO tasks to complete. Read carefully.

=== TASK 1: ANSWER THE QUESTION ===

You are a senior software engineer reading a codebase comprehension artifact (a "clue file") that summarises a repository's structure and behavior. Answer the question below using ONLY the information in the clue file. Do not use any external knowledge about the framework or library.

--- CLUE FILE START ---
=CC v2 httpx@HEAD 60mod 1241sym
? What security mechanisms prevent URL-based attacks like open redirects?


-- TREE
httpx/  (23 files)
  _transports/
tests/  (37 files)
  client/  models/

-- INDEX
httpx/__init__.py                               106L  main
httpx/__version__.py                              3L  
httpx/_api.py                                   438L  delete, get, head, options, patch
httpx/_auth.py                                  348L  async_auth_flow, auth_flow, sync_auth_flow, Auth, auth_flow
httpx/_client.py                               2019L  aclose, delete, get, head, options
httpx/_config.py                                248L  Limits, raw_auth, Proxy, as_dict, Timeout
httpx/_content.py                               240L  AsyncIteratorByteStream, ByteStream, IteratorByteStream, UnattachedStream, encode_content
httpx/_decoders.py                              393L  decode, flush, BrotliDecoder, decode, flush
httpx/_exceptions.py                            377L  CloseError, ConnectError, ConnectTimeout, CookieConflict, DecodingError
httpx/_main.py                                  506L  download_response, format_certificate, format_request_headers, format_response_headers, get_lexer_for_response
httpx/_models.py                               1277L  add_unredirected_header, info, clear, delete, extract_cookies
httpx/_multipart.py                             300L  get_length, render, render_data, render_headers, DataField
httpx/_status_codes.py                          162L  get_reason_phrase, is_client_error, is_error, is_informational, is_redirect
httpx/_transports/__init__.py                    15L  
httpx/_transports/asgi.py                       187L  ASGIResponseStream, receive, send, handle_async_request, ASGITransport
httpx/_transports/base.py                        86L  aclose, handle_async_request, AsyncBaseTransport, close, handle_request
  ...and 44 more modules

-- SYM
map_httpcore_exceptions             M httpx/_transports/default.py:96     function map_httpcore_exceptions
_load_httpcore_exceptions           M httpx/_transports/default.py:74     function _load_httpcore_exceptions
QueryParams                         C httpx/_urls.py:420    URL query parameters, as a multi-dict.
items                               M httpx/_urls.py:486    Return all items in the query params.
request                             M httpx/_api.py:39     Sends an HTTP request.
URL                                 C httpx/_urls.py:15     url = httpx.URL("HTTPS://jo%40email.com:a%20sec...
ByteStream                          C httpx/_content.py:31     class ByteStream
copy_with                           M httpx/_urls.py:327    Copy this URL, returning a new URL with some co...
PERCENT                             M httpx/_urlparse.py:478    function PERCENT
percent_encoded                     M httpx/_urlparse.py:482    Use percent-encoding to quote a string.
get_list                            M httpx/_models.py:252    Return a list of all header values for a given ...
_port_or_default                    M httpx/_client.py:77     function _port_or_default
multi_items                         M httpx/_models.py:231    Return a list of `(key, value)` pairs of headers.
get                                 M httpx/_urls.py:512    Get a value from the query param for a given key.
add_unredirected_header             M httpx/_models.py:1257   function add_unredirected_header
_format_form_param                  M httpx/_multipart.py:33     Encode a name/value pair within a multipart form.
quote                               M httpx/_urlparse.py:497    Use percent-encoding to quote a string, omittin...
_get_content_decoder                M httpx/_models.py:699    Returns a decoder instance which can be used to...
_skip_leading_empty_chunks          M httpx/_transports/wsgi.py:22     function _skip_leading_empty_chunks
Headers                             C httpx/_models.py:139    HTTP headers, as a case-insensitive multi-dict.
iter_chunks                         M httpx/_multipart.py:258    function iter_chunks
keys                                M httpx/_urls.py:463    Return all the keys in the query params.
urlparse                            M httpx/_urlparse.py:213    function urlparse
aclose                              M httpx/_models.py:1065   Close the response and release the connection.
close                               M httpx/_models.py:961    Close the response and release the connection.
_CookieCompatRequest                C httpx/_models.py:1243   Wraps a `Request` instance up in a compatibilit...
aclose                              M httpx/_transports/base.py:85     async_function aclose
close                               M httpx/_transports/base.py:61     function close
WSGIByteStream                      C httpx/_transports/wsgi.py:30     class WSGIByteStream
aiter_bytes                         M httpx/_models.py:982    A byte-iterator over the decoded response content.
iter_bytes                          M httpx/_models.py:884    A byte-iterator over the decoded response content.
__new__                             M httpx/_status_codes.py:28     function __new__
is_running_trio                     M httpx/_transports/asgi.py:29     function is_running_trio
get_list                            M httpx/_urls.py:526    Get all values from the query param for a given...
clear                               M httpx/_models.py:1192   Delete all cookies.
get_lexer_for_response              M httpx/_main.py:103    function get_lexer_for_response
aiter_raw                           M httpx/_models.py:1037   A byte-iterator over the raw response content.
iter_raw                            M httpx/_models.py:935    A byte-iterator over the raw response content.
_build_auth                         M httpx/_client.py:445    function _build_auth
format_request_headers              M httpx/_main.py:116    function format_request_headers
format_response_headers             M httpx/_main.py:129    function format_response_headers
multi_items                         M httpx/_urls.py:498    Return all items in the query params.
_DigestAuthChallenge                C httpx/_auth.py:343    class _DigestAuthChallenge
get_content_length                  M httpx/_multipart.py:265    Return the length of the multipart encoded cont...
items                               M httpx/_models.py:216    Return `(key, value)` items of headers.
DataField                           C httpx/_multipart.py:70     A single form field item, within a multipart fo...
aiter_text                          M httpx/_models.py:1007   A str-iterator over the decoded response content
iter_text                           M httpx/_models.py:907    A str-iterator over the decoded response content
_parse_content_type_charset         M httpx/_models.py:85     function _parse_content_type_charset
_parse_header_links                 M httpx/_models.py:93     Returns a list of parsed link headers, for more...
print_help                          M httpx/_main.py:26     function print_help
codes                               C httpx/_status_codes.py:8      HTTP status codes and reason phrases
merge                               M httpx/_urls.py:582    Return a new QueryParams instance, updated with.
add                                 M httpx/_urls.py:552    Return a new QueryParams instance, setting or a...
remove                              M httpx/_urls.py:567    Return a new QueryParams instance, removing the...
set                                 M httpx/_urls.py:537    Return a new QueryParams instance, setting the ...
join                                M httpx/_urls.py:354    Return an absolute URL, using this URL as the b...
_CookieCompatResponse               C httpx/_models.py:1261   Wraps a `Request` instance up in a compatibilit...
keys                                M httpx/_models.py:202    function keys
AsyncResponseStream                 C httpx/_transports/default.py:265    class AsyncResponseStream
ResponseStream                      C httpx/_transports/default.py:121    class ResponseStream
_is_https_redirect                  M httpx/_client.py:62     Return 'True' if 'location' is a HTTPS upgrade ...
_same_origin                        M httpx/_client.py:83     Return 'True' if the given URLs share the same ...
Cookies                             C httpx/_models.py:1079   HTTP Cookies, as a mutable mapping.
__aiter__                           M httpx/_transports/asgi.py:59     async_function __aiter__
ASGIResponseStream                  C httpx/_transports/asgi.py:55     class ASGIResponseStream
create_event                        M httpx/_transports/asgi.py:44     function create_event
extract_cookies                     M httpx/_models.py:1101   Loads any cookies based on the response `Set-Co...
values                              M httpx/_urls.py:474    Return all the values in the query params.
encode_content                      M httpx/_content.py:107    function encode_content
  ...and 463 more symbols

-- FOCUS
_send_handling_redirects (httpx/_client.py:1679-1715)
  sig: _send_handling_redirects(request, follow_redirects, history)
  raises: TooManyRedirects, exc

_build_redirect_request (httpx/_client.py:475-492)
  Given a request and a redirect response, return a new request that
  sig: _build_redirect_request(request, response)
  calls: _redirect_headers, _redirect_method, _redirect_stream, _redirect_url
  called_by: AsyncClient, Client

_redirect_headers (httpx/_client.py:546-571)
  Return the headers that should be used for the redirect request.
  sig: _redirect_headers(request, url, method)
  calls: _is_https_redirect, _same_origin
  called_by: _build_redirect_request, BaseClient

_redirect_method (httpx/_client.py:494-515)
  When being redirected we may want to change the method of the request
  sig: _redirect_method(request, response)
  called_by: _build_redirect_request, BaseClient

_redirect_stream (httpx/_client.py:573-582)
  Return the body that should be used for the redirect request.
  sig: _redirect_stream(request, method)
  called_by: _build_redirect_request, BaseClient

_redirect_url (httpx/_client.py:517-544)
  Return the URL for the redirect to follow.
  sig: _redirect_url(request, response)
  called_by: _build_redirect_request, BaseClient
  raises: RemoteProtocolError

_send_handling_redirects (httpx/_client.py:964-999)
  sig: _send_handling_redirects(request, follow_redirects, history)
  raises: TooManyRedirects, exc

_is_https_redirect (httpx/_client.py:62-74)
  Return 'True' if 'location' is a HTTPS upgrade of 'url'
  sig: _is_https_redirect(url, location)
  calls: _port_or_default
  called_by: _redirect_headers, BaseClient

TooManyRedirects (httpx/_exceptions.py:249-255)
  Too many redirects.
  extends: RequestError

add_unredirected_header (httpx/_models.py:1257-1259)
  sig: add_unredirected_header(key, value)
  called_by: _CookieCompatRequest, Cookies

has_redirect_location (httpx/_models.py:772-792)
  Returns True for 3xx responses with a properly formed URL redirection,

is_redirect (httpx/_models.py:739-748)
  A property which is `True` for 3xx status codes, `False` otherwise.
  called_by: Response

is_redirect (httpx/_status_codes.py:60-64)
  Returns `True` for 3xx status codes, `False` otherwise.
  sig: is_redirect(cls, value)

peek_filelike_length (httpx/_utils.py:95-117)
  Given a file-like stream object, return its length in number of bytes
  sig: peek_filelike_length(stream)

URL (httpx/_urls.py:15-420)
  url = httpx.URL("HTTPS://jo%40email.com:a%20secret@müller.de:1234/pa%20th?search=ab#anchorlink")
  imports: urllib.parse, idna, warnings
  calls: add, items, merge, remove, set, QueryParams, copy_with, join
  called_by: copy_with, join
  raises: TypeError

url (httpx/_models.py:629-633)
  Returns the URL for which the request was made.

QueryParams (httpx/_urls.py:420-642)
  URL query parameters, as a multi-dict.
  imports: urllib.parse, idna, warnings
  calls: get, get_list, items, keys, multi_items, values
  called_by: add, merge, remove, set, params, URL
  raises: RuntimeError

items (httpx/_urls.py:486-498)
  Return all items in the query params.
  called_by: multi_items, values, QueryParams, URL

set (httpx/_urls.py:537-552)
  Return a new QueryParams instance, setting the value of a key.
  sig: set(key, value)
  calls: QueryParams
  called_by: copy_set_param, URL

join (httpx/_urls.py:354-369)
  Return an absolute URL, using this URL as the base.
  sig: join(url)
  calls: URL
  called_by: URL

add (httpx/_urls.py:552-567)
  Return a new QueryParams instance, setting or appending the value of a key.
  sig: add(key, value)
  calls: get_list, QueryParams
  called_by: copy_add_param, URL

remove (httpx/_urls.py:567-582)
  Return a new QueryParams instance, removing the value of a key.
  sig: remove(key)
  calls: QueryParams
  called_by: copy_remove_param, URL

merge (httpx/_urls.py:582-600)
  Return a new QueryParams instance, updated with.
  sig: merge(params)
  calls: QueryParams
  called_by: copy_merge_params, URL

copy_with (httpx/_urls.py:327-342)
  Copy this URL, returning a new URL with some components altered.
  calls: URL
  called_by: copy_add_param, copy_merge_params, copy_remove_param, copy_set_param, URL

values (httpx/_urls.py:474-486)
  Return all the values in the query params.
  calls: items
  called_by: QueryParams

multi_items (httpx/_urls.py:498-512)
  Return all items in the query params.
  calls: items
  called_by: QueryParams

copy_set_param (httpx/_urls.py:342-345)
  sig: copy_set_param(key, value)
  calls: set, copy_with

params (httpx/_urls.py:276-283)
  The URL query parameters, neatly parsed and packaged into an immutable
  calls: QueryParams

get_list (httpx/_urls.py:526-537)
  Get all values from the query param for a given key.
  sig: get_list(key)
  calls: get
  called_by: add, QueryParams

keys (httpx/_urls.py:463-474)
  Return all the keys in the query params.
  called_by: __iter__, QueryParams

get (httpx/_urls.py:512-526)
  Get a value from the query param for a given key.
  sig: get(key, default)
  called_by: get_list, QueryParams

copy_add_param (httpx/_urls.py:345-348)
  sig: copy_add_param(key, value)
  calls: add, copy_with

copy_remove_param (httpx/_urls.py:348-351)
  sig: copy_remove_param(key)
  calls: remove, copy_with

copy_merge_params (httpx/_urls.py:351-354)
  sig: copy_merge_params(params)
  calls: merge, copy_with

-- GAPS
- Question mentions [attacks, based, like, mechanisms, open] — not found in focus or symbol index
- Module httpx/_urlparse.py matches question but has no focus detail
  > drill: httpx/_urlparse.py
- Module tests/client/test_redirects.py matches question but has no focus detail
  > drill: tests/client/test_redirects.py

--- CLUE FILE END ---

QUESTION: What security mechanisms prevent URL-based attacks like open redirects?

Provide a detailed answer covering:
1. Which specific files and symbols are involved
2. How the mechanism works (based on what the clue tells you)
3. Any security properties, error handling, or invariants mentioned in the clue
4. What risks or gaps you can identify from the clue

=== TASK 2: SELF-SCORE YOUR ANSWER ===

After writing your answer above, score it against these gold facts.
For EACH fact below, state whether your answer COVERS it (the information is present or can be inferred from your answer) or MISSES it (the information is not in your answer).

FACT 1: URLs are validated and normalized on instantiation to prevent injection
FACT 2: Client enforces DEFAULT_MAX_REDIRECTS limit to prevent redirect loops
FACT 3: HTTPS-to-HTTP downgrades are detected during redirect following
FACT 4: TooManyRedirects exception raised when redirect count exceeds limit

Output your scoring in this EXACT format at the end of your response:

```
=== SCORING ===
Task: httpx-tf5-redirect-security
Model: [state which model you are, e.g. Claude Opus 4.6, GPT-5.4, Gemini 3.4]
FACT 1: [COVERS or MISSES] - [brief justification]
FACT 2: [COVERS or MISSES] - [brief justification]
FACT 3: [COVERS or MISSES] - [brief justification]
FACT 4: [COVERS or MISSES] - [brief justification]
Score: [count of COVERS]/[total facts]
Sufficient: [YES if score >= 60%, NO otherwise]
```
