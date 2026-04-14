# Plan: Workspace-Aware CodeClue MCP Server — 11-Tool MVP

## TL;DR
Transform the MCP server from a single-graph drill-down server into a workspace-aware lifecycle server. Add 6 new "control layer" tools (discover_repos, get_repo_status, generate_clue, select_repo, generate_projection, get_projection_summary) on top of the existing 5 drill-down tools. Server starts empty, LLM drives the full workflow from chat.

**Origin:** Merged design from Mr.C (initial plan) + Mr.G (expanded architecture critique + workspace-aware framing). Both agreed on final 6-tool MVP.

## Architecture

### Two-Layer Model
- **Control layer** (6 new tools): repo discovery, clue lifecycle, projection generation, session state
- **Drill-down layer** (5 existing tools, unchanged): code_slice, resolve_dependency, check_freshness, expand_projection, fetch_contract

### Session State (dataclass, in-memory only, no persistence across restarts)
```python
@dataclass
class SessionState:
    workspace_root: str | None       # set from CLI or first discover_repos
    discovered_repos: list[RepoInfo] # populated by discover_repos
    active_repo: str | None          # set by select_repo
    active_clue_path: str | None     # set by generate_clue or select_repo
    active_graph: CanonicalClueGraph | None  # loaded graph
    active_projection_path: str | None       # set by generate_projection
```

### .git Policy (compromise — Mr.C + Mr.G agreed)
- `discover_repos`: scans for `.git/` dirs as default boundary (shallow, workspace children only)
- `generate_clue`: does NOT hard-require `.git/`. Path must be inside workspace root. Non-.git paths require explicit `allow_no_git=true` param. Default = require .git.
- Rationale: safe default, no over-constraining for monorepo subdirs or snapshots.

### Failure Semantics (Mr.G requirement)
- If extraction fails in `generate_clue`, the currently loaded graph MUST remain active
- No half-swapped state — swap only on full success
- Implementation: extract to temp path → validate → swap state → rename to final path

## Steps

### Phase 1: Session state + mutable server core
1. Create `src/codeclue_mcp/state.py` with `SessionState` dataclass and `RepoInfo` dataclass
2. Refactor `CodeClueServer.__init__` to accept optional graph/repo_root + hold `SessionState`
3. Add `swap_graph(graph, repo_root, graph_path)` on `CodeClueServer` with rollback-on-failure semantics
4. Add guard to existing 5 drill-down tools: if `active_graph is None`, return `{"status": "error", "message": "No clue loaded. Call generate_clue or select_repo first."}`

**Files:** `src/codeclue_mcp/state.py` (new), `src/codeclue_mcp/server.py`

### Phase 2: `discover_repos` tool
5. Implementation: scan `workspace_root` immediate children for `.git/` dirs. Return `[{repo_name, repo_path, language_hint, has_existing_clue}]`. Language hint from file extension survey (*.py → python, *.ts → typescript, *.go → go).
6. Register in server.py (definition, call_tool dispatch, FastMCP wrapper)

**Files:** `src/codeclue_mcp/tools.py`, `src/codeclue_mcp/server.py`

### Phase 3: `get_repo_status` tool
7. Implementation: given a repo path (or uses active_repo), returns `{repo_path, language, current_commit, clue_exists, clue_path, clue_generated_at, clue_node_count, is_stale}`. Staleness = commit in graph metadata != current HEAD.
8. Register in server.py

**Files:** `src/codeclue_mcp/tools.py`, `src/codeclue_mcp/server.py`

### Phase 4: `generate_clue` tool (*depends on Phase 1*)
9. Implementation:
   - Params: `repo_path: str`, `language: str` (python|typescript|go|auto), `output_path: str | None` (default: `<repo_path>/.codeclue/graph.json`), `allow_no_git: bool = false`
   - Validates: path inside workspace root, .git exists (unless allow_no_git), supported language
   - Calls `extract_graph()` → `save_graph()` to temp → validate → `swap_graph()` → rename to final
   - Returns `{status, repo_path, graph_path, node_count, edge_count, language, commit_id}` — NOT the graph blob
10. Register in server.py

**Files:** `src/codeclue_mcp/tools.py`, `src/codeclue_mcp/server.py`

### Phase 5: `select_repo` tool (*depends on Phase 1*)
11. Implementation: sets active_repo, finds existing clue at `<repo_path>/.codeclue/graph.json`, loads it if found. Returns `{status, repo_path, clue_loaded, clue_path, node_count}` or `{status: "no_clue", message: "Call generate_clue to create one"}`.
12. Register in server.py

**Files:** `src/codeclue_mcp/tools.py`, `src/codeclue_mcp/server.py`

### Phase 6: `generate_projection` tool (*depends on Phase 4*)
13. Implementation:
    - Params: `operation_family: str` (OF1-OF5), `output_path: str | None` (default: `<clue_dir>/projections/<OF>.json`)
    - Calls `project_operation()` from `codeclue_research.operation_projection`
    - Saves projection to disk, updates `active_projection_path`
    - Returns `{status, operation_family, node_count, confidence_overall, suggested_actions, projection_path}` — NOT the full projection blob
14. Register in server.py

**Files:** `src/codeclue_mcp/tools.py`, `src/codeclue_mcp/server.py`

### Phase 7: `get_projection_summary` tool (*parallel with Phase 6 once projection format is known*)
15. Implementation: reads the active (or specified) projection file, returns `{operation_family, node_count, confidence_overall, confidence_breakdown, low_confidence_nodes: list[{node_id, confidence, suggested_action}], artifact_path}`.
16. Register in server.py

**Files:** `src/codeclue_mcp/tools.py`, `src/codeclue_mcp/server.py`

### Phase 8: CLI updates
17. Make `--graph-path` and `--repo-root` optional in cli.py. Server starts with no graph when omitted.
18. Add `--workspace-root` arg (defaults to cwd)
19. Keep `--graph-path` + `--repo-root` for backward compat — pre-loads that graph on startup

**Files:** `src/codeclue_mcp/cli.py`

### Phase 9: `.vscode/mcp.json` update
20. Simplify to just `--workspace-root` pointing at workspace folder

**Files:** `.vscode/mcp.json`

### Phase 10: Tests
21. Unit tests for `SessionState` — swap, rollback on failure, guard when empty
22. Unit tests for `discover_repos` — temp workspace with .git dirs (*parallel with 23*)
23. Unit tests for `generate_clue` — mock extract_graph, verify swap + rollback (*parallel with 22*)
24. Unit tests for `select_repo` — existing clue found/not found
25. Unit tests for `generate_projection` — mock project_operation, verify disk write
26. Unit tests for `get_repo_status` and `get_projection_summary`
27. Integration test: discover → select → generate_clue → generate_projection → get_projection_summary → fetch_contract (full flow)
28. Regression: all 93 existing drill-down tests still pass

**Files:** `tests/mcp/test_state.py` (new), `tests/mcp/test_control_tools.py` (new), existing test files unchanged

## Relevant files
- `src/codeclue_mcp/state.py` — NEW: SessionState + RepoInfo dataclasses
- `src/codeclue_mcp/server.py` — CodeClueServer refactor: hold SessionState, swap_graph with rollback, register 6 new tools
- `src/codeclue_mcp/tools.py` — 6 new tool implementations
- `src/codeclue_mcp/cli.py` — make args optional, add --workspace-root
- `src/codeclue_research/extractor.py` — `extract_graph()` called by generate_clue
- `src/codeclue_research/operation_projection.py` — `project_operation()` called by generate_projection
- `src/codeclue_research/io.py` — save_graph/load_graph for persistence
- `.vscode/mcp.json` — simplified config
- `tests/mcp/test_state.py` — NEW: session state tests
- `tests/mcp/test_control_tools.py` — NEW: control layer tool tests

## Verification
1. `python -m pytest tests/mcp/ -v` — all 93 existing tests pass (regression)
2. All new unit tests pass (target: ~20-25 new tests)
3. Manual flow: start server empty → `discover_repos` → `select_repo` → `generate_clue` → `generate_projection` → `get_projection_summary` → `fetch_contract` on a low-confidence node
4. Manual failure test: give `generate_clue` a bad path → verify active graph unchanged
5. Manual: `generate_clue` with `allow_no_git=true` on a non-git directory

## Decisions
- **6 new tools + 5 existing = 11 total** — coherent, testable, no bloat
- **`refresh_clue` folded into `generate_clue`** (force param not even needed — just re-run, it overwrites)
- **`select_clue` folded into `select_repo`** — repo implies its clue
- **`ask_with_clue` deferred** — explicitly future scope
- **`list_clues` deferred** — nice-to-have, not MVP
- **No graph blobs over MCP** — tools return summaries, paths, stats. Big artifacts stay on disk.
- **Session state is in-memory only** — no persistence across restarts. Graph files on disk are the durable state.
- **Conventional clue location**: `<repo_path>/.codeclue/graph.json`
- **Conventional projection location**: `<repo_path>/.codeclue/projections/<OF>.json`
- **Synchronous extraction for MVP** — API designed to not block async upgrade later (return status object)
- **.git policy**: required by default for discover_repos; overrideable via allow_no_git for generate_clue; path must be inside workspace root regardless

## Excluded from MVP
- Async/background extraction with progress events
- Remote repo cloning (local clones only)
- `ask_with_clue` orchestration tool
- `list_clues` artifact browser
- Cross-server session persistence
- Multi-workspace support

## Additional deferred tool: render_clue
- Converts compact clue/projection artifacts to human-readable text (ETW trace → log file analogy)
- Should be implemented AFTER compact format research is complete

## Scaffolded Files (untracked in working tree)
These files were written, tested (133 tests passed), then source files reverted because compact format
research must happen first. The new files remain in the working tree as starting points:
- `src/codeclue_mcp/state.py` — SessionState + RepoInfo dataclasses
- `src/codeclue_mcp/cli.py` — CLI with optional --graph-path/--repo-root, added --workspace-root
- `src/codeclue_mcp/__main__.py` — entry point
- `tests/mcp/test_state.py` — 12 tests for session state, swap_graph, empty guards
- `tests/mcp/test_control_tools.py` — 27 tests for 6 control-layer tools

To re-implement, the modifications to server.py, tools.py, pyproject.toml, test_cross_repo.py, and
test_mcp_protocol.py need to be re-applied. The scaffolded files above can be used as-is.
