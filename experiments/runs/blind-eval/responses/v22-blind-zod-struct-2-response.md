# v2.2 Response: blind-zod-struct-2
Date: 2026-04-15

## Question
How are schema types, checks, and errors organized in Zod's documented internal architecture?

## Answer

Based solely on the clue file, Zod organizes schema types, checks, and errors across three main file areas, with a clear class/interface hierarchy and distinct patterns for validation logic.

---

### 1. Schema Types Organization

#### v3 Layer — Class Hierarchy in `packages/zod/src/v3/types.ts` (5138 lines)

All v3 schema types are **classes** extending a common base `ZodType` (`packages/zod/src/v3/types.ts:158–535`):

- **`ZodType`** is the root. It defines methods: `and`, `array`, `brand`, `constructor`, `default`, `optional`, `nullable`, `or`, `pipe`, `promise`, `readonly`, and `array` — each delegating to a specialized type's `create` method.
  - `ZodType.optional` → `DELEGATE(ZodOptional.create)` (line 444–446)
  - `ZodType.nullable` → `DELEGATE(ZodNullable.create)` (line 447–449)
  - `ZodType.array` → `DELEGATE(ZodArray.create)` (line 453–455)
  - `ZodType.or` → `DELEGATE(ZodUnion.create)` (line 460–462)
  - `ZodType.and` → `DELEGATE(ZodIntersection.create)` (line 464–466)
  - `ZodType.pipe` → `DELEGATE(ZodPipeline.create)` (line 522–524)
  - `ZodType.promise` → `DELEGATE(ZodPromise.create)` (line 456–458)
  - `ZodType.readonly` → `DELEGATE(ZodReadonly.create)` (line 525–527)

- **Concrete schema classes** extending `ZodType`:
  - `ZodString` (`types.ts:731–1339`) — extends `ZodType`, methods: `base64`, `base64url`, `cidr`, `cuid`, `cuid2`, `date`, etc.
  - `ZodNumber` (`types.ts:1369–1617`) — extends `ZodType`, methods: `finite`, `gt`, `gte`, `int`, `lt`, `lte`, etc.
  - `ZodBigInt` (`types.ts:1635–1821`) — extends `ZodType`, methods: `gt`, `gte`, `lt`, `lte`, `maxValue`, `minValue`.

- **Wrapper types** that unwrap an inner schema: `ZodOptional.unwrap` (line 4498), `ZodNullable.unwrap` (line 4538), `ZodBranded.unwrap` (line 4758), `ZodPromise.unwrap` (line 4240), `ZodReadonly.unwrap` (line 4896).

- **Parsing**: Every schema type implements a `_parse` method. `ZodType._parse` (line 170) is the base; `ZodType._parseSync` (line 210) is the synchronous variant. Individual types override `_parse` (e.g., `ZodString._parse` at line 732, `ZodNumber._parse` at line 1370, `ZodEffects._parse` at line 4322, etc.).

#### v4 Classic Layer

The v4 classic layer provides a `Types` interface in `packages/zod/src/v4/core/standard-schema.ts` (lines 19–24, 86, 141), and JSON schema conversion logic in `packages/zod/src/v4/classic/from-json-schema.ts` via `convertSchema` (line 541–620) and `convertBaseSchema` (line 146–539).

---

### 2. Checks Organization

Checks are the validation constraints added to schema types. They follow a consistent pattern:

- **`_addCheck` method**: Present on types that support validation constraints:
  - `ZodString._addCheck` (`types.ts:1050–1057`) — accepts a `ZodStringCheck`, calls `_addCheck` and `ZodString` internally. Called by `base64`, `base64url`, `cidr`, `cuid`, and many other format validators.
  - `ZodNumber._addCheck` (`types.ts:1497`)
  - `ZodBigInt._addCheck` (`types.ts:1749`)
  - `ZodDate._addCheck` (`types.ts:1943`)

- **`setLimit` pattern**: `ZodNumber.setLimit` (line 1482) and `ZodBigInt.setLimit` (line 1734) provide numeric range constraints.

- **Value accessors**: `ZodNumber.minValue`/`maxValue` (lines 1577, 1587), `ZodBigInt.minValue`/`maxValue` (lines 1800, 1810).

- **String parsing behavior**: `ZodString._parse` (line 732–1042) uses `PRECEDENCE(_def_coerce -> parsedType -> check -> default)` with `ACCUMULATE(loop -> result)`, meaning it iterates through checks in a loop, accumulating results.

---

### 3. Errors Organization

#### v3 Error Types — `packages/zod/src/v3/ZodError.ts`

- **`ZodError`** (`ZodError.ts:194–316`) extends JavaScript `Error`. Core methods:
  - `constructor` — accepts `ZodIssue[]`
  - `errors` (line 197–199) — getter, aliases `this.issues`
  - `flatten` (line 296) — called by `formErrors`
  - `formErrors` (line 313–315) — `DELEGATE(this.flatten -> result)`
  - `format` (lines 215, 217–264) — uses `PRECEDENCE(issue -> default)`, `ACCUMULATE(loop -> result)`, `TRANSFORM(map)` to build a nested error structure

- **Issue type interfaces** — all extend `ZodIssueBase`:
  - `ZodInvalidIntersectionTypesIssue` (`ZodError.ts:132–134`)

- **`ZodMap.keySchema`** and **`ZodMap.valueSchema`** (lines 3597–3603) are called by `ZodDiscriminatedUnion`, `ZodMap`, `ZodObject`, and `ZodRecord`, showing cross-schema structural querying used during validation.

- Similarly, **`ZodRecord.keySchema`** and **`ZodRecord.valueSchema`** (lines 3508–3514) share the same caller set.

#### v4 Classic Error Types — `packages/zod/src/v4/classic/errors.ts`

- **`ZodError`** (`errors.ts:9–23`) is an **interface** (not a class) with methods: `addIssue`, `addIssues`, `flatten`, `format`. These accept `core.$ZodIssue` types, indicating delegation to the `v4/core` layer.

---

### 4. Cross-Layer Relationships

- **Lazy schemas**: `ZodLazy.schema` (`types.ts:3975–3979`) uses `DELEGATE(this._def.getter -> result)` and is called by `ZodDiscriminatedUnion`, `ZodLazy`, and `ZodObject` — meaning objects and unions resolve lazy references at parse time.

- **JSON schema conversion**: `convertSchema` and `convertBaseSchema` (`from-json-schema.ts`) use `GUARD`, `DISPATCH(type)`, and `PRECEDENCE` patterns to convert external JSON Schema into Zod schemas, calling `resolveRef` for `$ref` resolution.

---

### What Cannot Be Determined

- The full list of issue types beyond `ZodInvalidIntersectionTypesIssue` is not shown in this clue's FOCUS section (the SYM section lists "1103 more symbols" truncated).
- How `v4/core` internally defines `$ZodIssue` or error base types is not visible — only that `v4/classic/errors.ts` references `core.$ZodIssue`.
- The 80 symbols noted in GAPS have 36 with behavior annotations, meaning the remaining 44 focused symbols lack behavioral detail.
