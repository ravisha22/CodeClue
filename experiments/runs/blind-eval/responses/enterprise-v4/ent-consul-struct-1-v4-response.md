# Enterprise v4 (full-stack): ent-consul-struct-1
Date: 2026-04-18

## Answer
The Consul architecture/docs split service mesh cleanly between a control plane and a request-path data plane. The data plane is the set of gateways, sidecar proxies, or native application libraries that actually sit in the traffic path, and the production recommendation is primarily Envoy as that proxy layer. The control plane’s main job is to generate and serve configuration to that data plane rather than to proxy traffic itself. In deployment terms, the mesh is composed of server agents, client agents, and consul-dataplane proxies working together.

## Synthesis
So the core divide is: Consul servers/agents compute policy and config, while Envoy-style sidecars and gateways enforce that config where requests actually flow.
