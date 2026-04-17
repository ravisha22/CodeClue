# Enterprise v2: ent-grafana-mech-1
Date: 2026-04-17

## Question
How does Grafana data source management work from setup to querying?

## Reasoning Scaffold

### 1. Relevant Symbols Identification

From **FOCUS** (clue file):

**Setup / Storage layer:**
- **`SqlStore.GetDataSource`** (`pkg/services/datasources/service/store.go:52`) — "adds a datasource to the query model by querying by org_id as well as either uid (preferred), id, or name." Calls `WithDbSession`, `getDataSource`. Called_by `NewIDScopeResolver`, `NewNameScopeResolver`, `ListConnections`.
- **`Service.GetDataSource`** (`pkg/services/datasources/service/datasource.go:188`) — behavior: `DELEGATE(s.retriever.GetDataSource -> result)`. Called_by `NewIDScopeResolver`, `NewNameScopeResolver`, `ListConnections`, `UpdateDataSource`.
- **`DataSourceRetrieverImpl.GetDataSource`** (`pkg/services/datasources/service/datasourceretriever.go:27`) — behavior: `DELEGATE(r.store.GetDataSource -> result)`.
- **`DataSourceRetrieverImpl.GetDataSourceInNamespace`** (`datasourceretriever.go:32`) — gets a data source by namespace, name (uid), and group (type). `DELEGATE(r.store.GetDataSourceInNamespace -> result)`.
- **`HTTPServer.DeleteDataSourceByName`** (`pkg/api/datasources.go:298`) — `DELETE /datasources/name/{name}` endpoint. Guard: `name == "" -> return response.Err...`.
- **`FakeDataSourceService.GetPrunableProvisionedDataSources`** (`fakes/fake_datasource_service.go:71`) — reveals provisioned data sources have a "prunable" concept.
- **`Service.getDataSourceCommands`** (`cloudmigrationimpl/snapshot_mgmt.go:292`) — extracts data source commands for cloud migration; calls `DecryptJsonData`, showing data sources store encrypted JSON data.

**Query layer:**
- **`DataSourceHandler.QueryData`** (PostgreSQL, `sql_engine.go:160`) — `ACCUMULATE(Unmarshal loop -> result)`; calls `Add`, `Error`, `Wait`, `executeQuery`.
- **`DataSourceHandler.QueryData`** (MSSQL, `pkg/tsdb/mssql/sqleng/sql_engine.go:257`) — same ACCUMULATE pattern; calls `Add`, `Errorf`, `Wait`, `executeQuery`.
- **`DataSourceHandler.execQuery`** (`sql_engine.go:201`) — guard: `err != nil -> return nil, backend...`; calls `Release`, `Close`, `ReadAll`.
- **`DataSourceHandler.handleQueryError`** (`sql_engine.go:260`) — calls `isDownstreamError` to classify errors.
- **`DataSourceHandler.TransformQueryError`** (`sql_engine.go:104`) — transforms errors; called_by `CheckHealth`.
- **`getGrafanaDataSourceSettings`** (`pkg/registry/apis/query/client/plugin.go:96`) — "handles the special `--grafana--` data source." Guard: `err != nil -> return nil, err`. Called_by `QueryData`.
- **`DataSource.handleGetEbsVolumeIds`** (`pkg/tsdb/cloudwatch/metric_find_query.go:44`) — CloudWatch-specific; calls `ec2DescribeInstances`, `parseMultiSelectValue`.

**API types:**
- **`DataSourceHandler`** type (`sql_engine.go:83`) — methods: `Dispose`, `Ping`, `QueryData`, `TransformQueryError`, `applyFill`, `execQuery`.
- **`DataSourceInfo`** type (`sql_engine.go:65`).
- **`DataSourceConnectionQuery.DeepCopy`** (`pkg/apis/datasource/v0alpha1/zz_generated.deepcopy.go:185`) — Kubernetes-style API type for data source connections.

From **SOURCE SNIPPETS** (File 2):

- **`SqlStore`** struct (`store.go:40`) — the concrete storage type.
- **`CreateStore`** (`store.go:46`) — `func CreateStore(db db.DB, logger log.Logger) *SqlStore` — factory function.
- **`SqlStore.AddDataSource`** (`store.go:276`) — creates a new data source.
- **`SqlStore.UpdateDataSource`** (`store.go:356`) — updates an existing data source.
- **`SqlStore.DeleteDataSource`** (`store.go:191`) — deletes a data source.
- **`SqlStore.GetDataSources`** (`store.go:131`) — lists data sources.
- **`SqlStore.GetAllDataSources`** (`store.go:147`) — lists all data sources.
- **`SqlStore.GetDataSourcesByType`** (`store.go:156`) — lists by type.
- **`SqlStore.GetDataSourceInNamespace`** (`store.go:96`) — namespace-scoped retrieval.
- **`SqlStore.GetPrunableProvisionedDataSources`** (`store.go:180`) — retrieves prunable provisioned sources.
- **`SqlStore.Count`** (`store.go:232`) — quota counting.
- **`SqlStore.getDataSource`** (`store.go:65`) — internal retrieval with session.
- **`SqlStore.getDataSourceInGroup`** (`store.go:112`) — retrieval by org, name, and group.
- **`updateIsDefaultFlag`** (`store.go:345`) — manages the "is default" flag.
- **`logDeprecatedInvalidDsUid`** (`store.go:465`) — logs deprecation warnings for invalid UIDs.
- **`generateNewDatasourceUid`** (`migrations/external_alertmanagers.go:112`) — generates UIDs for data sources during migration.
- **`pluginClient`** struct (`plugin.go:30`) — wraps plugin interaction for querying.
- **`newQueryClientForPluginClient`** (`plugin.go:67`) — creates a query client from a plugin client, taking `accessControl` parameter.
- **`pluginClient.CanQueryDataSource`** (`plugin.go:84`) — checks if a data source can be queried.
- **`pluginClient.QueryData`** (`plugin.go:112`) — executes query through plugin client.
- **`pluginRegistry`** struct (`plugin.go:36`).
- **`pluginRegistry.GetDatasourceGroupVersion`** (`plugin.go:165`) — resolves a plugin ID to a K8s-style GroupVersion.
- **`pluginRegistry.GetDatasourceApiServers`** (`plugin.go:185`) — returns `DataSourceApiServerList`.
- **`pluginRegistry.updatePlugins`** (`plugin.go:200`) — refreshes plugin registry.

### 2. Tracing the Flow: Setup → Storage → Query

**Phase 1: Data Source Creation (Setup)**

1. **Store creation**: `CreateStore(db, logger)` (`store.go:46`) creates the `SqlStore` instance backed by a database.
2. **Adding a data source**: `SqlStore.AddDataSource(ctx, cmd)` (`store.go:276`) persists a new data source. The `AddDataSourceCommand` (implied by signature) carries the configuration.
3. **UID generation**: `generateNewDatasourceUid(sess, orgId)` (`external_alertmanagers.go:112`) generates unique identifiers for data sources, confirming UIDs are org-scoped.
4. **Default flag management**: `updateIsDefaultFlag(ds, sess)` (`store.go:345`) manages which data source is the default, called during add/update operations.
5. **UID validation**: `logDeprecatedInvalidDsUid(logger, uid, name, action, err)` (`store.go:465`) logs deprecation warnings for invalid UIDs, indicating a migration away from legacy identifiers.

**Phase 2: Data Source Retrieval and Management**

The retrieval layer has a **three-tier delegation chain**:

1. **Service layer**: `Service.GetDataSource` (`datasource.go:188`) → delegates to `s.retriever.GetDataSource`.
2. **Retriever layer**: `DataSourceRetrieverImpl.GetDataSource` (`datasourceretriever.go:27`) → delegates to `r.store.GetDataSource`.
3. **Store layer**: `SqlStore.GetDataSource` (`store.go:52`) → calls `WithDbSession` then `getDataSource` (internal, `store.go:65`), which queries by org_id + uid/id/name.

Additional retrieval methods at the store level:
- `GetDataSources` (`store.go:131`) — filtered list.
- `GetAllDataSources` (`store.go:147`) — unfiltered.
- `GetDataSourcesByType` (`store.go:156`) — type-filtered.
- `GetDataSourceInNamespace` (`store.go:96`) — K8s namespace-scoped.
- `GetPrunableProvisionedDataSources` (`store.go:180`) — for provisioning cleanup.
- `Count` (`store.go:232`) — quota enforcement.

**CRUD operations**: `AddDataSource` (`store.go:276`), `UpdateDataSource` (`store.go:356`), `DeleteDataSource` (`store.go:191`). The HTTP layer exposes `DELETE /datasources/name/{name}` via `HTTPServer.DeleteDataSourceByName` (`datasources.go:298`).

**Encrypted data**: `Service.getDataSourceCommands` (`snapshot_mgmt.go:292`) calls `DecryptJsonData`, confirming data sources store sensitive configuration (credentials) as encrypted JSON.

**Phase 3: Query Execution**

1. **Access control check**: `pluginClient.CanQueryDataSource(ctx, uid)` (`plugin.go:84`) verifies the caller can query a specific data source. The `newQueryClientForPluginClient` (`plugin.go:67`) takes an `accessControl` parameter, wiring access control into the query path.

2. **Plugin resolution**: `pluginRegistry.GetDatasourceGroupVersion(pluginId)` (`plugin.go:165`) maps a plugin ID to a K8s GroupVersion. `pluginRegistry.GetDatasourceApiServers(ctx)` (`plugin.go:185`) lists available data source API servers. `pluginRegistry.updatePlugins()` (`plugin.go:200`) refreshes the registry.

3. **Special data source handling**: `getGrafanaDataSourceSettings(ctx)` (`plugin.go:96`) handles the built-in `--grafana--` data source, called_by `QueryData`.

4. **Query dispatch**: `pluginClient.QueryData(ctx, req)` (`plugin.go:112`) routes queries through the plugin client to the appropriate data source backend.

5. **SQL engine execution** (for SQL-based sources):
   - `DataSourceHandler.QueryData` (`sql_engine.go:160`) unmarshals each query from the request (`ACCUMULATE(Unmarshal loop)`), uses `Add`/`Wait` for concurrent execution, and calls `executeQuery` for each.
   - `DataSourceHandler.execQuery` (`sql_engine.go:201`) performs the actual database query, managing connection lifecycle (`Release`, `Close`, `ReadAll`).
   - Errors are classified by `handleQueryError` (`sql_engine.go:260`) using `isDownstreamError` to distinguish data-source-side errors from Grafana-side errors.
   - `TransformQueryError` (`sql_engine.go:104`) is also used by `CheckHealth`, connecting the health-check path to the same error-handling logic.

6. **Provider-specific queries**: CloudWatch's `DataSource.handleGetEbsVolumeIds` (`metric_find_query.go:44`) shows provider-specific query methods that call cloud APIs (`ec2DescribeInstances`).

### 3. GAPS — What Cannot Be Determined

The GAPS section lists as **uncovered**:
- **`AddDataSourceParams`** — the full parameter set for adding a data source is not detailed.
- **`BaseDataSourceService`** — a base service type is not visible.
- **`DashboardCompatibilityScoreDataSourceMapping`** and **`DashboardCompatibilityScoreDataSourceResult`** — how data sources relate to dashboard compatibility scoring is not determinable.

The **drill** targets confirm the clue identified `getGrafanaDataSourceSettings` (`plugin.go:96`) and `SqlStore.GetDataSource` (`store.go:52`) as needing deeper analysis, and the source snippets partially satisfy this.

Additionally:
- The **data source proxy** mechanism (how Grafana proxies HTTP requests to external data sources) is not visible.
- The **caching layer** (if any) between retrieval and query execution is not evidenced.
- The **provisioning pipeline** for data sources (file-based provisioning on startup) is only hinted at by `GetPrunableProvisionedDataSources` but not fully traced.

### 4. Synthesis

Grafana data source management follows a **three-phase lifecycle**:

**Setup**: Data sources are created via `SqlStore.AddDataSource` (`store.go:276`) with auto-generated UIDs (`generateNewDatasourceUid`, `external_alertmanagers.go:112`), a default-flag mechanism (`updateIsDefaultFlag`, `store.go:345`), and encrypted JSON data storage (evidenced by `DecryptJsonData` in `snapshot_mgmt.go:292`). The `CreateStore` factory (`store.go:46`) initializes the persistence layer.

**Management**: A three-tier delegation chain — `Service` → `DataSourceRetrieverImpl` → `SqlStore` (`datasource.go:188` → `datasourceretriever.go:27` → `store.go:52`) — provides data source retrieval by uid/id/name within an org scope. Full CRUD is supported (`AddDataSource`, `UpdateDataSource`, `DeleteDataSource` at `store.go:276`/`356`/`191`), with namespace-aware retrieval (`GetDataSourceInNamespace`, `store.go:96`) for K8s-style API integration. Quota enforcement uses `Count` (`store.go:232`).

**Querying**: Query execution begins with access control verification (`pluginClient.CanQueryDataSource`, `plugin.go:84`), proceeds through plugin resolution (`pluginRegistry.GetDatasourceGroupVersion`, `plugin.go:165`), handles the special `--grafana--` built-in source (`getGrafanaDataSourceSettings`, `plugin.go:96`), and dispatches via `pluginClient.QueryData` (`plugin.go:112`). For SQL sources, `DataSourceHandler.QueryData` (`sql_engine.go:160`) provides concurrent query execution with fan-out (`Add`/`Wait`) and error classification (`isDownstreamError` at `sql_engine.go:260`). The `DataSourceHandler` type (`sql_engine.go:83`) encapsulates the full SQL query lifecycle: `Ping`, `QueryData`, `execQuery`, `TransformQueryError`, `Dispose`.

**Unresolved**: The full `AddDataSourceParams` structure, the data source proxy mechanism, the dashboard compatibility scoring relationship, and any caching layer remain undetermined from the evidence (GAPS).
