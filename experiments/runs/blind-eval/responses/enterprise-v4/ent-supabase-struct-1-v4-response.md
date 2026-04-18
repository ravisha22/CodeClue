# Enterprise v4 (full-stack): ent-supabase-struct-1
Date: 2026-04-18

## Answer
The prompt’s architecture section already frames Supabase as a federation of services around a central Postgres core, with Studio acting as the project-scoped control plane over that federation. A Supabase project includes Postgres, Studio, GoTrue/Auth, PostgREST/API, Realtime, Storage, Deno Edge Functions, postgres-meta, Supavisor, and Kong. Kong sits in front as the API gateway, while Postgres remains the underlying core instead of being abstracted away from users. The prompt also makes clear that users can still reach Postgres directly with full privileges, and that postgres-meta is part of the management layer around it. Supavisor fits into that layout as the cloud-native, multi-tenant Postgres connection pooler.

## Synthesis
Supabase arranges a direct-access Postgres core behind Kong and around specialized services, with Studio and postgres-meta managing the project and Supavisor pooling connections.
