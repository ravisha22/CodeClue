# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: ent-consul-rel-2

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.


--- ARCHITECTURAL CONTEXT (LLM-generated, one-time) ---
(See deep context below for consul architecture)
--- END ARCHITECTURAL CONTEXT ---

--- DEEP DOMAIN CONTEXT (LLM-generated from key files, one-time) ---
# Consul deep domain context

## Files reviewed
- `README.md` (first section)
- `main.go`
- `command/registry.go`
- `command/agent/agent.go`
- `agent/agent.go`
- `agent/http.go`
- `agent/http_register.go`
- `agent/agent_endpoint.go`
- `agent/catalog_endpoint.go`
- `agent/health_endpoint.go`
- `agent/kvs_endpoint.go`
- `agent/connect_ca_endpoint.go`
- `agent/service_manager.go`
- `api/catalog.go`
- `api/health.go`
- `api/kv.go`
- `api/connect.go`
- `connect/service.go`
- `connect/resolver.go`

## Product-level framing from the README
Consul presents itself as a distributed, highly available, datacenter-aware control plane for service discovery, health, configuration, and service mesh. The README foregrounds five ideas that show up directly in the code: multi-datacenter operation, service mesh with automatic TLS and identity-based authorization, classic service discovery over DNS/HTTP, health-driven routing, and a dynamic configuration store built on indexed HTTP objects. The codebase mirrors that positioning: the agent is the operational nucleus, while catalog, health, KV, and Connect are exposed as tightly related API families rather than isolated subsystems.

## How the agent starts
The executable path is straightforward but layered. `main.go` builds the CLI shell, and `command/registry.go` registers `consul agent` as the long-running command. `command/agent/agent.go` is the real boot path: it parses config flags, loads configuration through `config.Load`, creates base dependencies with `agent.NewBaseDeps`, constructs the runtime agent with `agent.New`, and then calls `agent.Start(ctx)`. After startup succeeds, it calls `agent.StartSync()` to begin anti-entropy synchronization, then waits on OS signals, retry-join failures, or internal server failure channels.

`agent/agent.go` shows the actual runtime bootstrap sequence. `Agent.Start` first applies auto-config, updates TLS state, starts license management, creates local state (`local.NewState`), and constructs the anti-entropy state syncer (`ae.NewStateSyncer`). It then builds the Consul server/client config and branches on `ServerMode`: servers create a real `consul.Server`, clients create a `consul.Client`, but both are hidden behind the same `delegate` interface. That interface is important: much of the agent code talks to “the cluster” abstractly through RPC, membership, coordinate, snapshot, and ACL-resolution methods without caring whether the local node is a server or client.

After delegate setup, the agent starts a wide set of subsystems in a deliberate order: auto-config monitors, persisted/local services, checks, metadata, the view store, the proxy config manager, local proxy-config sync, service reaping, event handling, coordinate sync, DNS listeners, HTTP listeners, gRPC listeners, xDS session limiting, watches, retry join, telemetry certificate monitoring, and config file watch/reload. The startup sequence makes clear that Consul is not “just an HTTP server”; it is a host-local orchestration process that embeds networking, persistence, cache invalidation, certificate lifecycle, and control-plane streaming.

Two architectural details stand out. First, anti-entropy is central: the local agent maintains state and then reconciles it to the cluster rather than treating every local registration as a direct server mutation. Second, persistence is local and file-backed: directories like `services`, `services/configs`, and `checks/state` under the data dir allow registrations/check state to survive restarts and be replayed during bootstrap.

## Service catalog: registration, persistence, and discovery
There are really two catalog paths.

The first is **agent-local registration**. `agent/agent_endpoint.go` handles `/v1/agent/service/register`. It decodes a `ServiceDefinition`, validates the service, validates/checks sidecar definitions, resolves ACLs, expands `connect.sidecar_service` sugar into a concrete sidecar registration, and converts the payload into `AddServiceRequest`. That request goes into `Agent.AddService`, which acquires the state lock and eventually reaches `addServiceInternal`.

`addServiceInternal` is the core local registration path. It pauses anti-entropy while mutating state, normalizes the service, auto-populates tagged addresses, builds synthetic `HealthCheck` objects from declared check types, restores prior check output/status snapshots where possible, writes the service and checks into local state via `State.AddServiceWithChecks`, launches active check runners, reroutes checks if a proxy exposes them, persists service/service-config/check definitions when appropriate, and optionally removes superseded checks. This is why Consul service registration feels richer than a simple catalog insert: a registration creates runtime behavior, persistent artifacts, and sync obligations.

The second path is **server catalog RPC**. `agent/catalog_endpoint.go` handles `/v1/catalog/*` and mostly acts as an HTTP/RPC facade over `Catalog.*` RPC methods. `CatalogRegister` and `CatalogDeregister` forward writes to servers. Read endpoints (`datacenters`, `nodes`, `services`, `service`, `connect`, `node`, `node-services`, `gateway-services`) layer in Consul-specific query semantics: ACL-aware enterprise metadata, stale-read controls, cache use, retry-once logic when `max_stale` is exceeded, tag filtering, `merge-central-config`, peer/sameness-group handling, and post-processing like address translation and nil-to-empty normalization.

`agent/service_manager.go` adds another important dimension: central service config. When enabled for sidecars/gateways, service registration is not a one-shot local mutation. The `ServiceManager` fetches merged central defaults from cache, composes them with the local service definition, registers the merged result, and then keeps a live cache watch running so central config changes can transparently re-register local services. In other words, the local agent is both a registrar and a materializer of centrally managed defaults.

The public Go client in `api/catalog.go` mirrors this surface almost one-for-one. That package is thin by design: it models payloads and exposes methods like `Register`, `Deregister`, `Services`, `Service`, `Connect`, `Node`, and `GatewayServices`. The deeper semantics live server-side in `agent/*_endpoint.go` and downstream RPC/state layers.

## Health checks as routing truth
Health is both a first-class API and a runtime engine. In `agent/health_endpoint.go`, the HTTP API exposes four principal read shapes: checks by state, by node, by service, and service-node views for direct, Connect, or ingress traffic. The interesting method is `healthServiceNodes`, which toggles `args.Connect` or `args.Ingress`, parses `passing`, `tag`, `peer-name`, `sameness-group`, and `merge-central-config`, and then delegates to `rpcClientHealth.ServiceNodes`. That means health-backed discovery is not just catalog plus filtering; it has its own client path optimized for service-node resolution.

The check execution model lives in `agent/agent.go` and is extensive. `AddCheck`/`addCheck` translate a logical check definition into a running checker instance. Consul supports TTL, HTTP, TCP, UDP, gRPC, Docker, OS service, monitor/script, H2PING, and alias checks. Each check type is backed by a concrete runner from `agent/checks`, with shared status handling and guardrails like minimum intervals, output size limits, TLS config injection, and proxy-aware address rewriting for exposed checks. TTL checks restore persisted state on restart, alias checks resolve target service/node health through RPC, and checks with `DeregisterCriticalServiceAfter` feed the service reaper. This explains why health is deeply entangled with service lifecycle: failing checks can actively cause deregistration, not just annotate state.

`api/health.go` shows the client-side conceptual model. `HealthCheck` exposes both execution details and status, `AggregatedStatus` collapses multiple checks into maintenance/critical/warning/passing, and the `Health` client offers `Node`, `Checks`, `Service`, `Connect`, and `Ingress`. The split between `Service` and `Connect` is semantically important: Connect discovery is about healthy mTLS-reachable endpoints, potentially sidecars or native Connect services, not simply healthy application ports.

## KV store: simple surface, nuanced semantics
The KV API in `agent/kvs_endpoint.go` is deceptively small but carefully engineered. The handler sanitizes the path with `path.Clean` while preserving trailing slashes for directory semantics, validates keys unless `DisableKVKeyValidation` is set, and then dispatches by method.

Read operations support single-key get, recursive prefix list, key-only listing, and raw mode. Raw mode deliberately hardens the HTTP response with `Content-Type: text/plain`, `X-Content-Type-Options: nosniff`, and `Content-Security-Policy: sandbox` to reduce XSS risk from arbitrary stored values. Write operations support plain set, CAS (`cas`), session-based lock acquire/release (`acquire`/`release`), custom flags, and request-body size enforcement through `KVMaxValueSize`. Delete operations support single delete, recursive subtree delete, and delete-CAS.

The key thing is that KV is not only a configuration map; it is also a lightweight concurrency primitive. `api/kv.go` makes that explicit by exposing `Put`, `CAS`, `Acquire`, `Release`, `DeleteCAS`, and `DeleteTree`. `ModifyIndex` is reused both for optimistic concurrency and for blocking query progression. Sessions are therefore part of the KV story because lock semantics piggyback on them. The server API returns booleans for CAS/lock style operations rather than hiding conflict, preserving coordination semantics for clients.

## Connect/service mesh patterns
Connect appears in three layers.

At the agent control-plane layer, `Agent.Start` wires up the proxy config manager, local proxy sync, xDS server, leaf certificate manager usage, and optional server certificate manager for peering-enabled server nodes. `configureXDSServer` wraps a local proxy watcher with a catalog-backed config source when a server is present, which is a strong hint that Consul’s mesh is not bolted on; it is integrated into the agent’s combined local-state plus catalog-state model.

At the HTTP API layer, `agent/http_register.go` exposes both global Connect endpoints (`/v1/connect/ca/*`, intentions) and agent-scoped Connect endpoints (`/v1/agent/connect/ca/roots`, `/leaf/<service>`, `/authorize`). `agent/connect_ca_endpoint.go` serves CA roots and CA configuration. `AgentConnectCALeafCert` in `agent_endpoint.go` returns per-service leaf bundles, supports blocking queries, and forces revalidation on non-blocking fetches so stale or invalid leaf certs are not returned casually. `AgentConnectAuthorize` is the authorization hook for service-to-service connection checks and explicitly notes that L7 intentions are treated as deny in this path.

At the application SDK layer, `connect/service.go` is the clearest expression of Connect’s runtime contract. A `connect.Service` watches both roots and leaf certs via watch plans, maintains a dynamic TLS config, exposes `ServerTLSConfig()` for inbound verification and `Dial()`/`HTTPClient()` for outbound mTLS dialing, and treats readiness/cert availability as part of service health semantics. `connect/resolver.go` shows how discovery composes with health: the standard resolver calls `Health.Connect(..., passingOnly=true)` and synthesizes a SPIFFE-like service identity (`SpiffeIDService`) from the returned entry. That captures the mental model for Connect: discover healthy Connect-capable endpoints, obtain the expected identity, then enforce it at the TLS layer.

## HTTP API surface and code organization
The API surface is centrally declared in `agent/http_register.go`. That file is effectively the public HTTP routing table for the agent: ACL, agent, catalog, config, connect, coordinate, discovery chain, event, health, KV, operator, peering, prepared query, session, status, snapshot, and txn endpoints all register there. `agent/http.go` then provides the execution shell around those handlers: endpoint lookup, allowed-method enforcement, request metrics, gzip behavior, pprof protection, ACL integration, and reload-aware handler memoization.

A useful mental model for the repo is: `agent/` contains the server-side HTTP façade and runtime orchestration, while `api/` contains the consumer-facing Go client for that façade. They intentionally mirror one another, but the rich behavior usually lives under `agent/`.

## Bottom line
Consul’s agent is the control-plane kernel. Service registration is not just metadata insertion; it creates local runtime state, active health executors, persistence artifacts, and anti-entropy obligations. Catalog reads are RPC-backed, cache-aware, and discovery-oriented. Health is the routing truth layer. KV combines configuration storage with indexing, CAS, and session-backed lock semantics. Connect extends the same agent with certificate issuance, identity verification, and proxy/xDS orchestration rather than introducing a separate mesh daemon.

--- END DEEP DOMAIN CONTEXT ---

--- CLUE FILE (File 1) ---
=CC v2.1 consul@HEAD 1527mod 17749sym
? What documented paths can register checks in Consul?


-- README
<h1> <img src="./ui/logo.svg" align="left" height="46px" alt="Consul logo"/>
sections: Quick Start, Documentation, Contributing

-- TREE
acl/  (20 files)
agent/  (716 files)
api/  (55 files)
command/  (193 files)
connect/  (10 files)
envoyextensions/  (9 files)
grpcmocks/  (26 files)
internal/  (164 files)
ipaddr/  (2 files)
lib/  (28 files)
logging/  (13 files)
proto/  (70 files)
proto-public/  (68 files)
sdk/  (25 files)
sentinel/  (3 files)
service_os/  (2 files)
snapshot/  (2 files)
test/  (39 files)
test-integ/  (10 files)
testing/  (47 files)
testrpc/  (1 files)
tlsutil/  (3 files)
tools/  (1 files)
troubleshoot/  (12 files)
types/  (4 files)
ui/  (3 files)
version/  (3 files)

-- INDEX
proto/private/pbconfigentry/config_entry.pb.go  9779L  GetDefaults, GetHash, GetListeners, GetMeta, GetStatus
agent/structs/structs.deepcopy.go              1469L  DeepCopy, DeepCopy, DeepCopy, DeepCopy, DeepCopy
proto-public/pbresource/resource_deepcopy.gen.go   573L  DeepCopy, DeepCopyInterface, DeepCopyInto, DeepCopy, DeepCopyInterface
agent/config/flagset.go                         203L  Get, IsBoolFlag, Set, String, boolPtrValue
internal/controller/controller.go               361L  String, WithBackoff, WithCustomWatch, WithForceReconcileEvery, WithInitializer
agent/structs/structs_ce.go                     185L  String, DefaultEnterpriseMetaInDefaultPartition, DefaultEnterpriseMetaInPartition, EnterpriseServiceUsage, HasWildcardDestination
proto/private/pbsubscribe/subscribe.pb.go      1079L  Enum, Number, String, GetConfigEntry, GetOp
agent/submatview/rpc_materializer.go            128L  NewRPCMaterializer, Query, Run, reset, subscribeOnce
agent/consul/controller/reconciler.go            66L  Reconciler, Key, Request, RequeueAfter, Error
agent/structs/structs.go                       3354L  CensusRequest, NamespaceOrDefault, PartitionOrDefault, StringHashMD5, StringHashSHA256
agent/consul/stream/string_types.go              14L  String, String
proto-public/annotations/ratelimit/ratelimit.pb.go   318L  Enum, Number, String, Enum, Number
proto-public/pbdataplane/dataplane.pb.go        647L  GetFeatureName, GetSupported, ProtoReflect, Reset, String
types/tls.go                                    231L  MarshalEnvoyTLSCipherSuiteStrings, String, LessThan, String, TLSVersions
  ...and 1513 more modules

-- SYM
GRPCLogger.Errorf                   M logging/grpc.go:74     Errorf implements grpclog.LoggerV2
Client.doRequest                    M api/api.go:1085   doRequest runs a request with our client
Client.newRequest                   M api/api.go:1053   newRequest is used to create a new request
durToMsec                           M api/api.go:940    durToMsec converts a duration to a millisecond ...
ConstError.Error                    M internal/resource/errors.go:41     function ConstError.Error
txn.Get                             M internal/controller/cache/index/txn.go:19     function txn.Get
Mutex.Unlock                        M lib/mutex/mutex.go:28     function Mutex.Unlock
Mutex.Lock                          M lib/mutex/mutex.go:24     function Mutex.Lock
Lock.Lock                           M api/lock.go:138    Lock attempts to acquire the lock and blocks wh...
Lock.Unlock                         M api/lock.go:268    Unlock released the lock.
request.setQueryOptions             M api/api.go:843    setQueryOptions is used to annotate the request...
txn.getRaw                          M internal/controller/cache/index/txn.go:28     function txn.getRaw
ChainedAuthorizer.executeChain      M acl/chained_authorizer.go:29     function ChainedAuthorizer.executeChain
request.toHTTP                      M api/api.go:999    toHTTP converts the request to an HTTP request
request.toHTTP                      M command/resource/client/client.go:846    toHTTP converts the request to an HTTP request
GRPCLogger.Error                    M logging/grpc.go:64     Error implements grpclog.LoggerV2
ecsNotGlobalError.Error             M agent/dns.go:717    function ecsNotGlobalError.Error
APIGatewayListener.DeepCopy         M agent/structs/structs.deepcopy.go:11     DeepCopy generates a deep copy of *APIGatewayLi...
ACLRemoteError.Error                M agent/consul/acl.go:126    function ACLRemoteError.Error
caStateError.Error                  M agent/consul/leader_connect_ca.go:193    function caStateError.Error
errPeeringInvalidServerAddress.Error M agent/rpc/peering/service.go:62     Error implements the error interface
ProviderLoginFailedError.Error      M internal/go-sso/oidcauth/oidc.go:186    function ProviderLoginFailedError.Error
MethodNotAllowedError.Error         M agent/http.go:66     function MethodNotAllowedError.Error
PermissionDeniedError.Error         M acl/errors.go:88     Initially we may not have attribution informati...
enterpriseConfigKeyError.Error      M agent/config/builder_ce.go:74     function enterpriseConfigKeyError.Error
invalidCSRError.Error               M agent/connect/csr.go:145    function invalidCSRError.Error
RequeueAfterError.Error             M agent/consul/controller/reconciler.go:42     Error implements the error interface.
UnsupportedFSMApplyPanicError.Error M agent/consul/state/txn.go:22     function UnsupportedFSMApplyPanicError.Error
CodeWithPayloadError.Error          M agent/http.go:78     function CodeWithPayloadError.Error
HTTPError.Error                     M agent/http.go:89     function HTTPError.Error
terminalError.Error                 M agent/proxycfg/data_sources.go:42     function terminalError.Error
TxnError.Error                      M agent/structs/txn.go:131    Error returns the string representation of an a...
resetErr.Error                      M agent/submatview/rpc_materializer.go:116    Error implements error
StatusError.Error                   M api/api.go:107    function StatusError.Error
startupLogger.Error                 M command/agent/startup_logger.go:62     function startupLogger.Error
StatusError.Error                   M command/resource/client/client.go:94     function StatusError.Error
DuplicateIndexError.Error           M internal/controller/cache/errors.go:63     function DuplicateIndexError.Error
DuplicateQueryError.Error           M internal/controller/cache/errors.go:71     function DuplicateQueryError.Error
IndexNotFoundError.Error            M internal/controller/cache/errors.go:29     function IndexNotFoundError.Error
QueryNotFoundError.Error            M internal/controller/cache/errors.go:21     function QueryNotFoundError.Error
MissingRequiredIndexError.Error     M internal/controller/cache/index/errors.go:14     function MissingRequiredIndexError.Error
RequeueAfterError.Error             M internal/controller/controller.go:317    Error implements the error interface.
TokenVerificationFailedError.Error  M internal/go-sso/oidcauth/oidc.go:203    function TokenVerificationFailedError.Error
ErrDataParse.Error                  M internal/resource/errors.go:57     function ErrDataParse.Error
ErrInvalidField.Error               M internal/resource/errors.go:70     function ErrInvalidField.Error
ErrInvalidFields.Error              M internal/resource/errors.go:174    function ErrInvalidFields.Error
ErrInvalidListElement.Error         M internal/resource/errors.go:84     function ErrInvalidListElement.Error
ErrInvalidMapKey.Error              M internal/resource/errors.go:112    function ErrInvalidMapKey.Error
ErrInvalidMapValue.Error            M internal/resource/errors.go:98     function ErrInvalidMapValue.Error
ErrInvalidReferenceType.Error       M internal/resource/errors.go:165    function ErrInvalidReferenceType.Error
ErrOwnerTenantInvalid.Error         M internal/resource/errors.go:139    function ErrOwnerTenantInvalid.Error
ErrOwnerTypeInvalid.Error           M internal/resource/errors.go:125    function ErrOwnerTypeInvalid.Error
GroupVersionMismatchError.Error     M internal/storage/storage.go:316    Error implements the error interface.
TargetedUI.Error                    M command/exec/exec.go:683    function TargetedUI.Error
policyOrRoleTokenError.Error        M agent/consul/acl.go:155    function policyOrRoleTokenError.Error
ConfigEntryGraphError.Error         M agent/structs/config_entry_discoverychain.go:2019   function ConfigEntryGraphError.Error
TxnResponse.Error                   M agent/structs/txn.go:157    Error returns an aggregate of all errors in thi...
CacheTypeError.Error                M internal/controller/cache/errors.go:38     function CacheTypeError.Error
IndexError.Error                    M internal/controller/cache/errors.go:51     function IndexError.Error
IsEnterpriseData                    M agent/consul/fsm/decode_downgrade.go:17     function IsEnterpriseData
  ...and 16346 more symbols

-- FOCUS
ui/package.json (ui/package.json:1-69)
  Config summary for ui/package.json: deps: doctoc, license-checker, npm-run-all
  deps: doctoc, license-checker, npm-run-all

ui/packages/consul-ui/lib/block-slots/package.json (ui/packages/consul-ui/lib/block-slots/package.json:1-11)
  Config summary for ui/packages/consul-ui/lib/block-slots/package.json: deps: ember-cli-htmlbars, ember-cli-babel
  deps: ember-cli-htmlbars, ember-cli-babel

ui/packages/consul-ui/package.json (ui/packages/consul-ui/package.json:1-217)
  Config summary for ui/packages/consul-ui/package.json: deps: @babel/core, @babel/eslint-parser, @babel/plugin-proposal-decorators, @babel/plugin-transform-class-properties, @docfy/ember, @docfy/ember-cli, @ember-data/adapter, @ember-data/legacy-compat
  deps: @babel/core, @babel/eslint-parser, @babel/plugin-proposal-decorators, @babel/plugin-transform-class-properties, @docfy/ember, @docfy/ember-cli

RegisterMonitor.register (command/connect/proxy/register.go:175-175)
  register queries the Consul agent to determine if we've already registered.
  behavior: PRECEDENCE(err -> currentService)
  calls: checkID, serviceID, serviceName
  called_by: Register, Run

RegisterMonitor (command/connect/proxy/register.go:34-34)
  RegisterMonitor registers the proxy with the local Consul agent with a TTL health check that is kept alive.
  methods: Close, Run, checkID, deregister, heartbeat, register

Agent.registerEndpoint (agent/agent.go:1661-1661)
  registerEndpoint registers a handler for the consul RPC server under a unique name while making it accessible under the 
  sig: Agent.registerEndpoint(name string, handler interface{})
  calls: RegisterEndpoint
  raises: panic

Server.registerOperatorServer (agent/consul/server_grpc.go:443-443)
  sig: Server.registerOperatorServer(config *Config, deps Deps, registrars ...grpc.ServiceReg...)
  behavior: ACCUMULATE(Register loop -> result)
  calls: Register, ForwardGRPC, Errorf
  called_by: setupGRPCServices

Agent.CheckRegister (api/agent.go:1075-1075)
  CheckRegister is used to register a new check with the local agent
  sig: Agent.CheckRegister(check *AgentCheckRegistration)
  behavior: DELEGATE(a.CheckRegisterOpts -> result)
  calls: CheckRegisterOpts

CheckServiceNode.GetChecks (proto/private/pbservice/node.pb.go:136-136)
  behavior: GUARD(x != nil -> return x.Checks)

Server.registerACLServer (agent/consul/server_grpc.go:356-356)
  sig: Server.registerACLServer(registrars ...grpc.ServiceRegistrar)
  behavior: ACCUMULATE(Register loop -> result)
  calls: InPrimaryDatacenter, aclLogin, aclTokenWriter, loadAuthMethod, Register, ForwardGRPC
  called_by: setupGRPCServices

Server.registerConfigEntryServer (agent/consul/server_grpc.go:526-526)
  sig: Server.registerConfigEntryServer(registrars ...grpc.ServiceRegistrar)
  behavior: ACCUMULATE(Register loop -> result)
  calls: Register, ForwardGRPC
  called_by: setupGRPCServices

Server.registerConnectCAServer (agent/consul/server_grpc.go:477-477)
  sig: Server.registerConnectCAServer(registrars ...grpc.ServiceRegistrar)
  behavior: ACCUMULATE(Register loop -> result)
  calls: Register, ForwardGRPC, FSM
  called_by: setupGRPCServices

Server.registerDataplaneServer (agent/consul/server_grpc.go:497-497)
  sig: Server.registerDataplaneServer(registrars ...grpc.ServiceRegistrar)
  behavior: ACCUMULATE(Register loop -> result)
  calls: Register, FSM
  called_by: setupGRPCServices

Server.registerPeerStreamServer (agent/consul/server_grpc.go:381-381)
  sig: Server.registerPeerStreamServer(config *Config, registrars ...grpc.ServiceRegistrar)
  behavior: GUARD(s.peeringBackend == nil -> panic("peeringBacke...); ACCUMULATE(Register loop -> result)
  calls: Register, ForwardGRPC, FSM, Errorf
  called_by: setupGRPCServices
  raises: panic

Server.registerPeeringServer (agent/consul/server_grpc.go:409-409)
  sig: Server.registerPeeringServer(config *Config, registrars ...grpc.ServiceRegistrar)
  behavior: GUARD(s.peeringBackend == nil -> panic("peeringBacke...); PRECEDENCE(s); ACCUMULATE(Register loop -> result)
  calls: Register, ForwardGRPC, Errorf
  called_by: setupGRPCServices
  raises: panic

Server.registerResourceServiceServer (agent/consul/server_grpc.go:339-339)
  sig: Server.registerResourceServiceServer(typeRegistry resource.Registry, resolver resourcegrpc.AC...)
  behavior: GUARD(s.storageBackend == nil -> return fmt.Errorf("...); ACCUMULATE(RegisterResourceServi... -> result)
  calls: newResourceServiceConfig, Errorf
  called_by: setupGRPCServices

Server.registerServerDiscoveryServer (agent/consul/server_grpc.go:512-512)
  sig: Server.registerServerDiscoveryServer(resolver serverdiscovery.ACLResolver, registrars ...grpc...)
  behavior: ACCUMULATE(Register loop -> result)
  calls: Register
  called_by: setupGRPCServices

Server.registerStreamSubscriptionServer (agent/consul/server_grpc.go:464-464)
  sig: Server.registerStreamSubscriptionServer(deps Deps, registrars ...grpc.ServiceRegistrar)
  behavior: ACCUMULATE(RegisterStateChangeSu... -> result)
  called_by: setupGRPCServices

getNodeAndChecks (agent/consul/state/catalog_events.go:679-679)
  getNodeAndNodeChecks returns a the node structure and a function that returns the full list of checks for a specific ser
  sig: getNodeAndChecks(tx ReadTxn, node string, entMeta *acl.EnterpriseMeta, pe...)
  behavior: GUARD(err != nil -> return nil, nil, err); PRECEDENCE(err -> nodeRaw); ACCUMULATE(loop -> nodeChecks check)
  calls: Get
  called_by: newServiceHealthEventForService, newServiceHealthEventsForNode

MockRequestLimitsHandler.Register (agent/consul/rate/mock_RequestLimitsHandler.go:32-32)
  Register provides a mock function with given fields: serversStatusProvider
  sig: MockRequestLimitsHandler.Register(serversStatusProvider ServersStatusProvider)
  called_by: registerACLServer, registerConfigEntryServer, registerConnectCAServer, registerDataplaneServer, registerOperatorServer, registerPeerStreamServer, registerPeeringServer, registerServerDiscoveryServer

Catalog.Register (agent/consul/catalog_endpoint.go:108-108)
  Register a service and/or check(s) in a node, creating the node if it doesn't exist.
  sig: Catalog.Register(args *structs.RegisterRequest, reply *struct{})
  behavior: GUARD(!c.srv.config.PeeringTestAllowPeerRegistratio... -> return fmt.Errorf(...); PRECEDENCE(not_c.srv.config.PeeringTestAllo -> done -> err); ACCUMULATE(checkPreApply loop -> result)
  calls: State, ForwardRPC, NodeServices, checkPreApply, hasPeerNameInRequest, nodePreApply, servicePreApply, ResolveTokenAndDefaultMeta
  called_by: registerACLServer, registerConfigEntryServer, registerConnectCAServer, registerDataplaneServer, registerOperatorServer, registerPeerStreamServer, registerPeeringServer, registerServerDiscoveryServer

Handler.Register (agent/consul/rate/handler.go:337-337)
  sig: Handler.Register(serversStatusProvider ServersStatusProvider)
  called_by: Allow, registerACLServer, registerConfigEntryServer, registerConnectCAServer, registerDataplaneServer, registerOperatorServer, registerPeerStreamServer, registerPeeringServer

Agent.CheckRegisterOpts (api/agent.go:1081-1081)
  CheckRegisterOpts is used to register a new check with the local agent using query options
  sig: Agent.CheckRegisterOpts(check *AgentCheckRegistration, q *QueryOptions)
  behavior: GUARD(err != nil -> return err); PRECEDENCE(err); UNWIND(defer)
  calls: doRequest, newRequest, setQueryOptions
  called_by: CheckRegister

Agent.vetCheckRegisterWithAuthorizer (agent/acl.go:98-98)
  sig: Agent.vetCheckRegisterWithAuthorizer(authz acl.Authorizer, check *structs.HealthCheck)
  behavior: GUARD(len(check.ServiceName) > 0 -> return err); PRECEDENCE(len -> existing)
  calls: AgentEnterpriseMeta

CheckAlias.processChecks (agent/checks/alias.go:259-259)
  processChecks is a common helper for taking a set of health checks and using them to update our alias.
  sig: CheckAlias.processChecks(checks []*structs.HealthCheck, CheckIfServiceIDExists Ch...)
  behavior: ACCUMULATE(EqualFold loop -> result)
  calls: CompoundServiceID
  called_by: runLocal, runQuery

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 83 symbols in L3, 45 with behavior annotations
uncovered: registry.register, MockRegistry.Register, Server.Register, V1ConsulRegistrator.HandleFailedMember
drill: command/connect/proxy/register.go (~1 lines, RegisterMonitor.register)
drill: agent/agent.go (~1 lines, Agent.registerEndpoint)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## RegisterMonitor.register  (command/connect/proxy/register.go L175-175)
```
func (r *RegisterMonitor) register() {
```

## Agent.registerEndpoint  (agent/agent.go L1661-1661)
```
func (a *Agent) registerEndpoint(name string, handler interface{}) error {
```

## serviceName  (agent/consul/fsm/decode_downgrade.go L471-471)
```
	type serviceName struct {
```

## NewRegisterMonitor  (command/connect/proxy/register.go L92-92)
```
func NewRegisterMonitor(logger hclog.Logger) *RegisterMonitor {
```

## RegisterMonitor.Close  (command/connect/proxy/register.go L258-258)
```
func (r *RegisterMonitor) Close() error {
```

## RegisterMonitor.Run  (command/connect/proxy/register.go L110-110)
```
func (r *RegisterMonitor) Run() {
```

## RegisterMonitor.checkID  (command/connect/proxy/register.go L305-305)
```
func (r *RegisterMonitor) checkID() string {
```

## RegisterMonitor.deregister  (command/connect/proxy/register.go L241-241)
```
func (r *RegisterMonitor) deregister() {
```

## RegisterMonitor.heartbeat  (command/connect/proxy/register.go L230-230)
```
func (r *RegisterMonitor) heartbeat() {
```

## RegisterMonitor.serviceID  (command/connect/proxy/register.go L290-290)
```
func (r *RegisterMonitor) serviceID() string {
```

## RegisterMonitor.serviceName  (command/connect/proxy/register.go L300-300)
```
func (r *RegisterMonitor) serviceName() string {
```

## RegisterMonitor  (command/connect/proxy/register.go L34-34)
```
type RegisterMonitor struct {
```

## AddServiceRequest  (agent/agent.go L2418-2418)
```
type AddServiceRequest struct {
```

## Agent.AddCheck  (agent/agent.go L2878-2878)
```
func (a *Agent) AddCheck(check *structs.HealthCheck, chkType *structs.CheckType, persist bool, token string, source configSource) error {
```

## Agent.AddService  (agent/agent.go L2349-2349)
```
func (a *Agent) AddService(req AddServiceRequest) error {
```

## Agent.AdvertiseAddrLAN  (agent/agent.go L3444-3444)
```
func (a *Agent) AdvertiseAddrLAN() string {
```

## Agent.AgentLocalMember  (agent/agent.go L1937-1937)
```
func (a *Agent) AgentLocalMember() serf.Member {
```

## Agent.AutoReloadConfig  (agent/agent.go L4191-4191)
```
func (a *Agent) AutoReloadConfig() error {
```

## Agent.DisableNodeMaintenance  (api/agent.go L1329-1329)
```
func (a *Agent) DisableNodeMaintenance() error {
```

## Agent.DisableServiceMaintenance  (api/agent.go L1291-1291)
```
func (a *Agent) DisableServiceMaintenance(serviceID string) error {
```

## Agent.EnableNodeMaintenance  (api/agent.go L1312-1312)
```
func (a *Agent) EnableNodeMaintenance(reason string) error {
```

## Agent.EnableServiceMaintenance  (api/agent.go L1269-1269)
```
func (a *Agent) EnableServiceMaintenance(serviceID, reason string) error {
```

## Agent.Failed  (agent/agent.go L933-933)
```
func (a *Agent) Failed() <-chan struct{} {
```

## Agent.ForceLeave  (api/agent.go L1160-1160)
```
func (a *Agent) ForceLeave(node string) error {
```

## Agent.ForceLeaveWAN  (agent/agent.go L1918-1918)
```
func (a *Agent) ForceLeaveWAN(node string, prune bool, entMeta *acl.EnterpriseMeta) error {
```

## Agent.GetConfig  (agent/agent.go L574-574)
```
func (a *Agent) GetConfig() *config.RuntimeConfig {
```

## Agent.GetLANCoordinate  (agent/agent.go L2024-2024)
```
func (a *Agent) GetLANCoordinate() (librtt.CoordinateSet, error) {
```

## Agent.JoinLAN  (agent/agent.go L1837-1837)
```
func (a *Agent) JoinLAN(addrs []string, entMeta *acl.EnterpriseMeta) (n int, err error) {
```

## Agent.JoinWAN  (agent/agent.go L1857-1857)
```
func (a *Agent) JoinWAN(addrs []string) (n int, err error) {
```

## Agent.LANMembers  (agent/agent.go L1954-1954)
```
func (a *Agent) LANMembers(f consul.LANMemberFilter) ([]serf.Member, error) {
```

## Agent.LANMembersInAgentPartition  (agent/agent.go L1943-1943)
```
func (a *Agent) LANMembersInAgentPartition() []serf.Member {
```

## Agent.Leave  (api/agent.go L1137-1137)
```
func (a *Agent) Leave() error {
```

## Agent.LocalState  (agent/agent.go L4527-4527)
```
func (a *Agent) LocalState() *local.State {
```

## Agent.PauseSync  (agent/agent.go L1976-1976)
```
func (a *Agent) PauseSync() {
```

## Agent.PickRandomMeshGatewaySuitableForDialing  (agent/agent.go L1886-1886)
```
func (a *Agent) PickRandomMeshGatewaySuitableForDialing(dc string) string {
```

## Agent.PrimaryMeshGatewayAddressesReadyCh  (agent/agent.go L1878-1878)
```
func (a *Agent) PrimaryMeshGatewayAddressesReadyCh() <-chan struct{} {
```

## Agent.RPC  (agent/agent.go L1675-1675)
```
func (a *Agent) RPC(ctx context.Context, method string, args interface{}, reply interface{}) error {
```

## Agent.RefreshPrimaryGatewayFallbackAddresses  (agent/agent.go L1895-1895)
```
func (a *Agent) RefreshPrimaryGatewayFallbackAddresses(addrs []string) error {
```

## Agent.ReloadConfig  (agent/agent.go L4195-4195)
```
func (a *Agent) ReloadConfig() error {
```

## Agent.RemoveCheck  (agent/agent.go L3373-3373)
```
func (a *Agent) RemoveCheck(checkID structs.CheckID, persist bool) error {
```

## Agent.RemoveService  (agent/agent.go L2787-2787)
```
func (a *Agent) RemoveService(serviceID structs.ServiceID) error {
```

## Agent.ResumeSync  (agent/agent.go L1989-1989)
```
func (a *Agent) ResumeSync() {
```

## Agent.RetryJoinCh  (agent/agent.go L1826-1826)
```
func (a *Agent) RetryJoinCh() <-chan error {
```

## Agent.ServiceHTTPBasedChecks  (agent/agent.go L3425-3425)
```
func (a *Agent) ServiceHTTPBasedChecks(serviceID structs.ServiceID) []structs.CheckType {
```

## Agent.ShutdownAgent  (agent/agent.go L1707-1707)
```
func (a *Agent) ShutdownAgent() error {
```

## Agent.ShutdownCh  (agent/agent.go L1832-1832)
```
func (a *Agent) ShutdownCh() <-chan struct{} {
```

## Agent.ShutdownEndpoints  (agent/agent.go L1805-1805)
```
func (a *Agent) ShutdownEndpoints() {
```

## Agent.Start  (agent/agent.go L600-600)
```
func (a *Agent) Start(ctx context.Context) error {
```

## Agent.StartSync  (agent/agent.go L1968-1968)
```
func (a *Agent) StartSync() {
```

## Agent.Stats  (agent/agent.go L3619-3619)
```
func (a *Agent) Stats() map[string]map[string]string {
```

## Agent.SyncPausedCh  (agent/agent.go L2016-2016)
```
func (a *Agent) SyncPausedCh() <-chan struct{} {
```

## Agent.WANMembers  (agent/agent.go L1959-1959)
```
func (a *Agent) WANMembers() []serf.Member {
```

## Agent.addCheck  (agent/agent.go L2931-2931)
```
func (a *Agent) addCheck(check *structs.HealthCheck, chkType *structs.CheckType, service *structs.NodeService, token string, source configSource) error {
```

## Agent.addCheckLocked  (agent/agent.go L2884-2884)
```
func (a *Agent) addCheckLocked(check *structs.HealthCheck, chkType *structs.CheckType, persist bool, token string, source configSource) error {
```

## Agent.addServiceInternal  (agent/agent.go L2443-2443)
```
func (a *Agent) addServiceInternal(req addServiceInternalRequest) error {
```

## Agent.addServiceLocked  (agent/agent.go L2363-2363)
```
func (a *Agent) addServiceLocked(req addServiceLockedRequest) error {
```

## Agent.cancelCheckMonitors  (agent/agent.go L3448-3448)
```
func (a *Agent) cancelCheckMonitors(checkID structs.CheckID) {
```

## Agent.checkServerLastSeen  (agent/agent.go L4734-4734)
```
func (a *Agent) checkServerLastSeen(readFn consul.ServerMetadataReadFunc) error {
```

## Agent.cleanupRegistration  (agent/agent.go L2743-2743)
```
func (a *Agent) cleanupRegistration(serviceIDs []structs.ServiceID, checksIDs []structs.CheckID) {
```

## Agent.configureXDSServer  (agent/agent.go L940-940)
```
func (a *Agent) configureXDSServer(proxyWatcher xds.ProxyWatcher, server *consul.Server) {
```

## Agent.deletePid  (agent/agent.go L3678-3678)
```
func (a *Agent) deletePid() error {
```

## Agent.getRuntimeConfigForDisplay  (agent/agent.go L4390-4390)
```
func (a *Agent) getRuntimeConfigForDisplay() *config.RuntimeConfig {
```

## Agent.getTokenFunc  (agent/agent.go L4804-4804)
```
func (a *Agent) getTokenFunc() func() string {
```

## Agent.listenAndServeDNS  (agent/agent.go L1028-1028)
```
func (a *Agent) listenAndServeDNS() error {
```

## Agent.listenAndServeGRPC  (agent/agent.go L971-971)
```
func (a *Agent) listenAndServeGRPC(server *consul.Server) error {
```

## Agent.listenHTTP  (agent/agent.go L1136-1136)
```
func (a *Agent) listenHTTP() ([]apiServer, error) {
```

## Agent.listenSocket  (agent/agent.go L1252-1252)
```
func (a *Agent) listenSocket(path string) (net.Listener, error) {
```

## Agent.listenerPortLocked  (agent/agent.go L4590-4590)
```
func (a *Agent) listenerPortLocked(svcID structs.ServiceID, checkID structs.CheckID) (int, error) {
```

## Agent.loadCheckState  (agent/agent.go L3560-3560)
```
func (a *Agent) loadCheckState(check *structs.HealthCheck) error {
```

## Agent.loadChecks  (agent/agent.go L3934-3934)
```
func (a *Agent) loadChecks(conf *config.RuntimeConfig, snap map[structs.CheckID]*structs.HealthCheck) error {
```

## Agent.loadMetadata  (agent/agent.go L4078-4078)
```
func (a *Agent) loadMetadata(conf *config.RuntimeConfig) error {
```

## Agent.loadServices  (agent/agent.go L3703-3703)
```
func (a *Agent) loadServices(conf *config.RuntimeConfig, snap map[structs.CheckID]*structs.HealthCheck) error {
```

## Agent.makeServiceConfigFilePath  (agent/agent.go L2233-2233)
```
func (a *Agent) makeServiceConfigFilePath(serviceID structs.ServiceID) string {
```

## Agent.makeServiceFilePath  (agent/agent.go L2161-2161)
```
func (a *Agent) makeServiceFilePath(svcID structs.ServiceID) string {
```

## Agent.persistCheck  (agent/agent.go L2195-2195)
```
func (a *Agent) persistCheck(check *structs.HealthCheck, chkType *structs.CheckType, source configSource) error {
```

## Agent.persistCheckState  (agent/agent.go L3520-3520)
```
func (a *Agent) persistCheckState(check *checks.CheckTTL, status, output string) error {
```

## Agent.persistServerMetadata  (agent/agent.go L4685-4685)
```
func (a *Agent) persistServerMetadata() {
```

## Agent.persistService  (agent/agent.go L2166-2166)
```
func (a *Agent) persistService(service *structs.NodeService, source configSource, disableSidecarDefaultChecks bool) error {
```

## Agent.persistServiceConfig  (agent/agent.go L2237-2237)
```
func (a *Agent) persistServiceConfig(serviceID structs.ServiceID, defaults *structs.ServiceConfigResponse) error {
```
--- END SOURCE SNIPPETS ---

QUESTION: What documented paths can register checks in Consul?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
