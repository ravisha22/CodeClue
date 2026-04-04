# Instructions for Gemini 3.1 Pro — Meta-Review and Correction Application
# Role: META-REVIEWER AND EDITOR
# You review GPT 5.4's review, verify its corrections, and apply fixes to the paper.

## Prerequisites

Wait until GPT 5.4's review is complete. Check for:
`paper/review-gpt54-COMPLETE.json`

If it doesn't exist, stop and tell the user to run GPT 5.4 first.

## Your Task (Three Parts)

### Part 1: Meta-Review — Judge GPT 5.4's Review

Read GPT 5.4's review at `paper/review-gpt54.md` and its scores at `paper/review-gpt54-scores.json`.

For each factual correction GPT 5.4 identified:
1. Verify it yourself by reading the actual data file cited.
2. Mark as: CONFIRMED (GPT is right), DISPUTED (GPT is wrong), or PARTIAL (partially right).

For each logical issue or overclaim:
1. Assess whether you agree.
2. If you disagree, explain why.

Write your meta-review to: `paper/meta-review-gemini.md`

Format:
```
## Meta-Review: Gemini 3.1 Pro Assessment of GPT 5.4's Review

### Factual Corrections
- GPT correction 1: [CONFIRMED/DISPUTED/PARTIAL] — [your verification]
- GPT correction 2: ...

### Logical Issues
- GPT issue 1: [AGREE/DISAGREE] — [reasoning]
- ...

### Overclaims
- GPT overclaim 1: [AGREE/DISAGREE] — [reasoning]
- ...

### GPT Review Quality Assessment
- Thoroughness: X/5
- Accuracy of corrections: X/5
- Fairness: X/5

### Items GPT Missed
- [anything you caught that GPT didn't]
```

### Part 2: Apply CONFIRMED Corrections

Read the original paper at `paper/codeclue-arxiv-draft.md`.

For every correction that is CONFIRMED (by both GPT 5.4 and your verification):
- Apply the fix directly to the paper.
- Also apply any corrections YOU identified that GPT missed.

Do NOT apply DISPUTED corrections.

For PARTIAL corrections, apply only the part that is verified.

Save the corrected paper to: `paper/codeclue-arxiv-final.md`

### Part 3: Produce a Change Log

Write a change log documenting every edit made:
`paper/corrections-applied.md`

Format:
```
## Corrections Applied to CodeClue Paper

### From GPT 5.4 Review (CONFIRMED)
1. Section X.Y: Changed "Z" to "W" (source: file.json, field)
2. ...

### From Gemini Meta-Review (additional)
1. Section X.Y: Changed "Z" to "W" (reason)
2. ...

### DISPUTED (not applied)
1. GPT suggested X, but data shows Y because...

### Summary
- Total corrections from GPT: N confirmed, M disputed, P partial
- Additional corrections from Gemini: Q
- Paper version: final (ready for arXiv)
```

## Output Files

1. `paper/meta-review-gemini.md` — your meta-review of GPT's review
2. `paper/codeclue-arxiv-final.md` — the corrected paper
3. `paper/corrections-applied.md` — change log
4. `paper/gemini-editor-COMPLETE.json`:
```json
{
  "model": "gemini-3.1-pro",
  "role": "meta-reviewer-editor",
  "timestamp": "ISO 8601",
  "corrections_confirmed": 0,
  "corrections_disputed": 0,
  "corrections_partial": 0,
  "additional_corrections": 0,
  "final_paper": "paper/codeclue-arxiv-final.md"
}
```
