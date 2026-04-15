# v2.3 Response: blind-zod-mech-1
Date: 2026-04-15

## Summary

Zod provides configurable unknown-key handling for object schemas and multiple object-composition APIs. Based on the clue file, v3 uses an `UnknownKeysParam` type to control unknown-key behavior (strip, strict, passthrough), while v4 uses a `catchall` mechanism on `$ZodObject`. Object composition is supported through intersection types and record schemas.

## Detailed Analysis

### Unknown-Key Handling

#### v3: `UnknownKeysParam` and `SomeZodObject`

- **`SomeZodObject`** (`v3/types.ts:2418-2420`) — defined as `ZodObject<ZodRawShape, UnknownKeysParam, ZodTypeAny>` (FOCUS). The `UnknownKeysParam` type parameter is the second generic argument to `ZodObject`, indicating that each object schema carries a type-level configuration for how unknown keys are handled.
- The `UnknownKeysParam` type is referenced but not directly defined in the FOCUS. Based on the type alias structure, it is a type parameter that configures the object schema's behavior when encountering keys not defined in the shape.
- `ZodRawShape` is the first type parameter, representing the shape definition (the known keys and their schemas).
- `ZodTypeAny` is the third parameter (the catchall type for unknown keys).

#### v4: `$ZodObjectConfig` and `catchall`

- **`$ZodObjectConfig`** (`v4/core/schemas.ts:1748-1749`) — `{ out: Record<string, unknown>; in: Record<string, unknown> }` (FOCUS). This defines the object schema's input/output configuration, both typed as `Record<string, unknown>`, meaning objects with string keys and unknown values.
- **`$ZodObjectParams`** (`v4/core/api.ts:1161-1162`) — `TypeParams<schemas.$ZodObject, "shape" | "catchall">` (FOCUS). The presence of `"catchall"` as a parameter key indicates that v4 object schemas have a `catchall` property that defines what happens to unknown keys. This replaces the v3 `UnknownKeysParam` with a more flexible catchall schema approach.
- **`$ZodUnknownParams`** (`v4/core/api.ts:777-779`) — `TypeParams<schemas.$ZodUnknown>` (FOCUS). The `$ZodUnknown` schema is a separate type that accepts any value, and its params are defined independently.

### Object-Composition Behaviors

#### Parse Entry Points

Object schemas are validated through the same parse pipeline as all other schemas:

- **`$Parse`** (`v4/core/parse.ts:7-9`) — the synchronous parse function type: `<T extends schemas.$ZodType>(schema: T, value: unknown, _ctx?: schemas.ParseContext<errors.$ZodIssue>, _params?: { callee?: util.AnyFunc; Err?: $ZodErrorClass })` (FOCUS). Object schemas pass through this parse function.
- **`$ParseAsync`** (`parse.ts:31-32`) — async variant (FOCUS).
- **`$SafeParse`** (`parse.ts:52-53`) and **`$SafeParseAsync`** (`parse.ts:74-75`) — safe variants returning `util.SafeParseResult<core.output<T>>` (FOCUS).

#### v3 Object Parsing

- **`ZodType._parse`** (`v3/types.ts:170`) — the base parse method overridden by each schema type (SYM). The `ZodObject` type (one of the `ZodFirstPartySchemaTypes`) would override `_parse` to iterate over shape keys, validate each value, and handle unknown keys according to `UnknownKeysParam`.
- The `ZodIntersection._parse` (`v3/types.ts:3292`) handles intersection types, which is one way to compose objects (SYM).

#### Record Schemas

- **`$ZodRecordKey`** (`v4/core/schemas.ts:2684-2691`) — defined as `$ZodType<string | number | symbol, unknown>` (FOCUS, 8 entries at lines 2684-2691). This type constrains what can be used as a record key to `string | number | symbol`. Records are an alternative to objects for dynamic key structures.
- **`$ZodMapParams`** (`v4/core/api.ts:1290-1292`) — `TypeParams<schemas.$ZodMap, "keyType" | "valueType">` (FOCUS). Maps are another composition mechanism with explicit key and value types.

#### v3 Object Composition

From the SYM section:
- **`ZodIntersection._parse`** (`v3/types.ts:3292`) — handles intersection types, which combine two schemas (SYM).
- **`ZodRecord._parse`** (`v3/types.ts:3514`) — parses record schemas (SYM).
- **`ZodMap._parse`** (`v3/types.ts:3603`) — parses map schemas (SYM).
- **`ZodTuple._parse`** (`v3/types.ts:3399`) — parses tuple schemas (SYM).

### How Unknown Keys Are Processed

Based on the structural evidence:

1. **v3 approach**: `ZodObject` is parameterized with `UnknownKeysParam` (from `SomeZodObject`, FOCUS). During `_parse`, the object schema iterates over the input's keys. For keys not in the `ZodRawShape`:
   - If `UnknownKeysParam` specifies stripping: unknown keys are removed from the output.
   - If it specifies strict mode: an error is raised for unknown keys.
   - If it specifies passthrough: unknown keys are passed through to the output.
   - The third type parameter `ZodTypeAny` (catchall) provides schema-level validation for unknown keys.

2. **v4 approach**: `$ZodObject` uses a `catchall` schema (from `$ZodObjectParams`: `"shape" | "catchall"`, FOCUS). The `catchall` schema is applied to any keys not in the `shape`. If `catchall` is:
   - A `$ZodNever`-like schema: unknown keys would cause validation failures (strict).
   - A `$ZodUnknown`-like schema: unknown keys would pass through.
   - Any other schema: unknown keys are validated against it.

### Object Composition Mechanisms

The clue file reveals several composition patterns:

1. **Intersection** (`ZodIntersection._parse`, SYM line 3292): Combines two object schemas, requiring a value to satisfy both. In v4, `$ZodIntersectionInternals` is the core type (referenced by mini types).

2. **Record** (`ZodRecord._parse`, SYM line 3514; `$ZodRecordKey`, FOCUS): Dynamic key-value schemas where all keys share the same key and value schema types.

3. **Map** (`ZodMap._parse`, SYM line 3603; `$ZodMapParams`, FOCUS): Key-value pairs with explicit `keyType` and `valueType` schemas.

4. **Tuple** (`ZodTuple._parse`, SYM line 3399): Fixed-length arrays with per-position schemas, not directly object composition but related structured data validation.

5. **Pipeline** (`ZodPipeline._parse`, SYM line 4782): Chains transformations, allowing objects to be transformed through multiple validation/transformation steps.

## Uncertainty / Limits

- **Exact unknown-key behavior**: The `UnknownKeysParam` type's possible values (e.g., `"strip"`, `"strict"`, `"passthrough"`) are **not explicitly listed** in the clue file. The analysis above is inferred from the type parameter name and the `catchall` field in v4.
- **Object `_parse` body**: The `ZodObject._parse` method is not included in the FOCUS or source snippets. The exact iteration order, error accumulation strategy, and unknown-key handling logic cannot be confirmed.
- **`catchall` semantics in v4**: While `$ZodObjectParams` includes `"catchall"`, the exact runtime behavior when a catchall schema is or isn't provided is not documented.
- **Merging behavior**: Methods like `.merge()`, `.extend()`, `.pick()`, `.omit()`, `.partial()` on `ZodObject` are common object composition operations but are not covered in this task's FOCUS or SYM sections.
- **GAPS**: "80 symbols in L3, 0 with behavior annotations" — no behavioral annotations are available for the focused symbols in this task.
