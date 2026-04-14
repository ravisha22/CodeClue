# Three-Task External Drill-Down Pilot: Results and Token Efficiency

## Setup

- Consumer model: `GPT-5.4 Xhigh`
- Consumer execution mode: subagent-automated before/after reasoning
- Judge model: `Gemini 3.1 Pro`
- Judge mode: `independent-cross-family`
- Evidence tier: `cross-model-copilot`
- Task set: `flask-tf2-001`, `httpx-tf2-001`, `typeorm-tf2-001`

## Main result

This pilot provides externally judged evidence that confidence-gated drill-down can improve answer quality on low-confidence tasks, but the effect is mixed across repositories.

Aggregate judged outcome:

- Tasks judged: `3`
- Mean clue-only fidelity: `0.08`
- Mean post-drill fidelity: `0.50`
- Mean uplift: `+0.42`
- H5 pass count: `2/3`
- H7 pass count: `2/3`

Interpretation:

- The full clue -> drill-down -> revised-answer loop now has pilot external evidence.
- The clue file alone does **not** meet the intended quality bar on these low-confidence tasks.
- Drill-down improves quality in some cases, but not reliably enough yet to support broad benchmark-wide claims.

## Judged per-task results

| Task ID | Repo | Family | Before FS | After FS | Delta | H5 | H7 | ETRR | Judge summary |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | ---: | --- |
| `flask-tf2-001` | Flask | TF2 | 0.00 | 0.75 | 0.75 | pass | fail | 0.4616 | Drill-down recovered the core request lifecycle, but still missed testing-client coverage. |
| `httpx-tf2-001` | httpx | TF2 | 0.25 | 0.25 | 0.00 | fail | pass | 0.6879 | Drill-down did not expose enough timeout usage closure to improve the answer. |
| `typeorm-tf2-001` | TypeORM | TF2 | 0.00 | 0.50 | 0.50 | pass | pass | 0.9989 | Drill-down surfaced some relevant consumers, but still missed major subsystems. |

## Token-efficiency framing

These token counts are **estimated context-size proxies**, not provider-native tokenizer counts. The current measurement uses serialized byte length divided by 4 for clue size, tool output size, and raw-source size.

This is good enough for comparative efficiency analysis, but it should be described honestly as an approximation.

### Per-task token usage

| Task ID | Raw code estimate | Clue-only | Full drill-down extra | Clue + drill-down total | Relative total vs raw |
| --- | ---: | ---: | ---: | ---: | ---: |
| `flask-tf2-001` | 143,132 | 32,923 | 44,139 | 77,062 | 53.8% of raw |
| `httpx-tf2-001` | 142,484 | 9,834 | 34,631 | 44,465 | 31.2% of raw |
| `typeorm-tf2-001` | 2,559,461 | 474 | 2,294 | 2,768 | 0.1% of raw |

### Batch-level token totals

- Total raw-code-first estimate: `2,845,077`
- Total clue-only estimate: `43,231` (`1.52%` of raw)
- Total incremental drill-down estimate: `81,064`
- Total clue + drill-down estimate: `124,295` (`4.37%` of raw)

This aggregate ratio is directionally useful, but it is heavily influenced by the very large TypeORM raw-source baseline. The per-task view is therefore the more honest picture of practical behavior.

### Per-task drill-down cost by tool

| Task ID | `resolve_dependency` | `code_slice` | Total drill-down |
| --- | ---: | ---: | ---: |
| `flask-tf2-001` | 33,792 | 10,347 | 44,139 |
| `httpx-tf2-001` | 24,713 | 9,918 | 34,631 |
| `typeorm-tf2-001` | 1,263 | 1,031 | 2,294 |

## Practical conclusion on efficiency

1. `code_slice` is **not** the main source of drill-down cost in this pilot. `resolve_dependency` dominated token spend on the expensive tasks.
2. The efficiency story is therefore not simply "clue + a few code slices". It is really "clue + graph expansion + targeted source slices".
3. The pipeline can still be substantially cheaper than raw-source-first inference, but the margin depends heavily on the task and the amount of dependency expansion required.
4. The current Flask result is the warning sign: quality improved strongly, but total context still grew to more than half of raw-source size.
5. The current TypeORM result is the positive extreme: both quality uplift and efficiency held, but the clue itself was tiny because the projection was extremely sparse.

## What this means for the study

- If the claim is "clue-only artifacts are generally sufficient on low-confidence impact-analysis tasks," this pilot does **not** support that claim.
- If the claim is "confidence-gated drill-down can improve fidelity while often remaining more efficient than raw-source-first inference," this pilot provides **partial** support.
- If the claim is "the current clue format is already token-optimal for LLM use," this pilot does **not** establish that. In fact, the large `resolve_dependency` payloads suggest the current format may still be too verbose or too graph-heavy for practical LLM consumption.

## Linked artifacts

- `external-drilldown-summary.json`
- `external-drilldown-summary.md`
- `subagent-execution-summary.md`
- `judge-bundle.result.json`
- Per-task `drilldown-tool-results.json`
