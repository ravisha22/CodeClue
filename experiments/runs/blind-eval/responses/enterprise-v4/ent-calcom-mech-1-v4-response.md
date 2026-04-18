# Enterprise v4 (full-stack): ent-calcom-mech-1
Date: 2026-04-18

## Answer
The prompt’s domain and cancellation-path evidence show that cancellation-reason policy starts as data on the event type and is then enforced in both server and client flows. `requiresCancellationReason` lives on `EventType` as a Prisma enum with `MANDATORY_BOTH`, `MANDATORY_HOST_ONLY`, `MANDATORY_ATTENDEE_ONLY`, and `OPTIONAL_BOTH`. The effective default is `MANDATORY_HOST_ONLY`, including the fallback case where the database column is null or a booking has no `eventTypeId`. When a cancellation request reaches the backend, the handler checks who is acting and what the event-type setting requires before allowing the cancellation to proceed. The cancellation UI mirrors that same rule so the form itself already reflects whether the reason field is mandatory for that actor.

## Synthesis
Mechanically, the setting is defined once in the event model, enforced authoritatively on the backend, and echoed in the UI so the product behavior stays consistent end to end.
