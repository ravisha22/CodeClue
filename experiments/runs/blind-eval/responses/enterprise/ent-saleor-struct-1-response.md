# Enterprise Eval: ent-saleor-struct-1
Date: 2026-04-17

## Question
How is Saleor split across its core platform, multichannel commerce model, and extension surfaces?

---

## Reasoning Trace

### Step 1: Identify Relevant Modules from TREE and INDEX

The TREE reveals the top-level `saleor/` directory (4237 files) contains domain-specific sub-packages: `account/`, `app/`, `attribute/`, `auth/`, `channel/`, `checkout/`, `core/`, `csv/`, `discount/`, plus 20+ more (TREE, line 21). The INDEX further confirms deep nesting within each domain — e.g., `saleor/account/` has models, migrations, events, forms, error codes, and management commands (INDEX, lines 29–43).

### Step 2: Core Platform Layer

**Base model abstractions.** The core platform is anchored in `saleor/core/models.py`, which defines several foundational abstract model classes:

- **`SortableModel`** (saleor/core/models.py:16-45) — extends Django `Model`; provides `get_ordering_queryset`, `get_max_sort_order`, custom `save`, and `delete`. Uses `F` and `Max` from `django.db.models`. Raises `NotImplementedError` for `get_ordering_queryset`, establishing a template-method contract (FOCUS).
- **`PublishableModel`** (saleor/core/models.py:63-77) — extends `Model`; provides publish/unpublish semantics for domain objects (FOCUS).
- **`ModelWithMetadata`** (saleor/core/models.py:80-125) — extends `Model`; adds metadata capabilities. Migration logic in `flatten_model_metadata` (saleor/core/migrations/0001_migrate_metadata.py:6) shows this was retroactively applied to many domain models: attributes, categories, checkouts, collections, digital contents, fulfillments, orders, product types (SYM, called_by chain of `flatten_model_metadata`).
- **`ModelWithExternalReference`** (saleor/core/models.py:128-138) — extends `Model`; supports external reference IDs (FOCUS).
- **`SeoModel`** (saleor/seo/models.py:7-16) — extends `Model`; provides SEO fields. Has translation counterparts `SeoModelTranslation` and `SeoModelTranslationWithSlug` (FOCUS).

**Core app configuration.** `CoreAppConfig` (saleor/core/apps.py:11-37, `name='saleor.core'`) calls `validate_jwt_manager` on ready, showing core handles JWT validation setup (FOCUS).

**Password hashing.** `encode` and `pbkdf2_round` (saleor/core/hashers.py:18, :30) provide custom password hashing in the core layer (SYM).

**EditorJS validation.** `StrictBaseModel` (saleor/core/editorjs/models.py:42-52) extends `UnsafeBaseModel` with pydantic strict validation; `clean_model` (saleor/core/management/commands/clean_editorjs_fields.py:162-242) provides a management command to clean EditorJS fields (FOCUS).

**GraphQL foundation.** Core GraphQL infrastructure lives in `saleor/graphql/core/`:
- `ModelObjectType` (saleor/graphql/core/types/model.py:19-85) extends `BaseObjectType` and uses `ModelObjectOptions` to bind GraphQL types to Django models (FOCUS).
- `NonNullList` (saleor/graphql/core/types/common.py:111) auto-adds non-null constraints (SYM).
- `SaleorContext` (saleor/graphql/core/context.py:16-29) extends `HttpRequest` (FOCUS).
- `SaleorGraphQLBackend` (saleor/graphql/api.py:234-256) extends `GraphQLCoreBackend` (FOCUS).
- `CoreQueries` and `CoreMutations` (saleor/graphql/core/schema.py:11-28) extend `ObjectType`, providing the schema root for core operations (FOCUS).

**Mutation hierarchy.** A rich mutation class hierarchy exists:
- `ModelMutationOptions` (saleor/graphql/core/mutations.py:131-136) extends `MutationOptions` with `model`, `object_type`, `doc_category`, `exclude` (FOCUS).
- `ModelWithExtRefMutation` (saleor/graphql/core/mutations.py:864-892) extends `DeprecatedModelMutation`; calls `get_object_id` (FOCUS).
- `ModelDeleteMutation` (saleor/graphql/core/mutations.py:941-968) extends `DeprecatedModelMutation` (FOCUS).
- `ModelBulkDeleteMutation` (saleor/graphql/core/mutations.py:1125-1131) extends `BaseBulkMutation` (FOCUS).

### Step 3: Multichannel Commerce Model

**Channel-restricted mutations.** Two specialized mutation bases enforce channel-level access:
- **`ModelWithRestrictedChannelAccessMutation`** (saleor/graphql/core/mutations.py:895-938) extends `DeprecatedModelMutation`; calls `check_channel_permissions` before proceeding to `construct_instance`, `validate_and_update_metadata`, `_save_m2m`, `post_save_action`, `save`, `success_response`. Raises `NotImplementedError` and uses `PermissionDenied` (FOCUS).
- **`ModelDeleteWithRestrictedChannelAccessMutation`** (saleor/graphql/core/mutations.py:971-997) extends `ModelDeleteMutation`; also calls `check_channel_permissions`. Raises `NotImplementedError` and uses `PermissionDenied` (FOCUS).

These establish that channel-scoping is woven into the mutation layer itself — mutations that operate on channel-bound entities must pass channel-level permission checks.

**Channel as a top-level domain.** The `channel/` directory is listed as a top-level package in TREE. The `SyncWebhookControlContextModelObjectType` (saleor/graphql/core/types/sync_webhook_control.py:33-37) imports from `context` and `model`, indicating sync webhooks also interact with channel-aware contexts (FOCUS).

### Step 4: Extension Surfaces

**Plugin system.** The plugin infrastructure in `saleor/plugins/` provides the primary extension surface:
- `__run_method_on_plugins` (saleor/plugins/manager.py:211) — iterates over all plugins to invoke a named method (SYM).
- `__run_method_on_single_plugin` (saleor/plugins/manager.py:233) — runs a method on a single plugin (SYM).
- `get_plugins` (saleor/plugins/manager.py:2488) — returns plugins for a given channel, showing channel-aware plugin dispatch (SYM).
- `_ensure_channel_plugins_loaded` (saleor/plugins/manager.py:151) — lazy-loads plugins per channel (SYM).
- `_load_plugin` (saleor/plugins/manager.py:104) — loads a single plugin instance (SYM).
- `_get_db_plugin_configs` (saleor/plugins/manager.py:201) — fetches plugin configs from the database (SYM).
- `get_plugin` (saleor/plugins/manager.py:2669) — retrieves a specific plugin (SYM).
- Payment gateways are plugins: `_get_gateway_config` appears in `braintree/plugin.py`, `authorize_net/plugin.py`, `dummy/plugin.py`, `dummy_credit_card/plugin.py`, and Stripe has `stripe_otel_trace` (SYM).
- `send_email` (saleor/plugins/sendgrid/tasks.py:22) — SendGrid is implemented as a plugin (SYM).

**Webhook system.** The webhook plugin is a special built-in plugin:
- `trigger_webhooks_async` (saleor/plugins/webhook/plugin.py:246) — async webhook dispatch (SYM).
- `_get_webhooks_for_event` (saleor/plugins/webhook/plugin.py:175) — finds webhooks for a specific event type (SYM).
- `_get_webhooks_for_channel_events` (saleor/plugins/webhook/plugin.py:766) — channel-scoped webhook lookup (SYM).
- `__run_payment_webhook` (saleor/plugins/webhook/plugin.py:2994) — triggers payment-specific webhook events (SYM).
- `_serialize_payload` (saleor/plugins/webhook/plugin.py:181) and `_generate_meta` (:184) handle payload construction (SYM).

**App extension model.** Third-party apps have a formal extension surface:
- `AppExtension` model (saleor/app/models.py:155-174) extends Django `Model` (FOCUS).
- `AppExtension` GraphQL type (saleor/graphql/app/types.py:172-273) extends `AppManifestExtension` (FOCUS).
- `AppManifestExtension` (saleor/graphql/app/types.py:115-164) extends `BaseObjectType` (FOCUS).
- `ManifestExtensionSchema` (saleor/app/manifest_schema.py:53-61) extends pydantic `BaseModel` for manifest validation (FOCUS).
- `AppExtensionCountableConnection`, `AppExtensionFilter`, `AppExtensionFilterInput` provide pagination, filtering, and query input for extensions (FOCUS).
- `AppManifestRequiredSaleorVersion` (saleor/graphql/app/types.py:315-326) and `RequiredSaleorVersionSpec` (saleor/app/manifest_validations.py:36-41, extends `NpmSpec`) enforce version constraints on app manifests (FOCUS).

**Permission system.** Access control bridges core and extensions:
- `has_perm` (saleor/permission/models.py:143) — checks user permissions (SYM).
- `_user_has_perm` (saleor/permission/models.py:8) — backend-level perm check (SYM).
- `validate_ids_and_get_model_type_and_pks` (saleor/core/notification/validation.py:26-37) — validates entity IDs with guard behavior (FOCUS).
- `get_type_for_model` (saleor/graphql/core/mutations.py:782, :1027) — resolves GraphQL types from model metadata, raising `ImproperlyConfigured` if missing (FOCUS).

### Step 5: GAPS — What Cannot Be Determined

Per the GAPS section:
- **Type:** STRUCTURAL (answerable from L0-L2)
- **Coverage:** 80 symbols in L3, only 12 with behavior annotations
- **Uncovered symbols:** `move_email_templates_to_separate_model`, `perform_model_extra_actions`, `reorder_model`, `resolve_access_token_for_app_extension` — meaning the full behavior of email template migration, model reordering logic, extra model actions, and app extension access token resolution cannot be determined from this clue alone.

---

## Synthesized Answer

Saleor's architecture splits into three distinct layers:

1. **Core Platform:** Abstract Django models in `saleor/core/models.py` (`SortableModel`, `PublishableModel`, `ModelWithMetadata`, `ModelWithExternalReference`) provide shared behaviors (ordering, publishing, metadata, external refs). A deep GraphQL infrastructure in `saleor/graphql/core/` (`ModelObjectType`, `SaleorContext`, `SaleorGraphQLBackend`, the mutation class hierarchy) unifies API exposure. Domain modules (`account/`, `checkout/`, `order/`, `product/`, `discount/`, etc.) are separated as top-level packages under `saleor/`.

2. **Multichannel Commerce:** Channel-awareness is enforced at the mutation layer via `ModelWithRestrictedChannelAccessMutation` and `ModelDeleteWithRestrictedChannelAccessMutation`, which call `check_channel_permissions` before any data modification. The plugin manager dispatches per-channel (`get_plugins` returns plugins for a given channel; `_ensure_channel_plugins_loaded` lazy-loads them). Webhook dispatch also supports channel scoping via `_get_webhooks_for_channel_events`.

3. **Extension Surfaces:** Extensions are provided through (a) a **plugin system** (`saleor/plugins/manager.py` with `__run_method_on_plugins`, per-channel dispatch, DB-stored configs), (b) a **webhook system** (built-in plugin at `saleor/plugins/webhook/plugin.py` with async triggers, event-based dispatch, payload serialization), and (c) a **third-party app model** (`AppExtension` in `saleor/app/models.py`, manifest schemas with version constraints via `RequiredSaleorVersionSpec`, GraphQL query/filter surfaces in `saleor/graphql/app/`).
