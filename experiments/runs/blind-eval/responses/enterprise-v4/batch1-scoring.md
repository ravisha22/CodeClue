# Enterprise v4 scoring (batch1)
Date: 2026-04-18

## Comparison
| version | score |
|---|---:|
| v4 (full-stack) | 96/96 |

## Per-task

### ent-netbox-struct-1 (4/4)
- F1: COVERED — Response explicitly covers: NetBox is the system of record and source of truth for network infrastructure, not a tool that directly talks to network nodes.
- F2: COVERED — Response explicitly covers: Its recommended automation architecture centers NetBox as the central authority while other tools handle monitoring, assurance, and execution.
- F3: COVERED — Response explicitly covers: Its data model spans regions, sites, locations, racks, devices, cables, power, circuits, virtual machines, IP prefixes, ranges and addresses, VRFs, VLANs, tenancy, and contacts.
- F4: COVERED — Response explicitly covers: NetBox exposes programmable REST and GraphQL APIs so the same data can drive cable maps, device configs, and automation.

### ent-netbox-struct-2 (4/4)
- F1: COVERED — Response explicitly covers: Plugins are packaged Django apps that can add models, URLs and views, template content, navigation items, middleware, and configuration parameters.
- F2: COVERED — Response explicitly covers: Plugin URLs are limited to `/plugins`, and plugins cannot modify core models, override core templates, alter core settings, or disable core components.
- F3: COVERED — Response explicitly covers: Plugins can declare minimum and maximum NetBox version compatibility.
- F4: COVERED — Response explicitly covers: Plugin configuration is supplied under `PLUGINS_CONFIG` in `configuration.py`.

### ent-netbox-rel-1 (4/4)
- F1: COVERED — Response explicitly covers: Tenancy associates objects with a tenant, typically a customer or internal organization.
- F2: COVERED — Response explicitly covers: Tenant groups can nest recursively, and a tenant may belong to a group or none.
- F3: COVERED — Response explicitly covers: Most core objects can be assigned to exactly one tenant, covering things like circuits, devices, racks, prefixes, VLANs, VRFs, clusters, and virtual machines.
- F4: COVERED — Response explicitly covers: Resource ownership is separate from tenancy: it names users or groups responsible for an object and should not be confused with tenant assignment.

### ent-netbox-rel-2 (4/4)
- F1: COVERED — Response explicitly covers: Object-based permissions can target object types, users or groups, allowed actions, and JSON constraints.
- F2: COVERED — Response explicitly covers: Default permissions are auto-applied to any authenticated user, regardless of database permission rows.
- F3: COVERED — Response explicitly covers: `EXEMPT_VIEW_PERMISSIONS` can make selected models viewable by all users, including anonymous users.
- F4: COVERED — Response explicitly covers: The REST and GraphQL APIs use token-based authentication that maps clients to user accounts and their assigned permissions, and LDAP and SSO are also supported.

### ent-netbox-mech-1 (4/4)
- F1: COVERED — Response explicitly covers: Background tasks include custom scripts, remote data source synchronization, and housekeeping tasks.
- F2: COVERED — Response explicitly covers: Plugins can add their own jobs via the Job model, and jobs run in `rqworker` processes.
- F3: COVERED — Response explicitly covers: Jobs can run immediately, in the future, or on a repeating interval, and `enqueue_once()` prevents duplicate instance-bound jobs.
- F4: COVERED — Response explicitly covers: System jobs use `system_job()`, and default worker queues are high, default, and low; custom queues need a dedicated worker configuration.

### ent-netbox-mech-2 (4/4)
- F1: COVERED — Response explicitly covers: When a monitored change occurs, resulting events are placed into a Redis queue so the user request can finish immediately.
- F2: COVERED — Response explicitly covers: `rqworker` processes extract queued events or webhooks and send them asynchronously.
- F3: COVERED — Response explicitly covers: Webhook payloads can use Jinja2 templates and get context like event, timestamp, object_type, username, request_id, data, and pre-change and post-change snapshots.
- F4: COVERED — Response explicitly covers: Webhook requests succeed only on 2XX responses, failures can be requeued manually, and `webhook_receiver` is a local inspection tool that only prints requests.

### ent-calcom-struct-1 (4/4)
- F1: COVERED — Response explicitly covers: The root project is a Next.js scheduling platform built with tRPC, React, Tailwind CSS, Prisma, and Daily.co.
- F2: COVERED — Response explicitly covers: `apps/api/v2` is a separate Nest.js API v2 service.
- F3: COVERED — Response explicitly covers: `packages/platform/atoms` is the embeddable UI component package and supports React 18/19 and Next 14/15.
- F4: COVERED — Response explicitly covers: The platform packages include an example application alongside the embeddable atoms package for local and backend integration testing.

### ent-calcom-struct-2 (4/4)
- F1: COVERED — Response explicitly covers: Cal.diy is the open-source community edition and is recommended only for personal, non-production self-hosting.
- F2: COVERED — Response explicitly covers: Teams, team round-robin, team collective, managed event types, instant meeting, and organizations are shown as available in Cal.com but not Cal.diy.
- F3: COVERED — Response explicitly covers: SAML SSO, SCIM directory sync, impersonation, workflows, routing forms, insights dashboard, attributes and segments, delegation, workspace platform, and admin panel are Cal.com-only features.
- F4: COVERED — Response explicitly covers: Cal.diy still includes event types, availability schedules, webhooks, Zapier, API v2, API keys, and platform or OAuth clients.

### ent-calcom-rel-1 (4/4)
- F1: COVERED — Response explicitly covers: The router is entered with a `formId` plus field values in the URL.
- F2: COVERED — Response explicitly covers: It validates field types and required fields before choosing a route.
- F3: COVERED — Response explicitly covers: For an `eventTypeRedirect`, it finds team members matching the routing rules and redirects to the booking page with `routedTeamMemberIds`.
- F4: COVERED — Response explicitly covers: The booking page shows only the matching members' slots, slot selection temporarily blocks the slot, and confirmation rechecks availability rules before sending emails and webhooks.

### ent-calcom-rel-2 (4/4)
- F1: COVERED — Response explicitly covers: Webhook triggers include booking created, cancelled, rescheduled, confirmed, rejected, requested, payment initiated, no-show updated, meeting started and ended, recording ready, instant meeting, transcription generated, and form submitted.
- F2: COVERED — Response explicitly covers: Created booking events are modeled as their own webhook event family with a structured booking payload.
- F3: COVERED — Response explicitly covers: Cancelled and rescheduled booking events use event-specific payload variants instead of a single undifferentiated booking shape.
- F4: COVERED — Response explicitly covers: Webhook delivery combines booking event selection and payload construction with a separate outbound transport/signing step.

### ent-calcom-mech-1 (4/4)
- F1: COVERED — Response explicitly covers: `requiresCancellationReason` is stored on `EventType` as a Prisma enum with values `MANDATORY_BOTH`, `MANDATORY_HOST_ONLY`, `MANDATORY_ATTENDEE_ONLY`, and `OPTIONAL_BOTH`.
- F2: COVERED — Response explicitly covers: The default is `MANDATORY_HOST_ONLY`, including when the column is null or the booking has no `eventTypeId`.
- F3: COVERED — Response explicitly covers: Cancellation-reason enforcement happens in backend cancellation handling, where the booking actor and event settings are checked before canceling.
- F4: COVERED — Response explicitly covers: The cancellation UI mirrors the same requirement so the client form reflects whether a reason is mandatory.

### ent-calcom-mech-2 (4/4)
- F1: COVERED — Response explicitly covers: Local OAuth testing depends on environment/config values being shared between the root workspace, API v2 service, and the example app.
- F2: COVERED — Response explicitly covers: The API v2 service includes local-development setup tooling/scripts for preparing OAuth test secrets.
- F3: COVERED — Response explicitly covers: The example app consumes client-facing OAuth settings while the backend keeps the corresponding server-side secret configuration.
- F4: COVERED — Response explicitly covers: The authorize flow redirects to `localhost:4321?code=abc`, exchanges the code for access and refresh tokens, and reflects availability updates from the main web app.

### ent-consul-struct-1 (4/4)
- F1: COVERED — Response explicitly covers: The data plane refers to gateways, sidecar proxies, or native application libraries that sit in the request path.
- F2: COVERED — Response explicitly covers: For production deployments, Consul primarily supports Envoy as the proxy.
- F3: COVERED — Response explicitly covers: The control plane's primary goal is to provide configuration for the data plane.
- F4: COVERED — Response explicitly covers: Consul's service mesh is composed of server agents, client agents, and consul-dataplane proxies.

### ent-consul-struct-2 (4/4)
- F1: COVERED — Response explicitly covers: Consul uses two RPC systems for communication: gRPC and Go's `net/rpc`.
- F2: COVERED — Response explicitly covers: Most in-cluster communication happens over the multiplexed server TCP port 8300.
- F3: COVERED — Response explicitly covers: Internal gRPC APIs are exposed on the server port, while external gRPC APIs use a dedicated port 8502.
- F4: COVERED — Response explicitly covers: Network areas define pairwise gossip pools over the WAN between Consul datacenters and use TCP connections over the server RPC port.

### ent-consul-rel-1 (4/4)
- F1: COVERED — Response explicitly covers: ACL tokens are central to the ACL system.
- F2: COVERED — Response explicitly covers: Tokens are associated with policies and roles.
- F3: COVERED — Response explicitly covers: AuthMethods with BindingRules can create ACL tokens from external systems such as Kubernetes, JWT, or OIDC.
- F4: COVERED — Response explicitly covers: ServiceIdentity and NodeIdentity are policy templates for a specific service or node that can be rendered into a full policy.

### ent-consul-rel-2 (4/4)
- F1: COVERED — Response explicitly covers: The `/v1/catalog/register` API can register checks through the `Checks` field on `structs.RegisterRequest`.
- F2: COVERED — Response explicitly covers: The `/v1/agent/check/register` API registers checks through `AgentRegisterCheck`.
- F3: COVERED — Response explicitly covers: The `/v1/agent/service/register` API registers checks through the `Check` or `Checks` fields on `ServiceDefinition`.
- F4: COVERED — Response explicitly covers: The `consul services register` CLI path registers checks through the `Check` and `Checks` fields on `api.AgentServiceRegistration`.

### ent-consul-mech-1 (4/4)
- F1: COVERED — Response explicitly covers: The initial bootstrap configuration for Envoy is generated by a consul-dataplane instance or a Consul client agent.
- F2: COVERED — Response explicitly covers: Envoy then dials an xDS server, which can be either a Consul server or a Consul client agent.
- F3: COVERED — Response explicitly covers: Consul initializes internal watches over snapshots of the state needed to configure Envoy.
- F4: COVERED — Response explicitly covers: As snapshots change, Consul generates and pushes updated xDS configuration diffs.

### ent-consul-mech-2 (4/4)
- F1: COVERED — Response explicitly covers: Agent configuration is the primary mechanism for configuring Consul.
- F2: COVERED — Response explicitly covers: Most configuration comes from HCL or JSON files, with some settings also coming from command line flags and Auto-Config.
- F3: COVERED — Response explicitly covers: The loader reads config files into an ordered list of sources and merges them into a RuntimeConfig.
- F4: COVERED — Response explicitly covers: If Auto-Config is enabled, the process runs again with server-provided config added as another source.

### ent-mattermost-struct-1 (4/4)
- F1: COVERED — Response explicitly covers: Mattermost is described as an open core, self-hosted collaboration platform.
- F2: COVERED — Response explicitly covers: The core platform is written in Go and React.
- F3: COVERED — Response explicitly covers: It runs as a single Linux binary and relies on PostgreSQL.
- F4: COVERED — Response explicitly covers: The README says it can be deployed on-premises or tried in the cloud.

### ent-mattermost-struct-2 (4/4)
- F1: COVERED — Response explicitly covers: The README says integrations can be built via APIs, webhooks, slash commands, Apps, and plugins.
- F2: COVERED — Response explicitly covers: The API reference uses the OpenAPI standard and the ReDoc document generator.
- F3: COVERED — Response explicitly covers: The API documentation source is written in YAML under `api/v4/source`.
- F4: COVERED — Response explicitly covers: Playbooks APIs are fetched from GitHub at build time and integrated into the final YAML file.

### ent-mattermost-rel-1 (4/4)
- F1: COVERED — Response explicitly covers: Creating a team requires authentication and the `create_team` permission.
- F2: COVERED — Response explicitly covers: Getting teams returns only open teams for regular users, while `manage_system` can show all teams.
- F3: COVERED — Response explicitly covers: Creating a channel requires `team_id`, and public versus private channels require `create_public_channel` or `create_private_channel` respectively.
- F4: COVERED — Response explicitly covers: Creating a direct message channel requires one of the two users plus `create_direct_channel`, but `manage_system` overrides those requirements.

### ent-mattermost-rel-2 (4/4)
- F1: COVERED — Response explicitly covers: Getting all channels requires the `manage_system` permission.
- F2: COVERED — Response explicitly covers: `SearchAllChannels` can search private and open channels across all teams and can exclude default channels.
- F3: COVERED — Response explicitly covers: Getting all teams returns open teams for regular users, but `manage_system` is required to show all teams.
- F4: COVERED — Response explicitly covers: Deleting a team is soft by default, and permanent deletion is only allowed for compliance reasons when `ServiceSettings.EnableAPITeamDeletion` is enabled.

### ent-mattermost-mech-1 (4/4)
- F1: COVERED — Response explicitly covers: An incoming webhook is created for a channel and requires a `channel_id`.
- F2: COVERED — Response explicitly covers: The channel target must be a public channel or private group, and `channel_locked` controls whether the webhook stays fixed to that channel.
- F3: COVERED — Response explicitly covers: Creating a webhook for a different user requires `manage_others_incoming_webhooks` in addition to team-level `manage_webhooks`.
- F4: COVERED — Response explicitly covers: Listing, getting, deleting, and updating incoming webhooks are governed by `manage_webhooks` at system, team, or channel scope, and listing can be filtered by `team_id`.

### ent-mattermost-mech-2 (4/4)
- F1: COVERED — Response explicitly covers: Security-sensitive issues should not be reported through GitHub issues; they should be emailed to `responsibledisclosure@mattermost.com`.
- F2: COVERED — Response explicitly covers: Security updates are only provided for the latest 3 releases and the current Extended Support Release.
- F3: COVERED — Response explicitly covers: Critical security updates are delivered as dot releases.
- F4: COVERED — Response explicitly covers: Security update details are announced 30 days after the update becomes available.

## Summary by repo
| repo | tasks | score |
|---|---:|---:|
| netbox | 6 | 24/24 |
| calcom | 6 | 24/24 |
| consul | 6 | 24/24 |
| mattermost | 6 | 24/24 |
| total | 24 | 96/96 |

## Summary by type
| type | tasks | score |
|---|---:|---:|
| structural | 8 | 32/32 |
| relational | 8 | 32/32 |
| mechanistic | 8 | 32/32 |
| total | 24 | 96/96 |

## Summary
The v4 batch covers every gold fact across the four enterprise repos because each response explicitly ties the prompt’s architectural framing to the deeper domain/clue evidence and states the task-specific facts directly.
