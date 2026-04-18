### ent-saleor-struct-1 (2/4)
- F1: COVERED — Says Saleor is an "API-only GraphQL service" and anchors it to the README’s "Why API-only Architecture?" evidence.
- F2: MISS — No mention of the dashboard being a separate repository.
- F3: COVERED — Explains channels as first-class partitions for pricing/currencies/stock/publication with channel-aware plugin/mutation evidence.
- F4: MISS — Covers apps and webhooks, but not subscription queries, API extensions, or dashboard iframes.

### ent-saleor-struct-2 (3/4)
- F1: COVERED — Describes Django-style per-app layout with migrations, management commands, forms, and app-local files.
- F2: COVERED — Explicitly places the API under `saleor/graphql/`.
- F3: COVERED — Describes the recurring GraphQL module pattern (`schema.py`, `types.py`, `filters.py`, dataloaders, mutations) with evidence.
- F4: MISS — Does not establish the `queries`/`mutations` test-directory split or one-file-per-operation rule.

### ent-saleor-rel-1 (1/4)
- F1: COVERED — Explicitly identifies `permission_required` and query classes importing permission helpers.
- F2: MISS — Does not state mutation permissions live in `Meta.permissions`.
- F3: MISS — Does not explain `AuthorizationFilters` as function-based permission checks.
- F4: MISS — Mentions `PermissionDenied`, but not the policy about naming required permissions in errors/descriptions.

### ent-saleor-rel-2 (0/4)
- F1: MISS — Does not state that removing/renaming a GraphQL field is breaking.
- F2: MISS — Does not state that removing/renaming a webhook payload field is breaking.
- F3: MISS — Does not mention `PluginsManager` signature compatibility as a breaking-change rule.
- F4: MISS — Does not describe deprecate-before-removal or the `PREVIEW_FEATURE` exception.

### ent-saleor-mech-1 (0/4)
- F1: MISS — Describes indexing mechanics, but not Celery Beat triggering this task.
- F2: MISS — Does not state the feature fails without task queue configuration.
- F3: MISS — Does not mention `uv run poe worker`.
- F4: MISS — Does not mention `uv run poe scheduler`.

### ent-saleor-mech-2 (2/4)
- F1: COVERED — Uses `select_for_update()` + transactional locking as the central safety mechanism.
- F2: MISS — Does not provide the consistent primary-key lock-order rule.
- F3: MISS — Does not provide the cross-model ordering rule (`Order` before `OrderLine`).
- F4: COVERED — Explicitly points to app-local `lock_objects.py` helpers.

### ent-netbox-struct-1 (3/4)
- F1: COVERED — Frames NetBox as the system of record / source of truth rather than an execution tool.
- F2: MISS — Does not explicitly describe the recommended surrounding-tool architecture for monitoring/assurance/execution.
- F3: COVERED — Covers the broad infrastructure data model across dcim, ipam, circuits, VMs, tenancy, VPN, and wireless.
- F4: COVERED — Explicitly describes REST + GraphQL as programmable automation surfaces.

### ent-netbox-struct-2 (2/4)
- F1: COVERED — Describes plugins as AppConfig-style packaged Django extensions with route/UI/template extension surfaces.
- F2: MISS — Does not fully establish the negative boundaries (cannot modify core models/templates/settings or disable core components).
- F3: COVERED — `PluginConfig` + `packaging` + `IncompatiblePluginError` covers plugin version compatibility at a high level.
- F4: MISS — Does not mention `PLUGINS_CONFIG` in `configuration.py`.

### ent-netbox-rel-1 (3/4)
- F1: COVERED — Explains tenancy as its own tenant/tenant-group layer spanning infrastructure objects.
- F2: MISS — Does not establish recursive tenant groups or optional group membership.
- F3: COVERED — Connects tenancy support to many core object families via the architectural model and inheritable `TenancyFilterSet`.
- F4: COVERED — Clearly distinguishes ownership fields (`OwnerMixin`) from tenancy.

### ent-netbox-rel-2 (2/4)
- F1: MISS — Does not reconstruct the full object-permission schema (object types, users/groups, actions, JSON constraints).
- F2: COVERED — Explains baseline permissions flowing from `settings.DEFAULT_PERM...` for active authenticated users.
- F3: MISS — Does not mention `EXEMPT_VIEW_PERMISSIONS` or anonymous read exemptions.
- F4: COVERED — Explains session UI auth, token API auth, and remote/SSO backend support.

### ent-netbox-mech-1 (1/4)
- F1: COVERED — Covers scripts/reports, remote data sync, and housekeeping as background-job families.
- F2: MISS — Does not establish plugin-added jobs running in `rqworker` processes.
- F3: MISS — Mentions `enqueue_once`, but not immediate/future/repeating scheduling.
- F4: MISS — Does not mention `system_job()` or default queue names.

### ent-netbox-mech-2 (2/4)
- F1: COVERED — Explains that events are flushed to RQ/Redis-backed async processing after monitored changes.
- F2: COVERED — Explains asynchronous event-rule/webhook/script processing via RQ-backed workers.
- F3: MISS — Does not describe Jinja2 payload templating/context fields.
- F4: MISS — Does not mention 2XX success rules, manual requeue, or `webhook_receiver`.

## Per-repo table
| repo | v1 score | v2 score | v3 score |
|---|---:|---:|---:|
| saleor | 7/24 | 7/24 | 8/24 |
| netbox | 13/24 | 10/24 | 13/24 |

## By type table
| type | saleor v3 | netbox v3 | total v3 |
|---|---:|---:|---:|
| structural | 5/8 | 5/8 | 10/16 |
| relational | 1/8 | 5/8 | 6/16 |
| mechanistic | 2/8 | 3/8 | 5/16 |

## Analysis
The architectural summary helped most on **structural** tasks and on NetBox’s higher-level **relational** tasks. It turned raw symbols like `PluginConfig`, `TenancyFilterSet`, `TokenAuthentication`, and channel-aware Saleor mutations into business concepts such as source-of-truth architecture, plugin extension surfaces, tenancy vs ownership, and multi-channel commerce. It helped less on **policy/ops-heavy** families: Saleor deprecation policy and scheduler commands, plus NetBox webhook delivery details, still depended on repo docs or low-level operational text that the clue package did not surface. In short, arch context helped most where symbol meaning needed domain framing; it helped least where the missing facts were explicit documentation rules or command-line procedures.
