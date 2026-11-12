# Wildix API Reference (Compiled — full schemas)

Generated for use as a reference in Claude Code / automation projects targeting the Wildix PBX and collaboration platform.

Source: the live OpenAPI specifications published under `https://docs.wildix.com/codegen/api/*.openapi.json` (plus `https://docs.wildix.com/pbx-openapi.yaml` for the PBX API), fetched 2026-11-10. Previous revision: 2026-10-18.

Request bodies are **expanded field by field** (name, type, required flag, description, constraints) instead of only naming the OpenAPI component. Unions (`oneOf`) are expanded per variant. Deeply nested or recursive types are cut off and reproduced in each API's Schemas appendix.

## Statuts de publication

- 🆕 **Nouveau service / Nouvelle route** — publié(e) depuis la révision du 2026-10-18.
- ⚠️ **Deprecated (non publiée)** — route présente dans une révision antérieure mais retirée de la documentation publiée : en cours de décommissionnement, pas encore supprimée. Ces routes sont regroupées en fin de section API, sous « Routes non publiées », avec leur description d'origine et leur date de retrait.
- **Company API Key scope** — droit exigé quand la route est appelée avec une Company API Key (`Authorization: Bearer wsk-v1-…`) ; seules les routes PBX qui portent cette mention acceptent ces clés.

## Authentication

Security schemes declared by the services (Bearer unless noted):

| Scheme | Meaning |
|---|---|
| `Bearer` | S2S JWT (Bearer). See **S2S JWT signing** in the Authentication section. 🆕 |
| `CompanyApiKey` | Company API Key (`wsk-v1-...`, 100 characters). Send as `Authorization: Bearer wsk-v1-...`. Requires a route-specific scope — see `x-wildix-companyApiKeyScope` on each operation. 🆕 |
| `OAuth2` | OAuth2 Authorization Code or Implicit grant. See Authentication section for grant types and RFC links. 🆕 |
| `Token` | Simple Token integration. Use `Authorization: Bearer access_...` or the `token` query parameter. See Authentication section. 🆕 |
| `session` | Browser session cookie (`PHPSESSID`). Used by the WMS web UI. 🆕 |
| `smithy.api.httpBasicAuth` | HTTP Basic authentication 🆕 |
| `smithy.api.httpBearerAuth` | HTTP Bearer authentication 🆕 |
| `wildix.auth.apiKeys` | Wildix API Keys authentication |
| `wildix.auth.bot` | Wildix x-bees Bot authentication |
| `wildix.auth.openIdPbx` | Wildix OpenId PBX authentication |
| `wildix.auth.openIdUser` | Wildix OpenId User authentication |
| `wildix.auth.pbx` | Wildix PBX CPA authentication |
| `wildix.auth.pbxBasic` | Wildix PBX Basic authentication |
| `wildix.auth.s2s` | Wildix s2s authentication |
| `wildix.auth.xbs` | Wildix x-bees user authentication |

Tokens are obtained from the Auth Service (see that section). Per-operation scopes are listed inline as **Scopes** under each endpoint.

## Changements depuis la révision du 2026-10-18

- **[PBX API](#pbx-api)** — 21 route(s) de nouveau publiée(s) : `DELETE /api/v2/call-groups/{id}/members/dynamic/{member}`, `GET /api/v2/personal/features`, `GET /api/v2/personal/features/`, `GET /call-control/list-calls/`, `GET /call-control/list-devices/`, `POST /api/v2/call-groups/{id}/forward/`, `POST /api/v2/call-groups/{id}/members/dynamic/`, `POST /api/v2/personal/features`, `POST /api/v2/personal/features/`, `POST /broadcasts/reload/`, `POST /call-control/answer/`, `POST /call-control/attendant-transfer/`, `POST /call-control/blind-transfer/`, `POST /call-control/dtmf/`, `POST /call-control/hangup/`, `POST /call-control/hold/`, `POST /call-control/make-call/`, `POST /call-control/unhold/`, `POST /call-control/update-contact-info/`, `PUT /PBX/settings/`, `PUT /call-control/set-active-device/`
- **[Cloud PBX API (Permissions)](#cloud-pbx-api-permissions)** — 1 nouvelle(s) route(s) : `POST /v1/permissions/delete_call_recordings_of_users/check`
- **[WMP Info API](#wmp-info-api)** — 2 nouvelle(s) route(s) : `GET /v2/PBXs/{domain}`, `GET /v2/companies/{companyId}` ; 3 route(s) retirée(s) de la documentation, conservée(s) en non publiée(s) : `GET /v1/companies/{companyId}`, `GET /v1/pbxs/{nameOrSerial}`, `POST /v1/pbx-key/check`
- **[Classound API](#classound-api)** — 2 nouvelle(s) route(s) : `GET /v1/s2s/rcs/brands`, `POST /v1/s2s/rcs/send`
- **[Insights API](#insights-api)** — 2 nouvelle(s) route(s) : `DELETE /v2/insights/calls/{callId}/assets`, `DELETE /v2/insights/conferences/{conferenceId}/assets`
- **[Stream API](#stream-api)** — 1 nouvelle(s) route(s) : `POST /v2/stream/services/stats`
- **[x-caracal API](#x-caracal-api)** — 🆕 nouveau service (14 routes)
- **[Wilma Agents API](#wilma-agents-api)** — 🆕 nouveau service (17 routes)
- **[Wilma Artifacts API](#wilma-artifacts-api)** — 🆕 nouveau service (8 routes)
- **[Wilma Assistant API](#wilma-assistant-api)** — 🆕 nouveau service (21 routes)
- **[Wilma Audit API](#wilma-audit-api)** — 🆕 nouveau service (3 routes)
- **[Wilma Chat API](#wilma-chat-api)** — 🆕 nouveau service (7 routes)
- **[Wilma Copilot API](#wilma-copilot-api)** — 🆕 nouveau service (35 routes)
- **[Wilma Copilot Sessions API](#wilma-copilot-sessions-api)** — 🆕 nouveau service (11 routes)
- **[Wilma Sandbox API](#wilma-sandbox-api)** — 🆕 nouveau service (11 routes)
- **[Wilma Secrets API (Credential Broker)](#wilma-secrets-api-credential-broker)** — 🆕 nouveau service (20 routes)
- **[Wilma Skills API](#wilma-skills-api)** — 🆕 nouveau service (12 routes)
- **[Wilma Tools API](#wilma-tools-api)** — 🆕 nouveau service (25 routes)
- **[Wilma Traces API](#wilma-traces-api)** — 🆕 nouveau service (7 routes)
- **[Wilma Voice API](#wilma-voice-api)** — 🆕 nouveau service (9 routes)
- **[Wilma Workflows API](#wilma-workflows-api)** — 🆕 nouveau service (16 routes)

**Routes publiées mais marquées `deprecated` par Wildix** (22) — toujours documentées, à remplacer à terme :
  - **Conversations API** : `POST /v2/conversations/invite`
  - **Users & ChatBots API** : `POST /v2/users/UploadPicture`
  - **Integrations API** : `DELETE /v2/integrations/companies/{companyId}/integrations/{integrationId}`, `GET /v2/integrations/by-companys-and-services`, `GET /v2/integrations/by-id/{integrationId}`, `GET /v2/integrations/companies`, `GET /v2/integrations/companies/{companyId}`, `GET /v2/integrations/services`, `GET /v2/integrations/services/{service}`, `PATCH /v2/integrations/companies/{companyId}/integrations/{integrationId}`, `POST /v2/integrations/bulk/delete`, `PUT /v2/integrations/bulk/put`, `PUT /v2/integrations/companies/{companyId}`
  - **WNS Email API** : `POST /api/v2/mail/admin`
  - **Insights API** : `DELETE /v2/insights/projections-categories/{id}`, `POST /v2/insights/calls/{callId}/flows/{flowIndex}/schedule_summary_generation`, `POST /v2/insights/conferences/{conferenceId}/schedule_summary_generation`, `POST /v2/insights/conversations/insights`, `POST /v2/insights/conversations/insights/aggregations`, `POST /v2/insights/projections-categories`, `PUT /v2/insights/projections-categories/{id}`
  - **Wilma Assistant API** : `GET /v2/assistant/connectors`

Schémas régénérés à partir des spécifications actuelles : 159 route(s) existante(s) présentent des changements de paramètres, de corps, de réponse ou de description (détail dans le rapport des écarts). Les routes PBX indiquent désormais leurs droits (**Scopes**) et, le cas échéant, le droit exigé pour une Company API Key.

**Webhooks** — section reprise sans modification de la révision du 2026-10-18 (non revérifiée lors de cette mise à jour).

## Table of contents

- [PBX API](#pbx-api)
- [Cloud PBX API (Permissions)](#cloud-pbx-api-permissions)
- [Cloud PBX Server API](#cloud-pbx-server-api)
- [Conversations API](#conversations-api)
- [Assistant API](#assistant-api)
- [Kite API](#kite-api)
- [Users & ChatBots API](#users--chatbots-api)
- [Auth Service](#auth-service)
- [Auth API Keys Service](#auth-api-keys-service)
- [CDS CA API](#cds-ca-api)
- [CDS Console API](#cds-console-api)
- [CDS PBX API](#cds-pbx-api)
- [CDS Utils API](#cds-utils-api)
- [WAM API](#wam-api)
- [Integrations API](#integrations-api)
- [Calendar API](#calendar-api)
- [Cache API](#cache-api)
- [Knowledge Base API](#knowledge-base-api)
- [Wim Tools API](#wim-tools-api)
- [VoiceBots API](#voicebots-api)
- [WNS Email API](#wns-email-api)
- [WNS Push API](#wns-push-api)
- [Broadcasts API (x-hoppers)](#broadcasts-api-x-hoppers)
- [WMP Info API](#wmp-info-api)
- [Filesharing Service](#filesharing-service)
- [GEO Service](#geo-service)
- [MFA Service](#mfa-service)
- [SSL Service](#ssl-service)
- [STT Service](#stt-service)
- [TTS Service](#tts-service)
- [URL-Preview Service](#url-preview-service)
- [Classound API](#classound-api)
- [History API](#history-api)
- [Insights API](#insights-api)
- [Stream API](#stream-api)
- [x-caracal API](#x-caracal-api) 🆕
- [Wilma Agents API](#wilma-agents-api) 🆕
- [Wilma Artifacts API](#wilma-artifacts-api) 🆕
- [Wilma Assistant API](#wilma-assistant-api) 🆕
- [Wilma Audit API](#wilma-audit-api) 🆕
- [Wilma Chat API](#wilma-chat-api) 🆕
- [Wilma Copilot API](#wilma-copilot-api) 🆕
- [Wilma Copilot Sessions API](#wilma-copilot-sessions-api) 🆕
- [Wilma Sandbox API](#wilma-sandbox-api) 🆕
- [Wilma Secrets API (Credential Broker)](#wilma-secrets-api-credential-broker) 🆕
- [Wilma Skills API](#wilma-skills-api) 🆕
- [Wilma Tools API](#wilma-tools-api) 🆕
- [Wilma Traces API](#wilma-traces-api) 🆕
- [Wilma Voice API](#wilma-voice-api) 🆕
- [Wilma Workflows API](#wilma-workflows-api) 🆕
- [Webhooks](#webhooks)

---
