You are running the AFTER pass of a CodeClue drill-down evaluation.

Rules:
- Start from the same clue projection below.
- Use the automated MCP drill-down evidence below as your only post-clue evidence.
- Do NOT inspect any other source beyond what is included in this prompt.
- Produce a revised answer that clearly reflects what the drill-down changed.

Task ID: fastapi-tf4-001
Family: TF4
Operation Family: OF4

Question:
What happens when a sync dependency is used inside an async route in FastAPI? Is there a risk of blocking the event loop?

Return your answer in this format:

1. Revised answer
2. Tool evidence used:
   - tool name + what it contributed
3. What changed after drill-down:
   - ...
4. Remaining uncertainty:
   - ...
5. Final confidence: low|medium|high

## Confidence Block
{
  "p_context_miss": 0.0,
  "p_dependency_miss": 0.0,
  "p_hallucination": 0.0,
  "code_density_risk": 0.148649,
  "confidence_overall": 0.851351,
  "lookup_decision_hint": "clue_only",
  "operation_family": "OF4",
  "threshold": 0.95,
  "tool_call_budget": 20,
  "per_node_confidence": [
    {
      "node_id": "module:docs_src/additional_responses/tutorial001_py310.py",
      "confidence": 0.85,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 3,
        "fan_out_z_score": -0.21,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/additional_responses/tutorial001_py310.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "module:docs_src/additional_responses/tutorial002_py310.py",
      "confidence": 0.85,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 2,
        "fan_out_z_score": -0.334,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/additional_responses/tutorial002_py310.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "module:docs_src/additional_responses/tutorial003_py310.py",
      "confidence": 0.85,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 3,
        "fan_out_z_score": -0.21,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/additional_responses/tutorial003_py310.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "module:docs_src/additional_responses/tutorial004_py310.py",
      "confidence": 0.85,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 2,
        "fan_out_z_score": -0.334,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/additional_responses/tutorial004_py310.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "module:docs_src/additional_status_codes/tutorial001_an_py310.py",
      "confidence": 0.85,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 1,
        "fan_out_z_score": -0.459,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/additional_status_codes/tutorial001_an_py310.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "module:docs_src/additional_status_codes/tutorial001_py310.py",
      "confidence": 0.85,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 1,
        "fan_out_z_score": -0.459,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/additional_status_codes/tutorial001_py310.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "module:docs_src/advanced_middleware/tutorial001_py310.py",
      "confidence": 0.85,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 1,
        "fan_out_z_score": -0.459,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/advanced_middleware/tutorial001_py310.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "module:docs_src/advanced_middleware/tutorial002_py310.py",
      "confidence": 0.85,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 1,
        "fan_out_z_score": -0.459,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/advanced_middleware/tutorial002_py310.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "module:docs_src/advanced_middleware/tutorial003_py310.py",
      "confidence": 0.85,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 1,
        "fan_out_z_score": -0.459,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/advanced_middleware/tutorial003_py310.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "module:docs_src/app_testing/app_a_py310/main.py",
      "confidence": 0.85,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 1,
        "fan_out_z_score": -0.459,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/app_testing/app_a_py310/main.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "module:docs_src/app_testing/app_b_an_py310/main.py",
      "confidence": 0.85,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 3,
        "fan_out_z_score": -0.21,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/app_testing/app_b_an_py310/main.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "module:docs_src/async_tests/__init__.py",
      "confidence": 0.85,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.583,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": []
    },
    {
      "node_id": "module:docs_src/async_tests/app_a_py310/__init__.py",
      "confidence": 0.85,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.583,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": []
    },
    {
      "node_id": "module:docs_src/async_tests/app_a_py310/main.py",
      "confidence": 0.85,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 1,
        "fan_out_z_score": -0.459,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/async_tests/app_a_py310/main.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "module:docs_src/async_tests/app_a_py310/test_main.py",
      "confidence": 0.85,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 1,
        "fan_out_z_score": -0.459,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/async_tests/app_a_py310/test_main.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "module:fastapi/concurrency.py",
      "confidence": 0.85,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 1,
        "fan_out_z_score": -0.459,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/concurrency.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "module:fastapi/dependencies/utils.py",
      "confidence": 0.65,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 28,
        "fan_out_z_score": 2.899,
        "cross_file_span_ratio": 0.018,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "module:fastapi/middleware/asyncexitstack.py",
      "confidence": 0.85,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 3,
        "fan_out_z_score": -0.21,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/middleware/asyncexitstack.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "module:tests/test_tutorial/test_async_tests/__init__.py",
      "confidence": 0.85,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.583,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": []
    },
    {
      "node_id": "module:tests/test_tutorial/test_async_tests/test_main_a.py",
      "confidence": 0.85,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 1,
        "fan_out_z_score": -0.459,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "tests/test_tutorial/test_async_tests/test_main_a.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:docs_src/additional_responses/tutorial001_py310.py:Item:6",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": 0.0,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/additional_responses/tutorial001_py310.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:docs_src/additional_responses/tutorial001_py310.py:Message:11",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": 0.0,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/additional_responses/tutorial001_py310.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:docs_src/additional_responses/tutorial001_py310.py:read_item:19",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/additional_responses/tutorial001_py310.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:docs_src/additional_responses/tutorial002_py310.py:Item:6",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": 0.0,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/additional_responses/tutorial002_py310.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:docs_src/additional_responses/tutorial002_py310.py:read_item:24",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/additional_responses/tutorial002_py310.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:docs_src/additional_responses/tutorial003_py310.py:Item:6",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": 0.0,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/additional_responses/tutorial003_py310.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:docs_src/additional_responses/tutorial003_py310.py:Message:11",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": 0.0,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/additional_responses/tutorial003_py310.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:docs_src/additional_responses/tutorial003_py310.py:read_item:33",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/additional_responses/tutorial003_py310.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:docs_src/additional_responses/tutorial004_py310.py:Item:6",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": 0.0,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/additional_responses/tutorial004_py310.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:docs_src/additional_responses/tutorial004_py310.py:read_item:26",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/additional_responses/tutorial004_py310.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:docs_src/additional_status_codes/tutorial001_an_py310.py:upsert_item:12",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/additional_status_codes/tutorial001_an_py310.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:docs_src/additional_status_codes/tutorial001_py310.py:upsert_item:10",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/additional_status_codes/tutorial001_py310.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:docs_src/advanced_middleware/tutorial001_py310.py:main:10",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/advanced_middleware/tutorial001_py310.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:docs_src/advanced_middleware/tutorial002_py310.py:main:12",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/advanced_middleware/tutorial002_py310.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:docs_src/advanced_middleware/tutorial003_py310.py:main:10",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/advanced_middleware/tutorial003_py310.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:docs_src/app_testing/app_a_py310/main.py:read_main:7",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/app_testing/app_a_py310/main.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:docs_src/app_testing/app_b_an_py310/main.py:Item:16",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": 0.0,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/app_testing/app_b_an_py310/main.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:docs_src/app_testing/app_b_an_py310/main.py:create_item:32",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/app_testing/app_b_an_py310/main.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:docs_src/app_testing/app_b_an_py310/main.py:read_main:23",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/app_testing/app_b_an_py310/main.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:docs_src/async_tests/app_a_py310/main.py:root:7",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/async_tests/app_a_py310/main.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:docs_src/async_tests/app_a_py310/test_main.py:test_root:8",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "docs_src/async_tests/app_a_py310/test_main.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/concurrency.py:contextmanager_in_threadpool:18",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/concurrency.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:ParamDetails:384",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": 0.0,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:SolvedDependency:587",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": 0.0,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:_extract_form_body:909",
      "confidence": 0.57,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 3,
        "fan_out_z_score": 5.14,
        "cross_file_span_ratio": 0.018,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:_get_multidict_value:750",
      "confidence": 0.57,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 2,
        "fan_out_z_score": 2.411,
        "cross_file_span_ratio": 0.018,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:_get_signature:211",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:_is_json_field:746",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:_should_embed_body_fields:885",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 1,
        "fan_out_z_score": 1.088,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:_solve_generator:575",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:add_non_field_param_to_dependency:359",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:add_param_to_fields:559",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:analyze_param:390",
      "confidence": 0.57,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 2,
        "fan_out_z_score": 2.411,
        "cross_file_span_ratio": 0.018,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:ensure_multipart_is_installed:94",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:get_body_field:998",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:get_dependant:284",
      "confidence": 0.57,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 5,
        "fan_out_z_score": 6.381,
        "cross_file_span_ratio": 0.018,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:get_flat_dependant:136",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 1,
        "fan_out_z_score": 1.088,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:get_flat_params:202",
      "confidence": 0.57,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 5,
        "fan_out_z_score": 6.381,
        "cross_file_span_ratio": 0.018,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:get_parameterless_sub_dependant:121",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 1,
        "fan_out_z_score": 1.088,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:get_stream_item_type:274",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:get_typed_annotation:243",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:get_typed_return_annotation:252",
      "confidence": 0.57,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 2,
        "fan_out_z_score": 2.411,
        "cross_file_span_ratio": 0.018,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:get_typed_signature:226",
      "confidence": 0.57,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 2,
        "fan_out_z_score": 2.411,
        "cross_file_span_ratio": 0.018,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:is_union_of_base_models:866",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:request_body_to_args:948",
      "confidence": 0.57,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 5,
        "fan_out_z_score": 8.73,
        "cross_file_span_ratio": 0.018,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
      "confidence": 0.57,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 8,
        "fan_out_z_score": 10.351,
        "cross_file_span_ratio": 0.018,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
      "confidence": 0.57,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 9,
        "fan_out_z_score": 15.908,
        "cross_file_span_ratio": 0.018,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/dependencies/utils.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware.__call__:15",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/middleware/asyncexitstack.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware.__init__:9",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.235,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/middleware/asyncexitstack.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware:8",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": 0.0,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "fastapi/middleware/asyncexitstack.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:tests/test_tutorial/test_async_tests/test_main_a.py:test_async_testing:7",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 0,
        "fan_out_z_score": -0.244,
        "cross_file_span_ratio": 0.018,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "tests/test_tutorial/test_async_tests/test_main_a.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    }
  ],
  "per_edge_confidence": [
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:_extract_form_body:909:symbol:fastapi/dependencies/utils.py:_get_multidict_value:750:916",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:_extract_form_body:909:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:936",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:_extract_form_body:909:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:937",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:_get_multidict_value:750:symbol:fastapi/dependencies/utils.py:_is_json_field:746:755",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:_get_multidict_value:750:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:753",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:_should_embed_body_fields:885:symbol:fastapi/dependencies/utils.py:is_union_of_base_models:866:903",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:analyze_param:390:symbol:fastapi/dependencies/utils.py:ParamDetails:384:556",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:analyze_param:390:symbol:fastapi/dependencies/utils.py:ensure_multipart_is_installed:94:532",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_dependant:284:symbol:fastapi/dependencies/utils.py:add_non_field_param_to_dependency:359:342",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_dependant:284:symbol:fastapi/dependencies/utils.py:add_param_to_fields:559:355",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_dependant:284:symbol:fastapi/dependencies/utils.py:analyze_param:390:309",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_dependant:284:symbol:fastapi/dependencies/utils.py:get_dependant:284:331",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_dependant:284:symbol:fastapi/dependencies/utils.py:get_typed_signature:226:305",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_flat_dependant:136:symbol:fastapi/dependencies/utils.py:get_flat_dependant:136:173",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_flat_params:202:symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190:204",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_flat_params:202:symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190:205",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_flat_params:202:symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190:206",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_flat_params:202:symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190:207",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_flat_params:202:symbol:fastapi/dependencies/utils.py:get_flat_dependant:136:203",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_parameterless_sub_dependant:121:symbol:fastapi/dependencies/utils.py:get_dependant:284:128",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_typed_return_annotation:252:symbol:fastapi/dependencies/utils.py:_get_signature:211:253",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_typed_return_annotation:252:symbol:fastapi/dependencies/utils.py:get_typed_annotation:243:261",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_typed_signature:226:symbol:fastapi/dependencies/utils.py:_get_signature:211:227",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_typed_signature:226:symbol:fastapi/dependencies/utils.py:get_typed_annotation:243:235",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_body_to_args:948:symbol:fastapi/dependencies/utils.py:_extract_form_body:909:970",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_body_to_args:948:symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735:974",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_body_to_args:948:symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735:988",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_body_to_args:948:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:979",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_body_to_args:948:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:983",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:_get_multidict_value:750:822",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:_get_multidict_value:750:850",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735:844",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735:856",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:819",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:824",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:825",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:855",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:SolvedDependency:587:726",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:_solve_generator:575:669",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:get_dependant:284:638",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:request_body_to_args:948:703",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:682",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:685",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:688",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:691",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:646",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:docs_src/additional_responses/tutorial001_py310.py:symbol:docs_src/additional_responses/tutorial001_py310.py:Item:6",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:docs_src/additional_responses/tutorial001_py310.py:symbol:docs_src/additional_responses/tutorial001_py310.py:Message:11",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:docs_src/additional_responses/tutorial001_py310.py:symbol:docs_src/additional_responses/tutorial001_py310.py:read_item:19",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:docs_src/additional_responses/tutorial002_py310.py:symbol:docs_src/additional_responses/tutorial002_py310.py:Item:6",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:docs_src/additional_responses/tutorial002_py310.py:symbol:docs_src/additional_responses/tutorial002_py310.py:read_item:24",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:docs_src/additional_responses/tutorial003_py310.py:symbol:docs_src/additional_responses/tutorial003_py310.py:Item:6",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:docs_src/additional_responses/tutorial003_py310.py:symbol:docs_src/additional_responses/tutorial003_py310.py:Message:11",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:docs_src/additional_responses/tutorial003_py310.py:symbol:docs_src/additional_responses/tutorial003_py310.py:read_item:33",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:docs_src/additional_responses/tutorial004_py310.py:symbol:docs_src/additional_responses/tutorial004_py310.py:Item:6",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:docs_src/additional_responses/tutorial004_py310.py:symbol:docs_src/additional_responses/tutorial004_py310.py:read_item:26",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:docs_src/additional_status_codes/tutorial001_an_py310.py:symbol:docs_src/additional_status_codes/tutorial001_an_py310.py:upsert_item:12",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:docs_src/additional_status_codes/tutorial001_py310.py:symbol:docs_src/additional_status_codes/tutorial001_py310.py:upsert_item:10",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:docs_src/advanced_middleware/tutorial001_py310.py:symbol:docs_src/advanced_middleware/tutorial001_py310.py:main:10",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:docs_src/advanced_middleware/tutorial002_py310.py:symbol:docs_src/advanced_middleware/tutorial002_py310.py:main:12",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:docs_src/advanced_middleware/tutorial003_py310.py:symbol:docs_src/advanced_middleware/tutorial003_py310.py:main:10",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:docs_src/app_testing/app_a_py310/main.py:symbol:docs_src/app_testing/app_a_py310/main.py:read_main:7",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:docs_src/app_testing/app_b_an_py310/main.py:symbol:docs_src/app_testing/app_b_an_py310/main.py:Item:16",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:docs_src/app_testing/app_b_an_py310/main.py:symbol:docs_src/app_testing/app_b_an_py310/main.py:create_item:32",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:docs_src/app_testing/app_b_an_py310/main.py:symbol:docs_src/app_testing/app_b_an_py310/main.py:read_main:23",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:docs_src/async_tests/app_a_py310/main.py:symbol:docs_src/async_tests/app_a_py310/main.py:root:7",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:docs_src/async_tests/app_a_py310/test_main.py:symbol:docs_src/async_tests/app_a_py310/test_main.py:test_root:8",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/concurrency.py:symbol:fastapi/concurrency.py:contextmanager_in_threadpool:18",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:ParamDetails:384",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:SolvedDependency:587",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_extract_form_body:909",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_get_multidict_value:750",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_get_signature:211",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_is_json_field:746",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_should_embed_body_fields:885",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_solve_generator:575",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:add_non_field_param_to_dependency:359",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:add_param_to_fields:559",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:analyze_param:390",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:ensure_multipart_is_installed:94",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_body_field:998",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_dependant:284",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_flat_dependant:136",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_flat_params:202",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_parameterless_sub_dependant:121",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_stream_item_type:274",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_typed_annotation:243",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_typed_return_annotation:252",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_typed_signature:226",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:is_union_of_base_models:866",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:request_body_to_args:948",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/middleware/asyncexitstack.py:symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware.__call__:15",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/middleware/asyncexitstack.py:symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware.__init__:9",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:fastapi/middleware/asyncexitstack.py:symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware:8",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "contains:module:tests/test_tutorial/test_async_tests/test_main_a.py:symbol:tests/test_tutorial/test_async_tests/test_main_a.py:test_async_testing:7",
      "confidence": 1.0,
      "suggested_actions": []
    }
  ]
}

## Projection Stats
{
  "seed_count": 66,
  "initial_seed_count": 20,
  "projected_node_count": 74,
  "projected_edge_count": 100,
  "graph_node_count": 6359,
  "graph_edge_count": 6012
}

## Projected Nodes
[
  {
    "node_id": "module:docs_src/additional_responses/tutorial001_py310.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "docs_src/additional_responses/tutorial001_py310.py",
      "byte_start": 0,
      "byte_end": 506,
      "ast_path": "module",
      "content_hash": "612da60c415c496d69abe57869aa440fbcda1d6c532d1e37432f7f136f28d0dd"
    },
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
    "confidence": 1.0
  },
  {
    "node_id": "module:docs_src/additional_responses/tutorial002_py310.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "docs_src/additional_responses/tutorial002_py310.py",
      "byte_start": 0,
      "byte_end": 596,
      "ast_path": "module",
      "content_hash": "9affbc269aa5ac588f3024310c39e02a79778160fe75901ad8c1468fb28bdae5"
    },
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
    "confidence": 1.0
  },
  {
    "node_id": "module:docs_src/additional_responses/tutorial003_py310.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "docs_src/additional_responses/tutorial003_py310.py",
      "byte_start": 0,
      "byte_end": 837,
      "ast_path": "module",
      "content_hash": "6fc74f39c96da18ac4d179ba3fc4dd0a035288e31022d91cfa49dbaf440c662c"
    },
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
    "confidence": 1.0
  },
  {
    "node_id": "module:docs_src/additional_responses/tutorial004_py310.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "docs_src/additional_responses/tutorial004_py310.py",
      "byte_start": 0,
      "byte_end": 669,
      "ast_path": "module",
      "content_hash": "cab81f82d4e279d5c8185830647e9c38c1d858730262e8a4666ecbb08fa48f9d"
    },
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
    "confidence": 1.0
  },
  {
    "node_id": "module:docs_src/additional_status_codes/tutorial001_an_py310.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "docs_src/additional_status_codes/tutorial001_an_py310.py",
      "byte_start": 0,
      "byte_end": 686,
      "ast_path": "module",
      "content_hash": "243ef632dea60a9492750e5f1c57411d6e050417c211f5fe8e9b11c6f4870783"
    },
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
    "confidence": 1.0
  },
  {
    "node_id": "module:docs_src/additional_status_codes/tutorial001_py310.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "docs_src/additional_status_codes/tutorial001_py310.py",
      "byte_start": 0,
      "byte_end": 646,
      "ast_path": "module",
      "content_hash": "51d2b5effdc47584b7c45d16cb7c163b6df8cbbea8ad4c5b3fd3f09bdc06e5c6"
    },
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
    "confidence": 1.0
  },
  {
    "node_id": "module:docs_src/advanced_middleware/tutorial001_py310.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "docs_src/advanced_middleware/tutorial001_py310.py",
      "byte_start": 0,
      "byte_end": 231,
      "ast_path": "module",
      "content_hash": "33e9e46c522fda0144e0223d58f2e1f18ee54da574ddf2d4aae68e2430b60f96"
    },
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
    "confidence": 1.0
  },
  {
    "node_id": "module:docs_src/advanced_middleware/tutorial002_py310.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "docs_src/advanced_middleware/tutorial002_py310.py",
      "byte_start": 0,
      "byte_end": 279,
      "ast_path": "module",
      "content_hash": "503289271cfef94141627667ffdee2584a289cb88a022dc26ee94bea5c2bd02c"
    },
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
    "confidence": 1.0
  },
  {
    "node_id": "module:docs_src/advanced_middleware/tutorial003_py310.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "docs_src/advanced_middleware/tutorial003_py310.py",
      "byte_start": 0,
      "byte_end": 230,
      "ast_path": "module",
      "content_hash": "d21fa2479c14650e0f63c4489504671b1d63e8376bd13e9db65e5437b8b7b45b"
    },
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
    "confidence": 1.0
  },
  {
    "node_id": "module:docs_src/app_testing/app_a_py310/main.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "docs_src/app_testing/app_a_py310/main.py",
      "byte_start": 0,
      "byte_end": 118,
      "ast_path": "module",
      "content_hash": "799a66ca241638380ba6e08101ed0da161b8635b4938b46fe30beb3694cb8ab0"
    },
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
    "confidence": 1.0
  },
  {
    "node_id": "module:docs_src/app_testing/app_b_an_py310/main.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "docs_src/app_testing/app_b_an_py310/main.py",
      "byte_start": 0,
      "byte_end": 1163,
      "ast_path": "module",
      "content_hash": "bb5514b0dbea75e676a9447acf428d6a130727fa6a751c865cc302aaf476a053"
    },
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
    "confidence": 1.0
  },
  {
    "node_id": "module:docs_src/async_tests/__init__.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "docs_src/async_tests/__init__.py",
      "byte_start": 0,
      "byte_end": 0,
      "ast_path": "module",
      "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
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
    "confidence": 1.0
  },
  {
    "node_id": "module:docs_src/async_tests/app_a_py310/__init__.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "docs_src/async_tests/app_a_py310/__init__.py",
      "byte_start": 0,
      "byte_end": 0,
      "ast_path": "module",
      "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
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
    "confidence": 1.0
  },
  {
    "node_id": "module:docs_src/async_tests/app_a_py310/main.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "docs_src/async_tests/app_a_py310/main.py",
      "byte_start": 0,
      "byte_end": 112,
      "ast_path": "module",
      "content_hash": "f28e4cbedad7a9e0a8f72e6fb71a677c40a01977cf79f238b9e0f6402810e0ce"
    },
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
    "confidence": 1.0
  },
  {
    "node_id": "module:docs_src/async_tests/app_a_py310/test_main.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "docs_src/async_tests/app_a_py310/test_main.py",
      "byte_start": 0,
      "byte_end": 360,
      "ast_path": "module",
      "content_hash": "a129755184f168aaa0f56307f4e43541ca6e5d392a185a3442983400ab3daffb"
    },
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
    "confidence": 1.0
  },
  {
    "node_id": "module:fastapi/concurrency.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "fastapi/concurrency.py",
      "byte_start": 0,
      "byte_end": 1489,
      "ast_path": "module",
      "content_hash": "c4718310e40003a72f1440d7e3aa2adebdadd59778b15beb79a4607481388ee3"
    },
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
    "confidence": 1.0
  },
  {
    "node_id": "module:fastapi/dependencies/utils.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 0,
      "byte_end": 39276,
      "ast_path": "module",
      "content_hash": "434b0b2ade506c141727f9e91082093cbcc68e6b1417a417d7f9875dc5e56e9f"
    },
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
    "confidence": 1.0
  },
  {
    "node_id": "module:fastapi/middleware/asyncexitstack.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "fastapi/middleware/asyncexitstack.py",
      "byte_start": 0,
      "byte_end": 637,
      "ast_path": "module",
      "content_hash": "44a1a54291b383718ba2ca9586bc41cbf34267da894bbcd078d1ede58df1fb4d"
    },
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
    "confidence": 1.0
  },
  {
    "node_id": "module:tests/test_tutorial/test_async_tests/__init__.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "tests/test_tutorial/test_async_tests/__init__.py",
      "byte_start": 0,
      "byte_end": 0,
      "ast_path": "module",
      "content_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
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
    "confidence": 1.0
  },
  {
    "node_id": "module:tests/test_tutorial/test_async_tests/test_main_a.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "tests/test_tutorial/test_async_tests/test_main_a.py",
      "byte_start": 0,
      "byte_end": 155,
      "ast_path": "module",
      "content_hash": "8f119b37bfb8122479262f4db932d504d801f24cf3569976d88b35bdd1afd044"
    },
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
    "confidence": 1.0
  },
  {
    "node_id": "symbol:docs_src/additional_responses/tutorial001_py310.py:Item:6",
    "node_type": "class",
    "source_anchor": {
      "file_path": "docs_src/additional_responses/tutorial001_py310.py",
      "byte_start": 104,
      "byte_end": 153,
      "ast_path": "class:Item",
      "content_hash": "833b82b5b70fbed783f61f2ee13958ac3c2efd1665b0149baa7cb3895a3c1862"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:docs_src/additional_responses/tutorial001_py310.py:Message:11",
    "node_type": "class",
    "source_anchor": {
      "file_path": "docs_src/additional_responses/tutorial001_py310.py",
      "byte_start": 156,
      "byte_end": 198,
      "ast_path": "class:Message",
      "content_hash": "6a4d8965350ccb3363b3fd7628d44665794c7b755a89d54d9da4a86fb16f9912"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:docs_src/additional_responses/tutorial001_py310.py:read_item:19",
    "node_type": "async_function",
    "source_anchor": {
      "file_path": "docs_src/additional_responses/tutorial001_py310.py",
      "byte_start": 306,
      "byte_end": 505,
      "ast_path": "async_function:read_item",
      "content_hash": "98e752ca1bf5e928f959d52f862684c1ecaab6210eb589915f5e08b87cb46005"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:docs_src/additional_responses/tutorial002_py310.py:Item:6",
    "node_type": "class",
    "source_anchor": {
      "file_path": "docs_src/additional_responses/tutorial002_py310.py",
      "byte_start": 104,
      "byte_end": 153,
      "ast_path": "class:Item",
      "content_hash": "833b82b5b70fbed783f61f2ee13958ac3c2efd1665b0149baa7cb3895a3c1862"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:docs_src/additional_responses/tutorial002_py310.py:read_item:24",
    "node_type": "async_function",
    "source_anchor": {
      "file_path": "docs_src/additional_responses/tutorial002_py310.py",
      "byte_start": 389,
      "byte_end": 595,
      "ast_path": "async_function:read_item",
      "content_hash": "0267b55467af313a8e10d36950fb51103ded1c50f628d1223ab8a856501a7b29"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:docs_src/additional_responses/tutorial003_py310.py:Item:6",
    "node_type": "class",
    "source_anchor": {
      "file_path": "docs_src/additional_responses/tutorial003_py310.py",
      "byte_start": 104,
      "byte_end": 153,
      "ast_path": "class:Item",
      "content_hash": "833b82b5b70fbed783f61f2ee13958ac3c2efd1665b0149baa7cb3895a3c1862"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:docs_src/additional_responses/tutorial003_py310.py:Message:11",
    "node_type": "class",
    "source_anchor": {
      "file_path": "docs_src/additional_responses/tutorial003_py310.py",
      "byte_start": 156,
      "byte_end": 198,
      "ast_path": "class:Message",
      "content_hash": "6a4d8965350ccb3363b3fd7628d44665794c7b755a89d54d9da4a86fb16f9912"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:docs_src/additional_responses/tutorial003_py310.py:read_item:33",
    "node_type": "async_function",
    "source_anchor": {
      "file_path": "docs_src/additional_responses/tutorial003_py310.py",
      "byte_start": 623,
      "byte_end": 836,
      "ast_path": "async_function:read_item",
      "content_hash": "30e667a5ff2ad6105adc4dd3c35cc5c8554f23ee5b1da277015bace9135dfff8"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:docs_src/additional_responses/tutorial004_py310.py:Item:6",
    "node_type": "class",
    "source_anchor": {
      "file_path": "docs_src/additional_responses/tutorial004_py310.py",
      "byte_start": 104,
      "byte_end": 153,
      "ast_path": "class:Item",
      "content_hash": "833b82b5b70fbed783f61f2ee13958ac3c2efd1665b0149baa7cb3895a3c1862"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:docs_src/additional_responses/tutorial004_py310.py:read_item:26",
    "node_type": "async_function",
    "source_anchor": {
      "file_path": "docs_src/additional_responses/tutorial004_py310.py",
      "byte_start": 462,
      "byte_end": 668,
      "ast_path": "async_function:read_item",
      "content_hash": "0267b55467af313a8e10d36950fb51103ded1c50f628d1223ab8a856501a7b29"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:docs_src/additional_status_codes/tutorial001_an_py310.py:upsert_item:12",
    "node_type": "async_function",
    "source_anchor": {
      "file_path": "docs_src/additional_status_codes/tutorial001_an_py310.py",
      "byte_start": 252,
      "byte_end": 685,
      "ast_path": "async_function:upsert_item",
      "content_hash": "8f856d966c3f5246620fa05adfed32d409dd00fb740cf20f724861e9f6b38b3f"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:docs_src/additional_status_codes/tutorial001_py310.py:upsert_item:10",
    "node_type": "async_function",
    "source_anchor": {
      "file_path": "docs_src/additional_status_codes/tutorial001_py310.py",
      "byte_start": 222,
      "byte_end": 645,
      "ast_path": "async_function:upsert_item",
      "content_hash": "f4bef2e04ebcd36012be1c81d05372c7d993ec12188234d278554b96e5258edd"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:docs_src/advanced_middleware/tutorial001_py310.py:main:10",
    "node_type": "async_function",
    "source_anchor": {
      "file_path": "docs_src/advanced_middleware/tutorial001_py310.py",
      "byte_start": 175,
      "byte_end": 230,
      "ast_path": "async_function:main",
      "content_hash": "224af768dffdeeae2e2a33e9a3c4a5854557ec25bdf2989761f9d0300db65eea"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:docs_src/advanced_middleware/tutorial002_py310.py:main:12",
    "node_type": "async_function",
    "source_anchor": {
      "file_path": "docs_src/advanced_middleware/tutorial002_py310.py",
      "byte_start": 223,
      "byte_end": 278,
      "ast_path": "async_function:main",
      "content_hash": "224af768dffdeeae2e2a33e9a3c4a5854557ec25bdf2989761f9d0300db65eea"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:docs_src/advanced_middleware/tutorial003_py310.py:main:10",
    "node_type": "async_function",
    "source_anchor": {
      "file_path": "docs_src/advanced_middleware/tutorial003_py310.py",
      "byte_start": 184,
      "byte_end": 229,
      "ast_path": "async_function:main",
      "content_hash": "8cdf7c8b34d14c7d95ae84d95fa37b1a6dfe36622b0f75505fd86153e5befa4a"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:docs_src/app_testing/app_a_py310/main.py:read_main:7",
    "node_type": "async_function",
    "source_anchor": {
      "file_path": "docs_src/app_testing/app_a_py310/main.py",
      "byte_start": 61,
      "byte_end": 117,
      "ast_path": "async_function:read_main",
      "content_hash": "45c2ff112295f1634d82f2735207962f37de491a6dd3babaf40f37ab823fed4c"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:docs_src/app_testing/app_b_an_py310/main.py:Item:16",
    "node_type": "class",
    "source_anchor": {
      "file_path": "docs_src/app_testing/app_b_an_py310/main.py",
      "byte_start": 337,
      "byte_end": 421,
      "ast_path": "class:Item",
      "content_hash": "3eabe5818645b72d1fd60bfa09e477cbebd39aaed7dd6004a4e7fb5fe5f2d60c"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:docs_src/app_testing/app_b_an_py310/main.py:create_item:32",
    "node_type": "async_function",
    "source_anchor": {
      "file_path": "docs_src/app_testing/app_b_an_py310/main.py",
      "byte_start": 811,
      "byte_end": 1162,
      "ast_path": "async_function:create_item",
      "content_hash": "cea88fe067ad30ea61d56b1a8b0565a653e394508eb60e53e040f70f6172180a"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:docs_src/app_testing/app_b_an_py310/main.py:read_main:23",
    "node_type": "async_function",
    "source_anchor": {
      "file_path": "docs_src/app_testing/app_b_an_py310/main.py",
      "byte_start": 474,
      "byte_end": 787,
      "ast_path": "async_function:read_main",
      "content_hash": "16964a0ac0777ee9d754553d1c26e95ecb1dfe16f9ada8bc4d22882f8f514c7a"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:docs_src/async_tests/app_a_py310/main.py:root:7",
    "node_type": "async_function",
    "source_anchor": {
      "file_path": "docs_src/async_tests/app_a_py310/main.py",
      "byte_start": 61,
      "byte_end": 111,
      "ast_path": "async_function:root",
      "content_hash": "f10a1df2d619042f0ab7e411c59116a0bd99d03078a5ffaf179215b78af3003d"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:docs_src/async_tests/app_a_py310/test_main.py:test_root:8",
    "node_type": "async_function",
    "source_anchor": {
      "file_path": "docs_src/async_tests/app_a_py310/test_main.py",
      "byte_start": 103,
      "byte_end": 359,
      "ast_path": "async_function:test_root",
      "content_hash": "8a1c07015e2cfa2ed6247302ad562800438d219626a9d84eb59c17db6ec72459"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/concurrency.py:contextmanager_in_threadpool:18",
    "node_type": "async_function",
    "source_anchor": {
      "file_path": "fastapi/concurrency.py",
      "byte_start": 557,
      "byte_end": 1488,
      "ast_path": "async_function:contextmanager_in_threadpool",
      "content_hash": "4232d61205d9c955dad93fef003e540aaa709e990d3777695edf4c783ddcfae8"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:ParamDetails:384",
    "node_type": "class",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 13424,
      "byte_end": 13532,
      "ast_path": "class:ParamDetails",
      "content_hash": "c1444cd8def129d95a4cc46461041c98ae0eb9c9e8359d39da63cb43c23fc764"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:SolvedDependency:587",
    "node_type": "class",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 21541,
      "byte_end": 21742,
      "ast_path": "class:SolvedDependency",
      "content_hash": "17f1cabd23e445c103c117bf837625d2e74793a50297bc9fa16f1ea5d10dc277"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:_extract_form_body:909",
    "node_type": "async_function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 33895,
      "byte_end": 35319,
      "ast_path": "async_function:_extract_form_body",
      "content_hash": "d0c31d7d344152d117b5da94ec81bffb19db87eff67f63efb4c3b18a3a9816de"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190",
    "node_type": "function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 6350,
      "byte_end": 6744,
      "ast_path": "function:_get_flat_fields_from_params",
      "content_hash": "e7fa3732f0b0d987475fc3087ade88ed383741c991c69a78a7fd84830f5d1722"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:_get_multidict_value:750",
    "node_type": "function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 28053,
      "byte_end": 28946,
      "ast_path": "function:_get_multidict_value",
      "content_hash": "8d7c2e1c739661fe24eeaf288c5faef1e754f315d9a6eceefdc981d913678d1b"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:_get_signature:211",
    "node_type": "function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 7262,
      "byte_end": 7788,
      "ast_path": "function:_get_signature",
      "content_hash": "663852e9e7b0e861ddb9a4a5e1b3fc5bbee21e3231735197510eadbdc12cc9a5"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:_is_json_field:746",
    "node_type": "function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 27931,
      "byte_end": 28050,
      "ast_path": "function:_is_json_field",
      "content_hash": "6d206838173f40be73be0e7a1be1c0d7a499c6a81be048de5b1a35f79243ec6b"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:_should_embed_body_fields:885",
    "node_type": "function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 32834,
      "byte_end": 33892,
      "ast_path": "function:_should_embed_body_fields",
      "content_hash": "a18c3b6bc5eea3f937968abe2e8ffbe777728df2e1f536650f515c21973059de"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:_solve_generator:575",
    "node_type": "async_function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 21111,
      "byte_end": 21527,
      "ast_path": "async_function:_solve_generator",
      "content_hash": "69b9190419314723e2a125346a6e5337aeb2fba3bfbc451d7681ba9f79fa994a"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735",
    "node_type": "function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 27544,
      "byte_end": 27928,
      "ast_path": "function:_validate_value_with_model_field",
      "content_hash": "45ff8393dec2ebe41da7639903479f9374218d1af90e68017d415c02f4600073"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:add_non_field_param_to_dependency:359",
    "node_type": "function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 12461,
      "byte_end": 13410,
      "ast_path": "function:add_non_field_param_to_dependency",
      "content_hash": "450c1b66c8f8cb9dc935d6bf323506515f2a443c5532ecf67ec8d08258ceb4f6"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:add_param_to_fields:559",
    "node_type": "function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 20443,
      "byte_end": 21108,
      "ast_path": "function:add_param_to_fields",
      "content_hash": "5f87238254caa48893aeabbf1d4a475149db99debb72fd88c6000171840fb8cc"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:analyze_param:390",
    "node_type": "function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 13535,
      "byte_end": 20440,
      "ast_path": "function:analyze_param",
      "content_hash": "b361897cfff040ddd4e277e7709b4971b9736f91a8b3418813ad121e3ec124cf"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:ensure_multipart_is_installed:94",
    "node_type": "function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 2581,
      "byte_end": 3657,
      "ast_path": "function:ensure_multipart_is_installed",
      "content_hash": "381f46b8715314c1d6f1dd4648664bd3c6ba8ef907dd2191773e6f719527183c"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:get_body_field:998",
    "node_type": "function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 37214,
      "byte_end": 39142,
      "ast_path": "function:get_body_field",
      "content_hash": "d7f1fce5ec6d6b10b5d03e86e2ae672c27e11cc95caa6ed756c87f0ad7ffc4fc"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:get_dependant:284",
    "node_type": "function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 9437,
      "byte_end": 12458,
      "ast_path": "function:get_dependant",
      "content_hash": "e00aac4b07348f1448adca1ce1aabddcd9c5dd7f53353a63c1237af7eb8948d1"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:get_flat_dependant:136",
    "node_type": "function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 4175,
      "byte_end": 6347,
      "ast_path": "function:get_flat_dependant",
      "content_hash": "a4a8ee34e9b604a3c8fa5d7f1e730407887a0e63e154dd4f2073d799313e372b"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:get_flat_params:202",
    "node_type": "function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 6747,
      "byte_end": 7259,
      "ast_path": "function:get_flat_params",
      "content_hash": "b633d01dda801c969ab2a5825e5129125d375d68f4d72a0baa903c3bf62de18e"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:get_parameterless_sub_dependant:121",
    "node_type": "function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 3660,
      "byte_end": 4172,
      "ast_path": "function:get_parameterless_sub_dependant",
      "content_hash": "77bc961c0548a30f9eece029295419f3d089d841498f7849ad638a06525343e4"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:get_stream_item_type:274",
    "node_type": "function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 9155,
      "byte_end": 9434,
      "ast_path": "function:get_stream_item_type",
      "content_hash": "21d183b79cc4a3b13465d8afba47bb5445a83013ea3d0245d50191d5a3332d9e"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:get_typed_annotation:243",
    "node_type": "function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 8354,
      "byte_end": 8665,
      "ast_path": "function:get_typed_annotation",
      "content_hash": "33955de14066a1aea1b9a33296282eb6dd1ca35ae79c05ad0c37080562ac1a64"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:get_typed_return_annotation:252",
    "node_type": "function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 8668,
      "byte_end": 9027,
      "ast_path": "function:get_typed_return_annotation",
      "content_hash": "9a13036e2b1f0a4a292e037093d0cd72e2567127e727290e7d681c49a8b6384f"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:get_typed_signature:226",
    "node_type": "function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 7791,
      "byte_end": 8351,
      "ast_path": "function:get_typed_signature",
      "content_hash": "9a4baef3c22a8bd8b472712104f6eae5531313c75cd28bd355f047a75cd47d0d"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052",
    "node_type": "function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 39145,
      "byte_end": 39275,
      "ast_path": "function:get_validation_alias",
      "content_hash": "126b3a08e19782bfb21429df9b502fb925efa8913a4072800ed27601776d81a1"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:is_union_of_base_models:866",
    "node_type": "function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 32282,
      "byte_end": 32831,
      "ast_path": "function:is_union_of_base_models",
      "content_hash": "44c69a85969d4e1ae3ce8de1b9eff4fc328789a76d2b01151b2345f89d8d01d9"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:request_body_to_args:948",
    "node_type": "async_function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 35322,
      "byte_end": 37211,
      "ast_path": "async_function:request_body_to_args",
      "content_hash": "8b24311a51620699020243d703be0d01d7928dc3b1ce83567aca538d06bdf0d8"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "node_type": "function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 28949,
      "byte_end": 32279,
      "ast_path": "function:request_params_to_args",
      "content_hash": "056f212ccf6614ff42b30323bf31e44bf3b90eddff266d203897ff7f45c8fdef"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
    "node_type": "async_function",
    "source_anchor": {
      "file_path": "fastapi/dependencies/utils.py",
      "byte_start": 21745,
      "byte_end": 27541,
      "ast_path": "async_function:solve_dependencies",
      "content_hash": "7d6d2f9927bbee7ceafbfdb69a6b5b5cdd62d998edf08f1c3489be1a8782796d"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware.__call__:15",
    "node_type": "async_function",
    "source_anchor": {
      "file_path": "fastapi/middleware/asyncexitstack.py",
      "byte_start": 419,
      "byte_end": 636,
      "ast_path": "async_function:AsyncExitStackMiddleware.__call__",
      "content_hash": "4ac933ba1dc0080f5f33f5d1bcef363805f15bd57f699de49df2de01818ec5bc"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware.__init__:9",
    "node_type": "function",
    "source_anchor": {
      "file_path": "fastapi/middleware/asyncexitstack.py",
      "byte_start": 245,
      "byte_end": 413,
      "ast_path": "function:AsyncExitStackMiddleware.__init__",
      "content_hash": "9f69aad72d1a866ab554b3c908032f08435f6c5cf503482ae675bf006c6ca856"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware:8",
    "node_type": "class",
    "source_anchor": {
      "file_path": "fastapi/middleware/asyncexitstack.py",
      "byte_start": 209,
      "byte_end": 636,
      "ast_path": "class:AsyncExitStackMiddleware",
      "content_hash": "aafdef3eed0fc0fb00898f6f94a860f465678efa51fd16f4e2f6acb60c28fac7"
    },
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
    "confidence": 0.92
  },
  {
    "node_id": "symbol:tests/test_tutorial/test_async_tests/test_main_a.py:test_async_testing:7",
    "node_type": "async_function",
    "source_anchor": {
      "file_path": "tests/test_tutorial/test_async_tests/test_main_a.py",
      "byte_start": 101,
      "byte_end": 154,
      "ast_path": "async_function:test_async_testing",
      "content_hash": "9ed6bd4a20ca618505243d4dcca4a32c75b59412b57a8bad6f6a69670da40aea"
    },
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
    "confidence": 0.92
  }
]

## Projected Edges
[
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:_extract_form_body:909:symbol:fastapi/dependencies/utils.py:_get_multidict_value:750:916",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:_extract_form_body:909",
    "to_node": "symbol:fastapi/dependencies/utils.py:_get_multidict_value:750",
    "evidence": {
      "line": 916,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:_extract_form_body:909:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:936",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:_extract_form_body:909",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052",
    "evidence": {
      "line": 936,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:_extract_form_body:909:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:937",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:_extract_form_body:909",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052",
    "evidence": {
      "line": 937,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:_get_multidict_value:750:symbol:fastapi/dependencies/utils.py:_is_json_field:746:755",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:_get_multidict_value:750",
    "to_node": "symbol:fastapi/dependencies/utils.py:_is_json_field:746",
    "evidence": {
      "line": 755,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:_get_multidict_value:750:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:753",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:_get_multidict_value:750",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052",
    "evidence": {
      "line": 753,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:_should_embed_body_fields:885:symbol:fastapi/dependencies/utils.py:is_union_of_base_models:866:903",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:_should_embed_body_fields:885",
    "to_node": "symbol:fastapi/dependencies/utils.py:is_union_of_base_models:866",
    "evidence": {
      "line": 903,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:analyze_param:390:symbol:fastapi/dependencies/utils.py:ParamDetails:384:556",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:analyze_param:390",
    "to_node": "symbol:fastapi/dependencies/utils.py:ParamDetails:384",
    "evidence": {
      "line": 556,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:analyze_param:390:symbol:fastapi/dependencies/utils.py:ensure_multipart_is_installed:94:532",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:analyze_param:390",
    "to_node": "symbol:fastapi/dependencies/utils.py:ensure_multipart_is_installed:94",
    "evidence": {
      "line": 532,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_dependant:284:symbol:fastapi/dependencies/utils.py:add_non_field_param_to_dependency:359:342",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:get_dependant:284",
    "to_node": "symbol:fastapi/dependencies/utils.py:add_non_field_param_to_dependency:359",
    "evidence": {
      "line": 342,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_dependant:284:symbol:fastapi/dependencies/utils.py:add_param_to_fields:559:355",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:get_dependant:284",
    "to_node": "symbol:fastapi/dependencies/utils.py:add_param_to_fields:559",
    "evidence": {
      "line": 355,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_dependant:284:symbol:fastapi/dependencies/utils.py:analyze_param:390:309",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:get_dependant:284",
    "to_node": "symbol:fastapi/dependencies/utils.py:analyze_param:390",
    "evidence": {
      "line": 309,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_dependant:284:symbol:fastapi/dependencies/utils.py:get_dependant:284:331",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:get_dependant:284",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_dependant:284",
    "evidence": {
      "line": 331,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_dependant:284:symbol:fastapi/dependencies/utils.py:get_typed_signature:226:305",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:get_dependant:284",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_typed_signature:226",
    "evidence": {
      "line": 305,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_flat_dependant:136:symbol:fastapi/dependencies/utils.py:get_flat_dependant:136:173",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:get_flat_dependant:136",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_flat_dependant:136",
    "evidence": {
      "line": 173,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_flat_params:202:symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190:204",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:get_flat_params:202",
    "to_node": "symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190",
    "evidence": {
      "line": 204,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_flat_params:202:symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190:205",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:get_flat_params:202",
    "to_node": "symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190",
    "evidence": {
      "line": 205,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_flat_params:202:symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190:206",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:get_flat_params:202",
    "to_node": "symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190",
    "evidence": {
      "line": 206,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_flat_params:202:symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190:207",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:get_flat_params:202",
    "to_node": "symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190",
    "evidence": {
      "line": 207,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_flat_params:202:symbol:fastapi/dependencies/utils.py:get_flat_dependant:136:203",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:get_flat_params:202",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_flat_dependant:136",
    "evidence": {
      "line": 203,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_parameterless_sub_dependant:121:symbol:fastapi/dependencies/utils.py:get_dependant:284:128",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:get_parameterless_sub_dependant:121",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_dependant:284",
    "evidence": {
      "line": 128,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_typed_return_annotation:252:symbol:fastapi/dependencies/utils.py:_get_signature:211:253",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:get_typed_return_annotation:252",
    "to_node": "symbol:fastapi/dependencies/utils.py:_get_signature:211",
    "evidence": {
      "line": 253,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_typed_return_annotation:252:symbol:fastapi/dependencies/utils.py:get_typed_annotation:243:261",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:get_typed_return_annotation:252",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_typed_annotation:243",
    "evidence": {
      "line": 261,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_typed_signature:226:symbol:fastapi/dependencies/utils.py:_get_signature:211:227",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:get_typed_signature:226",
    "to_node": "symbol:fastapi/dependencies/utils.py:_get_signature:211",
    "evidence": {
      "line": 227,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:get_typed_signature:226:symbol:fastapi/dependencies/utils.py:get_typed_annotation:243:235",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:get_typed_signature:226",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_typed_annotation:243",
    "evidence": {
      "line": 235,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_body_to_args:948:symbol:fastapi/dependencies/utils.py:_extract_form_body:909:970",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:request_body_to_args:948",
    "to_node": "symbol:fastapi/dependencies/utils.py:_extract_form_body:909",
    "evidence": {
      "line": 970,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_body_to_args:948:symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735:974",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:request_body_to_args:948",
    "to_node": "symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735",
    "evidence": {
      "line": 974,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_body_to_args:948:symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735:988",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:request_body_to_args:948",
    "to_node": "symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735",
    "evidence": {
      "line": 988,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_body_to_args:948:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:979",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:request_body_to_args:948",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052",
    "evidence": {
      "line": 979,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_body_to_args:948:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:983",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:request_body_to_args:948",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052",
    "evidence": {
      "line": 983,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:_get_multidict_value:750:822",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "to_node": "symbol:fastapi/dependencies/utils.py:_get_multidict_value:750",
    "evidence": {
      "line": 822,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:_get_multidict_value:750:850",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "to_node": "symbol:fastapi/dependencies/utils.py:_get_multidict_value:750",
    "evidence": {
      "line": 850,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735:844",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "to_node": "symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735",
    "evidence": {
      "line": 844,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735:856",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "to_node": "symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735",
    "evidence": {
      "line": 856,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:819",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052",
    "evidence": {
      "line": 819,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:824",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052",
    "evidence": {
      "line": 824,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:825",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052",
    "evidence": {
      "line": 825,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052:855",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052",
    "evidence": {
      "line": 855,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:SolvedDependency:587:726",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
    "to_node": "symbol:fastapi/dependencies/utils.py:SolvedDependency:587",
    "evidence": {
      "line": 726,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:_solve_generator:575:669",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
    "to_node": "symbol:fastapi/dependencies/utils.py:_solve_generator:575",
    "evidence": {
      "line": 669,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:get_dependant:284:638",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_dependant:284",
    "evidence": {
      "line": 638,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:request_body_to_args:948:703",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
    "to_node": "symbol:fastapi/dependencies/utils.py:request_body_to_args:948",
    "evidence": {
      "line": 703,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:682",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
    "to_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "evidence": {
      "line": 682,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:685",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
    "to_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "evidence": {
      "line": 685,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:688",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
    "to_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "evidence": {
      "line": 688,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:request_params_to_args:781:691",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
    "to_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "evidence": {
      "line": 691,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:symbol:fastapi/dependencies/utils.py:solve_dependencies:595:646",
    "edge_type": "calls",
    "from_node": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
    "to_node": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
    "evidence": {
      "line": 646,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "contains:module:docs_src/additional_responses/tutorial001_py310.py:symbol:docs_src/additional_responses/tutorial001_py310.py:Item:6",
    "edge_type": "contains",
    "from_node": "module:docs_src/additional_responses/tutorial001_py310.py",
    "to_node": "symbol:docs_src/additional_responses/tutorial001_py310.py:Item:6",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:docs_src/additional_responses/tutorial001_py310.py:symbol:docs_src/additional_responses/tutorial001_py310.py:Message:11",
    "edge_type": "contains",
    "from_node": "module:docs_src/additional_responses/tutorial001_py310.py",
    "to_node": "symbol:docs_src/additional_responses/tutorial001_py310.py:Message:11",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:docs_src/additional_responses/tutorial001_py310.py:symbol:docs_src/additional_responses/tutorial001_py310.py:read_item:19",
    "edge_type": "contains",
    "from_node": "module:docs_src/additional_responses/tutorial001_py310.py",
    "to_node": "symbol:docs_src/additional_responses/tutorial001_py310.py:read_item:19",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:docs_src/additional_responses/tutorial002_py310.py:symbol:docs_src/additional_responses/tutorial002_py310.py:Item:6",
    "edge_type": "contains",
    "from_node": "module:docs_src/additional_responses/tutorial002_py310.py",
    "to_node": "symbol:docs_src/additional_responses/tutorial002_py310.py:Item:6",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:docs_src/additional_responses/tutorial002_py310.py:symbol:docs_src/additional_responses/tutorial002_py310.py:read_item:24",
    "edge_type": "contains",
    "from_node": "module:docs_src/additional_responses/tutorial002_py310.py",
    "to_node": "symbol:docs_src/additional_responses/tutorial002_py310.py:read_item:24",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:docs_src/additional_responses/tutorial003_py310.py:symbol:docs_src/additional_responses/tutorial003_py310.py:Item:6",
    "edge_type": "contains",
    "from_node": "module:docs_src/additional_responses/tutorial003_py310.py",
    "to_node": "symbol:docs_src/additional_responses/tutorial003_py310.py:Item:6",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:docs_src/additional_responses/tutorial003_py310.py:symbol:docs_src/additional_responses/tutorial003_py310.py:Message:11",
    "edge_type": "contains",
    "from_node": "module:docs_src/additional_responses/tutorial003_py310.py",
    "to_node": "symbol:docs_src/additional_responses/tutorial003_py310.py:Message:11",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:docs_src/additional_responses/tutorial003_py310.py:symbol:docs_src/additional_responses/tutorial003_py310.py:read_item:33",
    "edge_type": "contains",
    "from_node": "module:docs_src/additional_responses/tutorial003_py310.py",
    "to_node": "symbol:docs_src/additional_responses/tutorial003_py310.py:read_item:33",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:docs_src/additional_responses/tutorial004_py310.py:symbol:docs_src/additional_responses/tutorial004_py310.py:Item:6",
    "edge_type": "contains",
    "from_node": "module:docs_src/additional_responses/tutorial004_py310.py",
    "to_node": "symbol:docs_src/additional_responses/tutorial004_py310.py:Item:6",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:docs_src/additional_responses/tutorial004_py310.py:symbol:docs_src/additional_responses/tutorial004_py310.py:read_item:26",
    "edge_type": "contains",
    "from_node": "module:docs_src/additional_responses/tutorial004_py310.py",
    "to_node": "symbol:docs_src/additional_responses/tutorial004_py310.py:read_item:26",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:docs_src/additional_status_codes/tutorial001_an_py310.py:symbol:docs_src/additional_status_codes/tutorial001_an_py310.py:upsert_item:12",
    "edge_type": "contains",
    "from_node": "module:docs_src/additional_status_codes/tutorial001_an_py310.py",
    "to_node": "symbol:docs_src/additional_status_codes/tutorial001_an_py310.py:upsert_item:12",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:docs_src/additional_status_codes/tutorial001_py310.py:symbol:docs_src/additional_status_codes/tutorial001_py310.py:upsert_item:10",
    "edge_type": "contains",
    "from_node": "module:docs_src/additional_status_codes/tutorial001_py310.py",
    "to_node": "symbol:docs_src/additional_status_codes/tutorial001_py310.py:upsert_item:10",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:docs_src/advanced_middleware/tutorial001_py310.py:symbol:docs_src/advanced_middleware/tutorial001_py310.py:main:10",
    "edge_type": "contains",
    "from_node": "module:docs_src/advanced_middleware/tutorial001_py310.py",
    "to_node": "symbol:docs_src/advanced_middleware/tutorial001_py310.py:main:10",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:docs_src/advanced_middleware/tutorial002_py310.py:symbol:docs_src/advanced_middleware/tutorial002_py310.py:main:12",
    "edge_type": "contains",
    "from_node": "module:docs_src/advanced_middleware/tutorial002_py310.py",
    "to_node": "symbol:docs_src/advanced_middleware/tutorial002_py310.py:main:12",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:docs_src/advanced_middleware/tutorial003_py310.py:symbol:docs_src/advanced_middleware/tutorial003_py310.py:main:10",
    "edge_type": "contains",
    "from_node": "module:docs_src/advanced_middleware/tutorial003_py310.py",
    "to_node": "symbol:docs_src/advanced_middleware/tutorial003_py310.py:main:10",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:docs_src/app_testing/app_a_py310/main.py:symbol:docs_src/app_testing/app_a_py310/main.py:read_main:7",
    "edge_type": "contains",
    "from_node": "module:docs_src/app_testing/app_a_py310/main.py",
    "to_node": "symbol:docs_src/app_testing/app_a_py310/main.py:read_main:7",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:docs_src/app_testing/app_b_an_py310/main.py:symbol:docs_src/app_testing/app_b_an_py310/main.py:Item:16",
    "edge_type": "contains",
    "from_node": "module:docs_src/app_testing/app_b_an_py310/main.py",
    "to_node": "symbol:docs_src/app_testing/app_b_an_py310/main.py:Item:16",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:docs_src/app_testing/app_b_an_py310/main.py:symbol:docs_src/app_testing/app_b_an_py310/main.py:create_item:32",
    "edge_type": "contains",
    "from_node": "module:docs_src/app_testing/app_b_an_py310/main.py",
    "to_node": "symbol:docs_src/app_testing/app_b_an_py310/main.py:create_item:32",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:docs_src/app_testing/app_b_an_py310/main.py:symbol:docs_src/app_testing/app_b_an_py310/main.py:read_main:23",
    "edge_type": "contains",
    "from_node": "module:docs_src/app_testing/app_b_an_py310/main.py",
    "to_node": "symbol:docs_src/app_testing/app_b_an_py310/main.py:read_main:23",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:docs_src/async_tests/app_a_py310/main.py:symbol:docs_src/async_tests/app_a_py310/main.py:root:7",
    "edge_type": "contains",
    "from_node": "module:docs_src/async_tests/app_a_py310/main.py",
    "to_node": "symbol:docs_src/async_tests/app_a_py310/main.py:root:7",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:docs_src/async_tests/app_a_py310/test_main.py:symbol:docs_src/async_tests/app_a_py310/test_main.py:test_root:8",
    "edge_type": "contains",
    "from_node": "module:docs_src/async_tests/app_a_py310/test_main.py",
    "to_node": "symbol:docs_src/async_tests/app_a_py310/test_main.py:test_root:8",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/concurrency.py:symbol:fastapi/concurrency.py:contextmanager_in_threadpool:18",
    "edge_type": "contains",
    "from_node": "module:fastapi/concurrency.py",
    "to_node": "symbol:fastapi/concurrency.py:contextmanager_in_threadpool:18",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:ParamDetails:384",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:ParamDetails:384",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:SolvedDependency:587",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:SolvedDependency:587",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_extract_form_body:909",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:_extract_form_body:909",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:_get_flat_fields_from_params:190",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_get_multidict_value:750",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:_get_multidict_value:750",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_get_signature:211",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:_get_signature:211",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_is_json_field:746",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:_is_json_field:746",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_should_embed_body_fields:885",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:_should_embed_body_fields:885",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_solve_generator:575",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:_solve_generator:575",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:_validate_value_with_model_field:735",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:add_non_field_param_to_dependency:359",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:add_non_field_param_to_dependency:359",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:add_param_to_fields:559",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:add_param_to_fields:559",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:analyze_param:390",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:analyze_param:390",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:ensure_multipart_is_installed:94",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:ensure_multipart_is_installed:94",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_body_field:998",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_body_field:998",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_dependant:284",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_dependant:284",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_flat_dependant:136",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_flat_dependant:136",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_flat_params:202",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_flat_params:202",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_parameterless_sub_dependant:121",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_parameterless_sub_dependant:121",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_stream_item_type:274",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_stream_item_type:274",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_typed_annotation:243",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_typed_annotation:243",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_typed_return_annotation:252",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_typed_return_annotation:252",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_typed_signature:226",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_typed_signature:226",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:get_validation_alias:1052",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:get_validation_alias:1052",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:is_union_of_base_models:866",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:is_union_of_base_models:866",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:request_body_to_args:948",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:request_body_to_args:948",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:request_params_to_args:781",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/dependencies/utils.py:symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
    "edge_type": "contains",
    "from_node": "module:fastapi/dependencies/utils.py",
    "to_node": "symbol:fastapi/dependencies/utils.py:solve_dependencies:595",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/middleware/asyncexitstack.py:symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware.__call__:15",
    "edge_type": "contains",
    "from_node": "module:fastapi/middleware/asyncexitstack.py",
    "to_node": "symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware.__call__:15",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/middleware/asyncexitstack.py:symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware.__init__:9",
    "edge_type": "contains",
    "from_node": "module:fastapi/middleware/asyncexitstack.py",
    "to_node": "symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware.__init__:9",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:fastapi/middleware/asyncexitstack.py:symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware:8",
    "edge_type": "contains",
    "from_node": "module:fastapi/middleware/asyncexitstack.py",
    "to_node": "symbol:fastapi/middleware/asyncexitstack.py:AsyncExitStackMiddleware:8",
    "evidence": {
      "rel": "ast_containment"
    }
  },
  {
    "edge_id": "contains:module:tests/test_tutorial/test_async_tests/test_main_a.py:symbol:tests/test_tutorial/test_async_tests/test_main_a.py:test_async_testing:7",
    "edge_type": "contains",
    "from_node": "module:tests/test_tutorial/test_async_tests/test_main_a.py",
    "to_node": "symbol:tests/test_tutorial/test_async_tests/test_main_a.py:test_async_testing:7",
    "evidence": {
      "rel": "ast_containment"
    }
  }
]

## Automated MCP Drill-Down Results
{
  "task_id": "fastapi-tf4-001",
  "repo_dir": "fastapi",
  "operation_family": "OF4",
  "confidence_overall": 0.851351,
  "lookup_hint": "clue_only",
  "projected_nodes": 74,
  "actions_executed": 20,
  "budget": {
    "budget_exhausted": true,
    "operation_family": "OF4",
    "calls_made": 20,
    "budget": 20,
    "remaining": 0,
    "unresolved_nodes": []
  },
  "tokens": {
    "clue": 38010,
    "drill_down": 7547,
    "total": 45557,
    "raw_estimate": 944223
  },
  "etrr": 0.9518,
  "h7_pass": true,
  "tool_results": [
    {
      "tool": "code_slice",
      "args": {
        "file_path": "docs_src/additional_responses/tutorial001_py310.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "module:docs_src/additional_responses/tutorial001_py310.py",
      "confidence_trigger": 0.85,
      "output_size_tokens": 359,
      "result": {
        "status": "ok",
        "file_path": "docs_src/additional_responses/tutorial001_py310.py",
        "start_line": 1,
        "end_line": 22,
        "total_lines_in_file": 22,
        "lines": [
          {
            "line_number": 1,
            "content": "from fastapi import FastAPI"
          },
          {
            "line_number": 2,
            "content": "from fastapi.responses import JSONResponse"
          },
          {
            "line_number": 3,
            "content": "from pydantic import BaseModel"
          },
          {
            "line_number": 4,
            "content": ""
          },
          {
            "line_number": 5,
            "content": ""
          },
          {
            "line_number": 6,
            "content": "class Item(BaseModel):"
          },
          {
            "line_number": 7,
            "content": "    id: str"
          },
          {
            "line_number": 8,
            "content": "    value: str"
          },
          {
            "line_number": 9,
            "content": ""
          },
          {
            "line_number": 10,
            "content": ""
          },
          {
            "line_number": 11,
            "content": "class Message(BaseModel):"
          },
          {
            "line_number": 12,
            "content": "    message: str"
          },
          {
            "line_number": 13,
            "content": ""
          },
          {
            "line_number": 14,
            "content": ""
          },
          {
            "line_number": 15,
            "content": "app = FastAPI()"
          },
          {
            "line_number": 16,
            "content": ""
          },
          {
            "line_number": 17,
            "content": ""
          },
          {
            "line_number": 18,
            "content": "@app.get(\"/items/{item_id}\", response_model=Item, responses={404: {\"model\": Message}})"
          },
          {
            "line_number": 19,
            "content": "async def read_item(item_id: str):"
          },
          {
            "line_number": 20,
            "content": "    if item_id == \"foo\":"
          },
          {
            "line_number": 21,
            "content": "        return {\"id\": \"foo\", \"value\": \"there goes my hero\"}"
          },
          {
            "line_number": 22,
            "content": "    return JSONResponse(status_code=404, content={\"message\": \"Item not found\"})"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "docs_src/additional_responses/tutorial002_py310.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "module:docs_src/additional_responses/tutorial002_py310.py",
      "confidence_trigger": 0.85,
      "output_size_tokens": 435,
      "result": {
        "status": "ok",
        "file_path": "docs_src/additional_responses/tutorial002_py310.py",
        "start_line": 1,
        "end_line": 28,
        "total_lines_in_file": 28,
        "lines": [
          {
            "line_number": 1,
            "content": "from fastapi import FastAPI"
          },
          {
            "line_number": 2,
            "content": "from fastapi.responses import FileResponse"
          },
          {
            "line_number": 3,
            "content": "from pydantic import BaseModel"
          },
          {
            "line_number": 4,
            "content": ""
          },
          {
            "line_number": 5,
            "content": ""
          },
          {
            "line_number": 6,
            "content": "class Item(BaseModel):"
          },
          {
            "line_number": 7,
            "content": "    id: str"
          },
          {
            "line_number": 8,
            "content": "    value: str"
          },
          {
            "line_number": 9,
            "content": ""
          },
          {
            "line_number": 10,
            "content": ""
          },
          {
            "line_number": 11,
            "content": "app = FastAPI()"
          },
          {
            "line_number": 12,
            "content": ""
          },
          {
            "line_number": 13,
            "content": ""
          },
          {
            "line_number": 14,
            "content": "@app.get("
          },
          {
            "line_number": 15,
            "content": "    \"/items/{item_id}\","
          },
          {
            "line_number": 16,
            "content": "    response_model=Item,"
          },
          {
            "line_number": 17,
            "content": "    responses={"
          },
          {
            "line_number": 18,
            "content": "        200: {"
          },
          {
            "line_number": 19,
            "content": "            \"content\": {\"image/png\": {}},"
          },
          {
            "line_number": 20,
            "content": "            \"description\": \"Return the JSON item or an image.\","
          },
          {
            "line_number": 21,
            "content": "        }"
          },
          {
            "line_number": 22,
            "content": "    },"
          },
          {
            "line_number": 23,
            "content": ")"
          },
          {
            "line_number": 24,
            "content": "async def read_item(item_id: str, img: bool | None = None):"
          },
          {
            "line_number": 25,
            "content": "    if img:"
          },
          {
            "line_number": 26,
            "content": "        return FileResponse(\"image.png\", media_type=\"image/png\")"
          },
          {
            "line_number": 27,
            "content": "    else:"
          },
          {
            "line_number": 28,
            "content": "        return {\"id\": \"foo\", \"value\": \"there goes my hero\"}"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "docs_src/additional_responses/tutorial003_py310.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "module:docs_src/additional_responses/tutorial003_py310.py",
      "confidence_trigger": 0.85,
      "output_size_tokens": 579,
      "result": {
        "status": "ok",
        "file_path": "docs_src/additional_responses/tutorial003_py310.py",
        "start_line": 1,
        "end_line": 37,
        "total_lines_in_file": 37,
        "lines": [
          {
            "line_number": 1,
            "content": "from fastapi import FastAPI"
          },
          {
            "line_number": 2,
            "content": "from fastapi.responses import JSONResponse"
          },
          {
            "line_number": 3,
            "content": "from pydantic import BaseModel"
          },
          {
            "line_number": 4,
            "content": ""
          },
          {
            "line_number": 5,
            "content": ""
          },
          {
            "line_number": 6,
            "content": "class Item(BaseModel):"
          },
          {
            "line_number": 7,
            "content": "    id: str"
          },
          {
            "line_number": 8,
            "content": "    value: str"
          },
          {
            "line_number": 9,
            "content": ""
          },
          {
            "line_number": 10,
            "content": ""
          },
          {
            "line_number": 11,
            "content": "class Message(BaseModel):"
          },
          {
            "line_number": 12,
            "content": "    message: str"
          },
          {
            "line_number": 13,
            "content": ""
          },
          {
            "line_number": 14,
            "content": ""
          },
          {
            "line_number": 15,
            "content": "app = FastAPI()"
          },
          {
            "line_number": 16,
            "content": ""
          },
          {
            "line_number": 17,
            "content": ""
          },
          {
            "line_number": 18,
            "content": "@app.get("
          },
          {
            "line_number": 19,
            "content": "    \"/items/{item_id}\","
          },
          {
            "line_number": 20,
            "content": "    response_model=Item,"
          },
          {
            "line_number": 21,
            "content": "    responses={"
          },
          {
            "line_number": 22,
            "content": "        404: {\"model\": Message, \"description\": \"The item was not found\"},"
          },
          {
            "line_number": 23,
            "content": "        200: {"
          },
          {
            "line_number": 24,
            "content": "            \"description\": \"Item requested by ID\","
          },
          {
            "line_number": 25,
            "content": "            \"content\": {"
          },
          {
            "line_number": 26,
            "content": "                \"application/json\": {"
          },
          {
            "line_number": 27,
            "content": "                    \"example\": {\"id\": \"bar\", \"value\": \"The bar tenders\"}"
          },
          {
            "line_number": 28,
            "content": "                }"
          },
          {
            "line_number": 29,
            "content": "            },"
          },
          {
            "line_number": 30,
            "content": "        },"
          },
          {
            "line_number": 31,
            "content": "    },"
          },
          {
            "line_number": 32,
            "content": ")"
          },
          {
            "line_number": 33,
            "content": "async def read_item(item_id: str):"
          },
          {
            "line_number": 34,
            "content": "    if item_id == \"foo\":"
          },
          {
            "line_number": 35,
            "content": "        return {\"id\": \"foo\", \"value\": \"there goes my hero\"}"
          },
          {
            "line_number": 36,
            "content": "    else:"
          },
          {
            "line_number": 37,
            "content": "        return JSONResponse(status_code=404, content={\"message\": \"Item not found\"})"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "docs_src/additional_responses/tutorial004_py310.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "module:docs_src/additional_responses/tutorial004_py310.py",
      "confidence_trigger": 0.85,
      "output_size_tokens": 473,
      "result": {
        "status": "ok",
        "file_path": "docs_src/additional_responses/tutorial004_py310.py",
        "start_line": 1,
        "end_line": 30,
        "total_lines_in_file": 30,
        "lines": [
          {
            "line_number": 1,
            "content": "from fastapi import FastAPI"
          },
          {
            "line_number": 2,
            "content": "from fastapi.responses import FileResponse"
          },
          {
            "line_number": 3,
            "content": "from pydantic import BaseModel"
          },
          {
            "line_number": 4,
            "content": ""
          },
          {
            "line_number": 5,
            "content": ""
          },
          {
            "line_number": 6,
            "content": "class Item(BaseModel):"
          },
          {
            "line_number": 7,
            "content": "    id: str"
          },
          {
            "line_number": 8,
            "content": "    value: str"
          },
          {
            "line_number": 9,
            "content": ""
          },
          {
            "line_number": 10,
            "content": ""
          },
          {
            "line_number": 11,
            "content": "responses = {"
          },
          {
            "line_number": 12,
            "content": "    404: {\"description\": \"Item not found\"},"
          },
          {
            "line_number": 13,
            "content": "    302: {\"description\": \"The item was moved\"},"
          },
          {
            "line_number": 14,
            "content": "    403: {\"description\": \"Not enough privileges\"},"
          },
          {
            "line_number": 15,
            "content": "}"
          },
          {
            "line_number": 16,
            "content": ""
          },
          {
            "line_number": 17,
            "content": ""
          },
          {
            "line_number": 18,
            "content": "app = FastAPI()"
          },
          {
            "line_number": 19,
            "content": ""
          },
          {
            "line_number": 20,
            "content": ""
          },
          {
            "line_number": 21,
            "content": "@app.get("
          },
          {
            "line_number": 22,
            "content": "    \"/items/{item_id}\","
          },
          {
            "line_number": 23,
            "content": "    response_model=Item,"
          },
          {
            "line_number": 24,
            "content": "    responses={**responses, 200: {\"content\": {\"image/png\": {}}}},"
          },
          {
            "line_number": 25,
            "content": ")"
          },
          {
            "line_number": 26,
            "content": "async def read_item(item_id: str, img: bool | None = None):"
          },
          {
            "line_number": 27,
            "content": "    if img:"
          },
          {
            "line_number": 28,
            "content": "        return FileResponse(\"image.png\", media_type=\"image/png\")"
          },
          {
            "line_number": 29,
            "content": "    else:"
          },
          {
            "line_number": 30,
            "content": "        return {\"id\": \"foo\", \"value\": \"there goes my hero\"}"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "docs_src/additional_status_codes/tutorial001_an_py310.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "module:docs_src/additional_status_codes/tutorial001_an_py310.py",
      "confidence_trigger": 0.85,
      "output_size_tokens": 434,
      "result": {
        "status": "ok",
        "file_path": "docs_src/additional_status_codes/tutorial001_an_py310.py",
        "start_line": 1,
        "end_line": 25,
        "total_lines_in_file": 25,
        "lines": [
          {
            "line_number": 1,
            "content": "from typing import Annotated"
          },
          {
            "line_number": 2,
            "content": ""
          },
          {
            "line_number": 3,
            "content": "from fastapi import Body, FastAPI, status"
          },
          {
            "line_number": 4,
            "content": "from fastapi.responses import JSONResponse"
          },
          {
            "line_number": 5,
            "content": ""
          },
          {
            "line_number": 6,
            "content": "app = FastAPI()"
          },
          {
            "line_number": 7,
            "content": ""
          },
          {
            "line_number": 8,
            "content": "items = {\"foo\": {\"name\": \"Fighters\", \"size\": 6}, \"bar\": {\"name\": \"Tenders\", \"size\": 3}}"
          },
          {
            "line_number": 9,
            "content": ""
          },
          {
            "line_number": 10,
            "content": ""
          },
          {
            "line_number": 11,
            "content": "@app.put(\"/items/{item_id}\")"
          },
          {
            "line_number": 12,
            "content": "async def upsert_item("
          },
          {
            "line_number": 13,
            "content": "    item_id: str,"
          },
          {
            "line_number": 14,
            "content": "    name: Annotated[str | None, Body()] = None,"
          },
          {
            "line_number": 15,
            "content": "    size: Annotated[int | None, Body()] = None,"
          },
          {
            "line_number": 16,
            "content": "):"
          },
          {
            "line_number": 17,
            "content": "    if item_id in items:"
          },
          {
            "line_number": 18,
            "content": "        item = items[item_id]"
          },
          {
            "line_number": 19,
            "content": "        item[\"name\"] = name"
          },
          {
            "line_number": 20,
            "content": "        item[\"size\"] = size"
          },
          {
            "line_number": 21,
            "content": "        return item"
          },
          {
            "line_number": 22,
            "content": "    else:"
          },
          {
            "line_number": 23,
            "content": "        item = {\"name\": name, \"size\": size}"
          },
          {
            "line_number": 24,
            "content": "        items[item_id] = item"
          },
          {
            "line_number": 25,
            "content": "        return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "docs_src/additional_status_codes/tutorial001_py310.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "module:docs_src/additional_status_codes/tutorial001_py310.py",
      "confidence_trigger": 0.85,
      "output_size_tokens": 406,
      "result": {
        "status": "ok",
        "file_path": "docs_src/additional_status_codes/tutorial001_py310.py",
        "start_line": 1,
        "end_line": 23,
        "total_lines_in_file": 23,
        "lines": [
          {
            "line_number": 1,
            "content": "from fastapi import Body, FastAPI, status"
          },
          {
            "line_number": 2,
            "content": "from fastapi.responses import JSONResponse"
          },
          {
            "line_number": 3,
            "content": ""
          },
          {
            "line_number": 4,
            "content": "app = FastAPI()"
          },
          {
            "line_number": 5,
            "content": ""
          },
          {
            "line_number": 6,
            "content": "items = {\"foo\": {\"name\": \"Fighters\", \"size\": 6}, \"bar\": {\"name\": \"Tenders\", \"size\": 3}}"
          },
          {
            "line_number": 7,
            "content": ""
          },
          {
            "line_number": 8,
            "content": ""
          },
          {
            "line_number": 9,
            "content": "@app.put(\"/items/{item_id}\")"
          },
          {
            "line_number": 10,
            "content": "async def upsert_item("
          },
          {
            "line_number": 11,
            "content": "    item_id: str,"
          },
          {
            "line_number": 12,
            "content": "    name: str | None = Body(default=None),"
          },
          {
            "line_number": 13,
            "content": "    size: int | None = Body(default=None),"
          },
          {
            "line_number": 14,
            "content": "):"
          },
          {
            "line_number": 15,
            "content": "    if item_id in items:"
          },
          {
            "line_number": 16,
            "content": "        item = items[item_id]"
          },
          {
            "line_number": 17,
            "content": "        item[\"name\"] = name"
          },
          {
            "line_number": 18,
            "content": "        item[\"size\"] = size"
          },
          {
            "line_number": 19,
            "content": "        return item"
          },
          {
            "line_number": 20,
            "content": "    else:"
          },
          {
            "line_number": 21,
            "content": "        item = {\"name\": name, \"size\": size}"
          },
          {
            "line_number": 22,
            "content": "        items[item_id] = item"
          },
          {
            "line_number": 23,
            "content": "        return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "docs_src/advanced_middleware/tutorial001_py310.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "module:docs_src/advanced_middleware/tutorial001_py310.py",
      "confidence_trigger": 0.85,
      "output_size_tokens": 191,
      "result": {
        "status": "ok",
        "file_path": "docs_src/advanced_middleware/tutorial001_py310.py",
        "start_line": 1,
        "end_line": 11,
        "total_lines_in_file": 11,
        "lines": [
          {
            "line_number": 1,
            "content": "from fastapi import FastAPI"
          },
          {
            "line_number": 2,
            "content": "from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware"
          },
          {
            "line_number": 3,
            "content": ""
          },
          {
            "line_number": 4,
            "content": "app = FastAPI()"
          },
          {
            "line_number": 5,
            "content": ""
          },
          {
            "line_number": 6,
            "content": "app.add_middleware(HTTPSRedirectMiddleware)"
          },
          {
            "line_number": 7,
            "content": ""
          },
          {
            "line_number": 8,
            "content": ""
          },
          {
            "line_number": 9,
            "content": "@app.get(\"/\")"
          },
          {
            "line_number": 10,
            "content": "async def main():"
          },
          {
            "line_number": 11,
            "content": "    return {\"message\": \"Hello World\"}"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "docs_src/advanced_middleware/tutorial002_py310.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "module:docs_src/advanced_middleware/tutorial002_py310.py",
      "confidence_trigger": 0.85,
      "output_size_tokens": 222,
      "result": {
        "status": "ok",
        "file_path": "docs_src/advanced_middleware/tutorial002_py310.py",
        "start_line": 1,
        "end_line": 13,
        "total_lines_in_file": 13,
        "lines": [
          {
            "line_number": 1,
            "content": "from fastapi import FastAPI"
          },
          {
            "line_number": 2,
            "content": "from fastapi.middleware.trustedhost import TrustedHostMiddleware"
          },
          {
            "line_number": 3,
            "content": ""
          },
          {
            "line_number": 4,
            "content": "app = FastAPI()"
          },
          {
            "line_number": 5,
            "content": ""
          },
          {
            "line_number": 6,
            "content": "app.add_middleware("
          },
          {
            "line_number": 7,
            "content": "    TrustedHostMiddleware, allowed_hosts=[\"example.com\", \"*.example.com\"]"
          },
          {
            "line_number": 8,
            "content": ")"
          },
          {
            "line_number": 9,
            "content": ""
          },
          {
            "line_number": 10,
            "content": ""
          },
          {
            "line_number": 11,
            "content": "@app.get(\"/\")"
          },
          {
            "line_number": 12,
            "content": "async def main():"
          },
          {
            "line_number": 13,
            "content": "    return {\"message\": \"Hello World\"}"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "docs_src/advanced_middleware/tutorial003_py310.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "module:docs_src/advanced_middleware/tutorial003_py310.py",
      "confidence_trigger": 0.85,
      "output_size_tokens": 190,
      "result": {
        "status": "ok",
        "file_path": "docs_src/advanced_middleware/tutorial003_py310.py",
        "start_line": 1,
        "end_line": 11,
        "total_lines_in_file": 11,
        "lines": [
          {
            "line_number": 1,
            "content": "from fastapi import FastAPI"
          },
          {
            "line_number": 2,
            "content": "from fastapi.middleware.gzip import GZipMiddleware"
          },
          {
            "line_number": 3,
            "content": ""
          },
          {
            "line_number": 4,
            "content": "app = FastAPI()"
          },
          {
            "line_number": 5,
            "content": ""
          },
          {
            "line_number": 6,
            "content": "app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)"
          },
          {
            "line_number": 7,
            "content": ""
          },
          {
            "line_number": 8,
            "content": ""
          },
          {
            "line_number": 9,
            "content": "@app.get(\"/\")"
          },
          {
            "line_number": 10,
            "content": "async def main():"
          },
          {
            "line_number": 11,
            "content": "    return \"somebigcontent\""
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "docs_src/app_testing/app_a_py310/main.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "module:docs_src/app_testing/app_a_py310/main.py",
      "confidence_trigger": 0.85,
      "output_size_tokens": 134,
      "result": {
        "status": "ok",
        "file_path": "docs_src/app_testing/app_a_py310/main.py",
        "start_line": 1,
        "end_line": 8,
        "total_lines_in_file": 8,
        "lines": [
          {
            "line_number": 1,
            "content": "from fastapi import FastAPI"
          },
          {
            "line_number": 2,
            "content": ""
          },
          {
            "line_number": 3,
            "content": "app = FastAPI()"
          },
          {
            "line_number": 4,
            "content": ""
          },
          {
            "line_number": 5,
            "content": ""
          },
          {
            "line_number": 6,
            "content": "@app.get(\"/\")"
          },
          {
            "line_number": 7,
            "content": "async def read_main():"
          },
          {
            "line_number": 8,
            "content": "    return {\"msg\": \"Hello World\"}"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "docs_src/app_testing/app_b_an_py310/main.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "module:docs_src/app_testing/app_b_an_py310/main.py",
      "confidence_trigger": 0.85,
      "output_size_tokens": 668,
      "result": {
        "status": "ok",
        "file_path": "docs_src/app_testing/app_b_an_py310/main.py",
        "start_line": 1,
        "end_line": 38,
        "total_lines_in_file": 38,
        "lines": [
          {
            "line_number": 1,
            "content": "from typing import Annotated"
          },
          {
            "line_number": 2,
            "content": ""
          },
          {
            "line_number": 3,
            "content": "from fastapi import FastAPI, Header, HTTPException"
          },
          {
            "line_number": 4,
            "content": "from pydantic import BaseModel"
          },
          {
            "line_number": 5,
            "content": ""
          },
          {
            "line_number": 6,
            "content": "fake_secret_token = \"coneofsilence\""
          },
          {
            "line_number": 7,
            "content": ""
          },
          {
            "line_number": 8,
            "content": "fake_db = {"
          },
          {
            "line_number": 9,
            "content": "    \"foo\": {\"id\": \"foo\", \"title\": \"Foo\", \"description\": \"There goes my hero\"},"
          },
          {
            "line_number": 10,
            "content": "    \"bar\": {\"id\": \"bar\", \"title\": \"Bar\", \"description\": \"The bartenders\"},"
          },
          {
            "line_number": 11,
            "content": "}"
          },
          {
            "line_number": 12,
            "content": ""
          },
          {
            "line_number": 13,
            "content": "app = FastAPI()"
          },
          {
            "line_number": 14,
            "content": ""
          },
          {
            "line_number": 15,
            "content": ""
          },
          {
            "line_number": 16,
            "content": "class Item(BaseModel):"
          },
          {
            "line_number": 17,
            "content": "    id: str"
          },
          {
            "line_number": 18,
            "content": "    title: str"
          },
          {
            "line_number": 19,
            "content": "    description: str | None = None"
          },
          {
            "line_number": 20,
            "content": ""
          },
          {
            "line_number": 21,
            "content": ""
          },
          {
            "line_number": 22,
            "content": "@app.get(\"/items/{item_id}\", response_model=Item)"
          },
          {
            "line_number": 23,
            "content": "async def read_main(item_id: str, x_token: Annotated[str, Header()]):"
          },
          {
            "line_number": 24,
            "content": "    if x_token != fake_secret_token:"
          },
          {
            "line_number": 25,
            "content": "        raise HTTPException(status_code=400, detail=\"Invalid X-Token header\")"
          },
          {
            "line_number": 26,
            "content": "    if item_id not in fake_db:"
          },
          {
            "line_number": 27,
            "content": "        raise HTTPException(status_code=404, detail=\"Item not found\")"
          },
          {
            "line_number": 28,
            "content": "    return fake_db[item_id]"
          },
          {
            "line_number": 29,
            "content": ""
          },
          {
            "line_number": 30,
            "content": ""
          },
          {
            "line_number": 31,
            "content": "@app.post(\"/items/\")"
          },
          {
            "line_number": 32,
            "content": "async def create_item(item: Item, x_token: Annotated[str, Header()]) -> Item:"
          },
          {
            "line_number": 33,
            "content": "    if x_token != fake_secret_token:"
          },
          {
            "line_number": 34,
            "content": "        raise HTTPException(status_code=400, detail=\"Invalid X-Token header\")"
          },
          {
            "line_number": 35,
            "content": "    if item.id in fake_db:"
          },
          {
            "line_number": 36,
            "content": "        raise HTTPException(status_code=409, detail=\"Item already exists\")"
          },
          {
            "line_number": 37,
            "content": "    fake_db[item.id] = item.model_dump()"
          },
          {
            "line_number": 38,
            "content": "    return item"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "docs_src/async_tests/app_a_py310/main.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "module:docs_src/async_tests/app_a_py310/main.py",
      "confidence_trigger": 0.85,
      "output_size_tokens": 133,
      "result": {
        "status": "ok",
        "file_path": "docs_src/async_tests/app_a_py310/main.py",
        "start_line": 1,
        "end_line": 8,
        "total_lines_in_file": 8,
        "lines": [
          {
            "line_number": 1,
            "content": "from fastapi import FastAPI"
          },
          {
            "line_number": 2,
            "content": ""
          },
          {
            "line_number": 3,
            "content": "app = FastAPI()"
          },
          {
            "line_number": 4,
            "content": ""
          },
          {
            "line_number": 5,
            "content": ""
          },
          {
            "line_number": 6,
            "content": "@app.get(\"/\")"
          },
          {
            "line_number": 7,
            "content": "async def root():"
          },
          {
            "line_number": 8,
            "content": "    return {\"message\": \"Tomato\"}"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "docs_src/async_tests/app_a_py310/test_main.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "module:docs_src/async_tests/app_a_py310/test_main.py",
      "confidence_trigger": 0.85,
      "output_size_tokens": 249,
      "result": {
        "status": "ok",
        "file_path": "docs_src/async_tests/app_a_py310/test_main.py",
        "start_line": 1,
        "end_line": 14,
        "total_lines_in_file": 14,
        "lines": [
          {
            "line_number": 1,
            "content": "import pytest"
          },
          {
            "line_number": 2,
            "content": "from httpx import ASGITransport, AsyncClient"
          },
          {
            "line_number": 3,
            "content": ""
          },
          {
            "line_number": 4,
            "content": "from .main import app"
          },
          {
            "line_number": 5,
            "content": ""
          },
          {
            "line_number": 6,
            "content": ""
          },
          {
            "line_number": 7,
            "content": "@pytest.mark.anyio"
          },
          {
            "line_number": 8,
            "content": "async def test_root():"
          },
          {
            "line_number": 9,
            "content": "    async with AsyncClient("
          },
          {
            "line_number": 10,
            "content": "        transport=ASGITransport(app=app), base_url=\"http://test\""
          },
          {
            "line_number": 11,
            "content": "    ) as ac:"
          },
          {
            "line_number": 12,
            "content": "        response = await ac.get(\"/\")"
          },
          {
            "line_number": 13,
            "content": "    assert response.status_code == 200"
          },
          {
            "line_number": 14,
            "content": "    assert response.json() == {\"message\": \"Tomato\"}"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "fastapi/concurrency.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "module:fastapi/concurrency.py",
      "confidence_trigger": 0.85,
      "output_size_tokens": 760,
      "result": {
        "status": "ok",
        "file_path": "fastapi/concurrency.py",
        "start_line": 1,
        "end_line": 41,
        "total_lines_in_file": 41,
        "lines": [
          {
            "line_number": 1,
            "content": "from collections.abc import AsyncGenerator"
          },
          {
            "line_number": 2,
            "content": "from contextlib import AbstractContextManager"
          },
          {
            "line_number": 3,
            "content": "from contextlib import asynccontextmanager as asynccontextmanager"
          },
          {
            "line_number": 4,
            "content": "from typing import TypeVar"
          },
          {
            "line_number": 5,
            "content": ""
          },
          {
            "line_number": 6,
            "content": "import anyio.to_thread"
          },
          {
            "line_number": 7,
            "content": "from anyio import CapacityLimiter"
          },
          {
            "line_number": 8,
            "content": "from starlette.concurrency import iterate_in_threadpool as iterate_in_threadpool  # noqa"
          },
          {
            "line_number": 9,
            "content": "from starlette.concurrency import run_in_threadpool as run_in_threadpool  # noqa"
          },
          {
            "line_number": 10,
            "content": "from starlette.concurrency import (  # noqa"
          },
          {
            "line_number": 11,
            "content": "    run_until_first_complete as run_until_first_complete,"
          },
          {
            "line_number": 12,
            "content": ")"
          },
          {
            "line_number": 13,
            "content": ""
          },
          {
            "line_number": 14,
            "content": "_T = TypeVar(\"_T\")"
          },
          {
            "line_number": 15,
            "content": ""
          },
          {
            "line_number": 16,
            "content": ""
          },
          {
            "line_number": 17,
            "content": "@asynccontextmanager"
          },
          {
            "line_number": 18,
            "content": "async def contextmanager_in_threadpool("
          },
          {
            "line_number": 19,
            "content": "    cm: AbstractContextManager[_T],"
          },
          {
            "line_number": 20,
            "content": ") -> AsyncGenerator[_T, None]:"
          },
          {
            "line_number": 21,
            "content": "    # blocking __exit__ from running waiting on a free thread"
          },
          {
            "line_number": 22,
            "content": "    # can create race conditions/deadlocks if the context manager itself"
          },
          {
            "line_number": 23,
            "content": "    # has its own internal pool (e.g. a database connection pool)"
          },
          {
            "line_number": 24,
            "content": "    # to avoid this we let __exit__ run without a capacity limit"
          },
          {
            "line_number": 25,
            "content": "    # since we're creating a new limiter for each call, any non-zero limit"
          },
          {
            "line_number": 26,
            "content": "    # works (1 is arbitrary)"
          },
          {
            "line_number": 27,
            "content": "    exit_limiter = CapacityLimiter(1)"
          },
          {
            "line_number": 28,
            "content": "    try:"
          },
          {
            "line_number": 29,
            "content": "        yield await run_in_threadpool(cm.__enter__)"
          },
          {
            "line_number": 30,
            "content": "    except Exception as e:"
          },
          {
            "line_number": 31,
            "content": "        ok = bool("
          },
          {
            "line_number": 32,
            "content": "            await anyio.to_thread.run_sync("
          },
          {
            "line_number": 33,
            "content": "                cm.__exit__, type(e), e, e.__traceback__, limiter=exit_limiter"
          },
          {
            "line_number": 34,
            "content": "            )"
          },
          {
            "line_number": 35,
            "content": "        )"
          },
          {
            "line_number": 36,
            "content": "        if not ok:"
          },
          {
            "line_number": 37,
            "content": "            raise e"
          },
          {
            "line_number": 38,
            "content": "    else:"
          },
          {
            "line_number": 39,
            "content": "        await anyio.to_thread.run_sync("
          },
          {
            "line_number": 40,
            "content": "            cm.__exit__, None, None, None, limiter=exit_limiter"
          },
          {
            "line_number": 41,
            "content": "        )"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "fastapi/dependencies/utils.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "module:fastapi/dependencies/utils.py",
      "confidence_trigger": 0.65,
      "output_size_tokens": 742,
      "result": {
        "status": "ok",
        "file_path": "fastapi/dependencies/utils.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 1054,
        "lines": [
          {
            "line_number": 1,
            "content": "import dataclasses"
          },
          {
            "line_number": 2,
            "content": "import inspect"
          },
          {
            "line_number": 3,
            "content": "import sys"
          },
          {
            "line_number": 4,
            "content": "from collections.abc import ("
          },
          {
            "line_number": 5,
            "content": "    AsyncGenerator,"
          },
          {
            "line_number": 6,
            "content": "    AsyncIterable,"
          },
          {
            "line_number": 7,
            "content": "    AsyncIterator,"
          },
          {
            "line_number": 8,
            "content": "    Callable,"
          },
          {
            "line_number": 9,
            "content": "    Generator,"
          },
          {
            "line_number": 10,
            "content": "    Iterable,"
          },
          {
            "line_number": 11,
            "content": "    Iterator,"
          },
          {
            "line_number": 12,
            "content": "    Mapping,"
          },
          {
            "line_number": 13,
            "content": "    Sequence,"
          },
          {
            "line_number": 14,
            "content": ")"
          },
          {
            "line_number": 15,
            "content": "from contextlib import AsyncExitStack, contextmanager"
          },
          {
            "line_number": 16,
            "content": "from copy import copy, deepcopy"
          },
          {
            "line_number": 17,
            "content": "from dataclasses import dataclass"
          },
          {
            "line_number": 18,
            "content": "from typing import ("
          },
          {
            "line_number": 19,
            "content": "    Annotated,"
          },
          {
            "line_number": 20,
            "content": "    Any,"
          },
          {
            "line_number": 21,
            "content": "    ForwardRef,"
          },
          {
            "line_number": 22,
            "content": "    Literal,"
          },
          {
            "line_number": 23,
            "content": "    Union,"
          },
          {
            "line_number": 24,
            "content": "    cast,"
          },
          {
            "line_number": 25,
            "content": "    get_args,"
          },
          {
            "line_number": 26,
            "content": "    get_origin,"
          },
          {
            "line_number": 27,
            "content": ")"
          },
          {
            "line_number": 28,
            "content": ""
          },
          {
            "line_number": 29,
            "content": "from fastapi import params"
          },
          {
            "line_number": 30,
            "content": "from fastapi._compat import ("
          },
          {
            "line_number": 31,
            "content": "    ModelField,"
          },
          {
            "line_number": 32,
            "content": "    RequiredParam,"
          },
          {
            "line_number": 33,
            "content": "    Undefined,"
          },
          {
            "line_number": 34,
            "content": "    copy_field_info,"
          },
          {
            "line_number": 35,
            "content": "    create_body_model,"
          },
          {
            "line_number": 36,
            "content": "    evaluate_forwardref,"
          },
          {
            "line_number": 37,
            "content": "    field_annotation_is_scalar,"
          },
          {
            "line_number": 38,
            "content": "    field_annotation_is_scalar_sequence,"
          },
          {
            "line_number": 39,
            "content": "    field_annotation_is_sequence,"
          },
          {
            "line_number": 40,
            "content": "    get_cached_model_fields,"
          },
          {
            "line_number": 41,
            "content": "    get_missing_field_error,"
          },
          {
            "line_number": 42,
            "content": "    is_bytes_or_nonable_bytes_annotation,"
          },
          {
            "line_number": 43,
            "content": "    is_bytes_sequence_annotation,"
          },
          {
            "line_number": 44,
            "content": "    is_scalar_field,"
          },
          {
            "line_number": 45,
            "content": "    is_uploadfile_or_nonable_uploadfile_annotation,"
          },
          {
            "line_number": 46,
            "content": "    is_uploadfile_sequence_annotation,"
          },
          {
            "line_number": 47,
            "content": "    lenient_issubclass,"
          },
          {
            "line_number": 48,
            "content": "    sequence_types,"
          },
          {
            "line_number": 49,
            "content": "    serialize_sequence_value,"
          },
          {
            "line_number": 50,
            "content": "    value_is_sequence,"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "fastapi/middleware/asyncexitstack.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "module:fastapi/middleware/asyncexitstack.py",
      "confidence_trigger": 0.85,
      "output_size_tokens": 350,
      "result": {
        "status": "ok",
        "file_path": "fastapi/middleware/asyncexitstack.py",
        "start_line": 1,
        "end_line": 18,
        "total_lines_in_file": 18,
        "lines": [
          {
            "line_number": 1,
            "content": "from contextlib import AsyncExitStack"
          },
          {
            "line_number": 2,
            "content": ""
          },
          {
            "line_number": 3,
            "content": "from starlette.types import ASGIApp, Receive, Scope, Send"
          },
          {
            "line_number": 4,
            "content": ""
          },
          {
            "line_number": 5,
            "content": ""
          },
          {
            "line_number": 6,
            "content": "# Used mainly to close files after the request is done, dependencies are closed"
          },
          {
            "line_number": 7,
            "content": "# in their own AsyncExitStack"
          },
          {
            "line_number": 8,
            "content": "class AsyncExitStackMiddleware:"
          },
          {
            "line_number": 9,
            "content": "    def __init__("
          },
          {
            "line_number": 10,
            "content": "        self, app: ASGIApp, context_name: str = \"fastapi_middleware_astack\""
          },
          {
            "line_number": 11,
            "content": "    ) -> None:"
          },
          {
            "line_number": 12,
            "content": "        self.app = app"
          },
          {
            "line_number": 13,
            "content": "        self.context_name = context_name"
          },
          {
            "line_number": 14,
            "content": ""
          },
          {
            "line_number": 15,
            "content": "    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:"
          },
          {
            "line_number": 16,
            "content": "        async with AsyncExitStack() as stack:"
          },
          {
            "line_number": 17,
            "content": "            scope[self.context_name] = stack"
          },
          {
            "line_number": 18,
            "content": "            await self.app(scope, receive, send)"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "tests/test_tutorial/test_async_tests/test_main_a.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "module:tests/test_tutorial/test_async_tests/test_main_a.py",
      "confidence_trigger": 0.85,
      "output_size_tokens": 145,
      "result": {
        "status": "ok",
        "file_path": "tests/test_tutorial/test_async_tests/test_main_a.py",
        "start_line": 1,
        "end_line": 8,
        "total_lines_in_file": 8,
        "lines": [
          {
            "line_number": 1,
            "content": "import pytest"
          },
          {
            "line_number": 2,
            "content": ""
          },
          {
            "line_number": 3,
            "content": "from docs_src.async_tests.app_a_py310.test_main import test_root"
          },
          {
            "line_number": 4,
            "content": ""
          },
          {
            "line_number": 5,
            "content": ""
          },
          {
            "line_number": 6,
            "content": "@pytest.mark.anyio"
          },
          {
            "line_number": 7,
            "content": "async def test_async_testing():"
          },
          {
            "line_number": 8,
            "content": "    await test_root()"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "docs_src/additional_responses/tutorial001_py310.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "symbol:docs_src/additional_responses/tutorial001_py310.py:Item:6",
      "confidence_trigger": 0.77,
      "output_size_tokens": 359,
      "result": {
        "status": "ok",
        "file_path": "docs_src/additional_responses/tutorial001_py310.py",
        "start_line": 1,
        "end_line": 22,
        "total_lines_in_file": 22,
        "lines": [
          {
            "line_number": 1,
            "content": "from fastapi import FastAPI"
          },
          {
            "line_number": 2,
            "content": "from fastapi.responses import JSONResponse"
          },
          {
            "line_number": 3,
            "content": "from pydantic import BaseModel"
          },
          {
            "line_number": 4,
            "content": ""
          },
          {
            "line_number": 5,
            "content": ""
          },
          {
            "line_number": 6,
            "content": "class Item(BaseModel):"
          },
          {
            "line_number": 7,
            "content": "    id: str"
          },
          {
            "line_number": 8,
            "content": "    value: str"
          },
          {
            "line_number": 9,
            "content": ""
          },
          {
            "line_number": 10,
            "content": ""
          },
          {
            "line_number": 11,
            "content": "class Message(BaseModel):"
          },
          {
            "line_number": 12,
            "content": "    message: str"
          },
          {
            "line_number": 13,
            "content": ""
          },
          {
            "line_number": 14,
            "content": ""
          },
          {
            "line_number": 15,
            "content": "app = FastAPI()"
          },
          {
            "line_number": 16,
            "content": ""
          },
          {
            "line_number": 17,
            "content": ""
          },
          {
            "line_number": 18,
            "content": "@app.get(\"/items/{item_id}\", response_model=Item, responses={404: {\"model\": Message}})"
          },
          {
            "line_number": 19,
            "content": "async def read_item(item_id: str):"
          },
          {
            "line_number": 20,
            "content": "    if item_id == \"foo\":"
          },
          {
            "line_number": 21,
            "content": "        return {\"id\": \"foo\", \"value\": \"there goes my hero\"}"
          },
          {
            "line_number": 22,
            "content": "    return JSONResponse(status_code=404, content={\"message\": \"Item not found\"})"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "docs_src/additional_responses/tutorial001_py310.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "symbol:docs_src/additional_responses/tutorial001_py310.py:Message:11",
      "confidence_trigger": 0.77,
      "output_size_tokens": 359,
      "result": {
        "status": "ok",
        "file_path": "docs_src/additional_responses/tutorial001_py310.py",
        "start_line": 1,
        "end_line": 22,
        "total_lines_in_file": 22,
        "lines": [
          {
            "line_number": 1,
            "content": "from fastapi import FastAPI"
          },
          {
            "line_number": 2,
            "content": "from fastapi.responses import JSONResponse"
          },
          {
            "line_number": 3,
            "content": "from pydantic import BaseModel"
          },
          {
            "line_number": 4,
            "content": ""
          },
          {
            "line_number": 5,
            "content": ""
          },
          {
            "line_number": 6,
            "content": "class Item(BaseModel):"
          },
          {
            "line_number": 7,
            "content": "    id: str"
          },
          {
            "line_number": 8,
            "content": "    value: str"
          },
          {
            "line_number": 9,
            "content": ""
          },
          {
            "line_number": 10,
            "content": ""
          },
          {
            "line_number": 11,
            "content": "class Message(BaseModel):"
          },
          {
            "line_number": 12,
            "content": "    message: str"
          },
          {
            "line_number": 13,
            "content": ""
          },
          {
            "line_number": 14,
            "content": ""
          },
          {
            "line_number": 15,
            "content": "app = FastAPI()"
          },
          {
            "line_number": 16,
            "content": ""
          },
          {
            "line_number": 17,
            "content": ""
          },
          {
            "line_number": 18,
            "content": "@app.get(\"/items/{item_id}\", response_model=Item, responses={404: {\"model\": Message}})"
          },
          {
            "line_number": 19,
            "content": "async def read_item(item_id: str):"
          },
          {
            "line_number": 20,
            "content": "    if item_id == \"foo\":"
          },
          {
            "line_number": 21,
            "content": "        return {\"id\": \"foo\", \"value\": \"there goes my hero\"}"
          },
          {
            "line_number": 22,
            "content": "    return JSONResponse(status_code=404, content={\"message\": \"Item not found\"})"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "docs_src/additional_responses/tutorial001_py310.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "symbol:docs_src/additional_responses/tutorial001_py310.py:read_item:19",
      "confidence_trigger": 0.77,
      "output_size_tokens": 359,
      "result": {
        "status": "ok",
        "file_path": "docs_src/additional_responses/tutorial001_py310.py",
        "start_line": 1,
        "end_line": 22,
        "total_lines_in_file": 22,
        "lines": [
          {
            "line_number": 1,
            "content": "from fastapi import FastAPI"
          },
          {
            "line_number": 2,
            "content": "from fastapi.responses import JSONResponse"
          },
          {
            "line_number": 3,
            "content": "from pydantic import BaseModel"
          },
          {
            "line_number": 4,
            "content": ""
          },
          {
            "line_number": 5,
            "content": ""
          },
          {
            "line_number": 6,
            "content": "class Item(BaseModel):"
          },
          {
            "line_number": 7,
            "content": "    id: str"
          },
          {
            "line_number": 8,
            "content": "    value: str"
          },
          {
            "line_number": 9,
            "content": ""
          },
          {
            "line_number": 10,
            "content": ""
          },
          {
            "line_number": 11,
            "content": "class Message(BaseModel):"
          },
          {
            "line_number": 12,
            "content": "    message: str"
          },
          {
            "line_number": 13,
            "content": ""
          },
          {
            "line_number": 14,
            "content": ""
          },
          {
            "line_number": 15,
            "content": "app = FastAPI()"
          },
          {
            "line_number": 16,
            "content": ""
          },
          {
            "line_number": 17,
            "content": ""
          },
          {
            "line_number": 18,
            "content": "@app.get(\"/items/{item_id}\", response_model=Item, responses={404: {\"model\": Message}})"
          },
          {
            "line_number": 19,
            "content": "async def read_item(item_id: str):"
          },
          {
            "line_number": 20,
            "content": "    if item_id == \"foo\":"
          },
          {
            "line_number": 21,
            "content": "        return {\"id\": \"foo\", \"value\": \"there goes my hero\"}"
          },
          {
            "line_number": 22,
            "content": "    return JSONResponse(status_code=404, content={\"message\": \"Item not found\"})"
          }
        ]
      }
    }
  ],
  "trace_file": "experiments\\reports\\external-drilldown\\batch-20260405-subagents\\fastapi-tf4-001\\traces\\trace-20260405T134249.jsonl"
}
