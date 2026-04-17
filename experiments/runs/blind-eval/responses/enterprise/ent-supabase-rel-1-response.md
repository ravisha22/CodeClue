# Enterprise Eval: ent-supabase-rel-1
Date: 2026-04-17

## Question
How do API keys, auth tokens, and RLS work together in Supabase's access model?

---

## Reasoning Trace
- The key evidence is the split between project/API-key surfaces (`projectKeys.publishableKey`, `projectKeys.anonKey`, access-token queries, management API token) and auth/session surfaces (`auth.signInWithOtp`, `auth.getUser`, `auth.getClaims`).
- `DataApiAccessType` and `ApiAccessRole` show that data access is role/grant mediated.
- The clue is thin on explicit RLS semantics, so anything beyond that must be marked uncertain.

## Answer
The clue shows **three related but distinct layers** in the access model: project/API credentials, user auth/session tokens, and data-access roles/grants.

1. **API keys and access tokens are one credential layer.** Studio exposes `projectKeys.apiUrl`, `projectKeys.publishableKey`, and `projectKeys.anonKey`, and the repo has dedicated access-token and scoped-access-token query types. That indicates Supabase treats project keys and access tokens as explicit API credentials managed separately from user sessions (`ApiKeysTabContent`, `apps/studio/components/interfaces/Connect/ApiKeysTabContent.tsx:24-76`; `AccessTokensData`, `apps/studio/data/access-tokens/access-tokens-query.ts:14-18`; `ScopedAccessTokensData`, `apps/studio/data/scoped-access-tokens/scoped-access-token-query.ts:28-35`).

2. **User auth tokens are a separate identity layer.** The example clients authenticate with `auth.signInWithOtp`, fetch identity via `auth.getUser`, and read token claims via `auth.getClaims`. That means auth/session tokens identify a user session, while API keys/access tokens are not the only credential in play (`SupabaseService.signIn`, `examples/user-management/angular-user-management/src/app/supabase.service.ts:42-44`; `SupabaseService.getUser`, `examples/user-management/angular-user-management/src/app/supabase.service.ts:22-28`; `SupabaseService.session`, `examples/user-management/ionic-angular-user-management/src/app/supabase.service.ts:29-38`).

3. **Data access is mediated by roles/grants, not just by exposing an endpoint.** `isApiAccessRole` validates membership in `API_ACCESS_ROLES`, and `DataApiAccessType` distinguishes `'none'`, `'exposed-schema-no-grants'`, and `'access'`. So the clue supports a model where schema exposure alone is insufficient; some role/grant condition must also be satisfied to get actual API access (`isApiAccessRole`, `apps/studio/lib/data-api-types.ts:6-9`; `ApiAccessRole`, `apps/studio/lib/data-api-types.ts:5-5`; `DataApiAccessType`, `apps/studio/data/privileges/table-api-access-query.ts:63-64`).

4. **There is also a backend/management credential path distinct from user auth.** `forwardToSupabaseAPI` uses `process.env.SUPABASE_MANAGEMENT_API_TOKEN` and separately checks `userHasPermissionForProj`, which suggests privileged backend API access is handled differently from end-user auth/session state (`forwardToSupabaseAPI`, `apps/ui-library/registry/default/platform/platform-kit-nextjs/app/api/supabase-proxy/[...path]/route.ts:2-81`).

## Gaps / Unresolved
The clue does **not** explicitly define RLS, name the `anon`/`authenticated`/`service_role` Postgres roles, or say which keys bypass RLS. It also does not explicitly connect JWT claims to row-by-row policy evaluation. The most I can support is that auth claims exist and that data access depends on roles/grants (`SupabaseService.session`, `examples/user-management/ionic-angular-user-management/src/app/supabase.service.ts:29-38`; `DataApiAccessType`, `apps/studio/data/privileges/table-api-access-query.ts:63-64`; `GAPS`, `ent-supabase-rel-1-v23.prompt.md`).
