# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: blind-fastapi-rel-2

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.

--- CLUE FILE (File 1) ---
=CC v2.1 fastapi@HEAD 1118mod 5241sym
? How do router-level options and path-level options combine when FastAPI builds a larger application from routers?


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
options (fastapi/applications.py:3066-3439)
  Add a *path operation* using an HTTP OPTIONS operation.
  sig: options(path)
  behavior: DELEGATE(router.options -> result)
  called_by: FastAPI
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

options (fastapi/routing.py:3345-3722)
  Add a *path operation* using an HTTP OPTIONS operation.
  sig: options(path)
  behavior: DELEGATE(api_route -> result)
  calls: api_route
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

Path (fastapi/param_functions.py:14-355)
  Declare a path parameter for a *path operation*.
  sig: Path(default)
  behavior: DELEGATE(params.Path -> result)
  uses: Doc (annotated_doc)

get_openapi_path (fastapi/openapi/utils.py:263-481)
  behavior: BRANCH(isinstance(route.response_cla... -> result, else -> route.response_class)
  calls: _get_openapi_operation_parameters, get_openapi_operation_metadata, get_openapi_operation_request_body, get_openapi_security_definitions
  called_by: get_openapi

Path (fastapi/params.py:138-219)
  extends: Param
  imports: warnings, enum, fastapi.exceptions, fastapi.openapi.models, pydantic

PathItem (fastapi/openapi/models.py:305-318)
  extends: BaseModelWithConfig
  imports: enum, fastapi._compat, fastapi.logger, pydantic, typing_extensions

generate_operation_id_for_path (fastapi/utils.py:80-92)

get_path_param_names (fastapi/utils.py:43-44)
  sig: get_path_param_names(path)
  behavior: DELEGATE(set -> result)

generate_lang_path (scripts/translate.py:40-47)
  called_by: list_missing, list_outdated, translate_lang, translate_page

generate_en_path (scripts/translate.py:50-57)
  called_by: list_removable

redirect_fastapi (docs_src/custom_response/tutorial006b_py310.py:8-9)

APIRouter (fastapi/routing.py:1001-4953)
  `APIRouter` class, used to group *path operations*, for example to structure
  extends: Router
  imports: email.message, inspect, types, enum, anyio
  calls: add_api_route, add_api_websocket_route, add_event_handler, api_route, APIWebSocketRoute, _DefaultLifespan, _merge_lifespan_context, _wrap_gen_lifespan_context
  raises: FastAPIError
  uses: Default (fastapi.datastructures)

FastAPI (fastapi/applications.py:45-4693)
  `FastAPI` app class, the main entrypoint to use FastAPI.
  extends: Starlette
  imports: enum, annotated_doc, fastapi, fastapi.datastructures, fastapi.exception_handlers
  calls: __call__, add_api_route, add_api_websocket_route, delete, get, head, include_router, on_event
  uses: Default (fastapi.datastructures), Doc (annotated_doc), JSONResponse (starlette.responses)

include_router (fastapi/routing.py:1574-1827)
  Include another `APIRouter` in the same current `APIRouter`.
  sig: include_router(router)
  behavior: BRANCH(prefix -> result, else -> result); ACCUMULATE(router.routes loop -> current tags)
  calls: add_api_route, add_api_websocket_route, add_event_handler, _merge_lifespan_context
  raises: FastAPIError
  uses: Default (fastapi.datastructures), Doc (annotated_doc), FastAPIError (fastapi.exceptions)

include_router (fastapi/applications.py:1359-1564)
  Include an `APIRouter` in the same app.
  sig: include_router(router)
  called_by: FastAPI
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

get (fastapi/applications.py:1564-1937)
  Add a *path operation* using an HTTP GET operation.
  sig: get(path)
  behavior: DELEGATE(router.get -> result)
  called_by: redoc_html, swagger_ui_html, setup, FastAPI
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

delete (fastapi/applications.py:2693-3066)
  Add a *path operation* using an HTTP DELETE operation.
  sig: delete(path)
  behavior: DELEGATE(router.delete -> result)
  called_by: FastAPI
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

head (fastapi/applications.py:3439-3812)
  Add a *path operation* using an HTTP HEAD operation.
  sig: head(path)
  behavior: DELEGATE(router.head -> result)
  called_by: FastAPI
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

patch (fastapi/applications.py:3812-4190)
  Add a *path operation* using an HTTP PATCH operation.
  sig: patch(path)
  behavior: DELEGATE(router.patch -> result)
  called_by: FastAPI
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

post (fastapi/applications.py:2315-2693)
  Add a *path operation* using an HTTP POST operation.
  sig: post(path)
  behavior: DELEGATE(router.post -> result)
  called_by: FastAPI
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

put (fastapi/applications.py:1937-2315)
  Add a *path operation* using an HTTP PUT operation.
  sig: put(path)
  behavior: DELEGATE(router.put -> result)
  called_by: FastAPI
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

trace (fastapi/applications.py:4190-4563)
  Add a *path operation* using an HTTP TRACE operation.
  sig: trace(path)
  behavior: DELEGATE(router.trace -> result)
  called_by: FastAPI
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

on_event (fastapi/applications.py:4580-4601)
  Add an event handler for the application.
  sig: on_event(event_type)
  behavior: DELEGATE(router.on_event -> result)
  called_by: FastAPI
  uses: Doc (annotated_doc)

get (fastapi/routing.py:1827-2204)
  Add a *path operation* using an HTTP GET operation.
  sig: get(path)
  behavior: DELEGATE(api_route -> result)
  calls: api_route
  called_by: APIRoute, get_request_handler, get_websocket_app
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

delete (fastapi/routing.py:2968-3345)
  Add a *path operation* using an HTTP DELETE operation.
  sig: delete(path)
  behavior: DELEGATE(api_route -> result)
  calls: api_route
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

head (fastapi/routing.py:3722-4104)
  Add a *path operation* using an HTTP HEAD operation.
  sig: head(path)
  behavior: DELEGATE(api_route -> result)
  calls: api_route
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

patch (fastapi/routing.py:4104-4486)
  Add a *path operation* using an HTTP PATCH operation.
  sig: patch(path)
  behavior: DELEGATE(api_route -> result)
  calls: api_route
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

post (fastapi/routing.py:2586-2968)
  Add a *path operation* using an HTTP POST operation.
  sig: post(path)
  behavior: DELEGATE(api_route -> result)
  calls: api_route
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

put (fastapi/routing.py:2204-2586)
  Add a *path operation* using an HTTP PUT operation.
  sig: put(path)
  behavior: DELEGATE(api_route -> result)
  calls: api_route
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

trace (fastapi/routing.py:4486-4868)
  Add a *path operation* using an HTTP TRACE operation.
  sig: trace(path)
  behavior: DELEGATE(api_route -> result)
  calls: api_route
  uses: Default (fastapi.datastructures), Doc (annotated_doc)

get_body_field (fastapi/dependencies/utils.py:998-1049)
  Get a ModelField representing the request body for a path operation, combining

middleware (fastapi/applications.py:4601-4647)
  Add a middleware to the application.
  sig: middleware(middleware_type)
  uses: Doc (annotated_doc)

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 41 with behavior annotations
uncovered: _async_stream_raw, _build_response_args, _shutdown, _sse_producer_cm
drill: fastapi/routing.py (~373 lines, options)
drill: fastapi/applications.py (~370 lines, options)
drill: fastapi/openapi/utils.py (~288 lines, get_openapi_path)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## get_openapi_path  (fastapi/openapi/utils.py L263-481)
```
def get_openapi_path(
    *,
    route: routing.APIRoute,
    operation_ids: set[str],
    model_name_map: ModelNameMap,
    field_mapping: dict[
        tuple[ModelField, Literal["validation", "serialization"]], dict[str, Any]
    ],
    separate_input_output_schemas: bool = True,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    path = {}
    security_schemes: dict[str, Any] = {}
    definitions: dict[str, Any] = {}
    assert route.methods is not None, "Methods must be a list"
    if isinstance(route.response_class, DefaultPlaceholder):
        current_response_class: type[Response] = route.response_class.value
    else:
        current_response_class = route.response_class
    assert current_response_class, "A response class is needed to generate OpenAPI"
    route_response_media_type: str | None = current_response_class.media_type
    if route.include_in_schema:
        for method in route.methods:
            operation = get_openapi_operation_metadata(
                route=route, method=method, operation_ids=operation_ids
            )
            parameters: list[dict[str, Any]] = []
            flat_dependant = get_flat_dependant(route.dependant, skip_repeats=True)
            security_definitions, operation_security = get_openapi_security_definitions(
                flat_dependant=flat_dependant
            )
            if operation_security:
                operation.setdefault("security", []).extend(operation_security)
            if security_definitions:
                security_schemes.update(security_definitions)
            operation_parameters = _get_openapi_operation_parameters(
                dependant=route.dependant,
                model_name_map=model_name_map,
                field_mapping=field_mapping,
                separate_input_output_schemas=separate_input_output_schemas,
            )
            parameters.extend(operation_parameters)
            if parameters:
                all_parameters = {
                    (param["in"], param["name"]): param for param in parameters
                }
                required_parameters = {
                    (param["in"], param["name"]): param
                    for param in parameters
                    if param.get("required")
                }
                # Make sure required definitions of the same parameter take precedence
                # over non-required definitions
                all_parameters.update(required_parameters)
                operation["parameters"] = list(all_parameters.values())
            if method in METHODS_WITH_BODY:
                request_body_oai = get_openapi_operation_request_body(
                    body_field=route.body_field,
                    model_name_map=model_name_map,
                    field_mapping=field_mapping,
                    separate_input_output_schemas=separate_input_output_schemas,
                )
                if request_body_oai:
                    operation["requestBody"] = request_body_oai
            if route.callbacks:
                callbacks = {}
                for callback in route.callbacks:
                    if isinstance(callback, routing.APIRoute):
                        (
                            cb_path,
                            cb_security_schemes,
                            cb_definitions,
                        ) = get_openapi_path(
                            route=callback,
                            operation_ids=operation_ids,
                            model_name_map=model_name_map,
                            field_mapping=field_mapping,
                            separate_input_output_schemas=separate_input_output_schemas,
                        )
                        callbacks[callback.name] = {callback.path: cb_path}
                operation["callbacks"] = callbacks
            if route.status_code is not None:
                status_code = str(route.status_code)
            else:
                # It would probably make more sense for all response classes to have an
                # explicit default status_code, and to extract it from them, instead of
                # doing this inspection tricks, that would probably be in the future
                # TODO: probably make status_code a default class attribute for all
                # responses in Starlette
                response_signature = inspect.signature(current_response_class.__init__)
                status_code_param = response_signature.parameters.get("status_code")
                if status_code_param is not None:
                    if isinstance(status_code_param.default, int):
                        status_code = str(status_code_param.default)
            operation.setdefault("responses", {}).setdefault(status_code, {})[
                "description"
            ] = route.response_description
            if is_body_allowed_for_status_code(route.status_code):
                # Check for JSONL streaming (generator endpoints)
                if route.is_json_stream:
                    jsonl_content: dict[str, Any] = {}
                    if route.stream_item_field:
                        item_schema = get_schema_from_model_field(
                            field=route.stream_item_field,
                            model_name_map=model_name_map,
                            field_mapping=field_mapping,
                            separate_input_output_schemas=separate_input_output_schemas,
                        )
                        jsonl_content["itemSchema"] = item_schema
                    else:
                        jsonl_content["itemSchema"] = {}
                    operation.setdefault("responses", {}).setdefault(
                        status_code, {}
                    ).setdefault("content", {})["application/jsonl"] = jsonl_content
                elif route.is_sse_stream:
                    sse_content: dict[str, Any] = {}
                    item_schema = copy.deepcopy(_SSE_EVENT_SCHEMA)
                    if route.stream_item_field:
                        content_schema = get_schema_from_model_field(
                            field=route.stream_item_field,
                            model_name_map=model_name_map,
                            field_mapping=field_mapping,
                            separate_input_output_schemas=separate_input_output_schemas,
                        )
                        item_schema["required"] = ["data"]
                        item_schema["properties"]["data"] = {
                            "type": "string",
                            "contentMediaType": "application/json",
                            "contentSchema": content_schema,
                        }
                    sse_content["itemSchema"] = item_schema
                    operation.setdefault("responses", {}).setdefault(
                        status_code, {}
                    ).setdefault("content", {})["text/event-stream"] = sse_content
                elif route_response_media_type:
                    response_schema = {"type": "string"}
                    if lenient_issubclass(current_response_class, JSONResponse):
                        if route.response_field:
                            response_schema = get_schema_from_model_field(
                                field=route.response_field,
                                model_name_map=model_name_map,
                                field_mapping=field_mapping,
                                separate_input_output_schemas=separate_input_output_schemas,
                            )
                        else:
                            response_schema = {}
                    operation.setdefault("responses", {}).setdefault(
                        status_code, {}
                    ).setdefault("content", {}).setdefault(
                        route_response_media_type, {}
                    )["schema"] = response_schema
            if route.responses:
                operation_responses = operation.setdefault("responses", {})
                for (
                    additional_status_code,
                    additional_response,
                ) in route.responses.items():
                    process_response = copy.deepcopy(additional_response)
                    process_response.pop("model", None)
                    status_code_key = str(additional_status_code).upper()
                    if status_code_key == "DEFAULT":
                        status_code_key = "default"
                    openapi_response = operation_responses.setdefault(
                        status_code_key, {}
                    )
                    assert isinstance(process_response, dict), (
                        "An additional response must be a dict"
                    )
                    field = route.response_fields.get(additional_status_code)
                    additional_field_schema: dict[str, Any] | None = None
                    if field:
                        additional_field_schema = get_schema_from_model_field(
                            field=field,
                            model_name_map=model_name_map,
                            field_mapping=field_mapping,
                            separate_input_output_schemas=separate_input_output_schemas,
                        )
                        media_type = route_response_media_type or "application/json"
                        additional_schema = (
                            process_response.setdefault("content", {})
                            .setdefault(media_type, {})
                            .setdefault("schema", {})
                        )
                        deep_dict_update(additional_schema, additional_field_schema)
                    status_text: str | None = status_code_ranges.get(
                        str(additional_status_code).upper()
                    ) or http.client.responses.get(int(additional_status_code))
                    description = (
                        process_response.get("description")
                        or openapi_response.get("description")
                        or status_text
                        or "Additional Response"
                    )
                    deep_dict_update(openapi_response, process_response)
                    openapi_response["description"] = description
            http422 = "422"
            all_route_params = get_flat_params(route.dependant)
            if (all_route_params or route.body_field) and not any(
                status in operation["responses"]
                for status in [http422, "4XX", "default"]
            ):
                operation["responses"][http422] = {
                    "description": "Validation Error",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": REF_PREFIX + "HTTPValidationError"}
                        }
                    },
                }
                if "ValidationError" not in definitions:
                    definitions.update(
                        {
                            "ValidationError": validation_error_definition,
                            "HTTPValidationError": validation_error_response_definition,
                        }
                    )
            if route.openapi_extra:
                deep_dict_update(operation, route.openapi_extra)
            path[method.lower()] = operation
    return path, security_schemes, definitions
```

## options  (fastapi/routing.py L3345-3722)
```
    def options(
        self,
        path: Annotated[
            str,
            Doc(
                """
                The URL path to be used for this *path operation*.

                For example, in `http://example.com/items`, the path is `/items`.
                """
            ),
        ],
        *,
        response_model: Annotated[
            Any,
            Doc(
                """
                The type to use for the response.

                It could be any valid Pydantic *field* type. So, it doesn't have to
                be a Pydantic model, it could be other things, like a `list`, `dict`,
                etc.

                It will be used for:

                * Documentation: the generated OpenAPI (and the UI at `/docs`) will
                    show it as the response (JSON Schema).
                * Serialization: you could return an arbitrary object and the
                    `response_model` would be used to serialize that object into the
                    corresponding JSON.
                * Filtering: the JSON sent to the client will only contain the data
                    (fields) defined in the `response_model`. If you returned an object
                    that contains an attribute `password` but the `response_model` does
                    not include that field, the JSON sent to the client would not have
                    that `password`.
                * Validation: whatever you return will be serialized with the
                    `response_model`, converting any data as necessary to generate the
                    corresponding JSON. But if the data in the object returned is not
                    valid, that would mean a violation of the contract with the client,
                    so it's an error from the API developer. So, FastAPI will raise an
                    error and return a 500 error code (Internal Server Error).

                Read more about it in the
                [FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/).
                """
            ),
        ] = Default(None),
        status_code: Annotated[
            int | None,
            Doc(
                """
                The default status code to be used for the response.

                You could override the status code by returning a response directly.

                Read more about it in the
                [FastAPI docs for Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/).
                """
            ),
        ] = None,
        tags: Annotated[
            list[str | Enum] | None,
            Doc(
                """
                A list of tags to be applied to the *path operation*.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#tags).
                """
            ),
        ] = None,
        dependencies: Annotated[
            Sequence[params.Depends] | None,
            Doc(
                """
                A list of dependencies (using `Depends()`) to be applied to the
                *path operation*.

                Read more about it in the
                [FastAPI docs for Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/).
                """
            ),
        ] = None,
        summary: Annotated[
            str | None,
            Doc(
                """
                A summary for the *path operation*.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                """
            ),
        ] = None,
        description: Annotated[
            str | None,
            Doc(
                """
                A description for the *path operation*.

                If not provided, it will be extracted automatically from the docstring
                of the *path operation function*.

                It can contain Markdown.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                Read more about it in the
                [FastAPI docs for Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/).
                """
            ),
        ] = None,
        response_description: Annotated[
            str,
            Doc(
                """
                The description for the default response.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                """
            ),
        ] = "Successful Response",
        responses: Annotated[
            dict[int | str, dict[str, Any]] | None,
            Doc(
                """
                Additional responses that could be returned by this *path operation*.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                """
            ),
        ] = None,
        deprecated: Annotated[
            bool | None,
            Doc(
                """
                Mark this *path operation* as deprecated.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).
                """
            ),
        ] = None,
        operation_id: Annotated[
            str | None,
            Doc(
                """
                Custom operation ID to be used by this *path operation*.

                By default, it is generated automatically.

                If you provide a custom operation ID, you need to make sure it is
                unique for the whole API.

... (truncated)
```
--- END SOURCE SNIPPETS ---

QUESTION: How do router-level options and path-level options combine when FastAPI builds a larger application from routers?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
