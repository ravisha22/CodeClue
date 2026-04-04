# Comprehension Circuit Tracing (CCT)

CCT validates whether clue-based reasoning preserves the causal structure of source-based reasoning.

## Test Suite

- cct-path-agreement: compare inferred reasoning path with expected path.
- cct-causal-ablation: remove critical nodes and verify expected degradation.
- cct-contradiction-injection: insert false claims and verify rejection.
- cct-counterfactual-patch: modify branch behavior and verify path re-routing.

## Required Outputs

- trace.jsonl with ordered reasoning steps
- path-metrics.json with PP, PR, CS, CRR, PDI
- failure-report.md with root cause and violated invariants
