# Enterprise Eval: ent-saleor-struct-2
Date: 2026-04-17

## Question
How is the Saleor repository organized for app modules, GraphQL APIs, and tests?

---

## Reasoning Trace

### Step 1: Top-Level Repository Organization (TREE & INDEX)

The TREE shows the repository root contains:
- `saleor/` — the main package (4237 files), subdivided into domain packages: `account/`, `app/`, `asgi/`, `attribute/`, `auth/`, `channel/`, `checkout/`, `core/`, `csv/`, `discount/`, plus 20+ more (TREE, line 21).
- `conftest.py` (115L) — root-level pytest configuration with `django_db_setup`, `pytest_addoption`, `pytest_collection_modifyitems`, `pytest_configure`, and a `Custom` fixture/class (INDEX, line 25).
- `manage.py` (10L) — Django management entry point (INDEX, line 26).

### Step 2: App Module Organization

**The `saleor/app/` package** is a dedicated domain module for third-party app management. Evidence from FOCUS:

- **Models:** `AppExtension` (saleor/app/models.py:155-174) extends Django `Model`; imports include `uuid`, `django.contrib.auth.hashers`, `django.db`, `django.utils.text`, `oauthlib.common` — indicating apps have OAuth-based authentication (FOCUS).
- **Manifest handling:** `ManifestExtensionSchema` (saleor/app/manifest_schema.py:53-61) extends pydantic `BaseModel` for validating app manifests. `RequiredSaleorVersionSpec` (saleor/app/manifest_validations.py:36-41) extends `NpmSpec` for version constraint validation (FOCUS from struct-1 clue, referenced here).
- **Dataloaders:** `AppByTokenLoader` (saleor/graphql/app/dataloaders/app.py:49-113, `context_key='app_by_token'`) loads apps by auth token; calls `get_and_cache_app_id`, `remove_not_valid_tokens_from_cache`, `TokenInfo`. Also `create_app_cache_key_from_token` (saleor/graphql/app/dataloaders/app.py:15-17) (FOCUS).
- **Dataloader utilities:** `get_app_promise` (saleor/graphql/app/dataloaders/utils.py:20-27) guards on `hasattr(context, 'app')` and returns `Promise.resolve(app)`, calling `promise_app` (FOCUS). `promise_app` (saleor/graphql/app/dataloaders/utils.py:13-17) uses `AppByTokenLoader` (FOCUS).

**Each domain module** follows a consistent internal structure visible in the INDEX. Taking `account/` as an example:
- `__init__.py` — module-level constants/enums (e.g., `CustomerEvents`) (INDEX, line 29)
- `apps.py` — Django AppConfig with `ready()` hook (e.g., `AccountAppConfig`) (INDEX, line 30)
- `error_codes.py` — domain-specific error enums (e.g., `AccountErrorCode`, `CustomerBulkUpdateErrorCode`) (INDEX, line 31)
- `events.py` — event recording functions (INDEX, line 32)
- `forms.py` — Django forms (INDEX, line 33)
- `i18n.py` — internationalization (INDEX, line 34)
- `management/commands/` — CLI commands like `createsuperuser.py` (INDEX, lines 39-41)
- `migrations/` — database migrations (INDEX, lines 42-43)

### Step 3: GraphQL API Organization

The GraphQL layer lives in `saleor/graphql/` and mirrors the domain structure. Each domain has its own GraphQL sub-package:

**Per-domain schema modules (from FOCUS):**
- `saleor/graphql/app/schema.py` — `AppQueries` (lines 60-175) extends `ObjectType`; resolves `resolve_app`, `resolve_app_extensions`, `resolve_apps`, `resolve_apps_installations`. Uses `AppExtensionFilterInput`, `AppFilterInput`. Raises `PermissionDenied` (FOCUS).
- `saleor/graphql/app/types.py` — houses multiple GraphQL types: `App` (lines 645-825), `AppExtension` (lines 172-273), `AppManifestExtension` (lines 115-164), `AppManifestRequiredSaleorVersion` (lines 315-326) (FOCUS).
- `saleor/graphql/app/filters.py` — `AppExtensionFilter` (lines 45-58) extends `FilterSet` (FOCUS).

**Per-domain mutation modules (from FOCUS):**
- `AppCreate` (saleor/graphql/app/mutations/app_create.py:36-99) extends `DeprecatedModelMutation`; has `AppInput` (lines 19-33) as input type (FOCUS).
- `AppInstall` (saleor/graphql/app/mutations/app_install.py:44-85) extends `DeprecatedModelMutation` (FOCUS).
- `AppTokenCreate` (saleor/graphql/app/mutations/app_token_create.py:26-69) extends `DeprecatedModelMutation`; uses `AppTokenInput` (FOCUS).
- `AppFetchManifest` (saleor/graphql/app/mutations/app_fetch_manifest.py:18-122) extends `BaseMutation` (FOCUS).
- `AppProblemCreate` (saleor/graphql/app/mutations/app_problem_create.py:93-202) extends `BaseMutation` (FOCUS).
- `AppProblemDismiss` (saleor/graphql/app/mutations/app_problem_dismiss.py:102-327) extends `BaseMutation`; has `AppProblemDismissInput` (lines 82-99) (FOCUS).

**Consistent GraphQL sub-patterns visible from SYM and FOCUS:**
- **Types** modules: `saleor/graphql/account/types.py`, `saleor/graphql/product/types/products.py`, `saleor/graphql/page/schema.py`, etc. (SYM).
- **Mutations** modules: `saleor/graphql/product/mutations/product/product_create.py`, `product_update.py`, `saleor/graphql/page/mutations/page_create.py`, etc. — with `clean_input` and `clean_attributes` methods (SYM).
- **Filters** modules: `saleor/graphql/product/filters/product_attributes.py`, `product_variant.py`, `saleor/graphql/page/filters.py` (SYM).
- **Schema** modules: each domain has a `schema.py` defining `*Queries` ObjectTypes (SYM, FOCUS).
- **Dataloaders** modules: e.g., `saleor/graphql/app/dataloaders/` (FOCUS).

**Core GraphQL infrastructure (from SYM):**
- `NonNullList` (saleor/graphql/core/types/common.py:111) — shared list type (SYM).
- `get_form_field_description` (saleor/graphql/core/types/converter.py:24) — form-to-GraphQL conversion (SYM).
- Validators: `__queries_or_introspection_in_selections` (saleor/graphql/utils/validators.py:36) and `__queries_or_introspection_in_inline_fragment` (saleor/graphql/utils/validators.py:58) — query/introspection validation (SYM).

**App resolution across domains (from FOCUS):** `resolve_app` appears in multiple GraphQL type modules, each loading via `AppByIdLoader`:
- `saleor/graphql/giftcard/types.py:139` (FOCUS)
- `saleor/graphql/csv/types.py:63, :106` (FOCUS)
- `saleor/graphql/order/types.py:362, :576` (FOCUS)
- `saleor/graphql/account/types.py:259` (FOCUS)
- `saleor/graphql/payment/types.py:411, :780` — `get_active_app` with guard: `app and app.is_active and (not app.removed_at)` (FOCUS)
- `saleor/graphql/discount/types/promotion_events.py:62` — `_resolve_app` with permission check via `is_owner_or_has_one_of_perms` (FOCUS)

This shows the app concept is cross-cutting: many domain types reference apps through dataloaders.

### Step 4: Test Organization

**Root conftest.py** (115L) provides shared test infrastructure (INDEX, line 25):
- `django_db_setup` — database setup fixture
- `pytest_addoption` — custom CLI options for pytest
- `pytest_collection_modifyitems` — test collection customization
- `pytest_configure` — pytest configuration hook
- `Custom` — a shared fixture or test utility class

The INDEX shows `...and 4220 more modules` after the initial entries, and the overall file count is 4237. Given the domain-per-package structure, tests likely reside within or alongside domain packages, though their exact location (e.g., `tests/` subdirectories per domain vs. a top-level `tests/` directory) is not explicitly shown in the truncated TREE/INDEX.

### Step 5: GAPS — What Cannot Be Determined

Per the GAPS section:
- **Type:** STRUCTURAL (answerable from L0-L2)
- **Coverage:** 80 symbols in L3, only 10 with behavior annotations
- **Uncovered symbols:** `AppToken`, `AppTokenDelete`, `AppTokenVerify`, `AppTokensByAppIdLoader` — meaning the full lifecycle of app token management (deletion, verification) and bulk-loading tokens by app ID cannot be determined from this clue.

Additionally, the clue does not reveal:
- The exact test directory structure (whether tests are colocated with source modules or in a separate top-level `tests/` directory)
- The total number of test files vs. source files within the 4237-file count
- Whether there is a CI configuration or test runner configuration beyond the root `conftest.py`

---

## Synthesized Answer

**App Modules:** Saleor organizes domain logic into top-level packages under `saleor/` (e.g., `account/`, `app/`, `checkout/`, `channel/`, `product/`). Each follows a consistent pattern: `__init__.py` (enums/constants), `apps.py` (Django AppConfig), `error_codes.py`, `events.py`, `forms.py`, `migrations/`, and `management/commands/`. The `app/` package specifically manages third-party app lifecycle with OAuth-based token auth (`AppByTokenLoader` at saleor/graphql/app/dataloaders/app.py:49-113), manifest validation (`ManifestExtensionSchema`, `RequiredSaleorVersionSpec`), and a model layer (`AppExtension` at saleor/app/models.py:155-174).

**GraphQL APIs:** The GraphQL layer at `saleor/graphql/` mirrors the domain structure. Each domain has sub-packages for `schema.py` (query root, e.g., `AppQueries` at saleor/graphql/app/schema.py:60-175), `types.py` (GraphQL object types, e.g., `App` at saleor/graphql/app/types.py:645-825), `mutations/` (CRUD operations like `AppCreate`, `AppInstall`, `AppTokenCreate`), `filters.py` (Django-filter integration, e.g., `AppExtensionFilter`), and `dataloaders/` (batched data loading, e.g., `AppByTokenLoader`). The app concept is cross-cutting — `resolve_app` resolvers appear across gift card, CSV, order, account, payment, and discount types, all using `AppByIdLoader`.

**Tests:** The root `conftest.py` (115L) provides shared pytest infrastructure: `django_db_setup`, `pytest_addoption`, `pytest_collection_modifyitems`, and `pytest_configure`. The exact location of individual test files within the 4237-file count cannot be determined from the truncated TREE/INDEX (GAPS limitation).
