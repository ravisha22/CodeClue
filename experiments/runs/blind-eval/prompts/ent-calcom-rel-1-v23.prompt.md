# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: ent-calcom-rel-1

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.

--- CLUE FILE (File 1) ---
=CC v2.1 calcom@HEAD 5074mod 11723sym
? How does the headless router flow from a submitted form to a booked meeting?


-- TREE
__checks__/  (3 files)
apps/  (1632 files)
  api/  docs/  web/
example-apps/  (7 files)
  credential-sync/
packages/  (3418 files)
  app-store/  dayjs/  debugging/  emails/  embeds/  features/  i18n/  kysely/  lib/  prisma/  ...+4
scripts/  (9 files)
checkly.config.ts  i18n-unused.config.js  playwright.config.ts  setupVitest.ts  vitest.workspace.ts

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
SystemError.constructor             M packages/trpc/server/routers/viewer/bookings/editLocation.handler.ts:207    method SystemError.constructor
TestRepository.delete               M packages/features/cache/decorators/__tests__/Unmemoize.test.ts:118    async_method TestRepository.delete
TestRepository.delete               M packages/features/cache/decorators/__tests__/Unmemoize.test.ts:135    async_method TestRepository.delete
TestRepository.delete               M packages/features/cache/decorators/__tests__/Unmemoize.test.ts:31     async_method TestRepository.delete
TestRepository.delete               M packages/features/cache/decorators/__tests__/Unmemoize.test.ts:47     async_method TestRepository.delete
TestRepository.update               M packages/features/cache/decorators/__tests__/Unmemoize.test.ts:156    async_method TestRepository.update
TestRepository.update               M packages/features/cache/decorators/__tests__/Unmemoize.test.ts:186    async_method TestRepository.update
TestRepository.update               M packages/features/cache/decorators/__tests__/Unmemoize.test.ts:66     async_method TestRepository.update
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
UserError.constructor               M packages/trpc/server/routers/viewer/bookings/editLocation.handler.ts:197    method UserError.constructor
PartialWebhookInputPipe.transform   M apps/api/v2/src/modules/webhooks/pipes/WebhookInputPipe.ts:16     method PartialWebhookInputPipe.transform
WebhookInputPipe.transform          M apps/api/v2/src/modules/webhooks/pipes/WebhookInputPipe.ts:6      method WebhookInputPipe.transform
TestRepository.update               M packages/features/cache/decorators/__tests__/Unmemoize.test.ts:102    async_method TestRepository.update
TestRepository.update               M packages/features/cache/decorators/__tests__/Unmemoize.test.ts:171    async_method TestRepository.update
CalendarAppDelegationCredentialClientIdNotAuthorizedError.constructor M packages/lib/CalendarAppError.ts:30     method CalendarAppDelegationCredentialClientIdN...
CalendarAppDelegationCredentialConfigurationError.constructor M packages/lib/CalendarAppError.ts:16     method CalendarAppDelegationCredentialConfigura...
CalendarAppDelegationCredentialInvalidGrantError.constructor M packages/lib/CalendarAppError.ts:23     method CalendarAppDelegationCredentialInvalidGr...
CalendarAppError.constructor        M packages/lib/CalendarAppError.ts:2      method CalendarAppError.constructor
CalendarAppDelegationCredentialError.constructor M packages/lib/CalendarAppError.ts:9      method CalendarAppDelegationCredentialError.con...
CalendarAppDelegationCredentialNotSetupError.constructor M packages/lib/CalendarAppError.ts:37     method CalendarAppDelegationCredentialNotSetupE...
TestRepository.findById             M packages/features/cache/decorators/__tests__/Memoize.test.ts:113    async_method TestRepository.findById
TestRepository.findById             M packages/features/cache/decorators/__tests__/Memoize.test.ts:192    async_method TestRepository.findById
TestRepository.findById             M packages/features/cache/decorators/__tests__/Memoize.test.ts:34     async_method TestRepository.findById
TestRepository.findById             M packages/features/cache/decorators/__tests__/Memoize.test.ts:53     async_method TestRepository.findById
TestRepository.findById             M packages/features/cache/decorators/__tests__/Memoize.test.ts:74     async_method TestRepository.findById
TestRepository.findById             M packages/features/cache/decorators/__tests__/Memoize.test.ts:90     async_method TestRepository.findById
TestRepository.findById             M packages/features/cache/decorators/__tests__/Memoize.test.ts:136    async_method TestRepository.findById
TestRepository.findById             M packages/features/cache/decorators/__tests__/Memoize.test.ts:176    async_method TestRepository.findById
Office365CalendarService.triggerDelegationCredentialError M packages/app-store/office365calendar/lib/CalendarService.ts:126    async_method Office365CalendarService.triggerDe...
BookingAuditAccessService.constructor M packages/features/booking-audit/lib/service/BookingAuditAccessService.ts:33     method BookingAuditAccessService.constructor
BookingAuditPermissionError.constructor M packages/features/booking-audit/lib/service/BookingAuditAccessService.ts:13     method BookingAuditPermissionError.constructor
DefaultLayoutEnabledValidator.validate M packages/platform/types/event-types/event-types_2024_06_14/inputs/booker-layouts.input.ts:49     method DefaultLayoutEnabledValidator.validate
LayoutValidator.validate            M packages/platform/types/event-types/event-types_2024_06_14/inputs/booker-layouts.input.ts:17     method LayoutValidator.validate
DefaultLayoutEnabledValidator.defaultMessage M packages/platform/types/event-types/event-types_2024_06_14/inputs/booker-layouts.input.ts:58     method DefaultLayoutEnabledValidator.defaultMes...
  ...and 11280 more symbols

-- FOCUS
FormSubmittedDTO (packages/features/webhooks/lib/dto/types.ts:175-186)
  interface FormSubmittedDTO
  extends: BaseEventDTO
  uses: WebhookTriggerEvents.FORM_SUBMITTED

FormSubmittedNoEventDTO (packages/features/webhooks/lib/dto/types.ts:205-216)
  interface FormSubmittedNoEventDTO
  extends: BaseEventDTO
  uses: WebhookTriggerEvents.FORM_SUBMITTED_NO_EVENT

WebhookTaskerProducerService.queueFormSubmittedWebhook (packages/features/webhooks/lib/service/WebhookTaskerProducerService.ts:76-97)
  async_method WebhookTaskerProducerService.queueFormSubmittedWebhook
  sig: WebhookTaskerProducerService.queueFormSubmittedWebhook(params: QueueFormWebhookParams)
  calls: queueTask
  called_by: WebhookTaskerProducerService
  uses: params.operationId, this.log.debug, WebhookTriggerEvents.FORM_SUBMITTED, params.formId

FormSubmittedPayload (packages/features/webhooks/lib/factory/types.ts:6-13)
  interface FormSubmittedPayload

IWebhookProducerService.queueFormSubmittedWebhook (packages/features/webhooks/lib/interface/WebhookProducerService.ts:164-164)
  method IWebhookProducerService.queueFormSubmittedWebhook
  sig: IWebhookProducerService.queueFormSubmittedWebhook(params: QueueFormWebhookParams)
  called_by: IWebhookProducerService

BookingWebhookService.scheduleMeetingWebhooks (packages/features/webhooks/lib/service/BookingWebhookService.ts:239-328)
  async_method BookingWebhookService.scheduleMeetingWebhooks
  sig: BookingWebhookService.scheduleMeetingWebhooks(params: ScheduleMeetingWebhooksParams)
  behavior: ACCUMULATE(scheduleMeetingWebhoo... -> result)
  called_by: BookingWebhookService
  uses: this.webhookService, webhookService.getSubscribers, params.booking.userId, params.booking.eventTypeId

useRouterHelpers (apps/web/modules/embed/components/Embed.tsx:105-133)
  behavior: ACCUMULATE(useRouterHelpers loop -> result)
  called_by: useEmbedGoto
  uses: searchParams.toString, newQuery.delete, Object.keys, newQuery.set

BookingVideoService_2024_08_13.deleteOldVideoMeetingIfNeeded (apps/api/v2/src/platform/bookings/2024-08-13/services/booking-video.service.ts:13-40)
  async_method BookingVideoService_2024_08_13.deleteOldVideoMeetingIfNeeded
  sig: BookingVideoService_2024_08_13.deleteOldVideoMeetingIfNeeded(bookingId: number)
  behavior: GUARD(!booking || !booking.user -> return;); ACCUMULATE(deleteOldVideoMeeting... -> result)
  called_by: BookingVideoService_2024_08_13
  uses: this.bookingsRepository.getBookingByIdWithUserAndEventDetails, booking.user, booking.references.filter, ref.type.endsWith

buildFormStateWithNoErrors (packages/features/form-builder/useShouldBeDisabledDueToPrefill.test.ts:60-63)
  sig: buildFormStateWithNoErrors(formState?: FormState)
  behavior: DELEGATE(buildFormState -> result)
  calls: buildFormState

SeatBookedAuditActionService (packages/features/booking-audit/lib/actions/SeatBookedAuditActionService.ts:27-91)
  methods: constructor, getDataRequirements, getDisplayJson, getDisplayTitle, getVersion, getVersionedData
  calls: constructor, getDataRequirements, getDisplayJson, getDisplayTitle, getVersion, getVersionedData, migrateToLatest, parseStored
  uses: z.object, z.literal, SeatBookedAuditActionService.dataSchemaV1, SeatBookedAuditActionService.fieldsSchemaV1

getUpdatedFormValues (apps/web/modules/settings/my-account/profile-view.tsx:552-590)
  sig: getUpdatedFormValues(values: FormValues)
  behavior: TRANSFORM(map)
  called_by: handleFormSubmit, onDisconnect
  uses: formMethods.formState.dirtyFields, updatedValues.secondaryEmails.findIndex, secondaryEmail.emailPrimary, updatedValues.email

InstantMeetingDTO (packages/features/webhooks/lib/dto/types.ts:303-313)
  interface InstantMeetingDTO
  extends: BaseEventDTO
  uses: WebhookTriggerEvents.INSTANT_MEETING

MeetingEndedDTO (packages/features/webhooks/lib/dto/types.ts:260-302)
  interface MeetingEndedDTO
  extends: BaseEventDTO
  uses: WebhookTriggerEvents.MEETING_ENDED

MeetingPayloadBuilder (packages/features/webhooks/lib/factory/versioned/v2021-10-20/MeetingPayloadBuilder.ts:19-50)
  extends: BaseMeetingPayloadBuilder
  uses: dto.triggerEvent, WebhookTriggerEvents.AFTER_HOSTS_CAL_VIDEO_NO_SHOW, WebhookTriggerEvents.AFTER_GUESTS_CAL_VIDEO_NO_SHOW, dto.createdAt

MeetingStartedDTO (packages/features/webhooks/lib/dto/types.ts:217-259)
  interface MeetingStartedDTO
  extends: BaseEventDTO
  uses: WebhookTriggerEvents.MEETING_STARTED

BookingWebhookService.cancelScheduledMeetingWebhooks (packages/features/webhooks/lib/service/BookingWebhookService.ts:330-337)
  async_method BookingWebhookService.cancelScheduledMeetingWebhooks
  sig: BookingWebhookService.cancelScheduledMeetingWebhooks(params: CancelScheduledMeetingWebhooksParams)
  called_by: BookingWebhookService
  uses: this.webhookService, webhookService.cancelScheduledWebhooks, params.bookingId, WebhookTriggerEvents.MEETING_STARTED

EventTypeAppSettingsForm (apps/web/components/apps/installation/ConfigureStepCard.tsx:66-121)
  sig: EventTypeAppSettingsForm(props, ref)
  uses: eventType.id, z.object, formMethods.getValues, eventType.title

Form (packages/coss-ui/src/components/form.tsx:6-15)
  sig: Form({ className, ...props }: FormPrimitive.Props)
  uses: FormPrimitive.Props

Meeting (packages/lib/OgImages.tsx:181-258)
  sig: Meeting({ title, users = [], profile }: MeetingImageProps)
  behavior: TRANSFORM(map)
  calls: joinMultipleNames
  uses: OG_ASSETS.meeting, profile.image, self.findIndex, v.name

PlainForm (packages/ui/components/address/fields.tsx:202-244)
  sig: PlainForm(props: FormProps<T>, ref: Ref<HTMLFormElement>)
  behavior: TRANSFORM(map)
  uses: event.preventDefault, event.stopPropagation, form.com, React.Children.map

SeatBookedAuditActionService.constructor (packages/features/booking-audit/lib/actions/SeatBookedAuditActionService.ts:46-52)
  method SeatBookedAuditActionService.constructor
  called_by: SeatBookedAuditActionService
  uses: this.helper, this.VERSION, SeatBookedAuditActionService.latestFieldsSchema, SeatBookedAuditActionService.storedDataSchema

SeatBookedAuditActionService.getDisplayTitle (packages/features/booking-audit/lib/actions/SeatBookedAuditActionService.ts:76-78)
  async_method SeatBookedAuditActionService.getDisplayTitle
  sig: SeatBookedAuditActionService.getDisplayTitle(_: GetDisplayTitleParams)
  called_by: SeatBookedAuditActionService
  uses: booking_audit_action.seat_booked

deleteMeeting (packages/features/conferencing/lib/videoClient.ts:146-164)
  sig: deleteMeeting(credential: CredentialPayload | CredentialForCalendarServ...)
  behavior: GUARD(videoAdapter -> return videoAdapter...); PRECEDENCE(credential -> videoAdapter)
  uses: log.debug, e.g, videoAdapter.deleteMeeting, Promise.resolve

getMeetingInformationHandler (packages/trpc/server/routers/viewer/calVideo/getMeetingInformation.handler.ts:14-43)
  sig: getMeetingInformationHandler({ ctx: _ctx, input }: GetMeetingInformationOptions)
  uses: VideoApiAdapterMap.dailyvideo, dailyVideoAdapterModule.default, videoApiAdapter.getMeetingInformation

onRouterTransitionStart (apps/web/instrumentation-client.ts:46-51)
  sig: onRouterTransitionStart(url: string, navigationType: "push" | "replace" | "traverse")
  uses: process.env.NODE_ENV, Sentry.captureRouterTransitionStart

parseMultiFormData (apps/web/app/api/parseRequestData.ts:19-28)
  sig: parseMultiFormData(req: NextRequest)
  behavior: DELEGATE(Object.fromEntries -> result)
  called_by: parseRequestData
  uses: req.formData, Object.fromEntries, formData.entries, log.error

resetForm (apps/web/components/settings/DisableTwoFactorModal.tsx:45-51)
  sig: resetForm(clearPassword = true)
  called_by: handleDisable
  uses: form.setValue

useCreateEventTypeForm (packages/platform/atoms/hooks/event-types/private/useCreateEventTypeForm.ts:11-32)
  uses: form.watch, SchedulingType.MANAGED, form.setValue, metadata.managedEventConfig.unlockedFields

useRouterQuery (apps/web/lib/hooks/useRouterQuery.ts:5-28)
  sig: useRouterQuery(name: T)
  uses: _searchParams.delete, _searchParams.set, router.replace, _searchParams.toString

AppRouter (packages/trpc/server/routers/_app.ts:16-16)
  type alias AppRouter = typeof appRouter
  uses: appRouter

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 11 with behavior annotations
uncovered: IUseBookingForm, InstantMeetingBuilder, InstantMeetingPayload, JoinMeetingButtonProps
drill: packages/features/webhooks/lib/service/WebhookTaskerProducerService.ts (~17 lines, WebhookTaskerProducerService.queueFormSubmittedWebhook)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## WebhookTaskerProducerService.queueFormSubmittedWebhook  (packages/features/webhooks/lib/service/WebhookTaskerProducerService.ts L76-97)
```
  async queueFormSubmittedWebhook(params: QueueFormWebhookParams): Promise<void> {
    const operationId = params.operationId || uuidv4();

    this.log.debug("Queueing form webhook task", {
      operationId,
      triggerEvent: WebhookTriggerEvents.FORM_SUBMITTED,
      formId: params.formId,
    });

    const taskPayload: WebhookTaskPayload = {
      operationId,
      triggerEvent: WebhookTriggerEvents.FORM_SUBMITTED,
      formId: params.formId,
      teamId: params.teamId,
      userId: params.userId,
      oAuthClientId: params.oAuthClientId,
      metadata: params.metadata,
      timestamp: new Date().toISOString(),
    };

    await this.queueTask(operationId, taskPayload);
  }
```

## IWebhookTaskerProducerServiceDeps  (packages/features/webhooks/lib/service/WebhookTaskerProducerService.ts L27-30)
```
export interface IWebhookTaskerProducerServiceDeps {
  webhookTasker: WebhookTasker;
  logger: ILogger;
}
```

## WebhookTaskerProducerService.constructor  (packages/features/webhooks/lib/service/WebhookTaskerProducerService.ts L35-37)
```
  constructor(private readonly deps: IWebhookTaskerProducerServiceDeps) {
    this.log = deps.logger.getSubLogger({ prefix: ["[WebhookTaskerProducerService]"] });
  }
```

## WebhookTaskerProducerService.queueBookingCancelledWebhook  (packages/features/webhooks/lib/service/WebhookTaskerProducerService.ts L43-45)
```
  async queueBookingCancelledWebhook(params: QueueBookingWebhookParams): Promise<void> {
    await this.queueBookingWebhook(WebhookTriggerEvents.BOOKING_CANCELLED, params);
  }
```

## WebhookTaskerProducerService.queueBookingCreatedWebhook  (packages/features/webhooks/lib/service/WebhookTaskerProducerService.ts L39-41)
```
  async queueBookingCreatedWebhook(params: QueueBookingWebhookParams): Promise<void> {
    await this.queueBookingWebhook(WebhookTriggerEvents.BOOKING_CREATED, params);
  }
```

## WebhookTaskerProducerService.queueBookingNoShowUpdatedWebhook  (packages/features/webhooks/lib/service/WebhookTaskerProducerService.ts L72-74)
```
  async queueBookingNoShowUpdatedWebhook(params: QueueBookingWebhookParams): Promise<void> {
    await this.queueBookingWebhook(WebhookTriggerEvents.BOOKING_NO_SHOW_UPDATED, params);
  }
```

## WebhookTaskerProducerService.queueBookingPaidWebhook  (packages/features/webhooks/lib/service/WebhookTaskerProducerService.ts L68-70)
```
  async queueBookingPaidWebhook(params: QueuePaymentWebhookParams): Promise<void> {
    await this.queuePaymentWebhook(WebhookTriggerEvents.BOOKING_PAID, params);
  }
```

## WebhookTaskerProducerService.queueBookingPaymentInitiatedWebhook  (packages/features/webhooks/lib/service/WebhookTaskerProducerService.ts L64-66)
```
  async queueBookingPaymentInitiatedWebhook(params: QueuePaymentWebhookParams): Promise<void> {
    await this.queuePaymentWebhook(WebhookTriggerEvents.BOOKING_PAYMENT_INITIATED, params);
  }
```

## WebhookTaskerProducerService.queueBookingRejectedWebhook  (packages/features/webhooks/lib/service/WebhookTaskerProducerService.ts L60-62)
```
  async queueBookingRejectedWebhook(params: QueueBookingWebhookParams): Promise<void> {
    await this.queueBookingWebhook(WebhookTriggerEvents.BOOKING_REJECTED, params);
  }
```

## WebhookTaskerProducerService.queueBookingRequestedWebhook  (packages/features/webhooks/lib/service/WebhookTaskerProducerService.ts L56-58)
```
  async queueBookingRequestedWebhook(params: QueueBookingWebhookParams): Promise<void> {
    await this.queueBookingWebhook(WebhookTriggerEvents.BOOKING_REQUESTED, params);
  }
```

## WebhookTaskerProducerService.queueBookingRescheduledWebhook  (packages/features/webhooks/lib/service/WebhookTaskerProducerService.ts L47-49)
```
  async queueBookingRescheduledWebhook(params: QueueBookingWebhookParams): Promise<void> {
    await this.queueBookingWebhook(WebhookTriggerEvents.BOOKING_RESCHEDULED, params);
  }
```

## WebhookTaskerProducerService.queueOOOCreatedWebhook  (packages/features/webhooks/lib/service/WebhookTaskerProducerService.ts L125-147)
```
  async queueOOOCreatedWebhook(params: QueueOOOWebhookParams): Promise<void> {
    const operationId = params.operationId || uuidv4();

    this.log.debug("Queueing OOO webhook task", {
      operationId,
      triggerEvent: WebhookTriggerEvents.OOO_CREATED,
      oooEntryId: params.oooEntryId,
      userId: params.userId,
    });

    const taskPayload: WebhookTaskPayload = {
      operationId,
      triggerEvent: WebhookTriggerEvents.OOO_CREATED,
      oooEntryId: params.oooEntryId,
      userId: params.userId,
      teamId: params.teamId,
      oAuthClientId: params.oAuthClientId,
      metadata: params.metadata,
      timestamp: new Date().toISOString(),
    };

    await this.queueTask(operationId, taskPayload);
  }
```

## WebhookTaskerProducerService.queueRecordingReadyWebhook  (packages/features/webhooks/lib/service/WebhookTaskerProducerService.ts L99-123)
```
  async queueRecordingReadyWebhook(params: QueueRecordingWebhookParams): Promise<void> {
    const operationId = params.operationId || uuidv4();

    this.log.debug("Queueing recording webhook task", {
      operationId,
      triggerEvent: WebhookTriggerEvents.RECORDING_READY,
      recordingId: params.recordingId,
      bookingUid: params.bookingUid,
    });

    const taskPayload: WebhookTaskPayload = {
      operationId,
      triggerEvent: WebhookTriggerEvents.RECORDING_READY,
      recordingId: params.recordingId,
      bookingUid: params.bookingUid,
      eventTypeId: params.eventTypeId,
      teamId: params.teamId,
      userId: params.userId,
      oAuthClientId: params.oAuthClientId,
      metadata: params.metadata,
      timestamp: new Date().toISOString(),
    };

    await this.queueTask(operationId, taskPayload);
  }
```

## WebhookTaskerProducerService.queueTask  (packages/features/webhooks/lib/service/WebhookTaskerProducerService.ts L222-233)
```
  private async queueTask(operationId: string, taskPayload: WebhookTaskPayload): Promise<void> {
    try {
      const result = await this.deps.webhookTasker.deliverWebhook(taskPayload);
      this.log.debug("Webhook delivery task queued", { operationId, taskId: result.taskId });
    } catch (error) {
      this.log.error("Failed to queue webhook delivery task", {
        operationId,
        error: error instanceof Error ? error.message : String(error),
      });
      throw error;
    }
  }
```

## WebhookTaskerProducerService  (packages/features/webhooks/lib/service/WebhookTaskerProducerService.ts L31-234)
```

export class WebhookTaskerProducerService implements IWebhookProducerService {
  private readonly log: ILogger;

  constructor(private readonly deps: IWebhookTaskerProducerServiceDeps) {
    this.log = deps.logger.getSubLogger({ prefix: ["[WebhookTaskerProducerService]"] });
  }

  async queueBookingCreatedWebhook(params: QueueBookingWebhookParams): Promise<void> {
    await this.queueBookingWebhook(WebhookTriggerEvents.BOOKING_CREATED, params);
  }

  async queueBookingCancelledWebhook(params: QueueBookingWebhookParams): Promise<void> {
    await this.queueBookingWebhook(WebhookTriggerEvents.BOOKING_CANCELLED, params);
  }

  async queueBookingRescheduledWebhook(params: QueueBookingWebhookParams): Promise<void> {
    await this.queueBookingWebhook(WebhookTriggerEvents.BOOKING_RESCHEDULED, params);
  }

  /**
   * Queue a webhook for requested bookings.
   *
   * This fires when bookings require confirmation (status = PENDING).
   */
  async queueBookingRequestedWebhook(params: QueueBookingWebhookParams): Promise<void> {
    await this.queueBookingWebhook(WebhookTriggerEvents.BOOKING_REQUESTED, params);
  }

  async queueBookingRejectedWebhook(params: QueueBookingWebhookParams): Promise<void> {
    await this.queueBookingWebhook(WebhookTriggerEvents.BOOKING_REJECTED, params);
  }

  async queueBookingPaymentInitiatedWebhook(params: QueuePaymentWebhookParams): Promise<void> {
    await this.queuePaymentWebhook(WebhookTriggerEvents.BOOKING_PAYMENT_INITIATED, params);
  }

  async queueBookingPaidWebhook(params: QueuePaymentWebhookParams): Promise<void> {
    await this.queuePaymentWebhook(WebhookTriggerEvents.BOOKING_PAID, params);
  }

  async queueBookingNoShowUpdatedWebhook(params: QueueBookingWebhookParams): Promise<void> {
    await this.queueBookingWebhook(WebhookTriggerEvents.BOOKING_NO_SHOW_UPDATED, params);
  }

  async queueFormSubmittedWebhook(params: QueueFormWebhookParams): Promise<void> {
    const operationId = params.operationId || uuidv4();

    this.log.debug("Queueing form webhook task", {
      operationId,
      triggerEvent: WebhookTriggerEvents.FORM_SUBMITTED,
      formId: params.formId,
    });

    const taskPayload: WebhookTaskPayload = {
      operationId,
      triggerEvent: WebhookTriggerEvents.FORM_SUBMITTED,
      formId: params.formId,
      teamId: params.teamId,
      userId: params.userId,
      oAuthClientId: params.oAuthClientId,
      metadata: params.metadata,
      timestamp: new Date().toISOString(),
    };

    await this.queueTask(operationId, taskPayload);
  }

  async queueRecordingReadyWebhook(params: QueueRecordingWebhookParams): Promise<void> {
    const operationId = params.operationId || uuidv4();

    this.log.debug("Queueing recording webhook task", {
      operationId,
      triggerEvent: WebhookTriggerEvents.RECORDING_READY,
      recordingId: params.recordingId,
      bookingUid: params.bookingUid,
    });

    const taskPayload: WebhookTaskPayload = {
      operationId,
      triggerEvent: WebhookTriggerEvents.RECORDING_READY,
      recordingId: params.recordingId,
      bookingUid: params.bookingUid,
      eventTypeId: params.eventTypeId,
      teamId: params.teamId,
      userId: params.userId,
      oAuthClientId: params.oAuthClientId,
      metadata: params.metadata,
      timestamp: new Date().toISOString(),
    };

    await this.queueTask(operationId, taskPayload);
  }

  async queueOOOCreatedWebhook(params: QueueOOOWebhookParams): Promise<void> {
    const operationId = params.operationId || uuidv4();

    this.log.debug("Queueing OOO webhook task", {
      operationId,
      triggerEvent: WebhookTriggerEvents.OOO_CREATED,
      oooEntryId: params.oooEntryId,
      userId: params.userId,
    });

    const taskPayload: WebhookTaskPayload = {
      operationId,
      triggerEvent: WebhookTriggerEvents.OOO_CREATED,
      oooEntryId: params.oooEntryId,
      userId: params.userId,
      teamId: params.teamId,
      oAuthClientId: params.oAuthClientId,
      metadata: params.metadata,
      timestamp: new Date().toISOString(),
    };

    await this.queueTask(operationId, taskPayload);
  }

  /**
   * Internal helper to queue booking-related webhooks
   */
  private async queueBookingWebhook(
    triggerEvent: Exclude<
      BookingTriggerEvents,
      typeof WebhookTriggerEvents.BOOKING_PAYMENT_INITIATED | typeof WebhookTriggerEvents.BOOKING_PAID
    >,
    params: QueueBookingWebhookParams
  ): Promise<void> {
    const operationId = params.operationId || uuidv4();

    this.log.debug("Queueing booking webhook task", {
      operationId,
      triggerEvent,
      bookingUid: params.bookingUid,
      eventTypeId: params.eventTypeId,
    });

    const taskPayload: WebhookTaskPayload = {
      operationId,
      triggerEvent,
      bookingUid: params.bookingUid,
      eventTypeId: params.eventTypeId,
      teamId: params.teamId,
      userId: params.userId,
      orgId: params.orgId,
      oAuthClientId: params.oAuthClientId,
      metadata: params.metadata,
      timestamp: new Date().toISOString(),
    };

    await this.queueTask(operationId, taskPayload);
  }

  /**
   * Internal helper to queue payment-related webhooks
   */
  private async queuePaymentWebhook(
    triggerEvent: PaymentTriggerEvents,
    params: QueuePaymentWebhookParams
  ): Promise<void> {
    const operationId = params.operationId || uuidv4();

    this.log.debug("Queueing payment webhook task", {
      operationId,
      triggerEvent,
      bookingUid: params.bookingUid,
    });

    const taskPayload: WebhookTaskPayload = {
      operationId,
      triggerEvent,
      bookingUid: params.bookingUid,
      eventTypeId: params.eventTypeId,
      teamId: params.teamId,
      userId: params.userId,
      orgId: params.orgId,
      oAuthClientId: params.oAuthClientId,
      metadata: params.metadata,
      timestamp: new Date().toISOString(),
    };

    await this.queueTask(operationId, taskPayload);
  }

  /**
   * Internal helper to queue task via WebhookTasker
   *
   * The WebhookTasker automatically selects the appropriate execution mode:
   * - Production: Queues to Trigger.dev for background processing
   * - E2E Tests: Executes immediately via WebhookSyncTasker
   */
  private async queueTask(operationId: string, taskPayload: WebhookTaskPayload): Promise<void> {
    try {
... (truncated)
```
--- END SOURCE SNIPPETS ---

QUESTION: How does the headless router flow from a submitted form to a booked meeting?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
