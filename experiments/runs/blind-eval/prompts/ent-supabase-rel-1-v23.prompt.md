# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-supabase-rel-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 supabase@HEAD 6483mod 21358sym
? How do API keys, auth tokens, and RLS work together in Supabase's access model?


-- TREE
apps/  (5235 files)
  design-system/  docs/  learn/  lite-studio/  studio/  ui-library/  www/
blocks/  (32 files)
  vue/
docker/  (2 files)
e2e/  (56 files)
  studio/
examples/  (418 files)
  clerk/
packages/  (724 files)
  ai-commands/  api-types/  common/  config/  dev-tools/  eslint-config-supabase/  generator/  marketing/  shared-data/  ui/  ...+1
scripts/  (7 files)
  actions/
supabase/  (9 files)

-- INDEX
apps/studio/public/monaco-editor/base/worker/workerMain.js 11606L  $, A, A, A, constructor
apps/studio/public/monaco-editor/loader.js     1365L  a, configure, constructor, enqueueDefineAnonymousModule, getBuildInfo
apps/studio/components/layouts/TableEditorLayout/ExportAllRows.errors.ts    93L  constructor, BlobCreationError, constructor, DownloadSaveError, constructor
apps/docs/scripts/search/sources/markdown.ts     85L  fromGuideModel, load, MarkdownLoader, extractIndexedContent, process
apps/docs/resources/utils/connections.ts        382L  CollectionFetch, CollectionInMemory, GraphQLCollection, paginateArray, GraphQLCollectionBuilder
apps/docs/scripts/search/sources/github-discussion.ts   147L  Discussion, Discussion, DiscussionsResponse, DiscussionsResponse, ExtendedOctokit
apps/docs/scripts/search/sources/partner-integrations.ts    85L  load, IntegrationLoader, extractIndexedContent, process, IntegrationSource
apps/docs/scripts/search/sources/troubleshooting.ts   101L  load, TroubleshootingLoader, extractIndexedContent, process, TroubleshootingSource
apps/studio/lib/api/self-hosted/functions/fileSystemStore.ts    80L  constructor, getFileEntriesBySlug, getFunctionBySlug, getFunctions, FileSystemFunctionsArtifactStore
examples/edge-functions/supabase/functions/kysely-postgres/DenoPostgresDriver.ts   152L  constructor, executeQuery, PostgresConnection, PostgresConnectionOptions, PostgresDialectConfig
packages/pg-meta/src/query/QueryFilter.ts        82L  IQueryFilter, clone, filter, match, order
apps/design-system/__registry__/default/block/chart-bar-interactive.tsx   210L  Component
apps/design-system/__registry__/default/block/chart-composed-actions.tsx   106L  ChartComposedActions
  ...and 6470 more modules

-- SYM
S.push                              M apps/studio/public/monaco-editor/base/worker/workerMain.js:9966   method S.push
D.push                              M apps/studio/public/monaco-editor/base/worker/workerMain.js:3028   method D.push
D.get                               M apps/studio/public/monaco-editor/base/worker/workerMain.js:2040   method D.get
i.get                               M apps/studio/public/monaco-editor/base/worker/workerMain.js:10891  method i.get
D.get                               M apps/studio/public/monaco-editor/base/worker/workerMain.js:5208   method D.get
L.get                               M apps/studio/public/monaco-editor/base/worker/workerMain.js:6101   method L.get
R.get                               M apps/studio/public/monaco-editor/base/worker/workerMain.js:6116   method R.get
r.get                               M apps/studio/public/monaco-editor/base/worker/workerMain.js:2974   method r.get
D.get                               M apps/studio/public/monaco-editor/base/worker/workerMain.js:6975   method D.get
R.get                               M apps/studio/public/monaco-editor/base/worker/workerMain.js:2024   method R.get
p.get                               M apps/studio/public/monaco-editor/base/worker/workerMain.js:6078   method p.get
InvalidRequestError.constructor     M apps/docs/app/api/utils.ts:32     method InvalidRequestError.constructor
NoDataError.constructor             M apps/docs/app/api/utils.ts:50     method NoDataError.constructor
D._insert                           M apps/studio/public/monaco-editor/base/worker/workerMain.js:3031   method D._insert
d.set                               M apps/studio/public/monaco-editor/base/worker/workerMain.js:2939   method d.set
r.set                               M apps/studio/public/monaco-editor/base/worker/workerMain.js:2977   method r.set
EmptySqlError.constructor           M packages/ai-commands/src/errors.ts:23     method EmptySqlError.constructor
ContextLengthError.constructor      M packages/ai-commands/src/errors.ts:11     method ContextLengthError.constructor
EmptyResponseError.constructor      M packages/ai-commands/src/errors.ts:17     method EmptyResponseError.constructor
E.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:10675  method E.constructor
f.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:10273  method f.constructor
E.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:2880   method E.constructor
D.set                               M apps/studio/public/monaco-editor/base/worker/workerMain.js:6978   method D.set
D.set                               M apps/studio/public/monaco-editor/base/worker/workerMain.js:5204   method D.set
S.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:6446   method S.constructor
g.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:9836   method g.constructor
o.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:10117  method o.constructor
i.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:6983   method i.constructor
e.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:6283   method e.constructor
S.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:2844   method S.constructor
d.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:2936   method d.constructor
p.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:950    method p.constructor
r.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:2960   method r.constructor
i.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:5217   method i.constructor
y.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:2893   method y.constructor
ge.constructor                      M apps/studio/public/monaco-editor/base/worker/workerMain.js:9720   method ge.constructor
C.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:10791  method C.constructor
R.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:2085   method R.constructor
r.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:10055  method r.constructor
d.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:6851   method d.constructor
R.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:141    method R.constructor
D.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:5334   method D.constructor
D.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:5772   method D.constructor
D.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:909    method D.constructor
W.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:3384   method W.constructor
w.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:9750   method w.constructor
D.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:304    method D.constructor
R.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:2344   method R.constructor
S.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:10556  method S.constructor
S.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:11365  method S.constructor
a.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:3919   method a.constructor
a.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:7988   method a.constructor
p.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:10195  method p.constructor
D.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:5194   method D.constructor
ee.constructor                      M apps/studio/public/monaco-editor/base/worker/workerMain.js:3517   method ee.constructor
i.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:9447   method i.constructor
  ...and 21217 more symbols

-- FOCUS
authConfigToCustomAccessTokenHookDetails (apps/studio/hooks/misc/useCustomAccessTokenHookDetails.tsx:5-15)
  sig: authConfigToCustomAccessTokenHookDetails(authConfig?: AuthConfigResponse)
  behavior: GUARD(!authConfig || !authConfig.HOOK_CUSTOM_ACCESS_TOKEN_ENABLED -> return...)
  called_by: useCustomAccessTokenHookDetails
  uses: authConfig.HOOK_CUSTOM_ACCESS_TOKEN_ENABLED, authConfig.HOOK_CUSTOM_ACCESS_TOKEN_URI, authConfig.HOOK_CUSTOM_ACCESS_TOKEN_SECRETS

isApiAccessRole (apps/studio/lib/data-api-types.ts:6-9)
  sig: isApiAccessRole(value: string)
  behavior: DELEGATE(API_ACCESS_ROLES.includes -> result)
  uses: API_ACCESS_ROLES.includes

AccessToken (apps/studio/data/access-tokens/access-tokens-query.ts:18-18)
  type alias AccessToken = AccessTokensData[number] export const useAccessTokensQuery = <TData = AccessTokensData>({
  uses: AccessTokensData, number, const, useAccessTokensQuery

AccessToken (apps/studio/data/access-tokens/access-tokens-query.ts:17-17)
  type alias AccessToken = AccessTokensData[number] export const useAccessTokensQuery = <TData = AccessTokensData>({
  uses: AccessTokensData, number, const, useAccessTokensQuery

ScopedAccessToken (apps/studio/data/scoped-access-tokens/scoped-access-token-query.ts:31-31)
  type alias ScopedAccessToken = components['schemas']['GetScopedAccessTokensResponse']['tokens'][number] export type ScopedAccessTokenData = Awaited<ReturnType<typeof getScopedAccessToken>> export const useScopedAccessTokensQuery = <TData = ScopedAccessTokensData>({
  uses: components, schemas, GetScopedAccessTokensResponse, tokens

ScopedAccessToken (apps/studio/data/scoped-access-tokens/scoped-access-token-query.ts:32-32)
  type alias ScopedAccessToken = components['schemas']['GetScopedAccessTokensResponse']['tokens'][number] export type ScopedAccessTokenData = Awaited<ReturnType<typeof getScopedAccessToken>> export const useScopedAccessTokensQuery = <TData = ScopedAccessTokensData>({
  uses: components, schemas, GetScopedAccessTokensResponse, tokens

ScopedAccessTokenData (apps/studio/data/scoped-access-tokens/scoped-access-token-query.ts:35-35)
  type alias ScopedAccessTokenData = Awaited<ReturnType<typeof getScopedAccessToken>> export const useScopedAccessTokensQuery = <TData = ScopedAccessTokensData>({
  uses: Awaited, ReturnType, getScopedAccessToken, const

ScopedAccessTokenData (apps/studio/data/scoped-access-tokens/scoped-access-token-query.ts:34-34)
  type alias ScopedAccessTokenData = Awaited<ReturnType<typeof getScopedAccessToken>> export const useScopedAccessTokensQuery = <TData = ScopedAccessTokensData>({
  uses: Awaited, ReturnType, getScopedAccessToken, const

ScopedAccessTokensData (apps/studio/data/scoped-access-tokens/scoped-access-token-query.ts:29-29)
  type alias ScopedAccessTokensData = Awaited<ReturnType<typeof getScopedAccessTokens>> export type ScopedAccessTokensError = ResponseError export type ScopedAccessToken = components['schemas']['GetScopedAccessTokensResponse']['tokens'][number] export type ScopedAccessTokenData = Awaited<ReturnType<typeof getScopedAccessToken>>
  uses: Awaited, ReturnType, getScopedAccessTokens, ScopedAccessTokensError

ScopedAccessTokensData (apps/studio/data/scoped-access-tokens/scoped-access-token-query.ts:28-28)
  type alias ScopedAccessTokensData = Awaited<ReturnType<typeof getScopedAccessTokens>> export type ScopedAccessTokensError = ResponseError export type ScopedAccessToken = components['schemas']['GetScopedAccessTokensResponse']['tokens'][number] export type ScopedAccessTokenData = Awaited<ReturnType<typeof getScopedAccessToken>>
  uses: Awaited, ReturnType, getScopedAccessTokens, ScopedAccessTokensError

ScopedAccessTokensError (apps/studio/data/scoped-access-tokens/scoped-access-token-query.ts:30-30)
  type alias ScopedAccessTokensError = ResponseError export type ScopedAccessToken = components['schemas']['GetScopedAccessTokensResponse']['tokens'][number] export type ScopedAccessTokenData = Awaited<ReturnType<typeof getScopedAccessToken>> export const useScopedAccessTokensQuery = <TData = ScopedAccessTokensData>({
  uses: ResponseError, ScopedAccessToken, components, schemas

getScopedAccessTokens (apps/studio/data/scoped-access-tokens/scoped-access-token-query.ts:7-14)
  sig: getScopedAccessTokens(signal?: AbortSignal)

getApiAccessSwitch (e2e/studio/features/api-access-toggle.spec.ts:63-70)
  sig: getApiAccessSwitch(page: Page)
  behavior: DELEGATE(dataApiSection.getByRole -> result)
  uses: page.getByTestId, page.getByRole, dataApiSection.getByRole

forwardToSupabaseAPI (apps/ui-library/registry/default/platform/platform-kit-nextjs/app/api/supabase-proxy/[...path]/route.ts:2-81)
  sig: forwardToSupabaseAPI(request: Request, method: string, params: { path: string[] })
  behavior: PRECEDENCE(not_process -> not_userHasPermissionForProj -> contentType)
  called_by: GET, HEAD, PATCH, POST, PUT
  uses: process.env.SUPABASE_MANAGEMENT_API_TOKEN, console.error, NextResponse.json, path.join

ApiKeysFeedbackBanner (apps/studio/components/interfaces/APIKeys/ApiKeysIllustrations.tsx:126-165)
  uses: LOCAL_STORAGE_KEYS.API_KEYS_FEEDBACK_DISMISSED, github.com, SupportCategories.PROBLEM

ApiKeysTabContent (apps/studio/components/interfaces/Connect/ApiKeysTabContent.tsx:24-76)
  sig: ApiKeysTabContent({ projectKeys }: { projectKeys: projectKeys })
  behavior: PRECEDENCE(isLoadingPermissions -> not_canReadAPIKeys)
  uses: PermissionAction.SECRETS_READ, projectKeys.apiUrl, projectKeys.publishableKey, projectKeys.anonKey

ApiKeysTableIllustration (apps/studio/components/interfaces/APIKeys/ApiKeysIllustrations.tsx:48-90)
  behavior: TRANSFORM(map)
  uses: mockApiKeys.map, apiKey.id, apiKey.name

useApiKeysCommands (apps/studio/components/interfaces/App/CommandMenu/ApiKeys.tsx:23-166)
  behavior: TRANSFORM(map)
  uses: PermissionAction.SECRETS_READ, publishableKey.api_key, toast.success, publishableKey.type

AccessTokensData (apps/studio/data/access-tokens/access-tokens-query.ts:15-15)
  type alias AccessTokensData = Awaited<ReturnType<typeof getAccessTokens>> export type AccessTokensError = ResponseError export type AccessToken = AccessTokensData[number] export const useAccessTokensQuery = <TData = AccessTokensData>({
  uses: Awaited, ReturnType, getAccessTokens, AccessTokensError

AccessTokensData (apps/studio/data/access-tokens/access-tokens-query.ts:14-14)
  type alias AccessTokensData = Awaited<ReturnType<typeof getAccessTokens>> export type AccessTokensError = ResponseError export type AccessToken = AccessTokensData[number] export const useAccessTokensQuery = <TData = AccessTokensData>({
  uses: Awaited, ReturnType, getAccessTokens, AccessTokensError

AccessTokensError (apps/studio/data/access-tokens/access-tokens-query.ts:16-16)
  type alias AccessTokensError = ResponseError export type AccessToken = AccessTokensData[number] export const useAccessTokensQuery = <TData = AccessTokensData>({
  uses: ResponseError, AccessToken, AccessTokensData, number

ApiAccessRole (apps/studio/lib/data-api-types.ts:5-5)
  type alias ApiAccessRole = (typeof API_ACCESS_ROLES)[number]
  uses: API_ACCESS_ROLES, number

DataApiAccessType (apps/studio/data/privileges/table-api-access-query.ts:64-64)
  type alias DataApiAccessType = 'none' | 'exposed-schema-no-grants' | 'access' export type TableApiAccessData = | {
  uses: none, exposed, schema, no

DataApiAccessType (apps/studio/data/privileges/table-api-access-query.ts:63-63)
  type alias DataApiAccessType = 'none' | 'exposed-schema-no-grants' | 'access' export type TableApiAccessData = | {
  uses: none, exposed, schema, no

ProjectKeys (apps/docs/lib/fetch/projectApi.ts:14-14)
  type alias ProjectKeys = Awaited<ReturnType<typeof getProjectKeys>> export type ProjectSettings = Awaited<ReturnType<typeof getProjectSettings>> async function getProjectKeys({ projectRef }: ProjectApiVariables, signal?: AbortSignal) {
  uses: Awaited, ReturnType, getProjectKeys, ProjectSettings

ProjectKeys (apps/ui-library/lib/fetch/projectApi.ts:9-9)
  type alias ProjectKeys = Awaited<ReturnType<typeof getProjectKeys>> export type ProjectSettings = Awaited<ReturnType<typeof getProjectSettings>> const projectApiKeys = {
  uses: Awaited, ReturnType, getProjectKeys, ProjectSettings

ProjectKeys (apps/docs/lib/fetch/projectApi.ts:15-15)
  type alias ProjectKeys = Awaited<ReturnType<typeof getProjectKeys>> export type ProjectSettings = Awaited<ReturnType<typeof getProjectSettings>> async function getProjectKeys({ projectRef }: ProjectApiVariables, signal?: AbortSignal) {
  uses: Awaited, ReturnType, getProjectKeys, ProjectSettings

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 80 symbols in L3, 11 with behavior annotations
uncovered: AccessTokenListProps, AccessTokenNewBannerProps, NewAccessTokenButtonProps, NewAccessTokenDialogProps

--- CLUE FILE END ---

QUESTION: How do API keys, auth tokens, and RLS work together in Supabase's access model?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
