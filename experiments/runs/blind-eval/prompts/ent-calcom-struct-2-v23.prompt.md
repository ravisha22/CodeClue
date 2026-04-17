# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-calcom-struct-2

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 calcom@HEAD 5074mod 11733sym
? What enterprise capabilities does Cal.diy explicitly exclude compared with Cal.com?


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

CalComAdapter (packages/features/auth/lib/next-auth-custom-adapter.ts:62-170)
  sig: CalComAdapter(prismaClient: PrismaClient)
  behavior: GUARD(account?.user -> return toAdapterUse...); PRECEDENCE(account -> isinstance_Prisma)
  calls: createAccountData, createUserData, getAccountWhere, parseIntSafe, toAdapterAccount, toAdapterUser
  uses: prismaClient.user.create, prismaClient.user.findUnique, prismaClient.account.findUnique, providerAccountId.provider

Cal.getLastLoadedLinkInframe (packages/embeds/embed-core/src/embed.ts:711-721)
  method Cal.getLastLoadedLinkInframe
  behavior: GUARD(!this.iframe || !this.iframe.dataset.calLink -> return null;); PRECEDENCE(not_iframe -> not_calLink)
  called_by: recordUpdatedParamsForIframe, Cal, CalApi
  uses: this.iframe, this.iframe.dataset.calLink, this.iframe.src, urlObject.pathname

CalApi.init (packages/embeds/embed-core/src/embed.ts:862-883)
  method CalApi.init
  sig: CalApi.init(namespaceOrConfig?: string | InitArgConfig, config = {} a...)
  behavior: GUARD(initForNamespace !== this.cal.namespace -> return;)
  called_by: CalApi
  uses: this.cal.namespace, CalApi.initializedNamespaces.push, this.cal.__config.calOrigin, this.cal.__config

CalVideoService.getVideoSessions (apps/api/v2/src/platform/bookings/2024-08-13/services/cal-video.service.ts:88-101)
  async_method CalVideoService.getVideoSessions
  sig: CalVideoService.getVideoSessions(bookingUid: string)
  behavior: DELEGATE(this.calVideoOutputService.getOutputVideoSessions -> result)
  calls: getVideoSessionsRoomName
  called_by: CalVideoService
  uses: this.bookingsRepository.getByUidWithBookingReference, this.getVideoSessionsRoomName, booking.references, this.calVideoOutputService.getOutputVideoSessions

CalVideoSettingsRepository.deleteCalVideoSettings (packages/features/calVideoSettings/repositories/CalVideoSettingsRepository.ts:4-8)
  async_method CalVideoSettingsRepository.deleteCalVideoSettings
  sig: CalVideoSettingsRepository.deleteCalVideoSettings(eventTypeId: number)
  behavior: DELEGATE(prisma.calVideoSettings.delete -> result)
  called_by: CalVideoSettingsRepository
  uses: prisma.calVideoSettings.delete

getCloseComCustomActivityTypeFieldsIds (packages/lib/CloseComeUtils.ts:151-193)
  sig: getCloseComCustomActivityTypeFieldsIds(customFields: CloseComFieldOptions, closeCom: CloseCom)
  behavior: TRANSFORM(map)
  calls: getCustomFieldsIds
  called_by: getCustomActivityTypeInstanceData
  uses: closeCom.customActivity.type.get, customActivities.data.filter, act.name, calComCustomActivity.length

Cal.doInIframe (packages/embeds/embed-core/src/embed.ts:397-413)
  method Cal.doInIframe
  sig: Cal.doInIframe(doInIframeArg: DoInIframeArg)
  behavior: GUARD(!this.iframeReady -> this.iframeDoQueue....)
  called_by: constructor, Cal, ui, CalApi
  uses: this.iframeReady, this.iframeDoQueue.push, this.iframe, this.iframe.contentWindow

doWeNeedCalOriginProp (packages/features/embed/lib/EmbedCodes.tsx:7-12)
  sig: doWeNeedCalOriginProp(embedCalOrigin: string)
  called_by: MyApp
  uses: app.cal.com

isSmsCalEmail (packages/lib/isSmsCalEmail.ts:1-3)
  sig: isSmsCalEmail(email: string)
  behavior: DELEGATE(email.endsWith -> result)
  uses: email.endsWith, sms.cal.com

CalApi (packages/embeds/embed-core/src/embed.ts:847-1505)
  methods: closeModal, constructor, handleClose, init, initNamespace, log
  calls: constructor, doInIframe, ensureGuestKey, getCalConfig, getLastLoadedLinkInframe, getPreviousModalRenderStartVariables, log, Cal
  called_by: constructor, Cal
  uses: this.cal, this.cal.namespace, CalApi.initializedNamespaces.push, this.cal.__config.calOrigin

Cal.constructor (packages/embeds/embed-core/src/embed.ts:427-522)
  method Cal.constructor
  sig: Cal.constructor(namespace: string, q: Queue)
  behavior: GUARD(!iframe -> // Iframe might be...); PRECEDENCE(not_iframe -> data -> modalBox); ACCUMULATE(constructor loop -> result)
  calls: doInIframe, processQueue, resetQueue, constructor, CalApi
  called_by: Cal, constructor, CalApi
  uses: this.__config, this.api, this.namespace, this.actionManager

CloseCom (packages/lib/CloseCom.ts:194-487)
  methods: getHeaders, refreshAccessToken, shouldRefreshToken
  calls: getHeaders, refreshAccessToken, shouldRefreshToken
  uses: api.close.com, this.log, logger.getSubLogger, close.com

CalApi.ui (packages/embeds/embed-core/src/embed.ts:1488-1504)
  method CalApi.ui
  sig: CalApi.ui(uiConfig: UiConfig)
  calls: doInIframe, validate
  called_by: CalApi
  uses: this.cal.doInIframe

CalVideoSettingsRepository (packages/features/calVideoSettings/repositories/CalVideoSettingsRepository.ts:2-83)
  methods: deleteCalVideoSettings
  calls: deleteCalVideoSettings
  uses: prisma.calVideoSettings.delete, prisma.calVideoSettings.create, calVideoSettings.disableRecordingForGuests, calVideoSettings.disableRecordingForOrganizer

BookingLocationIntegrationService_2024_08_13.handleCalVideoLocation (apps/api/v2/src/platform/bookings/2024-08-13/services/booking-location-integration.service.ts:141-186)
  async_method BookingLocationIntegrationService_2024_08_13.handleCalVideoLocation
  sig: BookingLocationIntegrationService_2024_08_13.handleCalVideoLocation(ctx: IntegrationHandlerContext)
  behavior: DELEGATE(this.updateBookingWithVideoLocation -> result)
  called_by: handleGoogleMeetLocation, BookingLocationIntegrationService_2024_08_13
  uses: this.bookingVideoService.deleteOldVideoMeetingIfNeeded, ctx.existingBooking.id, this.calendarSyncService.buildCalEventFromBookingData, ctx.booking

CAL_AI_PHONE_NUMBER_MONTHLY_PRICE (packages/lib/constants.ts:248-253)
  sig: CAL_AI_PHONE_NUMBER_MONTHLY_PRICE(()
  behavior: DELEGATE(Number.isFinite -> result)
  uses: _rawCalAiPrice.trim, Number.isFinite

Cal.buildFilteredQueryParams (packages/embeds/embed-core/src/embed.ts:548-567)
  method Cal.buildFilteredQueryParams
  sig: Cal.buildFilteredQueryParams(queryParamsFromConfig: PrefillAndIframeAttrsConfig)
  behavior: ACCUMULATE(buildFilteredQueryPar... -> result)
  calls: getQueryParamsFromPage
  called_by: Cal
  uses: globalCal.config, this.getQueryParamsFromPage, Object.entries, value.forEach

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 83 symbols in L3, 24 with behavior annotations
uncovered: Cal.log, Cal.log, Cal.log, Cal.scrollByDistance

--- CLUE FILE END ---

QUESTION: What enterprise capabilities does Cal.diy explicitly exclude compared with Cal.com?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
