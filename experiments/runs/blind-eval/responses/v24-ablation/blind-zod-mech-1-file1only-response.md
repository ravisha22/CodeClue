# v2.4 Ablation (File 1 Only): blind-zod-mech-1
Date: 2026-04-16

The clue proves that Zod object schemas are parameterized by at least two object-specific dimensions: `shape` and `catchall`. That is explicit in `$ZodObjectParams = TypeParams<schemas.$ZodObject, "shape" | "catchall">`. [ $ZodObjectParams (packages/zod/src/v4/core/api.ts:1161-1162) ]

It also shows that object schemas carry both input and output record shapes: `$ZodObjectConfig = { out: Record<string, unknown>; in: Record<string, unknown> }`. [ $ZodObjectConfig (packages/zod/src/v4/core/schemas.ts:1748-1749) ]

For v3 object typing, `SomeZodObject` is parameterized as `ZodObject<ZodRawShape, UnknownKeysParam, ZodTypeAny>`, which proves unknown-key behavior is part of the object schema’s type-level configuration. [SomeZodObject (packages/zod/src/v3/types.ts:2418-2420)]

The clue also shows one composition pattern directly: a discriminated-union option is itself a `ZodObject` whose shape is the discriminator field plus additional raw shape entries. [ZodDiscriminatedUnionOption (packages/zod/src/v3/types.ts:3100-3101)]

Beyond that, the file is too thin to justify stronger claims. I cannot determine the exact runtime behavior for unknown keys (for example, whether the default is strip, passthrough, or strict), the exact meaning of `ZodObject.loose`, or the exact object-composition rules for merge/extend/intersection while parsing, because those behaviors are not exposed here and the prompt itself flags a drill into `ZodObject.loose`. [GAPS; drill: packages/zod/src/v4/classic/schemas.ts (~1 lines, ZodObject.loose)]
