# Enterprise v2: ent-calcom-mech-1
Date: 2026-04-17

## Question
How does the cancellation-reason setting change booking cancellation behavior?

## Answer

### Overview

The cancellation-reason setting in Cal.diy controls whether and for whom a cancellation reason is required when cancelling a booking. This is governed by the `CancellationReasonRequirement` enum, dispatched through the `isCancellationReasonRequired` function, and propagated through the `CalendarEventBuilder`/`CalendarEventDirector` pipeline into calendar event descriptions and the booking details UI.

### The Cancellation Reason Requirement Setting

The central dispatch point is `isCancellationReasonRequired` (FOCUS, `packages/features/bookings/lib/cancellationReason.ts:2-21`). Its signature accepts a `setting: CancellationReasonRequirement | null | undefined` and its behavior annotation is `DISPATCH(requirement)`, meaning it switches on the requirement value. The function references four `CancellationReasonRequirement` enum variants:

1. **`MANDATORY_HOST_ONLY`** — Only the host must provide a cancellation reason (FOCUS, `isCancellationReasonRequired`, uses `CancellationReasonRequirement.MANDATORY_HOST_ONLY`)
2. **`OPTIONAL_BOTH`** — Both host and attendee may optionally provide a reason (FOCUS, uses `CancellationReasonRequirement.OPTIONAL_BOTH`)
3. **`MANDATORY_BOTH`** — Both host and attendee must provide a reason (FOCUS, uses `CancellationReasonRequirement.MANDATORY_BOTH`)
4. **`MANDATORY_ATTENDEE_ONLY`** — Only the attendee must provide a cancellation reason (FOCUS, uses `CancellationReasonRequirement.MANDATORY_ATTENDEE_ONLY`)

This dispatch pattern means the setting directly controls the validation behavior: depending on who is cancelling (host vs. attendee) and the configured requirement level, the system either enforces or skips reason collection.

### Cancellation Reason Processing

Once collected, the cancellation reason flows through several processing stages:

**`getCancellationReason`** (FOCUS, `packages/lib/CalEventParser.ts:611-619`) — This function takes a `TFunction` (for i18n translation) and an optional `cancellationReason` string. It processes the reason using `cancellationReason.startsWith`, `cancellationReason.substring`, and `cancellationReason.trim`, suggesting it parses a prefixed reason format (possibly extracting a reason code from a prefixed string). It is called by `getRichDescription` and `getRichDescriptionHTML` (FOCUS, `called_by: getRichDescription, getRichDescriptionHTML`), meaning the cancellation reason is embedded into the rich-text calendar event descriptions.

### Calendar Event Building Pipeline

The cancellation reason is set on calendar events through a builder/director pattern:

1. **`CalendarEventBuilder.setCancellationReason`** (FOCUS, `packages/lib/builders/CalendarEvent/builder.ts:245-247`) — Sets `this.calendarEvent.cancellationReason` from a `CalendarEventClass["cancellationReason"]` parameter. This is a direct setter on the calendar event model.

2. **`CalendarEventDirector.setCancellationReason`** (FOCUS, `packages/lib/builders/CalendarEvent/director.ts:35-37`) — Sets `this.cancellationReason` and is called by `buildWithoutEventTypeForRescheduleEmail` (FOCUS, `called_by: buildWithoutEventTypeForRescheduleEmail, CalendarEventDirector`). This indicates the cancellation reason is included in reschedule email construction, not just cancellation emails.

### API v2 Cancellation Input Transformation

At the API v2 layer, `InputBookingsService_2024_08_13.transformInputCancelBooking` (FOCUS, `apps/api/v2/src/platform/bookings/2024-08-13/services/input.service.ts:818-852`) transforms cancellation inputs. Its behavior annotation is `PRECEDENCE(isRecurringUid -> inputBooking)`, and it uses `inputBooking.cancellationReason` alongside `this.bookingsRepository.getRecurringByUid`, `recurringBooking.length`, and `inputBooking.cancelSubsequentBookings`. This shows that:
- For recurring bookings, the service first checks if the UID is a recurring series UID
- The cancellation reason from the input is carried through the transformation
- Subsequent bookings in a recurring series can also be cancelled

### UI Display of Cancellation Reasons

The booking details UI surfaces cancellation reasons in two components:

1. **`CancelledBookingInfo`** (FOCUS, `apps/web/modules/bookings/components/BookingDetailsSheet.tsx:945-984`) — Displays cancellation information with guard logic: `GUARD(!isCancelled || wasRescheduled -> return null)` and `PRECEDENCE(not_isCancelled -> not_cancellationReason)`. It checks `booking.status` against `BookingStatus.CANCELLED` and `BookingStatus.REJECTED`, and respects `booking.rescheduled`. This means the component only shows cancellation info for genuinely cancelled (not rescheduled) bookings.

2. **`NewRescheduledBookingInfo`** (FOCUS, `apps/web/modules/bookings/components/BookingDetailsSheet.tsx:908-944`) — Displays reschedule context with `GUARD(!booking.fromReschedule -> return null)`. It uses `booking.cancellationReason`, `booking.rejectionReason`, and `booking.rescheduler`, showing that cancellation reasons are also preserved and displayed when a booking is rescheduled (as the original booking's cancellation reason).

### Assignment Reason (Related but Distinct)

The clue also reveals a related but distinct concept — **assignment reasons**:

- `AssignmentReasonRepository.findByBookingId` (FOCUS, `packages/features/assignment-reason/repositories/AssignmentReasonRepository.ts:36-47`) — Finds assignment reasons by booking ID
- `AssignmentReasonRepository.findLatestByBookingId` (FOCUS, `packages/features/assignment-reason/repositories/AssignmentReasonRepository.ts:54-65`) — Finds the most recent assignment reason
- `PrismaAssignmentReasonRepository.findLatestReasonFromBookingUid` (FOCUS, `packages/app-store/salesforce/lib/repositories/PrismaAssignmentReasonRepository.ts:4-15`) — Salesforce-specific assignment reason lookup
- `AssignmentReasonSection` (FOCUS, `apps/web/modules/bookings/components/BookingDetailsSheet.tsx:720-746`) — UI component displaying assignment reasons with guard `GUARD(!booking.assignmentReasonSortedByCreatedAt...)`
- `assignmentReasonBadgeTitleMap` (FOCUS, `apps/web/lib/booking/assignmentReasonBadgeTitleMap.ts:2-15`) — Maps `AssignmentReasonEnum` values (`REASSIGNED`, `RR_REASSIGNED`, `REROUTED`, `SALESFORCE_ASSIGNMENT`) to display titles
- `V20211020BookingEventPayload` (FOCUS, `packages/features/webhooks/lib/factory/versioned/v2021-10-20/types.ts:12`) — Explicitly `Omit<EventPayloadType, "assignmentReason">`, showing the v2021-10-20 webhook version strips assignment reasons from payloads

### Reschedule Reason (Related)

A `RescheduleReason` type (FOCUS, `packages/features/bookings/lib/handleNewBooking/getBookingData.ts:99`) is derived from `AwaitedBookingData["rescheduleReason"]`. The `RescheduleReasonDefaultFieldInput_2024_06_14` (FOCUS, `packages/platform/types/event-types/event-types_2024_06_14/inputs/booking-fields.input.ts:287-329`) and `RescheduleReasonDefaultFieldOutput_2024_06_14` (FOCUS, extending `RescheduleReasonDefaultFieldInput_2024_06_14`, `packages/platform/types/event-types/event-types_2024_06_14/outputs/booking-fields.output.ts:150-202`) define the reschedule reason as a default booking field, paralleling the cancellation reason field.

### Booking Event Handling

`BookingEventHandlerService.onBookingCreatedOrRescheduled` (FOCUS, `packages/features/bookings/lib/onBookingEvents/BookingEventHandlerService.ts:44-56`) handles post-booking events (both creation and rescheduling) by accumulating side effects including `updatePrivateLinkUsage`, using `Promise.allSettled`.

`isPastBookingRescheduleBehaviourToPreventBooking` (FOCUS, `packages/features/bookings/lib/reschedule/determineReschedulePreventionRedirect.ts:47-63`) checks team-based configuration to prevent rescheduling of past bookings.

### Gaps and Uncertainties

The GAPS section identifies this as a MECHANISTIC question requiring body logic for a full answer, with 83 symbols at L3 and 69 with behavior annotations. The following are uncovered (GAPS):
- `BookingsRepository_2024_08_13.updateBooking` — The actual database update that persists the cancellation
- `BookingsService_2024_08_13.confirmBooking` — Confirmation flow
- `BookingsService_2024_08_13.declineBooking` — Decline/rejection flow
- `BookingsService_2024_08_13.getBookingBySeatUid` — Seat-based booking lookup

This means the exact database-level cancellation logic (how `isCancellationReasonRequired` gates the update and what happens when a mandatory reason is missing) cannot be fully traced from the clue alone. The validation enforcement mechanism (whether it throws an error, shows a UI warning, or blocks the API call) is not visible.

### Synthesis

The cancellation-reason setting changes booking cancellation behavior through a four-variant `CancellationReasonRequirement` enum dispatched by `isCancellationReasonRequired`: it can mandate reasons for hosts only, attendees only, both parties, or make them optional for both. When provided, the reason flows through `CalendarEventBuilder.setCancellationReason` → `CalendarEventDirector.setCancellationReason` → `getCancellationReason` (which parses prefix formatting) → `getRichDescription`/`getRichDescriptionHTML` for calendar event descriptions. The API v2 carries `inputBooking.cancellationReason` through `transformInputCancelBooking`, including for recurring booking series. The UI displays the reason in `CancelledBookingInfo` (for cancelled bookings) and `NewRescheduledBookingInfo` (for rescheduled bookings). The exact enforcement mechanism (how a missing mandatory reason is rejected) is in the uncovered `BookingsService_2024_08_13` methods.
