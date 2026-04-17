# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-grafana-struct-2

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 grafana@HEAD 3950mod 35887sym
? What plugin surfaces and security controls does Grafana expose?


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

GrafanaPluginId (pkg/semconv/attributes.go:139-139)
  GrafanaPluginId returns an attribute KeyValue conforming to the "grafana.plugin.id" semantic conventions.
  sig: GrafanaPluginId(val string)
  behavior: DELEGATE(grafanaPluginIdKey.String -> result)

GrafanaLive.getStreamPlugin (pkg/services/live/live.go:497-497)
  sig: GrafanaLive.getStreamPlugin(ctx context.Context, pluginID string)
  behavior: GUARD(!exists -> return nil, fmt.Err...); PRECEDENCE(not_exists -> plugin)
  calls: Errorf
  called_by: handleDatasourceScope, handlePluginScope

installPlugin (pkg/cmd/grafana-cli/commands/install_command.go:108-108)
  installPlugin downloads the plugin code as a zip file from the Grafana.com API and then extracts the zip into the plugin
  sig: installPlugin(ctx context.Context, pluginID, version string, o pluginI...)
  behavior: DELEGATE(doInstallPlugin -> result)
  calls: doInstallPlugin
  called_by: installCommand

grafanaComChildPluginVersion (apps/plugins/pkg/app/meta/converter.go:732-732)
  grafanaComChildPluginVersion represents a child plugin in the parent's version response.

grafanaComPluginManifest (apps/plugins/pkg/app/meta/converter.go:741-741)
  type grafanaComPluginManifest

grafanaComPluginVersionMeta (apps/plugins/pkg/app/meta/converter.go:717-717)
  grafanaComPluginVersionMeta represents the response from grafana.com API GET /api/plugins/{pluginId}/versions/{version}

grafanaComPluginVersionMetaJSON (apps/plugins/pkg/app/meta/converter.go:710-710)
  grafanaComPluginVersionMetaJSON is a wrapper around MetaJSONData that includes additional fields like aliasIDs which are

GetGrafanaPluginDir (pkg/cmd/grafana-cli/utils/grafana_path.go:11-11)
  sig: GetGrafanaPluginDir(currentOS string)
  behavior: GUARD(rootPath, ok := tryGetRootForDevEnvironment()... -> return filepath.Jo...)
  calls: returnOsDefault, tryGetRootForDevEnvironment

GrafanaLive.handlePluginScope (pkg/services/live/live.go:989-989)
  sig: GrafanaLive.handlePluginScope(ctx context.Context, _ identity.Requester, namespace str...)
  behavior: GUARD(err != nil -> return nil, fmt.Err...)
  calls: Errorf, getStreamPlugin
  called_by: GetChannelHandlerFactory

Manager.grafanaCompatiblePluginVersions (pkg/plugins/repo/service.go:110-110)
  grafanaCompatiblePluginVersions will get version info from /api/plugins/$pluginID/versions
  sig: Manager.grafanaCompatiblePluginVersions(ctx context.Context, pluginID string, compatOpts CompatO...)
  behavior: GUARD(err != nil -> return nil, err); PRECEDENCE(err)
  calls: Error, Parse
  called_by: PluginVersion

grafanaComChildPluginVersionToMetaSpec (apps/plugins/pkg/app/meta/converter.go:756-756)
  grafanaComChildPluginVersionToMetaSpec converts a child plugin version to a MetaSpec.
  sig: grafanaComChildPluginVersionToMetaSpec(logger logging.Logger, child grafanaComChildPluginVersio...)
  behavior: GUARD(err != nil -> return pluginsv0alp...)
  calls: grafanaComPluginVersionMetaToMetaSpec, Errorf

grafanaComPluginVersionMetaToMetaSpec (apps/plugins/pkg/app/meta/converter.go:779-779)
  grafanaComPluginVersionMetaToMetaSpec converts a grafanaComPluginVersionMeta to a pluginsv0alpha1.MetaSpec.
  sig: grafanaComPluginVersionMetaToMetaSpec(logger logging.Logger, gcomMeta grafanaComPluginVersionM...)
  behavior: PRECEDENCE(len -> gcomMeta -> err); ACCUMULATE(append loop -> children c Slug)
  calls: calculateLoadingStrategyFromGcomMeta, translationsFromManifest, Errorf
  called_by: grafanaComChildPluginVersionToMetaSpec

CatalogPluginSpec (pkg/build/daggerbuild/arguments/catalog_plugins.go:16-16)
  CatalogPluginSpec defines a plugin to download from the Grafana catalog.

PluginInfo (pkg/plugins/repo/models.go:37-37)
  PluginInfo is (a subset of) the JSON response from grafana.com/api/plugins/$pluginID

corePlugin (pkg/plugins/backendplugin/coreplugin/core_plugin.go:15-15)
  corePlugin represents a plugin that's part of Grafana core.
  methods: CallResource, CheckHealth, CollectMetrics, ConvertObjects, Decommission, Exited

BuildPluginDownloadURL (pkg/build/daggerbuild/plugins/downloader.go:185-185)
  BuildPluginDownloadURL constructs the URL for downloading a plugin from grafana.com.
  sig: BuildPluginDownloadURL(pluginID, version string)
  behavior: DELEGATE(fmt.Sprintf -> result)
  called_by: ResolvePluginVersions

DBstore.filterByPluginOrigin (pkg/services/ngalert/store/alert_rule.go:1685-1685)
  filterByPluginOrigin adds filtering for plugin-originated rules based on the __grafana_origin label.
  sig: DBstore.filterByPluginOrigin(filter ngmodels.PluginOriginFilter, sess *xorm.Session)
  calls: Errorf
  called_by: buildListAlertRulesQuery

doInstallPlugin (pkg/cmd/grafana-cli/commands/install_command.go:114-114)
  doInstallPlugin is a recursive function that installs a plugin and its dependencies.
  sig: doInstallPlugin(ctx context.Context, pluginID, version string, o pluginI...)
  behavior: GUARD(installing[pluginID] -> return nil); PRECEDENCE(installing -> version -> o); ACCUMULATE(Infof loop -> result)
  called_by: installPlugin

Manager.PluginVersion (pkg/plugins/repo/service.go:84-84)
  PluginVersion will return plugin version based on the requested information
  sig: Manager.PluginVersion(ctx context.Context, pluginID, version string, compatOpt...)
  behavior: GUARD(err != nil -> return VersionData{...); PRECEDENCE(err -> isGrafanaCorePlugin)
  calls: grafanaCompatiblePluginVersions
  called_by: GetPluginArchiveInfo

DataPluginConfiguration (pkg/tsdb/grafana-postgresql-datasource/sqleng/sql_engine.go:76-76)
  type DataPluginConfiguration

InstalledPlugin (pkg/cmd/grafana-cli/models/model.go:8-8)
  type InstalledPlugin

Plugin (pkg/cmd/grafana-cli/models/model.go:27-27)
  type Plugin

PluginInfo (pkg/cmd/grafana-cli/models/model.go:22-22)
  type PluginInfo

PluginRepo (pkg/cmd/grafana-cli/models/model.go:45-45)
  type PluginRepo

pluginInstallOpts (pkg/cmd/grafana-cli/commands/install_command.go:88-88)
  type pluginInstallOpts

AccessControlStore.CleanupPluginRBAC (pkg/services/accesscontrol/database/cleanup.go:17-17)
  CleanupPluginRBAC removes all RBAC data associated with the given plugin IDs:   - permissions on any role whose action s
  sig: AccessControlStore.CleanupPluginRBAC(ctx context.Context, pluginIDs []string)
  behavior: ACCUMULATE(ContainsAny loop -> result)
  calls: Errorf, cleanupPlugin

ContextCommandLine.PluginDirectory (pkg/cmd/grafana-cli/utils/command_line.go:57-57)
  behavior: DELEGATE(c.String -> result)
  calls: String
  called_by: newInstallPluginOpts, uninstallPlugin, validateInput, lsCommand, upgradeAllCommand, upgradeCommand

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 83 symbols in L3, 61 with behavior annotations
uncovered: GetDatasourceGroupNameFromPluginID, GetPluginIDFromMeta, GrafanaDatasourceRequestQueryCount, GrafanaDatasourceType

--- CLUE FILE END ---

QUESTION: What plugin surfaces and security controls does Grafana expose?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
