# Enterprise v4 (full-stack): ent-calcom-struct-2
Date: 2026-04-18

## Answer
The README/clue framing is explicit that Cal.diy is the open-source community edition and is recommended only for personal, non-production self-hosting. Relative to Cal.com, the docs carve out a large enterprise-only surface: teams, team round-robin, team collective scheduling, managed event types, instant meeting, and organizations are presented as available in Cal.com but not in Cal.diy. The same exclusion pattern covers identity/admin and GTM features such as SAML SSO, SCIM directory sync, impersonation, workflows, routing forms, insights dashboard, attributes and segments, delegation, workspace platform, and the admin panel. Even with those cuts, the community edition still keeps meaningful scheduling and integration primitives, including event types, availability schedules, webhooks, Zapier, API v2, API keys, and platform or OAuth clients.

## Synthesis
So Cal.diy is not ‘featureless’; it preserves the core scheduling platform while intentionally excluding the team, enterprise identity, and operations/governance layers that differentiate Cal.com.
