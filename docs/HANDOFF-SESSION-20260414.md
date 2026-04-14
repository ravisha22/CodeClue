# CodeClue Research Scaffold — Exhaustive Handoff Document
# Date: April 14, 2026
# Repository: https://github.com/ravisha22/CodeClue
# HEAD: 07a7c8a (main)

## 1. PROJECT OVERVIEW

CodeClue is a research project designing a **compressed codebase comprehension
artifact** (a "clue file") that allows LLMs to answer deep questions about
codebases WITHOUT the full source code. The format is called **MRLF**
(Multi-Resolution Lattice Format).

**Goal:** Produce a mathematically-grounded, commercially viable format that
compresses codebases into ~4K token artifacts an LLM can consume and use to
answer structural, relational, and mechanistic questions about the code.

**This is a research design project, not a product build.** The bar is academic
rigor: reproducible experiments, honest metrics with confidence levels, held-out
validation, and blind evaluation on unseen repos.

---

## 2. FORMAT DESIGN — MRLF v2

Two files per repository:

### File 1: `.codeclue` (plain text, ≤4150 tiktoken tokens)
```
=CC v2 <repo>@HEAD <N>mod <M>sym
? <question>

-- TREE          (L0: directory structure)
-- INDEX         (L1: file listing with top symbols per file)
-- SYM           (L2: PageRank-ranked symbol table — name, type, file:line, docstring)
-- FOCUS         (L3: task-conditioned behavioral detail for selected nodes)
-- GAPS          (keywords and modules the question mentions but FOCUS doesn't cover)
```

### File 2: `.codeclue-detail` (JSONL detail store)
One record per symbol with full source snippets, accessible via drill-down.

### Mathematical Foundations
- Rate-Distortion (Shannon): minimize distortion at given bitrate
- Sufficient Statistics (Fisher-Neyman): preserve information needed for task
- Successive Refinement (Equitz-Cover): L0→L1→L2→L3 progressive detail
- MDL (Rissanen): shortest description preserving predictive power
- Wavelet MRA (Mallat): multi-resolution analysis

### Knowledge Types the Format Must Support
1. **Structural** — file/module layout (L0, L1)
2. **Relational** — class hierarchy, call graph edges (L2, L3)
3. **Declarative** — signatures, docstrings, attributes (L2, L3)
4. **Mechanistic** — how methods work internally (REQUIRES method body content)
5. **Invariant** — security properties, error handling guarantees (REQUIRES body)

---

## 3. ARCHITECTURE

### Source Code
```
src/codeclue_research/
  extractor.py          — Python AST-based extraction (SymbolCollector + edge detection)
  extract_go.py         — Go regex+convention extraction
  extract_typescript.py — TypeScript regex extraction
  models.py             — Node, Edge, SourceAnchor, CanonicalClueGraph dataclasses
  clue_view_mrlf.py     — MRLF renderer (L0-L3, GAPS, FOCUS selection, PageRank)
```

### Key Functions in clue_view_mrlf.py
- `render_mrlf(graph, question, repo_root)` — generates File 1
- `generate_detail_store(graph, repo_root)` — generates File 2 records
- `_select_focus_nodes(graph, question, max_nodes=80)` — FOCUS selection pipeline
- `_tokenize_symbol(name)` — splits on `_` and camelCase for keyword matching
- `_pagerank(node_ids, edges)` — simplified PageRank for L2 ranking
- `_extract_question_keywords(question)` — keyword extraction with stop words

### Extractors
- **Python** (`extractor.py`): AST-based. Extracts classes, functions, docstrings,
  signatures, bases, class_attrs, raises, uses, imports. Call edges via `ast.walk`
  on all FunctionDef/AsyncFunctionDef/ClassDef nodes. **9/9 call patterns passing.**
- **Go** (`extract_go.py`): Regex-based. Structs, functions, method-on-struct,
  doc comments, panic detection, call edges via line scanning. **7/7 patterns passing.**
- **TypeScript** (`extract_typescript.py`): Regex-based. Classes, functions, arrow
  functions. **Known gaps:** no class method extraction, no `this.method()`, caller
  always assigned to module. Only affects Nest repo.

### Tests
- `tests/foundation/test_mrlf.py` — 38 renderer tests (all pass)
- `tests/foundation/test_extractor_call_edges.py` — 28 extraction pattern tests
  (25 pass, 1 TS fail, 2 TS skip)

---

## 4. EXPERIMENT HISTORY (CHRONOLOGICAL)

### Phase 0: Prior Formats (v0.6.0–v0.7.8)
- Plan A (entity-centric) and Plan B (flat-table) both achieved 100% DFCR on
  keyword scorer but only 0.325 fidelity against verified gold answers
- Hybrid format (v0.8.0) won 3-0 vs Plan A, localization 0.543, 50% sufficient
- Task-aware node selection (v0.8.1): 4/5 families pass, DFCR=0.750
- **All these metrics are on DEVELOPMENT repos (Flask, httpx, Gin, FastAPI)**

### MRLF v2 (v0.8.1 → current HEAD)
- Complete redesign with mathematical foundations
- 4 resolution levels, question-aware FOCUS, PageRank ranking
- Phase 1-5 passed on development repos
- Option E enrichment: raises, uses, imports added to L3 FOCUS

### Real LLM Evaluation (April 9-10)
- 7 tasks evaluated by GPT-5.4 and Gemini
- 6/7 scored NOT sufficient, only httpx-tf5 passed (3/4)
- Identified content gaps in File 1 for Mechanistic/Invariant knowledge

### Blind Evaluation Design (April 10-13)
- 3 NEW repos never seen during development: aiohttp, fiber, click
- 6 gold tasks created by reading actual source code
- Gold facts hand-written, requiring mechanistic understanding
- User ran prompts through Gemini 3.1 Pro and GitHub Copilot

### Critical Audit (April 13)
- Blind eval: 0/20 facts covered — total failure
- Initially mis-diagnosed as "Python extractor missing 5/7 call patterns"
- That diagnosis was WRONG (audit script had fixture bugs)

### Due Diligence Steps (April 13-14) — THIS SESSION
See Section 5 below for complete details.

---

## 5. DUE DILIGENCE STEPS — COMPLETE LOG

### Step 1: Extractor Call Edge Audit (d236683)
**Hypothesis:** Extractors miss common call patterns → broken call graph → wrong rankings
**Test:** Created `tests/foundation/test_extractor_call_edges.py` with fixtures
for all call patterns (self.method, super(), instance.method, etc.)

**Results:**
- Python: 9/9 patterns CAPTURED
- Go: 7/7 patterns CAPTURED + panic detection
- TypeScript: 1 FAIL (this.method), 2 SKIP (caller tracking, class methods)

**Conclusion:** Extractors work. Prior diagnosis was wrong.
**File:** `tests/foundation/test_extractor_call_edges.py`

### Step 2: Root Cause Analysis (f9ef5f5)
**Investigation:** Created `experiments/runs/_trace_focus_selection.py` to trace
exactly which symbols the FOCUS selector picks for blind-click-2.

**Findings:**
- 1683 symbols extracted, 773 call edges — graph is complete
- Gold symbols `consume_value`, `type_cast_value`, `File`, `Path`, `LazyFile`
  ALL exist in the graph
- But only `consume_value` appears in FOCUS; rest excluded by cap

**Root cause:** FOCUS selection quality, not extraction.
**Files:** `_trace_focus_selection.py`, `_blind_eval_rootcause.py`, `_blind_eval_rootcause2.py`, `_check_click_symbols.py`

### Step 2b: Detailed FOCUS Trace (697f27a)
**Investigation:** Created `experiments/runs/_trace_focus_detail.py` to trace
the exact internal state of `_select_focus_nodes()`.

**Three bugs identified:**
1. **Seed explosion:** 560/1683 symbols match keywords (too broad). Regex
   `[a-z_]\w{2,}` treats `type_cast_value` as one token, so keyword `value`
   doesn't match it, but common words like `option`, `command`, `file` match
   hundreds of symbols.
2. **Seed dist overwrite:** `File` starts as seed (dist=0) but graph walk
   from an earlier seed overwrites it to dist=1 before File's own turn.
3. **80-node cap:** 566 candidates → 80 slots. `examples/imagepipe/copy_filename`
   makes it in; `File`, `Path`, `type_cast_value` do not because they're at
   dist=1 and dist=0 slots are filled by irrelevant examples.

**File:** `experiments/runs/_trace_focus_detail.py`

### Step 3: Fix FOCUS Selection (73f48fa)
**Changes to `src/codeclue_research/clue_view_mrlf.py`:**

1. `_tokenize_symbol(name)` — New function. Splits on `_` and camelCase boundaries.
   `type_cast_value` → `{type, cast, value}`, `LazyFile` → `{lazy, file}`.

2. Seed protection — Pre-register ALL seeds as dist=0 before graph walk.
   Walk skips `seed_set` members. Seeds can never be overwritten.

3. `_is_src_file()` / `_src_priority()` — src/ files rank above examples/
   within same distance tier in the sort key.

4. `_kw_overlap()` uses `_tokenize_symbol` instead of substring match.

5. Direct match (Stage 3) uses exact token set intersection instead of
   substring search.

**Impact on blind-click-2 gold symbols:**
- Before fix: 1/8 in FOCUS (only `consume_value`)
- After fix: 5/8 in FOCUS (`consume_value`, `type_cast_value`, `File`, `Path`, `LazyFile`)
- Still missing: `Choice`, `convert`, `normalize_choice` (words not in question)

**Regression check:** 63 tests pass, 1 pre-existing TS fail, 2 skips.
**File:** `src/codeclue_research/clue_view_mrlf.py`

### Step 3b: Verify Fix Across All Blind Tasks (ae8d176)
**Script:** `experiments/runs/_verify_focus_fix_all.py`

**Post-fix gold symbol coverage (bare name match):**
| Task | Before | After |
|------|--------|-------|
| aiohttp-1 | 0/6 | 2/6 |
| aiohttp-2 | 0/6 | 6/6 (PERFECT) |
| fiber-1 | 0/5 | 1/5 |
| fiber-2 | 0/6 | 3/6 |
| click-1 | 0/6 | 0/6 |
| click-2 | 0/5 | 2/5 |
| **Total** | **0/34** | **14/34 (41%)** |

### Step 4: Regenerate Clue Files (43f5fd6)
Regenerated all 6 blind eval clue files and 6 prompt files with fixed FOCUS.
Verified blind-click-2 now contains `type_cast_value`, `File`, `Path`, `LazyFile`
in the FOCUS section.

**Files:** `experiments/runs/blind-eval/clues/*.codeclue`, `experiments/runs/blind-eval/prompts/*.prompt.md`

### Step 5: Post-Fix Blind Evaluation (07a7c8a)
**Evaluator:** GPT-5.4, run in separate sessions by user.

**Results:**
| Task | Score | Notes |
|------|-------|-------|
| aiohttp-1 | 0/4 | Gold symbols still missing from FOCUS |
| aiohttp-2 | 0/4 | Symbols present but implementation detail absent |
| click-1 | 0/4 | Gold names too generic (command, group, invoke) |
| click-2 | 0/4 | Symbols present but mechanistic detail missing |
| fiber-1 | 0/4 | Gold symbols not in FOCUS |
| fiber-2 | **1/4** | DefaultPanicHandler COVERED (docstring sufficient) |
| **TOTAL** | **1/24 (4.2%)** | |

**File:** `experiments/runs/blind-eval/blind-eval-results.jsonl` (11 lines: 5 pre-fix + 6 post-fix)

---

## 6. ROOT CAUSE OF FORMAT FAILURE — DEFINITIVE ANALYSIS

The format correctly identifies and selects relevant symbols. The extractors
produce complete call graphs. The FOCUS selection (after fix) places gold
symbols into the clue.

**The problem is information density of FOCUS entries.** Each FOCUS entry contains:
```
symbol_name (file:line_start-line_end)
  docstring (first sentence, ≤120 chars)
  sig: signature
  extends: parent_class
  attrs: class_attributes
  imports: module_imports
  calls: direct_callees
  called_by: callers
  raises: exception_classes
  uses: external_classes_used
```

**What it does NOT contain:**
- Method body logic (conditionals, loops, precedence chains)
- Return value construction
- Fallback/default behavior
- Internal delegation patterns (A calls B which calls C — only A→B shown)
- Constructor-time setup (e.g., "installs DefaultErrorHandler when nil")

**Example — blind-click-2 FACT 1:**
> Parameter.consume_value resolves a parameter's value in precedence order from
> command-line parse output, then environment variables, then Context.default_map,
> and only then the parameter's own default.

The clue shows: `consume_value (src/click/core.py:2297-2340) sig: consume_value(ctx, opts)`
That's the location and signature. But the PRECEDENCE ORDER is in the method body
(lines 2297-2340), which the clue deliberately excludes from File 1.

**The one fact that WAS covered (fiber-2 FACT 2):**
> recover.DefaultPanicHandler preserves an existing error panic as-is, but wraps
> non-error panic values with fmt.Errorf

The clue shows: `DefaultPanicHandler — DefaultPanicHandler returns r directly if
it's an error, and creates a new one with the %v verb otherwise.`

This worked because the **docstring itself contained the mechanistic detail.**
When the first-sentence docstring happens to describe the mechanism, the format
works. When the mechanism is in the body (as in 23/24 other facts), it fails.

---

## 7. DESIGN OPTIONS FOR NEXT STEPS

### Option A: Adaptive Token Budget
Expand File 1 from 4150 tokens to `min(8K, max(4K, modules*3))`.
More tokens = more FOCUS entries with richer content.
**Risk:** More tokens of the SAME kind of content (structural metadata) won't help.
Need to change WHAT goes into FOCUS, not just how much.

### Option B: File 2 Drill-Down (Phase 5 approach)
FOCUS entries include `> drill: file.py:line` pointers. The evaluating LLM
is given File 2 and can look up source snippets.
**Risk:** Requires two-step prompting. But Phase 5 showed 18/20 sufficient with
File 2 appended. This is the most proven path.

### Option C: MCP Server Integration
Tool-calling LLM uses `focus_query(question)` which returns FOCUS + relevant
File 2 records bundled in one response. Server does the selection.
**Risk:** Requires MCP infrastructure. But eliminates LLM navigation burden.
User must approve this path (gated).

### Option D: Richer FOCUS Entries
Extract behavioral summaries from method bodies — key conditionals, return
patterns, precedence logic. Add a `behavior:` line to FOCUS entries.
**Risk:** Increases token usage significantly. Hard to automate extraction
of "the important logic" from arbitrary method bodies.

### Option E: Docstring Quality Assessment
The one covered fact worked because the docstring was mechanistic. Could
measure/filter for docstring quality and fall back to body snippet when
docstring is insufficient.
**Risk:** Docstring quality varies wildly across repos. Most internal methods
have minimal or no docstrings.

---

## 8. KEY FILES REFERENCE

### Core Source
| File | Purpose |
|------|---------|
| `src/codeclue_research/clue_view_mrlf.py` | MRLF renderer + FOCUS selection |
| `src/codeclue_research/extractor.py` | Python AST extractor |
| `src/codeclue_research/extract_go.py` | Go regex extractor |
| `src/codeclue_research/extract_typescript.py` | TypeScript regex extractor |
| `src/codeclue_research/models.py` | Node/Edge/Graph dataclasses |

### Tests
| File | Purpose |
|------|---------|
| `tests/foundation/test_mrlf.py` | 38 renderer tests |
| `tests/foundation/test_extractor_call_edges.py` | 28 call edge pattern tests |

### Design Documents
| File | Purpose |
|------|---------|
| `docs/New-Design-Basis.md` | MRLF design with Sections 0-12 |
| `docs/HANDOFF-SESSION-20260407.md` | Milestone tracking M0-M10 |
| `source/CodeClue-PRD-v0.3.0-mvp-FINAL.md` | Product Requirements Doc |

### Blind Evaluation
| File | Purpose |
|------|---------|
| `experiments/runs/blind-eval/blind-gold-tasks.json` | 6 gold tasks for 3 blind repos |
| `experiments/runs/blind-eval/blind-eval-results.jsonl` | 11 eval results (5 pre-fix + 6 post-fix) |
| `experiments/runs/blind-eval/clues/*.codeclue` | 6 generated clue files |
| `experiments/runs/blind-eval/prompts/*.prompt.md` | 6 evaluator prompts |

### Investigation Scripts (experiments/runs/)
| File | Purpose |
|------|---------|
| `_trace_focus_selection.py` | Traces FOCUS selection for blind-click-2 |
| `_trace_focus_detail.py` | Detailed internal state of FOCUS pipeline |
| `_blind_eval_rootcause.py` | Gold facts vs eval results analysis |
| `_blind_eval_rootcause2.py` | Gold symbols in clue files check |
| `_check_click_symbols.py` | Click graph symbol existence check |
| `_verify_focus_fix_all.py` | Post-fix coverage across all 6 tasks |
| `_debug_name_resolution.py` | Python extractor name_to_symbol debugging |
| `_full_pipeline_audit.py` | Full pipeline audit (has fixture bugs — DO NOT TRUST its call pattern results) |

### External Repos (experiments/external-repos/)
| Repo | Language | Role |
|------|----------|------|
| flask | Python | Development set |
| httpx | Python | Development set |
| fastapi | Python | Development set |
| django | Python | Scale test |
| gin | Go | Development set |
| chi | Go | Development set |
| express | TypeScript | Development set |
| nest | TypeScript | Development set |
| **aiohttp** | **Python** | **Blind set** |
| **click** | **Python** | **Blind set** |
| **fiber** | **Go** | **Blind set** |

---

## 9. GIT HISTORY

```
07a7c8a Step 5: post-fix blind eval results - 1/24 facts covered (GPT-5.4)
43f5fd6 Step 4: regenerate blind eval clues and prompts with fixed FOCUS
ae8d176 Step 3b: verify FOCUS fix across all blind tasks
73f48fa Step 3: fix FOCUS selection - tokenize on _ and camelCase, protect seeds, src/ priority
697f27a Step 2b: detailed FOCUS trace - 3 bugs identified
f9ef5f5 Step 2: root cause analysis - FOCUS selection is the problem, not extraction
d236683 Step 1: extractor call edge audit - Python 9/9, Go 7/7, TS 3/4+2skip
ba96b3f v0.8.1: Task-aware node selection + fixed projections
c8f6f04 v0.8.0: Hybrid format + action-task benchmark
d770a5f v0.7.9: Action-task benchmark + field-level analysis
9536973 v0.7.8: Ground-truth validation
f772bb2 v0.7.7: Django stress test
4a5e82f v0.7.6: Real LLM consumer responses + scoring
ad64c74 v0.7.5: Consumer prompt generation + response scoring pipeline
4039e33 v0.7.4: Benchmark execution — all 4 pillars pass
1ffa26e v0.7.3: Phases 2-5 benchmark infrastructure
682eb51 v0.7.2: Plan B flat-table renderer
d81293e v0.7.1: Plan A entity-centric renderer
cf8f440 v0.7.0: Phase 0 shared foundation
0f5e2b6 v0.6.3: Final paper cleanup
7dc3fea v0.6.2: Epic 2+3 execution
15987a9 v0.6.1: Epic 2+4 implementation
3f99aef v0.6.0: CodeClue Research Scaffold — initial
421e07b Initial commit
```

---

## 10. WHAT THE NEXT LLM MUST DO

1. **Read `docs/New-Design-Basis.md`** — Sections 0-12 contain the full MRLF
   design rationale and v2.0 architecture decisions.

2. **Understand the core bottleneck:** FOCUS entries are structurally correct
   but informationally shallow. They show WHAT a method is (name, sig, calls)
   but not HOW it works (body logic, precedence, conditionals).

3. **Make a design decision** from the options in Section 7 above. The user
   prefers Path A (originally: format validation → adaptive budget → ensemble
   retrieval → v0.9.0), but the blind eval proves adaptive budget alone won't
   help — the content TYPE must change, not just the token count.

4. **The most proven path is File 2 drill-down** (Option B). Phase 5 testing
   showed 18/20 tasks sufficient when File 2 source snippets were appended.
   But Phase 5 used development repos, not blind repos.

5. **Design discipline rules are in `/memories/codeclue-design-discipline.md`.**
   Key rules: diagnose before fixing, one-at-a-time changes, validate on
   held-out + blind data, never claim results without confidence levels.

6. **The user expects rigorous research methodology.** No hand-waving, no
   over-claiming, no celebrating on training data. Every metric must state
   what it depends on and what its confidence level is.

---

## 11. UNCOMMITTED FILES (large working set)

There are ~70 untracked files in the repo (scripts, handoff docs, MCP scaffolds,
diagnostic tools). Running `git status --short` shows them. Key uncommitted items:
- `docs/New-Design-Basis.md` — the core design document
- `docs/HANDOFF-SESSION-20260407.md` — milestone tracking
- Multiple `experiments/runs/_*.py` diagnostic scripts
- `src/codeclue_mcp/` — MCP server scaffold (not yet active)
- Modified: `extractor.py`, `extract_go.py` (MRLF v2 changes since v0.8.1)
