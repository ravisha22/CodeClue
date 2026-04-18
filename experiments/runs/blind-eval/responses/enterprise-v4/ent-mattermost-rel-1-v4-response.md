# Enterprise v4 (full-stack): ent-mattermost-rel-1
Date: 2026-04-18

## Answer
The API relationship is permission-driven all the way down. Creating a team requires an authenticated caller with the `create_team` permission. Team visibility is broader than team creation, but still permission-sensitive: regular users only get open teams from the all-teams listing, while `manage_system` expands that view to all teams. Channel creation is then anchored to a team via required `team_id`, and the permission branches by channel type: public channels need `create_public_channel`, private channels need `create_private_channel`. Direct-message creation is even more specific: one of the two users must be involved and the caller needs `create_direct_channel`, unless the caller has `manage_system`, which overrides those narrower constraints.

## Synthesis
So team/channel creation and discovery line up as a hierarchy of auth + scope + type-specific permissions, with `manage_system` acting as the admin override across the flow.
