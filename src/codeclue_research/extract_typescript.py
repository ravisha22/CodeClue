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


def _extract_ts_block(lines: list[str], start_idx: int) -> str:
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


def _clean_ts_expr(expr: str) -> str:
    expr = re.sub(r"//.*", "", expr).strip()
    expr = expr.removeprefix("return").strip()
    return expr.strip(" {}();")


def _ts_ref_summary(expr: str, *, source: bool = False) -> str:
    cleaned = _clean_ts_expr(expr)
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*", cleaned)
    tokens = [token for token in tokens if token not in {"if", "return", "else", "true", "false", "null", "undefined", "new", "await"}]
    if not tokens:
        if "{}" in expr or "[]" in expr:
            return "empty"
        return "value"
    token = tokens[0]
    if source:
        if token.startswith("this."):
            token = token.split(".", 1)[1]
        elif "." in token:
            token = token.split(".", 1)[0]
        return token.replace(".", "_")[:24]
    return token[:28]


def _summarize_ts_condition(expr: str) -> str:
    cleaned = _clean_ts_expr(expr)
    if cleaned.startswith("!"):
        return f"not_{_ts_ref_summary(cleaned[1:], source=True)}"
    if re.search(r"===?\s*(null|undefined|false)\b", cleaned):
        return _ts_ref_summary(re.split(r"===?|!==?", cleaned, maxsplit=1)[0], source=True)
    if re.search(r"!==?\s*(null|undefined)\b", cleaned):
        return _ts_ref_summary(re.split(r"===?|!==?", cleaned, maxsplit=1)[0], source=True)
    if cleaned.startswith("instanceof "):
        return _ts_ref_summary(cleaned.removeprefix("instanceof "), source=True)
    if "instanceof" in cleaned:
        left, right = cleaned.split("instanceof", 1)
        return f"isinstance_{_ts_ref_summary(right, source=True)}"[:28]
    return _ts_ref_summary(cleaned, source=True)


def _summarize_ts_action(expr: str, condition: str = "") -> str:
    value = _clean_ts_expr(expr)
    if not value:
        return "result"
    if value in {"null", "undefined"}:
        return "none"
    if value in {"{}", "[]"}:
        return "empty"
    condition_hints = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", condition))
    value_hints = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", value))
    if condition_hints and condition_hints.intersection(value_hints) and "(" not in value:
        return "pass_through"
    call_match = re.match(r"(?:await\s+)?(?:new\s+)?([A-Za-z_][A-Za-z0-9_\.]*)\s*\(", value)
    if call_match:
        callee = call_match.group(1).split(".")[-1]
        if condition_hints and condition_hints.intersection(value_hints):
            return f"wrap_{callee}"[:24]
        return callee[:24]
    return _ts_ref_summary(value)


def _extract_ts_behavior_patterns(body: str) -> list[str]:
    patterns: list[str] = []
    if not body:
        return patterns

    guard_match = re.search(r"(?s)if\s*\(([^)]*)\)\s*\{\s*([^{}]*return\b[^{};]*;?)\s*\}(?!\s*else\b)", body)
    if guard_match:
        guard_condition = _summarize_ts_condition(guard_match.group(1))
        guard_action = _summarize_ts_action(guard_match.group(2), guard_match.group(1))
        patterns.append(f"GUARD({guard_condition} -> {guard_action})")

    switch_match = re.search(r"\bswitch\s*\(([^)]*)\)", body)
    if switch_match:
        patterns.append(f"DISPATCH({_ts_ref_summary(switch_match.group(1), source=True)})")

    chain_matches = re.findall(r"(?:if|else\s+if)\s*\(([^)]*)\)\s*\{", body)
    if len(chain_matches) >= 2 and len(re.findall(r"\breturn\b", body)) >= 2:
        sources = [_summarize_ts_condition(cond) for cond in chain_matches[:3]]
        if re.search(r"\belse\s*\{", body):
            sources.append("default")
        patterns.append(f"PRECEDENCE({' -> '.join(dict.fromkeys(sources))})")

    branch_match = re.search(
        r"(?s)if\s*\(([^)]*)\)\s*\{\s*([^{}]*return\b[^{};]*;?)\s*\}\s*else\s*\{\s*([^{}]*return\b[^{};]*;?)\s*\}",
        body,
    )
    if branch_match:
        cond = _summarize_ts_condition(branch_match.group(1))
        true_action = _summarize_ts_action(branch_match.group(2), branch_match.group(1))
        false_action = _summarize_ts_action(branch_match.group(3), branch_match.group(1))
        patterns.append(f"BRANCH({cond} -> {true_action}, else -> {false_action})")

    delegate_match = re.search(r"(?m)^\s*return\s+(?:await\s+)?([A-Za-z_][A-Za-z0-9_\.]*)\s*\(", body)
    if delegate_match and len(re.findall(r"\breturn\b", body)) == 1:
        patterns.append(f"DELEGATE({delegate_match.group(1)} -> result)")

    if re.search(r"\bfor\s*\(", body) or ".forEach(" in body:
        acc_match = re.search(
            r"(?s)(?:for\s*\([^)]*\)|\.forEach\s*\([^)]*\))\s*\{\s*(?:([A-Za-z_][A-Za-z0-9_\.]*)\s*\+=|([A-Za-z_][A-Za-z0-9_\.]*)\.(?:push|set|add|write)\()",
            body,
        )
        target = next((group for group in acc_match.groups() if group), "result") if acc_match else "result"
        patterns.append(f"ACCUMULATE(loop -> {target.replace('.', '_')[:24]})")

    if ".map(" in body:
        patterns.append("TRANSFORM(map)")

    return list(dict.fromkeys(patterns))[:3]


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
        lines = text.splitlines()
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
        for line_no, line in enumerate(lines, start=1):
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
                behavior_patterns: list[str] = []
                if symbol_type == "function":
                    behavior_patterns = _extract_ts_behavior_patterns(_extract_ts_block(lines, line_no - 1))
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

        for line_no, line in enumerate(lines, start=1):
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
