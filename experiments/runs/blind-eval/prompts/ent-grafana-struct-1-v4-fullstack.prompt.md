# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-grafana-struct-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.


--- ARCHITECTURAL CONTEXT (LLM-generated, one-time) ---
(See deep context below for grafana architecture)
--- END ARCHITECTURAL CONTEXT ---

--- DEEP DOMAIN CONTEXT (LLM-generated from key files, one-time) ---
# Grafana Deep Context

-- DOMAIN MODEL
Grafana’s backend is organized around a few long-lived resource types that the rest of the system composes rather than replaces. The most central object is the dashboard model in `pkg/services/dashboards/models.go`. A `Dashboard` carries an integer database ID, a globally stable `UID`, organization ownership, folder placement, version, plugin provenance, and the raw JSON document that the frontend ultimately renders. The important nuance is that Grafana supports two storage idioms at once: the classic JSON dashboard document and a Kubernetes-style resource wrapper with `apiVersion`, metadata, and `spec`. `NewDashboardFromJson` branches on `apiVersion`, so the same save/load path can accept either legacy payloads or newer unified-storage resources. That duality explains a lot of otherwise odd compatibility code in the API layer, such as backfilling `id` and `version` into JSON for old clients even when the source of truth is a newer object representation.

Folders are not a separate conceptual layer in the UI alone; they are part of the dashboard resource graph. `FolderUID`, `FolderID`, and folder lookups in `pkg/api/dashboard.go` show that permissions, URLs, and routing all depend on whether a dashboard is root-scoped or folder-scoped. Dashboard metadata is also not just decoration: flags like `HasACL`, `IsFolder`, `Provisioned`, and annotation permissions determine whether the frontend treats a dashboard as editable content, provisioned config, or a permissions-managed object.

Data sources are the second major domain pillar. `pkg/services/datasources/models.go` defines a `DataSource` as an org-scoped connection profile with a stable `UID`, human name, plugin `Type`, access mode (`direct` vs `proxy`), URL/database/user credentials, arbitrary plugin-specific `JsonData`, encrypted `SecureJsonData`, and lifecycle flags like `ReadOnly` and `IsPrunable`. This is not just a connection string store. The model explicitly supports custom HTTP headers, secure SOCKS proxy configuration, plugin aliases, and access-control scopes keyed by datasource UID or name. In practice that means Grafana treats a datasource as a policy-bearing integration point rather than a dumb adapter.

Plugins sit behind the datasource model and expand the domain further. The README calls out panel plugins and mixed data sources, and the backend reflects that by resolving datasource `Type` through the plugin store in `pkg/api/datasources.go`. The displayed type, logo, and even canonical plugin ID may differ from the stored alias. That design lets Grafana evolve plugin packaging and branded integrations without breaking existing datasource rows. It also explains why datasource CRUD is tightly coupled to plugin lookup and access-control cache invalidation.

Unified alerting is its own subsystem rather than a thin dashboard add-on. The `pkg/services/ngalert` tree models alert rules, contact points, routing policies, mute timings, silences, notification settings, and provisioning. The API entrypoint in `pkg/services/ngalert/api/api.go` wires together rule storage, Alertmanager-compatible notification delivery, Prometheus-compatible status/queries, and Cortex Ruler-compatible rule management. In other words, alerting in Grafana is modeled as a federated control plane over several alerting backends, with Grafana adding authorization, provenance, and UI-facing composition on top.

-- API SURFACE
The main backend API surface is defined by `pkg/api/api.go`, whose top-level comment is blunt: the same HTTP API is used by the frontend “to do everything from saving dashboards, creating users and updating data sources.” That is a useful framing. Grafana is not a separate backend-for-frontend plus public API product; the browser is effectively the primary API client, and public automation rides the same surface. The route registry exposes both page routes and `/api` operations, but the semantics are shared.

Dashboard APIs illustrate Grafana’s compatibility-first posture. `pkg/api/dashboard.go` exposes deprecated-but-still-supported `/dashboards/uid/{uid}` behavior while nudging callers toward the newer Kubernetes-style dashboard API. The response is richer than raw JSON: Grafana computes folder metadata, creator/updater identities, per-dashboard edit/delete/admin permissions, annotation capabilities, provisioning state, and public-dashboard flags before returning the document. That tells you the API surface is intentionally opinionated and UI-ready, not merely a persistence CRUD layer.

Datasource APIs are similarly high-level. `pkg/api/datasources.go` supports list/get/create/update/delete by both numeric ID and UID, but the real behavior includes permission filtering, plugin metadata enrichment, read-only protections, live subsystem notifications on delete, and resolver-cache invalidation so RBAC scope lookups stay correct after renames. The request/response DTOs in `pkg/services/datasources/models.go` also reveal that secure settings updates are first-class and handled atomically with datasource mutation.

Alerting’s API surface is broader than a single REST controller. `pkg/services/ngalert/api/api.go` composes multiple endpoint families: Alertmanager-compatible APIs for silences/receivers/routing, Prometheus-compatible APIs for rule status and alert instances, Ruler-compatible APIs for rule CRUD, testing endpoints for evaluation/backtesting, configuration endpoints, provisioning endpoints, history endpoints, and conversion helpers for Prometheus rule migration. The important takeaway is that Grafana presents a unified alerting API while internally brokering among distinct backends and persistence paths.

Authentication and user/session APIs also participate in the same surface. `pkg/api/login.go` handles form login, auto-login redirects for OAuth/SAML, login ping, password reset starts, and invite flows; `pkg/services/auth/auth.go` and `pkg/services/auth/authimpl/*` provide token lifecycle operations underneath. Even “HTML” routes like `/login` are really part of the backend auth API because they are bound to token creation, redirect validation, and session rotation policy.

-- ROUTING
Grafana’s routing model is unusually revealing because `registerRoutes` in `pkg/api/api.go` is effectively a map of product areas. A large number of URLs are SPA entry routes guarded by middleware rather than server-rendered feature implementations. `/d/:uid` and `/dashboards/*` enter the dashboard experience, `/datasources/*` and `/connections/*` enter integration management, `/alerting/*` and `/monitoring/*` enter alerting/incident workflows, `/explore` and `/drilldown` cover investigation, and `/a/:id/*` mounts app plugins behind plugin-specific access control.

This means routing is domain-based, not controller-based. The backend mostly decides whether the caller may enter a product surface and then hands the browser enough bootstrapped context to continue. That is especially visible for dashboards: legacy `/dashboard/*` routes, current `/d/:uid` routes, solo routes, public dashboard routes, import routes, and provisioning routes all coexist because Grafana preserves user bookmarks, embedding URLs, snapshots, and newer canonical routes simultaneously.

Datasource routing also shows Grafana’s ongoing product evolution. Both `/datasources/*` and `/connections/datasources/*` are registered, implying that the backend is carrying route aliases while the product moves toward a broader “connections” framing. Plugin routes like `/connections/datasources/:id/page/:page` further show that plugin UIs can contribute subpages under managed routing without owning top-level auth logic themselves.

Alerting routes are intentionally broad. The page routes (`/alerting/*`, `/monitoring/*`, `/alerts-and-incidents/*`) are coarse SPA mounts, while fine-grained backend authorization for the underlying APIs is delegated to `pkg/services/ngalert/accesscontrol/routes.go` and rule-specific services. In other words, page routing is permissive enough to let the UI boot, while real object authorization happens closer to the alerting API handlers and resource scopes.

-- AUTH
Grafana auth is layered rather than centralized in one package. At the route level, `pkg/api/api.go` attaches middleware such as `ReqSignedIn`, `ReqSignedInNoAnonymous`, Grafana-admin checks, org-admin checks, plugin auth, and access-control evaluators. At the interaction layer, `pkg/api/login.go` implements login page rendering, redirect sanitization, auto-login selection, and cookie policy. At the token layer, `pkg/services/auth/auth.go` defines the `UserTokenService` contract for creating, looking up, rotating, revoking, and enumerating user tokens plus associated external sessions.

The redirect rules in `pkg/api/login.go` are worth calling out because they show Grafana’s threat model. Redirects must be relative, may not contain `//` or `..`, and must respect `AppSubURL`. That prevents open redirects and path traversal-style escape hatches during login. Cookie options are also derived from config for secure, same-site-aware session behavior.

Login itself is handled via `hs.authnService.Login(...)` in `LoginPost`, not by ad hoc password checks in the API layer. That abstraction allows multiple auth modules—form auth, OAuth providers, SAML, auth proxy, LDAP-backed proxy flows—to converge on a common identity response. `LoginView` can also auto-redirect into a single configured OAuth or SAML provider, which explains why Grafana’s login UX can feel dynamic depending on deployment settings.

Session tokens are long-lived backend objects, not opaque framework cookies. The auth service contract includes create, rotate, revoke, external-session lookup, and active-token enumeration. The implementation details surfaced in `pkg/services/auth/authimpl/auth_token.go` make it clear that token rotation is concurrency-aware and external sessions are treated as first-class state. Operationally, that means Grafana treats session state as a managed security resource with audit/revocation semantics, not just browser state.

Authorization is equally important. Dashboard, datasource, plugin, org, and alerting flows all call access-control evaluators with action/scope pairs. For example, dashboard save/delete/admin actions use dashboard UID-scoped permissions in `pkg/api/dashboard.go`, and datasource pages/actions use datasource-specific evaluators in `pkg/api/api.go` and `pkg/api/datasources.go`. The key idea is that auth in Grafana is a combination of authentication, token/session management, and pervasive fine-grained authorization checks attached to domain resources.

-- KEY WORKFLOWS
The dashboard read workflow starts in `pkg/api/dashboard.go:GetDashboard`. Grafana resolves the dashboard by UID, optionally honoring an API-version hint for unified storage. It then normalizes invalid or sparse JSON, rehydrates compatibility fields like `id`, computes dashboard-scoped permissions, resolves folder metadata, checks whether a public-dashboard projection exists, inspects provisioning state, and finally returns a `DashboardFullWithMeta` payload. That one path explains why Grafana dashboards feel “rich” when loaded: the backend is assembling permission, provenance, and folder context in one request.

The dashboard save workflow is the mirror image. The API binds a dashboard payload, rejects invalid mixed-format cases, constructs a `SaveDashboardCommand`, and sends it through the dashboard service. The service layer in `pkg/services/dashboards/models.go` turns that command into a normalized model, stamps org/folder/plugin/API version metadata, and keeps slug/UID/version state aligned. Provisioned dashboards complicate the flow because UI edits may be blocked depending on provisioning config, so the save path has to remain aware of file-backed ownership.

The datasource lifecycle is another core workflow. On list/get, Grafana loads datasource rows, filters them through read permissions, enriches them from the plugin registry, and attaches access-control metadata. On create/update, it validates structural fields plus plugin-specific JSON/header constraints, encrypts secure fields, persists the datasource, and updates resolver state used by RBAC scope lookups. On delete, it blocks read-only datasources, removes the row, notifies the live subsystem, and invalidates name-based scope caches. This workflow shows that “configure a datasource” is really “register a secured plugin integration and update the rest of the system to know about it.”

Unified alerting is the most orchestration-heavy workflow. `pkg/services/ngalert/api/api.go` creates proxy services for Alertmanager, Prometheus, and Ruler APIs, then layers Grafana-specific authz, provenance, quota, testing, and history services on top. A user editing alert rules in the UI is therefore not just changing a dashboard artifact; they are driving a coordinated pipeline across rule storage, evaluator/backtesting logic, datasource authorization, notification policies, and multi-org alertmanager state.

Finally, auth/session lifecycle is its own recurring workflow. `/login` can render a page, short-circuit into auto-login, attach login tokens for auth-proxy users, or redirect an already authenticated user to the appropriate post-login location. `/login` POST delegates to the authn service, which returns an identity that is then converted into cookies/session state. After that, token rotation, logout, and session revocation continue through the auth service contract. In practice, Grafana’s operational behavior depends heavily on this workflow because every product surface—dashboards, data sources, alerting, plugins—ultimately assumes the auth stack can issue identities, preserve redirects safely, and evaluate per-resource permissions correctly.

--- END DEEP DOMAIN CONTEXT ---

--- CLUE FILE START ---
=CC v2.1 grafana@HEAD 3950mod 35887sym
? What are the main administrative permission tiers in Grafana and where do their boundaries sit?


-- README
![Grafana Logo (Light)](docs/logo-horizontal.png#gh-light-mode-only) ![Grafana Logo (Dark)](docs/logo-horizontal-dark.png#gh-dark-mode-only)
sections: Get started, Documentation, Contributing, Get involved, License

-- TREE
apps/  (836 files)
devenv/  (12 files)
e2e/  (6 files)
emails/  (1 files)
hack/  (1 files)
kinds/  (1 files)
packages/  (1 files)
pkg/  (3089 files)
public/  (1 files)
scripts/  (4 files)
tools/  (1 files)

-- INDEX
apps/provisioning/pkg/apis/provisioning/v0alpha1/zz_generated.deepcopy.go  1570L  DeepCopy, DeepCopyInto, DeepCopy, DeepCopyInto, DeepCopy
apps/alerting/alertenrichment/pkg/apis/alertenrichment/v1beta1/zz_generated.deepcopy.go   489L  DeepCopy, DeepCopyInto, DeepCopyObject, DeepCopy, DeepCopyInto
apps/scope/pkg/apis/scope/v0alpha1/zz_generated.deepcopy.go   535L  DeepCopy, DeepCopyInto, DeepCopyObject, DeepCopy, DeepCopyInto
pkg/apis/datasource/v0alpha1/zz_generated.deepcopy.go   484L  DeepCopy, DeepCopyInto, DeepCopy, DeepCopyInto, DeepCopyObject
apps/dashboard/pkg/apis/dashboard/v0alpha1/zz_generated.deepcopy.go   413L  DeepCopy, DeepCopyInto, DeepCopy, DeepCopyInto, DeepCopy
pkg/apis/iam/v0alpha1/zz_generated.deepcopy.go   350L  DeepCopy, DeepCopyInto, DeepCopy, DeepCopyInto, DeepCopyObject
pkg/aggregator/apis/aggregation/v0alpha1/zz_generated.deepcopy.go   176L  DeepCopy, DeepCopyInto, DeepCopyObject, DeepCopy, DeepCopyInto
pkg/aggregator/apis/aggregation/zz_generated.deepcopy.go   176L  DeepCopy, DeepCopyInto, DeepCopyObject, DeepCopy, DeepCopyInto
pkg/storage/unified/resourcepb/resource.pb.go  3682L  GetAction, GetFolder, GetKey, GetValue, ProtoReflect
pkg/util/xorm/dialect_postgres.go              1253L  getIndexColName, parseOpts, parseURL, AutoIncrStr, DropIndexSql
pkg/services/folder/folderimpl/folder_unifiedstorage.go   761L  Create, Delete, Get, GetChildren, GetDescendantCounts
pkg/util/xorm/session_get.go                    235L  Get, get, nocacheGet
  ...and 3938 more modules

-- SYM
CLILogger.Errorf                    M pkg/cmd/grafana-cli/logger/loggerV2.go:64     function CLILogger.Errorf
TestPrettyLogger.Errorf             M pkg/plugins/log/fake.go:78     function TestPrettyLogger.Errorf
prettyLogger.Errorf                 M pkg/plugins/log/infra_wrapper.go:55     function prettyLogger.Errorf
XormLogger.Errorf                   M pkg/services/sqlstore/logger.go:33     Errorf implement core.ILogger
SimpleLogger.Errorf                 M pkg/util/xorm/logger.go:98     Errorf implement core.ILogger
SyslogLogger.Errorf                 M pkg/util/xorm/syslogger.go:46     Errorf log content as Errorf and format
Base.Errorf                         M pkg/apimachinery/errutil/errors.go:261    Errorf creates a new [Error] with Reason and Me...
XormLogger.Error                    M pkg/services/sqlstore/logger.go:26     Error implement core.ILogger
addNewlines                         M pkg/cmd/grafana-cli/logger/loggerV2.go:68     function addNewlines
MockGrafanaMetaAccessor_FindTitle_Call.Return M pkg/apimachinery/utils/meta_mock.go:69     function MockGrafanaMetaAccessor_FindTitle_Call...
tracingServerStream.Context         M pkg/services/grpcserver/interceptors/tracing.go:36     function tracingServerStream.Context
ResourceInfo.Context                M pkg/services/authz/zanzana/common/info.go:184    function ResourceInfo.Context
Session.Context                     M pkg/util/xorm/session_context.go:10     Context sets the context on this session
OSSMigrations.AddMigration          M pkg/services/sqlstore/migrations/migrations.go:30     function OSSMigrations.AddMigration
Migrator.AddMigration               M pkg/services/sqlstore/migrator/migrator.go:149    function Migrator.AddMigration
Migrator.AddCreateMigration         M pkg/services/sqlstore/migrator/migrator.go:131    AddCreateMigration adds the initial migration l...
MigrationBase.SetId                 M pkg/services/sqlstore/migrator/migrations.go:18     function MigrationBase.SetId
pooledClientConn.Invoke             M pkg/storage/unified/grpc_pool.go:22     Invoke implements the grpc.ClientConnInterface....
MockGrafanaMetaAccessor_FindTitle_Call.Run M pkg/apimachinery/utils/meta_mock.go:62     function MockGrafanaMetaAccessor_FindTitle_Call...
ResourceInfo.GroupVersionKind       M pkg/apimachinery/utils/resource.go:91     function ResourceInfo.GroupVersionKind
zapFieldsToArgs                     M pkg/services/authz/zanzana/logger/logger.go:27     Simple converter for zap logger fields
FakeDB.WithDbSession                M pkg/infra/db/dbtest/dbtest.go:27     function FakeDB.WithDbSession
SQLStore.WithDbSession              M pkg/services/sqlstore/session.go:75     WithDbSession calls the callback with the sessi...
Author.DeepCopyInto                 M apps/provisioning/pkg/apis/provisioning/v0alpha1/zz_generated.deepcopy.go:16     DeepCopyInto is an autogenerated deepcopy funct...
NormalResponse.Err                  M pkg/api/response/response.go:76     Err gets the response's err.
sectionGetter.Err                   M pkg/storage/unified/sql/db/dbimpl/util.go:37     function sectionGetter.Err
Row.Err                             M pkg/storage/unified/sql/db/mocks/Row.go:21     Err provides a mock function with no fields
Row_Expecter.Err                    M pkg/storage/unified/sql/db/mocks/Row.go:44     Err is a helper method to define mock.On call
Rows.Err                            M pkg/storage/unified/sql/db/mocks/Rows.go:66     Err provides a mock function with no fields
Rows_Expecter.Err                   M pkg/storage/unified/sql/db/mocks/Rows.go:89     Err is a helper method to define mock.On call
contextWithCancellableReason.Err    M pkg/util/contextutil.go:16     function contextWithCancellableReason.Err
Rows.Err                            M pkg/util/xorm/rows.go:73     Err returns the error, if any, that was encount...
SQLStore.withDbSession              M pkg/services/sqlstore/session.go:105    function SQLStore.withDbSession
ConcreteLogger.log                  M pkg/infra/log/log.go:217    function ConcreteLogger.log
formatArgs                          M pkg/plugins/backendplugin/grpcplugin/log_wrapper.go:20     function formatArgs
Logs.Call                           M pkg/plugins/log/fake.go:53     function Logs.Call
MockGithubRepository_Client_Call.Return M apps/provisioning/pkg/repository/github/github_repository_mock.go:64     function MockGithubRepository_Client_Call.Return
MockGitRepository_Branch_Call.Return M apps/provisioning/pkg/repository/git/git_repository_mock.go:62     function MockGitRepository_Branch_Call.Return
RemoteAlertmanagerMock_ApplyConfig_Call.Return M pkg/services/ngalert/remote/mock/remoteAlertmanager.go:77     function RemoteAlertmanagerMock_ApplyConfig_Cal...
MockProvider.Section                M pkg/setting/settingtest/provider_mock.go:81     Section provides a mock function with given fie...
New                                 M pkg/components/simplejson/simplejson.go:105    New returns a pointer to a new, empty `Json` ob...
MockResourceClient_BulkProcess_Call.Return M pkg/storage/unified/resource/client_mock.go:91     function MockResourceClient_BulkProcess_Call.Re...
ResourceVersionManager.Lock         M pkg/storage/unified/sql/rvmanager/rv_manager.go:385    Lock locks the resource version for the given key
BaseDialect.Unlock                  M pkg/services/sqlstore/migrator/dialect.go:376    function BaseDialect.Unlock
MySQLDialect.Unlock                 M pkg/services/sqlstore/migrator/mysql_dialect.go:298    function MySQLDialect.Unlock
PostgresDialect.Unlock              M pkg/services/sqlstore/migrator/postgres_dialect.go:330    function PostgresDialect.Unlock
UnknownReceiverError.Error          M pkg/services/ngalert/notifier/alertmanager_config.go:52     function UnknownReceiverError.Error
Server.Bind                         M pkg/services/ldap/ldap.go:59     Bind authenticates the connection with the LDAP...
MockRepositoryResources_EnsureFolderExists_Call.Return M pkg/registry/apis/provisioning/resources/repository_resources_mock.go:67     function MockRepositoryResources_EnsureFolderEx...
  ...and 34256 more symbols

-- FOCUS
devenv/docker/blocks/traefik/docker-compose.yml (devenv/docker/blocks/traefik/docker-compose.yml:1-20)
  Config summary for devenv/docker/blocks/traefik/docker-compose.yml: entries: traefik: traefik:v2.1, grafana-subpath: grafana/grafana:latest; services: traefik, volumes, ports, depends_on, grafana-subpath, environment
  entries: traefik: traefik:v2.1, grafana-subpath: grafana/grafana:latest
  services: traefik, volumes, ports, depends_on, grafana-subpath

emails/package.json (emails/package.json:1-17)
  Config summary for emails/package.json: deps: grunt, grunt-assemble, grunt-cli, grunt-contrib-copy, grunt-contrib-watch, grunt-text-replace, load-grunt-config, mjml
  deps: grunt, grunt-assemble, grunt-cli, grunt-contrib-copy, grunt-contrib-watch, grunt-text-replace

package.json (package.json:1-507)
  Config summary for package.json: deps: @bsull/augurs, @emotion/css, @emotion/react, @fingerprintjs/fingerprintjs, @floating-ui/react, @formatjs/intl-durationformat, @grafana/alerting, @grafana/api-clients
  deps: @bsull/augurs, @emotion/css, @emotion/react, @fingerprintjs/fingerprintjs, @floating-ui/react, @formatjs/intl-durationformat

main (scripts/openapi3/openapi3conv.go:18-18)
  main This simple script will take the swagger v2 spec generated by grafana and convert them into openapi 3 saving them a
  behavior: PRECEDENCE(len -> inFile)
  calls: ReadFile, postProcessSwaggerFile
  raises: panic

main (tools/setup_grafana_alertmanager_integration_test_images.go:22-22)
  behavior: ACCUMULATE(GetGrafanaImage loop -> result)
  calls: Add, Wait, Done, docker

MainApp (pkg/cmd/grafana/main.go:35-35)
  calls: GetCLICommand
  called_by: main

main (pkg/tsdb/grafana-testdata-datasource/standalone/main.go:10-10)
  calls: Error

main (pkg/tsdb/grafana-pyroscope-datasource/standalone/main.go:10-10)
  calls: Error

main (pkg/tsdb/grafana-postgresql-datasource/standalone/main.go:12-12)
  calls: Error

main (pkg/cmd/grafana/main.go:24-24)
  calls: Run, MainApp

grafanaInfraLogWrapper.New (pkg/services/pluginsintegration/pluginslog/pluginslog.go:23-23)
  sig: grafanaInfraLogWrapper.New(ctx ...any)
  behavior: GUARD(len(ctx) == 0 -> return &grafanaInfr...)
  calls: New
  called_by: ProvideAvatarCacheServer, NewKeyVal, Static, unsupported, RunServer, RunTargetServer, NewBasicFormatter, NewJSONFormatter

AlertmanagerApiHandler.handleRouteGetGrafanaAMAlertGroups (pkg/services/ngalert/api/forking_alertmanager.go:148-148)
  sig: AlertmanagerApiHandler.handleRouteGetGrafanaAMAlertGroups(ctx *contextmodel.ReqContext)
  behavior: DELEGATE(f.GrafanaSvc.RouteGetAMAlertGroups -> result)
  called_by: RouteGetGrafanaAMAlertGroups

ResourceSearchRequest.GetPermission (pkg/storage/unified/resourcepb/search.pb.go:348-348)
  behavior: GUARD(x != nil -> return x.Permission)
  called_by: GetResourcePermissionDeleteTuple, GetResourcePermissionWriteTuple

api.setSinglePermissionToK8s (pkg/services/accesscontrol/resourcepermissions/api_adapter.go:470-470)
  sig: api.setSinglePermissionToK8s(c *contextmodel.ReqContext, namespace string, resourceID...)
  behavior: GUARD(err != nil -> return err); PRECEDENCE(err -> permission); ACCUMULATE(string loop -> newPermissions perm)
  calls: Errorf, buildResourcePermissionName, createOrUpdateResourcePermission, getAPIGroup, getDynamicClient, getExistingResourcePermission, Context
  called_by: setBuiltInRolePermissionToK8s, setTeamPermissionToK8s, setUserPermissionToK8s

PermissionType.String (pkg/services/team/model.go:127-127)
  behavior: GUARD(p == PermissionTypeAdmin -> return "Admin")
  called_by: GetMeta, generateShortUID, Push, RangeQuery, generate, runAction, ServeHTTP, KeyVal

AlertmanagerApiHandler.RouteDeleteGrafanaSilence (pkg/services/ngalert/api/generated_base_api_alertmanager.go:72-72)
  sig: AlertmanagerApiHandler.RouteDeleteGrafanaSilence(ctx *contextmodel.ReqContext)
  behavior: DELEGATE(f.handleRouteDeleteGrafanaSilence -> result)
  calls: handleRouteDeleteGrafanaSilence

AlertmanagerApiHandler.RouteGetGrafanaAMAlertGroups (pkg/services/ngalert/api/generated_base_api_alertmanager.go:103-103)
  sig: AlertmanagerApiHandler.RouteGetGrafanaAMAlertGroups(ctx *contextmodel.ReqContext)
  behavior: DELEGATE(f.handleRouteGetGrafanaAMAlertGroups -> result)
  calls: handleRouteGetGrafanaAMAlertGroups

AlertmanagerApiHandler.RouteGetGrafanaAMAlerts (pkg/services/ngalert/api/generated_base_api_alertmanager.go:106-106)
  sig: AlertmanagerApiHandler.RouteGetGrafanaAMAlerts(ctx *contextmodel.ReqContext)
  behavior: DELEGATE(f.handleRouteGetGrafanaAMAlerts -> result)
  calls: handleRouteGetGrafanaAMAlerts

AlertmanagerApiHandler.RouteGetGrafanaAMStatus (pkg/services/ngalert/api/generated_base_api_alertmanager.go:109-109)
  sig: AlertmanagerApiHandler.RouteGetGrafanaAMStatus(ctx *contextmodel.ReqContext)
  behavior: DELEGATE(f.handleRouteGetGrafanaAMStatus -> result)
  calls: handleRouteGetGrafanaAMStatus

AlertmanagerApiHandler.RouteGetGrafanaAlertingConfig (pkg/services/ngalert/api/generated_base_api_alertmanager.go:112-112)
  sig: AlertmanagerApiHandler.RouteGetGrafanaAlertingConfig(ctx *contextmodel.ReqContext)
  behavior: DELEGATE(f.handleRouteGetGrafanaAlertingConfig -> result)
  calls: handleRouteGetGrafanaAlertingConfig

AlertmanagerApiHandler.RouteGetGrafanaAlertingConfigHistory (pkg/services/ngalert/api/generated_base_api_alertmanager.go:115-115)
  sig: AlertmanagerApiHandler.RouteGetGrafanaAlertingConfigHistory(ctx *contextmodel.ReqContext)
  behavior: DELEGATE(f.handleRouteGetGrafanaAlertingConfigHistory -> result)
  calls: handleRouteGetGrafanaAlertingConfigHistory

AlertmanagerApiHandler.RouteGetGrafanaReceivers (pkg/services/ngalert/api/generated_base_api_alertmanager.go:118-118)
  sig: AlertmanagerApiHandler.RouteGetGrafanaReceivers(ctx *contextmodel.ReqContext)
  behavior: DELEGATE(f.handleRouteGetGrafanaReceivers -> result)
  calls: handleRouteGetGrafanaReceivers

AlertmanagerApiHandler.RouteGetGrafanaSilence (pkg/services/ngalert/api/generated_base_api_alertmanager.go:121-121)
  sig: AlertmanagerApiHandler.RouteGetGrafanaSilence(ctx *contextmodel.ReqContext)
  behavior: DELEGATE(f.handleRouteGetGrafanaSilence -> result)
  calls: handleRouteGetGrafanaSilence

AlertmanagerApiHandler.RouteGetGrafanaSilences (pkg/services/ngalert/api/generated_base_api_alertmanager.go:126-126)
  sig: AlertmanagerApiHandler.RouteGetGrafanaSilences(ctx *contextmodel.ReqContext)
  behavior: DELEGATE(f.handleRouteGetGrafanaSilences -> result)
  calls: handleRouteGetGrafanaSilences

AlertmanagerApiHandler.RoutePostGrafanaAlertingConfigHistoryActivate (pkg/services/ngalert/api/generated_base_api_alertmanager.go:160-160)
  sig: AlertmanagerApiHandler.RoutePostGrafanaAlertingConfigHistoryActivate(ctx *contextmodel.ReqContext)
  behavior: DELEGATE(f.handleRoutePostGrafanaAlertingConfigHistoryActivate -> result)
  calls: handleRoutePostGrafanaAlertingConfigHistoryActivate

AlertmanagerApiHandler.RoutePostTestGrafanaReceivers (pkg/services/ngalert/api/generated_base_api_alertmanager.go:165-165)
  sig: AlertmanagerApiHandler.RoutePostTestGrafanaReceivers(ctx *contextmodel.ReqContext)
  behavior: DELEGATE(f.handleRoutePostTestGrafanaReceivers -> result)
  calls: handleRoutePostTestGrafanaReceivers

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 83 symbols in L3, 75 with behavior annotations
uncovered: TranslateResourcePermissionToTuples, api.setBuiltInRolePermissionToK8s, changeInfo.GrafanaHost, dashboardUidPermissionMigrator.migrateWildcards

--- CLUE FILE END ---

QUESTION: What are the main administrative permission tiers in Grafana and where do their boundaries sit?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
