# v2.4.1 Response: blind-zod-rel-1
Date: 2026-04-16

## Inheritance and Extension Relationships

The Zod codebase has a layered type hierarchy connecting three tiers: **core** (`zod/v4/core`), **full/classic** (`zod/v4/classic` and `zod/v3`), and **mini** (`zod/v4/mini`). Both the classic and mini surfaces extend core types.

### 1. Core Layer — The Root Abstractions

- **`$ZodType`** (in `packages/zod/src/v4/core/`) is the foundational schema interface. The mini layer's `ZodMiniType` explicitly `extends: $ZodType` (FOCUS: `ZodMiniType`, `packages/zod/src/v4/mini/schemas.ts:6-38`).
- **Core error types**: `$ZodError extends: Error, uses: Symbol.for, zod.error` (FOCUS: `$ZodError`, `packages/zod/src/v4/core/errors.ts:214-217`). `$ZodAsyncError` and `$ZodEncodeError` have constructors in `packages/zod/src/v4/core/core.ts` (SYM: lines 99, 105).
- **Core parse signatures**: `$Parse`, `$ParseAsync`, `$Decode`, `$DecodeAsync`, `$Encode`, `$EncodeAsync` are all generic over `T extends schemas.$ZodType` and use `schemas.ParseContext<errors.$ZodIssue>` (FOCUS entries in `packages/zod/src/v4/core/parse.ts`).
- **StandardSchema compliance**: `$ZodStandardSchema = StandardSchemaV1.Props<core.input<T>, core.output<T>>` (FOCUS: `packages/zod/src/v4/core/schemas.ts:169-170`).

### 2. Classic/Full Layer — Extends Core

- **Classic `ZodAny`** interface: `ZodAny extends _ZodType<core.$ZodAnyInternals>` (snippet: `ZodAny`, `packages/zod/src/v4/classic/schemas.ts L1049-1051`). The `_ZodType<Internals>` generic wrapper binds classic types to core internals.
- **Classic `ZodError`**: `ZodError extends: $ZodError` with methods `addIssue`, `addIssues`, `flatten`, `format` (FOCUS: `ZodError`, `packages/zod/src/v4/classic/errors.ts:9-23`). It `uses: z.treeifyError, core.$ZodFormattedError, core.$ZodIssue, core.$ZodFlattenedError`, showing it wraps core error infrastructure.
- **Classic `ZodStandardSchemaWithJSON`**: Defined in `packages/zod/src/v4/classic/schemas.ts` (FOCUS: lines 12-19, multiple overloads) as `StandardSchemaWithJSONProps<core.input<T>, core.output<T>>`, paralleling the core `$ZodStandardSchema`.
- **Compatibility layer**: `BRAND<T>` lives in `packages/zod/src/v4/classic/compat.ts` (snippet: L40); `inferFlattenedErrors = core.$ZodFlattenedError<core.output<T>, U>` (FOCUS: `packages/zod/src/v4/classic/compat.ts:31`), bridging classic API types to core error types.

### 3. v3 Layer — Independent Class Hierarchy

- **`ZodType`** is the v3 base class with `_parse`, `constructor`, `_getOrReturnCtx` (SYM: lines 170, 411, 176 in `packages/zod/src/v3/types.ts`).
- **v3 schema classes** extend `ZodType` directly — e.g., `ZodAny extends ZodType<any, ZodAnyDef, any>` (snippet: `ZodAnyDef`, L2101-2112).
- **v3 `ZodError`** class `extends: Error` independently, with its own `format`, `flatten`, `formErrors`, `assert`, `constructor` (FOCUS: `ZodError`, `packages/zod/src/v3/ZodError.ts:193-316`).
- **`ZodFirstPartySchemaTypes`** is a union of all v3 types: `| ZodString | ZodNumber | ZodNaN | ZodBigInt | ZodBoolean | ZodDate | ZodUndefined` (FOCUS: L4996-4997).
- **`ZodErrorMap`** in v3: `(issue: ZodIssueOptionalMessage, _ctx: ErrorMapCtx) => { message: string }` (FOCUS: `packages/zod/src/v3/ZodError.ts:329-330`).

### 4. Mini Layer — Parallel Surface on Core

- **`ZodMiniType extends: $ZodType`** with methods `clone, parse, parseAsync, safeParse` and uses `core.$ZodType, core.CheckFn, core.output, core.$ZodCheck` (FOCUS: `packages/zod/src/v4/mini/schemas.ts:6-38`).
- **Mini primitives extend both mini-base and core types**: `_ZodMiniString extends: _ZodMiniType, $ZodString, uses: core.$ZodString` (FOCUS: L80-85); `_ZodMiniNumber extends: _ZodMiniType, $ZodNumber, uses: core.$ZodNumber` (FOCUS: L517-523).
- **Mini composites follow the same pattern**: `ZodMiniArray extends: $ZodArrayInternals, $ZodArray, uses: core.$ZodArray, core.$ZodArrayInternals` (FOCUS: L783-789); `ZodMiniUnion extends: $ZodUnionInternals` (FOCUS: L997-1002); `ZodMiniDiscriminatedUnion extends: ZodMiniUnion` (FOCUS: L1047-1054).
- **Mini wrappers**: `ZodMiniPipe extends: $ZodPipeInternals` (FOCUS: L1569-1574); `ZodMiniCodec extends: ZodMiniPipe, $ZodCodec` (FOCUS: L1594-1601) — showing codec extends pipe within mini.
- **Mini string formats**: `ZodMiniStringFormat extends: $ZodStringFormatInternals, $ZodStringFormat, uses: core.$ZodStringFormat, core.$ZodStringFormatInternals` (FOCUS: L103-109). `ZodMiniCustomStringFormat extends: ZodMiniStringFormat, $ZodCustomStringFormat` (FOCUS: L469-475).

### 5. Cross-Cutting Relationships

- **Core ← Classic**: Classic interfaces use `core.$Zod*Internals` as type parameters (e.g., `ZodAny extends _ZodType<core.$ZodAnyInternals>`).
- **Core ← Mini**: Mini interfaces directly extend `core.$Zod*` and `$Zod*Internals` (e.g., `ZodMiniBigInt extends: $ZodBigIntInternals, $ZodBigInt, uses: core.$ZodBigIntInternals, core.$ZodBigInt` — FOCUS: L601-605).
- **v3 ↔ v4**: The v3 types are a separate class hierarchy. `SafeParseReturnType` in v3 (snippet: L156) uses `SafeParseSuccess` and `SafeParseError` from `packages/zod/src/v4/core/util.ts` (snippets: L180-181), showing some v3-to-v4 type sharing.
- **`Class` abstract base**: An abstract `Class` with `constructor(..._args: any[])` exists in `packages/zod/src/v4/mini/schemas.ts` (snippet: L1781-1785), used for instanceof-based type checking.

### What Cannot Be Determined

- **The exact definition of `_ZodType<Internals>`**: Referenced by classic types but its interface body is not in the FOCUS or snippets.
- **How `_ZodMiniType` relates to `ZodMiniType`**: The `_ZodMiniType` interface (used by `_ZodMiniString`, `_ZodMiniNumber`) is referenced but not shown in FOCUS — its relationship to `ZodMiniType` is unclear.
- **Whether v3 and v4 types share runtime instances**: The clue file shows type-level relationships but not runtime integration.
- **JSON schema generator internals**: Listed as uncovered (GAPS: `JSONSchemaGeneratorParams`, `ToJSONSchemaContext`, `JSONSchemaGenerator.emit`).
- **Full `$ZodError` v4 methods**: Only `$ZodError extends: Error` is shown; the full method set is in the classic `ZodError` wrapper, not in core directly.
- **`StandardSchemaV1` origin**: Referenced by `$ZodStandardSchema` but its definition is external to the clue file.
