# Blind Evaluation Prompt - MRLF v2.3 (File 1 Only — No Drill-Down)
# Task: blind-zod-struct-2

You are a senior software engineer. You have been given a codebase
comprehension artifact (a 'clue file') that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

--- CLUE FILE START ---
=CC v2.1 zod@HEAD 390mod 2677sym
? How are schema types, checks, and errors organized in Zod's documented internal architecture?


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
ZodType.constructor                 M packages/zod/src/v3/types.ts:411    method ZodType.constructor
Class.constructor                   M packages/zod/src/v3/types.ts:5036   method Class.constructor
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
ZodFunction._parse                  M packages/zod/src/v3/types.ts:3822   method ZodFunction._parse
ZodArray._parse                     M packages/zod/src/v3/types.ts:2241   method ZodArray._parse
ZodDate._parse                      M packages/zod/src/v3/types.ts:1878   method ZodDate._parse
ZodPipeline._parse                  M packages/zod/src/v3/types.ts:4782   method ZodPipeline._parse
ZodUnion._parse                     M packages/zod/src/v3/types.ts:2947   method ZodUnion._parse
ZodEnum._parse                      M packages/zod/src/v3/types.ts:4082   method ZodEnum._parse
ZodNaN._parse                       M packages/zod/src/v3/types.ts:4702   method ZodNaN._parse
ZodSymbol._parse                    M packages/zod/src/v3/types.ts:2010   method ZodSymbol._parse
ZodBoolean._parse                   M packages/zod/src/v3/types.ts:1834   method ZodBoolean._parse
ZodNull._parse                      M packages/zod/src/v3/types.ts:2080   method ZodNull._parse
ZodPromise._parse                   M packages/zod/src/v3/types.ts:4244   method ZodPromise._parse
ZodUndefined._parse                 M packages/zod/src/v3/types.ts:2045   method ZodUndefined._parse
ZodVoid._parse                      M packages/zod/src/v3/types.ts:2193   method ZodVoid._parse
ZodLiteral._parse                   M packages/zod/src/v3/types.ts:4007   method ZodLiteral._parse
ZodNativeEnum._parse                M packages/zod/src/v3/types.ts:4179   method ZodNativeEnum._parse
ZodNever._parse                     M packages/zod/src/v3/types.ts:2164   method ZodNever._parse
ZodRecord._parse                    M packages/zod/src/v3/types.ts:3514   method ZodRecord._parse
ZodMap._parse                       M packages/zod/src/v3/types.ts:3603   method ZodMap._parse
ZodSet._parse                       M packages/zod/src/v3/types.ts:3691   method ZodSet._parse
ZodTuple._parse                     M packages/zod/src/v3/types.ts:3399   method ZodTuple._parse
ZodDefault._parse                   M packages/zod/src/v3/types.ts:4569   method ZodDefault._parse
ZodBranded._parse                   M packages/zod/src/v3/types.ts:4748   method ZodBranded._parse
ZodCatch._parse                     M packages/zod/src/v3/types.ts:4619   method ZodCatch._parse
ZodLazy._parse                      M packages/zod/src/v3/types.ts:3979   method ZodLazy._parse
ZodNullable._parse                  M packages/zod/src/v3/types.ts:4530   method ZodNullable._parse
ZodOptional._parse                  M packages/zod/src/v3/types.ts:4490   method ZodOptional._parse
ZodUnknown._parse                   M packages/zod/src/v3/types.ts:2140   method ZodUnknown._parse
ZodAny._parse                       M packages/zod/src/v3/types.ts:2115   method ZodAny._parse
ZodReadonly._parse                  M packages/zod/src/v3/types.ts:4877   method ZodReadonly._parse
ZodBranded.unwrap                   M packages/zod/src/v3/types.ts:4758   method ZodBranded.unwrap
ZodNullable.unwrap                  M packages/zod/src/v3/types.ts:4538   method ZodNullable.unwrap
ZodOptional.unwrap                  M packages/zod/src/v3/types.ts:4498   method ZodOptional.unwrap
ZodReadonly.unwrap                  M packages/zod/src/v3/types.ts:4896   method ZodReadonly.unwrap
ZodPromise.unwrap                   M packages/zod/src/v3/types.ts:4240   method ZodPromise.unwrap
ZodBigInt.maxValue                  M packages/zod/src/v3/types.ts:1810   method ZodBigInt.maxValue
ZodBigInt.minValue                  M packages/zod/src/v3/types.ts:1800   method ZodBigInt.minValue
ZodNumber.maxValue                  M packages/zod/src/v3/types.ts:1587   method ZodNumber.maxValue
  ...and 2442 more symbols

-- FOCUS
ZodFirstPartySchemaTypes (packages/zod/src/v3/types.ts:4996-4997)
  type alias ZodFirstPartySchemaTypes = | ZodString | ZodNumber | ZodNaN | ZodBigInt | ZodBoolean | ZodDate | ZodUndefined
  uses: ZodString, ZodNumber, ZodNaN, ZodBigInt

$ZodStringFormatChecks (packages/zod/src/v4/core/checks.ts:1286-1286)
  type alias $ZodStringFormatChecks = | $ZodCheckRegex | $ZodCheckLowerCase | $ZodCheckUpperCase | $ZodCheckIncludes | $ZodCheckStartsWith | $ZodCheckEndsWith | schemas.$ZodStringFormatTypes
  uses: $ZodCheckRegex, $ZodCheckLowerCase, $ZodCheckUpperCase, $ZodCheckIncludes

$Decode (packages/zod/src/v4/core/parse.ts:110-110)
  type alias $Decode = <T extends schemas.$ZodType>( schema: T, value: core.input<T>, _ctx?: schemas.ParseContext<errors.$ZodIssue> ) => core.output<T>
  uses: T, schemas.$ZodType, schema, value

$Decode (packages/zod/src/v4/core/parse.ts:109-109)
  type alias $Decode = <T extends schemas.$ZodType>( schema: T, value: core.input<T>, _ctx?: schemas.ParseContext<errors.$ZodIssue> ) => core.output<T>
  uses: T, schemas.$ZodType, schema, value

$DecodeAsync (packages/zod/src/v4/core/parse.ts:135-135)
  type alias $DecodeAsync = <T extends schemas.$ZodType>( schema: T, value: core.input<T>, _ctx?: schemas.ParseContext<errors.$ZodIssue> ) => Promise<core.output<T>>
  uses: T, schemas.$ZodType, schema, value

$DecodeAsync (packages/zod/src/v4/core/parse.ts:134-134)
  type alias $DecodeAsync = <T extends schemas.$ZodType>( schema: T, value: core.input<T>, _ctx?: schemas.ParseContext<errors.$ZodIssue> ) => Promise<core.output<T>>
  uses: T, schemas.$ZodType, schema, value

$Encode (packages/zod/src/v4/core/parse.ts:95-95)
  type alias $Encode = <T extends schemas.$ZodType>( schema: T, value: core.output<T>, _ctx?: schemas.ParseContext<errors.$ZodIssue> ) => core.input<T>
  uses: T, schemas.$ZodType, schema, value

$Encode (packages/zod/src/v4/core/parse.ts:96-96)
  type alias $Encode = <T extends schemas.$ZodType>( schema: T, value: core.output<T>, _ctx?: schemas.ParseContext<errors.$ZodIssue> ) => core.input<T>
  uses: T, schemas.$ZodType, schema, value

$Encode (packages/zod/src/v4/core/parse.ts:97-97)
  type alias $Encode = <T extends schemas.$ZodType>( schema: T, value: core.output<T>, _ctx?: schemas.ParseContext<errors.$ZodIssue> ) => core.input<T>
  uses: T, schemas.$ZodType, schema, value

$EncodeAsync (packages/zod/src/v4/core/parse.ts:121-121)
  type alias $EncodeAsync = <T extends schemas.$ZodType>( schema: T, value: core.output<T>, _ctx?: schemas.ParseContext<errors.$ZodIssue> ) => Promise<core.input<T>>
  uses: T, schemas.$ZodType, schema, value

$EncodeAsync (packages/zod/src/v4/core/parse.ts:122-122)
  type alias $EncodeAsync = <T extends schemas.$ZodType>( schema: T, value: core.output<T>, _ctx?: schemas.ParseContext<errors.$ZodIssue> ) => Promise<core.input<T>>
  uses: T, schemas.$ZodType, schema, value

$Parse (packages/zod/src/v4/core/parse.ts:7-7)
  type alias $Parse = <T extends schemas.$ZodType>( schema: T, value: unknown, _ctx?: schemas.ParseContext<errors.$ZodIssue>, _params?: { callee?: util.AnyFunc; Err?: $ZodErrorClass }
  uses: T, schemas.$ZodType, schema, value

$Parse (packages/zod/src/v4/core/parse.ts:8-8)
  type alias $Parse = <T extends schemas.$ZodType>( schema: T, value: unknown, _ctx?: schemas.ParseContext<errors.$ZodIssue>, _params?: { callee?: util.AnyFunc; Err?: $ZodErrorClass }
  uses: T, schemas.$ZodType, schema, value

$Parse (packages/zod/src/v4/core/parse.ts:9-9)
  type alias $Parse = <T extends schemas.$ZodType>( schema: T, value: unknown, _ctx?: schemas.ParseContext<errors.$ZodIssue>, _params?: { callee?: util.AnyFunc; Err?: $ZodErrorClass }
  uses: T, schemas.$ZodType, schema, value

$ParseAsync (packages/zod/src/v4/core/parse.ts:32-32)
  type alias $ParseAsync = <T extends schemas.$ZodType>( schema: T, value: unknown, _ctx?: schemas.ParseContext<errors.$ZodIssue>, _params?: { callee?: util.AnyFunc; Err?: $ZodErrorClass }
  uses: T, schemas.$ZodType, schema, value

$ParseAsync (packages/zod/src/v4/core/parse.ts:31-31)
  type alias $ParseAsync = <T extends schemas.$ZodType>( schema: T, value: unknown, _ctx?: schemas.ParseContext<errors.$ZodIssue>, _params?: { callee?: util.AnyFunc; Err?: $ZodErrorClass }
  uses: T, schemas.$ZodType, schema, value

$SafeDecode (packages/zod/src/v4/core/parse.ts:160-160)
  type alias $SafeDecode = <T extends schemas.$ZodType>( schema: T, value: core.input<T>, _ctx?: schemas.ParseContext<errors.$ZodIssue> ) => util.SafeParseResult<core.output<T>>
  uses: T, schemas.$ZodType, schema, value

$SafeDecode (packages/zod/src/v4/core/parse.ts:159-159)
  type alias $SafeDecode = <T extends schemas.$ZodType>( schema: T, value: core.input<T>, _ctx?: schemas.ParseContext<errors.$ZodIssue> ) => util.SafeParseResult<core.output<T>>
  uses: T, schemas.$ZodType, schema, value

$SafeDecodeAsync (packages/zod/src/v4/core/parse.ts:185-185)
  type alias $SafeDecodeAsync = <T extends schemas.$ZodType>( schema: T, value: core.input<T>, _ctx?: schemas.ParseContext<errors.$ZodIssue> ) => Promise<util.SafeParseResult<core.output<T>>>
  uses: T, schemas.$ZodType, schema, value

$SafeDecodeAsync (packages/zod/src/v4/core/parse.ts:184-184)
  type alias $SafeDecodeAsync = <T extends schemas.$ZodType>( schema: T, value: core.input<T>, _ctx?: schemas.ParseContext<errors.$ZodIssue> ) => Promise<util.SafeParseResult<core.output<T>>>
  uses: T, schemas.$ZodType, schema, value

$SafeEncode (packages/zod/src/v4/core/parse.ts:147-147)
  type alias $SafeEncode = <T extends schemas.$ZodType>( schema: T, value: core.output<T>, _ctx?: schemas.ParseContext<errors.$ZodIssue> ) => util.SafeParseResult<core.input<T>>
  uses: T, schemas.$ZodType, schema, value

$SafeEncode (packages/zod/src/v4/core/parse.ts:146-146)
  type alias $SafeEncode = <T extends schemas.$ZodType>( schema: T, value: core.output<T>, _ctx?: schemas.ParseContext<errors.$ZodIssue> ) => util.SafeParseResult<core.input<T>>
  uses: T, schemas.$ZodType, schema, value

$SafeEncodeAsync (packages/zod/src/v4/core/parse.ts:171-171)
  type alias $SafeEncodeAsync = <T extends schemas.$ZodType>( schema: T, value: core.output<T>, _ctx?: schemas.ParseContext<errors.$ZodIssue> ) => Promise<util.SafeParseResult<core.input<T>>>
  uses: T, schemas.$ZodType, schema, value

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 80 symbols in L3, 2 with behavior annotations

--- CLUE FILE END ---

QUESTION: How are schema types, checks, and errors organized in Zod's documented internal architecture?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry that supports it.
