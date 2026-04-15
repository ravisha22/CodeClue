# v2.3 Response: blind-zod-rel-2
Date: 2026-04-15

## Summary

Zod's validation pipeline connects three systems: parsing APIs (which drive validation), schema-level checks (which constrain values), and error maps (which customize error messages). Parse functions invoke schemas, schemas apply checks, and errors are produced with messages that can be customized through error maps. The v3 and v4 architectures handle these relationships differently.

## Detailed Analysis

### Parsing APIs (`packages/zod/src/v4/core/parse.ts`)

The parse layer defines the entry points for validation. All parse type aliases are parameterized over `schemas.$ZodType` and accept a `ParseContext<errors.$ZodIssue>`, directly coupling parsing to both the schema and error systems.

- **`$Parse`** (`parse.ts:7-9`) — three overloads of the synchronous parse function: `<T extends schemas.$ZodType>(schema: T, value: unknown, _ctx?: schemas.ParseContext<errors.$ZodIssue>, _params?: { callee?: util.AnyFunc; Err?: $ZodErrorClass })` (FOCUS). The `_params` argument includes an `Err` field typed as `$ZodErrorClass`, allowing the caller to specify which error class to use.
- **`$ParseAsync`** (`parse.ts:31-32`) — async variant with the same parameter structure (FOCUS).
- **`$ZodErrorClass`** (`parse.ts:5-6`) — defines the error class constructor: `{ new (issues: errors.$ZodIssue[]): errors.$ZodError }` (FOCUS). This connects parsing to error creation: when parsing fails, it instantiates a `$ZodError` from an array of `$ZodIssue` objects.

### Relationship: Parse → Schema → Checks

#### v3 Architecture

In v3, parsing is embedded directly in schema types:

- **`ZodType._parse`** (`v3/types.ts:170`) — the abstract parse method that every schema type overrides (SYM). Each concrete type (e.g., `ZodString._parse` at line 732, `ZodNumber._parse` at line 1370, etc.) implements its own validation logic.
- **`_addCheck`** methods — schema types apply checks via `_addCheck`:
  - `ZodString._addCheck` (`types.ts:1050`), `ZodNumber._addCheck` (`types.ts:1497`), `ZodBigInt._addCheck` (`types.ts:1749`), `ZodDate._addCheck` (`types.ts:1943`) (SYM entries).
  - These checks are accumulated on the schema and evaluated during `_parse`.

#### v4 Architecture

In v4, checks are externalized into a dedicated module:

- **`$ZodChecks`** (`v4/core/checks.ts:1267-1268`) — a union type of all check types: `$ZodCheckLessThan | $ZodCheckGreaterThan | $ZodCheckMultipleOf | $ZodCheckNumberFormat | $ZodCheckBigIntFormat | $ZodCheckMaxSize | ...` (FOCUS: `$ZodChecks`). This is a comprehensive enumeration of all available check constraints.
- **`$ZodStringFormatChecks`** (`checks.ts:1286`) — string-specific checks: `$ZodCheckRegex | $ZodCheckLowerCase | $ZodCheckUpperCase | $ZodCheckIncludes | $ZodCheckStartsWith | $ZodCheckEndsWith | schemas.$ZodStringFormatTypes` (not in this task's FOCUS but referenced in struct-2).
- **Check parameter types** in `v4/core/api.ts`:
  - `$ZodCheckPropertyParams` (`api.ts:1082-1083`) — `CheckParams<checks.$ZodCheckProperty, "property" | "schema" | "when">` (FOCUS). The `when` field suggests checks can be conditional.
  - `CheckStringFormatParams` (`api.ts:49-50`) — params for string format checks, omitting `"type" | "coerce" | "checks" | "error" | "check" | "format"` (FOCUS).
  - `CheckTypeParams` (`api.ts:54-55`) — params for type-level checks, omitting `"type" | "checks" | "error" | "check"` (FOCUS). Note both omit `"error"` and `"check"`, suggesting these are handled elsewhere.
  - `StringFormatParams` (`api.ts:40-41`) — params for string formats (FOCUS).

### Error Maps — Customizing Error Messages

#### v3 Error Maps

- **`ZodErrorMap`** (`v3/ZodError.ts:329-330`) — `type alias ZodErrorMap = (issue: ZodIssueOptionalMessage, _ctx: ErrorMapCtx) => { message: string }` (FOCUS). This is a function that takes an issue (without a message) and a context, and returns a message string. It is the customization point for error messages.
- **`ZodIssueOptionalMessage`** (`ZodError.ts:151-152`) — a union of all issue types without the `message` field: `ZodInvalidTypeIssue | ZodInvalidLiteralIssue | ZodUnrecognizedKeysIssue | ZodInvalidUnionIssue | ZodInvalidUnionDiscriminatorIssue | ZodInvalidEnumValueIssue | ...` (FOCUS). This is the input to the error map.
- The error map receives the issue data and error context (`ErrorMapCtx`) and produces the `message` string. This means: **the error map runs after check/validation failures are detected but before the final issue is assembled with a message**.

#### v3 Error Formatting

- **`ZodError.format`** (`ZodError.ts:217-264`) — behavior: `PRECEDENCE(issue -> default); ACCUMULATE(loop -> result); TRANSFORM(map)` (FOCUS). This reveals:
  1. `PRECEDENCE(issue -> default)` — per-issue messages take precedence, with a default fallback.
  2. `ACCUMULATE(loop -> result)` — iterates over all issues to build the formatted output.
  3. `TRANSFORM(map)` — applies a mapper/transform function.
  - It processes `issue.message`, `error.issues`, `issue.code`, `issue.unionErrors.map` (FOCUS uses).

#### v4 Error Types

- **`$ZodError`** (`core/errors.ts:214-217`) — interface extending `Error`, identified by `Symbol.for("zod.error")` (FOCUS). This is the v4 core error type.
- **`ZodError`** (classic, `classic/errors.ts:9-23`) — extends `$ZodError` with `addIssue`, `addIssues`, `flatten`, `format` methods (FOCUS). Uses `core.$ZodIssue` and `core.$ZodFlattenedError`.
- **`ZodPipelineDef`** (`v3/types.ts:4764-4777`) — extends `ZodTypeDef`, uses `ZodFirstPartyTypeKind.ZodPipeline` (FOCUS). This shows that pipeline schemas carry a def that includes the pipeline kind.

### How They Relate — The Validation Pipeline Flow

Based on the clue file evidence, the validation pipeline works as follows:

1. **Entry**: A `$Parse` or `$ParseAsync` function is called with a schema and a value. The parse context includes `ParseContext<errors.$ZodIssue>` for collecting issues (FOCUS: `$Parse`).

2. **Schema validation**: In v3, the schema's `_parse` method runs, applying the schema's accumulated checks (via `_addCheck`). In v4, checks from `$ZodChecks` are evaluated against the value.

3. **Issue generation**: When checks fail, issues are created. In v3, issues are typed as `ZodIssueOptionalMessage` — they contain the issue code and data but **not yet the message** (FOCUS: `ZodIssueOptionalMessage`).

4. **Error map application**: The `ZodErrorMap` function is invoked to produce the `message` field for each issue. The map receives the issue and an `ErrorMapCtx` context (FOCUS: `ZodErrorMap`). This is how users customize error messages.

5. **Error construction**: Issues (now with messages, typed as `ZodIssue = ZodIssueOptionalMessage & { message }`) are collected into a `ZodError` (v3) or `$ZodError` (v4) via the `$ZodErrorClass` constructor: `new (issues: errors.$ZodIssue[]): errors.$ZodError` (FOCUS: `$ZodErrorClass`).

6. **Error formatting**: Users can call `ZodError.format()` to get structured output, or `flatten()` for a flat representation (FOCUS: `ZodError` classic — methods `flatten, format`).

### Cross-Cutting Relationships

- **Checks → Errors**: Check parameter types in `api.ts` omit `"error"` from their parameter sets (FOCUS: `CheckTypeParams`, `CheckStringFormatParams`), suggesting errors are handled separately from check definition — the error is produced when the check fails, not configured within the check itself.
- **Parse → Errors**: The `$Parse` type's `_params.Err` field (FOCUS: `$Parse`) allows injecting a custom error class, connecting the parse layer to the error system.
- **Schema → Checks**: In v4, checks are typed as `$ZodChecks` and `$ZodStringFormatChecks` unions (FOCUS), referenced by schemas through their internals. The `ZodMiniType` base type references `core.$ZodCheck` and `core.CheckFn` (from struct-1 FOCUS).

## Uncertainty / Limits

- **v4 error map mechanism**: The v3 `ZodErrorMap` is clearly documented, but the v4 equivalent error map type is not present in this task's FOCUS. It's unclear if v4 uses the same function-based error map pattern.
- **Check execution order**: Whether checks are evaluated in registration order, or if there's a priority system, is not documented.
- **Parse function bodies**: Only type signatures are available for `$Parse` and related types. The actual runtime flow (e.g., how parse catches check failures and invokes the error map) is not in the clue file.
- **`ErrorMapCtx`**: Referenced in `ZodErrorMap` but its structure is not detailed in the FOCUS.
- **GAPS**: "80 symbols in L3, 5 with behavior annotations" — limited behavioral information is available.
