# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: blind-fastapi-mech-2

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.

--- CLUE FILE (File 1) ---
=CC v2.1 fastapi@HEAD 1118mod 5241sym
? How does FastAPI turn raised exceptions and validation failures into HTTP responses?


-- TREE
docs_src/  (454 files)
  additional_responses/  additional_status_codes/  advanced_middleware/  app_testing/  async_tests/  authentication_error_status_code/  background_tasks/  behind_a_proxy/  bigger_applications/  body/  ...+66
fastapi/  (48 files)
  _compat/  dependencies/  middleware/  openapi/  security/
scripts/  (35 files)
tests/  (581 files)
  benchmarks/  test_modules_same_name_body/  test_request_params/  test_tutorial/  test_validate_response_recursive/

-- INDEX
docs_src/additional_responses/__init__.py         0L  
docs_src/additional_responses/tutorial001_py310.py    22L  Item, Message, read_item
docs_src/additional_responses/tutorial002_py310.py    28L  Item, read_item
docs_src/additional_responses/tutorial003_py310.py    37L  Item, Message, read_item
docs_src/additional_responses/tutorial004_py310.py    30L  Item, read_item
docs_src/additional_status_codes/__init__.py      0L  
docs_src/additional_status_codes/tutorial001_an_py310.py    25L  upsert_item
docs_src/additional_status_codes/tutorial001_py310.py    23L  upsert_item
docs_src/advanced_middleware/__init__.py          0L  
docs_src/advanced_middleware/tutorial001_py310.py    11L  main
docs_src/advanced_middleware/tutorial002_py310.py    13L  main
docs_src/advanced_middleware/tutorial003_py310.py    11L  main
docs_src/app_testing/__init__.py                  0L  
docs_src/app_testing/app_a_py310/__init__.py      0L  
docs_src/app_testing/app_a_py310/main.py          8L  read_main
docs_src/app_testing/app_a_py310/test_main.py    11L  test_read_main
docs_src/app_testing/app_b_an_py310/__init__.py     0L  
docs_src/app_testing/app_b_an_py310/main.py      38L  Item, create_item, read_main
docs_src/app_testing/app_b_an_py310/test_main.py    65L  test_create_existing_item, test_create_item, test_create_item_bad_token, test_read_item, test_read_item_bad_token
docs_src/app_testing/app_b_py310/__init__.py      0L  
  ...and 1098 more modules

-- SYM
api_route                           M fastapi/routing.py:1415   function api_route
lenient_issubclass                  M fastapi/_compat/shared.py:47     function lenient_issubclass
add_api_route                       M fastapi/routing.py:1332   function add_api_route
_impartial                          M fastapi/dependencies/models.py:25     function _impartial
_serialize_data                     M fastapi/routing.py:467    function _serialize_data
get_graphql_response                M scripts/notify_translations.py:198    function get_graphql_response
read_image                          M docs_src/stream_data/tutorial002_py310.py:12     function read_image
get_langs                           M scripts/translate.py:36     function get_langs
get_flat_models_from_model          M fastapi/_compat/v2.py:424    function get_flat_models_from_model
make_not_authenticated_error        M fastapi/security/api_key.py:29     The WWW-Authenticate header is not standardized...
get_lang_paths                      M scripts/docs.py:102    function get_lang_paths
ModelField                          C fastapi/_compat/v2.py:101    class ModelField
_unwrapped_call                     M fastapi/dependencies/models.py:18     function _unwrapped_call
get                                 M fastapi/applications.py:1564   Add a *path operation* using an HTTP GET operat...
_annotation_is_sequence             M fastapi/_compat/shared.py:58     function _annotation_is_sequence
body                                M docs_src/custom_request_and_route/tutorial001_an_py310.py:10     async_function body
body                                M docs_src/custom_request_and_route/tutorial001_py310.py:9      async_function body
get_model_fields                    M fastapi/_compat/v2.py:382    function get_model_fields
get_flat_models_from_field          M fastapi/_compat/v2.py:449    function get_flat_models_from_field
get_default                         M fastapi/_compat/v2.py:155    function get_default
generate_lang_path                  M scripts/translate.py:40     function generate_lang_path
UserInDB                            C docs_src/security/tutorial003_an_py310.py:41     class UserInDB
UserInDB                            C docs_src/security/tutorial003_py310.py:39     class UserInDB
check_api_key                       M fastapi/security/api_key.py:45     function check_api_key
make_not_authenticated_error        M fastapi/security/oauth2.py:401    The OAuth 2 specification doesn't define the ch...
GzipRequest                         C docs_src/custom_request_and_route/tutorial001_an_py310.py:9      class GzipRequest
GzipRequest                         C docs_src/custom_request_and_route/tutorial001_py310.py:8      class GzipRequest
_add_lang_code_to_url               M scripts/doc_parsing_utils.py:279    function _add_lang_code_to_url
get_flat_models_from_fields         M fastapi/_compat/v2.py:465    function get_flat_models_from_fields
get_validation_alias                M fastapi/dependencies/utils.py:1052   function get_validation_alias
iter_all_en_paths                   M scripts/translate.py:151    Iterate on the markdown files to translate in o...
generate_en_path                    M scripts/translate.py:50     function generate_en_path
EnFile                              C scripts/mkdocs_hooks.py:48     class EnFile
make_not_authenticated_error        M fastapi/security/http.py:87     function make_not_authenticated_error
_serialize_item                     M fastapi/routing.py:620    function _serialize_item
_annotation_is_complex              M fastapi/_compat/shared.py:80     function _annotation_is_complex
_serialize_sse_item                 M fastapi/routing.py:496    function _serialize_sse_item
get                                 M fastapi/routing.py:1827   Add a *path operation* using an HTTP GET operat...
APIWebSocketRoute                   C fastapi/routing.py:765    class APIWebSocketRoute
_regenerate_error_with_loc          M fastapi/_compat/v2.py:473    function _regenerate_error_with_loc
asdict                              M fastapi/_compat/v2.py:87     function asdict
get_en_config                       M scripts/docs.py:98     function get_en_config
get_graphql_response                M scripts/sponsors.py:92     function get_graphql_response
_AsyncLiftContextManager            C fastapi/routing.py:165    Wraps a synchronous context manager to make it ...
User                                C docs_src/graphql_/tutorial001_py310.py:7      class User
_format_endpoint_context            M fastapi/exceptions.py:193    function _format_endpoint_context
make_not_authenticated_error        M fastapi/security/open_id_connect_url.py:80     function make_not_authenticated_error
add_permalinks_page                 M scripts/docs.py:650    Add or update header permalinks in specific pag...
get_llm_translatable                M scripts/translate.py:212    function get_llm_translatable
CodeIncludeInfo                     C scripts/doc_parsing_utils.py:37     class CodeIncludeInfo
iter_en_paths_to_translate          M scripts/translate.py:175    function iter_en_paths_to_translate
get_graphql_response                M scripts/contributors.py:121    function get_graphql_response
get_flat_models_from_annotation     M fastapi/_compat/v2.py:433    function get_flat_models_from_annotation
list_removable                      M scripts/translate.py:272    function list_removable
resolve_file                        M scripts/mkdocs_hooks.py:63     function resolve_file
User                                C docs_src/security/tutorial002_an_py310.py:12     class User
User                                C docs_src/security/tutorial002_py310.py:10     class User
get_user                            M docs_src/security/tutorial003_an_py310.py:45     function get_user
get_user                            M docs_src/security/tutorial003_py310.py:43     function get_user
remove_header_permalinks            M scripts/docs.py:196    function remove_header_permalinks
UserInDB                            C docs_src/security/tutorial004_an_py310.py:45     class UserInDB
UserInDB                            C docs_src/security/tutorial004_py310.py:44     class UserInDB
UserInDB                            C docs_src/security/tutorial005_an_py310.py:57     class UserInDB
UserInDB                            C docs_src/security/tutorial005_py310.py:56     class UserInDB
__init__                            M scripts/docs.py:72     function __init__
translate_page                      M scripts/translate.py:61     function translate_page
field_annotation_is_sequence        M fastapi/_compat/shared.py:64     function field_annotation_is_sequence
field_annotation_is_complex         M fastapi/_compat/shared.py:88     function field_annotation_is_complex
add_event_handler                   M fastapi/routing.py:4901   Add an event handler function for startup or sh...
HTMLLinkAttribute                   C scripts/doc_parsing_utils.py:58     class HTMLLinkAttribute
update_languages                    M scripts/docs.py:275    Update the mkdocs.yml file Languages section in...
process_one_page                    M scripts/translation_fixer.py:65     Fix one translated document by comparing it to ...
get_request_handler                 M fastapi/routing.py:347    function get_request_handler
  ...and 1368 more symbols

-- FOCUS
RequestValidationError (fastapi/exceptions.py:212-221)
  extends: ValidationException
  imports: annotated_doc, pydantic, starlette.exceptions

ResponseValidationError (fastapi/exceptions.py:234-243)
  extends: ValidationException
  imports: annotated_doc, pydantic, starlette.exceptions

ValidationException (fastapi/exceptions.py:174-209)
  extends: Exception
  imports: annotated_doc, pydantic, starlette.exceptions
  calls: _format_endpoint_context

WebSocketRequestValidationError (fastapi/exceptions.py:224-231)
  extends: ValidationException
  imports: annotated_doc, pydantic, starlette.exceptions

http_exception_handler (fastapi/exception_handlers.py:11-17)
  sig: http_exception_handler(request, exc)
  uses: JSONResponse (starlette.responses), Response (starlette.responses)

request_validation_exception_handler (fastapi/exception_handlers.py:20-26)
  sig: request_validation_exception_handler(request, exc)
  behavior: DELEGATE(JSONResponse -> result)
  uses: JSONResponse (starlette.responses)

get_validation_alias (fastapi/dependencies/utils.py:1052-1054)
  sig: get_validation_alias(field)
  called_by: _extract_form_body, _get_multidict_value, request_body_to_args, request_params_to_args

validation_alias (fastapi/_compat/v2.py:113-117)

websocket_request_validation_exception_handler (fastapi/exception_handlers.py:29-34)
  sig: websocket_request_validation_exception_handler(websocket, exc)

custom_http_exception_handler (docs_src/handling_errors/tutorial006_py310.py:13-15)
  sig: custom_http_exception_handler(request, exc)
  behavior: DELEGATE(http_exception_handler -> result)

http_exception_handler (docs_src/handling_errors/tutorial004_py310.py:10-11)
  sig: http_exception_handler(request, exc)
  behavior: DELEGATE(PlainTextResponse -> result)
  uses: PlainTextResponse (fastapi.responses)

validation_exception_handler (docs_src/handling_errors/tutorial005_py310.py:11-15)
  sig: validation_exception_handler(request, exc)
  behavior: DELEGATE(JSONResponse -> result)
  uses: JSONResponse (fastapi.responses)

validation_exception_handler (docs_src/handling_errors/tutorial006_py310.py:19-21)
  sig: validation_exception_handler(request, exc)
  behavior: DELEGATE(request_validation_exception_handler -> result)

validation_exception_handler (docs_src/handling_errors/tutorial004_py310.py:15-19)
  sig: validation_exception_handler(request, exc)
  behavior: ACCUMULATE(exc.errors() loop -> message)
  uses: PlainTextResponse (fastapi.responses)

ValidationErrorLoggingRoute (docs_src/custom_request_and_route/tutorial002_py310.py:8-20)
  extends: APIRoute
  imports: fastapi, fastapi.exceptions, fastapi.routing
  calls: get_route_handler
  raises: HTTPException
  uses: HTTPException (fastapi)

ValidationErrorLoggingRoute (docs_src/custom_request_and_route/tutorial002_an_py310.py:9-21)
  extends: APIRoute
  imports: fastapi, fastapi.exceptions, fastapi.routing
  calls: get_route_handler
  raises: HTTPException
  uses: HTTPException (fastapi)

redirect_fastapi (docs_src/custom_response/tutorial006b_py310.py:8-9)

HTTPBasic (fastapi/security/http.py:105-219)
  HTTP Basic authentication.
  extends: HTTPBase
  imports: binascii, base64, annotated_doc, fastapi.exceptions, fastapi.openapi.models
  calls: make_not_authenticated_error, HTTPBasicCredentials
  raises: make_not_authenticated_error
  uses: HTTPException (fastapi.exceptions)

HTTPAuthorizationCredentials (fastapi/security/http.py:29-66)
  The HTTP authorization credentials in the result of using `HTTPBearer` or
  extends: BaseModel
  imports: binascii, base64, annotated_doc, fastapi.exceptions, fastapi.openapi.models
  called_by: HTTPBase, HTTPBearer, HTTPDigest

HTTPBearer (fastapi/security/http.py:222-316)
  HTTP Bearer token authentication.
  extends: HTTPBase
  imports: binascii, base64, annotated_doc, fastapi.exceptions, fastapi.openapi.models
  calls: HTTPAuthorizationCredentials, make_not_authenticated_error
  raises: make_not_authenticated_error
  uses: HTTPException (fastapi.exceptions)

HTTPDigest (fastapi/security/http.py:319-417)
  HTTP Digest authentication.
  extends: HTTPBase
  imports: binascii, base64, annotated_doc, fastapi.exceptions, fastapi.openapi.models
  calls: HTTPAuthorizationCredentials, make_not_authenticated_error
  raises: make_not_authenticated_error
  uses: HTTPException (fastapi.exceptions)

HTTPBasicCredentials (fastapi/security/http.py:16-26)
  The HTTP Basic credentials given as the result of using `HTTPBasic` in a
  extends: BaseModel
  imports: binascii, base64, annotated_doc, fastapi.exceptions, fastapi.openapi.models
  called_by: HTTPBasic

HTTPException (fastapi/exceptions.py:17-83)
  An HTTP exception you can raise in your own code to show errors to the client.
  extends: StarletteHTTPException
  imports: annotated_doc, pydantic, starlette.exceptions

FastAPI (fastapi/applications.py:45-4693)
  `FastAPI` app class, the main entrypoint to use FastAPI.
  extends: Starlette
  imports: enum, annotated_doc, fastapi, fastapi.datastructures, fastapi.exception_handlers
  calls: __call__, add_api_route, add_api_websocket_route, delete, get, head, include_router, on_event
  uses: Default (fastapi.datastructures), Doc (annotated_doc), JSONResponse (starlette.responses)

get (fastapi/routing.py:1827-2204)
  Add a *path operation* using an HTTP GET operation.
  sig: get(path)
  behavior: DELEGATE(api_route -> result)
  calls: api_route
  called_by: APIRoute, get_request_handler, get_websocket_app
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

get (fastapi/applications.py:1564-1937)
  Add a *path operation* using an HTTP GET operation.
  sig: get(path)
  behavior: DELEGATE(router.get -> result)
  called_by: redoc_html, swagger_ui_html, setup, FastAPI
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

delete (fastapi/routing.py:2968-3345)
  Add a *path operation* using an HTTP DELETE operation.
  sig: delete(path)
  behavior: DELEGATE(api_route -> result)
  calls: api_route
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

delete (fastapi/applications.py:2693-3066)
  Add a *path operation* using an HTTP DELETE operation.
  sig: delete(path)
  behavior: DELEGATE(router.delete -> result)
  called_by: FastAPI
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

head (fastapi/routing.py:3722-4104)
  Add a *path operation* using an HTTP HEAD operation.
  sig: head(path)
  behavior: DELEGATE(api_route -> result)
  calls: api_route
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

head (fastapi/applications.py:3439-3812)
  Add a *path operation* using an HTTP HEAD operation.
  sig: head(path)
  behavior: DELEGATE(router.head -> result)
  called_by: FastAPI
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

options (fastapi/routing.py:3345-3722)
  Add a *path operation* using an HTTP OPTIONS operation.
  sig: options(path)
  behavior: DELEGATE(api_route -> result)
  calls: api_route
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

options (fastapi/applications.py:3066-3439)
  Add a *path operation* using an HTTP OPTIONS operation.
  sig: options(path)
  behavior: DELEGATE(router.options -> result)
  called_by: FastAPI
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

patch (fastapi/routing.py:4104-4486)
  Add a *path operation* using an HTTP PATCH operation.
  sig: patch(path)
  behavior: DELEGATE(api_route -> result)
  calls: api_route
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

patch (fastapi/applications.py:3812-4190)
  Add a *path operation* using an HTTP PATCH operation.
  sig: patch(path)
  behavior: DELEGATE(router.patch -> result)
  called_by: FastAPI
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 36 with behavior annotations
uncovered: DependencyScopeError, EndpointContext, ORJSONResponse, PydanticV1NotSupportedError
drill: fastapi/dependencies/utils.py (~3 lines, get_validation_alias)
drill: fastapi/exception_handlers.py (~9 lines, http_exception_handler)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## get_validation_alias  (fastapi/dependencies/utils.py L1052-1054)
```
def get_validation_alias(field: ModelField) -> str:
    va = getattr(field, "validation_alias", None)
    return va or field.alias
```

## http_exception_handler  (tests/test_exception_handlers.py L8-9)
```
def http_exception_handler(request, exception):
    return JSONResponse({"exception": "http-exception"})
```

## request_validation_exception_handler  (tests/test_exception_handlers.py L12-13)
```
def request_validation_exception_handler(request, exception):
    return JSONResponse({"exception": "request-validation"})
```

## websocket_request_validation_exception_handler  (fastapi/exception_handlers.py L29-34)
```
async def websocket_request_validation_exception_handler(
    websocket: WebSocket, exc: WebSocketRequestValidationError
) -> None:
    await websocket.close(
        code=WS_1008_POLICY_VIOLATION, reason=jsonable_encoder(exc.errors())
    )
```

## ParamDetails  (fastapi/dependencies/utils.py L384-387)
```
class ParamDetails:
    type_annotation: Any
    depends: params.Depends | None
    field: ModelField | None
```

## SolvedDependency  (fastapi/dependencies/utils.py L587-592)
```
class SolvedDependency:
    values: dict[str, Any]
    errors: list[Any]
    background_tasks: StarletteBackgroundTasks | None
    response: Response
    dependency_cache: dict[DependencyCacheKey, Any]
```

## _extract_form_body  (fastapi/dependencies/utils.py L909-945)
```
async def _extract_form_body(
    body_fields: list[ModelField],
    received_body: FormData,
) -> dict[str, Any]:
    values = {}

    for field in body_fields:
        value = _get_multidict_value(field, received_body)
        field_info = field.field_info
        if (
            isinstance(field_info, params.File)
            and is_bytes_or_nonable_bytes_annotation(field.field_info.annotation)
            and isinstance(value, UploadFile)
        ):
            value = await value.read()
        elif (
            is_bytes_sequence_annotation(field.field_info.annotation)
            and isinstance(field_info, params.File)
            and value_is_sequence(value)
        ):
            # For types
            assert isinstance(value, sequence_types)
            results: list[bytes | str] = []
            for sub_value in value:
                results.append(await sub_value.read())
            value = serialize_sequence_value(field=field, value=results)
        if value is not None:
            values[get_validation_alias(field)] = value
    field_aliases = {get_validation_alias(field) for field in body_fields}
    for key in received_body.keys():
        if key not in field_aliases:
            param_values = received_body.getlist(key)
            if len(param_values) == 1:
                values[key] = param_values[0]
            else:
                values[key] = param_values
    return values
```

## _get_flat_fields_from_params  (fastapi/dependencies/utils.py L190-199)
```
def _get_flat_fields_from_params(fields: list[ModelField]) -> list[ModelField]:
    if not fields:
        return fields
    first_field = fields[0]
    if len(fields) == 1 and lenient_issubclass(
        first_field.field_info.annotation, BaseModel
    ):
        fields_to_extract = get_cached_model_fields(first_field.field_info.annotation)
        return fields_to_extract
    return fields
```

## _get_multidict_value  (fastapi/dependencies/utils.py L750-778)
```
def _get_multidict_value(
    field: ModelField, values: Mapping[str, Any], alias: str | None = None
) -> Any:
    alias = alias or get_validation_alias(field)
    if (
        (not _is_json_field(field))
        and field_annotation_is_sequence(field.field_info.annotation)
        and isinstance(values, (ImmutableMultiDict, Headers))
    ):
        value = values.getlist(alias)
    else:
        value = values.get(alias, None)
    if (
        value is None
        or (
            isinstance(field.field_info, params.Form)
            and isinstance(value, str)  # For type checks
            and value == ""
        )
        or (
            field_annotation_is_sequence(field.field_info.annotation)
            and len(value) == 0
        )
    ):
        if field.field_info.is_required():
            return
        else:
            return deepcopy(field.default)
    return value
```

## _get_signature  (fastapi/dependencies/utils.py L211-223)
```
def _get_signature(call: Callable[..., Any]) -> inspect.Signature:
    try:
        signature = inspect.signature(call, eval_str=True)
    except NameError:
        # Handle type annotations with if TYPE_CHECKING, not used by FastAPI
        # e.g. dependency return types
        if sys.version_info >= (3, 14):
            from annotationlib import Format

            signature = inspect.signature(call, annotation_format=Format.FORWARDREF)
        else:
            signature = inspect.signature(call)
    return signature
```

## _is_json_field  (fastapi/dependencies/utils.py L746-747)
```
def _is_json_field(field: ModelField) -> bool:
    return any(type(item) is Json for item in field.field_info.metadata)
```

## _should_embed_body_fields  (fastapi/dependencies/utils.py L885-906)
```
def _should_embed_body_fields(fields: list[ModelField]) -> bool:
    if not fields:
        return False
    # More than one dependency could have the same field, it would show up as multiple
    # fields but it's the same one, so count them by name
    body_param_names_set = {field.name for field in fields}
    # A top level field has to be a single field, not multiple
    if len(body_param_names_set) > 1:
        return True
    first_field = fields[0]
    # If it explicitly specifies it is embedded, it has to be embedded
    if getattr(first_field.field_info, "embed", None):
        return True
    # If it's a Form (or File) field, it has to be a BaseModel (or a union of BaseModels) to be top level
    # otherwise it has to be embedded, so that the key value pair can be extracted
    if (
        isinstance(first_field.field_info, params.Form)
        and not lenient_issubclass(first_field.field_info.annotation, BaseModel)
        and not is_union_of_base_models(first_field.field_info.annotation)
    ):
        return True
    return False
```

## _solve_generator  (fastapi/dependencies/utils.py L575-583)
```
async def _solve_generator(
    *, dependant: Dependant, stack: AsyncExitStack, sub_values: dict[str, Any]
) -> Any:
    assert dependant.call
    if dependant.is_async_gen_callable:
        cm = asynccontextmanager(dependant.call)(**sub_values)
    elif dependant.is_gen_callable:
        cm = contextmanager_in_threadpool(contextmanager(dependant.call)(**sub_values))
    return await stack.enter_async_context(cm)
```

## _validate_value_with_model_field  (fastapi/dependencies/utils.py L735-743)
```
def _validate_value_with_model_field(
    *, field: ModelField, value: Any, values: dict[str, Any], loc: tuple[str, ...]
) -> tuple[Any, list[Any]]:
    if value is None:
        if field.field_info.is_required():
            return None, [get_missing_field_error(loc=loc)]
        else:
            return deepcopy(field.default), []
    return field.validate(value, values, loc=loc)
```

## add_non_field_param_to_dependency  (fastapi/dependencies/utils.py L359-380)
```
def add_non_field_param_to_dependency(
    *, param_name: str, type_annotation: Any, dependant: Dependant
) -> bool | None:
    if lenient_issubclass(type_annotation, Request):
        dependant.request_param_name = param_name
        return True
    elif lenient_issubclass(type_annotation, WebSocket):
        dependant.websocket_param_name = param_name
        return True
    elif lenient_issubclass(type_annotation, HTTPConnection):
        dependant.http_connection_param_name = param_name
        return True
    elif lenient_issubclass(type_annotation, Response):
        dependant.response_param_name = param_name
        return True
    elif lenient_issubclass(type_annotation, StarletteBackgroundTasks):
        dependant.background_tasks_param_name = param_name
        return True
    elif lenient_issubclass(type_annotation, SecurityScopes):
        dependant.security_scopes_param_name = param_name
        return True
    return None
```

## add_param_to_fields  (fastapi/dependencies/utils.py L559-572)
```
def add_param_to_fields(*, field: ModelField, dependant: Dependant) -> None:
    field_info = field.field_info
    field_info_in = getattr(field_info, "in_", None)
    if field_info_in == params.ParamTypes.path:
        dependant.path_params.append(field)
    elif field_info_in == params.ParamTypes.query:
        dependant.query_params.append(field)
    elif field_info_in == params.ParamTypes.header:
        dependant.header_params.append(field)
    else:
        assert field_info_in == params.ParamTypes.cookie, (
            f"non-body parameters must be in path, query, header or cookie: {field.name}"
        )
        dependant.cookie_params.append(field)
```

## analyze_param  (fastapi/dependencies/utils.py L390-556)
```
def analyze_param(
    *,
    param_name: str,
    annotation: Any,
    value: Any,
    is_path_param: bool,
) -> ParamDetails:
    field_info = None
    depends = None
    type_annotation: Any = Any
    use_annotation: Any = Any
    if is_typealiastype(annotation):
        # unpack in case PEP 695 type syntax is used
        annotation = annotation.__value__
    if annotation is not inspect.Signature.empty:
        use_annotation = annotation
        type_annotation = annotation
    # Extract Annotated info
    if get_origin(use_annotation) is Annotated:
        annotated_args = get_args(annotation)
        type_annotation = annotated_args[0]
        fastapi_annotations = [
            arg
            for arg in annotated_args[1:]
            if isinstance(arg, (FieldInfo, params.Depends))
        ]
        fastapi_specific_annotations = [
            arg
            for arg in fastapi_annotations
            if isinstance(
                arg,
                (
                    params.Param,
                    params.Body,
                    params.Depends,
                ),
            )
        ]
        if fastapi_specific_annotations:
            fastapi_annotation: FieldInfo | params.Depends | None = (
                fastapi_specific_annotations[-1]
            )
        else:
            fastapi_annotation = None
        # Set default for Annotated FieldInfo
        if isinstance(fastapi_annotation, FieldInfo):
            # Copy `field_info` because we mutate `field_info.default` below.
            field_info = copy_field_info(
                field_info=fastapi_annotation,
                annotation=use_annotation,
            )
            assert (
                field_info.default == Undefined or field_info.default == RequiredParam
            ), (
                f"`{field_info.__class__.__name__}` default value cannot be set in"
                f" `Annotated` for {param_name!r}. Set the default value with `=` instead."
            )
            if value is not inspect.Signature.empty:
                assert not is_path_param, "Path parameters cannot have default values"
                field_info.default = value
            else:
                field_info.default = RequiredParam
        # Get Annotated Depends
        elif isinstance(fastapi_annotation, params.Depends):
            depends = fastapi_annotation
    # Get Depends from default value
    if isinstance(value, params.Depends):
        assert depends is None, (
            "Cannot specify `Depends` in `Annotated` and default value"
            f" together for {param_name!r}"
        )
        assert field_info is None, (
            "Cannot specify a FastAPI annotation in `Annotated` and `Depends` as a"
            f" default value together for {param_name!r}"
        )
        depends = value
    # Get FieldInfo from default value
    elif isinstance(value, FieldInfo):
        assert field_info is None, (
            "Cannot specify FastAPI annotations in `Annotated` and default value"
            f" together for {param_name!r}"
        )
        field_info = value
        if isinstance(field_info, FieldInfo):
            field_info.annotation = type_annotation

    # Get Depends from type annotation
    if depends is not None and depends.dependency is None:
        # Copy `depends` before mutating it
        depends = copy(depends)
        depends = dataclasses.replace(depends, dependency=type_annotation)

    # Handle non-param type annotations like Request
    # Only apply special handling when there's no explicit Depends - if there's a Depends,
    # the dependency will be called and its return value used instead of the special injection
    if depends is None and lenient_issubclass(
        type_annotation,
        (
            Request,
            WebSocket,
            HTTPConnection,
            Response,
            StarletteBackgroundTasks,
            SecurityScopes,
        ),
    ):
        assert field_info is None, (
            f"Cannot specify FastAPI annotation for type {type_annotation!r}"
        )
    # Handle default assignations, neither field_info nor depends was not found in Annotated nor default value
    elif field_info is None and depends is None:
        default_value = value if value is not inspect.Signature.empty else RequiredParam
        if is_path_param:
            # We might check here that `default_value is RequiredParam`, but the fact is that the same
            # parameter might sometimes be a path parameter and sometimes not. See
            # `tests/test_infer_param_optionality.py` for an example.
            field_info = params.Path(annotation=use_annotation)
        elif is_uploadfile_or_nonable_uploadfile_annotation(
            type_annotation
... (truncated)
```
--- END SOURCE SNIPPETS ---

QUESTION: How does FastAPI turn raised exceptions and validation failures into HTTP responses?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
