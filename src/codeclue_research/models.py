from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


DEFAULT_COMPLEXITY_INDICATORS = {
    "decorator_depth": 0,
    "generic_type_param_count": 0,
}


def _infer_language(file_path: str) -> str:
    lowered = file_path.lower()
    if lowered.endswith(".py"):
        return "python"
    if lowered.endswith(".ts") or lowered.endswith(".tsx"):
        return "typescript"
    if lowered.endswith(".go"):
        return "go"
    if lowered.endswith(".js") or lowered.endswith(".jsx"):
        return "javascript"
    return "unknown"


def _default_symbol_name(node_type: str, file_path: str, node_id: str) -> str:
    if node_type == "module":
        return file_path
    return node_id


def _default_purpose(node_type: str, symbol_name: str) -> str:
    if node_type == "module":
        return "Module-level semantic container"
    return f"{node_type} {symbol_name}"


def _normalize_semantic_contract(node: "Node") -> None:
    contract = dict(node.semantic_contract or {})
    symbol_name = str(
        contract.get("symbol_name")
        or _default_symbol_name(node.node_type, node.source_anchor.file_path, node.node_id)
    )

    contract["symbol_name"] = symbol_name
    contract.setdefault("symbol_type", node.node_type)
    contract.setdefault("purpose", _default_purpose(node.node_type, symbol_name))
    contract.setdefault("language", _infer_language(node.source_anchor.file_path))
    contract.setdefault("tier", 1)

    complexity = contract.get("complexity_indicators")
    if not isinstance(complexity, dict) or not complexity:
        contract["complexity_indicators"] = dict(DEFAULT_COMPLEXITY_INDICATORS)
    else:
        normalized_complexity = dict(DEFAULT_COMPLEXITY_INDICATORS)
        normalized_complexity.update(complexity)
        contract["complexity_indicators"] = normalized_complexity

    calls = contract.get("calls")
    called_by = contract.get("called_by")
    contract["calls"] = list(calls) if isinstance(calls, list) else []
    contract["called_by"] = list(called_by) if isinstance(called_by, list) else []
    node.semantic_contract = contract


def _hydrate_derived_contracts(nodes: list["Node"], edges: list["Edge"]) -> None:
    node_map = {node.node_id: node for node in nodes}
    for node in nodes:
        _normalize_semantic_contract(node)

    for edge in edges:
        if edge.edge_type != "calls":
            continue
        from_node = node_map.get(edge.from_node)
        to_node = node_map.get(edge.to_node)
        if from_node:
            entry = {"target": edge.to_node, "is_external": False}
            calls_list = from_node.semantic_contract["calls"]
            if entry not in calls_list:
                calls_list.append(entry)
        if to_node:
            entry = {"source": edge.from_node}
            called_by_list = to_node.semantic_contract["called_by"]
            if entry not in called_by_list:
                called_by_list.append(entry)


def _compact_semantic_contract(node: "Node") -> dict[str, Any]:
    contract = dict(node.semantic_contract or {})
    symbol_name = str(
        contract.get("symbol_name")
        or _default_symbol_name(node.node_type, node.source_anchor.file_path, node.node_id)
    )
    payload: dict[str, Any] = {"n": symbol_name}

    tier = int(contract.get("tier", 1))
    if tier != 1:
        payload["r"] = tier

    extras: dict[str, Any] = {}
    for key, value in contract.items():
        if key in {
            "calls",
            "called_by",
            "purpose",
            "language",
            "symbol_name",
            "symbol_type",
        }:
            continue
        if key == "tier" and tier == 1:
            continue
        if key == "complexity_indicators" and value == DEFAULT_COMPLEXITY_INDICATORS:
            continue
        if value in (None, [], {}):
            continue
        extras[key] = value

    if extras:
        payload["x"] = extras

    return payload


def _expand_semantic_contract(
    node_type: str,
    file_path: str,
    node_id: str,
    compact_contract: dict[str, Any],
) -> dict[str, Any]:
    symbol_name = str(
        compact_contract.get("n")
        or _default_symbol_name(node_type, file_path, node_id)
    )
    tier = int(compact_contract.get("r", 1))
    extras = compact_contract.get("x", {})
    contract = {
        "purpose": _default_purpose(node_type, symbol_name),
        "language": _infer_language(file_path),
        "symbol_name": symbol_name,
        "symbol_type": node_type,
        "tier": tier,
        "complexity_indicators": dict(DEFAULT_COMPLEXITY_INDICATORS),
        "calls": [],
        "called_by": [],
    }
    if isinstance(extras, dict):
        contract.update(extras)
        complexity = contract.get("complexity_indicators")
        if isinstance(complexity, dict):
            normalized_complexity = dict(DEFAULT_COMPLEXITY_INDICATORS)
            normalized_complexity.update(complexity)
            contract["complexity_indicators"] = normalized_complexity
    return contract


def _reconstruct_edge_id(
    edge_type: str,
    from_node: str,
    to_node: str,
    evidence: dict[str, Any],
) -> str | None:
    if edge_type == "contains":
        return f"contains:{from_node}:{to_node}"
    if edge_type == "calls":
        line = evidence.get("line")
        if line is None:
            return None
        return f"calls:{from_node}:{to_node}:{line}"
    return None


@dataclass
class SourceAnchor:
    file_path: str
    byte_start: int
    byte_end: int
    ast_path: str
    content_hash: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "file_path": self.file_path,
            "byte_start": self.byte_start,
            "byte_end": self.byte_end,
            "ast_path": self.ast_path,
            "content_hash": self.content_hash,
        }

    def to_storage_dict(self, path_index_by_path: dict[str, int]) -> dict[str, Any]:
        return {
            "p": path_index_by_path[self.file_path],
            "s": self.byte_start,
            "e": self.byte_end,
            "a": self.ast_path,
            "h": self.content_hash[:16],
        }


@dataclass
class Node:
    node_id: str
    node_type: str
    source_anchor: SourceAnchor
    semantic_contract: dict[str, Any]
    confidence: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "source_anchor": self.source_anchor.to_dict(),
            "semantic_contract": self.semantic_contract,
            "confidence": self.confidence,
        }

    def to_storage_dict(self, path_index_by_path: dict[str, int]) -> dict[str, Any]:
        return {
            "i": self.node_id,
            "t": self.node_type,
            "a": self.source_anchor.to_storage_dict(path_index_by_path),
            "sc": _compact_semantic_contract(self),
            "c": self.confidence,
        }


@dataclass
class Edge:
    edge_id: str
    edge_type: str
    from_node: str
    to_node: str
    evidence: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "edge_id": self.edge_id,
            "edge_type": self.edge_type,
            "from_node": self.from_node,
            "to_node": self.to_node,
            "evidence": self.evidence,
        }

    def to_storage_dict(self, node_index_by_id: dict[str, int]) -> dict[str, Any]:
        payload = {
            "t": self.edge_type,
            "f": node_index_by_id[self.from_node],
            "o": node_index_by_id[self.to_node],
        }
        if self.evidence:
            payload["v"] = self.evidence

        reconstructed_id = _reconstruct_edge_id(
            self.edge_type,
            self.from_node,
            self.to_node,
            self.evidence,
        )
        if reconstructed_id != self.edge_id:
            payload["i"] = self.edge_id
        return payload


@dataclass
class CanonicalClueGraph:
    metadata: dict[str, Any]
    repository: dict[str, Any]
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)
    operations: dict[str, Any] = field(default_factory=dict)
    invariants: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "metadata": self.metadata,
            "repository": self.repository,
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
            "operations": self.operations,
            "invariants": self.invariants,
        }

    def to_storage_dict(self) -> dict[str, Any]:
        path_table = sorted({node.source_anchor.file_path for node in self.nodes})
        path_index_by_path = {path: index for index, path in enumerate(path_table)}
        node_index_by_id = {
            node.node_id: index for index, node in enumerate(self.nodes)
        }
        metadata = dict(self.metadata)
        metadata["storage_format"] = "compact-v1"

        return {
            "metadata": metadata,
            "repository": self.repository,
            "path_table": path_table,
            "nodes": [
                node.to_storage_dict(path_index_by_path) for node in self.nodes
            ],
            "edges": [
                edge.to_storage_dict(node_index_by_id) for edge in self.edges
            ],
            "operations": self.operations,
            "invariants": self.invariants,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CanonicalClueGraph":
        if data.get("metadata", {}).get("storage_format") == "compact-v1":
            path_table = data.get("path_table", [])
            nodes: list[Node] = []
            for item in data.get("nodes", []):
                anchor_payload = item["a"]
                file_path = path_table[anchor_payload["p"]]
                source_anchor = SourceAnchor(
                    file_path=file_path,
                    byte_start=anchor_payload["s"],
                    byte_end=anchor_payload["e"],
                    ast_path=anchor_payload["a"],
                    content_hash=anchor_payload["h"],
                )
                nodes.append(
                    Node(
                        node_id=item["i"],
                        node_type=item["t"],
                        source_anchor=source_anchor,
                        semantic_contract=_expand_semantic_contract(
                            item["t"],
                            file_path,
                            item["i"],
                            item.get("sc", {}),
                        ),
                        confidence=float(item["c"]),
                    )
                )

            node_ids = [node.node_id for node in nodes]
            edges: list[Edge] = []
            for item in data.get("edges", []):
                from_node = node_ids[item["f"]]
                to_node = node_ids[item["o"]]
                evidence = item.get("v", {})
                edge_id = item.get("i") or _reconstruct_edge_id(
                    item["t"], from_node, to_node, evidence
                )
                if edge_id is None:
                    edge_id = f"{item['t']}:{from_node}:{to_node}"
                edges.append(
                    Edge(
                        edge_id=edge_id,
                        edge_type=item["t"],
                        from_node=from_node,
                        to_node=to_node,
                        evidence=evidence,
                    )
                )

            _hydrate_derived_contracts(nodes, edges)
            return cls(
                metadata=data.get("metadata", {}),
                repository=data.get("repository", {}),
                nodes=nodes,
                edges=edges,
                operations=data.get("operations", {}),
                invariants=data.get("invariants", {}),
            )

        nodes = [
            Node(
                node_id=item["node_id"],
                node_type=item["node_type"],
                source_anchor=SourceAnchor(**item["source_anchor"]),
                semantic_contract=item["semantic_contract"],
                confidence=float(item["confidence"]),
            )
            for item in data.get("nodes", [])
        ]
        edges = [
            Edge(
                edge_id=item["edge_id"],
                edge_type=item["edge_type"],
                from_node=item["from_node"],
                to_node=item["to_node"],
                evidence=item["evidence"],
            )
            for item in data.get("edges", [])
        ]
        _hydrate_derived_contracts(nodes, edges)
        return cls(
            metadata=data.get("metadata", {}),
            repository=data.get("repository", {}),
            nodes=nodes,
            edges=edges,
            operations=data.get("operations", {}),
            invariants=data.get("invariants", {}),
        )
