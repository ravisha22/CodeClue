# v2.4.1 Response: blind-zod-mech-1
Date: 2026-04-16

## Unknown-Key and Object-Composition Behaviors

### 1. Unknown-Key Handling Modes

#### The Three Modes

Zod defines three modes for handling unrecognized keys via `UnknownKeysParam = "passthrough" | "strict" | "strip"` (snippet: `UnknownKeysParam`, `packages/zod/src/v3/types.ts L2368-2370`).

- **`"strip"`** (default): Unknown keys are silently removed from output. This is the standard behavior when no explicit mode is set.
- **`"strict"`**: Unknown keys cause validation failures. The existence of `ZodUnrecognizedKeysIssue` in the `ZodIssueOptionalMessage` union (FOCUS: referenced indirectly via v3 error types) confirms that strict mode emits a specific issue code.
- **`"passthrough"`**: Unknown keys are preserved in output. The type `PassthroughType<T extends UnknownKeysParam> = T extends "passthrough" ? { [k: string]: unknown } : unknown` (snippet: `PassthroughType`, L2410-2412) shows that passthrough mode adds a `{ [k: string]: unknown }` index signature to the output type.

#### v4 Classic API

- **`ZodObject.loose()`**: Returns `ZodObject<Shape, core.$loose>` (snippet: `ZodObject.loose`, `packages/zod/src/v4/classic/schemas.ts L1193`). This provides the v4 equivalent of passthrough mode, using a `core.$loose` type parameter.
- **`$ZodObjectConfig`**: Defined as `{ out: Record<string, unknown>; in: Record<string, unknown> }` (FOCUS: `packages/zod/src/v4/core/schemas.ts:1748-1749`), showing object schemas track separate input and output type configurations.
- **`$ZodObjectParams`**: `TypeParams<schemas.$ZodObject, "shape" | "catchall">` (FOCUS: `packages/zod/src/v4/core/api.ts:1161-1162`), confirming object schemas are parameterized by `shape` and `catchall`.

#### Catchall Schemas

- **`CatchallOutput<T extends ZodType>`**: `ZodType extends T ? unknown : { [k: string]: T["_output"] }` (snippet: `CatchallOutput`, L2406-2408). When a catchall schema is set, unknown keys are validated against it and their values typed accordingly.
- **`CatchallInput<T extends ZodType>`**: Same pattern for input types — `{ [k: string]: T["_input"] }` (snippet: `CatchallInput`, L2408-2410).
- These conditional types ensure that when no catchall is provided (i.e., `T` is the base `ZodType`), the type resolves to `unknown`, effectively applying no constraint.

### 2. Object Type Variants

- **`SomeZodObject = ZodObject<ZodRawShape, UnknownKeysParam, ZodTypeAny>`** (snippet: `SomeZodObject`, L2418-2420; also FOCUS: `packages/zod/src/v3/types.ts:2418`). This is the constrained object type used in APIs that accept any object schema.
- **`AnyZodObject = ZodObject<any, any, any>`** (snippet: `AnyZodObject`, L2926-2928). This is the fully-unconstrained variant.

### 3. Object Composition

#### Shape Extension

- **`SafeExtendShape<Base extends core.$ZodShape, Ext extends core.$ZodLooseShape>`** (snippet: `SafeExtendShape`, `packages/zod/src/v4/mini/schemas.ts L882`). This type safely merges a base shape with an extension shape, using `$ZodShape` for strict shapes and `$ZodLooseShape` for extensions.

#### Discriminated Unions

- **v3 `ZodDiscriminatedUnionOption<Discriminator>`**: `ZodObject<{ [key in Discriminator]: ZodTypeAny } & ZodRawShape, ...>` (FOCUS: `packages/zod/src/v3/types.ts:3100-3101`). Each option in a discriminated union must be a ZodObject whose shape includes the discriminator key.
- **v4 `ZodDiscriminatedUnion`**: `extends ZodUnion<Options>, core.$ZodDiscriminatedUnion<Options, Disc>` with `_zod: core.$ZodDiscriminatedUnionInternals<Options, Disc>` and `def: core.$ZodDiscriminatedUnionDef<Options, Disc>` (snippet: `ZodDiscriminatedUnion`, `packages/zod/src/v4/classic/schemas.ts L1379-1389`). It extends `ZodUnion`, adding discriminator-specific internals.

#### Record and Map Schemas

- **`$ZodRecordKey = $ZodType<string | number | symbol, unknown>`** (FOCUS: `packages/zod/src/v4/core/schemas.ts:2684-2691`, multiple overloads). Record keys are constrained to string, number, or symbol types.
- **`$ZodRecordParams = TypeParams<schemas.$ZodRecord, "keyType" | "valueType">`** (FOCUS: `packages/zod/src/v4/core/api.ts:1273-1275`); similarly `$ZodMapParams = TypeParams<schemas.$ZodMap, "keyType" | "valueType">` (FOCUS: L1290-1292). Both use a `keyType`/`valueType` pair.
- **`$ZodUnknownParams = TypeParams<schemas.$ZodUnknown>`** (FOCUS: L777-779).

### 4. Optional and Exact-Optional

- **`ZodExactOptional<T>`**: `extends _ZodType<core.$ZodExactOptionalInternals<T>>, core.$ZodExactOptional<T>` with `unwrap(): T` (snippet: `ZodExactOptional`, L1849-1856; drill snippet: `ZodExactOptional.unwrap` returns `T` at L1855). This distinguishes between "key absent" and "key present but undefined".

### 5. v3 Parse Mechanics for Objects

- **Parse flow**: Object schemas follow the general `_parse` pattern — `ZodArray._parse` (shown in snippets) demonstrates the approach: call `_processInputParams(input)`, validate type, check constraints from `_def`, parse child elements. The object schema's `_parse` would similarly iterate over the shape, validate each property, and then apply the `UnknownKeysParam` policy to remaining keys.

### What Cannot Be Determined

- **`ZodObject._parse` implementation**: The actual body of the v3 `ZodObject._parse` method is not provided in snippets or FOCUS. The exact sequence of strip/strict/passthrough key handling within `_parse` cannot be confirmed.
- **How `ZodObject.loose()` modifies internals**: Only the return type `ZodObject<Shape, core.$loose>` is shown (snippet), not what `$loose` does at runtime.
- **`ZodObject.merge`, `ZodObject.extend`, `ZodObject.pick`, `ZodObject.omit`**: These composition methods are not shown in the clue file.
- **`$ZodLooseShape` definition**: Referenced by `SafeExtendShape` but not defined in the provided data.
- **Intersection behavior**: `ZodIntersection._parse` is listed in SYM (L3292) but its body is not provided — how intersections merge object shapes at parse time is unknown.
- **`noUnrecognized` type utility**: Mentioned adjacent to `SomeZodObject` (snippet: L2418-2420) but its definition is truncated.
- **GAPS explicitly lists**: `keyof`, `$ZSFObject`, `ArrayKeys` as uncovered symbols.
