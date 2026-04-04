# Comprehension Circuit Tracing (CCT) Framework

## Purpose

Borrowing from circuit-tracing ideas, validate whether clue-derived reasoning follows the same critical causal paths as source-derived reasoning.

## Core Idea

Treat comprehension as a reasoning circuit over semantic nodes and edges.

- Probe points: symbols, branches, side effects, contracts.
- Activation path: reasoning path used to answer a task.
- Expected path: gold path from source-level analysis.

## Test Modes

1. Path agreement test: overlap between inferred and expected reasoning paths.
2. Causal ablation test: remove key nodes and verify expected degradation.
3. Contradiction injection test: inject false semantic claims and verify rejection.
4. Counterfactual patch test: mutate a branch and test path re-routing.

## Metrics

- Path Precision (PP)
- Path Recall (PR)
- Causal Sensitivity (CS)
- Contradiction Rejection Rate (CRR)
- Path Drift Index (PDI)

## Acceptance Rules

- PP and PR above configured threshold by task family.
- CRR above critical threshold for safety-sensitive tasks.
- No critical causal path loss in delta-updated runs.
