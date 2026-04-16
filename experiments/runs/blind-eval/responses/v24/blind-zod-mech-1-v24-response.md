# v2.4 Response: blind-zod-mech-1
Date: 2026-04-16

## Question
What exact unknown-key and object-composition behaviors does Zod apply when parsing object schemas?

## Answer

### 1. Unknown-Key Handling

#### v3: Three Modes via `UnknownKeysParam`

The v3 layer defines three explicit modes for handling unknown keys:

- **`UnknownKeysParam = "passthrough" | "strict" | "strip"`** (`UnknownKeysParam`, `packages/zod/src/v3/types.ts:2368-2370` source snippet).
  - **`"strip"`** (default implied by being first): unknown keys are silently removed from output.
  - **`"passthrough"`**: unknown keys are passed through. `PassthroughType<T extends UnknownKeysParam> = T extends "passthrough" ? { [k: string]: unknown } : unknown` — when passthrough mode is active, the output type includes a string-indexed unknown record (`PassthroughType`, `packages/zod/src/v3/types.ts:2410` source snippet).
  - **`"strict"`**: unknown keys cause validation errors. The existence of `ZodUnrecognizedKeysIssue` as an issue type (referenced in `ZodIssueOptionalMessage` union) confirms that strict mode produces `unrecognized_keys` issues.

- **`SomeZodObject`**: typed as `ZodObject<ZodRawShape, UnknownKeysParam, ZodTypeAny>`, showing that every object schema is parameterized by its unknown-key behavior (`SomeZodObject`, `packages/zod/src/v3/types.ts:2418-2420` source snippet).

- **`ZodDiscriminatedUnionOption`**: typed as `ZodObject<{ [key in Discriminator]: ZodTypeAny } & ZodRawShape, ...>`, showing discriminated unions require a shape containing the discriminator key (`ZodDiscriminatedUnionOption`, `packages/zod/src/v3/types.ts:3100-3101`).

#### v4: Object Configuration with Catchall

- **`$ZodObjectConfig`**: `{ out: Record<string, unknown>; in: Record<string, unknown> }` — defines the input/output shape configuration for objects (`$ZodObjectConfig`, `packages/zod/src/v4/core/schemas.ts:1748-1749`).

- **`$ZodObjectParams`**: `TypeParams<schemas.$ZodObject, "shape" | "catchall">` — object schemas are parameterized by `shape` and `catchall` (`$ZodObjectParams`, `packages/zod/src/v4/core/api.ts:1161-1162`). The presence of `catchall` as a parameter indicates that v4 uses a catchall schema to determine unknown-key behavior.

- **`ZodObject.loose()`**: returns `ZodObject<Shape, core.$loose>` — a method to switch to loose/passthrough mode (`ZodObject.loose`, `packages/zod/src/v4/classic/schemas.ts:1193` source snippet). The `core.$loose` type parameter indicates the unknown-key policy.

#### v4: Unknown Type Params
- **`$ZodUnknownParams = TypeParams<schemas.$ZodUnknown>`** (`$ZodUnknownParams`, `packages/zod/src/v4/core/api.ts:777-779`) — a separate schema type for representing unknown values.

### 2. Object Composition Behaviors

#### v3: Catchall-Based Composition

- **`CatchallOutput<T extends ZodType>`**: `ZodType extends T ? unknown : { [k: string]: T["_output"] }` — when a catchall type is set, all unknown keys must match the catchall's output type. When not set (generic `ZodType`), it resolves to `unknown` (`CatchallOutput`, `packages/zod/src/v3/types.ts:2406-2408` source snippet).
- **`CatchallInput<T extends ZodType>`**: same pattern for input types — `ZodType extends T ? unknown : { [k: string]: T["_input"] }` (`CatchallInput`, `packages/zod/src/v3/types.ts:2408-2410` source snippet).
- **`noUnrecognized<Obj extends object, Shape extends object>`**: referenced at `packages/zod/src/v3/types.ts:2418-2420`, used to enforce that no unrecognized keys appear in the output (for strict mode).

#### v4: Shape Extension
- **`SafeExtendShape<Base extends core.$ZodShape, Ext extends core.$ZodLooseShape>`** (`SafeExtendShape`, `packages/zod/src/v4/mini/schemas.ts:882` source snippet) — a type for safely extending object shapes by merging a base shape with an extension shape. The distinction between `$ZodShape` and `$ZodLooseShape` suggests that extension shapes may have relaxed constraints compared to the base.

#### v3: Record/Map Key Schemas
- **`KeySchema = ZodType<string | number | symbol, any, any>`** — records accept keys typed as string, number, or symbol (`KeySchema`, `packages/zod/src/v3/types.ts:3493-3494` source snippet).
- **`RecordType<K extends string | number | symbol, V>`**: `[string] extends [K] ? Record<K, V> : ...` — special handling when key is string vs narrower types (`RecordType`, `packages/zod/src/v3/types.ts:3494-3495` source snippet).
- **`$ZodRecordKey = $ZodType<string | number | symbol, unknown>`** in v4 core, accepting the same key types (`$ZodRecordKey`, `packages/zod/src/v4/core/schemas.ts:2684-2691`).
- **`$ZodRecordParams = TypeParams<schemas.$ZodRecord, "keyType" | "valueType">`** — records are parameterized by key and value type schemas (`$ZodRecordParams`, `packages/zod/src/v4/core/api.ts:1273-1275`).
- **`$ZodMapParams = TypeParams<schemas.$ZodMap, "keyType" | "valueType">`** — maps follow the same dual-schema parameterization (`$ZodMapParams`, `packages/zod/src/v4/core/api.ts:1290-1292`).

#### v3: Parse Function Types
- **`$Parse`** accepts `_params?: { callee?: util.AnyFunc; Err?: $ZodErrorClass }` — the parse function can receive a custom error class, which would be used when object validation produces issues (`$Parse`, `packages/zod/src/v4/core/parse.ts:7-9`).
- **`$ParseAsync`** follows the same pattern for async parsing (`$ParseAsync`, `packages/zod/src/v4/core/parse.ts:31-32`).

### 3. Detailed v3 Object Parsing Behavior

While the clue file does not include the full `ZodObject._parse` source, related evidence provides insight:

- `ZodObjectDef` is the definition interface for objects, following the `ZodTypeDef` base (`UnknownKeysParam`, `packages/zod/src/v3/types.ts:2368-2370`).
- The v3 `ZodArray._parse` source snippet demonstrates the general parsing pattern: type-check → constraint checks → element parsing → issue accumulation. Object parsing likely follows the same pattern: type-check (is it an object?) → iterate shape keys → parse each property → handle unknown keys per `UnknownKeysParam` → accumulate issues.
- `ParseInputLazyPath` (`packages/zod/src/v3/types.ts:61-85` source snippet) handles path construction lazily, supporting both string and numeric keys, which is used when recursively parsing object properties to build accurate error paths.

### 4. Tuple Composition (Positional Object-Like)

Tuples serve as positional object analogs:
- **`AnyZodTuple = ZodTuple<[ZodTypeAny, ...ZodTypeAny[]] | [], ZodTypeAny | null>`** — tuples have typed positional elements and an optional rest element (`AnyZodTuple`, `packages/zod/src/v3/types.ts:3393-3394` source snippet).
- **`OutputTypeOfTuple`** / **`InputTypeOfTuple`**: map tuple item types to their output/input types (`packages/zod/src/v3/types.ts:3370-3379` source snippets).

### 5. Summary of Unknown-Key Behavior

| Mode | v3 Parameter | v4 Equivalent | Behavior |
|------|-------------|---------------|----------|
| Strip | `"strip"` | (default) | Remove unknown keys silently |
| Passthrough | `"passthrough"` | `ZodObject.loose()` → `core.$loose` | Include unknown keys in output |
| Strict | `"strict"` | (strict object) | Error on unknown keys (`ZodUnrecognizedKeysIssue`) |
| Catchall | Catchall schema | `$ZodObjectParams` `"catchall"` | Validate unknown keys against catchall schema |

### What Cannot Be Determined

- The exact runtime logic of `ZodObject._parse` — the source code for object parsing is not included in the clue file or source snippets.
- How v4's `core.$loose` type is defined or what other unknown-key policy types exist alongside it.
- The exact behavior when both a catchall and an `UnknownKeysParam` are specified simultaneously.
- How `SafeExtendShape` handles key conflicts between base and extension shapes at runtime.
- The `$InferZodRecordInput` types noted in GAPS are uncovered — exact record input inference logic is unknown.
- Whether v4 preserves the same three-mode (`strip`/`passthrough`/`strict`) model or replaces it entirely with the catchall approach.
