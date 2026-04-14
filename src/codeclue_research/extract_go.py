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


def _iter_go_files(repo_root: Path) -> list[Path]:
    files: list[Path] = []
    for path in repo_root.rglob("*.go"):
        if any(part.startswith(".") for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def _extract_go_function_body(lines: list[str], start_idx: int) -> str:
    body_lines: list[str] = []
    brace_depth = 0
    started = False
    for idx in range(start_idx, len(lines)):
        line = lines[idx]
        open_count = line.count("{")
        close_count = line.count("}")
        if open_count:
            started = True
        if started:
            body_lines.append(line)
        brace_depth += open_count - close_count
        if started and brace_depth <= 0:
            break
    return "\n".join(body_lines)


def _extract_go_behavior_patterns(body: str) -> list[str]:
    patterns: list[str] = []
    if not body:
        return patterns

    if re.search(r"(?m)^\s*if\s+err\s*!=\s*nil\s*\{[^{}]*(?:return|panic)", body):
        patterns.append("GUARD(err)")

    if body.count("if ") >= 2 and len(re.findall(r"(?m)^\s*if\b", body)) >= 2 and len(re.findall(r"(?m)^\s*return\b", body)) >= 2:
        patterns.append("PRECEDENCE(if_chain)")

    if re.search(r"(?m)^\s*for\b", body):
        patterns.append("ACCUMULATE(loop)")

    if re.search(r"(?m)^\s*defer\b", body):
        patterns.append("UNWIND(defer)")

    if re.search(r"(?m)^\s*switch\b", body):
        patterns.append("DISPATCH(switch)")

    return list(dict.fromkeys(patterns))[:3]


def extract_go_nodes_edges(repo_root: Path) -> tuple[list[Node], list[Edge]]:
    nodes: list[Node] = []
    edges: list[Edge] = []

    type_re = re.compile(r"type\s+([A-Za-z_][A-Za-z0-9_]*)\s+(?:struct|interface)")
    func_re = re.compile(r"func\s+(?:\((\w+)\s+\*?(\w+)\)\s*)?([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)")
    # Go doc comment: consecutive // lines immediately before a declaration
    comment_re = re.compile(r"^//\s?(.*)")

    for file_path in _iter_go_files(repo_root):
        text = file_path.read_text(encoding="utf-8")
        rel_path = file_path.relative_to(repo_root).as_posix()
        module_id = f"module:{rel_path}"
        lines_list = text.splitlines()

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
                    "language": "go",
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

        # First pass: collect all symbols with doc comments
        symbols: dict[str, str] = {}  # name -> node_id
        func_bodies: dict[str, tuple[int, int]] = {}  # node_id -> (start_line, approx_end_line)

        for line_no_0, line in enumerate(lines_list):
            line_no = line_no_0 + 1

            # Check for type declaration
            m = type_re.search(line)
            if m:
                name = m.group(1)
                node_id = f"symbol:{rel_path}:{name}:{line_no}"
                symbols[name] = node_id
                # Extract doc comment (consecutive // lines above)
                doc = _extract_go_doc_comment(lines_list, line_no_0)
                col_start = m.start(1)
                col_end = m.end(1)
                start, end = _byte_span(text, line_no, col_start, col_end)
                nodes.append(
                    Node(
                        node_id=node_id,
                        node_type="class",  # Go structs/interfaces → class for MRLF
                        source_anchor=SourceAnchor(
                            file_path=rel_path,
                            byte_start=max(0, start),
                            byte_end=max(start, end),
                            ast_path=f"struct:{name}",
                            content_hash=_hash_text(line.strip()),
                        ),
                        semantic_contract={
                            "purpose": doc if doc else f"type {name}",
                            "language": "go",
                            "symbol_name": name,
                            "symbol_type": "class",
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
                continue

            # Check for function declaration
            m = func_re.search(line)
            if m:
                receiver_var = m.group(1)  # e.g., "c" in func (c *Context)
                receiver_type = m.group(2)  # e.g., "Context"
                func_name = m.group(3)
                params = m.group(4).strip()
                name = func_name
                # If method, use Type.Method as symbol name
                if receiver_type:
                    name = f"{receiver_type}.{func_name}"
                node_id = f"symbol:{rel_path}:{name}:{line_no}"
                symbols[name] = node_id
                # Also register short name for call resolution
                if func_name not in symbols:
                    symbols[func_name] = node_id
                doc = _extract_go_doc_comment(lines_list, line_no_0)
                # Build signature
                sig = f"({params})" if params else "()"
                if len(sig) > 60:
                    sig = sig[:57] + "...)"
                body_text = _extract_go_function_body(lines_list, line_no_0)
                behavior_patterns = _extract_go_behavior_patterns(body_text)
                col_start = m.start(3)
                col_end = m.end(3)
                start, end = _byte_span(text, line_no, col_start, col_end)
                nodes.append(
                    Node(
                        node_id=node_id,
                        node_type="function",
                        source_anchor=SourceAnchor(
                            file_path=rel_path,
                            byte_start=max(0, start),
                            byte_end=max(start, end),
                            ast_path=f"function:{name}",
                            content_hash=_hash_text(line.strip()),
                        ),
                        semantic_contract={
                            "purpose": doc if doc else f"function {name}",
                            "language": "go",
                            "symbol_name": name,
                            "symbol_type": "function",
                            "signature": sig,
                            "behavior_patterns": behavior_patterns,
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
                # Track function body for call edge extraction
                func_bodies[node_id] = (line_no, line_no + 50)  # approximate

                # If it's a method, add containment edge from struct
                if receiver_type and receiver_type in symbols:
                    struct_id = symbols[receiver_type]
                    edges.append(
                        Edge(
                            edge_id=f"contains:{struct_id}:{node_id}",
                            edge_type="contains",
                            from_node=struct_id,
                            to_node=node_id,
                            evidence={"rel": "method_of"},
                        )
                    )

        # Second pass: extract call edges + panic detection
        node_by_id = {n.node_id: n for n in nodes}
        current_func_id: str | None = None
        func_panics: dict[str, list[str]] = {}  # func_id -> list of panic messages
        for line_no_0, line in enumerate(lines_list):
            line_no = line_no_0 + 1
            # Track which function we're inside
            m = func_re.search(line)
            if m:
                receiver_type = m.group(2)
                func_name = m.group(3)
                name = f"{receiver_type}.{func_name}" if receiver_type else func_name
                current_func_id = symbols.get(name)
                continue
            if current_func_id and line.strip() == "}":
                current_func_id = None
                continue
            if not current_func_id:
                continue

            # Detect panic calls
            panic_match = re.search(r'panic\s*\(', line)
            if panic_match and current_func_id:
                func_panics.setdefault(current_func_id, []).append("panic")

            # Look for calls to known symbols
            for sym_name, sym_id in symbols.items():
                if sym_id == current_func_id:
                    continue
                if f"{sym_name}(" in line or f".{sym_name}(" in line:
                    edge_id = f"calls:{current_func_id}:{sym_id}:{line_no}"
                    edges.append(
                        Edge(
                            edge_id=edge_id,
                            edge_type="calls",
                            from_node=current_func_id,
                            to_node=sym_id,
                            evidence={"rel": "regex_call", "line": line_no},
                        )
                    )

        # Update nodes with panic information
        for func_id, panics in func_panics.items():
            node = node_by_id.get(func_id)
            if node:
                node.semantic_contract["raises"] = list(dict.fromkeys(panics))[:3]

    return nodes, edges


def _extract_go_doc_comment(lines: list[str], decl_line_idx: int) -> str:
    """Extract Go doc comment: consecutive // lines immediately above a declaration.

    Returns first sentence of the doc comment, capped at 120 chars.
    """
    doc_lines: list[str] = []
    idx = decl_line_idx - 1
    while idx >= 0:
        m = re.match(r"^\s*//\s?(.*)", lines[idx])
        if m:
            doc_lines.insert(0, m.group(1))
            idx -= 1
        else:
            break

    if not doc_lines:
        return ""

    full_doc = " ".join(doc_lines).strip()
    # Take first sentence
    if ". " in full_doc:
        full_doc = full_doc[:full_doc.index(". ") + 1]
    return full_doc[:120]
