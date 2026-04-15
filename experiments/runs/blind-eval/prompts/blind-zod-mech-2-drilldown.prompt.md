# Blind Evaluation Prompt - MRLF v2.1 with File 2 Drill-Down
# Task: blind-zod-mech-2

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

--- CLUE FILE (File 1) ---
=CC v2.1 zod@HEAD 390mod 1321sym
? How does Zod decide which error message to emit when multiple customization layers are available?


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
ZodError.message (packages/zod/src/v3/ZodError.ts:280-282)
  method ZodError.message
  behavior: DELEGATE(JSON.stringify -> result)
  called_by: ZodError

ZodNotMultipleOfIssue (packages/zod/src/v3/ZodError.ts:136-139)
  interface ZodNotMultipleOfIssue
  extends: ZodIssueBase

ZodError (packages/zod/src/v3/ZodError.ts:194-316)
  extends: Error
  methods: assert, constructor, errors, flatten, formErrors, format
  calls: assert, constructor, errors, flatten, formErrors, format, isEmpty, message

ZodError (packages/zod/src/v4/classic/errors.ts:9-23)
  interface ZodError
  methods: addIssue, addIssues, flatten, format
  calls: addIssue, addIssues, flatten, format

_ZodBigInt.multipleOf (packages/zod/src/v4/classic/schemas.ts:949-949)
  method _ZodBigInt.multipleOf
  sig: _ZodBigInt.multipleOf(value: bigint, params?: string | core.$ZodCheckMultipleOf...)
  called_by: _ZodBigInt, _ZodNumber

_ZodNumber.multipleOf (packages/zod/src/v4/classic/schemas.ts:823-823)
  method _ZodNumber.multipleOf
  sig: _ZodNumber.multipleOf(value: number, params?: string | core.$ZodCheckMultipleOf...)
  called_by: _ZodBigInt, _ZodNumber

ZodBigInt.multipleOf (packages/zod/src/v3/types.ts:1792-1800)
  method ZodBigInt.multipleOf
  sig: ZodBigInt.multipleOf(value: bigint, message?: errorUtil.ErrMessage)
  behavior: DELEGATE(this._addCheck -> result)
  calls: _addCheck, multipleOf
  called_by: ZodBigInt, multipleOf, ZodNumber

ZodNumber.multipleOf (packages/zod/src/v3/types.ts:1547-1554)
  method ZodNumber.multipleOf
  sig: ZodNumber.multipleOf(value: number, message?: errorUtil.ErrMessage)
  behavior: DELEGATE(this._addCheck -> result)
  calls: multipleOf, _addCheck
  called_by: multipleOf, ZodBigInt, ZodNumber

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

ZodError.toString (packages/zod/src/v3/ZodError.ts:277-279)
  method ZodError.toString
  called_by: ZodError

ZodType.setError (packages/zod/src/v3/types.ts:362-362)
  method ZodType.setError
  called_by: ZodType

ZodType.setError (packages/zod/src/v3/types.ts:354-354)
  method ZodType.setError
  called_by: ZodType

ZodCustomIssue (packages/zod/src/v3/ZodError.ts:145-148)
  interface ZodCustomIssue
  extends: ZodIssueBase

ZodInvalidArgumentsIssue (packages/zod/src/v3/ZodError.ts:74-77)
  interface ZodInvalidArgumentsIssue
  extends: ZodIssueBase

ZodInvalidDateIssue (packages/zod/src/v3/ZodError.ts:84-86)
  interface ZodInvalidDateIssue
  extends: ZodIssueBase

ZodInvalidEnumValueIssue (packages/zod/src/v3/ZodError.ts:68-72)
  interface ZodInvalidEnumValueIssue
  extends: ZodIssueBase

ZodInvalidIntersectionTypesIssue (packages/zod/src/v3/ZodError.ts:132-134)
  interface ZodInvalidIntersectionTypesIssue
  extends: ZodIssueBase

ZodInvalidLiteralIssue (packages/zod/src/v3/ZodError.ts:47-51)
  interface ZodInvalidLiteralIssue
  extends: ZodIssueBase

ZodInvalidReturnTypeIssue (packages/zod/src/v3/ZodError.ts:79-82)
  interface ZodInvalidReturnTypeIssue
  extends: ZodIssueBase

ZodInvalidStringIssue (packages/zod/src/v3/ZodError.ts:111-114)
  interface ZodInvalidStringIssue
  extends: ZodIssueBase

ZodInvalidTypeIssue (packages/zod/src/v3/ZodError.ts:41-45)
  interface ZodInvalidTypeIssue
  extends: ZodIssueBase

ZodInvalidUnionDiscriminatorIssue (packages/zod/src/v3/ZodError.ts:63-66)
  interface ZodInvalidUnionDiscriminatorIssue
  extends: ZodIssueBase

ZodInvalidUnionIssue (packages/zod/src/v3/ZodError.ts:58-61)
  interface ZodInvalidUnionIssue
  extends: ZodIssueBase

ZodNotFiniteIssue (packages/zod/src/v3/ZodError.ts:141-143)
  interface ZodNotFiniteIssue
  extends: ZodIssueBase

ZodTooBigIssue (packages/zod/src/v3/ZodError.ts:124-130)
  interface ZodTooBigIssue
  extends: ZodIssueBase

ZodTooSmallIssue (packages/zod/src/v3/ZodError.ts:116-122)
  interface ZodTooSmallIssue
  extends: ZodIssueBase

ZodUnrecognizedKeysIssue (packages/zod/src/v3/ZodError.ts:53-56)
  interface ZodUnrecognizedKeysIssue
  extends: ZodIssueBase

JSONSchemaGenerator.emit (packages/zod/src/v4/core/json-schema-generator.ts:111-125)
  method JSONSchemaGenerator.emit
  sig: JSONSchemaGenerator.emit(schema: schemas.$ZodType, _params?: EmitParams)
  called_by: JSONSchemaGenerator

flattenError (packages/zod/src/v4/core/errors.ts:262-276)
  sig: flattenError(error: $ZodError<T>)
  behavior: ACCUMULATE(loop -> result)

formatError (packages/zod/src/v4/core/errors.ts:290-326)
  sig: formatError(error: $ZodError<T>)
  behavior: ACCUMULATE(loop -> result); TRANSFORM(map)

getErrorMap (packages/zod/src/v4/classic/compat.ts:53-55)
  behavior: DELEGATE(core.config -> result)

getErrorMap (packages/zod/src/v3/errors.ts:11-13)

prettifyError (packages/zod/src/v4/core/errors.ts:435-449)
  sig: prettifyError(error: StandardSchemaV1.FailureResult)
  behavior: DELEGATE(lines.join -> result); ACCUMULATE(loop -> lines)
  calls: toDotPath

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 20 with behavior annotations
drill: packages/zod/src/v3/ZodError.ts (~2 lines, ZodError.message)
drill: packages/zod/src/v4/classic/schemas.ts (~2 lines, _ZodBigInt.multipleOf)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## ZodError.message  (packages/zod/src/v3/ZodError.ts L280-282)
```
  override get message() {
    return JSON.stringify(this.issues, util.jsonStringifyReplacer, 2);
  }
```

## _ZodBigInt.multipleOf  (packages/zod/src/v4/classic/schemas.ts L949-949)
```
  multipleOf(value: bigint, params?: string | core.$ZodCheckMultipleOfParams): this;
```

## ZodCustomIssue  (packages/zod/src/v3/ZodError.ts L145-148)
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

## ZodInvalidArgumentsIssue  (packages/zod/src/v3/ZodError.ts L74-77)
```
export interface ZodInvalidArgumentsIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.invalid_arguments;
  argumentsError: ZodError;
}
```

## ZodInvalidDateIssue  (packages/zod/src/v3/ZodError.ts L84-86)
```
export interface ZodInvalidDateIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.invalid_date;
}
```

## ZodInvalidEnumValueIssue  (packages/zod/src/v3/ZodError.ts L68-72)
```
export interface ZodInvalidEnumValueIssue extends ZodIssueBase {
  received: string | number;
  code: typeof ZodIssueCode.invalid_enum_value;
  options: (string | number)[];
}
```

## ZodInvalidIntersectionTypesIssue  (packages/zod/src/v3/ZodError.ts L132-134)
```
export interface ZodInvalidIntersectionTypesIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.invalid_intersection_types;
}
```

## ZodInvalidLiteralIssue  (packages/zod/src/v3/ZodError.ts L47-51)
```
export interface ZodInvalidLiteralIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.invalid_literal;
  expected: unknown;
  received: unknown;
}
```

## ZodInvalidReturnTypeIssue  (packages/zod/src/v3/ZodError.ts L79-82)
```
export interface ZodInvalidReturnTypeIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.invalid_return_type;
  returnTypeError: ZodError;
}
```

## ZodInvalidStringIssue  (packages/zod/src/v3/ZodError.ts L111-114)
```
export interface ZodInvalidStringIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.invalid_string;
  validation: StringValidation;
}
```

## ZodInvalidTypeIssue  (packages/zod/src/v3/ZodError.ts L41-45)
```
export interface ZodInvalidTypeIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.invalid_type;
  expected: ZodParsedType;
  received: ZodParsedType;
}
```

## ZodInvalidUnionDiscriminatorIssue  (packages/zod/src/v3/ZodError.ts L63-66)
```
export interface ZodInvalidUnionDiscriminatorIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.invalid_union_discriminator;
  options: Primitive[];
}
```

## ZodInvalidUnionIssue  (packages/zod/src/v3/ZodError.ts L58-61)
```
export interface ZodInvalidUnionIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.invalid_union;
  unionErrors: ZodError[];
}
```

## ZodNotFiniteIssue  (packages/zod/src/v3/ZodError.ts L141-143)
```
export interface ZodNotFiniteIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.not_finite;
}
```

## ZodNotMultipleOfIssue  (packages/zod/src/v3/ZodError.ts L136-139)
```
export interface ZodNotMultipleOfIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.not_multiple_of;
  multipleOf: number | bigint;
}
```

## ZodTooBigIssue  (packages/zod/src/v3/ZodError.ts L124-130)
```
export interface ZodTooBigIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.too_big;
  maximum: number | bigint;
  inclusive: boolean;
  exact?: boolean;
  type: "array" | "string" | "number" | "set" | "date" | "bigint";
}
```

## ZodTooSmallIssue  (packages/zod/src/v3/ZodError.ts L116-122)
```
export interface ZodTooSmallIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.too_small;
  minimum: number | bigint;
  inclusive: boolean;
  exact?: boolean;
  type: "array" | "string" | "number" | "set" | "date" | "bigint";
}
```

## ZodUnrecognizedKeysIssue  (packages/zod/src/v3/ZodError.ts L53-56)
```
export interface ZodUnrecognizedKeysIssue extends ZodIssueBase {
  code: typeof ZodIssueCode.unrecognized_keys;
  keys: string[];
}
```

## quotelessJson  (packages/zod/src/v3/ZodError.ts L175-178)
```
export const quotelessJson = (obj: any) => {
  const json = JSON.stringify(obj, null, 2);
  return json.replace(/"([^"]+)":/g, "$1:");
};
```

## ZodAny  (packages/zod/src/v4/classic/schemas.ts L1051-1051)
```
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
--- END SOURCE SNIPPETS ---

QUESTION: How does Zod decide which error message to emit when multiple customization layers are available?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
