# Blind Evaluation Prompt - MRLF v2.1 with File 2 Drill-Down
# Task: blind-fiber-2

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

--- CLUE FILE (File 1) ---
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
DefaultReq.Accepts                  M req.go:51     Accepts checks if the specified extensions or c...
manager.logKey                      M middleware/cache/manager.go:210    function manager.logKey
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
Error (app.go:62-63)
  Error represents an error that occurred while handling a request.
  methods: Error
  called_by: serverErrorHandler, DefaultErrorHandler

handlerFunc (middleware/adaptor/adaptor.go:242-242)
  sig: handlerFunc(app *fiber.App, h ...fiber.Handler)
  calls: resolveRemoteAddr
  called_by: FiberApp, FiberHandlerFunc
  raises: panic

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

App.processSubAppsRoutes (mount.go:168-169)
  processSubAppsRoutes adds routes of sub-apps recursively when the server is started
  behavior: ACCUMULATE(hasMountedApps loop -> result)
  calls: hasMountedApps
  called_by: mountStartupProcess

App.ErrorHandler (app.go:1376-1376)
  ErrorHandler is the application's method in charge of finding the appropriate handler for the given request.
  sig: App.ErrorHandler(ctx Ctx, err error)
  behavior: GUARD(mountedErrHandler != nil -> return mountedErrHa...); ACCUMULATE(AddTrailingSlashStrin... -> result)
  called_by: serverErrorHandler

App.serverErrorHandler (app.go:1411-1411)
  serverErrorHandler is a wrapper around the application's error handler method user for the fasthttp server configuration
  sig: App.serverErrorHandler(fctx *fasthttp.RequestCtx, err error)
  behavior: UNWIND(defer)
  calls: ErrorHandler, Error, NewError

App.hasMountedApps (mount.go:108-109)
  hasMountedApps Checks if there are any mounted apps in the current application.
  behavior: DELEGATE(len -> result)
  called_by: mountStartupProcess, processSubAppsRoutes

NewError (app.go:1046-1046)
  NewError creates a new Error instance with an optional message
  sig: NewError(code int, message ...string)
  called_by: serverErrorHandler

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
  behavior: GUARD(handler == nil -> return nil)
  called_by: adaptHTTPHandler

HTTPHandler (middleware/adaptor/adaptor.go:56-56)
  HTTPHandler wraps net/http handler to fiber handler
  sig: HTTPHandler(h http.Handler)
  called_by: HTTPHandlerFunc, HTTPMiddleware

HTTPHandlerFunc (middleware/adaptor/adaptor.go:51-51)
  HTTPHandlerFunc wraps net/http handler func to fiber handler
  sig: HTTPHandlerFunc(h http.HandlerFunc)
  behavior: DELEGATE(HTTPHandler -> result)
  calls: HTTPHandler

toFiberHandler (adapter.go:13-13)
  toFiberHandler converts a supported handler type to a Fiber handler.
  sig: toFiberHandler(handler any)
  behavior: GUARD(handler == nil -> return nil, false); DISPATCH(handler)
  calls: adaptExpressHandler, adaptFastHTTPHandler, adaptFiberHandler, adaptHTTPHandler
  called_by: collectHandlers

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

DefaultPanicHandler (middleware/recover/recover.go:16-16)
  DefaultPanicHandler returns r directly if it's an error, and creates a new one with the %v verb otherwise.
  sig: DefaultPanicHandler(_ fiber.Ctx, r any)
  behavior: GUARD(err, ok := r.(error); ok -> return err)

App.appendSubAppLists (mount.go:139-139)
  appendSubAppLists supports nested for sub apps
  sig: App.appendSubAppLists(appList map[string]*App, parent ...string)
  behavior: ACCUMULATE(getGroupPath loop -> result)
  called_by: mountStartupProcess

Response.Protocol (client/response.go:48-48)
  Protocol returns the HTTP protocol used for the request.
  behavior: DELEGATE(string -> result)

httpClientTransport (client/transport.go:26-26)
  httpClientTransport unifies the operations exposed by the Fiber client across the fasthttp.Client, fasthttp.HostClient, 

collectHandlers (adapter.go:262-262)
  collectHandlers converts a slice of handler arguments to Fiber handlers.
  sig: collectHandlers(context string, args ...any)
  behavior: ACCUMULATE(toFiberHandler loop -> handlers, raises fmt.Sprintf("%s:...)
  calls: toFiberHandler
  raises: panic

HTTPMiddleware (middleware/adaptor/adaptor.go:162-162)
  HTTPMiddleware wraps net/http middleware to fiber middleware
  sig: HTTPMiddleware(mw func(http.Handler)
  calls: CopyContextToFiberContext, HTTPHandler

HandlerFromContext (middleware/csrf/csrf.go:238-238)
  HandlerFromContext returns the Handler found in the context.
  sig: HandlerFromContext(ctx any)
  behavior: GUARD(handler, ok := fiber.ValueFromContext[*Handle... -> return handler)

Response.BodyStream (client/response.go:95-95)
  BodyStream returns the response body as a stream reader.
  behavior: GUARD(stream := r.RawResponse.BodyStream(); stream... -> return stream)
  calls: Body
  called_by: IsStreaming, Save

Response.IsStreaming (client/response.go:104-104)
  IsStreaming returns true if the response body is being streamed.
  behavior: DELEGATE(r.RawResponse.BodyStream -> result)
  calls: BodyStream

acquireResponseChan (client/core.go:249-249)
  acquireResponseChan returns an empty, non-closed *Response channel from the pool.
  behavior: GUARD(!ok -> panic(errResponseCh...)
  called_by: execFunc
  raises: panic

Client.StreamResponseBody (client/client.go:530-530)
  StreamResponseBody returns the current StreamResponseBody setting.
  behavior: DELEGATE(c.transport.StreamResponseBody -> result)

Response.StatusCode (client/response.go:43-43)
  StatusCode returns the HTTP status code of the executed request.
  behavior: DELEGATE(r.RawResponse.StatusCode -> result)

Response (client/response.go:19-19)
  Response represents the result of a request.
  methods: Body, BodyStream, CBOR, Close, Cookies, Header

Response.Close (client/response.go:208-208)
  Close releases both the Request and Response objects back to their pools.
  calls: ReleaseResponse
  called_by: Save

Response.Save (client/response.go:144-144)
  Save writes the response body to a file or io.Writer.
  sig: Response.Save(v any)
  behavior: DISPATCH(p)
  calls: BodyStream, Close

newBindError (bind.go:102-102)
  sig: newBindError(source string, raw error)
  calls: extractFieldFromError
  called_by: returnBindErr

ReleaseResponse (client/response.go:238-238)
  ReleaseResponse returns the Response object to the pool.
  sig: ReleaseResponse(resp *Response)
  calls: Reset
  called_by: Close

Response.Reset (client/response.go:193-193)
  Reset clears the Response object, making it ready for reuse.
  behavior: ACCUMULATE(ReleaseCookie loop -> result)
  called_by: ReleaseResponse

Response.CBOR (client/response.go:123-123)
  CBOR unmarshal the response body into the given interface{} using CBOR.
  sig: Response.CBOR(v any)
  behavior: GUARD(r.client == nil -> return ErrClientNil)
  calls: Body

Response.JSON (client/response.go:114-114)
  JSON unmarshal the response body into the given interface{} using JSON.
  sig: Response.JSON(v any)
  behavior: GUARD(r.client == nil -> return ErrClientNil)
  calls: Body

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 44 with behavior annotations
uncovered: DefaultCtx.setIndexHandler, Error, PreStartupMessageData.AddError, beforeHandlerFunc
drill: middleware/adaptor/adaptor.go (~1 lines, FiberHandlerFunc)
drill: middleware/adaptor/adaptor.go (~1 lines, FiberHandler)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## FiberHandlerFunc  (middleware/adaptor/adaptor.go L199-199)
```
func FiberHandlerFunc(h fiber.Handler) http.HandlerFunc {
```

## FiberHandler  (middleware/adaptor/adaptor.go L194-194)
```
func FiberHandler(h fiber.Handler) http.Handler {
```

## handlerFunc  (middleware/adaptor/adaptor.go L242-242)
```
func handlerFunc(app *fiber.App, h ...fiber.Handler) http.HandlerFunc {
```

## ConvertRequest  (middleware/adaptor/adaptor.go L89-89)
```
func ConvertRequest(c fiber.Ctx, forServer bool) (*http.Request, error) {
```

## CopyContextToFiberContext  (middleware/adaptor/adaptor.go L101-101)
```
func CopyContextToFiberContext(src any, requestContext *fasthttp.RequestCtx) {
```

## FiberApp  (middleware/adaptor/adaptor.go L204-204)
```
func FiberApp(app *fiber.App) http.HandlerFunc {
```

## HTTPHandler  (middleware/adaptor/adaptor.go L56-56)
```
func HTTPHandler(h http.Handler) fiber.Handler {
```

## HTTPHandlerFunc  (middleware/adaptor/adaptor.go L51-51)
```
func HTTPHandlerFunc(h http.HandlerFunc) fiber.Handler {
```

## HTTPHandlerWithContext  (middleware/adaptor/adaptor.go L65-65)
```
func HTTPHandlerWithContext(h http.Handler) fiber.Handler {
```

## HTTPMiddleware  (middleware/adaptor/adaptor.go L162-162)
```
func HTTPMiddleware(mw func(http.Handler) http.Handler) fiber.Handler {
```

## LocalContextFromHTTPRequest  (middleware/adaptor/adaptor.go L78-78)
```
func LocalContextFromHTTPRequest(r *http.Request) (context.Context, bool) {
```

## disableLogger  (middleware/adaptor/adaptor.go L21-21)
```
type disableLogger struct{}
```

## isUnixNetwork  (middleware/adaptor/adaptor.go L208-208)
```
func isUnixNetwork(network string) bool {
```

## resolveRemoteAddr  (middleware/adaptor/adaptor.go L212-212)
```
func resolveRemoteAddr(remoteAddr string, localAddr any) (net.Addr, error) {
```
--- END SOURCE SNIPPETS ---

QUESTION: When a handler panics in Fiber, how is that turned into an HTTP response, and how can mounted sub-apps change which error formatter gets used?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
