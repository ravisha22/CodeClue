# Blind Evaluation Pipeline — Instructions

## Overview

This pipeline tests CodeClue's two-file comprehension system on repos and
tasks it was never tuned against, using model separation to prevent bias.

**Chain:**
1. Creator LLM (Model A) creates gold tasks from raw source → you save these
2. My code generates clue files (File 1 + File 2) → automated
3. Answerer LLM (Model B) reads clue and answers → you run these prompts
4. Scorer LLM (Model C) scores answers against gold facts → you run these

**No model appears in more than one role.**

## Repos (never used in development)

| Repo | Language | Modules | Symbols | Domain |
|------|----------|---------|---------|--------|
| aiohttp | Python | 166 | 6,741 | Async HTTP client/server |
| fiber | Go | 243 | 3,893 | HTTP framework |
| click | Python | 63 | 1,620 | CLI framework |

## Step 1: Create Gold Tasks

Open a **fresh chat** with GPT-5.4 (or Gemini 3.4 — NOT Claude).
Paste the STEP1 prompt from `step1-creator-prompt.md`.
For each repo, the Creator LLM will produce 2 tasks (6 total).
Save the output as `blind-gold-tasks.json`.

## Step 2: Generate Clues

Run: `python experiments/runs/run_blind_eval_clues.py`
This generates File 1 (.codeclue) and File 2 (.codeclue-detail) for each task.

## Step 3: Answer from Clue

For each task, paste the STEP3 prompt (with clue embedded) into a
**different LLM** than the Creator. If Creator was GPT-5.4, use Gemini or Claude.
Collect the answers.

## Step 4: Score

Paste each answer + gold facts into the STEP4 scorer prompt on a **third LLM**
(different from both Creator and Answerer). Collect COVERS/MISSES scores.

## Step 5: Repeat with Drill-Down

For tasks that scored < 60%, append File 2 detail records and re-run Step 3+4.
