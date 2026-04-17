# Enterprise Eval: ent-calcom-mech-1
Date: 2026-04-17

## Question
How does the cancellation-reason setting change booking cancellation behavior?

## Reasoning Scaffold

### Relevant Symbols Identification

The clue's FOCUS section contains rich detail about cancellation reason handling across multiple layers: configuration/validation, event building, UI rendering, and API processing.

### 1. The Cancellation Reason Requirement Setting

**isCancellationReasonRequired** (`packages/features/bookings/lib/cancellationReason.ts:2-21`, FOCUS):
- Behavior: `DISPATCH(requirement)`
- Uses: `CancellationReasonRequirement.MANDATORY_HOST_ONLY`, `CancellationReasonRequirement.OPTIONAL_BOTH`, `CancellationReasonRequirement.MANDATORY_BOTH`, `CancellationReasonRequirement.MANDATORY_ATTENDEE_ONLY`
- Signature: `isCancellationReasonRequired(setting: CancellationReasonRequirement | null | undefined...)`

This is the **core dispatch function**. It takes a `CancellationReasonRequirement` setting and determines whether a cancellation reason is required. The `DISPATCH(requirement)` behavior annotation means it switches on the `requirement` parameter. The four enum values reveal the configuration options:

| Setting | Meaning (inferred from name) |
|---------|------------------------------|
| `MANDATORY_HOST_ONLY` | Only the host must provide a cancellation reason |
| `MANDATORY_ATTENDEE_ONLY` | Only the attendee must provide a cancellation reason |
| `MANDATORY_BOTH` | Both host and attendee must provide a reason |
| `OPTIONAL_BOTH` | Reason is optional for both parties |

The function also accepts `null | undefined`, implying a default/unset state.

### 2. Cancellation Reason in Calendar Event Construction

**CalendarEventBuilder.setCancellationReason** (`packages/lib/builders/CalendarEvent/builder.ts:245-247`, FOCUS):
- Signature: `setCancellationReason(cancellationReason: CalendarEventClass["cancellationReason"])`
- Uses: `this.calendarEvent.cancellationReason`
- Sets the cancellation reason on the calendar event being built.

**CalendarEventDirector.setCancellationReason** (`packages/lib/builders/CalendarEvent/director.ts:35-37`, FOCUS):
- Signature: `setCancellationReason(reason: string)`
- Called by: `buildWithoutEventTypeForRescheduleEmail`, `CalendarEventDirector`
- Uses: `this.cancellationReason`
- The director orchestrates the builder; notably it's called during reschedule email generation (`buildWithoutEventTypeForRescheduleEmail`), meaning the cancellation reason flows into reschedule notifications.

### 3. Cancellation Reason Parsing and Formatting

**getCancellationReason** (`packages/lib/CalEventParser.ts:611-619`, FOCUS):
- Signature: `getCancellationReason(t: TFunction, cancellationReason?: string | null)`
- Called by: `getRichDescription`, `getRichDescriptionHTML`
- Uses: `cancellationReason.startsWith`, `cancellationReason.substring`, `cancellationReason.trim`

This parser processes the raw cancellation reason string. The `startsWith`/`substring`/`trim` operations suggest it handles a **prefixed format** — likely extracting a structured reason from a string that may start with a category prefix. It feeds into rich description generation for calendar events (called by both plain-text `getRichDescription` and HTML `getRichDescriptionHTML`).

### 4. UI Layer — Cancel Booking Component

**handleSelectChange** (`apps/web/components/booking/CancelBooking.tsx:39-48`, FOCUS):
- Signature: `handleSelectChange(option: { value: number | string; label: string } | null)`
- This is a select/dropdown handler in the cancellation UI, suggesting users can choose from **predefined cancellation reasons** (with a value + label structure), not just free-text.

### 5. Cancelled Booking Display

**CancelledBookingInfo** (`apps/web/modules/bookings/components/BookingDetailsSheet.tsx:945-984`, FOCUS):
- Signature: `CancelledBookingInfo({ booking }: { booking: BookingOutput })`
- Behavior: `GUARD(!isCancelled || wasRescheduled -> return null;); PRECEDENCE(not_isCancelled -> not_cancellationReason)`
- Uses: `booking.status`, `BookingStatus.CANCELLED`, `BookingStatus.REJECTED`, `booking.rescheduled`

The guard conditions reveal the rendering logic:
1. If the booking is **not cancelled** OR **was rescheduled** → returns null (doesn't show cancellation info)
2. The PRECEDENCE chain: first checks cancellation status, then checks for a cancellation reason
3. The component uses both `CANCELLED` and `REJECTED` statuses, meaning rejections also display cancellation info.

**NewRescheduledBookingInfo** (`BookingDetailsSheet.tsx:908-944`, FOCUS):
- Behavior: `GUARD(!booking.fromReschedule -> return null;)`
- Uses: `booking.fromReschedule`, `booking.cancellationReason`, `booking.rejectionReason`, `booking.rescheduler`
- Shows that when a booking is rescheduled, it displays the cancellation reason from the original booking alongside the rescheduler's identity.

### 6. Assignment Reason (Related but Distinct)

**AssignmentReasonRepository.findByBookingId** (`packages/features/assignment-reason/repositories/AssignmentReasonRepository.ts:36-47`, FOCUS):
- Delegates to `prisma.assignmentReason.findMany`

**AssignmentReasonRepository.findLatestByBookingId** (`AssignmentReasonRepository.ts:54-65`, FOCUS):
- Delegates to `prisma.assignmentReason.findFirst`

**PrismaAssignmentReasonRepository.findLatestReasonFromBookingUid** (`packages/app-store/salesforce/lib/repositories/PrismaAssignmentReasonRepository.ts:4-15`, FOCUS):
- Used by Salesforce integration to get assignment reason by booking UID.

**assignmentReasonBadgeTitleMap** (`apps/web/lib/booking/assignmentReasonBadgeTitleMap.ts:2-15`, FOCUS):
- Dispatches on `AssignmentReasonEnum`: `REASSIGNED`, `RR_REASSIGNED`, `REROUTED`, `SALESFORCE_ASSIGNMENT`

**AssignmentReasonSection** (`BookingDetailsSheet.tsx:720-746`, FOCUS):
- Guards on `!booking.assignmentReasonSortedByCreatedAt` or empty array

**V20211020BookingEventPayload** (`packages/features/webhooks/lib/factory/versioned/v2021-10-20/types.ts:12`, FOCUS):
- Type alias: `Omit<EventPayloadType, "assignmentReason"> & { ... }`
- The v2021-10-20 webhook payload **omits** assignmentReason, indicating it's a newer field excluded from legacy payloads.

### 7. API Layer — Cancel Booking Input Transformation

**InputBookingsService_2024_08_13.transformInputCancelBooking** (`apps/api/v2/src/platform/bookings/2024-08-13/services/input.service.ts:818-852`, FOCUS):
- Behavior: `PRECEDENCE(isRecurringUid -> inputBooking)`
- Uses: `this.bookingsRepository.getRecurringByUid`, `recurringBooking.length`, `inputBooking.cancelSubsequentBookings`, `inputBooking.cancellationReason`
- This transforms the API v2 cancel-booking input. The `cancellationReason` is extracted from `inputBooking` and the method also handles:
  - **Recurring bookings**: checks `isRecurringUid` first (PRECEDENCE), then processes
  - **Subsequent booking cancellation**: `cancelSubsequentBookings` flag

### 8. Reschedule Reason (Parallel Pattern)

**RescheduleReason** (`packages/features/bookings/lib/handleNewBooking/getBookingData.ts:99`, FOCUS):
- Type alias: `AwaitedBookingData["rescheduleReason"]`

**RescheduleReasonDefaultFieldInput_2024_06_14** (`packages/platform/types/event-types/event-types_2024_06_14/inputs/booking-fields.input.ts:287-329`, FOCUS):
- Platform type for reschedule reason as a booking field.

**RescheduleReasonDefaultFieldOutput_2024_06_14** (`outputs/booking-fields.output.ts:150-202`, FOCUS):
- Extends `RescheduleReasonDefaultFieldInput_2024_06_14`

**fieldIsCustomSystemRescheduleReason** (`apps/api/v2/src/platform/event-types/event-types_2024_06_14/transformers/api-to-internal/booking-fields.ts:282-287`, FOCUS):
- Checks `field.slug` to identify system reschedule reason fields.

### 9. Booking Event Handling and Side Effects

**BookingEventHandlerService.onBookingCreatedOrRescheduled** (`packages/features/bookings/lib/onBookingEvents/BookingEventHandlerService.ts:44-56`, FOCUS):
- Behavior: `ACCUMULATE(onBookingCreatedOrRes... -> result)`
- Called by: `onBookingCreated`, `onBookingRescheduled`
- Uses: `Promise.allSettled`, `this.updatePrivateLinkUsage`, `payload.bookingFormData.hashedLink`

**BookingEmailSmsHandler.send** (`packages/features/bookings/lib/BookingEmailSmsHandler.ts:94-106`, FOCUS):
- Behavior: `GUARD(action === BookingActionMap.rescheduled -> if (data.eventType....))`
- Calls: `_handleConfirmed`, `_handleRequested`, `_handleRescheduled`, `_handleRoundRobinRescheduled`
- The reschedule guard suggests cancellation reason flows into email/SMS notifications differently for rescheduled vs. cancelled bookings.

**ManagedEventCancellationResult** (`BookingRepository.ts:70-71`, FOCUS):
- Type alias for managed event cancellation results.

### 10. Reschedule Prevention

**isPastBookingRescheduleBehaviourToPreventBooking** (`packages/features/bookings/lib/reschedule/determineReschedulePreventionRedirect.ts:47-63`, FOCUS):
- Behavior: `GUARD(!teamId -> return false;); PRECEDENCE(not_teamId -> not_ENV_PAST_BOOKING_RESCHED); TRANSFORM(map)`
- Uses: `ENV_PAST_BOOKING_RESCHEDULE_CHANGE_TEAM_IDS.split`, `configuredTeamIds.includes`
- Environment-variable-driven reschedule prevention for specific teams.

### GAPS — What Cannot Be Determined

The GAPS section states:
- **Type**: MECHANISTIC (body logic needed for full answer)
- **Coverage**: 80 symbols in L3, 69 with behavior annotations
- **Uncovered symbols**:
  - `BookingsRepository_2024_08_13.updateBooking` — how the booking record is actually updated during cancellation
  - `BookingsService_2024_08_13.confirmBooking` — confirmation flow
  - `BookingsService_2024_08_13.declineBooking` — decline/rejection flow
  - `BookingsService_2024_08_13.getBookingBySeatUid` — seat-based booking retrieval

These mean:
1. The **actual database update** that records the cancellation reason on the booking is not visible.
2. How `isCancellationReasonRequired` is **enforced** (validation error thrown? UI-only? API guard?) cannot be fully determined.
3. The **decline/rejection path** and whether it uses the same cancellation reason mechanism is unknown.
4. Seat-based booking cancellation behavior is not covered.

### Synthesis

The cancellation-reason setting changes booking cancellation behavior through a **multi-layer dispatch system**:

**Configuration Layer:**
The `CancellationReasonRequirement` enum defines four modes: `MANDATORY_HOST_ONLY`, `MANDATORY_ATTENDEE_ONLY`, `MANDATORY_BOTH`, and `OPTIONAL_BOTH` (`isCancellationReasonRequired`, `cancellationReason.ts:2-21`). The `isCancellationReasonRequired` function dispatches on this setting to determine whether a reason is required for the current actor (host vs. attendee).

**UI Layer:**
- A dropdown selector (`handleSelectChange` in `CancelBooking.tsx:39-48`) presents predefined reason options with `{ value, label }` structure.
- `CancelledBookingInfo` (`BookingDetailsSheet.tsx:945-984`) conditionally displays cancellation info — only for bookings with status `CANCELLED` or `REJECTED` that were not rescheduled.
- `NewRescheduledBookingInfo` (`BookingDetailsSheet.tsx:908-944`) shows the original cancellation reason alongside rescheduler identity for rescheduled bookings.

**API Layer:**
`InputBookingsService_2024_08_13.transformInputCancelBooking` (`input.service.ts:818-852`) extracts `cancellationReason` from the cancel booking input, handling recurring bookings with precedence and supporting `cancelSubsequentBookings`.

**Event Building Layer:**
- `CalendarEventBuilder.setCancellationReason` (`builder.ts:245-247`) stores the reason on the calendar event.
- `CalendarEventDirector.setCancellationReason` (`director.ts:35-37`) is called during reschedule email building.
- `getCancellationReason` (`CalEventParser.ts:611-619`) parses the reason string (handling prefixes via `startsWith`/`substring`/`trim`) for inclusion in rich calendar descriptions.

**Display/Notification Layer:**
The parsed cancellation reason flows into `getRichDescription` and `getRichDescriptionHTML` for calendar event descriptions, and is available in the booking details sheet UI.

**What the setting changes:** When set to `MANDATORY_*`, the cancellation reason becomes required for the specified party. When `OPTIONAL_BOTH`, it is collected but not enforced. The exact enforcement mechanism (API validation error vs. UI-only gate) is in the GAPS and cannot be determined from the clue alone.
