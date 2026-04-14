
=== SCORING GUIDE (DO NOT SEND TO LLM) ===
Task: fastapi-tf4-form-parsing
Repo: fastapi
Family: TF4

Gold Facts to check in the LLM's answer:
  FACT 1: Form() parameter triggers multipart or urlencoded parsing based on Content-Type
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this

  FACT 2: solve_dependencies resolves all parameters and returns dict of resolved values
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this

  FACT 3: RequestValidationError raised if form data fails Pydantic model validation
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this

  FACT 4: File uploads use UploadFile wrapper with async read/write interface
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this


Scoring:
  Count PRESENT facts: ___/4
  Fidelity = PRESENT / TOTAL = ___
  Sufficient (fidelity >= 0.60)? YES / NO
