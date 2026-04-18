# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-calcom-struct-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.


--- ARCHITECTURAL CONTEXT (LLM-generated, one-time) ---
(See deep context below for calcom architecture)
--- END ARCHITECTURAL CONTEXT ---

--- DEEP DOMAIN CONTEXT (LLM-generated from key files, one-time) ---
# Cal.com / Cal.diy deep domain context

## Scope and framing
This repository is effectively the open-source Cal scheduling platform packaged as a Yarn/Turborepo monorepo. The README positions it as **Cal.diy**, a community-maintained fork of Cal.com with enterprise/commercial features stripped out, but the core scheduling architecture is still very recognizably Cal.com: Next.js web app, tRPC server layer, Prisma/Postgres data model, and a newer Nest-based API v2 alongside the legacy web/tRPC APIs.

The most important mental model is: **Cal is an event-type-driven scheduling engine**. Users, teams, and profiles own event types; event types point to schedules/availability rules and booking policies; slot computation combines those rules with busy calendars, booking limits, and temporary reservations; confirmed bookings then fan out to calendars, conferencing, workflows, notifications, and follow-up actions.

## Monorepo structure
The root `package.json` defines workspaces for `apps/*`, `apps/api/*`, `packages/*`, `packages/features/*`, `packages/platform/*`, and app-store/example packages. In practice:

- `apps/web` is the main Next.js product UI and booking frontend.
- `apps/api/v2` is the newer REST API, implemented with NestJS.
- `packages/prisma` owns the canonical Prisma schema and generated types.
- `packages/trpc` owns the shared tRPC server/router layer used heavily by the web app.
- `packages/features/*` contains most business logic split by domain (availability, bookings, auth, schedules, credentials, etc.).

`turbo.json` shows the architecture boundaries clearly: `@calcom/web` depends on shared packages, `@calcom/prisma` is foundational, `@calcom/trpc` builds types for consumers, and `@calcom/api-v2` is treated as a separate deployable. The large `globalEnv` list also tells you this app is heavily integration-driven: calendar providers, email, payments, telephony, Redis, SSO/OAuth, and feature flags all matter to runtime behavior.

## Core domain model
The Prisma schema is the best source of truth.

### Identity and ownership
`User` is the core actor. It stores login identity (`email`, password/2FA, `identityProvider`), preferences (`timeZone`, `weekStart`, locale, branding), scheduling state (`availability`, `schedules`, `selectedCalendars`, `destinationCalendar`), and business relationships (`bookings`, `teams`, `profiles`, `ownedEventTypes`).

`Profile` is important: it separates a user’s identity from their organization-specific presence. A user can have multiple profiles, one per organization, each with its own `username`. This is how org-aware usernames and profile switching work.

`Team` is overloaded in the Cal model: it represents both teams and organizations. It has branding, timezone defaults, booking limits, org settings, children/parent relationships, and `members` via `Membership`. `Membership` captures accepted membership plus role (`MEMBER`, `ADMIN`, `OWNER`).

### Scheduling primitives
`EventType` is the central business object. It defines what can be booked: title, slug, description, duration (`length`), timezone behavior, recurrence, custom booking fields, locations, confirmation rules, booking notice/buffers, seats, scheduling type, booking/duration limits, redirect behavior, metadata, and more.

The most important relations on `EventType` are:
- `users` / `owner`: who owns it
- `team` / `profile`: which scope it belongs to
- `bookings`: actual reservations made against it
- `availability` and `schedule`: explicit timing rules
- `hosts`: host assignments for team / round-robin / collective scheduling
- `destinationCalendar`: where resulting events land

`SchedulingType` has three core modes:
- `ROUND_ROBIN`: pick one qualified host
- `COLLECTIVE`: multiple hosts must be available together
- `MANAGED`: parent/template style event type relationship

`Host`, `HostGroup`, and `HostLocation` matter for team scheduling. Hosts can be fixed or weighted, may point at their own schedule, may belong to groups, and may override location/credential behavior. This is key to understanding routed teams and round-robin assignment.

`Schedule` is a named container for availability with a timezone. `Availability` entries are the actual rules: days of week, start/end time, optional date override, and optional attachment to user, event type, or schedule.

### Calendar integration and booking persistence
`Credential` stores linked provider credentials (Google/Outlook/etc.), while `SelectedCalendar` marks which external calendars are consulted for busy times. `DestinationCalendar` marks where booked meetings should be written.

`Booking` is the persisted reservation. It captures `uid`, attendee responses/custom inputs, start/end, status (`ACCEPTED`, `PENDING`, `AWAITING_HOST`, `CANCELLED`, `REJECTED`), references, payment state, reschedule lineage, recurring IDs, ratings, metadata, and reporting/audit relations. A booking is not just a time slot; it is the durable workflow object the rest of the system hangs off.

## API surface
There are two major surfaces.

### 1) tRPC (web app / internal frontend API)
`packages/trpc/server/routers/_app.ts` exposes a single root `appRouter` containing `viewer`.

`viewer/_router.tsx` then composes the real domain routers:
- `auth`
- `bookings`
- `availability`
- `slots`
- `eventTypes` / `eventTypesHeavy`
- `calendars`, `credentials`, `webhook`, `me`, `apps`, etc.
- `public` and `loggedInViewerRouter`

This is the older but still central application API.

Key booking-facing routers:
- `publicViewerRouter`: unauthenticated calls like `event`, `countryCode`, rating submission, email-verification requirement checks.
- `loggedInViewerRouter`: logged-in self-service actions like notifications subscriptions, connected accounts, event-type order, connect-and-join.
- `viewer.bookings`: authenticated booking management (`get`, `find`, `requestReschedule`, `confirm`, `addGuests`, `editLocation`, history, reporting).
- `viewer.availability`: authenticated availability/schedule queries and schedule CRUD subtree.
- `viewer.slots`: public slot discovery/reservation (`getSchedule`, `reserveSlot`, `isAvailable`, reservation cleanup).

A key pattern across routers is **schema + lazy-loaded handler**. Routers mostly validate input with Zod then dynamically import a handler. This keeps route declarations thin and domain logic elsewhere.

### 2) REST API v2 (NestJS)
`apps/api/v2` is the newer external-facing API. The clearest scheduling example is `/v2/slots` in `slots.controller.ts`.

The controller documents multiple lookup modes:
- by `eventTypeId`
- by `eventTypeSlug + username`
- by `eventTypeSlug + teamSlug`
- by `usernames[]` for dynamic multi-person availability
- with optional `organizationSlug`
- optional `duration`, `timeZone`, `format`, `bookingUidToReschedule`

It also exposes reservation endpoints (`POST /v2/slots/reservations`, lookup/update/delete by UID). The service layer enforces extra rules like ownership checks for custom reservation duration and round-robin slot validation.

## Auth and session handling
Auth is NextAuth-based but heavily customized.

`next-auth-options.ts` shows:
- session strategy is `jwt`
- providers include credentials, Google, Azure AD, and email magic links
- a custom adapter (`next-auth-custom-adapter`) maps Cal’s DB model to NextAuth expectations
- login can auto-link identities by email and enrich JWT/session with Cal-specific fields like `profileId`, `upId`, `orgAwareUsername`, org context, locale, and active-team status

Important auth behavior:
- Credentials login validates password, rate limits attempts, and enforces 2FA / backup codes.
- Google and Azure sign-in can auto-install calendar credentials and selected calendars if scopes are present.
- Session state carries **profile context** (`profileId`, `upId`) because the same user can operate through different org profiles.

`getServerSession.ts` is a slim server-side session resolver. Instead of running full NextAuth on every request, it decodes the JWT token, fetches the user from Prisma, enriches it, and reconstructs a `Session`. It caches sessions in an LRU by token payload. That is why a lot of server code can cheaply ask “who is this user/profile?” without invoking the full NextAuth stack.

`userFromSessionUtils.ts` is another crucial bridge: it turns session -> enriched user + org/profile context, verifies that the profile in session is authorized, and normalizes organization metadata for downstream business logic.

The API v2 side wraps this with guards/strategies (`AuthModule`, `NextAuthGuard`, `ApiAuthGuard`) so both browser sessions and API credentials can coexist.

## Booking flow
The booking flow spans public event discovery, slot calculation, temporary reservation, form submission, and final booking creation.

1. **Load public event metadata**  
   `publicViewer.event` is the frontend-facing way to fetch bookable event information for a public page.

2. **Load candidate slots**  
   `viewer.slots.getSchedule` delegates to `AvailableSlotsService.getAvailableSlots`. This is the core availability engine.

3. **Temporarily reserve a slot**  
   `viewer.slots.reserveSlot` creates temporary `selectedSlots` rows keyed by a `uid` cookie. This prevents two bookers from racing for the same non-seated slot. Reservation expiry is based on `MINUTES_TO_BOOK`. Seated events are treated differently because multiple attendees may share a slot.

4. **Collect booking form data**  
   `apps/web/modules/bookings/components/Booker.tsx` is the main booking UI orchestrator. It behaves like a state machine: selecting date -> selecting time -> booking. It integrates embed mode, responsive layouts, email verification, captcha, overlay calendars, quick availability checks, and skip-confirm-step logic.

5. **Submit booking**  
   `BookEventForm.tsx` renders dynamic booking fields from `eventType.bookingFields`, handles paid-event detection, validates captcha/email verification, and submits via `useBookings`.

6. **Persist booking / redirect**  
   `useBookings.ts` calls `createBooking` (`POST /api/book/event`) or recurring booking creation. On success it branches into dry-run handling, payment redirect, reschedule success, or normal success redirect. This is also where embed SDK events are fired.

## Availability and scheduling logic
The deepest scheduling logic lives in `packages/features/availability` and `packages/trpc/server/routers/viewer/slots/util.ts`.

`detectEventTypeScheduleForUser.ts` encodes schedule precedence:
1. event type schedule
2. host-specific schedule
3. user default schedule
4. fallback default Monday-Friday 09:00-17:00

`getUserAvailability.ts` shows the real complexity. User availability is not just static working hours; it combines:
- schedules and date overrides
- user/event buffers
- selected external calendars and busy times
- travel schedules
- out-of-office entries and reasons
- holidays
- booking limits / duration limits
- current bookings and seats
- event metadata and scheduling mode

`getAggregatedAvailability.ts` explains how multi-host events work:
- for collective/fixed-host scenarios, availability is based on intersection
- for round-robin, hosts are grouped and the system needs at least one available host per group
- out-of-office-excluded ranges are used when team semantics require it

`AvailableSlotsService` adds orchestration on top:
- resolves event type from slug/id/team/user context
- supports dynamic events built from username lists
- checks reserved slots and cleans expired reservations
- uses Redis caching for slot responses
- applies booking-period logic, interval limits, reserved-slot overlap checks, busy time/conflict checks, and org/subdomain rules
- ultimately maps computed availability into bookable slot output

The REST v2 slots service mirrors this but adds API-oriented validation and authorization.

## Practical code-navigation guidance
If you need to understand Cal quickly, start in this order:
1. `packages/prisma/schema.prisma` for the vocabulary
2. `packages/trpc/server/routers/viewer/_router.tsx` for major internal API domains
3. `packages/features/auth/lib/next-auth-options.ts` + `getServerSession.ts` for identity/session model
4. `packages/trpc/server/routers/viewer/slots/util.ts` for slot-generation orchestration
5. `packages/features/availability/lib/getUserAvailability.ts` for raw availability computation
6. `apps/web/modules/bookings/components/Booker.tsx` and `hooks/useBookings.ts` for the end-user booking UX

The biggest conceptual trap is assuming Cal is “just a calendar UI”. It is really a **policy-heavy scheduling engine** with layered ownership (user/profile/team/org), multiple event scheduling modes, temporary reservation semantics, and calendar/provider synchronization woven throughout.

--- END DEEP DOMAIN CONTEXT ---

--- CLUE FILE START ---
=CC v2.1 calcom@HEAD 5074mod 11733sym
? How is Cal.diy split across its main runtime components and platform packages?


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

WrappedBookerPropsForPlatform (apps/web/modules/bookings/types.ts:99-99)
  type alias WrappedBookerPropsForPlatform = WrappedBookerPropsMain & {
  uses: WrappedBookerPropsMain

WrappedBookerPropsForPlatform (apps/web/modules/bookings/types.ts:100-100)
  type alias WrappedBookerPropsForPlatform = WrappedBookerPropsMain & {
  uses: WrappedBookerPropsMain

packages/prisma/docker-compose.yml (packages/prisma/docker-compose.yml:1-27)
  Config summary for packages/prisma/docker-compose.yml: entries: postgres: postgres:18, environment: "cal-saml", "", trust, healthcheck: ["CMD-SHELL", "pg_isready"], 10s, 5s, 5, postgres_is_ready: postgres, postgres: service_healthy; services: postgres, ports, volumes, environment, healthcheck, postgres_is_ready
  entries: postgres: postgres:18, environment: "cal-saml", "", trust, healthcheck: ["CMD-SHELL", "pg_isready"], 10s, 5s, 5, postgres_is_ready: postgres, postgres: service_healthy
  services: postgres, ports, volumes, environment, healthcheck

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

BaseCalProviderProps (packages/platform/atoms/cal-provider/BaseCalProvider.tsx:37-37)
  type alias BaseCalProviderProps = {

BaseCalProviderProps (packages/platform/atoms/cal-provider/BaseCalProvider.tsx:38-38)
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

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 83 symbols in L3, 23 with behavior annotations
uncovered: GlobalCalWithoutNs, GoogleCalError, IWipeMyCalAction, IWipeMyCalActionButtonProps

--- CLUE FILE END ---

QUESTION: How is Cal.diy split across its main runtime components and platform packages?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
