# Enterprise v2: ent-netbox-mech-1
Date: 2026-04-17

## Question
How are NetBox background jobs enqueued, scheduled, and executed?

## Reasoning Scaffold

### Step 1: Identify relevant symbols from FOCUS, SYM, and INDEX

**Core job execution:**

| Symbol | Location | Description |
|---|---|---|
| `run_script` | `netbox/extras/jobs.py:30` | "Core script execution task" (SYM) |
| `run` | `netbox/extras/jobs.py:100` | "Run the script" (SYM) |
| `is_background_request` | `netbox/utilities/jobs.py:14-18` | "Return True if the request is being processed as a background job"; DELEGATE to `hasattr`; called_by `process_request_as_job` (FOCUS) |
| `get_jobs` (netbox/jobs.py) | `netbox/netbox/jobs.py:134-147` | "Get all jobs of this `JobRunner` related to a specific instance"; called_by `enqueue_once`, `JobRunner` (FOCUS) |
| `enqueue_once` | (implicit via `get_jobs`) | Part of `JobRunner` pattern |

**RQ integration:**

| Symbol | Location | Description |
|---|---|---|
| `get_rq_jobs` | `netbox/core/utils.py:28-38` | "Return a list of all RQ jobs"; ACCUMULATE from `get_queues_list()` loop (FOCUS) |
| `get_rq_jobs_from_status` | `netbox/core/utils.py:41-74` | "Return the RQ jobs with the given status"; BRANCH on `status != RQJobStatus.DEFERRED`; raises `Http404` (FOCUS) |
| `CoreRootView` | `netbox/core/api/views.py:30-35` | imports `django_rq.queues`, `django_rq.settings` — confirming RQ is the queue backend (FOCUS) |

**Job lifecycle helpers:**

| Symbol | Location | Description |
|---|---|---|
| `delete_expired_jobs` | `netbox/core/jobs.py:143-159` | "Delete any jobs older than the configured retention period"; called_by `SystemHousekeepingJob`; uses `Config` (FOCUS) |
| `get_jobs` (extras/models/mixins.py) | `netbox/extras/models/mixins.py:40-48` | "Returns a list of Jobs associated with this specific script or report module"; DELEGATE to `jobs.filter` (FOCUS) |
| `get_latest_jobs` | `netbox/netbox/models/features.py:466-470` | "Return a list of the most recent jobs for this instance"; DELEGATE to `jobs.filter.order_by.defer` (FOCUS) |
| `get_jobs` (views/generic) | `netbox/netbox/views/generic/feature_views.py:209-214` | called_by `ObjectJobsView` — the UI view for listing jobs on an object (FOCUS) |
| `JobsMixin` | (via `DataSource.extends`) | `DataSource` (FOCUS: `netbox/core/models/data.py:35-278`) extends `JobsMixin, PrimaryModel` — establishes that models can have jobs attached |

**UI views for job management (all in `netbox/core/views.py`, FOCUS):**

| Symbol | What it handles |
|---|---|
| `BackgroundQueueListView` (extends `TableMixin, BaseRQView`) | List RQ queues |
| `BackgroundTaskListView` (extends `TableMixin, BaseRQView`) | List tasks in a queue |
| `BackgroundTaskView` (extends `BaseRQView`) | View single task detail; raises `Http404` |
| `BackgroundTaskDeleteView` (extends `BaseRQView`) | Delete a task |
| `BackgroundTaskEnqueueView` (extends `BaseRQView`) | Manually enqueue a task |
| `BackgroundTaskRequeueView` (extends `BaseRQView`) | Requeue an existing task |
| `BackgroundTaskStopView` (extends `BaseRQView`) | Stop a running task |

**API serializers for job/queue/worker state (all `netbox/core/api/serializers_/tasks.py`, FOCUS):**

| Symbol | Description |
|---|---|
| `BackgroundTaskSerializer` | extends `Serializer`; calls `get_position`, `get_status` |
| `BackgroundQueueSerializer` | extends `Serializer` |
| `BackgroundWorkerSerializer` | extends `Serializer`; calls `get_state` |

**Tables for UI display (all `netbox/core/tables/tasks.py`, FOCUS):**
- `BackgroundQueueTable` (extends `BaseTable`)
- `BackgroundTaskTable` (extends `BaseTable`)

**URL routes for job management (all `netbox/core/urls.py`, FOCUS):**
- `path:background-queues/` → `BackgroundQueueListView`
- `path:background-queues/<i` → `BackgroundTaskListView`
- `path:background-tasks/<st` → `BackgroundTaskDeleteView`, `BackgroundTaskRequeueView`, `BackgroundTaskEnqueueView`, `BackgroundTaskStopView`, `BackgroundTaskView`
- `path:background-workers/<` → `WorkerListView`, `WorkerView`
- `path:jobs/` → include
- `path:jobs/<int:pk>/` → include

**Form mixin:**
- `BackgroundJobMixin` (FOCUS: `netbox/utilities/forms/mixins.py:102-116`): extends `Form`, imports `netbox.registry` — the form-level integration point for triggering jobs.

**Script-specific job view:**
- `ScriptJobsView` (FOCUS: `netbox/extras/views.py:1751-1765`): extends `BaseScriptView`, calls `get_object` — the UI view listing jobs for a specific script.

### Step 2: Trace the enqueuing mechanism

From the clue, the `JobRunner` pattern is central:
- `get_jobs` (FOCUS: `netbox/netbox/jobs.py:134-147`) is a classmethod on `JobRunner` that retrieves all jobs for a given instance. It is called by `enqueue_once`, which implies that `enqueue_once` first calls `get_jobs` to check for existing jobs before enqueuing a new one — preventing duplicate jobs.
- `is_background_request` (FOCUS: `netbox/utilities/jobs.py:14-18`) uses `DELEGATE(hasattr -> result)` — it checks for a specific attribute on the request object (set by the background job framework) to determine if the current code is running inside a background job. Its caller `process_request_as_job` suggests there is a mechanism to re-run a synchronous request as an asynchronous job.
- `BackgroundJobMixin` (form level) imports `netbox.registry`, connecting the form submission path to the background job system.

The underlying queue backend is **RQ (Redis Queue)**: `CoreRootView` imports `django_rq.queues` and `django_rq.settings` (FOCUS: `netbox/core/api/views.py`), and `get_rq_jobs` enumerates queues via `get_queues_list()` from the RQ integration.

### Step 3: Trace scheduling and execution

**Scheduling:**
- `get_rq_jobs_from_status` (FOCUS: `netbox/core/utils.py:41-74`) uses `BRANCH(status != RQJobStatus.DEFERRED -> get_jobs(queue, job_i..., else -> r...)` — the `DEFERRED` branch is handled differently from other statuses, indicating support for deferred (scheduled) execution in RQ.
- `delete_expired_jobs` (FOCUS: `netbox/core/jobs.py:143-159`) runs as part of `SystemHousekeepingJob`, consulting `Config` for the configured retention period. This is a housekeeping/maintenance job scheduled as part of the system.

**Script execution:**
- `run_script` (SYM: `netbox/extras/jobs.py:30`) is the "Core script execution task" — the function submitted to the RQ queue.
- `run` (SYM: `netbox/extras/jobs.py:100`) is the method on the Script object called within the RQ worker process.
- `sync_classes` (SYM: `netbox/extras/models/scripts.py:153`) "Syncs the file-based module to the database" — scripts defined on disk are registered in the database before execution.
- `save` and `delete` on `netbox/extras/models/scripts.py` manage the script module lifecycle.

**Job status tracking:**
- `get_latest_jobs` (FOCUS: `netbox/netbox/models/features.py:466-470`) DELEGATE to `jobs.filter.order_by.defer` — returns most recent job records in chronological order.
- `get_jobs` (extras/models/mixins.py:40-48) DELEGATE to `jobs.filter` — retrieves jobs scoped to a specific module.
- `BackgroundTaskSerializer.get_status` and `BackgroundWorkerSerializer.get_state` surface current job and worker state via the REST API.

### Gaps / Uncertainty

`(GAPS)` lists this as a **STRUCTURAL** question. Explicitly uncovered: `NetBoxModelFilter`, `NetBoxModelFilterSet`, `NetBoxModelFilterSetForm`, `README.md`. More specifically for the job question:
- The exact queue names and how many queues are defined cannot be determined.
- The full implementation of `process_request_as_job` (how a request is packaged and submitted to RQ) is not visible.
- The specific `enqueue_once` logic beyond its calling `get_jobs` is not fully described.
- Whether jobs can be scheduled with a future run time (cron-style) or only deferred/immediate cannot be fully confirmed beyond the existence of `RQJobStatus.DEFERRED`.

## Synthesized Answer

**Queue backend**: NetBox uses **RQ (Redis Queue)** via `django-rq` as its background job infrastructure. `CoreRootView` imports `django_rq.queues` and `django_rq.settings` (FOCUS: `netbox/core/api/views.py`). Queue enumeration is done by `get_rq_jobs` via `get_queues_list()` (FOCUS: `netbox/core/utils.py:28-38`).

**Enqueuing**: The `JobRunner` class (in `netbox/netbox/jobs.py`) provides `enqueue_once`, which calls `get_jobs` (FOCUS: `netbox/netbox/jobs.py:134-147`) to check for existing jobs before submitting, preventing duplicate enqueues. `process_request_as_job` (called by `is_background_request`, FOCUS: `netbox/utilities/jobs.py:14-18`) provides a mechanism to execute a web request asynchronously as a background job. At the form level, `BackgroundJobMixin` (FOCUS: `netbox/utilities/forms/mixins.py`) bridges form submissions to the job system via `netbox.registry`.

**Script execution**: `run_script` (SYM: `netbox/extras/jobs.py:30`) is the core RQ task function. Inside the worker, `Script.run` (SYM: `netbox/extras/jobs.py:100`) is called. Scripts are file-backed and synced to the DB via `sync_classes` (SYM: `netbox/extras/models/scripts.py:153`) before execution.

**Job status and deferred execution**: Jobs have RQ statuses including `DEFERRED`; `get_rq_jobs_from_status` handles deferred jobs separately from running/queued jobs (FOCUS: `netbox/core/utils.py:41-74`). Job records are queryable via `get_latest_jobs` (FOCUS: `netbox/netbox/models/features.py`) and `get_jobs` (FOCUS: `netbox/extras/models/mixins.py`).

**Lifecycle management**: `delete_expired_jobs` (FOCUS: `netbox/core/jobs.py:143-159`) runs inside `SystemHousekeepingJob`, checking `Config` for the retention period and purging old job records.

**UI and API management**: A full UI exists under `core/background-queues/`, `core/background-tasks/`, and `core/background-workers/` for listing, enqueuing, requeuing, stopping, and deleting tasks (FOCUS: `netbox/core/urls.py`). Serializers `BackgroundTaskSerializer`, `BackgroundQueueSerializer`, and `BackgroundWorkerSerializer` expose queue/task/worker state via the REST API (FOCUS: `netbox/core/api/serializers_/tasks.py`).
