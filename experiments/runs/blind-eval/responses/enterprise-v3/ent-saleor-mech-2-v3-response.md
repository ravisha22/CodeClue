# Enterprise v3 (arch-enhanced): ent-saleor-mech-2
Date: 2026-04-18

## Answer
The strongest concurrency-control evidence in the clue is that Saleor keeps locking helpers in app-local `lock_objects.py` modules and uses `select_for_update()`-style row locks. The index explicitly shows `saleor/account/lock_objects.py` with `user_qs_select_for_update`, which indicates an app-local locking helper dedicated to user rows (INDEX, ent-saleor-mech-2-v3.prompt.md:55-58).

The clearest drill-down evidence comes from the related search-indexing path: `set_search_index_dirty()` opens `transaction.atomic()`, calls `checkout_qs_select_for_update()`, and comments that it selects and locks checkouts "to ensure updating in correct order" before issuing the bulk update (set_search_index_dirty, saleor/checkout/search/indexing.py:60-72). That supports the general mechanism of using `select_for_update()` on querysets to serialize concurrent updates and avoid races.

So, from this prompt alone, the supported answer is: Saleor protects concurrent updates by placing lock helpers in per-app `lock_objects.py` files and by taking database row locks with `select_for_update()` inside transactions before updating shared state (INDEX, ent-saleor-mech-2-v3.prompt.md:55-58; set_search_index_dirty, saleor/checkout/search/indexing.py:60-72).

## Gaps
The clue does **not** expose the higher-level lock-order guidance from the question. It does not state the primary-key ordering rule, and it does not show a cross-model ordering convention such as locking `Order` before `OrderLine` (GAPS, ent-saleor-mech-2-v3.prompt.md:258-262).
