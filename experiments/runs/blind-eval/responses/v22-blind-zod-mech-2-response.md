# v2.2 Response: blind-zod-mech-2
Date: 2026-04-15

## Question
How does Zod decide which error message to emit when multiple customization layers are available?

## Answer

The clue file and source snippets reveal multiple error customization layers in Zod, though the exact precedence algorithm is only partially visible. Below is a synthesis of all available evidence.

---

### 1. Error Customization Layers Identified

#### Layer 1: Schema-Level Error Override — `ZodType.setError`

`ZodType.setError` (`packages/zod/src/v3/types.ts:354` and `types.ts:362`) — two overloads exist on the base `ZodType` class, both called by `ZodType`. This allows any schema to set a custom error that overrides default messages when validation fails. The exact signature and behavior body are not provided in the source snippets, but its placement on `ZodType` means it is available to all schema types.

#### Layer 2: Per-Check Inline Messages

Individual check methods accept an optional `message` parameter:

- **v3**: `ZodNumber.multipleOf(value: number, message?: errorUtil.ErrMessage)` (`types.ts:1547–1554`) — the `message` parameter allows per-check error customization. Behavior: `DELEGATE(this._addCheck -> result)`.
- **v3**: `ZodBigInt.multipleOf(value: bigint, message?: errorUtil.ErrMessage)` (`types.ts:1792–1800`) — same pattern with `DELEGATE(this._addCheck -> result)`.
- **v4**: `_ZodNumber.multipleOf(value: number, params?: string | core.$ZodCheckMultipleOfParams)` (`schemas.ts:823`) — the `params` can be a simple `string` (the error message) or a structured `core.$ZodCheckMultipleOfParams` object.
- **v4**: `_ZodBigInt.multipleOf(value: bigint, params?: string | core.$ZodCheckMultipleOfParams)` (source snippet at `schemas.ts:949`).
- **v4**: `ZodArray.max(maxLength: number, params?: string | core.$ZodCheckMaxLengthParams)` (source snippet at `schemas.ts:1135`).
- **v4**: `ZodArray.length(len: number, params?: string | core.$ZodCheckLengthEqualsParams)` (source snippet at `schemas.ts:1136`).

The v4 pattern of `params?: string | core.$ZodCheck*Params` unifies simple string messages and structured parameter objects into a single parameter.

#### Layer 3: Global Error Map — `getErrorMap`

- **v3**: `getErrorMap` (`packages/zod/src/v3/errors.ts:11–13`) — retrieves the globally-configured error map function.
- **v4**: `getErrorMap` (`packages/zod/src/v4/classic/compat.ts:53–55`) — behavior: `DELEGATE(core.config -> result)`, meaning the v4 error map is stored in core configuration and retrieved via `core.config`.

The error map provides a global customization layer that can transform any issue into a custom message. The delegation to `core.config` in v4 suggests a centralized configuration system.

#### Layer 4: Issue-Type-Specific Codes

Each issue type carries a discriminator `code` field that determines the default error message category. From the source snippets:

- `ZodInvalidTypeIssue` — `code: ZodIssueCode.invalid_type`, includes `expected` and `received` parsed types.
- `ZodInvalidLiteralIssue` — `code: ZodIssueCode.invalid_literal`, includes `expected` and `received`.
- `ZodUnrecognizedKeysIssue` — `code: ZodIssueCode.unrecognized_keys`, includes `keys: string[]`.
- `ZodInvalidUnionIssue` — `code: ZodIssueCode.invalid_union`, includes `unionErrors: ZodError[]`.
- `ZodInvalidUnionDiscriminatorIssue` — `code: ZodIssueCode.invalid_union_discriminator`, includes `options: Primitive[]`.
- `ZodInvalidEnumValueIssue` — `code: ZodIssueCode.invalid_enum_value`, includes `received` and `options`.
- `ZodInvalidArgumentsIssue` — `code: ZodIssueCode.invalid_arguments`, includes `argumentsError: ZodError`.
- `ZodInvalidReturnTypeIssue` — `code: ZodIssueCode.invalid_return_type`, includes `returnTypeError: ZodError`.
- `ZodInvalidDateIssue` — `code: ZodIssueCode.invalid_date`.
- `ZodInvalidStringIssue` — `code: ZodIssueCode.invalid_string`, includes `validation: StringValidation`.
- `ZodTooSmallIssue` — `code: ZodIssueCode.too_small`, includes `minimum`, `inclusive`, `exact`, `type`.
- `ZodTooBigIssue` — `code: ZodIssueCode.too_big`, includes `maximum`, `inclusive`, `exact`, `type`.
- `ZodInvalidIntersectionTypesIssue` — `code: ZodIssueCode.invalid_intersection_types`.
- `ZodNotMultipleOfIssue` — `code: ZodIssueCode.not_multiple_of`, includes `multipleOf: number | bigint`.
- `ZodNotFiniteIssue` — `code: ZodIssueCode.not_finite`.
- `ZodCustomIssue` — `code: ZodIssueCode.custom`, includes `params?: { [k: string]: any }` — this is the escape hatch for fully custom error scenarios.

All issue types extend `ZodIssueBase`, which likely provides common fields like `path` and `message`.

---

### 2. How Checks Feed Into Error Messages

The `_addCheck` mechanism connects checks to errors:

1. Schema methods (e.g., `multipleOf`, `min`, `max`) call `_addCheck` with a check descriptor and optional message.
2. During `_parse`, checks are evaluated in a loop. `ZodString._parse` (`types.ts:732–1042`) shows: `PRECEDENCE(_def_coerce -> parsedType -> check -> default)` with `ACCUMULATE(loop -> result)` — checks are the third priority after coercion and type validation, and results accumulate.
3. Each failing check produces a typed issue (e.g., `ZodTooSmallIssue`, `ZodNotMultipleOfIssue`).

---

### 3. Error Output and Presentation

Once issues are collected into a `ZodError`, multiple presentation methods are available:

- **`ZodError.message`** (source snippet, `ZodError.ts:280–282`):
  ```typescript
  override get message() {
    return JSON.stringify(this.issues, util.jsonStringifyReplacer, 2);
  }
  ```
  The default `message` is a pretty-printed JSON serialization of all issues.

- **`ZodError.toString`** (source snippet, `ZodError.ts:277–279`) — delegates to `this.message`.

- **`ZodError.errors`** (source snippet, `ZodError.ts:197–199`) — `get errors() { return this.issues; }` — aliases `issues`.

- **`ZodError.isEmpty`** (source snippet, `ZodError.ts:284–286`) — `this.issues.length === 0`.

- **`ZodError.flatten`** — transforms issues into a flat structure. v4 core provides `flattenError` (`core/errors.ts:262–276`) with `ACCUMULATE(loop -> result)`.

- **`ZodError.format`** — builds a nested error tree. v3 (`ZodError.ts:217–264`) uses `PRECEDENCE(issue -> default)`, `ACCUMULATE(loop -> result)`, `TRANSFORM(map)`. v4 core provides `formatError` (`core/errors.ts:290–326`) with the same pattern.

- **`prettifyError`** (`core/errors.ts:435–449`) — `DELEGATE(lines.join -> result)`, `ACCUMULATE(loop -> lines)` with `toDotPath` — renders errors into human-readable dot-path lines.

- **`ZodError.formErrors`** (source snippet, `ZodError.ts:313–315`) — `get formErrors() { return this.flatten(); }` — convenience alias.

#### v4 Classic `ZodError` Interface

The v4 `ZodError` (source snippet, `errors.ts:9–23`) marks several methods as `@deprecated`:
- `format()` — deprecated in favor of `z.treeifyError(err)`.
- `flatten()` — deprecated in favor of `z.treeifyError(err)`.
- `addIssue()` — deprecated, recommends pushing directly to `.issues`.
- `addIssues()` — deprecated, same recommendation.
- `isEmpty` — deprecated, recommends `err.issues.length === 0`.

This shows v4 is moving toward simpler error access patterns and external utility functions.

---

### 4. Inferred Precedence of Error Message Resolution

Based on available evidence, the likely precedence (highest to lowest) is:

1. **Per-check inline message** — provided via `message` (v3) or `params` (v4) when calling methods like `multipleOf`, `max`, `min`.
2. **Schema-level `setError`** — set on the schema via `ZodType.setError`, potentially overriding all checks on that schema.
3. **Global error map** — retrieved via `getErrorMap`, provides a fallback customization layer for all schemas.
4. **Default issue-code-based message** — generated from the issue type's `code` field and associated data.

**Important caveat**: This precedence is **inferred** from the structural relationships in the clue. The clue does not contain the actual resolution logic that combines these layers (e.g., the error map invocation code or the `_addCheck` body that decides which message to use). The GAPS section confirms: "type: MECHANISTIC (body logic needed for full answer)" with only 20 of 80 symbols having behavior annotations.

---

### 5. `ZodError.constructor` — Issue Assembly

From the source snippet (`ZodError.ts:201–213`):
```typescript
constructor(issues: ZodIssue[]) {
    super();
    const actualProto = new.target.prototype;
    if (Object.setPrototypeOf) {
        Object.setPrototypeOf(this, actualProto);
    } else {
        (this as any).__proto__ = actualProto;
    }
    this.name = "ZodError";
    this.issues = issues;
}
```
The constructor takes a pre-assembled `ZodIssue[]` array and stores it directly. The prototype manipulation ensures correct `instanceof` behavior when extending `Error`. This means error message resolution happens **before** `ZodError` construction — the issues array arrives with messages already determined.

### 6. `ZodError.assert` — Type Guard

From the source snippet (`ZodError.ts:271–275`):
```typescript
static assert(value: unknown): asserts value is ZodError {
    if (!(value instanceof ZodError)) {
        throw new Error(`Not a ZodError: ${value}`);
    }
}
```
A static type guard utility, not involved in message resolution.

---

### What Cannot Be Determined

- **The exact precedence algorithm**: The body of `_addCheck`, the error map invocation logic, and how `setError` interacts with per-check messages are not included in the clue or source snippets. The inferred precedence above is a best-effort reconstruction.
- **`errorUtil.ErrMessage` type**: Referenced in v3 method signatures but not defined in the clue — it may support string messages, objects with `message` fields, or functions.
- **`core.$ZodCheck*Params` structure**: The v4 params objects (e.g., `$ZodCheckMultipleOfParams`) are referenced but not defined, so we cannot see what fields beyond a message they support.
- **How `ZodCustomIssue.params`** interacts with the error map — the `params?: { [k: string]: any }` field suggests custom issues can carry arbitrary data for error map consumption, but the mechanism is not shown.
- **`quotelessJson`** (source snippet, `ZodError.ts:175–178`) — a utility that formats JSON without key quotes; its role in error messages is unclear from the clue.
