# CodeClue Research Scaffold

This workspace is a dedicated research environment for building and validating a lossless, LLM-native code comprehension representation.

## Primary Objective

Design and validate a clue representation that:

- Preserves task-dependent comprehension, not just static interpretation.
- Supports multiple operations and prompt regimes without comprehension collapse.
- Optimizes for LLM interpretability and comprehension preservation over human readability.
- Maintains lossless traceability back to source code spans and execution-relevant paths.
- Supports delta inference without introducing semantic gaps, broken paths, or whitespace-induced ambiguity.
- Uses graph-aware analysis where needed to preserve structural and operational semantics.
- Includes a verification framework inspired by circuit tracing to test interpretation accuracy.

## Workspace Layout

- `source/`: copied baseline PRD and source artifacts.
- `docs/`: topic-by-topic research specification scaffold.
- `scaffold/schemas/`: clue format and operation trace schemas.
- `scaffold/prompts/`: prompts for study arms and operation conditioning.
- `scaffold/tasks/`: task-family matrix and benchmark tasks.
- `tests/cct/`: Comprehension Circuit Tracing framework artifacts.
- `tests/harness/`: execution and evaluation harness specification.
- `experiments/`: run plans and result templates.

## Phase Status

Completed through Phase 4:

1. Phase 1: canonical graph extraction, invariant validation, round-trip checks, CCT probe runner.
2. Phase 2: graph-theoretic integrity analysis and delta patch application with no-gap and connectivity proofs.
3. Phase 3: multi-language extraction support (Python, TypeScript, Go) under one canonical schema.
4. Phase 4: unified pilot runner for extract, validate, roundtrip, integrity, and optional CCT execution.

Completed in current deployment extension:

1. Phase 5: OF1-OF5 operation projection engine with prompt-profile routing and projection trace output.
2. Phase 6: gold-path fidelity evaluation with node and edge F1 based pass/fail thresholds.

Execution runbooks:

- `docs/08-phase1-implementation.md`
- `docs/09-phase2-4-execution.md`
- `docs/10-operation-projection.md`
- `docs/11-fidelity-evaluation.md`
- `docs/HANDOFF-NEXT-SESSION.md`

## Remaining Research Execution

1. Add richer CCT suites (counterfactual reroutes, adversarial contradiction sets, and stress probes).
2. Expand fidelity gold-path suite across OF1-OF5 with multiple tasks per family.
3. Execute calibrated pilot matrix on 2-3 external repositories.
4. Scale to benchmark protocol for 500k-700k token repositories with preregistered decision gates.
