from __future__ import annotations

import re
from pathlib import Path

from .models import Edge, Node, SourceAnchor


def _hash_text(text: str) -> str:
    import hashlib

    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _line_offsets(text: str) -> list[int]:
    offsets = [0]
    total = 0
    for line in text.splitlines(keepends=True):
        total += len(line.encode("utf-8"))
        offsets.append(total)
    return offsets


def _byte_span(text: str, line: int, col_start: int, col_end: int) -> tuple[int, int]:
    offsets = _line_offsets(text)
    line_index = max(1, min(line, len(offsets) - 1))
    base = offsets[line_index - 1]
    return base + col_start, base + col_end


def _iter_ts_files(repo_root: Path) -> list[Path]:
    patterns = ("*.ts", "*.tsx", "*.js", "*.jsx")
    files: list[Path] = []
    for pattern in patterns:
        for path in repo_root.rglob(pattern):
            if any(part.startswith(".") for part in path.parts):
                continue
            files.append(path)
    return sorted(set(files))


def extract_typescript_nodes_edges(repo_root: Path) -> tuple[list[Node], list[Edge]]:
    nodes: list[Node] = []
    edges: list[Edge] = []

    class_re = re.compile(r"(?:export\s+)?class\s+([A-Za-z_][A-Za-z0-9_]*)")
    func_re = re.compile(
        r"(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\("
    )
    arrow_re = re.compile(
        r"(?:export\s+)?const\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?:async\s*)?\("
    )
    call_re = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*\(")

    for file_path in _iter_ts_files(repo_root):
        text = file_path.read_text(encoding="utf-8")
        rel_path = file_path.relative_to(repo_root).as_posix()
        module_id = f"module:{rel_path}"
        nodes.append(
            Node(
                node_id=module_id,
                node_type="module",
                source_anchor=SourceAnchor(
                    file_path=rel_path,
                    byte_start=0,
                    byte_end=len(text.encode("utf-8")),
                    ast_path="module",
                    content_hash=_hash_text(text),
                ),
                semantic_contract={
                    "purpose": "Module-level semantic container",
                    "language": "typescript",
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

        symbols: dict[str, str] = {}
        for line_no, line in enumerate(text.splitlines(), start=1):
            for matcher, symbol_type in (
                (class_re, "class"),
                (func_re, "function"),
                (arrow_re, "function"),
            ):
                m = matcher.search(line)
                if not m:
                    continue
                name = m.group(1)
                col_start = m.start(1)
                col_end = m.end(1)
                start, end = _byte_span(text, line_no, col_start, col_end)
                node_id = f"symbol:{rel_path}:{name}:{line_no}"
                symbols[name] = node_id
                nodes.append(
                    Node(
                        node_id=node_id,
                        node_type=symbol_type,
                        source_anchor=SourceAnchor(
                            file_path=rel_path,
                            byte_start=max(0, start),
                            byte_end=max(start, end),
                            ast_path=f"{symbol_type}:{name}",
                            content_hash=_hash_text(line.strip()),
                        ),
                        semantic_contract={
                            "purpose": f"{symbol_type} {name}",
                            "language": "typescript",
                            "symbol_name": name,
                            "symbol_type": symbol_type,
                            "tier": 1,
                            "calls": [],
                            "called_by": [],
                            "complexity_indicators": {
                                "decorator_depth": 0,
                                "generic_type_param_count": 0,
                            },
                        },
                        confidence=0.86,
                    )
                )
                edges.append(
                    Edge(
                        edge_id=f"contains:{module_id}:{node_id}",
                        edge_type="contains",
                        from_node=module_id,
                        to_node=node_id,
                        evidence={"rel": "regex_containment", "line": line_no},
                    )
                )

        for line_no, line in enumerate(text.splitlines(), start=1):
            calls = [m.group(1) for m in call_re.finditer(line)]
            if not calls:
                continue
            for callee_name in calls:
                callee_id = symbols.get(callee_name)
                if not callee_id:
                    continue
                edges.append(
                    Edge(
                        edge_id=f"calls:{module_id}:{callee_id}:{line_no}",
                        edge_type="calls",
                        from_node=module_id,
                        to_node=callee_id,
                        evidence={"rel": "regex_call", "line": line_no},
                    )
                )

    return nodes, edges
