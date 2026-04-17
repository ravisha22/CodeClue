# Enterprise Eval: ent-supabase-struct-2
Date: 2026-04-17

## Question
How are Supabase branches isolated from the main project and from each other?

---

## Reasoning Trace
- The most relevant evidence is `createProjectSupabaseClient(projectRef, clientEndpoint)`, the branch query types keyed by `projectRef`, and the branch selector UI that routes using `b.project_ref`.
- That supports per-branch/project-ref clients and credentials, but the clue does not spell out the full lifecycle or all isolated resources.

## Answer
The clue supports **credential and client isolation per branch/project reference**, but only part of the full branch-isolation story is visible.

1. **Branch access is keyed by a project/branch reference.** Branch queries are parameterized by `projectRef`, and the branch selector routes using `b.project_ref`, which indicates the system addresses branches as distinct project-ref targets rather than as one shared mutable environment (`BranchesData`, `apps/studio/data/branches/branches-query.ts:33-35`; `ProjectBranchSelector`, `apps/studio/components/layouts/Navigation/NavigationBar/ProjectBranchSelector.tsx:23-117`).

2. **Each branch/project-ref gets its own client endpoint and temporary API key.** `createProjectSupabaseClient(projectRef, clientEndpoint)` calls `getOrRefreshTemporaryApiKey(projectRef)` and then creates a client with that `clientEndpoint` plus returned `apiKey`. That is strong evidence that branch access is isolated through branch-specific connection parameters and credentials rather than a single shared client (`createProjectSupabaseClient`, `apps/studio/lib/project-supabase-client.ts:8-29`, source snippet lines 261-278).

3. **Auth/session state is intentionally not shared by that branch client.** The same snippet disables `persistSession`, `autoRefreshToken`, and `detectSessionInUrl`, and its storage adapter is effectively a no-op (`getItem` returns `null`; `setItem`/`removeItem` do nothing). That implies the temporary branch client is meant to stay isolated instead of reusing stored auth state across environments (`createProjectSupabaseClient`, source snippet lines 265-277).

4. **Branches are managed as separate selectable/createable environments in Studio.** The presence of `useBranchesQuery`, `ProjectBranchSelector`, and `BranchesPageWrapper` with `snap.setShowCreateBranchModal` shows Studio treats branches as first-class managed units that can be created and switched between (`BranchesData`, `apps/studio/data/branches/branches-query.ts:33-35`; `ProjectBranchSelector`, `apps/studio/components/layouts/Navigation/NavigationBar/ProjectBranchSelector.tsx:23-117`; `BranchesPageWrapper`, `apps/studio/pages/project/[ref]/branches/index.tsx:197-250`).

## Gaps / Unresolved
The clue does **not** establish whether preview branches are ephemeral, whether persistent branches are recommended for staging/QA/dev, whether new branches start data-less, or exactly which resources are isolated (database data, storage objects, Edge Functions, auth config). The `GAPS` section explicitly says this task is mechanistic and only drills into `createProjectSupabaseClient`, so the broader branch lifecycle cannot be determined from the provided evidence alone (`GAPS`; `createProjectSupabaseClient`, source snippet).
