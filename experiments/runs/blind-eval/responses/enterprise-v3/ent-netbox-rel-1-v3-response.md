# Enterprise v3 (arch-enhanced): ent-netbox-rel-1
Date: 2026-04-18

## Answer
Tenancy and ownership are separate concepts in this prompt. At the architectural level, NetBox’s domain model includes tenants as part of the infrastructure graph, and it says "tenancy overlays ownership and access boundaries" rather than being identical to ownership (ARCH, ent-netbox-rel-1-v3.prompt.md:20). The tenancy subsystem is its own bounded app area with its own app config, forms, API root, GraphQL query, URL mounts, filter forms, filter sets, and table columns for tenant and tenant-group data (TenancyConfig, netbox/tenancy/apps.py:4-13; TenancyRootView, netbox/tenancy/api/views.py:10-15; TenancyQuery, netbox/tenancy/graphql/schema.py:8-25; path:api/tenancy/, netbox/netbox/urls.py:1-97; path:tenancy/, netbox/netbox/urls.py:1-97; TenancyFilterSet, netbox/tenancy/filtersets.py:251-279; TenantColumn, netbox/tenancy/tables/columns.py:16-26; TenantGroupColumn, netbox/tenancy/tables/columns.py:29-42).

That organization implies tenancy is how many infrastructure objects are associated with tenant and tenant-group metadata across the platform. The architectural summary lists tenants alongside circuits, devices, racks, prefixes, VLANs, VRFs, clusters, and virtual machines in the overall model, and `TenancyFilterSet` is described as inheritable for models that support tenant assignment (ARCH, ent-netbox-rel-1-v3.prompt.md:20; TenancyFilterSet, netbox/tenancy/filtersets.py:251-279).

Ownership is modeled separately. `OwnerMixin` is a form mixin that adds ownership fields, so resource ownership is a distinct responsibility/owner layer instead of the same thing as tenant assignment (OwnerMixin, netbox/netbox/forms/mixins.py:143-163).

## Gaps
The prompt does not show the recursive tenant-group relationship or the exact rule that a tenant may belong to one group or none. It also does not enumerate the tenant-assignment cardinality per model with the precision of the gold fact; it only supports the broader conclusion that tenancy spans many core object types (GAPS, ent-netbox-rel-1-v3.prompt.md:282-285).
