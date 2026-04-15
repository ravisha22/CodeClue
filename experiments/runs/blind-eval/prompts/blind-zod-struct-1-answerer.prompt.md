# Blind Evaluation Prompt - MRLF v2.1
# Task: blind-zod-struct-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

--- CLUE FILE START ---
=CC v2.1 zod@HEAD 390mod 1321sym
? How is Zod 4 split across the `zod`, `zod/mini`, and `zod/v4/core` packages?


-- TREE
packages/  (384 files)
  bench/  docs/  resolution/  treeshake/  tsc/  zod/
scripts/  (4 files)
play.ts  vitest.config.ts

-- INDEX
packages/zod/src/v3/types.ts                   5138L  constructor, Class, path, ParseInputLazyPath, RefinementCtx
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
packages/bench/object-setup.ts                   35L  
  ...and 364 more modules

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
ZodNumber                           C packages/zod/src/v3/types.ts:1369   class ZodNumber
ZodBigInt                           C packages/zod/src/v3/types.ts:1635   class ZodBigInt
ZodBigInt.setLimit                  M packages/zod/src/v3/types.ts:1734   method ZodBigInt.setLimit
ZodNumber.setLimit                  M packages/zod/src/v3/types.ts:1482   method ZodNumber.setLimit
ZodString._parse                    M packages/zod/src/v3/types.ts:732    method ZodString._parse
ZodNumber._parse                    M packages/zod/src/v3/types.ts:1370   method ZodNumber._parse
ZodEffects._parse                   M packages/zod/src/v3/types.ts:4322   method ZodEffects._parse
ZodBigInt._parse                    M packages/zod/src/v3/types.ts:1636   method ZodBigInt._parse
ZodIntersection._parse              M packages/zod/src/v3/types.ts:3292   method ZodIntersection._parse
ZodArray._parse                     M packages/zod/src/v3/types.ts:2241   method ZodArray._parse
ZodDate._parse                      M packages/zod/src/v3/types.ts:1878   method ZodDate._parse
ZodFunction._parse                  M packages/zod/src/v3/types.ts:3822   method ZodFunction._parse
ZodPipeline._parse                  M packages/zod/src/v3/types.ts:4782   method ZodPipeline._parse
ZodUnion._parse                     M packages/zod/src/v3/types.ts:2947   method ZodUnion._parse
ZodBoolean._parse                   M packages/zod/src/v3/types.ts:1834   method ZodBoolean._parse
ZodEnum._parse                      M packages/zod/src/v3/types.ts:4082   method ZodEnum._parse
ZodNaN._parse                       M packages/zod/src/v3/types.ts:4702   method ZodNaN._parse
ZodNull._parse                      M packages/zod/src/v3/types.ts:2080   method ZodNull._parse
ZodPromise._parse                   M packages/zod/src/v3/types.ts:4244   method ZodPromise._parse
ZodSymbol._parse                    M packages/zod/src/v3/types.ts:2010   method ZodSymbol._parse
ZodUndefined._parse                 M packages/zod/src/v3/types.ts:2045   method ZodUndefined._parse
ZodVoid._parse                      M packages/zod/src/v3/types.ts:2193   method ZodVoid._parse
ZodLiteral._parse                   M packages/zod/src/v3/types.ts:4007   method ZodLiteral._parse
ZodMap._parse                       M packages/zod/src/v3/types.ts:3603   method ZodMap._parse
ZodNativeEnum._parse                M packages/zod/src/v3/types.ts:4179   method ZodNativeEnum._parse
ZodNever._parse                     M packages/zod/src/v3/types.ts:2164   method ZodNever._parse
ZodRecord._parse                    M packages/zod/src/v3/types.ts:3514   method ZodRecord._parse
ZodSet._parse                       M packages/zod/src/v3/types.ts:3691   method ZodSet._parse
ZodTuple._parse                     M packages/zod/src/v3/types.ts:3399   method ZodTuple._parse
ZodBranded._parse                   M packages/zod/src/v3/types.ts:4748   method ZodBranded._parse
ZodCatch._parse                     M packages/zod/src/v3/types.ts:4619   method ZodCatch._parse
ZodDefault._parse                   M packages/zod/src/v3/types.ts:4569   method ZodDefault._parse
ZodLazy._parse                      M packages/zod/src/v3/types.ts:3979   method ZodLazy._parse
ZodNullable._parse                  M packages/zod/src/v3/types.ts:4530   method ZodNullable._parse
ZodOptional._parse                  M packages/zod/src/v3/types.ts:4490   method ZodOptional._parse
ZodAny._parse                       M packages/zod/src/v3/types.ts:2115   method ZodAny._parse
ZodReadonly._parse                  M packages/zod/src/v3/types.ts:4877   method ZodReadonly._parse
ZodUnknown._parse                   M packages/zod/src/v3/types.ts:2140   method ZodUnknown._parse
ZodNullable.unwrap                  M packages/zod/src/v3/types.ts:4538   method ZodNullable.unwrap
ZodBranded.unwrap                   M packages/zod/src/v3/types.ts:4758   method ZodBranded.unwrap
ZodOptional.unwrap                  M packages/zod/src/v3/types.ts:4498   method ZodOptional.unwrap
ZodPromise.unwrap                   M packages/zod/src/v3/types.ts:4240   method ZodPromise.unwrap
ZodReadonly.unwrap                  M packages/zod/src/v3/types.ts:4896   method ZodReadonly.unwrap
ZodType._parseSync                  M packages/zod/src/v3/types.ts:210    method ZodType._parseSync
ZodBigInt.maxValue                  M packages/zod/src/v3/types.ts:1810   method ZodBigInt.maxValue
ZodBigInt.minValue                  M packages/zod/src/v3/types.ts:1800   method ZodBigInt.minValue
ZodNumber.maxValue                  M packages/zod/src/v3/types.ts:1587   method ZodNumber.maxValue
ZodNumber.minValue                  M packages/zod/src/v3/types.ts:1577   method ZodNumber.minValue
  ...and 1103 more symbols

-- FOCUS
_ZodMiniType (packages/zod/src/v4/mini/schemas.ts:40-41)
  interface _ZodMiniType

_ZodMiniString (packages/zod/src/v4/mini/schemas.ts:81-85)
  interface _ZodMiniString

ZodMiniLazy (packages/zod/src/v4/mini/schemas.ts:1684-1686)
  interface ZodMiniLazy
  extends: _ZodMiniType
  called_by: _lazy

ZodMiniEnum (packages/zod/src/v4/mini/schemas.ts:1245-1248)
  interface ZodMiniEnum
  extends: _ZodMiniType
  called_by: _enum, nativeEnum

ZodMiniPromise (packages/zod/src/v4/mini/schemas.ts:1708-1710)
  interface ZodMiniPromise
  extends: _ZodMiniType
  called_by: promise

ZodMiniSet (packages/zod/src/v4/mini/schemas.ts:1227-1229)
  interface ZodMiniSet
  extends: _ZodMiniType
  called_by: set

ZodMiniSuccess (packages/zod/src/v4/mini/schemas.ts:1510-1512)
  interface ZodMiniSuccess
  extends: _ZodMiniType
  called_by: success

ZodMiniType (packages/zod/src/v4/mini/schemas.ts:7-38)
  interface ZodMiniType
  methods: clone, parse, parseAsync, safeParse
  calls: clone, parse, parseAsync, safeParse, check

ZodMiniFunction (packages/zod/src/v4/mini/schemas.ts:1853-1870)
  interface ZodMiniFunction
  methods: input, input, output
  calls: input

ZodMiniAny (packages/zod/src/v4/mini/schemas.ts:701-703)
  interface ZodMiniAny
  extends: _ZodMiniType

ZodMiniArray (packages/zod/src/v4/mini/schemas.ts:785-789)
  interface ZodMiniArray
  called_by: array

ZodMiniBase64 (packages/zod/src/v4/mini/schemas.ts:408-410)
  interface ZodMiniBase64
  extends: _ZodMiniString

ZodMiniBase64URL (packages/zod/src/v4/mini/schemas.ts:424-426)
  interface ZodMiniBase64URL
  extends: _ZodMiniString

ZodMiniBigInt (packages/zod/src/v4/mini/schemas.ts:603-605)
  interface ZodMiniBigInt
  extends: _ZodMiniType

ZodMiniBigIntFormat (packages/zod/src/v4/mini/schemas.ts:622-624)
  interface ZodMiniBigIntFormat
  extends: _ZodMiniType

ZodMiniBoolean (packages/zod/src/v4/mini/schemas.ts:586-588)
  interface ZodMiniBoolean
  extends: _ZodMiniType

ZodMiniCIDRv4 (packages/zod/src/v4/mini/schemas.ts:360-362)
  interface ZodMiniCIDRv4
  extends: _ZodMiniString

ZodMiniCIDRv6 (packages/zod/src/v4/mini/schemas.ts:377-379)
  interface ZodMiniCIDRv6
  extends: _ZodMiniString

ZodMiniCUID (packages/zod/src/v4/mini/schemas.ts:244-246)
  interface ZodMiniCUID
  extends: _ZodMiniString

ZodMiniCUID2 (packages/zod/src/v4/mini/schemas.ts:261-263)
  interface ZodMiniCUID2
  extends: _ZodMiniString

ZodMiniCatch (packages/zod/src/v4/mini/schemas.ts:1530-1532)
  interface ZodMiniCatch
  extends: _ZodMiniType

ZodMiniCodec (packages/zod/src/v4/mini/schemas.ts:1596-1601)
  interface ZodMiniCodec

ZodMiniCustom (packages/zod/src/v4/mini/schemas.ts:1728-1730)
  interface ZodMiniCustom
  extends: _ZodMiniType

ZodMiniCustomStringFormat (packages/zod/src/v4/mini/schemas.ts:471-475)
  interface ZodMiniCustomStringFormat

ZodMiniDate (packages/zod/src/v4/mini/schemas.ts:767-769)
  interface ZodMiniDate
  extends: _ZodMiniType

ZodMiniDefault (packages/zod/src/v4/mini/schemas.ts:1433-1435)
  interface ZodMiniDefault
  extends: _ZodMiniType

ZodMiniDiscriminatedUnion (packages/zod/src/v4/mini/schemas.ts:1049-1054)
  interface ZodMiniDiscriminatedUnion

ZodMiniE164 (packages/zod/src/v4/mini/schemas.ts:440-442)
  interface ZodMiniE164
  extends: _ZodMiniString

ZodMiniEmail (packages/zod/src/v4/mini/schemas.ts:119-119)
  interface ZodMiniEmail
  extends: _ZodMiniString

ZodMiniEmoji (packages/zod/src/v4/mini/schemas.ts:210-212)
  interface ZodMiniEmoji
  extends: _ZodMiniString

ZodMiniExactOptional (packages/zod/src/v4/mini/schemas.ts:1384-1388)
  interface ZodMiniExactOptional
  called_by: exactOptional

ZodMiniFile (packages/zod/src/v4/mini/schemas.ts:1323-1325)
  interface ZodMiniFile
  extends: _ZodMiniType

ZodMiniGUID (packages/zod/src/v4/mini/schemas.ts:134-136)
  interface ZodMiniGUID
  extends: _ZodMiniString

ZodMiniIPv4 (packages/zod/src/v4/mini/schemas.ts:326-328)
  interface ZodMiniIPv4
  extends: _ZodMiniString

ZodMiniIPv6 (packages/zod/src/v4/mini/schemas.ts:343-345)
  interface ZodMiniIPv6
  extends: _ZodMiniString

ZodMiniISODate (packages/zod/src/v4/mini/iso.ts:21-23)
  interface ZodMiniISODate
  extends: ZodMiniStringFormat

ZodMiniISODateTime (packages/zod/src/v4/mini/iso.ts:5-7)
  interface ZodMiniISODateTime
  extends: ZodMiniStringFormat

ZodMiniISODuration (packages/zod/src/v4/mini/iso.ts:53-55)
  interface ZodMiniISODuration
  extends: ZodMiniStringFormat

ZodMiniISOTime (packages/zod/src/v4/mini/iso.ts:37-39)
  interface ZodMiniISOTime
  extends: ZodMiniStringFormat

ZodMiniIntersection (packages/zod/src/v4/mini/schemas.ts:1081-1084)
  interface ZodMiniIntersection
  called_by: intersection

ZodMiniJSONSchema (packages/zod/src/v4/mini/schemas.ts:1840-1842)
  interface ZodMiniJSONSchema
  extends: _ZodMiniJSONSchema

ZodMiniJSONSchemaInternals (packages/zod/src/v4/mini/schemas.ts:1836-1839)
  interface ZodMiniJSONSchemaInternals
  extends: _ZodMiniJSONSchemaInternals

ZodMiniJWT (packages/zod/src/v4/mini/schemas.ts:457-459)
  interface ZodMiniJWT
  extends: _ZodMiniString

ZodMiniKSUID (packages/zod/src/v4/mini/schemas.ts:309-311)
  interface ZodMiniKSUID
  extends: _ZodMiniString

ZodMiniLiteral (packages/zod/src/v4/mini/schemas.ts:1293-1296)
  interface ZodMiniLiteral
  called_by: literal

ZodMiniMAC (packages/zod/src/v4/mini/schemas.ts:394-396)
  interface ZodMiniMAC
  extends: _ZodMiniString

ZodMiniMap (packages/zod/src/v4/mini/schemas.ts:1203-1206)
  interface ZodMiniMap

ZodMiniNaN (packages/zod/src/v4/mini/schemas.ts:1557-1559)
  interface ZodMiniNaN
  extends: _ZodMiniType

ZodMiniNanoID (packages/zod/src/v4/mini/schemas.ts:227-229)
  interface ZodMiniNanoID
  extends: _ZodMiniString

ZodMiniNever (packages/zod/src/v4/mini/schemas.ts:732-734)
  interface ZodMiniNever
  extends: _ZodMiniType

ZodMiniNonOptional (packages/zod/src/v4/mini/schemas.ts:1485-1488)
  interface ZodMiniNonOptional

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 80 symbols in L3, 0 with behavior annotations

--- CLUE FILE END ---

QUESTION: How is Zod 4 split across the `zod`, `zod/mini`, and `zod/v4/core` packages?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
