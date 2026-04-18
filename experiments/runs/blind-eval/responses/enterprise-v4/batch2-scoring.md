# Enterprise v4 scoring (batch2)
Date: 2026-04-18

## Comparison
| version | score |
|---|---:|
| v4 (full-stack) | 72/72 |

## Per-task

### ent-grafana-struct-1 (4/4)
- F1: COVERED — Response explicitly covers: Grafana separates server administrator permissions from organization permissions; server admins manage server-wide settings and resources while org permissions manage organization-scoped resources.
- F2: COVERED — Response explicitly covers: Organization roles are Viewer, Editor, and Admin, and the Basic Role has no permissions until RBAC adds them.
- F3: COVERED — Response explicitly covers: Dashboard and folder permissions are narrower than org permissions and can override them for a selected dashboard or folder.
- F4: COVERED — Response explicitly covers: Grafana Enterprise adds data source permissions and role-based access control for finer-grained read/write access to Grafana resources.

### ent-grafana-struct-2 (4/4)
- F1: COVERED — Response explicitly covers: Grafana supports three plugin types: panel, data source, and app plugins.
- F2: COVERED — Response explicitly covers: App plugins can bundle data sources, panels, dashboards, and Grafana pages into one experience.
- F3: COVERED — Response explicitly covers: The plugin catalog is available to Grafana Server Administrators and Organization Administrators.
- F4: COVERED — Response explicitly covers: Grafana uses plugin signatures and the Plugin Frontend Sandbox to verify integrity and isolate plugin code.

### ent-grafana-rel-1 (4/4)
- F1: COVERED — Response explicitly covers: Every Grafana user belongs to at least one organization.
- F2: COVERED — Response explicitly covers: Teams exist inside an organization, can contain multiple users, and can have Member or Admin roles.
- F3: COVERED — Response explicitly covers: Organization permissions cover dashboards, folders, alerts, data sources, plugins, teams, service accounts, and other org resources.
- F4: COVERED — Response explicitly covers: Dashboard and folder permissions take precedence over organization permissions for the selected entity.

### ent-grafana-rel-2 (4/4)
- F1: COVERED — Response explicitly covers: A data source's query editor is used from dashboard panels and Explore.
- F2: COVERED — Response explicitly covers: After configuration, a data source can feed dashboards, Explore queries, and alert rules.
- F3: COVERED — Response explicitly covers: The Mixed data source lets one panel query multiple data sources at once.
- F4: COVERED — Response explicitly covers: The Dashboard data source reuses another panel's result set or annotations from the same dashboard.

### ent-grafana-mech-1 (4/4)
- F1: COVERED — Response explicitly covers: Only organization administrators can add or remove data sources, and they do it through the Configuration or Data Sources area.
- F2: COVERED — Response explicitly covers: To add a data source, Grafana has you open Connections, search for the source, and then configure it with source-specific instructions.
- F3: COVERED — Response explicitly covers: Each data source has a query editor whose UI can vary by source and may include autocomplete, metric suggestions, or visual query building.
- F4: COVERED — Response explicitly covers: Grafana also ships built-in core data sources and supports additional data source plugins or custom plugins.

### ent-grafana-mech-2 (4/4)
- F1: COVERED — Response explicitly covers: Grafana can provision alert rules, contact points, notification policies, mute timings, and templates.
- F2: COVERED — Response explicitly covers: Provisioning is available through files on disk, Terraform, or the Alerting provisioning HTTP API.
- F3: COVERED — Response explicitly covers: Imported alerting resources are not editable in the UI the same way as manual resources, and file provisioning is not available in Grafana Cloud.
- F4: COVERED — Response explicitly covers: The Alerting provisioning HTTP API manages Grafana-managed alerts, while data-source-managed alerts need Mimir or Cortex tooling.

### ent-maybe-struct-1 (4/4)
- F1: COVERED — Response explicitly covers: Maybe is described as a personal finance app for everyone and a fully working application.
- F2: COVERED — Response explicitly covers: The repository explicitly documents Docker-based self-hosting in `docs/hosting/docker.md`.
- F3: COVERED — Response explicitly covers: The README separates self-hosting users from developers and points self-hosters to the Docker guide instead of the local development steps.
- F4: COVERED — Response explicitly covers: The documented API surface includes an AI chat API under `/api/v1/chats`.

### ent-maybe-struct-2 (4/4)
- F1: COVERED — Response explicitly covers: The Docker guide recommends first installing Docker Engine and verifying it with `docker run hello-world`.
- F2: COVERED — Response explicitly covers: The sample compose file is downloaded from the repository as `compose.yml` from `compose.example.yml`.
- F3: COVERED — Response explicitly covers: Optional environment configuration is done through a local `.env` file containing `SECRET_KEY_BASE` and `POSTGRES_PASSWORD`.
- F4: COVERED — Response explicitly covers: The documented runtime flow includes `docker compose up`, then `docker compose up -d` for background mode, with `docker compose ls` used to verify it is running.

### ent-maybe-rel-1 (4/4)
- F1: COVERED — Response explicitly covers: All chat endpoints require authentication via OAuth2 or API keys and also require `ai_enabled` to be true.
- F2: COVERED — Response explicitly covers: GET endpoints for listing chats and fetching a chat require the `read` scope.
- F3: COVERED — Response explicitly covers: Create, update, delete, create-message, and retry-message operations require the `write` scope.
- F4: COVERED — Response explicitly covers: The documented error model distinguishes unauthorized from forbidden, where forbidden covers insufficient permissions or AI not enabled.

### ent-maybe-rel-2 (4/4)
- F1: COVERED — Response explicitly covers: List Chats returns a `chats` array with chat metadata plus pagination fields including `page`, `per_page`, `total_count`, and `total_pages`.
- F2: COVERED — Response explicitly covers: Get Chat returns a `messages` array that can include both `user_message` and `assistant_message` records.
- F3: COVERED — Response explicitly covers: Assistant messages include a `model` field and a `tool_calls` array.
- F4: COVERED — Response explicitly covers: The docs say the AI assistant can make tool calls to access user financial data.

### ent-maybe-mech-1 (4/4)
- F1: COVERED — Response explicitly covers: `POST /api/v1/chats` accepts an optional title, an initial message, and an optional model, and it returns the same shape as Get Chat.
- F2: COVERED — Response explicitly covers: `POST /api/v1/chats/:chat_id/messages` returns the user message immediately with `ai_response_status` set to `pending`.
- F3: COVERED — Response explicitly covers: The API processes AI responses asynchronously in the background rather than blocking the create request.
- F4: COVERED — Response explicitly covers: Clients are told to poll the chat endpoint and look for new messages with `type` equal to `assistant_message`.

### ent-maybe-mech-2 (4/4)
- F1: COVERED — Response explicitly covers: The documented image source for self-hosting is `ghcr.io/maybe-finance/maybe` with `latest` and `stable` tags.
- F2: COVERED — Response explicitly covers: By default the self-hosted app does not update automatically.
- F3: COVERED — Response explicitly covers: The documented update sequence is `docker compose pull`, `docker compose build`, then `docker compose up --no-deps -d web worker`.
- F4: COVERED — Response explicitly covers: If the first start hits an `ActiveRecord::DatabaseConnectionError`, the guide recommends `docker compose down`, removing the `maybe_postgres-data` volume, and starting `docker compose up` again.

### ent-supabase-struct-1 (4/4)
- F1: COVERED — Response explicitly covers: A Supabase project includes Postgres, Studio, GoTrue/Auth, PostgREST/API, Realtime, Storage, Deno Edge Functions, postgres-meta, Supavisor, and Kong.
- F2: COVERED — Response explicitly covers: Kong is the API gateway in front of the core services.
- F3: COVERED — Response explicitly covers: Postgres is the core of Supabase and is not abstracted away; users can access it with full privileges.
- F4: COVERED — Response explicitly covers: Supavisor is described as a cloud-native, multi-tenant Postgres connection pooler.

### ent-supabase-struct-2 (4/4)
- F1: COVERED — Response explicitly covers: Supabase branches create separate environments with their own Supabase instance and API credentials.
- F2: COVERED — Response explicitly covers: Preview branches are ephemeral and can be paused or deleted after inactivity or when a pull request is merged or closed.
- F3: COVERED — Response explicitly covers: Persistent branches are long-lived and are recommended for staging, QA, or development environments.
- F4: COVERED — Response explicitly covers: Branches are isolated Supabase environments with their own credentials and branch-scoped resources, not just lightweight git labels.

### ent-supabase-rel-1 (4/4)
- F1: COVERED — Response explicitly covers: API keys authenticate an application component, while Supabase Auth identifies the user.
- F2: COVERED — Response explicitly covers: Publishable and anon keys are public-facing but rely on RLS and the `anon` and `authenticated` Postgres roles for row access.
- F3: COVERED — Response explicitly covers: Secret and `service_role` keys are backend-only and bypass RLS through the `service_role` Postgres role.
- F4: COVERED — Response explicitly covers: Supabase Auth JWTs can scope database access row by row when used with RLS policies.

### ent-supabase-rel-2 (4/4)
- F1: COVERED — Response explicitly covers: Projects can be transferred between different organizations.
- F2: COVERED — Response explicitly covers: The transfer requires ownership of the source organization and at least membership in the target organization.
- F3: COVERED — Response explicitly covers: Project transfers are constrained by platform-level project metadata, so ownership checks are necessary but not sufficient for every move.
- F4: COVERED — Response explicitly covers: Existing integrations or project configuration can block a transfer even when source ownership and target membership are satisfied.

### ent-supabase-mech-1 (4/4)
- F1: COVERED — Response explicitly covers: Realtime is a separate service layer that maintains client connections while coordinating with Postgres-backed change sources.
- F2: COVERED — Response explicitly covers: Database change streaming is one Realtime path, where subscribed Postgres changes are forwarded to connected clients.
- F3: COVERED — Response explicitly covers: Broadcast is a second Realtime path, where application-originated messages are fanned out to subscribed channels.
- F4: COVERED — Response explicitly covers: Private and broadcast flows are gated by authorization checks before messages are delivered to clients.

### ent-supabase-mech-2 (4/4)
- F1: COVERED — Response explicitly covers: Supabase Cron is a Postgres module for scheduling recurring jobs and monitoring job runs inside Postgres.
- F2: COVERED — Response explicitly covers: Jobs can be created via SQL or the Dashboard and can run from every second to once a year.
- F3: COVERED — Response explicitly covers: A cron job can run SQL snippets, database functions, or HTTP requests such as invoking a Supabase Edge Function.
- F4: COVERED — Response explicitly covers: The cron subsystem stores both scheduled job definitions and execution history inside its database-backed scheduler layer.

## Summary by repo
| repo | tasks | score |
|---|---:|---:|
| grafana | 6 | 24/24 |
| maybe | 6 | 24/24 |
| supabase | 6 | 24/24 |
| total | 18 | 72/72 |

## Summary by type
| type | tasks | score |
|---|---:|---:|
| structural | 6 | 24/24 |
| relational | 6 | 24/24 |
| mechanistic | 6 | 24/24 |
| total | 18 | 72/72 |

## Summary
The v4 batch covers all 72 gold facts across Grafana, Maybe, and Supabase because each response names the right components and also explains the relevant mechanism, boundary, or lifecycle from the prompt evidence instead of only restating the question.
