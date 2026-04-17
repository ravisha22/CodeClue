# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: ent-consul-rel-2

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.

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
