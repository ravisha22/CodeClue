# Enterprise v2: ent-saleor-rel-2
Date: 2026-04-17

## Question
How do Saleor's API deprecation rules relate GraphQL fields, webhook payloads, plugins, and changelog entries?

## Reasoning Scaffold

### Step 1: Identify Relevant Symbols (FOCUS, SYM)

The most directly relevant symbols are:
- **`deprecation_reason`** (`saleor/graphql/webhook/enums.py:255-263`) — annotated with `GUARD(enum.value == WebhookEventAsyncType.NOTIFY_USER -> return 'See the doc...')`. This is the function that attaches a deprecation reason string to a webhook event enum value (FOCUS).
- **`print_field_directives_for_webhook_events_info`** (`saleor/graphql/schema_printer.py:171-195`) — `ACCUMULATE(webhook_events_info loop -> async events event type uppe)`; called by `print_field_directives` (FOCUS).
- **`print_object_directives`** (`saleor/graphql/schema_printer.py:152-155`) — calls `print_object_directives_for_category` and `print_object_directvie_for_webhook_events_info`; called by `print_enum`, `print_input_object`, `print_interface`, `print_object` (FOCUS).
- **`print_object`** (`saleor/graphql/schema_printer.py:239-251`) — calls `print_description`, `print_fields`, `print_implemented_interfaces`, `print_object_directives`; called by `print_type` (FOCUS).
- **`monitor_fields_usage`** (`saleor/graphql/api.py:59-89`) — "Wrap resolvers of tracked fields to record usage metrics on each call." `ACCUMULATE(schema.get_type_map()... -> result)`. Calls `wrapper`. This wraps resolvers of tracked (possibly deprecated) fields to capture usage metrics (FOCUS).
- **`WebhookPlugin`** (`saleor/plugins/webhook/plugin.py:156-3518`) — extends `BasePlugin`; `PLUGIN_ID='mirumee.webhooks'`, `DEFAULT_ACTIVE=True`, `CONFIGURATION_PER_CHANNEL=False`. It orchestrates webhook dispatch for all events (FOCUS, SYM).

### Step 2: Trace GraphQL Field Deprecation (FOCUS)

The schema-printer pipeline chains through:

`print_type` → `print_object` → `print_object_directives` → `print_field_directives` → `print_field_directives_for_webhook_events_info`

- `print_object` (`saleor/graphql/schema_printer.py:239-251`) calls `print_object_directives` as part of printing any GraphQL object type (FOCUS).
- `print_object_directives` (`:152-155`) always calls both `print_object_directives_for_category` and `print_object_directvie_for_webhook_events_info` (note the typo in the latter name). This means every object type, enum, input object, and interface that passes through the printer has webhook-event directives applied (FOCUS).
- `print_field_directives_for_webhook_events_info` (`:171-195`) iterates `webhook_events_info` and outputs async event type names as uppercase directive annotations. This attaches webhook event metadata directly to GraphQL field definitions in the printed schema (FOCUS).

This shows that **deprecation and webhook-event metadata are embedded directly into the GraphQL schema SDL** via custom directives when the schema is printed.

### Step 3: Trace Webhook Event Deprecation (FOCUS)

- **`deprecation_reason`** (`saleor/graphql/webhook/enums.py:255-263`) provides the deprecation string for the `NOTIFY_USER` async event type: `GUARD(enum.value == WebhookEventAsyncType.NOTIFY_USER -> return 'See the doc...')`. The docstring fragment "See the doc..." implies it redirects consumers to migration documentation (FOCUS).
- The `WebhookPlugin` (`saleor/plugins/webhook/plugin.py:156-3518`) dispatches all webhook events including deprecated ones. Its `_get_webhooks_for_event` (`:175`) and `_get_webhooks_for_channel_events` (`:766`) select which subscribed webhooks to fire; it does not itself filter out deprecated event types — the deprecation is surfaced at the schema layer via `deprecation_reason`, not at dispatch (FOCUS, SYM).
- `trigger_webhooks_async` (`:246`) and `process_webhook_payloads` (`saleor/webhook/transport/asynchronous/transport.py:150-218`) handle the asynchronous delivery of payloads. `process_webhook_payloads` accumulates `EventPayload` and `EventDelivery` model instances (FOCUS). Deprecated events would still be delivered if subscribed — the deprecation is advisory, not blocking.
- `generate_pre_save_payloads` (`saleor/graphql/webhook/subscription_payload.py:263-309`) — `GUARD(not settings.ENABLE_LIMITING_WEBHOOKS_FOR_IDENTICAL_PAYLOADS -> return {})`. This setting-controlled guard shows that payload deduplication can be toggled, but it is not directly tied to deprecation (FOCUS).

### Step 4: Trace Plugin Lifecycle and Deprecation Relation (FOCUS, SYM)

- Plugins are loaded via `_load_plugin` (`saleor/plugins/manager.py:104`), configured from DB via `_get_db_plugin_configs` (`:201`), and run via `__run_method_on_plugins` (`:211`) / `__run_method_on_single_plugin` (`:233`) (SYM).
- Plugin field validation runs at startup via `check_plugin_fields` (`saleor/plugins/apps.py:30-35`) — `ACCUMULATE(fields loop -> result, raises ImproperlyConfigured)`. This is a structural check, not a deprecation check (FOCUS).
- The plugin URL surface is registered in `saleor/urls.py` via three Django routes: `^plugins/(?P<plugin_id>...)` → `handle_plugin_webhook`, `^plugins/channel/(?P<...>...)` → `handle_plugin_per_channel_webhook`, `^plugins/global/(?P<...>...)` → `handle_global_plugin_webhook` (FOCUS). These are stable entry points; the clue does not show any deprecation annotation on these routes.
- `hide_private_configuration_fields` (`saleor/graphql/plugins/resolvers.py:15-37`) filters plugin configuration before surfacing it in the GraphQL API: `GUARD(not config_structure -> return); ACCUMULATE(configuration loop -> result)` (FOCUS). This is a visibility/privacy concern, not deprecation.
- `_wrap_with_sync_webhook_control_context` (`saleor/graphql/order/types.py:265-268` and `:837-840`) wraps order line resolvers with `SyncWebhookControlContext`, indicating that synchronous webhook calls during GraphQL resolution are context-managed (FOCUS).

### Step 5: Changelog and Usage Monitoring (FOCUS)

- `monitor_fields_usage` (`saleor/graphql/api.py:59-89`) wraps resolvers of **tracked fields** with a counter. It iterates `schema.get_type_map()` to find fields to monitor. The docstring "record usage metrics on each call" suggests this is used to observe live usage of fields that may be deprecated or subject to removal — informing changelog/deprecation decisions. However, the clue does not show a direct link from this function to a changelog data structure (FOCUS).
- No changelog module, file, or symbol is directly visible in the TREE, INDEX, or FOCUS sections. The clue does not reveal a changelog file or automated changelog entry mechanism.
- The README sections listed are: "Table of Contents, What makes Saleor special?, Why API-only Architecture?, What are the tradeoffs?, Features" — none mention a changelog format (README).

### Gaps / Uncertainty

Per GAPS (type: STRUCTURAL, coverage: 82 symbols in L3, 39 with behavior annotations):
- `update_fields`, `PluginsQueries`, `WebhookQueries`, `subscribe_webhook` are explicitly uncovered.
- The `subscribe_webhook` symbol being uncovered means the subscription-based webhook payload generation path (how new-style subscriptions replace deprecated notification-based ones) cannot be fully traced.
- `WebhookQueries` being uncovered means the GraphQL query surface for managing webhooks and their deprecation status is unknown.
- No changelog file or changelog-generation tooling is visible in the clue. The relationship between deprecation and changelog entries **cannot be determined** from the clue alone.
- The full content of the `deprecation_reason` return string ("See the doc...") is truncated; the exact documentation reference is unknown.

## Synthesized Answer

**GraphQL field deprecation:** Saleor integrates deprecation metadata directly into the GraphQL schema SDL through a custom schema printer (`saleor/graphql/schema_printer.py`). The chain `print_type → print_object → print_object_directives → print_field_directives → print_field_directives_for_webhook_events_info` annotates every object type and field with webhook-event directives. The `deprecation_reason` function (`saleor/graphql/webhook/enums.py`) attaches a deprecation string (redirecting to documentation) to the `NOTIFY_USER` async webhook event enum value specifically.

**Webhook payloads:** Deprecated events are not blocked at the dispatch layer — `WebhookPlugin` still fires them for subscribed consumers. The `process_webhook_payloads` pipeline delivers `EventPayload`/`EventDelivery` objects regardless of deprecation status. Deprecation is advisory, surfaced at the schema/enum level.

**Plugins:** Plugin configuration is validated structurally at startup (`check_plugin_fields`) and their webhook entry points are stable URL routes in `saleor/urls.py`. No deprecation annotations are visible on plugin routes or plugin manager methods in the clue.

**Usage monitoring:** `monitor_fields_usage` wraps resolvers of tracked GraphQL fields to record call-site metrics, which likely informs decisions about when deprecated fields can be safely removed, but this connection is inferential only.

**Changelog entries:** No changelog module or changelog-generation mechanism is visible in the clue. The relationship between API deprecation rules and changelog entries **cannot be determined** from the available evidence.
