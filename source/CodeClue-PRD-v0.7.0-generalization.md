---
title: "CodeClue Research Specification: MRLF v2.1 — Generalized Behavioral Comprehension"
version: 0.7.0-research
status: RESEARCH DRAFT — Generalization plan under implementation
author: Ravi Nandagopalan
created: 2026-03-28
last_updated: 2026-04-14
document_type: Research Design Document (not a product PRD)
classification: Internal / Open Source Candidate
supersedes: CodeClue-PRD-v0.3.0-mvp-FINAL.md (v0.6.0)
---

## Changelog from v0.6.0

### v0.7.0 (2026-04-14) — Generalization Pivot

**Context:** Blind evaluation on 3 unseen repositories (aiohttp, click, fiber)
scored 1/24 (4.2%) on mechanistic gold facts. Root cause: FOCUS entries contain
structural metadata (names, signatures, call edges) but NOT behavioral content
(control flow, precedence chains, return construction). 23/24 gold facts require
method body logic that the format deliberately excluded.

**Critical finding:** Previous fix attempt (Steps 3-3b, April 14 session) fell
into the overfitting trap — `_tokenize_symbol()`, `_src_priority()`, and keyword
matching improvements were calibrated to specific repos (Click, aiohttp). Result:
aiohttp-2 went to 6/6 symbol recall while click-1 stayed at 0/6. Classic overfitting.

**This version documents the principled generalization plan developed by GPT-5.4
and Claude Opus 4.6 in collaborative analysis.**

**Key design changes:**
1. **Abandon single-file sufficiency claim** for mechanistic questions. Embrace
   two-tier: File 1 for structural/relational (≥80%), guided drill-down for mechanistic.
2. **Replace lexical FOCUS selection** with graph-structural approach: docstring
   semantic anchoring + betweenness centrality + containment expansion.
3. **Add behavioral pattern extraction** — 8 universal control flow patterns
   (GUARD, PRECEDENCE, BRANCH, DELEGATE, ACCUMULATE, TRANSFORM, UNWIND, DISPATCH)
   extracted deterministically from AST.
4. **Budget-driven rendering** — remove arbitrary 80-node cap; render until token
   budget exhausted.
5. **Enhanced GAPS** — question type classification, coverage reporting, costed
   drill-down targets.
6. **Validation framework** — proper dev/validation/blind splits with automated
   overfitting detection.

---

## 1. Abstract

CodeClue proposes a persistent, versioned comprehension layer for software
repositories, authored by deterministic extraction and optimized for downstream
LLM consumption. The central artifact is the MRLF (Multi-Resolution Lattice
Format) — a two-file clue system that compresses codebase understanding into
a ≤4K token primary file with a JSONL detail store for drill-down.

**Revised claim (v0.7.0):** MRLF v2.1 provides:
- **Structural comprehension** (≥90% accuracy) from File 1 alone
- **Relational comprehension** (≥80% accuracy) from File 1 alone
- **Mechanistic comprehension** (~35-45% from File 1 behavioral annotations,
  ~80% with File 2 drill-down)
- **Zero hallucination** on all Tier 1 content (deterministic AST extraction)
- **Explicit sufficiency boundary** — the format self-reports what it can and
  cannot answer, with costed drill-down targets

The format does NOT claim to be a sufficient statistic for all question types.
It is a sufficient statistic for structural and relational questions, and an
*informative prior* for mechanistic questions that guides efficient drill-down.

---

## 2. Research Scope

### 2.1 In Scope (unchanged from v0.6.0, plus:)
- Behavioral pattern extraction from function bodies (AST-based, deterministic)
- Graph-structural symbol selection (naming-convention agnostic)
- Generalization validation across multiple languages and repo structures
- Overfitting detection and prevention methodology

### 2.2 Out of Scope (unchanged from v0.6.0)

---

## 3. Problem Framing

### 3.1 The Compression-Sufficiency Boundary (NEW in v0.7.0)

The blind evaluation definitively establishes a boundary between knowledge types
that can and cannot be compressed into ≤4K tokens:

| Knowledge Type | Compressible? | Evidence |
|---------------|--------------|----------|
| Structural (file/module layout) | Yes — L0+L1 | 100% coverage in all tests |
| Relational (call graph, hierarchy) | Yes — L2+L3 structure | ~80% in dev evaluation |
| Declarative (signatures, docstrings) | Yes — L2+L3 metadata | ~75% in dev evaluation |
| Mechanistic (internal logic) | Partially — behavioral patterns | 4.2% without patterns (blind eval) |
| Invariant (error/security properties) | Partially — behavioral patterns | Untested at scale |

**Rate-distortion analysis:** Each mechanistic fact requires ~30-80 tokens of
behavioral description. With ~40 FOCUS entries at ~50 tokens each = 2000 tokens
of L3 budget, behavioral annotations for the most relevant symbols are feasible
within the 4K ceiling.

**Minimum Description Length (MDL):** A method's behavioral mechanism has
Kolmogorov complexity bounded below by its control flow complexity. Our behavioral
pattern vocabulary compresses this to ~30-50 tokens by abstracting to universal
patterns (PRECEDENCE, GUARD, etc.) — a legitimate lossy compression that preserves
structural mechanism but not specific content values.

### 3.2 The Selection Generalization Problem (NEW in v0.7.0)

FOCUS selection must identify task-relevant symbols without depending on:
- Symbol naming conventions (snake_case, camelCase, Hungarian, abbreviated, non-English)
- Directory structure (`src/`, flat, deeply nested)
- Documentation quality (well-documented vs. undocumented)

**Solution:** Graph-structural selection using:
1. Semantic anchoring on docstring/purpose content (not name syntax)
2. Containment expansion (class ↔ methods)
3. Betweenness centrality in task subgraph (topological, not lexical)
4. Graceful degradation to PageRank for undocumented code

---

## 4. Core Claims and Hypotheses

### 4.1 Revised Claim Set (v0.7.0)

C1. Token efficiency: unchanged (≥80% reduction).
C2. **REVISED** Comprehension fidelity: File 1 alone achieves ≥80% on structural/
    relational questions. Mechanistic fidelity requires behavioral annotations
    (target: ≥35% from File 1) or File 2 drill-down (target: ≥80%).
C3. Update robustness: unchanged.
C4. Practicality: unchanged.
C5. **REVISED** Gap awareness: Enhanced GAPS section correctly classifies question
    types and provides costed drill-down targets with ≥80% accuracy.
**C6. (NEW) Generalization:** Format performance does not degrade by >10 percentage
    points between development and validation repository sets, measured per
    knowledge type.
**C7. (NEW) Behavioral coverage:** AST-extracted behavioral patterns are present
    for ≥60% of FOCUS functions across all tested languages.

### 4.2 Updated Hypotheses

H1-H7: unchanged from v0.6.0.

**H8 (Behavioral annotation impact):** Adding behavioral pattern annotations to
FOCUS entries raises mechanistic fact coverage by ≥25 percentage points on
validation repos compared to structural-only FOCUS.
Null H8_0: Improvement is < 25pp.

**H9 (Selection generalization):** Graph-structural FOCUS selection achieves
≥50% gold symbol recall on validation repos, with no more than 10pp variation
between repos.
Null H9_0: Recall < 50% or variation > 10pp between repos.

**H10 (Cross-language behavioral extraction):** Behavioral pattern extraction
produces annotations for ≥60% of FOCUS functions in Python, Go, and TypeScript.
Null H10_0: Annotation rate < 60% in any language.

---

## 5. MRLF v2.1 Format Design

### 5.1 File 1 (.codeclue) — Primary Clue (≤4150 tokens)

```
=CC v2.1 <repo>@HEAD <N>mod <M>sym
? <question>

-- TREE          (L0: directory structure, ~150 tokens)
-- INDEX         (L1: module listing + top exports, ~400 tokens)
-- SYM           (L2: PageRank-ranked symbol table, ~1500 tokens)
-- FOCUS         (L3: task-conditioned detail WITH behavioral patterns, ~2000 tokens)
-- GAPS          (sufficiency classification + costed drill targets, ~100 tokens)
```

### 5.2 FOCUS Entry Schema (v2.1 — with behavioral annotation)

```
symbol_name (file:line_start-line_end)
  purpose/docstring (first meaningful sentence)
  sig: signature
  behavior: PATTERN(detail); PATTERN(detail)     ← NEW in v2.1
  extends: parent_class (for classes)
  attrs: class_attributes (for classes)
  methods: public_methods (for classes)
  calls: direct_callees
  called_by: callers
  raises: exception_classes
  uses: external_classes_used
```

### 5.3 Behavioral Pattern Vocabulary (NEW in v2.1)

| Pattern | Meaning | AST Detection |
|---------|---------|---------------|
| `GUARD(condition)` | Early return/raise on condition | `if` at function start + return/raise |
| `PRECEDENCE(a, b, c)` | Tries sources in order | Sequential `if/elif` with returns |
| `BRANCH(condition, then, else)` | Conditional with distinct paths | `if/else` with significant bodies |
| `DELEGATE(target)` | Single call + return | Body is one call wrapped in return |
| `ACCUMULATE(loop)` | Loop building up a result | `for`/`while` with accumulator |
| `TRANSFORM(input → output)` | Data transformation | Assignment chain / pipeline |
| `UNWIND(collection)` | Reverse iteration / cleanup | `reversed()`, `defer`, `finally` |
| `DISPATCH(key)` | Lookup handler by key + delegate | Dict/map lookup + call |

**Properties:**
- Deterministic: same code → same patterns (AST-extracted, no LLM)
- Language-agnostic output: patterns are universal; extractors are per-language
- Compact: ~30-50 tokens per annotation
- Verifiable: each pattern maps to source anchors

### 5.4 Enhanced GAPS Section (v2.1)

```
-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 12/18 task-relevant symbols in L3, 8 with behavior annotations
uncovered: Group.parse_args, Group.resolve_command, Group.invoke
drill: core.py:1850-1920 (~70 lines, Group dispatch chain)
drill: decorators.py:1-50 (~50 lines, command/group setup)
```

### 5.5 FOCUS Selection Algorithm (v2.1 — Graph-Structural)

**Removed (v2.0 artifacts):**
- `_tokenize_symbol()` — naming-convention specific
- `_src_priority()` — directory-structure specific
- `_kw_overlap()` — lexical name matching
- English stemming heuristics
- Fixed 80-node cap

**New pipeline:**
1. Extract question keywords (unchanged — operates on question text, not code)
2. **Semantic anchoring:** Score each node's docstring/purpose against question keywords
3. **Containment expansion:** Class anchored → add methods; method anchored → add class
4. **Call-graph expansion:** 2-hop bidirectional from anchors
5. **Ranking:** Semantic overlap (primary) + betweenness centrality (secondary)
6. **Budget-driven cap:** Render until L3 token budget exhausted (no arbitrary node count)
7. **Fallback:** No anchors found → global PageRank (correct for undocumented code)

---

## 6. Validation Framework (NEW in v0.7.0)

### 6.1 Repository Splits

| Split | Repos | Purpose |
|-------|-------|---------|
| Dev | flask, httpx, gin, click | Iterate freely |
| Validation | aiohttp, fiber | Tune hyperparameters; never examine source for debugging |
| Blind | TBD (3+ new repos) | One-time final evaluation |

### 6.2 Gold Task Protocol

Per repo: 2 structural + 2 relational + 2 mechanistic tasks.
Each fact: statement + file:lines evidence + knowledge_type + expected_answerable_tier.

### 6.3 Overfitting Detection

After every code change:
- Compute Dev accuracy and Validation accuracy per knowledge type
- If Dev − Validation > 10pp → **revert, the change is overfitting**

### 6.4 Statistical Reporting

Every result includes: point estimate, Wilson 95% CI, sample size, split identity,
language breakdown. Minimum publishable: 60 facts across ≥3 languages.

---

## 7. Experimental Results

### 7.1 Baseline (Pre-Generalization)

| Split | Knowledge Type | Covered | Total | Accuracy | 95% CI |
|-------|---------------|---------|-------|----------|--------|
| Dev (click) | Mechanistic | 0 | 12 | 0.0% | [0.0%, 24.3%] |
| Validation (aiohttp, fiber) | Mechanistic | 1 | 32 | 3.1% | [0.6%, 15.7%] |

**Note:** All existing gold facts are mechanistic. Structural/relational gold tasks
not yet created. No overfitting detected (dev ≤ validation).

### 7.2 Post-Generalization (TBD)

_To be populated after Actions 1-4 are implemented and evaluated._

---

## 8. Commercial Viability Assessment (NEW in v0.7.0)

### 8.1 Value Proposition

"Pre-computed codebase understanding that eliminates cold-start latency and provides
deterministic structural answers, with guided drill-down for deep questions."

### 8.2 Minimum Viable Accuracy

| Knowledge Type | File 1 Only | With File 2 | Status |
|---------------|-------------|-------------|--------|
| Structural | ≥85% | ≥95% | On track |
| Relational | ≥70% | ≥90% | On track |
| Mechanistic | ≥30% | ≥70% | Blocked (4.2% → target 30%+) |

### 8.3 Competitive Positioning

| Alternative | Strength | CodeClue Advantage |
|-------------|----------|-------------------|
| Full RAG | Higher accuracy | 5× fewer tokens, deterministic, structured |
| Tree-sitter + embeddings | Good localization | Deeper comprehension, behavioral patterns |
| Agentic browsing | High accuracy | Pre-computed (instant), cheaper, reproducible |

---

## Appendices

### Appendix G: Behavioral Pattern Coverage Analysis

Mapping of blind eval gold facts to extractable behavioral patterns:

| Task | Fact | Pattern | Extractable? |
|------|------|---------|-------------|
| click-2 | consume_value precedence | PRECEDENCE | Yes |
| click-2 | type_cast_value branches | BRANCH | Yes |
| click-2 | Choice.convert normalize | TRANSFORM | Partial |
| click-2 | File.convert lazy + Path | DELEGATE+GUARD | Yes |
| aiohttp-1 | read accumulation + guard | ACCUMULATE+GUARD | Yes |
| aiohttp-1 | json mimetype guard | GUARD+DELEGATE | Yes |
| aiohttp-1 | post empty for non-POST | GUARD | Yes |
| aiohttp-1 | multipart tempfile stream | ACCUMULATE | Partial |
| aiohttp-2 | startup/shutdown wiring | DELEGATE | Yes |
| aiohttp-2 | cleanup fallback | GUARD+DELEGATE | Yes |
| aiohttp-2 | accepts generators/ctx mgrs | BRANCH | Partial |
| aiohttp-2 | reverse unwind multi-error | UNWIND | Yes |
| fiber-1 | Path mutates URI | TRANSFORM | Partial |
| fiber-1 | RestartRouting reset+next | DELEGATE | Yes |
| fiber-1 | next scans treeStack | DISPATCH | Partial |
| fiber-1 | 404 vs 405 method match | BRANCH | Yes |
| fiber-2 | recover defer/recover | GUARD | Yes |
| fiber-2 | DefaultPanicHandler | BRANCH | Yes (COVERED) |
| fiber-2 | Constructor installs handler | GUARD+DELEGATE | Yes |
| fiber-2 | ErrorHandler prefix search | DISPATCH | Yes |
| click-1 | command decorator | TRANSFORM | Yes |
| click-1 | group defaults to Group | DELEGATE | Yes |
| click-1 | add_command stores in map | TRANSFORM | Yes |
| click-1 | parse_args/resolve/invoke | DISPATCH | Yes |

**Summary:** 20/24 fully extractable, 4/24 partial. Theoretical ceiling: ~83%.

### Appendix H: Anti-Patterns Register

Patterns that led to wasted effort in prior sessions:

1. Repo-specific heuristics (`_src_priority`, `_tokenize_symbol` tuning)
2. Celebrating Dev accuracy without Validation confirmation
3. Magic numbers without information-theoretic justification
4. Testing on training data (examined repo ≠ blind repo)
5. Lexical tricks (stemming, substring matching) as proxies for relevance
6. Claiming File 1 sufficiency for mechanistic questions

---

*End of PRD v0.7.0*
