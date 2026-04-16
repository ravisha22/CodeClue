# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: blind-fastapi-mech-1

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.

--- CLUE FILE (File 1) ---
=CC v2.1 fastapi@HEAD 1118mod 5241sym
? When one FastAPI endpoint mixes path, query, and body inputs, how does the framework decide where each value comes from and how invalid data is reported?


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
get_body_field (fastapi/dependencies/utils.py:998-1049)
  Get a ModelField representing the request body for a path operation, combining

_check_data_exclusive (fastapi/sse.py:136-143)
  behavior: GUARD(self.data is not None and self.raw_data is not None -> raise ValueErro...)
  raises: ValueError

_extract_endpoint_context (fastapi/routing.py:250-270)
  Extract endpoint context with caching to avoid repeated file I/O.
  sig: _extract_endpoint_context(func)
  called_by: get_request_handler, get_websocket_app
  uses: EndpointContext (fastapi.exceptions)

request_body_to_args (fastapi/dependencies/utils.py:948-995)
  sig: request_body_to_args(body_fields, received_body, embed_body_fields)
  behavior: ACCUMULATE(body_fields loop -> errors)
  calls: _extract_form_body, _validate_value_with_model_field, get_validation_alias
  called_by: solve_dependencies

_extract_form_body (fastapi/dependencies/utils.py:909-945)
  sig: _extract_form_body(body_fields, received_body)
  behavior: ACCUMULATE(body_fields loop -> results)
  calls: _get_multidict_value, get_validation_alias
  called_by: request_body_to_args

_format_endpoint_context (fastapi/exceptions.py:193-202)
  behavior: GUARD(not (self.endpoint_file and self.endpoint_line and self.e... -> return...)
  called_by: __str__, ValidationException

_serialize_data (fastapi/routing.py:467-490)
  sig: _serialize_data(data)
  behavior: BRANCH(stream_item_field -> raise ResponseValidat..., else -> return json.du...)
  called_by: _serialize_item, _serialize_sse_item, get_request_handler
  raises: ResponseValidationError
  uses: ResponseValidationError (fastapi.exceptions), EndpointContext (fastapi.exceptions)

Body (fastapi/param_functions.py:1324-1651)
  sig: Body(default)
  behavior: DELEGATE(params.Body -> result)
  uses: Doc (annotated_doc)

Path (fastapi/param_functions.py:14-355)
  Declare a path parameter for a *path operation*.
  sig: Path(default)
  behavior: DELEGATE(params.Path -> result)
  uses: Doc (annotated_doc)

Query (fastapi/param_functions.py:358-699)
  sig: Query(default)
  behavior: DELEGATE(params.Query -> result)
  uses: Doc (annotated_doc)

get_openapi_operation_request_body (fastapi/openapi/utils.py:181-213)
  behavior: GUARD(not body_field -> return None)
  called_by: get_openapi_path

get_openapi_path (fastapi/openapi/utils.py:263-481)
  behavior: BRANCH(isinstance(route.response_cla... -> result, else -> route.response_class)
  calls: _get_openapi_operation_parameters, get_openapi_operation_metadata, get_openapi_operation_request_body, get_openapi_security_definitions
  called_by: get_openapi

_get_multidict_value (fastapi/dependencies/utils.py:750-778)
  sig: _get_multidict_value(field, values, alias)
  behavior: BRANCH(not _is_json_field(field) and... -> values.getlist(alias), else -> va...)
  calls: _is_json_field, get_validation_alias
  called_by: _extract_form_body, request_params_to_args

_validate_value_with_model_field (fastapi/dependencies/utils.py:735-743)
  called_by: request_body_to_args, request_params_to_args

APIKeyQuery (fastapi/security/api_key.py:53-142)
  API key authentication using a query parameter.
  extends: APIKeyBase
  imports: annotated_doc, fastapi.openapi.models, fastapi.security.base, starlette.exceptions, starlette.requests
  calls: check_api_key

Body (fastapi/params.py:470-579)
  extends: FieldInfo
  imports: warnings, enum, fastapi.exceptions, fastapi.openapi.models, pydantic

EndpointContext (fastapi/exceptions.py:10-14)
  extends: TypedDict
  imports: annotated_doc, pydantic, starlette.exceptions

Path (fastapi/params.py:138-219)
  extends: Param
  imports: warnings, enum, fastapi.exceptions, fastapi.openapi.models, pydantic

PathItem (fastapi/openapi/models.py:305-318)
  extends: BaseModelWithConfig
  imports: enum, fastapi._compat, fastapi.logger, pydantic, typing_extensions

Query (fastapi/params.py:222-301)
  extends: Param
  imports: warnings, enum, fastapi.exceptions, fastapi.openapi.models, pydantic

RequestBody (fastapi/openapi/models.py:267-270)
  extends: BaseModelWithConfig
  imports: enum, fastapi._compat, fastapi.logger, pydantic, typing_extensions

_should_embed_body_fields (fastapi/dependencies/utils.py:885-906)
  sig: _should_embed_body_fields(fields)
  behavior: GUARD(not fields -> return False)
  calls: is_union_of_base_models

create_body_model (fastapi/_compat/v2.py:374-379)

generate_operation_id_for_path (fastapi/utils.py:80-92)

get_path_param_names (fastapi/utils.py:43-44)
  sig: get_path_param_names(path)
  behavior: DELEGATE(set -> result)

is_body_allowed_for_status_code (fastapi/utils.py:26-40)
  sig: is_body_allowed_for_status_code(status_code)
  behavior: GUARD(status_code is None -> return True)

magic_data_reader (docs_src/path_operation_advanced_configuration/tutorial006_py310.py:6-16)
  sig: magic_data_reader(raw_body)
  called_by: create_item

run_endpoint_function (fastapi/routing.py:316-326)
  behavior: BRANCH(is_coroutine -> return await dependan..., else -> return await run_in...)
  called_by: get_request_handler

serialize_sequence_value (fastapi/_compat/v2.py:353-363)

value_is_sequence (fastapi/_compat/shared.py:76-77)
  sig: value_is_sequence(value)

query_or_cookie_extractor (docs_src/dependencies/tutorial005_py310.py:10-15)
  sig: query_or_cookie_extractor(q, last_query)
  behavior: GUARD(not q -> return last_query)
  uses: Depends (fastapi), Cookie (fastapi)

query_or_cookie_extractor (docs_src/dependencies/tutorial005_an_py310.py:12-18)
  sig: query_or_cookie_extractor(q, last_query)
  behavior: GUARD(not q -> return last_query)
  uses: Depends (fastapi), Cookie (fastapi)

get_legacy_data (docs_src/response_directly/tutorial002_py310.py:7-18)
  uses: Response (fastapi)

get_query_token (docs_src/bigger_applications/app_an_py310/dependencies.py:11-13)
  sig: get_query_token(token)
  raises: HTTPException
  uses: HTTPException (fastapi)

post (fastapi/routing.py:2586-2968)
  Add a *path operation* using an HTTP POST operation.
  sig: post(path)
  behavior: DELEGATE(api_route -> result)
  calls: api_route
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

post (fastapi/applications.py:2315-2693)
  Add a *path operation* using an HTTP POST operation.
  sig: post(path)
  behavior: DELEGATE(router.post -> result)
  called_by: FastAPI
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

read_query (docs_src/dependencies/tutorial005_py310.py:19-20)
  sig: read_query(query_or_default)
  uses: Depends (fastapi)

read_query (docs_src/dependencies/tutorial005_an_py310.py:22-25)
  sig: read_query(query_or_default)
  uses: Depends (fastapi)

read_query_check (docs_src/dependencies/tutorial011_py310.py:20-21)
  sig: read_query_check(fixed_content_included)
  uses: Depends (fastapi)

read_query_check (docs_src/dependencies/tutorial011_an_py310.py:22-23)
  sig: read_query_check(fixed_content_included)
  uses: Depends (fastapi)

websocket_endpoint (docs_src/websockets_/tutorial002_py310.py:75-89)
  sig: websocket_endpoint(websocket, item_id, q, cookie_or_token)
  behavior: ACCUMULATE(websocket.receive_tex... -> result)
  uses: Depends (fastapi)

websocket_endpoint (docs_src/websockets_/tutorial002_an_py310.py:77-92)
  behavior: ACCUMULATE(websocket.receive_tex... -> result)
  uses: Depends (fastapi)

generate_lang_path (scripts/translate.py:40-47)
  called_by: list_missing, list_outdated, translate_lang, translate_page

websocket_endpoint (docs_src/websockets_/tutorial003_py310.py:72-81)
  sig: websocket_endpoint(websocket, client_id)
  calls: broadcast, connect, disconnect, send_personal_message

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 22 with behavior annotations
uncovered: handle_data, post_data, post_data_in_out, query_extractor
drill: fastapi/dependencies/utils.py (~48 lines, get_body_field)
drill: fastapi/dependencies/utils.py (~47 lines, request_body_to_args)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## request_body_to_args  (fastapi/dependencies/utils.py L948-995)
```
async def request_body_to_args(
    body_fields: list[ModelField],
    received_body: dict[str, Any] | FormData | None,
    embed_body_fields: bool,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    values: dict[str, Any] = {}
    errors: list[dict[str, Any]] = []
    assert body_fields, "request_body_to_args() should be called with fields"
    single_not_embedded_field = len(body_fields) == 1 and not embed_body_fields
    first_field = body_fields[0]
    body_to_process = received_body

    fields_to_extract: list[ModelField] = body_fields

    if (
        single_not_embedded_field
        and lenient_issubclass(first_field.field_info.annotation, BaseModel)
        and isinstance(received_body, FormData)
    ):
        fields_to_extract = get_cached_model_fields(first_field.field_info.annotation)

    if isinstance(received_body, FormData):
        body_to_process = await _extract_form_body(fields_to_extract, received_body)

    if single_not_embedded_field:
        loc: tuple[str, ...] = ("body",)
        v_, errors_ = _validate_value_with_model_field(
            field=first_field, value=body_to_process, values=values, loc=loc
        )
        return {first_field.name: v_}, errors_
    for field in body_fields:
        loc = ("body", get_validation_alias(field))
        value: Any | None = None
        if body_to_process is not None:
            try:
                value = body_to_process.get(get_validation_alias(field))
            # If the received body is a list, not a dict
            except AttributeError:
                errors.append(get_missing_field_error(loc))
                continue
        v_, errors_ = _validate_value_with_model_field(
            field=field, value=value, values=values, loc=loc
        )
        if errors_:
            errors.extend(errors_)
        else:
            values[field.name] = v_
    return values, errors
```

## get_body_field  (fastapi/dependencies/utils.py L998-1049)
```
def get_body_field(
    *, flat_dependant: Dependant, name: str, embed_body_fields: bool
) -> ModelField | None:
    """
    Get a ModelField representing the request body for a path operation, combining
    all body parameters into a single field if necessary.

    Used to check if it's form data (with `isinstance(body_field, params.Form)`)
    or JSON and to generate the JSON Schema for a request body.

    This is **not** used to validate/parse the request body, that's done with each
    individual body parameter.
    """
    if not flat_dependant.body_params:
        return None
    first_param = flat_dependant.body_params[0]
    if not embed_body_fields:
        return first_param
    model_name = "Body_" + name
    BodyModel = create_body_model(
        fields=flat_dependant.body_params, model_name=model_name
    )
    required = any(
        True for f in flat_dependant.body_params if f.field_info.is_required()
    )
    BodyFieldInfo_kwargs: dict[str, Any] = {
        "annotation": BodyModel,
        "alias": "body",
    }
    if not required:
        BodyFieldInfo_kwargs["default"] = None
    if any(isinstance(f.field_info, params.File) for f in flat_dependant.body_params):
        BodyFieldInfo: type[params.Body] = params.File
    elif any(isinstance(f.field_info, params.Form) for f in flat_dependant.body_params):
        BodyFieldInfo = params.Form
    else:
        BodyFieldInfo = params.Body

        body_param_media_types = [
            f.field_info.media_type
            for f in flat_dependant.body_params
            if isinstance(f.field_info, params.Body)
        ]
        if len(set(body_param_media_types)) == 1:
            BodyFieldInfo_kwargs["media_type"] = body_param_media_types[0]
    final_field = create_model_field(
        name="body",
        type_=BodyModel,
        alias="body",
        field_info=BodyFieldInfo(**BodyFieldInfo_kwargs),
    )
    return final_field
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

## get_validation_alias  (fastapi/dependencies/utils.py L1052-1054)
```
def get_validation_alias(field: ModelField) -> str:
    va = getattr(field, "validation_alias", None)
    return va or field.alias
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
... (truncated)
```
--- END SOURCE SNIPPETS ---

QUESTION: When one FastAPI endpoint mixes path, query, and body inputs, how does the framework decide where each value comes from and how invalid data is reported?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
