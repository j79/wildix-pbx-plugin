# Rapport des écarts — référentiel API Wildix

Révision du 2026-11-20, comparée à la révision du 2026-11-10.

## Synthèse

- **931 routes publiées** dans 50 services.
- **1 routes nouvelles**.
- **0 routes de nouveau publiées**.
- **0 routes retirées** de la documentation depuis la révision précédente ; **8 routes deprecated conservées** au total, avec leur description d'origine et leur date de retrait.
- **21 routes existantes modifiées** dans leur structure.
- **22 routes publiées mais marquées `deprecated`** par Wildix.

## Détail par service

### Conversations API

- **Marquées `deprecated` par Wildix** : `POST /v2/conversations/invite`

### Users & ChatBots API

- **Marquées `deprecated` par Wildix** : `POST /v2/users/UploadPicture`

### Integrations API

- **Marquées `deprecated` par Wildix** : `DELETE /v2/integrations/companies/{companyId}/integrations/{integrationId}`, `GET /v2/integrations/by-companys-and-services`, `GET /v2/integrations/by-id/{integrationId}`, `GET /v2/integrations/companies`, `GET /v2/integrations/companies/{companyId}`, `GET /v2/integrations/services`, `GET /v2/integrations/services/{service}`, `PATCH /v2/integrations/companies/{companyId}/integrations/{integrationId}`, `POST /v2/integrations/bulk/delete`, `PUT /v2/integrations/bulk/put`, `PUT /v2/integrations/companies/{companyId}`

### Cache API

- **Routes modifiées (11)** :
  - `DELETE /v1/cache/general` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `GET /v1/cache/search` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `POST /v1/cache/integration-data/batch-write` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `POST /v1/cache/integration-data/delete` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `POST /v1/cache/integration-data/get` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `POST /v1/cache/object` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `POST /v1/cache/search` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `POST /v1/cache/sync` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `POST /v1/cache/weight` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `PUT /v1/cache/general` — codes d'erreur : `400`, `403` → `400`, `403`, `429`
  - `PUT /v1/cache/integration-data` — codes d'erreur : `400`, `403` → `400`, `403`, `429`

### VoiceBots API

- **Routes modifiées (1)** :
  - `POST /v2/voicebots/describe` — champ(s) ajouté(s) : `finalDropReason`

### WNS Email API

- **Marquées `deprecated` par Wildix** : `POST /api/v2/mail/admin`

### WMP Info API

- **Retirées lors d'une révision antérieure (toujours conservées)** : `GET /v1/companies/{companyId}`, `GET /v1/pbxs/{nameOrSerial}`, `POST /v1/pbx-key/check`

### STT Service

- **Retirées lors d'une révision antérieure (toujours conservées)** : `POST /api/v1/Common`, `POST /api/v1/Voicemail`

### TTS Service

- **Retirées lors d'une révision antérieure (toujours conservées)** : `GET /api/v2/Settings`, `POST /api/v2/Audio`

### URL-Preview Service

- **Retirées lors d'une révision antérieure (toujours conservées)** : `POST /api/v2/Url/`

### Insights API

- **Marquées `deprecated` par Wildix** : `DELETE /v2/insights/projections-categories/{id}`, `POST /v2/insights/calls/{callId}/flows/{flowIndex}/schedule_summary_generation`, `POST /v2/insights/conferences/{conferenceId}/schedule_summary_generation`, `POST /v2/insights/conversations/insights`, `POST /v2/insights/conversations/insights/aggregations`, `POST /v2/insights/projections-categories`, `PUT /v2/insights/projections-categories/{id}`

### Wilma Agents API

- **Routes modifiées (7)** :
  - `GET /v2/agents/agents` — champ(s) ajouté(s) : `duckAfterMs`, `duckVolumeDb`, `holdMs`, `lowConfidence`, `maxWaitMs`, `minConfidence`, `restoreAfterMs`, `silenceLevelDb`, `silenceMs`, `speechLevelDb`, `turnEnd`, `voiceDetection`
  - `GET /v2/agents/agents/{agentId}` — champ(s) ajouté(s) : `duckAfterMs`, `duckVolumeDb`, `holdMs`, `lowConfidence`, `maxWaitMs`, `minConfidence`, `restoreAfterMs`, `silenceLevelDb`, `silenceMs`, `speechLevelDb`, `turnEnd`, `voiceDetection`
  - `GET /v2/agents/agents/{agentId}/versions/{version}` — champ(s) ajouté(s) : `duckAfterMs`, `duckVolumeDb`, `holdMs`, `lowConfidence`, `maxWaitMs`, `minConfidence`, `restoreAfterMs`, `silenceLevelDb`, `silenceMs`, `speechLevelDb`, `turnEnd`, `voiceDetection`
  - `POST /v2/agents/agents` — champ(s) ajouté(s) : `duckAfterMs`, `duckVolumeDb`, `holdMs`, `lowConfidence`, `maxWaitMs`, `minConfidence`, `restoreAfterMs`, `silenceLevelDb`, `silenceMs`, `speechLevelDb`, `turnEnd`, `voiceDetection`
  - `POST /v2/agents/agents/{agentId}/versions` — champ(s) ajouté(s) : `duckAfterMs`, `duckVolumeDb`, `holdMs`, `lowConfidence`, `maxWaitMs`, `minConfidence`, `restoreAfterMs`, `silenceLevelDb`, `silenceMs`, `speechLevelDb`, `turnEnd`, `voiceDetection`
  - `POST /v2/agents/agents/{agentId}/versions/{version}/draft` — champ(s) ajouté(s) : `duckAfterMs`, `duckVolumeDb`, `holdMs`, `lowConfidence`, `maxWaitMs`, `minConfidence`, `restoreAfterMs`, `silenceLevelDb`, `silenceMs`, `speechLevelDb`, `turnEnd`, `voiceDetection`
  - `PUT /v2/agents/agents/{agentId}` — champ(s) ajouté(s) : `duckAfterMs`, `duckVolumeDb`, `holdMs`, `lowConfidence`, `maxWaitMs`, `minConfidence`, `restoreAfterMs`, `silenceLevelDb`, `silenceMs`, `speechLevelDb`, `turnEnd`, `voiceDetection`

### Wilma Assistant API

- **Nouvelles routes** : `POST /v2/assistant/voice/describe`
- **Marquées `deprecated` par Wildix** : `GET /v2/assistant/connectors`

### Wilma Voice API

- **Routes modifiées (2)** :
  - `POST /v2/voice/describe` — champ(s) ajouté(s) : `agent`, `atMs`, `audioBegin`, `audioEnd`, `callSocket`, `caller`, `client`, `company`, `connectionId`, `digits`, `draft`, `dropped` … ; champ(s) retiré(s) : `action`, `agentTranscriptionWebsocketEvent`, `audioWebsocketEvent`, `channels`, `command`, `completeWebsocketEvent`, `controlWebsocketEvent`, `encoding`, `errorWebsocketEvent`, `hangupWebsocketCommand`, `inputAudio`, `interruptionWebsocketEvent` …
  - `POST /v2/voice/sessions/{sessionId}/say` — champ(s) retiré(s) : `voice`

## Remarques

- **Webhooks** : section reprise sans modification de la révision précédente.
- Les changements de forme (descriptions, contraintes, renvois à l'annexe) ne sont pas comptés comme des modifications.
