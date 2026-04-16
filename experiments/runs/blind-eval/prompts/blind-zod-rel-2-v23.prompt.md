# Blind Evaluation Prompt - MRLF v2.1 with File 2 Drill-Down
# Task: blind-zod-rel-2

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

--- CLUE FILE (File 1) ---
=CC v2.1 zod@HEAD 390mod 2677sym
? How do parsing APIs, schema-level checks, and error maps relate to one another in Zod's validation pipeline?


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
$ZodEncodeError.constructor (packages/zod/src/v4/core/core.ts:105-108)
  method $ZodEncodeError.constructor
  sig: $ZodEncodeError.constructor(name: string)
  calls: constructor
  called_by: constructor, $ZodAsyncError, $ZodEncodeError
  uses: this.name

$ZodAsyncError.constructor (packages/zod/src/v4/core/core.ts:99-101)
  method $ZodAsyncError.constructor
  calls: constructor
  called_by: $ZodAsyncError, constructor, $ZodEncodeError

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

$ZodCheckPropertyParams (packages/zod/src/v4/core/api.ts:1083-1083)
  type alias $ZodCheckPropertyParams = CheckParams<checks.$ZodCheckProperty, "property" | "schema" | "when">
  uses: CheckParams, checks.$ZodCheckProperty, property, schema

$ZodCheckPropertyParams (packages/zod/src/v4/core/api.ts:1082-1082)
  type alias $ZodCheckPropertyParams = CheckParams<checks.$ZodCheckProperty, "property" | "schema" | "when">
  uses: CheckParams, checks.$ZodCheckProperty, property, schema

CheckStringFormatParams (packages/zod/src/v4/core/api.ts:49-49)
  type alias CheckStringFormatParams = never, > = Params<T, NonNullable<T["_zod"]["issc"]>, "type" | "coerce" | "checks" | "error" | "check" | "format" | AlsoOmit>
  uses: never, Params, T, NonNullable

CheckStringFormatParams (packages/zod/src/v4/core/api.ts:50-50)
  type alias CheckStringFormatParams = never, > = Params<T, NonNullable<T["_zod"]["issc"]>, "type" | "coerce" | "checks" | "error" | "check" | "format" | AlsoOmit>
  uses: never, Params, T, NonNullable

ZodError (packages/zod/src/v4/classic/errors.ts:9-23)
  interface ZodError
  extends: $ZodError
  methods: addIssue, addIssues, flatten, format
  calls: addIssue, addIssues, flatten, format
  uses: z.treeifyError, core.$ZodFormattedError, core.$ZodIssue, core.$ZodFlattenedError

ZodPipelineDef (packages/zod/src/v3/types.ts:4764-4777)
  interface ZodPipelineDef
  extends: ZodTypeDef
  uses: ZodFirstPartyTypeKind.ZodPipeline

$ZodError (packages/zod/src/v4/core/errors.ts:214-217)
  interface $ZodError
  extends: Error
  uses: Symbol.for, zod.error

$ZodErrorClass (packages/zod/src/v4/core/parse.ts:5-5)
  type alias $ZodErrorClass = { new (issues: errors.$ZodIssue[]): errors.$ZodError }
  uses: new, issues, errors.$ZodIssue, errors.$ZodError

$ZodErrorClass (packages/zod/src/v4/core/parse.ts:6-6)
  type alias $ZodErrorClass = { new (issues: errors.$ZodIssue[]): errors.$ZodError }
  uses: new, issues, errors.$ZodIssue, errors.$ZodError

ZodErrorMap (packages/zod/src/v3/ZodError.ts:329-329)
  type alias ZodErrorMap = (issue: ZodIssueOptionalMessage, _ctx: ErrorMapCtx) => { message: string }
  uses: issue, ZodIssueOptionalMessage, _ctx, ErrorMapCtx

ZodErrorMap (packages/zod/src/v3/ZodError.ts:330-330)
  type alias ZodErrorMap = (issue: ZodIssueOptionalMessage, _ctx: ErrorMapCtx) => { message: string }
  uses: issue, ZodIssueOptionalMessage, _ctx, ErrorMapCtx

ZodSafeParseError (packages/zod/src/v4/classic/parse.ts:6-6)
  type alias ZodSafeParseError = { success: false; data?: never; error: ZodError<T> }
  uses: success, false, data, never

ZodError (packages/zod/src/v3/ZodError.ts:193-316)
  extends: Error
  methods: assert, constructor, errors, flatten, formErrors, format
  calls: assert, constructor, errors, flatten, formErrors, format, isEmpty, message
  uses: this.issues, new.target.prototype, Object.setPrototypeOf, this.name

ZodError.format (packages/zod/src/v3/ZodError.ts:217-264)
  method ZodError.format
  sig: ZodError.format(_mapper?: any)
  behavior: PRECEDENCE(issue -> default); ACCUMULATE(format loop -> result); TRANSFORM(map)
  calls: format
  called_by: ZodError
  uses: issue.message, error.issues, issue.code, issue.unionErrors.map

$ZodChecks (packages/zod/src/v4/core/checks.ts:1266-1266)
  type alias $ZodChecks = | $ZodCheckLessThan | $ZodCheckGreaterThan | $ZodCheckMultipleOf | $ZodCheckNumberFormat
  uses: $ZodCheckLessThan, $ZodCheckGreaterThan, $ZodCheckMultipleOf, $ZodCheckNumberFormat

$ZodChecks (packages/zod/src/v4/core/checks.ts:1267-1267)
  type alias $ZodChecks = | $ZodCheckLessThan | $ZodCheckGreaterThan | $ZodCheckMultipleOf | $ZodCheckNumberFormat | $ZodCheckBigIntFormat
  uses: $ZodCheckLessThan, $ZodCheckGreaterThan, $ZodCheckMultipleOf, $ZodCheckNumberFormat

$ZodChecks (packages/zod/src/v4/core/checks.ts:1268-1268)
  type alias $ZodChecks = | $ZodCheckLessThan | $ZodCheckGreaterThan | $ZodCheckMultipleOf | $ZodCheckNumberFormat | $ZodCheckBigIntFormat | $ZodCheckMaxSize
  uses: $ZodCheckLessThan, $ZodCheckGreaterThan, $ZodCheckMultipleOf, $ZodCheckNumberFormat

$ZodChecks (packages/zod/src/v4/core/checks.ts:1265-1265)
  type alias $ZodChecks = | $ZodCheckLessThan | $ZodCheckGreaterThan | $ZodCheckMultipleOf
  uses: $ZodCheckLessThan, $ZodCheckGreaterThan, $ZodCheckMultipleOf

$ZodChecks (packages/zod/src/v4/core/checks.ts:1269-1269)
  type alias $ZodChecks = | $ZodCheckLessThan | $ZodCheckGreaterThan | $ZodCheckMultipleOf | $ZodCheckNumberFormat | $ZodCheckBigIntFormat | $ZodCheckMaxSize | $ZodCheckMinSize
  uses: $ZodCheckLessThan, $ZodCheckGreaterThan, $ZodCheckMultipleOf, $ZodCheckNumberFormat

$ZodChecks (packages/zod/src/v4/core/checks.ts:1263-1263)
  type alias $ZodChecks = | $ZodCheckLessThan
  uses: $ZodCheckLessThan

$ZodChecks (packages/zod/src/v4/core/checks.ts:1264-1264)
  type alias $ZodChecks = | $ZodCheckLessThan | $ZodCheckGreaterThan
  uses: $ZodCheckLessThan, $ZodCheckGreaterThan

$ZodFlattenedError (packages/zod/src/v4/core/errors.ts:250-250)
  type alias $ZodFlattenedError = _FlattenedError<T, U>
  uses: _FlattenedError, T, U

$ZodFlattenedError (packages/zod/src/v4/core/errors.ts:254-254)
  type alias $ZodFlattenedError = _FlattenedError<T, U>
  uses: _FlattenedError, T, U

$ZodFlattenedError (packages/zod/src/v4/core/errors.ts:251-251)
  type alias $ZodFlattenedError = _FlattenedError<T, U>
  uses: _FlattenedError, T, U

$ZodFlattenedError (packages/zod/src/v4/core/errors.ts:252-252)
  type alias $ZodFlattenedError = _FlattenedError<T, U>
  uses: _FlattenedError, T, U

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 5 with behavior annotations
uncovered: $ZodCheckBigIntFormatParams, $ZodCheckEndsWithParams, $ZodCheckEndsWithParams, $ZodCheckGreaterThanParams
drill: packages/zod/src/v4/core/core.ts (~3 lines, $ZodEncodeError.constructor)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## $ZodEncodeError.constructor  (packages/zod/src/v4/core/core.ts L105-108)
```
  constructor(name: string) {
    super(`Encountered unidirectional transform during encode: ${name}`);
    this.name = "ZodEncodeError";
  }
```

## $ZodAsyncError.constructor  (packages/zod/src/v4/core/core.ts L99-101)
```
  constructor() {
    super(`Encountered Promise during synchronous parse. Use .parseAsync() instead.`);
  }
```

## $ZodAsyncError  (packages/zod/src/v4/core/core.ts L97-102)
```

export class $ZodAsyncError extends Error {
  constructor() {
    super(`Encountered Promise during synchronous parse. Use .parseAsync() instead.`);
  }
}
```

## $ZodBranded  (packages/zod/src/v4/core/core.ts L85-85)
```
export type $ZodBranded<
```

## $ZodConfig  (packages/zod/src/v4/core/core.ts L121-131)
```

//////////////////////////////   CONFIG   ///////////////////////////////////////

export interface $ZodConfig {
  /** Custom error map. Overrides `config().localeError`. */
  customError?: errors.$ZodErrorMap | undefined;
  /** Localized error map. Lowest priority. */
  localeError?: errors.$ZodErrorMap | undefined;
  /** Disable JIT schema compilation. Useful in environments that disallow `eval`. */
  jitless?: boolean | undefined;
}
```

## $ZodEncodeError  (packages/zod/src/v4/core/core.ts L103-109)
```

export class $ZodEncodeError extends Error {
  constructor(name: string) {
    super(`Encountered unidirectional transform during encode: ${name}`);
    this.name = "ZodEncodeError";
  }
}
```

## $ZodNarrow  (packages/zod/src/v4/core/core.ts L96-96)
```
export type $ZodNarrow<T extends schemas.SomeType, Out> = T & { _zod: { output: Out } };
```

## $brand  (packages/zod/src/v4/core/core.ts L81-81)
```
export type $brand<T extends string | number | symbol = string | number | symbol> = {
```

## $constructor.init  (packages/zod/src/v4/core/core.ts L9-9)
```
  init(inst: T, def: D): asserts inst is T;
```

## $constructor.new  (packages/zod/src/v4/core/core.ts L8-8)
```
  new (def: D): T;
```

## $constructor  (packages/zod/src/v4/core/core.ts L7-10)
```
export interface $constructor<T extends ZodTrait, D = T["_zod"]["def"]> {
  new (def: D): T;
  init(inst: T, def: D): asserts inst is T;
}
```

## Definition  (packages/zod/src/v4/core/core.ts L55-55)
```
  class Definition extends Parent {}
```

## _  (packages/zod/src/v4/core/core.ts L57-66)
```

  function _(this: any, def: D) {
    const inst = params?.Parent ? new Definition() : this;
    init(inst, def);
    inst._zod.deferred ??= [];
    for (const fn of inst._zod.deferred) {
      fn();
    }
    return inst;
  }
```

## config  (packages/zod/src/v4/core/core.ts L134-138)
```

export function config(newConfig?: Partial<$ZodConfig>): $ZodConfig {
  if (newConfig) Object.assign(globalConfig, newConfig);
  return globalConfig;
}
```

## init  (packages/zod/src/v4/core/core.ts L22-51)
```
  function init(inst: T, def: D) {
    if (!inst._zod) {
      Object.defineProperty(inst, "_zod", {
        value: {
          def,
          constr: _,
          traits: new Set(),
        },
        enumerable: false,
      });
    }

    if (inst._zod.traits.has(name)) {
      return;
    }

    inst._zod.traits.add(name);

    initializer(inst, def);

    // support prototype modifications
    const proto = _.prototype;
    const keys = Object.keys(proto);
    for (let i = 0; i < keys.length; i++) {
      const k = keys[i]!;
      if (!(k in inst)) {
        (inst as any)[k] = proto[k].bind(inst);
      }
    }
  }
```

## input  (packages/zod/src/v4/core/core.ts L117-117)
```
export type input<T> = T extends { _zod: { input: any } } ? T["_zod"]["input"] : unknown;
```

## output  (packages/zod/src/v4/core/core.ts L118-118)
```
export type output<T> = T extends { _zod: { output: any } } ? T["_zod"]["output"] : unknown;
```
--- END SOURCE SNIPPETS ---

QUESTION: How do parsing APIs, schema-level checks, and error maps relate to one another in Zod's validation pipeline?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
