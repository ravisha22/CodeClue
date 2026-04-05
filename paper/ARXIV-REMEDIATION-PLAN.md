# CodeClue ArXiv Remediation Plan

Date: 2026-04-05
Status: Planning locked; execution pending evidence updates
Primary goal: convert the current paper into a defensible arXiv preprint without overstating results

## 1. Current Publication Blockers

| Blocker | Severity | Current state | Fix type |
| --- | --- | --- | --- |
| Headline contribution is not end-to-end tested | High | The paper centers confidence-gated drill-down, but the drill-down loop is still unmeasured | Evidence plus rewrite |
| Placeholder artifact availability | High | The paper still ends with a placeholder repository URL | Manuscript-only |
| Surviving internal inconsistencies | High | Contributions still say 3 languages and still overstate cross-model confirmation | Manuscript-only |
| Efficiency result is exposed to teardown | High | 81 percent TRR is paired with a large clue-vs-raw fidelity gap and no measured recovery after drill-down | Evidence plus rewrite |
| Structural losslessness wording is too strong | Medium | Related work claims structural losslessness while limitations admit regex extractor gaps | Manuscript-only |
| References are not submission clean | Medium | At least one missing citation and one inconsistent bibliography entry remain | Manuscript-only |
| Reproducibility packaging is incomplete | Medium | No final public URL, no compact reproducibility table in the paper, no threats-to-validity style packaging | Manuscript-only |
| Drift, calibration, and scale are not paper-ready yet | Medium | Test scaffolds exist, but these results should not enter headline claims unless they are complete and passing | Evidence-gated |

## 2. Execution Principle

Use the weakest defensible claim set.

No statement should survive in the final paper unless one of the following is true:

1. It is directly supported by a saved artifact in the repository.
2. It is clearly labeled as a limitation, planned release, or future work.

## 3. Workstream A: Manuscript Baseline Cleanup

This work does not depend on the new MCP, drill-down, drift, or calibration outputs. It can be executed immediately or immediately before the final rewrite.

### A1. Internal consistency cleanup

Tasks:

1. Fix the Contributions section so it matches the 4-language claim used elsewhere.
2. Replace any remaining wording that says cross-model evaluation "confirms" all findings.
3. Remove or truthfully reword the artifact availability statement until a real public URL exists.
4. Tighten the structural losslessness wording so it does not conflict with extractor limitations.

Acceptance criteria:

1. No section contradicts another section on languages, model roles, or evidence strength.
2. No line claims public availability without a real URL.
3. No line claims full replication when the artifact only supports partial replication.

### A2. Reference and packaging cleanup

Tasks:

1. Fix missing and inconsistent bibliography entries.
2. Add a compact reproducibility subsection or appendix pointer covering repo commits, task prompts, ground truth source, and judge protocol.
3. Add a compact threats-to-validity subsection or expand the current limitations section to match that role.
4. Number or formally reference important tables so the draft reads like a paper rather than working notes.

Acceptance criteria:

1. Every citation in the prose has a matching reference entry.
2. The bibliography has no visibly inconsistent year/venue combinations.
3. A reader can locate the task source, scoring method, and artifact provenance from the paper itself.

## 4. Workstream B: Evidence Integration From Pending Implementation Work

This work depends on the other LLM finishing the implementation and evidence-generation tasks.

### B1. MCP server validation

Required inputs:

1. Passing or partially passing `tests/mcp/` results.
2. Independent assessment results driven by `experiments/cross-model-eval/INSTRUCTIONS-MCP-ASSESSMENT.md`.
3. Adversarial and cross-repo tool behavior notes.

Required outputs for paper use:

1. Tool pass/fail summary.
2. Concrete failure modes.
3. Evidence that the tools are useful for real comprehension tasks, not just callable.

### B2. End-to-end drill-down trial

Required inputs:

1. Before/after fidelity for low-confidence tasks.
2. Token cost before and after drill-down.
3. Tool-call counts and unresolved cases.
4. At least one traceable end-to-end example.

Required outputs for paper use:

1. H5 verdict: did drill-down improve fidelity enough at acceptable cost.
2. H7 verdict: did effective token reduction survive after drill-down costs.
3. One running example suitable for the paper.

### B3. Drift testing

Current scaffold: `tests/drift/test_drift.py`

Required outputs for paper use:

1. H3 verdict with the measured delta non-inferiority gap.
2. H4 verdict with the measured drift slope and floor behavior.
3. Exact statement of whether drift becomes a result or stays in limitations.

### B4. Calibration testing

Current scaffold: `tests/calibration/test_calibration.py`

Required outputs for paper use:

1. Calibration profile artifacts.
2. ECE and Brier metrics.
3. Clear pass/fail status for whether calibration is a validated method or only a motivating observation.

### B5. Scale testing

Current scaffold: `tests/scale/test_scale.py`

Current diagnosis from the Django run:

1. The serialized canonical graph is larger than the Django Python source set at current settings.
2. This is not just an extractor issue; it is amplified by pretty-printed JSON, long repeated identifiers, redundant `edge_id` storage, and duplicated `calls` / `called_by` references.
3. The current scale harness also uses an invalid raw-token estimator for paper purposes because it sums overlapping node spans rather than deduplicated source files.

Implication:

1. Do not use the current Django scale result as paper evidence for H1-style token efficiency.
2. Separate canonical storage budget from clue-context budget.
3. Measure task-conditioned projections against deduplicated raw source bytes or files, not against overlapping node spans.
4. Keep scale out of the headline claim set unless the representation or measurement path is fixed.

Rule:

1. Treat scale as optional strengthening for arXiv.
2. Do not block the paper on scale unless the title or abstract is widened to make scale a central claim.
3. If scale is kept in the paper later, the serializer and scale harness must be revised before any Django-scale number is cited.

## 5. Claim Ladder and Decision Rules

### Tier A: Full drill-down evidence available

Use this framing only if the new artifacts show a real end-to-end drill-down gain and acceptable token economics.

Allowed:

1. Keep the current title centered on confidence-gated drill-down.
2. Keep drill-down as a headline contribution.
3. Report H5 and H7 as measured results.

Not allowed:

1. Claim full model-independence unless the new cross-model evidence truly supports it.

### Tier B: MCP works, but end-to-end drill-down evidence is partial or weak

Use this framing if the server is real and useful but the measured gains are mixed or below target.

Allowed:

1. Present drill-down as a validated mechanism with preliminary or mixed empirical support.
2. Keep the tool architecture in the paper, but not as the sole headline success story.

Required rewrite:

1. The title or abstract must be softened so the paper is not read as having already proven the full drill-down thesis.

### Tier C: Drill-down evidence is still incomplete

Use this framing if the implementation exists but the end-to-end paper-grade evidence is not ready.

Allowed:

1. Reposition the paper around persistent structural comprehension artifacts and safe Tier 1 behavior.
2. Treat Tier 2 and drill-down as the next validated step, not the current proven result.

Required rewrite:

1. Retitle the paper away from a drill-down-first claim.
2. Move H5 and H7 out of the implied-results set.

## 6. Rewrite Map For The Final Pass

| Section | Planned action |
| --- | --- |
| Title | Keep only if Tier A evidence exists; otherwise narrow to persistent structural comprehension artifacts |
| Abstract | Rebuild from measured artifacts only; keep the weakest defensible wording |
| Contributions | Synchronize language count, evidence strength, and what is actually validated |
| Evaluation | Add any new MCP, drill-down, drift, or calibration protocol details that were truly run |
| Results | Replace every impacted number from source artifacts rather than editing prose by hand |
| Discussion | Separate measured claims from interpretation |
| Limitations / Threats | Explicitly cover sample size, judge calibration, extractor parity, and any failed or incomplete tracks |
| Conclusion | Do not exceed the evidence strength reached in Results |
| References | Resolve missing citations and bibliography inconsistencies |

## 7. Inputs Required Before Final Execution

When returning for implementation, bring the following:

1. The commit hash or branch containing the new MCP, drift, and calibration work.
2. Paths to any newly generated result artifacts.
3. A short note on which tests pass, fail, or remain skipped.
4. Confirmation on whether a real public repository URL can be placed in the paper.
5. Confirmation on whether the paper should target Tier A, Tier B, or Tier C framing if the evidence is mixed.

## 8. Final Execution Order

1. Inspect the new code and result artifacts.
2. Run the MCP assessment and verify the saved outputs.
3. Run drift and calibration validations and classify them as result versus limitation.
4. Choose the claim tier.
5. Rewrite the paper in one pass.
6. Regenerate the final markdown, HTML, and PDF artifacts.
7. Perform one last hostile review focused on teardown risk.

## 9. ArXiv-Ready Acceptance Criteria

The paper is ready for arXiv only when all of the following are true:

1. No placeholders remain.
2. Every numeric claim in the paper traces to a concrete artifact.
3. The headline contribution is either empirically supported or explicitly narrowed.
4. The references are complete and internally consistent.
5. Reproducibility and artifact availability language are truthful.
6. The conclusion does not outrun the results.
7. A final hostile review finds no remaining high-severity credibility issues.
