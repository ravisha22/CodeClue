# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: ent-supabase-mech-1

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.

--- CLUE FILE (File 1) ---
=CC v2.1 supabase@HEAD 6483mod 21369sym
? How does Realtime move database changes and broadcasts from Postgres to clients?


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

RealtimeInspectorDatabaseRoleUpdatedEvent (packages/common/telemetry-constants.ts:511-516)
  interface RealtimeInspectorDatabaseRoleUpdatedEvent

IconDatabaseChanges (packages/ui/src/components/Icon/icons/IconDatabaseChanges/IconDatabaseChanges.tsx:31-34)
  sig: IconDatabaseChanges(props: any)

DatabaseQueueData (apps/studio/data/database-queues/database-queues-query.ts:31-31)
  type alias DatabaseQueueData = PostgresQueue[] export type DatabaseQueueError = ResponseError export const useQueuesQuery = <TData = DatabaseQueueData>( { projectRef, connectionString }: DatabaseQueuesVariables,
  uses: PostgresQueue, DatabaseQueueError, ResponseError, const

DatabaseQueueData (apps/studio/data/database-queues/database-queue-messages-infinite-query.ts:81-81)
  type alias DatabaseQueueData = PostgresQueueMessage[] export type DatabaseQueueError = ResponseError export const useQueueMessagesInfiniteQuery = <TData = DatabaseQueueData>( { projectRef, connectionString, queueName, status }: DatabaseQueueVariables,
  uses: PostgresQueueMessage, DatabaseQueueError, ResponseError, const

DatabaseQueueData (apps/studio/data/database-queues/database-queues-query.ts:32-32)
  type alias DatabaseQueueData = PostgresQueue[] export type DatabaseQueueError = ResponseError export const useQueuesQuery = <TData = DatabaseQueueData>( { projectRef, connectionString }: DatabaseQueuesVariables,
  uses: PostgresQueue, DatabaseQueueError, ResponseError, const

DatabaseQueueData (apps/studio/data/database-queues/database-queue-messages-infinite-query.ts:82-82)
  type alias DatabaseQueueData = PostgresQueueMessage[] export type DatabaseQueueError = ResponseError export const useQueueMessagesInfiniteQuery = <TData = DatabaseQueueData>( { projectRef, connectionString, queueName, status }: DatabaseQueueVariables,
  uses: PostgresQueueMessage, DatabaseQueueError, ResponseError, const

DatabaseQueuesMetricsData (apps/studio/data/database-queues/database-queues-metrics-query.ts:83-83)
  type alias DatabaseQueuesMetricsData = PostgresQueueMetric export type DatabaseQueuesMetricsError = ResponseError export const useQueuesMetricsQuery = <TData = DatabaseQueuesMetricsData>( { projectRef, connectionString, queueName }: DatabaseQueuesMetricsVariables,
  uses: PostgresQueueMetric, DatabaseQueuesMetricsError, ResponseError, const

DatabaseQueuesMetricsData (apps/studio/data/database-queues/database-queues-metrics-query.ts:84-84)
  type alias DatabaseQueuesMetricsData = PostgresQueueMetric export type DatabaseQueuesMetricsError = ResponseError export const useQueuesMetricsQuery = <TData = DatabaseQueuesMetricsData>( { projectRef, connectionString, queueName }: DatabaseQueuesMetricsVariables,
  uses: PostgresQueueMetric, DatabaseQueuesMetricsError, ResponseError, const

DatabaseExtension (apps/studio/data/database-extensions/database-extensions-query.ts:10-10)
  type alias DatabaseExtension = components['schemas']['PostgresExtension'] & {
  uses: components, schemas, PostgresExtension

DatabaseExtension (apps/studio/data/database-extensions/database-extensions-query.ts:11-11)
  type alias DatabaseExtension = components['schemas']['PostgresExtension'] & {
  uses: components, schemas, PostgresExtension

Database (examples/edge-functions/supabase/functions/kysely-postgres/index.ts:22-26)
  interface Database

PostgresTrigger (apps/studio/components/interfaces/Database/Triggers/TriggersList/TriggerList.utils.ts:1-15)
  interface PostgresTrigger

RealtimeInspectorBroadcastSentEvent (packages/common/telemetry-constants.ts:463-468)
  interface RealtimeInspectorBroadcastSentEvent

applyChanges (apps/studio/pages/project/[ref]/database/column-privileges.tsx:202-205)

handleMouseMove (apps/www/components/Products/RealtimeVisual.tsx:15-36)
  sig: handleMouseMove(event: React.MouseEvent<HTMLDivElement>)
  uses: React.MouseEvent, cardRef.current, cardRef.current.getBoundingClientRect, event.clientX

PostgresQueue (apps/studio/data/database-queues/database-queues-query.ts:12-12)
  type alias PostgresQueue = {

PostgresQueue (apps/studio/data/database-queues/database-queues-query.ts:11-11)
  type alias PostgresQueue = {

PostgresQueueMessage (apps/studio/data/database-queues/database-queue-messages-infinite-query.ts:20-20)
  type alias PostgresQueueMessage = {

PostgresQueueMessage (apps/studio/data/database-queues/database-queue-messages-infinite-query.ts:19-19)
  type alias PostgresQueueMessage = {

PostgresQueueMetric (apps/studio/data/database-queues/database-queues-metrics-query.ts:14-14)
  type alias PostgresQueueMetric = {

PostgresQueueMetric (apps/studio/data/database-queues/database-queues-metrics-query.ts:15-15)
  type alias PostgresQueueMetric = {

updateTableRealtime (apps/studio/components/interfaces/TableGridEditor/SidePanelEditor/SidePanelEditor.tsx:469-557)
  sig: updateTableRealtime(table: RetrieveTableResult, enabled: boolean)
  behavior: PRECEDENCE(realtimePublication); TRANSFORM(map)
  uses: console.error, pub.name, table.schema, table.name

useRealtimeMessages (apps/studio/components/interfaces/Realtime/Inspector/useRealtimeMessages.ts:56-241)
  sig: useRealtimeMessages(config: RealtimeConfig, setRealtimeConfig: Dispatch<SetSt...)
  behavior: GUARD(!enabled -> return); PRECEDENCE(not_enabled -> bearer -> not_client -> default)
  uses: supabase.co, realtimeClient.setAuth, realtimeClient.disconnect, newChannel.on

RealtimeFilterPopover (apps/studio/components/interfaces/Realtime/Inspector/RealtimeFilterPopover/index.tsx:34-260)
  sig: RealtimeFilterPopover({ config, onChangeConfig }: RealtimeFilterPopoverProps)
  uses: publication.name, config.table, tempConfig.enablePresence, tempConfig.enableBroadcast

RealtimePage (apps/www/pages/realtime.tsx:46-248)
  uses: supabase.com, supabase.com$, og.jpg, PRODUCT_NAMES.REALTIME

a.PrettifyChanges (apps/studio/public/monaco-editor/base/worker/workerMain.js:4175-4278)
  method a.PrettifyChanges
  sig: a.PrettifyChanges(e)
  behavior: ACCUMULATE(PrettifyChanges loop -> result)
  calls: ChangesOverlap, ElementsAreStrictEqual, ModifiedElementsAreEqual, OriginalElementsAreEqual, _boundaryScore, _findBetterContiguousSequence
  called_by: _ComputeDiff, a
  uses: e.length, this._originalElementsOrHash.length, this._modifiedElementsOrHash.length, f.originalLength

Database (apps/www/pages/database.tsx:39-386)
  uses: dashboardSwiper.slideTo, supabase.com, supabase.com$, og.jpg

DatabaseConnectionString (apps/studio/components/interfaces/Connect/DatabaseConnectionString.tsx:67-637)
  behavior: TRANSFORM(map)
  uses: parseAsString.withDefault, DATABASE_CONNECTION_TYPES.map, t.id, validTypes.includes

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 83 symbols in L3, 12 with behavior annotations
uncovered: DatabaseQueueError, DatabaseQueueError, DatabaseQueueError, DatabaseQueueVersionData
drill: packages/ui/src/components/Icon/icons/IconDatabaseChanges/IconDatabaseChanges.tsx (~3 lines, IconDatabaseChanges)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## IconDatabaseChanges  (packages/ui/src/components/Icon/icons/IconDatabaseChanges/IconDatabaseChanges.tsx L31-34)
```

function IconDatabaseChanges(props: any) {
  return <IconBase src={<SvgComponent />} viewBox="0 0 25 24" {...props} />
}
```

## SvgComponent  (packages/ui/src/components/Icon/icons/IconPresence/IconPresence.tsx L4-10)
```

const SvgComponent = () => (
  <>
    <path
      stroke="currentColor"
      strokeLinejoin="round"
      strokeMiterlimit={10}
```
--- END SOURCE SNIPPETS ---

QUESTION: How does Realtime move database changes and broadcasts from Postgres to clients?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
