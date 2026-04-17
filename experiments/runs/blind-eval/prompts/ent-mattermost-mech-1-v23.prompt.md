# Blind Evaluation Prompt - MRLF v2.4 with File 2 Drill-Down
# Task: ent-mattermost-mech-1

You are a senior software engineer. You have been given:
1. A codebase comprehension artifact (clue file) - a compressed representation
2. Source code snippets for key functions identified as needing deeper analysis

Answer the question using the clue file AND the source snippets below.
Do not use any external knowledge about the framework or library.

**Reasoning scaffold:** Think through the clue systematically before answering. First, identify the symbols most relevant to the question from FOCUS, SYM, and INDEX. Trace those symbols through the clue before forming any conclusion: follow calls: chains, walk extends: hierarchies, and read behavior: annotations as compact control-flow summaries. Use TREE and INDEX to place each symbol in its module context. Then consult the provided source snippets only to confirm or refine the traced path. State explicitly what GAPS says cannot be determined from the evidence. Finally, synthesize the answer, separating supported conclusions from remaining uncertainty.

--- CLUE FILE (File 1) ---
=CC v2.1 mattermost@HEAD 1346mod 19215sym
? How does incoming webhook administration work across team, channel, and system scopes?


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

SqlWebhookStore.GetIncomingByTeam (server/channels/store/sqlstore/webhook_store.go:205-205)
  sig: SqlWebhookStore.GetIncomingByTeam(teamId string, offset, limit int)
  behavior: DELEGATE(s.GetIncomingByTeamByUser -> result)
  calls: GetIncomingByTeamByUser

App.CreateIncomingWebhookForChannel (server/channels/app/webhook.go:390-390)
  sig: App.CreateIncomingWebhookForChannel(creatorId string, channel *model.Channel, hook *model.In...)
  behavior: GUARD(!*a.Config().ServiceSettings.EnableIncomingWe... -> return nil, model....); PRECEDENCE(not_a.Config)
  calls: Srv, Config
  called_by: createIncomingHook, localCreateIncomingHook

TimerLayerWebhookStore.PermanentDeleteIncomingByChannel (server/channels/store/timerlayer/timerlayer.go:14228-14228)
  sig: TimerLayerWebhookStore.PermanentDeleteIncomingByChannel(channelID string)

LocalCacheWebhookStore.PermanentDeleteIncomingByChannel (server/channels/store/localcachelayer/webhook_layer.go:81-81)
  sig: LocalCacheWebhookStore.PermanentDeleteIncomingByChannel(channelId string)
  behavior: GUARD(err != nil -> return err)
  calls: ClearCaches

RetryLayerWebhookStore.GetIncomingByChannel (server/channels/store/retrylayer/retrylayer.go:17727-17727)
  sig: RetryLayerWebhookStore.GetIncomingByChannel(channelID string)
  calls: isRepeatableError

RetryLayerWebhookStore.GetIncomingByTeam (server/channels/store/retrylayer/retrylayer.go:17748-17748)
  sig: RetryLayerWebhookStore.GetIncomingByTeam(teamID string, offset int, limit int)
  calls: isRepeatableError

RetryLayerWebhookStore.GetIncomingByTeamByUser (server/channels/store/retrylayer/retrylayer.go:17769-17769)
  sig: RetryLayerWebhookStore.GetIncomingByTeamByUser(teamID string, userID string, offset int, limit int)
  calls: isRepeatableError
  called_by: GetIncomingByTeam

RetryLayerWebhookStore.PermanentDeleteIncomingByChannel (server/channels/store/retrylayer/retrylayer.go:17985-17985)
  sig: RetryLayerWebhookStore.PermanentDeleteIncomingByChannel(channelID string)
  calls: isRepeatableError

SqlWebhookStore.GetIncomingByChannel (server/channels/store/sqlstore/webhook_store.go:209-209)
  sig: SqlWebhookStore.GetIncomingByChannel(channelId string)
  behavior: GUARD(err := s.GetReplica().SelectBuilder(&webhooks... -> return nil, errors...)
  calls: GetReplica

SqlWebhookStore.GetIncomingByTeamByUser (server/channels/store/sqlstore/webhook_store.go:183-183)
  sig: SqlWebhookStore.GetIncomingByTeamByUser(teamId string, userId string, offset, limit int)
  behavior: PRECEDENCE(userId -> err)
  calls: GetReplica
  called_by: GetIncomingByTeam

SqlWebhookStore.PermanentDeleteIncomingByChannel (server/channels/store/sqlstore/webhook_store.go:151-151)
  sig: SqlWebhookStore.PermanentDeleteIncomingByChannel(channelId string)
  behavior: GUARD(err != nil -> return errors.Wrapf...)
  calls: GetMaster

TestWebhookStoreGetIncomingByTeamByUser (server/channels/store/storetest/webhook_store.go:168-168)
  sig: TestWebhookStoreGetIncomingByTeamByUser(t *testing.T, rctx request.CTX, ss store.Store)
  calls: Run, Webhook, buildIncomingWebhook
  called_by: TestWebhookStore

TimerLayerWebhookStore.GetIncomingByChannel (server/channels/store/timerlayer/timerlayer.go:14021-14021)
  sig: TimerLayerWebhookStore.GetIncomingByChannel(channelID string)

TimerLayerWebhookStore.GetIncomingByTeam (server/channels/store/timerlayer/timerlayer.go:14037-14037)
  sig: TimerLayerWebhookStore.GetIncomingByTeam(teamID string, offset int, limit int)

TimerLayerWebhookStore.GetIncomingByTeamByUser (server/channels/store/timerlayer/timerlayer.go:14053-14053)
  sig: TimerLayerWebhookStore.GetIncomingByTeamByUser(teamID string, userID string, offset int, limit int)
  called_by: GetIncomingByTeam

testWebhookStoreDeleteIncomingByChannel (server/channels/store/storetest/webhook_store.go:233-233)
  sig: testWebhookStoreDeleteIncomingByChannel(t *testing.T, rctx request.CTX, ss store.Store)
  calls: Webhook, buildIncomingWebhook
  called_by: TestWebhookStore

testWebhookStoreGetIncomingByChannel (server/channels/store/storetest/webhook_store.go:200-200)
  sig: testWebhookStoreGetIncomingByChannel(t *testing.T, rctx request.CTX, ss store.Store)
  calls: Webhook, buildIncomingWebhook
  called_by: TestWebhookStore

testWebhookStoreGetIncomingByTeam (server/channels/store/storetest/webhook_store.go:152-152)
  sig: testWebhookStoreGetIncomingByTeam(t *testing.T, rctx request.CTX, ss store.Store)
  calls: Webhook, buildIncomingWebhook
  called_by: TestWebhookStore

Client4.CreateIncomingWebhook (server/public/model/client4.go:4540-4540)
  CreateIncomingWebhook creates an incoming webhook for a channel.
  sig: Client4.CreateIncomingWebhook(ctx context.Context, hook *IncomingWebhook)
  calls: BuildResponse, doAPIPostJSON, incomingWebhooksRoute, closeBody
  called_by: createIncomingWebhookCmdF

Client4.UpdateIncomingWebhook (server/public/model/client4.go:4550-4550)
  UpdateIncomingWebhook updates an incoming webhook for a channel.
  sig: Client4.UpdateIncomingWebhook(ctx context.Context, hook *IncomingWebhook)
  calls: BuildResponse, doAPIPutJSON, incomingWebhookRoute, closeBody
  called_by: updateIncomingHook, modifyIncomingWebhookCmdF

Client4.CreateOutgoingWebhook (server/public/model/client4.go:4621-4621)
  CreateOutgoingWebhook creates an outgoing webhook for a team or channel.
  sig: Client4.CreateOutgoingWebhook(ctx context.Context, hook *OutgoingWebhook)
  calls: BuildResponse, doAPIPostJSON, outgoingWebhooksRoute, closeBody
  called_by: createOutgoingHook, localCreateOutgoingHook, createOutgoingWebhookCmdF

SqlPropertyFieldStore.checkTeamLevelConflict (server/channels/store/sqlstore/property_field_store.go:407-407)
  checkTeamLevelConflict checks if a team-level property would conflict with system properties or channel properties withi
  sig: SqlPropertyFieldStore.checkTeamLevelConflict(field *model.PropertyField, excludeID string)
  behavior: GUARD(err != nil -> return "", errors.W...); PRECEDENCE(err -> excludeID)
  calls: Get, buildConflictSubquery, GetMaster
  called_by: CheckPropertyNameConflict

-- GAPS
type: MECHANISTIC (body logic needed for full answer)
coverage: 83 symbols in L3, 36 with behavior annotations
uncovered: ChannelStore.GetChannelsWithTeamDataByIds, ChannelStore.GetPublicChannelsByIdsForTeam, ChannelStore.GetTeamForChannel, ChannelStore.GetTeamMembersForChannel
drill: server/channels/store/sqlstore/webhook_store.go (~1 lines, SqlWebhookStore.GetIncomingByTeam)

--- END CLUE FILE ---

--- SOURCE SNIPPETS (File 2 Drill-Down) ---
## SqlWebhookStore.GetIncomingByTeam  (server/channels/store/sqlstore/webhook_store.go L205-205)
```
func (s SqlWebhookStore) GetIncomingByTeam(teamId string, offset, limit int) ([]*model.IncomingWebhook, error) {
```

## SqlWebhookStore.AnalyticsIncomingCount  (server/channels/store/sqlstore/webhook_store.go L390-390)
```
func (s SqlWebhookStore) AnalyticsIncomingCount(teamID string, userID string) (int64, error) {
```

## SqlWebhookStore.AnalyticsOutgoingCount  (server/channels/store/sqlstore/webhook_store.go L412-412)
```
func (s SqlWebhookStore) AnalyticsOutgoingCount(teamId string) (int64, error) {
```

## SqlWebhookStore.ClearCaches  (server/channels/store/sqlstore/webhook_store.go L25-25)
```
func (s SqlWebhookStore) ClearCaches() {
```

## SqlWebhookStore.DeleteIncoming  (server/channels/store/sqlstore/webhook_store.go L133-133)
```
func (s SqlWebhookStore) DeleteIncoming(webhookId string, time int64) error {
```

## SqlWebhookStore.DeleteOutgoing  (server/channels/store/sqlstore/webhook_store.go L346-346)
```
func (s SqlWebhookStore) DeleteOutgoing(webhookId string, time int64) error {
```

## SqlWebhookStore.GetIncoming  (server/channels/store/sqlstore/webhook_store.go L114-114)
```
func (s SqlWebhookStore) GetIncoming(id string, allowFromCache bool) (*model.IncomingWebhook, error) {
```

## SqlWebhookStore.GetIncomingByChannel  (server/channels/store/sqlstore/webhook_store.go L209-209)
```
func (s SqlWebhookStore) GetIncomingByChannel(channelId string) ([]*model.IncomingWebhook, error) {
```

## SqlWebhookStore.GetIncomingByTeamByUser  (server/channels/store/sqlstore/webhook_store.go L183-183)
```
func (s SqlWebhookStore) GetIncomingByTeamByUser(teamId string, userId string, offset, limit int) ([]*model.IncomingWebhook, error) {
```

## SqlWebhookStore.GetIncomingList  (server/channels/store/sqlstore/webhook_store.go L160-160)
```
func (s SqlWebhookStore) GetIncomingList(offset, limit int) ([]*model.IncomingWebhook, error) {
```

## SqlWebhookStore.GetIncomingListByUser  (server/channels/store/sqlstore/webhook_store.go L164-164)
```
func (s SqlWebhookStore) GetIncomingListByUser(userId string, offset, limit int) ([]*model.IncomingWebhook, error) {
```

## SqlWebhookStore.GetOutgoing  (server/channels/store/sqlstore/webhook_store.go L247-247)
```
func (s SqlWebhookStore) GetOutgoing(id string) (*model.OutgoingWebhook, error) {
```

## SqlWebhookStore.GetOutgoingByChannel  (server/channels/store/sqlstore/webhook_store.go L315-315)
```
func (s SqlWebhookStore) GetOutgoingByChannel(channelId string, offset, limit int) ([]*model.OutgoingWebhook, error) {
```

## SqlWebhookStore.GetOutgoingByChannelByUser  (server/channels/store/sqlstore/webhook_store.go L292-292)
```
func (s SqlWebhookStore) GetOutgoingByChannelByUser(channelId string, userId string, offset, limit int) ([]*model.OutgoingWebhook, error) {
```

## SqlWebhookStore.GetOutgoingByTeam  (server/channels/store/sqlstore/webhook_store.go L342-342)
```
func (s SqlWebhookStore) GetOutgoingByTeam(teamId string, offset, limit int) ([]*model.OutgoingWebhook, error) {
```

## SqlWebhookStore.GetOutgoingByTeamByUser  (server/channels/store/sqlstore/webhook_store.go L319-319)
```
func (s SqlWebhookStore) GetOutgoingByTeamByUser(teamId string, userId string, offset, limit int) ([]*model.OutgoingWebhook, error) {
```

## SqlWebhookStore.GetOutgoingList  (server/channels/store/sqlstore/webhook_store.go L288-288)
```
func (s SqlWebhookStore) GetOutgoingList(offset, limit int) ([]*model.OutgoingWebhook, error) {
```

## SqlWebhookStore.GetOutgoingListByUser  (server/channels/store/sqlstore/webhook_store.go L267-267)
```
func (s SqlWebhookStore) GetOutgoingListByUser(userId string, offset, limit int) ([]*model.OutgoingWebhook, error) {
```

## SqlWebhookStore.InvalidateWebhookCache  (server/channels/store/sqlstore/webhook_store.go L77-77)
```
func (s SqlWebhookStore) InvalidateWebhookCache(webhookId string) {
```

## SqlWebhookStore.PermanentDeleteIncomingByChannel  (server/channels/store/sqlstore/webhook_store.go L151-151)
```
func (s SqlWebhookStore) PermanentDeleteIncomingByChannel(channelId string) error {
```

## SqlWebhookStore.PermanentDeleteIncomingByUser  (server/channels/store/sqlstore/webhook_store.go L142-142)
```
func (s SqlWebhookStore) PermanentDeleteIncomingByUser(userId string) error {
```

## SqlWebhookStore.PermanentDeleteOutgoingByChannel  (server/channels/store/sqlstore/webhook_store.go L364-364)
```
func (s SqlWebhookStore) PermanentDeleteOutgoingByChannel(channelId string) error {
```

## SqlWebhookStore.PermanentDeleteOutgoingByUser  (server/channels/store/sqlstore/webhook_store.go L355-355)
```
func (s SqlWebhookStore) PermanentDeleteOutgoingByUser(userId string) error {
```

## SqlWebhookStore.SaveIncoming  (server/channels/store/sqlstore/webhook_store.go L80-80)
```
func (s SqlWebhookStore) SaveIncoming(webhook *model.IncomingWebhook) (*model.IncomingWebhook, error) {
```

## SqlWebhookStore.SaveOutgoing  (server/channels/store/sqlstore/webhook_store.go L225-225)
```
func (s SqlWebhookStore) SaveOutgoing(webhook *model.OutgoingWebhook) (*model.OutgoingWebhook, error) {
```

## SqlWebhookStore.UpdateIncoming  (server/channels/store/sqlstore/webhook_store.go L100-100)
```
func (s SqlWebhookStore) UpdateIncoming(hook *model.IncomingWebhook) (*model.IncomingWebhook, error) {
```

## SqlWebhookStore.UpdateOutgoing  (server/channels/store/sqlstore/webhook_store.go L375-375)
```
func (s SqlWebhookStore) UpdateOutgoing(hook *model.OutgoingWebhook) (*model.OutgoingWebhook, error) {
```

## SqlWebhookStore  (server/channels/store/sqlstore/webhook_store.go L17-17)
```
type SqlWebhookStore struct {
```

## newSqlWebhookStore  (server/channels/store/sqlstore/webhook_store.go L28-28)
```
func newSqlWebhookStore(sqlStore *SqlStore, metrics einterfaces.MetricsInterface) store.WebhookStore {
```
--- END SOURCE SNIPPETS ---

QUESTION: How does incoming webhook administration work across team, channel, and system scopes?

Provide a detailed answer based on the clue file and source snippets above.
For each claim you make, cite the specific clue entry or source snippet that supports it.
