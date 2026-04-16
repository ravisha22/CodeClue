# Cross-Model (Goldeneye): blind-zod-mech-1
Date: 2026-04-16

The provided evidence shows that Zod’s object parsing is parameterized around declared shape plus explicit unknown-key controls:

- In v4, object params are `TypeParams<schemas.$ZodObject, "shape" | "catchall">`, so the parser’s behavior for object schemas is driven by the object’s `shape` together with a `catchall` policy. [$ZodObjectParams, packages/zod/src/v4/core/api.ts:1161-1162]
- The object config itself is string-keyed on both input and output (`{ out: Record<string, unknown>; in: Record<string, unknown> }`), which means object parsing is framed as transforming one string-keyed record into another. [$ZodObjectConfig, packages/zod/src/v4/core/schemas.ts:1748-1749]
- In the v3 surface, `SomeZodObject` is explicitly parameterized as `ZodObject<ZodRawShape, UnknownKeysParam, ZodTypeAny>`, so unknown-key handling is an explicit part of the object type definition. [SomeZodObject, packages/zod/src/v3/types.ts:2418-2420]
- The one exact unknown-key mode that is directly exposed in the snippets is `loose()`, which returns `ZodObject<Shape, core.$loose>`. That is concrete evidence for a loose-object behavior. [ZodObject.loose, packages/zod/src/v4/classic/schemas.ts:1193]
- For object composition, the provided type-level mechanism is `SafeExtendShape<Base extends core.$ZodShape, Ext extends core.$ZodLooseShape>`, which shows that Zod composes object schemas by safely extending a base shape with an additional/loose shape. [SafeExtendShape, packages/zod/src/v4/mini/schemas.ts:882]
- Zod also uses object schemas compositionally inside larger constructs, such as `ZodDiscriminatedUnionOption`, which is itself a `ZodObject<... & ZodRawShape>`. [ZodDiscriminatedUnionOption, packages/zod/src/v3/types.ts:3100-3101]

I do not see further exact parse-branch details for non-`loose` unknown-key modes in the provided prompt, so the strongest supported conclusion is: object parsing is controlled by `shape` + `catchall`/`UnknownKeysParam`, and composition is shape extension via `SafeExtendShape`, with `loose()` as the explicit unknown-key behavior surfaced here. [$ZodObjectParams, packages/zod/src/v4/core/api.ts:1161-1162; SomeZodObject, packages/zod/src/v3/types.ts:2418-2420; ZodObject.loose, packages/zod/src/v4/classic/schemas.ts:1193; SafeExtendShape, packages/zod/src/v4/mini/schemas.ts:882]
