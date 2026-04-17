### ent-saleor-struct-1 (1/4)
- F1: MISS — Describes GraphQL infrastructure, but never states Saleor is GraphQL-only or API-only.
- F2: MISS — Never mentions the dashboard being decoupled in a separate repository.
- F3: COVERED — Describes channel-aware behavior and per-channel controls across mutations/plugins/webhooks.
- F4: MISS — Mentions webhooks and apps, but omits subscription queries, API extensions, and dashboard iframes.

### ent-saleor-struct-2 (3/4)
- F1: COVERED — Describes Django app-style module structure with migrations, management commands, error codes, and related app files.
- F2: COVERED — Explicitly says the GraphQL layer lives under `saleor/graphql/`.
- F3: COVERED — Identifies common GraphQL module contents including `schema.py`, `types.py`, `filters.py`, dataloaders, and mutations.
- F4: MISS — Does not identify the `queries`/`mutations` test split or one-file-per-operation guidance.

### ent-saleor-rel-1 (1/4)
- F1: COVERED — Explicitly describes `permission_required` decorators guarding query resolvers.
- F2: MISS — Never states mutation permissions live in `Meta.permissions`.
- F3: MISS — Does not describe `AuthorizationFilters` as function-based permission checks.
- F4: MISS — Notes `PermissionDenied`, but not the requirement to state needed permissions in errors and GraphQL descriptions.

### ent-saleor-rel-2 (0/4)
- F1: MISS — Does not state that removing or renaming a GraphQL schema field is breaking.
- F2: MISS — Does not state that removing or renaming a webhook payload field is breaking.
- F3: MISS — Does not mention `PluginsManager` signature changes as a breaking change.
- F4: MISS — Does not describe deprecate-before-removal policy or the `PREVIEW_FEATURE` exception.

### ent-saleor-mech-1 (0/4)
- F1: MISS — Explicitly says the scheduling mechanism cannot be determined; never identifies Celery beat.
- F2: MISS — Never says the feature depends on task queue configuration.
- F3: MISS — Does not mention `uv run poe worker`.
- F4: MISS — Does not mention `uv run poe scheduler`.

### ent-saleor-mech-2 (2/4)
- F1: COVERED — Describes `select_for_update()` querysets inside transactions for locking.
- F2: MISS — Does not mention consistent lock ordering by primary key.
- F3: MISS — Does not mention defined lock order across models such as `Order` before `OrderLine`.
- F4: COVERED — Identifies `lock_objects.py` helpers living alongside app models.

### ent-netbox-struct-1 (3/4)
- F1: COVERED — Clearly frames NetBox as a source-of-truth system rather than a tool that talks directly to network nodes.
- F2: MISS — Does not describe the recommended architecture where other tools handle monitoring/assurance/execution around NetBox.
- F3: COVERED — Enumerates broad infrastructure domains including sites, racks, devices, circuits, VMs, IPAM, VLANs, VRFs, tenancy, and contacts.
- F4: COVERED — Explicitly describes programmable REST and GraphQL APIs driving automation use cases.

### ent-netbox-struct-2 (2/4)
- F1: MISS — Covers some plugin capabilities, but misses or contradicts key points like middleware/config support and complete extension surface.
- F2: COVERED — Describes plugin boundaries around core models/templates/settings with plugin URLs kept separate.
- F3: COVERED — Mentions version compatibility constraints for plugins.
- F4: MISS — Does not mention `PLUGINS_CONFIG` in `configuration.py`.

### ent-netbox-rel-1 (3/4)
- F1: COVERED — Correctly describes tenancy as associating objects to customers/internal organizations.
- F2: MISS — Describes only a simple group→tenant hierarchy, not recursive tenant groups or optional group membership.
- F3: COVERED — Describes broad tenant assignment across core object types.
- F4: COVERED — Explicitly distinguishes ownership/responsibility from tenancy.

### ent-netbox-rel-2 (1/4)
- F1: MISS — Mentions object-level permissions generally, but not the full object-types/users-groups/actions-JSON-constraints model.
- F2: MISS — Does not clearly state default permissions auto-apply to all authenticated users.
- F3: MISS — Does not mention `EXEMPT_VIEW_PERMISSIONS` or anonymous viewing.
- F4: COVERED — Describes token-based auth mapping API access to user accounts and permissions.

### ent-netbox-mech-1 (2/4)
- F1: COVERED — Covers custom scripts and housekeeping as background tasks.
- F2: MISS — Describes Job model and RQ workers, but not plugin-added jobs specifically.
- F3: COVERED — Describes immediate/future/repeating scheduling and `enqueue_once()` deduplication.
- F4: MISS — Mentions `system_job()`, but not default queue names or dedicated worker needs for custom queues.

### ent-netbox-mech-2 (2/4)
- F1: COVERED — Describes monitored changes being queued so the user request can finish immediately.
- F2: COVERED — Describes asynchronous worker processing of queued events/webhooks.
- F3: MISS — Does not describe Jinja2 payload templating or the full webhook context fields.
- F4: MISS — Does not mention 2XX success rule, manual requeue, or `webhook_receiver`.

### ent-calcom-struct-1 (3/4)
- F1: COVERED — Identifies the main scheduling app stack with tRPC, React, Prisma, and core platform pieces, covering most of the stack fact.
- F2: COVERED — Explicitly identifies `apps/api/v2` as a separate Nest.js-style service.
- F3: COVERED — Correctly identifies `packages/platform/atoms` as the embeddable UI component package.
- F4: MISS — Does not mention `packages/platform/examples/base` as the example app for testing atoms.

### ent-calcom-struct-2 (0/4)
- F1: MISS — Does not identify Cal.diy as the community edition recommended only for personal/non-production self-hosting.
- F2: MISS — Does not identify team/org features as Cal.com-only.
- F3: MISS — Does not identify enterprise features like SAML/SCIM/workflows/admin panel as Cal.com-only.
- F4: MISS — Does not identify the features Cal.diy still retains.

### ent-calcom-rel-1 (0/4)
- F1: MISS — Does not describe entering the router with `formId` and URL field values.
- F2: MISS — Does not describe field validation before route choice.
- F3: MISS — Does not describe `eventTypeRedirect`, matched team members, or `routedTeamMemberIds`.
- F4: MISS — Does not describe slot filtering/blocking/recheck and downstream emails/webhooks.

### ent-calcom-rel-2 (1/4)
- F1: COVERED — Lists many webhook triggers, covering more than half of the trigger set.
- F2: MISS — Does not identify the specific `BOOKING_CREATED` payload fields.
- F3: MISS — Does not identify cancellation/reschedule-specific payload fields.
- F4: MISS — Does not mention `X-Cal-Signature-256` or SHA-256 signing.

### ent-calcom-mech-1 (1/4)
- F1: COVERED — Correctly lists the `requiresCancellationReason` enum values.
- F2: MISS — Does not state the default is `MANDATORY_HOST_ONLY`, including null/no-eventType cases.
- F3: MISS — Does not identify `handleCancelBooking` as enforcing the rule.
- F4: MISS — Does not describe the UI threading plus required indicator behavior.

### ent-calcom-mech-2 (0/4)
- F1: MISS — Does not mention the root/example env variable mapping for platform OAuth client credentials.
- F2: MISS — Does not mention `yarn generate-secrets` or `.generated-secrets`.
- F3: MISS — Does not mention plaintext vs hashed OAuth2 secret handling.
- F4: MISS — Does not describe the localhost authorize redirect, token exchange, and reflected availability updates.

### ent-maybe-struct-1 (1/4)
- F1: COVERED — Identifies Maybe as a personal finance application with core finance features.
- F2: MISS — Explicitly says self-hosting docs/config are not present; never mentions `docs/hosting/docker.md`.
- F3: MISS — Does not identify README guidance separating self-hosters from developers.
- F4: MISS — Does not identify the `/api/v1/chats` AI chat API.

### ent-maybe-struct-2 (0/4)
- F1: MISS — No Docker Engine installation or `docker run hello-world` verification.
- F2: MISS — No mention of downloading `compose.yml` from `compose.example.yml`.
- F3: MISS — No mention of `.env` with `SECRET_KEY_BASE` and `POSTGRES_PASSWORD`.
- F4: MISS — No mention of `docker compose up`, detached mode, or `docker compose ls` verification.

### ent-maybe-rel-1 (0/4)
- F1: MISS — Does not describe auth via OAuth2/API keys plus `ai_enabled`.
- F2: MISS — Does not mention `read` scope for GET endpoints.
- F3: MISS — Does not mention `write` scope for create/update/delete/message operations.
- F4: MISS — Does not describe unauthorized vs forbidden semantics.

### ent-maybe-rel-2 (0/4)
- F1: MISS — Does not identify the `chats` array plus pagination fields.
- F2: MISS — Does not identify `messages` containing `user_message` and `assistant_message`.
- F3: MISS — Does not identify assistant `model` and `tool_calls` fields.
- F4: MISS — Does not state the assistant can make tool calls to access financial data.

### ent-maybe-mech-1 (0/4)
- F1: MISS — Does not describe `POST /api/v1/chats` request shape or response shape.
- F2: MISS — Does not mention immediate return with `ai_response_status` set to `pending`.
- F3: MISS — Does not state AI responses are processed asynchronously in the background.
- F4: MISS — Does not tell clients to poll chat and watch for `assistant_message` entries.

### ent-maybe-mech-2 (0/4)
- F1: MISS — Does not mention `ghcr.io/maybe-finance/maybe` or `latest`/`stable` tags.
- F2: MISS — Does not mention lack of automatic updates by default.
- F3: MISS — Does not mention the documented update command sequence.
- F4: MISS — Does not mention the documented `ActiveRecord::DatabaseConnectionError` recovery sequence.

## Summary by repo
| repo | covered | total | % |
|---|---:|---:|---:|
| saleor | 7 | 24 | 29.2% |
| netbox | 13 | 24 | 54.2% |
| calcom | 5 | 24 | 20.8% |
| maybe | 1 | 24 | 4.2% |

## Summary by type
| knowledge_type | covered | total | % |
|---|---:|---:|---:|
| structural | 13 | 32 | 40.6% |
| relational | 6 | 32 | 18.8% |
| mechanistic | 7 | 32 | 21.9% |
