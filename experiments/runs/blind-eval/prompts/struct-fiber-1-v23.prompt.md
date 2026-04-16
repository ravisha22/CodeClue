# Blind Evaluation Prompt - MRLF v2.4
# Task: struct-fiber-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 fiber@HEAD 148mod 1472sym
? What are the main source files and packages in the Fiber framework, and how is the middleware organized?


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
HTTPMiddleware (middleware/adaptor/adaptor.go:162-162)
  HTTPMiddleware wraps net/http middleware to fiber middleware
  sig: HTTPMiddleware(mw func(http.Handler)
  calls: CopyContextToFiberContext, HTTPHandler

FromContext (middleware/session/middleware.go:179-179)
  FromContext returns the Middleware from the Fiber context.
  sig: FromContext(ctx any)
  behavior: GUARD(m, ok := fiber.ValueFromContext[*Middleware](... -> return m)

CustomCtx (ctx_interface.go:13-14)
  CustomCtx extends Ctx with the additional methods required by Fiber's internals and middleware helpers.

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

CopyContextToFiberContext (middleware/adaptor/adaptor.go:101-101)
  CopyContextToFiberContext copies the values of context.Context to a fasthttp.RequestCtx.
  sig: CopyContextToFiberContext(src any, requestContext *fasthttp.RequestCtx)
  behavior: GUARD(requestContext == nil -> return); PRECEDENCE(requestContext -> not_v.IsValid -> t); ACCUMULATE(IsNil loop -> result)
  called_by: HTTPMiddleware

FiberApp (middleware/adaptor/adaptor.go:204-204)
  FiberApp wraps fiber app to net/http handler func
  sig: FiberApp(app *fiber.App)
  behavior: DELEGATE(handlerFunc -> result)
  calls: handlerFunc

toFiberHandler (adapter.go:13-13)
  toFiberHandler converts a supported handler type to a Fiber handler.
  sig: toFiberHandler(handler any)
  behavior: GUARD(handler == nil -> return nil, false); DISPATCH(handler)
  calls: adaptExpressHandler, adaptFastHTTPHandler, adaptFiberHandler, adaptHTTPHandler
  called_by: collectHandlers

Middleware.initialize (middleware/session/middleware.go:111-111)
  initialize sets up middleware for the request.
  sig: Middleware.initialize(c fiber.Ctx, cfg *Config)
  behavior: GUARD(err != nil -> panic(err)); UNWIND(defer)
  called_by: NewWithStore
  raises: panic

acquireMiddleware (middleware/session/middleware.go:141-141)
  acquireMiddleware retrieves a middleware instance from the pool.
  behavior: GUARD(!ok -> panic(ErrTypeAssert...)
  calls: Get
  called_by: NewWithStore
  raises: panic

adaptFiberHandler (adapter.go:32-32)
  sig: adaptFiberHandler(handler any)
  behavior: DISPATCH(h)
  called_by: toFiberHandler

releaseMiddleware (middleware/session/middleware.go:157-157)
  releaseMiddleware resets and returns middleware to the pool.
  sig: releaseMiddleware(m *Middleware)
  called_by: NewWithStore

Middleware (middleware/session/middleware.go:13-13)
  Middleware holds session data and configuration.
  methods: Delete, Destroy, Fresh, Get, ID, Keys

DefaultCtx.IsMiddleware (ctx.go:380-381)
  IsMiddleware returns true if the current request handler was registered as middleware.
  behavior: GUARD(c.route == nil -> return false); PRECEDENCE(c)

Request.AddFiles (client/request.go:585-585)
  AddFiles adds multiple files at once.
  sig: Request.AddFiles(files ...*File)
  calls: resetBody

Request.Files (client/request.go:556-556)
  Files returns all files added to the Request.

domainRouter.Use (domain.go:350-350)
  Use registers a middleware route that will match requests with the provided prefix (which is optional and defaults to "/
  sig: domainRouter.Use(args ...any)
  behavior: PRECEDENCE(len -> d); ACCUMULATE(toFiberHandler loop -> handlers, raises fmt.Sprintf("use:...)
  calls: Name, mount, registerGroup, registerPath, wrapHandlers
  raises: panic

New (middleware/limiter/limiter.go:23-23)
  New creates a new middleware handler
  sig: New(config ...Config)
  behavior: DELEGATE(cfg.LimiterMiddleware.New -> result)

NewWithStore (middleware/session/middleware.go:77-77)
  NewWithStore creates session middleware with an optional custom store.
  sig: NewWithStore(config ...Config)
  calls: initialize, saveSession, acquireMiddleware, releaseMiddleware
  called_by: New

HTTPHandler (middleware/adaptor/adaptor.go:56-56)
  HTTPHandler wraps net/http handler to fiber handler
  sig: HTTPHandler(h http.Handler)
  called_by: HTTPHandlerFunc, HTTPMiddleware

HTTPHandlerFunc (middleware/adaptor/adaptor.go:51-51)
  HTTPHandlerFunc wraps net/http handler func to fiber handler
  sig: HTTPHandlerFunc(h http.HandlerFunc)
  behavior: DELEGATE(HTTPHandler -> result)
  calls: HTTPHandler

HTTPHandlerWithContext (middleware/adaptor/adaptor.go:65-65)
  HTTPHandlerWithContext is like HTTPHandler, but additionally stores Fiber’s user context in the request context
  sig: HTTPHandlerWithContext(h http.Handler)
  calls: LocalContextFromHTTPRequest

LocalContextFromHTTPRequest (middleware/adaptor/adaptor.go:78-78)
  LocalContextFromHTTPRequest extracts the Fiber user context previously stored into r.Context() by the adaptor.
  sig: LocalContextFromHTTPRequest(r *http.Request)
  behavior: GUARD(r == nil -> return nil, false)
  called_by: HTTPHandlerWithContext

New (middleware/redirect/redirect.go:13-13)
  New creates a new middleware handler
  sig: New(config ...Config)
  behavior: ACCUMULATE(ReplaceAll loop -> k)
  calls: captureTokens

New (middleware/session/middleware.go:56-56)
  New initializes session middleware with optional configuration.
  sig: New(config ...Config)
  behavior: GUARD(len(config) > 0 -> return handler)
  calls: NewWithStore

New (middleware/rewrite/rewrite.go:12-12)
  New creates a new middleware handler
  sig: New(config ...Config)
  behavior: ACCUMULATE(ReplaceAll loop -> k)
  calls: captureTokens

captureTokens (middleware/rewrite/rewrite.go:41-41)
  https://github.com/labstack/echo/blob/master/middleware/rewrite.go
  sig: captureTokens(pattern *regexp.Regexp, input string)
  behavior: GUARD(groups == nil -> return nil); ACCUMULATE(Itoa loop -> result)
  called_by: New

captureTokens (middleware/redirect/redirect.go:46-46)
  https://github.com/labstack/echo/blob/master/middleware/rewrite.go
  sig: captureTokens(pattern *regexp.Regexp, input string)
  behavior: PRECEDENCE(len -> groups); ACCUMULATE(Itoa loop -> result)
  called_by: New

New (middleware/cache/cache.go:109-109)
  New creates a new middleware handler
  sig: New(config ...Config)
  calls: allowsSharedCacheDirectives, appendWarningHeaders, cacheBodyFetchError, cachedResponseAge, clampDateSeconds, hasDirective, isHeuristicFreshness, loadVaryManifest
  called_by: makeBuildVaryKeyFunc

New (middleware/csrf/csrf.go:50-50)
  New creates a new middleware handler
  sig: New(config ...Config)
  behavior: PRECEDENCE(cfg -> token); ACCUMULATE(TrimSpace loop -> trustedSubOrigins, raises "[CSRF] Invalid o...); DISPATCH(c)
  calls: createOrExtendTokenInStorage, deleteTokenFromStorage, expireCSRFCookie, getRawFromStorage, originMatchesHost, refererMatchesHost, updateCSRFCookie, validateSecFetchSite
  raises: panic

New (middleware/cors/cors.go:28-28)
  New creates a new middleware handler
  sig: New(config ...Config)
  behavior: PRECEDENCE(len -> cfg); ACCUMULATE(TrimSpace loop -> allowSubOrigins, raises "[CORS] Invalid o...)
  calls: isOriginSerializedOrNull, setPreflightHeaders, setSimpleHeaders
  raises: panic

New (middleware/static/static.go:121-121)
  New creates a new middleware handler.
  sig: New(root string, cfg ...Config)
  calls: isFile, sanitizePath

New (middleware/basicauth/basicauth.go:27-27)
  New creates a new middleware handler
  sig: New(config ...Config)
  calls: containsCTL, containsInvalidHeaderChars

New (middleware/compress/compress.go:54-54)
  New creates a new middleware handler
  sig: New(config ...Config)
  behavior: DISPATCH(cfg)
  calls: appendVaryAcceptEncoding, shouldSkip

Config (middleware/encryptcookie/config.go:8-8)
  Config defines the config for middleware.

Config (middleware/csrf/config.go:15-15)
  Config defines the config for CSRF middleware.

Config (middleware/keyauth/config.go:19-19)
  Config defines the config for middleware.

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 80 symbols in L3, 28 with behavior annotations
uncovered: Middleware.saveSession, Middleware.Get, Middleware.Delete, Middleware.Destroy

--- CLUE FILE END ---

QUESTION: What are the main source files and packages in the Fiber framework, and how is the middleware organized?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
