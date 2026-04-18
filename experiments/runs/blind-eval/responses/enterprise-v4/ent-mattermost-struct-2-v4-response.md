# Enterprise v4 (full-stack): ent-mattermost-struct-2
Date: 2026-04-18

## Answer
The README and API-doc tooling together show a broad integration surface paired with a formal documentation pipeline. Mattermost says integrations can be built through APIs, webhooks, slash commands, Apps, and plugins. The API reference itself is generated around the OpenAPI standard and rendered with ReDoc. Its source-of-truth files live as YAML under `api/v4/source`, and the build process is not limited to local files: Playbooks API definitions are pulled from GitHub at build time and then merged into the final YAML artifact.

## Synthesis
That means Mattermost treats integrations as a first-class product surface, and it documents that surface through a reproducible OpenAPI/YAML build chain rather than ad hoc prose alone.
