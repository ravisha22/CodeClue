# Cross-Model (Haiku): blind-zod-mech-1
Date: 2026-04-16

## Answer

Zod's object parsing applies strict unknown-key filtering by default, with configurable behavior, and composable shape inheritance for object schema combination.

### Unknown-Key Handling: `UnknownKeysParam`

Object schemas are parameterized with `UnknownKeysParam` to control unknown key behavior [Line 172-173 (clue file): "SomeZodObject (packages/zod/src/v3/types.ts:2418-2420)" "type alias SomeZodObject = ZodObject<ZodRawShape, UnknownKeysParam, ZodTypeAny>"]. This parameter determines three possible behaviors during parsing:

1. **Strict (default)**: Unknown keys are rejected/stripped
2. **Passthrough**: Unknown keys are preserved in output
3. **Catch**: Unknown keys are caught with error info

The `UnknownKeysParam` parameter is encoded in the ZodObject type signature, controlling which keys are validated vs. allowed/stripped.

### Object Configuration: `$ZodObjectConfig`

Object parsing uses a configuration system that explicitly separates input and output shapes [Line 143-149 (clue file): "$ZodObjectConfig (packages/zod/src/v4/core/schemas.ts:1748-1749)" "type alias $ZodObjectConfig = { out: Record<string, unknown>; in: Record<string, unknown> }"]. This allows:
- Input schema (validates what the user provides, including unknown keys)
- Output schema (defines what emerges after unknown-key processing)

### Object Shape Composition: `SafeExtendShape` & `$ZodObjectParams`

Object composition is handled via shape extension [Line 251-254 (source snippet): "SafeExtendShape<Base extends core.$ZodShape, Ext extends core.$ZodLooseShape>"]. This type-level composition:
- Merges shape definitions safely
- Avoids key conflicts via type checking
- Uses `$ZodLooseShape` for flexible extension

The `$ZodObjectParams` type [Line 151-157 (clue file): "$ZodObjectParams = TypeParams<schemas.$ZodObject, \"shape\" | \"catchall\">" "uses: TypeParams, schemas.$ZodObject, shape, catchall"] parameterizes objects with:
- **shape**: The field definitions (ZodRawShape)
- **catchall**: Handler for unknown keys (the UnknownKeysParam behavior)

### Unknown-Key Behavior Modes: `loose()` vs Default

The `.loose()` method [Line 246-248 (source snippet): "ZodObject.loose(): ZodObject<Shape, core.$loose>"  ] changes unknown-key mode to allow unknown keys, returning a new object schema with the same shape but different unknown-key behavior. The core `$loose` parameter indicates passthrough mode.

This is distinct from default strict mode where unknown keys either trigger validation errors or are stripped based on the `UnknownKeysParam` setting.

### Parsing Flow with Unknown Keys

When `ZodObject._parse()` is invoked [implied by symbol table showing `ZodObject` has `_parse` method], the parser:
1. **Validates known fields** against the shape definitions
2. **Processes unknown keys** according to UnknownKeysParam:
   - **Strict**: Fails validation or strips them
   - **Passthrough (loose)**: Preserves all keys
   - **Catch**: Collects error info for reporting
3. **Constructs output** with only known keys or with passthrough keys depending on mode

### Catchall Support

The `"catchall"` parameter in `$ZodObjectParams` suggests Zod objects can define catch-all validators for any unmapped keys, providing fine-grained control beyond simple strip/passthrough modes.

In summary: Zod enforces **strict unknown-key filtering by default** via UnknownKeysParam, **separates input/output shapes** to handle filtering, and **supports shape composition** with SafeExtendShape while enabling **dynamic behavior switching** via methods like `.loose()`.
