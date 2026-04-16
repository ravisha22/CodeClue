# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: blind-gin-mech-2

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.

--- CLUE FILE (File 1) ---
=CC v2.1 gin@HEAD 58mod 541sym
? What documented rules does Gin follow when binding request data and handling binding failures?


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
Binding (binding/binding.go:32-32)
  Binding describes the interface which needs to be implemented for binding the data present in the request such as JSON r

Binding (binding/binding_nomsgpack.go:30-30)
  Binding describes the interface which needs to be implemented for binding the data present in the request such as JSON r

multipartRequest.TrySet (binding/multipart_form_mapping.go:27-27)
  TrySet tries to set a value by the multipart request with the binding a form file
  sig: multipartRequest.TrySet(value reflect.Value, field reflect.StructField, key stri...)
  behavior: GUARD(files := r.MultipartForm.File[key]; len(files... -> return setByMultip...)
  calls: setByMultipartFormFile

redirectRequest (gin.go:820-820)
  sig: redirectRequest(c *Context)
  calls: String
  called_by: redirectFixedPath, redirectTrailingSlash

Context.requestHeader (context.go:1050-1050)
  sig: Context.requestHeader(key string)
  behavior: DELEGATE(c.Request.Header.Get -> result)
  calls: Get
  called_by: BasicAuthForProxy, BasicAuthForRealm, ClientIP, ContentType, GetHeader, IsWebsocket, NegotiateFormat

Context.GetRawData (context.go:1094-1094)
  GetRawData returns stream data.
  behavior: GUARD(c.Request.Body == nil -> return nil, errors....)

Data.Render (render/data.go:19-19)
  Render (Data) writes data with custom ContentType.
  sig: Data.Render(w http.ResponseWriter)
  calls: Header, WriteContentType, Write
  called_by: AsciiJSON, BSON, Data, DataFromReader, HTML, IndentedJSON, JSON, JSONP

Context.Data (context.go:1268-1268)
  Data writes some data into the body stream and updates the HTTP code.
  sig: Context.Data(code int, contentType string, data []byte)
  calls: Render

Context.DataFromReader (context.go:1276-1276)
  DataFromReader writes the specified reader into the body stream and updates the HTTP code.
  sig: Context.DataFromReader(code int, contentLength int64, contentType string, reade...)
  calls: Render

bsonBinding.Bind (binding/bson.go:20-20)
  sig: bsonBinding.Bind(req *http.Request, obj any)
  called_by: ShouldBindWith, Bind

protobufBinding.Bind (binding/protobuf.go:21-21)
  sig: protobufBinding.Bind(req *http.Request, obj any)
  behavior: GUARD(err != nil -> return err)
  called_by: ShouldBindWith, Bind

Data.WriteContentType (render/data.go:29-29)
  WriteContentType (Data) writes custom ContentType.
  sig: Data.WriteContentType(w http.ResponseWriter)
  called_by: Render

Context.hasRequestContext (context.go:1440-1440)
  hasRequestContext returns whether c.Request has Context and fallback.
  calls: Context
  called_by: Deadline, Done, Err, Value

getMapFromFormData (context.go:674-674)
  getMapFromFormData return a map which satisfies conditions.
  sig: getMapFromFormData(m map[string][]string, key string)
  behavior: ACCUMULATE(len loop -> result)
  called_by: GetPostFormMap, GetQueryMap

BindingBody (binding/binding_nomsgpack.go:37-37)
  BindingBody adds BindBody method to Binding.

BindingBody (binding/binding.go:39-39)
  BindingBody adds BindBody method to Binding.

BindingUri (binding/binding.go:46-46)
  BindingUri adds BindUri method to Binding.

BindingUri (binding/binding_nomsgpack.go:44-44)
  BindingUri adds BindUri method to Binding.

Data (render/data.go:13-13)
  Data contains ContentType and bytes data.
  methods: Render, WriteContentType

bsonBinding (binding/bson.go:14-14)
  type bsonBinding
  methods: Bind

headerBinding (binding/header.go:13-13)
  type headerBinding

jsonBinding (binding/json.go:27-27)
  type jsonBinding

msgpackBinding (binding/msgpack.go:17-17)
  type msgpackBinding

plainBinding (binding/plain.go:12-12)
  type plainBinding

protobufBinding (binding/protobuf.go:15-15)
  type protobufBinding
  methods: Bind

queryBinding (binding/query.go:9-9)
  type queryBinding

tomlBinding (binding/toml.go:15-15)
  type tomlBinding

uriBinding (binding/uri.go:7-7)
  type uriBinding

xmlBinding (binding/xml.go:14-14)
  type xmlBinding

yamlBinding (binding/yaml.go:15-15)
  type yamlBinding

Context.SetCookieData (context.go:1128-1128)
  SetCookieData adds a Set-Cookie header to the ResponseWriter's headers.
  sig: Context.SetCookieData(cookie *http.Cookie)
  calls: SetCookie

chooseData (utils.go:100-100)
  sig: chooseData(custom, wildcard any)
  behavior: GUARD(custom != nil -> return custom); PRECEDENCE(custom -> wildcard)
  raises: panic

secureRequestDump (recovery.go:98-98)
  secureRequestDump returns a sanitized HTTP request dump where the Authorization header, if present, is replaced with a m
  sig: secureRequestDump(r *http.Request)
  behavior: DELEGATE(strings.Join -> result); ACCUMULATE(HasPrefix loop -> result)
  called_by: CustomRecoveryWithWriter

formSource.TrySet (binding/form_mapping.go:75-75)
  TrySet tries to set a value by request's form source (like map[string][]string)
  sig: formSource.TrySet(value reflect.Value, field reflect.StructField, tagValue...)
  behavior: DELEGATE(setByForm -> result)
  calls: setByForm
  called_by: tryToSetValue

RouteInfo (gin.go:68-68)
  RouteInfo represents a request route's specification which contains method and path and its handler.

Default (binding/binding.go:95-95)
  Default returns the appropriate Binding instance based on the HTTP method and the content type.
  sig: Default(method, contentType string)
  behavior: GUARD(method == http.MethodGet -> return Form); DISPATCH(contentType)

Default (binding/binding_nomsgpack.go:91-91)
  Default returns the appropriate Binding instance based on the HTTP method and the content type.
  sig: Default(method, contentType string)
  behavior: GUARD(method == "GET" -> return Form); DISPATCH(contentType)

WriteString (render/text.go:33-33)
  WriteString writes data according to its format and write custom ContentType.
  sig: WriteString(w http.ResponseWriter, format string, data []any)
  behavior: GUARD(len(data) > 0 -> return)
  calls: Write
  called_by: Render

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

Context (context.go:61-61)
  Context is the most important part of gin.
  methods: Abort, AbortWithError, AbortWithStatus, AbortWithStatusJSON, AbortWithStatusPureJSON, AddParam
  called_by: ClientIP, Deadline, Done, Err, Value, hasRequestContext

Context.Render (context.go:1152-1152)
  Render writes the response headers and calls render.Render to render data.
  sig: Context.Render(code int, r render.Render)
  behavior: GUARD(!bodyAllowedForStatus(code) -> return)
  calls: Error, Abort, Status, bodyAllowedForStatus, Render, WriteContentType
  called_by: AsciiJSON, BSON, Data, DataFromReader, HTML, IndentedJSON, JSON, JSONP

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 43 with behavior annotations
uncovered: Engine.ServeHTTP, Engine.handleHTTPRequest, Engine.updateRouteTrees, Engine
drill: binding/multipart_form_mapping.go (~1 lines, multipartRequest.TrySet)
drill: gin.go (~1 lines, redirectRequest)
drill: context.go (~1 lines, Context.DataFromReader)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## multipartRequest.TrySet  (binding/multipart_form_mapping.go L27-27)
```
func (r *multipartRequest) TrySet(value reflect.Value, field reflect.StructField, key string, opt setOptions) (bool, error) {
```

## redirectRequest  (gin.go L820-820)
```
func redirectRequest(c *Context) {
```

## Context.DataFromReader  (context.go L1276-1276)
```
func (c *Context) DataFromReader(code int, contentLength int64, contentType string, reader io.Reader, extraHeaders map[string]string) {
```

## setByMultipartFormFile  (binding/multipart_form_mapping.go L35-35)
```
func setByMultipartFormFile(value reflect.Value, field reflect.StructField, files []*multipart.FileHeader) (isSet bool, err error) {
```

## String  (render/text.go L15-15)
```
type String struct {
```

## Render  (render/render.go L10-10)
```
type Render interface {
```

## setArrayOfMultipartFormFiles  (binding/multipart_form_mapping.go L63-63)
```
func setArrayOfMultipartFormFiles(value reflect.Value, field reflect.StructField, files []*multipart.FileHeader) (isSet bool, err error) {
```

## Context.Abort  (context.go L207-207)
```
func (c *Context) Abort() {
```

## Context.AbortWithError  (context.go L238-238)
```
func (c *Context) AbortWithError(code int, err error) *Error {
```

## Context.AbortWithStatus  (context.go L213-213)
```
func (c *Context) AbortWithStatus(code int) {
```

## Context.AbortWithStatusJSON  (context.go L230-230)
```
func (c *Context) AbortWithStatusJSON(code int, jsonObj any) {
```

## Context.AbortWithStatusPureJSON  (context.go L222-222)
```
func (c *Context) AbortWithStatusPureJSON(code int, jsonObj any) {
```

## Context.AddParam  (context.go L512-512)
```
func (c *Context) AddParam(key, value string) {
```

## Context.AsciiJSON  (context.go L1211-1211)
```
func (c *Context) AsciiJSON(code int, obj any) {
```

## Context.BSON  (context.go L1249-1249)
```
func (c *Context) BSON(code int, obj any) {
```

## Context.Bind  (context.go L757-757)
```
func (c *Context) Bind(obj any) error {
```

## Context.BindHeader  (context.go L793-793)
```
func (c *Context) BindHeader(obj any) error {
```

## Context.BindJSON  (context.go L763-763)
```
func (c *Context) BindJSON(obj any) error {
```

## Context.BindPlain  (context.go L788-788)
```
func (c *Context) BindPlain(obj any) error {
```

## Context.BindQuery  (context.go L773-773)
```
func (c *Context) BindQuery(obj any) error {
```

## Context.BindTOML  (context.go L783-783)
```
func (c *Context) BindTOML(obj any) error {
```

## Context.BindUri  (context.go L799-799)
```
func (c *Context) BindUri(obj any) error {
```

## Context.BindXML  (context.go L768-768)
```
func (c *Context) BindXML(obj any) error {
```

## Context.BindYAML  (context.go L778-778)
```
func (c *Context) BindYAML(obj any) error {
```

## Context.ClientIP  (context.go L975-975)
```
func (c *Context) ClientIP() string {
```

## Context.ContentType  (context.go L1036-1036)
```
func (c *Context) ContentType() string {
```

## Context.Cookie  (context.go L1142-1142)
```
func (c *Context) Cookie(name string) (string, error) {
```

## Context.Copy  (context.go L122-122)
```
func (c *Context) Copy() *Context {
```

## Context.Data  (context.go L1268-1268)
```
func (c *Context) Data(code int, contentType string, data []byte) {
```

## Context.Deadline  (context.go L1447-1447)
```
func (c *Context) Deadline() (deadline time.Time, ok bool) {
```

## Context.DefaultPostForm  (context.go L609-609)
```
func (c *Context) DefaultPostForm(key, defaultValue string) string {
```

## Context.DefaultQuery  (context.go L538-538)
```
func (c *Context) DefaultQuery(key, defaultValue string) string {
```

## Context.Delete  (context.go L482-482)
```
func (c *Context) Delete(key any) {
```

## Context.Done  (context.go L1455-1455)
```
func (c *Context) Done() <-chan struct{} {
```

## Context.Err  (context.go L1463-1463)
```
func (c *Context) Err() error {
```

## Context.Error  (context.go L252-252)
```
func (c *Context) Error(err error) *Error {
```

## Context.File  (context.go L1286-1286)
```
func (c *Context) File(filepath string) {
```

## Context.FileAttachment  (context.go L1309-1309)
```
func (c *Context) FileAttachment(filepath, filename string) {
```

## Context.FileFromFS  (context.go L1291-1291)
```
func (c *Context) FileFromFS(filepath string, fs http.FileSystem) {
```

## Context.FormFile  (context.go L698-698)
```
func (c *Context) FormFile(name string) (*multipart.FileHeader, error) {
```

## Context.FullPath  (context.go L177-177)
```
func (c *Context) FullPath() string {
```

## Context.Get  (context.go L288-288)
```
func (c *Context) Get(key any) (value any, exists bool) {
```

## Context.GetBool  (context.go L316-316)
```
func (c *Context) GetBool(key any) bool {
```

## Context.GetDuration  (context.go L386-386)
```
func (c *Context) GetDuration(key any) time.Duration {
```

## Context.GetError  (context.go L391-391)
```
func (c *Context) GetError(key any) error {
```

## Context.GetErrorSlice  (context.go L461-461)
```
func (c *Context) GetErrorSlice(key any) []error {
```

## Context.GetFloat32  (context.go L371-371)
```
func (c *Context) GetFloat32(key any) float32 {
```

## Context.GetFloat32Slice  (context.go L446-446)
```
func (c *Context) GetFloat32Slice(key any) []float32 {
```

## Context.GetFloat64  (context.go L376-376)
```
func (c *Context) GetFloat64(key any) float64 {
```

## Context.GetFloat64Slice  (context.go L451-451)
```
func (c *Context) GetFloat64Slice(key any) []float64 {
```

## Context.GetHeader  (context.go L1089-1089)
```
func (c *Context) GetHeader(key string) string {
```

## Context.GetInt16  (context.go L331-331)
```
func (c *Context) GetInt16(key any) int16 {
```

## Context.GetInt16Slice  (context.go L406-406)
```
func (c *Context) GetInt16Slice(key any) []int16 {
```

## Context.GetInt32  (context.go L336-336)
```
func (c *Context) GetInt32(key any) int32 {
```

## Context.GetInt32Slice  (context.go L411-411)
```
func (c *Context) GetInt32Slice(key any) []int32 {
```

## Context.GetInt64  (context.go L341-341)
```
func (c *Context) GetInt64(key any) int64 {
```

## Context.GetInt64Slice  (context.go L416-416)
```
func (c *Context) GetInt64Slice(key any) []int64 {
```

## Context.GetInt8  (context.go L326-326)
```
func (c *Context) GetInt8(key any) int8 {
```

## Context.GetInt8Slice  (context.go L401-401)
```
func (c *Context) GetInt8Slice(key any) []int8 {
```

## Context.GetInt  (context.go L321-321)
```
func (c *Context) GetInt(key any) int {
```

## Context.GetIntSlice  (context.go L396-396)
```
func (c *Context) GetIntSlice(key any) []int {
```

## Context.GetPostForm  (context.go L624-624)
```
func (c *Context) GetPostForm(key string) (string, bool) {
```

## Context.GetPostFormArray  (context.go L653-653)
```
func (c *Context) GetPostFormArray(key string) (values []string, ok bool) {
```

## Context.GetPostFormMap  (context.go L667-667)
```
func (c *Context) GetPostFormMap(key string) (map[string]string, bool) {
```

## Context.GetQuery  (context.go L554-554)
```
func (c *Context) GetQuery(key string) (string, bool) {
```

## Context.GetQueryArray  (context.go L580-580)
```
func (c *Context) GetQueryArray(key string) (values []string, ok bool) {
```

## Context.GetQueryMap  (context.go L594-594)
```
func (c *Context) GetQueryMap(key string) (map[string]string, bool) {
```

## Context.GetRawData  (context.go L1094-1094)
```
func (c *Context) GetRawData() ([]byte, error) {
```

## Context.GetString  (context.go L311-311)
```
func (c *Context) GetString(key any) string {
```

## Context.GetStringMap  (context.go L466-466)
```
func (c *Context) GetStringMap(key any) map[string]any {
```

## Context.GetStringMapString  (context.go L471-471)
```
func (c *Context) GetStringMapString(key any) map[string]string {
```

## Context.GetStringMapStringSlice  (context.go L476-476)
```
func (c *Context) GetStringMapStringSlice(key any) map[string][]string {
```

## Context.GetStringSlice  (context.go L456-456)
```
func (c *Context) GetStringSlice(key any) []string {
```

## Context.GetTime  (context.go L381-381)
```
func (c *Context) GetTime(key any) time.Time {
```

## Context.GetUint16  (context.go L356-356)
```
func (c *Context) GetUint16(key any) uint16 {
```

## Context.GetUint16Slice  (context.go L431-431)
```
func (c *Context) GetUint16Slice(key any) []uint16 {
```

## Context.GetUint32  (context.go L361-361)
```
func (c *Context) GetUint32(key any) uint32 {
```

## Context.GetUint32Slice  (context.go L436-436)
```
func (c *Context) GetUint32Slice(key any) []uint32 {
```

## Context.GetUint64  (context.go L366-366)
```
func (c *Context) GetUint64(key any) uint64 {
```

## Context.GetUint64Slice  (context.go L441-441)
```
func (c *Context) GetUint64Slice(key any) []uint64 {
```

## Context.GetUint8  (context.go L351-351)
```
func (c *Context) GetUint8(key any) uint8 {
```

## Context.GetUint8Slice  (context.go L426-426)
```
func (c *Context) GetUint8Slice(key any) []uint8 {
```

## Context.GetUint  (context.go L346-346)
```
func (c *Context) GetUint(key any) uint {
```

## Context.GetUintSlice  (context.go L421-421)
```
func (c *Context) GetUintSlice(key any) []uint {
```

## Context.HTML  (context.go L1171-1171)
```
func (c *Context) HTML(code int, name string, obj any) {
```

## Context.Handler  (context.go L167-167)
```
func (c *Context) Handler() HandlerFunc {
```

## Context.HandlerName  (context.go L149-149)
```
func (c *Context) HandlerName() string {
```

## Context.HandlerNames  (context.go L155-155)
```
func (c *Context) HandlerNames() []string {
```

## Context.Header  (context.go L1080-1080)
```
func (c *Context) Header(key, value string) {
```

## Context.IndentedJSON  (context.go L1180-1180)
```
func (c *Context) IndentedJSON(code int, obj any) {
```

## Context.IsAborted  (context.go L199-199)
```
func (c *Context) IsAborted() bool {
```

## Context.IsWebsocket  (context.go L1042-1042)
```
func (c *Context) IsWebsocket() bool {
```

## Context.JSON  (context.go L1205-1205)
```
func (c *Context) JSON(code int, obj any) {
```
--- END SOURCE SNIPPETS ---

QUESTION: What documented rules does Gin follow when binding request data and handling binding failures?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
