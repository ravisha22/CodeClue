# v2.5 Response: blind-fastapi-mech-1
Date: 2026-04-16

## Question
When one FastAPI endpoint mixes path, query, and body inputs, how does the framework decide where each value comes from and how invalid data is reported?

## Answer

The clue file and source snippets reveal a multi-stage pipeline: parameter classification by type annotation, extraction from the appropriate request location, validation via model fields, and error accumulation into a structured response.

### 1. Parameter Classification — Where Each Value Comes From

FastAPI provides explicit parameter markers to classify endpoint parameters:

- **`Path`** (`fastapi/param_functions.py:14–355`): "Declare a path parameter for a *path operation*." Delegates to `params.Path` (`fastapi/params.py:138–219`), which extends `Param`.
- **`Query`** (`fastapi/param_functions.py:358–699`): Delegates to `params.Query` (`fastapi/params.py:222–301`), which also extends `Param`.
- **`Body`** (`fastapi/param_functions.py:1324–1651`): Delegates to `params.Body` (`fastapi/params.py:470–579`), which extends `FieldInfo`.

`add_non_field_param_to_dependency` (`fastapi/dependencies/utils.py:359–380`) has behavior `PRECEDENCE(type_annotation)`, indicating the type annotation drives classification. Parameters are classified into `ParamDetails` (source snippet, `fastapi/dependencies/utils.py:384–387`), which holds `type_annotation`, `depends`, and `field`.

`get_path_param_names` (`fastapi/utils.py:43–44`) extracts path parameter names from the URL template using `DELEGATE(set -> result)`, so any parameter matching a path template placeholder is classified as a path parameter.

### 2. Body Field Handling

**`get_body_field`** (source snippet, `fastapi/dependencies/utils.py:998–1049`) combines all body parameters:
- If there are no body params, returns `None`.
- If there's a single non-embedded body field, it returns that field directly.
- If embedding is needed, it creates a composite `BodyModel` via `create_body_model`, wrapping all body params into one model. It selects `params.File`, `params.Form`, or `params.Body` as the field info type depending on what parameter types are present.
- Media types are unified when all body params share the same `media_type`.

**`_should_embed_body_fields`** (source snippet, `fastapi/dependencies/utils.py:885–906`) determines when embedding is required:
- Multiple body params → embed.
- Explicit `embed=True` on the field → embed.
- A `Form` field that is not a `BaseModel` or union of `BaseModel` → embed.

### 3. Request Data Extraction

**`request_body_to_args`** (source snippet, `fastapi/dependencies/utils.py:948–995`) processes body data:
- For a single non-embedded field, validates the entire received body as that field with loc `("body",)`.
- For multiple/embedded fields, iterates `body_fields`, extracting each value from `body_to_process` using `get_validation_alias(field)` as the key, with loc `("body", alias)`.
- For `FormData`, delegates to `_extract_form_body` first.

**`_extract_form_body`** (source snippet, `fastapi/dependencies/utils.py:909–945`):
- Iterates body fields, calling `_get_multidict_value` to extract each value.
- Handles `File` parameters: reads `UploadFile` to bytes for byte-annotated fields, or reads sequences of files.
- Passes through unknown form keys as extra values.

**`_get_multidict_value`** (source snippet, `fastapi/dependencies/utils.py:750–778`):
- Uses `get_validation_alias(field)` to determine the alias.
- If the field is a sequence annotation and values are `ImmutableMultiDict` or `Headers`, uses `getlist(alias)`.
- Otherwise uses `values.get(alias, None)`.
- Returns the field's default if the value is missing/empty and the field is not required; returns sentinel `None` if required and missing.

### 4. Validation and Error Reporting

**`_validate_value_with_model_field`** (source snippet, `fastapi/dependencies/utils.py:735–743`):
- If value is `None` and field is required → returns `get_missing_field_error(loc=loc)`.
- If value is `None` and field is not required → returns `deepcopy(field.default)`.
- Otherwise calls `field.validate(value, values, loc=loc)`, which performs Pydantic validation and returns `(validated_value, errors)`.

The `loc` tuple (e.g., `("body",)`, `("body", "field_name")`) provides structured location information in errors, indicating exactly where the invalid data was found.

**Error accumulation** in `request_body_to_args`: errors from each field validation are collected into a list via `errors.extend(errors_)`. The behavior annotation `ACCUMULATE(body_fields loop -> errors)` confirms this aggregation pattern.

**`_regenerate_error_with_loc`** (`fastapi/_compat/v2.py:473`) suggests errors are enriched with location information to produce structured error responses.

### 5. The Complete Pipeline

The `get_request_handler` (`fastapi/routing.py:347`) orchestrates the full pipeline. The `_serialize_data` function (`fastapi/routing.py:467–490`) handles response serialization and raises `ResponseValidationError` for invalid response data (behavior: `BRANCH(stream_item_field -> raise ResponseValidat...)`).

### What Cannot Be Determined
GAPS states `type: MECHANISTIC` with uncovered symbols: `handle_data`, `post_data`, `post_data_in_out`, `query_extractor`. The exact logic of `request_params_to_args` (which handles path/query/header/cookie extraction) is not included in the FOCUS or snippets, so the parallel extraction pipeline for non-body parameters cannot be fully traced. The `get_dependant` function that builds the dependency graph and classifies parameters is also not covered.
