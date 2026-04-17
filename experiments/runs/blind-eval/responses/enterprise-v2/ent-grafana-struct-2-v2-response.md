# Enterprise v2: ent-grafana-struct-2
Date: 2026-04-17

## Question
What plugin surfaces and security controls does Grafana expose?

## Reasoning Scaffold

### 1. Relevant Symbols Identification

From **FOCUS**, the plugin-specific entries are:

- **`installPlugin`** (`pkg/cmd/grafana-cli/commands/install_command.go:108`) — downloads plugin code as a zip from the Grafana.com API and extracts it; delegates to `doInstallPlugin`.
- **`doInstallPlugin`** (`pkg/cmd/grafana-cli/commands/install_command.go:114`) — recursive function that installs a plugin and its dependencies. Behavior: `GUARD(installing[pluginID] -> return nil)` prevents re-entrant installation loops.
- **`corePlugin`** (`pkg/plugins/backendplugin/coreplugin/core_plugin.go:15`) — represents a plugin that's part of Grafana core; methods: `CallResource`, `CheckHealth`, `CollectMetrics`, `ConvertObjects`, `Decommission`, `Exited`.
- **`GrafanaLive.getStreamPlugin`** (`pkg/services/live/live.go:497`) — resolves a stream plugin by ID; behavior: `GUARD(!exists -> return nil, fmt.Err...)`.
- **`GrafanaLive.handlePluginScope`** (`pkg/services/live/live.go:989`) — handles plugin-scoped live channels; called_by `GetChannelHandlerFactory`.
- **`Manager.grafanaCompatiblePluginVersions`** (`pkg/plugins/repo/service.go:110`) — fetches compatible plugin versions from `/api/plugins/$pluginID/versions`.
- **`Manager.PluginVersion`** (`pkg/plugins/repo/service.go:84`) — returns plugin version data; calls `grafanaCompatiblePluginVersions`.
- **`AccessControlStore.CleanupPluginRBAC`** (`pkg/services/accesscontrol/database/cleanup.go:17`) — removes all RBAC data associated with given plugin IDs (permissions, roles with plugin-prefixed actions).
- **`GrafanaPluginId`** (`pkg/semconv/attributes.go:139`) — returns an attribute KeyValue for `"grafana.plugin.id"` semantic conventions (telemetry).
- **`DBstore.filterByPluginOrigin`** (`pkg/services/ngalert/store/alert_rule.go:1685`) — filters alert rules by plugin origin using the `__grafana_origin` label.
- **`grafanaComPluginManifest`** (`apps/plugins/pkg/app/meta/converter.go:741`) — type representing a plugin manifest from grafana.com.
- **`grafanaComPluginVersionMetaToMetaSpec`** (`apps/plugins/pkg/app/meta/converter.go:779`) — converts grafana.com version metadata to internal spec; calls `calculateLoadingStrategyFromGcomMeta`, `translationsFromManifest`.
- **`ContextCommandLine.PluginDirectory`** (`pkg/cmd/grafana-cli/utils/command_line.go:57`) — resolves the plugin directory path; called by install/uninstall/list/upgrade commands.
- **`GetGrafanaPluginDir`** (`pkg/cmd/grafana-cli/utils/grafana_path.go:11`) — determines the plugin directory, with a dev-environment guard.

From **SYM/INDEX**:

- **`pkg/plugins/repo/models.go:37`** — `PluginInfo` type: subset of JSON from `grafana.com/api/plugins/$pluginID`.
- **`pkg/cmd/grafana-cli/models/model.go`** — types: `InstalledPlugin`, `Plugin`, `PluginInfo`, `PluginRepo`.
- **`CatalogPluginSpec`** (`pkg/build/daggerbuild/arguments/catalog_plugins.go:16`) — defines a plugin to download from the Grafana catalog.
- **`BuildPluginDownloadURL`** (`pkg/build/daggerbuild/plugins/downloader.go:185`) — constructs the download URL for a plugin from grafana.com.

### 2. Plugin Surfaces

**A. CLI Installation Surface**

The primary user-facing plugin surface is the **CLI install/uninstall/upgrade pipeline**:

- `installPlugin` (`install_command.go:108`) delegates to `doInstallPlugin` (`install_command.go:114`), which is recursive — it installs a plugin and all its dependencies. The guard `GUARD(installing[pluginID] -> return nil)` prevents circular dependency loops.
- `ContextCommandLine.PluginDirectory` (`command_line.go:57`) resolves the target directory, and is called by `newInstallPluginOpts`, `uninstallPlugin`, `validateInput`, `lsCommand`, `upgradeAllCommand`, `upgradeCommand` — revealing install, uninstall, list, and upgrade as the full CLI command surface.
- `GetGrafanaPluginDir` (`grafana_path.go:11`) provides platform-aware directory resolution with a dev-environment override (`tryGetRootForDevEnvironment`).

**B. Plugin Repository / Catalog Surface**

- `Manager.PluginVersion` (`repo/service.go:84`) is the entry point for version resolution; it calls `grafanaCompatiblePluginVersions` (`repo/service.go:110`), which queries the grafana.com API at `/api/plugins/$pluginID/versions`.
- `PluginInfo` (`repo/models.go:37`) and `grafanaComPluginVersionMeta` (`converter.go:717`) model the API response.
- `BuildPluginDownloadURL` (`downloader.go:185`) constructs the download URL, called by `ResolvePluginVersions`.
- `grafanaComPluginManifest` (`converter.go:741`) represents the plugin manifest — the signed metadata artifact from grafana.com.

**C. Core Plugin Surface**

- `corePlugin` (`coreplugin/core_plugin.go:15`) represents plugins built into Grafana core. Its methods — `CallResource`, `CheckHealth`, `CollectMetrics`, `ConvertObjects`, `Decommission`, `Exited` — define the backend plugin interface surface: resource serving, health checks, metrics collection, object conversion, lifecycle management.

**D. Live/Streaming Plugin Surface**

- `GrafanaLive.handlePluginScope` (`live.go:989`) handles plugin-scoped live streaming channels; it is called by `GetChannelHandlerFactory` and internally calls `getStreamPlugin` (`live.go:497`), which resolves a stream plugin by ID with a guard on non-existence.

**E. Alerting Plugin Surface**

- `DBstore.filterByPluginOrigin` (`alert_rule.go:1685`) adds filtering for plugin-originated alert rules based on the `__grafana_origin` label, showing plugins can originate alert rules that are then filterable in queries.

**F. Telemetry/Observability Surface**

- `GrafanaPluginId` (`semconv/attributes.go:139`) emits a `"grafana.plugin.id"` attribute for OpenTelemetry-style semantic conventions, enabling plugin-level observability.

### 3. Security Controls

**A. RBAC Cleanup on Plugin Removal**

- **`AccessControlStore.CleanupPluginRBAC`** (`pkg/services/accesscontrol/database/cleanup.go:17`) — "removes all RBAC data associated with the given plugin IDs: permissions on any role whose action starts with plugin-prefixed actions." Behavior: `ACCUMULATE(ContainsAny loop -> result)`, calls `cleanupPlugin`. This is the security boundary that ensures plugin removal purges all associated access control grants.

**B. Plugin Manifest Verification**

- `grafanaComPluginManifest` (`converter.go:741`) is a dedicated type for plugin manifests from grafana.com, and `grafanaComPluginVersionMetaToMetaSpec` (`converter.go:779`) calls `translationsFromManifest` — suggesting manifest-based verification is part of the plugin metadata pipeline. The `calculateLoadingStrategyFromGcomMeta` call further indicates the loading strategy (and thus security posture) is derived from the manifest.

**C. Recursive Dependency Guard**

- `doInstallPlugin` (`install_command.go:114`) has `GUARD(installing[pluginID] -> return nil)` — a re-entrancy guard preventing infinite recursion during dependency installation, which is a safety control against circular plugin dependencies.

**D. Plugin Directory Validation**

- `ContextCommandLine.PluginDirectory` (`command_line.go:57`) is called by `validateInput`, showing there is an input validation step before plugin operations proceed.

### 4. GAPS — What Cannot Be Determined

The GAPS section lists as **uncovered**:
- **`GetDatasourceGroupNameFromPluginID`** — how plugin IDs map to datasource API groups is not visible.
- **`GetPluginIDFromMeta`** — how plugin identity is extracted from metadata is not covered.
- **`GrafanaDatasourceRequestQueryCount`** and **`GrafanaDatasourceType`** — datasource-specific plugin metrics/types are not determinable.

Additionally, from the clue alone:
- The **plugin signature verification** mechanism (whether signatures are cryptographically validated beyond manifest presence) cannot be confirmed.
- The **plugin sandbox or isolation** model (if any runtime isolation exists between plugins) is not visible.
- Whether RBAC permissions are **proactively checked before plugin loading** (vs. only cleaned up on removal) is not determinable from `CleanupPluginRBAC` alone.

### 5. Synthesis

Grafana exposes **six plugin surfaces**: (1) a CLI installation pipeline with recursive dependency resolution (`installPlugin`/`doInstallPlugin`, `install_command.go`), (2) a grafana.com catalog/repository API for version and compatibility resolution (`Manager.PluginVersion`, `repo/service.go:84`), (3) a core plugin backend interface with health, resource, metrics, and lifecycle methods (`corePlugin`, `core_plugin.go:15`), (4) a live/streaming channel scope for plugins (`GrafanaLive.handlePluginScope`, `live.go:989`), (5) an alerting origin filter for plugin-sourced rules (`DBstore.filterByPluginOrigin`, `alert_rule.go:1685`), and (6) a telemetry attribute surface (`GrafanaPluginId`, `semconv/attributes.go:139`).

Security controls include **RBAC cleanup on plugin removal** (`AccessControlStore.CleanupPluginRBAC`, `cleanup.go:17`), **manifest-based metadata verification** (`grafanaComPluginManifest`, `converter.go:741`), **circular dependency prevention** (`doInstallPlugin` guard, `install_command.go:114`), and **input validation** on plugin directory operations (`validateInput` caller chain, `command_line.go:57`). The full extent of runtime plugin isolation, signature cryptographic verification, and proactive RBAC checks before loading remain undeterminable from the clue (GAPS).
