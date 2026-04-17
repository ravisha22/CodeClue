# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-calcom-struct-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 calcom@HEAD 5074mod 11723sym
? How is Cal.diy split across its main runtime components and platform packages?


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
WrappedBookerPropsForPlatform (apps/web/modules/bookings/types.ts:100-100)
  type alias WrappedBookerPropsForPlatform = WrappedBookerPropsMain & {
  uses: WrappedBookerPropsMain

WrappedBookerPropsForPlatform (apps/web/modules/bookings/types.ts:99-99)
  type alias WrappedBookerPropsForPlatform = WrappedBookerPropsMain & {
  uses: WrappedBookerPropsMain

SplitNameDefaultFieldInput_2024_06_14 (packages/platform/types/event-types/event-types_2024_06_14/inputs/booking-fields.input.ts:58-103)
  uses: e.g, cal.com

CalProviderLanguagesType (packages/platform/atoms/cal-provider/languages.ts:34-34)
  type alias CalProviderLanguagesType = (typeof CAL_PROVIDER_LANGUAGES)[number]
  uses: CAL_PROVIDER_LANGUAGES, number

main (packages/platform/libraries/scripts/prepublish.js:42-63)
  calls: getCurrentVersion, incrementPatchVersion
  uses: console.log, package.json, path.join, JSON.parse

CalMeetingParticipant (packages/platform/types/bookings/2024-08-13/outputs/get-booking-video-sessions.output.ts:6-23)

CalMeetingSession (packages/platform/types/bookings/2024-08-13/outputs/get-booking-video-sessions.output.ts:24-55)

CalVideoSettings (packages/platform/types/event-types/event-types_2024_06_14/inputs/create-event-type.input.ts:139-196)

SplitButtonProps (packages/ui/components/button/SplitButton.tsx:10-21)
  interface SplitButtonProps
  extends: ButtonBaseProps

SplitNameDefaultFieldOutput_2024_06_14 (packages/platform/types/event-types/event-types_2024_06_14/outputs/booking-fields.output.ts:55-76)
  extends: SplitNameDefaultFieldInput_2024_06_14

BookerPlatformWrapperComponent (packages/platform/atoms/booker/BookerPlatformWrapper.tsx:49-577)
  sig: BookerPlatformWrapperComponent(props: BookerPlatformWrapperAtomPropsForIndividual | Book...)
  behavior: GUARD(bookingData?.user?.username -> return formatUserna...); PRECEDENCE(stateChanged -> bookingData -> props -> default); TRANSFORM(map)
  calls: formatUsername
  uses: props.isTeamEvent, props.teamId, state.state, state.setState

CalendarViewPlatformWrapperComponent (packages/platform/atoms/calendar-view/wrappers/CalendarViewPlatformWrapper.tsx:26-33)
  sig: CalendarViewPlatformWrapperComponent(props: CalendarViewProps)
  behavior: GUARD(!props.isEventTypeView -> return <CalendarVie...)
  uses: props.isEventTypeView

main (packages/platform/libraries/scripts/postpublish.js:12-63)
  calls: waitForNewestNpmRelease
  uses: path.join, package.json, JSON.parse, fs.readFileSync

BaseCalProviderProps (packages/platform/atoms/cal-provider/BaseCalProvider.tsx:38-38)
  type alias BaseCalProviderProps = {

BaseCalProviderProps (packages/platform/atoms/cal-provider/BaseCalProvider.tsx:37-37)
  type alias BaseCalProviderProps = {

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

PlatformOAuthClientRepository.getByUserId (packages/features/platform-oauth-client/platform-oauth-client.repository.ts:8-23)
  async_method PlatformOAuthClientRepository.getByUserId
  sig: PlatformOAuthClientRepository.getByUserId(userId: number)
  behavior: DELEGATE(prisma.platformOAuthClient.findFirst -> result)
  called_by: PlatformOAuthClientRepository
  uses: prisma.platformOAuthClient.findFirst

main (packages/embeds/embed-core/src/embed-iframe.ts:521-612)
  behavior: GUARD(!isBrowser -> return;); PRECEDENCE(not_isBrowser -> top -> not_data -> default)
  calls: actOnColorScheme, initializeAndSetupEmbed, messageParent, showPageAsNonEmbed
  uses: document.URL, embedStore.theme, url.searchParams.get, ui.autoscroll

main (packages/app-store/dailyvideo/lib/scripts/deleteRecordings.ts:199-241)
  behavior: ACCUMULATE(main loop -> result)
  calls: getAllRecordingsOlderThan6Months, saveRecordingsToJson
  uses: console.log, recordings.reduce, recording.duration, Math.floor

main (packages/prisma/seed-pbac-only.ts:8-40)
  behavior: ACCUMULATE(main loop -> result)
  uses: console.log, result.organization.name, result.organization.slug, Object.keys

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

Cal.doInIframe (packages/embeds/embed-core/src/embed.ts:397-413)
  method Cal.doInIframe
  sig: Cal.doInIframe(doInIframeArg: DoInIframeArg)
  behavior: GUARD(!this.iframeReady -> this.iframeDoQueue....)
  called_by: constructor, Cal, ui, CalApi
  uses: this.iframeReady, this.iframeDoQueue.push, this.iframe, this.iframe.contentWindow

main (scripts/pull-coss-ui-components.ts:217-259)
  behavior: TRANSFORM(map)
  calls: processComponent, resolvePaths
  uses: console.log, targetDirs.components, Array.isArray, uiJson.registryDependencies

doWeNeedCalOriginProp (packages/features/embed/lib/EmbedCodes.tsx:7-12)
  sig: doWeNeedCalOriginProp(embedCalOrigin: string)
  called_by: MyApp
  uses: app.cal.com

Cal.resetQueue (packages/embeds/embed-core/src/embed.ts:415-420)
  method Cal.resetQueue
  called_by: constructor, iframeReset, Cal
  uses: this.iframeDoQueue, this.iframeDoQueue.filter, this.commandsPersistAcrossIframeResets.includes, doInIframeArg.method

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

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 80 symbols in L3, 23 with behavior annotations
uncovered: GoogleCalError, IWipeMyCalAction, IWipeMyCalActionButtonProps, ListEventTypesPlatformWrapperProps

--- CLUE FILE END ---

QUESTION: How is Cal.diy split across its main runtime components and platform packages?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
