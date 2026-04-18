# Enterprise v4 (full-stack): ent-grafana-struct-2
Date: 2026-04-18

## Answer
The deep context and clue file both frame Grafana as a plugin-extensible platform: routes like `/a/:id/*`, plugin-backed datasource pages, and plugin lookup in datasource handling show where those extensions attach. Grafana supports three plugin surfaces: panel plugins, data source plugins, and app plugins. App plugins are the broadest surface because they can bundle data sources, panels, dashboards, and full Grafana pages into one package. The documented plugin catalog is an administrative surface available to Grafana Server Administrators and Organization Administrators. On the security side, Grafana uses plugin signatures to verify integrity and the Plugin Frontend Sandbox to isolate frontend plugin code.

## Synthesis
Grafana exposes panel, data source, and app plugins, but wraps them in admin-only catalog access plus signature and sandbox protections.
