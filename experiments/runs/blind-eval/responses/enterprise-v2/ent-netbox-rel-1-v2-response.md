# Enterprise v2: ent-netbox-rel-1
Date: 2026-04-17

## Question
How do tenancy and resource ownership differ in NetBox, and how are they organized?

## Reasoning Scaffold

### Step 1: Identify relevant symbols in FOCUS and SYM

**Tenancy-related:**

| Symbol | Location | Description |
|---|---|---|
| `TenancyConfig` | `netbox/tenancy/apps.py:4-13` | Django AppConfig for the tenancy app, `name='tenancy'` |
| `TenancyFilterSet` | `netbox/tenancy/filtersets.py:251-279` | "An inheritable FilterSet for models which support Tenant assignment" |
| `TenancyForm` | `netbox/tenancy/forms/forms.py:15-33` | Form for tenant assignment |
| `TenancyFilterForm` | `netbox/tenancy/forms/forms.py:36-51` | Filter form for tenancy |
| `TenancyFilterMixin` | `netbox/tenancy/graphql/filter_mixins.py:27-37` | GraphQL filter mixin for tenant fields |
| `TenancyColumnsMixin` | `netbox/tenancy/tables/columns.py:45-51` | Table mixin; calls `TenantColumn` and `TenantGroupColumn` |
| `TenantColumn` | `netbox/tenancy/tables/columns.py:16-26` | "Include the tenant description" — extends `TemplateColumn` |
| `TenantGroupColumn` | `netbox/tenancy/tables/columns.py:29-42` | "Include the tenant group description" — extends `TemplateColumn` |
| `TenancyRootView` | `netbox/tenancy/api/views.py:10-15` | "Tenancy API root view", extends `APIRootView` |
| `TenancyQuery` | `netbox/tenancy/graphql/schema.py:8-25` | GraphQL schema entry point for tenancy |
| `path:tenancy/` | `netbox/netbox/urls.py` | Django route `tenancy/` → include |
| `path:api/tenancy/` | `netbox/netbox/urls.py` | Django route `api/tenancy/` → include |

**Ownership-related:**

| Symbol | Location | Description |
|---|---|---|
| `OwnerMixin` | `netbox/netbox/forms/mixins.py:143-163` | "Mixin for forms which adds ownership fields", extends `Form` |
| `AdminModel` | `netbox/netbox/models/__init__.py:235-255` | "A model which represents an administrative resource", extends `BookmarksMixin, CloningMixin, CustomLinksMixin` |

**Functional roles (a third organizational concept):**

| Symbol | Location | Description |
|---|---|---|
| `DeviceRole` | `netbox/dcim/models/devices.py:387-440` | "Devices are organized by functional role; for example, 'Core Switch' or 'File Server'", extends `NestedGroupModel` |
| `RackRole` | `netbox/dcim/models/racks.py:229-241` | "Racks can be organized by functional role, similar to Devices", extends `OrganizationalModel` |
| `CircuitType` | `netbox/circuits/models/circuits.py:32-40` | "Circuits can be organized by their functional role", extends `BaseCircuitType` |
| `VirtualCircuitType` | `netbox/circuits/models/virtual_circuits.py:22-30` | "Like physical circuits, virtual circuits can be organized by their functional role", extends `BaseCircuitType` |
| `Role` (ipam) | `netbox/ipam/models/ip.py:191-207` | "A Role represents the functional role of a Prefix or VLAN", extends `OrganizationalModel` |

### Step 2: Trace the tenancy model

**Tenancy** is a **dedicated Django application** (`TenancyConfig`, FOCUS: `netbox/tenancy/apps.py:4-13`, `name='tenancy'`). It is exposed at both the UI (`path:tenancy/`) and REST API (`path:api/tenancy/`) levels (FOCUS: `netbox/netbox/urls.py`). The `TenancyFilterSet` (FOCUS: `netbox/tenancy/filtersets.py:251-279`) is described as "An inheritable FilterSet for models which support Tenant assignment" — meaning any model that accepts a tenant FK can include this FilterSet mixin. Tenant assignment is therefore a **cross-cutting relationship** applied to many resource models via inheritance, not a property of any one model in isolation.

The table display layer shows a two-level hierarchy: `TenantColumn` displays the tenant itself and `TenantGroupColumn` displays the tenant's group (FOCUS: `netbox/tenancy/tables/columns.py:16-26`, `29-42`), both `called_by: TenancyColumnsMixin`. This establishes that tenants are grouped, making tenancy a **hierarchical classification of resources by organizational owner**.

Filtering at the form level (`TenancyForm`, `TenancyFilterForm`), at the GraphQL level (`TenancyFilterMixin`), and at the REST/query level (`TenancyFilterSet`) all exist as separate mixins — confirming tenancy is an add-on trait, not a mandatory model attribute.

### Step 3: Trace the ownership model

`OwnerMixin` (FOCUS: `netbox/netbox/forms/mixins.py:143-163`) is described as "Mixin for forms which adds ownership fields" and extends `Form`. Its imports include `core.models`, `extras.choices`, and `extras.models`, suggesting ownership is expressed through the `extras` app (not `tenancy`). `OwnerMixin` is used by `EventRuleForm`, `EventRuleBulkEditForm`, and `EventRuleFilterForm` (all in `netbox/extras/` — inferred from import patterns of the mech-2 clue, but also hinted here by `extras.choices`/`extras.models`). Ownership in this sense appears to relate to **who owns or authored an object** (such as an event rule), rather than the organizational grouping of a resource.

`AdminModel` (FOCUS: `netbox/netbox/models/__init__.py:235-255`) "represents an administrative resource" and extends `BookmarksMixin, CloningMixin, CustomLinksMixin`. This is a third kind of ownership: objects classified as administrative — distinct from both tenancy (organizational assignment) and form-level ownership (OwnerMixin).

### Step 4: Distinguish the three concepts using behavior annotations and inheritance

| Concept | Mechanism | Scope | Hierarchy |
|---|---|---|---|
| **Tenancy** | FK assignment via `TenancyFilterSet`/`TenancyForm` mixins | Any model that opts in | Two levels: Tenant → TenantGroup |
| **Ownership (`OwnerMixin`)** | Form mixin adding ownership fields, uses `extras` models | Forms (event rules, etc.) | Not hierarchical in clue |
| **Functional role** | `DeviceRole`, `RackRole`, `Role` (ipam), `CircuitType` — each extends `OrganizationalModel` or `NestedGroupModel` | Per-resource-type | Possibly nested (`NestedGroupModel` for `DeviceRole`) |

Tenancy is cross-app (a shared mixin reusable by any app). Functional roles are per-domain (each app defines its own role taxonomy). Ownership via `OwnerMixin` is specific to administrative/automation objects in `extras`.

### Step 5: Organizational structure

- **Tenancy app** (`netbox/tenancy/`) owns tenant/tenant-group models with a dedicated API root (`TenancyRootView`), UI routes, REST routes, and GraphQL schema (`TenancyQuery`).
- **Role taxonomies** are defined locally within each domain app (`netbox/dcim/`, `netbox/ipam/`, `netbox/circuits/`) using `OrganizationalModel` or `NestedGroupModel`.
- **Ownership fields** are mixed into forms via `OwnerMixin` in `netbox/netbox/forms/mixins.py`.

### Gaps / Uncertainty

`(GAPS)` reports this as a **STRUCTURAL** question with 69 symbols in L3 and 7 behavior annotations. No specific symbols are listed as explicitly uncovered. However:
- The exact fields added by `OwnerMixin` to forms are not visible in the clue.
- Whether `OwnerMixin` connects to a DB-level `owner` FK (to a User, Group, or Token) vs. a soft ownership concept cannot be determined from the clue alone.
- The complete set of models that use `TenancyFilterSet` is not enumerated (only the pattern is established).

## Synthesized Answer

**Tenancy** in NetBox is a first-class, **cross-cutting organizational concept** implemented as a standalone Django app (`TenancyConfig`, FOCUS: `netbox/tenancy/apps.py`). Resources can be assigned to a **Tenant** (which belongs to a **TenantGroup**), forming a two-level hierarchy (`TenantColumn`/`TenantGroupColumn`, FOCUS: `netbox/tenancy/tables/columns.py`). Any model can opt into tenancy by including the `TenancyFilterSet` mixin (FOCUS: `netbox/tenancy/filtersets.py`). Tenancy is accessible via the REST API (`path:api/tenancy/`), UI (`path:tenancy/`), and GraphQL (`TenancyQuery`) — all separate from other domain apps (FOCUS: `netbox/netbox/urls.py`).

**Resource ownership** (`OwnerMixin`, FOCUS: `netbox/netbox/forms/mixins.py`) is a distinct, form-level concept that adds ownership fields using `extras` models. It appears on automation objects (event rules, scripts) rather than on infrastructure records, implying it tracks authorship/responsibility within NetBox's automation layer rather than organizational assignment.

**Functional roles** (`DeviceRole`, `RackRole`, `Role`/ipam, `CircuitType`, etc.) are a third and separate concept: domain-specific taxonomies that classify resources by their infrastructure purpose (e.g., "Core Switch", "Customer" prefix role). These are owned by individual domain apps and extend `OrganizationalModel`/`NestedGroupModel` rather than any shared tenancy type.

In summary: **tenancy** = who (organizationally) owns a resource; **ownership via OwnerMixin** = who authored/is responsible for an automation object; **functional role** = what the resource does in the infrastructure — three orthogonal dimensions of classification.
