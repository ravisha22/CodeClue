# Blind Evaluation Prompt - MRLF v2.3 (File 1 Only — No Drill-Down)
# Task: blind-fiber-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a 'clue file') that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

--- CLUE FILE START ---
=CC v2.1 fiber@HEAD 148mod 1472sym
? If middleware rewrites the request path and wants Fiber to match routes again, how does the framework restart dispatch and decide whether the request becomes a normal match, a 404, or a 405?


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
RoutePatternMatch (path.go:155-155)
  RoutePatternMatch reports whether path matches the provided Fiber route pattern.
  sig: RoutePatternMatch(path, pattern string, cfg ...Config)
  behavior: PRECEDENCE(len -> path -> pattern); UNWIND(defer)
  calls: RemoveEscapeCharBytes, parseRoute, getMatch, reset

pathMatch (client/cookiejar.go:307-307)
  pathMatch determines whether the request path matches the cookie path according to RFC 6265 section 5.1.4.
  sig: pathMatch(reqPath, cookiePath []byte)
  behavior: PRECEDENCE(len -> bytes)
  called_by: cookiesForRequest, searchCookieByKeyAndPath

Request.DisablePathNormalizing (client/request.go:614-614)
  DisablePathNormalizing reports whether path normalizing is disabled for the Request.

CookieJar.cookiesForRequest (client/cookiejar.go:103-103)
  cookiesForRequest returns cookies that match the given host, path and security settings.
  sig: CookieJar.cookiesForRequest(host string, path []byte, secure bool)
  behavior: ACCUMULATE(loop -> kept); UNWIND(defer)
  calls: domainMatch, pathMatch
  called_by: getByHostAndPath

IsFromCache (middleware/idempotency/idempotency.go:29-29)
  IsFromCache reports whether the middleware served the response from the cache for the current request.
  sig: IsFromCache(c fiber.Ctx)
  behavior: DELEGATE(c.Locals -> result)

WasPutToCache (middleware/idempotency/idempotency.go:35-35)
  WasPutToCache reports whether the middleware stored the response produced by the current request in the cache.
  sig: WasPutToCache(c fiber.Ctx)
  behavior: GUARD(wasPut -> pass_through)

Group (group.go:14-15)
  Group represents a collection of routes that share middleware and a common path prefix.
  methods: Add, All, Connect, Delete, Domain, Get
  called_by: Route

Registering.All (register.go:50-50)
  All registers a middleware route that will match requests with the provided path which is stored in register struct.
  sig: Registering.All(handler any, handlers ...any)

CopyContextToFiberContext (middleware/adaptor/adaptor.go:101-101)
  CopyContextToFiberContext copies the values of context.Context to a fasthttp.RequestCtx.
  sig: CopyContextToFiberContext(src any, requestContext *fasthttp.RequestCtx)
  behavior: GUARD(requestContext -> none); PRECEDENCE(requestContext -> not_v.IsValid -> t); ACCUMULATE(loop -> result)
  called_by: HTTPMiddleware

isValidRequestID (middleware/requestid/requestid.go:61-61)
  isValidRequestID reports whether the request ID contains only visible ASCII characters (0x20–0x7E) and is non-empty.
  sig: isValidRequestID(rid string)
  behavior: GUARD(rid -> value); ACCUMULATE(loop -> result)
  called_by: sanitizeRequestID

Request.SetDisablePathNormalizing (client/request.go:619-619)
  SetDisablePathNormalizing configures the Request to disable or enable path normalizing.
  sig: Request.SetDisablePathNormalizing(disable bool)

ConvertRequest (middleware/adaptor/adaptor.go:89-89)
  ConvertRequest converts a fiber.Ctx to a http.Request.
  sig: ConvertRequest(c fiber.Ctx, forServer bool)
  behavior: GUARD(err -> pass_through)

HTTPMiddleware (middleware/adaptor/adaptor.go:162-162)
  HTTPMiddleware wraps net/http middleware to fiber middleware
  sig: HTTPMiddleware(mw func(http.Handler)
  calls: CopyContextToFiberContext, HTTPHandler

Middleware.initialize (middleware/session/middleware.go:111-111)
  initialize sets up middleware for the request.
  sig: Middleware.initialize(c fiber.Ctx, cfg *Config)
  behavior: GUARD(err -> raise_panic); UNWIND(defer)
  called_by: NewWithStore
  raises: panic

HTTPHandlerWithContext (middleware/adaptor/adaptor.go:65-65)
  HTTPHandlerWithContext is like HTTPHandler, but additionally stores Fiber’s user context in the request context
  sig: HTTPHandlerWithContext(h http.Handler)
  calls: LocalContextFromHTTPRequest

domainMatch (client/cookiejar.go:327-327)
  domainMatch reports whether host domain-matches the given cookie domain.
  sig: domainMatch(host, domain string)
  behavior: GUARD(host -> value)
  called_by: cookiesForRequest

Client.DisablePathNormalizing (client/client.go:437-437)
  DisablePathNormalizing reports whether path normalizing is disabled for the client.

paramsMatch (helpers.go:412-412)
  paramsMatch returns whether offerParams contains all parameters present in specParams.
  sig: paramsMatch(specParamStr headerParams, offerParams string)
  behavior: GUARD(len -> value); ACCUMULATE(loop -> result)
  calls: unescapeHeaderValue
  called_by: acceptsOfferType

App.printRoutesMessage (listen.go:516-517)
  printRoutesMessage print all routes with method, path, name and handlers in a format of table, like this: method | path 
  behavior: GUARD(IsChild -> none); PRECEDENCE(IsChild -> os); ACCUMULATE(loop -> newRoute_handlers)
  called_by: printMessages

DefaultCtx.IsMiddleware (ctx.go:380-381)
  IsMiddleware returns true if the current request handler was registered as middleware.
  behavior: GUARD(c -> value); PRECEDENCE(c)

DefaultCtx.Path (ctx.go:297-297)
  Path returns the path part of the request URL.
  sig: DefaultCtx.Path(override ...string)
  behavior: DELEGATE(c.app.toString -> result)
  calls: configDependentPaths

FromContext (middleware/session/middleware.go:179-179)
  FromContext returns the Middleware from the Fiber context.
  sig: FromContext(ctx any)
  behavior: GUARD(m -> pass_through)

IsEarly (middleware/earlydata/earlydata.go:16-16)
  IsEarly returns true if the request used early data and was accepted by the middleware.
  sig: IsEarly(c fiber.Ctx)
  behavior: DELEGATE(c.Locals -> result)

New (middleware/skip/skip.go:10-10)
  New returns a middleware that calls the provided predicate for each request.
  sig: New(handler fiber.Handler, exclude func(c fiber.Ctx)
  behavior: GUARD(exclude -> handler)

core (client/core.go:48-48)
  core stores middleware and plugin definitions and defines the request execution process.
  methods: afterHooks, execFunc, execute, getRetryConfig, preHooks, timeout

domainRouter.Use (domain.go:350-350)
  Use registers a middleware route that will match requests with the provided prefix (which is optional and defaults to "/
  sig: domainRouter.Use(args ...any)
  behavior: PRECEDENCE(len -> d); ACCUMULATE(loop -> handlers)
  calls: Name, mount, registerGroup, registerPath, wrapHandlers
  raises: panic

App.Group (app.go:969-969)
  Group is used for Routes with common prefix to define a new sub-router with optional middleware.
  sig: App.Group(prefix string, handlers ...any)
  behavior: PRECEDENCE(len -> err)
  called_by: Route
  raises: panic

App.Use (app.go:860-860)
  Use registers a middleware route that will match requests with the provided prefix (which is optional and defaults to "/
  sig: App.Use(args ...any)
  behavior: ACCUMULATE(loop -> handlers)
  raises: panic

Group.Group (group.go:187-187)
  Group is used for Routes with common prefix to define a new sub-router with optional middleware.
  sig: Group.Group(prefix string, handlers ...any)
  behavior: PRECEDENCE(len -> err)
  raises: panic

Group.Use (group.go:70-70)
  Use registers a middleware route that will match requests with the provided prefix (which is optional and defaults to "/
  sig: Group.Use(args ...any)
  behavior: PRECEDENCE(len -> not_grp.anyRouteDefined); ACCUMULATE(loop -> handlers)
  raises: panic

DefaultCtx.Matched (ctx.go:375-376)
  Matched returns true if the current request path was matched by the router.
  behavior: DELEGATE(c.getMatched -> result)
  calls: getMatched
  called_by: OverrideParam

CustomCtx (ctx_interface.go:13-14)
  CustomCtx extends Ctx with the additional methods required by Fiber's internals and middleware helpers.

domainCheckResult (domain.go:32-33)
  domainCheckResult caches a domain match result for a single request.

DefaultCtx.HasHeader (req.go:239-239)
  HasHeader reports whether the request includes a header with the given key.
  sig: DefaultCtx.HasHeader(key string)
  behavior: DELEGATE(len -> result)

StoreInContext (helpers.go:83-83)
  StoreInContext stores key/value in both Fiber locals and request context.
  sig: StoreInContext(c Ctx, key, value any)

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 52 with behavior annotations
drill: path.go (~1 lines, RoutePatternMatch)
drill: client/cookiejar.go (~1 lines, pathMatch)
drill: client/request.go (~1 lines, Request.DisablePathNormalizing)
drill: client/cookiejar.go (~1 lines, CookieJar.cookiesForRequest)

--- CLUE FILE END ---

QUESTION: If middleware rewrites the request path and wants Fiber to match routes again, how does the framework restart dispatch and decide whether the request becomes a normal match, a 404, or a 405?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry that supports it.
