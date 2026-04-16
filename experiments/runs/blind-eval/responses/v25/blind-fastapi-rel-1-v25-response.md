# v2.5 Response: blind-fastapi-rel-1
Date: 2026-04-16

## Question
How do dependency functions relate to path operation functions and the generated API schema in FastAPI?

## Answer

The clue file reveals a three-way relationship: dependency functions feed values into path operations at runtime, and their parameter signatures also contribute to the generated OpenAPI schema.

### 1. Dependency Functions Feed Path Operations

**Dependency chaining** is documented in `docs_src/dependencies/tutorial008_py310.py` and `tutorial008_an_py310.py`:
- `dependency_a` (line 4) takes no dependencies.
- `dependency_b` (line 12) receives `dep_a` via `Depends` (`uses: Depends (fastapi)`).
- `dependency_c` (line 20) receives `dep_b` via `Depends`.

This shows dependencies are composable functions that form chains, each receiving the output of the previous dependency via the `Depends` marker.

**Dependency override** is shown in `docs_src/dependency_testing/tutorial001_an_py310.py:26` — `override_dependency` takes `q` as a parameter, demonstrating dependencies can be swapped for testing.

**`SolvedDependency`** (`fastapi/dependencies/utils.py:587–592`) is the result type of dependency resolution, containing `values`, `errors`, `background_tasks`, `response`, and `dependency_cache`. This is called by `solve_dependencies`, indicating the runtime resolves all dependencies before the path operation executes.

### 2. Dependencies Contribute to the OpenAPI Schema

**`get_openapi_path`** (`fastapi/openapi/utils.py:263–481`) is the key function that builds the OpenAPI entry for a route. Its behavior annotation shows it calls:
- `get_openapi_operation_metadata` — produces operation-level metadata (FOCUS entry, line 193).
- `_get_openapi_operation_parameters` — behavior `ACCUMULATE(parameter_groups loop -> parameters)`, which collects parameters from the dependency tree into the OpenAPI operation's parameter list (FOCUS entry, line 244).
- `get_openapi_operation_request_body` — behavior `GUARD(not body_field -> return None)`, which generates the request body schema (FOCUS entry, line 261).
- `get_openapi_security_definitions` — extracts security requirements from dependencies (FOCUS entry, line 186).

The `_get_openapi_operation_parameters` function takes `dependant=route.dependant`, showing it traverses the full dependency graph (not just the endpoint's own parameters) to collect query, path, header, and cookie parameters for schema generation.

### 3. Parameter Classification

The clue shows parameter type markers:
- `Path` (`fastapi/param_functions.py:14–355`) delegates to `params.Path` (`fastapi/params.py:138–219`), which extends `Param`.
- `Query` is implied by the same pattern.
- `Body` parameters and security dependencies also feed into the schema.

`add_non_field_param_to_dependency` (`fastapi/dependencies/utils.py:359–380`) has behavior `PRECEDENCE(type_annotation)`, and is called by `get_dependant`, indicating parameter classification is driven by type annotations.

### 4. Security Dependencies and Schema

Security classes like `APIKeyQuery` (`fastapi/security/api_key.py:53–142`), `APIKeyHeader` (line 145), and `APIKeyCookie` (line 233) all extend `APIKeyBase` and call `check_api_key`. They import `fastapi.openapi.models`, showing they contribute to the OpenAPI security definitions. The `get_openapi_security_definitions` call in `get_openapi_path` extracts these into the schema.

`DependencyScopeError` (`fastapi/exceptions.py:167–171`) extends `FastAPIError` and is described as "A dependency declared that it depends on another dependency with an invalid [scope]," confirming dependency scope validation exists.

### What Cannot Be Determined
GAPS states `type: STRUCTURAL` with uncovered symbols including `APIKeyIn`, `FastAPIDeprecationWarning`, `openapi`, and `custom_openapi`. The full internal logic of `solve_dependencies` — how it traverses the dependency graph, resolves caching, handles async vs sync — is not covered. The exact mechanism by which `get_dependant` classifies a parameter as path vs query vs body vs dependency cannot be fully traced from the clue alone.
