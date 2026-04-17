# Enterprise v2: ent-consul-struct-2
Date: 2026-04-17

## Question
How do the docs describe Consul's cluster communication and federation topology?

## Reasoning Scaffold

### Step 1: Identify Relevant Modules, Symbols, and Relationships

**From TREE:**
- `agent/consul/` — houses federation state endpoints, leader logic, and state store operations.
- `agent/xds/` — contains xDS resource generators that build Envoy configuration for cross-cluster routing.
- `proto/private/` — protobuf definitions for internal cluster communication.

**From INDEX:**
- `agent/structs/structs.go` (3354L) — `PartitionOrDefault`, `NamespaceOrDefault` indicate multi-tenancy awareness in cluster communication.

**From FOCUS — Federation topology symbols:**

- `FederationState` endpoint (`agent/consul/federation_state_endpoint.go:44`) — "used to manipulate federation states from all datacenters." Methods: `Apply`, `Get`, `List`, `ListMeshGateways`. This is the primary control surface for federation topology.

- `FederationState.Apply` (`agent/consul/federation_state_endpoint.go:48`) — behavior: `GUARD(done, err := c.srv.ForwardRPC("FederationStat... -> return err); PRECEDENCE(done -> not_c.srv.DatacenterSupportsFede -> err)`. Calls `ResolveToken`, `ForwardRPC`, `DatacenterSupportsFederationStates`, `raftApply`. The RPC forwarding pattern indicates that federation state mutations are forwarded across datacenters.

- `FederationState.Get` (`agent/consul/federation_state_endpoint.go:98`) — same GUARD/PRECEDENCE pattern with `ForwardRPC` and `DatacenterSupportsFederationStates`. Calls `ResolveToken` for ACL enforcement.

- `FederationState.List` (`agent/consul/federation_state_endpoint.go:137`) — "the endpoint meant to be used by consul servers performing replication." Same forwarding pattern. Called by `Acquire`, `Destroy`, `monitorLock`, `Run`, and others — showing it is consumed broadly for replication and coordination.

- `Server.DatacenterSupportsFederationStates` (`agent/consul/leader.go:1158`) — behavior: `GUARD(atomic.LoadInt32(&s.dcSupportsFederationState... -> return true); PRECEDENCE(atomic -> s -> state)`. Uses an atomic flag to track whether the datacenter supports federation states. Called by `Apply`, `Get`, `List`, `ListMeshGateways`, `FetchRemote`, `federationStateAntiEntropySync`, `startFederationStateAntiEntropy`.

- `Server.startFederationStateReplication` (`agent/consul/leader.go:823`) — behavior: `GUARD(s.config.PrimaryDatacenter == "" || s.config.... -> return)`. Called by `establishLeadership`. This shows replication is initiated by the leader and is conditional on having a `PrimaryDatacenter` configured, implying a primary/secondary datacenter topology.

- `Server.stopFederationStateAntiEntropy` (`agent/consul/leader_federation_state_ae.go:66`) — behavior: `GUARD(s.config.DisableFederationStateAntiEntropy -> return)`. Called by `revokeLeadership`. Anti-entropy runs on the leader and can be disabled via configuration.

- `Server.setDatacenterSupportsFederationStates` (`agent/consul/leader.go:1154`) — called by `updateFromState`, `DatacenterSupportsFederationStates`, `startFederationStateAntiEntropy`. This is the setter for the atomic flag.

- `serversFederationStatesInfo.update` (`agent/consul/leader.go:1198`) — behavior: `GUARD(srv.Status != serf.StatusAlive && srv.Status... -> return true); PRECEDENCE(srv -> supported)`. Uses serf member status to determine federation support, showing that federation capability detection is based on serf gossip membership.

**From FOCUS — State store operations:**

- `Store.FederationStateSet` (`agent/consul/state/federation_state.go:75`) — "upsert of a given federation state." Uses WriteTxn/Commit/Abort pattern.
- `Store.FederationStateGet` (`agent/consul/state/federation_state.go:131`) — "called to get a federation state." Delegates to `federationStateGetTxn`.
- `Store.FederationStateList` (`agent/consul/state/federation_state.go:161`) — "called to get all federation state objects."
- `Store.FederationStateDelete` (`agent/consul/state/federation_state.go:184`) — single datacenter delete.
- `Store.FederationStateBatchSet` (`agent/consul/state/federation_state.go:61`) — batch upsert, accumulates `federationStateSetTxn` calls.
- `Store.FederationStateBatchDelete` (`agent/consul/state/federation_state.go:195`) — batch delete across datacenters.
- `Restore.FederationState` (`agent/consul/state/federation_state.go:49`) — "used when restoring from a snapshot." Inserts into `tableFederationStates`.
- `federationStateSetTxn` (`agent/consul/state/federation_state.go:87`) — behavior: `GUARD(config.Datacenter == "" -> return fmt.Errorf("...)`. Requires a non-empty `Datacenter` field, confirming that federation state is keyed by datacenter.

**From FOCUS — Mesh topology and cross-cluster routing:**

- `updateMeshTopology` (`agent/consul/state/catalog.go:4924`) — "creates associations between the input service and its upstreams in the topology table." Called by `ensureServiceTxn`.
- `cleanupMeshTopology` (`agent/consul/state/catalog.go:4998`) — "removes a service from the mesh topology table." Called by `deleteServiceTxn`.
- `ResourceGenerator.makeExternalIPCluster` (`agent/xds/clusters.go:2108`) — "creates an Envoy cluster for routing to IP addresses outside of Consul. This is used by terminating." Called by `makeDestinationClusters`. This shows that cross-cluster communication can involve terminating gateways routing to external IPs.

### Step 2: Trace Call Chains and Hierarchies

**Federation state lifecycle (leader-driven):**
`establishLeadership` → `startFederationStateReplication` (guarded by `PrimaryDatacenter` config) → replication begins.
`revokeLeadership` → `stopFederationStateAntiEntropy` (guarded by `DisableFederationStateAntiEntropy`).

This shows federation replication is leader-initiated and follows a primary datacenter model.

**Federation state capability detection:**
`serversFederationStatesInfo.update` checks `serf.StatusAlive` → `setDatacenterSupportsFederationStates` sets atomic flag → `DatacenterSupportsFederationStates` reads atomic flag → used as a precondition in `FederationState.Apply/Get/List`.

This chain shows that federation support is discovered through serf gossip: servers detect whether peers support federation states based on serf membership tags, and this information gates federation operations.

**RPC forwarding pattern for federation:**
All `FederationState` endpoint methods (`Apply`, `Get`, `List`) follow the same behavior pattern: `ForwardRPC("FederationStat...")` → check `DatacenterSupportsFederationStates` → proceed or error. The `ForwardRPC` call indicates that federation operations can be forwarded to remote datacenters, with the prerequisite that the target datacenter supports federation states.

**State store CRUD:**
`FederationStateBatchSet` → loop of `federationStateSetTxn` (each requiring `Datacenter != ""`) → `Insert` into state store.
`FederationStateBatchDelete` → loop of `federationStateDeleteTxn`.
`Restore.FederationState` → `Insert` into `tableFederationStates` (for snapshot restore).

### Step 3: GAPS — What Cannot Be Determined

Per the GAPS section:
- **Type:** STRUCTURAL (answerable from L0-L2)
- **Coverage:** 83 symbols in L3, 43 with behavior annotations.
- **Uncovered symbols:**
  - `ServiceTopologySummary` — the aggregated topology summary structure cannot be examined.
  - `V1ConsulRegistrator` — the v1 registrator lifecycle is not traced.
  - `clusterOpts` — the options for cluster creation in xDS are not available.
  - `serverFederationStateListMeshGateways` — the mechanism by which federation state lists mesh gateways cannot be fully traced.

Additionally, the `FederationState.ListMeshGateways` method is listed in the `FederationState` endpoint's method list but has no dedicated FOCUS entry, so its behavior (how mesh gateway addresses are aggregated across federated datacenters) cannot be determined from the clue alone.

The README provides no inline documentation about federation topology (it only lists section headers: Quick Start, Documentation, Contributing).

### Step 4: Synthesis

**Cluster Communication Architecture:**

Based on the clue, Consul's cluster communication operates through several interacting layers:

1. **Serf gossip for capability discovery:** The `serversFederationStatesInfo.update` function (`agent/consul/leader.go:1198`) checks `serf.StatusAlive` to detect whether remote servers support federation states. This serf-based discovery mechanism is the foundation for determining cluster communication capabilities.

2. **RPC forwarding across datacenters:** All `FederationState` endpoint methods (`agent/consul/federation_state_endpoint.go`) use `ForwardRPC` to route requests to the appropriate datacenter. The consistent pattern — `ForwardRPC` → `DatacenterSupportsFederationStates` check → proceed — shows that cross-datacenter communication is RPC-based with capability gating.

3. **ACL-protected operations:** Each federation endpoint calls `ResolveToken` (`FederationState.Apply` at line 48, `FederationState.Get` at line 98, `FederationState.List` at line 137), ensuring federation operations are ACL-authorized.

**Federation Topology:**

1. **Primary/secondary datacenter model:** `Server.startFederationStateReplication` (`agent/consul/leader.go:823`) guards on `PrimaryDatacenter`, indicating a hub-and-spoke topology where a primary datacenter is designated and secondary datacenters replicate federation state from it.

2. **Datacenter-keyed federation state:** `federationStateSetTxn` (`agent/consul/state/federation_state.go:87`) requires `config.Datacenter != ""`, confirming that each federation state record is identified by its datacenter name. The state store supports full CRUD: `FederationStateSet`, `FederationStateGet`, `FederationStateList`, `FederationStateDelete`, plus batch operations (`FederationStateBatchSet`, `FederationStateBatchDelete`) — all in `agent/consul/state/federation_state.go`.

3. **Leader-driven anti-entropy:** Federation state synchronization uses an anti-entropy pattern driven by the cluster leader. `startFederationStateAntiEntropy` is called during leadership establishment (via `startFederationStateReplication` → `establishLeadership`), and `stopFederationStateAntiEntropy` (`agent/consul/leader_federation_state_ae.go:66`) runs on leadership revocation. This can be disabled via `DisableFederationStateAntiEntropy`.

4. **Snapshot restore support:** `Restore.FederationState` (`agent/consul/state/federation_state.go:49`) enables federation state recovery from snapshots, ensuring durability of the federation topology.

5. **Mesh topology tracking:** Within each datacenter, `updateMeshTopology` and `cleanupMeshTopology` (`agent/consul/state/catalog.go:4924, 4998`) maintain a service-level topology graph in the state store, tracking upstream/downstream relationships for meshed services.

6. **Cross-cluster routing via gateways:** `ResourceGenerator.makeExternalIPCluster` (`agent/xds/clusters.go:2108`) creates Envoy clusters for routing to IPs outside Consul, used by terminating gateways. The `FederationState` endpoint includes `ListMeshGateways` as a method, indicating mesh gateways play a role in cross-datacenter federation routing.

**Unresolved:** The exact behavior of `FederationState.ListMeshGateways` and `serverFederationStateListMeshGateways` (GAPS: uncovered) cannot be determined — these would clarify how mesh gateway addresses are aggregated and distributed across federated datacenters. The full gossip protocol details and WAN federation mechanics beyond RPC forwarding are also not reconstructable from the clue.
