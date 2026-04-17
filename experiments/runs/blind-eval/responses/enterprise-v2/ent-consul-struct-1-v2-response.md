# Enterprise v2: ent-consul-struct-1
Date: 2026-04-17

## Question
According to the docs, how is Consul's service mesh split between control plane and data plane?

## Reasoning Scaffold

### Step 1: Identify Relevant Modules, Symbols, and Relationships

**From TREE:**
- `agent/` (716 files) — the dominant module, housing proxy configuration (`proxycfg/`), xDS delivery, DNS, and consul server logic.
- `connect/` (10 files) — service-mesh connectivity primitives (resolver, CSR).
- `envoyextensions/` (9 files) — data-plane extension hooks.
- `proto-public/pbdataplane/` — a dedicated protobuf package for the data-plane interface.
- `acl/` (20 files) — authorization layer that gates mesh operations.

**From INDEX:**
- `proto-public/pbdataplane/dataplane.pb.go` (647L) exposes `GetFeatureName`, `GetSupported` — indicating a negotiation interface between the control plane and the data-plane sidecar (`proto-public/pbdataplane/dataplane.pb.go`, INDEX).

**From FOCUS — control-plane symbols:**
- `PeeringBackend.PeerThroughMeshGateways` (`agent/consul/peering_backend.go:183`) — determines whether "peering control plane traffic" is routed through a mesh gateway. Its `called_by` list includes `clustersFromSnapshotMeshGateway` and `endpointsFromSnapshotMeshGateway`, tying control-plane peering decisions to data-plane Envoy resource generation.
- `updateMeshTopology` (`agent/consul/state/catalog.go:4924`) — "creates associations between the input service and its upstreams in the topology table." This is a control-plane state-store operation called by `ensureServiceTxn`.
- `cleanupMeshTopology` (`agent/consul/state/catalog.go:4998`) — removes a service from the topology table, called by `deleteServiceTxn`. Together with `updateMeshTopology`, these maintain the control-plane's view of the mesh graph.
- `AllowAuthorizer.MeshReadAllowed` (`acl/authorizer.go:345`) and `AllowAuthorizer.MeshWriteAllowed` (`acl/authorizer.go:354`) — determine whether read-only or state-changing "Consul mesh functions" can be used. `MeshWriteAllowed` calls `MeshWrite`, which in turn is implemented by `ChainedAuthorizer.MeshWrite` (`acl/chained_authorizer.go:162`). This shows the control plane enforces ACL authorization on mesh operations.
- `Store.ServiceUsage` (`agent/consul/state/usage.go:413`) — returns compiled service usage data from the state store, accumulating usage entries. Another control-plane bookkeeping function.
- `configSnapshotMeshGateway.IsServiceExported` (`agent/proxycfg/snapshot.go:608`) and `ConfigSnapshot.MeshGatewayValidExportedServices` (`agent/proxycfg/snapshot.go:528`) — proxy configuration snapshots that the control plane compiles and the data plane consumes.
- `ServiceSplit` (`agent/structs/config_entry_discoverychain.go:842`) — "defines how much traffic to send to which set of service instances during a traffic split." This is a control-plane config entry.
- `NormalizeServiceSplitWeight` (`agent/structs/config_entry_discoverychain.go:728`) — normalizes split weights, delegates to `scaleWeight`.
- `DiscoverySplit` (`agent/structs/discovery_chain.go:243`) — "compiled form of ServiceSplit." The control plane compiles `ServiceSplit` into `DiscoverySplit` before the data plane uses it.

**From FOCUS — data-plane / connect symbols:**
- `ConsulResolver` (`connect/resolver.go:64`) — "queries Consul for a service instance." Methods: `Resolve`, `resolveQuery`, `resolveService`, `resolveServiceEntry`. The resolver sits in the `connect/` package and acts as a bridge: the data plane calls it to resolve endpoints that the control plane manages.
- `ConsulResolver.resolveServiceEntry` (`connect/resolver.go:143`) — behavior: `PRECEDENCE(addr -> entry -> service)`, showing a cascading resolution strategy.
- `ConsulResolver.resolveService` (`connect/resolver.go:102`) — calls `queryOptions` then `resolveServiceEntry`, guarding on errors.
- `MeshGatewayConfig` (`proto/private/pbservice/service.pb.go:708`) — protobuf type with a mog annotation targeting `agent/structs.MeshGatewayConfig`, bridging the proto layer (data-plane communication) to the structs layer (control-plane state).
- `ServiceDefaults.GetMeshGateway` (`proto/private/pbconfigentry/config_entry.pb.go:4145`) — retrieves mesh gateway configuration from a `ServiceDefaults` config entry.
- `ExportedService` / `ExportedServiceList` (`proto/private/pbpeerstream/peerstream.pb.go:258, 303`) — data returned via peer stream replication, representing exported services flowing between control planes.
- `DNSServer.lookupServiceNodes` (`agent/dns.go:1499`) — "look up a node in the Consul health catalog within ServiceNodes." This is a control-plane service discovery function that data-plane consumers (and DNS clients) rely on.

### Step 2: Trace Call Chains and Hierarchies

**Control-plane state management chain:**
`ensureServiceTxn` → `updateMeshTopology` → `Insert` (into topology table)
`deleteServiceTxn` → `cleanupMeshTopology` → `Delete` / `Insert`

This shows the control plane maintains a topology table in its state store that tracks upstream/downstream relationships between meshed services.

**ACL authorization chain for mesh operations:**
`MeshWriteAllowed` → `MeshWrite` → `ChainedAuthorizer.executeChain` (`acl/chained_authorizer.go:29`)
`MeshReadAllowed` → `MeshRead`

The control plane gates all mesh mutations through an ACL chain.

**Proxy configuration compilation chain:**
`ServiceSplit` (config entry) → `DiscoverySplit` (compiled form) — the control plane compiles user-defined traffic-split config entries into a form the data-plane proxy can consume.
`ConfigSnapshot.MeshGatewayValidExportedServices` accumulates exported services into the snapshot.
`configSnapshotMeshGateway.IsServiceExported` → `hasEntExportedService` — checks whether a service should be visible in the data plane.

**Data-plane resolution chain:**
`ConsulResolver.Resolve` → `resolveService` → `resolveServiceEntry`
The `connect/` package resolver queries the control plane's catalog to obtain service endpoints for the data-plane sidecar.

**Peering control-plane traffic routing:**
`PeeringBackend.PeerThroughMeshGateways` is called by `clustersFromSnapshotMeshGateway` and `endpointsFromSnapshotMeshGateway` — these are xDS resource generators that produce Envoy configuration. This shows the control plane decides *whether* peering traffic traverses mesh gateways, and that decision is encoded into the data-plane (Envoy) configuration.

### Step 3: GAPS — What Cannot Be Determined

Per the GAPS section:
- **Type:** STRUCTURAL (answerable from L0-L2)
- **Coverage:** 82 symbols in L3, 23 with behavior annotations.
- **Uncovered symbols:** `ShadowServiceRouterConfigEntry.CheckEnt`, `ACLResolver.synthesizePoliciesForServiceIdentities`, `ConnectProxyConfig.GetMeshGateway`, `EventPayloadServiceListUpdate.HasReadPermission`.

Specifically, `ConnectProxyConfig.GetMeshGateway` is uncovered, meaning the exact mechanism by which the connect proxy config retrieves its mesh gateway settings cannot be fully traced from the clue alone. Similarly, the detailed ACL policy synthesis for service identities (`ACLResolver.synthesizePoliciesForServiceIdentities`) is not available, so the full authorization pathway for mesh identity-based access cannot be determined.

The clue also does not provide the implementation details of how `proto-public/pbdataplane/dataplane.pb.go`'s `GetFeatureName`/`GetSupported` are used at runtime to negotiate data-plane capabilities. The README only lists sections (Quick Start, Documentation, Contributing) without inline doc content about the conceptual split.

### Step 4: Synthesis

**Control Plane** — Based on the clue, Consul's control plane encompasses:

1. **State store and topology management:** The control plane maintains a mesh topology table via `updateMeshTopology` (`agent/consul/state/catalog.go:4924`) and `cleanupMeshTopology` (`agent/consul/state/catalog.go:4998`), tracking which services are connected as upstreams/downstreams. Service usage is compiled by `Store.ServiceUsage` (`agent/consul/state/usage.go:413`).

2. **Configuration entries and compilation:** Traffic management policies are defined as control-plane config entries such as `ServiceSplit` (`agent/structs/config_entry_discoverychain.go:842`), which are then compiled into `DiscoverySplit` (`agent/structs/discovery_chain.go:243`) — the "compiled form of ServiceSplit" — for consumption by the data plane.

3. **ACL enforcement:** The control plane enforces mesh-level ACLs through `AllowAuthorizer.MeshReadAllowed` (`acl/authorizer.go:345`) and `AllowAuthorizer.MeshWriteAllowed` (`acl/authorizer.go:354`), using the `ChainedAuthorizer` pattern (`acl/chained_authorizer.go:162`).

4. **Proxy configuration snapshots:** The control plane builds configuration snapshots (`ConfigSnapshot.MeshGatewayValidExportedServices` at `agent/proxycfg/snapshot.go:528`, `configSnapshotMeshGateway.IsServiceExported` at `agent/proxycfg/snapshot.go:608`) that aggregate service export information and mesh gateway settings for delivery to data-plane sidecars.

5. **Peering and federation control:** `PeeringBackend.PeerThroughMeshGateways` (`agent/consul/peering_backend.go:183`) controls whether peering control-plane traffic flows through mesh gateways. Exported services are replicated via `ExportedService`/`ExportedServiceList` (`proto/private/pbpeerstream/peerstream.pb.go:258, 303`).

**Data Plane** — The data plane is represented by:

1. **The `proto-public/pbdataplane/` package:** `dataplane.pb.go` (`proto-public/pbdataplane/dataplane.pb.go`, INDEX) defines a gRPC interface with feature negotiation (`GetFeatureName`, `GetSupported`), indicating the data plane communicates with the control plane via gRPC to discover its supported capabilities.

2. **The `connect/` package resolver:** `ConsulResolver` (`connect/resolver.go:64`) queries Consul for service instances, bridging the data plane's need for endpoint addresses to the control plane's service catalog. It follows a `resolveService` → `resolveServiceEntry` chain with precedence-based resolution (`connect/resolver.go:143`).

3. **The `envoyextensions/` directory:** A dedicated package (9 files) for extending Envoy (the data-plane proxy) behavior.

4. **Mesh gateway configuration:** `MeshGatewayConfig` (`proto/private/pbservice/service.pb.go:708`) carries gateway mode settings from the control plane to the data plane via protobuf, mapped to `agent/structs.MeshGatewayConfig` through mog annotations.

**Structural boundary:** The split is reflected in the repository layout — control-plane logic lives primarily in `agent/consul/` (state store, endpoints, leader logic) and `agent/proxycfg/` (snapshot compilation), while data-plane interfaces live in `proto-public/pbdataplane/`, `connect/`, and `envoyextensions/`. The `agent/structs/` package serves as a shared vocabulary, with protobuf types in `proto/private/` bridging between the two planes.

**Unresolved:** The exact runtime negotiation protocol between the data-plane sidecar and the control plane (via `pbdataplane`) cannot be fully reconstructed from the clue. The behavior of `ConnectProxyConfig.GetMeshGateway` (GAPS: uncovered) would further clarify how mesh gateway mode propagates to the data plane.
