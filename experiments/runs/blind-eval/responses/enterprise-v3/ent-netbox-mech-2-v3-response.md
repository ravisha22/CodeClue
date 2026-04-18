# Enterprise v3 (arch-enhanced): ent-netbox-mech-2
Date: 2026-04-18

## Answer
The event-rule processing chain starts with change/event generation and queueing. `process_event_queue(events)` is described as flushing object representations to RQ for EventRule processing, and `flush_events(events)` also says it flushes object representations to RQ for event processing (process_event_queue, netbox/extras/events.py:258-285; flush_events, netbox/extras/events.py:286-297). Combined with the architectural summary’s statement that Redis is the companion service for task queues/cache and that `django-rq` handles background work, the supported conclusion is that monitored changes are pushed onto Redis-backed RQ processing so the follow-on work happens asynchronously (ARCH, ent-netbox-mech-2-v3.prompt.md:21,26; process_event_queue, netbox/extras/events.py:258-285).

Those queued events are then matched against event rules. `process_event_queue()` calls `process_event_rules(event_rules, object_type, event)`, and `process_event_rules()` iterates the rule list and can raise `ValueError` (process_event_queue, netbox/extras/events.py:258-285; process_event_rules, netbox/extras/events.py:162-257). `EventRulesMixin` explains what those rules do at the business level: they support transmitting webhooks or executing scripts automatically. `EventRuleActionChoices` confirms the supported actions are `webhook`, `script`, and `notification` (EventRulesMixin, netbox/netbox/models/features.py:503-508; EventRule, netbox/extras/models/models.py:54-162; EventRuleActionChoices, netbox/extras/choices.py:242-252).

The same event-rule machinery also handles job lifecycle events. `process_job_start_event_rules` and `process_job_end_event_rules` process event rules for jobs starting and ending, respectively (process_job_start_event_rules, netbox/extras/signals.py:98-112; process_job_end_event_rules, netbox/extras/signals.py:116-130).

## Gaps
The prompt does not expose the outbound delivery details for webhook payload rendering or HTTP success rules. It does not show Jinja2 webhook payload context, 2XX-only success handling, manual requeue semantics, or the `webhook_receiver` inspection tool; those remain outside the evidence provided here (GAPS, ent-netbox-mech-2-v3.prompt.md:277-280).
