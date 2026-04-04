# Session Handoff: CodeClue Research Scaffold

Date: 2026-03-28
Status: Ready for next execution session

## 1. What Is Implemented

Completed phases:

1. Canonical clue graph extraction with source anchors.
2. Invariant validation and graph integrity checks.
3. Round-trip lossless checks for JSON and YAML.
4. Delta patch apply with proof reporting.
5. Multi-language extraction frontends (Python, TypeScript, Go).
6. OF1-OF5 operation projection engine with prompt-profile routing.
7. Gold-path fidelity evaluation (node and edge precision/recall/F1 and path_fidelity).
8. Unified pilot runner with optional CCT and fidelity gating.

## 2. Latest Verified Outputs

Key reports:

- experiments/reports/of1-of5-comparison.md
- experiments/reports/of2-fidelity.json
- experiments/reports/fidelity-summary.md
- experiments/runs/pilot-fidelity/run-summary.json

Latest observed highlights:

- OF1-OF5 tuned projection report shows strong local coverage and precision.
- OF2 fidelity currently passes configured thresholds.
- Fidelity detail indicates extra structural edges remain; edge precision is lower than node precision.

## 3. Known Gaps and Risks

1. Gold-path fidelity coverage is limited (currently sample-focused; not yet broad across OF1-OF5 task sets).
2. CCT suites are still basic; adversarial and counterfactual depth is not yet complete.
3. External validation on 2-3 real repositories has not yet been executed.
4. 500k-700k token benchmark protocol is not yet run.

## 4. Immediate Next Session Plan

Priority order:

1. Expand gold-path fixtures for OF1, OF3, OF4, OF5.
2. Add edge-pruning strategy in projection output to reduce structural false positives and improve edge precision.
3. Add CCT adversarial probes (contradiction and counterfactual families).
4. Run pilot matrix on 2-3 external repositories.

## 5. Resume Commands

Run from repository root: C:/Users/ranandag/Documents/VSCodeProjects/CodeClue-Research-Scaffold

Install or refresh local package:

```bash
python -m pip install -e .
```

Generate multi-language graph:

```bash
python -m codeclue_research extract --repo-root . --language auto --output experiments/runs/session-resume/graph.json --commit-id session-resume
```

Run full pilot with projection and fidelity:

```bash
python -m codeclue_research run-pilot --repo-root . --run-dir experiments/runs/session-resume --commit-id session-resume --language auto --operation-family OF2 --prompt-profile-file tests/fixtures/prompt_profile_impact.yaml --gold-file tests/fixtures/gold_path_impact.yaml --probe-file tests/fixtures/sample_probe.yaml --trace-file tests/fixtures/sample_trace.jsonl
```

Run standalone fidelity evaluation:

```bash
python -m codeclue_research fidelity-eval --projection-file experiments/runs/batch-of/of2.json --gold-file tests/fixtures/gold_path_impact.yaml --output-file experiments/reports/of2-fidelity.json
```

## 6. Definition of Done for Next Session

Session can be considered successful if all are true:

1. At least one new gold-path fixture is added for each missing operation family.
2. Edge precision improves on the representative OF2 gold-path evaluation without unacceptable recall loss.
3. At least one new CCT adversarial probe is added and executed.
4. Updated report artifacts are saved under experiments/reports and linked from docs.

## 7. File Map for Fast Orientation

Core code:

- src/codeclue_research/extractor.py
- src/codeclue_research/operation_projection.py
- src/codeclue_research/fidelity.py
- src/codeclue_research/cct.py
- src/codeclue_research/harness.py
- src/codeclue_research/cli.py

Core docs:

- docs/08-phase1-implementation.md
- docs/09-phase2-4-execution.md
- docs/10-operation-projection.md
- docs/11-fidelity-evaluation.md
- NEXT-STEPS.md

## 8. Notes for the Next Operator

1. Use run-pilot whenever possible so artifacts are generated consistently.
2. Treat path_recall_global as compression/context indicator, not family-level fidelity.
3. Use gold-path metrics as primary acceptance criteria for projection quality.
