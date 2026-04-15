# Blind Evaluation Prompt - MRLF v2.1
# Task: blind-echo-struct-2

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

--- CLUE FILE START ---
=CC v2.1 echo@HEAD 90mod 1272sym
? Which public types and subcomponents make up Echo's routing and request-handling surface?


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
DefaultRouter (router.go:60-60)
  DefaultRouter is the registry of all registered routes for an `Echo` instance for request matching and URL path paramete
  methods: Add, Remove, Route, Routes, insert, storeRouteInfo

HTTPError (httperror.go:107-107)
  HTTPError represents an error that occurred while handling a request.
  methods: Error, StatusCode, Unwrap, Wrap

Router (router.go:21-21)
  Router is interface for routing request contexts to registered routes.

NewVirtualHostHandler (vhost.go:10-10)
  NewVirtualHostHandler creates instance of Echo that routes requests to given virtual hosts when hosts in request does no
  sig: NewVirtualHostHandler(vhosts map[string]*Echo)
  behavior: GUARD(vh -> result)

RequestLogger (middleware/request_logger.go:395-395)
  RequestLogger creates Request Logger middleware with Echo default settings that uses Context.Logger() as logger.
  calls: RequestLoggerWithConfig

ValueBinder (binder.go:92-92)
  ValueBinder provides utility methods for binding query or path parameter to various Go built-in types
  methods: BindError, BindErrors, BindUnmarshaler, BindWithDelimiter, Bool, Bools

Context (context.go:40-40)
  Context represents the context of the current HTTP request.
  methods: Attachment, Bind, Blob, Cookie, Cookies, Echo

Echo (echo.go:68-68)
  Echo is the top-level framework instance.
  methods: AcquireContext, Add, AddRoute, Any, CONNECT, DELETE

New (echo.go:333-333)
  New creates an instance of Echo.
  calls: NewDefaultFS
  called_by: NewWithConfig, main

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

Echo.Start (echo.go:744-744)
  Start stars HTTP server on given address with Echo as a handler serving requests.
  sig: Echo.Start(address string)
  behavior: DELEGATE(sc.Start -> result); UNWIND(defer)
  called_by: main

StartConfig (server.go:26-26)
  StartConfig is for creating configured http.Server instance to start serve http(s) requests with given Echo instance
  methods: Start, StartTLS, start

RequestLoggerConfig.ToMiddleware (middleware/request_logger.go:246-246)
  ToMiddleware converts RequestLoggerConfig into middleware or returns an error for invalid configuration.
  behavior: GUARD(config -> errors.New); PRECEDENCE(config); ACCUMULATE(loop -> result)
  called_by: RequestLoggerWithConfig

RequestLoggerWithConfig (middleware/request_logger.go:237-237)
  RequestLoggerWithConfig returns a RequestLogger middleware with config.
  sig: RequestLoggerWithConfig(config RequestLoggerConfig)
  calls: ToMiddleware
  called_by: RequestLogger
  raises: panic

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

Echo.add (echo.go:621-621)
  sig: Echo.add(route Route)
  behavior: GUARD(e -> RouteInfo); PRECEDENCE(e -> err)
  calls: AddRoute
  called_by: Add, AddRoute

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

AddTrailingSlashConfig (middleware/slash.go:15-15)
  AddTrailingSlashConfig is the middleware config for adding trailing slash to the request.
  methods: ToMiddleware

BindingError (binder.go:69-69)
  BindingError represents an error that occurred while binding request data.
  methods: Error

PathValue (router.go:1051-1051)
  PathValue is tuple pf path parameter name and its value in request path

RemoveTrailingSlashConfig (middleware/slash.go:80-80)
  RemoveTrailingSlashConfig is the middleware config for removing trailing slash from the request.
  methods: ToMiddleware

RequestIDConfig (middleware/request_id.go:11-11)
  RequestIDConfig defines the config for RequestID middleware.
  methods: ToMiddleware

RequestLoggerConfig (middleware/request_logger.go:124-124)
  RequestLoggerConfig is configuration for Request Logger middleware.
  methods: ToMiddleware

RequestLoggerValues (middleware/request_logger.go:189-189)
  RequestLoggerValues contains extracted values from logger.

bindMultipleUnmarshaler (bind.go:37-37)
  bindMultipleUnmarshaler is used by binder to unmarshal multiple values from request at once to type implementing this in

AddTrailingSlash (middleware/slash.go:29-29)
  AddTrailingSlash returns a root level (before router) middleware which adds a trailing slash to the request `URL#Path`.
  behavior: DELEGATE(AddTrailingSlashWithConfig -> result)
  calls: AddTrailingSlashWithConfig

BindBody (bind.go:66-66)
  BindBody binds request body contents to bindable object NB: then binding forms take note that this implementation uses s
  sig: BindBody(c *Context, target any)
  behavior: PRECEDENCE(req -> err -> errors); DISPATCH(mediatype)

CSRF (middleware/csrf.go:116-116)
  CSRF returns a Cross-Site Request Forgery (CSRF) middleware.
  behavior: DELEGATE(CSRFWithConfig -> result)
  calls: CSRFWithConfig

CSRFConfig.checkSecFetchSiteRequest (middleware/csrf.go:260-260)
  sig: CSRFConfig.checkSecFetchSiteRequest(c *echo.Context)
  behavior: GUARD(strings -> isSafe); PRECEDENCE(secFetchSite -> len -> origin); ACCUMULATE(loop -> result)

Context.Bind (context.go:399-399)
  Bind binds path params, query params and the request body into provided type `i`.
  sig: Context.Bind(i any)
  behavior: DELEGATE(c.echo.Binder.Bind -> result)

Context.Cookie (context.go:364-364)
  Cookie returns the named cookie provided in the request.
  sig: Context.Cookie(name string)
  behavior: DELEGATE(c.request.Cookie -> result)
  called_by: SetCookie

Context.Cookies (context.go:374-374)
  Cookies returns the HTTP cookies sent with the request.
  behavior: DELEGATE(c.request.Cookies -> result)

Context.Echo (context.go:665-665)
  Echo returns the `Echo` instance.

Context.Redirect (context.go:642-642)
  Redirect redirects the request to a provided URL with status code.
  sig: Context.Redirect(code int, url string)
  behavior: GUARD(code -> ErrInvalidRedirectCode)

Context.Request (context.go:129-129)
  Request returns `*http.Request`.

Context.Reset (context.go:107-107)
  Reset resets the context after request completes.
  sig: Context.Reset(r *http.Request, w http.ResponseWriter)

Context.RouteInfo (context.go:225-225)
  RouteInfo returns current request route information.
  behavior: GUARD(c -> wrap_Clone)

Context.SetPathValues (context.go:255-255)
  SetPathValues sets path parameters for current request.
  sig: Context.SetPathValues(pathValues PathValues)
  behavior: GUARD(pathValues -> raise_panic)
  raises: panic

Context.SetRequest (context.go:134-134)
  SetRequest sets `*http.Request`.
  sig: Context.SetRequest(r *http.Request)

ContextConfig.ToContext (echotest/context.go:75-75)
  ToContext converts ContextConfig to echo.Context
  sig: ContextConfig.ToContext(t *testing.T)
  calls: ToContextRecorder

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 80 symbols in L3, 46 with behavior annotations

--- CLUE FILE END ---

QUESTION: Which public types and subcomponents make up Echo's routing and request-handling surface?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
