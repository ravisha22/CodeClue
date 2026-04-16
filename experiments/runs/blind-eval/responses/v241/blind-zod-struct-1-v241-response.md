# v2.4.1 Response: blind-zod-struct-1
Date: 2026-04-16

## Package Split Overview

Zod 4 is organized as a three-tier architecture across distinct sub-packages within a single `packages/zod/` directory (TREE: `packages/ (384 files) > bench/ docs/ resolution/ treeshake/ tsc/ zod/`).

### 1. `zod/v4/core` — The Shared Foundation

The `core` layer defines the fundamental schema internals, error types, and parsing infrastructure that both the "full" and "mini" packages build on. Key evidence:

- **Base schema type `$ZodType`**: The `ZodMiniType` interface explicitly `extends: $ZodType` and `uses: core.$ZodType` (FOCUS: `ZodMiniType`, `packages/zod/src/v4/mini/schemas.ts:6-38`). This establishes `$ZodType` from core as the root abstraction.
- **Error types in core**: `$ZodAsyncError.constructor` and `$ZodEncodeError.constructor` both reside in `packages/zod/src/v4/core/core.ts` (SYM: lines 99 and 105 respectively), showing core houses error classes.
- **Check infrastructure**: Every `ZodMini*` type references `core.$Zod*Internals` — e.g., `ZodMiniBoolean extends: $ZodBooleanInternals, uses: core.$ZodBooleanInternals` (FOCUS: `packages/zod/src/v4/mini/schemas.ts:584-588`), `ZodMiniArray extends: $ZodArrayInternals, $ZodArray, uses: core.$ZodArray, core.$ZodArrayInternals` (FOCUS: `packages/zod/src/v4/mini/schemas.ts:783-789`).

### 2. `zod/mini` — Lightweight Schema Surface

The mini package provides a reduced-API surface built on core internals, using interfaces rather than classes with method chains:

- **`ZodMiniType`** serves as the base type with methods `clone`, `parse`, `parseAsync`, `safeParse`, and `check` (FOCUS: `ZodMiniType`, `packages/zod/src/v4/mini/schemas.ts:6-38`). It extends `$ZodType` directly.
- **Primitive schemas**: `_ZodMiniString extends: _ZodMiniType, $ZodString, uses: core.$ZodString` (FOCUS: `packages/zod/src/v4/mini/schemas.ts:80-85`); `_ZodMiniNumber extends: _ZodMiniType, $ZodNumber, uses: core.$ZodNumber` (FOCUS: `packages/zod/src/v4/mini/schemas.ts:517-523`).
- **String format types**: Mini has its own ISO-format schemas that extend `ZodMiniStringFormat` — e.g., `ZodMiniISODate extends: ZodMiniStringFormat, uses: schemas.ZodMiniStringFormat, core.$ZodISODateInternals` (FOCUS: `packages/zod/src/v4/mini/iso.ts:19-23`); similarly `ZodMiniISODateTime` (FOCUS: `packages/zod/src/v4/mini/iso.ts:3-7`), `ZodMiniISOTime` (FOCUS: line 35-39), `ZodMiniISODuration` (FOCUS: line 51-55).
- **`ZodMiniStringFormat`** itself `extends: $ZodStringFormatInternals, $ZodStringFormat, uses: core.$ZodStringFormat, core.$ZodStringFormatInternals` (FOCUS: `packages/zod/src/v4/mini/schemas.ts:103-109`).
- **Composite types**: `ZodMiniUnion extends: $ZodUnionInternals, called_by: union` (FOCUS: `packages/zod/src/v4/mini/schemas.ts:997-1002`); `ZodMiniDiscriminatedUnion extends: ZodMiniUnion` (FOCUS: `packages/zod/src/v4/mini/schemas.ts:1047-1054`); `ZodMiniPipe extends: $ZodPipeInternals` (FOCUS: line 1569-1574); `ZodMiniCodec extends: ZodMiniPipe, $ZodCodec` (FOCUS: line 1594-1601).
- **Wrapper types**: `ZodMiniDefault extends: $ZodDefaultInternals, called_by: _default, uses: core.$ZodType, core.$ZodDefaultInternals` (FOCUS: line 1431-1435); `ZodMiniCatch extends: $ZodCatchInternals, called_by: _catch` (FOCUS: line 1528-1532); `ZodMiniExactOptional extends: $ZodExactOptionalInternals, $ZodExactOptional, called_by: exactOptional` (FOCUS: line 1382-1388).
- **Wide coverage**: Mini exposes types for nearly every data type — `ZodMiniBigInt`, `ZodMiniDate`, `ZodMiniEnum`, `ZodMiniCustom`, `ZodMiniFunction`, `ZodMiniAny`, `ZodMiniBase64`, `ZodMiniBase64URL`, `ZodMiniCIDRv4`, `ZodMiniCIDRv6`, `ZodMiniCUID`, `ZodMiniCUID2`, `ZodMiniEmail`, `ZodMiniEmoji`, `ZodMiniE164`, and more (all documented in FOCUS entries under `packages/zod/src/v4/mini/schemas.ts`).

### 3. `zod` (Full / Classic) — The Feature-Rich Package

The full `zod` package includes the v3 backward-compatible API (class-based with `_parse` methods) alongside a v4 "classic" layer:

- **v3 types**: The monolithic `packages/zod/src/v3/types.ts` (5138 lines per INDEX) contains all v3 schema classes — `ZodString` (class, line 731), `ZodNumber` (class, line 1369), `ZodBigInt` (class, line 1635), etc. (SYM section). Each implements `_parse` and inherits from `ZodType` (SYM: `ZodType._parse` at line 170, `ZodType.constructor` at line 411).
- **v3 uses class-based `_addCheck`**: Methods like `ZodString._addCheck` (line 1050), `ZodNumber._addCheck` (line 1497), `ZodBigInt._addCheck` (line 1749), `ZodDate._addCheck` (line 1943) show the check-registration pattern in v3.
- **v4/classic layer**: Exists in `packages/zod/src/v4/classic/` — the `ZodMiniFunction` FOCUS entry references `core.$ZodFunction` (FOCUS: `packages/zod/src/v4/mini/schemas.ts:1851-1870`), and the `_ZodMiniJSONSchemaInternals` type alias (FOCUS: line 1834) shows JSON schema support.

### Pattern: Core Provides Internals, Mini and Full Provide Surfaces

The consistent pattern is:
- Core defines `$Zod*Internals` interfaces (the internal state/config) and `$Zod*` base types.
- Mini types wrap these with a `ZodMini*` interface that extends the core internals directly.
- The full package provides richer class-based APIs (v3) and interface-based classic wrappers (v4/classic) both consuming core internals.

### What Cannot Be Determined

- **Exact export/entry-point configuration**: The clue file does not show `package.json` exports maps, so the precise import paths consumers use (`zod`, `zod/mini`, `zod/v4/core`) cannot be confirmed — only the source directory layout is visible.
- **Which types are exclusive to each package**: The FOCUS section samples only a subset; 2442+ symbols are truncated (SYM: `...and 2442 more symbols`), so a complete enumeration of what each package exports is not available.
- **Runtime vs. type-only split**: Whether the mini package produces smaller bundles at runtime (tree-shaking behavior) cannot be confirmed from the clue file alone, though the `packages/treeshake/` directory in the TREE hints at tree-shaking tests.
- **The v4/classic layer's full API surface**: Only mini FOCUS entries were provided; the classic/full v4 schemas are not detailed in the FOCUS section for this prompt.
- **How v3 and v4 coexist at runtime**: Whether they share a single `ZodType` root or are completely independent type hierarchies cannot be determined from the clue file alone.
