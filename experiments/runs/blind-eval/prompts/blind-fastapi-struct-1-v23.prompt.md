# Blind Evaluation Prompt - MRLF v2.4
# Task: blind-fastapi-struct-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 fastapi@HEAD 1118mod 5241sym
? In FastAPI's documented bigger-application pattern, what public building blocks are used to split one API across multiple files and packages?


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
check_api_key (fastapi/security/api_key.py:45-50)
  sig: check_api_key(api_key)
  behavior: GUARD(not api_key -> raise self.make_not_authe...)
  calls: make_not_authenticated_error
  called_by: APIKeyCookie, APIKeyHeader, APIKeyQuery
  raises: make_not_authenticated_error

api_route (fastapi/routing.py:1415-1477)
  sig: api_route(path)
  calls: add_api_route
  called_by: delete, get, head, options, patch, post, put, trace
  uses: Default (fastapi.datastructures)

add_api_route (fastapi/applications.py:1162-1219)
  sig: add_api_route(path, endpoint)
  called_by: api_route, FastAPI
  uses: Default (fastapi.datastructures)

add_api_route (fastapi/routing.py:1332-1415)
  sig: add_api_route(path, endpoint)
  called_by: api_route, include_router, APIRouter
  uses: Default (fastapi.datastructures)

api_route (fastapi/applications.py:1219-1279)
  sig: api_route(path)
  calls: add_api_route
  uses: Default (fastapi.datastructures)

FastAPI (fastapi/applications.py:45-4693)
  `FastAPI` app class, the main entrypoint to use FastAPI.
  extends: Starlette
  imports: enum, annotated_doc, fastapi, fastapi.datastructures, fastapi.exception_handlers
  calls: __call__, add_api_route, add_api_websocket_route, delete, get, head, include_router, on_event
  uses: Default (fastapi.datastructures), Doc (annotated_doc), JSONResponse (starlette.responses)

add_api_websocket_route (fastapi/routing.py:1477-1498)
  sig: add_api_websocket_route(path, endpoint, name)
  calls: APIWebSocketRoute
  called_by: include_router, websocket, APIRouter

add_api_websocket_route (fastapi/applications.py:1279-1294)
  sig: add_api_websocket_route(path, endpoint, name)
  called_by: websocket, FastAPI

OpenAPI (fastapi/openapi/models.py:419-430)
  extends: BaseModelWithConfig
  imports: enum, fastapi._compat, fastapi.logger, pydantic, typing_extensions

create_files (docs_src/request_files/tutorial003_an_py310.py:10-13)
  sig: create_files(files)
  uses: File (fastapi)

create_files (docs_src/request_files/tutorial002_an_py310.py:10-11)
  sig: create_files(files)
  uses: File (fastapi)

create_files (docs_src/request_files/tutorial003_py310.py:8-11)
  sig: create_files(files)
  uses: File (fastapi)

create_files (docs_src/request_files/tutorial002_py310.py:8-9)
  sig: create_files(files)
  uses: File (fastapi)

create_upload_files (docs_src/request_files/tutorial003_py310.py:15-18)
  sig: create_upload_files(files)
  uses: File (fastapi)

create_upload_files (docs_src/request_files/tutorial003_an_py310.py:17-22)
  sig: create_upload_files(files)
  uses: File (fastapi)

extract_multiline_code_blocks (scripts/doc_parsing_utils.py:482-551)
  sig: extract_multiline_code_blocks(text)
  behavior: ACCUMULATE(enumerate(text, start... -> current block lines)
  calls: MultilineCodeBlockInfo, get_code_block_lang
  called_by: check_translation

process_one_page (scripts/translation_fixer.py:65-98)
  Fix one translated document by comparing it to the English version.
  sig: process_one_page(path)
  called_by: fix_all, fix_pages

HeroPublic (docs_src/sql_databases/tutorial002_py310.py:15-16)
  extends: HeroBase
  imports: fastapi, sqlmodel

HeroPublic (docs_src/sql_databases/tutorial002_an_py310.py:17-18)
  extends: HeroBase
  imports: fastapi, sqlmodel

_split_hash_comment (scripts/doc_parsing_utils.py:552-560)
  sig: _split_hash_comment(line)
  called_by: replace_multiline_code_block

_split_slashes_comment (scripts/doc_parsing_utils.py:561-569)
  sig: _split_slashes_comment(line)
  called_by: replace_multiline_code_block

create_multiple_images (docs_src/body_nested_models/tutorial008_py310.py:13-14)
  sig: create_multiple_images(images)

create_upload_files (docs_src/request_files/tutorial002_py310.py:13-14)
  sig: create_upload_files(files)

create_upload_files (docs_src/request_files/tutorial002_an_py310.py:15-16)
  sig: create_upload_files(files)

on_files (scripts/mkdocs_hooks.py:96-104)
  sig: on_files(files)
  calls: resolve_file, resolve_files

read_item_public_data (docs_src/response_model/tutorial005_py310.py:36-37)
  sig: read_item_public_data(item_id)

read_item_public_data (docs_src/response_model/tutorial006_py310.py:36-37)
  sig: read_item_public_data(item_id)

redirect_fastapi (docs_src/custom_response/tutorial006b_py310.py:8-9)

resolve_files (scripts/mkdocs_hooks.py:79-93)
  behavior: ACCUMULATE(items loop -> result, raises ValueError)
  calls: resolve_file
  called_by: on_files
  raises: ValueError

openapi (fastapi/applications.py:1069-1102)
  Generate the OpenAPI schema of the application.

APIKeyCookie (fastapi/security/api_key.py:233-318)
  API key authentication using a cookie.
  extends: APIKeyBase
  imports: annotated_doc, fastapi.openapi.models, fastapi.security.base, starlette.exceptions, starlette.requests
  calls: check_api_key

APIKeyHeader (fastapi/security/api_key.py:145-230)
  API key authentication using a header.
  extends: APIKeyBase
  imports: annotated_doc, fastapi.openapi.models, fastapi.security.base, starlette.exceptions, starlette.requests
  calls: check_api_key

APIKeyQuery (fastapi/security/api_key.py:53-142)
  API key authentication using a query parameter.
  extends: APIKeyBase
  imports: annotated_doc, fastapi.openapi.models, fastapi.security.base, starlette.exceptions, starlette.requests
  calls: check_api_key

APIRouter (fastapi/routing.py:1001-4953)
  `APIRouter` class, used to group *path operations*, for example to structure
  extends: Router
  imports: email.message, inspect, types, enum, anyio
  calls: add_api_route, add_api_websocket_route, add_event_handler, api_route, APIWebSocketRoute, _DefaultLifespan, _merge_lifespan_context, _wrap_gen_lifespan_context
  raises: FastAPIError
  uses: Default (fastapi.datastructures)

FastAPIError (fastapi/exceptions.py:161-164)
  A generic, FastAPI-specific error.
  extends: RuntimeError
  imports: annotated_doc, pydantic, starlette.exceptions

remove_unused_docs_src (scripts/docs.py:540-649)
  Delete .py files in docs_src that are not included in any .md file under docs/.
  behavior: ACCUMULATE(docs_path.rglob('*.md... -> all docs content)

APIWebSocketRoute (fastapi/routing.py:765-806)
  extends: WebSocketRoute
  imports: email.message, inspect, types, enum, anyio
  calls: get_websocket_app, websocket_session
  called_by: add_api_websocket_route, APIRouter
  uses: EndpointContext (fastapi.exceptions), WebSocketRequestValidationError (fastapi.exceptions), WebSocket (starlette.websockets)

replace_multiline_code_blocks_in_text (scripts/doc_parsing_utils.py:643-671)
  Update each code block in `text` with the corresponding code block from
  sig: replace_multiline_code_blocks_in_text(text, code_blocks, original_code_blocks)
  behavior: ACCUMULATE(zip(code_blocks, orig... -> result)
  calls: replace_multiline_code_block
  called_by: check_translation
  raises: ValueError

APIKeyBase (fastapi/security/api_key.py:11-50)
  extends: SecurityBase
  imports: annotated_doc, fastapi.openapi.models, fastapi.security.base, starlette.exceptions, starlette.requests
  calls: make_not_authenticated_error
  raises: make_not_authenticated_error
  uses: HTTPException (starlette.exceptions)

make_not_authenticated_error (fastapi/security/api_key.py:29-43)
  The WWW-Authenticate header is not standardized for API Key authentication but
  behavior: DELEGATE(HTTPException -> result)
  called_by: check_api_key, APIKeyBase
  uses: HTTPException (starlette.exceptions)

make_not_authenticated_error (fastapi/security/oauth2.py:401-421)
  The OAuth 2 specification doesn't define the challenge that should be used,
  behavior: DELEGATE(HTTPException -> result)
  called_by: OAuth2, OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer
  uses: HTTPException (fastapi.exceptions)

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 80 symbols in L3, 30 with behavior annotations
uncovered: include_router, delete, head, include_router

--- CLUE FILE END ---

QUESTION: In FastAPI's documented bigger-application pattern, what public building blocks are used to split one API across multiple files and packages?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
