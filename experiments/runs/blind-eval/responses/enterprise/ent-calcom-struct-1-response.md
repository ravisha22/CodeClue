# Enterprise Eval: ent-calcom-struct-1
Date: 2026-04-17

## Question
How is Cal.diy split across its main runtime components and platform packages?

## Reasoning Scaffold

### Relevant Clue Entries

**TREE section** gives the top-level directory layout:

| Directory | Files | Sub-directories |
|-----------|-------|-----------------|
| `__checks__/` | 3 | — |
| `apps/` | 1632 | `api/`, `docs/`, `web/` |
| `example-apps/` | 7 | `credential-sync/` |
| `packages/` | 3418 | `app-store/`, `dayjs/`, `debugging/`, `emails/`, `embeds/`, `features/`, `i18n/`, `kysely/`, `lib/`, `prisma/`, …+4 |
| `scripts/` | 9 | — |

The header line (`=CC v2.1 calcom@HEAD 5074mod 11723sym`) confirms 5074 modules and 11723 symbols across the entire repository.

### Main Runtime Components (apps/)

The `apps/` directory (1632 files) contains three runtime sub-applications:

1. **`apps/api/`** — The API v2 runtime. Evidence from INDEX: `apps/api/v2/src/modules/atoms/services/event-types-atom.service.ts` (INDEX, line 38) and `apps/api/v2/src/platform/calendars/services/calendars-cache.service.ts` (INDEX, line 39) show a NestJS-style module/service structure under `apps/api/v2/src/`. FOCUS entries confirm this is a platform-facing API layer, e.g.:
   - `CalVideoService.getVideoSessions` (`apps/api/v2/src/platform/bookings/2024-08-13/services/cal-video.service.ts:88-101`, FOCUS) — a versioned booking/video service.
   - `Logger.logInternal` (`apps/api/v2/src/lib/logger.bridge.ts:142`, SYM) — API-level logging infrastructure.

2. **`apps/web/`** — The main web front-end. FOCUS entries show React component-level code here:
   - `BookerPlatformWrapperComponent` (`packages/platform/atoms/booker/BookerPlatformWrapper.tsx:49-577`, FOCUS) wraps booking UI and uses `WrappedBookerPropsForPlatform` (`apps/web/modules/bookings/types.ts:100`, FOCUS), confirming the web app consumes platform atoms.
   - `CalendarViewPlatformWrapperComponent` (`packages/platform/atoms/calendar-view/wrappers/CalendarViewPlatformWrapper.tsx:26-33`, FOCUS) — platform calendar UI atom rendered in the web app.

3. **`apps/docs/`** — Documentation app (TREE, line 22). No further detail is available in the clue regarding its internal structure.

### Platform Packages (packages/)

The `packages/` tree (3418 files) provides shared libraries consumed by the apps:

1. **`packages/embeds/`** — The embed SDK. The largest indexed module is `packages/embeds/embed-core/src/embed.ts` (1709 lines, INDEX line 31). Key classes:
   - `Cal` (`packages/embeds/embed-core/src/embed.ts:427-522`, FOCUS) — core embed constructor; manages iframes, queues, and namespace initialization via `Cal.constructor` → calls `doInIframe`, `processQueue`, `resetQueue`, then instantiates `CalApi`.
   - `CalApi` (`packages/embeds/embed-core/src/embed.ts:847-1505`, FOCUS) — the public API surface; methods include `init`, `ui`, `closeModal`, `initNamespace`.
   - `Cal.doInIframe` (`embed.ts:397-413`, FOCUS) — iframe communication with a guard on `iframeReady`.
   - `Cal.resetQueue` (`embed.ts:415-420`, FOCUS) — filters persisted commands during iframe resets.
   - SDK action manager: `packages/embeds/embed-core/src/sdk-action-manager.ts` (362 lines, INDEX line 41) defines `EmbedEvent` and `EventDataMap`.
   - Iframe bootstrap: `main` (`packages/embeds/embed-core/src/embed-iframe.ts:521-612`, FOCUS) — guards on `isBrowser`, calls `actOnColorScheme`, `initializeAndSetupEmbed`, `messageParent`.

2. **`packages/lib/`** — Core domain library:
   - `CalendarService` (`packages/lib/CalendarService.ts`, 1023 lines, INDEX line 32) — `constructor`, `createEvent`, `deleteEvent`, `getAccount`, `getAttendees`.
   - `CalendarAppError` hierarchy (`packages/lib/CalendarAppError.ts`, SYM lines 78-83) — `CalendarAppError` → `CalendarAppDelegationCredentialError` → specialized sub-errors (`ConfigurationError`, `InvalidGrantError`, `ClientIdNotAuthorizedError`, `NotSetupError`).
   - `TriggerDevLogger.logInternal` (`packages/lib/triggerDevLogger.ts:76`, SYM).

3. **`packages/features/`** — Domain feature modules:
   - `packages/features/tasker/repository.ts` (218 lines, INDEX line 36) — `cancel`, `cancelWithReference`, `cleanup`, `count`.
   - `packages/features/webhooks/lib/repository/WebhookRepository.ts` (592 lines, INDEX line 37) — `checkPermission`, `hasPermission`, `PermissionCheckService`.
   - `packages/features/booking-audit/` — `EnrichmentDataStore` (INDEX line 35), `BookingAuditAccessService` (SYM line 93), `BookingAuditPermissionError` (SYM line 94).
   - `packages/features/calVideoSettings/repositories/CalVideoSettingsRepository.ts` (FOCUS) — CRUD for cal-video recording settings via Prisma.
   - `packages/features/watchlist/` — `OrganizationWatchlistOperationsService.checkPermission` (SYM line 47).
   - `packages/features/cache/decorators/` — `Memoize` and `Unmemoize` test suites (SYM, multiple `TestRepository` entries).
   - `packages/features/embed/lib/EmbedCodes.tsx` — `doWeNeedCalOriginProp` (FOCUS), references `app.cal.com`.

4. **`packages/platform/`** — Platform-specific types, atoms, and scripts:
   - Types: versioned input/output DTOs under `packages/platform/types/event-types/event-types_2024_06_14/` — `InputLocationValidator_2024_06_14` (SYM line 50), `LayoutValidator` (SYM line 96), `SplitNameDefaultFieldInput_2024_06_14` (FOCUS).
   - Atoms (React components): `BookerPlatformWrapperComponent` (FOCUS), `CalendarViewPlatformWrapperComponent` (FOCUS), `BaseCalProviderProps` (FOCUS), `CalProviderLanguagesType` (FOCUS).
   - Permissions: `hasPermission` in both `packages/platform/enums/permissions.ts:15` and `packages/platform/utils/permissions.ts:15` (SYM lines 52-53).
   - Build scripts: `main` in `packages/platform/libraries/scripts/prepublish.js:42-63` (FOCUS) calls `getCurrentVersion`, `incrementPatchVersion`; `main` in `postpublish.js:12-63` (FOCUS) calls `waitForNewestNpmRelease`. These confirm the platform packages are published to npm.
   - `PlatformOAuthClientRepository.getByUserId` (`packages/features/platform-oauth-client/platform-oauth-client.repository.ts:8-23`, FOCUS) — OAuth client lookup via Prisma.

5. **`packages/app-store/`** — Third-party integration adapters:
   - `zoho-bigin/lib/CrmService.ts` (336 lines, INDEX line 34) — CRM integration.
   - `ics-feedcalendar/lib/CalendarService.ts` (318 lines, INDEX line 40) — ICS feed calendar.
   - `office365calendar/lib/CalendarService.ts` — `Office365CalendarService.triggerDelegationCredentialError` (SYM line 92).

6. **`packages/prisma/`** — Database layer: `main` in `packages/prisma/seed-pbac-only.ts:8-40` (FOCUS) — seeds organization data.

7. **`packages/trpc/`** — tRPC API routers: `EventTypeGroupFilter` (`packages/trpc/server/routers/viewer/eventTypes/utils/EventTypeGroupFilter.ts`, 124 lines, INDEX line 33).

8. **Additional packages** (TREE "+4"): `packages/dayjs/`, `packages/debugging/`, `packages/emails/`, `packages/i18n/`, `packages/kysely/` are listed but not elaborated in FOCUS.

### Other Top-Level Directories

- **`example-apps/credential-sync/`** (7 files, TREE) — a credential-sync example app.
- **`scripts/`** (9 files, TREE) — including `scripts/pull-coss-ui-components.ts:217-259` (FOCUS) which calls `processComponent`, `resolvePaths`, confirming shared UI component syncing.
- **Root config files**: `checkly.config.ts`, `playwright.config.ts`, `setupVitest.ts`, `vitest.workspace.ts` (TREE) — E2E and unit test infrastructure.

### GAPS — What Cannot Be Determined

The GAPS section states:
- **Type**: STRUCTURAL (answerable from L0-L2)
- **Coverage**: 80 symbols in L3, 23 with behavior annotations
- **Uncovered symbols**: `GoogleCalError`, `IWipeMyCalAction`, `IWipeMyCalActionButtonProps`, `ListEventTypesPlatformWrapperProps`

This means:
- The internal structure of `GoogleCalError` and how Google Calendar errors are handled cannot be determined.
- The "Wipe My Cal" action feature (`IWipeMyCalAction`, `IWipeMyCalActionButtonProps`) is not described — its placement and behavior are unknown.
- `ListEventTypesPlatformWrapperProps` is uncovered, so the full props interface for listing event types in the platform atom layer is unknown.
- The TREE "+4" and "+4" unnamed packages and the "5063 more modules" / "11280 more symbols" are not enumerated.

### Synthesis

Cal.diy is a **monorepo** with two main structural tiers:

1. **Runtime applications** (`apps/`): three deployable units — `api/` (versioned platform API with NestJS-style services), `web/` (React front-end consuming platform atoms), and `docs/`.

2. **Shared packages** (`packages/`): a library layer with clear domain separation:
   - **`embeds/`**: client-side embed SDK (`Cal`, `CalApi`, iframe management)
   - **`lib/`**: core domain services (`CalendarService`, error hierarchies, logging)
   - **`features/`**: domain feature modules (tasker, webhooks, booking-audit, cache, watchlist, embed codes, cal-video settings, selected calendars)
   - **`platform/`**: externally publishable atoms, versioned types, and permission utilities — with npm publish scripts
   - **`app-store/`**: third-party integration adapters (Zoho Bigin, ICS feed, Office 365)
   - **`prisma/`**: database schema and seeds
   - **`trpc/`**: tRPC server routers

The platform layer (`packages/platform/`) is notable for its npm-publishable design (pre/post-publish scripts, versioned type namespaces like `event-types_2024_06_14`), its React atom components (`BookerPlatformWrapperComponent`, `CalendarViewPlatformWrapperComponent`, `BaseCalProvider`), and its permissions system (`hasPermission` in both enums and utils). The web app consumes these atoms via wrapper types like `WrappedBookerPropsForPlatform`.
