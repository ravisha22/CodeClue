# Blind Evaluation Prompt - MRLF v2.1
# Task: blind-zod-struct-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

--- CLUE FILE START ---
=CC v2.1 zod@HEAD 390mod 2677sym
? How is Zod 4 split across the `zod`, `zod/mini`, and `zod/v4/core` packages?


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

ZodMiniType (packages/zod/src/v4/mini/schemas.ts:6-38)
  interface ZodMiniType
  extends: $ZodType
  methods: clone, parse, parseAsync, safeParse
  calls: clone, parse, parseAsync, safeParse, check
  uses: core.$ZodType, core.CheckFn, core.output, core.$ZodCheck

ZodMiniFunction (packages/zod/src/v4/mini/schemas.ts:1851-1870)
  interface ZodMiniFunction
  extends: $ZodFunctionInternals, $ZodFunction
  methods: input, input, output
  calls: input
  uses: core.$ZodFunction, core.$ZodFunctionDef, core.$InferInnerFunctionType, core.$InferOuterFunctionType

ZodMiniUnion (packages/zod/src/v4/mini/schemas.ts:997-1002)
  interface ZodMiniUnion
  extends: $ZodUnionInternals
  called_by: union
  uses: core.$ZodUnionInternals

ZodMiniDiscriminatedUnion (packages/zod/src/v4/mini/schemas.ts:1047-1054)
  interface ZodMiniDiscriminatedUnion
  extends: ZodMiniUnion
  called_by: discriminatedUnion
  uses: core.$ZodDiscriminatedUnionInternals

ZodMiniCodec (packages/zod/src/v4/mini/schemas.ts:1594-1601)
  interface ZodMiniCodec
  extends: ZodMiniPipe, $ZodCodec
  uses: core.$ZodCodec, core.$ZodCodecInternals, core.$ZodCodecDef

ZodMiniCustomStringFormat (packages/zod/src/v4/mini/schemas.ts:469-475)
  interface ZodMiniCustomStringFormat
  extends: ZodMiniStringFormat, $ZodCustomStringFormat
  uses: core.$ZodCustomStringFormat, core.$ZodCustomStringFormatInternals

ZodMiniPipe (packages/zod/src/v4/mini/schemas.ts:1569-1574)
  interface ZodMiniPipe
  extends: $ZodPipeInternals
  uses: core.$ZodPipeInternals

ZodMiniStringFormat (packages/zod/src/v4/mini/schemas.ts:103-109)
  interface ZodMiniStringFormat
  extends: $ZodStringFormatInternals, $ZodStringFormat
  uses: core.$ZodStringFormat, core.$ZodStringFormatInternals

_ZodMiniNumber (packages/zod/src/v4/mini/schemas.ts:517-523)
  interface _ZodMiniNumber
  extends: _ZodMiniType, $ZodNumber
  uses: core.$ZodNumber

_ZodMiniString (packages/zod/src/v4/mini/schemas.ts:80-85)
  interface _ZodMiniString
  extends: _ZodMiniType, $ZodString
  uses: core.$ZodString

_ZodMiniJSONSchemaInternals (packages/zod/src/v4/mini/schemas.ts:1834-1834)
  type alias _ZodMiniJSONSchemaInternals = _ZodMiniJSONSchema["_zod"]
  uses: _ZodMiniJSONSchema, _zod

ZodMiniRecord (packages/zod/src/v4/mini/schemas.ts:1143-1150)
  interface ZodMiniRecord
  extends: $ZodRecordInternals
  called_by: looseRecord, partialRecord, record
  uses: core.$ZodRecordInternals

ZodMiniEnum (packages/zod/src/v4/mini/schemas.ts:1243-1248)
  interface ZodMiniEnum
  extends: $ZodEnumInternals
  called_by: _enum, nativeEnum
  uses: util.EnumLike, core.$ZodEnumInternals

ZodMiniObject (packages/zod/src/v4/mini/schemas.ts:814-823)
  interface ZodMiniObject
  extends: $ZodObjectInternals, $ZodObject
  called_by: looseObject, strictObject
  uses: core.$ZodObject

ZodMiniAny (packages/zod/src/v4/mini/schemas.ts:699-703)
  interface ZodMiniAny
  uses: core.$ZodAnyInternals

ZodMiniArray (packages/zod/src/v4/mini/schemas.ts:783-789)
  interface ZodMiniArray
  extends: $ZodArrayInternals, $ZodArray
  called_by: array
  uses: core.$ZodArray, core.$ZodArrayInternals

ZodMiniBase64 (packages/zod/src/v4/mini/schemas.ts:406-410)
  interface ZodMiniBase64
  uses: core.$ZodBase64Internals

ZodMiniBase64URL (packages/zod/src/v4/mini/schemas.ts:422-426)
  interface ZodMiniBase64URL
  uses: core.$ZodBase64URLInternals

ZodMiniBigInt (packages/zod/src/v4/mini/schemas.ts:601-605)
  interface ZodMiniBigInt
  extends: $ZodBigIntInternals, $ZodBigInt
  uses: core.$ZodBigIntInternals, core.$ZodBigInt

ZodMiniBigIntFormat (packages/zod/src/v4/mini/schemas.ts:618-624)
  interface ZodMiniBigIntFormat
  uses: core.$ZodBigIntFormatInternals

ZodMiniBoolean (packages/zod/src/v4/mini/schemas.ts:584-588)
  interface ZodMiniBoolean
  extends: $ZodBooleanInternals
  uses: core.$ZodBooleanInternals

ZodMiniCIDRv4 (packages/zod/src/v4/mini/schemas.ts:358-362)
  interface ZodMiniCIDRv4
  uses: core.$ZodCIDRv4Internals

ZodMiniCIDRv6 (packages/zod/src/v4/mini/schemas.ts:375-379)
  interface ZodMiniCIDRv6
  uses: core.$ZodCIDRv6Internals

ZodMiniCUID (packages/zod/src/v4/mini/schemas.ts:242-246)
  interface ZodMiniCUID
  uses: core.$ZodCUIDInternals

ZodMiniCUID2 (packages/zod/src/v4/mini/schemas.ts:259-263)
  interface ZodMiniCUID2
  uses: core.$ZodCUID2Internals

ZodMiniCatch (packages/zod/src/v4/mini/schemas.ts:1528-1532)
  interface ZodMiniCatch
  extends: $ZodCatchInternals
  called_by: _catch
  uses: core.$ZodType, core.$ZodCatchInternals

ZodMiniCustom (packages/zod/src/v4/mini/schemas.ts:1726-1730)
  interface ZodMiniCustom
  extends: $ZodCustomInternals
  uses: core.$ZodCustomInternals

ZodMiniDate (packages/zod/src/v4/mini/schemas.ts:765-769)
  interface ZodMiniDate
  extends: $ZodDateInternals
  uses: core.$ZodDateInternals

ZodMiniDefault (packages/zod/src/v4/mini/schemas.ts:1431-1435)
  interface ZodMiniDefault
  extends: $ZodDefaultInternals
  called_by: _default
  uses: core.$ZodType, core.$ZodDefaultInternals

ZodMiniE164 (packages/zod/src/v4/mini/schemas.ts:438-442)
  interface ZodMiniE164
  uses: core.$ZodE164Internals

ZodMiniEmail (packages/zod/src/v4/mini/schemas.ts:117-119)
  interface ZodMiniEmail
  uses: core.$ZodEmailInternals

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 80 symbols in L3, 0 with behavior annotations
uncovered: $InferZodRecordInput, $InferZodRecordInput, $InferZodRecordInput, $InferZodRecordInput

--- CLUE FILE END ---

QUESTION: How is Zod 4 split across the `zod`, `zod/mini`, and `zod/v4/core` packages?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
