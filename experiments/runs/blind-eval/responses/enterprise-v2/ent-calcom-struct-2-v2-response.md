# Enterprise v2: ent-calcom-struct-2
Date: 2026-04-17

## Question
What enterprise capabilities does Cal.diy explicitly exclude compared with Cal.com?

## Answer

### Positioning Statement

The README explicitly states: Cal.diy is "the open source community edition of Cal.com and it is intended for users who want..." (README). The README includes a section titled "What's different from Cal.com?" which directly addresses the divergence, though the clue only summarises the section headings, not the full prose (README, `sections: About Cal.diy, What's different from Cal.com?, Built With, Getting Started, Prerequisites`). A WARNING banner accompanies the README: "Use at your own risk" (README). This framing establishes Cal.diy as a self-hosted, community-oriented subset of the commercial Cal.com platform.

### Enterprise Capabilities Present in the Codebase (Structural Evidence)

Despite being positioned as a community edition, the clue reveals that the Cal.diy codebase **retains code artifacts** referencing enterprise-grade features. These may be structurally present but functionally disabled or excluded from the community runtime:

1. **Organization-level watchlist and permissions** — `OrganizationWatchlistOperationsService.checkPermission` (SYM, `packages/features/watchlist/lib/service/OrganizationWatchlistOperationsService.ts:48`) and `PermissionCheckService.checkPermission` (SYM, `packages/features/watchlist/lib/service/OrganizationWatchlistOperationsService.ts:19`) suggest organization-level governance features. The `hasPermission` utility exists in both `packages/platform/enums/permissions.ts:15` and `packages/platform/utils/permissions.ts:15` (SYM).

2. **Platform OAuth clients** — `PlatformOAuthClientRepository.getByUserId` (FOCUS, `packages/features/platform-oauth-client/platform-oauth-client.repository.ts:8-23`) suggests a platform-as-a-service OAuth client model, typically an enterprise/platform capability.

3. **SAML authentication** — The Docker Compose for PostgreSQL references a `cal-saml` environment value (FOCUS, `packages/prisma/docker-compose.yml:1-27`), indicating SAML SSO infrastructure is structurally present.

4. **PBAC (Policy-Based Access Control)** — A dedicated seed script `seed-pbac-only.ts` exists to populate organization-level PBAC data, referencing `result.organization.name` and `result.organization.slug` (FOCUS, `packages/prisma/seed-pbac-only.ts:8-40`).

5. **Insights/analytics database** — The root `.env.example` includes a separate `INSIGHTS_DATABASE_URL` (FOCUS, `.env.example:1-484`), suggesting an analytics tier that may be an enterprise feature.

6. **Booking audit trail** — `EnrichmentDataStore` in `packages/features/booking-audit/` with methods like `getAttendeeById`, `getCredentialById`, `getUserByUuid` (INDEX, `packages/features/booking-audit/lib/service/EnrichmentDataStore.ts`) indicates enterprise audit capabilities.

7. **Webhook permission system** — `WebhookRepository` (592L) includes `checkPermission`, `hasPermission`, `getTeamIdsWithPermission`, and a `PermissionCheckService` (INDEX, `packages/features/webhooks/lib/repository/WebhookRepository.ts`), suggesting granular webhook access control.

8. **CRM integrations** — `CrmService` for Zoho Bigin (INDEX, `packages/app-store/zoho-bigin/lib/CrmService.ts`) and `CloseCom` integration (FOCUS, `packages/lib/CloseCom.ts:194-487`) are enterprise CRM features.

9. **Cal Video with recording management** — `CalVideoSettingsRepository` with `disableRecordingForGuests`/`disableRecordingForOrganizer` (FOCUS, `packages/features/calVideoSettings/repositories/CalVideoSettingsRepository.ts:2-83`) and `deleteRecordings` scripts (FOCUS, `packages/app-store/dailyvideo/lib/scripts/deleteRecordings.ts:199-241`) indicate video recording infrastructure.

10. **AI phone capabilities** — `CAL_AI_PHONE_NUMBER_MONTHLY_PRICE` (FOCUS, `packages/lib/constants.ts:248-253`) references an AI phone number pricing constant, suggesting a paid AI feature.

11. **Calendar delegation credentials** — An extensive error hierarchy for delegation credentials (`CalendarAppDelegationCredentialError`, `CalendarAppDelegationCredentialConfigurationError`, `CalendarAppDelegationCredentialInvalidGrantError`, `CalendarAppDelegationCredentialClientIdNotAuthorizedError`, `CalendarAppDelegationCredentialNotSetupError`, SYM, `packages/lib/CalendarAppError.ts`) indicates a delegation model typical of enterprise calendar administration.

12. **Embed/platform distribution** — `CalApi` (FOCUS, `packages/embeds/embed-core/src/embed.ts:847-1505`) with namespace management, the embed iframe system (FOCUS, `packages/embeds/embed-core/src/embed-iframe.ts:521-612`), and platform atoms with pre/post-publish NPM scripts (FOCUS, `packages/platform/libraries/scripts/prepublish.js`, `postpublish.js`) suggest a white-label platform distribution capability.

### What Cannot Be Determined

The clue does **not** provide the full text of the "What's different from Cal.com?" README section, so the **explicit list of excluded enterprise features** as documented by the project maintainers is not available (README, section title only). The GAPS section confirms this is a STRUCTURAL question with 83 symbols at L3 coverage and 24 with behavior annotations. Symbols `Cal.log` and `Cal.scrollByDistance` are uncovered (GAPS).

Without the full README text or a feature-flag/license-gate mechanism visible in the clue, it is impossible to definitively distinguish which of the above features are:
- (a) fully functional in Cal.diy,
- (b) structurally present but runtime-gated behind Cal.com licensing, or
- (c) dead code in the community edition.

### Synthesis

The structural evidence shows Cal.diy shares the same monorepo codebase as Cal.com, with enterprise-grade infrastructure for SAML SSO, PBAC, organization watchlists, booking audits, CRM integrations, AI phone capabilities, calendar delegation, and platform OAuth all present as code artifacts. The README's "What's different from Cal.com?" section likely enumerates the runtime exclusions, but its content is not captured in the clue. The "Use at your own risk" warning and the "community edition" label indicate these enterprise capabilities are likely the boundary between Cal.diy and Cal.com — present in source but restricted in the community offering.
