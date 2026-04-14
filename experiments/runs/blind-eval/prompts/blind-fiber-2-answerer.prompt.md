# Blind Evaluation Prompt
# Run this in a SEPARATE VS Code Copilot Chat session (fresh chat, no prior context).

You have THREE tasks to complete. Read carefully.

=== TASK 1: ANSWER THE QUESTION ===

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code — it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.
If the clue does not contain enough information to fully answer, say what
you CAN determine and what you CANNOT.

--- CLUE FILE START ---
=CC v2 fiber@HEAD 243mod 3893sym
? When a handler panics in Fiber, how is that turned into an HTTP response, and how can mounted sub-apps change which error formatter gets used?


-- TREE
addon/  (4 files)
binder/  (24 files)
client/  (17 files)
extractors/  (2 files)
internal/  (6 files)
log/  (5 files)
middleware/  (134 files)

-- INDEX
client/client.go                                863L  C, AddHeader, AddHeaders, AddParam, AddParams
client/request.go                              1122L  AcquireFile, AcquireRequest, Add, All, Del
bind.go                                         477L  AcquireBind, All, Body, CBOR, Cookie
client/transport.go                             377L  composeRedirectURL, doRedirectsWithClient, extractTLSConfig, forEachHostClient, Client
res.go                                         1153L  Cookie, App, Append, Attachment, AutoFormat
app.go                                         1486L  Add, All, Config, Connect, Delete
client/core.go                                  304L  acquireErrChan, acquireResponseChan, addMissingPort, afterHooks, execFunc
internal/storage/memory/memory.go               233L  Entry, New, Close, Conn, Delete
middleware/cache/cache_test.go                 5093L  Benchmark_Cache, Benchmark_Cache_AdditionalHeaders, Benchmark_Cache_MaxSize, Benchmark_Cache_Miss, Benchmark_Cache_Storage
bind_test.go                                   2870L  ArrayQuery, BenchmarkBind_All, Benchmark_Bind_Body_CBOR, Benchmark_Bind_Body_Form, Benchmark_Bind_Body_Form_Map
middleware/limiter/limiter_test.go             1722L  Benchmark_Limiter, Benchmark_Limiter_Custom_Store, TestLimiterDefaultConfigNoPanic, TestLimiterFixedPropagatesRequestContextToStorage, TestLimiterFixedStorageGetError
middleware/paginate/page_info.go                190L  NewPageInfo, CursorValues, NextCursorURL, NextCursorURLWithKeys, NextPageURL
redirect.go                                     433L  AcquireRedirect, FlashMessage, OldInputData, Back, Message
client/cookiejar.go                             334L  AcquireCookieJar, Get, Release, Set, SetByHost
  ...and 229 more modules

-- SYM
domainRouter.Add                    M domain.go:530    Add allows you to specify multiple HTTP methods...
App.Add                             M app.go:953    Add allows you to specify multiple HTTP methods...
Group.Add                           M group.go:167    Add allows you to specify multiple HTTP methods...
Client.applyDial                    M client/client.go:107    function Client.applyDial
DefaultReq.getBody                  M req.go:1140   function DefaultReq.getBody
DefaultReq.Body                     M req.go:149    Body contains the raw body submitted in a POST ...
Client.SetDial                      M client/client.go:606    SetDial sets the custom dial function for the c...
Registering.Add                     M register.go:111    Add allows you to specify multiple HTTP methods...
C                                   M client/client.go:810    C returns the default client.
Cookie.All                          M client/request.go:816    All returns an iterator over cookie key-value p...
Bind.returnBindErr                  M bind.go:171    returnBindErr runs returnErr and, if the result...
DefaultCtx.Get                      M ctx.go:200    Get returns the HTTP request header specified b...
Bind.returnErr                      M bind.go:160    Check WithAutoHandling/WithoutAutoHandling erro...
pair.Len                            M client/request.go:140    Len implements sort.Interface and reports the n...
defaultLogger.privateLog            M log/default.go:24     privateLog logs a message at a given level log ...
defaultLogger.privateLogf           M log/default.go:47     privateLogf logs a formatted message at a given...
defaultLogger.privateLogw           M log/default.go:74     privateLogw logs a message at a given level log...
Cookie.Add                          M client/request.go:781    Add adds a cookie key-value pair.
domainRouter.registerPath           M domain.go:327    registerPath returns the full path for registra...
Cookie.Del                          M client/request.go:786    Del deletes a cookie by key.
domainRouter.registerGroup          M domain.go:336    registerGroup returns the group to associate wi...
domainRouter.wrapHandlers           M domain.go:278    wrapHandlers wraps every handler in the slice w...
DefaultReq.Get                      M req.go:427    Get returns the HTTP request header specified b...
WithStruct                          C client/request.go:24     WithStruct is implemented by types that allow d...
DefaultCtx.String                   M ctx.go:571    String returns unique string representation of ...
FormData.Set                        M client/request.go:893    Set sets a single form field, overriding previo...
Config                              C client/client.go:655    Config is used to easily set request parameters.
Client                              C client/client.go:37     Client provides Fiber's high-level HTTP API whi...
manager.logKey                      M middleware/cache/manager.go:210    function manager.logKey
Session.Get                         M middleware/session/session.go:74     Release releases the session back to the pool.
Bind                                C bind.go:40     Bind provides helper methods for binding reques...
Request.resetBody                   M client/request.go:438    resetBody clears the existing body.
domainRouter.Group                  M domain.go:552    Group creates a new sub-router with a common pr...
wrapContextError                    M internal/storage/memory/memory.go:228    function wrapContextError
DefaultReq.Accepts                  M req.go:51     Accepts checks if the specified extensions or c...
Request.Reset                       M client/request.go:680    Reset clears the Request object, returning it t...
buildPaginationURL                  M middleware/paginate/page_info.go:121    buildPaginationURL parses baseURL and sets/repl...
standardClientTransport.Client      M client/transport.go:82     function standardClientTransport.Client
domainRouter.Name                   M domain.go:602    Name assigns a name to the most recently regist...
Request.Params                      M client/request.go:224    Params returns an iterator over all query param...
Client.TLSConfig                    M client/client.go:236    TLSConfig returns the client's TLS configuration.
walkBalancingClientWithBreak        M client/transport.go:268    walkBalancingClientWithBreak traverses balancin...
decodeKey                           M middleware/encryptcookie/utils.go:20     decodeKey decodes the provided base64-encoded k...
redirectionMsg.Msgsize              M redirect_msgp.go:196    Msgsize returns an upper bound estimate of the ...
DefaultCtx.MediaType                M req.go:244    MediaType returns the MIME type from the Conten...
App.hasConfiguredServices           M services.go:29     hasConfiguredServices Checks if there are any s...
handlerFunc                         M middleware/adaptor/adaptor.go:242    function handlerFunc
setConfigToRequest                  M client/client.go:672    setConfigToRequest sets the parameters passed v...
QueryParam.Keys                     M client/request.go:747    Keys returns all keys from the query parameters.
Response.Body                       M client/response.go:88     Body returns the HTTP response body as a byte s...
File                                C client/request.go:932    File represents a file to be sent with the requ...
Request.Get                         M client/request.go:633    Get sends a GET request to the given URL.
Request.Method                      M client/request.go:76     Method returns the HTTP method set in the Request.
Request.Send                        M client/request.go:673    Send executes the Request.
Request.SetMethod                   M client/request.go:82     SetMethod sets the HTTP method for the Request.
Request.SetURL                      M client/request.go:93     SetURL sets the URL for the Request.
Request.URL                         M client/request.go:88     URL returns the URL set in the Request.
Request.Client                      M client/request.go:99     Client returns the Client instance associated w...
ReleaseFile                         M client/request.go:1053   ReleaseFile returns the File object to the pool.
SetValWithStruct                    M client/request.go:1066   SetValWithStruct sets values using a struct.
shouldIncludeCharset                M res.go:1069   shouldIncludeCharset determines if a MIME type ...
parseCacheControlDirectives         M middleware/cache/cache.go:948    function parseCacheControlDirectives
parseUintDirective                  M middleware/cache/cache.go:937    function parseUintDirective
App.ShutdownWithContext             M app.go:1147   ShutdownWithContext shuts down the server inclu...
decoderBuilder                      M binder/mapping.go:64     function decoderBuilder
CookieJar.SetByHost                 M client/cookiejar.go:154    SetByHost stores the given cookies for the spec...
Request.Cookies                     M client/request.go:335    Cookies returns an iterator over all cookies.
Request.Headers                     M client/request.go:160    Headers returns an iterator over all headers in...
Response.String                     M client/response.go:109    String returns the response body as a trimmed s...
standardClientTransport.Do          M client/transport.go:50     function standardClientTransport.Do
standardClientTransport.DoDeadline  M client/transport.go:58     function standardClientTransport.DoDeadline
standardClientTransport.DoTimeout   M client/transport.go:54     function standardClientTransport.DoTimeout
DefaultCtx.GetHeaders               M ctx.go:207    GetHeaders returns the HTTP request headers.
indexedHeap.removeInternal          M middleware/cache/heap.go:84     function indexedHeap.removeInternal
  ...and 1398 more symbols

-- FOCUS
adaptFiberHandler (adapter.go:32-32)
  sig: adaptFiberHandler(handler any)

toFiberHandler (adapter.go:13-13)
  toFiberHandler converts a supported handler type to a Fiber handler.
  sig: toFiberHandler(handler any)
  called_by: collectHandlers

App.ErrorHandler (app.go:1376-1376)
  ErrorHandler is the application's method in charge of finding the appropriate handler for the given request.
  sig: App.ErrorHandler(ctx Ctx, err error)

App.serverErrorHandler (app.go:1411-1411)
  serverErrorHandler is a wrapper around the application's error handler method user for the fasthttp server configuration
  sig: App.serverErrorHandler(fctx *fasthttp.RequestCtx, err error)
  calls: Error, NewError

DefaultErrorHandler (app.go:524-524)
  DefaultErrorHandler that process return errors from handlers
  sig: DefaultErrorHandler(c Ctx, err error)

FiberHandler (middleware/adaptor/adaptor.go:194-194)
  FiberHandler wraps fiber handler to net/http handler
  sig: FiberHandler(h fiber.Handler)
  calls: FiberHandlerFunc

FiberHandlerFunc (middleware/adaptor/adaptor.go:199-199)
  FiberHandlerFunc wraps fiber handler to net/http handler func
  sig: FiberHandlerFunc(h fiber.Handler)
  calls: handlerFunc
  called_by: FiberHandler

defaultErrorHandler (middleware/csrf/config.go:142-142)
  defaultErrorHandler is the default error handler that processes errors from fiber.Handler.
  sig: defaultErrorHandler(_ fiber.Ctx, _ error)

DefaultPanicHandler (middleware/recover/recover.go:16-16)
  DefaultPanicHandler returns r directly if it's an error, and creates a new one with the %v verb otherwise.
  sig: DefaultPanicHandler(_ fiber.Ctx, r any)

DefaultErrorHandler (middleware/session/config.go:109-109)
  DefaultErrorHandler logs the error and sends a 500 status code.
  sig: DefaultErrorHandler(c fiber.Ctx, err error)

App.hasMountedApps (mount.go:108-109)
  hasMountedApps Checks if there are any mounted apps in the current application.
  called_by: mountStartupProcess

App.processSubAppsRoutes (mount.go:168-169)
  processSubAppsRoutes adds routes of sub-apps recursively when the server is started
  called_by: mountStartupProcess

Error (app.go:62-63)
  Error represents an error that occurred while handling a request.
  methods: Error
  called_by: serverErrorHandler

BindError (bind.go:59-59)
  BindError wraps a binding failure with the source and field that failed.
  methods: Error, Unwrap

Response (client/response.go:19-19)
  Response represents the result of a request.
  methods: Body, BodyStream, CBOR, Close, Cookies, Header

httpClientTransport (client/transport.go:26-26)
  httpClientTransport unifies the operations exposed by the Fiber client across the fasthttp.Client, fasthttp.HostClient, 

responseCacheControl (middleware/cache/cache.go:1049-1049)
  type responseCacheControl

Handler (middleware/csrf/csrf.go:33-33)
  Handler for CSRF middleware
  methods: DeleteToken
  called_by: DeleteToken

healthResponse (middleware/healthcheck/healthcheck.go:8-8)
  healthResponse represents the JSON/XML/MsgPack/CBOR response structure.

response (middleware/idempotency/response.go:9-9)
  response is a struct that represents the response of a request.

Handler (middleware/limiter/limiter.go:18-18)
  Handler defines a rate-limiting strategy that can produce a middleware handler using the provided configuration.

mountFields (mount.go:16-17)
  Put fields related to mounting.

adaptExpressHandler (adapter.go:52-52)
  sig: adaptExpressHandler(handler any)

App.Handler (app.go:1096-1096)
  Handler returns the server handler.
  calls: startupProcess
  called_by: Use

Error.Error (app.go:1042-1042)
  Error makes it compatible with the `error` interface.

NewError (app.go:1046-1046)
  NewError creates a new Error instance with an optional message
  sig: NewError(code int, message ...string)
  called_by: serverErrorHandler

BindError.Error (bind.go:65-65)
  called_by: newBindError

BindError.Unwrap (bind.go:72-72)

extractFieldFromError (bind.go:76-76)
  sig: extractFieldFromError(err error)
  called_by: newBindError

newBindError (bind.go:102-102)
  sig: newBindError(source string, raw error)
  calls: Error, extractFieldFromError

Client.AddResponseHook (client/client.go:160-160)
  AddResponseHook adds user-defined response hooks.
  sig: Client.AddResponseHook(h ...ResponseHook)

Client.ResponseHook (client/client.go:155-155)
  ResponseHook returns the user-defined response hooks.

Client.SetStreamResponseBody (client/client.go:538-538)
  SetStreamResponseBody enables or disables response body streaming.
  sig: Client.SetStreamResponseBody(enable bool)
  calls: StreamResponseBody

Client.StreamResponseBody (client/client.go:530-530)
  StreamResponseBody returns the current StreamResponseBody setting.
  called_by: SetStreamResponseBody

acquireResponseChan (client/core.go:249-249)
  acquireResponseChan returns an empty, non-closed *Response channel from the pool.
  called_by: execFunc
  raises: panic

releaseResponseChan (client/core.go:262-262)
  releaseResponseChan returns the *Response channel to the pool.
  sig: releaseResponseChan(ch chan *Response)
  called_by: execFunc

parserResponseCookie (client/hooks.go:320-320)
  parserResponseCookie parses the Set-Cookie headers from the response and stores them.
  sig: parserResponseCookie(c *Client, resp *Response, req *Request)

AcquireResponse (client/response.go:228-228)
  AcquireResponse returns a new (pooled) Response object.
  raises: panic

ReleaseResponse (client/response.go:238-238)
  ReleaseResponse returns the Response object to the pool.
  sig: ReleaseResponse(resp *Response)
  calls: Reset

Response.Body (client/response.go:88-88)
  Body returns the HTTP response body as a byte slice.
  called_by: String

Response.BodyStream (client/response.go:95-95)
  BodyStream returns the response body as a stream reader.
  called_by: IsStreaming

Response.CBOR (client/response.go:123-123)
  CBOR unmarshal the response body into the given interface{} using CBOR.
  sig: Response.CBOR(v any)

Response.Close (client/response.go:208-208)
  Close releases both the Request and Response objects back to their pools.

Response.Cookies (client/response.go:83-83)
  Cookies returns all cookies set by the response.

Response.Header (client/response.go:53-53)
  Header returns the value of the specified response header field.
  sig: Response.Header(key string)
  calls: String

Response.Headers (client/response.go:62-62)
  Headers returns all headers in the response using an iterator.
  calls: String

Response.IsStreaming (client/response.go:104-104)
  IsStreaming returns true if the response body is being streamed.
  calls: BodyStream

Response.JSON (client/response.go:114-114)
  JSON unmarshal the response body into the given interface{} using JSON.
  sig: Response.JSON(v any)

Response.Protocol (client/response.go:48-48)
  Protocol returns the HTTP protocol used for the request.

Response.Reset (client/response.go:193-193)
  Reset clears the Response object, making it ready for reuse.
  called_by: ReleaseResponse

Response.Save (client/response.go:144-144)
  Save writes the response body to a file or io.Writer.
  sig: Response.Save(v any)

Response.Status (client/response.go:38-38)
  Status returns the HTTP status message of the executed request.

Response.StatusCode (client/response.go:43-43)
  StatusCode returns the HTTP status code of the executed request.

Response.String (client/response.go:109-109)
  String returns the response body as a trimmed string.
  calls: Body
  called_by: Header, Headers

Response.XML (client/response.go:132-132)
  XML unmarshal the response body into the given interface{} using XML.
  sig: Response.XML(v any)

Response.setClient (client/response.go:28-28)
  setClient sets the client instance in the response.
  sig: Response.setClient(c *Client)

Response.setRequest (client/response.go:33-33)
  setRequest sets the request object in the response.
  sig: Response.setRequest(req *Request)

hostClientTransport.SetStreamResponseBody (client/transport.go:144-144)
  sig: hostClientTransport.SetStreamResponseBody(enable bool)

hostClientTransport.StreamResponseBody (client/transport.go:140-140)

lbClientTransport.SetStreamResponseBody (client/transport.go:223-223)
  sig: lbClientTransport.SetStreamResponseBody(enable bool)
  calls: forEachHostClient, Client

lbClientTransport.StreamResponseBody (client/transport.go:206-206)

-- GAPS
- Question mentions [apps, change, fiber, formatter, gets] — not found in focus or symbol index
- Module log/fiberlog_test.go matches question but has no focus detail
  > drill: log/fiberlog_test.go
- Module client/response_test.go matches question but has no focus detail
  > drill: client/response_test.go

--- CLUE FILE END ---

QUESTION: When a handler panics in Fiber, how is that turned into an HTTP response, and how can mounted sub-apps change which error formatter gets used?

Provide a detailed answer covering:
1. Which specific files and symbols are involved (cite from the clue)
2. How the mechanism works (based on what the clue tells you)
3. Any error handling, invariants, or safety properties visible in the clue
4. What the clue does NOT tell you (gaps in your understanding)

=== TASK 2: SCORE YOUR ANSWER ===

After writing your answer above, score it against these gold facts.
For EACH fact, state COVERED (your answer contains or can infer this) or
MISSED (your answer does not contain this). Be strict — vague proximity
is not coverage.

FACT 1: The recover middleware wraps c.Next in a defer/recover block; when a panic occurs it optionally emits a stack trace through StackTraceHandler and converts the recovered value into an error with PanicHandler instead of writing a response directly.
FACT 2: recover.DefaultPanicHandler preserves an existing error panic as-is, but wraps non-error panic values with fmt.Errorf so the rest of the pipeline always receives an error.
FACT 3: Fiber's constructor installs DefaultErrorHandler when Config.ErrorHandler is nil, so recovered errors flow into a default text/plain response path unless the app or sub-app configured its own handler.
FACT 4: App.ErrorHandler searches mounted sub-app prefixes and chooses the deepest matching sub-app's configured error handler when one exists; otherwise it falls back to the main app's configured handler, which is DefaultErrorHandler by default.

=== TASK 3: WRITE RESULTS TO FILE ===

After completing Tasks 1 and 2, create or append to the file:
`experiments/runs/blind-eval/blind-eval-results.jsonl`

Write ONE JSON line (append, do not overwrite) with this exact structure:
```json
{"task_id": "blind-fiber-2", "model": "<your model name>", "scores": [{"fact": 1, "verdict": "COVERED_or_MISSED", "reason": "..."}, {"fact": 2, "verdict": "COVERED_or_MISSED", "reason": "..."}, {"fact": 3, "verdict": "COVERED_or_MISSED", "reason": "..."}, {"fact": 4, "verdict": "COVERED_or_MISSED", "reason": "..."}], "total_covered": <count>, "total_facts": <total>, "sufficient": <true or false>}
```

Replace each score entry with your actual COVERED/MISSED judgment.

Also output the scoring block in your response for visibility:

```
=== BLIND SCORING ===
Task: blind-fiber-2
Model: [state which model you are]
FACT 1: [COVERED or MISSED] - [brief justification]
FACT 2: [COVERED or MISSED] - [brief justification]
FACT 3: [COVERED or MISSED] - [brief justification]
FACT 4: [COVERED or MISSED] - [brief justification]
Score: [count of COVERED]/[total]
Sufficient: [YES if >= 60%, NO otherwise]
```
