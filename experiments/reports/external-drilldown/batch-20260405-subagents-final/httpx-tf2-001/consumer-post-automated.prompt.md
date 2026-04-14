You are running the AFTER pass of a CodeClue drill-down evaluation.

Rules:
- Start from the same clue projection below.
- Use the automated MCP drill-down evidence below as your only post-clue evidence.
- Do NOT inspect any other source beyond what is included in this prompt.
- Produce a revised answer that clearly reflects what the drill-down changed.

Task ID: httpx-tf2-001
Family: TF2
Operation Family: OF2

Question:
If I change the Timeout class in _config.py to make all timeouts optional (default None), what components would break?

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
  "p_dependency_miss": 0.878049,
  "p_hallucination": 0.0,
  "code_density_risk": 0.333333,
  "confidence_overall": 0.081301,
  "lookup_decision_hint": "expanded_lookup",
  "operation_family": "OF2",
  "threshold": 0.9,
  "tool_call_budget": 15,
  "per_node_confidence": [
    {
      "node_id": "module:httpx/_client.py",
      "confidence": 0.65,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 88,
        "fan_out_z_score": 3.015,
        "cross_file_span_ratio": 0.033,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "resolve_dependency",
          "args": {
            "node_id": "module:httpx/_client.py",
            "depth": 2
          },
          "rationale": "69 outgoing edge(s) point to nodes outside this projection; dependency closure is incomplete"
        },
        {
          "tool": "code_slice",
          "args": {
            "file_path": "httpx/_client.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "module:httpx/_config.py",
      "confidence": 0.85,
      "tier": 1,
      "density_indicators": {
        "uses_reflection": false,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "decorator_depth": 0,
        "generic_type_param_count": 0,
        "fan_out": 15,
        "fan_out_z_score": -0.255,
        "cross_file_span_ratio": 0.033,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "resolve_dependency",
          "args": {
            "node_id": "module:httpx/_config.py",
            "depth": 2
          },
          "rationale": "15 outgoing edge(s) point to nodes outside this projection; dependency closure is incomplete"
        },
        {
          "tool": "code_slice",
          "args": {
            "file_path": "httpx/_config.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:httpx/_client.py:AsyncClient.__aenter__:1990",
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
        "fan_out_z_score": 1.843,
        "cross_file_span_ratio": 0.033,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "httpx/_client.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:httpx/_client.py:AsyncClient.__aexit__:2008",
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
        "fan_out_z_score": 1.843,
        "cross_file_span_ratio": 0.033,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "httpx/_client.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:httpx/_client.py:BaseClient._build_auth:445",
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
        "fan_out_z_score": -0.344,
        "cross_file_span_ratio": 0.033,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "httpx/_client.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475",
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
        "fan_out_z_score": 5.145,
        "cross_file_span_ratio": 0.033,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "httpx/_client.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:httpx/_client.py:BaseClient._build_request_auth:457",
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
        "fan_out_z_score": 1.028,
        "cross_file_span_ratio": 0.033,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "httpx/_client.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:httpx/_client.py:BaseClient._merge_cookies:413",
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
        "fan_out_z_score": -0.344,
        "cross_file_span_ratio": 0.033,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "httpx/_client.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:httpx/_client.py:BaseClient._merge_headers:424",
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
        "fan_out_z_score": -0.344,
        "cross_file_span_ratio": 0.033,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "httpx/_client.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:httpx/_client.py:BaseClient._merge_queryparams:433",
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
        "fan_out_z_score": -0.344,
        "cross_file_span_ratio": 0.033,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "httpx/_client.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:httpx/_client.py:BaseClient._merge_url:391",
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
        "fan_out_z_score": -0.344,
        "cross_file_span_ratio": 0.033,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "httpx/_client.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:httpx/_client.py:BaseClient._redirect_headers:546",
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
        "fan_out_z_score": 2.401,
        "cross_file_span_ratio": 0.033,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "httpx/_client.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:httpx/_client.py:BaseClient._redirect_method:494",
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
        "fan_out_z_score": -0.344,
        "cross_file_span_ratio": 0.033,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "httpx/_client.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:httpx/_client.py:BaseClient._redirect_stream:573",
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
        "fan_out_z_score": -0.344,
        "cross_file_span_ratio": 0.033,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "httpx/_client.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:httpx/_client.py:BaseClient._redirect_url:517",
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
        "fan_out_z_score": -0.344,
        "cross_file_span_ratio": 0.033,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "httpx/_client.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:httpx/_client.py:BaseClient.build_request:340",
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
        "fan_out_z_score": 5.145,
        "cross_file_span_ratio": 0.033,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "httpx/_client.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:httpx/_client.py:Client.__enter__:1275",
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
        "fan_out_z_score": 2.401,
        "cross_file_span_ratio": 0.033,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "httpx/_client.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:httpx/_client.py:Client.__exit__:1293",
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
        "fan_out_z_score": 2.401,
        "cross_file_span_ratio": 0.033,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "httpx/_client.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:httpx/_client.py:_is_https_redirect:62",
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
        "fan_out_z_score": 2.401,
        "cross_file_span_ratio": 0.033,
        "density_flag": true
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "httpx/_client.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:httpx/_client.py:_port_or_default:77",
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
        "fan_out_z_score": -0.344,
        "cross_file_span_ratio": 0.033,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "httpx/_client.py",
            "start_line": 1,
            "end_line": 50
          },
          "rationale": "Low confidence on this node; source verification recommended"
        }
      ]
    },
    {
      "node_id": "symbol:httpx/_client.py:_same_origin:83",
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
        "fan_out_z_score": 1.028,
        "cross_file_span_ratio": 0.033,
        "density_flag": false
      },
      "suggested_actions": [
        {
          "tool": "code_slice",
          "args": {
            "file_path": "httpx/_client.py",
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
      "edge_id": "calls:symbol:httpx/_client.py:AsyncClient.__aenter__:1990:symbol:httpx/_client.py:AsyncClient.__aenter__:1990:2002",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:httpx/_client.py:AsyncClient.__aenter__:1990:symbol:httpx/_client.py:AsyncClient.__aenter__:1990:2005",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:httpx/_client.py:AsyncClient.__aexit__:2008:symbol:httpx/_client.py:AsyncClient.__aexit__:2008:2016",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:httpx/_client.py:AsyncClient.__aexit__:2008:symbol:httpx/_client.py:AsyncClient.__aexit__:2008:2019",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_redirect_request:475:symbol:httpx/_client.py:BaseClient._redirect_headers:546:482",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_redirect_request:475:symbol:httpx/_client.py:BaseClient._redirect_method:494:480",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_redirect_request:475:symbol:httpx/_client.py:BaseClient._redirect_stream:573:483",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_redirect_request:475:symbol:httpx/_client.py:BaseClient._redirect_url:517:481",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_request_auth:457:symbol:httpx/_client.py:BaseClient._build_auth:445:463",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:httpx/_client.py:BaseClient._redirect_headers:546:symbol:httpx/_client.py:_is_https_redirect:62:553",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:httpx/_client.py:BaseClient._redirect_headers:546:symbol:httpx/_client.py:_same_origin:83:552",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:httpx/_client.py:BaseClient.build_request:340:symbol:httpx/_client.py:BaseClient._merge_cookies:413:368",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:httpx/_client.py:BaseClient.build_request:340:symbol:httpx/_client.py:BaseClient._merge_headers:424:367",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:httpx/_client.py:BaseClient.build_request:340:symbol:httpx/_client.py:BaseClient._merge_queryparams:433:369",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:httpx/_client.py:BaseClient.build_request:340:symbol:httpx/_client.py:BaseClient._merge_url:391:366",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:httpx/_client.py:Client.__enter__:1275:symbol:httpx/_client.py:Client.__enter__:1275:1287",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:httpx/_client.py:Client.__enter__:1275:symbol:httpx/_client.py:Client.__enter__:1275:1290",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:httpx/_client.py:Client.__exit__:1293:symbol:httpx/_client.py:Client.__exit__:1293:1301",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:httpx/_client.py:Client.__exit__:1293:symbol:httpx/_client.py:Client.__exit__:1293:1304",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:httpx/_client.py:_is_https_redirect:62:symbol:httpx/_client.py:_port_or_default:77:71",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:httpx/_client.py:_is_https_redirect:62:symbol:httpx/_client.py:_port_or_default:77:73",
      "confidence": 1.0,
      "suggested_actions": []
    },
    {
      "edge_id": "calls:symbol:httpx/_client.py:_same_origin:83:symbol:httpx/_client.py:_port_or_default:77:90",
      "confidence": 1.0,
      "suggested_actions": []
    }
  ]
}

## Projection Stats
{
  "seed_count": 19,
  "initial_seed_count": 18,
  "projected_node_count": 21,
  "projected_edge_count": 22,
  "graph_node_count": 1301,
  "graph_edge_count": 1557
}

## Projected Nodes
[
  {
    "node_id": "module:httpx/_client.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "httpx/_client.py",
      "byte_start": 0,
      "byte_end": 65713,
      "ast_path": "module",
      "content_hash": "ed717b3ac00debb48d089daeb4dd7fbaf47cb5642ebc4a6e76f3a2fc6cfc0f70"
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
      "symbol_name": "httpx/_client.py",
      "symbol_type": "module",
      "tier": 1
    },
    "confidence": 1.0
  },
  {
    "node_id": "module:httpx/_config.py",
    "node_type": "module",
    "source_anchor": {
      "file_path": "httpx/_config.py",
      "byte_start": 0,
      "byte_end": 8547,
      "ast_path": "module",
      "content_hash": "a4fa7653ec2271f70ab05f8a6111352d876dddee84446788a1767c1a3a372d67"
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
      "symbol_name": "httpx/_config.py",
      "symbol_type": "module",
      "tier": 1
    },
    "confidence": 1.0
  },
  {
    "node_id": "symbol:httpx/_client.py:AsyncClient.__aenter__:1990",
    "node_type": "async_function",
    "source_anchor": {
      "file_path": "httpx/_client.py",
      "byte_start": 64633,
      "byte_end": 65246,
      "ast_path": "async_function:AsyncClient.__aenter__",
      "content_hash": "b8ac29d32f1e6b712ba5edb5bd6151f0cac78bfceb5962ac0a6c1cc9e30ef035"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:httpx/_client.py:AsyncClient.__aenter__:1990"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:httpx/_client.py:AsyncClient.__aenter__:1990"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "async_function __aenter__",
      "symbol_name": "__aenter__",
      "symbol_type": "async_function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:httpx/_client.py:AsyncClient.__aexit__:2008",
    "node_type": "async_function",
    "source_anchor": {
      "file_path": "httpx/_client.py",
      "byte_start": 65252,
      "byte_end": 65712,
      "ast_path": "async_function:AsyncClient.__aexit__",
      "content_hash": "df3f6245719ec2c095df970e08d7176e180316c741d43f837bfd3459b111c0f1"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:httpx/_client.py:AsyncClient.__aexit__:2008"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:httpx/_client.py:AsyncClient.__aexit__:2008"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "async_function __aexit__",
      "symbol_name": "__aexit__",
      "symbol_type": "async_function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:httpx/_client.py:BaseClient._build_auth:445",
    "node_type": "function",
    "source_anchor": {
      "file_path": "httpx/_client.py",
      "byte_start": 13950,
      "byte_end": 14376,
      "ast_path": "function:BaseClient._build_auth",
      "content_hash": "02a93e6a831147cc4f74236ba77656d7c1740fd1ca20e4bb4d7952ea717d99fa"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:httpx/_client.py:BaseClient._build_request_auth:457"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _build_auth",
      "symbol_name": "_build_auth",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475",
    "node_type": "function",
    "source_anchor": {
      "file_path": "httpx/_client.py",
      "byte_start": 14905,
      "byte_end": 15613,
      "ast_path": "function:BaseClient._build_redirect_request",
      "content_hash": "2f18ca3d8f28ed472f5be8cdb9b71b82d8bd52d2e79bcdc1078d1a548f20cb3b"
    },
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:httpx/_client.py:BaseClient._redirect_headers:546"
        },
        {
          "is_external": false,
          "target": "symbol:httpx/_client.py:BaseClient._redirect_method:494"
        },
        {
          "is_external": false,
          "target": "symbol:httpx/_client.py:BaseClient._redirect_stream:573"
        },
        {
          "is_external": false,
          "target": "symbol:httpx/_client.py:BaseClient._redirect_url:517"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _build_redirect_request",
      "symbol_name": "_build_redirect_request",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:httpx/_client.py:BaseClient._build_request_auth:457",
    "node_type": "function",
    "source_anchor": {
      "file_path": "httpx/_client.py",
      "byte_start": 14382,
      "byte_end": 14899,
      "ast_path": "function:BaseClient._build_request_auth",
      "content_hash": "a36fdfdb8a23565858a9378f2e703770c1a0da5fdd3ad0e7d3f3d33aa7ebdfbb"
    },
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:httpx/_client.py:BaseClient._build_auth:445"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _build_request_auth",
      "symbol_name": "_build_request_auth",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:httpx/_client.py:BaseClient._merge_cookies:413",
    "node_type": "function",
    "source_anchor": {
      "file_path": "httpx/_client.py",
      "byte_start": 12700,
      "byte_end": 13129,
      "ast_path": "function:BaseClient._merge_cookies",
      "content_hash": "1113038edb11f328c3da9ff0737fe9f780a429460a2376c3f7c9a6e7fecf2065"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:httpx/_client.py:BaseClient.build_request:340"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _merge_cookies",
      "symbol_name": "_merge_cookies",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:httpx/_client.py:BaseClient._merge_headers:424",
    "node_type": "function",
    "source_anchor": {
      "file_path": "httpx/_client.py",
      "byte_start": 13135,
      "byte_end": 13493,
      "ast_path": "function:BaseClient._merge_headers",
      "content_hash": "25537640006a58dc76c2da64aac5facd7910975066fc55318cb5c5c9dd11c120"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:httpx/_client.py:BaseClient.build_request:340"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _merge_headers",
      "symbol_name": "_merge_headers",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:httpx/_client.py:BaseClient._merge_queryparams:433",
    "node_type": "function",
    "source_anchor": {
      "file_path": "httpx/_client.py",
      "byte_start": 13499,
      "byte_end": 13944,
      "ast_path": "function:BaseClient._merge_queryparams",
      "content_hash": "0d0c4af31563061b1d2fbc115bfcbb7524c3bbb087790b6526a1b50a6eba787f"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:httpx/_client.py:BaseClient.build_request:340"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _merge_queryparams",
      "symbol_name": "_merge_queryparams",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:httpx/_client.py:BaseClient._merge_url:391",
    "node_type": "function",
    "source_anchor": {
      "file_path": "httpx/_client.py",
      "byte_start": 11694,
      "byte_end": 12694,
      "ast_path": "function:BaseClient._merge_url",
      "content_hash": "1d1e4f3806a40f76acc927927b4b6bdca831222477e0eab8fdd34167e121f4f2"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:httpx/_client.py:BaseClient.build_request:340"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _merge_url",
      "symbol_name": "_merge_url",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:httpx/_client.py:BaseClient._redirect_headers:546",
    "node_type": "function",
    "source_anchor": {
      "file_path": "httpx/_client.py",
      "byte_start": 17588,
      "byte_end": 18720,
      "ast_path": "function:BaseClient._redirect_headers",
      "content_hash": "cf40c6f53f3e49b9f6ebbb8926efe85db5ade78f26439864f896d70bdc6c370c"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:httpx/_client.py:_is_https_redirect:62"
        },
        {
          "is_external": false,
          "target": "symbol:httpx/_client.py:_same_origin:83"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _redirect_headers",
      "symbol_name": "_redirect_headers",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:httpx/_client.py:BaseClient._redirect_method:494",
    "node_type": "function",
    "source_anchor": {
      "file_path": "httpx/_client.py",
      "byte_start": 15619,
      "byte_end": 16494,
      "ast_path": "function:BaseClient._redirect_method",
      "content_hash": "e421099e82483a433735e1e0a31c750e54ccf65d1b752dd063979f1c2dc7b5c9"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _redirect_method",
      "symbol_name": "_redirect_method",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:httpx/_client.py:BaseClient._redirect_stream:573",
    "node_type": "function",
    "source_anchor": {
      "file_path": "httpx/_client.py",
      "byte_start": 18726,
      "byte_end": 19047,
      "ast_path": "function:BaseClient._redirect_stream",
      "content_hash": "887fda7354d3216c1d4440b3bdb55abad50de782b6ba64b142887efb0abf4698"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _redirect_stream",
      "symbol_name": "_redirect_stream",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:httpx/_client.py:BaseClient._redirect_url:517",
    "node_type": "function",
    "source_anchor": {
      "file_path": "httpx/_client.py",
      "byte_start": 16500,
      "byte_end": 17582,
      "ast_path": "function:BaseClient._redirect_url",
      "content_hash": "c814d4dbfc61c2b4b85c30252d30f77e7e6962b60b5c16c079c4b2e8371af2b2"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _redirect_url",
      "symbol_name": "_redirect_url",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:httpx/_client.py:BaseClient.build_request:340",
    "node_type": "function",
    "source_anchor": {
      "file_path": "httpx/_client.py",
      "byte_start": 9995,
      "byte_end": 11688,
      "ast_path": "function:BaseClient.build_request",
      "content_hash": "ecc2854536373aa7c57c14514d27ebd94ebf501e18959262b6d2c44a83b27065"
    },
    "semantic_contract": {
      "called_by": [],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:httpx/_client.py:BaseClient._merge_cookies:413"
        },
        {
          "is_external": false,
          "target": "symbol:httpx/_client.py:BaseClient._merge_headers:424"
        },
        {
          "is_external": false,
          "target": "symbol:httpx/_client.py:BaseClient._merge_queryparams:433"
        },
        {
          "is_external": false,
          "target": "symbol:httpx/_client.py:BaseClient._merge_url:391"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function build_request",
      "symbol_name": "build_request",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:httpx/_client.py:Client.__enter__:1275",
    "node_type": "function",
    "source_anchor": {
      "file_path": "httpx/_client.py",
      "byte_start": 41285,
      "byte_end": 41889,
      "ast_path": "function:Client.__enter__",
      "content_hash": "cdf6c01eefdcbefac0f0755ed2749b0b8ecec6f17617580c4adb988c0fafb78b"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:httpx/_client.py:Client.__enter__:1275"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:httpx/_client.py:Client.__enter__:1275"
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
    "node_id": "symbol:httpx/_client.py:Client.__exit__:1293",
    "node_type": "function",
    "source_anchor": {
      "file_path": "httpx/_client.py",
      "byte_start": 41895,
      "byte_end": 42346,
      "ast_path": "function:Client.__exit__",
      "content_hash": "363d3668eeea67bf86466057131fecaa6cccb2bb20f1d6f3a49ce1e79e136129"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:httpx/_client.py:Client.__exit__:1293"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:httpx/_client.py:Client.__exit__:1293"
        }
      ],
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
    "node_id": "symbol:httpx/_client.py:_is_https_redirect:62",
    "node_type": "function",
    "source_anchor": {
      "file_path": "httpx/_client.py",
      "byte_start": 1536,
      "byte_end": 1897,
      "ast_path": "function:_is_https_redirect",
      "content_hash": "f7fb9a7652de2ee8be1892fda8abdd18c5cafef3f0b7cee910a997b0d2e3108d"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:httpx/_client.py:BaseClient._redirect_headers:546"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:httpx/_client.py:_port_or_default:77"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _is_https_redirect",
      "symbol_name": "_is_https_redirect",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:httpx/_client.py:_port_or_default:77",
    "node_type": "function",
    "source_anchor": {
      "file_path": "httpx/_client.py",
      "byte_start": 1900,
      "byte_end": 2052,
      "ast_path": "function:_port_or_default",
      "content_hash": "d70ff71cb4458c59da46b26ea655df1e7c87c40d139515e3a672f86942b86c83"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:httpx/_client.py:_is_https_redirect:62"
        },
        {
          "source": "symbol:httpx/_client.py:_same_origin:83"
        }
      ],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _port_or_default",
      "symbol_name": "_port_or_default",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  },
  {
    "node_id": "symbol:httpx/_client.py:_same_origin:83",
    "node_type": "function",
    "source_anchor": {
      "file_path": "httpx/_client.py",
      "byte_start": 2055,
      "byte_end": 2327,
      "ast_path": "function:_same_origin",
      "content_hash": "aac753c9500e9d229397f05548f971de5a63129de76236da0994c25179fad392"
    },
    "semantic_contract": {
      "called_by": [
        {
          "source": "symbol:httpx/_client.py:BaseClient._redirect_headers:546"
        }
      ],
      "calls": [
        {
          "is_external": false,
          "target": "symbol:httpx/_client.py:_port_or_default:77"
        }
      ],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "python",
      "purpose": "function _same_origin",
      "symbol_name": "_same_origin",
      "symbol_type": "function",
      "tier": 1
    },
    "confidence": 0.92
  }
]

## Projected Edges
[
  {
    "edge_id": "calls:symbol:httpx/_client.py:AsyncClient.__aenter__:1990:symbol:httpx/_client.py:AsyncClient.__aenter__:1990:2002",
    "edge_type": "calls",
    "from_node": "symbol:httpx/_client.py:AsyncClient.__aenter__:1990",
    "to_node": "symbol:httpx/_client.py:AsyncClient.__aenter__:1990",
    "evidence": {
      "line": 2002,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:AsyncClient.__aenter__:1990:symbol:httpx/_client.py:AsyncClient.__aenter__:1990:2005",
    "edge_type": "calls",
    "from_node": "symbol:httpx/_client.py:AsyncClient.__aenter__:1990",
    "to_node": "symbol:httpx/_client.py:AsyncClient.__aenter__:1990",
    "evidence": {
      "line": 2005,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:AsyncClient.__aexit__:2008:symbol:httpx/_client.py:AsyncClient.__aexit__:2008:2016",
    "edge_type": "calls",
    "from_node": "symbol:httpx/_client.py:AsyncClient.__aexit__:2008",
    "to_node": "symbol:httpx/_client.py:AsyncClient.__aexit__:2008",
    "evidence": {
      "line": 2016,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:AsyncClient.__aexit__:2008:symbol:httpx/_client.py:AsyncClient.__aexit__:2008:2019",
    "edge_type": "calls",
    "from_node": "symbol:httpx/_client.py:AsyncClient.__aexit__:2008",
    "to_node": "symbol:httpx/_client.py:AsyncClient.__aexit__:2008",
    "evidence": {
      "line": 2019,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_redirect_request:475:symbol:httpx/_client.py:BaseClient._redirect_headers:546:482",
    "edge_type": "calls",
    "from_node": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475",
    "to_node": "symbol:httpx/_client.py:BaseClient._redirect_headers:546",
    "evidence": {
      "line": 482,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_redirect_request:475:symbol:httpx/_client.py:BaseClient._redirect_method:494:480",
    "edge_type": "calls",
    "from_node": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475",
    "to_node": "symbol:httpx/_client.py:BaseClient._redirect_method:494",
    "evidence": {
      "line": 480,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_redirect_request:475:symbol:httpx/_client.py:BaseClient._redirect_stream:573:483",
    "edge_type": "calls",
    "from_node": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475",
    "to_node": "symbol:httpx/_client.py:BaseClient._redirect_stream:573",
    "evidence": {
      "line": 483,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_redirect_request:475:symbol:httpx/_client.py:BaseClient._redirect_url:517:481",
    "edge_type": "calls",
    "from_node": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475",
    "to_node": "symbol:httpx/_client.py:BaseClient._redirect_url:517",
    "evidence": {
      "line": 481,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_request_auth:457:symbol:httpx/_client.py:BaseClient._build_auth:445:463",
    "edge_type": "calls",
    "from_node": "symbol:httpx/_client.py:BaseClient._build_request_auth:457",
    "to_node": "symbol:httpx/_client.py:BaseClient._build_auth:445",
    "evidence": {
      "line": 463,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:BaseClient._redirect_headers:546:symbol:httpx/_client.py:_is_https_redirect:62:553",
    "edge_type": "calls",
    "from_node": "symbol:httpx/_client.py:BaseClient._redirect_headers:546",
    "to_node": "symbol:httpx/_client.py:_is_https_redirect:62",
    "evidence": {
      "line": 553,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:BaseClient._redirect_headers:546:symbol:httpx/_client.py:_same_origin:83:552",
    "edge_type": "calls",
    "from_node": "symbol:httpx/_client.py:BaseClient._redirect_headers:546",
    "to_node": "symbol:httpx/_client.py:_same_origin:83",
    "evidence": {
      "line": 552,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:BaseClient.build_request:340:symbol:httpx/_client.py:BaseClient._merge_cookies:413:368",
    "edge_type": "calls",
    "from_node": "symbol:httpx/_client.py:BaseClient.build_request:340",
    "to_node": "symbol:httpx/_client.py:BaseClient._merge_cookies:413",
    "evidence": {
      "line": 368,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:BaseClient.build_request:340:symbol:httpx/_client.py:BaseClient._merge_headers:424:367",
    "edge_type": "calls",
    "from_node": "symbol:httpx/_client.py:BaseClient.build_request:340",
    "to_node": "symbol:httpx/_client.py:BaseClient._merge_headers:424",
    "evidence": {
      "line": 367,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:BaseClient.build_request:340:symbol:httpx/_client.py:BaseClient._merge_queryparams:433:369",
    "edge_type": "calls",
    "from_node": "symbol:httpx/_client.py:BaseClient.build_request:340",
    "to_node": "symbol:httpx/_client.py:BaseClient._merge_queryparams:433",
    "evidence": {
      "line": 369,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:BaseClient.build_request:340:symbol:httpx/_client.py:BaseClient._merge_url:391:366",
    "edge_type": "calls",
    "from_node": "symbol:httpx/_client.py:BaseClient.build_request:340",
    "to_node": "symbol:httpx/_client.py:BaseClient._merge_url:391",
    "evidence": {
      "line": 366,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:Client.__enter__:1275:symbol:httpx/_client.py:Client.__enter__:1275:1287",
    "edge_type": "calls",
    "from_node": "symbol:httpx/_client.py:Client.__enter__:1275",
    "to_node": "symbol:httpx/_client.py:Client.__enter__:1275",
    "evidence": {
      "line": 1287,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:Client.__enter__:1275:symbol:httpx/_client.py:Client.__enter__:1275:1290",
    "edge_type": "calls",
    "from_node": "symbol:httpx/_client.py:Client.__enter__:1275",
    "to_node": "symbol:httpx/_client.py:Client.__enter__:1275",
    "evidence": {
      "line": 1290,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:Client.__exit__:1293:symbol:httpx/_client.py:Client.__exit__:1293:1301",
    "edge_type": "calls",
    "from_node": "symbol:httpx/_client.py:Client.__exit__:1293",
    "to_node": "symbol:httpx/_client.py:Client.__exit__:1293",
    "evidence": {
      "line": 1301,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:Client.__exit__:1293:symbol:httpx/_client.py:Client.__exit__:1293:1304",
    "edge_type": "calls",
    "from_node": "symbol:httpx/_client.py:Client.__exit__:1293",
    "to_node": "symbol:httpx/_client.py:Client.__exit__:1293",
    "evidence": {
      "line": 1304,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:_is_https_redirect:62:symbol:httpx/_client.py:_port_or_default:77:71",
    "edge_type": "calls",
    "from_node": "symbol:httpx/_client.py:_is_https_redirect:62",
    "to_node": "symbol:httpx/_client.py:_port_or_default:77",
    "evidence": {
      "line": 71,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:_is_https_redirect:62:symbol:httpx/_client.py:_port_or_default:77:73",
    "edge_type": "calls",
    "from_node": "symbol:httpx/_client.py:_is_https_redirect:62",
    "to_node": "symbol:httpx/_client.py:_port_or_default:77",
    "evidence": {
      "line": 73,
      "rel": "ast_call"
    }
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:_same_origin:83:symbol:httpx/_client.py:_port_or_default:77:90",
    "edge_type": "calls",
    "from_node": "symbol:httpx/_client.py:_same_origin:83",
    "to_node": "symbol:httpx/_client.py:_port_or_default:77",
    "evidence": {
      "line": 90,
      "rel": "ast_call"
    }
  }
]

## Automated MCP Drill-Down Results
{
  "task_id": "httpx-tf2-001",
  "repo_dir": "httpx",
  "operation_family": "OF2",
  "confidence_overall": 0.081301,
  "lookup_hint": "expanded_lookup",
  "projected_nodes": 21,
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
    "clue": 9834,
    "drill_down": 34631,
    "total": 44465,
    "raw_estimate": 142484
  },
  "etrr": 0.6879,
  "h7_pass": true,
  "tool_results": [
    {
      "tool": "resolve_dependency",
      "args": {
        "node_id": "module:httpx/_client.py",
        "depth": 2
      },
      "node_id": "module:httpx/_client.py",
      "confidence_trigger": 0.65,
      "output_size_tokens": 21503,
      "result": {
        "status": "ok",
        "seed_node": "module:httpx/_client.py",
        "depth": 2,
        "nodes": [
          {
            "node_id": "module:httpx/_client.py",
            "node_type": "module",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 0,
              "byte_end": 65713,
              "ast_path": "module",
              "content_hash": "ed717b3ac00debb48d089daeb4dd7fbaf47cb5642ebc4a6e76f3a2fc6cfc0f70"
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
              "symbol_name": "httpx/_client.py",
              "symbol_type": "module",
              "tier": 1
            },
            "confidence": 1.0
          },
          {
            "node_id": "symbol:httpx/_client.py:AsyncClient.__aenter__:1990",
            "node_type": "async_function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 64633,
              "byte_end": 65246,
              "ast_path": "async_function:AsyncClient.__aenter__",
              "content_hash": "b8ac29d32f1e6b712ba5edb5bd6151f0cac78bfceb5962ac0a6c1cc9e30ef035"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:httpx/_client.py:AsyncClient.__aenter__:1990"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:httpx/_client.py:AsyncClient.__aenter__:1990"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "async_function __aenter__",
              "symbol_name": "__aenter__",
              "symbol_type": "async_function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:AsyncClient.__aexit__:2008",
            "node_type": "async_function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 65252,
              "byte_end": 65712,
              "ast_path": "async_function:AsyncClient.__aexit__",
              "content_hash": "df3f6245719ec2c095df970e08d7176e180316c741d43f837bfd3459b111c0f1"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:httpx/_client.py:AsyncClient.__aexit__:2008"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:httpx/_client.py:AsyncClient.__aexit__:2008"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "async_function __aexit__",
              "symbol_name": "__aexit__",
              "symbol_type": "async_function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:AsyncClient.__init__:1353",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 44349,
              "byte_end": 47113,
              "ast_path": "function:AsyncClient.__init__",
              "content_hash": "38ec7cf2c09fb1940bf1bc4c2ce78d12623f4831dbf2239d4f01f1ce9a676a67"
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
            "node_id": "symbol:httpx/_client.py:AsyncClient._init_proxy_transport:1454",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 47731,
              "byte_end": 48273,
              "ast_path": "function:AsyncClient._init_proxy_transport",
              "content_hash": "c6c571fd0bf42de33407c04184a912db92707642c7c4373df008134c82d9f9fe"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _init_proxy_transport",
              "symbol_name": "_init_proxy_transport",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:AsyncClient._init_transport:1432",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 47119,
              "byte_end": 47725,
              "ast_path": "function:AsyncClient._init_transport",
              "content_hash": "85fb23af62dd157c94b69423f725325decb9f5266cc68eecc0c867b36d73d34f"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _init_transport",
              "symbol_name": "_init_transport",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:AsyncClient._send_handling_auth:1645",
            "node_type": "async_function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 53804,
              "byte_end": 54882,
              "ast_path": "async_function:AsyncClient._send_handling_auth",
              "content_hash": "0e45e92eaf2a2165385c4805b7dde1c7a6741edb64b0907e8f3c7d8874cf7feb"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "async_function _send_handling_auth",
              "symbol_name": "_send_handling_auth",
              "symbol_type": "async_function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:AsyncClient._send_handling_redirects:1679",
            "node_type": "async_function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 54888,
              "byte_end": 56086,
              "ast_path": "async_function:AsyncClient._send_handling_redirects",
              "content_hash": "75a4c41878aa2139e193c5a7efe3b73028f78f44ee1ee3aa71232efc7ce7a7bf"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "async_function _send_handling_redirects",
              "symbol_name": "_send_handling_redirects",
              "symbol_type": "async_function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:AsyncClient._send_single_request:1717",
            "node_type": "async_function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 56092,
              "byte_end": 57225,
              "ast_path": "async_function:AsyncClient._send_single_request",
              "content_hash": "8651e0ecb7a687e1544e90810355cfeea7ebd239474e5f2db12c0cbfa36c9f9c"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "async_function _send_single_request",
              "symbol_name": "_send_single_request",
              "symbol_type": "async_function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:AsyncClient._transport_for_url:1474",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 48279,
              "byte_end": 48710,
              "ast_path": "function:AsyncClient._transport_for_url",
              "content_hash": "bf8e3fbac98db5b2854fddd5ba61b08794036dcba4a6414731e0c93be396528b"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _transport_for_url",
              "symbol_name": "_transport_for_url",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:AsyncClient.aclose:1978",
            "node_type": "async_function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 64273,
              "byte_end": 64627,
              "ast_path": "async_function:AsyncClient.aclose",
              "content_hash": "9bd341591aeb7c37c89db982adc70eba68524840882940edb51302df70115c24"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "async_function aclose",
              "symbol_name": "aclose",
              "symbol_type": "async_function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:AsyncClient.delete:1949",
            "node_type": "async_function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 63380,
              "byte_end": 64267,
              "ast_path": "async_function:AsyncClient.delete",
              "content_hash": "db469412503d405949e2d1eba4a8e18e5dcdeb4430ef39287328c1f249dbb29d"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "async_function delete",
              "symbol_name": "delete",
              "symbol_type": "async_function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:AsyncClient.get:1751",
            "node_type": "async_function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 57231,
              "byte_end": 58116,
              "ast_path": "async_function:AsyncClient.get",
              "content_hash": "4a133868fefb4929bfd87d10b5bb05625c822c2aa3b1b1f3a796e4d1604febf0"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "async_function get",
              "symbol_name": "get",
              "symbol_type": "async_function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:AsyncClient.head:1809",
            "node_type": "async_function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 59019,
              "byte_end": 59900,
              "ast_path": "async_function:AsyncClient.head",
              "content_hash": "c2066067a76a7e1f41baab51be3993fccda055a567c8e6b4d453639dabfdd4da"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "async_function head",
              "symbol_name": "head",
              "symbol_type": "async_function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:AsyncClient.options:1780",
            "node_type": "async_function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 58122,
              "byte_end": 59013,
              "ast_path": "async_function:AsyncClient.options",
              "content_hash": "dba1b74b68bec4e34884c7b7f9e639c8dee0ab9df22a1fa13bdad13e5de37b31"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "async_function options",
              "symbol_name": "options",
              "symbol_type": "async_function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:AsyncClient.patch:1912",
            "node_type": "async_function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 62219,
              "byte_end": 63374,
              "ast_path": "async_function:AsyncClient.patch",
              "content_hash": "33649cd639a271d9ad156e480b99306835a52e0f61d8c89035debf68c452e57b"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "async_function patch",
              "symbol_name": "patch",
              "symbol_type": "async_function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:AsyncClient.post:1838",
            "node_type": "async_function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 59906,
              "byte_end": 61058,
              "ast_path": "async_function:AsyncClient.post",
              "content_hash": "01313fcdb9e3be6b8362051d2248eef8066e6f4868b9de89b8957a4ff518dbdd"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "async_function post",
              "symbol_name": "post",
              "symbol_type": "async_function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:AsyncClient.put:1875",
            "node_type": "async_function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 61064,
              "byte_end": 62213,
              "ast_path": "async_function:AsyncClient.put",
              "content_hash": "9e41132fdaaa8551f5867ee6f9a1f30e9e11c37f453a10ffcd6642b6d0b9bd7d"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "async_function put",
              "symbol_name": "put",
              "symbol_type": "async_function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:AsyncClient.request:1485",
            "node_type": "async_function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 48716,
              "byte_end": 50676,
              "ast_path": "async_function:AsyncClient.request",
              "content_hash": "53800e9acb814bf27a26a75981e99f8c09dae8b720496b25d31bb74939b20bae"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "async_function request",
              "symbol_name": "request",
              "symbol_type": "async_function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:AsyncClient.send:1594",
            "node_type": "async_function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 52306,
              "byte_end": 53798,
              "ast_path": "async_function:AsyncClient.send",
              "content_hash": "bc5dc851f8b665670b090e84eccdc6b61d3acc51d105354cf7792ec6af54914d"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "async_function send",
              "symbol_name": "send",
              "symbol_type": "async_function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:AsyncClient.stream:1543",
            "node_type": "async_function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 50707,
              "byte_end": 52300,
              "ast_path": "async_function:AsyncClient.stream",
              "content_hash": "f0d4aa3e250a2de6f770c98594ee8c71add78be8503032d970fe8dc8132a8cce"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "async_function stream",
              "symbol_name": "stream",
              "symbol_type": "async_function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:AsyncClient:1307",
            "node_type": "class",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 42349,
              "byte_end": 65712,
              "ast_path": "class:AsyncClient",
              "content_hash": "ba86caa4d9babc17236a27d1bed5c8e952909ee291e6f80d885e1c670d31672d"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "class AsyncClient",
              "symbol_name": "AsyncClient",
              "symbol_type": "class",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient.__init__:189",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 5352,
              "byte_end": 6671,
              "ast_path": "function:BaseClient.__init__",
              "content_hash": "949bb940af6395d4ba92c3cd631c884d4b77323694e737bbc1e9777893a8fa7f"
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
            "node_id": "symbol:httpx/_client.py:BaseClient._build_auth:445",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 13950,
              "byte_end": 14376,
              "ast_path": "function:BaseClient._build_auth",
              "content_hash": "02a93e6a831147cc4f74236ba77656d7c1740fd1ca20e4bb4d7952ea717d99fa"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:httpx/_client.py:BaseClient._build_request_auth:457"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _build_auth",
              "symbol_name": "_build_auth",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 14905,
              "byte_end": 15613,
              "ast_path": "function:BaseClient._build_redirect_request",
              "content_hash": "2f18ca3d8f28ed472f5be8cdb9b71b82d8bd52d2e79bcdc1078d1a548f20cb3b"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:httpx/_client.py:BaseClient._redirect_headers:546"
                },
                {
                  "is_external": false,
                  "target": "symbol:httpx/_client.py:BaseClient._redirect_method:494"
                },
                {
                  "is_external": false,
                  "target": "symbol:httpx/_client.py:BaseClient._redirect_stream:573"
                },
                {
                  "is_external": false,
                  "target": "symbol:httpx/_client.py:BaseClient._redirect_url:517"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _build_redirect_request",
              "symbol_name": "_build_redirect_request",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient._build_request_auth:457",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 14382,
              "byte_end": 14899,
              "ast_path": "function:BaseClient._build_request_auth",
              "content_hash": "a36fdfdb8a23565858a9378f2e703770c1a0da5fdd3ad0e7d3f3d33aa7ebdfbb"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:httpx/_client.py:BaseClient._build_auth:445"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _build_request_auth",
              "symbol_name": "_build_request_auth",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient._enforce_trailing_slash:234",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 6918,
              "byte_end": 7091,
              "ast_path": "function:BaseClient._enforce_trailing_slash",
              "content_hash": "2d812631e86ac4259efa3779c22276c88b0ba6c1f86167e54c7701d304fb738c"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _enforce_trailing_slash",
              "symbol_name": "_enforce_trailing_slash",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient._get_proxy_map:239",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 7097,
              "byte_end": 7606,
              "ast_path": "function:BaseClient._get_proxy_map",
              "content_hash": "323ab9bb5d3b6e8579d129fd297e0bab1631037e85f9cbcbdee40bd7e0516cfe"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _get_proxy_map",
              "symbol_name": "_get_proxy_map",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient._merge_cookies:413",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 12700,
              "byte_end": 13129,
              "ast_path": "function:BaseClient._merge_cookies",
              "content_hash": "1113038edb11f328c3da9ff0737fe9f780a429460a2376c3f7c9a6e7fecf2065"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:httpx/_client.py:BaseClient.build_request:340"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _merge_cookies",
              "symbol_name": "_merge_cookies",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient._merge_headers:424",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 13135,
              "byte_end": 13493,
              "ast_path": "function:BaseClient._merge_headers",
              "content_hash": "25537640006a58dc76c2da64aac5facd7910975066fc55318cb5c5c9dd11c120"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:httpx/_client.py:BaseClient.build_request:340"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _merge_headers",
              "symbol_name": "_merge_headers",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient._merge_queryparams:433",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 13499,
              "byte_end": 13944,
              "ast_path": "function:BaseClient._merge_queryparams",
              "content_hash": "0d0c4af31563061b1d2fbc115bfcbb7524c3bbb087790b6526a1b50a6eba787f"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:httpx/_client.py:BaseClient.build_request:340"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _merge_queryparams",
              "symbol_name": "_merge_queryparams",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient._merge_url:391",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 11694,
              "byte_end": 12694,
              "ast_path": "function:BaseClient._merge_url",
              "content_hash": "1d1e4f3806a40f76acc927927b4b6bdca831222477e0eab8fdd34167e121f4f2"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:httpx/_client.py:BaseClient.build_request:340"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _merge_url",
              "symbol_name": "_merge_url",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient._redirect_headers:546",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 17588,
              "byte_end": 18720,
              "ast_path": "function:BaseClient._redirect_headers",
              "content_hash": "cf40c6f53f3e49b9f6ebbb8926efe85db5ade78f26439864f896d70bdc6c370c"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:httpx/_client.py:_is_https_redirect:62"
                },
                {
                  "is_external": false,
                  "target": "symbol:httpx/_client.py:_same_origin:83"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _redirect_headers",
              "symbol_name": "_redirect_headers",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient._redirect_method:494",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 15619,
              "byte_end": 16494,
              "ast_path": "function:BaseClient._redirect_method",
              "content_hash": "e421099e82483a433735e1e0a31c750e54ccf65d1b752dd063979f1c2dc7b5c9"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _redirect_method",
              "symbol_name": "_redirect_method",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient._redirect_stream:573",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 18726,
              "byte_end": 19047,
              "ast_path": "function:BaseClient._redirect_stream",
              "content_hash": "887fda7354d3216c1d4440b3bdb55abad50de782b6ba64b142887efb0abf4698"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _redirect_stream",
              "symbol_name": "_redirect_stream",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient._redirect_url:517",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 16500,
              "byte_end": 17582,
              "ast_path": "function:BaseClient._redirect_url",
              "content_hash": "c814d4dbfc61c2b4b85c30252d30f77e7e6962b60b5c16c079c4b2e8371af2b2"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _redirect_url",
              "symbol_name": "_redirect_url",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient._set_timeout:584",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 19053,
              "byte_end": 19409,
              "ast_path": "function:BaseClient._set_timeout",
              "content_hash": "d4a3327609119eb56554efc30901ea4ad2fb7a8f8f027fb36601396636259a35"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _set_timeout",
              "symbol_name": "_set_timeout",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient.auth:273",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 8190,
              "byte_end": 8427,
              "ast_path": "function:BaseClient.auth",
              "content_hash": "3d882eb628937f07496301e98615faf0d37cf9698c054dc419dea881f17962fe"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function auth",
              "symbol_name": "auth",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient.auth:284",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 8450,
              "byte_end": 8534,
              "ast_path": "function:BaseClient.auth",
              "content_hash": "5b6bfa68225e73fbc4b2ec4a168a1616783137ffdb74a402a7a7cf954b07ffc6"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function auth",
              "symbol_name": "auth",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient.base_url:288",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 8554,
              "byte_end": 8700,
              "ast_path": "function:BaseClient.base_url",
              "content_hash": "7c92daa9c482129ae7232d0cf58204a31dd35070345586b326d63861351bd1e7"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function base_url",
              "symbol_name": "base_url",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient.base_url:295",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 8727,
              "byte_end": 8834,
              "ast_path": "function:BaseClient.base_url",
              "content_hash": "c7e21a81ca153c8b1f3adcc5faf3e61f3829c7a6edec6d96bbc87cb9ca32481f"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function base_url",
              "symbol_name": "base_url",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient.build_request:340",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 9995,
              "byte_end": 11688,
              "ast_path": "function:BaseClient.build_request",
              "content_hash": "ecc2854536373aa7c57c14514d27ebd94ebf501e18959262b6d2c44a83b27065"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:httpx/_client.py:BaseClient._merge_cookies:413"
                },
                {
                  "is_external": false,
                  "target": "symbol:httpx/_client.py:BaseClient._merge_headers:424"
                },
                {
                  "is_external": false,
                  "target": "symbol:httpx/_client.py:BaseClient._merge_queryparams:433"
                },
                {
                  "is_external": false,
                  "target": "symbol:httpx/_client.py:BaseClient._merge_url:391"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function build_request",
              "symbol_name": "build_request",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient.cookies:319",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 9444,
              "byte_end": 9582,
              "ast_path": "function:BaseClient.cookies",
              "content_hash": "003114984299854bcfae185be934a3b176badbc5cb7f003b1476eb6db4d038fb"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function cookies",
              "symbol_name": "cookies",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient.cookies:326",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 9608,
              "byte_end": 9697,
              "ast_path": "function:BaseClient.cookies",
              "content_hash": "68983f9c35e3a617a0ac13e12436a58b2b7b388325f0ad859089099fb3382711"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function cookies",
              "symbol_name": "cookies",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient.event_hooks:262",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 7820,
              "byte_end": 7905,
              "ast_path": "function:BaseClient.event_hooks",
              "content_hash": "4b49e4d827ca437b4c94473e748d96c958e90d08b826f1e86a1d72d9f7e89eb2"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function event_hooks",
              "symbol_name": "event_hooks",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient.event_hooks:266",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 7935,
              "byte_end": 8170,
              "ast_path": "function:BaseClient.event_hooks",
              "content_hash": "6ceb30eb5b3a9af10c01a2d9578f76ce92e2b37b21af110e410db3162b7ea390"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function event_hooks",
              "symbol_name": "event_hooks",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient.headers:299",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 8854,
              "byte_end": 8991,
              "ast_path": "function:BaseClient.headers",
              "content_hash": "18448fc94eb773bc91b877a2e2c1bccc11e71b54c7d21cfaf35351abf122ae97"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function headers",
              "symbol_name": "headers",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient.headers:306",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 9017,
              "byte_end": 9424,
              "ast_path": "function:BaseClient.headers",
              "content_hash": "8d53d8fdb86971cdf17ec6d951333286480bcd868d7edf24f6f3e888792aa93f"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function headers",
              "symbol_name": "headers",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient.is_closed:224",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 6691,
              "byte_end": 6833,
              "ast_path": "function:BaseClient.is_closed",
              "content_hash": "fdfeb41ec3bfe885d2a0999679959167e47041c0d681e6e9444c233d6af6bfac"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function is_closed",
              "symbol_name": "is_closed",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient.params:330",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 9717,
              "byte_end": 9871,
              "ast_path": "function:BaseClient.params",
              "content_hash": "29d1ca1572b48a2c57908965e0d7a875c73a097822727330c9d1fafa523abaf1"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function params",
              "symbol_name": "params",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient.params:337",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 9896,
              "byte_end": 9989,
              "ast_path": "function:BaseClient.params",
              "content_hash": "1e238a155ad4d7a1c1d0321486d0d295f0ca83c8f1f349127642d9948d2a6640"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function params",
              "symbol_name": "params",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient.timeout:254",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 7626,
              "byte_end": 7684,
              "ast_path": "function:BaseClient.timeout",
              "content_hash": "b966cdc6b8cf1322b74b3809f90aa503102b119a7b30f2b2b9b610f02cb33419"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function timeout",
              "symbol_name": "timeout",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient.timeout:258",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 7710,
              "byte_end": 7800,
              "ast_path": "function:BaseClient.timeout",
              "content_hash": "aa30340040f913dde3164945e8b49095ec9dc20ec3b952ffca520bb3eafb7fb5"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function timeout",
              "symbol_name": "timeout",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient.trust_env:231",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 6853,
              "byte_end": 6912,
              "ast_path": "function:BaseClient.trust_env",
              "content_hash": "42d6e05a6c8d1578659dbd1da218fa640e26b8eec7c8d6ab20e37fc4723a02b7"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function trust_env",
              "symbol_name": "trust_env",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BaseClient:188",
            "node_type": "class",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 5330,
              "byte_end": 19409,
              "ast_path": "class:BaseClient",
              "content_hash": "d7d29cf66d50d4f39b756a818205c74593f1de9e77749b0409ff2e51292e149c"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "class BaseClient",
              "symbol_name": "BaseClient",
              "symbol_type": "class",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BoundAsyncStream.__aiter__:175",
            "node_type": "async_function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 4964,
              "byte_end": 5086,
              "ast_path": "async_function:BoundAsyncStream.__aiter__",
              "content_hash": "d784054719058c7d184507cd9b7ab2d02e281e5230915a96a386be9f1b07d341"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "async_function __aiter__",
              "symbol_name": "__aiter__",
              "symbol_type": "async_function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BoundAsyncStream.__init__:168",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 4766,
              "byte_end": 4958,
              "ast_path": "function:BoundAsyncStream.__init__",
              "content_hash": "2ae7b3b02b388beb117a3677b3d96b9dd8cb1a4f674f878e6ea43d4f3883c2be"
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
            "node_id": "symbol:httpx/_client.py:BoundAsyncStream.aclose:179",
            "node_type": "async_function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 5092,
              "byte_end": 5280,
              "ast_path": "async_function:BoundAsyncStream.aclose",
              "content_hash": "acc29666778996be634e77ea639c1932fae9966c73b5aab60c6d7ea6498e44fe"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "async_function aclose",
              "symbol_name": "aclose",
              "symbol_type": "async_function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BoundAsyncStream:162",
            "node_type": "class",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 4555,
              "byte_end": 5280,
              "ast_path": "class:BoundAsyncStream",
              "content_hash": "15e5bb2ccb76d9b4fe40dede8433e45744db6f9536163946043d9397698ed979"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "class BoundAsyncStream",
              "symbol_name": "BoundAsyncStream",
              "symbol_type": "class",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BoundSyncStream.__init__:145",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 4071,
              "byte_end": 4262,
              "ast_path": "function:BoundSyncStream.__init__",
              "content_hash": "16bb48a0c41127084b1497a57162fa36951bf6647dfc9df09fefd5448239ff93"
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
            "node_id": "symbol:httpx/_client.py:BoundSyncStream.__iter__:152",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 4268,
              "byte_end": 4372,
              "ast_path": "function:BoundSyncStream.__iter__",
              "content_hash": "00360c7afc0f9189b97ec0ae27a0010b27db0b2ed9d592683a5ca621559258a4"
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
            "node_id": "symbol:httpx/_client.py:BoundSyncStream.close:156",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 4378,
              "byte_end": 4552,
              "ast_path": "function:BoundSyncStream.close",
              "content_hash": "4b340260576cef93879a4bc5dbbb2abc98945490afb33901770932bd06c89fbd"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function close",
              "symbol_name": "close",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:BoundSyncStream:139",
            "node_type": "class",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 3869,
              "byte_end": 4552,
              "ast_path": "class:BoundSyncStream",
              "content_hash": "d2e9a40a7d8147e99ed1803903c0d17dbe0346e7ff685aa95596ebd3ede923a0"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "class BoundSyncStream",
              "symbol_name": "BoundSyncStream",
              "symbol_type": "class",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:Client.__enter__:1275",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 41285,
              "byte_end": 41889,
              "ast_path": "function:Client.__enter__",
              "content_hash": "cdf6c01eefdcbefac0f0755ed2749b0b8ecec6f17617580c4adb988c0fafb78b"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:httpx/_client.py:Client.__enter__:1275"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:httpx/_client.py:Client.__enter__:1275"
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
            "node_id": "symbol:httpx/_client.py:Client.__exit__:1293",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 41895,
              "byte_end": 42346,
              "ast_path": "function:Client.__exit__",
              "content_hash": "363d3668eeea67bf86466057131fecaa6cccb2bb20f1d6f3a49ce1e79e136129"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:httpx/_client.py:Client.__exit__:1293"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:httpx/_client.py:Client.__exit__:1293"
                }
              ],
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
            "node_id": "symbol:httpx/_client.py:Client.__init__:639",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 21364,
              "byte_end": 24113,
              "ast_path": "function:Client.__init__",
              "content_hash": "28115a77fa1ff89c74c9061021ba67ad22548cd75e96b766a1e35605fabe1385"
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
            "node_id": "symbol:httpx/_client.py:Client._init_proxy_transport:740",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 24716,
              "byte_end": 25248,
              "ast_path": "function:Client._init_proxy_transport",
              "content_hash": "c7266bec3312f9e80a0b4405d3827e7734f9c7483335a2241b12bfa0a21d19d3"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _init_proxy_transport",
              "symbol_name": "_init_proxy_transport",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:Client._init_transport:718",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 24119,
              "byte_end": 24710,
              "ast_path": "function:Client._init_transport",
              "content_hash": "ee4a0c466f94955acc047aaa56d5aa124f4146e4dbff5906a2dc854d2a9ab22e"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _init_transport",
              "symbol_name": "_init_transport",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:Client._send_handling_auth:930",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 30665,
              "byte_end": 31685,
              "ast_path": "function:Client._send_handling_auth",
              "content_hash": "d6cc4d080bf7354b17d9d779a874154d25bb6272698f94e234deae9134204f98"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _send_handling_auth",
              "symbol_name": "_send_handling_auth",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:Client._send_handling_redirects:964",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 31691,
              "byte_end": 32850,
              "ast_path": "function:Client._send_handling_redirects",
              "content_hash": "907341fd2949a24d059f72dc7c171fb8f8888a2849b4d8e8d029877225d07089"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _send_handling_redirects",
              "symbol_name": "_send_handling_redirects",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:Client._send_single_request:1001",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 32856,
              "byte_end": 33970,
              "ast_path": "function:Client._send_single_request",
              "content_hash": "9e28208b74ce0362acc80966f2f37254421445f9f854f87e70b1da40fa6dd0dc"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _send_single_request",
              "symbol_name": "_send_single_request",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:Client._transport_for_url:760",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 25254,
              "byte_end": 25680,
              "ast_path": "function:Client._transport_for_url",
              "content_hash": "bfea9e1bb9cfdd40bc8b0a21915625b5077a3f974edde501014ac6da6afd7c51"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _transport_for_url",
              "symbol_name": "_transport_for_url",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:Client.close:1263",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 40934,
              "byte_end": 41279,
              "ast_path": "function:Client.close",
              "content_hash": "904b304be94c2fdfe0a0a3f9d835451c442174edd228ce2addb217f7bdb0f375"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function close",
              "symbol_name": "close",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:Client.delete:1234",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 40053,
              "byte_end": 40928,
              "ast_path": "function:Client.delete",
              "content_hash": "b2359e130aefe3c687b799f42ca84a8f3f4123f5f2709aed98d7b1f06b6b0803"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function delete",
              "symbol_name": "delete",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:Client.get:1036",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 33976,
              "byte_end": 34849,
              "ast_path": "function:Client.get",
              "content_hash": "bf9a61d7562ded6a62750e4c68761766d23309c5cad2723caeb0dcad50c00945"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
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
            "node_id": "symbol:httpx/_client.py:Client.head:1094",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 35740,
              "byte_end": 36609,
              "ast_path": "function:Client.head",
              "content_hash": "f2a23df2db98d20650787389dcf6ab4cdf551e7b85409c0615c62dcb240bbc15"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function head",
              "symbol_name": "head",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:Client.options:1065",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 34855,
              "byte_end": 35734,
              "ast_path": "function:Client.options",
              "content_hash": "793da3be51dd88709989b58d87b26e267710fc7bac465932ec72d1e632d2eb0d"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function options",
              "symbol_name": "options",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:Client.patch:1197",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 38904,
              "byte_end": 40047,
              "ast_path": "function:Client.patch",
              "content_hash": "51b03b990fa13c3007e42b0680ae75dc70f50a363c77a7bdaa818d4de117f824"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function patch",
              "symbol_name": "patch",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:Client.post:1123",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 36615,
              "byte_end": 37755,
              "ast_path": "function:Client.post",
              "content_hash": "61f18a7bef292b49760c06e23c23a222e60fdbe7108e172297a591d1c3dccc7c"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function post",
              "symbol_name": "post",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:Client.put:1160",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 37761,
              "byte_end": 38898,
              "ast_path": "function:Client.put",
              "content_hash": "2f74dc5aba92aa241184119dba50523756420875ad29e26154e5d7217f584b4a"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function put",
              "symbol_name": "put",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:Client.request:771",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 25686,
              "byte_end": 27597,
              "ast_path": "function:Client.request",
              "content_hash": "13c19699f293fabef585ad97328984be3300aee027b27fec97ce080977553431"
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
            "node_id": "symbol:httpx/_client.py:Client.send:879",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 29198,
              "byte_end": 30659,
              "ast_path": "function:Client.send",
              "content_hash": "3d6606ace651b04dacca10545006ce6373351d92468eb5bdd5ab3d22c9e704d7"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function send",
              "symbol_name": "send",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:Client.stream:828",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 27623,
              "byte_end": 29192,
              "ast_path": "function:Client.stream",
              "content_hash": "4f1ed746aedee04af673e1e633236dd21bd3c086143751f52cd058f621c84bad"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function stream",
              "symbol_name": "stream",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:Client:594",
            "node_type": "class",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 19412,
              "byte_end": 42346,
              "ast_path": "class:Client",
              "content_hash": "38b20eb12f77c94252fb0b21bc72167940904b8a51453cb82159f2aacf94f685"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "class Client",
              "symbol_name": "Client",
              "symbol_type": "class",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:ClientState:125",
            "node_type": "class",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 3418,
              "byte_end": 3866,
              "ast_path": "class:ClientState",
              "content_hash": "f5a99a827436d7d490839ad520b80f6f01b66a41fb0aa035fdde5a4f6c6e869c"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "class ClientState",
              "symbol_name": "ClientState",
              "symbol_type": "class",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:UseClientDefault:94",
            "node_type": "class",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 2330,
              "byte_end": 3192,
              "ast_path": "class:UseClientDefault",
              "content_hash": "c7838b2b64aa3ba2027a32fbb676b75425f0eaeac31d583eb4948c0ded00ee5f"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "class UseClientDefault",
              "symbol_name": "UseClientDefault",
              "symbol_type": "class",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:_is_https_redirect:62",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 1536,
              "byte_end": 1897,
              "ast_path": "function:_is_https_redirect",
              "content_hash": "f7fb9a7652de2ee8be1892fda8abdd18c5cafef3f0b7cee910a997b0d2e3108d"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:httpx/_client.py:BaseClient._redirect_headers:546"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:httpx/_client.py:_port_or_default:77"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _is_https_redirect",
              "symbol_name": "_is_https_redirect",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:_port_or_default:77",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 1900,
              "byte_end": 2052,
              "ast_path": "function:_port_or_default",
              "content_hash": "d70ff71cb4458c59da46b26ea655df1e7c87c40d139515e3a672f86942b86c83"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:httpx/_client.py:_is_https_redirect:62"
                },
                {
                  "source": "symbol:httpx/_client.py:_same_origin:83"
                }
              ],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _port_or_default",
              "symbol_name": "_port_or_default",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_client.py:_same_origin:83",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_client.py",
              "byte_start": 2055,
              "byte_end": 2327,
              "ast_path": "function:_same_origin",
              "content_hash": "aac753c9500e9d229397f05548f971de5a63129de76236da0994c25179fad392"
            },
            "semantic_contract": {
              "called_by": [
                {
                  "source": "symbol:httpx/_client.py:BaseClient._redirect_headers:546"
                }
              ],
              "calls": [
                {
                  "is_external": false,
                  "target": "symbol:httpx/_client.py:_port_or_default:77"
                }
              ],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function _same_origin",
              "symbol_name": "_same_origin",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          }
        ],
        "edges": [
          {
            "edge_id": "calls:symbol:httpx/_client.py:AsyncClient.__aenter__:1990:symbol:httpx/_client.py:AsyncClient.__aenter__:1990:2002",
            "edge_type": "calls",
            "from_node": "symbol:httpx/_client.py:AsyncClient.__aenter__:1990",
            "to_node": "symbol:httpx/_client.py:AsyncClient.__aenter__:1990",
            "evidence": {
              "line": 2002,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:httpx/_client.py:AsyncClient.__aenter__:1990:symbol:httpx/_client.py:AsyncClient.__aenter__:1990:2005",
            "edge_type": "calls",
            "from_node": "symbol:httpx/_client.py:AsyncClient.__aenter__:1990",
            "to_node": "symbol:httpx/_client.py:AsyncClient.__aenter__:1990",
            "evidence": {
              "line": 2005,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:httpx/_client.py:AsyncClient.__aexit__:2008:symbol:httpx/_client.py:AsyncClient.__aexit__:2008:2016",
            "edge_type": "calls",
            "from_node": "symbol:httpx/_client.py:AsyncClient.__aexit__:2008",
            "to_node": "symbol:httpx/_client.py:AsyncClient.__aexit__:2008",
            "evidence": {
              "line": 2016,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:httpx/_client.py:AsyncClient.__aexit__:2008:symbol:httpx/_client.py:AsyncClient.__aexit__:2008:2019",
            "edge_type": "calls",
            "from_node": "symbol:httpx/_client.py:AsyncClient.__aexit__:2008",
            "to_node": "symbol:httpx/_client.py:AsyncClient.__aexit__:2008",
            "evidence": {
              "line": 2019,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_redirect_request:475:symbol:httpx/_client.py:BaseClient._redirect_headers:546:482",
            "edge_type": "calls",
            "from_node": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475",
            "to_node": "symbol:httpx/_client.py:BaseClient._redirect_headers:546",
            "evidence": {
              "line": 482,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_redirect_request:475:symbol:httpx/_client.py:BaseClient._redirect_method:494:480",
            "edge_type": "calls",
            "from_node": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475",
            "to_node": "symbol:httpx/_client.py:BaseClient._redirect_method:494",
            "evidence": {
              "line": 480,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_redirect_request:475:symbol:httpx/_client.py:BaseClient._redirect_stream:573:483",
            "edge_type": "calls",
            "from_node": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475",
            "to_node": "symbol:httpx/_client.py:BaseClient._redirect_stream:573",
            "evidence": {
              "line": 483,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_redirect_request:475:symbol:httpx/_client.py:BaseClient._redirect_url:517:481",
            "edge_type": "calls",
            "from_node": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475",
            "to_node": "symbol:httpx/_client.py:BaseClient._redirect_url:517",
            "evidence": {
              "line": 481,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_request_auth:457:symbol:httpx/_client.py:BaseClient._build_auth:445:463",
            "edge_type": "calls",
            "from_node": "symbol:httpx/_client.py:BaseClient._build_request_auth:457",
            "to_node": "symbol:httpx/_client.py:BaseClient._build_auth:445",
            "evidence": {
              "line": 463,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:httpx/_client.py:BaseClient._redirect_headers:546:symbol:httpx/_client.py:_is_https_redirect:62:553",
            "edge_type": "calls",
            "from_node": "symbol:httpx/_client.py:BaseClient._redirect_headers:546",
            "to_node": "symbol:httpx/_client.py:_is_https_redirect:62",
            "evidence": {
              "line": 553,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:httpx/_client.py:BaseClient._redirect_headers:546:symbol:httpx/_client.py:_same_origin:83:552",
            "edge_type": "calls",
            "from_node": "symbol:httpx/_client.py:BaseClient._redirect_headers:546",
            "to_node": "symbol:httpx/_client.py:_same_origin:83",
            "evidence": {
              "line": 552,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:httpx/_client.py:BaseClient.build_request:340:symbol:httpx/_client.py:BaseClient._merge_cookies:413:368",
            "edge_type": "calls",
            "from_node": "symbol:httpx/_client.py:BaseClient.build_request:340",
            "to_node": "symbol:httpx/_client.py:BaseClient._merge_cookies:413",
            "evidence": {
              "line": 368,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:httpx/_client.py:BaseClient.build_request:340:symbol:httpx/_client.py:BaseClient._merge_headers:424:367",
            "edge_type": "calls",
            "from_node": "symbol:httpx/_client.py:BaseClient.build_request:340",
            "to_node": "symbol:httpx/_client.py:BaseClient._merge_headers:424",
            "evidence": {
              "line": 367,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:httpx/_client.py:BaseClient.build_request:340:symbol:httpx/_client.py:BaseClient._merge_queryparams:433:369",
            "edge_type": "calls",
            "from_node": "symbol:httpx/_client.py:BaseClient.build_request:340",
            "to_node": "symbol:httpx/_client.py:BaseClient._merge_queryparams:433",
            "evidence": {
              "line": 369,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:httpx/_client.py:BaseClient.build_request:340:symbol:httpx/_client.py:BaseClient._merge_url:391:366",
            "edge_type": "calls",
            "from_node": "symbol:httpx/_client.py:BaseClient.build_request:340",
            "to_node": "symbol:httpx/_client.py:BaseClient._merge_url:391",
            "evidence": {
              "line": 366,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:httpx/_client.py:Client.__enter__:1275:symbol:httpx/_client.py:Client.__enter__:1275:1287",
            "edge_type": "calls",
            "from_node": "symbol:httpx/_client.py:Client.__enter__:1275",
            "to_node": "symbol:httpx/_client.py:Client.__enter__:1275",
            "evidence": {
              "line": 1287,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:httpx/_client.py:Client.__enter__:1275:symbol:httpx/_client.py:Client.__enter__:1275:1290",
            "edge_type": "calls",
            "from_node": "symbol:httpx/_client.py:Client.__enter__:1275",
            "to_node": "symbol:httpx/_client.py:Client.__enter__:1275",
            "evidence": {
              "line": 1290,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:httpx/_client.py:Client.__exit__:1293:symbol:httpx/_client.py:Client.__exit__:1293:1301",
            "edge_type": "calls",
            "from_node": "symbol:httpx/_client.py:Client.__exit__:1293",
            "to_node": "symbol:httpx/_client.py:Client.__exit__:1293",
            "evidence": {
              "line": 1301,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:httpx/_client.py:Client.__exit__:1293:symbol:httpx/_client.py:Client.__exit__:1293:1304",
            "edge_type": "calls",
            "from_node": "symbol:httpx/_client.py:Client.__exit__:1293",
            "to_node": "symbol:httpx/_client.py:Client.__exit__:1293",
            "evidence": {
              "line": 1304,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:httpx/_client.py:_is_https_redirect:62:symbol:httpx/_client.py:_port_or_default:77:71",
            "edge_type": "calls",
            "from_node": "symbol:httpx/_client.py:_is_https_redirect:62",
            "to_node": "symbol:httpx/_client.py:_port_or_default:77",
            "evidence": {
              "line": 71,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:httpx/_client.py:_is_https_redirect:62:symbol:httpx/_client.py:_port_or_default:77:73",
            "edge_type": "calls",
            "from_node": "symbol:httpx/_client.py:_is_https_redirect:62",
            "to_node": "symbol:httpx/_client.py:_port_or_default:77",
            "evidence": {
              "line": 73,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "calls:symbol:httpx/_client.py:_same_origin:83:symbol:httpx/_client.py:_port_or_default:77:90",
            "edge_type": "calls",
            "from_node": "symbol:httpx/_client.py:_same_origin:83",
            "to_node": "symbol:httpx/_client.py:_port_or_default:77",
            "evidence": {
              "line": 90,
              "rel": "ast_call"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:AsyncClient.__aenter__:1990",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:AsyncClient.__aenter__:1990",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:AsyncClient.__aexit__:2008",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:AsyncClient.__aexit__:2008",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:AsyncClient.__init__:1353",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:AsyncClient.__init__:1353",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:AsyncClient._init_proxy_transport:1454",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:AsyncClient._init_proxy_transport:1454",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:AsyncClient._init_transport:1432",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:AsyncClient._init_transport:1432",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:AsyncClient._send_handling_auth:1645",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:AsyncClient._send_handling_auth:1645",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:AsyncClient._send_handling_redirects:1679",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:AsyncClient._send_handling_redirects:1679",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:AsyncClient._send_single_request:1717",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:AsyncClient._send_single_request:1717",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:AsyncClient._transport_for_url:1474",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:AsyncClient._transport_for_url:1474",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:AsyncClient.aclose:1978",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:AsyncClient.aclose:1978",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:AsyncClient.delete:1949",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:AsyncClient.delete:1949",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:AsyncClient.get:1751",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:AsyncClient.get:1751",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:AsyncClient.head:1809",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:AsyncClient.head:1809",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:AsyncClient.options:1780",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:AsyncClient.options:1780",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:AsyncClient.patch:1912",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:AsyncClient.patch:1912",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:AsyncClient.post:1838",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:AsyncClient.post:1838",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:AsyncClient.put:1875",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:AsyncClient.put:1875",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:AsyncClient.request:1485",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:AsyncClient.request:1485",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:AsyncClient.send:1594",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:AsyncClient.send:1594",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:AsyncClient.stream:1543",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:AsyncClient.stream:1543",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:AsyncClient:1307",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:AsyncClient:1307",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient.__init__:189",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient.__init__:189",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient._build_auth:445",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient._build_auth:445",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient._build_redirect_request:475",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient._build_request_auth:457",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient._build_request_auth:457",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient._enforce_trailing_slash:234",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient._enforce_trailing_slash:234",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient._get_proxy_map:239",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient._get_proxy_map:239",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient._merge_cookies:413",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient._merge_cookies:413",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient._merge_headers:424",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient._merge_headers:424",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient._merge_queryparams:433",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient._merge_queryparams:433",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient._merge_url:391",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient._merge_url:391",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient._redirect_headers:546",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient._redirect_headers:546",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient._redirect_method:494",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient._redirect_method:494",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient._redirect_stream:573",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient._redirect_stream:573",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient._redirect_url:517",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient._redirect_url:517",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient._set_timeout:584",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient._set_timeout:584",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient.auth:273",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient.auth:273",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient.auth:284",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient.auth:284",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient.base_url:288",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient.base_url:288",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient.base_url:295",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient.base_url:295",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient.build_request:340",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient.build_request:340",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient.cookies:319",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient.cookies:319",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient.cookies:326",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient.cookies:326",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient.event_hooks:262",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient.event_hooks:262",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient.event_hooks:266",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient.event_hooks:266",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient.headers:299",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient.headers:299",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient.headers:306",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient.headers:306",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient.is_closed:224",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient.is_closed:224",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient.params:330",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient.params:330",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient.params:337",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient.params:337",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient.timeout:254",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient.timeout:254",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient.timeout:258",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient.timeout:258",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient.trust_env:231",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient.trust_env:231",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BaseClient:188",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BaseClient:188",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BoundAsyncStream.__aiter__:175",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BoundAsyncStream.__aiter__:175",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BoundAsyncStream.__init__:168",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BoundAsyncStream.__init__:168",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BoundAsyncStream.aclose:179",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BoundAsyncStream.aclose:179",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BoundAsyncStream:162",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BoundAsyncStream:162",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BoundSyncStream.__init__:145",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BoundSyncStream.__init__:145",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BoundSyncStream.__iter__:152",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BoundSyncStream.__iter__:152",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BoundSyncStream.close:156",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BoundSyncStream.close:156",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:BoundSyncStream:139",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:BoundSyncStream:139",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:Client.__enter__:1275",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:Client.__enter__:1275",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:Client.__exit__:1293",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:Client.__exit__:1293",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:Client.__init__:639",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:Client.__init__:639",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:Client._init_proxy_transport:740",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:Client._init_proxy_transport:740",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:Client._init_transport:718",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:Client._init_transport:718",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:Client._send_handling_auth:930",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:Client._send_handling_auth:930",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:Client._send_handling_redirects:964",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:Client._send_handling_redirects:964",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:Client._send_single_request:1001",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:Client._send_single_request:1001",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:Client._transport_for_url:760",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:Client._transport_for_url:760",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:Client.close:1263",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:Client.close:1263",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:Client.delete:1234",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:Client.delete:1234",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:Client.get:1036",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:Client.get:1036",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:Client.head:1094",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:Client.head:1094",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:Client.options:1065",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:Client.options:1065",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:Client.patch:1197",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:Client.patch:1197",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:Client.post:1123",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:Client.post:1123",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:Client.put:1160",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:Client.put:1160",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:Client.request:771",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:Client.request:771",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:Client.send:879",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:Client.send:879",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:Client.stream:828",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:Client.stream:828",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:Client:594",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:Client:594",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:ClientState:125",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:ClientState:125",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:UseClientDefault:94",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:UseClientDefault:94",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:_is_https_redirect:62",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:_is_https_redirect:62",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:_port_or_default:77",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:_port_or_default:77",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_client.py:symbol:httpx/_client.py:_same_origin:83",
            "edge_type": "contains",
            "from_node": "module:httpx/_client.py",
            "to_node": "symbol:httpx/_client.py:_same_origin:83",
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
        "file_path": "httpx/_client.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "module:httpx/_client.py",
      "confidence_trigger": 0.65,
      "output_size_tokens": 757,
      "result": {
        "status": "ok",
        "file_path": "httpx/_client.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 2019,
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
            "content": "import datetime"
          },
          {
            "line_number": 4,
            "content": "import enum"
          },
          {
            "line_number": 5,
            "content": "import logging"
          },
          {
            "line_number": 6,
            "content": "import time"
          },
          {
            "line_number": 7,
            "content": "import typing"
          },
          {
            "line_number": 8,
            "content": "import warnings"
          },
          {
            "line_number": 9,
            "content": "from contextlib import asynccontextmanager, contextmanager"
          },
          {
            "line_number": 10,
            "content": "from types import TracebackType"
          },
          {
            "line_number": 11,
            "content": ""
          },
          {
            "line_number": 12,
            "content": "from .__version__ import __version__"
          },
          {
            "line_number": 13,
            "content": "from ._auth import Auth, BasicAuth, FunctionAuth"
          },
          {
            "line_number": 14,
            "content": "from ._config import ("
          },
          {
            "line_number": 15,
            "content": "    DEFAULT_LIMITS,"
          },
          {
            "line_number": 16,
            "content": "    DEFAULT_MAX_REDIRECTS,"
          },
          {
            "line_number": 17,
            "content": "    DEFAULT_TIMEOUT_CONFIG,"
          },
          {
            "line_number": 18,
            "content": "    Limits,"
          },
          {
            "line_number": 19,
            "content": "    Proxy,"
          },
          {
            "line_number": 20,
            "content": "    Timeout,"
          },
          {
            "line_number": 21,
            "content": ")"
          },
          {
            "line_number": 22,
            "content": "from ._decoders import SUPPORTED_DECODERS"
          },
          {
            "line_number": 23,
            "content": "from ._exceptions import ("
          },
          {
            "line_number": 24,
            "content": "    InvalidURL,"
          },
          {
            "line_number": 25,
            "content": "    RemoteProtocolError,"
          },
          {
            "line_number": 26,
            "content": "    TooManyRedirects,"
          },
          {
            "line_number": 27,
            "content": "    request_context,"
          },
          {
            "line_number": 28,
            "content": ")"
          },
          {
            "line_number": 29,
            "content": "from ._models import Cookies, Headers, Request, Response"
          },
          {
            "line_number": 30,
            "content": "from ._status_codes import codes"
          },
          {
            "line_number": 31,
            "content": "from ._transports.base import AsyncBaseTransport, BaseTransport"
          },
          {
            "line_number": 32,
            "content": "from ._transports.default import AsyncHTTPTransport, HTTPTransport"
          },
          {
            "line_number": 33,
            "content": "from ._types import ("
          },
          {
            "line_number": 34,
            "content": "    AsyncByteStream,"
          },
          {
            "line_number": 35,
            "content": "    AuthTypes,"
          },
          {
            "line_number": 36,
            "content": "    CertTypes,"
          },
          {
            "line_number": 37,
            "content": "    CookieTypes,"
          },
          {
            "line_number": 38,
            "content": "    HeaderTypes,"
          },
          {
            "line_number": 39,
            "content": "    ProxyTypes,"
          },
          {
            "line_number": 40,
            "content": "    QueryParamTypes,"
          },
          {
            "line_number": 41,
            "content": "    RequestContent,"
          },
          {
            "line_number": 42,
            "content": "    RequestData,"
          },
          {
            "line_number": 43,
            "content": "    RequestExtensions,"
          },
          {
            "line_number": 44,
            "content": "    RequestFiles,"
          },
          {
            "line_number": 45,
            "content": "    SyncByteStream,"
          },
          {
            "line_number": 46,
            "content": "    TimeoutTypes,"
          },
          {
            "line_number": 47,
            "content": ")"
          },
          {
            "line_number": 48,
            "content": "from ._urls import URL, QueryParams"
          },
          {
            "line_number": 49,
            "content": "from ._utils import URLPattern, get_environment_proxies"
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
        "node_id": "module:httpx/_config.py",
        "depth": 2
      },
      "node_id": "module:httpx/_config.py",
      "confidence_trigger": 0.85,
      "output_size_tokens": 3210,
      "result": {
        "status": "ok",
        "seed_node": "module:httpx/_config.py",
        "depth": 2,
        "nodes": [
          {
            "node_id": "module:httpx/_config.py",
            "node_type": "module",
            "source_anchor": {
              "file_path": "httpx/_config.py",
              "byte_start": 0,
              "byte_end": 8547,
              "ast_path": "module",
              "content_hash": "a4fa7653ec2271f70ab05f8a6111352d876dddee84446788a1767c1a3a372d67"
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
              "symbol_name": "httpx/_config.py",
              "symbol_type": "module",
              "tier": 1
            },
            "confidence": 1.0
          },
          {
            "node_id": "symbol:httpx/_config.py:Limits.__eq__:184",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_config.py",
              "byte_start": 6272,
              "byte_end": 6597,
              "ast_path": "function:Limits.__eq__",
              "content_hash": "4d32fcc9cbca07965828ac035694bbf8b36e932ff384fe0940dbacab1fbc70e3"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function __eq__",
              "symbol_name": "__eq__",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_config.py:Limits.__init__:173",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_config.py",
              "byte_start": 5906,
              "byte_end": 6266,
              "ast_path": "function:Limits.__init__",
              "content_hash": "63a6d1b850d9d624eb4c1b464540f62358b78f0bc9aebbea33949c316ef370b5"
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
            "node_id": "symbol:httpx/_config.py:Limits.__repr__:192",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_config.py",
              "byte_start": 6603,
              "byte_end": 6903,
              "ast_path": "function:Limits.__repr__",
              "content_hash": "629047b9e48821105ac1c2e84feef2afcc6de3d6c8c09eff60e4512201ca7fd7"
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
            "node_id": "symbol:httpx/_config.py:Limits:159",
            "node_type": "class",
            "source_anchor": {
              "file_path": "httpx/_config.py",
              "byte_start": 5406,
              "byte_end": 6903,
              "ast_path": "class:Limits",
              "content_hash": "fb9586790c0bcd9f71e446b30e145d8969ca821fda0aabdab68a243a20787fd8"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "class Limits",
              "symbol_name": "Limits",
              "symbol_type": "class",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_config.py:Proxy.__init__:202",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_config.py",
              "byte_start": 6923,
              "byte_end": 7665,
              "ast_path": "function:Proxy.__init__",
              "content_hash": "e7a8691335089d07ab99ce0eee9a8990f814ef2b11075c56f933ed114828ad82"
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
            "node_id": "symbol:httpx/_config.py:Proxy.__repr__:235",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_config.py",
              "byte_start": 7944,
              "byte_end": 8396,
              "ast_path": "function:Proxy.__repr__",
              "content_hash": "a590cdeeac88f86587d6708808d11226ab9ab69d5b30967fbfef1d060b2eedf9"
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
            "node_id": "symbol:httpx/_config.py:Proxy.raw_auth:227",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_config.py",
              "byte_start": 7685,
              "byte_end": 7938,
              "ast_path": "function:Proxy.raw_auth",
              "content_hash": "cbfaadc0233c9799d2f7caa0db1cf3e39e8c826d5e3fb94e3d11523c83be1860"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function raw_auth",
              "symbol_name": "raw_auth",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_config.py:Proxy:201",
            "node_type": "class",
            "source_anchor": {
              "file_path": "httpx/_config.py",
              "byte_start": 6906,
              "byte_end": 8396,
              "ast_path": "class:Proxy",
              "content_hash": "d985925dc092a27aed20a27ff53a0df705be58f6bf32e1f2317d8846ae469b58"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "class Proxy",
              "symbol_name": "Proxy",
              "symbol_type": "class",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_config.py:Timeout.__eq__:140",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_config.py",
              "byte_start": 4760,
              "byte_end": 5045,
              "ast_path": "function:Timeout.__eq__",
              "content_hash": "d50bfbc0f710596d934958cf2fa387b74e2d0e55195342b67484c2e7feefb205"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function __eq__",
              "symbol_name": "__eq__",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_config.py:Timeout.__init__:86",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_config.py",
              "byte_start": 2581,
              "byte_end": 4544,
              "ast_path": "function:Timeout.__init__",
              "content_hash": "abb01af89faac47690f3a680c242578aebd4955cf4e33e22408b00678df2581a"
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
            "node_id": "symbol:httpx/_config.py:Timeout.__repr__:149",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_config.py",
              "byte_start": 5051,
              "byte_end": 5403,
              "ast_path": "function:Timeout.__repr__",
              "content_hash": "2f4f7e2621ca4b6975875a1a3e888bf346a04a86114d4cd5fa7db2fde95f6687"
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
            "node_id": "symbol:httpx/_config.py:Timeout.as_dict:132",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_config.py",
              "byte_start": 4550,
              "byte_end": 4754,
              "ast_path": "function:Timeout.as_dict",
              "content_hash": "6bc685ff914f2dee188f0cff3040bbed8dbf93554b2372c4d864cd1c32959350"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function as_dict",
              "symbol_name": "as_dict",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_config.py:Timeout:72",
            "node_type": "class",
            "source_anchor": {
              "file_path": "httpx/_config.py",
              "byte_start": 2098,
              "byte_end": 5403,
              "ast_path": "class:Timeout",
              "content_hash": "688d5013bbae27ff5a78da1ccf9567a86e0f2bc1234f5af49e09325b5192827a"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "class Timeout",
              "symbol_name": "Timeout",
              "symbol_type": "class",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_config.py:UnsetType:16",
            "node_type": "class",
            "source_anchor": {
              "file_path": "httpx/_config.py",
              "byte_start": 297,
              "byte_end": 322,
              "ast_path": "class:UnsetType",
              "content_hash": "3bd96fffe4f56bcb87e361f26d60c0c2548893f001bb21372df943c49933603b"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "class UnsetType",
              "symbol_name": "UnsetType",
              "symbol_type": "class",
              "tier": 1
            },
            "confidence": 0.92
          },
          {
            "node_id": "symbol:httpx/_config.py:create_ssl_context:23",
            "node_type": "function",
            "source_anchor": {
              "file_path": "httpx/_config.py",
              "byte_start": 367,
              "byte_end": 2095,
              "ast_path": "function:create_ssl_context",
              "content_hash": "9be7e17a2eea5af51fe82d3fff56635820ee42b10412dadf1f95902867e574cc"
            },
            "semantic_contract": {
              "called_by": [],
              "calls": [],
              "complexity_indicators": {
                "decorator_depth": 0,
                "generic_type_param_count": 0
              },
              "language": "python",
              "purpose": "function create_ssl_context",
              "symbol_name": "create_ssl_context",
              "symbol_type": "function",
              "tier": 1
            },
            "confidence": 0.92
          }
        ],
        "edges": [
          {
            "edge_id": "contains:module:httpx/_config.py:symbol:httpx/_config.py:Limits.__eq__:184",
            "edge_type": "contains",
            "from_node": "module:httpx/_config.py",
            "to_node": "symbol:httpx/_config.py:Limits.__eq__:184",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_config.py:symbol:httpx/_config.py:Limits.__init__:173",
            "edge_type": "contains",
            "from_node": "module:httpx/_config.py",
            "to_node": "symbol:httpx/_config.py:Limits.__init__:173",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_config.py:symbol:httpx/_config.py:Limits.__repr__:192",
            "edge_type": "contains",
            "from_node": "module:httpx/_config.py",
            "to_node": "symbol:httpx/_config.py:Limits.__repr__:192",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_config.py:symbol:httpx/_config.py:Limits:159",
            "edge_type": "contains",
            "from_node": "module:httpx/_config.py",
            "to_node": "symbol:httpx/_config.py:Limits:159",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_config.py:symbol:httpx/_config.py:Proxy.__init__:202",
            "edge_type": "contains",
            "from_node": "module:httpx/_config.py",
            "to_node": "symbol:httpx/_config.py:Proxy.__init__:202",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_config.py:symbol:httpx/_config.py:Proxy.__repr__:235",
            "edge_type": "contains",
            "from_node": "module:httpx/_config.py",
            "to_node": "symbol:httpx/_config.py:Proxy.__repr__:235",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_config.py:symbol:httpx/_config.py:Proxy.raw_auth:227",
            "edge_type": "contains",
            "from_node": "module:httpx/_config.py",
            "to_node": "symbol:httpx/_config.py:Proxy.raw_auth:227",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_config.py:symbol:httpx/_config.py:Proxy:201",
            "edge_type": "contains",
            "from_node": "module:httpx/_config.py",
            "to_node": "symbol:httpx/_config.py:Proxy:201",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_config.py:symbol:httpx/_config.py:Timeout.__eq__:140",
            "edge_type": "contains",
            "from_node": "module:httpx/_config.py",
            "to_node": "symbol:httpx/_config.py:Timeout.__eq__:140",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_config.py:symbol:httpx/_config.py:Timeout.__init__:86",
            "edge_type": "contains",
            "from_node": "module:httpx/_config.py",
            "to_node": "symbol:httpx/_config.py:Timeout.__init__:86",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_config.py:symbol:httpx/_config.py:Timeout.__repr__:149",
            "edge_type": "contains",
            "from_node": "module:httpx/_config.py",
            "to_node": "symbol:httpx/_config.py:Timeout.__repr__:149",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_config.py:symbol:httpx/_config.py:Timeout.as_dict:132",
            "edge_type": "contains",
            "from_node": "module:httpx/_config.py",
            "to_node": "symbol:httpx/_config.py:Timeout.as_dict:132",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_config.py:symbol:httpx/_config.py:Timeout:72",
            "edge_type": "contains",
            "from_node": "module:httpx/_config.py",
            "to_node": "symbol:httpx/_config.py:Timeout:72",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_config.py:symbol:httpx/_config.py:UnsetType:16",
            "edge_type": "contains",
            "from_node": "module:httpx/_config.py",
            "to_node": "symbol:httpx/_config.py:UnsetType:16",
            "evidence": {
              "rel": "ast_containment"
            }
          },
          {
            "edge_id": "contains:module:httpx/_config.py:symbol:httpx/_config.py:create_ssl_context:23",
            "edge_type": "contains",
            "from_node": "module:httpx/_config.py",
            "to_node": "symbol:httpx/_config.py:create_ssl_context:23",
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
        "file_path": "httpx/_config.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "module:httpx/_config.py",
      "confidence_trigger": 0.85,
      "output_size_tokens": 834,
      "result": {
        "status": "ok",
        "file_path": "httpx/_config.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 248,
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
            "content": "import os"
          },
          {
            "line_number": 4,
            "content": "import typing"
          },
          {
            "line_number": 5,
            "content": ""
          },
          {
            "line_number": 6,
            "content": "from ._models import Headers"
          },
          {
            "line_number": 7,
            "content": "from ._types import CertTypes, HeaderTypes, TimeoutTypes"
          },
          {
            "line_number": 8,
            "content": "from ._urls import URL"
          },
          {
            "line_number": 9,
            "content": ""
          },
          {
            "line_number": 10,
            "content": "if typing.TYPE_CHECKING:"
          },
          {
            "line_number": 11,
            "content": "    import ssl  # pragma: no cover"
          },
          {
            "line_number": 12,
            "content": ""
          },
          {
            "line_number": 13,
            "content": "__all__ = [\"Limits\", \"Proxy\", \"Timeout\", \"create_ssl_context\"]"
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
            "content": "class UnsetType:"
          },
          {
            "line_number": 17,
            "content": "    pass  # pragma: no cover"
          },
          {
            "line_number": 18,
            "content": ""
          },
          {
            "line_number": 19,
            "content": ""
          },
          {
            "line_number": 20,
            "content": "UNSET = UnsetType()"
          },
          {
            "line_number": 21,
            "content": ""
          },
          {
            "line_number": 22,
            "content": ""
          },
          {
            "line_number": 23,
            "content": "def create_ssl_context("
          },
          {
            "line_number": 24,
            "content": "    verify: ssl.SSLContext | str | bool = True,"
          },
          {
            "line_number": 25,
            "content": "    cert: CertTypes | None = None,"
          },
          {
            "line_number": 26,
            "content": "    trust_env: bool = True,"
          },
          {
            "line_number": 27,
            "content": ") -> ssl.SSLContext:"
          },
          {
            "line_number": 28,
            "content": "    import ssl"
          },
          {
            "line_number": 29,
            "content": "    import warnings"
          },
          {
            "line_number": 30,
            "content": ""
          },
          {
            "line_number": 31,
            "content": "    import certifi"
          },
          {
            "line_number": 32,
            "content": ""
          },
          {
            "line_number": 33,
            "content": "    if verify is True:"
          },
          {
            "line_number": 34,
            "content": "        if trust_env and os.environ.get(\"SSL_CERT_FILE\"):  # pragma: nocover"
          },
          {
            "line_number": 35,
            "content": "            ctx = ssl.create_default_context(cafile=os.environ[\"SSL_CERT_FILE\"])"
          },
          {
            "line_number": 36,
            "content": "        elif trust_env and os.environ.get(\"SSL_CERT_DIR\"):  # pragma: nocover"
          },
          {
            "line_number": 37,
            "content": "            ctx = ssl.create_default_context(capath=os.environ[\"SSL_CERT_DIR\"])"
          },
          {
            "line_number": 38,
            "content": "        else:"
          },
          {
            "line_number": 39,
            "content": "            # Default case..."
          },
          {
            "line_number": 40,
            "content": "            ctx = ssl.create_default_context(cafile=certifi.where())"
          },
          {
            "line_number": 41,
            "content": "    elif verify is False:"
          },
          {
            "line_number": 42,
            "content": "        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)"
          },
          {
            "line_number": 43,
            "content": "        ctx.check_hostname = False"
          },
          {
            "line_number": 44,
            "content": "        ctx.verify_mode = ssl.CERT_NONE"
          },
          {
            "line_number": 45,
            "content": "    elif isinstance(verify, str):  # pragma: nocover"
          },
          {
            "line_number": 46,
            "content": "        message = ("
          },
          {
            "line_number": 47,
            "content": "            \"`verify=<str>` is deprecated. \""
          },
          {
            "line_number": 48,
            "content": "            \"Use `verify=ssl.create_default_context(cafile=...)` \""
          },
          {
            "line_number": 49,
            "content": "            \"or `verify=ssl.create_default_context(capath=...)` instead.\""
          },
          {
            "line_number": 50,
            "content": "        )"
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "httpx/_client.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "symbol:httpx/_client.py:AsyncClient.__aenter__:1990",
      "confidence_trigger": 0.77,
      "output_size_tokens": 757,
      "result": {
        "status": "ok",
        "file_path": "httpx/_client.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 2019,
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
            "content": "import datetime"
          },
          {
            "line_number": 4,
            "content": "import enum"
          },
          {
            "line_number": 5,
            "content": "import logging"
          },
          {
            "line_number": 6,
            "content": "import time"
          },
          {
            "line_number": 7,
            "content": "import typing"
          },
          {
            "line_number": 8,
            "content": "import warnings"
          },
          {
            "line_number": 9,
            "content": "from contextlib import asynccontextmanager, contextmanager"
          },
          {
            "line_number": 10,
            "content": "from types import TracebackType"
          },
          {
            "line_number": 11,
            "content": ""
          },
          {
            "line_number": 12,
            "content": "from .__version__ import __version__"
          },
          {
            "line_number": 13,
            "content": "from ._auth import Auth, BasicAuth, FunctionAuth"
          },
          {
            "line_number": 14,
            "content": "from ._config import ("
          },
          {
            "line_number": 15,
            "content": "    DEFAULT_LIMITS,"
          },
          {
            "line_number": 16,
            "content": "    DEFAULT_MAX_REDIRECTS,"
          },
          {
            "line_number": 17,
            "content": "    DEFAULT_TIMEOUT_CONFIG,"
          },
          {
            "line_number": 18,
            "content": "    Limits,"
          },
          {
            "line_number": 19,
            "content": "    Proxy,"
          },
          {
            "line_number": 20,
            "content": "    Timeout,"
          },
          {
            "line_number": 21,
            "content": ")"
          },
          {
            "line_number": 22,
            "content": "from ._decoders import SUPPORTED_DECODERS"
          },
          {
            "line_number": 23,
            "content": "from ._exceptions import ("
          },
          {
            "line_number": 24,
            "content": "    InvalidURL,"
          },
          {
            "line_number": 25,
            "content": "    RemoteProtocolError,"
          },
          {
            "line_number": 26,
            "content": "    TooManyRedirects,"
          },
          {
            "line_number": 27,
            "content": "    request_context,"
          },
          {
            "line_number": 28,
            "content": ")"
          },
          {
            "line_number": 29,
            "content": "from ._models import Cookies, Headers, Request, Response"
          },
          {
            "line_number": 30,
            "content": "from ._status_codes import codes"
          },
          {
            "line_number": 31,
            "content": "from ._transports.base import AsyncBaseTransport, BaseTransport"
          },
          {
            "line_number": 32,
            "content": "from ._transports.default import AsyncHTTPTransport, HTTPTransport"
          },
          {
            "line_number": 33,
            "content": "from ._types import ("
          },
          {
            "line_number": 34,
            "content": "    AsyncByteStream,"
          },
          {
            "line_number": 35,
            "content": "    AuthTypes,"
          },
          {
            "line_number": 36,
            "content": "    CertTypes,"
          },
          {
            "line_number": 37,
            "content": "    CookieTypes,"
          },
          {
            "line_number": 38,
            "content": "    HeaderTypes,"
          },
          {
            "line_number": 39,
            "content": "    ProxyTypes,"
          },
          {
            "line_number": 40,
            "content": "    QueryParamTypes,"
          },
          {
            "line_number": 41,
            "content": "    RequestContent,"
          },
          {
            "line_number": 42,
            "content": "    RequestData,"
          },
          {
            "line_number": 43,
            "content": "    RequestExtensions,"
          },
          {
            "line_number": 44,
            "content": "    RequestFiles,"
          },
          {
            "line_number": 45,
            "content": "    SyncByteStream,"
          },
          {
            "line_number": 46,
            "content": "    TimeoutTypes,"
          },
          {
            "line_number": 47,
            "content": ")"
          },
          {
            "line_number": 48,
            "content": "from ._urls import URL, QueryParams"
          },
          {
            "line_number": 49,
            "content": "from ._utils import URLPattern, get_environment_proxies"
          },
          {
            "line_number": 50,
            "content": ""
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "httpx/_client.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "symbol:httpx/_client.py:AsyncClient.__aexit__:2008",
      "confidence_trigger": 0.77,
      "output_size_tokens": 757,
      "result": {
        "status": "ok",
        "file_path": "httpx/_client.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 2019,
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
            "content": "import datetime"
          },
          {
            "line_number": 4,
            "content": "import enum"
          },
          {
            "line_number": 5,
            "content": "import logging"
          },
          {
            "line_number": 6,
            "content": "import time"
          },
          {
            "line_number": 7,
            "content": "import typing"
          },
          {
            "line_number": 8,
            "content": "import warnings"
          },
          {
            "line_number": 9,
            "content": "from contextlib import asynccontextmanager, contextmanager"
          },
          {
            "line_number": 10,
            "content": "from types import TracebackType"
          },
          {
            "line_number": 11,
            "content": ""
          },
          {
            "line_number": 12,
            "content": "from .__version__ import __version__"
          },
          {
            "line_number": 13,
            "content": "from ._auth import Auth, BasicAuth, FunctionAuth"
          },
          {
            "line_number": 14,
            "content": "from ._config import ("
          },
          {
            "line_number": 15,
            "content": "    DEFAULT_LIMITS,"
          },
          {
            "line_number": 16,
            "content": "    DEFAULT_MAX_REDIRECTS,"
          },
          {
            "line_number": 17,
            "content": "    DEFAULT_TIMEOUT_CONFIG,"
          },
          {
            "line_number": 18,
            "content": "    Limits,"
          },
          {
            "line_number": 19,
            "content": "    Proxy,"
          },
          {
            "line_number": 20,
            "content": "    Timeout,"
          },
          {
            "line_number": 21,
            "content": ")"
          },
          {
            "line_number": 22,
            "content": "from ._decoders import SUPPORTED_DECODERS"
          },
          {
            "line_number": 23,
            "content": "from ._exceptions import ("
          },
          {
            "line_number": 24,
            "content": "    InvalidURL,"
          },
          {
            "line_number": 25,
            "content": "    RemoteProtocolError,"
          },
          {
            "line_number": 26,
            "content": "    TooManyRedirects,"
          },
          {
            "line_number": 27,
            "content": "    request_context,"
          },
          {
            "line_number": 28,
            "content": ")"
          },
          {
            "line_number": 29,
            "content": "from ._models import Cookies, Headers, Request, Response"
          },
          {
            "line_number": 30,
            "content": "from ._status_codes import codes"
          },
          {
            "line_number": 31,
            "content": "from ._transports.base import AsyncBaseTransport, BaseTransport"
          },
          {
            "line_number": 32,
            "content": "from ._transports.default import AsyncHTTPTransport, HTTPTransport"
          },
          {
            "line_number": 33,
            "content": "from ._types import ("
          },
          {
            "line_number": 34,
            "content": "    AsyncByteStream,"
          },
          {
            "line_number": 35,
            "content": "    AuthTypes,"
          },
          {
            "line_number": 36,
            "content": "    CertTypes,"
          },
          {
            "line_number": 37,
            "content": "    CookieTypes,"
          },
          {
            "line_number": 38,
            "content": "    HeaderTypes,"
          },
          {
            "line_number": 39,
            "content": "    ProxyTypes,"
          },
          {
            "line_number": 40,
            "content": "    QueryParamTypes,"
          },
          {
            "line_number": 41,
            "content": "    RequestContent,"
          },
          {
            "line_number": 42,
            "content": "    RequestData,"
          },
          {
            "line_number": 43,
            "content": "    RequestExtensions,"
          },
          {
            "line_number": 44,
            "content": "    RequestFiles,"
          },
          {
            "line_number": 45,
            "content": "    SyncByteStream,"
          },
          {
            "line_number": 46,
            "content": "    TimeoutTypes,"
          },
          {
            "line_number": 47,
            "content": ")"
          },
          {
            "line_number": 48,
            "content": "from ._urls import URL, QueryParams"
          },
          {
            "line_number": 49,
            "content": "from ._utils import URLPattern, get_environment_proxies"
          },
          {
            "line_number": 50,
            "content": ""
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "httpx/_client.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "symbol:httpx/_client.py:BaseClient._build_auth:445",
      "confidence_trigger": 0.77,
      "output_size_tokens": 757,
      "result": {
        "status": "ok",
        "file_path": "httpx/_client.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 2019,
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
            "content": "import datetime"
          },
          {
            "line_number": 4,
            "content": "import enum"
          },
          {
            "line_number": 5,
            "content": "import logging"
          },
          {
            "line_number": 6,
            "content": "import time"
          },
          {
            "line_number": 7,
            "content": "import typing"
          },
          {
            "line_number": 8,
            "content": "import warnings"
          },
          {
            "line_number": 9,
            "content": "from contextlib import asynccontextmanager, contextmanager"
          },
          {
            "line_number": 10,
            "content": "from types import TracebackType"
          },
          {
            "line_number": 11,
            "content": ""
          },
          {
            "line_number": 12,
            "content": "from .__version__ import __version__"
          },
          {
            "line_number": 13,
            "content": "from ._auth import Auth, BasicAuth, FunctionAuth"
          },
          {
            "line_number": 14,
            "content": "from ._config import ("
          },
          {
            "line_number": 15,
            "content": "    DEFAULT_LIMITS,"
          },
          {
            "line_number": 16,
            "content": "    DEFAULT_MAX_REDIRECTS,"
          },
          {
            "line_number": 17,
            "content": "    DEFAULT_TIMEOUT_CONFIG,"
          },
          {
            "line_number": 18,
            "content": "    Limits,"
          },
          {
            "line_number": 19,
            "content": "    Proxy,"
          },
          {
            "line_number": 20,
            "content": "    Timeout,"
          },
          {
            "line_number": 21,
            "content": ")"
          },
          {
            "line_number": 22,
            "content": "from ._decoders import SUPPORTED_DECODERS"
          },
          {
            "line_number": 23,
            "content": "from ._exceptions import ("
          },
          {
            "line_number": 24,
            "content": "    InvalidURL,"
          },
          {
            "line_number": 25,
            "content": "    RemoteProtocolError,"
          },
          {
            "line_number": 26,
            "content": "    TooManyRedirects,"
          },
          {
            "line_number": 27,
            "content": "    request_context,"
          },
          {
            "line_number": 28,
            "content": ")"
          },
          {
            "line_number": 29,
            "content": "from ._models import Cookies, Headers, Request, Response"
          },
          {
            "line_number": 30,
            "content": "from ._status_codes import codes"
          },
          {
            "line_number": 31,
            "content": "from ._transports.base import AsyncBaseTransport, BaseTransport"
          },
          {
            "line_number": 32,
            "content": "from ._transports.default import AsyncHTTPTransport, HTTPTransport"
          },
          {
            "line_number": 33,
            "content": "from ._types import ("
          },
          {
            "line_number": 34,
            "content": "    AsyncByteStream,"
          },
          {
            "line_number": 35,
            "content": "    AuthTypes,"
          },
          {
            "line_number": 36,
            "content": "    CertTypes,"
          },
          {
            "line_number": 37,
            "content": "    CookieTypes,"
          },
          {
            "line_number": 38,
            "content": "    HeaderTypes,"
          },
          {
            "line_number": 39,
            "content": "    ProxyTypes,"
          },
          {
            "line_number": 40,
            "content": "    QueryParamTypes,"
          },
          {
            "line_number": 41,
            "content": "    RequestContent,"
          },
          {
            "line_number": 42,
            "content": "    RequestData,"
          },
          {
            "line_number": 43,
            "content": "    RequestExtensions,"
          },
          {
            "line_number": 44,
            "content": "    RequestFiles,"
          },
          {
            "line_number": 45,
            "content": "    SyncByteStream,"
          },
          {
            "line_number": 46,
            "content": "    TimeoutTypes,"
          },
          {
            "line_number": 47,
            "content": ")"
          },
          {
            "line_number": 48,
            "content": "from ._urls import URL, QueryParams"
          },
          {
            "line_number": 49,
            "content": "from ._utils import URLPattern, get_environment_proxies"
          },
          {
            "line_number": 50,
            "content": ""
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "httpx/_client.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475",
      "confidence_trigger": 0.57,
      "output_size_tokens": 757,
      "result": {
        "status": "ok",
        "file_path": "httpx/_client.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 2019,
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
            "content": "import datetime"
          },
          {
            "line_number": 4,
            "content": "import enum"
          },
          {
            "line_number": 5,
            "content": "import logging"
          },
          {
            "line_number": 6,
            "content": "import time"
          },
          {
            "line_number": 7,
            "content": "import typing"
          },
          {
            "line_number": 8,
            "content": "import warnings"
          },
          {
            "line_number": 9,
            "content": "from contextlib import asynccontextmanager, contextmanager"
          },
          {
            "line_number": 10,
            "content": "from types import TracebackType"
          },
          {
            "line_number": 11,
            "content": ""
          },
          {
            "line_number": 12,
            "content": "from .__version__ import __version__"
          },
          {
            "line_number": 13,
            "content": "from ._auth import Auth, BasicAuth, FunctionAuth"
          },
          {
            "line_number": 14,
            "content": "from ._config import ("
          },
          {
            "line_number": 15,
            "content": "    DEFAULT_LIMITS,"
          },
          {
            "line_number": 16,
            "content": "    DEFAULT_MAX_REDIRECTS,"
          },
          {
            "line_number": 17,
            "content": "    DEFAULT_TIMEOUT_CONFIG,"
          },
          {
            "line_number": 18,
            "content": "    Limits,"
          },
          {
            "line_number": 19,
            "content": "    Proxy,"
          },
          {
            "line_number": 20,
            "content": "    Timeout,"
          },
          {
            "line_number": 21,
            "content": ")"
          },
          {
            "line_number": 22,
            "content": "from ._decoders import SUPPORTED_DECODERS"
          },
          {
            "line_number": 23,
            "content": "from ._exceptions import ("
          },
          {
            "line_number": 24,
            "content": "    InvalidURL,"
          },
          {
            "line_number": 25,
            "content": "    RemoteProtocolError,"
          },
          {
            "line_number": 26,
            "content": "    TooManyRedirects,"
          },
          {
            "line_number": 27,
            "content": "    request_context,"
          },
          {
            "line_number": 28,
            "content": ")"
          },
          {
            "line_number": 29,
            "content": "from ._models import Cookies, Headers, Request, Response"
          },
          {
            "line_number": 30,
            "content": "from ._status_codes import codes"
          },
          {
            "line_number": 31,
            "content": "from ._transports.base import AsyncBaseTransport, BaseTransport"
          },
          {
            "line_number": 32,
            "content": "from ._transports.default import AsyncHTTPTransport, HTTPTransport"
          },
          {
            "line_number": 33,
            "content": "from ._types import ("
          },
          {
            "line_number": 34,
            "content": "    AsyncByteStream,"
          },
          {
            "line_number": 35,
            "content": "    AuthTypes,"
          },
          {
            "line_number": 36,
            "content": "    CertTypes,"
          },
          {
            "line_number": 37,
            "content": "    CookieTypes,"
          },
          {
            "line_number": 38,
            "content": "    HeaderTypes,"
          },
          {
            "line_number": 39,
            "content": "    ProxyTypes,"
          },
          {
            "line_number": 40,
            "content": "    QueryParamTypes,"
          },
          {
            "line_number": 41,
            "content": "    RequestContent,"
          },
          {
            "line_number": 42,
            "content": "    RequestData,"
          },
          {
            "line_number": 43,
            "content": "    RequestExtensions,"
          },
          {
            "line_number": 44,
            "content": "    RequestFiles,"
          },
          {
            "line_number": 45,
            "content": "    SyncByteStream,"
          },
          {
            "line_number": 46,
            "content": "    TimeoutTypes,"
          },
          {
            "line_number": 47,
            "content": ")"
          },
          {
            "line_number": 48,
            "content": "from ._urls import URL, QueryParams"
          },
          {
            "line_number": 49,
            "content": "from ._utils import URLPattern, get_environment_proxies"
          },
          {
            "line_number": 50,
            "content": ""
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "httpx/_client.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "symbol:httpx/_client.py:BaseClient._build_request_auth:457",
      "confidence_trigger": 0.77,
      "output_size_tokens": 757,
      "result": {
        "status": "ok",
        "file_path": "httpx/_client.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 2019,
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
            "content": "import datetime"
          },
          {
            "line_number": 4,
            "content": "import enum"
          },
          {
            "line_number": 5,
            "content": "import logging"
          },
          {
            "line_number": 6,
            "content": "import time"
          },
          {
            "line_number": 7,
            "content": "import typing"
          },
          {
            "line_number": 8,
            "content": "import warnings"
          },
          {
            "line_number": 9,
            "content": "from contextlib import asynccontextmanager, contextmanager"
          },
          {
            "line_number": 10,
            "content": "from types import TracebackType"
          },
          {
            "line_number": 11,
            "content": ""
          },
          {
            "line_number": 12,
            "content": "from .__version__ import __version__"
          },
          {
            "line_number": 13,
            "content": "from ._auth import Auth, BasicAuth, FunctionAuth"
          },
          {
            "line_number": 14,
            "content": "from ._config import ("
          },
          {
            "line_number": 15,
            "content": "    DEFAULT_LIMITS,"
          },
          {
            "line_number": 16,
            "content": "    DEFAULT_MAX_REDIRECTS,"
          },
          {
            "line_number": 17,
            "content": "    DEFAULT_TIMEOUT_CONFIG,"
          },
          {
            "line_number": 18,
            "content": "    Limits,"
          },
          {
            "line_number": 19,
            "content": "    Proxy,"
          },
          {
            "line_number": 20,
            "content": "    Timeout,"
          },
          {
            "line_number": 21,
            "content": ")"
          },
          {
            "line_number": 22,
            "content": "from ._decoders import SUPPORTED_DECODERS"
          },
          {
            "line_number": 23,
            "content": "from ._exceptions import ("
          },
          {
            "line_number": 24,
            "content": "    InvalidURL,"
          },
          {
            "line_number": 25,
            "content": "    RemoteProtocolError,"
          },
          {
            "line_number": 26,
            "content": "    TooManyRedirects,"
          },
          {
            "line_number": 27,
            "content": "    request_context,"
          },
          {
            "line_number": 28,
            "content": ")"
          },
          {
            "line_number": 29,
            "content": "from ._models import Cookies, Headers, Request, Response"
          },
          {
            "line_number": 30,
            "content": "from ._status_codes import codes"
          },
          {
            "line_number": 31,
            "content": "from ._transports.base import AsyncBaseTransport, BaseTransport"
          },
          {
            "line_number": 32,
            "content": "from ._transports.default import AsyncHTTPTransport, HTTPTransport"
          },
          {
            "line_number": 33,
            "content": "from ._types import ("
          },
          {
            "line_number": 34,
            "content": "    AsyncByteStream,"
          },
          {
            "line_number": 35,
            "content": "    AuthTypes,"
          },
          {
            "line_number": 36,
            "content": "    CertTypes,"
          },
          {
            "line_number": 37,
            "content": "    CookieTypes,"
          },
          {
            "line_number": 38,
            "content": "    HeaderTypes,"
          },
          {
            "line_number": 39,
            "content": "    ProxyTypes,"
          },
          {
            "line_number": 40,
            "content": "    QueryParamTypes,"
          },
          {
            "line_number": 41,
            "content": "    RequestContent,"
          },
          {
            "line_number": 42,
            "content": "    RequestData,"
          },
          {
            "line_number": 43,
            "content": "    RequestExtensions,"
          },
          {
            "line_number": 44,
            "content": "    RequestFiles,"
          },
          {
            "line_number": 45,
            "content": "    SyncByteStream,"
          },
          {
            "line_number": 46,
            "content": "    TimeoutTypes,"
          },
          {
            "line_number": 47,
            "content": ")"
          },
          {
            "line_number": 48,
            "content": "from ._urls import URL, QueryParams"
          },
          {
            "line_number": 49,
            "content": "from ._utils import URLPattern, get_environment_proxies"
          },
          {
            "line_number": 50,
            "content": ""
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "httpx/_client.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "symbol:httpx/_client.py:BaseClient._merge_cookies:413",
      "confidence_trigger": 0.77,
      "output_size_tokens": 757,
      "result": {
        "status": "ok",
        "file_path": "httpx/_client.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 2019,
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
            "content": "import datetime"
          },
          {
            "line_number": 4,
            "content": "import enum"
          },
          {
            "line_number": 5,
            "content": "import logging"
          },
          {
            "line_number": 6,
            "content": "import time"
          },
          {
            "line_number": 7,
            "content": "import typing"
          },
          {
            "line_number": 8,
            "content": "import warnings"
          },
          {
            "line_number": 9,
            "content": "from contextlib import asynccontextmanager, contextmanager"
          },
          {
            "line_number": 10,
            "content": "from types import TracebackType"
          },
          {
            "line_number": 11,
            "content": ""
          },
          {
            "line_number": 12,
            "content": "from .__version__ import __version__"
          },
          {
            "line_number": 13,
            "content": "from ._auth import Auth, BasicAuth, FunctionAuth"
          },
          {
            "line_number": 14,
            "content": "from ._config import ("
          },
          {
            "line_number": 15,
            "content": "    DEFAULT_LIMITS,"
          },
          {
            "line_number": 16,
            "content": "    DEFAULT_MAX_REDIRECTS,"
          },
          {
            "line_number": 17,
            "content": "    DEFAULT_TIMEOUT_CONFIG,"
          },
          {
            "line_number": 18,
            "content": "    Limits,"
          },
          {
            "line_number": 19,
            "content": "    Proxy,"
          },
          {
            "line_number": 20,
            "content": "    Timeout,"
          },
          {
            "line_number": 21,
            "content": ")"
          },
          {
            "line_number": 22,
            "content": "from ._decoders import SUPPORTED_DECODERS"
          },
          {
            "line_number": 23,
            "content": "from ._exceptions import ("
          },
          {
            "line_number": 24,
            "content": "    InvalidURL,"
          },
          {
            "line_number": 25,
            "content": "    RemoteProtocolError,"
          },
          {
            "line_number": 26,
            "content": "    TooManyRedirects,"
          },
          {
            "line_number": 27,
            "content": "    request_context,"
          },
          {
            "line_number": 28,
            "content": ")"
          },
          {
            "line_number": 29,
            "content": "from ._models import Cookies, Headers, Request, Response"
          },
          {
            "line_number": 30,
            "content": "from ._status_codes import codes"
          },
          {
            "line_number": 31,
            "content": "from ._transports.base import AsyncBaseTransport, BaseTransport"
          },
          {
            "line_number": 32,
            "content": "from ._transports.default import AsyncHTTPTransport, HTTPTransport"
          },
          {
            "line_number": 33,
            "content": "from ._types import ("
          },
          {
            "line_number": 34,
            "content": "    AsyncByteStream,"
          },
          {
            "line_number": 35,
            "content": "    AuthTypes,"
          },
          {
            "line_number": 36,
            "content": "    CertTypes,"
          },
          {
            "line_number": 37,
            "content": "    CookieTypes,"
          },
          {
            "line_number": 38,
            "content": "    HeaderTypes,"
          },
          {
            "line_number": 39,
            "content": "    ProxyTypes,"
          },
          {
            "line_number": 40,
            "content": "    QueryParamTypes,"
          },
          {
            "line_number": 41,
            "content": "    RequestContent,"
          },
          {
            "line_number": 42,
            "content": "    RequestData,"
          },
          {
            "line_number": 43,
            "content": "    RequestExtensions,"
          },
          {
            "line_number": 44,
            "content": "    RequestFiles,"
          },
          {
            "line_number": 45,
            "content": "    SyncByteStream,"
          },
          {
            "line_number": 46,
            "content": "    TimeoutTypes,"
          },
          {
            "line_number": 47,
            "content": ")"
          },
          {
            "line_number": 48,
            "content": "from ._urls import URL, QueryParams"
          },
          {
            "line_number": 49,
            "content": "from ._utils import URLPattern, get_environment_proxies"
          },
          {
            "line_number": 50,
            "content": ""
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "httpx/_client.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "symbol:httpx/_client.py:BaseClient._merge_headers:424",
      "confidence_trigger": 0.77,
      "output_size_tokens": 757,
      "result": {
        "status": "ok",
        "file_path": "httpx/_client.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 2019,
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
            "content": "import datetime"
          },
          {
            "line_number": 4,
            "content": "import enum"
          },
          {
            "line_number": 5,
            "content": "import logging"
          },
          {
            "line_number": 6,
            "content": "import time"
          },
          {
            "line_number": 7,
            "content": "import typing"
          },
          {
            "line_number": 8,
            "content": "import warnings"
          },
          {
            "line_number": 9,
            "content": "from contextlib import asynccontextmanager, contextmanager"
          },
          {
            "line_number": 10,
            "content": "from types import TracebackType"
          },
          {
            "line_number": 11,
            "content": ""
          },
          {
            "line_number": 12,
            "content": "from .__version__ import __version__"
          },
          {
            "line_number": 13,
            "content": "from ._auth import Auth, BasicAuth, FunctionAuth"
          },
          {
            "line_number": 14,
            "content": "from ._config import ("
          },
          {
            "line_number": 15,
            "content": "    DEFAULT_LIMITS,"
          },
          {
            "line_number": 16,
            "content": "    DEFAULT_MAX_REDIRECTS,"
          },
          {
            "line_number": 17,
            "content": "    DEFAULT_TIMEOUT_CONFIG,"
          },
          {
            "line_number": 18,
            "content": "    Limits,"
          },
          {
            "line_number": 19,
            "content": "    Proxy,"
          },
          {
            "line_number": 20,
            "content": "    Timeout,"
          },
          {
            "line_number": 21,
            "content": ")"
          },
          {
            "line_number": 22,
            "content": "from ._decoders import SUPPORTED_DECODERS"
          },
          {
            "line_number": 23,
            "content": "from ._exceptions import ("
          },
          {
            "line_number": 24,
            "content": "    InvalidURL,"
          },
          {
            "line_number": 25,
            "content": "    RemoteProtocolError,"
          },
          {
            "line_number": 26,
            "content": "    TooManyRedirects,"
          },
          {
            "line_number": 27,
            "content": "    request_context,"
          },
          {
            "line_number": 28,
            "content": ")"
          },
          {
            "line_number": 29,
            "content": "from ._models import Cookies, Headers, Request, Response"
          },
          {
            "line_number": 30,
            "content": "from ._status_codes import codes"
          },
          {
            "line_number": 31,
            "content": "from ._transports.base import AsyncBaseTransport, BaseTransport"
          },
          {
            "line_number": 32,
            "content": "from ._transports.default import AsyncHTTPTransport, HTTPTransport"
          },
          {
            "line_number": 33,
            "content": "from ._types import ("
          },
          {
            "line_number": 34,
            "content": "    AsyncByteStream,"
          },
          {
            "line_number": 35,
            "content": "    AuthTypes,"
          },
          {
            "line_number": 36,
            "content": "    CertTypes,"
          },
          {
            "line_number": 37,
            "content": "    CookieTypes,"
          },
          {
            "line_number": 38,
            "content": "    HeaderTypes,"
          },
          {
            "line_number": 39,
            "content": "    ProxyTypes,"
          },
          {
            "line_number": 40,
            "content": "    QueryParamTypes,"
          },
          {
            "line_number": 41,
            "content": "    RequestContent,"
          },
          {
            "line_number": 42,
            "content": "    RequestData,"
          },
          {
            "line_number": 43,
            "content": "    RequestExtensions,"
          },
          {
            "line_number": 44,
            "content": "    RequestFiles,"
          },
          {
            "line_number": 45,
            "content": "    SyncByteStream,"
          },
          {
            "line_number": 46,
            "content": "    TimeoutTypes,"
          },
          {
            "line_number": 47,
            "content": ")"
          },
          {
            "line_number": 48,
            "content": "from ._urls import URL, QueryParams"
          },
          {
            "line_number": 49,
            "content": "from ._utils import URLPattern, get_environment_proxies"
          },
          {
            "line_number": 50,
            "content": ""
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "httpx/_client.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "symbol:httpx/_client.py:BaseClient._merge_queryparams:433",
      "confidence_trigger": 0.77,
      "output_size_tokens": 757,
      "result": {
        "status": "ok",
        "file_path": "httpx/_client.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 2019,
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
            "content": "import datetime"
          },
          {
            "line_number": 4,
            "content": "import enum"
          },
          {
            "line_number": 5,
            "content": "import logging"
          },
          {
            "line_number": 6,
            "content": "import time"
          },
          {
            "line_number": 7,
            "content": "import typing"
          },
          {
            "line_number": 8,
            "content": "import warnings"
          },
          {
            "line_number": 9,
            "content": "from contextlib import asynccontextmanager, contextmanager"
          },
          {
            "line_number": 10,
            "content": "from types import TracebackType"
          },
          {
            "line_number": 11,
            "content": ""
          },
          {
            "line_number": 12,
            "content": "from .__version__ import __version__"
          },
          {
            "line_number": 13,
            "content": "from ._auth import Auth, BasicAuth, FunctionAuth"
          },
          {
            "line_number": 14,
            "content": "from ._config import ("
          },
          {
            "line_number": 15,
            "content": "    DEFAULT_LIMITS,"
          },
          {
            "line_number": 16,
            "content": "    DEFAULT_MAX_REDIRECTS,"
          },
          {
            "line_number": 17,
            "content": "    DEFAULT_TIMEOUT_CONFIG,"
          },
          {
            "line_number": 18,
            "content": "    Limits,"
          },
          {
            "line_number": 19,
            "content": "    Proxy,"
          },
          {
            "line_number": 20,
            "content": "    Timeout,"
          },
          {
            "line_number": 21,
            "content": ")"
          },
          {
            "line_number": 22,
            "content": "from ._decoders import SUPPORTED_DECODERS"
          },
          {
            "line_number": 23,
            "content": "from ._exceptions import ("
          },
          {
            "line_number": 24,
            "content": "    InvalidURL,"
          },
          {
            "line_number": 25,
            "content": "    RemoteProtocolError,"
          },
          {
            "line_number": 26,
            "content": "    TooManyRedirects,"
          },
          {
            "line_number": 27,
            "content": "    request_context,"
          },
          {
            "line_number": 28,
            "content": ")"
          },
          {
            "line_number": 29,
            "content": "from ._models import Cookies, Headers, Request, Response"
          },
          {
            "line_number": 30,
            "content": "from ._status_codes import codes"
          },
          {
            "line_number": 31,
            "content": "from ._transports.base import AsyncBaseTransport, BaseTransport"
          },
          {
            "line_number": 32,
            "content": "from ._transports.default import AsyncHTTPTransport, HTTPTransport"
          },
          {
            "line_number": 33,
            "content": "from ._types import ("
          },
          {
            "line_number": 34,
            "content": "    AsyncByteStream,"
          },
          {
            "line_number": 35,
            "content": "    AuthTypes,"
          },
          {
            "line_number": 36,
            "content": "    CertTypes,"
          },
          {
            "line_number": 37,
            "content": "    CookieTypes,"
          },
          {
            "line_number": 38,
            "content": "    HeaderTypes,"
          },
          {
            "line_number": 39,
            "content": "    ProxyTypes,"
          },
          {
            "line_number": 40,
            "content": "    QueryParamTypes,"
          },
          {
            "line_number": 41,
            "content": "    RequestContent,"
          },
          {
            "line_number": 42,
            "content": "    RequestData,"
          },
          {
            "line_number": 43,
            "content": "    RequestExtensions,"
          },
          {
            "line_number": 44,
            "content": "    RequestFiles,"
          },
          {
            "line_number": 45,
            "content": "    SyncByteStream,"
          },
          {
            "line_number": 46,
            "content": "    TimeoutTypes,"
          },
          {
            "line_number": 47,
            "content": ")"
          },
          {
            "line_number": 48,
            "content": "from ._urls import URL, QueryParams"
          },
          {
            "line_number": 49,
            "content": "from ._utils import URLPattern, get_environment_proxies"
          },
          {
            "line_number": 50,
            "content": ""
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "httpx/_client.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "symbol:httpx/_client.py:BaseClient._merge_url:391",
      "confidence_trigger": 0.77,
      "output_size_tokens": 757,
      "result": {
        "status": "ok",
        "file_path": "httpx/_client.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 2019,
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
            "content": "import datetime"
          },
          {
            "line_number": 4,
            "content": "import enum"
          },
          {
            "line_number": 5,
            "content": "import logging"
          },
          {
            "line_number": 6,
            "content": "import time"
          },
          {
            "line_number": 7,
            "content": "import typing"
          },
          {
            "line_number": 8,
            "content": "import warnings"
          },
          {
            "line_number": 9,
            "content": "from contextlib import asynccontextmanager, contextmanager"
          },
          {
            "line_number": 10,
            "content": "from types import TracebackType"
          },
          {
            "line_number": 11,
            "content": ""
          },
          {
            "line_number": 12,
            "content": "from .__version__ import __version__"
          },
          {
            "line_number": 13,
            "content": "from ._auth import Auth, BasicAuth, FunctionAuth"
          },
          {
            "line_number": 14,
            "content": "from ._config import ("
          },
          {
            "line_number": 15,
            "content": "    DEFAULT_LIMITS,"
          },
          {
            "line_number": 16,
            "content": "    DEFAULT_MAX_REDIRECTS,"
          },
          {
            "line_number": 17,
            "content": "    DEFAULT_TIMEOUT_CONFIG,"
          },
          {
            "line_number": 18,
            "content": "    Limits,"
          },
          {
            "line_number": 19,
            "content": "    Proxy,"
          },
          {
            "line_number": 20,
            "content": "    Timeout,"
          },
          {
            "line_number": 21,
            "content": ")"
          },
          {
            "line_number": 22,
            "content": "from ._decoders import SUPPORTED_DECODERS"
          },
          {
            "line_number": 23,
            "content": "from ._exceptions import ("
          },
          {
            "line_number": 24,
            "content": "    InvalidURL,"
          },
          {
            "line_number": 25,
            "content": "    RemoteProtocolError,"
          },
          {
            "line_number": 26,
            "content": "    TooManyRedirects,"
          },
          {
            "line_number": 27,
            "content": "    request_context,"
          },
          {
            "line_number": 28,
            "content": ")"
          },
          {
            "line_number": 29,
            "content": "from ._models import Cookies, Headers, Request, Response"
          },
          {
            "line_number": 30,
            "content": "from ._status_codes import codes"
          },
          {
            "line_number": 31,
            "content": "from ._transports.base import AsyncBaseTransport, BaseTransport"
          },
          {
            "line_number": 32,
            "content": "from ._transports.default import AsyncHTTPTransport, HTTPTransport"
          },
          {
            "line_number": 33,
            "content": "from ._types import ("
          },
          {
            "line_number": 34,
            "content": "    AsyncByteStream,"
          },
          {
            "line_number": 35,
            "content": "    AuthTypes,"
          },
          {
            "line_number": 36,
            "content": "    CertTypes,"
          },
          {
            "line_number": 37,
            "content": "    CookieTypes,"
          },
          {
            "line_number": 38,
            "content": "    HeaderTypes,"
          },
          {
            "line_number": 39,
            "content": "    ProxyTypes,"
          },
          {
            "line_number": 40,
            "content": "    QueryParamTypes,"
          },
          {
            "line_number": 41,
            "content": "    RequestContent,"
          },
          {
            "line_number": 42,
            "content": "    RequestData,"
          },
          {
            "line_number": 43,
            "content": "    RequestExtensions,"
          },
          {
            "line_number": 44,
            "content": "    RequestFiles,"
          },
          {
            "line_number": 45,
            "content": "    SyncByteStream,"
          },
          {
            "line_number": 46,
            "content": "    TimeoutTypes,"
          },
          {
            "line_number": 47,
            "content": ")"
          },
          {
            "line_number": 48,
            "content": "from ._urls import URL, QueryParams"
          },
          {
            "line_number": 49,
            "content": "from ._utils import URLPattern, get_environment_proxies"
          },
          {
            "line_number": 50,
            "content": ""
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "httpx/_client.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "symbol:httpx/_client.py:BaseClient._redirect_headers:546",
      "confidence_trigger": 0.57,
      "output_size_tokens": 757,
      "result": {
        "status": "ok",
        "file_path": "httpx/_client.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 2019,
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
            "content": "import datetime"
          },
          {
            "line_number": 4,
            "content": "import enum"
          },
          {
            "line_number": 5,
            "content": "import logging"
          },
          {
            "line_number": 6,
            "content": "import time"
          },
          {
            "line_number": 7,
            "content": "import typing"
          },
          {
            "line_number": 8,
            "content": "import warnings"
          },
          {
            "line_number": 9,
            "content": "from contextlib import asynccontextmanager, contextmanager"
          },
          {
            "line_number": 10,
            "content": "from types import TracebackType"
          },
          {
            "line_number": 11,
            "content": ""
          },
          {
            "line_number": 12,
            "content": "from .__version__ import __version__"
          },
          {
            "line_number": 13,
            "content": "from ._auth import Auth, BasicAuth, FunctionAuth"
          },
          {
            "line_number": 14,
            "content": "from ._config import ("
          },
          {
            "line_number": 15,
            "content": "    DEFAULT_LIMITS,"
          },
          {
            "line_number": 16,
            "content": "    DEFAULT_MAX_REDIRECTS,"
          },
          {
            "line_number": 17,
            "content": "    DEFAULT_TIMEOUT_CONFIG,"
          },
          {
            "line_number": 18,
            "content": "    Limits,"
          },
          {
            "line_number": 19,
            "content": "    Proxy,"
          },
          {
            "line_number": 20,
            "content": "    Timeout,"
          },
          {
            "line_number": 21,
            "content": ")"
          },
          {
            "line_number": 22,
            "content": "from ._decoders import SUPPORTED_DECODERS"
          },
          {
            "line_number": 23,
            "content": "from ._exceptions import ("
          },
          {
            "line_number": 24,
            "content": "    InvalidURL,"
          },
          {
            "line_number": 25,
            "content": "    RemoteProtocolError,"
          },
          {
            "line_number": 26,
            "content": "    TooManyRedirects,"
          },
          {
            "line_number": 27,
            "content": "    request_context,"
          },
          {
            "line_number": 28,
            "content": ")"
          },
          {
            "line_number": 29,
            "content": "from ._models import Cookies, Headers, Request, Response"
          },
          {
            "line_number": 30,
            "content": "from ._status_codes import codes"
          },
          {
            "line_number": 31,
            "content": "from ._transports.base import AsyncBaseTransport, BaseTransport"
          },
          {
            "line_number": 32,
            "content": "from ._transports.default import AsyncHTTPTransport, HTTPTransport"
          },
          {
            "line_number": 33,
            "content": "from ._types import ("
          },
          {
            "line_number": 34,
            "content": "    AsyncByteStream,"
          },
          {
            "line_number": 35,
            "content": "    AuthTypes,"
          },
          {
            "line_number": 36,
            "content": "    CertTypes,"
          },
          {
            "line_number": 37,
            "content": "    CookieTypes,"
          },
          {
            "line_number": 38,
            "content": "    HeaderTypes,"
          },
          {
            "line_number": 39,
            "content": "    ProxyTypes,"
          },
          {
            "line_number": 40,
            "content": "    QueryParamTypes,"
          },
          {
            "line_number": 41,
            "content": "    RequestContent,"
          },
          {
            "line_number": 42,
            "content": "    RequestData,"
          },
          {
            "line_number": 43,
            "content": "    RequestExtensions,"
          },
          {
            "line_number": 44,
            "content": "    RequestFiles,"
          },
          {
            "line_number": 45,
            "content": "    SyncByteStream,"
          },
          {
            "line_number": 46,
            "content": "    TimeoutTypes,"
          },
          {
            "line_number": 47,
            "content": ")"
          },
          {
            "line_number": 48,
            "content": "from ._urls import URL, QueryParams"
          },
          {
            "line_number": 49,
            "content": "from ._utils import URLPattern, get_environment_proxies"
          },
          {
            "line_number": 50,
            "content": ""
          }
        ]
      }
    },
    {
      "tool": "code_slice",
      "args": {
        "file_path": "httpx/_client.py",
        "start_line": 1,
        "end_line": 50
      },
      "node_id": "symbol:httpx/_client.py:BaseClient._redirect_method:494",
      "confidence_trigger": 0.77,
      "output_size_tokens": 757,
      "result": {
        "status": "ok",
        "file_path": "httpx/_client.py",
        "start_line": 1,
        "end_line": 50,
        "total_lines_in_file": 2019,
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
            "content": "import datetime"
          },
          {
            "line_number": 4,
            "content": "import enum"
          },
          {
            "line_number": 5,
            "content": "import logging"
          },
          {
            "line_number": 6,
            "content": "import time"
          },
          {
            "line_number": 7,
            "content": "import typing"
          },
          {
            "line_number": 8,
            "content": "import warnings"
          },
          {
            "line_number": 9,
            "content": "from contextlib import asynccontextmanager, contextmanager"
          },
          {
            "line_number": 10,
            "content": "from types import TracebackType"
          },
          {
            "line_number": 11,
            "content": ""
          },
          {
            "line_number": 12,
            "content": "from .__version__ import __version__"
          },
          {
            "line_number": 13,
            "content": "from ._auth import Auth, BasicAuth, FunctionAuth"
          },
          {
            "line_number": 14,
            "content": "from ._config import ("
          },
          {
            "line_number": 15,
            "content": "    DEFAULT_LIMITS,"
          },
          {
            "line_number": 16,
            "content": "    DEFAULT_MAX_REDIRECTS,"
          },
          {
            "line_number": 17,
            "content": "    DEFAULT_TIMEOUT_CONFIG,"
          },
          {
            "line_number": 18,
            "content": "    Limits,"
          },
          {
            "line_number": 19,
            "content": "    Proxy,"
          },
          {
            "line_number": 20,
            "content": "    Timeout,"
          },
          {
            "line_number": 21,
            "content": ")"
          },
          {
            "line_number": 22,
            "content": "from ._decoders import SUPPORTED_DECODERS"
          },
          {
            "line_number": 23,
            "content": "from ._exceptions import ("
          },
          {
            "line_number": 24,
            "content": "    InvalidURL,"
          },
          {
            "line_number": 25,
            "content": "    RemoteProtocolError,"
          },
          {
            "line_number": 26,
            "content": "    TooManyRedirects,"
          },
          {
            "line_number": 27,
            "content": "    request_context,"
          },
          {
            "line_number": 28,
            "content": ")"
          },
          {
            "line_number": 29,
            "content": "from ._models import Cookies, Headers, Request, Response"
          },
          {
            "line_number": 30,
            "content": "from ._status_codes import codes"
          },
          {
            "line_number": 31,
            "content": "from ._transports.base import AsyncBaseTransport, BaseTransport"
          },
          {
            "line_number": 32,
            "content": "from ._transports.default import AsyncHTTPTransport, HTTPTransport"
          },
          {
            "line_number": 33,
            "content": "from ._types import ("
          },
          {
            "line_number": 34,
            "content": "    AsyncByteStream,"
          },
          {
            "line_number": 35,
            "content": "    AuthTypes,"
          },
          {
            "line_number": 36,
            "content": "    CertTypes,"
          },
          {
            "line_number": 37,
            "content": "    CookieTypes,"
          },
          {
            "line_number": 38,
            "content": "    HeaderTypes,"
          },
          {
            "line_number": 39,
            "content": "    ProxyTypes,"
          },
          {
            "line_number": 40,
            "content": "    QueryParamTypes,"
          },
          {
            "line_number": 41,
            "content": "    RequestContent,"
          },
          {
            "line_number": 42,
            "content": "    RequestData,"
          },
          {
            "line_number": 43,
            "content": "    RequestExtensions,"
          },
          {
            "line_number": 44,
            "content": "    RequestFiles,"
          },
          {
            "line_number": 45,
            "content": "    SyncByteStream,"
          },
          {
            "line_number": 46,
            "content": "    TimeoutTypes,"
          },
          {
            "line_number": 47,
            "content": ")"
          },
          {
            "line_number": 48,
            "content": "from ._urls import URL, QueryParams"
          },
          {
            "line_number": 49,
            "content": "from ._utils import URLPattern, get_environment_proxies"
          },
          {
            "line_number": 50,
            "content": ""
          }
        ]
      }
    }
  ],
  "trace_file": "experiments\\reports\\external-drilldown\\batch-20260405-subagents-final\\httpx-tf2-001\\traces\\trace-20260405T134652.jsonl"
}
