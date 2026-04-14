
=== SCORING GUIDE (DO NOT SEND TO LLM) ===
Task: fastapi-tf5-input-validation
Repo: fastapi
Family: TF5

Gold Facts to check in the LLM's answer:
  FACT 1: All inputs are validated against Pydantic models with type checking and coercion
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this

  FACT 2: Path parameters are automatically validated by type hints
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this

  FACT 3: Query parameters support constraints like min_length, max_length, regex
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this

  FACT 4: RequestValidationError raised with detailed field-level error information on validation failure
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this


Scoring:
  Count PRESENT facts: ___/4
  Fidelity = PRESENT / TOTAL = ___
  Sufficient (fidelity >= 0.60)? YES / NO
