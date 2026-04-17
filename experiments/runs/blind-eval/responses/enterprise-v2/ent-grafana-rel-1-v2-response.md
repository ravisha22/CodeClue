# Enterprise v2: ent-grafana-rel-1
Date: 2026-04-17

## Question
How do users, teams, organizations, and folders relate in Grafana access control?

## Reasoning Scaffold

### 1. Relevant Symbols Identification

From **FOCUS**, the access-control-specific entries are:

- **`AccessControlStore.GetUsersBasicRoles`** (`pkg/services/accesscontrol/database/database.go:316`) — "returns the list of user basic roles (Admin, Editor, Viewer, Grafana Admin) indexed by UserID." This directly enumerates the basic role tiers.
- **`AccessControlStore.GetUserPermissions`** (`database.go:52`) — retrieves user permissions with a guard on `query.UserID == 0 && len(query.TeamIDs) == 0`, revealing that permissions are queried by both user ID and team IDs jointly.
- **`AccessControlStore.GetTeamsPermissions`** (`database.go:132`) — retrieves team permissions; behavior: `GUARD(len(teams) == 0 -> return nil, nil)`, confirming teams are a first-class permission holder.
- **`AccessControlStore.DeleteUserPermissions`** (`database.go:359`) — deletes user permissions scoped to `orgID, userID`.
- **`AccessControlStore.DeleteTeamPermissions`** (`database.go:427`) — deletes team permissions scoped to `orgID, teamID`; called_by `deleteTeamByID`.
- **`deleteUserAccessControl`** (`pkg/services/org/orgimpl/store.go:766`) — deletes from `user_role` table; called_by `deleteUserInTransaction`, showing user-role bindings live in the org store.
- **`AccessControlAPI.searchUsersPermissions`** (`pkg/services/accesscontrol/api/api.go:99`) — `GET /api/access-control/users/permissions/search`, calls `GetOrgID`, confirming org-scoped permission searches.
- **`AccessControlAPI.getUserActions`** (`api.go:71`) — `GET /api/access-control/user/actions`.
- **`AccessControlAPI.getUserPermissions`** (`api.go:85`) — `GET /api/access-control/user/permissions`.
- **`AccessControlAPI.ComputeUserID`** (`api.go:199`) — resolves a typed identity string to a user ID; guard includes `IsIdentityType` check.
- **`accessControlCheck`** (`pkg/registry/apis/iam/user/search.go:45`) — "maps a legacy RBAC action name to a K8s-style check."
- **`teamAccessControlCheck`** (`pkg/registry/apis/iam/team_search.go:45`) — "maps a legacy RBAC action name to a K8s-style check" for teams.
- **`SearchHandler.stampAccessControl`** (`iam/user/search.go:374`) — stamps access control on user search results; called_by `DoTeamSearch`, `DoSearch`.
- **`TeamSearchHandler.stampAccessControl`** (`iam/team_search.go:420`) — stamps access control on team search results; same call pattern.
- **`xormRepositoryImpl.getAccessControlFilter`** (`pkg/services/annotations/annotationsimpl/xorm_store.go:467`) — applies access control filtering for annotations; guard: `accessResources.SkipAccessControlFilter -> return ""`.
- **`AccessControl.RegisterScopeAttributeResolver`** (`acimpl/accesscontrol.go:89`) — registers scope attribute resolvers by prefix; called_by `ProvideService`.
- **`FakeAccessControl.Evaluate`** (`actest/fake.go:71`) — called by `CanQueryDataSource`, `Authorize`, `GetAuthorizer`, `HasAccess`, `HasGlobalAccess`, `Check`, `Evaluate`, `authorize`.
- **`AccessControlService`** types for alerting resources: inhibition rules (`authorize.go:16`), receivers (`authorize.go:16`), routing trees (`authorize.go:16`).

From **INDEX**:

- **`pkg/services/folder/folderimpl/folder_unifiedstorage.go`** (761L) — methods: `Create`, `Delete`, `Get`, `GetChildren`, `GetDescendantCounts` — the folder storage layer.
- **`pkg/apis/iam/v0alpha1/zz_generated.deepcopy.go`** (350L) — IAM Kubernetes-style API surface.

### 2. Tracing Relationships

**Users → Organizations → Permissions:**

- `AccessControlStore.GetUsersBasicRoles` (`database.go:316`) explicitly returns "Admin, Editor, Viewer, Grafana Admin" indexed by UserID. The signature includes `orgID int64`, confirming these roles are **org-scoped**: a user has a basic role within a specific organization.
- `AccessControlStore.DeleteUserPermissions` (`database.go:359`) takes `orgID, userID`, confirming permissions are org-scoped per user.
- `deleteUserAccessControl` (`org/orgimpl/store.go:766`) deletes from the `user_role` table and is called by `deleteUserInTransaction`, showing the user-to-role binding is stored at the org level.
- `AccessControlAPI.searchUsersPermissions` (`api.go:99`) calls `GetOrgID`, further confirming org-scoping.

**Teams → Organizations → Permissions:**

- `AccessControlStore.GetTeamsPermissions` (`database.go:132`) retrieves permissions for a set of teams. The guard `len(teams) == 0 -> return nil` shows teams are passed as a collection.
- `AccessControlStore.DeleteTeamPermissions` (`database.go:427`) takes `orgID, teamID`, confirming teams are org-scoped entities with their own permission sets.
- `AccessControlStore.GetUserPermissions` (`database.go:52`) accepts both `query.UserID` and `query.TeamIDs`, showing that a user's effective permissions are the **union of their direct permissions and their teams' permissions**.

**Users ↔ Teams (cross-reference):**

- `SearchHandler.stampAccessControl` (`user/search.go:374`) is called by both `DoTeamSearch` and `DoSearch`, indicating user and team searches share the same access-control stamping mechanism — permissions are checked uniformly whether searching users or teams.
- `teamAccessControlCheck` (`team_search.go:45`) and `accessControlCheck` (`user/search.go:45`) both map "legacy RBAC action names to K8s-style checks," showing a parallel access control mapping for both entity types.

**Folders:**

- `pkg/services/folder/folderimpl/folder_unifiedstorage.go` (INDEX, 761L) provides `Create`, `Delete`, `Get`, `GetChildren`, `GetDescendantCounts` — a hierarchical folder structure.
- `xormRepositoryImpl.getAccessControlFilter` (`xorm_store.go:467`) applies access control filtering with an `accessResources` parameter, and the `SkipAccessControlFilter` guard shows annotations (and by extension resources within folders) can have access control filtering applied or skipped.
- The `AccessControl.RegisterScopeAttributeResolver` (`acimpl/accesscontrol.go:89`) registers resolvers by prefix, suggesting folder-scoped resource attributes can be resolved to permission scopes.

**Scope Resolution:**

- `AccessControl.RegisterScopeAttributeResolver` (`acimpl/accesscontrol.go:89`) allows scope attribute resolvers to be registered by prefix string. This is the mechanism by which folder paths, dashboard IDs, or other resource identifiers are resolved into permission scopes for evaluation.
- `FakeAccessControl.Evaluate` (`actest/fake.go:71`) is called by `HasAccess` and `HasGlobalAccess`, revealing two scope levels: **org-scoped** (`HasAccess`) and **global-scoped** (`HasGlobalAccess`, which implies a "Grafana Admin" level that transcends org boundaries).

### 3. GAPS — What Cannot Be Determined

The GAPS section lists as **uncovered**:
- **`toAccessControlPermissions`** — the full conversion from internal permissions to the access control model is not visible.
- **`AccessChecker`** — the runtime permission-checking interface is not covered.
- **`InhibitionRuleAccess`** — specific alerting inhibition rule access control logic is not visible.
- **`sessionAccessChecker`** — session-based access checking is not determinable.

Additionally:
- The exact **folder-to-permission inheritance** model (whether permissions cascade from parent to child folders) is not explicitly shown in the clue. The `GetChildren`/`GetDescendantCounts` methods suggest hierarchy, but no explicit inheritance call chain is visible.
- How the four basic roles (Admin, Editor, Viewer, Grafana Admin) map to **specific permission sets** is not determinable from the clue.
- The relationship between **folders and teams** (whether teams can be scoped to specific folders) is not directly evidenced.

### 4. Synthesis

**Users** belong to **organizations** and receive **basic roles** within each org — specifically Admin, Editor, Viewer, or Grafana Admin (`AccessControlStore.GetUsersBasicRoles`, `database.go:316`). All user permissions are org-scoped (`DeleteUserPermissions` takes `orgID, userID`, `database.go:359`; `searchUsersPermissions` calls `GetOrgID`, `api.go:99`). The user-to-role binding is stored in the `user_role` table (`deleteUserAccessControl`, `orgimpl/store.go:766`).

**Teams** are also org-scoped entities (`DeleteTeamPermissions` takes `orgID, teamID`, `database.go:427`) with their own permission sets (`GetTeamsPermissions`, `database.go:132`). A user's effective permissions are computed from **both** their direct permissions and their team memberships, as `GetUserPermissions` (`database.go:52`) accepts both `UserID` and `TeamIDs` in the query.

**Organizations** are the primary scoping boundary for all access control. Every permission query is org-qualified. The "Grafana Admin" role (named in `GetUsersBasicRoles`, `database.go:316`) appears to transcend org boundaries, as evidenced by the `HasGlobalAccess` caller of `FakeAccessControl.Evaluate` (`actest/fake.go:71`).

**Folders** provide hierarchical resource organization (`folder_unifiedstorage.go`, INDEX: `Create`, `Delete`, `Get`, `GetChildren`, `GetDescendantCounts`). Access control filtering can be applied to resources within folders (`getAccessControlFilter`, `xorm_store.go:467`), and scope attribute resolvers (`RegisterScopeAttributeResolver`, `acimpl/accesscontrol.go:89`) map resource identifiers (including folder-scoped resources) to evaluable permission scopes.

The access control system is transitioning from a **legacy RBAC model** to a **K8s-style model**, as shown by `accessControlCheck` and `teamAccessControlCheck` (both mapping "legacy RBAC action names to K8s-style checks", `user/search.go:45` and `team_search.go:45`), with dedicated `AccessControlService` types for alerting sub-resources (inhibition rules, receivers, routing trees at `authorize.go:16`).

**Unresolved**: The exact permission inheritance through folder hierarchies, the full mapping of basic roles to specific actions, and the runtime `AccessChecker` behavior remain undetermined (GAPS).
