# Enterprise v2: ent-calcom-rel-2
Date: 2026-04-17

## Question
How do Cal.diy webhooks map booking lifecycle events to outgoing requests?

## Answer

### Overview

Cal.diy maps booking lifecycle events to outgoing webhook requests through a layered architecture: trigger event types define the lifecycle stages, a `BookingWebhookService` orchestrates scheduling and cancellation, a `WebhookRepository` manages subscriber lookups with permission checks, and payload builder factories construct versioned payloads. The mapping is organized around two main event categories — **BookingTriggerEvents** and **MeetingTriggerEvents** — each with distinct trigger semantics.

### Booking Trigger Events

The `BookingTriggerEvents` type alias (FOCUS, `packages/features/webhooks/lib/factory/versioned/PayloadBuilderFactory.ts:104-105`) enumerates the core booking lifecycle webhooks:

| Trigger Event | Lifecycle Stage |
|---|---|
| `WebhookTriggerEvents.BOOKING_CREATED` | A new booking is confirmed |
| `WebhookTriggerEvents.BOOKING_RESCHEDULED` | An existing booking's time changes |
| `WebhookTriggerEvents.BOOKING_CANCELLED` | A booking is cancelled |
| `WebhookTriggerEvents.BOOKING_REJECTED` | A pending booking is rejected |
| `WebhookTriggerEvents.BOOKING_REQUESTED` | A booking requiring confirmation is requested |
| `WebhookTriggerEvents.BOOKING_PAYMENT_INITIATED` | Payment for a booking begins |
| `WebhookTriggerEvents.BOOKING_PAID` | Payment for a booking completes |

(FOCUS, `BookingTriggerEvents`, `packages/features/webhooks/lib/factory/versioned/PayloadBuilderFactory.ts:104-105`)

### Meeting Trigger Events

The `MeetingTriggerEvents` type alias (FOCUS, `packages/features/webhooks/lib/factory/versioned/PayloadBuilderFactory.ts:124-125`) covers real-time meeting state:

| Trigger Event | Lifecycle Stage |
|---|---|
| `WebhookTriggerEvents.MEETING_STARTED` | A scheduled meeting begins |
| `WebhookTriggerEvents.MEETING_ENDED` | A meeting concludes |
| `WebhookTriggerEvents.AFTER_HOSTS_CAL_VIDEO_NO_SHOW` | Host fails to join Cal Video |
| `WebhookTriggerEvents.AFTER_GUESTS_CAL_VIDEO_NO_SHOW` | Guest fails to join Cal Video |

(FOCUS, `MeetingTriggerEvents`, `packages/features/webhooks/lib/factory/versioned/PayloadBuilderFactory.ts:124-125`)

### BookingWebhookService — Orchestration Layer

The `BookingWebhookService` (located in `packages/features/webhooks/lib/service/BookingWebhookService.ts`) orchestrates how lifecycle events translate to outgoing webhook requests through three key methods:

1. **`scheduleMeetingWebhooks`** (FOCUS, `packages/features/webhooks/lib/service/BookingWebhookService.ts:239-328`) — Accumulates webhook subscribers using `webhookService.getSubscribers` scoped by `params.booking.userId` and `params.booking.eventTypeId`. The behavior annotation `ACCUMULATE(scheduleMeetingWebhoo... -> result)` indicates it iterates over matching subscribers to schedule outgoing requests for each.

2. **`cancelScheduledMeetingWebhooks`** (FOCUS, `packages/features/webhooks/lib/service/BookingWebhookService.ts:330-337`) — Cancels previously scheduled webhooks for a specific booking using `webhookService.cancelScheduledWebhooks` with `params.bookingId` and `WebhookTriggerEvents.MEETING_STARTED`. This shows that meeting-start webhooks can be pre-scheduled and later revoked (e.g., when a booking is cancelled).

3. **`scheduleNoShowWebhooks`** (FOCUS, `packages/features/webhooks/lib/service/BookingWebhookService.ts:339-439`) — Schedules no-show detection webhooks with precedence logic (`PRECEDENCE(params -> failureCount)`) and accumulation (`ACCUMULATE`). It uses `webhookService.getSubscribers` and calls `getTasker` to queue the no-show check, incorporating `params.triggerForUser` to scope the no-show trigger.

### WebhookRepository — Subscriber Resolution and Permissions

The `WebhookRepository` (INDEX, `packages/features/webhooks/lib/repository/WebhookRepository.ts`, 592L) provides subscriber lookup with embedded permission checking:

- `checkPermission` — Validates the requester's authorization to access webhooks (INDEX)
- `hasPermission` — Boolean permission check (INDEX)
- `getTeamIdsWithPermission` — Retrieves team-scoped permissions (INDEX)
- `PermissionCheckService` — Dedicated permission service (INDEX)

This indicates that outgoing webhook requests are only dispatched to subscribers whose permissions are validated through this repository layer.

### Webhook Input Transformation (API v2)

At the API v2 layer, webhook inputs are transformed through pipes:

- `WebhookInputPipe.transform` (SYM, `apps/api/v2/src/modules/webhooks/pipes/WebhookInputPipe.ts:6`) — Transforms incoming webhook configuration
- `PartialWebhookInputPipe.transform` (SYM, `apps/api/v2/src/modules/webhooks/pipes/WebhookInputPipe.ts:16`) — Handles partial webhook updates

### Payload Construction

The `BookingExtraDataMap` type (FOCUS, `packages/features/webhooks/lib/factory/base/BaseBookingPayloadBuilder.ts:11`) defines additional data that can accompany booking webhook payloads. The factory pattern in `PayloadBuilderFactory.ts` (where both `BookingTriggerEvents` and `MeetingTriggerEvents` are defined) suggests a versioned payload builder design where the trigger event type dispatches to the appropriate builder.

### Booking Data Access

The webhook system accesses booking data through:

- `BookingRepository.getBookingForCalEventBuilder` (FOCUS, `packages/features/bookings/repositories/BookingRepository.ts:1623-1628`) — Fetches booking by ID via `prismaClient.booking.findUnique`
- `BookingRepository.getBookingForCalEventBuilderFromUid` (FOCUS, `packages/features/bookings/repositories/BookingRepository.ts:1630-1635`) — Fetches booking by UID
- `IBookingRepository.getBookingForCalEventBuilderFromUid` (FOCUS, `packages/features/bookings/repositories/IBookingRepository.ts:52`) — Interface declaration
- `BookingRepository.findBookingIncludeCalVideoSettingsAndReferences` (FOCUS, `packages/features/bookings/repositories/BookingRepository.ts:896-967`) — Rich booking fetch including video settings and references
- `BookingForCalEventBuilder` type (FOCUS, `packages/features/CalendarEventBuilder.ts:72`) — Type alias wrapping the repository return type

### Recurring and Input Mapping

`mapRecurringBookingToMutationInput` (FOCUS, `packages/features/bookings/lib/client/booking-event-form/booking-to-mutation-input-mapper.tsx:98-131`) transforms recurring booking options with `recurringDates.map`, using `booking.date`, `booking.timeZone`, and `booking.event.recurringEvent`.

The API v2 video integration path — `BookingLocationIntegrationService_2024_08_13.handleCalVideoLocation` (FOCUS, `apps/api/v2/src/platform/bookings/2024-08-13/services/booking-location-integration.service.ts:141-186`) — delegates to `updateBookingWithVideoLocation` and interacts with `calendarSyncService.buildCalEventFromBookingData`, showing how booking location changes can trigger further webhook-relevant state updates.

### Gaps and Uncertainties

The GAPS section states this is a STRUCTURAL question with 83 symbols at L3 and 24 with behavior annotations. Critically, the following `IWebhookProducerService` methods are **uncovered** (GAPS):
- `IWebhookProducerService.queueBookingCreatedWebhook`
- `IWebhookProducerService.queueBookingNoShowUpdatedWebhook`
- `IWebhookProducerService.queueBookingPaidWebhook`
- `IWebhookProducerService.queueBookingPaymentInitiatedWebhook`

This means the exact implementation of how each booking lifecycle event is queued for outgoing delivery is not visible — only the subscriber-resolution and scheduling orchestration in `BookingWebhookService` and the type definitions in `PayloadBuilderFactory` are available. The actual HTTP dispatch mechanism (how `deliverWebhook` sends the HTTP request to the subscriber's endpoint) is not present in the clue.

### Synthesis

Cal.diy webhooks map booking lifecycle events to outgoing requests through: (1) **Event typing** — `BookingTriggerEvents` (7 events covering create/reschedule/cancel/reject/request/payment flows) and `MeetingTriggerEvents` (4 events covering start/end/no-show); (2) **Subscriber resolution** — `WebhookRepository` with permission-gated `getSubscribers`; (3) **Orchestration** — `BookingWebhookService` scheduling/cancelling meeting webhooks and no-show detection; (4) **Payload construction** — versioned builders via `PayloadBuilderFactory`. The outgoing request dispatch itself (the HTTP call to subscriber endpoints) is behind the uncovered `IWebhookProducerService.queueBooking*` methods and the `WebhookTasker` delivery mechanism.
