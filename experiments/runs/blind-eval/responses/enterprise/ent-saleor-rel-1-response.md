# Enterprise Eval: ent-saleor-rel-1
Date: 2026-04-17

## Question
How are permission checks attached to Saleor GraphQL queries and mutations?

---

## Reasoning Trace

### Step 1: Identify Permission-Related Symbols

From SYM and FOCUS, the following symbols are directly related to permission checking:

- `has_perm` (saleor/permission/models.py:143) — "Return True if the user has the specified permission" (SYM).
- `_user_has_perm` (saleor/permission/models.py:8) — "Backend can raise `PermissionDenied` to short-circuit..." (SYM).
- `permission_required` (saleor/graphql/decorators.py:70-81) — a decorator that calls `account_passes_test` and raises `PermissionDenied` (FOCUS).
- `PermissionDenied` (core.exceptions) — used pervasively across mutations and query resolvers (FOCUS, multiple entries).

### Step 2: Permission Checks on Mutations

**Base mutation classes enforce permissions.** The mutation hierarchy provides several permission enforcement points:

1. **`PermissionGroupCreate`** (saleor/graphql/account/mutations/permission_group/permission_group_create.py:60-272) extends `DeprecatedModelMutation`. It explicitly calls `check_permissions`, `ensure_can_manage_permissions`, `ensure_can_manage_channels`, and `ensure_users_are_staff`. Raises both `ValidationError` and `PermissionDenied` (FOCUS).

2. **`PermissionGroupUpdate`** (saleor/graphql/account/mutations/permission_group/permission_group_update.py:57-325) extends `PermissionGroupCreate`, inheriting its permission infrastructure. Additionally calls `check_if_removing_user_last_group`, `check_if_users_can_be_removed`, and `clean_remove_users` (FOCUS).

3. **`PermissionGroupDelete`** (saleor/graphql/account/mutations/permission_group/permission_group_delete.py:25-108) extends `ModelDeleteMutation`. Calls `check_permissions`, `ensure_deleting_not_left_not_manageable_permissions`, `ensure_not_removing_requestor_last_group`. Raises `PermissionDenied` and `ValidationError` (FOCUS).

4. **`ModelWithRestrictedChannelAccessMutation`** (from struct-1 clue) calls `check_channel_permissions` before proceeding — showing channel-scoped permission enforcement at the mutation base class level.

5. **`_requestor_has_permission`** (saleor/graphql/notifications/mutations/external_notification_trigger.py:95-98) — behavior: `GUARD(cls.check_permissions(context, (permission_type,)) -> return True)`. Called by `perform_mutation` of `ExternalNotificationTrigger`. Raises `PermissionDenied` (FOCUS). This shows mutations can also perform inline permission checks within `perform_mutation`.

**Input types for permission mutations:**
- `PermissionGroupInput` (saleor/graphql/account/mutations/permission_group/permission_group_create.py:27-43) extends `BaseInputObjectType` (FOCUS).
- `PermissionGroupCreateInput` (lines 46-57) extends `PermissionGroupInput` (FOCUS).
- `PermissionGroupUpdateInput` (saleor/graphql/account/mutations/permission_group/permission_group_update.py:33-54) extends `PermissionGroupInput` (FOCUS).

**Metadata mutations have their own permission model:**
- `MetadataPermissionOptions` (saleor/graphql/meta/mutations/base.py:28-29) extends `MutationOptions` — indicating metadata mutations declare their own permission requirements via a custom options class (FOCUS).

### Step 3: Permission Checks on Queries

**Query classes raise PermissionDenied directly.** Several query schema classes explicitly use `PermissionDenied`:

- **`AppQueries`** (saleor/graphql/app/schema.py:60-175) — extends `ObjectType`; raises `PermissionDenied`. Imports from `permission.auth_filters` and `permission.enums` (FOCUS).
- **`AccountQueries`** (saleor/graphql/account/schema.py:117-283) — extends `ObjectType`; imports from `permission.auth_filters`, `permission.enums`, `permission.utils`. Resolves `resolve_customers`, `resolve_staff_users`, `resolve_permission_group`, `resolve_permission_groups` (FOCUS).
- **`OrderQueries`** (saleor/graphql/order/schema.py:102-271) — extends `ObjectType`; explicitly raises `PermissionDenied` (FOCUS).
- **`ProductQueries`** (saleor/graphql/product/schema.py:141-638) — extends `ObjectType`; imports `permission.enums` (FOCUS).
- **`DiscountQueries`** (saleor/graphql/discount/schema.py:74-202) — extends `ObjectType`; imports `permission.enums` (FOCUS).
- **`CheckoutQueries`** (saleor/graphql/checkout/schema.py:50-123) — imports `permission.enums` (FOCUS).
- **`GiftCardQueries`** (saleor/graphql/giftcard/schema.py:38-134) — imports `permission.enums` (FOCUS).
- **`PaymentQueries`** (saleor/graphql/payment/schema.py:55-157) — imports `permission.enums` (FOCUS).
- **`ChannelQueries`** (saleor/graphql/channel/schema.py:20-50) — imports `permission.auth_filters` (FOCUS).
- **`CsvQueries`** (saleor/graphql/csv/schema.py:16-42) — imports `permission.enums` (FOCUS).
- **`PluginsQueries`** (saleor/graphql/plugins/schema.py:17-53) — imports `permission.enums` (FOCUS).
- **`StockQueries`** (saleor/graphql/warehouse/schema.py:87-114) — imports `permission.enums` (FOCUS).

The widespread import of `permission.enums` across query classes indicates that queries declare required permissions via enumerated permission constants.

### Step 4: The `permission_required` Decorator

`permission_required` (saleor/graphql/decorators.py:70-81) provides a decorator-based mechanism. It:
- Takes a `perm` argument
- Calls `account_passes_test` (a function it delegates to)
- Raises `PermissionDenied` on failure

This decorator can be applied to individual resolver functions, providing field-level permission enforcement separate from the class-level checks in query/mutation schemas.

### Step 5: App-Level Permission Checks

For app-related access:
- `has_required_permission` (saleor/graphql/app/types.py:84-89) — called by `resolve_tokens`, `resolve_webhooks`, and `App` type. Raises `PermissionDenied` (FOCUS).
- `check_permission_for_access_to_meta` (saleor/graphql/app/types.py:92-97) — calls `has_access_to_app_public_meta`; called by `resolve_metadata`, `resolve_metafield`, `resolve_metafields`. Raises `PermissionDenied` (FOCUS).
- `resolve_permission_groups` (saleor/graphql/account/types.py:608-611) — guards on `is_newly_created_user(root)` returning empty list for new users (FOCUS).

### Step 6: Permission Infrastructure

The `saleor/permission/` package provides the backend:
- `has_perm` (saleor/permission/models.py:143) — the core permission check method (SYM).
- `_user_has_perm` (saleor/permission/models.py:8) — authentication backend hook that can raise `PermissionDenied` to short-circuit (SYM).
- `permission.enums` — imported by virtually every query class, providing standardized permission constants.
- `permission.auth_filters` — imported by `AppQueries`, `AccountQueries`, `ChannelQueries`, providing queryset-level permission filtering.
- `permission.utils` — imported by `AccountQueries` (FOCUS).

### Step 7: Query Validation Layer

- `__queries_or_introspection_in_selections` (saleor/graphql/utils/validators.py:36-55) and `__queries_or_introspection_in_inline_fragment` (saleor/graphql/utils/validators.py:58) provide query-level validation that walks selections/fragments. While not strictly permission checks, they serve as a guard layer over what queries can be constructed (SYM).

### Step 8: GAPS — What Cannot Be Determined

Per the GAPS section:
- **Type:** STRUCTURAL (answerable from L0-L2)
- **Coverage:** 80 symbols in L3, only 7 with behavior annotations
- **Uncovered symbols:** `resolve_permission_group` (appears 3 times — suggesting multiple GraphQL types resolve permission groups, but their bodies are not available), `resolve_permission_groups` (1 occurrence uncovered)

Additionally, from the clue alone:
- The exact implementation of `account_passes_test` (called by `permission_required`) is not shown
- The full list of permission enums in `permission.enums` is not enumerated
- How `check_permissions` is implemented in the base mutation classes is not detailed
- Whether permissions are declared as class-level `Meta` attributes on mutations (a common Django-Graphene pattern) cannot be confirmed

---

## Synthesized Answer

Permission checks in Saleor GraphQL are attached at **four levels**:

1. **Permission backend** (`saleor/permission/`): `has_perm` (models.py:143) and `_user_has_perm` (models.py:8) form the foundation. `_user_has_perm` can raise `PermissionDenied` to short-circuit access. Permission constants are defined in `permission.enums`, imported by all query/mutation schema modules.

2. **Mutation base classes:** Mutations inherit from `DeprecatedModelMutation` and its subclasses. `PermissionGroupCreate` (permission_group_create.py:60) calls `check_permissions` and `ensure_can_manage_permissions`. Channel-restricted mutations (`ModelWithRestrictedChannelAccessMutation`) call `check_channel_permissions`. `_requestor_has_permission` (external_notification_trigger.py:95) shows inline permission guards within `perform_mutation`.

3. **Decorator-based field protection:** `permission_required` (saleor/graphql/decorators.py:70-81) wraps resolvers via `account_passes_test`, raising `PermissionDenied` on failure. This enables per-field permission enforcement.

4. **Query schema classes:** Every query class (e.g., `AppQueries`, `AccountQueries`, `OrderQueries`, `ProductQueries`, etc.) imports `permission.enums` and/or `permission.auth_filters`. Several explicitly raise `PermissionDenied` (e.g., `OrderQueries` at order/schema.py:102, `AppQueries` at app/schema.py:60). App-specific resolvers add further checks (`has_required_permission` at app/types.py:84, `check_permission_for_access_to_meta` at app/types.py:92).
