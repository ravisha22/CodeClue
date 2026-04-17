# Enterprise v2: ent-grafana-mech-2
Date: 2026-04-17

## Question
How does alerting resource provisioning work in Grafana?

## Reasoning Scaffold

### 1. Relevant Symbols Identification

From **FOCUS** (clue file):

**Core provisioning entry:**
- **`ProvisioningServiceImpl.ProvisionAlerting`** (`pkg/services/provisioning/provisioning.go:310`) — behavior: `DELEGATE(ps.provisionAlerting -> result)`; called_by `starting`.
- **`ProvisioningServiceMock.ProvisionAlerting`** (`provisioning_mock.go:65`) — mock version; also called_by `starting`.

**Alerting configuration API:**
- **`AlertmanagerApiHandler.RouteGetGrafanaAlertingConfig`** (`generated_base_api_alertmanager.go:112`) — `DELEGATE(f.handleRouteGetGrafanaAlertingConfig -> result)`.
- **`AlertmanagerApiHandler.handleRouteGetGrafanaAlertingConfig`** (`forking_alertmanager.go:152`) — `DELEGATE(f.GrafanaSvc.RouteGetAlertingConfig -> result)`.
- **`AlertmanagerApiHandler.RouteGetGrafanaAlertingConfigHistory`** (`generated_base_api_alertmanager.go:115`) — `DELEGATE(f.handleRouteGetGrafanaAlertingConfigHistory -> result)`.
- **`AlertmanagerApiHandler.handleRouteGetGrafanaAlertingConfigHistory`** (`forking_alertmanager.go:156`) — `DELEGATE(f.GrafanaSvc.RouteGetAlertingConfigHistory -> result)`.
- **`AlertmanagerApiHandler.RoutePostGrafanaAlertingConfigHistoryActivate`** (`generated_base_api_alertmanager.go:160`) — `DELEGATE(f.handleRoutePostGrafanaAlertingConfigHistoryActivate -> result)`.
- **`AlertmanagerApiHandler.handleRoutePostGrafanaAlertingConfigHistoryActivate`** (`forking_alertmanager.go:160`) — `DELEGATE(f.GrafanaSvc.RoutePostGrafanaAlertingConfigHistoryActivate -> result)`.
- **`AlertmanagerSrv.RoutePostGrafanaAlertingConfigHistoryActivate`** (`api_alertmanager.go:147`) — guard: `err != nil -> return ErrResp(http...`; calls `Error`, `GetOrgID`, `Context`, `ActivateHistoricalConfiguration`.

**Admin reload endpoint:**
- **`HTTPServer.AdminProvisioningReloadAlerting`** (`pkg/api/admin_provisioning.go:81`) — guard: `err != nil -> return response.Err...`; calls `Context`.

**Resource versioning (supporting):**
- **`grafanaMetaAccessor.GetResourceVersion`** (`pkg/apimachinery/utils/meta.go:393`) — `DELEGATE(m.obj.GetResourceVersion -> result)`; called_by `ConvertToTable`, `GetResourceVersionInt64`, `Update`, `prepareObjectForStorage`, etc.

**Swagger params:**
- **`RouteGetGrafanaAlertingConfigHistoryParams`** (`pkg/services/ngalert/api/tooling/definitions/alertmanager.go:320`) — swagger parameter definition.

From **SOURCE SNIPPETS** (File 2):

- **`ProvisioningServiceImpl`** struct (`provisioning.go:216`).
- **`ProvisioningService`** interface (`provisioning.go:180`).
- **`ProvisioningServiceImpl.ProvisionAlerting`** (`provisioning.go:310`) — `func (ps *ProvisioningServiceImpl) ProvisionAlerting(ctx context.Context) error`.
- **`ProvisioningServiceImpl.ProvisionDatasources`** (`provisioning.go:265`).
- **`ProvisioningServiceImpl.ProvisionDashboards`** (`provisioning.go:289`).
- **`ProvisioningServiceImpl.ProvisionPlugins`** (`provisioning.go:277`).
- **`ProvisioningServiceImpl.Run`** (`provisioning.go:257`).
- **`ProvisioningServiceImpl.RunInitProvisioners`** (`provisioning.go:250`).
- **`ProvisioningServiceImpl.starting`** (`provisioning.go:112`).
- **`ProvisioningServiceImpl.running`** (`provisioning.go:147`).
- **`ProvisioningServiceImpl.cancelPolling`** (`provisioning.go:384`).
- **`ProvisioningServiceImpl.setDashboardProvisioner`** (`provisioning.go:170`).
- **`ProvisioningServiceImpl.GetAllowUIUpdatesFromConfig`** (`provisioning.go:380`).
- **`ProvisioningServiceImpl.GetDashboardProvisionerResolvedPath`** (`provisioning.go:376`).

### 2. Tracing the Provisioning Flow

**Phase 1: Startup Lifecycle**

The provisioning lifecycle follows a clear startup sequence:

1. **`ProvisioningServiceImpl.starting`** (`provisioning.go:112`) is the entry point during Grafana startup. It is the **caller of `ProvisionAlerting`** (clue: `called_by: starting` on both `ProvisionAlerting` and `ProvisioningServiceMock.ProvisionAlerting`).

2. From the source snippets, the startup method ordering is visible:
   - `starting` (`provisioning.go:112`) — initial startup.
   - `RunInitProvisioners` (`provisioning.go:250`) — runs initial provisioners.
   - `Run` (`provisioning.go:257`) — main run loop.
   - `running` (`provisioning.go:147`) — ongoing runtime state.

3. **`ProvisionAlerting`** (`provisioning.go:310`) is one of **four provisioning methods** called during startup, alongside:
   - `ProvisionDatasources` (`provisioning.go:265`)
   - `ProvisionPlugins` (`provisioning.go:277`)
   - `ProvisionDashboards` (`provisioning.go:289`)

   The line numbers suggest an ordering: Datasources (L265) → Plugins (L277) → Dashboards (L289) → Alerting (L310), which is logically consistent — alerting depends on data sources and dashboards being provisioned first.

**Phase 2: Alerting Provisioning Execution**

- `ProvisioningServiceImpl.ProvisionAlerting` (`provisioning.go:310`) has behavior `DELEGATE(ps.provisionAlerting -> result)`, meaning it delegates to an internal `provisionAlerting` method (lowercase, unexported). The source snippet confirms the signature: `func (ps *ProvisioningServiceImpl) ProvisionAlerting(ctx context.Context) error`.

- The delegation pattern is consistent with the other provisioning methods visible in the source snippets, suggesting a uniform provisioning architecture where each `Provision*` method delegates to an internal implementation that reads configuration files and applies them.

**Phase 3: Admin Reload**

- **`HTTPServer.AdminProvisioningReloadAlerting`** (`admin_provisioning.go:81`) provides an HTTP endpoint for re-provisioning alerting at runtime. The guard `err != nil -> return response.Err...` shows it returns an error response on failure, and it calls `Context`, indicating it operates within the request context. This allows administrators to reload alerting provisioning without restarting Grafana.

**Phase 4: Alerting Configuration API**

The alerting configuration is exposed through a multi-layer API delegation chain:

1. **Generated route handler** → **Forking handler** → **Grafana service**:
   - `RouteGetGrafanaAlertingConfig` (`generated_base_api_alertmanager.go:112`) → `handleRouteGetGrafanaAlertingConfig` (`forking_alertmanager.go:152`) → `f.GrafanaSvc.RouteGetAlertingConfig`.
   - `RouteGetGrafanaAlertingConfigHistory` (`generated_base_api_alertmanager.go:115`) → `handleRouteGetGrafanaAlertingConfigHistory` (`forking_alertmanager.go:156`) → `f.GrafanaSvc.RouteGetAlertingConfigHistory`.
   - `RoutePostGrafanaAlertingConfigHistoryActivate` (`generated_base_api_alertmanager.go:160`) → `handleRoutePostGrafanaAlertingConfigHistoryActivate` (`forking_alertmanager.go:160`) → `f.GrafanaSvc.RoutePostGrafanaAlertingConfigHistoryActivate`.

2. The **config history activation** endpoint has the deepest visible implementation: `AlertmanagerSrv.RoutePostGrafanaAlertingConfigHistoryActivate` (`api_alertmanager.go:147`) calls `ActivateHistoricalConfiguration` (scoped to `GetOrgID`), showing that:
   - Alerting configurations are **versioned** (historical configurations exist).
   - Configurations are **org-scoped** (uses `GetOrgID`).
   - Previous configurations can be **re-activated** (rolled back to).

**Phase 5: UI Updates and Polling**

- `ProvisioningServiceImpl.GetAllowUIUpdatesFromConfig(name)` (`provisioning.go:380`) returns a boolean indicating whether UI updates are allowed for a named provisioner. This suggests provisioned alerting resources can be **locked from UI modification** when provisioning is active.
- `ProvisioningServiceImpl.cancelPolling` (`provisioning.go:384`) stops polling, indicating provisioning supports a **polling mode** for detecting configuration changes at runtime.

### 3. GAPS — What Cannot Be Determined

The GAPS section lists as **uncovered**:
- **`ResourceUnmanagedConflictError.Error`** — how conflicts between provisioned and manually-created resources are handled is not visible.
- **`JobResourceResult.Error`** — job-based resource processing errors are not covered.
- **`retryResourceInterface.Get`** — retry logic for resource retrieval is not determinable.
- **`ConnectionController.processNextWorkItem`** — controller-based work-item processing is not visible.

The **drill** target was `ProvisioningServiceImpl.ProvisionAlerting` (`provisioning.go:310`, ~1 line), and the source snippet confirms it is a single-line delegation to `ps.provisionAlerting`. The body of `provisionAlerting` (lowercase) is **not provided**, so the exact mechanism of reading alerting configuration files and applying them is not determinable.

Additionally:
- The **file format** for alerting provisioning configurations (YAML structure, supported fields) is not evidenced.
- The **reconciliation logic** (how provisioned state is compared against current state) is not visible.
- The **error recovery** behavior during provisioning failures (partial application, rollback) is not determinable.

### 4. Synthesis

Alerting resource provisioning in Grafana follows a **lifecycle-integrated, delegation-based architecture**:

**Startup**: The `ProvisioningServiceImpl.starting` method (`provisioning.go:112`) orchestrates all provisioning during Grafana startup. Alerting provisioning (`ProvisionAlerting`, `provisioning.go:310`) is invoked as the **fourth and final provisioning phase**, after datasources (L265), plugins (L277), and dashboards (L289) — ensuring alerting dependencies are satisfied first.

**Execution**: `ProvisionAlerting` delegates to an internal `provisionAlerting` method (`DELEGATE(ps.provisionAlerting -> result)`, `provisioning.go:310`). The exact body is not provided (GAPS drill), but the pattern is consistent with the other `Provision*` methods.

**Runtime Reload**: Administrators can trigger re-provisioning without restart via `HTTPServer.AdminProvisioningReloadAlerting` (`admin_provisioning.go:81`). A polling mechanism (`cancelPolling`, `provisioning.go:384`) supports continuous configuration change detection.

**Configuration Management**: Alerting configurations are **versioned and org-scoped** (`AlertmanagerSrv.RoutePostGrafanaAlertingConfigHistoryActivate`, `api_alertmanager.go:147`, which calls `ActivateHistoricalConfiguration` with `GetOrgID`). The API supports reading current config, viewing config history, and activating historical versions (rollback) through a three-layer delegation chain: generated handler → forking handler → Grafana alertmanager service.

**UI Control**: `GetAllowUIUpdatesFromConfig` (`provisioning.go:380`) gates whether provisioned alerting resources can be modified through the UI, preventing manual drift from provisioned state.

**Unified Provisioning Interface**: `ProvisioningService` interface (`provisioning.go:180`) defines the contract, with `ProvisioningServiceImpl` (`provisioning.go:216`) as the concrete implementation and `ProvisioningServiceMock` (`provisioning_mock.go:65`) for testing.

**Unresolved**: The internal `provisionAlerting` body, the provisioning file format, conflict resolution for unmanaged resources (`ResourceUnmanagedConflictError`, GAPS), retry logic (`retryResourceInterface.Get`, GAPS), and the reconciliation mechanism remain undetermined from the evidence.
