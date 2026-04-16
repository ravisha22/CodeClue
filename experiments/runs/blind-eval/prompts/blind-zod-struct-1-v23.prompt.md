# Blind Evaluation Prompt - MRLF v2.4
# Task: blind-zod-struct-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

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

_ZodMiniString (packages/zod/src/v4/mini/schemas.ts:80-85)
  interface _ZodMiniString
  extends: _ZodMiniType, $ZodString
  uses: core.$ZodString

ZodMiniType (packages/zod/src/v4/mini/schemas.ts:6-38)
  interface ZodMiniType
  extends: $ZodType
  methods: clone, parse, parseAsync, safeParse
  calls: clone, parse, parseAsync, safeParse, check
  uses: core.$ZodType, core.CheckFn, core.output, core.$ZodCheck

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

ZodMiniOptional (packages/zod/src/v4/mini/schemas.ts:1360-1366)
  interface ZodMiniOptional
  extends: _ZodMiniType, $ZodOptional
  called_by: optional
  uses: core.$ZodOptional, core.$ZodOptionalInternals

ZodMiniReadonly (packages/zod/src/v4/mini/schemas.ts:1636-1641)
  interface ZodMiniReadonly
  extends: _ZodMiniType
  called_by: readonly
  uses: core.$ZodReadonlyInternals

ZodMiniTransform (packages/zod/src/v4/mini/schemas.ts:1338-1342)
  interface ZodMiniTransform
  extends: _ZodMiniType
  called_by: transform
  uses: core.$ZodTransformInternals

ZodMiniArray (packages/zod/src/v4/mini/schemas.ts:783-789)
  interface ZodMiniArray
  extends: _ZodMiniType, $ZodArray
  called_by: array
  uses: core.$ZodArray, core.$ZodArrayInternals

ZodMiniLazy (packages/zod/src/v4/mini/schemas.ts:1682-1686)
  interface ZodMiniLazy
  extends: _ZodMiniType
  called_by: _lazy
  uses: core.$ZodType, core.$ZodLazyInternals

ZodMiniCatch (packages/zod/src/v4/mini/schemas.ts:1528-1532)
  interface ZodMiniCatch
  extends: _ZodMiniType
  called_by: _catch
  uses: core.$ZodType, core.$ZodCatchInternals

ZodMiniDefault (packages/zod/src/v4/mini/schemas.ts:1431-1435)
  interface ZodMiniDefault
  extends: _ZodMiniType
  called_by: _default
  uses: core.$ZodType, core.$ZodDefaultInternals

ZodMiniDiscriminatedUnion (packages/zod/src/v4/mini/schemas.ts:1047-1054)
  interface ZodMiniDiscriminatedUnion
  extends: ZodMiniUnion
  called_by: discriminatedUnion
  uses: core.$ZodDiscriminatedUnionInternals

ZodMiniExactOptional (packages/zod/src/v4/mini/schemas.ts:1382-1388)
  interface ZodMiniExactOptional
  extends: _ZodMiniType, $ZodExactOptional
  called_by: exactOptional
  uses: core.$ZodExactOptional, core.$ZodExactOptionalInternals

ZodMiniIntersection (packages/zod/src/v4/mini/schemas.ts:1079-1084)
  interface ZodMiniIntersection
  extends: _ZodMiniType
  called_by: intersection
  uses: core.$ZodIntersectionInternals

ZodMiniLiteral (packages/zod/src/v4/mini/schemas.ts:1291-1296)
  interface ZodMiniLiteral
  extends: _ZodMiniType
  called_by: literal
  uses: core.$ZodLiteralInternals

ZodMiniNonOptional (packages/zod/src/v4/mini/schemas.ts:1483-1488)
  interface ZodMiniNonOptional
  extends: _ZodMiniType
  called_by: nonoptional
  uses: core.$ZodNonOptionalInternals

ZodMiniPipe (packages/zod/src/v4/mini/schemas.ts:1569-1574)
  interface ZodMiniPipe
  extends: _ZodMiniType
  uses: core.$ZodPipeInternals

ZodMiniPrefault (packages/zod/src/v4/mini/schemas.ts:1457-1462)
  interface ZodMiniPrefault
  extends: _ZodMiniType
  called_by: prefault
  uses: core.$ZodPrefaultInternals

ZodMiniPromise (packages/zod/src/v4/mini/schemas.ts:1706-1710)
  interface ZodMiniPromise
  extends: _ZodMiniType
  called_by: promise
  uses: core.$ZodType, core.$ZodPromiseInternals

ZodMiniSet (packages/zod/src/v4/mini/schemas.ts:1225-1229)
  interface ZodMiniSet
  extends: _ZodMiniType
  called_by: set
  uses: core.$ZodType, core.$ZodSetInternals

ZodMiniStringFormat (packages/zod/src/v4/mini/schemas.ts:103-109)
  interface ZodMiniStringFormat
  extends: _ZodMiniString, $ZodStringFormat
  uses: core.$ZodStringFormat, core.$ZodStringFormatInternals

ZodMiniSuccess (packages/zod/src/v4/mini/schemas.ts:1508-1512)
  interface ZodMiniSuccess
  extends: _ZodMiniType
  called_by: success
  uses: core.$ZodType, core.$ZodSuccessInternals

ZodMiniTemplateLiteral (packages/zod/src/v4/mini/schemas.ts:1657-1662)
  interface ZodMiniTemplateLiteral
  extends: _ZodMiniType
  called_by: templateLiteral
  uses: core.$ZodTemplateLiteralInternals

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 80 symbols in L3, 0 with behavior annotations
uncovered: $InferZodRecordInput, $InferZodRecordInput, $InferZodRecordInput, $InferZodRecordInput

--- CLUE FILE END ---

QUESTION: How is Zod 4 split across the `zod`, `zod/mini`, and `zod/v4/core` packages?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
