# v2.2 Response: blind-zod-mech-1
Date: 2026-04-15

## Question
What exact unknown-key and object-composition behaviors does Zod apply when parsing object schemas?

## Answer

The clue file provides detailed evidence of Zod's unknown-key handling modes and object-composition methods across both v3 and v4 layers.

---

### 1. Unknown-Key Handling Modes

#### v4 Classic — `ZodObject` (`packages/zod/src/v4/classic/schemas.ts:1177–1255`)

The `ZodObject` interface exposes **four distinct unknown-key handling methods**:

- **`ZodObject.strip`** (`schemas.ts:1199`) — removes unrecognized keys from the output. Called by `ZodObject` itself.
- **`ZodObject.strict`** (`schemas.ts:1196`) — rejects input containing unrecognized keys (raises an error). Called by `ZodObject`.
- **`ZodObject.passthrough`** (`schemas.ts:1191`) — passes unrecognized keys through to the output unchanged. Called by `ZodObject`.
- **`ZodObject.loose`** (`schemas.ts:1193`) — another mode for lenient key handling. Called by `ZodObject`.
- **`ZodObject.catchall`** (`schemas.ts:1188`) — signature: `catchall(schema: T)` — validates unrecognized keys against a provided schema rather than stripping, rejecting, or passing them.

These methods are all listed in the `calls` of `ZodObject`: `extend, keyof, loose, passthrough, strict, strip`.

#### v3 — `ZodObject` (`packages/zod/src/v3/types.ts:2452–2453`)

The v3 `ZodObject` is also present with calls to `constructor`, `path`, `ParseInputLazyPath`, `_parse`, `element`, `max`, `min`, `nonempty`. It is called by `deepPartialify`. However, the v3 clue does not show explicit `strip`/`strict`/`passthrough`/`loose` methods in the FOCUS section — these appear to be a v4 explicit API.

#### v3 Error Integration

`ZodUnrecognizedKeysIssue` is not shown in this particular clue's FOCUS, but the `ZodObjectDef` interface (`types.ts:2370–2381`) and `ZodUnknownDef` (`types.ts:2133–2137`, `extends: ZodTypeDef`) are present, indicating the v3 layer has dedicated definitions for how unknown keys are configured.

#### `ZodUnknown` — The "accept anything" Schema

Separate from object-key handling, `ZodUnknown` represents a schema that accepts any value:
- **v3**: `ZodUnknown` (`types.ts:2137–2152`) — `extends: ZodType`, calls `_parse`, `processCreateParams`.
- **v3**: `ZodUnknown._parse` (`types.ts:2140–2144`) — behavior: `DELEGATE(OK -> result)` — simply passes any input through as valid.
- **v4 classic**: `ZodUnknown` (`schemas.ts:1063`) — `extends: _ZodType`.
- **v4 mini**: `ZodMiniUnknown` (`mini/schemas.ts:715–717`) — `extends: _ZodMiniType`.
- Both v4 `unknown` factory functions (`schemas.ts:1070–1072` and `mini/schemas.ts:727–729`) delegate: `DELEGATE(core._unknown -> result)`, showing both flavors use the shared core implementation.

---

### 2. Object-Composition Behaviors

#### v4 Classic `ZodObject` Composition Methods

- **`ZodObject.extend`** (`schemas.ts:1201`) — signature: `extend(shape: U)` — adds new properties to an object schema. Called by `ZodObject`.
- **`ZodObject.merge`** (`schemas.ts:1210`) — signature: `merge(other: U)` — combines two object schemas into one.
- **`ZodObject.keyof`** (`schemas.ts:1186`) — extracts the keys of the object schema as a schema (likely an enum of keys). Called by `ZodObject`.

#### Optional and Exact-Optional Properties

- **`ZodExactOptional`** (`schemas.ts:1851–1856`) — an interface with an `unwrap` method. Created via `exactOptional(innerType: T)` (`schemas.ts:1868–1873`), which calls `ZodExactOptional`. Called by `ZodType`.
- **`ZodType.exactOptional`** (`schemas.ts:103`) — a method on the base type, so any schema can be made exact-optional.
- **`ZodExactOptional.unwrap`** (`schemas.ts:1855`) — called by `ZodArray`, `ZodCatch`, `ZodDefault`, `ZodExactOptional`, `ZodLazy`, `ZodNonOptional`, `ZodNullable`, `ZodOptional` — showing widespread integration.

- **`ZodMiniExactOptional`** (`mini/schemas.ts:1384–1388`) — the mini equivalent, called by `exactOptional`.
- **`ZodMiniObject`** (`mini/schemas.ts:816–823`) — the mini object interface (no methods shown in FOCUS).

- **v3 wrappers**: `ZodOptional` (with `_parse` at line 4490 and `unwrap` at line 4498) and `ZodNullable` (with `_parse` at line 4530 and `unwrap` at line 4538) handle optional/nullable property wrapping.

#### Schema Key Access

- **`ZodMap.keySchema`** (`types.ts:3597–3600`) and **`ZodRecord.keySchema`** (`types.ts:3508–3511`) — both called by `ZodDiscriminatedUnion`, `ZodMap`, `ZodObject`, and `ZodRecord`, indicating that during object parsing, `ZodObject` accesses key schemas from map and record types for structural validation.

---

### 3. Broader Type Composition Ecosystem

The v4 classic layer provides additional composition types visible in the clue:

- **`ZodArray`** (`schemas.ts:1129–1140`) — methods: `length`, `max`, `min`, `nonempty`, `unwrap`.
- **`ZodReadonly`** (`schemas.ts:2124–2129`) — methods: `unwrap`. Called by `readonly`.
- **`ZodNullable`** (`schemas.ts:1876–1881`) — methods: `unwrap`. Called by `nullable`.
- **`ZodOptional`** (`schemas.ts:1826–1831`) — methods: `unwrap`. Called by `optional`.
- **`ZodEnum`** (`schemas.ts:1618–1635`) — calls `readonly`. Called by `_enum`, `nativeEnum`.

These provide the compositional building blocks that combine with object schemas.

#### `_ZodType` — v4 Classic Base

`_ZodType` (`schemas.ts:153–154`) is the internal base interface. `ZodUnknown` extends it (line 1063), and `_ZodBigInt` extends it (`schemas.ts:936–954`), indicating all v4 classic schema types share this base.

`ZodType` (`schemas.ts:20–151`) is the public base with methods: `and`, `array`, `clone`, `decode`, `decodeAsync`, `default`, `describe`, `encode`, `encodeAsync`, `exactOptional`, `nullable`, `optional`, `or`, `pipe`, `promise`, `readonly`, `transform`, etc.

---

### 4. `objectClone` Utility

`objectClone` (`packages/zod/src/v4/core/util.ts:291–293`) — behavior: `DELEGATE(Object.create -> result)` — creates a shallow clone of an object using `Object.create`. This utility is likely used during object parsing to create output objects without mutating input.

---

### Summary of Unknown-Key Behavior Modes

| Method | Behavior |
|--------|----------|
| `strip` | Remove unrecognized keys |
| `strict` | Reject input with unrecognized keys |
| `passthrough` | Include unrecognized keys in output |
| `loose` | Lenient handling (exact semantics unclear from clue) |
| `catchall(schema)` | Validate unrecognized keys against `schema` |

### What Cannot Be Determined

- **Default unknown-key behavior**: The clue does not state which mode (`strip`, `strict`, `passthrough`, or `loose`) is the default when creating a `ZodObject`. The existence of `strip` as a method implies it may need to be explicitly called, but the default is not documented here.
- **Exact difference between `loose` and `passthrough`**: Both appear to allow extra keys, but the precise semantic distinction is not explained in the clue.
- **v3 unknown-key handling**: The v3 `ZodObject` FOCUS entry does not list `strip`/`strict`/`passthrough` methods — whether these exist in v3 or only in v4 cannot be confirmed.
- **How `deepPartialify`** (which calls v3 `ZodObject`) interacts with unknown-key modes is not described.
- **The full parsing algorithm for object schemas** — the clue shows the methods but not the `_parse` body behavior for `ZodObject` in either v3 or v4.
