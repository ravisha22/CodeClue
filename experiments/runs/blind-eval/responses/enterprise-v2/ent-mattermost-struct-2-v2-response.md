# Enterprise v2: ent-mattermost-struct-2
Date: 2026-04-17

## Reasoning Scaffold

### 1. Relevant Clue Entries

The question asks how the README and API docs describe Mattermost's integration and API-documentation surface.

**README** (README.md:1-97): Describes Mattermost as "an open core, self-hosted collaboration platform that offers chat, workflow a…". FOCUS for README.md lists sections: "Install Mattermost", "Native mobile and desktop apps", "Get security bulletins", "Get involved".

**FOCUS – api/package.json** (api/package.json:1-33): Dependencies are `@redocly/cli`, `swagger-cli`, `sync-fetch`, `yaml`. This is the dedicated API documentation toolchain.

**TREE**: The `api/` directory contains 2 files with a `server/` subdirectory, confirming a separate top-level directory for API specification artifacts.

**INDEX – server/channels/api4/handlers.go** (256L): Exports `APIHandler`, `APIHandlerTrustRequester`, `APILocal`, `APISessionRequired`, `APISessionRequiredDisableWhenBusy` — the HTTP handler factory functions for the API layer.

**FOCUS – apiRPCServer** (server/public/plugin/client_rpc.go:152): Described as "the server-side RPC handler that runs in the Mattermost server process and receives requests from [apiRPC…]". Methods include `InstallPlugin`, `LoadPluginConfiguration`, `LogAuditRec`, `LogAuditRecWithLevel`, `LogDebug`, `LogError`.

**FOCUS – MattermostPlugin.SetAPI** (server/public/plugin/client.go:99): "SetAPI persists the given API interface to the plugin." Called by `ClientMain`.

**FOCUS – API.APILocal** (server/channels/api4/handlers.go:203): "provides a handler for API endpoints to be used in local mode, this is, through a UNIX socket and without an au…". Behavior: `GUARD(*api.srv.Config().ServiceSettings.WebserverMo... -> return gzhttp.Gzip...)`.

**FOCUS – API.APISessionRequired** (server/channels/api4/handlers.go:50): "provides a handler for API endpoints which require the user to be logged in in order for access to be…". Called by: `InitAccessControlPolicy`, `InitAgents`, `InitAIBridgeTestHelper`, `InitAuditLogging`, `InitBot`, `InitBrand`, `InitChannel`, `InitChannelBookmarks`.

**FOCUS – PluginAPI methods**: Multiple DELEGATE-pattern symbols:
- `PluginAPI.KVGet` (server/channels/app/plugin_api.go:1092) → delegates to `api.app.GetPluginKey`
- `PluginAPI.GetUser` (server/channels/app/plugin_api.go:285) → delegates to `api.app.GetUser`
- `PluginAPI.GetTeam` (server/channels/app/plugin_api.go:184) → delegates to `api.app.GetTeam`
- `PluginAPI.GetChannel` (server/channels/app/plugin_api.go:493) → delegates to `api.app.GetChannel`
- `PluginAPI.GetOAuthApp` (server/channels/app/plugin_api.go:1370) → delegates to `api.app.GetOAuthApp`
- `PluginAPI.RevokeSession` (server/channels/app/plugin_api.go:352) → delegates to `api.app.RevokeSessionById`
- `PluginAPI.CreateUser` (server/channels/app/plugin_api.go:264) → delegates to `api.app.CreateUser`

**SYM – Client4**: `Client4.doAPIRequest` (client4.go:797), `Client4.DoAPIGet` (client4.go:721), `Client4.DoAPIPostJSON` (client4.go:733), `Client4.doAPIRequestReader` (client4.go:908) — the Go HTTP client for consuming the REST API.

**INDEX – client_rpc_generated.go** (8077L): Auto-generated RPC argument/return types (`Z_AddChannelMemberArgs`, `Z_AddReactionArgs`, etc.) confirming a code-generated plugin RPC surface.

### 2. Tracing Through the Clue

**API Documentation Toolchain**: The `api/` directory (TREE) is a standalone top-level directory dedicated to API documentation. Its `package.json` (FOCUS api/package.json) pulls in:
- `@redocly/cli` — an OpenAPI documentation rendering and linting tool
- `swagger-cli` — Swagger/OpenAPI validation tooling
- `sync-fetch` and `yaml` — supporting libraries for fetching and parsing YAML specs

This confirms that Mattermost maintains an **OpenAPI/Swagger specification** for its REST API, with tooling to validate and render it.

**REST API Layer (api4)**: The `server/channels/api4/handlers.go` (INDEX) provides handler factories:
- `APISessionRequired` (handlers.go:50) — requires authenticated sessions; its `called_by` list (`InitAccessControlPolicy`, `InitAgents`, `InitBot`, `InitBrand`, `InitChannel`, etc.) shows it gates a wide range of resource endpoints.
- `APILocal` (handlers.go:203) — provides UNIX-socket-based local-only access without authentication, gated by `ServiceSettings.WebserverMode` config.
- `APIHandler` — a general handler (INDEX).
- `APIHandlerTrustRequester` — a handler that trusts the requester (INDEX).

**Plugin Integration Surface**: Plugins integrate via two mechanisms:
1. **PluginAPI** (server/channels/app/plugin_api.go) — a facade that uses the DELEGATE pattern to proxy calls into the core `App` layer. Each method (GetUser, GetTeam, GetChannel, CreateUser, KVGet, RevokeSession, GetOAuthApp, etc.) delegates to `api.app.*`, providing plugins with a controlled gateway to server functionality.
2. **RPC layer** — `apiRPCServer` (server/public/plugin/client_rpc.go:152) runs in the server process and receives RPC calls from plugin clients. `client_rpc_generated.go` (8077L, INDEX) contains auto-generated argument/return structs for the entire plugin API surface.
3. **MattermostPlugin.SetAPI** (server/public/plugin/client.go:99) persists the API interface to the plugin, called by `ClientMain` during plugin initialization.

**Client SDK**: `Client4` (server/public/model/client4.go, 8269L) is a comprehensive Go HTTP client. Methods like `DoAPIGet`, `DoAPIPostJSON`, `doAPIRequest`, and `doAPIRequestReader` (SYM) provide typed access to the REST API. `BuildResponse` (client4.go:135) and `closeBody` (client4.go:110) handle HTTP response lifecycle.

**OAuth**: `PluginAPI.GetOAuthApp` (plugin_api.go:1370) delegates to `api.app.GetOAuthApp`, and its callers include `authorizeOAuthPage`, `getOAuthApp`, `getOAuthAppInfo`, `regenerateOAuthAppSecret`, and `GetOAuthAccessTokenForImplicitFlow` — confirming an OAuth provider surface.

### 3. GAPS — What Cannot Be Determined

The GAPS section states:
- **Type**: STRUCTURAL (answerable from L0-L2)
- **Coverage**: 83 symbols in L3, 75 with behavior annotations
- **Uncovered**: `PluginAPI.GetGroup`, `PluginAPI.GetGroupByName`, `PluginAPI.GetGroupByRemoteID`, `PluginAPI.GetGroupChannel`

From the clue alone, we **cannot determine**:
- The exact OpenAPI specification version (e.g., 3.0 vs 3.1)
- The full list of REST API endpoints and their URL paths
- Whether a GraphQL or gRPC API exists alongside REST
- The contents of the `api/server/` subdirectory
- How the Redocly-rendered documentation is published or hosted
- The full scope of the Group-related plugin API surface (uncovered symbols)

### 4. Synthesis

Mattermost's integration and API-documentation surface has **four distinct layers** visible in the clue:

1. **OpenAPI/Swagger Specification** (`api/` directory, TREE): A dedicated top-level directory with tooling (`@redocly/cli`, `swagger-cli` in api/package.json) for validating and rendering an OpenAPI specification. This is the formal API documentation surface.

2. **REST API Handler Layer** (`server/channels/api4/handlers.go`, INDEX/FOCUS): Handler factories (`APISessionRequired`, `APILocal`, `APIHandler`, `APIHandlerTrustRequester`) create HTTP handlers with different authentication requirements. `APISessionRequired` gates most endpoints (called by `InitChannel`, `InitBot`, `InitAccessControlPolicy`, etc.), while `APILocal` serves UNIX-socket-only local administration without authentication.

3. **Plugin Integration API** (`server/channels/app/plugin_api.go`, `server/public/plugin/`): A comprehensive PluginAPI facade using the DELEGATE pattern to proxy calls to the core App layer. The RPC transport (`apiRPCServer` at client_rpc.go:152, auto-generated types in client_rpc_generated.go at 8077L) enables out-of-process plugin communication. Plugin initialization flows through `MattermostPlugin.SetAPI` (client.go:99) called by `ClientMain`.

4. **Go Client SDK** (`server/public/model/client4.go`, 8269L): A typed HTTP client (`Client4`) with methods for all API operations, using `DoAPIGet`, `DoAPIPostJSON`, and response handling via `BuildResponse`/`closeBody`.

Additionally, **OAuth** support is evidenced by `PluginAPI.GetOAuthApp` (plugin_api.go:1370) and its callers including `authorizeOAuthPage` and `GetOAuthAccessTokenForImplicitFlow`.
