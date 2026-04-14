
=== SCORING GUIDE (DO NOT SEND TO LLM) ===
Task: gin-tf5-credential-handling
Repo: gin
Family: TF5

Gold Facts to check in the LLM's answer:
  FACT 1: AuthUserKey is a constant string key for storing authenticated user identity
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this

  FACT 2: Context.Keys map is protected by sync.RWMutex for concurrent request safety
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this

  FACT 3: searchCredential uses subtle.ConstantTimeCompare to prevent timing-based credential leaks
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this

  FACT 4: Context provides Set/Get interface for storing request-scoped sensitive data
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this


Scoring:
  Count PRESENT facts: ___/4
  Fidelity = PRESENT / TOTAL = ___
  Sufficient (fidelity >= 0.60)? YES / NO
