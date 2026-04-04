# Projection Fidelity Summary (OF1-OF5)

Evaluation artifacts:

- experiments/reports/of1-fidelity.json
- experiments/reports/of2-fidelity.json
- experiments/reports/of3-fidelity.json
- experiments/reports/of4-fidelity.json
- experiments/reports/of5-fidelity.json

| Family | Gold ID | Passed | Node F1 | Edge F1 | Path Fidelity | Expected Nodes | Observed Nodes | Expected Edges | Observed Edges |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| OF1 | gold-architecture-sample-v1 | True | 1.000000 | 1.000000 | 1.000000 | 5 | 5 | 4 | 4 |
| OF2 | gold-impact-sample-v1 | True | 1.000000 | 1.000000 | 1.000000 | 4 | 4 | 2 | 2 |
| OF3 | gold-edit-sample-v1 | True | 1.000000 | 1.000000 | 1.000000 | 8 | 8 | 11 | 11 |
| OF4 | gold-behavior-sample-v1 | True | 1.000000 | 1.000000 | 1.000000 | 8 | 8 | 11 | 11 |
| OF5 | gold-security-sample-v1 | True | 1.000000 | 1.000000 | 1.000000 | 8 | 8 | 11 | 11 |

## Calibration Note

OF2 precision calibration is complete.

- OF2 edge and node precision are now both 1.000000 after output-edge and node export calibration.
- Next execution focus is the external repository pilot matrix (2-3 repositories).
