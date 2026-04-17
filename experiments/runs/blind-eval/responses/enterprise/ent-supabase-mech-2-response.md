# Enterprise Eval: ent-supabase-mech-2
Date: 2026-04-17

## Question
How do Supabase Cron jobs execute and interact with other services?

---

## Reasoning Trace
- The relevant evidence is concentrated in the `apps/studio/data/database-cron-jobs/` query modules and the Studio Cron Jobs UI components under `apps/studio/components/interfaces/Integrations/CronJobs/` (`DatabaseCronJobData`, `apps/studio/data/database-cron-jobs/database-cron-jobs-count-query.ts:28-30`; `DatabaseCronJobError`, `apps/studio/data/database-cron-jobs/database-cron-timezone-query.ts:25-26`; `DatabaseCronJobsCountEstimateData`, `apps/studio/data/database-cron-jobs/database-cron-jobs-count-estimate-query.ts:30-32`; `CronJobsTabDataGridProps`, `apps/studio/components/interfaces/Integrations/CronJobs/CronJobsTab.DataGrid.tsx:9-18`; `DeleteCronJob`, `apps/studio/components/interfaces/Integrations/CronJobs/DeleteCronJob.tsx:13-109`).
- The clue shows how Studio queries and manages cron-job metadata, but not the execution engine body.

## Answer
The clue makes Cron jobs look like a **database-native feature surfaced through Studio**, with management and monitoring tied to a specific database connection.

1. **Cron jobs are modeled as database-scoped resources.** The main query hooks live under `apps/studio/data/database-cron-jobs/`, and they all take `projectRef` plus `connectionString`. That shows Studio talks to Cron through a project/database context rather than through a separate standalone scheduler service (`DatabaseCronJobData`, `apps/studio/data/database-cron-jobs/database-cron-jobs-count-query.ts:28-30`; `DatabaseCronJobError`, `apps/studio/data/database-cron-jobs/database-cron-timezone-query.ts:25-26`; `DatabaseCronJobsCountEstimateData`, `apps/studio/data/database-cron-jobs/database-cron-jobs-count-estimate-query.ts:30-32`).

2. **Studio monitors Cron through counts, estimates, and timezone reads.** The visible data hooks are `useCronJobsCountQuery`, `useCronTimezoneQuery`, and `useCronJobsCountEstimateQuery`, so the observable integration is about reading job totals/estimates and scheduler timezone information from the database side (`DatabaseCronJobData`, `apps/studio/data/database-cron-jobs/database-cron-jobs-count-query.ts:28-30`; `DatabaseCronJobError`, `apps/studio/data/database-cron-jobs/database-cron-timezone-query.ts:25-26`; `DatabaseCronJobsCountEstimateData`, `apps/studio/data/database-cron-jobs/database-cron-jobs-count-estimate-query.ts:30-32`).

3. **Cron jobs are managed through a dedicated Studio UI.** The repository includes `CronJobsTab`, header/footer/data-grid props, an empty state, and an e2e helper that navigates to the Cron Jobs page, so Cron is exposed as a first-class integrations surface in Studio (`CronJobsTabDataGridProps`, `apps/studio/components/interfaces/Integrations/CronJobs/CronJobsTab.DataGrid.tsx:9-18`; `CronJobsTabHeaderProps`, `apps/studio/components/interfaces/Integrations/CronJobs/CronJobsTab.Header.tsx:5-14`; `CronJobsFooter`, `apps/studio/components/interfaces/Integrations/CronJobs/CronJobsTab.tsx:191-192`; `CronJobsEmptyState`, `apps/studio/components/interfaces/Integrations/CronJobs/CronJobsEmptyState.tsx:1-14`; `navigateToCronJobsPage`, `e2e/studio/features/cron-jobs.spec.ts:19-22`).

4. **Jobs are individually addressable and deletable by job id.** `DeleteCronJob` guards against a missing job, searches `grid.rows` for a matching `jobid.toString`, and shows `toast.success` on completion. That proves Studio can act on concrete Cron job records coming from the grid/model layer (`DeleteCronJob`, `apps/studio/components/interfaces/Integrations/CronJobs/DeleteCronJob.tsx:13-109`).

## Gaps / Unresolved
The clue does **not** expose the execution body, so I cannot determine from the provided evidence alone:
- what runtime actually fires the jobs,
- whether jobs run SQL, functions, or HTTP calls,
- what external services they invoke,
- or whether the implementation is `pg_cron` with `cron.job` / `cron.job_run_details`.

So the supported conclusion is limited to **database-scoped scheduling/monitoring surfaced in Studio**, not the full execution internals.
