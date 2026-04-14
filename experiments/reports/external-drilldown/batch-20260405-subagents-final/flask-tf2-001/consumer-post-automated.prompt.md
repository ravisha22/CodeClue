You are running the AFTER pass of a CodeClue drill-down evaluation.

Rules:
- Start from the same clue projection below.
- Use the automated MCP drill-down evidence below as your only post-clue evidence.
- Do NOT inspect any other source beyond what is included in this prompt.
- Produce a revised answer that clearly reflects what the drill-down changed.

Task ID: flask-tf2-001
Family: TF2
Operation Family: OF2

Question:
If I change the `push` method in RequestContext (ctx.py) to be async, what other components would be impacted?

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
  "p_dependency_miss": 0.428571,
  "p_hallucination": 0.0,
  "code_density_risk": 0.147059,
  "confidence_overall": 0.487395,
  "lookup_decision_hint": "expanded_lookup",
  "operation_family": "OF2",
  "threshold": 0.9,
  "tool_call_budget": 15,
  "per_node_confidence": [
    {
      "node_id": "module:src/flask/app.py",
      "confidence": 0.85,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 41,
        "fan_out_z_score": 0.581,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "resolve_dependency",
          "args": {
            "node_id": "module:src/flask/app.py",
            "depth": 2
          },
          "rationale": "12 outgoing edge(s) point to nodes outside this projection; dependency closure is incomplete"
        },
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "module:src/flask/cli.py",
      "confidence": 0.85,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 42,
        "fan_out_z_score": 0.609,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "resolve_dependency",
          "args": {
            "node_id": "module:src/flask/cli.py",
            "depth": 2
          },
          "rationale": "18 outgoing edge(s) point to nodes outside this projection; dependency closure is incomplete"
        },
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "module:src/flask/ctx.py",
      "confidence": 0.85,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 30,
        "fan_out_z_score": 0.282,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "resolve_dependency",
          "args": {
            "node_id": "module:src/flask/ctx.py",
            "depth": 2
          },
          "rationale": "18 outgoing edge(s) point to nodes outside this projection; dependency closure is incomplete"
        },
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/ctx.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.__call__:1618",
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
        "fan_out_z_score": 0.618,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.__init__:310",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 2,
        "fan_out_z_score": 1.594,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.__init_subclass__:254",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 2,
        "fan_out_z_score": 1.594,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.async_to_sync:1079",
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
        "fan_out_z_score": -0.358,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.create_url_adapter:509",
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
        "fan_out_z_score": -0.358,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.dispatch_request:966",
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
        "fan_out_z_score": 2.57,
        "cross_file_span_ratio": 0.036,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.do_teardown_appcontext:1453",
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
        "fan_out_z_score": 0.618,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.do_teardown_request:1420",
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
        "fan_out_z_score": 0.618,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
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
        "fan_out_z_score": 0.618,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.finalize_request:1021",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 2,
        "fan_out_z_score": 1.594,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.full_dispatch_request:992",
      "confidence": 0.57,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 4,
        "fan_out_z_score": 3.546,
        "cross_file_span_ratio": 0.036,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.get_send_file_max_age:365",
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
        "fan_out_z_score": -0.358,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.handle_exception:897",
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
        "fan_out_z_score": 2.57,
        "cross_file_span_ratio": 0.036,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.handle_http_exception:830",
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
        "fan_out_z_score": 0.618,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.handle_user_exception:865",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 2,
        "fan_out_z_score": 1.594,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.log_exception:950",
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
        "fan_out_z_score": -0.358,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.make_default_options_response:1053",
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
        "fan_out_z_score": -0.358,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.make_response:1224",
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
        "fan_out_z_score": -0.358,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.preprocess_request:1366",
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
        "fan_out_z_score": 0.618,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.process_response:1394",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 2,
        "fan_out_z_score": 1.594,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.raise_routing_exception:562",
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
        "fan_out_z_score": -0.358,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.request_context:1501",
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
        "fan_out_z_score": -0.358,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.send_static_file:392",
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
        "fan_out_z_score": 0.618,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.test_request_context:1517",
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
        "fan_out_z_score": 0.618,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.update_template_context:590",
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
        "fan_out_z_score": 0.618,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.url_for:1102",
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
        "fan_out_z_score": 0.618,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:Flask.wsgi_app:1566",
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
        "fan_out_z_score": 2.57,
        "cross_file_span_ratio": 0.036,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:add_ctx:97",
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
        "fan_out_z_score": -0.358,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/app.py:remove_ctx:85",
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
        "fan_out_z_score": -0.358,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/app.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/cli.py:AppGroup.command:413",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 2,
        "fan_out_z_score": 1.594,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/cli.py:AppGroup.group:429",
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
        "fan_out_z_score": 0.618,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/cli.py:CertParamType:780",
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
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600",
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
        "fan_out_z_score": -0.358,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/cli.py:FlaskGroup.get_command:609",
      "confidence": 0.57,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 4,
        "fan_out_z_score": 3.546,
        "cross_file_span_ratio": 0.036,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636",
      "confidence": 0.57,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 4,
        "fan_out_z_score": 3.546,
        "cross_file_span_ratio": 0.036,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/cli.py:FlaskGroup.make_context:657",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 2,
        "fan_out_z_score": 1.594,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/cli.py:FlaskGroup.parse_args:678",
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
        "fan_out_z_score": 0.618,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/cli.py:NoAppException:37",
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
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/cli.py:ScriptInfo.load_app:333",
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
        "fan_out_z_score": 2.57,
        "cross_file_span_ratio": 0.036,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/cli.py:ScriptInfo:293",
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
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/cli.py:SeparatedPathType:867",
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
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/cli.py:_called_with_wrong_args:94",
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
        "fan_out_z_score": -0.358,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/cli.py:_env_file_callback:493",
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
        "fan_out_z_score": 0.618,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/cli.py:find_app_by_string:120",
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
        "fan_out_z_score": 7.451,
        "cross_file_span_ratio": 0.036,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/cli.py:find_best_app:41",
      "confidence": 0.57,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 4,
        "fan_out_z_score": 3.546,
        "cross_file_span_ratio": 0.036,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/cli.py:load_dotenv:698",
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
        "fan_out_z_score": -0.358,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/cli.py:main:1122",
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
        "fan_out_z_score": 0.618,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/cli.py:prepare_import:200",
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
        "fan_out_z_score": -0.358,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/cli.py:routes_command:1061",
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
        "fan_out_z_score": 0.618,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/cli.py:run_command:935",
      "confidence": 0.57,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 6,
        "fan_out_z_score": 5.499,
        "cross_file_span_ratio": 0.036,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/cli.py:shell_command:1001",
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
        "fan_out_z_score": 0.618,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/cli.py:show_server_banner:766",
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
        "fan_out_z_score": -0.358,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/cli.py:with_appcontext:380",
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
        "fan_out_z_score": 0.618,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/cli.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/ctx.py:AppContext.__enter__:506",
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
        "fan_out_z_score": 0.618,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/ctx.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/ctx.py:AppContext._get_session:381",
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
        "fan_out_z_score": -0.358,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/ctx.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/ctx.py:AppContext.copy:355",
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
        "fan_out_z_score": -0.358,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/ctx.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/ctx.py:AppContext.match_request:405",
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
        "fan_out_z_score": -0.358,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/ctx.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/ctx.py:AppContext.push:416",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 2,
        "fan_out_z_score": 1.594,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/ctx.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/ctx.py:AppContext.session:396",
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
        "fan_out_z_score": 0.618,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/ctx.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68",
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
        "fan_out_z_score": 0.618,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/ctx.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93",
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
        "fan_out_z_score": 0.618,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/ctx.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/ctx.py:after_this_request:118",
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
        "fan_out_z_score": 0.618,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/ctx.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/ctx.py:copy_current_request_context:154",
      "confidence": 0.77,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 2,
        "fan_out_z_score": 1.594,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/ctx.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/ctx.py:has_app_context:235",
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
        "fan_out_z_score": 0.618,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/ctx.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:src/flask/ctx.py:has_request_context:209",
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
        "fan_out_z_score": 0.618,
        "cross_file_span_ratio": 0.036,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "src/flask/ctx.py",
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
      "edge_id": "calls:symbol:src/flask/app.py:Flask.__call__:1618:symbol:src/flask/app.py:Flask.wsgi_app:1566:1625",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.__init__:310:symbol:src/flask/app.py:Flask.__init__:310:323",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.__init__:310:symbol:src/flask/app.py:Flask.send_static_file:392:362",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.__init_subclass__:254:symbol:src/flask/app.py:add_ctx:97:308",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.__init_subclass__:254:symbol:src/flask/app.py:remove_ctx:85:307",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.dispatch_request:966:symbol:src/flask/app.py:Flask.ensure_sync:1065:990",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.dispatch_request:966:symbol:src/flask/app.py:Flask.make_default_options_response:1053:987",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.dispatch_request:966:symbol:src/flask/app.py:Flask.raise_routing_exception:562:979",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.do_teardown_appcontext:1453:symbol:src/flask/app.py:Flask.ensure_sync:1065:1474",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.do_teardown_request:1420:symbol:src/flask/app.py:Flask.ensure_sync:1065:1446",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.ensure_sync:1065:symbol:src/flask/app.py:Flask.async_to_sync:1079:1075",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.finalize_request:1021:symbol:src/flask/app.py:Flask.make_response:1224:1039",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.finalize_request:1021:symbol:src/flask/app.py:Flask.process_response:1394:1041",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.full_dispatch_request:992:symbol:src/flask/app.py:Flask.dispatch_request:966:1016",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.full_dispatch_request:992:symbol:src/flask/app.py:Flask.finalize_request:1021:1019",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.full_dispatch_request:992:symbol:src/flask/app.py:Flask.handle_user_exception:865:1018",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.full_dispatch_request:992:symbol:src/flask/app.py:Flask.preprocess_request:1366:1014",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_exception:897:symbol:src/flask/app.py:Flask.ensure_sync:1065:946",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_exception:897:symbol:src/flask/app.py:Flask.finalize_request:1021:948",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_exception:897:symbol:src/flask/app.py:Flask.log_exception:950:940",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_http_exception:830:symbol:src/flask/app.py:Flask.ensure_sync:1065:863",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_user_exception:865:symbol:src/flask/app.py:Flask.ensure_sync:1065:895",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_user_exception:865:symbol:src/flask/app.py:Flask.handle_http_exception:830:888",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.preprocess_request:1366:symbol:src/flask/app.py:Flask.ensure_sync:1065:1387",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.process_response:1394:symbol:src/flask/app.py:Flask.ensure_sync:1065:1408",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.process_response:1394:symbol:src/flask/app.py:Flask.ensure_sync:1065:1413",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.send_static_file:392:symbol:src/flask/app.py:Flask.get_send_file_max_age:365:409",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.test_request_context:1517:symbol:src/flask/app.py:Flask.request_context:1501:1564",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.update_template_context:590:symbol:src/flask/app.py:Flask.ensure_sync:1065:616",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.url_for:1102:symbol:src/flask/app.py:Flask.create_url_adapter:509:1182",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.wsgi_app:1566:symbol:src/flask/app.py:Flask.full_dispatch_request:992:1597",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.wsgi_app:1566:symbol:src/flask/app.py:Flask.handle_exception:897:1600",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/app.py:Flask.wsgi_app:1566:symbol:src/flask/app.py:Flask.request_context:1501:1592",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:AppGroup.command:413:symbol:src/flask/cli.py:AppGroup.command:413:425",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:AppGroup.command:413:symbol:src/flask/cli.py:with_appcontext:380:424",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:AppGroup.group:429:symbol:src/flask/cli.py:AppGroup.group:429:437",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.get_command:609:symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600:610",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.get_command:609:symbol:src/flask/cli.py:FlaskGroup.get_command:609:613",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.get_command:609:symbol:src/flask/cli.py:FlaskGroup.get_command:609:634",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.get_command:609:symbol:src/flask/cli.py:ScriptInfo.load_app:333:623",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600:637",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:639",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:645",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:symbol:src/flask/cli.py:ScriptInfo.load_app:333:645",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.make_context:657:symbol:src/flask/cli.py:FlaskGroup.make_context:657:676",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.make_context:657:symbol:src/flask/cli.py:ScriptInfo:293:670",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.parse_args:678:symbol:src/flask/cli.py:FlaskGroup.parse_args:678:688",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:ScriptInfo.load_app:333:symbol:src/flask/cli.py:NoAppException:37:359",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:ScriptInfo.load_app:333:symbol:src/flask/cli.py:prepare_import:200:348",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:ScriptInfo.load_app:333:symbol:src/flask/cli.py:prepare_import:200:352",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:_env_file_callback:493:symbol:src/flask/cli.py:load_dotenv:698:510",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:131",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:142",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:159",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:163",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:170",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:183",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:194",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:_called_with_wrong_args:94:180",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:find_best_app:41:symbol:src/flask/cli.py:NoAppException:37:60",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:find_best_app:41:symbol:src/flask/cli.py:NoAppException:37:80",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:find_best_app:41:symbol:src/flask/cli.py:NoAppException:37:87",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:find_best_app:41:symbol:src/flask/cli.py:_called_with_wrong_args:94:77",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:main:1122:symbol:src/flask/cli.py:main:1122:1123",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:routes_command:1061:symbol:src/flask/cli.py:AppGroup.command:413:1048",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:AppGroup.command:413:882",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:CertParamType:780:887",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:ScriptInfo.load_app:333:955",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:SeparatedPathType:867:918",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:SeparatedPathType:867:927",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:show_server_banner:766:981",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:shell_command:1001:symbol:src/flask/cli.py:AppGroup.command:413:999",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/cli.py:with_appcontext:380:symbol:src/flask/cli.py:ScriptInfo.load_app:333:397",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/ctx.py:AppContext.__enter__:506:symbol:src/flask/ctx.py:AppContext.push:416:507",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/ctx.py:AppContext.push:416:symbol:src/flask/ctx.py:AppContext._get_session:381:439",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/ctx.py:AppContext.push:416:symbol:src/flask/ctx.py:AppContext.match_request:405:444",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/ctx.py:AppContext.session:396:symbol:src/flask/ctx.py:AppContext._get_session:381:401",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:77",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93:symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93:103",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/ctx.py:after_this_request:118:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:139",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/ctx.py:copy_current_request_context:154:symbol:src/flask/ctx.py:AppContext.copy:355:200",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/ctx.py:copy_current_request_context:154:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:192",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/ctx.py:has_app_context:235:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:257",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:src/flask/ctx.py:has_request_context:209:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:232",
      "confidence": 1.0,
      "suggested_actions": []
    }
  ]
}

## Projection Stats
{
  "seed_count": 42,
  "initial_seed_count": 20,
  "projected_node_count": 68,
  "projected_edge_count": 84,
  "graph_node_count": 1712,
  "graph_edge_count": 2163
}

## Projected Nodes
[
  {
    "node_id": "module:src/flask/app.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 0,
      "byte_end": 65423,
      "ast_path": "module",
      "content_hash": "09a3a1a7b3d1f174a4d274da2c329f9377745bbf6f138b17c3187352f7466a15"
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
      "symbol_name": "src/flask/app.py",
      "symbol_type": "module",
      "tier": 1
    },
    "confidence": 1.0
  },
  {
    "node_id": "module:src/flask/cli.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 0,
      "byte_end": 36808,
      "ast_path": "module",
      "content_hash": "1f2e6624f5a34c86eb0e1928c6acb6b85297b19be0e039791bf0c065d2b2b7af"
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
      "symbol_name": "src/flask/cli.py",
      "symbol_type": "module",
      "tier": 1
    },
    "confidence": 1.0
  },
  {
    "node_id": "module:src/flask/ctx.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "src/flask/ctx.py",
      "byte_start": 0,
      "byte_end": 18104,
      "ast_path": "module",
      "content_hash": "fdff186ec6f47fa5a15fe5947c843bbd2ee20ab0be34036ea8dedaaa89c58f9f"
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
      "symbol_name": "src/flask/ctx.py",
      "symbol_type": "module",
      "tier": 1
    },
    "confidence": 1.0
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.__call__:1618",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 65068,
      "byte_end": 65422,
      "ast_path": "function:Flask.__call__",
      "content_hash": "16b710f47ea72347274ceccb21649a5a4ce7b9a941c1d69f39a6109c157cec97"
    },
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.wsgi_app:1566"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function __call__",
      "symbol_name": "__call__",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.__init__:310",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 12632,
      "byte_end": 15001,
      "ast_path": "function:Flask.__init__",
      "content_hash": "57da7ea2afea8f19b08c324002385c3be9baf0c6407c163a9e8049ec5a9c849b"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.__init__:310"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.__init__:310"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.send_static_file:392"
        }
      ],
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
    "node_id": "symbol:src/flask/app.py:Flask.__init_subclass__:254",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 10298,
      "byte_end": 12626,
      "ast_path": "function:Flask.__init_subclass__",
      "content_hash": "3b2870215f971ca43d2861a3add34b60453e15b3bc67e6dfd92c08468e07e45b"
    },
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:add_ctx:97"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:remove_ctx:85"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function __init_subclass__",
      "symbol_name": "__init_subclass__",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.async_to_sync:1079",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 43264,
      "byte_end": 44006,
      "ast_path": "function:Flask.async_to_sync",
      "content_hash": "84cc58adce4ab6990926b0445c184ef72fce3510204e177b41ccedb54327dedd"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function async_to_sync",
      "symbol_name": "async_to_sync",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.create_url_adapter:509",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 20375,
      "byte_end": 22649,
      "ast_path": "function:Flask.create_url_adapter",
      "content_hash": "326d82d2151f3a5db94d71701a097b93b1d963ff195012f28cc5d5aff7af34f3"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.url_for:1102"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function create_url_adapter",
      "symbol_name": "create_url_adapter",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.dispatch_request:966",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 38725,
      "byte_end": 39969,
      "ast_path": "function:Flask.dispatch_request",
      "content_hash": "f9c7ebf70a162afaa3e706b8d4162e9ff9869b62736df8d163e83a5a97c1ba09"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.full_dispatch_request:992"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.make_default_options_response:1053"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.raise_routing_exception:562"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function dispatch_request",
      "symbol_name": "dispatch_request",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.do_teardown_appcontext:1453",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 58699,
      "byte_end": 59703,
      "ast_path": "function:Flask.do_teardown_appcontext",
      "content_hash": "3c740347ee3ada59e3e126a5b9beaaaf97d94d1de8659072b69064bfd2c290e2"
    },
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function do_teardown_appcontext",
      "symbol_name": "do_teardown_appcontext",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.do_teardown_request:1420",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 57361,
      "byte_end": 58693,
      "ast_path": "function:Flask.do_teardown_request",
      "content_hash": "041737b4aa090af7eab203e32f8e5fea50ecb08f85041dd094e4f55928e97951"
    },
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function do_teardown_request",
      "symbol_name": "do_teardown_request",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 42765,
      "byte_end": 43258,
      "ast_path": "function:Flask.ensure_sync",
      "content_hash": "6b2a9bda8dd8e46b5098a7f3d631a7cfeda476f534749cb1101e21b18705a1ae"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.dispatch_request:966"
        },
        {
          "source": "symbol:src/flask/app.py:Flask.do_teardown_appcontext:1453"
        },
        {
          "source": "symbol:src/flask/app.py:Flask.do_teardown_request:1420"
        },
        {
          "source": "symbol:src/flask/app.py:Flask.handle_exception:897"
        },
        {
          "source": "symbol:src/flask/app.py:Flask.handle_http_exception:830"
        },
        {
          "source": "symbol:src/flask/app.py:Flask.handle_user_exception:865"
        },
        {
          "source": "symbol:src/flask/app.py:Flask.preprocess_request:1366"
        },
        {
          "source": "symbol:src/flask/app.py:Flask.process_response:1394"
        },
        {
          "source": "symbol:src/flask/app.py:Flask.update_template_context:590"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.async_to_sync:1079"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function ensure_sync",
      "symbol_name": "ensure_sync",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.finalize_request:1021",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 41065,
      "byte_end": 42285,
      "ast_path": "function:Flask.finalize_request",
      "content_hash": "7a66de46aa56116313f6ecb33949c6c7b43a88eec316c09a9a052b2cb946c9ca"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.full_dispatch_request:992"
        },
        {
          "source": "symbol:src/flask/app.py:Flask.handle_exception:897"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.make_response:1224"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.process_response:1394"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function finalize_request",
      "symbol_name": "finalize_request",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.full_dispatch_request:992",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 40006,
      "byte_end": 41059,
      "ast_path": "function:Flask.full_dispatch_request",
      "content_hash": "8e19522cc1da2b297a32103626a277c3fc185dcd358b57b6df698d2caf911b62"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.wsgi_app:1566"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.dispatch_request:966"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.finalize_request:1021"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.handle_user_exception:865"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.preprocess_request:1366"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function full_dispatch_request",
      "symbol_name": "full_dispatch_request",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.get_send_file_max_age:365",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 15007,
      "byte_end": 15930,
      "ast_path": "function:Flask.get_send_file_max_age",
      "content_hash": "01c9df7cbf2b57c53a553c81d0eebfc02ea31dd964b0ddb5e21178af8b70ed59"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.send_static_file:392"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function get_send_file_max_age",
      "symbol_name": "get_send_file_max_age",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.handle_exception:897",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 35936,
      "byte_end": 38144,
      "ast_path": "function:Flask.handle_exception",
      "content_hash": "94fa1a557d158357fa24901a30ed508910248cbd59a954626e771aa0c02f4b6b"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.wsgi_app:1566"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.finalize_request:1021"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.log_exception:950"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function handle_exception",
      "symbol_name": "handle_exception",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.handle_http_exception:830",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 33366,
      "byte_end": 34696,
      "ast_path": "function:Flask.handle_http_exception",
      "content_hash": "54f2cc1a7277891f9984d463c16bda67f3a49ccdd57ec93838af07a21370ddd5"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.handle_user_exception:865"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function handle_http_exception",
      "symbol_name": "handle_http_exception",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.handle_user_exception:865",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 34733,
      "byte_end": 35899,
      "ast_path": "function:Flask.handle_user_exception",
      "content_hash": "65f0f36c19963deafce37ba086efdf0079617dbcc34a99773cb839e4f2a3f42c"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.full_dispatch_request:992"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.handle_http_exception:830"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function handle_user_exception",
      "symbol_name": "handle_user_exception",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.log_exception:950",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 38150,
      "byte_end": 38719,
      "ast_path": "function:Flask.log_exception",
      "content_hash": "5c6d1f2f1c4c9778085f6ed59c1feba42b243771987ea7552ad00c4aff079b15"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.handle_exception:897"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function log_exception",
      "symbol_name": "log_exception",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.make_default_options_response:1053",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 42291,
      "byte_end": 42759,
      "ast_path": "function:Flask.make_default_options_response",
      "content_hash": "8a2f74eb652357b7559bdbb7f084cc51905249d5b85e3e9d9198b941e35d972c"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.dispatch_request:966"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function make_default_options_response",
      "symbol_name": "make_default_options_response",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.make_response:1224",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 49141,
      "byte_end": 55019,
      "ast_path": "function:Flask.make_response",
      "content_hash": "0d06b529b46e02f98ab2983ee4c22e3ec5ad669894e21669c941ba539f4a86d5"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.finalize_request:1021"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function make_response",
      "symbol_name": "make_response",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.preprocess_request:1366",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 55025,
      "byte_end": 56181,
      "ast_path": "function:Flask.preprocess_request",
      "content_hash": "e8241727e4adceb04aa62dcb3ba158f8fcade2feeb35cf6de5cfa4c2cab2867d"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.full_dispatch_request:992"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function preprocess_request",
      "symbol_name": "preprocess_request",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.process_response:1394",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 56187,
      "byte_end": 57355,
      "ast_path": "function:Flask.process_response",
      "content_hash": "01df3451a006199a5f04d18eab36b8bca8732d704c72fa60153e37a928bdb205"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.finalize_request:1021"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function process_response",
      "symbol_name": "process_response",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.raise_routing_exception:562",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 22655,
      "byte_end": 23625,
      "ast_path": "function:Flask.raise_routing_exception",
      "content_hash": "295ced4ad7dbf6e1f2e2ea95eebe4e5ab8d210f48fca8c2df8e994083551724e"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.dispatch_request:966"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function raise_routing_exception",
      "symbol_name": "raise_routing_exception",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.request_context:1501",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 60344,
      "byte_end": 61083,
      "ast_path": "function:Flask.request_context",
      "content_hash": "d233642d6405c7af5388bff1ffaeef51efc5feba7d33df39011b66e753588748"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.test_request_context:1517"
        },
        {
          "source": "symbol:src/flask/app.py:Flask.wsgi_app:1566"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function request_context",
      "symbol_name": "request_context",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.send_static_file:392",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 15967,
      "byte_end": 16782,
      "ast_path": "function:Flask.send_static_file",
      "content_hash": "27d2683e2746c869cb91807722d38ff946b71fa05f1a5f77b3bb6267d77abb71"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.__init__:310"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.get_send_file_max_age:365"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function send_static_file",
      "symbol_name": "send_static_file",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.test_request_context:1517",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 61089,
      "byte_end": 63177,
      "ast_path": "function:Flask.test_request_context",
      "content_hash": "01b99fd691fc355b938491b41a842566d73cfbe0d595bf74ca24097081c3a556"
    },
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.request_context:1501"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function test_request_context",
      "symbol_name": "test_request_context",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.update_template_context:590",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 23631,
      "byte_end": 24895,
      "ast_path": "function:Flask.update_template_context",
      "content_hash": "9605416d8b7e0803328f2aec29c5e5e0964d3eb5c6e6325a767176ee0456d857"
    },
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function update_template_context",
      "symbol_name": "update_template_context",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.url_for:1102",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 44012,
      "byte_end": 49135,
      "ast_path": "function:Flask.url_for",
      "content_hash": "b476a0dec4c79242e60a8469e83a4cb44b4645c44efe3fd67672d4284fe3239b"
    },
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.create_url_adapter:509"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function url_for",
      "symbol_name": "url_for",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:Flask.wsgi_app:1566",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 63183,
      "byte_end": 65062,
      "ast_path": "function:Flask.wsgi_app",
      "content_hash": "efd78a36ec1d79465da93b82553ebef531fd2c598cdd1231b32ebc959f3463e9"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.__call__:1618"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.full_dispatch_request:992"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.handle_exception:897"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/app.py:Flask.request_context:1501"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function wsgi_app",
      "symbol_name": "wsgi_app",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:add_ctx:97",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 3221,
      "byte_end": 3575,
      "ast_path": "function:add_ctx",
      "content_hash": "6d3df893048dde40a2e8d8ecda5c256d98b3f17c369b01fa7dffafe617fdc8ec"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.__init_subclass__:254"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function add_ctx",
      "symbol_name": "add_ctx",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/app.py:remove_ctx:85",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/app.py",
      "byte_start": 2818,
      "byte_end": 3075,
      "ast_path": "function:remove_ctx",
      "content_hash": "5c58ac17b76b3fb185090bf51555c9b39cbb0342f9bf535151347fe2f1826071"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/app.py:Flask.__init_subclass__:254"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function remove_ctx",
      "symbol_name": "remove_ctx",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/cli.py:AppGroup.command:413",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 13060,
      "byte_end": 13759,
      "ast_path": "function:AppGroup.command",
      "content_hash": "7cbc7fe2247437eb5981de5bc005d1176e0e2c707a67cff4b2d3fb18f6c1a623"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:AppGroup.command:413"
        },
        {
          "source": "symbol:src/flask/cli.py:routes_command:1061"
        },
        {
          "source": "symbol:src/flask/cli.py:run_command:935"
        },
        {
          "source": "symbol:src/flask/cli.py:shell_command:1001"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:AppGroup.command:413"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:with_appcontext:380"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function command",
      "symbol_name": "command",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/cli.py:AppGroup.group:429",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 13765,
      "byte_end": 14173,
      "ast_path": "function:AppGroup.group",
      "content_hash": "56dfb90977bf75433236c3ba6b505a74d878e1c9585b2b5bec395a7e9b514a2d"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:AppGroup.group:429"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:AppGroup.group:429"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function group",
      "symbol_name": "group",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/cli.py:CertParamType:780",
    "node_type": "class",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 26527,
      "byte_end": 27959,
      "ast_path": "class:CertParamType",
      "content_hash": "5a97b025ef493def3d3226a4bb2f57c50062059830724a3b0f77a82a5bc09db0"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:run_command:935"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "class CertParamType",
      "symbol_name": "CertParamType",
      "symbol_type": "class",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 20011,
      "byte_end": 20281,
      "ast_path": "function:FlaskGroup._load_plugin_commands",
      "content_hash": "e1a57664073884e8cf7c5c0237ee175695451f125ceaa7b6229d0e0daa044b68"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:FlaskGroup.get_command:609"
        },
        {
          "source": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _load_plugin_commands",
      "symbol_name": "_load_plugin_commands",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/cli.py:FlaskGroup.get_command:609",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 20287,
      "byte_end": 21344,
      "ast_path": "function:FlaskGroup.get_command",
      "content_hash": "cfb4a2ed09a26b0a2b396dbc38117a618b47e6e26c2df25943bf4098c40e42d4"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:FlaskGroup.get_command:609"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:FlaskGroup.get_command:609"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:ScriptInfo.load_app:333"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function get_command",
      "symbol_name": "get_command",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 21350,
      "byte_end": 22230,
      "ast_path": "function:FlaskGroup.list_commands",
      "content_hash": "db7aa35213f300bcbd95996c0762822d243516cc3715c21cd85a2dbe8f8a6b06"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:ScriptInfo.load_app:333"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function list_commands",
      "symbol_name": "list_commands",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/cli.py:FlaskGroup.make_context:657",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 22236,
      "byte_end": 23032,
      "ast_path": "function:FlaskGroup.make_context",
      "content_hash": "d5fd541910368dc55fd8ad4dc200c23d2768876ebc1988b2a1ec121e23e2fd56"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:FlaskGroup.make_context:657"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:FlaskGroup.make_context:657"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:ScriptInfo:293"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function make_context",
      "symbol_name": "make_context",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/cli.py:FlaskGroup.parse_args:678",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 23038,
      "byte_end": 23595,
      "ast_path": "function:FlaskGroup.parse_args",
      "content_hash": "d6cefdc254f2eedcbf1b83d1708a912a67f3fe16092180cb1683cd729b27da8c"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:FlaskGroup.parse_args:678"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:FlaskGroup.parse_args:678"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function parse_args",
      "symbol_name": "parse_args",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/cli.py:NoAppException:37",
    "node_type": "class",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 793,
      "byte_end": 894,
      "ast_path": "class:NoAppException",
      "content_hash": "9e968dd91274d585a76dc0e384e22c73915368b63eb1b58c2d5b72290ac35a19"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:ScriptInfo.load_app:333"
        },
        {
          "source": "symbol:src/flask/cli.py:find_app_by_string:120"
        },
        {
          "source": "symbol:src/flask/cli.py:find_best_app:41"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "class NoAppException",
      "symbol_name": "NoAppException",
      "symbol_type": "class",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/cli.py:ScriptInfo.load_app:333",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 10203,
      "byte_end": 11724,
      "ast_path": "function:ScriptInfo.load_app",
      "content_hash": "fcc5e00092c0dcfde838fbfd79d5492ad1ce3415cd57f8c8c088308d920dffb6"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:FlaskGroup.get_command:609"
        },
        {
          "source": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636"
        },
        {
          "source": "symbol:src/flask/cli.py:run_command:935"
        },
        {
          "source": "symbol:src/flask/cli.py:with_appcontext:380"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:NoAppException:37"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:prepare_import:200"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function load_app",
      "symbol_name": "load_app",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/cli.py:ScriptInfo:293",
    "node_type": "class",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 8628,
      "byte_end": 11724,
      "ast_path": "class:ScriptInfo",
      "content_hash": "592901e1d1006934831a264b7b30b61fb9fc1075d47bb685d40e4ef31e911431"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:FlaskGroup.make_context:657"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "class ScriptInfo",
      "symbol_name": "ScriptInfo",
      "symbol_type": "class",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/cli.py:SeparatedPathType:867",
    "node_type": "class",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 29098,
      "byte_end": 29677,
      "ast_path": "class:SeparatedPathType",
      "content_hash": "4e7c63eca412e2011eb711ff409e2fd4fe283745f8dab01fd8475913b13cfe7c"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:run_command:935"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "class SeparatedPathType",
      "symbol_name": "SeparatedPathType",
      "symbol_type": "class",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/cli.py:_called_with_wrong_args:94",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 2679,
      "byte_end": 3426,
      "ast_path": "function:_called_with_wrong_args",
      "content_hash": "5152c1adb4a87c355e684d73ccffa080ae06f81d67a6749406bddc65dae81c69"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:find_app_by_string:120"
        },
        {
          "source": "symbol:src/flask/cli.py:find_best_app:41"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _called_with_wrong_args",
      "symbol_name": "_called_with_wrong_args",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/cli.py:_env_file_callback:493",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 15909,
      "byte_end": 16666,
      "ast_path": "function:_env_file_callback",
      "content_hash": "ae6497dbece96def68c74d214584647fbd8ea5506ecca1e520ae0b70cf0e75a5"
    },
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:load_dotenv:698"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _env_file_callback",
      "symbol_name": "_env_file_callback",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/cli.py:find_app_by_string:120",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 3429,
      "byte_end": 6072,
      "ast_path": "function:find_app_by_string",
      "content_hash": "9bac2537de80d6198f90f5cb0db6004ffe1eb5ee047b1194b8b8e925bb41620b"
    },
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:NoAppException:37"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:_called_with_wrong_args:94"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function find_app_by_string",
      "symbol_name": "find_app_by_string",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/cli.py:find_best_app:41",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 897,
      "byte_end": 2676,
      "ast_path": "function:find_best_app",
      "content_hash": "31e4877b92dac2e4b30a01ac6de6b33aa9ac352b31f4f3020ce80f924a4f49b2"
    },
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:NoAppException:37"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:_called_with_wrong_args:94"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function find_best_app",
      "symbol_name": "find_best_app",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/cli.py:load_dotenv:698",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 23897,
      "byte_end": 26057,
      "ast_path": "function:load_dotenv",
      "content_hash": "2a267c0f6aafc25803425e9ae8180528f049b3052338b96d3aca2680293a7937"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:_env_file_callback:493"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function load_dotenv",
      "symbol_name": "load_dotenv",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/cli.py:main:1122",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 36733,
      "byte_end": 36767,
      "ast_path": "function:main",
      "content_hash": "3ce7e69224f9911d2368576d8d2636e55191585be61b570379a866d7eb8052c7"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:main:1122"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:main:1122"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function main",
      "symbol_name": "main",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/cli.py:prepare_import:200",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 6075,
      "byte_end": 6833,
      "ast_path": "function:prepare_import",
      "content_hash": "6f782cd47ba837652c22c7821a8ed94633d643c42a6d1e73afcfdbe528810040"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:ScriptInfo.load_app:333"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function prepare_import",
      "symbol_name": "prepare_import",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/cli.py:routes_command:1061",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 35041,
      "byte_end": 36462,
      "ast_path": "function:routes_command",
      "content_hash": "de54c495f02d2082084e70b33ad58590157df474c65053fbcd2d33db2f21cb33"
    },
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:AppGroup.command:413"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function routes_command",
      "symbol_name": "routes_command",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/cli.py:run_command:935",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 31221,
      "byte_end": 32873,
      "ast_path": "function:run_command",
      "content_hash": "274ef091406ad22f695821c2424adb1a05b3230349a4c26d2bf2426e32db69ee"
    },
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:AppGroup.command:413"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:CertParamType:780"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:ScriptInfo.load_app:333"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:SeparatedPathType:867"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:show_server_banner:766"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function run_command",
      "symbol_name": "run_command",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/cli.py:shell_command:1001",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 33009,
      "byte_end": 34586,
      "ast_path": "function:shell_command",
      "content_hash": "38fdf9991c96e369786c2b407f792344c23c3deb4920db80d4b857076589df8d"
    },
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:AppGroup.command:413"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function shell_command",
      "symbol_name": "shell_command",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/cli.py:show_server_banner:766",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 26104,
      "byte_end": 26524,
      "ast_path": "function:show_server_banner",
      "content_hash": "4cacbd42a7d6bb09208e5d498b4413f2ea05e91a570f49c7a05bb2824babb7f2"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:run_command:935"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function show_server_banner",
      "symbol_name": "show_server_banner",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/cli.py:with_appcontext:380",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/cli.py",
      "byte_start": 11849,
      "byte_end": 12726,
      "ast_path": "function:with_appcontext",
      "content_hash": "295814aff7ae90b368a4bfe6751cfa9eb672f4d6edd3e32e39da31b5cd858052"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/cli.py:AppGroup.command:413"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/cli.py:ScriptInfo.load_app:333"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function with_appcontext",
      "symbol_name": "with_appcontext",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/ctx.py:AppContext.__enter__:506",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/ctx.py",
      "byte_start": 17141,
      "byte_end": 17212,
      "ast_path": "function:AppContext.__enter__",
      "content_hash": "49d6e2603d322097fb8af9c91208bb12a9cb537500d3ed7e1510aae36fb00050"
    },
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/ctx.py:AppContext.push:416"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function __enter__",
      "symbol_name": "__enter__",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/ctx.py:AppContext._get_session:381",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/ctx.py",
      "byte_start": 12480,
      "byte_end": 12986,
      "ast_path": "function:AppContext._get_session",
      "content_hash": "c7002c97308535374aae1e0a5498d7487ec697c65c3313c915895f1be8e8a8af"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/ctx.py:AppContext.push:416"
        },
        {
          "source": "symbol:src/flask/ctx.py:AppContext.session:396"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _get_session",
      "symbol_name": "_get_session",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/ctx.py:AppContext.copy:355",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/ctx.py",
      "byte_start": 11645,
      "byte_end": 12093,
      "ast_path": "function:AppContext.copy",
      "content_hash": "567f7d1eba70f4f7ded882364729684643188fed01d229fa7ce27101de211eec"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/ctx.py:copy_current_request_context:154"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function copy",
      "symbol_name": "copy",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/ctx.py:AppContext.match_request:405",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/ctx.py",
      "byte_start": 13388,
      "byte_end": 13856,
      "ast_path": "function:AppContext.match_request",
      "content_hash": "30a3e8e2b7c2766b5f4a4905aa8b3b578b81ff809b295943a096e0091092127e"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/ctx.py:AppContext.push:416"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function match_request",
      "symbol_name": "match_request",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/ctx.py:AppContext.push:416",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/ctx.py",
      "byte_start": 13890,
      "byte_end": 15072,
      "ast_path": "function:AppContext.push",
      "content_hash": "baea61546581cd071253f636eab7755bb187517fc7ef18792714d8ff15c99ceb"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/ctx.py:AppContext.__enter__:506"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/ctx.py:AppContext._get_session:381"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/ctx.py:AppContext.match_request:405"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function push",
      "symbol_name": "push",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/ctx.py:AppContext.session:396",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/ctx.py",
      "byte_start": 13006,
      "byte_end": 13382,
      "ast_path": "function:AppContext.session",
      "content_hash": "590089f091d3708bc6500e680c2a3c5f5d9f23d40cd1afc1d06956bf353bd989"
    },
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/ctx.py:AppContext._get_session:381"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function session",
      "symbol_name": "session",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/ctx.py",
      "byte_start": 1701,
      "byte_end": 2066,
      "ast_path": "function:_AppCtxGlobals.get",
      "content_hash": "4cf395aed2615680e0cf616b5c5c1c824db38fd29a94ac5e59ed38cb723e5da8"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68"
        },
        {
          "source": "symbol:src/flask/ctx.py:after_this_request:118"
        },
        {
          "source": "symbol:src/flask/ctx.py:copy_current_request_context:154"
        },
        {
          "source": "symbol:src/flask/ctx.py:has_app_context:235"
        },
        {
          "source": "symbol:src/flask/ctx.py:has_request_context:209"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function get",
      "symbol_name": "get",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/ctx.py",
      "byte_start": 2565,
      "byte_end": 3008,
      "ast_path": "function:_AppCtxGlobals.setdefault",
      "content_hash": "a1b558471d75d55bc52218b7f969c7e3837f8dd415293c498a5fb423acdc8cc1"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function setdefault",
      "symbol_name": "setdefault",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/ctx.py:after_this_request:118",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/ctx.py",
      "byte_start": 3356,
      "byte_end": 4338,
      "ast_path": "function:after_this_request",
      "content_hash": "590fe62a7a96a19cbee51dd4bca788f3af64e20de69d6ead3cabd6a43c949c81"
    },
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function after_this_request",
      "symbol_name": "after_this_request",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/ctx.py:copy_current_request_context:154",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/ctx.py",
      "byte_start": 4392,
      "byte_end": 6364,
      "ast_path": "function:copy_current_request_context",
      "content_hash": "9504136be71c1a8e4bb30c06be7dac93ce3e790126eeba4b8142319bbe08e413"
    },
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/ctx.py:AppContext.copy:355"
        },
        {
          "is_external": false,
          "target": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function copy_current_request_context",
      "symbol_name": "copy_current_request_context",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/ctx.py:has_app_context:235",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/ctx.py",
      "byte_start": 7138,
      "byte_end": 7823,
      "ast_path": "function:has_app_context",
      "content_hash": "5da5ef672c2c455b670186d0805938dfb0fca798aba4a35efe3d992b4455a99a"
    },
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function has_app_context",
      "symbol_name": "has_app_context",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:src/flask/ctx.py:has_request_context:209",
    "node_type": "function",
    "source_anchor": {
      "file_path": "src/flask/ctx.py",
      "byte_start": 6397,
      "byte_end": 7135,
      "ast_path": "function:has_request_context",
      "content_hash": "888098922a159d358f8b355821b2f8786bb1d134f4257b8c69d8ca11b4296d02"
    },
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function has_request_context",
      "symbol_name": "has_request_context",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  }
]

## Projected Edges
[
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.__call__:1618:symbol:src/flask/app.py:Flask.wsgi_app:1566:1625",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.__call__:1618",
    "to_node": "symbol:src/flask/app.py:Flask.wsgi_app:1566",
    "evidence": {
      "line": 1625,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.__init__:310:symbol:src/flask/app.py:Flask.__init__:310:323",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.__init__:310",
    "to_node": "symbol:src/flask/app.py:Flask.__init__:310",
    "evidence": {
      "line": 323,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.__init__:310:symbol:src/flask/app.py:Flask.send_static_file:392:362",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.__init__:310",
    "to_node": "symbol:src/flask/app.py:Flask.send_static_file:392",
    "evidence": {
      "line": 362,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.__init_subclass__:254:symbol:src/flask/app.py:add_ctx:97:308",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.__init_subclass__:254",
    "to_node": "symbol:src/flask/app.py:add_ctx:97",
    "evidence": {
      "line": 308,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.__init_subclass__:254:symbol:src/flask/app.py:remove_ctx:85:307",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.__init_subclass__:254",
    "to_node": "symbol:src/flask/app.py:remove_ctx:85",
    "evidence": {
      "line": 307,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.dispatch_request:966:symbol:src/flask/app.py:Flask.ensure_sync:1065:990",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.dispatch_request:966",
    "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
    "evidence": {
      "line": 990,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.dispatch_request:966:symbol:src/flask/app.py:Flask.make_default_options_response:1053:987",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.dispatch_request:966",
    "to_node": "symbol:src/flask/app.py:Flask.make_default_options_response:1053",
    "evidence": {
      "line": 987,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.dispatch_request:966:symbol:src/flask/app.py:Flask.raise_routing_exception:562:979",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.dispatch_request:966",
    "to_node": "symbol:src/flask/app.py:Flask.raise_routing_exception:562",
    "evidence": {
      "line": 979,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.do_teardown_appcontext:1453:symbol:src/flask/app.py:Flask.ensure_sync:1065:1474",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.do_teardown_appcontext:1453",
    "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
    "evidence": {
      "line": 1474,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.do_teardown_request:1420:symbol:src/flask/app.py:Flask.ensure_sync:1065:1446",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.do_teardown_request:1420",
    "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
    "evidence": {
      "line": 1446,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.ensure_sync:1065:symbol:src/flask/app.py:Flask.async_to_sync:1079:1075",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
    "to_node": "symbol:src/flask/app.py:Flask.async_to_sync:1079",
    "evidence": {
      "line": 1075,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.finalize_request:1021:symbol:src/flask/app.py:Flask.make_response:1224:1039",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.finalize_request:1021",
    "to_node": "symbol:src/flask/app.py:Flask.make_response:1224",
    "evidence": {
      "line": 1039,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.finalize_request:1021:symbol:src/flask/app.py:Flask.process_response:1394:1041",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.finalize_request:1021",
    "to_node": "symbol:src/flask/app.py:Flask.process_response:1394",
    "evidence": {
      "line": 1041,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.full_dispatch_request:992:symbol:src/flask/app.py:Flask.dispatch_request:966:1016",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.full_dispatch_request:992",
    "to_node": "symbol:src/flask/app.py:Flask.dispatch_request:966",
    "evidence": {
      "line": 1016,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.full_dispatch_request:992:symbol:src/flask/app.py:Flask.finalize_request:1021:1019",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.full_dispatch_request:992",
    "to_node": "symbol:src/flask/app.py:Flask.finalize_request:1021",
    "evidence": {
      "line": 1019,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.full_dispatch_request:992:symbol:src/flask/app.py:Flask.handle_user_exception:865:1018",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.full_dispatch_request:992",
    "to_node": "symbol:src/flask/app.py:Flask.handle_user_exception:865",
    "evidence": {
      "line": 1018,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.full_dispatch_request:992:symbol:src/flask/app.py:Flask.preprocess_request:1366:1014",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.full_dispatch_request:992",
    "to_node": "symbol:src/flask/app.py:Flask.preprocess_request:1366",
    "evidence": {
      "line": 1014,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_exception:897:symbol:src/flask/app.py:Flask.ensure_sync:1065:946",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.handle_exception:897",
    "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
    "evidence": {
      "line": 946,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_exception:897:symbol:src/flask/app.py:Flask.finalize_request:1021:948",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.handle_exception:897",
    "to_node": "symbol:src/flask/app.py:Flask.finalize_request:1021",
    "evidence": {
      "line": 948,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_exception:897:symbol:src/flask/app.py:Flask.log_exception:950:940",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.handle_exception:897",
    "to_node": "symbol:src/flask/app.py:Flask.log_exception:950",
    "evidence": {
      "line": 940,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_http_exception:830:symbol:src/flask/app.py:Flask.ensure_sync:1065:863",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.handle_http_exception:830",
    "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
    "evidence": {
      "line": 863,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_user_exception:865:symbol:src/flask/app.py:Flask.ensure_sync:1065:895",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.handle_user_exception:865",
    "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
    "evidence": {
      "line": 895,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_user_exception:865:symbol:src/flask/app.py:Flask.handle_http_exception:830:888",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.handle_user_exception:865",
    "to_node": "symbol:src/flask/app.py:Flask.handle_http_exception:830",
    "evidence": {
      "line": 888,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.preprocess_request:1366:symbol:src/flask/app.py:Flask.ensure_sync:1065:1387",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.preprocess_request:1366",
    "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
    "evidence": {
      "line": 1387,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.process_response:1394:symbol:src/flask/app.py:Flask.ensure_sync:1065:1408",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.process_response:1394",
    "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
    "evidence": {
      "line": 1408,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.process_response:1394:symbol:src/flask/app.py:Flask.ensure_sync:1065:1413",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.process_response:1394",
    "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
    "evidence": {
      "line": 1413,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.send_static_file:392:symbol:src/flask/app.py:Flask.get_send_file_max_age:365:409",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.send_static_file:392",
    "to_node": "symbol:src/flask/app.py:Flask.get_send_file_max_age:365",
    "evidence": {
      "line": 409,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.test_request_context:1517:symbol:src/flask/app.py:Flask.request_context:1501:1564",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.test_request_context:1517",
    "to_node": "symbol:src/flask/app.py:Flask.request_context:1501",
    "evidence": {
      "line": 1564,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.update_template_context:590:symbol:src/flask/app.py:Flask.ensure_sync:1065:616",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.update_template_context:590",
    "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
    "evidence": {
      "line": 616,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.url_for:1102:symbol:src/flask/app.py:Flask.create_url_adapter:509:1182",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.url_for:1102",
    "to_node": "symbol:src/flask/app.py:Flask.create_url_adapter:509",
    "evidence": {
      "line": 1182,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.wsgi_app:1566:symbol:src/flask/app.py:Flask.full_dispatch_request:992:1597",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.wsgi_app:1566",
    "to_node": "symbol:src/flask/app.py:Flask.full_dispatch_request:992",
    "evidence": {
      "line": 1597,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.wsgi_app:1566:symbol:src/flask/app.py:Flask.handle_exception:897:1600",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.wsgi_app:1566",
    "to_node": "symbol:src/flask/app.py:Flask.handle_exception:897",
    "evidence": {
      "line": 1600,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/app.py:Flask.wsgi_app:1566:symbol:src/flask/app.py:Flask.request_context:1501:1592",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/app.py:Flask.wsgi_app:1566",
    "to_node": "symbol:src/flask/app.py:Flask.request_context:1501",
    "evidence": {
      "line": 1592,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:AppGroup.command:413:symbol:src/flask/cli.py:AppGroup.command:413:425",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:AppGroup.command:413",
    "to_node": "symbol:src/flask/cli.py:AppGroup.command:413",
    "evidence": {
      "line": 425,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:AppGroup.command:413:symbol:src/flask/cli.py:with_appcontext:380:424",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:AppGroup.command:413",
    "to_node": "symbol:src/flask/cli.py:with_appcontext:380",
    "evidence": {
      "line": 424,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:AppGroup.group:429:symbol:src/flask/cli.py:AppGroup.group:429:437",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:AppGroup.group:429",
    "to_node": "symbol:src/flask/cli.py:AppGroup.group:429",
    "evidence": {
      "line": 437,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.get_command:609:symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600:610",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:FlaskGroup.get_command:609",
    "to_node": "symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600",
    "evidence": {
      "line": 610,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.get_command:609:symbol:src/flask/cli.py:FlaskGroup.get_command:609:613",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:FlaskGroup.get_command:609",
    "to_node": "symbol:src/flask/cli.py:FlaskGroup.get_command:609",
    "evidence": {
      "line": 613,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.get_command:609:symbol:src/flask/cli.py:FlaskGroup.get_command:609:634",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:FlaskGroup.get_command:609",
    "to_node": "symbol:src/flask/cli.py:FlaskGroup.get_command:609",
    "evidence": {
      "line": 634,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.get_command:609:symbol:src/flask/cli.py:ScriptInfo.load_app:333:623",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:FlaskGroup.get_command:609",
    "to_node": "symbol:src/flask/cli.py:ScriptInfo.load_app:333",
    "evidence": {
      "line": 623,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600:637",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636",
    "to_node": "symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600",
    "evidence": {
      "line": 637,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:639",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636",
    "to_node": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636",
    "evidence": {
      "line": 639,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:645",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636",
    "to_node": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636",
    "evidence": {
      "line": 645,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:symbol:src/flask/cli.py:ScriptInfo.load_app:333:645",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636",
    "to_node": "symbol:src/flask/cli.py:ScriptInfo.load_app:333",
    "evidence": {
      "line": 645,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.make_context:657:symbol:src/flask/cli.py:FlaskGroup.make_context:657:676",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:FlaskGroup.make_context:657",
    "to_node": "symbol:src/flask/cli.py:FlaskGroup.make_context:657",
    "evidence": {
      "line": 676,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.make_context:657:symbol:src/flask/cli.py:ScriptInfo:293:670",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:FlaskGroup.make_context:657",
    "to_node": "symbol:src/flask/cli.py:ScriptInfo:293",
    "evidence": {
      "line": 670,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.parse_args:678:symbol:src/flask/cli.py:FlaskGroup.parse_args:678:688",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:FlaskGroup.parse_args:678",
    "to_node": "symbol:src/flask/cli.py:FlaskGroup.parse_args:678",
    "evidence": {
      "line": 688,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:ScriptInfo.load_app:333:symbol:src/flask/cli.py:NoAppException:37:359",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:ScriptInfo.load_app:333",
    "to_node": "symbol:src/flask/cli.py:NoAppException:37",
    "evidence": {
      "line": 359,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:ScriptInfo.load_app:333:symbol:src/flask/cli.py:prepare_import:200:348",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:ScriptInfo.load_app:333",
    "to_node": "symbol:src/flask/cli.py:prepare_import:200",
    "evidence": {
      "line": 348,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:ScriptInfo.load_app:333:symbol:src/flask/cli.py:prepare_import:200:352",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:ScriptInfo.load_app:333",
    "to_node": "symbol:src/flask/cli.py:prepare_import:200",
    "evidence": {
      "line": 352,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:_env_file_callback:493:symbol:src/flask/cli.py:load_dotenv:698:510",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:_env_file_callback:493",
    "to_node": "symbol:src/flask/cli.py:load_dotenv:698",
    "evidence": {
      "line": 510,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:131",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:find_app_by_string:120",
    "to_node": "symbol:src/flask/cli.py:NoAppException:37",
    "evidence": {
      "line": 131,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:142",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:find_app_by_string:120",
    "to_node": "symbol:src/flask/cli.py:NoAppException:37",
    "evidence": {
      "line": 142,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:159",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:find_app_by_string:120",
    "to_node": "symbol:src/flask/cli.py:NoAppException:37",
    "evidence": {
      "line": 159,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:163",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:find_app_by_string:120",
    "to_node": "symbol:src/flask/cli.py:NoAppException:37",
    "evidence": {
      "line": 163,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:170",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:find_app_by_string:120",
    "to_node": "symbol:src/flask/cli.py:NoAppException:37",
    "evidence": {
      "line": 170,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:183",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:find_app_by_string:120",
    "to_node": "symbol:src/flask/cli.py:NoAppException:37",
    "evidence": {
      "line": 183,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:194",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:find_app_by_string:120",
    "to_node": "symbol:src/flask/cli.py:NoAppException:37",
    "evidence": {
      "line": 194,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:_called_with_wrong_args:94:180",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:find_app_by_string:120",
    "to_node": "symbol:src/flask/cli.py:_called_with_wrong_args:94",
    "evidence": {
      "line": 180,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:find_best_app:41:symbol:src/flask/cli.py:NoAppException:37:60",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:find_best_app:41",
    "to_node": "symbol:src/flask/cli.py:NoAppException:37",
    "evidence": {
      "line": 60,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:find_best_app:41:symbol:src/flask/cli.py:NoAppException:37:80",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:find_best_app:41",
    "to_node": "symbol:src/flask/cli.py:NoAppException:37",
    "evidence": {
      "line": 80,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:find_best_app:41:symbol:src/flask/cli.py:NoAppException:37:87",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:find_best_app:41",
    "to_node": "symbol:src/flask/cli.py:NoAppException:37",
    "evidence": {
      "line": 87,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:find_best_app:41:symbol:src/flask/cli.py:_called_with_wrong_args:94:77",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:find_best_app:41",
    "to_node": "symbol:src/flask/cli.py:_called_with_wrong_args:94",
    "evidence": {
      "line": 77,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:main:1122:symbol:src/flask/cli.py:main:1122:1123",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:main:1122",
    "to_node": "symbol:src/flask/cli.py:main:1122",
    "evidence": {
      "line": 1123,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:routes_command:1061:symbol:src/flask/cli.py:AppGroup.command:413:1048",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:routes_command:1061",
    "to_node": "symbol:src/flask/cli.py:AppGroup.command:413",
    "evidence": {
      "line": 1048,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:AppGroup.command:413:882",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:run_command:935",
    "to_node": "symbol:src/flask/cli.py:AppGroup.command:413",
    "evidence": {
      "line": 882,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:CertParamType:780:887",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:run_command:935",
    "to_node": "symbol:src/flask/cli.py:CertParamType:780",
    "evidence": {
      "line": 887,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:ScriptInfo.load_app:333:955",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:run_command:935",
    "to_node": "symbol:src/flask/cli.py:ScriptInfo.load_app:333",
    "evidence": {
      "line": 955,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:SeparatedPathType:867:918",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:run_command:935",
    "to_node": "symbol:src/flask/cli.py:SeparatedPathType:867",
    "evidence": {
      "line": 918,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:SeparatedPathType:867:927",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:run_command:935",
    "to_node": "symbol:src/flask/cli.py:SeparatedPathType:867",
    "evidence": {
      "line": 927,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:show_server_banner:766:981",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:run_command:935",
    "to_node": "symbol:src/flask/cli.py:show_server_banner:766",
    "evidence": {
      "line": 981,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:shell_command:1001:symbol:src/flask/cli.py:AppGroup.command:413:999",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:shell_command:1001",
    "to_node": "symbol:src/flask/cli.py:AppGroup.command:413",
    "evidence": {
      "line": 999,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/cli.py:with_appcontext:380:symbol:src/flask/cli.py:ScriptInfo.load_app:333:397",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/cli.py:with_appcontext:380",
    "to_node": "symbol:src/flask/cli.py:ScriptInfo.load_app:333",
    "evidence": {
      "line": 397,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/ctx.py:AppContext.__enter__:506:symbol:src/flask/ctx.py:AppContext.push:416:507",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/ctx.py:AppContext.__enter__:506",
    "to_node": "symbol:src/flask/ctx.py:AppContext.push:416",
    "evidence": {
      "line": 507,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/ctx.py:AppContext.push:416:symbol:src/flask/ctx.py:AppContext._get_session:381:439",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/ctx.py:AppContext.push:416",
    "to_node": "symbol:src/flask/ctx.py:AppContext._get_session:381",
    "evidence": {
      "line": 439,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/ctx.py:AppContext.push:416:symbol:src/flask/ctx.py:AppContext.match_request:405:444",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/ctx.py:AppContext.push:416",
    "to_node": "symbol:src/flask/ctx.py:AppContext.match_request:405",
    "evidence": {
      "line": 444,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/ctx.py:AppContext.session:396:symbol:src/flask/ctx.py:AppContext._get_session:381:401",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/ctx.py:AppContext.session:396",
    "to_node": "symbol:src/flask/ctx.py:AppContext._get_session:381",
    "evidence": {
      "line": 401,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:77",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68",
    "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68",
    "evidence": {
      "line": 77,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93:symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93:103",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93",
    "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93",
    "evidence": {
      "line": 103,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/ctx.py:after_this_request:118:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:139",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/ctx.py:after_this_request:118",
    "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68",
    "evidence": {
      "line": 139,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/ctx.py:copy_current_request_context:154:symbol:src/flask/ctx.py:AppContext.copy:355:200",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/ctx.py:copy_current_request_context:154",
    "to_node": "symbol:src/flask/ctx.py:AppContext.copy:355",
    "evidence": {
      "line": 200,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/ctx.py:copy_current_request_context:154:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:192",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/ctx.py:copy_current_request_context:154",
    "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68",
    "evidence": {
      "line": 192,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/ctx.py:has_app_context:235:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:257",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/ctx.py:has_app_context:235",
    "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68",
    "evidence": {
      "line": 257,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:src/flask/ctx.py:has_request_context:209:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:232",
    "edge_type": "calls",
    "from_node": "symbol:src/flask/ctx.py:has_request_context:209",
    "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68",
    "evidence": {
      "line": 232,
      "rel": "ast_call"
    }
  }
]

## Automated MCP Drill-Down Results
{
  "task_id": "flask-tf2-001",
  "repo_dir": "flask",
  "operation_family": "OF2",
  "confidence_overall": 0.487395,
  "lookup_hint": "expanded_lookup",
  "projected_nodes": 68,
  "actions_executed": 15,
  "budget": {
    "budget_exhausted": true,
    "operation_family": "OF2",
    "calls_made": 15,
    "budget": 15,
    "remaining": 0,
    "unresolved_nodes": []
  },
  "tokens": {
    "clue": 32923,
    "drill_down": 44139,
    "total": 77062,
    "raw_estimate": 143132
  },
  "etrr": 0.4616,
  "h7_pass": false,
  "tool_results": [
    {
      "tool": "resolve_dependency",
      "args": {
        "node_id": "module:src/flask/app.py",
        "depth": 2
      },
      "node_id": "module:src/flask/app.py",
      "confidence_trigger": 0.85,
      "output_size_tokens": 12938,
      "result": {
        "status": "ok",
        "seed_node": "module:src/flask/app.py",
        "depth": 2,
        "nodes": [
          {
            "node_id": "module:src/flask/app.py",
            "node_type": "module",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 0,
              "byte_end": 65423,
              "ast_path": "module",
              "content_hash": "09a3a1a7b3d1f174a4d274da2c329f9377745bbf6f138b17c3187352f7466a15"
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
              "symbol_name": "src/flask/app.py",
              "symbol_type": "module",
              "tier": 1
            },
            "confidence": 1.0
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.__call__:1618",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 65068,
              "byte_end": 65422,
              "ast_path": "function:Flask.__call__",
              "content_hash": "16b710f47ea72347274ceccb21649a5a4ce7b9a941c1d69f39a6109c157cec97"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.wsgi_app:1566"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function __call__",
              "symbol_name": "__call__",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.__init__:310",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 12632,
              "byte_end": 15001,
              "ast_path": "function:Flask.__init__",
              "content_hash": "57da7ea2afea8f19b08c324002385c3be9baf0c6407c163a9e8049ec5a9c849b"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/app.py:Flask.__init__:310"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.__init__:310"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.send_static_file:392"
                }
              ],
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
            "node_id": "symbol:src/flask/app.py:Flask.__init_subclass__:254",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 10298,
              "byte_end": 12626,
              "ast_path": "function:Flask.__init_subclass__",
              "content_hash": "3b2870215f971ca43d2861a3add34b60453e15b3bc67e6dfd92c08468e07e45b"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:add_ctx:97"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:remove_ctx:85"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function __init_subclass__",
              "symbol_name": "__init_subclass__",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.app_context:1481",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 59709,
              "byte_end": 60338,
              "ast_path": "function:Flask.app_context",
              "content_hash": "79d5270e83d82ae8f1961f84747c190d1a8f7f26b23a208785a878e44c25d353"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function app_context",
              "symbol_name": "app_context",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.async_to_sync:1079",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 43264,
              "byte_end": 44006,
              "ast_path": "function:Flask.async_to_sync",
              "content_hash": "84cc58adce4ab6990926b0445c184ef72fce3510204e177b41ccedb54327dedd"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function async_to_sync",
              "symbol_name": "async_to_sync",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.create_jinja_environment:469",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 18905,
              "byte_end": 20369,
              "ast_path": "function:Flask.create_jinja_environment",
              "content_hash": "6dae4fe790863807b4e096b5fecc5f6fa14099c229951e2b5b5f80820d878f2e"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function create_jinja_environment",
              "symbol_name": "create_jinja_environment",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.create_url_adapter:509",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 20375,
              "byte_end": 22649,
              "ast_path": "function:Flask.create_url_adapter",
              "content_hash": "326d82d2151f3a5db94d71701a097b93b1d963ff195012f28cc5d5aff7af34f3"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/app.py:Flask.url_for:1102"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function create_url_adapter",
              "symbol_name": "create_url_adapter",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.dispatch_request:966",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 38725,
              "byte_end": 39969,
              "ast_path": "function:Flask.dispatch_request",
              "content_hash": "f9c7ebf70a162afaa3e706b8d4162e9ff9869b62736df8d163e83a5a97c1ba09"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/app.py:Flask.full_dispatch_request:992"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.make_default_options_response:1053"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.raise_routing_exception:562"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function dispatch_request",
              "symbol_name": "dispatch_request",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.do_teardown_appcontext:1453",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 58699,
              "byte_end": 59703,
              "ast_path": "function:Flask.do_teardown_appcontext",
              "content_hash": "3c740347ee3ada59e3e126a5b9beaaaf97d94d1de8659072b69064bfd2c290e2"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function do_teardown_appcontext",
              "symbol_name": "do_teardown_appcontext",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.do_teardown_request:1420",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 57361,
              "byte_end": 58693,
              "ast_path": "function:Flask.do_teardown_request",
              "content_hash": "041737b4aa090af7eab203e32f8e5fea50ecb08f85041dd094e4f55928e97951"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function do_teardown_request",
              "symbol_name": "do_teardown_request",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 42765,
              "byte_end": 43258,
              "ast_path": "function:Flask.ensure_sync",
              "content_hash": "6b2a9bda8dd8e46b5098a7f3d631a7cfeda476f534749cb1101e21b18705a1ae"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/app.py:Flask.dispatch_request:966"
                },
                {
                  "source": "symbol:src/flask/app.py:Flask.do_teardown_appcontext:1453"
                },
                {
                  "source": "symbol:src/flask/app.py:Flask.do_teardown_request:1420"
                },
                {
                  "source": "symbol:src/flask/app.py:Flask.handle_exception:897"
                },
                {
                  "source": "symbol:src/flask/app.py:Flask.handle_http_exception:830"
                },
                {
                  "source": "symbol:src/flask/app.py:Flask.handle_user_exception:865"
                },
                {
                  "source": "symbol:src/flask/app.py:Flask.preprocess_request:1366"
                },
                {
                  "source": "symbol:src/flask/app.py:Flask.process_response:1394"
                },
                {
                  "source": "symbol:src/flask/app.py:Flask.update_template_context:590"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.async_to_sync:1079"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function ensure_sync",
              "symbol_name": "ensure_sync",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.finalize_request:1021",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 41065,
              "byte_end": 42285,
              "ast_path": "function:Flask.finalize_request",
              "content_hash": "7a66de46aa56116313f6ecb33949c6c7b43a88eec316c09a9a052b2cb946c9ca"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/app.py:Flask.full_dispatch_request:992"
                },
                {
                  "source": "symbol:src/flask/app.py:Flask.handle_exception:897"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.make_response:1224"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.process_response:1394"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function finalize_request",
              "symbol_name": "finalize_request",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.full_dispatch_request:992",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 40006,
              "byte_end": 41059,
              "ast_path": "function:Flask.full_dispatch_request",
              "content_hash": "8e19522cc1da2b297a32103626a277c3fc185dcd358b57b6df698d2caf911b62"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/app.py:Flask.wsgi_app:1566"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.dispatch_request:966"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.finalize_request:1021"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.handle_user_exception:865"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.preprocess_request:1366"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function full_dispatch_request",
              "symbol_name": "full_dispatch_request",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.get_send_file_max_age:365",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 15007,
              "byte_end": 15930,
              "ast_path": "function:Flask.get_send_file_max_age",
              "content_hash": "01c9df7cbf2b57c53a553c81d0eebfc02ea31dd964b0ddb5e21178af8b70ed59"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/app.py:Flask.send_static_file:392"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function get_send_file_max_age",
              "symbol_name": "get_send_file_max_age",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.handle_exception:897",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 35936,
              "byte_end": 38144,
              "ast_path": "function:Flask.handle_exception",
              "content_hash": "94fa1a557d158357fa24901a30ed508910248cbd59a954626e771aa0c02f4b6b"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/app.py:Flask.wsgi_app:1566"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.finalize_request:1021"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.log_exception:950"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function handle_exception",
              "symbol_name": "handle_exception",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.handle_http_exception:830",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 33366,
              "byte_end": 34696,
              "ast_path": "function:Flask.handle_http_exception",
              "content_hash": "54f2cc1a7277891f9984d463c16bda67f3a49ccdd57ec93838af07a21370ddd5"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/app.py:Flask.handle_user_exception:865"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function handle_http_exception",
              "symbol_name": "handle_http_exception",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.handle_user_exception:865",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 34733,
              "byte_end": 35899,
              "ast_path": "function:Flask.handle_user_exception",
              "content_hash": "65f0f36c19963deafce37ba086efdf0079617dbcc34a99773cb839e4f2a3f42c"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/app.py:Flask.full_dispatch_request:992"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.handle_http_exception:830"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function handle_user_exception",
              "symbol_name": "handle_user_exception",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.log_exception:950",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 38150,
              "byte_end": 38719,
              "ast_path": "function:Flask.log_exception",
              "content_hash": "5c6d1f2f1c4c9778085f6ed59c1feba42b243771987ea7552ad00c4aff079b15"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/app.py:Flask.handle_exception:897"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function log_exception",
              "symbol_name": "log_exception",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.make_default_options_response:1053",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 42291,
              "byte_end": 42759,
              "ast_path": "function:Flask.make_default_options_response",
              "content_hash": "8a2f74eb652357b7559bdbb7f084cc51905249d5b85e3e9d9198b941e35d972c"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/app.py:Flask.dispatch_request:966"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function make_default_options_response",
              "symbol_name": "make_default_options_response",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.make_response:1224",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 49141,
              "byte_end": 55019,
              "ast_path": "function:Flask.make_response",
              "content_hash": "0d06b529b46e02f98ab2983ee4c22e3ec5ad669894e21669c941ba539f4a86d5"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/app.py:Flask.finalize_request:1021"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function make_response",
              "symbol_name": "make_response",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.make_shell_context:620",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 24901,
              "byte_end": 25294,
              "ast_path": "function:Flask.make_shell_context",
              "content_hash": "9a86aa861f236d80193637119f2829f7dcc61a2334347f410bf897e521b1ef8d"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function make_shell_context",
              "symbol_name": "make_shell_context",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.open_instance_resource:447",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 18031,
              "byte_end": 18899,
              "ast_path": "function:Flask.open_instance_resource",
              "content_hash": "bea7f186606ed1df22c9c1aa0b816a537a8ef7797c458339ffcc6fc067b67e1f"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function open_instance_resource",
              "symbol_name": "open_instance_resource",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.open_resource:414",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 16788,
              "byte_end": 18025,
              "ast_path": "function:Flask.open_resource",
              "content_hash": "2a30c20654894ab06599f496de7b66a03367515734e1bc09dbdb6b48d0db1377"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function open_resource",
              "symbol_name": "open_resource",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.preprocess_request:1366",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 55025,
              "byte_end": 56181,
              "ast_path": "function:Flask.preprocess_request",
              "content_hash": "e8241727e4adceb04aa62dcb3ba158f8fcade2feeb35cf6de5cfa4c2cab2867d"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/app.py:Flask.full_dispatch_request:992"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function preprocess_request",
              "symbol_name": "preprocess_request",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.process_response:1394",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 56187,
              "byte_end": 57355,
              "ast_path": "function:Flask.process_response",
              "content_hash": "01df3451a006199a5f04d18eab36b8bca8732d704c72fa60153e37a928bdb205"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/app.py:Flask.finalize_request:1021"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function process_response",
              "symbol_name": "process_response",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.raise_routing_exception:562",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 22655,
              "byte_end": 23625,
              "ast_path": "function:Flask.raise_routing_exception",
              "content_hash": "295ced4ad7dbf6e1f2e2ea95eebe4e5ab8d210f48fca8c2df8e994083551724e"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/app.py:Flask.dispatch_request:966"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function raise_routing_exception",
              "symbol_name": "raise_routing_exception",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.request_context:1501",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 60344,
              "byte_end": 61083,
              "ast_path": "function:Flask.request_context",
              "content_hash": "d233642d6405c7af5388bff1ffaeef51efc5feba7d33df39011b66e753588748"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/app.py:Flask.test_request_context:1517"
                },
                {
                  "source": "symbol:src/flask/app.py:Flask.wsgi_app:1566"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function request_context",
              "symbol_name": "request_context",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.run:632",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 25300,
              "byte_end": 30275,
              "ast_path": "function:Flask.run",
              "content_hash": "1d124b55d3a0a1775572e7953a0252e88e537e4c2f20d4a076cc91196620465a"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function run",
              "symbol_name": "run",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.send_static_file:392",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 15967,
              "byte_end": 16782,
              "ast_path": "function:Flask.send_static_file",
              "content_hash": "27d2683e2746c869cb91807722d38ff946b71fa05f1a5f77b3bb6267d77abb71"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/app.py:Flask.__init__:310"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.get_send_file_max_age:365"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function send_static_file",
              "symbol_name": "send_static_file",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.test_cli_runner:813",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 32810,
              "byte_end": 33344,
              "ast_path": "function:Flask.test_cli_runner",
              "content_hash": "872e7fb833f86ac31b992b47ea40964af22f875fe305eafa40a0810ca269cc7e"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function test_cli_runner",
              "symbol_name": "test_cli_runner",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.test_client:755",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 30281,
              "byte_end": 32804,
              "ast_path": "function:Flask.test_client",
              "content_hash": "caf08057437c0febbbf6485b2fe142d4616a223a7dd01fd8ca446c0da9ed04a9"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function test_client",
              "symbol_name": "test_client",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.test_request_context:1517",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 61089,
              "byte_end": 63177,
              "ast_path": "function:Flask.test_request_context",
              "content_hash": "01b99fd691fc355b938491b41a842566d73cfbe0d595bf74ca24097081c3a556"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.request_context:1501"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function test_request_context",
              "symbol_name": "test_request_context",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.update_template_context:590",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 23631,
              "byte_end": 24895,
              "ast_path": "function:Flask.update_template_context",
              "content_hash": "9605416d8b7e0803328f2aec29c5e5e0964d3eb5c6e6325a767176ee0456d857"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.ensure_sync:1065"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function update_template_context",
              "symbol_name": "update_template_context",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.url_for:1102",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 44012,
              "byte_end": 49135,
              "ast_path": "function:Flask.url_for",
              "content_hash": "b476a0dec4c79242e60a8469e83a4cb44b4645c44efe3fd67672d4284fe3239b"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.create_url_adapter:509"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function url_for",
              "symbol_name": "url_for",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask.wsgi_app:1566",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 63183,
              "byte_end": 65062,
              "ast_path": "function:Flask.wsgi_app",
              "content_hash": "efd78a36ec1d79465da93b82553ebef531fd2c598cdd1231b32ebc959f3463e9"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/app.py:Flask.__call__:1618"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.full_dispatch_request:992"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.handle_exception:897"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/app.py:Flask.request_context:1501"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function wsgi_app",
              "symbol_name": "wsgi_app",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:Flask:109",
            "node_type": "class",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 3608,
              "byte_end": 65422,
              "ast_path": "class:Flask",
              "content_hash": "5b9e20d673e16d2455888c112e8011200712200f3012b2dad645aeaf4bb6323f"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "class Flask",
              "symbol_name": "Flask",
              "symbol_type": "class",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:_make_timedelta:73",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 2455,
              "byte_end": 2638,
              "ast_path": "function:_make_timedelta",
              "content_hash": "dba2002505bcb415b6d2206f8aaa65eed7ae8eded71c2948464686fb866e15ce"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _make_timedelta",
              "symbol_name": "_make_timedelta",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:add_ctx.wrapper:98",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 3249,
              "byte_end": 3536,
              "ast_path": "function:add_ctx.wrapper",
              "content_hash": "8490871f452d41a8b340139b0e72ad487f11609d371eec25640f46f42ab726f5"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function wrapper",
              "symbol_name": "wrapper",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:add_ctx:97",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 3221,
              "byte_end": 3575,
              "ast_path": "function:add_ctx",
              "content_hash": "6d3df893048dde40a2e8d8ecda5c256d98b3f17c369b01fa7dffafe617fdc8ec"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/app.py:Flask.__init_subclass__:254"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function add_ctx",
              "symbol_name": "add_ctx",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:remove_ctx.wrapper:86",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 2849,
              "byte_end": 3036,
              "ast_path": "function:remove_ctx.wrapper",
              "content_hash": "79d5b98d3eefca83838547a158e0d2db2e99c361b8abe1e20623905428997424"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function wrapper",
              "symbol_name": "wrapper",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/app.py:remove_ctx:85",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/app.py",
              "byte_start": 2818,
              "byte_end": 3075,
              "ast_path": "function:remove_ctx",
              "content_hash": "5c58ac17b76b3fb185090bf51555c9b39cbb0342f9bf535151347fe2f1826071"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/app.py:Flask.__init_subclass__:254"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function remove_ctx",
              "symbol_name": "remove_ctx",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          }
        ],
        "edges": [
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.__call__:1618:symbol:src/flask/app.py:Flask.wsgi_app:1566:1625",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.__call__:1618",
            "to_node": "symbol:src/flask/app.py:Flask.wsgi_app:1566",
            "evidence": {
              "line": 1625,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.__init__:310:symbol:src/flask/app.py:Flask.__init__:310:323",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.__init__:310",
            "to_node": "symbol:src/flask/app.py:Flask.__init__:310",
            "evidence": {
              "line": 323,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.__init__:310:symbol:src/flask/app.py:Flask.send_static_file:392:362",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.__init__:310",
            "to_node": "symbol:src/flask/app.py:Flask.send_static_file:392",
            "evidence": {
              "line": 362,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.__init_subclass__:254:symbol:src/flask/app.py:add_ctx:97:308",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.__init_subclass__:254",
            "to_node": "symbol:src/flask/app.py:add_ctx:97",
            "evidence": {
              "line": 308,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.__init_subclass__:254:symbol:src/flask/app.py:remove_ctx:85:307",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.__init_subclass__:254",
            "to_node": "symbol:src/flask/app.py:remove_ctx:85",
            "evidence": {
              "line": 307,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.dispatch_request:966:symbol:src/flask/app.py:Flask.ensure_sync:1065:990",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.dispatch_request:966",
            "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
            "evidence": {
              "line": 990,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.dispatch_request:966:symbol:src/flask/app.py:Flask.make_default_options_response:1053:987",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.dispatch_request:966",
            "to_node": "symbol:src/flask/app.py:Flask.make_default_options_response:1053",
            "evidence": {
              "line": 987,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.dispatch_request:966:symbol:src/flask/app.py:Flask.raise_routing_exception:562:979",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.dispatch_request:966",
            "to_node": "symbol:src/flask/app.py:Flask.raise_routing_exception:562",
            "evidence": {
              "line": 979,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.do_teardown_appcontext:1453:symbol:src/flask/app.py:Flask.ensure_sync:1065:1474",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.do_teardown_appcontext:1453",
            "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
            "evidence": {
              "line": 1474,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.do_teardown_request:1420:symbol:src/flask/app.py:Flask.ensure_sync:1065:1446",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.do_teardown_request:1420",
            "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
            "evidence": {
              "line": 1446,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.ensure_sync:1065:symbol:src/flask/app.py:Flask.async_to_sync:1079:1075",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
            "to_node": "symbol:src/flask/app.py:Flask.async_to_sync:1079",
            "evidence": {
              "line": 1075,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.finalize_request:1021:symbol:src/flask/app.py:Flask.make_response:1224:1039",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.finalize_request:1021",
            "to_node": "symbol:src/flask/app.py:Flask.make_response:1224",
            "evidence": {
              "line": 1039,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.finalize_request:1021:symbol:src/flask/app.py:Flask.process_response:1394:1041",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.finalize_request:1021",
            "to_node": "symbol:src/flask/app.py:Flask.process_response:1394",
            "evidence": {
              "line": 1041,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.full_dispatch_request:992:symbol:src/flask/app.py:Flask.dispatch_request:966:1016",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.full_dispatch_request:992",
            "to_node": "symbol:src/flask/app.py:Flask.dispatch_request:966",
            "evidence": {
              "line": 1016,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.full_dispatch_request:992:symbol:src/flask/app.py:Flask.finalize_request:1021:1019",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.full_dispatch_request:992",
            "to_node": "symbol:src/flask/app.py:Flask.finalize_request:1021",
            "evidence": {
              "line": 1019,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.full_dispatch_request:992:symbol:src/flask/app.py:Flask.handle_user_exception:865:1018",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.full_dispatch_request:992",
            "to_node": "symbol:src/flask/app.py:Flask.handle_user_exception:865",
            "evidence": {
              "line": 1018,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.full_dispatch_request:992:symbol:src/flask/app.py:Flask.preprocess_request:1366:1014",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.full_dispatch_request:992",
            "to_node": "symbol:src/flask/app.py:Flask.preprocess_request:1366",
            "evidence": {
              "line": 1014,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_exception:897:symbol:src/flask/app.py:Flask.ensure_sync:1065:946",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.handle_exception:897",
            "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
            "evidence": {
              "line": 946,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_exception:897:symbol:src/flask/app.py:Flask.finalize_request:1021:948",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.handle_exception:897",
            "to_node": "symbol:src/flask/app.py:Flask.finalize_request:1021",
            "evidence": {
              "line": 948,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_exception:897:symbol:src/flask/app.py:Flask.log_exception:950:940",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.handle_exception:897",
            "to_node": "symbol:src/flask/app.py:Flask.log_exception:950",
            "evidence": {
              "line": 940,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_http_exception:830:symbol:src/flask/app.py:Flask.ensure_sync:1065:863",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.handle_http_exception:830",
            "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
            "evidence": {
              "line": 863,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_user_exception:865:symbol:src/flask/app.py:Flask.ensure_sync:1065:895",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.handle_user_exception:865",
            "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
            "evidence": {
              "line": 895,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.handle_user_exception:865:symbol:src/flask/app.py:Flask.handle_http_exception:830:888",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.handle_user_exception:865",
            "to_node": "symbol:src/flask/app.py:Flask.handle_http_exception:830",
            "evidence": {
              "line": 888,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.preprocess_request:1366:symbol:src/flask/app.py:Flask.ensure_sync:1065:1387",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.preprocess_request:1366",
            "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
            "evidence": {
              "line": 1387,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.process_response:1394:symbol:src/flask/app.py:Flask.ensure_sync:1065:1408",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.process_response:1394",
            "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
            "evidence": {
              "line": 1408,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.process_response:1394:symbol:src/flask/app.py:Flask.ensure_sync:1065:1413",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.process_response:1394",
            "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
            "evidence": {
              "line": 1413,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.send_static_file:392:symbol:src/flask/app.py:Flask.get_send_file_max_age:365:409",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.send_static_file:392",
            "to_node": "symbol:src/flask/app.py:Flask.get_send_file_max_age:365",
            "evidence": {
              "line": 409,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.test_request_context:1517:symbol:src/flask/app.py:Flask.request_context:1501:1564",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.test_request_context:1517",
            "to_node": "symbol:src/flask/app.py:Flask.request_context:1501",
            "evidence": {
              "line": 1564,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.update_template_context:590:symbol:src/flask/app.py:Flask.ensure_sync:1065:616",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.update_template_context:590",
            "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
            "evidence": {
              "line": 616,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.url_for:1102:symbol:src/flask/app.py:Flask.create_url_adapter:509:1182",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.url_for:1102",
            "to_node": "symbol:src/flask/app.py:Flask.create_url_adapter:509",
            "evidence": {
              "line": 1182,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.wsgi_app:1566:symbol:src/flask/app.py:Flask.full_dispatch_request:992:1597",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.wsgi_app:1566",
            "to_node": "symbol:src/flask/app.py:Flask.full_dispatch_request:992",
            "evidence": {
              "line": 1597,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.wsgi_app:1566:symbol:src/flask/app.py:Flask.handle_exception:897:1600",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.wsgi_app:1566",
            "to_node": "symbol:src/flask/app.py:Flask.handle_exception:897",
            "evidence": {
              "line": 1600,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/app.py:Flask.wsgi_app:1566:symbol:src/flask/app.py:Flask.request_context:1501:1592",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/app.py:Flask.wsgi_app:1566",
            "to_node": "symbol:src/flask/app.py:Flask.request_context:1501",
            "evidence": {
              "line": 1592,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.__call__:1618",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.__call__:1618",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.__init__:310",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.__init__:310",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.__init_subclass__:254",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.__init_subclass__:254",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.app_context:1481",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.app_context:1481",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.async_to_sync:1079",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.async_to_sync:1079",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.create_jinja_environment:469",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.create_jinja_environment:469",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.create_url_adapter:509",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.create_url_adapter:509",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.dispatch_request:966",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.dispatch_request:966",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.do_teardown_appcontext:1453",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.do_teardown_appcontext:1453",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.do_teardown_request:1420",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.do_teardown_request:1420",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.ensure_sync:1065",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.finalize_request:1021",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.finalize_request:1021",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.full_dispatch_request:992",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.full_dispatch_request:992",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.get_send_file_max_age:365",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.get_send_file_max_age:365",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.handle_exception:897",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.handle_exception:897",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.handle_http_exception:830",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.handle_http_exception:830",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.handle_user_exception:865",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.handle_user_exception:865",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.log_exception:950",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.log_exception:950",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.make_default_options_response:1053",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.make_default_options_response:1053",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.make_response:1224",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.make_response:1224",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.make_shell_context:620",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.make_shell_context:620",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.open_instance_resource:447",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.open_instance_resource:447",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.open_resource:414",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.open_resource:414",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.preprocess_request:1366",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.preprocess_request:1366",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.process_response:1394",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.process_response:1394",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.raise_routing_exception:562",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.raise_routing_exception:562",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.request_context:1501",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.request_context:1501",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.run:632",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.run:632",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.send_static_file:392",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.send_static_file:392",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.test_cli_runner:813",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.test_cli_runner:813",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.test_client:755",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.test_client:755",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.test_request_context:1517",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.test_request_context:1517",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.update_template_context:590",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.update_template_context:590",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.url_for:1102",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.url_for:1102",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask.wsgi_app:1566",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask.wsgi_app:1566",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:Flask:109",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:Flask:109",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:_make_timedelta:73",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:_make_timedelta:73",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:add_ctx.wrapper:98",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:add_ctx.wrapper:98",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:add_ctx:97",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:add_ctx:97",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:remove_ctx.wrapper:86",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:remove_ctx.wrapper:86",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/app.py:symbol:src/flask/app.py:remove_ctx:85",
            "edge_type": "contains",
            "from_node": "module:src/flask/app.py",
            "to_node": "symbol:src/flask/app.py:remove_ctx:85",
            "evidence": {
              "rel": "ast_containment"
            }
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "src/flask/app.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "module:src/flask/app.py",
      "confidence_trigger": 0.85,
      "output_size_tokens": 880,
      "result": {
        "status": "ok",
        "file_path": "src/flask/app.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 1536,
        "lines": [
          {
            "line_number": 1,
            "content": "from __future__ import annotations"
          },
          {
            "line_number": 2,
            "content": ""
          },
          {
            "line_number": 3,
            "content": "import collections.abc as cabc"
          },
          {
            "line_number": 4,
            "content": "import os"
          },
          {
            "line_number": 5,
            "content": "import sys"
          },
          {
            "line_number": 6,
            "content": "import typing as t"
          },
          {
            "line_number": 7,
            "content": "import weakref"
          },
          {
            "line_number": 8,
            "content": "from datetime import timedelta"
          },
          {
            "line_number": 9,
            "content": "from inspect import iscoroutinefunction"
          },
          {
            "line_number": 10,
            "content": "from itertools import chain"
          },
          {
            "line_number": 11,
            "content": "from types import TracebackType"
          },
          {
            "line_number": 12,
            "content": "from urllib.parse import quote as _url_quote"
          },
          {
            "line_number": 13,
            "content": ""
          },
          {
            "line_number": 14,
            "content": "import click"
          },
          {
            "line_number": 15,
            "content": "from werkzeug.datastructures import Headers"
          },
          {
            "line_number": 16,
            "content": "from werkzeug.datastructures import ImmutableDict"
          },
          {
            "line_number": 17,
            "content": "from werkzeug.exceptions import BadRequestKeyError"
          },
          {
            "line_number": 18,
            "content": "from werkzeug.exceptions import HTTPException"
          },
          {
            "line_number": 19,
            "content": "from werkzeug.exceptions import InternalServerError"
          },
          {
            "line_number": 20,
            "content": "from werkzeug.routing import BuildError"
          },
          {
            "line_number": 21,
            "content": "from werkzeug.routing import MapAdapter"
          },
          {
            "line_number": 22,
            "content": "from werkzeug.routing import RequestRedirect"
          },
          {
            "line_number": 23,
            "content": "from werkzeug.routing import RoutingException"
          },
          {
            "line_number": 24,
            "content": "from werkzeug.routing import Rule"
          },
          {
            "line_number": 25,
            "content": "from werkzeug.serving import is_running_from_reloader"
          },
          {
            "line_number": 26,
            "content": "from werkzeug.wrappers import Response as BaseResponse"
          },
          {
            "line_number": 27,
            "content": "from werkzeug.wsgi import get_host"
          },
          {
            "line_number": 28,
            "content": ""
          },
          {
            "line_number": 29,
            "content": "from . import cli"
          },
          {
            "line_number": 30,
            "content": "from . import typing as ft"
          },
          {
            "line_number": 31,
            "content": "from .ctx import AppContext"
          },
          {
            "line_number": 32,
            "content": "from .ctx import RequestContext"
          },
          {
            "line_number": 33,
            "content": "from .globals import _cv_app"
          },
          {
            "line_number": 34,
            "content": "from .globals import _cv_request"
          },
          {
            "line_number": 35,
            "content": "from .globals import current_app"
          },
          {
            "line_number": 36,
            "content": "from .globals import g"
          },
          {
            "line_number": 37,
            "content": "from .globals import request"
          },
          {
            "line_number": 38,
            "content": "from .globals import request_ctx"
          },
          {
            "line_number": 39,
            "content": "from .globals import session"
          },
          {
            "line_number": 40,
            "content": "from .helpers import get_debug_flag"
          },
          {
            "line_number": 41,
            "content": "from .helpers import get_flashed_messages"
          },
          {
            "line_number": 42,
            "content": "from .helpers import get_load_dotenv"
          },
          {
            "line_number": 43,
            "content": "from .helpers import send_from_directory"
          },
          {
            "line_number": 44,
            "content": "from .sansio.app import App"
          },
          {
            "line_number": 45,
            "content": "from .sansio.scaffold import _sentinel"
          },
          {
            "line_number": 46,
            "content": "from .sessions import SecureCookieSessionInterface"
          },
          {
            "line_number": 47,
            "content": "from .sessions import SessionInterface"
          },
          {
            "line_number": 48,
            "content": "from .signals import appcontext_tearing_down"
          },
          {
            "line_number": 49,
            "content": "from .signals import got_request_exception"
          },
          {
            "line_number": 50,
            "content": "from .signals import request_finished"
          }
        ]
      }
    },
    {
      "tool": "resolve_dependency",
      "args": {
        "node_id": "module:src/flask/cli.py",
        "depth": 2
      },
      "node_id": "module:src/flask/cli.py",
      "confidence_trigger": 0.85,
      "output_size_tokens": 13028,
      "result": {
        "status": "ok",
        "seed_node": "module:src/flask/cli.py",
        "depth": 2,
        "nodes": [
          {
            "node_id": "module:src/flask/cli.py",
            "node_type": "module",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 0,
              "byte_end": 36808,
              "ast_path": "module",
              "content_hash": "1f2e6624f5a34c86eb0e1928c6acb6b85297b19be0e039791bf0c065d2b2b7af"
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
              "symbol_name": "src/flask/cli.py",
              "symbol_type": "module",
              "tier": 1
            },
            "confidence": 1.0
          },
          {
            "node_id": "symbol:src/flask/cli.py:AppGroup.command.decorator:422",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 13507,
              "byte_end": 13702,
              "ast_path": "function:AppGroup.command.decorator",
              "content_hash": "2a648a7baf29f3f9e3faff7dfb33cacc3e24bd00d30025e4bc89cf3d4fcace41"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function decorator",
              "symbol_name": "decorator",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:AppGroup.command:413",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 13060,
              "byte_end": 13759,
              "ast_path": "function:AppGroup.command",
              "content_hash": "7cbc7fe2247437eb5981de5bc005d1176e0e2c707a67cff4b2d3fb18f6c1a623"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/cli.py:AppGroup.command:413"
                },
                {
                  "source": "symbol:src/flask/cli.py:routes_command:1061"
                },
                {
                  "source": "symbol:src/flask/cli.py:run_command:935"
                },
                {
                  "source": "symbol:src/flask/cli.py:shell_command:1001"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:AppGroup.command:413"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:with_appcontext:380"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function command",
              "symbol_name": "command",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:AppGroup.group:429",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 13765,
              "byte_end": 14173,
              "ast_path": "function:AppGroup.group",
              "content_hash": "56dfb90977bf75433236c3ba6b505a74d878e1c9585b2b5bec395a7e9b514a2d"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/cli.py:AppGroup.group:429"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:AppGroup.group:429"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function group",
              "symbol_name": "group",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:AppGroup:405",
            "node_type": "class",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 12759,
              "byte_end": 14173,
              "ast_path": "class:AppGroup",
              "content_hash": "eaff8e3673f6a3b31faf721803d7ff781b4d88e861280681cb2da5129ace792e"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "class AppGroup",
              "symbol_name": "AppGroup",
              "symbol_type": "class",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:CertParamType.__init__:788",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 26765,
              "byte_end": 26876,
              "ast_path": "function:CertParamType.__init__",
              "content_hash": "874e401fe3352bbd2d5107ed5a857130ab5fdace3d6d43efe32d90cb04c82c61"
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
            "node_id": "symbol:src/flask/cli.py:CertParamType.convert:791",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 26882,
              "byte_end": 27959,
              "ast_path": "function:CertParamType.convert",
              "content_hash": "95693e856885fa293d5940a2fe26acb18359fe7542006432e63fb5492e813d7a"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function convert",
              "symbol_name": "convert",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:CertParamType:780",
            "node_type": "class",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 26527,
              "byte_end": 27959,
              "ast_path": "class:CertParamType",
              "content_hash": "5a97b025ef493def3d3226a4bb2f57c50062059830724a3b0f77a82a5bc09db0"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/cli.py:run_command:935"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "class CertParamType",
              "symbol_name": "CertParamType",
              "symbol_type": "class",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:FlaskGroup.__init__:563",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 18694,
              "byte_end": 20005,
              "ast_path": "function:FlaskGroup.__init__",
              "content_hash": "0c5b08eea883aa0c3ab932c413dc6ca372374c2c74d698ca07927b1dcb18b01b"
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
            "node_id": "symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 20011,
              "byte_end": 20281,
              "ast_path": "function:FlaskGroup._load_plugin_commands",
              "content_hash": "e1a57664073884e8cf7c5c0237ee175695451f125ceaa7b6229d0e0daa044b68"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/cli.py:FlaskGroup.get_command:609"
                },
                {
                  "source": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _load_plugin_commands",
              "symbol_name": "_load_plugin_commands",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:FlaskGroup.get_command:609",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 20287,
              "byte_end": 21344,
              "ast_path": "function:FlaskGroup.get_command",
              "content_hash": "cfb4a2ed09a26b0a2b396dbc38117a618b47e6e26c2df25943bf4098c40e42d4"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/cli.py:FlaskGroup.get_command:609"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:FlaskGroup.get_command:609"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:ScriptInfo.load_app:333"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function get_command",
              "symbol_name": "get_command",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 21350,
              "byte_end": 22230,
              "ast_path": "function:FlaskGroup.list_commands",
              "content_hash": "db7aa35213f300bcbd95996c0762822d243516cc3715c21cd85a2dbe8f8a6b06"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:ScriptInfo.load_app:333"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function list_commands",
              "symbol_name": "list_commands",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:FlaskGroup.make_context:657",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 22236,
              "byte_end": 23032,
              "ast_path": "function:FlaskGroup.make_context",
              "content_hash": "d5fd541910368dc55fd8ad4dc200c23d2768876ebc1988b2a1ec121e23e2fd56"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/cli.py:FlaskGroup.make_context:657"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:FlaskGroup.make_context:657"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:ScriptInfo:293"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function make_context",
              "symbol_name": "make_context",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:FlaskGroup.parse_args:678",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 23038,
              "byte_end": 23595,
              "ast_path": "function:FlaskGroup.parse_args",
              "content_hash": "d6cefdc254f2eedcbf1b83d1708a912a67f3fe16092180cb1683cd729b27da8c"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/cli.py:FlaskGroup.parse_args:678"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:FlaskGroup.parse_args:678"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function parse_args",
              "symbol_name": "parse_args",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:FlaskGroup:531",
            "node_type": "class",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 17209,
              "byte_end": 23595,
              "ast_path": "class:FlaskGroup",
              "content_hash": "0772726b759c864442ae934b461980f9ec1c89e12e0e8f55818847234e1d9b0c"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "class FlaskGroup",
              "symbol_name": "FlaskGroup",
              "symbol_type": "class",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:NoAppException:37",
            "node_type": "class",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 793,
              "byte_end": 894,
              "ast_path": "class:NoAppException",
              "content_hash": "9e968dd91274d585a76dc0e384e22c73915368b63eb1b58c2d5b72290ac35a19"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/cli.py:ScriptInfo.load_app:333"
                },
                {
                  "source": "symbol:src/flask/cli.py:find_app_by_string:120"
                },
                {
                  "source": "symbol:src/flask/cli.py:find_best_app:41"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "class NoAppException",
              "symbol_name": "NoAppException",
              "symbol_type": "class",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:ScriptInfo.__init__:305",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 9148,
              "byte_end": 10197,
              "ast_path": "function:ScriptInfo.__init__",
              "content_hash": "3807ab1d4aacf63c711567d62a542e7a487a04a9bceb74570c4ae183787ea2cf"
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
            "node_id": "symbol:src/flask/cli.py:ScriptInfo.load_app:333",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 10203,
              "byte_end": 11724,
              "ast_path": "function:ScriptInfo.load_app",
              "content_hash": "fcc5e00092c0dcfde838fbfd79d5492ad1ce3415cd57f8c8c088308d920dffb6"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/cli.py:FlaskGroup.get_command:609"
                },
                {
                  "source": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636"
                },
                {
                  "source": "symbol:src/flask/cli.py:run_command:935"
                },
                {
                  "source": "symbol:src/flask/cli.py:with_appcontext:380"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:NoAppException:37"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:prepare_import:200"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function load_app",
              "symbol_name": "load_app",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:ScriptInfo:293",
            "node_type": "class",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 8628,
              "byte_end": 11724,
              "ast_path": "class:ScriptInfo",
              "content_hash": "592901e1d1006934831a264b7b30b61fb9fc1075d47bb685d40e4ef31e911431"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/cli.py:FlaskGroup.make_context:657"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "class ScriptInfo",
              "symbol_name": "ScriptInfo",
              "symbol_type": "class",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:SeparatedPathType.convert:873",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 29330,
              "byte_end": 29677,
              "ast_path": "function:SeparatedPathType.convert",
              "content_hash": "e089600edd6b348ea147d86902defc3da20324b7e2e86d3f7b4b54d5b0bf47dd"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function convert",
              "symbol_name": "convert",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:SeparatedPathType:867",
            "node_type": "class",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 29098,
              "byte_end": 29677,
              "ast_path": "class:SeparatedPathType",
              "content_hash": "4e7c63eca412e2011eb711ff409e2fd4fe283745f8dab01fd8475913b13cfe7c"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/cli.py:run_command:935"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "class SeparatedPathType",
              "symbol_name": "SeparatedPathType",
              "symbol_type": "class",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:_called_with_wrong_args:94",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 2679,
              "byte_end": 3426,
              "ast_path": "function:_called_with_wrong_args",
              "content_hash": "5152c1adb4a87c355e684d73ccffa080ae06f81d67a6749406bddc65dae81c69"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/cli.py:find_app_by_string:120"
                },
                {
                  "source": "symbol:src/flask/cli.py:find_best_app:41"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _called_with_wrong_args",
              "symbol_name": "_called_with_wrong_args",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:_env_file_callback:493",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 15909,
              "byte_end": 16666,
              "ast_path": "function:_env_file_callback",
              "content_hash": "ae6497dbece96def68c74d214584647fbd8ea5506ecca1e520ae0b70cf0e75a5"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:load_dotenv:698"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _env_file_callback",
              "symbol_name": "_env_file_callback",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:_path_is_ancestor:691",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 23598,
              "byte_end": 23894,
              "ast_path": "function:_path_is_ancestor",
              "content_hash": "8101ea9f91b2983c0b795e7a69294637a0b0fb7bb530ad02e3e1c2625e1ee9ab"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _path_is_ancestor",
              "symbol_name": "_path_is_ancestor",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:_set_app:440",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 14207,
              "byte_end": 14428,
              "ast_path": "function:_set_app",
              "content_hash": "0a52585948173cf5515f03ba10955b59a1bb61a99adcc7855a7e2c2488fc4b88"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _set_app",
              "symbol_name": "_set_app",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:_set_debug:468",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 15159,
              "byte_end": 15767,
              "ast_path": "function:_set_debug",
              "content_hash": "f1e2f14dae6a55eaabe1ac817b5a1574d9bf236df28a4e5c7b9ef4548df02354"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _set_debug",
              "symbol_name": "_set_debug",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:_validate_key:828",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 27962,
              "byte_end": 29095,
              "ast_path": "function:_validate_key",
              "content_hash": "026ef1238d4467168993e73a91861a7d9b34579cbe1428fa2427b7f10286541c"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _validate_key",
              "symbol_name": "_validate_key",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:find_app_by_string:120",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 3429,
              "byte_end": 6072,
              "ast_path": "function:find_app_by_string",
              "content_hash": "9bac2537de80d6198f90f5cb0db6004ffe1eb5ee047b1194b8b8e925bb41620b"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:NoAppException:37"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:_called_with_wrong_args:94"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function find_app_by_string",
              "symbol_name": "find_app_by_string",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:find_best_app:41",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 897,
              "byte_end": 2676,
              "ast_path": "function:find_best_app",
              "content_hash": "31e4877b92dac2e4b30a01ac6de6b33aa9ac352b31f4f3020ce80f924a4f49b2"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:NoAppException:37"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:_called_with_wrong_args:94"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function find_best_app",
              "symbol_name": "find_best_app",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:get_version:267",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 8003,
              "byte_end": 8448,
              "ast_path": "function:get_version",
              "content_hash": "13b38d8519deb4ca032b21dd1cb79aa6f88de7e861bf7a99558b3dc8c13e358b"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function get_version",
              "symbol_name": "get_version",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:load_dotenv:698",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 23897,
              "byte_end": 26057,
              "ast_path": "function:load_dotenv",
              "content_hash": "2a267c0f6aafc25803425e9ae8180528f049b3052338b96d3aca2680293a7937"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/cli.py:_env_file_callback:493"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function load_dotenv",
              "symbol_name": "load_dotenv",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:locate_app:230",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 6848,
              "byte_end": 6966,
              "ast_path": "function:locate_app",
              "content_hash": "3908ecfd01163fce6f128dc1c94ba7830ddb4ba5915d237da84cab023475f024"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function locate_app",
              "symbol_name": "locate_app",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:locate_app:236",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 6981,
              "byte_end": 7106,
              "ast_path": "function:locate_app",
              "content_hash": "bf8042145b4a39c8949c457413fb675aee21f09b67a8631fdcf7dd48cdbe34aa"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function locate_app",
              "symbol_name": "locate_app",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:locate_app:241",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 7109,
              "byte_end": 8000,
              "ast_path": "function:locate_app",
              "content_hash": "0cbdadbccdd09f3c8b7e5382830ad41bedfa87e4f0dc6650a6eb9607ccd5e05e"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function locate_app",
              "symbol_name": "locate_app",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:main:1122",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 36733,
              "byte_end": 36767,
              "ast_path": "function:main",
              "content_hash": "3ce7e69224f9911d2368576d8d2636e55191585be61b570379a866d7eb8052c7"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/cli.py:main:1122"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:main:1122"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function main",
              "symbol_name": "main",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:prepare_import:200",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 6075,
              "byte_end": 6833,
              "ast_path": "function:prepare_import",
              "content_hash": "6f782cd47ba837652c22c7821a8ed94633d643c42a6d1e73afcfdbe528810040"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/cli.py:ScriptInfo.load_app:333"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function prepare_import",
              "symbol_name": "prepare_import",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:routes_command:1061",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 35041,
              "byte_end": 36462,
              "ast_path": "function:routes_command",
              "content_hash": "de54c495f02d2082084e70b33ad58590157df474c65053fbcd2d33db2f21cb33"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:AppGroup.command:413"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function routes_command",
              "symbol_name": "routes_command",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:run_command.app:963",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 32137,
              "byte_end": 32292,
              "ast_path": "function:run_command.app",
              "content_hash": "ff10e64178d11e97eb758930517784fe7befcf3e7f00477ce7a5a5251dd194ed"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function app",
              "symbol_name": "app",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:run_command:935",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 31221,
              "byte_end": 32873,
              "ast_path": "function:run_command",
              "content_hash": "274ef091406ad22f695821c2424adb1a05b3230349a4c26d2bf2426e32db69ee"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:AppGroup.command:413"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:CertParamType:780"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:ScriptInfo.load_app:333"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:SeparatedPathType:867"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:show_server_banner:766"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function run_command",
              "symbol_name": "run_command",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:shell_command:1001",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 33009,
              "byte_end": 34586,
              "ast_path": "function:shell_command",
              "content_hash": "38fdf9991c96e369786c2b407f792344c23c3deb4920db80d4b857076589df8d"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:AppGroup.command:413"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function shell_command",
              "symbol_name": "shell_command",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:show_server_banner:766",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 26104,
              "byte_end": 26524,
              "ast_path": "function:show_server_banner",
              "content_hash": "4cacbd42a7d6bb09208e5d498b4413f2ea05e91a570f49c7a05bb2824babb7f2"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/cli.py:run_command:935"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function show_server_banner",
              "symbol_name": "show_server_banner",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:with_appcontext.decorator:395",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 12425,
              "byte_end": 12685,
              "ast_path": "function:with_appcontext.decorator",
              "content_hash": "c49c0af5fde1814f45b76a534b79d171378c458c0326b1ffa5edac36fa8414da"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function decorator",
              "symbol_name": "decorator",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/cli.py:with_appcontext:380",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/cli.py",
              "byte_start": 11849,
              "byte_end": 12726,
              "ast_path": "function:with_appcontext",
              "content_hash": "295814aff7ae90b368a4bfe6751cfa9eb672f4d6edd3e32e39da31b5cd858052"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/cli.py:AppGroup.command:413"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/cli.py:ScriptInfo.load_app:333"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function with_appcontext",
              "symbol_name": "with_appcontext",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          }
        ],
        "edges": [
          {
            "edge_id": "calls:symbol:src/flask/cli.py:AppGroup.command:413:symbol:src/flask/cli.py:AppGroup.command:413:425",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:AppGroup.command:413",
            "to_node": "symbol:src/flask/cli.py:AppGroup.command:413",
            "evidence": {
              "line": 425,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:AppGroup.command:413:symbol:src/flask/cli.py:with_appcontext:380:424",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:AppGroup.command:413",
            "to_node": "symbol:src/flask/cli.py:with_appcontext:380",
            "evidence": {
              "line": 424,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:AppGroup.group:429:symbol:src/flask/cli.py:AppGroup.group:429:437",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:AppGroup.group:429",
            "to_node": "symbol:src/flask/cli.py:AppGroup.group:429",
            "evidence": {
              "line": 437,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.get_command:609:symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600:610",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:FlaskGroup.get_command:609",
            "to_node": "symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600",
            "evidence": {
              "line": 610,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.get_command:609:symbol:src/flask/cli.py:FlaskGroup.get_command:609:613",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:FlaskGroup.get_command:609",
            "to_node": "symbol:src/flask/cli.py:FlaskGroup.get_command:609",
            "evidence": {
              "line": 613,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.get_command:609:symbol:src/flask/cli.py:FlaskGroup.get_command:609:634",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:FlaskGroup.get_command:609",
            "to_node": "symbol:src/flask/cli.py:FlaskGroup.get_command:609",
            "evidence": {
              "line": 634,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.get_command:609:symbol:src/flask/cli.py:ScriptInfo.load_app:333:623",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:FlaskGroup.get_command:609",
            "to_node": "symbol:src/flask/cli.py:ScriptInfo.load_app:333",
            "evidence": {
              "line": 623,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600:637",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636",
            "to_node": "symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600",
            "evidence": {
              "line": 637,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:639",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636",
            "to_node": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636",
            "evidence": {
              "line": 639,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:645",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636",
            "to_node": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636",
            "evidence": {
              "line": 645,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.list_commands:636:symbol:src/flask/cli.py:ScriptInfo.load_app:333:645",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636",
            "to_node": "symbol:src/flask/cli.py:ScriptInfo.load_app:333",
            "evidence": {
              "line": 645,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.make_context:657:symbol:src/flask/cli.py:FlaskGroup.make_context:657:676",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:FlaskGroup.make_context:657",
            "to_node": "symbol:src/flask/cli.py:FlaskGroup.make_context:657",
            "evidence": {
              "line": 676,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.make_context:657:symbol:src/flask/cli.py:ScriptInfo:293:670",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:FlaskGroup.make_context:657",
            "to_node": "symbol:src/flask/cli.py:ScriptInfo:293",
            "evidence": {
              "line": 670,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:FlaskGroup.parse_args:678:symbol:src/flask/cli.py:FlaskGroup.parse_args:678:688",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:FlaskGroup.parse_args:678",
            "to_node": "symbol:src/flask/cli.py:FlaskGroup.parse_args:678",
            "evidence": {
              "line": 688,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:ScriptInfo.load_app:333:symbol:src/flask/cli.py:NoAppException:37:359",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:ScriptInfo.load_app:333",
            "to_node": "symbol:src/flask/cli.py:NoAppException:37",
            "evidence": {
              "line": 359,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:ScriptInfo.load_app:333:symbol:src/flask/cli.py:prepare_import:200:348",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:ScriptInfo.load_app:333",
            "to_node": "symbol:src/flask/cli.py:prepare_import:200",
            "evidence": {
              "line": 348,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:ScriptInfo.load_app:333:symbol:src/flask/cli.py:prepare_import:200:352",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:ScriptInfo.load_app:333",
            "to_node": "symbol:src/flask/cli.py:prepare_import:200",
            "evidence": {
              "line": 352,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:_env_file_callback:493:symbol:src/flask/cli.py:load_dotenv:698:510",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:_env_file_callback:493",
            "to_node": "symbol:src/flask/cli.py:load_dotenv:698",
            "evidence": {
              "line": 510,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:131",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:find_app_by_string:120",
            "to_node": "symbol:src/flask/cli.py:NoAppException:37",
            "evidence": {
              "line": 131,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:142",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:find_app_by_string:120",
            "to_node": "symbol:src/flask/cli.py:NoAppException:37",
            "evidence": {
              "line": 142,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:159",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:find_app_by_string:120",
            "to_node": "symbol:src/flask/cli.py:NoAppException:37",
            "evidence": {
              "line": 159,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:163",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:find_app_by_string:120",
            "to_node": "symbol:src/flask/cli.py:NoAppException:37",
            "evidence": {
              "line": 163,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:170",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:find_app_by_string:120",
            "to_node": "symbol:src/flask/cli.py:NoAppException:37",
            "evidence": {
              "line": 170,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:183",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:find_app_by_string:120",
            "to_node": "symbol:src/flask/cli.py:NoAppException:37",
            "evidence": {
              "line": 183,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:NoAppException:37:194",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:find_app_by_string:120",
            "to_node": "symbol:src/flask/cli.py:NoAppException:37",
            "evidence": {
              "line": 194,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:find_app_by_string:120:symbol:src/flask/cli.py:_called_with_wrong_args:94:180",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:find_app_by_string:120",
            "to_node": "symbol:src/flask/cli.py:_called_with_wrong_args:94",
            "evidence": {
              "line": 180,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:find_best_app:41:symbol:src/flask/cli.py:NoAppException:37:60",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:find_best_app:41",
            "to_node": "symbol:src/flask/cli.py:NoAppException:37",
            "evidence": {
              "line": 60,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:find_best_app:41:symbol:src/flask/cli.py:NoAppException:37:80",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:find_best_app:41",
            "to_node": "symbol:src/flask/cli.py:NoAppException:37",
            "evidence": {
              "line": 80,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:find_best_app:41:symbol:src/flask/cli.py:NoAppException:37:87",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:find_best_app:41",
            "to_node": "symbol:src/flask/cli.py:NoAppException:37",
            "evidence": {
              "line": 87,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:find_best_app:41:symbol:src/flask/cli.py:_called_with_wrong_args:94:77",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:find_best_app:41",
            "to_node": "symbol:src/flask/cli.py:_called_with_wrong_args:94",
            "evidence": {
              "line": 77,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:main:1122:symbol:src/flask/cli.py:main:1122:1123",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:main:1122",
            "to_node": "symbol:src/flask/cli.py:main:1122",
            "evidence": {
              "line": 1123,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:routes_command:1061:symbol:src/flask/cli.py:AppGroup.command:413:1048",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:routes_command:1061",
            "to_node": "symbol:src/flask/cli.py:AppGroup.command:413",
            "evidence": {
              "line": 1048,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:AppGroup.command:413:882",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:run_command:935",
            "to_node": "symbol:src/flask/cli.py:AppGroup.command:413",
            "evidence": {
              "line": 882,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:CertParamType:780:887",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:run_command:935",
            "to_node": "symbol:src/flask/cli.py:CertParamType:780",
            "evidence": {
              "line": 887,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:ScriptInfo.load_app:333:955",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:run_command:935",
            "to_node": "symbol:src/flask/cli.py:ScriptInfo.load_app:333",
            "evidence": {
              "line": 955,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:SeparatedPathType:867:918",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:run_command:935",
            "to_node": "symbol:src/flask/cli.py:SeparatedPathType:867",
            "evidence": {
              "line": 918,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:SeparatedPathType:867:927",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:run_command:935",
            "to_node": "symbol:src/flask/cli.py:SeparatedPathType:867",
            "evidence": {
              "line": 927,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:run_command:935:symbol:src/flask/cli.py:show_server_banner:766:981",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:run_command:935",
            "to_node": "symbol:src/flask/cli.py:show_server_banner:766",
            "evidence": {
              "line": 981,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:shell_command:1001:symbol:src/flask/cli.py:AppGroup.command:413:999",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:shell_command:1001",
            "to_node": "symbol:src/flask/cli.py:AppGroup.command:413",
            "evidence": {
              "line": 999,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/cli.py:with_appcontext:380:symbol:src/flask/cli.py:ScriptInfo.load_app:333:397",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/cli.py:with_appcontext:380",
            "to_node": "symbol:src/flask/cli.py:ScriptInfo.load_app:333",
            "evidence": {
              "line": 397,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:AppGroup.command.decorator:422",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:AppGroup.command.decorator:422",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:AppGroup.command:413",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:AppGroup.command:413",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:AppGroup.group:429",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:AppGroup.group:429",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:AppGroup:405",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:AppGroup:405",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:CertParamType.__init__:788",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:CertParamType.__init__:788",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:CertParamType.convert:791",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:CertParamType.convert:791",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:CertParamType:780",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:CertParamType:780",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:FlaskGroup.__init__:563",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:FlaskGroup.__init__:563",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:FlaskGroup._load_plugin_commands:600",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:FlaskGroup.get_command:609",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:FlaskGroup.get_command:609",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:FlaskGroup.list_commands:636",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:FlaskGroup.list_commands:636",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:FlaskGroup.make_context:657",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:FlaskGroup.make_context:657",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:FlaskGroup.parse_args:678",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:FlaskGroup.parse_args:678",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:FlaskGroup:531",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:FlaskGroup:531",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:NoAppException:37",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:NoAppException:37",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:ScriptInfo.__init__:305",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:ScriptInfo.__init__:305",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:ScriptInfo.load_app:333",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:ScriptInfo.load_app:333",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:ScriptInfo:293",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:ScriptInfo:293",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:SeparatedPathType.convert:873",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:SeparatedPathType.convert:873",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:SeparatedPathType:867",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:SeparatedPathType:867",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:_called_with_wrong_args:94",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:_called_with_wrong_args:94",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:_env_file_callback:493",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:_env_file_callback:493",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:_path_is_ancestor:691",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:_path_is_ancestor:691",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:_set_app:440",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:_set_app:440",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:_set_debug:468",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:_set_debug:468",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:_validate_key:828",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:_validate_key:828",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:find_app_by_string:120",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:find_app_by_string:120",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:find_best_app:41",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:find_best_app:41",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:get_version:267",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:get_version:267",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:load_dotenv:698",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:load_dotenv:698",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:locate_app:230",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:locate_app:230",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:locate_app:236",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:locate_app:236",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:locate_app:241",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:locate_app:241",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:main:1122",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:main:1122",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:prepare_import:200",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:prepare_import:200",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:routes_command:1061",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:routes_command:1061",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:run_command.app:963",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:run_command.app:963",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:run_command:935",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:run_command:935",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:shell_command:1001",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:shell_command:1001",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:show_server_banner:766",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:show_server_banner:766",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:with_appcontext.decorator:395",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:with_appcontext.decorator:395",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/cli.py:symbol:src/flask/cli.py:with_appcontext:380",
            "edge_type": "contains",
            "from_node": "module:src/flask/cli.py",
            "to_node": "symbol:src/flask/cli.py:with_appcontext:380",
            "evidence": {
              "rel": "ast_containment"
            }
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "src/flask/cli.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "module:src/flask/cli.py",
      "confidence_trigger": 0.85,
      "output_size_tokens": 779,
      "result": {
        "status": "ok",
        "file_path": "src/flask/cli.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 1135,
        "lines": [
          {
            "line_number": 1,
            "content": "from __future__ import annotations"
          },
          {
            "line_number": 2,
            "content": ""
          },
          {
            "line_number": 3,
            "content": "import ast"
          },
          {
            "line_number": 4,
            "content": "import collections.abc as cabc"
          },
          {
            "line_number": 5,
            "content": "import importlib.metadata"
          },
          {
            "line_number": 6,
            "content": "import inspect"
          },
          {
            "line_number": 7,
            "content": "import os"
          },
          {
            "line_number": 8,
            "content": "import platform"
          },
          {
            "line_number": 9,
            "content": "import re"
          },
          {
            "line_number": 10,
            "content": "import sys"
          },
          {
            "line_number": 11,
            "content": "import traceback"
          },
          {
            "line_number": 12,
            "content": "import typing as t"
          },
          {
            "line_number": 13,
            "content": "from functools import update_wrapper"
          },
          {
            "line_number": 14,
            "content": "from operator import itemgetter"
          },
          {
            "line_number": 15,
            "content": "from types import ModuleType"
          },
          {
            "line_number": 16,
            "content": ""
          },
          {
            "line_number": 17,
            "content": "import click"
          },
          {
            "line_number": 18,
            "content": "from click.core import ParameterSource"
          },
          {
            "line_number": 19,
            "content": "from werkzeug import run_simple"
          },
          {
            "line_number": 20,
            "content": "from werkzeug.serving import is_running_from_reloader"
          },
          {
            "line_number": 21,
            "content": "from werkzeug.utils import import_string"
          },
          {
            "line_number": 22,
            "content": ""
          },
          {
            "line_number": 23,
            "content": "from .globals import current_app"
          },
          {
            "line_number": 24,
            "content": "from .helpers import get_debug_flag"
          },
          {
            "line_number": 25,
            "content": "from .helpers import get_load_dotenv"
          },
          {
            "line_number": 26,
            "content": ""
          },
          {
            "line_number": 27,
            "content": "if t.TYPE_CHECKING:"
          },
          {
            "line_number": 28,
            "content": "    import ssl"
          },
          {
            "line_number": 29,
            "content": ""
          },
          {
            "line_number": 30,
            "content": "    from _typeshed.wsgi import StartResponse"
          },
          {
            "line_number": 31,
            "content": "    from _typeshed.wsgi import WSGIApplication"
          },
          {
            "line_number": 32,
            "content": "    from _typeshed.wsgi import WSGIEnvironment"
          },
          {
            "line_number": 33,
            "content": ""
          },
          {
            "line_number": 34,
            "content": "    from .app import Flask"
          },
          {
            "line_number": 35,
            "content": ""
          },
          {
            "line_number": 36,
            "content": ""
          },
          {
            "line_number": 37,
            "content": "class NoAppException(click.UsageError):"
          },
          {
            "line_number": 38,
            "content": "    \"\"\"Raised if an application cannot be found or loaded.\"\"\""
          },
          {
            "line_number": 39,
            "content": ""
          },
          {
            "line_number": 40,
            "content": ""
          },
          {
            "line_number": 41,
            "content": "def find_best_app(module: ModuleType) -> Flask:"
          },
          {
            "line_number": 42,
            "content": "    \"\"\"Given a module instance this tries to find the best possible"
          },
          {
            "line_number": 43,
            "content": "    application in the module or raises an exception."
          },
          {
            "line_number": 44,
            "content": "    \"\"\""
          },
          {
            "line_number": 45,
            "content": "    from . import Flask"
          },
          {
            "line_number": 46,
            "content": ""
          },
          {
            "line_number": 47,
            "content": "    # Search for the most common names first."
          },
          {
            "line_number": 48,
            "content": "    for attr_name in (\"app\", \"application\"):"
          },
          {
            "line_number": 49,
            "content": "        app = getattr(module, attr_name, None)"
          },
          {
            "line_number": 50,
            "content": ""
          }
        ]
      }
    },
    {
      "tool": "resolve_dependency",
      "args": {
        "node_id": "module:src/flask/ctx.py",
        "depth": 2
      },
      "node_id": "module:src/flask/ctx.py",
      "confidence_trigger": 0.85,
      "output_size_tokens": 7826,
      "result": {
        "status": "ok",
        "seed_node": "module:src/flask/ctx.py",
        "depth": 2,
        "nodes": [
          {
            "node_id": "module:src/flask/ctx.py",
            "node_type": "module",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 0,
              "byte_end": 18104,
              "ast_path": "module",
              "content_hash": "fdff186ec6f47fa5a15fe5947c843bbd2ee20ab0be34036ea8dedaaa89c58f9f"
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
              "symbol_name": "src/flask/ctx.py",
              "symbol_type": "module",
              "tier": 1
            },
            "confidence": 1.0
          },
          {
            "node_id": "symbol:src/flask/ctx.py:AppContext.__enter__:506",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 17141,
              "byte_end": 17212,
              "ast_path": "function:AppContext.__enter__",
              "content_hash": "49d6e2603d322097fb8af9c91208bb12a9cb537500d3ed7e1510aae36fb00050"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/ctx.py:AppContext.push:416"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function __enter__",
              "symbol_name": "__enter__",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:AppContext.__exit__:510",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 17218,
              "byte_end": 17409,
              "ast_path": "function:AppContext.__exit__",
              "content_hash": "436857e855acca88fb1b7e9cb479939e377d85c53ecb17f079f83485d485e4e0"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function __exit__",
              "symbol_name": "__exit__",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:AppContext.__init__:300",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 9671,
              "byte_end": 11040,
              "ast_path": "function:AppContext.__init__",
              "content_hash": "2078f23f15db15ba76104359c1ca9e81facb42c18e3b71a035284fa8513e3fe3"
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
            "node_id": "symbol:src/flask/ctx.py:AppContext.__repr__:518",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 17415,
              "byte_end": 17724,
              "ast_path": "function:AppContext.__repr__",
              "content_hash": "f09653a8856474fcb8f0a8cc4270ff707229e8f75200c5b647988f989d09df5e"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function __repr__",
              "symbol_name": "__repr__",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:AppContext._get_session:381",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 12480,
              "byte_end": 12986,
              "ast_path": "function:AppContext._get_session",
              "content_hash": "c7002c97308535374aae1e0a5498d7487ec697c65c3313c915895f1be8e8a8af"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/ctx.py:AppContext.push:416"
                },
                {
                  "source": "symbol:src/flask/ctx.py:AppContext.session:396"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _get_session",
              "symbol_name": "_get_session",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:AppContext.copy:355",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 11645,
              "byte_end": 12093,
              "ast_path": "function:AppContext.copy",
              "content_hash": "567f7d1eba70f4f7ded882364729684643188fed01d229fa7ce27101de211eec"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/ctx.py:copy_current_request_context:154"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function copy",
              "symbol_name": "copy",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:AppContext.from_environ:340",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 11063,
              "byte_end": 11482,
              "ast_path": "function:AppContext.from_environ",
              "content_hash": "35ff65fa7b504351ae05f4c82b5fcd888f866f9f81136b82fc3604f02f635608"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function from_environ",
              "symbol_name": "from_environ",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:AppContext.has_request:351",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 11502,
              "byte_end": 11639,
              "ast_path": "function:AppContext.has_request",
              "content_hash": "380cc2b568acdef6a30b39dc24bdaab2933ba0c61738d12ab82872c904a0f3bb"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function has_request",
              "symbol_name": "has_request",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:AppContext.match_request:405",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 13388,
              "byte_end": 13856,
              "ast_path": "function:AppContext.match_request",
              "content_hash": "30a3e8e2b7c2766b5f4a4905aa8b3b578b81ff809b295943a096e0091092127e"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/ctx.py:AppContext.push:416"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function match_request",
              "symbol_name": "match_request",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:AppContext.pop:446",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 15078,
              "byte_end": 17135,
              "ast_path": "function:AppContext.pop",
              "content_hash": "f8d3c58cf108fe06a142bf57b64cbe018b2eaa32d845582931d811497d06d67d"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function pop",
              "symbol_name": "pop",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:AppContext.push:416",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 13890,
              "byte_end": 15072,
              "ast_path": "function:AppContext.push",
              "content_hash": "baea61546581cd071253f636eab7755bb187517fc7ef18792714d8ff15c99ceb"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/ctx.py:AppContext.__enter__:506"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/ctx.py:AppContext._get_session:381"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/ctx.py:AppContext.match_request:405"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function push",
              "symbol_name": "push",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:AppContext.request:371",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 12113,
              "byte_end": 12474,
              "ast_path": "function:AppContext.request",
              "content_hash": "434827a2e8688094cab8a5cd074172ea07d79b9ccbe0c31b22f18c03e291a182"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function request",
              "symbol_name": "request",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:AppContext.session:396",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 13006,
              "byte_end": 13382,
              "ast_path": "function:AppContext.session",
              "content_hash": "590089f091d3708bc6500e680c2a3c5f5d9f23d40cd1afc1d06956bf353bd989"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/ctx.py:AppContext._get_session:381"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function session",
              "symbol_name": "session",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:AppContext:260",
            "node_type": "class",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 7826,
              "byte_end": 17724,
              "ast_path": "class:AppContext",
              "content_hash": "41e3a98bbf3c7c8417f1a1a56087bc909c2bb0e71a69aaa7419637ccfbb9b4e5"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "class AppContext",
              "symbol_name": "AppContext",
              "symbol_type": "class",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:_AppCtxGlobals.__contains__:105",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 3014,
              "byte_end": 3093,
              "ast_path": "function:_AppCtxGlobals.__contains__",
              "content_hash": "372d4fd435778de7a0d630f04d742b381fd9c4fe5d4ccf52de0d5373553f6bc6"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function __contains__",
              "symbol_name": "__contains__",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:_AppCtxGlobals.__delattr__:62",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 1531,
              "byte_end": 1695,
              "ast_path": "function:_AppCtxGlobals.__delattr__",
              "content_hash": "d4473f10459f5bc5b511d3727272c83e99e370dc8e2ec20819c873519bc96b25"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function __delattr__",
              "symbol_name": "__delattr__",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:_AppCtxGlobals.__getattr__:53",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 1260,
              "byte_end": 1428,
              "ast_path": "function:_AppCtxGlobals.__getattr__",
              "content_hash": "47424390a52cdb65d1749b15943e84e296392b5f10668f7e6b6541b921dcf6c3"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function __getattr__",
              "symbol_name": "__getattr__",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:_AppCtxGlobals.__iter__:108",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 3099,
              "byte_end": 3172,
              "ast_path": "function:_AppCtxGlobals.__iter__",
              "content_hash": "fa52e38a238b57ff4cce61cbbeeb518ec2c44f57beeba3fa59163d92572639f6"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function __iter__",
              "symbol_name": "__iter__",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:_AppCtxGlobals.__repr__:111",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 3178,
              "byte_end": 3353,
              "ast_path": "function:_AppCtxGlobals.__repr__",
              "content_hash": "2f1e4b8fdf144ad853e6a492d0e8af1258225ed0baf2287b2a9ee415fa57c3e7"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function __repr__",
              "symbol_name": "__repr__",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:_AppCtxGlobals.__setattr__:59",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 1434,
              "byte_end": 1525,
              "ast_path": "function:_AppCtxGlobals.__setattr__",
              "content_hash": "29cbee7f8a5702f01d5eadf02c103cae633be76608525ce9e167c47ba1af09a1"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function __setattr__",
              "symbol_name": "__setattr__",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 1701,
              "byte_end": 2066,
              "ast_path": "function:_AppCtxGlobals.get",
              "content_hash": "4cf395aed2615680e0cf616b5c5c1c824db38fd29a94ac5e59ed38cb723e5da8"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68"
                },
                {
                  "source": "symbol:src/flask/ctx.py:after_this_request:118"
                },
                {
                  "source": "symbol:src/flask/ctx.py:copy_current_request_context:154"
                },
                {
                  "source": "symbol:src/flask/ctx.py:has_app_context:235"
                },
                {
                  "source": "symbol:src/flask/ctx.py:has_request_context:209"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function get",
              "symbol_name": "get",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:_AppCtxGlobals.pop:79",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 2072,
              "byte_end": 2559,
              "ast_path": "function:_AppCtxGlobals.pop",
              "content_hash": "a35b03211db5bdd48b04f6451c32780f58e7436e19d4e14e91bde6349a506db6"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function pop",
              "symbol_name": "pop",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 2565,
              "byte_end": 3008,
              "ast_path": "function:_AppCtxGlobals.setdefault",
              "content_hash": "a1b558471d75d55bc52218b7f969c7e3837f8dd415293c498a5fb423acdc8cc1"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function setdefault",
              "symbol_name": "setdefault",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:_AppCtxGlobals:30",
            "node_type": "class",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 682,
              "byte_end": 3353,
              "ast_path": "class:_AppCtxGlobals",
              "content_hash": "27b6e1bfb7f9586ebfade33d9dae93f6f8f5019c8f23f86bb525205734712d28"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "class _AppCtxGlobals",
              "symbol_name": "_AppCtxGlobals",
              "symbol_type": "class",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:__getattr__:528",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 17727,
              "byte_end": 18103,
              "ast_path": "function:__getattr__",
              "content_hash": "c5fad5c69c4d50ed44b68d2ad5cf4a905b7449f577f0fdd846822fccce57ae0b"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function __getattr__",
              "symbol_name": "__getattr__",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:after_this_request:118",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 3356,
              "byte_end": 4338,
              "ast_path": "function:after_this_request",
              "content_hash": "590fe62a7a96a19cbee51dd4bca788f3af64e20de69d6ead3cabd6a43c949c81"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function after_this_request",
              "symbol_name": "after_this_request",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:copy_current_request_context.wrapper:202",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 6196,
              "byte_end": 6325,
              "ast_path": "function:copy_current_request_context.wrapper",
              "content_hash": "5c894f7704a43f58bf74129ef5bbb2740e4deb346bf58274ac5004a0645e848e"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function wrapper",
              "symbol_name": "wrapper",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:copy_current_request_context:154",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 4392,
              "byte_end": 6364,
              "ast_path": "function:copy_current_request_context",
              "content_hash": "9504136be71c1a8e4bb30c06be7dac93ce3e790126eeba4b8142319bbe08e413"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/ctx.py:AppContext.copy:355"
                },
                {
                  "is_external": false,
                  "target": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function copy_current_request_context",
              "symbol_name": "copy_current_request_context",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:has_app_context:235",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 7138,
              "byte_end": 7823,
              "ast_path": "function:has_app_context",
              "content_hash": "5da5ef672c2c455b670186d0805938dfb0fca798aba4a35efe3d992b4455a99a"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function has_app_context",
              "symbol_name": "has_app_context",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:src/flask/ctx.py:has_request_context:209",
            "node_type": "function",
            "source_anchor": {
              "file_path": "src/flask/ctx.py",
              "byte_start": 6397,
              "byte_end": 7135,
              "ast_path": "function:has_request_context",
              "content_hash": "888098922a159d358f8b355821b2f8786bb1d134f4257b8c69d8ca11b4296d02"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function has_request_context",
              "symbol_name": "has_request_context",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          }
        ],
        "edges": [
          {
            "edge_id": "calls:symbol:src/flask/ctx.py:AppContext.__enter__:506:symbol:src/flask/ctx.py:AppContext.push:416:507",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/ctx.py:AppContext.__enter__:506",
            "to_node": "symbol:src/flask/ctx.py:AppContext.push:416",
            "evidence": {
              "line": 507,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/ctx.py:AppContext.push:416:symbol:src/flask/ctx.py:AppContext._get_session:381:439",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/ctx.py:AppContext.push:416",
            "to_node": "symbol:src/flask/ctx.py:AppContext._get_session:381",
            "evidence": {
              "line": 439,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/ctx.py:AppContext.push:416:symbol:src/flask/ctx.py:AppContext.match_request:405:444",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/ctx.py:AppContext.push:416",
            "to_node": "symbol:src/flask/ctx.py:AppContext.match_request:405",
            "evidence": {
              "line": 444,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/ctx.py:AppContext.session:396:symbol:src/flask/ctx.py:AppContext._get_session:381:401",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/ctx.py:AppContext.session:396",
            "to_node": "symbol:src/flask/ctx.py:AppContext._get_session:381",
            "evidence": {
              "line": 401,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:77",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68",
            "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68",
            "evidence": {
              "line": 77,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93:symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93:103",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93",
            "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93",
            "evidence": {
              "line": 103,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/ctx.py:after_this_request:118:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:139",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/ctx.py:after_this_request:118",
            "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68",
            "evidence": {
              "line": 139,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/ctx.py:copy_current_request_context:154:symbol:src/flask/ctx.py:AppContext.copy:355:200",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/ctx.py:copy_current_request_context:154",
            "to_node": "symbol:src/flask/ctx.py:AppContext.copy:355",
            "evidence": {
              "line": 200,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/ctx.py:copy_current_request_context:154:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:192",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/ctx.py:copy_current_request_context:154",
            "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68",
            "evidence": {
              "line": 192,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/ctx.py:has_app_context:235:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:257",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/ctx.py:has_app_context:235",
            "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68",
            "evidence": {
              "line": 257,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:src/flask/ctx.py:has_request_context:209:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68:232",
            "edge_type": "calls",
            "from_node": "symbol:src/flask/ctx.py:has_request_context:209",
            "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68",
            "evidence": {
              "line": 232,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:AppContext.__enter__:506",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:AppContext.__enter__:506",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:AppContext.__exit__:510",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:AppContext.__exit__:510",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:AppContext.__init__:300",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:AppContext.__init__:300",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:AppContext.__repr__:518",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:AppContext.__repr__:518",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:AppContext._get_session:381",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:AppContext._get_session:381",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:AppContext.copy:355",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:AppContext.copy:355",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:AppContext.from_environ:340",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:AppContext.from_environ:340",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:AppContext.has_request:351",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:AppContext.has_request:351",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:AppContext.match_request:405",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:AppContext.match_request:405",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:AppContext.pop:446",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:AppContext.pop:446",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:AppContext.push:416",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:AppContext.push:416",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:AppContext.request:371",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:AppContext.request:371",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:AppContext.session:396",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:AppContext.session:396",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:AppContext:260",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:AppContext:260",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:_AppCtxGlobals.__contains__:105",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.__contains__:105",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:_AppCtxGlobals.__delattr__:62",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.__delattr__:62",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:_AppCtxGlobals.__getattr__:53",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.__getattr__:53",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:_AppCtxGlobals.__iter__:108",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.__iter__:108",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:_AppCtxGlobals.__repr__:111",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.__repr__:111",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:_AppCtxGlobals.__setattr__:59",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.__setattr__:59",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:_AppCtxGlobals.get:68",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.get:68",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:_AppCtxGlobals.pop:79",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.pop:79",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals.setdefault:93",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:_AppCtxGlobals:30",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:_AppCtxGlobals:30",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:__getattr__:528",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:__getattr__:528",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:after_this_request:118",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:after_this_request:118",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:copy_current_request_context.wrapper:202",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:copy_current_request_context.wrapper:202",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:copy_current_request_context:154",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:copy_current_request_context:154",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:has_app_context:235",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:has_app_context:235",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:src/flask/ctx.py:symbol:src/flask/ctx.py:has_request_context:209",
            "edge_type": "contains",
            "from_node": "module:src/flask/ctx.py",
            "to_node": "symbol:src/flask/ctx.py:has_request_context:209",
            "evidence": {
              "rel": "ast_containment"
            }
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "src/flask/ctx.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "module:src/flask/ctx.py",
      "confidence_trigger": 0.85,
      "output_size_tokens": 768,
      "result": {
        "status": "ok",
        "file_path": "src/flask/ctx.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 449,
        "lines": [
          {
            "line_number": 1,
            "content": "from __future__ import annotations"
          },
          {
            "line_number": 2,
            "content": ""
          },
          {
            "line_number": 3,
            "content": "import contextvars"
          },
          {
            "line_number": 4,
            "content": "import sys"
          },
          {
            "line_number": 5,
            "content": "import typing as t"
          },
          {
            "line_number": 6,
            "content": "from functools import update_wrapper"
          },
          {
            "line_number": 7,
            "content": "from types import TracebackType"
          },
          {
            "line_number": 8,
            "content": ""
          },
          {
            "line_number": 9,
            "content": "from werkzeug.exceptions import HTTPException"
          },
          {
            "line_number": 10,
            "content": ""
          },
          {
            "line_number": 11,
            "content": "from . import typing as ft"
          },
          {
            "line_number": 12,
            "content": "from .globals import _cv_app"
          },
          {
            "line_number": 13,
            "content": "from .globals import _cv_request"
          },
          {
            "line_number": 14,
            "content": "from .signals import appcontext_popped"
          },
          {
            "line_number": 15,
            "content": "from .signals import appcontext_pushed"
          },
          {
            "line_number": 16,
            "content": ""
          },
          {
            "line_number": 17,
            "content": "if t.TYPE_CHECKING:  # pragma: no cover"
          },
          {
            "line_number": 18,
            "content": "    from _typeshed.wsgi import WSGIEnvironment"
          },
          {
            "line_number": 19,
            "content": ""
          },
          {
            "line_number": 20,
            "content": "    from .app import Flask"
          },
          {
            "line_number": 21,
            "content": "    from .sessions import SessionMixin"
          },
          {
            "line_number": 22,
            "content": "    from .wrappers import Request"
          },
          {
            "line_number": 23,
            "content": ""
          },
          {
            "line_number": 24,
            "content": ""
          },
          {
            "line_number": 25,
            "content": "# a singleton sentinel value for parameter defaults"
          },
          {
            "line_number": 26,
            "content": "_sentinel = object()"
          },
          {
            "line_number": 27,
            "content": ""
          },
          {
            "line_number": 28,
            "content": ""
          },
          {
            "line_number": 29,
            "content": "class _AppCtxGlobals:"
          },
          {
            "line_number": 30,
            "content": "    \"\"\"A plain object. Used as a namespace for storing data during an"
          },
          {
            "line_number": 31,
            "content": "    application context."
          },
          {
            "line_number": 32,
            "content": ""
          },
          {
            "line_number": 33,
            "content": "    Creating an app context automatically creates this object, which is"
          },
          {
            "line_number": 34,
            "content": "    made available as the :data:`g` proxy."
          },
          {
            "line_number": 35,
            "content": ""
          },
          {
            "line_number": 36,
            "content": "    .. describe:: 'key' in g"
          },
          {
            "line_number": 37,
            "content": ""
          },
          {
            "line_number": 38,
            "content": "        Check whether an attribute is present."
          },
          {
            "line_number": 39,
            "content": ""
          },
          {
            "line_number": 40,
            "content": "        .. versionadded:: 0.10"
          },
          {
            "line_number": 41,
            "content": ""
          },
          {
            "line_number": 42,
            "content": "    .. describe:: iter(g)"
          },
          {
            "line_number": 43,
            "content": ""
          },
          {
            "line_number": 44,
            "content": "        Return an iterator over the attribute names."
          },
          {
            "line_number": 45,
            "content": ""
          },
          {
            "line_number": 46,
            "content": "        .. versionadded:: 0.10"
          },
          {
            "line_number": 47,
            "content": "    \"\"\""
          },
          {
            "line_number": 48,
            "content": ""
          },
          {
            "line_number": 49,
            "content": "    # Define attr methods to let mypy know this is a namespace object"
          },
          {
            "line_number": 50,
            "content": "    # that has arbitrary attributes."
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "src/flask/app.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "symbol:src/flask/app.py:Flask.__call__:1618",
      "confidence_trigger": 0.77,
      "output_size_tokens": 880,
      "result": {
        "status": "ok",
        "file_path": "src/flask/app.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 1536,
        "lines": [
          {
            "line_number": 1,
            "content": "from __future__ import annotations"
          },
          {
            "line_number": 2,
            "content": ""
          },
          {
            "line_number": 3,
            "content": "import collections.abc as cabc"
          },
          {
            "line_number": 4,
            "content": "import os"
          },
          {
            "line_number": 5,
            "content": "import sys"
          },
          {
            "line_number": 6,
            "content": "import typing as t"
          },
          {
            "line_number": 7,
            "content": "import weakref"
          },
          {
            "line_number": 8,
            "content": "from datetime import timedelta"
          },
          {
            "line_number": 9,
            "content": "from inspect import iscoroutinefunction"
          },
          {
            "line_number": 10,
            "content": "from itertools import chain"
          },
          {
            "line_number": 11,
            "content": "from types import TracebackType"
          },
          {
            "line_number": 12,
            "content": "from urllib.parse import quote as _url_quote"
          },
          {
            "line_number": 13,
            "content": ""
          },
          {
            "line_number": 14,
            "content": "import click"
          },
          {
            "line_number": 15,
            "content": "from werkzeug.datastructures import Headers"
          },
          {
            "line_number": 16,
            "content": "from werkzeug.datastructures import ImmutableDict"
          },
          {
            "line_number": 17,
            "content": "from werkzeug.exceptions import BadRequestKeyError"
          },
          {
            "line_number": 18,
            "content": "from werkzeug.exceptions import HTTPException"
          },
          {
            "line_number": 19,
            "content": "from werkzeug.exceptions import InternalServerError"
          },
          {
            "line_number": 20,
            "content": "from werkzeug.routing import BuildError"
          },
          {
            "line_number": 21,
            "content": "from werkzeug.routing import MapAdapter"
          },
          {
            "line_number": 22,
            "content": "from werkzeug.routing import RequestRedirect"
          },
          {
            "line_number": 23,
            "content": "from werkzeug.routing import RoutingException"
          },
          {
            "line_number": 24,
            "content": "from werkzeug.routing import Rule"
          },
          {
            "line_number": 25,
            "content": "from werkzeug.serving import is_running_from_reloader"
          },
          {
            "line_number": 26,
            "content": "from werkzeug.wrappers import Response as BaseResponse"
          },
          {
            "line_number": 27,
            "content": "from werkzeug.wsgi import get_host"
          },
          {
            "line_number": 28,
            "content": ""
          },
          {
            "line_number": 29,
            "content": "from . import cli"
          },
          {
            "line_number": 30,
            "content": "from . import typing as ft"
          },
          {
            "line_number": 31,
            "content": "from .ctx import AppContext"
          },
          {
            "line_number": 32,
            "content": "from .ctx import RequestContext"
          },
          {
            "line_number": 33,
            "content": "from .globals import _cv_app"
          },
          {
            "line_number": 34,
            "content": "from .globals import _cv_request"
          },
          {
            "line_number": 35,
            "content": "from .globals import current_app"
          },
          {
            "line_number": 36,
            "content": "from .globals import g"
          },
          {
            "line_number": 37,
            "content": "from .globals import request"
          },
          {
            "line_number": 38,
            "content": "from .globals import request_ctx"
          },
          {
            "line_number": 39,
            "content": "from .globals import session"
          },
          {
            "line_number": 40,
            "content": "from .helpers import get_debug_flag"
          },
          {
            "line_number": 41,
            "content": "from .helpers import get_flashed_messages"
          },
          {
            "line_number": 42,
            "content": "from .helpers import get_load_dotenv"
          },
          {
            "line_number": 43,
            "content": "from .helpers import send_from_directory"
          },
          {
            "line_number": 44,
            "content": "from .sansio.app import App"
          },
          {
            "line_number": 45,
            "content": "from .sansio.scaffold import _sentinel"
          },
          {
            "line_number": 46,
            "content": "from .sessions import SecureCookieSessionInterface"
          },
          {
            "line_number": 47,
            "content": "from .sessions import SessionInterface"
          },
          {
            "line_number": 48,
            "content": "from .signals import appcontext_tearing_down"
          },
          {
            "line_number": 49,
            "content": "from .signals import got_request_exception"
          },
          {
            "line_number": 50,
            "content": "from .signals import request_finished"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "src/flask/app.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "symbol:src/flask/app.py:Flask.__init__:310",
      "confidence_trigger": 0.77,
      "output_size_tokens": 880,
      "result": {
        "status": "ok",
        "file_path": "src/flask/app.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 1536,
        "lines": [
          {
            "line_number": 1,
            "content": "from __future__ import annotations"
          },
          {
            "line_number": 2,
            "content": ""
          },
          {
            "line_number": 3,
            "content": "import collections.abc as cabc"
          },
          {
            "line_number": 4,
            "content": "import os"
          },
          {
            "line_number": 5,
            "content": "import sys"
          },
          {
            "line_number": 6,
            "content": "import typing as t"
          },
          {
            "line_number": 7,
            "content": "import weakref"
          },
          {
            "line_number": 8,
            "content": "from datetime import timedelta"
          },
          {
            "line_number": 9,
            "content": "from inspect import iscoroutinefunction"
          },
          {
            "line_number": 10,
            "content": "from itertools import chain"
          },
          {
            "line_number": 11,
            "content": "from types import TracebackType"
          },
          {
            "line_number": 12,
            "content": "from urllib.parse import quote as _url_quote"
          },
          {
            "line_number": 13,
            "content": ""
          },
          {
            "line_number": 14,
            "content": "import click"
          },
          {
            "line_number": 15,
            "content": "from werkzeug.datastructures import Headers"
          },
          {
            "line_number": 16,
            "content": "from werkzeug.datastructures import ImmutableDict"
          },
          {
            "line_number": 17,
            "content": "from werkzeug.exceptions import BadRequestKeyError"
          },
          {
            "line_number": 18,
            "content": "from werkzeug.exceptions import HTTPException"
          },
          {
            "line_number": 19,
            "content": "from werkzeug.exceptions import InternalServerError"
          },
          {
            "line_number": 20,
            "content": "from werkzeug.routing import BuildError"
          },
          {
            "line_number": 21,
            "content": "from werkzeug.routing import MapAdapter"
          },
          {
            "line_number": 22,
            "content": "from werkzeug.routing import RequestRedirect"
          },
          {
            "line_number": 23,
            "content": "from werkzeug.routing import RoutingException"
          },
          {
            "line_number": 24,
            "content": "from werkzeug.routing import Rule"
          },
          {
            "line_number": 25,
            "content": "from werkzeug.serving import is_running_from_reloader"
          },
          {
            "line_number": 26,
            "content": "from werkzeug.wrappers import Response as BaseResponse"
          },
          {
            "line_number": 27,
            "content": "from werkzeug.wsgi import get_host"
          },
          {
            "line_number": 28,
            "content": ""
          },
          {
            "line_number": 29,
            "content": "from . import cli"
          },
          {
            "line_number": 30,
            "content": "from . import typing as ft"
          },
          {
            "line_number": 31,
            "content": "from .ctx import AppContext"
          },
          {
            "line_number": 32,
            "content": "from .ctx import RequestContext"
          },
          {
            "line_number": 33,
            "content": "from .globals import _cv_app"
          },
          {
            "line_number": 34,
            "content": "from .globals import _cv_request"
          },
          {
            "line_number": 35,
            "content": "from .globals import current_app"
          },
          {
            "line_number": 36,
            "content": "from .globals import g"
          },
          {
            "line_number": 37,
            "content": "from .globals import request"
          },
          {
            "line_number": 38,
            "content": "from .globals import request_ctx"
          },
          {
            "line_number": 39,
            "content": "from .globals import session"
          },
          {
            "line_number": 40,
            "content": "from .helpers import get_debug_flag"
          },
          {
            "line_number": 41,
            "content": "from .helpers import get_flashed_messages"
          },
          {
            "line_number": 42,
            "content": "from .helpers import get_load_dotenv"
          },
          {
            "line_number": 43,
            "content": "from .helpers import send_from_directory"
          },
          {
            "line_number": 44,
            "content": "from .sansio.app import App"
          },
          {
            "line_number": 45,
            "content": "from .sansio.scaffold import _sentinel"
          },
          {
            "line_number": 46,
            "content": "from .sessions import SecureCookieSessionInterface"
          },
          {
            "line_number": 47,
            "content": "from .sessions import SessionInterface"
          },
          {
            "line_number": 48,
            "content": "from .signals import appcontext_tearing_down"
          },
          {
            "line_number": 49,
            "content": "from .signals import got_request_exception"
          },
          {
            "line_number": 50,
            "content": "from .signals import request_finished"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "src/flask/app.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "symbol:src/flask/app.py:Flask.__init_subclass__:254",
      "confidence_trigger": 0.77,
      "output_size_tokens": 880,
      "result": {
        "status": "ok",
        "file_path": "src/flask/app.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 1536,
        "lines": [
          {
            "line_number": 1,
            "content": "from __future__ import annotations"
          },
          {
            "line_number": 2,
            "content": ""
          },
          {
            "line_number": 3,
            "content": "import collections.abc as cabc"
          },
          {
            "line_number": 4,
            "content": "import os"
          },
          {
            "line_number": 5,
            "content": "import sys"
          },
          {
            "line_number": 6,
            "content": "import typing as t"
          },
          {
            "line_number": 7,
            "content": "import weakref"
          },
          {
            "line_number": 8,
            "content": "from datetime import timedelta"
          },
          {
            "line_number": 9,
            "content": "from inspect import iscoroutinefunction"
          },
          {
            "line_number": 10,
            "content": "from itertools import chain"
          },
          {
            "line_number": 11,
            "content": "from types import TracebackType"
          },
          {
            "line_number": 12,
            "content": "from urllib.parse import quote as _url_quote"
          },
          {
            "line_number": 13,
            "content": ""
          },
          {
            "line_number": 14,
            "content": "import click"
          },
          {
            "line_number": 15,
            "content": "from werkzeug.datastructures import Headers"
          },
          {
            "line_number": 16,
            "content": "from werkzeug.datastructures import ImmutableDict"
          },
          {
            "line_number": 17,
            "content": "from werkzeug.exceptions import BadRequestKeyError"
          },
          {
            "line_number": 18,
            "content": "from werkzeug.exceptions import HTTPException"
          },
          {
            "line_number": 19,
            "content": "from werkzeug.exceptions import InternalServerError"
          },
          {
            "line_number": 20,
            "content": "from werkzeug.routing import BuildError"
          },
          {
            "line_number": 21,
            "content": "from werkzeug.routing import MapAdapter"
          },
          {
            "line_number": 22,
            "content": "from werkzeug.routing import RequestRedirect"
          },
          {
            "line_number": 23,
            "content": "from werkzeug.routing import RoutingException"
          },
          {
            "line_number": 24,
            "content": "from werkzeug.routing import Rule"
          },
          {
            "line_number": 25,
            "content": "from werkzeug.serving import is_running_from_reloader"
          },
          {
            "line_number": 26,
            "content": "from werkzeug.wrappers import Response as BaseResponse"
          },
          {
            "line_number": 27,
            "content": "from werkzeug.wsgi import get_host"
          },
          {
            "line_number": 28,
            "content": ""
          },
          {
            "line_number": 29,
            "content": "from . import cli"
          },
          {
            "line_number": 30,
            "content": "from . import typing as ft"
          },
          {
            "line_number": 31,
            "content": "from .ctx import AppContext"
          },
          {
            "line_number": 32,
            "content": "from .ctx import RequestContext"
          },
          {
            "line_number": 33,
            "content": "from .globals import _cv_app"
          },
          {
            "line_number": 34,
            "content": "from .globals import _cv_request"
          },
          {
            "line_number": 35,
            "content": "from .globals import current_app"
          },
          {
            "line_number": 36,
            "content": "from .globals import g"
          },
          {
            "line_number": 37,
            "content": "from .globals import request"
          },
          {
            "line_number": 38,
            "content": "from .globals import request_ctx"
          },
          {
            "line_number": 39,
            "content": "from .globals import session"
          },
          {
            "line_number": 40,
            "content": "from .helpers import get_debug_flag"
          },
          {
            "line_number": 41,
            "content": "from .helpers import get_flashed_messages"
          },
          {
            "line_number": 42,
            "content": "from .helpers import get_load_dotenv"
          },
          {
            "line_number": 43,
            "content": "from .helpers import send_from_directory"
          },
          {
            "line_number": 44,
            "content": "from .sansio.app import App"
          },
          {
            "line_number": 45,
            "content": "from .sansio.scaffold import _sentinel"
          },
          {
            "line_number": 46,
            "content": "from .sessions import SecureCookieSessionInterface"
          },
          {
            "line_number": 47,
            "content": "from .sessions import SessionInterface"
          },
          {
            "line_number": 48,
            "content": "from .signals import appcontext_tearing_down"
          },
          {
            "line_number": 49,
            "content": "from .signals import got_request_exception"
          },
          {
            "line_number": 50,
            "content": "from .signals import request_finished"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "src/flask/app.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "symbol:src/flask/app.py:Flask.async_to_sync:1079",
      "confidence_trigger": 0.77,
      "output_size_tokens": 880,
      "result": {
        "status": "ok",
        "file_path": "src/flask/app.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 1536,
        "lines": [
          {
            "line_number": 1,
            "content": "from __future__ import annotations"
          },
          {
            "line_number": 2,
            "content": ""
          },
          {
            "line_number": 3,
            "content": "import collections.abc as cabc"
          },
          {
            "line_number": 4,
            "content": "import os"
          },
          {
            "line_number": 5,
            "content": "import sys"
          },
          {
            "line_number": 6,
            "content": "import typing as t"
          },
          {
            "line_number": 7,
            "content": "import weakref"
          },
          {
            "line_number": 8,
            "content": "from datetime import timedelta"
          },
          {
            "line_number": 9,
            "content": "from inspect import iscoroutinefunction"
          },
          {
            "line_number": 10,
            "content": "from itertools import chain"
          },
          {
            "line_number": 11,
            "content": "from types import TracebackType"
          },
          {
            "line_number": 12,
            "content": "from urllib.parse import quote as _url_quote"
          },
          {
            "line_number": 13,
            "content": ""
          },
          {
            "line_number": 14,
            "content": "import click"
          },
          {
            "line_number": 15,
            "content": "from werkzeug.datastructures import Headers"
          },
          {
            "line_number": 16,
            "content": "from werkzeug.datastructures import ImmutableDict"
          },
          {
            "line_number": 17,
            "content": "from werkzeug.exceptions import BadRequestKeyError"
          },
          {
            "line_number": 18,
            "content": "from werkzeug.exceptions import HTTPException"
          },
          {
            "line_number": 19,
            "content": "from werkzeug.exceptions import InternalServerError"
          },
          {
            "line_number": 20,
            "content": "from werkzeug.routing import BuildError"
          },
          {
            "line_number": 21,
            "content": "from werkzeug.routing import MapAdapter"
          },
          {
            "line_number": 22,
            "content": "from werkzeug.routing import RequestRedirect"
          },
          {
            "line_number": 23,
            "content": "from werkzeug.routing import RoutingException"
          },
          {
            "line_number": 24,
            "content": "from werkzeug.routing import Rule"
          },
          {
            "line_number": 25,
            "content": "from werkzeug.serving import is_running_from_reloader"
          },
          {
            "line_number": 26,
            "content": "from werkzeug.wrappers import Response as BaseResponse"
          },
          {
            "line_number": 27,
            "content": "from werkzeug.wsgi import get_host"
          },
          {
            "line_number": 28,
            "content": ""
          },
          {
            "line_number": 29,
            "content": "from . import cli"
          },
          {
            "line_number": 30,
            "content": "from . import typing as ft"
          },
          {
            "line_number": 31,
            "content": "from .ctx import AppContext"
          },
          {
            "line_number": 32,
            "content": "from .ctx import RequestContext"
          },
          {
            "line_number": 33,
            "content": "from .globals import _cv_app"
          },
          {
            "line_number": 34,
            "content": "from .globals import _cv_request"
          },
          {
            "line_number": 35,
            "content": "from .globals import current_app"
          },
          {
            "line_number": 36,
            "content": "from .globals import g"
          },
          {
            "line_number": 37,
            "content": "from .globals import request"
          },
          {
            "line_number": 38,
            "content": "from .globals import request_ctx"
          },
          {
            "line_number": 39,
            "content": "from .globals import session"
          },
          {
            "line_number": 40,
            "content": "from .helpers import get_debug_flag"
          },
          {
            "line_number": 41,
            "content": "from .helpers import get_flashed_messages"
          },
          {
            "line_number": 42,
            "content": "from .helpers import get_load_dotenv"
          },
          {
            "line_number": 43,
            "content": "from .helpers import send_from_directory"
          },
          {
            "line_number": 44,
            "content": "from .sansio.app import App"
          },
          {
            "line_number": 45,
            "content": "from .sansio.scaffold import _sentinel"
          },
          {
            "line_number": 46,
            "content": "from .sessions import SecureCookieSessionInterface"
          },
          {
            "line_number": 47,
            "content": "from .sessions import SessionInterface"
          },
          {
            "line_number": 48,
            "content": "from .signals import appcontext_tearing_down"
          },
          {
            "line_number": 49,
            "content": "from .signals import got_request_exception"
          },
          {
            "line_number": 50,
            "content": "from .signals import request_finished"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "src/flask/app.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "symbol:src/flask/app.py:Flask.create_url_adapter:509",
      "confidence_trigger": 0.77,
      "output_size_tokens": 880,
      "result": {
        "status": "ok",
        "file_path": "src/flask/app.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 1536,
        "lines": [
          {
            "line_number": 1,
            "content": "from __future__ import annotations"
          },
          {
            "line_number": 2,
            "content": ""
          },
          {
            "line_number": 3,
            "content": "import collections.abc as cabc"
          },
          {
            "line_number": 4,
            "content": "import os"
          },
          {
            "line_number": 5,
            "content": "import sys"
          },
          {
            "line_number": 6,
            "content": "import typing as t"
          },
          {
            "line_number": 7,
            "content": "import weakref"
          },
          {
            "line_number": 8,
            "content": "from datetime import timedelta"
          },
          {
            "line_number": 9,
            "content": "from inspect import iscoroutinefunction"
          },
          {
            "line_number": 10,
            "content": "from itertools import chain"
          },
          {
            "line_number": 11,
            "content": "from types import TracebackType"
          },
          {
            "line_number": 12,
            "content": "from urllib.parse import quote as _url_quote"
          },
          {
            "line_number": 13,
            "content": ""
          },
          {
            "line_number": 14,
            "content": "import click"
          },
          {
            "line_number": 15,
            "content": "from werkzeug.datastructures import Headers"
          },
          {
            "line_number": 16,
            "content": "from werkzeug.datastructures import ImmutableDict"
          },
          {
            "line_number": 17,
            "content": "from werkzeug.exceptions import BadRequestKeyError"
          },
          {
            "line_number": 18,
            "content": "from werkzeug.exceptions import HTTPException"
          },
          {
            "line_number": 19,
            "content": "from werkzeug.exceptions import InternalServerError"
          },
          {
            "line_number": 20,
            "content": "from werkzeug.routing import BuildError"
          },
          {
            "line_number": 21,
            "content": "from werkzeug.routing import MapAdapter"
          },
          {
            "line_number": 22,
            "content": "from werkzeug.routing import RequestRedirect"
          },
          {
            "line_number": 23,
            "content": "from werkzeug.routing import RoutingException"
          },
          {
            "line_number": 24,
            "content": "from werkzeug.routing import Rule"
          },
          {
            "line_number": 25,
            "content": "from werkzeug.serving import is_running_from_reloader"
          },
          {
            "line_number": 26,
            "content": "from werkzeug.wrappers import Response as BaseResponse"
          },
          {
            "line_number": 27,
            "content": "from werkzeug.wsgi import get_host"
          },
          {
            "line_number": 28,
            "content": ""
          },
          {
            "line_number": 29,
            "content": "from . import cli"
          },
          {
            "line_number": 30,
            "content": "from . import typing as ft"
          },
          {
            "line_number": 31,
            "content": "from .ctx import AppContext"
          },
          {
            "line_number": 32,
            "content": "from .ctx import RequestContext"
          },
          {
            "line_number": 33,
            "content": "from .globals import _cv_app"
          },
          {
            "line_number": 34,
            "content": "from .globals import _cv_request"
          },
          {
            "line_number": 35,
            "content": "from .globals import current_app"
          },
          {
            "line_number": 36,
            "content": "from .globals import g"
          },
          {
            "line_number": 37,
            "content": "from .globals import request"
          },
          {
            "line_number": 38,
            "content": "from .globals import request_ctx"
          },
          {
            "line_number": 39,
            "content": "from .globals import session"
          },
          {
            "line_number": 40,
            "content": "from .helpers import get_debug_flag"
          },
          {
            "line_number": 41,
            "content": "from .helpers import get_flashed_messages"
          },
          {
            "line_number": 42,
            "content": "from .helpers import get_load_dotenv"
          },
          {
            "line_number": 43,
            "content": "from .helpers import send_from_directory"
          },
          {
            "line_number": 44,
            "content": "from .sansio.app import App"
          },
          {
            "line_number": 45,
            "content": "from .sansio.scaffold import _sentinel"
          },
          {
            "line_number": 46,
            "content": "from .sessions import SecureCookieSessionInterface"
          },
          {
            "line_number": 47,
            "content": "from .sessions import SessionInterface"
          },
          {
            "line_number": 48,
            "content": "from .signals import appcontext_tearing_down"
          },
          {
            "line_number": 49,
            "content": "from .signals import got_request_exception"
          },
          {
            "line_number": 50,
            "content": "from .signals import request_finished"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "src/flask/app.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "symbol:src/flask/app.py:Flask.dispatch_request:966",
      "confidence_trigger": 0.57,
      "output_size_tokens": 880,
      "result": {
        "status": "ok",
        "file_path": "src/flask/app.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 1536,
        "lines": [
          {
            "line_number": 1,
            "content": "from __future__ import annotations"
          },
          {
            "line_number": 2,
            "content": ""
          },
          {
            "line_number": 3,
            "content": "import collections.abc as cabc"
          },
          {
            "line_number": 4,
            "content": "import os"
          },
          {
            "line_number": 5,
            "content": "import sys"
          },
          {
            "line_number": 6,
            "content": "import typing as t"
          },
          {
            "line_number": 7,
            "content": "import weakref"
          },
          {
            "line_number": 8,
            "content": "from datetime import timedelta"
          },
          {
            "line_number": 9,
            "content": "from inspect import iscoroutinefunction"
          },
          {
            "line_number": 10,
            "content": "from itertools import chain"
          },
          {
            "line_number": 11,
            "content": "from types import TracebackType"
          },
          {
            "line_number": 12,
            "content": "from urllib.parse import quote as _url_quote"
          },
          {
            "line_number": 13,
            "content": ""
          },
          {
            "line_number": 14,
            "content": "import click"
          },
          {
            "line_number": 15,
            "content": "from werkzeug.datastructures import Headers"
          },
          {
            "line_number": 16,
            "content": "from werkzeug.datastructures import ImmutableDict"
          },
          {
            "line_number": 17,
            "content": "from werkzeug.exceptions import BadRequestKeyError"
          },
          {
            "line_number": 18,
            "content": "from werkzeug.exceptions import HTTPException"
          },
          {
            "line_number": 19,
            "content": "from werkzeug.exceptions import InternalServerError"
          },
          {
            "line_number": 20,
            "content": "from werkzeug.routing import BuildError"
          },
          {
            "line_number": 21,
            "content": "from werkzeug.routing import MapAdapter"
          },
          {
            "line_number": 22,
            "content": "from werkzeug.routing import RequestRedirect"
          },
          {
            "line_number": 23,
            "content": "from werkzeug.routing import RoutingException"
          },
          {
            "line_number": 24,
            "content": "from werkzeug.routing import Rule"
          },
          {
            "line_number": 25,
            "content": "from werkzeug.serving import is_running_from_reloader"
          },
          {
            "line_number": 26,
            "content": "from werkzeug.wrappers import Response as BaseResponse"
          },
          {
            "line_number": 27,
            "content": "from werkzeug.wsgi import get_host"
          },
          {
            "line_number": 28,
            "content": ""
          },
          {
            "line_number": 29,
            "content": "from . import cli"
          },
          {
            "line_number": 30,
            "content": "from . import typing as ft"
          },
          {
            "line_number": 31,
            "content": "from .ctx import AppContext"
          },
          {
            "line_number": 32,
            "content": "from .ctx import RequestContext"
          },
          {
            "line_number": 33,
            "content": "from .globals import _cv_app"
          },
          {
            "line_number": 34,
            "content": "from .globals import _cv_request"
          },
          {
            "line_number": 35,
            "content": "from .globals import current_app"
          },
          {
            "line_number": 36,
            "content": "from .globals import g"
          },
          {
            "line_number": 37,
            "content": "from .globals import request"
          },
          {
            "line_number": 38,
            "content": "from .globals import request_ctx"
          },
          {
            "line_number": 39,
            "content": "from .globals import session"
          },
          {
            "line_number": 40,
            "content": "from .helpers import get_debug_flag"
          },
          {
            "line_number": 41,
            "content": "from .helpers import get_flashed_messages"
          },
          {
            "line_number": 42,
            "content": "from .helpers import get_load_dotenv"
          },
          {
            "line_number": 43,
            "content": "from .helpers import send_from_directory"
          },
          {
            "line_number": 44,
            "content": "from .sansio.app import App"
          },
          {
            "line_number": 45,
            "content": "from .sansio.scaffold import _sentinel"
          },
          {
            "line_number": 46,
            "content": "from .sessions import SecureCookieSessionInterface"
          },
          {
            "line_number": 47,
            "content": "from .sessions import SessionInterface"
          },
          {
            "line_number": 48,
            "content": "from .signals import appcontext_tearing_down"
          },
          {
            "line_number": 49,
            "content": "from .signals import got_request_exception"
          },
          {
            "line_number": 50,
            "content": "from .signals import request_finished"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "src/flask/app.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "symbol:src/flask/app.py:Flask.do_teardown_appcontext:1453",
      "confidence_trigger": 0.77,
      "output_size_tokens": 880,
      "result": {
        "status": "ok",
        "file_path": "src/flask/app.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 1536,
        "lines": [
          {
            "line_number": 1,
            "content": "from __future__ import annotations"
          },
          {
            "line_number": 2,
            "content": ""
          },
          {
            "line_number": 3,
            "content": "import collections.abc as cabc"
          },
          {
            "line_number": 4,
            "content": "import os"
          },
          {
            "line_number": 5,
            "content": "import sys"
          },
          {
            "line_number": 6,
            "content": "import typing as t"
          },
          {
            "line_number": 7,
            "content": "import weakref"
          },
          {
            "line_number": 8,
            "content": "from datetime import timedelta"
          },
          {
            "line_number": 9,
            "content": "from inspect import iscoroutinefunction"
          },
          {
            "line_number": 10,
            "content": "from itertools import chain"
          },
          {
            "line_number": 11,
            "content": "from types import TracebackType"
          },
          {
            "line_number": 12,
            "content": "from urllib.parse import quote as _url_quote"
          },
          {
            "line_number": 13,
            "content": ""
          },
          {
            "line_number": 14,
            "content": "import click"
          },
          {
            "line_number": 15,
            "content": "from werkzeug.datastructures import Headers"
          },
          {
            "line_number": 16,
            "content": "from werkzeug.datastructures import ImmutableDict"
          },
          {
            "line_number": 17,
            "content": "from werkzeug.exceptions import BadRequestKeyError"
          },
          {
            "line_number": 18,
            "content": "from werkzeug.exceptions import HTTPException"
          },
          {
            "line_number": 19,
            "content": "from werkzeug.exceptions import InternalServerError"
          },
          {
            "line_number": 20,
            "content": "from werkzeug.routing import BuildError"
          },
          {
            "line_number": 21,
            "content": "from werkzeug.routing import MapAdapter"
          },
          {
            "line_number": 22,
            "content": "from werkzeug.routing import RequestRedirect"
          },
          {
            "line_number": 23,
            "content": "from werkzeug.routing import RoutingException"
          },
          {
            "line_number": 24,
            "content": "from werkzeug.routing import Rule"
          },
          {
            "line_number": 25,
            "content": "from werkzeug.serving import is_running_from_reloader"
          },
          {
            "line_number": 26,
            "content": "from werkzeug.wrappers import Response as BaseResponse"
          },
          {
            "line_number": 27,
            "content": "from werkzeug.wsgi import get_host"
          },
          {
            "line_number": 28,
            "content": ""
          },
          {
            "line_number": 29,
            "content": "from . import cli"
          },
          {
            "line_number": 30,
            "content": "from . import typing as ft"
          },
          {
            "line_number": 31,
            "content": "from .ctx import AppContext"
          },
          {
            "line_number": 32,
            "content": "from .ctx import RequestContext"
          },
          {
            "line_number": 33,
            "content": "from .globals import _cv_app"
          },
          {
            "line_number": 34,
            "content": "from .globals import _cv_request"
          },
          {
            "line_number": 35,
            "content": "from .globals import current_app"
          },
          {
            "line_number": 36,
            "content": "from .globals import g"
          },
          {
            "line_number": 37,
            "content": "from .globals import request"
          },
          {
            "line_number": 38,
            "content": "from .globals import request_ctx"
          },
          {
            "line_number": 39,
            "content": "from .globals import session"
          },
          {
            "line_number": 40,
            "content": "from .helpers import get_debug_flag"
          },
          {
            "line_number": 41,
            "content": "from .helpers import get_flashed_messages"
          },
          {
            "line_number": 42,
            "content": "from .helpers import get_load_dotenv"
          },
          {
            "line_number": 43,
            "content": "from .helpers import send_from_directory"
          },
          {
            "line_number": 44,
            "content": "from .sansio.app import App"
          },
          {
            "line_number": 45,
            "content": "from .sansio.scaffold import _sentinel"
          },
          {
            "line_number": 46,
            "content": "from .sessions import SecureCookieSessionInterface"
          },
          {
            "line_number": 47,
            "content": "from .sessions import SessionInterface"
          },
          {
            "line_number": 48,
            "content": "from .signals import appcontext_tearing_down"
          },
          {
            "line_number": 49,
            "content": "from .signals import got_request_exception"
          },
          {
            "line_number": 50,
            "content": "from .signals import request_finished"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "src/flask/app.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "symbol:src/flask/app.py:Flask.do_teardown_request:1420",
      "confidence_trigger": 0.77,
      "output_size_tokens": 880,
      "result": {
        "status": "ok",
        "file_path": "src/flask/app.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 1536,
        "lines": [
          {
            "line_number": 1,
            "content": "from __future__ import annotations"
          },
          {
            "line_number": 2,
            "content": ""
          },
          {
            "line_number": 3,
            "content": "import collections.abc as cabc"
          },
          {
            "line_number": 4,
            "content": "import os"
          },
          {
            "line_number": 5,
            "content": "import sys"
          },
          {
            "line_number": 6,
            "content": "import typing as t"
          },
          {
            "line_number": 7,
            "content": "import weakref"
          },
          {
            "line_number": 8,
            "content": "from datetime import timedelta"
          },
          {
            "line_number": 9,
            "content": "from inspect import iscoroutinefunction"
          },
          {
            "line_number": 10,
            "content": "from itertools import chain"
          },
          {
            "line_number": 11,
            "content": "from types import TracebackType"
          },
          {
            "line_number": 12,
            "content": "from urllib.parse import quote as _url_quote"
          },
          {
            "line_number": 13,
            "content": ""
          },
          {
            "line_number": 14,
            "content": "import click"
          },
          {
            "line_number": 15,
            "content": "from werkzeug.datastructures import Headers"
          },
          {
            "line_number": 16,
            "content": "from werkzeug.datastructures import ImmutableDict"
          },
          {
            "line_number": 17,
            "content": "from werkzeug.exceptions import BadRequestKeyError"
          },
          {
            "line_number": 18,
            "content": "from werkzeug.exceptions import HTTPException"
          },
          {
            "line_number": 19,
            "content": "from werkzeug.exceptions import InternalServerError"
          },
          {
            "line_number": 20,
            "content": "from werkzeug.routing import BuildError"
          },
          {
            "line_number": 21,
            "content": "from werkzeug.routing import MapAdapter"
          },
          {
            "line_number": 22,
            "content": "from werkzeug.routing import RequestRedirect"
          },
          {
            "line_number": 23,
            "content": "from werkzeug.routing import RoutingException"
          },
          {
            "line_number": 24,
            "content": "from werkzeug.routing import Rule"
          },
          {
            "line_number": 25,
            "content": "from werkzeug.serving import is_running_from_reloader"
          },
          {
            "line_number": 26,
            "content": "from werkzeug.wrappers import Response as BaseResponse"
          },
          {
            "line_number": 27,
            "content": "from werkzeug.wsgi import get_host"
          },
          {
            "line_number": 28,
            "content": ""
          },
          {
            "line_number": 29,
            "content": "from . import cli"
          },
          {
            "line_number": 30,
            "content": "from . import typing as ft"
          },
          {
            "line_number": 31,
            "content": "from .ctx import AppContext"
          },
          {
            "line_number": 32,
            "content": "from .ctx import RequestContext"
          },
          {
            "line_number": 33,
            "content": "from .globals import _cv_app"
          },
          {
            "line_number": 34,
            "content": "from .globals import _cv_request"
          },
          {
            "line_number": 35,
            "content": "from .globals import current_app"
          },
          {
            "line_number": 36,
            "content": "from .globals import g"
          },
          {
            "line_number": 37,
            "content": "from .globals import request"
          },
          {
            "line_number": 38,
            "content": "from .globals import request_ctx"
          },
          {
            "line_number": 39,
            "content": "from .globals import session"
          },
          {
            "line_number": 40,
            "content": "from .helpers import get_debug_flag"
          },
          {
            "line_number": 41,
            "content": "from .helpers import get_flashed_messages"
          },
          {
            "line_number": 42,
            "content": "from .helpers import get_load_dotenv"
          },
          {
            "line_number": 43,
            "content": "from .helpers import send_from_directory"
          },
          {
            "line_number": 44,
            "content": "from .sansio.app import App"
          },
          {
            "line_number": 45,
            "content": "from .sansio.scaffold import _sentinel"
          },
          {
            "line_number": 46,
            "content": "from .sessions import SecureCookieSessionInterface"
          },
          {
            "line_number": 47,
            "content": "from .sessions import SessionInterface"
          },
          {
            "line_number": 48,
            "content": "from .signals import appcontext_tearing_down"
          },
          {
            "line_number": 49,
            "content": "from .signals import got_request_exception"
          },
          {
            "line_number": 50,
            "content": "from .signals import request_finished"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "src/flask/app.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "symbol:src/flask/app.py:Flask.ensure_sync:1065",
      "confidence_trigger": 0.77,
      "output_size_tokens": 880,
      "result": {
        "status": "ok",
        "file_path": "src/flask/app.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 1536,
        "lines": [
          {
            "line_number": 1,
            "content": "from __future__ import annotations"
          },
          {
            "line_number": 2,
            "content": ""
          },
          {
            "line_number": 3,
            "content": "import collections.abc as cabc"
          },
          {
            "line_number": 4,
            "content": "import os"
          },
          {
            "line_number": 5,
            "content": "import sys"
          },
          {
            "line_number": 6,
            "content": "import typing as t"
          },
          {
            "line_number": 7,
            "content": "import weakref"
          },
          {
            "line_number": 8,
            "content": "from datetime import timedelta"
          },
          {
            "line_number": 9,
            "content": "from inspect import iscoroutinefunction"
          },
          {
            "line_number": 10,
            "content": "from itertools import chain"
          },
          {
            "line_number": 11,
            "content": "from types import TracebackType"
          },
          {
            "line_number": 12,
            "content": "from urllib.parse import quote as _url_quote"
          },
          {
            "line_number": 13,
            "content": ""
          },
          {
            "line_number": 14,
            "content": "import click"
          },
          {
            "line_number": 15,
            "content": "from werkzeug.datastructures import Headers"
          },
          {
            "line_number": 16,
            "content": "from werkzeug.datastructures import ImmutableDict"
          },
          {
            "line_number": 17,
            "content": "from werkzeug.exceptions import BadRequestKeyError"
          },
          {
            "line_number": 18,
            "content": "from werkzeug.exceptions import HTTPException"
          },
          {
            "line_number": 19,
            "content": "from werkzeug.exceptions import InternalServerError"
          },
          {
            "line_number": 20,
            "content": "from werkzeug.routing import BuildError"
          },
          {
            "line_number": 21,
            "content": "from werkzeug.routing import MapAdapter"
          },
          {
            "line_number": 22,
            "content": "from werkzeug.routing import RequestRedirect"
          },
          {
            "line_number": 23,
            "content": "from werkzeug.routing import RoutingException"
          },
          {
            "line_number": 24,
            "content": "from werkzeug.routing import Rule"
          },
          {
            "line_number": 25,
            "content": "from werkzeug.serving import is_running_from_reloader"
          },
          {
            "line_number": 26,
            "content": "from werkzeug.wrappers import Response as BaseResponse"
          },
          {
            "line_number": 27,
            "content": "from werkzeug.wsgi import get_host"
          },
          {
            "line_number": 28,
            "content": ""
          },
          {
            "line_number": 29,
            "content": "from . import cli"
          },
          {
            "line_number": 30,
            "content": "from . import typing as ft"
          },
          {
            "line_number": 31,
            "content": "from .ctx import AppContext"
          },
          {
            "line_number": 32,
            "content": "from .ctx import RequestContext"
          },
          {
            "line_number": 33,
            "content": "from .globals import _cv_app"
          },
          {
            "line_number": 34,
            "content": "from .globals import _cv_request"
          },
          {
            "line_number": 35,
            "content": "from .globals import current_app"
          },
          {
            "line_number": 36,
            "content": "from .globals import g"
          },
          {
            "line_number": 37,
            "content": "from .globals import request"
          },
          {
            "line_number": 38,
            "content": "from .globals import request_ctx"
          },
          {
            "line_number": 39,
            "content": "from .globals import session"
          },
          {
            "line_number": 40,
            "content": "from .helpers import get_debug_flag"
          },
          {
            "line_number": 41,
            "content": "from .helpers import get_flashed_messages"
          },
          {
            "line_number": 42,
            "content": "from .helpers import get_load_dotenv"
          },
          {
            "line_number": 43,
            "content": "from .helpers import send_from_directory"
          },
          {
            "line_number": 44,
            "content": "from .sansio.app import App"
          },
          {
            "line_number": 45,
            "content": "from .sansio.scaffold import _sentinel"
          },
          {
            "line_number": 46,
            "content": "from .sessions import SecureCookieSessionInterface"
          },
          {
            "line_number": 47,
            "content": "from .sessions import SessionInterface"
          },
          {
            "line_number": 48,
            "content": "from .signals import appcontext_tearing_down"
          },
          {
            "line_number": 49,
            "content": "from .signals import got_request_exception"
          },
          {
            "line_number": 50,
            "content": "from .signals import request_finished"
          }
        ]
      }
    }
  ],
  "trace_file": "experiments\\reports\\external-drilldown\\batch-20260405-subagents-final\\flask-tf2-001\\traces\\trace-20260405T134643.jsonl"
}
