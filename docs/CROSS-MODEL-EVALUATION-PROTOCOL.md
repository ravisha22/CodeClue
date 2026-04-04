# CodeClue Cross-Model Evaluation Protocol
# Purpose: Eliminate self-evaluation bias by having independent models score the benchmark

## Overview

This protocol enables a second (evaluator) model to independently score the same
23 benchmark tasks that were originally scored by Claude Opus 4 as self-consumer.

The evaluator model:
1. Reads each clue projection (Arm B) and answers the question from clue only.
2. Reads the raw source files (Arm A) and answers the same question.
3. Scores are compared against the ground truth in the task YAML files.
4. The evaluator's scores are compared to Claude Opus 4's scores to detect bias.

## Recommended Models

### For Arm B/A Task Execution (Consumer Role)
Use models from DIFFERENT families than Claude to ensure cross-model validity:

| Model | Why | Access |
| --- | --- | --- |
| GPT-4o (primary) | Different family, strong reasoning, comparable capability | OpenAI API |
| Gemini 2.5 Pro | Third family, long context (1M tokens) | Google AI API |
| Qwen3-235B | Open-weights, strong on code, fourth family | Fireworks/Together/local |

Run with at least 2 of the above. Three eliminates pairwise bias.

### For Independent Scoring (Judge Role)
Use a model that did NOT generate the clue OR answer the task:

| If consumer was | Use as judge |
| --- | --- |
| GPT-4o consumed | Gemini 2.5 judges |
| Gemini consumed | GPT-4o judges |
| Claude consumed | Either GPT-4o or Gemini judges |

The judge scores each answer against ground truth on the same 0-1 fidelity scale.

## Prerequisites

```bash
cd C:\Users\ranandag\Documents\VSCodeProjects\CodeClue-Research-Scaffold
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

Verify the v2 code is installed:
```bash
python -c "from codeclue_research.confidence import compute_structural_confidence; print('OK')"
```

## Step 1: Extract Fresh Graphs (Skip if v2 graphs exist)

V2 graphs should already exist in `experiments/runs/v2-lane-a-{repo}/graph.json`.
Verify:
```bash
foreach($r in @("flask","fastapi","nest","httpx","express","typeorm","gin")) {
  $g = "experiments/runs/v2-lane-a-$r/graph.json"
  if (Test-Path $g) { Write-Host "$r : OK" } else { Write-Host "$r : MISSING" }
}
```

If any are missing, re-extract:
```bash
python -m codeclue_research extract \
  --repo-root experiments/external-repos/{repo} \
  --language {python|typescript|go} \
  --output experiments/runs/v2-lane-a-{repo}/graph.json \
  --commit-id {sha}
```

## Step 2: Load Task Definitions

All 23 tasks are defined in three YAML files:
- `tests/fixtures/lane_a_flask_tasks.yaml` (5 tasks: flask TF1-TF5)
- `tests/fixtures/lane_a_extended_tasks.yaml` (10 tasks: flask +2, fastapi +4, nest +4)
- `tests/fixtures/lane_a_newrepo_tasks.yaml` (8 tasks: httpx +2, express +2, typeorm +2, gin +2)

Each task has:
- `task_id`: unique identifier
- `family`: TF1-TF5
- `operation_family`: OF1-OF5
- `question`: the comprehension question
- `ground_truth_summary`: the expected answer
- `relevant_files`: source files needed for Arm A
- `prompt_profile`: projection configuration

## Step 3: Generate Projections (Skip if v2 projections exist)

Projections should exist as `experiments/runs/v2-lane-a-{repo}/v2-proj-{task_id}.json`.

If missing, run:
```bash
python experiments/runs/v2_pipeline.py      # 15 existing tasks
python experiments/runs/v2_newrepo_pipeline.py  # 8 new tasks
```

## Step 4: Execute Arm B (Clue-First) with External Model

For each task, provide the evaluator model with ONLY:
1. The projection JSON (the `projected_nodes` and `projected_edges` sections)
2. The confidence block (the `confidence` section)
3. The question

**IMPORTANT**: Do NOT provide raw source files. Do NOT provide ground truth.

### Prompt Template for Arm B

```
You are evaluating a code comprehension clue system. You will receive a
projected subgraph from a codebase and a question. Answer the question
using ONLY the information in the projection. If the projection is
insufficient, state what is missing.

## Projected Nodes
{paste projected_nodes from v2-proj-{task_id}.json}

## Projected Edges
{paste projected_edges from v2-proj-{task_id}.json}

## Confidence
Overall: {confidence_overall}
Hint: {lookup_decision_hint}

## Question
{question from task YAML}

Answer the question. Then assess: was the clue sufficient, or would you
need to look at the source code? List specific gaps if any.
```

Record:
- The model's answer
- Whether the model said clue was sufficient (yes/no)
- What gaps the model identified

## Step 5: Execute Arm A (Raw-First) with Same Model

For each task, provide the evaluator model with:
1. The raw source files listed in `relevant_files`
2. The question

**IMPORTANT**: Do NOT provide the clue projection. This is the control arm.

### Prompt Template for Arm A

```
You are answering a code comprehension question by reading source code.

## Source Files
{paste contents of each file listed in relevant_files}

## Question
{question from task YAML}

Answer the question comprehensively.
```

## Step 6: Score with Independent Judge

For each task, the judge model receives:
1. The ground truth summary from the task YAML
2. The consumer model's Arm B answer
3. The consumer model's Arm A answer

### Scoring Prompt

```
You are a scoring judge for a code comprehension benchmark. Score each
answer on a 0-1 fidelity scale where:
- 1.0 = fully correct, all key points from ground truth covered
- 0.75 = mostly correct, minor details missing
- 0.50 = partially correct, key structural points present but behavioral detail missing
- 0.25 = poor, only surface-level correct
- 0.0 = wrong or empty

## Ground Truth
{ground_truth_summary from task YAML}

## Answer A (raw-source-first)
{Arm A answer}

## Answer B (clue-first)
{Arm B answer}

For each answer, output:
- fidelity_score: float in [0, 1]
- key_points_hit: list of ground truth points that were correctly addressed
- key_points_missed: list of ground truth points that were missing
- hallucinations: list of claims not supported by ground truth (if any)
```

## Step 7: Record Results

Save results to `experiments/reports/cross-model-eval-{model_name}.json`:

```json
{
  "evaluator_model": "gpt-4o-2026-04",
  "judge_model": "gemini-2.5-pro",
  "timestamp": "ISO 8601",
  "tasks": [
    {
      "task_id": "flask-tf1-001",
      "arm_b_score": 0.65,
      "arm_a_score": 0.92,
      "arm_b_clue_sufficient": false,
      "arm_b_gaps_identified": ["could not see call chain ordering"],
      "hallucinations": [],
      "claude_arm_b_score": 0.70,
      "claude_arm_a_score": 0.95,
      "delta_vs_claude_arm_b": -0.05,
      "delta_vs_claude_arm_a": -0.03
    }
  ],
  "aggregate": {
    "arm_b_mean": 0.00,
    "arm_a_mean": 0.00,
    "correlation_with_claude_arm_b": 0.00,
    "correlation_with_claude_arm_a": 0.00,
    "mean_delta_arm_b": 0.00
  }
}
```

## Step 8: Validation Criteria

The cross-model evaluation passes if:

1. **Rank-order agreement**: Spearman correlation between evaluator scores and Claude scores >= 0.70
   (the two models rank tasks in similar difficulty order).

2. **Mean delta bounded**: |mean(evaluator_arm_b) - mean(claude_arm_b)| <= 0.15
   (the absolute fidelity scores are within 15 points of each other).

3. **Hallucination agreement**: Both models report zero hallucinations, or discrepancies are adjudicated.

4. **TF3 finding replicates**: Evaluator model also finds TF3 tasks clue-sufficient.

If these pass, the self-evaluation bias concern is retired.
