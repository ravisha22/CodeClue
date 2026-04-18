# Enterprise v4 (full-stack): ent-netbox-rel-1
Date: 2026-04-18

## Answer
Across the architectural context and clue/domain model, tenancy is the customer or internal-organization association attached to infrastructure objects, while ownership is a separate responsibility signal. Tenant groups are hierarchical and can nest recursively, and an individual tenant may belong to one of those groups or to none at all. Most major operational objects can carry exactly one tenant assignment, including circuits, devices, racks, prefixes, VLANs, VRFs, clusters, and virtual machines. Resource ownership is modeled differently: it identifies the users or groups responsible for an object, and the prompt explicitly distinguishes that from tenant assignment rather than treating it as the same concept.

## Synthesis
NetBox therefore separates commercial or organizational tenancy from operational accountability: one answers ‘whose environment is this,’ the other answers ‘who owns/supports it.’
