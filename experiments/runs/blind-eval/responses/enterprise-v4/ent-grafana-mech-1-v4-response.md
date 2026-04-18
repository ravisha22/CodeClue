# Enterprise v4 (full-stack): ent-grafana-mech-1
Date: 2026-04-18

## Answer
The prompt’s setup and lifecycle clues show datasource management as an admin-controlled registration flow followed by plugin-specific querying. Only organization admins can add or remove data sources, and they do that from the Configuration or Data Sources/Connections area. Setup starts in Connections, where the admin searches for the target backend and fills in source-specific settings such as URL, auth, headers, or plugin JSON. Grafana ships both built-in core datasources and plugin/custom datasources, so the configuration step also determines which plugin implementation will own the later query experience. Once configured, querying happens through that datasource’s own query editor UI—often with autocomplete or visual builders—and the saved datasource is then reused by dashboards, Explore, and alerting.

## Synthesis
Datasource management goes from org-admin setup in Connections to plugin-owned query editors that power dashboards, Explore, and alerts.
