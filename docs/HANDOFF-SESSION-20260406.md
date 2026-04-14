# Session Handoff — April 6, 2026

## Current State
- **Git**: v0.6.3 (0f5e2b6), all premature compact format changes reverted to clean HEAD
- **Source files**: confidence.py, operation_projection.py, server.py, tools.py — all at v0.6.3 state
- **Tests**: 93 MCP + 9 calibration + 3 drift = 105 passing (v0.6.3 baseline)
- **Untracked MCP files**: scaffolded but NOT wired into HEAD (see HANDOFF-MCP-PLAN.md)

## Untracked Files — MCP Workspace-Aware Server (DEFERRED)
These files were written and tested (133 tests passed) but then reverted because the compact format
research must happen FIRST. They are sitting in the working tree as untracked files.

### New files (working, tested, not committed):
- `src/codeclue_mcp/state.py` — SessionState + RepoInfo dataclasses
- `src/codeclue_mcp/cli.py` — CLI with optional --graph-path/--repo-root, added --workspace-root
- `src/codeclue_mcp/__main__.py` — entry point
- `tests/mcp/test_state.py` — 12 tests for session state, swap_graph, empty guards
- `tests/mcp/test_control_tools.py` — 27 tests for 6 control-layer tools

### To re-apply later:
See `docs/HANDOFF-MCP-PLAN.md` for the full plan. To re-implement:
1. Read the plan
2. Modify server.py: add SessionState, swap_graph, empty guards, 6 new tool registrations
3. Modify tools.py: add discover_repos, get_repo_status, generate_clue, select_repo, generate_projection, get_projection_summary
4. Update pyproject.toml: add `addopts = "--import-mode=importlib"` to fix tests/mcp namespace collision
5. Update test_cross_repo.py and test_mcp_protocol.py: tool count assertions (will be 11 or 12)

## What Was NOT Reverted (pre-existing working tree changes)
These were modified by Mr.G or earlier sessions, not by the current session's premature changes:
- LLMchat.md, README.md, docs/TOPICS-MAP.md, paper/codeclue-arxiv-final.md
- experiments/reports/scale-django-summary.json
- experiments/runs/ scripts (prepare_external_drilldown_*.py, collate_*, build_*)
- experiments/reports/external-drilldown/ (drill-down trial results)

## Critical Finding: Format Poisoning
The verbose format in confidence.py and operation_projection.py caused:
- 37% of clue tokens are format overhead (verbose keys, prose rationale, policy blocks)
- 83% of drill-down tool output tokens are verbose node/edge dicts (6x compressible)
- ETRR would jump from 0.64 → 0.91 with compact format
- The "drill-down is necessary" conclusion may be a format artifact, not a real information deficit
- This MUST be tested properly before any format changes are made

## Next Action: Clean-Room Format Research
User wants a proper research study with:
1. ≥85% token reduction target for compact clue format (small and large repos)
2. Proof that clue file alone can answer majority of questions without drill-down
3. Automated measurement wherever possible
4. Results suitable for publishing
5. Plan must be reviewed and approved BEFORE implementation begins
