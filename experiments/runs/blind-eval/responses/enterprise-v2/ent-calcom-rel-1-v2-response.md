# Enterprise v2: ent-calcom-rel-1
Date: 2026-04-17

## Question
How does the headless router flow from a submitted form to a booked meeting?

## Answer

### Overview

The flow from a submitted form to a booked meeting in Cal.diy involves three key layers: (1) form submission triggering a webhook event, (2) the `WebhookTaskerProducerService` queueing tasks for various booking lifecycle events, and (3) downstream meeting scheduling via the `BookingWebhookService`. The clue and source snippets together reveal a task-based architecture where form and booking events are queued as `WebhookTaskPayload` objects and delivered asynchronously.

### Step 1: Form Submission and Webhook Queueing

When a form is submitted, the system fires a `FORM_SUBMITTED` webhook event. The `FormSubmittedDTO` interface (FOCUS, `packages/features/webhooks/lib/dto/types.ts:175-186`) extends `BaseEventDTO` and references `WebhookTriggerEvents.FORM_SUBMITTED`. There is also a `FormSubmittedNoEventDTO` for forms that do not map to an event type (FOCUS, `packages/features/webhooks/lib/dto/types.ts:205-216`, referencing `WebhookTriggerEvents.FORM_SUBMITTED_NO_EVENT`).

The `FormSubmittedPayload` interface (FOCUS, `packages/features/webhooks/lib/factory/types.ts:6-13`) defines the payload structure for this event.

The `IWebhookProducerService` interface declares `queueFormSubmittedWebhook(params: QueueFormWebhookParams)` (FOCUS, `packages/features/webhooks/lib/interface/WebhookProducerService.ts:164`).

### Step 2: WebhookTaskerProducerService — The Central Dispatcher

The `WebhookTaskerProducerService` implements `IWebhookProducerService` (Source snippet, `packages/features/webhooks/lib/service/WebhookTaskerProducerService.ts L31-234`). It is constructed with `IWebhookTaskerProducerServiceDeps`, which requires a `webhookTasker: WebhookTasker` and a `logger: ILogger` (Source snippet, L27-30).

**Form submission path:** `queueFormSubmittedWebhook` (Source snippet, L76-97) generates an `operationId` (via `uuidv4()`), constructs a `WebhookTaskPayload` with `triggerEvent: WebhookTriggerEvents.FORM_SUBMITTED`, `formId`, `teamId`, `userId`, `oAuthClientId`, `metadata`, and a `timestamp`, then calls `this.queueTask(operationId, taskPayload)`.

**Booking lifecycle paths:** The same service provides a suite of booking-specific queuing methods, all following the same pattern:
- `queueBookingCreatedWebhook` → `WebhookTriggerEvents.BOOKING_CREATED` (Source snippet, L39-41)
- `queueBookingRescheduledWebhook` → `WebhookTriggerEvents.BOOKING_RESCHEDULED` (Source snippet, L47-49)
- `queueBookingCancelledWebhook` → `WebhookTriggerEvents.BOOKING_CANCELLED` (Source snippet, L43-45)
- `queueBookingRequestedWebhook` → `WebhookTriggerEvents.BOOKING_REQUESTED` — fires when bookings require confirmation (status = PENDING) (Source snippet, L56-58, with inline doc comment)
- `queueBookingRejectedWebhook` → `WebhookTriggerEvents.BOOKING_REJECTED` (Source snippet, L60-62)
- `queueBookingPaymentInitiatedWebhook` → `WebhookTriggerEvents.BOOKING_PAYMENT_INITIATED` (Source snippet, L64-66)
- `queueBookingPaidWebhook` → `WebhookTriggerEvents.BOOKING_PAID` (Source snippet, L68-70)
- `queueBookingNoShowUpdatedWebhook` → `WebhookTriggerEvents.BOOKING_NO_SHOW_UPDATED` (Source snippet, L72-74)
- `queueRecordingReadyWebhook` → `WebhookTriggerEvents.RECORDING_READY` (Source snippet, L99-123)
- `queueOOOCreatedWebhook` → `WebhookTriggerEvents.OOO_CREATED` (Source snippet, L125-147)

Booking-related webhooks use a private `queueBookingWebhook` helper (Source snippet, L526-556) that constructs a `WebhookTaskPayload` with `bookingUid`, `eventTypeId`, `teamId`, `userId`, `orgId`, `oAuthClientId`, `metadata`, and `timestamp`. Payment webhooks use a separate `queuePaymentWebhook` helper (Source snippet, L561-587).

### Step 3: Task Delivery via WebhookTasker

The private `queueTask` method (Source snippet, L222-233) calls `this.deps.webhookTasker.deliverWebhook(taskPayload)`. The inline documentation states: "The WebhookTasker automatically selects the appropriate execution mode: Production: Queues to Trigger.dev for background processing; E2E Tests: Executes immediately via WebhookSyncTasker" (Source snippet, L589-595). This shows the delivery is asynchronous in production and synchronous in tests.

### Step 4: Meeting Scheduling via BookingWebhookService

Once a booking is created, the `BookingWebhookService` handles meeting-related webhook scheduling:

- `scheduleMeetingWebhooks` (FOCUS, `packages/features/webhooks/lib/service/BookingWebhookService.ts:239-328`) accumulates meeting webhook subscriptions using `webhookService.getSubscribers` scoped to `params.booking.userId` and `params.booking.eventTypeId`.
- `cancelScheduledMeetingWebhooks` (FOCUS, `packages/features/webhooks/lib/service/BookingWebhookService.ts:330-337`) cancels scheduled webhooks for `WebhookTriggerEvents.MEETING_STARTED` via `webhookService.cancelScheduledWebhooks`.
- `scheduleNoShowWebhooks` (FOCUS, `packages/features/webhooks/lib/service/BookingWebhookService.ts:339-439`) schedules no-show detection webhooks with precedence logic on `params` and `failureCount`, calling `getTasker` for async task scheduling.

### Step 5: Meeting Event Types

Meeting-related trigger events are defined as:
- `MeetingStartedDTO` → `WebhookTriggerEvents.MEETING_STARTED` (FOCUS, `packages/features/webhooks/lib/dto/types.ts:217-259`)
- `MeetingEndedDTO` → `WebhookTriggerEvents.MEETING_ENDED` (FOCUS, `packages/features/webhooks/lib/dto/types.ts:260-302`)
- `InstantMeetingDTO` → `WebhookTriggerEvents.INSTANT_MEETING` (FOCUS, `packages/features/webhooks/lib/dto/types.ts:303-313`)

The `MeetingPayloadBuilder` (FOCUS, `packages/features/webhooks/lib/factory/versioned/v2021-10-20/MeetingPayloadBuilder.ts:19-50`) extends `BaseMeetingPayloadBuilder` and handles `AFTER_HOSTS_CAL_VIDEO_NO_SHOW` and `AFTER_GUESTS_CAL_VIDEO_NO_SHOW` trigger events.

### Supporting Infrastructure

- **Booking repository** — `BookingRepository.getBookingForCalEventBuilder` (FOCUS, `packages/features/bookings/repositories/BookingRepository.ts:1623-1628`) and `getBookingForCalEventBuilderFromUid` (FOCUS, `packages/features/bookings/repositories/BookingRepository.ts:1630-1635`) delegate to `prismaClient.booking.findUnique` to fetch booking data.
- **Calendar event building** — `BookingForCalEventBuilder` type (FOCUS, `packages/features/CalendarEventBuilder.ts:72`) is derived from `BookingRepository["getBookingForCalEventBuilder"]`.
- **Recurring bookings** — `mapRecurringBookingToMutationInput` (FOCUS, `packages/features/bookings/lib/client/booking-event-form/booking-to-mutation-input-mapper.tsx:98-131`) transforms recurring booking options using `recurringDates.map`.
- **Video integration** — `BookingVideoService_2024_08_13.deleteOldVideoMeetingIfNeeded` (FOCUS, `apps/api/v2/src/platform/bookings/2024-08-13/services/booking-video.service.ts:13-40`) handles video meeting cleanup.
- **Router helpers** — `useRouterHelpers` (FOCUS, `apps/web/modules/embed/components/Embed.tsx:105-133`) manages query param routing for the embed layer.

### Gaps and Uncertainties

The GAPS section identifies this as a MECHANISTIC question requiring body logic for a full answer, with 83 symbols at L3 and only 11 with behavior annotations. The following symbols are uncovered: `IUseBookingForm`, `InstantMeetingBuilder`, `InstantMeetingPayload`, `JoinMeetingButtonProps` (GAPS). This means the exact UI-to-handler binding (how a form component's submit handler invokes the booking mutation) and the `InstantMeetingBuilder` construction logic are not available from the clue.

The drill-down target was `WebhookTaskerProducerService.queueFormSubmittedWebhook` (GAPS, drill), and the source snippets confirm its implementation.

### Synthesis

The headless flow proceeds: Form submission → `WebhookTaskerProducerService.queueFormSubmittedWebhook` constructs a `WebhookTaskPayload` with `FORM_SUBMITTED` trigger and `formId` → `queueTask` delivers via `WebhookTasker.deliverWebhook` (Trigger.dev in production, sync in E2E) → On booking creation, `queueBookingCreatedWebhook` fires `BOOKING_CREATED` → `BookingWebhookService.scheduleMeetingWebhooks` schedules `MEETING_STARTED`/`MEETING_ENDED` webhooks for subscribers. The exact form-to-booking-mutation binding (the "headless router" itself) is not fully visible in the clue — `IUseBookingForm` is listed as uncovered. However, the webhook-driven architecture clearly decouples form submission from booking execution, with the `WebhookTaskerProducerService` acting as the central event dispatcher across the entire booking lifecycle.
