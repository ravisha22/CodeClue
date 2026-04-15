# Blind Evaluation Prompt - MRLF v2.1
# Task: blind-fiber-2

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

--- CLUE FILE START ---
=CC v2.1 fiber@HEAD 148mod 1472sym
? When a handler panics in Fiber, how is that turned into an HTTP response, and how can mounted sub-apps change which error formatter gets used?


-- TREE
addon/  (2 files)
binder/  (12 files)
client/  (8 files)
extractors/  (1 files)
internal/  (4 files)
log/  (3 files)
middleware/  (87 files)

-- INDEX
path.go                                         844L  CheckConstraint, Constraint, CustomConstraint, GetTrimmedParam, RemoveEscapeChar
client/client.go                                863L  C, AddHeader, AddHeaders, AddParam, AddParams
bind.go                                         477L  AcquireBind, All, Body, CBOR, Cookie
client/request.go                              1122L  AcquireFile, AcquireRequest, Add, All, Del
res.go                                         1153L  Cookie, App, Append, Attachment, AutoFormat
client/transport.go                             377L  composeRedirectURL, doRedirectsWithClient, extractTLSConfig, forEachHostClient, Client
binder/form.go                                  124L  Bind, Reset, bindMultipart, FormBinding, acquireFileHeaderMap
app.go                                         1486L  Add, All, Config, Connect, Delete
client/cookiejar.go                             334L  AcquireCookieJar, Get, Release, Set, SetByHost
client/core.go                                  304L  acquireErrChan, acquireResponseChan, addMissingPort, afterHooks, execFunc
internal/storage/memory/memory.go               233L  Entry, New, Close, Conn, Delete
domain.go                                       688L  DomainParam, domainCheckResult, domainLocalsKeyType, match, domainMatcher
middleware/paginate/page_info.go                190L  NewPageInfo, CursorValues, NextCursorURL, NextCursorURLWithKeys, NextPageURL
middleware/csrf/csrf.go                         403L  DeleteToken, Handler, HandlerFromContext, New, TokenFromContext
redirect.go                                     433L  AcquireRedirect, FlashMessage, OldInputData, Back, Message
client/response.go                              241L  AcquireResponse, ReleaseResponse, Body, BodyStream, CBOR
  ...and 132 more modules

-- SYM
domainRouter.Add                    M domain.go:530    Add allows you to specify multiple HTTP methods...
Client.applyTLSConfig               M client/client.go:103    function Client.applyTLSConfig
Client.SetTLSConfig                 M client/client.go:249    SetTLSConfig sets the TLS configuration for the...
App.Add                             M app.go:953    Add allows you to specify multiple HTTP methods...
Cookie.Add                          M client/request.go:781    Add adds a cookie key-value pair.
Group.Add                           M group.go:167    Add allows you to specify multiple HTTP methods...
C                                   M client/client.go:810    C returns the default client.
Client.applyDial                    M client/client.go:107    function Client.applyDial
Client.SetDial                      M client/client.go:606    SetDial sets the custom dial function for the c...
Registering.Add                     M register.go:111    Add allows you to specify multiple HTTP methods...
walkBalancingClientWithBreak        M client/transport.go:268    walkBalancingClientWithBreak traverses balancin...
defaultLogger.privateLog            M log/default.go:24     privateLog logs a message at a given level log ...
defaultLogger.privateLogf           M log/default.go:47     privateLogf logs a formatted message at a given...
defaultLogger.privateLogw           M log/default.go:74     privateLogw logs a message at a given level log...
Client.TLSConfig                    M client/client.go:236    TLSConfig returns the client's TLS configuration.
Cookie.All                          M client/request.go:816    All returns an iterator over cookie key-value p...
pathMatch                           M client/cookiejar.go:307    pathMatch determines whether the request path m...
Cookie.Del                          M client/request.go:786    Del deletes a cookie by key.
isASCIIAlphanumeric                 M domain.go:217    isASCIIAlphanumeric returns true if the rune is...
domainRouter.wrapHandlers           M domain.go:278    wrapHandlers wraps every handler in the slice w...
MemoryLock.Lock                     M middleware/idempotency/locker.go:25     Lock acquires the lock for the provided key, cr...
MemoryLock.Unlock                   M middleware/idempotency/locker.go:41     Unlock releases the lock associated with the pr...
Response.Body                       M client/response.go:88     Body returns the HTTP response body as a byte s...
domainRouter.registerGroup          M domain.go:336    registerGroup returns the group to associate wi...
domainRouter.registerPath           M domain.go:327    registerPath returns the full path for registra...
FormData.Set                        M client/request.go:893    Set sets a single form field, overriding previo...
App.normalizePath                   M router.go:398    function App.normalizePath
domainRouter.Name                   M domain.go:602    Name assigns a name to the most recently regist...
ReleaseFile                         M client/request.go:1053   ReleaseFile returns the File object to the pool.
buildPaginationURL                  M middleware/paginate/page_info.go:121    buildPaginationURL parses baseURL and sets/repl...
DefaultReq.Get                      M req.go:427    Get returns the HTTP request header specified b...
Request.Reset                       M client/request.go:680    Reset clears the Request object, returning it t...
Session.Get                         M middleware/session/session.go:74     Release releases the session back to the pool.
App.pruneAutoHeadRouteLocked        M router.go:491    pruneAutoHeadRouteLocked removes an automatical...
Request.resetBody                   M client/request.go:438    resetBody clears the existing body.
newClient                           M client/client.go:783    function newClient
searchCookieByKeyAndPath            M client/cookiejar.go:294    searchCookieByKeyAndPath looks up a cookie by i...
setConfigToRequest                  M client/client.go:672    setConfigToRequest sets the parameters passed v...
Request.Send                        M client/request.go:673    Send executes the Request.
Request.SetMethod                   M client/request.go:82     SetMethod sets the HTTP method for the Request.
Request.SetURL                      M client/request.go:93     SetURL sets the URL for the Request.
Bind.validateStruct                 M bind.go:183    Struct validation.
SetValWithStruct                    M client/request.go:1066   SetValWithStruct sets values using a struct.
domainMatcher.match                 M domain.go:139    match checks if a hostname matches the domain p...
Bind.returnBindErr                  M bind.go:171    returnBindErr runs returnErr and, if the result...
manager.logKey                      M middleware/cache/manager.go:210    function manager.logKey
DefaultReq.Accepts                  M req.go:51     Accepts checks if the specified extensions or c...
walkBalancingClient                 M client/transport.go:239    walkBalancingClient traverses balancing clients...
isUnixNetwork                       M middleware/adaptor/adaptor.go:208    function isUnixNetwork
Session.Reset                       M middleware/session/session.go:247    Reset generates a new session id, deletes the o...
DefaultReq.Body                     M req.go:149    Body contains the raw body submitted in a POST ...
forEachHostClient                   M client/transport.go:231    forEachHostClient applies fn to every host clie...
Do                                  M middleware/proxy/proxy.go:146    Do performs the given http request and fills th...
Client.currentTLSConfig             M client/client.go:99     function Client.currentTLSConfig
CookieJar.cookiesForRequest         M client/cookiejar.go:103    cookiesForRequest returns cookies that match th...
resolveRemoteAddr                   M middleware/adaptor/adaptor.go:212    function resolveRemoteAddr
Bind                                C bind.go:40     Bind provides helper methods for binding reques...
Request.Put                         M client/request.go:648    Put sends a PUT request to the given URL.
parseUintDirective                  M middleware/cache/cache.go:937    function parseUintDirective
BindError.Error                     M bind.go:65     function BindError.Error
DefaultReq.IsProxyTrusted           M req.go:1080   IsProxyTrusted checks trustworthiness of remote...
Session.refresh                     M middleware/session/session.go:278    refresh generates a new session, and sets sessi...
DefaultReq.getBody                  M req.go:1140   function DefaultReq.getBody
CookieJar.SetByHost                 M client/cookiejar.go:154    SetByHost stores the given cookies for the spec...
PreStartupMessageData.addEntry      M hooks.go:164    function PreStartupMessageData.addEntry
decodeKey                           M middleware/encryptcookie/utils.go:20     decodeKey decodes the provided base64-encoded k...
DefaultCtx.MediaType                M req.go:244    MediaType returns the MIME type from the Conten...
Request.Get                         M client/request.go:633    Get sends a GET request to the given URL.
extractFieldFromError               M bind.go:76     function extractFieldFromError
standardClientTransport.Do          M client/transport.go:50     function standardClientTransport.Do
DefaultCtx.Get                      M ctx.go:200    Get returns the HTTP request header specified b...
redirectionMsg.Msgsize              M redirect_msgp.go:196    Msgsize returns an upper bound estimate of the ...
  ...and 1400 more symbols

-- FOCUS
FiberHandler (middleware/adaptor/adaptor.go:194-194)
  FiberHandler wraps fiber handler to net/http handler
  sig: FiberHandler(h fiber.Handler)
  behavior: DELEGATE(FiberHandlerFunc -> result)
  calls: FiberHandlerFunc

FiberHandlerFunc (middleware/adaptor/adaptor.go:199-199)
  FiberHandlerFunc wraps fiber handler to net/http handler func
  sig: FiberHandlerFunc(h fiber.Handler)
  behavior: DELEGATE(handlerFunc -> result)
  calls: handlerFunc
  called_by: FiberHandler

defaultErrorHandler (middleware/csrf/config.go:142-142)
  defaultErrorHandler is the default error handler that processes errors from fiber.Handler.
  sig: defaultErrorHandler(_ fiber.Ctx, _ error)

FiberApp (middleware/adaptor/adaptor.go:204-204)
  FiberApp wraps fiber app to net/http handler func
  sig: FiberApp(app *fiber.App)
  behavior: DELEGATE(handlerFunc -> result)
  calls: handlerFunc

wrapHTTPHandler (adapter.go:246-246)
  wrapHTTPHandler adapts a net/http handler to a Fiber handler.
  sig: wrapHTTPHandler(handler http.Handler)
  behavior: GUARD(handler -> none)
  called_by: adaptHTTPHandler

App.mountStartupProcess (mount.go:113-114)
  mountStartupProcess Handles the startup process of mounted apps by appending sub-app routes, generating app list keys, a
  calls: appendSubAppLists, generateAppListKeys, hasMountedApps, processSubAppsRoutes

HTTPHandler (middleware/adaptor/adaptor.go:56-56)
  HTTPHandler wraps net/http handler to fiber handler
  sig: HTTPHandler(h http.Handler)
  called_by: HTTPHandlerFunc, HTTPMiddleware

lbClientTransport (client/transport.go:150-150)
  lbClientTransport adapts fasthttp.LBClient to the httpClientTransport interface used by Fiber's client helpers.
  methods: Client, CloseIdleConnections, Do, DoDeadline, DoRedirects, DoTimeout

standardClientTransport (client/transport.go:42-42)
  standardClientTransport adapts fasthttp.Client to the httpClientTransport interface used by Fiber's client helpers.
  methods: Client, CloseIdleConnections, Do, DoDeadline, DoRedirects, DoTimeout

hostClientTransport (client/transport.go:96-96)
  hostClientTransport adapts fasthttp.HostClient to the httpClientTransport interface used by Fiber's client helpers.
  methods: Client, CloseIdleConnections, Do, DoDeadline, DoRedirects, DoTimeout

HTTPHandlerFunc (middleware/adaptor/adaptor.go:51-51)
  HTTPHandlerFunc wraps net/http handler func to fiber handler
  sig: HTTPHandlerFunc(h http.HandlerFunc)
  behavior: DELEGATE(HTTPHandler -> result)
  calls: HTTPHandler

App.ErrorHandler (app.go:1376-1376)
  ErrorHandler is the application's method in charge of finding the appropriate handler for the given request.
  sig: App.ErrorHandler(ctx Ctx, err error)
  behavior: GUARD(mountedErrHandler -> wrap_mountedErrHandler); ACCUMULATE(loop -> result)
  called_by: serverErrorHandler

toFiberHandler (adapter.go:13-13)
  toFiberHandler converts a supported handler type to a Fiber handler.
  sig: toFiberHandler(handler any)
  behavior: GUARD(handler -> pass_through); DISPATCH(handler)
  calls: adaptExpressHandler, adaptFastHTTPHandler, adaptFiberHandler, adaptHTTPHandler
  called_by: collectHandlers

App.serverErrorHandler (app.go:1411-1411)
  serverErrorHandler is a wrapper around the application's error handler method user for the fasthttp server configuration
  sig: App.serverErrorHandler(fctx *fasthttp.RequestCtx, err error)
  behavior: UNWIND(defer)
  calls: ErrorHandler, Error, NewError

App.hasMountedApps (mount.go:108-109)
  hasMountedApps Checks if there are any mounted apps in the current application.
  behavior: DELEGATE(len -> result)
  called_by: mountStartupProcess, processSubAppsRoutes

App.processSubAppsRoutes (mount.go:168-169)
  processSubAppsRoutes adds routes of sub-apps recursively when the server is started
  behavior: ACCUMULATE(loop -> result)
  calls: hasMountedApps
  called_by: mountStartupProcess

DefaultErrorHandler (app.go:524-524)
  DefaultErrorHandler that process return errors from handlers
  sig: DefaultErrorHandler(c Ctx, err error)
  behavior: DELEGATE(c.Status -> result)
  calls: Error

adaptFiberHandler (adapter.go:32-32)
  sig: adaptFiberHandler(handler any)
  behavior: DISPATCH(h)
  called_by: toFiberHandler

DefaultErrorHandler (middleware/session/config.go:109-109)
  DefaultErrorHandler logs the error and sends a 500 status code.
  sig: DefaultErrorHandler(c fiber.Ctx, err error)

Response.Body (client/response.go:88-88)
  Body returns the HTTP response body as a byte slice.
  behavior: DELEGATE(r.RawResponse.Body -> result)
  called_by: BodyStream, CBOR, JSON, String, XML

App.appendSubAppLists (mount.go:139-139)
  appendSubAppLists supports nested for sub apps
  sig: App.appendSubAppLists(appList map[string]*App, parent ...string)
  behavior: ACCUMULATE(loop -> result)
  called_by: mountStartupProcess

Response.Protocol (client/response.go:48-48)
  Protocol returns the HTTP protocol used for the request.
  behavior: DELEGATE(string -> result)

httpClientTransport (client/transport.go:26-26)
  httpClientTransport unifies the operations exposed by the Fiber client across the fasthttp.Client, fasthttp.HostClient, 

DefaultPanicHandler (middleware/recover/recover.go:16-16)
  DefaultPanicHandler returns r directly if it's an error, and creates a new one with the %v verb otherwise.
  sig: DefaultPanicHandler(_ fiber.Ctx, r any)
  behavior: GUARD(err -> pass_through)

getEffectiveStatusCode (middleware/limiter/limiter.go:32-32)
  getEffectiveStatusCode returns the actual status code, considering both the error and response status
  sig: getEffectiveStatusCode(c fiber.Ctx, err error)
  behavior: GUARD(err -> fiberErr.Code)

Client (client/client.go:37-37)
  Client provides Fiber's high-level HTTP API while delegating transport work to fasthttp.Client, fasthttp.HostClient, or 
  methods: AddHeader, AddHeaders, AddParam, AddParams, AddRequestHook, AddResponseHook

DefaultRes.SendStatus (res.go:979-979)
  SendStatus sets the HTTP status code and if the response body is empty, it sets the correct status message in the body.
  sig: DefaultRes.SendStatus(status int)
  behavior: GUARD(statusDisallowsBody -> none); PRECEDENCE(statusDisallowsBody -> len)
  calls: SendString, Status, statusDisallowsBody
  called_by: Format

Do (middleware/proxy/proxy.go:146-146)
  Do performs the given http request and fills the given http response.
  sig: Do(c fiber.Ctx, addr string, clients ...*fasthttp.Client)
  called_by: Balancer, BalancerForward, DomainForward, Forward

DefaultRes.Append (res.go:140-140)
  Append the specified value to the HTTP response header field.
  sig: DefaultRes.Append(field string, values ...string)
  behavior: GUARD(len -> none); ACCUMULATE(loop -> h)
  calls: Set, headerContainsValue
  called_by: Vary

DefaultRes.SendString (res.go:997-997)
  SendString sets the HTTP response body for string types.
  sig: DefaultRes.SendString(body string)
  called_by: AutoFormat, SendStatus

HTTPMiddleware (middleware/adaptor/adaptor.go:162-162)
  HTTPMiddleware wraps net/http middleware to fiber middleware
  sig: HTTPMiddleware(mw func(http.Handler)
  calls: CopyContextToFiberContext, HTTPHandler

DefaultCtx.GetRespHeader (ctx.go:222-222)
  GetRespHeader returns the HTTP response header specified by field.
  sig: DefaultCtx.GetRespHeader(key string, defaultValue ...string)
  behavior: DELEGATE(c.DefaultRes.Get -> result)
  calls: Get
  called_by: RequestID

DefaultRes.Attachment (res.go:207-207)
  Attachment sets the HTTP response Content-Disposition header field to attachment.
  sig: DefaultRes.Attachment(filename ...string)
  behavior: GUARD(len -> none)
  calls: Type, setCanonical, fallbackFilenameIfInvalid, sanitizeFilename
  called_by: SendFile

DefaultRes.Set (res.go:1022-1022)
  Set sets the response's HTTP header field to the specified key, value.
  sig: DefaultRes.Set(key, val string)
  called_by: Append, SendFile

DefaultRes.Status (res.go:1032-1032)
  Status sets the HTTP status for the response.
  sig: DefaultRes.Status(status int)
  called_by: SendFile, SendStatus

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 80 symbols in L3, 43 with behavior annotations

--- CLUE FILE END ---

QUESTION: When a handler panics in Fiber, how is that turned into an HTTP response, and how can mounted sub-apps change which error formatter gets used?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
