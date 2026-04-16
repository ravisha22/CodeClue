# Blind Evaluation Prompt - MRLF v2.4
# Task: blind-zod-rel-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 zod@HEAD 390mod 2677sym
? What inheritance and extension relationships connect Zod's core, full, and mini schema/error types?


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
ZodFunction._parse                  M packages/zod/src/v3/types.ts:3822   method ZodFunction._parse
ZodDate._parse                      M packages/zod/src/v3/types.ts:1878   method ZodDate._parse
ZodPipeline._parse                  M packages/zod/src/v3/types.ts:4782   method ZodPipeline._parse
ZodUnion._parse                     M packages/zod/src/v3/types.ts:2947   method ZodUnion._parse
ZodBoolean._parse                   M packages/zod/src/v3/types.ts:1834   method ZodBoolean._parse
ZodEnum._parse                      M packages/zod/src/v3/types.ts:4082   method ZodEnum._parse
ZodPromise._parse                   M packages/zod/src/v3/types.ts:4244   method ZodPromise._parse
ZodSymbol._parse                    M packages/zod/src/v3/types.ts:2010   method ZodSymbol._parse
ZodVoid._parse                      M packages/zod/src/v3/types.ts:2193   method ZodVoid._parse
ZodNaN._parse                       M packages/zod/src/v3/types.ts:4702   method ZodNaN._parse
ZodNull._parse                      M packages/zod/src/v3/types.ts:2080   method ZodNull._parse
ZodUndefined._parse                 M packages/zod/src/v3/types.ts:2045   method ZodUndefined._parse
ZodLiteral._parse                   M packages/zod/src/v3/types.ts:4007   method ZodLiteral._parse
ZodMap._parse                       M packages/zod/src/v3/types.ts:3603   method ZodMap._parse
ZodNativeEnum._parse                M packages/zod/src/v3/types.ts:4179   method ZodNativeEnum._parse
ZodNever._parse                     M packages/zod/src/v3/types.ts:2164   method ZodNever._parse
ZodSet._parse                       M packages/zod/src/v3/types.ts:3691   method ZodSet._parse
ZodTuple._parse                     M packages/zod/src/v3/types.ts:3399   method ZodTuple._parse
ZodRecord._parse                    M packages/zod/src/v3/types.ts:3514   method ZodRecord._parse
ZodBranded._parse                   M packages/zod/src/v3/types.ts:4748   method ZodBranded._parse
ZodCatch._parse                     M packages/zod/src/v3/types.ts:4619   method ZodCatch._parse
ZodDefault._parse                   M packages/zod/src/v3/types.ts:4569   method ZodDefault._parse
ZodLazy._parse                      M packages/zod/src/v3/types.ts:3979   method ZodLazy._parse
ZodNullable._parse                  M packages/zod/src/v3/types.ts:4530   method ZodNullable._parse
ZodOptional._parse                  M packages/zod/src/v3/types.ts:4490   method ZodOptional._parse
ZodReadonly._parse                  M packages/zod/src/v3/types.ts:4877   method ZodReadonly._parse
ZodUnknown._parse                   M packages/zod/src/v3/types.ts:2140   method ZodUnknown._parse
ZodAny._parse                       M packages/zod/src/v3/types.ts:2115   method ZodAny._parse
ZodPromise.unwrap                   M packages/zod/src/v3/types.ts:4240   method ZodPromise.unwrap
ZodBranded.unwrap                   M packages/zod/src/v3/types.ts:4758   method ZodBranded.unwrap
ZodNullable.unwrap                  M packages/zod/src/v3/types.ts:4538   method ZodNullable.unwrap
ZodOptional.unwrap                  M packages/zod/src/v3/types.ts:4498   method ZodOptional.unwrap
ZodReadonly.unwrap                  M packages/zod/src/v3/types.ts:4896   method ZodReadonly.unwrap
ZodBigInt.maxValue                  M packages/zod/src/v3/types.ts:1810   method ZodBigInt.maxValue
ZodBigInt.minValue                  M packages/zod/src/v3/types.ts:1800   method ZodBigInt.minValue
ZodNumber.maxValue                  M packages/zod/src/v3/types.ts:1587   method ZodNumber.maxValue
  ...and 2442 more symbols

-- FOCUS
$ZodStandardSchema (packages/zod/src/v4/core/schemas.ts:170-170)
  type alias $ZodStandardSchema = StandardSchemaV1.Props<core.input<T>, core.output<T>>
  uses: StandardSchemaV1.Props, core.input, T, core.output

$ZodStandardSchema (packages/zod/src/v4/core/schemas.ts:169-169)
  type alias $ZodStandardSchema = StandardSchemaV1.Props<core.input<T>, core.output<T>>
  uses: StandardSchemaV1.Props, core.input, T, core.output

ZodStandardSchemaWithJSON (packages/zod/src/v4/core/to-json-schema.ts:582-582)
  type alias ZodStandardSchemaWithJSON = StandardSchemaWithJSONProps<core.input<T>, core.output<T>>
  uses: StandardSchemaWithJSONProps, core.input, T, core.output

ZodStandardSchemaWithJSON (packages/zod/src/v4/core/to-json-schema.ts:582-583)
  type alias ZodStandardSchemaWithJSON = StandardSchemaWithJSONProps<core.input<T>, core.output<T>>
  uses: StandardSchemaWithJSONProps, core.input, T, core.output

ZodFirstPartySchemaTypes (packages/zod/src/v3/types.ts:4996-4997)
  type alias ZodFirstPartySchemaTypes = | ZodString | ZodNumber | ZodNaN | ZodBigInt | ZodBoolean | ZodDate | ZodUndefined
  uses: ZodString, ZodNumber, ZodNaN, ZodBigInt

ZodStandardSchemaWithJSON (packages/zod/src/v4/classic/schemas.ts:12-12)
  type alias ZodStandardSchemaWithJSON = StandardSchemaWithJSONProps<core.input<T>, core.output<T>>
  uses: StandardSchemaWithJSONProps, core.input, T, core.output

ZodStandardSchemaWithJSON (packages/zod/src/v4/classic/schemas.ts:17-17)
  type alias ZodStandardSchemaWithJSON = StandardSchemaWithJSONProps<core.input<T>, core.output<T>>
  uses: StandardSchemaWithJSONProps, core.input, T, core.output

ZodStandardSchemaWithJSON (packages/zod/src/v4/classic/schemas.ts:15-15)
  type alias ZodStandardSchemaWithJSON = StandardSchemaWithJSONProps<core.input<T>, core.output<T>>
  uses: StandardSchemaWithJSONProps, core.input, T, core.output

ZodStandardSchemaWithJSON (packages/zod/src/v4/classic/schemas.ts:18-18)
  type alias ZodStandardSchemaWithJSON = StandardSchemaWithJSONProps<core.input<T>, core.output<T>>
  uses: StandardSchemaWithJSONProps, core.input, T, core.output

ZodStandardSchemaWithJSON (packages/zod/src/v4/classic/schemas.ts:14-14)
  type alias ZodStandardSchemaWithJSON = StandardSchemaWithJSONProps<core.input<T>, core.output<T>>
  uses: StandardSchemaWithJSONProps, core.input, T, core.output

ZodStandardSchemaWithJSON (packages/zod/src/v4/classic/schemas.ts:13-13)
  type alias ZodStandardSchemaWithJSON = StandardSchemaWithJSONProps<core.input<T>, core.output<T>>
  uses: StandardSchemaWithJSONProps, core.input, T, core.output

ZodStandardSchemaWithJSON (packages/zod/src/v4/classic/schemas.ts:16-16)
  type alias ZodStandardSchemaWithJSON = StandardSchemaWithJSONProps<core.input<T>, core.output<T>>
  uses: StandardSchemaWithJSONProps, core.input, T, core.output

ZodStandardSchemaWithJSON (packages/zod/src/v4/classic/schemas.ts:19-19)
  type alias ZodStandardSchemaWithJSON = StandardSchemaWithJSONProps<core.input<T>, core.output<T>>
  uses: StandardSchemaWithJSONProps, core.input, T, core.output

inferFlattenedErrors (packages/zod/src/v4/classic/compat.ts:31-31)
  type alias inferFlattenedErrors = core.$ZodFlattenedError<core.output<T>, U>
  uses: core.$ZodFlattenedError, core.output, T, U

$ZodError (packages/zod/src/v4/core/errors.ts:214-217)
  interface $ZodError
  extends: Error
  uses: Symbol.for, zod.error

ZodInvalidIntersectionTypesIssue (packages/zod/src/v3/ZodError.ts:131-134)
  interface ZodInvalidIntersectionTypesIssue
  extends: ZodIssueBase
  uses: ZodIssueCode.invalid_intersection_types

$ZodRealError (packages/zod/src/v4/core/errors.ts:248-248)
  interface $ZodRealError
  extends: $ZodError

ZodError (packages/zod/src/v4/classic/errors.ts:9-23)
  interface ZodError
  extends: $ZodError
  methods: addIssue, addIssues, flatten, format
  calls: addIssue, addIssues, flatten, format
  uses: z.treeifyError, core.$ZodFormattedError, core.$ZodIssue, core.$ZodFlattenedError

ZodMiniISODate (packages/zod/src/v4/mini/iso.ts:19-23)
  interface ZodMiniISODate
  extends: ZodMiniStringFormat
  uses: schemas.ZodMiniStringFormat, core.$ZodISODateInternals

ZodMiniISODateTime (packages/zod/src/v4/mini/iso.ts:3-7)
  interface ZodMiniISODateTime
  extends: ZodMiniStringFormat
  uses: schemas.ZodMiniStringFormat, core.$ZodISODateTimeInternals

ZodMiniISODuration (packages/zod/src/v4/mini/iso.ts:51-55)
  interface ZodMiniISODuration
  extends: ZodMiniStringFormat
  uses: schemas.ZodMiniStringFormat, core.$ZodISODurationInternals

ZodMiniISOTime (packages/zod/src/v4/mini/iso.ts:35-39)
  interface ZodMiniISOTime
  extends: ZodMiniStringFormat
  uses: schemas.ZodMiniStringFormat, core.$ZodISOTimeInternals

$ZodAsyncError (packages/zod/src/v4/core/core.ts:97-102)
  extends: Error
  methods: constructor
  calls: constructor
  uses: this.name

$ZodEncodeError (packages/zod/src/v4/core/core.ts:103-109)
  extends: Error
  methods: constructor
  calls: constructor
  uses: this.name

$ZodError (packages/zod/src/v4/core/errors.ts:218-227)
  interface $ZodError
  extends: Error

_ZodMiniString (packages/zod/src/v4/mini/schemas.ts:80-85)
  interface _ZodMiniString
  extends: _ZodMiniType, $ZodString
  uses: core.$ZodString

ZodMiniObject (packages/zod/src/v4/mini/schemas.ts:814-823)
  interface ZodMiniObject
  extends: ZodMiniType, $ZodObject
  called_by: looseObject, strictObject
  uses: core.$ZodObject

ZodMiniUnion (packages/zod/src/v4/mini/schemas.ts:997-1002)
  interface ZodMiniUnion
  extends: _ZodMiniType
  called_by: union
  uses: core.$ZodUnionInternals

ZodMiniRecord (packages/zod/src/v4/mini/schemas.ts:1143-1150)
  interface ZodMiniRecord
  extends: _ZodMiniType
  called_by: looseRecord, partialRecord, record
  uses: core.$ZodRecordInternals

ZodMiniFunction (packages/zod/src/v4/mini/schemas.ts:1851-1870)
  interface ZodMiniFunction
  extends: _ZodMiniType, $ZodFunction
  methods: input, input, output
  calls: input
  uses: core.$ZodFunction, core.$ZodFunctionDef, core.$InferInnerFunctionType, core.$InferOuterFunctionType

ZodMiniEnum (packages/zod/src/v4/mini/schemas.ts:1243-1248)
  interface ZodMiniEnum
  extends: _ZodMiniType
  called_by: _enum, nativeEnum
  uses: util.EnumLike, core.$ZodEnumInternals

_ZodMiniNumber (packages/zod/src/v4/mini/schemas.ts:517-523)
  interface _ZodMiniNumber
  extends: _ZodMiniType, $ZodNumber
  uses: core.$ZodNumber

ZodMiniNullable (packages/zod/src/v4/mini/schemas.ts:1404-1409)
  interface ZodMiniNullable
  extends: _ZodMiniType
  called_by: nullable
  uses: core.$ZodNullableInternals

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 0 with behavior annotations
uncovered: $ZodErrorClass, $ZodErrorClass, $ZodFlattenedError, $ZodFlattenedError

--- CLUE FILE END ---

QUESTION: What inheritance and extension relationships connect Zod's core, full, and mini schema/error types?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
