# Test Harness

## Purpose

Execute study arms A/B/C (and optional D), collect metrics, and enforce decision gates.

## Inputs

- Repository snapshot (frozen commit)
- Task matrix
- Prompt templates per arm
- Canonical clue graph and delta patch logs

## Outputs

- run-summary.json
- metrics-by-task.json
- cct-path-metrics.json
- gate-verdict.md

## Gate Enforcement

Run is valid only if:

- schema validation passes
- lossless invariants pass
- CCT suite passes minimum thresholds
