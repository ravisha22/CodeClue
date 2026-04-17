# Enterprise Eval: ent-saleor-rel-2
Date: 2026-04-17

## Question
How do Saleor's API deprecation rules relate GraphQL fields, webhook payloads, plugins, and changelog entries?

---

## Reasoning Trace

### Step 1: Identify Deprecation-Related Symbols

From FOCUS, two symbols directly address deprecation:

1. **`deprecation_reason`** (saleor/graphql/webhook/enums.py:255-263) — behavior: `GUARD(enum.value == WebhookEventAsyncType.NOTIFY_USER -> return 'See the doc...')`. This function returns a deprecation reason string for specific webhook event enum values, specifically guarding that if the enum value equals `WebhookEventAsyncType.NOTIFY_USER`, it returns a message starting with "See the doc..." (FOCUS).

2. **`print_field_directives_for_webhook_events_info`** (saleor/graphql/schema_printer.py:171-195) — behavior: `ACCUMULATE(webhook_events_info loop -> async events event type upper)`. Called by `print_field_directives`. This function iterates over webhook event info annotations and prints them as field directives in the schema, including event type information (FOCUS).

### Step 2: Schema Printing and Directive Emission

The schema printer module (`saleor/graphql/schema_printer.py`) contains several related functions:

- **`print_object`** (saleor/graphql/schema_printer.py:239-251) — calls `print_description`, `print_fields`, `print_implemented_interfaces`, `print_object_directives`. Called by `print_type` (FOCUS from mech-2 clue).
- **`print_input_object`** (saleor/graphql/schema_printer.py:284-294) — calls `print_block`, `print_description`, `print_input_value`, `print_object_directives`. Called by `print_type` (FOCUS from mech-2 clue).
- **`print_object_directives`** (saleor/graphql/schema_printer.py:152-155) — calls `print_object_directives_for_category` and `print_object_directvie_for_webhook_events_info` (FOCUS from mech-2 clue).

This chain shows that when the GraphQL schema is printed/exported, webhook event info is emitted as directives on fields and types. The `print_field_directives_for_webhook_events_info` function specifically outputs webhook event metadata (including async event types) as schema directives.

### Step 3: Webhook and Plugin Relationship

**WebhookPlugin** (saleor/plugins/webhook/plugin.py:156-3518) is the central integration between the plugin system and webhooks:
- Extends `BasePlugin` with attrs `PLUGIN_ID='mirumee.webhooks'`, `PLUGIN_NAME='Webhooks'`, `DEFAULT_ACTIVE=True`, `CONFIGURATION_PER_CHANNEL=False` (FOCUS).
- Calls `_get_webhooks_for_event` (line 175) and `_get_webhooks_for_channel_events` (line 766) to find registered webhooks per event (FOCUS).
- `trigger_webhooks_async` (line 246) dispatches webhook events asynchronously (SYM/FOCUS).
- `__run_payment_webhook` (line 2994-3072) triggers payment-specific webhook events, accumulating over apps and raising `PaymentError` (FOCUS).
- `_serialize_payload` (line 181), `_generate_meta` (line 184), and `_trigger_metadata_updated_event` (line 187) handle payload construction (SYM/FOCUS).

**Plugin configuration checking:**
- `check_plugin_fields` (saleor/plugins/apps.py:30-35) — accumulates over fields and raises `ImproperlyConfigured` if plugin class fields are invalid. Called by `load_and_check_plugin` (FOCUS). This validation ensures plugins declare required fields correctly.

**Plugin webhook views:**
- `handle_plugin_webhook` (saleor/plugins/views.py:9-11), `handle_global_plugin_webhook` (line 15-19), and `handle_plugin_per_channel_webhook` (line 23-27) provide HTTP endpoints for plugin webhook callbacks (FOCUS).

### Step 4: Webhook Payload Construction

- **`process_webhook_payloads`** (saleor/webhook/transport/asynchronous/transport.py:150-218) — accumulates subscribable objects into event payloads, using `EventPayload` and `EventDelivery` models (FOCUS).
- **`generate_pre_save_payloads`** (saleor/graphql/webhook/subscription_payload.py:263-309) — guards on `settings.ENABLE_LIMITING_WEBHOOKS_FOR_IDENTICAL_PAYLOADS`, then accumulates payloads per webhook. Calls `generate_payload_from_subscription`, `get_pre_save_payload_key`, `initialize_request` (FOCUS).
- **`generate_api_call_payload`** (saleor/webhook/observability/payloads.py:153-190) — serializes API call data for observability, using `ApiCallPayload`, `ApiCallRequest` typed dicts. Raises `ApiCallTruncationError` (FOCUS).

### Step 5: Observability Payload Schema

- `ApiCallPayload` (saleor/webhook/observability/payload_schema.py:110-114) extends `ObservabilityEventBase` (FOCUS).
- `ApiCallRequest` (line 95-101) and `ApiCallResponse` (line 104-107) extend `TypedDict` (FOCUS).

### Step 6: Field Usage Monitoring

- **`monitor_fields_usage`** (saleor/graphql/api.py:59-89) — "Wrap resolvers of tracked fields to record usage metrics on each call." Accumulates over `schema.get_type_map()` and calls `wrapper` to instrument resolvers (FOCUS). This provides runtime monitoring of which GraphQL fields are actually being used — relevant to deprecation decisions.

### Step 7: SyncWebhookControlContext Wrapping

Multiple types wrap objects in `SyncWebhookControlContext`:
- `_wrap_with_sync_webhook_control_context` appears in `saleor/graphql/order/types.py:265`, `:837`, `saleor/graphql/webhook/subscription_types.py:1327`, `saleor/graphql/invoice/types.py:38`, `saleor/graphql/account/types.py:276`. All delegate to `SyncWebhookControlContext` from `graphql.core.context` or `core.context` (FOCUS). This indicates sync webhooks can observe/control resolution of order, invoice, and account types.

### Step 8: Plugin Configuration Visibility

- **`hide_private_configuration_fields`** (saleor/graphql/plugins/resolvers.py:15-37) — guards on `not config_structure`, then accumulates over configuration to hide private fields. Called by `aggregate_plugins_configuration` (FOCUS). This controls what plugin configuration is exposed through the API.

### Step 9: GAPS — What Cannot Be Determined

Per the GAPS section:
- **Type:** STRUCTURAL (answerable from L0-L2)
- **Coverage:** 80 symbols in L3, 39 with behavior annotations
- **Uncovered symbols:** `clean_base_fields`, `call_gift_card_created_on_plugins`, `webhook`, `ApiCallTruncationError`

From the clue alone, the following **cannot** be determined:
- Whether there is a formal deprecation policy document or changelog generation system — no changelog-related symbols appear in the clue
- The full deprecation reason text for `NOTIFY_USER` (truncated to "See the doc...")
- How deprecated fields are annotated in the GraphQL schema beyond the webhook event directives (e.g., whether standard GraphQL `@deprecated` directives are used on individual fields)
- Whether there is a versioning strategy or migration path for deprecated API fields
- The relationship between `monitor_fields_usage` data and deprecation decisions — usage monitoring exists but no automated deprecation workflow is shown
- The `webhook` symbol listed in GAPS suggests there may be additional webhook-related functionality not covered

---

## Synthesized Answer

Based solely on the clue file, Saleor's deprecation and API evolution rules connect GraphQL fields, webhook payloads, plugins, and changelog entries as follows:

1. **GraphQL Deprecation via Webhook Enums:** The `deprecation_reason` function (saleor/graphql/webhook/enums.py:255-263) attaches deprecation reasons to specific webhook event enum values. When `WebhookEventAsyncType.NOTIFY_USER` is encountered, it returns a deprecation message ("See the doc..."). This links deprecation metadata directly to webhook event types exposed through the GraphQL schema.

2. **Schema Directives for Webhook Events:** `print_field_directives_for_webhook_events_info` (saleor/graphql/schema_printer.py:171-195) emits webhook event information as field directives during schema printing. Combined with `print_object_directives` (line 152), this means the printed/exported GraphQL schema contains embedded metadata about which webhook events each field or type can trigger — making deprecation of events visible in the schema itself.

3. **Field Usage Monitoring:** `monitor_fields_usage` (saleor/graphql/api.py:59-89) wraps field resolvers to track runtime usage metrics. While no direct link to automated deprecation is shown, this monitoring infrastructure could inform deprecation decisions by identifying unused or low-usage fields.

4. **Plugin System as Extension Surface:** The `WebhookPlugin` (saleor/plugins/webhook/plugin.py:156-3518) bridges the plugin and webhook systems. Plugin configuration is validated via `check_plugin_fields` (saleor/plugins/apps.py:30-35) and selectively exposed via `hide_private_configuration_fields` (saleor/graphql/plugins/resolvers.py:15-37). Plugin webhook endpoints are served through `handle_plugin_webhook`, `handle_global_plugin_webhook`, and `handle_plugin_per_channel_webhook` (saleor/plugins/views.py).

5. **Webhook Payload Pipeline:** Webhook payloads flow through `process_webhook_payloads` (webhook/transport/asynchronous/transport.py:150-218) and `generate_pre_save_payloads` (graphql/webhook/subscription_payload.py:263-309). Observability payloads use typed schemas (`ApiCallPayload`, `ApiCallRequest`, `ApiCallResponse`) ensuring structured payload formats.

6. **Changelog Entries: NOT determinable.** The clue contains **no symbols, modules, or references** related to changelog generation, release notes, or versioning documents. Whether Saleor has automated changelog generation tied to deprecation annotations cannot be established from the provided evidence.
