# Review of CodeClue arXiv Draft

## Part 1: Factual Corrections

FACTUAL ERROR at Abstract, paragraph 2:
  Paper says: "Cross-model evaluation using GPT 5.4 as consumer and Gemini 3.1 Pro as independent judge confirms these findings are not artifacts of self-evaluation, with a mean fidelity delta of 0.12 between models."
  Data shows: `experiments/cross-model-eval/results/gemini-judge-SUMMARY.json` reports `arm_b_mean_absolute_delta = 0.12`, but `arm_a_mean_absolute_delta = 0.35`. The unqualified phrase "mean fidelity delta" is only true for Arm B.
  File: `experiments/cross-model-eval/results/gemini-judge-SUMMARY.json`
  Fix: "..., with a mean Arm B fidelity delta of 0.12 between GPT 5.4 and Claude; Arm A deltas remain much larger (0.35)."

FACTUAL ERROR at Abstract, paragraph 1; Section 3.1, repository table; Section 4.3; Section 8:
  Paper says: "23 comprehension tasks across 7 public repositories ... spanning Python, TypeScript, and Go" and `| expressjs/express | TypeScript | 355 | 864 |`.
  Data shows: the Express repo in the workspace is JavaScript, not TypeScript. `package.json` lists `index.js` and `lib/`; `index.js` and `lib/application.js` are JavaScript files; the extracted graph begins with `.js` paths such as `examples/auth/index.js`.
  File: `experiments/external-repos/express/package.json`
  File: `experiments/external-repos/express/index.js`
  File: `experiments/external-repos/express/lib/application.js`
  File: `experiments/runs/v2-lane-a-express/graph.json`
  Fix: relabel Express as JavaScript and either update the language count to four languages (Python, JavaScript, TypeScript, Go) or explicitly say that JavaScript was processed by the TypeScript/regex extractor.

FACTUAL ERROR at Abstract, paragraph 1; Section 4.3:
  Paper says: "zero hallucination rate across all tasks and all three model families tested (Claude, GPT, Gemini)"
  Data shows: `experiments/reports/v2-benchmark-all-23.json` reports `hallucination_rate = 0.00` for the Claude consumer run, and `experiments/cross-model-eval/results/gemini-judge-SUMMARY.json` reports `hallucination_count = 0` for GPT 5.4. Gemini appears only as the judge model in that file; no hallucination metric is reported for Gemini as a task-answering model.
  File: `experiments/reports/v2-benchmark-all-23.json`
  File: `experiments/cross-model-eval/results/gemini-judge-SUMMARY.json`
  Fix: "zero hallucinations for the two consumer models evaluated (Claude and GPT 5.4); Gemini served as the judge."

FACTUAL ERROR at Section 4.4, `clue_only` row:
  Paper says: `| clue_only | 13/23 | 0.62 | Higher fidelity group |`
  Data shows: recomputing from the 23 task rows in `experiments/reports/v2-benchmark-all-23.json` gives 15/23 tasks with `v2_hint = clue_only` and mean Arm B fidelity 0.613. The required projection file `experiments/reports/v2-existing-projections.json` also does not support 13/23; it contains only 15 tasks total, of which 11 are `clue_only`.
  File: `experiments/reports/v2-benchmark-all-23.json`
  File: `experiments/reports/v2-existing-projections.json`
  Fix: update the row to `15/23` and `0.61`, or explain why a different subset is being used.

FACTUAL ERROR at Section 4.4, `targeted_lookup` row:
  Paper says: `| targeted_lookup | 4/23 | 0.53 | Intermediate |`
  Data shows: recomputing from the 23 task rows in `experiments/reports/v2-benchmark-all-23.json` gives 4/23 tasks with `v2_hint = targeted_lookup` and mean Arm B fidelity 0.5125.
  File: `experiments/reports/v2-benchmark-all-23.json`
  Fix: update the mean Arm B fidelity to `0.51` if the 23-task aggregate is the intended source.

FACTUAL ERROR at Section 4.4, `expanded_lookup` row:
  Paper says: `| expanded_lookup | 6/23 | 0.29 | Correct: lowest fidelity, most need for drill-down |`
  Data shows: recomputing from the 23 task rows in `experiments/reports/v2-benchmark-all-23.json` gives 4/23 tasks with `v2_hint = expanded_lookup` and mean Arm B fidelity 0.2625. The combined projection artifacts show 11 `clue_only`, 2 `targeted_lookup`, 2 `expanded_lookup` in `experiments/reports/v2-existing-projections.json` and 4 `clue_only`, 2 `targeted_lookup`, 2 `expanded_lookup` in `experiments/reports/v2-newrepo-projections.json`, which again totals 15/4/4 rather than 13/4/6.
  File: `experiments/reports/v2-benchmark-all-23.json`
  File: `experiments/reports/v2-existing-projections.json`
  File: `experiments/reports/v2-newrepo-projections.json`
  Fix: update the row to `4/23` and `0.26`, or document a different classification rule and the source artifact that produced it.

## Part 2: Logical Issues

LOGIC ISSUE at Abstract; Section 4.6; Section 8:
  Claim: Cross-model evaluation confirms the findings are not artifacts of self-evaluation.
  Problem: The replication file is mixed. `arm_b_mean_absolute_delta <= 0.15` passes, but `arm_b_spearman_correlation` is only 0.36, `arm_a_mean_absolute_delta` is 0.35, and `tf3_clue_sufficient_both_models` is `false`. That supports partial replication, not blanket confirmation.
  Suggestion: narrow the claim to the specific replicated findings: zero hallucinations across the two consumer models and near-identical TF4/TF5 Arm B means.

LOGIC ISSUE at Section 4.5:
  Claim: The negative Spearman correlation confirms that low confidence correctly predicts where models need more information.
  Problem: `experiments/reports/v2-lane-b-all-repos.json` marks `gate_g7.passed = false` because `callback_distribution_passed = false`. The data supports directional correlation on one proxy metric, but not full ecological validity or a general claim about information need.
  Suggestion: present this as partial support for the scent proxy while stating clearly that Lane B still requires remediation.

LOGIC ISSUE at Section 5 and Section 8:
  Claim: Zero hallucination at Tier 1 establishes that structural clue artifacts can be trusted without per-use verification.
  Problem: The evaluation is small (23 tasks), partly self-evaluated, and excludes the end-to-end clue -> tool -> enriched answer loop, drift testing, and adversarial robustness. That is evidence of conservative behavior under the current benchmark, not a proof of general trustworthiness.
  Suggestion: replace "establishes" with "suggests under the current benchmark" and keep verification requirements explicit for production use.

LOGIC ISSUE at Section 4.7:
  Claim: Tier 2 enrichment causes confidence to decrease, which is the correct behavior.
  Problem: The observed mean confidence delta of approximately -0.13 is measured on a 7-task Flask sample only. That is plausible evidence, but the paper generalizes from a narrow sample to a system-level interpretation.
  Suggestion: call this a preliminary Tier 2 signal from the Flask sample, not a generalized result.

## Part 3: Missing Context or Overclaiming

OVERCLAIM at Abstract, paragraph 2:
  Text: "We release the full scaffold, benchmark tasks, and evaluation protocol as open source."
  Issue: The paper still ends with `[repository URL]`, and the PRD metadata marks the project as `Internal / Open Source Candidate`. The release claim is not verifiable from the draft.
  Suggested rewrite: "We plan to release the scaffold, benchmark tasks, and evaluation protocol; the public repository URL will be added in the camera-ready version." Or add the actual public URL now.

OVERCLAIM at Section 4.3:
  Text: "This is the most robust safety finding in the evaluation."
  Issue: The hallucination result is promising, but it rests on 23 tasks and does not cover end-to-end drill-down execution, drift, or adversarial cases.
  Suggested rewrite: "This is the clearest safety signal in the current benchmark, but it still requires broader validation."

OVERCLAIM at Section 4.7:
  Text: "Claude Opus 4.6 generated Tier 2 semantic contracts for 154 functions across 8 Flask modules with a 100% schema validation pass rate."
  Issue: The supporting H6 appendix explicitly calls this a preliminary 8-file sample and says full H6 testing across benchmark repositories is still required. The draft currently reads more like a benchmark-level validation than a sample result.
  Suggested rewrite: "In a preliminary 8-file Flask sample, Claude Opus 4.6 generated Tier 2 contracts for 154 functions/methods with 100% schema validation."

OVERCLAIM at Section 8:
  Text: "Cross-model evaluation with three frontier LLMs confirms these findings are not artifacts of self-evaluation."
  Issue: The replication artifact contains significant disagreement on Arm A and task ordering, and TF3 clue sufficiency does not replicate.
  Suggested rewrite: "Cross-model evaluation provides partial external validation for the zero-hallucination result and for low TF4/TF5 deltas, but it does not fully replicate all findings."

## Part 4: Structural and Writing Issues

- Table 4.4 needs explicit provenance. Right now its counts cannot be reproduced from the named projection file and do not match the task rows in the 23-task benchmark file.
- The paper uses OF1-OF5 for operation families and TF1-TF5 for task families. The mapping is inferable but not explicit enough in the results section, which makes the tables harder to follow.
- Results are discussed against H1 and H2 implicitly, but H5-H7 are not mapped back cleanly in the paper even though the PRD makes them central. A short "Hypothesis status" subsection would help.
- Reproducibility remains incomplete because the draft lacks a real repository URL, a benchmark commit table in the paper itself, and a direct pointer to the task prompts and ground truths used for scoring.
- Tables are not numbered and are rarely referenced in prose as formal tables. That makes the draft feel closer to working notes than a submission-ready paper.
- The limitations section is reasonably candid, but it should be separated from a formal threats-to-validity section to match the rigor promised by the PRD.

## Part 5: Overall Assessment

```json
{
  "scores": {
    "technical_accuracy": 2,
    "logical_coherence": 2,
    "honest_reporting": 3,
    "clarity": 4,
    "novelty": 4,
    "reproducibility": 2
  },
  "recommendation": "major_revisions",
  "summary": "The draft has a clear research idea and a credible experimental scaffold, but several central presentation claims do not currently line up with the supplied artifacts. The most serious issues are a wrong language/accounting story for Express, a non-reproducible Table 4.4, and cross-model claims that are stronger than the replication file supports.",
  "top_3_strengths": [
    "Strong problem framing around persistent code-comprehension artifacts.",
    "Clear separation between Tier 1 structural safety claims and Tier 2 semantic enrichment goals.",
    "The workspace contains unusually explicit benchmark artifacts and falsifiable hypothesis definitions."
  ],
  "top_3_weaknesses": [
    "Table 4.4 does not reproduce from the supplied task and projection artifacts.",
    "Cross-model and zero-hallucination claims are overstated relative to the evidence.",
    "Public reproducibility is incomplete because the paper still lacks a real repository URL and clearer source provenance."
  ]
}
```
