# Blind Evaluation Prompt
# Run this in a SEPARATE VS Code Copilot Chat session (fresh chat, no prior context).

You have THREE tasks to complete. Read carefully.

=== TASK 1: ANSWER THE QUESTION ===

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code — it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.
If the clue does not contain enough information to fully answer, say what
you CAN determine and what you CANNOT.

--- CLUE FILE START ---
{CLUE_CONTENT}
--- CLUE FILE END ---

QUESTION: {QUESTION}

Provide a detailed answer covering:
1. Which specific files and symbols are involved (cite from the clue)
2. How the mechanism works (based on what the clue tells you)
3. Any error handling, invariants, or safety properties visible in the clue
4. What the clue does NOT tell you (gaps in your understanding)

=== TASK 2: SCORE YOUR ANSWER ===

After writing your answer above, score it against these gold facts.
For EACH fact, state COVERED (your answer contains or can infer this) or
MISSED (your answer does not contain this). Be strict — vague proximity
is not coverage.

{GOLD_FACTS_BLOCK}

=== TASK 3: WRITE RESULTS TO FILE ===

After completing Tasks 1 and 2, create or append to the file:
`experiments/runs/blind-eval/blind-eval-results.jsonl`

Write ONE JSON line (append, do not overwrite) with this exact structure:
```json
{"task_id": "{TASK_ID}", "model": "<your model name>", "scores": [{SCORING_JSON_TEMPLATE}], "total_covered": <count>, "total_facts": <total>, "sufficient": <true or false>}
```

Replace each score entry with your actual COVERED/MISSED judgment.

Also output the scoring block in your response for visibility:

```
=== BLIND SCORING ===
Task: {TASK_ID}
Model: [state which model you are]
{SCORING_LINES}
Score: [count of COVERED]/[total]
Sufficient: [YES if >= 60%, NO otherwise]
```
