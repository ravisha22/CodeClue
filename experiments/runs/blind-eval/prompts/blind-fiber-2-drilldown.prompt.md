# Blind Evaluation Prompt - MRLF v2.1
# Task: blind-fiber-2

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

--- CLUE FILE START ---
=CC v2.1 fiber@HEAD 243mod 3893sym
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
DefaultReq.Body                     M req.go:149    Body contains the raw body submitted in a POST ...
DefaultReq.getBody                  M req.go:1140   function DefaultReq.getBody
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
FormData.Set                        M client/request.go:893    Set sets a single form field, overriding previo...
DefaultCtx.String                   M ctx.go:571    String returns unique string representation of ...
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
standardClientTransport.Do          M client/transport.go:50     function standardClientTransport.Do
standardClientTransport.DoDeadline  M client/transport.go:58     function standardClientTransport.DoDeadline
standardClientTransport.DoTimeout   M client/transport.go:54     function standardClientTransport.DoTimeout
DefaultCtx.GetHeaders               M ctx.go:207    GetHeaders returns the HTTP request headers.
indexedHeap.removeInternal          M middleware/cache/heap.go:84     function indexedHeap.removeInternal
cachedHeader.Msgsize                M middleware/cache/manager_msgp.go:170    Msgsize returns an upper bound estimate of the ...
  ...and 1398 more symbols

-- FOCUS
standardClientTransport (client/transport.go:42-42)
  standardClientTransport adapts fasthttp.Client to the httpClientTransport interface used by Fiber's client helpers.
  methods: Client, CloseIdleConnections, Do, DoDeadline, DoRedirects, DoTimeout

hostClientTransport (client/transport.go:96-96)
  hostClientTransport adapts fasthttp.HostClient to the httpClientTransport interface used by Fiber's client helpers.
  methods: Client, CloseIdleConnections, Do, DoDeadline, DoRedirects, DoTimeout

lbClientTransport (client/transport.go:150-150)
  lbClientTransport adapts fasthttp.LBClient to the httpClientTransport interface used by Fiber's client helpers.
  methods: Client, CloseIdleConnections, Do, DoDeadline, DoRedirects, DoTimeout

App.mountStartupProcess (mount.go:113-114)
  mountStartupProcess Handles the startup process of mounted apps by appending sub-app routes, generating app list keys, a
  calls: appendSubAppLists, generateAppListKeys, hasMountedApps, processSubAppsRoutes

FiberHandlerFunc (middleware/adaptor/adaptor.go:199-199)
  FiberHandlerFunc wraps fiber handler to net/http handler func
  sig: FiberHandlerFunc(h fiber.Handler)
  calls: handlerFunc
  called_by: FiberHandler

HTTPHandler (middleware/adaptor/adaptor.go:56-56)
  HTTPHandler wraps net/http handler to fiber handler
  sig: HTTPHandler(h http.Handler)
  called_by: HTTPHandlerFunc, HTTPHandlerWithContext

FiberApp (middleware/adaptor/adaptor.go:204-204)
  FiberApp wraps fiber app to net/http handler func
  sig: FiberApp(app *fiber.App)
  calls: handlerFunc

FiberHandler (middleware/adaptor/adaptor.go:194-194)
  FiberHandler wraps fiber handler to net/http handler
  sig: FiberHandler(h fiber.Handler)
  calls: FiberHandlerFunc

HTTPHandlerFunc (middleware/adaptor/adaptor.go:51-51)
  HTTPHandlerFunc wraps net/http handler func to fiber handler
  sig: HTTPHandlerFunc(h http.HandlerFunc)
  calls: HTTPHandler

defaultErrorHandler (middleware/csrf/config.go:142-142)
  defaultErrorHandler is the default error handler that processes errors from fiber.Handler.
  sig: defaultErrorHandler(_ fiber.Ctx, _ error)

wrapHTTPHandler (adapter.go:246-246)
  wrapHTTPHandler adapts a net/http handler to a Fiber handler.
  sig: wrapHTTPHandler(handler http.Handler)

Client (client/client.go:37-37)
  Client provides Fiber's high-level HTTP API while delegating transport work to fasthttp.Client, fasthttp.HostClient, or 
  methods: AddHeader, AddHeaders, AddParam, AddParams, AddRequestHook, AddResponseHook
  called_by: Custom, Delete, Get, Head, Options, Patch, Post, Put

State (state.go:21-21)
  State is a key-value store for Fiber's app in order to be used as a global storage for the app's dependencies.
  methods: Delete, Get, GetBool, GetComplex128, GetComplex64, GetFloat32

App.serverErrorHandler (app.go:1411-1411)
  serverErrorHandler is a wrapper around the application's error handler method user for the fasthttp server configuration
  sig: App.serverErrorHandler(fctx *fasthttp.RequestCtx, err error)
  behavior: UNWIND(defer); DISPATCH(switch)
  calls: Error, NewError

DefaultRes.Attachment (res.go:207-207)
  Attachment sets the HTTP response Content-Disposition header field to attachment.
  sig: DefaultRes.Attachment(filename ...string)
  calls: Type, fallbackFilenameIfInvalid, sanitizeFilename

DefaultRes.SendStatus (res.go:979-979)
  SendStatus sets the HTTP status code and if the response body is empty, it sets the correct status message in the body.
  sig: DefaultRes.SendStatus(status int)
  behavior: PRECEDENCE(if_chain)
  calls: Status, statusDisallowsBody

HeaderBinding (binder/header.go:9-9)
  HeaderBinding is the binder implementation used to populate values from HTTP headers.
  methods: Bind, Reset

Do (middleware/proxy/proxy.go:146-146)
  Do performs the given http request and fills the given http response.
  sig: Do(c fiber.Ctx, addr string, clients ...*fasthttp.Client)
  called_by: DomainForward, Forward

DefaultCtx.GetRespHeader (ctx.go:222-222)
  GetRespHeader returns the HTTP response header specified by field.
  sig: DefaultCtx.GetRespHeader(key string, defaultValue ...string)
  calls: Get
  called_by: RequestID

Ctx (ctx_interface_gen.go:18-18)
  Ctx represents the Context which hold the HTTP request and response.

ResFmt (res.go:121-121)
  ResFmt associates a Content Type to a fiber.Handler for c.Format

httpClientTransport (client/transport.go:26-26)
  httpClientTransport unifies the operations exposed by the Fiber client across the fasthttp.Client, fasthttp.HostClient, 

sendFileStore (res.go:66-66)
  sendFileStore is used to keep the SendFile configuration and the handler.
  methods: configEqual

App.All (app.go:961-961)
  All will register the handler on all HTTP methods
  sig: App.All(path string, handler any, handlers ...any)
  calls: Add

App.ErrorHandler (app.go:1376-1376)
  ErrorHandler is the application's method in charge of finding the appropriate handler for the given request.
  sig: App.ErrorHandler(ctx Ctx, err error)
  behavior: PRECEDENCE(if_chain); ACCUMULATE(loop)

App.Group (app.go:969-969)
  Group is used for Routes with common prefix to define a new sub-router with optional middleware.
  sig: App.Group(prefix string, handlers ...any)

App.MountPath (mount.go:103-104)
  MountPath returns the route pattern where the current app instance was mounted as a sub-application.

App.Test (app.go:1199-1199)
  Test is used for internal debugging by passing a *http.Request.
  sig: App.Test(req *http.Request, config ...TestConfig)
  behavior: GUARD(err); PRECEDENCE(if_chain); ACCUMULATE(loop)

App.appendSubAppLists (mount.go:139-139)
  appendSubAppLists supports nested for sub apps
  sig: App.appendSubAppLists(appList map[string]*App, parent ...string)
  behavior: ACCUMULATE(loop)
  called_by: mountStartupProcess

App.hasMountedApps (mount.go:108-109)
  hasMountedApps Checks if there are any mounted apps in the current application.
  called_by: mountStartupProcess

App.processSubAppsRoutes (mount.go:168-169)
  processSubAppsRoutes adds routes of sub-apps recursively when the server is started
  behavior: ACCUMULATE(loop)
  called_by: mountStartupProcess

ConvertRequest (middleware/adaptor/adaptor.go:89-89)
  ConvertRequest converts a fiber.Ctx to a http.Request.
  sig: ConvertRequest(c fiber.Ctx, forServer bool)

DefaultCtx.GetRespHeaders (ctx.go:229-229)
  GetRespHeaders returns the HTTP response headers.
  calls: GetHeaders

DefaultCtx.Status (ctx.go:563-563)
  Status sets the HTTP status for the response.
  sig: DefaultCtx.Status(status int)

DefaultErrorHandler (middleware/session/config.go:109-109)
  DefaultErrorHandler logs the error and sends a 500 status code.
  sig: DefaultErrorHandler(c fiber.Ctx, err error)

DefaultErrorHandler (app.go:524-524)
  DefaultErrorHandler that process return errors from handlers
  sig: DefaultErrorHandler(c Ctx, err error)

DefaultPanicHandler (middleware/recover/recover.go:16-16)
  DefaultPanicHandler returns r directly if it's an error, and creates a new one with the %v verb otherwise.
  sig: DefaultPanicHandler(_ fiber.Ctx, r any)

DefaultRes.Append (res.go:140-140)
  Append the specified value to the HTTP response header field.
  sig: DefaultRes.Append(field string, values ...string)
  behavior: ACCUMULATE(loop)
  called_by: Vary

DefaultRes.GetHeaders (res.go:483-483)
  GetHeaders (a.k.a GetRespHeaders) returns the HTTP response headers.
  behavior: ACCUMULATE(loop)

DefaultRes.Links (res.go:603-603)
  Links joins the links followed by the property to populate the response's Link HTTP header field.
  sig: DefaultRes.Links(link ...string)
  behavior: ACCUMULATE(loop)

DefaultRes.Location (res.go:624-624)
  Location sets the response Location HTTP header to the specified path parameter.
  sig: DefaultRes.Location(path string)
  calls: setCanonical

DefaultRes.Send (res.go:762-762)
  Send sets the HTTP response body without copying it.
  sig: DefaultRes.Send(body []byte)

DefaultRes.SendString (res.go:997-997)
  SendString sets the HTTP response body for string types.
  sig: DefaultRes.SendString(body string)

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 20 with behavior annotations
drill: client/transport.go (~1 lines, standardClientTransport)
drill: client/transport.go (~1 lines, hostClientTransport)
drill: client/transport.go (~1 lines, lbClientTransport)

--- CLUE FILE END ---

QUESTION: When a handler panics in Fiber, how is that turned into an HTTP response, and how can mounted sub-apps change which error formatter gets used?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
