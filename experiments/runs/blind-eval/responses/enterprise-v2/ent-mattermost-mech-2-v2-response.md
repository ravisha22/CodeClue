# Enterprise v2: ent-mattermost-mech-2
Date: 2026-04-17

## Reasoning Scaffold

### 1. Relevant Clue Entries

The question asks how security-sensitive issues and security updates are handled in Mattermost's policy docs.

**README** (README.md:1-97): Describes Mattermost as "an open core, self-hosted collaboration platform." FOCUS for README.md lists sections including **"Get security bulletins"** — a dedicated section in the top-level README addressing security communications.

**FOCUS – Server.DoSecurityUpdateCheck** (server/channels/app/security_update_check.go:35):
- Behavior: `GUARD(!*s.platform.Config().ServiceSettings.EnableS... -> return); PRECEDENCE(not_s.platform.Config -> err -> currentTime)`
- Calls: `License`, `Log`, `ServerId`, `Set`, `MailServiceConfig`, `Store`, `Encode`
- Called by: `doSecurity`

**FOCUS – App.CreateOrUpdateAccessControlPolicy** (server/channels/app/access_control.go:77):
- Behavior: `GUARD(acs == nil -> return nil, model.N...); PRECEDENCE(acs -> policy -> appErr); ACCUMULATE(loop -> result)`
- Calls: `Srv`, `SavePolicy`
- Called by: `createAccessControlPolicy`

**FOCUS – AccessControlPolicyActiveUpdate** (server/public/model/access_policy.go:117):
- "represents a single policy's active status update."

**FOCUS – AccessControlPolicyActiveUpdateRequest** (server/public/model/access_policy.go:123):
- "is used in the API to update active status for multiple policies."
- Methods: `Auditable`

**FOCUS – AccessControlPolicyActiveUpdateRequest.Auditable** (server/public/model/access_policy.go:128):
- Behavior: `ACCUMULATE(append loop -> entries map)`
- Called by: `Auditable`, `AddEventParameterAuditableToAuditRec`, `LogClone`

**FOCUS – App.ValidateAccessControlPolicyPermission** (server/channels/app/access_control.go:390):
- "validates if a user has permission to manage a specific existing access control po…"
- Behavior: `DELEGATE(a.ValidateAccessControlPolicyPermissionWithOptions -> result)`
- Called by: `deleteAccessControlPolicy`, `setActiveStatus`, `updateActiveStatus`

**FOCUS – App.ValidateAccessControlPolicyPermissionWithChannelContext** (access_control.go:442):
- "validates access control policy permissions with channel context…"
- Behavior: `DELEGATE(a.ValidateAccessControlPolicyPermissionWithOptions -> result)`
- Called by: `getAccessControlPolicy`

**FOCUS – App.ValidateAccessControlPolicyPermissionWithMode** (access_control.go:435):
- "validates access control policy permissions with read-only mode option"
- Behavior: `DELEGATE(a.ValidateAccessControlPolicyPermissionWithOptions -> result)`

**FOCUS – App.ValidateChannelAccessControlPolicyCreation** (access_control.go:466):
- "validates if a user can create a channel-specific access control policy"
- Behavior: `GUARD(a.HasPermissionTo(userID, model.PermissionMan... -> return nil); PRECEDENCE(a -> policy)`
- Calls: `ValidateChannelAccessControlPermission`, `HasPermissionTo`
- Called by: `createAccessControlPolicy`

**FOCUS – App.isSystemPolicyAppliedToChannel** (access_control.go:450):
- "checks if a system policy is applied to a specific channel"
- Behavior: `GUARD(err != nil -> return false); PRECEDENCE(err -> channelPolicy)`
- Calls: `GetAccessControlPolicy`
- Called by: `ValidateAccessControlPolicyPermissionWithOptions`

**FOCUS – App.AssignAccessControlPolicyToChannels** (access_control.go:147):
- Behavior: `GUARD(acs == nil -> return nil, model.N...); PRECEDENCE(acs -> appErr -> policy); ACCUMULATE(ValidateChannelEligib... -> policies child)`
- Calls: `GetAccessControlPolicy`, `ValidateChannelEligibilityForAccessControl`, `Srv`, `GetChannels`, `Error`, `GetPolicy`, `SavePolicy`
- Called by: `assignAccessPolicy`

**FOCUS – App.GetChannelsForPolicy** (access_control.go:20):
- Behavior: `GUARD(appErr != nil -> return nil, 0, appErr); DISPATCH(policy)`
- Calls: `GetAccessControlPolicy`, `Srv`, `Error`
- Called by: `getChannelsForAccessControlPolicy`

**FOCUS – SqlAccessControlPolicyStore.Delete** (server/channels/store/sqlstore/access_control_policy_store.go:305):
- Behavior: `GUARD(err != nil -> return errors.Wrap(...); PRECEDENCE(err -> existingPolicy); UNWIND(defer)`
- Calls: `deleteT`, `getT`, `accessControlPolicyHistorySliceColumns`, `fromModel`, `GetMaster`, `ExecBuilder`, `IsBinaryParamEnabled`, `getQueryBuilder`

**FOCUS – SqlAccessControlPolicyStore.Save** (access_control_policy_store.go:184):
- Behavior: `GUARD(err := policy.IsValid(); err != nil -> return nil, err); PRECEDENCE(err); UNWIND(defer)`
- Calls: `deleteT`, `getHistoryT`, `getT`, `accessControlPolicySliceColumns`, `fromModel`, `preSaveAccessControlPolicy`, `toModel`

**FOCUS – SqlRetentionPolicyStore.Save** (server/channels/store/sqlstore/retention_policy_store.go:41):
- Behavior: `GUARD(err = s.checkTeamsExist(policy.TeamIDs); err... -> return nil, err); PRECEDENCE(err); UNWIND(defer)`
- Calls: `Get`, `buildGetPolicyQuery`, `buildInsertRetentionPoliciesChannelsQuery`, `buildInsertRetentionPoliciesTeamsQuery`, `checkChannelsExist`, `checkTeamsExist`, `executePossiblyEmptyQuery`, `GetMaster`

**FOCUS – createAccessControlPolicy** (server/channels/api4/access_control.go:40):
- Behavior: `GUARD(jsonErr := json.NewDecoder(r.Body).Decode(&po... -> return); PRECEDENCE(jsonErr -> policy -> appErr); UNWIND(defer)`
- Calls: `CreateOrUpdateAccessControlPolicy`, `ValidateChannelAccessControlPolicyCreation`, `LogAuditRec`, `MakeAuditRecord`, `HasPermissionToChannel`, `SessionHasPermissionTo`, `SessionHasPermissionToTeam`, `Config`

**INDEX – server/channels/app/audit.go** (235L): `AddAuditLogCertificate`, `GetAudits`, `GetAuditsPage`, `LogAuditRec`, `LogAuditRecWithLevel`

**INDEX – server/channels/web/handlers.go** (578L): `ServeHTTP`, `basicSecurityChecks`, `checkCSRFToken`

**TREE**: `server/fips/` — a dedicated FIPS directory

### 2. Tracing the Mechanisms

**A. Security Update Checks (Runtime Mechanism)**

`Server.DoSecurityUpdateCheck` (security_update_check.go:35) is the primary mechanism for handling security updates at runtime. It is:
- **Configuration-gated**: `GUARD(!*s.platform.Config().ServiceSettings.EnableS... -> return)` — the check only runs if `ServiceSettings.EnableSecurityUpdateCheck` (inferred from truncated name) is enabled in the server configuration.
- **Invoked by**: `doSecurity` — suggesting it runs on a scheduled basis.
- **Operations**: Calls `License` (checks current license), `Log` (logs the check), `ServerId` (identifies the server instance), `Set` (persists state), `MailServiceConfig` (potentially for email notifications), `Store` (database persistence), and `Encode` (data serialization).
- **Precedence logic**: `PRECEDENCE(not_s.platform.Config -> err -> currentTime)` indicates the function checks config first, handles errors, then evaluates timing — consistent with a periodic security bulletin check that phones home.

**B. README Security Bulletins Section**

The README.md (FOCUS) includes a dedicated **"Get security bulletins"** section (listed among the README sections). This establishes that the project's top-level documentation directs users to a security bulletin communication channel.

**C. Access Control Policy Framework (Policy-Level Security)**

The access control policy system provides fine-grained security policy management:

1. **Creation with permission validation**: `createAccessControlPolicy` (api4/access_control.go:40) enforces multiple permission checks before creating a policy:
   - `SessionHasPermissionTo` — system-level permission check
   - `SessionHasPermissionToTeam` — team-level permission check
   - `HasPermissionToChannel` — channel-level permission check
   - `ValidateChannelAccessControlPolicyCreation` (access_control.go:466) — checks `HasPermissionTo(userID, model.PermissionMan...)` (likely `PermissionManageSystem` or similar)
   - `LogAuditRec` and `MakeAuditRecord` — every policy creation is audit-logged

2. **Policy permission validation hierarchy**:
   - `ValidateAccessControlPolicyPermission` (access_control.go:390) — validates management permissions, delegates to `ValidateAccessControlPolicyPermissionWithOptions`. Called by `deleteAccessControlPolicy`, `setActiveStatus`, `updateActiveStatus`.
   - `ValidateAccessControlPolicyPermissionWithChannelContext` (access_control.go:442) — adds channel context for read access validation. Called by `getAccessControlPolicy`.
   - `ValidateAccessControlPolicyPermissionWithMode` (access_control.go:435) — adds read-only mode distinction.
   - `isSystemPolicyAppliedToChannel` (access_control.go:450) — checks if a system-wide policy applies to a specific channel, called during permission validation.

3. **Policy lifecycle is auditable**: `AccessControlPolicyActiveUpdateRequest.Auditable` (access_policy.go:128) implements the `Auditable` interface, called by `AddEventParameterAuditableToAuditRec` and `LogClone` — ensuring all policy status changes are captured in the audit trail.

4. **Store-level validation**: `SqlAccessControlPolicyStore.Save` (access_control_policy_store.go:184) guards with `policy.IsValid()` before persistence. `SqlAccessControlPolicyStore.Delete` (access_control_policy_store.go:305) retrieves the existing policy before deletion and maintains history via `accessControlPolicyHistorySliceColumns`.

**D. Data Retention Policies (Compliance)**

`SqlRetentionPolicyStore.Save` (retention_policy_store.go:41) validates that referenced teams and channels exist (`checkTeamsExist`, `checkChannelsExist`) before saving retention policies. This ensures retention policies cannot reference non-existent resources — a compliance integrity gate.

**E. Web Layer Security Checks**

`server/channels/web/handlers.go` (INDEX, 578L) includes `basicSecurityChecks` and `checkCSRFToken` — HTTP-level security mechanisms applied to incoming requests via the `ServeHTTP` handler.

**F. FIPS Compliance**

The `server/fips/` directory (TREE) indicates dedicated FIPS (Federal Information Processing Standards) compliance code, suggesting cryptographic operations can be configured to meet federal security standards.

**G. Audit Infrastructure**

`server/channels/app/audit.go` (INDEX, 235L) provides the audit infrastructure: `LogAuditRec`, `LogAuditRecWithLevel`, `GetAudits`, `GetAuditsPage`, and `AddAuditLogCertificate`. The certificate management function suggests audit logs can be cryptographically signed or verified.

### 3. GAPS — What Cannot Be Determined

The GAPS section states:
- **Type**: STRUCTURAL (answerable from L0-L2)
- **Coverage**: 83 symbols in L3, 28 with behavior annotations
- **Uncovered**: `RetentionPolicyForTeamList`, `RetentionPolicyStore` (2 entries), `RetentionPolicyTeam`

From the clue alone, we **cannot determine**:
- The exact URL or mechanism for the "Get security bulletins" section (README content is truncated)
- What external endpoint `DoSecurityUpdateCheck` contacts and what data it sends/receives
- The full retention policy store interface and its enforcement mechanism for data deletion
- Whether there is a formal security disclosure policy (e.g., SECURITY.md) — no such file appears in TREE
- The specific FIPS algorithms or compliance level supported by `server/fips/`
- The content and scope of `basicSecurityChecks` in the web handler layer
- How security vulnerabilities are reported by external researchers

### 4. Synthesis

Mattermost handles security-sensitive issues and security updates through **five interconnected mechanisms** visible in the clue:

1. **Automated Security Update Checks**: `Server.DoSecurityUpdateCheck` (security_update_check.go:35) performs periodic security update checks, gated by `ServiceSettings.EnableSecurityUpdateCheck` configuration. It consults the server's license, logs results, and uses mail service configuration — suggesting it can notify administrators of available security updates. Called by `doSecurity`, it runs as a scheduled server task.

2. **Security Bulletins Documentation**: The top-level README.md includes a **"Get security bulletins"** section (FOCUS README.md), directing users to security communication channels. This is the primary policy-document-level mechanism for security awareness.

3. **Access Control Policy Framework**: A comprehensive policy management system in `server/channels/app/access_control.go` provides:
   - Multi-level permission validation (`ValidateAccessControlPolicyPermission`, `ValidateAccessControlPolicyPermissionWithChannelContext`, `ValidateChannelAccessControlPolicyCreation`) spanning system, team, and channel scopes
   - Full audit trail integration via `Auditable` interface on policy update requests (`AccessControlPolicyActiveUpdateRequest.Auditable`, access_policy.go:128)
   - Policy history tracking in the store layer (`accessControlPolicyHistorySliceColumns` in `SqlAccessControlPolicyStore.Save/Delete`)

4. **Web-Level Security Gates**: `basicSecurityChecks` and `checkCSRFToken` (handlers.go, INDEX) provide HTTP request-level security enforcement, applied through the `ServeHTTP` handler chain.

5. **Compliance Infrastructure**: Data retention policies (`SqlRetentionPolicyStore.Save`, retention_policy_store.go:41) with existence validation, FIPS compliance support (`server/fips/` in TREE), and cryptographic audit log management (`AddAuditLogCertificate` in audit.go) provide the compliance layer.

**Unresolved**: The external security bulletin URL, the `DoSecurityUpdateCheck` phone-home details, the FIPS compliance scope, the existence of a formal vulnerability disclosure policy (e.g., SECURITY.md), and the full retention policy enforcement mechanism cannot be determined from the clue (GAPS: `RetentionPolicyStore`, `RetentionPolicyForTeamList`, `RetentionPolicyTeam` uncovered).
