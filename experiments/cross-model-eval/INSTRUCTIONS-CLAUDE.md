# Instructions for Claude Opus 4.6 — Tier 2 Contract Generation
# Role: GENERATOR
# You are generating structured semantic contracts for Flask source files.

## Your Task

Generate Tier 2 semantic contracts for every function and method in 8 Flask source files.
These contracts enrich the existing Tier 1 structural graph with behavioral semantics.

## Input Files (read each one)

1. `experiments/external-repos/flask/src/flask/app.py`
2. `experiments/external-repos/flask/src/flask/ctx.py`
3. `experiments/external-repos/flask/src/flask/sessions.py`
4. `experiments/external-repos/flask/src/flask/config.py`
5. `experiments/external-repos/flask/src/flask/blueprints.py`
6. `experiments/external-repos/flask/src/flask/helpers.py`
7. `experiments/external-repos/flask/src/flask/wrappers.py`
8. `experiments/external-repos/flask/src/flask/testing.py`

## Output Format

For each source file, create a YAML file at:
`experiments/runs/tier2-flask/{filename_without_path}.contracts.yaml`

Example: `app.py` → `experiments/runs/tier2-flask/app.py.contracts.yaml`

The YAML structure must be a dict where each key is a function/method name:

```yaml
function_name:
  preconditions:
    - type: parameter_valid|state_required|auth_required|config_required
      target: "parameter or state name"
      constraint: "description of constraint"
  postconditions:
    - type: return_value|state_mutation|side_effect|event_emitted
      target: "what is affected"
      description: "what happens"
  failure_modes:
    - trigger: "what causes failure"
      effect: "what happens"
      exception_type: "ExceptionClass or null"
  complexity_indicators:
    uses_reflection: false
    uses_generics: false
    uses_dynamic_dispatch: false
    uses_metaprogramming: false
```

## Rules

- Process ALL functions and methods, not just public ones.
- For class methods, use the format `ClassName.method_name` as the key.
- If a function has no preconditions, use an empty list `[]`.
- Be precise about exception types — use the actual Python exception class names.
- For `uses_dynamic_dispatch`, mark true if the function calls methods on objects
  where the concrete type varies (e.g., `self.session_interface.open_session()`).
- For `uses_reflection`, mark true if the function uses `getattr`, `hasattr`,
  `inspect`, or `importlib`.

## Execution Order

Process files in this order (largest first to catch issues early):
1. app.py (largest — ~1600 lines, many methods)
2. ctx.py
3. sessions.py
4. testing.py
5. config.py
6. blueprints.py
7. helpers.py
8. wrappers.py

## After All 8 Files Are Done

1. Run this command to inject contracts into the graph:
```bash
.\.venv\Scripts\python.exe experiments/runs/inject_tier2.py
```

2. Then re-project the 7 Flask tasks with the Tier 2 graph:
```bash
.\.venv\Scripts\python.exe experiments/runs/tier2_reproject.py
```

3. Write a summary of Tier 2 generation to:
`experiments/cross-model-eval/results/claude-tier2-generation-summary.json`

Format:
```json
{
  "model": "claude-opus-4.6",
  "timestamp": "ISO 8601",
  "files_processed": 8,
  "total_functions_contracted": <count>,
  "per_file": {
    "app.py": {"functions": <n>, "methods": <n>},
    ...
  },
  "issues_encountered": ["list any ambiguities or difficult cases"]
}
```
