# Enterprise v4 (full-stack): ent-saleor-mech-2
Date: 2026-04-18

## Answer
Saleor’s main concurrency-safety mechanism is Django row locking via `select_for_update()` on querysets. Both the contributing guide and AGENTS guidance say to use `select_for_update()` for concurrent read-modify-write flows to prevent race conditions, and the AGENTS example wraps that in a transaction. [`CONTRIBUTING.md` 388; `AGENTS.md` 103-123]

When multiple rows are locked, Saleor wants the lock order to be stable. The repo guidance says to lock multiple objects in a consistent order to avoid deadlocks, typically by primary key, and AGENTS gives the exact helper pattern `order_by("pk").select_for_update(...)`. [`CONTRIBUTING.md` 392-393; `AGENTS.md` 116-121]

When multiple models are involved, Saleor also requires a defined cross-model order. The documented example is to lock `Order` before `OrderLine`. [`CONTRIBUTING.md` 394]

To keep this pattern repeatable, Saleor says locking helpers should live in an app-local `lock_objects.py` file (or, for multi-model helpers, in the app of the last model locked). The prompt clue gives a concrete example with `saleor/account/lock_objects.py` and `user_qs_select_for_update`. [`CONTRIBUTING.md` 400-404; Prompt INDEX `saleor/account/lock_objects.py` -> `user_qs_select_for_update`]

## Synthesis
So the safe-update recipe is: wrap the change in a transaction, lock rows with `select_for_update()`, acquire locks in deterministic pk/model order, and centralize the locking queryset helpers in `lock_objects.py`.

