# Blind Evaluation Prompt - MRLF v2.1 with File 2 Drill-Down
# Task: blind-echo-rel-1

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

--- CLUE FILE (File 1) ---
=CC v2.1 echo@HEAD 44mod 565sym
? What are the main relationships among `Echo`, `Group`, `Context`, and handlers during normal request dispatch?


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
RequestLogger (middleware/request_logger.go:395-395)
  RequestLogger creates Request Logger middleware with Echo default settings that uses Context.Logger() as logger.
  calls: RequestLoggerWithConfig

Context (context.go:40-40)
  Context represents the context of the current HTTP request.
  methods: Attachment, Bind, Blob, Cookie, Cookies, Echo

Group.Add (group.go:158-158)
  Add implements `Echo#Add()` for sub-routes within the Group.
  sig: Group.Add(method, path string, handler HandlerFunc, middleware ......)
  behavior: GUARD(err != nil -> panic(err))
  calls: AddRoute
  called_by: Any, CONNECT, DELETE, File, GET, HEAD, OPTIONS, PATCH
  raises: panic

ContextConfig.ToContextRecorder (echotest/context.go:81-81)
  ToContextRecorder converts ContextConfig to echo.Context and httptest.ResponseRecorder
  sig: ContextConfig.ToContextRecorder(t *testing.T)
  called_by: ServeWithHandler, ToContext

Group.GET (group.go:37-37)
  GET implements `Echo#GET()` for sub-routes within the Group.
  sig: Group.GET(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(g.Add -> result)
  calls: Add
  called_by: FileFS

Group.StaticFS (group.go:122-122)
  StaticFS implements `Echo#StaticFS()` for sub-routes within the Group.
  sig: Group.StaticFS(pathPrefix string, filesystem fs.FS, middleware ...Middl...)
  behavior: DELEGATE(g.Add -> result)
  calls: Add
  called_by: Static

ContextConfig (echotest/context.go:20-20)
  ContextConfig is configuration for creating echo.Context for testing purposes.
  methods: ServeWithHandler, ToContext, ToContextRecorder

Context.InitializeRoute (context.go:263-263)
  InitializeRoute sets the route related variables of this request to the context.
  sig: Context.InitializeRoute(ri *RouteInfo, pathValues *PathValues)
  calls: setPathValues

ContextConfig.ToContext (echotest/context.go:75-75)
  ToContext converts ContextConfig to echo.Context
  sig: ContextConfig.ToContext(t *testing.T)
  calls: ToContextRecorder

Group.Any (group.go:72-72)
  Any implements `Echo#Any()` for sub-routes within the Group.
  sig: Group.Any(path string, handler HandlerFunc, middleware ...Middlewa...)
  behavior: DELEGATE(g.Add -> result)
  calls: Add

Group.CONNECT (group.go:27-27)
  CONNECT implements `Echo#CONNECT()` for sub-routes within the Group.
  sig: Group.CONNECT(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(g.Add -> result)
  calls: Add

Group.DELETE (group.go:32-32)
  DELETE implements `Echo#DELETE()` for sub-routes within the Group.
  sig: Group.DELETE(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(g.Add -> result)
  calls: Add

Group.File (group.go:143-143)
  File implements `Echo#File()` for sub-routes within the Group.
  sig: Group.File(path, file string, middleware ...MiddlewareFunc)
  calls: Add

Group.FileFS (group.go:135-135)
  FileFS implements `Echo#FileFS()` for sub-routes within the Group.
  sig: Group.FileFS(path, file string, filesystem fs.FS, m ...MiddlewareFunc)
  behavior: DELEGATE(g.GET -> result)
  calls: GET

Group.HEAD (group.go:42-42)
  HEAD implements `Echo#HEAD()` for sub-routes within the Group.
  sig: Group.HEAD(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(g.Add -> result)
  calls: Add

Group.OPTIONS (group.go:47-47)
  OPTIONS implements `Echo#OPTIONS()` for sub-routes within the Group.
  sig: Group.OPTIONS(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(g.Add -> result)
  calls: Add

Group.PATCH (group.go:52-52)
  PATCH implements `Echo#PATCH()` for sub-routes within the Group.
  sig: Group.PATCH(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(g.Add -> result)
  calls: Add

Group.POST (group.go:57-57)
  POST implements `Echo#POST()` for sub-routes within the Group.
  sig: Group.POST(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(g.Add -> result)
  calls: Add

Group.PUT (group.go:62-62)
  PUT implements `Echo#PUT()` for sub-routes within the Group.
  sig: Group.PUT(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(g.Add -> result)
  calls: Add

Group.RouteNotFound (group.go:153-153)
  RouteNotFound implements `Echo#RouteNotFound()` for sub-routes within the Group.
  sig: Group.RouteNotFound(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(g.Add -> result)
  calls: Add

Group.Static (group.go:112-112)
  Static implements `Echo#Static()` for sub-routes within the Group.
  sig: Group.Static(pathPrefix, fsRoot string, middleware ...MiddlewareFunc)
  behavior: DELEGATE(g.StaticFS -> result)
  calls: StaticFS

Group.TRACE (group.go:67-67)
  TRACE implements `Echo#TRACE()` for sub-routes within the Group.
  sig: Group.TRACE(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(g.Add -> result)
  calls: Add

Context.Reset (context.go:107-107)
  Reset resets the context after request completes.
  sig: Context.Reset(r *http.Request, w http.ResponseWriter)

Group.Match (group.go:77-77)
  Match implements `Echo#Match()` for sub-routes within the Group.
  sig: Group.Match(methods []string, path string, handler HandlerFunc, midd...)
  behavior: GUARD(len(errs) > 0 -> panic(errs)); ACCUMULATE(AddRoute loop -> errs)
  calls: AddRoute
  raises: panic

Group.Use (group.go:22-22)
  Use implements `Echo#Use()` for sub-routes within the Group.
  sig: Group.Use(middleware ...MiddlewareFunc)

DefaultRouter (router.go:60-60)
  DefaultRouter is the registry of all registered routes for an `Echo` instance for request matching and URL path paramete
  methods: Add, Remove, Route, Routes, insert, storeRouteInfo

NewVirtualHostHandler (vhost.go:10-10)
  NewVirtualHostHandler creates instance of Echo that routes requests to given virtual hosts when hosts in request does no
  sig: NewVirtualHostHandler(vhosts map[string]*Echo)

Echo.AcquireContext (echo.go:684-684)
  AcquireContext returns an empty `Context` instance from the pool.
  behavior: DELEGATE(e.contextPool.Get -> result)

Echo.NewContext (echo.go:357-357)
  NewContext returns a new Context instance.
  sig: Echo.NewContext(r *http.Request, w http.ResponseWriter)
  behavior: DELEGATE(newContext -> result)

main (echo.go:24-24)
  calls: GET, Start, Use, New

Context.SetRequest (context.go:134-134)
  SetRequest sets `*http.Request`.
  sig: Context.SetRequest(r *http.Request)
  called_by: newContext

Echo.Group (echo.go:659-659)
  Group creates a new router group with prefix and optional group-level middleware.
  sig: Echo.Group(prefix string, m ...MiddlewareFunc)
  calls: Use

Context.Request (context.go:129-129)
  Request returns `*http.Request`.
  called_by: fsFile

Context.Echo (context.go:665-665)
  Echo returns the `Echo` instance.

Echo.ReleaseContext (echo.go:690-690)
  ReleaseContext returns the `Context` instance back to the pool.
  sig: Echo.ReleaseContext(c *Context)

Context.json (context.go:464-464)
  sig: Context.json(code int, i any, indent string)
  behavior: DELEGATE(c.echo.JSONSerializer.Serialize -> result)
  calls: Response, SetResponse, writeContentType
  called_by: JSON, JSONPretty

Context.SetPathValues (context.go:255-255)
  SetPathValues sets path parameters for current request.
  sig: Context.SetPathValues(pathValues PathValues)
  behavior: GUARD(pathValues == nil -> panic("context SetP...)
  calls: setPathValues
  raises: panic

ContextTimeout (middleware/context_timeout.go:28-28)
  ContextTimeout returns a middleware which returns error (503 Service Unavailable error) to client when underlying method
  sig: ContextTimeout(timeout time.Duration)
  behavior: DELEGATE(ContextTimeoutWithConfig -> result)
  calls: ContextTimeoutWithConfig

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 46 with behavior annotations
uncovered: Group.AddRoute, Context.FormValues, Context.FormValue, Context.RealIP
drill: middleware/request_logger.go (~1 lines, RequestLogger)
drill: group.go (~1 lines, Group.Add)
drill: echotest/context.go (~1 lines, ContextConfig.ToContextRecorder)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## RequestLogger  (middleware/request_logger.go L395-395)
```
func RequestLogger() echo.MiddlewareFunc {
```

## Group.Add  (group.go L158-158)
```
func (g *Group) Add(method, path string, handler HandlerFunc, middleware ...MiddlewareFunc) RouteInfo {
```

## ContextConfig.ToContextRecorder  (echotest/context.go L81-81)
```
func (conf ContextConfig) ToContextRecorder(t *testing.T) (*echo.Context, *httptest.ResponseRecorder) {
```

## RequestLoggerWithConfig  (middleware/request_logger.go L237-237)
```
func RequestLoggerWithConfig(config RequestLoggerConfig) echo.MiddlewareFunc {
```

## RequestLoggerConfig.ToMiddleware  (middleware/request_logger.go L246-246)
```
func (config RequestLoggerConfig) ToMiddleware() (echo.MiddlewareFunc, error) {
```

## RequestLoggerConfig  (middleware/request_logger.go L124-124)
```
type RequestLoggerConfig struct {
```

## RequestLoggerValues  (middleware/request_logger.go L189-189)
```
type RequestLoggerValues struct {
```

## ContextConfig.ServeWithHandler  (echotest/context.go L167-167)
```
func (conf ContextConfig) ServeWithHandler(t *testing.T, handler echo.HandlerFunc, opts ...any) *httptest.ResponseRecorder {
```

## ContextConfig.ToContext  (echotest/context.go L75-75)
```
func (conf ContextConfig) ToContext(t *testing.T) *echo.Context {
```

## ContextConfig  (echotest/context.go L20-20)
```
type ContextConfig struct {
```

## MultipartForm  (echotest/context.go L62-62)
```
type MultipartForm struct {
```

## MultipartFormFile  (echotest/context.go L68-68)
```
type MultipartFormFile struct {
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

## Group.StaticFS  (group.go L122-122)
```
func (g *Group) StaticFS(pathPrefix string, filesystem fs.FS, middleware ...MiddlewareFunc) RouteInfo {
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
--- END SOURCE SNIPPETS ---

QUESTION: What are the main relationships among `Echo`, `Group`, `Context`, and handlers during normal request dispatch?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
