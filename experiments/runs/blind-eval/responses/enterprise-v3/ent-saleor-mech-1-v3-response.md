# Enterprise v3 (arch-enhanced): ent-saleor-mech-1
Date: 2026-04-18

## Answer
The clue gives a fairly detailed picture of **how search indexing work itself is performed**, but not of the full scheduler/worker lifecycle. Search updates are driven by dirty flags plus batch recomputation. `mark_search_index_dirty` fans out to page/product dirty-marking helpers; there are dedicated dirty-marking functions for gift cards and checkout search state; and `update_checkouts_search_vector` rebuilds vectors by loading checkout data and composing line/payment/transaction search-vector pieces (mark_search_index_dirty, saleor/graphql/attribute/mutations/attribute_value_update.py:86-88; _mark_pages_search_index_dirty, saleor/graphql/attribute/mutations/attribute_value_update.py:113-119; _mark_products_search_index_dirty, saleor/graphql/attribute/mutations/attribute_value_update.py:91-110; mark_checkout_search_index_dirty, saleor/payment/utils.py:1684-1686; mark_gift_cards_search_index_as_dirty, saleor/giftcard/search.py:43-46; update_checkouts_search_vector, saleor/checkout/search/indexing.py:27-57; prepare_checkout_search_vector_value, saleor/checkout/search/indexing.py:75-115).

The drill-down snippet shows the update path is concurrency-safe. `set_search_index_dirty()` runs inside `transaction.atomic()`, uses `allow_writer()`, locks the target checkouts through `checkout_qs_select_for_update()`, and then bulk-updates `search_vector` and `search_index_dirty` (set_search_index_dirty, saleor/checkout/search/indexing.py:60-72).

The architectural context also shows that background work depends on Celery and broker configuration: Saleor’s dependencies include "Celery for background jobs and beat scheduling" and `.env.example` contains `CELERY_BROKER_URL` (ARCH, ent-saleor-mech-1-v3.prompt.md:25-26; .env.example, ent-saleor-mech-1-v3.prompt.md:132-134).

## Gaps
The prompt still does **not** show the specific scheduler trigger for search-vector updates, does not prove that Celery Beat is what launches this exact task, and does not include the repo command lines for starting the worker or scheduler. Those operational details cannot be derived here (GAPS, ent-saleor-mech-1-v3.prompt.md:259-263).
