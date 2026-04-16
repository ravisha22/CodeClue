# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: blind-gin-mech-1

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.

--- CLUE FILE (File 1) ---
=CC v2.1 gin@HEAD 58mod 541sym
? How does Gin's documented router behavior handle named parameters, catch-all parameters, exact matches, and redirects when routes overlap?


-- TREE
binding/  (17 files)
codec/  (5 files)
  json/
ginS/  (1 files)
internal/  (2 files)
  bytesconv/  fs/
render/  (14 files)
auth.go  context.go  context_appengine.go  debug.go  deprecated.go  doc.go  errors.go  fs.go  gin.go  logger.go  mode.go  path.go  recovery.go  response_writer.go  routergroup.go

-- INDEX
tree.go                                         950L  Param, ByName, Get, countParams, countSections
errors.go                                       173L  Error, IsType, JSON, MarshalJSON, SetMeta
gin.go                                          832L  Default, Delims, HandleContext, Handler, LoadHTMLFS
context.go                                     1489L  Abort, AbortWithError, AbortWithStatus, AbortWithStatusJSON, AbortWithStatusPureJSON
binding/default_validator.go                     95L  Error, Engine, ValidateStruct, lazyinit, validateStruct
render/html.go                                  101L  Delims, Render, WriteContentType, HTML, Instance
render/json.go                                  194L  Render, WriteContentType, AsciiJSON, Render, WriteContentType
render/msgpack.go                                43L  Render, WriteContentType, MsgPack, WriteMsgPack
render/redirect.go                               29L  Render, WriteContentType, Redirect
render/text.go                                   41L  Render, WriteContentType, String, WriteString
auth.go                                         116L  BasicAuth, BasicAuthForProxy, BasicAuthForRealm, authPair, searchCredential
binding/binding.go                              127L  Binding, BindingBody, BindingUri, Default, StructValidator
binding/binding_nomsgpack.go                    121L  Binding, BindingBody, BindingUri, Default, StructValidator
binding/bson.go                                  30L  Bind, bsonBinding
binding/form.go                                  64L  
binding/form_mapping.go                         550L  BindUnmarshaler, MapFormWithTag, TrySet, head, mapForm
binding/header.go                                37L  headerBinding, TrySet, mapHeader
binding/json.go                                  56L  decodeJSON, jsonBinding
binding/msgpack.go                               37L  decodeMsgPack, msgpackBinding
  ...and 39 more modules

-- SYM
Context.Get                         M context.go:288    Get returns the value for the given key, ie: (v...
Context.initQueryCache              M context.go:568    function Context.initQueryCache
Context.GetQueryArray               M context.go:580    GetQueryArray returns a slice of strings for a ...
Context.GetQuery                    M context.go:554    GetQuery is like Query(), it returns the keyed ...
RouterGroup.handle                  M routergroup.go:86     function RouterGroup.handle
Context.Query                       M context.go:525    Query returns the keyed url query value if it e...
Context.ShouldBindWith              M context.go:919    ShouldBindWith binds the passed struct pointer ...
Context.MustBindWith                M context.go:810    MustBindWith binds the passed struct pointer us...
setByMultipartFormFile              M binding/multipart_form_mapping.go:35     function setByMultipartFormFile
responseWriter.WriteHeaderNow       M response_writer.go:77     function responseWriter.WriteHeaderNow
responseWriter.Written              M response_writer.go:106    function responseWriter.Written
setArrayOfMultipartFormFiles        M binding/multipart_form_mapping.go:63     function setArrayOfMultipartFormFiles
Context.AbortWithError              M context.go:238    AbortWithError calls `AbortWithStatus()` and `E...
Context.requestHeader               M context.go:1050   function Context.requestHeader
RouterGroup.returnObj               M routergroup.go:254    function RouterGroup.returnObj
Context.Set                         M context.go:276    Set is used to store a new key/value pair exclu...
Params.Get                          M tree.go:29     Get returns the value of the first Param which ...
IsDebugging                         M debug.go:22     IsDebugging returns true if the framework is ru...
Context.initFormCache               M context.go:638    function Context.initFormCache
Context.ShouldBindBodyWith          M context.go:928    ShouldBindBodyWith is similar with ShouldBindWi...
Context                             C context.go:61     Context is the most important part of gin.
responseWriter.Write                M response_writer.go:84     function responseWriter.Write
responseWriter.WriteHeader          M response_writer.go:67     function responseWriter.WriteHeader
Engine.isTrustedProxy               M gin.go:469    isTrustedProxy will check whether the IP addres...
Context.Next                        M context.go:188    Next should be used only inside middleware.
RouterGroup.calculateAbsolutePath   M routergroup.go:250    function RouterGroup.calculateAbsolutePath
SliceValidationError.Error          M binding/default_validator.go:24     Error concatenates all error elements in SliceV...
Context.Error                       M context.go:252    Error attaches an error to the current context.
RouterGroup.combineHandlers         M routergroup.go:241    function RouterGroup.combineHandlers
Context.GetPostFormArray            M context.go:653    GetPostFormArray returns a slice of strings for...
bsonBinding.Bind                    M binding/bson.go:20     function bsonBinding.Bind
protobufBinding.Bind                M binding/protobuf.go:21     function protobufBinding.Bind
Context.Bind                        M context.go:757    Bind checks the Method and Content-Type to sele...
Context.String                      M context.go:1254   String writes the given string into the respons...
Context.AbortWithStatus             M context.go:213    AbortWithStatus calls `Abort()` and writes the ...
debugPrint                          M debug.go:56     function debugPrint
Engine.isUnsafeTrustedProxies       M gin.go:457    isUnsafeTrustedProxies checks if Engine.trusted...
errorMsgs.String                    M errors.go:161    function errorMsgs.String
mapFormByTag                        M binding/form_mapping.go:46     function mapFormByTag
LoggerWithConfig                    M logger.go:245    LoggerWithConfig instance a Logger middleware w...
Context.Header                      M context.go:1080   Header is an intelligent shortcut for c.Writer....
Error.Error                         M errors.go:82     Error implements the error interface.
defaultValidator.lazyinit           M binding/default_validator.go:90     function defaultValidator.lazyinit
responseWriter.WriteString          M response_writer.go:91     function responseWriter.WriteString
CustomRecoveryWithWriter            M recovery.go:53     CustomRecoveryWithWriter returns a middleware f...
Engine.Handler                      M gin.go:243    function Engine.Handler
parseIP                             M gin.go:525    parseIP parse a string representation of an IP ...
Context.ContentType                 M context.go:1036   ContentType returns the Content-Type header of ...
mapping                             M binding/form_mapping.go:84     function mapping
Context.File                        M context.go:1286   File writes the specified file into the body st...
Context.Abort                       M context.go:207    Abort prevents pending handlers from being called.
HandlersChain.Last                  M gin.go:60     Last returns the last handler in the chain.
Context.BindUri                     M context.go:799    BindUri binds the passed struct pointer using b...
setWithProperType                   M binding/form_mapping.go:323    function setWithProperType
Error.JSON                          M errors.go:55     JSON creates a properly formatted JSON
WriteJSON                           M render/json.go:67     WriteJSON marshals the given interface object a...
WriteMsgPack                        M render/msgpack.go:39     WriteMsgPack writes MsgPack ContentType and enc...
Redirect                            C render/redirect.go:13     Redirect contains the http request reference an...
WriteString                         M render/text.go:33     WriteString writes data according to its format...
Context.GetPostForm                 M context.go:624    GetPostForm is like PostForm(key).
bufApp                              M path.go:128    Internal helper to lazily create a buffer if ne...
RecoveryWithWriter                  M recovery.go:45     RecoveryWithWriter returns a middleware for a g...
redirectRequest                     M gin.go:820    function redirectRequest
Error                               C errors.go:32     Error represents a error's specification.
shiftNRuneBytes                     M tree.go:687    Shift bytes in array by n bytes left
getMapFromFormData                  M context.go:674    getMapFromFormData return a map which satisfies...
Engine.prepareTrustedCIDRs          M gin.go:414    function Engine.prepareTrustedCIDRs
Delims                              C render/html.go:15     Delims represents a set of Left and Right delim...
Context.hasRequestContext           M context.go:1440   hasRequestContext returns whether c.Request has...
mappingByPtr                        M binding/form_mapping.go:79     function mappingByPtr
setFormMap                          M binding/form_mapping.go:528    function setFormMap
Context.ClientIP                    M context.go:975    ClientIP implements one best effort algorithm t...
updateRouteTree                     M gin.go:504    updateRouteTree do update to the route tree rec...
Context.JSON                        M context.go:1205   JSON serializes the given struct as JSON into t...
Engine.rebuild404Handlers           M gin.go:356    function Engine.rebuild404Handlers
Engine.rebuild405Handlers           M gin.go:360    function Engine.rebuild405Handlers
BSON.WriteContentType               M render/bson.go:32     WriteContentType (BSONBuf) writes BSONBuf Conte...
  ...and 461 more symbols

-- FOCUS
RouterGroup.handle (routergroup.go:86-86)
  sig: RouterGroup.handle(httpMethod, relativePath string, handlers HandlersChain)
  behavior: DELEGATE(group.returnObj -> result)
  calls: calculateAbsolutePath, combineHandlers, returnObj
  called_by: Any, DELETE, GET, HEAD, Handle, Match, OPTIONS, PATCH

RouterGroup.GET (routergroup.go:116-116)
  GET is a shortcut for router.Handle("GET", path, handlers).
  sig: RouterGroup.GET(relativePath string, handlers ...HandlerFunc)
  behavior: DELEGATE(group.handle -> result)
  calls: handle
  called_by: main, StaticFS, staticFileHandler

RouterGroup.HEAD (routergroup.go:141-141)
  HEAD is a shortcut for router.Handle("HEAD", path, handlers).
  sig: RouterGroup.HEAD(relativePath string, handlers ...HandlerFunc)
  behavior: DELEGATE(group.handle -> result)
  calls: handle
  called_by: StaticFS, staticFileHandler

RouterGroup.DELETE (routergroup.go:121-121)
  DELETE is a shortcut for router.Handle("DELETE", path, handlers).
  sig: RouterGroup.DELETE(relativePath string, handlers ...HandlerFunc)
  behavior: DELEGATE(group.handle -> result)
  calls: handle

RouterGroup.OPTIONS (routergroup.go:136-136)
  OPTIONS is a shortcut for router.Handle("OPTIONS", path, handlers).
  sig: RouterGroup.OPTIONS(relativePath string, handlers ...HandlerFunc)
  behavior: DELEGATE(group.handle -> result)
  calls: handle

RouterGroup.PATCH (routergroup.go:126-126)
  PATCH is a shortcut for router.Handle("PATCH", path, handlers).
  sig: RouterGroup.PATCH(relativePath string, handlers ...HandlerFunc)
  behavior: DELEGATE(group.handle -> result)
  calls: handle

RouterGroup.POST (routergroup.go:111-111)
  POST is a shortcut for router.Handle("POST", path, handlers).
  sig: RouterGroup.POST(relativePath string, handlers ...HandlerFunc)
  behavior: DELEGATE(group.handle -> result)
  calls: handle

RouterGroup.PUT (routergroup.go:131-131)
  PUT is a shortcut for router.Handle("PUT", path, handlers).
  sig: RouterGroup.PUT(relativePath string, handlers ...HandlerFunc)
  behavior: DELEGATE(group.handle -> result)
  calls: handle

IRouter (routergroup.go:27-27)
  IRouter defines all router handle interface includes single and group router.

IRoutes (routergroup.go:33-33)
  IRoutes defines all router handle interface.

Engine.handleHTTPRequest (gin.go:690-690)
  sig: Engine.handleHTTPRequest(c *Context)
  behavior: PRECEDENCE(engine); ACCUMULATE(getValue loop -> result)
  calls: Next, redirectFixedPath, redirectTrailingSlash, serveError
  called_by: HandleContext, ServeHTTP

Engine.HandleContext (gin.go:680-680)
  HandleContext re-enters a context that has been rewritten.
  sig: Engine.HandleContext(c *Context)
  calls: reset, handleHTTPRequest

Engine.Routes (gin.go:390-390)
  Routes returns a slice of registered routes, including some useful information, such as: the http method, path, and the 
  behavior: ACCUMULATE(iterate loop -> result)
  calls: iterate

Handle (ginS/gins.go:56-56)
  Handle is a wrapper for Engine.Handle.
  sig: Handle(httpMethod, relativePath string, handlers ...gin.Handler...)
  behavior: DELEGATE(engine -> result)

RouterGroup.Handle (routergroup.go:103-103)
  Handle registers a new request handle and middleware with the given path and method.
  sig: RouterGroup.Handle(httpMethod, relativePath string, handlers ...HandlerFunc)
  behavior: GUARD(matched := regEnLetter.MatchString(httpMethod... -> panic("http method...)
  calls: handle
  raises: panic

Routes (ginS/gins.go:129-129)
  Routes returns a slice of registered routes.
  behavior: DELEGATE(engine -> result)

RouterGroup.Any (routergroup.go:147-147)
  Any registers a route that matches all the HTTP methods.
  sig: RouterGroup.Any(relativePath string, handlers ...HandlerFunc)
  behavior: DELEGATE(group.returnObj -> result); ACCUMULATE(handle loop -> result)
  calls: handle, returnObj

RouterGroup.Match (routergroup.go:156-156)
  Match registers a route that matches the specified methods that you declared.
  sig: RouterGroup.Match(methods []string, relativePath string, handlers ...Handl...)
  behavior: DELEGATE(group.returnObj -> result); ACCUMULATE(handle loop -> result)
  calls: handle, returnObj

RouterGroup (routergroup.go:55-55)
  RouterGroup is used internally to configure router, a RouterGroup is associated with a prefix and an array of handlers (
  methods: Any, BasePath, DELETE, GET, Group, HEAD

RouterGroup.createStaticHandler (routergroup.go:216-216)
  sig: RouterGroup.createStaticHandler(relativePath string, fs http.FileSystem)
  calls: Param, Open, calculateAbsolutePath
  called_by: StaticFS

RouterGroup.staticFileHandler (routergroup.go:181-181)
  sig: RouterGroup.staticFileHandler(relativePath string, handler HandlerFunc)
  behavior: GUARD(strings.Contains(relativePath, ":") || string... -> panic("URL paramet...)
  calls: GET, HEAD, returnObj
  called_by: StaticFile, StaticFileFS
  raises: panic

RouterGroup.calculateAbsolutePath (routergroup.go:250-250)
  sig: RouterGroup.calculateAbsolutePath(relativePath string)
  behavior: DELEGATE(joinPaths -> result)
  called_by: Group, createStaticHandler, handle

RouterGroup.returnObj (routergroup.go:254-254)
  behavior: GUARD(group.root -> return group.engine)
  called_by: Any, Match, StaticFS, Use, handle, staticFileHandler

RouterGroup.Group (routergroup.go:72-72)
  Group creates a new router group.
  sig: RouterGroup.Group(relativePath string, handlers ...HandlerFunc)
  calls: calculateAbsolutePath, combineHandlers

RouterGroup.combineHandlers (routergroup.go:241-241)
  sig: RouterGroup.combineHandlers(handlers HandlersChain)
  called_by: Group, handle

RouterGroup.BasePath (routergroup.go:82-82)
  BasePath returns the base path of router group.

defaultHandleRecovery (recovery.go:109-109)
  sig: defaultHandleRecovery(c *Context, _ any)
  calls: AbortWithStatus

Engine.Run (gin.go:540-540)
  Run attaches the router to a http.Server and starts listening and serving HTTP requests.
  sig: Engine.Run(addr ...string)
  behavior: UNWIND(defer)
  calls: Handler, isUnsafeTrustedProxies, updateRouteTrees
  called_by: main

Engine.Use (gin.go:340-340)
  Use attaches a global middleware to the router.
  sig: Engine.Use(middleware ...HandlerFunc)
  calls: rebuild404Handlers, rebuild405Handlers
  called_by: Default

Engine.RunListener (gin.go:645-645)
  RunListener attaches the router to a http.Server and starts listening and serving HTTP requests through the specified ne
  sig: Engine.RunListener(listener net.Listener)
  behavior: UNWIND(defer)
  calls: Handler, isUnsafeTrustedProxies
  called_by: RunFd

Engine.RunQUIC (gin.go:630-630)
  RunQUIC attaches the router to a http.Server and starts listening and serving QUIC requests.
  sig: Engine.RunQUIC(addr, certFile, keyFile string)
  behavior: UNWIND(defer)
  calls: Handler, isUnsafeTrustedProxies

Engine.RunTLS (gin.go:561-561)
  RunTLS attaches the router to a http.Server and starts listening and serving HTTPS (secure) requests.
  sig: Engine.RunTLS(addr, certFile, keyFile string)
  behavior: UNWIND(defer)
  calls: Handler, isUnsafeTrustedProxies

Engine.RunUnix (gin.go:581-581)
  RunUnix attaches the router to a http.Server and starts listening and serving HTTP requests through the specified unix s
  sig: Engine.RunUnix(file string)
  behavior: PRECEDENCE(engine -> err); UNWIND(defer)
  calls: Handler, isUnsafeTrustedProxies

Engine.NoMethod (gin.go:332-332)
  NoMethod sets the handlers called when Engine.HandleMethodNotAllowed = true.
  sig: Engine.NoMethod(handlers ...HandlerFunc)
  calls: rebuild405Handlers

Engine.RunFd (gin.go:607-607)
  RunFd attaches the router to a http.Server and starts listening and serving HTTP requests through the specified file des
  sig: Engine.RunFd(fd int)
  behavior: PRECEDENCE(engine -> err); UNWIND(defer)
  calls: RunListener, isUnsafeTrustedProxies

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 61 with behavior annotations
uncovered: Engine.LoadHTMLFS, Engine.LoadHTMLFiles, Engine.LoadHTMLGlob, Engine.Delims
drill: routergroup.go (~1 lines, RouterGroup.handle)
drill: routergroup.go (~1 lines, RouterGroup.HEAD)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## RouterGroup.handle  (routergroup.go L86-86)
```
func (group *RouterGroup) handle(httpMethod, relativePath string, handlers HandlersChain) IRoutes {
```

## RouterGroup.HEAD  (routergroup.go L141-141)
```
func (group *RouterGroup) HEAD(relativePath string, handlers ...HandlerFunc) IRoutes {
```

## IRouter  (routergroup.go L27-27)
```
type IRouter interface {
```

## IRoutes  (routergroup.go L33-33)
```
type IRoutes interface {
```

## RouterGroup.Any  (routergroup.go L147-147)
```
func (group *RouterGroup) Any(relativePath string, handlers ...HandlerFunc) IRoutes {
```

## RouterGroup.BasePath  (routergroup.go L82-82)
```
func (group *RouterGroup) BasePath() string {
```

## RouterGroup.DELETE  (routergroup.go L121-121)
```
func (group *RouterGroup) DELETE(relativePath string, handlers ...HandlerFunc) IRoutes {
```

## RouterGroup.GET  (routergroup.go L116-116)
```
func (group *RouterGroup) GET(relativePath string, handlers ...HandlerFunc) IRoutes {
```

## RouterGroup.Group  (routergroup.go L72-72)
```
func (group *RouterGroup) Group(relativePath string, handlers ...HandlerFunc) *RouterGroup {
```

## RouterGroup.Handle  (routergroup.go L103-103)
```
func (group *RouterGroup) Handle(httpMethod, relativePath string, handlers ...HandlerFunc) IRoutes {
```

## RouterGroup.Match  (routergroup.go L156-156)
```
func (group *RouterGroup) Match(methods []string, relativePath string, handlers ...HandlerFunc) IRoutes {
```

## RouterGroup.OPTIONS  (routergroup.go L136-136)
```
func (group *RouterGroup) OPTIONS(relativePath string, handlers ...HandlerFunc) IRoutes {
```

## RouterGroup.PATCH  (routergroup.go L126-126)
```
func (group *RouterGroup) PATCH(relativePath string, handlers ...HandlerFunc) IRoutes {
```

## RouterGroup.POST  (routergroup.go L111-111)
```
func (group *RouterGroup) POST(relativePath string, handlers ...HandlerFunc) IRoutes {
```

## RouterGroup.PUT  (routergroup.go L131-131)
```
func (group *RouterGroup) PUT(relativePath string, handlers ...HandlerFunc) IRoutes {
```

## RouterGroup.Static  (routergroup.go L197-197)
```
func (group *RouterGroup) Static(relativePath, root string) IRoutes {
```

## RouterGroup.StaticFS  (routergroup.go L203-203)
```
func (group *RouterGroup) StaticFS(relativePath string, fs http.FileSystem) IRoutes {
```

## RouterGroup.StaticFile  (routergroup.go L166-166)
```
func (group *RouterGroup) StaticFile(relativePath, filepath string) IRoutes {
```

## RouterGroup.StaticFileFS  (routergroup.go L175-175)
```
func (group *RouterGroup) StaticFileFS(relativePath, filepath string, fs http.FileSystem) IRoutes {
```

## RouterGroup.Use  (routergroup.go L65-65)
```
func (group *RouterGroup) Use(middleware ...HandlerFunc) IRoutes {
```

## RouterGroup.calculateAbsolutePath  (routergroup.go L250-250)
```
func (group *RouterGroup) calculateAbsolutePath(relativePath string) string {
```

## RouterGroup.combineHandlers  (routergroup.go L241-241)
```
func (group *RouterGroup) combineHandlers(handlers HandlersChain) HandlersChain {
```

## RouterGroup.createStaticHandler  (routergroup.go L216-216)
```
func (group *RouterGroup) createStaticHandler(relativePath string, fs http.FileSystem) HandlerFunc {
```

## RouterGroup.returnObj  (routergroup.go L254-254)
```
func (group *RouterGroup) returnObj() IRoutes {
```

## RouterGroup.staticFileHandler  (routergroup.go L181-181)
```
func (group *RouterGroup) staticFileHandler(relativePath string, handler HandlerFunc) IRoutes {
```

## RouterGroup  (routergroup.go L55-55)
```
type RouterGroup struct {
```
--- END SOURCE SNIPPETS ---

QUESTION: How does Gin's documented router behavior handle named parameters, catch-all parameters, exact matches, and redirects when routes overlap?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
