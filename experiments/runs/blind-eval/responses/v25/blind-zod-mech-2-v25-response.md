# v2.5 Response: blind-zod-mech-2
Date: 2026-04-16

## Question

How does Zod decide which error message to emit when multiple customization layers are available?

---

## Answer

### 1. The Three-Layer Error Priority Hierarchy

The clue evidence from **$ZodConfig** (`v4/core/core.ts:121-131`) reveals the definitive priority hierarchy via inline comments in the source snippet:

```
customError?: errors.$ZodErrorMap | undefined
  — "Custom error map. Overrides config().localeError"

localeError?: errors.$ZodErrorMap | undefined
  — "Localized error map. Lowest priority."
```

This establishes three distinct layers for error message resolution, ordered from **highest to lowest priority**:

| Priority | Layer | Source | Scope |
|---|---|---|---|
| 1 (highest) | **Per-check inline message** | Individual check params (e.g., `message?: errorUtil.ErrMessage`) | Single validation check |
| 2 | **customError map** | `$ZodConfig.customError` | Global, overrides localeError |
| 3 (lowest) | **localeError map** | `$ZodConfig.localeError` | Global, lowest priority |

### 2. Per-Check Inline Messages (Priority 1)

Many validation checks accept an inline error message at the call site. Clue evidence:

- **ZodNumber.multipleOf** (`v3/types.ts:1547-1554`): Accepts `message?: errorUtil.ErrMessage` — allows the caller to specify a custom message for this specific check.
- **ZodBigInt.multipleOf** (`v3/types.ts:1792-1800`): Same pattern — `message?: errorUtil.ErrMessage`.
- **$ZodCheckMultipleOfParams** (`v4/core/api.ts:922-923`): Defined as `CheckParams<checks.$ZodCheckMultipleOf, "value" | "when">` — the `CheckParams` wrapper standardizes how check parameters (including error customization) are passed.
- **CustomErrorParams** (`v3/types.ts:55-56`): Defined as `Partial<util.Omit<ZodCustomIssue, "code">>` — provides a type for custom error parameters that can override all fields of a `ZodCustomIssue` except `code`.

When a per-check message is provided, it takes highest priority — the error maps (`customError`, `localeError`) are not consulted for that check.

### 3. Custom Error Map (Priority 2)

- **$ZodConfig.customError** (`v4/core/core.ts:121-131`): An `errors.$ZodErrorMap` that, per the source comment, "Overrides config().localeError". This map is set via the `config()` function and applies globally.
- **config() function** (`v4/core/core.ts:134-138`): Source: `if (newConfig) Object.assign(globalConfig, newConfig); return globalConfig;` — this shows that calling `config({ customError: myMap })` merges the custom error map into a global singleton via `Object.assign`. Subsequent calls accumulate or override properties on the same global object.

When no per-check message is provided, the runtime consults `customError`. If the custom error map returns a message for the given issue, that message is used.

### 4. Locale Error Map (Priority 3)

- **$ZodConfig.localeError** (`v4/core/core.ts:121-131`): An `errors.$ZodErrorMap` explicitly documented as "Lowest priority." This is the fallback for localization — it provides translated or locale-specific messages when neither a per-check message nor a `customError` map produces a result.

### 5. Error Map Function Signature

- **ZodErrorMap** (`v3/ZodError.ts:329-330`): Type signature:
  ```typescript
  (issue: ZodIssueOptionalMessage, _ctx: ErrorMapCtx) => { message: string }
  ```
  The input is a `ZodIssueOptionalMessage` (an issue without a guaranteed `message` field) and an `ErrorMapCtx` context. The output is always `{ message: string }`. This signature applies to both `customError` and `localeError` maps.

- **ZodIssueOptionalMessage** (`v3/ZodError.ts:151-152`): A union of all specific issue types (ZodInvalidTypeIssue, ZodInvalidLiteralIssue, ZodUnrecognizedKeysIssue, etc.) — each carrying a `code` discriminant but no guaranteed `message`.

- **ZodIssue** (`v3/ZodError.ts:169-170`): Defined as `ZodIssueOptionalMessage & { message: string }` — the final issue type always has a message, confirming that message resolution must occur before issues are surfaced to consumers.

### 6. Error Accumulation and Output

Once messages are resolved, errors are collected into structured output:

- **$ZodError** (`v4/core/errors.ts:214-217`): Extends `Error`. The base error container in v4.
- **ZodError** (`v4/classic/errors.ts:9-23`): Extends `$ZodError`, adds methods: `addIssue`, `addIssues`, `flatten`, `format`.
- **ZodError** (`v3/ZodError.ts:193-316`): Extends `Error`, constructor takes `ZodIssue[]`.
- **$ZodErrorClass** (`v4/core/parse.ts:5-6`): Defined as `{ new (issues: errors.$ZodIssue[]): errors.$ZodError }` — the error class constructor, confirming that errors are always constructed from an array of resolved issues.

**Message serialization:**

- **ZodError.message** (`v3/ZodError.ts:280-282`): Source:
  ```typescript
  override get message() {
    return JSON.stringify(this.issues, util.jsonStringifyReplacer, 2);
  }
  ```
  The `.message` property serializes all issues as pretty-printed JSON — not a human-friendly summary but a structured dump.

- **ZodError.toString** (`v3/ZodError.ts:277-279`): Returns `this.message`, so string coercion also produces the JSON representation.

**Formatting and flattening:**

- **ZodError.format** (`v3/ZodError.ts:217-264`): Behavior annotation from clue: `PRECEDENCE(issue -> default); ACCUMULATE(format loop -> result); TRANSFORM(map)`. This indicates that `format()` iterates over issues, accumulates them into a nested structure keyed by path, and applies a mapping transform.

- **$ZodFlattenedError** (`v4/core/errors.ts:250-254`): Defined as `_FlattenedError<T, U>` — the flattened representation separates form-level errors from field-level errors.

- **ZodSafeParseError** (`v4/classic/parse.ts:6`): `{ success: false; data?: never; error: ZodError<T> }` — the safe-parse failure wrapper, confirming that the full `ZodError` (with all resolved messages) is returned on validation failure.

### 7. Special-Purpose Error Classes

Two error classes bypass the error-map hierarchy entirely:

- **$ZodAsyncError** (`v4/core/core.ts:97-102`): Extends `Error`. Source reveals hardcoded message: `"Encountered Promise during synchronous parse. Use .parseAsync() instead."` — this is thrown as a programming error, not a validation error, and does not go through error maps.

- **$ZodEncodeError** (`v4/core/core.ts:103-109`): Extends `Error`. Source reveals hardcoded message: `"Encountered unidirectional transform during encode: ${name}"` — also a programming error with a fixed template, not subject to customization.

### 8. Issue Type Specificity

The error system uses discriminated issue types to carry structured context:

- **ZodInvalidTypeIssue**, **ZodInvalidLiteralIssue**, **ZodUnrecognizedKeysIssue**, etc. — each carries a `code` field that identifies the issue kind.
- **$ZodCheckMultipleOfInternals** (`v4/core/checks.ts:157-162`): Extends `$ZodCheckInternals`, uses `errors.$ZodIssueNotMultipleOf` — showing that each check type maps to a specific issue type, which the error maps can then match on via the `code` discriminant.

### 9. Identified Gaps

| Gap Category | Details |
|---|---|
| **Runtime resolution order** | While the priority hierarchy is established by `$ZodConfig` comments (`customError` overrides `localeError`, `localeError` is lowest), the exact imperative code that implements the fallback chain (i.e., "check per-check message → check customError → check localeError → use default") is not captured in the available source snippets. |
| **ZodDateCheck variants** | Not covered — how date-specific checks customize their error messages is undetermined. |
| **Default message generation** | The hardcoded default messages (when no error map provides a result) are not captured. There must be a base-level message generator, but its implementation is not in the clue data. |
| **Error map composition** | Whether multiple `customError` maps can be composed (e.g., merged or chained) is not evidenced. The `Object.assign` in `config()` suggests last-write-wins for the entire map, not per-issue merging. |

---

## Summary

Zod resolves error messages through a three-layer priority system established in `$ZodConfig`:

1. **Per-check inline messages** (highest) — provided at the call site via `message` parameters.
2. **`customError` map** — a global `$ZodErrorMap` that "overrides config().localeError" per source comments.
3. **`localeError` map** (lowest) — a global `$ZodErrorMap` for localization, documented as "lowest priority."

Special errors (`$ZodAsyncError`, `$ZodEncodeError`) bypass this hierarchy with hardcoded messages. All resolved issues are collected into `ZodError` (constructed from `ZodIssue[]`), which serializes its `.message` as pretty-printed JSON. The `format()` and `flatten()` methods provide alternative structured representations. The `config()` function uses `Object.assign` to merge settings into a global singleton, meaning the last call to `config()` wins for each property.
