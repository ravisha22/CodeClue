# Enterprise v3 (arch-enhanced): ent-saleor-rel-1
Date: 2026-04-18

## Answer
Permission checks are attached to Saleor GraphQL queries in two visible ways. First, there is an explicit `permission_required(perm)` decorator in `saleor/graphql/decorators.py`, which calls `account_passes_test` and can raise `PermissionDenied` (permission_required, saleor/graphql/decorators.py:70-81). Second, query groups import permission-related modules and expose permission-guarded resolvers: for example, `AccountQueries` imports `permission.auth_filters`, `permission.enums`, and `permission.utils`; `AppQueries` imports `permission.auth_filters` and `permission.enums`; and `OrderQueries` can raise `PermissionDenied` (AccountQueries, saleor/graphql/account/schema.py:117-283; AppQueries, saleor/graphql/app/schema.py:60-175; OrderQueries, saleor/graphql/order/schema.py:102-271).

Mutations are guarded through explicit permission-checking calls inside mutation classes. `PermissionGroupCreate` calls `check_permissions`, `ensure_can_manage_channels`, and `ensure_can_manage_permissions`; `PermissionGroupDelete` also calls `check_permissions`; and `_requestor_has_permission` wraps `cls.check_permissions(...)` and raises `PermissionDenied` when the check fails (PermissionGroupCreate, saleor/graphql/account/mutations/permission_group/permission_group_create.py:60-272; PermissionGroupDelete, saleor/graphql/account/mutations/permission_group/permission_group_delete.py:25-108; _requestor_has_permission, saleor/graphql/notifications/mutations/external_notification_trigger.py:95-98).

The same pattern appears on GraphQL object types. The `App` type calls `check_permission_for_access_to_meta` and `has_required_permission`, both of which can raise `PermissionDenied`; `has_required_permission` is called by `resolve_tokens` and `resolve_webhooks` (App, saleor/graphql/app/types.py:645-825; check_permission_for_access_to_meta, saleor/graphql/app/types.py:92-97; has_required_permission, saleor/graphql/app/types.py:84-89).

## Gaps
The clue does **not** show mutation permissions living in `Meta.permissions`, does not explain `AuthorizationFilters`, and does not provide the policy that `PermissionDenied` errors/descriptions must name the required permissions. Those details are unresolved from this prompt (GAPS, ent-saleor-rel-1-v3.prompt.md:260-263).
