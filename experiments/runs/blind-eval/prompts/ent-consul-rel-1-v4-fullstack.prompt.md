# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-consul-rel-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.


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

--- CLUE FILE START ---
=CC v2.1 consul@HEAD 1527mod 17749sym
? How are the ACL entities related in Consul's ACL documentation?


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

Server.filterACL (agent/consul/acl_server.go:201-201)
  sig: Server.filterACL(token string, subj interface{})
  behavior: DELEGATE(filterACL -> result)
  called_by: GatewayServices, ListNodes, NodeServiceList, NodeServices, ServiceNodes, ListMeshGateways, List, GatewayIntentions

Store.aclAuthMethodDelete (agent/consul/state/acl.go:1689-1689)
  sig: Store.aclAuthMethodDelete(idx uint64, name string, entMeta *acl.EnterpriseMeta)
  behavior: GUARD(err := aclAuthMethodDeleteTxn(tx, idx, name,... -> return err); UNWIND(defer)
  calls: aclAuthMethodDeleteTxn, WriteTxn, Commit, Abort
  called_by: ACLAuthMethodDeleteByName

Store.aclBindingRuleDelete (agent/consul/state/acl.go:1505-1505)
  sig: Store.aclBindingRuleDelete(idx uint64, id string, entMeta *acl.EnterpriseMeta)
  behavior: GUARD(err := aclBindingRuleDeleteTxn(tx, idx, id, e... -> return err); UNWIND(defer)
  calls: aclBindingRuleDeleteTxn, WriteTxn, Commit, Abort
  called_by: ACLBindingRuleDeleteByID

Store.aclPolicyDelete (agent/consul/state/acl.go:1077-1077)
  sig: Store.aclPolicyDelete(idx uint64, value string, fn aclPolicyGetFn, entMeta *ac...)
  behavior: GUARD(err := aclPolicyDeleteTxn(tx, idx, value, fn,... -> return err); UNWIND(defer)
  calls: aclPolicyDeleteTxn, WriteTxn, Commit, Abort
  called_by: ACLPolicyDeleteByID, ACLPolicyDeleteByName

Store.aclRoleDelete (agent/consul/state/acl.go:1350-1350)
  sig: Store.aclRoleDelete(idx uint64, value string, fn aclRoleGetFn, entMeta *acl....)
  behavior: GUARD(err := aclRoleDeleteTxn(tx, idx, value, fn, e... -> return err); UNWIND(defer)
  calls: aclRoleDeleteTxn, WriteTxn, Commit, Abort
  called_by: ACLRoleDeleteByID, ACLRoleDeleteByName

Store.aclTokenDelete (agent/consul/state/acl.go:816-816)
  sig: Store.aclTokenDelete(idx uint64, value, index string, entMeta *acl.Enterprise...)
  behavior: GUARD(err := aclTokenDeleteTxn(tx, idx, value, inde... -> return err); UNWIND(defer)
  calls: aclTokenDeleteTxn, WriteTxn, Commit, Abort
  called_by: ACLTokenDeleteByAccessor

ACL.aclPreCheck (agent/consul/acl_endpoint.go:160-160)
  called_by: AuthMethodDelete, AuthMethodList, AuthMethodRead, AuthMethodSet, Authorize, BindingRuleDelete, BindingRuleList, BindingRuleRead

aclRoleReplicator.Type (agent/consul/acl_replication_types.go:274-274)
  called_by: mergeValue, sanitize, visit, walk, handlePtr, handleQuery, readEntry, decodeAttributeToMessage

aclPolicyReplicator.Type (agent/consul/acl_replication_types.go:138-138)
  called_by: mergeValue, sanitize, visit, walk, handlePtr, handleQuery, readEntry, decodeAttributeToMessage

aclBindingRuleInsert (agent/consul/state/acl.go:1782-1782)
  sig: aclBindingRuleInsert(tx WriteTxn, rule *structs.ACLBindingRule)
  behavior: GUARD(err := tx.Insert(tableACLBindingRules, rule);... -> return fmt.Errorf(...)
  calls: Insert, Errorf
  called_by: ACLBindingRule, aclBindingRuleSetTxn

aclTokenSetTxn (agent/consul/state/acl.go:447-447)
  aclTokenSetTxn is the inner method used to insert an ACL token with the proper indexes into the state store.
  sig: aclTokenSetTxn(tx WriteTxn, idx uint64, token *structs.ACLToken, opts A...)
  behavior: GUARD(token.SecretID == "" -> return ErrMissingAC...); PRECEDENCE(token -> opts); ACCUMULATE(Errorf loop -> result)
  calls: aclTokenInsert, getAuthMethodWithTxn, resolveTokenPolicyLinks, resolveTokenRoleLinks, Errorf
  called_by: ACLBootstrap, ACLTokenBatchSet

aclTokenReplicator.RemoteMeta (agent/consul/acl_replication_types.go:65-65)
  sig: aclTokenReplicator.RemoteMeta(i int)
  called_by: diffACLType

aclTokenReplicator.SingularNoun (agent/consul/acl_replication_types.go:24-24)
  called_by: deleteLocalACLType, replicateACLType, updateLocalACLType

aclPolicyReplicator.SingularNoun (agent/consul/acl_replication_types.go:139-139)
  called_by: deleteLocalACLType, replicateACLType, updateLocalACLType

aclRoleReplicator.DeleteLocalBatch (agent/consul/acl_replication_types.go:360-360)
  sig: aclRoleReplicator.DeleteLocalBatch(srv *Server, batch []string)
  calls: leaderRaftApply
  called_by: deleteLocalACLType

ACL.Authorize (agent/consul/acl_endpoint.go:2192-2192)
  sig: ACL.Authorize(args *structs.RemoteACLAuthorizationRequest, reply *[]st...)
  calls: ResolveToken, aclPreCheck, ForwardRPC

ACL.TokenRead (agent/consul/acl_endpoint.go:266-266)
  sig: ACL.TokenRead(args *structs.ACLTokenGetRequest, reply *structs.ACLToke...)
  calls: aclPreCheck, lookupExpandedTokenInfo, LocalTokensEnabled, filterACLWithAuthorizer, ForwardRPC, ResolveTokenAndDefaultMeta, validateEnterpriseRequest, Errorf
  called_by: TokenExist, assignAgentJoinPolicyToAnonymousToken, getTokenByDescription

aclTokenDeleteTxn (agent/consul/state/acl.go:827-827)
  sig: aclTokenDeleteTxn(tx WriteTxn, idx uint64, value, index string, entMeta *a...)
  behavior: GUARD(err != nil -> return fmt.Errorf("...); PRECEDENCE(err -> token)
  calls: Errorf
  called_by: ACLTokenBatchDelete, aclTokenDelete

aclTokenList (agent/consul/state/acl.go:1724-1724)
  sig: aclTokenList(tx ReadTxn, entMeta *acl.EnterpriseMeta, locality bool)
  behavior: DELEGATE(tx.Get -> result)
  calls: Get
  called_by: ACLTokenListWithParameters

aclTokenReplicator.Type (agent/consul/acl_replication_types.go:23-23)
  called_by: mergeValue, sanitize, visit, walk, handlePtr, handleQuery, readEntry, decodeAttributeToMessage

Server.aclTokenWriter (agent/consul/acl_server.go:217-217)
  behavior: DELEGATE(auth.NewTokenWriter -> result)
  calls: State, InPrimaryDatacenter, LocalTokensEnabled
  called_by: Logout, TokenClone, TokenSet, aclLogin, registerACLServer

aclBindingRuleSetTxn (agent/consul/state/acl.go:1400-1400)
  sig: aclBindingRuleSetTxn(tx WriteTxn, idx uint64, rule *structs.ACLBindingRule)
  behavior: GUARD(rule.ID == "" -> return ErrMissingAC...); PRECEDENCE(rule -> err -> existingRaw)
  calls: aclBindingRuleInsert, Errorf
  called_by: ACLBindingRuleBatchSet, ACLBindingRuleSet

aclPolicyReplicator.PendingUpdateEstimatedSize (agent/consul/acl_replication_types.go:247-247)
  sig: aclPolicyReplicator.PendingUpdateEstimatedSize(i int)
  called_by: updateLocalACLType

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 83 symbols in L3, 27 with behavior annotations
uncovered: aclAuthMethodGetByName, aclAuthMethodInsert, aclAuthMethodList, aclAuthMethodMaxIndex

--- CLUE FILE END ---

QUESTION: How are the ACL entities related in Consul's ACL documentation?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
