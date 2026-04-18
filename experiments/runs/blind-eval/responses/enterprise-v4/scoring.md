# Enterprise v4 scoring (Saleor)
Date: 2026-04-18

## Comparison
| version | score |
|---|---:|
| v1 (AST only) | 7/24 |
| v3 (arch only) | 8/24 |
| v4 (full-stack) | 24/24 |

## Per-task

### ent-saleor-struct-1 (4/4)
- F1: COVERED — Explicitly says Saleor is GraphQL-only / API-only.
- F2: COVERED — Explicitly says the dashboard is a decoupled project in the separate `saleor-dashboard` repo.
- F3: COVERED — Explicitly describes native multichannel control over pricing, currencies, stock, and products.
- F4: COVERED — Explicitly lists webhooks, apps, subscription queries, API extensions, and dashboard iframes as extension surfaces.

### ent-saleor-struct-2 (4/4)
- F1: COVERED — Explicitly describes the standard Django app structure with migrations, management, models, utils, error codes, and tests.
- F2: COVERED — Explicitly places the API under `saleor/graphql/`.
- F3: COVERED — Explicitly lists `schema.py`, `sorters.py`, `filters.py`, `types.py`, `enums.py`, `dataloaders.py`, plus mutations/tests.
- F4: COVERED — Explicitly states tests are split into `queries` and `mutations` with one file per operation.

### ent-saleor-rel-1 (4/4)
- F1: COVERED — Explicitly says queries use `permission_required` / `one_of_permissions_required` decorators.
- F2: COVERED — Explicitly says mutation permissions live in `Meta.permissions`.
- F3: COVERED — Explicitly explains `AuthorizationFilters` as function-based permission checks.
- F4: COVERED — Explicitly says `PermissionDenied` should name required permissions and GraphQL descriptions should mention them.

### ent-saleor-rel-2 (4/4)
- F1: COVERED — Explicitly says removing/renaming a GraphQL field is a breaking change.
- F2: COVERED — Explicitly says removing/renaming a webhook payload field is a breaking change.
- F3: COVERED — Explicitly says changing `PluginsManager` signatures breaks existing plugins.
- F4: COVERED — Explicitly says API fields deprecate before removal and `PREVIEW_FEATURE` removals can happen in the next minor version with changelog coverage.

### ent-saleor-mech-1 (4/4)
- F1: COVERED — Explicitly says the search vector update task is triggered by Celery Beat.
- F2: COVERED — Explicitly says the feature will not work without task queue configuration.
- F3: COVERED — Explicitly gives `uv run poe worker`.
- F4: COVERED — Explicitly gives `uv run poe scheduler`.

### ent-saleor-mech-2 (4/4)
- F1: COVERED — Explicitly says to use `select_for_update()` on querysets to prevent race conditions.
- F2: COVERED — Explicitly says lock multiple objects in a consistent order, typically by primary key.
- F3: COVERED — Explicitly says to lock `Order` before `OrderLine` for cross-model locking.
- F4: COVERED — Explicitly says locking helpers belong in app-local `lock_objects.py` files.

## Per-type breakdown
| type | tasks | score |
|---|---:|---:|
| structural | 2 | 8/8 |
| relational | 2 | 8/8 |
| mechanistic | 2 | 8/8 |
| total | 6 | 24/24 |

## Summary
v4 closes every Saleor gap left by v1/v3 because it combines prompt-level architectural/domain/clue evidence with the repository’s explicit README / CONTRIBUTING / AGENTS guidance for policy and operational facts.

