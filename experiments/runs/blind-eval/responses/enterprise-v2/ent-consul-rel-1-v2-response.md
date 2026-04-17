# Enterprise v2: ent-consul-rel-1
Date: 2026-04-17

## Question
How are the ACL entities related in Consul's ACL documentation?

## Reasoning Scaffold

### Step 1: Identify Relevant Modules, Symbols, and Relationships

**From TREE:**
- `acl/` (20 files) — core ACL authorization primitives: authorizers, errors, chained authorization.
- `agent/consul/` — ACL endpoint implementations, ACL replication, ACL server logic, state store ACL operations.
- `agent/consul/state/acl.go` — persistent storage for all ACL entities.
- `internal/go-sso/oidcauth/` — SSO/OIDC authentication related to auth methods.

**From FOCUS — ACL Entity Types Identified:**

The clue reveals five distinct ACL entity types through their CRUD operations:

1. **Tokens** — `Store.aclTokenDelete` (`agent/consul/state/acl.go:816`), `aclTokenSetTxn` (`agent/consul/state/acl.go:447`), `aclTokenList` (`agent/consul/state/acl.go:1724`), `aclTokenDeleteTxn` (`agent/consul/state/acl.go:827`).

2. **Policies** — `Store.aclPolicyDelete` (`agent/consul/state/acl.go:1077`), called by `ACLPolicyDeleteByID` and `ACLPolicyDeleteByName`.

3. **Roles** — `Store.aclRoleDelete` (`agent/consul/state/acl.go:1350`), called by `ACLRoleDeleteByID` and `ACLRoleDeleteByName`.

4. **Binding Rules** — `Store.aclBindingRuleDelete` (`agent/consul/state/acl.go:1505`), called by `ACLBindingRuleDeleteByID`. `aclBindingRuleInsert` (`agent/consul/state/acl.go:1782`), `aclBindingRuleSetTxn` (`agent/consul/state/acl.go:1400`).

5. **Auth Methods** — `Store.aclAuthMethodDelete` (`agent/consul/state/acl.go:1689`), called by `ACLAuthMethodDeleteByName`.

**From FOCUS — Relationship-establishing symbols:**

- `aclTokenSetTxn` (`agent/consul/state/acl.go:447`) — "the inner method used to insert an ACL token with the proper indexes into the state store." Critically, it calls `resolveTokenPolicyLinks` and `resolveTokenRoleLinks`, directly establishing that **tokens reference both policies and roles**.

- `policyOrRoleTokenError` (`agent/consul/acl.go:155`) — an error type whose name explicitly encodes the relationship triad: policies, roles, and tokens are interlinked.

- `aclBindingRuleSetTxn` (`agent/consul/state/acl.go:1400`) — behavior: `GUARD(rule.ID == "" -> return ErrMissingAC...); PRECEDENCE(rule -> err -> existingRaw)`. Called by `ACLBindingRuleBatchSet` and `ACLBindingRuleSet`. Binding rules are persisted with their own IDs.

- `ACL.aclPreCheck` (`agent/consul/acl_endpoint.go:160`) — called by `AuthMethodDelete`, `AuthMethodList`, `AuthMethodRead`, `AuthMethodSet`, `Authorize`, `BindingRuleDelete`, `BindingRuleList`, `BindingRuleRead`. This shows that a common pre-check gate is shared across auth method and binding rule operations, implying these entities are managed through a unified ACL endpoint.

**From FOCUS — Replication types:**

- `aclTokenReplicator.Type` (`agent/consul/acl_replication_types.go:23`) — replication for tokens.
- `aclPolicyReplicator.Type` (`agent/consul/acl_replication_types.go:138`) — replication for policies.
- `aclRoleReplicator.Type` (`agent/consul/acl_replication_types.go:274`) — replication for roles.

All three replicator types share the same `called_by` set: `mergeValue`, `sanitize`, `visit`, `walk`, `handlePtr`, `handleQuery`, `readEntry`, `decodeAttributeToMessage`. This parallel structure confirms that tokens, policies, and roles are replicated as peer entities across datacenters using a common replication framework.

- `aclTokenReplicator.SingularNoun` (`agent/consul/acl_replication_types.go:24`) — called by `deleteLocalACLType`, `replicateACLType`, `updateLocalACLType`.
- `aclPolicyReplicator.SingularNoun` (`agent/consul/acl_replication_types.go:139`) — same callers.
- `aclRoleReplicator.DeleteLocalBatch` (`agent/consul/acl_replication_types.go:360`) — calls `leaderRaftApply`, called by `deleteLocalACLType`.
- `aclPolicyReplicator.PendingUpdateEstimatedSize` (`agent/consul/acl_replication_types.go:247`) — called by `updateLocalACLType`.
- `aclTokenReplicator.RemoteMeta` (`agent/consul/acl_replication_types.go:65`) — called by `diffACLType`.

**From FOCUS — Authorization chain:**

- `Server.filterACL` (`agent/consul/acl_server.go:201`) — delegates to `filterACL`. Called by `GatewayServices`, `ListNodes`, `NodeServiceList`, `NodeServices`, `ServiceNodes`, `ListMeshGateways`, `List`, `GatewayIntentions`. This shows ACL filtering is applied to many query endpoints.

- `ChainedAuthorizer.executeChain` (`acl/chained_authorizer.go:29`) — the core authorization execution pattern.

- `PermissionDeniedError.Error` (`acl/errors.go:88`) — "Initially we may not have attribution information." This is the error produced when ACL authorization fails.

- `ACL.Authorize` (`agent/consul/acl_endpoint.go:2192`) — calls `ResolveToken`, `aclPreCheck`, `ForwardRPC`. This is the main authorization endpoint.

- `ACL.TokenRead` (`agent/consul/acl_endpoint.go:266`) — calls `aclPreCheck`, `lookupExpandedTokenInfo`, `LocalTokensEnabled`, `filterACLWithAuthorizer`, `ForwardRPC`, `ResolveTokenAndDefaultMeta`. The call to `lookupExpandedTokenInfo` implies tokens carry expandable references to other entities.

- `Server.aclTokenWriter` (`agent/consul/acl_server.go:217`) — behavior: `DELEGATE(auth.NewTokenWriter -> result)`. Calls `State`, `InPrimaryDatacenter`, `LocalTokensEnabled`. Called by `Logout`, `TokenClone`, `TokenSet`, `aclLogin`. This shows token write operations are datacenter-aware.

**From SYM — Additional ACL symbols:**
- `ACLRemoteError.Error` (`agent/consul/acl.go:126`) — indicates remote ACL operations can fail, relevant to cross-datacenter ACL resolution.

### Step 2: Trace Call Chains and Hierarchies

**Token → Policy/Role relationship:**
`aclTokenSetTxn` calls → `resolveTokenPolicyLinks` + `resolveTokenRoleLinks`
This definitively establishes that tokens contain links to both policies and roles, and these links are resolved/validated at write time.

**Auth Method → Binding Rule relationship:**
`ACL.aclPreCheck` is called by both auth method operations (`AuthMethodDelete`, `AuthMethodList`, `AuthMethodRead`, `AuthMethodSet`) and binding rule operations (`BindingRuleDelete`, `BindingRuleList`, `BindingRuleRead`). Auth methods and binding rules share a common pre-check, suggesting binding rules are associated with auth methods. When an auth method is deleted (`Store.aclAuthMethodDelete` → `aclAuthMethodDeleteTxn`), binding rules likely need cleanup (though the exact cascade is in the uncovered `aclAuthMethodDeleteTxn`).

**Token creation via auth methods:**
`Server.aclTokenWriter` (`agent/consul/acl_server.go:217`) is called by `aclLogin`, and `aclTokenSetTxn` calls `getAuthMethodWithTxn`. This chain shows: auth method login → token creation, with the auth method looked up during token persistence. This establishes that auth methods produce tokens.

**Replication hierarchy:**
All three entity types (tokens, policies, roles) have dedicated replicators that plug into a common framework:
- `replicateACLType` calls each replicator's `SingularNoun`
- `deleteLocalACLType` calls `DeleteLocalBatch`
- `updateLocalACLType` calls `PendingUpdateEstimatedSize`
- `diffACLType` calls `RemoteMeta`

**Authorization evaluation:**
`ACL.Authorize` → `ResolveToken` (resolves a token) → `aclPreCheck` → authorization decision. The token resolution step is where the token's policy and role links are evaluated to produce an authorizer.

### Step 3: GAPS — What Cannot Be Determined

Per the GAPS section:
- **Type:** STRUCTURAL (answerable from L0-L2)
- **Coverage:** 83 symbols in L3, 27 with behavior annotations.
- **Uncovered symbols:**
  - `aclAuthMethodGetByName` — how auth methods are looked up by name.
  - `aclAuthMethodInsert` — how auth methods are persisted.
  - `aclAuthMethodList` — how auth methods are enumerated.
  - `aclAuthMethodMaxIndex` — indexing for auth methods.

This means the full auth method lifecycle (creation, lookup, listing) cannot be traced. Specifically, the relationship between auth methods and binding rules during auth method deletion (whether binding rules are cascade-deleted) cannot be confirmed from the clue alone.

The clue also does not provide the internal structure of tokens (which fields hold policy/role links), nor the exact binding rule evaluation logic that maps auth method identity claims to token properties.

### Step 4: Synthesis

**ACL Entity Relationship Model:**

Based solely on the clue, Consul's ACL system comprises five interconnected entity types:

1. **Tokens** are the central entity. `aclTokenSetTxn` (`agent/consul/state/acl.go:447`) calls `resolveTokenPolicyLinks` and `resolveTokenRoleLinks`, establishing that each token holds links to **policies** and **roles** that are resolved and validated at write time. Tokens are the unit of authentication — `ACL.Authorize` (`agent/consul/acl_endpoint.go:2192`) calls `ResolveToken` to begin authorization. `ACL.TokenRead` (`agent/consul/acl_endpoint.go:266`) calls `lookupExpandedTokenInfo`, implying tokens expose an expanded view that includes their linked policies and roles.

2. **Policies** define permissions. They have their own CRUD: `Store.aclPolicyDelete` (`agent/consul/state/acl.go:1077`) is called by both `ACLPolicyDeleteByID` and `ACLPolicyDeleteByName`, indicating policies can be addressed by either ID or name. Policies are linked *from* tokens (via `resolveTokenPolicyLinks`).

3. **Roles** group policies. `Store.aclRoleDelete` (`agent/consul/state/acl.go:1350`) supports deletion by both ID and name (`ACLRoleDeleteByID`, `ACLRoleDeleteByName`). Roles are linked *from* tokens (via `resolveTokenRoleLinks`). The `policyOrRoleTokenError` (`agent/consul/acl.go:155`) error type reinforces that policies and roles are the two types of associations a token can have.

4. **Auth Methods** are external authentication providers. They produce tokens upon login: `Server.aclTokenWriter` (`agent/consul/acl_server.go:217`) is called by `aclLogin`, and `aclTokenSetTxn` calls `getAuthMethodWithTxn` to look up the associated auth method. Auth methods are managed through the ACL endpoint with a shared `aclPreCheck` gate (`agent/consul/acl_endpoint.go:160`). `Store.aclAuthMethodDelete` (`agent/consul/state/acl.go:1689`) deletes by name.

5. **Binding Rules** connect auth methods to token properties. `aclBindingRuleSetTxn` (`agent/consul/state/acl.go:1400`) persists rules with their own IDs. Binding rules share the `aclPreCheck` gate with auth methods (`ACL.aclPreCheck` is called by both `BindingRuleDelete`/`BindingRuleList`/`BindingRuleRead` and `AuthMethodDelete`/`AuthMethodList`/`AuthMethodRead`/`AuthMethodSet`), indicating they are managed as a related pair. `aclBindingRuleInsert` (`agent/consul/state/acl.go:1782`) is called by `aclBindingRuleSetTxn`, showing a standard insert pattern.

**Relationship Summary:**
- **Token → Policy**: many-to-many via `resolveTokenPolicyLinks` in `aclTokenSetTxn`.
- **Token → Role**: many-to-many via `resolveTokenRoleLinks` in `aclTokenSetTxn`.
- **Auth Method → Token**: auth method login produces tokens (via `aclLogin` → `aclTokenWriter`).
- **Auth Method ↔ Binding Rule**: binding rules are evaluated in the context of auth methods; they share endpoint management through `aclPreCheck`.
- **Replication**: tokens, policies, and roles are each replicated across datacenters via parallel replicator implementations (`aclTokenReplicator`, `aclPolicyReplicator`, `aclRoleReplicator` in `agent/consul/acl_replication_types.go`).

**Unresolved:** The exact fields within a token that hold policy/role links, the cascade behavior when an auth method is deleted (whether its binding rules are removed), and the auth method lookup/listing logic (`aclAuthMethodGetByName`, `aclAuthMethodInsert`, `aclAuthMethodList`, `aclAuthMethodMaxIndex` — all GAPS uncovered) cannot be determined from the clue.
