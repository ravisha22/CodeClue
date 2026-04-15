# Response: blind-zod-mech-2 (with drill-down)
Date: 2026-04-15

The provided material shows several message-customization layers, but it does **not** fully reveal the final precedence rule among them.

The clearest global/customization layer is the error-map API. In v3 there are `setErrorMap` and `getErrorMap` functions in `packages/zod/src/v3/errors.ts`, and in v4 classic compat `getErrorMap` delegates to `core.config` (setErrorMap, packages/zod/src/v3/errors.ts:7-7; getErrorMap, packages/zod/src/v3/errors.ts:11-11; getErrorMap, packages/zod/src/v4/classic/compat.ts:53-53). That means one layer of message selection comes from shared error-map configuration stored in or behind core config (getErrorMap, packages/zod/src/v4/classic/compat.ts:53-53).

A second visible layer is direct message input normalization. `unwrapMessage` accepts `string | { message: string } | undefined | null` and returns `string | undefined`, so the system clearly supports caller-provided message values in at least two shapes and normalizes them before further use (source snippet: unwrapMessage, packages/zod/src/v4/core/util.ts L834-834).

A third layer is schema-side issue creation. There is a `setError` helper in `packages/zod/src/v3/types.ts`, plus `issue(...)` and `finalizeIssue(...)` helpers in `packages/zod/src/v4/core/util.ts` (setError, packages/zod/src/v3/types.ts:346-346; source snippet: issue, packages/zod/src/v4/core/util.ts L906-906; source snippet: finalizeIssue, packages/zod/src/v4/core/util.ts L838-838). That suggests schemas/checks can create raw issues and then pass them through a finalization step where the eventual emitted message is likely resolved (source snippet: finalizeIssue, packages/zod/src/v4/core/util.ts L838-838).

After message selection/finalization, the error output is processed and formatted. Both v3 and v4 expose `processError` functions that accumulate and transform via `map`, and v4 also exposes `prettifyError`, which accumulates lines and joins them (processError, packages/zod/src/v3/ZodError.ts:224-224; processError, packages/zod/src/v4/core/errors.ts:342-342; prettifyError, packages/zod/src/v4/core/errors.ts:435-435). So message choice happens before or during issue finalization, and then those finalized issues are rendered into final output strings (source snippet: finalizeIssue, packages/zod/src/v4/core/util.ts L838-838; prettifyError, packages/zod/src/v4/core/errors.ts:435-435).

The safest reconstruction is therefore:
1. A direct message may be supplied and normalized with `unwrapMessage` (source snippet: unwrapMessage, packages/zod/src/v4/core/util.ts L834-834).
2. Shared error-map configuration can be retrieved through `getErrorMap`, which in v4 classic reads from `core.config` (getErrorMap, packages/zod/src/v4/classic/compat.ts:53-53).
3. Issues are created and finalized through `issue(...)` / `finalizeIssue(...)`, which is the likely point where the final emitted message is decided (source snippet: issue, packages/zod/src/v4/core/util.ts L906-906; source snippet: finalizeIssue, packages/zod/src/v4/core/util.ts L838-838).
4. Finalized errors are processed and prettified for output (processError, packages/zod/src/v4/core/errors.ts:342-342; prettifyError, packages/zod/src/v4/core/errors.ts:435-435).

What I cannot determine from the prompt: the exact precedence between inline messages, schema-level `setError`, any per-parse customization, `finalizeIssue`, and the global error map, because the actual bodies/call graph for `finalizeIssue`, `setErrorMap`, `getErrorMap`, and `setError` are not shown.
