# Enterprise v2: ent-grafana-struct-1
Date: 2026-04-17

## Question
What are the main administrative permission tiers in Grafana and where do their boundaries sit?

## Reasoning Scaffold

### 1. Relevant Symbols Identification

From **FOCUS**, the most directly relevant entries are:

- **`PermissionType.String`** (`pkg/services/team/model.go:127`) — its behavior annotation `GUARD(p == PermissionTypeAdmin -> return "Admin")` explicitly names an "Admin" permission tier.
- **`api.setSinglePermissionToK8s`** (`pkg/services/accesscontrol/resourcepermissions/api_adapter.go:470`) — orchestrates setting a single resource permission into K8s-style storage and is called by three distinct callers that reveal three identity-level boundaries.
- **`ResourceSearchRequest.GetPermission`** (`pkg/storage/unified/resourcepb/search.pb.go:348`) — returns a `Permission` value from a search request; its `called_by` list (`GetResourcePermissionDeleteTuple`, `GetResourcePermissionWriteTuple`) reveals Write and Delete as distinguishable permission actions.

From **SYM / INDEX**:

- **`pkg/apis/iam/v0alpha1/zz_generated.deepcopy.go`** (350 L) — an IAM API surface at the Kubernetes-style API layer, indicating identity and access management has its own versioned API group.
- **`pkg/services/authz/zanzana/common/info.go`** — `ResourceInfo.Context` lives in a Zanzana authorization subsystem, pointing to a relationship-based authorization engine.

### 2. Tracing Calls and Hierarchies

**`api.setSinglePermissionToK8s`** (`api_adapter.go:470`):
- **called_by**: `setBuiltInRolePermissionToK8s`, `setTeamPermissionToK8s`, `setUserPermissionToK8s`
- This reveals three identity tiers that can receive permissions: **built-in roles**, **teams**, and **individual users**. The function itself calls `buildResourcePermissionName`, `createOrUpdateResourcePermission`, `getAPIGroup`, `getDynamicClient`, `getExistingResourcePermission`, and `Context`, showing the boundary sits at the K8s resource-permission level, where permissions are named objects in a dynamic API group.

**`PermissionType.String`** (`team/model.go:127`):
- The guard `p == PermissionTypeAdmin -> return "Admin"` indicates at least an "Admin" tier exists as a named constant. The function is called by a broad set of callers (`GetMeta`, `generateShortUID`, `Push`, `RangeQuery`, `generate`, `runAction`, `ServeHTTP`, `KeyVal`), suggesting this tier label is used across many subsystems.

**`ResourceSearchRequest.GetPermission`** (`search.pb.go:348`):
- **called_by**: `GetResourcePermissionDeleteTuple`, `GetResourcePermissionWriteTuple`
- This shows the permission model distinguishes at least **Write** and **Delete** as separate permission actions at the resource/tuple level.

### 3. Structural Context from TREE and INDEX

The permission system spans multiple packages:
- `pkg/services/accesscontrol/resourcepermissions/` — the adapter layer converting permissions to K8s representations.
- `pkg/services/authz/zanzana/` — relationship-based authorization (Zanzana), with `ResourceInfo.Context` (`info.go:184`).
- `pkg/storage/unified/resourcepb/` — the protobuf resource layer encoding permission tuples (`search.pb.go:348`).
- `pkg/services/team/model.go` — team-level permission type definitions.
- `pkg/apis/iam/v0alpha1/` — a versioned Kubernetes-style IAM API.

### 4. GAPS — What Cannot Be Determined

The GAPS section lists as **uncovered**:
- `TranslateResourcePermissionToTuples` — the full translation logic from resource permissions to authorization tuples is not visible.
- `api.setBuiltInRolePermissionToK8s` — the body of this caller is not included; we cannot see exactly how built-in roles are enumerated.
- `changeInfo.GrafanaHost` — unrelated to permissions.
- `dashboardUidPermissionMigrator.migrateWildcards` — a migration for wildcard permissions is not visible, meaning the exact handling of wildcard/broad permissions cannot be determined.

Additionally, the clue covers 83 symbols with 75 behavior annotations, but the full enumeration of all tier labels (e.g., "Editor", "Viewer", "Grafana Admin" vs org-scoped "Admin") is not directly present in these FOCUS entries.

### 5. Synthesis

**Supported Structure — Three Administrative Permission Tiers by Identity:**

1. **Built-in Role Permissions** — `setBuiltInRolePermissionToK8s` (called_by of `api.setSinglePermissionToK8s`, `api_adapter.go:470`) assigns permissions to built-in roles. The `PermissionType.String` guard (`team/model.go:127`) confirms at least an **"Admin"** named tier exists. These are org-level role assignments.

2. **Team Permissions** — `setTeamPermissionToK8s` (called_by of `api.setSinglePermissionToK8s`, `api_adapter.go:470`) assigns permissions at the team level. Teams have their own permission type model in `pkg/services/team/model.go`.

3. **User Permissions** — `setUserPermissionToK8s` (called_by of `api.setSinglePermissionToK8s`, `api_adapter.go:470`) assigns permissions to individual users, forming the most granular tier.

**Boundary Location:**

The boundary between these tiers sits at the **resource permission adapter** (`api.setSinglePermissionToK8s`, `api_adapter.go:470`), which is the convergence point where all three identity types are normalized into K8s-style named resource permissions via `buildResourcePermissionName` and `createOrUpdateResourcePermission`. Below this adapter, the **Zanzana authorization engine** (`pkg/services/authz/zanzana/`, `ResourceInfo.Context` at `info.go:184`) and the **protobuf tuple layer** (`GetResourcePermissionDeleteTuple`, `GetResourcePermissionWriteTuple` calling `GetPermission` at `search.pb.go:348`) encode the effective permission as Write or Delete tuples.

**Permission Action Granularity:**

Within each tier, the permission actions visible from the clue are at minimum **Write** and **Delete** (`GetResourcePermissionWriteTuple` and `GetResourcePermissionDeleteTuple`, called_by of `ResourceSearchRequest.GetPermission`, `search.pb.go:348`).

**Unresolved Uncertainty:**

- The complete list of built-in role names (e.g., whether "Editor", "Viewer", "Grafana Admin" are distinct tiers or sub-tiers) cannot be confirmed from the clue alone — `PermissionType.String` only shows the "Admin" guard, and `setBuiltInRolePermissionToK8s` body is uncovered (GAPS).
- The wildcard permission migration logic (`dashboardUidPermissionMigrator.migrateWildcards`, GAPS uncovered) means the handling of broad/wildcard permissions across tiers is not determinable.
- The full tuple translation (`TranslateResourcePermissionToTuples`, GAPS uncovered) means we cannot confirm every permission action type beyond Write and Delete.
