# Enterprise v4 (full-stack): ent-calcom-rel-2
Date: 2026-04-18

## Answer
The webhook surface in the prompt maps booking lifecycle states to distinct outbound event families rather than one generic callback. Triggers include booking created, cancelled, rescheduled, confirmed, rejected, requested, payment initiated, no-show updated, meeting started and ended, recording ready, instant meeting, transcription generated, and form submitted. Within that set, created bookings are treated as their own webhook family with a structured booking payload, while cancelled and rescheduled events use their own payload variants instead of collapsing everything into one undifferentiated booking shape. Delivery is also split into two concerns: one stage selects the booking event and constructs the appropriate payload, and a separate outbound transport/signing stage sends the request.

## Synthesis
So Cal.diy’s webhook model ties each lifecycle transition to an event-specific payload contract, then hands that contract to a distinct delivery/signing pipeline.
