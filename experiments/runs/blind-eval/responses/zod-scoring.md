# CodeClue Blind Evaluation — Zod Scoring

Scorer: Copilot CLI (automated)
Date: 2025-07-25

---

### blind-zod-struct-1 (3/4)
F1: COVERED — Response identifies `zod`/classic as "higher-level, compatibility-oriented, user-facing wrapper layer over core" with config APIs and schema conversion helpers.
F2: COVERED — Response calls `zod/mini` "a smaller alternate API built on the same core" with shared delegation to `core._unknown`, capturing the same-validation / different-surface split. Does not explicitly name the functional or tree-shakable character.
F3: COVERED — Response clearly states "`zod/v4/core` appears to be the shared low-level engine/utilities layer" and shows both classic and mini delegating to it.
F4: MISS — No mention of locale loading, English locale, or localization behavior in the package split.

### blind-zod-struct-2 (2/4)
F1: MISS — Response identifies v3 `ZodType` as the hub with colocated subclasses, but does not name the v4 core `$ZodType` or discuss documented categories in the core sense.
F2: MISS — No mention of the `_zod` property or its `def` field.
F3: COVERED — Response identifies checks as "an execution phase over one or more checks, rather than being represented only as standalone schema classes," capturing the separate modeling of refinements, though `$ZodCheck` subclass naming is absent.
F4: COVERED — Response references `ZodError` and multiple issue-related functions (`issue`, `finalizeIssue`, `processError`), identifying the error-class-plus-issues organization.

### blind-zod-rel-1 (0/4)
F1: MISS — Response explicitly states "the clue does not explicitly show inheritance edges such as `extends`" and does not mention `$ZodType` or input/output type parameters.
F2: MISS — Response explicitly says it cannot determine mini schema/error type relationships and does not mention `ZodMiniType` or its reduced method set.
F3: MISS — Response explicitly states it cannot determine "whether `ZodError` itself extends a core error base."
F4: MISS — No mention of string-format classes participating in both schema and refinement hierarchies.

### blind-zod-rel-2 (2/4)
F1: COVERED — Response describes a staged flow: schema types drive parsing, then `runChecks` runs as a separate "execution phase that can iterate, accumulate results, and potentially short-circuit," capturing the parse-then-check pipeline.
F2: MISS — `.parse()` and `.safeParse()` are not mentioned or compared.
F3: MISS — Async refinements and async parsing variants are not mentioned.
F4: COVERED — Response states "error maps/config influence how those issues are interpreted/rendered" and that "message choice happens before or during issue finalization," capturing that error maps layer on top of generated issues rather than replacing validation.

### blind-zod-mech-1 (0/4)
F1: MISS — Response explicitly says "I cannot determine… whether unknown keys are stripped, preserved, rejected, or handled differently."
F2: MISS — `z.strictObject()` is not mentioned.
F3: MISS — `z.looseObject()` is not mentioned.
F4: MISS — `.catchall()` is not mentioned.

### blind-zod-mech-2 (0/4)
F1: MISS — Response explicitly says it cannot determine "the exact precedence between inline messages, schema-level `setError`, any per-parse customization, `finalizeIssue`, and the global error map."
F2: MISS — Per-parse error map and its rank are not established.
F3: MISS — `z.config()` is mentioned only as a delegation target; its rank relative to per-parse and locale defaults is not stated.
F4: MISS — Returning `undefined` from an error map to yield to the next level is not mentioned.

---

## Summary

| Task               | Score | Notes                                      |
|--------------------|-------|--------------------------------------------|
| blind-zod-struct-1 | 3/4   | Missed locale/localization split            |
| blind-zod-struct-2 | 2/4   | Missed `$ZodType`, `_zod.def`              |
| blind-zod-rel-1    | 0/4   | Explicitly unable to determine inheritance  |
| blind-zod-rel-2    | 2/4   | Missed parse/safeParse, async refinements   |
| blind-zod-mech-1   | 0/4   | Explicitly unable to determine key handling  |
| blind-zod-mech-2   | 0/4   | Explicitly unable to determine precedence    |
| **Total**          | **7/24** |                                          |
