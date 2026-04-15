# Blind Evaluation Prompt - MRLF v2.1 with File 2 Drill-Down
# Task: blind-echo-rel-1

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

--- CLUE FILE (File 1) ---
=CC v2.1 echo@HEAD 90mod 1272sym
? What are the main relationships among `Echo`, `Group`, `Context`, and handlers during normal request dispatch?


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
RequestLogger (middleware/request_logger.go:395-395)
  RequestLogger creates Request Logger middleware with Echo default settings that uses Context.Logger() as logger.
  calls: RequestLoggerWithConfig

Context (context.go:40-40)
  Context represents the context of the current HTTP request.
  methods: Attachment, Bind, Blob, Cookie, Cookies, Echo

Group.Add (group.go:158-158)
  Add implements `Echo#Add()` for sub-routes within the Group.
  sig: Group.Add(method, path string, handler HandlerFunc, middleware ......)
  calls: AddRoute
  called_by: Any, CONNECT, DELETE, GET, HEAD, OPTIONS, PATCH, POST
  raises: panic

DefaultRouter (router.go:60-60)
  DefaultRouter is the registry of all registered routes for an `Echo` instance for request matching and URL path paramete
  methods: Add, Remove, Route, Routes, insert, storeRouteInfo

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

Context.Reset (context.go:107-107)
  Reset resets the context after request completes.
  sig: Context.Reset(r *http.Request, w http.ResponseWriter)

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

Group.Match (group.go:77-77)
  Match implements `Echo#Match()` for sub-routes within the Group.
  sig: Group.Match(methods []string, path string, handler HandlerFunc, midd...)
  behavior: ACCUMULATE(loop -> errs)
  calls: AddRoute

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

Group.Use (group.go:22-22)
  Use implements `Echo#Use()` for sub-routes within the Group.
  sig: Group.Use(middleware ...MiddlewareFunc)

NewVirtualHostHandler (vhost.go:10-10)
  NewVirtualHostHandler creates instance of Echo that routes requests to given virtual hosts when hosts in request does no
  sig: NewVirtualHostHandler(vhosts map[string]*Echo)
  behavior: GUARD(vh -> result)

Echo (echo.go:68-68)
  Echo is the top-level framework instance.
  methods: AcquireContext, Add, AddRoute, Any, CONNECT, DELETE

Group (group.go:14-14)
  Group is a set of sub-routes for a specified route.
  methods: Add, AddRoute, Any, CONNECT, DELETE, File
  called_by: Group

main (echo.go:24-24)
  calls: GET, Start, Use, New

New (echo.go:333-333)
  New creates an instance of Echo.
  calls: NewDefaultFS
  called_by: NewWithConfig, main

Echo.Use (echo.go:431-431)
  Use adds middleware to the chain which is run after router has found matching route and before route/request handler met
  sig: Echo.Use(middleware ...MiddlewareFunc)
  called_by: Group, main

Echo.Start (echo.go:744-744)
  Start stars HTTP server on given address with Echo as a handler serving requests.
  sig: Echo.Start(address string)
  behavior: DELEGATE(sc.Start -> result); UNWIND(defer)
  called_by: main

Context.writeContentType (context.go:121-121)
  sig: Context.writeContentType(value string)
  calls: Get, Set
  called_by: Blob, JSONPBlob, Stream, XMLBlob, json, jsonPBlob, xml

HTTPError (httperror.go:107-107)
  HTTPError represents an error that occurred while handling a request.
  methods: Error, StatusCode, Unwrap, Wrap

Context.json (context.go:464-464)
  sig: Context.json(code int, i any, indent string)
  behavior: DELEGATE(c.echo.JSONSerializer.Serialize -> result); UNWIND(defer)
  calls: Response, SetResponse, writeContentType
  called_by: JSON, JSONPretty

Context.contentDisposition (context.go:630-630)
  sig: Context.contentDisposition(file, name, dispositionType string)
  behavior: DELEGATE(c.File -> result)
  calls: File, Set
  called_by: Attachment, Inline

StartConfig (server.go:26-26)
  StartConfig is for creating configured http.Server instance to start serve http(s) requests with given Echo instance
  methods: Start, StartTLS, start

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 44 with behavior annotations
drill: middleware/request_logger.go (~1 lines, RequestLoggerWithConfig)
drill: context.go (~1 lines, Context.writeContentType)
drill: context.go (~1 lines, Context.InitializeRoute)
drill: middleware/request_logger.go (~1 lines, RequestLogger)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## RequestLoggerWithConfig  (middleware/request_logger.go L237-237)
```
func RequestLoggerWithConfig(config RequestLoggerConfig) echo.MiddlewareFunc {
```

## Context.writeContentType  (context.go L121-121)
```
func (c *Context) writeContentType(value string) {
```

## Context.InitializeRoute  (context.go L263-263)
```
func (c *Context) InitializeRoute(ri *RouteInfo, pathValues *PathValues) {
```

## RequestLogger  (middleware/request_logger.go L395-395)
```
func RequestLogger() echo.MiddlewareFunc {
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

## Context.FormValue  (context.go L319-319)
```
func (c *Context) FormValue(name string) string {
```

## Context.FormValueOr  (context.go L325-325)
```
func (c *Context) FormValueOr(name, defaultValue string) string {
```

## Context.FormValues  (context.go L334-334)
```
func (c *Context) FormValues() (url.Values, error) {
```

## Context.Get  (context.go L380-380)
```
func (c *Context) Get(key string) any {
```

## Context.HTML  (context.go L435-435)
```
func (c *Context) HTML(code int, html string) (err error) {
```

## Context.HTMLBlob  (context.go L440-440)
```
func (c *Context) HTMLBlob(code int, b []byte) (err error) {
```

## Context.Inline  (context.go L624-624)
```
func (c *Context) Inline(file, name string) error {
```

## Context.IsTLS  (context.go L150-150)
```
func (c *Context) IsTLS() bool {
```

## Context.IsWebSocket  (context.go L155-155)
```
func (c *Context) IsWebSocket() bool {
```

## Context.JSON  (context.go L482-482)
```
func (c *Context) JSON(code int, i any) (err error) {
```

## Context.JSONBlob  (context.go L492-492)
```
func (c *Context) JSONBlob(code int, b []byte) (err error) {
```

## Context.JSONP  (context.go L498-498)
```
func (c *Context) JSONP(code int, callback string, i any) (err error) {
```

## Context.JSONPBlob  (context.go L504-504)
```
func (c *Context) JSONPBlob(code int, callback string, b []byte) (err error) {
```

## Context.JSONPretty  (context.go L487-487)
```
func (c *Context) JSONPretty(code int, i any, indent string) (err error) {
```

## Context.Logger  (context.go L652-652)
```
func (c *Context) Logger() *slog.Logger {
```

## Context.MultipartForm  (context.go L358-358)
```
func (c *Context) MultipartForm() (*multipart.Form, error) {
```

## Context.NoContent  (context.go L636-636)
```
func (c *Context) NoContent(code int) error {
```

## Context.Param  (context.go L233-233)
```
func (c *Context) Param(name string) string {
```

## Context.ParamOr  (context.go L245-245)
```
func (c *Context) ParamOr(name, defaultValue string) string {
```

## Context.Path  (context.go L210-210)
```
func (c *Context) Path() string {
```

## Context.PathValues  (context.go L250-250)
```
func (c *Context) PathValues() PathValues {
```

## Context.QueryParam  (context.go L287-287)
```
func (c *Context) QueryParam(name string) string {
```

## Context.QueryParamOr  (context.go L297-297)
```
func (c *Context) QueryParamOr(name, defaultValue string) string {
```

## Context.QueryParams  (context.go L306-306)
```
func (c *Context) QueryParams() url.Values {
```

## Context.QueryString  (context.go L314-314)
```
func (c *Context) QueryString() string {
```

## Context.RealIP  (context.go L199-199)
```
func (c *Context) RealIP() string {
```

## Context.Redirect  (context.go L642-642)
```
func (c *Context) Redirect(code int, url string) error {
```

## Context.Render  (context.go L414-414)
```
func (c *Context) Render(code int, name string, data any) (err error) {
```

## Context.Request  (context.go L129-129)
```
func (c *Context) Request() *http.Request {
```

## Context.Reset  (context.go L107-107)
```
func (c *Context) Reset(r *http.Request, w http.ResponseWriter) {
```

## Context.Response  (context.go L139-139)
```
func (c *Context) Response() http.ResponseWriter {
```

## Context.RouteInfo  (context.go L225-225)
```
func (c *Context) RouteInfo() RouteInfo {
```

## Context.Scheme  (context.go L162-162)
```
func (c *Context) Scheme() string {
```

## Context.Set  (context.go L387-387)
```
func (c *Context) Set(key string, val any) {
```

## Context.SetCookie  (context.go L369-369)
```
func (c *Context) SetCookie(cookie *http.Cookie) {
```

## Context.SetLogger  (context.go L660-660)
```
func (c *Context) SetLogger(logger *slog.Logger) {
```

## Context.SetPath  (context.go L215-215)
```
func (c *Context) SetPath(p string) {
```

## Context.SetPathValues  (context.go L255-255)
```
func (c *Context) SetPathValues(pathValues PathValues) {
```

## Context.SetRequest  (context.go L134-134)
```
func (c *Context) SetRequest(r *http.Request) {
```

## Context.SetResponse  (context.go L145-145)
```
func (c *Context) SetResponse(r http.ResponseWriter) {
```

## Context.Stream  (context.go L560-560)
```
func (c *Context) Stream(code int, contentType string, r io.Reader) (err error) {
```

## Context.String  (context.go L445-445)
```
func (c *Context) String(code int, s string) (err error) {
```

## Context.Validate  (context.go L405-405)
```
func (c *Context) Validate(i any) error {
```

## Context.XML  (context.go L531-531)
```
func (c *Context) XML(code int, i any) (err error) {
```

## Context.XMLBlob  (context.go L541-541)
```
func (c *Context) XMLBlob(code int, b []byte) (err error) {
```

## Context.XMLPretty  (context.go L536-536)
```
func (c *Context) XMLPretty(code int, i any, indent string) (err error) {
```

## Context.contentDisposition  (context.go L630-630)
```
func (c *Context) contentDisposition(file, name, dispositionType string) error {
```

## Context.json  (context.go L464-464)
```
func (c *Context) json(code int, i any, indent string) error {
```

## Context.jsonPBlob  (context.go L449-449)
```
func (c *Context) jsonPBlob(code int, callback string, i any) (err error) {
```

## Context.setPathValues  (context.go L269-269)
```
func (c *Context) setPathValues(pv *PathValues) {
```

## Context.xml  (context.go L517-517)
```
func (c *Context) xml(code int, i any, indent string) (err error) {
```
--- END SOURCE SNIPPETS ---

QUESTION: What are the main relationships among `Echo`, `Group`, `Context`, and handlers during normal request dispatch?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
