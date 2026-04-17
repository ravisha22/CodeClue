# Enterprise Eval: ent-supabase-mech-1
Date: 2026-04-17

## Question
How does Realtime move database changes and broadcasts from Postgres to clients?

---

## Reasoning Trace
- The strongest evidence is in the Realtime inspector path: `useRealtimeMessages`, `RealtimeFilterPopover`, `updateTableRealtime`, and the broadcast/database-role telemetry event types (`useRealtimeMessages`, `apps/studio/components/interfaces/Realtime/Inspector/useRealtimeMessages.ts:56-241`; `RealtimeFilterPopover`, `apps/studio/components/interfaces/Realtime/Inspector/RealtimeFilterPopover/index.tsx:34-260`; `updateTableRealtime`, `apps/studio/components/interfaces/TableGridEditor/SidePanelEditor/SidePanelEditor.tsx:469-557`; `RealtimeInspectorBroadcastSentEvent`, `packages/common/telemetry-constants.ts:463-468`; `RealtimeInspectorDatabaseRoleUpdatedEvent`, `packages/common/telemetry-constants.ts:511-516`).
- The drill-down source snippet only confirms that `IconDatabaseChanges` is a UI icon wrapper; it does not add transport logic (`IconDatabaseChanges`, `packages/ui/src/components/Icon/icons/IconDatabaseChanges/IconDatabaseChanges.tsx:31-34`).

## Answer
From the clue, the visible mechanism is: **table/publication settings feed a Realtime client, and that client authenticates, opens channel listeners, and delivers database-change/broadcast events into the inspector UI.**

1. **Realtime subscribes on a client/channel abstraction.** `useRealtimeMessages` guards on `enabled`, sets auth with `realtimeClient.setAuth`, disconnects with `realtimeClient.disconnect`, and registers handlers with `newChannel.on`. That shows the client side receives Realtime data by authenticating a Realtime client and attaching channel listeners (`useRealtimeMessages`, `apps/studio/components/interfaces/Realtime/Inspector/useRealtimeMessages.ts:56-241`).

2. **Database changes are tied to publication/table configuration.** `updateTableRealtime(table, enabled)` has `PRECEDENCE(realtimePublication)` and uses `pub.name`, `table.schema`, and `table.name`, which indicates database-change streaming is associated with a named publication and specific schema/table targets (`updateTableRealtime`, `apps/studio/components/interfaces/TableGridEditor/SidePanelEditor/SidePanelEditor.tsx:469-557`).

3. **Broadcast is a separately configurable event path in the same inspector flow.** `RealtimeFilterPopover` exposes `publication.name`, `config.table`, `tempConfig.enablePresence`, and `tempConfig.enableBroadcast`, and the telemetry constants include `RealtimeInspectorBroadcastSentEvent`. Together that supports a separate broadcast toggle/event stream alongside table-change inspection (`RealtimeFilterPopover`, `apps/studio/components/interfaces/Realtime/Inspector/RealtimeFilterPopover/index.tsx:34-260`; `RealtimeInspectorBroadcastSentEvent`, `packages/common/telemetry-constants.ts:463-468`).

4. **Database-role changes are also part of the observed Realtime surface.** The telemetry constant `RealtimeInspectorDatabaseRoleUpdatedEvent` suggests the inspector also tracks database-role-related Realtime activity, not just row changes or broadcasts (`RealtimeInspectorDatabaseRoleUpdatedEvent`, `packages/common/telemetry-constants.ts:511-516`).

## Gaps / Unresolved
The clue does **not** reveal the lower-level transport and replication internals. I cannot determine from the provided evidence alone:
- whether the client transport is specifically WebSockets,
- whether Postgres changes arrive through WAL reading or a replication slot,
- whether broadcast uses a specific table such as `realtime.messages`,
- or how messages are routed across nodes or regions.

So the clue supports the **client-side subscription/configuration path**, but not the full backend replication pipeline.
