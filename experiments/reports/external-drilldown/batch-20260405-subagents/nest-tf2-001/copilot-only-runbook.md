# Copilot-Only Runbook

This version assumes the only LLM access you have is through GitHub Copilot in VS Code.

## Goal

Prove one simple thing: the answer gets better after Copilot uses the CodeClue MCP tools.

## Best evidence you can get with Copilot

### Best case

If your Copilot model picker exposes different model families, use:

- Chat A: consumer BEFORE pass
- Chat B: same consumer family for AFTER pass with MCP enabled
- Chat C: different model family as judge

This is acceptable cross-model evidence inside Copilot.

### Fallback case

If Copilot only gives you one model family, use three fresh chats anyway:

- Chat A: BEFORE pass
- Chat B: AFTER pass with MCP enabled
- Chat C: same-model strict judge

This is still useful, but it is only **pilot evidence**, not independent cross-model validation.

## Step 1: Start the MCP server

In the workspace root, run:

```powershell
.\.venv\Scripts\codeclue-mcp.exe --graph-path experiments/runs/v2-lane-a-nest/graph.json --repo-root experiments/external-repos/nest
```

## Step 2: BEFORE pass in Copilot

- Open a fresh Copilot chat.
- If you can choose a model, note which one you picked.
- Paste `consumer-pre.prompt.md`.
- Save the answer into `answers/pre-answer.md`.

## Step 3: AFTER pass in Copilot with MCP

- Open a second fresh Copilot chat.
- Use the same consumer model family as Step 2 if possible.
- Make sure MCP/tool usage is enabled for the chat.
- Paste `consumer-post.prompt.md`.
- Let Copilot use the CodeClue MCP tools.
- Save the answer into `answers/post-answer.md`.

## Step 4: Judge in Copilot

- Open a third fresh Copilot chat.
- If possible, choose a different model family than the consumer.
- If a different family is not available, use `judge-same-model.prompt.md` instead of `judge.prompt.md`.
- Paste the before/after answers into the prompt placeholders.
- Save the result into `answers/judge-result.json`.

## Step 5: Record what happened honestly

Fill in `result-template.json` and set:

- `consumer_model_before`
- `consumer_model_after`
- `judge_model`
- `judge_mode`
- `evidence_tier`

Use `evidence_tier = "cross-model-copilot"` only if the judge was a different model family.

Use `evidence_tier = "same-model-copilot-pilot"` if all three chats used the same family.

## What to say in the paper

- If different Copilot model families were used: this is partial external validation.
- If the same Copilot model family judged the run: this is preliminary pilot evidence only.

## Source of truth

- Task definition: `tests\fixtures\lane_a_extended_tasks.yaml`
- Projection: `experiments\runs\v2-lane-a-nest\v2-proj-nest-tf2-001.json`
- External repo root: `experiments/external-repos/nest`
