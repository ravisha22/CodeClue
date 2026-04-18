# Enterprise v4 (full-stack): ent-consul-struct-2
Date: 2026-04-18

## Answer
The docs in the prompt describe Consul cluster communication as a mixed-RPC system. It uses both gRPC and Go’s `net/rpc`, with most intra-cluster traffic multiplexed over the server TCP port `8300`. Internal gRPC APIs are exposed on that server port, while external gRPC APIs are split onto the dedicated `8502` port. Federation is layered on top through network areas, which form pairwise WAN gossip pools between datacenters and use TCP connections over the server RPC port.

## Synthesis
That gives Consul a topology where local cluster communication is port-consolidated, while cross-datacenter federation is modeled as explicit WAN gossip areas riding the server RPC channel.
