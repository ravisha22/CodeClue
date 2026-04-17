# Enterprise v2: ent-mattermost-rel-2
Date: 2026-04-17

## Reasoning Scaffold

### 1. Relevant Clue Entries

The question asks which admin and compliance gates span channel discovery and team deletion.

**FOCUS – App.ValidateTeamScopePolicyChannelAssignment** (server/channels/app/team_access_control.go:247):
- "validates that all channels are eligible for team policy assignment, is the gat…"
- Behavior: `GUARD(len(channelIDs) == 0 -> return model.NewApp...); PRECEDENCE(len -> appErr); ACCUMULATE(NewAppError loop -> result)`
- Calls: `GetChannels`
- Called by: `assignAccessPolicy`

**FOCUS – App.GetTeamSchemeChannelRoles** (server/channels/app/channel.go:1030):
- "Checks if a team has an override scheme and returns the scheme channel role names or default c…"
- Calls: `GetTeam`, `GetScheme`
- Called by: `GetChannelModerationsForChannel`, `GetSchemeRolesForChannel`, `PatchChannelModerationsForChannel`

**FOCUS – App.GetUsersInChannelPageByAdmin** (server/channels/app/user.go:734):
- Calls: `GetUsersInChannelByAdmin`, `sanitizeProfiles`
- Called by: `getUsers`

**FOCUS – App.GetUsersInChannelByAdmin** (server/channels/app/user.go:693):
- Calls: `Srv`
- Called by: `GetUsersInChannelPageByAdmin`

**FOCUS – App.RemoveUsersFromChannelNotMemberOfTeam** (server/channels/app/channel.go:3568):
- Calls: `GetChannelMembersPage`, `removeUserFromChannel`, `GetTeamMembersByIds`
- Called by: `moveChannel`, `localMoveChannel`, `MoveChannel`

**FOCUS – RetentionPolicyWithTeamAndChannelIDs** (server/public/model/data_retention_policy.go:19):
- Type with `Auditable` method
- Called by (Auditable): `Auditable`, `AddEventParameterAuditableToAuditRec`, `LogClone`

**FOCUS – RetentionPolicyWithTeamAndChannelCounts** (server/public/model/data_retention_policy.go:33):
- Type with `Auditable` method

**FOCUS – RetentionPolicyWithTeamAndChannelCountsList** (server/public/model/data_retention_policy.go:57):
- Type

**FOCUS – copyRetentionPolicyWithTeamAndChannelIds** (server/channels/store/storetest/retention_policy_store.go:79):
- Called by: `testRetentionPolicyStoreAddChannels`, `testRetentionPolicyStoreAddTeams`, `testRetentionPolicyStorePatch`, `testRetentionPolicyStoreRemoveChannels`, `testRetentionPolicyStoreRemoveTeams`

**FOCUS – TimerLayerChannelStore.PermanentDeleteByTeam** (server/channels/store/timerlayer/timerlayer.go:2581):
- Called by: `PermanentDeleteByTeam`

**FOCUS – TimerLayerChannelStore.GetPublicChannelsByIdsForTeam** (server/channels/store/timerlayer/timerlayer.go:2220):
- Called by: `getPublicChannelsByIdsForTeam`

**FOCUS – App.GetChannelMembersWithTeamDataForUserWithPagination** (server/channels/app/channel.go:2437):
- Calls: `Srv`
- Called by: `getChannelMembersForUser`

**FOCUS – App.buildUserTeamAndChannelMemberships** (server/channels/app/export.go:632):
- Behavior: `GUARD(err != nil -> return nil, model.N...); ACCUMULATE(importUserTeamDataFro... -> memberships)`
- Calls: `Srv`, `buildUserChannelMemberships`
- Called by: `exportAllUsers`

**FOCUS – App.resolveTeamSyncChannelIDs** (server/channels/app/job.go:154):
- "returns channel IDs the requester can sync, filtered by self-inclusion (same logic as SearchTe…)"
- Behavior: `GUARD(appErr != nil -> return nil, appErr); ACCUMULATE(loop -> channelIDs id)`
- Calls: `SearchTeamAccessPolicies`
- Called by: `CreateAccessControlSyncJob`

**FOCUS – ChannelWithTeamData** (server/public/model/channel.go:137): Type
**FOCUS – ChannelMemberWithTeamData** (server/public/model/channel_member.go:106): "contains ChannelMember appended with extra team information as well."
**FOCUS – GroupsAssociatedToChannelWithSchemeAdmin** (server/public/model/group.go:101): Type
**FOCUS – channelMemberWithTeamWithSchemeRoles** (server/channels/store/sqlstore/channel_store.go:97): Type with `ToModel` method

**INDEX – server/channels/app/authorization.go** (675L): `HasPermissionTo`, `HasPermissionToChannel`, `HasPermissionToChannelByPost`, `HasPermissionToChannelMemberCount`, `HasPermissionToEditPropertyField`

**INDEX – server/channels/app/audit.go** (235L): `AddAuditLogCertificate`, `GetAudits`, `GetAuditsPage`, `LogAuditRec`, `LogAuditRecWithLevel`

### 2. Tracing the Gates

**Gate 1: Access Control Policy — Channel Assignment Validation**

`App.ValidateTeamScopePolicyChannelAssignment` (team_access_control.go:247) is described as a "gat[e]" that validates channels are eligible for team policy assignment. It GUARDs on empty channel IDs, then accumulates errors per channel. It is called by `assignAccessPolicy`, linking it directly to the access control policy assignment flow.

`App.resolveTeamSyncChannelIDs` (job.go:154) filters which channels a requester can sync, using `SearchTeamAccessPolicies`. Called by `CreateAccessControlSyncJob`, this gates which channels are included in access control synchronization at the team scope.

**Gate 2: Team Scheme → Channel Role Overrides**

`App.GetTeamSchemeChannelRoles` (channel.go:1030) checks whether a team has an override scheme and returns the corresponding channel role names. It is called by `GetChannelModerationsForChannel`, `GetSchemeRolesForChannel`, and `PatchChannelModerationsForChannel`. This is an admin gate that controls channel moderation settings based on team-level scheme configuration.

**Gate 3: Retention Policies Spanning Teams and Channels**

The data retention compliance types span both scopes:
- `RetentionPolicyWithTeamAndChannelIDs` (data_retention_policy.go:19) and `RetentionPolicyWithTeamAndChannelCounts` (data_retention_policy.go:33) both implement `Auditable`, and their `Auditable` method is called by `AddEventParameterAuditableToAuditRec` and `LogClone` — connecting retention policies to the audit trail.
- `copyRetentionPolicyWithTeamAndChannelIds` (retention_policy_store.go:79) is used in tests for adding/removing channels and teams from retention policies (`testRetentionPolicyStoreAddChannels`, `testRetentionPolicyStoreAddTeams`, `testRetentionPolicyStoreRemoveChannels`, `testRetentionPolicyStoreRemoveTeams`), confirming that a single retention policy can govern both team and channel data lifecycle.

**Gate 4: Admin-Scoped Channel Discovery**

`App.GetUsersInChannelPageByAdmin` (user.go:734) calls `GetUsersInChannelByAdmin` (user.go:693) and `sanitizeProfiles`. The "ByAdmin" suffix indicates an admin-privileged path for channel member discovery that applies profile sanitization as a compliance measure.

`TimerLayerChannelStore.GetPublicChannelsByIdsForTeam` (timerlayer.go:2220) scopes public channel discovery to a team, called by `getPublicChannelsByIdsForTeam`.

**Gate 5: Team Deletion and Channel Cascade**

`TimerLayerChannelStore.PermanentDeleteByTeam` (timerlayer.go:2581) permanently deletes channels by team ID, called by `PermanentDeleteByTeam`. This is the cascade gate: when a team is permanently deleted, its channels are bulk-deleted.

`App.RemoveUsersFromChannelNotMemberOfTeam` (channel.go:3568) removes channel members who are not members of the target team. It calls `GetChannelMembersPage`, `removeUserFromChannel`, and `GetTeamMembersByIds`. Called by `moveChannel`, `localMoveChannel`, and `MoveChannel`, this enforces the invariant that channel membership requires team membership — a gate exercised during channel moves and, by extension, team restructuring.

**Gate 6: Export/Audit Trail**

`App.buildUserTeamAndChannelMemberships` (export.go:632) builds combined team-and-channel membership data for export, calling `buildUserChannelMemberships`. Called by `exportAllUsers`, this provides the compliance export gate spanning both scopes.

The audit module (`server/channels/app/audit.go`, INDEX) with `LogAuditRec`, `LogAuditRecWithLevel`, `GetAudits`, `GetAuditsPage`, and `AddAuditLogCertificate` provides the auditing infrastructure. The `Auditable` interface on retention policy types connects retention policy changes to this audit system.

### 3. GAPS — What Cannot Be Determined

The GAPS section states:
- **Type**: STRUCTURAL (answerable from L0-L2)
- **Coverage**: 83 symbols in L3, 13 with behavior annotations
- **Uncovered**: `SqlChannelStore.SearchInTeam`, `SqlChannelStore.autocompleteInTeamForSearchDirectMessages`, `SqlChannelStore.buildAutocompleteInTeamQuery`, `SqlRoleStore.ChannelRolesUnderTeamRole`

From the clue alone, we **cannot determine**:
- How `SqlChannelStore.SearchInTeam` implements channel discovery search within a team (uncovered) — this is a key channel discovery mechanism whose permission checks are unknown
- How `SqlChannelStore.autocompleteInTeamForSearchDirectMessages` gates DM channel discovery (uncovered)
- How `SqlRoleStore.ChannelRolesUnderTeamRole` maps team roles to channel roles (uncovered) — this would complete the team-scheme-to-channel-role gate picture
- The exact permission constants checked during team deletion (soft vs permanent)
- Whether there are additional compliance gates (e.g., legal hold) that prevent team deletion

### 4. Synthesis

Six admin and compliance gates span channel discovery and team deletion:

1. **Access Control Policy Channel Assignment** (`ValidateTeamScopePolicyChannelAssignment`, team_access_control.go:247): Validates that channels are eligible for team-scoped access policy assignment before policies are applied. Linked to `resolveTeamSyncChannelIDs` (job.go:154) which filters sync-eligible channels via `SearchTeamAccessPolicies`.

2. **Team Scheme → Channel Moderation** (`GetTeamSchemeChannelRoles`, channel.go:1030): Team-level schemes override default channel roles, gating `GetChannelModerationsForChannel`, `GetSchemeRolesForChannel`, and `PatchChannelModerationsForChannel`.

3. **Data Retention Policies** (`RetentionPolicyWithTeamAndChannelIDs`, data_retention_policy.go:19; `RetentionPolicyWithTeamAndChannelCounts`, data_retention_policy.go:33): Retention policies span both team and channel scopes, are `Auditable`, and connect to `AddEventParameterAuditableToAuditRec` for audit trail integration.

4. **Admin-Privileged Channel Discovery** (`GetUsersInChannelPageByAdmin`, user.go:734; `GetPublicChannelsByIdsForTeam`, timerlayer.go:2220): Admin-specific channel member enumeration with profile sanitization; public channel discovery scoped by team.

5. **Team Deletion → Channel Cascade** (`PermanentDeleteByTeam`, timerlayer.go:2581): Permanent team deletion cascades to bulk channel deletion. `RemoveUsersFromChannelNotMemberOfTeam` (channel.go:3568) enforces the team-membership-required-for-channel-membership invariant during channel moves.

6. **Compliance Export** (`buildUserTeamAndChannelMemberships`, export.go:632): Builds combined team-and-channel membership for `exportAllUsers`, providing a compliance/audit export gate.

**Unresolved**: The internal search-based channel discovery logic (`SearchInTeam`, `autocompleteInTeamForSearchDirectMessages`) and the detailed team-role-to-channel-role mapping (`ChannelRolesUnderTeamRole`) are in GAPS and cannot be fully traced.
