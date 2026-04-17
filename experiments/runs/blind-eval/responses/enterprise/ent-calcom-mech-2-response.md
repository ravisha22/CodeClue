# Enterprise Eval: ent-calcom-mech-2
Date: 2026-04-17

## Question
How is the platform example app wired to Cal.diy's API v2 for local OAuth testing?

## Reasoning Scaffold

### Relevant Symbols Identification

The question targets the platform example app's connection to the API v2 OAuth system. I trace through TREE structure, OAuth-related FOCUS entries, and the API v2 service layer.

### 1. Repository Structure — Example Apps

**TREE section**:
- `example-apps/` (7 files) contains `credential-sync/`
- `apps/api/` contains the API v2 runtime

The `example-apps/credential-sync/` directory is the only example app visible in the TREE. Its name suggests it demonstrates credential synchronization — a key part of OAuth integration.

### 2. OAuth Client Infrastructure in API v2

**OAuthCalendarApp** (`apps/api/v2/src/platform/calendars/calendars.interface.ts:25-28`, FOCUS):
- Interface extending `CalendarApp`
- Methods: `connect`
- This defines the contract for OAuth-based calendar apps in the platform.

**OAuthCalendarApp.connect** (`calendars.interface.ts:27`, FOCUS):
- Signature: `connect(authorization: string, req: Request)`
- The `authorization` parameter and `Request` object suggest this handles the OAuth callback/connection flow in the API.

**OAuthClientRepository.deleteOAuthClient** (`apps/api/v2/src/modules/oauth-clients/oauth-client.repository.ts:93-97`, FOCUS):
- Delegates to `this.dbWrite.prisma.platformOAuthClient.delete`
- Operates on the `platformOAuthClient` Prisma model.

**OAuthClientRepository.getByOrgId** (`oauth-client.repository.ts:123-130`, FOCUS):
- Delegates to `this.dbRead.prisma.platformOAuthClient.findMany`
- Reads OAuth clients scoped to an organization, using a read-replica database (`this.dbRead`).

These two repository methods reveal the API v2 module path: `apps/api/v2/src/modules/oauth-clients/` — a dedicated NestJS module for managing OAuth clients.

### 3. Platform OAuth Client Repository (Feature Package)

**PlatformOAuthClientRepository** (`packages/features/platform-oauth-client/platform-oauth-client.repository.ts:6-24`, FOCUS):
- Methods: `getByUserId`
- Uses: `prisma.platformOAuthClient.findFirst`

**PlatformOAuthClientRepository.getByUserId** (`platform-oauth-client.repository.ts:8-23`, FOCUS):
- Signature: `getByUserId(userId: number)`
- Behavior: `DELEGATE(prisma.platformOAuthClient.findFirst -> result)`
- Looks up an OAuth client associated with a user.

This is in the **shared packages** (`packages/features/`), separate from the API v2 module's `OAuthClientRepository`. The shared repository uses direct `prisma` access, while the API v2 repository uses `dbRead`/`dbWrite` split — indicating a read/write replica pattern in the API layer.

### 4. Platform Bookings and OAuth Wiring

**PlatformBookingsService.getOAuthClientParams** (`apps/api/v2/src/platform/bookings/shared/platform-bookings.service.ts:36-62`, FOCUS):
- Behavior: `PRECEDENCE(eventType -> not_oAuthClient)`
- Uses: `this.eventTypesRepository.getEventTypeById`, `this.oAuthClientRepository.getByUserId`, `eventType.userId`, `this.oAuthClientRepository.getByTeamId`
- This method resolves OAuth client parameters for a booking:
  1. Fetches the event type by ID
  2. Looks up OAuth client by the event type's user ID
  3. Falls back to team-based OAuth client lookup (`getByTeamId`)
  4. The PRECEDENCE annotation shows: event type is checked first, then OAuth client presence

### 5. E2E Test Fixture for OAuth Client Creation

**createOAuthClient** (`apps/api/v2/src/platform/bookings/2024-08-13/controllers/e2e/update-booking-location.e2e-spec.ts:722-735`, FOCUS):
- Signature: `createOAuthClient(organizationId: number)`
- Behavior: `DELEGATE(oauthClientRepositoryFixture.create -> result)`
- Called by: `setupTestData`
- This test fixture creates an OAuth client for a given organization during E2E tests. The `oauthClientRepositoryFixture.create` call shows a test helper pattern for setting up OAuth clients.

### 6. Platform OAuth Client DTO

**PlatformOAuthClientDto** (`packages/platform/types/oauth-clients/outputs/oauth-client.output.ts:7-79`, FOCUS):
- Uses: `Object.keys`, `example.com`, `logo.png`
- This DTO defines the output shape of an OAuth client, with example values suggesting documentation/test defaults (`example.com`, `logo.png`).

### 7. Conferencing OAuth Integration

**ConferencingService.connectUserNonOauthApp** (`apps/api/v2/src/modules/conferencing/services/conferencing.service.ts:45-53`, FOCUS):
- Behavior: `DISPATCH(app)`
- Uses: `this.googleMeetService.connectGoogleMeetToUser`
- Dispatches on the app type to connect conferencing services. Google Meet is explicitly handled.

### 8. Workspace Platform Test Helper

**createWorkspacePlatform** (`apps/web/app/api/cron/selected-calendars/__tests__/cron.test.ts:61`, FOCUS):
- Signature: `createWorkspacePlatform({ id = 1 }: WorkspacePlatformParams = {})`
- A test helper for creating a workspace platform configuration.

### 9. Embed and Platform Atom Integration

**CalApi.init** (`packages/embeds/embed-core/src/embed.ts:862-883`, FOCUS):
- Uses `this.cal.__config.calOrigin` — the embed system uses a configurable origin, which would point to the local API v2 during development.

**getCalApi** (`packages/embeds/embed-react/src/index.ts:15-22`, FOCUS):
- Signature: `getCalApi(embedJsUrl: string)`
- Accepts an embed JS URL, enabling local development pointing.

**getArgumentForGetCalApi** (`packages/features/embed/lib/EmbedCodes.tsx:346-351`, FOCUS):
- Signature: `getArgumentForGetCalApi(namespace: string)`
- Generates arguments for `getCalApi` calls.

**AppListCardPlatformWrapper** (`packages/platform/atoms/connect/conferencing-apps/AppListCardPlatformWrapper.tsx:3-7`, FOCUS):
- Uses: `app.cal.com$`, `props.logo`
- The `app.cal.com$` pattern (regex anchor) suggests conditional behavior based on whether the app origin matches Cal.com.

### 10. Local App Metadata

**getLocalAppMetadata** (`packages/app-store/utils.ts:109-112`, FOCUS):
- This function retrieves local app metadata — relevant for local development where apps are loaded from the local filesystem rather than a remote registry.

**AppHandler** (`packages/types/AppHandler.d.ts:24`, FOCUS):
- Type alias: `AppDeclarativeHandler | NextApiHandler`
- The dual handler type supports both declarative app definitions and Next.js API routes.

### GAPS — What Cannot Be Determined

The GAPS section states:
- **Type**: STRUCTURAL (answerable from L0-L2)
- **Coverage**: 80 symbols in L3, 18 with behavior annotations
- **Uncovered symbols**:
  - `CredentialSyncCalendarApp.save` — the save method for the credential sync example app's calendar integration
  - `ICSFeedCalendarApp.check` — ICS feed calendar validation
  - `InputEventTypesService_2024_06_14.transformInputCalVideoSettings` — Cal Video settings transformation
  - `CalVideoOutputService` — Cal Video output service

The following **cannot be determined** from the clue:
1. **The actual wiring configuration** of the example app — no `.env`, `config.ts`, or setup script content is shown. How the example app's OAuth client ID/secret are configured for local use is unknown.
2. **`CredentialSyncCalendarApp.save`** — the save mechanism in the credential-sync example app is uncovered, which is directly relevant to understanding how credentials flow.
3. **The OAuth authorization flow steps** — redirect URIs, token exchange endpoints, callback handling within the example app itself.
4. **Docker/dev server configuration** — whether the API v2 runs locally alongside the example app, and on what ports.

### Synthesis

Based on the available evidence, the platform example app's wiring to API v2 for local OAuth testing involves the following architecture:

**1. Example App** (`example-apps/credential-sync/`, TREE):
The only example app in the repository is `credential-sync`, which — based on its name and the presence of `CredentialSyncCalendarApp.save` in GAPS — handles syncing OAuth credentials between the platform and calendar integrations.

**2. API v2 OAuth Module** (`apps/api/v2/src/modules/oauth-clients/`):
- `OAuthClientRepository` manages `platformOAuthClient` records via Prisma with read/write replica separation (`dbRead`/`dbWrite`).
- `deleteOAuthClient` and `getByOrgId` confirm CRUD operations scoped to organizations.

**3. Platform OAuth Client Model** (shared):
- `PlatformOAuthClientRepository` in `packages/features/` provides user-level OAuth client lookup.
- `PlatformOAuthClientDto` defines the output shape with example defaults.

**4. Booking-OAuth Integration**:
- `PlatformBookingsService.getOAuthClientParams` resolves which OAuth client applies to a booking by checking the event type's user, then falling back to team-level lookup.

**5. E2E Test Pattern**:
- `createOAuthClient(organizationId)` in E2E tests creates OAuth clients via `oauthClientRepositoryFixture.create`, establishing the pattern: create an org → create an OAuth client for that org → use it in platform API calls.

**6. Calendar OAuth Connection**:
- `OAuthCalendarApp.connect(authorization, req)` handles the OAuth callback for calendar apps via the API v2 platform layer.

**Supported conclusion:** The platform example app (`credential-sync`) connects to API v2's OAuth infrastructure through the `platformOAuthClient` Prisma model. OAuth clients are organization-scoped (created via `OAuthClientRepository.getByOrgId`), and the platform services resolve them per-booking via `PlatformBookingsService.getOAuthClientParams`. The embed system's configurable `calOrigin` (`CalApi.init`) enables pointing to a local API v2 instance.

**Unresolved:** The specific configuration mechanism (environment variables, config files) that wires the example app to a local API v2 instance, the credential sync flow's `save` implementation, and the redirect URI / token exchange details are all outside the clue's coverage.
