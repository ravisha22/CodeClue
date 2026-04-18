# Enterprise v3 (arch-enhanced): ent-netbox-struct-2
Date: 2026-04-18

## Answer
NetBox plugins are packaged Django app-style extensions. `PluginConfig` is explicitly a subclass of Django `AppConfig` for NetBox plugins, and NetBox keeps separate plugin routes and plugin API roots under `plugins/` and `api/plugins/` (PluginConfig, netbox/netbox/plugins/__init__.py:44-168; path:plugins/, netbox/netbox/urls.py:1-97; path:api/plugins/, netbox/netbox/urls.py:1-97; InstalledPluginsAPIView, netbox/netbox/plugins/views.py:15-42; PluginsAPIRootView, netbox/netbox/plugins/views.py:46-81).

The clue shows several concrete extension surfaces. Plugins can contribute plugin-provided content into core pages through `PluginTemplateExtension`, and NetBox renders registered plugin alerts, buttons, head content, full-width page content, and left-page content with dedicated template tags (PluginTemplateExtension, netbox/netbox/plugins/templates.py:9-114; plugin_alerts, netbox/utilities/templatetags/plugins.py:81-85; plugin_buttons, netbox/utilities/templatetags/plugins.py:73-77; plugin_head, netbox/utilities/templatetags/plugins.py:49-53; plugin_full_width_page, netbox/utilities/templatetags/plugins.py:105-109; plugin_left_page, netbox/utilities/templatetags/plugins.py:89-93). NetBox also catalogs and lists installed plugins through `get_local_plugins`, `get_catalog_plugins`, and `get_installed_plugins` (get_local_plugins, netbox/core/plugins.py:74-126; get_catalog_plugins, netbox/core/plugins.py:129-241; get_installed_plugins, netbox/netbox/plugins/utils.py:13-26).

The plugin layer also includes compatibility checks. `PluginConfig` imports `packaging` and can raise `IncompatiblePluginError`, so plugin loading is version-gated rather than unconditional (PluginConfig, netbox/netbox/plugins/__init__.py:44-168).

## Gaps
The clue supports template/UI and route-level extension, but it does **not** explicitly state the full boundary list from the question: it does not say plugins cannot modify core models, override core templates, alter core settings, or disable core components, and it does not surface `PLUGINS_CONFIG` in `configuration.py` (GAPS, ent-netbox-struct-2-v3.prompt.md:298-301).
