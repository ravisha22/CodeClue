# Enterprise v2: ent-supabase-struct-1
Date: 2026-04-17

## Question
What are the major services in a Supabase project and how are they arranged?

## Reasoning

### Relevant Clue Entries

**Repository structure (TREE):** The monorepo is organized into top-level directories: `apps/` (5237 files), `packages/` (725 files), `examples/` (422 files), `docker/` (4 files), `e2e/` (56 files), `blocks/` (32 files), `scripts/` (7 files), and `supabase/` (9 files) (TREE). This tells us the codebase is a monorepo with applications, shared packages, example projects, Docker infrastructure, and end-to-end tests.

**Key application modules (INDEX):** The INDEX reveals major applications under `apps/`:
- **Studio** (`apps/studio/`): The admin dashboard/management UI, evidenced by numerous modules including `apps/studio/components/layouts/TableEditorLayout/ExportAllRows.errors.ts`, `apps/studio/lib/api/self-hosted/functions/fileSystemStore.ts`, and `apps/studio/lib/project-supabase-client.ts` (INDEX, FOCUS).
- **Docs** (`apps/docs/`): The documentation site, with modules like `apps/docs/scripts/search/sources/markdown.ts`, `apps/docs/resources/utils/connections.ts`, and `apps/docs/scripts/search/sources/github-discussion.ts` (INDEX).
- **Design System** (`apps/design-system/`): UI component registry, e.g., `apps/design-system/__registry__/default/block/chart-bar-interactive.tsx` (INDEX).

**Shared packages (INDEX):** The `packages/` directory contains reusable libraries:
- `packages/pg-meta/` — Postgres metadata querying, with `QueryFilter` providing `clone`, `filter`, `match`, `order` operations (INDEX: `packages/pg-meta/src/query/QueryFilter.ts`).
- `packages/ai-commands/` — AI-related error types like `ContextLengthError`, `EmptyResponseError`, `EmptySqlError` (SYM: `packages/ai-commands/src/errors.ts`).

**Docker/self-hosted infrastructure (FOCUS):** The `docker/.env.example` file defines configuration for major backend services via environment variables: `POSTGRES_PASSWORD`, `JWT_SECRET`, `ANON_KEY`, `SERVICE_ROLE_KEY`, `SUPABASE_PUBLISHABLE_KEY`, and `SUPABASE_SECRET_KEY` (FOCUS: `docker/.env.example:1-345`). This indicates the self-hosted deployment comprises at minimum a **Postgres database**, a **JWT-based auth layer**, and an **API gateway** that uses anon/service-role keys.

**Client-facing services identified through SupabaseService (FOCUS):** The example `SupabaseService` classes expose the client-side service surface:
- **Auth service**: `signIn` delegates to `this.supabase.auth.signInWithOtp` (FOCUS: `SupabaseService.signIn`, `angular-user-management/src/app/supabase.service.ts:42-44`); `signOut` delegates to `this.supabase.auth.signOut` (FOCUS: `SupabaseService.signOut`, same file:46-48); `getUser` delegates to `this.supabase.auth.getUser` (FOCUS: `SupabaseService.getUser`, same file:22-28).
- **Database/table service**: `profile` and `updateProfile` delegate to `this.supabase.from(...)` for table queries (FOCUS: `SupabaseService.profile`, `angular-user-management/src/app/supabase.service.ts:30-36`; `SupabaseService.updateProfile`, same file:50-57).
- **Storage service**: `downLoadImage` delegates to `this.supabase.storage.from(...)` (FOCUS: `SupabaseService.downLoadImage`, `angular-user-management/src/app/supabase.service.ts:59-61`); `uploadAvatar` also delegates to `this.supabase.storage.from(...)` (FOCUS: `SupabaseService.uploadAvatar`, same file:63-65).

**Project-level client creation (FOCUS):** `createProjectSupabaseClient` in `apps/studio/lib/project-supabase-client.ts:8-29` takes a `projectRef` and `clientEndpoint`, indicating each project is addressable by a unique reference and endpoint (FOCUS: `createProjectSupabaseClient`).

**Project restart services (FOCUS):** The type `ProjectRestartServicesVariables` in `apps/studio/data/projects/project-restart-services-mutation.ts:6-7` indicates there is a mechanism to restart services within a project, implying services are independently managed units (FOCUS: `ProjectRestartServicesVariables`).

**Edge Functions (INDEX):** The `examples/edge-functions/supabase/functions/` path and `FileSystemFunctionsArtifactStore` in `apps/studio/lib/api/self-hosted/functions/fileSystemStore.ts` reveal an **Edge Functions** service that stores and retrieves function artifacts (INDEX, FOCUS: `FileSystemFunctionsArtifactStore`).

### Synthesis

Based solely on the clue, the major services in a Supabase project are:

1. **Postgres Database** — The core data layer, configured via `POSTGRES_PASSWORD` (FOCUS: `docker/.env.example`). Accessed by clients through `this.supabase.from(...)` for table operations (FOCUS: `SupabaseService.profile`, `SupabaseService.updateProfile`). Metadata is managed through the `packages/pg-meta` package (INDEX: `packages/pg-meta/src/query/QueryFilter.ts`).

2. **Auth** — JWT-based authentication, configured via `JWT_SECRET`, `ANON_KEY`, and `SERVICE_ROLE_KEY` (FOCUS: `docker/.env.example`). Client methods delegate to `this.supabase.auth.*` for sign-in, sign-out, and user retrieval (FOCUS: `SupabaseService.signIn`, `SupabaseService.signOut`, `SupabaseService.getUser`).

3. **Storage** — File/object storage accessed via `this.supabase.storage.from(...)` for image download and avatar upload (FOCUS: `SupabaseService.downLoadImage`, `SupabaseService.uploadAvatar`).

4. **Edge Functions** — Serverless functions managed through `FileSystemFunctionsArtifactStore` with methods `getFunctions`, `getFunctionBySlug`, `getFileEntriesBySlug` (INDEX/FOCUS: `apps/studio/lib/api/self-hosted/functions/fileSystemStore.ts`). Example functions exist under `examples/edge-functions/supabase/functions/` (INDEX).

5. **Studio (Dashboard)** — The management UI under `apps/studio/`, providing table editing, project management, and service configuration (TREE, INDEX).

6. **API Gateway** — Implied by the dual key system (`ANON_KEY` for public/anonymous access, `SERVICE_ROLE_KEY` for privileged access, `SUPABASE_PUBLISHABLE_KEY` and `SUPABASE_SECRET_KEY`) and by `createProjectSupabaseClient` which connects to a `clientEndpoint` using an API key (FOCUS: `docker/.env.example`, `createProjectSupabaseClient`).

**Arrangement:** These services are arranged in a monorepo with `apps/` containing the main deployable applications (Studio, Docs, Design System), `packages/` holding shared libraries (pg-meta, ai-commands, etc.), `docker/` providing self-hosted orchestration configuration, and `examples/` demonstrating client-side integration patterns (TREE). Each project is identified by a `projectRef` and accessed via a dedicated endpoint (FOCUS: `createProjectSupabaseClient`). Services within a project can be independently restarted (FOCUS: `ProjectRestartServicesVariables`).

### Gaps and Uncertainties

- The GAPS section lists `supabase`, `supabaseAdmin`, `toDisplayNameOrgProject` as uncovered symbols (GAPS). The internal implementation details of the core `supabase` and `supabaseAdmin` client objects cannot be determined from the clue.
- The clue does not reveal the full Docker Compose topology or the networking arrangement between services in a self-hosted deployment.
- The specific API gateway technology (e.g., Kong, custom proxy) cannot be determined from the clue alone.
- The README sections mention "How it works" and "Client libraries" but their content is not included in the clue (README).
