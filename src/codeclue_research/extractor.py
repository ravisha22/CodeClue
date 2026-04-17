from __future__ import annotations

import ast
import json
import hashlib
import re
import tomllib
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
    docstring: str = ""
    signature: str = ""
    bases: list[str] = None  # parent class names (for classes)
    class_attrs: dict[str, str] = None  # class-level attribute name -> literal value
    raises: list[str] = None  # exception class names raised
    uses: list[str] = None  # external classes/functions instantiated ("Name (module)")
    behavior_patterns: list[str] = None  # universal control flow patterns

    def __post_init__(self):
        if self.bases is None:
            self.bases = []
        if self.class_attrs is None:
            self.class_attrs = {}
        if self.raises is None:
            self.raises = []
        if self.uses is None:
            self.uses = []
        if self.behavior_patterns is None:
            self.behavior_patterns = []


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


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


def _get_call_name(node: ast.AST | None) -> str:
    if node is None:
        return ""
    target = node.func if isinstance(node, ast.Call) else node
    if isinstance(target, ast.Name):
        return target.id
    if isinstance(target, ast.Attribute):
        return target.attr
    return ""


def _has_return(node: ast.AST) -> bool:
    return any(isinstance(child, ast.Return) for child in ast.walk(node))


def _is_early_exit(node: ast.If) -> bool:
    return any(isinstance(stmt, (ast.Return, ast.Raise)) for stmt in node.body)


def _clip_summary(text: str, *, max_parts: int = 4, max_len: int = 32) -> str:
    normalized = text.replace(" ", "_")
    parts = [part for part in normalized.split("_") if part]
    if parts:
        normalized = "_".join(parts[:max_parts])
    if len(normalized) > max_len:
        normalized = normalized[:max_len].rstrip("_")
    return normalized or "value"


def _compact_text(text: str) -> str:
    return " ".join(text.split())


def _truncate_text(text: str, max_len: int) -> str:
    compact = _compact_text(text)
    if len(compact) <= max_len:
        return compact
    return compact[: max_len - 3].rstrip() + "..."


def _pattern_text(prefix: str, detail: str, *, max_len: int = 80) -> str:
    text = f"{prefix}({detail})"
    if len(text) <= max_len:
        return text
    return f"{prefix}({_truncate_text(detail, max_len - len(prefix) - 2)})"


def _expr_text(node: ast.AST | None, *, max_len: int = 60) -> str:
    if node is None:
        return "condition"
    try:
        text = ast.unparse(node)
    except Exception:
        text = _reference_summary(node)
    return _truncate_text(text, max_len)


def _literal_summary(node: ast.AST | None) -> str:
    if isinstance(node, ast.Constant):
        if node.value is None:
            return "none"
        if isinstance(node.value, bool):
            return str(node.value).lower()
        return _clip_summary(str(node.value), max_parts=3, max_len=20)
    if isinstance(node, ast.Dict) and not node.keys:
        return "empty"
    if isinstance(node, (ast.List, ast.Set, ast.Tuple)) and not node.elts:
        return "empty"
    return "value"


def _reference_summary(node: ast.AST | None) -> str:
    if node is None:
        return "value"
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _reference_summary(node.value)
        if parent in {"self", "cls", "value"}:
            return node.attr
        return f"{parent}.{node.attr}"
    if isinstance(node, ast.Subscript):
        return _reference_summary(node.value)
    if isinstance(node, ast.Call):
        return _reference_summary(node.func)
    if isinstance(node, ast.Constant):
        return _literal_summary(node)
    if isinstance(node, (ast.Dict, ast.List, ast.Set, ast.Tuple)):
        return _literal_summary(node)
    return type(node).__name__.lower()


def _approx_token_count(text: str) -> int:
    return max(1, len(re.findall(r"\S+", text)))


def _truncate_to_tokens(text: str, max_tokens: int) -> str:
    words = text.split()
    if len(words) <= max_tokens:
        return text
    return " ".join(words[:max_tokens]) + " ..."


def _find_repo_files(repo_root: Path, file_names: list[str], *, max_matches_per_name: int = 3) -> list[Path]:
    matches: list[Path] = []
    seen: set[Path] = set()
    for name in file_names:
        candidates = sorted(
            (
                path for path in repo_root.rglob(name)
                if not any(part.startswith(".") for part in path.relative_to(repo_root).parts[:-1])
            ),
            key=lambda path: (len(path.relative_to(repo_root).parts), path.as_posix()),
        )
        for path in candidates[:max_matches_per_name]:
            if path not in seen:
                seen.add(path)
                matches.append(path)
    return matches


def _make_aux_node(
    repo_root: Path,
    file_path: Path,
    *,
    node_id: str,
    node_type: str,
    symbol_name: str,
    purpose: str,
    confidence: float = 0.86,
    extra_contract: dict | None = None,
    snippet_text: str | None = None,
) -> Node:
    rel_path = file_path.relative_to(repo_root).as_posix()
    raw_text = snippet_text
    if raw_text is None:
        try:
            raw_text = file_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            raw_text = ""
    contract = {
        "purpose": purpose,
        "language": "config" if node_type == "config" else "documentation",
        "symbol_name": symbol_name,
        "symbol_type": node_type,
        "tier": 1,
        "calls": [],
        "called_by": [],
        "complexity_indicators": {
            "decorator_depth": 0,
            "generic_type_param_count": 0,
        },
    }
    if extra_contract:
        contract.update(extra_contract)
    return Node(
        node_id=node_id,
        node_type=node_type,
        source_anchor=SourceAnchor(
            file_path=rel_path,
            byte_start=0,
            byte_end=len(raw_text.encode("utf-8")),
            ast_path=node_type,
            content_hash=_hash_text(raw_text),
        ),
        semantic_contract=contract,
        confidence=confidence,
    )


def _parse_python_config_entries(text: str) -> tuple[list[str], dict[str, list[str]]]:
    entries: list[str] = []
    settings_refs: dict[str, list[str]] = {}
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return entries, settings_refs

    interesting = {"INSTALLED_APPS", "MIDDLEWARE", "DATABASES"}
    for node in tree.body:
        target_name = None
        value = None
        if isinstance(node, ast.Assign):
            if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                target_name = node.targets[0].id
                value = node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            target_name = node.target.id
            value = node.value
        if not target_name or value is None:
            continue

        if target_name.isupper():
            summary = _expr_text(value, max_len=100)
            entries.append(f"{target_name}={summary}")

        if target_name in interesting:
            refs: list[str] = []
            if isinstance(value, (ast.List, ast.Tuple)):
                for elt in value.elts[:12]:
                    ref = _reference_summary(elt).strip("'\"")
                    if ref:
                        refs.append(ref)
            elif isinstance(value, ast.Dict):
                for key in value.keys[:8]:
                    ref = _reference_summary(key).strip("'\"")
                    if ref:
                        refs.append(ref)
            if refs:
                settings_refs[target_name] = refs

    return entries[:12], settings_refs


def _parse_env_entries(text: str) -> list[str]:
    entries: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key:
            entries.append(f"{key}={_truncate_text(value, 40) if value else '<set>'}")
    return entries[:15]


def _parse_package_json(text: str) -> tuple[list[str], list[str]]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return [], []
    dependencies: list[str] = []
    for section in ("dependencies", "devDependencies", "peerDependencies"):
        block = payload.get(section, {})
        if isinstance(block, dict):
            dependencies.extend(block.keys())
    scripts = list(payload.get("scripts", {}).keys()) if isinstance(payload.get("scripts"), dict) else []
    return list(dict.fromkeys(dependencies))[:20], scripts[:10]


def _parse_pyproject(text: str) -> tuple[list[str], list[str]]:
    try:
        payload = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return [], []

    dependencies: list[str] = []
    scripts: list[str] = []

    project = payload.get("project", {})
    if isinstance(project, dict):
        for item in project.get("dependencies", [])[:20]:
            if isinstance(item, str):
                dependencies.append(item.split()[0])
        if isinstance(project.get("scripts"), dict):
            scripts.extend(project["scripts"].keys())

    poetry = payload.get("tool", {}).get("poetry", {}) if isinstance(payload.get("tool"), dict) else {}
    if isinstance(poetry, dict):
        deps = poetry.get("dependencies", {})
        if isinstance(deps, dict):
            dependencies.extend(k for k in deps.keys() if k.lower() != "python")
        poetry_scripts = poetry.get("scripts", {})
        if isinstance(poetry_scripts, dict):
            scripts.extend(poetry_scripts.keys())

    build_system = payload.get("build-system", {})
    if isinstance(build_system, dict):
        for item in build_system.get("requires", [])[:10]:
            if isinstance(item, str):
                dependencies.append(item.split()[0])

    return list(dict.fromkeys(dependencies))[:20], list(dict.fromkeys(scripts))[:10]


def _parse_compose_services(text: str) -> tuple[list[str], list[str]]:
    services: list[str] = []
    details: list[str] = []
    lines = text.splitlines()
    in_services = False
    service_indent = None
    current_service = ""
    current_props: list[str] = []

    def _flush() -> None:
        if current_service:
            services.append(current_service)
            if current_props:
                details.append(f"{current_service}: {', '.join(current_props[:4])}")

    for raw_line in lines:
        line = raw_line.split("#", 1)[0].rstrip()
        if not line:
            continue
        if not in_services:
            if line.strip() == "services:":
                in_services = True
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        if indent == 0:
            break

        service_match = re.match(r"^\s{2,}([A-Za-z0-9_.-]+):\s*$", raw_line)
        if service_match:
            _flush()
            current_service = service_match.group(1)
            current_props = []
            service_indent = indent
            continue

        if not current_service or service_indent is None or indent <= service_indent:
            continue

        prop_match = re.match(r"^\s+[A-Za-z0-9_.-]+:\s*(.+)$", raw_line)
        if prop_match:
            current_props.append(_truncate_text(prop_match.group(1).strip(), 40))

    _flush()
    return services[:10], details[:10]


def _summarize_doc_text(text: str, *, max_headings: int = 6, max_lines: int = 4) -> tuple[list[str], list[str]]:
    headings: list[str] = []
    summary_lines: list[str] = []
    architecture_keywords = {
        "architecture", "service", "worker", "queue", "database", "api",
        "auth", "docker", "deploy", "stack", "webhook", "celery", "django",
    }
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
            if heading and heading not in headings:
                headings.append(heading)
            continue
        if line.startswith(("-", "*", "`", "```")):
            continue
        lowered = line.lower()
        if any(keyword in lowered for keyword in architecture_keywords) or len(summary_lines) < 2:
            compact = _truncate_text(line, 120)
            if compact not in summary_lines:
                summary_lines.append(compact)
        if len(headings) >= max_headings and len(summary_lines) >= max_lines:
            break
    return headings[:max_headings], summary_lines[:max_lines]


def _extract_config_context(repo_root: Path, *, max_tokens: int = 500) -> tuple[list[Node], list[Edge]]:
    nodes: list[Node] = []
    edges: list[Edge] = []
    used_tokens = 0
    config_files = _find_repo_files(
        repo_root,
        ["settings.py", "config.py", ".env.example", "docker-compose.yml", "pyproject.toml", "package.json"],
    )

    for file_path in config_files:
        try:
            text = file_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        rel_path = file_path.relative_to(repo_root).as_posix()
        entries: list[str] = []
        dependencies: list[str] = []
        services: list[str] = []
        extra: dict = {"context_kind": "config"}

        lowered = file_path.name.lower()
        if lowered in {"settings.py", "config.py"}:
            entries, settings_refs = _parse_python_config_entries(text)
            if settings_refs:
                extra["settings_refs"] = settings_refs
        elif lowered == ".env.example":
            entries = _parse_env_entries(text)
        elif lowered == "docker-compose.yml":
            services, entries = _parse_compose_services(text)
        elif lowered == "pyproject.toml":
            dependencies, scripts = _parse_pyproject(text)
            if scripts:
                extra["scripts"] = scripts
        elif lowered == "package.json":
            dependencies, scripts = _parse_package_json(text)
            if scripts:
                extra["scripts"] = scripts

        summary_parts: list[str] = []
        if entries:
            summary_parts.append(f"entries: {', '.join(entries[:6])}")
        if services:
            summary_parts.append(f"services: {', '.join(services[:6])}")
        if dependencies:
            summary_parts.append(f"deps: {', '.join(dependencies[:8])}")
        if not summary_parts:
            continue

        purpose = f"Config summary for {rel_path}: " + "; ".join(summary_parts)
        entry_tokens = _approx_token_count(purpose)
        if used_tokens + entry_tokens > max_tokens:
            remaining = max(20, max_tokens - used_tokens)
            purpose = _truncate_to_tokens(purpose, remaining)
            entry_tokens = _approx_token_count(purpose)
        if used_tokens + entry_tokens > max_tokens:
            break

        extra.update({
            "config_entries": entries[:10],
            "services": services[:10],
            "dependencies": dependencies[:12],
            "summary": purpose,
        })
        node = _make_aux_node(
            repo_root,
            file_path,
            node_id=f"config:{rel_path}",
            node_type="config",
            symbol_name=rel_path,
            purpose=purpose,
            confidence=0.88,
            extra_contract=extra,
            snippet_text=text,
        )
        nodes.append(node)
        used_tokens += entry_tokens

    return nodes, edges


def _extract_doc_context(repo_root: Path, *, max_tokens: int = 300) -> tuple[list[Node], list[Edge]]:
    nodes: list[Node] = []
    edges: list[Edge] = []
    used_tokens = 0
    doc_files = _find_repo_files(repo_root, ["README.md", "mkdocs.yml", "docusaurus.config.js", "index.md"])
    preferred = []
    for path in doc_files:
        rel = path.relative_to(repo_root).as_posix()
        if rel == "README.md" or rel == "docs/index.md" or path.name in {"mkdocs.yml", "docusaurus.config.js"}:
            preferred.append(path)
    seen: set[Path] = set()
    ordered = []
    for path in preferred + doc_files:
        if path not in seen:
            seen.add(path)
            ordered.append(path)

    for file_path in ordered:
        rel_path = file_path.relative_to(repo_root).as_posix()
        if rel_path not in {"README.md", "docs/index.md"} and file_path.name not in {"mkdocs.yml", "docusaurus.config.js"}:
            continue
        try:
            text = file_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        snippet_lines = text.splitlines()[:200] if file_path.name.lower() == "readme.md" else text.splitlines()[:120]
        snippet_text = "\n".join(snippet_lines)
        headings, summary_lines = _summarize_doc_text(snippet_text)
        if not headings and not summary_lines:
            continue

        purpose_parts = []
        if summary_lines:
            purpose_parts.append(" ".join(summary_lines[:2]))
        if headings:
            purpose_parts.append("sections: " + ", ".join(headings[:5]))
        purpose = f"Documentation summary for {rel_path}: " + "; ".join(purpose_parts)
        entry_tokens = _approx_token_count(purpose)
        if used_tokens + entry_tokens > max_tokens:
            remaining = max(20, max_tokens - used_tokens)
            purpose = _truncate_to_tokens(purpose, remaining)
            entry_tokens = _approx_token_count(purpose)
        if used_tokens + entry_tokens > max_tokens:
            break

        extra = {
            "context_kind": "doc",
            "doc_kind": "readme" if rel_path == "README.md" else "doc",
            "headings": headings[:8],
            "summary_lines": summary_lines[:4],
            "summary": purpose,
        }
        nodes.append(
            _make_aux_node(
                repo_root,
                file_path,
                node_id=f"doc:{rel_path}",
                node_type="doc",
                symbol_name=rel_path,
                purpose=purpose,
                confidence=0.84,
                extra_contract=extra,
                snippet_text=snippet_text,
            )
        )
        used_tokens += entry_tokens

    return nodes, edges


def _identifier_hints(node: ast.AST | None) -> list[str]:
    if node is None:
        return []

    hints: list[str] = []

    def visit(expr: ast.AST | None) -> None:
        if expr is None:
            return
        if isinstance(expr, ast.Name):
            if expr.id not in {"self", "cls"}:
                hints.append(expr.id)
            return
        if isinstance(expr, ast.Attribute):
            name = _reference_summary(expr).replace(".", "_")
            if name not in {"self", "cls"}:
                hints.append(name)
            visit(expr.value)
            return
        if isinstance(expr, ast.Call):
            visit(expr.func)
            for arg in expr.args[:3]:
                visit(arg)
            return
        if isinstance(expr, ast.Subscript):
            visit(expr.value)
            visit(expr.slice)
            return
        if isinstance(expr, ast.Compare):
            visit(expr.left)
            for item in expr.comparators[:2]:
                visit(item)
            return
        if isinstance(expr, ast.BoolOp):
            for item in expr.values[:2]:
                visit(item)
            return
        if isinstance(expr, ast.UnaryOp):
            visit(expr.operand)
            return
        if isinstance(expr, (ast.Tuple, ast.List, ast.Set)):
            for item in expr.elts[:2]:
                visit(item)
            return

    visit(node)
    return list(dict.fromkeys(hints))


def _compare_word(op: ast.AST) -> str:
    mapping = {
        ast.Eq: "eq",
        ast.NotEq: "not",
        ast.Is: "is",
        ast.IsNot: "not",
        ast.In: "in",
        ast.NotIn: "notin",
        ast.Lt: "lt",
        ast.LtE: "lte",
        ast.Gt: "gt",
        ast.GtE: "gte",
    }
    return mapping.get(type(op), "cmp")


def _summarize_condition(node: ast.AST | None) -> str:
    if node is None:
        return "condition"
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        return _clip_summary(f"not {_summarize_condition(node.operand)}", max_parts=5, max_len=28)
    if isinstance(node, ast.BoolOp):
        joiner = " and " if isinstance(node.op, ast.And) else " or "
        parts = [_summarize_condition(part) for part in node.values[:2]]
        return _clip_summary(joiner.join(parts), max_parts=6, max_len=32)
    if isinstance(node, ast.Call):
        callee = _reference_summary(node.func)
        if callee == "isinstance" and len(node.args) >= 2:
            return _clip_summary(f"isinstance {_reference_summary(node.args[1])}", max_parts=4, max_len=28)
        if callee == "hasattr" and len(node.args) >= 2:
            return _clip_summary(f"hasattr {_reference_summary(node.args[1])}", max_parts=4, max_len=28)
        return _clip_summary(callee, max_parts=4, max_len=28)
    if isinstance(node, ast.Compare):
        left = _reference_summary(node.left)
        right = _reference_summary(node.comparators[0]) if node.comparators else "value"
        op = node.ops[0] if node.ops else None
        if right in {"none", "empty"} and op and isinstance(op, (ast.Is, ast.IsNot, ast.Eq, ast.NotEq)):
            return _clip_summary(left, max_parts=4, max_len=28)
        if right in {"true", "false"} and op and isinstance(op, (ast.Is, ast.IsNot, ast.Eq, ast.NotEq)):
            return _clip_summary(f"{left}_{right}", max_parts=4, max_len=28)
        return _clip_summary(f"{left} {_compare_word(op) if op else 'cmp'} {right}", max_parts=5, max_len=28)
    if isinstance(node, (ast.Attribute, ast.Name, ast.Subscript)):
        return _clip_summary(_reference_summary(node), max_parts=4, max_len=28)
    if isinstance(node, ast.Constant):
        return _literal_summary(node)
    return type(node).__name__.lower()


def _find_terminal_action(stmts: list[ast.stmt]) -> ast.stmt | None:
    for stmt in stmts:
        if isinstance(stmt, (ast.Return, ast.Raise)):
            return stmt
        if isinstance(stmt, ast.If):
            nested = _find_terminal_action(stmt.body)
            if nested:
                return nested
            nested = _find_terminal_action(stmt.orelse)
            if nested:
                return nested
    return None


def _terminal_action_text(stmts: list[ast.stmt], *, max_len: int = 28) -> str:
    action = _find_terminal_action(stmts)
    if isinstance(action, ast.Return):
        if action.value is None:
            return "return"
        return _truncate_text(f"return {ast.unparse(action.value)}", max_len)
    if isinstance(action, ast.Raise):
        exc = ast.unparse(action.exc) if action.exc is not None else "Exception"
        return _truncate_text(f"raise {exc}", max_len)
    for stmt in stmts:
        if isinstance(stmt, ast.Expr):
            return _truncate_text(ast.unparse(stmt.value), max_len)
        if isinstance(stmt, ast.Assign):
            return _truncate_text(ast.unparse(stmt.value), max_len)
    return "result"


def _summarize_action(stmts: list[ast.stmt], context: ast.AST | None = None) -> str:
    action = _find_terminal_action(stmts)
    context_hints = set(_identifier_hints(context))
    if isinstance(action, ast.Return):
        value = action.value
        if value is None:
            return "none"
        if isinstance(value, ast.Await):
            value = value.value
        if isinstance(value, (ast.Dict, ast.List, ast.Set, ast.Tuple)):
            return _literal_summary(value)
        if isinstance(value, ast.Constant):
            return _literal_summary(value)
        if isinstance(value, (ast.Name, ast.Attribute, ast.Subscript)):
            ref = _reference_summary(value).replace(".", "_")
            if context_hints and any(hint in ref for hint in context_hints):
                return "pass_through"
            return _clip_summary(ref, max_parts=4, max_len=24)
        if isinstance(value, ast.Call):
            callee = _reference_summary(value.func).replace(".", "_")
            arg_hints = set()
            for arg in value.args[:3]:
                arg_hints.update(_identifier_hints(arg))
            if context_hints and context_hints.intersection(arg_hints):
                return _clip_summary(f"wrap {callee}", max_parts=4, max_len=24)
            return _clip_summary(callee, max_parts=4, max_len=24)
    if isinstance(action, ast.Raise):
        exc = action.exc
        if isinstance(exc, ast.Call):
            return _clip_summary(f"raise {_reference_summary(exc.func)}", max_parts=4, max_len=24)
        return _clip_summary(f"raise {_reference_summary(exc)}", max_parts=4, max_len=24)
    return "result"


def _summarize_source(node: ast.AST | None) -> str:
    if node is None:
        return "default"
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        return _summarize_source(node.operand)
    if isinstance(node, ast.BoolOp) and node.values:
        return _summarize_source(node.values[0])
    if isinstance(node, ast.Compare):
        return _clip_summary(_reference_summary(node.left).replace(".", "_"), max_parts=4, max_len=20)
    if isinstance(node, ast.Call):
        callee = _reference_summary(node.func)
        if "." in callee:
            return _clip_summary(callee.rsplit(".", 1)[0].replace(".", "_"), max_parts=4, max_len=20)
        if node.args:
            first = _summarize_source(node.args[0])
            if first != "default":
                return first
        return _clip_summary(callee.replace(".", "_"), max_parts=4, max_len=20)
    if isinstance(node, (ast.Attribute, ast.Name, ast.Subscript)):
        return _clip_summary(_reference_summary(node).replace(".", "_"), max_parts=4, max_len=20)
    if isinstance(node, ast.Constant):
        return _literal_summary(node)
    return "default"


def _extract_accumulator_target(loop: ast.stmt) -> str:
    for child in ast.walk(loop):
        if isinstance(child, ast.AugAssign):
            return _clip_summary(_reference_summary(child.target).replace(".", "_"), max_parts=4, max_len=24)
        if isinstance(child, ast.Assign) and isinstance(child.value, ast.BinOp) and isinstance(child.value.op, ast.Add):
            return _clip_summary(_reference_summary(child.targets[0]).replace(".", "_"), max_parts=4, max_len=24)
        if isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute) and child.func.attr in {"append", "extend", "update", "add", "write"}:
            return _clip_summary(_reference_summary(child.func.value).replace(".", "_"), max_parts=4, max_len=24)
    return "result"


def _extract_accumulator_detail(loop: ast.stmt) -> str:
    for child in ast.walk(loop):
        if isinstance(child, ast.AugAssign):
            target = _reference_summary(child.target).replace(".", "_")
            value = _reference_summary(child.value).replace(".", "_")
            return _clip_summary(f"{target} {value}", max_parts=5, max_len=28)
        if isinstance(child, ast.Assign) and isinstance(child.value, ast.BinOp) and isinstance(child.value.op, ast.Add):
            target = _reference_summary(child.targets[0]).replace(".", "_")
            value = _reference_summary(child.value.right).replace(".", "_")
            return _clip_summary(f"{target} {value}", max_parts=5, max_len=28)
        if isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute) and child.func.attr in {"append", "extend", "update", "add", "write"}:
            container = _reference_summary(child.func.value).replace(".", "_")
            arg = _reference_summary(child.args[0]).replace(".", "_") if child.args else child.func.attr
            return _clip_summary(f"{container} {arg}", max_parts=5, max_len=28)
    return _extract_accumulator_target(loop)


def _loop_label(loop: ast.stmt) -> str:
    if isinstance(loop, (ast.For, ast.AsyncFor)):
        return _truncate_text(f"{ast.unparse(loop.iter)} loop", 24)
    if isinstance(loop, ast.While):
        for child in ast.walk(loop):
            if isinstance(child, ast.Call):
                return _truncate_text(f"{_reference_summary(child.func)} loop", 24)
        return _truncate_text(f"{_expr_text(loop.test, max_len=18)} loop", 24)
    return "loop"


def _loop_raises(loop: ast.stmt) -> str:
    for child in ast.walk(loop):
        if isinstance(child, ast.Raise):
            exc = child.exc
            if isinstance(exc, ast.Call):
                return _truncate_text(_reference_summary(exc.func), 20)
            if exc is not None:
                return _truncate_text(_reference_summary(exc), 20)
    return ""


def _guarded_name(test: ast.AST | None) -> str:
    if isinstance(test, ast.Compare):
        return _reference_summary(test.left).replace(".", "_")
    return ""


def _summarize_precedence_step(stmt: ast.If, guarded_name: str) -> str:
    for child in stmt.body:
        if isinstance(child, ast.Assign):
            for target in child.targets:
                target_name = _reference_summary(target).replace(".", "_")
                if target_name and target_name != guarded_name:
                    return _clip_summary(target_name.removesuffix("_value"), max_parts=4, max_len=20)
            return _summarize_source(child.value)
        if isinstance(child, ast.AnnAssign):
            target_name = _reference_summary(child.target).replace(".", "_")
            if target_name and target_name != guarded_name:
                return _clip_summary(target_name.removesuffix("_value"), max_parts=4, max_len=20)
            return _summarize_source(child.value)
        if isinstance(child, ast.If):
            nested = _summarize_precedence_step(child, guarded_name)
            if nested != "default":
                return nested
    return "default"


def _extract_repeated_if_precedence(body: list[ast.stmt]) -> list[str]:
    best_sources: list[str] = []
    for idx, stmt in enumerate(body):
        if not isinstance(stmt, ast.If):
            continue
        guarded = _guarded_name(stmt.test)
        if not guarded:
            continue
        chain: list[ast.If] = [stmt]
        cursor = idx + 1
        while cursor < len(body) and isinstance(body[cursor], ast.If) and _guarded_name(body[cursor].test) == guarded:
            chain.append(body[cursor])
            cursor += 1
        if len(chain) < 2:
            continue

        sources: list[str] = []
        for prev in reversed(body[:idx]):
            if isinstance(prev, ast.Assign):
                if any(_reference_summary(target).replace(".", "_") == guarded for target in prev.targets):
                    sources.append(_summarize_source(prev.value))
                    break
            if isinstance(prev, ast.AnnAssign) and _reference_summary(prev.target).replace(".", "_") == guarded:
                sources.append(_summarize_source(prev.value))
                break

        for item in chain:
            sources.append(_summarize_precedence_step(item, guarded))

        compact = list(dict.fromkeys(source for source in sources if source))
        if len(compact) > len(best_sources):
            best_sources = compact[:4]

    return best_sources


def _extract_behavior_patterns(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    """Extract universal control flow patterns from a function body."""
    patterns: list[str] = []
    body = node.body
    if not body:
        return patterns

    first_stmt = body[0]
    if isinstance(first_stmt, ast.If) and _is_early_exit(first_stmt) and not first_stmt.orelse and len(body) > 1:
        guard_condition = _expr_text(first_stmt.test)
        guard_action = _terminal_action_text(first_stmt.body)
        patterns.append(_pattern_text("GUARD", f"{guard_condition} -> {guard_action}"))

    if_chain: list[ast.If] = []
    cursor = body[0] if isinstance(body[0], ast.If) else None
    while isinstance(cursor, ast.If):
        if_chain.append(cursor)
        cursor = cursor.orelse[0] if len(cursor.orelse) == 1 and isinstance(cursor.orelse[0], ast.If) else None
    if len(if_chain) >= 2:
        branches_with_return = sum(1 for stmt in if_chain if _has_return(stmt))
        if branches_with_return >= 2:
            sources = [_summarize_source(stmt.test) for stmt in if_chain[:4]]
            tail = if_chain[-1].orelse
            if tail:
                tail_action = _find_terminal_action(tail)
                if isinstance(tail_action, ast.Return):
                    sources.append(_summarize_source(tail_action.value))
                elif isinstance(tail_action, ast.Raise):
                    sources.append("raise")
                else:
                    sources.append("default")
            patterns.append(_pattern_text("PRECEDENCE", " -> ".join(list(dict.fromkeys(sources))[:4])))

    repeated_if_sources = _extract_repeated_if_precedence(body)
    if len(repeated_if_sources) >= 2:
        repeated_pattern = _pattern_text("PRECEDENCE", " -> ".join(repeated_if_sources[:4]))
        if not any(pattern.startswith("PRECEDENCE(") for pattern in patterns):
            patterns.append(repeated_pattern)
        else:
            existing_idx = next(
                (index for index, pattern in enumerate(patterns) if pattern.startswith("PRECEDENCE(")),
                -1,
            )
            if existing_idx >= 0 and repeated_pattern.count("->") > patterns[existing_idx].count("->"):
                patterns[existing_idx] = repeated_pattern

    for stmt in body:
        if isinstance(stmt, ast.If) and stmt.orelse and not (len(stmt.orelse) == 1 and isinstance(stmt.orelse[0], ast.If)):
            test_summary = _expr_text(stmt.test, max_len=32)
            true_action = _terminal_action_text(stmt.body, max_len=24)
            false_action = _terminal_action_text(stmt.orelse, max_len=24)
            patterns.append(_pattern_text("BRANCH", f"{test_summary} -> {true_action}, else -> {false_action}"))
            break

    simple_body = [stmt for stmt in body if not isinstance(stmt, ast.Expr)]
    if len(simple_body) <= 1:
        for stmt in body:
            return_value = stmt.value if isinstance(stmt, ast.Return) else None
            if isinstance(return_value, ast.Await):
                return_value = return_value.value
            if isinstance(return_value, ast.Call):
                callee = _reference_summary(return_value.func)
                if callee:
                    patterns.append(f"DELEGATE({callee} -> result)")
                    break

    for stmt in body:
        if isinstance(stmt, (ast.For, ast.AsyncFor, ast.While)):
            target = _extract_accumulator_detail(stmt).replace("_", " ")
            loop_label = _loop_label(stmt)
            raise_name = _loop_raises(stmt)
            detail = f"{loop_label} -> {target}"
            if raise_name:
                detail += f", raises {raise_name}"
            patterns.append(_pattern_text("ACCUMULATE", detail))
            break

    for stmt in ast.walk(node):
        if isinstance(stmt, ast.Call):
            callee = _get_call_name(stmt)
            if callee == "reversed":
                patterns.append("UNWIND(reversed)")
                break

    deduped = list(dict.fromkeys(patterns))
    return deduped[:3]


class SymbolCollector(ast.NodeVisitor):
    def __init__(self, rel_path: str) -> None:
        self.rel_path = rel_path
        self.scope_stack: list[str] = []
        self.symbols: list[SymbolRecord] = []

    def _record(self, node: ast.AST, symbol_type: str, symbol_name: str) -> None:
        qname = ".".join(self.scope_stack + [symbol_name])
        symbol_id = f"symbol:{self.rel_path}:{qname}:{node.lineno}"

        # Extract docstring (first sentence)
        docstring = ""
        raw_doc = ast.get_docstring(node) if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) else None
        if raw_doc:
            # Take first sentence, cap at 120 chars
            first_line = raw_doc.strip().split("\n")[0].strip()
            if ". " in first_line:
                first_line = first_line[:first_line.index(". ") + 1]
            docstring = first_line[:120]

        # Extract signature for functions
        signature = ""
        raises: list[str] = []
        behavior_patterns: list[str] = []
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = []
            for arg in node.args.args:
                args.append(arg.arg)
            if args and args[0] == "self":
                args = args[1:]
            signature = f"({', '.join(args[:5])}{'...' if len(args) > 5 else ''})" if args else "()"
            behavior_patterns = _extract_behavior_patterns(node)
            # Extract raised exceptions
            for child in ast.walk(node):
                if isinstance(child, ast.Raise) and child.exc:
                    if isinstance(child.exc, ast.Call):
                        if isinstance(child.exc.func, ast.Name):
                            raises.append(child.exc.func.id)
                        elif isinstance(child.exc.func, ast.Attribute):
                            raises.append(child.exc.func.attr)
                    elif isinstance(child.exc, ast.Name):
                        raises.append(child.exc.id)
            raises = list(dict.fromkeys(raises))[:5]  # deduplicate, cap at 5

        # For classes, also extract raises from all methods
        if isinstance(node, ast.ClassDef):
            for item in ast.walk(node):
                if isinstance(item, ast.Raise) and item.exc:
                    if isinstance(item.exc, ast.Call):
                        if isinstance(item.exc.func, ast.Name):
                            raises.append(item.exc.func.id)
                        elif isinstance(item.exc.func, ast.Attribute):
                            raises.append(item.exc.func.attr)
                    elif isinstance(item.exc, ast.Name):
                        raises.append(item.exc.id)
            raises = list(dict.fromkeys(raises))[:5]

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
                docstring=docstring,
                signature=signature,
                raises=raises,
                behavior_patterns=behavior_patterns,
            )
        )

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._record(node, "class", node.name)
        # Extract parent class names
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(base.attr)
        # Extract class-level constant attributes (name = literal)
        class_attrs: dict[str, str] = {}
        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name) and not target.id.startswith("_"):
                        # Only capture literals
                        if isinstance(item.value, ast.Constant):
                            val = repr(item.value.value)
                            if len(val) <= 40:
                                class_attrs[target.id] = val
        # Update the last recorded symbol with bases and attrs
        if self.symbols:
            self.symbols[-1].bases = bases
            self.symbols[-1].class_attrs = class_attrs
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


def _decorator_name(decorator: ast.AST) -> str:
    if isinstance(decorator, ast.Call):
        return _reference_summary(decorator.func)
    return _reference_summary(decorator)


def _call_keyword(call: ast.Call, key: str) -> ast.AST | None:
    for keyword in call.keywords:
        if keyword.arg == key:
            return keyword.value
    return None


def _resolve_symbol_candidates(name_to_symbol: dict[str, list[str]], raw_name: str) -> list[str]:
    if not raw_name:
        return []
    candidates = name_to_symbol.get(raw_name, [])
    if candidates:
        return candidates
    tail = raw_name.rsplit(".", 1)[-1]
    return name_to_symbol.get(tail, [])


def extract_python_nodes_edges(repo_root: Path) -> tuple[list[Node], list[Edge]]:
    nodes: list[Node] = []
    edges: list[Edge] = []

    for file_path in _iter_python_files(repo_root):
        try:
            text = file_path.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            continue
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
                    "imports": [],  # populated after AST parse
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

        # Extract file-level imports for Approach 6 enrichment
        file_imports: list[str] = []
        # Build imported_name -> module mapping for uses: extraction
        imported_names: dict[str, str] = {}  # local_name -> source_module
        _STDLIB_SKIP = ("os", "sys", "typing", "collections", "abc",
                       "functools", "contextlib", "dataclasses",
                       "pathlib", "json", "re", "time", "datetime")
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    mod_name = alias.name.split(".")[0]
                    if mod_name not in _STDLIB_SKIP:
                        file_imports.append(alias.name)
                        local = alias.asname or alias.name
                        imported_names[local] = alias.name
            elif isinstance(node, ast.ImportFrom):
                if node.module and not node.module.startswith("_"):
                    mod_name = node.module.split(".")[0]
                    if mod_name not in _STDLIB_SKIP:
                        file_imports.append(node.module)
                        if node.names:
                            for alias in node.names:
                                if alias.name != "*":
                                    local = alias.asname or alias.name
                                    imported_names[local] = node.module
        # Deduplicate and cap
        file_imports = list(dict.fromkeys(file_imports))[:10]

        # Update module node's imports
        for n in nodes:
            if n.node_id == module_node_id:
                n.semantic_contract["imports"] = file_imports
                break

        collector = SymbolCollector(rel_path)
        collector.visit(tree)

        # Extract uses: for each function/method — find calls to imported names
        for symbol in collector.symbols:
            if symbol.symbol_type not in ("function", "async_function"):
                continue
            # Find the AST node for this symbol
            for ast_node in ast.walk(tree):
                if (isinstance(ast_node, (ast.FunctionDef, ast.AsyncFunctionDef))
                        and ast_node.name == symbol.symbol_name.rsplit(".", 1)[-1]
                        and ast_node.lineno == symbol.line_start):
                    uses: list[str] = []
                    for child in ast.walk(ast_node):
                        if not isinstance(child, ast.Call):
                            continue
                        callee = ""
                        if isinstance(child.func, ast.Name):
                            callee = child.func.id
                        if callee and callee in imported_names and callee[0].isupper():
                            # Only track PascalCase names (class instantiations)
                            mod = imported_names[callee]
                            uses.append(f"{callee} ({mod})")
                    symbol.uses = list(dict.fromkeys(uses))[:4]  # dedupe, cap
                    break

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
                        "purpose": symbol.docstring if symbol.docstring else f"{symbol.symbol_type} {symbol.symbol_name}",
                        "language": "python",
                        "symbol_name": symbol.symbol_name,
                        "symbol_type": symbol.symbol_type,
                        "signature": symbol.signature,
                        "bases": symbol.bases,
                        "class_attrs": symbol.class_attrs,
                        "raises": symbol.raises,
                        "uses": symbol.uses,
                        "behavior_patterns": symbol.behavior_patterns,
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

        # Build class-to-method containment edges
        class_to_methods: dict[str, list[str]] = {}
        for symbol in collector.symbols:
            if symbol.symbol_type == "class":
                class_to_methods[symbol.symbol_name] = []
        for symbol in collector.symbols:
            if symbol.symbol_type in ("function", "async_function"):
                # Check if this symbol is a method (qualified name contains a class)
                parts = symbol.symbol_name.split(".")
                if len(parts) >= 2:
                    parent_class = parts[-2]
                    if parent_class in class_to_methods:
                        class_ids = name_to_symbol.get(parent_class, [])
                        method_ids = name_to_symbol.get(symbol.symbol_name, [])
                        if len(class_ids) == 1 and len(method_ids) == 1:
                            edges.append(
                                Edge(
                                    edge_id=f"contains:{class_ids[0]}:{method_ids[0]}",
                                    edge_type="contains",
                                    from_node=class_ids[0],
                                    to_node=method_ids[0],
                                    evidence={"rel": "class_containment"},
                                )
                            )

        route_nodes_to_add: list[Node] = []
        route_edges_to_add: list[Edge] = []

        class_nodes = {
            symbol.line_start: symbol
            for symbol in collector.symbols
            if symbol.symbol_type == "class"
        }
        function_nodes = {
            symbol.line_start: symbol
            for symbol in collector.symbols
            if symbol.symbol_type in ("function", "async_function")
        }

        # Framework-aware extraction: Django models, routes, settings, Celery.
        for ast_node in ast.walk(tree):
            if isinstance(ast_node, ast.ClassDef):
                class_symbol = class_nodes.get(ast_node.lineno)
                if not class_symbol:
                    continue
                class_ids = name_to_symbol.get(class_symbol.symbol_name, [])
                if len(class_ids) != 1:
                    continue
                class_id = class_ids[0]

                for item in ast_node.body:
                    value = None
                    field_name = ""
                    if isinstance(item, ast.Assign) and item.targets and isinstance(item.targets[0], ast.Name):
                        field_name = item.targets[0].id
                        value = item.value
                    elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                        field_name = item.target.id
                        value = item.value
                    if not isinstance(value, ast.Call):
                        continue

                    relation_name = _get_call_name(value.func)
                    if relation_name not in {"ForeignKey", "ManyToManyField", "OneToOneField"}:
                        continue

                    target_node = value.args[0] if value.args else _call_keyword(value, "to")
                    target_name = _reference_summary(target_node).strip("'\"")
                    for related_id in _resolve_symbol_candidates(name_to_symbol, target_name):
                        if related_id == class_id:
                            continue
                        route_edges_to_add.append(
                            Edge(
                                edge_id=f"relates:{class_id}:{related_id}:{field_name or relation_name}:{getattr(value, 'lineno', 0)}",
                                edge_type="relates",
                                from_node=class_id,
                                to_node=related_id,
                                evidence={
                                    "rel": relation_name,
                                    "field": field_name,
                                    "line": getattr(value, "lineno", 0),
                                },
                            )
                        )

            elif isinstance(ast_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_symbol = function_nodes.get(ast_node.lineno)
                if not func_symbol:
                    continue
                func_ids = _resolve_symbol_candidates(name_to_symbol, func_symbol.symbol_name)
                if len(func_ids) != 1:
                    continue
                func_id = func_ids[0]
                for decorator in ast_node.decorator_list:
                    decorator_name = _decorator_name(decorator)
                    if decorator_name.rsplit(".", 1)[-1] in {"task", "shared_task"}:
                        route_edges_to_add.append(
                            Edge(
                                edge_id=f"task:{module_node_id}:{func_id}:{getattr(decorator, 'lineno', ast_node.lineno)}",
                                edge_type="task",
                                from_node=module_node_id,
                                to_node=func_id,
                                evidence={
                                    "rel": "celery_task",
                                    "decorator": decorator_name,
                                    "line": getattr(decorator, "lineno", ast_node.lineno),
                                },
                            )
                        )
                        node_obj = next((n for n in nodes if n.node_id == func_id), None)
                        if node_obj:
                            decorators = node_obj.semantic_contract.get("decorators", [])
                            if decorator_name not in decorators:
                                decorators.append(decorator_name)
                            node_obj.semantic_contract["decorators"] = decorators

            elif isinstance(ast_node, ast.Call):
                route_kind = _get_call_name(ast_node.func)
                if route_kind not in {"path", "re_path"}:
                    continue

                pattern_node = ast_node.args[0] if ast_node.args else None
                target_node = ast_node.args[1] if len(ast_node.args) > 1 else _call_keyword(ast_node, "view")
                route_pattern = _reference_summary(pattern_node).strip("'\"") or route_kind
                target_name = _reference_summary(target_node)
                route_symbol = f"{route_kind}:{route_pattern}"
                route_id = f"route:{rel_path}:{route_pattern}:{getattr(ast_node, 'lineno', 0)}"
                purpose = f"Django route {route_pattern} -> {target_name or 'view'}"
                route_nodes_to_add.append(
                    _make_aux_node(
                        repo_root,
                        file_path,
                        node_id=route_id,
                        node_type="route",
                        symbol_name=route_symbol,
                        purpose=purpose,
                        confidence=0.9,
                        extra_contract={
                            "route_pattern": route_pattern,
                            "route_target": target_name,
                            "framework": "django",
                        },
                        snippet_text=text,
                    )
                )
                route_edges_to_add.append(
                    Edge(
                        edge_id=f"contains:{module_node_id}:{route_id}",
                        edge_type="contains",
                        from_node=module_node_id,
                        to_node=route_id,
                        evidence={"rel": "django_urlpattern"},
                    )
                )
                for target_id in _resolve_symbol_candidates(name_to_symbol, target_name):
                    route_edges_to_add.append(
                        Edge(
                            edge_id=f"routes:{route_id}:{target_id}:{getattr(ast_node, 'lineno', 0)}",
                            edge_type="routes",
                            from_node=route_id,
                            to_node=target_id,
                            evidence={
                                "rel": route_kind,
                                "pattern": route_pattern,
                                "line": getattr(ast_node, "lineno", 0),
                            },
                        )
                    )

        # Attach settings references captured in settings.py/config.py modules.
        if file_path.name in {"settings.py", "config.py"}:
            _, settings_refs = _parse_python_config_entries(text)
            if settings_refs:
                for node_obj in nodes:
                    if node_obj.node_id == module_node_id:
                        node_obj.semantic_contract["django_settings_refs"] = settings_refs
                        break
                for setting_name, refs in settings_refs.items():
                    for ref in refs:
                        for target_id in _resolve_symbol_candidates(name_to_symbol, ref):
                            route_edges_to_add.append(
                                Edge(
                                    edge_id=f"configures:{module_node_id}:{target_id}:{setting_name}",
                                    edge_type="configures",
                                    from_node=module_node_id,
                                    to_node=target_id,
                                    evidence={"rel": setting_name},
                                )
                            )

        nodes.extend(route_nodes_to_add)
        edges.extend(route_edges_to_add)

        # Detect call edges: walk ALL node types (functions, async functions, AND classes)
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue

            # Determine the caller node ID
            caller_name = node.name
            caller_candidates = name_to_symbol.get(caller_name, [])

            # For methods inside classes, try qualified name
            if len(caller_candidates) != 1 and isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Try to find parent class scope from collector
                for sym in collector.symbols:
                    if sym.symbol_name.endswith("." + caller_name) and sym.line_start == node.lineno:
                        caller_candidates = name_to_symbol.get(sym.symbol_name, [])
                        break

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

                # Try exact match first
                callee_candidates = name_to_symbol.get(callee_name, [])

                # If multiple candidates, try to disambiguate by file
                if len(callee_candidates) > 1:
                    same_file = [c for c in callee_candidates if rel_path in c]
                    if len(same_file) == 1:
                        callee_candidates = same_file

                if len(callee_candidates) != 1:
                    continue
                callee_id = callee_candidates[0]

                # Avoid self-edges
                if caller_id == callee_id:
                    continue

                edge_id = (
                    f"calls:{caller_id}:{callee_id}:"
                    f"{getattr(child, 'lineno', 0)}"
                )
                edges.append(
                    Edge(
                        edge_id=edge_id,
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

    config_nodes, config_edges = _extract_config_context(repo_root)
    doc_nodes, doc_edges = _extract_doc_context(repo_root)
    nodes.extend(config_nodes)
    nodes.extend(doc_nodes)
    edges.extend(config_edges)
    edges.extend(doc_edges)

    node_map = {node.node_id: node for node in nodes}

    # Link extracted config/doc context to graph symbols when possible.
    module_nodes = [node for node in nodes if node.node_type == "module"]
    symbol_lookup: dict[str, list[str]] = {}
    for node in nodes:
        symbol_lookup.setdefault(node.semantic_contract.get("symbol_name", node.node_id), []).append(node.node_id)

    for node in config_nodes:
        settings_refs = node.semantic_contract.get("settings_refs", {})
        for setting_name, refs in settings_refs.items():
            for ref in refs:
                linked = False
                for module in module_nodes:
                    mod_symbol = module.semantic_contract.get("symbol_name", "")
                    mod_path = module.source_anchor.file_path
                    mod_stem = Path(mod_path).stem
                    if ref in mod_symbol or ref in mod_path or ref.rsplit(".", 1)[-1] == mod_stem:
                        edge_id = f"configures:{node.node_id}:{module.node_id}:{setting_name}"
                        edges.append(
                            Edge(
                                edge_id=edge_id,
                                edge_type="configures",
                                from_node=node.node_id,
                                to_node=module.node_id,
                                evidence={"rel": setting_name, "ref": ref},
                            )
                        )
                        linked = True
                if linked:
                    continue
                for target_id in _resolve_symbol_candidates(symbol_lookup, ref):
                    edges.append(
                        Edge(
                            edge_id=f"configures:{node.node_id}:{target_id}:{setting_name}",
                            edge_type="configures",
                            from_node=node.node_id,
                            to_node=target_id,
                            evidence={"rel": setting_name, "ref": ref},
                        )
                    )

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
