# Enterprise v2: ent-supabase-struct-2
Date: 2026-04-17

## Question
How are Supabase branches isolated from the main project and from each other?

## Reasoning

### Relevant Clue Entries

**Branch data layer (FOCUS):** Multiple type aliases named `BranchesData` are defined in both `apps/docs/lib/fetch/branches.ts:26-27` and `apps/studio/data/branches/branches-query.ts:33-34`. Both are typed as `Awaited<ReturnType<typeof getBranches>>` and reference `BranchesError` as `ResponseError` (FOCUS: `BranchesData`, `apps/studio/data/branches/branches-query.ts:33-34`; `BranchesData`, `apps/docs/lib/fetch/branches.ts:26-27`). The query is parameterized by `projectRef` via `BranchesVariables`/`BranchVariables`, indicating branches are scoped to a specific project (FOCUS: `BranchesData` uses `getBranches`; query hooks accept `{ projectRef }`).

**Branch UI selectors (FOCUS):** Several UI components manage branch selection:
- `ProjectBranchSelector` in `apps/studio/components/layouts/Navigation/NavigationBar/ProjectBranchSelector.tsx:23-117` exhibits `behavior: PRECEDENCE(not_IS_PLATFORM -> isMobile)` and uses `b.project_ref`, `router.push`, `displayProject.name` (FOCUS: `ProjectBranchSelector`). This shows branches are selected within the context of a project reference, and the selector navigates the user to a branch-specific view.
- `ProjectBranchSelectorPopover` accepts `ProjectBranchSelectorPopoverProps` with an `onClose` callback (FOCUS: `ProjectBranchSelectorPopover`, `ProjectBranchSelectorPopoverProps`).
- `ProjectBranchSelectorSheet` has props defined in `ProjectBranchSelectorSheetProps` (FOCUS: `ProjectBranchSelectorSheetProps`, lines 22-35).
- `ProjectBranchSelectorTrigger` has props at `ProjectBranchSelectorTriggerProps` (FOCUS: `ProjectBranchSelectorTriggerProps`, lines 4-13).
- `ProjectBranchSelectorState` (interface at lines 3-10) holds the branch selector's internal state (FOCUS: `ProjectBranchSelectorState`).

**Branches management page (FOCUS):** `BranchesPageWrapper` in `apps/studio/pages/project/[ref]/branches/index.tsx:197-250` uses `PermissionAction.CREATE` and `snap.setShowCreateBranchModal` and references `github.com` (FOCUS: `BranchesPageWrapper`). This indicates:
1. Creating branches requires a specific permission (`PermissionAction.CREATE`).
2. Branch creation is tied to GitHub integration (the `github.com` reference).
3. The page is nested under `project/[ref]/branches/`, meaning branches live within a project's namespace.

**Main branch actions (FOCUS):** `MainBranchActions` in `apps/studio/components/interfaces/BranchManagement/Overview.tsx:522-565` takes `{ branch: Branch; repo: string }` and uses `PermissionAction.UPDATE` (FOCUS: `MainBranchActions`). This shows the main branch has distinct management actions gated by update permissions, and is associated with a repository string.

**Per-branch client isolation via createProjectSupabaseClient (Source Snippet):** The drilled-down source for `createProjectSupabaseClient` in `apps/studio/lib/project-supabase-client.ts:8-29` reveals:
```typescript
export async function createProjectSupabaseClient(projectRef: string, clientEndpoint: string) {
  const { apiKey } = await getOrRefreshTemporaryApiKey(projectRef)
  return createClient(clientEndpoint, apiKey, {
    auth: {
      persistSession: false,
      autoRefreshToken: false,
      detectSessionInUrl: false,
      storage: { getItem: (key) => null, setItem: (key, value) => {}, removeItem: (key) => {} },
    },
  })
}
```
Key isolation mechanisms visible here:
- Each client is created with a **project-specific `clientEndpoint`** and a **temporary API key** obtained via `getOrRefreshTemporaryApiKey(projectRef)` (Source Snippet: `createProjectSupabaseClient`).
- Session persistence is explicitly **disabled** (`persistSession: false`), auto-refresh is off, URL session detection is off, and the storage adapter is a no-op (Source Snippet). This ensures each client connection is stateless and cannot leak session state between branches or projects.

**Project state management (FOCUS):** `PauseProjectButton` in `apps/studio/components/interfaces/Settings/General/Infrastructure/PauseProjectButton.tsx:16-113` guards on `!canPauseProject` and uses `PROJECT_STATUS.ACTIVE_UNHEALTHY`, `PROJECT_STATUS.INACTIVE`, and `queue_jobs.projects.pause` (FOCUS: `PauseProjectButton`). `ProjectPausedState` uses `pauseStatus.can_restore` (FOCUS: `ProjectPausedState`). These suggest branches may inherit project-level lifecycle states (pause/resume), but the exact per-branch lifecycle is not detailed.

### Synthesis

Based on the clue and source snippets, Supabase branches are isolated from the main project and each other through the following mechanisms:

1. **Project-scoped namespace:** Branches are fetched per-project via `getBranches` parameterized by `projectRef` (FOCUS: `BranchesData` at `branches-query.ts:33-34`). The management page lives at `project/[ref]/branches/` (FOCUS: `BranchesPageWrapper`), confirming branches are namespaced under a project reference.

2. **Distinct client endpoints:** `createProjectSupabaseClient` creates a Supabase client using a unique `clientEndpoint` per project/branch and a temporary API key scoped to that `projectRef` (Source Snippet: `createProjectSupabaseClient`, `apps/studio/lib/project-supabase-client.ts:8-29`). This means each branch can have its own API endpoint, achieving network-level isolation.

3. **Stateless, non-persisted sessions:** The client configuration explicitly disables session persistence, auto-refresh, and URL detection, with a no-op storage backend (Source Snippet: `createProjectSupabaseClient`). This prevents cross-contamination of authentication state between branch clients.

4. **Temporary, per-project API keys:** The `getOrRefreshTemporaryApiKey(projectRef)` call provides a scoped, temporary credential for each branch/project connection (Source Snippet: `createProjectSupabaseClient`). This means each branch operates with its own short-lived key, not a shared long-lived credential.

5. **Permission-gated branch operations:** Creating branches requires `PermissionAction.CREATE` (FOCUS: `BranchesPageWrapper`), and managing the main branch requires `PermissionAction.UPDATE` (FOCUS: `MainBranchActions`). This provides authorization-level isolation of branch lifecycle operations.

6. **GitHub integration:** The `BranchesPageWrapper` references `github.com` and `MainBranchActions` accepts a `repo` parameter (FOCUS: `BranchesPageWrapper`, `MainBranchActions`). This suggests branches may map to Git branches in a linked GitHub repository, providing version-control-level isolation.

### Gaps and Uncertainties

- **GAPS declares type MECHANISTIC**, indicating body logic is needed for a full answer. The clue covers 83 symbols at L3 with 46 behavior annotations but lists `toOrgProjectValue`, `useGetProjectPermissions`, `useInvalidateProjectDetailsQuery`, `useIsProjectActive` as uncovered (GAPS). The permission-checking logic and project-active state checks that may gate branch operations cannot be fully traced.
- The clue does not reveal whether each branch gets its own **isolated Postgres database** (separate schema, separate instance, or separate logical database). The database-level isolation mechanism is not determinable from the available evidence.
- The drill target was `createProjectSupabaseClient` (~13 lines), and the source confirms client-level isolation, but **server-side** branch isolation (e.g., separate containers, separate database schemas) is not documented in the clue.
- How branches relate to specific Git branches in the linked repository beyond the surface-level GitHub reference is not determinable.
