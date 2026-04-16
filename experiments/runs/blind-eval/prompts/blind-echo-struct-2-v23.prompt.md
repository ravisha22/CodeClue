# Blind Evaluation Prompt - MRLF v2.1
# Task: blind-echo-struct-2

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

--- CLUE FILE START ---
=CC v2.1 echo@HEAD 44mod 565sym
? Which public types and subcomponents make up Echo's routing and request-handling surface?


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

RequestID (middleware/request_id.go:30-30)
  RequestID returns a middleware that reads RequestIDConfig.TargetHeader (`X-Request-ID`) header value or when the header 
  behavior: DELEGATE(RequestIDWithConfig -> result)
  calls: RequestIDWithConfig

Echo (echo.go:68-68)
  Echo is the top-level framework instance.
  methods: AcquireContext, Add, AddRoute, Any, CONNECT, DELETE

RequestLoggerWithConfig (middleware/request_logger.go:237-237)
  RequestLoggerWithConfig returns a RequestLogger middleware with config.
  sig: RequestLoggerWithConfig(config RequestLoggerConfig)
  behavior: GUARD(err != nil -> panic(err))
  calls: ToMiddleware
  called_by: RequestLogger
  raises: panic

RequestLoggerConfig.ToMiddleware (middleware/request_logger.go:246-246)
  ToMiddleware converts RequestLoggerConfig into middleware or returns an error for invalid configuration.
  behavior: PRECEDENCE(config); ACCUMULATE(CanonicalHeaderKey loop -> result)
  called_by: RequestLoggerWithConfig

RequestIDWithConfig (middleware/request_id.go:37-37)
  RequestIDWithConfig returns a middleware with given valid config or panics on invalid configuration.
  sig: RequestIDWithConfig(config RequestIDConfig)
  behavior: DELEGATE(toMiddlewareOrPanic -> result)
  called_by: RequestID

Context.SetRequest (context.go:134-134)
  SetRequest sets `*http.Request`.
  sig: Context.SetRequest(r *http.Request)
  called_by: newContext

Echo.Use (echo.go:431-431)
  Use adds middleware to the chain which is run after router has found matching route and before route/request handler met
  sig: Echo.Use(middleware ...MiddlewareFunc)
  called_by: Group, main

Echo.Start (echo.go:744-744)
  Start stars HTTP server on given address with Echo as a handler serving requests.
  sig: Echo.Start(address string)
  behavior: DELEGATE(sc.Start -> result); UNWIND(defer)
  called_by: main

Context.Request (context.go:129-129)
  Request returns `*http.Request`.
  called_by: fsFile

Echo.add (echo.go:621-621)
  sig: Echo.add(route Route)
  behavior: GUARD(e.OnAddRoute != nil -> return RouteInfo{},...); PRECEDENCE(e -> err -> paramsCount)
  calls: Add
  called_by: Add, AddRoute

RequestIDConfig (middleware/request_id.go:11-11)
  RequestIDConfig defines the config for RequestID middleware.
  methods: ToMiddleware

RequestLoggerConfig (middleware/request_logger.go:124-124)
  RequestLoggerConfig is configuration for Request Logger middleware.
  methods: ToMiddleware

Context.Echo (context.go:665-665)
  Echo returns the `Echo` instance.

Echo.Any (echo.go:504-504)
  Any registers a new route for all HTTP methods (supported by Echo) and path with matching handler in the router with opt
  sig: Echo.Any(path string, handler HandlerFunc, middleware ...Middlewa...)
  behavior: DELEGATE(e.Add -> result)
  calls: Add

RequestIDConfig.ToMiddleware (middleware/request_id.go:42-42)
  ToMiddleware converts RequestIDConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)

RequestLoggerValues (middleware/request_logger.go:189-189)
  RequestLoggerValues contains extracted values from logger.

CSRFConfig.checkSecFetchSiteRequest (middleware/csrf.go:260-260)
  sig: CSRFConfig.checkSecFetchSiteRequest(c *echo.Context)
  behavior: GUARD(secFetchSite == "" -> return false, nil); PRECEDENCE(secFetchSite -> len -> not_isSafe)
  called_by: ToMiddleware

setMultipartFileHeaderTypes (bind.go:449-449)
  sig: setMultipartFileHeaderTypes(structField reflect.Value, inputFieldName string, files ...)
  behavior: GUARD(len(fileHeaders) == 0 -> return false); DISPATCH(structField)
  called_by: bindData

Group.Match (group.go:77-77)
  Match implements `Echo#Match()` for sub-routes within the Group.
  sig: Group.Match(methods []string, path string, handler HandlerFunc, midd...)
  behavior: GUARD(len(errs) > 0 -> panic(errs)); ACCUMULATE(AddRoute loop -> errs)
  calls: AddRoute
  raises: panic

New (echo.go:333-333)
  New creates an instance of Echo.
  calls: DefaultHTTPErrorHandler, NewDefaultFS
  called_by: NewWithConfig, main

NewWithConfig (echo.go:294-294)
  NewWithConfig creates an instance of Echo with given configuration.
  sig: NewWithConfig(config Config)
  calls: New

WrapHandler (echo.go:752-752)
  WrapHandler wraps `http.Handler` into `echo.HandlerFunc`.
  sig: WrapHandler(h http.Handler)
  calls: ServeHTTP

WrapMiddleware (echo.go:766-766)
  WrapMiddleware wraps `func(http.Handler) http.Handler` into `echo.MiddlewareFunc`
  sig: WrapMiddleware(m func(http.Handler)
  calls: ServeHTTP

Context.Bind (context.go:399-399)
  Bind binds path params, query params and the request body into provided type `i`.
  sig: Context.Bind(i any)
  behavior: DELEGATE(c.echo.Binder.Bind -> result)

Context.Cookie (context.go:364-364)
  Cookie returns the named cookie provided in the request.
  sig: Context.Cookie(name string)
  behavior: DELEGATE(c.request.Cookie -> result)

Context.Cookies (context.go:374-374)
  Cookies returns the HTTP cookies sent with the request.
  behavior: DELEGATE(c.request.Cookies -> result)

DefaultJSONSerializer.Deserialize (json.go:24-24)
  Deserialize reads a JSON from a request body and converts it into an interface.
  sig: DefaultJSONSerializer.Deserialize(c *Context, target any)
  behavior: GUARD(err := json.NewDecoder(c.Request().Body).Deco... -> return ErrBadReque...)

Group.Add (group.go:158-158)
  Add implements `Echo#Add()` for sub-routes within the Group.
  sig: Group.Add(method, path string, handler HandlerFunc, middleware ......)
  behavior: GUARD(err != nil -> panic(err))
  calls: AddRoute
  called_by: Any, CONNECT, DELETE, File, GET, HEAD, OPTIONS, PATCH
  raises: panic

Context (context.go:40-40)
  Context represents the context of the current HTTP request.
  methods: Attachment, Bind, Blob, Cookie, Cookies, Echo

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

ContextConfig.ToContextRecorder (echotest/context.go:81-81)
  ToContextRecorder converts ContextConfig to echo.Context and httptest.ResponseRecorder
  sig: ContextConfig.ToContextRecorder(t *testing.T)
  called_by: ServeWithHandler, ToContext

ContextConfig.ToContext (echotest/context.go:75-75)
  ToContext converts ContextConfig to echo.Context
  sig: ContextConfig.ToContext(t *testing.T)
  calls: ToContextRecorder

ContextConfig (echotest/context.go:20-20)
  ContextConfig is configuration for creating echo.Context for testing purposes.
  methods: ServeWithHandler, ToContext, ToContextRecorder

Group.Any (group.go:72-72)
  Any implements `Echo#Any()` for sub-routes within the Group.
  sig: Group.Any(path string, handler HandlerFunc, middleware ...Middlewa...)
  behavior: DELEGATE(g.Add -> result)
  calls: Add

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 80 symbols in L3, 44 with behavior annotations
uncovered: Echo.DELETE, Echo.File, Echo.HEAD, Echo.Match

--- CLUE FILE END ---

QUESTION: Which public types and subcomponents make up Echo's routing and request-handling surface?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
