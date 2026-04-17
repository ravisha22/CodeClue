# Enterprise v2: ent-mattermost-rel-1
Date: 2026-04-17

## Reasoning Scaffold

### 1. Relevant Clue Entries

The question asks how team and channel creation permissions line up across the Mattermost API.

**FOCUS – PluginAPI.CreateTeam** (server/channels/app/plugin_api.go:168):
- Behavior: `DELEGATE(api.app.CreateTeam -> result)`
- Calls: `CreateTeam`, `License`, `Config`
- Called by: `InitBasic`, `localCreateTeam`, `importTeam`, `CreateTeamWithUser`, `Fuzz`, `createTeamCmdF`, `TestDeleteUserPosts`, `TestSearchUsersInTeam`

**FOCUS – PluginAPI.CreateChannel** (server/channels/app/plugin_api.go:468):
- Behavior: `DELEGATE(api.app.CreateChannel -> result)`
- Calls: `License`, `CreateChannel`, `Config`
- Called by: `localCreateChannel`, `CreateChannelWithUser`, `importChannel`, `SlackImport`, `createRandomChannel`, `Fuzz`, `ManualTest`, `createChannelCmdF`

**FOCUS – PluginAPI.CreateTeamMember** (server/channels/app/plugin_api.go:224):
- Behavior: `DELEGATE(api.app.AddTeamMember -> result)`
- Calls: `AddTeamMember`
- Called by: `CreateMember`

**FOCUS – PluginAPI.CreateTeamMembersGracefully** (server/channels/app/plugin_api.go:236):
- Behavior: `DELEGATE(api.app.AddTeamMembers -> result)`
- Calls: `AddTeamMembers`

**FOCUS – PluginAPI.DeleteTeam** (server/channels/app/plugin_api.go:176):
- Behavior: `DELEGATE(api.app.SoftDeleteTeam -> result)`
- Calls: `SoftDeleteTeam`
- Called by: `Delete`

**FOCUS – PluginAPI.DeleteTeamMember** (server/channels/app/plugin_api.go:240):
- Behavior: `DELEGATE(api.app.RemoveUserFromTeam -> result)`

**FOCUS – PluginAPI.DeleteChannelMember** (server/channels/app/plugin_api.go:670):
- Behavior: `DELEGATE(api.app.LeaveChannel -> result)`

**FOCUS – PluginAPI.HasPermissionToTeam** (server/channels/app/plugin_api.go:1122):
- Behavior: `DELEGATE(api.app.HasPermissionToTeam -> result)`
- Called by: `moveCommand`, `getPostInfo`, `getTeamMember`, `HasPermissionToChannel`, `HasPermissionToChannelByPost`, `HasPermissionToChannelMemberCount`, `HasPermissionToReadChannel`, `userCreatePostPermissionCheckWithApp`, `GetViewUsersRestrictions`

**FOCUS – PluginAPI.GetChannelByNameForTeamName** (server/channels/app/plugin_api.go:501):
- Behavior: `DELEGATE(api.app.GetChannelByNameForTeamName -> result)`

**FOCUS – testRoleStoreChannelHigherScopedPermissionsBlankTeamSchemeChannelGuest** (server/channels/store/storetest/role_store.go:549):
- Behavior: `UNWIND(defer)`
- Calls: `Channel`, `Role`, `Scheme`, `Team`, `GetMaster`
- Called by: `TestRoleStore`

**INDEX – server/channels/app/authorization.go** (675L): Exports `HasPermissionTo`, `HasPermissionToChannel`, `HasPermissionToChannelByPost`, `HasPermissionToChannelMemberCount`, `HasPermissionToEditPropertyField`.

**FOCUS – PluginAPI.GetTeam** (server/channels/app/plugin_api.go:184): Delegates to `api.app.GetTeam`.

**FOCUS – PluginAPI.GetChannel** (server/channels/app/plugin_api.go:493): Delegates to `api.app.GetChannel`.

**FOCUS – PluginAPI.GetTeamByName** (server/channels/app/plugin_api.go:193): Delegates to `api.app.GetTeamByName`.

**FOCUS – PluginAPI.GetChannelMember** (server/channels/app/plugin_api.go:639): Delegates to `api.app.GetChannelMember`.

**FOCUS – PluginAPI.GetTeamMember** (server/channels/app/plugin_api.go:248): Delegates to `api.app.GetTeamMember`.

**FOCUS – PluginAPI.GetChannelMembersForUser** (server/channels/app/plugin_api.go:651): Delegates to `api.app.GetChannelMembersForUserWithPagination`.

### 2. Tracing the Relationship

**Parallel structure between Team and Channel creation:**

Both `PluginAPI.CreateTeam` (plugin_api.go:168) and `PluginAPI.CreateChannel` (plugin_api.go:468) share a strikingly similar pattern:
- Both use the **DELEGATE** behavior pattern, proxying to the core `App` layer (`api.app.CreateTeam` and `api.app.CreateChannel` respectively).
- Both call **`License`** and **`Config`** in addition to the core create function. This indicates that both team and channel creation are gated by **license checks** and **configuration settings** before the create operation proceeds.
- Both have parallel caller sets: they are invoked by local admin commands (`localCreateTeam` / `localCreateChannel`), user-facing commands (`CreateTeamWithUser` / `CreateChannelWithUser`), import paths (`importTeam` / `importChannel`, `SlackImport`), CLI commands (`createTeamCmdF` / `createChannelCmdF`), and testing utilities (`Fuzz`).

**Permission hierarchy — Team scopes Channel:**

`PluginAPI.HasPermissionToTeam` (plugin_api.go:1122) is called by `HasPermissionToChannel`, `HasPermissionToChannelByPost`, `HasPermissionToChannelMemberCount`, and `HasPermissionToReadChannel`. This demonstrates that **channel-level permission checks cascade through team-level permission checks** — a user must have appropriate team permissions before channel permissions are evaluated.

The authorization module (`server/channels/app/authorization.go`, 675L, INDEX) centralizes permission logic with `HasPermissionTo`, `HasPermissionToChannel`, `HasPermissionToChannelByPost`, and `HasPermissionToChannelMemberCount`. The team permission check (`HasPermissionToTeam`) feeding into channel permission checks confirms a **hierarchical permission model**: system → team → channel.

**Scheme-based role customization:**

The test `testRoleStoreChannelHigherScopedPermissionsBlankTeamSchemeChannelGuest` (role_store.go:549) calls `Channel`, `Role`, `Scheme`, `Team`, and `GetMaster`, and is invoked by `TestRoleStore`. This confirms that **team-level schemes** can override default channel roles — the "higher scoped permissions" in the test name indicates that team scheme permissions propagate down to channel-scoped roles.

**Membership operations mirror the hierarchy:**

- Team membership: `CreateTeamMember` → `AddTeamMember` (plugin_api.go:224); `CreateTeamMembersGracefully` → `AddTeamMembers` (plugin_api.go:236); `DeleteTeamMember` → `RemoveUserFromTeam` (plugin_api.go:240).
- Channel membership: `GetChannelMember` → `GetChannelMember` (plugin_api.go:639); `GetChannelMembersForUser` → `GetChannelMembersForUserWithPagination` (plugin_api.go:651); `DeleteChannelMember` → `LeaveChannel` (plugin_api.go:670).

The naming asymmetry is notable: team deletion is a **soft delete** (`SoftDeleteTeam` via `DeleteTeam`, plugin_api.go:176), while channel member removal delegates to `LeaveChannel` — suggesting different lifecycle semantics.

**Channel-within-team scoping:**

`PluginAPI.GetChannelByNameForTeamName` (plugin_api.go:501) takes `teamName, channelName` parameters, confirming channels are scoped within teams. The RPC layer mirrors this with `apiRPCClient.GetChannelByNameForTeamName` (client_rpc_generated.go:3323) and `apiTimerLayer.GetChannelByNameForTeamName` (api_timer_layer_generated.go:521).

### 3. GAPS — What Cannot Be Determined

The GAPS section states:
- **Type**: STRUCTURAL (answerable from L0-L2)
- **Coverage**: 83 symbols in L3, 52 with behavior annotations
- **Uncovered**: `apiRPCServer.GetChannelSidebarCategories`, `apiRPCServer.ShareChannel`, `apiRPCServer.UpdateTeam`, `apiRPCServer.UpdateTeamMemberRoles`

From the clue alone, we **cannot determine**:
- The specific permission constants checked during team or channel creation (e.g., `PermissionCreateTeam`, `PermissionCreatePublicChannel`)
- How `License` and `Config` gate creation — whether specific license tiers restrict team/channel creation counts or types
- The exact behavior of `UpdateTeam` and `UpdateTeamMemberRoles` (listed as uncovered)
- How shared channels (`ShareChannel`, uncovered) interact with team-scoped permissions
- Whether channel creation requires explicit team membership or just team-level permission
- The full channel sidebar category system (`GetChannelSidebarCategories`, uncovered)

### 4. Synthesis

Team and channel creation permissions in the Mattermost API are **structurally parallel and hierarchically linked**:

1. **Parallel creation patterns**: Both `PluginAPI.CreateTeam` (plugin_api.go:168) and `PluginAPI.CreateChannel` (plugin_api.go:468) delegate to the core App layer and both consult `License` and `Config`, indicating that creation of both entity types is gated by license and configuration checks.

2. **Hierarchical permission model**: Channel permissions depend on team permissions. `HasPermissionToTeam` (plugin_api.go:1122) is called by `HasPermissionToChannel`, `HasPermissionToChannelByPost`, `HasPermissionToChannelMemberCount`, and `HasPermissionToReadChannel` — establishing that team-level authorization is a **prerequisite** for channel-level authorization. The centralized authorization module (`authorization.go`, 675L) manages this hierarchy.

3. **Channels are scoped within teams**: `GetChannelByNameForTeamName` (plugin_api.go:501) requires both team and channel names, confirming the team-channel containment relationship.

4. **Scheme-based role overrides**: Team schemes can customize channel roles, as evidenced by `testRoleStoreChannelHigherScopedPermissionsBlankTeamSchemeChannelGuest` (role_store.go:549), allowing team-level schemes to override default channel guest permissions.

5. **Multiple invocation paths**: Both team and channel creation are accessible through user-facing API calls (`CreateTeamWithUser`, `CreateChannelWithUser`), local admin paths (`localCreateTeam`, `localCreateChannel`), CLI commands (`createTeamCmdF`, `createChannelCmdF`), and import utilities — all converging through the PluginAPI DELEGATE layer.

**Unresolved**: The exact permission constants, license tier restrictions, and shared-channel permission interactions cannot be determined from the clue (GAPS: `apiRPCServer.ShareChannel`, `apiRPCServer.UpdateTeamMemberRoles` uncovered).
