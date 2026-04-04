# Phase 6: Gold-Path Fidelity Evaluation

## Purpose

Evaluate projection quality against external gold paths (task-specific expected nodes and edges), instead of relying only on policy-local metrics.

## Command

```bash
python -m codeclue_research fidelity-eval --projection-file experiments/runs/batch-of/of2.json --gold-file tests/fixtures/gold_path_impact.yaml --output-file experiments/reports/of2-fidelity.json
```

## Metrics

- node precision, recall, F1
- edge precision, recall, F1
- path_fidelity = average(node_f1, edge_f1)

## Pass Criteria

Pass/fail is determined by threshold values in the gold file:

- `node_f1_min`
- `edge_f1_min`
- `path_fidelity_min`
