from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


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

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CanonicalClueGraph":
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
        return cls(
            metadata=data.get("metadata", {}),
            repository=data.get("repository", {}),
            nodes=nodes,
            edges=edges,
            operations=data.get("operations", {}),
            invariants=data.get("invariants", {}),
        )
