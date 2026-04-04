# Instructions for GPT 5.4 — Paper Reviewer
# Role: CRITICAL ACADEMIC REVIEWER
# You are reviewing an arXiv paper draft for technical accuracy, logical coherence,
# and honest presentation of results.

## Your Task

Read the paper draft at `paper/codeclue-arxiv-draft.md` and produce a thorough
peer review. You have full access to the workspace to verify every claim against
the actual data.

## Review Criteria

Score each criterion on a 1-5 scale (1=poor, 5=excellent):

1. **Technical Accuracy**: Do the numbers in the paper match the actual data files?
2. **Logical Coherence**: Do the conclusions follow from the evidence?
3. **Honest Reporting**: Are limitations adequately disclosed? Any spin or overclaiming?
4. **Clarity**: Can a reader understand the system and results?
5. **Novelty**: Is the contribution clearly differentiated from prior work?
6. **Reproducibility**: Could someone replicate the results from what's described?

## Verification Steps (DO THESE)

Check every number in the paper against source data:

1. Read `experiments/reports/v2-benchmark-all-23.json` — verify the per-family fidelity scores,
   TRR, and task counts match what the paper claims.

2. Read `experiments/cross-model-eval/results/gemini-judge-SUMMARY.json` — verify cross-model
   evaluation numbers (delta 0.12, Spearman 0.36, hallucination count).

3. Read `experiments/reports/v2-lane-b-all-repos.json` — verify IFT alignment (0.65),
   Spearman (−0.30), KL divergence (0.29).

4. Read `experiments/reports/tier2-flask-comparison.json` — verify Tier 2 enrichment
   numbers (154 functions, confidence deltas).

5. Read `experiments/reports/v2-existing-projections.json` — verify confidence scores
   and hint distributions match the paper's Table 4.4.

6. Read `source/CodeClue-PRD-v0.3.0-mvp-FINAL.md` Section 4.2 — verify that hypotheses
   in the paper match the PRD's definitions.

## What To Produce

### Part 1: Factual Corrections

For every number that doesn't match the data, produce:
```
FACTUAL ERROR at Section X.Y, paragraph Z:
  Paper says: [exact text]
  Data shows: [actual value from file]
  File: [path to source file]
  Fix: [corrected text]
```

### Part 2: Logical Issues

For any conclusion that doesn't follow from the evidence:
```
LOGIC ISSUE at Section X.Y:
  Claim: [what the paper says]
  Problem: [why it doesn't follow]
  Suggestion: [how to fix]
```

### Part 3: Missing Context or Overclaiming

For any claim that overstates what the data shows:
```
OVERCLAIM at Section X.Y:
  Text: [exact text]
  Issue: [why this overstates]
  Suggested rewrite: [more accurate phrasing]
```

### Part 4: Structural and Writing Issues

- Missing sections or topics that should be covered
- Unclear explanations
- Redundancies
- Missing figure/table references

### Part 5: Overall Assessment

```json
{
  "scores": {
    "technical_accuracy": X,
    "logical_coherence": X,
    "honest_reporting": X,
    "clarity": X,
    "novelty": X,
    "reproducibility": X
  },
  "recommendation": "accept_as_is | minor_revisions | major_revisions | reject",
  "summary": "2-3 sentence overall assessment",
  "top_3_strengths": ["...", "...", "..."],
  "top_3_weaknesses": ["...", "...", "..."]
}
```

## Output

Write your complete review to:
`paper/review-gpt54.md`

Write the structured assessment JSON to:
`paper/review-gpt54-scores.json`

After completing both files, write a marker:
`paper/review-gpt54-COMPLETE.json`
```json
{"model": "gpt-5.4", "role": "reviewer", "timestamp": "ISO 8601", "status": "complete"}
```
