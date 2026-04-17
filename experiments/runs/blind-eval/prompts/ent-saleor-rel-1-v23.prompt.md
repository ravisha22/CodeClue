# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-saleor-rel-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 saleor@HEAD 4239mod 27374sym
? How are permission checks attached to Saleor GraphQL queries and mutations?


-- TREE
saleor/  (4237 files)
  account/  app/  asgi/  attribute/  auth/  channel/  checkout/  core/  csv/  discount/  ...+20
conftest.py  manage.py

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
clean_attributes                    M saleor/graphql/page/mutations/page_create.py:72     function clean_attributes
_resolve_page                       M saleor/graphql/page/schema.py:103    function _resolve_page
resolve_page                        M saleor/graphql/page/schema.py:94     function resolve_page
_resolve_pages                      M saleor/graphql/page/schema.py:122    function _resolve_pages
resolve_pages                       M saleor/graphql/page/schema.py:117    function resolve_pages
_create_variant_errors              M saleor/graphql/checkout/mutations/checkout_create_from_order.py:81     function _create_variant_errors
__run_payment_method                M saleor/plugins/manager.py:2556   function __run_payment_method
__run_payment_webhook               M saleor/plugins/webhook/plugin.py:2994   Trigger payment webhook event.
get_form_field_description          M saleor/graphql/core/types/converter.py:24     function get_form_field_description
_resolve_product                    M saleor/graphql/product/schema.py:455    function _resolve_product
  ...and 13182 more symbols

-- FOCUS
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

__queries_or_introspection_in_selections (saleor/graphql/utils/validators.py:36-55)
  sig: __queries_or_introspection_in_selections(selections, is_query)
  behavior: ACCUMULATE(selections loop -> result)
  calls: __queries_or_introspection_in_inline_fragment
  called_by: __queries_or_introspection_in_fragment_definition, __queries_or_introspection_in_inline_fragment, __queries_or_introspection_in_operation_definition

CheckoutQueries (saleor/graphql/checkout/schema.py:50-123)
  extends: ObjectType
  imports: graphene, permission.enums, core, core.connection, core.descriptions
  calls: resolve_checkout, resolve_checkout_lines, resolve_checkouts

GiftCardQueries (saleor/graphql/giftcard/schema.py:38-134)
  extends: ObjectType
  imports: graphene, graphql.error, core.search, giftcard, permission.enums
  calls: resolve_gift_card, resolve_gift_card_tags, resolve_gift_cards
  raises: GraphQLError
  uses: GraphQLError (graphql.error)

PaymentQueries (saleor/graphql/payment/schema.py:55-157)
  extends: ObjectType
  imports: graphene, permission.enums, core, core.connection, core.descriptions
  calls: resolve_payments, resolve_transaction, resolve_transactions

ChannelQueries (saleor/graphql/channel/schema.py:20-50)
  extends: ObjectType
  imports: graphene, permission.auth_filters, core, core.doc_category, core.fields
  calls: resolve_channel, resolve_channels

CsvQueries (saleor/graphql/csv/schema.py:16-42)
  extends: ObjectType
  imports: graphene, permission.enums, core, core.connection, core.descriptions
  calls: resolve_export_file, resolve_export_files

PluginsQueries (saleor/graphql/plugins/schema.py:17-53)
  extends: ObjectType
  imports: graphene, permission.enums, core, core.connection, core.context
  calls: resolve_plugin, resolve_plugins

StockQueries (saleor/graphql/warehouse/schema.py:87-114)
  extends: ObjectType
  imports: graphene, permission.enums, warehouse, core, core.connection
  calls: resolve_stock, resolve_stocks

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 80 symbols in L3, 7 with behavior annotations
uncovered: resolve_permission_group, resolve_permission_group, resolve_permission_group, resolve_permission_groups

--- CLUE FILE END ---

QUESTION: How are permission checks attached to Saleor GraphQL queries and mutations?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
