# Enterprise v2 TS scoring

Scored against recalibrated gold facts. COVERED = specific mechanism/fact supported (>50%); otherwise MISS.

### ent-maybe-struct-1 (0/4)
- F1: **MISS** — UI/controller inventory, not the README positioning as a personal-finance app / fully working application.
- F2: **MISS** — No mention of docs/hosting/docker.md.
- F3: **MISS** — Mentions README sections only, not the self-hoster-vs-developer split or redirect to Docker guide.
- F4: **MISS** — Discusses chat UI, not the /api/v1/chats API surface.

### ent-maybe-struct-2 (0/4)
- F1: **MISS** — No Docker Engine prerequisite or hello-world verification.
- F2: **MISS** — No compose.yml downloaded from compose.example.yml.
- F3: **MISS** — Mentions env config generally, but not a local .env with both SECRET_KEY_BASE and POSTGRES_PASSWORD.
- F4: **MISS** — No docker compose up / up -d / ls runtime flow.

### ent-maybe-rel-1 (0/4)
- F1: **MISS** — Says auth is undocumented; does not give OAuth2/API keys plus ai_enabled requirement.
- F2: **MISS** — No read-scope mapping for GET chat endpoints.
- F3: **MISS** — No write-scope mapping for create/update/delete/message operations.
- F4: **MISS** — No unauthorized-vs-forbidden error distinction.

### ent-maybe-rel-2 (0/4)
- F1: **MISS** — No List Chats payload with chats array and pagination fields.
- F2: **MISS** — No Get Chat messages array with user_message and assistant_message records.
- F3: **MISS** — No assistant-message model field or tool_calls array.
- F4: **MISS** — Explicitly says tool calls are not documented.

### ent-maybe-mech-1 (0/4)
- F1: **MISS** — No POST /api/v1/chats request/response contract.
- F2: **MISS** — No immediate user-message response with ai_response_status=pending.
- F3: **MISS** — No asynchronous/background AI processing behavior.
- F4: **MISS** — messagesObserver is not the documented poll-the-chat-endpoint flow for assistant_message.

### ent-maybe-mech-2 (0/4)
- F1: **MISS** — No ghcr.io/maybe-finance/maybe image/tags.
- F2: **MISS** — No statement that self-hosted installs do not auto-update.
- F3: **MISS** — Explicitly says the update path is undocumented.
- F4: **MISS** — No ActiveRecord::DatabaseConnectionError recovery sequence.

### ent-calcom-struct-1 (1/4)
- F1: **MISS** — Gets the Next.js app layout, but not the full stack claim (tRPC/React/Tailwind/Prisma/Daily.co).
- F2: **COVERED** — Describes apps/api/v2 as a separate API v2 runtime/service.
- F3: **MISS** — Notes platform atoms wrappers, but not the embeddable-package support matrix (React 18/19, Next 14/15).
- F4: **MISS** — Mentions example apps generally, not the platform example app for local/backend integration testing.

### ent-calcom-struct-2 (0/4)
- F1: **MISS** — Says community edition / use-at-your-own-risk, but not the explicit personal non-production recommendation.
- F2: **MISS** — Does not list the Cal.com-only teams/orgs/instant-meeting feature set.
- F3: **MISS** — Does not give the Cal.com-only enterprise feature list; instead points to enterprise artifacts in the codebase.
- F4: **MISS** — Does not list the features Cal.diy still includes.

### ent-calcom-rel-1 (0/4)
- F1: **MISS** — No router entry via formId plus URL field values.
- F2: **MISS** — No field-type / required-field validation step.
- F3: **MISS** — No eventTypeRedirect -> routedTeamMemberIds booking redirect.
- F4: **MISS** — No slot filtering/blocking/recheck-before-email-webhook flow.

### ent-calcom-rel-2 (1/4)
- F1: **COVERED** — Lists many lifecycle webhook triggers, though it is still less precise than the gold set.
- F2: **MISS** — Does not specifically say created bookings are their own event family with a structured booking payload.
- F3: **MISS** — Does not describe cancel/reschedule payload variants.
- F4: **MISS** — Does not document a separate outbound transport/signing step.

### ent-calcom-mech-1 (2/4)
- F1: **COVERED** — Enumerates the four cancellation-reason requirement enum values.
- F2: **MISS** — No default-to-MANDATORY_HOST_ONLY behavior for null / no eventTypeId.
- F3: **COVERED** — Explains that enforcement depends on who is canceling and the configured requirement before cancellation proceeds.
- F4: **MISS** — Discusses display components, not a cancellation UI that mirrors the requirement on the client form.

### ent-calcom-mech-2 (0/4)
- F1: **MISS** — Describes example-app/API pieces, but not the shared root+API+example config requirement for local OAuth testing.
- F2: **MISS** — No API v2 setup tooling/scripts for OAuth test secrets.
- F3: **MISS** — Does not clearly separate client-facing example settings from backend secret config.
- F4: **MISS** — No localhost:4321 code exchange / refresh-token / availability-sync flow.

### ent-supabase-struct-1 (1/4)
- F1: **COVERED** — Lists most major services: Postgres, Studio, Auth, Storage, Edge Functions, pg-meta, and an API gateway.
- F2: **MISS** — Does not name Kong; says the gateway technology is unclear.
- F3: **MISS** — Calls Postgres the core data layer, but not the not-abstracted-away / full-privileges claim.
- F4: **MISS** — Does not mention Supavisor.

### ent-supabase-struct-2 (2/4)
- F1: **COVERED** — Separate client endpoints and temporary keys support the separate-environment / separate-credentials claim.
- F2: **MISS** — No ephemeral preview-branch pause/delete behavior.
- F3: **MISS** — No persistent-branch recommendation for staging/QA/dev.
- F4: **COVERED** — Describes isolation via scoped endpoints/keys/sessions, i.e. more than lightweight git labels.

### ent-supabase-rel-1 (1/4)
- F1: **COVERED** — Distinguishes project/API keys from user-auth token flows.
- F2: **MISS** — Does not explain anon/publishable keys plus anon/authenticated roles with RLS.
- F3: **MISS** — Does not explain backend-only secret/service_role keys bypassing RLS.
- F4: **MISS** — Does not explain Auth JWTs scoping row access through RLS.

### ent-supabase-rel-2 (2/4)
- F1: **COVERED** — Clearly says projects can be transferred between organizations.
- F2: **MISS** — Mentions target-org membership, but not the source-org ownership requirement.
- F3: **COVERED** — The preview/validation flow supports the idea that extra platform constraints exist beyond simple permission checks.
- F4: **MISS** — Does not mention integrations or config blocking transfers.

### ent-supabase-mech-1 (3/4)
- F1: **COVERED** — Describes a Realtime server/client layer coordinating Postgres-backed publications with client channels.
- F2: **COVERED** — Explains publications forwarding database changes to subscribed clients.
- F3: **COVERED** — Explains broadcast as a separate message fan-out path.
- F4: **MISS** — Auth is discussed at connection level, but not explicit authorization gating for private/broadcast delivery.

### ent-supabase-mech-2 (2/4)
- F1: **COVERED** — Describes cron as database-native Postgres scheduling with run-history support.
- F2: **MISS** — Does not say jobs can be created via SQL or Dashboard or specify the every-second-to-year cadence range.
- F3: **MISS** — Only speculates about SQL/functions/HTTP job types; no concrete support.
- F4: **COVERED** — Job counts plus run-history support a database-backed scheduler storing jobs/executions.

## Summary by repo

| Repo | Tasks | Covered facts | Total facts | Coverage |
|---|---:|---:|---:|---:|
| Maybe | 6 | 0 | 24 | 0% |
| Cal.com | 6 | 4 | 24 | 17% |
| Supabase | 6 | 11 | 24 | 46% |
| **Overall** | **18** | **15** | **72** | **21%** |

## Summary by type

| Type | Tasks | Covered facts | Total facts | Coverage |
|---|---:|---:|---:|---:|
| Structural | 6 | 4 | 24 | 17% |
| Relational | 6 | 4 | 24 | 17% |
| Mechanistic | 6 | 7 | 24 | 29% |
