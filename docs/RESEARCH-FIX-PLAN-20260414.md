# CodeClue Research Fix Plan — Principled Design for Generalization

**Date:** 2026-04-14  
**Authors:** Claude Opus 4.6 (research design), GPT-5.4 (evaluation partner)  
**Status:** Proposal — requires researcher approval before implementation  
**Supersedes:** All prior repo-specific patches (Steps 3–3b of the April 14 session)

---

## Executive Summary

The blind evaluation (1/24 = 4.2%) reveals a **fundamental information-theoretic gap**, not a software bug. The MRLF format currently captures a *structural skeleton* (what exists, what calls what) but discards *behavioral content* (how things work internally). 23 of 24 gold facts require behavioral content that lives in method bodies — content the format deliberately excludes from File 1.

This plan proposes five principled changes grounded in information theory, graph theory, and statistical methodology. Every change passes the **unseen repo test**: "Would this work identically on a repository in a language I haven't tested, with naming conventions I've never seen?"

**Key insight:** The format's claimed theoretical foundation — that File 1 is a sufficient statistic — is provably false for mechanistic questions. Rather than patching around this impossibility, we embrace it: File 1 becomes an *index with behavioral annotations*, and the system explicitly acknowledges what requires drill-down. The commercial value proposition shifts from "answer everything from 4K tokens" to "answer 70% from 4K tokens, and *know exactly where to look* for the other 30%."

---

## Part I: PRINCIPLES

### Principle 1: The Behavioral Gap Is Information-Theoretic, Not Algorithmic

**Claim:** No selection algorithm, no matter how sophisticated, can make mechanistic facts answerable from the current FOCUS entry format.

**Proof sketch:** Consider blind-click-2 FACT 1: *"Parameter.consume_value resolves a parameter's value in precedence order from command-line parse output, then environment variables, then Context.default_map, and only then the parameter's own default."*

The FOCUS entry for `consume_value` currently contains:
```
consume_value (src/click/core.py:2297-2340)
  sig: consume_value(ctx, opts)
  calls: resolve_envvar_value, ...
  called_by: ...
```

The **precedence order** is encoded in the control flow of lines 2297–2340 — specifically in the sequence of `if` statements and their short-circuit returns. This information has **zero representation** in the current FOCUS schema. The schema captures the *call graph* (what `consume_value` calls) but not the *control flow graph* (the order and conditions under which those calls happen).

**Rate-distortion estimate:** Each mechanistic fact requires ~30–80 tokens of behavioral description (a conditional chain, a return pattern, a delegation sequence). With ~80 FOCUS slots at ~25 tokens each = 2000 tokens of L3 budget, we can fit behavioral annotations for ~25–40 symbols if we compress to ~50 tokens/symbol. This is feasible within the 4K ceiling if behavioral annotations *replace* some of the current structural redundancy.

**The unseen repo test:** This analysis depends only on information theory (a method's behavior is encoded in its body, not its signature). It holds for any language, any naming convention, any codebase.

---

### Principle 2: Selection Must Be Graph-Structural, Not Lexical

**Claim:** Any selection algorithm that depends on matching question keywords against symbol names will fail on codebases where naming conventions don't align with natural language.

**Evidence from the session:**
- `_tokenize_symbol()` was tuned to handle `type_cast_value` (underscore-split) and `LazyFile` (camelCase). This works for English-named Python/Go symbols.
- It fails for: Hungarian notation (`m_szFileName`), abbreviated names (`ctx`, `cfg`, `srv`), non-English identifiers, or symbols whose names are semantically distant from their purpose (`New` in Go means "constructor" but the word "new" matches nothing useful).

**The principled alternative: task-graph intersection.** Instead of asking "which symbol names match the question keywords?", ask "which symbols are structurally positioned to participate in answering this question?"

Formalization: Given a task question Q, define the *task subgraph* G_Q as the set of nodes reachable from any node whose **docstring, purpose, or structural role** overlaps with Q's intent. This is computable via:
1. **Semantic anchors:** Nodes whose `purpose` field (docstring first sentence) has semantic overlap with Q. This uses the *content* of documentation, not the *syntax* of names.
2. **Structural expansion:** From anchors, expand via the call graph (callers + callees, 1-2 hops) and containment graph (class→methods).
3. **Centrality-weighted ranking:** Among expanded nodes, rank by betweenness centrality in the task subgraph (not the full repo graph). Betweenness identifies *bottleneck* symbols — those through which many information paths flow.

**Why this generalizes:** It depends on graph topology (universal) and documentation content (language-agnostic), not name syntax. A Go function called `New` is selected because its docstring says "creates a new Foo" and it has high fan-out, not because the word "new" matches a question keyword.

---

### Principle 3: Behavioral Annotations Must Be Language-Agnostic Patterns

**Claim:** Method body logic can be summarized as a small set of universal control flow patterns that apply to any imperative/OO language.

**The pattern vocabulary (complete for mechanistic facts):**

| Pattern | Description | Example |
|---------|-------------|---------|
| `PRECEDENCE(a, b, c)` | Tries sources in order, returns first non-null | `consume_value`: CLI → env → default_map → default |
| `GUARD(condition) → action` | Early return/error on condition | `BaseRequest.post`: returns empty for non-POST |
| `DELEGATE(target)` | Calls another method and returns its result | `Application.startup` → signals `on_startup` |
| `ACCUMULATE(loop) → result` | Iterates and builds up a result | `BaseRequest.read`: `readany` loop → bytes |
| `BRANCH(condition, then, else)` | Conditional with distinct paths | `DefaultPanicHandler`: error→pass-through, other→wrap |
| `TRANSFORM(input) → output` | Data transformation pipeline | `Choice.convert`: normalize → case-fold → return original |
| `UNWIND(collection, reverse)` | Cleanup/teardown in reverse order | `CleanupContext._on_cleanup`: reverse exit iteration |
| `DISPATCH(key, map)` | Looks up handler by key and delegates | `Group.invoke`: token → subcommand → invoke |

**Why 8 patterns suffice:** These cover the 24 gold facts across 3 repos (aiohttp, click, fiber) and 2 languages (Python, Go). Let me verify:

- click-2 FACT 1 (consume_value precedence) → `PRECEDENCE`
- click-2 FACT 2 (type_cast_value branches) → `BRANCH` + `TRANSFORM`
- click-2 FACT 3 (Choice.convert normalization) → `TRANSFORM`
- click-2 FACT 4 (File.convert lazy + Path.convert) → `DELEGATE` + `GUARD`
- aiohttp-1 FACT 1 (read accumulation + size guard) → `ACCUMULATE` + `GUARD`
- aiohttp-1 FACT 2 (json mimetype guard) → `GUARD` + `DELEGATE`
- aiohttp-2 FACT 4 (cleanup reverse unwind) → `UNWIND`
- fiber-1 FACT 2 (RestartRouting index reset) → `DISPATCH`(restart variant)
- fiber-2 FACT 2 (DefaultPanicHandler) → `BRANCH` ← **the one fact that was COVERED** (because the docstring described the branch)

**Extraction is AST-based, not LLM-based:** For each language, a control-flow visitor walks function bodies and identifies:
- Sequential `if/elif/else` chains → `PRECEDENCE` or `BRANCH`
- `for`/`while` with accumulator variable → `ACCUMULATE`
- Single call + return → `DELEGATE`
- `raise`/`panic` at top of function → `GUARD`

This is NOT summarization (which would require an LLM and be non-deterministic). It is **pattern classification** from AST structure — deterministic and reproducible.

**The unseen repo test:** The patterns are defined over control flow primitives that exist in every imperative language. Python `if/elif`, Go `if/else if`, TypeScript `if/else`, Java `if/else` all map to the same patterns. The extractor is language-specific (as it must be — different ASTs), but the output representation is universal.

---

### Principle 4: The 80-Node FOCUS Cap Must Be Information-Theoretically Justified

**Claim:** An arbitrary cap (80 nodes) is indefensible because the *right* number depends on the task's information requirements, not a fixed constant.

**Principled alternative: budget-driven, not count-driven.** Instead of selecting up to N nodes and rendering each until budget runs out, select nodes greedily until the L3 token budget (2000 tokens) is exhausted.

Algorithm:
1. Rank all candidate nodes by task relevance score (Principle 2).
2. For each node in rank order, estimate its rendering cost: ~25 tokens (structural) + ~30 tokens (behavioral annotation, if extractable).
3. Add to FOCUS until budget is consumed.
4. Report actual coverage in GAPS: "L3 covers N/M task-relevant symbols; top uncovered: X, Y, Z (drill: file.py:line)"

This means:
- A task requiring 5 deeply-annotated symbols gets 5 rich entries (~55 tokens × 5 = 275 tokens, with remaining budget for more symbols).
- A task touching 60 symbols gets 60 sparse entries (structural-only, no behavior).
- The format **self-reports** its coverage, enabling the LLM to make informed drill-down decisions.

**The unseen repo test:** The algorithm depends on token counting (universal) and relevance ranking (graph-structural). No repo-specific parameter.

---

### Principle 5: Validation Must Prevent Overfitting by Design

**Claim:** The current methodology (develop on click, test on click) is a recipe for overfitting. Any improvement measured this way is suspect.

**Principled validation framework:**

#### 5a. Data Splits

| Split | Repos | Purpose | When to use |
|-------|-------|---------|-------------|
| **Dev** | Flask, httpx, Gin (existing) | Iterate freely | During development |
| **Validation** | aiohttp, fiber (existing blind, now promoted) | Tune hyperparameters | After dev iteration converges |
| **Blind** | **3+ NEW repos, never examined** | Final evaluation | Once, at publication time |

**Critical rule:** Click must be moved to Dev (its gold tasks have been examined during debugging). aiohttp and fiber move to Validation. Three genuinely new repos (recommended: one Python, one Go/Rust, one TypeScript/Java) become the Blind set.

#### 5b. Minimum Sample Size for Generalizable Claims

Using binomial confidence intervals:
- At n=24 tasks, a score of 1/24 has 95% CI [0.1%, 21%]. We cannot distinguish this from random.
- At n=60 tasks, a score of 40/60 has 95% CI [54%, 79%]. This starts being publishable.
- **Minimum viable evaluation:** 10 repos × 6 tasks × 4 facts = 240 fact-checks across ≥3 languages.

#### 5c. Overfitting Detection During Development

After each code change, compute:
- **Dev accuracy** (on dev repos)
- **Validation accuracy** (on validation repos)
- **Gap = Dev - Validation**

If Gap > 10 percentage points, the change is overfitting. Revert and rethink.

This is standard ML practice (train/val monitoring) adapted for format engineering.

#### 5d. Per-Knowledge-Type Reporting

Every evaluation must break down by knowledge type:

| Type | Definition | Expected ceiling (File 1 only) |
|------|-----------|-------------------------------|
| Structural | File/module layout | ≥90% |
| Relational | Call graph, inheritance | ≥80% |
| Declarative | Signatures, docstrings | ≥75% |
| Mechanistic | Internal logic, precedence | ≥40% (with behavioral annotations) |
| Invariant | Error handling, security | ≥30% (with behavioral annotations) |

**The unseen repo test:** The validation framework itself is repo-agnostic. It treats repos as samples from a population of "all possible codebases" and uses standard statistical methods.

---

## Part II: ACTIONS

### Action 1: Add Behavioral Annotation Extraction

**Implements:** Principle 3 (language-agnostic behavioral patterns)

**What changes:**
- `extractor.py`: Add `_extract_behavior_patterns(node: ast.AST) -> list[str]` that walks a function/method body and classifies its top-level control flow into the 8-pattern vocabulary.
- `extract_go.py`: Add equivalent Go pattern extraction (regex-based, operating on the function body text between `func` and closing `}`).
- `extract_typescript.py`: Add equivalent TS pattern extraction.
- `models.py`: Add `behavior_patterns: list[str]` to Node's semantic_contract schema.
- `clue_view_mrlf.py`: FOCUS entry renderer includes a `behavior:` line when patterns are available.

**Example output for `consume_value`:**
```
consume_value (src/click/core.py:2297-2340)
  sig: consume_value(ctx, opts)
  behavior: PRECEDENCE(opts_parse, envvar, default_map, param_default)
  calls: resolve_envvar_value, ...
```

**Why it generalizes:** The patterns are defined over universal control flow structures. Every language has conditionals, loops, delegation, and guards. The *extractor* is language-specific (necessarily), but the *output representation* is identical across languages.

**Validation criteria:**
- On Dev repos: behavioral annotations present for ≥60% of FOCUS functions
- On Validation repos: same ≥60% threshold (tests for generalization)
- Manual audit: 20 randomly sampled annotations checked for correctness

**Complexity:** Medium (2-3 days). AST walking for Python is straightforward; Go/TS regex-based extraction is approximate but sufficient.

**Expected impact:** Mechanistic accuracy from ~4% to ~35-45% (estimated from gold fact coverage analysis: 18/24 gold facts map to extractable patterns).

---

### Action 2: Replace Lexical FOCUS Selection with Graph-Structural Selection

**Implements:** Principle 2 (graph-structural, not lexical)

**What changes to `_select_focus_nodes()`:**

**Stage 1 — Semantic Anchoring (replaces keyword matching):**
```python
def _semantic_overlap(purpose: str, question_keywords: set[str]) -> float:
    """Score overlap between a node's purpose/docstring and question intent.
    
    Operates on documentation CONTENT, not symbol NAME syntax.
    Language-agnostic: works on any natural-language documentation.
    """
    purpose_words = set(re.findall(r'[a-zA-Z]{3,}', purpose.lower()))
    return len(purpose_words & question_keywords) / max(len(question_keywords), 1)
```

**Stage 2 — Structural Expansion (replaces keyword-match + graph walk):**
- From semantic anchor nodes, expand via call graph edges (bidirectional, 2 hops).
- Add *containment expansion*: if a class is anchored, include all its methods. If a method is anchored, include its containing class.
- This is the current graph walk, but seeded by docstring content rather than name syntax.

**Stage 3 — Betweenness-Weighted Ranking (replaces keyword overlap count):**
```python
def _betweenness_centrality(nodes, edges) -> dict[str, float]:
    """Betweenness centrality on the task subgraph.
    
    Identifies bottleneck nodes through which many paths flow.
    Language-agnostic: operates on graph topology only.
    """
```

**What's removed:**
- `_tokenize_symbol()` — name syntax parsing, inherently convention-specific
- `_src_priority()` — directory heuristic, inherently structure-specific  
- `_kw_overlap()` — lexical matching on names
- Stemming heuristics (remove trailing 's', 'ing', 'ed') — English-specific

**Why it generalizes:** The algorithm depends on:
1. Docstring/purpose content (natural language, present in any well-documented repo)
2. Graph topology (universal — call edges exist in any language)
3. Betweenness centrality (a graph-theoretic property, not a lexical one)

**Graceful degradation:** For repos with no docstrings (undocumented code), Stage 1 produces no anchors, and the algorithm falls back to PageRank (top globally-central symbols). This is the *correct* behavior: without documentation, the best we can do is select structurally important symbols.

**Validation criteria:**
- Gold symbol recall on Validation repos ≥ 50% (currently 41% with lexical matching)
- Gold symbol recall on Dev repos: no regression from current 41%
- Recall is identical whether symbols use snake_case, camelCase, or any other convention (tested by checking that recall doesn't correlate with naming convention)

**Complexity:** Medium (2 days). Betweenness centrality is O(V×E) but the task subgraph is small (~100–500 nodes). Pure-Python implementation is fine.

**Expected impact:** FOCUS selection accuracy from ~41% to ~55-65% (estimated). More importantly, the improvement should be *uniform* across repos (no more aiohttp-2=6/6, click-1=0/6 disparity).

---

### Action 3: Budget-Driven FOCUS Rendering (Replace Fixed Node Cap)

**Implements:** Principle 4 (information-theoretically justified budget)

**What changes to `_render_l3()` and `_select_focus_nodes()`:**

- Remove `max_nodes=80` parameter.
- Add token-budget-driven loop: render nodes in rank order until L3 budget (2000 tokens) is consumed.
- Each node's rendering cost is estimated before rendering (avoids the current pattern of rendering 80 nodes then discovering most got clipped by budget).
- When behavioral annotations are available, they're included in the cost estimate.

**New FOCUS entry cost model:**
```
Base (name, file, lines):      ~10 tokens
Purpose/docstring:              ~15 tokens  
Signature:                      ~5 tokens
Behavioral annotation:          ~30 tokens (when available)
Call edges:                     ~10 tokens
TOTAL per symbol:               ~40-70 tokens
```

At 2000 tokens, this yields ~28-50 FOCUS entries depending on behavioral annotation availability. This is *fewer* than 80 but *richer* — exactly the tradeoff Principle 1 demands.

**Why it generalizes:** Token counting is language-agnostic. The budget is fixed (2000 tokens). The algorithm adapts to whatever content is available without repo-specific tuning.

**Validation criteria:**
- L3 section always uses ≥90% of its 2000-token budget (no wasted space)
- Mechanistic fact coverage improves vs. current (measured on Validation repos)
- Total clue stays under 4150-token ceiling

**Complexity:** Low (1 day). Mostly refactoring existing rendering code.

**Expected impact:** Moderate. The main benefit is removing an arbitrary parameter (80) and ensuring token budget is used efficiently. Combined with Actions 1+2, this enables behavioral annotations to fit within the existing budget.

---

### Action 4: Enhanced GAPS as Explicit Sufficiency Boundary

**Implements:** Principle 1 (acknowledging the behavioral gap)

**What changes to `_render_gaps()`:**

Currently GAPS reports uncovered keywords. Enhance to report:

1. **Sufficiency classification:** For each question, classify as STRUCTURAL (answerable from L0-L2), RELATIONAL (answerable from L2-L3 structure), or MECHANISTIC (requires body content).
2. **Coverage report:** "L3 covers N of M task-relevant symbols. Behavioral annotations present for K."
3. **Drill targets with cost:** "For mechanistic detail, drill: consume_value (core.py:2297, ~45 lines), type_cast_value (core.py:2342, ~30 lines)" — the LLM knows exactly how many tokens drilling will cost.

**New GAPS format:**
```
-- GAPS
type: MECHANISTIC (body logic needed for full answer)
L3 coverage: 12/18 task-relevant symbols, 8 with behavior annotations
uncovered: Group.parse_args, Group.resolve_command, Group.invoke
drill: core.py:1850-1920 (Group dispatch chain, ~70 lines)
drill: decorators.py:1-50 (command/group helper, ~50 lines)
```

**Why it generalizes:** The sufficiency classification depends on question structure (does it ask "what" vs "how"), not on repo specifics. The coverage report is computed from the graph. The drill targets are computed from symbol locations.

**Commercial viability impact:** This is *critical*. If the format can tell the LLM "I can't answer this from File 1 alone, but here's exactly where to look in File 2," then the two-tier system (File 1 + File 2 drill-down) becomes the correct architecture. The format's value proposition becomes: **instant structural understanding + guided deep-dive**, not "answer everything from 4K tokens."

**Validation criteria:**
- GAPS correctly classifies ≥80% of questions as structural/relational/mechanistic (tested on gold tasks)
- Drill targets point to the correct file regions for ≥70% of uncovered facts
- Total GAPS section stays under 100-token budget

**Complexity:** Low-Medium (1-2 days).

**Expected impact:** Does not directly improve fact coverage, but dramatically improves the *usefulness* of the format in a two-tier system. Enables Action 5.

---

### Action 5: Establish Proper Validation Framework

**Implements:** Principle 5 (overfitting prevention)

**What changes:**

#### 5a. Repo Split Restructuring

Create `experiments/eval-config.json`:
```json
{
  "splits": {
    "dev": ["flask", "httpx", "gin", "click"],
    "validation": ["aiohttp", "fiber"],
    "blind": []
  },
  "notes": "Blind repos must be added from outside this repo. Never examine blind repo source."
}
```

**Researcher action required:** Select 3+ new Blind repos. Recommended criteria:
- At least 2 languages (one must be a language NOT in the dev set)
- At least 1 repo with minimal docstrings (tests graceful degradation)
- At least 1 repo with 500K+ tokens (tests scale)
- At least 1 repo with non-English or heavily abbreviated naming (tests convention independence)

Suggested: `requests` (Python, well-documented), `echo` (Go, terse naming), `prisma` or `zod` (TypeScript, complex generics), plus optionally a Java or Rust repo.

#### 5b. Gold Task Generation Protocol

For each Blind repo, create 6 tasks:
- 2 Structural (answerable from L0-L2)
- 2 Relational (answerable from L2-L3 structure)
- 2 Mechanistic (requires body content)

Gold facts must be written by reading source code, not by running the format. Each fact must include:
- The fact statement
- The file+lines that contain the evidence
- The knowledge type (structural/relational/mechanistic)
- Whether File 1 alone should be sufficient (based on knowledge type)

#### 5c. Automated Overfitting Monitor

Create `experiments/runs/eval_monitor.py`:
```python
def evaluate_split(split_name: str, repos: list[str]) -> dict:
    """Run all gold tasks for a split and return per-knowledge-type accuracy."""
    
def check_overfitting(dev_results: dict, val_results: dict) -> bool:
    """Return True if dev accuracy exceeds val accuracy by >10pp on any knowledge type."""
```

Run after every code change. If overfitting detected, flag the change.

#### 5d. Statistical Reporting Standards

Every result must include:
- Point estimate (e.g., 45% mechanistic accuracy)
- 95% confidence interval (Wilson binomial CI at the given sample size)
- Sample size and composition (N tasks, across M repos, K languages)
- Split identity (dev/validation/blind)

**Complexity:** Medium (2-3 days for framework; ongoing cost for new gold tasks).

**Expected impact:** No direct accuracy improvement, but prevents wasted effort on overfitting changes and makes results publishable.

---

## Part III: RESEARCH QUESTIONS — ANSWERS

### Q1: The Compression-Sufficiency Tradeoff

**Answer:** Abandon the single-file sufficiency claim for mechanistic questions. The format should embrace a **two-tier architecture**:

- **Tier 1 (File 1):** Sufficient statistic for structural, relational, and declarative questions (~70% of tasks). Behavioral annotations provide partial coverage of mechanistic questions (~35-45% estimated).
- **Tier 2 (File 2 drill-down):** Required for deep mechanistic and invariant questions. Guided by enhanced GAPS section.

**Rate-distortion estimate for mechanistic facts:** Each fact requires ~50 tokens of behavioral description. At 24 gold facts, that's 1200 tokens — which fits within L3 budget. But this is for a *specific task*. The general problem is that we don't know which methods' bodies will be relevant until the question is asked, and there are thousands of methods. The 4K token ceiling cannot contain behavioral annotations for all of them.

**MDL perspective:** The minimum description length for "how method X works" is bounded below by the method's Kolmogorov complexity. For non-trivial methods (20-50 lines of logic), this is ~100-300 tokens — irreducible. Our behavioral pattern annotations achieve ~30-50 tokens by abstracting to patterns, which is a legitimate lossy compression. But patterns can only capture *structure* (precedence, branching), not *content* (what specific values are checked, what specific errors are raised).

**Commercial recommendation:** Market as "instant codebase understanding with guided deep-dive capability." The 4K artifact is the entry point; the value is in knowing *where to look*, not in answering everything from 4K tokens.

### Q2: The Selection Problem (Generalized)

**Answer:** Graph-structural selection via semantic anchoring + betweenness centrality (Action 2). See Principle 2 for details.

**Key insight:** The selection problem is really a **task relevance** problem. Task relevance is a *semantic* property (does this symbol help answer the question?) that must be approximated from *structural* signals (where is this symbol in the call graph? what does its documentation say?). Name matching is a poor proxy for semantic relevance.

### Q3: The Behavioral Gap (Generalized)

**Answer:** Language-agnostic control flow pattern extraction (Action 1). See Principle 3 for the 8-pattern vocabulary.

**What this cannot capture:** Data-specific logic (e.g., "checks if content_type starts with 'application/json'"). This is irreducible content that lives in the source code. The behavioral patterns capture *structure* ("there's a guard clause that checks content type") but not *content* ("the specific content type is application/json").

**This is acceptable** because the patterns give the LLM enough context to formulate a targeted drill-down request: "I see consume_value uses PRECEDENCE pattern with 4 sources. Show me the body to learn what the sources are."

### Q4: Validation Without Overfitting

**Answer:** Proper dev/validation/blind splits + automated overfitting monitor + per-knowledge-type reporting + statistical confidence intervals (Action 5). See Principle 5.

### Q5: Commercial Viability Assessment

**Current state:** 1/24 mechanistic facts from File 1 alone. Not viable as a standalone product.

**Projected state after this plan:**
- Structural questions: ≥90% (already ~80%, behavioral annotations don't affect this)
- Relational questions: ≥80% (already good, selection improvement helps)
- Mechanistic questions: ~35-45% from File 1 alone (up from 4%)
- With File 2 drill-down: ~80%+ (Phase 5 showed 18/20 sufficient with source appended)

**Competitive landscape:**
- **Full RAG (embed all source):** Higher accuracy but O(n) token cost, no structure guarantee. CodeClue wins on efficiency and consistency.
- **Tree-sitter + embeddings:** Good for localization, poor for behavioral understanding. CodeClue wins on comprehension depth.
- **Agentic browsing (read files on demand):** High accuracy but high latency, high token cost, non-deterministic. CodeClue wins on speed and cost.

**Unique value proposition that survives even at 50% mechanistic:** "Pre-computed codebase understanding that eliminates cold-start latency and provides deterministic structural answers, with guided drill-down for deep questions." No competitor offers this combination of speed (pre-computed), consistency (deterministic), and efficiency (4K tokens for structural + behavioral patterns).

**Minimum viable accuracy:**
- Structural ≥85% (table stakes)
- Relational ≥70% (competitive differentiator)
- Mechanistic ≥30% from File 1, ≥70% with drill-down (the two-tier story)

---

## Part IV: IMPLEMENTATION ORDER

| Priority | Action | Depends On | Days | Risk |
|----------|--------|------------|------|------|
| **1** | Action 5: Validation framework | Nothing | 2-3 | Low — must do first to prevent overfitting |
| **2** | Action 2: Graph-structural selection | Validation framework | 2 | Medium — betweenness centrality may be slow on large graphs |
| **3** | Action 1: Behavioral annotations | Validation framework | 2-3 | Medium — pattern extraction quality varies by language |
| **4** | Action 3: Budget-driven rendering | Actions 1+2 | 1 | Low — straightforward refactoring |
| **5** | Action 4: Enhanced GAPS | Actions 1+2+3 | 1-2 | Low — builds on existing GAPS infrastructure |

**Total estimated time:** 8-11 days of focused implementation.

**Checkpoints:**
1. After Action 5: Baseline metrics on all splits with current code.
2. After Action 2: Selection quality on Validation repos (expect uniform improvement).
3. After Actions 1+3: Mechanistic accuracy on Validation repos (expect ≥30%).
4. After Action 4: Full pipeline metrics on all splits.
5. Final: Blind evaluation on new repos (one-time, publish-or-not decision).

---

## Part V: ANTI-PATTERNS TO AVOID

These are patterns that the previous session fell into. Explicitly listing them as guardrails:

1. **NO repo-specific heuristics.** If a fix mentions a specific repo name, directory convention, or naming pattern, it's wrong.
2. **NO accuracy celebration on Dev repos.** Dev accuracy is expected to be high. Only Validation and Blind accuracy matter.
3. **NO magic numbers without justification.** Every threshold, cap, and parameter must derive from information theory or be explicitly labeled as "tunable hyperparameter, to be set via Validation performance."
4. **NO testing on training data.** If you examined a repo's source code to write a fix, that repo is Dev, not Blind.
5. **NO lexical tricks.** Stemming, substring matching, regex tokenization of symbol names — all of these are fragile proxies for semantic relevance. Use structural signals instead.
6. **NO claiming File 1 sufficiency for mechanistic questions.** The theory says it's impossible within 4K tokens. Embrace the two-tier architecture.

---

## Appendix A: Mapping Gold Facts to Behavioral Patterns

| Task | Fact# | Gold Fact (abbreviated) | Pattern | Extractable? |
|------|-------|------------------------|---------|-------------|
| click-2 | 1 | consume_value precedence order | `PRECEDENCE` | Yes — sequential if-return |
| click-2 | 2 | type_cast_value branches by nargs | `BRANCH` | Yes — if/elif chain |
| click-2 | 3 | Choice.convert normalizes then returns original | `TRANSFORM` | Partial — normalize step detectable |
| click-2 | 4 | File.convert deferred open + Path.convert constraints | `DELEGATE`+`GUARD` | Yes — conditional + delegation |
| aiohttp-1 | 1 | read accumulates with size guard | `ACCUMULATE`+`GUARD` | Yes — while loop + raise |
| aiohttp-1 | 2 | json calls text, rejects mimetype | `DELEGATE`+`GUARD` | Yes — call + if-raise |
| aiohttp-1 | 3 | post returns empty for wrong method | `GUARD` | Yes — early return |
| aiohttp-1 | 4 | post streams multipart to tempfile | `ACCUMULATE` | Partial — async iteration |
| aiohttp-2 | 1 | startup/shutdown signal wiring | `DELEGATE` | Yes — method calls signal |
| aiohttp-2 | 2 | cleanup fallback for incomplete startup | `GUARD`+`DELEGATE` | Yes — if-not-frozen check |
| aiohttp-2 | 3 | _on_startup accepts generators/ctx managers | `BRANCH` | Partial — isinstance check |
| aiohttp-2 | 4 | _on_cleanup reverse unwind, multi-error | `UNWIND` | Yes — reversed() + except |
| fiber-1 | 1 | Path mutates URI + recomputes | `TRANSFORM` | Partial — assignment chain |
| fiber-1 | 2 | RestartRouting resets index, calls next | `DELEGATE` | Yes — assignment + call |
| fiber-1 | 3 | next scans treeStack, matches routes | `DISPATCH` | Partial — for loop + match |
| fiber-1 | 4 | 404 vs 405 based on method match | `BRANCH` | Yes — if methodMatched |
| fiber-2 | 1 | recover wraps c.Next in defer/recover | `GUARD` | Yes — defer/recover pattern |
| fiber-2 | 2 | DefaultPanicHandler error vs wrap | `BRANCH` | Yes — **already covered** |
| fiber-2 | 3 | Constructor installs DefaultErrorHandler | `GUARD`+`DELEGATE` | Yes — if nil assignment |
| fiber-2 | 4 | ErrorHandler searches sub-app prefixes | `DISPATCH` | Yes — for loop + prefix match |
| click-1 | 1 | decorators.command builds Command | `TRANSFORM` | Yes — constructor call |
| click-1 | 2 | group defaults cls to Group | `DELEGATE` | Yes — defaults + call |
| click-1 | 3 | add_command stores in map | `TRANSFORM` | Yes — dict assignment |
| click-1 | 4 | parse_args/resolve/invoke chain | `DISPATCH` | Yes — sequential delegation |

**Summary:** 20/24 facts map to extractable patterns. 4 are "partial" (complex async iteration, isinstance branching, assignment chains). Even partial extraction provides enough signal for the LLM to formulate targeted drill-down requests.

---

## Appendix B: What This Plan Does NOT Address

1. **TypeScript class method extraction** — Known gap in `extract_typescript.py`. This is a language-specific extractor bug, not a format design issue. Fix separately.
2. **Multi-language repos** — Format handles single-language extraction per repo. Multi-language support is an orchestration concern.
3. **Streaming/incremental updates** — Excluded by design constraint NC6.
4. **MCP server integration** — Infrastructure concern, not format design. The enhanced GAPS + File 2 design enables MCP but doesn't require it.
5. **LLM prompt engineering** — How to best prompt an LLM to use the clue is a separate research question. This plan addresses the *content* of the clue, not how it's consumed.
