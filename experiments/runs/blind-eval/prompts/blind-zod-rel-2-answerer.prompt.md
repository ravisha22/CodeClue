# Blind Evaluation Prompt - MRLF v2.1
# Task: blind-zod-rel-2

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

--- CLUE FILE START ---
=CC v2.1 zod@HEAD 390mod 1321sym
? How do parsing APIs, schema-level checks, and error maps relate to one another in Zod's validation pipeline?


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
ZodPipeline._parse (packages/zod/src/v3/types.ts:4782-4827)
  method ZodPipeline._parse
  sig: ZodPipeline._parse(input: ParseInput)
  behavior: PRECEDENCE(ctx -> inResult -> default)
  calls: _parse, _parseAsync, _parseSync, _processInputParams
  called_by: _parse, ZodAny, ZodArray, ZodBigInt, ZodBoolean, ZodBranded, ZodCatch, ZodDate

ZodError (packages/zod/src/v3/ZodError.ts:194-316)
  extends: Error
  methods: assert, constructor, errors, flatten, formErrors, format
  calls: assert, constructor, errors, flatten, formErrors, format, isEmpty, message

ZodPipeline (packages/zod/src/v3/types.ts:4777-4839)
  extends: ZodType
  calls: _parse, _parseAsync, _parseSync, _processInputParams
  called_by: ZodDiscriminatedUnion, ZodObject

ZodError (packages/zod/src/v4/classic/errors.ts:9-23)
  interface ZodError
  methods: addIssue, addIssues, flatten, format
  calls: addIssue, addIssues, flatten, format

ZodMap.keySchema (packages/zod/src/v3/types.ts:3597-3600)
  method ZodMap.keySchema
  calls: keySchema
  called_by: ZodDiscriminatedUnion, ZodMap, ZodObject, keySchema, ZodRecord

ZodMap.valueSchema (packages/zod/src/v3/types.ts:3600-3603)
  method ZodMap.valueSchema
  calls: valueSchema
  called_by: ZodDiscriminatedUnion, ZodMap, ZodObject, valueSchema, ZodRecord

ZodRecord.keySchema (packages/zod/src/v3/types.ts:3508-3511)
  method ZodRecord.keySchema
  calls: keySchema
  called_by: ZodDiscriminatedUnion, keySchema, ZodMap, ZodObject, ZodRecord

ZodRecord.valueSchema (packages/zod/src/v3/types.ts:3511-3514)
  method ZodRecord.valueSchema
  calls: valueSchema
  called_by: ZodDiscriminatedUnion, valueSchema, ZodMap, ZodObject, ZodRecord

ZodLazy.schema (packages/zod/src/v3/types.ts:3975-3979)
  method ZodLazy.schema
  behavior: DELEGATE(this._def.getter -> result)
  called_by: ZodDiscriminatedUnion, ZodLazy, ZodObject

ZodPipelineDef (packages/zod/src/v3/types.ts:4771-4777)
  interface ZodPipelineDef
  extends: ZodTypeDef

ZodError.addIssue (packages/zod/src/v4/classic/errors.ts:17-17)
  method ZodError.addIssue
  sig: ZodError.addIssue(issue: core.$ZodIssue)
  called_by: ZodError

ZodError.addIssues (packages/zod/src/v4/classic/errors.ts:19-19)
  method ZodError.addIssues
  sig: ZodError.addIssues(issues: core.$ZodIssue[])
  called_by: ZodError

ZodError.assert (packages/zod/src/v3/ZodError.ts:271-275)
  method ZodError.assert
  sig: ZodError.assert(value: unknown)
  called_by: ZodError

ZodError.constructor (packages/zod/src/v3/ZodError.ts:201-213)
  method ZodError.constructor
  sig: ZodError.constructor(issues: ZodIssue[])
  called_by: ZodError

ZodError.errors (packages/zod/src/v3/ZodError.ts:197-199)
  method ZodError.errors
  called_by: ZodError

ZodError.flatten (packages/zod/src/v4/classic/errors.ts:14-14)
  method ZodError.flatten
  called_by: ZodError

ZodError.flatten (packages/zod/src/v3/ZodError.ts:296-296)
  method ZodError.flatten
  called_by: formErrors, ZodError

ZodError.formErrors (packages/zod/src/v3/ZodError.ts:313-315)
  method ZodError.formErrors
  behavior: DELEGATE(this.flatten -> result)
  calls: flatten
  called_by: ZodError

ZodError.format (packages/zod/src/v3/ZodError.ts:215-215)
  method ZodError.format
  called_by: format, ZodError

ZodError.format (packages/zod/src/v3/ZodError.ts:217-264)
  method ZodError.format
  sig: ZodError.format(_mapper?: any)
  behavior: PRECEDENCE(issue -> default); ACCUMULATE(loop -> result); TRANSFORM(map)
  calls: format
  called_by: ZodError

ZodError.format (packages/zod/src/v4/classic/errors.ts:11-11)
  method ZodError.format
  called_by: ZodError

ZodError.isEmpty (packages/zod/src/v3/ZodError.ts:284-286)
  method ZodError.isEmpty
  called_by: ZodError

ZodError.message (packages/zod/src/v3/ZodError.ts:280-282)
  method ZodError.message
  behavior: DELEGATE(JSON.stringify -> result)
  called_by: ZodError

ZodError.toString (packages/zod/src/v3/ZodError.ts:277-279)
  method ZodError.toString
  called_by: ZodError

ZodType.setError (packages/zod/src/v3/types.ts:362-362)
  method ZodType.setError
  called_by: ZodType

ZodType.setError (packages/zod/src/v3/types.ts:354-354)
  method ZodType.setError
  called_by: ZodType

convertSchema (packages/zod/src/v4/classic/from-json-schema.ts:541-620)
  sig: convertSchema(schema: JSONSchema.JSONSchema | boolean, ctx: ConversionC...)
  behavior: GUARD(typeof -> schema); PRECEDENCE(typeof -> schema -> default); ACCUMULATE(loop -> result)
  calls: convertBaseSchema
  called_by: convertBaseSchema, fromJSONSchema

convertBaseSchema (packages/zod/src/v4/classic/from-json-schema.ts:146-539)
  sig: convertBaseSchema(schema: JSONSchema.JSONSchema, ctx: ConversionContext)
  behavior: GUARD(ctx -> pass_through); DISPATCH(type); PRECEDENCE(schema -> default)
  calls: convertSchema, resolveRef
  called_by: convertSchema

ZodType.pipe (packages/zod/src/v3/types.ts:522-524)
  method ZodType.pipe
  sig: ZodType.pipe(target: T)
  behavior: DELEGATE(ZodPipeline.create -> result)
  calls: create

ArraySchema (packages/zod/src/v4/core/json-schema.ts:125-127)
  interface ArraySchema
  extends: JSONSchema

BooleanSchema (packages/zod/src/v4/core/json-schema.ts:141-143)
  interface BooleanSchema
  extends: JSONSchema

IntegerSchema (packages/zod/src/v4/core/json-schema.ts:137-139)
  interface IntegerSchema
  extends: JSONSchema

NullSchema (packages/zod/src/v4/core/json-schema.ts:145-147)
  interface NullSchema
  extends: JSONSchema

NumberSchema (packages/zod/src/v4/core/json-schema.ts:133-135)
  interface NumberSchema
  extends: JSONSchema

ObjectSchema (packages/zod/src/v4/core/json-schema.ts:121-123)
  interface ObjectSchema
  extends: JSONSchema

SchemaPart (packages/zod/src/v4/core/schemas.ts:4069-4071)
  interface SchemaPart

SchemaPartInternals (packages/zod/src/v4/core/schemas.ts:4066-4068)
  interface SchemaPartInternals

StandardSchemaV1 (packages/zod/src/v4/core/standard-schema.ts:34-37)
  interface StandardSchemaV1

StandardSchemaWithJSON (packages/zod/src/v4/core/standard-schema.ts:157-159)
  interface StandardSchemaWithJSON

StandardSchemaWithJSONProps (packages/zod/src/v4/core/standard-schema.ts:150-152)
  interface StandardSchemaWithJSONProps

StringSchema (packages/zod/src/v4/core/json-schema.ts:129-131)
  interface StringSchema
  extends: JSONSchema

ZodCustomIssue (packages/zod/src/v3/ZodError.ts:145-148)
  interface ZodCustomIssue
  extends: ZodIssueBase

ZodInvalidArgumentsIssue (packages/zod/src/v3/ZodError.ts:74-77)
  interface ZodInvalidArgumentsIssue
  extends: ZodIssueBase

ZodInvalidDateIssue (packages/zod/src/v3/ZodError.ts:84-86)
  interface ZodInvalidDateIssue
  extends: ZodIssueBase

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 80 symbols in L3, 25 with behavior annotations

--- CLUE FILE END ---

QUESTION: How do parsing APIs, schema-level checks, and error maps relate to one another in Zod's validation pipeline?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
