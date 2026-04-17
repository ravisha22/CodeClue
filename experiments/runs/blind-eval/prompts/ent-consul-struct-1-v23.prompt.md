# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-consul-struct-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 consul@HEAD 1527mod 17749sym
? According to the docs, how is Consul's service mesh split between control plane and data plane?


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

PeeringBackend.PeerThroughMeshGateways (agent/consul/peering_backend.go:183-183)
  PeerThroughMeshGateways determines if the config entry to enable peering control plane traffic through a mesh gateway is
  sig: PeeringBackend.PeerThroughMeshGateways(ws memdb.WatchSet)
  behavior: GUARD(err != nil -> return false, fmt.E...); PRECEDENCE(err -> rawEntry)
  calls: State, Errorf
  called_by: GetLocalServerAddresses, maybeFetchGatewayAddresses, Valid, clustersFromSnapshotMeshGateway, endpointsFromSnapshotMeshGateway

MeshGatewayConfig (proto/private/pbservice/service.pb.go:708-708)
  mog annotation:  target=github.com/hashicorp/consul/agent/structs.MeshGatewayConfig output=service.gen.go name=Structs
  methods: GetMode, ProtoReflect, Reset, String

ConfigSnapshot.MeshGatewayValidExportedServices (agent/proxycfg/snapshot.go:528-528)
  MeshGatewayValidExportedServices ensures that the following data is present if it exists for a service before it returns
  behavior: ACCUMULATE(hasEntExportedService... -> out svc)

ConsulResolver.resolveServiceEntry (connect/resolver.go:143-143)
  sig: ConsulResolver.resolveServiceEntry(entry *api.ServiceEntry)
  behavior: PRECEDENCE(addr -> entry -> service)
  calls: Errorf
  called_by: resolveQuery, resolveService

ServiceDefaults.GetMeshGateway (proto/private/pbconfigentry/config_entry.pb.go:4145-4145)

configSnapshotMeshGateway.hasEntExportedService (agent/proxycfg/snapshot_ce.go:10-10)
  sig: configSnapshotMeshGateway.hasEntExportedService(_ structs.ServiceName)
  called_by: IsServiceExported

updateMeshTopology (agent/consul/state/catalog.go:4924-4924)
  updateMeshTopology creates associations between the input service and its upstreams in the topology table
  sig: updateMeshTopology(tx WriteTxn, idx uint64, node string, svc *structs.NodeS...)
  calls: String, PartitionOrDefault, CompoundServiceID, Insert, Errorf
  called_by: ensureServiceTxn

ServiceSplit.GetEnterpriseMeta (agent/structs/config_entry_discoverychain_ce.go:22-22)
  GetEnterpriseMeta is used to synthesize the EnterpriseMeta struct from fields in the ServiceSplit
  sig: ServiceSplit.GetEnterpriseMeta(_ *acl.EnterpriseMeta)
  behavior: DELEGATE(DefaultEnterpriseMetaInDefaultPartition -> result)
  called_by: EqualID, assembleChain, newDefaultServiceResolver, AuthorizeAndSignCertificate, ensureNodeTxn, configEntryHasVirtualIP, deleteConfigEntryTxn, newConfigEntryQuery

cleanupMeshTopology (agent/consul/state/catalog.go:4998-4998)
  cleanupMeshTopology removes a service from the mesh topology table This is only safe to call when there are no more know
  sig: cleanupMeshTopology(tx WriteTxn, idx uint64, service *structs.ServiceNode)
  calls: String, Get, DeepCopy, Delete, Insert, Errorf
  called_by: deleteServiceTxn

ServiceSplit (api/config_entry_discoverychain.go:155-155)
  type ServiceSplit

ServiceSplit (agent/structs/config_entry_discoverychain.go:842-842)
  ServiceSplit defines how much traffic to send to which set of service instances during a traffic split.
  methods: MergeParent, appendHash, getHash

ConsulResolver.resolveService (connect/resolver.go:102-102)
  sig: ConsulResolver.resolveService(ctx context.Context)
  behavior: GUARD(err != nil -> return "", nil, err); PRECEDENCE(err -> len)
  calls: queryOptions, resolveServiceEntry, Errorf
  called_by: Resolve

IsConsulServiceID (agent/structs/catalog_ce.go:8-8)
  sig: IsConsulServiceID(id ServiceID)

NormalizeServiceSplitWeight (agent/structs/config_entry_discoverychain.go:728-728)
  sig: NormalizeServiceSplitWeight(weight float32)
  behavior: DELEGATE(float32 -> result)
  calls: scaleWeight
  called_by: Normalize

ServiceSplit.appendHash (agent/structs/config_entry_discoverychain.go:889-889)
  sig: ServiceSplit.appendHash(h *customHasher)
  behavior: GUARD(d == nil -> return)
  calls: addFloat32, addString
  called_by: hashValue

ServiceSplit.getHash (agent/structs/config_entry_discoverychain.go:885-885)
  behavior: DELEGATE(hashValue -> result)

Store.ServiceUsage (agent/consul/state/usage.go:413-413)
  ServiceUsage returns the latest seen Raft index, a compiled set of service usage data, and any errors.
  sig: Store.ServiceUsage(ws memdb.WatchSet, tenantUsage bool)
  behavior: GUARD(err != nil -> return 0, structs.S...); PRECEDENCE(err); ACCUMULATE(firstUsageEntry loop -> result)
  calls: ReadTxn, Abort, billableServiceInstancesTableName, connectUsageTableName, firstUsageEntry, Errorf

configSnapshotMeshGateway.IsServiceExported (agent/proxycfg/snapshot.go:608-608)
  sig: configSnapshotMeshGateway.IsServiceExported(svc structs.ServiceName)
  behavior: GUARD(c == nil -> return false); PRECEDENCE(c -> _)
  calls: hasEntExportedService

AllowAuthorizer.MeshReadAllowed (acl/authorizer.go:345-345)
  MeshReadAllowed determines if the read-only Consul mesh functions can be used.
  sig: AllowAuthorizer.MeshReadAllowed(ctx *AuthorizerContext)
  behavior: GUARD(a.MeshRead(ctx) != Allow -> return PermissionDe...)
  calls: MeshRead

AllowAuthorizer.MeshWriteAllowed (acl/authorizer.go:354-354)
  MeshWriteAllowed determines if the state-changing Consul mesh functions can be used.
  sig: AllowAuthorizer.MeshWriteAllowed(ctx *AuthorizerContext)
  behavior: GUARD(a.MeshWrite(ctx) != Allow -> return PermissionDe...)
  calls: MeshWrite

DNSServer.lookupServiceNodes (agent/dns.go:1499-1499)
  lookupServiceNodes is used to look up a node in the Consul health catalog within ServiceNodes.
  sig: DNSServer.lookupServiceNodes(cfg *dnsRequestConfig, lookup serviceLookup)
  calls: coalesceDNSToken
  called_by: getNameserversAndNodeRecord, handleServiceQuery

ChainedAuthorizer.MeshWrite (acl/chained_authorizer.go:162-162)
  MeshWrite determines if the state-changing Consul mesh functions can be used.
  sig: ChainedAuthorizer.MeshWrite(entCtx *AuthorizerContext)
  calls: executeChain
  called_by: MeshWriteAllowed

Agent.purgeService (agent/agent.go:2186-2186)
  purgeService removes a persisted service definition file from the data dir
  sig: Agent.purgeService(serviceID structs.ServiceID)
  calls: makeServiceFilePath, Remove, Stat
  called_by: cleanupRegistration, loadServices, removeServiceLocked

ConsulResolver (connect/resolver.go:64-64)
  ConsulResolver queries Consul for a service instance.
  methods: Resolve, queryOptions, resolveQuery, resolveService, resolveServiceEntry

DiscoverySplit (api/discovery_chain.go:175-175)
  compiled form of ServiceSplit

DiscoverySplit (agent/structs/discovery_chain.go:243-243)
  compiled form of ServiceSplit
  methods: appendHash, getHash

ExportedService (proto/private/pbpeerstream/peerstream.pb.go:258-258)
  ExportedService is one of the types of data returned via peer stream replication.
  methods: GetNodes, ProtoReflect, Reset, String

ExportedServiceList (proto/private/pbpeerstream/peerstream.pb.go:303-303)
  ExportedServiceList is one of the types of data returned via peer stream replication.
  methods: GetServices, ProtoReflect, Reset, String

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 82 symbols in L3, 23 with behavior annotations
uncovered: ShadowServiceRouterConfigEntry.CheckEnt, ACLResolver.synthesizePoliciesForServiceIdentities, ConnectProxyConfig.GetMeshGateway, EventPayloadServiceListUpdate.HasReadPermission

--- CLUE FILE END ---

QUESTION: According to the docs, how is Consul's service mesh split between control plane and data plane?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
