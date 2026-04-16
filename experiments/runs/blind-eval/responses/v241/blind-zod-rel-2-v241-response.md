# v2.4.1 Response: blind-zod-rel-2
Date: 2026-04-16

## Parsing APIs, Schema-Level Checks, and Error Maps

The Zod validation pipeline connects three subsystems: **parsing APIs** that drive execution, **schema-level checks** that define constraints, and **error maps** that customize error messages.

### 1. Parsing APIs

#### v3 Parsing

- **`ZodType._parse`** (SYM: `packages/zod/src/v3/types.ts:170`) is the abstract entry point. Each schema overrides it.
- **`ParseInputLazyPath`** implements `ParseInput`, tracking `parent: ParseContext`, `data`, `_path`, and `_key` with lazy path computation via a cached getter (snippet: `ParseInputLazyPath`, L61-85).
- **Parse results** use a three-state model: `OK`, `DIRTY`, `INVALID`. In `ZodArray._parse`, after `_processInputParams(input)`, the method checks `ctx.parsedType`, validates length constraints, then returns `INVALID` on type mismatch or accumulates `status.dirty()` on constraint failures (snippet: `ZodArray._parse`, L2241-2317).
- **`ZodPipeline._parse`** chains two schemas (`_def.in` and `_def.out`): it parses input through `_def.in` first; if `aborted`, returns `INVALID`; if `dirty`, marks status dirty and returns; otherwise feeds `inResult.value` into `_def.out` (snippet: `ZodPipeline._parse`, L4782-4827). Both sync (`_parseSync`) and async (`_parseAsync`) paths are handled.
- **`SafeParseReturnType<Input, Output> = SafeParseSuccess<Output> | SafeParseError<Input>`** (snippet: L156).

#### v4 Parsing

- **`$Parse`**: `<T extends schemas.$ZodType>(schema: T, value: unknown, _ctx?, _params?: { callee?; Err?: $ZodErrorClass })` (FOCUS: `packages/zod/src/v4/core/parse.ts:7-9`). The `_params` includes an `Err` constructor for `$ZodErrorClass = { new (issues: errors.$ZodIssue[]): errors.$ZodError }` (FOCUS: L5-6).
- **`$ParseAsync`** mirrors `$Parse` with `Promise` return (FOCUS: L31-32).
- **Encode/Decode**: `$Decode` takes `core.input<T>` and returns `core.output<T>` (FOCUS: L109-110); `$Encode` reverses this (FOCUS: L95-97). These support codec-style bidirectional parsing.

### 2. Schema-Level Checks

#### v3 Check Pattern

- Schemas use `_addCheck` to register constraints: `ZodString._addCheck` (SYM: L1050), `ZodNumber._addCheck` (SYM: L1497), `ZodBigInt._addCheck` (SYM: L1749), `ZodDate._addCheck` (SYM: L1943).
- During `_parse`, checks are evaluated from `_def` — `ZodArray._parse` reads `def.exactLength`, `def.minLength`, `def.maxLength` and calls `addIssueToContext` with specific `ZodIssueCode` values (`too_big`, `too_small`, `invalid_type`) (snippet: `ZodArray._parse`).
- **Effects** compose additional checks: `Effect<T> = RefinementEffect<T> | TransformEffect<T> | PreprocessEffect<T>` (snippet: L4299-4301). `Refinement<T> = (arg: T, ctx: RefinementCtx) => any` (snippet: L4284); `SuperRefinement` adds `Promise<void>` support (snippet: L4285).

#### v4 Check Types

- **`$ZodCheckPropertyParams`** uses `CheckParams<checks.$ZodCheckProperty, "property" | "schema" | "when">` (FOCUS: `packages/zod/src/v4/core/api.ts:1082-1083`), showing the check-params pattern with `when` conditional support.
- **`CheckStringFormatParams`** and **`StringFormatParams`** both omit `"type" | "coerce" | "checks" | "error" | "check" | "format"` from their params (FOCUS: `packages/zod/src/v4/core/api.ts:40-50`), separating format configuration from check configuration.
- **`CheckTypeParams`** omits `"type" | "checks" | "error" | "check"` (FOCUS: L54-55), confirming that checks, errors, and type are configured separately in the API layer.

### 3. Error Maps and Error Customization

- **`ZodErrorMap`** in v3: `(issue: ZodIssueOptionalMessage, _ctx: ErrorMapCtx) => { message: string }` (FOCUS: `packages/zod/src/v3/ZodError.ts:329-330`). It takes an issue without a required message and a context, returning a message string.
- **`ZodIssueOptionalMessage`** is a union of all issue types without mandatory messages: `| ZodInvalidTypeIssue | ZodInvalidLiteralIssue | ZodUnrecognizedKeysIssue | ZodInvalidUnionIssue | ZodInvalidUnionDiscriminatorIssue | ZodInvalidEnumValueIssue` and more (FOCUS: L151-152).
- **`RefinementCtx`** connects checks to errors: `addIssue: (arg: IssueData) => void; path: (string | number)[]` (snippet: `RefinementCtx`, L38-48). Refinement and SuperRefinement functions receive this context to emit custom issues.
- **`CustomErrorParams = Partial<util.Omit<ZodCustomIssue, "code">>`** (snippet: L56) — allows passing partial custom error data excluding the code.

### 4. How They Connect

- **Checks → Issues → Error Map**: During `_parse`, checks that fail call `addIssueToContext(ctx, { code, ... })` (seen in `ZodArray._parse` snippet). Each issue has a `code` (e.g., `ZodIssueCode.invalid_type`, `too_small`, `too_big`). The `ZodErrorMap` is then consulted to generate the human-readable `message` from the issue and context.
- **Refinements → Issues**: `Refinement<T>` and `SuperRefinement<T>` receive `RefinementCtx` with `addIssue`, allowing custom checks to emit issues into the same pipeline.
- **Pipeline chaining**: `ZodPipeline._parse` shows how two schemas compose: the output of `_def.in._parse` feeds into `_def.out._parse`, with status propagation. If the first stage is `dirty`, the pipeline can short-circuit (snippet: `ZodPipeline._parse`).
- **v4 error class**: `$ZodErrorClass = { new (issues: errors.$ZodIssue[]): errors.$ZodError }` (FOCUS: L5-6), and `$ZodError extends: Error` (FOCUS: `packages/zod/src/v4/core/errors.ts:214-217`). The `$Parse` function accepts an optional `Err` parameter, allowing callers to inject a custom error class.
- **Classic `ZodError`** wraps `$ZodError` with `flatten`, `format`, `addIssue`, `addIssues` (FOCUS: `packages/zod/src/v4/classic/errors.ts:9-23`), and uses `core.$ZodFlattenedError` and `core.$ZodFormattedError`.
- **v3 `ZodError`** extends `Error` independently with `format` having behavior `PRECEDENCE(issue -> default); ACCUMULATE(format loop -> result); TRANSFORM(map)` (FOCUS: `ZodError.format`, L217-264).
- **`ZodPipelineDef extends: ZodTypeDef`** (FOCUS: `packages/zod/src/v3/types.ts:4764-4777`) links pipeline configuration into the standard def pattern.
- **`ZodSafeParseError = { success: false; data?: never; error: ZodError<T> }`** (FOCUS: `packages/zod/src/v4/classic/parse.ts:6`) wraps the error in the safe-parse result type.

### What Cannot Be Determined

- **Exact error map invocation order**: The clue shows `ZodErrorMap` type and `ZodError.format` behavior annotation (`PRECEDENCE(issue -> default)`), but the exact resolution logic — when schema-level messages override error maps vs. global error maps — is not shown in the provided snippets.
- **How `addIssueToContext` constructs issues**: The function is called in snippets but its body is not provided.
- **Global error map registration**: How a user sets a global `ZodErrorMap` (if such an API exists) is not shown.
- **`_processInputParams` internals**: Called in multiple `_parse` methods but never shown.
- **JSON Schema generation**: Listed as uncovered in GAPS (`JSONSchemaGeneratorParams`, `ToJSONSchemaContext`, `JSONSchemaGenerator.emit`, `JSONSchemaGenerator.process`).
- **Async check evaluation**: While `$ParseAsync` and `$DecodeAsync` signatures exist, the actual async check flow is not detailed.
