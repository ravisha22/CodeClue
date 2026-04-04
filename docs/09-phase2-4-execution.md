# Phase 2-4 Execution Guide

## Phase 2: Graph Integrity and Delta Proofs

Run integrity analysis:

```bash
python -m codeclue_research integrity --graph-file experiments/runs/pilot-001/graph.json --output-file experiments/runs/pilot-001/integrity.json
```

Apply delta patch with proof checks:

```bash
python -m codeclue_research delta-apply --base-graph experiments/runs/pilot-001/graph.json --delta-file tests/fixtures/sample_delta_patch.json --repo-root . --output-graph experiments/runs/pilot-001/graph-delta.json --output-report experiments/runs/pilot-001/delta-report.json
```

## Phase 3: Multi-Language Extraction

Extract from Python, TypeScript, and Go in one graph:

```bash
python -m codeclue_research extract --repo-root . --language auto --output experiments/runs/pilot-ml/graph.json --commit-id pilot-ml
```

## Phase 4: Unified Pilot Runner

Run extract + validate + roundtrip + integrity + optional CCT:

```bash
python -m codeclue_research run-pilot --repo-root . --run-dir experiments/runs/pilot-unified --commit-id pilot-unified --language auto --probe-file tests/fixtures/sample_probe.yaml --trace-file tests/fixtures/sample_trace.jsonl
```
