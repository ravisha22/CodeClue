# Enterprise v2: ent-consul-mech-2
Date: 2026-04-17

## Question
How does Consul load agent configuration and apply Auto-Config?

## Reasoning Scaffold

### Step 1: Identify Relevant Modules, Symbols, and Relationships

**From TREE:**
- `agent/config/` — configuration building, parsing, defaults, and runtime config.
- `agent/auto-config/` — Auto-Config client-side logic (requesting and recording configuration).
- `agent/consul/auto_config_endpoint.go` — Auto-Config server-side endpoint.
- `agent/` — core agent lifecycle including config loading and reloading.
- `proto/private/pbautoconf/` — protobuf definitions for AutoConfig request/response.

**From FOCUS — Configuration Loading Symbols:**

- `Load` (`agent/config/builder.go:109`) — "will build the configuration including the config source injected after all other defaults but before any user supplied configuration." Calls `build`, `validate`, `newBuilder`. This is the top-level configuration loading function.

- `RuntimeConfig` (`agent/config/runtime.go:55`) — "specifies the configuration the consul agent actually uses." Methods: `APIConfig`, `ClientAddress`, `ConnectCAConfiguration`, `Sanitized`, `StructLocality`, `VersionWithMetadata`. This is the final runtime configuration type.

- `StaticRuntimeConfig` (`agent/config/runtime.go:38`) — "specifies the subset of configuration the consul agent actually uses and that are not reloadable by the agent." This separates static (immutable after startup) from dynamic configuration.

- `DefaultConsulSource` (`agent/config/default.go:277`) — "returns the default configuration for the consul agent." Provides baseline defaults.

- `DevConsulSource` (`agent/config/default.go:305`) — "returns the consul agent configuration for the dev mode." Calls `strPtr`. Provides development-mode overrides.

- `enterpriseConsulConfig` (`agent/agent_ce.go:40`) — "a noop stub for the func defined in agent_ent.go." This shows that enterprise-specific configuration is injected via a build-tag-controlled function.

- `Agent.loadMetadata` (`agent/agent.go:4078`) — "loads node metadata fields from the agent config and updates them on the local agent." Called by `Start` and `reloadConfigInternal`, showing it runs both at startup and on reload.

- `Agent.AutoReloadConfig` (`agent/agent.go:4191`) — calls `reloadConfig`. Called by `Start`. This sets up automatic configuration reloading.

- `Handler.ReloadConfig` (`agent/uiserver/uiserver.go:95`) — "called by the agent when the configuration is reloaded and updates the UIConfig values the handler uses." Called by `reloadConfigInternal`. Shows the reload cascade reaches the UI server.

- `State.LoadMetadata` (`agent/local/state.go:979`) — "loads node metadata fields from the agent config and updates them on the local agent." Behavior: `ACCUMULATE(loop -> result); UNWIND(defer)`. Uses `Lock`/`Unlock` for thread safety.

- `GetAgentConfig` (`agent/netutil/network.go:43`) — "retrieves the agent's configuration using the local Consul agent's API." Calls `NewClient`. This is a network utility for fetching config from a running agent.

- `GetAgentConfigWithDTO` (`agent/netutil/network.go:92`) — DTO variant. Behavior: `GUARD(req.Client != nil -> return nil, err); PRECEDENCE(req -> err)`. Called by `GetAgentBindAddrWithDTO`.

**From FOCUS — Auto-Config Server-Side (Endpoint):**

- `AutoConfig` endpoint (`agent/consul/auto_config_endpoint.go:152`) — "used for cluster auto configuration operations." Methods: `InitialConfiguration`, `baseConfig`, `updateACLsInConfig`, `updateGossipEncryptionInConfig`, `updateJoinAddressesInConfig`, `updateTLSCertificatesInConfig`.

- `AutoConfig.InitialConfiguration` (`agent/consul/auto_config_endpoint.go:349`) — "will authorize the incoming request and then generate the configuration to push down to the client." Behavior: `PRECEDENCE(req -> ac); ACCUMULATE(configFn loop -> result)`. Calls `Authorize`, `Errorf`. The `ACCUMULATE(configFn loop)` pattern shows it iterates through a series of configuration functions to build the response.

- `AutoConfig.baseConfig` — source snippet: `func (ac *AutoConfig) baseConfig(opts AutoConfigOptions, resp *pbautoconf.AutoConfigResponse) error` (`agent/consul/auto_config_endpoint.go:317`). Provides the base configuration.

- `AutoConfig.updateACLsInConfig` (`agent/consul/auto_config_endpoint.go:223`) — "will configure all of the agents ACL settings and will populate the configuration with an agent token." Behavior: `GUARD(ac.config.ACLsEnabled -> return fmt.Errorf("...))`. Calls `PartitionOrDefault`, `printNodeName`. This shows ACL configuration is conditionally applied based on whether ACLs are enabled.

- `AutoConfig.updateGossipEncryptionInConfig` — source snippet at `agent/consul/auto_config_endpoint.go:278`. Configures gossip encryption keys.

- `AutoConfig.updateJoinAddressesInConfig` — source snippet at `agent/consul/auto_config_endpoint.go:263`. Provides join addresses for cluster membership.

- `AutoConfig.updateTLSCertificatesInConfig` — source snippet at `agent/consul/auto_config_endpoint.go:180`. Provisions TLS certificates.

- `AutoConfig.updateTLSSettingsInConfig` — source snippet at `agent/consul/auto_config_endpoint.go:303`. Configures TLS settings.

**From Source Snippets — Server-Side Supporting Types:**

- `AutoConfigAuthorizer` interface (`agent/consul/auto_config_endpoint.go:41`) — authorization interface for Auto-Config requests.
- `AutoConfigBackend` interface (`agent/consul/auto_config_endpoint.go:143`) — backend interface for Auto-Config operations.
- `AutoConfigOptions` (`agent/consul/auto_config_endpoint.go:28`) — options struct with `PartitionOrDefault()` method.
- `NewAutoConfig` (`agent/consul/auto_config_endpoint.go:163`) — constructor taking `Config`, `tlsutil.Configurator`, `AutoConfigBackend`, `AutoConfigAuthorizer`.
- `jwtAuthorizer` (`agent/consul/auto_config_endpoint.go:53`) — JWT-based authorizer implementation with `Authorize` method (`agent/consul/auto_config_endpoint.go:65`).
- `disabledAuthorizer` (`agent/consul/auto_config_endpoint.go:47`) — authorizer that disables Auto-Config.
- `parseAutoConfigCSR` (`agent/consul/auto_config_endpoint.go:394`) — parses a CSR from the Auto-Config request, returning a `SpiffeIDAgent`.

**From FOCUS — Auto-Config Client-Side:**

- `AutoConfig` (`agent/auto-config/auto_config.go:25`) — "all the state necessary for being able to parse a configuration as well as perform the necessary RPCs to provide the initial TLS certificates." Methods: `Done`, `InitialConfiguration`, `IsRunning`, `ReadConfig`, `Start`, `Stop`.

- `AutoConfig.maybeLoadConfig` (`agent/auto-config/auto_config.go:190`) — "will read the Consul configuration using the provided config loader if and only if the config field of the AutoConfig is nil." Behavior: `GUARD(ac.config == nil -> return err)`. Calls `ReadConfig`. Called by `InitialConfiguration`. This is a lazy-loading mechanism.

- `AutoConfig.ReadConfig` (`agent/auto-config/auto_config.go:110`) — "will parse the current configuration and inject any auto-config sources if present into the correct place in the configuration." Behavior: `GUARD(err != nil -> return result.Runti...); ACCUMULATE(Warn loop -> result); UNWIND(defer)`. Calls `Lock`, `Unlock`. Called by `InitialConfiguration`, `maybeLoadConfig`, `recordInitialConfiguration`. Thread-safe configuration parsing with auto-config source injection.

- `AutoConfig.recordInitialConfiguration` (`agent/auto-config/auto_config.go:232`) — "responsible for recording the AutoConfigResponse from the AutoConfig.InitialConfiguration RPC." Behavior: `GUARD(err != nil -> return fmt.Errorf("...)); PRECEDENCE(err)`. Calls `ReadConfig`, `persistAutoConfig`, `populateCertificateCache`, `updateTLSFromResponse`. Called by `InitialConfiguration`, `handleFallback`. This shows the client records the server response, persists it, populates the certificate cache, and updates TLS settings.

**From Source Snippets — Client-Side Lifecycle:**

- `AutoConfig.Start` (`agent/auto-config/auto_config.go:352`) — starts the Auto-Config client.
- `AutoConfig.Stop` (`agent/auto-config/auto_config.go:414`) — stops the client.
- `AutoConfig.Done` (`agent/auto-config/auto_config.go:394`) — returns a channel signaling completion.
- `AutoConfig.IsRunning` (`agent/auto-config/auto_config.go:408`) — checks if running.
- `AutoConfig.getInitialConfiguration` (`agent/auto-config/auto_config.go:326`) — retrieves initial configuration.
- `AutoConfig.getInitialConfigurationOnce` (`agent/auto-config/auto_config.go:275`) — single-attempt retrieval, takes a CSR and key.
- `AutoConfig.introToken` (`agent/auto-config/auto_config.go:204`) — retrieves the introduction token for authentication.

**From FOCUS — Protobuf Request/Response:**

- `AutoConfigRequest` (`proto/private/pbautoconf/auto_config.pb.go:31`) — "the data structure to be sent along with the AutoConfig.InitialConfiguration RPC." Methods: `GetCSR`, `GetConsulToken`, `GetDatacenter`, `GetJWT`, `GetNode`, `GetPartition`.
- `AutoConfigResponse` (`proto/private/pbautoconf/auto_config.pb.go:137`) — "the data structure sent in response to a AutoConfig.InitialConfiguration request." Methods: `GetCARoots`, `GetCertificate`, `GetConfig`, `GetExtraCACertificates`.
- `AutoConfigRequest.GetConsulToken` (`proto/private/pbautoconf/auto_config.pb.go:122`) — behavior: `GUARD(x != nil -> return x.ConsulToken)`.

**From FOCUS — Other Configuration:**
- `AutoEncrypt` (`agent/config/config.go:624`) — "the agent-global auto_encrypt configuration." A separate but related auto-encryption mechanism.
- `AgentConfigWatcher` (`connect/proxy/config.go:214`) — "watches the local Consul agent for proxy config changes." Methods: `Close`, `Watch`.
- `ConnectProxyConfig` (`api/agent.go:508`) — "response structure for agent-local proxy configuration."
- `AgentServiceConnectProxyConfig` (`api/agent.go:197`) — "proxy configuration in a connect-proxy ServiceDefinition or response."

### Step 2: Trace the Configuration Loading Lifecycle

**Phase 1: Initial Configuration Build**
`Load` (`agent/config/builder.go:109`) → `newBuilder` → `build` → `validate` → produces `RuntimeConfig`.

The `Load` function accepts `LoadOpts` and builds the configuration by:
1. Creating a builder (`newBuilder`).
2. Building the config (`build`), which incorporates `DefaultConsulSource` (`agent/config/default.go:277`) for defaults and `DevConsulSource` (`agent/config/default.go:305`) for dev mode.
3. Validating the result (`validate`).
4. The injected config source is inserted "after all other defaults but before any user supplied configuration."

Enterprise-specific config is injected via `enterpriseConsulConfig` (`agent/agent_ce.go:40`), which is a noop in CE builds.

**Phase 2: Auto-Config Client Initialization (if enabled)**
When Auto-Config is enabled, the client-side `AutoConfig` (`agent/auto-config/auto_config.go:25`) manages the RPC lifecycle:

1. `AutoConfig.Start` (`agent/auto-config/auto_config.go:352`) begins the Auto-Config process.
2. `AutoConfig.maybeLoadConfig` (`agent/auto-config/auto_config.go:190`) lazily loads configuration if not already present, guarded by `ac.config == nil`, calling `ReadConfig`.
3. `AutoConfig.getInitialConfiguration` (`agent/auto-config/auto_config.go:326`) → `getInitialConfigurationOnce` (`agent/auto-config/auto_config.go:275`) — makes the RPC call to the server, using a CSR and intro token (`introToken` at line 204).
4. The RPC goes to the server's `AutoConfig.InitialConfiguration` endpoint.

**Phase 3: Auto-Config Server Processing**
`AutoConfig.InitialConfiguration` (`agent/consul/auto_config_endpoint.go:349`):
1. Calls `Authorize` to validate the request (via `AutoConfigAuthorizer` — either `jwtAuthorizer` for JWT-based auth or `disabledAuthorizer`).
2. Iterates through configuration functions (`ACCUMULATE(configFn loop)`):
   - `baseConfig` — provides base configuration.
   - `updateTLSCertificatesInConfig` — provisions TLS certificates (parses CSR via `parseAutoConfigCSR`).
   - `updateTLSSettingsInConfig` — configures TLS settings.
   - `updateACLsInConfig` — configures ACL settings and agent token (guarded by `ACLsEnabled`).
   - `updateJoinAddressesInConfig` — provides cluster join addresses.
   - `updateGossipEncryptionInConfig` — configures gossip encryption.
3. Returns an `AutoConfigResponse` containing `CARoots`, `Certificate`, `Config`, `ExtraCACertificates`.

**Phase 4: Client Records the Response**
`AutoConfig.recordInitialConfiguration` (`agent/auto-config/auto_config.go:232`):
1. Calls `ReadConfig` — re-parses configuration with auto-config sources injected.
2. Calls `persistAutoConfig` — persists the response to disk for crash recovery.
3. Calls `populateCertificateCache` — caches the provisioned certificates.
4. Calls `updateTLSFromResponse` — updates the agent's TLS configuration.

**Phase 5: ReadConfig Integrates Auto-Config Sources**
`AutoConfig.ReadConfig` (`agent/auto-config/auto_config.go:110`) — thread-safe (uses `Lock`/`Unlock`), parses the configuration and injects auto-config sources "into the correct place in the configuration." This produces a `RuntimeConfig` that incorporates both user-supplied config and auto-config-derived settings (TLS, ACL tokens, join addresses, gossip keys).

**Phase 6: Agent Startup with Loaded Config**
`Agent.Start` (`agent/agent.go:600`) uses the `RuntimeConfig`:
1. Calls `Agent.loadMetadata` (`agent/agent.go:4078`) to load node metadata.
2. Sets up `Agent.AutoReloadConfig` (`agent/agent.go:4191`) for automatic config reloading.

**Phase 7: Configuration Reloading**
`Agent.AutoReloadConfig` → `reloadConfig` → `reloadConfigInternal`:
1. Re-calls `Agent.loadMetadata` to update node metadata.
2. Calls `Handler.ReloadConfig` (`agent/uiserver/uiserver.go:95`) to update UI server config.
3. `State.LoadMetadata` (`agent/local/state.go:979`) accumulates metadata updates with thread safety.

### Step 3: GAPS — What Cannot Be Determined

Per the GAPS section:
- **Type:** MECHANISTIC (body logic needed for full answer)
- **Coverage:** 83 symbols in L3, 28 with behavior annotations.
- **Uncovered symbols:**
  - `AutoConfig.getDNSSANs` — how DNS SANs are computed for certificate requests.
  - `AutoConfig.Stop` — the shutdown mechanism details.
  - `Config.AgentEnterpriseMeta` — enterprise metadata on the config object.
  - `builder.validateAutoConfig` — validation logic for auto-config settings.

The source snippets provide only function signatures (1-line bodies), so the internal logic of `AutoConfig.InitialConfiguration`, `AutoConfig.maybeLoadConfig`, and the various `update*InConfig` functions cannot be fully reconstructed.

The exact ordering of config sources within `Load` (how defaults, auto-config sources, and user config are layered) is described conceptually ("after all other defaults but before any user supplied configuration") but the precise merge logic is in the uncovered `build` method.

The fallback mechanism (`handleFallback`, which also calls `recordInitialConfiguration`) is referenced but not detailed in the FOCUS entries.

### Step 4: Synthesis

**Configuration Loading:**

Consul loads agent configuration through a layered builder pattern:

1. `Load` (`agent/config/builder.go:109`) orchestrates the build by calling `newBuilder` → `build` → `validate`, producing a `RuntimeConfig` (`agent/config/runtime.go:55`). The config is split into `RuntimeConfig` (the full mutable config) and `StaticRuntimeConfig` (`agent/config/runtime.go:38`) for non-reloadable settings.

2. Default values come from `DefaultConsulSource` (`agent/config/default.go:277`), with `DevConsulSource` (`agent/config/default.go:305`) providing dev-mode overrides. Enterprise-specific configuration is injected via `enterpriseConsulConfig` (`agent/agent_ce.go:40`), which is a noop stub in the community edition.

3. The `Load` function injects auto-config sources "after all other defaults but before any user supplied configuration," establishing a precedence order: defaults → auto-config → user config.

**Auto-Config Mechanism:**

Auto-Config operates as a client-server RPC mechanism:

- **Client side:** `AutoConfig` (`agent/auto-config/auto_config.go:25`) manages the lifecycle via `Start`/`Stop`/`Done`/`IsRunning`. On startup, `maybeLoadConfig` (`agent/auto-config/auto_config.go:190`) lazily loads config (guarded by `ac.config == nil`), then `getInitialConfiguration` → `getInitialConfigurationOnce` makes the RPC using an intro token (`introToken`) and CSR. `ReadConfig` (`agent/auto-config/auto_config.go:110`) parses the config with auto-config sources injected, using lock-based thread safety.

- **Server side:** `AutoConfig.InitialConfiguration` (`agent/consul/auto_config_endpoint.go:349`) authorizes the request (via JWT: `jwtAuthorizer`, or disabled: `disabledAuthorizer`), then iterates through a chain of config functions — `baseConfig`, `updateTLSCertificatesInConfig`, `updateTLSSettingsInConfig`, `updateACLsInConfig`, `updateJoinAddressesInConfig`, `updateGossipEncryptionInConfig` — accumulating configuration into the `AutoConfigResponse`. The response includes CA roots, a signed certificate, agent config, and extra CA certificates (`AutoConfigResponse.GetCARoots`, `GetCertificate`, `GetConfig`, `GetExtraCACertificates` at `proto/private/pbautoconf/auto_config.pb.go:137`).

- **Recording:** `recordInitialConfiguration` (`agent/auto-config/auto_config.go:232`) persists the response (`persistAutoConfig`), populates the certificate cache (`populateCertificateCache`), updates TLS (`updateTLSFromResponse`), and re-reads the config (`ReadConfig`).

**Reloading:**
`Agent.AutoReloadConfig` (`agent/agent.go:4191`) → `reloadConfig` is set up during `Agent.Start`. On reload, `Agent.loadMetadata` (`agent/agent.go:4078`) updates node metadata, `Handler.ReloadConfig` (`agent/uiserver/uiserver.go:95`) updates the UI server, and `State.LoadMetadata` (`agent/local/state.go:979`) updates the local state with thread safety.

**Unresolved:** The exact config merge/layering logic within `build`, the `builder.validateAutoConfig` validation, the DNS SAN computation (`AutoConfig.getDNSSANs`), the fallback mechanism (`handleFallback`), and enterprise-specific auto-config behavior (`Config.AgentEnterpriseMeta`) cannot be determined from the clue alone (GAPS: uncovered).
