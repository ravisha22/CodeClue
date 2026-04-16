# v2.5 Response: blind-zod-rel-1
Date: 2026-04-16

## Question

What inheritance and extension relationships connect Zod's core, full, and mini schema/error types?

---

## Answer

Zod v4 organizes its type system into three layers — **core**, **full (classic)**, and **mini** — connected through a consistent inheritance hierarchy. The relationships flow outward from core, with both classic and mini extending core base types and adding their own API surfaces.

### 1. Error Type Hierarchy

The error system is rooted in `$ZodError`, defined in `v4/core/errors.ts:214-227`. Two interface entries exist for `$ZodError`: one (lines 214-217) extends `Error` and uses `Symbol.for("zod.error")` for runtime identification, and a second (lines 218-227) also extends `Error`, providing the structural contract for error objects.

**Core error types:**

| Type | Location | Extends | Role |
|------|----------|---------|------|
| `$ZodError` | `v4/core/errors.ts:214-227` | `Error` | Base error interface; uses `Symbol.for("zod.error")` for brand checking |
| `$ZodRealError` | `v4/core/errors.ts:248` | `$ZodError` | Concrete error class that fulfills the `$ZodError` contract |
| `$ZodAsyncError` | `v4/core/core.ts:97-102` | `Error` | Thrown when a synchronous parse encounters a Promise (async schema used in sync context) |
| `$ZodEncodeError` | `v4/core/core.ts:103-109` | `Error` | Thrown when attempting to encode through a unidirectional transform |

**Classic (full) error extension:**

- `ZodError` (`v4/classic/errors.ts:9-23`) **extends `$ZodError`** from core. It adds user-facing methods: `addIssue`, `addIssues`, `flatten`, and `format`. This is the primary error type users interact with in the classic API.
- `inferFlattenedErrors` (`v4/classic/compat.ts:31`) references `core.$ZodFlattenedError`, demonstrating that classic's error utilities depend on core's flattened error shape.

**Relationship chain (errors):**

```
Error (built-in)
├── $ZodError (core interface, v4/core/errors.ts:214-227)
│   ├── $ZodRealError (core concrete, v4/core/errors.ts:248)
│   └── ZodError (classic, v4/classic/errors.ts:9-23)
│         └── adds: addIssue, addIssues, flatten, format
├── $ZodAsyncError (core, v4/core/core.ts:97-102) — independent branch
└── $ZodEncodeError (core, v4/core/core.ts:103-109) — independent branch
```

Key observation: `$ZodAsyncError` and `$ZodEncodeError` extend `Error` directly, **not** `$ZodError`. They represent operational failures (wrong parse mode, invalid encode) rather than validation failures, which is why they sit outside the `$ZodError` hierarchy.

### 2. Mini Schema Hierarchy

The mini layer provides a lightweight schema API by extending core's `$ZodType` and mixing in core schema traits.

**Base type:**

- `ZodMiniType` (`v4/mini/schemas.ts:6-38`) **extends `$ZodType`** from core. It provides the mini API surface: `clone`, `parse`, `parseAsync`, `safeParse`. This is the root of all mini schemas.

**Dual-inheritance pattern (mini + core):**

Most mini schemas use dual extension — they extend both `_ZodMiniType` (for mini API) and the corresponding core `$Zod*` type (for core validation logic):

| Mini Type | Location | Extends (mini) | Extends (core) |
|-----------|----------|-----------------|-----------------|
| `_ZodMiniString` | `v4/mini/schemas.ts:80-85` | `_ZodMiniType` | `$ZodString` |
| `_ZodMiniNumber` | `v4/mini/schemas.ts:517-523` | `_ZodMiniType` | `$ZodNumber` |
| `ZodMiniObject` | `v4/mini/schemas.ts:814-823` | `ZodMiniType` | `$ZodObject` |
| `ZodMiniFunction` | `v4/mini/schemas.ts:1851-1870` | `_ZodMiniType` | `$ZodFunction` |
| `ZodMiniOptional` | `v4/mini/schemas.ts:1360-1366` | `_ZodMiniType` | `$ZodOptional` |
| `ZodMiniExactOptional` | `v4/mini/schemas.ts:1382-1388` | `_ZodMiniType` | `$ZodExactOptional` |

**Single-inheritance mini types (no core dual-extend):**

Some mini types extend only `_ZodMiniType` without a second core parent:

- `ZodMiniUnion` (`v4/mini/schemas.ts:997-1002`) — extends `_ZodMiniType` only
- `ZodMiniRecord` (`v4/mini/schemas.ts:1143-1150`) — extends `_ZodMiniType` only
- `ZodMiniEnum` (`v4/mini/schemas.ts:1243-1248`) — extends `_ZodMiniType` only
- `ZodMiniNullable` (`v4/mini/schemas.ts:1404-1409`) — extends `_ZodMiniType` only

**Mini sub-hierarchies:**

- `ZodMiniDiscriminatedUnion` (`v4/mini/schemas.ts:1047-1054`) extends `ZodMiniUnion` — a refinement within the mini layer itself.
- `ZodMiniStringFormat` (`v4/mini/schemas.ts:103-109`) extends both `_ZodMiniString` and `$ZodStringFormat`, creating a three-level chain: `_ZodMiniType` → `_ZodMiniString` → `ZodMiniStringFormat`.
- `ZodMiniISO*` types extend `ZodMiniStringFormat`, adding a fourth level for specific ISO format validators.

### 3. Full/Classic Schema Layer

The classic layer connects to core primarily through **type aliases** rather than direct class extension:

- `ZodStandardSchemaWithJSON` is defined in `v4/classic/schemas.ts:12-19` (multiple entries), serving as a type alias that wraps core schema types with classic API conveniences.
- Classic schemas use core internals through these aliases, meaning the classic API surface is layered on top of core without deep class hierarchies of its own.

### 4. V3 Legacy Types

The v3 layer (`v3/types.ts`) uses a separate, self-contained hierarchy:

- `ZodType._parse` (`v3/types.ts:170`) is the base class with the `_parse` method as the extension point.
- `ZodString`, `ZodNumber`, `ZodBigInt`, etc. are concrete classes in `v3/types.ts`, each implementing their own `_parse` method.

V3 types do **not** extend v4 core types — they are an independent hierarchy.

### 5. Structural Summary

```
$ZodType (v4/core)
├── ZodMiniType (v4/mini/schemas.ts:6-38)
│   ├── _ZodMiniString + $ZodString (dual)
│   │   └── ZodMiniStringFormat + $ZodStringFormat
│   │       └── ZodMiniISO* types
│   ├── _ZodMiniNumber + $ZodNumber (dual)
│   ├── ZodMiniObject + $ZodObject (dual)
│   ├── ZodMiniFunction + $ZodFunction (dual)
│   ├── ZodMiniOptional + $ZodOptional (dual)
│   ├── ZodMiniExactOptional + $ZodExactOptional (dual)
│   ├── ZodMiniUnion (mini-only)
│   │   └── ZodMiniDiscriminatedUnion
│   ├── ZodMiniRecord (mini-only)
│   ├── ZodMiniEnum (mini-only)
│   └── ZodMiniNullable (mini-only)
├── [Classic schemas via type aliases: ZodStandardSchemaWithJSON etc.]
└── [Core $Zod* types: $ZodString, $ZodNumber, $ZodObject, ...]

ZodType (v3/types.ts:170) — independent legacy hierarchy
├── ZodString, ZodNumber, ZodBigInt, ... (each with _parse)
```

### 6. Identified Gaps

- **MECHANISTIC**: The body logic of how dual inheritance is resolved at runtime (e.g., method resolution order between `_ZodMiniType` and `$ZodString`) is not covered by the clue entries. Understanding the actual mixin/trait application mechanism requires examining function bodies.
- **Uncovered types**: `$ZodErrorClass` (constructor pattern for errors, referenced in `v4/core/parse.ts:5-6`) and `$ZodFlattenedError` (aliased in `v4/core/errors.ts:250-254` as `_FlattenedError<T, U>`) were noted in clues but their internal structure is not fully detailed.
