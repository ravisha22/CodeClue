from __future__ import annotations

import ast
import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .extract_go import extract_go_nodes_edges
from .extract_typescript import extract_typescript_nodes_edges
from .models import CanonicalClueGraph, Edge, Node, SourceAnchor


@dataclass
class SymbolRecord:
    symbol_id: str
    symbol_name: str
    symbol_type: str
    line_start: int
    line_end: int
    col_start: int
    col_end: int
    ast_path: str


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _line_col_to_offset(text: str, line: int, col: int) -> int:
    if line < 1:
        return 0
    lines = text.splitlines(keepends=True)
    if line > len(lines):
        return len(text.encode("utf-8"))
    prefix = "".join(lines[: line - 1])
    target = lines[line - 1]
    return len((prefix + target[:col]).encode("utf-8"))


def _iter_python_files(repo_root: Path) -> Iterable[Path]:
    for path in repo_root.rglob("*.py"):
        if any(part.startswith(".") for part in path.parts):
            continue
        yield path


class SymbolCollector(ast.NodeVisitor):
    def __init__(self, rel_path: str) -> None:
        self.rel_path = rel_path
        self.scope_stack: list[str] = []
        self.symbols: list[SymbolRecord] = []

    def _record(self, node: ast.AST, symbol_type: str, symbol_name: str) -> None:
        qname = ".".join(self.scope_stack + [symbol_name])
        symbol_id = f"symbol:{self.rel_path}:{qname}:{node.lineno}"
        self.symbols.append(
            SymbolRecord(
                symbol_id=symbol_id,
                symbol_name=symbol_name,
                symbol_type=symbol_type,
                line_start=getattr(node, "lineno", 1),
                line_end=getattr(node, "end_lineno", getattr(node, "lineno", 1)),
                col_start=getattr(node, "col_offset", 0),
                col_end=getattr(node, "end_col_offset", 0),
                ast_path=f"{symbol_type}:{qname}",
            )
        )

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._record(node, "class", node.name)
        self.scope_stack.append(node.name)
        self.generic_visit(node)
        self.scope_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._record(node, "function", node.name)
        self.scope_stack.append(node.name)
        self.generic_visit(node)
        self.scope_stack.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._record(node, "async_function", node.name)
        self.scope_stack.append(node.name)
        self.generic_visit(node)
        self.scope_stack.pop()


def extract_python_nodes_edges(repo_root: Path) -> tuple[list[Node], list[Edge]]:
    nodes: list[Node] = []
    edges: list[Edge] = []

    for file_path in _iter_python_files(repo_root):
        text = file_path.read_text(encoding="utf-8")
        rel_path = file_path.relative_to(repo_root).as_posix()
        module_node_id = f"module:{rel_path}"

        module_anchor = SourceAnchor(
            file_path=rel_path,
            byte_start=0,
            byte_end=len(text.encode("utf-8")),
            ast_path="module",
            content_hash=_hash_text(text),
        )
        nodes.append(
            Node(
                node_id=module_node_id,
                node_type="module",
                source_anchor=module_anchor,
                semantic_contract={
                    "purpose": "Module-level semantic container",
                    "language": "python",
                    "symbol_name": rel_path,
                    "symbol_type": "module",
                    "tier": 1,
                    "calls": [],
                    "called_by": [],
                    "complexity_indicators": {
                        "decorator_depth": 0,
                        "generic_type_param_count": 0,
                    },
                },
                confidence=1.0,
            )
        )

        try:
            tree = ast.parse(text, filename=rel_path)
        except SyntaxError:
            # Skip files that can't be parsed (e.g., intentional syntax error test fixtures)
            continue
        collector = SymbolCollector(rel_path)
        collector.visit(tree)

        name_to_symbol: dict[str, list[str]] = {}
        for symbol in collector.symbols:
            start = _line_col_to_offset(text, symbol.line_start, symbol.col_start)
            end = _line_col_to_offset(text, symbol.line_end, symbol.col_end)
            snippet = text.encode("utf-8")[start:end].decode("utf-8", errors="ignore")
            nodes.append(
                Node(
                    node_id=symbol.symbol_id,
                    node_type=symbol.symbol_type,
                    source_anchor=SourceAnchor(
                        file_path=rel_path,
                        byte_start=start,
                        byte_end=end,
                        ast_path=symbol.ast_path,
                        content_hash=_hash_text(snippet),
                    ),
                    semantic_contract={
                        "purpose": f"{symbol.symbol_type} {symbol.symbol_name}",
                        "language": "python",
                        "symbol_name": symbol.symbol_name,
                        "symbol_type": symbol.symbol_type,
                        "tier": 1,
                        "calls": [],
                        "called_by": [],
                        "complexity_indicators": {
                            "decorator_depth": 0,
                            "generic_type_param_count": 0,
                        },
                    },
                    confidence=0.92,
                )
            )
            edges.append(
                Edge(
                    edge_id=f"contains:{module_node_id}:{symbol.symbol_id}",
                    edge_type="contains",
                    from_node=module_node_id,
                    to_node=symbol.symbol_id,
                    evidence={"rel": "ast_containment"},
                )
            )
            name_to_symbol.setdefault(symbol.symbol_name, []).append(symbol.symbol_id)

        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            caller_candidates = name_to_symbol.get(node.name, [])
            if len(caller_candidates) != 1:
                continue
            caller_id = caller_candidates[0]
            for child in ast.walk(node):
                if not isinstance(child, ast.Call):
                    continue
                callee_name = ""
                if isinstance(child.func, ast.Name):
                    callee_name = child.func.id
                elif isinstance(child.func, ast.Attribute):
                    callee_name = child.func.attr
                if not callee_name:
                    continue
                callee_candidates = name_to_symbol.get(callee_name, [])
                if len(callee_candidates) != 1:
                    continue
                callee_id = callee_candidates[0]
                edges.append(
                    Edge(
                        edge_id=(
                            f"calls:{caller_id}:{callee_id}:"
                            f"{getattr(child, 'lineno', 0)}"
                        ),
                        edge_type="calls",
                        from_node=caller_id,
                        to_node=callee_id,
                        evidence={"rel": "ast_call", "line": getattr(child, "lineno", 0)},
                    )
                )

    return nodes, edges


def extract_graph(
    repo_root: Path,
    commit_id: str = "unknown",
    language: str = "auto",
    generator_model: str = "codeclue-structural-v1",
    generator_model_family: str = "codeclue",
) -> CanonicalClueGraph:
    repo_root = repo_root.resolve()
    nodes: list[Node] = []
    edges: list[Edge] = []

    normalized = language.lower()
    if normalized not in {"auto", "python", "typescript", "go"}:
        raise ValueError(f"Unsupported language selector: {language}")

    selected = [normalized]
    if normalized == "auto":
        selected = ["python", "typescript", "go"]

    for entry in selected:
        if entry == "python":
            py_nodes, py_edges = extract_python_nodes_edges(repo_root)
            nodes.extend(py_nodes)
            edges.extend(py_edges)
        elif entry == "typescript":
            ts_nodes, ts_edges = extract_typescript_nodes_edges(repo_root)
            nodes.extend(ts_nodes)
            edges.extend(ts_edges)
        elif entry == "go":
            go_nodes, go_edges = extract_go_nodes_edges(repo_root)
            nodes.extend(go_nodes)
            edges.extend(go_edges)

    node_map = {node.node_id: node for node in nodes}
    edge_map = {edge.edge_id: edge for edge in edges}
    nodes = sorted(node_map.values(), key=lambda item: item.node_id)
    edges = sorted(edge_map.values(), key=lambda item: item.edge_id)

    # Fix 3: Populate calls/called_by from edge data into semantic contracts
    for edge in edges:
        if edge.edge_type == "calls":
            from_node = node_map.get(edge.from_node)
            to_node = node_map.get(edge.to_node)
            if from_node:
                calls_list = from_node.semantic_contract.get("calls", [])
                call_entry = {"target": edge.to_node, "is_external": False}
                if call_entry not in calls_list:
                    calls_list.append(call_entry)
                from_node.semantic_contract["calls"] = calls_list
            if to_node:
                called_by_list = to_node.semantic_contract.get("called_by", [])
                cb_entry = {"source": edge.from_node}
                if cb_entry not in called_by_list:
                    called_by_list.append(cb_entry)
                to_node.semantic_contract["called_by"] = called_by_list

    root_hash_source = "\n".join(sorted(node.node_id for node in nodes))
    graph = CanonicalClueGraph(
        metadata={
            "schema_version": "codeclue.lcf.v1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "generator": "phase2.extractor.multi_language",
            "generator_model": generator_model,
            "generator_model_family": generator_model_family,
            "commit_id": commit_id,
            "language_selector": normalized,
        },
        repository={
            "name": repo_root.name,
            "default_branch": "unknown",
            "root_hash": _hash_text(root_hash_source),
        },
        nodes=nodes,
        edges=edges,
        operations={
            "operation_families": ["OF1", "OF2", "OF3", "OF4", "OF5"],
            "projection_policies": {
                "default": "task-conditioned subgraph extraction from canonical graph"
            },
        },
        invariants={
            "connectivity_invariant": True,
            "anchor_invariant": True,
            "no_gap_invariant": True,
            "round_trip_invariant": True,
        },
    )
    return graph
