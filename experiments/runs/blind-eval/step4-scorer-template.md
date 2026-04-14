# Step 4: Scorer Prompt Template
# For each task, replace {ANSWER}, {GOLD_FACTS}, and {TASK_ID} below.
# Paste into a THIRD LLM (different from both Creator and Answerer).

You are an impartial evaluator. You will compare an answer against a set of
gold-standard facts and determine which facts the answer covers.

RULES:
- A fact is COVERED if the answer states it directly OR contains enough
  information that the fact can be logically inferred with high confidence.
- A fact is MISSED if the answer does not contain the information and it
  cannot be reasonably inferred from what is stated.
- Be strict: vague proximity is not coverage. "uses cryptographic signing"
  covers "data is signed" but does NOT cover "uses SECRET_KEY" unless
  SECRET_KEY is mentioned.
- Do not give credit for external knowledge the answerer might have.
  Only credit information that demonstrably came from the clue.

## Answer to evaluate:

{ANSWER}

## Gold facts:

{GOLD_FACTS}

## Output format:

```
=== BLIND SCORING ===
Task: {TASK_ID}
Scorer: [state which model you are]
FACT 1: [COVERED or MISSED] - [one-sentence justification citing the answer]
FACT 2: [COVERED or MISSED] - [one-sentence justification citing the answer]
FACT 3: [COVERED or MISSED] - [one-sentence justification citing the answer]
FACT 4: [COVERED or MISSED] - [one-sentence justification citing the answer]
Score: [count]/[total]
Sufficient: [YES if >= 60%, NO otherwise]
```
