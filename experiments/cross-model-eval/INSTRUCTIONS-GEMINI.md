# Instructions for Gemini 3.1 Pro — Independent Judge
# Role: JUDGE
# You score answers from GPT 5.4 against ground truth.
# You did NOT generate the clues. You did NOT answer the tasks.

## Prerequisites

Wait until GPT 5.4 has finished. Check for:
`experiments/cross-model-eval/results/gpt54-COMPLETE.json`

If it doesn't exist yet, stop and tell the user to run the GPT 5.4 tab first.

## Your Task

Score GPT 5.4's Arm B and Arm A answers against ground truth for all 23 tasks.
Also compare with Claude Opus 4.6's prior scores.

## Input Files

1. **Task definitions with ground truth** — read `ground_truth_summary` from:
   - `tests/fixtures/lane_a_flask_tasks.yaml`
   - `tests/fixtures/lane_a_extended_tasks.yaml`
   - `tests/fixtures/lane_a_newrepo_tasks.yaml`

2. **GPT 5.4 answers** — read from:
   `experiments/cross-model-eval/results/gpt54-{task_id}.json`

3. **Claude's prior scores** — read from:
   `experiments/reports/v2-benchmark-all-23.json`
   
   For existing 15 tasks, Claude scores are in `existing_15_tasks_v2[].arm_b_fs` and `arm_a_fs`.
   For new 8 tasks, scores are in `new_8_tasks_v2[].arm_b_fs` and `arm_a_fs`.

## Scoring Scale

Score each answer on a continuous 0.0 to 1.0 fidelity scale:

- **1.0** = Fully correct. All key points from ground truth covered accurately.
- **0.85** = Nearly complete. One minor point missing but no errors.
- **0.75** = Mostly correct. 1-2 secondary points missing.
- **0.60** = Partially correct. Core structural understanding present but behavioral detail missing.
- **0.50** = Half right. Key points present but significant gaps.
- **0.35** = Poor. Only surface-level structural info, missing behavioral semantics.
- **0.20** = Very poor. Mostly wrong or extremely incomplete.
- **0.0** = Wrong, empty, or hallucinated.

Key scoring principles:
- A correct but incomplete answer scores higher than a complete but inaccurate one.
- Hallucinated claims (stating things not in source) score LOWER than admitting gaps.
- "I cannot determine this from the clue" is an honest answer, not a failure — score based on what WAS correctly stated.

## Output

For each task, write:
`experiments/cross-model-eval/results/gemini-judge-{task_id}.json`

```json
{
  "task_id": "flask-tf1-001",
  "judge_model": "gemini-3.1-pro",
  "timestamp": "ISO 8601",
  "gpt54_arm_b": {
    "score": 0.65,
    "key_points_hit": ["identified wsgi_app as entry", "found dispatch_request"],
    "key_points_missed": ["did not identify context push/pop mechanics"],
    "hallucinations": [],
    "notes": "Structural understanding good, behavioral flow missing"
  },
  "gpt54_arm_a": {
    "score": 0.92,
    "key_points_hit": ["full pipeline identified", "context mechanics correct", "teardown flow correct"],
    "key_points_missed": ["minor: did not mention error handler integration"],
    "hallucinations": [],
    "notes": "Comprehensive answer from source"
  },
  "claude_prior": {
    "arm_b_score": 0.70,
    "arm_a_score": 0.95
  },
  "delta_vs_claude": {
    "arm_b_delta": -0.05,
    "arm_a_delta": -0.03
  }
}
```

## After All 23 Tasks Are Scored

Create the final summary at:
`experiments/cross-model-eval/results/gemini-judge-SUMMARY.json`

```json
{
  "judge_model": "gemini-3.1-pro",
  "consumer_model": "gpt-5.4",
  "baseline_model": "claude-opus-4.6",
  "timestamp": "ISO 8601",
  "total_tasks_scored": 23,
  "gpt54_aggregate": {
    "arm_b_mean": 0.00,
    "arm_a_mean": 0.00,
    "tasks_clue_sufficient": 0,
    "hallucination_count": 0
  },
  "claude_aggregate": {
    "arm_b_mean": 0.54,
    "arm_a_mean": 0.93
  },
  "cross_model_comparison": {
    "arm_b_spearman_correlation": 0.00,
    "arm_a_spearman_correlation": 0.00,
    "arm_b_mean_absolute_delta": 0.00,
    "arm_a_mean_absolute_delta": 0.00,
    "tf3_clue_sufficient_both_models": false,
    "rank_order_agreement": "describe whether task difficulty ranking agrees"
  },
  "per_family": {
    "TF1": {"gpt54_arm_b_mean": 0.00, "claude_arm_b_mean": 0.00, "delta": 0.00},
    "TF2": {"gpt54_arm_b_mean": 0.00, "claude_arm_b_mean": 0.00, "delta": 0.00},
    "TF3": {"gpt54_arm_b_mean": 0.00, "claude_arm_b_mean": 0.00, "delta": 0.00},
    "TF4": {"gpt54_arm_b_mean": 0.00, "claude_arm_b_mean": 0.00, "delta": 0.00},
    "TF5": {"gpt54_arm_b_mean": 0.00, "claude_arm_b_mean": 0.00, "delta": 0.00}
  },
  "validation_criteria": {
    "spearman_gte_070": false,
    "mean_delta_lte_015": false,
    "tf3_replicates": false,
    "zero_hallucinations_both": false,
    "overall_pass": false
  },
  "verdict": "PASS or FAIL with explanation"
}
```

Compute the Spearman rank correlation by ranking all 23 tasks by Arm B score for
GPT 5.4 and Claude separately, then correlating the ranks.

## Processing Order

Score in the same order as GPT 5.4 processed them.
Start only after confirming gpt54-COMPLETE.json exists.
