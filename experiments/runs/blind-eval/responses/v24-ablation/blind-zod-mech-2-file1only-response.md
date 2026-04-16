# v2.4 Ablation (File 1 Only): blind-zod-mech-2
Date: 2026-04-16

The clue shows at least three message-customization layers exist.

First, individual checks can accept a custom message-like parameter: both `ZodBigInt.multipleOf` and `ZodNumber.multipleOf` take `message?: errorUtil.ErrMessage` and delegate that through `_addCheck`, using `errorUtil.toString`. [ZodBigInt.multipleOf (packages/zod/src/v3/types.ts:1792-1800); ZodNumber.multipleOf (packages/zod/src/v3/types.ts:1547-1554)]

Second, Zod has error-map machinery: `ZodErrorMap` is a function from `(issue, ctx)` to `{ message: string }`, and v4 check definitions explicitly reference `errors.$ZodErrorMap`. [ZodErrorMap (packages/zod/src/v3/ZodError.ts:329-330); $ZodCheckDef (packages/zod/src/v4/core/checks.ts:8-18)]

Third, `ZodError.format` has an explicit precedence annotation: `PRECEDENCE(issue -> default)`. Combined with its use of `issue.message`, that is the clearest statement in the clue about message selection order: a message already present on the issue wins over the default formatting path. [ZodError.format (packages/zod/src/v3/ZodError.ts:217-264)]

Separately, `ZodError.message` itself just delegates to `JSON.stringify(this.issues)`, so by the time `.message` is read, the selected issue messages have already been fixed elsewhere. [ZodError.message (packages/zod/src/v3/ZodError.ts:280-282)]

What I cannot determine exactly from this clue file is the complete global precedence chain across every customization source (for example, schema-level custom messages vs per-check messages vs per-parse error maps across v3/v4 APIs). The only explicit precedence rule exposed here is `issue -> default` inside `ZodError.format`. [ZodError.format (packages/zod/src/v3/ZodError.ts:217-264); GAPS]
