# Enterprise v4 (full-stack): ent-supabase-struct-2
Date: 2026-04-18

## Answer
The branch-related prompt material shows that Supabase treats branches as separate operational environments, not as lightweight labels on one shared instance. Each branch creates its own Supabase environment with its own instance and API credentials, which is why the branch UI works through branch-specific clients and permissions. Preview branches are ephemeral: they can be paused or deleted after inactivity or when the related pull request is merged or closed. Persistent branches are the opposite case—they are long-lived and meant for staging, QA, or development environments. So isolation comes from separate branch-scoped resources and credentials, both from the main project and from other branches.

## Synthesis
Supabase branches are isolated environments with their own instances, credentials, and lifecycle rules, not just alternate names for the main project.
