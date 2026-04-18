# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: ent-saleor-mech-1

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.


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

--- CLUE FILE (File 1) ---
=CC v2.1 saleor@HEAD 4239mod 27389sym
? How does Saleor keep search indexing and other scheduled work running?


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

set_search_index_dirty (saleor/checkout/search/indexing.py:60-72)
  Reset search vectors for multiple checkouts.
  sig: set_search_index_dirty(checkout_pks, search_index_dirty_value)
  called_by: update_checkouts_search_vector

prepare_checkout_search_vector_value (saleor/checkout/search/indexing.py:75-115)
  Prepare all search vector components for a checkout.
  sig: prepare_checkout_search_vector_value(checkout, data)
  calls: generate_checkout_lines_search_vector_value, generate_checkout_payments_search_vector_value, generate_checkout_transactions_search_vector_value
  called_by: update_checkouts_search_vector
  uses: NoValidationSearchVector (core.postgres), Value (django.db.models)

_prep_product_search_vector_index (saleor/product/search.py:32-49)
  sig: _prep_product_search_vector_index(products, page_id_to_title_map)
  behavior: ACCUMULATE(products loop -> result)
  calls: prepare_product_search_vector_value
  called_by: update_products_search_vector
  uses: FlatConcatSearchVector (core.postgres)

update_checkouts_search_vector (saleor/checkout/search/indexing.py:27-57)
  Update search vectors for multiple checkouts using efficient data loading.
  sig: update_checkouts_search_vector(checkouts)
  calls: prepare_checkout_search_vector_value, set_search_index_dirty
  uses: FlatConcatSearchVector (core.postgres)

generate_checkout_lines_search_vector_value (saleor/checkout/search/indexing.py:180-217)
  Generate search vectors for checkout lines.
  sig: generate_checkout_lines_search_vector_value(lines_data)
  behavior: ACCUMULATE(lines_data[:settings.... -> line vectors NoValidationSea)
  called_by: prepare_checkout_search_vector_value
  uses: NoValidationSearchVector (core.postgres), Value (django.db.models)

generate_checkout_payments_search_vector_value (saleor/checkout/search/indexing.py:156-177)
  Generate search vectors for checkout payments.
  sig: generate_checkout_payments_search_vector_value(payments)
  behavior: ACCUMULATE(payments[:settings.CH... -> payment vectors NoValidation)
  called_by: prepare_checkout_search_vector_value
  uses: NoValidationSearchVector (core.postgres), Value (django.db.models)

generate_checkout_transactions_search_vector_value (saleor/checkout/search/indexing.py:118-153)
  Generate search vectors for checkout transactions.
  sig: generate_checkout_transactions_search_vector_value(transactions_data)
  behavior: ACCUMULATE(transactions_data[:se... -> transaction vectors NoValida)
  called_by: prepare_checkout_search_vector_value
  uses: NoValidationSearchVector (core.postgres), Value (django.db.models)

mark_search_index_dirty (saleor/graphql/attribute/mutations/attribute_value_update.py:86-88)
  sig: mark_search_index_dirty(cls, instance)
  calls: _mark_pages_search_index_dirty, _mark_products_search_index_dirty
  called_by: post_save_action, AttributeValueUpdate

get_page_ids_to_search_index_update (saleor/graphql/attribute/mutations/attribute_delete.py:97-106)
  sig: get_page_ids_to_search_index_update(cls, instance)
  called_by: perform_mutation, AttributeDelete
  uses: Exists (django.db.models), OuterRef (django.db.models)

get_product_ids_to_search_index_update (saleor/graphql/attribute/mutations/attribute_delete.py:84-94)
  sig: get_product_ids_to_search_index_update(cls, instance)
  called_by: perform_mutation, AttributeDelete
  uses: Exists (django.db.models), OuterRef (django.db.models)

_mark_pages_search_index_dirty (saleor/graphql/attribute/mutations/attribute_value_update.py:113-119)
  sig: _mark_pages_search_index_dirty(cls, instance)
  called_by: mark_search_index_dirty, AttributeValueUpdate
  uses: Exists (django.db.models), OuterRef (django.db.models)

_mark_products_search_index_dirty (saleor/graphql/attribute/mutations/attribute_value_update.py:91-110)
  sig: _mark_products_search_index_dirty(cls, instance)
  called_by: mark_search_index_dirty, AttributeValueUpdate
  uses: Exists (django.db.models), OuterRef (django.db.models), Q (django.db.models)

get_page_ids_to_search_index_update_for_attribute_values (saleor/graphql/attribute/mutations/utils.py:37-52)
  Get page IDs that need search index updates when attribute values are changed.
  sig: get_page_ids_to_search_index_update_for_attribute_values(values)
  uses: Exists (django.db.models), OuterRef (django.db.models)

get_product_ids_to_search_index_update_for_attribute_values (saleor/graphql/attribute/mutations/utils.py:8-34)
  Get product IDs that need search index updates when attribute values are changed.
  sig: get_product_ids_to_search_index_update_for_attribute_values(values)
  uses: Exists (django.db.models), OuterRef (django.db.models)

mark_checkout_search_index_dirty (saleor/payment/utils.py:1684-1686)
  sig: mark_checkout_search_index_dirty(checkout)
  called_by: create_transaction_event_from_request_and_webhook_response

mark_gift_cards_search_index_as_dirty (saleor/giftcard/search.py:43-46)
  sig: mark_gift_cards_search_index_as_dirty(gift_cards)
  behavior: ACCUMULATE(gift_cards loop -> result)
  called_by: mark_gift_cards_search_index_as_dirty_by_users

mark_gift_cards_search_index_as_dirty (saleor/giftcard/migrations/0023_mark_gift_cards_search_vector_as_dirty.py:10-15)
  sig: mark_gift_cards_search_index_as_dirty(apps, _schema_editor)

mark_gift_cards_search_index_as_dirty_by_users (saleor/giftcard/search.py:49-57)
  sig: mark_gift_cards_search_index_as_dirty_by_users(users)
  calls: mark_gift_cards_search_index_as_dirty
  uses: Q (django.db.models)

mark_gift_cards_search_index_as_dirty_task (saleor/giftcard/migrations/tasks/saleor3_22.py:10-11)

mark_products_search_index_as_dirty (saleor/product/migrations/0203_mark_products_search_index_as_dirty.py:10-15)
  sig: mark_products_search_index_as_dirty(apps, _schema_editor)

mark_products_search_index_as_dirty_task (saleor/product/migrations/tasks/saleor3_23.py:15-31)

update_products_search_index (saleor/graphql/page/mutations/page_delete.py:48-62)
  sig: update_products_search_index(cls, instance)
  called_by: perform_mutation, PageDelete
  uses: Exists (django.db.models.expressions), OuterRef (django.db.models.expressions)

update_products_search_index (saleor/graphql/page/mutations/page_update.py:70-84)
  sig: update_products_search_index(cls, instance)
  called_by: save, PageUpdate
  uses: Exists (django.db.models), OuterRef (django.db.models)

update_products_search_index (saleor/graphql/page/bulk_mutations.py:146-164)
  sig: update_products_search_index(cls, instance_pks)
  uses: Exists (django.db.models), OuterRef (django.db.models)

update_products_search_index (saleor/graphql/page/bulk_mutations.py:53-67)
  sig: update_products_search_index(cls, instance_pks)
  uses: Exists (django.db.models), OuterRef (django.db.models)

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 83 symbols in L3, 32 with behavior annotations
uncovered: generate_attributes_search_vector_value, get_reference_attribute_search_value, mark_pages_search_vector_as_dirty, mark_pages_search_vector_as_dirty_in_batches
drill: saleor/checkout/search/indexing.py (~15 lines, set_search_index_dirty)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## set_search_index_dirty  (saleor/checkout/search/indexing.py L60-72)
```
def set_search_index_dirty(checkout_pks: list["UUID"], search_index_dirty_value: bool):
    """Reset search vectors for multiple checkouts."""
    with transaction.atomic():
        with allow_writer():
            # select and lock checkouts to ensure updating in correct order
            pks = (
                checkout_qs_select_for_update()
                .filter(pk__in=checkout_pks)
                .values_list("pk", flat=True)
            )
            Checkout.objects.filter(pk__in=pks).update(
                search_vector=None, search_index_dirty=search_index_dirty_value
            )
```

## generate_checkout_lines_search_vector_value  (saleor/checkout/search/indexing.py L180-217)
```
def generate_checkout_lines_search_vector_value(
    lines_data: list[CheckoutLineData],
) -> list[NoValidationSearchVector]:
    """Generate search vectors for checkout lines."""
    line_vectors = []
    for line_data in lines_data[: settings.CHECKOUT_MAX_INDEXED_LINES]:
        variant = line_data.variant
        if not variant:
            continue

        if variant.sku:
            line_vectors.append(
                NoValidationSearchVector(
                    Value(variant.sku),
                    config="simple",
                    weight="C",
                )
            )

        product = line_data.product
        if product and product.name:
            line_vectors.append(
                NoValidationSearchVector(
                    Value(product.name),
                    config="simple",
                    weight="C",
                )
            )
        if variant.name:
            line_vectors.append(
                NoValidationSearchVector(
                    Value(variant.name),
                    config="simple",
                    weight="C",
                )
            )

    return line_vectors
```

## generate_checkout_payments_search_vector_value  (saleor/checkout/search/indexing.py L156-177)
```
def generate_checkout_payments_search_vector_value(
    payments: list["Payment"],
) -> list[NoValidationSearchVector]:
    """Generate search vectors for checkout payments."""
    payment_vectors = []
    for payment in payments[: settings.CHECKOUT_MAX_INDEXED_PAYMENTS]:
        payment_vectors.append(
            NoValidationSearchVector(
                Value(graphene.Node.to_global_id("Payment", payment.id)),
                config="simple",
                weight="D",
            )
        )
        if payment.psp_reference:
            payment_vectors.append(
                NoValidationSearchVector(
                    Value(payment.psp_reference),
                    config="simple",
                    weight="D",
                )
            )
    return payment_vectors
```

## generate_checkout_transactions_search_vector_value  (saleor/checkout/search/indexing.py L118-153)
```
def generate_checkout_transactions_search_vector_value(
    transactions_data: list[TransactionData],
) -> list[NoValidationSearchVector]:
    """Generate search vectors for checkout transactions."""
    transaction_vectors = []
    for transaction_data in transactions_data[
        : settings.CHECKOUT_MAX_INDEXED_TRANSACTIONS
    ]:
        transaction = transaction_data.transaction
        transaction_vectors.append(
            NoValidationSearchVector(
                Value(graphene.Node.to_global_id("TransactionItem", transaction.token)),
                config="simple",
                weight="D",
            )
        )
        if transaction.psp_reference:
            transaction_vectors.append(
                NoValidationSearchVector(
                    Value(transaction.psp_reference),
                    config="simple",
                    weight="D",
                )
            )

        for event in transaction_data.events:
            if event.psp_reference:
                transaction_vectors.append(
                    NoValidationSearchVector(
                        Value(event.psp_reference),
                        config="simple",
                        weight="D",
                    )
                )

    return transaction_vectors
```

## prepare_checkout_search_vector_value  (saleor/checkout/search/indexing.py L75-115)
```
def prepare_checkout_search_vector_value(
    checkout: "Checkout", data: CheckoutData
) -> list[NoValidationSearchVector]:
    """Prepare all search vector components for a checkout."""
    search_vectors = [
        NoValidationSearchVector(
            Value(str(checkout.token)), config="simple", weight="A"
        ),
    ]

    if checkout.email:
        search_vectors.extend(generate_email_vector(checkout.email))

    if data.user:
        search_vectors.extend(generate_email_vector(data.user.email))
        search_vectors.append(
            NoValidationSearchVector(
                Value(data.user.first_name), config="simple", weight="A"
            )
        )
        search_vectors.append(
            NoValidationSearchVector(
                Value(data.user.last_name), config="simple", weight="A"
            )
        )

    if data.billing_address:
        search_vectors += generate_address_search_vector_value(
            data.billing_address, weight="B"
        )
    if data.shipping_address:
        search_vectors += generate_address_search_vector_value(
            data.shipping_address, weight="B"
        )

    search_vectors += generate_checkout_payments_search_vector_value(data.payments)
    search_vectors += generate_checkout_lines_search_vector_value(data.lines)
    search_vectors += generate_checkout_transactions_search_vector_value(
        data.transactions
    )
    return search_vectors
```

## update_checkouts_search_vector  (saleor/checkout/search/indexing.py L27-57)
```
def update_checkouts_search_vector(checkouts: list["Checkout"]):
    """Update search vectors for multiple checkouts using efficient data loading."""
    checkout_pks = [checkout.pk for checkout in checkouts]
    # update search_index_dirty flag before to ensure that will not update search vector
    # with outdated data
    set_search_index_dirty(checkout_pks, search_index_dirty_value=False)

    try:
        checkout_data_map = load_checkout_data(checkouts)

        for checkout in checkouts:
            data = checkout_data_map.get(checkout.pk)
            if not data:
                continue

            checkout.search_vector = FlatConcatSearchVector(
                *prepare_checkout_search_vector_value(checkout, data)
            )
    except Exception:
        # Reset search_index_dirty flag if processing fails
        set_search_index_dirty(checkout_pks, search_index_dirty_value=True)
        raise

    with transaction.atomic():
        with allow_writer():
            _locked_checkouts = (
                checkout_qs_select_for_update()
                .filter(pk__in=[checkout.pk for checkout in checkouts])
                .values_list("pk", flat=True)
            )
            Checkout.objects.bulk_update(checkouts, ["search_vector"])
```
--- END SOURCE SNIPPETS ---

QUESTION: How does Saleor keep search indexing and other scheduled work running?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
