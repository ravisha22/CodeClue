# v2.5 Response: blind-zod-struct-1
Date: 2026-04-16

## Question

How is Zod 4 split across the `zod`, `zod/mini`, and `zod/v4/core` packages?

---

## Answer

Zod 4 is organized into a **three-layer architecture** visible in the monorepo under `packages/zod/src/v4/`. Each layer builds on the one beneath it, providing progressively richer APIs while sharing a single internal core. The clue header (`=CC v2.1 zod@HEAD 390mod 2677sym`) confirms this is a substantial codebase (390 modified files, 2,677 symbols indexed), and the TREE entry (`packages/` with 384 files across `bench/`, `docs/`, `resolution/`, `treeshake/`, `tsc/`, `zod/`) shows the monorepo layout.

### 1. Core Layer — `zod/v4/core`

**Location:** `packages/zod/src/v4/core/`

The core layer defines the foundational, framework-internal types prefixed with `$Zod*`. These are not meant to be used directly by consumers but serve as the base classes and interfaces that both `mini` and the full/classic API extend.

**Evidence from clue entries:**

- Every `ZodMini*` type in `v4/mini/schemas.ts` references a `core.$Zod*` counterpart in its `uses` field. For example:
  - `_ZodMiniString` (v4/mini/schemas.ts:80-85) — `uses: core.$ZodString`
  - `_ZodMiniNumber` (v4/mini/schemas.ts:517-523) — `uses: core.$ZodNumber` (via `$ZodNumber`)
  - `ZodMiniObject` (v4/mini/schemas.ts:814-823) — `uses: core.$ZodObject` (via `$ZodObject`)
  - `ZodMiniArray` (v4/mini/schemas.ts:783-789) — `uses: core.$ZodArray` (via `$ZodArray`)
  - `ZodMiniFunction` (v4/mini/schemas.ts:1851-1870) — `uses: core.$ZodFunction` (via `$ZodFunction`)

- The `$ZodStandardSchema` type alias is defined in `v4/core/schemas.ts:170`, confirming the core layer owns the StandardSchemaV1 integration surface.

- The checks system (`$ZodChecks` at `v4/core/checks.ts:1263-1269`) and errors system (`$ZodInternalIssue` at `v4/core/errors.ts:193-194`) are both housed in the core layer, meaning validation logic and error reporting are centralized here rather than duplicated across mini and full.

**Role:** Core provides the raw type definitions (`$ZodType`, `$ZodString`, `$ZodNumber`, `$ZodObject`, etc.), the checks/validation infrastructure, and error types. It is the single source of truth for parsing behavior.

### 2. Mini Layer — `zod/mini`

**Location:** `packages/zod/src/v4/mini/`

The mini layer provides a **lightweight public API** with reduced bundle size. It defines `ZodMini*` wrapper types that extend the core `$Zod*` types but expose a smaller method surface.

**Evidence from clue entries:**

- `ZodMiniType` (v4/mini/schemas.ts:6-38) is the base interface:
  - `extends: $ZodType` — inherits from core
  - `methods: clone, parse, parseAsync, safeParse` — exposes only essential parse methods

- A comprehensive set of schema types is provided, each following the pattern of extending both `_ZodMiniType` and the corresponding core `$Zod*` type:

  | Mini Type | Location | Extends |
  |-----------|----------|---------|
  | `_ZodMiniString` | schemas.ts:80-85 | `_ZodMiniType`, `$ZodString` |
  | `_ZodMiniNumber` | schemas.ts:517-523 | `_ZodMiniType`, `$ZodNumber` |
  | `ZodMiniObject` | schemas.ts:814-823 | `ZodMiniType`, `$ZodObject` |
  | `ZodMiniArray` | schemas.ts:783-789 | `_ZodMiniType`, `$ZodArray` |
  | `ZodMiniUnion` | schemas.ts:997-1002 | `_ZodMiniType` |
  | `ZodMiniRecord` | schemas.ts:1143-1150 | `_ZodMiniType` |
  | `ZodMiniFunction` | schemas.ts:1851-1870 | `_ZodMiniType`, `$ZodFunction` |
  | `ZodMiniEnum` | schemas.ts:1243-1248 | `_ZodMiniType` |

- Additional utility types are present: `ZodMiniNullable`, `ZodMiniOptional`, `ZodMiniReadonly`, `ZodMiniTransform`, `ZodMiniLazy`, `ZodMiniCatch`, `ZodMiniDefault`, `ZodMiniDiscriminatedUnion`, `ZodMiniExactOptional`, `ZodMiniIntersection`, `ZodMiniLiteral`, `ZodMiniNonOptional`, `ZodMiniPipe`, `ZodMiniPrefault`, `ZodMiniPromise`, `ZodMiniSet`, `ZodMiniStringFormat`, `ZodMiniSuccess`, `ZodMiniTemplateLiteral`.

- ISO format types are defined in `v4/mini/iso.ts`: `ZodMiniISODate`, `ZodMiniISODateTime`, `ZodMiniISODuration`, `ZodMiniISOTime` — all extending `ZodMiniStringFormat`, demonstrating that domain-specific string formats are layered on top of the mini string format base.

**Role:** Mini is the tree-shakeable, minimal-API entry point. It wraps core internals with a narrow public interface (parse, safeParse, clone) while omitting convenience methods available in the full API.

### 3. Full/Classic Layer — `zod` (main entry)

**Location:** `packages/zod/src/v4/classic/` (inferred) and `packages/zod/src/v3/types.ts` (legacy)

The full layer is what users get when they `import { z } from "zod"`. It provides the richest API surface with chained methods, `.describe()`, `.transform()`, `.refine()`, and other convenience features.

**Evidence from clue entries:**

- The v3 types file (`packages/zod/src/v3/types.ts`, 5138 lines) contains the legacy class-based schemas:
  - `ZodFirstPartySchemaTypes` (v3/types.ts:4996-4997) — a union of all first-party types: `ZodString | ZodNumber | ZodNaN | ZodBigInt | ZodBoolean | ZodDate | ZodUndefined...`
  - `ZodType._parse` (v3/types.ts:170) — the abstract parse method that each schema class overrides
  - Each schema class implements `_parse`: `ZodString._parse`, `ZodNumber._parse`, `ZodArray._parse`, etc.
  - `ZodLazy.schema` (v3/types.ts:3975) — `DELEGATE(this._def.getter -> result)`, showing lazy evaluation
  - `ParseInputLazyPath` class (v3/types.ts:61-85) — implements `ParseInput` with cached path for parse context

- References to `packages/zod/src/v4/classic/` in other tasks confirm the v4 classic layer exists as a parallel to the mini layer, building on the same core but with a full-featured API.

**Role:** The full layer provides backward compatibility with the v3 API style while internally delegating to v4 core for parsing logic. It is the default import and offers the complete developer experience.

### Architectural Relationship

```
┌─────────────────────────────────────┐
│         zod (full/classic)          │  ← richest API, default import
│   ZodString, ZodNumber, ZodObject   │
├─────────────────────────────────────┤
│           zod/mini                  │  ← lightweight API, tree-shakeable
│  ZodMiniString, ZodMiniNumber, ...  │
├─────────────────────────────────────┤
│          zod/v4/core                │  ← internal foundation
│  $ZodType, $ZodString, $ZodChecks  │
│  $ZodInternalIssue, $ZodErrorTree  │
└─────────────────────────────────────┘
```

Both mini and full extend core types (`$ZodType` and its specializations). Mini exposes a reduced method set (`clone`, `parse`, `parseAsync`, `safeParse`), while full provides the complete chainable API that v3 users expect.

### Identified Gaps

- **STRUCTURAL gap**: 80 symbols at L3 depth, 0 with behavior annotations — meaning we see the type hierarchy but not the runtime behavior of individual methods.
- **Uncovered**: `$InferZodRecordInput` variants — inference helpers for record input types are not surfaced in the clue.
- The full/classic v4 layer (`v4/classic/`) is referenced but its internal symbol details were not included in the clue set for this question.
