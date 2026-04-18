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
