# Blind Evaluation Prompt - MRLF v2.1 with File 2 Drill-Down
# Task: blind-zod-mech-2

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

--- CLUE FILE (File 1) ---
=CC v2.1 zod@HEAD 390mod 2677sym
? How does Zod decide which error message to emit when multiple customization layers are available?


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
ZodIntersection._parse              M packages/zod/src/v3/types.ts:3292   method ZodIntersection._parse
ZodBigInt._parse                    M packages/zod/src/v3/types.ts:1636   method ZodBigInt._parse
ZodDate._parse                      M packages/zod/src/v3/types.ts:1878   method ZodDate._parse
ZodFunction._parse                  M packages/zod/src/v3/types.ts:3822   method ZodFunction._parse
ZodPipeline._parse                  M packages/zod/src/v3/types.ts:4782   method ZodPipeline._parse
ZodArray._parse                     M packages/zod/src/v3/types.ts:2241   method ZodArray._parse
ZodUnion._parse                     M packages/zod/src/v3/types.ts:2947   method ZodUnion._parse
ZodEnum._parse                      M packages/zod/src/v3/types.ts:4082   method ZodEnum._parse
ZodPromise._parse                   M packages/zod/src/v3/types.ts:4244   method ZodPromise._parse
ZodVoid._parse                      M packages/zod/src/v3/types.ts:2193   method ZodVoid._parse
ZodNull._parse                      M packages/zod/src/v3/types.ts:2080   method ZodNull._parse
ZodBoolean._parse                   M packages/zod/src/v3/types.ts:1834   method ZodBoolean._parse
ZodNaN._parse                       M packages/zod/src/v3/types.ts:4702   method ZodNaN._parse
ZodSymbol._parse                    M packages/zod/src/v3/types.ts:2010   method ZodSymbol._parse
ZodUndefined._parse                 M packages/zod/src/v3/types.ts:2045   method ZodUndefined._parse
ZodNativeEnum._parse                M packages/zod/src/v3/types.ts:4179   method ZodNativeEnum._parse
ZodNever._parse                     M packages/zod/src/v3/types.ts:2164   method ZodNever._parse
ZodSet._parse                       M packages/zod/src/v3/types.ts:3691   method ZodSet._parse
ZodTuple._parse                     M packages/zod/src/v3/types.ts:3399   method ZodTuple._parse
ZodLiteral._parse                   M packages/zod/src/v3/types.ts:4007   method ZodLiteral._parse
ZodRecord._parse                    M packages/zod/src/v3/types.ts:3514   method ZodRecord._parse
ZodMap._parse                       M packages/zod/src/v3/types.ts:3603   method ZodMap._parse
ZodBranded._parse                   M packages/zod/src/v3/types.ts:4748   method ZodBranded._parse
ZodDefault._parse                   M packages/zod/src/v3/types.ts:4569   method ZodDefault._parse
ZodLazy._parse                      M packages/zod/src/v3/types.ts:3979   method ZodLazy._parse
ZodNullable._parse                  M packages/zod/src/v3/types.ts:4530   method ZodNullable._parse
ZodOptional._parse                  M packages/zod/src/v3/types.ts:4490   method ZodOptional._parse
ZodCatch._parse                     M packages/zod/src/v3/types.ts:4619   method ZodCatch._parse
ZodAny._parse                       M packages/zod/src/v3/types.ts:2115   method ZodAny._parse
ZodUnknown._parse                   M packages/zod/src/v3/types.ts:2140   method ZodUnknown._parse
ZodReadonly._parse                  M packages/zod/src/v3/types.ts:4877   method ZodReadonly._parse
ZodBranded.unwrap                   M packages/zod/src/v3/types.ts:4758   method ZodBranded.unwrap
ZodPromise.unwrap                   M packages/zod/src/v3/types.ts:4240   method ZodPromise.unwrap
ZodNullable.unwrap                  M packages/zod/src/v3/types.ts:4538   method ZodNullable.unwrap
ZodOptional.unwrap                  M packages/zod/src/v3/types.ts:4498   method ZodOptional.unwrap
ZodReadonly.unwrap                  M packages/zod/src/v3/types.ts:4896   method ZodReadonly.unwrap
ZodBigInt.minValue                  M packages/zod/src/v3/types.ts:1800   method ZodBigInt.minValue
ZodNumber.maxValue                  M packages/zod/src/v3/types.ts:1587   method ZodNumber.maxValue
ZodNumber.minValue                  M packages/zod/src/v3/types.ts:1577   method ZodNumber.minValue
  ...and 2442 more symbols

-- FOCUS
ZodError.message (packages/zod/src/v3/ZodError.ts:280-282)
  method ZodError.message
  behavior: DELEGATE(JSON.stringify -> result)
  called_by: ZodError
  uses: JSON.stringify, this.issues, util.jsonStringifyReplacer

ZodErrorMap (packages/zod/src/v3/ZodError.ts:329-329)
  type alias ZodErrorMap = (issue: ZodIssueOptionalMessage, _ctx: ErrorMapCtx) => { message: string }
  uses: issue, ZodIssueOptionalMessage, _ctx, ErrorMapCtx

ZodErrorMap (packages/zod/src/v3/ZodError.ts:330-330)
  type alias ZodErrorMap = (issue: ZodIssueOptionalMessage, _ctx: ErrorMapCtx) => { message: string }
  uses: issue, ZodIssueOptionalMessage, _ctx, ErrorMapCtx

ZodNotMultipleOfIssue (packages/zod/src/v3/ZodError.ts:135-139)
  interface ZodNotMultipleOfIssue
  extends: ZodIssueBase
  uses: ZodIssueCode.not_multiple_of

ZodIssueOptionalMessage (packages/zod/src/v3/ZodError.ts:151-151)
  type alias ZodIssueOptionalMessage = | ZodInvalidTypeIssue | ZodInvalidLiteralIssue | ZodUnrecognizedKeysIssue | ZodInvalidUnionIssue | ZodInvalidUnionDiscriminatorIssue | ZodInvalidEnumValueIssue
  uses: ZodInvalidTypeIssue, ZodInvalidLiteralIssue, ZodUnrecognizedKeysIssue, ZodInvalidUnionIssue

ZodIssueOptionalMessage (packages/zod/src/v3/ZodError.ts:152-152)
  type alias ZodIssueOptionalMessage = | ZodInvalidTypeIssue | ZodInvalidLiteralIssue | ZodUnrecognizedKeysIssue | ZodInvalidUnionIssue | ZodInvalidUnionDiscriminatorIssue | ZodInvalidEnumValueIssue | ZodInvalidArgumentsIssue
  uses: ZodInvalidTypeIssue, ZodInvalidLiteralIssue, ZodUnrecognizedKeysIssue, ZodInvalidUnionIssue

ZodError (packages/zod/src/v3/ZodError.ts:193-316)
  extends: Error
  methods: assert, constructor, errors, flatten, formErrors, format
  calls: assert, constructor, errors, flatten, formErrors, format, isEmpty, message
  uses: this.issues, new.target.prototype, Object.setPrototypeOf, this.name

ZodError (packages/zod/src/v4/classic/errors.ts:9-23)
  interface ZodError
  extends: $ZodError
  methods: addIssue, addIssues, flatten, format
  calls: addIssue, addIssues, flatten, format
  uses: z.treeifyError, core.$ZodFormattedError, core.$ZodIssue, core.$ZodFlattenedError

ZodBigInt.multipleOf (packages/zod/src/v3/types.ts:1792-1800)
  method ZodBigInt.multipleOf
  sig: ZodBigInt.multipleOf(value: bigint, message?: errorUtil.ErrMessage)
  behavior: DELEGATE(this._addCheck -> result)
  calls: _addCheck, multipleOf
  called_by: ZodBigInt, multipleOf, ZodNumber
  uses: errorUtil.ErrMessage, this._addCheck, errorUtil.toString

ZodNumber.multipleOf (packages/zod/src/v3/types.ts:1547-1554)
  method ZodNumber.multipleOf
  sig: ZodNumber.multipleOf(value: number, message?: errorUtil.ErrMessage)
  behavior: DELEGATE(this._addCheck -> result)
  calls: multipleOf, _addCheck
  called_by: multipleOf, ZodBigInt, ZodNumber
  uses: errorUtil.ErrMessage, this._addCheck, errorUtil.toString

ZodError.format (packages/zod/src/v3/ZodError.ts:217-264)
  method ZodError.format
  sig: ZodError.format(_mapper?: any)
  behavior: PRECEDENCE(issue -> default); ACCUMULATE(format loop -> result); TRANSFORM(map)
  calls: format
  called_by: ZodError
  uses: issue.message, error.issues, issue.code, issue.unionErrors.map

$ZodCheckMultipleOfInternals (packages/zod/src/v4/core/checks.ts:157-162)
  interface $ZodCheckMultipleOfInternals
  extends: $ZodCheckInternals
  uses: errors.$ZodIssueNotMultipleOf

$ZodError (packages/zod/src/v4/core/errors.ts:214-217)
  interface $ZodError
  extends: Error
  uses: Symbol.for, zod.error

$ZodCheckMultipleOfParams (packages/zod/src/v4/core/api.ts:922-922)
  type alias $ZodCheckMultipleOfParams = CheckParams<checks.$ZodCheckMultipleOf, "value" | "when">
  uses: CheckParams, checks.$ZodCheckMultipleOf, value, when

$ZodCheckMultipleOfParams (packages/zod/src/v4/core/api.ts:923-923)
  type alias $ZodCheckMultipleOfParams = CheckParams<checks.$ZodCheckMultipleOf, "value" | "when">
  uses: CheckParams, checks.$ZodCheckMultipleOf, value, when

$ZodErrorClass (packages/zod/src/v4/core/parse.ts:5-5)
  type alias $ZodErrorClass = { new (issues: errors.$ZodIssue[]): errors.$ZodError }
  uses: new, issues, errors.$ZodIssue, errors.$ZodError

$ZodErrorClass (packages/zod/src/v4/core/parse.ts:6-6)
  type alias $ZodErrorClass = { new (issues: errors.$ZodIssue[]): errors.$ZodError }
  uses: new, issues, errors.$ZodIssue, errors.$ZodError

ZodIssue (packages/zod/src/v3/ZodError.ts:169-169)
  type alias ZodIssue = ZodIssueOptionalMessage & {
  uses: ZodIssueOptionalMessage

ZodIssue (packages/zod/src/v3/ZodError.ts:170-170)
  type alias ZodIssue = ZodIssueOptionalMessage & {
  uses: ZodIssueOptionalMessage

ZodSafeParseError (packages/zod/src/v4/classic/parse.ts:6-6)
  type alias ZodSafeParseError = { success: false; data?: never; error: ZodError<T> }
  uses: success, false, data, never

ZodError.toString (packages/zod/src/v3/ZodError.ts:277-279)
  method ZodError.toString
  called_by: ZodError
  uses: this.message

$ZodFlattenedError (packages/zod/src/v4/core/errors.ts:250-250)
  type alias $ZodFlattenedError = _FlattenedError<T, U>
  uses: _FlattenedError, T, U

$ZodFlattenedError (packages/zod/src/v4/core/errors.ts:251-251)
  type alias $ZodFlattenedError = _FlattenedError<T, U>
  uses: _FlattenedError, T, U

$ZodFlattenedError (packages/zod/src/v4/core/errors.ts:252-252)
  type alias $ZodFlattenedError = _FlattenedError<T, U>
  uses: _FlattenedError, T, U

$ZodFlattenedError (packages/zod/src/v4/core/errors.ts:253-253)
  type alias $ZodFlattenedError = _FlattenedError<T, U>
  uses: _FlattenedError, T, U

$ZodFlattenedError (packages/zod/src/v4/core/errors.ts:254-254)
  type alias $ZodFlattenedError = _FlattenedError<T, U>
  uses: _FlattenedError, T, U

CustomErrorParams (packages/zod/src/v3/types.ts:55-55)
  type alias CustomErrorParams = Partial<util.Omit<ZodCustomIssue, "code">>
  uses: Partial, util.Omit, ZodCustomIssue, code

CustomErrorParams (packages/zod/src/v3/types.ts:56-56)
  type alias CustomErrorParams = Partial<util.Omit<ZodCustomIssue, "code">>
  uses: Partial, util.Omit, ZodCustomIssue, code

$ZodAsyncError.constructor (packages/zod/src/v4/core/core.ts:99-101)
  method $ZodAsyncError.constructor
  calls: constructor
  called_by: $ZodAsyncError, constructor, $ZodEncodeError

$ZodEncodeError.constructor (packages/zod/src/v4/core/core.ts:105-108)
  method $ZodEncodeError.constructor
  sig: $ZodEncodeError.constructor(name: string)
  calls: constructor
  called_by: constructor, $ZodAsyncError, $ZodEncodeError
  uses: this.name

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 1513 symbols in L3, 110 with behavior annotations
uncovered: errToObj, quotelessJson, toString, toString
drill: packages/zod/src/v3/ZodError.ts (~2 lines, ZodError.message)
drill: packages/zod/src/v3/types.ts (~4 lines, ZodNumber.multipleOf)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## ZodError.message  (packages/zod/src/v3/ZodError.ts L280-282)
```
  override get message() {
    return JSON.stringify(this.issues, util.jsonStringifyReplacer, 2);
  }
```

## ZodNumber.multipleOf  (packages/zod/src/v3/types.ts L1547-1554)
```
  multipleOf(value: number, message?: errorUtil.ErrMessage) {
    return this._addCheck({
      kind: "multipleOf",
      value: value,
      message: errorUtil.toString(message),
    });
  }
  step = this.multipleOf;
```

## AnyZodObject  (packages/zod/src/v3/types.ts L2926-2928)
```
export type AnyZodObject = ZodObject<any, any, any>;

////////////////////////////////////////
```

## AnyZodTuple  (packages/zod/src/v3/types.ts L3393-3394)
```
export type AnyZodTuple = ZodTuple<[ZodTypeAny, ...ZodTypeAny[]] | [], ZodTypeAny | null>;
// type ZodTupleItems = [ZodTypeAny, ...ZodTypeAny[]];
```

## ArrayCardinality  (packages/zod/src/v3/types.ts L2230-2231)
```
export type ArrayCardinality = "many" | "atleastone";
export type arrayOutputType<
```

## ArrayKeys  (packages/zod/src/v3/types.ts L4040-4041)
```
export type ArrayKeys = keyof any[];
export type Indices<T> = Exclude<keyof T, ArrayKeys>;
```

## AssertArray  (packages/zod/src/v3/types.ts L3369-3370)
```
export type AssertArray<T> = T extends any[] ? T : never;
export type OutputTypeOfTuple<T extends ZodTupleItems | []> = AssertArray<{
```

## BRAND  (packages/zod/src/v4/classic/compat.ts L40-40)
```
export type BRAND<T extends string | number | symbol = string | number | symbol> = {
```

## CatchallInput  (packages/zod/src/v3/types.ts L2408-2410)
```
export type CatchallInput<T extends ZodType> = ZodType extends T ? unknown : { [k: string]: T["_input"] };

export type PassthroughType<T extends UnknownKeysParam> = T extends "passthrough" ? { [k: string]: unknown } : unknown;
```

## CatchallOutput  (packages/zod/src/v3/types.ts L2406-2408)
```
export type CatchallOutput<T extends ZodType> = ZodType extends T ? unknown : { [k: string]: T["_output"] };

export type CatchallInput<T extends ZodType> = ZodType extends T ? unknown : { [k: string]: T["_input"] };
```

## Class.constructor  (packages/zod/src/v4/mini/schemas.ts L1784-1784)
```
  constructor(..._args: any[]) {}
```

## Class  (packages/zod/src/v4/mini/schemas.ts L1781-1785)
```

// instanceof
abstract class Class {
  constructor(..._args: any[]) {}
}
```

## CustomErrorParams  (packages/zod/src/v3/types.ts L56-56)
```
export type CustomErrorParams = Partial<util.Omit<ZodCustomIssue, "code">>;
```

## Effect  (packages/zod/src/v3/types.ts L4299-4301)
```
export type Effect<T> = RefinementEffect<T> | TransformEffect<T> | PreprocessEffect<T>;

export interface ZodEffectsDef<T extends ZodTypeAny = ZodTypeAny> extends ZodTypeDef {
```

## EnumLike  (packages/zod/src/v4/core/util.ts L168-168)
```
export type EnumLike = Readonly<Record<string, EnumValue>>;
```

## EnumValues  (packages/zod/src/v3/types.ts L4043-4045)
```
export type EnumValues<T extends string = string> = readonly [T, ...T[]];

export type Values<T extends EnumValues> = {
```

## FilterEnum  (packages/zod/src/v3/types.ts L4056-4057)
```
export type FilterEnum<Values, ToExclude> = Values extends []
  ? []
```

## Indices  (packages/zod/src/v3/types.ts L4041-4043)
```
export type Indices<T> = Exclude<keyof T, ArrayKeys>;

export type EnumValues<T extends string = string> = readonly [T, ...T[]];
```

## InputTypeOfTuple  (packages/zod/src/v3/types.ts L3378-3379)
```
export type InputTypeOfTuple<T extends ZodTupleItems | []> = AssertArray<{
  [k in keyof T]: T[k] extends ZodType<any, any, any> ? T[k]["_input"] : never;
```

## InputTypeOfTupleWithRest  (packages/zod/src/v3/types.ts L3381-3382)
```
export type InputTypeOfTupleWithRest<
  T extends ZodTupleItems | [],
```

## IpVersion  (packages/zod/src/v3/types.ts L544-544)
```
export type IpVersion = "v4" | "v6";
```

## KeySchema  (packages/zod/src/v3/types.ts L3493-3494)
```
export type KeySchema = ZodType<string | number | symbol, any, any>;
export type RecordType<K extends string | number | symbol, V> = [string] extends [K]
```

## OutputTypeOfTuple  (packages/zod/src/v3/types.ts L3370-3371)
```
export type OutputTypeOfTuple<T extends ZodTupleItems | []> = AssertArray<{
  [k in keyof T]: T[k] extends ZodType<any, any, any> ? T[k]["_output"] : never;
```

## OutputTypeOfTupleWithRest  (packages/zod/src/v3/types.ts L3373-3374)
```
export type OutputTypeOfTupleWithRest<
  T extends ZodTupleItems | [],
```

## ParseInputLazyPath.path  (packages/zod/src/v3/types.ts L74-84)
```
  get path() {
    if (!this._cachedPath.length) {
      if (Array.isArray(this._key)) {
        this._cachedPath.push(...this._path, ...this._key);
      } else {
        this._cachedPath.push(...this._path, this._key);
      }
    }

    return this._cachedPath;
  }
```

## ParseInputLazyPath  (packages/zod/src/v3/types.ts L61-85)
```

class ParseInputLazyPath implements ParseInput {
  parent: ParseContext;
  data: any;
  _path: ParsePath;
  _key: string | number | (string | number)[];
  _cachedPath: ParsePath = [];
  constructor(parent: ParseContext, value: any, path: ParsePath, key: string | number | (string | number)[]) {
    this.parent = parent;
    this.data = value;
    this._path = path;
    this._key = key;
  }
  get path() {
    if (!this._cachedPath.length) {
      if (Array.isArray(this._key)) {
        this._cachedPath.push(...this._path, ...this._key);
      } else {
        this._cachedPath.push(...this._path, this._key);
      }
    }

    return this._cachedPath;
  }
}
```

## PassthroughType  (packages/zod/src/v3/types.ts L2410-2412)
```
export type PassthroughType<T extends UnknownKeysParam> = T extends "passthrough" ? { [k: string]: unknown } : unknown;

export type deoptional<T extends ZodTypeAny> = T extends ZodOptional<infer U>
```

## PreprocessEffect  (packages/zod/src/v3/types.ts L4295-4296)
```
export type PreprocessEffect<T> = {
  type: "preprocess";
```

## ProcessedCreateParams  (packages/zod/src/v3/types.ts L119-119)
```
export type ProcessedCreateParams = {
```

## RawCreateParams  (packages/zod/src/v3/types.ts L110-110)
```
export type RawCreateParams =
```

## RecordType  (packages/zod/src/v3/types.ts L3494-3495)
```
export type RecordType<K extends string | number | symbol, V> = [string] extends [K]
  ? Record<K, V>
```

## Refinement  (packages/zod/src/v3/types.ts L4284-4285)
```
export type Refinement<T> = (arg: T, ctx: RefinementCtx) => any;
export type SuperRefinement<T> = (arg: T, ctx: RefinementCtx) => void | Promise<void>;
```

## RefinementCtx  (packages/zod/src/v3/types.ts L38-48)
```
///////////////////////////////////////
//////////                   //////////
//////////      ZodType      //////////
//////////                   //////////
///////////////////////////////////////
///////////////////////////////////////

export interface RefinementCtx {
  addIssue: (arg: IssueData) => void;
  path: (string | number)[];
}
```

## RefinementEffect  (packages/zod/src/v3/types.ts L4287-4288)
```
export type RefinementEffect<T> = {
  type: "refinement";
```

## SafeParseError  (packages/zod/src/v4/core/util.ts L181-181)
```
export type SafeParseError<T> = {
```

## SafeParseReturnType  (packages/zod/src/v3/types.ts L156-156)
```
export type SafeParseReturnType<Input, Output> = SafeParseSuccess<Output> | SafeParseError<Input>;
```

## SafeParseSuccess  (packages/zod/src/v4/core/util.ts L180-180)
```
export type SafeParseSuccess<T> = { success: true; data: T; error?: never };
```

## SomeZodObject  (packages/zod/src/v3/types.ts L2418-2420)
```
export type SomeZodObject = ZodObject<ZodRawShape, UnknownKeysParam, ZodTypeAny>;

export type noUnrecognized<Obj extends object, Shape extends object> = {
```

## SuperRefinement  (packages/zod/src/v3/types.ts L4285-4287)
```
export type SuperRefinement<T> = (arg: T, ctx: RefinementCtx) => void | Promise<void>;

export type RefinementEffect<T> = {
```

## TransformEffect  (packages/zod/src/v3/types.ts L4291-4292)
```
export type TransformEffect<T> = {
  type: "transform";
```

## UnknownKeysParam  (packages/zod/src/v3/types.ts L2368-2370)
```
export type UnknownKeysParam = "passthrough" | "strict" | "strip";

export interface ZodObjectDef<
```

## Values  (packages/zod/src/v3/types.ts L4045-4046)
```
export type Values<T extends EnumValues> = {
  [k in T[number]]: k;
```

## Writeable  (packages/zod/src/v4/core/util.ts L101-101)
```
export type Writeable<T> = { -readonly [P in keyof T]: T[P] } & {};
```

## ZodAny._parse  (packages/zod/src/v3/types.ts L2115-2118)
```
  _parse(input: ParseInput): ParseReturnType<this["_output"]> {
    return OK(input.data);
  }
  static create = (params?: RawCreateParams): ZodAny => {
```

## ZodAny  (packages/zod/src/v4/classic/schemas.ts L1049-1051)
```

// ZodAny
export interface ZodAny extends _ZodType<core.$ZodAnyInternals> {}
```

## ZodAnyDef  (packages/zod/src/v3/types.ts L2101-2112)
```
//////////////////////////////////////
//////////////////////////////////////
//////////                  //////////
//////////      ZodAny      //////////
//////////                  //////////
//////////////////////////////////////
//////////////////////////////////////
export interface ZodAnyDef extends ZodTypeDef {
  typeName: ZodFirstPartyTypeKind.ZodAny;
}

export class ZodAny extends ZodType<any, ZodAnyDef, any> {
```

## ZodArray._parse  (packages/zod/src/v3/types.ts L2241-2317)
```
  _parse(input: ParseInput): ParseReturnType<this["_output"]> {
    const { ctx, status } = this._processInputParams(input);

    const def = this._def;

    if (ctx.parsedType !== ZodParsedType.array) {
      addIssueToContext(ctx, {
        code: ZodIssueCode.invalid_type,
        expected: ZodParsedType.array,
        received: ctx.parsedType,
      });
      return INVALID;
    }

    if (def.exactLength !== null) {
      const tooBig = ctx.data.length > def.exactLength.value;
      const tooSmall = ctx.data.length < def.exactLength.value;
      if (tooBig || tooSmall) {
        addIssueToContext(ctx, {
          code: tooBig ? ZodIssueCode.too_big : ZodIssueCode.too_small,
          minimum: (tooSmall ? def.exactLength.value : undefined) as number,
          maximum: (tooBig ? def.exactLength.value : undefined) as number,
          type: "array",
          inclusive: true,
          exact: true,
          message: def.exactLength.message,
        });
        status.dirty();
      }
    }

    if (def.minLength !== null) {
      if (ctx.data.length < def.minLength.value) {
        addIssueToContext(ctx, {
          code: ZodIssueCode.too_small,
          minimum: def.minLength.value,
          type: "array",
... (truncated)
```
--- END SOURCE SNIPPETS ---

QUESTION: How does Zod decide which error message to emit when multiple customization layers are available?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
