# Enterprise v4 (full-stack): ent-calcom-struct-1
Date: 2026-04-18

## Answer
The full-stack prompt describes Cal.diy as a monorepo scheduling platform whose main runtime is the Next.js web product backed by tRPC/React/Tailwind UI code and Prisma-driven persistence, with Daily.co in the documented stack as well. That core runtime is complemented by a separate `apps/api/v2` Nest.js service, so the newer external API is split from the web/tRPC application surface. The platform layer also reaches outside the main app: `packages/platform/atoms` is the embeddable UI package, and the prompt explicitly says it targets both React 18/19 and Next 14/15. The same platform area includes an example application used alongside the atoms package for local and backend integration testing.

## Synthesis
In short, Cal.diy is organized as a scheduling monorepo with three visible runtime tiers: the main web app, a distinct API v2 service, and reusable platform/embed packages backed by an example integration app.
