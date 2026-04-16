# Blind Evaluation Prompt - MRLF v2.4
# Task: blind-echo-struct-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 echo@HEAD 44mod 565sym
? How is Echo's public API split between the core framework package and middleware packages?


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
WrapMiddleware (echo.go:766-766)
  WrapMiddleware wraps `func(http.Handler) http.Handler` into `echo.MiddlewareFunc`
  sig: WrapMiddleware(m func(http.Handler)
  calls: Path, PathValues, Request, Response, SetRequest, SetResponse, ServeHTTP

Echo (echo.go:68-68)
  Echo is the top-level framework instance.
  methods: AcquireContext, Add, AddRoute, Any, CONNECT, DELETE

MiddlewareConfigurator (echo.go:121-121)
  MiddlewareConfigurator defines interface for creating middleware handlers with possibility to return configuration error

applyMiddleware (echo.go:785-785)
  sig: applyMiddleware(h HandlerFunc, middleware ...MiddlewareFunc)
  behavior: ACCUMULATE(loop -> result)
  called_by: serveHTTP

GzipConfig.ToMiddleware (middleware/compress.go:69-69)
  ToMiddleware converts GzipConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)
  calls: Request, Reset, Response, SetResponse, WriteHeader, Close, bufferPool, gzipCompressPool

DecompressConfig.ToMiddleware (middleware/decompress.go:65-65)
  ToMiddleware converts DecompressConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)
  calls: Error, Request, Reset, Close, gzipDecompressPool

Echo.File (echo.go:609-609)
  File registers a new route with path to serve a static file with optional route-level middleware.
  sig: Echo.File(path, file string, middleware ...MiddlewareFunc)
  calls: File, Add
  called_by: contentDisposition, File

StaticConfig.ToMiddleware (middleware/static.go:156-156)
  ToMiddleware converts StaticConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)
  calls: Echo, Param, Path, Request, Response, StatusCode, listDir, serveFile

ProxyConfig.ToMiddleware (middleware/proxy.go:305-305)
  ToMiddleware converts ProxyConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)
  calls: Echo, Get, IsWebSocket, RealIP, Request, Response, Scheme, Set

CORSConfig.ToMiddleware (middleware/cors.go:145-145)
  ToMiddleware converts CORSConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config -> len)
  calls: Get, NoContent, Request, Response

RequestLoggerConfig.ToMiddleware (middleware/request_logger.go:246-246)
  ToMiddleware converts RequestLoggerConfig into middleware or returns an error for invalid configuration.
  behavior: PRECEDENCE(config); ACCUMULATE(CanonicalHeaderKey loop -> result)
  calls: Echo, Path, QueryParams, RealIP, Request, Response
  called_by: RequestLoggerWithConfig

CSRFConfig.ToMiddleware (middleware/csrf.go:126-126)
  ToMiddleware converts CSRFConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)
  calls: Cookie, Request, Response, Set, SetCookie, checkSecFetchSiteRequest, validateCSRFToken

RemoveTrailingSlashConfig.ToMiddleware (middleware/slash.go:103-103)
  ToMiddleware converts RemoveTrailingSlashConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)
  calls: QueryString, Redirect, Request, sanitizeURI

AddTrailingSlashConfig.ToMiddleware (middleware/slash.go:39-39)
  ToMiddleware converts AddTrailingSlashConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)
  calls: QueryString, Redirect, Request, sanitizeURI

Echo.GET (echo.go:449-449)
  GET registers a new GET route for a path with matching handler in the router with optional route-level middleware.
  sig: Echo.GET(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(e.Add -> result)
  calls: Add
  called_by: FileFS, main

BodyLimitConfig.ToMiddleware (middleware/body_limit.go:47-47)
  ToMiddleware converts BodyLimitConfig to middleware or returns an error for invalid configuration
  calls: Request, Reset

ContextTimeoutConfig.ToMiddleware (middleware/context_timeout.go:38-38)
  ToMiddleware converts Config to middleware.
  behavior: GUARD(config.Timeout == 0 -> return nil, errors....); PRECEDENCE(config)
  calls: Request, SetRequest

SecureConfig.ToMiddleware (middleware/secure.go:101-101)
  ToMiddleware converts SecureConfig to middleware or returns an error for invalid configuration
  calls: IsTLS, Request, Response

RedirectConfig.ToMiddleware (middleware/redirect.go:119-119)
  ToMiddleware converts RedirectConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)
  calls: Redirect, Request, Scheme

BodyDumpConfig.ToMiddleware (middleware/body_dump.go:73-73)
  ToMiddleware converts BodyDumpConfig to middleware or returns an error for invalid configuration
  behavior: GUARD(config.Handler == nil -> return nil, errors....); PRECEDENCE(config)
  calls: Request, Response, SetResponse

BasicAuthConfig.ToMiddleware (middleware/basic_auth.go:97-97)
  ToMiddleware converts BasicAuthConfig to middleware or returns an error for invalid configuration
  behavior: GUARD(config.Validator == nil -> return nil, errors....); PRECEDENCE(config)
  calls: Request, Response

RequestIDConfig.ToMiddleware (middleware/request_id.go:42-42)
  ToMiddleware converts RequestIDConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)
  calls: Request, Response

MethodOverrideConfig.ToMiddleware (middleware/method_override.go:46-46)
  ToMiddleware converts MethodOverrideConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)
  calls: Request

RewriteConfig.ToMiddleware (middleware/rewrite.go:53-53)
  ToMiddleware converts RewriteConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config); ACCUMULATE(loop -> result)
  calls: Request

Context.Echo (context.go:665-665)
  Echo returns the `Echo` instance.
  called_by: BindBody, ToMiddleware

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

Echo.Group (echo.go:659-659)
  Group creates a new router group with prefix and optional group-level middleware.
  sig: Echo.Group(prefix string, m ...MiddlewareFunc)
  calls: Use

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

RateLimiterConfig.ToMiddleware (middleware/rate_limiter.go:109-109)
  ToMiddleware converts RateLimiterConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)
  calls: Allow

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 80 symbols in L3, 65 with behavior annotations
uncovered: Echo.AcquireContext, Echo.Middlewares, Echo.NewContext, Echo.PreMiddlewares

--- CLUE FILE END ---

QUESTION: How is Echo's public API split between the core framework package and middleware packages?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
