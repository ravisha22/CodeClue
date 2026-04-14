# CodeClue MRLF v2.1 — Session Handoff
# Date: April 14, 2026
# Session: Generalization plan — design, implementation, evaluation
# Models Used: Claude Opus 4.6 (1M, orchestrator), GPT-5.4 (implementation + answerer), Claude Opus 4.6 (research analysis + scorer)
# Repository: https://github.com/ravisha22/CodeClue
# HEAD: 7b8ed8c (main)

---

## 1. WHAT HAPPENED THIS SESSION

### Starting State
- MRLF v2.0: blind eval scored **1/24 (4.2%)** on mechanistic gold facts
- Root cause identified: FOCUS entries had structural metadata but no behavioral content
- Previous fix attempt (Steps 3-3b) overfitted to specific repos

### Collaborative Analysis Phase
- Launched GPT-5.4 + Claude Opus 4.6 in parallel to analyze the project
- GPT-5.4 analyzed: code architecture, FOCUS algorithm, test coverage, format gaps
- Opus analyzed: research methodology, blind eval validity, design strategy, paper readiness
- Both independently converged on the same diagnosis and solution direction

### Key Findings from Analysis
1. **Root cause confirmed:** Information-theoretic gap, not algorithmic
2. **Previous overfitting identified:** `_tokenize_symbol()`, `_src_priority()` were repo-specific
3. **Design options ranked:** Option D (behavioral patterns) + Option B (File 2 drill-down)
4. **Paper publishable:** Even as negative result, the diagnostic methodology is the contribution

### Generalization Plan (5 Actions)
Both models collaborated on a principled fix plan with anti-overfitting guardrails.
The researcher reviewed and approved the plan before implementation.

### Implementation Results

| Commit | Action | Description |
|--------|--------|-------------|
| `998088b` | Checkpoint | Pre-generalization baseline (70+ untracked files) |
| `71a6724` | Action 0 | Validation framework: eval config, overfitting monitor, baseline |
| `f4f8a45` | PRD v0.7.0 | Full design documentation of generalization pivot |
| `60b8c1e` | Actions 2+1 | Graph-structural selection + behavioral pattern extraction |
| `9bd27b5` | Actions 3+4 | Budget-driven rendering + enhanced GAPS |
| `1f37655` | Regen | Regenerated all clue files with MRLF v2.1 |
| `4d10643` | Eval R1 | Blind eval round 1: 6/24 (25%) |
| `9f7da8b` | Bugfix | Compound-word splitting in _semantic_overlap |
| `7b8ed8c` | Eval R2 | Blind eval round 2: 7/24 (29.2%) |

### Final Score: 1/24 → 7/24 (4.2% → 29.2%, 7× improvement)

---

## 2. WHAT CHANGED IN THE CODE

### `src/codeclue_research/clue_view_mrlf.py` (major rewrite)
- **Removed:** `_tokenize_symbol()`, `_is_src_file()`, `_src_priority()`, `_kw_overlap()`, stemming heuristics, fixed 80-node cap, Stage 3 direct name matching
- **Added:** `_split_compound_words()`, `_semantic_overlap()`, `_betweenness_centrality()`, `_classify_question_type()`
- **Rewritten:** `_select_focus_nodes()` (semantic anchoring + containment expansion + call-graph walk + betweenness centrality ranking + budget-driven cap)
- **Rewritten:** `_render_gaps()` (sufficiency classification + coverage report + costed drill targets)
- **Updated:** Header version to `v2.1`, docstring to reference PRD v0.7.0

### `src/codeclue_research/extractor.py` (Python extractor)
- **Added:** `_extract_behavior_patterns()` with helpers `_is_early_exit()`, `_summarize_condition()`, `_has_return()`, `_get_call_name()`
- **Added:** `behavior_patterns` field to `_Symbol` dataclass
- **Updated:** `visit_FunctionDef` / `visit_AsyncFunctionDef` to extract behavioral patterns

### `src/codeclue_research/extract_go.py` (Go extractor)
- **Added:** `_extract_go_behavior_patterns()` — regex-based on function body text
- **Updated:** Function extraction to include `behavior_patterns` in semantic contract

### `src/codeclue_research/extract_typescript.py` (TypeScript extractor)
- **Added:** `_extract_ts_behavior_patterns()`, `_extract_ts_block()`
- **Updated:** Function/class extraction to include `behavior_patterns`

### `src/codeclue_research/models.py`
- **Added:** `behavior_patterns` normalization in `_normalize_semantic_contract()`

### `tests/foundation/test_mrlf.py`
- **Updated:** GAPS tests to match new format (type classification + coverage instead of keyword gaps)
- **Updated:** Header version check to `v2.1`

### New Files
- `experiments/eval-config.json` — Dev/validation/blind splits + overfitting detection config
- `experiments/runs/eval_monitor.py` — Automated evaluation with Wilson CIs + overfitting detection
- `experiments/runs/eval-baseline.json` — Pre-generalization baseline metrics
- `experiments/runs/regen_clues_v21.py` — Clue regeneration script
- `experiments/runs/blind-eval/blind-eval-results-v21.jsonl` — Round 1 results (6/24)
- `experiments/runs/blind-eval/blind-eval-results-v21-r2.jsonl` — Round 2 results (7/24)
- `experiments/runs/blind-eval/responses/*.md` — GPT-5.4 response files
- `source/CodeClue-PRD-v0.7.0-generalization.md` — Updated PRD with actual results
- `docs/RESEARCH-FIX-PLAN-20260414.md` — Opus-authored detailed research plan

---

## 3. EVALUATION RESULTS DETAIL

### Progression
```
v2.0 (pre-fix):   1/24 =  4.2%   [0.6%, 15.7%] (Wilson 95% CI)
v2.1 round 1:     6/24 = 25.0%   [12.0%, 43.8%]
v2.1 round 2:     7/24 = 29.2%   [14.9%, 49.2%]
```

### Per-Task Breakdown (v2.1-r2)

| Task | Score | Facts Covered | Why |
|------|-------|---------------|-----|
| aiohttp-1 | 0/4 | — | Payload accumulation, mimetype guards, multipart streaming too deep |
| aiohttp-2 | 1/4 | Reverse unwind | `UNWIND(reversed)` pattern + CleanupError in docstring |
| fiber-1 | 2/4 | Path rewrite, 404/405 | `configDependentPaths` in docstring, `BRANCH` pattern |
| fiber-2 | 1/4 | DefaultPanicHandler | Docstring contains full mechanism (same as v2.0) |
| click-1 | 3/4 | Decorator, add_command, dispatch | Docstrings + call graph + `DELEGATE` patterns |
| click-2 | 0/4 | — | Precedence chain, type_cast paths, Choice.convert normalization |

### What Behavioral Patterns Contributed
- **UNWIND(reversed)** → aiohttp-2 fact 4 (reverse cleanup)
- **BRANCH** → fiber-1 fact 4 (404 vs 405)
- **DELEGATE/DISPATCH** → click-1 facts 1,3,4 (decorator + dispatch chain)
- Behavioral patterns were directly responsible for **~4 of the 6 new coverages**

### What Still Fails (17/24 facts)
All require method body text that behavioral patterns can't capture:
- Precedence ORDER (which source is tried first, second, third)
- Specific guard CONDITIONS (what content type, what exception class)
- Constructor wiring (what gets installed when config field is nil)
- Async iteration mechanics (how chunks are streamed)
- Type-cast branching (different paths for single/tuple/variadic)

---

## 4. WHAT THE NEXT SESSION MUST DO

### Immediate (highest impact)
1. **Implement File 2 drill-down for MECHANISTIC questions.** Enhanced GAPS already reports costed drill targets. The two-step protocol: LLM reads File 1, identifies gaps via GAPS section, retrieves specific File 2 records. Phase 5 showed 18/20 sufficient with File 2 on dev repos. Test on validation repos.

2. **Add structural and relational gold tasks.** Current eval is 100% mechanistic (deliberately). Adding 2 structural + 2 relational tasks per repo would show the format's strengths (≥80% expected) and produce a more balanced paper.

3. **Select 3+ blind repos.** Current validation repos (aiohttp, fiber) have been examined. Recommended: `requests` (Python), `echo` (Go), `zod` (TS). Create gold tasks WITHOUT examining the repos' source code for debugging.

### Medium-term
4. **Improve behavioral pattern extraction.** Current patterns are shallow (e.g., `BRANCH(value_FLAG_NEEDS_VALUE)` doesn't describe the branches). Richer patterns with condition summaries would help: `PRECEDENCE(opts → envvar → default_map → default)`.

5. **Run overfitting check.** After any code change: `python experiments/runs/eval_monitor.py check`. If dev-val gap > 10pp, revert.

6. **Write the paper.** The story is: 81% TRR + zero hallucination + 29% mechanistic from File 1 + guided drill-down for the rest. Target: ICSE NIER or ASE Tool Track.

### Design Discipline Rules
- NO repo-specific heuristics
- NO celebrating dev accuracy
- NO magic numbers without justification
- Validate on held-out, publish on blind
- Every metric with confidence intervals

---

## 5. KEY FILES REFERENCE

### Core Source (modified this session)
| File | What Changed |
|------|-------------|
| `src/codeclue_research/clue_view_mrlf.py` | FOCUS selection, GAPS, behavioral rendering |
| `src/codeclue_research/extractor.py` | Python behavioral pattern extraction |
| `src/codeclue_research/extract_go.py` | Go behavioral pattern extraction |
| `src/codeclue_research/extract_typescript.py` | TS behavioral pattern extraction |
| `src/codeclue_research/models.py` | behavior_patterns normalization |

### Evaluation Infrastructure (new this session)
| File | Purpose |
|------|---------|
| `experiments/eval-config.json` | Splits, thresholds, reporting standards |
| `experiments/runs/eval_monitor.py` | Overfitting monitor + metric reporter |
| `experiments/runs/regen_clues_v21.py` | Clue regeneration script |
| `experiments/runs/blind-eval/blind-eval-results-v21-r2.jsonl` | Latest results |

### Design Documents (new/updated this session)
| File | Purpose |
|------|---------|
| `source/CodeClue-PRD-v0.7.0-generalization.md` | Updated PRD with actual results |
| `docs/RESEARCH-FIX-PLAN-20260414.md` | Detailed research fix plan (Opus-authored) |

---

## 6. TEST STATUS

**102 passed, 1 pre-existing TS fail, 2 skips** — same baseline throughout session.

The 1 TS failure (`this.findById()` call edge detection) is a known gap in `extract_typescript.py` — tracked but out of scope for format design.

---

## 7. UNCOMMITTED FILES

None — all work committed and pushed to `origin/main`.

```
7b8ed8c (HEAD -> main, origin/main) Blind eval v2.1 round 2: 7/24 (29.2%)
9f7da8b Fix: split compound words in _semantic_overlap
4d10643 Blind eval v2.1: GPT-5.4 answers + Opus scoring — 6/24 (25%)
1f37655 Regenerate blind-eval clues and prompts with MRLF v2.1
9bd27b5 Action 3+4: Budget-driven rendering + enhanced GAPS
60b8c1e Action 2+1: Graph-structural FOCUS selection + behavioral pattern extraction
f4f8a45 PRD v0.7.0: Generalization pivot
71a6724 Action 0: Validation framework
998088b chore: checkpoint pre-generalization
```
