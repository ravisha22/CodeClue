from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Any

from .extractor import (
    _find_repo_files,
    _parse_package_json,
    _parse_pyproject,
    _parse_python_config_entries,
    _summarize_doc_text,
)


_ROOT_DOC_FILES = ("README.md", "CONTRIBUTING.md", "AGENTS.md")
_SETTINGS_FILES = ("settings.py", "config.py", "configuration.py")
_ROUTE_FILES = ("urls.py",)
_SCHEMA_FILES = ("schema.py", "schema.prisma")
_INFRA_FILES = ("docker-compose.yml", "Dockerfile", "package.json", "pyproject.toml", "go.mod")
_MODEL_RELATIONS = {"ForeignKey", "ManyToManyField", "OneToOneField"}


def default_context_output_path(output_path: Path) -> Path:
    base = output_path.with_suffix("") if output_path.suffix else output_path
    return base.with_name(f"{base.name}.codeclue-context")


def extract_deep_context(repo_root: Path) -> dict[str, Any]:
    files = []
    files.extend(_extract_root_docs(repo_root))
    files.extend(_extract_python_configs(repo_root))
    files.extend(_extract_model_files(repo_root))
    files.extend(_extract_route_files(repo_root))
    files.extend(_extract_schema_files(repo_root))
    files.extend(_extract_infra_files(repo_root))
    files.sort(key=lambda item: (item["category"], item["path"]))
    return {
        "version": 1,
        "strategy": "deterministic-deep-context",
        "repo_root": str(repo_root),
        "files": files,
    }


def _extract_root_docs(repo_root: Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for name in _ROOT_DOC_FILES:
        path = repo_root / name
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        snippet = "\n".join(text.splitlines()[:200])
        headings, summary_lines = _summarize_doc_text(snippet, max_headings=8, max_lines=6)
        items.append({
            "path": name,
            "category": "doc",
            "summary": {
                "headings": headings,
                "summary_lines": summary_lines,
            },
        })
    return items


def _extract_python_configs(repo_root: Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for path in _find_repo_files(repo_root, list(_SETTINGS_FILES), max_matches_per_name=4):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        entries, settings_refs = _parse_python_config_entries(text)
        summary = {"entries": entries}
        if settings_refs:
            summary["settings_refs"] = settings_refs
        items.append({
            "path": path.relative_to(repo_root).as_posix(),
            "category": "config",
            "summary": summary,
        })
    return items


def _extract_model_files(repo_root: Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    candidates = []
    for path in _find_repo_files(repo_root, ["models.py"], max_matches_per_name=5):
        candidates.append(path)
    for path in _find_repo_files(repo_root, ["__init__.py"], max_matches_per_name=5):
        if path.parent.name == "models":
            candidates.append(path)
    seen: set[Path] = set()
    for path in candidates:
        if path in seen:
            continue
        seen.add(path)
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        summary = _summarize_model_file(text)
        if not any(summary.values()):
            continue
        items.append({
            "path": path.relative_to(repo_root).as_posix(),
            "category": "model",
            "summary": summary,
        })
    return items


def _summarize_model_file(text: str) -> dict[str, Any]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return {}

    classes: list[str] = []
    relations: list[str] = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        bases = [_expr_text(base) for base in node.bases]
        if bases and any("model" in base.lower() for base in bases):
            classes.append(node.name)
        for item in node.body:
            field_name = ""
            value: ast.AST | None = None
            if isinstance(item, ast.Assign) and item.targets and isinstance(item.targets[0], ast.Name):
                field_name = item.targets[0].id
                value = item.value
            elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                field_name = item.target.id
                value = item.value
            if not isinstance(value, ast.Call):
                continue
            relation_name = _call_name(value.func).rsplit(".", 1)[-1]
            if relation_name not in _MODEL_RELATIONS:
                continue
            target_node = value.args[0] if value.args else _keyword_arg(value, "to")
            target_name = _expr_text(target_node).strip("'\"")
            relation = f"{node.name}.{field_name}->{target_name or '?'} ({relation_name})"
            relations.append(relation)

    return {
        "classes": classes[:12],
        "relations": relations[:20],
    }


def _extract_route_files(repo_root: Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for path in _find_repo_files(repo_root, list(_ROUTE_FILES), max_matches_per_name=5):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        summary = _summarize_route_file(text)
        if not any(summary.values()):
            continue
        items.append({
            "path": path.relative_to(repo_root).as_posix(),
            "category": "route",
            "summary": summary,
        })
    return items


def _summarize_route_file(text: str) -> dict[str, Any]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return {}

    routes: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        call_name = _call_name(node.func).rsplit(".", 1)[-1]
        if call_name in {"path", "re_path", "url"}:
            route_pattern = _expr_text(node.args[0]) if node.args else "?"
            target = _expr_text(node.args[1]) if len(node.args) > 1 else "?"
            routes.append(f"{route_pattern} -> {target}")
        elif call_name == "register":
            prefix = _expr_text(node.args[0]) if node.args else "?"
            target = _expr_text(node.args[1]) if len(node.args) > 1 else "?"
            routes.append(f"{prefix} -> {target}")
    return {"routes": routes[:20]}


def _extract_schema_files(repo_root: Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for path in _find_repo_files(repo_root, list(_SCHEMA_FILES), max_matches_per_name=4):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        summary = (
            _summarize_prisma_schema(text)
            if path.name.lower() == "schema.prisma"
            else _summarize_python_schema(text)
        )
        if not any(summary.values()):
            continue
        items.append({
            "path": path.relative_to(repo_root).as_posix(),
            "category": "schema",
            "summary": summary,
        })
    return items


def _summarize_prisma_schema(text: str) -> dict[str, Any]:
    models = re.findall(r"(?m)^\s*model\s+([A-Za-z_]\w*)\s*\{", text)
    enums = re.findall(r"(?m)^\s*enum\s+([A-Za-z_]\w*)\s*\{", text)
    return {
        "models": models[:20],
        "enums": enums[:20],
    }


def _summarize_python_schema(text: str) -> dict[str, Any]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return {}
    classes = [node.name for node in tree.body if isinstance(node, ast.ClassDef)]
    assignments = [
        target.id
        for node in tree.body
        if isinstance(node, ast.Assign)
        for target in node.targets
        if isinstance(target, ast.Name) and "schema" in target.id.lower()
    ]
    return {
        "classes": classes[:20],
        "schema_symbols": assignments[:10],
    }


def _extract_infra_files(repo_root: Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for name in _INFRA_FILES:
        path = repo_root / name
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        summary = _summarize_infra_file(path.name, text)
        if not any(summary.values()):
            continue
        items.append({
            "path": name,
            "category": "infra",
            "summary": summary,
        })
    return items


def _summarize_infra_file(name: str, text: str) -> dict[str, Any]:
    lowered = name.lower()
    if lowered == "package.json":
        dependencies, scripts = _parse_package_json(text)
        return {"dependencies": dependencies, "scripts": scripts}
    if lowered == "pyproject.toml":
        dependencies, scripts = _parse_pyproject(text)
        return {"dependencies": dependencies, "scripts": scripts}
    if lowered == "go.mod":
        module_match = re.search(r"(?m)^\s*module\s+(.+)$", text)
        requires = re.findall(r"(?m)^\s*require\s+([A-Za-z0-9./_-]+)", text)
        if not requires:
            block = re.search(r"(?ms)^\s*require\s*\((.*?)^\s*\)", text)
            if block:
                requires = re.findall(r"(?m)^\s*([A-Za-z0-9./_-]+)\s+v", block.group(1))
        return {
            "module": module_match.group(1).strip() if module_match else "",
            "dependencies": requires[:20],
        }
    if lowered == "dockerfile":
        return {
            "instructions": [
                line.strip()
                for line in text.splitlines()
                if line.strip() and re.match(r"^(FROM|RUN|CMD|ENTRYPOINT|EXPOSE|WORKDIR)\b", line.strip(), re.I)
            ][:20],
        }
    if lowered == "docker-compose.yml":
        services = re.findall(r"(?m)^\s{2}([A-Za-z0-9_.-]+):\s*$", text)
        return {"services": services[:20]}
    return {}


def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = _call_name(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return ""


def _keyword_arg(node: ast.Call, name: str) -> ast.AST | None:
    for keyword in node.keywords:
        if keyword.arg == name:
            return keyword.value
    return None


def _expr_text(node: ast.AST | None) -> str:
    if node is None:
        return ""
    try:
        return ast.unparse(node)
    except Exception:
        return ""
