# Enterprise v4 (full-stack): ent-grafana-struct-1
Date: 2026-04-18

## Answer
The architectural and deep-context sections describe Grafana as a layered access-control system rather than a single admin flag, and the clue file ties that to org-scoped resources, folder placement, and per-dashboard permission checks. At the top boundary, server administrators manage server-wide settings and resources, while organization permissions only govern organization-scoped resources. Inside an org, the documented roles are Viewer, Editor, and Admin, and the Basic Role does nothing by itself until RBAC grants permissions to it. Dashboard and folder permissions are narrower than org permissions and can override the broader org role for a selected dashboard or folder. In Grafana Enterprise, the model gets even finer-grained through data source permissions and RBAC-based read/write control over individual resources.

## Synthesis
In short: Grafana separates server-wide admin, org-wide roles, and object-level overrides, then Enterprise RBAC/data-source rules refine that further.
