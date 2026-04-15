# v2.2 Response: blind-zod-rel-1
Date: 2026-04-15

## Question
What inheritance and extension relationships connect Zod's core, full, and mini schema/error types?

## Answer

The clue file reveals a multi-layered type system spanning v3 (class-based), v4/classic (interface-based), and v4/mini (interface-based) packages, each with distinct inheritance hierarchies. Below are all relationships documented in the clue.

---

### 1. v3 Full (Class-Based) — `packages/zod/src/v3/types.ts`

**Root class**: `ZodType` (`packages/zod/src/v3/types.ts:158–535`) — not shown with an explicit `extends`, but serves as the base for all v3 schema classes.

**Concrete schema classes extending ZodType**:
- `ZodString` (`types.ts:731–1339`) — `extends: ZodType`
- `ZodNumber` (`types.ts:1369–1617`) — `extends: ZodType`
- `ZodBigInt` (`types.ts:1635–1821`) — `extends: ZodType`
- `ZodUnknown` (not in FOCUS with explicit extends, but listed in SYM)

Each of these classes inherits `_parse`, `_parseSync`, `_getOrReturnCtx`, `constructor`, and the builder methods (`optional`, `nullable`, `array`, `or`, `and`, `pipe`, `promise`, `readonly`) from `ZodType`.

### 2. v3 Error Hierarchy — `packages/zod/src/v3/ZodError.ts`

**`ZodError`** (`ZodError.ts:194–316`) — `extends: Error` (the native JavaScript `Error` class). Methods: `assert`, `constructor`, `errors`, `flatten`, `formErrors`, `format`.

**Issue interfaces** — all extend `ZodIssueBase`:
- `ZodInvalidIntersectionTypesIssue` (`ZodError.ts:132–134`) — `extends: ZodIssueBase`

This establishes that all specific issue types are subtypes of a common `ZodIssueBase` interface.

### 3. v4 Mini (Interface-Based) — `packages/zod/src/v4/mini/schemas.ts`

**Two-tier base**: The mini package uses a two-level base type system:
- `ZodMiniType` (`schemas.ts:7–38`) — top-level public interface with methods: `clone`, `parse`, `parseAsync`, `safeParse`. Also calls `check`.
- `_ZodMiniType` (`schemas.ts:40–41`) — internal interface (no methods or extends shown beyond being referenced as a base).

**String specialization hierarchy**:
- `_ZodMiniString` (`schemas.ts:81–85`) — intermediate string interface.
- Types extending `_ZodMiniString`:
  - `ZodMiniEmail` (line 119), `ZodMiniGUID` (line 134), `ZodMiniCUID` (line 244), `ZodMiniCUID2` (line 261), `ZodMiniNanoID` (line 227), `ZodMiniEmoji` (line 210), `ZodMiniKSUID` (line 309), `ZodMiniIPv4` (line 326), `ZodMiniIPv6` (line 343), `ZodMiniCIDRv4` (line 360), `ZodMiniCIDRv6` (line 377), `ZodMiniMAC` (line 394), `ZodMiniBase64` (line 408), `ZodMiniBase64URL` (line 424), `ZodMiniE164` (line 440)

**Types extending `_ZodMiniType`**:
- `ZodMiniLazy` (line 1684), `ZodMiniEnum` (line 1245), `ZodMiniPromise` (line 1708), `ZodMiniSet` (line 1227), `ZodMiniSuccess` (line 1510), `ZodMiniAny` (line 701), `ZodMiniBigInt` (line 603), `ZodMiniBigIntFormat` (line 622), `ZodMiniBoolean` (line 586), `ZodMiniCatch` (line 1530), `ZodMiniCustom` (line 1728), `ZodMiniDate` (line 767), `ZodMiniDefault` (line 1433), `ZodMiniFile` (line 1323), `ZodMiniNever` (line 732), `ZodMiniUnknown` (line 715) — `extends: _ZodMiniType`

**Types with no explicit extends shown**:
- `ZodMiniArray` (line 785), `ZodMiniCodec` (line 1596), `ZodMiniDiscriminatedUnion` (line 1049), `ZodMiniIntersection` (line 1081), `ZodMiniMap` (line 1203), `ZodMiniNonOptional` (line 1485), `ZodMiniExactOptional` (line 1384), `ZodMiniCustomStringFormat` (line 471), `ZodMiniFunction` (line 1853), `ZodMiniObject` (not in this clue's FOCUS)

### 4. v4 Classic Error — `packages/zod/src/v4/classic/errors.ts`

**`ZodError`** (`errors.ts:9–23`) — an **interface** (not a class, unlike v3). Methods: `addIssue`, `addIssues`, `flatten`, `format`. The method signatures accept `core.$ZodIssue` types, indicating this interface depends on `v4/core` types.

### 5. v4 Core — `packages/zod/src/v4/core/standard-schema.ts`

**`Types` interface** appears at three locations:
- `standard-schema.ts:19–24` — base `Types` interface (no extends shown)
- `standard-schema.ts:86` — `extends: Types`
- `standard-schema.ts:141` — `extends: Types`

This suggests a self-referencing or layered `Types` interface pattern within the standard schema compliance layer.

### 6. `ZodType.setError` — `packages/zod/src/v3/types.ts`

Two overloads of `ZodType.setError` exist (lines 354 and 362), both called by `ZodType`, showing the error customization point sits on the base type.

---

### Summary of Inheritance Chains

```
v3 (classes):
  Error → ZodError
  ZodType → ZodString, ZodNumber, ZodBigInt, ...
  ZodIssueBase → ZodInvalidIntersectionTypesIssue, ...

v4/mini (interfaces):
  ZodMiniType (public)
  _ZodMiniType → ZodMiniLazy, ZodMiniEnum, ZodMiniAny, ZodMiniBigInt, ...
  _ZodMiniString → ZodMiniEmail, ZodMiniGUID, ZodMiniCUID, ...

v4/classic (interfaces):
  ZodError interface (references core.$ZodIssue)

v4/core:
  Types → Types (self-extending layered pattern)
```

### What Cannot Be Determined

- **The relationship between `_ZodMiniType` and `ZodMiniType`** is not explicitly stated as an extends relationship — both exist but the clue doesn't show `_ZodMiniType extends ZodMiniType` or vice versa. Their exact connection is unclear.
- **Whether `_ZodMiniString` extends `_ZodMiniType`** is not stated.
- **The v4/classic schema type hierarchy** (full `ZodType`, `_ZodType`, etc.) is not present in this clue's FOCUS, so the classic v4 schema inheritance chain cannot be mapped.
- **Cross-package relationships**: Whether v4/mini or v4/classic types extend or reference `v4/core` types beyond `$ZodIssue` is not shown.
- **`ZodMiniObject`** is not detailed in this clue (only mentioned at line 816–823 with no extends).
