# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: blind-fiber-1

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.

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
  called_by: parserRequestURL

CookieJar.cookiesForRequest (client/cookiejar.go:103-103)
  cookiesForRequest returns cookies that match the given host, path and security settings.
  sig: CookieJar.cookiesForRequest(host string, path []byte, secure bool)
  behavior: ACCUMULATE(domainMatch loop -> kept); UNWIND(defer)
  calls: domainMatch, pathMatch, Path, Secure, Lock, Unlock
  called_by: getByHostAndPath

DefaultCtx.RestartRouting (ctx.go:265-266)
  RestartRouting instead of going to the next handler.
  behavior: GUARD(c.handlerCtx != nil -> return err)
  calls: next, nextCustom

CopyContextToFiberContext (middleware/adaptor/adaptor.go:101-101)
  CopyContextToFiberContext copies the values of context.Context to a fasthttp.RequestCtx.
  sig: CopyContextToFiberContext(src any, requestContext *fasthttp.RequestCtx)
  behavior: GUARD(requestContext == nil -> return); PRECEDENCE(requestContext -> not_v.IsValid -> t); ACCUMULATE(IsNil loop -> result)
  calls: Type
  called_by: HTTPMiddleware

ConvertRequest (middleware/adaptor/adaptor.go:89-89)
  ConvertRequest converts a fiber.Ctx to a http.Request.
  sig: ConvertRequest(c fiber.Ctx, forServer bool)
  behavior: GUARD(err := fasthttpadaptor.ConvertRequest(c.Reque... -> return nil, err)
  calls: RequestCtx

Request.SetDisablePathNormalizing (client/request.go:619-619)
  SetDisablePathNormalizing configures the Request to disable or enable path normalizing.
  sig: Request.SetDisablePathNormalizing(disable bool)
  called_by: setConfigToRequest

isValidRequestID (middleware/requestid/requestid.go:61-61)
  isValidRequestID reports whether the request ID contains only visible ASCII characters (0x20–0x7E) and is non-empty.
  sig: isValidRequestID(rid string)
  behavior: GUARD(rid == "" -> return false); ACCUMULATE(loop -> result)
  called_by: sanitizeRequestID

DefaultCtx.Path (ctx.go:297-297)
  Path returns the path part of the request URL.
  sig: DefaultCtx.Path(override ...string)
  behavior: DELEGATE(c.app.toString -> result)
  calls: configDependentPaths, toString
  called_by: ErrorHandler, Get, cookiesForRequest, dumpCookiesToReq, parseCookiesFromResp, searchCookieByKeyAndPath, New, defaultLoggerInstance

Client.DisablePathNormalizing (client/client.go:437-437)
  DisablePathNormalizing reports whether path normalizing is disabled for the client.
  called_by: parserRequestURL

Middleware.initialize (middleware/session/middleware.go:111-111)
  initialize sets up middleware for the request.
  sig: Middleware.initialize(c fiber.Ctx, cfg *Config)
  behavior: GUARD(err != nil -> panic(err)); UNWIND(defer)
  calls: Lock, Unlock
  called_by: NewWithStore
  raises: panic

paramsMatch (helpers.go:412-412)
  paramsMatch returns whether offerParams contains all parameters present in specParams.
  sig: paramsMatch(specParamStr headerParams, offerParams string)
  behavior: GUARD(len(specParamStr) == 0 -> return true); ACCUMULATE(VisitHeaderParams loop -> result)
  calls: unescapeHeaderValue
  called_by: acceptsOfferType

App.printRoutesMessage (listen.go:516-517)
  printRoutesMessage print all routes with method, path, name and handlers in a format of table, like this: method | path 
  behavior: GUARD(IsChild() -> return); PRECEDENCE(IsChild -> os); ACCUMULATE(FuncForPC loop -> newRoute handlers)
  called_by: printMessages, prefork

DefaultCtx.IsMiddleware (ctx.go:380-381)
  IsMiddleware returns true if the current request handler was registered as middleware.
  behavior: GUARD(c.route == nil -> return false); PRECEDENCE(c)

domainMatch (client/cookiejar.go:327-327)
  domainMatch reports whether host domain-matches the given cookie domain.
  sig: domainMatch(host, domain string)
  behavior: GUARD(host == domain -> return true)
  called_by: cookiesForRequest

routeParser.getMatch (path.go:507-507)
  getMatch parses the passed url and tries to match it against the route segments and determine the parameter positions
  sig: routeParser.getMatch(detectionPath, path string, params *[maxParams]string, p...)
  behavior: GUARD(detectionPath != "" -> return false); ACCUMULATE(len loop -> result)
  calls: CheckConstraint, findParamLen, hasPartialMatchBoundary
  called_by: RoutePatternMatch

Request.PathParam (client/request.go:365-365)
  PathParam returns the value of a named path parameter.
  sig: Request.PathParam(key string)
  behavior: GUARD(val, ok := r.path[key]; ok -> return val)

sanitizeRequestID (middleware/requestid/requestid.go:43-43)
  sanitizeRequestID returns the provided request ID when it is valid, otherwise it tries up to three values from the confi
  sig: sanitizeRequestID(rid string, generator func()
  behavior: GUARD(isValidRequestID(rid) -> return rid); ACCUMULATE(generator loop -> result)
  calls: isValidRequestID
  called_by: New

Request.PathParams (client/request.go:374-374)
  PathParams returns an iterator over all path parameters.
  behavior: DELEGATE(r.path.All -> result)
  calls: All

FiberHandler (middleware/adaptor/adaptor.go:194-194)
  FiberHandler wraps fiber handler to net/http handler
  sig: FiberHandler(h fiber.Handler)
  behavior: DELEGATE(FiberHandlerFunc -> result)
  calls: FiberHandlerFunc

hasPartialMatchBoundary (path.go:486-486)
  sig: hasPartialMatchBoundary(path string, matchedLength int)
  behavior: GUARD(matchedLength < 0 || matchedLength > len(path) -> return false); PRECEDENCE(matchedLength)
  called_by: getMatch

parseRequestCacheControlString (middleware/cache/cache.go:1139-1139)
  sig: parseRequestCacheControlString(cc string)
  behavior: DELEGATE(parseRequestCacheControl -> result)
  calls: parseRequestCacheControl

sanitizePath (middleware/static/static.go:27-27)
  sanitizePath validates and cleans the requested path.
  sig: sanitizePath(p []byte, filesystem fs.FS)
  behavior: PRECEDENCE(bytes -> strings); ACCUMULATE(PathUnescape loop -> result)
  called_by: New

parserRequestURL (client/hooks.go:72-72)
  parserRequestURL sets options for the hostclient and normalizes the URL.
  sig: parserRequestURL(c *Client, req *Request)
  behavior: GUARD(!protocolCheck.MatchString(uri) -> return ErrURLFormat); PRECEDENCE(not_protocolCheck.MatchString -> disablePathNormalizing); ACCUMULATE(ReplaceAll loop -> result)
  calls: DisablePathNormalizing

PathParam.Add (client/request.go:829-829)
  Add adds a path parameter key-value pair.
  sig: PathParam.Add(key, val string)
  called_by: All, Connect, Delete, Get, Head, Options, Patch, Post

parseRequestCacheControl (middleware/cache/cache.go:1104-1104)
  sig: parseRequestCacheControl(cc []byte)
  calls: parseCacheControlDirectives, parseUintDirective
  called_by: New, parseRequestCacheControlString

PathParam.Reset (client/request.go:869-869)
  Reset clears the PathParam map.
  called_by: ReleaseFile, ReleaseRequest, String, AcquireCtx, ResetWithContext, privateLog, privateLogf, privateLogw

PathParam.Del (client/request.go:834-834)
  Del deletes a path parameter by key.
  sig: PathParam.Del(key string)
  called_by: DelCookies, DelData, SetHeaders, DelParams, SetValWithStruct

FiberHandlerFunc (middleware/adaptor/adaptor.go:199-199)
  FiberHandlerFunc wraps fiber handler to net/http handler func
  sig: FiberHandlerFunc(h fiber.Handler)
  behavior: DELEGATE(handlerFunc -> result)
  calls: handlerFunc
  called_by: FiberHandler

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 53 with behavior annotations
uncovered: App.nextCustom, App.next, Request.AddFile, App.processSubAppsRoutes
drill: path.go (~1 lines, RoutePatternMatch)
drill: client/cookiejar.go (~1 lines, pathMatch)
drill: client/request.go (~1 lines, Request.DisablePathNormalizing)

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

## RemoveEscapeCharBytes  (path.go L659-659)
```
func RemoveEscapeCharBytes(word []byte) []byte {
```

## parseRoute  (path.go L245-245)
```
func parseRoute(pattern string, customConstraints ...CustomConstraint) routeParser {
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

## Request.AllFormData  (client/request.go L463-463)
```
func (r *Request) AllFormData() iter.Seq2[string, []string] {
```

## Request.Boundary  (client/request.go L303-303)
```
func (r *Request) Boundary() string {
```

## Request.Client  (client/request.go L99-99)
```
func (r *Request) Client() *Client {
```

## Request.Context  (client/request.go L115-115)
```
func (r *Request) Context() context.Context {
```

## Request.Cookie  (client/request.go L326-326)
```
func (r *Request) Cookie(key string) string {
```

## Request.Cookies  (client/request.go L335-335)
```
func (r *Request) Cookies() iter.Seq2[string, string] {
```

## Request.Custom  (client/request.go L668-668)
```
func (r *Request) Custom(url, method string) (*Response, error) {
```

## Request.DelCookies  (client/request.go L358-358)
```
func (r *Request) DelCookies(key ...string) *Request {
```

## Request.DelFormData  (client/request.go L528-528)
```
func (r *Request) DelFormData(key ...string) *Request {
```

## Request.DelParams  (client/request.go L284-284)
```
func (r *Request) DelParams(key ...string) *Request {
```

## Request.DelPathParams  (client/request.go L397-397)
```
func (r *Request) DelPathParams(key ...string) *Request {
```

## Request.Delete  (client/request.go L653-653)
```
func (r *Request) Delete(url string) (*Response, error) {
```

## Request.File  (client/request.go L536-536)
```
func (r *Request) File(name string) *File {
```

## Request.FileByPath  (client/request.go L561-561)
```
func (r *Request) FileByPath(path string) *File {
```

## Request.Files  (client/request.go L556-556)
```
func (r *Request) Files() []*File {
```

## Request.FormData  (client/request.go L449-449)
```
func (r *Request) FormData(key string) []string {
```

## Request.Get  (client/request.go L633-633)
```
func (r *Request) Get(url string) (*Response, error) {
```

## Request.Head  (client/request.go L643-643)
```
func (r *Request) Head(url string) (*Response, error) {
```

## Request.Header  (client/request.go L130-130)
```
func (r *Request) Header(key string) []string {
```

## Request.Headers  (client/request.go L160-160)
```
func (r *Request) Headers() iter.Seq2[string, []string] {
```

## Request.MaxRedirects  (client/request.go L603-603)
```
func (r *Request) MaxRedirects() int {
```

## Request.Method  (client/request.go L76-76)
```
func (r *Request) Method() string {
```

## Request.Options  (client/request.go L658-658)
```
func (r *Request) Options(url string) (*Response, error) {
```

## Request.Param  (client/request.go L210-210)
```
func (r *Request) Param(key string) []string {
```

## Request.Params  (client/request.go L224-224)
```
func (r *Request) Params() iter.Seq2[string, []string] {
```

## Request.Patch  (client/request.go L663-663)
```
func (r *Request) Patch(url string) (*Response, error) {
```

## Request.PathParam  (client/request.go L365-365)
```
func (r *Request) PathParam(key string) string {
```

## Request.PathParams  (client/request.go L374-374)
```
func (r *Request) PathParams() iter.Seq2[string, string] {
```

## Request.Post  (client/request.go L638-638)
```
func (r *Request) Post(url string) (*Response, error) {
```

## Request.Put  (client/request.go L648-648)
```
func (r *Request) Put(url string) (*Response, error) {
```

## Request.Referer  (client/request.go L314-314)
```
func (r *Request) Referer() string {
```

## Request.Reset  (client/request.go L680-680)
```
func (r *Request) Reset() {
```

## Request.ResetPathParams  (client/request.go L403-403)
```
func (r *Request) ResetPathParams() *Request {
```

## Request.Send  (client/request.go L673-673)
```
func (r *Request) Send() (*Response, error) {
```

## Request.SetBoundary  (client/request.go L308-308)
```
func (r *Request) SetBoundary(b string) *Request {
```

## Request.SetCBOR  (client/request.go L423-423)
```
func (r *Request) SetCBOR(v any) *Request {
```

## Request.SetClient  (client/request.go L104-104)
```
func (r *Request) SetClient(c *Client) *Request {
```

## Request.SetContext  (client/request.go L124-124)
```
func (r *Request) SetContext(ctx context.Context) *Request {
```

## Request.SetCookie  (client/request.go L340-340)
```
func (r *Request) SetCookie(key, val string) *Request {
```

## Request.SetCookies  (client/request.go L346-346)
```
func (r *Request) SetCookies(m map[string]string) *Request {
```

## Request  (client/request.go L46-46)
```
type Request struct {
```
--- END SOURCE SNIPPETS ---

QUESTION: If middleware rewrites the request path and wants Fiber to match routes again, how does the framework restart dispatch and decide whether the request becomes a normal match, a 404, or a 405?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
