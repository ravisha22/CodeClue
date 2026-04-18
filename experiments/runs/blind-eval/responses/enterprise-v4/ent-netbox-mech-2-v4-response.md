# Enterprise v4 (full-stack): ent-netbox-mech-2
Date: 2026-04-18

## Answer
The event/webhook workflow in the prompt makes the chain explicit. When a monitored object change happens, NetBox does not synchronously perform the downstream work; it drops the resulting event into Redis-backed queues so the user-facing request can complete quickly. `rqworker` processes later pull those queued events or webhook jobs and send them asynchronously. The payload side is templated and rich: webhooks can use Jinja2 bodies and receive context including the event type, timestamp, object type, username, request ID, current data, and pre-change/post-change snapshots. Delivery semantics are strict as well: only 2XX HTTP responses count as success, failed jobs can be requeued manually, and the local `webhook_receiver` helper is just an inspection endpoint that prints what was sent.

## Synthesis
So the mechanism is queue first, deliver later: change capture is decoupled from outbound integration, while payload rendering and retry handling stay explicit and inspectable.
