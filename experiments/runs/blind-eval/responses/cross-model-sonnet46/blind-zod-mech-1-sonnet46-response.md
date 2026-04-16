# Cross-Model (Sonnet 4.6): blind-zod-mech-1
Date: 2026-04-16

## Question
What exact unknown-key and object-composition behaviors does Zod apply when parsing object schemas?

## Answer

Zod's object schema handles unknown keys via configurable modes and supports object composition through type-safe shape extension. The clue file provides evidence from both the v3 and v4 APIs.

---

## Part 1 — Unknown-key handling

### 1. v3: `UnknownKeysParam` type parameter

> `SomeZodObject (packages/zod/src/v3/types.ts:2418-2418)` — `type alias SomeZodObject = ZodObject<ZodRawShape, UnknownKeysParam, ZodTypeAny>` [FOCUS, SomeZodObject v3/types.ts:2418].

In v3, `ZodObject` has three type-level parameters: the shape (`ZodRawShape`), an `UnknownKeysParam`, and a catchall type (`ZodTypeAny`). The `UnknownKeysParam` controls what happens to keys in the input that are not in the declared shape. The three possible values (from standard Zod v3 usage, evidenced by this type alias) are:
- **`"strip"`** — Unknown keys are stripped from the parsed output (the default).
- **`"passthrough"`** — Unknown keys are passed through to the output unchanged.
- **`"strict"`** — Unknown keys cause a parse error.

### 2. v4: `$ZodObjectConfig` — `out` and `in` shapes

> `$ZodObjectConfig (packages/zod/src/v4/core/schemas.ts:1748-1748)` — `type alias $ZodObjectConfig = { out: Record<string, unknown>; in: Record<string, unknown> }` [FOCUS, $ZodObjectConfig v4/core/schemas.ts:1748].

In v4 the object configuration is expressed as a type with both `out` (parsed output type) and `in` (input type) constraints, decoupling the input shape from the output shape.

### 3. v4: `$ZodObjectParams` — `shape` and `catchall` parameters

> `$ZodObjectParams (packages/zod/src/v4/core/api.ts:1161-1161)` — `type alias $ZodObjectParams = TypeParams<schemas.$ZodObject, "shape" | "catchall">` [FOCUS, $ZodObjectParams v4/core/api.ts:1161].

The two configurable object parameters are `shape` (the declared field schemas) and `catchall` (the schema applied to any extra keys that are not in `shape`). The `catchall` field is the v4 mechanism that unifies what v3 expressed as `UnknownKeysParam` + catchall type:
- When `catchall` is absent or set to `ZodNever`, unknown keys are stripped.
- When `catchall` is set to a specific type schema, unknown keys matching that schema are passed through (typed passthrough).
- When `catchall` is set to `core.$loose` (see below), unknown keys are allowed freely.

### 4. v4: `ZodObject.loose()` sets catchall to `$loose`

From the source snippet:
```typescript
// ZodObject.loose  (packages/zod/src/v4/classic/schemas.ts L1193-1193)
loose(): ZodObject<Shape, core.$loose>;
```
[source snippet, ZodObject.loose classic/schemas.ts:1193].

Calling `.loose()` on an object schema returns a new `ZodObject` with `catchall` set to `core.$loose`, which allows all unknown keys through without validation. This is the v4 equivalent of v3's `.passthrough()`.

---

## Part 2 — Object composition behaviors

### 5. v4: `SafeExtendShape` — type-safe shape merging

From the source snippet:
```typescript
// SafeExtendShape  (packages/zod/src/v4/mini/schemas.ts L882-882)
export type SafeExtendShape<Base extends core.$ZodShape, Ext extends core.$ZodLooseShape> = { ... }
```
[source snippet, SafeExtendShape mini/schemas.ts:882].

`SafeExtendShape<Base, Ext>` is the type-level utility used when extending an object schema. It constrains the extension shape (`Ext`) to `$ZodLooseShape`, meaning the extending shape can have any field types. The result correctly types the merged shape so that fields in `Ext` override fields in `Base`. This is the implementation basis for `.extend()` and `.merge()` operations.

### 6. v3: `ZodDiscriminatedUnionOption` — objects used in discriminated unions

> `ZodDiscriminatedUnionOption (packages/zod/src/v3/types.ts:3100-3100)` — `type alias ZodDiscriminatedUnionOption = ZodObject<{ [key in Discriminator]: ZodTypeAny } & ZodRawShape, UnknownKeysParam, ZodTypeAny>` [FOCUS, ZodDiscriminatedUnionOption v3/types.ts:3100].

Objects used as discriminated union options must have a discriminant key. The type intersection `{ [key in Discriminator]: ZodTypeAny } & ZodRawShape` enforces this. The `UnknownKeysParam` is preserved, so each branch of a discriminated union retains its own unknown-key policy.

### 7. v3 `ZodObject._parse` — the runtime object parsing method

The SYM table shows all major Zod types have a `_parse` method. The INDEX lists `packages/zod/src/v3/types.ts` (5138L) with exports including `AnyZodObject` [INDEX, v3/types.ts]. The base `ZodType._parse (v3/types.ts:170)` [SYM] is the protocol; `ZodObject._parse` follows it to:
1. Check the input is a plain object (fail if not).
2. Iterate over the declared `shape` keys and parse each field.
3. Apply the unknown-key policy (`strip` / `passthrough` / `strict`) to any extra keys.
4. If a `catchall` schema is set, parse unknown keys through it.

### 8. v4: `$ZodExactOptional` — exact optional fields

From the source snippet:
```typescript
// ZodExactOptional  (packages/zod/src/v4/classic/schemas.ts L1849-1856)
export interface ZodExactOptional<T extends core.SomeType = core.$ZodType>
  extends _ZodType<core.$ZodExactOptionalInternals<T>>,
    core.$ZodExactOptional<T> {
  "~standard": ZodStandardSchemaWithJSON<this>;
  unwrap(): T;
}
```
[source snippet, ZodExactOptional classic/schemas.ts:1849].

`ZodExactOptional` is a wrapper type used on object fields to implement "exact optional" semantics: the field is valid when the key is completely absent from the input, but invalid when the key is explicitly set to `undefined`. This is stricter than standard `ZodOptional` (which accepts `undefined`). The `.unwrap(): T` method [source snippet, ZodExactOptional.unwrap classic/schemas.ts:1855] retrieves the inner schema.

---

## Part 3 — v4 record key constraints

> `$ZodRecordKey (packages/zod/src/v4/core/schemas.ts:2684-2691)` — `type alias $ZodRecordKey = $ZodType<string | number | symbol, unknown>` [FOCUS, $ZodRecordKey v4/core/schemas.ts:2684-2691].

This is relevant to object composition: when building a `ZodRecord` (an object with a dynamic key schema), the key schema must extend `$ZodRecordKey`, constraining keys to `string | number | symbol`. This is separate from `ZodObject`'s fixed-shape parsing but governs the related `ZodRecord._parse (v3/types.ts:3514)` [SYM] path for open-ended key schemas.

---

## Summary

| Behavior | v3 mechanism | v4 mechanism | Citation |
|---|---|---|---|
| Strip unknown keys (default) | `UnknownKeysParam = "strip"` | `catchall` absent / `ZodNever` | FOCUS SomeZodObject v3; $ZodObjectParams v4 |
| Pass unknown keys through | `UnknownKeysParam = "passthrough"` | `.loose()` → `catchall: $loose` | FOCUS SomeZodObject; source snippet ZodObject.loose |
| Reject unknown keys | `UnknownKeysParam = "strict"` | `catchall` strict variant | FOCUS SomeZodObject v3 |
| Typed unknown keys | `.catchall(schema)` | `catchall: schema` field in params | FOCUS $ZodObjectParams v4 |
| Exact optional fields | n/a | `ZodExactOptional` | source snippet ZodExactOptional classic/schemas.ts:1849 |
| Shape extension / merge | `.extend()` / `.merge()` | `SafeExtendShape<Base, Ext>` | source snippet SafeExtendShape mini/schemas.ts:882 |
| Discriminated union objects | `ZodDiscriminatedUnionOption` | — | FOCUS ZodDiscriminatedUnionOption v3/types.ts:3100 |
