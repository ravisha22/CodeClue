# External Drill-Down Runbook

This packet is prepared for task `nest-tf2-001`.

## What you are proving

Show that an external consumer model gives a better answer after using CodeClue MCP drill-down than it gives from the clue alone.

## Files in this packet

- `task.json`: task metadata
- `projection-snippet.json`: clue projection used for the experiment
- `consumer-pre.prompt.md`: paste into the consumer model for the BEFORE pass
- `consumer-post.prompt.md`: paste into the consumer model for the AFTER pass
- `judge.prompt.md`: paste into the independent judge after inserting both answers
- `result-template.json`: fill in the final measured result
- `server-command.txt`: exact MCP server command

## Step 1: Start the MCP server

Run this in the workspace root:

```powershell
.\.venv\Scripts\codeclue-mcp.exe --graph-path experiments/runs/v2-lane-a-nest/graph.json --repo-root experiments/external-repos/nest
```

## Step 2: BEFORE pass

- Open your external consumer model.
- Paste `consumer-pre.prompt.md`.
- Save the full answer into `answers/pre-answer.md`.

## Step 3: AFTER pass

- Connect the same consumer model to the running MCP server.
- Paste `consumer-post.prompt.md`.
- Allow it to use MCP tools.
- Save the full answer into `answers/post-answer.md`.

## Step 4: Judge

- Open a different model family as judge.
- Open `judge.prompt.md`.
- Replace the BEFORE and AFTER placeholders with the saved answers.
- Save the result into `answers/judge-result.json`.

## Step 5: Fill the result template

Copy the judge scores and token totals into `result-template.json`.

Use these token values from the existing drill-down trial if you reuse the same task flow:

- clue_tokens: 8958
- drill_down_tokens: 44102
- total_tokens: 53060
- raw_estimate_tokens: 147680
- etrr: 0.6407

## Source of truth

- Task definition: `tests\fixtures\lane_a_extended_tasks.yaml`
- Projection: `experiments\runs\v2-lane-a-nest\v2-proj-nest-tf2-001.json`
- External repo root: `experiments/external-repos/nest`
