# Unpoisoned Clue Study Design

## Purpose

This document defines a clean research and implementation plan for testing whether
CodeClue can achieve both of the intended outcomes at the same time:

1. substantial token compression relative to raw-source-first consumption, and
2. high-fidelity code interpretation from the clue artifact alone for the majority of tasks.

The design explicitly separates the canonical internal graph, the evaluation-facing
clue artifact, and the optional drill-down layer so the study no longer conflates
debugging or routing metadata with the clue itself.

## Problem Statement

The currently shipped evaluation path uses projection JSON plus confidence-routing
payload as the clue artifact. That introduces two distortions:

1. token-budget distortion:
   large parts of the prompt are spent on verbose projection/debug/routing fields,
   not on the semantic payload that a consumer model actually needs.
2. capability distortion:
   poor clue-only performance can no longer be attributed cleanly to the clue
   concept, because the tested artifact is not the intended LLM-facing clue view.

The new study must answer a narrower and more defensible question:

Can a deliberately designed LLM-facing clue view, derived from the canonical graph
 but isolated from projection/debug payload, deliver strong clue-only fidelity while
 preserving a large token reduction advantage over raw-source-first inference?

## Target Success Factors

The study is successful only if all four target outcomes are measured directly and
reported separately.

### Compression

- At least 85% token reduction for 70% to 80% of tasks.
- This target must hold across both:
  - small-node tasks, and
  - large-node tasks.

### Clue-Only Sufficiency

- At least 60% to 70% of tasks should reach the accepted fidelity threshold without
  drill-down.

### Drill-Down Dependence

- Drill-down should be the minority path, not the default path.
- The majority of tasks should complete in clue-only mode.

### Post-Drill Value

- For the minority of tasks that require lookup, post-drill fidelity should improve
  materially while total clue-plus-drill context remains well below raw-first cost.

## Core Research Questions

### RQ1: Compression

Can a compact clue view preserve task-relevant semantics while reducing context cost
by more than 85% versus raw-first for most tasks?

### RQ2: Clue-Only Interpretation

Can the clue view alone answer the majority of representative code comprehension
questions with acceptable fidelity?

### RQ3: Selective Lookup

Can confidence be used to route only the difficult minority of tasks into drill-down,
without turning lookup into the default behavior?

### RQ4: Efficient Recovery

When clue-only is insufficient, can drill-down recover fidelity at a favorable total
context cost relative to raw-first?

## Non-Goals

This design does not attempt to eliminate drill-down entirely.

This design does not attempt to prove the canonical graph alone is directly optimal
for LLM consumption.

This design does not treat projection traces, calibration payloads, or debugging
metadata as part of the LLM-facing clue artifact.

## Design Principles

### Principle 1: Artifact Separation

The system must maintain three distinct artifact layers:

1. canonical graph
2. LLM-facing clue view
3. drill-down results

These layers may be derived from one another, but they must not be evaluated as if
they were the same thing.

### Principle 2: Consumer-Centric Serialization

The clue view must optimize for model interpretation and token efficiency, not for
human inspection or internal debugging.

### Principle 3: Confidence as Orchestration, Not Content Flooding

Confidence stays in the system, but the consumer prompt should receive only compact
confidence signals that influence behavior. It should not receive bulky per-node or
per-edge routing payload unless the study explicitly tests such exposure.

### Principle 4: Single-Cause Attribution

Each experiment must isolate one question at a time:

1. clue-only sufficiency,
2. drill-down dependence,
3. post-drill recovery, and
4. compression.

### Principle 5: Benchmark Honesty

Results must be reported both in aggregate and stratified by:

- task family,
- repository,
- projection size band,
- raw-source token band,
- clue-size band, and
- confidence band.

## Proposed Architecture

## Layer 1: Canonical Graph

The canonical graph remains the complete internal semantic representation.

It is allowed to include:

- full nodes and edges,
- source anchors,
- semantic contracts,
- structural metadata,
- confidence inputs,
- calibration features, and
- validation/debug information.

The canonical graph is not the clue artifact.

## Layer 2: Task-Conditioned Projection Trace

The projection trace remains an internal execution artifact used for:

- seed selection,
- candidate narrowing,
- confidence estimation,
- validation metrics,
- policy analysis, and
- experiment debugging.

The projection trace is also not the clue artifact.

## Layer 3: LLM-Facing Clue View

This is the new artifact to be evaluated in clue-only experiments.

It must be produced from the canonical graph and task-conditioned projection, but it
must be serialized separately from both.

### Required properties

The clue view must be:

- compact,
- semantically dense,
- anchored to source,
- task-conditioned,
- easy for an LLM to scan,
- free of projection-debug clutter.

### Required fields per clue packet

Each clue packet should contain only the following top-level blocks:

1. task header
2. compact clue summary
3. compact node table
4. compact relation table
5. compact uncertainty block

### Task header

The task header contains:

- task_id
- repo
- task_family
- operation_family
- question

### Compact clue summary

This is a short synthesized summary of the relevant subsystem behavior.

It should answer, in compressed form:

- what the main execution path is,
- which symbols matter most,
- which files are involved,
- what state transitions or side effects occur,
- what notable conditions or branches matter for the task.

This summary should be concise and machine-oriented, not essay-like.

### Compact node table

Each node entry should include only:

- short node id
- node type
- symbol or module name
- one-line behavioral summary
- file path
- line range
- optional importance rank

Fields that should not appear in the clue view by default:

- full semantic contract dumps
- content hashes
- AST paths
- byte offsets unless needed for tooling
- validation fields
- calibration internals
- repeated nested structures

### Compact relation table

Each relation entry should include only:

- relation type
- source node id
- target node id
- optional brief note when the relation is task-critical

This should preserve the path logic needed for the question while avoiding graph-wide
expansion noise.

### Compact uncertainty block

This block is allowed to contain only compact orchestrative signals:

- overall confidence
- lookup decision hint
- at most 3 short missing-context bullets

This block must not contain:

- per-node confidence arrays
- per-edge confidence arrays
- tool arguments for every low-confidence element
- English rationale paragraphs

## Data Model for the New Clue Artifact

The recommended new clue-view schema is:

```json
{
  "task": {
    "task_id": "flask-tf2-001",
    "repo": "pallets/flask",
    "task_family": "TF2",
    "operation_family": "OF2",
    "question": "..."
  },
  "clue_summary": {
    "system_behavior": [
      "Request enters Flask.wsgi_app and creates a request context.",
      "Request handling flows through full_dispatch_request before finalization.",
      "User exceptions route through handle_user_exception or handle_exception."
    ],
    "key_files": [
      "src/flask/app.py"
    ],
    "key_symbols": [
      "Flask.wsgi_app",
      "Flask.full_dispatch_request",
      "Flask.dispatch_request",
      "Flask.finalize_request"
    ]
  },
  "nodes": [
    {
      "id": "n1",
      "type": "symbol",
      "name": "Flask.wsgi_app",
      "summary": "Top-level request entrypoint that creates context and drives dispatch.",
      "file": "src/flask/app.py",
      "lines": [1566, 1624],
      "importance": 1
    }
  ],
  "relations": [
    {
      "type": "calls",
      "from": "n1",
      "to": "n2",
      "note": "Main request-dispatch path"
    }
  ],
  "uncertainty": {
    "overall_confidence": 0.74,
    "lookup_hint": "targeted_lookup",
    "known_gaps": [
      "Testing client path is not fully covered.",
      "Timeout propagation is not fully resolved."
    ]
  }
}
```

## What Changes in the Codebase

No implementation is performed by this document. This section defines the proposed
code changes required to run the clean study.

### New module: clue renderer

Add a renderer that derives a compact clue view from the projection and canonical graph.

Proposed file:

- `src/codeclue_research/clue_view.py`

Responsibilities:

1. take the existing projection output,
2. select the minimal node and relation subset needed for the task,
3. summarize nodes into one-line behavioral descriptions,
4. compress relation output into a task-salient path view,
5. emit only compact uncertainty signals.

### New serializer modes

Extend the pipeline with explicit output modes:

1. `projection_trace`
2. `clue_view`
3. `drilldown_context`

Proposed changes:

- `src/codeclue_research/operation_projection.py`
- `src/codeclue_research/cli.py`

### New batch-preparation scripts

Add dedicated study scripts that do not reuse the current poisoned prompt builders.

Proposed scripts:

- `experiments/runs/prepare_clean_clue_batch.py`
- `experiments/runs/build_clean_clue_judge_bundle.py`
- `experiments/runs/collate_clean_clue_results.py`

### New prompt family separation

Add three explicit consumer prompt types:

1. raw-first
2. clue-only
3. clue-plus-drill-down

The clue-only prompt must consume only the clue view artifact.

The clue-plus-drill-down prompt must start from the clue view and then append only
the actual tool outputs used during that run.

### New guardrail checks

Add a validation layer that fails clue generation if forbidden fields leak into the
consumer artifact.

Examples of forbidden leaked fields:

- `per_node_confidence`
- `per_edge_confidence`
- `reasoning_path`
- `validation`
- `policy`
- `suggested_actions`
- `rationale`

## End-to-End Experimental Workflow

## Phase A: Artifact Purification

Goal:

Produce a clean clue artifact and prove that it is structurally isolated from the
projection/debug layer.

Steps:

1. Generate canonical graph.
2. Generate task-conditioned projection trace.
3. Render compact clue view.
4. Run clue-purity validator.
5. Save all three artifacts separately.

Outputs:

- graph artifact
- projection trace artifact
- clue-view artifact
- purity validation report

## Phase B: Clue-Only Benchmark

Goal:

Measure clue-only fidelity without allowing drill-down.

Execution:

1. Consumer receives only:
   - question
   - clue-view artifact
2. Consumer answers the question.
3. Independent judge scores answer against ground truth.

Metrics:

- clue-only fidelity score
- clue sufficiency yes/no
- missing-information categories
- clue token count
- compression ratio vs raw-first

## Phase C: Confidence-Gated Drill-Down Benchmark

Goal:

Measure whether only the minority of difficult tasks require lookup, and whether
lookup materially improves fidelity.

Execution:

1. Start from the same clue-view artifact.
2. Permit MCP drill-down only after clue-only answer is recorded.
3. Capture exact tools used and total drill-down context size.
4. Score the revised answer independently.

Metrics:

- post-drill fidelity
- fidelity uplift over clue-only
- tool count
- lookup path frequency
- total context cost vs raw-first

## Phase D: Cross-Size Stress Validation

Goal:

Verify that the success criteria hold for both sparse/small and dense/large tasks.

Task bands:

1. small-node projections
2. medium-node projections
3. large-node projections

Raw-source bands:

1. small repo slices
2. medium repo slices
3. very large repo slices

This phase prevents the study from passing only because large raw baselines make the
 compression ratio look favorable.

## Benchmark and Sampling Strategy

## Task set

Use the current task-family framework TF1 to TF5 and expand only after the clean
artifact path is stable.

Recommended first clean benchmark:

- existing 23 tasks for direct comparability,
- then scale to 50 tasks,
- then scale to the preregistered larger benchmark.

## Required stratification

Every analysis should report results by:

- TF1 architecture
- TF2 impact analysis
- TF3 edit-point localization
- TF4 behavior/debugging
- TF5 security/compliance

And also by:

- small vs large clue packet size,
- small vs large raw-source size,
- high vs medium vs low confidence.

## Quantitative Metrics

## Compression metrics

### Clue Compression Ratio

`CCR = 1 - (clue_tokens / raw_first_tokens)`

Primary threshold:

- `CCR >= 0.85`

### Total Recovery Compression Ratio

`TRCR = 1 - ((clue_tokens + drilldown_tokens) / raw_first_tokens)`

This is the real efficiency metric for tasks that require lookup.

## Fidelity metrics

### Clue-Only Fidelity Score

Independent judge score for the clue-only answer.

### Post-Drill Fidelity Score

Independent judge score after drill-down evidence is allowed.

### Fidelity Uplift

`FU = post_drill_fs - clue_only_fs`

Primary threshold for valuable lookup:

- `FU >= 0.10`

## Dependence metrics

### Drill-Down Rate

`DDR = tasks_using_drilldown / total_tasks`

Success interpretation:

- lookup should be the minority path,
- target `DDR <= 0.40`

### Default-Free Completion Rate

`DFCR = tasks_completed_without_drilldown / total_tasks`

Success interpretation:

- target `DFCR >= 0.60`

## Token-budget metrics

### Post-Drill Efficiency Retention

`PER = 1 - ((clue_tokens + drilldown_tokens) / raw_first_tokens)`

Recommended threshold:

- `PER >= 0.50` for tasks that needed lookup,
- stretch target `PER >= 0.65`

## Acceptance Criteria

The study passes only if all of the following hold:

1. at least 70% to 80% of tasks achieve `CCR >= 0.85`
2. at least 60% to 70% of tasks achieve accepted clue-only fidelity without lookup
3. `DDR <= 0.40`
4. lookup tasks show `FU >= 0.10` on average
5. lookup tasks remain materially cheaper than raw-first overall
6. results do not collapse when stratified by small-node and large-node bands

## Automated Testing Plan

Automation should exist at four levels.

## Level 1: Unit tests

Purpose:

Ensure the clue renderer emits only allowed structures and preserves required meaning.

Test areas:

1. clue schema generation
2. forbidden field exclusion
3. node summarization correctness
4. relation compaction correctness
5. uncertainty block size limits

Proposed test files:

- `tests/clue_view/test_schema.py`
- `tests/clue_view/test_forbidden_fields.py`
- `tests/clue_view/test_summary_rendering.py`
- `tests/clue_view/test_relation_compaction.py`

Expected results:

- all generated clue artifacts validate against schema
- no forbidden field leakage
- summary fields remain under configured length budgets

## Level 2: Integration tests

Purpose:

Ensure end-to-end generation from graph to clue artifact behaves correctly.

Test areas:

1. graph -> projection trace -> clue view pipeline
2. clue-view prompt construction
3. clue-only batch generation
4. clue-plus-drill-down batch generation
5. token-count reporting consistency

Proposed test files:

- `tests/harness/test_clean_clue_batch.py`
- `tests/harness/test_clean_prompt_generation.py`
- `tests/harness/test_token_metrics.py`

Expected results:

- same task input always produces deterministic clue artifact under fixed seed
- clue token count remains smaller than projection-trace count for all fixtures
- clue-only prompt contains only allowed sections

## Level 3: Regression tests

Purpose:

Prevent the original poisoning failure from re-entering the evaluation path.

Test areas:

1. projection fields must not leak into clue prompts
2. confidence arrays must not leak into clue prompts
3. reasoning paths must not leak into clue prompts
4. suggested actions must not leak into clue-only prompts

Proposed test files:

- `tests/regression/test_clue_prompt_purity.py`
- `tests/regression/test_projection_is_not_clue.py`

Expected results:

- any reintroduction of debug/projection payload causes test failure

## Level 4: Benchmark validation tests

Purpose:

Verify the research thresholds continuously as the clue renderer evolves.

Test areas:

1. compression threshold report
2. clue-only fidelity threshold report
3. drill-down minority-path report
4. post-drill uplift report

Proposed harness artifacts:

- `experiments/reports/clean-clue-summary.json`
- `experiments/reports/clean-clue-summary.md`
- `experiments/reports/clean-clue-stratified.json`

Expected results:

- benchmark report is reproducible from saved artifacts
- failure modes are stratified and attributable

## Minimal Manual Steps

The study should be automated as far as possible. The user should only be required
for the following minimal steps:

1. run the prepared external consumer prompts if a hosted model does not have an API
   path available in the repo environment
2. run the independent judge prompt when needed
3. confirm any external-model outputs are saved into the expected answer files

Everything else should be automated:

1. artifact generation
2. prompt generation
3. tool-run capture
4. token accounting
5. result collation
6. summary table generation

## Expected Results by Phase

## Phase 1: Clean artifact prototype

Expected result:

- clue artifacts become dramatically smaller than current projection packets
- clue purity tests pass
- current poisoned clue packets are replaced by compact clue artifacts

Expected quantitative effect:

- 60% to 85% size reduction versus current clue packets alone

## Phase 2: Clue-only pilot on existing 23 tasks

Expected result:

- clue-only mean fidelity should improve over the current poisoned baseline on tasks
  where verbosity and routing clutter were the main problem
- some hard behavioral tasks will still fail without lookup

Expected quantitative effect:

- clue-only pass rate should move materially upward from the current low-confidence
  pilot baseline
- not all families will improve equally

## Phase 3: Confidence-gated lookup pilot

Expected result:

- fewer tasks should require drill-down than in the current workflow
- lookup should concentrate on the hard tail

Expected quantitative effect:

- `DDR` should drop below current behavior
- post-drill uplift should remain positive on the difficult subset

## Phase 4: Threshold pursuit

Expected result:

- repeated iteration on clue renderer and summarization policy should make the study
  capable of reaching the stated thresholds

Most likely order of difficulty:

1. easiest target: compression
2. next: post-drill value
3. harder: drill-down minority-path
4. hardest: clue-only sufficiency across TF2 and TF4 hard tasks

## Risks and Mitigations

## Risk 1: Over-compression destroys behavior

Mitigation:

- preserve one-line behavioral summaries per node
- keep task-salient relation notes
- test by family, not only aggregate

## Risk 2: Clue summaries become human prose rather than machine-helpful structure

Mitigation:

- cap summary lengths
- keep semi-structured lists
- validate with prompt-purity and token-budget tests

## Risk 3: Compression looks good only because raw baselines are huge

Mitigation:

- report by per-task ratios
- stratify by small and large raw-source bands

## Risk 4: Lookup remains default because clue renderer omits causal semantics

Mitigation:

- improve behavior summaries for TF2 and TF4 tasks first
- maintain gap taxonomy from clue-only failures

## Risk 5: Confidence gating becomes over-conservative

Mitigation:

- evaluate lookup hint separately from clue fidelity
- calibrate threshold on holdout tasks

## Implementation Sequence

Recommended build order:

1. implement compact clue renderer
2. add clue-purity validator
3. add clean prompt builders for raw-first, clue-only, and clue-plus-drill-down
4. add batch preparation and collation scripts
5. run existing 23 tasks for direct before/after comparison
6. tune clue summarization policy on the failure taxonomy
7. scale to 50 tasks

## Deliverables

The execution should produce the following deliverables:

1. this design document
2. compact clue-view schema and renderer
3. clean benchmark prompt family
4. automated clean-study batch scripts
5. purity regression tests
6. threshold summary reports
7. paper-ready evidence pack

## Final Position

This design is intended to test the real hypothesis that matters:

not whether the current projection-debug artifact is sufficient, but whether a
properly designed LLM-facing clue artifact can become the primary source of code
interpretation for most tasks while preserving a major token-efficiency advantage.

If this design fails after clean isolation, then the conclusion that clue-only is
insufficient becomes much stronger. If it succeeds, the current negative result can
be attributed correctly to artifact poisoning rather than to the core clue idea.
