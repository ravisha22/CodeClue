# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-mattermost-rel-2

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 mattermost@HEAD 1346mod 19215sym
? Which admin and compliance gates span channel discovery and team deletion?


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

PluginAPI.GetChannelByNameForTeamName (server/channels/app/plugin_api.go:501-501)
  sig: PluginAPI.GetChannelByNameForTeamName(teamName, channelName string, includeDeleted bool)
  behavior: DELEGATE(api.app.GetChannelByNameForTeamName -> result)
  calls: GetChannelByNameForTeamName
  called_by: getChannelByNameForTeamName, sanitizeChannelMentionsForUser, GetByNameForTeamName

App.ValidateTeamScopePolicyChannelAssignment (server/channels/app/team_access_control.go:247-247)
  ValidateTeamScopePolicyChannelAssignment validates that all channels are eligible for team policy assignment, is the gat
  sig: App.ValidateTeamScopePolicyChannelAssignment(rctx request.CTX, teamID string, channelIDs []string)
  behavior: GUARD(len(channelIDs) == 0 -> return model.NewApp...); PRECEDENCE(len -> appErr); ACCUMULATE(NewAppError loop -> result)
  calls: GetChannels
  called_by: assignAccessPolicy

App.buildUserTeamAndChannelMemberships (server/channels/app/export.go:632-632)
  sig: App.buildUserTeamAndChannelMemberships(rctx request.CTX, userID string, includeArchivedChannels...)
  behavior: GUARD(err != nil -> return nil, model.N...); ACCUMULATE(importUserTeamDataFro... -> memberships)
  calls: Srv, buildUserChannelMemberships
  called_by: exportAllUsers

App.resolveTeamSyncChannelIDs (server/channels/app/job.go:154-154)
  resolveTeamSyncChannelIDs returns channel IDs the requester can sync, filtered by self-inclusion (same logic as SearchTe
  sig: App.resolveTeamSyncChannelIDs(rctx request.CTX, teamID, requesterID string)
  behavior: GUARD(appErr != nil -> return nil, appErr); ACCUMULATE(loop -> channelIDs id)
  calls: SearchTeamAccessPolicies
  called_by: CreateAccessControlSyncJob

TimerLayerChannelStore.GetPublicChannelsByIdsForTeam (server/channels/store/timerlayer/timerlayer.go:2220-2220)
  sig: TimerLayerChannelStore.GetPublicChannelsByIdsForTeam(teamID string, channelIds []string)
  called_by: getPublicChannelsByIdsForTeam

TimerLayerChannelStore.PermanentDeleteByTeam (server/channels/store/timerlayer/timerlayer.go:2581-2581)
  sig: TimerLayerChannelStore.PermanentDeleteByTeam(teamID string)
  called_by: PermanentDeleteByTeam

RetentionPolicyWithTeamAndChannelIDs.Auditable (server/public/model/data_retention_policy.go:25-25)
  called_by: Auditable, AddEventParameterAuditableToAuditRec, LogClone

copyRetentionPolicyWithTeamAndChannelIds (server/channels/store/storetest/retention_policy_store.go:79-79)
  sig: copyRetentionPolicyWithTeamAndChannelIds(policy *model.RetentionPolicyWithTeamAndChannelIDs)
  called_by: testRetentionPolicyStoreAddChannels, testRetentionPolicyStoreAddTeams, testRetentionPolicyStorePatch, testRetentionPolicyStoreRemoveChannels, testRetentionPolicyStoreRemoveTeams

ChannelMemberWithTeamData (server/public/model/channel_member.go:106-106)
  ChannelMemberWithTeamData contains ChannelMember appended with extra team information as well.

ChannelTeam (server/cmd/mmctl/commands/importer/validate.go:41-41)
  type ChannelTeam

ChannelWithTeamData (server/public/model/channel.go:137-137)
  type ChannelWithTeamData

ChannelWithTeamDataAndBookmarks (server/public/model/channel_bookmark.go:249-249)
  type ChannelWithTeamDataAndBookmarks

GroupsAssociatedToChannelWithSchemeAdmin (server/public/model/group.go:101-101)
  type GroupsAssociatedToChannelWithSchemeAdmin

RetentionPolicyWithTeamAndChannelCounts (server/public/model/data_retention_policy.go:33-33)
  type RetentionPolicyWithTeamAndChannelCounts
  methods: Auditable

RetentionPolicyWithTeamAndChannelCountsList (server/public/model/data_retention_policy.go:57-57)
  type RetentionPolicyWithTeamAndChannelCountsList

RetentionPolicyWithTeamAndChannelIDs (server/public/model/data_retention_policy.go:19-19)
  type RetentionPolicyWithTeamAndChannelIDs
  methods: Auditable

Z_GetChannelByNameForTeamNameArgs (server/public/plugin/client_rpc_generated.go:3312-3312)
  type Z_GetChannelByNameForTeamNameArgs

Z_GetChannelByNameForTeamNameReturns (server/public/plugin/client_rpc_generated.go:3318-3318)
  type Z_GetChannelByNameForTeamNameReturns

channelMemberWithTeamWithSchemeRoles (server/channels/store/sqlstore/channel_store.go:97-97)
  type channelMemberWithTeamWithSchemeRoles
  methods: ToModel

groupAssociatedToChannelWithSchemeAdmin (server/channels/store/sqlstore/group_store.go:1208-1208)
  type groupAssociatedToChannelWithSchemeAdmin
  methods: ToModel

API.GetChannelByNameForTeamName (server/public/plugin/plugintest/api.go:1409-1409)
  GetChannelByNameForTeamName provides a mock function with given fields: teamName, channelName, includeDeleted
  sig: API.GetChannelByNameForTeamName(teamName string, channelName string, includeDeleted bool)
  calls: Get
  called_by: getChannelByNameForTeamName, GetChannelByNameForTeamName, sanitizeChannelMentionsForUser, GetByNameForTeamName
  raises: panic

App.GetChannelByNameForTeamName (server/channels/app/channel.go:2171-2171)
  sig: App.GetChannelByNameForTeamName(rctx request.CTX, channelName, teamName string, includeD...)
  calls: Srv
  called_by: getChannelByNameForTeamName, GetChannelByNameForTeamName, sanitizeChannelMentionsForUser, GetByNameForTeamName

App.GetChannelMembersWithTeamDataForUserWithPagination (server/channels/app/channel.go:2437-2437)
  sig: App.GetChannelMembersWithTeamDataForUserWithPagination(rctx request.CTX, userID string, cursor *model.ChannelMe...)
  calls: Srv
  called_by: getChannelMembersForUser

App.GetTeamSchemeChannelRoles (server/channels/app/channel.go:1030-1030)
  GetTeamSchemeChannelRoles Checks if a team has an override scheme and returns the scheme channel role names or default c
  sig: App.GetTeamSchemeChannelRoles(rctx request.CTX, teamID string)
  calls: GetTeam, GetScheme
  called_by: GetChannelModerationsForChannel, GetSchemeRolesForChannel, PatchChannelModerationsForChannel

App.GetUsersInChannelByAdmin (server/channels/app/user.go:693-693)
  sig: App.GetUsersInChannelByAdmin(options *model.UserGetOptions)
  calls: Srv
  called_by: GetUsersInChannelPageByAdmin

App.GetUsersInChannelPageByAdmin (server/channels/app/user.go:734-734)
  sig: App.GetUsersInChannelPageByAdmin(options *model.UserGetOptions, asAdmin bool)
  calls: GetUsersInChannelByAdmin, sanitizeProfiles
  called_by: getUsers

App.RemoveUsersFromChannelNotMemberOfTeam (server/channels/app/channel.go:3568-3568)
  sig: App.RemoveUsersFromChannelNotMemberOfTeam(rctx request.CTX, remover *model.User, channel *model.Ch...)
  calls: GetChannelMembersPage, removeUserFromChannel, GetTeamMembersByIds
  called_by: moveChannel, localMoveChannel, MoveChannel

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 83 symbols in L3, 13 with behavior annotations
uncovered: SqlChannelStore.SearchInTeam, SqlChannelStore.autocompleteInTeamForSearchDirectMessages, SqlChannelStore.buildAutocompleteInTeamQuery, SqlRoleStore.ChannelRolesUnderTeamRole

--- CLUE FILE END ---

QUESTION: Which admin and compliance gates span channel discovery and team deletion?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
