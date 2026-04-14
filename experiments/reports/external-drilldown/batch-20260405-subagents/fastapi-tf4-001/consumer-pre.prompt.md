You are running the BEFORE pass of a CodeClue drill-down evaluation.

Rules:
- Use ONLY the clue projection below.
- Do NOT use raw source code.
- Do NOT call MCP tools.
- If the clue is insufficient, say exactly what is missing.

Task ID: fastapi-tf4-001
Family: TF4
Operation Family: OF4

Question:
What happens when a sync dependency is used inside an async route in FastAPI? Is there a risk of blocking the event loop?

Return your answer in this format:

1. Answer
2. Clue sufficient: yes|no
3. Missing information:
   - ...
4. Confidence in your answer: low|medium|high

## Confidence Block
{
  "code_density_risk": 0.148649,
  "confidence_overall": 0.851351,
  "lookup_decision_hint": "clue_only",
  "operation_family": "OF4",
  "p_context_miss": 0.0,
  "p_dependency_miss": 0.0,
  "p_hallucination": 0.0,
  "per_edge_confidence": [
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:_extract_form_body:909:symbol:fastapi/dependencies/utils.py:_get_multidict_value:750:916",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:_extract_form_body:909:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:936",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:_extract_form_body:909:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:937",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:_get_multidict_value:750:symbol:fastapi/dependencies/utils.py:_is_json_field:746:755",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:_get_multidict_value:750:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:753",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:_should_embed_body_fields:885:symbol:fastapi/dependencies/utils.py:is_union_of_base_models:866:903",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:analyze_param:390:symbol:fastapi/dependencies/utils.py:ParamDetails:384:556",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:analyze_param:390:symbol:fastapi/dependencies/utils.py:ensure_multipart_is_installed:94:532",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_dependant:284:symbol:fastapi/dependencies/utils.py:add_non_field_param_to_dependency:359:342",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_dependant:284:symbol:fastapi/dependencies/utils.py:add_param_to_fields:559:355",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_dependant:284:symbol:fastapi/dependencies/utils.py:analyze_param:390:309",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_dependant:284:symbol:fastapi/dependencies/utils.py:get_dependant:284:331",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_dependant:284:symbol:fastapi/dependencies/utils.py:get_typed_signature:226:305",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_flat_dependant:136:symbol:fastapi/dependencies/utils.py:get_flat_dependant:136:173",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_flat_params:202:symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190:204",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_flat_params:202:symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190:205",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_flat_params:202:symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190:206",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_flat_params:202:symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190:207",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_flat_params:202:symbol:fastapi/dependencies/utils.py:get_flat_dependant:136:203",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_parameterless_sub_dependant:121:symbol:fastapi/dependencies/utils.py:get_dependant:284:128",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_typed_return_annotation:252:symbol:fastapi/dependencies/utils.py:_get_signature:211:253",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_typed_return_annotation:252:symbol:fastapi/dependencies/utils.py:get_typed_annotation:243:261",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_typed_signature:226:symbol:fastapi/dependencies/utils.py:_get_signature:211:227",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_typed_signature:226:symbol:fastapi/dependencies/utils.py:get_typed_annotation:243:235",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_body_to_args:948:symbol:fastapi/dependencies/utils.py:_extract_form_body:909:970",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_body_to_args:948:symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735:974",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_body_to_args:948:symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735:988",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_body_to_args:948:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:979",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_body_to_args:948:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:983",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:_get_multidict_value:750:822",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:_get_multidict_value:750:850",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735:844",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735:856",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:819",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:824",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:825",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:855",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:SolvedDependency:587:726",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:_solve_generator:575:669",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:get_dependant:284:638",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:request_body_to_args:948:703",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:682",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:685",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:688",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:691",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:646",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:docs_src/additional_responses/tutorial001_py310.py:symbol:docs_src/additional_responses/tutorial001_py310.py:Item:6",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:docs_src/additional_responses/tutorial001_py310.py:symbol:docs_src/additional_responses/tutorial001_py310.py:Message:11",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:docs_src/additional_responses/tutorial001_py310.py:symbol:docs_src/additional_responses/tutorial001_py310.py:read_item:19",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:docs_src/additional_responses/tutorial002_py310.py:symbol:docs_src/additional_responses/tutorial002_py310.py:Item:6",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:docs_src/additional_responses/tutorial002_py310.py:symbol:docs_src/additional_responses/tutorial002_py310.py:read_item:24",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:docs_src/additional_responses/tutorial003_py310.py:symbol:docs_src/additional_responses/tutorial003_py310.py:Item:6",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:docs_src/additional_responses/tutorial003_py310.py:symbol:docs_src/additional_responses/tutorial003_py310.py:Message:11",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:docs_src/additional_responses/tutorial003_py310.py:symbol:docs_src/additional_responses/tutorial003_py310.py:read_item:33",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:docs_src/additional_responses/tutorial004_py310.py:symbol:docs_src/additional_responses/tutorial004_py310.py:Item:6",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:docs_src/additional_responses/tutorial004_py310.py:symbol:docs_src/additional_responses/tutorial004_py310.py:read_item:26",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:docs_src/additional_status_codes/tutorial001_an_py310.py:symbol:docs_src/additional_status_codes/tutorial001_an_py310.py:upsert_item:12",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:docs_src/additional_status_codes/tutorial001_py310.py:symbol:docs_src/additional_status_codes/tutorial001_py310.py:upsert_item:10",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:docs_src/advanced_middleware/tutorial001_py310.py:symbol:docs_src/advanced_middleware/tutorial001_py310.py:main:10",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:docs_src/advanced_middleware/tutorial002_py310.py:symbol:docs_src/advanced_middleware/tutorial002_py310.py:main:12",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:docs_src/advanced_middleware/tutorial003_py310.py:symbol:docs_src/advanced_middleware/tutorial003_py310.py:main:10",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:docs_src/app_testing/app_a_py310/main.py:symbol:docs_src/app_testing/app_a_py310/main.py:read_main:7",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:docs_src/app_testing/app_b_an_py310/main.py:symbol:docs_src/app_testing/app_b_an_py310/main.py:Item:16",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:docs_src/app_testing/app_b_an_py310/main.py:symbol:docs_src/app_testing/app_b_an_py310/main.py:create_item:32",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:docs_src/app_testing/app_b_an_py310/main.py:symbol:docs_src/app_testing/app_b_an_py310/main.py:read_main:23",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:docs_src/async_tests/app_a_py310/main.py:symbol:docs_src/async_tests/app_a_py310/main.py:root:7",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:docs_src/async_tests/app_a_py310/test_main.py:symbol:docs_src/async_tests/app_a_py310/test_main.py:test_root:8",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/concurrency.py:symbol:fastapi/concurrency.py:contextmanager_in_threadpool:18",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:ParamDetails:384",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:SolvedDependency:587",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_extract_form_body:909",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_get_multidict_value:750",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_get_signature:211",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_is_json_field:746",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_should_embed_body_fields:885",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_solve_generator:575",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:add_non_field_param_to_dependency:359",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:add_param_to_fields:559",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:analyze_param:390",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:ensure_multipart_is_installed:94",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_body_field:998",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_dependant:284",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_flat_dependant:136",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_flat_params:202",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_parameterless_sub_dependant:121",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_stream_item_type:274",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_typed_annotation:243",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_typed_return_annotation:252",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_typed_signature:226",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:is_union_of_base_models:866",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:request_body_to_args:948",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/middleware/asyncexitstack.py:symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware.__call__:15",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/middleware/asyncexitstack.py:symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware.__init__:9",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:fastapi/middleware/asyncexitstack.py:symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware:8",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "contains:module:tests/test_tutorial/test_async_tests/test_main_a.py:symbol:tests/test_tutorial/test_async_tests/test_main_a.py:test_async_testing:7",
      "suggested_actions": []
    }
  ],
  "per_node_confidence": [
    {
      "confidence": 0.85,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 3,
        "fan_out_z_score": -0.21,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:docs_src/additional_responses/tutorial001_py310.py",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/additional_responses/tutorial001_py310.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.85,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 2,
        "fan_out_z_score": -0.334,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:docs_src/additional_responses/tutorial002_py310.py",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/additional_responses/tutorial002_py310.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.85,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 3,
        "fan_out_z_score": -0.21,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:docs_src/additional_responses/tutorial003_py310.py",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/additional_responses/tutorial003_py310.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.85,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 2,
        "fan_out_z_score": -0.334,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:docs_src/additional_responses/tutorial004_py310.py",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/additional_responses/tutorial004_py310.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.85,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": -0.459,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:docs_src/additional_status_codes/tutorial001_an_py310.py",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/additional_status_codes/tutorial001_an_py310.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.85,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": -0.459,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:docs_src/additional_status_codes/tutorial001_py310.py",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/additional_status_codes/tutorial001_py310.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.85,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": -0.459,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:docs_src/advanced_middleware/tutorial001_py310.py",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/advanced_middleware/tutorial001_py310.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.85,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": -0.459,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:docs_src/advanced_middleware/tutorial002_py310.py",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/advanced_middleware/tutorial002_py310.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.85,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": -0.459,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:docs_src/advanced_middleware/tutorial003_py310.py",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/advanced_middleware/tutorial003_py310.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.85,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": -0.459,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:docs_src/app_testing/app_a_py310/main.py",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/app_testing/app_a_py310/main.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.85,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 3,
        "fan_out_z_score": -0.21,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:docs_src/app_testing/app_b_an_py310/main.py",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/app_testing/app_b_an_py310/main.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.85,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.583,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:docs_src/async_tests/__init__.py",
      "suggested_actions": [],
      "tier": 1
    },
    {
      "confidence": 0.85,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.583,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:docs_src/async_tests/app_a_py310/__init__.py",
      "suggested_actions": [],
      "tier": 1
    },
    {
      "confidence": 0.85,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": -0.459,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:docs_src/async_tests/app_a_py310/main.py",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/async_tests/app_a_py310/main.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.85,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": -0.459,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:docs_src/async_tests/app_a_py310/test_main.py",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/async_tests/app_a_py310/test_main.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.85,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": -0.459,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:fastapi/concurrency.py",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/concurrency.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.65,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 28,
        "fan_out_z_score": 2.899,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:fastapi/dependencies/utils.py",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.85,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 3,
        "fan_out_z_score": -0.21,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:fastapi/middleware/asyncexitstack.py",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/middleware/asyncexitstack.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.85,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.583,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:tests/test_tutorial/test_async_tests/__init__.py",
      "suggested_actions": [],
      "tier": 1
    },
    {
      "confidence": 0.85,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": -0.459,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:tests/test_tutorial/test_async_tests/test_main_a.py",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "tests/test_tutorial/test_async_tests/test_main_a.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": 0.0,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:docs_src/additional_responses/tutorial001_py310.py:Item:6",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/additional_responses/tutorial001_py310.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": 0.0,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:docs_src/additional_responses/tutorial001_py310.py:Message:11",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/additional_responses/tutorial001_py310.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:docs_src/additional_responses/tutorial001_py310.py:read_item:19",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/additional_responses/tutorial001_py310.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": 0.0,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:docs_src/additional_responses/tutorial002_py310.py:Item:6",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/additional_responses/tutorial002_py310.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:docs_src/additional_responses/tutorial002_py310.py:read_item:24",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/additional_responses/tutorial002_py310.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": 0.0,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:docs_src/additional_responses/tutorial003_py310.py:Item:6",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/additional_responses/tutorial003_py310.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": 0.0,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:docs_src/additional_responses/tutorial003_py310.py:Message:11",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/additional_responses/tutorial003_py310.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:docs_src/additional_responses/tutorial003_py310.py:read_item:33",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/additional_responses/tutorial003_py310.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": 0.0,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:docs_src/additional_responses/tutorial004_py310.py:Item:6",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/additional_responses/tutorial004_py310.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:docs_src/additional_responses/tutorial004_py310.py:read_item:26",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/additional_responses/tutorial004_py310.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:docs_src/additional_status_codes/tutorial001_an_py310.py:upsert_item:12",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/additional_status_codes/tutorial001_an_py310.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:docs_src/additional_status_codes/tutorial001_py310.py:upsert_item:10",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/additional_status_codes/tutorial001_py310.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:docs_src/advanced_middleware/tutorial001_py310.py:main:10",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/advanced_middleware/tutorial001_py310.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:docs_src/advanced_middleware/tutorial002_py310.py:main:12",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/advanced_middleware/tutorial002_py310.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:docs_src/advanced_middleware/tutorial003_py310.py:main:10",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/advanced_middleware/tutorial003_py310.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:docs_src/app_testing/app_a_py310/main.py:read_main:7",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/app_testing/app_a_py310/main.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": 0.0,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:docs_src/app_testing/app_b_an_py310/main.py:Item:16",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/app_testing/app_b_an_py310/main.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:docs_src/app_testing/app_b_an_py310/main.py:create_item:32",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/app_testing/app_b_an_py310/main.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:docs_src/app_testing/app_b_an_py310/main.py:read_main:23",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/app_testing/app_b_an_py310/main.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:docs_src/async_tests/app_a_py310/main.py:root:7",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/async_tests/app_a_py310/main.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:docs_src/async_tests/app_a_py310/test_main.py:test_root:8",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "docs_src/async_tests/app_a_py310/test_main.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/concurrency.py:contextmanager_in_threadpool:18",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/concurrency.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": 0.0,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:ParamDetails:384",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": 0.0,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:SolvedDependency:587",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.57,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 3,
        "fan_out_z_score": 5.14,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:_extract_form_body:909",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.57,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 2,
        "fan_out_z_score": 2.411,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:_get_multidict_value:750",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:_get_signature:211",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:_is_json_field:746",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 1.088,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:_should_embed_body_fields:885",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:_solve_generator:575",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:add_non_field_param_to_dependency:359",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:add_param_to_fields:559",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.57,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 2,
        "fan_out_z_score": 2.411,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:analyze_param:390",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:ensure_multipart_is_installed:94",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:get_body_field:998",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.57,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 5,
        "fan_out_z_score": 6.381,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:get_dependant:284",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 1.088,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:get_flat_dependant:136",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.57,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 5,
        "fan_out_z_score": 6.381,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:get_flat_params:202",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 1.088,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:get_parameterless_sub_dependant:121",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:get_stream_item_type:274",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:get_typed_annotation:243",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.57,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 2,
        "fan_out_z_score": 2.411,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:get_typed_return_annotation:252",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.57,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 2,
        "fan_out_z_score": 2.411,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:get_typed_signature:226",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:is_union_of_base_models:866",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.57,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 5,
        "fan_out_z_score": 8.73,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:request_body_to_args:948",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.57,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 8,
        "fan_out_z_score": 10.351,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.57,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 9,
        "fan_out_z_score": 15.908,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware.__call__:15",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/middleware/asyncexitstack.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware.__init__:9",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/middleware/asyncexitstack.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": 0.0,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware:8",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "fastapi/middleware/asyncexitstack.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    },
    {
      "confidence": 0.77,
      "density_indicators": {
        "cross_file_span_ratio": 0.018,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:tests/test_tutorial/test_async_tests/test_main_a.py:test_async_testing:7",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "tests/test_tutorial/test_async_tests/test_main_a.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    }
  ],
  "threshold": 0.95,
  "tool_call_budget": 20
}

## Projection Stats
{
  "graph_edge_count": 6012,
  "graph_node_count": 6359,
  "initial_seed_count": 20,
  "projected_edge_count": 100,
  "projected_node_count": 74,
  "seed_count": 66
}

## Projected Nodes
[
  {
    "confidence": 1.0,
    "node_id": "module:docs_src/additional_responses/tutorial001_py310.py",
    "node_type": "module",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "Module-level semantic container",
      "symbol_name": "docs_src/additional_responses/tutorial001_py310.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 506,
      "byte_start": 0,
      "content_hash": "612da60c415c496d69abe57869aa440fbcda1d6c532d1e37432f7f136f28d0dd",
      "file_path": "docs_src/additional_responses/tutorial001_py310.py"
    }
  },
  {
    "confidence": 1.0,
    "node_id": "module:docs_src/additional_responses/tutorial002_py310.py",
    "node_type": "module",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "Module-level semantic container",
      "symbol_name": "docs_src/additional_responses/tutorial002_py310.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 596,
      "byte_start": 0,
      "content_hash": "9affbc269aa5ac588f3024310c39e02a79778160fe75901ad8c1468fb28bdae5",
      "file_path": "docs_src/additional_responses/tutorial002_py310.py"
    }
  },
  {
    "confidence": 1.0,
    "node_id": "module:docs_src/additional_responses/tutorial003_py310.py",
    "node_type": "module",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "Module-level semantic container",
      "symbol_name": "docs_src/additional_responses/tutorial003_py310.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 837,
      "byte_start": 0,
      "content_hash": "6fc74f39c96da18ac4d179ba3fc4dd0a035288e31022d91cfa49dbaf440c662c",
      "file_path": "docs_src/additional_responses/tutorial003_py310.py"
    }
  },
  {
    "confidence": 1.0,
    "node_id": "module:docs_src/additional_responses/tutorial004_py310.py",
    "node_type": "module",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "Module-level semantic container",
      "symbol_name": "docs_src/additional_responses/tutorial004_py310.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 669,
      "byte_start": 0,
      "content_hash": "cab81f82d4e279d5c8185830647e9c38c1d858730262e8a4666ecbb08fa48f9d",
      "file_path": "docs_src/additional_responses/tutorial004_py310.py"
    }
  },
  {
    "confidence": 1.0,
    "node_id": "module:docs_src/additional_status_codes/tutorial001_an_py310.py",
    "node_type": "module",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "Module-level semantic container",
      "symbol_name": "docs_src/additional_status_codes/tutorial001_an_py310.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 686,
      "byte_start": 0,
      "content_hash": "243ef632dea60a9492750e5f1c57411d6e050417c211f5fe8e9b11c6f4870783",
      "file_path": "docs_src/additional_status_codes/tutorial001_an_py310.py"
    }
  },
  {
    "confidence": 1.0,
    "node_id": "module:docs_src/additional_status_codes/tutorial001_py310.py",
    "node_type": "module",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "Module-level semantic container",
      "symbol_name": "docs_src/additional_status_codes/tutorial001_py310.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 646,
      "byte_start": 0,
      "content_hash": "51d2b5effdc47584b7c45d16cb7c163b6df8cbbea8ad4c5b3fd3f09bdc06e5c6",
      "file_path": "docs_src/additional_status_codes/tutorial001_py310.py"
    }
  },
  {
    "confidence": 1.0,
    "node_id": "module:docs_src/advanced_middleware/tutorial001_py310.py",
    "node_type": "module",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "Module-level semantic container",
      "symbol_name": "docs_src/advanced_middleware/tutorial001_py310.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 231,
      "byte_start": 0,
      "content_hash": "33e9e46c522fda0144e0223d58f2e1f18ee54da574ddf2d4aae68e2430b60f96",
      "file_path": "docs_src/advanced_middleware/tutorial001_py310.py"
    }
  },
  {
    "confidence": 1.0,
    "node_id": "module:docs_src/advanced_middleware/tutorial002_py310.py",
    "node_type": "module",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "Module-level semantic container",
      "symbol_name": "docs_src/advanced_middleware/tutorial002_py310.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 279,
      "byte_start": 0,
      "content_hash": "503289271cfef94141627667ffdee2584a289cb88a022dc26ee94bea5c2bd02c",
      "file_path": "docs_src/advanced_middleware/tutorial002_py310.py"
    }
  },
  {
    "confidence": 1.0,
    "node_id": "module:docs_src/advanced_middleware/tutorial003_py310.py",
    "node_type": "module",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "Module-level semantic container",
      "symbol_name": "docs_src/advanced_middleware/tutorial003_py310.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 230,
      "byte_start": 0,
      "content_hash": "d21fa2479c14650e0f63c4489504671b1d63e8376bd13e9db65e5437b8b7b45b",
      "file_path": "docs_src/advanced_middleware/tutorial003_py310.py"
    }
  },
  {
    "confidence": 1.0,
    "node_id": "module:docs_src/app_testing/app_a_py310/main.py",
    "node_type": "module",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "Module-level semantic container",
      "symbol_name": "docs_src/app_testing/app_a_py310/main.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 118,
      "byte_start": 0,
      "content_hash": "799a66ca241638380ba6e08101ed0da161b8635b4938b46fe30beb3694cb8ab0",
      "file_path": "docs_src/app_testing/app_a_py310/main.py"
    }
  },
  {
    "confidence": 1.0,
    "node_id": "module:docs_src/app_testing/app_b_an_py310/main.py",
    "node_type": "module",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "Module-level semantic container",
      "symbol_name": "docs_src/app_testing/app_b_an_py310/main.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 1163,
      "byte_start": 0,
      "content_hash": "bb5514b0dbea75e676a9447acf428d6a130727fa6a751c865cc302aaf476a053",
      "file_path": "docs_src/app_testing/app_b_an_py310/main.py"
    }
  },
  {
    "confidence": 1.0,
    "node_id": "module:docs_src/async_tests/__init__.py",
    "node_type": "module",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "Module-level semantic container",
      "symbol_name": "docs_src/async_tests/__init__.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 0,
      "byte_start": 0,
      "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "file_path": "docs_src/async_tests/__init__.py"
    }
  },
  {
    "confidence": 1.0,
    "node_id": "module:docs_src/async_tests/app_a_py310/__init__.py",
    "node_type": "module",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "Module-level semantic container",
      "symbol_name": "docs_src/async_tests/app_a_py310/__init__.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 0,
      "byte_start": 0,
      "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "file_path": "docs_src/async_tests/app_a_py310/__init__.py"
    }
  },
  {
    "confidence": 1.0,
    "node_id": "module:docs_src/async_tests/app_a_py310/main.py",
    "node_type": "module",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "Module-level semantic container",
      "symbol_name": "docs_src/async_tests/app_a_py310/main.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 112,
      "byte_start": 0,
      "content_hash": "f28e4cbedad7a9e0a8f72e6fb71a677c40a01977cf79f238b9e0f6402810e0ce",
      "file_path": "docs_src/async_tests/app_a_py310/main.py"
    }
  },
  {
    "confidence": 1.0,
    "node_id": "module:docs_src/async_tests/app_a_py310/test_main.py",
    "node_type": "module",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "Module-level semantic container",
      "symbol_name": "docs_src/async_tests/app_a_py310/test_main.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 360,
      "byte_start": 0,
      "content_hash": "a129755184f168aaa0f56307f4e43541ca6e5d392a185a3442983400ab3daffb",
      "file_path": "docs_src/async_tests/app_a_py310/test_main.py"
    }
  },
  {
    "confidence": 1.0,
    "node_id": "module:fastapi/concurrency.py",
    "node_type": "module",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "Module-level semantic container",
      "symbol_name": "fastapi/concurrency.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 1489,
      "byte_start": 0,
      "content_hash": "c4718310e40003a72f1440d7e3aa2adebdadd59778b15beb79a4607481388ee3",
      "file_path": "fastapi/concurrency.py"
    }
  },
  {
    "confidence": 1.0,
    "node_id": "module:fastapi/dependencies/utils.py",
    "node_type": "module",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "Module-level semantic container",
      "symbol_name": "fastapi/dependencies/utils.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 39276,
      "byte_start": 0,
      "content_hash": "434b0b2ade506c141727f9e91082093cbcc68e6b1417a417d7f9875dc5e56e9f",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 1.0,
    "node_id": "module:fastapi/middleware/asyncexitstack.py",
    "node_type": "module",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "Module-level semantic container",
      "symbol_name": "fastapi/middleware/asyncexitstack.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 637,
      "byte_start": 0,
      "content_hash": "44a1a54291b383718ba2ca9586bc41cbf34267da894bbcd078d1ede58df1fb4d",
      "file_path": "fastapi/middleware/asyncexitstack.py"
    }
  },
  {
    "confidence": 1.0,
    "node_id": "module:tests/test_tutorial/test_async_tests/__init__.py",
    "node_type": "module",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "Module-level semantic container",
      "symbol_name": "tests/test_tutorial/test_async_tests/__init__.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 0,
      "byte_start": 0,
      "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "file_path": "tests/test_tutorial/test_async_tests/__init__.py"
    }
  },
  {
    "confidence": 1.0,
    "node_id": "module:tests/test_tutorial/test_async_tests/test_main_a.py",
    "node_type": "module",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "Module-level semantic container",
      "symbol_name": "tests/test_tutorial/test_async_tests/test_main_a.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 155,
      "byte_start": 0,
      "content_hash": "8f119b37bfb8122479262f4db932d504d801f24cf3569976d88b35bdd1afd044",
      "file_path": "tests/test_tutorial/test_async_tests/test_main_a.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:docs_src/additional_responses/tutorial001_py310.py:Item:6",
    "node_type": "class",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "class Item",
      "symbol_name": "Item",
      "symbol_type": "class",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "class:Item",
      "byte_end": 153,
      "byte_start": 104,
      "content_hash": "833b82b5b70fbed783f61f2ee13958ac3c2efd1665b0149baa7cb3895a3c1862",
      "file_path": "docs_src/additional_responses/tutorial001_py310.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:docs_src/additional_responses/tutorial001_py310.py:Message:11",
    "node_type": "class",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "class Message",
      "symbol_name": "Message",
      "symbol_type": "class",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "class:Message",
      "byte_end": 198,
      "byte_start": 156,
      "content_hash": "6a4d8965350ccb3363b3fd7628d44665794c7b755a89d54d9da4a86fb16f9912",
      "file_path": "docs_src/additional_responses/tutorial001_py310.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:docs_src/additional_responses/tutorial001_py310.py:read_item:19",
    "node_type": "async_function",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "async_function read_item",
      "symbol_name": "read_item",
      "symbol_type": "async_function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "async_function:read_item",
      "byte_end": 505,
      "byte_start": 306,
      "content_hash": "98e752ca1bf5e928f959d52f862684c1ecaab6210eb589915f5e08b87cb46005",
      "file_path": "docs_src/additional_responses/tutorial001_py310.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:docs_src/additional_responses/tutorial002_py310.py:Item:6",
    "node_type": "class",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "class Item",
      "symbol_name": "Item",
      "symbol_type": "class",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "class:Item",
      "byte_end": 153,
      "byte_start": 104,
      "content_hash": "833b82b5b70fbed783f61f2ee13958ac3c2efd1665b0149baa7cb3895a3c1862",
      "file_path": "docs_src/additional_responses/tutorial002_py310.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:docs_src/additional_responses/tutorial002_py310.py:read_item:24",
    "node_type": "async_function",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "async_function read_item",
      "symbol_name": "read_item",
      "symbol_type": "async_function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "async_function:read_item",
      "byte_end": 595,
      "byte_start": 389,
      "content_hash": "0267b55467af313a8e10d36950fb51103ded1c50f628d1223ab8a856501a7b29",
      "file_path": "docs_src/additional_responses/tutorial002_py310.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:docs_src/additional_responses/tutorial003_py310.py:Item:6",
    "node_type": "class",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "class Item",
      "symbol_name": "Item",
      "symbol_type": "class",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "class:Item",
      "byte_end": 153,
      "byte_start": 104,
      "content_hash": "833b82b5b70fbed783f61f2ee13958ac3c2efd1665b0149baa7cb3895a3c1862",
      "file_path": "docs_src/additional_responses/tutorial003_py310.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:docs_src/additional_responses/tutorial003_py310.py:Message:11",
    "node_type": "class",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "class Message",
      "symbol_name": "Message",
      "symbol_type": "class",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "class:Message",
      "byte_end": 198,
      "byte_start": 156,
      "content_hash": "6a4d8965350ccb3363b3fd7628d44665794c7b755a89d54d9da4a86fb16f9912",
      "file_path": "docs_src/additional_responses/tutorial003_py310.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:docs_src/additional_responses/tutorial003_py310.py:read_item:33",
    "node_type": "async_function",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "async_function read_item",
      "symbol_name": "read_item",
      "symbol_type": "async_function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "async_function:read_item",
      "byte_end": 836,
      "byte_start": 623,
      "content_hash": "30e667a5ff2ad6105adc4dd3c35cc5c8554f23ee5b1da277015bace9135dfff8",
      "file_path": "docs_src/additional_responses/tutorial003_py310.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:docs_src/additional_responses/tutorial004_py310.py:Item:6",
    "node_type": "class",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "class Item",
      "symbol_name": "Item",
      "symbol_type": "class",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "class:Item",
      "byte_end": 153,
      "byte_start": 104,
      "content_hash": "833b82b5b70fbed783f61f2ee13958ac3c2efd1665b0149baa7cb3895a3c1862",
      "file_path": "docs_src/additional_responses/tutorial004_py310.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:docs_src/additional_responses/tutorial004_py310.py:read_item:26",
    "node_type": "async_function",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "async_function read_item",
      "symbol_name": "read_item",
      "symbol_type": "async_function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "async_function:read_item",
      "byte_end": 668,
      "byte_start": 462,
      "content_hash": "0267b55467af313a8e10d36950fb51103ded1c50f628d1223ab8a856501a7b29",
      "file_path": "docs_src/additional_responses/tutorial004_py310.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:docs_src/additional_status_codes/tutorial001_an_py310.py:upsert_item:12",
    "node_type": "async_function",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "async_function upsert_item",
      "symbol_name": "upsert_item",
      "symbol_type": "async_function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "async_function:upsert_item",
      "byte_end": 685,
      "byte_start": 252,
      "content_hash": "8f856d966c3f5246620fa05adfed32d409dd00fb740cf20f724861e9f6b38b3f",
      "file_path": "docs_src/additional_status_codes/tutorial001_an_py310.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:docs_src/additional_status_codes/tutorial001_py310.py:upsert_item:10",
    "node_type": "async_function",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "async_function upsert_item",
      "symbol_name": "upsert_item",
      "symbol_type": "async_function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "async_function:upsert_item",
      "byte_end": 645,
      "byte_start": 222,
      "content_hash": "f4bef2e04ebcd36012be1c81d05372c7d993ec12188234d278554b96e5258edd",
      "file_path": "docs_src/additional_status_codes/tutorial001_py310.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:docs_src/advanced_middleware/tutorial001_py310.py:main:10",
    "node_type": "async_function",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "async_function main",
      "symbol_name": "main",
      "symbol_type": "async_function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "async_function:main",
      "byte_end": 230,
      "byte_start": 175,
      "content_hash": "224af768dffdeeae2e2a33e9a3c4a5854557ec25bdf2989761f9d0300db65eea",
      "file_path": "docs_src/advanced_middleware/tutorial001_py310.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:docs_src/advanced_middleware/tutorial002_py310.py:main:12",
    "node_type": "async_function",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "async_function main",
      "symbol_name": "main",
      "symbol_type": "async_function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "async_function:main",
      "byte_end": 278,
      "byte_start": 223,
      "content_hash": "224af768dffdeeae2e2a33e9a3c4a5854557ec25bdf2989761f9d0300db65eea",
      "file_path": "docs_src/advanced_middleware/tutorial002_py310.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:docs_src/advanced_middleware/tutorial003_py310.py:main:10",
    "node_type": "async_function",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "async_function main",
      "symbol_name": "main",
      "symbol_type": "async_function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "async_function:main",
      "byte_end": 229,
      "byte_start": 184,
      "content_hash": "8cdf7c8b34d14c7d95ae84d95fa37b1a6dfe36622b0f75505fd86153e5befa4a",
      "file_path": "docs_src/advanced_middleware/tutorial003_py310.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:docs_src/app_testing/app_a_py310/main.py:read_main:7",
    "node_type": "async_function",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "async_function read_main",
      "symbol_name": "read_main",
      "symbol_type": "async_function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "async_function:read_main",
      "byte_end": 117,
      "byte_start": 61,
      "content_hash": "45c2ff112295f1634d82f2735207962f37de491a6dd3babaf40f37ab823fed4c",
      "file_path": "docs_src/app_testing/app_a_py310/main.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:docs_src/app_testing/app_b_an_py310/main.py:Item:16",
    "node_type": "class",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "class Item",
      "symbol_name": "Item",
      "symbol_type": "class",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "class:Item",
      "byte_end": 421,
      "byte_start": 337,
      "content_hash": "3eabe5818645b72d1fd60bfa09e477cbebd39aaed7dd6004a4e7fb5fe5f2d60c",
      "file_path": "docs_src/app_testing/app_b_an_py310/main.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:docs_src/app_testing/app_b_an_py310/main.py:create_item:32",
    "node_type": "async_function",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "async_function create_item",
      "symbol_name": "create_item",
      "symbol_type": "async_function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "async_function:create_item",
      "byte_end": 1162,
      "byte_start": 811,
      "content_hash": "cea88fe067ad30ea61d56b1a8b0565a653e394508eb60e53e040f70f6172180a",
      "file_path": "docs_src/app_testing/app_b_an_py310/main.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:docs_src/app_testing/app_b_an_py310/main.py:read_main:23",
    "node_type": "async_function",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "async_function read_main",
      "symbol_name": "read_main",
      "symbol_type": "async_function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "async_function:read_main",
      "byte_end": 787,
      "byte_start": 474,
      "content_hash": "16964a0ac0777ee9d754553d1c26e95ecb1dfe16f9ada8bc4d22882f8f514c7a",
      "file_path": "docs_src/app_testing/app_b_an_py310/main.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:docs_src/async_tests/app_a_py310/main.py:root:7",
    "node_type": "async_function",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "async_function root",
      "symbol_name": "root",
      "symbol_type": "async_function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "async_function:root",
      "byte_end": 111,
      "byte_start": 61,
      "content_hash": "f10a1df2d619042f0ab7e411c59116a0bd99d03078a5ffaf179215b78af3003d",
      "file_path": "docs_src/async_tests/app_a_py310/main.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:docs_src/async_tests/app_a_py310/test_main.py:test_root:8",
    "node_type": "async_function",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "async_function test_root",
      "symbol_name": "test_root",
      "symbol_type": "async_function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "async_function:test_root",
      "byte_end": 359,
      "byte_start": 103,
      "content_hash": "8a1c07015e2cfa2ed6247302ad562800438d219626a9d84eb59c17db6ec72459",
      "file_path": "docs_src/async_tests/app_a_py310/test_main.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/concurrency.py:contextmanager_in_threadpool:18",
    "node_type": "async_function",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "async_function contextmanager_in_threadpool",
      "symbol_name": "contextmanager_in_threadpool",
      "symbol_type": "async_function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "async_function:contextmanager_in_threadpool",
      "byte_end": 1488,
      "byte_start": 557,
      "content_hash": "4232d61205d9c955dad93fef003e540aaa709e990d3777695edf4c783ddcfae8",
      "file_path": "fastapi/concurrency.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:ParamDetails:384",
    "node_type": "class",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:fastapi/dependencies/utils.py:analyze_param:390"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "class ParamDetails",
      "symbol_name": "ParamDetails",
      "symbol_type": "class",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "class:ParamDetails",
      "byte_end": 13532,
      "byte_start": 13424,
      "content_hash": "c1444cd8def129d95a4cc46461041c98ae0eb9c9e8359d39da63cb43c23fc764",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:SolvedDependency:587",
    "node_type": "class",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "class SolvedDependency",
      "symbol_name": "SolvedDependency",
      "symbol_type": "class",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "class:SolvedDependency",
      "byte_end": 21742,
      "byte_start": 21541,
      "content_hash": "17f1cabd23e445c103c117bf837625d2e74793a50297bc9fa16f1ea5d10dc277",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:_extract_form_body:909",
    "node_type": "async_function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:fastapi/dependencies/utils.py:request_body_to_args:948"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:_get_multidict_value:750"
        },
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "async_function _extract_form_body",
      "symbol_name": "_extract_form_body",
      "symbol_type": "async_function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "async_function:_extract_form_body",
      "byte_end": 35319,
      "byte_start": 33895,
      "content_hash": "d0c31d7d344152d117b5da94ec81bffb19db87eff67f63efb4c3b18a3a9816de",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:fastapi/dependencies/utils.py:get_flat_params:202"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _get_flat_fields_from_params",
      "symbol_name": "_get_flat_fields_from_params",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:_get_flat_fields_from_params",
      "byte_end": 6744,
      "byte_start": 6350,
      "content_hash": "e7fa3732f0b0d987475fc3087ade88ed383741c991c69a78a7fd84830f5d1722",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:_get_multidict_value:750",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:fastapi/dependencies/utils.py:_extract_form_body:909"
        },
        {
          "source": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:_is_json_field:746"
        },
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _get_multidict_value",
      "symbol_name": "_get_multidict_value",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:_get_multidict_value",
      "byte_end": 28946,
      "byte_start": 28053,
      "content_hash": "8d7c2e1c739661fe24eeaf288c5faef1e754f315d9a6eceefdc981d913678d1b",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:_get_signature:211",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:fastapi/dependencies/utils.py:get_typed_return_annotation:252"
        },
        {
          "source": "symbol:fastapi/dependencies/utils.py:get_typed_signature:226"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _get_signature",
      "symbol_name": "_get_signature",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:_get_signature",
      "byte_end": 7788,
      "byte_start": 7262,
      "content_hash": "663852e9e7b0e861ddb9a4a5e1b3fc5bbee21e3231735197510eadbdc12cc9a5",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:_is_json_field:746",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:fastapi/dependencies/utils.py:_get_multidict_value:750"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _is_json_field",
      "symbol_name": "_is_json_field",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:_is_json_field",
      "byte_end": 28050,
      "byte_start": 27931,
      "content_hash": "6d206838173f40be73be0e7a1be1c0d7a499c6a81be048de5b1a35f79243ec6b",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:_should_embed_body_fields:885",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:is_union_of_base_models:866"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _should_embed_body_fields",
      "symbol_name": "_should_embed_body_fields",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:_should_embed_body_fields",
      "byte_end": 33892,
      "byte_start": 32834,
      "content_hash": "a18c3b6bc5eea3f937968abe2e8ffbe777728df2e1f536650f515c21973059de",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:_solve_generator:575",
    "node_type": "async_function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "async_function _solve_generator",
      "symbol_name": "_solve_generator",
      "symbol_type": "async_function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "async_function:_solve_generator",
      "byte_end": 21527,
      "byte_start": 21111,
      "content_hash": "69b9190419314723e2a125346a6e5337aeb2fba3bfbc451d7681ba9f79fa994a",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:fastapi/dependencies/utils.py:request_body_to_args:948"
        },
        {
          "source": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _validate_value_with_model_field",
      "symbol_name": "_validate_value_with_model_field",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:_validate_value_with_model_field",
      "byte_end": 27928,
      "byte_start": 27544,
      "content_hash": "45ff8393dec2ebe41da7639903479f9374218d1af90e68017d415c02f4600073",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:add_non_field_param_to_dependency:359",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:fastapi/dependencies/utils.py:get_dependant:284"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function add_non_field_param_to_dependency",
      "symbol_name": "add_non_field_param_to_dependency",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:add_non_field_param_to_dependency",
      "byte_end": 13410,
      "byte_start": 12461,
      "content_hash": "450c1b66c8f8cb9dc935d6bf323506515f2a443c5532ecf67ec8d08258ceb4f6",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:add_param_to_fields:559",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:fastapi/dependencies/utils.py:get_dependant:284"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function add_param_to_fields",
      "symbol_name": "add_param_to_fields",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:add_param_to_fields",
      "byte_end": 21108,
      "byte_start": 20443,
      "content_hash": "5f87238254caa48893aeabbf1d4a475149db99debb72fd88c6000171840fb8cc",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:analyze_param:390",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:fastapi/dependencies/utils.py:get_dependant:284"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:ParamDetails:384"
        },
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:ensure_multipart_is_installed:94"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function analyze_param",
      "symbol_name": "analyze_param",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:analyze_param",
      "byte_end": 20440,
      "byte_start": 13535,
      "content_hash": "b361897cfff040ddd4e277e7709b4971b9736f91a8b3418813ad121e3ec124cf",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:ensure_multipart_is_installed:94",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:fastapi/dependencies/utils.py:analyze_param:390"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function ensure_multipart_is_installed",
      "symbol_name": "ensure_multipart_is_installed",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:ensure_multipart_is_installed",
      "byte_end": 3657,
      "byte_start": 2581,
      "content_hash": "381f46b8715314c1d6f1dd4648664bd3c6ba8ef907dd2191773e6f719527183c",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:get_body_field:998",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function get_body_field",
      "symbol_name": "get_body_field",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:get_body_field",
      "byte_end": 39142,
      "byte_start": 37214,
      "content_hash": "d7f1fce5ec6d6b10b5d03e86e2ae672c27e11cc95caa6ed756c87f0ad7ffc4fc",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:get_dependant:284",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:fastapi/dependencies/utils.py:get_dependant:284"
        },
        {
          "source": "symbol:fastapi/dependencies/utils.py:get_parameterless_sub_dependant:121"
        },
        {
          "source": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:add_non_field_param_to_dependency:359"
        },
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:add_param_to_fields:559"
        },
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:analyze_param:390"
        },
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:get_dependant:284"
        },
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:get_typed_signature:226"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function get_dependant",
      "symbol_name": "get_dependant",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:get_dependant",
      "byte_end": 12458,
      "byte_start": 9437,
      "content_hash": "e00aac4b07348f1448adca1ce1aabddcd9c5dd7f53353a63c1237af7eb8948d1",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:get_flat_dependant:136",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:fastapi/dependencies/utils.py:get_flat_dependant:136"
        },
        {
          "source": "symbol:fastapi/dependencies/utils.py:get_flat_params:202"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:get_flat_dependant:136"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function get_flat_dependant",
      "symbol_name": "get_flat_dependant",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:get_flat_dependant",
      "byte_end": 6347,
      "byte_start": 4175,
      "content_hash": "a4a8ee34e9b604a3c8fa5d7f1e730407887a0e63e154dd4f2073d799313e372b",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:get_flat_params:202",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190"
        },
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:get_flat_dependant:136"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function get_flat_params",
      "symbol_name": "get_flat_params",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:get_flat_params",
      "byte_end": 7259,
      "byte_start": 6747,
      "content_hash": "b633d01dda801c969ab2a5825e5129125d375d68f4d72a0baa903c3bf62de18e",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:get_parameterless_sub_dependant:121",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:get_dependant:284"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function get_parameterless_sub_dependant",
      "symbol_name": "get_parameterless_sub_dependant",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:get_parameterless_sub_dependant",
      "byte_end": 4172,
      "byte_start": 3660,
      "content_hash": "77bc961c0548a30f9eece029295419f3d089d841498f7849ad638a06525343e4",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:get_stream_item_type:274",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function get_stream_item_type",
      "symbol_name": "get_stream_item_type",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:get_stream_item_type",
      "byte_end": 9434,
      "byte_start": 9155,
      "content_hash": "21d183b79cc4a3b13465d8afba47bb5445a83013ea3d0245d50191d5a3332d9e",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:get_typed_annotation:243",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:fastapi/dependencies/utils.py:get_typed_return_annotation:252"
        },
        {
          "source": "symbol:fastapi/dependencies/utils.py:get_typed_signature:226"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function get_typed_annotation",
      "symbol_name": "get_typed_annotation",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:get_typed_annotation",
      "byte_end": 8665,
      "byte_start": 8354,
      "content_hash": "33955de14066a1aea1b9a33296282eb6dd1ca35ae79c05ad0c37080562ac1a64",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:get_typed_return_annotation:252",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:_get_signature:211"
        },
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:get_typed_annotation:243"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function get_typed_return_annotation",
      "symbol_name": "get_typed_return_annotation",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:get_typed_return_annotation",
      "byte_end": 9027,
      "byte_start": 8668,
      "content_hash": "9a13036e2b1f0a4a292e037093d0cd72e2567127e727290e7d681c49a8b6384f",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:get_typed_signature:226",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:fastapi/dependencies/utils.py:get_dependant:284"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:_get_signature:211"
        },
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:get_typed_annotation:243"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function get_typed_signature",
      "symbol_name": "get_typed_signature",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:get_typed_signature",
      "byte_end": 8351,
      "byte_start": 7791,
      "content_hash": "9a4baef3c22a8bd8b472712104f6eae5531313c75cd28bd355f047a75cd47d0d",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:fastapi/dependencies/utils.py:_extract_form_body:909"
        },
        {
          "source": "symbol:fastapi/dependencies/utils.py:_get_multidict_value:750"
        },
        {
          "source": "symbol:fastapi/dependencies/utils.py:request_body_to_args:948"
        },
        {
          "source": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function get_validation_alias",
      "symbol_name": "get_validation_alias",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:get_validation_alias",
      "byte_end": 39275,
      "byte_start": 39145,
      "content_hash": "126b3a08e19782bfb21429df9b502fb925efa8913a4072800ed27601776d81a1",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:is_union_of_base_models:866",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:fastapi/dependencies/utils.py:_should_embed_body_fields:885"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function is_union_of_base_models",
      "symbol_name": "is_union_of_base_models",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:is_union_of_base_models",
      "byte_end": 32831,
      "byte_start": 32282,
      "content_hash": "44c69a85969d4e1ae3ce8de1b9eff4fc328789a76d2b01151b2345f89d8d01d9",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:request_body_to_args:948",
    "node_type": "async_function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:_extract_form_body:909"
        },
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735"
        },
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "async_function request_body_to_args",
      "symbol_name": "request_body_to_args",
      "symbol_type": "async_function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "async_function:request_body_to_args",
      "byte_end": 37211,
      "byte_start": 35322,
      "content_hash": "8b24311a51620699020243d703be0d01d7928dc3b1ce83567aca538d06bdf0d8",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:_get_multidict_value:750"
        },
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735"
        },
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function request_params_to_args",
      "symbol_name": "request_params_to_args",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:request_params_to_args",
      "byte_end": 32279,
      "byte_start": 28949,
      "content_hash": "056f212ccf6614ff42b30323bf31e44bf3b90eddff266d203897ff7f45c8fdef",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
    "node_type": "async_function",
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:SolvedDependency:587"
        },
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:_solve_generator:575"
        },
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:get_dependant:284"
        },
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:request_body_to_args:948"
        },
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781"
        },
        {
          "is_external": false,
          "target": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "async_function solve_dependencies",
      "symbol_name": "solve_dependencies",
      "symbol_type": "async_function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "async_function:solve_dependencies",
      "byte_end": 27541,
      "byte_start": 21745,
      "content_hash": "7d6d2f9927bbee7ceafbfdb69a6b5b5cdd62d998edf08f1c3489be1a8782796d",
      "file_path": "fastapi/dependencies/utils.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware.__call__:15",
    "node_type": "async_function",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "async_function __call__",
      "symbol_name": "__call__",
      "symbol_type": "async_function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "async_function:AsyncExitStackMiddleware.__call__",
      "byte_end": 636,
      "byte_start": 419,
      "content_hash": "4ac933ba1dc0080f5f33f5d1bcef363805f15bd57f699de49df2de01818ec5bc",
      "file_path": "fastapi/middleware/asyncexitstack.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware.__init__:9",
    "node_type": "function",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function __init__",
      "symbol_name": "__init__",
      "symbol_type": "function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "function:AsyncExitStackMiddleware.__init__",
      "byte_end": 413,
      "byte_start": 245,
      "content_hash": "9f69aad72d1a866ab554b3c908032f08435f6c5cf503482ae675bf006c6ca856",
      "file_path": "fastapi/middleware/asyncexitstack.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware:8",
    "node_type": "class",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "class AsyncExitStackMiddleware",
      "symbol_name": "AsyncExitStackMiddleware",
      "symbol_type": "class",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "class:AsyncExitStackMiddleware",
      "byte_end": 636,
      "byte_start": 209,
      "content_hash": "aafdef3eed0fc0fb00898f6f94a860f465678efa51fd16f4e2f6acb60c28fac7",
      "file_path": "fastapi/middleware/asyncexitstack.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:tests/test_tutorial/test_async_tests/test_main_a.py:test_async_testing:7",
    "node_type": "async_function",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "async_function test_async_testing",
      "symbol_name": "test_async_testing",
      "symbol_type": "async_function",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "async_function:test_async_testing",
      "byte_end": 154,
      "byte_start": 101,
      "content_hash": "9ed6bd4a20ca618505243d4dcca4a32c75b59412b57a8bad6f6a69670da40aea",
      "file_path": "tests/test_tutorial/test_async_tests/test_main_a.py"
    }
  }
]

## Projected Edges
[
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:_extract_form_body:909:symbol:fastapi/dependencies/utils.py:_get_multidict_value:750:916",
    "edge_type": "calls",
    "evidence": {
      "line": 916,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:_extract_form_body:909",
    "to_node": "symbol:fastapi/dependencies/utils.py:_get_multidict_value:750"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:_extract_form_body:909:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:936",
    "edge_type": "calls",
    "evidence": {
      "line": 936,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:_extract_form_body:909",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:_extract_form_body:909:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:937",
    "edge_type": "calls",
    "evidence": {
      "line": 937,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:_extract_form_body:909",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:_get_multidict_value:750:symbol:fastapi/dependencies/utils.py:_is_json_field:746:755",
    "edge_type": "calls",
    "evidence": {
      "line": 755,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:_get_multidict_value:750",
    "to_node": "symbol:fastapi/dependencies/utils.py:_is_json_field:746"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:_get_multidict_value:750:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:753",
    "edge_type": "calls",
    "evidence": {
      "line": 753,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:_get_multidict_value:750",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:_should_embed_body_fields:885:symbol:fastapi/dependencies/utils.py:is_union_of_base_models:866:903",
    "edge_type": "calls",
    "evidence": {
      "line": 903,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:_should_embed_body_fields:885",
    "to_node": "symbol:fastapi/dependencies/utils.py:is_union_of_base_models:866"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:analyze_param:390:symbol:fastapi/dependencies/utils.py:ParamDetails:384:556",
    "edge_type": "calls",
    "evidence": {
      "line": 556,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:analyze_param:390",
    "to_node": "symbol:fastapi/dependencies/utils.py:ParamDetails:384"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:analyze_param:390:symbol:fastapi/dependencies/utils.py:ensure_multipart_is_installed:94:532",
    "edge_type": "calls",
    "evidence": {
      "line": 532,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:analyze_param:390",
    "to_node": "symbol:fastapi/dependencies/utils.py:ensure_multipart_is_installed:94"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_dependant:284:symbol:fastapi/dependencies/utils.py:add_non_field_param_to_dependency:359:342",
    "edge_type": "calls",
    "evidence": {
      "line": 342,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:get_dependant:284",
    "to_node": "symbol:fastapi/dependencies/utils.py:add_non_field_param_to_dependency:359"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_dependant:284:symbol:fastapi/dependencies/utils.py:add_param_to_fields:559:355",
    "edge_type": "calls",
    "evidence": {
      "line": 355,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:get_dependant:284",
    "to_node": "symbol:fastapi/dependencies/utils.py:add_param_to_fields:559"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_dependant:284:symbol:fastapi/dependencies/utils.py:analyze_param:390:309",
    "edge_type": "calls",
    "evidence": {
      "line": 309,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:get_dependant:284",
    "to_node": "symbol:fastapi/dependencies/utils.py:analyze_param:390"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_dependant:284:symbol:fastapi/dependencies/utils.py:get_dependant:284:331",
    "edge_type": "calls",
    "evidence": {
      "line": 331,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:get_dependant:284",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_dependant:284"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_dependant:284:symbol:fastapi/dependencies/utils.py:get_typed_signature:226:305",
    "edge_type": "calls",
    "evidence": {
      "line": 305,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:get_dependant:284",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_typed_signature:226"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_flat_dependant:136:symbol:fastapi/dependencies/utils.py:get_flat_dependant:136:173",
    "edge_type": "calls",
    "evidence": {
      "line": 173,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:get_flat_dependant:136",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_flat_dependant:136"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_flat_params:202:symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190:204",
    "edge_type": "calls",
    "evidence": {
      "line": 204,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:get_flat_params:202",
    "to_node": "symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_flat_params:202:symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190:205",
    "edge_type": "calls",
    "evidence": {
      "line": 205,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:get_flat_params:202",
    "to_node": "symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_flat_params:202:symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190:206",
    "edge_type": "calls",
    "evidence": {
      "line": 206,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:get_flat_params:202",
    "to_node": "symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_flat_params:202:symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190:207",
    "edge_type": "calls",
    "evidence": {
      "line": 207,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:get_flat_params:202",
    "to_node": "symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_flat_params:202:symbol:fastapi/dependencies/utils.py:get_flat_dependant:136:203",
    "edge_type": "calls",
    "evidence": {
      "line": 203,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:get_flat_params:202",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_flat_dependant:136"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_parameterless_sub_dependant:121:symbol:fastapi/dependencies/utils.py:get_dependant:284:128",
    "edge_type": "calls",
    "evidence": {
      "line": 128,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:get_parameterless_sub_dependant:121",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_dependant:284"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_typed_return_annotation:252:symbol:fastapi/dependencies/utils.py:_get_signature:211:253",
    "edge_type": "calls",
    "evidence": {
      "line": 253,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:get_typed_return_annotation:252",
    "to_node": "symbol:fastapi/dependencies/utils.py:_get_signature:211"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_typed_return_annotation:252:symbol:fastapi/dependencies/utils.py:get_typed_annotation:243:261",
    "edge_type": "calls",
    "evidence": {
      "line": 261,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:get_typed_return_annotation:252",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_typed_annotation:243"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_typed_signature:226:symbol:fastapi/dependencies/utils.py:_get_signature:211:227",
    "edge_type": "calls",
    "evidence": {
      "line": 227,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:get_typed_signature:226",
    "to_node": "symbol:fastapi/dependencies/utils.py:_get_signature:211"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_typed_signature:226:symbol:fastapi/dependencies/utils.py:get_typed_annotation:243:235",
    "edge_type": "calls",
    "evidence": {
      "line": 235,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:get_typed_signature:226",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_typed_annotation:243"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_body_to_args:948:symbol:fastapi/dependencies/utils.py:_extract_form_body:909:970",
    "edge_type": "calls",
    "evidence": {
      "line": 970,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:request_body_to_args:948",
    "to_node": "symbol:fastapi/dependencies/utils.py:_extract_form_body:909"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_body_to_args:948:symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735:974",
    "edge_type": "calls",
    "evidence": {
      "line": 974,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:request_body_to_args:948",
    "to_node": "symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_body_to_args:948:symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735:988",
    "edge_type": "calls",
    "evidence": {
      "line": 988,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:request_body_to_args:948",
    "to_node": "symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_body_to_args:948:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:979",
    "edge_type": "calls",
    "evidence": {
      "line": 979,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:request_body_to_args:948",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_body_to_args:948:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:983",
    "edge_type": "calls",
    "evidence": {
      "line": 983,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:request_body_to_args:948",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:_get_multidict_value:750:822",
    "edge_type": "calls",
    "evidence": {
      "line": 822,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "to_node": "symbol:fastapi/dependencies/utils.py:_get_multidict_value:750"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:_get_multidict_value:750:850",
    "edge_type": "calls",
    "evidence": {
      "line": 850,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "to_node": "symbol:fastapi/dependencies/utils.py:_get_multidict_value:750"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735:844",
    "edge_type": "calls",
    "evidence": {
      "line": 844,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "to_node": "symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735:856",
    "edge_type": "calls",
    "evidence": {
      "line": 856,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "to_node": "symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:819",
    "edge_type": "calls",
    "evidence": {
      "line": 819,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:824",
    "edge_type": "calls",
    "evidence": {
      "line": 824,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:825",
    "edge_type": "calls",
    "evidence": {
      "line": 825,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:855",
    "edge_type": "calls",
    "evidence": {
      "line": 855,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:SolvedDependency:587:726",
    "edge_type": "calls",
    "evidence": {
      "line": 726,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
    "to_node": "symbol:fastapi/dependencies/utils.py:SolvedDependency:587"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:_solve_generator:575:669",
    "edge_type": "calls",
    "evidence": {
      "line": 669,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
    "to_node": "symbol:fastapi/dependencies/utils.py:_solve_generator:575"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:get_dependant:284:638",
    "edge_type": "calls",
    "evidence": {
      "line": 638,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_dependant:284"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:request_body_to_args:948:703",
    "edge_type": "calls",
    "evidence": {
      "line": 703,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
    "to_node": "symbol:fastapi/dependencies/utils.py:request_body_to_args:948"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:682",
    "edge_type": "calls",
    "evidence": {
      "line": 682,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
    "to_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:685",
    "edge_type": "calls",
    "evidence": {
      "line": 685,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
    "to_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:688",
    "edge_type": "calls",
    "evidence": {
      "line": 688,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
    "to_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:691",
    "edge_type": "calls",
    "evidence": {
      "line": 691,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
    "to_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781"
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:646",
    "edge_type": "calls",
    "evidence": {
      "line": 646,
      "rel": "ast_call"
    },
    "from_node": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
    "to_node": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595"
  },
  {
    "edge_id": "contains:module:docs_src/additional_responses/tutorial001_py310.py:symbol:docs_src/additional_responses/tutorial001_py310.py:Item:6",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:docs_src/additional_responses/tutorial001_py310.py",
    "to_node": "symbol:docs_src/additional_responses/tutorial001_py310.py:Item:6"
  },
  {
    "edge_id": "contains:module:docs_src/additional_responses/tutorial001_py310.py:symbol:docs_src/additional_responses/tutorial001_py310.py:Message:11",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:docs_src/additional_responses/tutorial001_py310.py",
    "to_node": "symbol:docs_src/additional_responses/tutorial001_py310.py:Message:11"
  },
  {
    "edge_id": "contains:module:docs_src/additional_responses/tutorial001_py310.py:symbol:docs_src/additional_responses/tutorial001_py310.py:read_item:19",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:docs_src/additional_responses/tutorial001_py310.py",
    "to_node": "symbol:docs_src/additional_responses/tutorial001_py310.py:read_item:19"
  },
  {
    "edge_id": "contains:module:docs_src/additional_responses/tutorial002_py310.py:symbol:docs_src/additional_responses/tutorial002_py310.py:Item:6",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:docs_src/additional_responses/tutorial002_py310.py",
    "to_node": "symbol:docs_src/additional_responses/tutorial002_py310.py:Item:6"
  },
  {
    "edge_id": "contains:module:docs_src/additional_responses/tutorial002_py310.py:symbol:docs_src/additional_responses/tutorial002_py310.py:read_item:24",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:docs_src/additional_responses/tutorial002_py310.py",
    "to_node": "symbol:docs_src/additional_responses/tutorial002_py310.py:read_item:24"
  },
  {
    "edge_id": "contains:module:docs_src/additional_responses/tutorial003_py310.py:symbol:docs_src/additional_responses/tutorial003_py310.py:Item:6",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:docs_src/additional_responses/tutorial003_py310.py",
    "to_node": "symbol:docs_src/additional_responses/tutorial003_py310.py:Item:6"
  },
  {
    "edge_id": "contains:module:docs_src/additional_responses/tutorial003_py310.py:symbol:docs_src/additional_responses/tutorial003_py310.py:Message:11",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:docs_src/additional_responses/tutorial003_py310.py",
    "to_node": "symbol:docs_src/additional_responses/tutorial003_py310.py:Message:11"
  },
  {
    "edge_id": "contains:module:docs_src/additional_responses/tutorial003_py310.py:symbol:docs_src/additional_responses/tutorial003_py310.py:read_item:33",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:docs_src/additional_responses/tutorial003_py310.py",
    "to_node": "symbol:docs_src/additional_responses/tutorial003_py310.py:read_item:33"
  },
  {
    "edge_id": "contains:module:docs_src/additional_responses/tutorial004_py310.py:symbol:docs_src/additional_responses/tutorial004_py310.py:Item:6",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:docs_src/additional_responses/tutorial004_py310.py",
    "to_node": "symbol:docs_src/additional_responses/tutorial004_py310.py:Item:6"
  },
  {
    "edge_id": "contains:module:docs_src/additional_responses/tutorial004_py310.py:symbol:docs_src/additional_responses/tutorial004_py310.py:read_item:26",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:docs_src/additional_responses/tutorial004_py310.py",
    "to_node": "symbol:docs_src/additional_responses/tutorial004_py310.py:read_item:26"
  },
  {
    "edge_id": "contains:module:docs_src/additional_status_codes/tutorial001_an_py310.py:symbol:docs_src/additional_status_codes/tutorial001_an_py310.py:upsert_item:12",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:docs_src/additional_status_codes/tutorial001_an_py310.py",
    "to_node": "symbol:docs_src/additional_status_codes/tutorial001_an_py310.py:upsert_item:12"
  },
  {
    "edge_id": "contains:module:docs_src/additional_status_codes/tutorial001_py310.py:symbol:docs_src/additional_status_codes/tutorial001_py310.py:upsert_item:10",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:docs_src/additional_status_codes/tutorial001_py310.py",
    "to_node": "symbol:docs_src/additional_status_codes/tutorial001_py310.py:upsert_item:10"
  },
  {
    "edge_id": "contains:module:docs_src/advanced_middleware/tutorial001_py310.py:symbol:docs_src/advanced_middleware/tutorial001_py310.py:main:10",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:docs_src/advanced_middleware/tutorial001_py310.py",
    "to_node": "symbol:docs_src/advanced_middleware/tutorial001_py310.py:main:10"
  },
  {
    "edge_id": "contains:module:docs_src/advanced_middleware/tutorial002_py310.py:symbol:docs_src/advanced_middleware/tutorial002_py310.py:main:12",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:docs_src/advanced_middleware/tutorial002_py310.py",
    "to_node": "symbol:docs_src/advanced_middleware/tutorial002_py310.py:main:12"
  },
  {
    "edge_id": "contains:module:docs_src/advanced_middleware/tutorial003_py310.py:symbol:docs_src/advanced_middleware/tutorial003_py310.py:main:10",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:docs_src/advanced_middleware/tutorial003_py310.py",
    "to_node": "symbol:docs_src/advanced_middleware/tutorial003_py310.py:main:10"
  },
  {
    "edge_id": "contains:module:docs_src/app_testing/app_a_py310/main.py:symbol:docs_src/app_testing/app_a_py310/main.py:read_main:7",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:docs_src/app_testing/app_a_py310/main.py",
    "to_node": "symbol:docs_src/app_testing/app_a_py310/main.py:read_main:7"
  },
  {
    "edge_id": "contains:module:docs_src/app_testing/app_b_an_py310/main.py:symbol:docs_src/app_testing/app_b_an_py310/main.py:Item:16",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:docs_src/app_testing/app_b_an_py310/main.py",
    "to_node": "symbol:docs_src/app_testing/app_b_an_py310/main.py:Item:16"
  },
  {
    "edge_id": "contains:module:docs_src/app_testing/app_b_an_py310/main.py:symbol:docs_src/app_testing/app_b_an_py310/main.py:create_item:32",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:docs_src/app_testing/app_b_an_py310/main.py",
    "to_node": "symbol:docs_src/app_testing/app_b_an_py310/main.py:create_item:32"
  },
  {
    "edge_id": "contains:module:docs_src/app_testing/app_b_an_py310/main.py:symbol:docs_src/app_testing/app_b_an_py310/main.py:read_main:23",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:docs_src/app_testing/app_b_an_py310/main.py",
    "to_node": "symbol:docs_src/app_testing/app_b_an_py310/main.py:read_main:23"
  },
  {
    "edge_id": "contains:module:docs_src/async_tests/app_a_py310/main.py:symbol:docs_src/async_tests/app_a_py310/main.py:root:7",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:docs_src/async_tests/app_a_py310/main.py",
    "to_node": "symbol:docs_src/async_tests/app_a_py310/main.py:root:7"
  },
  {
    "edge_id": "contains:module:docs_src/async_tests/app_a_py310/test_main.py:symbol:docs_src/async_tests/app_a_py310/test_main.py:test_root:8",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:docs_src/async_tests/app_a_py310/test_main.py",
    "to_node": "symbol:docs_src/async_tests/app_a_py310/test_main.py:test_root:8"
  },
  {
    "edge_id": "contains:module:fastapi/concurrency.py:symbol:fastapi/concurrency.py:contextmanager_in_threadpool:18",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/concurrency.py",
    "to_node": "symbol:fastapi/concurrency.py:contextmanager_in_threadpool:18"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:ParamDetails:384",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:ParamDetails:384"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:SolvedDependency:587",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:SolvedDependency:587"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_extract_form_body:909",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:_extract_form_body:909"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_get_multidict_value:750",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:_get_multidict_value:750"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_get_signature:211",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:_get_signature:211"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_is_json_field:746",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:_is_json_field:746"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_should_embed_body_fields:885",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:_should_embed_body_fields:885"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_solve_generator:575",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:_solve_generator:575"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:add_non_field_param_to_dependency:359",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:add_non_field_param_to_dependency:359"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:add_param_to_fields:559",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:add_param_to_fields:559"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:analyze_param:390",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:analyze_param:390"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:ensure_multipart_is_installed:94",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:ensure_multipart_is_installed:94"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_body_field:998",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_body_field:998"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_dependant:284",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_dependant:284"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_flat_dependant:136",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_flat_dependant:136"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_flat_params:202",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_flat_params:202"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_parameterless_sub_dependant:121",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_parameterless_sub_dependant:121"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_stream_item_type:274",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_stream_item_type:274"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_typed_annotation:243",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_typed_annotation:243"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_typed_return_annotation:252",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_typed_return_annotation:252"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_typed_signature:226",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_typed_signature:226"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:is_union_of_base_models:866",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:is_union_of_base_models:866"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:request_body_to_args:948",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:request_body_to_args:948"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781"
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595"
  },
  {
    "edge_id": "contains:module:fastapi/middleware/asyncexitstack.py:symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware.__call__:15",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/middleware/asyncexitstack.py",
    "to_node": "symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware.__call__:15"
  },
  {
    "edge_id": "contains:module:fastapi/middleware/asyncexitstack.py:symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware.__init__:9",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/middleware/asyncexitstack.py",
    "to_node": "symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware.__init__:9"
  },
  {
    "edge_id": "contains:module:fastapi/middleware/asyncexitstack.py:symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware:8",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:fastapi/middleware/asyncexitstack.py",
    "to_node": "symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware:8"
  },
  {
    "edge_id": "contains:module:tests/test_tutorial/test_async_tests/test_main_a.py:symbol:tests/test_tutorial/test_async_tests/test_main_a.py:test_async_testing:7",
    "edge_type": "contains",
    "evidence": {
      "rel": "ast_containment"
    },
    "from_node": "module:tests/test_tutorial/test_async_tests/test_main_a.py",
    "to_node": "symbol:tests/test_tutorial/test_async_tests/test_main_a.py:test_async_testing:7"
  }
]
