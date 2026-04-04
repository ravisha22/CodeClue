# CodeClue

**Persistent LLM-native code comprehension with confidence-gated source drill-down.**

CodeClue generates persistent "clue files" for your codebase — graph-structured comprehension artifacts optimized for LLM consumption. Instead of re-reading raw source on every interaction, your AI assistant reads a 5x smaller clue file and only drills into source where the artifact signals insufficient confidence.

## Key Results

Validated on **23 tasks across 7 public repositories** (Flask, FastAPI, NestJS, httpx, Express, TypeORM, Gin) in **4 languages** (Python, TypeScript, JavaScript, Go):

| Metric | Value |
|---|---|
| **Token reduction** | 81% fewer tokens than raw-source-first |
| **Hallucination rate** | 0.00 — zero across all tasks, repos, and model families |
| **Confidence accuracy** | IFT alignment 0.65 — low confidence correctly predicts where drill-down is needed |
| **Cross-model validity** | Confirmed across Claude, GPT, and Gemini (mean delta 0.12) |

The confidence system correctly identifies which tasks can be answered from the clue alone (edit localization: 0.80 fidelity) and which need source verification (impact analysis: 0.29 fidelity at Tier 1).

Full empirical data: [source/CodeClue-PRD-v0.3.0-mvp-FINAL.md](source/CodeClue-PRD-v0.3.0-mvp-FINAL.md) Appendix F.

## How It Works

```
Source Code                    Clue Graph                      LLM Consumption
  ├── app.py         ──►     ├── nodes (symbols)      ──►    Read clue first
  ├── ctx.py                  ├── edges (calls, contains)     Check confidence
  ├── sessions.py             ├── confidence scores           If low → drill down
  └── ...                     └── suggested actions           If high → answer directly
```

1. **Extract**: Parse your codebase into a canonical graph of nodes (modules, functions, classes) and edges (calls, containment).
2. **Score**: Each node and edge gets a structural confidence score measuring coverage gaps, dependency closure, and code density risk.
3. **Suggest**: Low-confidence nodes carry concrete drill-down actions: "fetch lines 88-142 of validator.py" or "resolve dependency closure for this edge."
4. **Serve**: An MCP server exposes 5 typed tools that the consuming LLM can call when it needs more information.

## Quick Start

### Installation

```bash
git clone https://github.com/ravisha22/CodeClue.git
cd CodeClue
python -m venv .venv
.venv/Scripts/activate    # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -e .
```

### Extract a Clue Graph

```bash
# Extract from any repository
codeclue extract --repo-root /path/to/your/repo --language auto --output .codeclue/graph.json --commit-id HEAD

# Extract with generator model tagging (for cross-model calibration)
codeclue extract --repo-root . --language python --output .codeclue/graph.json --commit-id HEAD --generator-model claude-opus-4.6
```

### Generate a Task-Conditioned Projection

```bash
# Architecture view (OF1)
codeclue project --graph-file .codeclue/graph.json --operation-family OF1 --output-file .codeclue/projection-arch.json

# Impact analysis (OF2) with a focus profile
codeclue project --graph-file .codeclue/graph.json --operation-family OF2 --prompt-profile-file profile.yaml --output-file .codeclue/projection-impact.json
```

The output includes a `confidence` block:
```json
{
  "confidence": {
    "confidence_overall": 0.73,
    "lookup_decision_hint": "targeted_lookup",
    "p_context_miss": 0.12,
    "p_dependency_miss": 0.18,
    "tool_call_budget": 15,
    "per_node_confidence": [
      {
        "node_id": "symbol:src/payments/processor.py:ProcessPayment:45",
        "confidence": 0.62,
        "suggested_actions": [
          {"tool": "resolve_dependency", "args": {"node_id": "...", "depth": 2},
           "rationale": "3 edges point outside projection"}
        ]
      }
    ]
  }
}
```

### Run the Full Evaluation Pipeline

```bash
# Full pilot: extract + validate + roundtrip + integrity + project + fidelity + CCT
codeclue run-pilot --repo-root . --run-dir experiments/runs/my-run --commit-id HEAD --language auto --operation-family OF2 --prompt-profile-file tests/fixtures/prompt_profile_impact.yaml --gold-file tests/fixtures/gold_path_impact.yaml --probe-file tests/fixtures/cct_probe_adversarial.yaml --trace-file tests/fixtures/cct_trace_adversarial.jsonl
```

## MCP Server Setup

CodeClue provides a Model Context Protocol (MCP) server that exposes 5 drill-down tools to any MCP-compatible AI agent.

### Tools Available

| Tool | What It Does | When To Use |
|---|---|---|
| `code_slice` | Fetches raw source lines | Confidence low on a node, need to see the implementation |
| `resolve_dependency` | BFS-expands a dependency subgraph | Edge points outside projection, dependency closure incomplete |
| `check_freshness` | Compares clue hash against current source | Before trusting a clue that may be stale |
| `expand_projection` | Widens the view around a node by N hops | Projection too narrow for the current question |
| `fetch_contract` | Returns full semantic contract for a node | Need behavioral detail (preconditions, failure modes) |

### Using the Server Programmatically

```python
from codeclue_mcp.server import create_server

# Create server from a clue graph
server = create_server(
    graph_path=".codeclue/graph.json",
    repo_root="/path/to/your/repo"
)

# List available tools
tools = server.list_tools()  # Returns 5 tool definitions with JSON schemas

# Call a tool
result = server.call_tool("code_slice", {
    "file_path": "src/flask/app.py",
    "start_line": 1420,
    "end_line": 1460
})
# result["status"] == "ok"
# result["lines"] == [{"line_number": 1420, "content": "..."}, ...]
```

### Invocation Tracing

Every tool call is logged to JSONL for reproducibility:

```python
from codeclue_mcp.tracer import InvocationTracer

tracer = InvocationTracer(trace_dir=".codeclue/traces")
tracer.log(
    tool="code_slice",
    args={"file_path": "app.py", "start_line": 1, "end_line": 50},
    output_hash="a1b2c3d4",
    source_anchor="symbol:app.py:Flask:1",
    confidence_trigger=0.62,
    session_id="session-001"
)
```

### Budget Enforcement

Per-session tool call budgets prevent drill-down from negating token savings:

```python
from codeclue_mcp.budget import BudgetTracker

tracker = BudgetTracker(operation_family="OF2")  # Budget: 15 calls
tracker.can_call()  # True
tracker.record_call(tool="code_slice", node_id="symbol:app.py:dispatch:966")
tracker.remaining()  # 14

# When exhausted:
tracker.register_unresolved(["node_c", "node_d"])
escalation = tracker.get_escalation()
# {"budget_exhausted": True, "unresolved_nodes": ["node_c", "node_d"]}
```

Default budgets per operation family: OF1: 5, OF2: 15, OF3: 10, OF4: 20, OF5: 30.

## Operation Families

Five task-conditioned projections extract different views from the same canonical graph:

| Family | Focus | Best For | Tier 1 Sufficient? |
|---|---|---|---|
| **OF1** Architecture | Structural overview | "How is this organized?" | Partial |
| **OF2** Impact Analysis | Change propagation chains | "What breaks if I change X?" | No — needs Tier 2 |
| **OF3** Edit Localization | Where to modify | "Where should I add this feature?" | **Yes** |
| **OF4** Debugging | Runtime behavior | "Why does this throw?" | No — needs Tier 2 |
| **OF5** Security | Compliance verification | "Is auth enforced here?" | No — needs Tier 2 |

## Two-Tier Contract Schema

**Tier 1 (Structural)** — always present, extracted by AST/regex parsing:
- `purpose`, `language`, `symbol_name`, `symbol_type`
- `calls` (populated from edge data), `called_by`
- `complexity_indicators` (decorator depth, generic params)

**Tier 2 (Semantic)** — requires LLM generation pass:
- `preconditions`, `postconditions`, `failure_modes`
- Extended complexity (reflection, dynamic dispatch detection)

Tier 1 is safe (zero hallucinations in all testing). Tier 2 unlocks behavioral understanding for OF2/OF4/OF5.

## Validation Results

### Cross-Model Evaluation

Three frontier LLMs tested — no single model served more than one role per task:

| Role | Model |
|---|---|
| Generator (Tier 2 contracts) | Claude Opus 4.6 |
| Consumer (blind task execution) | GPT 5.4 |
| Judge (independent scoring) | Gemini 3.1 Pro |

Gemini verdict: **PASS** (mean Arm B delta 0.12, zero hallucinations both models).

Full cross-model results: [experiments/cross-model-eval/results/gemini-judge-SUMMARY.json](experiments/cross-model-eval/results/gemini-judge-SUMMARY.json)

### Ecological Validity (Lane B)

Validated against Information Foraging Theory (Piorkowski et al., 2016):

| Metric | Value | Target |
|---|---|---|
| IFT Scent Alignment | 0.65 | ≥ 0.60 ✓ |
| Spearman ρ | −0.30 | Negative ✓ |
| Sillito KL divergence | 0.29 | < 0.15 (improved 3x, not yet passing) |

### Per-Family Fidelity (v2, 23 tasks)

| Family | Arm B (Clue) | Arm A (Raw Source) | Gap |
|---|---|---|---|
| TF1 Architecture | 0.61 | 0.93 | 0.32 |
| TF2 Impact | 0.29 | 0.89 | 0.60 |
| TF3 Edit | 0.80 | 0.93 | 0.13 |
| TF4 Debugging | 0.55 | 0.95 | 0.40 |
| TF5 Security | 0.53 | 0.94 | 0.41 |

## Project Structure

```
src/
  codeclue_research/     # Core research package
    extractor.py         # Graph extraction (Python, TypeScript, Go, JS)
    confidence.py        # Structural confidence scoring
    operation_projection.py  # OF1-OF5 projection engine
    fidelity.py          # Gold-path fidelity evaluation
    cct.py               # Comprehension Circuit Tracing
    lane_a.py            # Lane A batch evaluation
    lane_b.py            # Lane B ecological validity (IFT, Sillito)
    ...
  codeclue_mcp/          # MCP tool server
    server.py            # Server with 5 tools
    tools.py             # Tool implementations
    tracer.py            # Invocation trace logging
    budget.py            # Per-session budget enforcement
tests/
  mcp/                   # 93 tests for MCP server
  fixtures/              # Gold paths, probes, task definitions
source/
  CodeClue-PRD-v0.3.0-mvp-FINAL.md  # Full research specification (v0.6.0)
paper/
  codeclue-arxiv-final.md   # arXiv paper draft
  codeclue-explainer.md     # Technical manager explainer
experiments/
  reports/               # Benchmark results, Lane B data
  cross-model-eval/      # GPT/Gemini evaluation artifacts
docs/
  CROSS-MODEL-EVALUATION-PROTOCOL.md  # How to reproduce
  GAP-REMEDIATION-PLAN.md             # Remaining research gaps
```

## Testing

```bash
# Run MCP server tests (93 tests across 7 repos)
python -m pytest tests/mcp/ -v

# Run fidelity regression checks
codeclue fidelity-eval --projection-file experiments/runs/sprint6-test/blue-check-OF2.json --gold-file tests/fixtures/gold_path_impact.yaml
```

## Research Paper

- **arXiv draft**: [paper/codeclue-arxiv-final.md](paper/codeclue-arxiv-final.md) — reviewed by GPT 5.4, corrected by Gemini 3.1 Pro, 11 factual corrections applied.
- **Explainer**: [paper/codeclue-explainer.md](paper/codeclue-explainer.md) — non-academic version for technical managers.
- **Full PRD**: [source/CodeClue-PRD-v0.3.0-mvp-FINAL.md](source/CodeClue-PRD-v0.3.0-mvp-FINAL.md) — v0.6.0 with Appendices A-F.

## Roadmap

| Epic | Status | What |
|---|---|---|
| MCP Server | ✅ Complete | 5 tools, 93 tests, cross-repo validated |
| Delta Drift Testing | Planned | H3/H4: 50-commit drift protocol |
| Scale Testing | Planned | 500K+ token repos (django, TypeScript compiler) |
| Per-Model Calibration | Planned | Calibration profiles for Claude/GPT/Gemini |

## License

MIT

## Author

Ravi Nandagopalan
