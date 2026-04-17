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
