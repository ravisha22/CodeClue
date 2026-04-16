# v2.4 Response: blind-zod-struct-1
Date: 2026-04-16

## Question
How is Zod 4 split across the `zod`, `zod/mini`, and `zod/v4/core` packages?

## Answer

### 1. Three-Layer Architecture

The clue file reveals a three-tier package architecture for Zod 4, with `zod/v4/core` serving as the foundational layer, `zod/mini` as a lightweight consumer, and the main `zod` (classic/full) package providing the richest API surface.

### 2. `zod/v4/core` — The Foundation

The core layer lives under `packages/zod/src/v4/core/` and defines the `$`-prefixed base types and internals that both `mini` and `full` packages depend on. Key evidence:

- **`$ZodType`** is the root schema interface used by both mini and classic layers. `ZodMiniType` explicitly `extends: $ZodType` and `uses: core.$ZodType` (`ZodMiniType`, `packages/zod/src/v4/mini/schemas.ts:6-38`).
- Core defines low-level internals like `$ZodString`, `$ZodNumber`, `$ZodBigInt`, `$ZodArray`, `$ZodObject`, `$ZodUnionInternals`, `$ZodPipeInternals`, `$ZodCodec`, `$ZodFunction`, `$ZodCustom`, etc. These are consumed via `core.$...` references by both mini and classic schemas.
- Core also provides error types: `$ZodAsyncError` and `$ZodEncodeError` are classes extending `Error` defined in `packages/zod/src/v4/core/core.ts:97-109`.
- Core owns the ISO-format internals (e.g., `core.$ZodISODateTimeInternals`, `core.$ZodISODateInternals`, `core.$ZodISOTimeInternals`, `core.$ZodISODurationInternals`) used by mini's ISO types (`ZodMiniISODateTime`, `packages/zod/src/v4/mini/iso.ts:3-7`; `ZodMiniISODate`, `packages/zod/src/v4/mini/iso.ts:19-23`; `ZodMiniISOTime`, `packages/zod/src/v4/mini/iso.ts:35-39`; `ZodMiniISODuration`, `packages/zod/src/v4/mini/iso.ts:51-55`).
- Core provides check functionality (`core.CheckFn`, `core.$ZodCheck`) used by `ZodMiniType` (`ZodMiniType`, `packages/zod/src/v4/mini/schemas.ts:6-38`).

### 3. `zod/mini` — Lightweight / Tree-Shakeable Layer

The mini package lives under `packages/zod/src/v4/mini/` and provides a minimal API surface by defining interfaces that extend core internals with a simplified method set:

- **Base type**: `ZodMiniType` extends `$ZodType` and exposes only `clone`, `parse`, `parseAsync`, `safeParse` as methods (`ZodMiniType`, `packages/zod/src/v4/mini/schemas.ts:6-38`). This is a deliberately reduced API compared to the full package.
- **Primitive schemas** extend both a mini base and a core type. For example:
  - `_ZodMiniString extends _ZodMiniType, $ZodString` and `uses: core.$ZodString` (`_ZodMiniString`, `packages/zod/src/v4/mini/schemas.ts:80-85`).
  - `_ZodMiniNumber extends _ZodMiniType, $ZodNumber` and `uses: core.$ZodNumber` (`_ZodMiniNumber`, `packages/zod/src/v4/mini/schemas.ts:517-523`).
- **Compound schemas** wrap core internals directly:
  - `ZodMiniUnion extends $ZodUnionInternals` (`ZodMiniUnion`, `packages/zod/src/v4/mini/schemas.ts:997-1002`).
  - `ZodMiniDiscriminatedUnion extends ZodMiniUnion` and `uses: core.$ZodDiscriminatedUnionInternals` (`ZodMiniDiscriminatedUnion`, `packages/zod/src/v4/mini/schemas.ts:1047-1054`).
  - `ZodMiniObject extends $ZodObjectInternals, $ZodObject` (`ZodMiniObject`, `packages/zod/src/v4/mini/schemas.ts:814-823`).
  - `ZodMiniArray extends $ZodArrayInternals, $ZodArray` (`ZodMiniArray`, `packages/zod/src/v4/mini/schemas.ts:783-789`).
  - `ZodMiniPipe extends $ZodPipeInternals` (`ZodMiniPipe`, `packages/zod/src/v4/mini/schemas.ts:1569-1574`).
  - `ZodMiniCodec extends ZodMiniPipe, $ZodCodec` (`ZodMiniCodec`, `packages/zod/src/v4/mini/schemas.ts:1594-1601`).
  - `ZodMiniFunction extends $ZodFunctionInternals, $ZodFunction` (`ZodMiniFunction`, `packages/zod/src/v4/mini/schemas.ts:1851-1870`).
- **String format types** follow the same pattern: `ZodMiniStringFormat extends $ZodStringFormatInternals, $ZodStringFormat` (`ZodMiniStringFormat`, `packages/zod/src/v4/mini/schemas.ts:103-109`), with concrete formats like `ZodMiniEmail`, `ZodMiniCUID`, `ZodMiniBase64`, etc., each referencing core internals (e.g., `core.$ZodEmailInternals`, `core.$ZodCUIDInternals`, `core.$ZodBase64Internals`).
- **Wrapper types**: `ZodMiniCatch uses: core.$ZodCatchInternals` (`packages/zod/src/v4/mini/schemas.ts:1528-1532`); `ZodMiniDefault uses: core.$ZodDefaultInternals` (`packages/zod/src/v4/mini/schemas.ts:1431-1435`); `ZodMiniCustom uses: core.$ZodCustomInternals` (`packages/zod/src/v4/mini/schemas.ts:1726-1730`).
- Mini schemas are wired to factory functions (`called_by: union`, `called_by: array`, `called_by: looseRecord, partialRecord, record`, `called_by: looseObject, strictObject`, `called_by: discriminatedUnion`, etc.).

### 4. `zod` (Classic/Full) — Feature-Rich Layer

The classic layer exists under `packages/zod/src/v4/classic/` (visible from entries like `packages/zod/src/v4/classic/schemas.ts` and `packages/zod/src/v4/classic/errors.ts` in the FOCUS section). This layer is not directly shown in the struct-1 FOCUS entries but is visible in the SYM section's v3 types. The clue file's GAPS note states there are "80 symbols in L3, 0 with behavior annotations", indicating the full classic layer's internals are not fully covered in this particular clue file.

### 5. Shared v3 Legacy Layer

Alongside v4, the repository retains v3 types in `packages/zod/src/v3/types.ts` (5138 lines), which defines the class-based `ZodType`, `ZodString`, `ZodNumber`, `ZodObject`, etc., with `_parse` methods and class inheritance (`ZodType._parse`, `packages/zod/src/v3/types.ts:170`; `ZodType.constructor`, `packages/zod/src/v3/types.ts:411`).

### 6. Summary of the Split Pattern

| Layer | Location | Base Type | Pattern |
|-------|----------|-----------|---------|
| Core | `packages/zod/src/v4/core/` | `$ZodType` | `$`-prefixed interfaces/internals |
| Mini | `packages/zod/src/v4/mini/` | `ZodMiniType extends $ZodType` | Thin wrappers over core internals |
| Classic | `packages/zod/src/v4/classic/` | (not in this clue) | Richer API surface over core |

The architecture uses a **delegation pattern**: core defines the internal interfaces and logic, mini provides a minimal surface extending core internals, and classic provides the full-featured surface. Both mini and classic depend on core's `$`-prefixed types but offer different API breadths.

### What Cannot Be Determined

- The full classic/`zod` layer's type hierarchy and method surface is not covered in this clue file's FOCUS section; only v3 class-based types and v4 mini types are shown.
- The exact re-export/entry-point structure (how `zod`, `zod/mini` resolve as package imports) is not documented in the clue file.
- Whether the v3 layer is included for backward compatibility or is a separate package entry point cannot be determined.
- The `_ZodMiniJSONSchemaInternals` type (`packages/zod/src/v4/mini/schemas.ts:1834`) hints at JSON schema support in mini but its full structure is not covered.
