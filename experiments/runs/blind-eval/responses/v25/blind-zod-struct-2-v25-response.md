# v2.5 Response: blind-zod-struct-2
Date: 2026-04-16

## Question

How are schema types, checks, and errors organized in Zod's documented internal architecture?

---

## Answer

Zod's internal architecture separates concerns into three distinct subsystems — **schema types**, **checks**, and **errors** — each with its own module and design pattern. The v3 and v4 generations coexist in the codebase, with v4 introducing a more modular, type-union-driven approach compared to v3's class hierarchy.

---

### 1. Schema Types

Schema types define **what shapes of data** Zod can validate. They are organized differently across v3 and v4.

#### v3 Schema Types (`packages/zod/src/v3/types.ts`, 5138 lines)

The v3 layer uses a **class-based hierarchy** rooted in an abstract `ZodType` base class.

**Evidence from clue entries:**

- `ZodType._parse` (v3/types.ts:170) — abstract parse method. Every schema class must override this to implement its own validation logic. This is the single dispatch point for all v3 parsing.

- `ZodFirstPartySchemaTypes` (v3/types.ts:4996-4997) — a **discriminated union** enumerating all built-in schema types:
  ```
  ZodString | ZodNumber | ZodNaN | ZodBigInt | ZodBoolean | ZodDate | ZodUndefined | ...
  ```
  This union serves as the exhaustive catalog of first-party types, used for type narrowing and schema introspection.

- Each concrete schema class implements `_parse` with its own validation:
  - `ZodString._parse` — string validation
  - `ZodNumber._parse` — number validation
  - `ZodArray._parse` (v3/types.ts:2241-317) — array validation, confirmed to use `addIssueToContext` and `ZodIssueCode` constants for error reporting
  - `ZodMap.valueSchema` — returns `this._def.valueType`, showing that schemas store their config in `_def`

- `ParseInputLazyPath` class (v3/types.ts:61-85) — implements `ParseInput` with a **cached path** mechanism. This is the context object threaded through parse calls, lazily computing the JSON-path location of the current value for error reporting efficiency.

- `KeySchema` (v3/types.ts:3493) — type alias `ZodType<string | number | symbol>`, used to constrain the key types accepted by record/map schemas.

- `ZodLazy.schema` (v3/types.ts:3975) — `DELEGATE(this._def.getter -> result)`. The lazy schema pattern defers schema construction via a getter function stored in `_def`, enabling recursive and self-referential schemas without infinite loops during definition.

**Design pattern:** v3 schemas are **classes with `_def` configuration objects**. Each class owns its validation via `_parse`, and the class hierarchy provides shared behavior (`.parse()`, `.safeParse()`, `.transform()`, etc.) from the `ZodType` base.

#### v4 Schema Types (`packages/zod/src/v4/core/`)

The v4 core layer introduces **`$Zod*` prefixed types** as the internal foundation.

**Evidence from clue entries:**

- `$ZodStandardSchema` (v4/core/schemas.ts:170) — a `StandardSchemaV1.Props` type alias. This confirms v4 integrates with the [Standard Schema](https://github.com/standard-schema/standard-schema) interop specification, meaning Zod v4 schemas can be consumed by any framework that supports StandardSchemaV1.

- The mini layer's type hierarchy confirms the core types exist as extensible bases:
  - `ZodMiniType` (v4/mini/schemas.ts:6-38) `extends: $ZodType` — the mini base inherits from core's `$ZodType`
  - `_ZodMiniString` extends `$ZodString`, `_ZodMiniNumber` extends `$ZodNumber`, `ZodMiniObject` extends `$ZodObject`, etc.

**Design pattern:** v4 uses a **layered type system** where `$Zod*` core types define the internal parsing contract, and public-facing types (mini or classic) wrap them with different API surfaces.

---

### 2. Checks System

Checks define **validation constraints** applied to schema types (e.g., min length, max value, regex patterns). In v4, checks are extracted into their own module with a union-based architecture.

**Location:** `packages/zod/src/v4/core/checks.ts`

**Evidence from clue entries:**

- `$ZodChecks` (v4/core/checks.ts:1263-1269) — a **progressive union type** that aggregates all numeric/size checks:
  ```
  $ZodCheckLessThan | $ZodCheckGreaterThan | $ZodCheckMultipleOf |
  $ZodCheckNumberFormat | $ZodCheckBigIntFormat |
  $ZodCheckMaxSize | $ZodCheckMinSize
  ```
  This union is the type-level catalog of all applicable checks. Each check type is a discrete interface with its own parameters, enabling type-safe check composition.

- `$ZodStringFormatChecks` (v4/core/checks.ts:1285-1286) — a separate union for string-specific checks:
  ```
  $ZodCheckRegex | $ZodCheckLowerCase | $ZodCheckUpperCase |
  $ZodCheckIncludes | $ZodCheckStartsWith | $ZodCheckEndsWith |
  schemas.$ZodStringFormatTypes
  ```
  Note: this union references `schemas.$ZodStringFormatTypes`, creating a cross-module dependency where the checks module pulls in format-type definitions from the schemas module. This allows string format checks (email, URL, UUID, etc.) to be treated as checks rather than separate schema types.

- `$ZodCheckPropertyParams` (v4/core/api.ts:1082) — `CheckParams<checks.$ZodCheckProperty>`. This type alias in the API layer wraps check parameters, confirming that the public API references the checks module for its parameter types. The `CheckParams<>` generic provides a uniform parameter interface for all checks.

**Design pattern:** Checks are **value objects** — each check is a plain data structure (not a class) that describes a constraint. The union types (`$ZodChecks`, `$ZodStringFormatChecks`) serve as exhaustive enumerations, enabling pattern matching and type narrowing. This is a deliberate departure from v3, where checks were embedded within schema class methods.

**Relationship to schemas:** Schemas hold arrays of checks in their `_def`. During `_parse`, the schema iterates its checks and applies each one, collecting issues into the error context. The `ZodArray._parse` implementation (v3/types.ts:2241-317) demonstrates this pattern with `addIssueToContext` calls using `ZodIssueCode` discriminants.

---

### 3. Errors System

Errors define **how validation failures are represented and structured**. Zod has parallel error systems for v3 and v4.

#### v3 Errors (`packages/zod/src/v3/ZodError.ts`)

**Evidence from clue entries:**

- `ZodInvalidIntersectionTypesIssue` (v3/ZodError.ts:131-134) — `extends ZodIssueBase`. This shows v3 errors use a **class/interface inheritance pattern** where specific issue types extend a base interface. Each issue type carries a discriminant (likely via `ZodIssueCode`) for pattern matching.

- `addIssueToContext` and `ZodIssueCode` constants (referenced in ZodArray._parse at v3/types.ts:2241-317) — confirms that v3 parse methods create issues by calling `addIssueToContext` with a `ZodIssueCode` enum value, threading issues through the parse context.

**Design pattern:** v3 errors are **discriminated union members** extending `ZodIssueBase`, collected into a `ZodError` container that holds an array of issues.

#### v4 Errors (`packages/zod/src/v4/core/errors.ts`)

**Evidence from clue entries:**

- `$ZodInternalIssue` (v4/core/errors.ts:193-194) — defined as:
  ```typescript
  T extends any ? RawIssue<T> : never
  ```
  This is a **distributive conditional type** — when `T` is a union, it distributes `RawIssue<>` over each member, producing a union of raw issue types. This ensures that every issue variant gets its own `RawIssue` wrapper with correct type parameters.

- `$ZodRawIssue` (v4/core/errors.ts:207-208) — `$ZodInternalIssue<T>`. This is the public-facing type alias for internal issues, providing a cleaner name for external consumption while the distributive conditional handles the type mechanics internally.

- `$ZodErrorTree` (v4/core/errors.ts:327-328) — a tree-structured error type. This suggests v4 organizes errors **hierarchically** rather than as a flat list, which is consistent with nested schema validation where an object schema's errors contain child errors from its property schemas.

**Design pattern:** v4 errors use **conditional types for exhaustive issue generation** and **tree structures for hierarchical error reporting**. This is a significant architectural evolution from v3's flat issue array, enabling better error composition for deeply nested schemas.

---

### Cross-Cutting Relationships

```
┌──────────────────────────────────────────────────────┐
│                  Schema Types                         │
│  v3: ZodType._parse (class hierarchy)                │
│  v4: $ZodType (core) → ZodMini*/Zod* (public)       │
│                                                      │
│  Schemas hold checks in _def and iterate them        │
│  during _parse, producing issues on failure           │
├──────────────────────────────────────────────────────┤
│                  Checks                               │
│  v4/core/checks.ts                                   │
│  $ZodChecks: LessThan|GreaterThan|MultipleOf|...     │
│  $ZodStringFormatChecks: Regex|Lower|Upper|...       │
│                                                      │
│  Each check is a value object with typed params       │
│  Applied by schemas, produces errors on failure       │
├──────────────────────────────────────────────────────┤
│                  Errors                               │
│  v3: ZodIssueBase → specific issue interfaces         │
│  v4: $ZodInternalIssue (distributive conditional)    │
│      $ZodErrorTree (hierarchical composition)         │
│                                                      │
│  Errors are the output of failed check application    │
└──────────────────────────────────────────────────────┘
```

### Summary Table

| Subsystem | v3 Location | v4 Location | Pattern |
|-----------|------------|------------|---------|
| Schema types | `v3/types.ts` (5138L) | `v4/core/schemas.ts`, `v4/core/core.ts` | Class hierarchy (v3) → Layered type system (v4) |
| Checks | Embedded in schema classes | `v4/core/checks.ts` | Inline methods (v3) → Union of value objects (v4) |
| Errors | `v3/ZodError.ts` | `v4/core/errors.ts` | Flat issue array (v3) → Distributive conditional + error tree (v4) |

---

### Identified Gaps

- **MECHANISTIC gap**: The clue provides structural information (type hierarchies, union members, file locations) but does not include behavior annotations explaining *how* checks are evaluated at runtime or *how* the error tree is assembled during recursive parsing.
- **Uncovered symbols**:
  - `$ZodCheckUpperCaseParams` — parameter type for the uppercase check is not surfaced in the clue.
  - `$ZodErrorClass` — the concrete error class implementation is not detailed; only the type-level interfaces are visible.
- The relationship between `$ZodStringFormatChecks` and `schemas.$ZodStringFormatTypes` creates a circular-looking cross-module reference whose resolution mechanism is not explained in the clue.
