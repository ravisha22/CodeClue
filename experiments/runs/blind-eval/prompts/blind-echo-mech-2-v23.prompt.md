# Blind Evaluation Prompt - MRLF v2.1 with File 2 Drill-Down
# Task: blind-echo-mech-2

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

--- CLUE FILE (File 1) ---
=CC v2.1 echo@HEAD 44mod 565sym
? What happens inside Echo's centralized HTTP error path when handlers return ordinary errors, HTTP errors, or errors after the response is already committed?


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
Echo.Any (echo.go:504-504)
  Any registers a new route for all HTTP methods (supported by Echo) and path with matching handler in the router with opt
  sig: Echo.Any(path string, handler HandlerFunc, middleware ...Middlewa...)
  behavior: DELEGATE(e.Add -> result)
  calls: Add

UnwrapResponse (response.go:120-120)
  UnwrapResponse unwraps given ResponseWriter to return contexts original Echo Response.
  sig: UnwrapResponse(rw http.ResponseWriter)
  behavior: ACCUMULATE(loop -> result)
  calls: Unwrap

HTTPStatusCoder (httperror.go:39-39)
  HTTPStatusCoder is interface that errors can implement to produce status code for HTTP response

MiddlewareConfigurator (echo.go:121-121)
  MiddlewareConfigurator defines interface for creating middleware handlers with possibility to return configuration error

ResolveResponseStatus (httperror.go:66-66)
  ResolveResponseStatus returns the Response and HTTP status code that should be (or has been) sent for rw, given an optio
  sig: ResolveResponseStatus(rw http.ResponseWriter, err error)
  behavior: GUARD(resp != nil && resp.Committed -> return resp, http.S...); PRECEDENCE(resp -> err)
  calls: StatusCode

httpError.Error (httperror.go:152-152)
  behavior: DELEGATE(http.StatusText -> result)

Response.WriteHeader (response.go:49-49)
  WriteHeader sends an HTTP response header with status code.
  sig: Response.WriteHeader(code int)
  behavior: GUARD(r.Committed -> return); ACCUMULATE(fn loop -> result)
  called_by: Write, WriteHeader

ValueBinder.BindError (binder.go:186-186)
  BindError returns first seen bind error and resets/empties binder errors for further calls
  behavior: GUARD(b.errors == nil -> return nil)

isIgnorableOpenFileError (middleware/static_other.go:13-13)
  We ignore these errors as there could be handler that matches request path.
  sig: isIgnorableOpenFileError(err error)
  behavior: GUARD(os.IsNotExist(err) -> return true); PRECEDENCE(os -> errors)

httpError (httperror.go:144-144)
  type httpError
  methods: Error, StatusCode, Wrap

httpError.StatusCode (httperror.go:148-148)

httpError.Wrap (httperror.go:156-156)
  sig: httpError.Wrap(err error)

Echo.Add (echo.go:642-642)
  Add registers a new route for an HTTP method and path with matching handler in the router with optional route-level midd
  sig: Echo.Add(method, path string, handler HandlerFunc, middleware ......)
  behavior: GUARD(err != nil -> panic(err))
  calls: add
  called_by: Any, CONNECT, DELETE, File, GET, HEAD, OPTIONS, PATCH
  raises: panic

Response (response.go:18-18)
  Response wraps an http.ResponseWriter and implements its interface to be used by an HTTP handler to construct an HTTP re
  methods: After, Before, Flush, Hijack, Unwrap, Write

Response.Unwrap (response.go:105-105)
  Unwrap returns the original http.ResponseWriter.
  called_by: UnwrapResponse

Context.SetResponse (context.go:145-145)
  SetResponse sets `*http.ResponseWriter`.
  sig: Context.SetResponse(r http.ResponseWriter)
  called_by: json

Echo.Match (echo.go:510-510)
  Match registers a new route for multiple HTTP methods and path with matching handler in the router with optional route-l
  sig: Echo.Match(methods []string, path string, handler HandlerFunc, midd...)
  behavior: GUARD(len(errs) > 0 -> panic(errs)); ACCUMULATE(AddRoute loop -> errs)
  calls: AddRoute
  raises: panic

Echo.Start (echo.go:744-744)
  Start stars HTTP server on given address with Echo as a handler serving requests.
  sig: Echo.Start(address string)
  behavior: DELEGATE(sc.Start -> result); UNWIND(defer)
  called_by: main

ValueExtractorError.Error (middleware/extractor.go:42-42)
  Error returns errors text

DefaultHTTPErrorHandler (echo.go:374-374)
  DefaultHTTPErrorHandler creates new default HTTP error handler implementation.
  sig: DefaultHTTPErrorHandler(exposeError bool)
  called_by: New

HTTPError.StatusCode (httperror.go:115-115)
  StatusCode returns status code for HTTP response

HTTPError.Wrap (httperror.go:132-132)
  Wrap eturns new HTTPError with given errors wrapped inside
  sig: HTTPError.Wrap(err error)

WrapHandler (echo.go:752-752)
  WrapHandler wraps `http.Handler` into `echo.HandlerFunc`.
  sig: WrapHandler(h http.Handler)
  calls: ServeHTTP

WrapMiddleware (echo.go:766-766)
  WrapMiddleware wraps `func(http.Handler) http.Handler` into `echo.MiddlewareFunc`
  sig: WrapMiddleware(m func(http.Handler)
  calls: ServeHTTP

delayedStatusWriter (response.go:136-136)
  delayedStatusWriter is a wrapper around http.ResponseWriter that delays writing the status code until first Write is cal
  methods: Flush, Hijack, Unwrap, Write, WriteHeader

Context.HTMLBlob (context.go:440-440)
  HTMLBlob sends an HTTP blob response with status code.
  sig: Context.HTMLBlob(code int, b []byte)
  behavior: DELEGATE(c.Blob -> result)
  calls: Blob
  called_by: HTML, Render

ContextConfig.ToContextRecorder (echotest/context.go:81-81)
  ToContextRecorder converts ContextConfig to echo.Context and httptest.ResponseRecorder
  sig: ContextConfig.ToContextRecorder(t *testing.T)
  called_by: ServeWithHandler, ToContext

Context.HTML (context.go:435-435)
  HTML sends an HTTP response with status code.
  sig: Context.HTML(code int, html string)
  behavior: DELEGATE(c.HTMLBlob -> result)
  calls: HTMLBlob

Context.SetCookie (context.go:369-369)
  SetCookie adds a `Set-Cookie` header in HTTP response.
  sig: Context.SetCookie(cookie *http.Cookie)
  calls: Response

DefaultRouter (router.go:60-60)
  DefaultRouter is the registry of all registered routes for an `Echo` instance for request matching and URL path paramete
  methods: Add, Remove, Route, Routes, insert, storeRouteInfo

StartConfig (server.go:26-26)
  StartConfig is for creating configured http.Server instance to start serve http(s) requests with given Echo instance
  methods: Start, StartTLS, start

Gzip (middleware/compress.go:59-59)
  Gzip returns a middleware which compresses HTTP response using gzip compression scheme.
  behavior: DELEGATE(GzipWithConfig -> result)
  calls: GzipWithConfig

GzipWithConfig (middleware/compress.go:64-64)
  GzipWithConfig returns a middleware which compresses HTTP response using gzip compression scheme.
  sig: GzipWithConfig(config GzipConfig)
  behavior: DELEGATE(toMiddlewareOrPanic -> result)
  called_by: Gzip

gzipResponseWriter.Push (middleware/compress.go:209-209)
  sig: gzipResponseWriter.Push(target string, opts *http.PushOptions)
  behavior: GUARD(p, ok := w.ResponseWriter.(http.Pusher); ok -> return p.Push(targe...)

Echo.serveHTTP (echo.go:700-700)
  serveHTTP implements `http.Handler` interface, which serves HTTP requests.
  sig: Echo.serveHTTP(w http.ResponseWriter, r *http.Request)
  behavior: GUARD(e.premiddleware == nil -> return h1(cc)); DELEGATE(h1 -> result); UNWIND(defer)
  calls: applyMiddleware

Response.Flush (response.go:81-81)
  Flush implements the http.Flusher interface to allow an HTTP handler to flush buffered data to the client.
  behavior: GUARD(err != nil && errors.Is(err, http.ErrNotSuppo... -> panic(fmt.Errorf("...)
  called_by: Flush
  raises: panic

Response.Hijack (response.go:92-92)
  Hijack implements the http.Hijacker interface to allow an HTTP handler to take over the connection.
  behavior: DELEGATE(http.NewResponseController -> result)
  called_by: Hijack

ValueBinder.BindErrors (binder.go:196-196)
  BindErrors returns all bind errors and resets/empties binder errors for further calls
  behavior: GUARD(b.errors == nil -> return nil)

ValueBinder.setError (binder.go:177-177)
  sig: ValueBinder.setError(err error)
  behavior: GUARD(b.errors == nil -> return)
  called_by: BindUnmarshaler, JSONUnmarshaler, MustBindUnmarshaler, MustJSONUnmarshaler, MustString, MustStrings, MustTextUnmarshaler, TextUnmarshaler

bodyDumpResponseWriter.Flush (middleware/body_dump.go:154-154)
  behavior: GUARD(err != nil && errors.Is(err, http.ErrNotSuppo... -> panic(errors.New("...)
  raises: panic

bodyDumpResponseWriter.Hijack (middleware/body_dump.go:161-161)
  behavior: DELEGATE(http.NewResponseController -> result)

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 189 symbols in L3, 115 with behavior annotations
uncovered: Echo.AddRoute, Echo.RouteNotFound, Echo.Use, Echo.AcquireContext
drill: response.go (~1 lines, UnwrapResponse)
drill: echo.go (~1 lines, Echo.Any)
drill: httperror.go (~1 lines, httpError.StatusCode)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## UnwrapResponse  (response.go L120-120)
```
func UnwrapResponse(rw http.ResponseWriter) (*Response, error) {
```

## Echo.Any  (echo.go L504-504)
```
func (e *Echo) Any(path string, handler HandlerFunc, middleware ...MiddlewareFunc) RouteInfo {
```

## httpError.StatusCode  (httperror.go L148-148)
```
func (he httpError) StatusCode() int {
```

## NewResponse  (response.go L31-31)
```
func NewResponse(w http.ResponseWriter, logger *slog.Logger) (r *Response) {
```

## Response.After  (response.go L41-41)
```
func (r *Response) After(fn func()) {
```

## Response.Before  (response.go L36-36)
```
func (r *Response) Before(fn func()) {
```

## Response.Flush  (response.go L81-81)
```
func (r *Response) Flush() {
```

## Response.Hijack  (response.go L92-92)
```
func (r *Response) Hijack() (net.Conn, *bufio.ReadWriter, error) {
```

## Response.Unwrap  (response.go L105-105)
```
func (r *Response) Unwrap() http.ResponseWriter {
```

## Response.Write  (response.go L63-63)
```
func (r *Response) Write(b []byte) (n int, err error) {
```

## Response.WriteHeader  (response.go L49-49)
```
func (r *Response) WriteHeader(code int) {
```

## Response.reset  (response.go L109-109)
```
func (r *Response) reset(w http.ResponseWriter) {
```

## Response  (response.go L18-18)
```
type Response struct {
```

## delayedStatusWriter.Flush  (response.go L159-159)
```
func (w *delayedStatusWriter) Flush() {
```

## delayedStatusWriter.Hijack  (response.go L166-166)
```
func (w *delayedStatusWriter) Hijack() (net.Conn, *bufio.ReadWriter, error) {
```

## delayedStatusWriter.Unwrap  (response.go L170-170)
```
func (w *delayedStatusWriter) Unwrap() http.ResponseWriter {
```

## delayedStatusWriter.Write  (response.go L148-148)
```
func (w *delayedStatusWriter) Write(data []byte) (int, error) {
```

## delayedStatusWriter.WriteHeader  (response.go L142-142)
```
func (w *delayedStatusWriter) WriteHeader(statusCode int) {
```

## delayedStatusWriter  (response.go L136-136)
```
type delayedStatusWriter struct {
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

## HTTPError.Error  (httperror.go L120-120)
```
func (he *HTTPError) Error() string {
```

## HTTPError.StatusCode  (httperror.go L115-115)
```
func (he *HTTPError) StatusCode() int {
```

## HTTPError.Unwrap  (httperror.go L140-140)
```
func (he *HTTPError) Unwrap() error {
```

## HTTPError.Wrap  (httperror.go L132-132)
```
func (he HTTPError) Wrap(err error) error {
```

## HTTPError  (httperror.go L107-107)
```
type HTTPError struct {
```

## HTTPStatusCoder  (httperror.go L39-39)
```
type HTTPStatusCoder interface {
```

## NewHTTPError  (httperror.go L99-99)
```
func NewHTTPError(code int, message string) *HTTPError {
```

## ResolveResponseStatus  (httperror.go L66-66)
```
func ResolveResponseStatus(rw http.ResponseWriter, err error) (resp *Response, status int) {
```

## StatusCode  (httperror.go L45-45)
```
func StatusCode(err error) int {
```

## httpError.Error  (httperror.go L152-152)
```
func (he httpError) Error() string {
```

## httpError.Wrap  (httperror.go L156-156)
```
func (he httpError) Wrap(err error) error {
```

## httpError  (httperror.go L144-144)
```
type httpError struct {
```
--- END SOURCE SNIPPETS ---

QUESTION: What happens inside Echo's centralized HTTP error path when handlers return ordinary errors, HTTP errors, or errors after the response is already committed?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
