# Enterprise v2: ent-supabase-rel-1
Date: 2026-04-17

## Question
How do API keys, auth tokens, and RLS work together in Supabase's access model?

## Reasoning

### Relevant Clue Entries

**API key types in docker configuration (FOCUS):** The `docker/.env.example` file (lines 1-345) defines several key/secret entries: `ANON_KEY`, `SERVICE_ROLE_KEY`, `JWT_SECRET`, `SUPABASE_PUBLISHABLE_KEY`, and `SUPABASE_SECRET_KEY` (FOCUS: `docker/.env.example`). From the clue alone, this supports a multi-key access model plus a separate JWT secret, but not the full semantics of each key.

**Client-side API key usage (FOCUS):** The `examples/auth/hono-full/.env.example` shows clients are configured with `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` (FOCUS: `examples/auth/hono-full/.env.example:1-3`). This confirms clients use the anon key to connect to the Supabase API endpoint.

**OAuth flow (FOCUS):** The `examples/oauth-app-authorization-flow/.env.example` introduces `SUPABASE_CLIENT_ID` and `SUPABASE_CLIENT_SECRET` alongside `SUPABASE_REDIRECT_URL` (FOCUS: `examples/oauth-app-authorization-flow/.env.example:1-4`), indicating an OAuth authorization flow exists as an alternative or supplementary access mechanism.

**Custom access token hook (FOCUS):** `authConfigToCustomAccessTokenHookDetails` in `apps/studio/hooks/misc/useCustomAccessTokenHookDetails.tsx:5-15` accepts an `authConfig` and guards on `!authConfig || !authConfig.HOOK_CUSTOM_ACCESS_TOKEN_ENABLED`. It uses `authConfig.HOOK_CUSTOM_ACCESS_TOKEN_ENABLED`, `authConfig.HOOK_CUSTOM_ACCESS_TOKEN_URI`, and `authConfig.HOOK_CUSTOM_ACCESS_TOKEN_SECRETS` (FOCUS: `authConfigToCustomAccessTokenHookDetails`). This reveals an extensibility point: a custom access token hook can be enabled to modify or enrich the access token, which would influence what claims are available for RLS policy evaluation.

**API access role checking (FOCUS):** `isApiAccessRole` in `apps/studio/lib/data-api-types.ts:6-9` checks whether a value is in `API_ACCESS_ROLES` via `API_ACCESS_ROLES.includes(value)` with `behavior: DELEGATE` (FOCUS: `isApiAccessRole`). This indicates there is a defined set of API access roles, and the system validates whether a given role string belongs to that set — connecting API keys to role-based access.

**Access token types (FOCUS):** Multiple access token types exist:
- `AccessToken` and `AccessTokensData` in `apps/studio/data/access-tokens/access-tokens-query.ts:14-18`, typed as `Awaited<ReturnType<typeof getAccessTokens>>` (FOCUS: `AccessToken`, `AccessTokensData`). These represent management-plane access tokens.
- `ScopedAccessToken` and `ScopedAccessTokensData` in `apps/studio/data/scoped-access-tokens/scoped-access-token-query.ts:28-35`, deriving from `components['schemas']['GetScopedAccessTokensResponse']['tokens']` (FOCUS: `ScopedAccessToken`, `ScopedAccessTokensData`). Scoped tokens imply fine-grained, limited-scope access — distinct from the broad anon/service-role keys.

**API keys UI and permissions (FOCUS):** 
- `ApiKeysTabContent` in `apps/studio/components/interfaces/Connect/ApiKeysTabContent.tsx:24-76` uses `PermissionAction.SECRETS_READ` and accesses `projectKeys.apiUrl`, `projectKeys.publishableKey`, `projectKeys.anonKey` with `behavior: PRECEDENCE(isLoadingPermissions -> not_canReadAPIKeys)` (FOCUS: `ApiKeysTabContent`). This shows reading API keys requires `SECRETS_READ` permission, and a project has at least an `apiUrl`, `publishableKey`, and `anonKey`.
- `useApiKeysCommands` in `apps/studio/components/interfaces/App/CommandMenu/ApiKeys.tsx:23-166` also uses `PermissionAction.SECRETS_READ` and accesses `publishableKey.api_key` and `publishableKey.type` (FOCUS: `useApiKeysCommands`). This confirms publishable keys have a `type` attribute, reinforcing the multi-key-type model.

**Auth operations on the client (FOCUS):**
- `SupabaseService.signIn` delegates to `this.supabase.auth.signInWithOtp` (FOCUS: `SupabaseService.signIn`, `angular-user-management/src/app/supabase.service.ts:42-44`).
- `SupabaseService.getUser` delegates to `this.supabase.auth.getUser` with a guard `GUARD(error -> return null)` (FOCUS: `SupabaseService.getUser`, same file:22-28).
- `SupabaseService.signOut` delegates to `this.supabase.auth.signOut` (FOCUS: `SupabaseService.signOut`, same file:46-48).

These show that the client-side service surface includes sign-in, sign-out, and current-user retrieval operations, but the exact token contents and transport are not described in the clue.

**API proxy/forwarding (FOCUS):** `forwardToSupabaseAPI` in `apps/ui-library/registry/default/platform/platform-kit-nextjs/app/api/supabase-proxy/[...path]/route.ts:2-81` uses `process.env.SUPABASE_MANAGEMENT_API_TOKEN` and applies `behavior: PRECEDENCE(not_process -> not_userHasPermissionForProj -> contentType)`. It is `called_by: GET, HEAD, PATCH, POST, PUT` (FOCUS: `forwardToSupabaseAPI`). This shows the management API proxy checks for a management API token and verifies user project permissions before forwarding requests.

**API access toggle (FOCUS):** `getApiAccessSwitch` in `e2e/studio/features/api-access-toggle.spec.ts:63-70` retrieves a switch element via `page.getByTestId` and `dataApiSection.getByRole` (FOCUS: `getApiAccessSwitch`). This indicates API access can be toggled on/off per project, providing an additional layer of access control.

### Synthesis

Based on the clue, API keys, auth tokens, and RLS work together in Supabase's access model as follows:

1. **API keys are tiered and role-related:** The configuration distinguishes `ANON_KEY`, `SERVICE_ROLE_KEY`, `SUPABASE_PUBLISHABLE_KEY`, and `SUPABASE_SECRET_KEY`, alongside `JWT_SECRET` (FOCUS: `docker/.env.example`). Separately, `isApiAccessRole` validates whether a value is one of `API_ACCESS_ROLES` (FOCUS: `isApiAccessRole`, `apps/studio/lib/data-api-types.ts:6-9`). Together, those entries support the narrower claim that Supabase has multiple key classes and a role vocabulary for API access.

2. **Auth tokens are a separate access surface from project keys:** Users can authenticate through methods such as OTP via `this.supabase.auth.signInWithOtp` (FOCUS: `SupabaseService.signIn`), while the Studio also exposes access-token and scoped-access-token types (`AccessToken`, `ScopedAccessToken`, `ScopedAccessTokensData`) and a custom-access-token hook configuration (`authConfigToCustomAccessTokenHookDetails`) (FOCUS: `AccessToken`; FOCUS: `ScopedAccessToken`; FOCUS: `ScopedAccessTokensData`; FOCUS: `authConfigToCustomAccessTokenHookDetails`). That supports a distinction between project-level keys and user/token-oriented auth flows.

3. **RLS is related conceptually, but its exact coupling is not exposed here:** The question asks about RLS, and the clue gives adjacent evidence — API-access roles (`isApiAccessRole`), multiple key classes (`docker/.env.example`), client auth operations (`SupabaseService.signIn` / `getUser`), and custom access-token hooks (`authConfigToCustomAccessTokenHookDetails`) — that suggest keys/tokens feed into access decisions (FOCUS: `isApiAccessRole`; FOCUS: `docker/.env.example`; FOCUS: `SupabaseService.signIn`; FOCUS: `SupabaseService.getUser`; FOCUS: `authConfigToCustomAccessTokenHookDetails`). But the clue does **not** include any direct RLS policy definitions, role-to-policy mappings, or execution-path annotations showing exactly how RLS is enforced.

4. **Layered access control:**
   - **Key level:** multiple configured key classes: `ANON_KEY`, `SERVICE_ROLE_KEY`, `SUPABASE_PUBLISHABLE_KEY`, and `SUPABASE_SECRET_KEY` (FOCUS: `docker/.env.example`).
   - **Token level:** Scoped access tokens (`ScopedAccessToken` at `scoped-access-token-query.ts:31-32`) provide fine-grained, limited-scope access beyond the broad key types (FOCUS: `ScopedAccessToken`).
   - **Permission level:** Studio operations require permissions like `PermissionAction.SECRETS_READ` to view keys (FOCUS: `ApiKeysTabContent`, `useApiKeysCommands`).
   - **Toggle level:** API access can be toggled at the project level (FOCUS: `getApiAccessSwitch`).

5. **Proxy-level validation:** The management API proxy (`forwardToSupabaseAPI`) validates the management API token and user project permissions before forwarding (FOCUS: `forwardToSupabaseAPI`).

### Gaps and Uncertainties

- **GAPS type is STRUCTURAL** with 82 symbols at L3 but only 11 with behavior annotations. The uncovered symbols include `SessionAccessTokenError`, `AccessTokenListProps`, `AccessTokenNewBannerProps`, and `NewAccessTokenButtonProps` (GAPS). The UI for creating and managing access tokens cannot be fully traced.
- The clue does not contain any direct RLS policy definitions, database role configurations, or field-level policy expressions. The connection between keys/tokens and RLS therefore remains only partially supported.
- The exact difference between `SUPABASE_PUBLISHABLE_KEY`/`SUPABASE_SECRET_KEY` and `ANON_KEY`/`SERVICE_ROLE_KEY` is not explained in the clue.
- How the custom access token hook modifies token claims and how those modified claims flow to RLS evaluation cannot be determined from the available evidence.
