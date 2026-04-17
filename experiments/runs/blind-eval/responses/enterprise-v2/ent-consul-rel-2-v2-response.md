# Enterprise v2: ent-consul-rel-2
Date: 2026-04-17

## Question
What documented paths can register checks in Consul?

## Reasoning Scaffold

### Step 1: Identify Relevant Modules, Symbols, and Relationships

**From TREE:**
- `agent/` (716 files) — main agent logic including check registration, service registration, and health checking.
- `api/` (55 files) — client-side API for interacting with the Consul agent, including check registration.
- `command/connect/proxy/` — proxy registration with TTL health checks.
- `agent/consul/` — server-side catalog registration including checks.
- `agent/checks/` — check implementation types (e.g., alias checks).

**From FOCUS — Check Registration Paths Identified:**

**Path 1: API Client — `Agent.CheckRegister` / `Agent.CheckRegisterOpts`**

- `Agent.CheckRegister` (`api/agent.go:1075`) — "used to register a new check with the local agent." Behavior: `DELEGATE(a.CheckRegisterOpts -> result)`. This is the public API entry point for check registration.
- `Agent.CheckRegisterOpts` (`api/agent.go:1081`) — "used to register a new check with the local agent using query options." Behavior: `GUARD(err != nil -> return err); PRECEDENCE(err); UNWIND(defer)`. Calls `doRequest`, `newRequest`, `setQueryOptions`. Called by `CheckRegister`.

This path represents the HTTP API client path: external callers use the `api` package to register checks with the local agent via HTTP.

**Path 2: Catalog Server — `Catalog.Register`**

- `Catalog.Register` (`agent/consul/catalog_endpoint.go:108`) — "Register a service and/or check(s) in a node, creating the node if it doesn't exist." Behavior: `GUARD(!c.srv.config.PeeringTestAllowPeerRegistratio... -> return fmt.Errorf(...)); PRECEDENCE(not_c.srv.config.PeeringTestAllo -> done -> err); ACCUMULATE(checkPreApply loop -> result)`. Calls `State`, `ForwardRPC`, `NodeServices`, `checkPreApply`, `hasPeerNameInRequest`, `nodePreApply`, `servicePreApply`, `ResolveTokenAndDefaultMeta`.

This is the server-side catalog registration path. It accumulates checks via a `checkPreApply` loop, meaning multiple checks can be registered in a single catalog registration request. It supports RPC forwarding (`ForwardRPC`) for cross-datacenter operation.

**Path 3: Connect Proxy Registration — `RegisterMonitor`**

- `RegisterMonitor` (`command/connect/proxy/register.go:34`) — "registers the proxy with the local Consul agent with a TTL health check that is kept alive." Methods: `Close`, `Run`, `checkID`, `deregister`, `heartbeat`, `register`.
- `RegisterMonitor.register` (`command/connect/proxy/register.go:175`) — "register queries the Consul agent to determine if we've already registered." Behavior: `PRECEDENCE(err -> currentService)`. Calls `checkID`, `serviceID`, `serviceName`. Called by `Register`, `Run`.

This path is specific to the connect proxy command. The `RegisterMonitor` registers a proxy service *with a TTL health check* and keeps it alive via heartbeats (`RegisterMonitor.heartbeat` at `command/connect/proxy/register.go:230`).

**Path 4: Direct Agent Check Addition — `Agent.AddCheck`**

From source snippets:
- `Agent.AddCheck` (`agent/agent.go:2878`) — `func (a *Agent) AddCheck(check *structs.HealthCheck, chkType *structs.CheckType, persist bool, token string, source configSource) error`. This is the agent's internal method for adding a check, accepting a `HealthCheck` struct, a `CheckType`, persistence flag, token, and config source.
- `Agent.addCheckLocked` (`agent/agent.go:2884`) — the lock-protected variant.
- `Agent.addCheck` (`agent/agent.go:2931`) — an internal variant that also takes a `service` parameter.

**Path 5: Loading Persisted Checks on Agent Start — `Agent.loadChecks`**

From source snippets:
- `Agent.loadChecks` (`agent/agent.go:3934`) — `func (a *Agent) loadChecks(conf *config.RuntimeConfig, snap map[structs.CheckID]*structs.HealthCheck) error`. Loads previously persisted check definitions from disk on agent startup.
- `Agent.loadCheckState` (`agent/agent.go:3560`) — loads saved check state (e.g., TTL output).
- `Agent.persistCheck` (`agent/agent.go:2195`) — persists a check definition to disk, enabling reload on restart.

**Path 6: gRPC Server Registration (server-side infrastructure)**

Multiple `Server.register*Server` methods register gRPC service handlers:
- `Server.registerACLServer` (`agent/consul/server_grpc.go:356`)
- `Server.registerConfigEntryServer` (`agent/consul/server_grpc.go:526`)
- `Server.registerConnectCAServer` (`agent/consul/server_grpc.go:477`)
- `Server.registerDataplaneServer` (`agent/consul/server_grpc.go:497`)
- `Server.registerPeerStreamServer` (`agent/consul/server_grpc.go:381`)
- `Server.registerPeeringServer` (`agent/consul/server_grpc.go:409`)
- `Server.registerOperatorServer` (`agent/consul/server_grpc.go:443`)
- `Server.registerResourceServiceServer` (`agent/consul/server_grpc.go:339`)
- `Server.registerServerDiscoveryServer` (`agent/consul/server_grpc.go:512`)
- `Server.registerStreamSubscriptionServer` (`agent/consul/server_grpc.go:464`)

All called by `setupGRPCServices`. These are infrastructure registration paths (registering gRPC handlers), not health check registration per se, but they use `Handler.Register` (`agent/consul/rate/handler.go:337`) and `MockRequestLimitsHandler.Register` (`agent/consul/rate/mock_RequestLimitsHandler.go:32`) for rate-limiting registration.

**Path 7: Agent RPC Endpoint Registration**

- `Agent.registerEndpoint` (`agent/agent.go:1661`) — "registers a handler for the consul RPC server under a unique name while making it accessible." Calls `RegisterEndpoint`. Raises `panic` on failure. This is an agent infrastructure path for registering RPC handlers.

**From FOCUS — ACL verification for check registration:**

- `Agent.vetCheckRegisterWithAuthorizer` (`agent/acl.go:98`) — behavior: `GUARD(len(check.ServiceName) > 0 -> return err); PRECEDENCE(len -> existing)`. Calls `AgentEnterpriseMeta`. This shows that check registration is ACL-gated, and the authorization behavior differs based on whether the check is associated with a service (`check.ServiceName > 0`) or is a node-level check.

**From FOCUS — Check Alias processing:**

- `CheckAlias.processChecks` (`agent/checks/alias.go:259`) — "a common helper for taking a set of health checks and using them to update our alias." Behavior: `ACCUMULATE(EqualFold loop -> result)`. Calls `CompoundServiceID`. Called by `runLocal`, `runQuery`. This shows alias checks consume registered health checks but do not register new ones.

**From FOCUS — Related protobuf:**

- `CheckServiceNode.GetChecks` (`proto/private/pbservice/node.pb.go:136`) — behavior: `GUARD(x != nil -> return x.Checks)`. Returns checks associated with a service node, used for data retrieval.

**From FOCUS — State event processing:**

- `getNodeAndChecks` (`agent/consul/state/catalog_events.go:679`) — "returns a the node structure and a function that returns the full list of checks for a specific service." Behavior: `GUARD(err != nil -> return nil, nil, err); ACCUMULATE(loop -> nodeChecks check)`. Called by `newServiceHealthEventForService`, `newServiceHealthEventsForNode`. This is a read path, not a registration path.

### Step 2: Trace Call Chains

**API client path:**
`Agent.CheckRegister` → `Agent.CheckRegisterOpts` → `newRequest` → `setQueryOptions` → `doRequest` (HTTP PUT to agent API endpoint).

**Catalog server path:**
External RPC → `Catalog.Register` → `ForwardRPC` (if needed) → `checkPreApply` loop (validates each check) → `ResolveTokenAndDefaultMeta` (ACL check) → state store write.

**Connect proxy path:**
`RegisterMonitor.Run` → `RegisterMonitor.register` → queries agent, uses `checkID`/`serviceID`/`serviceName` to build registration → `heartbeat` keeps TTL check alive.
`RegisterMonitor.Close` → `RegisterMonitor.deregister` — cleans up on shutdown.

**Direct agent path:**
`Agent.AddCheck` → `Agent.addCheckLocked` → `Agent.addCheck` (with service context) → persistence via `Agent.persistCheck`.

**Startup loading path:**
Agent start → `Agent.loadChecks` (reads persisted checks from disk) → re-registers them. `Agent.loadCheckState` restores TTL state.

**ACL gate for all agent-local registration:**
`Agent.vetCheckRegisterWithAuthorizer` — differentiates service-bound checks from node-level checks for authorization purposes.

### Step 3: GAPS — What Cannot Be Determined

Per the GAPS section:
- **Type:** MECHANISTIC (body logic needed for full answer)
- **Coverage:** 83 symbols in L3, 45 with behavior annotations.
- **Uncovered symbols:**
  - `registry.register` — a generic registry registration method whose role is unclear.
  - `MockRegistry.Register` — test mock, not a production path.
  - `Server.Register` — the server-level registration method body is not available.
  - `V1ConsulRegistrator.HandleFailedMember` — the v1 registrator's failure handling is not traced.
- **Drill targets:** `RegisterMonitor.register` and `Agent.registerEndpoint` were identified for drill-down but source snippets show only function signatures without bodies.

The source snippets provided (File 2) show function signatures only (1-line bodies), so the internal logic of `RegisterMonitor.register` and `Agent.registerEndpoint` cannot be fully reconstructed. The exact HTTP endpoint paths (e.g., `/v1/agent/check/register`) are not visible in the clue.

Additionally, the `Agent.cleanupRegistration` (`agent/agent.go:2743`) source snippet shows it takes `serviceIDs` and `checkIDs` to clean up, but its relationship to registration is cleanup (deregistration), not registration.

### Step 4: Synthesis

**Documented Check Registration Paths:**

Based solely on the clue file and source snippets, there are five distinct paths for registering checks in Consul:

1. **HTTP API Client Path** — `Agent.CheckRegister` (`api/agent.go:1075`) delegates to `Agent.CheckRegisterOpts` (`api/agent.go:1081`), which constructs an HTTP request via `newRequest`, applies `setQueryOptions`, and sends it via `doRequest`. This is the external-facing API path for programmatic check registration.

2. **Catalog Registration (Server RPC)** — `Catalog.Register` (`agent/consul/catalog_endpoint.go:108`) accepts a `RegisterRequest` containing services and checks, applies `checkPreApply` in a loop to validate each check, uses `ForwardRPC` for cross-datacenter routing, and enforces ACL via `ResolveTokenAndDefaultMeta`. This path registers checks as part of a broader catalog registration that can also create nodes and services.

3. **Connect Proxy TTL Registration** — `RegisterMonitor` (`command/connect/proxy/register.go:34`) registers a connect proxy with the local agent, specifically including a TTL health check. `RegisterMonitor.register` (`command/connect/proxy/register.go:175`) queries the agent to check for existing registration, then registers using `checkID`, `serviceID`, and `serviceName`. The TTL check is maintained by `RegisterMonitor.heartbeat` (`command/connect/proxy/register.go:230`), and cleaned up by `RegisterMonitor.deregister` (`command/connect/proxy/register.go:241`) on `Close`.

4. **Direct Agent Internal Path** — `Agent.AddCheck` (`agent/agent.go:2878`) is the agent's internal method, accepting a `HealthCheck`, `CheckType`, persistence flag, token, and config source. This flows through `Agent.addCheckLocked` (`agent/agent.go:2884`) and `Agent.addCheck` (`agent/agent.go:2931`). Checks can be persisted to disk via `Agent.persistCheck` (`agent/agent.go:2195`). ACL authorization is performed by `Agent.vetCheckRegisterWithAuthorizer` (`agent/acl.go:98`), which distinguishes service-bound checks (`check.ServiceName > 0`) from node-level checks.

5. **Startup Reload Path** — `Agent.loadChecks` (`agent/agent.go:3934`) loads previously persisted check definitions from the configuration and snapshot on agent startup. `Agent.loadCheckState` (`agent/agent.go:3560`) restores saved check state. This ensures checks survive agent restarts.

**Additional Infrastructure Registration (not health checks):**
- `Agent.registerEndpoint` (`agent/agent.go:1661`) registers RPC handlers, not health checks.
- `Server.register*Server` methods (e.g., `registerACLServer`, `registerConfigEntryServer` in `agent/consul/server_grpc.go`) register gRPC service handlers with rate limiting via `Handler.Register` (`agent/consul/rate/handler.go:337`). These are infrastructure registrations, not health check registrations.

**ACL Enforcement:**
All agent-local check registration paths are gated by `Agent.vetCheckRegisterWithAuthorizer` (`agent/acl.go:98`), which checks whether the caller has permission to register the check. Service-bound checks require service-level authorization, while node checks require node-level authorization.

**Unresolved:** The exact body logic of `RegisterMonitor.register` and `Agent.registerEndpoint` (GAPS: drill targets with only 1-line snippets) cannot be fully traced. The `Server.Register` and `registry.register` methods (GAPS: uncovered) may represent additional registration paths not visible in the clue. The HTTP endpoint URL paths used by the API client are not documented in the clue.
