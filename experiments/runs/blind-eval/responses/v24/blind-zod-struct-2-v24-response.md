# v2.4 Response: blind-zod-struct-2
Date: 2026-04-16

## Question
How are schema types, checks, and errors organized in Zod's documented internal architecture?

## Answer

### 1. Schema Type Organization

#### v3 Schema Types (Class-Based)
The v3 layer in `packages/zod/src/v3/types.ts` (5138 lines) uses a **class hierarchy** rooted in `ZodType`. Every schema is a class extending `ZodType` with a `_parse` method:

- **Base**: `ZodType` defines `_parse`, `constructor`, `_getOrReturnCtx` (`ZodType._parse`, `packages/zod/src/v3/types.ts:170`; `ZodType.constructor`, `packages/zod/src/v3/types.ts:411`).
- **Concrete types**: `ZodString` (line 731), `ZodNumber` (line 1369), `ZodBigInt` (line 1635), `ZodDate` (line 1878), `ZodBoolean` (line 1834), `ZodArray` (line 2241), `ZodObject` (via `SomeZodObject`, `packages/zod/src/v3/types.ts:2418`), `ZodUnion` (line 2947), `ZodEnum` (line 4082), `ZodEffects` (line 4322), `ZodPipeline` (line 4782), and many more—each with its own `_parse` method.
- **`ZodFirstPartySchemaTypes`** enumerates all built-in schema types as a union: `| ZodString | ZodNumber | ZodNaN | ZodBigInt | ZodBoolean | ZodDate | ZodUndefined` and more (`ZodFirstPartySchemaTypes`, `packages/zod/src/v3/types.ts:4996-4997`).
- **Helper types**: `UnknownKeysParam = "passthrough" | "strict" | "strip"` for object key handling (`UnknownKeysParam`, `packages/zod/src/v3/types.ts:2368-2370`); `ParseInputLazyPath` for lazy path construction (`ParseInputLazyPath`, `packages/zod/src/v3/types.ts:61-85`).

#### v4 Schema Types (Interface-Based)
The v4 architecture splits into core, classic, and mini layers:

- **Core**: defines `$`-prefixed types like `$ZodType`, plus internals such as `$ZodArrayInternals`, `$ZodObjectInternals`, `$ZodUnionInternals`, `$ZodPipeInternals`, `$ZodCodecInternals`, `$ZodCustomInternals`, etc. (referenced throughout the FOCUS entries via `core.$...` prefixes).
- **Classic** (`packages/zod/src/v4/classic/schemas.ts`): defines user-facing types like `ZodArray` extending `_ZodType<core.$ZodArrayInternals<T>>` and `core.$ZodArray<T>` with methods like `min`, `max`, `length`, `nonempty`, `unwrap` (`ZodArray`, `packages/zod/src/v4/classic/schemas.ts:1127-1140`). Similarly: `ZodAny extends _ZodType<core.$ZodAnyInternals>` (`packages/zod/src/v4/classic/schemas.ts:1049-1051`); `ZodCustom extends _ZodType<core.$ZodCustomInternals>` (`packages/zod/src/v4/classic/schemas.ts:2284-2290`); `ZodDefault`, `ZodCatch`, `ZodCodec`, `ZodDiscriminatedUnion`, `ZodEnum`, `ZodFile`, `ZodFunction`, `ZodExactOptional`, and many string format types.
- **Standard Schema**: Classic types include `"~standard": ZodStandardSchemaWithJSON<this>` properties, typed as `StandardSchemaWithJSONProps<core.input<T>, core.output<T>>` (`ZodStandardSchemaWithJSON`, `packages/zod/src/v4/classic/schemas.ts:12-18`).

### 2. Check Organization

#### v3 Checks
In v3, checks are added via `_addCheck` methods on individual schema classes:
- `ZodString._addCheck` (`packages/zod/src/v3/types.ts:1050`)
- `ZodNumber._addCheck` (`packages/zod/src/v3/types.ts:1497`)
- `ZodBigInt._addCheck` (`packages/zod/src/v3/types.ts:1749`)
- `ZodDate._addCheck` (`packages/zod/src/v3/types.ts:1943`)

These are schema-specific; each type implements its own check addition.

#### v4 Checks (Centralized)
The v4 core centralizes checks in `packages/zod/src/v4/core/checks.ts`:

- **`$ZodStringFormatChecks`**: a union of `$ZodCheckRegex | $ZodCheckLowerCase | $ZodCheckUpperCase | $ZodCheckIncludes | $ZodCheckStartsWith | $ZodCheckEndsWith | schemas.$ZodStringFormatTypes` (`$ZodStringFormatChecks`, `packages/zod/src/v4/core/checks.ts:1286`).
- **`$ZodCheckPropertyParams`**: parameterized as `CheckParams<checks.$ZodCheckProperty, "property" | "schema" | "when">` (`$ZodCheckPropertyParams`, `packages/zod/src/v4/core/api.ts:1082-1083`).
- Classic schemas expose check-aware methods, e.g., `ZodArray.min(minLength, params?: string | core.$ZodCheckMinLengthParams)`, `ZodArray.max(...)`, `ZodArray.length(...)` (`ZodArray`, `packages/zod/src/v4/classic/schemas.ts:1127-1140`).

### 3. Parse API Organization

#### v3 Parsing
Each v3 class implements `_parse(input: ParseInput): ParseReturnType` independently. Example from `ZodArray._parse`:
- Validates type is array, checks `exactLength`, `minLength`, `maxLength`, then recursively parses elements using `addIssueToContext` on failure (`ZodArray._parse`, `packages/zod/src/v3/types.ts:2241-2317` source snippet).
- `ZodAny._parse` simply returns `OK(input.data)` (`ZodAny._parse`, `packages/zod/src/v3/types.ts:2115-2118` source snippet).

#### v4 Parsing (Functional)
The v4 core defines standalone parse function types in `packages/zod/src/v4/core/parse.ts`:

- **`$Parse`**: `<T extends schemas.$ZodType>(schema: T, value: unknown, _ctx?, _params?: { callee?; Err?: $ZodErrorClass }) => core.output<T>` (`$Parse`, `packages/zod/src/v4/core/parse.ts:7-9`).
- **`$ParseAsync`**: same but returns `Promise<core.output<T>>` (`$ParseAsync`, `packages/zod/src/v4/core/parse.ts:31-32`).
- **`$Decode`** / **`$DecodeAsync`**: take `core.input<T>` and produce `core.output<T>` (`$Decode`, `packages/zod/src/v4/core/parse.ts:109-110`; `$DecodeAsync`, `packages/zod/src/v4/core/parse.ts:134-135`).
- **`$Encode`** / **`$EncodeAsync`**: reverse direction, take `core.output<T>` and produce `core.input<T>` (`$Encode`, `packages/zod/src/v4/core/parse.ts:95-97`; `$EncodeAsync`, `packages/zod/src/v4/core/parse.ts:121-122`).
- **Safe variants**: `$SafeDecode`, `$SafeDecodeAsync`, `$SafeEncode` return `util.SafeParseResult` (`$SafeDecode`, `packages/zod/src/v4/core/parse.ts:159-160`; `$SafeEncode`, `packages/zod/src/v4/core/parse.ts:146-147`).
- **`$ZodErrorClass`**: `{ new (issues: errors.$ZodIssue[]): errors.$ZodError }` — a constructor type for error creation during parsing (`$ZodErrorClass`, `packages/zod/src/v4/core/parse.ts:5-6`).

### 4. Error Organization

#### v3 Errors
Defined in `packages/zod/src/v3/ZodError.ts`:
- **`ZodError`** extends `Error` with methods `constructor`, `errors`, `flatten`, `formErrors`, `format`, `assert`, `isEmpty`, `message`, `toString` (`ZodError`, `packages/zod/src/v3/ZodError.ts:193-316`).
- **`ZodErrorMap`**: `(issue: ZodIssueOptionalMessage, _ctx: ErrorMapCtx) => { message: string }` — a callback for customizing error messages (`ZodErrorMap`, `packages/zod/src/v3/ZodError.ts:329-330`).
- **Issue types**: a rich hierarchy of issue interfaces all extending `ZodIssueBase`, including `ZodInvalidTypeIssue`, `ZodInvalidLiteralIssue`, `ZodUnrecognizedKeysIssue`, `ZodInvalidUnionIssue`, `ZodCustomIssue`, etc.
- **`ZodIssueOptionalMessage`**: union of all issue types without required message (`ZodIssueOptionalMessage`, `packages/zod/src/v3/ZodError.ts:151-152`).

#### v4 Errors
- **Core**: `$ZodError extends Error` using `Symbol.for("zod.error")` for identification (`$ZodError`, `packages/zod/src/v4/core/errors.ts:214-217`). `$ZodFlattenedError = _FlattenedError<T, U>` (`$ZodFlattenedError`, `packages/zod/src/v4/core/errors.ts:250-254`).
- **Classic**: `ZodError extends $ZodError` adding `addIssue`, `addIssues`, `flatten`, `format` methods that delegate to `core.$ZodFormattedError`, `core.$ZodIssue`, `core.$ZodFlattenedError` (`ZodError`, `packages/zod/src/v4/classic/errors.ts:9-23`).
- **Safe parse result types**: `ZodSafeParseError = { success: false; data?: never; error: ZodError<T> }` (`ZodSafeParseError`, `packages/zod/src/v4/classic/parse.ts:6`); `SafeParseSuccess = { success: true; data: T; error?: never }` (`SafeParseSuccess`, `packages/zod/src/v4/core/util.ts:180`).

### 5. Structural Summary

```
v4/core/
├── schemas.ts    → $ZodType, internals ($ZodArrayInternals, $ZodObjectInternals, ...)
├── checks.ts     → $ZodStringFormatChecks, $ZodCheckProperty, centralized check types
├── parse.ts      → $Parse, $ParseAsync, $Decode, $Encode, $SafeDecode, $ZodErrorClass
├── errors.ts     → $ZodError, $ZodFlattenedError
├── core.ts       → $ZodAsyncError, $ZodEncodeError, $constructor, config
└── api.ts        → Parameterized check/type params ($ZodCheckPropertyParams, $ZodObjectParams, ...)

v4/classic/
├── schemas.ts    → ZodArray, ZodObject, ZodEnum, etc. (extends core internals + adds methods)
├── errors.ts     → ZodError extends $ZodError (adds format, flatten, addIssue)
└── parse.ts      → ZodSafeParseError

v3/
├── types.ts      → Class-based ZodType hierarchy with _parse methods
└── ZodError.ts   → Class-based ZodError with issue types
```

### What Cannot Be Determined

- The exact body logic of v4 core parse functions (`$Parse`, `$Decode`, etc.) — only type signatures are shown; actual validation flow is not in the clue file.
- How v4 checks are executed at runtime (the check pipeline mechanism) — only type definitions are available.
- The mini layer's check and error organization is not covered in this clue file's FOCUS section.
- The `$ZodCheckLengthEqualsParams`, `$ZodCheckLessThanParams` and other uncovered params noted in GAPS.
