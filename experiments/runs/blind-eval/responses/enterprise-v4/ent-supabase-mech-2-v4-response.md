# Enterprise v4 (full-stack): ent-supabase-mech-2
Date: 2026-04-18

## Answer
The prompt places Cron under the project’s database tooling, which fits the documented execution model: Supabase Cron is a Postgres module that schedules recurring jobs and records their runs. Jobs can be created either through SQL or through the Dashboard, and the supported cadence ranges from every second up to once a year. The actual job body can run SQL directly, invoke database functions, or make HTTP requests to other services such as Edge Functions. Both the scheduled definitions and the run history live in the database-backed scheduler layer that Studio queries and displays. In other words, Cron is database-native scheduling that can still reach outward into the rest of the Supabase platform.

## Synthesis
Supabase Cron executes from a Postgres-backed scheduler, but its jobs can call SQL, functions, or HTTP services like Edge Functions.
