# Enterprise v2: ent-saleor-mech-1
Date: 2026-04-17

## Question
How does Saleor keep search indexing and other scheduled work running?

## Reasoning Scaffold

### Step 1: Identify Relevant Symbols (FOCUS, SYM, INDEX)

The FOCUS section is dense with search indexing symbols, all in `saleor/checkout/search/indexing.py`, `saleor/product/search.py`, `saleor/giftcard/search.py`, and attribute mutation helpers. The key symbols are:

- `set_search_index_dirty` (`saleor/checkout/search/indexing.py:60-72`) — resets search vectors and marks checkout rows dirty/clean (FOCUS + snippet)
- `update_checkouts_search_vector` (`:27-57`) — orchestrates batch vector updates (FOCUS + snippet)
- `prepare_checkout_search_vector_value` (`:75-115`) — assembles all vector components for a single checkout (FOCUS + snippet)
- `generate_checkout_lines_search_vector_value` (`:180-217`), `generate_checkout_payments_search_vector_value` (`:156-177`), `generate_checkout_transactions_search_vector_value` (`:118-153`) — sub-generators per data type (FOCUS + snippets)
- `_prep_product_search_vector_index` (`saleor/product/search.py:32-49`) — product search index preparation (FOCUS)
- `mark_search_index_dirty` (`saleor/graphql/attribute/mutations/attribute_value_update.py:86-88`) — called by `post_save_action` (FOCUS)
- `mark_checkout_search_index_dirty` (`saleor/payment/utils.py:1684-1686`) — called by `create_transaction_event_from_request_and_webhook_response` (FOCUS)
- `mark_gift_cards_search_index_as_dirty` / `mark_gift_cards_search_index_as_dirty_by_users` (`saleor/giftcard/search.py:43-57`) (FOCUS)
- `mark_products_search_index_as_dirty_task` (`saleor/product/migrations/tasks/saleor3_23.py:15-31`) and `mark_gift_cards_search_index_as_dirty_task` (`saleor/giftcard/migrations/tasks/saleor3_22.py:10-11`) — Celery tasks embedded in migration task files (FOCUS)
- `update_products_search_index` (multiple callers in `saleor/graphql/page/mutations/`) (FOCUS)
- Settings: `CELERY_BROKER_URL=redis://localhost:6379/1` (`.env.example`), `CELERY_TASK_ALWAYS_EAGER=True` in test settings (FOCUS)

### Step 2: Trace the "Dirty Flag + Deferred Rebuild" Pattern (FOCUS + Snippets)

The core mechanism is a **dirty-flag pattern** implemented with a `search_index_dirty` boolean column and `search_vector` field on each indexed model:

**Marking dirty (write path):**
- When a mutation saves a related entity, it marks affected rows as dirty rather than immediately rebuilding the index:
  - `mark_search_index_dirty` (`saleor/graphql/attribute/mutations/attribute_value_update.py:86-88`) is called by `post_save_action` of `AttributeValueUpdate`. It calls `_mark_pages_search_index_dirty` and `_mark_products_search_index_dirty`, each using `Exists`/`OuterRef` to find all affected pages/products (FOCUS).
  - `get_page_ids_to_search_index_update` and `get_product_ids_to_search_index_update` in `AttributeDelete.perform_mutation` find IDs to mark dirty when an attribute is deleted (FOCUS).
  - `mark_checkout_search_index_dirty` (`saleor/payment/utils.py:1684-1686`) is called by `create_transaction_event_from_request_and_webhook_response` — payment transaction events trigger checkout re-indexing (FOCUS).
  - `mark_gift_cards_search_index_as_dirty` (`saleor/giftcard/search.py:43-46`) — `ACCUMULATE(gift_cards loop -> result)`, called by `mark_gift_cards_search_index_as_dirty_by_users` which filters by users via `Q` (FOCUS).
  - `update_products_search_index` is called directly from `PageDelete.perform_mutation`, `PageUpdate.save`, and bulk page mutations — page changes propagate product index dirtying (FOCUS).

**Rebuilding (scheduled/async path):**
- `set_search_index_dirty` (snippet, `saleor/checkout/search/indexing.py:60-72`):
  ```python
  with transaction.atomic():
      with allow_writer():
          pks = checkout_qs_select_for_update().filter(pk__in=checkout_pks).values_list("pk", flat=True)
          Checkout.objects.filter(pk__in=pks).update(
              search_vector=None, search_index_dirty=search_index_dirty_value
          )
  ```
  This sets `search_vector=None` and flips `search_index_dirty` inside a transaction with a `SELECT FOR UPDATE` lock to prevent concurrent races (snippet).

- `update_checkouts_search_vector` (snippet, `saleor/checkout/search/indexing.py:27-57`):
  1. Calls `set_search_index_dirty(checkout_pks, search_index_dirty_value=False)` first — optimistically marks rows as clean before processing, so no other worker picks them up.
  2. Loads checkout data: `checkout_data_map = load_checkout_data(checkouts)`.
  3. For each checkout, calls `prepare_checkout_search_vector_value` and stores result as `FlatConcatSearchVector(...)`.
  4. On any exception, calls `set_search_index_dirty(checkout_pks, search_index_dirty_value=True)` to reset dirty flag, then re-raises — ensuring dirty rows are retried next cycle.
  5. In a final `transaction.atomic()` + `allow_writer()` block, re-acquires locks with `checkout_qs_select_for_update()` and calls `Checkout.objects.bulk_update(checkouts, ["search_vector"])`.

### Step 3: Trace Search Vector Assembly (Snippets)

`prepare_checkout_search_vector_value` (snippet) assembles a list of `NoValidationSearchVector` entries with weighted components:
- **Weight A** (highest): checkout token (always), user first name, user last name, user email
- **Weight B**: billing address components, shipping address components
- **Weight C**: product name, variant SKU, variant name (per checkout line, up to `settings.CHECKOUT_MAX_INDEXED_LINES`)
- **Weight D** (lowest): payment global ID and `psp_reference` (up to `settings.CHECKOUT_MAX_INDEXED_PAYMENTS`); transaction token, `psp_reference`, and event `psp_reference` values (up to `settings.CHECKOUT_MAX_INDEXED_TRANSACTIONS`)

The settings constants (`CHECKOUT_MAX_INDEXED_LINES`, `CHECKOUT_MAX_INDEXED_PAYMENTS`, `CHECKOUT_MAX_INDEXED_TRANSACTIONS`) bound the size of each indexed vector (snippets).

For products, `_prep_product_search_vector_index` (`saleor/product/search.py:32-49`) loops over products: `ACCUMULATE(products loop -> result)`, calls `prepare_product_search_vector_value`, and uses `FlatConcatSearchVector` — the same search vector type (FOCUS).

### Step 4: Scheduled Work — Celery Integration

- `.env.example` sets `CELERY_BROKER_URL=redis://localhost:6379/1` — Celery uses Redis as its broker (FOCUS).
- Test settings override `CELERY_TASK_ALWAYS_EAGER=True` so tasks run synchronously in tests (FOCUS).
- `mark_products_search_index_as_dirty_task` (`saleor/product/migrations/tasks/saleor3_23.py:15-31`) is a Celery task that marks products dirty in bulk — used as part of a data migration to trigger re-indexing after a schema change (FOCUS).
- `mark_gift_cards_search_index_as_dirty_task` (`saleor/giftcard/migrations/tasks/saleor3_22.py:10-11`) is the equivalent for gift cards (FOCUS).
- There is also a migration function `mark_products_search_index_as_dirty` (`saleor/product/migrations/0203_mark_products_search_index_as_dirty.py:10-15`) that is called as a data migration operation (FOCUS).
- `send_email` (`saleor/plugins/sendgrid/tasks.py:22`) confirms the Celery task pattern is also used for email delivery via the Sendgrid plugin (SYM).

The overall scheduled-work pattern is: **write-side events mark rows dirty → a Celery worker picks up dirty rows → `update_*_search_vector` rebuilds vectors atomically with pessimistic locking**.

### Gaps / Uncertainty

Per GAPS (type: MECHANISTIC, coverage: 83 symbols in L3, 32 with behavior annotations):
- `generate_attributes_search_vector_value` — attribute-value vector generation details are uncovered.
- `get_reference_attribute_search_value` — how reference attributes (page/product references as attribute values) contribute to search vectors is not shown.
- `mark_pages_search_vector_as_dirty` and `mark_pages_search_vector_as_dirty_in_batches` — the dirty-marking mechanism for pages (parallel to the checkout/product logic) is not covered.
- How the periodic Celery beat schedule (if any) triggers the actual rebuild worker (what task picks up dirty rows and calls `update_checkouts_search_vector`) is not shown in the clue — the snippets only show the rebuild function itself, not how it is scheduled or triggered.
- `update_products_search_vector` (called by `_prep_product_search_vector_index`) and its trigger mechanism are not covered.

## Synthesized Answer

Saleor uses a **two-phase dirty-flag + deferred rebuild** pattern for search indexing:

**Phase 1 — Mark dirty (inline, synchronous):** When a relevant entity changes (attribute value update, attribute delete, payment transaction, page delete/update), mutation `post_save_action` hooks or action functions call `mark_*_search_index_dirty` helpers. These use `Exists`/`OuterRef` subqueries to identify all transitively affected rows and set their `search_index_dirty=True` / `search_vector=None`. This is fast and inline — no vector computation happens at write time.

**Phase 2 — Rebuild (deferred, Celery-backed):** A Celery worker (broker: Redis on port 6379/1) consumes dirty rows and calls `update_checkouts_search_vector` (or equivalent for products/gift cards). The rebuild function:
1. First marks rows as clean (`search_index_dirty=False`) with a `SELECT FOR UPDATE` lock inside a `transaction.atomic()` block.
2. Assembles `NoValidationSearchVector` components weighted by field significance (A: identity fields, B: address, C: line items, D: payment/transaction refs).
3. If any exception occurs, resets `search_index_dirty=True` so the batch is retried.
4. Writes the final `search_vector` via `bulk_update` inside a second locked transaction.

For data migration scenarios (schema upgrades requiring full re-index), dedicated Celery tasks (`mark_products_search_index_as_dirty_task`, `mark_gift_cards_search_index_as_dirty_task`) bulk-mark rows, which then flow through the same rebuild pipeline.

Other scheduled work (e.g., email delivery via `send_email` in the Sendgrid plugin) follows the same Celery infrastructure.
