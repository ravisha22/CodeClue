# Research Charter

## Thesis

Code comprehension should be a persistent, verifiable artifact that preserves operational meaning across tasks, prompts, and incremental code evolution.

## Core Questions

1. Can we encode code understanding in a format that is natively interpretable by LLMs while remaining lossless to source behavior?
2. Can prompt- or task-conditioned views be generated from a single canonical clue representation without semantic drift?
3. Can delta updates preserve full-path comprehension under repeated changes?

## Non-Negotiable Properties

- Lossless source anchoring for every semantic unit.
- Task-dependent comprehension views derivable without hallucinated links.
- Deterministic validation of clue to source consistency.
- Explicit uncertainty and contradiction channels.

## Scope of This Workspace

This workspace is implementation-oriented. It converts the research boundary document into runnable schemas, prompts, test harnesses, and verification methods.
