# Enterprise v2: ent-supabase-mech-1
Date: 2026-04-17

## Question
How does Realtime move database changes and broadcasts from Postgres to clients?

## Reasoning

### Relevant Clue Entries

**Realtime message consumption (FOCUS):** `useRealtimeMessages` at `apps/studio/components/interfaces/Realtime/Inspector/useRealtimeMessages.ts:56-241` is the central hook for consuming Realtime messages. Its signature is `useRealtimeMessages(config: RealtimeConfig, setRealtimeConfig: Dispatch<SetSt...>)`. Its behavior annotation is `GUARD(!enabled -> return); PRECEDENCE(not_enabled -> bearer -> not_client -> default)` and it uses `supabase.co`, `realtimeClient.setAuth`, `realtimeClient.disconnect`, `newChannel.on` (FOCUS: `useRealtimeMessages`).

Key observations from this entry:
- **Guard on enabled:** The hook only proceeds if the Realtime feature is enabled (`GUARD(!enabled -> return)`).
- **Auth precedence:** The behavior `PRECEDENCE(not_enabled -> bearer -> not_client -> default)` suggests authentication is applied to the Realtime connection — a bearer token is checked, then the client connection is established or a default path is taken.
- **Client lifecycle:** `realtimeClient.setAuth` sets authentication on the Realtime client, `realtimeClient.disconnect` manages disconnection, and `newChannel.on` subscribes to events on a channel. This shows a WebSocket-like channel-subscription model.
- **Domain reference:** Uses `supabase.co`, indicating the Realtime client connects to a Supabase-hosted endpoint.

**Realtime filter configuration (FOCUS):** `RealtimeFilterPopover` at `apps/studio/components/interfaces/Realtime/Inspector/RealtimeFilterPopover/index.tsx:34-260` takes `{ config, onChangeConfig }` and uses `publication.name`, `config.table`, `tempConfig.enablePresence`, `tempConfig.enableBroadcast` (FOCUS: `RealtimeFilterPopover`).

Key observations:
- **Publication-based:** The filter references `publication.name`, indicating Realtime uses Postgres **publications** to define which table changes are captured. A publication is a Postgres logical replication concept that selects a set of tables whose changes are emitted.
- **Per-table configuration:** `config.table` shows changes can be filtered to a specific table.
- **Multiple Realtime modes:** `tempConfig.enablePresence` and `tempConfig.enableBroadcast` reveal at least three distinct Realtime capabilities: **database changes** (via publications), **presence** (tracking connected users), and **broadcast** (arbitrary message distribution).

**Table-level Realtime toggling (FOCUS):** `updateTableRealtime` at `apps/studio/components/interfaces/TableGridEditor/SidePanelEditor/SidePanelEditor.tsx:469-557` has signature `updateTableRealtime(table: RetrieveTableResult, enabled: boolean)` with `behavior: PRECEDENCE(realtimePublication); TRANSFORM(map)` and uses `console.error`, `pub.name`, `table.schema`, `table.name` (FOCUS: `updateTableRealtime`).

Key observations:
- **Publication management:** The behavior `PRECEDENCE(realtimePublication)` and usage of `pub.name` confirm that enabling/disabling Realtime for a table involves adding or removing it from a **Realtime publication**.
- **Schema and table granularity:** The function uses both `table.schema` and `table.name`, showing that Realtime change tracking is configured at the schema.table level.

**Realtime telemetry events (FOCUS):**
- `RealtimeInspectorDatabaseRoleUpdatedEvent` at `packages/common/telemetry-constants.ts:511-516` is an interface tracking when the database role used by the Realtime inspector is updated (FOCUS: `RealtimeInspectorDatabaseRoleUpdatedEvent`). This reveals that Realtime connections run under a specific **database role**, and changing that role is a tracked event.
- `RealtimeInspectorBroadcastSentEvent` at `packages/common/telemetry-constants.ts:463-468` tracks broadcast-sent events (FOCUS: `RealtimeInspectorBroadcastSentEvent`). This confirms broadcast is a distinct Realtime feature, separate from database changes.

**Database Changes icon (FOCUS + Source Snippet):** `IconDatabaseChanges` at `packages/ui/src/components/Icon/icons/IconDatabaseChanges/IconDatabaseChanges.tsx:31-34` renders an `IconBase` with a custom SVG (Source Snippet: `IconDatabaseChanges`). This is purely a UI icon component and does not reveal mechanism details, but it confirms "Database Changes" is a named concept in the Realtime UI.

**Presence icon (Source Snippet):** The `SvgComponent` at `packages/ui/src/components/Icon/icons/IconPresence/IconPresence.tsx:4-10` renders a Presence icon (Source Snippet: `SvgComponent`), confirming Presence is a visually distinct Realtime feature.

**Realtime marketing page (FOCUS):** `RealtimePage` at `apps/www/pages/realtime.tsx:46-248` uses `PRODUCT_NAMES.REALTIME` and `supabase.com` (FOCUS: `RealtimePage`). This confirms Realtime is a named, first-class product in the Supabase offering.

**Realtime visual component (FOCUS):** `handleMouseMove` at `apps/www/components/Products/RealtimeVisual.tsx:15-36` is a mouse-tracking handler for the Realtime product visualization on the marketing site (FOCUS: `handleMouseMove`). Not mechanistically relevant.

**Database connection and queue infrastructure (FOCUS):** Various `DatabaseQueue*` types (`PostgresQueue`, `PostgresQueueMessage`, `PostgresQueueMetric`) at `apps/studio/data/database-queues/` (FOCUS: `DatabaseQueueData`, `PostgresQueue`, `PostgresQueueMessage`) and `DatabaseConnectionString` at `apps/studio/components/interfaces/Connect/DatabaseConnectionString.tsx:67-637` (FOCUS: `DatabaseConnectionString`) show the project's database infrastructure includes queue-based messaging and configurable connection strings. While not directly Realtime-specific, queues may interact with the Realtime pipeline.

**Postgres triggers (FOCUS):** `PostgresTrigger` at `apps/studio/components/interfaces/Database/Triggers/TriggersList/TriggerList.utils.ts:1-15` is an interface for Postgres triggers (FOCUS: `PostgresTrigger`). Triggers are relevant because database change detection for Realtime may rely on Postgres trigger mechanisms or logical replication.

### Synthesis

Based on the clue and source snippets, the Realtime pipeline from Postgres to clients operates as follows:

1. **Postgres publications as the source:** Database changes are captured via Postgres **publications**. Tables are added to or removed from a Realtime publication using `updateTableRealtime`, which operates on `pub.name` (the publication name) and `table.schema`/`table.name` (FOCUS: `updateTableRealtime`). The `RealtimeFilterPopover` references `publication.name` to select which publication to monitor (FOCUS: `RealtimeFilterPopover`).

2. **Channel-subscription model on the client:** The client connects to a Realtime server (at a `supabase.co` endpoint) and subscribes to channels via `newChannel.on` (FOCUS: `useRealtimeMessages`). This is consistent with a WebSocket-based pub/sub model where clients open a persistent connection and receive events pushed by the server.

3. **Authentication of Realtime connections:** The Realtime client authenticates using `realtimeClient.setAuth` with a bearer token (FOCUS: `useRealtimeMessages`, behavior annotation `PRECEDENCE(... -> bearer -> ...)`). The connection runs under a specific **database role** that can be updated, as tracked by `RealtimeInspectorDatabaseRoleUpdatedEvent` (FOCUS: `RealtimeInspectorDatabaseRoleUpdatedEvent`). This means RLS policies apply to what changes a client can see via Realtime.

4. **Three Realtime modes:**
   - **Database Changes:** Table mutations captured via publications and delivered to subscribed clients (FOCUS: `updateTableRealtime`, `RealtimeFilterPopover` with `config.table`, `IconDatabaseChanges`).
   - **Broadcast:** Arbitrary messages sent to channel subscribers, tracked by `RealtimeInspectorBroadcastSentEvent` (FOCUS: `RealtimeInspectorBroadcastSentEvent`, `tempConfig.enableBroadcast`).
   - **Presence:** Tracks connected users/state, toggled via `tempConfig.enablePresence` (FOCUS: `RealtimeFilterPopover`).

5. **Guard and lifecycle:** The Realtime hook is guarded by an `enabled` flag — if Realtime is disabled, no connection is established (FOCUS: `useRealtimeMessages`, `GUARD(!enabled -> return)`). The client can be disconnected via `realtimeClient.disconnect` (FOCUS: `useRealtimeMessages`).

### Gaps and Uncertainties

- **GAPS type is MECHANISTIC**, indicating body logic is needed for a full answer. The clue covers 83 symbols at L3 with only 12 behavior annotations. Uncovered symbols include `DatabaseQueueError` and `DatabaseQueueVersionData` (GAPS).
- The **server-side Realtime engine** (e.g., how the Realtime server reads from Postgres logical replication slots or WAL, how it fans out to WebSocket connections) is **not visible** in the clue. The clue only shows the client-side subscription and Studio configuration.
- The drill target was `IconDatabaseChanges` (~3 lines), which is only a UI icon and does not illuminate the mechanism. The source snippet for `SvgComponent` (Presence icon) is similarly non-informative mechanistically.
- Whether the Realtime server uses Postgres logical replication (WAL-based), polling, or triggers to detect changes is not determinable from the clue.
- The exact WebSocket protocol, message format, and channel naming conventions are not visible.
- How broadcast messages are routed (in-memory pub/sub, Redis, database-backed queue) cannot be determined.
