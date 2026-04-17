# Enterprise v2: ent-saleor-struct-2
Date: 2026-04-17

## Question
How is the Saleor repository organized for app modules, GraphQL APIs, and tests?

## Reasoning Scaffold

### Step 1: Repository Root and Top-Level Layout (TREE, INDEX)

The root contains `manage.py` (10L), `conftest.py` (115L), `pyproject.toml`, `package.json`, `.env.example`, and `README.md` (TREE, INDEX). The single `saleor/` package (4237 files) contains all application code, while test infrastructure is split between root-level `conftest.py` and `saleor/tests/settings.py` (FOCUS).

The TREE enumerates the first ten domain submodules: `account/`, `app/`, `asgi/`, `attribute/`, `auth/`, `channel/`, `checkout/`, `core/`, `csv/`, `discount/`, plus 20 more (TREE). This establishes a **flat, domain-first** internal package layout.

### Step 2: App Module Organization (INDEX, FOCUS)

Each domain module follows a consistent internal layout, observable from `saleor/account/`:

- `__init__.py` — exports domain-level enums (e.g., `CustomerEvents`) (INDEX)
- `apps.py` — `AppConfig` subclass (e.g., `AccountAppConfig` with `ready` hook) (INDEX)
- `error_codes.py` — domain error code enums (e.g., `AccountErrorCode`, `CustomerBulkUpdateErrorCode`, `PermissionGroupErrorCode`) (INDEX)
- `events.py` — domain event emission functions (e.g., `customer_account_created_event`) (INDEX)
- `forms.py` — optional Django forms (e.g., `get_address_form`) (INDEX)
- `i18n.py` — internationalisation support (e.g., `AddressForm`) (INDEX)
- `migrations/` — versioned schema migration files (INDEX)
- `management/commands/` — custom Django management commands (e.g., `createsuperuser`, `changepassword`) (INDEX)
- `lock_objects.py` — DB locking helpers (e.g., `user_qs_select_for_update`) (INDEX)
- `notifications.py` — notification payload helpers (e.g., `get_default_user_payload`) (SYM)

The `saleor/core/` module contains shared base model classes: `SortableModel`, `ModelWithMetadata`, `PublishableModel`, `ModelWithExternalReference` (all from `saleor/core/models.py`) (FOCUS). `CoreAppConfig` (`saleor/core/apps.py`) acts as the core Django app with startup validation (FOCUS).

The `saleor/app/` module has its own model layer: `AppExtension` (`saleor/app/models.py:155-174`), manifest schema (`saleor/app/manifest_schema.py`) and manifest validations (`saleor/app/manifest_validations.py`) (FOCUS).

The `saleor/plugins/` module hosts the plugin manager (`saleor/plugins/manager.py`) and the webhook plugin (`saleor/plugins/webhook/plugin.py`), with per-integration sub-packages under `saleor/payment/gateways/` (SYM).

### Step 3: GraphQL API Organization (FOCUS, SYM)

The GraphQL layer lives under `saleor/graphql/` and mirrors the domain module structure:

- Each domain has a `schema.py` containing a `*Queries` and/or `*Mutations` `ObjectType` subclass:
  - `AppQueries` (`saleor/graphql/app/schema.py:60-175`) — exposes `resolve_app`, `resolve_app_extensions`, `resolve_apps`, `resolve_apps_installations` (FOCUS)
  - `AccountQueries` (`saleor/graphql/account/schema.py:117-283`) — imports `permission.auth_filters`, `permission.enums`, `permission.utils` (FOCUS)
  - `ProductQueries` (`saleor/graphql/product/schema.py:141-638`) (FOCUS)
  - `DiscountQueries` (`saleor/graphql/discount/schema.py:74-202`) (FOCUS)
  - `OrderQueries` (`saleor/graphql/order/schema.py:102-271`) (FOCUS)
  - `PageQueries` (`saleor/graphql/page/schema.py:38-150`) (FOCUS)
  - `MenuQueries` (`saleor/graphql/menu/schema.py:32-116`) (FOCUS)
  - `CoreQueries` / `CoreMutations` (`saleor/graphql/core/schema.py`) (FOCUS)

- Each domain's `types.py` defines `ModelObjectType` subclasses (e.g., `App` at `saleor/graphql/app/types.py:645-825`, `AppExtension` at `:172-273`, `AppManifestExtension` at `:115-164`) (FOCUS).
- Each domain's `mutations/` directory contains mutation classes. Mutations follow an inheritance hierarchy: `BaseMutation` → `DeprecatedModelMutation` → `ModelWithRestrictedChannelAccessMutation` / `ModelDeleteWithRestrictedChannelAccessMutation` / `ModelBulkDeleteMutation` etc. (FOCUS).
- Shared mutation configuration is held in `ModelMutationOptions` (`saleor/graphql/core/mutations.py:131-136`), which stores `doc_category`, `exclude`, `model`, `object_type` (FOCUS).
- Cross-domain type utilities live in `saleor/graphql/core/types/` — e.g., `NonNullList` (`saleor/graphql/core/types/common.py:111`), `ModelObjectType` (`saleor/graphql/core/types/model.py`) (SYM, FOCUS).
- Dataloaders follow a `*ByIdLoader` / `*ByTokenLoader` pattern. `AppByTokenLoader` (`saleor/graphql/app/dataloaders/app.py:49-113`) caches app lookups by token; `AppByIdLoader` is referenced by multiple `resolve_app` resolvers across CSV, account, giftcard, order types (FOCUS).
- `get_app_promise` and `promise_app` (`saleor/graphql/app/dataloaders/utils.py`) manage async app context resolution (FOCUS).
- The `SaleorContext` (`saleor/graphql/core/context.py:16-29`) extends `HttpRequest`, providing per-request app/user context to all resolvers (FOCUS).
- GraphQL schema printing utilities in `saleor/graphql/schema_printer.py` support custom directives for webhook event annotations.

### Step 4: Test Organization (FOCUS, INDEX)

- `conftest.py` (root, 115L) registers pytest plugins: `django_db_setup`, `pytest_addoption`, `pytest_collection_modifyitems`, `pytest_configure`, and `Custom` fixtures (INDEX, FOCUS).
- `saleor/tests/settings.py` (105L) contains test-specific overrides: `POPULATE_DEFAULTS=False`, `CELERY_TASK_ALWAYS_EAGER=True` (so tasks run synchronously in tests), `PUBLIC_URL='https://example.com'`, `SECRET_KEY='NOTREALLY'`, `ALLOWED_CLIENT_HOSTS=['www.example.com']`, `EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'` (FOCUS).
- The INDEX shows `saleor/account/migrations/0001_initial.py` (440L) and subsequent migrations — tests therefore run against a fully migrated schema.
- The `saleor/__init__.py` (23L) exports `reset` and `PatchedSubscriberExecutionContext`, the latter suggesting GraphQL subscription execution is patched for test isolation (INDEX).
- The clue does not directly expose per-module `tests/` directories, but the INDEX shows migrations and management commands co-located with domain modules, consistent with tests living under `saleor/<domain>/tests/`.

### Gaps / Uncertainty

Per GAPS (type: STRUCTURAL, coverage: 83 symbols in L3, 10 with behavior annotations):
- `AppToken`, `AppTokenDelete`, `AppTokenVerify`, `AppTokensByAppIdLoader` are explicitly listed as uncovered.
- The full list of 20+ additional TREE modules beyond the first 10 is not shown; those modules follow the same pattern by inference but cannot be confirmed individually.
- The exact structure of per-domain `tests/` directories (whether co-located or consolidated under `saleor/tests/`) is not determinable from the INDEX (only the root `conftest.py` and `saleor/tests/settings.py` are directly visible).

## Synthesized Answer

**App Modules:** `saleor/` uses a flat, domain-first layout where each business domain (account, app, channel, checkout, discount, order, payment, product, etc.) is a self-contained Django app with a standard internal structure: `apps.py`, `error_codes.py`, `events.py`, `models.py`, `migrations/`, optional `management/commands/`, and `lock_objects.py`. Shared base models (`SortableModel`, `ModelWithMetadata`, etc.) live in `saleor/core/models.py`. The App/Plugin extension system is in `saleor/app/` and `saleor/plugins/`.

**GraphQL APIs:** A parallel `saleor/graphql/` tree mirrors the domain layout. Each domain contributes a `schema.py` (with `*Queries`/`*Mutations` ObjectTypes), `types.py` (ModelObjectType subclasses), `mutations/` (mutation classes), `filters.py`, and `dataloaders/`. Cross-cutting utilities are in `saleor/graphql/core/`. Mutations inherit from a shared hierarchy rooted at `BaseMutation`/`DeprecatedModelMutation`, and dataloaders use a consistent `*ByIdLoader`/`*ByTokenLoader` pattern.

**Tests:** Root `conftest.py` provides global pytest configuration; `saleor/tests/settings.py` provides test-specific Django settings (CELERY eager, in-memory email backend, fixed secrets). The `saleor/__init__.py` patches the GraphQL subscriber execution context for test isolation.
