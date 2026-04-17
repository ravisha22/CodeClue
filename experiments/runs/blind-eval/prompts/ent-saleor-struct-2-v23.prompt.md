# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-saleor-struct-2

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 saleor@HEAD 4239mod 27374sym
? How is the Saleor repository organized for app modules, GraphQL APIs, and tests?


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
AppManifestRequiredSaleorVersion (saleor/graphql/app/types.py:315-326)
  extends: BaseObjectType
  imports: base64, graphene, graphql, app, app.types

get_active_app (saleor/graphql/payment/types.py:411-423)
  sig: get_active_app(app)
  behavior: GUARD(app and app.is_active and (not app.removed_at) -> return app)
  uses: ActiveAppsByAppIdentifierLoader (app.dataloaders)

get_active_app (saleor/graphql/payment/types.py:780-792)
  sig: get_active_app(app)
  behavior: GUARD(app and app.is_active and (not app.removed_at) -> return app)
  uses: ActiveAppsByAppIdentifierLoader (app.dataloaders)

resolve_app (saleor/graphql/app/types.py:211-231)
  sig: resolve_app(root, info, app_requestor)
  behavior: GUARD(app_requestor and app_requestor.id == root.app_id -> return AppByIdLoa...)
  raises: PermissionDenied
  uses: PermissionDenied (core.exceptions), AppByIdLoader (dataloaders)

get_app_promise (saleor/graphql/app/dataloaders/utils.py:20-27)
  sig: get_app_promise(context)
  behavior: GUARD(hasattr(context, 'app') -> return Promise.resolve(app))
  calls: promise_app
  called_by: _wrapper, app_promise_callback

clean_tax_app_id (saleor/graphql/tax/mutations/tax_configuration_update.py:252-292)
  sig: clean_tax_app_id(cls, info, instance, data)
  behavior: ACCUMULATE(update_countries_conf... -> identifiers country app iden)
  calls: __verify_tax_app_id
  called_by: clean_input, TaxConfigurationUpdate

clean_app_from_payment_gateway (saleor/graphql/payment/mutations/transaction/transaction_initialize.py:117-137)
  sig: clean_app_from_payment_gateway(cls, payment_gateway)
  behavior: GUARD(payment_gateway.app_identifier == GIFT_CARD_PAYMENT_GATEW... -> return...)
  called_by: perform_mutation, TransactionInitialize
  raises: ValidationError
  uses: ValidationError (django.core.exceptions)

clean_payment_app (saleor/graphql/payment/mutations/transaction/transaction_process.py:149-174)
  sig: clean_payment_app(cls, transaction_item)
  behavior: GUARD(not transaction_item.app_identifier -> raise ValidationError({'i...)
  called_by: perform_mutation, TransactionProcess
  raises: ValidationError
  uses: ValidationError (django.core.exceptions)

_resolve_app (saleor/graphql/discount/types/promotion_events.py:62-69)
  sig: _resolve_app(app)
  behavior: GUARD(is_owner_or_has_one_of_perms(requester, app, AppPermissio... -> return...)

resolve_access_token_for_app (saleor/graphql/app/resolvers.py:30-40)
  sig: resolve_access_token_for_app(info, root)
  behavior: GUARD(root.type != AppTypeEnum.THIRDPARTY.value -> return None)

_resolve_app (saleor/graphql/order/types.py:580-589)
  sig: _resolve_app(user)
  called_by: OrderEvent
  uses: AppByIdLoader (app.dataloaders)

app_is_active (saleor/graphql/app/schema.py:161-172)
  sig: app_is_active(app_extension)
  uses: AppByIdLoader (dataloaders)

promise_app (saleor/graphql/app/dataloaders/utils.py:13-17)
  sig: promise_app(context)
  called_by: get_app_promise
  uses: AppByTokenLoader (app)

resolve_app (saleor/graphql/giftcard/types.py:139-150)
  sig: resolve_app(root, info)
  uses: AppByIdLoader (app.dataloaders)

resolve_app (saleor/graphql/csv/types.py:63-68)
  sig: resolve_app(root, info)
  uses: AppByIdLoader (app.dataloaders)

resolve_app (saleor/graphql/csv/types.py:106-111)
  sig: resolve_app(root, info)
  uses: AppByIdLoader (app.dataloaders)

resolve_app (saleor/graphql/giftcard/types.py:469-480)
  sig: resolve_app(root, info)
  uses: AppByIdLoader (app.dataloaders)

resolve_app (saleor/graphql/order/types.py:362-366)
  sig: resolve_app(root, info)
  uses: AppByIdLoader (app.dataloaders)

resolve_app (saleor/graphql/order/types.py:576-595)
  sig: resolve_app(root, info)
  uses: AppByIdLoader (app.dataloaders), UserByUserIdLoader (account.dataloaders)

resolve_app (saleor/graphql/account/types.py:259-264)
  sig: resolve_app(root, info)
  uses: AppByIdLoader (app.dataloaders)

resolve_app_extension (saleor/graphql/app/schema.py:160-175)
  sig: resolve_app_extension(_root, info)
  uses: AppExtensionByIdLoader (dataloaders), AppByIdLoader (dataloaders)

AppProblemDismiss (saleor/graphql/app/mutations/app_problem_dismiss.py:102-327)
  extends: BaseMutation
  imports: graphene, django.core.exceptions, account.models, app.error_codes, app.lock_objects
  calls: _dismiss_by_ids_for_staff, _dismiss_by_keys_for_staff, _dismiss_for_app_caller, _parse_problem_ids, _raise_caller_type_mismatch, _validate_by_app_input, _validate_items_limit, AppProblemDismissInput
  called_by: perform_mutation
  raises: ValidationError
  uses: ValidationError (django.core.exceptions)

App (saleor/graphql/app/types.py:645-825)
  imports: base64, graphene, graphql, app, app.types
  calls: resolve_metadata, resolve_metafield, resolve_metafields, check_permission_for_access_to_meta, has_required_permission
  raises: GraphQLError
  uses: PermissionDenied (core.exceptions)

AppQueries (saleor/graphql/app/schema.py:60-175)
  extends: ObjectType
  imports: graphene, core.exceptions, permission.auth_filters, permission.enums, core
  calls: AppExtensionFilterInput, AppFilterInput, resolve_app, resolve_app_extensions, resolve_apps, resolve_apps_installations
  raises: PermissionDenied
  uses: PermissionDenied (core.exceptions)

AppProblemCreate (saleor/graphql/app/mutations/app_problem_create.py:93-202)
  extends: BaseMutation
  imports: graphene, django.utils, pydantic, app.error_codes, app.lock_objects
  calls: _aggregate_existing, _create_new_problem, AppProblemCreateInput, AppProblemCreateValidatedInput
  called_by: perform_mutation
  raises: pydantic_to_validation_error

AppProblemDismissInput (saleor/graphql/app/mutations/app_problem_dismiss.py:82-99)
  Input for dismissing app problems.
  extends: BaseInputObjectType
  imports: graphene, django.core.exceptions, account.models, app.error_codes, app.lock_objects
  called_by: Arguments, AppProblemDismiss

AppByTokenLoader (saleor/graphql/app/dataloaders/app.py:49-113)
  attrs: context_key='app_by_token'
  imports: hashlib, django.contrib.auth.hashers, django.core.cache, app.models, core.dataloaders
  calls: get_and_cache_app_id, remove_not_valid_tokens_from_cache, TokenInfo

AppCreate (saleor/graphql/app/mutations/app_create.py:36-99)
  extends: DeprecatedModelMutation
  imports: graphene, app, permission.enums, webhook.event_types, core.descriptions
  calls: clean_input, save, AppInput

AppInstall (saleor/graphql/app/mutations/app_install.py:44-85)
  extends: DeprecatedModelMutation
  imports: graphene, app, app.manifest_validations, app.tasks, permission.enums
  calls: clean_input, perform_mutation, AppInstallInput

AppProblemCreateInput (saleor/graphql/app/mutations/app_problem_create.py:59-90)
  extends: InputObjectType
  imports: graphene, django.utils, pydantic, app.error_codes, app.lock_objects
  called_by: Arguments, AppProblemCreate

AppInput (saleor/graphql/app/mutations/app_create.py:19-33)
  extends: BaseInputObjectType
  imports: graphene, app, permission.enums, webhook.event_types, core.descriptions
  called_by: Arguments, AppCreate

AppTokenCreate (saleor/graphql/app/mutations/app_token_create.py:26-69)
  extends: DeprecatedModelMutation
  imports: graphene, django.core.exceptions, oauthlib.common, app, app.error_codes
  calls: clean_input, AppTokenInput
  raises: ValidationError
  uses: ValidationError (django.core.exceptions)

create_app_cache_key_from_token (saleor/graphql/app/dataloaders/app.py:15-17)
  Create a cache key for the app based on the token.
  sig: create_app_cache_key_from_token(token)
  called_by: cache_key, TokenInfo

AppFetchManifest (saleor/graphql/app/mutations/app_fetch_manifest.py:18-122)
  extends: BaseMutation
  imports: graphene, requests, django.conf, django.core.exceptions, app.error_codes
  calls: clean_manifest_data, construct_instance, fetch_manifest, success_response
  raises: ValidationError
  uses: Manifest (types), ValidationError (django.core.exceptions)

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 80 symbols in L3, 10 with behavior annotations
uncovered: AppToken, AppTokenDelete, AppTokenVerify, AppTokensByAppIdLoader

--- CLUE FILE END ---

QUESTION: How is the Saleor repository organized for app modules, GraphQL APIs, and tests?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
