# v2.4 Response: blind-zod-mech-2
Date: 2026-04-16

## Question
How does Zod decide which error message to emit when multiple customization layers are available?

## Answer

### 1. Error Message Customization Layers

The clue file and source snippets reveal multiple layers that can influence the final error message, operating at different scopes.

#### Layer 1: Check-Level Error Map (Per-Check)
Each individual check definition carries its own error map:
- **`$ZodCheckDef`** `uses: errors.$ZodErrorMap` — the check definition interface directly references an error map (`$ZodCheckDef`, `packages/zod/src/v4/core/checks.ts:8-18`). This means when defining a check (e.g., min length, max value, multipleOf), a custom error map can be attached at the check level.
- **`$ZodCheckInternals`** has a `check` method that produces `errors.$ZodIssueBase` via `schemas.ParsePayload` (`$ZodCheckInternals`, `packages/zod/src/v4/core/checks.ts:19-26`). The check generates issue data, and the associated error map can customize the message.
- **`$ZodCheck`** is the base check interface (`$ZodCheck`, `packages/zod/src/v4/core/checks.ts:27-30`).

#### Layer 2: Schema-Level Custom Error (`customError` in Config)
The global configuration provides a schema-wide error map:
- **`$ZodConfig.customError`**: `errors.$ZodErrorMap | undefined` — described as "Custom error map. Overrides `config().localeError`." This is explicitly documented as higher priority than localeError (`$ZodConfig`, `packages/zod/src/v4/core/core.ts:121-131` source snippet).

#### Layer 3: Locale-Level Error Map (`localeError` in Config)
- **`$ZodConfig.localeError`**: `errors.$ZodErrorMap | undefined` — described as "Localized error map. Lowest priority." This serves as the fallback for i18n/l10n error messages (`$ZodConfig`, `packages/zod/src/v4/core/core.ts:121-131` source snippet).

#### Layer 4: Inline Error Messages (Per-Method Call)
Classic schema methods accept inline error parameters:
- `ZodArray.min(minLength: number, params?: string | core.$ZodCheckMinLengthParams)` — accepts either a string message or a check params object (`ZodArray`, `packages/zod/src/v4/classic/schemas.ts:1127-1140`).
- Similarly: `ZodArray.max(maxLength, params?: string | core.$ZodCheckMaxLengthParams)`, `ZodArray.length(len, params?: string | core.$ZodCheckLengthEqualsParams)`.
- `ZodFile.min`, `ZodFile.max`, `ZodFile.mime` all accept similar params.
- In v3: `ZodNumber.multipleOf(value: number, message?: errorUtil.ErrMessage)` uses `errorUtil.ErrMessage` and delegates to `this._addCheck` (`ZodNumber.multipleOf`, `packages/zod/src/v3/types.ts:1547-1554`). `ZodBigInt.multipleOf` follows the same pattern (`packages/zod/src/v3/types.ts:1792-1800`).

### 2. Priority / Precedence Order

Based on the `$ZodConfig` documentation comments and the `ZodError.format` behavior annotation, the precedence from highest to lowest is:

1. **Inline/per-call message** — passed directly to check methods (e.g., `string | $ZodCheckMinLengthParams`). This is the most specific level.
2. **Check-level `$ZodErrorMap`** — carried in `$ZodCheckDef`, allowing per-check error customization.
3. **`customError`** — global config's custom error map. The doc comment explicitly states it "Overrides `config().localeError`" (`$ZodConfig`, `packages/zod/src/v4/core/core.ts:124`).
4. **`localeError`** — global config's locale error map. Documented as "Lowest priority" (`$ZodConfig`, `packages/zod/src/v4/core/core.ts:126`).
5. **Default/built-in message** — when no customization layers provide a message.

The `ZodError.format` behavior annotation confirms a precedence model: `PRECEDENCE(issue -> default)` — meaning issue-specific data takes priority, falling back to defaults (`ZodError.format`, `packages/zod/src/v3/ZodError.ts:217-264`).

### 3. v3 Error Map Mechanism

In v3, the error map is a function type:
- **`ZodErrorMap = (issue: ZodIssueOptionalMessage, _ctx: ErrorMapCtx) => { message: string }`** (`ZodErrorMap`, `packages/zod/src/v3/ZodError.ts:329-330`).
- The input is a `ZodIssueOptionalMessage` — an issue union type that does **not** include a `message` field, meaning the error map is responsible for generating the message.
- `ZodIssueOptionalMessage` includes: `ZodInvalidTypeIssue | ZodInvalidLiteralIssue | ZodUnrecognizedKeysIssue | ZodInvalidUnionIssue | ZodInvalidUnionDiscriminatorIssue | ZodInvalidEnumValueIssue | ZodInvalidArgumentsIssue` and more (`ZodIssueOptionalMessage`, `packages/zod/src/v3/ZodError.ts:151-152`).
- `ErrorMapCtx` provides additional context for message generation (`ErrorMapCtx`, `packages/zod/src/v3/ZodError.ts:325`).
- The final `ZodIssue` type is `ZodIssueOptionalMessage & { message: string }` — the error map's output `{ message }` is merged onto the issue (`ZodIssue`, `packages/zod/src/v3/ZodError.ts:169-170`).

### 4. Error Message Rendering

Once the final message is determined, it flows into the error object:

#### v3 ZodError
- **`ZodError.message`**: returns `JSON.stringify(this.issues, util.jsonStringifyReplacer, 2)` — the `message` getter serializes all issues to JSON (`ZodError.message`, `packages/zod/src/v3/ZodError.ts:280-282` source snippet).
- **`ZodError.toString()`**: delegates to `this.message` (`ZodError.toString`, `packages/zod/src/v3/ZodError.ts:277-279` source snippet).
- **`ZodError.format()`**: `PRECEDENCE(issue -> default); ACCUMULATE(format loop -> result); TRANSFORM(map)` — iterates issues, accumulates a formatted tree, applies mapper transform (`ZodError.format`, `packages/zod/src/v3/ZodError.ts:217-264`). Uses `issue.message, error.issues, issue.code, issue.unionErrors.map`.
- **`ZodError.flatten()`**: returns `$ZodFlattenedError` — separates form-level and field-level errors (`ZodError.flatten`, `packages/zod/src/v4/classic/errors.ts:14`).
- **`ZodError.isEmpty`**: `this.issues.length === 0` (`ZodError.isEmpty`, `packages/zod/src/v3/ZodError.ts:284-286` source snippet).

#### v4 Classic ZodError
- **`ZodError extends $ZodError`** with `format()` → `core.$ZodFormattedError` and `flatten()` → `core.$ZodFlattenedError`, plus `addIssue` and `addIssues` methods (`ZodError`, `packages/zod/src/v4/classic/errors.ts:9-23`). The `format` and `flatten` methods are marked as `@deprecated` in favor of `z.treeifyError(err)`.
- **`ZodSafeParseError = { success: false; data?: never; error: ZodError<T> }`** — safe parse wraps the error in a result object (`ZodSafeParseError`, `packages/zod/src/v4/classic/parse.ts:6`).

#### v4 Core $ZodError
- **`$ZodError extends Error`** using `Symbol.for("zod.error")` for runtime identification (`$ZodError`, `packages/zod/src/v4/core/errors.ts:214-217`).

### 5. Special Error Classes

Two specialized error classes bypass the error map system entirely:

- **`$ZodAsyncError`**: thrown when a Promise is encountered during synchronous parse. Message is hardcoded: `"Encountered Promise during synchronous parse. Use .parseAsync() instead."` (`$ZodAsyncError`, `packages/zod/src/v4/core/core.ts:97-102` source snippet).
- **`$ZodEncodeError`**: thrown during unidirectional transform encode. Message: `"Encountered unidirectional transform during encode: ${name}"` (`$ZodEncodeError`, `packages/zod/src/v4/core/core.ts:103-109` source snippet). Both extend `Error` directly, not `$ZodError`.

### 6. Issue Type Hierarchy

Different issue types carry different data for error map resolution:
- `ZodInvalidTypeIssue`: `expected: ZodParsedType, received: ZodParsedType` (`packages/zod/src/v3/ZodError.ts:40-45`).
- `ZodInvalidLiteralIssue`: `expected: unknown, received: unknown` (`packages/zod/src/v3/ZodError.ts:46-51`).
- `ZodInvalidUnionIssue`: `unionErrors: ZodError[]` (`packages/zod/src/v3/ZodError.ts:57-61`).
- `ZodNotMultipleOfIssue`: `multipleOf: number | bigint` (`ZodNotMultipleOfIssue`, `packages/zod/src/v3/ZodError.ts:135-139`).
- `ZodCustomIssue`: `params?: { [k: string]: any }` (`ZodCustomIssue`, `packages/zod/src/v3/ZodError.ts:144-148` source snippet).
- `ZodTooBigIssue`: `maximum: number | bigint, inclusive: boolean, exact?: boolean` (`ZodTooBigIssue`, `packages/zod/src/v3/ZodError.ts:123-130`).
- v4 classic: `ZodIssue = core.$ZodIssue` (`ZodIssue`, `packages/zod/src/v4/classic/errors.ts:6`).

### 7. Config Application

The `config()` function applies error maps globally:
```typescript
export function config(newConfig?: Partial<$ZodConfig>): $ZodConfig {
  if (newConfig) Object.assign(globalConfig, newConfig);
  return globalConfig;
}
```
(`config`, `packages/zod/src/v4/core/core.ts:134-138` source snippet)

This means `customError` and `localeError` are set once and apply to all subsequent validations. The `Object.assign` merge means later calls to `config()` can overwrite earlier maps.

### Summary: Decision Flow

```
Validation failure occurs
        │
        ▼
  Has inline message/params?  ──yes──►  Use inline message
        │ no
        ▼
  Check has $ZodErrorMap?     ──yes──►  Call check-level error map
        │ no
        ▼
  config().customError set?   ──yes──►  Call customError map
        │ no
        ▼
  config().localeError set?   ──yes──►  Call localeError map
        │ no
        ▼
  Use built-in default message
```

### What Cannot Be Determined

- The exact runtime code that implements this precedence chain — the actual resolution function that queries each layer in order is not in the clue file.
- Whether the check-level error map in `$ZodCheckDef` is called before or after `customError` — the ordering is inferred from naming patterns and doc comments, not from source code.
- How `when` parameters in check params (e.g., `$ZodCheckMultipleOfParams = CheckParams<..., "value" | "when">`) affect error map selection.
- The `ZodBigIntCheck` and `ZodDateCheck` types noted in GAPS are uncovered.
- The v4 `$ZodErrorMap` type definition itself (vs the v3 `ZodErrorMap`) — its exact signature is not shown.
- Whether `$ZodConfig.jitless` (which disables JIT schema compilation) affects error message generation.
