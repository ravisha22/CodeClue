# Blind Evaluation Prompt - MRLF v2.4
# Task: blind-gin-struct-2

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 gin@HEAD 58mod 541sym
? How do Gin's public context helpers divide request reading, binding, and response writing responsibilities?


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
Context.requestHeader (context.go:1050-1050)
  sig: Context.requestHeader(key string)
  behavior: DELEGATE(c.Request.Header.Get -> result)
  calls: Get
  called_by: BasicAuthForProxy, BasicAuthForRealm, ClientIP, ContentType, GetHeader, IsWebsocket, NegotiateFormat

Context.Deadline (context.go:1447-1447)
  Deadline returns that there is no deadline (ok==false) when c.Request has no Context.
  behavior: GUARD(!c.hasRequestContext() -> return)
  calls: hasRequestContext, Context

Context.Done (context.go:1455-1455)
  Done returns nil (chan which will wait forever) when c.Request has no Context.
  behavior: GUARD(!c.hasRequestContext() -> return nil)
  calls: hasRequestContext, Context

Context.Err (context.go:1463-1463)
  Err returns nil when c.Request has no Context.
  behavior: GUARD(!c.hasRequestContext() -> return nil)
  calls: hasRequestContext, Context

Context.hasRequestContext (context.go:1440-1440)
  hasRequestContext returns whether c.Request has Context and fallback.
  calls: Context
  called_by: Deadline, Done, Err, Value

multipartRequest.TrySet (binding/multipart_form_mapping.go:27-27)
  TrySet tries to set a value by the multipart request with the binding a form file
  sig: multipartRequest.TrySet(value reflect.Value, field reflect.StructField, key stri...)
  behavior: GUARD(files := r.MultipartForm.File[key]; len(files... -> return setByMultip...)
  calls: setByMultipartFormFile

Context (context.go:61-61)
  Context is the most important part of gin.
  methods: Abort, AbortWithError, AbortWithStatus, AbortWithStatusJSON, AbortWithStatusPureJSON, AddParam
  called_by: ClientIP, Deadline, Done, Err, Value, hasRequestContext

Context.ShouldBindBodyWith (context.go:928-928)
  ShouldBindBodyWith is similar with ShouldBindWith, but it stores the request body into the context, and reuse when it is
  sig: Context.ShouldBindBodyWith(obj any, bb binding.BindingBody)
  behavior: PRECEDENCE(cb -> body)
  calls: Get, Set
  called_by: ShouldBindBodyWithJSON, ShouldBindBodyWithPlain, ShouldBindBodyWithTOML, ShouldBindBodyWithXML, ShouldBindBodyWithYAML

Context.Copy (context.go:122-122)
  Copy returns a copy of the current context that can be safely used outside the request's scope.
  called_by: SaveUploadedFile, Render

Binding (binding/binding.go:32-32)
  Binding describes the interface which needs to be implemented for binding the data present in the request such as JSON r

Binding (binding/binding_nomsgpack.go:30-30)
  Binding describes the interface which needs to be implemented for binding the data present in the request such as JSON r

Context.Value (context.go:1473-1473)
  Value returns the value associated with this context for key, or nil if no value is associated with key.
  sig: Context.Value(key any)
  behavior: GUARD(key == ContextRequestKey -> return c.Request); PRECEDENCE(key -> keyAsString)
  calls: Get, hasRequestContext, Context
  called_by: ClientIP

Engine.HandleContext (gin.go:680-680)
  HandleContext re-enters a context that has been rewritten.
  sig: Engine.HandleContext(c *Context)
  calls: reset, handleHTTPRequest

redirectRequest (gin.go:820-820)
  sig: redirectRequest(c *Context)
  calls: String
  called_by: redirectFixedPath, redirectTrailingSlash

Engine.allocateContext (gin.go:252-252)
  sig: Engine.allocateContext(maxParams uint16)
  called_by: New, CreateTestContext, CreateTestContextOnly

Context.GetHeader (context.go:1089-1089)
  GetHeader returns value from request headers.
  sig: Context.GetHeader(key string)
  behavior: DELEGATE(c.requestHeader -> result)
  calls: requestHeader

Context.IsWebsocket (context.go:1042-1042)
  IsWebsocket returns true if the request headers indicate that a websocket handshake is being initiated by the client.
  behavior: GUARD(strings.Contains(strings.ToLower(c.requestHea... -> return true)
  calls: requestHeader

Context.ShouldBindUri (context.go:909-909)
  ShouldBindUri binds the passed struct pointer using the specified binding engine.
  sig: Context.ShouldBindUri(obj any)
  behavior: DELEGATE(binding.Uri.BindUri -> result); ACCUMULATE(loop -> result)
  calls: BindUri
  called_by: BindUri

responseWriter.Pusher (response_writer.go:136-136)
  behavior: GUARD(pusher, ok := w.ResponseWriter.(http.Pusher); ok -> return pusher)

Context.JSON (context.go:1205-1205)
  JSON serializes the given struct as JSON into the response body.
  sig: Context.JSON(code int, obj any)
  calls: Render
  called_by: AbortWithStatusJSON, Negotiate, main, MarshalJSON, JSON, ErrorLoggerT

Context.Render (context.go:1152-1152)
  Render writes the response headers and calls render.Render to render data.
  sig: Context.Render(code int, r render.Render)
  behavior: GUARD(!bodyAllowedForStatus(code) -> return)
  calls: Error, Abort, Status, bodyAllowedForStatus, Render, WriteContentType
  called_by: AsciiJSON, BSON, Data, DataFromReader, HTML, IndentedJSON, JSON, JSONP

Context.String (context.go:1254-1254)
  String writes the given string into the response body.
  sig: Context.String(code int, format string, values ...any)
  calls: Render
  called_by: Error, ClientIP, debugPrintLoadTemplate, JSON, redirectRequest

Context.reset (context.go:103-103)
  called_by: HandleContext, ServeHTTP, CreateTestContext, CreateTestContextOnly

responseWriter (response_writer.go:49-49)
  type responseWriter
  methods: CloseNotify, Flush, Hijack, Pusher, Size, Status

Context.ShouldBindWith (context.go:919-919)
  ShouldBindWith binds the passed struct pointer using the specified binding engine.
  sig: Context.ShouldBindWith(obj any, b binding.Binding)
  behavior: DELEGATE(b.Bind -> result)
  calls: Bind
  called_by: MustBindWith, ShouldBind, ShouldBindHeader, ShouldBindJSON, ShouldBindPlain, ShouldBindQuery, ShouldBindTOML, ShouldBindXML

Context.Stream (context.go:1328-1328)
  Stream sends a streaming response and returns a boolean indicates "Is client disconnected in middle of stream"
  sig: Context.Stream(step func(w io.Writer)
  behavior: ACCUMULATE(step loop -> result)
  calls: CloseNotify, Flush

responseWriter.Write (response_writer.go:84-84)
  sig: responseWriter.Write(data []byte)
  calls: WriteHeaderNow
  called_by: Render, WriteJSON, WriteString

responseWriter.Status (response_writer.go:98-98)
  called_by: AbortWithStatus, Render

Context.Error (context.go:252-252)
  Error attaches an error to the current context.
  sig: Context.Error(err error)
  behavior: GUARD(err == nil -> panic("err is nil")); PRECEDENCE(err -> not_ok)
  called_by: AbortWithError, Render, Error, JSON, Errors, CustomRecoveryWithWriter
  raises: panic

Context.Set (context.go:276-276)
  Set is used to store a new key/value pair exclusively for this context.
  sig: Context.Set(key any, value any)
  behavior: UNWIND(defer)
  called_by: BasicAuthForProxy, BasicAuthForRealm, FileAttachment, Header, ShouldBindBodyWith, Bind

Context.JSONP (context.go:1194-1194)
  JSONP serializes the given struct as JSON into the response body.
  sig: Context.JSONP(code int, obj any)
  behavior: GUARD(callback == "" -> return)
  calls: DefaultQuery, Render

Context.PureJSON (context.go:1217-1217)
  PureJSON serializes the given struct as JSON into the response body.
  sig: Context.PureJSON(code int, obj any)
  calls: Render
  called_by: AbortWithStatusPureJSON

Context.MustBindWith (context.go:810-810)
  MustBindWith binds the passed struct pointer using the specified binding engine.
  sig: Context.MustBindWith(obj any, b binding.Binding)
  behavior: GUARD(err != nil -> return err)
  calls: AbortWithError, ShouldBindWith
  called_by: Bind, BindHeader, BindJSON, BindPlain, BindQuery, BindTOML, BindXML, BindYAML

Context.BSON (context.go:1249-1249)
  BSON serializes the given struct as BSON into the response body.
  sig: Context.BSON(code int, obj any)
  calls: Render
  called_by: Negotiate

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 80 symbols in L3, 32 with behavior annotations
uncovered: Context.Delete, Context.HandlerNames, Context.IsAborted, Context.RemoteIP

--- CLUE FILE END ---

QUESTION: How do Gin's public context helpers divide request reading, binding, and response writing responsibilities?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
