# Blind Evaluation Prompt - MRLF v2.1 with File 2 Drill-Down
# Task: blind-echo-rel-2

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

--- CLUE FILE (File 1) ---
=CC v2.1 echo@HEAD 44mod 565sym
? How does Echo relate its router, route match types, and middleware ordering?


-- TREE
echotest/  (2 files)
middleware/  (24 files)
bind.go  binder.go  binder_generic.go  context.go  context_generic.go  echo.go  group.go  httperror.go  ip.go  json.go  renderer.go  response.go  route.go  router.go  router_concurrent.go

-- INDEX
echo.go                                         865L  Config, DefaultHTTPErrorHandler, AcquireContext, Add, AddRoute
router.go                                      1074L  Error, Unwrap, AddRouteError, Add, Remove
bind.go                                         472L  BindBody, BindHeaders, BindPathValues, BindQueryParams, BindUnmarshaler
middleware/static.go                            371L  Static, ToMiddleware, StaticConfig, StaticWithConfig, format
server.go                                       202L  Start, StartTLS, start, StartConfig, filepathOrContent
context.go                                      667L  Attachment, Bind, Blob, Cookie, Cookies
middleware/compress.go                          235L  Gzip, ToMiddleware, GzipConfig, GzipWithConfig, bufferPool
middleware/proxy.go                             441L  NewRandomBalancer, NewRoundRobinBalancer, Proxy, ProxyBalancer, ToMiddleware
middleware/slash.go                             151L  AddTrailingSlash, ToMiddleware, AddTrailingSlashConfig, AddTrailingSlashWithConfig, RemoveTrailingSlash
group.go                                        178L  Add, AddRoute, Any, CONNECT, DELETE
middleware/csrf.go                              307L  CSRF, ToMiddleware, checkSecFetchSiteRequest, CSRFConfig, CSRFWithConfig
binder.go                                      1329L  Error, BindingError, FormFieldBinder, NewBindingError, PathValuesBinder
binder_generic.go                               571L  TimeOpts, bindValue
context_generic.go                               43L  
echotest/context.go                             183L  ServeWithHandler, ToContext, ToContextRecorder, ContextConfig, MultipartForm
echotest/reader.go                               46L  LoadBytes, TrimNewlineEnd, loadBytes
httperror.go                                    162L  Error, StatusCode, Unwrap, Wrap, HTTPError
  ...and 27 more modules

-- SYM
ValueBinder.setError                M binder.go:177    function ValueBinder.setError
Echo.Add                            M echo.go:642    Add registers a new route for an HTTP method an...
Echo.add                            M echo.go:621    function Echo.add
Group.Add                           M group.go:158    Add implements `Echo#Add()` for sub-routes with...
Group.AddRoute                      M group.go:172    AddRoute registers a new Routable with Router
Context.writeContentType            M context.go:121    function Context.writeContentType
ValueBinder.uintValue               M binder.go:727    function ValueBinder.uintValue
Context.Get                         M context.go:380    Get retrieves data from the context.
ValueBinder.uint                    M binder.go:743    function ValueBinder.uint
ValueBinder.int                     M binder.go:515    function ValueBinder.int
ValueBinder.intValue                M binder.go:499    function ValueBinder.intValue
ValueBinder.intsValue               M binder.go:541    function ValueBinder.intsValue
ValueBinder.uintsValue              M binder.go:769    function ValueBinder.uintsValue
Context.Set                         M context.go:387    Set saves data in the context.
ValueBinder.unixTime                M binder.go:1301   function ValueBinder.unixTime
Context.Blob                        M context.go:552    Blob sends a blob response with status code and...
ValueBinder.float                   M binder.go:1006   function ValueBinder.float
ValueBinder.ints                    M binder.go:556    function ValueBinder.ints
ValueBinder.uints                   M binder.go:784    function ValueBinder.uints
bindData                            M bind.go:139    bindData will bind data ONLY fields in destinat...
ValueBinder.floatValue              M binder.go:990    function ValueBinder.floatValue
ValueBinder.floatsValue             M binder.go:1022   function ValueBinder.floatsValue
ValueBinder.bool                    M binder.go:920    function ValueBinder.bool
Context.Response                    M context.go:139    Response returns `*Response`.
fsFile                              M context.go:584    function fsFile
Response.WriteHeader                M response.go:49     WriteHeader sends an HTTP response header with ...
ValueBinder.floats                  M binder.go:1037   function ValueBinder.floats
gzipResponseWriter.WriteHeader      M middleware/compress.go:147    function gzipResponseWriter.WriteHeader
gracefulShutdown                    M server.go:183    function gracefulShutdown
ValueBinder.bindWithDelimiter       M binder.go:411    function ValueBinder.bindWithDelimiter
ValueBinder.boolValue               M binder.go:905    function ValueBinder.boolValue
ValueBinder.boolsValue              M binder.go:931    function ValueBinder.boolsValue
ValueBinder.customFunc              M binder.go:215    function ValueBinder.customFunc
ValueBinder.duration                M binder.go:1167   function ValueBinder.duration
ValueBinder.durationsValue          M binder.go:1198   function ValueBinder.durationsValue
ValueBinder.time                    M binder.go:1095   function ValueBinder.time
ValueBinder.times                   M binder.go:1126   function ValueBinder.times
Context.HTMLBlob                    M context.go:440    HTMLBlob sends an HTTP blob response with statu...
Context.contentDisposition          M context.go:630    function Context.contentDisposition
Context.json                        M context.go:464    function Context.json
Context.setPathValues               M context.go:269    function Context.setPathValues
Context.xml                         M context.go:517    function Context.xml
Echo.ServeHTTP                      M echo.go:695    ServeHTTP implements `http.Handler` interface, ...
ContextConfig.ToContextRecorder     M echotest/context.go:81     ToContextRecorder converts ContextConfig to ech...
sanitizeURI                         M middleware/slash.go:144    function sanitizeURI
Context.SetRequest                  M context.go:134    SetRequest sets `*http.Request`.
RateLimiterMemoryStore.cleanupStaleVisitors M middleware/rate_limiter.go:256    function RateLimiterMemoryStore.cleanupStaleVis...
RequestLoggerConfig.ToMiddleware    M middleware/request_logger.go:246    ToMiddleware converts RequestLoggerConfig into ...
Context.Request                     M context.go:129    Request returns `*http.Request`.
routeMethods.updateAllowHeader      M router.go:251    function routeMethods.updateAllowHeader
ValueBinder.bools                   M binder.go:946    function ValueBinder.bools
ValueBinder.durations               M binder.go:1213   function ValueBinder.durations
setWithProperType                   M bind.go:292    function setWithProperType
node.findStaticChild                M router.go:709    function node.findStaticChild
Echo.Use                            M echo.go:431    Use adds middleware to the chain which is run a...
Context.File                        M context.go:571    File sends a response with the content of the f...
Context.SetResponse                 M context.go:145    SetResponse sets `*http.ResponseWriter`.
StartConfig.start                   M server.go:100    start starts handler with HTTP(s) server.
subFS                               M echo.go:827    function subFS
format                              M middleware/static.go:341    format formats bytes integer to human readable ...
New                                 M echo.go:333    New creates an instance of Echo.
node.setHandler                     M router.go:731    function node.setHandler
unmarshalInputToField               M bind.go:352    function unmarshalInputToField
DefaultHTTPErrorHandler             M echo.go:374    DefaultHTTPErrorHandler creates new default HTT...
NewDefaultFS                        M echo.go:804    NewDefaultFS returns a new defaultFS instance w...
applyMiddleware                     M echo.go:785    function applyMiddleware
Response.Unwrap                     M response.go:105    Unwrap returns the original http.ResponseWriter.
Context.FormValue                   M context.go:319    FormValue returns the form field value for the ...
Context.QueryParam                  M context.go:287    QueryParam returns the query param for the prov...
Context.String                      M context.go:445    String sends a string response with status code.
Context.jsonPBlob                   M context.go:449    function Context.jsonPBlob
newContext                          M context.go:75     function newContext
Echo.AddRoute                       M echo.go:617    AddRoute registers a new Route with default hos...
loadBytes                           M echotest/reader.go:36     function loadBytes
Group.GET                           M group.go:37     GET implements `Echo#GET()` for sub-routes with...
Group.StaticFS                      M group.go:122    StaticFS implements `Echo#StaticFS()` for sub-r...
Group                               C group.go:14     Group is a set of sub-routes for a specified ro...
StatusCode                          M httperror.go:45     StatusCode returns status code from error if it...
BasicAuthWithConfig                 M middleware/basic_auth.go:92     BasicAuthWithConfig returns an BasicAuthWithCon...
BodyDumpWithConfig                  M middleware/body_dump.go:68     BodyDumpWithConfig returns a BodyDump middlewar...
bodyDumpResponseWriter.Write        M middleware/body_dump.go:150    function bodyDumpResponseWriter.Write
BodyLimitWithConfig                 M middleware/body_limit.go:42     BodyLimitWithConfig returns a BodyLimitWithConf...
  ...and 483 more symbols

-- FOCUS
Echo.Match (echo.go:510-510)
  Match registers a new route for multiple HTTP methods and path with matching handler in the router with optional route-l
  sig: Echo.Match(methods []string, path string, handler HandlerFunc, midd...)
  behavior: GUARD(len(errs) > 0 -> panic(errs)); ACCUMULATE(AddRoute loop -> errs)
  calls: AddRoute
  raises: panic

Echo.GET (echo.go:449-449)
  GET registers a new GET route for a path with matching handler in the router with optional route-level middleware.
  sig: Echo.GET(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(e.Add -> result)
  calls: Add
  called_by: FileFS, main

Echo.Any (echo.go:504-504)
  Any registers a new route for all HTTP methods (supported by Echo) and path with matching handler in the router with opt
  sig: Echo.Any(path string, handler HandlerFunc, middleware ...Middlewa...)
  behavior: DELEGATE(e.Add -> result)
  calls: Add

Echo.DELETE (echo.go:443-443)
  DELETE registers a new DELETE route for a path with matching handler in the router with optional route-level middleware.
  sig: Echo.DELETE(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(e.Add -> result)
  calls: Add

Echo.HEAD (echo.go:455-455)
  HEAD registers a new HEAD route for a path with matching handler in the router with optional route-level middleware.
  sig: Echo.HEAD(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(e.Add -> result)
  calls: Add

Echo.PATCH (echo.go:467-467)
  PATCH registers a new PATCH route for a path with matching handler in the router with optional route-level middleware.
  sig: Echo.PATCH(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(e.Add -> result)
  calls: Add

Echo.POST (echo.go:473-473)
  POST registers a new POST route for a path with matching handler in the router with optional route-level middleware.
  sig: Echo.POST(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(e.Add -> result)
  calls: Add

Echo.PUT (echo.go:479-479)
  PUT registers a new PUT route for a path with matching handler in the router with optional route-level middleware.
  sig: Echo.PUT(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(e.Add -> result)
  calls: Add

Echo.TRACE (echo.go:485-485)
  TRACE registers a new TRACE route for a path with matching handler in the router with optional route-level middleware.
  sig: Echo.TRACE(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(e.Add -> result)
  calls: Add

Echo.Use (echo.go:431-431)
  Use adds middleware to the chain which is run after router has found matching route and before route/request handler met
  sig: Echo.Use(middleware ...MiddlewareFunc)
  called_by: Group, main

Echo.Pre (echo.go:426-426)
  Pre adds middleware to the chain which is run before router tries to find matching route.
  sig: Echo.Pre(middleware ...MiddlewareFunc)

concurrentRouter.Route (router_concurrent.go:21-21)
  sig: concurrentRouter.Route(c *Context)
  behavior: DELEGATE(r.router.Route -> result); UNWIND(defer)

Echo.AddRoute (echo.go:617-617)
  AddRoute registers a new Route with default host Router
  sig: Echo.AddRoute(route Route)
  behavior: DELEGATE(e.add -> result)
  calls: add
  called_by: Match

DefaultRouter.storeRouteInfo (router.go:538-538)
  sig: DefaultRouter.storeRouteInfo(ri RouteInfo)
  behavior: ACCUMULATE(loop -> result)
  called_by: Add

AddRouteError (router.go:428-428)
  AddRouteError is error returned by Router.Add containing information what actual route adding failed.
  methods: Error, Unwrap

WrapMiddleware (echo.go:766-766)
  WrapMiddleware wraps `func(http.Handler) http.Handler` into `echo.MiddlewareFunc`
  sig: WrapMiddleware(m func(http.Handler)
  calls: ServeHTTP

Group.AddRoute (group.go:172-172)
  AddRoute registers a new Routable with Router
  sig: Group.AddRoute(route Route)
  behavior: DELEGATE(g.echo.add -> result)
  called_by: Add, Match

Group.Match (group.go:77-77)
  Match implements `Echo#Match()` for sub-routes within the Group.
  sig: Group.Match(methods []string, path string, handler HandlerFunc, midd...)
  behavior: GUARD(len(errs) > 0 -> panic(errs)); ACCUMULATE(AddRoute loop -> errs)
  calls: AddRoute
  raises: panic

Echo.Add (echo.go:642-642)
  Add registers a new route for an HTTP method and path with matching handler in the router with optional route-level midd
  sig: Echo.Add(method, path string, handler HandlerFunc, middleware ......)
  behavior: GUARD(err != nil -> panic(err))
  calls: add
  called_by: Any, CONNECT, DELETE, File, GET, HEAD, OPTIONS, PATCH
  raises: panic

DefaultRouter (router.go:60-60)
  DefaultRouter is the registry of all registered routes for an `Echo` instance for request matching and URL path paramete
  methods: Add, Remove, Route, Routes, insert, storeRouteInfo

Echo.CONNECT (echo.go:437-437)
  CONNECT registers a new CONNECT route for a path with matching handler in the router with optional route-level middlewar
  sig: Echo.CONNECT(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(e.Add -> result)
  calls: Add

Echo.File (echo.go:609-609)
  File registers a new route with path to serve a static file with optional route-level middleware.
  sig: Echo.File(path, file string, middleware ...MiddlewareFunc)
  calls: Add

Echo.Group (echo.go:659-659)
  Group creates a new router group with prefix and optional group-level middleware.
  sig: Echo.Group(prefix string, m ...MiddlewareFunc)
  calls: Use

Echo.OPTIONS (echo.go:461-461)
  OPTIONS registers a new OPTIONS route for a path with matching handler in the router with optional route-level middlewar
  sig: Echo.OPTIONS(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(e.Add -> result)
  calls: Add

Group.RouteNotFound (group.go:153-153)
  RouteNotFound implements `Echo#RouteNotFound()` for sub-routes within the Group.
  sig: Group.RouteNotFound(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(g.Add -> result)
  calls: Add

Route (route.go:16-16)
  Route contains information to adding/registering new route with the router.
  methods: ToRouteInfo, WithPrefix

AddTrailingSlash (middleware/slash.go:29-29)
  AddTrailingSlash returns a root level (before router) middleware which adds a trailing slash to the request `URL#Path`.
  behavior: DELEGATE(AddTrailingSlashWithConfig -> result)
  calls: AddTrailingSlashWithConfig

RemoveTrailingSlash (middleware/slash.go:93-93)
  RemoveTrailingSlash returns a root level (before router) middleware which removes a trailing slash from the request URI.
  behavior: DELEGATE(RemoveTrailingSlashWithConfig -> result)
  calls: RemoveTrailingSlashWithConfig

RequestLogger (middleware/request_logger.go:395-395)
  RequestLogger creates Request Logger middleware with Echo default settings that uses Context.Logger() as logger.
  calls: RequestLoggerWithConfig

routeMethods (router.go:148-148)
  type routeMethods
  methods: find, isHandler, set, updateAllowHeader

routeMethods.find (router.go:213-213)
  sig: routeMethods.find(method string, fallbackToAny bool)
  behavior: GUARD(r != nil || !fallbackToAny -> return r); DISPATCH(method)
  called_by: Remove, Route

DefaultRouter.Route (router.go:791-791)
  Route looks up a handler registered for method and path.
  sig: DefaultRouter.Route(c *Context)
  behavior: PRECEDENCE(cap -> not_r.useEscapedPathForRouting -> currentNode); ACCUMULATE(len loop -> searchIndex)
  calls: findStaticChild, node, find

Echo.RouteNotFound (echo.go:495-495)
  RouteNotFound registers a special-case route which is executed when no other route is found (i.e.
  sig: Echo.RouteNotFound(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(e.Add -> result)
  calls: Add

routeMethods.set (router.go:171-171)
  sig: routeMethods.set(method string, r *routeMethod)
  behavior: DISPATCH(method)
  calls: updateAllowHeader
  called_by: setHandler

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 188 symbols in L3, 119 with behavior annotations
uncovered: Echo.ServeHTTP, Echo.serveHTTP, randomBalancer.Next, DefaultRouter.Routes
drill: echo.go (~1 lines, Echo.Match)
drill: echo.go (~1 lines, Echo.GET)
drill: echo.go (~1 lines, Echo.DELETE)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## Echo.Match  (echo.go L510-510)
```
func (e *Echo) Match(methods []string, path string, handler HandlerFunc, middleware ...MiddlewareFunc) Routes {
```

## Echo.GET  (echo.go L449-449)
```
func (e *Echo) GET(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo {
```

## Echo.DELETE  (echo.go L443-443)
```
func (e *Echo) DELETE(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo {
```

## Config  (echo.go L237-237)
```
type Config struct {
```

## DefaultHTTPErrorHandler  (echo.go L374-374)
```
func DefaultHTTPErrorHandler(exposeError bool) HTTPErrorHandler {
```

## Echo.AcquireContext  (echo.go L684-684)
```
func (e *Echo) AcquireContext() *Context {
```

## Echo.Add  (echo.go L642-642)
```
func (e *Echo) Add(method, path string, handler HandlerFunc, middleware ...MiddlewareFunc) RouteInfo {
```

## Echo.AddRoute  (echo.go L617-617)
```
func (e *Echo) AddRoute(route Route) (RouteInfo, error) {
```

## Echo.Any  (echo.go L504-504)
```
func (e *Echo) Any(path string, handler HandlerFunc, middleware ...MiddlewareFunc) RouteInfo {
```

## Echo.CONNECT  (echo.go L437-437)
```
func (e *Echo) CONNECT(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo {
```

## Echo.File  (echo.go L609-609)
```
func (e *Echo) File(path, file string, middleware ...MiddlewareFunc) RouteInfo {
```

## Echo.FileFS  (echo.go L591-591)
```
func (e *Echo) FileFS(path, file string, filesystem fs.FS, m ...MiddlewareFunc) RouteInfo {
```

## Echo.Group  (echo.go L659-659)
```
func (e *Echo) Group(prefix string, m ...MiddlewareFunc) (g *Group) {
```

## Echo.HEAD  (echo.go L455-455)
```
func (e *Echo) HEAD(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo {
```

## Echo.Middlewares  (echo.go L678-678)
```
func (e *Echo) Middlewares() []MiddlewareFunc {
```

## Echo.NewContext  (echo.go L357-357)
```
func (e *Echo) NewContext(r *http.Request, w http.ResponseWriter) *Context {
```

## Echo.OPTIONS  (echo.go L461-461)
```
func (e *Echo) OPTIONS(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo {
```

## Echo.PATCH  (echo.go L467-467)
```
func (e *Echo) PATCH(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo {
```

## Echo.POST  (echo.go L473-473)
```
func (e *Echo) POST(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo {
```

## Echo.PUT  (echo.go L479-479)
```
func (e *Echo) PUT(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo {
```

## Echo.Pre  (echo.go L426-426)
```
func (e *Echo) Pre(middleware ...MiddlewareFunc) {
```

## Echo.PreMiddlewares  (echo.go L670-670)
```
func (e *Echo) PreMiddlewares() []MiddlewareFunc {
```

## Echo.ReleaseContext  (echo.go L690-690)
```
func (e *Echo) ReleaseContext(c *Context) {
```

## Echo.RouteNotFound  (echo.go L495-495)
```
func (e *Echo) RouteNotFound(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo {
```

## Echo.Router  (echo.go L362-362)
```
func (e *Echo) Router() Router {
```

## Echo.ServeHTTP  (echo.go L695-695)
```
func (e *Echo) ServeHTTP(w http.ResponseWriter, r *http.Request) {
```

## Echo.Start  (echo.go L744-744)
```
func (e *Echo) Start(address string) error {
```

## Echo.Static  (echo.go L533-533)
```
func (e *Echo) Static(pathPrefix, fsRoot string, middleware ...MiddlewareFunc) RouteInfo {
```

## Echo.StaticFS  (echo.go L548-548)
```
func (e *Echo) StaticFS(pathPrefix string, filesystem fs.FS, middleware ...MiddlewareFunc) RouteInfo {
```

## Echo.TRACE  (echo.go L485-485)
```
func (e *Echo) TRACE(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo {
```

## Echo.Use  (echo.go L431-431)
```
func (e *Echo) Use(middleware ...MiddlewareFunc) {
```

## Echo.add  (echo.go L621-621)
```
func (e *Echo) add(route Route) (RouteInfo, error) {
```

## Echo.serveHTTP  (echo.go L700-700)
```
func (e *Echo) serveHTTP(w http.ResponseWriter, r *http.Request) {
```

## Echo  (echo.go L68-68)
```
type Echo struct {
```

## JSONSerializer  (echo.go L106-106)
```
type JSONSerializer interface {
```

## MiddlewareConfigurator  (echo.go L121-121)
```
type MiddlewareConfigurator interface {
```

## MustSubFS  (echo.go L850-850)
```
func MustSubFS(currentFs fs.FS, fsRoot string) fs.FS {
```

## New  (echo.go L333-333)
```
func New() *Echo {
```

## NewDefaultFS  (echo.go L804-804)
```
func NewDefaultFS(dir string) fs.FS {
```

## NewWithConfig  (echo.go L294-294)
```
func NewWithConfig(config Config) *Echo {
```

## StaticDirectoryHandler  (echo.go L559-559)
```
func StaticDirectoryHandler(fileSystem fs.FS, disablePathUnescaping bool) HandlerFunc {
```

## StaticFileHandler  (echo.go L599-599)
```
func StaticFileHandler(file string, filesystem fs.FS) HandlerFunc {
```

## Validator  (echo.go L126-126)
```
type Validator interface {
```

## WrapHandler  (echo.go L752-752)
```
func WrapHandler(h http.Handler) HandlerFunc {
```

## WrapMiddleware  (echo.go L766-766)
```
func WrapMiddleware(m func(http.Handler) http.Handler) MiddlewareFunc {
```

## applyMiddleware  (echo.go L785-785)
```
func applyMiddleware(h HandlerFunc, middleware ...MiddlewareFunc) HandlerFunc {
```

## defaultFS.Open  (echo.go L811-811)
```
func (fs defaultFS) Open(name string) (fs.File, error) {
```

## defaultFS  (echo.go L797-797)
```
type defaultFS struct {
```

## hello  (echo.go L20-20)
```
	func hello(c *echo.Context) error {
```

## main  (echo.go L24-24)
```
	func main() {
```

## sanitizeURI  (middleware/slash.go L144-144)
```
func sanitizeURI(uri string) string {
```

## subFS  (echo.go L827-827)
```
func subFS(currentFs fs.FS, root string) (fs.FS, error) {
```
--- END SOURCE SNIPPETS ---

QUESTION: How does Echo relate its router, route match types, and middleware ordering?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
