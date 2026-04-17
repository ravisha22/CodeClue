# Enterprise v2: ent-supabase-rel-2
Date: 2026-04-17

## Question
What ownership and transfer constraints exist around Supabase projects and organizations?

## Reasoning

### Relevant Clue Entries

**Project transfer data types (FOCUS):**
- `ProjectTransferPreviewVariables` at `apps/studio/data/projects/project-transfer-preview-query.ts:6-7` is a type alias for the variables required to preview a project transfer (FOCUS: `ProjectTransferPreviewVariables`).
- `ProjectTransferPreviewData` at `apps/studio/data/projects/project-transfer-preview-query.ts:28-29` is typed as `Awaited<ReturnType<typeof previewProjectTransfer>>` and uses `previewProjectTransfer` (FOCUS: `ProjectTransferPreviewData`). This indicates a **preview step** exists before executing a transfer, allowing users to see the consequences of a transfer before committing.
- `ProjectTransferPreviewError` at the same file (line 30) is a distinct error type, indicating the preview operation can fail with specific error conditions (FOCUS: `ProjectTransferPreviewError`).
- `ProjectTransferVariables` at `apps/studio/data/projects/project-transfer-mutation.ts:8-9` is the type alias for the actual transfer mutation variables (FOCUS: `ProjectTransferVariables`). The separation of preview query and transfer mutation confirms a **two-step transfer process**: preview first, then execute.

**Transfer UI component (FOCUS):** `TransferProjectButton` at `apps/studio/components/interfaces/Settings/General/TransferProjectPanel/TransferProjectButton.tsx:19-290` has `behavior: TRANSFORM(map)` and uses `it.id`, `toast.success`, `queryClient.removeQueries`, and `projectKeys.projectTransferPreview` (FOCUS: `TransferProjectButton`). Key observations:
- It references `projectKeys.projectTransferPreview`, linking back to the preview query — the UI calls the preview before enabling the transfer action.
- On success, it shows `toast.success` and calls `queryClient.removeQueries`, indicating cached project data is invalidated after transfer (the project's ownership context has changed).
- The use of `it.id` within a `map` transform suggests iteration over a list (likely target organizations).

**Transfer panel (FOCUS):** `TransferProjectPanel` at `apps/studio/components/interfaces/Settings/General/TransferProjectPanel/TransferProjectPanel.tsx:14-50` is the container panel for the transfer functionality, located under Settings > General, indicating project transfer is a project-level administrative operation (FOCUS: `TransferProjectPanel`).

**Organization data layer (FOCUS):**
- `OrganizationsData` at `apps/studio/data/organizations/organization-query.ts:33-34` is typed as `Awaited<ReturnType<typeof getOrganization>>` with `OrganizationsError` as `ResponseError` (FOCUS: `OrganizationsData`). Organizations are fetched by `slug` via `OrganizationVariables` (FOCUS: `OrganizationsData` uses chain).
- `OrganizationsError` at the same file (line 35) uses `ResponseError` (FOCUS: `OrganizationsError`).
- `invalidateOrganizationsQuery` at `apps/studio/data/organizations/organization-query.ts:52-55` delegates to `client.invalidateQueries` using `organizationKeys.list` (FOCUS: `invalidateOrganizationsQuery`). This function would be called when organization membership changes (e.g., after a project transfer), ensuring the organization list is refreshed.

**Role-based access within organizations (FOCUS):** `projectsToAddToRole` at `apps/studio/components/interfaces/Organization/TeamSettings/UpdateRolesPanel/UpdateRolesPanel.utils.ts:145-162` operates on `groupByAddedRoles[role.base_role_id]?.map((r) ...)` and uses `toUpdate.push`, `role.id` (FOCUS: `projectsToAddToRole`). This reveals:
- Organizations have **role-based team settings** with roles identified by `base_role_id`.
- Projects can be **assigned to roles** within an organization, meaning access to projects is governed by organizational role membership.
- The function maps added roles to projects, suggesting a constraint: when a project is transferred to an organization, it must be assigned appropriate roles for team members.

**Empty states (FOCUS):**
- `NoOrganizationsState` at `apps/studio/components/interfaces/Home/ProjectList/EmptyStates.tsx:94-106` renders when a user has no organizations (FOCUS: `NoOrganizationsState`).
- `NoProjectsState` at the same file (lines 76-93) takes `{ slug: string }` and renders when an organization (identified by slug) has no projects (FOCUS: `NoProjectsState`). The fact that `NoProjectsState` is scoped by organization slug confirms projects belong to an organization.

**Client creation per project (FOCUS):** `createProjectSupabaseClient` at `apps/studio/lib/project-supabase-client.ts:8-29` takes `projectRef` and `clientEndpoint` (FOCUS: `createProjectSupabaseClient`), confirming each project has a unique reference identifier.

### Synthesis

Based on the clue, the following ownership and transfer constraints exist:

1. **Projects belong to organizations:** Projects are listed within an organization context (`NoProjectsState` accepts a `slug` parameter) (FOCUS: `NoProjectsState`). Organizations are identified by `slug` (FOCUS: `OrganizationsData`). Each project has a unique `projectRef` (FOCUS: `createProjectSupabaseClient`).

2. **Two-step transfer process:** Transferring a project requires:
   - **Step 1 — Preview:** A preview query (`previewProjectTransfer`) is called with `ProjectTransferPreviewVariables` to evaluate the transfer's feasibility and consequences (FOCUS: `ProjectTransferPreviewData`, `ProjectTransferPreviewVariables`).
   - **Step 2 — Execute:** The actual transfer mutation uses `ProjectTransferVariables` (FOCUS: `ProjectTransferVariables`, `project-transfer-mutation.ts:8-9`).
   The preview can fail with `ProjectTransferPreviewError` (FOCUS: `ProjectTransferPreviewError`), implying there are validation constraints that may block a transfer.

3. **Cache invalidation on transfer:** After a successful transfer, `queryClient.removeQueries` is called (FOCUS: `TransferProjectButton`), and `invalidateOrganizationsQuery` exists to refresh organization data (FOCUS: `invalidateOrganizationsQuery`). This ensures the UI reflects the new ownership.

4. **Transfer is an admin-level setting:** The transfer panel is located under `Settings/General/TransferProjectPanel/` (FOCUS: `TransferProjectPanel`), indicating it is an administrative operation within project settings — not a casual action.

5. **Role-based project access in organizations:** Projects within an organization are governed by roles (`projectsToAddToRole` maps projects to roles identified by `base_role_id`) (FOCUS: `projectsToAddToRole`). When a project is transferred to a new organization, it would need to be integrated into that organization's role structure.

6. **Organization membership is required:** The `NoOrganizationsState` component (FOCUS: `NoOrganizationsState`) indicates users must belong to an organization to manage projects. Projects cannot exist outside an organizational context.

### Gaps and Uncertainties

- **GAPS type is STRUCTURAL** with 83 symbols at L3 and 27 with behavior annotations. Uncovered symbols include `SupabaseClient` (listed multiple times) and `SupabaseJsResult` (GAPS). The internal implementation of the Supabase client used during transfer operations cannot be determined.
- The specific **validation constraints** checked during `previewProjectTransfer` (e.g., billing tier compatibility, project status requirements, organization capacity limits) are not visible in the clue.
- Whether transfer changes the project's `projectRef` or `clientEndpoint` is not determinable.
- The **permission level** required to initiate a transfer (which `PermissionAction` is checked) is not shown in the FOCUS entries for the transfer components.
- Whether a project can be transferred to a **personal account** vs. only to another organization is not determinable from the clue.
- The SupabaseService examples in the FOCUS section are from example apps and do not directly relate to transfer constraints — they illustrate the general client interaction pattern but not ownership mechanics.
