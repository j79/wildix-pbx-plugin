# Rapport des écarts — référentiel API Wildix

Révision du 2026-11-10, comparée à la révision du 2026-10-18 (V2).

## Synthèse

- **930 routes publiées** dans 50 services (V2 : 35 services).
- **224 routes nouvelles**, dont 15 nouveaux services : x-caracal (WDA) et 14 services Wilma (`api.wilma.wildix.com`).
- **21 routes de nouveau publiées** (PBX API, dont tout le bloc `/call-control/*`).
- **3 routes retirées** de la documentation depuis le 18/10 ; avec les routes déjà retirées en octobre, **8 routes deprecated sont conservées**, avec leur description d'origine et leur date de retrait.
- **Aucune route supprimée** : vérification automatique faite, chaque route de la V2 figure dans la V3 (publiée ou deprecated).
- **159 routes existantes modifiées** dans leur structure (paramètres, champs, codes d'erreur).
- **22 routes publiées mais marquées `deprecated`** par Wildix.

## Détail par service

### PBX API

- **De nouveau publiées** : `DELETE /api/v2/call-groups/{id}/members/dynamic/{member}`, `GET /api/v2/personal/features`, `GET /api/v2/personal/features/`, `GET /call-control/list-calls/`, `GET /call-control/list-devices/`, `POST /api/v2/call-groups/{id}/forward/`, `POST /api/v2/call-groups/{id}/members/dynamic/`, `POST /api/v2/personal/features`, `POST /api/v2/personal/features/`, `POST /broadcasts/reload/`, `POST /call-control/answer/`, `POST /call-control/attendant-transfer/`, `POST /call-control/blind-transfer/`, `POST /call-control/dtmf/`, `POST /call-control/hangup/`, `POST /call-control/hold/`, `POST /call-control/make-call/`, `POST /call-control/unhold/`, `POST /call-control/update-contact-info/`, `PUT /PBX/settings/`, `PUT /call-control/set-active-device/`
- **Routes modifiées (55)** :
  - `DELETE /Phonebooks/{phonebookID}/Contacts/{contactId}/` — codes d'erreur : `401` → `401`, `403`
  - `DELETE /Sounds/{path}/` — codes d'erreur : `400`, `401` → `400`, `401`, `403`
  - `GET /CallHistory/` — paramètre(s) retiré(s) : `count`, `dir`, `fields`, `filter`, `search`, `searchFields`, `sort`, `start`
  - `GET /CallHistory/{callId}` — paramètre(s) retiré(s) : `fields`
  - `GET /Colleagues/` — codes d'erreur : `400`, `401` → `400`, `401`, `403`
  - `GET /Colleagues/{id}/` — codes d'erreur : `401`, `404` → `401`, `403`, `404`
  - `GET /Contacts/` — codes d'erreur : `401`, `500` → `401`, `403`, `500`
  - `GET /Devices/` — codes d'erreur : `401` → `401`, `403`
  - `GET /Devices/verify/` — codes d'erreur : `400`, `401` → `400`, `401`, `403`
  - `GET /Dialplan/GeneralSettings/` — champ(s) ajouté(s) : `personalRecordType`
  - `GET /PBX/AclGroups/Permissions/` — codes d'erreur : `401`, `500` → `401`, `403`, `500`
  - `GET /PBX/AclGroups/Rules/` — codes d'erreur : `401`, `500` → `401`, `403`, `500`
  - `GET /PBX/CallHistory/` — paramètre(s) retiré(s) : `count`, `dir`, `fields`, `filter`, `search`, `searchFields`, `sort`, `start`
  - `GET /PBX/Ports/Status/` — codes d'erreur : `401`, `500` → `401`, `403`, `500`
  - `GET /PBX/candidates` — codes d'erreur : `401`, `500` → `401`, `403`, `500`
  - `GET /PBX/recordings/download/{id}` — codes d'erreur : `401` → `401`, `403`
  - `GET /PBX/settings/` — champ(s) ajouté(s) : `allowCustomTags`, `available`, `database`, `error`, `features`, `hint`, `isServerManagement`, `label`, `message`, `partnerLogo`, `user` ; codes d'erreur : `401` → `401`, `403`
  - `GET /PBX/settings/license/` — champ(s) retiré(s) : `wizyWebinar`
  - `GET /PBX/version/` — codes d'erreur : `401` → `401`, `403`
  - `GET /Phonebooks/` — codes d'erreur : `401`, `500` → `401`, `403`, `500`
  - `GET /Phonebooks/{id}/` — codes d'erreur : `401`, `500` → `401`, `403`, `500`
  - `GET /Phonebooks/{phonebookID}/Contacts/` — codes d'erreur : `401`, `500` → `401`, `403`, `500`
  - `GET /Phonebooks/{phonebookID}/Contacts/{contactId}` — codes d'erreur : `401`, `500` → `401`, `403`, `500`
  - `GET /Sounds/{path}/` — codes d'erreur : — → `403`
  - `GET /Trunks/Sip/` — champ(s) ajouté(s) : `kernelLevelMedia`
  - `GET /User/{extension}/CallHistory/` — paramètre(s) retiré(s) : `count`, `dir`, `fields`, `filter`, `search`, `searchFields`, `sort`, `start`
  - `POST /Contacts` — codes d'erreur : `401`, `500` → `401`, `403`, `500`
  - `POST /Device/ResetToken/` — codes d'erreur : `401`, `404`, `500` → `401`, `403`, `404`, `500`
  - `POST /Devices/` — codes d'erreur : `400`, `401` → `400`, `401`, `403`
  - `POST /Devices/scan/` — codes d'erreur : `400`, `401` → `400`, `401`, `403`
  - `POST /Dialplan/CallGroups/` — champ(s) retiré(s) : `announce`, `autoPause`, `autoPauseDelay`, `autoPauseTime`, `busy`, `cid`, `exitAllMembers`, `frequency`, `holdTime`, `maxLen`, `members`, `paused` …
  - `POST /Dialplan/DB/{family}/{key}+/` — champ(s) retiré(s) : `value`
  - `POST /Dialplan/Ivr/` — champ(s) retiré(s) : `backcode`, `context`, `exten`, `id`, `items`, `number`, `parameters`, `sound`, `timeout`, `times`, `title`
  - `POST /PBX/recordings/download/` — codes d'erreur : `401` → `401`, `403`
  - `POST /Phonebooks` — champ(s) retiré(s) : `data` ; codes d'erreur : `401`, `500` → `401`, `403`, `500`
  - `POST /Phonebooks/{phonebookID}/Contacts` — codes d'erreur : `401`, `500` → `401`, `403`, `500`
  - `POST /Trunks/Groups/` — champ(s) retiré(s) : `description`, `maxCalls`, `name`, `prepend`, `remove`, `rules`, `timeout`, `trunkName`
  - `POST /Trunks/Prices/` — champ(s) retiré(s) : `upload`
  - `POST /Trunks/Prices/{ID}/` — champ(s) retiré(s) : `upload`
  - `POST /Trunks/Sip/` — champ(s) ajouté(s) : `kernelLevelMedia`
  - `POST /notifications/` — champ(s) ajouté(s) : `broadcastId`, `extension`, `skills`, `skipTranscribe` ; champ(s) retiré(s) : `conferenceId`
  - `POST /videoConference/Rooms/` — type ou caractère obligatoire de champ(s) modifié(s)
  - `PUT /Dialplan/CallGroups/{id}/` — champ(s) retiré(s) : `announce`, `autoPause`, `autoPauseDelay`, `autoPauseTime`, `busy`, `cid`, `exitAllMembers`, `frequency`, `holdTime`, `maxLen`, `members`, `paused` …
  - `PUT /Dialplan/DB/{family}/{keys}+/` — champ(s) retiré(s) : `value`
  - `PUT /Dialplan/GeneralSettings/` — champ(s) ajouté(s) : `personalRecordType`
  - `PUT /Dialplan/Ivr/{id}/` — champ(s) retiré(s) : `backcode`, `context`, `exten`, `id`, `items`, `number`, `parameters`, `sound`, `timeout`, `times`, `title`
  - `PUT /PBX/Colleagues/{id}/` — paramètre(s) ajouté(s) : `transferRnaChats`
  - `PUT /PBX/Colleagues/{id}/preferences/` — codes d'erreur : `401`, `404` → `401`, `403`, `404`
  - `PUT /Phonebooks/{id}` — champ(s) retiré(s) : `data`
  - `PUT /Sounds/directory/` — champ(s) retiré(s) : `move`, `name`
  - `PUT /Sounds/{path}/` — champ(s) retiré(s) : `move`, `name` ; codes d'erreur : `400`, `401` → `400`, `401`, `403`
  - `PUT /Trunks/Groups/{id}` — champ(s) retiré(s) : `description`, `maxCalls`, `name`, `prepend`, `remove`, `rules`, `timeout`, `trunkName`
  - `PUT /Trunks/Sip/{id}` — champ(s) ajouté(s) : `kernelLevelMedia`
  - `PUT /phonebooks/{phonebookID}/Contacts/{contactId}` — codes d'erreur : `401`, `500` → `401`, `403`, `500`
  - `PUT /videoConference/Rooms/` — champ(s) retiré(s) : `country`, `description`, `dialInNumbers`, `email`, `enabled`, `end`, `jid`, `lang`, `name`, `participants`, `password`, `recurrence` …

### Cloud PBX API (Permissions)

- **Nouvelles routes** : `POST /v1/permissions/delete_call_recordings_of_users/check`

### Cloud PBX Server API

- **Routes modifiées (1)** :
  - `GET /api/v1/Departments/` — structure modifiée (réponse ou corps)

### Conversations API

- **Marquées `deprecated` par Wildix** : `POST /v2/conversations/invite`
- **Routes modifiées (24)** :
  - `GET /v2/conversations/channels/` — champ(s) ajouté(s) : `autoTranscribe`
  - `GET /v2/conversations/channels/{channelId}` — champ(s) ajouté(s) : `autoTranscribe`
  - `GET /v2/conversations/channels/{channelId}/messages` — champ(s) ajouté(s) : `wilma`
  - `GET /v2/conversations/channels/{channelId}/messages/{messageId}` — champ(s) ajouté(s) : `artifacts`, `endIndex`, `sessionId`, `startIndex`, `summary`, `turn`, `verbosity`, `wilma`
  - `GET /v2/conversations/channels/{channelId}/pinned_messages` — champ(s) ajouté(s) : `wilma`
  - `PATCH /v2/conversations/channels/{channelId}` — champ(s) ajouté(s) : `autoTranscribe`
  - `PATCH /v2/conversations/channels/{channelId}/messages/{messageId}` — champ(s) ajouté(s) : `artifacts`, `endIndex`, `sessionId`, `startIndex`, `summary`, `turn`, `verbosity`, `wilma`
  - `POST /v2/conversations/channels/{channelId}/join` — champ(s) ajouté(s) : `autoTranscribe`
  - `POST /v2/conversations/channels/{channelId}/messages` — champ(s) ajouté(s) : `artifacts`, `durationMs`, `endIndex`, `failedCount`, `outcome`, `sessionId`, `startIndex`, `summary`, `toolCount`, `turn`, `verbosity`, `wilma`
  - `POST /v2/conversations/channels/{channelId}/send_giphy` — champ(s) ajouté(s) : `artifacts`, `endIndex`, `sessionId`, `startIndex`, `summary`, `turn`, `verbosity`, `wilma`
  - `POST /v2/conversations/channels/{channelId}/system-messages` — champ(s) ajouté(s) : `artifacts`, `endIndex`, `sessionId`, `startIndex`, `summary`, `turn`, `verbosity`, `wilma`
  - `POST /v2/conversations/describe` — champ(s) ajouté(s) : `autoTranscribe`
  - `POST /v2/conversations/direct/get_or_create_channel` — champ(s) ajouté(s) : `autoTranscribe`
  - `POST /v2/conversations/group` — champ(s) ajouté(s) : `autoTranscribe`
  - `POST /v2/conversations/invite` — champ(s) retiré(s) : `bot`, `createdAt`, `pbxDomain`, `pbxExtension`, `pbxGroupId`, `pbxPort`, `pbxSerial`, `timeZone`, `updatedAt`
  - `POST /v2/conversations/kite` — champ(s) ajouté(s) : `artifacts`, `autoTranscribe`, `endIndex`, `sessionId`, `startIndex`, `turn`, `verbosity`, `wilma`
  - `POST /v2/conversations/messaging/get_channel_id` — champ(s) ajouté(s) : `senderId`
  - `POST /v2/conversations/messaging/get_or_create_channel` — champ(s) ajouté(s) : `autoTranscribe`, `senderId`
  - `POST /v2/conversations/query-channels` — champ(s) ajouté(s) : `autoTranscribe`
  - `POST /v2/conversations/sms/get_or_create_channel` — champ(s) ajouté(s) : `autoTranscribe`
  - `POST /v2/conversations/telephony/get_or_create_channel` — champ(s) ajouté(s) : `autoTranscribe`
  - `POST /v2/conversations/whatsapp/get_or_create_channel` — champ(s) ajouté(s) : `autoTranscribe`
  - `PUT /v2/conversations/channels/{channelId}` — champ(s) ajouté(s) : `autoTranscribe`
  - `PUT /v2/conversations/channels/{channelId}/messages/{messageId}` — champ(s) ajouté(s) : `artifacts`, `durationMs`, `endIndex`, `failedCount`, `outcome`, `sessionId`, `startIndex`, `summary`, `toolCount`, `turn`, `verbosity`, `wilma`

### Kite API

- **Routes modifiées (6)** :
  - `DELETE /v2/kite/calendar/channels/{channelId}/events/{eventOwner}/{eventId}` — champ(s) ajouté(s) : `autoTranscribe`
  - `PATCH /v2/kite/calendar/channels/{channelId}/events/{eventOwner}/{eventId}` — champ(s) ajouté(s) : `autoTranscribe`
  - `POST /v2/kite/calendar/widgets/{targetId}` — champ(s) ajouté(s) : `autoTranscribe`
  - `POST /v2/kite/widgets` — champ(s) ajouté(s) : `wilma`
  - `POST /v2/kite/widgets/preview` — champ(s) ajouté(s) : `wilma`
  - `PUT /v2/kite/widgets/{widgetId}` — champ(s) ajouté(s) : `wilma`

### Users & ChatBots API

- **Marquées `deprecated` par Wildix** : `POST /v2/users/UploadPicture`
- **Routes modifiées (45)** :
  - `DELETE /v2/users/accounts/{accountId}/identities/{identity}` — codes d'erreur : `400`, `403`, `404` → `400`, `403`, `404`, `429`
  - `DELETE /v2/users/accounts/{accountId}/workspaces/{workspaceId}` — codes d'erreur : `400`, `403`, `404` → `400`, `403`, `404`, `429`
  - `DELETE /v2/users/bots/{botId}` — codes d'erreur : `400`, `403`, `404` → `400`, `403`, `404`, `429`
  - `DELETE /v2/users/bots/{botId}/keys/{apiKeySecret}` — codes d'erreur : `400`, `403`, `404` → `400`, `403`, `404`, `429`
  - `GET /v2/users/GetUserPbxLinkSuggestion` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `GET /v2/users/accounts/{accountId}` — codes d'erreur : `400`, `403`, `404` → `400`, `403`, `404`, `429`
  - `GET /v2/users/accounts/{accountId}/identities` — codes d'erreur : `400`, `403`, `404` → `400`, `403`, `404`, `429`
  - `GET /v2/users/accounts/{accountId}/workspaces` — paramètre(s) ajouté(s) : `limit`, `offset`, `query` ; champ(s) ajouté(s) : `total` ; codes d'erreur : `400`, `403`, `404` → `400`, `403`, `404`, `429`
  - `GET /v2/users/app-version` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `GET /v2/users/bots` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `GET /v2/users/bots/{botId}` — codes d'erreur : `400`, `403`, `404` → `400`, `403`, `404`, `429`
  - `GET /v2/users/bots/{botId}/callback` — codes d'erreur : `400`, `403`, `404` → `400`, `403`, `404`, `429`
  - `GET /v2/users/bots/{botId}/keys` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `GET /v2/users/cloud/{userId}` — codes d'erreur : `400`, `403`, `404` → `400`, `403`, `404`, `429`
  - `GET /v2/users/cloud/{userId}/notifications/email` — codes d'erreur : `400`, `403`, `404` → `400`, `403`, `404`, `429`
  - `GET /v2/users/cloud/{userId}/pbx-link-data` — codes d'erreur : `400`, `403`, `404` → `400`, `403`, `404`, `429`
  - `GET /v2/users/get-user-pbx-link-suggestion` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `GET /v2/users/intelligence-search` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `PATCH /v2/users/cloud/{userId}/notifications/email` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `POST /v2/users/BatchGetUsersPbxLinkData` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `POST /v2/users/UploadPicture` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `POST /v2/users/accounts/{accountId}/identities` — codes d'erreur : `400`, `403`, `404` → `400`, `403`, `404`, `429`
  - `POST /v2/users/accounts/{accountId}/identities/verify` — codes d'erreur : `400`, `403`, `404` → `400`, `403`, `404`, `429`
  - `POST /v2/users/auth/VerifyBotSecretKey` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `POST /v2/users/batch-get-users` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `POST /v2/users/batch-get-users-email-notifications-settings` — champ(s) ajouté(s) : `transcription`, `unread` ; codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `POST /v2/users/batch-get-users-pbx-link-data` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `POST /v2/users/bots` — codes d'erreur : `400`, `403`, `409` → `400`, `403`, `409`, `429`
  - `POST /v2/users/bots/{botId}/keys` — codes d'erreur : `400`, `403`, `404` → `400`, `403`, `404`, `429`
  - `POST /v2/users/cloud/{userId}/notifications/email` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `POST /v2/users/create-anonymous-session` — codes d'erreur : `400`, `403`, `404` → `400`, `403`, `404`, `429`
  - `POST /v2/users/invite` — champ(s) retiré(s) : `bot`, `createdAt`, `pbxDomain`, `pbxExtension`, `pbxGroupId`, `pbxPort`, `pbxSerial`, `timeZone`, `updatedAt` ; codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `POST /v2/users/query-colleagues` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `POST /v2/users/query-user` — paramètre(s) ajouté(s) : `company` ; codes d'erreur : `400`, `403`, `404` → `400`, `403`, `404`, `429`
  - `POST /v2/users/query-users` — paramètre(s) ajouté(s) : `company` ; codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `POST /v2/users/system-bots` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `POST /v2/users/toggle-transcription-email-notifications-subscription` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `POST /v2/users/toggle-unread-email-notifications-subscription` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `POST /v2/users/upload-picture` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `POST /v2/users/verify-bot-secret-key` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `PUT /v2/users/accounts/{accountId}` — codes d'erreur : `400`, `403`, `404` → `400`, `403`, `404`, `429`
  - `PUT /v2/users/accounts/{accountId}/workspaces/{workspaceId}` — codes d'erreur : `400`, `403`, `404` → `400`, `403`, `404`, `429`
  - `PUT /v2/users/bots/{botId}` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `PUT /v2/users/bots/{botId}/callback` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `PUT /v2/users/change-email` — codes d'erreur : `400`, `403`, `404` → `400`, `403`, `404`, `429`

### Integrations API

- **Marquées `deprecated` par Wildix** : `DELETE /v2/integrations/companies/{companyId}/integrations/{integrationId}`, `GET /v2/integrations/by-companys-and-services`, `GET /v2/integrations/by-id/{integrationId}`, `GET /v2/integrations/companies`, `GET /v2/integrations/companies/{companyId}`, `GET /v2/integrations/services`, `GET /v2/integrations/services/{service}`, `PATCH /v2/integrations/companies/{companyId}/integrations/{integrationId}`, `POST /v2/integrations/bulk/delete`, `PUT /v2/integrations/bulk/put`, `PUT /v2/integrations/companies/{companyId}`

### Cache API

- **Routes modifiées (1)** :
  - `GET /v1/cache/search` — paramètre(s) ajouté(s) : `company`, `userId`

### WNS Email API

- **Marquées `deprecated` par Wildix** : `POST /api/v2/mail/admin`

### WMP Info API

- **Nouvelles routes** : `GET /v2/PBXs/{domain}`, `GET /v2/companies/{companyId}`
- **Retirées le 2026-11-10 (conservées en deprecated)** : `GET /v1/companies/{companyId}`, `GET /v1/pbxs/{nameOrSerial}`, `POST /v1/pbx-key/check`

### STT Service

- **Retirées le 2026-10-18 (toujours conservées en deprecated)** : `POST /api/v1/Common`, `POST /api/v1/Voicemail`

### TTS Service

- **Retirées le 2026-10-18 (toujours conservées en deprecated)** : `GET /api/v2/Settings`, `POST /api/v2/Audio`

### URL-Preview Service

- **Retirées le 2026-10-18 (toujours conservées en deprecated)** : `POST /api/v2/Url/`

### Classound API

- **Nouvelles routes** : `GET /v1/s2s/rcs/brands`, `POST /v1/s2s/rcs/send`

### History API

- **Routes modifiées (6)** :
  - `GET /v2/history/calls/{callId}/flows/{flowIndex}` — champ(s) ajouté(s) : `key`, `metric`, `payload`, `result`, `source`, `tag`, `text`, `variables`
  - `GET /v2/history/chats/{chatId}` — champ(s) ajouté(s) : `autoTranscribe`, `key`, `metric`, `payload`, `result`, `tag`, `text`, `variables`
  - `GET /v2/history/chats/{chatId}/transcription/text` — champ(s) ajouté(s) : `wilma`
  - `GET /v2/history/conferences/{conferenceId}` — champ(s) ajouté(s) : `key`, `metric`, `payload`, `result`, `source`, `tag`, `text`, `variables`
  - `POST /v2/history/user/calls` — champ(s) ajouté(s) : `key`, `payload`, `source`
  - `PUT /v2/history/calls/{callId}/flows/{flowIndex}` — champ(s) ajouté(s) : `key`, `metric`, `payload`, `result`, `source`, `tag`, `text`, `variables`

### Insights API

- **Nouvelles routes** : `DELETE /v2/insights/calls/{callId}/assets`, `DELETE /v2/insights/conferences/{conferenceId}/assets`
- **Marquées `deprecated` par Wildix** : `DELETE /v2/insights/projections-categories/{id}`, `POST /v2/insights/calls/{callId}/flows/{flowIndex}/schedule_summary_generation`, `POST /v2/insights/conferences/{conferenceId}/schedule_summary_generation`, `POST /v2/insights/conversations/insights`, `POST /v2/insights/conversations/insights/aggregations`, `POST /v2/insights/projections-categories`, `PUT /v2/insights/projections-categories/{id}`
- **Routes modifiées (11)** :
  - `GET /v2/insights/calls/{callId}/flows/{flowIndex}/characteristics` — codes d'erreur : `400`, `403` → `400`, `403`, `404`
  - `GET /v2/insights/calls/{callId}/flows/{flowIndex}/insights` — codes d'erreur : `400`, `403` → `400`, `403`, `404`
  - `GET /v2/insights/calls/{callId}/flows/{flowIndex}/state` — champ(s) ajouté(s) : `canDelete` ; codes d'erreur : `400`, `403` → `400`, `403`, `404`
  - `GET /v2/insights/calls/{callId}/flows/{flowIndex}/summary` — codes d'erreur : `400`, `403` → `400`, `403`, `404`
  - `GET /v2/insights/chats/{chatId}/state` — champ(s) ajouté(s) : `canDelete`
  - `GET /v2/insights/conferences/{conferenceId}/insights` — codes d'erreur : `400`, `403` → `400`, `403`, `404`
  - `GET /v2/insights/conferences/{conferenceId}/state` — champ(s) ajouté(s) : `canDelete` ; codes d'erreur : `400`, `403` → `400`, `403`, `404`
  - `GET /v2/insights/conferences/{conferenceId}/summary` — codes d'erreur : `400`, `403` → `400`, `403`, `404`
  - `GET /v2/insights/conferences/{conferenceId}/timeframes` — codes d'erreur : `400`, `403` → `400`, `403`, `404`
  - `POST /v2/insights/conversations/aggregations/nested` — structure modifiée (réponse ou corps)
  - `POST /v2/insights/conversations/insights/aggregations` — structure modifiée (réponse ou corps)

### Stream API

- **Nouvelles routes** : `POST /v2/stream/services/stats`
- **Routes modifiées (10)** :
  - `GET /v2/stream/calls/{callId}` — champ(s) ajouté(s) : `id`, `key`, `payload`, `source`, `time`
  - `GET /v2/stream/calls/{callId}/annotations` — structure modifiée (réponse ou corps)
  - `GET /v2/stream/calls/{callId}/transcription` — champ(s) ajouté(s) : `key`, `payload`, `source`
  - `GET /v2/stream/chats/{chatId}/annotations` — structure modifiée (réponse ou corps)
  - `GET /v2/stream/conferences/{conferenceId}` — champ(s) ajouté(s) : `key`, `metric`, `payload`, `result`, `source`, `tag`, `text`, `variables`
  - `GET /v2/stream/conferences/{conferenceId}/annotations` — structure modifiée (réponse ou corps)
  - `GET /v2/stream/conferences/{conferenceId}/transcription` — champ(s) ajouté(s) : `key`, `metric`, `payload`, `result`, `source`, `tag`, `variables`
  - `POST /v2/stream/conversations` — champ(s) ajouté(s) : `key`, `payload`, `source`
  - `POST /v2/stream/events/consume` — champ(s) ajouté(s) : `autoTranscribe`, `rcsInbound`, `rcsStatus`
  - `POST /v2/stream/events/describe` — champ(s) ajouté(s) : `RcsInboundEvent`, `RcsStatusEvent`, `ServiceStatsAnalyticsLiveEvent`, `ServiceStatsSnapshotEvent`, `WebhookRcsStatusEvent`, `abandoned`, `abandonedWaitSumMs`, `acwSumMs`, `agentId`, `agentStats`, `agentsAvailable`, `agentsLoggedOff` …

### x-caracal API 🆕

- Nouveau service : 14 routes.

### Wilma Agents API 🆕

- Nouveau service : 17 routes.

### Wilma Artifacts API 🆕

- Nouveau service : 8 routes.

### Wilma Assistant API 🆕

- Nouveau service : 21 routes.

### Wilma Audit API 🆕

- Nouveau service : 3 routes.

### Wilma Chat API 🆕

- Nouveau service : 7 routes.

### Wilma Copilot API 🆕

- Nouveau service : 35 routes.

### Wilma Copilot Sessions API 🆕

- Nouveau service : 11 routes.

### Wilma Sandbox API 🆕

- Nouveau service : 11 routes.

### Wilma Secrets API (Credential Broker) 🆕

- Nouveau service : 20 routes.

### Wilma Skills API 🆕

- Nouveau service : 12 routes.

### Wilma Tools API 🆕

- Nouveau service : 25 routes.

### Wilma Traces API 🆕

- Nouveau service : 7 routes.

### Wilma Voice API 🆕

- Nouveau service : 9 routes.

### Wilma Workflows API 🆕

- Nouveau service : 16 routes.

## Remarques

- **Webhooks** : section reprise sans modification de la V2, non revérifiée lors de cette mise à jour.
- **Changements de forme non comptés** : les descriptions, contraintes (longueurs, motifs, bornes) et renvois à l'annexe des schémas ont été régénérés partout mais ne sont pas comptés comme des modifications.
- **PBX API** : chaque route indique désormais ses droits (**Scopes**) et, quand elle accepte une Company API Key, le droit exigé (**Company API Key scope**).
