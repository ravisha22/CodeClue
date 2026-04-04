# Phase 1 Implementation Notes

This phase ships runnable tooling for:

- Canonical graph extraction from Python repositories.
- Invariant validation for clue graph integrity.
- Lossless round-trip checks across JSON and YAML.
- Comprehension Circuit Tracing (CCT) probe execution.

## CLI Commands

Install local editable package from repository root:

```bash
pip install -e .
```

If `codeclue` is not on your shell `PATH`, use module invocation:

```bash
python -m codeclue_research <subcommand> ...
```

Extract graph:

```bash
codeclue extract --repo-root . --output experiments/runs/pilot-001/graph.json --commit-id local-dev
```

```bash
python -m codeclue_research extract --repo-root . --output experiments/runs/pilot-001/graph.json --commit-id local-dev
```

Validate graph:

```bash
codeclue validate --graph-file experiments/runs/pilot-001/graph.json --repo-root .
```

```bash
python -m codeclue_research validate --graph-file experiments/runs/pilot-001/graph.json --repo-root .
```

Round-trip checks:

```bash
codeclue roundtrip --graph-file experiments/runs/pilot-001/graph.json
```

```bash
python -m codeclue_research roundtrip --graph-file experiments/runs/pilot-001/graph.json
```

Run CCT sample:

```bash
codeclue cct --probe-file tests/fixtures/sample_probe.yaml --trace-file tests/fixtures/sample_trace.jsonl --output-file experiments/runs/pilot-001/cct-result.json
```

```bash
python -m codeclue_research cct --probe-file tests/fixtures/sample_probe.yaml --trace-file tests/fixtures/sample_trace.jsonl --output-file experiments/runs/pilot-001/cct-result.json
```
