# Enterprise v2: ent-consul-mech-1
Date: 2026-04-17

## Question
How does the docs describe the Envoy configuration lifecycle in Consul?

## Reasoning Scaffold

### Step 1: Identify Relevant Modules, Symbols, and Relationships

**From TREE:**
- `agent/xds/` — xDS server implementation, delta protocol, resource generation.
- `envoyextensions/` (9 files) — Envoy extension framework with extensioncommon.
- `agent/proxycfg/` — proxy configuration snapshots consumed by xDS.
- `proto/private/pbcommon/` — protobuf definitions for EnvoyExtension.
- `command/connect/envoy/` — Envoy bootstrap and version compatibility.
- `agent/structs/` — structural definitions including `EnvoyExtension`.

**From INDEX:**
- `proto-public/pbdataplane/dataplane.pb.go` (647L) — `GetFeatureName`, `GetSupported` — data-plane feature negotiation.

**From FOCUS — Core xDS Lifecycle Symbols:**

- `getEnvoyConfiguration` (`agent/xds/delta.go:105`) — "a utility function that instantiates the proper Envoy resource generator and returns the generated Envoy resources." Behavior: `DELEGATE(generator.AllResourcesFromSnapshot -> result)`. Called by `processDelta`. This is the function that transforms a proxy config snapshot into Envoy resources.

- `Server.applyEnvoyExtensions` (`agent/xds/delta.go:416`) — applies Envoy extensions to generated resources. Behavior: `GUARD(err != nil -> return nil, status....); ACCUMULATE(validateAndApplyEnvoy... -> result)`. Calls `validateAndApplyEnvoyExtension`. Called by `processDelta`. This shows extensions are applied *after* base resource generation.

**From Source Snippets — xDS Delta Protocol:**

- `Server.DeltaAggregatedResources` (`agent/xds/delta.go:63`) — `func (s *Server) DeltaAggregatedResources(stream ADSDeltaStream) error`. This is the main xDS entry point — an ADS (Aggregated Discovery Service) delta stream handler.

- `Server.processDelta` (`agent/xds/delta.go:120`) — `func (s *Server) processDelta(stream ADSDeltaStream, reqCh <-chan *envoy_discovery_v3.DeltaDiscoveryRequest) error`. The core processing loop that handles the delta xDS protocol. It consumes `DeltaDiscoveryRequest` messages from the stream channel.

- `xDSDeltaType` (`agent/xds/delta.go:637`) — struct type representing a single xDS resource type within the delta protocol. Methods include:
  - `Recv` (`agent/xds/delta.go:709`) — receives a `DeltaDiscoveryRequest` and returns a `deltaRecvResponse`, also takes `SupportedProxyFeatures`.
  - `ack` (`agent/xds/delta.go:841`) — acknowledges a nonce.
  - `nack` (`agent/xds/delta.go:859`) — negative-acknowledges a nonce.
  - `subscribed` (`agent/xds/delta.go:676`) — checks if a resource name is subscribed.
  - `ensureChildResend` (`agent/xds/delta.go:1049`) — ensures child resources are resent when a parent changes.

- `xDSDeltaChild` (`agent/xds/delta.go:626`) — struct for tracking child resource relationships.
- `PendingUpdate` (`agent/xds/delta.go:684`) — struct tracking a pending update to be sent.
- `xDSUpdateOperation` (`agent/xds/delta.go:607`) — struct with method `errorLogNameReplyPrefix` (`agent/xds/delta.go:613`) for logging.

- `computeResourceVersions` (`agent/xds/delta.go:1097`) — computes resource versions from an `IndexedResources` map.
- `hashResource` (`agent/xds/delta.go:1141`) — hashes a single proto message for version tracking.
- `hashResourceMap` (`agent/xds/delta.go:1128`) — hashes a map of resources.
- `populateChildIndexMap` (`agent/xds/delta.go:1109`) — populates the child index map from `IndexedResources`.

**From Source Snippets — Extension Application:**

- `validateAndApplyEnvoyExtension` (`agent/xds/delta.go:439`) — `func validateAndApplyEnvoyExtension(logger hclog.Logger, cfgSnap *proxycfg.ConfigSnapshot, resources *xdscommon.IndexedResources, runtimeConfig extensioncommon.RuntimeConfig, envoyVersion, consulVersion *goversion.Version) (*xdscommon.IndexedResources, error)`. Validates version compatibility and applies a single extension.

- `applyEnvoyExtension` (`agent/xds/delta.go:554`) — `func applyEnvoyExtension(extender extensioncommon.EnvoyExtender, resources *xdscommon.IndexedResources, runtimeConfig *extensioncommon.RuntimeConfig) (r *xdscommon.IndexedResources, e error)`. Applies a single extension using an `EnvoyExtender`.

**From FOCUS — EnvoyExtension Entity:**

- `EnvoyExtension` (`agent/structs/envoy_extension.go:11`) — "has configuration for an extension that patches Envoy resources." Methods: `appendHash`, `getHash`.
- `EnvoyExtension` (`proto/private/pbcommon/common.pb.go:582`) — protobuf definition with mog annotation targeting `agent/structs.EnvoyExtension`. Methods: `GetArguments`, `GetConsulVersion`, `GetEnvoyVersion`, `GetName`, `GetRequired`, `ProtoReflect`.
- `EnvoyExtension` (`api/config_entry.go:148`) — API-level definition.
- `EnvoyExtension.GetConsulVersion` (`proto/private/pbcommon/common.pb.go:645`) — behavior: `GUARD(x != nil -> return x.ConsulVersion)`.
- `EnvoyExtension.GetEnvoyVersion` (`proto/private/pbcommon/common.pb.go:652`) — behavior: `GUARD(x != nil -> return x.EnvoyVersion)`.
- `ConnectProxyConfig.GetEnvoyExtensions` (`proto/private/pbservice/service.pb.go:210`) — behavior: `GUARD(x != nil -> return x.EnvoyExten...)`. Extensions are carried on the connect proxy configuration.

**From FOCUS — Extension Patching:**

- `UpstreamEnvoyExtender.patchConnectProxyListener` (`envoyextensions/extensioncommon/upstream_envoy_extender.go:169`) — behavior: `GUARD(IsOutboundTProxyListener(l) -> return ext.patchTPr...); PRECEDENCE(IsOutboundTProxyListener -> envoyID); ACCUMULATE(PatchFilter loop -> filters filter)`. Calls `patchTProxyListener`. Called by `patchListener`. This shows the extension patching differentiates between transparent proxy listeners and regular listeners, and patches individual filters within listeners.

**From FOCUS — Version Compatibility:**

- `checkEnvoyVersionCompatibility` (`command/connect/envoy/envoy.go:1074`) — behavior: `GUARD(err != nil -> return envoyCompat{...); PRECEDENCE(err -> len)`. Calls `replacePatchVersionWithX`. Called by `run`. This validates Envoy version compatibility during the `consul connect envoy` command, before the Envoy process is started.

**From FOCUS — Configuration and Autopilot:**

- `AutoConfig.InitialConfiguration` (`agent/consul/auto_config_endpoint.go:349`) — "authorize the incoming request and then generate the configuration to push down to the client." While not directly Envoy-specific, this shows the broader configuration lifecycle pattern.

- `UpstreamConfiguration` (`proto/private/pbconfigentry/config_entry.pb.go:4503`) — upstream configuration that feeds into proxy config snapshots.

- `IsConsulServer` (`agent/metadata/server.go:77`) — "returns true if a serf member is a consul server agent." Behavior: `GUARD(m.Tags["role"] != "consul" -> return false, nil)`. Uses serf member tags to determine server identity.

### Step 2: Trace the Envoy Configuration Lifecycle

**Phase 1: Version Check and Bootstrap**
`run` (consul connect envoy command) → `checkEnvoyVersionCompatibility` (`command/connect/envoy/envoy.go:1074`) — validates Envoy version against unsupported list using `replacePatchVersionWithX`. If incompatible, returns an `envoyCompat` struct indicating the issue.

**Phase 2: Proxy Configuration Snapshot Compilation**
The control plane compiles proxy configuration snapshots (in `agent/proxycfg/`). These snapshots include:
- Service definitions and upstream configurations (`UpstreamConfiguration`)
- Envoy extensions attached to the proxy config (`ConnectProxyConfig.GetEnvoyExtensions`)
- Mesh gateway settings and exported services

**Phase 3: xDS Delta Stream Establishment**
`Server.DeltaAggregatedResources` (`agent/xds/delta.go:63`) — the Envoy sidecar connects to Consul's xDS server via the ADS delta protocol. This creates a bidirectional stream.

**Phase 4: Delta Processing Loop**
`Server.processDelta` (`agent/xds/delta.go:120`) — the main loop that:
1. Receives `DeltaDiscoveryRequest` messages from Envoy via `xDSDeltaType.Recv` (`agent/xds/delta.go:709`).
2. Generates Envoy resources by calling `getEnvoyConfiguration` → `generator.AllResourcesFromSnapshot` (transforms the config snapshot into Envoy resource types: clusters, listeners, routes, endpoints).
3. Applies Envoy extensions via `Server.applyEnvoyExtensions` (`agent/xds/delta.go:416`).
4. Computes resource versions via `computeResourceVersions` → `hashResourceMap` → `hashResource` (`agent/xds/delta.go:1097, 1128, 1141`) for change detection.
5. Populates child index maps via `populateChildIndexMap` (`agent/xds/delta.go:1109`) to track parent-child resource relationships.
6. Sends updates back to Envoy through the stream.
7. Processes ack/nack responses from Envoy via `xDSDeltaType.ack` / `xDSDeltaType.nack` (`agent/xds/delta.go:841, 859`).

**Phase 5: Extension Validation and Application**
`Server.applyEnvoyExtensions` accumulates results from `validateAndApplyEnvoyExtension` (`agent/xds/delta.go:439`), which:
1. Checks Envoy version and Consul version compatibility (using `EnvoyExtension.GetEnvoyVersion` and `GetConsulVersion`).
2. Calls `applyEnvoyExtension` (`agent/xds/delta.go:554`) with an `EnvoyExtender` and `RuntimeConfig`.
3. The `EnvoyExtender` patches resources — e.g., `UpstreamEnvoyExtender.patchConnectProxyListener` patches listener filters, differentiating transparent proxy listeners from standard ones.

**Phase 6: Incremental Updates**
The delta protocol supports incremental updates:
- `xDSDeltaType.subscribed` (`agent/xds/delta.go:676`) — tracks which resources Envoy has subscribed to.
- `xDSDeltaType.ensureChildResend` (`agent/xds/delta.go:1049`) — ensures child resources are resent when a parent resource changes (e.g., when a cluster changes, its associated endpoints are resent).
- `PendingUpdate` (`agent/xds/delta.go:684`) — tracks pending updates to be delivered.

### Step 3: GAPS — What Cannot Be Determined

Per the GAPS section:
- **Type:** MECHANISTIC (body logic needed for full answer)
- **Coverage:** 83 symbols in L3, 47 with behavior annotations.
- **Uncovered symbols:**
  - `ConsulResolver` — the connect resolver's full lifecycle in xDS context is not traced.
  - `DataplaneServiceClient_GetEnvoyBootstrapParams_Call` — the bootstrap parameter retrieval mechanism is not available.
  - `DataplaneServiceServer_GetEnvoyBootstrapParams_Call` — server-side bootstrap params generation is not traced.
  - `EnvoyExtender` — the `EnvoyExtender` interface itself is not fully described (only its usage via `UpstreamEnvoyExtender`).
- **Drill target:** `getEnvoyConfiguration` (`agent/xds/delta.go:105`) — only the function signature is provided in the source snippet, not the body.

This means the exact Envoy bootstrap configuration process (how initial bootstrap parameters are generated and delivered), the full `EnvoyExtender` interface contract, and the internal resource generation logic within `getEnvoyConfiguration` / `AllResourcesFromSnapshot` cannot be determined from the clue.

### Step 4: Synthesis

**The Envoy Configuration Lifecycle in Consul** follows a multi-phase pipeline:

1. **Version Compatibility Check:** Before Envoy starts, `checkEnvoyVersionCompatibility` (`command/connect/envoy/envoy.go:1074`) validates the Envoy version against a known-unsupported list. Bootstrap parameters are retrieved (via the uncovered `GetEnvoyBootstrapParams` mechanism in `proto-public/pbdataplane/`).

2. **xDS Stream Establishment:** Envoy connects to Consul's xDS server via `Server.DeltaAggregatedResources` (`agent/xds/delta.go:63`), establishing a bidirectional ADS delta stream. This is the only xDS entry point visible in the clue.

3. **Resource Generation from Config Snapshots:** Within the delta processing loop (`Server.processDelta`, `agent/xds/delta.go:120`), `getEnvoyConfiguration` (`agent/xds/delta.go:105`) delegates to `generator.AllResourcesFromSnapshot` to transform a `ConfigSnapshot` into Envoy resource maps (clusters, listeners, routes, endpoints). The config snapshot aggregates data from the control plane including upstream configuration (`UpstreamConfiguration`), service defaults, and mesh gateway settings.

4. **Extension Application:** After base resource generation, `Server.applyEnvoyExtensions` (`agent/xds/delta.go:416`) iterates through configured extensions. Each extension is validated for version compatibility (`validateAndApplyEnvoyExtension` at line 439 checks `EnvoyExtension.GetEnvoyVersion` and `GetConsulVersion`) and then applied via an `EnvoyExtender` (`applyEnvoyExtension` at line 554). Extensions can patch listeners (e.g., `UpstreamEnvoyExtender.patchConnectProxyListener` at `envoyextensions/extensioncommon/upstream_envoy_extender.go:169`), with special handling for transparent proxy listeners.

5. **Change Detection and Incremental Delivery:** Resources are version-tracked using `computeResourceVersions` → `hashResourceMap` → `hashResource` (`agent/xds/delta.go:1097-1141`). Parent-child relationships are tracked via `populateChildIndexMap` (`agent/xds/delta.go:1109`) and `xDSDeltaChild` (`agent/xds/delta.go:626`). When parent resources change, `ensureChildResend` (`agent/xds/delta.go:1049`) triggers re-delivery of dependent child resources.

6. **ACK/NACK Protocol:** Envoy responds with acknowledgments or negative-acknowledgments to each resource update. `xDSDeltaType.ack` (`agent/xds/delta.go:841`) confirms receipt; `xDSDeltaType.nack` (`agent/xds/delta.go:859`) signals rejection. The `Recv` method (`agent/xds/delta.go:709`) processes incoming requests, taking into account `SupportedProxyFeatures`.

7. **EnvoyExtension as a First-Class Entity:** `EnvoyExtension` exists in three parallel definitions — API (`api/config_entry.go:148`), structs (`agent/structs/envoy_extension.go:11`), and protobuf (`proto/private/pbcommon/common.pb.go:582`) — with mog annotations bridging proto to structs. Extensions carry `Name`, `Arguments`, `Required`, `ConsulVersion`, and `EnvoyVersion` fields. They are attached to proxy configurations via `ConnectProxyConfig.GetEnvoyExtensions` (`proto/private/pbservice/service.pb.go:210`).

**Unresolved:** The bootstrap parameter generation (`GetEnvoyBootstrapParams`), the `EnvoyExtender` interface definition, the full body of `getEnvoyConfiguration`, and the `ConsulResolver`'s interaction with the xDS lifecycle cannot be reconstructed from the clue alone.
