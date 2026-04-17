# Enterprise v2: ent-grafana-rel-2
Date: 2026-04-17

## Question
How do data sources connect Grafana's query, visualization, and alerting workflows?

## Reasoning Scaffold

### 1. Relevant Symbols Identification

From **FOCUS**, the data-source-centric entries are:

**Query workflow:**
- **`DataSourceHandler.QueryData`** (`pkg/tsdb/grafana-postgresql-datasource/sqleng/sql_engine.go:160`) — behavior: `ACCUMULATE(Unmarshal loop -> result)`; calls `Add`, `Error`, `Wait`, `executeQuery`; called_by `QueryData`, `executeConcurrentQueries`, `healthcheck`.
- **`Datasource.QueryData`** (Pyroscope, `pkg/tsdb/grafana-pyroscope-datasource/standalone/datasource.go:29`) — behavior: `DELEGATE(d.Service.QueryData -> result)`.
- **`Datasource.QueryData`** (Testdata, `pkg/tsdb/grafana-testdata-datasource/standalone/datasource.go:27`) — behavior: `DELEGATE(d.Service.QueryData -> result)`.
- **`HostedGrafanaACHeaderMiddleware.QueryData`** (`pkg/services/pluginsintegration/clientmiddleware/grafana_request_id_header_middleware.go:118`) — guard: `req == nil -> return m.BaseHandle...`; calls `applyGrafanaRequestIDHeader`.
- **`UseAlertHeadersMiddleware.QueryData`** (`pkg/services/pluginsintegration/clientmiddleware/usealertingheaders_middleware.go:55`) — behavior: `DELEGATE(m.BaseHandler.QueryData -> result)`; calls `applyAlertHeaders`.
- **`DataSourceHandler.execQuery`** (`sql_engine.go:201`) — the actual query execution; calls `Release`, `Close`, `ReadAll`.
- **`DataSourceHandler.handleQueryError`** (`sql_engine.go:260`) — error handling; calls `isDownstreamError`.
- **`DataSourceHandler.TransformQueryError`** (`sql_engine.go:104`) — transforms errors; called_by `CheckHealth`.

**Data source model types:**
- **`GetDataSourcesQuery`** (`pkg/services/datasources/models.go:250`) — query model for listing data sources.
- **`GetDataSourcesByTypeQuery`** (`models.go:257`) — query model filtered by type.
- **`GetAllDataSourcesQuery`** (`models.go:255`) — query model for all data sources.
- **`FakeDataSourceService.GetDataSources`** (`fakes/fake_datasource_service.go:56`) — called_by `ListConnections`.
- **`FakeDataSourceService.GetDataSourcesByType`** (`fakes/fake_datasource_service.go:81`) — called_by `ListConnections`.

**Visualization/transformation:**
- **`DashboardDataTransformerConfig`** (`apps/dashboard/pkg/apis/dashboard/v2beta1/dashboard_spec_gen.go:325`) — "Transformations allow to manipulate data returned by a query before the system applies a visualization."
- **`DashboardDataTransformerConfig`** (`v2alpha1/dashboard_spec_gen.go:328`) — same type in alpha version.
- **`DataTransformerConfig`** (`pkg/kinds/dashboard/dashboard_spec_gen.go:341`) — same concept in legacy kinds.
- **`AnnotationQuery`** (`dashboard_spec_gen.go:1016`) — "TODO docs FROM: AnnotationQuery in grafana-data/src/types/annotations.ts."

**Alerting integration:**
- **`RuleService.getRulesQueryEvaluator`** (`pkg/services/ngalert/accesscontrol/rules.go:63`) — "constructs accesscontrol.Evaluator that checks all permissions to query data sources used by the rule." Called_by: `AuthorizeDatasourceAccessForRule`, `AuthorizeDatasourceAccessForRuleGroup`, `AuthorizeRuleChanges`.
- **`LogsDataSourceQuery`** (`apps/alerting/alertenrichment/pkg/apis/alertenrichment/v1beta1/types.go:257`) — "simplified method of describing a logs query, typically those that return data frames with a 'L' [logs] format."
- **`RawDataSourceQuery`** (`alertenrichment/v1beta1/types.go:243`) — "allows defining the entire query request."
- **`schema_pkg_apis_alertenrichment_v1beta1_RawDataSourceQuery`** (`zz_generated.openapi.go:679`) — OpenAPI schema for the raw data source query.

**Pyroscope-specific:**
- **`GrafanaPyroscopeDataQuery`** (`pkg/tsdb/grafana-pyroscope-datasource/kinds/dataquery/types_dataquery_gen.go:29`).
- **`NewGrafanaPyroscopeDataQuery`** (`types_dataquery_gen.go:69`) — factory function.

### 2. Tracing the Data Flow

**Step 1: Data Source → Query Execution**

The `QueryData` method is the universal entry point across data sources. Multiple implementations exist:
- `DataSourceHandler.QueryData` (`sql_engine.go:160`) for SQL-based sources uses an `ACCUMULATE(Unmarshal loop)` pattern — it unmarshals each query from the request, fans out execution via `Add`/`Wait` (concurrent execution), and calls `executeQuery` for each.
- Standalone data sources (Pyroscope at `datasource.go:29`, Testdata at `datasource.go:27`) use `DELEGATE(d.Service.QueryData -> result)`, wrapping an inner service.
- All are called_by the same callers: `QueryData`, `executeConcurrentQueries`, `healthcheck` — showing a shared calling convention.

**Step 2: Middleware Chain**

Before reaching the data source handler, queries pass through middleware:
- `HostedGrafanaACHeaderMiddleware.QueryData` (`grafana_request_id_header_middleware.go:118`) applies a Grafana request ID header (guard: `req == nil -> return m.BaseHandle...`), adding traceability.
- `UseAlertHeadersMiddleware.QueryData` (`usealertingheaders_middleware.go:55`) applies alert-specific headers via `applyAlertHeaders` before delegating to `m.BaseHandler.QueryData`. This middleware is the **bridge between alerting and query workflows** — it annotates query requests with alerting context.

Both middlewares share the same `called_by` set (`QueryData`, `executeConcurrentQueries`, `healthcheck`), confirming they sit in the same middleware chain.

**Step 3: Query Results → Visualization**

Query results flow into the visualization layer through transformations:
- `DashboardDataTransformerConfig` (`dashboard_spec_gen.go:325` in v2beta1, `dashboard_spec_gen.go:328` in v2alpha1) — "Transformations allow to manipulate data returned by a query before the system applies a visualization." This is defined in the dashboard spec, showing it is a **dashboard-level configuration** that sits between query results and visual rendering.
- `DataTransformerConfig` (`dashboard_spec_gen.go:341`) in the legacy kinds package provides the same role.
- `AnnotationQuery` (`dashboard_spec_gen.go:1016`) links annotation queries to the dashboard visualization layer.

**Step 4: Query Results → Alerting**

Data sources connect to alerting through two mechanisms:

1. **Access control**: `RuleService.getRulesQueryEvaluator` (`rules.go:63`) constructs an evaluator that checks permissions to query the data sources used by alert rules. It is called by `AuthorizeDatasourceAccessForRule`, `AuthorizeDatasourceAccessForRuleGroup`, and `AuthorizeRuleChanges` — showing that every alert rule change or evaluation requires validating the user's permission to query the referenced data sources.

2. **Alert enrichment queries**: `LogsDataSourceQuery` (`types.go:257`) and `RawDataSourceQuery` (`types.go:243`) in the `alertenrichment/v1beta1` API define specialized query types for alert enrichment — simplified logs queries and full raw queries, respectively. These are Kubernetes-style API resources (evidenced by `DeepCopy` methods in `zz_generated.deepcopy.go`).

### 3. GAPS — What Cannot Be Determined

The GAPS section lists as **uncovered**:
- **`schema_pkg_apis_datasource_v0alpha1_DataSourceConnectionQuery`** — the K8s-style data source connection query schema is not visible, so the full API-server query path is not determinable.
- **`ClientV2.QueryData`** and **`ClientV2.QueryChunkedData`** — a v2 client interface for querying (possibly supporting streaming/chunked responses) is not covered.
- **`CloudWatchQuery.GetGetMetricDataAPIMode`** — CloudWatch-specific query modes are not determinable.

Additionally:
- The exact **data frame format** that connects query results to visualization panels is not detailed.
- How **alert rule evaluation schedules** trigger `QueryData` calls is not traceable from the clue.
- The full set of data source types beyond PostgreSQL, Pyroscope, Testdata, and CloudWatch is not enumerable.

### 4. Synthesis

Data sources serve as the **connective tissue** between Grafana's three primary workflows:

**Query Workflow**: Data sources implement `QueryData` (e.g., `DataSourceHandler.QueryData` at `sql_engine.go:160` for SQL sources, standalone delegates at `datasource.go:27`/`29`). Queries pass through a middleware chain including `HostedGrafanaACHeaderMiddleware.QueryData` (`grafana_request_id_header_middleware.go:118`) for request tracing and `UseAlertHeadersMiddleware.QueryData` (`usealertingheaders_middleware.go:55`) for alerting context injection. SQL data sources fan out queries concurrently (`ACCUMULATE` + `Add`/`Wait` pattern) and execute them via `execQuery` (`sql_engine.go:201`).

**Visualization Workflow**: Query results feed into the dashboard layer through `DashboardDataTransformerConfig` (`dashboard_spec_gen.go:325`), which transforms data "returned by a query before the system applies a visualization." This configuration lives in the dashboard spec at both v2alpha1 and v2beta1 API versions, as well as the legacy `DataTransformerConfig` (`dashboard_spec_gen.go:341`). `AnnotationQuery` (`dashboard_spec_gen.go:1016`) provides a parallel query path for annotation overlays on visualizations.

**Alerting Workflow**: Data sources connect to alerting through (a) access control validation — `RuleService.getRulesQueryEvaluator` (`rules.go:63`) ensures users have permission to query the data sources referenced by alert rules, gating `AuthorizeDatasourceAccessForRule`, `AuthorizeDatasourceAccessForRuleGroup`, and `AuthorizeRuleChanges`; and (b) alert enrichment query types — `LogsDataSourceQuery` (`types.go:257`) and `RawDataSourceQuery` (`types.go:243`) define structured query formats for alerting data retrieval. The `UseAlertHeadersMiddleware` (`usealertingheaders_middleware.go:55`) bridges the query and alerting paths by injecting alert-specific headers into standard `QueryData` calls.

**Unresolved**: The v2 client query interface (`ClientV2.QueryData`, `ClientV2.QueryChunkedData`), the K8s-style data source connection query schema, and the alert evaluation scheduling mechanism remain undetermined from the clue (GAPS).
