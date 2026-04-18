# Enterprise v4 (full-stack): ent-saleor-mech-1
Date: 2026-04-18

## Answer
Saleor keeps search indexing running as a background pipeline built around dirty flags plus batch recomputation. In the prompt, entities are marked dirty through helpers like `mark_search_index_dirty`, `mark_checkout_search_index_dirty`, `mark_gift_cards_search_index_as_dirty`, and `set_search_index_dirty`; then `update_checkouts_search_vector` rebuilds `search_vector` values by composing checkout, line, payment, and transaction fragments. [Prompt clue `mark_search_index_dirty`, `mark_checkout_search_index_dirty`, `set_search_index_dirty`, `update_checkouts_search_vector`; Prompt source snippets in `saleor/checkout/search/indexing.py`]

The actual scheduling hook is Celery Beat. Saleor’s contributing guide says explicitly: “The search vector update task is triggered by celery beat scheduler,” and immediately adds that “This feature will not work without task queue configuration.” [`CONTRIBUTING.md` 411-413]

Operationally, the two required processes are also documented: `uv run poe worker` starts the Celery worker, and `uv run poe scheduler` starts the Celery Beat scheduler. [`CONTRIBUTING.md` 90-99]

That operational guidance lines up with the prompt’s architecture/config context, which names Celery as the background-job and beat-scheduling system and shows broker settings such as `CELERY_BROKER_URL`. [Prompt ARCH 25-26; Prompt FOCUS `.env.example` and `saleor/tests/settings.py`]

At execution time, the task itself is careful about data integrity: the source snippet for `update_checkouts_search_vector` flips `search_index_dirty`, regenerates vectors, and bulk-updates locked rows; `set_search_index_dirty` uses `transaction.atomic()`, `allow_writer()`, and row locking to keep the update safe. [Prompt source snippets `set_search_index_dirty` and `update_checkouts_search_vector`]

## Synthesis
Rows get marked dirty in business code, Celery Beat schedules the update task, the Celery worker executes it, and the task recomputes and writes search vectors safely. Without task-queue infrastructure, that scheduled indexing path does not run.

