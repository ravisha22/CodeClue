# Blind Evaluation Prompt - MRLF v2.1 with File 2 Drill-Down
# Task: blind-echo-mech-1

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

--- CLUE FILE (File 1) ---
=CC v2.1 echo@HEAD 90mod 1272sym
? How does Echo decide which route wins when static segments, parameters, and wildcards overlap?


-- TREE
echotest/  (6 files)
middleware/  (47 files)
bind.go  bind_test.go  binder.go  binder_external_test.go  binder_generic.go  binder_generic_test.go  binder_test.go  context.go  context_generic.go  context_generic_test.go  context_test.go  echo.go  echo_test.go  group.go  group_test.go

-- INDEX
echo.go                                         865L  Config, DefaultHTTPErrorHandler, AcquireContext, Add, AddRoute
context.go                                      667L  Attachment, Bind, Blob, Cookie, Cookies
router.go                                      1074L  Error, Unwrap, AddRouteError, Add, Remove
bind.go                                         472L  BindBody, BindHeaders, BindPathValues, BindQueryParams, BindUnmarshaler
context_test.go                                1428L  BenchmarkAllocJSON, BenchmarkAllocJSONP, BenchmarkAllocXML, BenchmarkContext_Store, BenchmarkRealIPForHeaderXForwardFor
group.go                                        178L  Add, AddRoute, Any, CONNECT, DELETE
bind_test.go                                   1693L  Bar, BenchmarkBindbindDataWithTags, UnmarshalParam, UnmarshalParams, Node
binder.go                                      1329L  Error, BindingError, FormFieldBinder, NewBindingError, PathValuesBinder
binder_external_test.go                         134L  ExampleValueBinder_BindError, ExampleValueBinder_BindErrors, ExampleValueBinder_CustomFunc
binder_generic.go                               571L  TimeOpts, bindValue
binder_generic_test.go                         1616L  UnmarshalJSON, JSONUnmarshalerType, TestFormValue, TestFormValueOr, TestFormValue_UnsupportedType
binder_test.go                                 3252L  BenchmarkDefaultBinder_BindInt64_10_fields, BenchmarkDefaultBinder_BindInt64_single, BenchmarkRawFunc_Int64_single, BenchmarkValueBinder_BindInt64_10_fields, BenchmarkValueBinder_BindInt64_single
context_generic.go                               43L  
context_generic_test.go                          70L  TestContextGetInvalidCast, TestContextGetNonExistentKey, TestContextGetOK, TestContextGetOrInvalidCast, TestContextGetOrNonExistentKey
  ...and 76 more modules

-- SYM
Echo.add                            M echo.go:621    function Echo.add
Echo.AddRoute                       M echo.go:617    AddRoute registers a new Route with default hos...
ValueBinder.intValue                M binder.go:499    function ValueBinder.intValue
ValueBinder.intsValue               M binder.go:541    function ValueBinder.intsValue
Group.Add                           M group.go:158    Add implements `Echo#Add()` for sub-routes with...
Group.AddRoute                      M group.go:172    AddRoute registers a new Routable with Router
Echo.Add                            M echo.go:642    Add registers a new route for an HTTP method an...
Context.writeContentType            M context.go:121    function Context.writeContentType
Context.Get                         M context.go:380    Get retrieves data from the context.
Context.Set                         M context.go:387    Set saves data in the context.
ValueBinder.uintValue               M binder.go:727    function ValueBinder.uintValue
ValueBinder.uintsValue              M binder.go:769    function ValueBinder.uintsValue
ValueBinder.time                    M binder.go:1095   function ValueBinder.time
Context.Blob                        M context.go:552    Blob sends a blob response with status code and...
ValueBinder.floatValue              M binder.go:990    function ValueBinder.floatValue
ValueBinder.floatsValue             M binder.go:1022   function ValueBinder.floatsValue
fsFile                              M context.go:584    function fsFile
BindingError.Error                  M binder.go:87     Error returns error message
ValueBinder.setError                M binder.go:177    function ValueBinder.setError
ValueBinder.Time                    M binder.go:1086   Time binds parameter to time.Time variable
ValueBinder.unixTime                M binder.go:1301   function ValueBinder.unixTime
Context.File                        M context.go:571    File sends a response with the content of the f...
ValueBinder.boolValue               M binder.go:905    function ValueBinder.boolValue
WWWRedirectWithConfig               M middleware/redirect.go:99     WWWRedirectWithConfig returns a WWW redirect mi...
ValueBinder.duration                M binder.go:1167   function ValueBinder.duration
Context.Response                    M context.go:139    Response returns `*Response`.
NewDefaultFS                        M echo.go:804    NewDefaultFS returns a new defaultFS instance w...
bindData                            M bind.go:139    bindData will bind data ONLY fields in destinat...
ValueBinder.bindWithDelimiter       M binder.go:411    function ValueBinder.bindWithDelimiter
ValueBinder.boolsValue              M binder.go:931    function ValueBinder.boolsValue
ValueBinder.customFunc              M binder.go:215    function ValueBinder.customFunc
ValueBinder.durationsValue          M binder.go:1198   function ValueBinder.durationsValue
ValueBinder.times                   M binder.go:1126   function ValueBinder.times
Context.contentDisposition          M context.go:630    function Context.contentDisposition
Context.json                        M context.go:464    function Context.json
Context.xml                         M context.go:517    function Context.xml
ContextConfig.ToContextRecorder     M echotest/context.go:81     ToContextRecorder converts ContextConfig to ech...
ProxyWithConfig                     M middleware/proxy.go:300    ProxyWithConfig returns a Proxy middleware or p...
RequestLoggerConfig.ToMiddleware    M middleware/request_logger.go:246    ToMiddleware converts RequestLoggerConfig into ...
ValueBinder.int                     M binder.go:515    function ValueBinder.int
Echo.File                           M echo.go:609    File registers a new route with path to serve a...
Echo.Use                            M echo.go:431    Use adds middleware to the chain which is run a...
subFS                               M echo.go:827    function subFS
New                                 M echo.go:333    New creates an instance of Echo.
applyMiddleware                     M echo.go:785    function applyMiddleware
newIPChecker                        M ip.go:183    function newIPChecker
Response.Unwrap                     M response.go:105    Unwrap returns the original http.ResponseWriter.
BindPathValues                      M bind.go:42     BindPathValues binds path parameter values to b...
unmarshalInputToField               M bind.go:352    function unmarshalInputToField
ValueBinder.bool                    M binder.go:920    function ValueBinder.bool
ValueBinder.float                   M binder.go:1006   function ValueBinder.float
Context.FormValue                   M context.go:319    FormValue returns the form field value for the ...
Context.IsTLS                       M context.go:150    IsTLS returns true if HTTP connection is TLS ot...
loadBytes                           M echotest/reader.go:36     function loadBytes
Group.GET                           M group.go:37     GET implements `Echo#GET()` for sub-routes with...
Group.StaticFS                      M group.go:122    StaticFS implements `Echo#StaticFS()` for sub-r...
Group                               C group.go:14     Group is a set of sub-routes for a specified ro...
BasicAuthWithConfig                 M middleware/basic_auth.go:92     BasicAuthWithConfig returns an BasicAuthWithCon...
BodyDumpWithConfig                  M middleware/body_dump.go:68     BodyDumpWithConfig returns a BodyDump middlewar...
bodyDumpResponseWriter.Write        M middleware/body_dump.go:150    function bodyDumpResponseWriter.Write
BodyLimitWithConfig                 M middleware/body_limit.go:42     BodyLimitWithConfig returns a BodyLimitWithConf...
GzipWithConfig                      M middleware/compress.go:64     GzipWithConfig returns a middleware which compr...
gzipResponseWriter.WriteHeader      M middleware/compress.go:147    function gzipResponseWriter.WriteHeader
ContextTimeoutWithConfig            M middleware/context_timeout.go:33     ContextTimeoutWithConfig returns a Timeout midd...
CSRFWithConfig                      M middleware/csrf.go:121    CSRFWithConfig returns a CSRF middleware with c...
DecompressWithConfig                M middleware/decompress.go:60     DecompressWithConfig returns a decompress middl...
createExtractors                    M middleware/extractor.go:78     function createExtractors
KeyAuthWithConfig                   M middleware/key_auth.go:133    KeyAuthWithConfig returns an KeyAuth middleware...
MethodOverrideWithConfig            M middleware/method_override.go:41     MethodOverrideWithConfig returns a Method Overr...
Proxy                               M middleware/proxy.go:291    Proxy returns a Proxy middleware.
NewRateLimiterMemoryStoreWithConfig M middleware/rate_limiter.go:203    function NewRateLimiterMemoryStoreWithConfig
RateLimiterWithConfig               M middleware/rate_limiter.go:104    function RateLimiterWithConfig
RecoverWithConfig                   M middleware/recover.go:48     RecoverWithConfig returns a Recovery middleware...
HTTPSRedirectWithConfig             M middleware/redirect.go:57     HTTPSRedirectWithConfig returns a HTTPS redirec...
RequestIDWithConfig                 M middleware/request_id.go:37     RequestIDWithConfig returns a middleware with g...
RequestLoggerWithConfig             M middleware/request_logger.go:237    RequestLoggerWithConfig returns a RequestLogger...
RewriteWithConfig                   M middleware/rewrite.go:48     RewriteWithConfig returns a Rewrite middleware ...
SecureWithConfig                    M middleware/secure.go:96     SecureWithConfig returns a Secure middleware wi...
  ...and 487 more symbols

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

Echo.File (echo.go:609-609)
  File registers a new route with path to serve a static file with optional route-level middleware.
  sig: Echo.File(path, file string, middleware ...MiddlewareFunc)
  called_by: StaticFileHandler

RouteInfo.Reverse (route.go:75-75)
  Reverse reverses route to URL string by replacing path parameters with given params values.
  sig: RouteInfo.Reverse(pathValues ...any)
  behavior: DELEGATE(uri.String -> result); ACCUMULATE(loop -> result)
  called_by: Reverse

Group.StaticFS (group.go:122-122)
  StaticFS implements `Echo#StaticFS()` for sub-routes within the Group.
  sig: Group.StaticFS(pathPrefix string, filesystem fs.FS, middleware ...Middl...)
  behavior: DELEGATE(g.Add -> result)
  calls: Add
  called_by: Static

Echo.Any (echo.go:504-504)
  Any registers a new route for all HTTP methods (supported by Echo) and path with matching handler in the router with opt
  sig: Echo.Any(path string, handler HandlerFunc, middleware ...Middlewa...)
  behavior: DELEGATE(e.Add -> result)
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

Routes.Reverse (route.go:117-117)
  Reverse reverses route to URL string by replacing path parameters with given params values.
  sig: Routes.Reverse(routeName string, pathValues ...any)
  behavior: GUARD(rr -> wrap_Reverse); ACCUMULATE(loop -> result)
  calls: Reverse

Echo (echo.go:68-68)
  Echo is the top-level framework instance.
  methods: AcquireContext, Add, AddRoute, Any, CONNECT, DELETE

Group (group.go:14-14)
  Group is a set of sub-routes for a specified route.
  methods: Add, AddRoute, Any, CONNECT, DELETE, File
  called_by: Group

Echo.Add (echo.go:642-642)
  Add registers a new route for an HTTP method and path with matching handler in the router with optional route-level midd
  sig: Echo.Add(method, path string, handler HandlerFunc, middleware ......)
  calls: add
  called_by: Any, CONNECT, DELETE, GET, HEAD, OPTIONS, PATCH, POST
  raises: panic

New (echo.go:333-333)
  New creates an instance of Echo.
  calls: NewDefaultFS
  called_by: NewWithConfig, main

Echo.GET (echo.go:449-449)
  GET registers a new GET route for a path with matching handler in the router with optional route-level middleware.
  sig: Echo.GET(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(e.Add -> result)
  calls: Add
  called_by: FileFS, main

Group.Add (group.go:158-158)
  Add implements `Echo#Add()` for sub-routes within the Group.
  sig: Group.Add(method, path string, handler HandlerFunc, middleware ......)
  calls: AddRoute
  called_by: Any, CONNECT, DELETE, GET, HEAD, OPTIONS, PATCH, POST
  raises: panic

Echo.Use (echo.go:431-431)
  Use adds middleware to the chain which is run after router has found matching route and before route/request handler met
  sig: Echo.Use(middleware ...MiddlewareFunc)
  called_by: Group, main

DefaultRouter (router.go:60-60)
  DefaultRouter is the registry of all registered routes for an `Echo` instance for request matching and URL path paramete
  methods: Add, Remove, Route, Routes, insert, storeRouteInfo

Echo.Start (echo.go:744-744)
  Start stars HTTP server on given address with Echo as a handler serving requests.
  sig: Echo.Start(address string)
  behavior: DELEGATE(sc.Start -> result); UNWIND(defer)
  called_by: main

DefaultRouter.Add (router.go:447-447)
  Add registers a new route for method and path with matching handler.
  sig: DefaultRouter.Add(route Route)
  behavior: GUARD(route -> RouteInfo); PRECEDENCE(route -> not_r.allowOverwritingRoute); ACCUMULATE(loop -> result)
  calls: Error, AddRouteError, newAddRouteError

Echo.FileFS (echo.go:591-591)
  FileFS registers a new route with path to serve file from the provided file system.
  sig: Echo.FileFS(path, file string, filesystem fs.FS, m ...MiddlewareFunc)
  behavior: DELEGATE(e.GET -> result)
  calls: GET, StaticFileHandler

routeMethods (router.go:148-148)
  type routeMethods
  methods: find, isHandler, set, updateAllowHeader

AddRouteError (router.go:428-428)
  AddRouteError is error returned by Router.Add containing information what actual route adding failed.
  methods: Error, Unwrap
  called_by: Add

routeMethods.isHandler (router.go:301-301)
  called_by: setHandler

routeMethods.set (router.go:171-171)
  sig: routeMethods.set(method string, r *routeMethod)
  behavior: DISPATCH(method)
  called_by: setHandler

RouteInfo (route.go:53-53)
  RouteInfo contains information about registered Route.
  methods: Clone, Reverse

RouteInfo.Clone (route.go:65-65)
  Clone creates copy of RouteInfo
  called_by: Clone

StartConfig (server.go:26-26)
  StartConfig is for creating configured http.Server instance to start serve http(s) requests with given Echo instance
  methods: Start, StartTLS, start

Route (route.go:16-16)
  Route contains information to adding/registering new route with the router.
  methods: ToRouteInfo, WithPrefix

StaticDirectoryHandler (echo.go:559-559)
  StaticDirectoryHandler creates handler function to serve files from provided file system When disablePathUnescaping is s
  sig: StaticDirectoryHandler(fileSystem fs.FS, disablePathUnescaping bool)
  behavior: PRECEDENCE(not_disablePathUnescaping -> err)
  called_by: Static, StaticFS

ContextConfig (echotest/context.go:20-20)
  ContextConfig is configuration for creating echo.Context for testing purposes.
  methods: ServeWithHandler, ToContext, ToContextRecorder

Context.InitializeRoute (context.go:263-263)
  InitializeRoute sets the route related variables of this request to the context.
  sig: Context.InitializeRoute(ri *RouteInfo, pathValues *PathValues)
  calls: PathValues, setPathValues

ContextConfig.ToContextRecorder (echotest/context.go:81-81)
  ToContextRecorder converts ContextConfig to echo.Context and httptest.ResponseRecorder
  sig: ContextConfig.ToContextRecorder(t *testing.T)
  behavior: ACCUMULATE(loop -> conf_RouteInfo_Parameter)
  called_by: ServeWithHandler, ToContext

Echo.AddRoute (echo.go:617-617)
  AddRoute registers a new Route with default host Router
  sig: Echo.AddRoute(route Route)
  behavior: DELEGATE(e.add -> result)
  calls: add
  called_by: Match, add

Echo.add (echo.go:621-621)
  sig: Echo.add(route Route)
  behavior: GUARD(e -> RouteInfo); PRECEDENCE(e -> err)
  calls: AddRoute
  called_by: Add, AddRoute

Group.AddRoute (group.go:172-172)
  AddRoute registers a new Routable with Router
  sig: Group.AddRoute(route Route)
  behavior: DELEGATE(g.echo.add -> result)
  called_by: Add, Match

Group.GET (group.go:37-37)
  GET implements `Echo#GET()` for sub-routes within the Group.
  sig: Group.GET(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(g.Add -> result)
  calls: Add
  called_by: FileFS

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 47 with behavior annotations
drill: echo.go (~1 lines, StaticFileHandler)
drill: context.go (~1 lines, Context.InitializeRoute)
drill: echo.go (~1 lines, NewWithConfig)
drill: middleware/request_logger.go (~1 lines, RequestLogger)
drill: context.go (~1 lines, Context.QueryParams)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## StaticFileHandler  (echo.go L599-599)
```
func StaticFileHandler(file string, filesystem fs.FS) HandlerFunc {
```

## Context.InitializeRoute  (context.go L263-263)
```
func (c *Context) InitializeRoute(ri *RouteInfo, pathValues *PathValues) {
```

## NewWithConfig  (echo.go L294-294)
```
func NewWithConfig(config Config) *Echo {
```

## RequestLogger  (middleware/request_logger.go L395-395)
```
func RequestLogger() echo.MiddlewareFunc {
```

## Context.QueryParams  (context.go L306-306)
```
func (c *Context) QueryParams() url.Values {
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

## StaticDirectoryHandler  (echo.go L559-559)
```
func StaticDirectoryHandler(fileSystem fs.FS, disablePathUnescaping bool) HandlerFunc {
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

## Context.Attachment  (context.go L616-616)
```
func (c *Context) Attachment(file, name string) error {
```

## Context.Bind  (context.go L399-399)
```
func (c *Context) Bind(i any) error {
```

## Context.Blob  (context.go L552-552)
```
func (c *Context) Blob(code int, contentType string, b []byte) (err error) {
```

## Context.Cookie  (context.go L364-364)
```
func (c *Context) Cookie(name string) (*http.Cookie, error) {
```

## Context.Cookies  (context.go L374-374)
```
func (c *Context) Cookies() []*http.Cookie {
```

## Context.Echo  (context.go L665-665)
```
func (c *Context) Echo() *Echo {
```

## Context.File  (context.go L571-571)
```
func (c *Context) File(file string) error {
```

## Context.FileFS  (context.go L580-580)
```
func (c *Context) FileFS(file string, filesystem fs.FS) error {
```

## Context.FormFile  (context.go L348-348)
```
func (c *Context) FormFile(name string) (*multipart.FileHeader, error) {
```
--- END SOURCE SNIPPETS ---

QUESTION: How does Echo decide which route wins when static segments, parameters, and wildcards overlap?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
