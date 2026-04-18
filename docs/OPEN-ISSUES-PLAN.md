# CodeClue Open Issues Plan

## Context Map

### Files to Modify
| File | Purpose | Changes Needed |
|------|---------|----------------|
| docs/OPEN-ISSUES-PLAN.md | Canonical prioritized backlog for v2.4 paper-readiness and research execution | New issue inventory, priority labels, sequencing, effort, dependencies |

### Dependencies (informational)
| File | Relationship |
|------|--------------|
| docs/PROJECT-CHARTER-AND-DIRECTIVES.md | Defines success factors, paper targets, and v2.4 blind metrics |
| source/CodeClue-PRD-generalization.md | Holds current design intent and latest generalized-comprehension framing |
| docs/REASONING-SCAFFOLD.md | Defines scaffold text and current unvalidated status |
| docs/FINAL-PROJECT-SUMMARY.md | Captures consolidated status, evidence, and paper-readiness context |
| experiments/runs/blind-eval/responses/v24/blind-scoring.md | Source of v2.4 blind scores and task-level misses |
| paper/codeclue-paper-v25.md | Current paper draft that should stay aligned with backlog priorities |

### Test Files
| Test | Coverage |
|------|----------|
| N/A (doc-only task) | No code changes; verification is file-content review only |

### Reference Patterns
| File | Pattern |
|------|---------|
| docs/FINAL-PROJECT-SUMMARY.md | Consolidated status narrative and evidence framing |
| paper/codeclue-paper-v25.md | Current manuscript structure and claim packaging |

### Risk Assessment
- [ ] Breaking changes to public API
- [ ] Database migrations needed
- [ ] Configuration changes required

## Scope and Prioritization Rule

This plan uses the following rule:
- **P0** = blocks a defensible paper submission or prevents producing the submission artifact.
- **P1** = should be fixed before paper submission to reduce reviewer risk or tighten the main claim set.
- **P2** = important, but can remain in limitations/future work without blocking submission.
- **P3** = cleanup or future-work items that should not slow paper-critical execution.

Current state assumed for planning: **v2.4 blind = structural 87.5%, relational 91.7%, mechanistic 66.7%; 123 passing tests; Python/Go/TypeScript supported; scaffold added but not yet re-measured.**

## Critical Path Summary

1. Fix evaluation credibility blockers (**#7, #9**).
2. Re-run scaffold and statistical packaging needed for paper tables (**#20, #8, #6**).
3. Close the highest-leverage correctness gaps that directly affect blind misses (**#1, #2, #3**).
4. Write and freeze the paper once evidence is stable (**#11**).
5. Tidy supporting docs so future sessions do not drift (**#12, #15**).

## P0 — Blocks Paper Submission

| Issue | Description | Impact | Suggested Fix | Effort (hours) | Dependencies |
|------|-------------|--------|---------------|----------------|--------------|
| #7 | **No inter-rater agreement measured.** Gold facts were created by GPT-5.4 and scored by GPT-5.4. | Biggest credibility risk in the current evaluation stack; weakens any claim that scores are objective or reproducible. | Add a second independent judge model plus a human spot-check set; compute agreement (Cohen/Fleiss where applicable or percent agreement + adjudication log) on a representative task sample before freezing paper numbers. | 8 | None |
| #9 | **Need more repos for publishable sample size.** Current evidence is 6 repos; target is 10+. | Fails the project's own minimum-publishable bar and leaves repo-level variance too high for a strong submission. | Expand to at least 10 repos with balanced Python/Go/TypeScript coverage, add 6 fact-backed tasks per repo, and rerun the full blind protocol with the same rubric. | 24 | #6, #7 |
| #11 | **Paper not written yet.** | No submission artifact exists; all other work has nowhere to land until a manuscript is drafted. | Create paper outline immediately, but freeze results/tables only after #7, #8, #9, and #20; then draft full manuscript, figures, threats-to-validity, and reproducibility appendix. | 18 | #7, #8, #9, #20, #12 |

## P1 — Should Fix Before Paper

| Issue | Description | Impact | Suggested Fix | Effort (hours) | Dependencies |
|------|-------------|--------|---------------|----------------|--------------|
| #1 | **Go extractor misses `c.Next()` as a call edge** (`rel-fiber-2` scores 0/2). | Leaves a known relational blind spot in one of the three supported languages and creates an avoidable negative example in paper artifacts. | Extend Go call-edge detection to capture method calls on short receiver variables (`c.Next()` style), add a regression fixture, and regenerate the affected Fiber clues/eval traces. | 4 | None |
| #2 | **TS extractor misses some Zod v4 internal patterns** (`$ZodType`, `_zod.def`). | Undercuts the TypeScript-language parity story and leaves a known blind miss in the strongest TS benchmark repo. | Patch TypeScript extraction/rendering for `$`-prefixed symbols and nested internal-property surfacing, then add Zod-specific regression fixtures that stay pattern-based rather than repo-hardcoded. | 6 | None |
| #3 | **FOCUS selection is unstable across dev vs blind.** Expansion helps blind but not dev consistently. | Makes it hard to explain selector behavior and raises the risk that gains are benchmark-composition artifacts rather than genuine generalization. | Instrument selector diagnostics per repo/task, compare gold-symbol recall by split, and tune ranking/expansion rules only if the change improves both dev and blind under the overfitting monitor. | 8 | #6 |
| #6 | **Dev gold facts are harder than blind gold facts.** | Dev-vs-blind comparisons become misleading; split-level conclusions may reflect gold difficulty rather than model/clue quality. | Recalibrate the gold set: tag each fact by difficulty and evidence depth, normalize task composition across splits, and stop pooling dev+blind until difficulty is matched. | 6 | None |
| #8 | **Wilson CIs exist, but cluster-aware bootstrap is missing.** | Repo-level correlation is currently under-modeled, so uncertainty bands may look tighter than they really are. | Add repo-cluster bootstrap intervals for all headline metrics and report both Wilson and cluster-aware intervals in the paper tables/appendix. | 6 | #9 |
| #20 | **Reasoning scaffold added but not tested.** | The project cannot honestly claim scaffold value, cross-model stabilization, or prompt-overhead payoff without fresh evidence. | Re-run the 6-model comparison with the scaffold enabled, compare against the prior baseline, and decide whether scaffold results are headline evidence or appendix-only. | 8 | #7 |

## P2 — Important but Not Blocking

| Issue | Description | Impact | Suggested Fix | Effort (hours) | Dependencies |
|------|-------------|--------|---------------|----------------|--------------|
| #4 | **`struct-fiber-2` still scores 0/2** (`ctx.go`/`router.go` not always surfacing). | Leaves a known structural miss, but current structural blind score already clears threshold. | Add task-level selector diagnostics for Fiber structural questions and bias file/module surfacing toward route/context anchor files when question terms imply architecture layout. | 4 | #3 |
| #5 | **Behavioral patterns remain too shallow** (e.g., `ACCUMULATE(loop→exits)` misses generator vs context-manager distinctions). | Caps mechanistic accuracy and makes some answers too generic for publication-quality exemplars. | Add richer pattern details for generator lifecycle, context-manager enter/exit, precedence chains, and guard condition summaries; validate on existing mechanistic misses before broader rollout. | 10 | #1, #2, #3 |
| #10 | **No human evaluation.** | Limits claims about practical usefulness and answer quality outside the gold-fact rubric. | Run a small human study or expert audit on a stratified sample of tasks: usefulness, faithfulness, and drill-down utility; include as supporting evidence or appendix. | 12 | #7, #9 |
| #12 | **PRD v0.7.0 has outdated results** (still references v2.1 numbers). | Increases documentation drift and risks stale numbers leaking into the paper or README. | Update the PRD summary tables and result references to v2.4, while clearly marking which numbers are final and which remain provisional pending expanded eval. | 3 | #8, #20 |
| #15 | **Multiple handoff docs overlap or contradict each other.** | Future sessions may execute against stale assumptions or cite the wrong metrics. | Create one canonical handoff/status doc, archive old handoffs as historical-only, and add a short “authoritative documents” index. | 4 | #12 |
| #16 | **MCP server exists but is not integrated with the v2.4 MRLF renderer.** | Prevents clean end-to-end demonstrations of clue → gap → tool → answer, but a paper can still scope this as future work. | Connect renderer GAPS output to MCP tool targets, prove one traceable end-to-end path, and save artifacts for a possible demo/appendix section. | 10 | #17 |
| #17 | **Confidence-gated tool calling is designed but not implemented.** | Leaves a central architecture idea unvalidated, reducing the strength of any drill-down-first framing. | Implement minimal confidence thresholds + tool budget enforcement, log tool calls, and run one controlled drill-down evaluation to decide whether this stays future work or becomes a measured result. | 14 | #16 |
| #18 | **No delta update testing with the v2.4 format.** | Weakens update-robustness claims, but does not block a paper focused on comprehension fidelity. | Extend the existing delta-update test harness to v2.4 MRLF outputs and record pass/fail artifacts against a few controlled repo mutations. | 6 | #12 |
| #19 | **No CI/CD pipeline for automated eval on code changes.** | Slows iteration and increases regression risk, but does not block publication if manual runs remain reproducible. | Add GitHub Actions for tests plus a lightweight eval-smoke workflow; reserve full benchmark runs for manual or scheduled execution to control cost. | 8 | #1, #2, #3, #18 |

## P3 — Nice to Have / Future Work

| Issue | Description | Impact | Suggested Fix | Effort (hours) | Dependencies |
|------|-------------|--------|---------------|----------------|--------------|
| #13 | **`NEXT-STEPS.md` is stale** (still references obsolete sprints 6-12). | Creates confusion for operators, but does not affect paper validity if ignored. | Replace with a short living roadmap that points readers to this issue plan and the canonical handoff doc. | 1.5 | #15 |
| #14 | **`recall.md` is 57 KB and needs cleanup.** | Lowers navigability and session continuity, but has no direct effect on paper claims. | Split archival material from active notes, keep a one-page summary at the top, and move bulky historical detail to archived sections. | 2 | #15 |

## Recommended Execution Order

1. **Evaluation credibility first:** #7 → #6 → #9 → #8 → #20
2. **Highest-leverage code fixes:** #1 → #2 → #3
3. **Targeted quality lifts:** #4 → #5 → #10
4. **Paper and canonical docs:** #12 → #15 → #11
5. **Architecture validation (only if time remains before submission):** #16 → #17 → #18 → #19
6. **Backlog cleanup:** #13 → #14

## Minimum Pre-Submission Checklist

Before declaring the project paper-ready, all of the following should be true:
- Independent scoring reliability has been measured (**#7**).
- Repo count reaches the planned publishable floor (**#9**).
- Uncertainty reporting uses repo-aware statistics (**#8**).
- Scaffold claims are either validated or removed from the headline narrative (**#20**).
- Known cross-language misses with obvious fixes have been addressed or explicitly limited (**#1, #2**).
- The paper draft and supporting docs reference one consistent result set (**#11, #12, #15**).
