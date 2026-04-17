# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-calcom-mech-2

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 calcom@HEAD 5074mod 11733sym
? How is the platform example app wired to Cal.diy's API v2 for local OAuth testing?


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

OAuthCalendarApp (apps/api/v2/src/platform/calendars/calendars.interface.ts:25-28)
  interface OAuthCalendarApp
  extends: CalendarApp
  methods: connect
  calls: connect

OAuthCalendarApp.connect (apps/api/v2/src/platform/calendars/calendars.interface.ts:27-27)
  method OAuthCalendarApp.connect
  sig: OAuthCalendarApp.connect(authorization: string, req: Request)
  called_by: OAuthCalendarApp

PlatformOAuthClientRepository.getByUserId (packages/features/platform-oauth-client/platform-oauth-client.repository.ts:8-23)
  async_method PlatformOAuthClientRepository.getByUserId
  sig: PlatformOAuthClientRepository.getByUserId(userId: number)
  behavior: DELEGATE(prisma.platformOAuthClient.findFirst -> result)
  called_by: PlatformOAuthClientRepository
  uses: prisma.platformOAuthClient.findFirst

ConferencingService.connectUserNonOauthApp (apps/api/v2/src/modules/conferencing/services/conferencing.service.ts:45-53)
  async_method ConferencingService.connectUserNonOauthApp
  sig: ConferencingService.connectUserNonOauthApp(app: string, userId: number)
  behavior: DISPATCH(app)
  called_by: ConferencingService
  uses: this.googleMeetService.connectGoogleMeetToUser

CalApi.init (packages/embeds/embed-core/src/embed.ts:862-883)
  method CalApi.init
  sig: CalApi.init(namespaceOrConfig?: string | InitArgConfig, config = {} a...)
  behavior: GUARD(initForNamespace !== this.cal.namespace -> return;)
  called_by: CalApi
  uses: this.cal.namespace, CalApi.initializedNamespaces.push, this.cal.__config.calOrigin, this.cal.__config

PlatformBookingsService.getOAuthClientParams (apps/api/v2/src/platform/bookings/shared/platform-bookings.service.ts:36-62)
  async_method PlatformBookingsService.getOAuthClientParams
  sig: PlatformBookingsService.getOAuthClientParams(eventTypeId: number)
  behavior: PRECEDENCE(eventType -> not_oAuthClient)
  called_by: PlatformBookingsService
  uses: this.eventTypesRepository.getEventTypeById, this.oAuthClientRepository.getByUserId, eventType.userId, this.oAuthClientRepository.getByTeamId

CalApi (packages/embeds/embed-core/src/embed.ts:847-1505)
  methods: closeModal, constructor, handleClose, init, initNamespace, log
  calls: constructor, doInIframe, ensureGuestKey, getCalConfig, getLastLoadedLinkInframe, getPreviousModalRenderStartVariables, log, Cal
  called_by: constructor, Cal
  uses: this.cal, this.cal.namespace, CalApi.initializedNamespaces.push, this.cal.__config.calOrigin

PlatformOAuthClientRepository (packages/features/platform-oauth-client/platform-oauth-client.repository.ts:6-24)
  methods: getByUserId
  calls: getByUserId
  uses: prisma.platformOAuthClient.findFirst

AppListCardPlatformWrapper (packages/platform/atoms/connect/conferencing-apps/AppListCardPlatformWrapper.tsx:3-7)
  sig: AppListCardPlatformWrapper(props: AppListCardProps)
  uses: app.cal.com$, props.logo

CalApi.ui (packages/embeds/embed-core/src/embed.ts:1488-1504)
  method CalApi.ui
  sig: CalApi.ui(uiConfig: UiConfig)
  calls: doInIframe, validate
  called_by: CalApi
  uses: this.cal.doInIframe

PlatformOAuthClientDto (packages/platform/types/oauth-clients/outputs/oauth-client.output.ts:7-79)
  uses: Object.keys, example.com, logo.png

CalApi.closeModal (packages/embeds/embed-core/src/embed.ts:1333-1340)
  method CalApi.closeModal
  called_by: CalApi
  uses: this.cal.inlineEl, this.cal.modalBox, this.cal.actionManager.fire

CalApi.constructor (packages/embeds/embed-core/src/embed.ts:854-856)
  method CalApi.constructor
  sig: CalApi.constructor(cal: Cal)
  calls: constructor
  called_by: constructor, Cal, CalApi
  uses: this.cal

CalApi.handleClose (packages/embeds/embed-core/src/embed.ts:1276-1281)
  method CalApi.handleClose
  called_by: CalApi
  uses: this.cal.actionManager.on, this.cal.modalBox

CalApi.initNamespace (packages/embeds/embed-core/src/embed.ts:889-893)
  method CalApi.initNamespace
  sig: CalApi.initNamespace(namespace: string)
  calls: Cal
  called_by: CalApi
  uses: globalCal.ns

CalApi.log (packages/embeds/embed-core/src/embed.ts:1195-1195)
  method CalApi.log
  sig: CalApi.log("Initiating full page load")
  called_by: Cal, CalApi, log

CalApi.log (packages/embeds/embed-core/src/embed.ts:1226-1226)
  method CalApi.log
  sig: CalApi.log(`Creating new modal ${uid}`)
  called_by: Cal, CalApi, log

CalApi.log (packages/embeds/embed-core/src/embed.ts:1190-1190)
  method CalApi.log
  sig: CalApi.log("Attempting to load/connect regular booking link")
  called_by: Cal, CalApi, log

CalApi.log (packages/embeds/embed-core/src/embed.ts:1164-1164)
  method CalApi.log
  sig: CalApi.log(`Trying to reuse modal ${uid}`)
  called_by: Cal, CalApi, log

CalApi.log (packages/embeds/embed-core/src/embed.ts:1184-1184)
  method CalApi.log
  sig: CalApi.log(`Reopening modal without any other action needed ${uid}`)
  called_by: Cal, CalApi, log

CalApi.log (packages/embeds/embed-core/src/embed.ts:1090-1090)
  method CalApi.log
  sig: CalApi.log(`Prevented unnecessary repeat prerender for ${calLink}`)
  called_by: Cal, CalApi, log

CalApi.preloadAssetsForCalLink (packages/embeds/embed-core/src/embed.ts:1420-1420)
  method CalApi.preloadAssetsForCalLink
  sig: CalApi.preloadAssetsForCalLink({ calLink, config })
  called_by: CalApi

CalApi.preloadAssetsForCalLink (packages/embeds/embed-core/src/embed.ts:1417-1417)
  method CalApi.preloadAssetsForCalLink
  sig: CalApi.preloadAssetsForCalLink({ calLink, config })
  called_by: CalApi

getArgumentForGetCalApi (packages/features/embed/lib/EmbedCodes.tsx:346-351)
  sig: getArgumentForGetCalApi(namespace: string)

getCalApi (packages/embeds/embed-react/src/index.ts:15-22)
  sig: getCalApi(embedJsUrl: string)

getLocalAppMetadata (packages/app-store/utils.ts:109-112)

AppHandler (packages/types/AppHandler.d.ts:24-24)
  type alias AppHandler = AppDeclarativeHandler | NextApiHandler
  uses: AppDeclarativeHandler, NextApiHandler

createWorkspacePlatform (apps/web/app/api/cron/selected-calendars/__tests__/cron.test.ts:61-61)
  sig: createWorkspacePlatform({ id = 1 }: WorkspacePlatformParams = {})

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 82 symbols in L3, 18 with behavior annotations
uncovered: CredentialSyncCalendarApp.check, CredentialSyncCalendarApp.save, ICSFeedCalendarApp.check, InputEventTypesService_2024_06_14.transformInputCalVideoSettings

--- CLUE FILE END ---

QUESTION: How is the platform example app wired to Cal.diy's API v2 for local OAuth testing?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
