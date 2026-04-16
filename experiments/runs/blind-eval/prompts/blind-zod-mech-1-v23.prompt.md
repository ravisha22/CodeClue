# Blind Evaluation Prompt - MRLF v2.1 with File 2 Drill-Down
# Task: blind-zod-mech-1

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

--- CLUE FILE (File 1) ---
=CC v2.1 zod@HEAD 390mod 2677sym
? What exact unknown-key and object-composition behaviors does Zod apply when parsing object schemas?


-- TREE
packages/  (384 files)
  bench/  docs/  resolution/  treeshake/  tsc/  zod/
scripts/  (4 files)
play.ts  vitest.config.ts

-- INDEX
packages/zod/src/v3/types.ts                   5138L  AnyZodObject, AnyZodObject, AnyZodTuple, AnyZodTuple, ArrayCardinality
packages/bench/array.ts                          20L  
packages/bench/benchUtil.ts                      69L  formatNumber, makeData, makeSchema, randomPick, randomString
packages/bench/boolean.ts                        16L  
packages/bench/datetime-regex.ts                 52L  
packages/bench/datetime.ts                       16L  
packages/bench/discriminated-union.ts           159L  makeSchema
packages/bench/error-handling.ts                 33L  
packages/bench/index.ts                          20L  run
packages/bench/init.ts                           89L  
packages/bench/instanceof.ts                     69L  constructor, ZodFailure, instanceofClass
packages/bench/ipv4-regex.ts                     46L  
packages/bench/jit-union.ts                      79L  
packages/bench/key-iteration.ts                  50L  
packages/bench/lazy-box.ts                       59L  lazyWithGetterOverride, lazyWithInternalProp, lazyWithScopeProp
packages/bench/libs.ts                           57L  
packages/bench/metabench.ts                     227L  BenchWithDataParams, run, BenchmarkJS, run, Metabench
packages/bench/number.ts                         16L  
packages/bench/object-async.ts                   13L  
packages/bench/object-creation.ts                18L  constructor, ZodFail
packages/bench/object-fail.ts                    13L  
packages/bench/object-moltar-jitless.ts          89L  
packages/bench/object-moltar.ts                  81L  
packages/bench/object-safe.ts                    13L  
packages/bench/object-safeasync.ts               13L  
  ...and 365 more modules

-- SYM
ZodString._addCheck                 M packages/zod/src/v3/types.ts:1050   method ZodString._addCheck
ZodNumber._addCheck                 M packages/zod/src/v3/types.ts:1497   method ZodNumber._addCheck
ZodBigInt._addCheck                 M packages/zod/src/v3/types.ts:1749   method ZodBigInt._addCheck
ZodDate._addCheck                   M packages/zod/src/v3/types.ts:1943   method ZodDate._addCheck
ZodType._parse                      M packages/zod/src/v3/types.ts:170    method ZodType._parse
ZodString                           C packages/zod/src/v3/types.ts:731    class ZodString
Class.constructor                   M packages/zod/src/v3/types.ts:5036   method Class.constructor
ZodType.constructor                 M packages/zod/src/v3/types.ts:411    method ZodType.constructor
ZodType._getOrReturnCtx             M packages/zod/src/v3/types.ts:176    method ZodType._getOrReturnCtx
$ZodAsyncError.constructor          M packages/zod/src/v4/core/core.ts:99     method $ZodAsyncError.constructor
$ZodEncodeError.constructor         M packages/zod/src/v4/core/core.ts:105    method $ZodEncodeError.constructor
ZodNumber                           C packages/zod/src/v3/types.ts:1369   class ZodNumber
ZodBigInt                           C packages/zod/src/v3/types.ts:1635   class ZodBigInt
ZodString._parse                    M packages/zod/src/v3/types.ts:732    method ZodString._parse
ZodBigInt.setLimit                  M packages/zod/src/v3/types.ts:1734   method ZodBigInt.setLimit
ZodNumber.setLimit                  M packages/zod/src/v3/types.ts:1482   method ZodNumber.setLimit
ZodNumber._parse                    M packages/zod/src/v3/types.ts:1370   method ZodNumber._parse
ZodEffects._parse                   M packages/zod/src/v3/types.ts:4322   method ZodEffects._parse
ZodBigInt._parse                    M packages/zod/src/v3/types.ts:1636   method ZodBigInt._parse
ZodIntersection._parse              M packages/zod/src/v3/types.ts:3292   method ZodIntersection._parse
ZodArray._parse                     M packages/zod/src/v3/types.ts:2241   method ZodArray._parse
ZodDate._parse                      M packages/zod/src/v3/types.ts:1878   method ZodDate._parse
ZodFunction._parse                  M packages/zod/src/v3/types.ts:3822   method ZodFunction._parse
ZodPipeline._parse                  M packages/zod/src/v3/types.ts:4782   method ZodPipeline._parse
ZodUnion._parse                     M packages/zod/src/v3/types.ts:2947   method ZodUnion._parse
ZodEnum._parse                      M packages/zod/src/v3/types.ts:4082   method ZodEnum._parse
ZodPromise._parse                   M packages/zod/src/v3/types.ts:4244   method ZodPromise._parse
ZodSymbol._parse                    M packages/zod/src/v3/types.ts:2010   method ZodSymbol._parse
ZodVoid._parse                      M packages/zod/src/v3/types.ts:2193   method ZodVoid._parse
ZodBoolean._parse                   M packages/zod/src/v3/types.ts:1834   method ZodBoolean._parse
ZodNaN._parse                       M packages/zod/src/v3/types.ts:4702   method ZodNaN._parse
ZodNull._parse                      M packages/zod/src/v3/types.ts:2080   method ZodNull._parse
ZodUndefined._parse                 M packages/zod/src/v3/types.ts:2045   method ZodUndefined._parse
ZodNever._parse                     M packages/zod/src/v3/types.ts:2164   method ZodNever._parse
ZodSet._parse                       M packages/zod/src/v3/types.ts:3691   method ZodSet._parse
ZodLiteral._parse                   M packages/zod/src/v3/types.ts:4007   method ZodLiteral._parse
ZodMap._parse                       M packages/zod/src/v3/types.ts:3603   method ZodMap._parse
ZodNativeEnum._parse                M packages/zod/src/v3/types.ts:4179   method ZodNativeEnum._parse
ZodRecord._parse                    M packages/zod/src/v3/types.ts:3514   method ZodRecord._parse
ZodTuple._parse                     M packages/zod/src/v3/types.ts:3399   method ZodTuple._parse
ZodDefault._parse                   M packages/zod/src/v3/types.ts:4569   method ZodDefault._parse
ZodNullable._parse                  M packages/zod/src/v3/types.ts:4530   method ZodNullable._parse
ZodBranded._parse                   M packages/zod/src/v3/types.ts:4748   method ZodBranded._parse
ZodCatch._parse                     M packages/zod/src/v3/types.ts:4619   method ZodCatch._parse
ZodLazy._parse                      M packages/zod/src/v3/types.ts:3979   method ZodLazy._parse
ZodOptional._parse                  M packages/zod/src/v3/types.ts:4490   method ZodOptional._parse
ZodReadonly._parse                  M packages/zod/src/v3/types.ts:4877   method ZodReadonly._parse
ZodAny._parse                       M packages/zod/src/v3/types.ts:2115   method ZodAny._parse
ZodUnknown._parse                   M packages/zod/src/v3/types.ts:2140   method ZodUnknown._parse
ZodOptional.unwrap                  M packages/zod/src/v3/types.ts:4498   method ZodOptional.unwrap
ZodPromise.unwrap                   M packages/zod/src/v3/types.ts:4240   method ZodPromise.unwrap
ZodBranded.unwrap                   M packages/zod/src/v3/types.ts:4758   method ZodBranded.unwrap
ZodReadonly.unwrap                  M packages/zod/src/v3/types.ts:4896   method ZodReadonly.unwrap
ZodNullable.unwrap                  M packages/zod/src/v3/types.ts:4538   method ZodNullable.unwrap
ZodNumber.maxValue                  M packages/zod/src/v3/types.ts:1587   method ZodNumber.maxValue
ZodNumber.minValue                  M packages/zod/src/v3/types.ts:1577   method ZodNumber.minValue
ZodBigInt.maxValue                  M packages/zod/src/v3/types.ts:1810   method ZodBigInt.maxValue
  ...and 2442 more symbols

-- FOCUS
$ZodRecordKey (packages/zod/src/v4/core/schemas.ts:2688-2688)
  type alias $ZodRecordKey = $ZodType<string | number | symbol, unknown>
  uses: $ZodType, string, number, symbol

$ZodRecordKey (packages/zod/src/v4/core/schemas.ts:2690-2690)
  type alias $ZodRecordKey = $ZodType<string | number | symbol, unknown>
  uses: $ZodType, string, number, symbol

$ZodRecordKey (packages/zod/src/v4/core/schemas.ts:2687-2687)
  type alias $ZodRecordKey = $ZodType<string | number | symbol, unknown>
  uses: $ZodType, string, number, symbol

$ZodRecordKey (packages/zod/src/v4/core/schemas.ts:2684-2684)
  type alias $ZodRecordKey = $ZodType<string | number | symbol, unknown>
  uses: $ZodType, string, number, symbol

$ZodRecordKey (packages/zod/src/v4/core/schemas.ts:2689-2689)
  type alias $ZodRecordKey = $ZodType<string | number | symbol, unknown>
  uses: $ZodType, string, number, symbol

$ZodRecordKey (packages/zod/src/v4/core/schemas.ts:2685-2685)
  type alias $ZodRecordKey = $ZodType<string | number | symbol, unknown>
  uses: $ZodType, string, number, symbol

$ZodRecordKey (packages/zod/src/v4/core/schemas.ts:2691-2691)
  type alias $ZodRecordKey = $ZodType<string | number | symbol, unknown>
  uses: $ZodType, string, number, symbol

$ZodRecordKey (packages/zod/src/v4/core/schemas.ts:2686-2686)
  type alias $ZodRecordKey = $ZodType<string | number | symbol, unknown>
  uses: $ZodType, string, number, symbol

$ZodObjectConfig (packages/zod/src/v4/core/schemas.ts:1748-1748)
  type alias $ZodObjectConfig = { out: Record<string, unknown>; in: Record<string, unknown> }
  uses: out, Record, string, unknown

$ZodObjectConfig (packages/zod/src/v4/core/schemas.ts:1749-1749)
  type alias $ZodObjectConfig = { out: Record<string, unknown>; in: Record<string, unknown> }
  uses: out, Record, string, unknown

$ZodObjectParams (packages/zod/src/v4/core/api.ts:1162-1162)
  type alias $ZodObjectParams = TypeParams<schemas.$ZodObject, "shape" | "catchall">
  uses: TypeParams, schemas.$ZodObject, shape, catchall

$ZodObjectParams (packages/zod/src/v4/core/api.ts:1161-1161)
  type alias $ZodObjectParams = TypeParams<schemas.$ZodObject, "shape" | "catchall">
  uses: TypeParams, schemas.$ZodObject, shape, catchall

$ZodUnknownParams (packages/zod/src/v4/core/api.ts:777-777)
  type alias $ZodUnknownParams = TypeParams<schemas.$ZodUnknown>
  uses: TypeParams, schemas.$ZodUnknown

$ZodUnknownParams (packages/zod/src/v4/core/api.ts:779-779)
  type alias $ZodUnknownParams = TypeParams<schemas.$ZodUnknown>
  uses: TypeParams, schemas.$ZodUnknown

$ZodUnknownParams (packages/zod/src/v4/core/api.ts:778-778)
  type alias $ZodUnknownParams = TypeParams<schemas.$ZodUnknown>
  uses: TypeParams, schemas.$ZodUnknown

SomeZodObject (packages/zod/src/v3/types.ts:2418-2418)
  type alias SomeZodObject = ZodObject<ZodRawShape, UnknownKeysParam, ZodTypeAny>
  uses: ZodObject, ZodRawShape, UnknownKeysParam, ZodTypeAny

SomeZodObject (packages/zod/src/v3/types.ts:2418-2420)
  type alias SomeZodObject = ZodObject<ZodRawShape, UnknownKeysParam, ZodTypeAny>
  uses: ZodObject, ZodRawShape, UnknownKeysParam, ZodTypeAny

$ZodMapParams (packages/zod/src/v4/core/api.ts:1291-1291)
  type alias $ZodMapParams = TypeParams<schemas.$ZodMap, "keyType" | "valueType">
  uses: TypeParams, schemas.$ZodMap, keyType, valueType

$ZodMapParams (packages/zod/src/v4/core/api.ts:1290-1290)
  type alias $ZodMapParams = TypeParams<schemas.$ZodMap, "keyType" | "valueType">
  uses: TypeParams, schemas.$ZodMap, keyType, valueType

$ZodMapParams (packages/zod/src/v4/core/api.ts:1292-1292)
  type alias $ZodMapParams = TypeParams<schemas.$ZodMap, "keyType" | "valueType">
  uses: TypeParams, schemas.$ZodMap, keyType, valueType

$ZodRecordParams (packages/zod/src/v4/core/api.ts:1273-1273)
  type alias $ZodRecordParams = TypeParams<schemas.$ZodRecord, "keyType" | "valueType">
  uses: TypeParams, schemas.$ZodRecord, keyType, valueType

$ZodRecordParams (packages/zod/src/v4/core/api.ts:1275-1275)
  type alias $ZodRecordParams = TypeParams<schemas.$ZodRecord, "keyType" | "valueType">
  uses: TypeParams, schemas.$ZodRecord, keyType, valueType

$ZodRecordParams (packages/zod/src/v4/core/api.ts:1274-1274)
  type alias $ZodRecordParams = TypeParams<schemas.$ZodRecord, "keyType" | "valueType">
  uses: TypeParams, schemas.$ZodRecord, keyType, valueType

ZodDiscriminatedUnionOption (packages/zod/src/v3/types.ts:3100-3100)
  type alias ZodDiscriminatedUnionOption = ZodObject< { [key in Discriminator]: ZodTypeAny } & ZodRawShape,
  uses: ZodObject, key, in, Discriminator

ZodDiscriminatedUnionOption (packages/zod/src/v3/types.ts:3100-3101)
  type alias ZodDiscriminatedUnionOption = ZodObject< { [key in Discriminator]: ZodTypeAny } & ZodRawShape,
  uses: ZodObject, key, in, Discriminator

$Parse (packages/zod/src/v4/core/parse.ts:8-8)
  type alias $Parse = <T extends schemas.$ZodType>( schema: T, value: unknown, _ctx?: schemas.ParseContext<errors.$ZodIssue>, _params?: { callee?: util.AnyFunc; Err?: $ZodErrorClass }
  uses: T, schemas.$ZodType, schema, value

$Parse (packages/zod/src/v4/core/parse.ts:7-7)
  type alias $Parse = <T extends schemas.$ZodType>( schema: T, value: unknown, _ctx?: schemas.ParseContext<errors.$ZodIssue>, _params?: { callee?: util.AnyFunc; Err?: $ZodErrorClass }
  uses: T, schemas.$ZodType, schema, value

$Parse (packages/zod/src/v4/core/parse.ts:9-9)
  type alias $Parse = <T extends schemas.$ZodType>( schema: T, value: unknown, _ctx?: schemas.ParseContext<errors.$ZodIssue>, _params?: { callee?: util.AnyFunc; Err?: $ZodErrorClass }
  uses: T, schemas.$ZodType, schema, value

$ParseAsync (packages/zod/src/v4/core/parse.ts:31-31)
  type alias $ParseAsync = <T extends schemas.$ZodType>( schema: T, value: unknown, _ctx?: schemas.ParseContext<errors.$ZodIssue>, _params?: { callee?: util.AnyFunc; Err?: $ZodErrorClass }
  uses: T, schemas.$ZodType, schema, value

$ParseAsync (packages/zod/src/v4/core/parse.ts:32-32)
  type alias $ParseAsync = <T extends schemas.$ZodType>( schema: T, value: unknown, _ctx?: schemas.ParseContext<errors.$ZodIssue>, _params?: { callee?: util.AnyFunc; Err?: $ZodErrorClass }
  uses: T, schemas.$ZodType, schema, value

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 0 with behavior annotations
uncovered: $InferZodRecordInput, $InferZodRecordInput, $InferZodRecordInput, $InferZodRecordInput
drill: packages/zod/src/v4/classic/schemas.ts (~1 lines, ZodObject.loose)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## ZodObject.loose  (packages/zod/src/v4/classic/schemas.ts L1193-1193)
```
  loose(): ZodObject<Shape, core.$loose>;
```

## SafeExtendShape  (packages/zod/src/v4/mini/schemas.ts L882-882)
```
export type SafeExtendShape<Base extends core.$ZodShape, Ext extends core.$ZodLooseShape> = {
```

## ZodAny  (packages/zod/src/v4/classic/schemas.ts L1049-1051)
```

// ZodAny
export interface ZodAny extends _ZodType<core.$ZodAnyInternals> {}
```

## ZodArray.length  (packages/zod/src/v4/classic/schemas.ts L1136-1136)
```
  length(len: number, params?: string | core.$ZodCheckLengthEqualsParams): this;
```

## ZodArray.max  (packages/zod/src/v4/classic/schemas.ts L1135-1135)
```
  max(maxLength: number, params?: string | core.$ZodCheckMaxLengthParams): this;
```

## ZodArray.min  (packages/zod/src/v4/classic/schemas.ts L1133-1133)
```
  min(minLength: number, params?: string | core.$ZodCheckMinLengthParams): this;
```

## ZodArray.nonempty  (packages/zod/src/v4/classic/schemas.ts L1134-1134)
```
  nonempty(params?: string | core.$ZodCheckMinLengthParams): this;
```

## ZodArray.unwrap  (packages/zod/src/v4/classic/schemas.ts L1138-1138)
```
  unwrap(): T;
```

## ZodArray  (packages/zod/src/v4/classic/schemas.ts L1127-1140)
```

// ZodArray
export interface ZodArray<T extends core.SomeType = core.$ZodType>
  extends _ZodType<core.$ZodArrayInternals<T>>,
    core.$ZodArray<T> {
  element: T;
  min(minLength: number, params?: string | core.$ZodCheckMinLengthParams): this;
  nonempty(params?: string | core.$ZodCheckMinLengthParams): this;
  max(maxLength: number, params?: string | core.$ZodCheckMaxLengthParams): this;
  length(len: number, params?: string | core.$ZodCheckLengthEqualsParams): this;

  unwrap(): T;
  "~standard": ZodStandardSchemaWithJSON<this>;
}
```

## ZodBase64  (packages/zod/src/v4/classic/schemas.ts L702-706)
```

// ZodBase64
export interface ZodBase64 extends ZodStringFormat<"base64"> {
  _zod: core.$ZodBase64Internals;
}
```

## ZodBase64URL  (packages/zod/src/v4/classic/schemas.ts L715-719)
```

// ZodBase64URL
export interface ZodBase64URL extends ZodStringFormat<"base64url"> {
  _zod: core.$ZodBase64URLInternals;
}
```

## ZodBigInt  (packages/zod/src/v4/classic/schemas.ts L955-956)
```

export interface ZodBigInt extends _ZodBigInt<core.$ZodBigIntInternals<bigint>> {}
```

## ZodBigIntFormat  (packages/zod/src/v4/classic/schemas.ts L985-990)
```
// bigint formats

// ZodBigIntFormat
export interface ZodBigIntFormat extends ZodBigInt {
  _zod: core.$ZodBigIntFormatInternals;
}
```

## ZodBoolean  (packages/zod/src/v4/classic/schemas.ts L924-924)
```
export interface ZodBoolean extends _ZodBoolean<core.$ZodBooleanInternals<boolean>> {}
```

## ZodCIDRv4  (packages/zod/src/v4/classic/schemas.ts L676-680)
```

// ZodCIDRv4
export interface ZodCIDRv4 extends ZodStringFormat<"cidrv4"> {
  _zod: core.$ZodCIDRv4Internals;
}
```

## ZodCIDRv6  (packages/zod/src/v4/classic/schemas.ts L689-693)
```

// ZodCIDRv6
export interface ZodCIDRv6 extends ZodStringFormat<"cidrv6"> {
  _zod: core.$ZodCIDRv6Internals;
}
```

## ZodCUID2  (packages/zod/src/v4/classic/schemas.ts L566-570)
```

// ZodCUID2
export interface ZodCUID2 extends ZodStringFormat<"cuid2"> {
  _zod: core.$ZodCUID2Internals;
}
```

## ZodCUID  (packages/zod/src/v4/classic/schemas.ts L552-556)
```

// ZodCUID
export interface ZodCUID extends ZodStringFormat<"cuid"> {
  _zod: core.$ZodCUIDInternals;
}
```

## ZodCatch.removeCatch  (packages/zod/src/v4/classic/schemas.ts L2024-2024)
```
  removeCatch(): T;
```

## ZodCatch.unwrap  (packages/zod/src/v4/classic/schemas.ts L2022-2022)
```
  unwrap(): T;
```

## ZodCatch  (packages/zod/src/v4/classic/schemas.ts L2016-2025)
```

// ZodCatch
export interface ZodCatch<T extends core.SomeType = core.$ZodType>
  extends _ZodType<core.$ZodCatchInternals<T>>,
    core.$ZodCatch<T> {
  "~standard": ZodStandardSchemaWithJSON<this>;
  unwrap(): T;
  /** @deprecated Use `.unwrap()` instead. */
  removeCatch(): T;
}
```

## ZodCodec  (packages/zod/src/v4/classic/schemas.ts L2092-2100)
```

// ZodCodec
export interface ZodCodec<A extends core.SomeType = core.$ZodType, B extends core.SomeType = core.$ZodType>
  extends ZodPipe<A, B>,
    core.$ZodCodec<A, B> {
  "~standard": ZodStandardSchemaWithJSON<this>;
  _zod: core.$ZodCodecInternals<A, B>;
  def: core.$ZodCodecDef<A, B>;
}
```

## ZodCustom  (packages/zod/src/v4/classic/schemas.ts L2284-2290)
```

// ZodCustom
export interface ZodCustom<O = unknown, I = unknown>
  extends _ZodType<core.$ZodCustomInternals<O, I>>,
    core.$ZodCustom<O, I> {
  "~standard": ZodStandardSchemaWithJSON<this>;
}
```

## ZodCustomStringFormat  (packages/zod/src/v4/classic/schemas.ts L759-766)
```

// ZodCustomStringFormat
export interface ZodCustomStringFormat<Format extends string = string>
  extends ZodStringFormat<Format>,
    core.$ZodCustomStringFormat<Format> {
  _zod: core.$ZodCustomStringFormatInternals<Format>;
  "~standard": ZodStandardSchemaWithJSON<this>;
}
```

## ZodDate  (packages/zod/src/v4/classic/schemas.ts L1109-1110)
```

export interface ZodDate extends _ZodDate<core.$ZodDateInternals<Date>> {}
```

## ZodDefault.removeDefault  (packages/zod/src/v4/classic/schemas.ts L1912-1912)
```
  removeDefault(): T;
```

## ZodDefault.unwrap  (packages/zod/src/v4/classic/schemas.ts L1910-1910)
```
  unwrap(): T;
```

## ZodDefault  (packages/zod/src/v4/classic/schemas.ts L1904-1913)
```

// ZodDefault
export interface ZodDefault<T extends core.SomeType = core.$ZodType>
  extends _ZodType<core.$ZodDefaultInternals<T>>,
    core.$ZodDefault<T> {
  "~standard": ZodStandardSchemaWithJSON<this>;
  unwrap(): T;
  /** @deprecated Use `.unwrap()` instead. */
  removeDefault(): T;
}
```

## ZodDiscriminatedUnion  (packages/zod/src/v4/classic/schemas.ts L1379-1389)
```

// ZodDiscriminatedUnion
export interface ZodDiscriminatedUnion<
  Options extends readonly core.SomeType[] = readonly core.$ZodType[],
  Disc extends string = string,
> extends ZodUnion<Options>,
    core.$ZodDiscriminatedUnion<Options, Disc> {
  "~standard": ZodStandardSchemaWithJSON<this>;
  _zod: core.$ZodDiscriminatedUnionInternals<Options, Disc>;
  def: core.$ZodDiscriminatedUnionDef<Options, Disc>;
}
```

## ZodE164  (packages/zod/src/v4/classic/schemas.ts L731-735)
```

// ZodE164
export interface ZodE164 extends ZodStringFormat<"e164"> {
  _zod: core.$ZodE164Internals;
}
```

## ZodEmail  (packages/zod/src/v4/classic/schemas.ts L444-448)
```

// ZodEmail
export interface ZodEmail extends ZodStringFormat<"email"> {
  _zod: core.$ZodEmailInternals;
}
```

## ZodEmoji  (packages/zod/src/v4/classic/schemas.ts L524-528)
```

// ZodEmoji
export interface ZodEmoji extends ZodStringFormat<"emoji"> {
  _zod: core.$ZodEmojiInternals;
}
```

## ZodEnum  (packages/zod/src/v4/classic/schemas.ts L1616-1635)
```

// ZodEnum
export interface ZodEnum<
  /** @ts-ignore Cast variance */
  out T extends util.EnumLike = util.EnumLike,
> extends _ZodType<core.$ZodEnumInternals<T>>,
    core.$ZodEnum<T> {
  "~standard": ZodStandardSchemaWithJSON<this>;
  enum: T;
  options: Array<T[keyof T]>;

  extract<const U extends readonly (keyof T)[]>(
    values: U,
    params?: string | core.$ZodEnumParams
  ): ZodEnum<util.Flatten<Pick<T, U[number]>>>;
  exclude<const U extends readonly (keyof T)[]>(
    values: U,
    params?: string | core.$ZodEnumParams
  ): ZodEnum<util.Flatten<Omit<T, U[number]>>>;
}
```

## ZodExactOptional.unwrap  (packages/zod/src/v4/classic/schemas.ts L1855-1855)
```
  unwrap(): T;
```

## ZodExactOptional  (packages/zod/src/v4/classic/schemas.ts L1849-1856)
```

// ZodExactOptional
export interface ZodExactOptional<T extends core.SomeType = core.$ZodType>
  extends _ZodType<core.$ZodExactOptionalInternals<T>>,
    core.$ZodExactOptional<T> {
  "~standard": ZodStandardSchemaWithJSON<this>;
  unwrap(): T;
}
```

## ZodFile.max  (packages/zod/src/v4/classic/schemas.ts L1752-1752)
```
  max(size: number, params?: string | core.$ZodCheckMaxSizeParams): this;
```

## ZodFile.mime  (packages/zod/src/v4/classic/schemas.ts L1753-1753)
```
  mime(types: util.MimeTypes | Array<util.MimeTypes>, params?: string | core.$ZodCheckMimeTypeParams): this;
```

## ZodFile.min  (packages/zod/src/v4/classic/schemas.ts L1751-1751)
```
  min(size: number, params?: string | core.$ZodCheckMinSizeParams): this;
```

## ZodFile  (packages/zod/src/v4/classic/schemas.ts L1747-1754)
```

// ZodFile
export interface ZodFile extends _ZodType<core.$ZodFileInternals>, core.$ZodFile {
  "~standard": ZodStandardSchemaWithJSON<this>;
  min(size: number, params?: string | core.$ZodCheckMinSizeParams): this;
  max(size: number, params?: string | core.$ZodCheckMaxSizeParams): this;
  mime(types: util.MimeTypes | Array<util.MimeTypes>, params?: string | core.$ZodCheckMimeTypeParams): this;
}
```

## ZodFloat32  (packages/zod/src/v4/classic/schemas.ts L897-899)
```

// float32
export interface ZodFloat32 extends ZodNumberFormat {}
```

## ZodFloat64  (packages/zod/src/v4/classic/schemas.ts L903-905)
```

// float64
export interface ZodFloat64 extends ZodNumberFormat {}
```

## ZodFunction.input  (packages/zod/src/v4/classic/schemas.ts L2234-2234)
```
  input(...args: any[]): ZodFunction<any, Returns>;
```

## ZodFunction.output  (packages/zod/src/v4/classic/schemas.ts L2236-2236)
```
  output<NewReturns extends core.$ZodType>(output: NewReturns): ZodFunction<Args, NewReturns>;
```

## ZodFunction  (packages/zod/src/v4/classic/schemas.ts L2217-2237)
```

// ZodFunction
export interface ZodFunction<
... (truncated)
```
--- END SOURCE SNIPPETS ---

QUESTION: What exact unknown-key and object-composition behaviors does Zod apply when parsing object schemas?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
