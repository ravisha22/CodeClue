# Session Handoff — April 7, 2026

## Quick Resume

Read these files in order:
1. `docs/New-Design-Basis.md` — full MRLF design, constraints, use cases, execution plan
2. This file — milestone log and current state
3. `src/codeclue_research/clue_view_mrlf.py` — the renderer
4. `tests/foundation/test_mrlf.py` — 38 passing tests

## What Happened This Session

### Decision: Abandon all prior formats, redesign from scratch

All prior formats (Poisoned, Plan A, Plan B, Hybrid) failed H2 (fidelity ≥ 0.85).
Root cause: selecting 15 nodes and discarding 99% of the codebase violates the
Data Processing Inequality. Flask-only success (0.93) vs everything-else failure
(0.20–0.45) proves the projector, not the format, was the bottleneck.

New design: Multi-Resolution Lattice Format (MRLF).
- 2 files per repo (not 5): File 1 (.codeclue) ≤ 4150 tokens, File 2 (.codeclue-detail) JSONL
- 4 resolution levels: L0 TREE → L1 INDEX → L2 SYM (PageRank) → L3 FOCUS (keyword + graph walk) → GAPS
- 100% structural coverage at L0-L1 (every module visible)
- No JSON in consumer artifact; plain text with `-- SECTION` markers
- Scale-invariant: fixed token ceiling regardless of repo size

### Design documented in `docs/New-Design-Basis.md`:
- Section 0: Purpose, persona, 50 use cases across 9 categories
- Section 1-2: Root cause diagnosis + mathematical framework
- Section 3: MRLF format spec
- Section 4: 9 active constraints + 10 excluded constraints (with rationale)
- Section 5: Risk analysis, token efficiency, NC2/NC5 deep-dive
- Section 6-7: Success mapping + killed approaches
- Section 8: All 7 open questions resolved
- Section 9: Fresh-start reconstruction guide
- Section 10: 6-phase execution plan with gates

---

## Milestone Log

### M0: Design Complete ✅
- Date: 2026-04-07
- Artifact: `docs/New-Design-Basis.md`
- Status: Full design with constraints, use cases, math framework, execution plan

### M1: MRLF Renderer Implemented ✅
- Date: 2026-04-07
- Artifact: `src/codeclue_research/clue_view_mrlf.py`
- What: Pure-Python PageRank, L0-L3+GAPS rendering, budget enforcement, detail store generator
- Tests: 38 passing (`tests/foundation/test_mrlf.py`)

### M2: First Multi-Repo Generation ✅
- Date: 2026-04-07
- Artifacts: `experiments/runs/mrlf-benchmark/*.codeclue`
- Results:
  | Repo | Modules | Symbols | ~Tokens (est) | Budget Used (est) |
  |------|---------|---------|---------------|-------------------|
  | Flask | 83 | 1,629 | ~2,661 | 64% |
  | httpx | 60 | 1,241 | ~2,607 | 63% |
  | Gin | 99 | 1,481 | ~2,354 | 57% |
  | FastAPI | 1,122 | 5,252 | ~2,732 | 66% |
- Confirmed: Scale-invariance holds. FastAPI (3× Flask symbols) → only 71 more tokens.
- Not confirmed: CCR (raw baseline not computed), fidelity, localization.

### M3: Phase 1 — Baseline CCR ✅ COMPLETE (4/5 repos)
- Date: 2026-04-07
- Script: `experiments/runs/run_phase1_baseline.py`
- **CRITICAL FINDING: word-to-token ratio is ~3.9-4.4, NOT 1.3 as designed.**
  All clues EXCEED the 4150 token budget when measured with tiktoken.
  Design assumed 1 word ≈ 1.3 tokens. Reality: 1 word ≈ 3.9 tokens.
  This is because file paths, symbol names, and code-like identifiers tokenize
  into many sub-word tokens (e.g., "Flask.wsgi_app" = 5+ tokens, 1 word).
- **ACTION NEEDED:** Switch budget caps from words to actual tiktoken counts.
  Current word budgets produce ~2× the intended token output.
- Results (actual tiktoken tokens):
  | Repo | Raw Tokens | Clue Tokens | CCR | CCR Pass | Budget % |
  |------|-----------|-------------|-----|----------|----------|
  | Flask | 82,503 | 8,011 | 90.3% | YES | 193% |
  | httpx | 65,782 | 7,723 | 88.3% | YES | 186% |
  | Gin | 59,102 | 7,269 | 87.7% | YES | 175% |
  | FastAPI | 223,882 | 9,249 | 95.9% | YES | 223% |
  | Django | 2,682,461 | pending | pending | pending | pending |
- **Gate: CCR ≥ 0.85 for ≥ 3 repos → 4/4 PASS** ✅
- Django extraction still running (~165s+ for 45K nodes)
- Next: fix token budget enforcement, then re-run

### M4: Phase 2 — Gold Task Set ✅ COMPLETE
- Date: 2026-04-07
- Artifact: `experiments/runs/mrlf-benchmark/gold-tasks.json`
- 20 tasks: 4 repos × 5 TFs
- Each task has: question, gold_files, gold_symbols, gold_facts (3-4 each)
- Gate: 20 validated golds exist ✅

### M5: Phase 3 — Localization Scoring ✅ COMPLETE
- Date: 2026-04-07
- Script: `experiments/runs/run_phase3_localization.py`
- Results: `experiments/runs/mrlf-benchmark/phase3-localization-results.json`
- Per-task clue files: `experiments/runs/mrlf-benchmark/{task_id}.codeclue`
- Results by repo:
  | Repo | Mean Loc | Sufficient | File Recall | Sym Recall |
  |------|----------|-----------|-------------|------------|
  | FastAPI | 0.530 | 3/5 (60%) | 0.800 | 0.350 |
  | Flask | 0.590 | 2/5 (40%) | 0.950 | 0.350 |
  | Gin | 0.557 | 2/5 (40%) | 0.667 | 0.483 |
  | httpx | 0.610 | 3/5 (60%) | 1.000 | 0.350 |
- Results by TF:
  | Family | Mean Loc | Sufficient |
  |--------|----------|-----------|
  | TF1 | 0.538 | 1/4 |
  | TF2 | 0.721 | 3/4 |
  | TF3 | 0.392 | 1/4 |
  | TF4 | 0.592 | 3/4 |
  | TF5 | 0.617 | 3/4 |
- Overall: mean_loc=0.572, sufficient=10/20 (50%)
- **Gate: mean_loc ≥ 0.50: 0.572 → PASS** ✅
- **Gate: Flask loc ≥ 0.80: 0.590 → FAIL** ❌
- **Key finding:** File recall is excellent (0.80-1.00) across all repos.
  Symbol recall is the bottleneck (0.35) — the clue mentions the right files
  but the specific class/function names from gold don't appear in L2/L3.
  This is a symbol extraction + matching problem, not a format problem.

### M6: PIVOT — Symbol Recall Root Cause + Fix Cycle
- Date: 2026-04-07
- **Trigger:** Phase 3 Flask loc gate FAILED (0.590 < 0.80). Symbol recall 0.35.
- **Diagnostic:** `experiments/runs/diagnose_symbol_recall.py`
- **Three fixes applied one-at-a-time:**
  - Step 1 (Scorer): No impact. Confirmed Hyp C is negligible.
  - Step 2 (Extractor): +146 call edges, 6 symbols gained connectivity.
    But Phase 3 unchanged (0.567 vs 0.572). Symbols promoted from Hyp B→A
    (connected but still out-ranked). KEPT (no regression).
  - Step 3 (Test exclusion): Already built into renderer. Verified: 0 test 
    files in L2 SYM top lines. But production symbols like `SessionInterface`
    still rank #529 because they have 0 in-degree.
- **Remaining root cause:** PageRank rewards symbols that are CALLED BY many
  others. Classes like `SessionInterface`, `SecureCookieSession`, `AppContext`
  have high out-degree (they call things) but 0 in-degree (nothing calls them
  — they're instantiated, not called). PageRank gives them minimum rank.
  L3 FOCUS keyword anchoring can't reach them either because the graph walk
  from keyword-matched nodes doesn't connect to these disconnected classes.
- **Options to discuss with user:**
  1. Switch L2 ranking from PageRank to combined metric (in+out degree)
  2. Add L3 FOCUS fallback: if keyword matches a symbol name directly,
     include it even without graph walk connectivity
  3. Accept the limitation — these symbols are in File 2 detail store,
     accessible via drill-down
- **Current metrics (after all fixes):**
  Overall loc=0.787, sufficient=17/20, Flask loc=0.870, httpx loc=0.870
  **ALL Phase 3 gates now PASS.**

### M6b: Phase 3 Re-Run — ALL GATES PASS ✅
- Date: 2026-04-08
- Fix applied: L3 FOCUS class-priority + stemmed keyword matching + test exclusion
  (class seeds ranked first within each distance tier; stemmed keywords for fuzzy match;
  test file symbols excluded from direct name-match)
- Results (compared to pre-fix baseline):
  | Repo | Before | After | Change |
  |------|--------|-------|--------|
  | Flask | 0.570 | 0.870 | +0.300 |
  | httpx | 0.610 | 0.870 | +0.260 |
  | FastAPI | 0.530 | 0.770 | +0.240 |
  | Gin | 0.557 | 0.637 | +0.080 |
  | Overall | 0.567 | 0.787 | +0.220 |
  | Sufficient | 10/20 | 17/20 | +7 |
- Gate: mean_loc ≥ 0.50: 0.787 → **PASS** ✅
- Gate: Flask loc ≥ 0.80: 0.870 → **PASS** ✅
- Gate: httpx loc (guard): 0.870 → **No regression** ✅
- 3 remaining failures: fastapi-tf1 (DI internals), gin-tf3/tf5 (Go extractor limits)
- 38 unit tests passing

### M6c: Django Scale Test ✅ COMPLETE (5 of 5 tasks)
- Date: 2026-04-09
- Scripts: `experiments/runs/_django_full_test.py`, `experiments/runs/_profile_django_render.py`
- **Root cause of 505s render: O(N×E) linear scan in L1 INDEX.**
  `next((n for n in graph.nodes if ...))` scanned 42K nodes per edge (69K edges).
  Fix: dict lookup `node_by_id.get(edge.to_node)` → O(1) per edge.
  Result: 505s → 7.6s mean render (66× faster). NOT a hardware/parallelism issue.
- **All 5 tasks complete, all under budget:**
  | Task | Time | Tokens | Budget | Gold |
  |------|------|--------|--------|------|
  | django-tf1-settings-refactor | 5.8s | 3,824 (92%) | PASS | 3/3 |
  | django-tf2-middleware-impact | 12.6s | 3,746 (90%) | PASS | 0/3 |
  | django-tf3-admin-customization | 2.6s | 4,018 (97%) | PASS | 1/3 |
  | django-tf4-orm-query-execution | 6.8s | 3,770 (91%) | PASS | 0/3 |
  | django-tf5-csrf-protection | 10.2s | 3,749 (90%) | PASS | 1/3 |
- Total pipeline: 293s extraction + 7.6s render = ~5 min per repo (one-time)
- Phase 3 re-verified: all 20 tasks unchanged (17/20 sufficient, 0.79 overall loc)
- **Performance conclusion:** The 505s was a quadratic algorithm bug, not architectural.
  No hardware scaling or parallelism was needed. Current render is 2-13s on laptop.
  Server-client architecture decision deferred — not needed at current perf level.

### M6d: Nest TypeScript Validation ✅ COMPLETE
- Date: 2026-04-09
- Script: `experiments/runs/_nest_validation_test.py`
- **Untested repo validation: Nest (TypeScript, 1659 .ts files, 471K raw tokens)**
- Results:
  | Task | Time | Tokens | Budget | Gold Sym | Gold Files |
  |------|------|--------|--------|----------|-----------|
  | nest-tf1-module-refactor | 2.5s | 3,850 (93%) | PASS | 1/3 | 2/2 |
  | nest-tf2-middleware-impact | 2.9s | 3,514 (85%) | PASS | 2/3 | 1/2 |
  | nest-tf3-guard-integration | 3.7s | 3,766 (91%) | PASS | 2/3 | 2/2 |
  | nest-tf4-exception-handling | 1.0s | 3,826 (92%) | PASS | 2/3 | 1/2 |
  | nest-tf5-auth-security | 2.6s | 3,569 (86%) | PASS | 1/3 | 1/2 |
- All 5 tasks complete, all under budget, CCR 99.2%, mean render 2.5s
- Gold symbol recall 53% (lower than Python repos — TS extractor has fewer call edges)

### M7: Go Extractor Rewrite + Phase 4 Keyword Scoring ✅ COMPLETE
- Date: 2026-04-09
- **Go extractor rewrites (`src/codeclue_research/extract_go.py`):**
  - Doc comment extraction via `_extract_go_doc_comment()`
  - Method-on-struct detection (receiver type → class node)
  - Symbol-to-symbol call edge tracking (current_func_id → callee)
  - Panic extraction for invariant knowledge
  - Struct → class type mapping
- **Python extractor enrichment (`src/codeclue_research/extractor.py`):**
  - `ast.get_docstring()` for purpose field (replacing template "class X")
  - Class attributes via `ast.Assign` with literal values
  - Parent classes via `node.bases`
  - Raise extraction (`ast.Raise` → exception class names)
  - Import tracking (`ast.Import`/`ast.ImportFrom`)
- **Phase 4 keyword scorer results:**
  - Script: `experiments/runs/run_phase4_consumption.py`
  - DFCR = 0.650 (13/20 sufficient), DDR = 0.350
  - **Gate D5 (DFCR ≥ 0.60): PASS** ✅
  - **Gate D6 (DDR ≤ 0.40): PASS** ✅
  - TF breakdown: TF2 4/4, TF3 4/4, TF4 3/4, TF1 2/4, TF5 0/4
- **Chi (second Go repo) validation:** 3/3 tasks complete

### M8: Knowledge Type Analysis + Option E ✅ COMPLETE
- Date: 2026-04-09
- **Section 10b added to design doc** — classified all gold facts into 5 types:
  Structural, Relational, Declarative, Mechanistic, Invariant
- TF5 fails because it requires Mechanistic + Invariant — neither extracted
- **5 options evaluated (A-E):** selected Option E (Hybrid import fingerprint + raise extraction)
- **Implemented:**
  - Python: `ast.Raise` extraction, import propagation to L3 FOCUS entries
  - Go: `panic(...)` extraction via regex
  - Renderer: `raises:` line in L3 FOCUS entries
- **TF5 diagnostic:** 3/4 Python repo gold facts ARE in the clue after Option E,
  but keyword scorer can't match the wording (e.g., "signed cookies" in docstring
  but gold fact says "cryptographically signed with SECRET_KEY")

### M9: Real LLM Evaluation ✅ COMPLETE
- Date: 2026-04-10
- **7 consumer prompts built** with self-scoring format (LLM answers + scores itself)
- **Cross-model evaluation** (3 frontier models):
  | # | Task | Model | Score | Sufficient? |
  |---|------|-------|-------|-------------|
  | 1 | fastapi-tf1-dependency-injection | Gemini 3.1 Pro | 1/4 | NO |
  | 2 | fastapi-tf4-form-parsing | Gemini 3.1 Pro | 1/4 | NO |
  | 3 | gin-tf5-credential-handling | Claude Opus 4.6 | 1/4 | NO |
  | 4 | fastapi-tf5-input-validation | GPT-5.4 | 1/4 | NO |
  | 5 | httpx-tf5-redirect-security | GPT-5.4 | 3/4 | **YES** |
  | 6 | flask-tf1-refactor-sessions | GPT-5.4 | 2/4 | NO |
  | 7 | flask-tf5-session-security | GPT-5.4 | 0/4 | NO |
- **Keyword scorer accuracy:** 86% (6/7 correct, only httpx-tf5 flipped)
- **Real DFCR = 0.700** (14/20 sufficient), DDR = 0.300
- **Gates still pass:** D5 (0.700 ≥ 0.60) ✅, D6 (0.300 ≤ 0.40) ✅
- **Key finding:** Failures are genuine content gaps (Mechanistic + Invariant
  knowledge types), not scorer limitations. The format works for ~70% of tasks.

### M10: Stale Clues + Calls Truncation + Focus Relevance Fix ✅ COMPLETE
- Date: 2026-04-10
- **3 changes applied (one-at-a-time, with regression checks):**
  1. **Calls limit 5→8 + deduplication** in L3 FOCUS renderer
  2. **Regenerate all clues** — picks up Option E raises data
  3. **Keyword relevance sorting in FOCUS** — within same graph distance,
     nodes matching more question keywords are ranked first
- Cross-repo durability verified: Chi 2/2 PASS, Nest unchanged, no regressions

### M11: External Class Instantiation — `uses:` Line ✅ COMPLETE
- Date: 2026-04-10
- **New extraction: `uses:` line** for mechanistic knowledge (Root Cause A fix)
- **Python extractor changes:**
  - Build `imported_names` dict during import scanning (local_name → source_module)
  - For each function: scan `ast.Call` where callee is PascalCase imported name
  - Record as `uses: ClassName (module)` in SymbolRecord
- **Renderer changes:**
  - For classes: aggregate `uses:` from child methods via calls/contains edges
  - Render `uses:` line after `raises:` in L3 FOCUS entries
- **Key result: Flask sessions.py clue now contains:**
  ```
  SecureCookieSessionInterface (src/flask/sessions.py:284-385)
    ...
    uses: URLSafeTimedSerializer (itsdangerous)
  ```
- **Phase 3:** 19/20 sufficient (0.820), identical to pre-change — NO REGRESSION
- **Phase 4:** DFCR = **0.750 (15/20)**, DDR = 0.250
  - flask-tf5: FAIL → **PASS** (URLSafeTimedSerializer keyword match)
  - flask: 4/5 → **5/5** (all tasks pass!)
  - TF5: 0/4 → 1/4 (flask-tf5 now passes)
  - TF1: 2/4 → 3/4 (flask-tf1 improved)
- **38 unit tests pass. No regressions.**
- **Remaining 5 failures:** fastapi-tf1, fastapi-tf4, fastapi-tf5, gin-tf5, httpx-tf5
  (httpx-tf5 passes real LLM → projected real DFCR ~0.800)

### M12: Held-Out Validation ✅ COMPLETE — OVERFITTING CONFIRMED
- Date: 2026-04-10
- **7 held-out tasks created** on repos never tuned against (Django 3, Chi 2, Flask-adversarial 1, httpx-new 1)
- **Held-out gold tasks:** `experiments/runs/mrlf-benchmark/heldout-gold-tasks.json`
- **Results:** `experiments/runs/mrlf-benchmark/heldout-validation-results.json`
- **Held-out DFCR = 0.429 (3/7)**
- **Development DFCR = 0.750 (15/20)**
- **Overfitting gap = 0.321** — WARNING: >0.10 threshold
- Per-task results:
  | Task | Repo | Loc | Fid | Loc Pass | Fid Pass |
  |------|------|-----|-----|----------|----------|
  | chi-tf4-panic-recovery | chi | 0.700 | 0.750 | YES | **YES** |
  | chi-tf5-rate-limiting | chi | 1.000 | 0.625 | YES | **YES** |
  | django-tf2-middleware-chain | django | 0.267 | 0.500 | NO | NO |
  | django-tf4-password-hashing | django | 0.350 | 0.500 | NO | NO |
  | django-tf5-csrf-protection | django | 0.000 | 0.250 | NO | NO |
  | flask-tf5-adversarial | flask | 0.600 | 0.500 | YES | NO |
  | httpx-tf4-connection-pooling | httpx | 1.000 | 0.625 | YES | **YES** |
- **Key findings:**
  - Chi + httpx: 3/3 pass — format works on non-Django repos
  - Django: 0/3 pass — large repo localization is weak (0 symbol recall on tf5)
  - Flask adversarial: loc passes but fidelity 0.500 (FAIL) — keyword relevance
    sorting DOES NOT HELP when question avoids symbol names ("user state persist"
    vs "session data"). Confirms fragility of sorting fix.
  - The `uses:` extraction helped on chi/httpx but NOT on Django/Flask-adversarial

### M13: Phase 5 — Drill-Down ✅ COMPLETE
- Date: 2026-04-10
- Script: `experiments/runs/run_phase5_drilldown.py`
- Results: `experiments/runs/mrlf-benchmark/phase5-drilldown-results.json`
- **9 tasks required drill-down (fidelity < 0.60), 18 already passing**
- **Mean FU (Fidelity Uplift) = +0.222 — Gate D7 PASS (≥ 0.10)** ✅
- **7 of 9 tasks flipped FAIL → PASS with File 2 detail records**
- Per-task results:
  | Task | Clue-Only | Post-Drill | Uplift | Flipped? |
  |------|-----------|------------|--------|----------|
  | fastapi-tf1-dependency-injection | 0.500 | 0.750 | +0.250 | YES |
  | fastapi-tf4-form-parsing | 0.500 | 0.750 | +0.250 | YES |
  | fastapi-tf5-input-validation | 0.375 | 0.625 | +0.250 | YES |
  | django-tf2-middleware-chain | 0.500 | 0.750 | +0.250 | YES |
  | django-tf4-password-hashing | 0.500 | 0.750 | +0.250 | YES |
  | django-tf5-csrf-protection | 0.250 | 0.625 | +0.375 | YES |
  | flask-tf5-adversarial | 0.500 | 0.875 | +0.375 | YES |
  | httpx-tf5-redirect-security | 0.500 | 0.500 | +0.000 | NO |
  | gin-tf5-credential-handling | 0.250 | 0.250 | +0.000 | NO |
- **Post-drill blended DFCR: 25/27 = 0.926** (from 0.667 pre-drill)
- **Key findings:**
  - Django: 0/3 → 3/3 — File 2 source snippets contain the missing mechanistic detail
  - Flask adversarial: 0.500 → 0.875 — source code bridges the semantic gap
  - FastAPI: 2/5 → 5/5 — all three failures rescued by drill-down
  - Only Gin-tf5 and httpx-tf5 remain at FAIL (Go extractor + structural-only facts)
  - **The two-file architecture IS validated.** File 1 handles 67% directly;
    File 1 + File 2 drill-down handles 93%.

### M14: Adaptive Budget ⬜
- Change token ceiling from fixed 4150 to `min(8192, max(4096, n_modules * 3))`
- Blocks on: Phase 5 complete
- Expected impact: Django 0/3 → 2/3

### M15: Ensemble Retrieval ⬜
- 4-strategy FOCUS selector (symbol name, docstring, imports, file path)
- Blocks on: Phase 5 data
- Expected impact: adversarial questions recovered

### M16: Commit v0.9.0 ⬜
- Blocks on: M13-M15 complete
- All MRLF work currently uncommitted since v0.8.1

### M17+: MCP Integration (v2.0) ⬜ — ASK USER BEFORE STARTING
- `serve_mcp()` transport + `focus_query` tool (D2)
- Pointer accumulation (D4)
- Fat bundled responses (D5)
- Own evaluation protocol (not Phase 4 scorer)
- See design doc Section 12 for full architecture

---

## Forward Plan (Path A — Agreed April 10)

| Step | What | Blocks On | Gate |
|------|------|-----------|------|
| **NOW** | Phase 5 drill-down | Nothing | FU ≥ 0.10 |
| 2 | Adaptive budget | Phase 5 | No Django regression |
| 3 | Ensemble retrieval | Phase 5 | Held-out adversarial passes |
| 4 | Commit v0.9.0 | Steps 1-3 | All D1-D8 pass |
| 5 | **ASK USER** | — | Permission to start MCP |
| 6 | MCP `focus_query` + transport | User approval | System eval protocol |
| 7 | Pointer accumulation | MCP running | — |
| 8 | Held-out re-evaluation | All above | Gap < 0.10 |

---

## Current Metrics (April 10, 2026)

| Metric | Value | Confidence |
|--------|-------|------------|
| Dev DFCR (keyword) | 0.750 (15/20) | LOW (circular) |
| Held-out DFCR | 0.429 (3/7) | HIGH (unseen) |
| Blended DFCR | 0.667 (18/27) | MEDIUM |
| **Post-drill DFCR** | **0.926 (25/27)** | **MEDIUM** |
| Phase 3 loc (dev) | 0.820, 19/20 suff | HIGH |
| **Phase 5 FU** | **+0.222** | **HIGH** |
| **Gate D7** | **PASS** | — |
| Unit tests | 38 passing | HIGH |
| Overfitting gap | 0.321 (pre-drill) | — |

---

## Session Summary — April 7, 2026

### What Was Accomplished

1. **Designed MRLF format from scratch** with mathematical foundations
   (Rate-Distortion, Sufficient Statistics, Successive Refinement, MDL, Wavelet MRA).
   Full design in `docs/New-Design-Basis.md` with 50 use cases, 9 constraints,
   10 non-constraints, 7 resolved open questions, and fresh-start reconstruction guide.

2. **Implemented MRLF renderer** (`src/codeclue_research/clue_view_mrlf.py`):
   pure-Python PageRank, 4-level progressive resolution, tiktoken budget enforcement,
   detail store generator (JSONL). 38 unit tests passing.

3. **Ran 6-phase validation plan through Phase 3:**
   - Phase 1 (CCR): 4/4 repos pass ≥ 85% compression. Budget bug found and fixed
     (word-to-token ratio was 3.9×, not 1.3×).
   - Phase 2 (Gold Tasks): 20 tasks created (4 repos × 5 TFs).
   - Phase 3 (Localization): Overall loc=0.567 (PASS ≥ 0.50). Flask loc=0.570 (FAIL ≥ 0.80).

4. **Ran disciplined root cause analysis** on the Flask gate failure:
   - Diagnostic proved 75% of missing symbols caused by extractor (Hyp B), not format.
   - Applied 3 fixes one-at-a-time with regression checks. No regressions.
   - Identified fundamental PageRank limitation: classes with 0 in-degree get
     minimum rank regardless of their architectural importance.

### What Was NOT Accomplished

- Flask localization gate (≥ 0.80) not met. Currently at 0.570.
- Django scale test not completed (extraction timeout).
- Phase 4 (LLM consumption) blocked by Phase 3 gate.
- Phase 5 (drill-down) and Phase 6 (tuning) not started.
- No commit made — all work is uncommitted in working tree.

### Key Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| CCR ≥ 0.85 | ≥ 85% | 87.7–95.9% | **PASS** |
| Token budget ≤ 4150 | ≤ 4150 | 3,971 (Flask) | **PASS** (after tiktoken fix) |
| Overall mean loc ≥ 0.50 | ≥ 0.50 | 0.567 | **PASS** |
| Flask mean loc ≥ 0.80 | ≥ 0.80 | 0.570 | **FAIL** |
| Overall sufficient ≥ 65% | ≥ 13/20 | 10/20 (50%) | **FAIL** |
| File recall | high | 0.85 avg | Good |
| Symbol recall | high | 0.35 avg | **Bottleneck** |

### Root Cause Chain (Fully Diagnosed)

```
Symbol recall = 0.35
  └─ Gold symbols not in L2 SYM or L3 FOCUS
      └─ Gold symbols rank #200-600 in PageRank (budget cuts at ~89)
          └─ Gold symbols have 0 in-degree (nothing calls them)
              └─ They are CLASSES — instantiated, not called as functions
                  └─ Extractor captures ast.Call but not class instantiation
                      └─ Even after extractor fix (+146 edges), classes still
                         have 0 in-degree because Python instantiation
                         (Class(...)) resolves to __init__ not to the class node
                              └─ PageRank fundamentally rewards callees, not callers
```

### Unresolved Decision: How to Fix Symbol Recall

Three options identified, none yet implemented:

**Option 1: Replace PageRank with combined centrality for L2 ranking**
- Use `rank = in_degree + out_degree + containment_children_count`
- Pros: Classes like SessionInterface (out-degree 12) would rank higher
- Cons: Changes L2 SYM content for ALL repos and ALL tasks — must re-run
  full Phase 3 to check for regressions
- Scientific basis: Total degree centrality is task-agnostic and rewards
  architectural hub nodes regardless of call direction

**Option 2: Add direct name-match fallback to L3 FOCUS**
- If question keyword exactly matches a symbol name, include that symbol
  in FOCUS regardless of graph walk reachability
- Pros: Task-conditioned fix — only affects tasks where question mentions
  the missing symbol. Doesn't change L2 at all.
- Cons: May include disconnected symbols with no context (no callers/callees
  to show). Doesn't help if question uses different terminology than symbol name.
- Scientific basis: Keyword grounding (IR foundation) — if the user asks
  about "sessions", the clue should contain SessionInterface.

**Option 3: Accept limitation, rely on File 2 drill-down**
- Accept DDR > 0.40 for class-heavy tasks
- Pros: No changes to any component. Format works as designed.
- Cons: Fails the Flask loc gate. Phase 4 blocked indefinitely.
  The 50% sufficiency rate means half of tasks need drill-down,
  which contradicts the "clue-only for majority" design principle.

**Recommendation:** Option 2 first (lowest risk, task-conditioned, no L2 regression
possible), then Option 1 if needed (higher impact but higher risk).

---

## Forward Plan

### Immediate Next Session: Fix Symbol Recall Gate

| Step | What | Risk | Effort |
|------|------|------|--------|
| 1 | Apply Option 2: L3 FOCUS direct name-match fallback | Low | ~30 min |
| 2 | Re-run diagnostic on Flask | None | ~5 min |
| 3 | Re-run Phase 3 on all 20 tasks | None | ~30 min |
| 4 | Check: Flask loc ≥ 0.80? Overall sufficient ≥ 65%? | — | — |
| 5 | IF still failing → Apply Option 1: combined centrality for L2 | Medium | ~1 hr |
| 6 | Re-run Phase 3 again, check for regressions across all repos | — | ~30 min |

### After Symbol Recall Gate Passes

| Phase | What | Prerequisite |
|-------|------|-------------|
| Phase 1d | Run Django scale test | Need to optimise tiktoken calls for speed |
| Phase 4 | LLM consumption test (20 tasks, Arm A vs Arm B) | Phase 3 Flask gate pass |
| Phase 5 | Drill-down test on failed tasks | Phase 4 complete |
| Phase 6 | Budget tuning pass | All prior data |
| Commit | Tag as v0.9.0 | All Phase 3 gates pass |

### Definition of Done (unchanged from Section 10.8)

| # | Criterion | Threshold | Current |
|---|-----------|-----------|---------|
| D1 | CCR ≥ 0.85 for ≥ 70% of repos | ≥ 3 of 4 repos | **PASS** (4/4) |
| D2 | Django clue fits under 4150 tokens | ≤ 4150 tokens | **PASS** (90-98%) |
| D3 | Mean localization ≥ 0.50 across all repos | ≥ 0.50 | **PASS** (0.787) |
| D4 | Mean localization ≥ 0.80 on Flask | ≥ 0.80 | **PASS** (0.870) |
| D5 | DFCR ≥ 0.60 | ≥ 60% | **PASS** (0.750 keyword, ~0.800 projected LLM) |
| D6 | DDR ≤ 0.40 | ≤ 40% | **PASS** (0.250) |
| D7 | FU ≥ 0.10 for drill tasks | ≥ 0.10 | BLOCKED |
| D8 | No regression after tuning | Hold or improve | NOT STARTED |

---

## Current State

- **Git:** v0.8.1 (HEAD, ba96b3f) — MRLF files not yet committed
- **New files (uncommitted):**
  - `src/codeclue_research/clue_view_mrlf.py`
  - `tests/foundation/test_mrlf.py`
  - `experiments/runs/run_mrlf_benchmark.py`
  - `experiments/runs/run_phase1_baseline.py`
  - `experiments/runs/run_phase3_localization.py`
  - `experiments/runs/diagnose_symbol_recall.py`
  - `experiments/runs/mrlf-benchmark/*.codeclue`
  - `experiments/runs/mrlf-benchmark/*.codeclue-detail`
  - `experiments/runs/mrlf-benchmark/gold-tasks.json`
  - `experiments/runs/mrlf-benchmark/phase3-localization-results.json`
  - `docs/New-Design-Basis.md`
  - `docs/HANDOFF-SESSION-20260407.md`
- **Modified files:**
  - `src/codeclue_research/extractor.py` (class body call edges + containment)
  - `experiments/runs/run_phase3_localization.py` (scorer improvement)
- **Tests:** 38 MRLF tests passing. Existing tests not re-run (MCP import issue predates this session).
  - `experiments/runs/mrlf-benchmark/flask.codeclue`
  - `experiments/runs/mrlf-benchmark/httpx.codeclue`
  - `experiments/runs/mrlf-benchmark/gin.codeclue`
  - `experiments/runs/mrlf-benchmark/fastapi.codeclue`
  - `experiments/runs/mrlf-benchmark/*.codeclue-detail`
  - `docs/New-Design-Basis.md`
- **Tests:** 38 MRLF tests passing
- **External repos available:** django (2894 py), fastapi (1118 py), flask (83 py), httpx (60 py), gin (99 go), nest (1659 ts), typeorm (3438 ts), express (no source)
- **Django:** NOT yet extracted/rendered (expected ~165s extraction)

## Immediate Next Action

Start Phase 1 (baseline CCR) + Phase 2 (gold tasks) in parallel:
1. Build `run_phase1_baseline.py`: count raw source tokens with tiktoken, compute CCR, include Django
2. Build `gold-tasks.json`: 20 tasks with verified gold answers

## Key Design Decisions (for any resuming session)

Read `docs/New-Design-Basis.md` Section 9.4 for the 10 non-negotiable decisions.
Read Section 8 for the 7 resolved open questions.
Read Section 10 for the full execution plan with gates and Definition of Done.
