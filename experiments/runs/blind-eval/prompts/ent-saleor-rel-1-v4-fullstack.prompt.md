# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-saleor-rel-1

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

--- DEEP DOMAIN CONTEXT (LLM-generated from key files, one-time) ---
-- DOMAIN MODEL (Django models, ~800 tok)
Saleor’s commerce core is anchored on Product, Checkout, Order, Payment, Inventory, Shipping, and Identity models, with Channel and TaxClass acting as important cross-cutting references. In product/models.py, Category is a metadata + SEO-aware MPTT tree; products belong to a category and a ProductType, and categories can nest via parent -> children. ProductType defines structural behavior: kind, whether shipping is required, whether the type is digital, whether variants exist, and an optional tax_class. Product is the sellable catalog parent: it references ProductType and Category, carries SEO/search fields, timestamps, an optional default_variant, and an optional tax_class override. ProductVariant is the operational SKU-level entity: it belongs to a Product, has sku/name, supports media M2M, track_inventory, preorder settings, quantity-per-customer limits, and pricing logic methods such as get_base_price, get_price, get_weight, is_shipping_required, is_gift_card, and is_preorder_active. Channel-specific commerce state is not stored directly on Product/ProductVariant; it lives in ProductChannelListing and ProductVariantChannelListing, which attach catalog visibility, availability dates, currency, list price, cost price, prior price, discounted price, preorder thresholds, and promotion_rules to a given Channel. Collection and CollectionProduct form a merchandising grouping layer, while ProductMedia and VariantMedia capture images/external media attachment.

Order is the durable sales record. order/models.py shows Order as a large aggregate rooted by UUID/number, with user, billing/shipping address snapshots, channel/currency, status, authorize_status, charge_status, origin, tracking, language, and money totals. Its methods reveal business semantics: is_fully_paid / is_partly_paid, is_pre_authorized / is_captured, can_cancel / can_capture / can_void / can_refund / can_mark_as_paid, plus total_balance and shipping/quantity helpers. OrderLine is a denormalized snapshot of the purchased variant: it links back to Order and optionally ProductVariant, but also copies product_name, variant_name, SKU, product type id, shipping/gift-card flags, quantity and price/discount fields so the order survives catalog changes. Fulfillment and FulfillmentLine represent post-purchase logistics; a fulfillment belongs to an order, has status, tracking, optional refund amounts, and lines that point back to order lines and optionally the stock row used. OrderEvent is the event log for lifecycle changes, and OrderGrantedRefund / OrderGrantedRefundLine model approved refund intents tied to orders, lines, users/apps, and optionally a TransactionItem.

Checkout is the pre-order aggregate. checkout/models.py centers on Checkout, keyed by token, with optional user/email, channel, billing/shipping addresses, selected shipping_method or collection_point warehouse, note, currency, completion lock timestamps, authorization state, and helper methods like is_shipping_required, is_checkout_locked, get_last_active_payment, get_total_gift_cards_balance, and country setters/getters. CheckoutLine is the mutable cart line: it binds checkout to ProductVariant with quantity, gift flag, optional price override, stored undiscounted/prior price, total taxed price, and tax rate. CheckoutDelivery is an enterprise addition that stores delivery options as first-class rows, including internal vs external shipping ids, label/description, price, ETA bounds, metadata/private_metadata, validity flags, and tax_class_id; it lets checkout support multiple cached delivery choices and app-provided shipping methods. CheckoutMetadata is a one-to-one metadata store.

Account/auth models provide actors and address book data. Address is reusable and copyable via as_data/get_copy. User extends AbstractBaseUser + PermissionsMixin + metadata/external-reference mixins; it uses email as username, links M2M to Address, stores default billing/shipping addresses, avatar, jwt_token_key, language, search fields, uuid, and a denormalized number_of_orders. Its effective_permissions property merges direct user permissions with permissions inherited through Group. Group adds an enterprise permission scoping concept: besides permissions M2M, it can restrict access_to_channels via a channels M2M. CustomerNote and CustomerEvent attach CRM-style notes/events to users.

Payments are modeled in two layers. The older Payment aggregate is checkout/order-linked and gateway-oriented: gateway, charge_status, token, total, captured amount, billing snapshot fields, and capability methods such as can_authorize/capture/void/refund/confirm. Transaction is the legacy event row under Payment. The newer, more app-centric model is TransactionItem: it tracks authorized/charged/refunded/canceled/refund-pending balances, PSP references, idempotency key, available actions, and metadata. TransactionEvent records the external payment/timeline events attached to a TransactionItem, including amount, type, PSP reference, app/user origin, whether it participates in calculations, and links to granted refunds.

Inventory and shipping close the loop. Warehouse belongs to channels and shipping zones, has an Address, email, click-and-collect mode, and privacy flag. Stock is the on-hand quantity for a ProductVariant in a Warehouse, with quantity and quantity_allocated plus increase_stock/decrease_stock helpers. Allocation ties an OrderLine to a Stock row; Reservation ties a CheckoutLine to temporary reserved stock; preorder has separate PreorderAllocation and PreorderReservation records against ProductVariantChannelListing. ShippingZone groups countries/channels/warehouses; ShippingMethod belongs to a zone, can exclude products, has type, delivery-day hints, and optional tax_class. ShippingMethodChannelListing adds per-channel currency, min/max order price constraints, and price. Overall ER picture: catalog entities are channel-listed and stocked in warehouses; checkout lines reference variants and reserve stock; completion converts checkout/address/shipping/payment state into order/order-line/payment/fulfillment-ready records.

-- API SURFACE (GraphQL, ~300 tok)
Saleor exposes a single federated GraphQL schema from saleor/graphql/api.py. The root Query type is composed from mixins for account, app, attribute, channel, checkout, core, CSV, discount, plugins, gift card, menu, order, page, payment, product, shipping, shop, stock, tax, translation, warehouse, and webhook queries. Mutation is similarly composed from domain mixins, so GraphQL mirrors the bounded contexts in the Django apps rather than one monolith.

On the commerce path, CheckoutQueries exposes checkout, checkouts, and checkout_lines. CheckoutMutations covers cart lifecycle and conversion: checkout_create, checkout_lines_add/update/delete, shipping/billing/email/language updates, promo code add/remove, customer attach/detach, checkout_payment_create, checkout_complete, and order_create_from_checkout. These mutations map directly to Checkout, CheckoutLine, Address, Payment, and finally Order.

OrderQueries exposes order, orders, draft_orders, homepage_events, orders_total, and deprecated order_by_token. OrderMutations maps to the Order aggregate and downstream logistics/finance actions: draft_order_create/update/complete/delete, order_cancel, order_confirm, order_capture, order_void, order_refund, order_mark_as_paid, order_update_shipping, order_fulfill, fulfillment cancel/approve/update-tracking/refund/return, order line CRUD, order/order-line discount mutations, notes, bulk cancel, and bulk create.

PaymentQueries exposes payment(s), transaction, and transactions. PaymentMutations spans both legacy and new payment APIs: payment_capture/refund/void/initialize/check_balance, checkout_payment_create, plus transaction_create/update/request_action/event_report/initialize/process and tokenization/stored-payment-method flows. In short: GraphQL types are thin façades over the Django aggregates, with mutations delegating into checkout completion, order actions, payment gateway orchestration, and warehouse allocation logic.

-- ROUTING (~100 tok)
HTTP routing is intentionally minimal in saleor/urls.py. The primary public surface is ^graphql/$, served by GraphQLView with the federated schema and backend. Separate webhook-style endpoints exist for plugins: per-channel, global, and generic plugin callbacks. Media infrastructure is also routed here: thumbnail generation, original image serving, and JWKS at .well-known/jwks.json. In DEBUG mode, Saleor additionally serves /media/, /static/, and a simple home view. There are effectively no large REST sub-app URL trees; most business functionality is consolidated behind GraphQL plus webhook/media endpoints.

-- AUTH/PERMISSIONS (~200 tok)
Saleor blends Django auth with app-based auth. Human users are account.User records; machine actors are app.App plus AppToken. Permission constants live in permission/enums.py as namespaced values such as order.manage_orders, checkout.handle_checkouts, payment.handle_payments, etc. Users inherit direct permissions and group permissions through effective_permissions; groups can additionally restrict staff access to specific channels, so authorization is not just role-based but channel-scoped. Apps own explicit Permission M2M rows and implement has_perm/has_perms similarly, but only while active.

permission/utils.py provides the policy combinators used across GraphQL: all_permissions_required, one_of_permissions_or_auth_filter_required, permission_required, and has_one_of_permissions. This lets resolvers/mutations accept either strict permission checks or richer authorization filters. Request context in graphql/core/context.py carries user, app, requestor, decoded token data, dataloaders, and a replica-routing flag.

Authentication itself is token-centric. core/middleware.py extracts bearer/JWT tokens from either a custom Saleor header or standard Authorization. core/auth.py adds JWT refresh-token cookie handling to responses. So the auth model is: JWT/app token identifies a requestor, GraphQL context resolves it to User or App, and permission checks are enforced at field/mutation boundaries with optional channel-aware scoping.

-- KEY WORKFLOWS (~300 tok)
The checkout-to-order flow is implemented mainly in checkout/checkout_cleaner.py, checkout/complete_checkout.py, and exposed through GraphQL checkout_complete / order_create_from_checkout. First, the mutation loads Checkout plus CheckoutLineInfo via fetch_checkout_lines and fetch_checkout_info, then validates invariant data: channel must be active, lines must exist, email must be set, billing must exist, shipping method/address must be valid when shipping is required, voucher/gift cards must still be applicable, and plugin-based tax/order-preprocessing hooks must succeed.

From there Saleor chooses one of two completion paths. If the checkout is already fully authorized, already uses transaction flow, is zero-value, or the channel allows unpaid orders, it uses the transaction-based path and directly calls create_order_from_checkout. Otherwise it enters the payment path: it locks the checkout row, records completing_started_at, prepares order_data, temporarily reserves stock, then processes the active Payment outside the DB transaction so stock rows are not held during gateway latency. If the gateway requires extra action (for example 3DS), checkout_complete returns confirmation_needed/confirmation_data and does not yet create the order.

When payment succeeds or a transaction-based checkout is ready, _create_order / _create_order_from_checkout converts the aggregate. It computes totals, shipping, taxes, voucher usage, user/address snapshots, and line discount objects; creates the Order and bulk-creates OrderLine rows; allocates stocks and preorder quantities; moves payments/transaction items from checkout to order; stores gift card application and discount records; updates order charge/authorize/display-gross state and search vectors; then deletes the checkout. Post-commit hooks emit order_created events and confirmation notifications. Failure handlers unwind state by clearing completion locks, releasing voucher usage, and refunding/voiding payments when necessary.

--- END DEEP DOMAIN CONTEXT ---

--- CLUE FILE START ---
=CC v2.1 saleor@HEAD 4239mod 27389sym
? How are permission checks attached to Saleor GraphQL queries and mutations?


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

get_saleor_permission_names (saleor/plugins/openid_connect/utils.py:728-731)
  sig: get_saleor_permission_names(permissions)

_requestor_has_permission (saleor/graphql/notifications/mutations/external_notification_trigger.py:95-98)
  sig: _requestor_has_permission(cls, context, permission_type)
  behavior: GUARD(cls.check_permissions(context, (permission_type,)) -> return True)
  called_by: perform_mutation, ExternalNotificationTrigger
  raises: PermissionDenied
  uses: PermissionDenied (core.exceptions)

check_permission_for_access_to_meta (saleor/graphql/app/types.py:92-97)
  sig: check_permission_for_access_to_meta(root, info, app)
  calls: has_access_to_app_public_meta
  called_by: resolve_metadata, resolve_metafield, resolve_metafields, App
  raises: PermissionDenied
  uses: PermissionDenied (core.exceptions)

PermissionGroupUpdate (saleor/graphql/account/mutations/permission_group/permission_group_update.py:57-325)
  extends: PermissionGroupCreate
  imports: graphene, django.core.exceptions, account, account.error_codes, account.models
  calls: _save_m2m, check_duplicates, check_if_removing_user_last_group, check_if_users_can_be_removed, clean_channels, clean_input, clean_permissions, clean_remove_users
  raises: ValidationError
  uses: AccessibleChannelsByGroupIdLoader (dataloaders), ValidationError (django.core.exceptions)

PermissionGroupCreate (saleor/graphql/account/mutations/permission_group/permission_group_create.py:60-272)
  extends: DeprecatedModelMutation
  imports: graphene, django.core.exceptions, account, account.error_codes, account.models
  calls: check_permissions, clean_channels, clean_input, clean_permissions, clean_users, ensure_can_manage_channels, ensure_can_manage_permissions, ensure_users_are_staff
  raises: ValidationError, PermissionDenied
  uses: PermissionDenied (core.exceptions), ValidationError (django.core.exceptions)

PermissionGroupUpdateInput (saleor/graphql/account/mutations/permission_group/permission_group_update.py:33-54)
  extends: PermissionGroupInput
  imports: graphene, django.core.exceptions, account, account.error_codes, account.models
  called_by: Arguments, PermissionGroupUpdate

PermissionGroupCreateInput (saleor/graphql/account/mutations/permission_group/permission_group_create.py:46-57)
  extends: PermissionGroupInput
  imports: graphene, django.core.exceptions, account, account.error_codes, account.models
  called_by: Arguments, PermissionGroupCreate

PermissionGroupDelete (saleor/graphql/account/mutations/permission_group/permission_group_delete.py:25-108)
  extends: ModelDeleteMutation
  imports: graphene, django.core.exceptions, account, account.error_codes, core.exceptions
  calls: check_if_group_can_be_removed, check_permissions, ensure_deleting_not_left_not_manageable_permissions, ensure_not_removing_requestor_last_group
  raises: PermissionDenied, ValidationError
  uses: PermissionDenied (core.exceptions), ValidationError (django.core.exceptions)

MetadataPermissionOptions (saleor/graphql/meta/mutations/base.py:28-29)
  extends: MutationOptions
  imports: graphene, django.core.exceptions, graphql.error.base, attribute, checkout
  called_by: __init_subclass_with_meta__, BaseMetadataMutation

PermissionGroupInput (saleor/graphql/account/mutations/permission_group/permission_group_create.py:27-43)
  extends: BaseInputObjectType
  imports: graphene, django.core.exceptions, account, account.error_codes, account.models

_update_queries (saleor/graphql/product/filters/product_attributes.py:89-98)
  sig: _update_queries(queries, filter_values, attributes_slug_pk_map, value_maps)
  behavior: ACCUMULATE(filter_values loop -> queries attr val pk, raises ValueError)
  called_by: _clean_product_attributes_filter_input
  raises: ValueError

has_required_permission (saleor/graphql/app/types.py:84-89)
  sig: has_required_permission(app, context)
  called_by: resolve_tokens, resolve_webhooks, App
  raises: PermissionDenied
  uses: PermissionDenied (core.exceptions)

permission_required (saleor/graphql/decorators.py:70-81)
  sig: permission_required(perm)
  calls: account_passes_test
  raises: PermissionDenied
  uses: PermissionDenied (core.exceptions)

ProductQueries (saleor/graphql/product/schema.py:141-638)
  extends: ObjectType
  imports: graphene, django.db.models, promise, core.search, permission.enums
  calls: resolve_categories, resolve_collections, _resolve_product, resolve_product, resolve_product_types, _resolve_product_variant, _resolve_product_variants, resolve_product_variants
  uses: ChannelContext (core.context), ChannelBySlugLoader (channel.dataloaders.by_self), ChannelQsContext (core.context), Exists (django.db.models)

AccountQueries (saleor/graphql/account/schema.py:117-283)
  extends: ObjectType
  imports: graphene, core.search, permission.auth_filters, permission.enums, permission.utils
  calls: resolve_address, resolve_address_validation_rules, resolve_customers, resolve_permission_group, resolve_permission_groups, resolve_staff_users, resolve_user, CustomerFilterInput

DiscountQueries (saleor/graphql/discount/schema.py:74-202)
  extends: ObjectType
  imports: graphene, permission.enums, core, core.connection, core.descriptions
  calls: resolve_promotion, resolve_promotions, resolve_sale, resolve_sales, resolve_voucher, resolve_vouchers, SaleFilterInput, VoucherFilterInput

OrderQueries (saleor/graphql/order/schema.py:102-271)
  extends: ObjectType
  imports: graphene, django.core.exceptions, core.exceptions, core.search, order
  calls: OrderDraftFilterInput, OrderFilterInput, resolve_draft_orders, resolve_homepage_events, resolve_order, resolve_order_by_token, resolve_orders, resolve_orders_total
  raises: PermissionDenied
  uses: PermissionDenied (core.exceptions), OrderByIdLoader (dataloaders)

resolve_permission_groups (saleor/graphql/account/types.py:608-611)
  sig: resolve_permission_groups(root, info)
  behavior: GUARD(is_newly_created_user(root) -> return [])
  calls: is_newly_created_user
  called_by: Group

AppQueries (saleor/graphql/app/schema.py:60-175)
  extends: ObjectType
  imports: graphene, core.exceptions, permission.auth_filters, permission.enums, core
  calls: AppExtensionFilterInput, AppFilterInput, resolve_app, resolve_app_extensions, resolve_apps, resolve_apps_installations
  raises: PermissionDenied
  uses: PermissionDenied (core.exceptions)

PageQueries (saleor/graphql/page/schema.py:38-150)
  extends: ObjectType
  imports: graphene, core.search, channel.dataloaders.by_self, core, core.connection
  calls: _resolve_page, resolve_page, resolve_page_type, resolve_page_types, _resolve_pages, resolve_pages
  uses: ChannelContext (core.context), ChannelBySlugLoader (channel.dataloaders.by_self), ChannelQsContext (core.context)

MenuQueries (saleor/graphql/menu/schema.py:32-116)
  extends: ObjectType
  imports: graphene, channel.utils, core, core.connection, core.context
  calls: resolve_menu, resolve_menu_item, resolve_menu_items, resolve_menus
  uses: ChannelQsContext (core.context)

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 83 symbols in L3, 7 with behavior annotations
uncovered: resolve_permission_group, resolve_permission_group, resolve_permission_group, resolve_permission_groups

--- CLUE FILE END ---

QUESTION: How are permission checks attached to Saleor GraphQL queries and mutations?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
