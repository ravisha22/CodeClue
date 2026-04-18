# Enterprise v4 (full-stack): ent-supabase-mech-1
Date: 2026-04-18

## Answer
The prompt’s Realtime UI and hook code show the client side of a dedicated Realtime service rather than a feature baked directly into Studio. Under the hood, that service keeps client connections and listens to Postgres-backed change sources, then forwards subscribed database changes to connected clients. It also has a second fan-out path for app-originated broadcasts, so database replication events and broadcast messages are related but distinct flows. The same prompt surfaces separate broadcast/presence controls and auth setup, which aligns with private or broadcast channels being authorization-gated. So Realtime moves data by bridging Postgres change streams and broadcast events into authorized client subscriptions.

## Synthesis
Supabase Realtime is a separate service that turns Postgres changes and broadcast events into authorized client-channel updates.
