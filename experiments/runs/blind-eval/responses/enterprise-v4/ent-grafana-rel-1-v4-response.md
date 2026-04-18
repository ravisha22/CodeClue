# Enterprise v4 (full-stack): ent-grafana-rel-1
Date: 2026-04-18

## Answer
The prompt’s auth and dashboard/folder context shows that Grafana access control is anchored on organizations and then narrowed from there. Every user belongs to at least one organization, and teams exist inside an organization rather than above it. A team can contain multiple users and has its own Member versus Admin distinction, while org permissions cover the broad set of org resources such as dashboards, folders, alerts, data sources, plugins, teams, and service accounts. Folder and dashboard permissions are more specific than those org permissions, so they can override the org-level role on the selected folder or dashboard. That makes the hierarchy user → organization/team membership → org-wide permissions → folder/dashboard overrides.

## Synthesis
Users and teams live inside orgs, org permissions cover the broad resource surface, and folder/dashboard ACLs are the local override layer.
