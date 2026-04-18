# Enterprise v4 (full-stack): ent-calcom-rel-1
Date: 2026-04-18

## Answer
The prompt’s scheduling and booking context shows a multi-stage handoff from routing to booking. The headless router is entered with a `formId` and submitted field values encoded in the URL, then it validates required fields and field types before deciding how to route. For the `eventTypeRedirect` case, it evaluates the routing rules, finds the matching team members, and redirects the user to the booking surface with `routedTeamMemberIds` attached. From there the booking page narrows availability to those matched members, slot selection temporarily blocks the chosen slot, and the final confirmation step rechecks availability rules before the system emits follow-on effects like emails and webhooks.

## Synthesis
That means the router is not just a redirect helper: it is the policy gate that determines who is bookable, and the downstream booking flow carries that routing result all the way through slot locking and final side effects.
