# Mattermost Server Deep Domain Context

## Context map
**Files reviewed:** root `README.md`; `server/`; `server/channels/README.md`; `server/channels/store/store.go`; `server/public/model/{user,team,channel,post,session,oauth,token,websocket_message}.go`; `server/channels/api4/{api,handlers,user,oauth,plugin,websocket}.go`; `server/channels/app/{authentication,login,session}.go`; `server/channels/app/platform/{service,session,web_hub,web_conn}.go`; `server/channels/web/{context,handlers}.go`; `server/channels/wsapi/{api,websocket_handler,user,system}.go`; `server/public/plugin/{api,hooks,client,environment,supervisor}.go`.

## 1) What the Mattermost server is
Mattermost is an open-core collaboration platform whose server side is primarily Go code. The root README frames it as a self-hosted collaboration system for chat, workflows, voice/screen sharing, and AI integration, shipped as a single Linux binary and backed by PostgreSQL. In the repo, the server is not a monolith in one package; it is layered into routing, business logic, persistence, platform/runtime services, and an SDK/runtime for plugins.

At the top level under `server/`, the most important architectural areas are:
- `cmd/`: entrypoints like the main `mattermost` binary and tooling.
- `channels/`: the core product logic for chat/collaboration features.
- `public/`: stable/shared public packages, especially `model/` and `plugin/`.
- `platform/`: cross-cutting runtime services like cache, search, filestore, remote cluster support.
- `config/`, `enterprise/`, `tests/`: configuration, enterprise extensions, and test assets.

Within `server/channels/`, the structure is especially important:
- `api4/`: REST API handler layer.
- `app/`: application/business logic and orchestration.
- `store/`: persistence abstractions and implementations.
- `web/`: generic HTTP handler/middleware/context machinery.
- `wsapi/`: websocket request-action handlers from client to server.
- `audit/`, `db/`, `jobs/`, `utils/`: supporting infrastructure.

A good mental model is: **`api4` parses HTTP + permissions, `app` enforces business rules, `store` persists entities, `platform` provides runtime primitives, `public/model` defines contracts, and `public/plugin` opens extension points.**

## 2) Persistence and package layering
`server/channels/store/store.go` defines a very broad `Store` interface. It exposes sub-stores for almost every first-class entity or subsystem: `Team`, `Channel`, `Post`, `Thread`, `User`, `Session`, `OAuth`, `Token`, `Plugin`, `Group`, `Draft`, `ScheduledPost`, `View`, `AccessControlPolicy`, `ContentFlagging`, `Recap`, `ReadReceipt`, and many more. This tells you Mattermost’s domain is wide, but still normalized around a store-per-aggregate pattern.

The store implementation is layered:
- `sqlstore/`: concrete SQL/Postgres-backed storage; lots of `*_store.go` files per entity.
- `localcachelayer/`: in-process caching wrappers.
- `searchlayer/`: search-optimized wrappers.
- `timerlayer/`: timing/instrumentation wrappers.
- `retrylayer/`: retry behavior.

That layout strongly suggests an onion of decorators around the base SQL store rather than logic embedded directly in handlers. The `server/channels/README.md` also emphasizes performance discipline: avoid unnecessary round trips, run `EXPLAIN ANALYZE`, think at 100M+ post scale, and treat permission enforcement as a first-class concern.

## 3) Core domain model
The canonical shared types live under `server/public/model/`.

### User
`model.User` is the identity anchor. It includes basic profile fields plus auth state and feature flags:
- identity: `Id`, `Username`, `Email`
- auth: `Password`, `AuthData`, `AuthService`, `EmailVerified`
- authorization: `Roles`
- UX/profile: nickname, first/last name, position, locale, timezone, notify props
- security: `FailedAttempts`, `MfaActive`, `MfaSecret`, `LastPasswordUpdate`
- product roles: `IsBot`, guest/system roles via `Roles`, welcome-email flag, ToS acceptance metadata

A key design detail is that `AuthService`/`AuthData` allow users to be backed by email/password, LDAP, SAML/OAuth-related identities, and magic-link style auth without changing the main user shape.

### Team
`model.Team` is a workspace-like boundary. Important fields:
- `DisplayName`, `Name`, `Description`, `Email`
- `Type` (`O` open or `I` invite/private)
- `InviteId`, `AllowOpenInvite`
- policy/governance hooks: `SchemeId`, `GroupConstrained`, `PolicyID`

This means teams are not just cosmetic containers; they participate in permission schemes, group sync, and access-control policy enforcement.

### Channel
`model.Channel` is the main conversation container. The channel type enum is central:
- `O` open/public
- `P` private
- `D` direct message
- `G` group message

Important fields include `TeamId`, `DisplayName`, `Name`, `Header`, `Purpose`, message counters, `CreatorId`, `SchemeId`, `Props`, `GroupConstrained`, `Shared`, `PolicyID`, banner info, and category-related fields. The presence of `Shared`, `PolicyID`, `PolicyEnforced`, and category/view metadata shows channels are not just chat streams; they also participate in federation/shared-channels, policy enforcement, and client information architecture.

### Post
`model.Post` is the message/event primitive. Key fields are `UserId`, `ChannelId`, `RootId`, `Message`, `Type`, `Props`, `FileIds`, and `Metadata`. Two things stand out:
1. It supports threaded messaging via `RootId`, `ReplyCount`, `LastReplyAt`, `Participants`, `IsFollowing`.
2. Many server-generated behaviors are encoded as post types (`system_join_channel`, `system_add_to_channel`, `system_ephemeral`, `reminder`, `burn_on_read`, etc.) and props (`from_webhook`, `from_bot`, `from_oauth_app`, `from_plugin`, attachments, urgency, expiration).

So posts are both user chat messages and a general timeline/event transport.

### Session / OAuth / Token
`model.Session` carries authenticated runtime state: `Token`, `UserId`, `DeviceId`, `Roles`, expiry/activity timestamps, OAuth flag, and `Props`. The props record platform/browser/OS, bot status, OAuth app id, mobile version, guest flag, and token type.

`model.OAuthApp` defines registered OAuth clients, including callback URLs, trust flag, dynamic registration, and token endpoint auth method. Public clients are supported and validated differently from confidential clients.

`model.Token` is for short-lived transactional tokens: password recovery, email verification, team/guest invitations, magic links, OAuth, SAML, and SSO code exchange.

## 4) REST API surface
`server/channels/api4/api.go` is the best entry point for the REST surface. It builds a large Gorilla Mux router tree rooted at `/api/v4` (and `/api/v5`). The `Routes` struct enumerates almost every major resource family:
- users, bots
- teams, team members, threads
- channels, memberships, bookmarks, categories, views
- posts, files, uploads
- plugins
- commands, incoming/outgoing hooks
- OAuth, SAML, LDAP
- compliance, cluster, jobs, system, license
- preferences, reactions, roles, schemes, emoji, groups
- cloud, imports/exports, remote cluster, shared channels
- permissions, usage, reports, limits
- custom profile attributes, audit logs, access-control policies
- agents, LLM services, properties

This is a very broad product API, but the implementation style is consistent: each feature file registers routes in `InitX()` and each handler delegates to app-layer logic.

`api4/handlers.go` defines important middleware wrappers:
- `APIHandler`: no session required
- `APISessionRequired`: session + MFA required
- `APISessionRequiredMfa`: session required but MFA completion waived
- `APIHandlerTrustRequester`: allows direct browser/websocket-style requests
- `CloudAPIKeyRequired`, `RemoteClusterTokenRequired`: specialized auth modes
- `APILocal`: local/unix-socket style unrestricted mode
- rate limiting and busy-shedding support

That wrapper system is a major architectural seam: authentication policy is declared at route registration time, not reimplemented in every handler.

## 5) Authentication and session model
Auth spans `web/`, `api4/`, and `app/`.

In `web/handlers.go`, every request passes through a common HTTP handler that sets security headers, request context, max payload size, request ID, and then parses auth via `app.ParseAuthTokenFromRequest`. Token precedence is explicit in `authentication.go`:
1. session cookie `MMAUTHTOKEN`
2. `Authorization: Bearer ...`
3. `Authorization: Token ...`
4. `access_token` query parameter
5. cloud header token
6. remote-cluster header token

`web/context.go` then applies session-required, MFA-required, cloud-key, or remote-cluster-token checks depending on handler configuration.

Login itself is split cleanly:
- `api4/user.go` exposes `/users/login`, `/login/sso/code-exchange`, `/login/desktop_token`, `/login/cws`, `/login/type`, `/logout`, session endpoints, and personal access token endpoints.
- `app/login.go` performs the real work.
- `app/authentication.go` handles password validation, login attempt limits, MFA, LDAP, and token parsing.

`AuthenticateUserForLogin` finds the user by id/login/email/username, falls back to LDAP lookups, optionally handles CWS one-time tokens, and then authenticates. `authentication.go` shows defensive details: password hashing migration, failed-attempt counters, separate locks for email vs LDAP login attempts, MFA checks, and restrictions on inactive users, bots, unverified accounts, and remote/synthetic users.

`DoLogin` is especially important. It:
- runs plugin `UserWillLogIn` hooks (plugins can reject login)
- builds a `Session` with `UserId`, roles, device id, auth flags, and CSRF token
- sets expiry based on web/mobile/SSO/device semantics
- records platform/OS/browser props from user-agent parsing
- marks guest status in session props
- persists the session and updates `LastLogin`
- returns the token in the response header
- triggers async `UserHasLoggedIn` hooks

Cookie attachment is also explicit: `AttachSessionCookies` sets `MMAUTHTOKEN`, `MMUSERID`, and `MMCSRF`, with secure/samesite adjustments and a cloud workspace cookie when applicable.

Logout removes cookies and revokes the backing session if present. Session enumeration/revocation endpoints sanitize tokens before returning them.

A subtle but important point from `app/session.go`: `GetSession` first tries the normal session store/cache, but can also synthesize sessions from personal access tokens (`createSessionForUserAccessToken`). That means PATs participate in the session pipeline without being identical to browser sessions.

## 6) Real-time / websocket architecture
Mattermost has a two-part websocket design.

### Upgrade + connection lifecycle
`api4/websocket.go` exposes `GET /api/v4/websocket`. It upgrades using Gorilla WebSocket with origin checks. The resulting `WebConnConfig` includes the authenticated session, connection id, optional sequence number for reconnect, posted-ack behavior, client origin, and client network metadata.

If a prior `connection_id` and `sequence_number` are supplied, `PlatformService.PopulateWebConnConfig` tries to recover prior active/dead queues for lossless reconnect. Otherwise a fresh connection id is minted.

### Hub + connection runtime
`platform/service.go` owns a `WebSocketRouter` plus multiple hubs. `platform/web_hub.go` shows the system scales websocket handling horizontally inside the process: the number of hubs equals CPU count, and users are hashed to a hub by user id. Hubs manage register/unregister, broadcast queues, direct messages, activity tracking, and connection checks.

`platform/web_conn.go` shows `WebConn` as the stateful per-connection object. It stores:
- the websocket socket
- session token/session pointer/expiry
- send queue and dead queue
- sequence number and reuse count for reconnect
- presence state (active team/channel/thread)
- origin client metadata
- plugin websocket hook channel

The dead queue is especially important: it acts like a user-space socket buffer so messages can be replayed after transient disconnects.

`model/websocket_message.go` defines a huge event catalog: posts, typing, channel lifecycle, team membership, preference changes, reactions, plugin status, config/license changes, drafts, acknowledgements, bookmarks, scheduled posts, custom profile attributes, views, properties, and more. `WebsocketBroadcast` lets the server target messages by user, team, channel, or connection and mark content as sanitized vs sensitive.

### Websocket action handlers
Client-to-server websocket actions are handled in `server/channels/wsapi/`. `wsapi/api.go` initializes user/system/status handlers. `wsapi/websocket_handler.go` reloads the session from the connection token, dispatches the action handler, and returns websocket responses/errors via the hub. `wsapi/user.go` includes actions like `user_typing` and `user_update_active_status`; `wsapi/system.go` includes `ping` and notification acknowledgement.

So the split is: **API4 upgrades the socket, platform manages connection reliability/broadcasting, and WSAPI handles client commands over that connection.**

## 7) Plugin framework
Mattermost’s plugin system is substantial, not superficial.

`server/public/plugin/api.go` defines a large server API exposed to plugins: config access, command registration, user/team/channel operations, preference APIs, session APIs, tokens, etc. The intent is that plugins can act through supported RPCs instead of directly patching internals.

`server/public/plugin/hooks.go` defines the stable hook protocol. Hooks span activation/deactivation, HTTP serving under `/plugins/{id}`, slash commands, post pre/post hooks, membership hooks, login hooks, websocket connect/disconnect, plugin cluster events, SAML login, notifications, file download/upload interception, and more. The numeric hook IDs indicate a wire-compatible RPC contract.

`server/public/plugin/client.go` is what plugin authors embed (`MattermostPlugin`) and how plugin processes call `plugin.Serve(...)` via HashiCorp go-plugin. On the server side, `environment.go` scans plugin directories, tracks active/registered plugins, and exposes statuses/public files. `supervisor.go` launches the plugin executable chosen from the manifest, verifies it with a checksum-based secure config, dispenses the `hooks` RPC implementation, tracks which hooks are implemented, and performs health checks/ping.

At the REST layer, `api4/plugin.go` exposes plugin lifecycle endpoints: upload/install, install-from-URL, marketplace install, status listing, enable/disable, removal, and webapp plugin bundle discovery. These are guarded both by server plugin settings and sysconsole plugin permissions.

## 8) Practical mental model
If you need to understand or change Mattermost server behavior, usually start with this path:
1. **`public/model`** for the data contract.
2. **`api4` or `wsapi`** for externally visible endpoints/actions.
3. **`app`** for the business rule and orchestration.
4. **`store`/`platform`** for persistence, caching, sessions, cluster, and real-time runtime.
5. **`public/plugin`** if the behavior may be intercepted or extended by plugins.

The core domain centers on **users interacting in channels within teams via posts**, but the real architecture is defined by **sessions, permissions, policies, plugins, and websocket event flow**. That is what makes Mattermost feel like more than a CRUD chat app: nearly every core operation is policy-aware, extension-aware, realtime-aware, and often cluster-aware.
