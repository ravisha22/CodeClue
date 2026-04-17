"""CodeClue MCP server and workspace-aware control surface."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from codeclue_research.clue_view_mrlf import generate_detail_store, render_mrlf, write_detail_store
from codeclue_research.extractor import extract_graph
from codeclue_research.io import load_data, load_graph, save_data, save_graph
from codeclue_research.models import CanonicalClueGraph
from codeclue_research.operation_projection import project_operation

from .budget import DEFAULT_CONFIDENCE_THRESHOLD
from .state import RepoInfo, SessionState
from .tools import (
    check_freshness,
    code_slice,
    expand_projection,
    fetch_contract,
    get_clue,
    get_drill_targets,
    load_detail_records,
    resolve_dependency,
)
from .tracer import InvocationTracer, hash_output


_PUBLIC_TOOL_DEFINITIONS = [
    {
        "name": "code_slice",
        "description": "Fetch raw source for a file range or resolve a symbol to its source.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Relative path to source file within the repository"},
                "start_line": {"type": "integer", "description": "First line to fetch (1-based)"},
                "end_line": {"type": "integer", "description": "Last line to fetch (1-based, inclusive)"},
                "symbol_name": {"type": "string", "description": "Optional symbol to resolve via the detail store"},
            },
        },
    },
    {
        "name": "resolve_dependency",
        "description": "Expand a compressed edge to its full dependency subgraph via BFS from a node.",
        "input_schema": {
            "type": "object",
            "properties": {
                "node_id": {"type": "string", "description": "The node_id to expand from"},
                "depth": {"type": "integer", "description": "BFS depth (default 2)", "default": 2},
            },
            "required": ["node_id"],
        },
    },
    {
        "name": "check_freshness",
        "description": "Verify whether a clue module is stale relative to the current source.",
        "input_schema": {
            "type": "object",
            "properties": {
                "module_id": {"type": "string", "description": "The module node_id to check"},
            },
            "required": ["module_id"],
        },
    },
    {
        "name": "expand_projection",
        "description": "Widen the projected subgraph around a seed node by additional hops.",
        "input_schema": {
            "type": "object",
            "properties": {
                "node_id": {"type": "string", "description": "The seed node_id"},
                "additional_hops": {"type": "integer", "description": "Number of additional BFS hops", "default": 1},
                "edge_types": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Edge types to follow (default: contains, calls)",
                },
            },
            "required": ["node_id"],
        },
    },
    {
        "name": "fetch_contract",
        "description": "Retrieve the semantic contract for a node, enriched from the detail store when available.",
        "input_schema": {
            "type": "object",
            "properties": {
                "node_id": {"type": "string", "description": "The node_id to fetch the contract for"},
            },
            "required": ["node_id"],
        },
    },
    {
        "name": "get_clue",
        "description": "Return a pre-generated File 1 clue or render one for a question.",
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "Optional question to render against the active graph"},
            },
        },
    },
    {
        "name": "get_drill_targets",
        "description": "Parse the GAPS section from the active clue and return drill targets.",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
]


def _default_question(repo_name: str) -> str:
    return f"What are the key structures and behaviors in {repo_name}?"


def _detect_language(repo_path: Path) -> str:
    counts = {"python": 0, "typescript": 0, "go": 0}
    for entry in repo_path.rglob("*"):
        if entry.name == ".git":
            continue
        if not entry.is_file():
            continue
        suffix = entry.suffix.lower()
        if suffix == ".py":
            counts["python"] += 1
        elif suffix in {".ts", ".tsx", ".js", ".jsx"}:
            counts["typescript"] += 1
        elif suffix == ".go":
            counts["go"] += 1
    language = max(counts, key=counts.get)
    return language if counts[language] else "unknown"


def _is_git_repo(path: Path) -> bool:
    return (path / ".git").exists()


def _find_clue_artifacts(clue_dir: Path) -> tuple[Path | None, Path | None, Path | None]:
    clue_path = next(iter(sorted(clue_dir.glob("*.codeclue"))), None)
    detail_path = next(
        iter(sorted(list(clue_dir.glob("*.codeclue-detail")) + list(clue_dir.glob("*.codeclue-detail.jsonl")))),
        None,
    )
    graph_path = clue_dir / "graph.json"
    if not graph_path.exists():
        graph_path = None
    return clue_path, detail_path, graph_path


def _repo_clue_dir(repo_path: Path) -> Path:
    return repo_path / ".codeclue"


class CodeClueServer:
    """Workspace-aware server that can expose MRLF clues and graph drill-down tools."""

    def __init__(
        self,
        graph: CanonicalClueGraph | None = None,
        repo_root: str | None = None,
        *,
        graph_path: str | None = None,
        clue_dir: str | None = None,
        workspace_root: str | None = None,
        confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
        tracer: InvocationTracer | None = None,
    ) -> None:
        self.state = SessionState(
            workspace_root=workspace_root,
            confidence_threshold=confidence_threshold,
        )
        self._graph = graph
        self._repo_root = repo_root
        self._graph_path = graph_path
        self._clue_dir = clue_dir
        self._tracer = tracer

        if graph is not None:
            self.state.active_graph = graph
        if repo_root is not None:
            self.state.active_repo = repo_root
        if graph_path is not None:
            self.state.active_graph_path = graph_path
        if clue_dir is not None:
            self._load_clue_dir(Path(clue_dir), repo_root=repo_root, load_graph_if_present=graph is None)

    def list_tools(self) -> list[dict[str, Any]]:
        return list(_PUBLIC_TOOL_DEFINITIONS)

    def _ensure_tracer(self) -> InvocationTracer | None:
        if self._tracer is not None:
            return self._tracer
        base_dir = self.state.active_clue_dir or (
            str(_repo_clue_dir(Path(self._repo_root))) if self._repo_root else None
        )
        if not base_dir:
            return None
        self._tracer = InvocationTracer(Path(base_dir) / "traces")
        return self._tracer

    def _load_clue_dir(
        self,
        clue_dir: Path,
        *,
        repo_root: str | None = None,
        load_graph_if_present: bool = True,
    ) -> None:
        clue_path, detail_path, graph_path = _find_clue_artifacts(clue_dir)
        if clue_path is None:
            raise FileNotFoundError(f"No .codeclue file found in {clue_dir}")
        clue_text = clue_path.read_text(encoding="utf-8")
        detail_records = load_detail_records(detail_path) if detail_path else []
        graph = self._graph
        if load_graph_if_present and graph_path is not None:
            graph = load_graph(graph_path)

        self.state.active_clue_dir = str(clue_dir)
        self.state.active_clue_path = str(clue_path)
        self.state.active_detail_path = str(detail_path) if detail_path else None
        self.state.active_clue_text = clue_text
        self.state.active_detail_records = detail_records
        self.state.active_graph_path = str(graph_path) if graph_path else self.state.active_graph_path
        if graph is not None:
            self.state.active_graph = graph
            self._graph = graph
        if repo_root is not None:
            self.state.active_repo = repo_root
            self._repo_root = repo_root
        self._clue_dir = str(clue_dir)

    def swap_graph(
        self,
        *,
        graph: CanonicalClueGraph,
        repo_root: str,
        graph_path: str | None = None,
        clue_dir: str | None = None,
        clue_path: str | None = None,
        detail_path: str | None = None,
        clue_text: str | None = None,
        detail_records: list[dict[str, Any]] | None = None,
    ) -> None:
        if graph is None:
            raise ValueError("graph cannot be None")
        self._graph = graph
        self._repo_root = repo_root
        self._graph_path = graph_path
        self._clue_dir = clue_dir or self._clue_dir
        self.state.active_graph = graph
        self.state.active_repo = repo_root
        self.state.active_graph_path = graph_path
        if clue_dir is not None:
            self.state.active_clue_dir = clue_dir
        if clue_path is not None:
            self.state.active_clue_path = clue_path
        if detail_path is not None:
            self.state.active_detail_path = detail_path
        if clue_text is not None:
            self.state.active_clue_text = clue_text
        if detail_records is not None:
            self.state.active_detail_records = detail_records

    def _graph_required_result(self, tool_name: str) -> dict[str, Any]:
        return {
            "status": "error",
            "message": f"No clue loaded for {tool_name}. Generate or select a repository clue first.",
        }

    def _log_tool_call(self, name: str, arguments: dict[str, Any], result: dict[str, Any]) -> None:
        tracer = self._ensure_tracer()
        if tracer is None or result.get("status") != "ok":
            return
        source_anchor = (
            result.get("node_id")
            or result.get("module_id")
            or result.get("seed_node")
            or result.get("symbol_name")
            or result.get("file_path")
            or self.state.active_clue_path
            or ""
        )
        tracer.log(
            tool=name,
            args=arguments,
            output_hash=hash_output(result),
            source_anchor=str(source_anchor),
            confidence_trigger=float(self.state.confidence_threshold),
            session_id=self.state.active_repo or "session",
            confidence=float(result.get("confidence", 0.0)),
            warning=result.get("warning"),
        )

    def _repo_within_workspace(self, repo_path: Path) -> bool:
        if not self.state.workspace_root:
            return True
        workspace = Path(self.state.workspace_root).resolve()
        try:
            repo_path.resolve().relative_to(workspace)
        except ValueError:
            return False
        return True

    def _discover_repos(self) -> dict[str, Any]:
        if not self.state.workspace_root:
            return {"status": "error", "message": "workspace_root is required"}
        workspace = Path(self.state.workspace_root)
        repos: list[RepoInfo] = []
        for child in sorted(workspace.iterdir()):
            if not child.is_dir() or not _is_git_repo(child):
                continue
            clue_dir = _repo_clue_dir(child)
            clue_path, detail_path, graph_path = _find_clue_artifacts(clue_dir) if clue_dir.exists() else (None, None, None)
            repos.append(
                RepoInfo(
                    repo_name=child.name,
                    repo_path=str(child),
                    language_hint=_detect_language(child),
                    has_existing_clue=bool(clue_path or detail_path or graph_path),
                    clue_dir=str(clue_dir) if clue_dir.exists() else None,
                    clue_path=str(clue_path) if clue_path else None,
                    detail_path=str(detail_path) if detail_path else None,
                )
            )
        self.state.discovered_repos = repos
        return {"status": "ok", "repos": [repo.__dict__ for repo in repos]}

    def _get_repo_status(self, repo_path: str | None = None) -> dict[str, Any]:
        raw_path = repo_path or self.state.active_repo
        if not raw_path:
            return {"status": "error", "message": "repo_path or active_repo is required"}
        target = Path(raw_path)
        clue_dir = _repo_clue_dir(target)
        clue_path, detail_path, graph_path = _find_clue_artifacts(clue_dir) if clue_dir.exists() else (None, None, None)
        return {
            "status": "ok",
            "repo_name": target.name,
            "repo_path": str(target),
            "language": _detect_language(target),
            "clue_exists": bool(clue_path or detail_path or graph_path),
            "clue_dir": str(clue_dir),
        }

    def _generate_clue(self, arguments: dict[str, Any]) -> dict[str, Any]:
        repo_path = Path(arguments["repo_path"])
        language = arguments.get("language", "auto")
        allow_no_git = bool(arguments.get("allow_no_git", False))
        if not repo_path.exists():
            return {"status": "error", "message": f"Repository path not found: {repo_path}"}
        if not self._repo_within_workspace(repo_path):
            return {"status": "error", "message": "repo_path must be inside workspace_root"}
        if not allow_no_git and not _is_git_repo(repo_path):
            return {"status": "error", "message": "Repository must be a git repo unless allow_no_git is set"}

        previous_graph = self._graph
        try:
            graph = extract_graph(repo_path, language=language)
        except Exception as exc:
            self._graph = previous_graph
            if previous_graph is not None:
                self.state.active_graph = previous_graph
            return {"status": "error", "message": str(exc)}

        if not graph.nodes:
            self._graph = previous_graph
            if previous_graph is not None:
                self.state.active_graph = previous_graph
            return {"status": "error", "message": "Extraction produced no graph nodes"}

        clue_dir = _repo_clue_dir(repo_path)
        clue_dir.mkdir(parents=True, exist_ok=True)
        graph_output_path = Path(arguments.get("output_path") or (clue_dir / "graph.json"))
        question = arguments.get("question") or _default_question(repo_path.name)
        clue_text = render_mrlf(graph, question, repo_root=repo_path)
        clue_path = clue_dir / f"{repo_path.name}.codeclue"
        detail_path = clue_dir / f"{repo_path.name}.codeclue-detail.jsonl"
        detail_records = generate_detail_store(graph, repo_root=repo_path)

        save_graph(graph_output_path, graph)
        clue_path.write_text(clue_text, encoding="utf-8")
        write_detail_store(detail_records, detail_path)

        self.swap_graph(
            graph=graph,
            repo_root=str(repo_path),
            graph_path=str(graph_output_path),
            clue_dir=str(clue_dir),
            clue_path=str(clue_path),
            detail_path=str(detail_path),
            clue_text=clue_text,
            detail_records=detail_records,
        )
        return {
            "status": "ok",
            "repo_path": str(repo_path),
            "graph_path": str(graph_output_path),
            "clue_path": str(clue_path),
            "detail_path": str(detail_path),
            "node_count": len(graph.nodes),
            "edge_count": len(graph.edges),
        }

    def _select_repo(self, repo_path: str) -> dict[str, Any]:
        repo = Path(repo_path)
        self.state.active_repo = str(repo)
        clue_dir = _repo_clue_dir(repo)
        if not clue_dir.exists():
            return {"status": "no_clue", "repo_path": str(repo), "clue_loaded": False}
        try:
            self._load_clue_dir(clue_dir, repo_root=str(repo))
        except FileNotFoundError:
            return {"status": "no_clue", "repo_path": str(repo), "clue_loaded": False}
        return {"status": "ok", "repo_path": str(repo), "clue_loaded": True}

    def _generate_projection(self, operation_family: str, prompt_profile: dict[str, Any] | None = None) -> dict[str, Any]:
        if self._graph is None:
            return self._graph_required_result("generate_projection")
        clue_dir = Path(self.state.active_clue_dir or _repo_clue_dir(Path(self._repo_root or ".")))
        trace = project_operation(
            graph=self._graph,
            operation_family=operation_family,
            prompt_profile=prompt_profile or {},
        )
        projection_path = clue_dir / f"projection-{operation_family}.json"
        save_data(projection_path, trace)
        self.state.active_projection_path = str(projection_path)
        confidence_block = trace.get("confidence", {})
        return {
            "status": "ok",
            "projection_path": str(projection_path),
            "node_count": trace["stats"]["projected_node_count"],
            "edge_count": trace["stats"]["projected_edge_count"],
            "confidence_overall": confidence_block.get("confidence_overall"),
        }

    def _get_projection_summary(self, projection_path: str | None = None) -> dict[str, Any]:
        raw_path = projection_path or self.state.active_projection_path
        if not raw_path:
            return {"status": "error", "message": "projection_path is required"}
        target = Path(raw_path)
        trace = load_data(target)
        confidence_block = trace.get("confidence", {})
        return {
            "status": "ok",
            "projection_path": str(target),
            "operation_family": trace.get("operation_family"),
            "node_count": trace.get("stats", {}).get("projected_node_count"),
            "edge_count": trace.get("stats", {}).get("projected_edge_count"),
            "confidence_overall": confidence_block.get("confidence_overall"),
        }

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        threshold = self.state.confidence_threshold

        if name == "discover_repos":
            result = self._discover_repos()
        elif name == "get_repo_status":
            result = self._get_repo_status(arguments.get("repo_path"))
        elif name == "generate_clue":
            result = self._generate_clue(arguments)
        elif name == "select_repo":
            result = self._select_repo(arguments["repo_path"])
        elif name == "generate_projection":
            result = self._generate_projection(arguments["operation_family"], arguments.get("prompt_profile"))
        elif name == "get_projection_summary":
            result = self._get_projection_summary(arguments.get("projection_path"))
        elif name == "code_slice":
            if not self._repo_root:
                result = {"status": "error", "message": "No repository root configured for code_slice"}
            else:
                result = code_slice(
                    repo_root=self._repo_root,
                    file_path=arguments.get("file_path"),
                    start_line=arguments.get("start_line"),
                    end_line=arguments.get("end_line"),
                    symbol_name=arguments.get("symbol_name"),
                    graph=self._graph,
                    detail_records=self.state.active_detail_records,
                    confidence_threshold=threshold,
                )
        elif name == "resolve_dependency":
            if self._graph is None:
                result = self._graph_required_result(name)
            else:
                result = resolve_dependency(
                    graph=self._graph,
                    node_id=arguments["node_id"],
                    depth=arguments.get("depth", 2),
                    confidence_threshold=threshold,
                )
        elif name == "check_freshness":
            if self._graph is None or not self._repo_root:
                result = self._graph_required_result(name)
            else:
                result = check_freshness(
                    graph=self._graph,
                    repo_root=self._repo_root,
                    module_id=arguments["module_id"],
                    confidence_threshold=threshold,
                )
        elif name == "expand_projection":
            if self._graph is None:
                result = self._graph_required_result(name)
            else:
                result = expand_projection(
                    graph=self._graph,
                    node_id=arguments["node_id"],
                    additional_hops=arguments.get("additional_hops", 1),
                    edge_types=arguments.get("edge_types"),
                    confidence_threshold=threshold,
                )
        elif name == "fetch_contract":
            if self._graph is None:
                result = self._graph_required_result(name)
            else:
                result = fetch_contract(
                    graph=self._graph,
                    node_id=arguments["node_id"],
                    detail_records=self.state.active_detail_records,
                    confidence_threshold=threshold,
                )
        elif name == "get_clue":
            if self._graph is None or not self._repo_root:
                result = self._graph_required_result(name)
            else:
                commit_id = self._graph.metadata.get("commit_id", "") if self._graph.metadata else ""
                result = get_clue(
                    graph=self._graph,
                    repo_root=self._repo_root,
                    question=arguments.get("question"),
                    clue_text=self.state.active_clue_text,
                    commit_id=commit_id,
                    confidence_threshold=threshold,
                )
        elif name == "get_drill_targets":
            if not self.state.active_clue_text:
                result = {"status": "error", "message": "No clue loaded for get_drill_targets"}
            else:
                result = get_drill_targets(
                    clue_text=self.state.active_clue_text,
                    confidence_threshold=threshold,
                )
        else:
            result = {"status": "error", "message": f"Unknown tool: {name}"}

        self._log_tool_call(name, arguments, result)
        return result


def create_server(
    graph_path: str | None = None,
    repo_root: str | None = None,
    *,
    clue_dir: str | None = None,
    workspace_root: str | None = None,
    confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
) -> CodeClueServer:
    """Create a CodeClueServer from graph or MRLF clue artifacts."""
    graph = load_graph(Path(graph_path)) if graph_path else None
    return CodeClueServer(
        graph=graph,
        repo_root=repo_root,
        graph_path=graph_path,
        clue_dir=clue_dir,
        workspace_root=workspace_root,
        confidence_threshold=confidence_threshold,
    )


def serve_mcp(
    *,
    graph_path: str | None = None,
    repo_root: str | None = None,
    clue_dir: str | None = None,
    transport: str = "stdio",
    workspace_root: str | None = None,
    confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
) -> None:
    """Run the MCP transport for the public drill-down tools."""
    from mcp.server.fastmcp import FastMCP

    server = create_server(
        graph_path=graph_path,
        repo_root=repo_root,
        clue_dir=clue_dir,
        workspace_root=workspace_root,
        confidence_threshold=confidence_threshold,
    )

    app = FastMCP(name="CodeClue", instructions="CodeClue MRLF drill-down server")

    @app.tool(name="code_slice", description=_PUBLIC_TOOL_DEFINITIONS[0]["description"], structured_output=True)
    def _tool_code_slice(
        file_path: str | None = None,
        start_line: int | None = None,
        end_line: int | None = None,
        symbol_name: str | None = None,
    ) -> dict[str, Any]:
        return server.call_tool(
            "code_slice",
            {
                "file_path": file_path,
                "start_line": start_line,
                "end_line": end_line,
                "symbol_name": symbol_name,
            },
        )

    @app.tool(name="resolve_dependency", description=_PUBLIC_TOOL_DEFINITIONS[1]["description"], structured_output=True)
    def _tool_resolve_dependency(node_id: str, depth: int = 2) -> dict[str, Any]:
        return server.call_tool("resolve_dependency", {"node_id": node_id, "depth": depth})

    @app.tool(name="check_freshness", description=_PUBLIC_TOOL_DEFINITIONS[2]["description"], structured_output=True)
    def _tool_check_freshness(module_id: str) -> dict[str, Any]:
        return server.call_tool("check_freshness", {"module_id": module_id})

    @app.tool(name="expand_projection", description=_PUBLIC_TOOL_DEFINITIONS[3]["description"], structured_output=True)
    def _tool_expand_projection(
        node_id: str,
        additional_hops: int = 1,
        edge_types: list[str] | None = None,
    ) -> dict[str, Any]:
        return server.call_tool(
            "expand_projection",
            {"node_id": node_id, "additional_hops": additional_hops, "edge_types": edge_types},
        )

    @app.tool(name="fetch_contract", description=_PUBLIC_TOOL_DEFINITIONS[4]["description"], structured_output=True)
    def _tool_fetch_contract(node_id: str) -> dict[str, Any]:
        return server.call_tool("fetch_contract", {"node_id": node_id})

    @app.tool(name="get_clue", description=_PUBLIC_TOOL_DEFINITIONS[5]["description"], structured_output=True)
    def _tool_get_clue(question: str | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        if question is not None:
            payload["question"] = question
        return server.call_tool("get_clue", payload)

    @app.tool(name="get_drill_targets", description=_PUBLIC_TOOL_DEFINITIONS[6]["description"], structured_output=True)
    def _tool_get_drill_targets() -> dict[str, Any]:
        return server.call_tool("get_drill_targets", {})

    app.run(transport=transport)
