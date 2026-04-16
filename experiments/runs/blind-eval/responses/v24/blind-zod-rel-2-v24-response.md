# v2.4 Response: blind-zod-rel-2
Date: 2026-04-16

## Question
How do parsing APIs, schema-level checks, and error maps relate to one another in Zod's validation pipeline?

## Answer

### 1. Parsing APIs as the Entry Point

The validation pipeline begins with parsing APIs that accept a schema, a value, and optional context/error configuration.

#### v4 Parse Functions
In v4, parsing is modeled as standalone function types in `packages/zod/src/v4/core/parse.ts`:

- **`$Parse`**: `<T extends schemas.$ZodType>(schema: T, value: unknown, _ctx?: schemas.ParseContext<errors.$ZodIssue>, _params?: { callee?: util.AnyFunc; Err?: $ZodErrorClass })` — takes a schema and an unknown value, with optional parse context and an error class constructor (`$Parse`, `packages/zod/src/v4/core/parse.ts:7-9`).
- **`$ParseAsync`**: same signature but returns `Promise<core.output<T>>` (`$ParseAsync`, `packages/zod/src/v4/core/parse.ts:31-32`).
- The `_params` argument accepts `Err?: $ZodErrorClass`, which is `{ new (issues: errors.$ZodIssue[]): errors.$ZodError }` — connecting parsing directly to error construction (`$ZodErrorClass`, `packages/zod/src/v4/core/parse.ts:5-6`).

#### v4 Encode/Decode (Bidirectional)
- **`$Encode`**: takes `core.output<T>` and produces `core.input<T>` — the reverse direction (`$Encode`, `packages/zod/src/v4/core/parse.ts:95-97`).
- **`$Decode`**: takes `core.input<T>` and produces `core.output<T>` (`$Decode`, `packages/zod/src/v4/core/parse.ts:109-110`).
- When a unidirectional transform is encountered during encode, `$ZodEncodeError` is thrown with message `"Encountered unidirectional transform during encode: ${name}"` (`$ZodEncodeError.constructor`, `packages/zod/src/v4/core/core.ts:105-108` source snippet).
- When a Promise is encountered during synchronous parse, `$ZodAsyncError` is thrown with message `"Encountered Promise during synchronous parse. Use .parseAsync() instead."` (`$ZodAsyncError.constructor`, `packages/zod/src/v4/core/core.ts:99-101` source snippet).

#### v3 Parse Methods
In v3, parsing is instance-based via `_parse` methods on each schema class:
- `ZodType._parse` is the abstract base (`packages/zod/src/v3/types.ts:170`).
- Each schema overrides it (e.g., `ZodString._parse` at line 732, `ZodNumber._parse` at line 1370, `ZodArray._parse` at line 2241, etc.).

#### Schema-Level Parse Methods (Mini)
`ZodMiniType` exposes `parse`, `parseAsync`, and `safeParse` methods directly on schema instances (`ZodMiniType`, `packages/zod/src/v4/mini/schemas.ts:6-38`).

### 2. Schema-Level Checks

Checks are constraints applied to schemas that run during the validation phase of parsing.

#### v4 Check Architecture
- **`$ZodCheckDef`** is the base check definition interface, which `uses: errors.$ZodErrorMap, z.util.isAborted, schemas.ParsePayload` — showing that each check definition carries its own error map reference (`$ZodCheckDef`, `packages/zod/src/v4/core/checks.ts:8-18`).
- **`$ZodCheckInternals`** has a `check` method using `errors.$ZodIssueBase, schemas.ParsePayload, util.MaybeAsync, schemas.$ZodType` — the check function receives a parse payload and can produce issues (`$ZodCheckInternals`, `packages/zod/src/v4/core/checks.ts:19-26`).
- **`$ZodChecks`**: a growing union type starting from `$ZodCheckLessThan` and accumulating `$ZodCheckGreaterThan`, `$ZodCheckMultipleOf`, `$ZodCheckNumberFormat`, `$ZodCheckBigIntFormat`, `$ZodCheckMaxSize`, `$ZodCheckMinSize` (`$ZodChecks`, `packages/zod/src/v4/core/checks.ts:1263-1269`).
- **`$ZodCheckPropertyParams`**: parameterized check for property-level validation, typed as `CheckParams<checks.$ZodCheckProperty, "property" | "schema" | "when">` (`$ZodCheckPropertyParams`, `packages/zod/src/v4/core/api.ts:1082-1083`).
- **`CheckStringFormatParams`**: parameterized for string format checks, omitting `"type" | "coerce" | "checks" | "error" | "check" | "format"` (`CheckStringFormatParams`, `packages/zod/src/v4/core/api.ts:49-50`).
- `ZodMiniType` invokes checks via its `check` call (`ZodMiniType`, `packages/zod/src/v4/mini/schemas.ts:6-38`): `calls: clone, parse, parseAsync, safeParse, check`.

#### v3 Check Pattern
In v3, checks are added via `_addCheck` methods per schema type:
- `ZodString._addCheck` (`packages/zod/src/v3/types.ts:1050`), `ZodNumber._addCheck` (line 1497), `ZodBigInt._addCheck` (line 1749), `ZodDate._addCheck` (line 1943).
- Numeric checks delegate via methods like `ZodNumber.multipleOf` → `this._addCheck` (`ZodNumber.multipleOf`, `packages/zod/src/v3/types.ts:1547-1554` — behavior: `DELEGATE(this._addCheck -> result)`).

### 3. Error Maps — The Message Customization Layer

Error maps sit between validation failures and the final error messages emitted to users.

#### v4 Error Map Configuration
The `$ZodConfig` interface defines a **two-level error map priority**:
- **`customError`**: `errors.$ZodErrorMap | undefined` — "Custom error map. Overrides `config().localeError`." (highest priority)
- **`localeError`**: `errors.$ZodErrorMap | undefined` — "Localized error map. Lowest priority."
- (`$ZodConfig`, `packages/zod/src/v4/core/core.ts:121-131` source snippet)

The `config()` function merges new configuration via `Object.assign(globalConfig, newConfig)` (`config`, `packages/zod/src/v4/core/core.ts:134-138` source snippet).

This establishes a precedence chain: **check-level error** (from `$ZodCheckDef` which `uses: errors.$ZodErrorMap`) > **`customError`** > **`localeError`**.

#### v3 Error Map
- `ZodErrorMap = (issue: ZodIssueOptionalMessage, _ctx: ErrorMapCtx) => { message: string }` — a function that receives an issue without a message and a context, returning the message string (`ZodErrorMap`, `packages/zod/src/v3/ZodError.ts:329-330`).
- `ZodIssueOptionalMessage` is a union of all issue types: `ZodInvalidTypeIssue | ZodInvalidLiteralIssue | ZodUnrecognizedKeysIssue | ZodInvalidUnionIssue | ZodInvalidUnionDiscriminatorIssue | ZodInvalidEnumValueIssue | ZodInvalidArgumentsIssue` and more (`ZodIssueOptionalMessage`, `packages/zod/src/v3/ZodError.ts:151-152`).

#### Classic Error Surface
- `ZodError extends $ZodError` with `format()` → `core.$ZodFormattedError` and `flatten()` → `core.$ZodFlattenedError` (`ZodError`, `packages/zod/src/v4/classic/errors.ts:9-23`).
- v3 `ZodError.format` has behavior `PRECEDENCE(issue -> default); ACCUMULATE(format loop -> result); TRANSFORM(map)` — showing it processes issues with a precedence model (`ZodError.format`, `packages/zod/src/v3/ZodError.ts:217-264`).

### 4. How They Relate: The Pipeline

```
User calls parse(schema, value)
        │
        ▼
  ┌─────────────────┐
  │   Schema._parse  │  (v3) or $Parse function (v4)
  │   validates type │
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  Schema checks   │  $ZodCheckInternals.check() / _addCheck
  │  (constraints)   │  Each check carries its own error map via $ZodCheckDef
  └────────┬────────┘
           │ on failure: creates issue
           ▼
  ┌─────────────────┐
  │  Error Map       │  Priority: check-level > customError > localeError
  │  Resolution      │  ZodErrorMap(issue, ctx) → { message }
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  $ZodError       │  Collects $ZodIssue[] → thrown or returned
  │  construction    │  via $ZodErrorClass constructor
  └─────────────────┘
```

### 5. Key Relationship: Checks Carry Error Maps

The critical connection is that `$ZodCheckDef` directly `uses: errors.$ZodErrorMap` (`$ZodCheckDef`, `packages/zod/src/v4/core/checks.ts:8-18`). This means each individual check can have its own error map, allowing per-check message customization. When no check-level error map is provided, the system falls back to `$ZodConfig.customError`, then `$ZodConfig.localeError`.

### 6. Constructor and Initialization

The `$constructor` interface and `init` function (`packages/zod/src/v4/core/core.ts:7-51` source snippet) show how schemas are instantiated:
- `init` sets up `_zod` with `{ def, constr, traits }`, runs the `initializer`, and binds prototype methods.
- The `_` constructor function processes deferred initialization callbacks.
- `input<T>` and `output<T>` utility types extract I/O types from `_zod` metadata (`input`, `packages/zod/src/v4/core/core.ts:117`; `output`, line 118 source snippet).

### What Cannot Be Determined

- The exact runtime execution order within `$Parse` — how it invokes schema internals, runs checks, and applies error maps — is not shown (only type signatures are available).
- Whether the check-level `$ZodErrorMap` in `$ZodCheckDef` truly takes precedence over `$ZodConfig.customError` at runtime — this is inferred from the `$ZodConfig` doc comments but the actual resolution logic is not in the clue file.
- How `ParsePayload` is structured and flows through the check pipeline.
- The relationship between v3's `addIssueToContext` and v4's issue creation mechanism.
- How `z.util.isAborted` (referenced in `$ZodCheckDef`) affects check execution flow.
