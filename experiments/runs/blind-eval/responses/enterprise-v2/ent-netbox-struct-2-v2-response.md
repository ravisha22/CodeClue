# Enterprise v2: ent-netbox-struct-2
Date: 2026-04-17

## Question
What can NetBox plugins extend, and what core boundaries do they not cross?

## Reasoning Scaffold

### Step 1: Identify plugin-related symbols in FOCUS, SYM, and INDEX

Key symbols from FOCUS relevant to the plugin system:

| Symbol | Location | Role |
|---|---|---|
| `PluginConfig` | `netbox/netbox/plugins/__init__.py:44-168` | Base class for every plugin |
| `PluginTemplateExtension` | `netbox/netbox/plugins/templates.py:9-114` | Template injection API |
| `InstalledPluginsAPIView` | `netbox/netbox/plugins/views.py:15-42` | REST API endpoint for listing plugins |
| `PluginsAPIRootView` | `netbox/netbox/plugins/views.py:46-81` | Root of the plugin API namespace |
| `get_local_plugins` | `netbox/core/plugins.py:74-126` | Discovers locally installed plugins |
| `get_catalog_plugins` | `netbox/core/plugins.py:129-241` | Retrieves catalog/registry plugin list |
| `get_cached_plugins` | `netbox/core/views.py:765-775` | Serves cached plugin list to views |
| `get_installed_plugins` | `netbox/netbox/plugins/utils.py:13-26` | Maps plugin names to versions via registry |
| `ready` | `netbox/netbox/plugins/__init__.py:101-135` | Django AppConfig lifecycle hook for plugins |
| `_load_resource` | `netbox/netbox/plugins/__init__.py:87-99` | Loads a named plugin resource (e.g. URLs, filtersets) |
| `plugin_alerts`, `plugin_buttons`, `plugin_head`, `plugin_left_page`, `plugin_full_width_page` | `netbox/utilities/templatetags/plugins.py` | Template tag rendering hooks |
| `_get_registered_content` | `netbox/utilities/templatetags/plugins.py:11` | "Given an object and a PluginTemplateExtension method…" — dispatches per hook point |

Also relevant from INDEX and paths:
- `path:plugins/` → `views.PluginListView.as_view` (`netbox/core/urls.py`) — admin UI plugin list.
- `path:plugins/<str:name>/` → `views.PluginView.as_view` (`netbox/core/urls.py`) — per-plugin detail.
- `path:api/plugins/` → `include` (`netbox/netbox/urls.py`) — plugins get their own API namespace.
- `path:installed-plugins/` → `InstalledPluginsAPIView.as_view` (`netbox/netbox/plugins/urls.py`).
- `path:value` → `PluginsAPIRootView.as_view` (`netbox/netbox/plugins/urls.py`).

### Step 2: Trace what plugins can extend

**2a. Class registration — `PluginConfig`**
`PluginConfig` (FOCUS: `netbox/netbox/plugins/__init__.py:44-168`) is a subclass of Django's `AppConfig` with added attrs (`author`, `author_email`, `description`, `version`) and raises `IncompatiblePluginError` / `ImproperlyConfigured`. Plugins declare themselves by subclassing `PluginConfig`. During Django startup, `ready()` (FOCUS: `netbox/netbox/plugins/__init__.py:101-135`) iterates over `search_indexes` and calls `_load_resource` to load each named extension point.

**2b. Loading plugin resources — `_load_resource`**
`_load_resource` (FOCUS: `netbox/netbox/plugins/__init__.py:87-99`) has the behavior `GUARD((path := getattr(self, name, None)) -> return import_string(f'{s...'))` — it reads an attribute on the `PluginConfig` (e.g. `search_indexes`) and dynamically imports the named module. This is the mechanism by which plugins register custom search indexes and other resources.

**2c. Template injection — `PluginTemplateExtension`**
`PluginTemplateExtension` (FOCUS: `netbox/netbox/plugins/templates.py:9-114`) has `models=None` and a `render` method. Plugins subclass this to inject content into core NetBox templates. The injection points are exposed as Django template tags in `netbox/utilities/templatetags/plugins.py`:

- `plugin_head` — injects into `<head>` (FOCUS: `templatetags/plugins.py:49-53`)
- `plugin_buttons` — renders plugin-added buttons (FOCUS: `templatetags/plugins.py:73-77`)
- `plugin_alerts` — renders plugin-added alerts (FOCUS: `templatetags/plugins.py:81-85`)
- `plugin_left_page` — injects left-column content (FOCUS: `templatetags/plugins.py:89-93`)
- `plugin_full_width_page` — injects full-width content (FOCUS: `templatetags/plugins.py:105-109`)

All five delegate to `_get_registered_content` (SYM: `netbox/utilities/templatetags/plugins.py:11`), which looks up registered `PluginTemplateExtension` instances for the current object and calls the appropriate method.

**2d. URL namespacing**
`path:api/plugins/` (FOCUS: `netbox/netbox/urls.py`) and `path:plugins/` are reserved namespaces into which each installed plugin can mount its own URL configurations. `PluginsAPIRootView` (FOCUS) enumerates these. Plugins thus get their own API root within the `/api/plugins/` prefix.

**2e. Discovery and versioning**
`get_local_plugins` (FOCUS: `netbox/core/plugins.py:74-126`) "Return[s] a dictionary of all locally-installed plugins, mapped by name" using `ACCUMULATE(settings.PLUGINS loop -> result)`. `get_installed_plugins` (FOCUS: `netbox/netbox/plugins/utils.py:13-26`) reads `registry['plugins']` to map names to versions. This establishes that plugins are declared in Django's `settings.PLUGINS` list and tracked in a central registry.

**2f. Bulk edit forms**
`NetBoxModelBulkEditForm` (FOCUS: `netbox/netbox/forms/bulk_edit.py:20-71`) "Base form for modifying multiple NetBox objects… in bulk via the UI", and `_extend_nullable_fields` is called by its `__init__`. Plugins that add models can build on this base form.

**2g. ViewSet extension**
`NetBoxModelViewSet` (FOCUS: `netbox/netbox/api/viewsets/__init__.py:107-259`) is the base DRF viewset for all NetBox model APIs; plugins can subclass it for their own models.

### Step 3: Trace what core boundaries plugins do NOT cross

**Template rendering internals**: `PluginTemplateExtension.render` raises `NotImplementedError` and `TypeError` (FOCUS: `templates.py`), meaning plugins must implement `render` themselves — the core does not provide default rendering for plugin content; it only provides the injection points.

**Core model logic**: Plugins integrate via `PluginConfig` and template tags but cannot alter the behavior of `NetBoxModelViewSet.perform_create` (listed in GAPS as uncovered). Plugins do not directly override core viewset mutation methods.

**`_load_resource` internals**: The exact set of named resources plugins can register (i.e., the full list of attribute names accepted by `_load_resource`) is partially visible (`search_indexes`) but `(GAPS)` lists `_load_resource` as uncovered. The complete set of extension points loaded by `ready()` cannot be fully determined from the clue alone.

**Core URL router**: `NetBoxRouter` (FOCUS: `netbox/netbox/api/routers.py`) is used for core app URL registration. Plugins receive their own API namespace under `api/plugins/` but do not modify the core router registration.

### Gaps / Uncertainty

`(GAPS)` explicitly lists as uncovered: `_load_resource` (full behavior), `render` (exact template rendering), `ready` (full loop body), and `perform_create`. Therefore:
- The complete enumeration of plugin-registerable resource types (beyond `search_indexes`) cannot be confirmed.
- The full set of UI injection points (whether plugins can inject into non-object views or only object-detail views) cannot be confirmed—`models=None` on `PluginTemplateExtension` suggests scope filtering but its exact semantics are not resolvable from the clue.

## Synthesized Answer

**What plugins can extend:**
1. **App registration**: Plugins declare a `PluginConfig` subclass (extends `AppConfig`) and are listed in `settings.PLUGINS`; discovery is via `get_local_plugins` / `get_installed_plugins` (FOCUS: `netbox/core/plugins.py`, `netbox/netbox/plugins/utils.py`).
2. **Template injection points**: Five named slots in core templates — `<head>`, buttons, alerts, left-page, and full-width — via `PluginTemplateExtension` subclasses (FOCUS: `netbox/netbox/plugins/templates.py`; `netbox/utilities/templatetags/plugins.py`).
3. **URL namespaces**: Plugins get mounted under both `/plugins/` (UI) and `/api/plugins/` (REST), with `PluginsAPIRootView` and `InstalledPluginsAPIView` serving discovery endpoints (FOCUS: `netbox/netbox/plugins/views.py`, `netbox/netbox/urls.py`).
4. **Search indexes and other named resources**: `ready()` calls `_load_resource` per registered resource name (FOCUS: `netbox/netbox/plugins/__init__.py:101-135`).
5. **API views and forms**: Plugins can subclass `NetBoxModelViewSet` and `NetBoxModelBulkEditForm` for their own models (FOCUS: `netbox/netbox/api/viewsets/__init__.py`, `netbox/netbox/forms/bulk_edit.py`).

**Core boundaries plugins do not cross (from clue):**
- Core model mutation logic (`perform_create` — listed in GAPS as uncovered and not exposed as a plugin hook).
- The core URL router registration for built-in apps; plugins are strictly additive under their own namespace.
- Internal rendering of `PluginTemplateExtension.render` — the core only calls the method, it does not provide fallback logic (raises `NotImplementedError`/`TypeError` if not implemented).
- The full internal behavior of `_load_resource` and the `ready()` lifecycle are not fully determinable from the clue, so the complete boundary of registerable resource types remains uncertain `(GAPS)`.
