# Enterprise Eval: ent-calcom-rel-2
Date: 2026-04-17

## Question
How do Cal.diy webhooks map booking lifecycle events to outgoing requests?

## Reasoning Scaffold

### Relevant Symbols Identification

The clue file's FOCUS section is heavily oriented toward the webhook system, booking lifecycle types, and the data-fetching pipeline. I trace the flow from trigger event definitions through to subscriber dispatch.

### 1. Booking Lifecycle Event Taxonomy

The webhook system defines booking lifecycle events via type aliases in the **PayloadBuilderFactory** module:

**BookingTriggerEvents** (`packages/features/webhooks/lib/factory/versioned/PayloadBuilderFactory.ts:104-105`, FOCUS):
- Defined as a union type: `BOOKING_CREATED | BOOKING_RESCHEDULED | BOOKING_CANCELLED | BOOKING_REJECTED | BOOKING_REQUESTED | BOOKING_PAYMENT_INITIATED | BOOKING_PAID`
- These are the core booking lifecycle transitions.

**MeetingTriggerEvents** (`packages/features/webhooks/lib/factory/versioned/PayloadBuilderFactory.ts:124-125`, FOCUS):
- Union type: `MEETING_STARTED | MEETING_ENDED | AFTER_HOSTS_CAL_VIDEO_NO_SHOW | AFTER_GUESTS_CAL_VIDEO_NO_SHOW`
- These track real-time meeting state via Cal Video.

**PaymentTriggerEvents** (`packages/features/webhooks/lib/factory/versioned/PayloadBuilderFactory.ts:114-115`, FOCUS):
- Union type: `BOOKING_PAYMENT_INITIATED | BOOKING_PAID`
- A subset of booking triggers specifically for payment workflows.

**BookingActionType** (`packages/features/bookings/lib/BookingEmailSmsHandler.ts:20-21`, FOCUS):
- Type alias: `(typeof BookingActionMap)["confirmed"]`
- Maps booking actions to handler dispatch in the email/SMS system.

### 2. Webhook Scheduling and Cancellation

**BookingWebhookService.scheduleMeetingWebhooks** (`packages/features/webhooks/lib/service/BookingWebhookService.ts:239-328`, FOCUS):
- Behavior: `ACCUMULATE(scheduleMeetingWebhoo... -> result)`
- Uses: `this.webhookService`, `webhookService.getSubscribers`, `params.booking.userId`, `params.booking.eventTypeId`
- This method looks up webhook subscribers for a booking's user and event type, then schedules meeting-related webhooks (MEETING_STARTED, MEETING_ENDED).

**BookingWebhookService.cancelScheduledMeetingWebhooks** (`BookingWebhookService.ts:330-337`, FOCUS):
- Uses: `webhookService.cancelScheduledWebhooks`, `params.bookingId`, `WebhookTriggerEvents.MEETING_STARTED`
- Cancels previously scheduled MEETING_STARTED webhooks for a given booking ID.

**BookingWebhookService.scheduleNoShowWebhooks** (`BookingWebhookService.ts:339-439`, FOCUS):
- Behavior: `PRECEDENCE(params -> failureCount); ACCUMULATE(scheduleNoShowWebhook... -> result); TRANSFORM(map)`
- Calls: `getTasker`
- Uses: `this.webhookService`, `this.getTasker`, `webhookService.getSubscribers`, `params.triggerForUser`
- Schedules no-show detection webhooks. The PRECEDENCE annotation indicates params are checked first, then failure counts. The method accumulates results and transforms them, using a tasker for deferred execution.

### 3. Webhook Data Fetching Pipeline

**BookingWebhookDataFetcher.fetchEventData** (`packages/features/webhooks/lib/service/data-fetchers/BookingWebhookDataFetcher.ts:27-73`, FOCUS):
- Behavior: `GUARD(!bookingUid -> this.logger.warn("M...); PRECEDENCE(not_bookingUid -> not_booking -> not_calendarEvent)`
- Uses: `this.logger.warn`, `this.bookingRepository.getBookingForCalEventBuilderFromUid`, `CalendarEventBuilder.fromBooking`, `payload.oAuthClientId`
- This fetcher retrieves booking data for webhook payloads:
  1. Guards against missing `bookingUid` (logs warning)
  2. Fetches the booking via `BookingRepository.getBookingForCalEventBuilderFromUid`
  3. Builds a `CalendarEvent` via `CalendarEventBuilder.fromBooking`
  4. Uses `oAuthClientId` from the payload for platform context

### 4. Booking Repository Support

**BookingRepository.getBookingForCalEventBuilder** (`packages/features/bookings/repositories/BookingRepository.ts:1623-1628`, FOCUS):
- Delegates to `this.prismaClient.booking.findUnique`
- Retrieves a booking by numeric ID for calendar event building.

**BookingRepository.getBookingForCalEventBuilderFromUid** (`BookingRepository.ts:1630-1635`, FOCUS):
- Delegates to `this.prismaClient.booking.findUnique`
- Retrieves a booking by UID string — this is what the webhook data fetcher calls.

**IBookingRepository.getBookingForCalEventBuilderFromUid** (`packages/features/bookings/repositories/IBookingRepository.ts:52`, FOCUS):
- Interface method confirming the repository contract.

**BookingForCalEventBuilder** (`packages/features/CalendarEventBuilder.ts:72`, FOCUS):
- Type alias: `NonNullable<Awaited<ReturnType<BookingRepository["getBookingForCalEventBuilder"]>>>`
- This derives the booking type from the repository method's return type.

**BookingRepository.findBookingIncludeCalVideoSettingsAndReferences** (`BookingRepository.ts:896-967`, FOCUS):
- Delegates to `this.prismaClient.booking.findUnique`
- Retrieves booking with Cal Video settings and references — used for video-related webhook payloads.

### 5. Webhook Infrastructure

**WebhookRepository** (`packages/features/webhooks/lib/repository/WebhookRepository.ts`, 592 lines, INDEX):
- Methods: `checkPermission`, `constructor`, `getTeamIdsWithPermission`, `hasPermission`, `PermissionCheckService`
- This repository manages webhook subscription CRUD and permission checks for teams.

**WebhookInputPipe.transform** (`apps/api/v2/src/modules/webhooks/pipes/WebhookInputPipe.ts:6`, SYM):
- Transforms incoming webhook configuration input in the API v2 layer.

**PartialWebhookInputPipe.transform** (`WebhookInputPipe.ts:16`, SYM):
- Handles partial webhook input updates.

### 6. Booking Location and Video Integration

**BookingLocationIntegrationService_2024_08_13.handleCalVideoLocation** (`apps/api/v2/src/platform/bookings/2024-08-13/services/booking-location-integration.service.ts:141-186`, FOCUS):
- Behavior: `DELEGATE(this.updateBookingWithVideoLocation -> result)`
- Called by: `handleGoogleMeetLocation`
- Uses: `this.bookingVideoService.deleteOldVideoMeetingIfNeeded`, `this.calendarSyncService.buildCalEventFromBookingData`
- This connects booking creation to video meeting provisioning, which then triggers meeting lifecycle webhooks.

### 7. Extra Payload Data

**BookingExtraDataMap** (`packages/features/webhooks/lib/factory/base/BaseBookingPayloadBuilder.ts:11`, FOCUS):
- Type alias for extra data attached to booking webhook payloads.

### 8. Email/SMS Side Effects

**BookingEmailSmsHandler.send** (`packages/features/bookings/lib/BookingEmailSmsHandler.ts:94-106`, FOCUS — from mech-1 clue but cross-referenced):
- Dispatches to `_handleConfirmed`, `_handleRequested`, `_handleRescheduled`, `_handleRoundRobinRescheduled`
- This runs in parallel with webhooks as a side effect of booking lifecycle events.

### GAPS — What Cannot Be Determined

The GAPS section states:
- **Type**: MECHANISTIC (body logic needed for full answer)
- **Coverage**: 80 symbols in L3, 24 with behavior annotations
- **Uncovered symbols**:
  - `IWebhookProducerService.queueBookingCreatedWebhook` — the interface method for queuing booking creation webhooks
  - `IWebhookProducerService.queueBookingNoShowUpdatedWebhook` — no-show update queuing
  - `IWebhookProducerService.queueBookingPaidWebhook` — payment completion queuing
  - `IWebhookProducerService.queueBookingPaymentInitiatedWebhook` — payment initiation queuing

These uncovered symbols mean:
1. The **producer service interface** for booking-specific webhook queuing is not fully visible. We can see the `BookingWebhookService` scheduling side but not the `IWebhookProducerService` implementations for booking CRUD webhooks.
2. The **exact payload construction** for `BOOKING_CREATED`, `BOOKING_PAID`, etc. within the producer is unknown.
3. How **subscriber matching** works inside `webhookService.getSubscribers` is not detailed.

### Synthesis: Webhook-to-Request Mapping

The Cal.diy webhook system maps booking lifecycle events to outgoing requests through a layered architecture:

**Layer 1 — Event Taxonomy** (PayloadBuilderFactory):
| Category | Trigger Events |
|----------|---------------|
| Booking | `BOOKING_CREATED`, `BOOKING_RESCHEDULED`, `BOOKING_CANCELLED`, `BOOKING_REJECTED`, `BOOKING_REQUESTED`, `BOOKING_PAYMENT_INITIATED`, `BOOKING_PAID` |
| Meeting | `MEETING_STARTED`, `MEETING_ENDED`, `AFTER_HOSTS_CAL_VIDEO_NO_SHOW`, `AFTER_GUESTS_CAL_VIDEO_NO_SHOW` |
| Payment | `BOOKING_PAYMENT_INITIATED`, `BOOKING_PAID` (subset of Booking) |

**Layer 2 — Scheduling** (BookingWebhookService):
- `scheduleMeetingWebhooks`: Accumulates meeting webhook schedules for a booking, looking up subscribers by `userId` and `eventTypeId`.
- `cancelScheduledMeetingWebhooks`: Cancels `MEETING_STARTED` webhooks by `bookingId`.
- `scheduleNoShowWebhooks`: Schedules no-show detection, using a tasker for deferred execution, with precedence on params and failure count.

**Layer 3 — Data Fetching** (BookingWebhookDataFetcher):
- Fetches booking by UID via `BookingRepository.getBookingForCalEventBuilderFromUid`
- Builds a `CalendarEvent` via `CalendarEventBuilder.fromBooking`
- Guards against missing bookingUid, logs warnings
- Includes platform context via `oAuthClientId`

**Layer 4 — Payload Building** (PayloadBuilderFactory + BaseBookingPayloadBuilder):
- Versioned payload builders (e.g., `v2021-10-20/MeetingPayloadBuilder` extending `BaseMeetingPayloadBuilder`)
- `BookingExtraDataMap` for additional metadata
- Payload builders dispatch on `dto.triggerEvent` to construct version-specific payloads

**Layer 5 — Permission & Delivery** (WebhookRepository):
- 592-line repository with `checkPermission`, `hasPermission`, `getTeamIdsWithPermission`
- Ensures the webhook subscriber has permission before delivery
- API input pipes (`WebhookInputPipe`, `PartialWebhookInputPipe`) validate webhook configuration

**Supported flow:**
```
Booking lifecycle event
  → BookingWebhookService schedules webhooks (subscriber lookup by userId/eventTypeId)
  → BookingWebhookDataFetcher.fetchEventData (booking UID → Prisma → CalendarEventBuilder)
  → PayloadBuilder constructs versioned payload (BookingTriggerEvents/MeetingTriggerEvents)
  → WebhookRepository permission check
  → Outgoing HTTP request to subscriber endpoint
```

**Unresolved:** The actual HTTP dispatch mechanism (how the outgoing request is sent), the `IWebhookProducerService` queue methods for booking CRUD events, and the subscriber matching algorithm within `getSubscribers` are all outside the clue's coverage.
