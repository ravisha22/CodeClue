# Enterprise Eval: ent-calcom-struct-2
Date: 2026-04-17

## Question
What enterprise capabilities does Cal.diy explicitly exclude compared with Cal.com?

## Reasoning Scaffold

### Approach
This question asks about *explicit exclusions* — features Cal.diy deliberately omits relative to Cal.com. The clue file is built from the Cal.diy (calcom) repository itself, so it can only show what *is present* in the codebase. To answer what is "excluded," I must look for:
1. References to Cal.com-specific services that appear as integration points but are gated or stubbed.
2. Naming patterns or guards that distinguish "platform" (Cal.diy) from "hosted" (Cal.com) behavior.
3. The GAPS section, which notes what is structurally uncovered.

### Evidence from the Clue File

#### 1. The codebase appears to be the *same* monorepo

The header `=CC v2.1 calcom@HEAD 5074mod 11723sym` names the repository as `calcom@HEAD`. The TREE shows a comprehensive monorepo with `apps/api/`, `apps/web/`, `apps/docs/`, plus extensive `packages/` (app-store, features, lib, prisma, platform, embeds, etc.). There is **no explicit marker in the clue file** that delineates "Cal.diy-only" vs "Cal.com-only" code paths.

#### 2. Cal.com domain references in the codebase

Several FOCUS entries reference `cal.com` domain names directly, suggesting the codebase serves Cal.com as well:

- `doWeNeedCalOriginProp` (`packages/features/embed/lib/EmbedCodes.tsx:7-12`, FOCUS) — `uses: app.cal.com`. This function checks whether a Cal origin property is needed, referencing `app.cal.com` as a baseline.
- `isSmsCalEmail` (`packages/lib/isSmsCalEmail.ts:1-3`, FOCUS) — `uses: email.endsWith, sms.cal.com`. This checks if an email ends with `sms.cal.com`, indicating SMS-to-email functionality tied to the Cal.com domain.
- `CloseCom` (`packages/lib/CloseCom.ts:194-487`, FOCUS) — `uses: api.close.com, close.com`. This is an integration with Close CRM, using the `close.com` API.
- `getCloseComCustomActivityTypeFieldsIds` (`packages/lib/CloseComeUtils.ts:151-193`, FOCUS) — CRM utility for Close.com.
- `AppListCardPlatformWrapper` (not in this clue but referenced patterns) — uses `app.cal.com$` pattern.
- `CAL_AI_PHONE_NUMBER_MONTHLY_PRICE` (`packages/lib/constants.ts:248-253`, FOCUS) — a pricing constant for Cal AI phone numbers, with behavior `DELEGATE(Number.isFinite -> result)`. This suggests a paid feature (AI phone numbers) whose pricing is defined in the codebase.

#### 3. Feature presence — what IS in the codebase

The clue shows the following enterprise-grade features are *present* in the repository:

- **Organization watchlists**: `OrganizationWatchlistOperationsService.checkPermission` (SYM, `packages/features/watchlist/`).
- **Booking audit**: `BookingAuditAccessService`, `BookingAuditPermissionError` (SYM, `packages/features/booking-audit/`).
- **Permission system**: `hasPermission` in `packages/platform/enums/permissions.ts` and `packages/platform/utils/permissions.ts` (SYM), `PermissionCheckService` in `WebhookRepository` (INDEX).
- **Webhooks with team-level permissions**: `WebhookRepository` (592 lines, INDEX) with `checkPermission`, `getTeamIdsWithPermission`.
- **Calendar delegation credentials**: Full error hierarchy — `CalendarAppDelegationCredentialError`, `CalendarAppDelegationCredentialConfigurationError`, `CalendarAppDelegationCredentialInvalidGrantError`, `CalendarAppDelegationCredentialClientIdNotAuthorizedError`, `CalendarAppDelegationCredentialNotSetupError` (SYM, `packages/lib/CalendarAppError.ts`).
- **Office 365 delegation**: `Office365CalendarService.triggerDelegationCredentialError` (SYM, `packages/app-store/office365calendar/`).
- **Cal Video settings**: `CalVideoSettingsRepository` (FOCUS) with recording control (`disableRecordingForGuests`, `disableRecordingForOrganizer`, `enableAutomaticRecordingForOrganizer`, `enableAutomaticTranscription`).
- **Cal AI phone pricing**: `CAL_AI_PHONE_NUMBER_MONTHLY_PRICE` (FOCUS).
- **Platform OAuth**: `PlatformOAuthClientRepository.getByUserId` (FOCUS).
- **CalComAdapter for auth**: `CalComAdapter` (`packages/features/auth/lib/next-auth-custom-adapter.ts:62-170`, FOCUS) — custom NextAuth adapter.

#### 4. What is NOT explicitly excluded

**The clue file does not contain any explicit exclusion markers, feature flags, or conditional compilation that distinguishes Cal.diy from Cal.com.** There are no:
- Feature-gating constants (e.g., `IS_CALCOM_HOSTED`, `ENTERPRISE_ONLY`).
- Conditional imports or lazy-loaded enterprise modules.
- License checks or plan-tier guards.

visible in the provided clue entries.

#### 5. The embed origin check as a possible differentiation point

`doWeNeedCalOriginProp` (`packages/features/embed/lib/EmbedCodes.tsx:7-12`, FOCUS) checks against `app.cal.com`, suggesting embed code generation may differ when the origin is *not* `app.cal.com` (i.e., a self-hosted or Cal.diy instance needs an explicit `calOrigin` prop). This is a *configuration* difference, not a feature exclusion.

### GAPS — What Cannot Be Determined

The GAPS section states:
- **Type**: STRUCTURAL (answerable from L0-L2)
- **Coverage**: 80 symbols in L3, 24 with behavior annotations
- **Uncovered symbols**: `Cal.log` (3 instances), `Cal.scrollByDistance`

Additionally:
- The clue only covers 80 of potentially thousands of L3 symbols. Feature-gating logic (e.g., environment variable checks, license validation, plan-tier guards) that would explicitly exclude enterprise capabilities may exist in the **11,280+ symbols and 5,063+ modules not shown**.
- No deployment configuration, environment variable definitions, or license files are included in the clue.
- The question references "Cal.diy" vs "Cal.com" but the clue file is from `calcom@HEAD` — it is **not possible to determine from this clue alone** whether Cal.diy is a separate fork, a deployment mode, or a branding variant of the same codebase.

### Synthesis

**Based solely on the clue file, Cal.diy does not *explicitly* exclude any enterprise capabilities compared with Cal.com.** The evidence shows:

1. **The codebase is unified**: The repository header is `calcom@HEAD` and contains the full monorepo structure with enterprise features (booking audit, organization watchlists, delegation credentials, permission systems, Cal AI pricing, video recording controls) all present in the code.

2. **Cal.com references are configuration, not exclusions**: References to `app.cal.com` and `sms.cal.com` appear in utility functions (`doWeNeedCalOriginProp`, `isSmsCalEmail`) that check domain-specific behavior, but these are runtime configuration checks, not feature gates that disable functionality.

3. **No exclusion evidence found**: The clue contains no feature flags, license gates, plan-tier checks, or conditional compilation that would indicate Cal.diy explicitly removes enterprise capabilities.

4. **Critical limitation**: The GAPS section and the truncated symbol/module lists (80 of 11,723 symbols shown) mean that explicit exclusion logic *could* exist in the uncovered portions of the codebase. The clue is insufficient to make a definitive claim that no exclusions exist — only that none are visible in the provided evidence.

The most that can be said is that `CAL_AI_PHONE_NUMBER_MONTHLY_PRICE` (`packages/lib/constants.ts:248-253`, FOCUS) implies a monetized feature that might be handled differently in a self-hosted context, and the `isSmsCalEmail` function's reliance on the `sms.cal.com` domain suggests SMS features are inherently tied to Cal.com infrastructure. But neither of these constitutes an *explicit exclusion* documented in the clue.
