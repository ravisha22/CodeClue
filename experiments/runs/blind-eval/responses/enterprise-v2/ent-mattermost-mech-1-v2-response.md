# Enterprise v2: ent-mattermost-mech-1
Date: 2026-04-17

## Reasoning Scaffold

### 1. Relevant Clue Entries and Source Snippets

The question asks how incoming webhook administration works across team, channel, and system scopes.

**FOCUS – App.CreateIncomingWebhookForChannel** (server/channels/app/webhook.go:390):
- Behavior: `GUARD(!*a.Config().ServiceSettings.EnableIncomingWe... -> return nil, model....); PRECEDENCE(not_a.Config)`
- Calls: `Srv`, `Config`
- Called by: `createIncomingHook`, `localCreateIncomingHook`

**FOCUS – SqlWebhookStore.GetIncomingByTeam** (server/channels/store/sqlstore/webhook_store.go:205):
- Behavior: `DELEGATE(s.GetIncomingByTeamByUser -> result)`
- Calls: `GetIncomingByTeamByUser`

**FOCUS – SqlWebhookStore.GetIncomingByTeamByUser** (webhook_store.go:183):
- Behavior: `PRECEDENCE(userId -> err)`
- Calls: `GetReplica`
- Called by: `GetIncomingByTeam`

**FOCUS – SqlWebhookStore.GetIncomingByChannel** (webhook_store.go:209):
- Behavior: `GUARD(err := s.GetReplica().SelectBuilder(&webhooks... -> return nil, errors...)`
- Calls: `GetReplica`

**FOCUS – SqlWebhookStore.PermanentDeleteIncomingByChannel** (webhook_store.go:151):
- Behavior: `GUARD(err != nil -> return errors.Wrapf...)`
- Calls: `GetMaster`

**FOCUS – LocalCacheWebhookStore.PermanentDeleteIncomingByChannel** (server/channels/store/localcachelayer/webhook_layer.go:81):
- Behavior: `GUARD(err != nil -> return err)`
- Calls: `ClearCaches`

**FOCUS – RetryLayerWebhookStore** variants:
- `GetIncomingByChannel` (retrylayer.go:17727): calls `isRepeatableError`
- `GetIncomingByTeam` (retrylayer.go:17748): calls `isRepeatableError`
- `GetIncomingByTeamByUser` (retrylayer.go:17769): calls `isRepeatableError`, called by `GetIncomingByTeam`
- `PermanentDeleteIncomingByChannel` (retrylayer.go:17985): calls `isRepeatableError`

**FOCUS – TimerLayerWebhookStore** variants:
- `GetIncomingByChannel` (timerlayer.go:14021)
- `GetIncomingByTeam` (timerlayer.go:14037)
- `GetIncomingByTeamByUser` (timerlayer.go:14053): called by `GetIncomingByTeam`
- `PermanentDeleteIncomingByChannel` (timerlayer.go:14228)

**FOCUS – Client4.CreateIncomingWebhook** (server/public/model/client4.go:4540):
- "creates an incoming webhook for a channel."
- Calls: `BuildResponse`, `doAPIPostJSON`, `incomingWebhooksRoute`, `closeBody`
- Called by: `createIncomingWebhookCmdF`

**FOCUS – Client4.UpdateIncomingWebhook** (client4.go:4550):
- "updates an incoming webhook for a channel."
- Calls: `BuildResponse`, `doAPIPutJSON`, `incomingWebhookRoute`, `closeBody`
- Called by: `updateIncomingHook`, `modifyIncomingWebhookCmdF`

**FOCUS – Client4.CreateOutgoingWebhook** (client4.go:4621):
- "creates an outgoing webhook for a team or channel."
- Calls: `BuildResponse`, `doAPIPostJSON`, `outgoingWebhooksRoute`, `closeBody`
- Called by: `createOutgoingHook`, `localCreateOutgoingHook`, `createOutgoingWebhookCmdF`

**FOCUS – SqlPropertyFieldStore.checkTeamLevelConflict** (server/channels/store/sqlstore/property_field_store.go:407):
- "checks if a team-level property would conflict with system properties or channel properties withi…"

**Source Snippets (File 2):**

| Function | Signature | File:Line |
|---|---|---|
| `SqlWebhookStore.GetIncomingByTeam` | `(teamId string, offset, limit int) ([]*model.IncomingWebhook, error)` | webhook_store.go:205 |
| `SqlWebhookStore.GetIncomingByTeamByUser` | `(teamId string, userId string, offset, limit int) ([]*model.IncomingWebhook, error)` | webhook_store.go:183 |
| `SqlWebhookStore.GetIncomingByChannel` | `(channelId string) ([]*model.IncomingWebhook, error)` | webhook_store.go:209 |
| `SqlWebhookStore.GetIncomingList` | `(offset, limit int) ([]*model.IncomingWebhook, error)` | webhook_store.go:160 |
| `SqlWebhookStore.GetIncomingListByUser` | `(userId string, offset, limit int) ([]*model.IncomingWebhook, error)` | webhook_store.go:164 |
| `SqlWebhookStore.SaveIncoming` | `(webhook *model.IncomingWebhook) (*model.IncomingWebhook, error)` | webhook_store.go:80 |
| `SqlWebhookStore.UpdateIncoming` | `(hook *model.IncomingWebhook) (*model.IncomingWebhook, error)` | webhook_store.go:100 |
| `SqlWebhookStore.DeleteIncoming` | `(webhookId string, time int64) error` | webhook_store.go:133 |
| `SqlWebhookStore.GetIncoming` | `(id string, allowFromCache bool) (*model.IncomingWebhook, error)` | webhook_store.go:114 |
| `SqlWebhookStore.PermanentDeleteIncomingByChannel` | `(channelId string) error` | webhook_store.go:151 |
| `SqlWebhookStore.PermanentDeleteIncomingByUser` | `(userId string) error` | webhook_store.go:142 |
| `SqlWebhookStore.InvalidateWebhookCache` | `(webhookId string)` | webhook_store.go:77 |
| `SqlWebhookStore.ClearCaches` | `()` | webhook_store.go:25 |
| `SqlWebhookStore.AnalyticsIncomingCount` | `(teamID string, userID string) (int64, error)` | webhook_store.go:390 |
| `SqlWebhookStore.GetOutgoingByTeam` | `(teamId string, offset, limit int) ([]*model.OutgoingWebhook, error)` | webhook_store.go:342 |
| `SqlWebhookStore.GetOutgoingByTeamByUser` | `(teamId string, userId string, offset, limit int) ([]*model.OutgoingWebhook, error)` | webhook_store.go:319 |
| `SqlWebhookStore.GetOutgoingByChannel` | `(channelId string, offset, limit int) ([]*model.OutgoingWebhook, error)` | webhook_store.go:315 |
| `SqlWebhookStore.GetOutgoingByChannelByUser` | `(channelId string, userId string, offset, limit int) ([]*model.OutgoingWebhook, error)` | webhook_store.go:292 |
| `SqlWebhookStore.GetOutgoingList` | `(offset, limit int) ([]*model.OutgoingWebhook, error)` | webhook_store.go:288 |
| `SqlWebhookStore.GetOutgoingListByUser` | `(userId string, offset, limit int) ([]*model.OutgoingWebhook, error)` | webhook_store.go:267 |
| `newSqlWebhookStore` | `(sqlStore *SqlStore, metrics einterfaces.MetricsInterface) store.WebhookStore` | webhook_store.go:28 |

### 2. Tracing the Mechanism

**A. Configuration Gate (System Scope)**

`App.CreateIncomingWebhookForChannel` (webhook.go:390) uses a GUARD behavior: `GUARD(!*a.Config().ServiceSettings.EnableIncomingWe... -> return nil, model....)`. This means incoming webhook creation is **globally gated by a system-level configuration setting** (`ServiceSettings.EnableIncomingWebhooks`). If disabled, the function returns an error model immediately, preventing creation regardless of team or channel context.

**B. Three Query Scopes for Incoming Webhooks**

The source snippets and clue reveal three distinct administrative scopes for listing incoming webhooks:

1. **System scope** (no team/channel filter):
   - `GetIncomingList(offset, limit int)` (webhook_store.go:160) — returns all incoming webhooks across the entire system, paginated.
   - `GetIncomingListByUser(userId string, offset, limit int)` (webhook_store.go:164) — returns all incoming webhooks created by a specific user, system-wide.

2. **Team scope**:
   - `GetIncomingByTeam(teamId string, offset, limit int)` (webhook_store.go:205) — delegates to `GetIncomingByTeamByUser` (FOCUS behavior annotation). The clue's behavior annotation `DELEGATE(s.GetIncomingByTeamByUser -> result)` shows that the team-scoped query is implemented by calling the team+user variant.
   - `GetIncomingByTeamByUser(teamId string, userId string, offset, limit int)` (webhook_store.go:183) — behavior `PRECEDENCE(userId -> err)` indicates that when a `userId` is provided, it takes precedence in the query filtering; when absent (via delegation from `GetIncomingByTeam`), the filter is team-only.

3. **Channel scope**:
   - `GetIncomingByChannel(channelId string)` (webhook_store.go:209) — returns all incoming webhooks for a single channel, no pagination (returns full list). Uses `GetReplica` for read queries.

**C. Delegation Pattern: Team → Team+User**

A critical mechanistic detail: `GetIncomingByTeam` does NOT query directly. It **delegates** to `GetIncomingByTeamByUser` (FOCUS: `DELEGATE(s.GetIncomingByTeamByUser -> result)`). The source snippet confirms the delegation target accepts both `teamId` and `userId`. The `PRECEDENCE(userId -> err)` behavior on `GetIncomingByTeamByUser` indicates that when called by `GetIncomingByTeam`, the userId parameter controls whether user-level filtering is applied — allowing the same function to serve both "all team webhooks" and "team webhooks for a specific user" queries.

This same pattern exists for outgoing webhooks: `GetOutgoingByTeam` and `GetOutgoingByTeamByUser` (webhook_store.go:342, 319).

**D. CRUD Operations (Channel-Scoped Creation)**

- **Create**: `Client4.CreateIncomingWebhook` (client4.go:4540) — "creates an incoming webhook for a channel" — routes through `doAPIPostJSON` to `incomingWebhooksRoute`. The server-side handler `App.CreateIncomingWebhookForChannel` (webhook.go:390) receives the request, applies the config guard, and persists via `SqlWebhookStore.SaveIncoming` (webhook_store.go:80).
- **Update**: `Client4.UpdateIncomingWebhook` (client4.go:4550) — "updates an incoming webhook for a channel" — uses `doAPIPutJSON` to `incomingWebhookRoute`. Server persists via `SqlWebhookStore.UpdateIncoming` (webhook_store.go:100).
- **Delete**: `SqlWebhookStore.DeleteIncoming(webhookId string, time int64)` (webhook_store.go:133) — soft-deletes by webhook ID and timestamp.
- **Single Get**: `SqlWebhookStore.GetIncoming(id string, allowFromCache bool)` (webhook_store.go:114) — retrieves by ID with optional cache usage.

**E. Permanent Deletion (Channel and User Scopes)**

- `PermanentDeleteIncomingByChannel(channelId string)` (webhook_store.go:151) — uses `GetMaster` for write operations (FOCUS). The `LocalCacheWebhookStore` variant (webhook_layer.go:81) calls `ClearCaches` after deletion, ensuring cache consistency.
- `PermanentDeleteIncomingByUser(userId string)` (webhook_store.go:142) — deletes all incoming webhooks by user.
- Corresponding outgoing variants: `PermanentDeleteOutgoingByChannel` (webhook_store.go:364), `PermanentDeleteOutgoingByUser` (webhook_store.go:355).

**F. Layered Store Architecture**

The webhook store is wrapped in three decorator layers, all visible in the clue:
1. **SqlWebhookStore** (webhook_store.go:17) — core SQL implementation, created by `newSqlWebhookStore(sqlStore, metrics)` (webhook_store.go:28).
2. **RetryLayerWebhookStore** (retrylayer.go) — wraps each operation with `isRepeatableError` retry logic for transient DB failures.
3. **TimerLayerWebhookStore** (timerlayer.go) — adds timing/metrics instrumentation.
4. **LocalCacheWebhookStore** (webhook_layer.go) — adds local caching with `ClearCaches` for invalidation.

**G. Analytics (Team+User Scope)**

`SqlWebhookStore.AnalyticsIncomingCount(teamID string, userID string)` (webhook_store.go:390) and `AnalyticsOutgoingCount(teamId string)` (webhook_store.go:412) provide aggregate counts scoped by team (and optionally user for incoming), supporting admin dashboard analytics.

**H. Outgoing Webhook Comparison**

Outgoing webhooks mirror the incoming pattern with one notable difference visible in the Client4 API: `Client4.CreateOutgoingWebhook` (client4.go:4621) is described as creating "an outgoing webhook for a team or channel" — whereas `Client4.CreateIncomingWebhook` (client4.go:4540) creates one "for a channel". This suggests outgoing webhooks have a broader creation scope (team OR channel) compared to incoming webhooks (channel only).

### 3. GAPS — What Cannot Be Determined

The GAPS section states:
- **Type**: MECHANISTIC (body logic needed for full answer)
- **Coverage**: 83 symbols in L3, 36 with behavior annotations
- **Uncovered**: `ChannelStore.GetChannelsWithTeamDataByIds`, `ChannelStore.GetPublicChannelsByIdsForTeam`, `ChannelStore.GetTeamForChannel`, `ChannelStore.GetTeamMembersForChannel`
- **Drill**: `server/channels/store/sqlstore/webhook_store.go (~1 lines, SqlWebhookStore.GetIncomingByTeam)` — only the function signature was drilled, not the full body

From the clue and snippets alone, we **cannot determine**:
- The full SQL query logic inside `GetIncomingByTeamByUser` — specifically how it conditionally filters by userId (the `PRECEDENCE(userId -> err)` annotation is compact; the actual SQL WHERE clause is not shown)
- The permission checks in the API handler layer (`createIncomingHook`, `localCreateIncomingHook`) — only the App-layer config guard is visible
- Whether team-level or system-level admin permissions are required to list all webhooks vs. user-scoped webhooks
- The cache TTL and eviction strategy in `LocalCacheWebhookStore`
- How `GetIncomingByTeam` passes an empty or zero userId to delegate to `GetIncomingByTeamByUser` for the "all team" query

### 4. Synthesis

Incoming webhook administration in Mattermost operates across **three hierarchical scopes**, with a system-level configuration gate and a layered store architecture:

**System Scope**: A global config guard (`ServiceSettings.EnableIncomingWebhooks`) in `App.CreateIncomingWebhookForChannel` (webhook.go:390) enables or disables incoming webhooks platform-wide. System-wide listing is provided by `GetIncomingList` (webhook_store.go:160) and `GetIncomingListByUser` (webhook_store.go:164). Analytics via `AnalyticsIncomingCount` (webhook_store.go:390) accepts team+user filters.

**Team Scope**: `GetIncomingByTeam` (webhook_store.go:205) delegates to `GetIncomingByTeamByUser` (webhook_store.go:183), which applies `PRECEDENCE(userId -> err)` to conditionally filter by user within a team. This delegation allows a single implementation to serve both team-admin (all team webhooks) and user-self-service (my webhooks in team) queries.

**Channel Scope**: Creation is channel-scoped — `Client4.CreateIncomingWebhook` (client4.go:4540) creates "for a channel," and `App.CreateIncomingWebhookForChannel` (webhook.go:390) is the server handler. `GetIncomingByChannel` (webhook_store.go:209) retrieves all webhooks for a channel. `PermanentDeleteIncomingByChannel` (webhook_store.go:151) removes all incoming webhooks for a channel, with cache invalidation via `ClearCaches` in the local cache layer (webhook_layer.go:81).

The store is decorated with **retry** (retrylayer, using `isRepeatableError`), **timer** (timerlayer, metrics), and **local cache** layers. Write operations use `GetMaster`; reads use `GetReplica` — confirming master/replica routing.

**Unresolved**: The exact permission checks at the API handler level, the conditional SQL filtering logic in `GetIncomingByTeamByUser`, and cache configuration details remain outside the clue's coverage.
