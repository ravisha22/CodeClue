from __future__ import annotations

import re
import time
from pathlib import Path

from .models import Edge, Node, SourceAnchor

GO_BEHAVIOR_PROGRESS_EVERY = 10
GO_BEHAVIOR_FILE_BUDGET_SECONDS = 5.0
GO_BEHAVIOR_FILE_SIZE_LIMIT_BYTES = 64_000
GO_BEHAVIOR_BODY_SIZE_LIMIT_CHARS = 12_000

_GO_CALL_CANDIDATE_RE = re.compile(r"(?:\.|\b)([A-Za-z_][A-Za-z0-9_]*)\s*\(")
_GO_SHORT_RECEIVER_CALL_RE = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]{0,2})\.([A-Za-z_][A-Za-z0-9_]*)\s*\(")
_GO_PANIC_RE = re.compile(r"panic\s*\(")


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
    skip_dirs = {"testdata", "example", "examples", "doc", "docs", "bench", "benchmark"}
    for path in repo_root.rglob("*.go"):
        if any(part.startswith(".") for part in path.parts):
            continue
        if any(part.lower() in skip_dirs for part in path.parts):
            continue
        if path.name.endswith("_test.go"):
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


def _clean_go_expr(expr: str) -> str:
    expr = re.sub(r"//.*", "", expr).strip()
    expr = expr.removeprefix("return").removeprefix("panic")
    expr = expr.strip(" {}();")
    return expr


def _compact_go_text(text: str) -> str:
    return " ".join(text.split())


def _truncate_go_text(text: str, max_len: int) -> str:
    compact = _compact_go_text(text)
    if len(compact) <= max_len:
        return compact
    return compact[: max_len - 3].rstrip() + "..."


def _go_pattern_text(prefix: str, detail: str, *, max_len: int = 80) -> str:
    text = f"{prefix}({detail})"
    if len(text) <= max_len:
        return text
    return f"{prefix}({_truncate_go_text(detail, max_len - len(prefix) - 2)})"


def _go_action_text(expr: str, *, max_len: int = 24) -> str:
    raw = _compact_go_text(expr.strip())
    if not raw:
        return "result"
    return _truncate_go_text(raw, max_len)


def _go_ref_summary(expr: str, *, source: bool = False) -> str:
    cleaned = _clean_go_expr(expr)
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*", cleaned)
    tokens = [token for token in tokens if token not in {"if", "return", "else", "nil", "true", "false"}]
    if not tokens:
        if "{}" in expr or "nil" in expr:
            return "empty" if "{}" in expr else "none"
        return "value"
    token = tokens[0]
    if source:
        if "." in token:
            token = token.split(".", 1)[0]
        return token.replace(".", "_")[:24]
    return token.replace(".", ".")[:28]


def _summarize_go_condition(expr: str) -> str:
    cleaned = _clean_go_expr(expr)
    if cleaned.startswith("!"):
        return f"not_{_go_ref_summary(cleaned[1:])}"
    if "!=" in cleaned and "nil" in cleaned:
        return _go_ref_summary(cleaned.split("!=", 1)[0], source=True)
    if "==" in cleaned and "nil" in cleaned:
        return _go_ref_summary(cleaned.split("==", 1)[0], source=True)
    if any(op in cleaned for op in ("<", ">", "==", "!=", "<=", ">=")):
        left = re.split(r"<=|>=|==|!=|<|>", cleaned, maxsplit=1)[0]
        return _go_ref_summary(left, source=True)
    return _go_ref_summary(cleaned, source=True)


def _summarize_go_action(expr: str, condition: str = "") -> str:
    raw = expr.strip()
    if not raw:
        return "result"
    if raw.startswith("return"):
        value = _clean_go_expr(raw)
        if value in {"", "nil"}:
            return "none"
        if value in {"{}", "[]"}:
            return "empty"
        condition_hints = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", condition))
        value_hints = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", value))
        if condition_hints and condition_hints.intersection(value_hints) and "(" not in value:
            return "pass_through"
        call_match = re.match(r"([A-Za-z_][A-Za-z0-9_\.]*)\s*\(", value)
        if call_match:
            callee = call_match.group(1).split(".")[-1]
            if condition_hints and condition_hints.intersection(value_hints):
                return f"wrap_{callee}"[:24]
            return callee[:24]
        return _go_ref_summary(value)
    if raw.startswith("panic"):
        return "raise_panic"
    return "result"


def _extract_go_return_expr(block: str) -> str:
    match = re.search(r"(?m)^\s*(return\b.*|panic\b.*)$", block)
    return match.group(1).strip() if match else ""


def _strip_go_line_comment(line: str) -> str:
    return line.split("//", 1)[0].rstrip()


def _iter_go_body_lines(body: str) -> list[tuple[int, str, int]]:
    entries: list[tuple[int, str, int]] = []
    depth = 0
    in_body = False
    for idx, raw_line in enumerate(body.splitlines()):
        clean_line = _strip_go_line_comment(raw_line)
        line_depth = depth
        open_count = clean_line.count("{")
        close_count = clean_line.count("}")
        if open_count:
            in_body = True
        if in_body and line_depth >= 1:
            stripped = clean_line.strip()
            if stripped:
                entries.append((idx, stripped, line_depth))
        depth += open_count - close_count
    return entries


def _parse_go_if_condition(line: str) -> str:
    stripped = line.strip()
    for prefix in ("if ", "} else if ", "else if "):
        if stripped.startswith(prefix):
            return stripped[len(prefix):].split("{", 1)[0].strip()
    return ""


def _collect_go_block_lines(lines: list[str], start_idx: int) -> tuple[list[str], int]:
    block_lines: list[str] = []
    depth = 0
    started = False
    end_idx = start_idx
    for idx in range(start_idx, len(lines)):
        clean_line = _strip_go_line_comment(lines[idx])
        open_count = clean_line.count("{")
        close_count = clean_line.count("}")
        if open_count:
            started = True
        if started:
            stripped = clean_line.strip()
            if stripped:
                block_lines.append(stripped)
        depth += open_count - close_count
        end_idx = idx
        if started and depth <= 0:
            break
    return block_lines, end_idx


def _first_go_terminal_action(lines: list[str]) -> str:
    for line in lines:
        stripped = _strip_go_line_comment(line).strip()
        if stripped.startswith("return") or stripped.startswith("panic"):
            return stripped
    return ""


def _find_next_go_terminal_action(lines: list[str], start_idx: int) -> str:
    for idx in range(start_idx, len(lines)):
        stripped = _strip_go_line_comment(lines[idx]).strip()
        if stripped.startswith("return") or stripped.startswith("panic"):
            return stripped
    return ""


def _find_go_accumulate_target(lines: list[str], start_idx: int) -> str:
    block_lines, _ = _collect_go_block_lines(lines, start_idx)
    for line in block_lines[1:]:
        for pattern in (
            r"([A-Za-z_][A-Za-z0-9_\.]*)\s*\+=",
            r"([A-Za-z_][A-Za-z0-9_\.]*)\s*=\s*append\(",
            r"([A-Za-z_][A-Za-z0-9_\.]*)\.(?:append|write|add|store)\(",
        ):
            match = re.search(pattern, line)
            if match:
                return match.group(1).replace(".", "_")[:24]
    return "result"


def _find_go_accumulate_detail(lines: list[str], start_idx: int) -> str:
    block_lines, _ = _collect_go_block_lines(lines, start_idx)
    for line in block_lines[1:]:
        match = re.search(r"([A-Za-z_][A-Za-z0-9_\.]*)\s*\+=\s*([A-Za-z_][A-Za-z0-9_\.]*)", line)
        if match:
            return _truncate_go_text(
                f"{match.group(1).replace('.', '_')} {match.group(2).replace('.', '_')}",
                28,
            )
        match = re.search(r"([A-Za-z_][A-Za-z0-9_\.]*)\s*=\s*append\([^,]+,\s*([A-Za-z_][A-Za-z0-9_\.]*)", line)
        if match:
            return _truncate_go_text(
                f"{match.group(1).replace('.', '_')} {match.group(2).replace('.', '_')}",
                28,
            )
        match = re.search(r"([A-Za-z_][A-Za-z0-9_\.]*)\.(?:append|write|add|store)\(\s*([A-Za-z_][A-Za-z0-9_\.]*)", line)
        if match:
            return _truncate_go_text(
                f"{match.group(1).replace('.', '_')} {match.group(2).replace('.', '_')}",
                28,
            )
    return _find_go_accumulate_target(lines, start_idx)


def _go_loop_label(lines: list[str], start_idx: int) -> str:
    block_lines, _ = _collect_go_block_lines(lines, start_idx)
    for line in block_lines[1:]:
        match = re.search(r"([A-Za-z_][A-Za-z0-9_\.]*)\s*\(", line)
        if match:
            return _truncate_go_text(f"{match.group(1).split('.')[-1]} loop", 24)
    return "loop"


def _go_loop_raise(lines: list[str], start_idx: int) -> str:
    block_lines, _ = _collect_go_block_lines(lines, start_idx)
    for line in block_lines[1:]:
        match = re.search(r"panic\s*\(([^)]*)\)", line)
        if match:
            return _truncate_go_text(match.group(1), 20)
    return ""


def _extract_go_behavior_patterns(body: str) -> list[str]:
    patterns: list[str] = []
    if not body:
        return patterns

    raw_lines = body.splitlines()
    body_lines = _iter_go_body_lines(body)
    if not body_lines:
        return patterns

    top_level_conditions: list[str] = []
    top_level_return_count = 0
    has_else_branch = False
    first_branch: tuple[int, str] | None = None
    delegate_callee = ""
    switch_expr = ""
    loop_idx: int | None = None
    has_defer = False

    for idx, stripped, depth in body_lines:
        if stripped.startswith("return"):
            top_level_return_count += 1
            if not delegate_callee:
                match = re.match(r"return\s+([A-Za-z_][A-Za-z0-9_\.]*)\s*\(", stripped)
                if match:
                    delegate_callee = match.group(1)
        elif stripped.startswith("panic"):
            top_level_return_count += 1

        if depth != 1:
            continue

        cond = _parse_go_if_condition(stripped)
        if cond:
            top_level_conditions.append(cond)
            if first_branch is None and stripped.startswith("if "):
                first_branch = (idx, cond)
        if stripped.startswith("else ") or stripped.startswith("} else"):
            has_else_branch = True
        if not switch_expr and stripped.startswith("switch "):
            switch_expr = stripped[7:].split("{", 1)[0].strip()
        if loop_idx is None and (stripped == "for" or stripped.startswith("for ") or stripped.startswith("for{")):
            loop_idx = idx
        if stripped.startswith("defer"):
            has_defer = True

    if first_branch:
        branch_idx, branch_cond = first_branch
        block_lines, end_idx = _collect_go_block_lines(raw_lines, branch_idx)
        true_action_expr = _first_go_terminal_action(block_lines[1:])
        branch_window = "\n".join(raw_lines[branch_idx: min(len(raw_lines), end_idx + 6)])
        branch_match = re.search(
            r"(?s)if\s+(.+?)\s*\{\s*(return\b.*?|panic\b.*?)\s*\}\s*else\s*\{\s*(return\b.*?|panic\b.*?)\s*\}",
            branch_window,
        )
        false_action_expr = branch_match.group(3).strip() if branch_match else ""
        else_idx = end_idx
        current_line = _strip_go_line_comment(raw_lines[end_idx]).strip() if end_idx < len(raw_lines) else ""
        if "} else" not in current_line and not false_action_expr:
            else_idx = end_idx + 1
            while else_idx < len(raw_lines) and not _strip_go_line_comment(raw_lines[else_idx]).strip():
                else_idx += 1
        if else_idx < len(raw_lines) and not false_action_expr:
            else_line = _strip_go_line_comment(raw_lines[else_idx]).strip()
            if else_line.startswith("else") or else_line.startswith("} else"):
                false_action_expr = _find_next_go_terminal_action(raw_lines, else_idx + 1)
        has_branch_else = bool(false_action_expr)
        if true_action_expr and not has_branch_else:
            guard_condition = _truncate_go_text(branch_cond, 48)
            guard_action = _go_action_text(true_action_expr, max_len=22)
            patterns.append(_go_pattern_text("GUARD", f"{guard_condition} -> {guard_action}"))
        if true_action_expr and has_branch_else:
            cond = _truncate_go_text(branch_match.group(1), 28) if branch_match else _truncate_go_text(branch_cond, 28)
            true_expr = branch_match.group(2).strip() if branch_match else true_action_expr
            true_action = _go_action_text(true_expr, max_len=22)
            false_action = _go_action_text(false_action_expr, max_len=22)
            patterns.append(_go_pattern_text("BRANCH", f"{cond} -> {true_action}, else -> {false_action}"))

    if len(top_level_conditions) >= 2 and top_level_return_count >= 2:
        sources = [_summarize_go_condition(cond) for cond in top_level_conditions[:3]]
        if has_else_branch:
            sources.append("default")
        patterns.append(_go_pattern_text("PRECEDENCE", " -> ".join(dict.fromkeys(sources))))

    if delegate_callee and top_level_return_count == 1:
        patterns.append(f"DELEGATE({delegate_callee} -> result)")

    if loop_idx is not None:
        loop_label = _go_loop_label(raw_lines, loop_idx)
        target = _find_go_accumulate_detail(raw_lines, loop_idx).replace("_", " ")
        raise_name = _go_loop_raise(raw_lines, loop_idx)
        detail = f"{loop_label} -> {target}"
        if raise_name:
            detail += f", raises {raise_name}"
        patterns.append(_go_pattern_text("ACCUMULATE", detail))

    if has_defer:
        patterns.append("UNWIND(defer)")

    if switch_expr:
        patterns.append(f"DISPATCH({_go_ref_summary(switch_expr, source=True)})")

    return list(dict.fromkeys(patterns))[:3]


def extract_go_nodes_edges(repo_root: Path) -> tuple[list[Node], list[Edge]]:
    nodes: list[Node] = []
    edges: list[Edge] = []
    file_scan_records: list[tuple[list[str], dict[str, str]]] = []

    repo_start = time.perf_counter()
    type_re = re.compile(r"type\s+([A-Za-z_][A-Za-z0-9_]*)\s+(?:struct|interface)")
    func_re = re.compile(r"func\s+(?:\((\w+)\s+\*?(\w+)\)\s*)?([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)")
    go_files = _iter_go_files(repo_root)
    method_symbols: dict[str, list[str]] = {}

    for file_index, file_path in enumerate(go_files, start=1):
        file_start = time.perf_counter()
        text = file_path.read_text(encoding="utf-8")
        rel_path = file_path.relative_to(repo_root).as_posix()
        module_id = f"module:{rel_path}"
        lines_list = text.splitlines()
        behavior_budget_enabled = file_path.stat().st_size <= GO_BEHAVIOR_FILE_SIZE_LIMIT_BYTES
        if not behavior_budget_enabled:
            print(
                f"[extract_go] skipping behavior patterns for {rel_path} "
                f"(size>{GO_BEHAVIOR_FILE_SIZE_LIMIT_BYTES} bytes)"
            )

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
                if receiver_type:
                    method_symbols.setdefault(func_name, []).append(node_id)
                doc = _extract_go_doc_comment(lines_list, line_no_0)
                # Build signature
                sig = f"({params})" if params else "()"
                if len(sig) > 60:
                    sig = sig[:57] + "...)"
                body_text = _extract_go_function_body(lines_list, line_no_0)
                behavior_patterns: list[str] = []
                if behavior_budget_enabled:
                    if len(body_text) <= GO_BEHAVIOR_BODY_SIZE_LIMIT_CHARS:
                        behavior_start = time.perf_counter()
                        behavior_patterns = _extract_go_behavior_patterns(body_text)
                        behavior_elapsed = time.perf_counter() - behavior_start
                        if behavior_elapsed > 1.0:
                            print(
                                f"[extract_go] slow behavior scan {rel_path}:{name} "
                                f"{behavior_elapsed:.2f}s"
                            )
                    else:
                        print(
                            f"[extract_go] skipping large behavior body {rel_path}:{name} "
                            f"({len(body_text)} chars)"
                        )
                    file_elapsed = time.perf_counter() - file_start
                    if file_elapsed > GO_BEHAVIOR_FILE_BUDGET_SECONDS:
                        behavior_budget_enabled = False
                        print(
                            f"[extract_go] disabling behavior patterns for {rel_path} "
                            f"after {file_elapsed:.2f}s at {name}"
                        )
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

        file_scan_records.append((lines_list, symbols))

        # Second pass: extract call edges + panic detection
        node_by_id = {n.node_id: n for n in nodes}
        current_func_id: str | None = None
        current_func_depth = 0
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
                current_func_depth = line.count("{") - line.count("}")
                continue
            if not current_func_id:
                continue

            # Detect panic calls
            if _GO_PANIC_RE.search(line):
                func_panics.setdefault(current_func_id, []).append("panic")

            emitted_call_targets: set[str] = set()

            def _emit_call_edge(sym_id: str, rel: str) -> None:
                if not sym_id or sym_id == current_func_id or sym_id in emitted_call_targets:
                    return
                emitted_call_targets.add(sym_id)
                edge_id = f"calls:{current_func_id}:{sym_id}:{line_no}"
                edges.append(
                    Edge(
                        edge_id=edge_id,
                        edge_type="calls",
                        from_node=current_func_id,
                        to_node=sym_id,
                        evidence={"rel": rel, "line": line_no},
                    )
                )

            for sym_name in dict.fromkeys(_GO_CALL_CANDIDATE_RE.findall(line)):
                _emit_call_edge(symbols.get(sym_name, ""), "regex_call")

            for receiver_name, method_name in dict.fromkeys(_GO_SHORT_RECEIVER_CALL_RE.findall(line)):
                if len(receiver_name) > 3:
                    continue
                for sym_id in method_symbols.get(method_name, []):
                    _emit_call_edge(sym_id, "short_receiver_call")
            current_func_depth += line.count("{") - line.count("}")
            if current_func_depth <= 0:
                current_func_id = None
                current_func_depth = 0

        # Update nodes with panic information
        for func_id, panics in func_panics.items():
            node = node_by_id.get(func_id)
            if node:
                node.semantic_contract["raises"] = list(dict.fromkeys(panics))[:3]

        if len(go_files) >= GO_BEHAVIOR_PROGRESS_EVERY and file_index % GO_BEHAVIOR_PROGRESS_EVERY == 0:
            print(
                f"[extract_go] processed {file_index}/{len(go_files)} files "
                f"in {time.perf_counter() - repo_start:.1f}s"
            )

    existing_edge_ids = {edge.edge_id for edge in edges}
    for lines_list, symbols in file_scan_records:
        current_func_id: str | None = None
        current_func_depth = 0
        for line_no_0, line in enumerate(lines_list):
            line_no = line_no_0 + 1
            m = func_re.search(line)
            if m:
                receiver_type = m.group(2)
                func_name = m.group(3)
                name = f"{receiver_type}.{func_name}" if receiver_type else func_name
                current_func_id = symbols.get(name)
                current_func_depth = line.count("{") - line.count("}")
                continue
            if not current_func_id:
                continue
            for receiver_name, method_name in dict.fromkeys(_GO_SHORT_RECEIVER_CALL_RE.findall(line)):
                if len(receiver_name) > 3:
                    continue
                for sym_id in method_symbols.get(method_name, []):
                    if sym_id == current_func_id:
                        continue
                    edge_id = f"calls:{current_func_id}:{sym_id}:{line_no}"
                    if edge_id in existing_edge_ids:
                        continue
                    existing_edge_ids.add(edge_id)
                    edges.append(
                        Edge(
                            edge_id=edge_id,
                            edge_type="calls",
                            from_node=current_func_id,
                            to_node=sym_id,
                            evidence={"rel": "short_receiver_call", "line": line_no},
                        )
                    )
            current_func_depth += line.count("{") - line.count("}")
            if current_func_depth <= 0:
                current_func_id = None
                current_func_depth = 0

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
