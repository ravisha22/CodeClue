# External Drill-Down Summary

- Batch ID: `batch-20260405-subagents-final`
- Consumer model: `GPT-5.4 Xhigh`
- Judge model: `Gemini 3.1 Pro`
- Judge mode: `independent-cross-family`
- Evidence tier: `cross-model-copilot`

## Aggregate

- Tasks judged: 3
- Mean before fidelity: 0.08
- Mean after fidelity: 0.50
- Mean delta: 0.42
- H5 pass count: 2/3
- H7 pass count: 2/3

## Per-Task

| Task ID | Repo | Family | Before | After | Delta | H5 | H7 | ETRR |
| --- | --- | --- | ---: | ---: | ---: | --- | --- | ---: |
| flask-tf2-001 | flask | TF2 | 0.00 | 0.75 | 0.75 | pass | fail | 0.4616 |
| httpx-tf2-001 | httpx | TF2 | 0.25 | 0.25 | 0.00 | fail | pass | 0.6879 |
| typeorm-tf2-001 | typeorm | TF2 | 0.00 | 0.50 | 0.50 | pass | pass | 0.9989 |
