# v2.3 Response: blind-zod-struct-2
Date: 2026-04-15

## Summary

Zod organizes schema types, checks, and errors across three architectural layers — v3 (legacy monolithic), v4/core (shared internals), and v4/classic (user-facing). Schema types define validation structure, checks constrain values, and errors report failures. Each layer has its own file organization with clear naming conventions.

## Detailed Analysis

### Schema Types Organization

#### v3 Schema Types (`packages/zod/src/v3/types.ts`, 5138L)

The legacy v3 layer puts all schema types in a single file:

- **Base type**: `ZodType` with methods `_parse` (line 170), `constructor` (line 411), `_getOrReturnCtx` (line 176) (SYM entries).
- **First-party schema types** are enumerated by the type alias **`ZodFirstPartySchemaTypes`** (`types.ts:4996-4997`): `ZodString | ZodNumber | ZodNaN | ZodBigInt | ZodBoolean | ZodDate | ZodUndefined | ...` (FOCUS: `ZodFirstPartySchemaTypes`). This is a comprehensive union of all built-in schema types.
- **Individual schema classes** (all in `types.ts`): `ZodString` (line 731), `ZodNumber` (line 1369), `ZodBigInt` (line 1635), `ZodArray` (line 2241), `ZodUnion` (line 2947), `ZodIntersection` (line 3292), `ZodRecord` (line 3514), `ZodMap` (line 3603), `ZodSet` (line 3691), `ZodTuple` (line 3399), `ZodEnum` (line 4082), `ZodNativeEnum` (line 4179), `ZodPromise` (line 4244), `ZodEffects` (line 4322), `ZodFunction` (line 3822), `ZodLazy` (line 3979), `ZodLiteral` (line 4007), `ZodOptional` (line 4490), `ZodNullable` (line 4530), `ZodDefault` (line 4569), `ZodCatch` (line 4619), `ZodBranded` (line 4748), `ZodPipeline` (line 4782), `ZodReadonly` (line 4877), and others (SYM entries).
- Each schema type has a **`_parse` method** that implements its validation logic (SYM: 25+ `_parse` entries).
- Several types have **`unwrap`** methods: `ZodBranded.unwrap` (line 4758), `ZodNullable.unwrap` (line 4538), `ZodOptional.unwrap` (line 4498), `ZodReadonly.unwrap` (line 4896), `ZodPromise.unwrap` (line 4240) (SYM entries).
- `Class.constructor` at line 5036 suggests a utility class near the end of the file (SYM).

#### v4/core Schema Types

- Schema types in v4/core use the `$Zod` prefix and are referenced by both mini and classic packages.
- Schemas are defined in `packages/zod/src/v4/core/core.ts` and related modules. The `$ZodType` is the foundational type (referenced by FOCUS: `ZodMiniType` — `extends: $ZodType`).
- Error-related schema types: `$ZodAsyncError` (core.ts:97-102) and `$ZodEncodeError` (core.ts:103-109) both extend `Error` (SYM + FOCUS).

### Checks Organization

#### v3 Checks

- Checks in v3 are embedded within schema types via **`_addCheck`** methods:
  - `ZodString._addCheck` (types.ts:1050), `ZodNumber._addCheck` (types.ts:1497), `ZodBigInt._addCheck` (types.ts:1749), `ZodDate._addCheck` (types.ts:1943) (SYM entries).
- Limit-setting methods: `ZodNumber.setLimit` (types.ts:1482), `ZodBigInt.setLimit` (types.ts:1734) (SYM entries).
- Value accessors: `ZodBigInt.maxValue` (line 1810), `ZodBigInt.minValue` (line 1800), `ZodNumber.maxValue` (line 1587) (SYM entries).

#### v4/core Checks (`packages/zod/src/v4/core/checks.ts`)

- Checks are organized in a dedicated file. Two key type aliases define the check taxonomy:
  - **`$ZodStringFormatChecks`** (`checks.ts:1286`): a union type combining `$ZodCheckRegex | $ZodCheckLowerCase | $ZodCheckUpperCase | $ZodCheckIncludes | $ZodCheckStartsWith | $ZodCheckEndsWith | schemas.$ZodStringFormatTypes` (FOCUS: `$ZodStringFormatChecks`).
  - **`$ZodCheck`** is referenced by `ZodMiniType` (`uses: core.$ZodCheck`) but not directly in the FOCUS for this task.
- The `CheckFn` type is also referenced by `ZodMiniType` (FOCUS: `ZodMiniType` — `uses: core.CheckFn`).

### Errors Organization

#### v3 Errors (`packages/zod/src/v3/ZodError.ts`)

- This is not directly in the FOCUS for struct-2, but is referenced from the INDEX and SYM. The v3 ZodError is a class extending `Error` (see SYM for `$ZodAsyncError` and `$ZodEncodeError` patterns).

#### v4/core Errors (`packages/zod/src/v4/core/errors.ts`)

- **`$ZodError`** (`errors.ts:214-217`): interface extending `Error`, uses `Symbol.for` with identifier `zod.error` (FOCUS: `$ZodError`). This is the core error type.
- **`$ZodRealError`** (`errors.ts:248`): interface extending `$ZodError` — a more concrete error type (FOCUS: `$ZodRealError`).
- **`$ZodAsyncError`** (`core/core.ts:97-102`): extends `Error` directly, for async parse errors (SYM/FOCUS).
- **`$ZodEncodeError`** (`core/core.ts:103-109`): extends `Error` directly, for encode errors (SYM/FOCUS).

#### v4/classic Errors (`packages/zod/src/v4/classic/errors.ts`)

- **`ZodError`** (`classic/errors.ts:9-23`): extends `$ZodError` (from core), adding methods `addIssue`, `addIssues`, `flatten`, `format`. Uses `z.treeifyError`, `core.$ZodFormattedError`, `core.$ZodIssue`, `core.$ZodFlattenedError` (FOCUS: `ZodError`).

### Parse API Organization (`packages/zod/src/v4/core/parse.ts`)

The parsing layer is organized as type aliases in a dedicated file:

- **`$Parse`** (parse.ts:7-9): three overloads of the synchronous parse function type. Signature: `<T extends schemas.$ZodType>(schema: T, value: unknown, _ctx?: schemas.ParseContext<errors.$ZodIssue>, _params?: { callee?: util.AnyFunc; Err?: $ZodErrorClass })` (FOCUS: `$Parse`).
- **`$ParseAsync`** (parse.ts:31-32): async variant (FOCUS: `$ParseAsync`).
- **`$Decode`** (parse.ts:109-110): decode function type taking `core.input<T>` and returning `core.output<T>` (FOCUS: `$Decode`).
- **`$DecodeAsync`** (parse.ts:134-135): async decode variant (FOCUS: `$DecodeAsync`).
- **`$Encode`** (parse.ts:95-97): three overloads, takes `core.output<T>` returns `core.input<T>` (FOCUS: `$Encode`).
- **`$EncodeAsync`** (parse.ts:121-122): async encode variant (FOCUS: `$EncodeAsync`).
- **`$SafeDecode`** (parse.ts:159-160): safe decode returning `util.SafeParseResult` (FOCUS: `$SafeDecode`).
- **`$SafeDecodeAsync`** (parse.ts:184-185): async safe decode (FOCUS: `$SafeDecodeAsync`).
- **`$SafeEncode`** (parse.ts:146-147): safe encode variant (FOCUS: `$SafeEncode`).
- **`$SafeEncodeAsync`** (parse.ts:171): async safe encode (FOCUS: `$SafeEncodeAsync`).

All parse types are parameterized over `schemas.$ZodType` and use `schemas.ParseContext<errors.$ZodIssue>` for context, directly coupling the parse layer to both the schema and error systems.

### Architectural Summary

| Concern | v3 Location | v4/core Location | v4/classic Location |
|---------|-------------|-------------------|---------------------|
| Schema types | `v3/types.ts` (monolithic) | `v4/core/core.ts`, `v4/core/schemas.ts` | `v4/classic/` (extends core) |
| Checks | Embedded in schema `_addCheck` | `v4/core/checks.ts` (dedicated) | Uses core checks |
| Errors | `v3/ZodError.ts` | `v4/core/errors.ts` (`$ZodError`) | `v4/classic/errors.ts` (`ZodError` extends `$ZodError`) |
| Parse API | Built into `ZodType._parse` | `v4/core/parse.ts` (type aliases) | Uses core parse |

## Uncertainty / Limits

- **v3 ZodError details**: The v3 `ZodError.ts` file is listed in the INDEX but its symbols are not prominently featured in this task's FOCUS section. Its internal structure is only partially visible.
- **Check type definitions**: Individual check types (e.g., `$ZodCheckRegex`, `$ZodCheckLowerCase`) are mentioned in the `$ZodStringFormatChecks` union but their individual definitions are not in the FOCUS.
- **Behavioral logic**: GAPS note "80 symbols in L3, 2 with behavior annotations" — meaning almost no runtime behavior information is available; this analysis is structural only.
- **v4/mini errors**: Whether the mini package has its own error types or reuses core `$ZodError` directly is not explicitly stated, though the pattern of mini types using `core.$Zod*` suggests direct reuse.
