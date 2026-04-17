# Enterprise Eval: ent-supabase-rel-2
Date: 2026-04-17

## Question
What ownership and transfer constraints exist around Supabase projects and organizations?

---

## Reasoning Trace
- The most relevant clues are the project-transfer preview and mutation modules, the transfer UI components, and the organization lookup helpers (`ProjectTransferPreviewData`, `apps/studio/data/projects/project-transfer-preview-query.ts:28-30`; `ProjectTransferVariables`, `apps/studio/data/projects/project-transfer-mutation.ts:8-9`; `TransferProjectButton`, `apps/studio/components/interfaces/Settings/General/TransferProjectPanel/TransferProjectButton.tsx:19-290`; `OrganizationsData`, `apps/studio/data/organizations/organization-query.ts:33-35`; `useOrganizationsState`, `apps/studio/components/interfaces/ApiAuthorization/ApiAuthorization.Valid.tsx:48-86`).
- Those entries prove that Studio has an organization-aware project-transfer flow, but they do not expose the exact permission rules or blocker list.

## Answer
The clue supports a **project-transfer workflow that is scoped around organizations**, but most hard constraints are not spelled out.

1. **Projects are transferable through a dedicated flow.** The repository contains both a preview query based on `previewProjectTransfer` and a transfer mutation with `ProjectTransferVariables`, which shows transfer is a first-class operation rather than an ad hoc UI action (`ProjectTransferPreviewData`, `apps/studio/data/projects/project-transfer-preview-query.ts:28-30`; `ProjectTransferVariables`, `apps/studio/data/projects/project-transfer-mutation.ts:8-9`).

2. **The transfer flow is organization-aware.** Organization data is fetched with `useOrganizationQuery({ slug })`, and `useOrganizationsState(organization_slug)` calls `getMatchingOrganization`, so project transfer is framed relative to organization identity rather than only project-local state (`OrganizationsData`, `apps/studio/data/organizations/organization-query.ts:33-35`; `invalidateOrganizationsQuery`, `apps/studio/data/organizations/organization-query.ts:52-55`; `useOrganizationsState`, `apps/studio/components/interfaces/ApiAuthorization/ApiAuthorization.Valid.tsx:48-86`).

3. **A preview step exists before transfer completion.** `TransferProjectButton` uses `projectKeys.projectTransferPreview`, maps over items via `it.id`, and clears cached preview state after success, which strongly suggests Studio computes and shows transfer-related preview data/checks before finishing the transfer (`TransferProjectButton`, `apps/studio/components/interfaces/Settings/General/TransferProjectPanel/TransferProjectButton.tsx:19-290`).

4. **Project roles are part of the broader organization/project model, but the exact transfer rule is not visible.** The clue includes `projectsToAddToRole(...)` in the team-settings role utilities, showing project-specific role assignment exists in the same org/team area, but it does not directly state whether those roles block transfers or must be removed first (`projectsToAddToRole`, `apps/studio/components/interfaces/Organization/TeamSettings/UpdateRolesPanel/UpdateRolesPanel.utils.ts:145-162`).

## Gaps / Unresolved
From the provided clue alone, I cannot determine:
- whether the source actor must be an **owner** of the source organization,
- whether the destination requires mere **membership** or a stronger role,
- whether transfers are restricted by **region**,
- or whether **GitHub integration**, **project-scoped roles**, or **log drains** are explicit transfer blockers.

Those constraints are not exposed in the visible symbol summaries or behavior annotations for this task.
