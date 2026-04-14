# New Design Basis — Multi-Resolution Lattice Format (MRLF)

Date: 2026-04-07
Status: Working draft — not yet formalised

---

## Upfront: What This Design Considers and Does Not Consider

### Active Constraints

| ID | Constraint | One-Line Rationale |
|----|-----------|-------------------|
| C1 | Fixed ~4150 token ceiling for primary clue | Bounded encoding for unbounded input; clue must be ≤5% of context budget |
| C2 | 100% structural coverage at L0-L1 | Data Processing Inequality — discarding modules destroys information irrecoverably |
| C3 | No JSON/markup in consumer artifact | MDL — every `{`, `"key":` is a token with zero task-answer information |
| C4 | Task-conditioning at L3 only | L0-L2 cacheable; if projection fails, LLM still has full repo map |
| C5 | GAPS section mandatory | Successive refinement requires first stage to signal where refinement is needed |
| C6 | PageRank ranking for L2 symbols | Centrality identifies symbols most likely to appear in any task answer |
| C7 | File 2 (detail store) is record-level | Random access; drill cost proportional to need, not repo size |
| C8 | Language-agnostic normalisation | Same format for Python/TypeScript/Go; no language-specific constructs |
| C9 | Repo-size independence | MDL — if model description grows with data, you're encoding data, not a model |

### Excluded Constraints

| ID | Not Considered | One-Line Rationale |
|----|---------------|-------------------|
| NC1 | Human readability | LLM-only consumer; humans get a separate MCP converter tool |
| NC2 | Round-trip losslessness | Provably incompatible with CCR ≥ 80% at any scale (see Section 5.3) |
| NC3 | Backward compatibility | All prior formats failed H2; no installed base; clean break |
| NC4 | Raw source code in primary clue | Would break token ceiling; source goes in File 2 |
| NC5 | Per-node confidence scores | 41% of poisoned format was confidence; replaced by GAPS (see Section 5.3) |
| NC6 | Streaming/incremental update | Primary clue is cheap to regenerate (1–4K tokens) |
| NC7 | Multi-repo queries | Orchestration concern for MCP layer, not format concern |
| NC8 | LLM-family-specific optimisation | Universal plain text avoids vendor lock-in |
| NC9 | Real-time generation latency | Batch operation; even Django computes in seconds |
| NC10 | Formal schema validation | Schema compliance drove format bloat; conventions + linter instead |

### File Architecture

| File | Contents | Size | Sent to LLM? |
|------|----------|------|--------------|
| File 1: `.codeclue` | L0 TREE + L1 INDEX + L2 SYM + L3 FOCUS + GAPS (all in one file) | 1–4K tokens (fixed ceiling) | Yes, always |
| File 2: `.codeclue-detail` | Per-symbol JSONL records with source, call graphs, complexity, confidence | Proportional to repo | No — individual records accessed via MCP on demand |

**2 files per repo, not 5.** L0–L3 and GAPS are sections within one File 1.

---

## 0. Purpose, Persona and Use Cases

### 0.1 Problem Statement

Every time an LLM interacts with a code repository it re-reads, re-parses
and re-infers the same structural and behavioural understanding that was already
derived in a previous session. This throwaway interpretation is:

- **Expensive** — consumes tokens proportional to repository size on every interaction.
- **Slow** — latency grows with codebase size as the model ingests raw source.
- **Inconsistent** — the same question asked twice can produce different structural
  inferences depending on which files happen to land in the context window.
- **Incomplete** — large repos exceed context windows, forcing the LLM to work from
  partial views and guess at the rest.

CodeClue eliminates this waste by generating a **persistent, versioned comprehension
artifact** (the "clue file") that can be loaded once and reused across sessions,
tools, and models. The clue file is the LLM's pre-built understanding of a codebase.

### 0.2 User Persona

**Primary:** Software developers and engineers who use LLM-powered tools as part
of their daily workflow — in IDE assistants, chat interfaces, CI pipelines, code
review tools, and terminal agents.

**Secondary:** Anyone who needs to interact with a code repository through an LLM
but is not the author — SREs investigating incidents, security auditors reviewing
dependencies, new team members onboarding to an unfamiliar codebase, engineering
managers assessing change impact, technical writers documenting APIs.

**Common trait:** These users do not want to manually explain the code structure
to the LLM. They expect the LLM to "already know" the codebase, the way a senior
engineer on the team would.

### 0.3 Core Intent

Avoid repetitive and throwaway code interpretation, inference, and task execution
by giving the LLM a pre-computed structural and behavioural understanding of a
codebase that persists across sessions.

The clue file is NOT:

- A replacement for reading source code (it's a map, not the territory).
- A documentation generator (it's optimised for LLM consumption, not human reading).
- A static analysis tool (it captures structure and behaviour, not correctness).

The clue file IS:

- A persistent context artifact that survives session boundaries.
- A compression of the codebase into its task-relevant essence.
- A starting point from which the LLM can drill into source when detail is needed.

### 0.4 Use Cases (Exhaustive)

The following use cases define the full range of tasks an LLM might perform using
a clue file. They are grouped by category and ordered roughly by frequency of
occurrence in typical developer workflows.

#### Category 1: Code Comprehension and Navigation

| ID | Use Case | What the LLM needs from the clue |
|----|----------|----------------------------------|
| UC-01 | **Codebase orientation** — "What does this repo do? What are the main modules?" | L0 TREE, L1 INDEX, L2 top symbols |
| UC-02 | **Symbol lookup** — "Where is X defined? What calls it?" | L2 SYM with centrality, L3 call chains |
| UC-03 | **Dependency tracing** — "What does module A depend on?" | L1 INDEX exports, L2 SYM call edges |
| UC-04 | **Execution flow tracing** — "What happens when a user hits /login?" | L3 FOCUS with call chain from entrypoint |
| UC-05 | **Configuration impact** — "What reads SETTING_X and what breaks if it changes?" | L2 SYM readers, L3 FOCUS impact chain |
| UC-06 | **API surface discovery** — "What endpoints/functions are exposed?" | L1 INDEX + L2 SYM entrypoints |
| UC-07 | **Architecture overview** — "How are modules layered? What talks to what?" | L0 TREE + L1 INDEX + L2 SYM centrality |
| UC-08 | **Onboarding Q&A** — "I'm new, explain how the auth system works" | L3 FOCUS behavioural summaries |

#### Category 2: Debugging and Incident Response

| ID | Use Case | What the LLM needs from the clue |
|----|----------|----------------------------------|
| UC-09 | **Crash analysis** — "Given this stack trace, what went wrong?" | L2 SYM for stack symbols, L3 FOCUS for behavioural context |
| UC-10 | **Exception path tracing** — "What can throw X and who catches it?" | L2 SYM + L3 FOCUS error-handler chains |
| UC-11 | **State mutation debugging** — "Where does object.field get modified?" | L2 SYM + File 2 detail records for mutation sites |
| UC-12 | **Race condition analysis** — "What shared state is accessed without locks?" | L3 FOCUS concurrency annotations, GAPS for unresolved |
| UC-13 | **Memory/resource leak investigation** — "Where are connections opened but not closed?" | L2 SYM resource lifecycle, L3 FOCUS cleanup paths |
| UC-14 | **Log correlation** — "Given this log line, trace back to the code path" | L2 SYM + File 2 source snippets for logging calls |
| UC-15 | **Performance bottleneck identification** — "What's on the hot path for /api/heavy?" | L3 FOCUS call chain with complexity hints |

#### Category 3: Code Review and PR Analysis

| ID | Use Case | What the LLM needs from the clue |
|----|----------|----------------------------------|
| UC-16 | **PR impact analysis** — "What does this diff affect downstream?" | L2 SYM call graph, L3 FOCUS impact chain |
| UC-17 | **Risk assessment** — "Is this change safe? What could break?" | L3 FOCUS invariants, GAPS for untested paths |
| UC-18 | **Review prioritisation** — "Which files in this PR are highest risk?" | L2 SYM centrality ranking |
| UC-19 | **Semantic diff** — "What changed behaviourally, not just syntactically?" | L3 FOCUS behavioural summaries (pre vs post) |
| UC-20 | **Test coverage gap detection** — "What code paths are changed but untested?" | L2 SYM test files, L3 FOCUS coverage flags |

#### Category 4: Refactoring and Transformation

| ID | Use Case | What the LLM needs from the clue |
|----|----------|----------------------------------|
| UC-21 | **Safe refactoring** — "Can I rename/move X without breaking anything?" | L2 SYM callers/callees, L3 FOCUS dependency chain |
| UC-22 | **Module extraction** — "Split this god-class into smaller modules" | L2 SYM cohesion analysis, L1 INDEX module boundaries |
| UC-23 | **Interface extraction** — "What's the minimal interface for module X?" | L2 SYM public API + call edges |
| UC-24 | **Dead code identification** — "What's never called?" | L2 SYM with zero in-degree |
| UC-25 | **Dependency inversion** — "Invert the dependency between A and B" | L2 SYM bidirectional edges, L3 FOCUS coupling analysis |
| UC-26 | **Migration planning** — "Move from framework X to framework Y" | L1 INDEX for framework-specific files, L2 SYM for API usage |
| UC-27 | **Function transformation** — "Convert sync function to async" | L3 FOCUS call chain (who calls it, who it calls), GAPS for side effects |

#### Category 5: Feature Development

| ID | Use Case | What the LLM needs from the clue |
|----|----------|----------------------------------|
| UC-28 | **Feature addition** — "Add a caching layer to the data access module" | L1 INDEX for module structure, L2 SYM for integration points |
| UC-29 | **Endpoint implementation** — "Add a new /api/v2/users endpoint" | L2 SYM for existing endpoint patterns, L3 FOCUS for middleware chain |
| UC-30 | **Error handling improvement** — "Add retry logic to all external API calls" | L2 SYM for call sites, L3 FOCUS for error paths |
| UC-31 | **Configuration addition** — "Add a new config option and wire it through" | L3 FOCUS config readers (existing pattern), L2 SYM for wiring points |
| UC-32 | **Test generation** — "Write tests for module X" | L2 SYM public API, L3 FOCUS behavioural invariants |

#### Category 6: Security and Compliance

| ID | Use Case | What the LLM needs from the clue |
|----|----------|----------------------------------|
| UC-33 | **Security audit** — "Identify all authentication and authorisation points" | L2 SYM security-tagged symbols, L3 FOCUS auth chain |
| UC-34 | **Vulnerability assessment** — "Does this repo have SQL injection vectors?" | L2 SYM input handlers, L3 FOCUS data flow to DB |
| UC-35 | **Secret detection** — "Where are credentials, tokens, or keys handled?" | L2 SYM config/secret modules, GAPS for runtime injection |
| UC-36 | **Compliance check** — "Does the data handling comply with GDPR/PII rules?" | L2 SYM data model, L3 FOCUS data flow paths |
| UC-37 | **Dependency risk** — "What third-party packages are used and where?" | L1 INDEX imports, L2 SYM external call sites |
| UC-38 | **Attack surface mapping** — "What's exposed to untrusted input?" | L2 SYM entrypoints + parsers, L3 FOCUS input validation chains |

#### Category 7: Documentation and Knowledge Transfer

| ID | Use Case | What the LLM needs from the clue |
|----|----------|----------------------------------|
| UC-39 | **API documentation generation** — "Document all public endpoints" | L2 SYM public API signatures, L3 FOCUS behavior |
| UC-40 | **Architecture decision record** — "Why is the code structured this way?" | L0 TREE + L1 INDEX + L2 SYM patterns |
| UC-41 | **Runbook generation** — "How to deploy, configure, troubleshoot" | L1 INDEX for config/deploy files, L3 FOCUS for operational paths |
| UC-42 | **Changelog generation** — "What changed between v1.2 and v1.3?" | Delta between two clue files |

#### Category 8: CI/CD and Automation

| ID | Use Case | What the LLM needs from the clue |
|----|----------|----------------------------------|
| UC-43 | **Build failure diagnosis** — "Why did the build fail? What changed?" | L2 SYM for build-related modules, L3 FOCUS error paths |
| UC-44 | **Deployment impact prediction** — "What services need redeployment?" | L2 SYM inter-service call edges |
| UC-45 | **Automated code review** — "Flag risky patterns in CI" | L2 SYM risk-tagged nodes, L3 FOCUS invariant violations |
| UC-46 | **Regression scope prediction** — "What tests should run for this diff?" | L2 SYM caller graph from changed files |

#### Category 9: Cross-Repository and System-Level

| ID | Use Case | What the LLM needs from the clue |
|----|----------|----------------------------------|
| UC-47 | **Service interaction mapping** — "How does service A call service B?" | L1 INDEX + L2 SYM for both repos (composed) |
| UC-48 | **Shared library impact** — "If I change lib X, what services break?" | L2 SYM for lib consumers across clue files |
| UC-49 | **Monorepo navigation** — "Show me the boundaries in this monorepo" | L0 TREE + L1 INDEX (package boundaries) |
| UC-50 | **Tech debt inventory** — "Where are the TODO/HACK/FIXME hotspots?" | L2 SYM + File 2 annotations |

### 0.5 How Use Cases Inform the Design

The use cases above share three structural properties that directly drive the
format design:

**Property 1: Most tasks start with "where/what" before "how/why".**

UC-01 through UC-08 are all localization tasks. The LLM first needs to know
WHICH files and symbols matter before it needs to understand HOW they work.
This is why L0-L2 (structure) must cover 100% of the repo (Constraint C2)
while L3 (behaviour) can be task-conditioned (Constraint C4).

**Property 2: 70%+ of tasks can be answered from structure + short behavioural summary.**

Categories 1, 3, 5, 7, and 8 (UC-01 through UC-08, UC-16 through UC-20,
UC-28 through UC-32, UC-39 through UC-46) are answerable from the primary clue
without drill-down. Only deep debugging (Category 2) and security analysis
(Category 6) regularly need source-level detail. This is why the success factor
target is DFCR ≥ 0.60–0.70 (not 1.0) and DDR ≤ 0.40.

**Property 3: Scale-insensitive framing.**

UC-49 (monorepo navigation) and UC-05 (config impact on Django) must work
on 100K+ node repos. UC-01 (codebase orientation) must work on a 500-node
microservice. The format cannot scale token cost with repo size. This is why
the token ceiling (Constraint C1) is fixed at ~4K regardless of input size.

### 0.6 Task Family Mapping

The 5 task families (TF1–TF5) used in evaluation map to these use cases:

| Task Family | Description | Representative Use Cases |
|-------------|-------------|------------------------|
| TF1 — Refactoring | Structural change planning | UC-21, UC-22, UC-23, UC-24, UC-25, UC-26, UC-27 |
| TF2 — Impact Analysis | Downstream effect prediction | UC-05, UC-16, UC-17, UC-44, UC-48 |
| TF3 — Edit Localization | Finding what to modify | UC-28, UC-29, UC-30, UC-31 |
| TF4 — Behaviour/Debugging | Runtime path tracing | UC-04, UC-09, UC-10, UC-11, UC-12, UC-15 |
| TF5 — Security/Compliance | Vulnerability and policy checking | UC-33, UC-34, UC-35, UC-36, UC-37, UC-38 |

### 0.7 Why These Constraints Follow From the Use Cases

| Constraint | Derived From |
|-----------|-------------|
| C1: Fixed token ceiling | Property 3 (scale-insensitive), UC-49 (monorepo must work) |
| C2: 100% structural coverage | Property 1 (where/what comes first), UC-01/UC-07 (orientation must see all modules) |
| C3: No JSON | MDL + Property 2 (70% answerable from structure; tokens wasted on syntax are tokens lost from coverage) |
| C4: Task-conditioning at L3 only | Property 1 (structure is task-independent), UC-01 through UC-08 (same L0-L2 serves all comprehension tasks) |
| C5: GAPS mandatory | Categories 2 and 6 (debugging and security NEED drill-down; GAPS tells the LLM where) |
| C6: PageRank ranking | UC-18 (review prioritisation), UC-16 (PR impact) — centrality identifies high-consequence symbols |
| C7: File 2 record-level | UC-11 (state mutation — need one symbol's detail, not the whole repo) |
| C9: Repo-size independence | UC-49 (monorepo), UC-05 (Django-scale config), Property 3 |

---

## 1. Root Cause Diagnosis of Prior Formats

### 1.1 Format Generations Tested

| Format | Era | Description | Key Result |
|--------|-----|-------------|------------|
| Poisoned | v0.6.0–v0.6.3 | Full verbose JSON: node dicts, prose rationale, confidence payload, policy blocks | 37% of tokens = format overhead. Cross-model fidelity 0.55 vs target 0.85 |
| Plan A | v0.7.1–v0.7.9 | Entity-centric compact view: per-node structured blocks, stripped metadata | Localization 0.492, 4/10 sufficient (40%) |
| Plan B | v0.7.2 | Flat-table: tabular format, separate relations/assertions | Tied with Plan A on all 4 pillars |
| Hybrid | v0.8.0–v0.8.1 | Plan A structure + restored semantic content (calls/called_by as short IDs) | Localization 0.636, 6/10 sufficient (60%), won 3-0 vs Plan A |

### 1.2 Per-Repo Results (Hybrid, Best Available)

| Repo | Language | Nodes | Mean Localization | Sufficient | Verdict |
|------|----------|-------|-------------------|------------|---------|
| Flask | Python | 1,712 | 0.932 | 4/4 (100%) | Works |
| Express | TypeScript | ~800 | 0.600 | 1/1 (100%) | Marginal |
| httpx | Python | ~2K | 0.450 | 0/1 (0%) | Broken |
| FastAPI | Python | ~4K | 0.200 | 0/1 (0%) | Broken |
| Nest | TypeScript | ~6K | 0.200 | 0/1 (0%) | Broken |
| Gin | Go | ~1K | 0.253 | 0/1 (0%) | Broken |

### 1.3 Information-Theoretic Failure Analysis

#### Failure 1: Fixed 15-node selection discards 99% of codebase

*Data Processing Inequality (Cover & Thomas, 2006):*

$$I(\theta; T(X)) \leq I(\theta; X)$$

Once 99% of nodes are discarded, information about those nodes cannot be recovered
regardless of format quality. If the 15 selected nodes are wrong, fidelity collapses.
This is exactly what happened on httpx (0.45), nest (0.20), fastapi (0.20), gin (0.25).

#### Failure 2: 37% of tokens spent on debug/routing metadata

*Minimum Description Length principle (Rissanen, 1978):*

$$L(D) = \min_{H \in \mathcal{H}} \left( L(H) + L(D|H) \right)$$

The poisoned format over-specified the "model" — policy blocks, per-node confidence
arrays, validation metadata, verbose JSON keys carry zero task-answer information
but consume token budget. MDL says the shortest description that reproduces the
data IS the best model. Everything else is noise.

#### Failure 3: Flask works, nothing else does

*Sufficient Statistic bias (Fisher-Neyman Factorization):*

$$f(x;\theta) = h(x) \cdot g(\theta, T(x))$$

The statistic T(X) must capture all parameter-relevant information regardless of
which specific x is observed. Our extractor's node selection was implicitly trained
on Flask's AST patterns — a biased estimator that collapses on different code
structures.

#### Failure 4: Django graph exceeds source size

*Entropy violation:*

$$H(\text{graph}) > H(\text{source})$$

Pretty-printed JSON, duplicated call lists, default-value padding are encoding
waste — they increase description length without adding information. A compressed
representation must satisfy H(clue) << H(source).

### 1.4 Hypothesis Scorecard at v0.8.1

| # | Hypothesis | Target | Best Observed | Verdict |
|---|-----------|--------|--------------|---------|
| H1 | CCR ≥ 80% | ≥ 0.80 | 0.81 (Flask-heavy) | Weak pass, small repos only |
| H2 | Fidelity ≥ 0.85 | ≥ 0.85 | 0.636 hybrid / 0.325 ground-truth | **FAIL** |
| H3 | Delta quality d ≤ 0.05 | d ≤ 0.05 | — | Untested |
| H4 | Drift 50 commits | no floor breach | 10/50 steps done, fidelity 1.0 | 20% tested |
| H5 | Drill-down +0.10 lift | ≥ 0.10 | — | Untested |
| H6 | Contract gen ≥ 90% | ≥ 90% | — | Untested |
| H7 | ETRR ≥ 0.65 | ≥ 0.65 | — | Untested |

---

## 2. Mathematical Framework

### 2.1 Rate-Distortion Bound (Shannon, 1959)

For a source with variance σ² and target distortion D:

$$R(D) = \frac{1}{2}\log_2\frac{\sigma^2}{D}$$

Translation: There exists a minimum token rate (clue size) below which fidelity
≥ 0.85 is unachievable. Current formats operate far above this minimum — tokens
are wasted on format overhead rather than useful signal.

### 2.2 Sufficient Statistic (Fisher-Neyman Factorization)

A statistic T(X) is sufficient for parameter θ iff:

$$I(\theta; T(X)) = I(\theta; X)$$

Translation: The clue file must preserve all information the raw source contains
about the task answer. Current formats violate this by discarding entire modules
from the representation.

### 2.3 Successive Refinement (Equitz & Cover, 1991)

A source can be described at rate R₁ with distortion D₁, then refined to rate
R₁ + R₂ with distortion D₂ < D₁, if the source satisfies Markov chain conditions.

Translation: Two-file split. File 1 (primary clue) at distortion D₁ (acceptable
for ~70% tasks). File 2 (detail store) refines to D₂ for the remaining ~30%.

### 2.4 Wavelet Multi-Resolution Analysis (Mallat, 1989)

Decompose a signal into approximation coefficients (full coverage, coarse) plus
detail coefficients (targeted, fine-grained) at each scale.

Translation: Instead of selecting K nodes and giving them maximum detail, encode
the entire codebase at adaptive resolution across multiple levels. Each level
doubles detail density while covering fewer entities.

### 2.5 Lloyd-Max Quantization

Allocate more representation capacity (tokens) to regions with higher information
content (task-relevant detail), less capacity to low-variance regions (stable
infrastructure code).

---

## 3. Proposed Design: Multi-Resolution Lattice Format (MRLF)

### 3.1 Core Principle

Progressive coverage, not fixed selection. Encode the entire codebase at adaptive
resolution across 4 levels. Each level doubles detail density while covering fewer
entities.

### 3.2 Resolution Levels

| Level | What it encodes | Tokens per entity | Coverage |
|-------|----------------|-------------------|----------|
| L0: TREE | Package/directory structure | ~1 | 100% of repo |
| L1: INDEX | Every module with top exports | ~4 | 100% of modules |
| L2: SYM | Public symbols ranked by centrality | ~5 | Top N by PageRank |
| L3: FOCUS | Task-relevant behavioral detail | ~25 | Top K task-relevant nodes |
| GAPS | Missing information + drill targets | ~20 | 3-5 bullets |

### 3.3 Token Budget Model

| Level | Budget Cap | Formula |
|-------|-----------|---------|
| L0 | 150 tokens | min(N_pkg × 1, 150) |
| L1 | 400 tokens | min(N_mod × 4, 400) |
| L2 | 1500 tokens | min(N_sym × 5, 1500) |
| L3 | 2000 tokens | K × 25 where K ≤ 80 |
| GAPS | 100 tokens | 3-5 bullets |
| **Total max** | **~4150 tokens** | **For ANY repo size** |

### 3.4 Scaling Predictions

| Repo | Nodes | Raw Tokens | MRLF Primary | CCR |
|------|-------|-----------|-------------|-----|
| Flask | 1,712 | ~18K | ~2,100 | 88.3% |
| FastAPI | ~4K | ~28K | ~2,800 | 90.0% |
| Django | 45,457 | ~80K | ~3,800 | 95.3% |
| 100K-node repo | 100K | ~500K | ~4,150 (cap) | 99.2% |

### 3.5 Why This Solves the Node Selection Problem

Current format: LLM sees 15 nodes, has zero awareness of the other 1,697. If
the 15 are wrong → catastrophic failure.

MRLF format: LLM always sees the full module map and symbol index. Even if L3
FOCUS picks slightly wrong nodes, the LLM can:

1. Identify from L1/L2 that relevant modules exist.
2. Reason about what's in scope but not detailed.
3. Make targeted drill-down requests based on real information, not guesswork.

### 3.6 Two-File Architecture

#### File 1: Primary Clue (MRLF)

- Always sent to LLM — this IS the context.
- Contains: TREE + INDEX + SYM + FOCUS + GAPS.
- Size: 1K–4K tokens regardless of repo size.
- Designed to be sufficient for 70%+ of tasks.

#### File 2: Detail Store (retrieved on demand via MCP)

- Never sent upfront — accessed record-by-record.
- Per-symbol records with: full call graph, source snippet, complexity analysis,
  confidence breakdown, edge weights and evidence.
- Access pattern: LLM reads GAPS in File 1 → requests specific records from File 2.
- This is the successive refinement step (R₁ + R₂ achieving D₂ < D₁).

### 3.7 Format Serialisation

No JSON. No XML. Plain text with code-like delimiters that LLMs are natively
trained on. Section markers use `-- SECTION` prefix. Header uses `=CC v2`.
Indentation is significant. Pure information, zero syntactic overhead.

### 3.8 Structural Extraction Layers

| Layer | Source | Failure Mode |
|-------|--------|-------------|
| L0 TREE | os.listdir + file extensions | Cannot fail |
| L1 INDEX | File line counts + top-level names | Cannot fail (AST parse) |
| L2 SYM | PageRank on call graph + AST | Might rank poorly, but all symbols listed |
| L3 FOCUS | Task-conditioned projection | Can fail, but bounded to FOCUS only |
| GAPS | Confidence threshold | Explicitly flags what L3 missed |

---

## 4. Constraints Under Consideration

### 4.1 Active Constraints (with rationale)

#### C1: Fixed Token Ceiling — 4,150 tokens maximum for primary clue

**Rationale:** Rate-Distortion theory says there's a minimum rate below which target
fidelity is impossible. But our constraint works from the other direction — the
consumer LLM has a finite context window and the clue competes with the user's
question, conversation history, and system prompt for space. If the clue exceeds
~5K tokens, it dominates the context budget and becomes the problem (raw source
re-ingestion) rather than the solution.

The 4,150 cap was derived from: typical context window 128K tokens, typical
coding conversation 8K–30K tokens already committed, clue should be ≤ 5% of
remaining budget to leave room for reasoning. In practice the clue rarely hits
the cap — most repos produce 1.5K–3K token clues.

This constraint is scale-invariant: Flask and Django both fit under it. That's the
mathematical property we need — bounded encoding for unbounded input.

#### C2: 100% Structural Coverage at L0-L1

**Rationale:** Data Processing Inequality. If we discard modules, we cannot answer
questions about them. L0 (directory tree) and L1 (module index with exports) must
cover every file in the repo, or we violate the sufficiency condition. The cost is
~550 tokens combined (L0: 150, L1: 400) — this is non-negotiable budget allocated
to structural completeness.

This is the single biggest design change from prior formats. All three previous
formats started by selecting K nodes and discarding everything else. MRLF starts
from the full repo and compresses downward.

#### C3: No JSON, No Structured Markup in Consumer Artifact

**Rationale:** MDL. Every `{`, `}`, `"key":`, `,` is a token that carries zero
task-answer information. JSON formatting consumes 15–25% of tokens in typical
clue files. LLMs are trained on billions of lines of plain text, code, and
markdown — they parse indented plain text natively. The format should exploit
what LLMs already know, not impose external structure that costs tokens.

Counterpoint: JSON is machine-parseable. But the consumer is an LLM, not a
JSON parser. The MCP tool for human conversion (the "ETW trace → log" analogy)
can parse the plain-text format just as easily.

#### C4: Task-Conditioning at L3 Only

**Rationale:** L0–L2 are task-independent (same for any question about the repo).
Only L3 FOCUS is task-conditioned (shaped by the specific question). This
separation means L0–L2 can be computed once and cached, with only L3 regenerated
per task. It also means that if the task-conditioning fails (wrong focus), the
LLM still has the full repo map from L0–L2 to reason from.

#### C5: GAPS Section Must Exist

**Rationale:** Successive refinement requires the first-stage output to signal where
refinement is needed. The GAPS section serves as the "pointer" to File 2 — it
tells the LLM which symbols or modules are under-resolved and should be drilled
into. Without GAPS, the LLM has no principled way to decide when to drill.

#### C6: Centrality Ranking via PageRank (L2)

**Rationale:** Code call graphs are directed graphs. PageRank (or eigenvector
centrality) identifies nodes that are most "reachable" — symbols that many other
symbols depend on. These are the symbols most likely to appear in any task answer,
regardless of task type. This is a better ranking than confidence (which is a
projection-specific score) or alphabetical (which has no information content).

The cap at ~300 symbols (1500 tokens) ensures L2 doesn't dominate the budget
while still covering the core API surface of even large repos.

#### C7: Detail Store (File 2) is Record-Level, Not Monolithic

**Rationale:** File 2 must support random access — the LLM requests one symbol's
detail record at a time via MCP. If File 2 were a monolithic dump, retrieving it
would defeat the purpose (back to raw-source-first). Record-level access means the
successive refinement cost (R₂) is proportional to how many records are actually
needed, not to the total repo size.

#### C8: Multi-Language Support via Uniform AST Extraction

**Rationale:** L0 and L1 are language-agnostic (directory listing + file scan).
L2 and L3 require AST extraction. The current codebase already has extractors for
Python, TypeScript, and Go. The format does not embed language-specific constructs
— it normalises to: module, class, function, method. This keeps the format
consistent regardless of source language.

#### C9: Repo-Size Independence

**Rationale:** This is the mathematical core — the encoding rate must be bounded
while the source size grows unboundedly. The budget caps at each level enforce
this. If a repo has 500 modules and the L1 budget is 400 tokens, the renderer
must select and compress to fit. This forces progressive lossy compression at
each level rather than allowing the output to grow with input.

MDL: If the model description length grows with the data size, you're encoding
the data, not the model. The clue is the model; its size must stay bounded.

### 4.2 Constraints NOT Under Consideration (with rationale)

#### NC1: Human Readability

**Not considered because:** The consumer is an LLM. Human readability is handled
by a separate MCP tool that converts the MRLF format to a human-friendly view
(the "ETW trace → log file" analogy from the user). Optimising for both human
and LLM consumption is a conflicting constraint — JSON is human-readable but
token-expensive; natural language is human-friendly but imprecise for machines.
We optimise for the LLM and build a converter for humans.

#### NC2: Round-Trip Losslessness

**Not considered because:** The clue is a lossy compression of the source. Rate-
distortion theory explicitly permits and requires distortion for compression.
The prior approach attempted lossless round-trip (graph → JSON → graph) which
contributed to bloated artifacts. The clue does not need to reconstruct the
source — it needs to provide enough information to answer questions about it.
The source is always available on disk for drill-down.

#### NC3: Backward Compatibility with Poisoned/Plan A/Plan B/Hybrid Formats

**Not considered because:** All prior formats failed to meet H2 (fidelity 0.85).
There is no installed base of consumers depending on these formats. Clean break
is appropriate. Old test fixtures will be archived, not migrated.

#### NC4: Embedding Raw Source Code in the Primary Clue

**Not considered because:** Including source snippets in File 1 would break the
token ceiling constraint (C1). A 20-line function body is ~100 tokens; including
even 15 such snippets would consume the full FOCUS budget with code rather than
compressed behavioural summaries. Source code is available in File 2 (detail
store) for on-demand retrieval. The primary clue provides pointers (file + line
range), not content.

#### NC5: Per-Node Confidence Scores in Consumer Artifact

**Not considered because:** The poisoned format devoted ~41% of clue bytes to
confidence payload. The MRLF design replaces per-node confidence with a single
GAPS section that lists 3–5 missing-information bullets. This is the MDL-optimal
approach: instead of encoding uncertainty about every node (most of which is
0.9+ and useless), encode only the actionable gaps.

#### NC6: Streaming/Incremental Update of Primary Clue

**Not considered because:** The primary clue is small (1–4K tokens) and cheap to
regenerate from the canonical graph. Delta-update complexity is not justified for
a file this size. If the source changes, regenerate the clue. The canonical graph
(which IS expensive to rebuild) supports incremental update — but that's a
separate concern from the consumer-facing format.

#### NC7: Supporting Queries That Span Multiple Repositories

**Not considered because:** Each clue file describes one repository. Cross-repo
questions (e.g., "how does service A's API affect service B?") require composing
multiple clue files. That's an orchestration concern for the MCP layer, not a
format concern. The format must be self-contained per repo.

#### NC8: Optimising for a Specific LLM Family

**Not considered because:** The format uses universal plain text — no model-specific
tokens, no chat-template tags, no function-call schema. Any LLM that can parse
indented text can consume it. Optimising for Claude vs GPT vs Gemini token
boundaries would create vendor lock-in and fragile format choices.

#### NC9: Real-Time / Low-Latency Generation

**Not considered because:** Clue generation is a batch operation — it runs when the
user triggers it or a CI job executes. It does not need to complete in sub-second
time. L0–L2 generation is pure file I/O and AST parsing (already fast). L3 may
involve PageRank computation on the call graph, but even for Django (45K nodes,
55K edges) this completes in seconds. Latency is not a binding constraint.

#### NC10: Formal Schema Validation of the Primary Clue

**Not considered because:** JSON Schema validation was part of the poisoned format
and contributed to format verbosity (fields existed to satisfy schema, not to help
the LLM). The MRLF format uses structural conventions (section markers, indentation
rules) rather than a formal schema. A linter can enforce conventions without requiring
the format to carry schema metadata.

---

## 5. Risk Analysis and Edge Cases

### 5.1 Token Ceiling Risks (C1: 4,150 token cap)

The fixed ceiling is the sharpest constraint. Here's where it breaks:

| Risk | Scenario | Impact | Mitigation |
|------|----------|--------|------------|
| R1: TREE overflow | Monorepo with 2000+ directories | L0 truncates; some package subtrees invisible | Collapse deep paths: `a/b/c/d/` → `a/.../d/`. Show depth-2 tree + count. |
| R2: INDEX overflow | Repo with 500+ modules, each gets ~4 tokens → 2000 needed vs 400 budget | 75% of modules dropped from L1 | Rank modules by import fan-in. Show top 100 + "...and 400 more modules". GAPS flags the cutoff. |
| R3: SYM overflow | Repo with 5000+ symbols, each gets ~5 tokens → 25K needed vs 1500 budget | 94% of symbols dropped from L2 | PageRank sorts. Top ~300 symbols shown. This is acceptable — 300 symbols covers the core API of even large repos. |
| R4: FOCUS too shallow | Task needs 30 symbols at ~25 tokens each = 750 tokens, but only 2000 budget | Can only detail ~80 nodes max | For tasks needing broader coverage, L3 becomes a map of entry points rather than deep behavioural description. Drill-down compensates. |
| R5: Tiny repo waste | Repo with 10 files, 50 symbols — clue is 400 tokens, 3750 budget wasted | Inefficiency, not failure | Not a problem. Smaller clue = cheaper. No padding needed. |
| R6: Polyglot repos | Mixed Python/TS/Go — each language adds AST overhead | L1/L2 count grows faster | Language-agnostic L0/L1. L2 SYM is unified across languages. Budget still holds. |
| R7: Generated code | Repo with auto-generated files (protobuf, codegen) | Inflates node count, drowns real code in L2 | Filter: ignore known generated directories (node_modules, __pycache__, .generated/, vendor/) |
| R8: Flat repos | Single-directory repo with 200 files, no package structure | L0 TREE carries zero information (~2 tokens) | L0 budget flows to L1/L2 instead (adaptive reallocation). |

**Critical edge case: when 4,150 tokens is genuinely insufficient.**

This happens when the task requires understanding relationships across many modules
simultaneously — e.g., UC-48 "shared library impact across 50 consumers". At 4K
tokens the clue can list the 50 consumers (in L2) but cannot describe HOW each
consumes the library. The LLM must drill into File 2 for each consumer.

This is by design: DDR ≤ 0.40 means we accept 40% drill-down rate. The token
ceiling forces the system into the two-file architecture rather than trying to
solve everything in one pass.

### 5.2 File Architecture Clarification

**The system generates 2 files per repo, not 5.**

| File | Contents | Generated When | Size |
|------|----------|---------------|------|
| File 1: Primary Clue (`.codeclue`) | L0 TREE + L1 INDEX + L2 SYM + L3 FOCUS + GAPS — all in one file | On `generate_clue` command or CI trigger | 1–4K tokens |
| File 2: Detail Store (`.codeclue-detail`) | Per-symbol records with source snippets, full call graphs, complexity data | Generated alongside File 1 | Proportional to repo size; stored on disk, accessed record-by-record |

L0–L3 and GAPS are sections within a single File 1, not separate files. The
resolution levels are logical layers inside one artifact.

The reason for 2 files rather than 5:

- **Single-file primary:** The LLM loads one file into context. Splitting L0/L1/L2/L3
  into separate files would require 4 MCP loads or prompt-assembly steps. One file
  = one context injection = zero orchestration overhead.
- **Detail store separate:** Because it can be large (proportional to repo) and is
  accessed selectively. Never dumped wholesale into context.

### 5.3 Token Efficiency Analysis — MRLF vs Alternatives

#### MRLF (proposed lossy format)

| Metric | Flask (1.7K nodes) | FastAPI (4K nodes) | Django (45K nodes) | 100K nodes |
|--------|-------------------|-------------------|-------------------|------------|
| Raw source tokens | ~18,000 | ~28,000 | ~80,000 | ~500,000 |
| MRLF primary clue | ~2,100 | ~2,800 | ~3,800 | ~4,150 |
| CCR | 88.3% | 90.0% | 95.3% | 99.2% |
| Tokens per node (average) | 1.23 | 0.70 | 0.08 | 0.04 |
| Information density | High | High | High (heavily compressed) | Very high (extreme compression) |

#### What if compression were lossless? (NC2 analysis)

Lossless means the clue must encode enough information to reconstruct the full
canonical graph — every node ID, every edge, every source anchor, every symbol name.

| Metric | Flask | FastAPI | Django | 100K nodes |
|--------|-------|---------|--------|------------|
| Minimum lossless encoding* | ~12,000 tokens | ~22,000 tokens | ~180,000 tokens | ~850,000 tokens |
| CCR (lossless) | 33% | 21% | -125% (LARGER than source) | -70% |
| Lossless vs MRLF ratio | 5.7× larger | 7.9× larger | 47× larger | 205× larger |

*Estimated as: N_nodes × ~3 tokens (name + type + file) + N_edges × ~2 tokens
(from + to) + overhead. This is the absolute minimum with zero formatting.

**Where lossless fails:**

1. **CCR collapse at scale.** For Django, lossless clue tokens exceed raw source tokens.
   The graph captures derived information (call edges, containment edges) that doesn't
   exist verbatim in source — reconstructing it requires MORE tokens than the source
   itself. This was exactly the Django failure at v0.6.3 (64MB graph vs 18MB source).

2. **H1 violation.** The hypothesis requires CCR ≥ 80%. Lossless encoding achieves
   this only on Flask (33% < 80% → FAIL even on the smallest repo). Lossless is
   mathematically incompatible with our compression target.

3. **Context window saturation.** A 180K token lossless Django clue exceeds the context
   window of most models (128K). The clue literally doesn't fit.

4. **Diminishing returns.** Most of the lossless payload is edges and node metadata
   that the LLM never needs for any single task. You're paying for 45K nodes to
   answer a question about 3 of them.

**Conclusion:** Lossless is not merely "not considered" — it is provably incompatible
with H1 (CCR ≥ 80%) at any scale beyond trivial repos. Rate-distortion theory says:
for a given rate budget R, increasing D (distortion) is the ONLY way to compress.
The question is not "should we be lossy?" but "where exactly should we lose information?"
MRLF's answer: lose detail at low-priority nodes (L2 is one-line summaries),
preserve full detail at high-priority nodes (L3 FOCUS), and provide recovery via
File 2 for everything in between.

#### What if we kept per-node confidence? (NC5 analysis)

Per-node confidence means: for each of N nodes in the projection, include a float
(confidence 0.0–1.0) plus a suggested action string.

Token cost of per-node confidence per format:

| Format | Fields per node | Tokens per node | N nodes × cost |
|--------|----------------|-----------------|----------------|
| Poisoned (actual) | confidence, p_context_miss, p_dependency_miss, p_hallucination, suggested_actions, rationale | ~45 tokens | 15 × 45 = 675 tokens |
| Compact confidence | confidence float only | ~2 tokens | 15 × 2 = 30 tokens |
| MRLF GAPS (actual) | 3-5 bullets for the whole clue | ~100 tokens total | 100 tokens total |

Per-task token efficiency impact:

| Task Type | Per-node conf useful? | Token cost | Value |
|-----------|----------------------|-----------|-------|
| UC-01 Orientation | No — you need structure, not uncertainty scores | +30 to +675 tokens wasted | Zero |
| UC-09 Crash analysis | Marginally — tells you which symbols are uncertain | +30 tokens, might save one drill-down | Low |
| UC-16 PR impact | No — you need call chains, not confidence numbers | +30 to +675 tokens wasted | Zero |
| UC-33 Security audit | Yes — low-confidence auth symbols flag risk | +30 tokens, genuinely useful | Medium |
| UC-21 Refactoring | No — you need callers/callees, not confidence | +30 to +675 tokens wasted | Zero |

**Conclusion:** Per-node confidence is useful for ~2 of 50 use cases (UC-09, UC-33)
and costs 30–675 tokens per task. The GAPS section captures the same actionable
information ("these specific symbols need drill-down") at a fixed 100 tokens for
ALL tasks. The break-even is:

- GAPS: 100 tokens, covers all tasks.
- Compact per-node (2 tokens × 15 nodes): 30 tokens, but the LLM must figure out
  what to DO with bare numbers — no action guidance.
- Full per-node (poisoned): 675 tokens, explicit guidance but 85% wasted on high-
  confidence nodes where the guidance is "no action needed".

GAPS is more token-efficient for all task categories except the edge case where the
LLM needs to compare confidence levels across many nodes simultaneously (e.g.,
"which of these 15 symbols is least trustworthy?"). That specific use case is
addressed by File 2, which carries full confidence breakdowns per symbol.

---

## 6. Success Factor Mapping

| # | Success Factor | Target | How MRLF Achieves It |
|---|---------------|--------|---------------------|
| 1 | CCR ≥ 0.85 for 70-80% of tasks | ≥ 85% | Budget cap ~4K tokens; CCR improves with repo size |
| 2 | DFCR ≥ 0.60-0.70 clue-only | ≥ 60% | Full repo coverage at L0-L2 eliminates wrong-15-nodes failure |
| 3 | DDR ≤ 0.40 | ≤ 40% | GAPS section bounds missing info; most tasks covered by L0-L3 |
| 4 | FU ≥ 0.10 post-drill | ≥ 0.10 | File 2 provides full source snippets for fidelity boost |
| 5 | Scale invariance | Small AND large repos | Capped budgets; logarithmic compression as repo grows |
| 6 | Multi-repo validity | Not just Flask | L0-L2 extraction is projection-independent; works on any repo |

---

## 6. What This Design Kills From Prior Approaches

1. No more JSON — zero braces, zero quoted keys, zero commas.
2. No more 15-node selection — full repo always visible at coarse resolution.
3. No more per-node confidence arrays — one GAPS section.
4. No more format overhead — no hashes, AST paths, byte offsets, policy blocks.
5. No more Flask-only success — structural extraction works on any repo with files.
6. No more scale failure — Django gets the same ~4K token budget as Flask.

---

## 8. Open Questions — Resolved

### OQ1: L2 Ranking Algorithm

**Question:** PageRank is proposed but not validated. Compare PageRank vs
betweenness centrality vs degree centrality for symbol ranking?

**Resolution: Use PageRank, validate empirically against degree centrality baseline.**

Rationale:
- PageRank measures transitive reachability ("how many paths pass through this
  symbol?"). This directly maps to our use case: high-PageRank symbols are the
  ones most likely to appear in any task answer because they sit on many call paths.
- Degree centrality (count of direct edges) over-weights hub nodes that have many
  direct connections but may not be on critical paths. E.g., a utility function
  called by 50 test files has high degree but low task relevance.
- Betweenness centrality (fraction of shortest paths passing through a node) is
  expensive to compute: O(V × E) for unweighted graphs. On Django (45K nodes,
  55K edges) this is ~2.5 billion operations vs O(V + E) for PageRank.

Action: Implement PageRank as primary, degree centrality as cheap fallback for
repos where call graph extraction fails. Compare top-50 overlap in the evaluation.

### OQ2: L3 FOCUS Generation Method

**Question:** Current projector selects by confidence + keyword overlap. Should L3
use a fundamentally different method?

**Resolution: Two-stage selection — keyword anchoring + graph walk.**

Stage 1 — Keyword anchoring: Extract noun phrases and symbol-like tokens from the
task question. Match against L2 SYM symbol names and module names. These are the
"seed" nodes.

Stage 2 — Graph walk: From seed nodes, walk the call graph (1-2 hops outward for
callers AND callees). Collect all reached nodes. Rank by distance from seeds
(closer = higher priority). Take top K=80 nodes.

Why this is better than the current approach:
- Current approach selects by confidence alone — misses nodes that are low-confidence
  but task-relevant (the httpx/nest/gin failure mode).
- Keyword anchoring grounds the selection in the actual question.
- Graph walk discovers the neighbourhood context that makes individual nodes
  interpretable (you can't understand `dispatch_request` without knowing who calls
  it and what it calls).

### OQ3: Budget Tuning

**Question:** The 150/400/1500/2000/100 split is theoretical. Validate empirically?

**Resolution: Yes, but after first implementation — not before.**

The budget split is a design hypothesis. We will:
1. Implement the renderer with the proposed budgets.
2. Generate clues for all test repos (Flask, FastAPI, Django, httpx, Nest, Gin, Express).
3. Measure actual token counts per level.
4. Run the full task benchmark.
5. Adjust budgets based on which levels are under/over-used.

Premature tuning without empirical data is how we got into the Plan A vs Plan B
format war. Implement first, measure, then tune.

One known adjustment: for small repos (≤ 30 modules), L1 won't need its full 400
budget. Unused L1 budget should flow to L2 or L3 rather than being wasted. This
is an adaptive reallocation rule, not a fixed split. The total cap (4150) is fixed;
the per-level allocation is soft.

### OQ4: Detail Store Format

**Question:** Should File 2 use plain text or structured format (JSON)?

**Resolution: JSON Lines (.jsonl) — one JSON object per line, one line per symbol.**

Rationale:
- File 2 is never sent raw into an LLM prompt. It's read by MCP tool code (Python),
  which parses it and injects specific records into the prompt on demand.
- JSON Lines is trivially parseable by Python (`json.loads(line)`), supports
  random access via line seek, and is appendable.
- Plain text in File 2 would require a custom parser with no benefit — no LLM will
  ever see it directly.
- Each line: `{"symbol": "Flask.wsgi_app", "file": "app.py", "lines": [1566, 1624], "source": "...", "calls": [...], "called_by": [...], "complexity": {...}, "confidence": {...}}`
- For MCP delivery: the tool reads the JSONL record and formats it as a plain-text
  snippet injected into the conversation. The MCP tool controls the prompt format,
  not the storage format.

### OQ5: What Goes in GAPS

**Question:** How does the system decide what goes in GAPS? Confidence-based,
coverage-based, or something else?

**Resolution: Three-signal merge.**

1. **Coverage signal:** After L3 FOCUS is generated, check which keywords from the
   task question are NOT covered by any node in L3. Any unmatched keyword maps to
   a "missing from focus" gap bullet.

2. **Confidence signal:** Among L3 FOCUS nodes, any with structural confidence < 0.70
   generates a gap bullet: "X may have unresolved dependencies (confidence 0.65)".

3. **Scope signal:** If the question mentions modules/files that exist in L1 INDEX
   but have zero symbols in L2 SYM (because they fell below the PageRank cut), that
   generates a gap bullet: "Module X exists but is not indexed in detail".

Maximum 5 bullets. Prioritised by: (1) uncovered question keywords, (2) low-
confidence focus nodes, (3) unindexed but mentioned modules. Each bullet includes
a drill target: `> drill: file:line-range` or `> drill: symbol_name`.

### OQ6: Validation Repos

**Question:** Use current 7-repo set or fresh repos to avoid overfitting?

**Resolution: Both — 7 existing for regression + 3 fresh for validation.**

Existing repos (regression baseline):
- Flask, FastAPI, httpx, Express, Nest, Gin, Django

Fresh repos (validation — never seen by any prior format):
- **requests** (Python, ~3K nodes) — well-known, moderate size, different API style
- **react** (TypeScript/JavaScript, ~15K nodes) — large frontend framework, tests monorepo handling
- **kubernetes/client-go** (Go, ~20K nodes) — large Go repo, tests Go extraction quality

Fresh repos are selected to cover:
- A Python library that is NOT a web framework (requests)
- A large TypeScript project that is NOT a backend framework (react)
- A large Go project that is NOT a microframework (client-go)

### OQ7: Tokeniser Dependency

**Question:** Token counts vary by model. Use word counts with conversion factor?

**Resolution: Budget in whitespace-delimited words. Conversion factor ~1.3 tokens/word.**

Rationale:
- Token counts vary: GPT-4 tokeniser ≠ Claude tokeniser ≠ Gemini tokeniser.
- Word counts are tokeniser-agnostic and easier to reason about.
- Empirical ratio from our data: 1 whitespace-delimited word ≈ 1.3 tokens (± 0.2)
  across GPT-4, Claude, and Gemini tokenisers.
- Budget caps reframed as words:

| Level | Token Budget | Word Budget (÷ 1.3) |
|-------|-------------|---------------------|
| L0 | 150 | ~115 words |
| L1 | 400 | ~310 words |
| L2 | 1500 | ~1150 words |
| L3 | 2000 | ~1540 words |
| GAPS | 100 | ~75 words |
| **Total** | **4150** | **~3190 words** |

The renderer will count words, not tokens. The 1.3 conversion factor will be
validated during the first benchmark run against at least 2 tokenisers.

---

## 9. Fresh-Start Reconstruction Guide

If this session is lost and work must restart from scratch, this section contains
everything needed to reconstruct the design intent.

### 9.1 The One-Sentence Design

A multi-resolution plain-text clue file that compresses any codebase into a fixed
≤4150-token artifact by encoding the full repo at progressively finer resolution
(directory → modules → symbols → focused behaviour → gaps), paired with a separate
detail store accessed record-by-record via MCP for the ~30% of tasks that need deeper
information.

### 9.2 Why This Design Exists

All prior formats (Poisoned, Plan A, Plan B, Hybrid) failed because they selected
15 nodes from the full graph and discarded everything else. This violates the Data
Processing Inequality — if the 15 nodes are wrong, fidelity is zero. The Flask-only
success (localization 0.93) vs everything-else failure (0.20–0.45) proves the
projector's node selection, not the format, is the bottleneck. MRLF fixes this by
never discarding information entirely — every module and symbol appears at some
resolution level. The question shifts from "did we pick the right 15 nodes?" to
"is the progressive summary at each level sufficient?"

### 9.3 Mathematical Basis (Summary)

- Rate-Distortion (Shannon): Bounded rate ↔ bounded tokens. Lossy compression required.
- Sufficient Statistic (Fisher-Neyman): Clue must preserve all task-answer-relevant
  information. 100% repo coverage ensures this.
- Successive Refinement (Equitz-Cover): Two-file split. File 1 sufficient for 70%.
  File 2 refines for the remaining 30%.
- MDL (Rissanen): Shortest description that reproduces data = best model. No format overhead.
- Wavelet MRA (Mallat): Multi-resolution = coarse everywhere, fine where it matters.

### 9.4 Critical Design Decisions (Non-Negotiable)

1. 2 files per repo, not 5. File 1 is a single all-in-one clue. File 2 is JSONL detail store.
2. No JSON in File 1. Plain text with `-- SECTION` markers.
3. 100% repo coverage at L0-L1. Every directory and module visible.
4. Fixed ~4150 token ceiling. Scale-invariant.
5. L3 FOCUS is the only task-conditioned layer. L0-L2 are static per repo.
6. GAPS section is mandatory. It's the pointer to File 2.
7. PageRank for L2 symbol ranking.
8. L3 FOCUS uses keyword anchoring + graph walk (not confidence-only selection).
9. File 2 uses JSONL format (one record per symbol, machine-parsed by MCP tool).
10. Budget caps are in words (~3190 total), tokeniser-agnostic.

### 9.5 Key File Locations

- This design document: `docs/New-Design-Basis.md`
- Prior study design (superseded): `docs/12-unpoisoned-clue-study-design.md`
- Prior format renderers: `src/codeclue_research/clue_view_plan_a.py`, `clue_view_plan_b.py`, `clue_view_hybrid.py`
- Existing extractor: `src/codeclue_research/extractor.py`
- Prior benchmark results: `experiments/reports/action-benchmark-results.json`
- Success factor definitions: `source/CodeClue-PRD-v0.3.0-mvp-FINAL.md` (Section 4.2)
- MCP server scaffold: `src/codeclue_mcp/server.py`

### 9.6 What To Implement (Ordered)

1. New renderer: `src/codeclue_research/clue_view_mrlf.py` — canonical graph + question → File 1 text.
2. Detail store generator: produces `.codeclue-detail` JSONL alongside File 1.
3. MCP tool: `drill_detail` — reads a symbol from File 2, formats into prompt snippet.
4. Benchmark harness: 50 use cases across 10 repos (7 existing + 3 fresh), measure CCR/DFCR/DDR/FU.
5. Budget tuning pass: adjust L0/L1/L2/L3/GAPS splits based on empirical data.

---

## 10. Future TODOs (Deferred — Revisit Before Commercialisation)

### TODO-1: Clue File Encryption

**Requirement:** Both File 1 (.codeclue) and File 2 (.codeclue-detail) must be
encrypted at rest and in transit to prevent theft of proprietary code structure.

**Impact on architecture:**
- MCP server must decrypt before injecting into LLM prompt
- Key management needed (per-repo or per-org encryption keys)
- File 2 random-access becomes "decrypt-record" not "read-line"
- May need envelope encryption: fast symmetric for file content, asymmetric for key exchange

**When to address:** After format validation is complete. Encryption is orthogonal
to format correctness — it wraps the artifact without changing its content.

### TODO-2: Minimum Hardware Recommendations

Document the minimum hardware specs for the MCP server based on profiled performance:
- Extraction time vs CPU cores and disk speed
- Render time vs memory and CPU
- File 2 random access vs disk latency
- Server-client architecture for large repos (server creates clue, clients consume)

### TODO-3: TypeScript JSDoc Extraction

The TypeScript extractor (extract_typescript.py) uses regex-based extraction with
no JSDoc comment extraction. Same issue as the Go extractor had before the doc
comment fix. Needed for Nest/TypeORM quality.

---

## 10b. Knowledge Type Analysis — Why TF5 Fails and How To Fix It

### Background

Phase 4 testing showed TF5 (security/compliance) at 0/4 sufficient across all
repos, while TF2 and TF3 achieve 4/4. All other gates pass (DFCR=0.650 overall).
This section analyses the root cause at the knowledge representation level and
proposes a durable, language-agnostic solution.

### Knowledge Type Taxonomy

Every gold fact in the evaluation set falls into one of five knowledge types:

| Type | Definition | Example | Extracted by MRLF? |
|------|-----------|---------|-------------------|
| **Structural** | "X exists in file Y, is type Z" | "Blueprint is in blueprints.py" | YES — L0-L2 |
| **Relational** | "X calls/depends on/extends Y" | "RequestContext depends on AppContext" | YES — L3 calls, extends |
| **Declarative** | "X does Y" (documented purpose) | "stores sessions in signed cookies" | YES — docstrings |
| **Mechanistic** | "X achieves Y by using Z" (implementation mechanism) | "uses URLSafeTimedSerializer with SECRET\_KEY" | **NO** |
| **Invariant** | "X guarantees Y under condition Z" (safety property) | "raises RuntimeError if SECRET\_KEY not set" | **NO** |

### Task Family Knowledge Requirements

| TF | Primary knowledge types | MRLF provides? | Phase 4 result |
|----|------------------------|----------------|----------------|
| TF1 Refactoring | Structural + Relational | YES | 2/4 |
| TF2 Impact | Relational + Declarative | YES | 4/4 |
| TF3 Edit localization | Structural | YES | 4/4 |
| TF4 Debugging | Relational + Mechanistic | PARTIAL | 3/4 |
| TF5 Security | **Mechanistic + Invariant** | **NO** | **0/4** |

TF5 fails because it requires two knowledge types (mechanistic and invariant)
that the current extractor does not produce. This is not a format problem — the
format has capacity. It is a data pipeline problem — the right information is
never extracted from source.

### Where Mechanistic and Invariant Knowledge Lives in Source Code

**Mechanistic knowledge** (what tools/libraries implement a behavior):

1. Import statements — `from itsdangerous import URLSafeTimedSerializer`
2. Function call arguments — `URLSafeTimedSerializer(secret_key, salt=salt)`
3. Variable assignments — `serializer = URLSafeTimedSerializer(...)`

**Invariant knowledge** (what guarantees/error-handling exists):

1. Exception raises — `raise RuntimeError("session is unavailable")`
2. Assert statements — `assert secret_key is not None`
3. Guard clauses — `if not secret_key: raise ...`
4. Doc comments about safety properties — "protected by RWMutex"

### Design Options Evaluated

Five options were evaluated for extracting mechanistic and invariant knowledge:

**Option A: Deep AST Pattern Extraction**

Scan AST for known security-relevant targets (crypto imports, timing-safe
comparisons, auth decorators). Annotate symbols with `uses: {library}`.

- Pros: Precise for known patterns. Compact annotations.
- Cons: Requires per-language vocabulary of known patterns. New libraries need
  vocabulary updates. Go/TypeScript AST parsing limited.
- Cross-language stability: LOW.

**Option B: Design by Contract Extraction (Hoare Logic)**

Extract preconditions, postconditions, and error paths for every function.
Inspired by Meyer's Design by Contract and Hoare Logic {P}C{Q}.

- Pros: Language-agnostic in concept. Formally sound.
- Cons: Full-precision precondition extraction from arbitrary code is a hard
  static analysis problem approaching theorem proving.
- Cross-language stability: HIGH in theory, impractical in implementation.

**Option C: Behavioral Fingerprinting**

Extract a fingerprint of HOW a symbol works: import set, call pattern, exception
pattern. The LLM interprets the fingerprint.

- Pros: No semantic understanding needed on our side. Compact.
- Cons: False positives (import of hashlib does not mean crypto is used).
- Cross-language stability: MEDIUM.

**Option D: Constraint Propagation via Graph Annotations**

Add constraint edges that propagate security-relevant properties through the
call graph. Analogous to taint analysis: a property at an import source
propagates to all reachable symbols.

- Pros: Elegant. Scales well — large repos benefit MORE.
- Cons: Computationally expensive. Over-propagation risk.
- Cross-language stability: HIGH (once graph exists).

**Option E: Hybrid Import Fingerprint + Raise Extraction (RECOMMENDED)**

Combine the cheapest, most verifiable parts:

1. **Import fingerprint** per module (already implemented). Propagate to symbols
   that belong to each module.
2. **Raise extraction** — scan Python AST for `ast.Raise`, extract exception
   class name. Go: regex for `panic(...)`. TypeScript: regex for `throw`.
3. Render in L3 FOCUS as two additional compact lines:
   `imports: itsdangerous`
   `raises: RuntimeError`

- Pros: Additive — no existing fields change. Verifiable — check if exception
  class appears in clue. No source code in clue. Uses existing AST walk.
- Cons: Go/TypeScript raise extraction is regex-based (less precise).
- Cross-language stability: HIGH for Python, MEDIUM for Go/TypeScript.
- Implementation effort: LOW (~1 hour).

### Evaluation Matrix

| Requirement | A | B | C | D | **E** |
|-------------|---|---|---|---|-------|
| No source code in clue | YES | YES | YES | YES | **YES** |
| Verifiable | HIGH | LOW | MEDIUM | MEDIUM | **HIGH** |
| Cross-language stable | LOW | HIGH | MEDIUM | HIGH | **MEDIUM** |
| Cross-size stable | HIGH | HIGH | HIGH | HIGH | **HIGH** |
| Implementation effort | HIGH | V.HIGH | MEDIUM | HIGH | **LOW** |
| Risk of regression | MEDIUM | HIGH | LOW | MEDIUM | **LOW** |
| Expected TF5 impact | +2-3/4 | +3-4/4 | +1-2/4 | +2-3/4 | **+2-3/4** |

### Decision

**Option E** selected for implementation. It is the minimum-risk, maximum-impact
choice that:

1. Captures the two missing knowledge types (mechanistic via imports, invariant
   via raises) without embedding source code.
2. Fits within the existing L3 FOCUS entry format and token budget.
3. Is verifiable: the presence of `imports: itsdangerous` and `raises: RuntimeError`
   in the clue can be checked against gold facts deterministically.
4. Is language-universal in concept: every language has imports and error-raising
   mechanisms. The extraction method differs (AST vs regex) but the output format
   is identical.

**Option D** (constraint propagation) is noted as the long-term evolution path for
a future version where security property propagation through the call graph would
give the LLM richer reasoning material. Deferred to post-validation.

---

## 11. Execution Plan

### 10.0 Current State (April 7, 2026)

**Done:**
- MRLF renderer implemented (`src/codeclue_research/clue_view_mrlf.py`)
- Detail store generator implemented (JSONL output)
- 38 unit tests passing
- Clues generated for 4 repos: Flask, httpx, Gin, FastAPI
- Token budgets confirmed: all 4 repos under ceiling (57–66%)

**Not done:**
- No raw-source baseline tokens computed (CCR denominator unknown)
- No Django scale test
- No LLM consumption test (no fidelity measurement)
- No ground-truth scoring
- No Nest/TypeORM/Express clues (TS extractor not wired to MRLF)
- Design doc OQ resolutions not empirically validated

### 10.1 Phase 1: Baseline Measurement (no LLM needed)

**Goal:** Compute CCR for every repo using actual token counts. This is pure
arithmetic — no LLM calls required.

**Steps:**

| Step | What | How | Output |
|------|------|-----|--------|
| 1a | Compute raw-source tokens for each repo | For each task question, identify the source files an LLM would need. Count tokens with tiktoken. | `raw_tokens` per repo |
| 1b | Compute MRLF clue tokens | Use tiktoken on the generated `.codeclue` files. | `clue_tokens` per repo |
| 1c | Compute CCR | `CCR = 1 - (clue_tokens / raw_tokens)` | CCR per repo |
| 1d | Run Django extraction + MRLF | Extract Django graph, render MRLF clue, measure tokens. | Django row in results |
| 1e | Report | Table with: repo, modules, symbols, raw_tokens, clue_tokens, CCR | Pass/fail per H1 |

**Gate:** CCR ≥ 0.85 for ≥ 70% of repos. If fails → revisit budget allocation
before proceeding to Phase 2.

**Raw baseline definition:** For each repo, raw_tokens = total tokens in all
Python/TypeScript/Go source files (excluding tests, docs, generated code).
This matches the "what would the LLM need to read" baseline.

**Effort:** ~1 hour. Script + run.

### 10.2 Phase 2: Ground-Truth Task Set

**Goal:** Define tasks with verifiable gold answers that can be scored without
an LLM judge.

**Steps:**

| Step | What | How | Output |
|------|------|-----|--------|
| 2a | Define 5 tasks per repo (1 per TF) | For each repo × task family, write a question + gold answer with: expected files, expected symbols, expected behavioural facts | Task manifest JSON |
| 2b | Use 4 repos × 5 TFs = 20 tasks minimum | Flask, httpx, FastAPI, Gin (Python + Go coverage) | 20 task definitions |
| 2c | Gold answer format | `{"question": "...", "gold_files": [...], "gold_symbols": [...], "gold_facts": [...]}` | Per-task gold files |
| 2d | Validate golds | Manually verify each gold answer against actual source code | Validated task set |

**Task family distribution per repo:**

| Repo | TF1 Refactor | TF2 Impact | TF3 Edit | TF4 Debug | TF5 Security |
|------|-------------|-----------|---------|----------|-------------|
| Flask | refactor request handling | config change impact | add new endpoint | trace exception path | audit session handling |
| FastAPI | refactor dependency injection | middleware change impact | add new route | trace async error path | audit CORS config |
| httpx | refactor transport layer | timeout config impact | add retry logic | trace connection lifecycle | audit TLS handling |
| Gin | refactor middleware chain | binding change impact | add new handler | trace context propagation | audit auth middleware |

**Gate:** 20 tasks with validated gold answers exist before Phase 3.

**Effort:** ~2-3 hours. Manual, requires reading source code.

### 10.3 Phase 3: Automated Localization Scoring (no LLM needed)

**Goal:** Measure whether the MRLF clue contains the gold symbols and files.
This is the same localization_accuracy metric used in v0.8.1 but applied to
the new MRLF format.

**Steps:**

| Step | What | How | Output |
|------|------|-----|--------|
| 3a | Build scorer | Parse MRLF clue text, extract all mentioned symbols and files. Compare against gold. | `mrlf_scorer.py` |
| 3b | Score file recall | `file_recall = files_in_clue ∩ gold_files / gold_files` | Per-task metric |
| 3c | Score symbol recall | `symbol_recall = symbols_in_clue ∩ gold_symbols / gold_symbols` | Per-task metric |
| 3d | Score localization accuracy | `loc = 0.4 × file_recall + 0.6 × symbol_recall` (same formula as v0.8.1) | Per-task metric |
| 3e | Score sufficiency | `sufficient = loc ≥ 0.60` | Per-task boolean |
| 3f | Report | Table per repo × TF, mean localization, % sufficient | Comparison vs v0.8.1 |

**Key comparison:**

| Metric | v0.8.1 Hybrid | Phase 3 Target |
|--------|--------------|---------------|
| Mean localization (Flask) | 0.932 | ≥ 0.85 (maintain) |
| Mean localization (non-Flask) | 0.275 | ≥ 0.50 (double) |
| Sufficient rate overall | 60% (6/10) | ≥ 65% (13/20) |

**Why Phase 3 before LLM tests:** Localization scoring is deterministic —
it checks whether the right symbols appear in the clue. If symbols are missing,
no amount of LLM reasoning will recover them. This is the cheapest, fastest
gate that catches the "wrong nodes selected" failure mode.

**Gate:** Mean localization ≥ 0.50 across all repos AND ≥ 0.80 on Flask.
If fails → fix L3 FOCUS selection before proceeding.

**Effort:** ~1-2 hours. Script + analysis.

### 10.4 Phase 4: LLM Consumption Test

**Goal:** Feed the MRLF clue to an LLM, have it answer the task question,
and score the answer against gold.

**Steps:**

| Step | What | How | Output |
|------|------|-----|--------|
| 4a | Build consumer prompt template | System prompt with clue, question, instruction to answer grounded in clue only | `mrlf_consumer_prompt.md` |
| 4b | Generate 20 consumer prompts | One per task: template + task question + MRLF clue | Prompt files |
| 4c | Run Arm B (clue-only) | Feed each prompt to Claude/GPT, collect answers | 20 response files |
| 4d | Run Arm A (raw-source-first) | Same questions but with raw source files instead of clue | 20 baseline responses |
| 4e | Score answers | Compare each answer against gold facts: fact_recall, fact_precision | Per-task fidelity |
| 4f | Compute DFCR | `DFCR = tasks where clue_fidelity ≥ 0.60 / total_tasks` | Overall DFCR |
| 4g | Compute DDR | `DDR = tasks where clue_fidelity < 0.60 / total_tasks` | Overall DDR |
| 4h | Report | Arm A vs Arm B comparison, per-TF breakdown | Full results table |

**Gate:** DFCR ≥ 0.60 AND DDR ≤ 0.40.

**Effort:** ~3-4 hours. LLM calls + manual gold scoring.

### 10.5 Phase 5: Drill-Down Test

**Goal:** For tasks that failed clue-only (DDR tasks), test whether File 2
detail records improve the answer.

**Steps:**

| Step | What | How | Output |
|------|------|-----|--------|
| 5a | Identify failed tasks | Tasks where clue_fidelity < 0.60 from Phase 4 | Drill candidate list |
| 5b | Simulate drill-down | For each failed task, append the relevant File 2 records to the clue prompt | Enhanced prompts |
| 5c | Re-run LLM | Get revised answers | Revised response files |
| 5d | Score revised answers | Same gold scoring as Phase 4 | Post-drill fidelity |
| 5e | Compute FU | `FU = mean(post_drill_fidelity - clue_only_fidelity)` for drill tasks | Fidelity uplift |
| 5f | Compute TRCR | `TRCR = 1 - (clue_tokens + drill_tokens) / raw_tokens` | Post-drill compression |
| 5g | Report | FU, TRCR, per-task drill record count | Drill value analysis |

**Gate:** FU ≥ 0.10 AND TRCR ≥ 0.50.

**Effort:** ~2 hours. Only for tasks that failed Phase 4.

### 10.6 Phase 6: Budget Tuning

**Goal:** Adjust L0/L1/L2/L3/GAPS budgets based on empirical data from
Phases 1–5.

**Steps:**

| Step | What |
|------|------|
| 6a | Analyse which level contributed most to correct answers (L2 SYM vs L3 FOCUS) |
| 6b | Analyse which level wasted budget on irrelevant content |
| 6c | For repos where L1 overflow occurred, measure impact on localization |
| 6d | Adjust budgets: shift tokens from underused to underserved levels |
| 6e | Re-run Phases 1 + 3 with adjusted budgets |
| 6f | Final budget freeze if metrics improve or hold |

**Gate:** No regression on any Phase 3 metric after tuning.

**Effort:** ~2 hours. Analysis + re-run.

### 10.7 Execution Order and Dependencies

```
Phase 1 (Baseline)
  │
  ├── 1a-1c: CCR for 4 repos ───────────────────────┐
  └── 1d: Django scale test ─────────────────────────┤
                                                     │
Phase 2 (Gold Tasks) ← can run in parallel with 1 ──┤
  │                                                  │
  └── 2a-2d: 20 task definitions ────────────────────┤
                                                     │
Phase 3 (Localization Scoring) ← needs 1 + 2 ───────┤
  │                                                  │
  └── 3a-3f: Score all 20 tasks ─────── GATE: loc ≥ 0.50
                                          │
                                   [IF FAIL → fix L3]
                                          │
Phase 4 (LLM Consumption) ← needs 3 pass ┤
  │                                       │
  └── 4a-4h: Arm A vs Arm B ──── GATE: DFCR ≥ 0.60
                                          │
Phase 5 (Drill-Down) ← needs 4 ──────────┤
  │                                       │
  └── 5a-5g: Drill failed tasks ── GATE: FU ≥ 0.10
                                          │
Phase 6 (Tuning) ← needs 1-5 data ───────┘
```

**Critical path:** Phase 1 → Phase 3 → Phase 4. Phase 2 runs in parallel
with Phase 1.

**Fastest to signal:** Phase 3 (localization scoring) is the cheapest test
that tells us if the format works. If Phase 3 fails, we don't need to spend
money on LLM calls in Phase 4.

### 10.8 Definition of Done

The MRLF format is validated when ALL of the following hold:

| # | Criterion | Threshold |
|---|-----------|-----------|
| D1 | CCR ≥ 0.85 for ≥ 70% of repos (Phase 1) | ≥ 3 of 4 repos |
| D2 | Django clue fits under 4150 token ceiling (Phase 1d) | ≤ 4150 tokens |
| D3 | Mean localization ≥ 0.50 across all repos (Phase 3) | ≥ 0.50 |
| D4 | Mean localization ≥ 0.80 on Flask (Phase 3) | ≥ 0.80 (no regression) |
| D5 | DFCR ≥ 0.60 (Phase 4) | ≥ 60% of 20 tasks |
| D6 | DDR ≤ 0.40 (Phase 4) | ≤ 40% of 20 tasks |
| D7 | FU ≥ 0.10 for drill tasks (Phase 5) | ≥ 0.10 mean uplift |
| D8 | No Phase 3 regression after tuning (Phase 6) | Metrics hold or improve |

**If all 8 criteria pass:** Format is validated. Proceed to paper update,
MCP integration, and broader benchmark.

**If D1-D2 fail:** Budget or format problem. Fix renderer.
**If D3-D4 fail:** Node selection problem. Fix L3 FOCUS or L2 ranking.
**If D5-D6 fail:** Content quality problem. Clue has right symbols but
wrong behavioural summaries. Fix L3 detail generation.
**If D7 fails:** Detail store content insufficient. Fix File 2 records.

### 10.9 Immediate Next Action

**Start Phase 1 + Phase 2 in parallel.**

Phase 1 script needs:
1. For each repo, sum raw source tokens (excluding tests/docs/generated).
2. Use tiktoken to count actual clue tokens (not word × 1.3 estimate).
3. Compute CCR.
4. Run Django extraction + MRLF.

Phase 2 needs:
1. Write 20 task definitions (4 repos × 5 TFs) with gold answers.
2. Each gold: question, expected files, expected symbols, 3-5 expected facts.

---

## 12. v2.0 Architecture — MCP-Served Comprehension

**Date:** April 10, 2026. Decisions from held-out validation analysis.

### 12.1 Problem Statement

MRLF v1 has a fundamental tension: a fixed-budget static file cannot serve
both small repos (Flask: 83 files, 3K tokens sufficient) and large repos
(Django: 2894 files, 4K tokens covers <2% of symbols). Held-out validation
proved this empirically: Dev DFCR=0.750 vs Held-out DFCR=0.429, with Django
0/3 as the primary failure mode and adversarial question phrasing as secondary.

### 12.2 Agreed Decisions

**D1: Adaptive Budget.** Token ceiling becomes `min(8192, max(4096, n_modules * 3))`
instead of fixed 4150. MDL is satisfied at any compression ratio >99%. The 4K
ceiling was designed for 80K context windows; frontier models now have 200K-1M.
Django at 8K gets ~70 FOCUS entries vs current 35.

**D2: MCP Sectional Loading.** File 1 splits into:
- TOC (L0 TREE + L1 INDEX, ~800 tokens) — always loaded
- FOCUS entries — served on-demand via MCP `focus_query(question)` tool
The existing MCP server (`src/codeclue_mcp/`) has `expand_projection`,
`resolve_dependency`, `fetch_contract` tools. Missing: `serve_mcp()` transport
implementation and a `focus_query` tool that runs ensemble retrieval server-side.
Key principle: the LLM sends the question, the server selects symbols. The LLM
does NOT navigate the TOC — server-side retrieval avoids poor LLM navigation.

**D3: Ensemble Retrieval (Multi-Strategy FOCUS Selection).** Replace single
keyword-match selector with 4 strategies that vote:
1. Symbol name match (current) — "session" → `SecureCookieSession`
2. Docstring/purpose match — "persist" → matches "sessions based on signed cookies"
3. Import/dependency match — "security" → modules importing `hashlib`, `itsdangerous`
4. File path match — "authentication" → `auth.py`, `sessions.py`
Symbols found by >1 strategy rank higher. Addresses adversarial phrasing fragility.

**D4: Pointer Navigation (Not Cache).** New `-- POINTERS` section in File 1:
topic labels → symbol sets. Example: `"session security" → sessions.py
[SecureCookieSessionInterface, NullSession]`. Pointers cache the RETRIEVAL PATH,
not the answer. Invalid only when referenced symbol is deleted (detectable from
commit diff). Accumulates from drill-down sessions. ~5-10 tokens per pointer.

**D5: Fat MCP Responses.** Bundle FOCUS entries + relevant File 2 records in ONE
tool call response. Target ≤2 tool calls per question. Mitigates provider
tool-call budget limits (~50 calls/conversation on most APIs).

### 12.3 Risks

1. **LLM navigation quality** — LLMs are mediocre at selecting symbols from flat
   TOC. Mitigated by D2 (server-side `focus_query`).
2. **Tool-call budget limits** — Mitigated by D5 (fat bundled responses).
3. **Format vs System validation divergence** — Phase 5 validates the static
   format; MCP validates the system. Decision: complete Phase 5 first, then
   build MCP integration with its own evaluation protocol.

### 12.4 Implementation Order

| # | What | Blocks On | Changes Format? |
|---|------|-----------|-----------------|
| 1 | Phase 5 drill-down (current format) | Nothing | No |
| 2 | Adaptive budget (D1) | Phase 5 | No (parameter) |
| 3 | Ensemble retrieval (D3) | Phase 5 data | No (selector) |
| 4 | MCP transport + `focus_query` (D2) | D3 | Yes (delivery) |
| 5 | Pointer accumulation (D4) | D2 | Yes (new section) |
| 6 | Held-out re-evaluation | All above | No |

**Decision: Path A selected.** Complete format validation (Phase 5 → adaptive
budget → ensemble retrieval → commit v0.9.0), then MCP integration as v2.0.
User approval required before starting MCP implementation (step 4+).
