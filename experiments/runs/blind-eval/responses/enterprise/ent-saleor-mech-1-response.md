# Enterprise Eval: ent-saleor-mech-1
Date: 2026-04-17

## Question
How does Saleor keep search indexing and other scheduled work running?

---

## Reasoning Trace

### Step 1: Identify Search Indexing Symbols

The FOCUS section is rich with search-related symbols. They can be grouped by domain:

**Checkout search indexing:**
- `update_checkouts_search_vector` (saleor/checkout/search/indexing.py:27-57) — orchestrator that updates search vectors for multiple checkouts (FOCUS + source snippet).
- `set_search_index_dirty` (saleor/checkout/search/indexing.py:60-72) — resets search vectors by marking them dirty (FOCUS + source snippet).
- `prepare_checkout_search_vector_value` (saleor/checkout/search/indexing.py:75-115) — assembles all search vector components for a checkout (FOCUS + source snippet).
- `generate_checkout_lines_search_vector_value` (saleor/checkout/search/indexing.py:180-217) — generates vectors from checkout lines (SKU, product name, variant name) (FOCUS + source snippet).
- `generate_checkout_payments_search_vector_value` (saleor/checkout/search/indexing.py:156-177) — generates vectors from payment IDs and PSP references (FOCUS + source snippet).
- `generate_checkout_transactions_search_vector_value` (saleor/checkout/search/indexing.py:118-153) — generates vectors from transaction tokens, PSP references, and event PSP references (FOCUS + source snippet).
- `mark_checkout_search_index_dirty` (saleor/payment/utils.py:1684-1686) — called by `create_transaction_event_from_request_and_webhook_response` (FOCUS).

**Product search indexing:**
- `_prep_product_search_vector_index` (saleor/product/search.py:32-49) — accumulates over products, calls `prepare_product_search_vector_value`. Called by `update_products_search_vector`. Uses `FlatConcatSearchVector` (FOCUS).
- `generate_attributes_search_vector_value_with_assignment` (saleor/product/search.py:155-172) — generates vectors from assigned attributes. Called by `generate_variants_search_vector_value` (FOCUS).
- `mark_products_search_index_as_dirty` (saleor/product/migrations/0203_mark_products_search_index_as_dirty.py:10-15) — migration that marks products dirty (FOCUS).
- `mark_products_search_index_as_dirty_task` (saleor/product/migrations/tasks/saleor3_23.py:15-31) — a **task** for marking products dirty, suggesting Celery or similar async task infrastructure (FOCUS).

**Page search indexing:**
- `generate_attributes_search_vector_value` (saleor/page/search.py:192-211) — generates vectors from page attribute values. Called by `prepare_page_search_vector_value` (FOCUS).
- Multiple `update_products_search_index` methods across page mutations: `PageDelete` (saleor/graphql/page/mutations/page_delete.py:48-62), `PageTypeDelete` (page_type_delete.py:43-60), `PageUpdate` (page_update.py:70-84), and bulk mutations (bulk_mutations.py:53-67, :146-164) — all mark product search indexes dirty when pages change, showing cross-domain search invalidation (FOCUS).

**Gift card search indexing:**
- `mark_gift_cards_search_index_as_dirty` (saleor/giftcard/search.py:43-46) — accumulates over gift cards. Called by `mark_gift_cards_search_index_as_dirty_by_users` (FOCUS).
- `mark_gift_cards_search_index_as_dirty_by_users` (saleor/giftcard/search.py:49-57) — calls `mark_gift_cards_search_index_as_dirty`. Uses `Q` (FOCUS).
- `mark_gift_cards_search_index_as_dirty` (saleor/giftcard/migrations/0023_mark_gift_cards_search_vector_as_dirty.py:10-15) — migration-level dirty marking (FOCUS).
- `mark_gift_cards_search_index_as_dirty_task` (saleor/giftcard/migrations/tasks/saleor3_22.py:10-11) — another **task** for async processing (FOCUS).

**Order search indexing:**
- `prepare_order_search_vector_value` (saleor/order/search.py:23-93) — assembles vectors from discounts, events, invoices, lines, payments, and transactions. Called by `update_order_search_vector`. Uses `NoValidationSearchVector` and `Value` (FOCUS).

**Attribute-triggered search updates:**
- `mark_search_index_dirty` (saleor/graphql/attribute/mutations/attribute_value_update.py:86-88) — called by `post_save_action` of `AttributeValueUpdate`; calls `_mark_pages_search_index_dirty` and `_mark_products_search_index_dirty` (FOCUS).
- `_mark_products_search_index_dirty` (line 91-110) and `_mark_pages_search_index_dirty` (line 113-119) — use `Exists`, `OuterRef`, `Q` to find affected products/pages (FOCUS).
- `get_product_ids_to_search_index_update` and `get_page_ids_to_search_index_update` (saleor/graphql/attribute/mutations/attribute_delete.py:84-106) — called by `perform_mutation` of `AttributeDelete` (FOCUS).
- `get_product_ids_to_search_index_update_for_attribute_values` and `get_page_ids_to_search_index_update_for_attribute_values` (saleor/graphql/attribute/mutations/utils.py:8-52) — utility functions for attribute-value-level changes (FOCUS).

**Search filter entry points:**
- `filter_checkout_search` (saleor/graphql/checkout/filters.py:101-102) — delegates to `prefix_search` (FOCUS).
- `filter_order_search` (saleor/graphql/order/filters.py:184-185) — delegates to `prefix_search` (FOCUS).
- `filter_search` (saleor/graphql/product/filters/product_helpers.py:324-325) — delegates to `prefix_search` (FOCUS).
- `filter_user_search` (saleor/graphql/account/filters.py:67-68) — delegates to `prefix_search` (FOCUS).

### Step 2: Analyze the Core Search Update Mechanism (Source Snippets)

The source snippet for `update_checkouts_search_vector` reveals a sophisticated two-phase approach:

**Phase 1 — Pre-mark dirty:**
```python
set_search_index_dirty(checkout_pks, search_index_dirty_value=False)
```
Before computing search vectors, the function first marks `search_index_dirty=False` and clears `search_vector=None`. This uses `transaction.atomic()` with `allow_writer()` and `checkout_qs_select_for_update()` (SELECT FOR UPDATE) for concurrency safety (source snippet, `set_search_index_dirty`).

**Phase 2 — Compute and bulk update:**
The function loads checkout data via `load_checkout_data(checkouts)`, then computes `FlatConcatSearchVector(*prepare_checkout_search_vector_value(checkout, data))` per checkout. Finally, it bulk-updates with `Checkout.objects.bulk_update(checkouts, ["search_vector"])`, again inside `transaction.atomic()` and `allow_writer()` with SELECT FOR UPDATE (source snippet, `update_checkouts_search_vector`).

**Error recovery:** If processing fails between phases, `set_search_index_dirty(checkout_pks, search_index_dirty_value=True)` re-marks the checkouts as dirty so they can be retried (source snippet, `update_checkouts_search_vector`, lines in `except` block).

### Step 3: Search Vector Composition (Source Snippets)

`prepare_checkout_search_vector_value` assembles vectors with **weighted priorities** (source snippet):
- **Weight "A"** (highest): checkout token, user first/last name, user email
- **Weight "B"**: billing and shipping address fields
- **Weight "C"**: line items — variant SKU, product name, variant name
- **Weight "D"** (lowest): payment global IDs, PSP references, transaction tokens, transaction event PSP references

All vectors use `NoValidationSearchVector` with `config="simple"` (PostgreSQL text search configuration).

Lines, payments, and transactions are capped by settings: `settings.CHECKOUT_MAX_INDEXED_LINES`, `settings.CHECKOUT_MAX_INDEXED_PAYMENTS`, `settings.CHECKOUT_MAX_INDEXED_TRANSACTIONS` (source snippets for each generator function).

### Step 4: Scheduled Work / Task Infrastructure

Two symbols explicitly reference **tasks**, indicating asynchronous/scheduled processing:
- `mark_products_search_index_as_dirty_task` (saleor/product/migrations/tasks/saleor3_23.py:15-31) (FOCUS).
- `mark_gift_cards_search_index_as_dirty_task` (saleor/giftcard/migrations/tasks/saleor3_22.py:10-11) (FOCUS).

These task modules reside under `migrations/tasks/` with version-specific naming (`saleor3_22`, `saleor3_23`), suggesting they are migration-associated background tasks that run during or after schema migrations to rebuild search indexes.

Additionally, the dirty-flag pattern itself implies a scheduled re-indexer: objects are marked with `search_index_dirty=True`, and a separate process (likely a Celery task or management command) periodically picks up dirty records and recomputes their search vectors.

### Step 5: Dirty-Flag Pattern as the Scheduling Mechanism

The dirty-flag pattern is the primary coordination mechanism:
1. **Mutations mark dirty:** When data changes (attribute value update, page delete, transaction event creation), the relevant mutation/handler marks affected objects' `search_index_dirty=True` (e.g., `mark_search_index_dirty` called from `post_save_action` of `AttributeValueUpdate`, `mark_checkout_search_index_dirty` called from payment utils).
2. **Batch re-index:** Functions like `update_checkouts_search_vector` and `update_products_search_vector` process dirty records in batches, using SELECT FOR UPDATE to prevent concurrent update conflicts.
3. **Cross-domain propagation:** Page mutations trigger product search index updates (multiple `update_products_search_index` methods), attribute changes trigger both page and product updates — showing the dirty flag propagates across domain boundaries.

### Step 6: GAPS — What Cannot Be Determined

Per the GAPS section:
- **Type:** MECHANISTIC (body logic needed for full answer)
- **Coverage:** 80 symbols in L3, 32 with behavior annotations
- **Drill:** `saleor/checkout/search/indexing.py` (~15 lines, `set_search_index_dirty`) — provided in source snippets
- **Uncovered symbols:** `generate_attributes_search_vector_value`, `get_reference_attribute_search_value`, `mark_pages_search_vector_as_dirty`, `mark_pages_search_vector_as_dirty_in_batches`

From the evidence, the following **cannot** be determined:
- The exact scheduling mechanism (Celery beat, cron, management command) that triggers the batch re-indexer
- The task queue configuration or worker setup
- Whether there are other types of scheduled work beyond search indexing (e.g., cleanup jobs, analytics aggregation)
- The implementation of `load_checkout_data` used in `update_checkouts_search_vector`
- How `mark_pages_search_vector_as_dirty_in_batches` works (listed in GAPS uncovered)
- The full implementation of `FlatConcatSearchVector` and `NoValidationSearchVector` beyond their usage

---

## Synthesized Answer

Saleor keeps search indexing running through a **dirty-flag + batch re-index** pattern backed by PostgreSQL full-text search vectors:

1. **Dirty-flag invalidation:** When data changes, mutation handlers mark affected objects as dirty. Examples: `mark_search_index_dirty` (saleor/graphql/attribute/mutations/attribute_value_update.py:86) propagates to products and pages via `_mark_products_search_index_dirty` and `_mark_pages_search_index_dirty`; `mark_checkout_search_index_dirty` (saleor/payment/utils.py:1684) fires on transaction events; page mutations trigger `update_products_search_index` across 5+ call sites.

2. **Batch re-indexing with concurrency safety:** `update_checkouts_search_vector` (saleor/checkout/search/indexing.py:27-57, source snippet) demonstrates the pattern: pre-clear vectors under SELECT FOR UPDATE (`set_search_index_dirty`), compute weighted `NoValidationSearchVector` values (weight A–D) via `prepare_checkout_search_vector_value`, then `bulk_update` inside `transaction.atomic()`. On failure, dirty flags are restored for retry.

3. **Weighted search vectors:** Search vectors use PostgreSQL `tsvector` with weights: A (tokens, names, emails), B (addresses), C (product/variant info), D (payment/transaction references). Indexable items are capped via settings (`CHECKOUT_MAX_INDEXED_LINES`, etc.). All use `config="simple"`.

4. **Cross-domain search filters:** GraphQL search resolvers (`filter_checkout_search`, `filter_order_search`, `filter_search`, `filter_user_search`) all delegate to `prefix_search`, consuming the pre-built search vectors.

5. **Scheduled tasks:** `mark_products_search_index_as_dirty_task` (saleor/product/migrations/tasks/saleor3_23.py:15-31) and `mark_gift_cards_search_index_as_dirty_task` (saleor/giftcard/migrations/tasks/saleor3_22.py:10-11) are migration-associated background tasks. **The exact task runner (Celery, etc.) and scheduling configuration cannot be determined from the clue alone** (GAPS limitation).
