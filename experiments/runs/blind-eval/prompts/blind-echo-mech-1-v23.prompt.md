# Blind Evaluation Prompt - MRLF v2.1 with File 2 Drill-Down
# Task: blind-echo-mech-1

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

--- CLUE FILE (File 1) ---
=CC v2.1 echo@HEAD 44mod 565sym
? How does Echo decide which route wins when static segments, parameters, and wildcards overlap?


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
Echo.Static (echo.go:533-533)
  Static registers a new route with path prefix to serve static files from the provided root directory.
  sig: Echo.Static(pathPrefix, fsRoot string, middleware ...MiddlewareFunc)
  behavior: DELEGATE(e.Add -> result)
  calls: Add, MustSubFS, StaticDirectoryHandler

Echo.StaticFS (echo.go:548-548)
  StaticFS registers a new route with path prefix to serve static files from the provided file system.
  sig: Echo.StaticFS(pathPrefix string, filesystem fs.FS, middleware ...Middl...)
  behavior: DELEGATE(e.Add -> result)
  calls: Add, StaticDirectoryHandler

Group.Static (group.go:112-112)
  Static implements `Echo#Static()` for sub-routes within the Group.
  sig: Group.Static(pathPrefix, fsRoot string, middleware ...MiddlewareFunc)
  behavior: DELEGATE(g.StaticFS -> result)
  calls: StaticFS

Group.StaticFS (group.go:122-122)
  StaticFS implements `Echo#StaticFS()` for sub-routes within the Group.
  sig: Group.StaticFS(pathPrefix string, filesystem fs.FS, middleware ...Middl...)
  behavior: DELEGATE(g.Add -> result)
  calls: Add
  called_by: Static

RouteInfo.Reverse (route.go:75-75)
  Reverse reverses route to URL string by replacing path parameters with given params values.
  sig: RouteInfo.Reverse(pathValues ...any)
  behavior: DELEGATE(uri.String -> result); ACCUMULATE(loop -> result)
  called_by: Reverse

Echo.Any (echo.go:504-504)
  Any registers a new route for all HTTP methods (supported by Echo) and path with matching handler in the router with opt
  sig: Echo.Any(path string, handler HandlerFunc, middleware ...Middlewa...)
  behavior: DELEGATE(e.Add -> result)
  calls: Add

Echo.File (echo.go:609-609)
  File registers a new route with path to serve a static file with optional route-level middleware.
  sig: Echo.File(path, file string, middleware ...MiddlewareFunc)
  calls: Add

Group.RouteNotFound (group.go:153-153)
  RouteNotFound implements `Echo#RouteNotFound()` for sub-routes within the Group.
  sig: Group.RouteNotFound(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(g.Add -> result)
  calls: Add

Routes.Reverse (route.go:117-117)
  Reverse reverses route to URL string by replacing path parameters with given params values.
  sig: Routes.Reverse(routeName string, pathValues ...any)
  behavior: ACCUMULATE(loop -> result)
  calls: Reverse

Echo.AddRoute (echo.go:617-617)
  AddRoute registers a new Route with default host Router
  sig: Echo.AddRoute(route Route)
  behavior: DELEGATE(e.add -> result)
  calls: add
  called_by: Match

StaticDirectoryHandler (echo.go:559-559)
  StaticDirectoryHandler creates handler function to serve files from provided file system When disablePathUnescaping is s
  sig: StaticDirectoryHandler(fileSystem fs.FS, disablePathUnescaping bool)
  calls: Open, sanitizeURI
  called_by: Static, StaticFS

Echo.RouteNotFound (echo.go:495-495)
  RouteNotFound registers a special-case route which is executed when no other route is found (i.e.
  sig: Echo.RouteNotFound(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(e.Add -> result)
  calls: Add

StaticFileHandler (echo.go:599-599)
  StaticFileHandler creates handler function to serve file from provided file system.
  sig: StaticFileHandler(file string, filesystem fs.FS)
  called_by: FileFS

Echo.add (echo.go:621-621)
  sig: Echo.add(route Route)
  behavior: GUARD(e -> RouteInfo); PRECEDENCE(e -> err -> paramsCount)
  calls: Add
  called_by: Add, AddRoute

Group.AddRoute (group.go:172-172)
  AddRoute registers a new Routable with Router
  sig: Group.AddRoute(route Route)
  behavior: DELEGATE(g.echo.add -> result)
  called_by: Add, Match

Static (middleware/static.go:144-144)
  Static returns a Static middleware to serves static content from the provided root directory.
  sig: Static(root string)
  behavior: DELEGATE(StaticWithConfig -> result)
  calls: StaticWithConfig

Routes.FindByMethodPath (route.go:127-127)
  FindByMethodPath searched for matching route info by method and path
  sig: Routes.FindByMethodPath(method string, path string)
  behavior: GUARD(r -> RouteInfo); ACCUMULATE(loop -> result)

concurrentRouter.Route (router_concurrent.go:21-21)
  sig: concurrentRouter.Route(c *Context)
  behavior: DELEGATE(r.router.Route -> result); UNWIND(defer)

Echo (echo.go:68-68)
  Echo is the top-level framework instance.
  methods: AcquireContext, Add, AddRoute, Any, CONNECT, DELETE

Echo.Add (echo.go:642-642)
  Add registers a new route for an HTTP method and path with matching handler in the router with optional route-level midd
  sig: Echo.Add(method, path string, handler HandlerFunc, middleware ......)
  behavior: GUARD(err -> raise_panic)
  calls: add
  called_by: Any, CONNECT, DELETE, File, GET, HEAD, OPTIONS, PATCH
  raises: panic

routeMethods (router.go:148-148)
  type routeMethods
  methods: find, isHandler, set, updateAllowHeader

Echo.GET (echo.go:449-449)
  GET registers a new GET route for a path with matching handler in the router with optional route-level middleware.
  sig: Echo.GET(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(e.Add -> result)
  calls: Add
  called_by: FileFS, main

Echo.FileFS (echo.go:591-591)
  FileFS registers a new route with path to serve file from the provided file system.
  sig: Echo.FileFS(path, file string, filesystem fs.FS, m ...MiddlewareFunc)
  behavior: DELEGATE(e.GET -> result)
  calls: GET, StaticFileHandler

DefaultRouter.Route (router.go:791-791)
  Route looks up a handler registered for method and path.
  sig: DefaultRouter.Route(c *Context)
  behavior: PRECEDENCE(cap -> not_r.useEscapedPathForRouting -> currentNode); ACCUMULATE(loop -> searchIndex)
  calls: findStaticChild, node, find

routeMethods.find (router.go:213-213)
  sig: routeMethods.find(method string, fallbackToAny bool)
  behavior: GUARD(r -> pass_through); DISPATCH(method)
  called_by: Remove, Route

node.findStaticChild (router.go:709-709)
  sig: node.findStaticChild(l byte)
  behavior: ACCUMULATE(loop -> result)
  called_by: Remove, Route, findChildWithLabel

routeMethods.set (router.go:171-171)
  sig: routeMethods.set(method string, r *routeMethod)
  behavior: DISPATCH(method)
  calls: updateAllowHeader
  called_by: setHandler

DefaultRouter.storeRouteInfo (router.go:538-538)
  sig: DefaultRouter.storeRouteInfo(ri RouteInfo)
  behavior: ACCUMULATE(loop -> result)
  called_by: Add

Echo.CONNECT (echo.go:437-437)
  CONNECT registers a new CONNECT route for a path with matching handler in the router with optional route-level middlewar
  sig: Echo.CONNECT(path string, h HandlerFunc, m ...MiddlewareFunc)
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

Echo.Match (echo.go:510-510)
  Match registers a new route for multiple HTTP methods and path with matching handler in the router with optional route-l
  sig: Echo.Match(methods []string, path string, handler HandlerFunc, midd...)
  behavior: GUARD(len -> raise_panic); ACCUMULATE(loop -> errs)
  calls: AddRoute
  raises: panic

Echo.OPTIONS (echo.go:461-461)
  OPTIONS registers a new OPTIONS route for a path with matching handler in the router with optional route-level middlewar
  sig: Echo.OPTIONS(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(e.Add -> result)
  calls: Add

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 48 with behavior annotations
drill: echo.go (~1 lines, Echo.StaticFS)
drill: echo.go (~1 lines, Echo.Static)
drill: group.go (~1 lines, Group.StaticFS)
drill: route.go (~1 lines, RouteInfo.Reverse)
drill: route.go (~1 lines, Routes.Reverse)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## Echo.StaticFS  (echo.go L548-548)
```
func (e *Echo) StaticFS(pathPrefix string, filesystem fs.FS, middleware ...MiddlewareFunc) RouteInfo {
```

## Echo.Static  (echo.go L533-533)
```
func (e *Echo) Static(pathPrefix, fsRoot string, middleware ...MiddlewareFunc) RouteInfo {
```

## Group.StaticFS  (group.go L122-122)
```
func (g *Group) StaticFS(pathPrefix string, filesystem fs.FS, middleware ...MiddlewareFunc) RouteInfo {
```

## RouteInfo.Reverse  (route.go L75-75)
```
func (r RouteInfo) Reverse(pathValues ...any) string {
```

## Routes.Reverse  (route.go L117-117)
```
func (r Routes) Reverse(routeName string, pathValues ...any) (string, error) {
```

## StaticDirectoryHandler  (echo.go L559-559)
```
func StaticDirectoryHandler(fileSystem fs.FS, disablePathUnescaping bool) HandlerFunc {
```

## MustSubFS  (echo.go L850-850)
```
func MustSubFS(currentFs fs.FS, fsRoot string) fs.FS {
```

## Group.Add  (group.go L158-158)
```
func (g *Group) Add(method, path string, handler HandlerFunc, middleware ...MiddlewareFunc) RouteInfo {
```

## Group.AddRoute  (group.go L172-172)
```
func (g *Group) AddRoute(route Route) (RouteInfo, error) {
```

## Group.Any  (group.go L72-72)
```
func (g *Group) Any(path string, handler HandlerFunc, middleware ...MiddlewareFunc) RouteInfo {
```

## Group.CONNECT  (group.go L27-27)
```
func (g *Group) CONNECT(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo {
```

## Group.DELETE  (group.go L32-32)
```
func (g *Group) DELETE(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo {
```

## Group.File  (group.go L143-143)
```
func (g *Group) File(path, file string, middleware ...MiddlewareFunc) RouteInfo {
```

## Group.FileFS  (group.go L135-135)
```
func (g *Group) FileFS(path, file string, filesystem fs.FS, m ...MiddlewareFunc) RouteInfo {
```

## Group.GET  (group.go L37-37)
```
func (g *Group) GET(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo {
```

## Group.Group  (group.go L103-103)
```
func (g *Group) Group(prefix string, middleware ...MiddlewareFunc) (sg *Group) {
```

## Group.HEAD  (group.go L42-42)
```
func (g *Group) HEAD(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo {
```

## Group.Match  (group.go L77-77)
```
func (g *Group) Match(methods []string, path string, handler HandlerFunc, middleware ...MiddlewareFunc) Routes {
```

## Group.OPTIONS  (group.go L47-47)
```
func (g *Group) OPTIONS(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo {
```

## Group.PATCH  (group.go L52-52)
```
func (g *Group) PATCH(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo {
```

## Group.POST  (group.go L57-57)
```
func (g *Group) POST(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo {
```

## Group.PUT  (group.go L62-62)
```
func (g *Group) PUT(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo {
```

## Group.RouteNotFound  (group.go L153-153)
```
func (g *Group) RouteNotFound(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo {
```

## Group.Static  (group.go L112-112)
```
func (g *Group) Static(pathPrefix, fsRoot string, middleware ...MiddlewareFunc) RouteInfo {
```

## Group.TRACE  (group.go L67-67)
```
func (g *Group) TRACE(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo {
```

## Group.Use  (group.go L22-22)
```
func (g *Group) Use(middleware ...MiddlewareFunc) {
```

## Group  (group.go L14-14)
```
type Group struct {
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

## Echo.DELETE  (echo.go L443-443)
```
func (e *Echo) DELETE(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo {
```

## Echo.File  (echo.go L609-609)
```
func (e *Echo) File(path, file string, middleware ...MiddlewareFunc) RouteInfo {
```

## Echo.FileFS  (echo.go L591-591)
```
func (e *Echo) FileFS(path, file string, filesystem fs.FS, m ...MiddlewareFunc) RouteInfo {
```

## Echo.GET  (echo.go L449-449)
```
func (e *Echo) GET(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo {
```

## Echo.Group  (echo.go L659-659)
```
func (e *Echo) Group(prefix string, m ...MiddlewareFunc) (g *Group) {
```

## Echo.HEAD  (echo.go L455-455)
```
func (e *Echo) HEAD(path string, h HandlerFunc, m ...MiddlewareFunc) RouteInfo {
```

## Echo.Match  (echo.go L510-510)
```
func (e *Echo) Match(methods []string, path string, handler HandlerFunc, middleware ...MiddlewareFunc) Routes {
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

## HandlerName  (route.go L99-99)
```
func HandlerName(h HandlerFunc) string {
```

## Route.ToRouteInfo  (route.go L25-25)
```
func (r Route) ToRouteInfo(params []string) RouteInfo {
```

## Route.WithPrefix  (route.go L40-40)
```
func (r Route) WithPrefix(pathPrefix string, middlewares []MiddlewareFunc) Route {
```

## Route  (route.go L16-16)
```
type Route struct {
```

## RouteInfo.Clone  (route.go L65-65)
```
func (r RouteInfo) Clone() RouteInfo {
```

## RouteInfo  (route.go L53-53)
```
type RouteInfo struct {
```

## Routes.Clone  (route.go L108-108)
```
func (r Routes) Clone() Routes {
```

## Routes.FilterByMethod  (route.go L141-141)
```
func (r Routes) FilterByMethod(method string) (Routes, error) {
```

## Routes.FilterByName  (route.go L177-177)
```
func (r Routes) FilterByName(name string) (Routes, error) {
```

## Routes.FilterByPath  (route.go L159-159)
```
func (r Routes) FilterByPath(path string) (Routes, error) {
```

## Routes.FindByMethodPath  (route.go L127-127)
```
func (r Routes) FindByMethodPath(method string, path string) (RouteInfo, error) {
```
--- END SOURCE SNIPPETS ---

QUESTION: How does Echo decide which route wins when static segments, parameters, and wildcards overlap?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
