
=== SCORING GUIDE (DO NOT SEND TO LLM) ===
Task: fastapi-tf1-dependency-injection
Repo: fastapi
Family: TF1

Gold Facts to check in the LLM's answer:
  FACT 1: get_dependant analyzes function signatures and annotations to extract dependency metadata
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this

  FACT 2: Dependant stores dependency chain including path params, query params, body, and sub-dependents
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this

  FACT 3: Dependencies can be sync callable, async callable, or context manager
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this

  FACT 4: Cache keys are generated per unique dependency signature for memoization
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this


Scoring:
  Count PRESENT facts: ___/4
  Fidelity = PRESENT / TOTAL = ___
  Sufficient (fidelity >= 0.60)? YES / NO
