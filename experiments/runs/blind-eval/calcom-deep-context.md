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
