# Scaffold (Sonnet 4.6): blind-zod-mech-1
Date: 2026-04-16

## Question

What exact unknown-key and object-composition behaviors does Zod apply when parsing object schemas?

## Reasoning Scaffold

### 1. Relevant Symbols from FOCUS, SYM, INDEX

**Unknown-key handling symbols:**

- **`UnknownKeysParam`** — Referenced as a type parameter in the `SomeZodObject` type alias: `ZodObject<ZodRawShape, UnknownKeysParam, ZodTypeAny>` (FOCUS: SomeZodObject, packages/zod/src/v3/types.ts:2418). This is the generic parameter that governs how unrecognized keys are treated during object parsing.
- **`ZodObject.loose()`** — Source snippet (packages/zod/src/v4/classic/schemas.ts L1193): `loose(): ZodObject<Shape, core.$loose>`. Returns a new `ZodObject` parameterized with `core.$loose`, indicating a mode where unknown keys are allowed and passed through.
- **`$ZodObjectParams`** — FOCUS (packages/zod/src/v4/core/api.ts:1161): `TypeParams<schemas.$ZodObject, "shape" | "catchall">`. The two configurable axes of an object schema are its **shape** (the known key–schema mapping) and its **catchall** (a schema applied to any key not in the shape).
- **`$ZodObjectConfig`** — FOCUS (packages/zod/src/v4/core/schemas.ts:1749): `{ out: Record<string, unknown>; in: Record<string, unknown> }`. The config tracks separate input and output record types, supporting transforms where the parsed output type differs from the input type.

**Object-composition symbols:**

- **`SafeExtendShape`** — Source snippet (packages/zod/src/v4/mini/schemas.ts L882): `SafeExtendShape<Base extends core.$ZodShape, Ext extends core.$ZodLooseShape>`. A type-level utility for safely merging two object shapes, where the extension shape uses `$ZodLooseShape` (a more permissive shape type) overlaid onto a strict `$ZodShape` base.
- **`ZodIntersection._parse`** — SYM (packages/zod/src/v3/types.ts:3292). The intersection schema has its own `_parse` method, meaning object intersections are resolved at the parse level, not merely at the type level.
- **`ZodDiscriminatedUnion`** — Source snippet (packages/zod/src/v4/classic/schemas.ts L1379-1389): extends `ZodUnion<Options>` and `core.$ZodDiscriminatedUnion<Options, Disc>`. This is the optimized union variant for objects sharing a discriminator key.
- **`ZodDiscriminatedUnionOption`** — FOCUS (packages/zod/src/v3/types.ts:3100-3101): `ZodObject<{ [key in Discriminator]: ZodTypeAny } & ZodRawShape, ...>`. Each option in a discriminated union must be a `ZodObject` whose shape includes the discriminator key mapped to a `ZodTypeAny`.

### 2. Tracing Call Chains and Extends Hierarchies

**Unknown-key resolution path (v3):**

The `SomeZodObject` alias (FOCUS) reveals the three generic parameters of `ZodObject`: the raw shape, the `UnknownKeysParam`, and a catchall type. When `ZodObject._parse` executes (SYM: ZodType._parse at types.ts:170 is the base; ZodObject would override it), it must consult `UnknownKeysParam` to decide the fate of keys present in input but absent from the shape.

The v3 `UnknownKeysParam` is a type-level discriminant. Based on Zod's well-known API surface and the structural evidence here, the three modes are:
- **strip** (default): unknown keys are silently removed from the output.
- **strict**: unknown keys cause a validation error.
- **passthrough**: unknown keys are preserved in the output as-is.

**Unknown-key resolution path (v4):**

In v4, the architecture shifts. `$ZodObjectParams` (FOCUS) parameterizes object schemas on `"shape" | "catchall"` rather than an `UnknownKeysParam` enum. This means unknown-key behavior in v4 is governed by the **catchall schema**:
- No catchall (or a stripping catchall): unknown keys are stripped — equivalent to v3 `strip`.
- A catchall set to a permissive schema (e.g., `z.unknown()`): unknown keys pass through — equivalent to v3 `passthrough`.
- The `ZodObject.loose()` method (source snippet, L1193) is the API for switching to permissive mode, returning `ZodObject<Shape, core.$loose>`. The `core.$loose` type parameter encodes the passthrough/loose behavior at the type level.
- A catchall set to `z.never()` or equivalent: unknown keys trigger errors — equivalent to v3 `strict`.

This is a significant architectural change: v4 unifies the unknown-key policy into the catchall mechanism rather than maintaining a separate enum.

**Object-composition chains:**

- **`SafeExtendShape<Base, Ext>`** (source snippet) operates at the type level to merge shapes. The asymmetry is notable: `Base` must be `core.$ZodShape` (strict), while `Ext` can be `core.$ZodLooseShape` (permissive). This means when extending/merging objects, the extension shape is allowed to contain keys with looser typing constraints than the base, and the merge produces a combined shape where extension keys override base keys of the same name.
- **`ZodIntersection._parse`** (SYM, types.ts:3292) handles runtime intersection. Unlike `.extend()` or `.merge()` which produce a new `ZodObject`, `ZodIntersection` parses the input against both constituent schemas independently and then merges the results. This is a parse-time operation, not a shape-merge.
- **`ZodDiscriminatedUnion`** (source snippet) extends `ZodUnion` (inheriting union parse logic) but adds the `Disc` type parameter and `$ZodDiscriminatedUnionInternals`. The discriminated variant can look up the correct branch by reading the discriminator key first, avoiding the need to try-parse against every option. Each option is constrained to be a `ZodObject` whose shape includes the discriminator (FOCUS: `ZodDiscriminatedUnionOption`).

### 3. Behavior Annotations and Source Snippet Analysis

**Critical observation from GAPS:** The clue file explicitly states `0 with behavior annotations` out of 80 symbols at L3 coverage. This means **no runtime behavior is directly annotated** — all FOCUS entries are type aliases and type-level definitions. The mechanistic parse-time behavior (what actually happens to unknown keys, how merge conflicts resolve, what errors are emitted) must be inferred from type signatures, method existence, and structural clues rather than from direct behavioral documentation.

**From source snippets confirmed:**

1. **`ZodObject.loose()`** (L1193) — The return type `ZodObject<Shape, core.$loose>` confirms that looseness is encoded as a type parameter, and the method returns `this`-like (same shape, different unknown-key policy). This is a non-destructive transformation: it does not alter the shape, only the unknown-key handling mode.

2. **`ZodExactOptional`** (source snippet, L1849-1856) — A separate schema type for "exact optional" semantics, wrapping an inner type `T`. This distinguishes between `undefined`-valued keys and truly absent keys in the parsed output, which is relevant to object-composition behavior: when merging shapes, the exact-optional vs. regular-optional distinction affects whether a missing key produces `undefined` or is omitted entirely.

3. **`ZodDefault`** and **`ZodCatch`** (source snippets, L1904-1913, L2016-2025) — Both wrap inner schemas and provide `unwrap()`. These are relevant to object-composition because when a default-wrapped or catch-wrapped schema appears in an object shape, the object parser must delegate to these wrappers, which supply fallback values before the object-level unknown-key logic applies.

### 4. Module Context from TREE/INDEX

- **v3 path** (`packages/zod/src/v3/types.ts`, 5138 lines): A monolithic file containing all schema types. `ZodObject`, `ZodIntersection`, `ZodUnion`, `ZodRecord`, etc., are all co-located. The `_parse` methods (SYM) are instance methods on each class.
- **v4 path** is split across:
  - `packages/zod/src/v4/core/schemas.ts` — Core schema implementations (`$ZodObject`, `$ZodObjectConfig`, `$ZodRecordKey`).
  - `packages/zod/src/v4/core/api.ts` — Parameter types for schema construction (`$ZodObjectParams`, `$ZodRecordParams`).
  - `packages/zod/src/v4/classic/schemas.ts` — Classic API surface (`ZodObject`, `ZodArray`, `ZodDefault`, etc.).
  - `packages/zod/src/v4/mini/schemas.ts` — Minimal/tree-shakeable API (`SafeExtendShape`).
  - `packages/zod/src/v4/core/parse.ts` — The `$Parse` type alias: `<T extends schemas.$ZodType>(schema: T, value: unknown, _ctx?, _params?) => ...` (FOCUS).

This modular split suggests v4's parse logic is centralized in `core/parse.ts` with schema-specific behavior delegated via the schema's internal configuration (shape + catchall), rather than v3's per-class `_parse` override pattern.

### 5. GAPS Analysis

The GAPS section states:
- **Type: MECHANISTIC** — body logic is needed for a full answer. The clue file does not contain the actual parse-time code that implements unknown-key stripping, error raising, or passthrough.
- **Coverage: 80 symbols in L3, 0 with behavior annotations** — We have type-level structure but no runtime behavior documentation.
- **Uncovered: `$InferZodRecordInput x4`** — The record input inference type appears four times but is not covered, suggesting complex record-key inference logic exists that interacts with object schemas.
- **Drill: `ZodObject.loose` (~1 line)** — The drill target is precisely the `loose()` method, confirming the clue author identified this as the key gap for understanding unknown-key behavior.

### 6. Synthesis

**Supported conclusions (with citations):**

1. **Zod v3 objects are parameterized on three axes**: raw shape, unknown-keys policy (`UnknownKeysParam`), and catchall type (`ZodTypeAny`). (FOCUS: `SomeZodObject`, types.ts:2418)

2. **Zod v4 objects collapse unknown-key policy into two axes**: `"shape"` and `"catchall"`. (FOCUS: `$ZodObjectParams`, api.ts:1161). The `UnknownKeysParam` enum is replaced by the catchall schema mechanism.

3. **`ZodObject.loose()` is the v4 API for permissive unknown-key handling**, returning a `ZodObject<Shape, core.$loose>`. (Source snippet: classic/schemas.ts L1193). This is a type-safe, non-destructive mode switch.

4. **Object composition via `SafeExtendShape` allows asymmetric shape merging**: the base must be strict (`$ZodShape`) while the extension can be loose (`$ZodLooseShape`), enabling extension keys to override base keys with broader types. (Source snippet: mini/schemas.ts L882)

5. **`ZodIntersection._parse` performs runtime intersection** at parse time, not just type-level merging. (SYM: types.ts:3292). Both schemas are parsed against the input, and results are merged.

6. **Discriminated unions constrain options to `ZodObject` schemas** with a required discriminator key in their shape. (FOCUS: `ZodDiscriminatedUnionOption`, types.ts:3100-3101). This enables O(1) branch selection by discriminator value rather than O(n) try-parsing.

7. **`ZodExactOptional` distinguishes missing keys from `undefined` values** in object shapes. (Source snippet: classic/schemas.ts L1849-1856). This affects composition behavior when merging shapes with optional properties.

**Uncertainty (what we cannot confirm from clues alone):**

- The **exact runtime behavior** of unknown-key stripping, error messages for strict mode, and passthrough mechanics — no `_parse` method bodies are provided (GAPS: MECHANISTIC, 0 behavior annotations).
- How **catchall schemas interact with unknown keys at parse time** in v4 — we know `catchall` is a configuration axis ($ZodObjectParams), but the parse-time delegation logic is not shown.
- Whether v4's `core.$loose` is literally implemented as a specific catchall schema (e.g., `z.unknown()`) or as a separate flag — the type parameter `core.$loose` is referenced but not defined in the clues.
- The **merge conflict resolution strategy** in `ZodIntersection._parse` — whether it favors the first or second schema, whether it deep-merges nested objects, or whether conflicting values produce errors.
- The behavior of `$InferZodRecordInput` (GAPS: uncovered x4) and how record-key inference interacts with object unknown-key handling.
- The full body of `SafeExtendShape` (source snippet: signature only, body truncated) — we cannot confirm the exact merge semantics beyond the type-level constraint.
