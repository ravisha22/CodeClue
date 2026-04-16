# Blind Evaluation Prompt - MRLF v2.4
# Task: blind-echo-struct-2

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 echo@HEAD 44mod 565sym
? Which public types and subcomponents make up Echo's routing and request-handling surface?


-- TREE
echotest/  (2 files)
middleware/  (24 files)
bind.go  binder.go  binder_generic.go  context.go  context_generic.go  echo.go  group.go  httperror.go  ip.go  json.go  renderer.go  response.go  route.go  router.go  router_concurrent.go

-- INDEX
router.go                                      1074L  Error, Unwrap, AddRouteError, Add, Remove
echo.go                                         865L  Config, DefaultHTTPErrorHandler, AcquireContext, Add, AddRoute
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
Context.writeContentType            M context.go:121    function Context.writeContentType
Context.Request                     M context.go:129    Request returns `*http.Request`.
Context.Get                         M context.go:380    Get retrieves data from the context.
ValueBinder.uintValue               M binder.go:727    function ValueBinder.uintValue
Context.Set                         M context.go:387    Set saves data in the context.
ValueBinder.uint                    M binder.go:743    function ValueBinder.uint
ValueBinder.int                     M binder.go:515    function ValueBinder.int
ValueBinder.intValue                M binder.go:499    function ValueBinder.intValue
ValueBinder.intsValue               M binder.go:541    function ValueBinder.intsValue
ValueBinder.uintsValue              M binder.go:769    function ValueBinder.uintsValue
Context.Blob                        M context.go:552    Blob sends a blob response with status code and...
Group.Add                           M group.go:158    Add implements `Echo#Add()` for sub-routes with...
DefaultRouter.Add                   M router.go:447    Add registers a new route for method and path w...
concurrentRouter.Add                M router_concurrent.go:35     function concurrentRouter.Add
Context.Response                    M context.go:139    Response returns `*Response`.
ValueBinder.unixTime                M binder.go:1301   function ValueBinder.unixTime
ValueBinder.float                   M binder.go:1006   function ValueBinder.float
Context.String                      M context.go:445    String sends a string response with status code.
ValueBinder.ints                    M binder.go:556    function ValueBinder.ints
ValueBinder.uints                   M binder.go:784    function ValueBinder.uints
Echo.AddRoute                       M echo.go:617    AddRoute registers a new Route with default hos...
Group.AddRoute                      M group.go:172    AddRoute registers a new Routable with Router
DefaultRouter.insert                M router.go:548    function DefaultRouter.insert
ValueBinder.floatValue              M binder.go:990    function ValueBinder.floatValue
ValueBinder.floatsValue             M binder.go:1022   function ValueBinder.floatsValue
ValueBinder.String                  M binder.go:234    String binds parameter to string variable
ValueBinder.bool                    M binder.go:920    function ValueBinder.bool
Context.QueryParams                 M context.go:306    QueryParams returns the query parameters as `ur...
fsFile                              M context.go:584    function fsFile
node.setHandler                     M router.go:731    function node.setHandler
Response.WriteHeader                M response.go:49     WriteHeader sends an HTTP response header with ...
ValueBinder.floats                  M binder.go:1037   function ValueBinder.floats
Context.setPathValues               M context.go:269    function Context.setPathValues
routeMethods.updateAllowHeader      M router.go:251    function routeMethods.updateAllowHeader
StartConfig.start                   M server.go:100    start starts handler with HTTP(s) server.
Context.PathValues                  M context.go:250    PathValues returns path parameter values.
limitedReader.Close                 M middleware/body_limit.go:92     function limitedReader.Close
limitedGzipReader.Close             M middleware/decompress.go:153    function limitedGzipReader.Close
Context.SetRequest                  M context.go:134    SetRequest sets `*http.Request`.
gzipResponseWriter.WriteHeader      M middleware/compress.go:147    function gzipResponseWriter.WriteHeader
bindData                            M bind.go:139    bindData will bind data ONLY fields in destinat...
Context.json                        M context.go:464    function Context.json
ValueBinder.bindWithDelimiter       M binder.go:411    function ValueBinder.bindWithDelimiter
ValueBinder.boolValue               M binder.go:905    function ValueBinder.boolValue
ValueBinder.boolsValue              M binder.go:931    function ValueBinder.boolsValue
ValueBinder.customFunc              M binder.go:215    function ValueBinder.customFunc
ValueBinder.duration                M binder.go:1167   function ValueBinder.duration
ValueBinder.durationsValue          M binder.go:1198   function ValueBinder.durationsValue
ValueBinder.time                    M binder.go:1095   function ValueBinder.time
ValueBinder.times                   M binder.go:1126   function ValueBinder.times
Context.FormValue                   M context.go:319    FormValue returns the form field value for the ...
Context.HTMLBlob                    M context.go:440    HTMLBlob sends an HTTP blob response with statu...
Context.QueryParam                  M context.go:287    QueryParam returns the query param for the prov...
Context.contentDisposition          M context.go:630    function Context.contentDisposition
Context.xml                         M context.go:517    function Context.xml
ContextConfig.ToContextRecorder     M echotest/context.go:81     ToContextRecorder converts ContextConfig to ech...
RateLimiterMemoryStore.cleanupStaleVisitors M middleware/rate_limiter.go:256    function RateLimiterMemoryStore.cleanupStaleVis...
node.findStaticChild                M router.go:709    function node.findStaticChild
Context.SetResponse                 M context.go:145    SetResponse sets `*http.ResponseWriter`.
bodyDumpResponseWriter.Write        M middleware/body_dump.go:150    function bodyDumpResponseWriter.Write
ValueBinder.bools                   M binder.go:946    function ValueBinder.bools
ValueBinder.durations               M binder.go:1213   function ValueBinder.durations
routeMethods.isHandler              M router.go:301    function routeMethods.isHandler
routeMethods.set                    M router.go:171    function routeMethods.set
newAddRouteError                    M router.go:438    function newAddRouteError
node.addStaticChild                 M router.go:705    function node.addStaticChild
RequestLoggerConfig.ToMiddleware    M middleware/request_logger.go:246    ToMiddleware converts RequestLoggerConfig into ...
Response.Flush                      M response.go:81     Flush implements the http.Flusher interface to ...
Context.Param                       M context.go:233    Param returns path parameter by name.
Context.Cookies                     M context.go:374    Cookies returns the HTTP cookies sent with the ...
Context.File                        M context.go:571    File sends a response with the content of the f...
StartConfig.Start                   M server.go:64     Start starts given Handler with HTTP(s) server.
subFS                               M echo.go:827    function subFS
HTTPError.StatusCode                M httperror.go:115    StatusCode returns status code for HTTP response
httpError.StatusCode                M httperror.go:148    function httpError.StatusCode
New                                 M echo.go:333    New creates an instance of Echo.
Context.Redirect                    M context.go:642    Redirect redirects the request to a provided UR...
PathValues.Get                      M router.go:1057   Get returns path parameter value for given name...
Response.Write                      M response.go:63     Write writes the data to the connection as part...
format                              M middleware/static.go:341    format formats bytes integer to human readable ...
BindingError.Error                  M binder.go:87     Error returns error message
  ...and 481 more symbols

-- FOCUS
RequestLogger (middleware/request_logger.go:395-395)
  RequestLogger creates Request Logger middleware with Echo default settings that uses Context.Logger() as logger.
  calls: Logger, RequestLoggerWithConfig

RequestID (middleware/request_id.go:30-30)
  RequestID returns a middleware that reads RequestIDConfig.TargetHeader (`X-Request-ID`) header value or when the header 
  behavior: DELEGATE(RequestIDWithConfig -> result)
  calls: RequestIDWithConfig

Context.Request (context.go:129-129)
  Request returns `*http.Request`.
  called_by: BindBody, BindHeaders, Bind, FormFieldBinder, fsFile, DefaultHTTPErrorHandler, StaticDirectoryHandler, WrapHandler

Echo (echo.go:68-68)
  Echo is the top-level framework instance.
  methods: AcquireContext, Add, AddRoute, Any, CONNECT, DELETE

RequestLoggerConfig.ToMiddleware (middleware/request_logger.go:246-246)
  ToMiddleware converts RequestLoggerConfig into middleware or returns an error for invalid configuration.
  behavior: PRECEDENCE(config); ACCUMULATE(CanonicalHeaderKey loop -> result)
  calls: Echo, Path, QueryParams, RealIP, Request, Response
  called_by: RequestLoggerWithConfig

Context.SetRequest (context.go:134-134)
  SetRequest sets `*http.Request`.
  sig: Context.SetRequest(r *http.Request)
  called_by: newContext, WrapMiddleware, ToMiddleware

RequestIDConfig.ToMiddleware (middleware/request_id.go:42-42)
  ToMiddleware converts RequestIDConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)
  calls: Request, Response

Context.Echo (context.go:665-665)
  Echo returns the `Echo` instance.
  called_by: BindBody, ToMiddleware

CSRFConfig.checkSecFetchSiteRequest (middleware/csrf.go:260-260)
  sig: CSRFConfig.checkSecFetchSiteRequest(c *echo.Context)
  behavior: GUARD(secFetchSite == "" -> return false, nil); PRECEDENCE(secFetchSite -> len -> not_isSafe)
  calls: Request, Set
  called_by: ToMiddleware

Echo.Start (echo.go:744-744)
  Start stars HTTP server on given address with Echo as a handler serving requests.
  sig: Echo.Start(address string)
  behavior: DELEGATE(sc.Start -> result); UNWIND(defer)
  calls: Start
  called_by: main

Echo.Use (echo.go:431-431)
  Use adds middleware to the chain which is run after router has found matching route and before route/request handler met
  sig: Echo.Use(middleware ...MiddlewareFunc)
  called_by: Group, main

RequestLoggerWithConfig (middleware/request_logger.go:237-237)
  RequestLoggerWithConfig returns a RequestLogger middleware with config.
  sig: RequestLoggerWithConfig(config RequestLoggerConfig)
  behavior: GUARD(err != nil -> panic(err))
  calls: ToMiddleware
  called_by: RequestLogger
  raises: panic

Echo.Any (echo.go:504-504)
  Any registers a new route for all HTTP methods (supported by Echo) and path with matching handler in the router with opt
  sig: Echo.Any(path string, handler HandlerFunc, middleware ...Middlewa...)
  behavior: DELEGATE(e.Add -> result)
  calls: Add

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

RequestLoggerValues (middleware/request_logger.go:189-189)
  RequestLoggerValues contains extracted values from logger.

RequestIDWithConfig (middleware/request_id.go:37-37)
  RequestIDWithConfig returns a middleware with given valid config or panics on invalid configuration.
  sig: RequestIDWithConfig(config RequestIDConfig)
  behavior: DELEGATE(toMiddlewareOrPanic -> result)
  called_by: RequestID

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

HTTPError (httperror.go:107-107)
  HTTPError represents an error that occurred while handling a request.
  methods: Error, StatusCode, Unwrap, Wrap

NewVirtualHostHandler (vhost.go:10-10)
  NewVirtualHostHandler creates instance of Echo that routes requests to given virtual hosts when hosts in request does no
  sig: NewVirtualHostHandler(vhosts map[string]*Echo)
  calls: ServeHTTP, serveHTTP

Router (router.go:21-21)
  Router is interface for routing request contexts to registered routes.

Echo.File (echo.go:609-609)
  File registers a new route with path to serve a static file with optional route-level middleware.
  sig: Echo.File(path, file string, middleware ...MiddlewareFunc)
  calls: File, Add
  called_by: contentDisposition, File

Echo.serveHTTP (echo.go:700-700)
  serveHTTP implements `http.Handler` interface, which serves HTTP requests.
  sig: Echo.serveHTTP(w http.ResponseWriter, r *http.Request)
  behavior: GUARD(e.premiddleware == nil -> return h1(cc)); DELEGATE(h1 -> result); UNWIND(defer)
  calls: Reset, applyMiddleware
  called_by: NewVirtualHostHandler

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
  called_by: Static

Echo.ServeHTTP (echo.go:695-695)
  ServeHTTP implements `http.Handler` interface, which serves HTTP requests.
  sig: Echo.ServeHTTP(w http.ResponseWriter, r *http.Request)
  called_by: WrapHandler, WrapMiddleware, NewVirtualHostHandler

Echo.FileFS (echo.go:591-591)
  FileFS registers a new route with path to serve file from the provided file system.
  sig: Echo.FileFS(path, file string, filesystem fs.FS, m ...MiddlewareFunc)
  behavior: DELEGATE(e.GET -> result)
  calls: GET, StaticFileHandler

Echo.GET (echo.go:449-449)
  GET registers a new GET route for a path with matching handler in the router with optional route-level middleware.
  sig: Echo.GET(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(e.Add -> result)
  calls: Add
  called_by: FileFS, main

Echo.AddRoute (echo.go:617-617)
  AddRoute registers a new Route with default host Router
  sig: Echo.AddRoute(route Route)
  behavior: DELEGATE(e.add -> result)
  calls: add
  called_by: Match, Add

Echo.Group (echo.go:659-659)
  Group creates a new router group with prefix and optional group-level middleware.
  sig: Echo.Group(prefix string, m ...MiddlewareFunc)
  calls: Use

Echo.CONNECT (echo.go:437-437)
  CONNECT registers a new CONNECT route for a path with matching handler in the router with optional route-level middlewar
  sig: Echo.CONNECT(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(e.Add -> result)
  calls: Add

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 80 symbols in L3, 51 with behavior annotations
uncovered: Echo.AcquireContext, Echo.Middlewares, Echo.NewContext, Echo.Pre

--- CLUE FILE END ---

QUESTION: Which public types and subcomponents make up Echo's routing and request-handling surface?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
