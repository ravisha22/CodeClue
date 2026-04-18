# Enterprise v4 (full-stack): ent-mattermost-mech-1
Date: 2026-04-18

## Answer
The incoming-webhook admin path spans channel targeting, actor scope, and permission scope. Creation starts with a required `channel_id`, because an incoming webhook is always attached to a channel. That target is constrained to a public channel or private group, and `channel_locked` decides whether the webhook remains pinned to that channel instead of allowing per-request overrides. If the webhook is being created on behalf of another user, the caller needs `manage_others_incoming_webhooks` in addition to the normal team-level `manage_webhooks` capability. After creation, the same manage-webhooks capability governs listing, fetching, updating, and deleting at system, team, or channel scope, and the listing APIs can be narrowed by `team_id`.

## Synthesis
So the mechanism is: bind webhook to a valid channel, enforce extra privilege for acting on someone else’s behalf, then reuse scoped `manage_webhooks` checks for the rest of the lifecycle.
