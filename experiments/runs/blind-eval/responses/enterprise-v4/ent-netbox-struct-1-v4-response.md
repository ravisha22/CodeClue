# Enterprise v4 (full-stack): ent-netbox-struct-1
Date: 2026-04-18

## Answer
The full-stack prompt frames NetBox as a Django-based source-of-truth platform for network infrastructure, and the clue docs make clear that its architectural role is to be the system of record rather than a controller that directly talks to routers or switches. In the recommended operating model, NetBox stays the central authority while separate monitoring, assurance, and execution systems consume its data. That data scope is broad: the repository context and clue cover regions, sites, locations, racks, devices, cables, power, circuits, virtual machines, IP prefixes, ranges and addresses, VRFs, VLANs, tenancy, and contacts. Because the same relational model is exposed through both REST and GraphQL, the identical inventory/IPAM graph can drive cable maps, device configuration generation, and automation workflows.

## Synthesis
So NetBox is positioned as the canonical infrastructure knowledge graph: one authoritative model, many downstream operational consumers.
