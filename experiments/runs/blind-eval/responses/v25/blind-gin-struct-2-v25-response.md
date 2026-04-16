# v2.5 Response: blind-gin-struct-2
Date: 2026-04-16

## Question
How do Gin's public context helpers divide request reading, binding, and response writing responsibilities?

## Answer

The clue file shows `Context` (`context.go:61`) is "the most important part of gin," and its methods divide cleanly into three responsibility areas: **request reading**, **binding/validation**, and **response writing**.

### 1. Request Reading Helpers

These methods extract raw data from the incoming request without validation:

**Query parameters:**
- `Context.Query` (`context.go:525`): "returns the keyed url query value if it exists."
- `Context.GetQuery` (`context.go:554`): "like Query(), returns the keyed url query value." Returns a boolean indicating existence.
- `Context.GetQueryArray` (`context.go:580`): "returns a slice of strings for a given query key."
- `Context.DefaultQuery` (referenced in `Context.JSONP` as `DefaultQuery`): returns a default if key is absent.
- `Context.initQueryCache` (`context.go:568`): internal lazy initialization of query cache.

**Form/POST data:**
- `Context.GetPostForm` (`context.go:624`): "like PostForm(key)."
- `Context.GetPostFormArray` (`context.go:653`): "returns a slice of strings for form data."
- `Context.initFormCache` (`context.go:638`): internal lazy initialization of form cache.

**Headers and metadata:**
- `Context.GetHeader` (`context.go:1089`): behavior `DELEGATE(c.requestHeader -> result)`.
- `Context.requestHeader` (`context.go:1050`): behavior `DELEGATE(c.Request.Header.Get -> result)`. Called by `BasicAuthForProxy`, `BasicAuthForRealm`, `ClientIP`, `ContentType`, `GetHeader`, `IsWebsocket`, `NegotiateFormat`.
- `Context.ContentType` (`context.go:1036`): "returns the Content-Type header of the request."
- `Context.ClientIP` (`context.go:975`): "implements one best effort algorithm to return the real client IP."
- `Context.IsWebsocket` (`context.go:1042`): behavior `GUARD(strings.Contains(...) -> return true)`.

**Path parameters:**
- `Params.Get` (`tree.go:29`): "returns the value of the first Param which key matches."

**Context key-value store:**
- `Context.Get` (`context.go:288`): "returns the value for the given key."
- `Context.Set` (`context.go:276`): "store a new key/value pair exclusively for this context." Behavior: `UNWIND(defer)` (mutex-protected).
- `Context.Value` (`context.go:1473`): behavior `GUARD(key == ContextRequestKey -> return c.Request); PRECEDENCE(key -> keyAsString)`.

### 2. Binding/Validation Helpers

Two tiers exist: **Must** (aborts on error) and **Should** (returns error):

**MustBind tier** (aborts the request on failure):
- `Context.Bind` (`context.go:757`): "checks the Method and Content-Type to select a binding engine automatically." Behavior: `DELEGATE(c.MustBindWith -> result)`. Calls `ContentType` then `MustBindWith`.
- `Context.MustBindWith` (`context.go:810`): behavior `GUARD(err != nil -> return err)`. Calls `AbortWithError` and `ShouldBindWith`. Called by `Bind`, `BindHeader`, `BindJSON`, `BindPlain`, `BindQuery`, `BindTOML`, `BindXML`, `BindYAML`.
- Format-specific shortcuts: `BindJSON` (`context.go:763`), `BindQuery` (`context.go:773`), `BindPlain` (`context.go:788`), `BindHeader` (`context.go:793`), `BindTOML` (`context.go:783`) — all delegate to `MustBindWith`.
- `Context.BindUri` (`context.go:799`): behavior `GUARD(err -> return err)`. Calls `AbortWithError` and `ShouldBindUri`.

**ShouldBind tier** (returns error without aborting):
- `Context.ShouldBindWith` (`context.go:919`): behavior `DELEGATE(b.Bind -> result)`. Called by `MustBindWith`, `ShouldBind`, `ShouldBindHeader`, `ShouldBindJSON`, `ShouldBindPlain`, `ShouldBindQuery`, `ShouldBindTOML`, `ShouldBindXML`.
- `Context.ShouldBindBodyWith` (`context.go:928`): "stores the request body into the context, and reuse when it is called again." Behavior: `PRECEDENCE(cb -> body)`. Called by `ShouldBindBodyWithJSON`, `ShouldBindBodyWithPlain`, `ShouldBindBodyWithTOML`, `ShouldBindBodyWithXML`, `ShouldBindBodyWithYAML`.
- `Context.ShouldBindUri` (`context.go:909`): behavior `DELEGATE(binding.Uri.BindUri -> result); ACCUMULATE(loop -> result)`.

**Binding interface** (`binding/binding.go:32`): "describes the interface which needs to be implemented for binding the data present in the request." Extended by `BindingBody` (adds `BindBody`) and `BindingUri` (adds `BindUri`).

### 3. Response Writing Helpers

**Core render method:**
- `Context.Render` (`context.go:1152`): "writes the response headers and calls render.Render to render data." Behavior: `GUARD(!bodyAllowedForStatus(code) -> return)`. Called by all format-specific response methods.

**Format-specific writers:**
- `Context.JSON` (`context.go:1205`): "serializes the given struct as JSON into the response body." Calls `Render`.
- `Context.PureJSON` (`context.go:1217`): serializes without HTML escaping. Calls `Render`.
- `Context.JSONP` (`context.go:1194`): behavior `GUARD(callback == "" -> return)`. Calls `DefaultQuery` and `Render`.
- `Context.String` (`context.go:1254`): "writes the given string into the response body." Calls `Render`.
- `Context.BSON` (`context.go:1249`): serializes as BSON. Calls `Render`.
- `Context.File` (`context.go:1286`): "writes the specified file into the body stream."
- `Context.Stream` (`context.go:1328`): "sends a streaming response." Behavior: `ACCUMULATE(step loop -> result)`. Calls `CloseNotify` and `Flush`.

**Response control:**
- `Context.Header` (`context.go:1080`): "intelligent shortcut for c.Writer."
- `Context.Abort` (`context.go:207`): "prevents pending handlers from being called."
- `Context.AbortWithStatus` (`context.go:213`): calls `Abort()` and writes the status code.
- `Context.AbortWithError` (`context.go:238`): calls `AbortWithStatus()` and `Error()`.
- `Context.AbortWithStatusJSON` / `AbortWithStatusPureJSON`: abort with JSON body.
- `Context.Error` (`context.go:252`): "attaches an error to the current context." Behavior: `GUARD(err == nil -> panic("err is nil"))`.
- `Context.Copy` (`context.go:122`): "returns a copy of the current context that can be safely used outside the request's scope."

**Underlying writer:**
- `responseWriter` (`response_writer.go:49`): type with methods `Write`, `WriteHeader`, `WriteHeaderNow`, `WriteString`, `Status`, `Written`, `Flush`, `Hijack`, `CloseNotify`, `Pusher`.

### What Cannot Be Determined
GAPS lists uncovered: `Context.Delete`, `Context.HandlerNames`, `Context.IsAborted`, `Context.RemoteIP`. The full set of response negotiation methods (e.g., `Negotiate`, `NegotiateFormat`) is not detailed. The `GetPostFormMap` and `GetQueryMap` implementations are referenced only indirectly via `getMapFromFormData`.
