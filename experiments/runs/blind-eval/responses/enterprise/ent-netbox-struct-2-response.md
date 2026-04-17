# Enterprise Eval: ent-netbox-struct-2
Date: 2026-04-17

## Question

What can NetBox plugins extend, and what core boundaries do they not cross?

---

## Reasoning Scaffold

### 1. Relevant Modules & Symbols Identified

The clue file surfaces two primary clusters of evidence:

- **Plugin infrastructure** — `netbox/netbox/plugins/` (`PluginConfig`, `PluginTemplateExtension`, `InstalledPluginsAPIView`, `PluginsAPIRootView`, `_load_resource`, `get_installed_plugins`)
- **Plugin template-tag injection points** — `netbox/utilities/templatetags/plugins.py` (eight `plugin_*` template tags plus `_get_registered_content`)
- **Core boundaries** — `netbox/core/` (own `AppConfig`, middleware, API root, GraphQL schema), `netbox/netbox/api/` (`NetBoxModelViewSet`, `NetBoxRouter`), and domain apps (`dcim/`, `ipam/`, `circuits/`, etc.)

### 2. What Plugins CAN Extend

#### 2.1 Application Configuration via `PluginConfig`

`PluginConfig` (FOCUS: `netbox/netbox/plugins/__init__.py:44-168`) is described as a *"Subclass of Django's built-in AppConfig class, to be used for NetBox plugins."* It exposes declarative attributes (`author`, `author_email`, `description`, `version`) and calls `_load_resource` to load plugin-specific assets. It raises `IncompatiblePluginError` and `ImproperlyConfigured` when a plugin violates version or configuration constraints. **This is the formal entry point every plugin must use** to register itself with NetBox's plugin subsystem.

#### 2.2 Template Content Injection via `PluginTemplateExtension`

`PluginTemplateExtension` (FOCUS: `netbox/netbox/plugins/templates.py:9-114`) is defined as a class *"used to register plugin content to be injected into core NetBox templates."* It declares `models=None` and calls `render`, raising `NotImplementedError` and `TypeError` for incorrect implementations. Plugins subclass this to supply content that is rendered in predefined slots.

The eight injection slots are exposed as Django template tags (all in `netbox/utilities/templatetags/plugins.py`), each delegating to `_get_registered_content`:

| Template Tag | Line | Purpose (from clue) |
|---|---|---|
| `plugin_head` | 49-53 | *"Render any head content embedded by plugins"* |
| `plugin_navbar` | 57-61 | *"Render any navbar content embedded by plugins"* |
| `plugin_list_buttons` | 65-69 | *"Render all list buttons registered by plugins"* |
| `plugin_buttons` | 73-77 | *"Render all buttons registered by plugins"* |
| `plugin_alerts` | 81-85 | *"Render all object alerts registered by plugins"* |
| `plugin_left_page` | 89-93 | *"Render all left page content registered by plugins"* |
| `plugin_right_page` | 97-101 | *"Render all right page content registered by plugins"* |
| `plugin_full_width_page` | 105-109 | *"Render all full width page content registered by plugins"* |

The dispatcher `_get_registered_content` (SYM: `netbox/utilities/templatetags/plugins.py:11`) is annotated *"Given an object and a PluginTemplateExtension m…"*, confirming it resolves registered extensions per-object and per-slot.

#### 2.3 Plugin Discovery & Catalog

- `get_local_plugins` (FOCUS: `netbox/core/plugins.py:74-126`) iterates `settings.PLUGINS` and accumulates `Plugin` / `PluginAuthor` records.
- `get_catalog_plugins` (FOCUS: `netbox/core/plugins.py:129-241`) fetches the full plugin catalog using `Plugin`, `PluginAuthor`, `PluginVersion`, and paging helpers.
- `get_installed_plugins` (FOCUS: `netbox/netbox/plugins/utils.py:13-26`) reads from `registry['plugins']` to map installed plugin names to versions.
- `get_cached_plugins` (FOCUS: `netbox/core/views.py:765-775`) is called by `PluginListView` and `PluginView` to serve cached plugin data.
- `InstalledPluginsAPIView` (FOCUS: `netbox/netbox/plugins/views.py:15-42`) provides an *"API view for listing all installed plugins"* (with `schema=None`, meaning it is excluded from the generated OpenAPI schema).
- `PluginsAPIRootView` (FOCUS: `netbox/netbox/plugins/views.py:46-81`) provides the API root for all plugin endpoints (also `schema=None`).

These together form a managed lifecycle: plugins are declared via `PluginConfig`, discovered through `settings.PLUGINS`, registered in an internal `registry`, and surfaced via both UI views and API views.

#### 2.4 Forms: Custom Fields Mixin

`CustomFieldsMixin` (FOCUS: `netbox/netbox/forms/mixins.py:39-89`) is documented as *"Extend a Form to include custom field support"* and raises `NotImplementedError`. This suggests plugins (or any code) can attach custom fields to forms, a known NetBox extensibility surface.

### 3. Core Boundaries Plugins Do NOT Cross

#### 3.1 Core Application Configuration

`CoreConfig` (FOCUS: `netbox/core/apps.py:20-48`) is NetBox's own `AppConfig` subclass (`name='core'`). It is distinct from `PluginConfig` — plugins subclass `PluginConfig`, **not** `CoreConfig`. The core app's configuration, middleware registration, and startup hooks are not accessible to plugins through the plugin API.

#### 3.2 Core Middleware

`CoreMiddleware` (FOCUS: `netbox/netbox/middleware.py:29-105`) handles request-level processing for the entire application. No clue evidence shows any plugin hook into or extension of the middleware pipeline.

#### 3.3 Core API Infrastructure

- `NetBoxModelViewSet` (FOCUS: `netbox/netbox/api/viewsets/__init__.py:107-259`) extends DRF's `ModelViewSet` with bulk operations, object snapshots, and `PermissionDenied` enforcement. It forms the base for all core API endpoints. Plugins are not shown to modify or override its behavior; they receive their own API root (`PluginsAPIRootView`) separate from the core roots like `CoreRootView`.
- `NetBoxRouter` (FOCUS: `netbox/netbox/api/routers.py:4-29`) extends DRF's `DefaultRouter`. Plugin API endpoints route through `PluginsAPIRootView`, not through the core router directly.
- `CoreRootView` (FOCUS: `netbox/core/api/views.py:30-35`) is the *"Core API root view"*. There is no evidence plugins can register endpoints under this root.
- `NetBoxAutoSchema` and `NetBoxDjangoFilterExtension` (FOCUS: `netbox/core/api/schema.py`) control OpenAPI schema generation. Plugin API views explicitly set `schema=None`, meaning they opt out of the core schema pipeline entirely.

#### 3.4 Core GraphQL Schema

`CoreQuery` (FOCUS: `netbox/core/graphql/schema.py:8-13`) defines the core GraphQL root. No clue evidence shows a plugin mechanism for injecting into or extending this schema.

#### 3.5 Core Domain Models

Domain apps — `dcim/`, `ipam/`, `circuits/`, `tenancy/`, etc. — own their models (e.g., `DeviceRole` at `netbox/dcim/models/devices.py:387-440`). The TREE shows 1107 files in `netbox/` across 10+ subpackages. Plugin template extensions can *render content alongside* these objects (via the eight template-tag slots), but the clue provides no evidence that plugins can alter core model schemas, migrations, or business logic.

#### 3.6 Job Enqueueing

`enqueue` (SYM: `netbox/netbox/jobs.py:150`) is described as *"Enqueue a new Job."* While plugins could conceivably call this, the clue does not show it as part of the plugin API surface.

#### 3.7 Query-Level Restrictions

`RestrictedPrefetch` (FOCUS: `netbox/utilities/querysets.py:12-35`) extends Django's `Prefetch` with user/action-scoped restrictions. This is a core query mechanism, not exposed through the plugin extension API.

### 4. GAPS — What Cannot Be Determined

The GAPS declaration states:

- **type: STRUCTURAL** — the analysis is answerable from L0–L2 (tree, index, symbol signatures), meaning deeper behavioral/runtime analysis was not performed.
- **coverage: 80 symbols in L3, 17 with behavior annotations** — only a fraction of the 7826+ total symbols were deeply inspected.
- **uncovered symbols**: `_get_form_field`, `get_bound_field`, `get_current_querysets`, `restrict` — these were not analyzed.

Consequently, the following **cannot be determined** from the provided clues:

1. **Whether plugins can register custom Django models or database migrations** — no FOCUS entry covers plugin model registration or migration hooks.
2. **Whether plugins can register custom GraphQL types or queries** — `CoreQuery` is shown but no plugin GraphQL extension mechanism is evidenced.
3. **Whether plugins can register background jobs** — `enqueue` exists but its relationship to the plugin API is not documented in the clues.
4. **Whether plugins can extend or override permissions/object restrictions** — `restrict` is explicitly listed as uncovered, and `RestrictedPrefetch` shows no plugin hook.
5. **Whether plugins can add custom filter backends or form fields** — `_get_form_field` and `get_bound_field` are uncovered.
6. **Whether plugins can register middleware** — no evidence either way.
7. **The full set of `PluginConfig` declarative attributes** — only `author`, `author_email`, `description`, `version` are shown; additional attributes (e.g., for registering menu items, nav links, or custom validators) may exist but are not in the clue file.
8. **Runtime behavior of `_load_resource`** — called by `PluginConfig` but its implementation details are not in FOCUS.

### 5. Synthesis

**What plugins can extend** (grounded in clues):

- **Application registration**: Plugins must subclass `PluginConfig` (extends `AppConfig`), declaring metadata and loading resources via `_load_resource`. Compatibility is enforced through `IncompatiblePluginError` / `ImproperlyConfigured` exceptions.
- **Template content**: Plugins subclass `PluginTemplateExtension` to inject rendered content into **eight well-defined slots** in core templates — head, navbar, list buttons, object buttons, alerts, left page, right page, and full-width page content. Injection is mediated by `_get_registered_content` and rendered per-object.
- **API surface**: Plugins receive a dedicated API namespace under `PluginsAPIRootView`, with `InstalledPluginsAPIView` providing plugin metadata. Both views set `schema=None`, separating them from the core OpenAPI schema.
- **Forms**: `CustomFieldsMixin` provides a pattern for extending forms with custom fields, available to plugins.

**Core boundaries plugins do not cross** (grounded in clues):

- **Core app configuration** (`CoreConfig`) is separate from `PluginConfig`; plugins do not modify the core app's startup.
- **Middleware pipeline** (`CoreMiddleware`) has no plugin injection point.
- **Core API routing** (`NetBoxRouter`, `CoreRootView`) and **schema generation** (`NetBoxAutoSchema`, `NetBoxDjangoFilterExtension`) are not extensible by plugins.
- **Core GraphQL schema** (`CoreQuery`) shows no plugin extension mechanism.
- **Domain model definitions** (e.g., `DeviceRole`, models in `dcim/`, `ipam/`, etc.) are owned by core apps; plugins render alongside objects but do not alter model schemas.
- **Query-level restrictions** (`RestrictedPrefetch`, uncovered `restrict`) are internal to the core permission system.
- **Bulk edit infrastructure** (`NetBoxModelBulkEditForm`, `_extend_nullable_fields`) is core-internal with no documented plugin hook.

The plugin system follows a **"extend at the edges, not in the core"** architecture: plugins can add content, register themselves, and expose their own API endpoints, but the core middleware, routing, schema, model definitions, and permission enforcement remain under NetBox's exclusive control.
