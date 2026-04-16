# v2.5 Response: blind-gin-mech-2
Date: 2026-04-16

## Question
What documented rules does Gin follow when binding request data and handling binding failures?

## Answer

The clue file and source snippets reveal a structured binding system with automatic engine selection, two error-handling tiers, pluggable validators, and format-specific data extraction rules.

### 1. Automatic Binding Engine Selection

**`Default`** (`binding/binding.go:95` and `binding_nomsgpack.go:91`): "returns the appropriate Binding instance based on the HTTP method and the content type."
- Behavior: `GUARD(method == http.MethodGet -> return Form); DISPATCH(contentType)`.
- **Rule**: GET requests always use Form binding. For other methods, the Content-Type header determines the binding engine (JSON, XML, BSON, Protobuf, MsgPack, TOML, YAML, etc.).

This is used by `Context.Bind` and `Context.ShouldBind`, which call `ContentType` to determine the Content-Type before selecting the binding.

### 2. Two-Tier Error Handling: MustBind vs ShouldBind

**MustBind tier** — aborts the request on failure:

- **`Context.MustBindWith`** (`context.go:810`): behavior `GUARD(err != nil -> return err)`. Calls `ShouldBindWith` first, then if there's an error, calls `AbortWithError` to abort the request. Called by `Bind`, `BindHeader`, `BindJSON`, `BindPlain`, `BindQuery`, `BindTOML`, `BindXML`, `BindYAML`.
- **`Context.Bind`** (`context.go:757`): behavior `DELEGATE(c.MustBindWith -> result)`. Auto-selects binding engine via `ContentType`.
- **`Context.BindUri`** (`context.go:799`): behavior `GUARD(err := c.ShouldBindUri(obj); err != nil -> return err)`. Also calls `AbortWithError` on failure.

**Rule**: MustBind methods abort the request chain by calling `AbortWithError` (`context.go:238`), which calls `AbortWithStatus()` and `Error()` — attaching the error to the context and preventing subsequent handlers from running.

**ShouldBind tier** — returns error without aborting:

- **`Context.ShouldBindWith`** (`context.go:919`): behavior `DELEGATE(b.Bind -> result)`. Simply delegates to the binding engine and returns the error. Called by `MustBindWith`, `ShouldBind`, and all format-specific `ShouldBind*` shortcuts.
- **`Context.ShouldBind`** (`context.go:838`, from blind-gin-rel-2): behavior `DELEGATE(c.ShouldBindWith -> result)`.
- **`Context.ShouldBindUri`** (`context.go:909`): behavior `DELEGATE(binding.Uri.BindUri -> result); ACCUMULATE(loop -> result)`.
- **`Context.ShouldBindBodyWith`** (`context.go:928`): "stores the request body into the context, and reuse when it is called again." Behavior: `PRECEDENCE(cb -> body)`. This caches the request body so multiple binding attempts don't consume the body stream twice. Called by `ShouldBindBodyWithJSON`, `ShouldBindBodyWithPlain`, `ShouldBindBodyWithTOML`, `ShouldBindBodyWithXML`, `ShouldBindBodyWithYAML`.

**Rule**: ShouldBind methods return the error to the caller, leaving the handler to decide how to respond.

### 3. Binding Engine Implementations

The `Binding` interface (`binding/binding.go:32`): "describes the interface which needs to be implemented for binding the data present in the request." Each implementation handles a specific format:

- `bsonBinding.Bind` (`binding/bson.go:20`): called by `ShouldBindWith` and `Bind`.
- `protobufBinding.Bind` (`binding/protobuf.go:21`): behavior `GUARD(err != nil -> return err)`.
- `jsonBinding` (`binding/json.go:27`), `xmlBinding` (`binding/xml.go:14`), `yamlBinding` (`binding/yaml.go:15`), `tomlBinding` (`binding/toml.go:15`), `plainBinding` (`binding/plain.go:12`), `headerBinding` (`binding/header.go:13`), `queryBinding` (`binding/query.go:9`), `msgpackBinding` (`binding/msgpack.go:17`), `uriBinding` (`binding/uri.go:7`).

**`BindingBody`** (`binding/binding.go:39`): "adds BindBody method to Binding" — for body-based binding.
**`BindingUri`** (`binding/binding.go:46`): "adds BindUri method to Binding" — for URI parameter binding.

### 4. Form Data and Multipart Handling

**`formSource.TrySet`** (`binding/form_mapping.go:75`): behavior `DELEGATE(setByForm -> result)`. Maps form fields to struct fields.

**`multipartRequest.TrySet`** (source snippet, `binding/multipart_form_mapping.go:27`): "tries to set a value by the multipart request with the binding a form file." Behavior: `GUARD(files := r.MultipartForm.File[key]; len(files) -> return setByMultip...)`. Handles file upload binding.

**`setByMultipartFormFile`** (source snippet, `binding/multipart_form_mapping.go:35`): sets a value from multipart file headers.
**`setArrayOfMultipartFormFiles`** (source snippet, `binding/multipart_form_mapping.go:63`): handles arrays of uploaded files.

**`mapFormByTag`** (`binding/form_mapping.go:46`): maps form data to structs using struct tags.

### 5. Validation After Binding

**`defaultValidator.ValidateStruct`** (`binding/default_validator.go:44`, from blind-gin-rel-2): "receives any kind of type, but only performed struct or pointer to struct type." Behavior: `GUARD(obj == nil -> return nil); DISPATCH(value)`.

**`defaultValidator.validateStruct`** (`binding/default_validator.go:76`): behavior `DELEGATE(v.validate.Struct -> result)`. Calls `lazyinit` first, then delegates to the underlying validation engine's `Struct` method, which processes validation tags.

**Rule**: Validation runs automatically after deserialization. Only struct types are validated; nil values return no error.

**`SliceValidationError.Error`** (`binding/default_validator.go:24`): "concatenates all error elements" — handles errors when validating slices.

### 6. Response Writing After Binding

The clue shows response rendering is separate from binding:

**`Context.Render`** (`context.go:1152`): behavior `GUARD(!bodyAllowedForStatus(code) -> return)`. Called by `JSON`, `String`, `BSON`, `Data`, `HTML`, `JSONP`, etc. The Render interface (`render/render.go:10`, source snippet) defines the contract.

**`Context.Data`** (`context.go:1268`): writes raw data with custom ContentType. `Data.Render` (`render/data.go:19`) calls `Header`, `WriteContentType`, and `Write`.

**`Default` binding selection** (`binding/binding.go:95`): behavior `GUARD(method == http.MethodGet -> return Form); DISPATCH(contentType)`. Combined with `Context.Render`, this shows binding (input) and rendering (output) are independently configured.

### What Cannot Be Determined
GAPS lists uncovered: `Engine.ServeHTTP`, `Engine.handleHTTPRequest`, `Engine.updateRouteTrees`, `Engine`. The drill targets show single-line snippets for `multipartRequest.TrySet`, `redirectRequest`, and `Context.DataFromReader`. The exact struct tags recognized for binding (e.g., `form:"name"`, `json:"name"`, `uri:"name"`, `header:"name"`, `binding:"required"`) are not enumerated in the clue. The internal deserialization logic of each concrete binding type (how JSON decoding, XML parsing, etc. handle errors) is not exposed. Whether validation errors are automatically transformed into HTTP error responses in the MustBind path (beyond calling `AbortWithError`) is not fully detailed.
