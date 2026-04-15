## Standard Scoring Rubric

### Fact Labels
- **COVERED**: The response describes the specific mechanism or behavior from the gold fact and includes supporting evidence. Exact wording is not required, but the core behavior must be identified, not just the function or class name.
- **PARTIAL**: The response identifies the right function/class or hints at the behavior, but misses important mechanism detail. Upgrade PARTIAL to **COVERED** when more than 50% of the mechanism is captured.
- **MISS**: The response does not contain the information, gives the wrong behavior, or explicitly says it cannot determine the answer.

### Grounding Rules
- Judge only what is present in the answer.
- Do not award credit for external framework knowledge.
- Prefer mechanism-level evidence over symbol-name mentions.
- When a response only names a symbol, treat that as **PARTIAL** unless it also explains the mechanism.
- When in doubt between **PARTIAL** and **MISS**, use **PARTIAL** only if the answer points to the correct code element and some correct behavior.
