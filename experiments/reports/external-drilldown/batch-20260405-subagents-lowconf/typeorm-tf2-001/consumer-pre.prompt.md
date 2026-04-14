You are running the BEFORE pass of a CodeClue drill-down evaluation.

Rules:
- Use ONLY the clue projection below.
- Do NOT use raw source code.
- Do NOT call MCP tools.
- If the clue is insufficient, say exactly what is missing.

Task ID: typeorm-tf2-001
Family: TF2
Operation Family: OF2

Question:
If Entity metadata resolution is changed from synchronous to lazy/async loading, what subsystems would be impacted?

Return your answer in this format:

1. Answer
2. Clue sufficient: yes|no
3. Missing information:
   - ...
4. Confidence in your answer: low|medium|high

## Confidence Block
{
  "code_density_risk": 0.0,
  "confidence_overall": 0.0,
  "lookup_decision_hint": "expanded_lookup",
  "operation_family": "OF2",
  "p_context_miss": 0.0,
  "p_dependency_miss": 1.0,
  "p_hallucination": 0.0,
  "per_edge_confidence": [],
  "per_node_confidence": [
    {
      "confidence": 0.85,
      "density_indicators": {
        "cross_file_span_ratio": 0.0,
        "decorator_depth": 0,
        "density_flag": false,
        "fan_out": 5,
        "fan_out_z_score": 0.78,
        "generic_type_param_count": 0,
        "uses_dynamic_dispatch": false,
        "uses_generics": false,
        "uses_metaprogramming": false,
        "uses_reflection": false
      },
      "node_id": "module:src/metadata/EntityMetadata.ts",
      "suggested_actions": [
        {
          "args": {
            "depth": 2,
            "node_id": "module:src/metadata/EntityMetadata.ts"
          },
          "rationale": "5 outgoing edge(s) point to nodes outside this projection; dependency closure is incomplete",
          "tool": "resolve_dependency"
        },
        {
          "args": {
            "end_line": 50,
            "file_path": "src/metadata/EntityMetadata.ts",
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
  "graph_edge_count": 4075,
  "graph_node_count": 6461,
  "initial_seed_count": 1,
  "projected_edge_count": 0,
  "projected_node_count": 1,
  "seed_count": 2
}

## Projected Nodes
[
  {
    "confidence": 1.0,
    "node_id": "module:src/metadata/EntityMetadata.ts",
    "node_type": "module",
    "semantic_contract": {
      "called_by": [],
      "calls": [],
      "complexity_indicators": {
        "decorator_depth": 0,
        "generic_type_param_count": 0
      },
      "language": "typescript",
      "purpose": "Module-level semantic container",
      "symbol_name": "src/metadata/EntityMetadata.ts",
      "symbol_type": "module",
      "tier": 1
    },
    "source_anchor": {
      "ast_path": "module",
      "byte_end": 37529,
      "byte_start": 0,
      "content_hash": "613f3578ed44381c4c0ffbee8281253142dbeb215da9e5e1c1352a7df67df53a",
      "file_path": "src/metadata/EntityMetadata.ts"
    }
  }
]

## Projected Edges
[]
