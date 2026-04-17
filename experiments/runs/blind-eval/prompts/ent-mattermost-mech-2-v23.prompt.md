# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-mattermost-mech-2

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 mattermost@HEAD 1346mod 19215sym
? How are security-sensitive issues and security updates handled in Mattermost's policy docs?


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

App.CreateOrUpdateAccessControlPolicy (server/channels/app/access_control.go:77-77)
  sig: App.CreateOrUpdateAccessControlPolicy(rctx request.CTX, policy *model.AccessControlPolicy)
  behavior: GUARD(acs == nil -> return nil, model.N...); PRECEDENCE(acs -> policy -> appErr); ACCUMULATE(loop -> result)
  calls: Srv, SavePolicy
  called_by: createAccessControlPolicy

AccessControlPolicyActiveUpdate (server/public/model/access_policy.go:117-117)
  AccessControlPolicyActiveUpdate represents a single policy's active status update.

AccessControlPolicyActiveUpdateRequest (server/public/model/access_policy.go:123-123)
  AccessControlPolicyActiveUpdateRequest is used in the API to update active status for multiple policies.
  methods: Auditable

AccessControlPolicyActiveUpdateRequest.Auditable (server/public/model/access_policy.go:128-128)
  behavior: ACCUMULATE(append loop -> entries map)
  called_by: Auditable, AddEventParameterAuditableToAuditRec, LogClone

Server.DoSecurityUpdateCheck (server/channels/app/security_update_check.go:35-35)
  behavior: GUARD(!*s.platform.Config().ServiceSettings.EnableS... -> return); PRECEDENCE(not_s.platform.Config -> err -> currentTime)
  calls: License, Log, ServerId, Set, MailServiceConfig, Store, Encode
  called_by: doSecurity

App.AssignAccessControlPolicyToChannels (server/channels/app/access_control.go:147-147)
  sig: App.AssignAccessControlPolicyToChannels(rctx request.CTX, parentID string, channelIDs []string)
  behavior: GUARD(acs == nil -> return nil, model.N...); PRECEDENCE(acs -> appErr -> policy); ACCUMULATE(ValidateChannelEligib... -> policies child)
  calls: GetAccessControlPolicy, ValidateChannelEligibilityForAccessControl, Srv, GetChannels, Error, GetPolicy, SavePolicy
  called_by: assignAccessPolicy

App.GetChannelsForPolicy (server/channels/app/access_control.go:20-20)
  sig: App.GetChannelsForPolicy(rctx request.CTX, policyID string, cursor model.AccessCo...)
  behavior: GUARD(appErr != nil -> return nil, 0, appErr); DISPATCH(policy)
  calls: GetAccessControlPolicy, Srv, Error
  called_by: getChannelsForAccessControlPolicy

App.ValidateAccessControlPolicyPermission (server/channels/app/access_control.go:390-390)
  ValidateAccessControlPolicyPermission validates if a user has permission to manage a specific existing access control po
  sig: App.ValidateAccessControlPolicyPermission(rctx request.CTX, userID, policyID string)
  behavior: DELEGATE(a.ValidateAccessControlPolicyPermissionWithOptions -> result)
  calls: ValidateAccessControlPolicyPermissionWithOptions
  called_by: deleteAccessControlPolicy, setActiveStatus, updateActiveStatus

App.ValidateAccessControlPolicyPermissionWithChannelContext (server/channels/app/access_control.go:442-442)
  ValidateAccessControlPolicyPermissionWithChannelContext validates access control policy permissions with channel context
  sig: App.ValidateAccessControlPolicyPermissionWithChannelContext(rctx request.CTX, userID, policyID string, isReadOnly bo...)
  behavior: DELEGATE(a.ValidateAccessControlPolicyPermissionWithOptions -> result)
  calls: ValidateAccessControlPolicyPermissionWithOptions
  called_by: getAccessControlPolicy

App.ValidateAccessControlPolicyPermissionWithMode (server/channels/app/access_control.go:435-435)
  ValidateAccessControlPolicyPermissionWithMode validates access control policy permissions with read-only mode option
  sig: App.ValidateAccessControlPolicyPermissionWithMode(rctx request.CTX, userID, policyID string, isReadOnly bool)
  behavior: DELEGATE(a.ValidateAccessControlPolicyPermissionWithOptions -> result)
  calls: ValidateAccessControlPolicyPermissionWithOptions

App.ValidateChannelAccessControlPolicyCreation (server/channels/app/access_control.go:466-466)
  ValidateChannelAccessControlPolicyCreation validates if a user can create a channel-specific access control policy
  sig: App.ValidateChannelAccessControlPolicyCreation(rctx request.CTX, userID string, policy *model.AccessCon...)
  behavior: GUARD(a.HasPermissionTo(userID, model.PermissionMan... -> return nil); PRECEDENCE(a -> policy)
  calls: ValidateChannelAccessControlPermission, HasPermissionTo
  called_by: createAccessControlPolicy

App.isSystemPolicyAppliedToChannel (server/channels/app/access_control.go:450-450)
  isSystemPolicyAppliedToChannel checks if a system policy is applied to a specific channel
  sig: App.isSystemPolicyAppliedToChannel(rctx request.CTX, policyID, channelID string)
  behavior: GUARD(err != nil -> return false); PRECEDENCE(err -> channelPolicy)
  calls: GetAccessControlPolicy
  called_by: ValidateAccessControlPolicyPermissionWithOptions

SqlAccessControlPolicyStore.Delete (server/channels/store/sqlstore/access_control_policy_store.go:305-305)
  sig: SqlAccessControlPolicyStore.Delete(rctx request.CTX, id string)
  behavior: GUARD(err != nil -> return errors.Wrap(...); PRECEDENCE(err -> existingPolicy); UNWIND(defer)
  calls: deleteT, getT, accessControlPolicyHistorySliceColumns, fromModel, GetMaster, ExecBuilder, IsBinaryParamEnabled, getQueryBuilder
  called_by: deleteT, SaveOrUpdate, removeState, DeletePanelPostID

SqlAccessControlPolicyStore.Save (server/channels/store/sqlstore/access_control_policy_store.go:184-184)
  sig: SqlAccessControlPolicyStore.Save(rctx request.CTX, policy *model.AccessControlPolicy)
  behavior: GUARD(err := policy.IsValid(); err != nil -> return nil, err); PRECEDENCE(err); UNWIND(defer)
  calls: deleteT, getHistoryT, getT, accessControlPolicyHistorySliceColumns, accessControlPolicySliceColumns, fromModel, preSaveAccessControlPolicy, toModel
  called_by: Upsert, testCommandWebhookStore

SqlRetentionPolicyStore.Save (server/channels/store/sqlstore/retention_policy_store.go:41-41)
  sig: SqlRetentionPolicyStore.Save(policy *model.RetentionPolicyWithTeamAndChannelIDs)
  behavior: GUARD(err = s.checkTeamsExist(policy.TeamIDs); err... -> return nil, err); PRECEDENCE(err); UNWIND(defer)
  calls: Get, buildGetPolicyQuery, buildInsertRetentionPoliciesChannelsQuery, buildInsertRetentionPoliciesTeamsQuery, checkChannelsExist, checkTeamsExist, executePossiblyEmptyQuery, GetMaster
  called_by: Upsert, testCommandWebhookStore

createAccessControlPolicy (server/channels/api4/access_control.go:40-40)
  sig: createAccessControlPolicy(c *Context, w http.ResponseWriter, r *http.Request)
  behavior: GUARD(jsonErr := json.NewDecoder(r.Body).Decode(&po... -> return); PRECEDENCE(jsonErr -> policy -> appErr); UNWIND(defer)
  calls: CreateOrUpdateAccessControlPolicy, ValidateChannelAccessControlPolicyCreation, LogAuditRec, MakeAuditRecord, HasPermissionToChannel, SessionHasPermissionTo, SessionHasPermissionToTeam, Config

testAccessControlPolicyStoreSearchByActions (server/channels/store/storetest/access_control_policy_store.go:741-741)
  sig: testAccessControlPolicyStoreSearchByActions(t *testing.T, rctx request.CTX, ss store.Store)
  behavior: ACCUMULATE(AccessControlPolicy loop -> result)
  calls: Run, AccessControlPolicy, Cleanup
  called_by: TestAccessControlPolicyStore

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 83 symbols in L3, 28 with behavior annotations
uncovered: RetentionPolicyForTeamList, RetentionPolicyStore, RetentionPolicyStore, RetentionPolicyTeam

--- CLUE FILE END ---

QUESTION: How are security-sensitive issues and security updates handled in Mattermost's policy docs?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
