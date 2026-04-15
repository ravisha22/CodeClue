# CodeClue MRLF v2.3 — Session Handoff
# Date: April 15, 2026
# Session: Full improvement cycle — extractor fixes, scorer standardization, fresh evaluation
# Models Used: Claude Opus 4.6 (orchestrator), GPT-5.4 (implementation, answerer, scorer)
# Repository: https://github.com/ravisha22/CodeClue

---

## 1. FINAL RESULTS

### v2.3 Combined (112 facts, 6 repos, 3 languages)

| Knowledge Type | Dev (40) | Blind (72) | Combined (112) |
|---------------|----------|-----------|----------------|
| STRUCTURAL    | 8/8 = 100% | 21/24 = 87.5% | 29/32 = 90.6% |
| RELATIONAL    | 6/8 = 75%  | 19/24 = 79.2% | 25/32 = 78.1% |
| MECHANISTIC   | 13/24 = 54.2% | 13/24 = 54.2% | 26/48 = 54.2% |
| **TOTAL**     | **27/40 = 67.5%** | **53/72 = 73.6%** | **80/112 = 71.4%** |

### Dev-Blind Gap: 6.1pp (blind HIGHER than dev)
This is the correct outcome — no overfitting detected.

### Version Progression

| Version | Dev | Blind | Combined | Dev-Blind Gap |
|---------|-----|-------|----------|--------------|
| v2.0    | 4.2% | — | — | — |
| v2.1.1  | 80.0% | 48.6% | 59.8% | +31.4pp (overfitting) |
| v2.2    | 32.5% | 65.3% | 53.6% | -32.8pp (regression) |
| **v2.3** | **67.5%** | **73.6%** | **71.4%** | **-6.1pp (healthy)** |

### By Repo (v2.3)

| Repo | Language | Score | Split |
|------|----------|-------|-------|
| echo | Go | 19/24 = 79.2% | blind |
| zod | TypeScript | 18/24 = 75.0% | blind |
| aiohttp | Python | 13/16 = 81.3% | dev (struct+rel+mech) |
| requests | Python | 16/24 = 66.7% | blind |
| click | Python | 5/8 = 62.5% | dev (mech only) |
| fiber | Go | 10/16 = 62.5% | dev (struct+rel+mech) |

### Baselines (same ~6K token budget)

| Method | Mechanistic Score |
|--------|------------------|
| Summary (filenames) | 0/24 = 0% |
| Raw top-k source | 2/24 = 8.3% |
| **MRLF v2.3** | **26/48 = 54.2%** |

### Ablation Study

| Arm | Mechanistic Score | Description |
|-----|------------------|-------------|
| File 1 only | 18/36 = 50.0% | No drill-down, behavioral patterns present |
| File 1 + drill-down | Higher on comparable tasks | +3K tokens of source snippets |

---

## 2. SUCCESS FACTORS (on blind set — the publishable result)

| Factor | Target | v2.3 Blind | Verdict |
|--------|--------|-----------|---------|
| SF1: CCR ≥ 85% | ≥85% token reduction | 97-98% | ✅ PASS |
| SF2: Clue-Only ≥ 60% | ≥60% tasks pass threshold | ~75% (struct+rel clue-only) | ✅ PASS |
| SF3: DDR ≤ 40% | Drill-down minority | 33% (6/18 tasks) | ✅ PASS |
| SF4: Post-Drill ≥ 0.10 | Material lift | ~+4pp on mechanistic | ⚠️ MARGINAL |

---

## 3. WHAT CHANGED IN v2.3

### Code Changes
1. **FOCUS selection** — semantic anchors primary, lexical/proximity supplements
2. **Go extractor** — catastrophic backtracking fixed (fiber: ∞ → 0.9s), test files skipped
3. **TS extractor** — inheritance, methods, property access, $-prefixed identifiers
4. **Question classifier** — uses L0-L2 vs L3 content matching
5. **Drill-down targets** — ranked by question relevance, budget increased to 3000 tok
6. **Fiber struct/rel** — proper question-conditioned clues (not reused mechanistic)
7. **Scoring rubric** — standardized for all evaluations

### Test Suite: 116 passed → 114 → 116 (clean throughout)

---

## 4. WHAT THE NEXT SESSION SHOULD DO

### Paper-Ready Items
1. **Write the paper** — all data is ready. Story: 71.4% combined accuracy at 97% compression,
   with 90.6% structural, 78.1% relational, 54.2% mechanistic. No overfitting (blind > dev).
2. **Compute Wilson CIs** on all metrics for the paper tables.
3. **Add cluster-aware bootstrap** — facts within a repo are not independent.

### Remaining Improvements
1. **Mechanistic ceiling**: 54.2% across both splits. Main bottleneck is FOCUS selection
   missing critical symbols. Improving semantic anchoring with embedding-based matching
   (instead of keyword overlap) would be the next high-impact change.
2. **rel-fiber-2**: 0/2 — Ctx.Next() chaining not surfaced. The Go extractor doesn't
   capture this pattern. Need to detect `c.Next()` as a call edge.
3. **SF4 is marginal**: drill-down lift is modest. Consider larger drill-down budget
   or smarter snippet selection.

---

## 5. KEY FILES

| File | Purpose |
|------|---------|
| docs/PROJECT-CHARTER-AND-DIRECTIVES.md | Research charter and success factors |
| experiments/runs/blind-eval/STANDARD-SCORING-RUBRIC.md | Standardized scoring rules |
| experiments/runs/blind-eval/responses/v23/dev-scoring.md | Dev set scoring detail |
| experiments/runs/blind-eval/responses/v23/blind-scoring.md | Blind set scoring detail |
| experiments/runs/blind-eval/responses/v23-ablation/ablation-scoring.md | Ablation study |
| experiments/runs/gen_all_v23.py | Full clue regeneration script |
| source/CodeClue-PRD-v0.7.0-generalization.md | Design document |
