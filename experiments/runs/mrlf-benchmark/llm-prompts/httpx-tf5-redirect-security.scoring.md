
=== SCORING GUIDE (DO NOT SEND TO LLM) ===
Task: httpx-tf5-redirect-security
Repo: httpx
Family: TF5

Gold Facts to check in the LLM's answer:
  FACT 1: URLs are validated and normalized on instantiation to prevent injection
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this

  FACT 2: Client enforces DEFAULT_MAX_REDIRECTS limit to prevent redirect loops
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this

  FACT 3: HTTPS-to-HTTP downgrades are detected during redirect following
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this

  FACT 4: TooManyRedirects exception raised when redirect count exceeds limit
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this


Scoring:
  Count PRESENT facts: ___/4
  Fidelity = PRESENT / TOTAL = ___
  Sufficient (fidelity >= 0.60)? YES / NO
