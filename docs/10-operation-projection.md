# Phase 5: Operation Projection Engine (OF1-OF5)

## Purpose

Generate task-conditioned subgraphs from one canonical clue graph, with prompt-profile routing and trace output.

## Command

```bash
python -m codeclue_research project --graph-file experiments/runs/pilot-unified-r2/graph.json --operation-family OF2 --prompt-profile-file tests/fixtures/prompt_profile_impact.yaml --output-file experiments/runs/pilot-unified-r2/projection-of2.json
```

## Notes

- OF1: architecture view
- OF2: impact analysis view
- OF3: edit-point localization view
- OF4: behavior/debugging view
- OF5: security/compliance view

Each run emits:

- projected nodes and edges
- ordered reasoning path
- validation metrics for projection quality proxies

Metric interpretation:

- `path_recall`: context-normalized recall (coverage within the candidate operational universe for the selected family and prompt profile).
- `path_recall_global`: global recall against total graph size (useful as a compression/context-budget indicator, not as family-level fidelity).
