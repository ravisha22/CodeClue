# v2.4 Response: blind-zod-rel-1
Date: 2026-04-16

## Question
What inheritance and extension relationships connect Zod's core, full, and mini schema/error types?

## Answer

### 1. Core → Mini Schema Inheritance

The mini layer's types consistently extend core `$`-prefixed interfaces, establishing a clear dependency direction: **core defines internals, mini wraps them**.

#### Base Type Chain
- **`ZodMiniType extends $ZodType`**: The root mini schema interface extends the core base type and adds methods `clone`, `parse`, `parseAsync`, `safeParse`. It `uses: core.$ZodType, core.CheckFn, core.output, core.$ZodCheck` (`ZodMiniType`, `packages/zod/src/v4/mini/schemas.ts:6-38`).

#### Primitive Types (Dual Inheritance)
Mini primitive schemas use **dual inheritance** — extending both a mini base and a core type:
- `_ZodMiniString extends _ZodMiniType, $ZodString` — uses `core.$ZodString` (`_ZodMiniString`, `packages/zod/src/v4/mini/schemas.ts:80-85`).
- `_ZodMiniNumber extends _ZodMiniType, $ZodNumber` — uses `core.$ZodNumber` (`_ZodMiniNumber`, `packages/zod/src/v4/mini/schemas.ts:517-523`).

#### Compound/Wrapper Types (Internals Extension)
- `ZodMiniUnion extends $ZodUnionInternals` — uses `core.$ZodUnionInternals` (`ZodMiniUnion`, `packages/zod/src/v4/mini/schemas.ts:997-1002`).
- `ZodMiniPipe extends $ZodPipeInternals` — uses `core.$ZodPipeInternals` (`ZodMiniPipe`, `packages/zod/src/v4/mini/schemas.ts:1569-1574`).
- `ZodMiniFunction extends $ZodFunctionInternals, $ZodFunction` — uses `core.$ZodFunction` (`ZodMiniFunction`, `packages/zod/src/v4/mini/schemas.ts:1851-1870`).

#### Mini-to-Mini Inheritance
- `ZodMiniDiscriminatedUnion extends ZodMiniUnion` — adds `core.$ZodDiscriminatedUnionInternals` on top of the union base (`ZodMiniDiscriminatedUnion`, `packages/zod/src/v4/mini/schemas.ts:1047-1054`).
- `ZodMiniCodec extends ZodMiniPipe, $ZodCodec` — uses `core.$ZodCodec, core.$ZodCodecInternals, core.$ZodCodecDef` (`ZodMiniCodec`, `packages/zod/src/v4/mini/schemas.ts:1594-1601`).
- `ZodMiniCustomStringFormat extends ZodMiniStringFormat, $ZodCustomStringFormat` — uses `core.$ZodCustomStringFormat, core.$ZodCustomStringFormatInternals` (`ZodMiniCustomStringFormat`, `packages/zod/src/v4/mini/schemas.ts:469-475`).

#### String Format Hierarchy
- `ZodMiniStringFormat extends $ZodStringFormatInternals, $ZodStringFormat` — uses `core.$ZodStringFormat, core.$ZodStringFormatInternals` (`ZodMiniStringFormat`, `packages/zod/src/v4/mini/schemas.ts:103-109`).
- All mini ISO types extend `ZodMiniStringFormat`:
  - `ZodMiniISODateTime extends ZodMiniStringFormat` — uses `core.$ZodISODateTimeInternals` (`packages/zod/src/v4/mini/iso.ts:3-7`).
  - `ZodMiniISODate extends ZodMiniStringFormat` — uses `core.$ZodISODateInternals` (`packages/zod/src/v4/mini/iso.ts:19-23`).
  - `ZodMiniISOTime extends ZodMiniStringFormat` — uses `core.$ZodISOTimeInternals` (`packages/zod/src/v4/mini/iso.ts:35-39`).
  - `ZodMiniISODuration extends ZodMiniStringFormat` — uses `core.$ZodISODurationInternals` (`packages/zod/src/v4/mini/iso.ts:51-55`).

### 2. Core → Classic/Full Schema Inheritance

The classic layer follows a similar pattern, extending core internals:

- **`$ZodStandardSchema`**: typed as `StandardSchemaV1.Props<core.input<T>, core.output<T>>` — the core-level standard schema interface (`$ZodStandardSchema`, `packages/zod/src/v4/core/schemas.ts:169-170`).
- **`ZodStandardSchemaWithJSON`**: the classic layer's extension, typed as `StandardSchemaWithJSONProps<core.input<T>, core.output<T>>` — appears in both `packages/zod/src/v4/classic/schemas.ts:12-18` and `packages/zod/src/v4/core/to-json-schema.ts:582`. This extends the core standard schema with JSON schema support.

### 3. Error Type Inheritance

#### Core Error Types
- **`$ZodError extends Error`** — the base v4 error type, identified via `Symbol.for("zod.error")` (`$ZodError`, `packages/zod/src/v4/core/errors.ts:214-217`).
- **`$ZodRealError extends $ZodError`** — a further specialization in core (`$ZodRealError`, `packages/zod/src/v4/core/errors.ts:248`).
- **`$ZodAsyncError extends Error`** — a standalone error for synchronous parse encountering promises (`$ZodAsyncError`, `packages/zod/src/v4/core/core.ts:97-102`).
- **`$ZodEncodeError extends Error`** — thrown for unidirectional transforms during encode (`$ZodEncodeError`, `packages/zod/src/v4/core/core.ts:103-109`).

#### Classic Error Extension
- **`ZodError extends $ZodError`** — the classic/full layer extends the core error, adding convenience methods: `addIssue`, `addIssues`, `flatten`, `format`. It `uses: z.treeifyError, core.$ZodFormattedError, core.$ZodIssue, core.$ZodFlattenedError` (`ZodError`, `packages/zod/src/v4/classic/errors.ts:9-23`).

#### v3 Error Types (Separate Hierarchy)
- **`ZodError extends Error`** — the v3 error class with methods `constructor`, `errors`, `flatten`, `formErrors`, `format`, `assert`, `isEmpty`, `message`, `toString` (`ZodError`, `packages/zod/src/v3/ZodError.ts:193-316`). This is a **separate class hierarchy** not connected to the v4 `$ZodError`.
- v3 issue types all extend `ZodIssueBase`: `ZodInvalidIntersectionTypesIssue extends ZodIssueBase` (`packages/zod/src/v3/ZodError.ts:131-134`), and similarly for `ZodInvalidTypeIssue`, `ZodInvalidLiteralIssue`, `ZodInvalidUnionIssue`, etc.

### 4. v3 Schema Inheritance (Class-Based)

The v3 layer uses a class-based hierarchy (separate from v4):
- **`ZodType`** is the root class with `_parse`, `constructor`, `_getOrReturnCtx` (`packages/zod/src/v3/types.ts:170, 411, 176`).
- All v3 schemas are classes: `ZodString` (line 731), `ZodNumber` (line 1369), `ZodBigInt` (line 1635), etc., each implementing `_parse`.
- `ZodFirstPartySchemaTypes` enumerates these as a union type (`packages/zod/src/v3/types.ts:4996-4997`).

### 5. Inheritance Diagram

```
Error
├── $ZodAsyncError                    (core/core.ts)
├── $ZodEncodeError                   (core/core.ts)
├── $ZodError                         (core/errors.ts)
│   ├── $ZodRealError                 (core/errors.ts)
│   └── ZodError (classic)            (classic/errors.ts)
└── ZodError (v3)                     (v3/ZodError.ts) — separate hierarchy

$ZodType (core)
├── ZodMiniType (mini)
│   ├── _ZodMiniType
│   │   ├── _ZodMiniString (+ $ZodString)
│   │   └── _ZodMiniNumber (+ $ZodNumber)
│   ├── ZodMiniStringFormat (+ $ZodStringFormatInternals, $ZodStringFormat)
│   │   ├── ZodMiniISODateTime, ZodMiniISODate, ZodMiniISOTime, ZodMiniISODuration
│   │   └── ZodMiniCustomStringFormat (+ $ZodCustomStringFormat)
│   ├── ZodMiniUnion (+ $ZodUnionInternals)
│   │   └── ZodMiniDiscriminatedUnion
│   ├── ZodMiniPipe (+ $ZodPipeInternals)
│   │   └── ZodMiniCodec (+ $ZodCodec)
│   └── ZodMiniFunction (+ $ZodFunctionInternals, $ZodFunction)
└── (classic types extend core internals via _ZodType<core.$...Internals>)
```

### What Cannot Be Determined

- The full classic schema inheritance tree — only a few classic types appear in this clue file's FOCUS section.
- The `$ZodErrorClass` type constructor interface is referenced but its exact relationship to classic vs. mini instantiation is not shown (`$ZodErrorClass`, `packages/zod/src/v4/core/parse.ts:5-6` noted in GAPS as uncovered).
- The `$ZodFlattenedError` type's internal `_FlattenedError<T, U>` definition is not provided (`$ZodFlattenedError`, `packages/zod/src/v4/core/errors.ts:250`).
- Whether the mini layer has its own error type (parallel to classic's `ZodError extends $ZodError`) cannot be determined — no mini error type appears in the clue file.
- The relationship between `ZodStandardSchemaWithJSON` in classic and `$ZodStandardSchema` in core — whether one extends the other or they are parallel — is not explicitly stated.
