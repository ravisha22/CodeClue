# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-saleor-struct-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.


--- ARCHITECTURAL CONTEXT (LLM-generated, one-time) ---
Saleor
-- ARCH (LLM-generated architectural summary, ~500 tokens)
Framework: Django 5.2.x (Saleor 3.24.0-a.0) with Graphene/GraphQL Core 2
Architecture: Modular Django monolith exposed primarily as an API-only GraphQL service. It behaves like a headless commerce backend: one deployable application, but decomposed internally into domain apps (product, checkout, order, payment, shipping, warehouse, discount, app, webhook, etc.) and extended through plugins/webhooks instead of in-process storefront code.
Domain model: The core commerce model centers on products, attributes, channels, warehouses/stock, checkouts, orders, payments, shipping methods, discounts, gift cards, pages/menus, accounts, apps, and webhooks. Channels are a first-class partitioning concept for pricing, currencies, stock, and publication, so catalog and fulfillment data are not just global tables but are shaped by sales channel. Checkouts evolve into orders, orders connect to payments, shipping, invoices, and fulfillment state, and apps/plugins act as external actors around the commerce lifecycle.
Data layer: PostgreSQL via Django ORM, with explicit primary/replica database configuration and a router (PrimaryReplicaRouter). The project uses standard Django migrations across many domain apps, and test setup is aware of multiple databases. The schema shows a fairly normalized relational model spread across app boundaries rather than a single giant commerce module.
API surface: GraphQL-first. saleor.urls routes /graphql/ to a custom GraphQLView backed by a federated schema assembled in graphql/api.py from per-domain query and mutation modules (AccountQueries, ProductQueries, OrderMutations, etc.). Additional HTTP endpoints are mostly operational or integration-oriented: plugin webhooks, thumbnail/image handlers, and JWKS discovery. This confirms that business capabilities are surfaced mainly through one composed GraphQL endpoint rather than many REST resources.
Auth/permissions: Authentication is centered on JWT plus a plugin-aware backend. AUTHENTICATION_BACKENDS includes JSONWebTokenBackend and PluginBackend. Permissions are Django-style codename permissions attached to users and groups, with Saleor-specific permission models/mixins. This supports staff/admin roles and external app/plugin authentication without coupling auth rules directly to the storefront.
Key workflows: (1) Catalog and channel publishing: manage products, attributes, menus, and channel-specific availability/pricing. (2) Checkout-to-order conversion: build checkout, price/reprice, apply discounts/taxes/shipping, then create order. (3) Payment and fulfillment orchestration: attach payment providers, invoices, stock/warehouse updates, and shipment logic. (4) Extensibility flow: apps/plugins receive synchronous or asynchronous webhook events and can influence business operations. (5) Media/content flow: image thumbnailing, pages, metadata, and translations support headless frontends.
Config: Configuration is environment-variable driven. settings.py reads DATABASE_URL, DATABASE_URL_REPLICA, CELERY_BROKER_URL/CLOUDAMQP_URL, SECRET_KEY, ALLOWED_HOSTS, ALLOWED_GRAPHQL_ORIGINS, email URLs, JWT/RSA settings, storage credentials, and feature flags. This is consistent with cloud/container deployment.
Dependencies: PostgreSQL primary/replica, Celery for background jobs and beat scheduling, broker backends via AMQP or SQS, SMTP/SendGrid for mail, optional cloud object storage (AWS S3, Google Cloud Storage, Azure Blob), and external apps/webhooks as integration points.
Test approach: Pytest + pytest-django with reuse-db, async/celery coverage, and extensive fixture modules registered from a root conftest.py. The test harness explicitly supports multi-database scenarios and organizes fixtures by domain app.
--- END ARCHITECTURAL CONTEXT ---

--- CLUE FILE START ---
=CC v2.1 saleor@HEAD 4239mod 27389sym
? How is Saleor split across its core platform, multichannel commerce model, and extension surfaces?


-- README
<div align="center" width="100px"> <picture>
sections: Table of Contents, What makes Saleor special?, Why API-only Architecture?, What are the tradeoffs?, Features

-- TREE
saleor/  (4237 files)
  account/  app/  asgi/  attribute/  auth/  channel/  checkout/  core/  csv/  discount/  ...+20
.env.example  README.md  conftest.py  manage.py  package.json  pyproject.toml

-- INDEX
conftest.py                                     115L  Custom, django_db_setup, pytest_addoption, pytest_collection_modifyitems, pytest_configure
manage.py                                        10L  
saleor/__init__.py                               23L  reset, PatchedSubscriberExecutionContext
saleor/__main__.py                                7L  
saleor/account/__init__.py                       46L  CustomerEvents
saleor/account/apps.py                           16L  ready, AccountAppConfig
saleor/account/error_codes.py                    72L  AccountErrorCode, CustomerBulkUpdateErrorCode, PermissionGroupErrorCode, SendConfirmationEmailErrorCode
saleor/account/events.py                        113L  assigned_email_to_a_customer_event, assigned_name_to_a_customer_event, customer_account_activated_event, customer_account_created_event, customer_account_deactivated_event
saleor/account/forms.py                          36L  get_address_form
saleor/account/i18n.py                          343L  Meta, clean, AddressForm, Meta, clean
saleor/account/i18n_rules_override.py            28L  i18n_rules_override, patched_load_validation_data
saleor/account/i18n_valid_address_extension.py    45L  AddressFieldsToSubstitute
saleor/account/lock_objects.py                    5L  user_qs_select_for_update
saleor/account/management/__init__.py             0L  
saleor/account/management/commands/__init__.py     0L  
saleor/account/management/commands/changepassword.py     3L  
saleor/account/management/commands/createsuperuser.py   284L  add_arguments, execute, get_input_data, handle, Command
saleor/account/migrations/0001_initial.py       440L  Migration
saleor/account/migrations/0002_auto_20150907_0602.py    15L  Migration
  ...and 4220 more modules

-- SYM
__run_method_on_plugins             M saleor/plugins/manager.py:211    Try to run a method with the given name on each...
get_plugins                         M saleor/plugins/manager.py:2488   Return list of plugins for a given channel.
__run_method_on_single_plugin       M saleor/plugins/manager.py:233    Run method_name on plugin.
_ensure_channel_plugins_loaded      M saleor/plugins/manager.py:151    function _ensure_channel_plugins_loaded
trigger_webhooks_async              M saleor/plugins/webhook/plugin.py:246    function trigger_webhooks_async
_serialize_payload                  M saleor/plugins/webhook/plugin.py:181    function _serialize_payload
_get_db_plugin_configs              M saleor/plugins/manager.py:201    function _get_db_plugin_configs
_load_plugin                        M saleor/plugins/manager.py:104    function _load_plugin
_get_webhooks_for_event             M saleor/plugins/webhook/plugin.py:175    function _get_webhooks_for_event
get_attribute_values                M saleor/graphql/attribute/types.py:702    function get_attribute_values
NonNullList                         C saleor/graphql/core/types/common.py:111    A list type that automatically adds non-null co...
OrderBulkError                      C saleor/graphql/order/bulk_mutations/order_bulk_create.py:91     class OrderBulkError
is_newly_created_user               M saleor/graphql/account/types.py:314    Determine if the resolver is called for newly c...
send_email                          M saleor/plugins/sendgrid/tasks.py:22     function send_email
_generate_meta                      M saleor/plugins/webhook/plugin.py:184    function _generate_meta
_get_assigned_page_attribute_for_attribute_value M saleor/graphql/page/filters.py:73     function _get_assigned_page_attribute_for_attri...
_get_assigned_product_attribute_for_attribute_value M saleor/graphql/product/filters/product_attributes.py:325    function _get_assigned_product_attribute_for_at...
__queries_or_introspection_in_selections M saleor/graphql/utils/validators.py:36     function __queries_or_introspection_in_selections
__queries_or_introspection_in_inline_fragment M saleor/graphql/utils/validators.py:58     function __queries_or_introspection_in_inline_f...
_trigger_metadata_updated_event     M saleor/plugins/webhook/plugin.py:187    function _trigger_metadata_updated_event
flatten_model_metadata              M saleor/core/migrations/0001_migrate_metadata.py:6      function flatten_model_metadata
flatten_metadata                    M saleor/core/migrations/0001_migrate_metadata.py:20     function flatten_metadata
_line_per_quantity_to_line_object   M saleor/order/events.py:17     function _line_per_quantity_to_line_object
fetch_checkout_data                 M saleor/checkout/calculations.py:843    Fetch checkout data.
_get_webhooks_for_channel_events    M saleor/plugins/webhook/plugin.py:766    Get webhooks for channel-based events.
_get_gateway_config                 M saleor/payment/gateways/braintree/plugin.py:116    function _get_gateway_config
_fetch_checkout_prices_if_expired   M saleor/checkout/calculations.py:367    Fetch checkout prices with taxes.
has_perm                            M saleor/permission/models.py:143    Return True if the user has the specified permi...
_user_has_perm                      M saleor/permission/models.py:8      Backend can raise `PermissionDenied` to short-c...
get_plugin                          M saleor/plugins/manager.py:2669   function get_plugin
fetch_order_prices_if_expired       M saleor/order/calculations.py:192    Fetch order prices with taxes.
_filter_contains_single_expression  M saleor/graphql/page/filters.py:167    function _filter_contains_single_expression
_filter_contains_single_expression  M saleor/graphql/product/filters/product_variant.py:174    function _filter_contains_single_expression
_get_gateway_config                 M saleor/payment/gateways/authorize_net/plugin.py:104    function _get_gateway_config
_filter_contains_single_expression  M saleor/graphql/product/filters/product_attributes.py:419    function _filter_contains_single_expression
_get_gateway_config                 M saleor/payment/gateways/dummy/plugin.py:67     function _get_gateway_config
_get_gateway_config                 M saleor/payment/gateways/dummy_credit_card/plugin.py:67     function _get_gateway_config
call_order_events                   M saleor/order/actions.py:244    function call_order_events
stripe_otel_trace                   M saleor/payment/gateways/stripe/stripe_api.py:32     function stripe_otel_trace
encode                              M saleor/core/hashers.py:18     function encode
pbkdf2_round                        M saleor/core/hashers.py:30     PBKDF2 round (salt + secure hash function added).
call_order_event                    M saleor/order/actions.py:266    function call_order_event
get_default_user_payload            M saleor/account/notifications.py:11     function get_default_user_payload
update_errors                       M saleor/graphql/account/mutations/permission_group/permission_group_create.py:262    Create ValidationError and add it to error list.
_get_assigned_variant_attribute_for_attribute_value_qs M saleor/graphql/product/filters/product_variant.py:155    function _get_assigned_variant_attribute_for_at...
resolve_product_variants            M saleor/graphql/product/types/products.py:1546   function resolve_product_variants
_get_metadata_instance              M saleor/graphql/meta/types.py:41     function _get_metadata_instance
clean_input                         M saleor/graphql/product/mutations/product/product_update.py:65     function clean_input
clean_input                         M saleor/graphql/product/mutations/product/product_create.py:140    function clean_input
_resolve_product_variants           M saleor/graphql/product/types/products.py:1549   function _resolve_product_variants
clean_input                         M saleor/graphql/product/mutations/product_variant/product_variant_update.py:111    function clean_input
clean_attributes                    M saleor/graphql/product/mutations/product/product_create.py:153    function clean_attributes
clean_attributes                    M saleor/graphql/product/mutations/product/product_update.py:78     function clean_attributes
clean_attributes                    M saleor/graphql/product/mutations/product_variant/product_variant_update.py:130    function clean_attributes
clean_input                         M saleor/graphql/page/mutations/page_create.py:81     function clean_input
  ...and 13206 more symbols

-- FOCUS
saleor/settings.py (saleor/settings.py:1-1261)
  Config summary for saleor/settings.py: entries: SOFT_MEMORY_LIMIT_IN_MB=os.environ.get('SOFT_MEMORY_LIMIT_IN_MB', None), HARD_MEMORY_LIMIT_IN_MB=os.environ.get('HARD_MEMORY_LIMIT_IN_MB', None), DEBUG=get_bool_from_env('DEBUG', True), SITE_ID=1, PROJECT_ROOT=os.path.normpath(os.path.join(os.path.dirname(__file__), '..')), ROOT_URLCONF='saleor.urls'
  entries: SOFT_MEMORY_LIMIT_IN_MB=os.environ.get('SOFT_MEMORY_LIMIT_IN_MB', None), HARD_MEMORY_LIMIT_IN_MB=os.environ.get('HARD_MEMORY_LIMIT_IN_MB', None), DEBUG=get_bool_from_env('DEBUG', True), SITE_ID=1, PROJECT_ROOT=os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))

saleor/tests/settings.py (saleor/tests/settings.py:1-105)
  Config summary for saleor/tests/settings.py: entries: POPULATE_DEFAULTS=False, CELERY_TASK_ALWAYS_EAGER=True, PUBLIC_URL='https://example.com', SECRET_KEY='NOTREALLY', ALLOWED_CLIENT_HOSTS=['www.example.com'], EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
  entries: POPULATE_DEFAULTS=False, CELERY_TASK_ALWAYS_EAGER=True, PUBLIC_URL='https://example.com', SECRET_KEY='NOTREALLY', ALLOWED_CLIENT_HOSTS=['www.example.com']

.env.example (.env.example:1-8)
  Config summary for .env.example: entries: CACHE_URL=redis://localhost:6379/0, CELERY_BROKER_URL=redis://localhost:6379/1, DEFAULT_FROM_EMAIL=noreply@example.com, EMAIL_URL=smtp://localhost:1025, SECRET_KEY=changeme, HTTP_IP_FILTER_ALLOW_LOOPBACK_IPS=True
  entries: CACHE_URL=redis://localhost:6379/0, CELERY_BROKER_URL=redis://localhost:6379/1, DEFAULT_FROM_EMAIL=noreply@example.com, EMAIL_URL=smtp://localhost:1025, SECRET_KEY=changeme

ModelWithRestrictedChannelAccessMutation (saleor/graphql/core/mutations.py:895-938)
  extends: DeprecatedModelMutation
  imports: secrets, enum, itertools, uuid, graphene
  calls: check_channel_permissions, construct_instance, create_metadata_from_graphql_input, validate_and_update_metadata, _save_m2m, post_save_action, save, success_response
  raises: NotImplementedError
  uses: PermissionDenied (core.exceptions), ValidationError (django.core.exceptions)

ModelDeleteWithRestrictedChannelAccessMutation (saleor/graphql/core/mutations.py:971-997)
  extends: ModelDeleteMutation
  imports: secrets, enum, itertools, uuid, graphene
  calls: check_channel_permissions, post_save_action, success_response
  raises: NotImplementedError
  uses: PermissionDenied (core.exceptions)

SortableModel (saleor/core/models.py:16-45)
  extends: Model
  imports: django.contrib.postgres.indexes, django.core.files.base, django.db, django.db.models, django.utils.crypto
  calls: delete, get_max_sort_order, get_ordering_queryset, save
  raises: NotImplementedError
  uses: F (django.db.models), Max (django.db.models)

ModelDeleteMutation (saleor/graphql/core/mutations.py:941-968)
  extends: DeprecatedModelMutation
  imports: secrets, enum, itertools, uuid, graphene
  calls: post_save_action, success_response

ModelWithExtRefMutation (saleor/graphql/core/mutations.py:864-892)
  extends: DeprecatedModelMutation
  imports: secrets, enum, itertools, uuid, graphene
  calls: get_object_id

ModelWithExternalReference (saleor/core/models.py:128-138)
  extends: Model
  imports: django.contrib.postgres.indexes, django.core.files.base, django.db, django.db.models, django.utils.crypto

ModelWithMetadata (saleor/core/models.py:80-125)
  extends: Model
  imports: django.contrib.postgres.indexes, django.core.files.base, django.db, django.db.models, django.utils.crypto

PublishableModel (saleor/core/models.py:63-77)
  extends: Model
  imports: django.contrib.postgres.indexes, django.core.files.base, django.db, django.db.models, django.utils.crypto

StrictBaseModel (saleor/core/editorjs/models.py:42-52)
  Strict version of the pydantic BaseModel.
  extends: UnsafeBaseModel
  imports: django.conf, django.core.exceptions, pydantic, cleaners, utils

ModelMutationOptions (saleor/graphql/core/mutations.py:131-136)
  extends: MutationOptions
  attrs: doc_category=None, exclude=None, model=None, object_type=None
  imports: secrets, enum, itertools, uuid, graphene
  called_by: BaseBulkMutation, DeprecatedModelMutation

ModelBulkDeleteMutation (saleor/graphql/core/mutations.py:1125-1131)
  extends: BaseBulkMutation
  imports: secrets, enum, itertools, uuid, graphene

ModelObjectOptions (saleor/graphql/core/types/model.py:12-13)
  extends: ObjectTypeOptions
  attrs: model=None
  imports: uuid, django.db.models, graphene.types.objecttype, doc_category, base
  called_by: __init_subclass_with_meta__, ModelObjectType

ModelObjectType (saleor/graphql/core/types/model.py:19-85)
  extends: BaseObjectType
  imports: uuid, django.db.models, graphene.types.objecttype, doc_category, base
  calls: ModelObjectOptions, __init_subclass_with_meta__
  raises: ValueError

AppExtension (saleor/graphql/app/types.py:172-273)
  extends: AppManifestExtension
  imports: base64, graphene, graphql, app, app.types
  raises: PermissionDenied

AppExtension (saleor/app/models.py:155-174)
  extends: Model
  imports: uuid, django.contrib.auth.hashers, django.db, django.utils.text, oauthlib.common

ManifestExtensionSchema (saleor/app/manifest_schema.py:53-61)
  extends: BaseModel
  imports: mimetypes, django.core.exceptions, pydantic, pydantic.alias_generators, pydantic_core

SeoModel (saleor/seo/models.py:7-16)
  extends: Model
  imports: django.core.validators, django.db, core.utils.translations

SeoModelTranslationWithSlug (saleor/seo/models.py:37-47)
  extends: SeoModelTranslation
  imports: django.core.validators, django.db, core.utils.translations

AppExtensionCountableConnection (saleor/graphql/app/types.py:276-279)
  extends: CountableConnection
  imports: base64, graphene, graphql, app, app.types

AppExtensionFilter (saleor/graphql/app/filters.py:45-58)
  extends: FilterSet
  imports: django_filters, graphene, app, app.types, core.descriptions

AppExtensionFilterInput (saleor/graphql/app/schema.py:54-57)
  extends: FilterInputObjectType
  imports: graphene, core.exceptions, permission.auth_filters, permission.enums, core
  called_by: AppQueries

AppManifestExtension (saleor/graphql/app/types.py:115-164)
  extends: BaseObjectType
  imports: base64, graphene, graphql, app, app.types

CoreAppConfig (saleor/core/apps.py:11-37)
  extends: AppConfig
  attrs: name='saleor.core'
  imports: django.apps, django.conf, django.db.models, django.utils.module_loading, db.filters
  calls: validate_jwt_manager
  raises: ImportError

CoreErrorCode (saleor/core/error_codes.py:37-38)
  extends: Enum
  attrs: GRAPHQL_ERROR='graphql_error'
  imports: enum

CoreMutations (saleor/graphql/core/schema.py:27-28)
  extends: ObjectType
  imports: graphene, core.doc_category, core.fields, plugins.dataloaders, mutations

CoreQueries (saleor/graphql/core/schema.py:11-24)
  extends: ObjectType
  imports: graphene, core.doc_category, core.fields, plugins.dataloaders, mutations

ModelData (saleor/thumbnail/views.py:36-39)
  extends: NamedTuple
  imports: logging, django.conf, django.core.exceptions, django.http, graphql.error

SaleorContext (saleor/graphql/core/context.py:16-29)
  extends: HttpRequest
  imports: django.conf, django.db.models, django.http, django.utils.functional, account.models

SaleorProvider (saleor/core/utils/random_data.py:479-484)
  extends: BaseProvider
  imports: itertools, random, unicodedata, uuid, decimal

SeoModelTranslation (saleor/seo/models.py:19-34)
  extends: Translation
  imports: django.core.validators, django.db, core.utils.translations

AppManifestRequiredSaleorVersion (saleor/graphql/app/types.py:315-326)
  extends: BaseObjectType
  imports: base64, graphene, graphql, app, app.types

RequiredSaleorVersionSpec (saleor/app/manifest_validations.py:36-41)
  extends: NpmSpec
  imports: logging, django.core.exceptions, django.db.models, django.db.models.functions, pydantic
  called_by: _clean_required_saleor_version

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 83 symbols in L3, 12 with behavior annotations
uncovered: move_email_templates_to_separate_model, perform_model_extra_actions, reorder_model, resolve_access_token_for_app_extension

--- CLUE FILE END ---

QUESTION: How is Saleor split across its core platform, multichannel commerce model, and extension surfaces?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
