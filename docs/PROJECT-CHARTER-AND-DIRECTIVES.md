# CodeClue Research — Project Charter, Directives & Success Factors

> **Purpose:** Durable reference document memorializing the researcher's charter,
> objectives, methodology directives, and success factors. All collaborating LLMs
> must read and adhere to this document throughout the project lifecycle.
>
> **Author:** Ravi Nandagopalan (researcher/principal investigator)
> **Created:** 2026-04-15 (memorialized from directives given 2026-04-14 and prior)
> **Repository:** https://github.com/ravisha22/CodeClue

---

## 1. Thesis

Code comprehension should be a persistent, verifiable artifact that preserves
operational meaning across tasks, prompts, and incremental code evolution.

CodeClue proposes the MRLF (Multi-Resolution Lattice Format) — a two-file clue
system that compresses codebase understanding into a ≤4K token primary file with
a JSONL detail store for drill-down — as the concrete realization of this thesis.

---

## 2. Project Nature

This is a **research design project**, NOT a product. The objective is to produce
a mathematically-grounded, commercially viable format. Every design decision,
implementation choice, and evaluation must be approached with the rigor of
research methodology, not feature-shipping urgency.

---

## 3. Core Objective

Prove that a compressed, deterministic clue artifact can deliver:
- **Instant structural understanding** from ≤4K tokens (File 1)
- **Guided deep-dive capability** for mechanistic questions (File 1 → File 2)
- **Zero hallucination** on all deterministic Layer 1 content (AST extraction)
- **Explicit sufficiency boundary** — the format self-reports what it can and
  cannot answer, with costed drill-down targets

The value proposition: **"answer 70%+ from 4K tokens, and know exactly where
to look for the other 30%."**

---

## 4. Researcher's Directives (Non-Negotiable)

### 4.1 No Overfitting
- Everything must pass the "unseen repo" test
- NO repo-specific heuristics (the `_src_priority()` / `_tokenize_symbol()` trap)
- NO celebrating Dev accuracy without Validation confirmation
- NO magic numbers without information-theoretic justification
- NO testing on training data (examined repo ≠ blind repo)
- NO claiming File 1 sufficiency for mechanistic questions
- If Dev − Validation gap > 10 percentage points → **revert immediately**

### 4.2 Flexible, Not Rigid
- Adaptable token budgets — not arbitrary fixed caps
- Separate methodology for different programming languages where warranted
- "Precise flexibility with constraints, not mindless rule following"
- Consider practical applicability in every design and implementation decision
- Adaptability with constraints, not brittle one-size-fits-all rules

### 4.3 Research Design Mindset
- Must meet success factors for **commercial viability**, not just pass tests
- Principled, theory-grounded decisions
- Every metric with confidence intervals
- Validate on held-out, publish on blind
- Minimum publishable: 60 facts across ≥3 languages

### 4.4 Documentation & Continuity
- Document design, approach, and implementation in versioned PRD
- Log everything as you go
- Push to remote GitHub repo at each stage
- Be prepared for abrupt compactions — state must be recoverable
- Maintain handoff documents for session continuity

### 4.5 Collaborative Dual-Model Protocol
- **GPT-5.4:** Implementation + answerer (generates responses to blind eval prompts)
- **Claude Opus 4.6:** Orchestrator + scorer (designs changes, scores responses
  against gold facts, manages project flow)
- Both models collaborate on analysis and planning
- Neither model operates in isolation on critical decisions
- Cross-validate findings between models to prevent blind spots

---

## 5. Success Factors

The project succeeds only if **all four** target outcomes are measured directly
and reported separately.

### SF1: Compression (CCR ≥ 0.85)
- At least 85% token reduction for 70-80% of tasks
- Must hold across both small-node and large-node tasks
- Scale invariance: small repos AND large repos get the same treatment

### SF2: Clue-Only Sufficiency (DFCR ≥ 0.60-0.70)
- At least 60-70% of tasks should reach accepted fidelity threshold
  without drill-down
- Drill-down should be the minority path, not the default

### SF3: Drill-Down Dependence (DDR ≤ 0.40)
- The majority of tasks should complete in clue-only mode
- Drill-down is for the hard tail, not the common case

### SF4: Post-Drill Value (FU ≥ 0.10)
- For tasks requiring drill-down, post-drill fidelity should improve
  materially
- Total clue-plus-drill context must remain well below raw-first cost

### Minimum Viable Accuracy Targets

| Knowledge Type | File 1 Only | With File 2 | v2.4 Blind |
|---------------|-------------|-------------|------------|
| Structural    | ≥85%        | ≥95%        | 87.5% ✅   |
| Relational    | ≥70%        | ≥90%        | 91.7% ✅   |
| Mechanistic   | ≥30%        | ≥70%        | 66.7% ⚠️   |

### Multi-Repo Validity
- Not just Flask — must generalize across repos, languages, and conventions
- Minimum 3 languages (Python, Go, TypeScript)
- Minimum 3+ blind repos for publishable results

---

## 6. Non-Negotiable Properties (from Research Charter)

1. Lossless source anchoring for every semantic unit
2. Task-dependent comprehension views derivable without hallucinated links
3. Deterministic validation of clue-to-source consistency
4. Explicit uncertainty and contradiction channels

---

## 7. Architecture

CodeClue uses a **three-layer architecture** rendered as a **two-file format**.

- **Layer 1 — Deterministic AST Extraction:** Produces the primary
  **File 1** artifact (`.codeclue`, ≤4K tokens) with TREE, INDEX, SYM, FOCUS,
  and GAPS. This layer provides structural + relational comprehension plus
  behavioral annotations and explicit sufficiency boundaries.
- **Layer 2 — LLM Domain Summary:** Adds semantic and architectural context
  that AST extraction misses by reading key files such as README, settings,
  models, schema, and routes. This layer is essential for enterprise apps and
  optional for smaller libraries.
- **Layer 3 — Guided Drill-Down:** Uses GAPS-guided retrieval to fetch targeted
  **File 2** records (`.codeclue-detail.jsonl`) for mechanistic questions that
  need source-level detail.

The file format remains intentionally **two-file**: File 1 is the portable clue,
and File 2 is the detail store for selective deep-dive. The protocol is to read
File 1 first, consult GAPS, and retrieve only the specific File 2 records needed
for the question at hand. This is the "double-click" pattern.

---

## 8. Anti-Patterns Register

Patterns that led to wasted effort in prior sessions — avoid at all costs:

1. Repo-specific heuristics (`_src_priority`, `_tokenize_symbol` tuning)
2. Celebrating Dev accuracy without Validation confirmation
3. Magic numbers without information-theoretic justification
4. Testing on training data (examined repo ≠ blind repo)
5. Lexical tricks (stemming, substring matching) as proxies for relevance
6. Claiming File 1 sufficiency for mechanistic questions
7. Overfitting the selector, test cases, or evaluation to specific repos

---

## 9. Open Source Project

CodeClue is an **open source project**. All code, extractors, format specifications,
evaluation data, and tooling are publicly available. There are no commercial tiers,
paid features, or proprietary components.

The generation pipeline (deterministic AST extraction + optional LLM-enhanced
behavioral summaries) is fully open. Users can run it with any model of their
choice, including local/self-hosted models for privacy-sensitive codebases.

Repository: https://github.com/ravisha22/CodeClue

---

## 10. Publication Target

- **Venue:** ICSE NIER or ASE Tool Track
- **Story:** 81% TRR + zero hallucination + behavioral annotations from File 1
  + guided drill-down for mechanistic questions
- **Minimum evidence:** 60 facts, ≥3 languages, ≥3 blind repos, all metrics
  with Wilson 95% confidence intervals
- **Design discipline:** Validate on held-out, publish on blind

---

*This document is the authoritative reference for all project directives.
Any collaborating LLM session must read this before making design or
implementation decisions.*
