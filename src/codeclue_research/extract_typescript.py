from __future__ import annotations

import re
from dataclasses import dataclass
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
    tokens = re.findall(r"[$A-Za-z_][$A-Za-z0-9_]*(?:\.[$A-Za-z_][$A-Za-z0-9_]*)*", cleaned)
    tokens = [
        token
        for token in tokens
        if token
        not in {
            "if",
            "return",
            "else",
            "true",
            "false",
            "null",
            "undefined",
            "new",
            "await",
        }
    ]
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
        _, right = cleaned.split("instanceof", 1)
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
    condition_hints = set(re.findall(r"[$A-Za-z_][$A-Za-z0-9_]*", condition))
    value_hints = set(re.findall(r"[$A-Za-z_][$A-Za-z0-9_]*", value))
    if condition_hints and condition_hints.intersection(value_hints) and "(" not in value:
        return "pass_through"
    call_match = re.match(r"(?:await\s+)?(?:new\s+)?([$A-Za-z_][$A-Za-z0-9_\.]*)\s*\(", value)
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

    delegate_match = re.search(r"(?m)^\s*return\s+(?:await\s+)?([$A-Za-z_][$A-Za-z0-9_\.]*)\s*\(", body)
    if delegate_match and len(re.findall(r"\breturn\b", body)) == 1:
        patterns.append(f"DELEGATE({delegate_match.group(1)} -> result)")

    if re.search(r"\bfor\s*\(", body) or ".forEach(" in body:
        acc_match = re.search(
            r"(?s)(?:for\s*\([^)]*\)|\.forEach\s*\([^)]*\))\s*\{\s*(?:([$A-Za-z_][$A-Za-z0-9_\.]*)\s*\+=|([$A-Za-z_][$A-Za-z0-9_\.]*)\.(?:push|set|add|write)\()",
            body,
        )
        target = next((group for group in acc_match.groups() if group), "result") if acc_match else "result"
        patterns.append(f"ACCUMULATE(loop -> {target.replace('.', '_')[:24]})")

    if ".map(" in body:
        patterns.append("TRANSFORM(map)")

    return list(dict.fromkeys(patterns))[:3]


@dataclass
class _TSDecl:
    node_id: str
    node_type: str
    symbol_type: str
    symbol_name: str
    short_name: str
    start_line: int
    end_line: int
    start_col: int
    end_col: int
    body: str
    params: str = ""
    class_name: str = ""
    bases: list[str] | None = None


CLASS_RE = re.compile(
    r"^\s*(?:export\s+)?(?:default\s+)?(?:abstract\s+)?class\s+([$A-Za-z_][$A-Za-z0-9_]*)"
    r"(?:\s*<[^>{]+>)?(?:\s+extends\s+([$A-Za-z_][$A-Za-z0-9_\.]*))?"
)
INTERFACE_RE = re.compile(
    r"^\s*(?:export\s+)?interface\s+([$A-Za-z_][$A-Za-z0-9_]*)"
    r"(?:\s*<[^>{]+>)?(?:\s+extends\s+([$A-Za-z0-9_\.,\s]+))?"
)
FUNCTION_RE = re.compile(
    r"^\s*(?:export\s+)?(?:default\s+)?(?:(async)\s+)?function\s+([$A-Za-z_][$A-Za-z0-9_]*)"
    r"(?:\s*<[^>{]+>)?\s*\(([^)]*)\)"
)
ARROW_RE = re.compile(
    r"^\s*(?:export\s+)?(?:const|let|var)\s+([$A-Za-z_][$A-Za-z0-9_]*)\s*=\s*(?:(async)\s*)?"
    r"(?:<[^>{]+>\s*)?\(([^)]*)\)\s*(?::[^=]+)?=>"
)
TYPE_ALIAS_RE = re.compile(
    r"^\s*export\s+type\s+([$A-Za-z_][$A-Za-z0-9_]*)(?:\s*<[^>{]+>)?\s*=\s*(.+?);?\s*$"
)
METHOD_RE = re.compile(
    r"^\s*(?:(?:public|private|protected|static|readonly|override|abstract|get|set)\s+)*"
    r"(?:(async)\s+)?(constructor|[$A-Za-z_][$A-Za-z0-9_]*)"
    r"(?:\s*<[^>{]+>)?\s*\(([^)]*)\)\s*(?::\s*[^=;{]+)?\s*([;{])"
)


def _find_block_end(lines: list[str], start_idx: int) -> int:
    brace_depth = 0
    started = False
    for idx in range(start_idx, len(lines)):
        line = lines[idx]
        open_count = line.count("{")
        close_count = line.count("}")
        if open_count:
            started = True
        if started:
            brace_depth += open_count - close_count
            if brace_depth <= 0:
                return idx
    return start_idx


def _collect_ts_header(lines: list[str], start_idx: int, max_lines: int = 8) -> str:
    parts: list[str] = []
    for idx in range(start_idx, min(len(lines), start_idx + max_lines)):
        cleaned = re.sub(r"//.*", "", lines[idx]).strip()
        if cleaned:
            parts.append(cleaned)
        joined = " ".join(parts)
        if "{" in cleaned or ";" in cleaned or "=>" in cleaned:
            break
        if joined.count("(") > 0 and joined.count(")") >= joined.count("("):
            break
    return " ".join(parts)


def _split_bases(raw: str) -> list[str]:
    if not raw:
        return []
    bases: list[str] = []
    items: list[str] = []
    current: list[str] = []
    depth = 0
    for char in raw:
        if char == "<":
            depth += 1
        elif char == ">" and depth > 0:
            depth -= 1
        if char == "," and depth == 0:
            items.append("".join(current))
            current = []
            continue
        current.append(char)
    if current:
        items.append("".join(current))

    for item in items:
        candidate = item.strip().split(".")[-1]
        candidate = candidate.split("<", 1)[0].strip()
        if re.match(r"^[$A-Za-z_][$A-Za-z0-9_]*$", candidate):
            bases.append(candidate)
    return list(dict.fromkeys(bases))


def _extract_header_bases(header: str) -> list[str]:
    if " extends " not in header:
        return []
    raw = header.rsplit(" extends ", 1)[1]
    raw = raw.split("{", 1)[0].split(" implements ", 1)[0].strip()
    return _split_bases(raw)


def _extract_type_references(raw: str) -> list[str]:
    refs: list[str] = []
    for candidate in re.findall(r"[$A-Za-z_][$A-Za-z0-9_]*(?:\.[$A-Za-z_][$A-Za-z0-9_]*)*", raw):
        if candidate in {"export", "type", "extends", "readonly", "keyof", "typeof"}:
            continue
        refs.append(candidate)
    return list(dict.fromkeys(refs))


def _extract_ts_uses(body: str) -> list[str]:
    if not body:
        return []
    uses: list[str] = []
    for ref in re.findall(r"[$A-Za-z_][$A-Za-z0-9_]*(?:\.[$A-Za-z_][$A-Za-z0-9_]*)+", body):
        if ref in {"this", "super"}:
            continue
        uses.append(ref)
    return list(dict.fromkeys(uses))[:8]


def _signature_from_params(params: str) -> str:
    compact = " ".join(params.split())
    if not compact:
        return "()"
    if len(compact) > 60:
        compact = compact[:57] + "..."
    return f"({compact})"


def _resolve_decl_span(
    text: str,
    lines: list[str],
    start_line: int,
    name_start: int,
    end_line: int,
) -> tuple[int, int]:
    start, _ = _byte_span(text, start_line, name_start, name_start)
    end_line_text = lines[end_line - 1] if 0 < end_line <= len(lines) else ""
    _, end = _byte_span(text, end_line, 0, len(end_line_text))
    return start, max(start, end)


def _register_node(
    *,
    nodes: list[Node],
    edges: list[Edge],
    decls: list[_TSDecl],
    symbol_ids_by_name: dict[str, list[str]],
    text: str,
    lines: list[str],
    rel_path: str,
    module_id: str,
    symbol_name: str,
    short_name: str,
    node_type: str,
    symbol_type: str,
    start_line: int,
    end_line: int,
    start_col: int,
    end_col: int,
    body: str,
    params: str = "",
    class_name: str = "",
    bases: list[str] | None = None,
    purpose: str | None = None,
    uses: list[str] | None = None,
) -> str:
    node_id = f"symbol:{rel_path}:{symbol_name}:{start_line}"
    start, end = _resolve_decl_span(text, lines, start_line, start_col, end_line)
    snippet = text.encode("utf-8")[start:end].decode("utf-8", errors="ignore")
    behavior_patterns = _extract_ts_behavior_patterns(body) if body and node_type != "class" else []
    semantic_contract = {
        "purpose": purpose or f"{symbol_type} {symbol_name}",
        "language": "typescript",
        "symbol_name": symbol_name,
        "symbol_type": symbol_type,
        "signature": _signature_from_params(params) if node_type != "class" else "",
        "behavior_patterns": behavior_patterns,
        "tier": 1,
        "calls": [],
        "uses": list(uses or _extract_ts_uses(body)),
        "called_by": [],
        "complexity_indicators": {
            "decorator_depth": 0,
            "generic_type_param_count": 0,
        },
    }
    if bases:
        semantic_contract["bases"] = list(bases)
    nodes.append(
        Node(
            node_id=node_id,
            node_type=node_type,
            source_anchor=SourceAnchor(
                file_path=rel_path,
                byte_start=max(0, start),
                byte_end=max(start, end),
                ast_path=f"{symbol_type}:{symbol_name}",
                content_hash=_hash_text(snippet or symbol_name),
            ),
            semantic_contract=semantic_contract,
            confidence=0.86,
        )
    )
    edges.append(
        Edge(
            edge_id=f"contains:{module_id}:{node_id}",
            edge_type="contains",
            from_node=module_id,
            to_node=node_id,
            evidence={"rel": "regex_containment", "line": start_line},
        )
    )
    decls.append(
        _TSDecl(
            node_id=node_id,
            node_type=node_type,
            symbol_type=symbol_type,
            symbol_name=symbol_name,
            short_name=short_name,
            start_line=start_line,
            end_line=end_line,
            start_col=start_col,
            end_col=end_col,
            body=body,
            params=params,
            class_name=class_name,
            bases=list(bases or []),
        )
    )
    symbol_ids_by_name.setdefault(symbol_name, []).append(node_id)
    if short_name != symbol_name:
        symbol_ids_by_name.setdefault(short_name, []).append(node_id)
    return node_id


def _extract_class_members(
    *,
    text: str,
    lines: list[str],
    rel_path: str,
    module_id: str,
    class_name: str,
    class_node_id: str,
    class_start_idx: int,
    class_end_idx: int,
    nodes: list[Node],
    edges: list[Edge],
    decls: list[_TSDecl],
    symbol_ids_by_name: dict[str, list[str]],
) -> None:
    idx = class_start_idx + 1
    while idx < class_end_idx:
        line = lines[idx]
        stripped = re.sub(r"//.*", "", line).strip()
        if not stripped:
            idx += 1
            continue
        match = METHOD_RE.match(line)
        if not match:
            idx += 1
            continue
        async_flag, raw_name, params, terminator = match.groups()
        if raw_name in {"if", "for", "while", "switch", "catch", "return"}:
            idx += 1
            continue
        method_name = raw_name
        symbol_name = f"{class_name}.{method_name}"
        node_type = "async_function" if async_flag else "function"
        symbol_type = "async_method" if async_flag else "method"
        start_line = idx + 1
        end_line = start_line
        body = ""
        if terminator == "{":
            end_idx = _find_block_end(lines, idx)
            end_line = end_idx + 1
            body = _extract_ts_block(lines, idx)
            idx = end_idx + 1
        else:
            idx += 1
        method_node_id = _register_node(
            nodes=nodes,
            edges=edges,
            decls=decls,
            symbol_ids_by_name=symbol_ids_by_name,
            text=text,
            lines=lines,
            rel_path=rel_path,
            module_id=module_id,
            symbol_name=symbol_name,
            short_name=method_name,
            node_type=node_type,
            symbol_type=symbol_type,
            start_line=start_line,
            end_line=end_line,
            start_col=match.start(2),
            end_col=match.end(2),
            body=body,
            params=params,
            class_name=class_name,
        )
        edges.append(
            Edge(
                edge_id=f"contains:{class_node_id}:{method_node_id}",
                edge_type="contains",
                from_node=class_node_id,
                to_node=method_node_id,
                evidence={"rel": "method_of", "line": start_line},
            )
        )


def _extract_local_types(body: str, params: str) -> dict[str, str]:
    local_types: dict[str, str] = {}
    for name, type_name in re.findall(r"\b([$A-Za-z_][$A-Za-z0-9_]*)\s*:\s*([$A-Za-z_][$A-Za-z0-9_\.]*)", params):
        local_types[name] = type_name.split(".")[-1]
    for var_name, type_name in re.findall(
        r"\b(?:const|let|var)\s+([$A-Za-z_][$A-Za-z0-9_]*)\s*=\s*new\s+([$A-Za-z_][$A-Za-z0-9_]*)\s*\(",
        body,
    ):
        local_types[var_name] = type_name
    return local_types


def _unique_ids(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def _resolve_ts_call_targets(
    ref: str,
    *,
    current_class: str,
    local_types: dict[str, str],
    bases_by_class: dict[str, list[str]],
    symbol_ids_by_name: dict[str, list[str]],
    class_ids_by_name: dict[str, str],
) -> list[str]:
    if not ref:
        return []
    if "." not in ref:
        return _unique_ids(symbol_ids_by_name.get(ref, []))

    owner, member = ref.rsplit(".", 1)
    candidates: list[str] = []
    if owner == "this" and current_class:
        candidates.extend(symbol_ids_by_name.get(f"{current_class}.{member}", []))
        for base in bases_by_class.get(current_class, []):
            candidates.extend(symbol_ids_by_name.get(f"{base}.{member}", []))
        return _unique_ids(candidates or symbol_ids_by_name.get(member, []))

    if owner == "super" and current_class:
        for base in bases_by_class.get(current_class, []):
            candidates.extend(symbol_ids_by_name.get(f"{base}.{member}", []))
        return _unique_ids(candidates or symbol_ids_by_name.get(member, []))

    resolved_type = local_types.get(owner, owner)
    if resolved_type in class_ids_by_name:
        candidates.extend(symbol_ids_by_name.get(f"{resolved_type}.{member}", []))
    candidates.extend(symbol_ids_by_name.get(member, []))
    return _unique_ids(candidates)


def _iter_ts_calls(body: str) -> list[tuple[int, str, str]]:
    results: list[tuple[int, str, str]] = []
    for line_no, line in enumerate(body.splitlines(), start=0):
        if not line.strip():
            continue
        for match in re.finditer(r"\bnew\s+([$A-Za-z_][$A-Za-z0-9_]*)\s*\(", line):
            results.append((line_no, "new", match.group(1)))
        for match in re.finditer(
            r"(?<!function\s)(?<!class\s)(?<!interface\s)\b([$A-Za-z_][$A-Za-z0-9_]*(?:\.[$A-Za-z_][$A-Za-z0-9_]*)*)\s*\(",
            line,
        ):
            ref = match.group(1)
            if ref in {"if", "for", "while", "switch", "catch", "return", "new"}:
                continue
            results.append((line_no, "call", ref))
    return results


def extract_typescript_nodes_edges(repo_root: Path) -> tuple[list[Node], list[Edge]]:
    nodes: list[Node] = []
    edges: list[Edge] = []

    for file_path in _iter_ts_files(repo_root):
        try:
            text = file_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
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

        decls: list[_TSDecl] = []
        symbol_ids_by_name: dict[str, list[str]] = {}
        class_ids_by_name: dict[str, str] = {}
        bases_by_class: dict[str, list[str]] = {}

        idx = 0
        while idx < len(lines):
            line = lines[idx]
            header = _collect_ts_header(lines, idx)

            class_match = CLASS_RE.match(header)
            interface_match = INTERFACE_RE.match(header)
            func_match = FUNCTION_RE.match(header)
            arrow_match = ARROW_RE.match(header)
            type_alias_match = TYPE_ALIAS_RE.match(header)

            if class_match or interface_match:
                match = class_match or interface_match
                assert match is not None
                class_name = match.group(1)
                bases = _extract_header_bases(header)
                end_idx = _find_block_end(lines, idx)
                class_node_id = _register_node(
                    nodes=nodes,
                    edges=edges,
                    decls=decls,
                    symbol_ids_by_name=symbol_ids_by_name,
                    text=text,
                    lines=lines,
                    rel_path=rel_path,
                    module_id=module_id,
                    symbol_name=class_name,
                    short_name=class_name,
                    node_type="class",
                    symbol_type="interface" if interface_match else "class",
                    start_line=idx + 1,
                    end_line=end_idx + 1,
                    start_col=max(0, line.find(class_name)),
                    end_col=max(0, line.find(class_name)) + len(class_name),
                    body=_extract_ts_block(lines, idx),
                    bases=bases,
                )
                class_ids_by_name[class_name] = class_node_id
                if bases:
                    bases_by_class[class_name] = bases
                _extract_class_members(
                    text=text,
                    lines=lines,
                    rel_path=rel_path,
                    module_id=module_id,
                    class_name=class_name,
                    class_node_id=class_node_id,
                    class_start_idx=idx,
                    class_end_idx=end_idx,
                    nodes=nodes,
                    edges=edges,
                    decls=decls,
                    symbol_ids_by_name=symbol_ids_by_name,
                )
                idx = end_idx + 1
                continue

            if func_match:
                async_flag, func_name, params = func_match.groups()
                end_idx = _find_block_end(lines, idx)
                _register_node(
                    nodes=nodes,
                    edges=edges,
                    decls=decls,
                    symbol_ids_by_name=symbol_ids_by_name,
                    text=text,
                    lines=lines,
                    rel_path=rel_path,
                    module_id=module_id,
                    symbol_name=func_name,
                    short_name=func_name,
                    node_type="async_function" if async_flag else "function",
                    symbol_type="async_function" if async_flag else "function",
                    start_line=idx + 1,
                    end_line=end_idx + 1,
                    start_col=max(0, line.find(func_name)),
                    end_col=max(0, line.find(func_name)) + len(func_name),
                    body=_extract_ts_block(lines, idx),
                    params=params,
                )
                idx = end_idx + 1
                continue

            if arrow_match:
                func_name, async_flag, params = arrow_match.groups()
                end_idx = _find_block_end(lines, idx)
                _register_node(
                    nodes=nodes,
                    edges=edges,
                    decls=decls,
                    symbol_ids_by_name=symbol_ids_by_name,
                    text=text,
                    lines=lines,
                    rel_path=rel_path,
                    module_id=module_id,
                    symbol_name=func_name,
                    short_name=func_name,
                    node_type="async_function" if async_flag else "function",
                    symbol_type="async_function" if async_flag else "function",
                    start_line=idx + 1,
                    end_line=end_idx + 1,
                    start_col=max(0, line.find(func_name)),
                    end_col=max(0, line.find(func_name)) + len(func_name),
                    body=_extract_ts_block(lines, idx),
                    params=params,
                )
                idx = end_idx + 1
                continue

            if type_alias_match:
                alias_name, alias_target = type_alias_match.groups()
                _register_node(
                    nodes=nodes,
                    edges=edges,
                    decls=decls,
                    symbol_ids_by_name=symbol_ids_by_name,
                    text=text,
                    lines=lines,
                    rel_path=rel_path,
                    module_id=module_id,
                    symbol_name=alias_name,
                    short_name=alias_name,
                    node_type="type_alias",
                    symbol_type="type_alias",
                    start_line=idx + 1,
                    end_line=idx + 1,
                    start_col=max(0, line.find(alias_name)),
                    end_col=max(0, line.find(alias_name)) + len(alias_name),
                    body=header,
                    purpose=f"type alias {alias_name} = {alias_target.strip()}",
                    uses=_extract_type_references(alias_target),
                )
                idx += 1
                continue

            idx += 1

        for class_name, bases in bases_by_class.items():
            class_id = class_ids_by_name.get(class_name)
            if not class_id:
                continue
            for base in bases:
                base_ids = symbol_ids_by_name.get(base, [])
                if len(base_ids) != 1:
                    continue
                edges.append(
                    Edge(
                        edge_id=f"inherits:{class_id}:{base_ids[0]}",
                        edge_type="inherits",
                        from_node=class_id,
                        to_node=base_ids[0],
                        evidence={"rel": "extends"},
                    )
                )

        for decl in decls:
            if not decl.body:
                continue
            local_types = _extract_local_types(decl.body, decl.params)
            seen_edges: set[tuple[str, str, int]] = set()
            for rel_line, kind, ref in _iter_ts_calls(decl.body):
                line_no = decl.start_line + rel_line
                candidate_ids: list[str] = []
                if kind == "new":
                    candidate_ids = symbol_ids_by_name.get(ref, [])
                else:
                    candidate_ids = _resolve_ts_call_targets(
                        ref,
                        current_class=decl.class_name,
                        local_types=local_types,
                        bases_by_class=bases_by_class,
                        symbol_ids_by_name=symbol_ids_by_name,
                        class_ids_by_name=class_ids_by_name,
                    )
                for callee_id in candidate_ids:
                    if callee_id == decl.node_id:
                        continue
                    edge_key = (decl.node_id, callee_id, line_no)
                    if edge_key in seen_edges:
                        continue
                    seen_edges.add(edge_key)
                    edges.append(
                        Edge(
                            edge_id=f"calls:{decl.node_id}:{callee_id}:{line_no}",
                            edge_type="calls",
                            from_node=decl.node_id,
                            to_node=callee_id,
                            evidence={"rel": "regex_call", "line": line_no},
                        )
                    )

    return nodes, edges
