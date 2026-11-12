# Webhooks

> Vérifié le 2026-10-18 contre les pages publiées sur docs.wildix.com : les événements, descriptions et commandes ci-dessous sont inchangés depuis la révision du 2026-07-17.

Wildix supports two webhook delivery mechanisms: HTTP callbacks and AWS SQS. General rules for HTTP webhook endpoints:

- Must be publicly reachable (tunneling services such as Ngrok are supported for development)
- Must accept HTTP POST requests with a JSON payload
- Must respond with an HTTP status code in the 200-299 range
- Should respond as fast as possible (exact timing depends on webhook type)
- Must be idempotent / safe to receive the same event multiple times (Wildix may retry on failure)

Each event payload generally includes: `id`, `pbx`, `company`, `time`, `type`, `integrationId`, and a `data` object with event-specific fields.

## Calls (`/docs/calls/webhooks`)

- **call:live:progress** — Triggered when an ongoing call starts or gets updated.
- **call:live:completed** — Triggered when a call ends.
- **call:live:interrupted** — Triggered when a call ends due to an error.
- **call:live:transcription** — Triggered when a new transcription segment for the call is available.
- **call:start** (deprecated) — Triggered when a call starts.
- **call:update** (deprecated) — Triggered when a call gets updated.
- **call:end** (deprecated) — Triggered when a call ends.

## Messaging (`/docs/messaging/webhooks`)

- **chat:channel:created** — Triggered when a new chat channel is created.
- **chat:channel:updated** — Triggered when a chat channel is updated.
- **chat:member:added** — Triggered when a new member is added to a chat channel.
- **chat:member:removed** — Triggered when a member is removed from a chat channel.
- **chat:message:new** — Triggered when a new message is sent in a chat channel.
- **chat:message:updated** — Triggered when a message is updated in a chat channel.
- **chat:message:deleted** — Triggered when a message is deleted from a chat channel.
- **chat:reaction:new** — Triggered when a user reacts to a message.
- **chat:reaction:deleted** — Triggered when a user removes a reaction from a message.
- **chat:live:progress** — Triggered when a live chat session starts or gets updated.
- **chat:live:completed** — Triggered when a live chat session ends.
- **chat:live:interrupted** — Triggered when a live chat session ends due to an error.
- **chat:manager:missed** — Triggered when a chat detects a missed manager.

## Conferences (`/docs/conferences/webhooks`)

- **conference:live:progress** — Triggered when an ongoing conference starts or gets updated.
- **conference:live:join** — Triggered when a user joins the conference.
- **conference:live:leave** — Triggered when a user leaves the conference.
- **conference:live:completed** — Triggered when a conference ends.
- **conference:live:interrupted** — Triggered when a conference ends due to an error.
- **conference:live:transcription** — Triggered when a new transcription segment for the conference is available.

## Presences (`/docs/presences/webhooks`)

- **presence:user** — Triggered when a user changes their presence status.
- **presence:telephony** — Triggered when a user changes their "On the call" status.
- **presence:conference** — Triggered when a user joins or leaves a conference, updating their presence status.

## SMS (`/docs/sms/webhooks`)

- **sms:status** — Triggered when an SMS status event is received.

## Analytics (`/docs/analytics/webhooks`)

- **call:completed** — Triggered when a call ends and all related information is stored.
- **conference:completed** — Triggered when a conference ends and all related information is stored.
- **chat:completed** — Triggered when a chat session ends and all related information is stored.

## VoiceBots — Webhook & AWS SQS integration (`/docs/calls/voicebots/integrations/webhooks_sqs`)

Used for bidirectional, real-time control of a Voice Agent session (custom conversation handling).

Events sent by the voice agent service to your application:
- **transcription** — fields: `type`, `id`, `text`, `time` — sent when the user's speech is recognized and transcribed.
- **reply** — fields: `type`, `id`, `text`, `startTime`, `endTime` — sent when the user finishes speaking.
- **playback** — fields: `type`, `text`, `replyId`, `complete`, `startTime`, `endTime` — sent when the bot starts or finishes speaking a response.
- **interruption** — fields: `type`, `replyId`, `playedText`, `originalText`, `time` — sent when the user interrupts the bot while it's speaking.

Commands your application can send back (over HTTP API / SDK):
- **SendHangupCommand** — Terminates the voice session and the call. Scope: `voicebots:SendHangup`
- **SendSayCommand** — Generates and plays specified text through the voice session's audio stream. Scope: `voicebots:SendSay`
- **SendTransferCommand** — Transfers the call to a specified context/extension and ends the voice bot session. Scope: `voicebots:SendTransfer`

## Chatbots — Webhook & AWS SQS integration (`/docs/messaging/bots/integrations/webhooks_sqs`)

> 🆕 Page absente de la révision précédente (ajoutée dans cette révision).

Used for full, real-time control of a chatbot session (custom conversation handling). The chatbot service sends chat events to your HTTP endpoint or AWS SQS queue; your application replies by calling x-bees Conversations API commands.

Events sent by the chatbot service to your application (same payloads as the Messaging webhooks; TypeScript definitions in `@wildix/xbees-conversations-client`):
- **chat:channel:created** — Triggered when a new chat channel is created (`WebhookChatChannelCreatedEvent`).
- **chat:message:new** — Triggered when a new message is sent in a chat channel.

Commands your application can send back (over HTTP API / SDK — see [Conversations API](#conversations-api)):
- **UploadFileCommand** — Creates a presigned URL for file upload in the channel. Scope: `messaging:UploadFile`
- **AddChannelMembersCommand** — Adds members to an existing channel (idempotent; deactivated accounts are skipped and returned). Scope: `messaging:AddChannelMembers`
- **SendMessageCommand** — Sends a message to a specified channel (the channel must be accessible to the user). Scope: `messaging:SendMessage`
- **GetFilePresignedDownloadUrlCommand** — Retrieves a presigned URL to download a file from a message in a channel. Scopes: `messaging:GetFilePresignedDownloadUrl`, `messaging:read`
- **SendTypingStartCommand** — Sends a typing start event to a channel. Scope: `messaging:SendTypingStart`
- **SendTypingStopCommand** — Sends a typing stop event to a channel. Scope: `messaging:SendTypingStop`

## Types d'événements déclarés dans les spécifications OpenAPI mais absents des pages Webhooks

> Ces types figurent dans l'énumération `WebhookEventType` des spécifications OpenAPI, sans page de documentation dédiée ni exemple de charge utile. Les schémas correspondants (`Webhook…Event`), lorsqu'ils existent, sont décrits dans l'annexe des schémas de l'API concernée. 🆕 = valeur absente de la spécification au 2026-07-17.

**Stream API — `WebhookEventType`**

- `call:live:annotation`
- `call:live:record:start`
- `call:live:record:stop`
- `call:live:record:pause`
- `call:live:record:unpause`
- `call:transcription:completed`
- `call:transcription:text:completed`
- `call:annotations:completed`
- `call:insights:completed` 🆕
- `call:summary:completed`
- `conference:live:annotation`
- `conference:transcription:completed`
- `conference:transcription:text:completed`
- `conference:annotations:completed`
- `conference:insights:completed` 🆕
- `conference:summary:completed`
- `service:call:live:progress`
- `service:call:live:completed`
- `chat:live:annotation`
- `chat:live:missed`
- `chat:annotations:completed`
- `chat:insights:completed` 🆕
- `chat:summary:completed`
- `whatsapp:status` 🆕
- `messenger:status` 🆕

**Conversations API — `WebhookEventType`**

- `chat:action:triggered`
