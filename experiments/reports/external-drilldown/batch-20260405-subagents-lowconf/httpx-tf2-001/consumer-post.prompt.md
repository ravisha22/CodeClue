You are running the AFTER pass of a CodeClue drill-down evaluation.

Rules:
- Start from the same clue projection below.
- You MAY use the configured CodeClue MCP tools if needed.
- Use tool calls only where the clue is insufficient.
- After any tool usage, produce a revised answer.
- Be explicit about what changed because of the tools.

Task ID: httpx-tf2-001
Family: TF2
Operation Family: OF2

Question:
If I change the Timeout class in _config.py to make all timeouts optional (default None), what components would break?

Return your answer in this format:

1. Revised answer
2. Tools used:
   - tool name + why you used it
3. What changed after drill-down:
   - ...
4. Remaining uncertainty:
   - ...
5. Final confidence: low|medium|high

## Confidence Block
{
  "code_density_risk": 0.333333,
  "confidence_overall": 0.081301,
  "lookup_decision_hint": "expanded_lookup",
  "operation_family": "OF2",
  "p_context_miss": 0.0,
  "p_dependency_miss": 0.878049,
  "p_hallucination": 0.0,
  "per_edge_confidence": [
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:httpx/_client.py:AsyncClient.__aenter__:1990:symbol:httpx/_client.py:AsyncClient.__aenter__:1990:2002",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:httpx/_client.py:AsyncClient.__aenter__:1990:symbol:httpx/_client.py:AsyncClient.__aenter__:1990:2005",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:httpx/_client.py:AsyncClient.__aexit__:2008:symbol:httpx/_client.py:AsyncClient.__aexit__:2008:2016",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:httpx/_client.py:AsyncClient.__aexit__:2008:symbol:httpx/_client.py:AsyncClient.__aexit__:2008:2019",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_redirect_request:475:symbol:httpx/_client.py:BaseClient._redirect_headers:546:482",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_redirect_request:475:symbol:httpx/_client.py:BaseClient._redirect_method:494:480",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_redirect_request:475:symbol:httpx/_client.py:BaseClient._redirect_stream:573:483",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_redirect_request:475:symbol:httpx/_client.py:BaseClient._redirect_url:517:481",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_request_auth:457:symbol:httpx/_client.py:BaseClient._build_auth:445:463",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:httpx/_client.py:BaseClient._redirect_headers:546:symbol:httpx/_client.py:_is_https_redirect:62:553",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:httpx/_client.py:BaseClient._redirect_headers:546:symbol:httpx/_client.py:_same_origin:83:552",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:httpx/_client.py:BaseClient.build_request:340:symbol:httpx/_client.py:BaseClient._merge_cookies:413:368",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:httpx/_client.py:BaseClient.build_request:340:symbol:httpx/_client.py:BaseClient._merge_headers:424:367",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:httpx/_client.py:BaseClient.build_request:340:symbol:httpx/_client.py:BaseClient._merge_queryparams:433:369",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:httpx/_client.py:BaseClient.build_request:340:symbol:httpx/_client.py:BaseClient._merge_url:391:366",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:httpx/_client.py:Client.__enter__:1275:symbol:httpx/_client.py:Client.__enter__:1275:1287",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:httpx/_client.py:Client.__enter__:1275:symbol:httpx/_client.py:Client.__enter__:1275:1290",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:httpx/_client.py:Client.__exit__:1293:symbol:httpx/_client.py:Client.__exit__:1293:1301",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:httpx/_client.py:Client.__exit__:1293:symbol:httpx/_client.py:Client.__exit__:1293:1304",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:httpx/_client.py:_is_https_redirect:62:symbol:httpx/_client.py:_port_or_default:77:71",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:httpx/_client.py:_is_https_redirect:62:symbol:httpx/_client.py:_port_or_default:77:73",
      "suggested_actions": []
    },
    {
      "confidence": 1.0,
      "edge_id": "calls:symbol:httpx/_client.py:_same_origin:83:symbol:httpx/_client.py:_port_or_default:77:90",
      "suggested_actions": []
    }
  ],
  "per_node_confidence": [
    {
      "confidence": 0.65,
      "density_indicators": {
        "cross_file_span_ratio": 0.033,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 88,
        "fan_out_z_score": 3.015,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:httpx/_client.py",
      "suggested_actions": [
        {
          "args": {
            "depth": 2,
            "node_id": "module:httpx/_client.py"
          },
          "rationale": "69 outgoing edge(s) point to nodes outside this projection; dependency closure is incomplete",
          "tool": "resolve_dependency"
        },
        {
          "args": {
            "end_line": 50,
            "file_path": "httpx/_client.py",
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
        "cross_file_span_ratio": 0.033,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 15,
        "fan_out_z_score": -0.255,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:httpx/_config.py",
      "suggested_actions": [
        {
          "args": {
            "depth": 2,
            "node_id": "module:httpx/_config.py"
          },
          "rationale": "15 outgoing edge(s) point to nodes outside this projection; dependency closure is incomplete",
          "tool": "resolve_dependency"
        },
        {
          "args": {
            "end_line": 50,
            "file_path": "httpx/_config.py",
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
        "cross_file_span_ratio": 0.033,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 2,
        "fan_out_z_score": 1.843,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:httpx/_client.py:AsyncClient.__aenter__:1990",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "httpx/_client.py",
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
        "cross_file_span_ratio": 0.033,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 2,
        "fan_out_z_score": 1.843,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:httpx/_client.py:AsyncClient.__aexit__:2008",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "httpx/_client.py",
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
        "cross_file_span_ratio": 0.033,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.344,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:httpx/_client.py:BaseClient._build_auth:445",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "httpx/_client.py",
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
        "cross_file_span_ratio": 0.033,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 4,
        "fan_out_z_score": 5.145,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "httpx/_client.py",
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
        "cross_file_span_ratio": 0.033,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 1.028,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:httpx/_client.py:BaseClient._build_request_auth:457",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "httpx/_client.py",
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
        "cross_file_span_ratio": 0.033,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.344,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:httpx/_client.py:BaseClient._merge_cookies:413",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "httpx/_client.py",
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
        "cross_file_span_ratio": 0.033,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.344,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:httpx/_client.py:BaseClient._merge_headers:424",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "httpx/_client.py",
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
        "cross_file_span_ratio": 0.033,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.344,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:httpx/_client.py:BaseClient._merge_queryparams:433",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "httpx/_client.py",
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
        "cross_file_span_ratio": 0.033,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.344,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:httpx/_client.py:BaseClient._merge_url:391",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "httpx/_client.py",
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
        "cross_file_span_ratio": 0.033,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 2,
        "fan_out_z_score": 2.401,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:httpx/_client.py:BaseClient._redirect_headers:546",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "httpx/_client.py",
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
        "cross_file_span_ratio": 0.033,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.344,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:httpx/_client.py:BaseClient._redirect_method:494",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "httpx/_client.py",
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
        "cross_file_span_ratio": 0.033,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.344,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:httpx/_client.py:BaseClient._redirect_stream:573",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "httpx/_client.py",
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
        "cross_file_span_ratio": 0.033,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.344,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:httpx/_client.py:BaseClient._redirect_url:517",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "httpx/_client.py",
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
        "cross_file_span_ratio": 0.033,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 4,
        "fan_out_z_score": 5.145,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:httpx/_client.py:BaseClient.build_request:340",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "httpx/_client.py",
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
        "cross_file_span_ratio": 0.033,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 2,
        "fan_out_z_score": 2.401,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:httpx/_client.py:Client.__enter__:1275",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "httpx/_client.py",
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
        "cross_file_span_ratio": 0.033,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 2,
        "fan_out_z_score": 2.401,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:httpx/_client.py:Client.__exit__:1293",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "httpx/_client.py",
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
        "cross_file_span_ratio": 0.033,
        "decorator_depth": 0,
        "density_flag": true,
        "fan_out": 2,
        "fan_out_z_score": 2.401,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:httpx/_client.py:_is_https_redirect:62",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "httpx/_client.py",
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
        "cross_file_span_ratio": 0.033,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 0,
        "fan_out_z_score": -0.344,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:httpx/_client.py:_port_or_default:77",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "httpx/_client.py",
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
        "cross_file_span_ratio": 0.033,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 1,
        "fan_out_z_score": 1.028,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "symbol:httpx/_client.py:_same_origin:83",
      "suggested_actions": [
        {
          "args": {
            "end_line": 50,
            "file_path": "httpx/_client.py",
            "start_line": 1
          },
          "rationale": "Low confidence on this node; source verification recommended",
          "tool": "code_slice"
        }
      ],
      "tier": 1
    }
  ],
  "threshold": 0.9,
  "tool_call_budget": 15
}

## Projection Stats
{
  "graph_edge_count": 1557,
  "graph_node_count": 1301,
  "initial_seed_count": 18,
  "projected_edge_count": 22,
  "projected_node_count": 21,
  "seed_count": 19
}

## Projected Nodes
[
  {
    "confidence": 1.0,
    "node_id": "module:httpx/_client.py",
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
      "symbol_name": "httpx/_client.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 65713,
      "byte_start": 0,
      "content_hash": "ed717b3ac00debb48d089daeb4dd7fbaf47cb5642ebc4a6e76f3a2fc6cfc0f70",
      "file_path": "httpx/_client.py"
    }
  },
  {
    "confidence": 1.0,
    "node_id": "module:httpx/_config.py",
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
      "symbol_name": "httpx/_config.py",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 8547,
      "byte_start": 0,
      "content_hash": "a4fa7653ec2271f70ab05f8a6111352d876dddee84446788a1767c1a3a372d67",
      "file_path": "httpx/_config.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:httpx/_client.py:AsyncClient.__aenter__:1990",
    "node_type": "async_function",
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
    "source_anchor": {
      "ast_path": "async_function:AsyncClient.__aenter__",
      "byte_end": 65246,
      "byte_start": 64633,
      "content_hash": "b8ac29d32f1e6b712ba5edb5bd6151f0cac78bfceb5962ac0a6c1cc9e30ef035",
      "file_path": "httpx/_client.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:httpx/_client.py:AsyncClient.__aexit__:2008",
    "node_type": "async_function",
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
    "source_anchor": {
      "ast_path": "async_function:AsyncClient.__aexit__",
      "byte_end": 65712,
      "byte_start": 65252,
      "content_hash": "df3f6245719ec2c095df970e08d7176e180316c741d43f837bfd3459b111c0f1",
      "file_path": "httpx/_client.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:httpx/_client.py:BaseClient._build_auth:445",
    "node_type": "function",
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
    "source_anchor": {
      "ast_path": "function:BaseClient._build_auth",
      "byte_end": 14376,
      "byte_start": 13950,
      "content_hash": "02a93e6a831147cc4f74236ba77656d7c1740fd1ca20e4bb4d7952ea717d99fa",
      "file_path": "httpx/_client.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475",
    "node_type": "function",
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
    "source_anchor": {
      "ast_path": "function:BaseClient._build_redirect_request",
      "byte_end": 15613,
      "byte_start": 14905,
      "content_hash": "2f18ca3d8f28ed472f5be8cdb9b71b82d8bd52d2e79bcdc1078d1a548f20cb3b",
      "file_path": "httpx/_client.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:httpx/_client.py:BaseClient._build_request_auth:457",
    "node_type": "function",
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
    "source_anchor": {
      "ast_path": "function:BaseClient._build_request_auth",
      "byte_end": 14899,
      "byte_start": 14382,
      "content_hash": "a36fdfdb8a23565858a9378f2e703770c1a0da5fdd3ad0e7d3f3d33aa7ebdfbb",
      "file_path": "httpx/_client.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:httpx/_client.py:BaseClient._merge_cookies:413",
    "node_type": "function",
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
    "source_anchor": {
      "ast_path": "function:BaseClient._merge_cookies",
      "byte_end": 13129,
      "byte_start": 12700,
      "content_hash": "1113038edb11f328c3da9ff0737fe9f780a429460a2376c3f7c9a6e7fecf2065",
      "file_path": "httpx/_client.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:httpx/_client.py:BaseClient._merge_headers:424",
    "node_type": "function",
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
    "source_anchor": {
      "ast_path": "function:BaseClient._merge_headers",
      "byte_end": 13493,
      "byte_start": 13135,
      "content_hash": "25537640006a58dc76c2da64aac5facd7910975066fc55318cb5c5c9dd11c120",
      "file_path": "httpx/_client.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:httpx/_client.py:BaseClient._merge_queryparams:433",
    "node_type": "function",
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
    "source_anchor": {
      "ast_path": "function:BaseClient._merge_queryparams",
      "byte_end": 13944,
      "byte_start": 13499,
      "content_hash": "0d0c4af31563061b1d2fbc115bfcbb7524c3bbb087790b6526a1b50a6eba787f",
      "file_path": "httpx/_client.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:httpx/_client.py:BaseClient._merge_url:391",
    "node_type": "function",
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
    "source_anchor": {
      "ast_path": "function:BaseClient._merge_url",
      "byte_end": 12694,
      "byte_start": 11694,
      "content_hash": "1d1e4f3806a40f76acc927927b4b6bdca831222477e0eab8fdd34167e121f4f2",
      "file_path": "httpx/_client.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:httpx/_client.py:BaseClient._redirect_headers:546",
    "node_type": "function",
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
    "source_anchor": {
      "ast_path": "function:BaseClient._redirect_headers",
      "byte_end": 18720,
      "byte_start": 17588,
      "content_hash": "cf40c6f53f3e49b9f6ebbb8926efe85db5ade78f26439864f896d70bdc6c370c",
      "file_path": "httpx/_client.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:httpx/_client.py:BaseClient._redirect_method:494",
    "node_type": "function",
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
    "source_anchor": {
      "ast_path": "function:BaseClient._redirect_method",
      "byte_end": 16494,
      "byte_start": 15619,
      "content_hash": "e421099e82483a433735e1e0a31c750e54ccf65d1b752dd063979f1c2dc7b5c9",
      "file_path": "httpx/_client.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:httpx/_client.py:BaseClient._redirect_stream:573",
    "node_type": "function",
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
    "source_anchor": {
      "ast_path": "function:BaseClient._redirect_stream",
      "byte_end": 19047,
      "byte_start": 18726,
      "content_hash": "887fda7354d3216c1d4440b3bdb55abad50de782b6ba64b142887efb0abf4698",
      "file_path": "httpx/_client.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:httpx/_client.py:BaseClient._redirect_url:517",
    "node_type": "function",
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
    "source_anchor": {
      "ast_path": "function:BaseClient._redirect_url",
      "byte_end": 17582,
      "byte_start": 16500,
      "content_hash": "c814d4dbfc61c2b4b85c30252d30f77e7e6962b60b5c16c079c4b2e8371af2b2",
      "file_path": "httpx/_client.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:httpx/_client.py:BaseClient.build_request:340",
    "node_type": "function",
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
    "source_anchor": {
      "ast_path": "function:BaseClient.build_request",
      "byte_end": 11688,
      "byte_start": 9995,
      "content_hash": "ecc2854536373aa7c57c14514d27ebd94ebf501e18959262b6d2c44a83b27065",
      "file_path": "httpx/_client.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:httpx/_client.py:Client.__enter__:1275",
    "node_type": "function",
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
    "source_anchor": {
      "ast_path": "function:Client.__enter__",
      "byte_end": 41889,
      "byte_start": 41285,
      "content_hash": "cdf6c01eefdcbefac0f0755ed2749b0b8ecec6f17617580c4adb988c0fafb78b",
      "file_path": "httpx/_client.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:httpx/_client.py:Client.__exit__:1293",
    "node_type": "function",
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
    "source_anchor": {
      "ast_path": "function:Client.__exit__",
      "byte_end": 42346,
      "byte_start": 41895,
      "content_hash": "363d3668eeea67bf86466057131fecaa6cccb2bb20f1d6f3a49ce1e79e136129",
      "file_path": "httpx/_client.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:httpx/_client.py:_is_https_redirect:62",
    "node_type": "function",
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
    "source_anchor": {
      "ast_path": "function:_is_https_redirect",
      "byte_end": 1897,
      "byte_start": 1536,
      "content_hash": "f7fb9a7652de2ee8be1892fda8abdd18c5cafef3f0b7cee910a997b0d2e3108d",
      "file_path": "httpx/_client.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:httpx/_client.py:_port_or_default:77",
    "node_type": "function",
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
    "source_anchor": {
      "ast_path": "function:_port_or_default",
      "byte_end": 2052,
      "byte_start": 1900,
      "content_hash": "d70ff71cb4458c59da46b26ea655df1e7c87c40d139515e3a672f86942b86c83",
      "file_path": "httpx/_client.py"
    }
  },
  {
    "confidence": 0.92,
    "node_id": "symbol:httpx/_client.py:_same_origin:83",
    "node_type": "function",
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
    "source_anchor": {
      "ast_path": "function:_same_origin",
      "byte_end": 2327,
      "byte_start": 2055,
      "content_hash": "aac753c9500e9d229397f05548f971de5a63129de76236da0994c25179fad392",
      "file_path": "httpx/_client.py"
    }
  }
]

## Projected Edges
[
  {
    "edge_id": "calls:symbol:httpx/_client.py:AsyncClient.__aenter__:1990:symbol:httpx/_client.py:AsyncClient.__aenter__:1990:2002",
    "edge_type": "calls",
    "evidence": {
      "line": 2002,
      "rel": "ast_call"
    },
    "from_node": "symbol:httpx/_client.py:AsyncClient.__aenter__:1990",
    "to_node": "symbol:httpx/_client.py:AsyncClient.__aenter__:1990"
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:AsyncClient.__aenter__:1990:symbol:httpx/_client.py:AsyncClient.__aenter__:1990:2005",
    "edge_type": "calls",
    "evidence": {
      "line": 2005,
      "rel": "ast_call"
    },
    "from_node": "symbol:httpx/_client.py:AsyncClient.__aenter__:1990",
    "to_node": "symbol:httpx/_client.py:AsyncClient.__aenter__:1990"
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:AsyncClient.__aexit__:2008:symbol:httpx/_client.py:AsyncClient.__aexit__:2008:2016",
    "edge_type": "calls",
    "evidence": {
      "line": 2016,
      "rel": "ast_call"
    },
    "from_node": "symbol:httpx/_client.py:AsyncClient.__aexit__:2008",
    "to_node": "symbol:httpx/_client.py:AsyncClient.__aexit__:2008"
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:AsyncClient.__aexit__:2008:symbol:httpx/_client.py:AsyncClient.__aexit__:2008:2019",
    "edge_type": "calls",
    "evidence": {
      "line": 2019,
      "rel": "ast_call"
    },
    "from_node": "symbol:httpx/_client.py:AsyncClient.__aexit__:2008",
    "to_node": "symbol:httpx/_client.py:AsyncClient.__aexit__:2008"
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_redirect_request:475:symbol:httpx/_client.py:BaseClient._redirect_headers:546:482",
    "edge_type": "calls",
    "evidence": {
      "line": 482,
      "rel": "ast_call"
    },
    "from_node": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475",
    "to_node": "symbol:httpx/_client.py:BaseClient._redirect_headers:546"
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_redirect_request:475:symbol:httpx/_client.py:BaseClient._redirect_method:494:480",
    "edge_type": "calls",
    "evidence": {
      "line": 480,
      "rel": "ast_call"
    },
    "from_node": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475",
    "to_node": "symbol:httpx/_client.py:BaseClient._redirect_method:494"
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_redirect_request:475:symbol:httpx/_client.py:BaseClient._redirect_stream:573:483",
    "edge_type": "calls",
    "evidence": {
      "line": 483,
      "rel": "ast_call"
    },
    "from_node": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475",
    "to_node": "symbol:httpx/_client.py:BaseClient._redirect_stream:573"
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_redirect_request:475:symbol:httpx/_client.py:BaseClient._redirect_url:517:481",
    "edge_type": "calls",
    "evidence": {
      "line": 481,
      "rel": "ast_call"
    },
    "from_node": "symbol:httpx/_client.py:BaseClient._build_redirect_request:475",
    "to_node": "symbol:httpx/_client.py:BaseClient._redirect_url:517"
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:BaseClient._build_request_auth:457:symbol:httpx/_client.py:BaseClient._build_auth:445:463",
    "edge_type": "calls",
    "evidence": {
      "line": 463,
      "rel": "ast_call"
    },
    "from_node": "symbol:httpx/_client.py:BaseClient._build_request_auth:457",
    "to_node": "symbol:httpx/_client.py:BaseClient._build_auth:445"
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:BaseClient._redirect_headers:546:symbol:httpx/_client.py:_is_https_redirect:62:553",
    "edge_type": "calls",
    "evidence": {
      "line": 553,
      "rel": "ast_call"
    },
    "from_node": "symbol:httpx/_client.py:BaseClient._redirect_headers:546",
    "to_node": "symbol:httpx/_client.py:_is_https_redirect:62"
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:BaseClient._redirect_headers:546:symbol:httpx/_client.py:_same_origin:83:552",
    "edge_type": "calls",
    "evidence": {
      "line": 552,
      "rel": "ast_call"
    },
    "from_node": "symbol:httpx/_client.py:BaseClient._redirect_headers:546",
    "to_node": "symbol:httpx/_client.py:_same_origin:83"
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:BaseClient.build_request:340:symbol:httpx/_client.py:BaseClient._merge_cookies:413:368",
    "edge_type": "calls",
    "evidence": {
      "line": 368,
      "rel": "ast_call"
    },
    "from_node": "symbol:httpx/_client.py:BaseClient.build_request:340",
    "to_node": "symbol:httpx/_client.py:BaseClient._merge_cookies:413"
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:BaseClient.build_request:340:symbol:httpx/_client.py:BaseClient._merge_headers:424:367",
    "edge_type": "calls",
    "evidence": {
      "line": 367,
      "rel": "ast_call"
    },
    "from_node": "symbol:httpx/_client.py:BaseClient.build_request:340",
    "to_node": "symbol:httpx/_client.py:BaseClient._merge_headers:424"
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:BaseClient.build_request:340:symbol:httpx/_client.py:BaseClient._merge_queryparams:433:369",
    "edge_type": "calls",
    "evidence": {
      "line": 369,
      "rel": "ast_call"
    },
    "from_node": "symbol:httpx/_client.py:BaseClient.build_request:340",
    "to_node": "symbol:httpx/_client.py:BaseClient._merge_queryparams:433"
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:BaseClient.build_request:340:symbol:httpx/_client.py:BaseClient._merge_url:391:366",
    "edge_type": "calls",
    "evidence": {
      "line": 366,
      "rel": "ast_call"
    },
    "from_node": "symbol:httpx/_client.py:BaseClient.build_request:340",
    "to_node": "symbol:httpx/_client.py:BaseClient._merge_url:391"
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:Client.__enter__:1275:symbol:httpx/_client.py:Client.__enter__:1275:1287",
    "edge_type": "calls",
    "evidence": {
      "line": 1287,
      "rel": "ast_call"
    },
    "from_node": "symbol:httpx/_client.py:Client.__enter__:1275",
    "to_node": "symbol:httpx/_client.py:Client.__enter__:1275"
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:Client.__enter__:1275:symbol:httpx/_client.py:Client.__enter__:1275:1290",
    "edge_type": "calls",
    "evidence": {
      "line": 1290,
      "rel": "ast_call"
    },
    "from_node": "symbol:httpx/_client.py:Client.__enter__:1275",
    "to_node": "symbol:httpx/_client.py:Client.__enter__:1275"
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:Client.__exit__:1293:symbol:httpx/_client.py:Client.__exit__:1293:1301",
    "edge_type": "calls",
    "evidence": {
      "line": 1301,
      "rel": "ast_call"
    },
    "from_node": "symbol:httpx/_client.py:Client.__exit__:1293",
    "to_node": "symbol:httpx/_client.py:Client.__exit__:1293"
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:Client.__exit__:1293:symbol:httpx/_client.py:Client.__exit__:1293:1304",
    "edge_type": "calls",
    "evidence": {
      "line": 1304,
      "rel": "ast_call"
    },
    "from_node": "symbol:httpx/_client.py:Client.__exit__:1293",
    "to_node": "symbol:httpx/_client.py:Client.__exit__:1293"
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:_is_https_redirect:62:symbol:httpx/_client.py:_port_or_default:77:71",
    "edge_type": "calls",
    "evidence": {
      "line": 71,
      "rel": "ast_call"
    },
    "from_node": "symbol:httpx/_client.py:_is_https_redirect:62",
    "to_node": "symbol:httpx/_client.py:_port_or_default:77"
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:_is_https_redirect:62:symbol:httpx/_client.py:_port_or_default:77:73",
    "edge_type": "calls",
    "evidence": {
      "line": 73,
      "rel": "ast_call"
    },
    "from_node": "symbol:httpx/_client.py:_is_https_redirect:62",
    "to_node": "symbol:httpx/_client.py:_port_or_default:77"
  },
  {
    "edge_id": "calls:symbol:httpx/_client.py:_same_origin:83:symbol:httpx/_client.py:_port_or_default:77:90",
    "edge_type": "calls",
    "evidence": {
      "line": 90,
      "rel": "ast_call"
    },
    "from_node": "symbol:httpx/_client.py:_same_origin:83",
    "to_node": "symbol:httpx/_client.py:_port_or_default:77"
  }
]
