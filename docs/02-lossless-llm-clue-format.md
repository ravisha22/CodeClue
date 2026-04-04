# Lossless LLM-Native Clue Format (LCF)

## Design Principle

The canonical clue artifact is optimized for machine interpretation, not human prose readability.

## Canonical Representation

The format is a graph-first semantic package with deterministic source anchoring:

- Node types: module, symbol, control-region, data-contract, side-effect, invariant.
- Edge types: calls, imports, data-flow, control-flow, exception-flow, temporal-order.
- Anchors: file path, byte span, AST path, hash, commit id.
- Semantics: preconditions, postconditions, mutation points, failure modes.
- Confidence: per-node and per-edge confidence with evidence references.

## Serialization Strategy

- Canonical logical model: schema-defined graph document.
- Transport forms: YAML (debug), JSON Lines (pipeline), optional binary (MessagePack/CBOR).
- Round-trip rule: no semantic field may be dropped between transport forms.

## Lossless Criteria

A clue package is lossless only if all of the following hold:

- Every node/edge resolves to source anchor(s).
- Reconstructed operational paths match baseline graph extraction.
- No orphan semantic units remain after serialization-deserialization cycles.
- Delta patches preserve graph connectivity invariants.
