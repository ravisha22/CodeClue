# CCT Expansion Summary

Date: 2026-03-28

## Executed Probes

| Probe ID | Task ID | Passed | PP | PR | CS | CRR | PDI |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| cct_probe_adversarial_v1 | task-adversarial-001 | True | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 0.000000 |
| cct_probe_counterfactual_v1 | task-counterfactual-001 | True | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 0.000000 |

## Input Artifacts

- tests/fixtures/cct_probe_adversarial.yaml
- tests/fixtures/cct_trace_adversarial.jsonl
- tests/fixtures/cct_probe_counterfactual.yaml
- tests/fixtures/cct_trace_counterfactual.jsonl

## Output Artifacts

- experiments/reports/cct-adversarial-result.json
- experiments/reports/cct-counterfactual-result.json

## Notes

- Contradiction rejection and path agreement thresholds passed for both new probes.
- Probe fixtures are structured for direct use with `python -m codeclue_research cct`.