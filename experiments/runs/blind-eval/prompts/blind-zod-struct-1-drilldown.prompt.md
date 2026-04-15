# Blind Evaluation Prompt - MRLF v2.1 with File 2 Drill-Down
# Task: blind-zod-struct-1

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

--- CLUE FILE (File 1) ---
=CC v2.1 zod@HEAD 390mod 686sym
? How is Zod 4 split across the `zod`, `zod/mini`, and `zod/v4/core` packages?


-- TREE
packages/  (384 files)
  bench/  docs/  resolution/  treeshake/  tsc/  zod/
scripts/  (4 files)
play.ts  vitest.config.ts

-- INDEX
packages/bench/array.ts                          20L  
packages/bench/benchUtil.ts                      69L  formatNumber, makeData, randomPick, randomString, toFixed
packages/bench/boolean.ts                        16L  
packages/bench/datetime-regex.ts                 52L  
packages/bench/datetime.ts                       16L  
packages/bench/discriminated-union.ts           159L  makeSchema
packages/bench/error-handling.ts                 33L  
packages/bench/index.ts                          20L  run
packages/bench/init.ts                           89L  
packages/bench/instanceof.ts                     69L  ZodFailure, falsyThenCheckSymbol, falsyThenCheckTag, instanceofClass, instanceofObjectThenCheckSymbol
packages/bench/ipv4-regex.ts                     46L  
packages/bench/jit-union.ts                      79L  
packages/bench/key-iteration.ts                  50L  
packages/bench/lazy-box.ts                       59L  
packages/bench/libs.ts                           57L  
packages/bench/metabench.ts                     227L  BenchmarkJS, Metabench, Mitata, Tinybench
packages/bench/number.ts                         16L  
packages/bench/object-async.ts                   13L  
packages/bench/object-creation.ts                18L  ZodFail
packages/bench/object-fail.ts                    13L  
packages/bench/object-moltar-jitless.ts          89L  
packages/bench/object-moltar.ts                  81L  
packages/bench/object-safe.ts                    13L  
packages/bench/object-safeasync.ts               13L  
packages/bench/object-setup.ts                   35L  
packages/bench/object.ts                         48L  
packages/bench/property-access.ts                84L  
  ...and 363 more modules

-- SYM
formatNumber                        M packages/bench/benchUtil.ts:36     function formatNumber
makeData                            M packages/bench/benchUtil.ts:27     function makeData
randomPick                          M packages/bench/benchUtil.ts:23     function randomPick
randomString                        M packages/bench/benchUtil.ts:14     function randomString
toFixed                             M packages/bench/benchUtil.ts:67     function toFixed
makeSchema                          M packages/bench/discriminated-union.ts:53     function makeSchema
run                                 M packages/bench/index.ts:5      function run
ZodFailure                          C packages/bench/instanceof.ts:6      class ZodFailure
falsyThenCheckSymbol                M packages/bench/instanceof.ts:30     function falsyThenCheckSymbol
falsyThenCheckTag                   M packages/bench/instanceof.ts:29     function falsyThenCheckTag
instanceofClass                     M packages/bench/instanceof.ts:21     function instanceofClass
instanceofObjectThenCheckSymbol     M packages/bench/instanceof.ts:27     function instanceofObjectThenCheckSymbol
instanceofObjectThenCheckTag        M packages/bench/instanceof.ts:28     function instanceofObjectThenCheckTag
instanceofPromise                   M packages/bench/instanceof.ts:22     function instanceofPromise
keyin                               M packages/bench/instanceof.ts:23     function keyin
nullChainCheckSymbol                M packages/bench/instanceof.ts:31     function nullChainCheckSymbol
nullChainCheckTag                   M packages/bench/instanceof.ts:32     function nullChainCheckTag
typeofObject                        M packages/bench/instanceof.ts:24     function typeofObject
typeofThenCheckSymbol               M packages/bench/instanceof.ts:25     function typeofThenCheckSymbol
typeofThenCheckTag                  M packages/bench/instanceof.ts:26     function typeofThenCheckTag
BenchmarkJS                         C packages/bench/metabench.ts:148    class BenchmarkJS
Metabench                           C packages/bench/metabench.ts:65     class Metabench
Mitata                              C packages/bench/metabench.ts:216    class Mitata
Tinybench                           C packages/bench/metabench.ts:80     class Tinybench
ZodFail                             C packages/bench/object-creation.ts:3      class ZodFail
ZodFail                             C packages/bench/safe.ts:4      class ZodFail
makeFail                            M packages/bench/safe.ts:14     function makeFail
makeSuccess                         M packages/bench/safe.ts:11     function makeSuccess
Page                                M packages/docs/app/(doc)/[[...slug]]/page.tsx:15     function Page
generateMetadata                    M packages/docs/app/(doc)/[[...slug]]/page.tsx:79     function generateMetadata
generateStaticParams                M packages/docs/app/(doc)/[[...slug]]/page.tsx:75     function generateStaticParams
Layout                              M packages/docs/app/(doc)/layout.tsx:68     function Layout
Page                                M packages/docs/app/blog/[slug]/page.tsx:9      function Page
generateMetadata                    M packages/docs/app/blog/[slug]/page.tsx:80     function generateMetadata
generateStaticParams                M packages/docs/app/blog/[slug]/page.tsx:74     function generateStaticParams
BlogLayout                          M packages/docs/app/blog/layout.tsx:5      function BlogLayout
BlogIndexPage                       M packages/docs/app/blog/page.tsx:6      function BlogIndexPage
logo                                M packages/docs/app/layout.config.tsx:5      function logo
Layout                              M packages/docs/app/layout.tsx:16     function Layout
GET                                 M packages/docs/app/llms-full.txt/route.ts:8      function GET
GET                                 M packages/docs/app/llms.txt/route.ts:40     function GET
stringifyTitle                      M packages/docs/app/llms.txt/route.ts:6      function stringifyTitle
GET                                 M packages/docs/app/og.png/route.tsx:15     function GET
loadImage                           M packages/docs/app/og.png/route.tsx:10     function loadImage
Bronze                              M packages/docs/components/bronze.tsx:1      function Bronze
ThemedImage                         M packages/docs/components/codec-image.tsx:12     function ThemedImage
CopyMarkdownButton                  M packages/docs/components/copy-markdown-button.tsx:11     function CopyMarkdownButton
handleCopy                          M packages/docs/components/copy-markdown-button.tsx:14     function handleCopy
ApiLibraries                        M packages/docs/components/ecosystem.tsx:364    function ApiLibraries
FormIntegrations                    M packages/docs/components/ecosystem.tsx:368    function FormIntegrations
MockingLibraries                    M packages/docs/components/ecosystem.tsx:380    function MockingLibraries
PoweredByZod                        M packages/docs/components/ecosystem.tsx:384    function PoweredByZod
ResourceTable                       M packages/docs/components/ecosystem.tsx:358    function ResourceTable
Table                               M packages/docs/components/ecosystem.tsx:325    function Table
XToZod                              M packages/docs/components/ecosystem.tsx:377    function XToZod
ZodToX                              M packages/docs/components/ecosystem.tsx:373    function ZodToX
ZodUtilities                        M packages/docs/components/ecosystem.tsx:388    function ZodUtilities
Featured                            M packages/docs/components/featured.tsx:8      function Featured
Gold                                M packages/docs/components/gold.tsx:1      function Gold
SDKs                                C packages/docs/components/gold.tsx:45     class SDKs
__handleScroll                      M packages/docs/components/heading.tsx:27     function __handleScroll
HeroLogo                            M packages/docs/components/hero-logo.tsx:10     function HeroLogo
If                                  M packages/docs/components/if.tsx:3      function If
InkeepBubble                        M packages/docs/components/inkeep-bubble.tsx:6      function InkeepBubble
InkeepSearchBox                     M packages/docs/components/inkeep-search.tsx:7      function InkeepSearchBox
Platinum                            M packages/docs/components/platinum.tsx:1      function Platinum
Scroller                            M packages/docs/components/scroller.tsx:7      function Scroller
handleScroll                        M packages/docs/components/scroller.tsx:23     function handleScroll
SidebarItem                         M packages/docs/components/sidebar-item.tsx:17     function SidebarItem
SidebarSeparator                    M packages/docs/components/sidebar-item.tsx:41     function SidebarSeparator
SidebarLogo                         M packages/docs/components/sidebar-logo.tsx:6      function SidebarLogo
Silver                              M packages/docs/components/silver.tsx:1      function Silver
Tabs                                M packages/docs/components/tabs.tsx:11     function Tabs
ThemedImage                         M packages/docs/components/themed-image.tsx:12     function ThemedImage
getLLMText                          M packages/docs/loaders/get-llm-text.ts:14     function getLLMText
  ...and 437 more symbols

-- FOCUS
ZodAny (packages/zod/src/v3/types.ts:2112-2112)
  called_by: ts

ZodArray (packages/zod/src/v3/types.ts:2236-2236)
  called_by: ts

ZodBigInt (packages/zod/src/v3/types.ts:1635-1635)
  called_by: ts

ZodBoolean (packages/zod/src/v3/types.ts:1833-1833)
  called_by: ts

ZodBranded (packages/zod/src/v3/types.ts:4743-4743)
  called_by: ts

ZodCatch (packages/zod/src/v3/types.ts:4614-4614)
  called_by: ts

ZodDate (packages/zod/src/v3/types.ts:1877-1877)
  called_by: ts

ZodDefault (packages/zod/src/v3/types.ts:4564-4564)
  called_by: ts

ZodDiscriminatedUnion (packages/zod/src/v3/types.ts:3116-3117)

ZodEffects (packages/zod/src/v3/types.ts:4307-4307)
  called_by: ts

ZodEnum (packages/zod/src/v3/types.ts:4079-4079)
  called_by: ts

ZodError (packages/zod/src/v3/ZodError.ts:194-194)
  called_by: ts

ZodFail (packages/bench/object-creation.ts:3-3)
  called_by: ts

ZodFail (packages/bench/safe.ts:4-4)
  called_by: ts

ZodFailure (packages/bench/instanceof.ts:6-6)
  called_by: ts

ZodFunction (packages/zod/src/v3/types.ts:3817-3817)
  called_by: ts

ZodIntersection (packages/zod/src/v3/types.ts:3287-3287)
  called_by: ts

ZodLazy (packages/zod/src/v3/types.ts:3974-3974)
  called_by: ts

ZodLiteral (packages/zod/src/v3/types.ts:4006-4006)
  called_by: ts

ZodMap (packages/zod/src/v3/types.ts:3592-3592)
  called_by: ts

ZodNaN (packages/zod/src/v3/types.ts:4701-4701)
  called_by: ts

ZodNativeEnum (packages/zod/src/v3/types.ts:4177-4177)
  called_by: ts

ZodNever (packages/zod/src/v3/types.ts:2163-2163)
  called_by: ts

ZodNull (packages/zod/src/v3/types.ts:2079-2079)
  called_by: ts

ZodNullable (packages/zod/src/v3/types.ts:4525-4525)
  called_by: ts

ZodNumber (packages/zod/src/v3/types.ts:1369-1369)
  called_by: ts

ZodObject (packages/zod/src/v3/types.ts:2452-2453)
  called_by: ts

ZodOptional (packages/zod/src/v3/types.ts:4485-4485)
  called_by: ts

ZodPipeline (packages/zod/src/v3/types.ts:4777-4777)
  called_by: ts

ZodPromise (packages/zod/src/v3/types.ts:4235-4235)
  called_by: ts

ZodReadonly (packages/zod/src/v3/types.ts:4872-4872)
  called_by: ts

ZodRecord (packages/zod/src/v3/types.ts:3503-3503)
  called_by: ts

ZodSet (packages/zod/src/v3/types.ts:3686-3686)
  called_by: ts

ZodString (packages/zod/src/v3/types.ts:731-731)
  called_by: ts

ZodSymbol (packages/zod/src/v3/types.ts:2009-2009)
  called_by: ts

ZodTuple (packages/zod/src/v3/types.ts:3395-3396)
  called_by: ts

ZodType (packages/zod/src/v3/types.ts:158-158)

ZodUndefined (packages/zod/src/v3/types.ts:2044-2044)
  called_by: ts

ZodUnion (packages/zod/src/v3/types.ts:2942-2942)
  called_by: ts

ZodUnknown (packages/zod/src/v3/types.ts:2137-2137)
  called_by: ts

ZodVoid (packages/zod/src/v3/types.ts:2192-2192)
  called_by: ts

PoweredByZod (packages/docs/components/ecosystem.tsx:384-385)
  called_by: tsx

XToZod (packages/docs/components/ecosystem.tsx:377-377)
  called_by: tsx

ZodToX (packages/docs/components/ecosystem.tsx:373-373)
  called_by: tsx

ZodUtilities (packages/docs/components/ecosystem.tsx:388-389)
  called_by: tsx

createZodEnum (packages/zod/src/v3/types.ts:4071-4071)
  called_by: ts

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 46 symbols in L3, 0 with behavior annotations
drill: packages/zod/src/v3/types.ts (~1 lines, createZodEnum)
drill: packages/docs/components/ecosystem.tsx (~1 lines, PoweredByZod)
drill: packages/docs/components/ecosystem.tsx (~1 lines, ZodUtilities)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## createZodEnum  (packages/zod/src/v3/types.ts L4071-4071)
```
function createZodEnum(values: [string, ...string[]], params?: RawCreateParams) {
```

## PoweredByZod  (packages/docs/components/ecosystem.tsx L384-385)
```
export async function PoweredByZod() {
  return <ResourceTable resources={poweredByZodProjects} />;
```

## ZodUtilities  (packages/docs/components/ecosystem.tsx L388-389)
```
export async function ZodUtilities() {
  return <ResourceTable resources={zodUtilities} />;
```

## ApiLibraries  (packages/docs/components/ecosystem.tsx L364-365)
```
export async function ApiLibraries() {
  return <ResourceTable resources={apiLibraries} />;
```

## FormIntegrations  (packages/docs/components/ecosystem.tsx L368-369)
```
export async function FormIntegrations() {
  return <ResourceTable resources={formIntegrations} />;
```

## MockingLibraries  (packages/docs/components/ecosystem.tsx L380-381)
```
export async function MockingLibraries() {
  return <ResourceTable resources={mockingLibraries} />;
```

## ResourceTable  (packages/docs/components/ecosystem.tsx L358-358)
```
async function ResourceTable({ resources }: ResourceTableProps) {
```

## Table  (packages/docs/components/ecosystem.tsx L325-325)
```
export function Table(props: { resources: ZodResource[] }) {
```

## XToZod  (packages/docs/components/ecosystem.tsx L377-377)
```
  return <ResourceTable resources={xToZodConverters} />;
```

## ZodToX  (packages/docs/components/ecosystem.tsx L373-373)
```
  return <ResourceTable resources={zodToXConverters} />;
```

## Class  (packages/zod/src/v4/mini/schemas.ts L1783-1783)
```
abstract class Class {
```

## ParseInputLazyPath  (packages/zod/src/v3/types.ts L62-62)
```
class ParseInputLazyPath implements ParseInput {
```

## This  (packages/zod/src/v3/types.ts L515-515)
```
    const This = (this as any).constructor;
```

## ZodAny  (packages/zod/src/v3/types.ts L2112-2112)
```
export class ZodAny extends ZodType<any, ZodAnyDef, any> {
```

## ZodArray  (packages/zod/src/v3/types.ts L2236-2236)
```
export class ZodArray<T extends ZodTypeAny, Cardinality extends ArrayCardinality = "many"> extends ZodType<
```

## ZodBigInt  (packages/zod/src/v3/types.ts L1635-1635)
```
export class ZodBigInt extends ZodType<bigint, ZodBigIntDef, bigint> {
```

## ZodBoolean  (packages/zod/src/v3/types.ts L1833-1833)
```
export class ZodBoolean extends ZodType<boolean, ZodBooleanDef, boolean> {
```

## ZodBranded  (packages/zod/src/v3/types.ts L4743-4743)
```
export class ZodBranded<T extends ZodTypeAny, B extends string | number | symbol> extends ZodType<
```

## ZodCatch  (packages/zod/src/v3/types.ts L4614-4614)
```
export class ZodCatch<T extends ZodTypeAny> extends ZodType<
```

## ZodDate  (packages/zod/src/v3/types.ts L1877-1877)
```
export class ZodDate extends ZodType<Date, ZodDateDef, Date> {
```

## ZodDefault  (packages/zod/src/v3/types.ts L4564-4564)
```
export class ZodDefault<T extends ZodTypeAny> extends ZodType<
```

## ZodDiscriminatedUnion  (packages/zod/src/v3/types.ts L3116-3117)
```
export class ZodDiscriminatedUnion<
  Discriminator extends string,
```

## ZodEffects  (packages/zod/src/v3/types.ts L4307-4307)
```
export class ZodEffects<T extends ZodTypeAny, Output = output<T>, Input = input<T>> extends ZodType<
```

## ZodEnum  (packages/zod/src/v3/types.ts L4079-4079)
```
export class ZodEnum<T extends [string, ...string[]]> extends ZodType<T[number], ZodEnumDef<T>, T[number]> {
```

## ZodFunction  (packages/zod/src/v3/types.ts L3817-3817)
```
export class ZodFunction<Args extends ZodTuple<any, any>, Returns extends ZodTypeAny> extends ZodType<
```

## ZodIntersection  (packages/zod/src/v3/types.ts L3287-3287)
```
export class ZodIntersection<T extends ZodTypeAny, U extends ZodTypeAny> extends ZodType<
```

## ZodLazy  (packages/zod/src/v3/types.ts L3974-3974)
```
export class ZodLazy<T extends ZodTypeAny> extends ZodType<output<T>, ZodLazyDef<T>, input<T>> {
```

## ZodLiteral  (packages/zod/src/v3/types.ts L4006-4006)
```
export class ZodLiteral<T> extends ZodType<T, ZodLiteralDef<T>, T> {
```

## ZodMap  (packages/zod/src/v3/types.ts L3592-3592)
```
export class ZodMap<Key extends ZodTypeAny = ZodTypeAny, Value extends ZodTypeAny = ZodTypeAny> extends ZodType<
```

## ZodNaN  (packages/zod/src/v3/types.ts L4701-4701)
```
export class ZodNaN extends ZodType<number, ZodNaNDef, number> {
```

## ZodNativeEnum  (packages/zod/src/v3/types.ts L4177-4177)
```
export class ZodNativeEnum<T extends EnumLike> extends ZodType<T[keyof T], ZodNativeEnumDef<T>, T[keyof T]> {
```

## ZodNever  (packages/zod/src/v3/types.ts L2163-2163)
```
export class ZodNever extends ZodType<never, ZodNeverDef, never> {
```

## ZodNull  (packages/zod/src/v3/types.ts L2079-2079)
```
export class ZodNull extends ZodType<null, ZodNullDef, null> {
```

## ZodNullable  (packages/zod/src/v3/types.ts L4525-4525)
```
export class ZodNullable<T extends ZodTypeAny> extends ZodType<
```

## ZodNumber  (packages/zod/src/v3/types.ts L1369-1369)
```
export class ZodNumber extends ZodType<number, ZodNumberDef, number> {
```

## ZodObject  (packages/zod/src/v3/types.ts L2452-2453)
```
export class ZodObject<
  T extends ZodRawShape,
```

## ZodOptional  (packages/zod/src/v3/types.ts L4485-4485)
```
export class ZodOptional<T extends ZodTypeAny> extends ZodType<
```

## ZodPipeline  (packages/zod/src/v3/types.ts L4777-4777)
```
export class ZodPipeline<A extends ZodTypeAny, B extends ZodTypeAny> extends ZodType<
```

## ZodPromise  (packages/zod/src/v3/types.ts L4235-4235)
```
export class ZodPromise<T extends ZodTypeAny> extends ZodType<
```

## ZodReadonly  (packages/zod/src/v3/types.ts L4872-4872)
```
export class ZodReadonly<T extends ZodTypeAny> extends ZodType<
```

## ZodRecord  (packages/zod/src/v3/types.ts L3503-3503)
```
export class ZodRecord<Key extends KeySchema = ZodString, Value extends ZodTypeAny = ZodTypeAny> extends ZodType<
```

## ZodSet  (packages/zod/src/v3/types.ts L3686-3686)
```
export class ZodSet<Value extends ZodTypeAny = ZodTypeAny> extends ZodType<
```

## ZodString  (packages/zod/src/v3/types.ts L731-731)
```
export class ZodString extends ZodType<string, ZodStringDef, string> {
```

## ZodSymbol  (packages/zod/src/v3/types.ts L2009-2009)
```
export class ZodSymbol extends ZodType<symbol, ZodSymbolDef, symbol> {
```

## ZodTuple  (packages/zod/src/v3/types.ts L3395-3396)
```
export class ZodTuple<
  T extends ZodTupleItems | [] = ZodTupleItems,
```
--- END SOURCE SNIPPETS ---

QUESTION: How is Zod 4 split across the `zod`, `zod/mini`, and `zod/v4/core` packages?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
