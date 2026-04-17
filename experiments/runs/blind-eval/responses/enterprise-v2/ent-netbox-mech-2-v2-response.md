# Enterprise v2: ent-netbox-mech-2
Date: 2026-04-17

## Question
What is the processing chain for event rules and outgoing webhooks?

## Reasoning Scaffold

### Step 1: Identify the core event-rule symbols from FOCUS and SYM

**Model layer:**

| Symbol | Location | Description |
|---|---|---|
| `EventRulesMixin` | `netbox/netbox/models/features.py:503-508` | "Enables support for event rules, which can be used to transmit webhooks or execute scripts automatically"; extends `Model` |
| `EventRule` | `netbox/extras/models/models.py:54-162` | "An EventRule defines an action to be taken automatically in response to a specific set of events"; extends `CustomFieldsMixin, ExportTemplatesMixin, OwnerMixin`; raises `ValidationError` |
| `EventRuleActionChoices` | `netbox/extras/choices.py:242-252` | attrs: `WEBHOOK='webhook'`, `SCRIPT='script'`, `NOTIFICATION='notification'` — the three action types |

**Event processing pipeline:**

| Symbol | Location | Description / Behavior |
|---|---|---|
| `serialize_for_event` | `netbox/extras/events.py:79` (SYM) | "Return a serialized representation of the given…" — prepares the object data payload |
| `process_event_rules` | `netbox/extras/events.py:162-257` | "Process a list of EventRules against an event"; ACCUMULATE(event_rules loop → result); raises `ValueError`; called_by `process_event_queue` |
| `process_event_queue` | `netbox/extras/events.py:258-285` | "Flush a list of object representation to RQ for EventRule processing"; ACCUMULATE(events loop → result); calls `process_event_rules` |
| `flush_events` | `netbox/extras/events.py:286-297` | "Flush a list of object representations to RQ for event processing" |

**Signal handlers:**

| Symbol | Location | Description |
|---|---|---|
| `process_job_start_event_rules` | `netbox/extras/signals.py:98-112` | "Process event rules for jobs starting"; uses `EventContext` from `extras.events` |
| `process_job_end_event_rules` | `netbox/extras/signals.py:116-130` | "Process event rules for jobs terminating"; uses `EventContext` from `extras.events` |

**Full CRUD / UI / API stack for EventRule:**

| Symbol | Location |
|---|---|
| `EventRuleListView` | `netbox/extras/views.py:801-805` |
| `EventRuleEditView` | `netbox/extras/views.py:828-830` |
| `EventRuleDeleteView` | `netbox/extras/views.py:834-835` |
| `EventRuleBulkImportView` | `netbox/extras/views.py:839-841` |
| `EventRuleBulkEditView` | `netbox/extras/views.py:845-849` |
| `EventRuleBulkRenameView` | `netbox/extras/views.py:853-855` |
| `EventRuleBulkDeleteView` | `netbox/extras/views.py:859-862` |
| `EventRuleSerializer` | `netbox/extras/api/serializers_/events.py:19-37` |
| `EventRuleFilterSet` | `netbox/extras/filtersets.py:99-137` |
| `EventRuleFilterForm` | `netbox/extras/forms/filtersets.py:325-354` |
| `EventRuleForm` | `netbox/extras/forms/model_forms.py:464-577` |
| `EventRuleImportForm` | `netbox/extras/forms/bulk_import.py:229-275` |
| `EventRuleTable` | `netbox/extras/tables/tables.py:505-546` |
| `EventRuleFilter` (GraphQL) | `netbox/extras/graphql/filters.py:336-355` |
| `EventRulePanel` / `EventRuleActionPanel` / `EventRuleEventTypesPanel` | `netbox/extras/ui/panels.py` |
| `path:event-rules/` | `netbox/extras/urls.py` |
| `path:event-rules/<int:pk>` | `netbox/extras/urls.py` |

**Migration helpers:**

| Symbol | Location | Description |
|---|---|---|
| `update_event_rules` | `netbox/extras/migrations/0109_script_model.py:122-146` | "Update any existing EventRules for scripts"; ACCUMULATE over `EventRule.objects` |
| `set_event_types` | `netbox/extras/migrations/0120_eventrule_event_types.py:7-26` | ACCUMULATE(event_rules loop → event rule event types OBJECT) — migration to populate event type fields |

### Step 2: Trace the event model

**Model opt-in**: Any NetBox model that extends `EventRulesMixin` (FOCUS: `netbox/netbox/models/features.py:503-508`) gains support for event rules. This is a mixin — individual domain models opt in, enabling event processing for creates, updates, and deletes on those models.

**Rule definition**: Each `EventRule` (FOCUS: `netbox/extras/models/models.py:54-162`) specifies:
- The object type(s) it watches.
- The event types that trigger it (populated via migration `set_event_types`).
- The action to take: one of `WEBHOOK`, `SCRIPT`, or `NOTIFICATION` (`EventRuleActionChoices`, FOCUS: `netbox/extras/choices.py`).
- Rules can raise `ValidationError`, suggesting they are validated before persisting.

`EventRuleForm` (FOCUS: `netbox/extras/forms/model_forms.py:464-577`) calls `init_notificationgroup_choice`, `init_script_choice`, and `init_webhook_choice` — confirming that each of the three action types has a distinct target object that must be selected when creating a rule.

### Step 3: Trace the processing chain

The chain can be reconstructed from `extras/events.py` symbols:

```
[Object change / job signal]
        │
        ├─ process_job_start_event_rules (extras/signals.py:98-112)   [on job start]
        └─ process_job_end_event_rules   (extras/signals.py:116-130)  [on job end]
                │
                └─ EventContext (extras.events) — packages context for downstream
                        │
        [Object change event for regular model changes]
                │
                ▼
        serialize_for_event (extras/events.py:79)
        — serializes the affected object to a portable representation
                │
                ▼
        flush_events (extras/events.py:286-297)
        — "Flush a list of object representations to RQ for event processing"
                │
                ▼ (dispatched via RQ)
        process_event_queue (extras/events.py:258-285)
        — ACCUMULATE(events loop → result)
        — calls process_event_rules per batch
                │
                ▼
        process_event_rules (extras/events.py:162-257)
        — ACCUMULATE(event_rules loop → result)
        — iterates matching EventRules, raises ValueError on bad config
        — dispatches action based on rule.action_type:
                ├─ WEBHOOK → [send_webhook — GAPS: uncovered]
                ├─ SCRIPT  → run_script (extras/jobs.py:30)
                └─ NOTIFICATION → [notification mechanism — partially uncovered]
```

**Key call chain** confirmed by clue:
- `process_event_queue` (FOCUS) **calls** `process_event_rules` (FOCUS: `called_by: process_event_queue`).
- `process_event_queue` is described as flushing to **RQ** ("Flush a list of object representation to **RQ** for EventRule processing"), confirming async delivery.
- `flush_events` is a related flushing function ("Flush a list of object representations to RQ for event processing") — possibly the initiating step before `process_event_queue`.

### Step 4: Webhook-specific dispatch

`EventRuleActionChoices.WEBHOOK = 'webhook'` (FOCUS: `netbox/extras/choices.py`) confirms webhooks are one of the three action types. `EventRuleForm.init_webhook_choice` (FOCUS: `netbox/extras/forms/model_forms.py`) confirms a specific webhook target object must be configured per rule.

However, `(GAPS)` explicitly lists `send_webhook` and `register_webhook_callback` as **uncovered**. This means the actual HTTP dispatch logic for webhooks — how the HTTP request is constructed, what HTTP client is used, retry handling, and TLS configuration — cannot be determined from the clue alone.

### Gaps / Uncertainty

`(GAPS)` classifies this as **STRUCTURAL**. Explicitly uncovered: `register_webhook_callback`, `send_webhook`, `Command`, `VLANTranslationRule`. Therefore:
- The exact mechanism by which a webhook HTTP request is assembled and sent cannot be determined.
- Whether `flush_events` is the first step in the chain (before `process_event_queue`) or an alternative path is not fully certain; both flush to RQ but their precise relationship is not annotated.
- The `NOTIFICATION` action target's delivery mechanism is not described in the clue.
- The `EventContext` object's full structure (used by signal handlers) is not described.

## Synthesized Answer

**Processing chain** (as far as the clue permits):

1. **Opt-in**: Models that extend `EventRulesMixin` (FOCUS: `netbox/netbox/models/features.py:503-508`) are eligible for event rule processing.

2. **Rule definition**: `EventRule` objects (FOCUS: `netbox/extras/models/models.py:54-162`) specify watched object types, event types, and a target action — one of `WEBHOOK`, `SCRIPT`, or `NOTIFICATION` (`EventRuleActionChoices`, FOCUS: `netbox/extras/choices.py:242-252`). Each action type requires a distinct target configured via `EventRuleForm` (`init_webhook_choice`, `init_script_choice`, `init_notificationgroup_choice`).

3. **Serialization**: When an event occurs, `serialize_for_event` (SYM: `netbox/extras/events.py:79`) converts the affected object to a portable representation.

4. **Queue flush**: `flush_events` (FOCUS: `netbox/extras/events.py:286-297`) and/or `process_event_queue` (FOCUS: `netbox/extras/events.py:258-285`) submit the serialized events to **RQ** for asynchronous processing.

5. **Rule matching and dispatch**: `process_event_rules` (FOCUS: `netbox/extras/events.py:162-257`) iterates each matching `EventRule` against the event, raises `ValueError` on configuration errors, and dispatches:
   - `SCRIPT` → `run_script` (SYM: `netbox/extras/jobs.py:30`) — core RQ task.
   - `WEBHOOK` → `send_webhook` — **cannot be determined from clue** `(GAPS)`.
   - `NOTIFICATION` → notification group — mechanism not detailed in clue.

6. **Job lifecycle signals**: `process_job_start_event_rules` and `process_job_end_event_rules` (FOCUS: `netbox/extras/signals.py`) fire at job start/end, using `EventContext` to feed event rule processing for job-lifecycle events specifically.

The overall pipeline is **asynchronous via RQ**: changes are serialized, flushed to an RQ queue, and then matched and dispatched by a background worker — keeping event-rule processing out of the synchronous HTTP request/response cycle.
