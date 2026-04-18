# Enterprise v4 (full-stack): ent-supabase-rel-1
Date: 2026-04-18

## Answer
The prompt exposes the key pieces of Supabase’s access model together: project API keys in env/config, GoTrue-based auth, and database-facing roles. API keys identify the application component making the request, while Supabase Auth tokens identify the user behind that request. Public-facing publishable and anon keys are therefore designed to work with Row Level Security, relying on the `anon` and `authenticated` Postgres roles for row access. Secret and `service_role` keys are the backend-only exception: they use the privileged `service_role` role and bypass RLS. Auth JWTs bridge the two layers by carrying user identity into Postgres so RLS policies can scope which rows that authenticated user may access.

## Synthesis
Supabase combines app-level keys, user-level auth tokens, and Postgres RLS so public clients stay policy-bound while backend `service_role` clients bypass those row checks.
