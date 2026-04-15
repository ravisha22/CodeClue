# v2.3 Response: blind-zod-struct-1
Date: 2026-04-15

## Summary

Zod 4 is organized into three distinct package layers: a shared core (`zod/v4/core`), a full-featured "classic" API (`zod` / `zod/v4/classic`), and a lightweight "mini" API (`zod/mini` / `zod/v4/mini`). The core defines the foundational schema internals (prefixed with `$Zod`), while both full and mini packages define their own user-facing types that extend or use the core types. A legacy v3 layer also coexists in the same repository.

## Detailed Analysis

### Repository Structure (TREE + INDEX)

- The entire codebase lives under `packages/` (384 files), with subdirectories including `bench/`, `docs/`, `resolution/`, `treeshake/`, `tsc/`, and `zod/` (TREE section).
- The Zod source is organized into version-specific paths within `packages/zod/src/`:
  - **v3**: `packages/zod/src/v3/types.ts` (5138L) — the legacy Zod v3 monolithic types file (INDEX).
  - **v4/core**: `packages/zod/src/v4/core/core.ts` — foundational types and constructors (SYM: `$ZodAsyncError.constructor` at `core.ts:99`, `$ZodEncodeError.constructor` at `core.ts:105`).
  - **v4/mini**: `packages/zod/src/v4/mini/schemas.ts` and `packages/zod/src/v4/mini/iso.ts` — the mini package schemas (FOCUS section, many entries).
  - **v4/classic**: Implied by `packages/zod/src/v4/classic/errors.ts` (SYM/FOCUS: `ZodError` at `classic/errors.ts:9-23`).

### The `zod/v4/core` Package

This is the foundational layer. All types here use the `$Zod` prefix convention, indicating internal/core types:

- **`$ZodType`** — the base schema type, referenced extensively. `ZodMiniType` extends it (FOCUS: `ZodMiniType` at `mini/schemas.ts:6-38` — `extends: $ZodType`, `uses: core.$ZodType`).
- **`$ZodString`**, **`$ZodNumber`**, **`$ZodBigInt`**, **`$ZodBoolean`**, etc. — core schema type internals. Mini types reference them via `uses: core.$ZodString`, `core.$ZodNumber`, etc. (FOCUS: `_ZodMiniString` — `uses: core.$ZodString`; `_ZodMiniNumber` — `uses: core.$ZodNumber`).
- **`$ZodArray`**, **`$ZodObject`**, **`$ZodUnion`**, **`$ZodRecord`**, **`$ZodEnum`**, **`$ZodFunction`**, **`$ZodPipe`**, **`$ZodCodec`**, **`$ZodCatch`**, **`$ZodDefault`**, **`$ZodCustom`**, **`$ZodExactOptional`**, **`$ZodIntersection`**, **`$ZodDate`** — all core internals referenced by mini types (FOCUS entries for each `ZodMini*` type cite `core.$Zod*Internals` or `core.$Zod*`).
- **String format internals**: `$ZodStringFormat`, `$ZodStringFormatInternals`, `$ZodCustomStringFormat`, `$ZodCustomStringFormatInternals` — core string validation format types (FOCUS: `ZodMiniStringFormat` — `uses: core.$ZodStringFormat, core.$ZodStringFormatInternals`).
- **ISO date/time internals**: `$ZodISODateTimeInternals`, `$ZodISODateInternals`, `$ZodISOTimeInternals`, `$ZodISODurationInternals` — specialized core types for ISO string formats (FOCUS: `ZodMiniISODateTime`, `ZodMiniISODate`, `ZodMiniISOTime`, `ZodMiniISODuration` each reference these).
- **Error types**: `$ZodAsyncError` and `$ZodEncodeError` in `core/core.ts` (SYM: lines 99 and 105).
- **Check types**: `$ZodCheck`, `CheckFn` — referenced by `ZodMiniType` (FOCUS: `ZodMiniType` — `uses: core.$ZodCheck, core.CheckFn`).

### The `zod/mini` Package

This is a lightweight/tree-shakeable variant. All types use the `ZodMini` prefix and extend core internals:

- **`ZodMiniType`** (`mini/schemas.ts:6-38`) — the base mini schema type. Extends `$ZodType` and provides methods `clone`, `parse`, `parseAsync`, `safeParse` (FOCUS: `ZodMiniType`).
- **Primitive types**:
  - `_ZodMiniString` (`mini/schemas.ts:80-85`) — extends `_ZodMiniType, $ZodString` (FOCUS).
  - `_ZodMiniNumber` (`mini/schemas.ts:517-523`) — extends `_ZodMiniType, $ZodNumber` (FOCUS).
  - `ZodMiniBoolean` (`mini/schemas.ts:584-588`) — extends `$ZodBooleanInternals` (FOCUS).
  - `ZodMiniBigInt` (`mini/schemas.ts:601-605`) — extends `$ZodBigIntInternals, $ZodBigInt` (FOCUS).
  - `ZodMiniDate` (`mini/schemas.ts:765-769`) — extends `$ZodDateInternals` (FOCUS).
- **String format types**:
  - `ZodMiniStringFormat` (`mini/schemas.ts:103-109`) — extends `$ZodStringFormatInternals, $ZodStringFormat` (FOCUS).
  - `ZodMiniCustomStringFormat` (`mini/schemas.ts:469-475`) — extends `ZodMiniStringFormat, $ZodCustomStringFormat` (FOCUS).
  - `ZodMiniEmail` (`mini/schemas.ts:117-119`), `ZodMiniCUID` (`mini/schemas.ts:242-246`), `ZodMiniCUID2` (`mini/schemas.ts:259-263`), etc. (FOCUS).
  - `ZodMiniBase64` (`mini/schemas.ts:406-410`), `ZodMiniBase64URL` (`mini/schemas.ts:422-426`), `ZodMiniE164` (`mini/schemas.ts:438-442`) (FOCUS).
  - `ZodMiniCIDRv4` (`mini/schemas.ts:358-362`), `ZodMiniCIDRv6` (`mini/schemas.ts:375-379`) (FOCUS).
- **Collection types**:
  - `ZodMiniArray` (`mini/schemas.ts:783-789`) — extends `$ZodArrayInternals, $ZodArray` (FOCUS).
  - `ZodMiniObject` (`mini/schemas.ts:814-823`) — extends `$ZodObjectInternals, $ZodObject` (FOCUS).
  - `ZodMiniRecord` (`mini/schemas.ts:1143-1150`) — extends `$ZodRecordInternals` (FOCUS).
  - `ZodMiniEnum` (`mini/schemas.ts:1243-1248`) — extends `$ZodEnumInternals` (FOCUS).
- **Composition types**:
  - `ZodMiniUnion` (`mini/schemas.ts:997-1002`) — extends `$ZodUnionInternals` (FOCUS).
  - `ZodMiniDiscriminatedUnion` (`mini/schemas.ts:1047-1054`) — extends `ZodMiniUnion` (FOCUS).
  - `ZodMiniIntersection` — implied by pattern (not in FOCUS for struct-1 but present in rel-1).
  - `ZodMiniPipe` (`mini/schemas.ts:1569-1574`) — extends `$ZodPipeInternals` (FOCUS).
  - `ZodMiniCodec` (`mini/schemas.ts:1594-1601`) — extends `ZodMiniPipe, $ZodCodec` (FOCUS).
- **Wrapper types**:
  - `ZodMiniDefault` (`mini/schemas.ts:1431-1435`) — extends `$ZodDefaultInternals` (FOCUS).
  - `ZodMiniCatch` (`mini/schemas.ts:1528-1532`) — extends `$ZodCatchInternals` (FOCUS).
  - `ZodMiniCustom` (`mini/schemas.ts:1726-1730`) — extends `$ZodCustomInternals` (FOCUS).
  - `ZodMiniAny` (`mini/schemas.ts:699-703`) — uses `core.$ZodAnyInternals` (FOCUS).
- **Function type**: `ZodMiniFunction` (`mini/schemas.ts:1851-1870`) — extends `$ZodFunctionInternals, $ZodFunction` (FOCUS).
- **ISO types** (in `mini/iso.ts`):
  - `ZodMiniISODateTime` (lines 3-7), `ZodMiniISODate` (lines 19-23), `ZodMiniISOTime` (lines 35-39), `ZodMiniISODuration` (lines 51-55) — all extend `ZodMiniStringFormat` (FOCUS).
- **Internal type aliases**: `_ZodMiniJSONSchemaInternals` (`mini/schemas.ts:1834`) — a type alias for `_ZodMiniJSONSchema["_zod"]` (FOCUS).
- **BigInt format**: `ZodMiniBigIntFormat` (`mini/schemas.ts:618-624`) — uses `core.$ZodBigIntFormatInternals` (FOCUS).

### The `zod` (Full/Classic) Package

The full package appears to be at `packages/zod/src/v4/classic/`:

- **`ZodError`** (`classic/errors.ts:9-23`) — extends `$ZodError` from core. Provides methods `addIssue`, `addIssues`, `flatten`, `format` and uses `z.treeifyError`, `core.$ZodFormattedError`, `core.$ZodIssue`, `core.$ZodFlattenedError` (FOCUS: `ZodError`). This is richer than the core `$ZodError`.

### The Legacy v3 Layer

- `packages/zod/src/v3/types.ts` (5138L) contains the entire v3 type system as a single monolithic file (INDEX).
- v3 types use the `Zod` prefix without `$` or `Mini`: `ZodString`, `ZodNumber`, `ZodBigInt`, `ZodDate`, `ZodBoolean`, `ZodArray`, `ZodObject`, `ZodUnion`, `ZodEnum`, etc. (SYM section — dozens of entries).
- The v3 base type is `ZodType` with methods `_parse`, `constructor`, `_getOrReturnCtx` (SYM: `ZodType._parse` at line 170, `ZodType.constructor` at line 411).
- Each v3 type has its own `_parse` method (SYM: 25+ `_parse` entries) and some have `_addCheck` (SYM: `ZodString._addCheck`, `ZodNumber._addCheck`, `ZodBigInt._addCheck`, `ZodDate._addCheck`).

### Architectural Pattern Summary

| Layer | Path | Type Prefix | Base Type | Role |
|-------|------|-------------|-----------|------|
| Core | `v4/core/` | `$Zod` | `$ZodType` | Shared internals, trait-based |
| Mini | `v4/mini/` | `ZodMini` | `ZodMiniType` (extends `$ZodType`) | Lightweight API |
| Classic/Full | `v4/classic/` | `Zod` | (extends core `$Zod*`) | Full-featured API |
| Legacy v3 | `v3/` | `Zod` | `ZodType` | Backward compatibility |

## Uncertainty / Limits

- **Full/classic schema types**: The FOCUS section for this task heavily covers mini types but provides very little detail on the full/classic package's schema types (only `ZodError` from `classic/errors.ts`). The full package's schema type hierarchy (e.g., `ZodString`, `ZodNumber` for v4 classic) is not documented in this clue file.
- **Re-export / entry point structure**: How `zod`, `zod/mini`, and `zod/v4/core` map to package.json exports or entry points is not available in the clue file.
- **v3 ↔ v4 compatibility layer**: Whether v3 types are re-exported or wrapped by v4 is not clear from the clue file.
- **GAPS**: The clue notes "80 symbols in L3, 0 with behavior annotations" — meaning no behavioral (runtime logic) information is available for the focused symbols; only structural/type relationships are documented.
