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
WrapMiddleware (echo.go:766-766)
  WrapMiddleware wraps `func(http.Handler) http.Handler` into `echo.MiddlewareFunc`
  sig: WrapMiddleware(m func(http.Handler)
  calls: ServeHTTP

Echo (echo.go:68-68)
  Echo is the top-level framework instance.
  methods: AcquireContext, Add, AddRoute, Any, CONNECT, DELETE

RequestLogger (middleware/request_logger.go:395-395)
  RequestLogger creates Request Logger middleware with Echo default settings that uses Context.Logger() as logger.
  calls: RequestLoggerWithConfig

MiddlewareConfigurator (echo.go:121-121)
  MiddlewareConfigurator defines interface for creating middleware handlers with possibility to return configuration error

applyMiddleware (echo.go:785-785)
  sig: applyMiddleware(h HandlerFunc, middleware ...MiddlewareFunc)
  behavior: ACCUMULATE(loop -> result)
  called_by: serveHTTP

Echo.Use (echo.go:431-431)
  Use adds middleware to the chain which is run after router has found matching route and before route/request handler met
  sig: Echo.Use(middleware ...MiddlewareFunc)
  called_by: Group, main

RequestLoggerConfig.ToMiddleware (middleware/request_logger.go:246-246)
  ToMiddleware converts RequestLoggerConfig into middleware or returns an error for invalid configuration.
  behavior: PRECEDENCE(config); ACCUMULATE(CanonicalHeaderKey loop -> result)
  called_by: RequestLoggerWithConfig

Echo.Group (echo.go:659-659)
  Group creates a new router group with prefix and optional group-level middleware.
  sig: Echo.Group(prefix string, m ...MiddlewareFunc)
  calls: Use

Echo.GET (echo.go:449-449)
  GET registers a new GET route for a path with matching handler in the router with optional route-level middleware.
  sig: Echo.GET(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(e.Add -> result)
  calls: Add
  called_by: FileFS, main

Echo.Start (echo.go:744-744)
  Start stars HTTP server on given address with Echo as a handler serving requests.
  sig: Echo.Start(address string)
  behavior: DELEGATE(sc.Start -> result); UNWIND(defer)
  called_by: main

GzipConfig.ToMiddleware (middleware/compress.go:69-69)
  ToMiddleware converts GzipConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)
  calls: bufferPool, gzipCompressPool, WriteHeader

ProxyConfig.ToMiddleware (middleware/proxy.go:305-305)
  ToMiddleware converts ProxyConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)
  calls: proxyHTTP, proxyRaw, Next

DecompressConfig.ToMiddleware (middleware/decompress.go:65-65)
  ToMiddleware converts DecompressConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)
  calls: gzipDecompressPool, Close

StaticConfig.ToMiddleware (middleware/static.go:156-156)
  ToMiddleware converts StaticConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)
  calls: listDir, serveFile

AddTrailingSlashConfig.ToMiddleware (middleware/slash.go:39-39)
  ToMiddleware converts AddTrailingSlashConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)
  calls: sanitizeURI

RemoveTrailingSlashConfig.ToMiddleware (middleware/slash.go:103-103)
  ToMiddleware converts RemoveTrailingSlashConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)
  calls: sanitizeURI

CSRFConfig.ToMiddleware (middleware/csrf.go:126-126)
  ToMiddleware converts CSRFConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)
  calls: checkSecFetchSiteRequest, validateCSRFToken

BodyLimitConfig.ToMiddleware (middleware/body_limit.go:47-47)
  ToMiddleware converts BodyLimitConfig to middleware or returns an error for invalid configuration
  calls: Reset

Echo.add (echo.go:621-621)
  sig: Echo.add(route Route)
  behavior: GUARD(e.OnAddRoute != nil -> return RouteInfo{},...); PRECEDENCE(e -> err -> paramsCount)
  calls: Add
  called_by: Add, AddRoute

BasicAuthConfig.ToMiddleware (middleware/basic_auth.go:97-97)
  ToMiddleware converts BasicAuthConfig to middleware or returns an error for invalid configuration
  behavior: GUARD(config.Validator == nil -> return nil, errors....); PRECEDENCE(config)

BodyDumpConfig.ToMiddleware (middleware/body_dump.go:73-73)
  ToMiddleware converts BodyDumpConfig to middleware or returns an error for invalid configuration
  behavior: GUARD(config.Handler == nil -> return nil, errors....); PRECEDENCE(config)

CORSConfig.ToMiddleware (middleware/cors.go:145-145)
  ToMiddleware converts CORSConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config -> len)

ContextTimeoutConfig.ToMiddleware (middleware/context_timeout.go:38-38)
  ToMiddleware converts Config to middleware.
  behavior: GUARD(config.Timeout == 0 -> return nil, errors....); PRECEDENCE(config)

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

Echo.File (echo.go:609-609)
  File registers a new route with path to serve a static file with optional route-level middleware.
  sig: Echo.File(path, file string, middleware ...MiddlewareFunc)
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

Echo.Pre (echo.go:426-426)
  Pre adds middleware to the chain which is run before router tries to find matching route.
  sig: Echo.Pre(middleware ...MiddlewareFunc)

Echo.TRACE (echo.go:485-485)
  TRACE registers a new TRACE route for a path with matching handler in the router with optional route-level middleware.
  sig: Echo.TRACE(path string, h HandlerFunc, m ...MiddlewareFunc)
  behavior: DELEGATE(e.Add -> result)
  calls: Add

KeyAuthConfig.ToMiddleware (middleware/key_auth.go:138-138)
  ToMiddleware converts KeyAuthConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)

MethodOverrideConfig.ToMiddleware (middleware/method_override.go:46-46)
  ToMiddleware converts MethodOverrideConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)

RecoverConfig.ToMiddleware (middleware/recover.go:53-53)
  ToMiddleware converts RecoverConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)
  raises: panic

RedirectConfig.ToMiddleware (middleware/redirect.go:119-119)
  ToMiddleware converts RedirectConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)

RequestIDConfig.ToMiddleware (middleware/request_id.go:42-42)
  ToMiddleware converts RequestIDConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config)

RewriteConfig.ToMiddleware (middleware/rewrite.go:53-53)
  ToMiddleware converts RewriteConfig to middleware or returns an error for invalid configuration
  behavior: PRECEDENCE(config); ACCUMULATE(loop -> result)

SecureConfig.ToMiddleware (middleware/secure.go:101-101)
  ToMiddleware converts SecureConfig to middleware or returns an error for invalid configuration

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 80 symbols in L3, 67 with behavior annotations
uncovered: Echo.Add, Echo.ServeHTTP, Echo.FileFS, Echo.serveHTTP

--- CLUE FILE END ---

QUESTION: How is Echo's public API split between the core framework package and middleware packages?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
