# v2.5 Response: blind-zod-rel-2
Date: 2026-04-16

## Question

How do parsing APIs, schema-level checks, and error maps relate to one another in Zod's validation pipeline?

---

## Answer

Zod's validation pipeline is a three-stage system: **parsing APIs** invoke schemas, **schema-level checks** perform constraint validation, and **error maps** transform raw issues into user-facing messages. These stages are connected through shared error types and a configuration-driven priority system.

### 1. Parsing APIs — Entry Points

Parsing APIs are the external interface through which user data enters the validation pipeline.

**V4 Classic parse result types (`v4/classic/parse.ts`):**

- `ZodSafeParseError` (line 6): `{ success: false; data?: never; error: ZodError<T> }` — the failure branch of safe parsing. The `error` field holds a `ZodError`, which is the classic layer's enriched error type.
- The complementary success type would be `{ success: true; data: T }`, forming a discriminated union for `safeParse` results.

**Error construction pattern (`v4/core/parse.ts:5-6`):**

- `$ZodErrorClass = { new (issues: errors.$ZodIssue[]): errors.$ZodError }` — this is a constructor signature, not a class. It defines the contract for how errors are instantiated from issue arrays. This decouples error construction from any specific error class, allowing both core (`$ZodRealError`) and classic (`ZodError`) to fulfill the contract.

**Schema initialization (`v4/core/core.ts:22-51`):**

- The `init()` function initializes schema instances by populating the `_zod` property with:
  - `def` — the schema definition
  - `constr` — the constructor reference
  - `traits` — trait mixins for the schema
- This initialization is the bridge between schema construction and parse-time behavior.

**Parse-time error branching:**

- `$ZodAsyncError` (`v4/core/core.ts:97-102`, extends `Error`) is thrown when a `Promise` is encountered during synchronous `parse()`. This guards the sync parse path from schemas that require async resolution.
- `$ZodEncodeError` (`v4/core/core.ts:103-109`, extends `Error`) is thrown when attempting to `encode()` through a unidirectional transform. This prevents invalid reverse operations.

Both are operational errors (not validation errors) and extend `Error` directly, not `$ZodError`.

### 2. Schema-Level Checks — Constraint Validation

Checks are the individual constraint validators that run during schema parsing. They are composable units attached to schema definitions.

**The checks union (`v4/core/checks.ts:1263-1269`):**

`$ZodChecks` is a large discriminated union type encompassing all built-in check types:

| Check Type | Purpose |
|------------|---------|
| `$ZodCheckLessThan` | Numeric upper bound |
| `$ZodCheckGreaterThan` | Numeric lower bound |
| `$ZodCheckMultipleOf` | Divisibility constraint |
| `$ZodCheckNumberFormat` | Number format (int, float, finite, safe) |
| `$ZodCheckBigIntFormat` | BigInt-specific format checks |
| `$ZodCheckMaxSize` | Collection/string max length |
| `$ZodCheckMinSize` | Collection/string min length |

**Check parameter types:**

- `$ZodCheckPropertyParams` (`v4/core/api.ts:1082-1083`): `CheckParams<checks.$ZodCheckProperty>` — parameterizes property-level checks for object schemas.
- `CheckStringFormatParams` (`v4/core/api.ts:49-50`): Parameter type for string format checks (email, URL, UUID, etc.).

These parameter types provide the configuration interface for attaching checks to schemas. They bridge the gap between the user-facing API (e.g., `z.string().email()`) and the internal check type system.

**Relationship to parsing:** When a parse is executed, each check attached to the schema runs against the input value. If a check fails, it produces a `$ZodIssue` which is accumulated into the issues array that eventually populates a `$ZodError`.

### 3. Error Maps — Message Transformation

Error maps control how raw validation issues are transformed into human-readable error messages. They operate through a **priority system** defined in configuration.

**V3 error map signature (`v3/ZodError.ts:329-330`):**

```
ZodErrorMap = (issue: ZodIssueOptionalMessage, _ctx: ErrorMapCtx) => { message: string }
```

This signature shows that error maps receive an issue (without a finalized message) and a context object, and return the message string. The issue contains structural information (code, path, etc.) while the map produces the human-readable text.

**V4 configuration and priority (`v4/core/core.ts:121-131`):**

`$ZodConfig` defines the error map priority chain:

| Config Field | Priority | Role |
|-------------|----------|------|
| `customError` | Highest | User-provided `errors.$ZodErrorMap`; overrides all other message sources |
| `localeError` | Lowest | Locale-specific default messages; used as fallback |
| `jitless` | N/A | Performance flag, not error-related |

The `config()` function (`v4/core/core.ts:134-138`) merges user configuration into a global `globalConfig` object, establishing the error map chain at initialization time.

**Error map resolution order:**

1. **Issue-level message** — if a check or schema provides an explicit message, it takes precedence
2. **`customError` map** — the user's custom error map is consulted next
3. **`localeError` map** — the locale-specific default map is the final fallback

This is confirmed by `ZodError.format` (`v3/ZodError.ts:217-264`), which shows the behavior pattern: `PRECEDENCE(issue -> default); ACCUMULATE(format loop -> result); TRANSFORM(map)`. Issues are iterated, messages are accumulated into a result tree, and the error map transforms issue codes into messages.

### 4. How the Three Components Connect

The pipeline flows as follows:

```
User Input
    │
    ▼
┌─────────────────────────────┐
│  Parsing API                │  parse() / safeParse() / parseAsync()
│  (v4/classic/parse.ts)      │
│                             │  Operational guards:
│                             │  ├── $ZodAsyncError (sync + async schema)
│                             │  └── $ZodEncodeError (unidirectional encode)
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  Schema init + validation   │  init() populates _zod { def, constr, traits }
│  (v4/core/core.ts:22-51)   │
│                             │
│  For each check in schema:  │
│  ├── $ZodCheckLessThan      │
│  ├── $ZodCheckMinSize       │  Each failed check → $ZodIssue
│  ├── $ZodCheckNumberFormat  │
│  └── ...($ZodChecks union)  │
└─────────────┬───────────────┘
              │ issues: $ZodIssue[]
              ▼
┌─────────────────────────────┐
│  Error Construction         │  $ZodErrorClass pattern:
│  (v4/core/parse.ts:5-6)    │  new(issues) → $ZodError
│                             │
│  Error map application:     │
│  1. Issue explicit message  │  (highest priority)
│  2. customError map         │  ($ZodConfig.customError)
│  3. localeError map         │  ($ZodConfig.localeError, lowest)
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  Error Result               │
│                             │
│  Core: $ZodError            │  (v4/core/errors.ts:214-227)
│    └── $ZodRealError        │  (v4/core/errors.ts:248)
│                             │
│  Classic: ZodError          │  (v4/classic/errors.ts:9-23)
│    methods: addIssue,       │  extends $ZodError
│    addIssues, flatten,      │
│    format                   │
│                             │
│  Flattened view:            │
│  $ZodFlattenedError         │  (v4/core/errors.ts:250-254)
│  = _FlattenedError<T, U>   │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  Parse Result (classic)     │
│  ZodSafeParseError<T>       │  { success: false, error: ZodError<T> }
│  (v4/classic/parse.ts:6)    │
└─────────────────────────────┘
```

### 5. Cross-Version Comparison

**V3 (`v3/ZodError.ts`, `v3/types.ts`):**

- `ZodError` (lines 193-316) extends `Error` directly (no `$ZodError` intermediary).
- `ZodError.format` (lines 217-264) applies the error map with the `PRECEDENCE → ACCUMULATE → TRANSFORM` pattern.
- `ZodErrorMap` (line 329-330) is the map signature.
- `ZodPipelineDef` (lines 4764-4777) extends `ZodTypeDef`, showing that pipeline schemas participate in the same type definition system.
- The `_parse` method on `ZodType` (line 170) is the extension point — each concrete schema (ZodString, ZodNumber, etc.) overrides `_parse` to implement its validation.

**V4 differences:**

- Error hierarchy gains an intermediary: `Error` → `$ZodError` → `ZodError` (classic) / `$ZodRealError` (core).
- Error maps are configured globally via `$ZodConfig` rather than passed per-parse.
- Checks are formalized as a union type (`$ZodChecks`) with explicit parameter types, replacing v3's more ad-hoc check system.
- Input/output type extractors (`v4/core/core.ts:117-118`) provide type-level access to schema I/O types.

### 6. Key Integration Points

1. **Checks → Issues**: Each `$ZodCheck*` failure produces a `$ZodIssue` with a specific issue code. The check type determines the issue shape.

2. **Issues → Error Map**: The error map receives issues with optional messages. The `$ZodConfig` priority chain (`customError` > `localeError`) determines which map produces the final message.

3. **Issues → Error Object**: The `$ZodErrorClass` constructor pattern (`new(issues) → $ZodError`) aggregates issues into an error object. The classic `ZodError` adds `flatten` and `format` for structured access.

4. **Error Object → Parse Result**: `ZodSafeParseError` wraps the error in a discriminated union result, providing a type-safe way to handle failures without exceptions.

### 7. Identified Gaps

- **MECHANISTIC**: The internal logic of how checks are iterated during parsing, how the error map is invoked per-issue, and how issues are merged from nested schemas (e.g., object properties, union branches) requires examining function bodies not covered by the clue entries.
- **Uncovered parameter types**: `$ZodCheckBigIntFormatParams`, `$ZodCheckEndsWithParams`, `$ZodCheckGreaterThanParams` are referenced but their structures are not detailed in the available evidence.
- **Pipeline behavior**: How `ZodPipelineDef` chains parsing stages and propagates/merges errors between pipeline steps is not fully covered.
