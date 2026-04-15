# v2.3 Response: blind-zod-rel-1
Date: 2026-04-15

## Summary

Zod's type hierarchy follows a three-tier architecture: core types (`$Zod*` in `v4/core`) form the foundation, mini types (`ZodMini*` in `v4/mini`) extend core internals for a lightweight API, and full/classic types (`Zod*` in `v4/classic`) also extend core types with richer features. The v3 legacy types form a separate, independent hierarchy. Error types follow the same layered pattern.

## Detailed Analysis

### Core Layer — The Foundation (`packages/zod/src/v4/core/`)

The core layer defines the `$Zod*` prefixed types that serve as the shared foundation:

#### Core Error Types

- **`$ZodError`** (`core/errors.ts:214-217`) — interface extending JavaScript `Error`. Uses `Symbol.for` with `zod.error` (FOCUS: `$ZodError`). This is the base error interface for all of Zod v4.
- **`$ZodError`** (`core/errors.ts:218-227`) — a second entry (likely an overload or declaration merge) also extending `Error` (FOCUS).
- **`$ZodRealError`** (`core/errors.ts:248`) — interface extending `$ZodError` (FOCUS: `$ZodRealError extends: $ZodError`). This is a more concrete error type.
- **`$ZodAsyncError`** (`core/core.ts:97-102`) — extends `Error` directly (not `$ZodError`). Its constructor produces the message "Encountered Promise during synchronous parse. Use .parseAsync() instead." (FOCUS: `$ZodAsyncError extends: Error`).
- **`$ZodEncodeError`** (`core/core.ts:103-109`) — extends `Error` directly. Constructor produces "Encountered unidirectional transform during encode: ${name}" and sets `this.name = "ZodEncodeError"` (FOCUS: `$ZodEncodeError extends: Error`).

#### Core Schema Types (referenced by mini/classic)

The core defines `$ZodType` as the base schema type. All other core schema types provide "internals" interfaces:
- `$ZodString`, `$ZodNumber`, `$ZodBigInt`, `$ZodBoolean`, `$ZodDate`, `$ZodArray`, `$ZodObject`, `$ZodUnion`, `$ZodRecord`, `$ZodEnum`, `$ZodFunction`, `$ZodPipe`, `$ZodCodec`, `$ZodCatch`, `$ZodDefault`, `$ZodCustom`, `$ZodExactOptional`, `$ZodIntersection`, `$ZodStringFormat`, `$ZodCustomStringFormat`, `$ZodAny` — all are referenced via `core.$Zod*` or `core.$Zod*Internals` in the FOCUS entries for mini types.

### Mini Layer — Lightweight API (`packages/zod/src/v4/mini/`)

Mini types use `ZodMini*` prefix and extend core types. The inheritance relationships are:

#### Base Type
- **`ZodMiniType`** (`mini/schemas.ts:6-38`) — `extends: $ZodType`. This is the mini package's root schema type. Methods: `clone`, `parse`, `parseAsync`, `safeParse`. Uses `core.$ZodType`, `core.CheckFn`, `core.output`, `core.$ZodCheck` (FOCUS).

#### Primitive Schema Types
- **`_ZodMiniString`** (`mini/schemas.ts:80-85`) — `extends: _ZodMiniType, $ZodString`. Uses `core.$ZodString` (FOCUS).
- **`_ZodMiniNumber`** (`mini/schemas.ts:517-523`) — `extends: _ZodMiniType, $ZodNumber`. Uses `core.$ZodNumber` (FOCUS).
- **`ZodMiniBoolean`** (`mini/schemas.ts:584-588`) — `extends: $ZodBooleanInternals`. Uses `core.$ZodBooleanInternals` (FOCUS).
- **`ZodMiniBigInt`** (`mini/schemas.ts:601-605`) — `extends: $ZodBigIntInternals, $ZodBigInt`. Uses `core.$ZodBigIntInternals, core.$ZodBigInt` (FOCUS).
- **`ZodMiniDate`** (`mini/schemas.ts:765-769`) — `extends: $ZodDateInternals`. Uses `core.$ZodDateInternals` (FOCUS).

#### String Format Types
- **`ZodMiniStringFormat`** (`mini/schemas.ts:103-109`) — `extends: $ZodStringFormatInternals, $ZodStringFormat`. Uses `core.$ZodStringFormat, core.$ZodStringFormatInternals` (FOCUS).
- **`ZodMiniCustomStringFormat`** (`mini/schemas.ts:469-475`) — `extends: ZodMiniStringFormat, $ZodCustomStringFormat`. Uses `core.$ZodCustomStringFormat, core.$ZodCustomStringFormatInternals` (FOCUS). This shows **dual inheritance**: from both a mini type and a core type.

#### ISO Format Types (mini/iso.ts)
All extend `ZodMiniStringFormat` (the mini string format base):
- **`ZodMiniISODateTime`** (`mini/iso.ts:3-7`) — `extends: ZodMiniStringFormat`. Uses `schemas.ZodMiniStringFormat, core.$ZodISODateTimeInternals` (FOCUS).
- **`ZodMiniISODate`** (`mini/iso.ts:19-23`) — `extends: ZodMiniStringFormat`. Uses `core.$ZodISODateInternals` (FOCUS).
- **`ZodMiniISOTime`** (`mini/iso.ts:35-39`) — `extends: ZodMiniStringFormat`. Uses `core.$ZodISOTimeInternals` (FOCUS).
- **`ZodMiniISODuration`** (`mini/iso.ts:51-55`) — `extends: ZodMiniStringFormat`. Uses `core.$ZodISODurationInternals` (FOCUS).

#### Collection Types
- **`ZodMiniArray`** (`mini/schemas.ts:783-789`) — `extends: $ZodArrayInternals, $ZodArray`. Uses `core.$ZodArray, core.$ZodArrayInternals` (FOCUS).
- **`ZodMiniObject`** (`mini/schemas.ts:814-823`) — `extends: $ZodObjectInternals, $ZodObject`. Uses `core.$ZodObject` (FOCUS).
- **`ZodMiniRecord`** (`mini/schemas.ts:1143-1150`) — `extends: $ZodRecordInternals`. Uses `core.$ZodRecordInternals` (FOCUS).
- **`ZodMiniEnum`** (`mini/schemas.ts:1243-1248`) — `extends: $ZodEnumInternals`. Uses `util.EnumLike, core.$ZodEnumInternals` (FOCUS).

#### Composition Types
- **`ZodMiniUnion`** (`mini/schemas.ts:997-1002`) — `extends: $ZodUnionInternals`. Uses `core.$ZodUnionInternals` (FOCUS).
- **`ZodMiniDiscriminatedUnion`** (`mini/schemas.ts:1047-1054`) — `extends: ZodMiniUnion` (inherits from mini, not core directly). Uses `core.$ZodDiscriminatedUnionInternals` (FOCUS). This is a **mini-to-mini inheritance chain**: `ZodMiniDiscriminatedUnion` → `ZodMiniUnion` → `$ZodUnionInternals` (core).
- **`ZodMiniIntersection`** (`mini/schemas.ts:1079-1084`) — `extends: $ZodIntersectionInternals`. Uses `core.$ZodIntersectionInternals` (FOCUS).

#### Pipeline Types
- **`ZodMiniPipe`** (`mini/schemas.ts:1569-1574`) — `extends: $ZodPipeInternals`. Uses `core.$ZodPipeInternals` (FOCUS).
- **`ZodMiniCodec`** (`mini/schemas.ts:1594-1601`) — `extends: ZodMiniPipe, $ZodCodec`. Uses `core.$ZodCodec, core.$ZodCodecInternals, core.$ZodCodecDef` (FOCUS). This is another **dual inheritance**: both from `ZodMiniPipe` (mini layer) and `$ZodCodec` (core layer).

#### Wrapper Types
- **`ZodMiniDefault`** (`mini/schemas.ts:1431-1435`) — `extends: $ZodDefaultInternals`. Uses `core.$ZodType, core.$ZodDefaultInternals` (FOCUS).
- **`ZodMiniCatch`** (`mini/schemas.ts:1528-1532`) — `extends: $ZodCatchInternals`. Uses `core.$ZodType, core.$ZodCatchInternals` (FOCUS).
- **`ZodMiniExactOptional`** (`mini/schemas.ts:1382-1388`) — `extends: $ZodExactOptionalInternals, $ZodExactOptional`. Uses `core.$ZodExactOptional, core.$ZodExactOptionalInternals` (FOCUS).
- **`ZodMiniCustom`** (`mini/schemas.ts:1726-1730`) — `extends: $ZodCustomInternals`. Uses `core.$ZodCustomInternals` (FOCUS).

#### Function Type
- **`ZodMiniFunction`** (`mini/schemas.ts:1851-1870`) — `extends: $ZodFunctionInternals, $ZodFunction`. Uses `core.$ZodFunction, core.$ZodFunctionDef, core.$InferInnerFunctionType, core.$InferOuterFunctionType` (FOCUS).

### Full/Classic Layer (`packages/zod/src/v4/classic/`)

#### Classic Error Type
- **`ZodError`** (`classic/errors.ts:9-23`) — `extends: $ZodError` (from core). Adds methods: `addIssue`, `addIssues`, `flatten`, `format`. Uses `z.treeifyError`, `core.$ZodFormattedError`, `core.$ZodIssue`, `core.$ZodFlattenedError` (FOCUS). This shows the classic layer **enriches** the core error type with convenience methods.

### v3 Legacy Layer (`packages/zod/src/v3/`)

The v3 layer is structurally independent:

#### v3 Error Types
- **`ZodInvalidIntersectionTypesIssue`** (`v3/ZodError.ts:131-134`) — `extends: ZodIssueBase`. Uses `ZodIssueCode.invalid_intersection_types` (FOCUS). This shows v3 has its own issue type hierarchy extending `ZodIssueBase`.

#### v3 Schema Types
- The v3 schema hierarchy is rooted in `ZodType` (`v3/types.ts`), with all types in a single monolithic file (SYM section, 5138 lines).
- v3 types do NOT extend core `$Zod*` types — they are a separate hierarchy.

### Inheritance Pattern Summary

```
Core Layer ($Zod*):
  Error ← $ZodError ← $ZodRealError
  Error ← $ZodAsyncError
  Error ← $ZodEncodeError
  $ZodType (base schema)

Mini Layer (ZodMini*):
  $ZodType ← ZodMiniType
  _ZodMiniType + $ZodString ← _ZodMiniString
  _ZodMiniType + $ZodNumber ← _ZodMiniNumber
  $ZodUnionInternals ← ZodMiniUnion ← ZodMiniDiscriminatedUnion
  ZodMiniPipe + $ZodCodec ← ZodMiniCodec
  ZodMiniStringFormat ← ZodMiniCustomStringFormat
  ZodMiniStringFormat ← ZodMiniISO{DateTime,Date,Time,Duration}

Classic Layer (Zod*):
  $ZodError ← ZodError (classic)

v3 Layer (separate):
  Error ← ZodError (v3)
  ZodType (independent base)
```

## Uncertainty / Limits

- **Classic schema types**: The FOCUS for this task covers mini and error types extensively but does **not** include classic schema types (e.g., `ZodString`, `ZodNumber` for v4 classic). It is unclear whether classic schema types extend the same core internals pattern as mini types.
- **`_ZodMiniType`**: This type (used in `_ZodMiniString extends: _ZodMiniType`) is not separately defined in the FOCUS. Its relationship to `ZodMiniType` is inferred but not confirmed.
- **No behavior annotations**: GAPS notes "80 symbols in L3, 0 with behavior annotations" — only structural/type relationships are available, not runtime behavior.
- **Mini error handling**: Whether mini types produce `$ZodError` directly or have their own error wrapper is not documented.
