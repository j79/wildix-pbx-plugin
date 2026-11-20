# Wildix API Reference (Compiled — full schemas)

Generated for use as a reference in Claude Code / automation projects targeting the Wildix PBX and collaboration platform.

Source: the live OpenAPI specifications published under `https://docs.wildix.com/codegen/api/*.openapi.json` (plus `https://docs.wildix.com/pbx-openapi.yaml` for the PBX API), fetched 2026-11-20. Previous revision: 2026-11-10.

Request bodies are **expanded field by field** (name, type, required flag, description, constraints) instead of only naming the OpenAPI component. Unions (`oneOf`) are expanded per variant. Deeply nested or recursive types are cut off and reproduced in each API's Schemas appendix.

## Statuts de publication

- 🆕 **Nouveau service / Nouvelle route** — publié(e) depuis la révision du 2026-11-10.
- ⚠️ **Deprecated (non publiée)** — route présente dans une révision antérieure mais retirée de la documentation publiée : en cours de décommissionnement, pas encore supprimée. Ces routes sont regroupées en fin de section API, sous « Routes non publiées », avec leur description d'origine et leur date de retrait.
- **Company API Key scope** — droit exigé quand la route est appelée avec une Company API Key (`Authorization: Bearer wsk-v1-…`) ; seules les routes PBX qui portent cette mention acceptent ces clés.

## Authentication

Security schemes declared by the services (Bearer unless noted):

| Scheme | Meaning |
|---|---|
| `Bearer` | S2S JWT (Bearer). See **S2S JWT signing** in the Authentication section. |
| `CompanyApiKey` | Company API Key (`wsk-v1-...`, 100 characters). Send as `Authorization: Bearer wsk-v1-...`. Requires a route-specific scope — see `x-wildix-companyApiKeyScope` on each operation. |
| `OAuth2` | OAuth2 Authorization Code or Implicit grant. See Authentication section for grant types and RFC links. |
| `Token` | Simple Token integration. Use `Authorization: Bearer access_...` or the `token` query parameter. See Authentication section. |
| `session` | Browser session cookie (`PHPSESSID`). Used by the WMS web UI. |
| `smithy.api.httpBasicAuth` | HTTP Basic authentication |
| `smithy.api.httpBearerAuth` | HTTP Bearer authentication |
| `wildix.auth.apiKeys` | Wildix API Keys authentication |
| `wildix.auth.bot` | Wildix x-bees Bot authentication |
| `wildix.auth.openIdPbx` | Wildix OpenId PBX authentication |
| `wildix.auth.openIdUser` | Wildix OpenId User authentication |
| `wildix.auth.pbx` | Wildix PBX CPA authentication |
| `wildix.auth.pbxBasic` | Wildix PBX Basic authentication |
| `wildix.auth.s2s` | Wildix s2s authentication |
| `wildix.auth.xbs` | Wildix x-bees user authentication |

Tokens are obtained from the Auth Service (see that section). Per-operation scopes are listed inline as **Scopes** under each endpoint.

## Changements depuis la révision du 2026-11-10

- **[Wilma Assistant API](#wilma-assistant-api)** — 1 nouvelle(s) route(s) : `POST /v2/assistant/voice/describe`

**Routes publiées mais marquées `deprecated` par Wildix** (22) — toujours documentées, à remplacer à terme :
  - **Conversations API** : `POST /v2/conversations/invite`
  - **Users & ChatBots API** : `POST /v2/users/UploadPicture`
  - **Integrations API** : `DELETE /v2/integrations/companies/{companyId}/integrations/{integrationId}`, `GET /v2/integrations/by-companys-and-services`, `GET /v2/integrations/by-id/{integrationId}`, `GET /v2/integrations/companies`, `GET /v2/integrations/companies/{companyId}`, `GET /v2/integrations/services`, `GET /v2/integrations/services/{service}`, `PATCH /v2/integrations/companies/{companyId}/integrations/{integrationId}`, `POST /v2/integrations/bulk/delete`, `PUT /v2/integrations/bulk/put`, `PUT /v2/integrations/companies/{companyId}`
  - **WNS Email API** : `POST /api/v2/mail/admin`
  - **Insights API** : `DELETE /v2/insights/projections-categories/{id}`, `POST /v2/insights/calls/{callId}/flows/{flowIndex}/schedule_summary_generation`, `POST /v2/insights/conferences/{conferenceId}/schedule_summary_generation`, `POST /v2/insights/conversations/insights`, `POST /v2/insights/conversations/insights/aggregations`, `POST /v2/insights/projections-categories`, `PUT /v2/insights/projections-categories/{id}`
  - **Wilma Assistant API** : `GET /v2/assistant/connectors`

Schémas régénérés à partir des spécifications actuelles : 21 route(s) existante(s) présentent des changements de paramètres, de corps, de réponse ou de codes d'erreur (détail dans le rapport des écarts).

**Webhooks** — section reprise sans modification de la révision précédente (non revérifiée automatiquement).

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
- [x-caracal API](#x-caracal-api)
- [Wilma Agents API](#wilma-agents-api)
- [Wilma Artifacts API](#wilma-artifacts-api)
- [Wilma Assistant API](#wilma-assistant-api)
- [Wilma Audit API](#wilma-audit-api)
- [Wilma Chat API](#wilma-chat-api)
- [Wilma Copilot API](#wilma-copilot-api)
- [Wilma Copilot Sessions API](#wilma-copilot-sessions-api)
- [Wilma Sandbox API](#wilma-sandbox-api)
- [Wilma Secrets API (Credential Broker)](#wilma-secrets-api-credential-broker)
- [Wilma Skills API](#wilma-skills-api)
- [Wilma Tools API](#wilma-tools-api)
- [Wilma Traces API](#wilma-traces-api)
- [Wilma Voice API](#wilma-voice-api)
- [Wilma Workflows API](#wilma-workflows-api)
- [Webhooks](#webhooks)

---
