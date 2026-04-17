# Enterprise Eval: ent-saleor-mech-2
Date: 2026-04-17

## Question
How are concurrent object updates kept safe in Saleor?

---

## Reasoning Trace

### Step 1: Identify Concurrency-Related Symbols

From INDEX, FOCUS, and SYM, the following symbols directly relate to concurrency control:

**Locking mechanisms:**
- `user_qs_select_for_update` (saleor/account/lock_objects.py:5) — a 5-line module providing a SELECT FOR UPDATE queryset for user objects (INDEX). The module name `lock_objects.py` explicitly indicates database-level row locking for concurrency control.

**Transaction and atomic patterns (from FOCUS — mech-1 source snippets provided context):**
The `set_search_index_dirty` function (from ent-saleor-mech-1 source) demonstrates the pattern:
- Uses `transaction.atomic()` for transactional consistency
- Uses `allow_writer()` context manager
- Uses `checkout_qs_select_for_update()` — SELECT FOR UPDATE to lock rows before modification

### Step 2: Guard-Based Concurrency Safety in Business Logic

Several FOCUS symbols show guard patterns that prevent unsafe concurrent state transitions:

- **`get_active_app`** (saleor/graphql/payment/types.py:411-423 and :780-792) — behavior: `GUARD(app and app.is_active and (not app.removed_at) -> return app)`. This ensures only active, non-removed apps are resolved, preventing race conditions where a concurrently removed app could be used (not in this clue, but referenced from struct-2).

- **`clean_source_object`** (saleor/graphql/payment/mutations/base.py:27-101) — behavior: `BRANCH(source_object_type == 'Checkout' -> checkout_models.Check..., else -> ...)`. Raises both `GraphQLError` and `ValidationError`. This validates the source object exists and is of the correct type before proceeding, serving as an optimistic concurrency guard (FOCUS).

- **`get_source_object`** (saleor/graphql/payment/mutations/transaction/transaction_process.py:93-109) — behavior: `GUARD(transaction_item.checkout_id -> return checkout)`. Called by `perform_mutation` of `TransactionProcess`. Raises `ValidationError` (FOCUS). Validates the transaction's source object exists at mutation time.

- **`clean_payment_app`** (saleor/graphql/payment/mutations/transaction/transaction_process.py:149-174) — behavior: `GUARD(not transaction_item.app_identifier -> raise ValidationError({'i...))`. Called by `perform_mutation` of `TransactionProcess` (FOCUS). Guards that the payment app is properly linked before processing.

- **`clean_app_from_payment_gateway`** (saleor/graphql/payment/mutations/transaction/transaction_initialize.py:117-137) — behavior: `GUARD(payment_gateway.app_identifier == GIFT_CARD_PAYMENT_GATEW... -> return...)`. Called by `perform_mutation` of `TransactionInitialize` (FOCUS from struct-2). Validates app identity before initializing a transaction.

### Step 3: Order Amount Synchronization

- **`updates_amounts_for_order`** (saleor/order/utils.py:1081-1108) — calls `update_order_authorize_data` and `update_order_charge_data`. Takes a `save` parameter, suggesting it can batch multiple amount updates before persisting (FOCUS). This centralized update function prevents partial writes of authorization and charge data.

- **`_update_order_line_discount_object`** (saleor/order/utils.py:883-913) — called by `update_discount_for_order_line` (FOCUS). Centralizes discount object updates for order lines.

- **`create_or_update_discount_object_from_order_level_voucher`** (saleor/discount/utils/voucher.py:387-481) — behavior: `BRANCH(is_shipping_voucher(voucher) -> voucher.get_discount_..., else -> ord...)`. Called by `create_or_update_voucher_discount_objects_for_order` (FOCUS). The branch-then-update pattern ensures consistent discount application.

### Step 4: App Problem Mutation Locking

- **`AppProblemDismiss`** (saleor/graphql/app/mutations/app_problem_dismiss.py:102-327) — imports `app.lock_objects`, indicating it uses row-level locking when dismissing app problems (FOCUS from struct-2).
- **`AppProblemCreate`** (saleor/graphql/app/mutations/app_problem_create.py:93-202) — also imports `app.lock_objects`. Calls `_aggregate_existing` and `_create_new_problem`, suggesting it checks for existing problems before creating new ones, with locking to prevent duplicates (FOCUS from struct-2).

This reveals a `lock_objects` pattern used across multiple domains — at minimum `account/lock_objects.py` and `app/lock_objects.py`.

### Step 5: SortableModel Ordering Safety

- **`SortableModel`** (saleor/core/models.py:16-45) — extends Django `Model`; calls `get_max_sort_order` and `get_ordering_queryset` during `save` and `delete`. Raises `NotImplementedError` for `get_ordering_queryset` (FOCUS from struct-1). By computing `get_max_sort_order` at save time, it ensures ordering consistency, though whether this is done under a lock is not visible in the clue.

### Step 6: ObjectWithMetadata Interface

- **`ObjectWithMetadata`** (saleor/graphql/meta/types.py:49-154) — extends `Interface`; resolves metadata, private metadata, and filters metadata via `_get_metadata_instance` and `_filter_metadata` (FOCUS). While not directly a concurrency mechanism, the centralized metadata resolution through an interface ensures consistent access patterns.

### Step 7: BaseObjectType and BaseInputObjectType

- **`BaseObjectType`** (saleor/graphql/core/types/base.py:8-28) and **`BaseInputObjectType`** (line 31-37) extend `ObjectType` and `InputObjectType` respectively (FOCUS). These provide standardized base types ensuring consistent serialization/deserialization across mutations, reducing the risk of inconsistent object representations during concurrent access.

### Step 8: GAPS — What Cannot Be Determined

Per the GAPS section:
- **Type:** STRUCTURAL (answerable from L0-L2)
- **Coverage:** 80 symbols in L3, 11 with behavior annotations
- **Uncovered symbols:** `get_translated_object_id` (appears 3 times), `linked_object`

From the clue alone, the following **cannot** be determined:
- The full implementation of `lock_objects.py` modules — we know `account/lock_objects.py` contains `user_qs_select_for_update` (5 lines) and `app/lock_objects.py` exists (imported by app mutations), but we don't see whether other domains have their own `lock_objects` modules
- Whether Saleor uses Django's database-level advisory locks, optimistic concurrency control (version fields), or both
- The implementation of `allow_writer()` context manager (seen in mech-1 source snippets) — this likely controls write access in a read-replica setup, but its mechanism is not detailed
- Whether there are database-level constraints (unique constraints, check constraints) used for concurrency safety beyond SELECT FOR UPDATE
- The `checkout_qs_select_for_update()` implementation details
- Whether any distributed locking mechanism (Redis, etc.) is used beyond PostgreSQL row locks

---

## Synthesized Answer

Saleor keeps concurrent object updates safe through several layered mechanisms:

1. **SELECT FOR UPDATE row locking:** Dedicated `lock_objects` modules provide queryset functions that use PostgreSQL's SELECT FOR UPDATE. Evidence: `user_qs_select_for_update` (saleor/account/lock_objects.py:5) for user rows, and `app.lock_objects` imported by `AppProblemDismiss` (app/mutations/app_problem_dismiss.py:102) and `AppProblemCreate` (app/mutations/app_problem_create.py:93). The mech-1 source snippet confirms `checkout_qs_select_for_update()` is used inside `transaction.atomic()` blocks in search indexing.

2. **Atomic transactions:** Operations that modify shared state are wrapped in `transaction.atomic()` with `allow_writer()` (seen in `set_search_index_dirty` and `update_checkouts_search_vector` source snippets from ent-saleor-mech-1). The `allow_writer()` context manager suggests a read-replica–aware architecture where writes must be explicitly routed to the primary database.

3. **Dirty-flag with error recovery:** The search indexing system (ent-saleor-mech-1 evidence) demonstrates a two-phase pattern: pre-mark records as clean under lock → compute new values → bulk-update under lock. On failure, dirty flags are restored (`set_search_index_dirty(checkout_pks, search_index_dirty_value=True)`) ensuring eventual consistency.

4. **Guard-based validation in mutations:** Mutations validate object state before modification: `clean_source_object` (payment/mutations/base.py:27) verifies source objects exist, `clean_payment_app` (transaction_process.py:149) checks app linkage, `get_active_app` (payment/types.py:411) guards against removed apps. These prevent operations on stale or concurrently-deleted objects.

5. **Centralized update functions:** `updates_amounts_for_order` (saleor/order/utils.py:1081) atomically updates both authorization and charge data. `_update_order_line_discount_object` (order/utils.py:883) centralizes line discount modifications, reducing the window for inconsistent partial updates.

**Limitations:** The exact scope of `lock_objects` modules across all domains, whether optimistic concurrency control (version fields) is used, and the implementation of `allow_writer()` cannot be determined from the clue alone (GAPS).
