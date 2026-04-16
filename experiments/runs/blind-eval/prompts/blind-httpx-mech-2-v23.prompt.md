# Blind Evaluation Prompt - MRLF v2.4
# Task: blind-httpx-mech-2

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 httpx@HEAD 60mod 1241sym
? How do timeouts and streamed response access work in HTTPX according to the public docs?


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
set                                 M httpx/_urls.py:537    Return a new QueryParams instance, setting the ...
add                                 M httpx/_urls.py:552    Return a new QueryParams instance, setting or a...
remove                              M httpx/_urls.py:567    Return a new QueryParams instance, removing the...
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
ResponseNotRead (httpx/_exceptions.py:338-351)
  Attempted to access streaming response content, without having called `read()`.
  extends: StreamError

Response (httpx/_models.py:515-1076)
  imports: codecs, email.message, urllib.request, http.cookiejar
  calls: extract_cookies, Cookies, get_list, items, Headers, _get_content_decoder, aclose, aiter_bytes
  raises: HTTPStatusError, RuntimeError, ResponseNotRead, ValueError

print_response_headers (httpx/_main.py:156-167)
  sig: print_response_headers(http_version, status, reason_phrase, headers)
  calls: format_response_headers
  called_by: trace

print_response (httpx/_main.py:170-186)
  sig: print_response(response)
  behavior: BRANCH(lexer_name -> rich.syntax.Syntax(te..., else -> console.print(f'<{len...)
  calls: get_lexer_for_response
  called_by: main

AsyncResponseStream (httpx/_transports/default.py:265-276)
  extends: AsyncByteStream
  imports: types, base, ssl, httpx, httpcore
  calls: map_httpcore_exceptions
  called_by: handle_async_request, AsyncHTTPTransport

ResponseStream (httpx/_transports/default.py:121-132)
  extends: SyncByteStream
  imports: types, base, ssl, httpx, httpcore
  calls: map_httpcore_exceptions
  called_by: handle_request, HTTPTransport

download_response (httpx/_main.py:251-270)
  sig: download_response(response, download)
  called_by: main

format_response_headers (httpx/_main.py:129-144)
  sig: format_response_headers(http_version, status, reason_phrase, headers)
  called_by: print_response_headers

get_lexer_for_response (httpx/_main.py:103-113)
  sig: get_lexer_for_response(response)
  called_by: print_response

start_response (httpx/_transports/wsgi.py:123-132)
  sig: start_response(status, response_headers, exc_info)

stream (httpx/_client.py:1543-1592)
  Alternative to `httpx.request()` that streams the response body
  sig: stream(method, url)

stream (httpx/_client.py:828-877)
  Alternative to `httpx.request()` that streams the response body
  sig: stream(method, url)

stream (httpx/_api.py:124-171)
  Alternative to `httpx.request()` that streams the response body
  sig: stream(method, url)

_CookieCompatResponse (httpx/_models.py:1261-1277)
  Wraps a `Request` instance up in a compatibility interface suitable
  imports: codecs, email.message, urllib.request, http.cookiejar
  calls: multi_items
  called_by: extract_cookies, Cookies

_build_redirect_request (httpx/_client.py:475-492)
  Given a request and a redirect response, return a new request that
  sig: _build_redirect_request(request, response)
  calls: _redirect_headers, _redirect_method, _redirect_stream, _redirect_url
  called_by: AsyncClient, Client

extract_cookies (httpx/_models.py:1101-1108)
  Loads any cookies based on the response `Set-Cookie` headers.
  sig: extract_cookies(response)
  calls: _CookieCompatRequest, _CookieCompatResponse
  called_by: Cookies, cookies, Response

aiter_text (httpx/_models.py:1007-1026)
  A str-iterator over the decoded response content
  sig: aiter_text(chunk_size)
  calls: aiter_bytes
  called_by: aiter_lines, Response

iter_text (httpx/_models.py:907-924)
  A str-iterator over the decoded response content
  sig: iter_text(chunk_size)
  calls: iter_bytes
  called_by: iter_lines, Response

URL (httpx/_urls.py:15-420)
  url = httpx.URL("HTTPS://jo%40email.com:a%20secret@müller.de:1234/pa%20th?search=ab#anchorlink")
  imports: urllib.parse, idna, warnings
  calls: add, items, merge, remove, set, QueryParams, copy_with, join
  called_by: copy_with, join
  raises: TypeError

aiter_bytes (httpx/_models.py:982-1005)
  A byte-iterator over the decoded response content.
  sig: aiter_bytes(chunk_size)
  behavior: BRANCH(hasattr(self, '_content') -> len(self._content) if..., else -> self._...)
  calls: _get_content_decoder, aiter_raw
  called_by: aiter_text, Response

iter_bytes (httpx/_models.py:884-905)
  A byte-iterator over the decoded response content.
  sig: iter_bytes(chunk_size)
  behavior: BRANCH(hasattr(self, '_content') -> len(self._content) if..., else -> self._...)
  calls: _get_content_decoder, iter_raw
  called_by: iter_text, Response

aiter_raw (httpx/_models.py:1037-1063)
  A byte-iterator over the raw response content.
  sig: aiter_raw(chunk_size)
  behavior: ACCUMULATE(chunker.flush() loop -> result)
  calls: aclose
  called_by: aiter_bytes, Response
  raises: StreamConsumed, StreamClosed, RuntimeError

iter_raw (httpx/_models.py:935-959)
  A byte-iterator over the raw response content.
  sig: iter_raw(chunk_size)
  behavior: ACCUMULATE(chunker.flush() loop -> result)
  calls: close
  called_by: iter_bytes, Response
  raises: StreamConsumed, StreamClosed, RuntimeError

BoundAsyncStream (httpx/_client.py:162-182)
  An async byte stream that is bound to a given response instance, and that
  extends: AsyncByteStream
  imports: enum, logging, warnings, types, ssl
  called_by: AsyncClient

BoundSyncStream (httpx/_client.py:139-159)
  A byte stream that is bound to a given response instance, and that
  extends: SyncByteStream
  imports: enum, logging, warnings, types, ssl
  called_by: Client

DecodingError (httpx/_exceptions.py:243-249)
  Decoding of the response failed, due to a malformed encoding.
  extends: RequestError

HTTPStatusError (httpx/_exceptions.py:258-271)
  The response had an error HTTP status of 4xx or 5xx.
  extends: HTTPError

RequestNotRead (httpx/_exceptions.py:351-364)
  Attempted to access streaming request content, without having called `read()`.
  extends: StreamError

StreamClosed (httpx/_exceptions.py:327-338)
  Attempted to read or stream response content, but the request has been
  extends: StreamError

UnattachedStream (httpx/_content.py:92-104)
  If a request or response is serialized using pickle, then it is no longer
  extends: AsyncByteStream, SyncByteStream
  imports: inspect, warnings, urllib.parse
  raises: StreamClosed

aclose (httpx/_models.py:1065-1076)
  Close the response and release the connection.
  called_by: aiter_raw, Response
  raises: RuntimeError

aread (httpx/_models.py:974-980)
  Read and return the response content.

close (httpx/_models.py:961-972)
  Close the response and release the connection.
  called_by: iter_raw, Response
  raises: RuntimeError

elapsed (httpx/_models.py:579-589)
  Returns the time taken for the complete request/response
  raises: RuntimeError

handle_request (httpx/_transports/base.py:26-59)
  Send a single HTTP request and return a response.
  sig: handle_request(request)
  raises: NotImplementedError

links (httpx/_models.py:842-853)
  Returns the parsed header links of the response, if any
  calls: _parse_header_links

read (httpx/_models.py:876-882)
  Read and return the response content.

request (httpx/_models.py:596-604)
  Returns the request instance associated to the current response.
  raises: RuntimeError

encode_response (httpx/_content.py:221-240)
  Handles encoding the given `content`, returning a two-tuple of
  sig: encode_response(content, text, html, json)
  calls: ByteStream, encode_content, encode_html, encode_json, encode_text

ASGIResponseStream (httpx/_transports/asgi.py:55-60)
  extends: AsyncByteStream
  imports: base, asyncio, trio, sniffio
  called_by: handle_async_request, ASGITransport

NetworkError (httpx/_exceptions.py:167-175)
  The base class for network-related errors.
  extends: TransportError

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 80 symbols in L3, 16 with behavior annotations
uncovered: BaseClient, Request, multi_items, _build_request_auth

--- CLUE FILE END ---

QUESTION: How do timeouts and streamed response access work in HTTPX according to the public docs?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
