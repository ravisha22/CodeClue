# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: blind-zod-mech-2

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.

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

ZodIssueOptionalMessage (packages/zod/src/v3/ZodError.ts:152-152)
  type alias ZodIssueOptionalMessage = | ZodInvalidTypeIssue | ZodInvalidLiteralIssue | ZodUnrecognizedKeysIssue | ZodInvalidUnionIssue | ZodInvalidUnionDiscriminatorIssue | ZodInvalidEnumValueIssue | ZodInvalidArgumentsIssue
  uses: ZodInvalidTypeIssue, ZodInvalidLiteralIssue, ZodUnrecognizedKeysIssue, ZodInvalidUnionIssue

ZodIssueOptionalMessage (packages/zod/src/v3/ZodError.ts:151-151)
  type alias ZodIssueOptionalMessage = | ZodInvalidTypeIssue | ZodInvalidLiteralIssue | ZodUnrecognizedKeysIssue | ZodInvalidUnionIssue | ZodInvalidUnionDiscriminatorIssue | ZodInvalidEnumValueIssue
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

$ZodCheckMultipleOfInternals (packages/zod/src/v4/core/checks.ts:157-162)
  interface $ZodCheckMultipleOfInternals
  extends: $ZodCheckInternals
  uses: errors.$ZodIssueNotMultipleOf

$ZodError (packages/zod/src/v4/core/errors.ts:214-217)
  interface $ZodError
  extends: Error
  uses: Symbol.for, zod.error

ZodError.format (packages/zod/src/v3/ZodError.ts:217-264)
  method ZodError.format
  sig: ZodError.format(_mapper?: any)
  behavior: PRECEDENCE(issue -> default); ACCUMULATE(format loop -> result); TRANSFORM(map)
  calls: format
  called_by: ZodError
  uses: issue.message, error.issues, issue.code, issue.unionErrors.map

$ZodCheckMultipleOfParams (packages/zod/src/v4/core/api.ts:923-923)
  type alias $ZodCheckMultipleOfParams = CheckParams<checks.$ZodCheckMultipleOf, "value" | "when">
  uses: CheckParams, checks.$ZodCheckMultipleOf, value, when

$ZodCheckMultipleOfParams (packages/zod/src/v4/core/api.ts:922-922)
  type alias $ZodCheckMultipleOfParams = CheckParams<checks.$ZodCheckMultipleOf, "value" | "when">
  uses: CheckParams, checks.$ZodCheckMultipleOf, value, when

$ZodErrorClass (packages/zod/src/v4/core/parse.ts:6-6)
  type alias $ZodErrorClass = { new (issues: errors.$ZodIssue[]): errors.$ZodError }
  uses: new, issues, errors.$ZodIssue, errors.$ZodError

$ZodErrorClass (packages/zod/src/v4/core/parse.ts:5-5)
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

$ZodFlattenedError (packages/zod/src/v4/core/errors.ts:253-253)
  type alias $ZodFlattenedError = _FlattenedError<T, U>
  uses: _FlattenedError, T, U

$ZodFlattenedError (packages/zod/src/v4/core/errors.ts:252-252)
  type alias $ZodFlattenedError = _FlattenedError<T, U>
  uses: _FlattenedError, T, U

$ZodFlattenedError (packages/zod/src/v4/core/errors.ts:250-250)
  type alias $ZodFlattenedError = _FlattenedError<T, U>
  uses: _FlattenedError, T, U

$ZodFlattenedError (packages/zod/src/v4/core/errors.ts:254-254)
  type alias $ZodFlattenedError = _FlattenedError<T, U>
  uses: _FlattenedError, T, U

$ZodFlattenedError (packages/zod/src/v4/core/errors.ts:251-251)
  type alias $ZodFlattenedError = _FlattenedError<T, U>
  uses: _FlattenedError, T, U

CustomErrorParams (packages/zod/src/v3/types.ts:56-56)
  type alias CustomErrorParams = Partial<util.Omit<ZodCustomIssue, "code">>
  uses: Partial, util.Omit, ZodCustomIssue, code

CustomErrorParams (packages/zod/src/v3/types.ts:55-55)
  type alias CustomErrorParams = Partial<util.Omit<ZodCustomIssue, "code">>
  uses: Partial, util.Omit, ZodCustomIssue, code

_ZodBigInt.multipleOf (packages/zod/src/v4/classic/schemas.ts:949-949)
  method _ZodBigInt.multipleOf
  sig: _ZodBigInt.multipleOf(value: bigint, params?: string | core.$ZodCheckMultipleOf...)
  called_by: _ZodBigInt, _ZodNumber

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 5 with behavior annotations
uncovered: ZodDateCheck, ZodDateCheck, ZodDateCheck, ZodDateCheck
drill: packages/zod/src/v3/ZodError.ts (~2 lines, ZodError.message)
drill: packages/zod/src/v4/core/core.ts (~3 lines, $ZodEncodeError.constructor)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## ZodError.message  (packages/zod/src/v3/ZodError.ts L280-282)
```
  override get message() {
    return JSON.stringify(this.issues, util.jsonStringifyReplacer, 2);
  }
```

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

## DenormalizedError  (packages/zod/src/v3/ZodError.ts L150-150)
```
export type DenormalizedError = { [k: string]: DenormalizedError | string[] };
```

## ErrorMapCtx  (packages/zod/src/v3/ZodError.ts L325-325)
```
export type ErrorMapCtx = {
```

## IssueData  (packages/zod/src/v4/classic/errors.ts L79-79)
```
export type IssueData = core.$ZodRawIssue;
```

## StringValidation  (packages/zod/src/v3/ZodError.ts L88-88)
```
export type StringValidation =
```

## ZodCustomIssue  (packages/zod/src/v3/ZodError.ts L144-148)
```

export interface ZodCustomIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.custom;
  params?: { [k: string]: any };
}
```

## ZodError.assert  (packages/zod/src/v3/ZodError.ts L271-275)
```
  static assert(value: unknown): asserts value is ZodError {
    if (!(value instanceof ZodError)) {
      throw new Error(`Not a ZodError: ${value}`);
    }
  }
```

## ZodError.constructor  (packages/zod/src/v3/ZodError.ts L201-213)
```
  constructor(issues: ZodIssue[]) {
    super();

    const actualProto = new.target.prototype;
    if (Object.setPrototypeOf) {
      // eslint-disable-next-line ban/ban
      Object.setPrototypeOf(this, actualProto);
    } else {
      (this as any).__proto__ = actualProto;
    }
    this.name = "ZodError";
    this.issues = issues;
  }
```

## ZodError.errors  (packages/zod/src/v3/ZodError.ts L197-199)
```
  get errors() {
    return this.issues;
  }
```

## ZodError.flatten  (packages/zod/src/v4/classic/errors.ts L14-14)
```
  flatten(): core.$ZodFlattenedError<T>;
```

## ZodError.formErrors  (packages/zod/src/v3/ZodError.ts L313-315)
```
  get formErrors() {
    return this.flatten();
  }
```

## ZodError.format  (packages/zod/src/v4/classic/errors.ts L11-11)
```
  format(): core.$ZodFormattedError<T>;
```

## ZodError.isEmpty  (packages/zod/src/v3/ZodError.ts L284-286)
```
  get isEmpty(): boolean {
    return this.issues.length === 0;
  }
```

## ZodError.toString  (packages/zod/src/v3/ZodError.ts L277-279)
```
  override toString() {
    return this.message;
  }
```

## ZodError  (packages/zod/src/v4/classic/errors.ts L9-23)
```
export interface ZodError<T = unknown> extends $ZodError<T> {
  /** @deprecated Use the `z.treeifyError(err)` function instead. */
  format(): core.$ZodFormattedError<T>;
  format<U>(mapper: (issue: core.$ZodIssue) => U): core.$ZodFormattedError<T, U>;
  /** @deprecated Use the `z.treeifyError(err)` function instead. */
  flatten(): core.$ZodFlattenedError<T>;
  flatten<U>(mapper: (issue: core.$ZodIssue) => U): core.$ZodFlattenedError<T, U>;
  /** @deprecated Push directly to `.issues` instead. */
  addIssue(issue: core.$ZodIssue): void;
  /** @deprecated Push directly to `.issues` instead. */
  addIssues(issues: core.$ZodIssue[]): void;

  /** @deprecated Check `err.issues.length === 0` instead. */
  isEmpty: boolean;
}
```

## ZodErrorMap  (packages/zod/src/v3/ZodError.ts L330-330)
```
export type ZodErrorMap = (issue: ZodIssueOptionalMessage, _ctx: ErrorMapCtx) => { message: string };
```

## ZodFormattedError  (packages/zod/src/v3/ZodError.ts L188-188)
```
export type ZodFormattedError<T, U = string> = {
```

## ZodInvalidArgumentsIssue  (packages/zod/src/v3/ZodError.ts L73-77)
```

export interface ZodInvalidArgumentsIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.invalid_arguments;
  argumentsError: ZodError;
}
```

## ZodInvalidDateIssue  (packages/zod/src/v3/ZodError.ts L83-86)
```

export interface ZodInvalidDateIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.invalid_date;
}
```

## ZodInvalidEnumValueIssue  (packages/zod/src/v3/ZodError.ts L67-72)
```

export interface ZodInvalidEnumValueIssue extends ZodIssueBase {
  received: string | number;
  code: typeof ZodIssueCode.invalid_enum_value;
  options: (string | number)[];
}
```

## ZodInvalidIntersectionTypesIssue  (packages/zod/src/v3/ZodError.ts L131-134)
```

export interface ZodInvalidIntersectionTypesIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.invalid_intersection_types;
}
```

## ZodInvalidLiteralIssue  (packages/zod/src/v3/ZodError.ts L46-51)
```

export interface ZodInvalidLiteralIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.invalid_literal;
  expected: unknown;
  received: unknown;
}
```

## ZodInvalidReturnTypeIssue  (packages/zod/src/v3/ZodError.ts L78-82)
```

export interface ZodInvalidReturnTypeIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.invalid_return_type;
  returnTypeError: ZodError;
}
```

## ZodInvalidStringIssue  (packages/zod/src/v3/ZodError.ts L110-114)
```

export interface ZodInvalidStringIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.invalid_string;
  validation: StringValidation;
}
```

## ZodInvalidTypeIssue  (packages/zod/src/v3/ZodError.ts L40-45)
```

export interface ZodInvalidTypeIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.invalid_type;
  expected: ZodParsedType;
  received: ZodParsedType;
}
```

## ZodInvalidUnionDiscriminatorIssue  (packages/zod/src/v3/ZodError.ts L62-66)
```

export interface ZodInvalidUnionDiscriminatorIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.invalid_union_discriminator;
  options: Primitive[];
}
```

## ZodInvalidUnionIssue  (packages/zod/src/v3/ZodError.ts L57-61)
```

export interface ZodInvalidUnionIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.invalid_union;
  unionErrors: ZodError[];
}
```

## ZodIssue  (packages/zod/src/v4/classic/errors.ts L6-6)
```
export type ZodIssue = core.$ZodIssue;
```

## ZodIssueBase  (packages/zod/src/v3/ZodError.ts L36-36)
```
export type ZodIssueBase = {
```

## ZodIssueCode  (packages/zod/src/v3/ZodError.ts L34-34)
```
export type ZodIssueCode = keyof typeof ZodIssueCode;
```

## ZodIssueOptionalMessage  (packages/zod/src/v3/ZodError.ts L152-152)
```
export type ZodIssueOptionalMessage =
```

## ZodNotFiniteIssue  (packages/zod/src/v3/ZodError.ts L140-143)
```

export interface ZodNotFiniteIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.not_finite;
}
```

## ZodNotMultipleOfIssue  (packages/zod/src/v3/ZodError.ts L135-139)
```

export interface ZodNotMultipleOfIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.not_multiple_of;
  multipleOf: number | bigint;
}
```

## ZodTooBigIssue  (packages/zod/src/v3/ZodError.ts L123-130)
```

export interface ZodTooBigIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.too_big;
  maximum: number | bigint;
  inclusive: boolean;
  exact?: boolean;
... (truncated)
```
--- END SOURCE SNIPPETS ---

QUESTION: How does Zod decide which error message to emit when multiple customization layers are available?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
