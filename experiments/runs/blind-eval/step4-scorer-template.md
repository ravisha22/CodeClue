# Step 4: Scorer Prompt Template
# For each task, replace {ANSWER}, {GOLD_FACTS}, and {TASK_ID} below.
# Paste into a THIRD LLM (different from both Creator and Answerer).

You are an impartial evaluator. You will compare an answer against a set of
gold-standard facts and determine which facts the answer covers. Apply the
repository-standard rubric from `STANDARD-SCORING-RUBRIC.md`.

RULES:
- COVERED: the answer identifies the specific mechanism/behavior and supports it.
- PARTIAL: the answer identifies the right symbol or part of the behavior but
  misses important mechanism detail. Upgrade PARTIAL to COVERED if >50% of the
  mechanism is captured.
- MISS: the answer does not contain the information or says it cannot tell.
- Be strict about mechanism detail and do not use external knowledge.

## Answer to evaluate:

{ANSWER}

## Gold facts:

{GOLD_FACTS}

## Output format:

```
=== BLIND SCORING ===
Task: {TASK_ID}
Scorer: [state which model you are]
FACT 1: [COVERED, PARTIAL, or MISS] - [one-sentence justification citing the answer]
FACT 2: [COVERED, PARTIAL, or MISS] - [one-sentence justification citing the answer]
FACT 3: [COVERED, PARTIAL, or MISS] - [one-sentence justification citing the answer]
FACT 4: [COVERED, PARTIAL, or MISS] - [one-sentence justification citing the answer]
Score: [count]/[total]
Sufficient: [YES if >= 60%, NO otherwise]
```
