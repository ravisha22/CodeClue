# Blind Evaluation Prompt - MRLF v2.1 with File 2 Drill-Down
# Task: blind-fiber-1

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

--- CLUE FILE (File 1) ---
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

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## RoutePatternMatch  (path.go L155-155)
```
func RoutePatternMatch(path, pattern string, cfg ...Config) bool {
```

## pathMatch  (client/cookiejar.go L307-307)
```
func pathMatch(reqPath, cookiePath []byte) bool {
```

## Request.DisablePathNormalizing  (client/request.go L614-614)
```
func (r *Request) DisablePathNormalizing() bool {
```

## CookieJar.cookiesForRequest  (client/cookiejar.go L103-103)
```
func (cj *CookieJar) cookiesForRequest(host string, path []byte, secure bool) []*fasthttp.Cookie {
```

## RemoveEscapeCharBytes  (path.go L659-659)
```
func RemoveEscapeCharBytes(word []byte) []byte {
```

## parseRoute  (path.go L245-245)
```
func parseRoute(pattern string, customConstraints ...CustomConstraint) routeParser {
```

## domainMatch  (client/cookiejar.go L327-327)
```
func domainMatch(host, domain string) bool {
```

## Constraint.CheckConstraint  (path.go L707-707)
```
func (c *Constraint) CheckConstraint(param string) bool {
```

## Constraint  (path.go L80-80)
```
	RegexCompiler     *regexp.Regexp
```

## CustomConstraint  (path.go L88-89)
```
type CustomConstraint interface {
	// Name returns the name of the constraint.
```

## GetTrimmedParam  (path.go L623-623)
```
func GetTrimmedParam(param string) string {
```

## RemoveEscapeChar  (path.go L639-639)
```
func RemoveEscapeChar(word string) string {
```

## addParameterMetaInfo  (path.go L260-260)
```
func addParameterMetaInfo(segs []*routeSegment) []*routeSegment {
```

## findGreedyParamLen  (path.go L607-607)
```
func findGreedyParamLen(s string, searchCount int, segment *routeSegment) int {
```

## findNextNonEscapedCharPosition  (path.go L462-462)
```
func findNextNonEscapedCharPosition(search string, char byte) int {
```

## findNextParamPosition  (path.go L305-305)
```
func findNextParamPosition(pattern string) int {
```

## findParamLen  (path.go L563-563)
```
func findParamLen(s string, segment *routeSegment) int {
```

## findParamLenForLastSegment  (path.go L596-596)
```
func findParamLenForLastSegment(s string, seg *routeSegment) int {
```

## getParamConstraintType  (path.go L670-670)
```
func getParamConstraintType(constraintPart string) TypeConstraint {
```

## hasPartialMatchBoundary  (path.go L486-486)
```
func hasPartialMatchBoundary(path string, matchedLength int) bool {
```

## routeParser.analyseParameterPart  (path.go L342-342)
```
func (parser *routeParser) analyseParameterPart(pattern string, customConstraints ...CustomConstraint) (int, *routeSegment) {
```

## routeParser.getMatch  (path.go L507-507)
```
func (parser *routeParser) getMatch(detectionPath, path string, params *[maxParams]string, partialCheck bool) bool { //nolint:revive // Accepting a bool param is fine here
```

## routeParser.parseRoute  (path.go L221-221)
```
func (parser *routeParser) parseRoute(pattern string, customConstraints ...CustomConstraint) {
```

## routeParser.reset  (path.go L213-213)
```
	parser.segs = parser.segs[:0]
```

## routeParser  (path.go L27-27)
```
	segs          []*routeSegment // the parsed segments of the route
```

## routeSegment  (path.go L40-41)
```
type routeSegment struct {
	// const information
```

## splitNonEscaped  (path.go L473-473)
```
func splitNonEscaped(s string, sep byte) []string {
```

## AcquireCookieJar  (client/cookiejar.go L24-24)
```
func AcquireCookieJar() *CookieJar {
```

## CookieJar.Get  (client/cookiejar.go L50-50)
```
func (cj *CookieJar) Get(uri *fasthttp.URI) []*fasthttp.Cookie {
```

## CookieJar.Release  (client/cookiejar.go L281-281)
```
func (cj *CookieJar) Release() {
```

## CookieJar.Set  (client/cookiejar.go L143-143)
```
func (cj *CookieJar) Set(uri *fasthttp.URI, cookies ...*fasthttp.Cookie) {
```

## CookieJar.SetByHost  (client/cookiejar.go L154-154)
```
func (cj *CookieJar) SetByHost(host []byte, cookies ...*fasthttp.Cookie) {
```

## CookieJar.SetKeyValue  (client/cookiejar.go L195-195)
```
func (cj *CookieJar) SetKeyValue(host, key, value string) {
```

## CookieJar.SetKeyValueBytes  (client/cookiejar.go L206-206)
```
func (cj *CookieJar) SetKeyValueBytes(host string, key, value []byte) {
```

## CookieJar.dumpCookiesToReq  (client/cookiejar.go L215-215)
```
func (cj *CookieJar) dumpCookiesToReq(req *fasthttp.Request) {
```

## CookieJar.getByHostAndPath  (client/cookiejar.go L60-60)
```
func (cj *CookieJar) getByHostAndPath(host, path []byte, secure bool) []*fasthttp.Cookie {
```

## CookieJar.getCookiesByHost  (client/cookiejar.go L79-79)
```
func (cj *CookieJar) getCookiesByHost(host string) []*fasthttp.Cookie {
```

## CookieJar.parseCookiesFromResp  (client/cookiejar.go L226-226)
```
func (cj *CookieJar) parseCookiesFromResp(host, _ []byte, resp *fasthttp.Response) {
```

## CookieJar  (client/cookiejar.go L40-40)
```
type CookieJar struct {
```

## ReleaseCookieJar  (client/cookiejar.go L34-34)
```
func ReleaseCookieJar(c *CookieJar) {
```

## searchCookieByKeyAndPath  (client/cookiejar.go L294-294)
```
func searchCookieByKeyAndPath(key, path []byte, cookies []*fasthttp.Cookie) *fasthttp.Cookie {
```

## AcquireFile  (client/request.go L1032-1032)
```
func AcquireFile(setter ...SetFileFunc) *File {
```

## AcquireRequest  (client/request.go L983-983)
```
func AcquireRequest() *Request {
```

## Cookie.Add  (client/request.go L781-781)
```
func (c Cookie) Add(key, val string) {
```

## Cookie.All  (client/request.go L816-816)
```
func (c Cookie) All() iter.Seq2[string, string] {
```

## Cookie.Del  (client/request.go L786-786)
```
func (c Cookie) Del(key string) {
```

## Cookie.DelCookies  (client/request.go L807-807)
```
func (c Cookie) DelCookies(key ...string) {
```

## Cookie.Reset  (client/request.go L821-821)
```
func (c Cookie) Reset() {
```

## Cookie.SetCookie  (client/request.go L791-791)
```
func (c Cookie) SetCookie(key, val string) {
```

## Cookie.SetCookies  (client/request.go L796-796)
```
func (c Cookie) SetCookies(m map[string]string) {
```

## Cookie.SetCookiesWithStruct  (client/request.go L802-802)
```
func (c Cookie) SetCookiesWithStruct(v any) {
```

## File.Reset  (client/request.go L960-960)
```
func (f *File) Reset() {
```

## File.SetFieldName  (client/request.go L945-945)
```
func (f *File) SetFieldName(n string) {
```

## File.SetName  (client/request.go L940-940)
```
func (f *File) SetName(n string) {
```

## File.SetPath  (client/request.go L950-950)
```
func (f *File) SetPath(p string) {
```

## File.SetReader  (client/request.go L955-955)
```
func (f *File) SetReader(r io.ReadCloser) {
```

## File  (client/request.go L932-932)
```
type File struct {
```

## FormData.Add  (client/request.go L888-888)
```
func (f *FormData) Add(key, val string) {
```

## FormData.AddWithMap  (client/request.go L898-898)
```
func (f *FormData) AddWithMap(m map[string][]string) {
```

## FormData.DelData  (client/request.go L920-920)
```
func (f *FormData) DelData(key ...string) {
```

## FormData.Keys  (client/request.go L879-879)
```
func (f *FormData) Keys() []string {
```

## FormData.Reset  (client/request.go L927-927)
```
func (f *FormData) Reset() {
```

## FormData.Set  (client/request.go L893-893)
```
func (f *FormData) Set(key, val string) {
```

## FormData.SetWithMap  (client/request.go L907-907)
```
func (f *FormData) SetWithMap(m map[string]string) {
```

## FormData.SetWithStruct  (client/request.go L915-915)
```
func (f *FormData) SetWithStruct(v any) {
```

## FormData  (client/request.go L874-874)
```
type FormData struct {
```

## Header.AddHeaders  (client/request.go L725-725)
```
func (h *Header) AddHeaders(r map[string][]string) {
```

## Header.PeekMultiple  (client/request.go L713-713)
```
func (h *Header) PeekMultiple(key string) []string {
```

## Header.SetHeaders  (client/request.go L734-734)
```
func (h *Header) SetHeaders(r map[string]string) {
```

## Header  (client/request.go L708-708)
```
type Header struct {
```

## PathParam.Add  (client/request.go L829-829)
```
func (p PathParam) Add(key, val string) {
```

## PathParam.All  (client/request.go L864-864)
```
func (p PathParam) All() iter.Seq2[string, string] {
```

## PathParam.Del  (client/request.go L834-834)
```
func (p PathParam) Del(key string) {
```

## PathParam.DelParams  (client/request.go L855-855)
```
func (p PathParam) DelParams(key ...string) {
```

## PathParam.Reset  (client/request.go L869-869)
```
func (p PathParam) Reset() {
```

## PathParam.SetParam  (client/request.go L839-839)
```
func (p PathParam) SetParam(key, val string) {
```

## PathParam.SetParams  (client/request.go L844-844)
```
func (p PathParam) SetParams(m map[string]string) {
```

## PathParam.SetParamsWithStruct  (client/request.go L850-850)
```
func (p PathParam) SetParamsWithStruct(v any) {
```

## QueryParam.AddParams  (client/request.go L756-756)
```
func (p *QueryParam) AddParams(r map[string][]string) {
```

## QueryParam.Keys  (client/request.go L747-747)
```
func (p *QueryParam) Keys() []string {
```

## QueryParam.SetParams  (client/request.go L765-765)
```
func (p *QueryParam) SetParams(r map[string]string) {
```

## QueryParam.SetParamsWithStruct  (client/request.go L773-773)
```
func (p *QueryParam) SetParamsWithStruct(v any) {
```

## QueryParam  (client/request.go L742-742)
```
type QueryParam struct {
```

## ReleaseFile  (client/request.go L1053-1053)
```
func ReleaseFile(f *File) {
```

## ReleaseRequest  (client/request.go L993-993)
```
func ReleaseRequest(req *Request) {
```

## Request.AddFile  (client/request.go L571-571)
```
func (r *Request) AddFile(path string) *Request {
```

## Request.AddFileWithReader  (client/request.go L578-578)
```
func (r *Request) AddFileWithReader(name string, reader io.ReadCloser) *Request {
```

## Request.AddFiles  (client/request.go L585-585)
```
func (r *Request) AddFiles(files ...*File) *Request {
```

## Request.AddFormData  (client/request.go L493-493)
```
func (r *Request) AddFormData(key, val string) *Request {
```

## Request.AddFormDataWithMap  (client/request.go L507-507)
```
func (r *Request) AddFormDataWithMap(m map[string][]string) *Request {
```

## Request.AddHeader  (client/request.go L185-185)
```
func (r *Request) AddHeader(key, val string) *Request {
```

## Request.AddHeaders  (client/request.go L198-198)
```
func (r *Request) AddHeaders(h map[string][]string) *Request {
```

## Request.AddParam  (client/request.go L254-254)
```
func (r *Request) AddParam(key, val string) *Request {
```

## Request.AddParams  (client/request.go L266-266)
```
func (r *Request) AddParams(m map[string][]string) *Request {
```
--- END SOURCE SNIPPETS ---

QUESTION: If middleware rewrites the request path and wants Fiber to match routes again, how does the framework restart dispatch and decide whether the request becomes a normal match, a 404, or a 405?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
