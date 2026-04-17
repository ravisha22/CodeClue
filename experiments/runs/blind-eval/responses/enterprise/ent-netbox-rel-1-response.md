# Enterprise Eval: ent-netbox-rel-1
Date: 2026-04-17

## Question

How do tenancy and resource ownership differ in NetBox, and how are they organized?

---

## Reasoning Scaffold

### 1. Identifying Relevant Modules and Symbols

The clue file surfaces two distinct but related concepts: **tenancy** (a dedicated Django app) and **ownership** (a cross-cutting form mixin). The relevant evidence clusters into three groups:

| Concept | Key Symbols | Source |
|---|---|---|
| Tenancy app infrastructure | `TenancyConfig`, `TenancyRootView`, `TenancyQuery` | `tenancy/apps.py`, `tenancy/api/views.py`, `tenancy/graphql/schema.py` |
| Tenancy as an assignable property | `TenancyFilterSet`, `TenancyFilterMixin`, `TenancyFilterForm`, `TenancyForm`, `TenancyColumnsMixin`, `TenantColumn`, `TenantGroupColumn` | `tenancy/filtersets.py`, `tenancy/forms/`, `tenancy/tables/columns.py`, `tenancy/graphql/filter_mixins.py` |
| Ownership | `OwnerMixin` | `netbox/forms/mixins.py` |

### 2. Tracing Through the Clues

#### 2a. Tenancy Is a First-Class Django Application

NetBox dedicates an entire top-level package—`tenancy/`—to the concept.  
`TenancyConfig` (netbox/tenancy/apps.py:4-13) is an `AppConfig` subclass with `name='tenancy'`, confirming it is registered as a standalone Django application in the project's installed-apps list. The TREE entry corroborates this: `tenancy/` appears alongside `dcim/`, `ipam/`, `circuits/`, etc., as a peer subpackage under the root `netbox/` directory (TREE: netbox/ subpackages).

#### 2b. Tenancy Is Built Around Tenant and Tenant Group

Two custom table columns reveal the core domain objects:

- **`TenantColumn`** (netbox/tenancy/tables/columns.py:16-26) — a `TemplateColumn` that "Include[s] the tenant description." It is consumed by `TenancyColumnsMixin`.
- **`TenantGroupColumn`** (netbox/tenancy/tables/columns.py:29-42) — a `TemplateColumn` that "Include[s] the tenant group description." Also consumed by `TenancyColumnsMixin`.

`TenancyColumnsMixin` (netbox/tenancy/tables/columns.py:45-51) extends `Table` and calls both `TenantColumn` and `TenantGroupColumn`, indicating that any table class mixing it in automatically gains columns for both the *tenant* and the *tenant group*. This two-level hierarchy (group → tenant) is the organizing principle for tenancy.

#### 2c. Tenancy Is a Cross-Cutting Concern Assignable to Many Models

Several mixin/filter constructs prove that tenancy is not confined to its own app but is *mixed into* objects across NetBox:

- **`TenancyFilterSet`** (netbox/tenancy/filtersets.py:251-279) is described as *"An inheritable FilterSet for models which support Tenant assignment."* The word "inheritable" is key—other apps (dcim, ipam, circuits, etc.) inherit this FilterSet to allow filtering their own models by tenant.
- **`TenancyFilterMixin`** (netbox/tenancy/graphql/filter_mixins.py:27-37) provides the same tenant-aware filtering surface for the GraphQL API.
- **`TenancyFilterForm`** (netbox/tenancy/forms/forms.py:36-51) and **`TenancyForm`** (netbox/tenancy/forms/forms.py:15-33) supply reusable form fragments so that any model's create/edit UI can include tenant-assignment fields.

Together these show that tenancy operates as a **tag-like assignment**: resources across many apps can be stamped with a Tenant (and, transitively, a Tenant Group) to express organizational ownership or responsibility.

#### 2d. Ownership Is a Separate, Form-Level Concept

**`OwnerMixin`** (netbox/netbox/forms/mixins.py:143-163) is described as *"Mixin for forms which adds ownership fields."* Critically, it lives in the generic `netbox/forms/mixins.py` module—**not** inside the `tenancy/` package—and it extends `Form`. This placement signals that "ownership" in NetBox is a **distinct mechanism** from tenancy. While tenancy tracks which organizational tenant a resource is associated with, ownership adds fields that record *who* (likely a user or group) owns a particular object at the form level.

#### 2e. How Resources Are Organized More Broadly

The clues reveal a recurring pattern of **role-based organization** for different object types, separate from tenancy:

- **`DeviceRole`** (netbox/dcim/models/devices.py:387-440) — *"Devices are organized by functional role; for example, 'Core Switch' or 'File Server'."*
- **`RackRole`** (netbox/dcim/models/racks.py:229-241) — *"Racks can be organized by functional role, similar to Devices."*
- **`CircuitType`** (netbox/circuits/models/circuits.py:32-40) — *"Circuits can be organized by their functional role."*
- **`VirtualCircuitType`** (netbox/circuits/models/virtual_circuits.py:22-30) — *"Like physical circuits, virtual circuits can be organized by their functional role."*

These role/type models extend organizational models (`NestedGroupModel`, `OrganizationalModel`, `BaseCircuitType`) and are orthogonal to tenancy: a device has both a `DeviceRole` *and* (optionally) a `Tenant`.

#### 2f. Base Model Hierarchy Relevant to Both

- **`NetBoxModel`** (netbox/netbox/models/__init__.py:111-117) — *"Base model for most object types."* Extends `NetBoxFeatureSet` and `BaseModel`.
- **`NetBoxFeatureSet`** (netbox/netbox/models/__init__.py:25-47) — bundles `BookmarksMixin`, `ChangeLoggingMixin`, `CloningMixin`, and other capabilities.
- **`AdminModel`** (netbox/netbox/models/__init__.py:235-255) — *"A model which represents an administrative resource."* Extends `BookmarksMixin`, `CloningMixin`, `CustomLinksMixin`.

The tenancy mixins (`TenancyFilterSet`, `TenancyColumnsMixin`, etc.) are designed to be composed onto models that inherit from `NetBoxModel`, while `OwnerMixin` operates at the form layer.

### 3. Synthesis: Tenancy vs. Ownership

| Dimension | Tenancy | Ownership |
|---|---|---|
| **Scope** | Dedicated Django app (`tenancy/`) with its own models, API (`TenancyRootView`), GraphQL schema (`TenancyQuery`), filtersets, and forms | A single form mixin (`OwnerMixin`) in the generic forms package |
| **Hierarchy** | Two-level: *Tenant Group → Tenant* (evidenced by `TenantGroupColumn` and `TenantColumn`) | No hierarchy visible in the clues |
| **Application mechanism** | Mixins injected across apps: `TenancyFilterSet` for querysets, `TenancyColumnsMixin` for tables, `TenancyFilterMixin` for GraphQL, `TenancyForm`/`TenancyFilterForm` for UI forms | Mixed into individual forms via `OwnerMixin` |
| **Semantic purpose** | Expresses *organizational or customer association*—which tenant (business unit, customer, department) a resource belongs to | Expresses *individual ownership*—which user or entity owns the record |
| **Layer** | Model + API + GraphQL + UI (full stack) | Form-level only (based on available evidence) |

### 4. GAPS and Limitations

The GAPS annotation states:

> - **type: STRUCTURAL** (answerable from L0-L2)
> - **coverage: 45 symbols in L3, 4 with behavior annotations**

This means the following **cannot be determined** from the provided clues alone:

1. **The actual model definitions for `Tenant` and `TenantGroup`** — while columns and filtersets reference them, the model source code is not included; we cannot confirm their exact fields, relationships, or constraints.
2. **What fields `OwnerMixin` adds** — the clue says it "adds ownership fields" but does not enumerate them. We cannot determine whether ownership tracks a User, a Group, or some other principal.
3. **Whether tenancy assignment is implemented as a ForeignKey on each model** — the filtersets and forms strongly suggest this, but the actual field definition on consuming models is not in the clues.
4. **The relationship (if any) between `OwnerMixin` and `Tenant`** — whether ownership and tenancy can coexist on the same object, or are mutually exclusive, is not established.
5. **How tenancy interacts with permissions or access control** — no RBAC or object-permission evidence is present in the clues.
6. **Full list of models that support tenant assignment** — `TenancyFilterSet` is described as "inheritable," but the consuming models are not enumerated.
7. **Behavior details for 41 of 45 L3 symbols** — only 4 symbols carry behavior annotations, so internal logic of most listed symbols is opaque.

### 5. Conclusion

In NetBox, **tenancy** and **resource ownership** are architecturally separate concerns. Tenancy is a full-stack, first-class Django application organized around a two-level *Tenant Group → Tenant* hierarchy, designed to be mixed into any model across the codebase via inheritable filtersets, form fragments, table-column mixins, and GraphQL filter mixins. It expresses organizational association. Ownership, by contrast, is a lightweight form-level mixin (`OwnerMixin`) that adds ownership fields to individual forms, expressing a different dimension of "who is responsible." Both coexist with a third organizational axis—functional roles (`DeviceRole`, `RackRole`, `CircuitType`, `VirtualCircuitType`)—that classifies resources by purpose rather than by organizational affiliation.
