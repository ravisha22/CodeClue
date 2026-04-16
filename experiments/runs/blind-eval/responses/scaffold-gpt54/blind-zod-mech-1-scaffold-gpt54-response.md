# Scaffold (GPT-5.4): blind-zod-mech-1
Date: 2026-04-16

## Trace
The object-schema evidence centers on `SomeZodObject`, `$ZodObjectParams`, `$ZodObjectConfig`, `ZodObject.loose`, `SafeExtendShape`, and the presence of `ZodAny` (`SomeZodObject — packages/zod/src/v3/types.ts:2418-2420`; `$ZodObjectParams — packages/zod/src/v4/core/api.ts:1161-1162`; `$ZodObjectConfig — packages/zod/src/v4/core/schemas.ts:1748-1749`; source snippet `ZodObject.loose  (packages/zod/src/v4/classic/schemas.ts L1193-1193)`; source snippet `SafeExtendShape  (packages/zod/src/v4/mini/schemas.ts L882-882)`; source snippet `ZodAny  (packages/zod/src/v4/classic/schemas.ts L1049-1051)`).

## Answer
- **Zod object schemas carry an explicit unknown-key policy as part of their type shape.** In v3, `SomeZodObject` is `ZodObject<ZodRawShape, UnknownKeysParam, ZodTypeAny>`, which shows that an object schema is parameterized by both its field shape and an `UnknownKeysParam` (`SomeZodObject — packages/zod/src/v3/types.ts:2418-2420`).
- **In v4, object schemas are also parameterized by `shape` and `catchall`.** `$ZodObjectParams` is `TypeParams<schemas.$ZodObject, "shape" | "catchall">`, and `$ZodObjectConfig` says object input/output are `Record<string, unknown>`, so object parsing/configuration explicitly includes a catchall dimension in addition to the declared shape (`$ZodObjectParams — packages/zod/src/v4/core/api.ts:1161-1162`; `$ZodObjectConfig — packages/zod/src/v4/core/schemas.ts:1748-1749`).
- **One concrete unknown-key mode exposed by the snippets is `.loose()`.** The drill-down snippet shows `loose(): ZodObject<Shape, core.$loose>;`, so calling `.loose()` changes the object schema to the `$loose` unknown-key mode (`source snippet `ZodObject.loose  (packages/zod/src/v4/classic/schemas.ts L1193-1193)`).
- **Object composition includes shape extension.** The snippet `SafeExtendShape<Base extends core.$ZodShape, Ext extends core.$ZodLooseShape>` shows that Zod has a composition helper for extending a base shape with an extension shape, and that the extension side is explicitly “loose” (`source snippet `SafeExtendShape  (packages/zod/src/v4/mini/schemas.ts L882-882)`).
- **Object composition also appears in specialized object-derived types.** `ZodDiscriminatedUnionOption` is typed as a `ZodObject` whose shape is an intersection of a discriminator field and a raw shape, which shows Zod composes object schemas by combining shapes, not only by flat declaration (`ZodDiscriminatedUnionOption — packages/zod/src/v3/types.ts:3100-3101`).
- **A catchall schema may be able to accept arbitrary-value types, but the evidence stops short of showing its exact runtime parse effect.** We can see that object params include `catchall`, and we can see `ZodAny` exists as a schema type, but the prompt does not show the object-parser body that would prove how unknown keys are handled at runtime with a given catchall (`$ZodObjectParams — packages/zod/src/v4/core/api.ts:1161-1162`; source snippet `ZodAny  (packages/zod/src/v4/classic/schemas.ts L1049-1051)`).

## Exactness the evidence does support
From the supplied clue/snippets, the exact supported claims are:
1. object parsing/configuration has an explicit **unknown-key policy parameter** (`UnknownKeysParam`) (`SomeZodObject — packages/zod/src/v3/types.ts:2418-2420`);
2. object configuration also includes a **catchall** dimension (`$ZodObjectParams — packages/zod/src/v4/core/api.ts:1161-1162`);
3. `.loose()` selects the **`core.$loose`** object mode (`source snippet `ZodObject.loose  (packages/zod/src/v4/classic/schemas.ts L1193-1193)`);
4. object composition includes **safe shape extension** (`source snippet `SafeExtendShape  (packages/zod/src/v4/mini/schemas.ts L882-882)`).

## Gaps / uncertainty
`GAPS` explicitly says this question is mechanistic and only drills into `ZodObject.loose`. So the prompt does **not** reveal the parser body that would let us state, with evidence, whether unknown keys are stripped, rejected, or preserved in each mode, nor how merge/extend precedence is resolved at runtime (`GAPS`; source snippet `ZodObject.loose  (packages/zod/src/v4/classic/schemas.ts L1193-1193)`). In other words: the artifact proves the existence of unknown-key modes and composition hooks, but not the full runtime semantics of every object mode.
