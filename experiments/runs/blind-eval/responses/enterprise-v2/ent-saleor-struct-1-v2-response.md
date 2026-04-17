# Enterprise v2: ent-saleor-struct-1
Date: 2026-04-17

## Question
How is Saleor split across its core platform, multichannel commerce model, and extension surfaces?

## Reasoning Scaffold

### Step 1: Identify Relevant Modules from TREE and INDEX

The TREE shows `saleor/` contains at least 30 top-level domain submodules including `account/`, `app/`, `asgi/`, `attribute/`, `auth/`, `channel/`, `checkout/`, `core/`, `csv/`, `discount/`, and 20 more (TREE). The INDEX exposes a consistent pattern: each domain module has `apps.py`, `error_codes.py`, `events.py`, `migrations/`, and often `management/commands/` — e.g., `saleor/account/apps.py` (AccountAppConfig), `saleor/account/error_codes.py`, `saleor/account/events.py` (INDEX).

The repository root also contains `manage.py`, `conftest.py`, `pyproject.toml`, `package.json`, and `.env.example`, establishing it as a Django project (INDEX, FOCUS: `saleor/settings.py`).

### Step 2: Trace the Core Platform Layer

The core platform layer is anchored in `saleor/core/`:

- **`SortableModel`** (`saleor/core/models.py:16-45`) extends `Model` and provides reusable ordering logic (`save`, `get_max_sort_order`, `get_ordering_queryset`; uses `F` and `Max` from `django.db.models`). This is a base mixin used across domain entities (FOCUS).
- **`ModelWithMetadata`** (`saleor/core/models.py:80-125`) extends `Model` — provides a shared metadata interface for any entity that exposes private/public metadata (FOCUS).
- **`PublishableModel`** (`saleor/core/models.py:63-77`) extends `Model` — provides publishability semantics (FOCUS).
- **`ModelWithExternalReference`** (`saleor/core/models.py:128-138`) extends `Model` — provides the `external_reference` field for third-party integrations (FOCUS).
- **`CoreAppConfig`** (`saleor/core/apps.py:11-37`) extends `AppConfig` with `name='saleor.core'`; calls `validate_jwt_manager` on `ready`, raising `ImportError` if the JWT manager is misconfigured (FOCUS).
- **`SaleorContext`** (`saleor/graphql/core/context.py:16-29`) extends `HttpRequest` — wraps each GraphQL request with Saleor-specific context (user, app, etc.) (FOCUS).
- **`CoreQueries`** / **`CoreMutations`** (`saleor/graphql/core/schema.py:11-24`, `:27-28`) extend `ObjectType` and compose the core GraphQL schema (FOCUS).
- **`ModelObjectType`** (`saleor/graphql/core/types/model.py:19-85`) provides the base GraphQL type wired to a Django model (FOCUS).
- The **`CoreErrorCode`** (`saleor/core/error_codes.py:37-38`) with `GRAPHQL_ERROR='graphql_error'` signals that core-level error codes are enum-based and centralised (FOCUS).
- Infrastructure is configured in `saleor/settings.py`: `SITE_ID=1`, `ROOT_URLCONF='saleor.urls'`, `SOFT_MEMORY_LIMIT_IN_MB`, `HARD_MEMORY_LIMIT_IN_MB`, Redis caching (`CACHE_URL=redis://localhost:6379/0`), Celery broker (`CELERY_BROKER_URL=redis://localhost:6379/1`) (FOCUS: `.env.example`).

### Step 3: Trace the Multichannel Commerce Layer

Multichannel commerce is a first-class structural concern:

- A dedicated `channel/` submodule is present in the TREE alongside `checkout/`, `discount/`, `order/`, `payment/`, `product/`, `attribute/` — all domain areas expected to be channel-aware.
- **`ModelWithRestrictedChannelAccessMutation`** (`saleor/graphql/core/mutations.py:895-938`) extends `DeprecatedModelMutation` and explicitly calls `check_channel_permissions` before any write proceeds. Raises `PermissionDenied` if the channel constraint is violated (FOCUS).
- **`ModelDeleteWithRestrictedChannelAccessMutation`** (`saleor/graphql/core/mutations.py:971-997`) similarly extends `ModelDeleteMutation` and calls `check_channel_permissions` before deletion (FOCUS).
- **`_get_webhooks_for_channel_events`** (`saleor/plugins/webhook/plugin.py:766`) has the annotation "Get webhooks for channel-based events," confirming that the webhook/event system is also segmented by channel (SYM).
- The `get_plugins` function (`saleor/plugins/manager.py:2488`) is described as "Return list of plugins for a given channel" — plugins are resolved per-channel (SYM).
- `_ensure_channel_plugins_loaded` (`saleor/plugins/manager.py:151`) lazily loads plugins scoped to a channel (SYM).
- Checkout calculations (`fetch_checkout_data` at `saleor/checkout/calculations.py:843` and `_fetch_checkout_prices_if_expired` at `:367`) and order calculations (`fetch_order_prices_if_expired` at `saleor/order/calculations.py:192`) indicate per-entity tax/price computation that feed into channel-scoped pricing (SYM).

### Step 4: Trace the Extension Surfaces Layer

Saleor exposes two primary extension surfaces — **Apps** and **Plugins/Webhooks**:

**App Extension Surface:**
- `saleor/app/` domain module provides the App data model. **`AppExtension`** (`saleor/app/models.py:155-174`) extends Django's `Model` and stores extension registrations in the database (FOCUS).
- **`ManifestExtensionSchema`** (`saleor/app/manifest_schema.py:53-61`) extends Pydantic `BaseModel` for validating app manifests (FOCUS).
- **`RequiredSaleorVersionSpec`** (`saleor/app/manifest_validations.py:36-41`) extends `NpmSpec` and enforces Saleor version compatibility for apps (FOCUS).
- On the GraphQL side, **`AppManifestExtension`** (`saleor/graphql/app/types.py:115-164`) and **`AppExtension`** (`saleor/graphql/app/types.py:172-273`) expose app extensions through the API. `AppExtension` raises `PermissionDenied` on unauthorised access (FOCUS).
- **`AppExtensionCountableConnection`** (`saleor/graphql/app/types.py:276-279`), **`AppExtensionFilter`** (`saleor/graphql/app/filters.py:45-58`), and **`AppExtensionFilterInput`** (`saleor/graphql/app/schema.py:54-57`) support paginated, filtered listing of extensions (FOCUS).
- **`AppManifestRequiredSaleorVersion`** (`saleor/graphql/app/types.py:315-326`) extends `BaseObjectType` and surfaces the version requirement through the API (FOCUS).
- **`AppQueries`** (`saleor/graphql/app/schema.py:60-175`) extends `ObjectType` and exposes queries `resolve_app`, `resolve_app_extensions`, `resolve_apps`, `resolve_apps_installations` — a full CRUD surface for apps (FOCUS).

**Plugin/Webhook Extension Surface:**
- `saleor/plugins/` houses the plugin system. **`WebhookPlugin`** (`saleor/plugins/webhook/plugin.py:156-3518`) extends `BasePlugin` with `PLUGIN_ID='mirumee.webhooks'`, `DEFAULT_ACTIVE=True`, `CONFIGURATION_PER_CHANNEL=False`. It dispatches async webhooks via `trigger_webhooks_async` (`:246`) and payment events via `__run_payment_webhook` (`:2994-3072`) (FOCUS, SYM).
- The plugin manager (`saleor/plugins/manager.py`) coordinates plugin execution: `_load_plugin` (`:104`), `_get_db_plugin_configs` (`:201`), `__run_method_on_plugins` (`:211`), `__run_method_on_single_plugin` (`:233`), `get_plugin` (`:2669`) (SYM).
- Payment gateway plugins follow a consistent pattern: each gateway (`braintree`, `authorize_net`, `stripe`, `dummy`, `dummy_credit_card`) exposes `_get_gateway_config` (`saleor/payment/gateways/*/plugin.py`) (SYM).
- The SEO surface (`SeoModel`, `SeoModelTranslation`, `SeoModelTranslationWithSlug` in `saleor/seo/models.py`) provides a reusable SEO metadata layer for page/product entities (FOCUS).

### Gaps / Uncertainty

Per GAPS (type: STRUCTURAL, coverage: 83 symbols in L3, 12 with behavior annotations):
- `move_email_templates_to_separate_model`, `perform_model_extra_actions`, `reorder_model`, `resolve_access_token_for_app_extension` are uncovered.
- The precise internal implementation of `check_channel_permissions` (called by the channel-restricted mutations) cannot be determined from the clue.
- The full list of domain modules hidden behind `...+20` in TREE is unknown; only the first 10 are visible.
- How the multichannel pricing pipeline chains through tax plugins is partially visible (via `_fetch_checkout_prices_if_expired`) but the complete flow is not traceable.

## Synthesized Answer

Saleor is structured in three clearly delineated layers:

1. **Core Platform (`saleor/core/`):** Provides base Django model mixins (`SortableModel`, `ModelWithMetadata`, `PublishableModel`, `ModelWithExternalReference`) and GraphQL primitives (`ModelObjectType`, `SaleorContext`, `CoreQueries`/`CoreMutations`). Infrastructure is Django + Redis (cache) + Celery (async tasks). The core validates itself at startup via `CoreAppConfig.validate_jwt_manager`.

2. **Multichannel Commerce Model:** A dedicated `channel/` module combined with channel-aware query/mutation base classes (`ModelWithRestrictedChannelAccessMutation`, `ModelDeleteWithRestrictedChannelAccessMutation`) that enforce `check_channel_permissions` on every write. The plugin manager resolves plugins per-channel (`get_plugins`), and webhook events are also channel-scoped (`_get_webhooks_for_channel_events`). Checkout and order calculations are price-expiry-aware (lazy recomputation hooks).

3. **Extension Surfaces:** Two surfaces exist in parallel. The **App surface** uses database-backed `AppExtension` records validated through Pydantic manifests (`ManifestExtensionSchema`, `RequiredSaleorVersionSpec`) and exposed via `AppQueries`/`AppExtension` GraphQL types. The **Plugin/Webhook surface** uses `BasePlugin` subclasses (including the built-in `WebhookPlugin`) managed by a central plugin manager that runs each plugin's methods in sequence per event, with payment webhooks handled separately by `__run_payment_webhook`.
