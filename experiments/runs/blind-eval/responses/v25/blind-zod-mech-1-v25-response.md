# v2.5 Response: blind-zod-mech-1
Date: 2026-04-16

## Question

What exact unknown-key and object-composition behaviors does Zod apply when parsing object schemas?

---

## Answer

### 1. Object Schema Foundation

Zod provides two object schema implementations across its module structure:

- **ZodObject** (`v4/classic/schemas.ts:1176-1255`): Extends `_ZodType` and `$ZodObject`. Exposes the full surface of object-manipulation methods: `catchall`, `extend`, `keyof`, `loose`, `merge`, `passthrough`, `strict`, `strip`. Internally delegates to `looseObject` and `strictObject` factory functions and references `core.$ZodObject`, `util.ToEnum`, `core.SomeType`, and `core.$catchall`.

- **ZodMiniObject** (`v4/mini/schemas.ts:814-823`): Extends `ZodMiniType` and `$ZodObject`. A lighter variant also constructed via `looseObject` and `strictObject`.

Both schemas share the underlying core type:

- **$ZodObjectConfig** (`v4/core/schemas.ts:1748-1749`): Defined as `{ out: Record<string, unknown>; in: Record<string, unknown> }`, establishing that the object schema fundamentally operates over open records of unknown values at the type level.

- **$ZodObjectParams** (`v4/core/api.ts:1161-1162`): Defined as `TypeParams<schemas.$ZodObject, "shape" | "catchall">`, confirming that the two key structural parameters of an object schema are its `shape` (the known-property map) and its `catchall` (the schema applied to unknown keys).

### 2. Unknown-Key Handling

The clue evidence identifies four methods on `ZodObject` that control how unrecognized keys in input data are treated:

| Method | Behavior (per clue evidence) |
|---|---|
| `strip()` | Default. Removes unknown keys from the parsed output. |
| `strict()` | Rejects input containing unknown keys (produces an error). |
| `passthrough()` | Allows unknown keys through to the output unmodified. |
| `loose()` | Returns `ZodObject<Shape, core.$loose>` — changes the `Config` type parameter to `core.$loose`, indicating a permissive unknown-key policy at the type level. |

**Evidence for the mode taxonomy:**

- **UnknownKeysParam** (`v3/types.ts:2368-2370`): Source snippet shows the type is `"passthrough" | "strict" | "strip"` — an exhaustive enum of the three v3 modes.
- **SomeZodObject** (`v3/types.ts:2418`): Defined as `ZodObject<ZodRawShape, UnknownKeysParam, ZodTypeAny>`, showing that `UnknownKeysParam` is a first-class generic parameter of every v3 object schema.
- **ZodObject.loose()** source: Returns `ZodObject<Shape, core.$loose>`, demonstrating that in v4 the unknown-key policy is encoded via the `Config` type parameter rather than a string union.

**Catchall interaction:**

The `catchall` method (listed in ZodObject's method set) and the `core.$catchall` reference suggest that when a catchall schema is specified, unknown keys are parsed through it rather than being stripped or rejected. This provides a fourth handling path beyond the three `UnknownKeysParam` modes: unknown keys are validated against the catchall schema and, if valid, included in the output.

**Related types for unknown values:**

- **ZodUnknown** (`v4/classic/schemas.ts:1061-1063`): Extends `_ZodType`, uses `core.$ZodUnknownInternals` — represents the `unknown` type itself (not object unknown keys).
- **ZodMiniUnknown** (`v4/mini/schemas.ts:713-717`): Mini variant, same internals.

### 3. Object Composition

Two primary composition mechanisms are evidenced:

#### 3a. `extend`

- **ZodObject.extend** (`v4/classic/schemas.ts:1201`): Source snippet:
  ```typescript
  extend<U extends core.$ZodLooseShape>(shape: U): ZodObject<util.Extend<Shape, U>, Config>
  ```
  This shows:
  - The extension shape `U` must conform to `core.$ZodLooseShape` (a shape where values are any Zod type, not necessarily matching the base shape's constraints).
  - The result type uses `util.Extend<Shape, U>`, which merges the base shape with the extension, with `U` properties overriding `Shape` properties on collision.
  - The `Config` type parameter is preserved — the unknown-key mode of the original schema carries through to the extended schema.

- **SafeExtendShape** (`v4/mini/schemas.ts:882`): Source defines:
  ```typescript
  type SafeExtendShape<Base extends core.$ZodShape, Ext extends core.$ZodLooseShape>
  ```
  This type-level utility constrains the extension to be safe, ensuring that the `Ext` shape uses `$ZodLooseShape` (allowing any Zod type) while the `Base` uses the stricter `$ZodShape`.

#### 3b. `merge`

- `merge` is listed among ZodObject's methods (`v4/classic/schemas.ts:1176-1255`). While no source snippet for the implementation body is available, merge semantics in Zod typically combine two object schemas, producing a new schema whose shape is the union of both shapes (with the second schema's properties taking precedence).

#### 3c. Optional Properties

- **ZodExactOptional** (`v4/classic/schemas.ts:1849-1856`): Extends `_ZodType` and `$ZodExactOptional`. This handles the distinction between a property being absent vs. being explicitly `undefined` — relevant when composing objects with optional fields.
- **ZodMiniExactOptional** (`v4/mini/schemas.ts:1382-1388`): Mini variant with the same base type.

#### 3d. Record and Map Schemas

- **$ZodRecordKey** (`v4/core/schemas.ts:2684-2691`): Defined as `$ZodType<string | number | symbol, unknown>` — constrains record keys to string, number, or symbol types.
- **$ZodRecordParams** and **$ZodMapParams** are referenced in `v4/core/api.ts`, providing parameterized construction for record and map schemas which represent alternative object-like compositions.

### 4. Discriminated Unions (Object-Level Composition)

- **ZodDiscriminatedUnionOption** (`v3/types.ts:3100`): Defined as `ZodObject<{[key in Discriminator]: ZodTypeAny} & ZodRawShape>`, showing that each branch of a discriminated union must be a ZodObject with at least the discriminator key present in its shape. This is a constrained form of object composition used for tagged unions.

### 5. Identified Gaps

| Gap Category | Details |
|---|---|
| **$InferZodRecordOutput** | Not covered — the inferred output type for record schemas is unknown. |
| **KeySchema** | Not covered — how key schemas interact with object parsing is not traced. |
| **SomeObject** | Not covered — this utility type's role in composition is undetermined. |
| **Runtime parsing behavior** | The exact runtime execution of `loose`/`strict`/`strip`/`passthrough` during `parse()` cannot be fully traced from the clue data. The type-level signatures are clear, but the imperative logic (e.g., iteration over input keys, deletion of unknown keys, error accumulation for strict mode) is not captured in the available source snippets. |

---

## Summary

Zod object schemas use a `Config` type parameter (v4) or `UnknownKeysParam` string union (v3) to encode one of four unknown-key policies: **strip** (default, remove unknowns), **strict** (error on unknowns), **passthrough** (keep unknowns), and **catchall** (validate unknowns against a sub-schema). Object composition is achieved via `extend` (merges shapes with `util.Extend`, preserving config) and `merge` (combines two object schemas). Optional property handling is explicit via `ZodExactOptional` / `ZodMiniExactOptional`, distinguishing absent from undefined.
