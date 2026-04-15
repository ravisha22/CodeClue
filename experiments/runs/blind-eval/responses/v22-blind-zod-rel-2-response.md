# v2.2 Response: blind-zod-rel-2
Date: 2026-04-15

## Question
How do parsing APIs, schema-level checks, and error maps relate to one another in Zod's validation pipeline?

## Answer

The clue file reveals a layered validation pipeline where parsing APIs invoke schema-level checks, which produce typed error issues collected by error containers. Below is the detailed relationship analysis.

---

### 1. Parsing APIs — The Entry Point

#### v3 — `packages/zod/src/v3/types.ts`

The parsing pipeline is rooted in `ZodType`:

- **`ZodType._parse`** (`types.ts:170`) — the abstract base parsing method that all schema types override.
- **`ZodType._parseSync`** (`types.ts:210`) — synchronous variant of parsing.
- **`ZodType._getOrReturnCtx`** (`types.ts:176`) — retrieves or creates a parsing context, used by `_parse` implementations.

Every concrete schema overrides `_parse`. The SYM section lists 30+ implementations: `ZodString._parse` (line 732), `ZodNumber._parse` (line 1370), `ZodBigInt._parse` (line 1636), `ZodDate._parse` (line 1878), `ZodArray._parse` (line 2241), `ZodUnion._parse` (line 2947), `ZodIntersection._parse` (line 3292), `ZodFunction._parse` (line 3822), `ZodEffects._parse` (line 4322), `ZodPipeline._parse` (line 4782), etc.

#### Pipeline Composition via `ZodPipeline`

`ZodPipeline._parse` (`types.ts:4782–4827`) chains schemas together:
- **Behavior**: `PRECEDENCE(ctx -> inResult -> default)`
- **Calls**: `_parse`, `_parseAsync`, `_parseSync`, `_processInputParams`
- `ZodPipeline` (`types.ts:4777–4839`) extends `ZodType` and is callable by `ZodDiscriminatedUnion` and `ZodObject`.

The `ZodType.pipe` method (`types.ts:522–524`) creates a pipeline: `DELEGATE(ZodPipeline.create -> result)`.

#### Delegation patterns in special schemas:

- **`ZodLazy._parse`** (`types.ts:3979–3985`) — `DELEGATE(lazySchema._parse -> result)`, meaning it resolves the lazy getter then delegates to the inner schema's `_parse`.
- **`ZodFunction._parse`** (`types.ts:3822–3904`) — `PRECEDENCE(ctx -> isinstance_ZodPromise -> not_parsedArgs -> default)`, calls `_parse`, `_processInputParams`, `parseAsync`, `safeParse`.

---

### 2. Schema-Level Checks — Validation Constraints

Checks are added to schemas via `_addCheck` methods, which register constraint objects:

- **`ZodString._addCheck`** (`types.ts:1050–1057`) — accepts `ZodStringCheck`, called by format validators: `base64`, `base64url`, `cidr`, `cuid`, `cuid2`, `date`, `datetime`, `email`, etc.
- **`ZodNumber._addCheck`** (`types.ts:1497`) — called by numeric constraint methods.
- **`ZodBigInt._addCheck`** (`types.ts:1749`)
- **`ZodDate._addCheck`** (`types.ts:1943`)

**Limit-setting pattern**: `ZodNumber.setLimit` (`types.ts:1482`) and `ZodBigInt.setLimit` (`types.ts:1734`) provide min/max constraints that internally use `_addCheck`.

**How checks relate to parsing**: `ZodString._parse` (`types.ts:732–1042`) has behavior `PRECEDENCE(_def_coerce -> parsedType -> check -> default)` with `ACCUMULATE(loop -> result)`. This means during parsing, the method first coerces (if configured), then validates the parsed type, then iterates through all registered checks in a loop. Each failing check contributes to the error result.

---

### 3. Error Maps — Error Customization and Structure

#### v3 Error System — `packages/zod/src/v3/ZodError.ts`

**`ZodError`** (`ZodError.ts:194–316`) extends `Error` and collects `ZodIssue[]`:
- `ZodError.constructor` (line 201–213) — accepts `ZodIssue[]`
- `ZodError.errors` (line 197–199) — getter aliasing `this.issues`
- `ZodError.flatten` (line 296) — transforms issues into a flat structure
- `ZodError.formErrors` (line 313–315) — `DELEGATE(this.flatten -> result)`
- `ZodError.format` (lines 217–264) — `PRECEDENCE(issue -> default)`, `ACCUMULATE(loop -> result)`, `TRANSFORM(map)` — iterates issues, builds a nested formatted error tree
- `ZodError.message` (line 280–282) — `DELEGATE(JSON.stringify -> result)`
- `ZodError.isEmpty` (line 284–286), `ZodError.toString` (line 277–279), `ZodError.assert` (line 271–275)

**Error customization on schemas**: `ZodType.setError` (`types.ts:354, 362`) — two overloads on the base type, allowing per-schema error message customization. This is the bridge between schemas and error maps: a schema can set a custom error that overrides default messages when checks fail.

**Error map retrieval**: `getErrorMap` exists in two versions:
- `packages/zod/src/v3/errors.ts:11–13` — v3 error map getter
- `packages/zod/src/v4/classic/compat.ts:53–55` — `DELEGATE(core.config -> result)`, indicating the v4 error map is retrieved from core configuration.

#### v4 Error System — `packages/zod/src/v4/classic/errors.ts`

**`ZodError`** (`errors.ts:9–23`) is an **interface** with methods: `addIssue` (accepts `core.$ZodIssue`), `addIssues` (accepts `core.$ZodIssue[]`), `flatten`, `format`. This v4 version references core types (`core.$ZodIssue`), showing the error structure is defined in `v4/core`.

#### v4 Core Error Utilities — `packages/zod/src/v4/core/errors.ts`

- **`flattenError`** (`core/errors.ts:262–276`) — `ACCUMULATE(loop -> result)` — iterates error issues into a flat structure.
- **`formatError`** (`core/errors.ts:290–326`) — `ACCUMULATE(loop -> result)`, `TRANSFORM(map)` — builds a formatted error tree.
- **`prettifyError`** (`core/errors.ts:435–449`) — `DELEGATE(lines.join -> result)`, `ACCUMULATE(loop -> lines)`, calls `toDotPath` — renders errors as human-readable text.

#### Typed Issue Interfaces (v3)

All extend `ZodIssueBase` and carry specific `code` discriminators:
- `ZodInvalidTypeIssue` (line 41), `ZodInvalidLiteralIssue` (line 47), `ZodUnrecognizedKeysIssue` (line 53), `ZodInvalidUnionIssue` (line 58), `ZodInvalidUnionDiscriminatorIssue` (line 63), `ZodInvalidEnumValueIssue` (line 68), `ZodInvalidArgumentsIssue` (line 74), `ZodInvalidReturnTypeIssue` (line 79), `ZodInvalidDateIssue` (line 84), `ZodInvalidStringIssue` (line 111), `ZodTooSmallIssue` (line 116), `ZodTooBigIssue` (line 124), `ZodInvalidIntersectionTypesIssue` (line 132), `ZodNotMultipleOfIssue` (line 136), `ZodNotFiniteIssue` (line 141), `ZodCustomIssue` (line 145)

---

### 4. How They Relate — The Pipeline Flow

```
Schema.parse(input)
  → ZodType._parse(input) / _parseSync(input)
    → _getOrReturnCtx(input) — create parse context
    → Type-specific validation (coerce → type-check → checks loop)
      → _addCheck constraints evaluated in sequence
      → Failures produce typed ZodIssue instances (ZodInvalidTypeIssue, etc.)
    → Issues collected into ZodError(issues[])
      → ZodType.setError can override default messages
      → getErrorMap provides global customization layer
    → ZodError provides output APIs: flatten(), format(), formErrors
```

**Key relationships**:
1. **Parsing invokes checks**: `_parse` iterates through checks added via `_addCheck` (`ZodString._parse` behavior annotation confirms this loop).
2. **Checks produce issues**: Failed checks create typed issue objects extending `ZodIssueBase`.
3. **Issues feed errors**: Issues are collected into `ZodError`, which wraps them with presentation methods.
4. **Error maps customize messages**: `ZodType.setError` and `getErrorMap` allow customization at the schema level and global level respectively.
5. **Pipeline composition**: `ZodPipeline._parse` chains multiple schemas, propagating errors through `_parseAsync`/`_parseSync`.

#### JSON Schema Conversion (Related)

`convertSchema` (`from-json-schema.ts:541–620`) and `convertBaseSchema` (`from-json-schema.ts:146–539`) convert JSON Schema into Zod schemas using `DISPATCH(type)` and `PRECEDENCE(schema -> default)`, showing the schema layer also supports external schema format ingestion.

---

### What Cannot Be Determined

- **The exact error map function signature and precedence rules** — `getErrorMap` is shown but its behavior annotations are missing; the priority between `setError`, error map, and default messages cannot be precisely ordered.
- **How v4/core's `$ZodIssue`** relates structurally to v3's `ZodIssueBase` hierarchy is not shown.
- **Whether checks in v4** use the same `_addCheck` pattern or a different mechanism — the v4 classic schemas use `params?: string | core.$ZodCheck*Params` signatures (seen in `_ZodBigInt.multipleOf` and `_ZodNumber.multipleOf`), suggesting a different check registration API.
