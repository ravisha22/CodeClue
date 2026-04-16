# v2.4.1 Response: blind-zod-struct-2
Date: 2026-04-16

## Organization of Schema Types, Checks, and Errors

Zod's internal architecture organizes its validation system into three major pillars — schema types, checks, and errors — spread across both v3 and v4 codebases.

### 1. Schema Types

#### v3 Schema Types (Class-Based)

All v3 schemas live in a single monolithic file, `packages/zod/src/v3/types.ts` (5138 lines, per INDEX). They follow a class hierarchy rooted at `ZodType`:

- **`ZodType`** is the base, with `_parse` (SYM: `ZodType._parse`, line 170), `constructor` (SYM: `ZodType.constructor`, line 411), and `_getOrReturnCtx` (SYM: line 176).
- **Concrete schemas** extend `ZodType` — e.g., `ZodAny extends ZodType<any, ZodAnyDef, any>` (snippet: `ZodAnyDef`, `packages/zod/src/v3/types.ts L2101-2112`). Each has a `*Def` interface extending `ZodTypeDef` with a `typeName` discriminant — `ZodAnyDef` has `typeName: ZodFirstPartyTypeKind.ZodAny` (same snippet).
- **`ZodFirstPartySchemaTypes`** is a union type alias aggregating all first-party schemas: `| ZodString | ZodNumber | ZodNaN | ZodBigInt | ZodBoolean | ZodDate | ZodUndefined` and more (FOCUS: `packages/zod/src/v3/types.ts:4996-4997`).
- **Parsing entry**: Each schema implements `_parse(input: ParseInput): ParseReturnType<this["_output"]>` — e.g., `ZodAny._parse` simply returns `OK(input.data)` (snippet: `ZodAny._parse`, L2115-2118). `ZodArray._parse` demonstrates the full pattern: call `_processInputParams(input)`, check `ctx.parsedType`, validate constraints (`exactLength`, `minLength`, `maxLength`), then parse each element (snippet: `ZodArray._parse`, L2241-2317).
- **Parse context**: `ParseInputLazyPath` implements `ParseInput` with lazy path computation — `path` getter concatenates `_path` and `_key`, caching the result in `_cachedPath` (snippet: `ParseInputLazyPath`, L61-85).

#### v4 Schema Types (Interface-Based)

- **Core schemas** use `$ZodType` as base (FOCUS: `ZodMiniType extends: $ZodType` in `packages/zod/src/v4/mini/schemas.ts:6-38`).
- **Parse/decode/encode type aliases** in `packages/zod/src/v4/core/parse.ts` define the function signatures: `$Parse` takes `(schema: T, value: unknown, _ctx?, _params?)` (FOCUS: L7-9); `$Decode` takes `(schema: T, value: core.input<T>, _ctx?)` returning `core.output<T>` (FOCUS: L109-110); `$Encode` is the reverse (FOCUS: L95-97). Async variants exist for each (`$ParseAsync`, `$DecodeAsync`, `$EncodeAsync`).
- **Safe variants**: `$SafeDecode`, `$SafeEncode` return `util.SafeParseResult<...>` (FOCUS: L159-160, L146-147).

### 2. Checks

- **v3 check pattern**: Schema-specific `_addCheck` methods — `ZodString._addCheck` (SYM: line 1050), `ZodNumber._addCheck` (SYM: line 1497), `ZodBigInt._addCheck` (SYM: line 1749), `ZodDate._addCheck` (SYM: line 1943). Checks are stored in `_def` and validated during `_parse`.
- **v4 check types**: Organized in `packages/zod/src/v4/core/checks.ts`. The union type `$ZodStringFormatChecks` aggregates format-specific checks: `$ZodCheckRegex | $ZodCheckLowerCase | $ZodCheckUpperCase | $ZodCheckIncludes | $ZodCheckStartsWith | $ZodCheckEndsWith | schemas.$ZodStringFormatTypes` (FOCUS: `$ZodStringFormatChecks`, L1286).
- **Check params** in `packages/zod/src/v4/core/api.ts` use a `CheckParams<T, OmitKeys>` pattern — e.g., `$ZodCheckPropertyParams = CheckParams<checks.$ZodCheckProperty, "property" | "schema" | "when">` (FOCUS: L1082-1083).
- **Accessor schemas**: `ZodMap.valueSchema` and `ZodRecord.valueSchema` are getters returning `this._def.valueType` (snippets: `ZodMap.valueSchema` L3600-3603, `ZodRecord.valueSchema` L3511-3514), providing access to inner schemas for recursive validation.

### 3. Error Organization

- **v3 errors**: `RefinementCtx` interface provides `addIssue: (arg: IssueData) => void` and `path: (string | number)[]` (snippet: `RefinementCtx`, L38-48). `CustomErrorParams = Partial<util.Omit<ZodCustomIssue, "code">>` (snippet: `CustomErrorParams`, L56). `SafeParseReturnType<Input, Output> = SafeParseSuccess<Output> | SafeParseError<Input>` (snippet: L156).
- **v4 errors**: `SafeParseSuccess<T> = { success: true; data: T; error?: never }` (snippet: `SafeParseSuccess`, L180); `SafeParseError<T>` (snippet: L181). Both live in `packages/zod/src/v4/core/util.ts`.
- **Effects system**: `Effect<T> = RefinementEffect<T> | TransformEffect<T> | PreprocessEffect<T>` (snippet: L4299-4301). Each has a `type` discriminant: `"refinement"` (snippet: L4287), `"transform"` (snippet: L4291), `"preprocess"` (snippet: L4295).
- **Refinement types**: `Refinement<T> = (arg: T, ctx: RefinementCtx) => any` and `SuperRefinement<T> = (arg: T, ctx: RefinementCtx) => void | Promise<void>` (snippet: L4284-4287).

### 4. Object Schema Configuration

- **Unknown keys**: `UnknownKeysParam = "passthrough" | "strict" | "strip"` (snippet: L2368-2370), governing how unrecognized properties are handled.
- **Object specializations**: `SomeZodObject = ZodObject<ZodRawShape, UnknownKeysParam, ZodTypeAny>` (snippet: L2418-2420); `AnyZodObject = ZodObject<any, any, any>` (snippet: L2926-2928).
- **Catchall types**: `CatchallOutput<T>` and `CatchallInput<T>` provide conditional types for catchall schemas on objects (snippets: L2406-2410).

### What Cannot Be Determined

- **Full check type enumeration**: The `$ZodStringFormatChecks` union is shown, but the complete `$ZodChecks` union and all individual check interfaces are not fully listed in the FOCUS section.
- **How `addIssueToContext` works internally**: Used in `ZodArray._parse` (snippet), but its implementation is not provided.
- **JSON Schema generation internals**: Listed as uncovered in GAPS (`JSONSchemaGeneratorParams`, `ToJSONSchemaContext`, `JSONSchemaGenerator.emit`, `JSONSchemaGenerator.process`).
- **How `_processInputParams` transforms input**: Called in `ZodArray._parse` but its body is not shown.
- **Error formatting internals in v4**: Only the v4 `$ZodError` interface signature is shown (`extends: Error, uses: Symbol.for, zod.error`), not its implementation.
