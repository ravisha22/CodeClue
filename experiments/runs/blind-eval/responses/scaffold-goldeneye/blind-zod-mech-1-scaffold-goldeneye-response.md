# Scaffold (Goldeneye): blind-zod-mech-1
Date: 2026-04-16

## Relevant symbols traced
- Object schemas are parameterized by `shape` and `catchall`. [$ZodObjectParams (packages/zod/src/v4/core/api.ts:1161-1162)]
- `SomeZodObject` also carries an `UnknownKeysParam`, making unknown-key handling an explicit type parameter. [SomeZodObject (packages/zod/src/v3/types.ts:2418-2420)]
- A distinct `loose()` object variant exists. [ZodObject.loose (packages/zod/src/v4/classic/schemas.ts:1193-1193)]
- Composition shows up through safe extension and object-based discriminated-union options. [SafeExtendShape (packages/zod/src/v4/mini/schemas.ts:882-882); ZodDiscriminatedUnionOption (packages/zod/src/v3/types.ts:3100-3101)]

## Answer
From the provided clue/snippets, the strongest supported conclusions are:

1. **Zod object parsing is configurable along at least three axes: declared shape, catch-all handling, and an unknown-key mode.** That is visible from `$ZodObjectParams`, which includes `"shape" | "catchall"`, and from `SomeZodObject`, which is parameterized by `UnknownKeysParam`. [$ZodObjectParams (packages/zod/src/v4/core/api.ts:1161-1162); SomeZodObject (packages/zod/src/v3/types.ts:2418-2420)]
2. **There is an explicit “loose” object mode.** The `ZodObject.loose()` signature returns `ZodObject<Shape, core.$loose>`, which is direct evidence of a dedicated unknown-key/object-mode variant. [ZodObject.loose (packages/zod/src/v4/classic/schemas.ts:1193-1193)]
3. **Object composition is also a first-class concern.** `SafeExtendShape` indicates a typed extension/composition helper for object shapes, and `ZodDiscriminatedUnionOption` is itself defined in terms of a `ZodObject` composed from a discriminator field plus a raw shape. [SafeExtendShape (packages/zod/src/v4/mini/schemas.ts:882-882); ZodDiscriminatedUnionOption (packages/zod/src/v3/types.ts:3100-3101)]

## Gaps / uncertainty
The prompt does **not** expose the runtime parse bodies that would tell us the *exact* behavior for unknown keys - e.g., whether they are stripped, preserved, rejected, or validated via `catchall`, nor how merges/extensions resolve collisions at parse time. The GAPS section explicitly says this question is mechanistic and that there are zero behavior annotations, so those exact runtime semantics cannot be proven from the supplied evidence alone. [GAPS]
