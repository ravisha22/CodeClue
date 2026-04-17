# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: ent-consul-mech-2

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.

--- CLUE FILE (File 1) ---
=CC v2.1 consul@HEAD 1527mod 17749sym
? How does Consul load agent configuration and apply Auto-Config?


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

AutoConfig.InitialConfiguration (agent/consul/auto_config_endpoint.go:349-349)
  AgentAutoConfig will authorize the incoming request and then generate the configuration to push down to the client
  sig: AutoConfig.InitialConfiguration(req *pbautoconf.AutoConfigRequest, resp *pbautoconf.Auto...)
  behavior: PRECEDENCE(req -> ac); ACCUMULATE(configFn loop -> result)
  calls: Authorize, Errorf

AutoConfig.maybeLoadConfig (agent/auto-config/auto_config.go:190-190)
  maybeLoadConfig will read the Consul configuration using the provided config loader if and only if the config field of t
  behavior: GUARD(ac.config == nil -> return err)
  calls: ReadConfig
  called_by: InitialConfiguration

GetAgentConfig (agent/netutil/network.go:43-43)
  GetAgentConfig retrieves the agent's configuration using the local Consul agent's API.
  sig: GetAgentConfig(config *api.Config)
  behavior: PRECEDENCE(config -> err)
  calls: NewClient

LoadBalancer (proto/private/pbconfigentry/config_entry.pb.go:2475-2475)
  mog annotation:  target=github.com/hashicorp/consul/agent/structs.LoadBalancer output=config_entry.gen.go name=Structs
  methods: GetHashPolicies, GetLeastRequestConfig, GetPolicy, GetRingHashConfig, ProtoReflect, Reset

RuntimeConfig (agent/config/runtime.go:55-55)
  RuntimeConfig specifies the configuration the consul agent actually uses.
  methods: APIConfig, ClientAddress, ConnectCAConfiguration, Sanitized, StructLocality, VersionWithMetadata

StaticRuntimeConfig (agent/config/runtime.go:38-38)
  StaticRuntimeConfig specifies the subset of configuration the consul agent actually uses and that are not reloadable by 

UpstreamConfiguration (proto/private/pbconfigentry/config_entry.pb.go:4503-4503)
  mog annotation:  target=github.com/hashicorp/consul/agent/structs.UpstreamConfiguration output=config_entry.gen.go name=
  methods: GetDefaults, GetOverrides, ProtoReflect, Reset, String

GetAgentConfigWithDTO (agent/netutil/network.go:92-92)
  GetAgentConfigDTO retrieves the agent's configuration using the local Consul agent's API.
  sig: GetAgentConfigWithDTO(req *IPStackRequestDTO)
  behavior: GUARD(req.Client != nil -> return nil, err); PRECEDENCE(req -> err)
  calls: NewClient
  called_by: GetAgentBindAddrWithDTO

AutoConfig.updateACLsInConfig (agent/consul/auto_config_endpoint.go:223-223)
  updateACLtokensInConfig will configure all of the agents ACL settings and will populate the configuration with an agent 
  sig: AutoConfig.updateACLsInConfig(opts AutoConfigOptions, resp *pbautoconf.AutoConfigRespo...)
  behavior: GUARD(ac.config.ACLsEnabled -> return fmt.Errorf("...)
  calls: PartitionOrDefault, printNodeName, Errorf

AutoConfig (agent/consul/auto_config_endpoint.go:152-152)
  AutoConfig endpoint is used for cluster auto configuration operations
  methods: InitialConfiguration, baseConfig, updateACLsInConfig, updateGossipEncryptionInConfig, updateJoinAddressesInConfig, updateTLSCertificatesInConfig

AutoConfig.recordInitialConfiguration (agent/auto-config/auto_config.go:232-232)
  recordInitialConfiguration is responsible for recording the AutoConfigResponse from the AutoConfig.InitialConfiguration 
  sig: AutoConfig.recordInitialConfiguration(resp *pbautoconf.AutoConfigResponse)
  behavior: GUARD(err != nil -> return fmt.Errorf("...); PRECEDENCE(err)
  calls: ReadConfig, persistAutoConfig, populateCertificateCache, updateTLSFromResponse, Errorf
  called_by: InitialConfiguration, handleFallback

AutoConfigRequest.GetConsulToken (proto/private/pbautoconf/auto_config.pb.go:122-122)
  behavior: GUARD(x != nil -> return x.ConsulToken)

AutoConfig.ReadConfig (agent/auto-config/auto_config.go:110-110)
  ReadConfig will parse the current configuration and inject any auto-config sources if present into the correct place in 
  behavior: GUARD(err != nil -> return result.Runti...); ACCUMULATE(Warn loop -> result); UNWIND(defer)
  calls: Lock, Unlock
  called_by: InitialConfiguration, maybeLoadConfig, recordInitialConfiguration

AutoConfig (agent/auto-config/auto_config.go:25-25)
  AutoConfig is all the state necessary for being able to parse a configuration as well as perform the necessary RPCs to p
  methods: Done, InitialConfiguration, IsRunning, ReadConfig, Start, Stop

AutoEncrypt (agent/config/config.go:624-624)
  AutoEncrypt is the agent-global auto_encrypt configuration.

Agent.AutoReloadConfig (agent/agent.go:4191-4191)
  calls: reloadConfig
  called_by: Start

DefaultConsulSource (agent/config/default.go:277-277)
  DefaultConsulSource returns the default configuration for the consul agent.

DevConsulSource (agent/config/default.go:305-305)
  DevConsulSource returns the consul agent configuration for the dev mode.
  calls: strPtr

Load (agent/config/builder.go:109-109)
  Load will build the configuration including the config source injected after all other defaults but before any user supp
  sig: Load(opts LoadOpts)
  calls: build, validate, newBuilder

enterpriseConsulConfig (agent/agent_ce.go:40-40)
  enterpriseConsulConfig is a noop stub for the func defined in agent_ent.go
  sig: enterpriseConsulConfig(_ *consul.Config, _ *config.RuntimeConfig)

Agent.loadMetadata (agent/agent.go:4078-4078)
  loadMetadata loads node metadata fields from the agent config and updates them on the local agent.
  sig: Agent.loadMetadata(conf *config.RuntimeConfig)
  called_by: Start, reloadConfigInternal

AgentConfigWatcher (connect/proxy/config.go:214-214)
  AgentConfigWatcher watches the local Consul agent for proxy config changes.
  methods: Close, Watch

AgentServiceConnectProxyConfig (api/agent.go:197-197)
  AgentServiceConnectProxyConfig is the proxy configuration in a connect-proxy ServiceDefinition or response.

AutoConfigRequest (proto/private/pbautoconf/auto_config.pb.go:31-31)
  AutoConfigRequest is the data structure to be sent along with the AutoConfig.InitialConfiguration RPC
  methods: GetCSR, GetConsulToken, GetDatacenter, GetJWT, GetNode, GetPartition

AutoConfigResponse (proto/private/pbautoconf/auto_config.pb.go:137-137)
  AutoConfigResponse is the data structure sent in response to a AutoConfig.InitialConfiguration request
  methods: GetCARoots, GetCertificate, GetConfig, GetExtraCACertificates, ProtoReflect, Reset

ConnectProxyConfig (api/agent.go:508-508)
  ConnectProxyConfig is the response structure for agent-local proxy configuration.

Handler.ReloadConfig (agent/uiserver/uiserver.go:95-95)
  ReloadConfig is called by the agent when the configuration is reloaded and updates the UIConfig values the handler uses 
  sig: Handler.ReloadConfig(newCfg *config.RuntimeConfig)
  called_by: reloadConfigInternal, DNSDisableCompression

State.LoadMetadata (agent/local/state.go:979-979)
  LoadMetadata loads node metadata fields from the agent config and updates them on the local agent.
  sig: State.LoadMetadata(data map[string]string)
  behavior: ACCUMULATE(loop -> result); UNWIND(defer)
  calls: Lock, Unlock

AccessLogsConfig (proto/private/pbservice/service.pb.go:819-819)
  mog annotation:  target=github.com/hashicorp/consul/agent/structs.AccessLogsConfig output=service.gen.go name=Structs
  methods: GetDisableListenerLogs, GetEnabled, GetJSONFormat, GetPath, GetTextFormat, GetType

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 83 symbols in L3, 28 with behavior annotations
uncovered: AutoConfig.getDNSSANs, AutoConfig.Stop, Config.AgentEnterpriseMeta, builder.validateAutoConfig
drill: agent/consul/auto_config_endpoint.go (~1 lines, AutoConfig.InitialConfiguration)
drill: agent/auto-config/auto_config.go (~1 lines, AutoConfig.maybeLoadConfig)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## AutoConfig.InitialConfiguration  (agent/consul/auto_config_endpoint.go L349-349)
```
func (ac *AutoConfig) InitialConfiguration(req *pbautoconf.AutoConfigRequest, resp *pbautoconf.AutoConfigResponse) error {
```

## AutoConfig.maybeLoadConfig  (agent/auto-config/auto_config.go L190-190)
```
func (ac *AutoConfig) maybeLoadConfig() error {
```

## AutoConfig.baseConfig  (agent/consul/auto_config_endpoint.go L317-317)
```
func (ac *AutoConfig) baseConfig(opts AutoConfigOptions, resp *pbautoconf.AutoConfigResponse) error {
```

## AutoConfig.updateACLsInConfig  (agent/consul/auto_config_endpoint.go L223-223)
```
func (ac *AutoConfig) updateACLsInConfig(opts AutoConfigOptions, resp *pbautoconf.AutoConfigResponse) error {
```

## AutoConfig.updateGossipEncryptionInConfig  (agent/consul/auto_config_endpoint.go L278-278)
```
func (ac *AutoConfig) updateGossipEncryptionInConfig(_ AutoConfigOptions, resp *pbautoconf.AutoConfigResponse) error {
```

## AutoConfig.updateJoinAddressesInConfig  (agent/consul/auto_config_endpoint.go L263-263)
```
func (ac *AutoConfig) updateJoinAddressesInConfig(opts AutoConfigOptions, resp *pbautoconf.AutoConfigResponse) error {
```

## AutoConfig.updateTLSCertificatesInConfig  (agent/consul/auto_config_endpoint.go L180-180)
```
func (ac *AutoConfig) updateTLSCertificatesInConfig(opts AutoConfigOptions, resp *pbautoconf.AutoConfigResponse) error {
```

## AutoConfig.updateTLSSettingsInConfig  (agent/consul/auto_config_endpoint.go L303-303)
```
func (ac *AutoConfig) updateTLSSettingsInConfig(_ AutoConfigOptions, resp *pbautoconf.AutoConfigResponse) error {
```

## AutoConfig  (agent/consul/auto_config_endpoint.go L152-152)
```
type AutoConfig struct {
```

## AutoConfigAuthorizer  (agent/consul/auto_config_endpoint.go L41-41)
```
type AutoConfigAuthorizer interface {
```

## AutoConfigBackend  (agent/consul/auto_config_endpoint.go L143-143)
```
type AutoConfigBackend interface {
```

## AutoConfigOptions.PartitionOrDefault  (agent/consul/auto_config_endpoint.go L37-37)
```
func (opts AutoConfigOptions) PartitionOrDefault() string {
```

## AutoConfigOptions  (agent/consul/auto_config_endpoint.go L28-28)
```
type AutoConfigOptions struct {
```

## NewAutoConfig  (agent/consul/auto_config_endpoint.go L163-163)
```
func NewAutoConfig(conf *Config, tlsConfigurator *tlsutil.Configurator, backend AutoConfigBackend, authz AutoConfigAuthorizer) *AutoConfig {
```

## disabledAuthorizer  (agent/consul/auto_config_endpoint.go L47-47)
```
type disabledAuthorizer struct{}
```

## jwtAuthorizer.Authorize  (agent/consul/auto_config_endpoint.go L65-65)
```
func (a *jwtAuthorizer) Authorize(req *pbautoconf.AutoConfigRequest) (AutoConfigOptions, error) {
```

## jwtAuthorizer  (agent/consul/auto_config_endpoint.go L53-53)
```
type jwtAuthorizer struct {
```

## parseAutoConfigCSR  (agent/consul/auto_config_endpoint.go L394-394)
```
func parseAutoConfigCSR(csr string) (*x509.CertificateRequest, *connect.SpiffeIDAgent, error) {
```

## printNodeName  (agent/consul/state/catalog.go L173-173)
```
func printNodeName(nodeName, partition string) string {
```

## AutoConfig.Done  (agent/auto-config/auto_config.go L394-394)
```
func (ac *AutoConfig) Done() <-chan struct{} {
```

## AutoConfig.IsRunning  (agent/auto-config/auto_config.go L408-408)
```
func (ac *AutoConfig) IsRunning() bool {
```

## AutoConfig.ReadConfig  (agent/auto-config/auto_config.go L110-110)
```
func (ac *AutoConfig) ReadConfig() (*config.RuntimeConfig, error) {
```

## AutoConfig.Start  (agent/auto-config/auto_config.go L352-352)
```
func (ac *AutoConfig) Start(ctx context.Context) error {
```

## AutoConfig.Stop  (agent/auto-config/auto_config.go L414-414)
```
func (ac *AutoConfig) Stop() bool {
```

## AutoConfig.getInitialConfiguration  (agent/auto-config/auto_config.go L326-326)
```
func (ac *AutoConfig) getInitialConfiguration(ctx context.Context) (*pbautoconf.AutoConfigResponse, error) {
```

## AutoConfig.getInitialConfigurationOnce  (agent/auto-config/auto_config.go L275-275)
```
func (ac *AutoConfig) getInitialConfigurationOnce(ctx context.Context, csr string, key string) (*pbautoconf.AutoConfigResponse, error) {
```

## AutoConfig.introToken  (agent/auto-config/auto_config.go L204-204)
```
func (ac *AutoConfig) introToken() (string, error) {
```

## AutoConfig.recordInitialConfiguration  (agent/auto-config/auto_config.go L232-232)
```
func (ac *AutoConfig) recordInitialConfiguration(resp *pbautoconf.AutoConfigResponse) error {
```

## New  (test/integration/consul-container/libs/cluster/cluster.go L70-70)
```
func New(t TestingT, configs []Config, ports ...int) (*Cluster, error) {
```
--- END SOURCE SNIPPETS ---

QUESTION: How does Consul load agent configuration and apply Auto-Config?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
