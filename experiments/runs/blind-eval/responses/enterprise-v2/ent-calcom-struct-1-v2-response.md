# Enterprise v2: ent-calcom-struct-1
Date: 2026-04-17

## Question
How is Cal.diy split across its main runtime components and platform packages?

## Answer

### Top-Level Repository Layout

Cal.diy is organised as a monorepo with three top-level groupings visible in TREE: **`apps/`** (1635 files), **`packages/`** (3420 files), and **`example-apps/`** (8 files), alongside root config files (`package.json`, `docker-compose.yml`, `playwright.config.ts`, `vitest.workspace.ts`, etc.) (TREE, root).

### Runtime Application Components (`apps/`)

The `apps/` directory contains three deployable runtime components (TREE, `apps/`):

1. **`apps/web/`** — The primary Next.js web application. It serves the scheduling UI and references `NEXT_PUBLIC_WEBAPP_URL=http://localhost:3000` and `NEXT_PUBLIC_WEBSITE_URL=http://localhost:3000` (FOCUS, `.env.example:1-484`). The web app consumes platform wrapper components such as `BookerPlatformWrapperComponent` (FOCUS, `packages/platform/atoms/booker/BookerPlatformWrapper.tsx:49-577`) and `CalendarViewPlatformWrapperComponent` (FOCUS, `packages/platform/atoms/calendar-view/wrappers/CalendarViewPlatformWrapper.tsx:26-33`).

2. **`apps/api/`** — The API v2 application, a separate runtime that runs on port 5555 (`API_PORT=5555`) and uses a read/write database split (`DATABASE_READ_URL`, `DATABASE_WRITE_URL`) (FOCUS, `apps/api/v2/.env.example:1-76`). It hosts services like `CalVideoService` (FOCUS, `apps/api/v2/src/platform/bookings/2024-08-13/services/cal-video.service.ts:88-101`), `CalendarsCacheService` using Redis (INDEX, `apps/api/v2/src/platform/calendars/services/calendars-cache.service.ts`), and event-type atom services (INDEX, `apps/api/v2/src/modules/atoms/services/event-types-atom.service.ts`). It has its own logger bridge (`Logger.logInternal`, SYM, `apps/api/v2/src/lib/logger.bridge.ts:142`).

3. **`apps/docs/`** — A documentation application (TREE, `apps/docs/`). No further detail is available from the clue.

### Shared Packages (`packages/`)

The `packages/` directory contains 3420 files across at least 14 sub-packages (TREE, `packages/`):

- **`packages/lib/`** — Core library code including `CalendarService` (INDEX, `packages/lib/CalendarService.ts`, 1023L), calendar-app error hierarchies (`CalendarAppError`, `CalendarAppDelegationCredentialError`, etc., SYM, `packages/lib/CalendarAppError.ts`), constants like `CAL_AI_PHONE_NUMBER_MONTHLY_PRICE` (FOCUS, `packages/lib/constants.ts:248-253`), and `TriggerDevLogger` (SYM, `packages/lib/triggerDevLogger.ts:76`).

- **`packages/features/`** — Domain feature modules: booking audit (`EnrichmentDataStore`, INDEX, `packages/features/booking-audit/lib/service/EnrichmentDataStore.ts`), tasker (`repository.ts` with cancel/cleanup/count, INDEX, `packages/features/tasker/repository.ts`), webhooks (`WebhookRepository` with permission checking, INDEX, `packages/features/webhooks/lib/repository/WebhookRepository.ts`), calendar video settings (`CalVideoSettingsRepository`, FOCUS, `packages/features/calVideoSettings/repositories/CalVideoSettingsRepository.ts`), caching decorators (`Memoize`/`Unmemoize` tests, SYM), selected calendar repository (SYM, `packages/features/selectedCalendar/repositories/SelectedCalendarRepository.ts`), watchlist operations (SYM, `packages/features/watchlist/lib/service/OrganizationWatchlistOperationsService.ts`), and platform OAuth client repository (FOCUS, `packages/features/platform-oauth-client/platform-oauth-client.repository.ts:8-23`).

- **`packages/embeds/`** — Embed infrastructure: `embed-core` with the main `Cal` class (INDEX, `packages/embeds/embed-core/src/embed.ts`, 1709L) providing `CalApi` (FOCUS, `packages/embeds/embed-core/src/embed.ts:847-1505`), iframe communication (`Cal.doInIframe`, FOCUS), query param filtering (`Cal.buildFilteredQueryParams`, FOCUS), and the SDK action manager (`sdk-action-manager.ts`, INDEX). Also includes `embed-iframe.ts` with browser-side initialization (FOCUS, `packages/embeds/embed-core/src/embed-iframe.ts:521-612`).

- **`packages/prisma/`** — Database layer with Prisma schema, a Docker Compose for PostgreSQL 18 (`postgres:18`) with SAML support and health checks (FOCUS, `packages/prisma/docker-compose.yml:1-27`), and PBAC seeding scripts (FOCUS, `packages/prisma/seed-pbac-only.ts:8-40`).

- **`packages/app-store/`** — Third-party integrations: ICS feed calendar (INDEX, `packages/app-store/ics-feedcalendar/lib/CalendarService.ts`), Zoho Bigin CRM (INDEX, `packages/app-store/zoho-bigin/lib/CrmService.ts`), daily video recording scripts (FOCUS, `packages/app-store/dailyvideo/lib/scripts/deleteRecordings.ts:199-241`).

- **`packages/i18n/`** — Internationalization (TREE).

- **`packages/emails/`** — Email templates (TREE).

- **`packages/dayjs/`** — Date/time utilities (TREE).

- **`packages/debugging/`** — Debugging utilities (TREE).

- **`packages/kysely/`** — Kysely query-builder integration (TREE).

### Platform Packages

A dedicated `packages/platform/` subtree provides platform-specific types, atoms, and utilities:

- **Platform types** — Versioned API types for event types (`SplitNameDefaultFieldInput_2024_06_14`, FOCUS, `packages/platform/types/event-types/event-types_2024_06_14/inputs/booking-fields.input.ts:58-103`), location validators (`InputLocationValidator_2024_06_14`, SYM, `packages/platform/types/event-types/event-types_2024_06_14/inputs/locations.input.ts:160`), booking video session types (`CalMeetingParticipant`, `CalMeetingSession`, FOCUS), and video settings (`CalVideoSettings`, FOCUS, `packages/platform/types/event-types/event-types_2024_06_14/inputs/create-event-type.input.ts:139-196`).

- **Platform atoms** — Reusable UI components: `BookerPlatformWrapperComponent` (FOCUS, `packages/platform/atoms/booker/BookerPlatformWrapper.tsx:49-577`), `CalendarViewPlatformWrapperComponent` (FOCUS, `packages/platform/atoms/calendar-view/wrappers/CalendarViewPlatformWrapper.tsx:26-33`), `CalProvider` with language support (`CalProviderLanguagesType`, FOCUS, `packages/platform/atoms/cal-provider/languages.ts:34`, `BaseCalProviderProps`, FOCUS, `packages/platform/atoms/cal-provider/BaseCalProvider.tsx:37`).

- **Platform permissions** — `hasPermission` functions in both `packages/platform/enums/permissions.ts:15` and `packages/platform/utils/permissions.ts:15` (SYM).

- **Platform libraries/scripts** — Pre/post-publish scripts managing NPM versioning (`main` in `prepublish.js` calling `getCurrentVersion`/`incrementPatchVersion`, FOCUS, `packages/platform/libraries/scripts/prepublish.js:42-63`; `postpublish.js` calling `waitForNewestNpmRelease`, FOCUS, `packages/platform/libraries/scripts/postpublish.js:12-63`).

### Example Apps

`example-apps/credential-sync/` provides a credential-sync example configured with Google and Zoom tokens (FOCUS, `example-apps/credential-sync/.env.example:1-15`).

### Data Layer

The repository uses PostgreSQL (port 5450) as its primary database, accessed through Prisma (FOCUS, `.env.example`). The API v2 introduces a read/write database split (FOCUS, `apps/api/v2/.env.example`). A separate `INSIGHTS_DATABASE_URL` is configured for analytics (FOCUS, `.env.example`). Redis caching is used in the API for calendars (`REDIS_CALENDARS_CACHE_KEY`, INDEX, `apps/api/v2/src/platform/calendars/services/calendars-cache.service.ts`).

### Gaps and Uncertainties

The GAPS section notes this is a STRUCTURAL question answerable from L0–L2, with 83 symbols at L3, 23 having behavior annotations. The symbols `GlobalCalWithoutNs`, `GoogleCalError`, `IWipeMyCalAction`, and `IWipeMyCalActionButtonProps` are uncovered (GAPS). The TREE shows `...+4` additional packages under `packages/` whose names are not enumerated. The internal structure of `apps/docs/` and several app-store integrations are not detailed in the clue.
