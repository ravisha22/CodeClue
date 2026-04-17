# Enterprise Eval: ent-calcom-rel-1
Date: 2026-04-17

## Question
How does the headless router flow from a submitted form to a booked meeting?

## Reasoning Scaffold

### Relevant Symbols and Tracing

The question asks about the end-to-end flow: form submission → webhook/event processing → booked meeting. I will trace through the clue file's FOCUS entries, then confirm with the source snippets.

### Step 1: Form Submission Triggers a Webhook

**FormSubmittedDTO** (`packages/features/webhooks/lib/dto/types.ts:175-186`, FOCUS):
- Interface extending `BaseEventDTO`
- Uses `WebhookTriggerEvents.FORM_SUBMITTED`
- This is the DTO representing a form submission event in the webhook system.

**FormSubmittedNoEventDTO** (`packages/features/webhooks/lib/dto/types.ts:205-216`, FOCUS):
- Also extends `BaseEventDTO`
- Uses `WebhookTriggerEvents.FORM_SUBMITTED_NO_EVENT`
- A variant for form submissions that don't have an associated event type.

**FormSubmittedPayload** (`packages/features/webhooks/lib/factory/types.ts:6-13`, FOCUS):
- Interface representing the payload structure for form-submitted webhooks.

### Step 2: The Producer Service Queues the Webhook

**IWebhookProducerService.queueFormSubmittedWebhook** (`packages/features/webhooks/lib/interface/WebhookProducerService.ts:164`, FOCUS):
- Interface method signature: `queueFormSubmittedWebhook(params: QueueFormWebhookParams)`
- Defines the contract for queuing form submission webhooks.

**WebhookTaskerProducerService.queueFormSubmittedWebhook** (`packages/features/webhooks/lib/service/WebhookTaskerProducerService.ts:76-97`, FOCUS + Source Snippet):
- Implements `IWebhookProducerService` (Source Snippet: `class WebhookTaskerProducerService implements IWebhookProducerService`)
- Generates an `operationId` via `uuidv4()` (Source Snippet L76-82)
- Constructs a `WebhookTaskPayload` with:
  - `triggerEvent: WebhookTriggerEvents.FORM_SUBMITTED`
  - `formId: params.formId`
  - `teamId`, `userId`, `oAuthClientId`, `metadata`, `timestamp`
- Calls `this.queueTask(operationId, taskPayload)` (Source Snippet L95)

### Step 3: The Task Queue Delivers the Webhook

**WebhookTaskerProducerService.queueTask** (`WebhookTaskerProducerService.ts:222-233`, Source Snippet):
- Private method that calls `this.deps.webhookTasker.deliverWebhook(taskPayload)`
- The `WebhookTasker` is injected via `IWebhookTaskerProducerServiceDeps` (Source Snippet L27-30): `{ webhookTasker: WebhookTasker; logger: ILogger; }`
- Per the source comment (Source Snippet L614-620): "The WebhookTasker automatically selects the appropriate execution mode: Production: Queues to Trigger.dev for background processing; E2E Tests: Executes immediately via WebhookSyncTasker"

### Step 4: Booking Lifecycle Webhook Events

The `WebhookTaskerProducerService` class (Source Snippet, full class L31-234) provides a complete set of booking lifecycle queue methods, each delegating to internal helpers:

**Booking-related webhooks** (all via `queueBookingWebhook` private helper, Source Snippet L551-581):
1. `queueBookingCreatedWebhook` → `WebhookTriggerEvents.BOOKING_CREATED` (Source Snippet L39-41)
2. `queueBookingCancelledWebhook` → `WebhookTriggerEvents.BOOKING_CANCELLED` (Source Snippet L43-45)
3. `queueBookingRescheduledWebhook` → `WebhookTriggerEvents.BOOKING_RESCHEDULED` (Source Snippet L47-49)
4. `queueBookingRequestedWebhook` → `WebhookTriggerEvents.BOOKING_REQUESTED` — fires when bookings require confirmation (status = PENDING) (Source Snippet L450-457, with doc comment)
5. `queueBookingRejectedWebhook` → `WebhookTriggerEvents.BOOKING_REJECTED` (Source Snippet L60-62)
6. `queueBookingNoShowUpdatedWebhook` → `WebhookTriggerEvents.BOOKING_NO_SHOW_UPDATED` (Source Snippet L72-74)

**Payment-related webhooks** (via `queuePaymentWebhook` private helper, Source Snippet L586-612):
7. `queueBookingPaymentInitiatedWebhook` → `WebhookTriggerEvents.BOOKING_PAYMENT_INITIATED` (Source Snippet L64-66)
8. `queueBookingPaidWebhook` → `WebhookTriggerEvents.BOOKING_PAID` (Source Snippet L68-70)

**Non-booking webhooks**:
9. `queueRecordingReadyWebhook` → `WebhookTriggerEvents.RECORDING_READY` (Source Snippet L99-123)
10. `queueOOOCreatedWebhook` → `WebhookTriggerEvents.OOO_CREATED` (Source Snippet L125-147)

### Step 5: Meeting Scheduling via BookingWebhookService

**BookingWebhookService.scheduleMeetingWebhooks** (`packages/features/webhooks/lib/service/BookingWebhookService.ts:239-328`, FOCUS):
- Behavior: `ACCUMULATE(scheduleMeetingWebhoo... -> result)`
- Uses `this.webhookService`, `webhookService.getSubscribers`, `params.booking.userId`, `params.booking.eventTypeId`
- This method schedules meeting-related webhooks (MEETING_STARTED, MEETING_ENDED) for a booking.

**BookingWebhookService.cancelScheduledMeetingWebhooks** (`BookingWebhookService.ts:330-337`, FOCUS):
- Uses `webhookService.cancelScheduledWebhooks`, `params.bookingId`, `WebhookTriggerEvents.MEETING_STARTED`
- Can cancel previously scheduled meeting webhooks.

### Step 6: Meeting DTOs and Video Integration

**MeetingStartedDTO** (`packages/features/webhooks/lib/dto/types.ts:217-259`, FOCUS):
- Extends `BaseEventDTO`, uses `WebhookTriggerEvents.MEETING_STARTED`

**MeetingEndedDTO** (`packages/features/webhooks/lib/dto/types.ts:260-302`, FOCUS):
- Extends `BaseEventDTO`, uses `WebhookTriggerEvents.MEETING_ENDED`

**InstantMeetingDTO** (`packages/features/webhooks/lib/dto/types.ts:303-313`, FOCUS):
- Extends `BaseEventDTO`, uses `WebhookTriggerEvents.INSTANT_MEETING`

**MeetingPayloadBuilder** (`packages/features/webhooks/lib/factory/versioned/v2021-10-20/MeetingPayloadBuilder.ts:19-50`, FOCUS):
- Extends `BaseMeetingPayloadBuilder`
- Uses `dto.triggerEvent`, `WebhookTriggerEvents.AFTER_HOSTS_CAL_VIDEO_NO_SHOW`, `WebhookTriggerEvents.AFTER_GUESTS_CAL_VIDEO_NO_SHOW`

**BookingVideoService_2024_08_13.deleteOldVideoMeetingIfNeeded** (`apps/api/v2/src/platform/bookings/2024-08-13/services/booking-video.service.ts:13-40`, FOCUS):
- Guards on `!booking || !booking.user`
- Filters booking references by type to find video meetings

### Step 7: Supporting UI/Form Infrastructure

**useRouterHelpers** (`apps/web/modules/embed/components/Embed.tsx:105-133`, FOCUS):
- Behavior: `ACCUMULATE(useRouterHelpers loop -> result)`
- Called by `useEmbedGoto`
- Manages search params for embed routing

**PlainForm** (`packages/ui/components/address/fields.tsx:202-244`, FOCUS):
- A generic form component; behavior includes `event.preventDefault`, `event.stopPropagation`

**useCreateEventTypeForm** (`packages/platform/atoms/hooks/event-types/private/useCreateEventTypeForm.ts:11-32`, FOCUS):
- Uses `form.watch`, `SchedulingType.MANAGED`, `form.setValue`

### GAPS — What Cannot Be Determined

The GAPS section states:
- **Type**: MECHANISTIC (body logic needed for full answer)
- **Coverage**: 80 symbols in L3, 11 with behavior annotations
- **Uncovered symbols**: `IUseBookingForm`, `InstantMeetingBuilder`, `InstantMeetingPayload`, `JoinMeetingButtonProps`
- **Drill target**: `WebhookTaskerProducerService.queueFormSubmittedWebhook` (~17 lines) — this was resolved via the source snippets.

The following **cannot be determined**:
1. **`IUseBookingForm`** — the hook interface that connects form state to booking creation. This is the critical missing link between "form submitted" and "booking created."
2. **`InstantMeetingBuilder`** and **`InstantMeetingPayload`** — how instant meetings are constructed from form data.
3. **`JoinMeetingButtonProps`** — the UI component interface for joining meetings.
4. The **`queueBookingWebhook` internal helper's full type constraints** are visible in the source snippet but the upstream callers (who invoke `queueBookingCreatedWebhook` after a form is processed) are not shown.
5. The **routing layer** between `FormSubmittedDTO` and `BOOKING_CREATED` — i.e., what service receives the form submission and decides to create a booking — is not covered in the clue.

### Synthesis: The End-to-End Flow

Based on the available evidence, the headless router flow from form submission to booked meeting follows this path:

```
Form Submission
    │
    ▼
WebhookTaskerProducerService.queueFormSubmittedWebhook()
    │  constructs WebhookTaskPayload with FORM_SUBMITTED trigger
    │  includes formId, teamId, userId, oAuthClientId, metadata, timestamp
    │  (Source Snippet: WebhookTaskerProducerService.ts L76-97)
    │
    ▼
WebhookTaskerProducerService.queueTask()
    │  calls this.deps.webhookTasker.deliverWebhook(taskPayload)
    │  (Source Snippet: WebhookTaskerProducerService.ts L222-233)
    │  Production: queues to Trigger.dev
    │  E2E: executes via WebhookSyncTasker
    │
    ▼
[BOOKING CREATION — not visible in clue]
    │  IUseBookingForm (GAPS: uncovered) connects form → booking
    │
    ▼
WebhookTaskerProducerService.queueBookingCreatedWebhook()
    │  triggers WebhookTriggerEvents.BOOKING_CREATED
    │  (Source Snippet: WebhookTaskerProducerService.ts L39-41)
    │
    ▼
BookingWebhookService.scheduleMeetingWebhooks()
    │  schedules MEETING_STARTED / MEETING_ENDED webhooks
    │  uses webhookService.getSubscribers for the booking's userId/eventTypeId
    │  (FOCUS: BookingWebhookService.ts:239-328)
    │
    ▼
Meeting DTOs dispatched:
    ├── MeetingStartedDTO (MEETING_STARTED)
    ├── MeetingEndedDTO (MEETING_ENDED)
    ├── InstantMeetingDTO (INSTANT_MEETING)
    └── MeetingPayloadBuilder handles NO_SHOW variants
```

**Key supported conclusions:**
- The `WebhookTaskerProducerService` is the central producer, implementing `IWebhookProducerService`, that queues all webhook events through a `WebhookTasker` dependency (confirmed by source snippets).
- Form submissions produce `FORM_SUBMITTED` events with form-specific metadata (formId, not bookingUid).
- Booking events produce booking-specific payloads (bookingUid, eventTypeId, orgId).
- The `queueTask` method delegates to `webhookTasker.deliverWebhook()` with environment-aware execution (Trigger.dev vs sync).
- `BookingWebhookService` separately handles meeting lifecycle scheduling (start/end/no-show).

**Key unresolved uncertainty:**
- The critical middle step — how a submitted form *becomes* a booking (the `IUseBookingForm` interface and its implementation) — is in the GAPS and cannot be traced from the available evidence.
- Whether `FORM_SUBMITTED` webhooks directly trigger booking creation or if the form submission is handled by a separate booking service that then fires `BOOKING_CREATED` is not determinable.
