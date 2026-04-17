# CodeClue Canonical Status

This document is the single source of truth for current project status.

## Current Result Set

- **Artifact version:** MRLF v2.5
- **Blind evaluation:** **86/168 = 51.2%**
- **By family:** structural **29/56 = 51.8%**, relational **34/56 = 60.7%**, mechanistic **23/56 = 41.1%**
- **Best blind repos:** zod **83.3%**, requests **70.8%**, echo **58.3%**
- **Drill-down lift:** mechanistic **22.9% → 47.9%** on the measured slice
- **Cross-model note:** Sonnet 4.6 improved **50.0% → 81.3%** on the 8-task subset with the reasoning scaffold

## Authoritative Documents

1. `paper/codeclue-paper-v25.md` — latest narrative summary and tables
2. `experiments/runs/blind-eval/responses/v25/blind-scoring.md` — authoritative task-by-task v2.5 blind scores
3. `source/CodeClue-PRD-v0.7.0-generalization.md` — design/specification, now updated to v0.8.0 content
4. `docs/REASONING-SCAFFOLD.md` — canonical scaffold text and token-cost notes
5. `docs/OPEN-ISSUES-PLAN.md` — prioritized remaining work

## Operational Guidance

- Treat this file as the current status snapshot.
- Treat the documents above as the only sources for claims, numbers, and next-step planning.
- If a handoff doc disagrees with this file, the handoff is historical unless explicitly superseded here.

## Historical Handoffs

The following remain useful as archives only:

- `docs/HANDOFF-MCP-PLAN.md`
- `docs/HANDOFF-NEXT-SESSION.md`
- `docs/HANDOFF-SESSION-20260406.md`
- `docs/HANDOFF-SESSION-20260407.md`
- `docs/HANDOFF-SESSION-20260414.md`
- `docs/HANDOFF-SESSION-20260414-v2.md`
- `docs/HANDOFF-SESSION-20260415.md`
