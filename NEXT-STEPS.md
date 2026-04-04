# Next Steps

## Completed

1. Canonical graph extractor and source-anchor validator.
2. Strict round-trip checks across JSON and YAML.
3. Delta updater with invariant checks and proof report.
4. Multi-language extraction frontends (Python, TypeScript, Go).
5. CCT probe runner and unified pilot harness.
6. OF1-OF5 operation projection engine with prompt-profile routing.
7. Gold-path fidelity evaluator integrated into CLI and pilot run.

## Continued Plan (2026-03-28)

### Sprint 1: Gold-Path Coverage Expansion (Immediate)

1. Add missing gold fixtures for OF1, OF3, OF4, and OF5 under `tests/fixtures/`.
2. Keep one fixture schema per task with:
	- `gold_id`, `operation_family`, `gold_path.nodes`, `gold_path.edges`, `thresholds`.
3. Add at least 2 representative tasks per missing family before external repo pilots.
4. Generate family-level fidelity reports under `experiments/reports/`.

Definition of done:

1. All OF1-OF5 have at least one passing gold-path evaluation artifact.
2. Reports exist for each family and are linked in docs.

### Sprint 2: Projection Precision Calibration (Immediate)

1. Calibrate `src/codeclue_research/operation_projection.py` to reduce structural edge over-selection.
2. Add policy controls to separate structural (`contains`) and operational (`calls`) edge retention.
3. Re-run OF1-OF5 comparison and fidelity reports after each calibration change.
4. Track threshold movement in `experiments/reports/of1-of5-comparison.md`.

Current calibration target (based on latest OF2 report):

1. Improve edge precision from 0.333333 to >= 0.50.
2. Keep edge recall at >= 0.90.
3. Keep path_fidelity >= 0.60.

### Sprint 3: CCT Adversarial and Counterfactual Suite Expansion

1. Add new probe fixtures in `tests/fixtures/` for:
	- contradiction injection families,
	- counterfactual reroute cases,
	- multi-ablation sensitivity checks.
2. Validate that `src/codeclue_research/cct.py` metrics remain stable under expanded probe formats.
3. Run CCT through `run-pilot` and capture outputs in `experiments/runs/` and `experiments/reports/`.

Definition of done:

1. At least 1 new adversarial probe and 1 new counterfactual probe executed successfully.
2. CRR and PR thresholds pass for new probes.

### Sprint 4: External Repository Pilot Matrix (2-3 repos)

1. Select 2-3 external repositories spanning Python/TypeScript/Go mix.
2. Execute pilot matrix per repo:
	- extract,
	- validate,
	- roundtrip,
	- integrity,
	- OF projection,
	- fidelity,
	- optional CCT.
3. Save reproducibility metadata for each run:
	- repo URL,
	- commit hash,
	- language selector,
	- prompt profile,
	- gold fixture version.

Definition of done:

1. All selected repos have run summaries and fidelity reports.
2. Threshold calibrations are updated from real-repo outcomes.

### Sprint 5: Benchmark Scale-Up (500k-700k tokens)

1. Build preregistered benchmark set per `docs/06-experimental-protocol.md`.
2. Enforce decision gates from `docs/07-decision-gates-and-reproducibility.md`.
3. Execute arms A/B/C with task-family stratification.
4. Publish reporting pack for each run:
	- pass/fail summary,
	- threshold deltas,
	- anomaly notes,
	- root-cause notes.

Definition of done:

1. Minimum benchmark coverage criteria are met.
2. Gate outcomes are reproducible from saved artifacts.

## Next Execution Block (Suggested Order)

1. Create OF1/OF3/OF4/OF5 gold fixtures.
2. Run baseline batch comparison and fidelity reports.
3. Implement first projection edge-pruning calibration pass.
4. Re-run OF2 fidelity and compare edge precision delta.
5. Add first adversarial CCT probe and execute via `run-pilot`.
6. Begin external repo pilot matrix once fixture and calibration gates are green.

## Execution Update (2026-03-28)

Completed now:

1. Added missing OF1/OF3/OF4/OF5 gold fixtures in `tests/fixtures/`.
2. Generated OF1-OF5 family fidelity artifacts in `experiments/reports/`.
3. Published consolidated matrix summary in `experiments/reports/fidelity-summary.md`.
4. Calibrated OF2 edge export policy and raised OF2 edge precision from 0.333333 to 1.000000.
5. Calibrated OF2 exported node selection and raised OF2 node precision from 0.800000 to 1.000000.
6. Added and executed adversarial and counterfactual CCT probes with passing metrics.

Active next target:

1. External repository pilot matrix (2-3 repositories) with reproducibility metadata and calibrated thresholds.
2. Use preregistered replay seed manifest in `experiments/reports/pr-replay-set-v1.json` for deterministic PR-level replays.
3. Expand from seed set to full 12-repository benchmark protocol once Sprint 4 gates are green.

## Continued Plan (2026-04-01): Confidence-Gated Tool Calling

### Sprint 6: Confidence Scoring Infrastructure

1. Extend `src/codeclue_research/models.py` with per-node `suggested_actions` list and code density indicator fields.
2. Add confidence estimation logic to `src/codeclue_research/operation_projection.py`:
	- Compute `p_context_miss` from unresolved edge count / total edges in projection.
	- Compute `p_dependency_miss` from dependency closure coverage ratio.
	- Detect code density indicators (dynamic dispatch, reflection, high fan-out, cross-file span ratio).
	- Emit `confidence_overall` and `lookup_decision_hint` per projection.
3. Emit `suggested_actions` on nodes/edges with confidence below task-family threshold.
4. Persist confidence block in projection trace output JSON.

Definition of done:

1. `project` CLI command emits confidence block and suggested_actions in output.
2. Existing OF1-OF5 fidelity tests still pass (no regression).
3. At least one projection on sample code produces a node with confidence < 0.85 and a suggested action.

### Sprint 7: Tool Registry and Invocation Tracing

1. Implement typed tool registry with the 5 tools defined in PRD Section 6.4.3:
	- `code_slice`, `resolve_dependency`, `check_freshness`, `expand_projection`, `fetch_contract`.
2. Each tool has input/output schema validation.
3. Add invocation trace logger: tool name, input args, output hash, source anchor binding, triggering confidence score.
4. Integrate tool invocation into `run-pilot` harness with `--enable-drill-down` flag.
5. Persist invocation traces in run artifacts alongside projection traces.
6. Implement per-session tool call budget per operation family (OF1:5, OF2:15, OF3:10, OF4:20, OF5:30).
7. Budget exhaustion emits escalation event with unresolved low-confidence node list.

Definition of done:

1. Each tool is callable from CLI and harness.
2. Invocation traces are persisted and contain all required fields.
3. Tool outputs do NOT mutate the canonical clue graph.
4. Budget is enforced; exhaustion logs escalation event.

### Sprint 8: Confidence Calibration Dataset (Lane A Prerequisite)

Note: R0/R1 runs use Layer 1 structural confidence only (bootstrap phase — breaks circular calibration dependency). This sprint uses R0/R1 labeled outcome data to train calibration models.

1. Execute OF1-OF5 projections across external repo pilot set (Sprint 4 outputs).
2. Label each projection node/edge with binary outcomes: context_miss, dependency_miss, hallucination_event.
3. Build training/holdout/test splits for confidence estimator calibration.
4. Train estimators and validate per Appendix A.5 protocol (ECE <= 0.05, Brier <= 0.18).
5. Build per-model calibration profiles per Appendix D.2.
6. Publish calibration report with reliability diagrams.

Definition of done:

1. Calibration gates pass on test split.
2. Per-operation-family confidence baselines are published.
3. Per-model calibration profiles saved to `.codeclue/calibration/`.
4. Calibration staleness detector implemented (fallback to structural-only on version mismatch).

### Sprint 9: Lane A Benchmark Execution with Confidence

1. Execute full Lane A benchmark matrix (Arms A/B/C) on replay set with confidence-enabled artifacts.
2. Measure H5: on tasks where static confidence < 0.85, does drill-down raise fidelity by >= 0.10 at cost < 50% of raw baseline?
3. Measure H7: ETRR >= 0.65 across tasks (clue + drill-down tokens combined).
4. Measure SAP: suggested action precision >= 0.60 on 30% sample of actions.
5. Publish Lane A report with gate verdicts for G1-G6, G9, G10.

Definition of done:

1. Gates G1-G6, G9, G10 have published pass/fail verdicts.
2. H5 and H7 have published confidence intervals.
3. SAP report published.

### Sprint 10: Lane B Ecological Validity (Phase R5)

1. Collect LLM tool invocation traces from confidence-gated runs on external repos.
2. Compute IFT Scent Alignment: correlation between confidence scores and IFT-predicted information scent (target >= 0.60).
3. Compute Callback Distribution Agreement: KL divergence vs Sillito reference distribution (target KL < 0.15).
4. Compute SWE-bench Drill-Down Precision on SWE-bench tasks (target >= 0.50).
5. Compute self-consistency score: run each task 5 times, measure tool call stability (target >= 0.70).
6. Publish Lane A / Lane B cross-comparison report.

Definition of done:

1. Gate G7 has published pass/fail verdict.
2. Gap taxonomy is published with frequency distribution across code density levels.
3. Self-consistency >= 0.70 across task families.

### Sprint 11: Generation Quality Validation (Phase R7)

1. Test H6: run structured contract generation (Appendix D.1, Tier 2) with at least 2 frontier LLMs and 1 strong-open model.
2. Measure schema validation pass rate per module across benchmark repos.
3. Identify module patterns where Tier 2 generation fails (target: pass rate >= 90%).
4. If pass rate < 90%, document capability boundary and Tier 1 fallback coverage.
5. Publish G9 gate verdict.

Definition of done:

1. Gate G9 has published pass/fail verdict.
2. Per-model generation pass rates published.

### Sprint 12: Cross-Model Interoperability (Phase R6)

1. Execute cross-model fidelity benchmark (Appendix D.3): 3 generators x 3 consumers.
2. Measure per-consumer variance across generators (target: max pairwise FS delta <= 0.05).
3. Measure drill-down path agreement across consumers on same clue (target: >= 70% node overlap).
4. Publish G8 gate verdict and cross-model fidelity matrix.

Definition of done:

1. Gate G8 has published pass/fail verdict.
2. Cross-model matrix and drill-down path agreement report published.
