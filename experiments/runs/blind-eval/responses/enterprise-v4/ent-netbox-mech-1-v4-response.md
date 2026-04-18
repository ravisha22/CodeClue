# Enterprise v4 (full-stack): ent-netbox-mech-1
Date: 2026-04-18

## Answer
The deep workflow context plus job clues show that NetBox pushes asynchronous work through its Redis/RQ job system. The documented background workload includes custom scripts, remote data source synchronization, and housekeeping tasks, and plugins can participate by defining their own jobs through the Job model. Execution happens in `rqworker` processes, not in the request thread. Scheduling is flexible: jobs may run immediately, be delayed to a future time, or repeat on an interval, while `enqueue_once()` is the guard that suppresses duplicate instance-bound jobs. The platform also distinguishes system-owned jobs via `system_job()`, and the standard worker queues are `high`, `default`, and `low`; any custom queue needs its own worker configuration.

## Synthesis
Operationally, NetBox uses RQ as the durable execution layer that turns model- and plugin-level jobs into queued, prioritized worker activity.
