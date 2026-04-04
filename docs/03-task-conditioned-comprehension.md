# Task-Conditioned Comprehension

## Problem

Different prompts induce different comprehension pathways. A single static summary cannot preserve all task-relevant understanding.

## Strategy

Separate canonical comprehension state from task-conditioned projection.

- Canonical layer: full graph and semantics.
- Projection layer: operation-specific subgraph and constraints.
- Prompt lens: explicit projection policy for task families.

## Operation Families

- OF1 architecture reasoning
- OF2 impact analysis
- OF3 edit-point localization
- OF4 behavior debugging
- OF5 security and compliance reasoning

## Expected Properties

- Projection completeness: no missing required path for the requested operation.
- Projection minimality: irrelevant context bounded but never at cost of correctness.
- Projection traceability: every projected claim links back to canonical anchors.
