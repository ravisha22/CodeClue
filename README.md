# CodeClue: Compressed Code Comprehension for LLMs

**Persistent, versioned codebase understanding in ≤10K tokens.**

## Goals

This project investigates whether compressed, persistent code comprehension
artifacts can replace raw source reading for LLM-assisted software engineering.

**Research question:** Can we encode code understanding in ≤10K tokens that
preserves enough meaning for LLMs to answer structural, relational, and
mechanistic questions about enterprise codebases — at 95%+ compression?

**Success criteria:**
- SF1: ≥85% token compression
- SF2: ≥60% of questions answerable from clue alone (no drill-down)
- SF3: ≤40% of questions need drill-down
- SF4: Drill-down provides ≥10pp accuracy lift when used

CodeClue compresses entire codebases into structured comprehension artifacts that LLMs consume instead of reading raw source. The format achieves 95-97% token reduction while retaining enough information to answer structural, relational, and mechanistic questions about the code — including enterprise applications.

## Results

Evaluated on **18 repositories** across **3 languages** (Python, Go, TypeScript), including both open source libraries and enterprise applications.

### Libraries (7 repos: requests, echo, zod, express, gin, httpx, fastapi)

| Task Family | Accuracy | What It Tests |
|---|---|---|
| **Structural** | 51.8% | File/module organization, project layout |
| **Relational** | 60.7% | Class hierarchies, call graphs, dependencies |
| **Mechanistic** | 41.1% | Internal logic, error handling, control flow |

### Enterprise Apps with Full-Stack Hybrid (8 repos)

| Repo | Language | AST Only | Full-Stack | Compression |
|---|---|---|---|---|
| saleor | Python | 29% | **100%** | 95% |
| netbox | Python | 42% | **100%** | 96% |
| calcom | TypeScript | 17% | **100%** | 95% |
| supabase | TypeScript | 21% | **100%** | 95% |
| consul | Go | 33% | **100%** | 97% |
| mattermost | Go | 13% | **100%** | 97% |
| grafana | Go | 8% | **100%** | 97% |
| maybe | TypeScript | 0% | **100%** | 94% |

Enterprise scores independently verified by Claude Sonnet 4.6 (48 facts, zero disagreements).

### Baselines (same ~6K token budget)

| Method | Score |
|---|---|
| Plain summary (filenames only) | 0% |
| Raw top-k source files | 8.3% |
| **CodeClue (deterministic)** | **41-61%** |
| **CodeClue (full-stack hybrid)** | **100%** |

### Cross-Model Validation (6 models, same format)

| Model | Accuracy |
|---|---|
| Sonnet 4.6 + reasoning scaffold | 81.3% |
| GPT-5.4 | 75.0% |
| Haiku 4.5 | 50.0% |
| Sonnet 4.6 (no scaffold) | 50.0% |
| Goldeneye | 43.8% |
| GPT-5.4-mini | 34.4% |

The reasoning scaffold (a model-agnostic prompt block, ~110 tokens) narrows the cross-model gap by +31pp on Sonnet.

## How It Works

```
Source Code  →  Three-Layer Extraction  →  ≤10K Token Artifact  →  LLM Consumption
```

**Layer 1: Deterministic AST Extraction (~4K tokens)**
- TREE: directory layout
- INDEX: modules + top exports
- SYM: PageRank-ranked symbol table
- FOCUS: task-conditioned detail with behavioral patterns (GUARD, BRANCH, PRECEDENCE)
- GAPS: self-reports what the clue can and cannot answer

**Layer 2: LLM Domain Summary (~2K tokens, one-time)**
- Reads 10-20 key files (README, settings, models, schema, URLs)
- Produces: domain model, API surface, auth, key workflows
- Cost: ~$0.05 per repo, generated once, consumed thousands of times
- Essential for enterprise apps, optional for libraries

**Layer 3: File 2 Drill-Down (~3K tokens, on-demand)**
- GAPS identifies what's missing → MCP tools retrieve source snippets
- Adds +25pp on mechanistic questions

## Quick Start

```bash
git clone https://github.com/ravisha22/CodeClue.git
cd CodeClue
python -m venv .venv && .venv/Scripts/activate  # or source .venv/bin/activate
pip install -e .

# Inspect the installed CLI
.venv\Scripts\python.exe -m codeclue_research.cli --help

# Extract the canonical graph
.venv\Scripts\python.exe -m codeclue_research.cli extract --repo-root /path/to/repo --output artifacts\graph.json --language python

# Add deterministic deep context (writes artifacts\graph.codeclue-context)
.venv\Scripts\python.exe -m codeclue_research.cli extract --repo-root /path/to/repo --output artifacts\graph.json --language python --deep

# Start the MCP server for drill-down
codeclue-mcp --clue-dir .codeclue/ --repo-root /path/to/repo
```

## MCP Server

5 tools exposed via Model Context Protocol:

| Tool | Purpose |
|---|---|
| `code_slice` | Fetch source lines for a symbol or file range |
| `resolve_dependency` | Expand dependency subgraph from a node |
| `check_freshness` | Verify clue is current vs source |
| `expand_projection` | Widen view around a node |
| `fetch_contract` | Get full semantic contract for a symbol |

The MCP server is functional with real stdio transport (tested end-to-end via subprocess spawning). 138 MCP tests pass. Two test files have an import resolution conflict with the `mcp` SDK package namespace but the server itself works correctly.

## Validation Rigor

| Check | Result |
|---|---|
| Dev-blind split | 3.8pp gap (no overfitting) |
| Inter-rater agreement | κ = 0.607 (GPT-5.4 vs Sonnet 4.6) |
| Cross-model validation | 6 models tested on same prompts |
| Gold difficulty calibration | Dev 75% DEEP vs blind 12.5% DEEP (documented) |
| Cluster-aware CIs | Bootstrap at repo level for all metrics |
| Independent verification | Sonnet 4.6 strict re-score, zero disagreements |
| Ablation | File 1 only vs +drill-down: +25pp lift |

## Testing

```bash
pytest tests/foundation/ tests/test_mcp/ -q    # run foundation and MCP test suites
```

## Project Structure

```
src/codeclue_research/     # Extractors, renderer, models
src/codeclue_mcp/          # MCP server (5 tools, budget, tracing)
experiments/               # Evaluation data, gold tasks, responses
paper/                     # Research paper draft
docs/                      # Architecture, charter, open issues
tests/                     # Foundation and MCP test suites
```

## License

MIT

## Author

Ravi Nandagopalan
