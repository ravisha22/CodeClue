# Enterprise v4 (full-stack): ent-supabase-rel-2
Date: 2026-04-18

## Answer
The project-transfer flow in the prompt is built as a preview-then-transfer workflow, which already suggests that ownership alone is not enough. A project can move between organizations, but the source-side requirement is that you own the current organization and the destination-side requirement is that you are already a member of the target organization. Even when those identity checks pass, platform metadata can still constrain the transfer. Existing integrations or other project configuration can also block the move. So project ownership transfer in Supabase is conditional on both org relationships and project state, not just on clicking a button.

## Synthesis
Supabase allows project transfers across orgs, but only when source ownership, target membership, and the project’s integration/metadata state all allow it.
