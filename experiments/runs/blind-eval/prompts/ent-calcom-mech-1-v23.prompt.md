# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-calcom-mech-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 calcom@HEAD 5074mod 11733sym
? How does the cancellation-reason setting change booking cancellation behavior?


-- README
> [!WARNING] > Use at your own risk. Cal.diy is the open source community edition of Cal.com and it is intended for users who want...
sections: About Cal.diy, What's different from Cal.com?, Built With, Getting Started, Prerequisites

-- TREE
__checks__/  (3 files)
apps/  (1635 files)
  api/  docs/  web/
example-apps/  (8 files)
  credential-sync/
packages/  (3420 files)
  app-store/  dayjs/  debugging/  emails/  embeds/  features/  i18n/  kysely/  lib/  prisma/  ...+4
scripts/  (9 files)
.env.example  README.md  checkly.config.ts  docker-compose.yml  i18n-unused.config.js  package.json  playwright.config.ts  setupVitest.ts  vitest.workspace.ts

-- INDEX
packages/embeds/embed-core/src/embed.ts        1709L  buildFilteredQueryParams, constructor, doInIframe, ensureGuestKey, filterParams
packages/lib/CalendarService.ts                1023L  constructor, createEvent, deleteEvent, getAccount, getAttendees
packages/trpc/server/routers/viewer/eventTypes/utils/EventTypeGroupFilter.ts   124L  byTeam, constructor, count, exists, get
packages/app-store/zoho-bigin/lib/CrmService.ts   336L  BiginContact, BiginContact, biginAuth, constructor, createBiginEvent
packages/features/booking-audit/lib/service/EnrichmentDataStore.ts   190L  DataRequirements, fetch, getAttendeeById, getCredentialById, getUserByUuid
packages/features/tasker/repository.ts          218L  cancel, cancelWithReference, cleanup, constructor, count
packages/features/webhooks/lib/repository/WebhookRepository.ts   592L  checkPermission, constructor, getTeamIdsWithPermission, hasPermission, PermissionCheckService
apps/api/v2/src/modules/atoms/services/event-types-atom.service.ts   435L  bulkUpdateEventTypesDefaultLocation, checkTeamOwnsEventType, getEventTypesAppIntegration, getTeamSlug, getUserEventType
apps/api/v2/src/platform/calendars/services/calendars-cache.service.ts    36L  constructor, deleteConnectedAndDestinationCalendarsCache, getConnectedAndDestinationCalendarsCache, CalendarsCacheService, REDIS_CALENDARS_CACHE_KEY
packages/app-store/ics-feedcalendar/lib/CalendarService.ts   318L  BuildCalendarService, constructor, createEvent, deleteEvent, getAvailability
packages/embeds/embed-core/src/sdk-action-manager.ts   362L  EmbedEvent, EmbedEvent, EventData, EventData, EventDataMap
  ...and 5063 more modules

-- SYM
Logger.logInternal                  M apps/api/v2/src/lib/logger.bridge.ts:142    method Logger.logInternal
TriggerDevLogger.logInternal        M packages/lib/triggerDevLogger.ts:76     method TriggerDevLogger.logInternal
OrganizationWatchlistOperationsService.checkPermission M packages/features/watchlist/lib/service/OrganizationWatchlistOperationsService.ts:48     async_method OrganizationWatchlistOperationsSer...
SelectedCalendarRepository.findMany M packages/features/selectedCalendar/repositories/SelectedCalendarRepository.ts:334    async_method SelectedCalendarRepository.findMany
PermissionCheckService.checkPermission M packages/features/watchlist/lib/service/OrganizationWatchlistOperationsService.ts:19     async_method PermissionCheckService.checkPermis...
InputLocationValidator_2024_06_14.validate M packages/platform/types/event-types/event-types_2024_06_14/inputs/locations.input.ts:160    async_method InputLocationValidator_2024_06_14....
InputTeamLocationValidator_2024_06_14.validate M packages/platform/types/event-types/event-types_2024_06_14/inputs/locations.input.ts:215    async_method InputTeamLocationValidator_2024_06...
hasPermission                       M packages/platform/enums/permissions.ts:15     function hasPermission
hasPermission                       M packages/platform/utils/permissions.ts:15     function hasPermission
TestTasker.constructor              M packages/lib/tasker/Tasker.test.ts:118    method TestTasker.constructor
TestTasker.constructor              M packages/lib/tasker/Tasker.test.ts:152    method TestTasker.constructor
TestTasker.constructor              M packages/lib/tasker/Tasker.test.ts:194    method TestTasker.constructor
TestTasker.constructor              M packages/lib/tasker/Tasker.test.ts:233    method TestTasker.constructor
TestTasker.constructor              M packages/lib/tasker/Tasker.test.ts:267    method TestTasker.constructor
TestTasker.constructor              M packages/lib/tasker/Tasker.test.ts:312    method TestTasker.constructor
TestTasker.constructor              M packages/lib/tasker/Tasker.test.ts:349    method TestTasker.constructor
TestTasker.constructor              M packages/lib/tasker/Tasker.test.ts:386    method TestTasker.constructor
TestTasker.constructor              M packages/lib/tasker/Tasker.test.ts:430    method TestTasker.constructor
TestTasker.constructor              M packages/lib/tasker/Tasker.test.ts:470    method TestTasker.constructor
TestTasker.constructor              M packages/lib/tasker/Tasker.test.ts:73     method TestTasker.constructor
TestRepository.findById             M packages/features/cache/decorators/__tests__/Memoize.test.ts:113    async_method TestRepository.findById
TestRepository.findById             M packages/features/cache/decorators/__tests__/Memoize.test.ts:136    async_method TestRepository.findById
TestRepository.findById             M packages/features/cache/decorators/__tests__/Memoize.test.ts:176    async_method TestRepository.findById
TestRepository.findById             M packages/features/cache/decorators/__tests__/Memoize.test.ts:192    async_method TestRepository.findById
TestRepository.findById             M packages/features/cache/decorators/__tests__/Memoize.test.ts:34     async_method TestRepository.findById
TestRepository.findById             M packages/features/cache/decorators/__tests__/Memoize.test.ts:53     async_method TestRepository.findById
TestRepository.findById             M packages/features/cache/decorators/__tests__/Memoize.test.ts:74     async_method TestRepository.findById
TestRepository.findById             M packages/features/cache/decorators/__tests__/Memoize.test.ts:90     async_method TestRepository.findById
TestRepository.delete               M packages/features/cache/decorators/__tests__/Unmemoize.test.ts:31     async_method TestRepository.delete
PartialWebhookInputPipe.transform   M apps/api/v2/src/modules/webhooks/pipes/WebhookInputPipe.ts:16     method PartialWebhookInputPipe.transform
TestRepository.delete               M packages/features/cache/decorators/__tests__/Unmemoize.test.ts:118    async_method TestRepository.delete
TestRepository.delete               M packages/features/cache/decorators/__tests__/Unmemoize.test.ts:135    async_method TestRepository.delete
TestRepository.delete               M packages/features/cache/decorators/__tests__/Unmemoize.test.ts:47     async_method TestRepository.delete
CalendarAppDelegationCredentialClientIdNotAuthorizedError.constructor M packages/lib/CalendarAppError.ts:30     method CalendarAppDelegationCredentialClientIdN...
CalendarAppDelegationCredentialConfigurationError.constructor M packages/lib/CalendarAppError.ts:16     method CalendarAppDelegationCredentialConfigura...
CalendarAppDelegationCredentialError.constructor M packages/lib/CalendarAppError.ts:9      method CalendarAppDelegationCredentialError.con...
CalendarAppDelegationCredentialInvalidGrantError.constructor M packages/lib/CalendarAppError.ts:23     method CalendarAppDelegationCredentialInvalidGr...
CalendarAppError.constructor        M packages/lib/CalendarAppError.ts:2      method CalendarAppError.constructor
UserError.constructor               M packages/trpc/server/routers/viewer/bookings/editLocation.handler.ts:197    method UserError.constructor
WebhookInputPipe.transform          M apps/api/v2/src/modules/webhooks/pipes/WebhookInputPipe.ts:6      method WebhookInputPipe.transform
CalendarAppDelegationCredentialNotSetupError.constructor M packages/lib/CalendarAppError.ts:37     method CalendarAppDelegationCredentialNotSetupE...
SystemError.constructor             M packages/trpc/server/routers/viewer/bookings/editLocation.handler.ts:207    method SystemError.constructor
TestRepository.update               M packages/features/cache/decorators/__tests__/Unmemoize.test.ts:102    async_method TestRepository.update
TestRepository.update               M packages/features/cache/decorators/__tests__/Unmemoize.test.ts:156    async_method TestRepository.update
TestRepository.update               M packages/features/cache/decorators/__tests__/Unmemoize.test.ts:171    async_method TestRepository.update
TestRepository.update               M packages/features/cache/decorators/__tests__/Unmemoize.test.ts:186    async_method TestRepository.update
TestRepository.update               M packages/features/cache/decorators/__tests__/Unmemoize.test.ts:66     async_method TestRepository.update
  ...and 11296 more symbols

-- FOCUS
.env.example (.env.example:1-484)
  Config summary for .env.example: entries: DATABASE_URL=postgresql://postgres:@localhost:5450..., DATABASE_DIRECT_URL=postgresql://postgres:@localhost:5450..., INSIGHTS_DATABASE_URL=<set>, NEXT_PUBLIC_WEBAPP_URL=http://localhost:3000, NEXT_PUBLIC_WEBSITE_URL=http://localhost:3000, NEXT_PUBLIC_EMBED_LIB_URL=http://localhost:3000/embed/embed.js
  entries: DATABASE_URL=postgresql://postgres:@localhost:5450..., DATABASE_DIRECT_URL=postgresql://postgres:@localhost:5450..., INSIGHTS_DATABASE_URL=<set>, NEXT_PUBLIC_WEBAPP_URL=http://localhost:3000, NEXT_PUBLIC_WEBSITE_URL=http://localhost:3000

apps/api/v2/.env.example (apps/api/v2/.env.example:1-76)
  Config summary for apps/api/v2/.env.example: entries: NODE_ENV=development, API_PORT=5555, API_URL=http://localhost, DATABASE_READ_URL=postgresql://postgres:@localhost:5450..., DATABASE_WRITE_URL=postgresql://postgres:@localhost:5450..., LOG_LEVEL=DEBUG
  entries: NODE_ENV=development, API_PORT=5555, API_URL=http://localhost, DATABASE_READ_URL=postgresql://postgres:@localhost:5450..., DATABASE_WRITE_URL=postgresql://postgres:@localhost:5450...

example-apps/credential-sync/.env.example (example-apps/credential-sync/.env.example:1-15)
  Config summary for example-apps/credential-sync/.env.example: entries: CALCOM_TEST_USER_ID=1, GOOGLE_REFRESH_TOKEN=<set>, GOOGLE_CLIENT_ID=<set>, GOOGLE_CLIENT_SECRET=<set>, ZOOM_REFRESH_TOKEN=<set>, ZOOM_CLIENT_ID=<set>
  entries: CALCOM_TEST_USER_ID=1, GOOGLE_REFRESH_TOKEN=<set>, GOOGLE_CLIENT_ID=<set>, GOOGLE_CLIENT_SECRET=<set>, ZOOM_REFRESH_TOKEN=<set>

AssignmentReasonRepository.findByBookingId (packages/features/assignment-reason/repositories/AssignmentReasonRepository.ts:36-47)
  async_method AssignmentReasonRepository.findByBookingId
  sig: AssignmentReasonRepository.findByBookingId(bookingId: number)
  behavior: DELEGATE(this.prismaClient.assignmentReason.findMany -> result)
  called_by: AssignmentReasonRepository
  uses: this.prismaClient.assignmentReason.findMany

AssignmentReasonRepository.findLatestByBookingId (packages/features/assignment-reason/repositories/AssignmentReasonRepository.ts:54-65)
  async_method AssignmentReasonRepository.findLatestByBookingId
  sig: AssignmentReasonRepository.findLatestByBookingId(bookingId: number)
  behavior: DELEGATE(this.prismaClient.assignmentReason.findFirst -> result)
  called_by: AssignmentReasonRepository
  uses: this.prismaClient.assignmentReason.findFirst

PrismaAssignmentReasonRepository.findLatestReasonFromBookingUid (packages/app-store/salesforce/lib/repositories/PrismaAssignmentReasonRepository.ts:4-15)
  async_method PrismaAssignmentReasonRepository.findLatestReasonFromBookingUid
  sig: PrismaAssignmentReasonRepository.findLatestReasonFromBookingUid(bookingUid: string)
  behavior: DELEGATE(prisma.assignmentReason.findFirst -> result)
  called_by: PrismaAssignmentReasonRepository
  uses: prisma.assignmentReason.findFirst

getCancellationReason (packages/lib/CalEventParser.ts:611-619)
  sig: getCancellationReason(t: TFunction, cancellationReason?: string | null)
  called_by: getRichDescription, getRichDescriptionHTML
  uses: cancellationReason.startsWith, cancellationReason.substring, cancellationReason.trim

CalendarEventBuilder.setCancellationReason (packages/lib/builders/CalendarEvent/builder.ts:245-247)
  method CalendarEventBuilder.setCancellationReason
  sig: CalendarEventBuilder.setCancellationReason(cancellationReason: CalendarEventClass["cancellationReason"])
  called_by: CalendarEventBuilder
  uses: this.calendarEvent.cancellationReason

CalendarEventDirector.setCancellationReason (packages/lib/builders/CalendarEvent/director.ts:35-37)
  method CalendarEventDirector.setCancellationReason
  sig: CalendarEventDirector.setCancellationReason(reason: string)
  called_by: buildWithoutEventTypeForRescheduleEmail, CalendarEventDirector
  uses: this.cancellationReason

isCancellationReasonRequired (packages/features/bookings/lib/cancellationReason.ts:2-21)
  sig: isCancellationReasonRequired(setting: CancellationReasonRequirement | null | undefined...)
  behavior: DISPATCH(requirement)
  uses: CancellationReasonRequirement.MANDATORY_HOST_ONLY, CancellationReasonRequirement.OPTIONAL_BOTH, CancellationReasonRequirement.MANDATORY_BOTH, CancellationReasonRequirement.MANDATORY_ATTENDEE_ONLY

RescheduleReason (packages/features/bookings/lib/handleNewBooking/getBookingData.ts:99-99)
  type alias RescheduleReason = AwaitedBookingData["rescheduleReason"]
  uses: AwaitedBookingData, rescheduleReason

V20211020BookingEventPayload (packages/features/webhooks/lib/factory/versioned/v2021-10-20/types.ts:12-12)
  type alias V20211020BookingEventPayload = Omit<EventPayloadType, "assignmentReason"> & {
  uses: Omit, EventPayloadType, assignmentReason

AssignmentReasonSection (apps/web/modules/bookings/components/BookingDetailsSheet.tsx:720-746)
  sig: AssignmentReasonSection({ booking }: { booking: BookingOutput })
  behavior: GUARD(!booking.assignmentReasonSortedByCreatedAt || booking.ass... -> return...); PRECEDENCE(not_booking -> not_reason)
  uses: booking.assignmentReasonSortedByCreatedAt, booking.assignmentReasonSortedByCreatedAt.length, reason.reasonString

CancelledBookingInfo (apps/web/modules/bookings/components/BookingDetailsSheet.tsx:945-984)
  sig: CancelledBookingInfo({ booking }: { booking: BookingOutput })
  behavior: GUARD(!isCancelled || wasRescheduled -> return null;); PRECEDENCE(not_isCancelled -> not_cancellationReason)
  uses: booking.status, BookingStatus.CANCELLED, BookingStatus.REJECTED, booking.rescheduled

assignmentReasonBadgeTitleMap (apps/web/lib/booking/assignmentReasonBadgeTitleMap.ts:2-15)
  sig: assignmentReasonBadgeTitleMap(assignmentReason: AssignmentReasonEnum)
  behavior: DISPATCH(assignmentReason)
  uses: AssignmentReasonEnum.REASSIGNED, AssignmentReasonEnum.RR_REASSIGNED, AssignmentReasonEnum.REROUTED, AssignmentReasonEnum.SALESFORCE_ASSIGNMENT

InputBookingsService_2024_08_13.transformInputCancelBooking (apps/api/v2/src/platform/bookings/2024-08-13/services/input.service.ts:818-852)
  async_method InputBookingsService_2024_08_13.transformInputCancelBooking
  sig: InputBookingsService_2024_08_13.transformInputCancelBooking(bookingUid: string, inputBooking: CancelBookingInput_2024...)
  behavior: PRECEDENCE(isRecurringUid -> inputBooking)
  called_by: InputBookingsService_2024_08_13
  uses: this.bookingsRepository.getRecurringByUid, recurringBooking.length, inputBooking.cancelSubsequentBookings, inputBooking.cancellationReason

NewRescheduledBookingInfo (apps/web/modules/bookings/components/BookingDetailsSheet.tsx:908-944)
  sig: NewRescheduledBookingInfo({ booking }: { booking: BookingOutput })
  behavior: GUARD(!booking.fromReschedule -> return null;)
  uses: booking.fromReschedule, booking.cancellationReason, booking.rejectionReason, booking.rescheduler

BookingEventHandlerService.onBookingCreatedOrRescheduled (packages/features/bookings/lib/onBookingEvents/BookingEventHandlerService.ts:44-56)
  async_method BookingEventHandlerService.onBookingCreatedOrRescheduled
  sig: BookingEventHandlerService.onBookingCreatedOrRescheduled(payload: BookingCreatedPayload | BookingRescheduledPayload)
  behavior: ACCUMULATE(onBookingCreatedOrRes... -> result)
  calls: updatePrivateLinkUsage
  called_by: onBookingCreated, onBookingRescheduled, BookingEventHandlerService
  uses: Promise.allSettled, this.updatePrivateLinkUsage, payload.bookingFormData.hashedLink, results.forEach

isPastBookingRescheduleBehaviourToPreventBooking (packages/features/bookings/lib/reschedule/determineReschedulePreventionRedirect.ts:47-63)
  sig: isPastBookingRescheduleBehaviourToPreventBooking(teamId: number | null | undefined)
  behavior: GUARD(!teamId -> return false;); PRECEDENCE(not_teamId -> not_ENV_PAST_BOOKING_RESCHED); TRANSFORM(map)
  called_by: determineReschedulePreventionRedirect
  uses: ENV_PAST_BOOKING_RESCHEDULE_CHANGE_TEAM_IDS.split, id.trim, configuredTeamIds.includes

RescheduleReasonDefaultFieldInput_2024_06_14 (packages/platform/types/event-types/event-types_2024_06_14/inputs/booking-fields.input.ts:287-329)
  uses: e.g, cal.com

RescheduleReasonDefaultFieldOutput_2024_06_14 (packages/platform/types/event-types/event-types_2024_06_14/outputs/booking-fields.output.ts:150-202)
  extends: RescheduleReasonDefaultFieldInput_2024_06_14

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 83 symbols in L3, 69 with behavior annotations
uncovered: BookingsRepository_2024_08_13.updateBooking, BookingsService_2024_08_13.confirmBooking, BookingsService_2024_08_13.declineBooking, BookingsService_2024_08_13.getBookingBySeatUid

--- CLUE FILE END ---

QUESTION: How does the cancellation-reason setting change booking cancellation behavior?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
