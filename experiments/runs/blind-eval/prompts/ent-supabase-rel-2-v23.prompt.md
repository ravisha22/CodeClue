# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-supabase-rel-2

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 supabase@HEAD 6483mod 21369sym
? What ownership and transfer constraints exist around Supabase projects and organizations?


-- README
<p align="center"> <img src="https://user-images.githubusercontent.com/8291514/213727234-cda046d6-28c6-491a-b284-b86c5cede25d.png#gh-lig...
sections: Supabase, Documentation, Community & Support, How it works, Client libraries

-- TREE
apps/  (5237 files)
blocks/  (32 files)
docker/  (4 files)
e2e/  (56 files)
examples/  (422 files)
packages/  (725 files)
scripts/  (7 files)
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
L.get                               M apps/studio/public/monaco-editor/base/worker/workerMain.js:6101   method L.get
D.get                               M apps/studio/public/monaco-editor/base/worker/workerMain.js:5208   method D.get
D.get                               M apps/studio/public/monaco-editor/base/worker/workerMain.js:6975   method D.get
R.get                               M apps/studio/public/monaco-editor/base/worker/workerMain.js:2024   method R.get
R.get                               M apps/studio/public/monaco-editor/base/worker/workerMain.js:6116   method R.get
p.get                               M apps/studio/public/monaco-editor/base/worker/workerMain.js:6078   method p.get
r.get                               M apps/studio/public/monaco-editor/base/worker/workerMain.js:2974   method r.get
InvalidRequestError.constructor     M apps/docs/app/api/utils.ts:32     method InvalidRequestError.constructor
NoDataError.constructor             M apps/docs/app/api/utils.ts:50     method NoDataError.constructor
D._insert                           M apps/studio/public/monaco-editor/base/worker/workerMain.js:3031   method D._insert
d.set                               M apps/studio/public/monaco-editor/base/worker/workerMain.js:2939   method d.set
r.set                               M apps/studio/public/monaco-editor/base/worker/workerMain.js:2977   method r.set
ContextLengthError.constructor      M packages/ai-commands/src/errors.ts:11     method ContextLengthError.constructor
EmptyResponseError.constructor      M packages/ai-commands/src/errors.ts:17     method EmptyResponseError.constructor
EmptySqlError.constructor           M packages/ai-commands/src/errors.ts:23     method EmptySqlError.constructor
E.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:10675  method E.constructor
f.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:10273  method f.constructor
E.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:2880   method E.constructor
D.set                               M apps/studio/public/monaco-editor/base/worker/workerMain.js:5204   method D.set
D.set                               M apps/studio/public/monaco-editor/base/worker/workerMain.js:6978   method D.set
S.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:6446   method S.constructor
g.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:9836   method g.constructor
o.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:10117  method o.constructor
i.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:6983   method i.constructor
e.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:6283   method e.constructor
d.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:2936   method d.constructor
i.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:5217   method i.constructor
r.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:2960   method r.constructor
y.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:2893   method y.constructor
S.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:2844   method S.constructor
p.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:950    method p.constructor
ge.constructor                      M apps/studio/public/monaco-editor/base/worker/workerMain.js:9720   method ge.constructor
C.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:10791  method C.constructor
R.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:2085   method R.constructor
r.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:10055  method r.constructor
d.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:6851   method d.constructor
R.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:141    method R.constructor
D.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:5334   method D.constructor
D.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:5772   method D.constructor
D.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:304    method D.constructor
D.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:909    method D.constructor
W.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:3384   method W.constructor
w.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:9750   method w.constructor
R.constructor                       M apps/studio/public/monaco-editor/base/worker/workerMain.js:2344   method R.constructor
  ...and 21235 more symbols

-- FOCUS
docker/.env.example (docker/.env.example:1-345)
  Config summary for docker/.env.example: entries: POSTGRES_PASSWORD=your-super-secret-and-long-postgres-p..., JWT_SECRET=your-super-secret-jwt-token-with-at-l..., ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...., SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...., SUPABASE_PUBLISHABLE_KEY=<set>, SUPABASE_SECRET_KEY=<set>
  entries: POSTGRES_PASSWORD=your-super-secret-and-long-postgres-p..., JWT_SECRET=your-super-secret-jwt-token-with-at-l..., ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...., SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...., SUPABASE_PUBLISHABLE_KEY=<set>

examples/auth/hono-full/.env.example (examples/auth/hono-full/.env.example:1-3)
  Config summary for examples/auth/hono-full/.env.example: entries: VITE_SUPABASE_URL=your_supabase_url, VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
  entries: VITE_SUPABASE_URL=your_supabase_url, VITE_SUPABASE_ANON_KEY=your_supabase_anon_key

examples/oauth-app-authorization-flow/.env.example (examples/oauth-app-authorization-flow/.env.example:1-4)
  Config summary for examples/oauth-app-authorization-flow/.env.example: entries: SUPABASE_REDIRECT_URL=http://localhost:3000/callback, SUPABASE_CLIENT_ID=<set>, SUPABASE_CLIENT_SECRET=<set>
  entries: SUPABASE_REDIRECT_URL=http://localhost:3000/callback, SUPABASE_CLIENT_ID=<set>, SUPABASE_CLIENT_SECRET=<set>

ProjectTransferPreviewData (apps/studio/data/projects/project-transfer-preview-query.ts:28-28)
  type alias ProjectTransferPreviewData = Awaited<ReturnType<typeof previewProjectTransfer>> export type ProjectTransferPreviewError = {
  uses: Awaited, ReturnType, previewProjectTransfer, ProjectTransferPreviewError

ProjectTransferPreviewData (apps/studio/data/projects/project-transfer-preview-query.ts:29-29)
  type alias ProjectTransferPreviewData = Awaited<ReturnType<typeof previewProjectTransfer>> export type ProjectTransferPreviewError = {
  uses: Awaited, ReturnType, previewProjectTransfer, ProjectTransferPreviewError

ProjectTransferPreviewError (apps/studio/data/projects/project-transfer-preview-query.ts:30-30)
  type alias ProjectTransferPreviewError = {

ProjectTransferPreviewVariables (apps/studio/data/projects/project-transfer-preview-query.ts:6-6)
  type alias ProjectTransferPreviewVariables = {

ProjectTransferPreviewVariables (apps/studio/data/projects/project-transfer-preview-query.ts:7-7)
  type alias ProjectTransferPreviewVariables = {

ProjectTransferVariables (apps/studio/data/projects/project-transfer-mutation.ts:8-8)
  type alias ProjectTransferVariables = {

ProjectTransferVariables (apps/studio/data/projects/project-transfer-mutation.ts:9-9)
  type alias ProjectTransferVariables = {

TransferProjectButton (apps/studio/components/interfaces/Settings/General/TransferProjectPanel/TransferProjectButton.tsx:19-290)
  behavior: TRANSFORM(map)
  uses: it.id, toast.success, queryClient.removeQueries, projectKeys.projectTransferPreview

OrganizationsData (apps/studio/data/organizations/organization-query.ts:34-34)
  type alias OrganizationsData = Awaited<ReturnType<typeof getOrganization>> export type OrganizationsError = ResponseError export const useOrganizationQuery = <TData = OrganizationsData>( { slug }: OrganizationVariables,
  uses: Awaited, ReturnType, getOrganization, OrganizationsError

OrganizationsData (apps/studio/data/organizations/organization-query.ts:33-33)
  type alias OrganizationsData = Awaited<ReturnType<typeof getOrganization>> export type OrganizationsError = ResponseError export const useOrganizationQuery = <TData = OrganizationsData>( { slug }: OrganizationVariables,
  uses: Awaited, ReturnType, getOrganization, OrganizationsError

OrganizationsError (apps/studio/data/organizations/organization-query.ts:35-35)
  type alias OrganizationsError = ResponseError export const useOrganizationQuery = <TData = OrganizationsData>( { slug }: OrganizationVariables,
  uses: ResponseError, const, useOrganizationQuery, TData

NoOrganizationsState (apps/studio/components/interfaces/Home/ProjectList/EmptyStates.tsx:94-106)

NoProjectsState (apps/studio/components/interfaces/Home/ProjectList/EmptyStates.tsx:76-93)
  sig: NoProjectsState({ slug }: { slug: string })

TransferProjectPanel (apps/studio/components/interfaces/Settings/General/TransferProjectPanel/TransferProjectPanel.tsx:14-50)

createProjectSupabaseClient (apps/studio/lib/project-supabase-client.ts:8-29)
  sig: createProjectSupabaseClient(projectRef: string, clientEndpoint: string)

invalidateOrganizationsQuery (apps/studio/data/organizations/organization-query.ts:52-55)
  sig: invalidateOrganizationsQuery(client: QueryClient)
  behavior: DELEGATE(client.invalidateQueries -> result)
  uses: client.invalidateQueries, organizationKeys.list

projectsToAddToRole (apps/studio/components/interfaces/Organization/TeamSettings/UpdateRolesPanel/UpdateRolesPanel.utils.ts:145-162)
  sig: projectsToAddToRole(groupByAddedRoles[role.base_role_id]?.map((r)
  uses: toUpdate.push, role.id

SupabaseService.updateProfile (examples/user-management/ionic-angular-user-management/src/app/supabase.service.ts:60-69)
  async_method SupabaseService.updateProfile
  sig: SupabaseService.updateProfile(profile: Profile)
  behavior: DELEGATE(this.supabase.from -> result)
  called_by: SupabaseService
  uses: this.user, this.supabase.from

SupabaseService.signIn (examples/user-management/angular-user-management/src/app/supabase.service.ts:42-44)
  method SupabaseService.signIn
  sig: SupabaseService.signIn(email: string)
  behavior: DELEGATE(this.supabase.auth.signInWithOtp -> result)
  called_by: SupabaseService
  uses: this.supabase.auth.signInWithOtp

SupabaseService.updateProfile (examples/user-management/angular-user-management/src/app/supabase.service.ts:50-57)
  method SupabaseService.updateProfile
  sig: SupabaseService.updateProfile(profile: Profile)
  behavior: DELEGATE(this.supabase.from -> result)
  called_by: SupabaseService
  uses: this.supabase.from

SupabaseService.downLoadImage (examples/user-management/ionic-angular-user-management/src/app/supabase.service.ts:71-73)
  method SupabaseService.downLoadImage
  sig: SupabaseService.downLoadImage(path: string)
  behavior: DELEGATE(this.supabase.storage.from -> result)
  called_by: SupabaseService
  uses: this.supabase.storage.from

SupabaseService.user (examples/user-management/ionic-angular-user-management/src/app/supabase.service.ts:25-27)
  method SupabaseService.user
  behavior: DELEGATE(this.supabase.auth.getUser -> result)
  called_by: SupabaseService
  uses: this.supabase.auth.getUser

SupabaseService.downLoadImage (examples/user-management/angular-user-management/src/app/supabase.service.ts:59-61)
  method SupabaseService.downLoadImage
  sig: SupabaseService.downLoadImage(path: string)
  behavior: DELEGATE(this.supabase.storage.from -> result)
  called_by: SupabaseService
  uses: this.supabase.storage.from

SupabaseService.signIn (examples/user-management/ionic-angular-user-management/src/app/supabase.service.ts:52-54)
  method SupabaseService.signIn
  sig: SupabaseService.signIn(email: string)
  behavior: DELEGATE(this.supabase.auth.signInWithOtp -> result)
  called_by: SupabaseService
  uses: this.supabase.auth.signInWithOtp

SupabaseService.signOut (examples/user-management/angular-user-management/src/app/supabase.service.ts:46-48)
  method SupabaseService.signOut
  behavior: DELEGATE(this.supabase.auth.signOut -> result)
  called_by: SupabaseService
  uses: this.supabase.auth.signOut

SupabaseService.signOut (examples/user-management/ionic-angular-user-management/src/app/supabase.service.ts:56-58)
  method SupabaseService.signOut
  behavior: DELEGATE(this.supabase.auth.signOut -> result)
  called_by: SupabaseService
  uses: this.supabase.auth.signOut

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 83 symbols in L3, 27 with behavior annotations
uncovered: SupabaseClient, SupabaseClient, SupabaseClient, SupabaseJsResult

--- CLUE FILE END ---

QUESTION: What ownership and transfer constraints exist around Supabase projects and organizations?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
