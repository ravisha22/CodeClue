# Enterprise v2: ent-saleor-rel-1
Date: 2026-04-17

## Question
How are permission checks attached to Saleor GraphQL queries and mutations?

## Reasoning Scaffold

### Step 1: Identify the Permission Infrastructure (SYM, FOCUS, INDEX)

The primary permission backend lives in `saleor/permission/models.py`:
- **`has_perm`** (`:143`) — "Return True if the user has the specified permission." This is the model-level permission check entry point (SYM).
- **`_user_has_perm`** (`:8`) — "Backend can raise `PermissionDenied` to short-circuit." This is the low-level backend that can immediately terminate a request with a denied error (SYM).

The GraphQL decorator entry point is:
- **`permission_required`** (`saleor/graphql/decorators.py:70-81`) — calls `account_passes_test`; raises `PermissionDenied`. This is a function decorator that can be applied to resolver functions (FOCUS).

`PermissionDenied` is sourced from `core.exceptions` and is consistently used across all permission-checking sites (FOCUS, multiple entries).

### Step 2: Trace Permission Checks on Mutations (FOCUS, SYM)

**Mutation class hierarchy:**

`DeprecatedModelMutation` is the shared base for writable mutations. Several specialisations sit above it:
- **`ModelWithRestrictedChannelAccessMutation`** (`saleor/graphql/core/mutations.py:895-938`) extends `DeprecatedModelMutation` and calls `check_channel_permissions` as part of its execution — enforcing that the requestor has access to the relevant channel in addition to any base permissions (FOCUS).
- **`ModelDeleteWithRestrictedChannelAccessMutation`** (`saleor/graphql/core/mutations.py:971-997`) extends `ModelDeleteMutation` and similarly calls `check_channel_permissions` (FOCUS).
- **`ModelDeleteMutation`** (`saleor/graphql/core/mutations.py:941-968`) extends `DeprecatedModelMutation` (FOCUS).
- **`ModelBulkDeleteMutation`** (`saleor/graphql/core/mutations.py:1125-1131`) extends `BaseBulkMutation` (FOCUS).

**Domain-level mutations with explicit permission calls:**

- **`PermissionGroupCreate`** (`saleor/graphql/account/mutations/permission_group/permission_group_create.py:60-272`) extends `DeprecatedModelMutation` and explicitly calls `check_permissions`, `ensure_can_manage_channels`, `ensure_can_manage_permissions`, `ensure_users_are_staff`. Raises `ValidationError` and `PermissionDenied` (FOCUS).
- **`PermissionGroupUpdate`** (`saleor/graphql/account/mutations/permission_group/permission_group_update.py:57-325`) extends `PermissionGroupCreate`, so inherits the same permission-checking logic. Also calls `check_if_removing_user_last_group`, `check_if_users_can_be_removed` (FOCUS).
- **`PermissionGroupDelete`** (`saleor/graphql/account/mutations/permission_group/permission_group_delete.py:25-108`) extends `ModelDeleteMutation` and explicitly calls `check_permissions`, `ensure_deleting_not_left_not_manageable_permissions`, `ensure_not_removing_requestor_last_group`. Raises `PermissionDenied` and `ValidationError` (FOCUS).
- **`AppProblemDismiss`** (`saleor/graphql/app/mutations/app_problem_dismiss.py:102-327`) extends `BaseMutation` and raises `ValidationError`; it imports `app.lock_objects` but does not list a `check_permissions` call directly in the FOCUS snippet — permission enforcement likely comes from `BaseMutation`'s inherited mechanism (FOCUS).

**Notification mutation:**
- **`_requestor_has_permission`** (`saleor/graphql/notifications/mutations/external_notification_trigger.py:95-98`) — behaviour annotated as `GUARD(cls.check_permissions(context, (permission_type,)) -> return True)`. Called by `perform_mutation`. Raises `PermissionDenied`. This pattern shows that at the mutation's `perform_mutation` step, a custom guard function calls the inherited `check_permissions` method (FOCUS).

### Step 3: Trace Permission Checks on Queries (FOCUS, SYM)

Query objects (`*Queries` classes extending `ObjectType`) declare permission requirements through their imports and resolver calls:

- **`AccountQueries`** (`saleor/graphql/account/schema.py:117-283`) imports `permission.auth_filters`, `permission.enums`, `permission.utils` — authority filtering is applied at the query level (FOCUS).
- **`AppQueries`** (`saleor/graphql/app/schema.py:60-175`) imports `permission.auth_filters`, `permission.enums`; raises `PermissionDenied` (FOCUS).
- **`OrderQueries`** (`saleor/graphql/order/schema.py:102-271`) raises `PermissionDenied` and uses `PermissionDenied (core.exceptions)` (FOCUS).
- **`DiscountQueries`** (`saleor/graphql/discount/schema.py:74-202`) imports `permission.enums` (FOCUS).
- **`ProductQueries`** (`saleor/graphql/product/schema.py:141-638`) imports `permission.enums` (FOCUS).

Field-level and resolver-level permission checks:

- **`has_required_permission`** (`saleor/graphql/app/types.py:84-89`) — called by `resolve_tokens`, `resolve_webhooks`, `App`; raises `PermissionDenied` (FOCUS). This is a field-resolver guard that fires when sensitive sub-fields are accessed.
- **`check_permission_for_access_to_meta`** (`saleor/graphql/app/types.py:92-97`) — calls `has_access_to_app_public_meta`; called by `resolve_metadata`, `resolve_metafield`, `resolve_metafields` in `App`. Raises `PermissionDenied` (FOCUS). Shows that metadata field resolution is separately permission-gated.
- **`_resolve_app`** (`saleor/graphql/discount/types/promotion_events.py:62-69`) — `GUARD(is_owner_or_has_one_of_perms(requester, app, AppPermissio... -> return ...)` (FOCUS). Demonstrates inline GUARD patterns in type resolvers using `is_owner_or_has_one_of_perms`.
- **`resolve_access_token_for_app`** (`saleor/graphql/app/resolvers.py:30-40`) — `GUARD(root.type != AppTypeEnum.THIRDPARTY.value -> return None)`. Type-based conditional return, acting as an implicit permission fence (FOCUS).
- **`resolve_permission_groups`** (`saleor/graphql/account/types.py:608-611`) — `GUARD(is_newly_created_user(root) -> return [])` — short-circuits for new users (FOCUS).
- **`MetadataPermissionOptions`** (`saleor/graphql/meta/mutations/base.py:28-29`) extends `MutationOptions`, dedicated options class for metadata mutations indicating that metadata mutations have their own permission-option subsystem (FOCUS).

### Step 4: Walk the Full Attachment Chain

The call chain for a typical permission-checked mutation can be traced as:

1. **Decorator layer:** `permission_required` (decorator in `saleor/graphql/decorators.py`) wraps the resolver function; it calls `account_passes_test` and raises `PermissionDenied` on failure.
2. **Mutation base class layer:** `DeprecatedModelMutation` subclasses inherit a `check_permissions` method; this is called explicitly in `PermissionGroupCreate`, `PermissionGroupDelete`, and via `_requestor_has_permission` in notification mutations.
3. **Channel restriction layer:** `ModelWithRestrictedChannelAccessMutation` adds `check_channel_permissions` on top of the base permissions.
4. **Model-level backend:** `_user_has_perm` (`saleor/permission/models.py:8`) short-circuits with `PermissionDenied`; `has_perm` (`:143`) performs the positive check.
5. **Field/type resolver layer:** `has_required_permission` and `check_permission_for_access_to_meta` apply additional guards at the individual field level within type resolvers.

### Gaps / Uncertainty

Per GAPS (type: STRUCTURAL, coverage: 83 symbols in L3, 7 with behavior annotations):
- `resolve_permission_group` (4 occurrences listed) is explicitly uncovered — the exact implementation of permission-group-specific resolvers cannot be determined.
- The internal implementation of `check_permissions` (the base mutation method called by multiple mutation classes) is not shown — its signature and how it interacts with `has_perm`/`_user_has_perm` is not directly traceable from the clue.
- `account_passes_test` (called by `permission_required`) is not detailed in the clue.
- Whether `permission_required` is applied via class-level `Meta` declarations or per-field decorators is not determinable.

## Synthesized Answer

Saleor attaches permission checks at **four distinct layers** in the GraphQL stack:

1. **Decorator layer** (`permission_required` in `saleor/graphql/decorators.py`): A function decorator that calls `account_passes_test` and raises `PermissionDenied`. Applied directly to resolver functions.

2. **Mutation base class layer**: `DeprecatedModelMutation` and its subclasses inherit `check_permissions`. Domain mutations such as `PermissionGroupCreate`, `PermissionGroupDelete` call it explicitly during `clean_input`/`perform_mutation`. The notification mutation uses an internal `_requestor_has_permission` guard that delegates to `cls.check_permissions`. Channel-scoped mutations (`ModelWithRestrictedChannelAccessMutation`, `ModelDeleteWithRestrictedChannelAccessMutation`) add a second `check_channel_permissions` call on top.

3. **Query schema imports**: `*Queries` classes (`AccountQueries`, `AppQueries`, `OrderQueries`, `DiscountQueries`, `ProductQueries`) import `permission.auth_filters` and `permission.enums` to scope their querysets and raise `PermissionDenied` when access is denied.

4. **Field/type resolver guards**: Sensitive type resolvers use `has_required_permission` and `check_permission_for_access_to_meta` for field-level gating (e.g., `resolve_tokens`, `resolve_webhooks`, `resolve_metadata` on `App`). Inline GUARD patterns (`is_owner_or_has_one_of_perms`, type checks) are also used in individual resolvers.

The model-level backend (`_user_has_perm` / `has_perm` in `saleor/permission/models.py`) underpins all layers and can short-circuit any request with `PermissionDenied`.
