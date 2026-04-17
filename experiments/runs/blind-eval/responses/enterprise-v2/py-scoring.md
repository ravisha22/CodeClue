### ent-saleor-struct-1 (1/4)
- F1: MISS — Describes GraphQL infrastructure, but never states Saleor is GraphQL-only or API-only.
- F2: MISS — Never mentions the dashboard being decoupled into a separate repository.
- F3: COVERED — Describes channel-aware behavior and per-channel controls, especially around pricing and channel-scoped operations.
- F4: MISS — Mentions apps and webhooks, but omits subscription queries, API extensions, and dashboard iframes.

### ent-saleor-struct-2 (3/4)
- F1: COVERED — Describes Django app-style module structure with per-app directories, migrations, management commands, models, and related files.
- F2: COVERED — Explicitly says the API layer lives under `saleor/graphql/`.
- F3: COVERED — Identifies common GraphQL module contents including `schema.py`, `types.py`, `filters.py`, dataloaders, and mutations.
- F4: MISS — Does not identify the `queries`/`mutations` test split or the one-file-per-operation convention.

### ent-saleor-rel-1 (1/4)
- F1: COVERED — Explicitly describes `permission_required` decorators guarding query resolvers.
- F2: MISS — Never states mutation permissions are declared in `Meta.permissions`.
- F3: MISS — Does not describe `AuthorizationFilters` as function-based permission checks.
- F4: MISS — Mentions `PermissionDenied`, but not the requirement to state needed permissions in the error and GraphQL description.

### ent-saleor-rel-2 (0/4)
- F1: MISS — Does not state that removing or renaming a GraphQL schema field is a breaking change.
- F2: MISS — Does not state that removing or renaming a webhook payload field is a breaking change.
- F3: MISS — Does not mention `PluginsManager` signature changes as a breaking change.
- F4: MISS — Does not describe deprecate-before-removal policy or the `PREVIEW_FEATURE` exception.

### ent-saleor-mech-1 (0/4)
- F1: MISS — Explicitly says the scheduling trigger cannot be determined and never identifies Celery Beat.
- F2: MISS — Never states the feature depends on task queue configuration.
- F3: MISS — Does not mention `uv run poe worker`.
- F4: MISS — Does not mention `uv run poe scheduler`.

### ent-saleor-mech-2 (2/4)
- F1: COVERED — Describes `select_for_update()`-style locking on querysets to prevent races.
- F2: MISS — Does not mention consistent lock ordering by primary key.
- F3: MISS — Does not mention defined lock order across models such as `Order` before `OrderLine`.
- F4: COVERED — Identifies `lock_objects.py` helpers living alongside app models.

### ent-netbox-struct-1 (3/4)
- F1: COVERED — Clearly frames NetBox as a source-of-truth / authoritative system rather than a tool that directly acts on network nodes.
- F2: MISS — Does not describe the recommended architecture where other tools handle monitoring, assurance, and execution around NetBox.
- F3: COVERED — Enumerates a broad infrastructure data scope including circuits, racks, devices, cables, IPAM, tenancy, and related domains.
- F4: COVERED — Explicitly describes programmable REST and GraphQL APIs used for automation and integration.

### ent-netbox-struct-2 (1/4)
- F1: COVERED — Describes plugins as Django-app-style extensions that add URLs, template content, API views, and related resources.
- F2: MISS — Keeps plugin URLs separate, but does not clearly state the documented `/plugins` boundary plus the full list of prohibited core modifications.
- F3: MISS — Mentions plugin versioning generally, but not min/max NetBox compatibility declarations.
- F4: MISS — Does not mention `PLUGINS_CONFIG` in `configuration.py`.

### ent-netbox-rel-1 (2/4)
- F1: COVERED — Correctly describes tenancy as associating resources with organizational tenants.
- F2: MISS — Describes only a simple tenant/group hierarchy, not recursive tenant groups or optional group membership.
- F3: MISS — Does not clearly state the one-tenant-per-object model across the listed core object types.
- F4: COVERED — Explicitly distinguishes ownership/responsibility from tenancy.

### ent-netbox-rel-2 (0/4)
- F1: MISS — Mentions object-level permissions generally, but not the object-type/users-groups/actions/JSON-constraints model.
- F2: MISS — Does not clearly state default permissions auto-apply to authenticated users.
- F3: MISS — Does not mention `EXEMPT_VIEW_PERMISSIONS` or anonymous viewing.
- F4: MISS — Describes token auth, but not GraphQL parity or LDAP/SSO support.

### ent-netbox-mech-1 (2/4)
- F1: COVERED — Covers custom scripts and housekeeping, and partially situates remote-data jobs in the background-job system.
- F2: MISS — Describes Job/RQ execution generally, but not plugin-added jobs specifically or `rqworker` processes by name.
- F3: COVERED — Describes deferred scheduling and `enqueue_once()` duplicate prevention, covering most of the scheduling fact.
- F4: MISS — Does not mention `system_job()`, the default `high/default/low` queues, or dedicated workers for custom queues.

### ent-netbox-mech-2 (2/4)
- F1: COVERED — Describes monitored changes being queued asynchronously so the user request can finish immediately.
- F2: COVERED — Describes queued events/webhooks being processed asynchronously by background workers.
- F3: MISS — Does not describe Jinja2 payload templating or the full webhook context fields.
- F4: MISS — Does not mention 2XX success semantics, manual requeue, or `webhook_receiver`.

## Summary by repo
| repo | covered | total | % |
|---|---:|---:|---:|
| saleor | 7 | 24 | 29.2% |
| netbox | 10 | 24 | 41.7% |

## Summary by type
| type | covered | total | % |
|---|---:|---:|---:|
| structural | 8 | 16 | 50.0% |
| relational | 3 | 16 | 18.8% |
| mechanistic | 6 | 16 | 37.5% |
