# v2.3 Response: blind-zod-mech-2
Date: 2026-04-15

## Summary

Zod uses a multi-layered error message system where messages can be customized at the check level, the schema level, and through global error maps. Based on the clue file and source snippets, the v3 `ZodErrorMap` is the primary customization mechanism, while v4 introduces a `$ZodConfig` with both `customError` and `localeError` maps at different priority levels. The error message getter in v3 serializes issues as JSON.

## Detailed Analysis

### Error Message Customization Layers

#### Layer 1: Per-Check / Per-Schema Error Messages (v3)

Individual validation methods accept an optional `message` parameter:

- **`ZodNumber.multipleOf`** (`v3/types.ts:1547-1554`) — signature: `multipleOf(value: number, message?: errorUtil.ErrMessage)`. Behavior: `DELEGATE(this._addCheck -> result)`. Uses `errorUtil.ErrMessage`, `errorUtil.toString` (FOCUS + source snippet). The `message` parameter allows per-check custom messages.
- **`ZodBigInt.multipleOf`** (`v3/types.ts:1792-1800`) — same pattern: `multipleOf(value: bigint, message?: errorUtil.ErrMessage)`. Behavior: `DELEGATE(this._addCheck -> result)` (FOCUS).
- The `errorUtil.ErrMessage` type and `errorUtil.toString` helper suggest that error messages can be either strings or objects with a `message` property.

#### Layer 2: Error Maps (v3)

- **`ZodErrorMap`** (`v3/ZodError.ts:329-330`) — `type alias ZodErrorMap = (issue: ZodIssueOptionalMessage, _ctx: ErrorMapCtx) => { message: string }` (FOCUS + source snippet at line 330).
  - Takes an issue (without message) and an error context (`ErrorMapCtx`).
  - Returns `{ message: string }`.
  - This is a function-based customization point where users can map any issue to any message.
- **`ErrorMapCtx`** (`ZodError.ts:325`) — the context object passed to error maps. Its structure is `{ defaultError: string; data: any }` based on the source snippet (source snippet: `ErrorMapCtx`).
- **`ZodIssueOptionalMessage`** (`ZodError.ts:151-152`) — the input to error maps, a union of all issue types: `ZodInvalidTypeIssue | ZodInvalidLiteralIssue | ZodUnrecognizedKeysIssue | ZodInvalidUnionIssue | ZodInvalidUnionDiscriminatorIssue | ZodInvalidEnumValueIssue | ZodInvalidArgumentsIssue | ...` (FOCUS). Each issue type has a `code` field identifying the issue kind.

#### Layer 3: Global Configuration (v4)

- **`$ZodConfig`** (`v4/core/core.ts:121-131`, source snippet) defines the global configuration:
  ```typescript
  export interface $ZodConfig {
    /** Custom error map. Overrides `config().localeError`. */
    customError?: errors.$ZodErrorMap | undefined;
    /** Localized error map. Lowest priority. */
    localeError?: errors.$ZodErrorMap | undefined;
    /** Disable JIT schema compilation. */
    jitless?: boolean | undefined;
  }
  ```
  - **`customError`**: A `$ZodErrorMap` that **overrides** the `localeError`. This is the higher-priority error map.
  - **`localeError`**: A `$ZodErrorMap` with **lowest priority**. This is intended for localization.
  - The comments explicitly state the priority: `customError` overrides `localeError`.

- **`config`** function (`core/core.ts:134-138`, source snippet):
  ```typescript
  export function config(newConfig?: Partial<$ZodConfig>): $ZodConfig {
    if (newConfig) Object.assign(globalConfig, newConfig);
    return globalConfig;
  }
  ```
  This reveals the config is stored in a `globalConfig` object and can be updated via `Object.assign`.

### Priority Order for Error Messages

Based on the evidence, the priority order (highest to lowest) when multiple customization layers are available is:

1. **Per-check `message` parameter** — provided directly in schema method calls like `multipleOf(5, "Must be multiple of 5")`. This is the most specific customization (FOCUS: `ZodNumber.multipleOf`, `ZodBigInt.multipleOf` — `message?: errorUtil.ErrMessage`).

2. **`customError` map** (v4) — set via `config({ customError: myMap })`. The JSDoc explicitly says it "Overrides `config().localeError`" (source snippet: `$ZodConfig`).

3. **`localeError` map** (v4) — set via `config({ localeError: myMap })`. Documented as "Lowest priority" (source snippet: `$ZodConfig`).

4. **Default messages** — when no custom message or error map provides a message, the framework produces a default. In v3, `ZodError.format` has behavior `PRECEDENCE(issue -> default)` (FOCUS: `ZodError.format`), confirming that per-issue messages take precedence over defaults.

### Error Construction and Representation

#### v3 ZodError

- **`ZodError.constructor`** (`ZodError.ts:201-213`, source snippet) — takes `issues: ZodIssue[]`, sets up prototype chain, assigns `this.name = "ZodError"` and `this.issues = issues`.
- **`ZodError.message`** getter (`ZodError.ts:280-282`, source snippet):
  ```typescript
  override get message() {
    return JSON.stringify(this.issues, util.jsonStringifyReplacer, 2);
  }
  ```
  The message is the **JSON-stringified** issues array with pretty printing (2-space indent). Behavior: `DELEGATE(JSON.stringify -> result)` (FOCUS: `ZodError.message`).
- **`ZodError.toString`** (`ZodError.ts:277-279`, source snippet) — `return this.message`, so `toString()` also returns the JSON-stringified issues.
- **`ZodError.errors`** getter (`ZodError.ts:197-199`, source snippet) — `return this.issues`, making `errors` an alias for `issues`.
- **`ZodError.isEmpty`** (`ZodError.ts:284-286`, source snippet) — `return this.issues.length === 0`.
- **`ZodError.formErrors`** (`ZodError.ts:313-315`, source snippet) — `return this.flatten()`, making `formErrors` an alias for `flatten()`.

#### v3 Error Formatting

- **`ZodError.format`** (`ZodError.ts:217-264`) — behavior: `PRECEDENCE(issue -> default); ACCUMULATE(loop -> result); TRANSFORM(map)` (FOCUS). Processes issues using:
  - `issue.message` — the per-issue message
  - `issue.code` — the issue type code
  - `issue.unionErrors.map` — for union errors, maps over sub-errors
  - A `_mapper` function parameter for custom transformation

#### v4 Classic ZodError

- **`ZodError`** (`classic/errors.ts:9-23`, source snippet) — extends `$ZodError<T>` and provides:
  - `format()` — marked `@deprecated`, suggests using `z.treeifyError(err)` instead.
  - `flatten()` — marked `@deprecated`, returns `core.$ZodFlattenedError`.
  - `addIssue(issue)` — marked `@deprecated`, suggests pushing directly to `.issues`.
  - `addIssues(issues)` — marked `@deprecated`.
  - `isEmpty` — marked `@deprecated`, suggests checking `err.issues.length === 0`.

### Specialized Error Types

- **`$ZodAsyncError`** (`core/core.ts:97-102`, source snippet) — thrown when a Promise is encountered during synchronous parse. Constructor: `super("Encountered Promise during synchronous parse. Use .parseAsync() instead.")`. This is a **fixed message** — not customizable through error maps.
- **`$ZodEncodeError`** (`core/core.ts:103-109`, source snippet) — thrown during encode operations. Constructor: `super("Encountered unidirectional transform during encode: ${name}")`. Sets `this.name = "ZodEncodeError"`. Also a **fixed message** using the schema name.

### Issue Type System

The v3 issue types that feed into error maps (source snippets):

- `ZodInvalidTypeIssue` — `code: ZodIssueCode.invalid_type`, `expected: ZodParsedType`, `received: ZodParsedType`
- `ZodInvalidLiteralIssue` — `code: ZodIssueCode.invalid_literal`
- `ZodUnrecognizedKeysIssue` — for unknown object keys
- `ZodInvalidUnionIssue` — `code: ZodIssueCode.invalid_union`, `unionErrors: ZodError[]`
- `ZodInvalidUnionDiscriminatorIssue` — `code: ZodIssueCode.invalid_union_discriminator`
- `ZodInvalidEnumValueIssue` — `code: ZodIssueCode.invalid_enum_value`
- `ZodInvalidStringIssue` — `code: ZodIssueCode.invalid_string`, `validation: StringValidation`
- `ZodTooBigIssue` — `code: ZodIssueCode.too_big`, `maximum`, `inclusive`
- `ZodNotMultipleOfIssue` — `code: ZodIssueCode.not_multiple_of`, `multipleOf: number | bigint`
- `ZodNotFiniteIssue` — `code: ZodIssueCode.not_finite`
- `ZodInvalidIntersectionTypesIssue` — `code: ZodIssueCode.invalid_intersection_types`
- `ZodInvalidArgumentsIssue` — `code: ZodIssueCode.invalid_arguments`, `argumentsError: ZodError`
- `ZodInvalidReturnTypeIssue` — `code: ZodIssueCode.invalid_return_type`, `returnTypeError: ZodError`
- `ZodInvalidDateIssue` — `code: ZodIssueCode.invalid_date`
- `ZodCustomIssue` — `code: ZodIssueCode.custom`, `params?: { [k: string]: any }`

Each of these is an input to the `ZodErrorMap` function, which the map can inspect via the `code` field to produce customized messages.

#### v4 Issue Aliases

- **`ZodIssue`** (`classic/errors.ts:6`) — `type ZodIssue = core.$ZodIssue` (source snippet). The v4 classic layer re-exports core issues.
- **`IssueData`** (`classic/errors.ts:79`) — `type IssueData = core.$ZodRawIssue` (source snippet). Raw issue data before processing.

### Custom Error Params (v3)

- **`CustomErrorParams`** (`v3/types.ts:55-56`) — `Partial<util.Omit<ZodCustomIssue, "code">>` (FOCUS). This allows users to provide custom issue data (except the code) when defining custom validations.

## Uncertainty / Limits

- **Exact v4 error map invocation**: The runtime flow for how `customError` and `localeError` maps interact with per-check messages in v4 is not shown in the source snippets. The priority ordering is inferred from the JSDoc comments.
- **`_addCheck` internals**: The body of `_addCheck` methods is not provided. How they store the `message` parameter and when it's consulted during validation is not visible.
- **v4 `$ZodErrorMap` type**: While `$ZodConfig` references `errors.$ZodErrorMap`, its exact type signature for v4 is not in the FOCUS (only the v3 `ZodErrorMap` is shown).
- **Error map scope**: Whether error maps can be set per-schema in addition to globally is not documented in the available clue file data.
- **GAPS**: "80 symbols in L3, 5 with behavior annotations" — limited behavioral information is available for the focused symbols.
