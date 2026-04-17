### ent-supabase-struct-1 (1/4)
- F1: COVERED — The response identifies more than half of the listed service surfaces from the clue-backed answer: Studio, Auth, Storage, database/Postgres-oriented access, Edge Functions, and `pg-meta`, with explicit citations. It misses Realtime, Supavisor, and Kong.
- F2: MISS — It explicitly says the clue does not establish an API gateway in front of the services, so it does not describe Kong as that gateway.
- F3: MISS — It mentions Postgres-oriented tooling, but does not state that Postgres is the core of Supabase, is not abstracted away, or is accessible with full privileges.
- F4: MISS — It does not describe Supavisor as a cloud-native multi-tenant Postgres connection pooler.

### ent-supabase-struct-2 (1/4)
- F1: COVERED — The response says branches/project refs get distinct `clientEndpoint` values and temporary API keys via `getOrRefreshTemporaryApiKey(projectRef)`, which covers separate environments with their own credentials, though it does not explicitly prove “own Supabase instance.”
- F2: MISS — It explicitly marks preview-branch ephemerality, inactivity cleanup, and PR-close/merge behavior as unresolved.
- F3: MISS — It does not state that persistent branches are long-lived or recommended for staging, QA, or development.
- F4: MISS — It explicitly says the clue does not establish data-less branch creation or the exact isolation scope across schema/data, storage, Edge Functions, and auth configuration.

### ent-supabase-rel-1 (1/4)
- F1: COVERED — The response clearly separates project/API credentials from auth/session tokens and says auth tokens identify user sessions, matching the gold fact.
- F2: MISS — Although it mentions `publishableKey` and `anonKey`, it does not say they are public-facing, does not tie them to RLS, and does not identify the `anon` and `authenticated` Postgres roles.
- F3: MISS — It notes a management token path, but does not identify secret or `service_role` keys, backend-only usage, or RLS bypass through `service_role`.
- F4: MISS — It explicitly says the clue does not connect JWT claims to row-by-row RLS policy enforcement.

### ent-supabase-rel-2 (1/4)
- F1: COVERED — The response explicitly says projects are transferable and grounds that in the dedicated preview query and transfer mutation.
- F2: MISS — It does not establish the source-organization ownership plus target-organization membership rule; it marks exact permission rules as unresolved.
- F3: MISS — It does not mention region immobility.
- F4: MISS — It mentions project roles only as surrounding context and explicitly says GitHub integration, log drains, and concrete blockers are not derivable from the clue.

### ent-supabase-mech-1 (0/4)
- F1: MISS — It describes authenticated client/channel listeners, but does not state that clients connect to cluster nodes over WebSockets.
- F2: MISS — It mentions publication/table configuration, but not initialization of `postgres_changes`, replication slots, or Postgres streaming internals.
- F3: MISS — It does not identify a `realtime.messages` publication, WAL reading, or JSON packaging on insert.
- F4: MISS — It notes auth and broadcast toggles, but does not establish Realtime Authorization for broadcast/private channels or global cross-region routing.

### ent-supabase-mech-2 (1/4)
- F1: COVERED — The response characterizes Cron as database-native scheduling/monitoring tied to project/database connection context, which covers more than half of the “Postgres module for scheduling recurring jobs and monitoring job runs inside Postgres” fact.
- F2: MISS — It does not say jobs can be created via SQL or Dashboard, nor that schedules range from every second to once a year.
- F3: MISS — It does not identify job targets such as SQL snippets, database functions, HTTP requests, or Edge Functions.
- F4: MISS — It explicitly says `pg_cron`, `cron.job`, and `cron.job_run_details` are not visible from the clue.

## Summary
| task_id | score | covered | missed |
|---|---:|---:|---:|
| ent-supabase-struct-1 | 1/4 | 1 | 3 |
| ent-supabase-struct-2 | 1/4 | 1 | 3 |
| ent-supabase-rel-1 | 1/4 | 1 | 3 |
| ent-supabase-rel-2 | 1/4 | 1 | 3 |
| ent-supabase-mech-1 | 0/4 | 0 | 4 |
| ent-supabase-mech-2 | 1/4 | 1 | 3 |
