# Reasoning Scaffold — Design & Token Cost Documentation

## Purpose

The reasoning scaffold is an openly stated reasoning aid embedded in CodeClue
evaluation prompts. It standardises how any LLM should read a CodeClue file
before answering a question. The scaffold:

1. Directs the model to **trace evidence first** — identify relevant symbols,
   follow call chains and inheritance hierarchies through the clue
2. Uses clue annotations in a **consistent order** — FOCUS → SYM → INDEX → TREE
3. **Surfaces declared uncertainty** from the GAPS section before answering
4. Only then asks for a **synthesised response** with supported vs uncertain claims

## Why It Exists

Cross-model testing showed that different LLMs extract different amounts of
information from the same clue file. The gap is not in parsing (all models read
the format correctly) but in reasoning depth — some models pattern-match on
surface text while others trace relationships through the clue systematically.

The scaffold bridges this gap by explicitly prompting systematic analysis,
which is especially important for MECHANISTIC questions where the answer must
be assembled from multiple clue entries (behavioral annotations + call chains +
drill-down source snippets).

## Model Agnosticism

The scaffold uses plain procedural English — no model-specific tags, no hidden
instructions, no `<thinking>` blocks. It works identically with GPT, Claude,
Gemini, and other models. This is by design: the format and its consumption
protocol must be deterministic and transparent.

## Token Cost

| Component | Tokens (approx) |
|-----------|-----------------|
| MECHANISTIC scaffold block | ~110 tokens |
| STRUCTURAL/RELATIONAL scaffold block | ~105 tokens |
| File 1 clue content | ~4,100 tokens |
| File 2 drill-down snippets (when used) | ~3,000 tokens |
| Question + framing | ~80 tokens |
| **Total (clue-only with scaffold)** | **~4,285 tokens** |
| **Total (drill-down with scaffold)** | **~7,290 tokens** |

The scaffold adds approximately **2.5-3%** overhead to total prompt size.
This is explicitly documented because transparency about token consumption is
a core trust principle of CodeClue.

## Where It Is Used

| Context | Scaffold Present? | Notes |
|---------|------------------|-------|
| Evaluation (answerer prompts) | Yes | Standardises eval across models |
| LLM-enhanced clue generation (future) | Yes | Ensures deeper behavioral summaries |
| End-user clue consumption | No (user's choice) | Users may add their own instructions |
| MCP server tool calls | No | Tools return raw data, LLM reasons freely |

## Text of the Scaffold

### For MECHANISTIC questions (with File 2 drill-down)

> **Reasoning scaffold:** Think through the clue systematically before answering.
> First, identify the symbols most relevant to the question from FOCUS, SYM, and
> INDEX. Trace those symbols through the clue before forming any conclusion:
> follow calls: chains, walk extends: hierarchies, and read behavior: annotations
> as compact control-flow summaries. Use TREE and INDEX to place each symbol in
> its module context. Then consult the provided source snippets only to confirm
> or refine the traced path. State explicitly what GAPS says cannot be determined
> from the evidence. Finally, synthesize the answer, separating supported
> conclusions from remaining uncertainty.

### For STRUCTURAL/RELATIONAL questions (clue-only)

> **Reasoning scaffold:** Think through the clue systematically before answering.
> First, identify the modules, symbols, or relationships most relevant to the
> question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before
> concluding: follow calls: chains, walk extends: hierarchies, and use behavior:
> annotations as summaries of how control or responsibility moves. Use TREE and
> INDEX to situate the relationship in the repository structure. State explicitly
> what GAPS says cannot be determined from the clue alone. Finally, synthesize
> the answer, distinguishing supported structure from unresolved uncertainty.
