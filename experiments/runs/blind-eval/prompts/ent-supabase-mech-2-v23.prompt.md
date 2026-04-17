# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-supabase-mech-2

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 supabase@HEAD 6483mod 21358sym
? How do Supabase Cron jobs execute and interact with other services?


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
DatabaseCronJobData (apps/studio/data/database-cron-jobs/database-cron-jobs-count-query.ts:28-28)
  type alias DatabaseCronJobData = number export type DatabaseCronJobError = ResponseError export const useCronJobsCountQuery = <TData = DatabaseCronJobData>( { projectRef, connectionString }: DatabaseCronJobsCountVariables,
  uses: number, DatabaseCronJobError, ResponseError, const

DatabaseCronJobData (apps/studio/data/database-cron-jobs/database-cron-jobs-count-query.ts:29-29)
  type alias DatabaseCronJobData = number export type DatabaseCronJobError = ResponseError export const useCronJobsCountQuery = <TData = DatabaseCronJobData>( { projectRef, connectionString }: DatabaseCronJobsCountVariables,
  uses: number, DatabaseCronJobError, ResponseError, const

DatabaseCronJobError (apps/studio/data/database-cron-jobs/database-cron-jobs-count-query.ts:30-30)
  type alias DatabaseCronJobError = ResponseError export const useCronJobsCountQuery = <TData = DatabaseCronJobData>( { projectRef, connectionString }: DatabaseCronJobsCountVariables,
  uses: ResponseError, const, useCronJobsCountQuery, TData

DatabaseCronJobError (apps/studio/data/database-cron-jobs/database-cron-timezone-query.ts:25-25)
  type alias DatabaseCronJobError = ResponseError export const useCronTimezoneQuery = <TData = string>( { projectRef, connectionString }: DatabaseCronJobsVariables,
  uses: ResponseError, const, useCronTimezoneQuery, TData

DatabaseCronJobError (apps/studio/data/database-cron-jobs/database-cron-timezone-query.ts:26-26)
  type alias DatabaseCronJobError = ResponseError export const useCronTimezoneQuery = <TData = string>( { projectRef, connectionString }: DatabaseCronJobsVariables,
  uses: ResponseError, const, useCronTimezoneQuery, TData

DatabaseCronJobsCountEstimateData (apps/studio/data/database-cron-jobs/database-cron-jobs-count-estimate-query.ts:30-30)
  type alias DatabaseCronJobsCountEstimateData = Awaited<ReturnType<typeof getCronJobsCountEstimate>> export type DatabaseCronJobsCountEstimateError = Error export const useCronJobsCountEstimateQuery = <TData = DatabaseCronJobsCountEstimateData>( { projectRef, connectionString }: DatabaseCronJobsCountEstimateVariables,
  uses: Awaited, ReturnType, getCronJobsCountEstimate, DatabaseCronJobsCountEstimateError

DatabaseCronJobsCountEstimateData (apps/studio/data/database-cron-jobs/database-cron-jobs-count-estimate-query.ts:31-31)
  type alias DatabaseCronJobsCountEstimateData = Awaited<ReturnType<typeof getCronJobsCountEstimate>> export type DatabaseCronJobsCountEstimateError = Error export const useCronJobsCountEstimateQuery = <TData = DatabaseCronJobsCountEstimateData>( { projectRef, connectionString }: DatabaseCronJobsCountEstimateVariables,
  uses: Awaited, ReturnType, getCronJobsCountEstimate, DatabaseCronJobsCountEstimateError

DatabaseCronJobsCountEstimateError (apps/studio/data/database-cron-jobs/database-cron-jobs-count-estimate-query.ts:32-32)
  type alias DatabaseCronJobsCountEstimateError = Error export const useCronJobsCountEstimateQuery = <TData = DatabaseCronJobsCountEstimateData>( { projectRef, connectionString }: DatabaseCronJobsCountEstimateVariables,
  uses: Error, const, useCronJobsCountEstimateQuery, TData

CronJobsCountState (apps/studio/components/interfaces/Integrations/CronJobs/CronJobsTab.useCronJobsData.ts:41-46)
  interface CronJobsCountState

CronJobsFooterProps (apps/studio/components/interfaces/Integrations/CronJobs/CronJobsTab.tsx:182-190)
  interface CronJobsFooterProps

CronJobsGridState (apps/studio/components/interfaces/Integrations/CronJobs/CronJobsTab.useCronJobsData.ts:23-40)
  interface CronJobsGridState

CronJobsTabDataGridProps (apps/studio/components/interfaces/Integrations/CronJobs/CronJobsTab.DataGrid.tsx:9-18)
  interface CronJobsTabDataGridProps

CronJobsTabHeaderProps (apps/studio/components/interfaces/Integrations/CronJobs/CronJobsTab.Header.tsx:5-14)
  interface CronJobsTabHeaderProps

UseCronJobsDataResult (apps/studio/components/interfaces/Integrations/CronJobs/CronJobsTab.useCronJobsData.ts:47-57)
  interface UseCronJobsDataResult

CronJobsEmptyState (apps/studio/components/interfaces/Integrations/CronJobs/CronJobsEmptyState.tsx:1-14)
  sig: CronJobsEmptyState({ page }: { page: string })

CronJobsFooter (apps/studio/components/interfaces/Integrations/CronJobs/CronJobsTab.tsx:191-192)
  sig: CronJobsFooter({ count }: CronJobsFooterProps)

cronJobsCountEstimateKey (apps/studio/data/database-cron-jobs/database-cron-jobs-count-estimate-query.ts:12-29)
  sig: cronJobsCountEstimateKey(projectRef: string | undefined)

navigateToCronJobsPage (e2e/studio/features/cron-jobs.spec.ts:19-22)
  sig: navigateToCronJobsPage(page: Page, ref: string)
  uses: page.goto, page.getByRole

DatabaseCronJobsVariables (apps/studio/data/database-cron-jobs/database-cron-timezone-query.ts:7-7)
  type alias DatabaseCronJobsVariables = {

DatabaseCronJobsVariables (apps/studio/data/database-cron-jobs/database-cron-timezone-query.ts:6-6)
  type alias DatabaseCronJobsVariables = {

DeleteCronJob (apps/studio/components/interfaces/Integrations/CronJobs/DeleteCronJob.tsx:13-109)
  behavior: GUARD(!cronJob -> return null); PRECEDENCE(grid -> not_cronJob)
  uses: parseAsString.withDefault, grid.rows.find, j.jobid.toString, toast.success

SupabaseService.downLoadImage (examples/user-management/angular-user-management/src/app/supabase.service.ts:59-61)
  method SupabaseService.downLoadImage
  sig: SupabaseService.downLoadImage(path: string)
  behavior: DELEGATE(this.supabase.storage.from -> result)
  called_by: SupabaseService
  uses: this.supabase.storage.from

SupabaseService.downLoadImage (examples/user-management/ionic-angular-user-management/src/app/supabase.service.ts:71-73)
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

SupabaseService.signIn (examples/user-management/angular-user-management/src/app/supabase.service.ts:42-44)
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

SupabaseService.updateProfile (examples/user-management/angular-user-management/src/app/supabase.service.ts:50-57)
  method SupabaseService.updateProfile
  sig: SupabaseService.updateProfile(profile: Profile)
  behavior: DELEGATE(this.supabase.from -> result)
  called_by: SupabaseService
  uses: this.supabase.from

-- GAPS
type: RELATIONAL (answerable from L2-L3 structure)
coverage: 80 symbols in L3, 19 with behavior annotations
uncovered: DatabaseCronJobRunsVariables, DatabaseCronJobRunsVariables, DatabaseCronJobRunsVariables, DatabaseCronJobRunsVariables

--- CLUE FILE END ---

QUESTION: How do Supabase Cron jobs execute and interact with other services?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
