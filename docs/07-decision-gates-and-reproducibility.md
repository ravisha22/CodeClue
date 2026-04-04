# Decision Gates and Reproducibility

## Go/No-Go Gates

- G1 Efficiency: TRR target achieved.
- G2 Fidelity: FS target achieved.
- G3 Delta quality: non-inferiority margin met.
- G4 Drift resilience: floor maintained over sequential updates.
- G5 Safety: contradiction rejection and verification checks pass.

Failure at any mandatory gate blocks production claims.

## Reproducibility Requirements

- Exact repo commit hashes.
- Tokenization scripts and ignore manifests.
- Prompt templates for each arm.
- Raw outputs, parsed metrics, and adjudication logs.
- Deterministic seed and environment manifest.

## Reporting Pack

Every run must publish:

- Pass/fail summary table
- Threshold deltas
- Known anomalies
- Root-cause notes for failed gates
