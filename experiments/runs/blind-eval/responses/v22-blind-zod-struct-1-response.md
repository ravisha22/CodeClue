# v2.2 Response: blind-zod-struct-1
Date: 2026-04-15

## Question
How is Zod 4 split across the `zod`, `zod/mini`, and `zod/v4/core` packages?

## Answer

Based solely on the clue file, the Zod 4 codebase is split into three distinct layers within the `packages/zod/src/` directory, each providing a different interface surface over shared core logic.

### 1. `zod/v4/core` — Shared Foundation

The core package is located under `packages/zod/src/v4/core/` and provides foundational infrastructure that both the full and mini packages build upon. Evidence of this layer includes:

- **Standard Schema compliance**: Multiple `Types` interfaces are defined in `packages/zod/src/v4/core/standard-schema.ts` (lines 19–24, 86, 141), indicating core defines the standard-schema integration point.

No schema classes are shown directly from `v4/core` in the FOCUS section, but the presence of `standard-schema.ts` under this path confirms it serves as the shared base layer.

### 2. `zod/mini` — Lightweight Interface-Based API

The mini package is located at `packages/zod/src/v4/mini/schemas.ts` and provides a full set of schema types implemented as **interfaces** (not classes). Key structural observations:

- **Base type hierarchy**: `ZodMiniType` (`packages/zod/src/v4/mini/schemas.ts:7–38`) is the top-level interface, exposing methods `clone`, `parse`, `parseAsync`, and `safeParse`. A second internal interface `_ZodMiniType` (`packages/zod/src/v4/mini/schemas.ts:40–41`) serves as an intermediate type.

- **String specialization**: `_ZodMiniString` (`packages/zod/src/v4/mini/schemas.ts:81–85`) is an intermediate string interface. Numerous string-format interfaces extend it: `ZodMiniEmail` (line 119), `ZodMiniGUID` (line 134), `ZodMiniCUID` (line 244), `ZodMiniCUID2` (line 261), `ZodMiniNanoID` (line 227), `ZodMiniEmoji` (line 210), `ZodMiniKSUID` (line 309), `ZodMiniIPv4` (line 326), `ZodMiniIPv6` (line 343), `ZodMiniCIDRv4` (line 360), `ZodMiniCIDRv6` (line 377), `ZodMiniMAC` (line 394), `ZodMiniBase64` (line 408), `ZodMiniBase64URL` (line 424), `ZodMiniE164` (line 440), `ZodMiniJWT` (line 457) — all extending `_ZodMiniString`.

- **Primitive and composite types**: `ZodMiniBoolean` (line 586), `ZodMiniBigInt` (line 603), `ZodMiniBigIntFormat` (line 622), `ZodMiniDate` (line 767), `ZodMiniNever` (line 732), `ZodMiniAny` (line 701), `ZodMiniFile` (line 1323), `ZodMiniNaN` (line 1557) — all extend `_ZodMiniType`.

- **Wrapper and composition types**: `ZodMiniLazy` (line 1684), `ZodMiniEnum` (line 1245), `ZodMiniPromise` (line 1708), `ZodMiniSet` (line 1227), `ZodMiniSuccess` (line 1510), `ZodMiniCatch` (line 1530), `ZodMiniDefault` (line 1433), `ZodMiniCustom` (line 1728) — all extend `_ZodMiniType`.

- **Standalone composites** (no explicit extends shown): `ZodMiniArray` (line 785), `ZodMiniCodec` (line 1596), `ZodMiniDiscriminatedUnion` (line 1049), `ZodMiniIntersection` (line 1081), `ZodMiniMap` (line 1203), `ZodMiniNonOptional` (line 1485), `ZodMiniExactOptional` (line 1384), `ZodMiniCustomStringFormat` (line 471).

- **ISO-specific types** are in a separate file `packages/zod/src/v4/mini/iso.ts`: `ZodMiniISODate` (line 21), `ZodMiniISODateTime` (line 5), `ZodMiniISODuration` (line 53), `ZodMiniISOTime` (line 37) — these extend `ZodMiniStringFormat` (not `_ZodMiniString`).

- **Function type**: `ZodMiniFunction` (`packages/zod/src/v4/mini/schemas.ts:1853–1870`) has its own methods `input` and `output`.

### 3. `zod` (Full / Classic) — Not Directly Visible in this Clue's FOCUS

The v3 layer at `packages/zod/src/v3/types.ts` (5138 lines) contains the class-based v3 API with `ZodType` as the root class. The SYM section shows all v3 types (ZodString, ZodNumber, ZodBigInt, ZodDate, etc.) as **classes** with `_parse` and `_addCheck` methods. This contrasts with the mini package's interface-based design.

### Key Structural Differences

| Aspect | `zod/mini` | `zod` (v3/classic) |
|--------|-----------|-------------------|
| Type system | Interfaces | Classes |
| Base type | `ZodMiniType` / `_ZodMiniType` | `ZodType` (class) |
| String hierarchy | `_ZodMiniString` → format interfaces | `ZodString` class with `_addCheck` |
| Parse method | `parse`, `safeParse`, `parseAsync` on `ZodMiniType` | `_parse`, `_parseSync` on `ZodType` |
| Check mechanism | `check` called by `ZodMiniType` | `_addCheck` methods on individual classes |

### What Cannot Be Determined

- The exact content and API surface of `zod/v4/core` beyond `standard-schema.ts` is not detailed in the FOCUS section. The GAPS note states "80 symbols in L3, 0 with behavior annotations," meaning the clue provides limited depth into core internals.
- Whether the mini and classic v4 packages re-export or wrap `v4/core` types directly cannot be confirmed from this clue alone — only their separate file paths are visible.
- The relationship between `ZodMiniStringFormat` (used by ISO types in `mini/iso.ts`) and `_ZodMiniString` is not shown.
