# Delta Inference and Graph Integrity

## Objective

Infer only changed sections while preserving full operational comprehension.

## Delta Update Contract

Input:

- Previous canonical clue graph C_n
- Repository diff D_n_to_n1
- Optional baseline graph extraction G_n1_full for audit mode

Output:

- Updated clue graph C_n1
- Patch log P_n_to_n1 with semantic change rationale

## Required Invariants

- Connectivity invariant: required operational paths remain connected.
- Anchor invariant: updated units maintain valid source anchors.
- No-gap invariant: no unresolved placeholder nodes in executable paths.
- Equivalence invariant: recomputed task projections are non-inferior to full rebuild.

## Graph Analysis Hooks

- SCC checks for cyclic dependency stability.
- Dominator and post-dominator checks for control-path continuity.
- Data-flow slice comparison for mutated symbols.
- Impact frontier extraction to bound safe incremental updates.

## Reset Policy

Trigger full regeneration when:

- Invariant failures exceed threshold.
- Drift slope crosses guard band.
- High-churn region crosses complexity cap.
