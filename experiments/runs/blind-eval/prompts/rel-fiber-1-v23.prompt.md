# Blind Evaluation Prompt - MRLF v2.4
# Task: rel-fiber-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 fiber@HEAD 148mod 1472sym
? What is the relationship between the App struct, Router, and Route types in Fiber, and how do they connect?


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
Colors (color.go:8-9)
  Colors is a struct to define custom colors for Fiber app and middlewares.

App.deleteRoute (router.go:443-443)
  sig: App.deleteRoute(methods []string, matchFunc func(r *Route)
  behavior: ACCUMULATE(ToUpper loop -> result); UNWIND(defer)
  calls: pruneAutoHeadRouteLocked
  called_by: RemoveRoute, RemoveRouteByName, RemoveRouteFunc

App.addRoute (router.go:590-590)
  sig: App.addRoute(method string, route *Route)
  behavior: UNWIND(defer)
  calls: pruneAutoHeadRouteLocked
  called_by: register
  raises: panic

App.addPrefixToRoute (router.go:355-355)
  sig: App.addPrefixToRoute(prefix string, route *Route)

App.Connect (app.go:929-929)
  Connect registers a route for CONNECT methods that establishes a tunnel to the server identified by the target resource.
  sig: App.Connect(path string, handler any, handlers ...any)
  behavior: DELEGATE(app.Add -> result)
  calls: Add

domainRouter.Connect (domain.go:506-506)
  Connect registers a route for CONNECT methods.
  sig: domainRouter.Connect(path string, handler any, handlers ...any)
  behavior: DELEGATE(d.Add -> result)
  calls: Add

Route (router.go:45-46)
  Route is a struct that holds all metadata for each registered handler.
  methods: match

domainRouter.RouteChain (domain.go:575-575)
  RouteChain creates a Registering instance for the domain router.
  sig: domainRouter.RouteChain(path string)
  calls: registerPath

FiberApp (middleware/adaptor/adaptor.go:204-204)
  FiberApp wraps fiber app to net/http handler func
  sig: FiberApp(app *fiber.App)
  behavior: DELEGATE(handlerFunc -> result)
  calls: handlerFunc

domainRouter.mount (domain.go:403-403)
  mount attaches a sub-app instance to the domain router at the specified prefix.
  sig: domainRouter.mount(prefix string, subApp *App)
  behavior: PRECEDENCE(d -> mountPath -> err); ACCUMULATE(copyRoute loop -> result); UNWIND(defer)
  calls: Name, wrapHandlers
  called_by: Use
  raises: panic

DefaultCtx.Route (ctx.go:355-356)
  Route returns the matched Route struct.
  behavior: GUARD(c.route == nil -> return &Route{)
  called_by: FullPath

DefaultReq.Route (req.go:1002-1002)
  Route returns the matched Route struct.
  behavior: DELEGATE(r.c.Route -> result)
  called_by: Params

App (app.go:69-69)
  App denotes the Fiber application.
  methods: Add, All, Config, Connect, Delete, Domain

RoutePatternMatch (path.go:155-155)
  RoutePatternMatch reports whether path matches the provided Fiber route pattern.
  sig: RoutePatternMatch(path, pattern string, cfg ...Config)
  behavior: PRECEDENCE(len -> path -> pattern); UNWIND(defer)
  calls: RemoveEscapeCharBytes, parseRoute, getMatch, reset

Registering.Connect (register.go:87-87)
  Connect registers a route for CONNECT methods that establishes a tunnel to the server identified by the target resource.
  sig: Registering.Connect(handler any, handlers ...any)
  behavior: DELEGATE(r.Add -> result)
  calls: Add

Group.Connect (group.go:143-143)
  Connect registers a route for CONNECT methods that establishes a tunnel to the server identified by the target resource.
  sig: Group.Connect(path string, handler any, handlers ...any)
  behavior: DELEGATE(grp.Add -> result)
  calls: Add

Redirect.Route (redirect.go:339-339)
  Route redirects to the Route registered in the app with appropriate parameters.
  sig: Redirect.Route(name string, config ...RedirectConfig)
  behavior: PRECEDENCE(len -> err)
  calls: To

Router (router.go:18-19)
  Router defines all router handle interface, including app and group router.

WithStruct (client/request.go:24-24)
  WithStruct is implemented by types that allow data to be stored from a struct via reflection.

App.MountPath (mount.go:103-104)
  MountPath returns the route pattern where the current app instance was mounted as a sub-application.

App.mount (mount.go:42-42)
  Mount attaches another app instance as a sub-router along a routing path.
  sig: App.mount(prefix string, subApp *App)
  behavior: PRECEDENCE(prefix -> err); ACCUMULATE(getGroupPath loop -> result)
  raises: panic

DefaultCtx.App (ctx.go:102-102)
  App returns the *App reference to the instance of the Fiber application

DefaultReq.App (req.go:83-83)
  App returns the *App reference to the instance of the Fiber application

DefaultRes.App (res.go:134-134)
  App returns the *App reference to the instance of the Fiber application

Bind.URI (bind.go:352-352)
  URI binds the route parameters into the struct, map[string]string and map[string][]string.
  sig: Bind.URI(out any)
  behavior: GUARD(err := b.returnBindErr(bind.Bind(b.ctx.Route(... -> return err); UNWIND(defer)
  calls: returnBindErr, validateStruct, Bind

Hooks (hooks.go:35-35)
  Hooks is a struct to use it with App.
  methods: OnFork, OnGroup, OnGroupName, OnListen, OnMount, OnName

domainRegistering (domain.go:623-624)
  domainRegistering provides route registration helpers for a specific path on a domain router, implementing the [Register
  methods: Add, All, Connect, Delete, Get, Head

Registering.All (register.go:50-50)
  All registers a middleware route that will match requests with the provided path which is stored in register struct.
  sig: Registering.All(handler any, handlers ...any)

State (state.go:21-21)
  State is a key-value store for Fiber's app in order to be used as a global storage for the app's dependencies.
  methods: Delete, Get, GetBool, GetComplex128, GetComplex64, GetFloat32

ListenConfig (listen.go:44-45)
  ListenConfig is a struct to customize startup of Fiber.

Register (register.go:8-9)
  Register defines all router handle interface generate by RouteChain().

Group.mount (mount.go:73-73)
  Mount attaches another app instance as a sub-router along a routing path.
  sig: Group.mount(prefix string, subApp *App)
  behavior: PRECEDENCE(groupPath -> err); ACCUMULATE(getGroupPath loop -> result)
  raises: panic

App.next (router.go:115-115)
  sig: App.next(c *DefaultCtx)
  behavior: PRECEDENCE(not_ok -> c -> exists); ACCUMULATE(match loop -> result)
  calls: match
  called_by: requestHandler

App.nextCustom (router.go:216-216)
  sig: App.nextCustom(c CustomCtx)
  behavior: PRECEDENCE(not_ok -> c -> exists); ACCUMULATE(match loop -> result)
  calls: match
  called_by: requestHandler

App.pruneAutoHeadRouteLocked (router.go:491-491)
  pruneAutoHeadRouteLocked removes an automatically generated HEAD route so a later explicit registration can take its pla
  sig: App.pruneAutoHeadRouteLocked(path string)
  behavior: GUARD(headIndex == -1 -> return); ACCUMULATE(append loop -> result)
  calls: normalizePath
  called_by: addRoute, deleteRoute

App.RemoveRoute (router.go:417-417)
  RemoveRoute is used to remove a route from the stack by path.
  sig: App.RemoveRoute(path string, methods ...string)
  calls: deleteRoute, normalizePath

App.RemoveRouteByName (router.go:430-430)
  RemoveRouteByName is used to remove a route from the stack by name.
  sig: App.RemoveRouteByName(name string, methods ...string)
  calls: deleteRoute

App.RemoveRouteFunc (router.go:439-439)
  RemoveRouteFunc is used to remove a route from the stack by a custom match function.
  sig: App.RemoveRouteFunc(matchFunc func(r *Route)
  calls: deleteRoute

App.Route (app.go:1024-1024)
  Route is used to define routes with a common prefix inside the supplied function.
  sig: App.Route(prefix string, fn func(router Router)
  behavior: GUARD(fn == nil -> panic("route handle...); PRECEDENCE(fn -> len)
  calls: Group, Name
  raises: panic

domainRouter.Route (domain.go:584-584)
  Route defines routes with a common prefix inside the supplied function, scoped to the domain pattern.
  sig: domainRouter.Route(prefix string, fn func(router Router)
  behavior: GUARD(fn == nil -> panic("route handle...); PRECEDENCE(fn -> len)
  calls: Group, Name
  raises: panic

-- GAPS
type: RELATIONAL (answerable from L2-L3 structure)
coverage: 80 symbols in L3, 50 with behavior annotations
uncovered: DefaultCtx.RestartRouting, routeParser.analyseParameterPart, App.setCtxFunc, routeParser.parseRoute

--- CLUE FILE END ---

QUESTION: What is the relationship between the App struct, Router, and Route types in Fiber, and how do they connect?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
