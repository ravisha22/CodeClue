# Blind Evaluation Prompt - MRLF v2.4
# Task: ent-mattermost-struct-1

You are a senior software engineer. You have been given a codebase
comprehension artifact (a "clue file") that summarises a repository's
structure, symbols, and behavior. This is NOT the full source code - it is
a compressed representation.

Answer the question below using ONLY the information in the clue file.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the modules, symbols, or relationships most relevant to the question from FOCUS, SYM, INDEX, and TREE. Trace them through the clue before concluding: follow calls: chains, walk extends: hierarchies, and use behavior: annotations as summaries of how control or responsibility moves. Use TREE and INDEX to situate the relationship in the repository structure. State explicitly what GAPS says cannot be determined from the clue alone. Finally, synthesize the answer, distinguishing supported structure from unresolved uncertainty.

--- CLUE FILE START ---
=CC v2.1 mattermost@HEAD 1346mod 19215sym
? According to the top-level README, what is Mattermost's core runtime and deployment profile?


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

App.hasPropertyFieldPermissionLevel (server/channels/app/authorization.go:578-578)
  hasPropertyFieldPermissionLevel checks if the user has the specified permission level for the field.
  sig: App.hasPropertyFieldPermissionLevel(rctx request.CTX, userID string, field *model.PropertyFi...)
  behavior: DISPATCH(level)
  calls: HasPermissionTo, hasPropertyFieldScopeAccess
  called_by: HasPermissionToEditPropertyField, HasPermissionToManagePropertyFieldOptions, HasPermissionToSetPropertyFieldValues, SessionHasPermissionToEditPropertyField, SessionHasPermissionToManagePropertyFieldOptions, SessionHasPermissionToSetPropertyFieldValues

Logger.IsLevelEnabled (server/public/shared/mlog/mlog.go:306-306)
  IsLevelEnabled returns true only if at least one log target is configured to emit the specified log level.
  sig: Logger.IsLevelEnabled(level Level)
  behavior: DELEGATE(l.log.IsLevelEnabled -> result)

PluginAPI.ReceiveSharedChannelProfileImageSyncMsg (server/channels/app/plugin_api.go:1525-1525)
  sig: PluginAPI.ReceiveSharedChannelProfileImageSyncMsg(remoteID, userID string, image []byte)
  behavior: DELEGATE(api.app.ReceiveSharedChannelProfileImageSyncMsg -> result)
  calls: ReceiveSharedChannelProfileImageSyncMsg

Service.sendProfileImageSyncData (server/platform/services/sharedchannel/sync_send_remote.go:964-964)
  sendProfileImageSyncData sends the collected user profile image updates to the remote cluster.
  sig: Service.sendProfileImageSyncData(sd *syncData)
  behavior: ACCUMULATE(syncProfileImage loop -> result)
  calls: syncProfileImage
  called_by: sendSyncData

processProfileImagesDir (server/cmd/mmctl/commands/sampledata.go:151-151)
  sig: processProfileImagesDir(profileImagesPath, tmpDir, bulk string)
  behavior: GUARD(os.IsNotExist(err) -> return nil, fmt.Err...); PRECEDENCE(os -> not_profileImagesStat.IsDir -> err)
  calls: Errorf
  called_by: sampledataCmdF

UserService.SanitizeProfile (server/channels/app/users/utils.go:42-42)
  sig: UserService.SanitizeProfile(user *model.User, asAdmin bool)
  calls: GetSanitizeOptions
  called_by: testExpression, getUser, getUserByEmail, getUserByUsername, verifyUserEmailWithoutToken, localGetUser, localGetUserByEmail, localGetUserByUsername

apiRPCClient.LogAuditRecWithLevel (server/public/plugin/client_rpc.go:1156-1156)
  sig: apiRPCClient.LogAuditRecWithLevel(rec *model.AuditRecord, level mlog.Level)
  calls: Error, Printf
  called_by: flagPost, getFlaggedPost, keepFlaggedPost, removeFlaggedPost, applyIPFilters, burnPost, createPost, deletePost

Client4.GetProfileImage (server/public/model/client4.go:1233-1233)
  GetProfileImage gets user's profile image.
  sig: Client4.GetProfileImage(ctx context.Context, userId, etag string)
  calls: BuildResponse, doAPIGet, userRoute, ReadBytesFromResponse, closeBody
  called_by: getProfileImage, SendNotifications, GetProfileImage, MessageWillBePosted, InviteGuestsToChannels, InviteGuestsToChannelsGracefully, InviteNewUsersToTeamGracefully

IsChannelNotifyLevelValid (server/public/model/channel_member.go:219-219)
  sig: IsChannelNotifyLevelValid(notifyLevel string)
  called_by: IsChannelMemberNotifyPropsValid

PluginAPI.GetProfileImage (server/channels/app/plugin_api.go:884-884)
  sig: PluginAPI.GetProfileImage(userID string)
  behavior: GUARD(err != nil -> return nil, err)
  calls: GetUser, GetProfileImage
  called_by: getProfileImage, SendNotifications, MessageWillBePosted, InviteGuestsToChannels, InviteGuestsToChannelsGracefully, InviteNewUsersToTeamGracefully, GetProfileImage

PluginAPI.SetProfileImage (server/channels/app/plugin_api.go:894-894)
  sig: PluginAPI.SetProfileImage(userID string, data []byte)
  behavior: GUARD(_, err := api.app.GetUser(userID); err != nil -> return err)
  calls: GetUser, SetProfileImageFromFile
  called_by: remoteSetProfileImage, setProfileImage, MessageWillBePosted, ensureBot, SetProfileImage

SqlPropertyFieldStore.checkTeamLevelConflict (server/channels/store/sqlstore/property_field_store.go:407-407)
  checkTeamLevelConflict checks if a team-level property would conflict with system properties or channel properties withi
  sig: SqlPropertyFieldStore.checkTeamLevelConflict(field *model.PropertyField, excludeID string)
  behavior: GUARD(err != nil -> return "", errors.W...); PRECEDENCE(err -> excludeID)
  calls: Get, buildConflictSubquery, GetMaster
  called_by: CheckPropertyNameConflict

UserService.GetDefaultProfileImage (server/channels/app/users/profile_picture.go:96-96)
  sig: UserService.GetDefaultProfileImage(user *model.User)
  behavior: GUARD(user.IsBot -> return botDefaultIm...)
  calls: createProfileImage
  called_by: getDefaultProfileImage, GetProfileImage, GetDefaultProfileImage, UpdateDefaultProfileImage

UserService.SetProfileImage (server/public/pluginapi/user.go:187-187)
  SetProfileImage sets a user's profile image.
  sig: UserService.SetProfileImage(userID string, content io.Reader)
  behavior: GUARD(err != nil -> return err)
  calls: SetProfileImage
  called_by: remoteSetProfileImage, setProfileImage, MessageWillBePosted, ensureBot

mockSharedChannelService.NotifyUserProfileChanged (server/channels/app/platform/shared_channel_service_iface.go:59-59)
  sig: mockSharedChannelService.NotifyUserProfileChanged(userId string)

CustomProfileAttributesSelectOption.IsValid (server/public/model/custom_profile_attributes.go:91-91)
  behavior: GUARD(c.ID == "" -> return errors.New("...); PRECEDENCE(c -> not_IsValidId)
  calls: Errorf
  called_by: updateConfig, localUpdateConfig, AddAuditLogCertificate, RemoveAuditLogCertificate, AddLdapPrivateCertificate, AddLdapPublicCertificate, RemoveLdapPrivateCertificate, RemoveLdapPublicCertificate

-- GAPS
type: STRUCTURAL (answerable from L0-L2)
coverage: 83 symbols in L3, 25 with behavior annotations
uncovered: PlatformService.getGoroutineProfile, PlatformService.getHeapProfile, PluginAPI.LogAuditRecWithLevel, ProfileImageBytes

--- CLUE FILE END ---

QUESTION: According to the top-level README, what is Mattermost's core runtime and deployment profile?

Provide a detailed answer based solely on the clue file above.
For each claim you make, cite the specific clue entry (symbol name + file location) that supports it.
