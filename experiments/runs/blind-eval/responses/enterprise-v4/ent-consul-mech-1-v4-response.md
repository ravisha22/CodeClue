# Enterprise v4 (full-stack): ent-consul-mech-1
Date: 2026-04-18

## Answer
The docs and deep runtime context describe Envoy configuration as an incremental control-plane loop. First, the initial bootstrap configuration is generated either by a `consul-dataplane` instance or by a Consul client agent. Once bootstrapped, Envoy connects outward to an xDS server, and that xDS endpoint may be provided by either a Consul server or a Consul client agent. On the Consul side, the system initializes internal watches over the state snapshots needed to configure Envoy. As those snapshots change, Consul computes and pushes updated xDS configuration diffs instead of rebuilding the whole world from scratch each time.

## Synthesis
So the lifecycle is bootstrap once, attach to xDS, watch cluster state continuously, and stream diffs whenever the watched snapshot changes.
