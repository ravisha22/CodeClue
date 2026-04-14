
=== SCORING GUIDE (DO NOT SEND TO LLM) ===
Task: flask-tf1-refactor-sessions
Repo: flask
Family: TF1

Gold Facts to check in the LLM's answer:
  FACT 1: SessionInterface.open_session and save_session are the core abstract methods
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this

  FACT 2: SecureCookieSessionInterface uses URLSafeTimedSerializer with SECRET_KEY for signing
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this

  FACT 3: Flask app stores session_interface property which can be replaced
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this

  FACT 4: Session persistence is handled via response hooks in request teardown
    [ ] PRESENT — LLM's answer contains or implies this fact
    [ ] ABSENT  — LLM's answer does not mention this


Scoring:
  Count PRESENT facts: ___/4
  Fidelity = PRESENT / TOTAL = ___
  Sufficient (fidelity >= 0.60)? YES / NO
