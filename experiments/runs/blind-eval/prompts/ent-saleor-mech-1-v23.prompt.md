# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: ent-saleor-mech-1

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.

--- CLUE FILE (File 1) ---
=CC v2.1 saleor@HEAD 4239mod 27374sym
? How does Saleor keep search indexing and other scheduled work running?


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

update_products_search_index (saleor/graphql/page/mutations/page_type_delete.py:43-60)
  sig: update_products_search_index(cls, instance)
  called_by: perform_mutation, PageTypeDelete
  uses: Exists (django.db.models.expressions), OuterRef (django.db.models.expressions)

update_products_search_index (saleor/graphql/page/bulk_mutations.py:53-67)
  sig: update_products_search_index(cls, instance_pks)
  uses: Exists (django.db.models), OuterRef (django.db.models)

update_products_search_index (saleor/graphql/page/bulk_mutations.py:146-164)
  sig: update_products_search_index(cls, instance_pks)
  uses: Exists (django.db.models), OuterRef (django.db.models)

update_products_search_index (saleor/graphql/page/mutations/page_update.py:70-84)
  sig: update_products_search_index(cls, instance)
  called_by: save, PageUpdate
  uses: Exists (django.db.models), OuterRef (django.db.models)

filter_checkout_search (saleor/graphql/checkout/filters.py:101-102)
  sig: filter_checkout_search(qs, _, value)
  behavior: DELEGATE(prefix_search -> result)

filter_order_search (saleor/graphql/order/filters.py:184-185)
  sig: filter_order_search(qs, _, value)
  behavior: DELEGATE(prefix_search -> result)

filter_search (saleor/graphql/product/filters/product_helpers.py:324-325)
  sig: filter_search(qs, _, value)
  behavior: DELEGATE(prefix_search -> result)

filter_user_search (saleor/graphql/account/filters.py:67-68)
  sig: filter_user_search(qs, _, value)
  behavior: DELEGATE(prefix_search -> result)

generate_attributes_search_vector_value (saleor/page/search.py:192-211)
  Prepare `search_vector` value for assigned attributes.
  sig: generate_attributes_search_vector_value(values_data)
  behavior: ACCUMULATE(values_data loop -> search vectors get search ve)
  called_by: prepare_page_search_vector_value

generate_attributes_search_vector_value_with_assignment (saleor/product/search.py:155-172)
  Prepare `search_vector` value for assigned attributes.
  sig: generate_attributes_search_vector_value_with_assignment(assigned_attributes)
  behavior: ACCUMULATE(assigned_attributes loop -> search vectors get search ve)
  called_by: generate_variants_search_vector_value

prepare_order_search_vector_value (saleor/order/search.py:23-93)
  sig: prepare_order_search_vector_value(order)
  calls: generate_order_discounts_search_vector_value, generate_order_events_search_vector_value, generate_order_invoices_search_vector_value, generate_order_lines_search_vector_value, generate_order_payments_search_vector_value, generate_order_transactions_search_vector_value
  called_by: update_order_search_vector
  uses: NoValidationSearchVector (core.postgres), Value (django.db.models)

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 80 symbols in L3, 32 with behavior annotations
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
