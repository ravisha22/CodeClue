from __future__ import annotations

import hashlib
import json
from typing import Any

import yaml

from codeclue_research.models import CanonicalClueGraph


def _canonicalize(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _canonicalize(value[key]) for key in sorted(value.keys())}
    if isinstance(value, list):
        return [_canonicalize(item) for item in value]
    return value


def _semantic_hash(value: Any) -> str:
    normalized = _canonicalize(value)
    blob = json.dumps(normalized, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def run_roundtrip(graph: CanonicalClueGraph) -> dict[str, Any]:
    original = graph.to_dict()

    json_blob = json.dumps(original, sort_keys=True)
    from_json = json.loads(json_blob)

    yaml_blob = yaml.safe_dump(original, sort_keys=False)
    from_yaml = yaml.safe_load(yaml_blob)

    original_hash = _semantic_hash(original)
    json_hash = _semantic_hash(from_json)
    yaml_hash = _semantic_hash(from_yaml)

    original_nodes = {node["node_id"] for node in original.get("nodes", [])}
    json_nodes = {node["node_id"] for node in from_json.get("nodes", [])}
    yaml_nodes = {node["node_id"] for node in from_yaml.get("nodes", [])}

    original_edges = {
        (edge["from_node"], edge["to_node"], edge["edge_type"])
        for edge in original.get("edges", [])
    }
    json_edges = {
        (edge["from_node"], edge["to_node"], edge["edge_type"])
        for edge in from_json.get("edges", [])
    }
    yaml_edges = {
        (edge["from_node"], edge["to_node"], edge["edge_type"])
        for edge in from_yaml.get("edges", [])
    }

    passed = (
        original_hash == json_hash == yaml_hash
        and original_nodes == json_nodes == yaml_nodes
        and original_edges == json_edges == yaml_edges
    )

    return {
        "passed": passed,
        "hashes": {
            "original": original_hash,
            "json": json_hash,
            "yaml": yaml_hash,
        },
        "node_counts": {
            "original": len(original_nodes),
            "json": len(json_nodes),
            "yaml": len(yaml_nodes),
        },
        "edge_counts": {
            "original": len(original_edges),
            "json": len(json_edges),
            "yaml": len(yaml_edges),
        },
        "lossless_requirements": {
            "semantic_hash_equal": original_hash == json_hash == yaml_hash,
            "node_set_preserved": original_nodes == json_nodes == yaml_nodes,
            "edge_set_preserved": original_edges == json_edges == yaml_edges,
        },
    }
