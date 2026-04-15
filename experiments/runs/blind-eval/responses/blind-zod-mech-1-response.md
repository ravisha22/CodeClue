# Response: blind-zod-mech-1
Date: 2026-04-15

The prompt does not expose the `ZodObject` parse body, so it does **not** let me state the exact unknown-key policy or exact composition algorithm with confidence (ZodObject, packages/zod/src/v3/types.ts:2452-2453). In particular, I cannot determine from the provided clue whether unknown keys are stripped, preserved, rejected, or handled differently under different modes, because no unknown-key policy symbol or object-parse implementation is shown.

What the clue *does* show is the supporting machinery around object parsing:
- Object schemas are represented by `ZodObject` in `packages/zod/src/v3/types.ts` (ZodObject, packages/zod/src/v3/types.ts:2452-2453).
- There are object tests in v4 core utilities: `isObject` and `isPlainObject` (isObject, packages/zod/src/v4/core/util.ts:367-367; isPlainObject, packages/zod/src/v4/core/util.ts:386-386).
- There is object cloning support via `objectClone`, whose behavior delegates to `Object.create` (objectClone, packages/zod/src/v4/core/util.ts:291-291).
- There is value extraction/mapping support via `objectValues`, whose behavior is `TRANSFORM(map)` (objectValues, packages/zod/src/v3/helpers/util.ts:33-33).
- Both classic and mini expose an `unknown()` schema constructor, and both delegate to `core._unknown`, which suggests shared handling for the standalone "unknown" schema type across front-ends (unknown, packages/zod/src/v4/classic/schemas.ts:1070-1070; unknown, packages/zod/src/v4/mini/schemas.ts:727-727).

From that evidence, the strongest safe conclusion is that object parsing likely relies on object-ness checks and helper utilities for cloning/value traversal, and that Zod's classic and mini layers share a common core implementation for the `unknown()` schema constructor (isObject, packages/zod/src/v4/core/util.ts:367-367; objectClone, packages/zod/src/v4/core/util.ts:291-291; unknown, packages/zod/src/v4/classic/schemas.ts:1070-1070; unknown, packages/zod/src/v4/mini/schemas.ts:727-727).

What I cannot determine from this prompt:
- the exact unknown-key behavior inside `ZodObject` parsing;
- whether composition happens by merge, extension, overwrite, or some other rule during parse;
- whether only plain objects are accepted or whether non-plain objects can also pass;
- how unknown-key handling interacts with nested shapes.

Those details would require the actual `ZodObject` implementation or object-composition helpers, and they are not provided here.
