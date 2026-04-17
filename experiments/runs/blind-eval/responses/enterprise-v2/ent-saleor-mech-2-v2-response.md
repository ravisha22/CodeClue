# Enterprise v2: ent-saleor-mech-2
Date: 2026-04-17

## Question
How are concurrent object updates kept safe in Saleor?

## Reasoning Scaffold

### Step 1: Identify Relevant Symbols (INDEX, FOCUS, SYM)

The most directly relevant evidence for concurrency safety is:

- **`user_qs_select_for_update`** (`saleor/account/lock_objects.py:5L`) — a 5-line helper that returns a queryset with `SELECT FOR UPDATE`, used to lock user rows before modification (INDEX).
- **`SortableModel`** (`saleor/core/models.py:16-45`) — uses `F` and `Max` from `django.db.models` in its `save` method; `get_max_sort_order` and `get_ordering_queryset` support safe ordering operations (FOCUS).
- **`AppProblemDismiss`** (`saleor/graphql/app/mutations/app_problem_dismiss.py:102-327`) — imports `app.lock_objects` (FOCUS).
- **`AppProblemCreate`** (`saleor/graphql/app/mutations/app_problem_create.py:93-202`) — imports `app.lock_objects` (FOCUS).
- **`updates_amounts_for_order`** (`saleor/order/utils.py:1081-1108`) — calls `update_order_authorize_data` and `update_order_charge_data` (FOCUS).
- **`_update_order_line_discount_object`** (`saleor/order/utils.py:883-913`) — called by `update_discount_for_order_line` (FOCUS).
- **`create_or_update_discount_object_from_order_level_voucher`** (`saleor/discount/utils/voucher.py:387-481`) — `BRANCH(is_shipping_voucher -> ..., else -> ...)` (FOCUS).
- **`ModelWithRestrictedChannelAccessMutation`** (`saleor/graphql/core/mutations.py:895-938`) and **`ModelDeleteWithRestrictedChannelAccessMutation`** (`:971-997`) — call `check_channel_permissions` before any write (FOCUS).

Supporting context from the INDEX: `saleor/account/lock_objects.py` is 5 lines — it almost certainly contains only the `user_qs_select_for_update` function, which returns a queryset with `SELECT FOR UPDATE` applied (INDEX).

### Step 2: Trace the SELECT FOR UPDATE Locking Pattern (INDEX, FOCUS)

**`lock_objects.py` pattern:**  
`saleor/account/lock_objects.py` (5L) exports `user_qs_select_for_update` (INDEX). This is a canonical `SELECT FOR UPDATE` helper that locks user rows at the database level during a transaction, preventing concurrent updates from reading stale data.

The analogous checkout pattern is visible from the mech-1 clue (shared FOCUS) via `update_checkouts_search_vector`, which demonstrates the broader Saleor locking convention:
- A dedicated `lock_objects.py` module per domain exports a `*_qs_select_for_update` function.
- All updates to that object type within a transaction use this helper to acquire row-level locks before reading or writing.

**App lock objects:**  
Both `AppProblemDismiss` and `AppProblemCreate` import `app.lock_objects` (FOCUS). This confirms that the `lock_objects.py` pattern is not limited to `account/` — `app/` also has its own locking module, indicating that `app` entities (likely `App` model rows) are similarly protected with `SELECT FOR UPDATE` during problem creation/dismissal.

### Step 3: Trace Atomic Update Patterns (FOCUS)

**`SortableModel` with Django F expressions:**  
`SortableModel` (`saleor/core/models.py:16-45`) uses `F` (from `django.db.models`) in its `save` method and `Max` in `get_max_sort_order` (FOCUS). Django's `F` expression performs field updates as a single SQL expression (`UPDATE t SET sort_order = sort_order + 1`) without a read-modify-write cycle, eliminating a common concurrency race. `Max` in an aggregate query is similarly a single-query operation. This makes sort-order reordering safe under concurrent load.

**Order financial update coordination:**  
`updates_amounts_for_order` (`saleor/order/utils.py:1081-1108`) calls both `update_order_authorize_data` and `update_order_charge_data` (FOCUS). By encapsulating both updates in a single function, financial totals (authorize/charge amounts) are updated together. This implies a coordinated update pattern to keep the two amounts consistent — if one fails, neither is partially written.

**Order line discount updates:**  
`_update_order_line_discount_object` (`saleor/order/utils.py:883-913`) is called by `update_discount_for_order_line` (FOCUS). Discount objects on order lines are updated through a dedicated function rather than direct field writes, centralising the update logic and making atomic database transactions easier to reason about.

**Voucher discount creation/update:**  
`create_or_update_discount_object_from_order_level_voucher` (`saleor/discount/utils/voucher.py:387-481`) uses a `BRANCH` pattern (`is_shipping_voucher` → shipping discount path; else → order-level discount path) (FOCUS). The "create_or_update" naming (rather than separate create/update functions) indicates an upsert pattern — the database row is either created or updated in one operation, avoiding a race between a check and a write.

### Step 4: Trace Mutation-Level Concurrency Controls (FOCUS)

**Channel permission checks as a serialisation fence:**  
`ModelWithRestrictedChannelAccessMutation` calls `check_channel_permissions` before proceeding (FOCUS). While primarily a permission check, this also serves as a serialisation point — mutations that would conflict across channels are prevented from executing without the appropriate channel scope.

**`ObjectWithMetadata`** (`saleor/graphql/meta/types.py:49-154`) — `GUARD`/`ACCUMULATE` behavior with `_filter_metadata` and `_get_metadata_instance` (FOCUS). Metadata reads go through a consistent accessor, which when combined with Django's transactional model ensures that metadata reads during a write transaction see a consistent snapshot.

**Ordered filtering with `Q` and subqueries:**  
Multiple `filter_by_contains_referenced_object_ids` functions (`saleor/graphql/product/filters/product_variant.py:521-556`, `saleor/graphql/page/filters.py:505-540`, `saleor/graphql/product/filters/product_attributes.py:757-792`) use `Q` expressions and delegate to `_filter_by_contains_all_referenced_object_ids` / `_filter_by_contains_any_referenced_object_ids` (FOCUS). These are read-only filters, but their use of subquery composition (rather than in-application set operations) keeps filtering inside the database's MVCC isolation boundary.

### Step 5: Identify What Is Not Covered (GAPS)

Per GAPS (type: STRUCTURAL, coverage: 83 symbols in L3, 11 with behavior annotations):
- `get_translated_object_id` (3 occurrences) and `linked_object` are uncovered.
- The clue does not show any optimistic locking mechanism (e.g., version counters or ETags on the GraphQL mutation inputs).
- The `checkout_qs_select_for_update` helper (referenced by name in the mech-1 snippets, but not in this clue's FOCUS) is analogous to `user_qs_select_for_update` but its implementation details are not shown here.
- Whether `updates_amounts_for_order` is wrapped in a `transaction.atomic()` call cannot be determined from the clue alone.
- The `allow_writer()` context manager (used in the mech-1 snippets' `set_search_index_dirty`) appears to be part of a read/write database routing setup; its relationship to concurrency safety in other write paths is not traceable from this clue.

## Synthesized Answer

Saleor's concurrent object update safety relies on **three complementary mechanisms**, all grounded in the evidence:

1. **`SELECT FOR UPDATE` via per-domain `lock_objects.py` modules:**  
   Each domain that requires safe concurrent updates has a `lock_objects.py` file (e.g., `saleor/account/lock_objects.py` with `user_qs_select_for_update`, `saleor/app/lock_objects.py` imported by `AppProblemDismiss` and `AppProblemCreate`). These helpers apply row-level database locks within a `transaction.atomic()` block, ensuring that concurrent writers serialise on the locked rows rather than reading stale data.

2. **Django `F` expressions for atomic field updates:**  
   `SortableModel` (`saleor/core/models.py`) uses `F` expressions in `save` and `Max` in `get_max_sort_order` to update ordering fields without a read-modify-write race. `F` expressions translate directly to SQL arithmetic, making the update atomic at the database level.

3. **Coordinated multi-field update functions:**  
   Financial and discount updates use dedicated functions that encapsulate multiple field writes: `updates_amounts_for_order` (authorize + charge amounts), `_update_order_line_discount_object` (discount state), and `create_or_update_discount_object_from_order_level_voucher` (upsert pattern). By centralising related writes in a single function, Saleor makes it easier to wrap them in a single transaction and avoids partial-update inconsistencies.

No optimistic locking (version counters/ETags) is visible in the clue. The primary concurrency strategy is **pessimistic row locking** (`SELECT FOR UPDATE`) combined with **atomic SQL expressions** (`F`) and **transactional encapsulation** of multi-field updates.
