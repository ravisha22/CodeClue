# Enterprise v2: ent-calcom-mech-2
Date: 2026-04-17

## Question
How is the platform example app wired to Cal.diy's API v2 for local OAuth testing?

## Answer

### Overview

The platform example app (`example-apps/credential-sync/`) is wired to Cal.diy's API v2 through the platform OAuth client infrastructure. The example app provides credential synchronization between external OAuth providers (Google, Zoom) and Cal.diy, connecting to the API v2 which runs as a separate service on port 5555 with its own database configuration and OAuth client management layer.

### Example App Structure and Configuration

The example app lives at `example-apps/credential-sync/` (TREE, `example-apps/`) containing 8 files. Its `.env.example` (FOCUS, `example-apps/credential-sync/.env.example:1-15`) configures:

- `CALCOM_TEST_USER_ID=1` — A hardcoded test user ID for local development
- `GOOGLE_REFRESH_TOKEN`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` — Google OAuth credentials
- `ZOOM_REFRESH_TOKEN`, `ZOOM_CLIENT_ID` — Zoom OAuth credentials

This shows the example app is designed for local OAuth testing with pre-provisioned test credentials for Google and Zoom integrations.

### API v2 as the OAuth Backend

The API v2 application (`apps/api/v2/`) runs as a separate service with its own configuration (FOCUS, `apps/api/v2/.env.example:1-76`):

- `NODE_ENV=development` — Development mode
- `API_PORT=5555` — Separate from the web app's port 3000
- `API_URL=http://localhost` — Local base URL
- `DATABASE_READ_URL` / `DATABASE_WRITE_URL` — Read/write database split pointing to PostgreSQL on port 5450
- `LOG_LEVEL=DEBUG` — Verbose logging for development

### Platform OAuth Client Infrastructure

The OAuth client management layer connects the example app to API v2:

1. **`PlatformOAuthClientRepository`** (FOCUS, `packages/features/platform-oauth-client/platform-oauth-client.repository.ts:6-24`) — Repository class with `getByUserId` as its primary method, using `prisma.platformOAuthClient.findFirst` (FOCUS, `PlatformOAuthClientRepository.getByUserId`, `packages/features/platform-oauth-client/platform-oauth-client.repository.ts:8-23`). This delegates OAuth client lookup to the Prisma database layer.

2. **`PlatformOAuthClientDto`** (FOCUS, `packages/platform/types/oauth-clients/outputs/oauth-client.output.ts:7-79`) — The DTO for OAuth clients, referencing `example.com` and `logo.png` as example values, confirming it's designed for platform OAuth client representation.

3. **`PlatformBookingsService.getOAuthClientParams`** (FOCUS, `apps/api/v2/src/platform/bookings/shared/platform-bookings.service.ts:36-62`) — Resolves OAuth client parameters for a given event type. Its behavior annotation `PRECEDENCE(eventType -> not_oAuthClient)` shows it first fetches the event type via `this.eventTypesRepository.getEventTypeById`, then looks up the OAuth client via `this.oAuthClientRepository.getByUserId` (using `eventType.userId`) or `this.oAuthClientRepository.getByTeamId`. This is the bridge between booking operations and the OAuth client that authorized them.

4. **`createWorkspacePlatform`** (FOCUS, `apps/web/app/api/cron/selected-calendars/__tests__/cron.test.ts:61`) — A test helper with signature `createWorkspacePlatform({ id = 1 })` that creates a workspace platform fixture, indicating test infrastructure for OAuth platform scenarios.

### OAuth Calendar App Interface

The `OAuthCalendarApp` interface (FOCUS, `apps/api/v2/src/platform/calendars/calendars.interface.ts:25-28`) extends `CalendarApp` and adds a `connect(authorization: string, req: Request)` method (FOCUS, `OAuthCalendarApp.connect`, `apps/api/v2/src/platform/calendars/calendars.interface.ts:27`). This defines the contract that calendar integrations (like Google Calendar) must implement for OAuth-based connection through the API v2 platform layer.

### Conferencing OAuth Integration

`ConferencingService.connectUserNonOauthApp` (FOCUS, `apps/api/v2/src/modules/conferencing/services/conferencing.service.ts:45-53`) has `DISPATCH(app)` behavior, dispatching on the app name and using `this.googleMeetService.connectGoogleMeetToUser`. This shows that conferencing apps can be connected through a non-OAuth path as well, with Google Meet as a specific case.

### Embed/Platform Layer

The platform atoms provide UI components that consume the OAuth-authenticated platform:

- `AppListCardPlatformWrapper` (FOCUS, `packages/platform/atoms/connect/conferencing-apps/AppListCardPlatformWrapper.tsx:3-7`) — Wraps app list cards, referencing `app.cal.com$` for logo resolution.
- `CalApi` (FOCUS, `packages/embeds/embed-core/src/embed.ts:847-1505`) with `CalApi.init` (FOCUS, `packages/embeds/embed-core/src/embed.ts:862-883`) — The embed SDK initializes with `calOrigin` configuration, which would point to the local API v2 URL during testing.
- `getCalApi` (FOCUS, `packages/embeds/embed-react/src/index.ts:15-22`) — React-specific Cal API getter accepting `embedJsUrl`.

### Wiring Summary

The local OAuth testing flow works as follows:

1. The **example app** (`example-apps/credential-sync/`) is configured with a test user ID (`CALCOM_TEST_USER_ID=1`) and OAuth credentials for Google/Zoom.
2. The **API v2** (`apps/api/v2/`) runs locally on port 5555 with a shared PostgreSQL database (port 5450).
3. The **`PlatformOAuthClientRepository`** stores and retrieves OAuth client registrations from the database, keyed by user ID.
4. When the example app performs credential sync, it communicates with API v2, which resolves the OAuth client via `PlatformBookingsService.getOAuthClientParams` and connects calendar/conferencing apps through the `OAuthCalendarApp.connect` interface.
5. The `CalendarsCacheService` entry shows a calendar-cache service with a `REDIS_CALENDARS_CACHE_KEY`, so some cache layer participates in this platform path, but the underlying cache implementation is not otherwise described in the clue (INDEX, `apps/api/v2/src/platform/calendars/services/calendars-cache.service.ts`).

### Gaps and Uncertainties

The GAPS section identifies this as a STRUCTURAL question with 82 symbols at L3 and 18 with behavior annotations. The following are uncovered (GAPS):

- `CredentialSyncCalendarApp.check` — The validation logic for credential sync calendar apps
- `CredentialSyncCalendarApp.save` — The persistence logic for synced credentials
- `ICSFeedCalendarApp.check` — ICS feed validation
- `InputEventTypesService_2024_06_14.transformInputCalVideoSettings` — Video settings transformation

The uncovering of `CredentialSyncCalendarApp.check` and `CredentialSyncCalendarApp.save` is significant because those names suggest important credential-sync logic, but their implementation details are not available from the clue. The exact HTTP endpoints the example app calls on API v2, and the exact token exchange sequence, are not visible.

### Synthesis

The platform example app is wired to API v2 through: (1) shared PostgreSQL database containing `platformOAuthClient` records, (2) pre-configured test credentials in `.env.example` with `CALCOM_TEST_USER_ID=1`, (3) `PlatformOAuthClientRepository` for client lookup, (4) `OAuthCalendarApp.connect` interface for calendar OAuth connections, and (5) `PlatformBookingsService.getOAuthClientParams` bridging event types to their authorizing OAuth clients. The exact credential-sync app logic (`CredentialSyncCalendarApp.check`/`.save`) is uncovered in the clue, leaving the implementation of the sync mechanism itself as a gap.
