# Gap Remediation Plan: From Workshop Paper to Conference Paper
# Three critical gaps must be closed for ICSE/FSE/ASE submission

## Gap 1: Self-Evaluation Bias
### Problem
Claude Opus 4 served as system-under-test AND evaluator.
Fidelity scores may reflect model self-consistency rather than objective quality.

### Remediation
Execute the cross-model evaluation protocol (docs/CROSS-MODEL-EVALUATION-PROTOCOL.md):

1. **Run Arm B/A with GPT-4o** on all 23 tasks using the SAME projections.
   - Access: OpenAI API with gpt-4o model.
   - Estimated cost: ~$5-10 (23 tasks × 2 arms × ~5K tokens per task).
   - Time: 1-2 hours of scripted API calls.

2. **Run Arm B/A with Gemini 2.5 Pro** on the same 23 tasks.
   - Access: Google AI Studio or Vertex AI.
   - Estimated cost: ~$3-5.
   - Time: 1-2 hours.

3. **Score all answers with an independent judge model** (the model that did NOT consume).
   - GPT-4o consumed → Gemini judges. Gemini consumed → GPT-4o judges.

4. **Compute correlation with Claude's scores.**
   - Need: Spearman >= 0.70, mean delta <= 0.15, TF3 finding replicates.

### Effort: 1 day. No code changes needed — protocol and prompt templates are ready.

## Gap 2: Statistical Power (n=23)
### Problem
3-5 tasks per family is too few for per-family statistical significance.
Bootstrap confidence intervals on 3-sample families will be very wide.

### Remediation

1. **Scale to 50 tasks total** (10 per family × 5 families).
   - Add 27 more tasks across the 7 existing repos.
   - The task design infrastructure is built: YAML format, prompt profiles, projection pipeline.
   - Ground truth: leverage the source files already cloned and the LLM's ability to read them.

2. **Task design targets:**

   | Family | Current | Add | Total |
   | --- | ---: | ---: | ---: |
   | TF1 (architecture) | 5 | 5 | 10 |
   | TF2 (impact) | 5 | 5 | 10 |
   | TF3 (edit) | 3 | 7 | 10 |
   | TF4 (behavior) | 5 | 5 | 10 |
   | TF5 (security) | 5 | 5 | 10 |

3. **Statistical analysis** with 10 per family:
   - Bootstrap 95% CI on per-family fidelity (1000 resamples).
   - Wilcoxon signed-rank test for Arm B vs Arm A paired differences.
   - Effect size (Cliff's delta) per family.

### Effort: 2-3 days. Task design (1 day), projection generation (automated), scoring (1-2 days).

## Gap 3: Tier 2 Not Tested
### Problem
H5, H6, H7 are all untested. The core novel contribution (confidence-gated drill-down
with semantic contracts) has zero empirical evidence.

### Remediation (Phased)

#### Phase 1: Tier 2 Generation on Flask (1 repo, proof of concept)
1. Use Claude/GPT-4o to generate Tier 2 semantic contracts for Flask's 8 core modules:
   - app.py, ctx.py, sessions.py, config.py, blueprints.py, helpers.py, wrappers.py, testing.py

2. For each module, generate:
   - `preconditions`, `postconditions`, `failure_modes` for all function nodes.
   - `complexity_indicators` semantic fields (uses_reflection, uses_dynamic_dispatch, etc.).
   - Set `tier: 2` in the contract.

3. Inject the Tier 2 contracts into the graph: update node `semantic_contract` fields.

4. Re-run the 7 Flask tasks with Tier 2 enriched graph.

5. **Measure H6**: Did >= 90% of modules produce valid Tier 2 contracts?

6. **Score Arm B again with Tier 2**: Does fidelity improve?

#### Phase 2: MCP Tool Server (drill-down execution)
1. Implement the MCP server with `code_slice` and `resolve_dependency` tools.
   - Engineering design exists in PRD Appendix E.5.
   - The server is ~300 lines of Python using the `mcp` SDK.

2. Run a "drill-down trial":
   - On the tasks where v2 confidence is < 0.85 (expanded_lookup or targeted_lookup).
   - Let the consuming model invoke tools via MCP protocol.
   - Measure: fidelity AFTER drill-down vs fidelity BEFORE.

3. **Measure H5**: Is the lift >= 0.10 at cost < 50% raw?
4. **Measure H7**: Is ETRR >= 0.65?

#### Phase 3: End-to-End Demo
1. Pick the single best TF2 task (worst Tier 1 family).
2. Show the full pipeline: Tier 1 clue → low confidence → suggested action → MCP tool call → enriched reasoning → improved answer.
3. This becomes the paper's running example.

### Effort:
- Phase 1: 1-2 days (LLM generation + validation + re-scoring).
- Phase 2: 2-3 days (MCP server implementation + trial execution).
- Phase 3: 0.5 day (writeup of the demo).

## Priority Order

| Priority | Gap | Effort | Impact on Paper |
| --- | --- | --- | --- |
| 1 | Cross-model eval (Gap 1) | 1 day | Eliminates the #1 reviewer objection |
| 2 | Tier 2 on Flask (Gap 3 Phase 1) | 1-2 days | Proves the core contribution works |
| 3 | Scale to 50 tasks (Gap 2) | 2-3 days | Enables statistical claims per family |
| 4 | MCP drill-down trial (Gap 3 Phase 2) | 2-3 days | Tests H5/H7, the novel hypotheses |

**Total to conference-ready: ~7-10 days of focused execution.**

## Model Recommendations for Each Role

| Role | Primary | Backup |
| --- | --- | --- |
| Clue generation (Tier 2) | Claude 3.5 Sonnet | GPT-4o |
| Task consumption (Arm B/A) | GPT-4o | Gemini 2.5 Pro |
| Independent judge | Gemini 2.5 Pro | Qwen3-235B |
| Self-consistency runs | GPT-4o at temperature 0.7 | Claude at temperature 0.7 |

Why these choices:
- Claude for generation: best at structured output with typed YAML fields.
- GPT-4o for consumption: different family from generator (eliminates same-model bias for G8).
- Gemini for judging: third family, longest context window, lowest cost for bulk scoring.
- Qwen3 as backup judge: fourth family, open-weights, independent verification.
