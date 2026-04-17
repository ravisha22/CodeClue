# Enterprise v2: ent-supabase-mech-2
Date: 2026-04-17

## Question
How do Supabase Cron jobs execute and interact with other services?

## Reasoning

### Relevant Clue Entries

**Cron job data layer (FOCUS):** Multiple type aliases and query hooks define the cron job data model:
- `DatabaseCronJobData` at `apps/studio/data/database-cron-jobs/database-cron-jobs-count-query.ts:28-29` is typed as `number`, used by `useCronJobsCountQuery` with parameters `{ projectRef, connectionString }: DatabaseCronJobsCountVariables` (FOCUS: `DatabaseCronJobData`). This reveals cron jobs are counted per project, and the count query requires both a `projectRef` and a `connectionString` to the database.
- `DatabaseCronJobError` appears in two query files: `database-cron-timezone-query.ts:25-26` and `database-cron-jobs-count-query.ts:30` (FOCUS: `DatabaseCronJobError`). Both alias it to `ResponseError`, indicating cron job operations can fail with standard response errors.
- `DatabaseCronJobsVariables` at `database-cron-timezone-query.ts:6-7` is the variable type for cron queries (FOCUS: `DatabaseCronJobsVariables`).

**Cron timezone query (FOCUS):** The `useCronTimezoneQuery` hook (referenced in `DatabaseCronJobError` at `database-cron-timezone-query.ts:25-26`) accepts `{ projectRef, connectionString }` (FOCUS: `DatabaseCronJobError` uses chain). This confirms cron jobs are **timezone-aware** — the system queries and configures a timezone for cron schedule evaluation.

**Cron job count estimation (FOCUS):**
- `DatabaseCronJobsCountEstimateData` at `apps/studio/data/database-cron-jobs/database-cron-jobs-count-estimate-query.ts:30-31` is typed as `Awaited<ReturnType<typeof getCronJobsCountEstimate>>` (FOCUS: `DatabaseCronJobsCountEstimateData`).
- `DatabaseCronJobsCountEstimateError` at the same file (line 32) is typed as `Error` (not `ResponseError`), suggesting the estimate may be computed differently — possibly via a local estimation rather than an API call (FOCUS: `DatabaseCronJobsCountEstimateError`).
- `cronJobsCountEstimateKey` at lines 12-29 takes `projectRef` as a parameter (FOCUS: `cronJobsCountEstimateKey`). The count estimate function and the exact count function coexist, implying that for large numbers of cron jobs, an estimate is used for performance.

**Cron job run variables (GAPS):** The GAPS section lists `DatabaseCronJobRunsVariables` (listed four times) as uncovered (GAPS). This type presumably parameterizes queries for individual cron job run history/execution records, but its structure is not visible in the clue.

**Cron jobs UI components (FOCUS):**
- `CronJobsGridState` at `apps/studio/components/interfaces/Integrations/CronJobs/CronJobsTab.useCronJobsData.ts:23-40` is an interface defining the grid state for displaying cron jobs (FOCUS: `CronJobsGridState`).
- `CronJobsCountState` at the same file (lines 41-46) tracks the count state (FOCUS: `CronJobsCountState`).
- `UseCronJobsDataResult` at the same file (lines 47-57) defines the result shape of the `useCronJobsData` hook (FOCUS: `UseCronJobsDataResult`).
- `CronJobsTabDataGridProps` at `CronJobsTab.DataGrid.tsx:9-18` defines props for the data grid (FOCUS: `CronJobsTabDataGridProps`).
- `CronJobsTabHeaderProps` at `CronJobsTab.Header.tsx:5-14` defines header props (FOCUS: `CronJobsTabHeaderProps`).
- `CronJobsFooter` at `CronJobsTab.tsx:191-192` takes `{ count }: CronJobsFooterProps` (FOCUS: `CronJobsFooter`, `CronJobsFooterProps`).
- `CronJobsEmptyState` at `CronJobsEmptyState.tsx:1-14` takes `{ page }` (FOCUS: `CronJobsEmptyState`).

**Cron jobs in Integrations path:** All cron job UI components reside under `apps/studio/components/interfaces/Integrations/CronJobs/` (FOCUS: all `CronJobs*` components). The **Integrations** directory placement indicates cron jobs are considered an **integration** or extension — not a core database primitive — suggesting they are backed by a Postgres extension (likely `pg_cron`, though the clue does not name it explicitly).

**E2E test navigation (FOCUS):** `navigateToCronJobsPage` at `e2e/studio/features/cron-jobs.spec.ts:19-22` navigates to a cron jobs page via `page.goto` and `page.getByRole` (FOCUS: `navigateToCronJobsPage`). This confirms the cron jobs feature is accessible as a dedicated UI page within Studio.

**Database connection requirement (FOCUS):** Every cron job query takes `connectionString` as a required parameter alongside `projectRef` (FOCUS: `DatabaseCronJobData`, `DatabaseCronJobsVariables`). This indicates cron job operations are **executed against the project's Postgres database** — the Studio UI directly queries the database to manage cron jobs, rather than going through a separate cron service API.

**Docker/config context (FOCUS):** The `docker/.env.example` defines `POSTGRES_PASSWORD` and other database credentials (FOCUS: `docker/.env.example`). Cron jobs would execute within this Postgres environment.

### Synthesis

Based on the clue, Supabase Cron jobs execute and interact with other services as follows:

1. **Database-native execution:** Cron jobs are executed within the project's **Postgres database**. All query hooks (`useCronJobsCountQuery`, `useCronTimezoneQuery`, etc.) require a `connectionString` to the database (FOCUS: `DatabaseCronJobData` at `database-cron-jobs-count-query.ts:28-29`; `DatabaseCronJobsVariables` at `database-cron-timezone-query.ts:6-7`). This means cron jobs are defined and run as database-level scheduled tasks, not as an external service.

2. **Timezone-aware scheduling:** The `useCronTimezoneQuery` hook queries the configured timezone for cron job evaluation (FOCUS: `DatabaseCronJobError` at `database-cron-timezone-query.ts:25-26`). Cron schedules are interpreted relative to this configured timezone.

3. **Integration-tier feature:** Cron jobs are organized under `Integrations/CronJobs/` in the Studio UI (FOCUS: all `CronJobs*` components under `apps/studio/components/interfaces/Integrations/CronJobs/`). This placement suggests they are implemented via a **Postgres extension** that provides in-database cron scheduling capabilities, integrated into Studio as a managed feature.

4. **Project-scoped:** Each cron job operation is scoped by `projectRef` (FOCUS: `DatabaseCronJobData`, `cronJobsCountEstimateKey`). Cron jobs belong to a specific project and execute within that project's database.

5. **Job execution history:** The GAPS section reveals `DatabaseCronJobRunsVariables` as an uncovered type (GAPS), indicating there is a mechanism to query individual cron job run history (execution records), but its structure is not visible in the clue.

6. **Count and estimation:** The system provides both exact counts (`useCronJobsCountQuery` returning `number`) and estimated counts (`getCronJobsCountEstimate`) (FOCUS: `DatabaseCronJobData`, `DatabaseCronJobsCountEstimateData`). The estimate uses a different error type (`Error` vs. `ResponseError`), suggesting it may be computed via a database-level estimation (e.g., `pg_class.reltuples`) rather than a precise count query (FOCUS: `DatabaseCronJobsCountEstimateError`).

7. **Interaction with other services:** Since cron jobs execute as SQL within Postgres, they can interact with other Supabase services through database mechanisms:
   - **Tables/data:** Direct SQL access to all project tables.
   - **Edge Functions:** Potentially callable via `pg_net` or HTTP extensions (not confirmed in clue).
   - **Auth:** Runs under the database's own credentials, not a user session.
   The clue does not provide direct evidence of specific cross-service interactions from cron jobs.

### Gaps and Uncertainties

- **GAPS type is RELATIONAL** with 83 symbols at L3 and 19 with behavior annotations. `DatabaseCronJobRunsVariables` is listed four times as uncovered (GAPS). The run history data model — including what fields are tracked per run (start time, end time, status, error message) — cannot be determined.
- The **underlying Postgres extension** powering cron jobs (presumably `pg_cron`) is not named in the clue. The exact scheduling mechanism (internal Postgres background worker vs. external scheduler) is not visible.
- How cron jobs **interact with Edge Functions, Realtime, or Storage** is not documented in the clue. Whether cron jobs can trigger HTTP calls to other services is not determinable.
- The **SQL content** of cron jobs — what kinds of commands they execute — is not shown.
- Whether cron jobs respect **RLS policies** or run with elevated privileges is not determinable from the available evidence.
- The `useCronJobsData` hook's full implementation (combining grid state, count state, and result) is not visible, only its interface shapes.
