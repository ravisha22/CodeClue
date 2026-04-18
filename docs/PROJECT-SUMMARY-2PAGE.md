# CodeClue: Compressed Code Comprehension for LLM Consumption
### Project Summary — April 2026

## 1. Architecture

CodeClue compresses codebases into structured ≤10K token artifacts using three layers:

This extraction pipeline is rendered as a **two-file format**: **File 1**
(`.codeclue`) carries the compressed clue, and **File 2**
(`.codeclue-detail.jsonl`) provides drill-down detail on demand.

**Layer 1 — Deterministic AST Extraction (~4K tokens).** Parses source into five resolution levels: directory tree, module index, PageRank-ranked symbols, task-conditioned FOCUS entries (with behavioral patterns like GUARD, BRANCH, PRECEDENCE extracted from AST), and a GAPS section that self-reports sufficiency. Zero hallucination — same code always produces the same clue. Supports Python, Go, TypeScript.

**Layer 2 — LLM Domain Summary (~2K tokens).** A one-time LLM read of 10-20 key files (README, settings, models, schema, URLs) produces an architectural and domain model summary. Captures what AST extraction misses: entity relationships, business workflows, auth model, API surface. Generated once (~$0.05), consumed thousands of times.

**Layer 3 — File 2 Drill-Down (~3K tokens).** For mechanistic questions requiring function body logic, the GAPS section identifies specific symbols to drill into. An MCP server (5 tools) retrieves source snippets on demand within a token budget.

Total context per query: ~9-10K tokens. Compression: 95-97% on codebases ranging from 25K to 250K tokens.

## 2. Results

Evaluated on 18 repositories (10 libraries, 8 enterprise apps) across Python, Go, and TypeScript, with 400+ gold facts scored by GPT-5.4 using a standardized rubric.

**Libraries (deterministic extraction only):**
Structural 51.8%, relational 60.7%, mechanistic 41.1%. The format outperforms raw source retrieval at the same token budget by 8×.

**Enterprise apps — the breakthrough finding:**
AST-only extraction scored 23.4% across 8 enterprise repos (saleor, netbox, calcom, supabase, consul, mattermost, grafana, maybe). The full-stack hybrid (AST + LLM domain summary + drill-down) scored 100% on all 8 repos — independently verified by Claude Sonnet 4.6 on a 48-fact sample with zero disagreements.

The gap analysis showed 27% of enterprise misses were extraction gaps (patterns AST can't capture), 26% were thin graphs (too few symbols), and 19% were gold facts too specific for any 4K summary. The LLM domain summary layer addresses all three categories by providing the business context that makes code structure interpretable.

**Cross-model:** Six models tested on the same 8 tasks with identical prompts. Accuracy ranges from 34% (GPT-5.4-mini) to 75% (GPT-5.4). A 110-token reasoning scaffold (model-agnostic prompt block) narrows the gap — Sonnet 4.6 improves from 50% to 81% with scaffold.

## 3. Validation Rigor

| Check | Method | Result |
|---|---|---|
| Overfitting | Dev/blind split, 10 repos | 3.8pp gap (blind higher) |
| Scorer bias | Inter-rater agreement | κ = 0.607 (GPT-5.4 vs Sonnet 4.6) |
| Gold difficulty | Difficulty tagging per fact | Dev 75% DEEP vs blind 12.5% (documented) |
| Cross-model | 6 models, same prompts | Format readable by all; reasoning varies |
| Independent verify | Sonnet 4.6 strict re-score | 48/48 facts confirmed |
| Ablation | File 1 only vs +drill-down | +25pp mechanistic lift |
| Baselines | Summary, raw-topk, MRLF | 0%, 8.3%, 41-100% respectively |
| Statistical | Wilson + cluster-bootstrap CIs | All metrics with 95% intervals |
| Scalability | Up to 40K nodes, 1.5M edges | PageRank fallback for >100K edges |

## 4. Practical Applications and Token Efficiency

**The economics:** A 200K-token codebase compressed to ~10K tokens means every LLM interaction costs 95% fewer input tokens. For a team making 100 queries/day against a codebase, that's ~19M tokens/day saved. At $3/M input tokens, that's ~$57/day or ~$1,700/month per codebase.

**Generation cost:** Layer 1 (AST) is free. Layer 2 (LLM domain summary) costs ~$0.05 once per repo. Layer 3 (drill-down) adds ~3K tokens per query when needed (~35% of queries). Total incremental cost is negligible against the consumption savings.

**Use cases proven by evaluation:**

| Use Case | Task Family | Evidence |
|---|---|---|
| Codebase onboarding | Structural | 52-100% accuracy on "how is this organized?" |
| Dependency understanding | Relational | 61-100% on "what calls what? what extends what?" |
| Bug investigation | Mechanistic | 41-100% on "how does X handle error Y?" |
| Architecture review | All | Works on repos from 358 to 40K nodes |
| Cross-language comprehension | All | Python, Go, TypeScript from same format |

**Deployment options:**
- **CLI:** `codeclue extract` generates clue files for any repo
- **MCP Server:** 5 drill-down tools for LLM agents (code_slice, resolve_dependency, check_freshness, expand_projection, fetch_contract)
- **CI/CD:** GitHub Actions workflow regenerates clues on push
- **IDE:** Clue files injected into Copilot/Cursor context window

**Open source.** MIT license. 247 tests. All evaluation data published.
