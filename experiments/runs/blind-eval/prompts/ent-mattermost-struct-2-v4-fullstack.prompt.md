# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-mattermost-struct-2

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.


--- ARCHITECTURAL CONTEXT (LLM-generated, one-time) ---
(See deep context below for mattermost architecture)
--- END ARCHITECTURAL CONTEXT ---

--- DEEP DOMAIN CONTEXT (LLM-generated from key files, one-time) ---
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

--- END DEEP DOMAIN CONTEXT ---

--- CLUE FILE START ---
=CC v2.1 mattermost@HEAD 1346mod 19215sym
? How do the README and API docs describe Mattermost's integration and API-documentation surface?


-- README
[Mattermost](https://mattermost.com) is an open core, self-hosted collaboration platform that offers chat, workflow a... [Deploy Mattermost on-premises](https://mattermost.com/deploy/?utm_source=github-mattermost-server-readme), or [try i...

-- TREE
api/  (2 files)
  server/
e2e-tests/  (1 files)
  cypress/
server/  (1309 files)
  build/  config/  einterfaces/  enterprise/  fips/
tools/  (37 files)
  mattermost-govet/  mmgotool/  sharedchannel-test/
webapp/  (1 files)
README.md

-- INDEX
server/public/plugin/client_rpc_generated.go   8077L  Z_AddChannelMemberArgs, Z_AddChannelMemberReturns, Z_AddReactionArgs, Z_AddReactionReturns, Z_AddUserToChannelArgs
server/channels/app/config.go                   283L  AddConfigListener, AddLicenseListener, AsymmetricSigningKey, ClientConfig, ClientConfigHash
server/public/model/client4.go                 8269L  BuildResponse, AcknowledgePost, AddChannelMember, AddChannelMemberWithRootId, AddChannelMembers
server/channels/app/platform/config.go          418L  AddConfigListener, AsymmetricSigningKey, CleanUpConfig, ClientConfig, ClientConfigHash
server/channels/store/retrylayer/retrylayer.go 18248L  New, AccessControlPolicy, Attributes, Audit, AutoTranslation
server/channels/api4/handlers.go                256L  APIHandler, APIHandlerTrustRequester, APILocal, APISessionRequired, APISessionRequiredDisableWhenBusy
server/channels/app/authorization.go            675L  HasPermissionTo, HasPermissionToChannel, HasPermissionToChannelByPost, HasPermissionToChannelMemberCount, HasPermissionToEditPropertyField
server/channels/app/audit.go                    235L  AddAuditLogCertificate, GetAudits, GetAuditsPage, LogAuditRec, LogAuditRecWithLevel
server/channels/app/properties/property_group.go    53L  GetPropertyGroup, Group, RegisterBuiltinGroups, RegisterPropertyGroup
server/channels/web/handlers.go                 578L  GetHandlerName, GetOriginClient, ServeHTTP, basicSecurityChecks, checkCSRFToken
server/channels/app/user.go                    3208L  ActivateMfa, AddUserToTeamByInviteIfNeeded, AdjustImage, AuthenticateUserForGuestMagicLink, AutocompleteUsersInChannel
  ...and 1335 more modules

-- SYM
isRepeatableError                   M server/channels/store/retrylayer/retrylayer.go:595    function isRepeatableError
App.Srv                             M server/channels/app/app.go:62     function App.Srv
SqlStore.GetReplica                 M server/channels/store/sqlstore/store.go:462    function SqlStore.GetReplica
TimerLayerAccessControlPolicyStore.Get M server/channels/store/timerlayer/timerlayer.go:610    function TimerLayerAccessControlPolicyStore.Get
StoreTestWrapper.GetMaster          M server/channels/store/sqlstore/sqlx_wrapper.go:33     function StoreTestWrapper.GetMaster
SqlStore.GetMaster                  M server/channels/store/sqlstore/store.go:428    function SqlStore.GetMaster
SqlStore.getQueryBuilder            M server/channels/store/sqlstore/store.go:937    function SqlStore.getQueryBuilder
closeBody                           M server/public/model/client4.go:110    function closeBody
SqlStore.getQueryPlaceholder        M server/channels/store/sqlstore/store.go:941    function SqlStore.getQueryPlaceholder
RetryLayerAccessControlPolicyStore.Get M server/channels/store/retrylayer/retrylayer.go:627    function RetryLayerAccessControlPolicyStore.Get
BuildResponse                       M server/public/model/client4.go:135    function BuildResponse
adminCCLogger.Errorf                M server/public/pluginapi/experimental/bot/logger/admincclogger/admincc_logger.go:57     function adminCCLogger.Errorf
defaultLogger.Errorf                M server/public/pluginapi/experimental/bot/logger/default_logger.go:65     function defaultLogger.Errorf
nilLogger.Errorf                    M server/public/pluginapi/experimental/bot/logger/nil_logger.go:15     function nilLogger.Errorf
MockLogger.Errorf                   M server/public/pluginapi/experimental/bot/mocks/mock_logger.go:69     Errorf mocks base method.
MockLoggerMockRecorder.Errorf       M server/public/pluginapi/experimental/bot/mocks/mock_logger.go:79     Errorf indicates an expected call of Errorf.
hooksTimerLayer.recordTime          M server/public/plugin/hooks_timer_layer_generated.go:24     function hooksTimerLayer.recordTime
adminCCLogger.logToAdmins           M server/public/pluginapi/experimental/bot/logger/admincclogger/admincc_logger.go:81     function adminCCLogger.logToAdmins
WebSocketEvent.Copy                 M server/public/model/websocket_message.go:296    function WebSocketEvent.Copy
PostMetadata.Copy                   M server/public/model/post_metadata.go:91     Copy does a deep copy
Client4.doAPIRequestReader          M server/public/model/client4.go:908    doAPIRequestReader makes an HTTP request using ...
Server.Config                       M server/channels/app/config.go:27     function Server.Config
Mutex.Lock                          M server/public/pluginapi/cluster/mutex.go:108    Lock locks m.
apiTimerLayer.recordTime            M server/public/plugin/api_timer_layer_generated.go:24     function apiTimerLayer.recordTime
apiTimerLayer.recordTime            M server/public/plugin/interface_generator/main.go:418    function apiTimerLayer.recordTime
hooksTimerLayer.recordTime          M server/public/plugin/interface_generator/main.go:460    function hooksTimerLayer.recordTime
SqlStore.hasLicense                 M server/channels/store/sqlstore/store.go:966    function SqlStore.hasLicense
Mutex.LockWithContext               M server/public/pluginapi/cluster/mutex.go:117    LockWithContext locks m unless the context is c...
Client4.doAPIRequest                M server/public/model/client4.go:797    function Client4.doAPIRequest
BulkIndexerDebugLogger.Printf       M server/enterprise/elasticsearch/common/logger.go:86     function BulkIndexerDebugLogger.Printf
Client4.DoAPIGet                    M server/public/model/client4.go:721    Returns the HTTP response or any error that occ...
Context.SetInvalidURLParam          M server/channels/web/context.go:198    function Context.SetInvalidURLParam
pluginAPIConfigServiceAdapter.Config M server/public/shared/httpservice/httpservice.go:59     function pluginAPIConfigServiceAdapter.Config
App.Config                          M server/channels/app/config.go:31     function App.Config
PlatformService.Config              M server/channels/app/platform/config.go:40     function PlatformService.Config
JobServer.Config                    M server/channels/jobs/server.go:60     function JobServer.Config
testHelper.Config                   M server/cmd/mattermost/commands/cmdtestlib.go:82     Config returns the configuration passed to a ru...
ServerIface.Config                  M server/platform/services/telemetry/mocks/ServerIface.go:24     Config provides a mock function with no fields
NewInvalidURLParamError             M server/channels/web/context.go:251    function NewInvalidURLParamError
Mutex.Unlock                        M server/public/pluginapi/cluster/mutex.go:171    Unlock unlocks m.
Client4.doAPIRequestBytes           M server/public/model/client4.go:801    function Client4.doAPIRequestBytes
checkParentChildIntegrity           M server/channels/store/sqlstore/integrity.go:64     function checkParentChildIntegrity
Client4.usersRoute                  M server/public/model/client4.go:195    function Client4.usersRoute
Client4.doAPIGet                    M server/public/model/client4.go:805    function Client4.doAPIGet
getOrphanedRecords                  M server/channels/store/sqlstore/integrity.go:23     function getOrphanedRecords
LRU.removeElement                   M server/platform/services/cache/lru.go:230    function LRU.removeElement
SqlStore.DBXFromContext             M server/channels/store/sqlstore/context.go:32     DBXFromContext is a helper utility that returns...
Client4.doAPIPostJSON               M server/public/model/client4.go:857    function Client4.doAPIPostJSON
Client4.DoAPIPostJSON               M server/public/model/client4.go:733    DoAPIPostJSON marshals the provided data to JSO...
TimerLayerAccessControlPolicyStore.Save M server/channels/store/timerlayer/timerlayer.go:642    function TimerLayerAccessControlPolicyStore.Save
TestHelper.CreatePost               M server/channels/api4/apitestlib.go:849    function TestHelper.CreatePost
LRU.Remove                          M server/platform/services/cache/lru.go:88     Remove deletes the value for a key.
  ...and 18915 more symbols

-- FOCUS
server/build/docker-compose.yml (server/build/docker-compose.yml:1-73)
  Config summary for server/build/docker-compose.yml: entries: extends: docker-compose.common.yml, postgres, extends: docker-compose.common.yml, minio, extends: docker-compose.common.yml, inbucket, extends: docker-compose.common.yml, openldap, extends: docker-compose.common.yml, elasticsearch, extends: docker-compose.common.yml, opensearch; services: postgres, extends, minio, extends, inbucket, extends
  entries: extends: docker-compose.common.yml, postgres, extends: docker-compose.common.yml, minio, extends: docker-compose.common.yml, inbucket, extends: docker-compose.common.yml, openldap, extends: docker-compose.common.yml, elasticsearch
  services: postgres, extends, minio, extends, inbucket

api/package.json (api/package.json:1-33)
  Config summary for api/package.json: deps: @redocly/cli, swagger-cli, sync-fetch, yaml
  deps: @redocly/cli, swagger-cli, sync-fetch, yaml

e2e-tests/cypress/package.json (e2e-tests/cypress/package.json:1-110)
  Config summary for e2e-tests/cypress/package.json: deps: @aws-sdk/client-s3, @aws-sdk/lib-storage, @babel/eslint-parser, @babel/eslint-plugin, @cypress/request, @cypress/webpack-preprocessor, @eslint/js, @mattermost/client
  deps: @aws-sdk/client-s3, @aws-sdk/lib-storage, @babel/eslint-parser, @babel/eslint-plugin, @cypress/request, @cypress/webpack-preprocessor

README.md (README.md:1-97)
  Documentation summary for README.md: [Mattermost](https://mattermost.com) is an open core, self-hosted collaboration platform that offers chat, workflow a... [Deploy Mattermost on-premises](https://mattermost.com/deploy/?utm_source=github-mattermost-server-readme), or [try i...; sections: [![Mattermost logo](https://user-images.githubusercontent.com/7205829/137170381-fe86eef0-bccc-4fdd-8e92-b258884ebdd7.png)](https://mattermost.com), Install Mattermost, Native mobile and desktop apps, Get security bulletins, Get involved
  sections: [![Mattermost logo](https://user-images.githubusercontent.com/7205829/137170381-fe86eef0-bccc-4fdd-8e92-b258884ebdd7.png)](https://mattermost.com), Install Mattermost, Native mobile and desktop apps, Get security bulletins, Get involved

apiRPCServer (server/public/plugin/client_rpc.go:152-152)
  apiRPCServer is the server-side RPC handler that runs in the Mattermost server process and receives requests from [apiRP
  methods: InstallPlugin, LoadPluginConfiguration, LogAuditRec, LogAuditRecWithLevel, LogDebug, LogError

apiHandlers (tools/mattermost-govet/facts/apiHandlers.go:29-29)
  sig: apiHandlers(pass *analysis.Pass)
  behavior: GUARD(pass.Pkg.Path() != util.API4PkgPath -> return nil, nil)
  calls: Path, isApiHandler

MattermostPlugin.SetAPI (server/public/plugin/client.go:99-99)
  SetAPI persists the given API interface to the plugin.
  sig: MattermostPlugin.SetAPI(api API)
  called_by: ClientMain

IsApiHandler (tools/mattermost-govet/facts/apiHandlers.go:16-16)
  type IsApiHandler

API.InitAction (server/channels/api4/integration_action.go:15-15)
  calls: APIHandler, APISessionRequired
  called_by: Init

isApiHandler (tools/mattermost-govet/facts/apiHandlers.go:49-49)
  sig: isApiHandler(funDecl *ast.FuncDecl)
  behavior: GUARD(len(funcType.Params.List) < 3 -> return false); PRECEDENCE(len -> not_ok)
  called_by: apiHandlers

PluginAPI.KVGet (server/channels/app/plugin_api.go:1092-1092)
  sig: PluginAPI.KVGet(key string)
  behavior: DELEGATE(api.app.GetPluginKey -> result)
  calls: GetPluginKey
  called_by: MessageWillBePosted, Get, ShouldProcessMessage

API.APILocal (server/channels/api4/handlers.go:203-203)
  APILocal provides a handler for API endpoints to be used in local mode, this is, through a UNIX socket and without an au
  sig: API.APILocal(h handlerFunc, opts ...APIHandlerOption)
  behavior: GUARD(*api.srv.Config().ServiceSettings.WebserverMo... -> return gzhttp.Gzip...)
  calls: setHandlerOpts, Config
  called_by: InitAccessControlPolicyLocal, InitBotLocal, InitChannelLocal, InitCommandLocal, InitConfigLocal, InitCustomProfileAttributesLocal, InitExportLocal, InitGroupLocal

API.APISessionRequired (server/channels/api4/handlers.go:50-50)
  APISessionRequired provides a handler for API endpoints which require the user to be logged in in order for access to be
  sig: API.APISessionRequired(h handlerFunc, opts ...APIHandlerOption)
  behavior: GUARD(*api.srv.Config().ServiceSettings.WebserverMo... -> return gzhttp.Gzip...)
  calls: setHandlerOpts, Config
  called_by: InitAccessControlPolicy, InitAgents, InitAIBridgeTestHelper, InitAuditLogging, InitBot, InitBrand, InitChannel, InitChannelBookmarks

PluginAPI.GetUser (server/channels/app/plugin_api.go:285-285)
  sig: PluginAPI.GetUser(userID string)
  behavior: DELEGATE(api.app.GetUser -> result)
  calls: GetUser
  called_by: InitLogin, SetUserRemoteID, assignBot, createBot, convertGroupMessageToChannel, deleteChannel, getDirectOrGroupMessageMembersCommonTeams, moveChannel

PluginAPI.GetTeam (server/channels/app/plugin_api.go:184-184)
  sig: PluginAPI.GetTeam(teamID string)
  behavior: DELEGATE(api.app.GetTeam -> result)
  calls: GetTeam
  called_by: moveChannel, localMoveChannel, moveCommand, getGroups, getPostInfo, remoteClusterAcceptInvite, addTeamMember, addTeamMembers

PluginAPI.GetChannel (server/channels/app/plugin_api.go:493-493)
  sig: PluginAPI.GetChannel(channelID string)
  behavior: DELEGATE(api.app.GetChannel -> result)
  calls: GetChannel
  called_by: PatchChannelModerationsForMembers, addChannelMember, deleteChannel, getChannel, getChannelModerations, getPinnedPosts, moveChannel, patchChannel

PluginAPI.GetOAuthApp (server/channels/app/plugin_api.go:1370-1370)
  sig: PluginAPI.GetOAuthApp(appID string)
  behavior: DELEGATE(api.app.GetOAuthApp -> result)
  calls: GetOAuthApp
  called_by: deleteOAuthApp, getOAuthApp, getOAuthAppInfo, regenerateOAuthAppSecret, updateOAuthApp, GetOAuthAccessTokenForImplicitFlow, UpdateOAuthApp, authorizeOAuthPage

PluginAPI.GetTeamByName (server/channels/app/plugin_api.go:193-193)
  sig: PluginAPI.GetTeamByName(name string)
  behavior: DELEGATE(api.app.GetTeamByName -> result)
  calls: GetTeamByName
  called_by: getTeamByName, teamExists, RenameTeam, getCommandFromTeamTrigger, getTeamFromArg, getTeamFromTeamArg, listUsersCmdF, GetByName

PluginAPI.RevokeSession (server/channels/app/plugin_api.go:352-352)
  sig: PluginAPI.RevokeSession(sessionID string)
  behavior: DELEGATE(api.app.RevokeSessionById -> result)
  calls: RevokeSessionById
  called_by: revokeSession, RevokeSessionsForDeviceId, MessageWillBePosted, DisableUserAccessToken, RevokeSessionById, RevokeUserAccessToken, limitNumberOfSessions, Revoke

PluginAPI.GetChannelMembersForUser (server/channels/app/plugin_api.go:651-651)
  sig: PluginAPI.GetChannelMembersForUser(_, userID string, page, perPage int)
  behavior: DELEGATE(api.app.GetChannelMembersForUserWithPagination -> result)
  calls: GetChannelMembersForUserWithPagination
  called_by: getChannelMembersForTeamForUser, removeUserFromChannel, MessageWillBePosted, DemoteUserToGuest, PromoteGuestToUser, ListMembersForUser

PluginAPI.CreateUser (server/channels/app/plugin_api.go:264-264)
  sig: PluginAPI.CreateUser(user *model.User)
  behavior: DELEGATE(api.app.CreateUser -> result)
  calls: CreateUser
  called_by: CreateUserWithAuth, InitLogin, CreateOAuthUser, CreateUserAsAdmin, CreateUserFromSignup, CreateUserWithInviteId, CreateUserWithToken, Fuzz

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 83 symbols in L3, 75 with behavior annotations
uncovered: PluginAPI.GetGroup, PluginAPI.GetGroupByName, PluginAPI.GetGroupByRemoteID, PluginAPI.GetGroupChannel

--- CLUE FILE END ---

QUESTION: How do the README and API docs describe Mattermost's integration and API-documentation surface?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
