
=== SCORING GUIDE (DO NOT SEND TO LLM) ===
Task: flask-tf5-session-security
Repo: flask
Family: TF5

Gold Facts to check in the LLM's answer:
  FACT 1: Session data is cryptographically signed with SECRET_KEY to detect tampering
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this

  FACT 2: itsdangerous URLSafeTimedSerializer includes timestamp to prevent replay attacks
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this

  FACT 3: Session is stored as cookie value with optional secure, httponly, and samesite flags
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this

  FACT 4: NullSession raises RuntimeError if SECRET_KEY is not set, preventing unencrypted sessions
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this


Scoring:
  Count PRESENT facts: ___/4
  Fidelity = PRESENT / TOTAL = ___
  Sufficient (fidelity >= 0.60)? YES / NO
