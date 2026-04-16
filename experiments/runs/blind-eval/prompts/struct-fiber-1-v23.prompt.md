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
log/log.go                                      121L  CommonLogger, FormatLogger, toString, Logger, WithLogger
router.go                                       767L  RebuildTree, RemoveRoute, RemoveRouteByName, RemoveRouteFunc, addPrefixToRoute
middleware/cache/manager_msgp.go                945L  DecodeMsg, EncodeMsg, MarshalMsg, Msgsize, UnmarshalMsg
redirect_msgp.go                                301L  DecodeMsg, EncodeMsg, MarshalMsg, Msgsize, UnmarshalMsg
path.go                                         844L  CheckConstraint, Constraint, CustomConstraint, GetTrimmedParam, RemoveEscapeChar
client/client.go                                863L  C, AddHeader, AddHeaders, AddParam, AddParams
helpers.go                                     1126L  isEtagStale, method, methodInt, quoteRawString, quoteString
bind.go                                         477L  AcquireBind, All, Body, CBOR, Cookie
middleware/csrf/storage_manager_msgp.go          92L  DecodeMsg, EncodeMsg, MarshalMsg, Msgsize, UnmarshalMsg
middleware/idempotency/response_msgp.go         282L  DecodeMsg, EncodeMsg, MarshalMsg, Msgsize, UnmarshalMsg
middleware/limiter/manager_msgp.go              160L  DecodeMsg, EncodeMsg, MarshalMsg, Msgsize, UnmarshalMsg
client/request.go                              1122L  AcquireFile, AcquireRequest, Add, All, Del
res.go                                         1153L  Cookie, App, Append, Attachment, AutoFormat
mount.go                                        227L  MountPath, appendSubAppLists, generateAppListKeys, hasMountedApps, mount
client/transport.go                             377L  composeRedirectURL, doRedirectsWithClient, extractTLSConfig, forEachHostClient, Client
  ...and 133 more modules

-- SYM
MemoryLock.Unlock                   M middleware/idempotency/locker.go:41     Unlock releases the lock associated with the pr...
MemoryLock.Lock                     M middleware/idempotency/locker.go:25     Lock acquires the lock for the provided key, cr...
defaultLogger.privateLogf           M log/default.go:47     privateLogf logs a formatted message at a given...
Level.toString                      M log/log.go:116    function Level.toString
defaultLogger.Errorf                M log/default.go:174    Errorf formats according to a format specifier ...
App.register                        M router.go:513    function App.register
App.methodInt                       M helpers.go:923    HTTP methods and their unique INTs
App.addRoute                        M router.go:590    function App.addRoute
Cookie.Add                          M client/request.go:781    Add adds a cookie key-value pair.
App.pruneAutoHeadRouteLocked        M router.go:491    pruneAutoHeadRouteLocked removes an automatical...
App.Name                            M app.go:783    Name Assign name to specific route.
defaultLogger.privateLog            M log/default.go:24     privateLog logs a message at a given level log ...
DefaultCtx.Next                     M ctx.go:243    Next executes the next method in the stack that...
domainRouter.Name                   M domain.go:602    Name assigns a name to the most recently regist...
App.Add                             M app.go:953    Add allows you to specify multiple HTTP methods...
FormData.Add                        M client/request.go:888    Add adds a single form field.
PathParam.Add                       M client/request.go:829    Add adds a path parameter key-value pair.
domainRegistering.Add               M domain.go:675    function domainRegistering.Add
domainRouter.Add                    M domain.go:530    Add allows you to specify multiple HTTP methods...
Group.Add                           M group.go:167    Add allows you to specify multiple HTTP methods...
Registering.Add                     M register.go:111    Add allows you to specify multiple HTTP methods...
DefaultReq.Locals                   M req.go:672    Locals makes it possible to pass any values und...
DefaultRes.Append                   M res.go:140    Append the specified value to the HTTP response...
Response.String                     M client/response.go:109    String returns the response body as a trimmed s...
DefaultCtx.String                   M ctx.go:571    String returns unique string representation of ...
C                                   M client/client.go:810    C returns the default client.
walkBalancingClientWithBreak        M client/transport.go:268    walkBalancingClientWithBreak traverses balancin...
Client.LBClient                     M client/client.go:128    LBClient returns the underlying fasthttp.LBClie...
Group.Name                          M group.go:27     Name Assign name to specific route or group its...
defaultLogger.privateLogw           M log/default.go:74     privateLogw logs a message at a given level log...
DefaultRes.WriteString              M res.go:1110   WriteString appends s to response body.
ReleaseFile                         M client/request.go:1053   ReleaseFile returns the File object to the pool.
Response.Body                       M client/response.go:88     Body returns the HTTP response body as a byte s...
Request.Reset                       M client/request.go:680    Reset clears the Request object, returning it t...
DefaultReq.Host                     M req.go:465    Host contains the host derived from the X-Forwa...
App.normalizePath                   M router.go:398    function App.normalizePath
DefaultReq.Body                     M req.go:149    Body contains the raw body submitted in a POST ...
Cookie.All                          M client/request.go:816    All returns an iterator over cookie key-value p...
domainRouter.wrapHandlers           M domain.go:278    wrapHandlers wraps every handler in the slice w...
FormData.Set                        M client/request.go:893    Set sets a single form field, overriding previo...
Session.Get                         M middleware/session/session.go:74     Release releases the session back to the pool.
buildPaginationURL                  M middleware/paginate/page_info.go:121    buildPaginationURL parses baseURL and sets/repl...
domainRouter.registerGroup          M domain.go:336    registerGroup returns the group to associate wi...
DefaultCtx.Path                     M ctx.go:297    Path returns the path part of the request URL.
Response.Reset                      M client/response.go:193    Reset clears the Response object, making it rea...
Request.resetBody                   M client/request.go:438    resetBody clears the existing body.
Bind.Body                           M bind.go:385    Body binds the request body into the struct, ma...
newClient                           M client/client.go:783    function newClient
Session.Reset                       M middleware/session/session.go:247    Reset generates a new session id, deletes the o...
SetValWithStruct                    M client/request.go:1066   SetValWithStruct sets values using a struct.
standardClientTransport.Do          M client/transport.go:50     function standardClientTransport.Do
defaultLogger.Warnf                 M log/default.go:169    Warnf formats according to a format specifier a...
Request.Send                        M client/request.go:673    Send executes the Request.
isASCIIAlphanumeric                 M domain.go:217    isASCIIAlphanumeric returns true if the rune is...
Request.SetMethod                   M client/request.go:82     SetMethod sets the HTTP method for the Request.
Request.SetURL                      M client/request.go:93     SetURL sets the URL for the Request.
Cookie.Del                          M client/request.go:786    Del deletes a cookie by key.
DefaultCtx.RequestCtx               M ctx.go:118    RequestCtx returns *fasthttp.RequestCtx that ca...
DefaultReq.RequestCtx               M req.go:201    RequestCtx returns *fasthttp.RequestCtx that ca...
DefaultRes.RequestCtx               M res.go:248    RequestCtx returns *fasthttp.RequestCtx that ca...
Request.Get                         M client/request.go:633    Get sends a GET request to the given URL.
DefaultReq.Accepts                  M req.go:51     Accepts checks if the specified extensions or c...
ExponentialBackoff.next             M addon/retry/exponential_backoff.go:62     next calculates the next sleeping time interval.
App.next                            M router.go:115    function App.next
DefaultCtx.App                      M ctx.go:102    App returns the *App reference to the instance ...
DefaultReq.App                      M req.go:83     App returns the *App reference to the instance ...
DefaultRes.App                      M res.go:134    App returns the *App reference to the instance ...
CookieJar.SetByHost                 M client/cookiejar.go:154    SetByHost stores the given cookies for the spec...
walkBalancingClient                 M client/transport.go:239    walkBalancingClient traverses balancing clients...
DefaultCtx.configDependentPaths     M ctx.go:632    configDependentPaths set paths for route recogn...
App.nextCustom                      M router.go:216    function App.nextCustom
domainRouter.registerPath           M domain.go:327    registerPath returns the full path for registra...
forEachHostClient                   M client/transport.go:231    forEachHostClient applies fn to every host clie...
DefaultRes.Write                    M res.go:1098   Write appends p into response body.
  ...and 1398 more symbols

-- FOCUS
HTTPMiddleware (middleware/adaptor/adaptor.go:162-162)
  HTTPMiddleware wraps net/http middleware to fiber middleware
  sig: HTTPMiddleware(mw func(http.Handler)
  calls: Context, Next, Request, RequestCtx, CopyContextToFiberContext, HTTPHandler

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
  calls: Type
  called_by: HTTPMiddleware

FiberApp (middleware/adaptor/adaptor.go:204-204)
  FiberApp wraps fiber app to net/http handler func
  sig: FiberApp(app *fiber.App)
  behavior: DELEGATE(handlerFunc -> result)
  calls: handlerFunc

Middleware (middleware/session/middleware.go:13-13)
  Middleware holds session data and configuration.
  methods: Delete, Destroy, Fresh, Get, ID, Keys

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
  calls: Lock, Unlock
  called_by: NewWithStore
  raises: panic

releaseMiddleware (middleware/session/middleware.go:157-157)
  releaseMiddleware resets and returns middleware to the pool.
  sig: releaseMiddleware(m *Middleware)
  calls: Lock, Unlock
  called_by: NewWithStore

Request.AddFiles (client/request.go:585-585)
  AddFiles adds multiple files at once.
  sig: Request.AddFiles(files ...*File)
  calls: resetBody
  called_by: setConfigToRequest

acquireMiddleware (middleware/session/middleware.go:141-141)
  acquireMiddleware retrieves a middleware instance from the pool.
  behavior: GUARD(!ok -> panic(ErrTypeAssert...)
  calls: Get
  called_by: NewWithStore
  raises: panic

DefaultCtx.IsMiddleware (ctx.go:380-381)
  IsMiddleware returns true if the current request handler was registered as middleware.
  behavior: GUARD(c.route == nil -> return false); PRECEDENCE(c)

Request.Files (client/request.go:556-556)
  Files returns all files added to the Request.

adaptFiberHandler (adapter.go:32-32)
  sig: adaptFiberHandler(handler any)
  behavior: DISPATCH(h)
  called_by: toFiberHandler

domainRouter.Use (domain.go:350-350)
  Use registers a middleware route that will match requests with the provided prefix (which is optional and defaults to "/
  sig: domainRouter.Use(args ...any)
  behavior: PRECEDENCE(len -> d); ACCUMULATE(toFiberHandler loop -> handlers, raises fmt.Sprintf("use:...)
  calls: Name, mount, registerGroup, registerPath, wrapHandlers, register
  raises: panic

FromContext (middleware/session/middleware.go:179-179)
  FromContext returns the Middleware from the Fiber context.
  sig: FromContext(ctx any)
  behavior: GUARD(m, ok := fiber.ValueFromContext[*Middleware](... -> return m)

CustomCtx (ctx_interface.go:13-14)
  CustomCtx extends Ctx with the additional methods required by Fiber's internals and middleware helpers.

Middleware.Get (middleware/session/middleware.go:214-214)
  Get retrieves a value from the session by key.
  sig: Middleware.Get(key any)
  behavior: DELEGATE(m.Session.Get -> result); UNWIND(defer)
  called_by: fieldName, Get, SetValWithStruct, RequestID, FromAuthHeader, FromHeader, GetWithContext, New

Middleware.Set (middleware/session/middleware.go:196-196)
  Set sets a key-value pair in the session.
  sig: Middleware.Set(key, value any)
  behavior: UNWIND(defer)
  calls: Lock, Unlock
  called_by: DefaultErrorHandler, SetWithMap, SetHeaders, SetParams, SetWithContext, configDefault, New, appendVaryAcceptEncoding

Middleware.saveSession (middleware/session/middleware.go:128-128)
  saveSession handles session saving and error management after the response.
  called_by: NewWithStore, Save

Middleware.Reset (middleware/session/middleware.go:300-300)
  Reset resets the session.
  behavior: DELEGATE(m.Session.Reset -> result); UNWIND(defer)
  calls: Lock, Unlock
  called_by: ReleaseFile, ReleaseRequest, String, AcquireCtx, ResetWithContext, privateLog, privateLogf, privateLogw

Middleware.Delete (middleware/session/middleware.go:229-229)
  Delete removes a key-value pair from the session.
  sig: Middleware.Delete(key any)
  behavior: UNWIND(defer)
  calls: Lock, Unlock
  called_by: Delete, DeleteWithContext, deleteService

Middleware.Destroy (middleware/session/middleware.go:259-259)
  Destroy destroys the session.
  behavior: UNWIND(defer)
  calls: Lock, Unlock

Middleware.Regenerate (middleware/session/middleware.go:318-318)
  Regenerate generates a new session ID while preserving session data.
  behavior: DELEGATE(m.Session.Regenerate -> result); UNWIND(defer)
  calls: Lock, Unlock

New (middleware/limiter/limiter.go:23-23)
  New creates a new middleware handler
  sig: New(config ...Config)
  behavior: DELEGATE(cfg.LimiterMiddleware.New -> result)

New (middleware/idempotency/idempotency.go:45-45)
  New creates idempotency middleware that caches responses keyed by the configured idempotency header.
  sig: New(config ...Config)
  behavior: ACCUMULATE(ToLower loop -> result)
  calls: Get, Bind, Send, Status, App, Next, RequestCtx, Response

New (middleware/cache/cache.go:109-109)
  New creates a new middleware handler
  sig: New(config ...Config)
  calls: Set, Context, Method, Next, Request, Response, Errorf, allowsSharedCacheDirectives
  called_by: makeBuildVaryKeyFunc

New (middleware/cors/cors.go:28-28)
  New creates a new middleware handler
  sig: New(config ...Config)
  behavior: PRECEDENCE(len -> cfg); ACCUMULATE(TrimSpace loop -> allowSubOrigins, raises "[CORS] Invalid o...)
  calls: Get, Set, Method, Next, Warn, isOriginSerializedOrNull, setPreflightHeaders, setSimpleHeaders
  raises: panic

New (middleware/requestid/requestid.go:18-18)
  New creates a new middleware handler
  sig: New(config ...Config)
  calls: Get, Set, Next, sanitizeRequestID

New (middleware/static/static.go:121-121)
  New creates a new middleware handler.
  sig: New(root string, cfg ...Config)
  calls: Route, Method, App, Next, Path, RequestCtx, isFile, sanitizePath

New (middleware/csrf/csrf.go:50-50)
  New creates a new middleware handler
  sig: New(config ...Config)
  behavior: PRECEDENCE(cfg -> token); ACCUMULATE(TrimSpace loop -> trustedSubOrigins, raises "[CSRF] Invalid o...); DISPATCH(c)
  calls: ErrorHandler, Cookies, Method, Next, createOrExtendTokenInStorage, deleteTokenFromStorage, expireCSRFCookie, getRawFromStorage
  raises: panic

New (middleware/basicauth/basicauth.go:27-27)
  New creates a new middleware handler
  sig: New(config ...Config)
  calls: Get, App, Next, containsCTL, containsInvalidHeaderChars, SendStatus

New (middleware/favicon/favicon.go:21-21)
  New creates a new middleware handler
  sig: New(config ...Config)
  behavior: GUARD(cfg.Data != nil -> panic(err))
  calls: Set, Method, Close, Status, Next, Path, readLimited, SendStatus
  raises: panic

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 80 symbols in L3, 29 with behavior annotations
uncovered: Middleware.Fresh, Middleware.ID, Middleware.Keys, Middleware.Store

--- CLUE FILE END ---

QUESTION: What are the main source files and packages in the Fiber framework, and how is the middleware organized?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
