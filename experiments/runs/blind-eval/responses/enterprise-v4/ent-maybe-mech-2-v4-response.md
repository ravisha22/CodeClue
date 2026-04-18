# Enterprise v4 (full-stack): ent-maybe-mech-2
Date: 2026-04-18

## Answer
The self-hosting update path is manual and image-based. The documented image source is `ghcr.io/maybe-finance/maybe`, using the `latest` or `stable` tags, and the prompt explicitly notes that a self-hosted deployment does not auto-update by default. To update, the documented sequence is `docker compose pull`, then `docker compose build`, then `docker compose up --no-deps -d web worker` so only the app services are refreshed. The same guide also documents a first-start recovery path for `ActiveRecord::DatabaseConnectionError`: run `docker compose down`, remove the `maybe_postgres-data` volume, and start again with `docker compose up`. That recovery flow makes the initial database state disposable when the first boot gets wedged.

## Synthesis
Maybe self-hosting updates are explicit pull/build/restart steps, and first-time database failures are recovered by tearing down and recreating the local Postgres volume.
