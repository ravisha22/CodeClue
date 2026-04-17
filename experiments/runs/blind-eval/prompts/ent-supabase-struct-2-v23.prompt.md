# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: ent-supabase-struct-2

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.

--- CLUE FILE (File 1) ---
=CC v2.1 supabase@HEAD 6483mod 21369sym
? How are Supabase branches isolated from the main project and from each other?


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

createProjectSupabaseClient (apps/studio/lib/project-supabase-client.ts:8-29)
  sig: createProjectSupabaseClient(projectRef: string, clientEndpoint: string)

BranchesData (apps/docs/lib/fetch/branches.ts:27-27)
  type alias BranchesData = Awaited<ReturnType<typeof getBranches>> type BranchesError = ResponseError export function useBranchesQuery<TData = BranchesData>( { projectRef }: BranchVariables,
  uses: Awaited, ReturnType, getBranches, BranchesError

BranchesData (apps/studio/data/branches/branches-query.ts:34-34)
  type alias BranchesData = Awaited<ReturnType<typeof getBranches>> export type BranchesError = ResponseError export const useBranchesQuery = <TData = BranchesData>( { projectRef }: BranchesVariables,
  uses: Awaited, ReturnType, getBranches, BranchesError

BranchesData (apps/docs/lib/fetch/branches.ts:26-26)
  type alias BranchesData = Awaited<ReturnType<typeof getBranches>> type BranchesError = ResponseError export function useBranchesQuery<TData = BranchesData>( { projectRef }: BranchVariables,
  uses: Awaited, ReturnType, getBranches, BranchesError

BranchesData (apps/studio/data/branches/branches-query.ts:33-33)
  type alias BranchesData = Awaited<ReturnType<typeof getBranches>> export type BranchesError = ResponseError export const useBranchesQuery = <TData = BranchesData>( { projectRef }: BranchesVariables,
  uses: Awaited, ReturnType, getBranches, BranchesError

BranchesError (apps/studio/data/branches/branches-query.ts:35-35)
  type alias BranchesError = ResponseError export const useBranchesQuery = <TData = BranchesData>( { projectRef }: BranchesVariables,
  uses: ResponseError, const, useBranchesQuery, TData

ProjectBranchSelector (apps/studio/components/layouts/Navigation/NavigationBar/ProjectBranchSelector.tsx:23-117)
  behavior: PRECEDENCE(not_IS_PLATFORM -> isMobile)
  uses: b.project_ref, router.push, displayProject.name

ProjectBranchSelectorPopoverProps (apps/studio/components/layouts/Navigation/NavigationBar/ProjectBranchSelectorPopover.tsx:6-9)
  interface ProjectBranchSelectorPopoverProps

ProjectBranchSelectorSheetProps (apps/studio/components/layouts/Navigation/NavigationBar/ProjectBranchSelectorSheet.tsx:22-35)
  interface ProjectBranchSelectorSheetProps

ProjectBranchSelectorSheetTabTriggerProps (apps/studio/components/layouts/Navigation/NavigationBar/ProjectBranchSelectorSheetTabTrigger.tsx:3-10)
  interface ProjectBranchSelectorSheetTabTriggerProps

ProjectBranchSelectorState (apps/studio/components/layouts/Navigation/NavigationBar/ProjectBranchSelector.utils.ts:3-10)
  interface ProjectBranchSelectorState

ProjectBranchSelectorTriggerProps (apps/studio/components/layouts/Navigation/NavigationBar/ProjectBranchSelectorTrigger.tsx:4-13)
  interface ProjectBranchSelectorTriggerProps

BranchesPageWrapper (apps/studio/pages/project/[ref]/branches/index.tsx:197-250)
  uses: PermissionAction.CREATE, snap.setShowCreateBranchModal, github.com

MainBranchActions (apps/studio/components/interfaces/BranchManagement/Overview.tsx:522-565)
  sig: MainBranchActions({ branch, repo }: { branch: Branch; repo: string })
  uses: PermissionAction.UPDATE

ProjectBranchSelectorPopover (apps/studio/components/layouts/Navigation/NavigationBar/ProjectBranchSelectorPopover.tsx:10-19)
  sig: ProjectBranchSelectorPopover({ onClose }: ProjectBranchSelectorPopoverProps)

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

PauseProjectButton (apps/studio/components/interfaces/Settings/General/Infrastructure/PauseProjectButton.tsx:16-113)
  behavior: GUARD(!canPauseProject -> return toast.error(...)
  uses: PROJECT_STATUS.ACTIVE_UNHEALTHY, PROJECT_STATUS.INACTIVE, PermissionAction.INFRA_EXECUTE, queue_jobs.projects.pause

ProjectPausedState (apps/studio/components/layouts/ProjectLayout/PausedState/ProjectPausedState.tsx:55-361)
  sig: ProjectPausedState({ product }: ProjectPausedStateProps)
  behavior: GUARD(!project -> return toast.error(...); PRECEDENCE(not_canResumeProject -> not_project -> not_showPostgresVersionSel...); TRANSFORM(map)
  uses: Object.values, x.code, PROJECT_STATUS.INACTIVE, pauseStatus.can_restore

ProjectPicker (apps/ui-library/components/tanstack-db-generator/ProjectPicker.tsx:18-190)
  sig: ProjectPicker({ onProjectResolved }: ProjectPickerProps)
  behavior: GUARD(!selectedProject?.ref || isApiKeysPending || isApiKeysErr... -> onProj...); PRECEDENCE(storedMaybeOrgId -> storedOrg -> projects -> default); TRANSFORM(map)
  uses: search.length, pages.flatMap, page.projects, org.id

SupabaseService.downLoadImage (examples/user-management/angular-user-management/src/app/supabase.service.ts:59-61)
  method SupabaseService.downLoadImage
  sig: SupabaseService.downLoadImage(path: string)
  behavior: DELEGATE(this.supabase.storage.from -> result)
  called_by: SupabaseService
  uses: this.supabase.storage.from

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 83 symbols in L3, 46 with behavior annotations
uncovered: toOrgProjectValue, useGetProjectPermissions, useInvalidateProjectDetailsQuery, useIsProjectActive
drill: apps/studio/lib/project-supabase-client.ts (~13 lines, createProjectSupabaseClient)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## createProjectSupabaseClient  (apps/studio/lib/project-supabase-client.ts L8-29)
```
export async function createProjectSupabaseClient(projectRef: string, clientEndpoint: string) {
  try {
    const { apiKey } = await getOrRefreshTemporaryApiKey(projectRef)

    return createClient(clientEndpoint, apiKey, {
      auth: {
        persistSession: false,
        autoRefreshToken: false,
        detectSessionInUrl: false,
        storage: {
          getItem: (key) => {
            return null
          },
          setItem: (key, value) => {},
          removeItem: (key) => {},
        },
      },
    })
  } catch (error) {
    throw error
  }
}
```
--- END SOURCE SNIPPETS ---

QUESTION: How are Supabase branches isolated from the main project and from each other?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
