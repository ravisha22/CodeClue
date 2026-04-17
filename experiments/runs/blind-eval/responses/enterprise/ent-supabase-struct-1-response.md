# Enterprise Eval: ent-supabase-struct-1
Date: 2026-04-17

## Question
What are the major services in a Supabase project and how are they arranged?

---

## Reasoning Trace
- The strongest structural evidence lives in `apps/studio/`, the `packages/pg-meta/` package, the edge-functions example path, and the example `SupabaseService` methods that fan out into auth, storage, and data access (TREE; INDEX; `SupabaseService` entries in `examples/user-management/*/supabase.service.ts`; `ProjectServiceStatus` in `apps/studio/data/service-status/service-status-query.ts:17-40`; `ProjectRestartServicesVariables` in `apps/studio/data/projects/project-restart-services-mutation.ts:6-7`).
- Those clues support a multi-service project shape, but they do **not** enumerate every backend component or a full deployment diagram.

## Answer
From the clue alone, a Supabase project appears to be organized around a **Studio/admin surface** plus several backend capabilities behind one Supabase client.

1. **Studio is one major surface.** The repository has a large `apps/studio/` application in TREE, and project-level service operations live under Studio data modules such as `ProjectServiceStatus` and `ProjectRestartServicesVariables`, which implies Studio is the control plane used to inspect and operate project services (`TREE`; `ProjectServiceStatus`, `apps/studio/data/service-status/service-status-query.ts:17-40`; `ProjectRestartServicesVariables`, `apps/studio/data/projects/project-restart-services-mutation.ts:6-7`).

2. **Auth is a distinct service area.** The example clients call `this.supabase.auth.signInWithOtp`, `this.supabase.auth.signOut`, `this.supabase.auth.getUser`, and `this.supabase.auth.getClaims`, so authentication/session handling is a separate capability exposed off the Supabase client (`SupabaseService.signIn`, `examples/user-management/angular-user-management/src/app/supabase.service.ts:42-44`; `SupabaseService.signOut`, `examples/user-management/angular-user-management/src/app/supabase.service.ts:46-48`; `SupabaseService.getUser`, `examples/user-management/angular-user-management/src/app/supabase.service.ts:22-28`; `SupabaseService.session`, `examples/user-management/ionic-angular-user-management/src/app/supabase.service.ts:29-38`).

3. **Storage is another distinct service area.** File operations route through `this.supabase.storage.from`, which shows storage is exposed as its own subsystem alongside auth and table access (`SupabaseService.downLoadImage`, `examples/user-management/angular-user-management/src/app/supabase.service.ts:59-61`; `SupabaseService.uploadAvatar`, `examples/user-management/angular-user-management/src/app/supabase.service.ts:63-65`).

4. **Database/table access is another major capability.** Profile reads and writes go through `this.supabase.from`, and the repo also contains `packages/pg-meta/` plus an edge-functions example with `DenoPostgresDriver`, which together indicate first-class Postgres-oriented/database tooling in the project layout (`SupabaseService.updateProfile`, `examples/user-management/angular-user-management/src/app/supabase.service.ts:50-57`; `SupabaseService.profile`, `examples/user-management/ionic-angular-user-management/src/app/supabase.service.ts:40-46`; INDEX entry `packages/pg-meta/src/query/QueryFilter.ts`; INDEX entry `examples/edge-functions/supabase/functions/kysely-postgres/DenoPostgresDriver.ts`).

5. **Edge/serverless functions are arranged as another surface.** The INDEX explicitly includes `examples/edge-functions/supabase/functions/...`, so edge functions are represented as a separate part of the ecosystem rather than folded into Studio (`examples/edge-functions/supabase/functions/kysely-postgres/DenoPostgresDriver.ts`, INDEX).

6. **Arrangement:** the clue suggests a layout where Studio/control-plane code lives under `apps/studio/`, shared packages such as `pg-meta` live under `packages/`, and client-facing service calls are grouped under one `this.supabase` client with sub-APIs for auth, storage, and table/database operations (`TREE`; `SupabaseService`, `examples/user-management/angular-user-management/src/app/supabase.service.ts:15-66`; `SupabaseService`, `examples/user-management/ionic-angular-user-management/src/app/supabase.service.ts:15-87`).

## Gaps / Unresolved
The `GAPS` block says uncovered symbols include `supabase` and `supabaseAdmin`, so the clue does **not** let me reliably determine the full canonical service list, nor whether components like an API gateway, Realtime, or a connection pooler sit in front of the others. It also does not establish a full runtime topology beyond the Studio/data/example structure shown (`GAPS`, `ent-supabase-struct-1-v23.prompt.md`).
