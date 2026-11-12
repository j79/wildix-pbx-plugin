## Wilma Agents API 🆕

_OpenAPI: Wilma Agents Service — version v2_

**Servers**

- `https://api.wilma.wildix.com` — Production
- `https://api-stable.wilma.wildix.com` — Stable
- `https://api-stage.wilma.wildix.com` — Stage

### Agents

#### `GET` `/v2/agents/agents`

Retrieves a paginated list of agents for the specified company.

- operationId: `ListAgents`
- **Scopes**: `wilma-agents:ListAgents`, `wilma-agents:read`
- **Parameters**
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `channel` (query) — string — Only agents that have this channel enabled (voice / chat / assistant) and whose engine can serve it. An agent serving no channel matches no value of this filter, so a caller listing agents to run as a task must leave it unset. _(enum: `voice`, `chat`, `assistant`)_
  - `status` (query) — string _(enum: `draft`, `active`)_
  - `search` (query) — string — Filter by name or category.
  - `limit` (query) — number _(min=1; max=100)_
  - `cursor` (query) — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- **Response 200** (`ListAgentsResponseContent`)
  - `agents` — array **(required)**
    - _array of_ `Agent`
      - `name` — string **(required)** _(minLen=3; maxLen=255)_
      - `description` — string _(minLen=1; maxLen=1000)_
      - `category` — string — Category of the agent, e.g.: 'Support'. _(minLen=1; maxLen=128)_
      - `picture` — string — Avatar URL.
      - `channels` — AgentChannels **(required)** — The channels an agent serves and their channel-specific settings. Presence of a member enables that channel. Empty means the agent serves no channel: it is not reachable on its own and runs only as an automation's task or when another agent calls it. Enabled channels are mirrored as ChannelType values on AgentInfo.
        - `voice` — VoiceChannelSettings — Voice channel settings. Note: a voice agent's AgentAccess.grants are ignored — inbound calls are routed by the PBX dialplan and data ACL is the agent-level `settings.pbxGroupId`, not per-user grants.
          - `greeting` — string — Message spoken when the call starts.
          - `backgroundSound` — VoiceBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT like `interruptions` and `endCall`, rather than a loose name on the channel: it is one switchable call behaviour, it reads the same way as its siblings, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
            - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
            - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
          - `speech` — VoiceSpeechSettings — Speech configuration for the voice channel. When present it WINS over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the single exception, because it is the channel's own input signal and the feature has no starting point without it.
            - `languages` — array **(required)** — Configured languages. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once: automatic detection here is opt-in (`transcription.autoDetect`), and once a caller turns it on, the service does not clamp the resulting candidate list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five) — a caller who both opts in and configures more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. With detection off, only the single resolved language is ever sent, so the ceiling never becomes a candidate-list problem at all. _(minItems=1; maxItems=10)_
              - _(nesting depth limit — see `VoiceLanguage` in the Schemas appendix)_
            - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in the voice, provider account and pronunciation rules of its own language, instead of only the language the call resolved to. Languages whose first message is empty, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
            - `transcription` — VoiceTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
              - _(nesting depth limit — see `VoiceTranscriptionSettings` in the Schemas appendix)_
          - `interruptions` — VoiceInterruptionSettings
            - `enabled` — boolean **(required)** — Whether the caller can interrupt the agent while it is speaking.
            - `minWords` — number — Minimum number of caller words that count as an interruption. _(min=1; max=10)_
          - `silenceTimeout` — VoiceSilenceTimeoutSettings
            - `seconds` — number **(required)** — Seconds of caller silence before the action is taken. _(min=1; max=600)_
            - `action` — union **(required)**
              - _(nesting depth limit — see `VoiceTerminateAction` in the Schemas appendix)_
          - `maxDuration` — VoiceMaxDurationSettings
            - `seconds` — number **(required)** — Maximum call duration in seconds before the action is taken. _(min=10; max=14400)_
            - `action` — union **(required)**
              - _(nesting depth limit — see `VoiceTerminateAction` in the Schemas appendix)_
          - `endCall` — VoiceEndCallSettings
            - `enabled` — boolean **(required)**
            - `phrases` — string — Comma-separated phrases that end the call, e.g. 'goodbye,bye'.
          - `callerMetadata` — VoiceCallerMetadataSettings — Caller context injected into the model prompt.
            - `callerName` — boolean — Include the caller name. Defaults to true.
            - `callerNumber` — boolean — Include the caller phone number. Defaults to true.
            - `callerEmail` — boolean — Include the caller email when known. Defaults to false.
            - `callerCompany` — boolean — Include the caller company when known. Defaults to false.
            - `time` — boolean — Include the current time, rendered in the agent's `engine.ai.timeZone`. Defaults to false.
        - `chat` — ChatChannelSettings
          - `discoverable` — boolean — Whether users can find and add this agent to conversations.
          - `sessionTimeoutMinutes` — number — Minutes a conversation can stay idle before the next message starts a new session. Omit to start a new session at the end of the agent's local day (`engine.ai.timeZone`). Allowed values: 15, 30, 60, 120. _(min=15; max=120)_
          - `verbosity` — string — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
        - `assistant` — AssistantChannelSettings — Assistant channel settings. Presence enables the in-app assistant surface; audio remains unavailable unless its separate settings are present and enabled.
          - `default` — boolean — Offer this agent as the default assistant for users covered by the agent access settings.
          - `ui` — AssistantUiSettings — How the agent presents itself in the assistant UI: what the user reads before typing anything, and what they can start from without typing at all. Everything here is presentation — it never changes what the agent can do.
            - `welcome` — AssistantWelcomeSettings — Greeting shown on an empty thread, above the quick commands.
              - _(nesting depth limit — see `AssistantWelcomeSettings` in the Schemas appendix)_
            - `commands` — array — Cards offered under the welcome message on an empty thread, in the order given. Empty or omitted shows no cards. _(maxItems=8)_
              - _(nesting depth limit — see `AssistantQuickCommand` in the Schemas appendix)_
            - `placeholder` — string — Placeholder text in the composer, e.g. 'Ask about an account…'. Defaults to the client's own placeholder when omitted. _(minLen=1; maxLen=100)_
          - `audio` — AssistantAudioSettings — Switchable audio for the assistant channel. The settings object keeps enablement beside its speech policy, matching the voice channel's switchable blocks so a disabled configuration can be retained without serving audio.
            - `enabled` — boolean **(required)** — Whether the assistant accepts audio calls. Required so the presence of saved speech configuration is never mistaken for enablement.
            - `speech` — AssistantSpeechSettings — Recognition and synthesis policy for assistant audio. This is assistant-owned rather than a VoiceSpeechSettings reuse so telephony and assistant audio can evolve independently. It has no language greeting and no greet-every-language switch because an assistant conversation is already open when its audio call starts, leaving nothing for the channel to greet.
              - _(nesting depth limit — see `AssistantSpeechSettings` in the Schemas appendix)_
      - `engine` — union **(required)** — How the agent produces replies. `ai` is the managed engine; `webhook` and `sqs` delegate to an external backend.
        - _oneOf_ — exactly one of:
          - **`ai`**
            - `ai` — AgentAiEngine **(required)** — Managed AI engine: the platform runs the model, tools and knowledge lookups.
              - `instructions` — string **(required)** _(minLen=1; maxLen=60000)_
              - `workflow` — AgentWorkflow — The agent's conversation as a graph: which step runs first, what each step does, and on what condition control moves on. Optional on AgentAiEngine — without one the agent is prompt-driven, steered by `instructions` and free to use its capabilities in any order. Versioned with the rest of the agent definition: publishing a version snapshots the graph, and a draft edit reaches no session until it is published and routed.
                - _(nesting depth limit — see `AgentWorkflow` in the Schemas appendix)_
              - `guardrails` — AgentGuardrails — Turn screening, by side. Only `input` exists: it guards what reaches the model, and output screening is a separate policy with different actions, added here when it is built.
                - _(nesting depth limit — see `AgentGuardrails` in the Schemas appendix)_
              - `model` — string — Defaults to the platform default model when omitted. _(pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
              - `timeZone` — string — IANA timezone the agent reasons about time in: it anchors the current date and time given to the model and how times are read from and written to tool arguments and replies. Shared by every channel the agent serves. Defaults to 'UTC'. _(minLen=1; maxLen=64)_
              - `artifacts` — boolean — Whether the agent can produce artifacts (wilma-artifacts): files it writes in its sandbox and shares back during a session — a document, a PDF, a spreadsheet, a chart, a multi-page web site, a folder of files. Needs the sandbox capability. An artifact starts private to the user the session runs for, who can share it company-wide from the viewer; on the chat channel the runtime shares each one company-wide as it is created, so the link posted into the conversation opens for every signed-in colleague. Artifacts are company-internal: recipients on external transports (sms / whatsapp) or outside the company cannot open the links, so keep this disabled for customer-facing agents. Defaults to false.
              - `skills` — array — Skills attached to this agent (progressive disclosure). A skill may carry its own tools, which join this agent's toolset while that skill is active.
                - _(nesting depth limit — see `AgentSkillReference` in the Schemas appendix)_
              - `capabilities` — array — Everything the agent can do. When a `workflow` is set these are the capabilities in scope at every step, and a step may add to them or narrow them with its own list of the same shape.
                - _(nesting depth limit — see `AgentCapability` in the Schemas appendix)_
              - `variables` — array
                - _(nesting depth limit — see `AgentVariable` in the Schemas appendix)_
          - **`webhook`**
            - `webhook` — AgentWebhookEngine **(required)** — Bring-your-own backend over HTTPS. The platform POSTs call events to the URL; the backend answers out of band through the channel's command API. The response body is not read.
              - `url` — string **(required)**
              - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
                - _(nesting depth limit — see `SecretRef` in the Schemas appendix)_
              - `timeout` — number — Timeout of one delivery, in milliseconds. _(default=10000; min=5000; max=120000)_
          - **`sqs`**
            - `sqs` — AgentSqsEngine **(required)** — Bring-your-own backend over SQS. The platform sends call events to the queue; the backend answers out of band through the channel's command API.
              - `url` — string **(required)**
              - `key` — string **(required)**
              - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
                - _(nesting depth limit — see `SecretRef` in the Schemas appendix)_
      - `settings` — AgentSettings — Agent-level settings shared across all channels.
        - `pbxGroupId` — string — PBX group used for data ACL (e.g. Sales Intelligence lookups).
      - `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
        - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
        - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
          - _array of_ `AgentGrantPrincipal`
            - _oneOf_ — exactly one of:
              - **`userId`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`groupId`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`department`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
        - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
        - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
        - `name` — string — Human readable name of the actor at the time of the action.
      - `updatedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `updatedBy` — Actor — Who performed an action: an interactive user, an API key or an internal service.
        - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
        - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
        - `name` — string — Human readable name of the actor at the time of the action.
      - `id` — string **(required)** _(minLen=12; maxLen=12)_
      - `status` — string **(required)** _(enum: `draft`, `active`)_
      - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
      - `latestVersion` — number — Latest published version number; absent while the agent is still a draft. _(min=1)_
      - `draftBaseVersion` — number — Published version number from which the current draft originated. Absent before the first version is published. _(min=1)_
      - `deployment` — array — How new sessions are split across published versions. Absent while the agent is still a draft. _(minItems=1; maxItems=10)_
        - _array of_ `AgentDeploymentRoute`
          - `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
          - `percentage` — number **(required)** — Percentage of new sessions routed to this version. Percentages must sum to 100. _(min=1; max=100)_
  - `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- Errors: `400`

#### `POST` `/v2/agents/agents`

Creates a new mutable agent draft. The agent serves no traffic until the draft is published and PutAgentDeployment routes sessions to that version.

- operationId: `CreateAgent`
- **Scopes**: `wilma-agents:CreateAgent`
- **Parameters**
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `CreateAgentRequestContent`) **(required)**
  - `name` — string **(required)** _(minLen=3; maxLen=255)_
  - `description` — string _(minLen=1; maxLen=1000)_
  - `category` — string — Category of the agent, e.g.: 'Support'. _(minLen=1; maxLen=128)_
  - `picture` — string — Avatar URL.
  - `channels` — AgentChannels **(required)** — The channels an agent serves and their channel-specific settings. Presence of a member enables that channel. Empty means the agent serves no channel: it is not reachable on its own and runs only as an automation's task or when another agent calls it. Enabled channels are mirrored as ChannelType values on AgentInfo.
    - `voice` — VoiceChannelSettings — Voice channel settings. Note: a voice agent's AgentAccess.grants are ignored — inbound calls are routed by the PBX dialplan and data ACL is the agent-level `settings.pbxGroupId`, not per-user grants.
      - `greeting` — string — Message spoken when the call starts.
      - `backgroundSound` — VoiceBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT like `interruptions` and `endCall`, rather than a loose name on the channel: it is one switchable call behaviour, it reads the same way as its siblings, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
        - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
        - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
      - `speech` — VoiceSpeechSettings — Speech configuration for the voice channel. When present it WINS over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the single exception, because it is the channel's own input signal and the feature has no starting point without it.
        - `languages` — array **(required)** — Configured languages. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once: automatic detection here is opt-in (`transcription.autoDetect`), and once a caller turns it on, the service does not clamp the resulting candidate list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five) — a caller who both opts in and configures more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. With detection off, only the single resolved language is ever sent, so the ceiling never becomes a candidate-list problem at all. _(minItems=1; maxItems=10)_
          - _array of_ `VoiceLanguage`
            - `code` — string **(required)** — BCP-47 code with locale, e.g. 'en-US', 'it-IT'. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
            - `voice` — string **(required)** — Voice this language speaks with, as a URI — provider, voice id, synthesis parameters and, where the company uses its own provider account, an `apiKey=secrets:{secretId}` reference. See VoiceUri. PER LANGUAGE, and that is the whole reason the member is here rather than on the settings above: provider quality is not uniform across languages, a voice id belongs to exactly one provider, and a bot-wide provider made changing it invalidate every configured voice at once. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
            - `greeting` — string — Initial phrase spoken when the call starts in this language. Absent or empty means the agent says nothing and waits — it does NOT fall back to VoiceChannelSettings.greeting, which would speak one language's text in another language's voice.
            - `isDefault` — boolean — Marks the language a caller hears when their own matches nothing configured. THE FULL RESOLUTION ORDER, since a client author reading only this contract cannot otherwise find it: an exact match on the call's language, then a match on its primary subtag (`fr` finds `fr-FR`), then the language marked here, then a language whose primary subtag is `en`, then the first entry in the list. Marked is consulted BEFORE the English step, so a record with none marked resolves exactly as it did before this member existed. English is deliberate rather than arbitrary — it is the language a caller the agent was not built for is likeliest to understand — and the last step exists only to keep the rule total, which is why list order should not be treated as configuration. At most one language may carry it. A record with two — reachable through the API or the CLI, where no form prevents it — resolves to the first marked one in list order, because refusing a call over configuration drift is worse than serving it and saying so in the trace.
            - `pronunciations` — array — The rules this language is spoken with. THE WHOLE SET rather than an override layer: an agent's respellings are stored here and read from here, so what this list says is what the caller hears. THERE IS NOTHING ABOVE IT. An earlier draft of this contract carried a company-wide dictionary per language that every agent speaking it inherited, with a merge order over this member and an identity rule ('Wildix' -> 'Wildix') for declining an inherited respelling. It bought correcting a handful of names in one place, and cost a second store, a merge on every synthesis path, a screen of its own, and a reader who could not tell from an agent what that agent would actually say. Per language per agent is where the divergence that matters already lives. _(maxItems=200)_
              - _(nesting depth limit — see `VoicePronunciation` in the Schemas appendix)_
        - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in the voice, provider account and pronunciation rules of its own language, instead of only the language the call resolved to. Languages whose first message is empty, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
        - `transcription` — VoiceTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
          - `engine` — string — Recogniser to transcribe the caller with. Absent resolves to the platform default ('aws://transcribe' today), resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
          - `autoDetect` — boolean — Identify the caller's language per utterance and switch voice and reply language mid-call. HERE RATHER THAN ON `VoiceSpeechSettings`, because identifying a language is something the RECOGNISER does: it becomes identify-multiple-languages plus language-options on the recognition stream, and nothing about synthesis reads it. Requires at least two configured languages and a recogniser that can identify them; the server clamps it to false otherwise, because forwarding true with a single candidate makes Amazon reject the stream outright.
      - `interruptions` — VoiceInterruptionSettings
        - `enabled` — boolean **(required)** — Whether the caller can interrupt the agent while it is speaking.
        - `minWords` — number — Minimum number of caller words that count as an interruption. _(min=1; max=10)_
      - `silenceTimeout` — VoiceSilenceTimeoutSettings
        - `seconds` — number **(required)** — Seconds of caller silence before the action is taken. _(min=1; max=600)_
        - `action` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`hangup`**
              - `hangup` — VoiceTerminateHangupAction **(required)**
                - _(nesting depth limit — see `VoiceTerminateHangupAction` in the Schemas appendix)_
            - **`transfer`**
              - `transfer` — VoiceTransferTarget **(required)**
                - _(nesting depth limit — see `VoiceTransferTarget` in the Schemas appendix)_
      - `maxDuration` — VoiceMaxDurationSettings
        - `seconds` — number **(required)** — Maximum call duration in seconds before the action is taken. _(min=10; max=14400)_
        - `action` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`hangup`**
              - `hangup` — VoiceTerminateHangupAction **(required)**
                - _(nesting depth limit — see `VoiceTerminateHangupAction` in the Schemas appendix)_
            - **`transfer`**
              - `transfer` — VoiceTransferTarget **(required)**
                - _(nesting depth limit — see `VoiceTransferTarget` in the Schemas appendix)_
      - `endCall` — VoiceEndCallSettings
        - `enabled` — boolean **(required)**
        - `phrases` — string — Comma-separated phrases that end the call, e.g. 'goodbye,bye'.
      - `callerMetadata` — VoiceCallerMetadataSettings — Caller context injected into the model prompt.
        - `callerName` — boolean — Include the caller name. Defaults to true.
        - `callerNumber` — boolean — Include the caller phone number. Defaults to true.
        - `callerEmail` — boolean — Include the caller email when known. Defaults to false.
        - `callerCompany` — boolean — Include the caller company when known. Defaults to false.
        - `time` — boolean — Include the current time, rendered in the agent's `engine.ai.timeZone`. Defaults to false.
    - `chat` — ChatChannelSettings
      - `discoverable` — boolean — Whether users can find and add this agent to conversations.
      - `sessionTimeoutMinutes` — number — Minutes a conversation can stay idle before the next message starts a new session. Omit to start a new session at the end of the agent's local day (`engine.ai.timeZone`). Allowed values: 15, 30, 60, 120. _(min=15; max=120)_
      - `verbosity` — string — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
    - `assistant` — AssistantChannelSettings — Assistant channel settings. Presence enables the in-app assistant surface; audio remains unavailable unless its separate settings are present and enabled.
      - `default` — boolean — Offer this agent as the default assistant for users covered by the agent access settings.
      - `ui` — AssistantUiSettings — How the agent presents itself in the assistant UI: what the user reads before typing anything, and what they can start from without typing at all. Everything here is presentation — it never changes what the agent can do.
        - `welcome` — AssistantWelcomeSettings — Greeting shown on an empty thread, above the quick commands.
          - `title` — string — Heading, e.g. 'How can I help?'. Rendered on one line. _(minLen=1; maxLen=80)_
          - `subtitle` — string — Line under the heading, saying what this agent is for, e.g. 'Ask about your conversations, accounts and calls.'. _(minLen=1; maxLen=200)_
        - `commands` — array — Cards offered under the welcome message on an empty thread, in the order given. Empty or omitted shows no cards. _(maxItems=8)_
          - _array of_ `AssistantQuickCommand`
            - `title` — string **(required)** — Card label, e.g. 'Summarize my day'. Rendered on one line and truncated when it does not fit. _(minLen=1; maxLen=60)_
            - `description` — string — Optional line under the label. Also one line, so keep it to a short clarification of what the command does. _(minLen=1; maxLen=120)_
            - `prompt` — string **(required)** — The message actually sent when the card is picked. Usually longer and more explicit than the label, since it is what the model reads. _(minLen=1; maxLen=2000)_
        - `placeholder` — string — Placeholder text in the composer, e.g. 'Ask about an account…'. Defaults to the client's own placeholder when omitted. _(minLen=1; maxLen=100)_
      - `audio` — AssistantAudioSettings — Switchable audio for the assistant channel. The settings object keeps enablement beside its speech policy, matching the voice channel's switchable blocks so a disabled configuration can be retained without serving audio.
        - `enabled` — boolean **(required)** — Whether the assistant accepts audio calls. Required so the presence of saved speech configuration is never mistaken for enablement.
        - `speech` — AssistantSpeechSettings — Recognition and synthesis policy for assistant audio. This is assistant-owned rather than a VoiceSpeechSettings reuse so telephony and assistant audio can evolve independently. It has no language greeting and no greet-every-language switch because an assistant conversation is already open when its audio call starts, leaving nothing for the channel to greet.
          - `languages` — array **(required)** — Languages the assistant audio channel can recognise and speak. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once — unlike the voice channel, where a caller opts into identification with `autoDetect`, THIS channel derives identification from `languages` and turns it on whenever the recogniser can identify among more than one, so every one of the up to ten rows here can become a live candidate list. The service does not clamp that list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five); a caller configuring more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. _(minItems=1; maxItems=10)_
            - _array of_ `AssistantLanguage`
              - _(nesting depth limit — see `AssistantLanguage` in the Schemas appendix)_
          - `transcription` — AssistantTranscriptionSettings — Speech-to-text configuration owned by the assistant channel, so changes to assistant recognition policy cannot alter telephony calls. NO `autoDetect` HERE, unlike the voice channel: on this channel configuring a second language IS the request to recognise which one is being spoken — nobody lists two and then asks to be heard in only one — so the server derives identification from the language list and clamps it to false when the recogniser cannot identify among them, or there are too few to identify. The voice channel keeps the switch because a dialplan can hand a call its language, which is a choice an assistant conversation never has to make.
            - `engine` — string — Recogniser used for assistant audio. Absent resolves to the platform default, resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
  - `engine` — union **(required)** — How the agent produces replies. `ai` is the managed engine; `webhook` and `sqs` delegate to an external backend.
    - _oneOf_ — exactly one of:
      - **`ai`**
        - `ai` — AgentAiEngine **(required)** — Managed AI engine: the platform runs the model, tools and knowledge lookups.
          - `instructions` — string **(required)** _(minLen=1; maxLen=60000)_
          - `workflow` — AgentWorkflow — The agent's conversation as a graph: which step runs first, what each step does, and on what condition control moves on. Optional on AgentAiEngine — without one the agent is prompt-driven, steered by `instructions` and free to use its capabilities in any order. Versioned with the rest of the agent definition: publishing a version snapshots the graph, and a draft edit reaches no session until it is published and routed.
            - `entry` — string **(required)** — Step the graph starts at. Must be one of `steps`. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
            - `steps` — array **(required)** — Steps of one graph. Ids are unique within it. _(minItems=1; maxItems=200)_
              - _array of_ `AgentWorkflowStep`
                - _(nesting depth limit — see `AgentWorkflowStep` in the Schemas appendix)_
            - `nested` — array — Graphs the main workflow can run, referenced by `workflow` steps.
              - _array of_ `AgentWorkflowNested`
                - _(nesting depth limit — see `AgentWorkflowNested` in the Schemas appendix)_
            - `settings` — AgentWorkflowSettings
              - `maxTransitions` — number — Give up after this many step transitions, so a cycle whose conditions all keep matching cannot run forever. Absent means no limit, which is the default: a deliberate loop — 'keep asking until you have the postcode' — is a normal shape, and silently capping it would be worse than making the author say so. _(min=1; max=500)_
              - `variables` — array — Workflow variables seeded before the first step runs. Agent input variables (`engine.ai.variables`) are already in scope and need no entry here.
                - _(nesting depth limit — see `AgentWorkflowAssignment` in the Schemas appendix)_
              - `layout` — string — How the builder arranges the graph. Authoring metadata: the runtime ignores it. `stages` bands the graph by `stage`, which is what a forty-step workflow needs. _(enum: `flow`, `compact`, `stages`)_
          - `guardrails` — AgentGuardrails — Turn screening, by side. Only `input` exists: it guards what reaches the model, and output screening is a separate policy with different actions, added here when it is built.
            - `input` — AgentGuardrailInput — Screening applied to what reaches the model. There is deliberately no bundle or preset-group member. A named group that expands to a set of checks reads like convenience and behaves like version skew: the same agent definition would mean different things before and after a platform release, invisibly to the tenant who published it. Listing the checks costs a few lines in a document the console writes anyway, and the published version then states exactly what it enforces. There is also no set-level default action. One field standing behind every check reads as a convenience and hides the thing a reader most needs to see: what a given check will actually do. A check's action is its own or its preset's, and both are visible on the check.
              - `checks` — array — The checks to run, evaluated together in one call. Absent or empty means no screening. _(maxItems=30)_
                - _(nesting depth limit — see `AgentGuardrailCheck` in the Schemas appendix)_
              - `model` — string — The model that runs the checks. Defaults to the platform's guardrail model — deliberately small and fast, and deliberately not the agent's own, whose cost and latency are what this exists to avoid spending on a bad turn. _(pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
              - `action` — union — What happens when a check trips. Exactly one member is set. Ordered by severity: observe < redact < block < end. When more than one check trips in the same call the most severe action wins and ties break on the order of `checks`, so a set can mix an observed check with an enforced one without the observation weakening the enforcement. There is no hand-over member yet. Handing a session to a human is a different mechanism on every channel — a voice transfer, a chat assignment, an assistant with no human behind it — and wiring a guardrail into all of them is out of proportion to the rest of this feature. Until AgentHandoverCapability has a runtime on more than one channel, the crisis path is a block whose message routes the caller.
                - _(nesting depth limit — see `AgentGuardrailAction` in the Schemas appendix)_
              - `mode` — string — Runs the checker before the agent's model (BLOCKING) or alongside it (PARALLEL). Blocking costs the checker's latency on every turn but guarantees that a refused turn spent no tokens and fired no tool; parallel adds no latency and is the right trade on voice, where the delay is audible, at the risk that part of a reply reaches the caller and that a tool has already run before the cancellation lands. Defaults to BLOCKING. _(enum: `blocking`, `parallel`)_
              - `errorMode` — string — What happens when the checker itself errors or times out. OPEN lets the turn through unscreened and records GuardrailFailedEvent, so an unscreened turn is a fact in the log rather than an absence; CLOSED refuses it. Defaults to OPEN: an agent that stops answering because a small model had a bad minute is a worse and far likelier outage than the rare turn that goes unscreened. Background tasks, where nobody is waiting and a retry is free, are the case for CLOSED. _(enum: `open`, `closed`)_
              - `window` — string — How much of the conversation the checker sees. Defaults to LAST_WITH_PRIOR, because the jailbreaks worth catching are built across several turns — establish a fiction, then cash it in — and a checker shown only the last turn sees an innocuous sentence. There is no full-transcript option: screening a whole call on every turn would make the guardrail dearer than the agent. _(enum: `lastMessage`, `lastWithPrior`)_
          - `model` — string — Defaults to the platform default model when omitted. _(pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
          - `timeZone` — string — IANA timezone the agent reasons about time in: it anchors the current date and time given to the model and how times are read from and written to tool arguments and replies. Shared by every channel the agent serves. Defaults to 'UTC'. _(minLen=1; maxLen=64)_
          - `artifacts` — boolean — Whether the agent can produce artifacts (wilma-artifacts): files it writes in its sandbox and shares back during a session — a document, a PDF, a spreadsheet, a chart, a multi-page web site, a folder of files. Needs the sandbox capability. An artifact starts private to the user the session runs for, who can share it company-wide from the viewer; on the chat channel the runtime shares each one company-wide as it is created, so the link posted into the conversation opens for every signed-in colleague. Artifacts are company-internal: recipients on external transports (sms / whatsapp) or outside the company cannot open the links, so keep this disabled for customer-facing agents. Defaults to false.
          - `skills` — array — Skills attached to this agent (progressive disclosure). A skill may carry its own tools, which join this agent's toolset while that skill is active.
            - _array of_ `AgentSkillReference`
              - `id` — string **(required)** _(minLen=12; maxLen=12)_
              - `skillVersion` — number — Pin a specific published skill version. When omitted, latestVersion is resolved. _(min=1)_
              - `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
                - _(nesting depth limit — see `AgentAccess` in the Schemas appendix)_
          - `capabilities` — array — Everything the agent can do. When a `workflow` is set these are the capabilities in scope at every step, and a step may add to them or narrow them with its own list of the same shape.
            - _array of_ `AgentCapability`
              - _oneOf_ — exactly one of:
                - **`tool`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`connector`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`kb`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`sandbox`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`webSearch`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`webFetch`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`agent`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`handover`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`delegation`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`transfer`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`suggestions`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`hangup`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`wait`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `variables` — array
            - _array of_ `AgentVariable`
              - `name` — string **(required)** _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
              - `type` — string **(required)** _(enum: `string`, `number`, `boolean`, `string_array`, `number_array`)_
              - `optional` — boolean **(required)**
              - `description` — string — What the variable means and how it should be filled.
      - **`webhook`**
        - `webhook` — AgentWebhookEngine **(required)** — Bring-your-own backend over HTTPS. The platform POSTs call events to the URL; the backend answers out of band through the channel's command API. The response body is not read.
          - `url` — string **(required)**
          - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
            - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
          - `timeout` — number — Timeout of one delivery, in milliseconds. _(default=10000; min=5000; max=120000)_
      - **`sqs`**
        - `sqs` — AgentSqsEngine **(required)** — Bring-your-own backend over SQS. The platform sends call events to the queue; the backend answers out of band through the channel's command API.
          - `url` — string **(required)**
          - `key` — string **(required)**
          - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
            - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `settings` — AgentSettings — Agent-level settings shared across all channels.
    - `pbxGroupId` — string — PBX group used for data ACL (e.g. Sales Intelligence lookups).
  - `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
    - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
    - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
      - _array of_ `AgentGrantPrincipal`
        - _oneOf_ — exactly one of:
          - **`userId`**
            - `userId` — string **(required)** _(minLen=12; maxLen=12)_
          - **`groupId`**
            - `groupId` — string **(required)**
          - **`department`**
            - `department` — string **(required)** — PBX department NAME, as carried on the colleague record (`PbxColleague.department`), not a department id. The x-bees directory knows a colleague's department only by name, so matching by name is what lets the check read a field the runtime already has instead of resolving the PBX department tree on every request. Two consequences: renaming a department in the PBX invalidates every grant naming it, and two departments with the same name in different branches of the tree are one value here.
- **Response 200** (`CreateAgentResponseContent`)
  - `agent` — Agent **(required)** — The complete, versionable configuration of an agent. This is what gets snapshotted when a version is published.
    - `name` — string **(required)** _(minLen=3; maxLen=255)_
    - `description` — string _(minLen=1; maxLen=1000)_
    - `category` — string — Category of the agent, e.g.: 'Support'. _(minLen=1; maxLen=128)_
    - `picture` — string — Avatar URL.
    - `channels` — AgentChannels **(required)** — The channels an agent serves and their channel-specific settings. Presence of a member enables that channel. Empty means the agent serves no channel: it is not reachable on its own and runs only as an automation's task or when another agent calls it. Enabled channels are mirrored as ChannelType values on AgentInfo.
      - `voice` — VoiceChannelSettings — Voice channel settings. Note: a voice agent's AgentAccess.grants are ignored — inbound calls are routed by the PBX dialplan and data ACL is the agent-level `settings.pbxGroupId`, not per-user grants.
        - `greeting` — string — Message spoken when the call starts.
        - `backgroundSound` — VoiceBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT like `interruptions` and `endCall`, rather than a loose name on the channel: it is one switchable call behaviour, it reads the same way as its siblings, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
          - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
          - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
        - `speech` — VoiceSpeechSettings — Speech configuration for the voice channel. When present it WINS over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the single exception, because it is the channel's own input signal and the feature has no starting point without it.
          - `languages` — array **(required)** — Configured languages. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once: automatic detection here is opt-in (`transcription.autoDetect`), and once a caller turns it on, the service does not clamp the resulting candidate list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five) — a caller who both opts in and configures more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. With detection off, only the single resolved language is ever sent, so the ceiling never becomes a candidate-list problem at all. _(minItems=1; maxItems=10)_
            - _array of_ `VoiceLanguage`
              - _(nesting depth limit — see `VoiceLanguage` in the Schemas appendix)_
          - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in the voice, provider account and pronunciation rules of its own language, instead of only the language the call resolved to. Languages whose first message is empty, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
          - `transcription` — VoiceTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
            - `engine` — string — Recogniser to transcribe the caller with. Absent resolves to the platform default ('aws://transcribe' today), resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
            - `autoDetect` — boolean — Identify the caller's language per utterance and switch voice and reply language mid-call. HERE RATHER THAN ON `VoiceSpeechSettings`, because identifying a language is something the RECOGNISER does: it becomes identify-multiple-languages plus language-options on the recognition stream, and nothing about synthesis reads it. Requires at least two configured languages and a recogniser that can identify them; the server clamps it to false otherwise, because forwarding true with a single candidate makes Amazon reject the stream outright.
        - `interruptions` — VoiceInterruptionSettings
          - `enabled` — boolean **(required)** — Whether the caller can interrupt the agent while it is speaking.
          - `minWords` — number — Minimum number of caller words that count as an interruption. _(min=1; max=10)_
        - `silenceTimeout` — VoiceSilenceTimeoutSettings
          - `seconds` — number **(required)** — Seconds of caller silence before the action is taken. _(min=1; max=600)_
          - `action` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`hangup`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`transfer`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `maxDuration` — VoiceMaxDurationSettings
          - `seconds` — number **(required)** — Maximum call duration in seconds before the action is taken. _(min=10; max=14400)_
          - `action` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`hangup`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`transfer`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `endCall` — VoiceEndCallSettings
          - `enabled` — boolean **(required)**
          - `phrases` — string — Comma-separated phrases that end the call, e.g. 'goodbye,bye'.
        - `callerMetadata` — VoiceCallerMetadataSettings — Caller context injected into the model prompt.
          - `callerName` — boolean — Include the caller name. Defaults to true.
          - `callerNumber` — boolean — Include the caller phone number. Defaults to true.
          - `callerEmail` — boolean — Include the caller email when known. Defaults to false.
          - `callerCompany` — boolean — Include the caller company when known. Defaults to false.
          - `time` — boolean — Include the current time, rendered in the agent's `engine.ai.timeZone`. Defaults to false.
      - `chat` — ChatChannelSettings
        - `discoverable` — boolean — Whether users can find and add this agent to conversations.
        - `sessionTimeoutMinutes` — number — Minutes a conversation can stay idle before the next message starts a new session. Omit to start a new session at the end of the agent's local day (`engine.ai.timeZone`). Allowed values: 15, 30, 60, 120. _(min=15; max=120)_
        - `verbosity` — string — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
      - `assistant` — AssistantChannelSettings — Assistant channel settings. Presence enables the in-app assistant surface; audio remains unavailable unless its separate settings are present and enabled.
        - `default` — boolean — Offer this agent as the default assistant for users covered by the agent access settings.
        - `ui` — AssistantUiSettings — How the agent presents itself in the assistant UI: what the user reads before typing anything, and what they can start from without typing at all. Everything here is presentation — it never changes what the agent can do.
          - `welcome` — AssistantWelcomeSettings — Greeting shown on an empty thread, above the quick commands.
            - `title` — string — Heading, e.g. 'How can I help?'. Rendered on one line. _(minLen=1; maxLen=80)_
            - `subtitle` — string — Line under the heading, saying what this agent is for, e.g. 'Ask about your conversations, accounts and calls.'. _(minLen=1; maxLen=200)_
          - `commands` — array — Cards offered under the welcome message on an empty thread, in the order given. Empty or omitted shows no cards. _(maxItems=8)_
            - _array of_ `AssistantQuickCommand`
              - _(nesting depth limit — see `AssistantQuickCommand` in the Schemas appendix)_
          - `placeholder` — string — Placeholder text in the composer, e.g. 'Ask about an account…'. Defaults to the client's own placeholder when omitted. _(minLen=1; maxLen=100)_
        - `audio` — AssistantAudioSettings — Switchable audio for the assistant channel. The settings object keeps enablement beside its speech policy, matching the voice channel's switchable blocks so a disabled configuration can be retained without serving audio.
          - `enabled` — boolean **(required)** — Whether the assistant accepts audio calls. Required so the presence of saved speech configuration is never mistaken for enablement.
          - `speech` — AssistantSpeechSettings — Recognition and synthesis policy for assistant audio. This is assistant-owned rather than a VoiceSpeechSettings reuse so telephony and assistant audio can evolve independently. It has no language greeting and no greet-every-language switch because an assistant conversation is already open when its audio call starts, leaving nothing for the channel to greet.
            - `languages` — array **(required)** — Languages the assistant audio channel can recognise and speak. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once — unlike the voice channel, where a caller opts into identification with `autoDetect`, THIS channel derives identification from `languages` and turns it on whenever the recogniser can identify among more than one, so every one of the up to ten rows here can become a live candidate list. The service does not clamp that list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five); a caller configuring more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. _(minItems=1; maxItems=10)_
              - _(nesting depth limit — see `AssistantLanguage` in the Schemas appendix)_
            - `transcription` — AssistantTranscriptionSettings — Speech-to-text configuration owned by the assistant channel, so changes to assistant recognition policy cannot alter telephony calls. NO `autoDetect` HERE, unlike the voice channel: on this channel configuring a second language IS the request to recognise which one is being spoken — nobody lists two and then asks to be heard in only one — so the server derives identification from the language list and clamps it to false when the recogniser cannot identify among them, or there are too few to identify. The voice channel keeps the switch because a dialplan can hand a call its language, which is a choice an assistant conversation never has to make.
              - _(nesting depth limit — see `AssistantTranscriptionSettings` in the Schemas appendix)_
    - `engine` — union **(required)** — How the agent produces replies. `ai` is the managed engine; `webhook` and `sqs` delegate to an external backend.
      - _oneOf_ — exactly one of:
        - **`ai`**
          - `ai` — AgentAiEngine **(required)** — Managed AI engine: the platform runs the model, tools and knowledge lookups.
            - `instructions` — string **(required)** _(minLen=1; maxLen=60000)_
            - `workflow` — AgentWorkflow — The agent's conversation as a graph: which step runs first, what each step does, and on what condition control moves on. Optional on AgentAiEngine — without one the agent is prompt-driven, steered by `instructions` and free to use its capabilities in any order. Versioned with the rest of the agent definition: publishing a version snapshots the graph, and a draft edit reaches no session until it is published and routed.
              - `entry` — string **(required)** — Step the graph starts at. Must be one of `steps`. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
              - `steps` — array **(required)** — Steps of one graph. Ids are unique within it. _(minItems=1; maxItems=200)_
                - _(nesting depth limit — see `AgentWorkflowStep` in the Schemas appendix)_
              - `nested` — array — Graphs the main workflow can run, referenced by `workflow` steps.
                - _(nesting depth limit — see `AgentWorkflowNested` in the Schemas appendix)_
              - `settings` — AgentWorkflowSettings
                - _(nesting depth limit — see `AgentWorkflowSettings` in the Schemas appendix)_
            - `guardrails` — AgentGuardrails — Turn screening, by side. Only `input` exists: it guards what reaches the model, and output screening is a separate policy with different actions, added here when it is built.
              - `input` — AgentGuardrailInput — Screening applied to what reaches the model. There is deliberately no bundle or preset-group member. A named group that expands to a set of checks reads like convenience and behaves like version skew: the same agent definition would mean different things before and after a platform release, invisibly to the tenant who published it. Listing the checks costs a few lines in a document the console writes anyway, and the published version then states exactly what it enforces. There is also no set-level default action. One field standing behind every check reads as a convenience and hides the thing a reader most needs to see: what a given check will actually do. A check's action is its own or its preset's, and both are visible on the check.
                - _(nesting depth limit — see `AgentGuardrailInput` in the Schemas appendix)_
            - `model` — string — Defaults to the platform default model when omitted. _(pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
            - `timeZone` — string — IANA timezone the agent reasons about time in: it anchors the current date and time given to the model and how times are read from and written to tool arguments and replies. Shared by every channel the agent serves. Defaults to 'UTC'. _(minLen=1; maxLen=64)_
            - `artifacts` — boolean — Whether the agent can produce artifacts (wilma-artifacts): files it writes in its sandbox and shares back during a session — a document, a PDF, a spreadsheet, a chart, a multi-page web site, a folder of files. Needs the sandbox capability. An artifact starts private to the user the session runs for, who can share it company-wide from the viewer; on the chat channel the runtime shares each one company-wide as it is created, so the link posted into the conversation opens for every signed-in colleague. Artifacts are company-internal: recipients on external transports (sms / whatsapp) or outside the company cannot open the links, so keep this disabled for customer-facing agents. Defaults to false.
            - `skills` — array — Skills attached to this agent (progressive disclosure). A skill may carry its own tools, which join this agent's toolset while that skill is active.
              - _array of_ `AgentSkillReference`
                - _(nesting depth limit — see `AgentSkillReference` in the Schemas appendix)_
            - `capabilities` — array — Everything the agent can do. When a `workflow` is set these are the capabilities in scope at every step, and a step may add to them or narrow them with its own list of the same shape.
              - _array of_ `AgentCapability`
                - _(nesting depth limit — see `AgentCapability` in the Schemas appendix)_
            - `variables` — array
              - _array of_ `AgentVariable`
                - _(nesting depth limit — see `AgentVariable` in the Schemas appendix)_
        - **`webhook`**
          - `webhook` — AgentWebhookEngine **(required)** — Bring-your-own backend over HTTPS. The platform POSTs call events to the URL; the backend answers out of band through the channel's command API. The response body is not read.
            - `url` — string **(required)**
            - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
              - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
            - `timeout` — number — Timeout of one delivery, in milliseconds. _(default=10000; min=5000; max=120000)_
        - **`sqs`**
          - `sqs` — AgentSqsEngine **(required)** — Bring-your-own backend over SQS. The platform sends call events to the queue; the backend answers out of band through the channel's command API.
            - `url` — string **(required)**
            - `key` — string **(required)**
            - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
              - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
    - `settings` — AgentSettings — Agent-level settings shared across all channels.
      - `pbxGroupId` — string — PBX group used for data ACL (e.g. Sales Intelligence lookups).
    - `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
      - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
      - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
        - _array of_ `AgentGrantPrincipal`
          - _oneOf_ — exactly one of:
            - **`userId`**
              - `userId` — string **(required)** _(minLen=12; maxLen=12)_
            - **`groupId`**
              - `groupId` — string **(required)**
            - **`department`**
              - `department` — string **(required)** — PBX department NAME, as carried on the colleague record (`PbxColleague.department`), not a department id. The x-bees directory knows a colleague's department only by name, so matching by name is what lets the check read a field the runtime already has instead of resolving the PBX department tree on every request. Two consequences: renaming a department in the PBX invalidates every grant naming it, and two departments with the same name in different branches of the tree are one value here.
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
    - `updatedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `updatedBy` — Actor — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
    - `latestVersion` — number — Latest published version number; absent while the agent is still a draft. _(min=1)_
    - `draftBaseVersion` — number — Published version number from which the current draft originated. Absent before the first version is published. _(min=1)_
    - `deployment` — array — How new sessions are split across published versions. Absent while the agent is still a draft. _(minItems=1; maxItems=10)_
      - _array of_ `AgentDeploymentRoute`
        - `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
        - `percentage` — number **(required)** — Percentage of new sessions routed to this version. Percentages must sum to 100. _(min=1; max=100)_
- Errors: `400`, `409`

#### `GET` `/v2/agents/agents-names`

Retrieves a lightweight list of agent names and basic information for the specified company.

- operationId: `ListAgentsNames`
- **Scopes**: `wilma-agents:ListAgentsNames`, `wilma-agents:read`
- **Parameters**
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `channel` (query) — string — A channel an agent can serve (see AgentChannels for enablement). Also the runtime channel recorded by the channel runtimes / wilma-traces. A background task has no delivery surface and therefore no channel. _(enum: `voice`, `chat`, `assistant`)_
- **Response 200** (`ListAgentsNamesResponseContent`)
  - `agents` — array **(required)**
    - _array of_ `AgentInfo`
      - `id` — string **(required)** _(minLen=12; maxLen=12)_
      - `name` — string **(required)** _(minLen=3; maxLen=255)_
      - `picture` — string — Avatar URL, from the agent definition.
      - `category` — string _(minLen=1; maxLen=128)_
      - `status` — string **(required)** _(enum: `draft`, `active`)_
      - `channels` — array **(required)** — The channels this agent serves (voice / chat / assistant). Empty for an agent that serves none — one only an automation runs or another agent calls.
        - _array of_ `ChannelType`
      - `speechConfigured` — boolean — Whether the voice channel has at least one configured speech language. A dialplan form partitions its application lists on this, so the answer has to travel with the list rather than cost one lookup per entry — it is the reason this member exists and the reason removing it broke that form. Absent is read as false.
      - `engine` — string — Which member of AgentEngine an agent carries, without the engine's configuration. _(enum: `ai`, `webhook`, `sqs`)_
      - `assistantVoice` — AssistantVoiceSettings — End-user view of an agent's assistant voice. New end-user voice parameters are added here rather than as AgentInfo members.
        - `enabled` — boolean **(required)** — Whether a client should offer a voice call. True only when the definition the agent currently runs has assistant audio enabled and configured (`channels.assistant.audio.enabled` with at least one speech language); audio that is not configured counts as disabled. For a deployment that splits traffic, every routed version must qualify, so the answer holds whichever version a call lands on.
      - `skillIds` — array — Ids of the skills attached to this agent. Always active in this agent's sessions; user skill preferences cannot disable them.
        - _array of_ `string`
      - `connectorIds` — array — Ids of the connector instances attached to this agent, in capability order — the order an administrator sees on the agent's capabilities page. This is how a client knows which of the connectors in the assistant's settings catalogue this agent can call: filter that catalogue by these ids.
        - _array of_ `string`
      - `assistant` — AssistantUiSettings — How the agent presents itself in the assistant UI: what the user reads before typing anything, and what they can start from without typing at all. Everything here is presentation — it never changes what the agent can do.
        - `welcome` — AssistantWelcomeSettings — Greeting shown on an empty thread, above the quick commands.
          - `title` — string — Heading, e.g. 'How can I help?'. Rendered on one line. _(minLen=1; maxLen=80)_
          - `subtitle` — string — Line under the heading, saying what this agent is for, e.g. 'Ask about your conversations, accounts and calls.'. _(minLen=1; maxLen=200)_
        - `commands` — array — Cards offered under the welcome message on an empty thread, in the order given. Empty or omitted shows no cards. _(maxItems=8)_
          - _array of_ `AssistantQuickCommand`
            - `title` — string **(required)** — Card label, e.g. 'Summarize my day'. Rendered on one line and truncated when it does not fit. _(minLen=1; maxLen=60)_
            - `description` — string — Optional line under the label. Also one line, so keep it to a short clarification of what the command does. _(minLen=1; maxLen=120)_
            - `prompt` — string **(required)** — The message actually sent when the card is picked. Usually longer and more explicit than the label, since it is what the model reads. _(minLen=1; maxLen=2000)_
        - `placeholder` — string — Placeholder text in the composer, e.g. 'Ask about an account…'. Defaults to the client's own placeholder when omitted. _(minLen=1; maxLen=100)_
      - `latestVersion` — number — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
- Errors: `400`

#### `GET` `/v2/agents/agents/{agentId}`

Retrieves an agent, including its draft definition and version/rollout state.

- operationId: `GetAgent`
- **Scopes**: `wilma-agents:GetAgent`, `wilma-agents:read`
- **Parameters**
  - `agentId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Response 200** (`GetAgentResponseContent`)
  - `agent` — Agent **(required)** — The complete, versionable configuration of an agent. This is what gets snapshotted when a version is published.
    - `name` — string **(required)** _(minLen=3; maxLen=255)_
    - `description` — string _(minLen=1; maxLen=1000)_
    - `category` — string — Category of the agent, e.g.: 'Support'. _(minLen=1; maxLen=128)_
    - `picture` — string — Avatar URL.
    - `channels` — AgentChannels **(required)** — The channels an agent serves and their channel-specific settings. Presence of a member enables that channel. Empty means the agent serves no channel: it is not reachable on its own and runs only as an automation's task or when another agent calls it. Enabled channels are mirrored as ChannelType values on AgentInfo.
      - `voice` — VoiceChannelSettings — Voice channel settings. Note: a voice agent's AgentAccess.grants are ignored — inbound calls are routed by the PBX dialplan and data ACL is the agent-level `settings.pbxGroupId`, not per-user grants.
        - `greeting` — string — Message spoken when the call starts.
        - `backgroundSound` — VoiceBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT like `interruptions` and `endCall`, rather than a loose name on the channel: it is one switchable call behaviour, it reads the same way as its siblings, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
          - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
          - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
        - `speech` — VoiceSpeechSettings — Speech configuration for the voice channel. When present it WINS over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the single exception, because it is the channel's own input signal and the feature has no starting point without it.
          - `languages` — array **(required)** — Configured languages. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once: automatic detection here is opt-in (`transcription.autoDetect`), and once a caller turns it on, the service does not clamp the resulting candidate list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five) — a caller who both opts in and configures more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. With detection off, only the single resolved language is ever sent, so the ceiling never becomes a candidate-list problem at all. _(minItems=1; maxItems=10)_
            - _array of_ `VoiceLanguage`
              - _(nesting depth limit — see `VoiceLanguage` in the Schemas appendix)_
          - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in the voice, provider account and pronunciation rules of its own language, instead of only the language the call resolved to. Languages whose first message is empty, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
          - `transcription` — VoiceTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
            - `engine` — string — Recogniser to transcribe the caller with. Absent resolves to the platform default ('aws://transcribe' today), resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
            - `autoDetect` — boolean — Identify the caller's language per utterance and switch voice and reply language mid-call. HERE RATHER THAN ON `VoiceSpeechSettings`, because identifying a language is something the RECOGNISER does: it becomes identify-multiple-languages plus language-options on the recognition stream, and nothing about synthesis reads it. Requires at least two configured languages and a recogniser that can identify them; the server clamps it to false otherwise, because forwarding true with a single candidate makes Amazon reject the stream outright.
        - `interruptions` — VoiceInterruptionSettings
          - `enabled` — boolean **(required)** — Whether the caller can interrupt the agent while it is speaking.
          - `minWords` — number — Minimum number of caller words that count as an interruption. _(min=1; max=10)_
        - `silenceTimeout` — VoiceSilenceTimeoutSettings
          - `seconds` — number **(required)** — Seconds of caller silence before the action is taken. _(min=1; max=600)_
          - `action` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`hangup`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`transfer`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `maxDuration` — VoiceMaxDurationSettings
          - `seconds` — number **(required)** — Maximum call duration in seconds before the action is taken. _(min=10; max=14400)_
          - `action` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`hangup`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`transfer`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `endCall` — VoiceEndCallSettings
          - `enabled` — boolean **(required)**
          - `phrases` — string — Comma-separated phrases that end the call, e.g. 'goodbye,bye'.
        - `callerMetadata` — VoiceCallerMetadataSettings — Caller context injected into the model prompt.
          - `callerName` — boolean — Include the caller name. Defaults to true.
          - `callerNumber` — boolean — Include the caller phone number. Defaults to true.
          - `callerEmail` — boolean — Include the caller email when known. Defaults to false.
          - `callerCompany` — boolean — Include the caller company when known. Defaults to false.
          - `time` — boolean — Include the current time, rendered in the agent's `engine.ai.timeZone`. Defaults to false.
      - `chat` — ChatChannelSettings
        - `discoverable` — boolean — Whether users can find and add this agent to conversations.
        - `sessionTimeoutMinutes` — number — Minutes a conversation can stay idle before the next message starts a new session. Omit to start a new session at the end of the agent's local day (`engine.ai.timeZone`). Allowed values: 15, 30, 60, 120. _(min=15; max=120)_
        - `verbosity` — string — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
      - `assistant` — AssistantChannelSettings — Assistant channel settings. Presence enables the in-app assistant surface; audio remains unavailable unless its separate settings are present and enabled.
        - `default` — boolean — Offer this agent as the default assistant for users covered by the agent access settings.
        - `ui` — AssistantUiSettings — How the agent presents itself in the assistant UI: what the user reads before typing anything, and what they can start from without typing at all. Everything here is presentation — it never changes what the agent can do.
          - `welcome` — AssistantWelcomeSettings — Greeting shown on an empty thread, above the quick commands.
            - `title` — string — Heading, e.g. 'How can I help?'. Rendered on one line. _(minLen=1; maxLen=80)_
            - `subtitle` — string — Line under the heading, saying what this agent is for, e.g. 'Ask about your conversations, accounts and calls.'. _(minLen=1; maxLen=200)_
          - `commands` — array — Cards offered under the welcome message on an empty thread, in the order given. Empty or omitted shows no cards. _(maxItems=8)_
            - _array of_ `AssistantQuickCommand`
              - _(nesting depth limit — see `AssistantQuickCommand` in the Schemas appendix)_
          - `placeholder` — string — Placeholder text in the composer, e.g. 'Ask about an account…'. Defaults to the client's own placeholder when omitted. _(minLen=1; maxLen=100)_
        - `audio` — AssistantAudioSettings — Switchable audio for the assistant channel. The settings object keeps enablement beside its speech policy, matching the voice channel's switchable blocks so a disabled configuration can be retained without serving audio.
          - `enabled` — boolean **(required)** — Whether the assistant accepts audio calls. Required so the presence of saved speech configuration is never mistaken for enablement.
          - `speech` — AssistantSpeechSettings — Recognition and synthesis policy for assistant audio. This is assistant-owned rather than a VoiceSpeechSettings reuse so telephony and assistant audio can evolve independently. It has no language greeting and no greet-every-language switch because an assistant conversation is already open when its audio call starts, leaving nothing for the channel to greet.
            - `languages` — array **(required)** — Languages the assistant audio channel can recognise and speak. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once — unlike the voice channel, where a caller opts into identification with `autoDetect`, THIS channel derives identification from `languages` and turns it on whenever the recogniser can identify among more than one, so every one of the up to ten rows here can become a live candidate list. The service does not clamp that list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five); a caller configuring more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. _(minItems=1; maxItems=10)_
              - _(nesting depth limit — see `AssistantLanguage` in the Schemas appendix)_
            - `transcription` — AssistantTranscriptionSettings — Speech-to-text configuration owned by the assistant channel, so changes to assistant recognition policy cannot alter telephony calls. NO `autoDetect` HERE, unlike the voice channel: on this channel configuring a second language IS the request to recognise which one is being spoken — nobody lists two and then asks to be heard in only one — so the server derives identification from the language list and clamps it to false when the recogniser cannot identify among them, or there are too few to identify. The voice channel keeps the switch because a dialplan can hand a call its language, which is a choice an assistant conversation never has to make.
              - _(nesting depth limit — see `AssistantTranscriptionSettings` in the Schemas appendix)_
    - `engine` — union **(required)** — How the agent produces replies. `ai` is the managed engine; `webhook` and `sqs` delegate to an external backend.
      - _oneOf_ — exactly one of:
        - **`ai`**
          - `ai` — AgentAiEngine **(required)** — Managed AI engine: the platform runs the model, tools and knowledge lookups.
            - `instructions` — string **(required)** _(minLen=1; maxLen=60000)_
            - `workflow` — AgentWorkflow — The agent's conversation as a graph: which step runs first, what each step does, and on what condition control moves on. Optional on AgentAiEngine — without one the agent is prompt-driven, steered by `instructions` and free to use its capabilities in any order. Versioned with the rest of the agent definition: publishing a version snapshots the graph, and a draft edit reaches no session until it is published and routed.
              - `entry` — string **(required)** — Step the graph starts at. Must be one of `steps`. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
              - `steps` — array **(required)** — Steps of one graph. Ids are unique within it. _(minItems=1; maxItems=200)_
                - _(nesting depth limit — see `AgentWorkflowStep` in the Schemas appendix)_
              - `nested` — array — Graphs the main workflow can run, referenced by `workflow` steps.
                - _(nesting depth limit — see `AgentWorkflowNested` in the Schemas appendix)_
              - `settings` — AgentWorkflowSettings
                - _(nesting depth limit — see `AgentWorkflowSettings` in the Schemas appendix)_
            - `guardrails` — AgentGuardrails — Turn screening, by side. Only `input` exists: it guards what reaches the model, and output screening is a separate policy with different actions, added here when it is built.
              - `input` — AgentGuardrailInput — Screening applied to what reaches the model. There is deliberately no bundle or preset-group member. A named group that expands to a set of checks reads like convenience and behaves like version skew: the same agent definition would mean different things before and after a platform release, invisibly to the tenant who published it. Listing the checks costs a few lines in a document the console writes anyway, and the published version then states exactly what it enforces. There is also no set-level default action. One field standing behind every check reads as a convenience and hides the thing a reader most needs to see: what a given check will actually do. A check's action is its own or its preset's, and both are visible on the check.
                - _(nesting depth limit — see `AgentGuardrailInput` in the Schemas appendix)_
            - `model` — string — Defaults to the platform default model when omitted. _(pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
            - `timeZone` — string — IANA timezone the agent reasons about time in: it anchors the current date and time given to the model and how times are read from and written to tool arguments and replies. Shared by every channel the agent serves. Defaults to 'UTC'. _(minLen=1; maxLen=64)_
            - `artifacts` — boolean — Whether the agent can produce artifacts (wilma-artifacts): files it writes in its sandbox and shares back during a session — a document, a PDF, a spreadsheet, a chart, a multi-page web site, a folder of files. Needs the sandbox capability. An artifact starts private to the user the session runs for, who can share it company-wide from the viewer; on the chat channel the runtime shares each one company-wide as it is created, so the link posted into the conversation opens for every signed-in colleague. Artifacts are company-internal: recipients on external transports (sms / whatsapp) or outside the company cannot open the links, so keep this disabled for customer-facing agents. Defaults to false.
            - `skills` — array — Skills attached to this agent (progressive disclosure). A skill may carry its own tools, which join this agent's toolset while that skill is active.
              - _array of_ `AgentSkillReference`
                - _(nesting depth limit — see `AgentSkillReference` in the Schemas appendix)_
            - `capabilities` — array — Everything the agent can do. When a `workflow` is set these are the capabilities in scope at every step, and a step may add to them or narrow them with its own list of the same shape.
              - _array of_ `AgentCapability`
                - _(nesting depth limit — see `AgentCapability` in the Schemas appendix)_
            - `variables` — array
              - _array of_ `AgentVariable`
                - _(nesting depth limit — see `AgentVariable` in the Schemas appendix)_
        - **`webhook`**
          - `webhook` — AgentWebhookEngine **(required)** — Bring-your-own backend over HTTPS. The platform POSTs call events to the URL; the backend answers out of band through the channel's command API. The response body is not read.
            - `url` — string **(required)**
            - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
              - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
            - `timeout` — number — Timeout of one delivery, in milliseconds. _(default=10000; min=5000; max=120000)_
        - **`sqs`**
          - `sqs` — AgentSqsEngine **(required)** — Bring-your-own backend over SQS. The platform sends call events to the queue; the backend answers out of band through the channel's command API.
            - `url` — string **(required)**
            - `key` — string **(required)**
            - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
              - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
    - `settings` — AgentSettings — Agent-level settings shared across all channels.
      - `pbxGroupId` — string — PBX group used for data ACL (e.g. Sales Intelligence lookups).
    - `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
      - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
      - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
        - _array of_ `AgentGrantPrincipal`
          - _oneOf_ — exactly one of:
            - **`userId`**
              - `userId` — string **(required)** _(minLen=12; maxLen=12)_
            - **`groupId`**
              - `groupId` — string **(required)**
            - **`department`**
              - `department` — string **(required)** — PBX department NAME, as carried on the colleague record (`PbxColleague.department`), not a department id. The x-bees directory knows a colleague's department only by name, so matching by name is what lets the check read a field the runtime already has instead of resolving the PBX department tree on every request. Two consequences: renaming a department in the PBX invalidates every grant naming it, and two departments with the same name in different branches of the tree are one value here.
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
    - `updatedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `updatedBy` — Actor — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
    - `latestVersion` — number — Latest published version number; absent while the agent is still a draft. _(min=1)_
    - `draftBaseVersion` — number — Published version number from which the current draft originated. Absent before the first version is published. _(min=1)_
    - `deployment` — array — How new sessions are split across published versions. Absent while the agent is still a draft. _(minItems=1; maxItems=10)_
      - _array of_ `AgentDeploymentRoute`
        - `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
        - `percentage` — number **(required)** — Percentage of new sessions routed to this version. Percentages must sum to 100. _(min=1; max=100)_
- Errors: `400`, `404`

#### `PUT` `/v2/agents/agents/{agentId}`

Updates the draft definition of an agent. Does not affect served traffic until the draft is published.

- operationId: `UpdateAgent`
- **Scopes**: `wilma-agents:UpdateAgent`
- **Parameters**
  - `agentId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `UpdateAgentRequestContent`) **(required)**
  - `name` — string **(required)** _(minLen=3; maxLen=255)_
  - `description` — string _(minLen=1; maxLen=1000)_
  - `category` — string — Category of the agent, e.g.: 'Support'. _(minLen=1; maxLen=128)_
  - `picture` — string — Avatar URL.
  - `channels` — AgentChannels **(required)** — The channels an agent serves and their channel-specific settings. Presence of a member enables that channel. Empty means the agent serves no channel: it is not reachable on its own and runs only as an automation's task or when another agent calls it. Enabled channels are mirrored as ChannelType values on AgentInfo.
    - `voice` — VoiceChannelSettings — Voice channel settings. Note: a voice agent's AgentAccess.grants are ignored — inbound calls are routed by the PBX dialplan and data ACL is the agent-level `settings.pbxGroupId`, not per-user grants.
      - `greeting` — string — Message spoken when the call starts.
      - `backgroundSound` — VoiceBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT like `interruptions` and `endCall`, rather than a loose name on the channel: it is one switchable call behaviour, it reads the same way as its siblings, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
        - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
        - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
      - `speech` — VoiceSpeechSettings — Speech configuration for the voice channel. When present it WINS over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the single exception, because it is the channel's own input signal and the feature has no starting point without it.
        - `languages` — array **(required)** — Configured languages. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once: automatic detection here is opt-in (`transcription.autoDetect`), and once a caller turns it on, the service does not clamp the resulting candidate list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five) — a caller who both opts in and configures more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. With detection off, only the single resolved language is ever sent, so the ceiling never becomes a candidate-list problem at all. _(minItems=1; maxItems=10)_
          - _array of_ `VoiceLanguage`
            - `code` — string **(required)** — BCP-47 code with locale, e.g. 'en-US', 'it-IT'. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
            - `voice` — string **(required)** — Voice this language speaks with, as a URI — provider, voice id, synthesis parameters and, where the company uses its own provider account, an `apiKey=secrets:{secretId}` reference. See VoiceUri. PER LANGUAGE, and that is the whole reason the member is here rather than on the settings above: provider quality is not uniform across languages, a voice id belongs to exactly one provider, and a bot-wide provider made changing it invalidate every configured voice at once. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
            - `greeting` — string — Initial phrase spoken when the call starts in this language. Absent or empty means the agent says nothing and waits — it does NOT fall back to VoiceChannelSettings.greeting, which would speak one language's text in another language's voice.
            - `isDefault` — boolean — Marks the language a caller hears when their own matches nothing configured. THE FULL RESOLUTION ORDER, since a client author reading only this contract cannot otherwise find it: an exact match on the call's language, then a match on its primary subtag (`fr` finds `fr-FR`), then the language marked here, then a language whose primary subtag is `en`, then the first entry in the list. Marked is consulted BEFORE the English step, so a record with none marked resolves exactly as it did before this member existed. English is deliberate rather than arbitrary — it is the language a caller the agent was not built for is likeliest to understand — and the last step exists only to keep the rule total, which is why list order should not be treated as configuration. At most one language may carry it. A record with two — reachable through the API or the CLI, where no form prevents it — resolves to the first marked one in list order, because refusing a call over configuration drift is worse than serving it and saying so in the trace.
            - `pronunciations` — array — The rules this language is spoken with. THE WHOLE SET rather than an override layer: an agent's respellings are stored here and read from here, so what this list says is what the caller hears. THERE IS NOTHING ABOVE IT. An earlier draft of this contract carried a company-wide dictionary per language that every agent speaking it inherited, with a merge order over this member and an identity rule ('Wildix' -> 'Wildix') for declining an inherited respelling. It bought correcting a handful of names in one place, and cost a second store, a merge on every synthesis path, a screen of its own, and a reader who could not tell from an agent what that agent would actually say. Per language per agent is where the divergence that matters already lives. _(maxItems=200)_
              - _(nesting depth limit — see `VoicePronunciation` in the Schemas appendix)_
        - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in the voice, provider account and pronunciation rules of its own language, instead of only the language the call resolved to. Languages whose first message is empty, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
        - `transcription` — VoiceTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
          - `engine` — string — Recogniser to transcribe the caller with. Absent resolves to the platform default ('aws://transcribe' today), resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
          - `autoDetect` — boolean — Identify the caller's language per utterance and switch voice and reply language mid-call. HERE RATHER THAN ON `VoiceSpeechSettings`, because identifying a language is something the RECOGNISER does: it becomes identify-multiple-languages plus language-options on the recognition stream, and nothing about synthesis reads it. Requires at least two configured languages and a recogniser that can identify them; the server clamps it to false otherwise, because forwarding true with a single candidate makes Amazon reject the stream outright.
      - `interruptions` — VoiceInterruptionSettings
        - `enabled` — boolean **(required)** — Whether the caller can interrupt the agent while it is speaking.
        - `minWords` — number — Minimum number of caller words that count as an interruption. _(min=1; max=10)_
      - `silenceTimeout` — VoiceSilenceTimeoutSettings
        - `seconds` — number **(required)** — Seconds of caller silence before the action is taken. _(min=1; max=600)_
        - `action` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`hangup`**
              - `hangup` — VoiceTerminateHangupAction **(required)**
                - _(nesting depth limit — see `VoiceTerminateHangupAction` in the Schemas appendix)_
            - **`transfer`**
              - `transfer` — VoiceTransferTarget **(required)**
                - _(nesting depth limit — see `VoiceTransferTarget` in the Schemas appendix)_
      - `maxDuration` — VoiceMaxDurationSettings
        - `seconds` — number **(required)** — Maximum call duration in seconds before the action is taken. _(min=10; max=14400)_
        - `action` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`hangup`**
              - `hangup` — VoiceTerminateHangupAction **(required)**
                - _(nesting depth limit — see `VoiceTerminateHangupAction` in the Schemas appendix)_
            - **`transfer`**
              - `transfer` — VoiceTransferTarget **(required)**
                - _(nesting depth limit — see `VoiceTransferTarget` in the Schemas appendix)_
      - `endCall` — VoiceEndCallSettings
        - `enabled` — boolean **(required)**
        - `phrases` — string — Comma-separated phrases that end the call, e.g. 'goodbye,bye'.
      - `callerMetadata` — VoiceCallerMetadataSettings — Caller context injected into the model prompt.
        - `callerName` — boolean — Include the caller name. Defaults to true.
        - `callerNumber` — boolean — Include the caller phone number. Defaults to true.
        - `callerEmail` — boolean — Include the caller email when known. Defaults to false.
        - `callerCompany` — boolean — Include the caller company when known. Defaults to false.
        - `time` — boolean — Include the current time, rendered in the agent's `engine.ai.timeZone`. Defaults to false.
    - `chat` — ChatChannelSettings
      - `discoverable` — boolean — Whether users can find and add this agent to conversations.
      - `sessionTimeoutMinutes` — number — Minutes a conversation can stay idle before the next message starts a new session. Omit to start a new session at the end of the agent's local day (`engine.ai.timeZone`). Allowed values: 15, 30, 60, 120. _(min=15; max=120)_
      - `verbosity` — string — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
    - `assistant` — AssistantChannelSettings — Assistant channel settings. Presence enables the in-app assistant surface; audio remains unavailable unless its separate settings are present and enabled.
      - `default` — boolean — Offer this agent as the default assistant for users covered by the agent access settings.
      - `ui` — AssistantUiSettings — How the agent presents itself in the assistant UI: what the user reads before typing anything, and what they can start from without typing at all. Everything here is presentation — it never changes what the agent can do.
        - `welcome` — AssistantWelcomeSettings — Greeting shown on an empty thread, above the quick commands.
          - `title` — string — Heading, e.g. 'How can I help?'. Rendered on one line. _(minLen=1; maxLen=80)_
          - `subtitle` — string — Line under the heading, saying what this agent is for, e.g. 'Ask about your conversations, accounts and calls.'. _(minLen=1; maxLen=200)_
        - `commands` — array — Cards offered under the welcome message on an empty thread, in the order given. Empty or omitted shows no cards. _(maxItems=8)_
          - _array of_ `AssistantQuickCommand`
            - `title` — string **(required)** — Card label, e.g. 'Summarize my day'. Rendered on one line and truncated when it does not fit. _(minLen=1; maxLen=60)_
            - `description` — string — Optional line under the label. Also one line, so keep it to a short clarification of what the command does. _(minLen=1; maxLen=120)_
            - `prompt` — string **(required)** — The message actually sent when the card is picked. Usually longer and more explicit than the label, since it is what the model reads. _(minLen=1; maxLen=2000)_
        - `placeholder` — string — Placeholder text in the composer, e.g. 'Ask about an account…'. Defaults to the client's own placeholder when omitted. _(minLen=1; maxLen=100)_
      - `audio` — AssistantAudioSettings — Switchable audio for the assistant channel. The settings object keeps enablement beside its speech policy, matching the voice channel's switchable blocks so a disabled configuration can be retained without serving audio.
        - `enabled` — boolean **(required)** — Whether the assistant accepts audio calls. Required so the presence of saved speech configuration is never mistaken for enablement.
        - `speech` — AssistantSpeechSettings — Recognition and synthesis policy for assistant audio. This is assistant-owned rather than a VoiceSpeechSettings reuse so telephony and assistant audio can evolve independently. It has no language greeting and no greet-every-language switch because an assistant conversation is already open when its audio call starts, leaving nothing for the channel to greet.
          - `languages` — array **(required)** — Languages the assistant audio channel can recognise and speak. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once — unlike the voice channel, where a caller opts into identification with `autoDetect`, THIS channel derives identification from `languages` and turns it on whenever the recogniser can identify among more than one, so every one of the up to ten rows here can become a live candidate list. The service does not clamp that list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five); a caller configuring more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. _(minItems=1; maxItems=10)_
            - _array of_ `AssistantLanguage`
              - _(nesting depth limit — see `AssistantLanguage` in the Schemas appendix)_
          - `transcription` — AssistantTranscriptionSettings — Speech-to-text configuration owned by the assistant channel, so changes to assistant recognition policy cannot alter telephony calls. NO `autoDetect` HERE, unlike the voice channel: on this channel configuring a second language IS the request to recognise which one is being spoken — nobody lists two and then asks to be heard in only one — so the server derives identification from the language list and clamps it to false when the recogniser cannot identify among them, or there are too few to identify. The voice channel keeps the switch because a dialplan can hand a call its language, which is a choice an assistant conversation never has to make.
            - `engine` — string — Recogniser used for assistant audio. Absent resolves to the platform default, resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
  - `engine` — union **(required)** — How the agent produces replies. `ai` is the managed engine; `webhook` and `sqs` delegate to an external backend.
    - _oneOf_ — exactly one of:
      - **`ai`**
        - `ai` — AgentAiEngine **(required)** — Managed AI engine: the platform runs the model, tools and knowledge lookups.
          - `instructions` — string **(required)** _(minLen=1; maxLen=60000)_
          - `workflow` — AgentWorkflow — The agent's conversation as a graph: which step runs first, what each step does, and on what condition control moves on. Optional on AgentAiEngine — without one the agent is prompt-driven, steered by `instructions` and free to use its capabilities in any order. Versioned with the rest of the agent definition: publishing a version snapshots the graph, and a draft edit reaches no session until it is published and routed.
            - `entry` — string **(required)** — Step the graph starts at. Must be one of `steps`. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
            - `steps` — array **(required)** — Steps of one graph. Ids are unique within it. _(minItems=1; maxItems=200)_
              - _array of_ `AgentWorkflowStep`
                - _(nesting depth limit — see `AgentWorkflowStep` in the Schemas appendix)_
            - `nested` — array — Graphs the main workflow can run, referenced by `workflow` steps.
              - _array of_ `AgentWorkflowNested`
                - _(nesting depth limit — see `AgentWorkflowNested` in the Schemas appendix)_
            - `settings` — AgentWorkflowSettings
              - `maxTransitions` — number — Give up after this many step transitions, so a cycle whose conditions all keep matching cannot run forever. Absent means no limit, which is the default: a deliberate loop — 'keep asking until you have the postcode' — is a normal shape, and silently capping it would be worse than making the author say so. _(min=1; max=500)_
              - `variables` — array — Workflow variables seeded before the first step runs. Agent input variables (`engine.ai.variables`) are already in scope and need no entry here.
                - _(nesting depth limit — see `AgentWorkflowAssignment` in the Schemas appendix)_
              - `layout` — string — How the builder arranges the graph. Authoring metadata: the runtime ignores it. `stages` bands the graph by `stage`, which is what a forty-step workflow needs. _(enum: `flow`, `compact`, `stages`)_
          - `guardrails` — AgentGuardrails — Turn screening, by side. Only `input` exists: it guards what reaches the model, and output screening is a separate policy with different actions, added here when it is built.
            - `input` — AgentGuardrailInput — Screening applied to what reaches the model. There is deliberately no bundle or preset-group member. A named group that expands to a set of checks reads like convenience and behaves like version skew: the same agent definition would mean different things before and after a platform release, invisibly to the tenant who published it. Listing the checks costs a few lines in a document the console writes anyway, and the published version then states exactly what it enforces. There is also no set-level default action. One field standing behind every check reads as a convenience and hides the thing a reader most needs to see: what a given check will actually do. A check's action is its own or its preset's, and both are visible on the check.
              - `checks` — array — The checks to run, evaluated together in one call. Absent or empty means no screening. _(maxItems=30)_
                - _(nesting depth limit — see `AgentGuardrailCheck` in the Schemas appendix)_
              - `model` — string — The model that runs the checks. Defaults to the platform's guardrail model — deliberately small and fast, and deliberately not the agent's own, whose cost and latency are what this exists to avoid spending on a bad turn. _(pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
              - `action` — union — What happens when a check trips. Exactly one member is set. Ordered by severity: observe < redact < block < end. When more than one check trips in the same call the most severe action wins and ties break on the order of `checks`, so a set can mix an observed check with an enforced one without the observation weakening the enforcement. There is no hand-over member yet. Handing a session to a human is a different mechanism on every channel — a voice transfer, a chat assignment, an assistant with no human behind it — and wiring a guardrail into all of them is out of proportion to the rest of this feature. Until AgentHandoverCapability has a runtime on more than one channel, the crisis path is a block whose message routes the caller.
                - _(nesting depth limit — see `AgentGuardrailAction` in the Schemas appendix)_
              - `mode` — string — Runs the checker before the agent's model (BLOCKING) or alongside it (PARALLEL). Blocking costs the checker's latency on every turn but guarantees that a refused turn spent no tokens and fired no tool; parallel adds no latency and is the right trade on voice, where the delay is audible, at the risk that part of a reply reaches the caller and that a tool has already run before the cancellation lands. Defaults to BLOCKING. _(enum: `blocking`, `parallel`)_
              - `errorMode` — string — What happens when the checker itself errors or times out. OPEN lets the turn through unscreened and records GuardrailFailedEvent, so an unscreened turn is a fact in the log rather than an absence; CLOSED refuses it. Defaults to OPEN: an agent that stops answering because a small model had a bad minute is a worse and far likelier outage than the rare turn that goes unscreened. Background tasks, where nobody is waiting and a retry is free, are the case for CLOSED. _(enum: `open`, `closed`)_
              - `window` — string — How much of the conversation the checker sees. Defaults to LAST_WITH_PRIOR, because the jailbreaks worth catching are built across several turns — establish a fiction, then cash it in — and a checker shown only the last turn sees an innocuous sentence. There is no full-transcript option: screening a whole call on every turn would make the guardrail dearer than the agent. _(enum: `lastMessage`, `lastWithPrior`)_
          - `model` — string — Defaults to the platform default model when omitted. _(pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
          - `timeZone` — string — IANA timezone the agent reasons about time in: it anchors the current date and time given to the model and how times are read from and written to tool arguments and replies. Shared by every channel the agent serves. Defaults to 'UTC'. _(minLen=1; maxLen=64)_
          - `artifacts` — boolean — Whether the agent can produce artifacts (wilma-artifacts): files it writes in its sandbox and shares back during a session — a document, a PDF, a spreadsheet, a chart, a multi-page web site, a folder of files. Needs the sandbox capability. An artifact starts private to the user the session runs for, who can share it company-wide from the viewer; on the chat channel the runtime shares each one company-wide as it is created, so the link posted into the conversation opens for every signed-in colleague. Artifacts are company-internal: recipients on external transports (sms / whatsapp) or outside the company cannot open the links, so keep this disabled for customer-facing agents. Defaults to false.
          - `skills` — array — Skills attached to this agent (progressive disclosure). A skill may carry its own tools, which join this agent's toolset while that skill is active.
            - _array of_ `AgentSkillReference`
              - `id` — string **(required)** _(minLen=12; maxLen=12)_
              - `skillVersion` — number — Pin a specific published skill version. When omitted, latestVersion is resolved. _(min=1)_
              - `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
                - _(nesting depth limit — see `AgentAccess` in the Schemas appendix)_
          - `capabilities` — array — Everything the agent can do. When a `workflow` is set these are the capabilities in scope at every step, and a step may add to them or narrow them with its own list of the same shape.
            - _array of_ `AgentCapability`
              - _oneOf_ — exactly one of:
                - **`tool`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`connector`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`kb`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`sandbox`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`webSearch`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`webFetch`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`agent`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`handover`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`delegation`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`transfer`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`suggestions`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`hangup`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`wait`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `variables` — array
            - _array of_ `AgentVariable`
              - `name` — string **(required)** _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
              - `type` — string **(required)** _(enum: `string`, `number`, `boolean`, `string_array`, `number_array`)_
              - `optional` — boolean **(required)**
              - `description` — string — What the variable means and how it should be filled.
      - **`webhook`**
        - `webhook` — AgentWebhookEngine **(required)** — Bring-your-own backend over HTTPS. The platform POSTs call events to the URL; the backend answers out of band through the channel's command API. The response body is not read.
          - `url` — string **(required)**
          - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
            - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
          - `timeout` — number — Timeout of one delivery, in milliseconds. _(default=10000; min=5000; max=120000)_
      - **`sqs`**
        - `sqs` — AgentSqsEngine **(required)** — Bring-your-own backend over SQS. The platform sends call events to the queue; the backend answers out of band through the channel's command API.
          - `url` — string **(required)**
          - `key` — string **(required)**
          - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
            - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `settings` — AgentSettings — Agent-level settings shared across all channels.
    - `pbxGroupId` — string — PBX group used for data ACL (e.g. Sales Intelligence lookups).
  - `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
    - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
    - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
      - _array of_ `AgentGrantPrincipal`
        - _oneOf_ — exactly one of:
          - **`userId`**
            - `userId` — string **(required)** _(minLen=12; maxLen=12)_
          - **`groupId`**
            - `groupId` — string **(required)**
          - **`department`**
            - `department` — string **(required)** — PBX department NAME, as carried on the colleague record (`PbxColleague.department`), not a department id. The x-bees directory knows a colleague's department only by name, so matching by name is what lets the check read a field the runtime already has instead of resolving the PBX department tree on every request. Two consequences: renaming a department in the PBX invalidates every grant naming it, and two departments with the same name in different branches of the tree are one value here.
  - `revision` — number **(required)** — Draft revision this update is based on (optimistic locking). When it does not match the current revision, RevisionConflictException is returned.
- **Response 200** (`UpdateAgentResponseContent`)
  - `agent` — Agent **(required)** — The complete, versionable configuration of an agent. This is what gets snapshotted when a version is published.
    - `name` — string **(required)** _(minLen=3; maxLen=255)_
    - `description` — string _(minLen=1; maxLen=1000)_
    - `category` — string — Category of the agent, e.g.: 'Support'. _(minLen=1; maxLen=128)_
    - `picture` — string — Avatar URL.
    - `channels` — AgentChannels **(required)** — The channels an agent serves and their channel-specific settings. Presence of a member enables that channel. Empty means the agent serves no channel: it is not reachable on its own and runs only as an automation's task or when another agent calls it. Enabled channels are mirrored as ChannelType values on AgentInfo.
      - `voice` — VoiceChannelSettings — Voice channel settings. Note: a voice agent's AgentAccess.grants are ignored — inbound calls are routed by the PBX dialplan and data ACL is the agent-level `settings.pbxGroupId`, not per-user grants.
        - `greeting` — string — Message spoken when the call starts.
        - `backgroundSound` — VoiceBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT like `interruptions` and `endCall`, rather than a loose name on the channel: it is one switchable call behaviour, it reads the same way as its siblings, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
          - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
          - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
        - `speech` — VoiceSpeechSettings — Speech configuration for the voice channel. When present it WINS over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the single exception, because it is the channel's own input signal and the feature has no starting point without it.
          - `languages` — array **(required)** — Configured languages. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once: automatic detection here is opt-in (`transcription.autoDetect`), and once a caller turns it on, the service does not clamp the resulting candidate list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five) — a caller who both opts in and configures more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. With detection off, only the single resolved language is ever sent, so the ceiling never becomes a candidate-list problem at all. _(minItems=1; maxItems=10)_
            - _array of_ `VoiceLanguage`
              - _(nesting depth limit — see `VoiceLanguage` in the Schemas appendix)_
          - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in the voice, provider account and pronunciation rules of its own language, instead of only the language the call resolved to. Languages whose first message is empty, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
          - `transcription` — VoiceTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
            - `engine` — string — Recogniser to transcribe the caller with. Absent resolves to the platform default ('aws://transcribe' today), resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
            - `autoDetect` — boolean — Identify the caller's language per utterance and switch voice and reply language mid-call. HERE RATHER THAN ON `VoiceSpeechSettings`, because identifying a language is something the RECOGNISER does: it becomes identify-multiple-languages plus language-options on the recognition stream, and nothing about synthesis reads it. Requires at least two configured languages and a recogniser that can identify them; the server clamps it to false otherwise, because forwarding true with a single candidate makes Amazon reject the stream outright.
        - `interruptions` — VoiceInterruptionSettings
          - `enabled` — boolean **(required)** — Whether the caller can interrupt the agent while it is speaking.
          - `minWords` — number — Minimum number of caller words that count as an interruption. _(min=1; max=10)_
        - `silenceTimeout` — VoiceSilenceTimeoutSettings
          - `seconds` — number **(required)** — Seconds of caller silence before the action is taken. _(min=1; max=600)_
          - `action` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`hangup`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`transfer`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `maxDuration` — VoiceMaxDurationSettings
          - `seconds` — number **(required)** — Maximum call duration in seconds before the action is taken. _(min=10; max=14400)_
          - `action` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`hangup`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`transfer`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `endCall` — VoiceEndCallSettings
          - `enabled` — boolean **(required)**
          - `phrases` — string — Comma-separated phrases that end the call, e.g. 'goodbye,bye'.
        - `callerMetadata` — VoiceCallerMetadataSettings — Caller context injected into the model prompt.
          - `callerName` — boolean — Include the caller name. Defaults to true.
          - `callerNumber` — boolean — Include the caller phone number. Defaults to true.
          - `callerEmail` — boolean — Include the caller email when known. Defaults to false.
          - `callerCompany` — boolean — Include the caller company when known. Defaults to false.
          - `time` — boolean — Include the current time, rendered in the agent's `engine.ai.timeZone`. Defaults to false.
      - `chat` — ChatChannelSettings
        - `discoverable` — boolean — Whether users can find and add this agent to conversations.
        - `sessionTimeoutMinutes` — number — Minutes a conversation can stay idle before the next message starts a new session. Omit to start a new session at the end of the agent's local day (`engine.ai.timeZone`). Allowed values: 15, 30, 60, 120. _(min=15; max=120)_
        - `verbosity` — string — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
      - `assistant` — AssistantChannelSettings — Assistant channel settings. Presence enables the in-app assistant surface; audio remains unavailable unless its separate settings are present and enabled.
        - `default` — boolean — Offer this agent as the default assistant for users covered by the agent access settings.
        - `ui` — AssistantUiSettings — How the agent presents itself in the assistant UI: what the user reads before typing anything, and what they can start from without typing at all. Everything here is presentation — it never changes what the agent can do.
          - `welcome` — AssistantWelcomeSettings — Greeting shown on an empty thread, above the quick commands.
            - `title` — string — Heading, e.g. 'How can I help?'. Rendered on one line. _(minLen=1; maxLen=80)_
            - `subtitle` — string — Line under the heading, saying what this agent is for, e.g. 'Ask about your conversations, accounts and calls.'. _(minLen=1; maxLen=200)_
          - `commands` — array — Cards offered under the welcome message on an empty thread, in the order given. Empty or omitted shows no cards. _(maxItems=8)_
            - _array of_ `AssistantQuickCommand`
              - _(nesting depth limit — see `AssistantQuickCommand` in the Schemas appendix)_
          - `placeholder` — string — Placeholder text in the composer, e.g. 'Ask about an account…'. Defaults to the client's own placeholder when omitted. _(minLen=1; maxLen=100)_
        - `audio` — AssistantAudioSettings — Switchable audio for the assistant channel. The settings object keeps enablement beside its speech policy, matching the voice channel's switchable blocks so a disabled configuration can be retained without serving audio.
          - `enabled` — boolean **(required)** — Whether the assistant accepts audio calls. Required so the presence of saved speech configuration is never mistaken for enablement.
          - `speech` — AssistantSpeechSettings — Recognition and synthesis policy for assistant audio. This is assistant-owned rather than a VoiceSpeechSettings reuse so telephony and assistant audio can evolve independently. It has no language greeting and no greet-every-language switch because an assistant conversation is already open when its audio call starts, leaving nothing for the channel to greet.
            - `languages` — array **(required)** — Languages the assistant audio channel can recognise and speak. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once — unlike the voice channel, where a caller opts into identification with `autoDetect`, THIS channel derives identification from `languages` and turns it on whenever the recogniser can identify among more than one, so every one of the up to ten rows here can become a live candidate list. The service does not clamp that list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five); a caller configuring more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. _(minItems=1; maxItems=10)_
              - _(nesting depth limit — see `AssistantLanguage` in the Schemas appendix)_
            - `transcription` — AssistantTranscriptionSettings — Speech-to-text configuration owned by the assistant channel, so changes to assistant recognition policy cannot alter telephony calls. NO `autoDetect` HERE, unlike the voice channel: on this channel configuring a second language IS the request to recognise which one is being spoken — nobody lists two and then asks to be heard in only one — so the server derives identification from the language list and clamps it to false when the recogniser cannot identify among them, or there are too few to identify. The voice channel keeps the switch because a dialplan can hand a call its language, which is a choice an assistant conversation never has to make.
              - _(nesting depth limit — see `AssistantTranscriptionSettings` in the Schemas appendix)_
    - `engine` — union **(required)** — How the agent produces replies. `ai` is the managed engine; `webhook` and `sqs` delegate to an external backend.
      - _oneOf_ — exactly one of:
        - **`ai`**
          - `ai` — AgentAiEngine **(required)** — Managed AI engine: the platform runs the model, tools and knowledge lookups.
            - `instructions` — string **(required)** _(minLen=1; maxLen=60000)_
            - `workflow` — AgentWorkflow — The agent's conversation as a graph: which step runs first, what each step does, and on what condition control moves on. Optional on AgentAiEngine — without one the agent is prompt-driven, steered by `instructions` and free to use its capabilities in any order. Versioned with the rest of the agent definition: publishing a version snapshots the graph, and a draft edit reaches no session until it is published and routed.
              - `entry` — string **(required)** — Step the graph starts at. Must be one of `steps`. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
              - `steps` — array **(required)** — Steps of one graph. Ids are unique within it. _(minItems=1; maxItems=200)_
                - _(nesting depth limit — see `AgentWorkflowStep` in the Schemas appendix)_
              - `nested` — array — Graphs the main workflow can run, referenced by `workflow` steps.
                - _(nesting depth limit — see `AgentWorkflowNested` in the Schemas appendix)_
              - `settings` — AgentWorkflowSettings
                - _(nesting depth limit — see `AgentWorkflowSettings` in the Schemas appendix)_
            - `guardrails` — AgentGuardrails — Turn screening, by side. Only `input` exists: it guards what reaches the model, and output screening is a separate policy with different actions, added here when it is built.
              - `input` — AgentGuardrailInput — Screening applied to what reaches the model. There is deliberately no bundle or preset-group member. A named group that expands to a set of checks reads like convenience and behaves like version skew: the same agent definition would mean different things before and after a platform release, invisibly to the tenant who published it. Listing the checks costs a few lines in a document the console writes anyway, and the published version then states exactly what it enforces. There is also no set-level default action. One field standing behind every check reads as a convenience and hides the thing a reader most needs to see: what a given check will actually do. A check's action is its own or its preset's, and both are visible on the check.
                - _(nesting depth limit — see `AgentGuardrailInput` in the Schemas appendix)_
            - `model` — string — Defaults to the platform default model when omitted. _(pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
            - `timeZone` — string — IANA timezone the agent reasons about time in: it anchors the current date and time given to the model and how times are read from and written to tool arguments and replies. Shared by every channel the agent serves. Defaults to 'UTC'. _(minLen=1; maxLen=64)_
            - `artifacts` — boolean — Whether the agent can produce artifacts (wilma-artifacts): files it writes in its sandbox and shares back during a session — a document, a PDF, a spreadsheet, a chart, a multi-page web site, a folder of files. Needs the sandbox capability. An artifact starts private to the user the session runs for, who can share it company-wide from the viewer; on the chat channel the runtime shares each one company-wide as it is created, so the link posted into the conversation opens for every signed-in colleague. Artifacts are company-internal: recipients on external transports (sms / whatsapp) or outside the company cannot open the links, so keep this disabled for customer-facing agents. Defaults to false.
            - `skills` — array — Skills attached to this agent (progressive disclosure). A skill may carry its own tools, which join this agent's toolset while that skill is active.
              - _array of_ `AgentSkillReference`
                - _(nesting depth limit — see `AgentSkillReference` in the Schemas appendix)_
            - `capabilities` — array — Everything the agent can do. When a `workflow` is set these are the capabilities in scope at every step, and a step may add to them or narrow them with its own list of the same shape.
              - _array of_ `AgentCapability`
                - _(nesting depth limit — see `AgentCapability` in the Schemas appendix)_
            - `variables` — array
              - _array of_ `AgentVariable`
                - _(nesting depth limit — see `AgentVariable` in the Schemas appendix)_
        - **`webhook`**
          - `webhook` — AgentWebhookEngine **(required)** — Bring-your-own backend over HTTPS. The platform POSTs call events to the URL; the backend answers out of band through the channel's command API. The response body is not read.
            - `url` — string **(required)**
            - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
              - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
            - `timeout` — number — Timeout of one delivery, in milliseconds. _(default=10000; min=5000; max=120000)_
        - **`sqs`**
          - `sqs` — AgentSqsEngine **(required)** — Bring-your-own backend over SQS. The platform sends call events to the queue; the backend answers out of band through the channel's command API.
            - `url` — string **(required)**
            - `key` — string **(required)**
            - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
              - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
    - `settings` — AgentSettings — Agent-level settings shared across all channels.
      - `pbxGroupId` — string — PBX group used for data ACL (e.g. Sales Intelligence lookups).
    - `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
      - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
      - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
        - _array of_ `AgentGrantPrincipal`
          - _oneOf_ — exactly one of:
            - **`userId`**
              - `userId` — string **(required)** _(minLen=12; maxLen=12)_
            - **`groupId`**
              - `groupId` — string **(required)**
            - **`department`**
              - `department` — string **(required)** — PBX department NAME, as carried on the colleague record (`PbxColleague.department`), not a department id. The x-bees directory knows a colleague's department only by name, so matching by name is what lets the check read a field the runtime already has instead of resolving the PBX department tree on every request. Two consequences: renaming a department in the PBX invalidates every grant naming it, and two departments with the same name in different branches of the tree are one value here.
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
    - `updatedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `updatedBy` — Actor — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
    - `latestVersion` — number — Latest published version number; absent while the agent is still a draft. _(min=1)_
    - `draftBaseVersion` — number — Published version number from which the current draft originated. Absent before the first version is published. _(min=1)_
    - `deployment` — array — How new sessions are split across published versions. Absent while the agent is still a draft. _(minItems=1; maxItems=10)_
      - _array of_ `AgentDeploymentRoute`
        - `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
        - `percentage` — number **(required)** — Percentage of new sessions routed to this version. Percentages must sum to 100. _(min=1; max=100)_
- Errors: `400`, `404`, `409`

#### `DELETE` `/v2/agents/agents/{agentId}`

Deletes an agent, its draft, versions and API keys. Fails with ConflictException while the agent has active sessions or is referenced by other agents.

- operationId: `DeleteAgent`
- **Scopes**: `wilma-agents:DeleteAgent`
- **Parameters**
  - `agentId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- Errors: `400`, `409`

### Versions

#### `GET` `/v2/agents/agents/{agentId}/compare-versions`

Returns the field-level differences between two versions, or between a version and the current draft.

- operationId: `CompareAgentVersions`
- **Scopes**: `wilma-agents:CompareAgentVersions`, `wilma-agents:read`
- **Parameters**
  - `agentId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `from` (query) — number — Base published version number. Omit when fromDraft is true. _(min=1)_
  - `fromDraft` (query) — boolean — Use the current draft as the base instead of a published version.
  - `to` (query) — number — Target published version number. Omit when toDraft is true. _(min=1)_
  - `toDraft` (query) — boolean — Use the current draft as the target instead of a published version.
- **Response 200** (`CompareAgentVersionsResponseContent`)
  - `changes` — array **(required)**
    - _array of_ `AgentVersionChange`
      - `path` — string **(required)** — JSON pointer of the changed field within the agent definition, e.g. '/engine/ai/instructions'.
      - `before` — any — Value before the change (absent when the field was added).
      - `after` — any — Value after the change (absent when the field was removed).
- Errors: `400`, `404`

#### `GET` `/v2/agents/agents/{agentId}/versions`

Lists the published versions of an agent, newest first.

- operationId: `ListAgentVersions`
- **Scopes**: `wilma-agents:ListAgentVersions`, `wilma-agents:read`
- **Parameters**
  - `agentId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `limit` (query) — number _(min=1; max=100)_
  - `cursor` (query) — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- **Response 200** (`ListAgentVersionsResponseContent`)
  - `versions` — array **(required)**
    - _array of_ `AgentVersionInfo`
      - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
      - `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
      - `basedOnVersion` — number — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
      - `name` — string _(minLen=1; maxLen=255)_
      - `changelog` — string — Human-readable description of what changed in a published version. _(minLen=1; maxLen=500)_
      - `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
        - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
        - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
        - `name` — string — Human readable name of the actor at the time of the action.
  - `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- Errors: `400`, `404`

#### `POST` `/v2/agents/agents/{agentId}/versions`

Publishes the current draft as a new immutable version. Publishing never changes what is served; call PutAgentDeployment separately to route sessions to it.

- operationId: `PublishAgentVersion`
- **Scopes**: `wilma-agents:PublishAgentVersion`
- **Parameters**
  - `agentId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `PublishAgentVersionRequestContent`) **(required)**
  - `changelog` — string — What changed in this version. _(minLen=1; maxLen=500)_
  - `name` — string — Optional human-readable name for this version. _(minLen=1; maxLen=255)_
  - `revision` — number **(required)** — Draft revision this publish is based on (optimistic locking).
- **Response 200** (`PublishAgentVersionResponseContent`)
  - `version` — AgentVersion **(required)**
    - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
    - `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
    - `basedOnVersion` — number — Published version from which the draft originated. Absent for the first version of a new agent. _(min=1)_
    - `name` — string — Optional human-readable name supplied at publish time. _(minLen=1; maxLen=255)_
    - `changelog` — string — What changed in this version, provided at publish time. _(minLen=1; maxLen=500)_
    - `definition` — AgentDefinitionSnapshot **(required)** — The complete, versionable configuration of an agent. This is what gets snapshotted when a version is published.
      - `name` — string **(required)** _(minLen=3; maxLen=255)_
      - `description` — string _(minLen=1; maxLen=1000)_
      - `category` — string — Category of the agent, e.g.: 'Support'. _(minLen=1; maxLen=128)_
      - `picture` — string — Avatar URL.
      - `channels` — AgentChannels **(required)** — The channels an agent serves and their channel-specific settings. Presence of a member enables that channel. Empty means the agent serves no channel: it is not reachable on its own and runs only as an automation's task or when another agent calls it. Enabled channels are mirrored as ChannelType values on AgentInfo.
        - `voice` — VoiceChannelSettings — Voice channel settings. Note: a voice agent's AgentAccess.grants are ignored — inbound calls are routed by the PBX dialplan and data ACL is the agent-level `settings.pbxGroupId`, not per-user grants.
          - `greeting` — string — Message spoken when the call starts.
          - `backgroundSound` — VoiceBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT like `interruptions` and `endCall`, rather than a loose name on the channel: it is one switchable call behaviour, it reads the same way as its siblings, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
            - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
            - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
          - `speech` — VoiceSpeechSettings — Speech configuration for the voice channel. When present it WINS over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the single exception, because it is the channel's own input signal and the feature has no starting point without it.
            - `languages` — array **(required)** — Configured languages. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once: automatic detection here is opt-in (`transcription.autoDetect`), and once a caller turns it on, the service does not clamp the resulting candidate list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five) — a caller who both opts in and configures more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. With detection off, only the single resolved language is ever sent, so the ceiling never becomes a candidate-list problem at all. _(minItems=1; maxItems=10)_
              - _(nesting depth limit — see `VoiceLanguage` in the Schemas appendix)_
            - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in the voice, provider account and pronunciation rules of its own language, instead of only the language the call resolved to. Languages whose first message is empty, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
            - `transcription` — VoiceTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
              - _(nesting depth limit — see `VoiceTranscriptionSettings` in the Schemas appendix)_
          - `interruptions` — VoiceInterruptionSettings
            - `enabled` — boolean **(required)** — Whether the caller can interrupt the agent while it is speaking.
            - `minWords` — number — Minimum number of caller words that count as an interruption. _(min=1; max=10)_
          - `silenceTimeout` — VoiceSilenceTimeoutSettings
            - `seconds` — number **(required)** — Seconds of caller silence before the action is taken. _(min=1; max=600)_
            - `action` — union **(required)**
              - _(nesting depth limit — see `VoiceTerminateAction` in the Schemas appendix)_
          - `maxDuration` — VoiceMaxDurationSettings
            - `seconds` — number **(required)** — Maximum call duration in seconds before the action is taken. _(min=10; max=14400)_
            - `action` — union **(required)**
              - _(nesting depth limit — see `VoiceTerminateAction` in the Schemas appendix)_
          - `endCall` — VoiceEndCallSettings
            - `enabled` — boolean **(required)**
            - `phrases` — string — Comma-separated phrases that end the call, e.g. 'goodbye,bye'.
          - `callerMetadata` — VoiceCallerMetadataSettings — Caller context injected into the model prompt.
            - `callerName` — boolean — Include the caller name. Defaults to true.
            - `callerNumber` — boolean — Include the caller phone number. Defaults to true.
            - `callerEmail` — boolean — Include the caller email when known. Defaults to false.
            - `callerCompany` — boolean — Include the caller company when known. Defaults to false.
            - `time` — boolean — Include the current time, rendered in the agent's `engine.ai.timeZone`. Defaults to false.
        - `chat` — ChatChannelSettings
          - `discoverable` — boolean — Whether users can find and add this agent to conversations.
          - `sessionTimeoutMinutes` — number — Minutes a conversation can stay idle before the next message starts a new session. Omit to start a new session at the end of the agent's local day (`engine.ai.timeZone`). Allowed values: 15, 30, 60, 120. _(min=15; max=120)_
          - `verbosity` — string — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
        - `assistant` — AssistantChannelSettings — Assistant channel settings. Presence enables the in-app assistant surface; audio remains unavailable unless its separate settings are present and enabled.
          - `default` — boolean — Offer this agent as the default assistant for users covered by the agent access settings.
          - `ui` — AssistantUiSettings — How the agent presents itself in the assistant UI: what the user reads before typing anything, and what they can start from without typing at all. Everything here is presentation — it never changes what the agent can do.
            - `welcome` — AssistantWelcomeSettings — Greeting shown on an empty thread, above the quick commands.
              - _(nesting depth limit — see `AssistantWelcomeSettings` in the Schemas appendix)_
            - `commands` — array — Cards offered under the welcome message on an empty thread, in the order given. Empty or omitted shows no cards. _(maxItems=8)_
              - _(nesting depth limit — see `AssistantQuickCommand` in the Schemas appendix)_
            - `placeholder` — string — Placeholder text in the composer, e.g. 'Ask about an account…'. Defaults to the client's own placeholder when omitted. _(minLen=1; maxLen=100)_
          - `audio` — AssistantAudioSettings — Switchable audio for the assistant channel. The settings object keeps enablement beside its speech policy, matching the voice channel's switchable blocks so a disabled configuration can be retained without serving audio.
            - `enabled` — boolean **(required)** — Whether the assistant accepts audio calls. Required so the presence of saved speech configuration is never mistaken for enablement.
            - `speech` — AssistantSpeechSettings — Recognition and synthesis policy for assistant audio. This is assistant-owned rather than a VoiceSpeechSettings reuse so telephony and assistant audio can evolve independently. It has no language greeting and no greet-every-language switch because an assistant conversation is already open when its audio call starts, leaving nothing for the channel to greet.
              - _(nesting depth limit — see `AssistantSpeechSettings` in the Schemas appendix)_
      - `engine` — union **(required)** — How the agent produces replies. `ai` is the managed engine; `webhook` and `sqs` delegate to an external backend.
        - _oneOf_ — exactly one of:
          - **`ai`**
            - `ai` — AgentAiEngine **(required)** — Managed AI engine: the platform runs the model, tools and knowledge lookups.
              - `instructions` — string **(required)** _(minLen=1; maxLen=60000)_
              - `workflow` — AgentWorkflow — The agent's conversation as a graph: which step runs first, what each step does, and on what condition control moves on. Optional on AgentAiEngine — without one the agent is prompt-driven, steered by `instructions` and free to use its capabilities in any order. Versioned with the rest of the agent definition: publishing a version snapshots the graph, and a draft edit reaches no session until it is published and routed.
                - _(nesting depth limit — see `AgentWorkflow` in the Schemas appendix)_
              - `guardrails` — AgentGuardrails — Turn screening, by side. Only `input` exists: it guards what reaches the model, and output screening is a separate policy with different actions, added here when it is built.
                - _(nesting depth limit — see `AgentGuardrails` in the Schemas appendix)_
              - `model` — string — Defaults to the platform default model when omitted. _(pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
              - `timeZone` — string — IANA timezone the agent reasons about time in: it anchors the current date and time given to the model and how times are read from and written to tool arguments and replies. Shared by every channel the agent serves. Defaults to 'UTC'. _(minLen=1; maxLen=64)_
              - `artifacts` — boolean — Whether the agent can produce artifacts (wilma-artifacts): files it writes in its sandbox and shares back during a session — a document, a PDF, a spreadsheet, a chart, a multi-page web site, a folder of files. Needs the sandbox capability. An artifact starts private to the user the session runs for, who can share it company-wide from the viewer; on the chat channel the runtime shares each one company-wide as it is created, so the link posted into the conversation opens for every signed-in colleague. Artifacts are company-internal: recipients on external transports (sms / whatsapp) or outside the company cannot open the links, so keep this disabled for customer-facing agents. Defaults to false.
              - `skills` — array — Skills attached to this agent (progressive disclosure). A skill may carry its own tools, which join this agent's toolset while that skill is active.
                - _(nesting depth limit — see `AgentSkillReference` in the Schemas appendix)_
              - `capabilities` — array — Everything the agent can do. When a `workflow` is set these are the capabilities in scope at every step, and a step may add to them or narrow them with its own list of the same shape.
                - _(nesting depth limit — see `AgentCapability` in the Schemas appendix)_
              - `variables` — array
                - _(nesting depth limit — see `AgentVariable` in the Schemas appendix)_
          - **`webhook`**
            - `webhook` — AgentWebhookEngine **(required)** — Bring-your-own backend over HTTPS. The platform POSTs call events to the URL; the backend answers out of band through the channel's command API. The response body is not read.
              - `url` — string **(required)**
              - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
                - _(nesting depth limit — see `SecretRef` in the Schemas appendix)_
              - `timeout` — number — Timeout of one delivery, in milliseconds. _(default=10000; min=5000; max=120000)_
          - **`sqs`**
            - `sqs` — AgentSqsEngine **(required)** — Bring-your-own backend over SQS. The platform sends call events to the queue; the backend answers out of band through the channel's command API.
              - `url` — string **(required)**
              - `key` — string **(required)**
              - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
                - _(nesting depth limit — see `SecretRef` in the Schemas appendix)_
      - `settings` — AgentSettings — Agent-level settings shared across all channels.
        - `pbxGroupId` — string — PBX group used for data ACL (e.g. Sales Intelligence lookups).
      - `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
        - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
        - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
          - _array of_ `AgentGrantPrincipal`
            - _oneOf_ — exactly one of:
              - **`userId`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`groupId`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`department`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
- Errors: `400`, `404`, `409`

#### `GET` `/v2/agents/agents/{agentId}/versions/{version}`

Retrieves a published version, including its full immutable definition snapshot.

- operationId: `GetAgentVersion`
- **Scopes**: `wilma-agents:GetAgentVersion`, `wilma-agents:read`
- **Parameters**
  - `agentId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `version` (path) — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Response 200** (`GetAgentVersionResponseContent`)
  - `version` — AgentVersion **(required)**
    - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
    - `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
    - `basedOnVersion` — number — Published version from which the draft originated. Absent for the first version of a new agent. _(min=1)_
    - `name` — string — Optional human-readable name supplied at publish time. _(minLen=1; maxLen=255)_
    - `changelog` — string — What changed in this version, provided at publish time. _(minLen=1; maxLen=500)_
    - `definition` — AgentDefinitionSnapshot **(required)** — The complete, versionable configuration of an agent. This is what gets snapshotted when a version is published.
      - `name` — string **(required)** _(minLen=3; maxLen=255)_
      - `description` — string _(minLen=1; maxLen=1000)_
      - `category` — string — Category of the agent, e.g.: 'Support'. _(minLen=1; maxLen=128)_
      - `picture` — string — Avatar URL.
      - `channels` — AgentChannels **(required)** — The channels an agent serves and their channel-specific settings. Presence of a member enables that channel. Empty means the agent serves no channel: it is not reachable on its own and runs only as an automation's task or when another agent calls it. Enabled channels are mirrored as ChannelType values on AgentInfo.
        - `voice` — VoiceChannelSettings — Voice channel settings. Note: a voice agent's AgentAccess.grants are ignored — inbound calls are routed by the PBX dialplan and data ACL is the agent-level `settings.pbxGroupId`, not per-user grants.
          - `greeting` — string — Message spoken when the call starts.
          - `backgroundSound` — VoiceBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT like `interruptions` and `endCall`, rather than a loose name on the channel: it is one switchable call behaviour, it reads the same way as its siblings, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
            - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
            - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
          - `speech` — VoiceSpeechSettings — Speech configuration for the voice channel. When present it WINS over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the single exception, because it is the channel's own input signal and the feature has no starting point without it.
            - `languages` — array **(required)** — Configured languages. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once: automatic detection here is opt-in (`transcription.autoDetect`), and once a caller turns it on, the service does not clamp the resulting candidate list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five) — a caller who both opts in and configures more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. With detection off, only the single resolved language is ever sent, so the ceiling never becomes a candidate-list problem at all. _(minItems=1; maxItems=10)_
              - _(nesting depth limit — see `VoiceLanguage` in the Schemas appendix)_
            - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in the voice, provider account and pronunciation rules of its own language, instead of only the language the call resolved to. Languages whose first message is empty, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
            - `transcription` — VoiceTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
              - _(nesting depth limit — see `VoiceTranscriptionSettings` in the Schemas appendix)_
          - `interruptions` — VoiceInterruptionSettings
            - `enabled` — boolean **(required)** — Whether the caller can interrupt the agent while it is speaking.
            - `minWords` — number — Minimum number of caller words that count as an interruption. _(min=1; max=10)_
          - `silenceTimeout` — VoiceSilenceTimeoutSettings
            - `seconds` — number **(required)** — Seconds of caller silence before the action is taken. _(min=1; max=600)_
            - `action` — union **(required)**
              - _(nesting depth limit — see `VoiceTerminateAction` in the Schemas appendix)_
          - `maxDuration` — VoiceMaxDurationSettings
            - `seconds` — number **(required)** — Maximum call duration in seconds before the action is taken. _(min=10; max=14400)_
            - `action` — union **(required)**
              - _(nesting depth limit — see `VoiceTerminateAction` in the Schemas appendix)_
          - `endCall` — VoiceEndCallSettings
            - `enabled` — boolean **(required)**
            - `phrases` — string — Comma-separated phrases that end the call, e.g. 'goodbye,bye'.
          - `callerMetadata` — VoiceCallerMetadataSettings — Caller context injected into the model prompt.
            - `callerName` — boolean — Include the caller name. Defaults to true.
            - `callerNumber` — boolean — Include the caller phone number. Defaults to true.
            - `callerEmail` — boolean — Include the caller email when known. Defaults to false.
            - `callerCompany` — boolean — Include the caller company when known. Defaults to false.
            - `time` — boolean — Include the current time, rendered in the agent's `engine.ai.timeZone`. Defaults to false.
        - `chat` — ChatChannelSettings
          - `discoverable` — boolean — Whether users can find and add this agent to conversations.
          - `sessionTimeoutMinutes` — number — Minutes a conversation can stay idle before the next message starts a new session. Omit to start a new session at the end of the agent's local day (`engine.ai.timeZone`). Allowed values: 15, 30, 60, 120. _(min=15; max=120)_
          - `verbosity` — string — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
        - `assistant` — AssistantChannelSettings — Assistant channel settings. Presence enables the in-app assistant surface; audio remains unavailable unless its separate settings are present and enabled.
          - `default` — boolean — Offer this agent as the default assistant for users covered by the agent access settings.
          - `ui` — AssistantUiSettings — How the agent presents itself in the assistant UI: what the user reads before typing anything, and what they can start from without typing at all. Everything here is presentation — it never changes what the agent can do.
            - `welcome` — AssistantWelcomeSettings — Greeting shown on an empty thread, above the quick commands.
              - _(nesting depth limit — see `AssistantWelcomeSettings` in the Schemas appendix)_
            - `commands` — array — Cards offered under the welcome message on an empty thread, in the order given. Empty or omitted shows no cards. _(maxItems=8)_
              - _(nesting depth limit — see `AssistantQuickCommand` in the Schemas appendix)_
            - `placeholder` — string — Placeholder text in the composer, e.g. 'Ask about an account…'. Defaults to the client's own placeholder when omitted. _(minLen=1; maxLen=100)_
          - `audio` — AssistantAudioSettings — Switchable audio for the assistant channel. The settings object keeps enablement beside its speech policy, matching the voice channel's switchable blocks so a disabled configuration can be retained without serving audio.
            - `enabled` — boolean **(required)** — Whether the assistant accepts audio calls. Required so the presence of saved speech configuration is never mistaken for enablement.
            - `speech` — AssistantSpeechSettings — Recognition and synthesis policy for assistant audio. This is assistant-owned rather than a VoiceSpeechSettings reuse so telephony and assistant audio can evolve independently. It has no language greeting and no greet-every-language switch because an assistant conversation is already open when its audio call starts, leaving nothing for the channel to greet.
              - _(nesting depth limit — see `AssistantSpeechSettings` in the Schemas appendix)_
      - `engine` — union **(required)** — How the agent produces replies. `ai` is the managed engine; `webhook` and `sqs` delegate to an external backend.
        - _oneOf_ — exactly one of:
          - **`ai`**
            - `ai` — AgentAiEngine **(required)** — Managed AI engine: the platform runs the model, tools and knowledge lookups.
              - `instructions` — string **(required)** _(minLen=1; maxLen=60000)_
              - `workflow` — AgentWorkflow — The agent's conversation as a graph: which step runs first, what each step does, and on what condition control moves on. Optional on AgentAiEngine — without one the agent is prompt-driven, steered by `instructions` and free to use its capabilities in any order. Versioned with the rest of the agent definition: publishing a version snapshots the graph, and a draft edit reaches no session until it is published and routed.
                - _(nesting depth limit — see `AgentWorkflow` in the Schemas appendix)_
              - `guardrails` — AgentGuardrails — Turn screening, by side. Only `input` exists: it guards what reaches the model, and output screening is a separate policy with different actions, added here when it is built.
                - _(nesting depth limit — see `AgentGuardrails` in the Schemas appendix)_
              - `model` — string — Defaults to the platform default model when omitted. _(pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
              - `timeZone` — string — IANA timezone the agent reasons about time in: it anchors the current date and time given to the model and how times are read from and written to tool arguments and replies. Shared by every channel the agent serves. Defaults to 'UTC'. _(minLen=1; maxLen=64)_
              - `artifacts` — boolean — Whether the agent can produce artifacts (wilma-artifacts): files it writes in its sandbox and shares back during a session — a document, a PDF, a spreadsheet, a chart, a multi-page web site, a folder of files. Needs the sandbox capability. An artifact starts private to the user the session runs for, who can share it company-wide from the viewer; on the chat channel the runtime shares each one company-wide as it is created, so the link posted into the conversation opens for every signed-in colleague. Artifacts are company-internal: recipients on external transports (sms / whatsapp) or outside the company cannot open the links, so keep this disabled for customer-facing agents. Defaults to false.
              - `skills` — array — Skills attached to this agent (progressive disclosure). A skill may carry its own tools, which join this agent's toolset while that skill is active.
                - _(nesting depth limit — see `AgentSkillReference` in the Schemas appendix)_
              - `capabilities` — array — Everything the agent can do. When a `workflow` is set these are the capabilities in scope at every step, and a step may add to them or narrow them with its own list of the same shape.
                - _(nesting depth limit — see `AgentCapability` in the Schemas appendix)_
              - `variables` — array
                - _(nesting depth limit — see `AgentVariable` in the Schemas appendix)_
          - **`webhook`**
            - `webhook` — AgentWebhookEngine **(required)** — Bring-your-own backend over HTTPS. The platform POSTs call events to the URL; the backend answers out of band through the channel's command API. The response body is not read.
              - `url` — string **(required)**
              - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
                - _(nesting depth limit — see `SecretRef` in the Schemas appendix)_
              - `timeout` — number — Timeout of one delivery, in milliseconds. _(default=10000; min=5000; max=120000)_
          - **`sqs`**
            - `sqs` — AgentSqsEngine **(required)** — Bring-your-own backend over SQS. The platform sends call events to the queue; the backend answers out of band through the channel's command API.
              - `url` — string **(required)**
              - `key` — string **(required)**
              - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
                - _(nesting depth limit — see `SecretRef` in the Schemas appendix)_
      - `settings` — AgentSettings — Agent-level settings shared across all channels.
        - `pbxGroupId` — string — PBX group used for data ACL (e.g. Sales Intelligence lookups).
      - `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
        - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
        - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
          - _array of_ `AgentGrantPrincipal`
            - _oneOf_ — exactly one of:
              - **`userId`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`groupId`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`department`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
- Errors: `400`, `404`

#### `POST` `/v2/agents/agents/{agentId}/versions/{version}/draft`

Replaces the mutable draft with a published version's definition. The draft revision is incremented; published versions and the deployment configuration are unchanged.

- operationId: `RestoreAgentVersionToDraft`
- **Scopes**: `wilma-agents:RestoreAgentVersionToDraft`
- **Parameters**
  - `agentId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `version` (path) — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `RestoreAgentVersionToDraftRequestContent`) **(required)**
  - `revision` — number **(required)** — Draft revision this restore is based on (optimistic locking).
- **Response 200** (`RestoreAgentVersionToDraftResponseContent`)
  - `agent` — Agent **(required)** — The complete, versionable configuration of an agent. This is what gets snapshotted when a version is published.
    - `name` — string **(required)** _(minLen=3; maxLen=255)_
    - `description` — string _(minLen=1; maxLen=1000)_
    - `category` — string — Category of the agent, e.g.: 'Support'. _(minLen=1; maxLen=128)_
    - `picture` — string — Avatar URL.
    - `channels` — AgentChannels **(required)** — The channels an agent serves and their channel-specific settings. Presence of a member enables that channel. Empty means the agent serves no channel: it is not reachable on its own and runs only as an automation's task or when another agent calls it. Enabled channels are mirrored as ChannelType values on AgentInfo.
      - `voice` — VoiceChannelSettings — Voice channel settings. Note: a voice agent's AgentAccess.grants are ignored — inbound calls are routed by the PBX dialplan and data ACL is the agent-level `settings.pbxGroupId`, not per-user grants.
        - `greeting` — string — Message spoken when the call starts.
        - `backgroundSound` — VoiceBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT like `interruptions` and `endCall`, rather than a loose name on the channel: it is one switchable call behaviour, it reads the same way as its siblings, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
          - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
          - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
        - `speech` — VoiceSpeechSettings — Speech configuration for the voice channel. When present it WINS over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the single exception, because it is the channel's own input signal and the feature has no starting point without it.
          - `languages` — array **(required)** — Configured languages. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once: automatic detection here is opt-in (`transcription.autoDetect`), and once a caller turns it on, the service does not clamp the resulting candidate list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five) — a caller who both opts in and configures more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. With detection off, only the single resolved language is ever sent, so the ceiling never becomes a candidate-list problem at all. _(minItems=1; maxItems=10)_
            - _array of_ `VoiceLanguage`
              - _(nesting depth limit — see `VoiceLanguage` in the Schemas appendix)_
          - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in the voice, provider account and pronunciation rules of its own language, instead of only the language the call resolved to. Languages whose first message is empty, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
          - `transcription` — VoiceTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
            - `engine` — string — Recogniser to transcribe the caller with. Absent resolves to the platform default ('aws://transcribe' today), resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
            - `autoDetect` — boolean — Identify the caller's language per utterance and switch voice and reply language mid-call. HERE RATHER THAN ON `VoiceSpeechSettings`, because identifying a language is something the RECOGNISER does: it becomes identify-multiple-languages plus language-options on the recognition stream, and nothing about synthesis reads it. Requires at least two configured languages and a recogniser that can identify them; the server clamps it to false otherwise, because forwarding true with a single candidate makes Amazon reject the stream outright.
        - `interruptions` — VoiceInterruptionSettings
          - `enabled` — boolean **(required)** — Whether the caller can interrupt the agent while it is speaking.
          - `minWords` — number — Minimum number of caller words that count as an interruption. _(min=1; max=10)_
        - `silenceTimeout` — VoiceSilenceTimeoutSettings
          - `seconds` — number **(required)** — Seconds of caller silence before the action is taken. _(min=1; max=600)_
          - `action` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`hangup`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`transfer`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `maxDuration` — VoiceMaxDurationSettings
          - `seconds` — number **(required)** — Maximum call duration in seconds before the action is taken. _(min=10; max=14400)_
          - `action` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`hangup`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`transfer`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `endCall` — VoiceEndCallSettings
          - `enabled` — boolean **(required)**
          - `phrases` — string — Comma-separated phrases that end the call, e.g. 'goodbye,bye'.
        - `callerMetadata` — VoiceCallerMetadataSettings — Caller context injected into the model prompt.
          - `callerName` — boolean — Include the caller name. Defaults to true.
          - `callerNumber` — boolean — Include the caller phone number. Defaults to true.
          - `callerEmail` — boolean — Include the caller email when known. Defaults to false.
          - `callerCompany` — boolean — Include the caller company when known. Defaults to false.
          - `time` — boolean — Include the current time, rendered in the agent's `engine.ai.timeZone`. Defaults to false.
      - `chat` — ChatChannelSettings
        - `discoverable` — boolean — Whether users can find and add this agent to conversations.
        - `sessionTimeoutMinutes` — number — Minutes a conversation can stay idle before the next message starts a new session. Omit to start a new session at the end of the agent's local day (`engine.ai.timeZone`). Allowed values: 15, 30, 60, 120. _(min=15; max=120)_
        - `verbosity` — string — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
      - `assistant` — AssistantChannelSettings — Assistant channel settings. Presence enables the in-app assistant surface; audio remains unavailable unless its separate settings are present and enabled.
        - `default` — boolean — Offer this agent as the default assistant for users covered by the agent access settings.
        - `ui` — AssistantUiSettings — How the agent presents itself in the assistant UI: what the user reads before typing anything, and what they can start from without typing at all. Everything here is presentation — it never changes what the agent can do.
          - `welcome` — AssistantWelcomeSettings — Greeting shown on an empty thread, above the quick commands.
            - `title` — string — Heading, e.g. 'How can I help?'. Rendered on one line. _(minLen=1; maxLen=80)_
            - `subtitle` — string — Line under the heading, saying what this agent is for, e.g. 'Ask about your conversations, accounts and calls.'. _(minLen=1; maxLen=200)_
          - `commands` — array — Cards offered under the welcome message on an empty thread, in the order given. Empty or omitted shows no cards. _(maxItems=8)_
            - _array of_ `AssistantQuickCommand`
              - _(nesting depth limit — see `AssistantQuickCommand` in the Schemas appendix)_
          - `placeholder` — string — Placeholder text in the composer, e.g. 'Ask about an account…'. Defaults to the client's own placeholder when omitted. _(minLen=1; maxLen=100)_
        - `audio` — AssistantAudioSettings — Switchable audio for the assistant channel. The settings object keeps enablement beside its speech policy, matching the voice channel's switchable blocks so a disabled configuration can be retained without serving audio.
          - `enabled` — boolean **(required)** — Whether the assistant accepts audio calls. Required so the presence of saved speech configuration is never mistaken for enablement.
          - `speech` — AssistantSpeechSettings — Recognition and synthesis policy for assistant audio. This is assistant-owned rather than a VoiceSpeechSettings reuse so telephony and assistant audio can evolve independently. It has no language greeting and no greet-every-language switch because an assistant conversation is already open when its audio call starts, leaving nothing for the channel to greet.
            - `languages` — array **(required)** — Languages the assistant audio channel can recognise and speak. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once — unlike the voice channel, where a caller opts into identification with `autoDetect`, THIS channel derives identification from `languages` and turns it on whenever the recogniser can identify among more than one, so every one of the up to ten rows here can become a live candidate list. The service does not clamp that list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five); a caller configuring more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. _(minItems=1; maxItems=10)_
              - _(nesting depth limit — see `AssistantLanguage` in the Schemas appendix)_
            - `transcription` — AssistantTranscriptionSettings — Speech-to-text configuration owned by the assistant channel, so changes to assistant recognition policy cannot alter telephony calls. NO `autoDetect` HERE, unlike the voice channel: on this channel configuring a second language IS the request to recognise which one is being spoken — nobody lists two and then asks to be heard in only one — so the server derives identification from the language list and clamps it to false when the recogniser cannot identify among them, or there are too few to identify. The voice channel keeps the switch because a dialplan can hand a call its language, which is a choice an assistant conversation never has to make.
              - _(nesting depth limit — see `AssistantTranscriptionSettings` in the Schemas appendix)_
    - `engine` — union **(required)** — How the agent produces replies. `ai` is the managed engine; `webhook` and `sqs` delegate to an external backend.
      - _oneOf_ — exactly one of:
        - **`ai`**
          - `ai` — AgentAiEngine **(required)** — Managed AI engine: the platform runs the model, tools and knowledge lookups.
            - `instructions` — string **(required)** _(minLen=1; maxLen=60000)_
            - `workflow` — AgentWorkflow — The agent's conversation as a graph: which step runs first, what each step does, and on what condition control moves on. Optional on AgentAiEngine — without one the agent is prompt-driven, steered by `instructions` and free to use its capabilities in any order. Versioned with the rest of the agent definition: publishing a version snapshots the graph, and a draft edit reaches no session until it is published and routed.
              - `entry` — string **(required)** — Step the graph starts at. Must be one of `steps`. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
              - `steps` — array **(required)** — Steps of one graph. Ids are unique within it. _(minItems=1; maxItems=200)_
                - _(nesting depth limit — see `AgentWorkflowStep` in the Schemas appendix)_
              - `nested` — array — Graphs the main workflow can run, referenced by `workflow` steps.
                - _(nesting depth limit — see `AgentWorkflowNested` in the Schemas appendix)_
              - `settings` — AgentWorkflowSettings
                - _(nesting depth limit — see `AgentWorkflowSettings` in the Schemas appendix)_
            - `guardrails` — AgentGuardrails — Turn screening, by side. Only `input` exists: it guards what reaches the model, and output screening is a separate policy with different actions, added here when it is built.
              - `input` — AgentGuardrailInput — Screening applied to what reaches the model. There is deliberately no bundle or preset-group member. A named group that expands to a set of checks reads like convenience and behaves like version skew: the same agent definition would mean different things before and after a platform release, invisibly to the tenant who published it. Listing the checks costs a few lines in a document the console writes anyway, and the published version then states exactly what it enforces. There is also no set-level default action. One field standing behind every check reads as a convenience and hides the thing a reader most needs to see: what a given check will actually do. A check's action is its own or its preset's, and both are visible on the check.
                - _(nesting depth limit — see `AgentGuardrailInput` in the Schemas appendix)_
            - `model` — string — Defaults to the platform default model when omitted. _(pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
            - `timeZone` — string — IANA timezone the agent reasons about time in: it anchors the current date and time given to the model and how times are read from and written to tool arguments and replies. Shared by every channel the agent serves. Defaults to 'UTC'. _(minLen=1; maxLen=64)_
            - `artifacts` — boolean — Whether the agent can produce artifacts (wilma-artifacts): files it writes in its sandbox and shares back during a session — a document, a PDF, a spreadsheet, a chart, a multi-page web site, a folder of files. Needs the sandbox capability. An artifact starts private to the user the session runs for, who can share it company-wide from the viewer; on the chat channel the runtime shares each one company-wide as it is created, so the link posted into the conversation opens for every signed-in colleague. Artifacts are company-internal: recipients on external transports (sms / whatsapp) or outside the company cannot open the links, so keep this disabled for customer-facing agents. Defaults to false.
            - `skills` — array — Skills attached to this agent (progressive disclosure). A skill may carry its own tools, which join this agent's toolset while that skill is active.
              - _array of_ `AgentSkillReference`
                - _(nesting depth limit — see `AgentSkillReference` in the Schemas appendix)_
            - `capabilities` — array — Everything the agent can do. When a `workflow` is set these are the capabilities in scope at every step, and a step may add to them or narrow them with its own list of the same shape.
              - _array of_ `AgentCapability`
                - _(nesting depth limit — see `AgentCapability` in the Schemas appendix)_
            - `variables` — array
              - _array of_ `AgentVariable`
                - _(nesting depth limit — see `AgentVariable` in the Schemas appendix)_
        - **`webhook`**
          - `webhook` — AgentWebhookEngine **(required)** — Bring-your-own backend over HTTPS. The platform POSTs call events to the URL; the backend answers out of band through the channel's command API. The response body is not read.
            - `url` — string **(required)**
            - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
              - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
            - `timeout` — number — Timeout of one delivery, in milliseconds. _(default=10000; min=5000; max=120000)_
        - **`sqs`**
          - `sqs` — AgentSqsEngine **(required)** — Bring-your-own backend over SQS. The platform sends call events to the queue; the backend answers out of band through the channel's command API.
            - `url` — string **(required)**
            - `key` — string **(required)**
            - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
              - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
    - `settings` — AgentSettings — Agent-level settings shared across all channels.
      - `pbxGroupId` — string — PBX group used for data ACL (e.g. Sales Intelligence lookups).
    - `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
      - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
      - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
        - _array of_ `AgentGrantPrincipal`
          - _oneOf_ — exactly one of:
            - **`userId`**
              - `userId` — string **(required)** _(minLen=12; maxLen=12)_
            - **`groupId`**
              - `groupId` — string **(required)**
            - **`department`**
              - `department` — string **(required)** — PBX department NAME, as carried on the colleague record (`PbxColleague.department`), not a department id. The x-bees directory knows a colleague's department only by name, so matching by name is what lets the check read a field the runtime already has instead of resolving the PBX department tree on every request. Two consequences: renaming a department in the PBX invalidates every grant naming it, and two departments with the same name in different branches of the tree are one value here.
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
    - `updatedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `updatedBy` — Actor — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
    - `latestVersion` — number — Latest published version number; absent while the agent is still a draft. _(min=1)_
    - `draftBaseVersion` — number — Published version number from which the current draft originated. Absent before the first version is published. _(min=1)_
    - `deployment` — array — How new sessions are split across published versions. Absent while the agent is still a draft. _(minItems=1; maxItems=10)_
      - _array of_ `AgentDeploymentRoute`
        - `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
        - `percentage` — number **(required)** — Percentage of new sessions routed to this version. Percentages must sum to 100. _(min=1; max=100)_
- Errors: `400`, `404`, `409`

### Deployment

#### `GET` `/v2/agents/agents/{agentId}/deployment`

Retrieves how new sessions are currently split across the agent's published versions.

- operationId: `GetAgentDeployment`
- **Scopes**: `wilma-agents:GetAgentDeployment`, `wilma-agents:read`
- **Parameters**
  - `agentId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Response 200** (`GetAgentDeploymentResponseContent`)
  - `deployment` — array — Absent while the agent has no published version serving traffic. _(minItems=1; maxItems=10)_
    - _array of_ `AgentDeploymentRoute`
      - `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
      - `percentage` — number **(required)** — Percentage of new sessions routed to this version. Percentages must sum to 100. _(min=1; max=100)_
- Errors: `400`, `404`

#### `PUT` `/v2/agents/agents/{agentId}/deployment`

Sets how new sessions are split across the agent's published versions, e.g. 80% on version 1 and 20% on version 2. Percentages must total 100. Running sessions keep the version they started on.

- operationId: `PutAgentDeployment`
- **Scopes**: `wilma-agents:PutAgentDeployment`
- **Parameters**
  - `agentId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `PutAgentDeploymentRequestContent`) **(required)**
  - `deployment` — array **(required)** — Weighted routing over distinct published versions. Percentages must sum to 100; a single entry at 100 serves one version to everyone. _(minItems=1; maxItems=10)_
    - _array of_ `AgentDeploymentRoute`
      - `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
      - `percentage` — number **(required)** — Percentage of new sessions routed to this version. Percentages must sum to 100. _(min=1; max=100)_
- **Response 200** (`PutAgentDeploymentResponseContent`)
  - `deployment` — array **(required)** — Weighted routing over distinct published versions. Percentages must sum to 100; a single entry at 100 serves one version to everyone. _(minItems=1; maxItems=10)_
    - _array of_ `AgentDeploymentRoute`
      - `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
      - `percentage` — number **(required)** — Percentage of new sessions routed to this version. Percentages must sum to 100. _(min=1; max=100)_
- Errors: `400`, `404`

#### `POST` `/v2/agents/agents/{agentId}/deployment/reset`

Resets the deployment to the default: 100% of new sessions on the latest published version. Fails with ConflictException while the agent has no published version.

- operationId: `ResetAgentDeployment`
- **Scopes**: `wilma-agents:ResetAgentDeployment`
- **Parameters**
  - `agentId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Response 200** (`ResetAgentDeploymentResponseContent`)
  - `deployment` — array **(required)** — Weighted routing over distinct published versions. Percentages must sum to 100; a single entry at 100 serves one version to everyone. _(minItems=1; maxItems=10)_
    - _array of_ `AgentDeploymentRoute`
      - `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
      - `percentage` — number **(required)** — Percentage of new sessions routed to this version. Percentages must sum to 100. _(min=1; max=100)_
- Errors: `400`, `404`, `409`

### ApiKeys

#### `GET` `/v2/agents/agents/{agentId}/keys`

Lists the API keys of an agent. Secrets are never returned.

- operationId: `ListAgentApiKeys`
- **Scopes**: `wilma-agents:ListAgentApiKeys`, `wilma-agents:read`
- **Parameters**
  - `agentId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Response 200** (`ListAgentApiKeysResponseContent`)
  - `keys` — array **(required)**
    - _array of_ `AgentApiKey`
      - `id` — string **(required)** _(minLen=12; maxLen=12)_
      - `name` — string _(minLen=1; maxLen=64)_
      - `prefix` — string **(required)** — Non-secret prefix of the key, e.g. 'sk-a1b2', for display purposes.
      - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
        - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
        - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
        - `name` — string — Human readable name of the actor at the time of the action.
      - `expiresAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `lastUsedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- Errors: `400`, `404`

#### `POST` `/v2/agents/agents/{agentId}/keys`

Creates a new API key for an agent. The secret is returned only in this response and cannot be retrieved later.

- operationId: `CreateAgentApiKey`
- **Scopes**: `wilma-agents:CreateAgentApiKey`
- **Parameters**
  - `agentId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `CreateAgentApiKeyRequestContent`)
  - `name` — string _(minLen=1; maxLen=64)_
  - `expiresAt` — string — Optional expiry; the key stops working after this time.
- **Response 200** (`CreateAgentApiKeyResponseContent`)
  - `key` — AgentApiKey **(required)**
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `name` — string _(minLen=1; maxLen=64)_
    - `prefix` — string **(required)** — Non-secret prefix of the key, e.g. 'sk-a1b2', for display purposes.
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
    - `expiresAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `lastUsedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `secret` — string **(required)** — The full secret. Shown only once.
- Errors: `400`, `404`

#### `DELETE` `/v2/agents/agents/{agentId}/keys/{keyId}`

Revokes an API key.

- operationId: `DeleteAgentApiKey`
- **Scopes**: `wilma-agents:DeleteAgentApiKey`
- **Parameters**
  - `agentId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `keyId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- Errors: `400`, `404`

### Schemas appendix — Wilma Agents API

<details><summary>179 component schemas</summary>

**`Actor`**

_Who performed an action: an interactive user, an API key or an internal service._

- `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
- `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
- `name` — string — Human readable name of the actor at the time of the action.

**`ActorType`**

- string _(enum: `user`, `api_key`, `service`)_

**`Agent`**

_The complete, versionable configuration of an agent. This is what gets snapshotted when a version is published._

- `name` — string **(required)** _(minLen=3; maxLen=255)_
- `description` — string _(minLen=1; maxLen=1000)_
- `category` — string — Category of the agent, e.g.: 'Support'. _(minLen=1; maxLen=128)_
- `picture` — string — Avatar URL.
- `channels` — AgentChannels **(required)** — The channels an agent serves and their channel-specific settings. Presence of a member enables that channel. Empty means the agent serves no channel: it is not reachable on its own and runs only as an automation's task or when another agent calls it. Enabled channels are mirrored as ChannelType values on AgentInfo.
  - `voice` — VoiceChannelSettings — Voice channel settings. Note: a voice agent's AgentAccess.grants are ignored — inbound calls are routed by the PBX dialplan and data ACL is the agent-level `settings.pbxGroupId`, not per-user grants.
    - `greeting` — string — Message spoken when the call starts.
    - `backgroundSound` — VoiceBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT like `interruptions` and `endCall`, rather than a loose name on the channel: it is one switchable call behaviour, it reads the same way as its siblings, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
      - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
      - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
    - `speech` — VoiceSpeechSettings — Speech configuration for the voice channel. When present it WINS over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the single exception, because it is the channel's own input signal and the feature has no starting point without it.
      - `languages` — array **(required)** — Configured languages. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once: automatic detection here is opt-in (`transcription.autoDetect`), and once a caller turns it on, the service does not clamp the resulting candidate list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five) — a caller who both opts in and configures more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. With detection off, only the single resolved language is ever sent, so the ceiling never becomes a candidate-list problem at all. _(minItems=1; maxItems=10)_
        - _(nesting depth limit — see `VoiceLanguage` in the Schemas appendix)_
      - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in the voice, provider account and pronunciation rules of its own language, instead of only the language the call resolved to. Languages whose first message is empty, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
      - `transcription` — VoiceTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
        - _(nesting depth limit — see `VoiceTranscriptionSettings` in the Schemas appendix)_
    - `interruptions` — VoiceInterruptionSettings
      - `enabled` — boolean **(required)** — Whether the caller can interrupt the agent while it is speaking.
      - `minWords` — number — Minimum number of caller words that count as an interruption. _(min=1; max=10)_
    - `silenceTimeout` — VoiceSilenceTimeoutSettings
      - `seconds` — number **(required)** — Seconds of caller silence before the action is taken. _(min=1; max=600)_
      - `action` — union **(required)**
        - _(nesting depth limit — see `VoiceTerminateAction` in the Schemas appendix)_
    - `maxDuration` — VoiceMaxDurationSettings
      - `seconds` — number **(required)** — Maximum call duration in seconds before the action is taken. _(min=10; max=14400)_
      - `action` — union **(required)**
        - _(nesting depth limit — see `VoiceTerminateAction` in the Schemas appendix)_
    - `endCall` — VoiceEndCallSettings
      - `enabled` — boolean **(required)**
      - `phrases` — string — Comma-separated phrases that end the call, e.g. 'goodbye,bye'.
    - `callerMetadata` — VoiceCallerMetadataSettings — Caller context injected into the model prompt.
      - `callerName` — boolean — Include the caller name. Defaults to true.
      - `callerNumber` — boolean — Include the caller phone number. Defaults to true.
      - `callerEmail` — boolean — Include the caller email when known. Defaults to false.
      - `callerCompany` — boolean — Include the caller company when known. Defaults to false.
      - `time` — boolean — Include the current time, rendered in the agent's `engine.ai.timeZone`. Defaults to false.
  - `chat` — ChatChannelSettings
    - `discoverable` — boolean — Whether users can find and add this agent to conversations.
    - `sessionTimeoutMinutes` — number — Minutes a conversation can stay idle before the next message starts a new session. Omit to start a new session at the end of the agent's local day (`engine.ai.timeZone`). Allowed values: 15, 30, 60, 120. _(min=15; max=120)_
    - `verbosity` — string — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
  - `assistant` — AssistantChannelSettings — Assistant channel settings. Presence enables the in-app assistant surface; audio remains unavailable unless its separate settings are present and enabled.
    - `default` — boolean — Offer this agent as the default assistant for users covered by the agent access settings.
    - `ui` — AssistantUiSettings — How the agent presents itself in the assistant UI: what the user reads before typing anything, and what they can start from without typing at all. Everything here is presentation — it never changes what the agent can do.
      - `welcome` — AssistantWelcomeSettings — Greeting shown on an empty thread, above the quick commands.
        - _(nesting depth limit — see `AssistantWelcomeSettings` in the Schemas appendix)_
      - `commands` — array — Cards offered under the welcome message on an empty thread, in the order given. Empty or omitted shows no cards. _(maxItems=8)_
        - _(nesting depth limit — see `AssistantQuickCommand` in the Schemas appendix)_
      - `placeholder` — string — Placeholder text in the composer, e.g. 'Ask about an account…'. Defaults to the client's own placeholder when omitted. _(minLen=1; maxLen=100)_
    - `audio` — AssistantAudioSettings — Switchable audio for the assistant channel. The settings object keeps enablement beside its speech policy, matching the voice channel's switchable blocks so a disabled configuration can be retained without serving audio.
      - `enabled` — boolean **(required)** — Whether the assistant accepts audio calls. Required so the presence of saved speech configuration is never mistaken for enablement.
      - `speech` — AssistantSpeechSettings — Recognition and synthesis policy for assistant audio. This is assistant-owned rather than a VoiceSpeechSettings reuse so telephony and assistant audio can evolve independently. It has no language greeting and no greet-every-language switch because an assistant conversation is already open when its audio call starts, leaving nothing for the channel to greet.
        - _(nesting depth limit — see `AssistantSpeechSettings` in the Schemas appendix)_
- `engine` — union **(required)** — How the agent produces replies. `ai` is the managed engine; `webhook` and `sqs` delegate to an external backend.
  - _oneOf_ — exactly one of:
    - **`ai`**
      - `ai` — AgentAiEngine **(required)** — Managed AI engine: the platform runs the model, tools and knowledge lookups.
        - `instructions` — string **(required)** _(minLen=1; maxLen=60000)_
        - `workflow` — AgentWorkflow — The agent's conversation as a graph: which step runs first, what each step does, and on what condition control moves on. Optional on AgentAiEngine — without one the agent is prompt-driven, steered by `instructions` and free to use its capabilities in any order. Versioned with the rest of the agent definition: publishing a version snapshots the graph, and a draft edit reaches no session until it is published and routed.
          - _(nesting depth limit — see `AgentWorkflow` in the Schemas appendix)_
        - `guardrails` — AgentGuardrails — Turn screening, by side. Only `input` exists: it guards what reaches the model, and output screening is a separate policy with different actions, added here when it is built.
          - _(nesting depth limit — see `AgentGuardrails` in the Schemas appendix)_
        - `model` — string — Defaults to the platform default model when omitted. _(pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
        - `timeZone` — string — IANA timezone the agent reasons about time in: it anchors the current date and time given to the model and how times are read from and written to tool arguments and replies. Shared by every channel the agent serves. Defaults to 'UTC'. _(minLen=1; maxLen=64)_
        - `artifacts` — boolean — Whether the agent can produce artifacts (wilma-artifacts): files it writes in its sandbox and shares back during a session — a document, a PDF, a spreadsheet, a chart, a multi-page web site, a folder of files. Needs the sandbox capability. An artifact starts private to the user the session runs for, who can share it company-wide from the viewer; on the chat channel the runtime shares each one company-wide as it is created, so the link posted into the conversation opens for every signed-in colleague. Artifacts are company-internal: recipients on external transports (sms / whatsapp) or outside the company cannot open the links, so keep this disabled for customer-facing agents. Defaults to false.
        - `skills` — array — Skills attached to this agent (progressive disclosure). A skill may carry its own tools, which join this agent's toolset while that skill is active.
          - _(nesting depth limit — see `AgentSkillReference` in the Schemas appendix)_
        - `capabilities` — array — Everything the agent can do. When a `workflow` is set these are the capabilities in scope at every step, and a step may add to them or narrow them with its own list of the same shape.
          - _(nesting depth limit — see `AgentCapability` in the Schemas appendix)_
        - `variables` — array
          - _(nesting depth limit — see `AgentVariable` in the Schemas appendix)_
    - **`webhook`**
      - `webhook` — AgentWebhookEngine **(required)** — Bring-your-own backend over HTTPS. The platform POSTs call events to the URL; the backend answers out of band through the channel's command API. The response body is not read.
        - `url` — string **(required)**
        - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
          - _(nesting depth limit — see `SecretRef` in the Schemas appendix)_
        - `timeout` — number — Timeout of one delivery, in milliseconds. _(default=10000; min=5000; max=120000)_
    - **`sqs`**
      - `sqs` — AgentSqsEngine **(required)** — Bring-your-own backend over SQS. The platform sends call events to the queue; the backend answers out of band through the channel's command API.
        - `url` — string **(required)**
        - `key` — string **(required)**
        - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
          - _(nesting depth limit — see `SecretRef` in the Schemas appendix)_
- `settings` — AgentSettings — Agent-level settings shared across all channels.
  - `pbxGroupId` — string — PBX group used for data ACL (e.g. Sales Intelligence lookups).
- `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
  - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
  - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
    - _array of_ `AgentGrantPrincipal`
      - _oneOf_ — exactly one of:
        - **`userId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`groupId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`department`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
- `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
  - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
  - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
  - `name` — string — Human readable name of the actor at the time of the action.
- `updatedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `updatedBy` — Actor — Who performed an action: an interactive user, an API key or an internal service.
  - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
  - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
  - `name` — string — Human readable name of the actor at the time of the action.
- `id` — string **(required)** _(minLen=12; maxLen=12)_
- `status` — string **(required)** _(enum: `draft`, `active`)_
- `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
- `latestVersion` — number — Latest published version number; absent while the agent is still a draft. _(min=1)_
- `draftBaseVersion` — number — Published version number from which the current draft originated. Absent before the first version is published. _(min=1)_
- `deployment` — array — How new sessions are split across published versions. Absent while the agent is still a draft. _(minItems=1; maxItems=10)_
  - _array of_ `AgentDeploymentRoute`
    - `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
    - `percentage` — number **(required)** — Percentage of new sessions routed to this version. Percentages must sum to 100. _(min=1; max=100)_

**`AgentAccess`**

_Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access)._

- `visibility` — string _(enum: `explicit`, `organization`, `public`)_
- `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
  - _array of_ `AgentGrantPrincipal`
    - _oneOf_ — exactly one of:
      - **`userId`**
        - `userId` — string **(required)** _(minLen=12; maxLen=12)_
      - **`groupId`**
        - `groupId` — string **(required)**
      - **`department`**
        - `department` — string **(required)** — PBX department NAME, as carried on the colleague record (`PbxColleague.department`), not a department id. The x-bees directory knows a colleague's department only by name, so matching by name is what lets the check read a field the runtime already has instead of resolving the PBX department tree on every request. Two consequences: renaming a department in the PBX invalidates every grant naming it, and two departments with the same name in different branches of the tree are one value here.

**`AgentAiEngine`**

_Managed AI engine: the platform runs the model, tools and knowledge lookups._

- `instructions` — string **(required)** _(minLen=1; maxLen=60000)_
- `workflow` — AgentWorkflow — The agent's conversation as a graph: which step runs first, what each step does, and on what condition control moves on. Optional on AgentAiEngine — without one the agent is prompt-driven, steered by `instructions` and free to use its capabilities in any order. Versioned with the rest of the agent definition: publishing a version snapshots the graph, and a draft edit reaches no session until it is published and routed.
  - `entry` — string **(required)** — Step the graph starts at. Must be one of `steps`. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
  - `steps` — array **(required)** — Steps of one graph. Ids are unique within it. _(minItems=1; maxItems=200)_
    - _array of_ `AgentWorkflowStep`
      - `id` — string **(required)** — Identifier of a step within its workflow, unique per workflow (the main graph and each nested workflow are separate scopes). Stable and machine-facing: transitions reference it, and a result step's id is the name a caller branches on, so renaming a step's `label` never unwires the graph. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
      - `label` — string **(required)** — Human readable name of a step, e.g. 'Transfer to the sales desk'. Shown in the builder and in traces, and read by the model too: when this step is an exit of the live step, the label is the preview offered alongside the exit's condition. Never a routing key — see AgentWorkflowStepId — so renaming one never unwires a graph. _(minLen=1; maxLen=128)_
      - `stage` — string — The phase this step belongs to. Inherited by steps downstream, so a handful of tags organise a long graph. _(minLen=1; maxLen=64)_
      - `handler` — union **(required)** — What a step does. Exactly one member is set. `action` carries a capability; the others are workflow-only handlers with no capability equivalent.
        - _(nesting depth limit — see `AgentWorkflowHandler` in the Schemas appendix)_
      - `transitions` — array — The ways out of this step. Must be non-empty on every step that stays in the session, since a step the runtime cannot leave is a dead end. On `result` and `end` it must be empty. On the `action` members that leave the session (`handover`, `delegation`, `transfer`, `hangup`) it may carry `failure` transitions and nothing else: an action that was supposed to leave and failed — a busy extension, a service desk with nobody on it — has not left, and a graph with no answer for that drops the caller.
        - _(nesting depth limit — see `AgentWorkflowTransition` in the Schemas appendix)_
      - `position` — AgentWorkflowStepPosition — Canvas coordinates of a step in the builder. Authoring metadata: the runtime ignores it, and a workflow that arrives without positions is laid out automatically.
        - _(nesting depth limit — see `AgentWorkflowStepPosition` in the Schemas appendix)_
  - `nested` — array — Graphs the main workflow can run, referenced by `workflow` steps.
    - _array of_ `AgentWorkflowNested`
      - `entry` — string **(required)** — Step the graph starts at. Must be one of `steps`. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
      - `steps` — array **(required)** — Steps of one graph. Ids are unique within it. _(minItems=1; maxItems=200)_
        - _(nesting depth limit — see `AgentWorkflowStep` in the Schemas appendix)_
      - `id` — string **(required)** — Identifier of a nested workflow within the agent's workflow. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
      - `name` — string **(required)** _(minLen=1; maxLen=128)_
      - `description` — string — One line saying what the nested workflow is for, shown on the step that runs it. _(minLen=1; maxLen=1000)_
  - `settings` — AgentWorkflowSettings
    - `maxTransitions` — number — Give up after this many step transitions, so a cycle whose conditions all keep matching cannot run forever. Absent means no limit, which is the default: a deliberate loop — 'keep asking until you have the postcode' — is a normal shape, and silently capping it would be worse than making the author say so. _(min=1; max=500)_
    - `variables` — array — Workflow variables seeded before the first step runs. Agent input variables (`engine.ai.variables`) are already in scope and need no entry here.
      - _array of_ `AgentWorkflowAssignment`
        - _(nesting depth limit — see `AgentWorkflowAssignment` in the Schemas appendix)_
    - `layout` — string — How the builder arranges the graph. Authoring metadata: the runtime ignores it. `stages` bands the graph by `stage`, which is what a forty-step workflow needs. _(enum: `flow`, `compact`, `stages`)_
- `guardrails` — AgentGuardrails — Turn screening, by side. Only `input` exists: it guards what reaches the model, and output screening is a separate policy with different actions, added here when it is built.
  - `input` — AgentGuardrailInput — Screening applied to what reaches the model. There is deliberately no bundle or preset-group member. A named group that expands to a set of checks reads like convenience and behaves like version skew: the same agent definition would mean different things before and after a platform release, invisibly to the tenant who published it. Listing the checks costs a few lines in a document the console writes anyway, and the published version then states exactly what it enforces. There is also no set-level default action. One field standing behind every check reads as a convenience and hides the thing a reader most needs to see: what a given check will actually do. A check's action is its own or its preset's, and both are visible on the check.
    - `checks` — array — The checks to run, evaluated together in one call. Absent or empty means no screening. _(maxItems=30)_
      - _array of_ `AgentGuardrailCheck`
        - _(nesting depth limit — see `AgentGuardrailCheck` in the Schemas appendix)_
    - `model` — string — The model that runs the checks. Defaults to the platform's guardrail model — deliberately small and fast, and deliberately not the agent's own, whose cost and latency are what this exists to avoid spending on a bad turn. _(pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
    - `action` — union — What happens when a check trips. Exactly one member is set. Ordered by severity: observe < redact < block < end. When more than one check trips in the same call the most severe action wins and ties break on the order of `checks`, so a set can mix an observed check with an enforced one without the observation weakening the enforcement. There is no hand-over member yet. Handing a session to a human is a different mechanism on every channel — a voice transfer, a chat assignment, an assistant with no human behind it — and wiring a guardrail into all of them is out of proportion to the rest of this feature. Until AgentHandoverCapability has a runtime on more than one channel, the crisis path is a block whose message routes the caller.
      - _oneOf_ — exactly one of:
        - **`observe`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`redact`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`block`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`end`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `mode` — string — Runs the checker before the agent's model (BLOCKING) or alongside it (PARALLEL). Blocking costs the checker's latency on every turn but guarantees that a refused turn spent no tokens and fired no tool; parallel adds no latency and is the right trade on voice, where the delay is audible, at the risk that part of a reply reaches the caller and that a tool has already run before the cancellation lands. Defaults to BLOCKING. _(enum: `blocking`, `parallel`)_
    - `errorMode` — string — What happens when the checker itself errors or times out. OPEN lets the turn through unscreened and records GuardrailFailedEvent, so an unscreened turn is a fact in the log rather than an absence; CLOSED refuses it. Defaults to OPEN: an agent that stops answering because a small model had a bad minute is a worse and far likelier outage than the rare turn that goes unscreened. Background tasks, where nobody is waiting and a retry is free, are the case for CLOSED. _(enum: `open`, `closed`)_
    - `window` — string — How much of the conversation the checker sees. Defaults to LAST_WITH_PRIOR, because the jailbreaks worth catching are built across several turns — establish a fiction, then cash it in — and a checker shown only the last turn sees an innocuous sentence. There is no full-transcript option: screening a whole call on every turn would make the guardrail dearer than the agent. _(enum: `lastMessage`, `lastWithPrior`)_
- `model` — string — Defaults to the platform default model when omitted. _(pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
- `timeZone` — string — IANA timezone the agent reasons about time in: it anchors the current date and time given to the model and how times are read from and written to tool arguments and replies. Shared by every channel the agent serves. Defaults to 'UTC'. _(minLen=1; maxLen=64)_
- `artifacts` — boolean — Whether the agent can produce artifacts (wilma-artifacts): files it writes in its sandbox and shares back during a session — a document, a PDF, a spreadsheet, a chart, a multi-page web site, a folder of files. Needs the sandbox capability. An artifact starts private to the user the session runs for, who can share it company-wide from the viewer; on the chat channel the runtime shares each one company-wide as it is created, so the link posted into the conversation opens for every signed-in colleague. Artifacts are company-internal: recipients on external transports (sms / whatsapp) or outside the company cannot open the links, so keep this disabled for customer-facing agents. Defaults to false.
- `skills` — array — Skills attached to this agent (progressive disclosure). A skill may carry its own tools, which join this agent's toolset while that skill is active.
  - _array of_ `AgentSkillReference`
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `skillVersion` — number — Pin a specific published skill version. When omitted, latestVersion is resolved. _(min=1)_
    - `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
      - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
      - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
        - _(nesting depth limit — see `AgentGrantPrincipal` in the Schemas appendix)_
- `capabilities` — array — Everything the agent can do. When a `workflow` is set these are the capabilities in scope at every step, and a step may add to them or narrow them with its own list of the same shape.
  - _array of_ `AgentCapability`
    - _oneOf_ — exactly one of:
      - **`tool`**
        - `tool` — AgentTool **(required)**
          - _(nesting depth limit — see `AgentTool` in the Schemas appendix)_
      - **`connector`**
        - `connector` — AgentConnectorCapability **(required)** — A configured connector (wilma-tools) exposed to the model as a single meta-tool named after the connector. The model calls the reserved `help` action to learn the callable actions, then dispatches an action through the same tool. Progressive disclosure runs through the connector tool itself, not the skills catalogue.
          - _(nesting depth limit — see `AgentConnectorCapability` in the Schemas appendix)_
      - **`kb`**
        - `kb` — AgentKnowledgeBase **(required)**
          - _(nesting depth limit — see `AgentKnowledgeBase` in the Schemas appendix)_
      - **`sandbox`**
        - `sandbox` — union **(required)** — Embedded sandbox: shell + file tools backed by an execution environment. The only capability with no `channels` list — being a union it has nowhere to carry one — so it is offered on every channel the agent serves.
          - _(nesting depth limit — see `AgentSandboxCapability` in the Schemas appendix)_
      - **`webSearch`**
        - `webSearch` — AgentWebSearchCapability **(required)** — Model-native web search. The provider tool is selected from the agent model.
          - _(nesting depth limit — see `AgentWebSearchCapability` in the Schemas appendix)_
      - **`webFetch`**
        - `webFetch` — AgentWebFetchCapability **(required)** — Server-side fetch of a URL, returning its readable text/markdown to the model.
          - _(nesting depth limit — see `AgentWebFetchCapability` in the Schemas appendix)_
      - **`agent`**
        - `agent` — AgentCallCapability **(required)** — Invoke another agent as a dedicated execution with its own state. The called agent runs independently and returns its result.
          - _(nesting depth limit — see `AgentCallCapability` in the Schemas appendix)_
      - **`handover`**
        - `handover` — AgentHandoverCapability **(required)** — Hand the conversation over to a human and leave it. Honoured on conversation channels (chat, assistant).
          - _(nesting depth limit — see `AgentHandoverCapability` in the Schemas appendix)_
      - **`delegation`**
        - `delegation` — AgentDelegationCapability **(required)** — Delegate the conversation to another agent (max 3 transitions per turn). One capability entry per delegate target.
          - _(nesting depth limit — see `AgentDelegationCapability` in the Schemas appendix)_
      - **`transfer`**
        - `transfer` — AgentTransferCapability **(required)** — Transfer the call to a PBX destination. Honoured on the voice channel. One capability entry per transfer target.
          - _(nesting depth limit — see `AgentTransferCapability` in the Schemas appendix)_
      - **`suggestions`**
        - `suggestions` — AgentSuggestionsCapability **(required)** — Emit suggested replies for human operators. Honoured on the chat channel.
          - _(nesting depth limit — see `AgentSuggestionsCapability` in the Schemas appendix)_
      - **`hangup`**
        - `hangup` — AgentHangupCapability **(required)** — Let the model end the call. Honoured on the voice channel.
          - _(nesting depth limit — see `AgentHangupCapability` in the Schemas appendix)_
      - **`wait`**
        - `wait` — AgentWaitCapability **(required)** — Let the model hold the call while it works (e.g. a lookup), keeping the caller on the line. Honoured on the voice channel.
          - _(nesting depth limit — see `AgentWaitCapability` in the Schemas appendix)_
- `variables` — array
  - _array of_ `AgentVariable`
    - `name` — string **(required)** _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
    - `type` — string **(required)** _(enum: `string`, `number`, `boolean`, `string_array`, `number_array`)_
    - `optional` — boolean **(required)**
    - `description` — string — What the variable means and how it should be filled.

**`AgentApiKey`**

- `id` — string **(required)** _(minLen=12; maxLen=12)_
- `name` — string _(minLen=1; maxLen=64)_
- `prefix` — string **(required)** — Non-secret prefix of the key, e.g. 'sk-a1b2', for display purposes.
- `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
  - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
  - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
  - `name` — string — Human readable name of the actor at the time of the action.
- `expiresAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `lastUsedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.

**`AgentCallCapability`**

_Invoke another agent as a dedicated execution with its own state. The called agent runs independently and returns its result._

- `agentId` — string **(required)** _(minLen=12; maxLen=12)_
- `agentVersion` — number — Pin a specific published version of the called agent. When absent, the called agent's deployment configuration selects the version at invocation time. _(min=1)_
- `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
  - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
  - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
    - _array of_ `AgentGrantPrincipal`
      - _oneOf_ — exactly one of:
        - **`userId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`groupId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`department`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
- `variables` — array
  - _array of_ `AgentToolVariable`
    - `name` — string **(required)** — Name of the tool variable, e.g.: 'myvar' _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
    - `handler` — union
      - _oneOf_ — exactly one of:
        - **`auto`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`guided`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`predefined`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
- `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
  - _array of_ `ChannelType`

**`AgentCapability`**

- _oneOf_ — exactly one of:
  - **`tool`**
    - `tool` — AgentTool **(required)**
      - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `toolVersion` — number — Pin a specific published tool version. When omitted, the tool's latestVersion is resolved at load, so a republished tool reaches this agent without a new agent version. Pin it when `fields` must keep aiming at an exact input schema. _(min=1)_
      - `description` — string — Override the tool's description for this agent. When omitted, the tool's own description is used. _(minLen=1; maxLen=4096)_
      - `fields` — array — Per-field overrides on the tool input schema: pin fixed values (hidden from the model) or refine field descriptions. Fields not listed are filled by the model per the tool schema. Paths are resolved against the input schema of the tool version in effect — pin `toolVersion` when they must not move.
        - _array of_ `AgentToolField`
          - _(nesting depth limit — see `AgentToolField` in the Schemas appendix)_
      - `startMessage` — string — Message spoken when the tool call starts. Honoured on the voice channel. Spoken in every language of the call while `startMessages` is absent or empty; not consulted once `startMessages` carries any entry.
      - `startMessages` — array — Per-language start messages. When present and non-empty, the entry for the call's current language is spoken and `startMessage` is not consulted; a language with no entry is silent. When absent or empty, `startMessage` is spoken as before. On a call with no effective speech configuration — no configured languages, or a PBX below protocol 2 — `startMessage` is spoken regardless, because there is no current language to choose by.
        - _array of_ `AgentSpokenPhrase`
          - _(nesting depth limit — see `AgentSpokenPhrase` in the Schemas appendix)_
      - `pipeline` — AgentToolPipeline
        - `type` — string — How the model waits for a tool and whether it synthesizes a reply from the result. _(enum: `blocking_request`, `blocking_request_guided`, `async_request`, `async_request_guided`)_
        - `instructions` — string — Reply instructions for the *_GUIDED pipeline types. Use {{response}} to reference the tool result.
      - `approval` — AgentToolApproval — Human-in-the-loop confirmation for a tool. Presence requires approval: the agent pauses before running the tool and the session user (whoever controls the session) approves or denies inline.
        - `prompt` — string — Optional message shown in the confirmation prompt. Supports handlebars against agent variables and the pending tool arguments. When omitted, a default prompt is shown.
      - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
        - _array of_ `ChannelType`
      - `annotations` — array
        - _array of_ `AgentToolAnnotation`
          - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
  - **`connector`**
    - `connector` — AgentConnectorCapability **(required)** — A configured connector (wilma-tools) exposed to the model as a single meta-tool named after the connector. The model calls the reserved `help` action to learn the callable actions, then dispatches an action through the same tool. Progressive disclosure runs through the connector tool itself, not the skills catalogue.
      - `id` — string **(required)** — Configured connector instance in wilma-tools. Its pinned definition, permission `grant` and authorization govern what the model can discover via `help` and call. There is no version pin here, unlike `AgentTool.toolVersion`: the action catalogue and its schemas are already frozen by the connector's pinned definition, while `grant` and authorization are read live so permission changes apply at once. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `startMessage` — string — Message spoken when a connector action call starts. Honoured on the voice channel. Mirrors `AgentTool.startMessage`. Not applied to the read-only `help` action. Not consulted once `startMessages` carries any entry.
      - `startMessages` — array — Forward-compatible per-language connector start messages, mirroring `AgentTool.startMessages`. Accepted and stored so clients can configure connector and tool phrases consistently, but currently ignored at execution time because the voice runtime does not read connector start messages yet. Runtime enablement is tracked in wilma-services docs/todo.md item 8.
        - _array of_ `AgentSpokenPhrase`
          - _(nesting depth limit — see `AgentSpokenPhrase` in the Schemas appendix)_
      - `pipeline` — AgentToolPipeline
        - `type` — string — How the model waits for a tool and whether it synthesizes a reply from the result. _(enum: `blocking_request`, `blocking_request_guided`, `async_request`, `async_request_guided`)_
        - `instructions` — string — Reply instructions for the *_GUIDED pipeline types. Use {{response}} to reference the tool result.
      - `approval` — AgentToolApproval — Human-in-the-loop confirmation for a tool. Presence requires approval: the agent pauses before running the tool and the session user (whoever controls the session) approves or denies inline.
        - `prompt` — string — Optional message shown in the confirmation prompt. Supports handlebars against agent variables and the pending tool arguments. When omitted, a default prompt is shown.
      - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
        - _array of_ `ChannelType`
      - `annotations` — array
        - _array of_ `AgentToolAnnotation`
          - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
  - **`kb`**
    - `kb` — AgentKnowledgeBase **(required)**
      - `knowledgeBaseId` — string
      - `instructions` — string — Additional instructions for when the agent should use this knowledge base. _(minLen=1; maxLen=60000)_
      - `searchStrategy` — string — Search algorithm used to retrieve passages. _(enum: `bm25`, `vector`, `hybrid`)_
      - `searchThreshold` — string — Minimum similarity a passage needs to be returned. Raising it trades recall for precision. _(enum: `low`, `medium`, `high`)_
      - `searchLimit` — number — Maximum number of passages this capability returns. Defaults to the knowledge base service's own default (10) when omitted. Keep it low on voice: every passage is prompt the model reads before it can speak. _(min=1; max=50)_
      - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
        - _array of_ `ChannelType`
      - `annotations` — array
        - _array of_ `AgentToolAnnotation`
          - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
  - **`sandbox`**
    - `sandbox` — union **(required)** — Embedded sandbox: shell + file tools backed by an execution environment. The only capability with no `channels` list — being a union it has nowhere to carry one — so it is offered on every channel the agent serves.
      - _oneOf_ — exactly one of:
        - **`inline`**
          - `inline` — AgentInlineSandboxOptions **(required)** — Sandbox configured inline on the agent, without a pre-built snapshot.
            - _(nesting depth limit — see `AgentInlineSandboxOptions` in the Schemas appendix)_
        - **`snapshot`**
          - `snapshot` — AgentSnapshotSandboxOptions **(required)** — Sandbox launched from a pre-built snapshot managed by the wilma-sandbox service.
            - _(nesting depth limit — see `AgentSnapshotSandboxOptions` in the Schemas appendix)_
  - **`webSearch`**
    - `webSearch` — AgentWebSearchCapability **(required)** — Model-native web search. The provider tool is selected from the agent model.
      - `contextSize` — string — Search depth/context hint, mapped per provider. _(enum: `low`, `medium`, `high`)_
      - `allowedDomains` — array — Restrict results to these domains where the provider supports it.
        - _array of_ `string`
      - `userLocation` — WebSearchUserLocation
        - `country` — string — ISO 3166-1 alpha-2 country code, e.g. 'US'.
        - `region` — string
        - `city` — string
        - `timezone` — string — IANA timezone, e.g. 'Europe/Rome'.
      - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
        - _array of_ `ChannelType`
  - **`webFetch`**
    - `webFetch` — AgentWebFetchCapability **(required)** — Server-side fetch of a URL, returning its readable text/markdown to the model.
      - `allowedDomains` — array — Restrict fetches to these domains. Empty list means any domain is allowed.
        - _array of_ `string`
      - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
        - _array of_ `ChannelType`
  - **`agent`**
    - `agent` — AgentCallCapability **(required)** — Invoke another agent as a dedicated execution with its own state. The called agent runs independently and returns its result.
      - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
      - `agentVersion` — number — Pin a specific published version of the called agent. When absent, the called agent's deployment configuration selects the version at invocation time. _(min=1)_
      - `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
        - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
        - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
          - _(nesting depth limit — see `AgentGrantPrincipal` in the Schemas appendix)_
      - `variables` — array
        - _array of_ `AgentToolVariable`
          - _(nesting depth limit — see `AgentToolVariable` in the Schemas appendix)_
      - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
        - _array of_ `ChannelType`
  - **`handover`**
    - `handover` — AgentHandoverCapability **(required)** — Hand the conversation over to a human and leave it. Honoured on conversation channels (chat, assistant).
      - `name` — string — Tool name exposed to the model. Auto-generated when omitted.
      - `description` — string — Description for the model to decide when to hand over.
      - `variant` — string _(enum: `agent`, `service`)_
      - `agent` — string — Wilma agent to hand over to when variant = AGENT. _(minLen=12; maxLen=12)_
      - `agentVersion` — number — Pin a specific published version of the target agent when variant = AGENT. When absent, the target's deployment configuration selects the version at handover time. _(min=1)_
      - `service` — string — x-bees service id to hand over to when variant = SERVICE.
      - `silent` — boolean — Hand over without posting a visible message to the user.
      - `pipeline` — AgentHandoverPipeline
        - `type` — string _(enum: `handover`, `reply_and_handover`, `reply_instructed_and_handover`)_
        - `instructions` — string — Instructions for the model reply when type is REPLY_INSTRUCTED_AND_HANDOVER.
      - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
        - _array of_ `ChannelType`
      - `annotations` — array
        - _array of_ `AgentToolAnnotation`
          - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
  - **`delegation`**
    - `delegation` — AgentDelegationCapability **(required)** — Delegate the conversation to another agent (max 3 transitions per turn). One capability entry per delegate target.
      - `name` — string — Tool name exposed to the model. Auto-generated when omitted.
      - `description` — string — Description for the model to decide when to delegate.
      - `id` — string **(required)** — Agent to delegate to. _(minLen=12; maxLen=12)_
      - `agentVersion` — number — Pin a specific published version of the delegate agent. When absent, the delegate's deployment configuration selects the version at delegation time. _(min=1)_
      - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
        - _array of_ `ChannelType`
      - `annotations` — array
        - _array of_ `AgentToolAnnotation`
          - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
  - **`transfer`**
    - `transfer` — AgentTransferCapability **(required)** — Transfer the call to a PBX destination. Honoured on the voice channel. One capability entry per transfer target.
      - `name` — string — Tool name exposed to the model. Auto-generated when omitted.
      - `description` — string — Description for the model to decide when to transfer.
      - `variant` — string _(enum: `predefined`, `dynamic`, `directory`)_
      - `context` — string — Routing context for PREDEFINED transfers.
      - `extension` — string — Extension or phone number for PREDEFINED transfers.
      - `pipeline` — AgentTransferPipeline
        - `type` — string _(enum: `transfer`, `reply_and_transfer`, `reply_instructed_and_transfer`)_
        - `instructions` — string — Instructions for the model reply when type is REPLY_INSTRUCTED_AND_TRANSFER.
      - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
        - _array of_ `ChannelType`
      - `annotations` — array
        - _array of_ `AgentToolAnnotation`
          - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
  - **`suggestions`**
    - `suggestions` — AgentSuggestionsCapability **(required)** — Emit suggested replies for human operators. Honoured on the chat channel.
      - `name` — string — Tool name. Auto-generated when omitted.
      - `instructions` — string — Steers what the suggestions say. Appended to the platform's own generation prompt rather than replacing it, so the shape of a suggestion — short, tappable, a plausible next thing to send — stays the platform's to keep, and this narrows the subject: 'offer a callback and a link to the status page, never a discount'. NOT a tool description, unlike the `description` every other capability carries: suggestions are not a tool the model chooses to call. They are generated from a reply that has already been written, so there is no decision to describe — only the generation to steer. Absent means the platform's prompt alone. _(minLen=1; maxLen=2000)_
      - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
        - _array of_ `ChannelType`
      - `annotations` — array
        - _array of_ `AgentToolAnnotation`
          - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
  - **`hangup`**
    - `hangup` — AgentHangupCapability **(required)** — Let the model end the call. Honoured on the voice channel.
      - `name` — string — Tool name exposed to the model. Auto-generated when omitted.
      - `description` — string — Description for the model to decide when to hang up.
      - `pipeline` — AgentHangupPipeline
        - `type` — string _(enum: `hangup`, `reply_and_hangup`, `reply_instructed_and_hangup`)_
        - `instructions` — string — Instructions for the model reply when type is REPLY_INSTRUCTED_AND_HANGUP.
      - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
        - _array of_ `ChannelType`
      - `annotations` — array
        - _array of_ `AgentToolAnnotation`
          - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
  - **`wait`**
    - `wait` — AgentWaitCapability **(required)** — Let the model hold the call while it works (e.g. a lookup), keeping the caller on the line. Honoured on the voice channel.
      - `name` — string — Tool name exposed to the model. Auto-generated when omitted.
      - `description` — string — Description for the model to decide when to wait.
      - `message` — string — Message spoken when entering the wait state. Spoken in every language of the call while `messages` is absent or empty; not consulted once `messages` carries any entry.
      - `messages` — array — Per-language wait messages. Same rule as `AgentTool.startMessages`: the entry for the call's current language is spoken, a language with no entry is silent, and with no effective speech configuration `message` is spoken.
        - _array of_ `AgentSpokenPhrase`
          - _(nesting depth limit — see `AgentSpokenPhrase` in the Schemas appendix)_
      - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
        - _array of_ `ChannelType`
      - `annotations` — array
        - _array of_ `AgentToolAnnotation`
          - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_

**`AgentChannels`**

_The channels an agent serves and their channel-specific settings. Presence of a member enables that channel. Empty means the agent serves no channel: it is not reachable on its own and runs only as an automation's task or when another agent calls it. Enabled channels are mirrored as ChannelType values on AgentInfo._

- `voice` — VoiceChannelSettings — Voice channel settings. Note: a voice agent's AgentAccess.grants are ignored — inbound calls are routed by the PBX dialplan and data ACL is the agent-level `settings.pbxGroupId`, not per-user grants.
  - `greeting` — string — Message spoken when the call starts.
  - `backgroundSound` — VoiceBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT like `interruptions` and `endCall`, rather than a loose name on the channel: it is one switchable call behaviour, it reads the same way as its siblings, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
    - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
    - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
  - `speech` — VoiceSpeechSettings — Speech configuration for the voice channel. When present it WINS over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the single exception, because it is the channel's own input signal and the feature has no starting point without it.
    - `languages` — array **(required)** — Configured languages. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once: automatic detection here is opt-in (`transcription.autoDetect`), and once a caller turns it on, the service does not clamp the resulting candidate list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five) — a caller who both opts in and configures more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. With detection off, only the single resolved language is ever sent, so the ceiling never becomes a candidate-list problem at all. _(minItems=1; maxItems=10)_
      - _array of_ `VoiceLanguage`
        - _(nesting depth limit — see `VoiceLanguage` in the Schemas appendix)_
    - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in the voice, provider account and pronunciation rules of its own language, instead of only the language the call resolved to. Languages whose first message is empty, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
    - `transcription` — VoiceTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
      - `engine` — string — Recogniser to transcribe the caller with. Absent resolves to the platform default ('aws://transcribe' today), resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
      - `autoDetect` — boolean — Identify the caller's language per utterance and switch voice and reply language mid-call. HERE RATHER THAN ON `VoiceSpeechSettings`, because identifying a language is something the RECOGNISER does: it becomes identify-multiple-languages plus language-options on the recognition stream, and nothing about synthesis reads it. Requires at least two configured languages and a recogniser that can identify them; the server clamps it to false otherwise, because forwarding true with a single candidate makes Amazon reject the stream outright.
  - `interruptions` — VoiceInterruptionSettings
    - `enabled` — boolean **(required)** — Whether the caller can interrupt the agent while it is speaking.
    - `minWords` — number — Minimum number of caller words that count as an interruption. _(min=1; max=10)_
  - `silenceTimeout` — VoiceSilenceTimeoutSettings
    - `seconds` — number **(required)** — Seconds of caller silence before the action is taken. _(min=1; max=600)_
    - `action` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`hangup`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`transfer`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `maxDuration` — VoiceMaxDurationSettings
    - `seconds` — number **(required)** — Maximum call duration in seconds before the action is taken. _(min=10; max=14400)_
    - `action` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`hangup`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`transfer`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `endCall` — VoiceEndCallSettings
    - `enabled` — boolean **(required)**
    - `phrases` — string — Comma-separated phrases that end the call, e.g. 'goodbye,bye'.
  - `callerMetadata` — VoiceCallerMetadataSettings — Caller context injected into the model prompt.
    - `callerName` — boolean — Include the caller name. Defaults to true.
    - `callerNumber` — boolean — Include the caller phone number. Defaults to true.
    - `callerEmail` — boolean — Include the caller email when known. Defaults to false.
    - `callerCompany` — boolean — Include the caller company when known. Defaults to false.
    - `time` — boolean — Include the current time, rendered in the agent's `engine.ai.timeZone`. Defaults to false.
- `chat` — ChatChannelSettings
  - `discoverable` — boolean — Whether users can find and add this agent to conversations.
  - `sessionTimeoutMinutes` — number — Minutes a conversation can stay idle before the next message starts a new session. Omit to start a new session at the end of the agent's local day (`engine.ai.timeZone`). Allowed values: 15, 30, 60, 120. _(min=15; max=120)_
  - `verbosity` — string — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
- `assistant` — AssistantChannelSettings — Assistant channel settings. Presence enables the in-app assistant surface; audio remains unavailable unless its separate settings are present and enabled.
  - `default` — boolean — Offer this agent as the default assistant for users covered by the agent access settings.
  - `ui` — AssistantUiSettings — How the agent presents itself in the assistant UI: what the user reads before typing anything, and what they can start from without typing at all. Everything here is presentation — it never changes what the agent can do.
    - `welcome` — AssistantWelcomeSettings — Greeting shown on an empty thread, above the quick commands.
      - `title` — string — Heading, e.g. 'How can I help?'. Rendered on one line. _(minLen=1; maxLen=80)_
      - `subtitle` — string — Line under the heading, saying what this agent is for, e.g. 'Ask about your conversations, accounts and calls.'. _(minLen=1; maxLen=200)_
    - `commands` — array — Cards offered under the welcome message on an empty thread, in the order given. Empty or omitted shows no cards. _(maxItems=8)_
      - _array of_ `AssistantQuickCommand`
        - _(nesting depth limit — see `AssistantQuickCommand` in the Schemas appendix)_
    - `placeholder` — string — Placeholder text in the composer, e.g. 'Ask about an account…'. Defaults to the client's own placeholder when omitted. _(minLen=1; maxLen=100)_
  - `audio` — AssistantAudioSettings — Switchable audio for the assistant channel. The settings object keeps enablement beside its speech policy, matching the voice channel's switchable blocks so a disabled configuration can be retained without serving audio.
    - `enabled` — boolean **(required)** — Whether the assistant accepts audio calls. Required so the presence of saved speech configuration is never mistaken for enablement.
    - `speech` — AssistantSpeechSettings — Recognition and synthesis policy for assistant audio. This is assistant-owned rather than a VoiceSpeechSettings reuse so telephony and assistant audio can evolve independently. It has no language greeting and no greet-every-language switch because an assistant conversation is already open when its audio call starts, leaving nothing for the channel to greet.
      - `languages` — array **(required)** — Languages the assistant audio channel can recognise and speak. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once — unlike the voice channel, where a caller opts into identification with `autoDetect`, THIS channel derives identification from `languages` and turns it on whenever the recogniser can identify among more than one, so every one of the up to ten rows here can become a live candidate list. The service does not clamp that list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five); a caller configuring more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. _(minItems=1; maxItems=10)_
        - _(nesting depth limit — see `AssistantLanguage` in the Schemas appendix)_
      - `transcription` — AssistantTranscriptionSettings — Speech-to-text configuration owned by the assistant channel, so changes to assistant recognition policy cannot alter telephony calls. NO `autoDetect` HERE, unlike the voice channel: on this channel configuring a second language IS the request to recognise which one is being spoken — nobody lists two and then asks to be heard in only one — so the server derives identification from the language list and clamps it to false when the recogniser cannot identify among them, or there are too few to identify. The voice channel keeps the switch because a dialplan can hand a call its language, which is a choice an assistant conversation never has to make.
        - _(nesting depth limit — see `AssistantTranscriptionSettings` in the Schemas appendix)_

**`AgentConnectorCapability`**

_A configured connector (wilma-tools) exposed to the model as a single meta-tool named after the connector. The model calls the reserved `help` action to learn the callable actions, then dispatches an action through the same tool. Progressive disclosure runs through the connector tool itself, not the skills catalogue._

- `id` — string **(required)** — Configured connector instance in wilma-tools. Its pinned definition, permission `grant` and authorization govern what the model can discover via `help` and call. There is no version pin here, unlike `AgentTool.toolVersion`: the action catalogue and its schemas are already frozen by the connector's pinned definition, while `grant` and authorization are read live so permission changes apply at once. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
- `startMessage` — string — Message spoken when a connector action call starts. Honoured on the voice channel. Mirrors `AgentTool.startMessage`. Not applied to the read-only `help` action. Not consulted once `startMessages` carries any entry.
- `startMessages` — array — Forward-compatible per-language connector start messages, mirroring `AgentTool.startMessages`. Accepted and stored so clients can configure connector and tool phrases consistently, but currently ignored at execution time because the voice runtime does not read connector start messages yet. Runtime enablement is tracked in wilma-services docs/todo.md item 8.
  - _array of_ `AgentSpokenPhrase`
    - `language` — string **(required)** — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - `text` — string **(required)**
- `pipeline` — AgentToolPipeline
  - `type` — string — How the model waits for a tool and whether it synthesizes a reply from the result. _(enum: `blocking_request`, `blocking_request_guided`, `async_request`, `async_request_guided`)_
  - `instructions` — string — Reply instructions for the *_GUIDED pipeline types. Use {{response}} to reference the tool result.
- `approval` — AgentToolApproval — Human-in-the-loop confirmation for a tool. Presence requires approval: the agent pauses before running the tool and the session user (whoever controls the session) approves or denies inline.
  - `prompt` — string — Optional message shown in the confirmation prompt. Supports handlebars against agent variables and the pending tool arguments. When omitted, a default prompt is shown.
- `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
  - _array of_ `ChannelType`
- `annotations` — array
  - _array of_ `AgentToolAnnotation`
    - _oneOf_ — exactly one of:
      - **`tag`**
        - `tag` — AgentToolTagAnnotation **(required)** — Tag annotation emitted after a tool completes.
          - _(nesting depth limit — see `AgentToolTagAnnotation` in the Schemas appendix)_
      - **`comment`**
        - `comment` — AgentToolCommentAnnotation **(required)** — Comment annotation emitted after a tool completes.
          - _(nesting depth limit — see `AgentToolCommentAnnotation` in the Schemas appendix)_
      - **`variables`**
        - `variables` — AgentToolVariablesAnnotation **(required)** — Variables annotation emitted after a tool completes.
      - **`result`**
        - `result` — AgentToolResultAnnotation **(required)** — Result annotation emitted after a tool completes.

**`AgentDefinitionSnapshot`**

_The complete, versionable configuration of an agent. This is what gets snapshotted when a version is published._

- `name` — string **(required)** _(minLen=3; maxLen=255)_
- `description` — string _(minLen=1; maxLen=1000)_
- `category` — string — Category of the agent, e.g.: 'Support'. _(minLen=1; maxLen=128)_
- `picture` — string — Avatar URL.
- `channels` — AgentChannels **(required)** — The channels an agent serves and their channel-specific settings. Presence of a member enables that channel. Empty means the agent serves no channel: it is not reachable on its own and runs only as an automation's task or when another agent calls it. Enabled channels are mirrored as ChannelType values on AgentInfo.
  - `voice` — VoiceChannelSettings — Voice channel settings. Note: a voice agent's AgentAccess.grants are ignored — inbound calls are routed by the PBX dialplan and data ACL is the agent-level `settings.pbxGroupId`, not per-user grants.
    - `greeting` — string — Message spoken when the call starts.
    - `backgroundSound` — VoiceBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT like `interruptions` and `endCall`, rather than a loose name on the channel: it is one switchable call behaviour, it reads the same way as its siblings, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
      - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
      - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
    - `speech` — VoiceSpeechSettings — Speech configuration for the voice channel. When present it WINS over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the single exception, because it is the channel's own input signal and the feature has no starting point without it.
      - `languages` — array **(required)** — Configured languages. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once: automatic detection here is opt-in (`transcription.autoDetect`), and once a caller turns it on, the service does not clamp the resulting candidate list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five) — a caller who both opts in and configures more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. With detection off, only the single resolved language is ever sent, so the ceiling never becomes a candidate-list problem at all. _(minItems=1; maxItems=10)_
        - _(nesting depth limit — see `VoiceLanguage` in the Schemas appendix)_
      - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in the voice, provider account and pronunciation rules of its own language, instead of only the language the call resolved to. Languages whose first message is empty, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
      - `transcription` — VoiceTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
        - _(nesting depth limit — see `VoiceTranscriptionSettings` in the Schemas appendix)_
    - `interruptions` — VoiceInterruptionSettings
      - `enabled` — boolean **(required)** — Whether the caller can interrupt the agent while it is speaking.
      - `minWords` — number — Minimum number of caller words that count as an interruption. _(min=1; max=10)_
    - `silenceTimeout` — VoiceSilenceTimeoutSettings
      - `seconds` — number **(required)** — Seconds of caller silence before the action is taken. _(min=1; max=600)_
      - `action` — union **(required)**
        - _(nesting depth limit — see `VoiceTerminateAction` in the Schemas appendix)_
    - `maxDuration` — VoiceMaxDurationSettings
      - `seconds` — number **(required)** — Maximum call duration in seconds before the action is taken. _(min=10; max=14400)_
      - `action` — union **(required)**
        - _(nesting depth limit — see `VoiceTerminateAction` in the Schemas appendix)_
    - `endCall` — VoiceEndCallSettings
      - `enabled` — boolean **(required)**
      - `phrases` — string — Comma-separated phrases that end the call, e.g. 'goodbye,bye'.
    - `callerMetadata` — VoiceCallerMetadataSettings — Caller context injected into the model prompt.
      - `callerName` — boolean — Include the caller name. Defaults to true.
      - `callerNumber` — boolean — Include the caller phone number. Defaults to true.
      - `callerEmail` — boolean — Include the caller email when known. Defaults to false.
      - `callerCompany` — boolean — Include the caller company when known. Defaults to false.
      - `time` — boolean — Include the current time, rendered in the agent's `engine.ai.timeZone`. Defaults to false.
  - `chat` — ChatChannelSettings
    - `discoverable` — boolean — Whether users can find and add this agent to conversations.
    - `sessionTimeoutMinutes` — number — Minutes a conversation can stay idle before the next message starts a new session. Omit to start a new session at the end of the agent's local day (`engine.ai.timeZone`). Allowed values: 15, 30, 60, 120. _(min=15; max=120)_
    - `verbosity` — string — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
  - `assistant` — AssistantChannelSettings — Assistant channel settings. Presence enables the in-app assistant surface; audio remains unavailable unless its separate settings are present and enabled.
    - `default` — boolean — Offer this agent as the default assistant for users covered by the agent access settings.
    - `ui` — AssistantUiSettings — How the agent presents itself in the assistant UI: what the user reads before typing anything, and what they can start from without typing at all. Everything here is presentation — it never changes what the agent can do.
      - `welcome` — AssistantWelcomeSettings — Greeting shown on an empty thread, above the quick commands.
        - _(nesting depth limit — see `AssistantWelcomeSettings` in the Schemas appendix)_
      - `commands` — array — Cards offered under the welcome message on an empty thread, in the order given. Empty or omitted shows no cards. _(maxItems=8)_
        - _(nesting depth limit — see `AssistantQuickCommand` in the Schemas appendix)_
      - `placeholder` — string — Placeholder text in the composer, e.g. 'Ask about an account…'. Defaults to the client's own placeholder when omitted. _(minLen=1; maxLen=100)_
    - `audio` — AssistantAudioSettings — Switchable audio for the assistant channel. The settings object keeps enablement beside its speech policy, matching the voice channel's switchable blocks so a disabled configuration can be retained without serving audio.
      - `enabled` — boolean **(required)** — Whether the assistant accepts audio calls. Required so the presence of saved speech configuration is never mistaken for enablement.
      - `speech` — AssistantSpeechSettings — Recognition and synthesis policy for assistant audio. This is assistant-owned rather than a VoiceSpeechSettings reuse so telephony and assistant audio can evolve independently. It has no language greeting and no greet-every-language switch because an assistant conversation is already open when its audio call starts, leaving nothing for the channel to greet.
        - _(nesting depth limit — see `AssistantSpeechSettings` in the Schemas appendix)_
- `engine` — union **(required)** — How the agent produces replies. `ai` is the managed engine; `webhook` and `sqs` delegate to an external backend.
  - _oneOf_ — exactly one of:
    - **`ai`**
      - `ai` — AgentAiEngine **(required)** — Managed AI engine: the platform runs the model, tools and knowledge lookups.
        - `instructions` — string **(required)** _(minLen=1; maxLen=60000)_
        - `workflow` — AgentWorkflow — The agent's conversation as a graph: which step runs first, what each step does, and on what condition control moves on. Optional on AgentAiEngine — without one the agent is prompt-driven, steered by `instructions` and free to use its capabilities in any order. Versioned with the rest of the agent definition: publishing a version snapshots the graph, and a draft edit reaches no session until it is published and routed.
          - _(nesting depth limit — see `AgentWorkflow` in the Schemas appendix)_
        - `guardrails` — AgentGuardrails — Turn screening, by side. Only `input` exists: it guards what reaches the model, and output screening is a separate policy with different actions, added here when it is built.
          - _(nesting depth limit — see `AgentGuardrails` in the Schemas appendix)_
        - `model` — string — Defaults to the platform default model when omitted. _(pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
        - `timeZone` — string — IANA timezone the agent reasons about time in: it anchors the current date and time given to the model and how times are read from and written to tool arguments and replies. Shared by every channel the agent serves. Defaults to 'UTC'. _(minLen=1; maxLen=64)_
        - `artifacts` — boolean — Whether the agent can produce artifacts (wilma-artifacts): files it writes in its sandbox and shares back during a session — a document, a PDF, a spreadsheet, a chart, a multi-page web site, a folder of files. Needs the sandbox capability. An artifact starts private to the user the session runs for, who can share it company-wide from the viewer; on the chat channel the runtime shares each one company-wide as it is created, so the link posted into the conversation opens for every signed-in colleague. Artifacts are company-internal: recipients on external transports (sms / whatsapp) or outside the company cannot open the links, so keep this disabled for customer-facing agents. Defaults to false.
        - `skills` — array — Skills attached to this agent (progressive disclosure). A skill may carry its own tools, which join this agent's toolset while that skill is active.
          - _(nesting depth limit — see `AgentSkillReference` in the Schemas appendix)_
        - `capabilities` — array — Everything the agent can do. When a `workflow` is set these are the capabilities in scope at every step, and a step may add to them or narrow them with its own list of the same shape.
          - _(nesting depth limit — see `AgentCapability` in the Schemas appendix)_
        - `variables` — array
          - _(nesting depth limit — see `AgentVariable` in the Schemas appendix)_
    - **`webhook`**
      - `webhook` — AgentWebhookEngine **(required)** — Bring-your-own backend over HTTPS. The platform POSTs call events to the URL; the backend answers out of band through the channel's command API. The response body is not read.
        - `url` — string **(required)**
        - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
          - _(nesting depth limit — see `SecretRef` in the Schemas appendix)_
        - `timeout` — number — Timeout of one delivery, in milliseconds. _(default=10000; min=5000; max=120000)_
    - **`sqs`**
      - `sqs` — AgentSqsEngine **(required)** — Bring-your-own backend over SQS. The platform sends call events to the queue; the backend answers out of band through the channel's command API.
        - `url` — string **(required)**
        - `key` — string **(required)**
        - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
          - _(nesting depth limit — see `SecretRef` in the Schemas appendix)_
- `settings` — AgentSettings — Agent-level settings shared across all channels.
  - `pbxGroupId` — string — PBX group used for data ACL (e.g. Sales Intelligence lookups).
- `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
  - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
  - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
    - _array of_ `AgentGrantPrincipal`
      - _oneOf_ — exactly one of:
        - **`userId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`groupId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`department`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_

**`AgentDelegationCapability`**

_Delegate the conversation to another agent (max 3 transitions per turn). One capability entry per delegate target._

- `name` — string — Tool name exposed to the model. Auto-generated when omitted.
- `description` — string — Description for the model to decide when to delegate.
- `id` — string **(required)** — Agent to delegate to. _(minLen=12; maxLen=12)_
- `agentVersion` — number — Pin a specific published version of the delegate agent. When absent, the delegate's deployment configuration selects the version at delegation time. _(min=1)_
- `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
  - _array of_ `ChannelType`
- `annotations` — array
  - _array of_ `AgentToolAnnotation`
    - _oneOf_ — exactly one of:
      - **`tag`**
        - `tag` — AgentToolTagAnnotation **(required)** — Tag annotation emitted after a tool completes.
          - _(nesting depth limit — see `AgentToolTagAnnotation` in the Schemas appendix)_
      - **`comment`**
        - `comment` — AgentToolCommentAnnotation **(required)** — Comment annotation emitted after a tool completes.
          - _(nesting depth limit — see `AgentToolCommentAnnotation` in the Schemas appendix)_
      - **`variables`**
        - `variables` — AgentToolVariablesAnnotation **(required)** — Variables annotation emitted after a tool completes.
      - **`result`**
        - `result` — AgentToolResultAnnotation **(required)** — Result annotation emitted after a tool completes.

**`AgentDeploymentRoute`**

- `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
- `percentage` — number **(required)** — Percentage of new sessions routed to this version. Percentages must sum to 100. _(min=1; max=100)_

**`AgentEngine`**

_How the agent produces replies. `ai` is the managed engine; `webhook` and `sqs` delegate to an external backend._

- _oneOf_ — exactly one of:
  - **`ai`**
    - `ai` — AgentAiEngine **(required)** — Managed AI engine: the platform runs the model, tools and knowledge lookups.
      - `instructions` — string **(required)** _(minLen=1; maxLen=60000)_
      - `workflow` — AgentWorkflow — The agent's conversation as a graph: which step runs first, what each step does, and on what condition control moves on. Optional on AgentAiEngine — without one the agent is prompt-driven, steered by `instructions` and free to use its capabilities in any order. Versioned with the rest of the agent definition: publishing a version snapshots the graph, and a draft edit reaches no session until it is published and routed.
        - `entry` — string **(required)** — Step the graph starts at. Must be one of `steps`. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
        - `steps` — array **(required)** — Steps of one graph. Ids are unique within it. _(minItems=1; maxItems=200)_
          - _(nesting depth limit — see `AgentWorkflowStep` in the Schemas appendix)_
        - `nested` — array — Graphs the main workflow can run, referenced by `workflow` steps.
          - _(nesting depth limit — see `AgentWorkflowNested` in the Schemas appendix)_
        - `settings` — AgentWorkflowSettings
          - _(nesting depth limit — see `AgentWorkflowSettings` in the Schemas appendix)_
      - `guardrails` — AgentGuardrails — Turn screening, by side. Only `input` exists: it guards what reaches the model, and output screening is a separate policy with different actions, added here when it is built.
        - `input` — AgentGuardrailInput — Screening applied to what reaches the model. There is deliberately no bundle or preset-group member. A named group that expands to a set of checks reads like convenience and behaves like version skew: the same agent definition would mean different things before and after a platform release, invisibly to the tenant who published it. Listing the checks costs a few lines in a document the console writes anyway, and the published version then states exactly what it enforces. There is also no set-level default action. One field standing behind every check reads as a convenience and hides the thing a reader most needs to see: what a given check will actually do. A check's action is its own or its preset's, and both are visible on the check.
          - _(nesting depth limit — see `AgentGuardrailInput` in the Schemas appendix)_
      - `model` — string — Defaults to the platform default model when omitted. _(pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
      - `timeZone` — string — IANA timezone the agent reasons about time in: it anchors the current date and time given to the model and how times are read from and written to tool arguments and replies. Shared by every channel the agent serves. Defaults to 'UTC'. _(minLen=1; maxLen=64)_
      - `artifacts` — boolean — Whether the agent can produce artifacts (wilma-artifacts): files it writes in its sandbox and shares back during a session — a document, a PDF, a spreadsheet, a chart, a multi-page web site, a folder of files. Needs the sandbox capability. An artifact starts private to the user the session runs for, who can share it company-wide from the viewer; on the chat channel the runtime shares each one company-wide as it is created, so the link posted into the conversation opens for every signed-in colleague. Artifacts are company-internal: recipients on external transports (sms / whatsapp) or outside the company cannot open the links, so keep this disabled for customer-facing agents. Defaults to false.
      - `skills` — array — Skills attached to this agent (progressive disclosure). A skill may carry its own tools, which join this agent's toolset while that skill is active.
        - _array of_ `AgentSkillReference`
          - _(nesting depth limit — see `AgentSkillReference` in the Schemas appendix)_
      - `capabilities` — array — Everything the agent can do. When a `workflow` is set these are the capabilities in scope at every step, and a step may add to them or narrow them with its own list of the same shape.
        - _array of_ `AgentCapability`
          - _(nesting depth limit — see `AgentCapability` in the Schemas appendix)_
      - `variables` — array
        - _array of_ `AgentVariable`
          - _(nesting depth limit — see `AgentVariable` in the Schemas appendix)_
  - **`webhook`**
    - `webhook` — AgentWebhookEngine **(required)** — Bring-your-own backend over HTTPS. The platform POSTs call events to the URL; the backend answers out of band through the channel's command API. The response body is not read.
      - `url` — string **(required)**
      - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
        - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
      - `timeout` — number — Timeout of one delivery, in milliseconds. _(default=10000; min=5000; max=120000)_
  - **`sqs`**
    - `sqs` — AgentSqsEngine **(required)** — Bring-your-own backend over SQS. The platform sends call events to the queue; the backend answers out of band through the channel's command API.
      - `url` — string **(required)**
      - `key` — string **(required)**
      - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
        - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_

**`AgentEngineKind`**

_Which member of AgentEngine an agent carries, without the engine's configuration._

- string _(enum: `ai`, `webhook`, `sqs`)_

**`AgentGrantPrincipal`**

_A user, group or department that access is granted to._

- _oneOf_ — exactly one of:
  - **`userId`**
    - `userId` — string **(required)** _(minLen=12; maxLen=12)_
  - **`groupId`**
    - `groupId` — string **(required)**
  - **`department`**
    - `department` — string **(required)** — PBX department NAME, as carried on the colleague record (`PbxColleague.department`), not a department id. The x-bees directory knows a colleague's department only by name, so matching by name is what lets the check read a field the runtime already has instead of resolving the PBX department tree on every request. Two consequences: renaming a department in the PBX invalidates every grant naming it, and two departments with the same name in different branches of the tree are one value here.

**`AgentGuardrailAction`**

_What happens when a check trips. Exactly one member is set. Ordered by severity: observe < redact < block < end. When more than one check trips in the same call the most severe action wins and ties break on the order of `checks`, so a set can mix an observed check with an enforced one without the observation weakening the enforcement. There is no hand-over member yet. Handing a session to a human is a different mechanism on every channel — a voice transfer, a chat assignment, an assistant with no human behind it — and wiring a guardrail into all of them is out of proportion to the rest of this feature. Until AgentHandoverCapability has a runtime on more than one channel, the crisis path is a block whose message routes the caller._

- _oneOf_ — exactly one of:
  - **`observe`**
    - `observe` — AgentGuardrailObserveAction **(required)** — Record the verdict and let the turn through. The rollout mode: every guardrail should run here first, against real traffic, until its trips are read and its sensitivity is tuned. A tripped check still emits GuardrailTrippedEvent and still appears in the trace, which is what makes this a tuning tool rather than a switched-off check.
  - **`redact`**
    - `redact` — AgentGuardrailRedactAction **(required)** — Mask the matched spans and let the turn continue. The mask is chosen by the platform and is not configurable — a tenant-authored placeholder that collides with real text, or that the model reads as an instruction, is worse than having no choice. Only valid on checks that return spans (PII, SECRETS).
  - **`block`**
    - `block` — AgentGuardrailBlockAction **(required)** — Refuse the turn. The agent's model is never called, no tool runs, and the caller is answered with `message` instead. The session stays alive and the conversation continues, so on a check meant to redirect rather than stop — 'let me take a few details first' — the message is doing the work.
      - `message` — string — Said to the caller in place of the agent's reply. Falls back to a channel default when unset. _(minLen=1; maxLen=1000)_
  - **`end`**
    - `end` — AgentGuardrailEndAction **(required)** — End the session. It lands in SessionStatus TERMINATED — not STOPPED, which is what a user asking to stop means — so a refused session is never read back as a clean finish. On voice this hangs up the call; on the other channels the session simply accepts no further turns.
      - `message` — string — Said to the caller before the session ends. _(minLen=1; maxLen=1000)_

**`AgentGuardrailBlockAction`**

_Refuse the turn. The agent's model is never called, no tool runs, and the caller is answered with `message` instead. The session stays alive and the conversation continues, so on a check meant to redirect rather than stop — 'let me take a few details first' — the message is doing the work._

- `message` — string — Said to the caller in place of the agent's reply. Falls back to a channel default when unset. _(minLen=1; maxLen=1000)_

**`AgentGuardrailCheck`**

_One thing the checker is asked about a turn. There is deliberately no `enabled` flag: a check that should not run is removed, so a published version never carries a switched-off check that reads like policy._

- `name` — string **(required)** — Name of a check, unique within a guardrail set. Stable and machine-facing: session events and trace spans report a verdict by this name, so a reader needs no copy of the agent definition to tell which check fired. _(minLen=1; maxLen=64)_
- `description` — string
- `kind` — union **(required)** — What a check is: one of the platform's presets, or a prompt the tenant wrote. Exactly one member is set.
  - _oneOf_ — exactly one of:
    - **`preset`**
      - `preset` — AgentGuardrailPresetCheck **(required)** — A check backed by one of the platform's prebuilt prompts.
        - `preset` — string **(required)** — A prebuilt check. Each preset is a platform-maintained prompt shipped in code and versioned with the platform, not a tenant row — so a support question about what a preset caught has one answer. A preset check is otherwise an ordinary AgentGuardrailCheck: its sensitivity and action are the tenant's to set, and `notes` narrows its prompt without replacing it. _(enum: `jailbreak`, `offTopic`, `abuse`, `harmful`, `selfHarm`, `pii`, `secrets`, `regulatedAdvice`)_
        - `notes` — string — Appended to the preset's prompt. For narrowing, not redefining — 'ignore card numbers read back after our own IVR prompts for them' — so the preset keeps its maintenance while fitting a tenant whose product would otherwise fight it. _(minLen=1; maxLen=2000)_
    - **`custom`**
      - `custom` — AgentGuardrailCustomCheck **(required)** — A check written by the tenant. A name and a prompt is the whole surface: no category enum can express the rules customers actually buy, such as refusing to quote a price before qualifying.
        - `instructions` — string **(required)** — Natural-language description of what a custom check looks for. Describe the *content* to be caught, not an instruction to the checker: 'The caller is asking about cryptocurrency investments' works, 'Block all content about crypto' does not, and a negative definition ('anything except billing questions') reliably misfires. _(minLen=1; maxLen=10000)_
        - `examples` — array — Up to five turns that should trip this check. They steer the model's judgement and are NOT matched literally — a description plus examples catches the plural, the typo and the paraphrase that a term list misses. _(maxItems=5)_
          - _array of_ `string`
- `sensitivity` — string — How much confidence a verdict needs before it counts as tripped. The checker reports a confidence per check and this is the threshold against it, so raising sensitivity catches more and costs more false positives without changing the prompt or the model: `low` trips only on high confidence, `medium` on high and medium, `high` on anything but a clear pass. Defaults to MEDIUM. _(enum: `low`, `medium`, `high`)_
- `action` — union — What happens when a check trips. Exactly one member is set. Ordered by severity: observe < redact < block < end. When more than one check trips in the same call the most severe action wins and ties break on the order of `checks`, so a set can mix an observed check with an enforced one without the observation weakening the enforcement. There is no hand-over member yet. Handing a session to a human is a different mechanism on every channel — a voice transfer, a chat assignment, an assistant with no human behind it — and wiring a guardrail into all of them is out of proportion to the rest of this feature. Until AgentHandoverCapability has a runtime on more than one channel, the crisis path is a block whose message routes the caller.
  - _oneOf_ — exactly one of:
    - **`observe`**
      - `observe` — AgentGuardrailObserveAction **(required)** — Record the verdict and let the turn through. The rollout mode: every guardrail should run here first, against real traffic, until its trips are read and its sensitivity is tuned. A tripped check still emits GuardrailTrippedEvent and still appears in the trace, which is what makes this a tuning tool rather than a switched-off check.
    - **`redact`**
      - `redact` — AgentGuardrailRedactAction **(required)** — Mask the matched spans and let the turn continue. The mask is chosen by the platform and is not configurable — a tenant-authored placeholder that collides with real text, or that the model reads as an instruction, is worse than having no choice. Only valid on checks that return spans (PII, SECRETS).
    - **`block`**
      - `block` — AgentGuardrailBlockAction **(required)** — Refuse the turn. The agent's model is never called, no tool runs, and the caller is answered with `message` instead. The session stays alive and the conversation continues, so on a check meant to redirect rather than stop — 'let me take a few details first' — the message is doing the work.
        - `message` — string — Said to the caller in place of the agent's reply. Falls back to a channel default when unset. _(minLen=1; maxLen=1000)_
    - **`end`**
      - `end` — AgentGuardrailEndAction **(required)** — End the session. It lands in SessionStatus TERMINATED — not STOPPED, which is what a user asking to stop means — so a refused session is never read back as a clean finish. On voice this hangs up the call; on the other channels the session simply accepts no further turns.
        - `message` — string — Said to the caller before the session ends. _(minLen=1; maxLen=1000)_

**`AgentGuardrailCheckKind`**

_What a check is: one of the platform's presets, or a prompt the tenant wrote. Exactly one member is set._

- _oneOf_ — exactly one of:
  - **`preset`**
    - `preset` — AgentGuardrailPresetCheck **(required)** — A check backed by one of the platform's prebuilt prompts.
      - `preset` — string **(required)** — A prebuilt check. Each preset is a platform-maintained prompt shipped in code and versioned with the platform, not a tenant row — so a support question about what a preset caught has one answer. A preset check is otherwise an ordinary AgentGuardrailCheck: its sensitivity and action are the tenant's to set, and `notes` narrows its prompt without replacing it. _(enum: `jailbreak`, `offTopic`, `abuse`, `harmful`, `selfHarm`, `pii`, `secrets`, `regulatedAdvice`)_
      - `notes` — string — Appended to the preset's prompt. For narrowing, not redefining — 'ignore card numbers read back after our own IVR prompts for them' — so the preset keeps its maintenance while fitting a tenant whose product would otherwise fight it. _(minLen=1; maxLen=2000)_
  - **`custom`**
    - `custom` — AgentGuardrailCustomCheck **(required)** — A check written by the tenant. A name and a prompt is the whole surface: no category enum can express the rules customers actually buy, such as refusing to quote a price before qualifying.
      - `instructions` — string **(required)** — Natural-language description of what a custom check looks for. Describe the *content* to be caught, not an instruction to the checker: 'The caller is asking about cryptocurrency investments' works, 'Block all content about crypto' does not, and a negative definition ('anything except billing questions') reliably misfires. _(minLen=1; maxLen=10000)_
      - `examples` — array — Up to five turns that should trip this check. They steer the model's judgement and are NOT matched literally — a description plus examples catches the plural, the typo and the paraphrase that a term list misses. _(maxItems=5)_
        - _array of_ `string`

**`AgentGuardrailCustomCheck`**

_A check written by the tenant. A name and a prompt is the whole surface: no category enum can express the rules customers actually buy, such as refusing to quote a price before qualifying._

- `instructions` — string **(required)** — Natural-language description of what a custom check looks for. Describe the *content* to be caught, not an instruction to the checker: 'The caller is asking about cryptocurrency investments' works, 'Block all content about crypto' does not, and a negative definition ('anything except billing questions') reliably misfires. _(minLen=1; maxLen=10000)_
- `examples` — array — Up to five turns that should trip this check. They steer the model's judgement and are NOT matched literally — a description plus examples catches the plural, the typo and the paraphrase that a term list misses. _(maxItems=5)_
  - _array of_ `string`

**`AgentGuardrailEndAction`**

_End the session. It lands in SessionStatus TERMINATED — not STOPPED, which is what a user asking to stop means — so a refused session is never read back as a clean finish. On voice this hangs up the call; on the other channels the session simply accepts no further turns._

- `message` — string — Said to the caller before the session ends. _(minLen=1; maxLen=1000)_

**`AgentGuardrailErrorMode`**

_What happens when the checker itself errors or times out. OPEN lets the turn through unscreened and records GuardrailFailedEvent, so an unscreened turn is a fact in the log rather than an absence; CLOSED refuses it. Defaults to OPEN: an agent that stops answering because a small model had a bad minute is a worse and far likelier outage than the rare turn that goes unscreened. Background tasks, where nobody is waiting and a retry is free, are the case for CLOSED._

- string _(enum: `open`, `closed`)_

**`AgentGuardrailInput`**

_Screening applied to what reaches the model. There is deliberately no bundle or preset-group member. A named group that expands to a set of checks reads like convenience and behaves like version skew: the same agent definition would mean different things before and after a platform release, invisibly to the tenant who published it. Listing the checks costs a few lines in a document the console writes anyway, and the published version then states exactly what it enforces. There is also no set-level default action. One field standing behind every check reads as a convenience and hides the thing a reader most needs to see: what a given check will actually do. A check's action is its own or its preset's, and both are visible on the check._

- `checks` — array — The checks to run, evaluated together in one call. Absent or empty means no screening. _(maxItems=30)_
  - _array of_ `AgentGuardrailCheck`
    - `name` — string **(required)** — Name of a check, unique within a guardrail set. Stable and machine-facing: session events and trace spans report a verdict by this name, so a reader needs no copy of the agent definition to tell which check fired. _(minLen=1; maxLen=64)_
    - `description` — string
    - `kind` — union **(required)** — What a check is: one of the platform's presets, or a prompt the tenant wrote. Exactly one member is set.
      - _oneOf_ — exactly one of:
        - **`preset`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`custom`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `sensitivity` — string — How much confidence a verdict needs before it counts as tripped. The checker reports a confidence per check and this is the threshold against it, so raising sensitivity catches more and costs more false positives without changing the prompt or the model: `low` trips only on high confidence, `medium` on high and medium, `high` on anything but a clear pass. Defaults to MEDIUM. _(enum: `low`, `medium`, `high`)_
    - `action` — union — What happens when a check trips. Exactly one member is set. Ordered by severity: observe < redact < block < end. When more than one check trips in the same call the most severe action wins and ties break on the order of `checks`, so a set can mix an observed check with an enforced one without the observation weakening the enforcement. There is no hand-over member yet. Handing a session to a human is a different mechanism on every channel — a voice transfer, a chat assignment, an assistant with no human behind it — and wiring a guardrail into all of them is out of proportion to the rest of this feature. Until AgentHandoverCapability has a runtime on more than one channel, the crisis path is a block whose message routes the caller.
      - _oneOf_ — exactly one of:
        - **`observe`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`redact`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`block`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`end`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
- `model` — string — The model that runs the checks. Defaults to the platform's guardrail model — deliberately small and fast, and deliberately not the agent's own, whose cost and latency are what this exists to avoid spending on a bad turn. _(pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
- `action` — union — What happens when a check trips. Exactly one member is set. Ordered by severity: observe < redact < block < end. When more than one check trips in the same call the most severe action wins and ties break on the order of `checks`, so a set can mix an observed check with an enforced one without the observation weakening the enforcement. There is no hand-over member yet. Handing a session to a human is a different mechanism on every channel — a voice transfer, a chat assignment, an assistant with no human behind it — and wiring a guardrail into all of them is out of proportion to the rest of this feature. Until AgentHandoverCapability has a runtime on more than one channel, the crisis path is a block whose message routes the caller.
  - _oneOf_ — exactly one of:
    - **`observe`**
      - `observe` — AgentGuardrailObserveAction **(required)** — Record the verdict and let the turn through. The rollout mode: every guardrail should run here first, against real traffic, until its trips are read and its sensitivity is tuned. A tripped check still emits GuardrailTrippedEvent and still appears in the trace, which is what makes this a tuning tool rather than a switched-off check.
    - **`redact`**
      - `redact` — AgentGuardrailRedactAction **(required)** — Mask the matched spans and let the turn continue. The mask is chosen by the platform and is not configurable — a tenant-authored placeholder that collides with real text, or that the model reads as an instruction, is worse than having no choice. Only valid on checks that return spans (PII, SECRETS).
    - **`block`**
      - `block` — AgentGuardrailBlockAction **(required)** — Refuse the turn. The agent's model is never called, no tool runs, and the caller is answered with `message` instead. The session stays alive and the conversation continues, so on a check meant to redirect rather than stop — 'let me take a few details first' — the message is doing the work.
        - `message` — string — Said to the caller in place of the agent's reply. Falls back to a channel default when unset. _(minLen=1; maxLen=1000)_
    - **`end`**
      - `end` — AgentGuardrailEndAction **(required)** — End the session. It lands in SessionStatus TERMINATED — not STOPPED, which is what a user asking to stop means — so a refused session is never read back as a clean finish. On voice this hangs up the call; on the other channels the session simply accepts no further turns.
        - `message` — string — Said to the caller before the session ends. _(minLen=1; maxLen=1000)_
- `mode` — string — Runs the checker before the agent's model (BLOCKING) or alongside it (PARALLEL). Blocking costs the checker's latency on every turn but guarantees that a refused turn spent no tokens and fired no tool; parallel adds no latency and is the right trade on voice, where the delay is audible, at the risk that part of a reply reaches the caller and that a tool has already run before the cancellation lands. Defaults to BLOCKING. _(enum: `blocking`, `parallel`)_
- `errorMode` — string — What happens when the checker itself errors or times out. OPEN lets the turn through unscreened and records GuardrailFailedEvent, so an unscreened turn is a fact in the log rather than an absence; CLOSED refuses it. Defaults to OPEN: an agent that stops answering because a small model had a bad minute is a worse and far likelier outage than the rare turn that goes unscreened. Background tasks, where nobody is waiting and a retry is free, are the case for CLOSED. _(enum: `open`, `closed`)_
- `window` — string — How much of the conversation the checker sees. Defaults to LAST_WITH_PRIOR, because the jailbreaks worth catching are built across several turns — establish a fiction, then cash it in — and a checker shown only the last turn sees an innocuous sentence. There is no full-transcript option: screening a whole call on every turn would make the guardrail dearer than the agent. _(enum: `lastMessage`, `lastWithPrior`)_

**`AgentGuardrailMode`**

_Runs the checker before the agent's model (BLOCKING) or alongside it (PARALLEL). Blocking costs the checker's latency on every turn but guarantees that a refused turn spent no tokens and fired no tool; parallel adds no latency and is the right trade on voice, where the delay is audible, at the risk that part of a reply reaches the caller and that a tool has already run before the cancellation lands. Defaults to BLOCKING._

- string _(enum: `blocking`, `parallel`)_

**`AgentGuardrailObserveAction`**

_Record the verdict and let the turn through. The rollout mode: every guardrail should run here first, against real traffic, until its trips are read and its sensitivity is tuned. A tripped check still emits GuardrailTrippedEvent and still appears in the trace, which is what makes this a tuning tool rather than a switched-off check._

- AgentGuardrailObserveAction

**`AgentGuardrailPreset`**

_A prebuilt check. Each preset is a platform-maintained prompt shipped in code and versioned with the platform, not a tenant row — so a support question about what a preset caught has one answer. A preset check is otherwise an ordinary AgentGuardrailCheck: its sensitivity and action are the tenant's to set, and `notes` narrows its prompt without replacing it._

- string _(enum: `jailbreak`, `offTopic`, `abuse`, `harmful`, `selfHarm`, `pii`, `secrets`, `regulatedAdvice`)_

**`AgentGuardrailPresetCheck`**

_A check backed by one of the platform's prebuilt prompts._

- `preset` — string **(required)** — A prebuilt check. Each preset is a platform-maintained prompt shipped in code and versioned with the platform, not a tenant row — so a support question about what a preset caught has one answer. A preset check is otherwise an ordinary AgentGuardrailCheck: its sensitivity and action are the tenant's to set, and `notes` narrows its prompt without replacing it. _(enum: `jailbreak`, `offTopic`, `abuse`, `harmful`, `selfHarm`, `pii`, `secrets`, `regulatedAdvice`)_
- `notes` — string — Appended to the preset's prompt. For narrowing, not redefining — 'ignore card numbers read back after our own IVR prompts for them' — so the preset keeps its maintenance while fitting a tenant whose product would otherwise fight it. _(minLen=1; maxLen=2000)_

**`AgentGuardrailRedactAction`**

_Mask the matched spans and let the turn continue. The mask is chosen by the platform and is not configurable — a tenant-authored placeholder that collides with real text, or that the model reads as an instruction, is worse than having no choice. Only valid on checks that return spans (PII, SECRETS)._

- AgentGuardrailRedactAction

**`AgentGuardrailSensitivity`**

_How much confidence a verdict needs before it counts as tripped. The checker reports a confidence per check and this is the threshold against it, so raising sensitivity catches more and costs more false positives without changing the prompt or the model: `low` trips only on high confidence, `medium` on high and medium, `high` on anything but a clear pass. Defaults to MEDIUM._

- string _(enum: `low`, `medium`, `high`)_

**`AgentGuardrailWindow`**

_How much of the conversation the checker sees. Defaults to LAST_WITH_PRIOR, because the jailbreaks worth catching are built across several turns — establish a fiction, then cash it in — and a checker shown only the last turn sees an innocuous sentence. There is no full-transcript option: screening a whole call on every turn would make the guardrail dearer than the agent._

- string _(enum: `lastMessage`, `lastWithPrior`)_

**`AgentGuardrails`**

_Turn screening, by side. Only `input` exists: it guards what reaches the model, and output screening is a separate policy with different actions, added here when it is built._

- `input` — AgentGuardrailInput — Screening applied to what reaches the model. There is deliberately no bundle or preset-group member. A named group that expands to a set of checks reads like convenience and behaves like version skew: the same agent definition would mean different things before and after a platform release, invisibly to the tenant who published it. Listing the checks costs a few lines in a document the console writes anyway, and the published version then states exactly what it enforces. There is also no set-level default action. One field standing behind every check reads as a convenience and hides the thing a reader most needs to see: what a given check will actually do. A check's action is its own or its preset's, and both are visible on the check.
  - `checks` — array — The checks to run, evaluated together in one call. Absent or empty means no screening. _(maxItems=30)_
    - _array of_ `AgentGuardrailCheck`
      - `name` — string **(required)** — Name of a check, unique within a guardrail set. Stable and machine-facing: session events and trace spans report a verdict by this name, so a reader needs no copy of the agent definition to tell which check fired. _(minLen=1; maxLen=64)_
      - `description` — string
      - `kind` — union **(required)** — What a check is: one of the platform's presets, or a prompt the tenant wrote. Exactly one member is set.
        - _(nesting depth limit — see `AgentGuardrailCheckKind` in the Schemas appendix)_
      - `sensitivity` — string — How much confidence a verdict needs before it counts as tripped. The checker reports a confidence per check and this is the threshold against it, so raising sensitivity catches more and costs more false positives without changing the prompt or the model: `low` trips only on high confidence, `medium` on high and medium, `high` on anything but a clear pass. Defaults to MEDIUM. _(enum: `low`, `medium`, `high`)_
      - `action` — union — What happens when a check trips. Exactly one member is set. Ordered by severity: observe < redact < block < end. When more than one check trips in the same call the most severe action wins and ties break on the order of `checks`, so a set can mix an observed check with an enforced one without the observation weakening the enforcement. There is no hand-over member yet. Handing a session to a human is a different mechanism on every channel — a voice transfer, a chat assignment, an assistant with no human behind it — and wiring a guardrail into all of them is out of proportion to the rest of this feature. Until AgentHandoverCapability has a runtime on more than one channel, the crisis path is a block whose message routes the caller.
        - _(nesting depth limit — see `AgentGuardrailAction` in the Schemas appendix)_
  - `model` — string — The model that runs the checks. Defaults to the platform's guardrail model — deliberately small and fast, and deliberately not the agent's own, whose cost and latency are what this exists to avoid spending on a bad turn. _(pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
  - `action` — union — What happens when a check trips. Exactly one member is set. Ordered by severity: observe < redact < block < end. When more than one check trips in the same call the most severe action wins and ties break on the order of `checks`, so a set can mix an observed check with an enforced one without the observation weakening the enforcement. There is no hand-over member yet. Handing a session to a human is a different mechanism on every channel — a voice transfer, a chat assignment, an assistant with no human behind it — and wiring a guardrail into all of them is out of proportion to the rest of this feature. Until AgentHandoverCapability has a runtime on more than one channel, the crisis path is a block whose message routes the caller.
    - _oneOf_ — exactly one of:
      - **`observe`**
        - `observe` — AgentGuardrailObserveAction **(required)** — Record the verdict and let the turn through. The rollout mode: every guardrail should run here first, against real traffic, until its trips are read and its sensitivity is tuned. A tripped check still emits GuardrailTrippedEvent and still appears in the trace, which is what makes this a tuning tool rather than a switched-off check.
      - **`redact`**
        - `redact` — AgentGuardrailRedactAction **(required)** — Mask the matched spans and let the turn continue. The mask is chosen by the platform and is not configurable — a tenant-authored placeholder that collides with real text, or that the model reads as an instruction, is worse than having no choice. Only valid on checks that return spans (PII, SECRETS).
      - **`block`**
        - `block` — AgentGuardrailBlockAction **(required)** — Refuse the turn. The agent's model is never called, no tool runs, and the caller is answered with `message` instead. The session stays alive and the conversation continues, so on a check meant to redirect rather than stop — 'let me take a few details first' — the message is doing the work.
          - _(nesting depth limit — see `AgentGuardrailBlockAction` in the Schemas appendix)_
      - **`end`**
        - `end` — AgentGuardrailEndAction **(required)** — End the session. It lands in SessionStatus TERMINATED — not STOPPED, which is what a user asking to stop means — so a refused session is never read back as a clean finish. On voice this hangs up the call; on the other channels the session simply accepts no further turns.
          - _(nesting depth limit — see `AgentGuardrailEndAction` in the Schemas appendix)_
  - `mode` — string — Runs the checker before the agent's model (BLOCKING) or alongside it (PARALLEL). Blocking costs the checker's latency on every turn but guarantees that a refused turn spent no tokens and fired no tool; parallel adds no latency and is the right trade on voice, where the delay is audible, at the risk that part of a reply reaches the caller and that a tool has already run before the cancellation lands. Defaults to BLOCKING. _(enum: `blocking`, `parallel`)_
  - `errorMode` — string — What happens when the checker itself errors or times out. OPEN lets the turn through unscreened and records GuardrailFailedEvent, so an unscreened turn is a fact in the log rather than an absence; CLOSED refuses it. Defaults to OPEN: an agent that stops answering because a small model had a bad minute is a worse and far likelier outage than the rare turn that goes unscreened. Background tasks, where nobody is waiting and a retry is free, are the case for CLOSED. _(enum: `open`, `closed`)_
  - `window` — string — How much of the conversation the checker sees. Defaults to LAST_WITH_PRIOR, because the jailbreaks worth catching are built across several turns — establish a fiction, then cash it in — and a checker shown only the last turn sees an innocuous sentence. There is no full-transcript option: screening a whole call on every turn would make the guardrail dearer than the agent. _(enum: `lastMessage`, `lastWithPrior`)_

**`AgentHandoverCapability`**

_Hand the conversation over to a human and leave it. Honoured on conversation channels (chat, assistant)._

- `name` — string — Tool name exposed to the model. Auto-generated when omitted.
- `description` — string — Description for the model to decide when to hand over.
- `variant` — string _(enum: `agent`, `service`)_
- `agent` — string — Wilma agent to hand over to when variant = AGENT. _(minLen=12; maxLen=12)_
- `agentVersion` — number — Pin a specific published version of the target agent when variant = AGENT. When absent, the target's deployment configuration selects the version at handover time. _(min=1)_
- `service` — string — x-bees service id to hand over to when variant = SERVICE.
- `silent` — boolean — Hand over without posting a visible message to the user.
- `pipeline` — AgentHandoverPipeline
  - `type` — string _(enum: `handover`, `reply_and_handover`, `reply_instructed_and_handover`)_
  - `instructions` — string — Instructions for the model reply when type is REPLY_INSTRUCTED_AND_HANDOVER.
- `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
  - _array of_ `ChannelType`
- `annotations` — array
  - _array of_ `AgentToolAnnotation`
    - _oneOf_ — exactly one of:
      - **`tag`**
        - `tag` — AgentToolTagAnnotation **(required)** — Tag annotation emitted after a tool completes.
          - _(nesting depth limit — see `AgentToolTagAnnotation` in the Schemas appendix)_
      - **`comment`**
        - `comment` — AgentToolCommentAnnotation **(required)** — Comment annotation emitted after a tool completes.
          - _(nesting depth limit — see `AgentToolCommentAnnotation` in the Schemas appendix)_
      - **`variables`**
        - `variables` — AgentToolVariablesAnnotation **(required)** — Variables annotation emitted after a tool completes.
      - **`result`**
        - `result` — AgentToolResultAnnotation **(required)** — Result annotation emitted after a tool completes.

**`AgentHandoverPipeline`**

- `type` — string _(enum: `handover`, `reply_and_handover`, `reply_instructed_and_handover`)_
- `instructions` — string — Instructions for the model reply when type is REPLY_INSTRUCTED_AND_HANDOVER.

**`AgentHandoverPipelineType`**

- string _(enum: `handover`, `reply_and_handover`, `reply_instructed_and_handover`)_

**`AgentHandoverVariant`**

- string _(enum: `agent`, `service`)_

**`AgentHangupCapability`**

_Let the model end the call. Honoured on the voice channel._

- `name` — string — Tool name exposed to the model. Auto-generated when omitted.
- `description` — string — Description for the model to decide when to hang up.
- `pipeline` — AgentHangupPipeline
  - `type` — string _(enum: `hangup`, `reply_and_hangup`, `reply_instructed_and_hangup`)_
  - `instructions` — string — Instructions for the model reply when type is REPLY_INSTRUCTED_AND_HANGUP.
- `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
  - _array of_ `ChannelType`
- `annotations` — array
  - _array of_ `AgentToolAnnotation`
    - _oneOf_ — exactly one of:
      - **`tag`**
        - `tag` — AgentToolTagAnnotation **(required)** — Tag annotation emitted after a tool completes.
          - _(nesting depth limit — see `AgentToolTagAnnotation` in the Schemas appendix)_
      - **`comment`**
        - `comment` — AgentToolCommentAnnotation **(required)** — Comment annotation emitted after a tool completes.
          - _(nesting depth limit — see `AgentToolCommentAnnotation` in the Schemas appendix)_
      - **`variables`**
        - `variables` — AgentToolVariablesAnnotation **(required)** — Variables annotation emitted after a tool completes.
      - **`result`**
        - `result` — AgentToolResultAnnotation **(required)** — Result annotation emitted after a tool completes.

**`AgentHangupPipeline`**

- `type` — string _(enum: `hangup`, `reply_and_hangup`, `reply_instructed_and_hangup`)_
- `instructions` — string — Instructions for the model reply when type is REPLY_INSTRUCTED_AND_HANGUP.

**`AgentHangupPipelineType`**

- string _(enum: `hangup`, `reply_and_hangup`, `reply_instructed_and_hangup`)_

**`AgentInfo`**

_What a client needs to render an agent, and nothing more: AgentInfo is the end-user view of an agent, served by the channel runtimes (e.g. GetAgent / GetSettings on wilma-assistant) to callers who must not see instructions, capabilities or access rules. Everything here is safe to show to whoever can use the agent._

- `id` — string **(required)** _(minLen=12; maxLen=12)_
- `name` — string **(required)** _(minLen=3; maxLen=255)_
- `picture` — string — Avatar URL, from the agent definition.
- `category` — string _(minLen=1; maxLen=128)_
- `status` — string **(required)** _(enum: `draft`, `active`)_
- `channels` — array **(required)** — The channels this agent serves (voice / chat / assistant). Empty for an agent that serves none — one only an automation runs or another agent calls.
  - _array of_ `ChannelType`
- `speechConfigured` — boolean — Whether the voice channel has at least one configured speech language. A dialplan form partitions its application lists on this, so the answer has to travel with the list rather than cost one lookup per entry — it is the reason this member exists and the reason removing it broke that form. Absent is read as false.
- `engine` — string — Which member of AgentEngine an agent carries, without the engine's configuration. _(enum: `ai`, `webhook`, `sqs`)_
- `assistantVoice` — AssistantVoiceSettings — End-user view of an agent's assistant voice. New end-user voice parameters are added here rather than as AgentInfo members.
  - `enabled` — boolean **(required)** — Whether a client should offer a voice call. True only when the definition the agent currently runs has assistant audio enabled and configured (`channels.assistant.audio.enabled` with at least one speech language); audio that is not configured counts as disabled. For a deployment that splits traffic, every routed version must qualify, so the answer holds whichever version a call lands on.
- `skillIds` — array — Ids of the skills attached to this agent. Always active in this agent's sessions; user skill preferences cannot disable them.
  - _array of_ `string`
- `connectorIds` — array — Ids of the connector instances attached to this agent, in capability order — the order an administrator sees on the agent's capabilities page. This is how a client knows which of the connectors in the assistant's settings catalogue this agent can call: filter that catalogue by these ids.
  - _array of_ `string`
- `assistant` — AssistantUiSettings — How the agent presents itself in the assistant UI: what the user reads before typing anything, and what they can start from without typing at all. Everything here is presentation — it never changes what the agent can do.
  - `welcome` — AssistantWelcomeSettings — Greeting shown on an empty thread, above the quick commands.
    - `title` — string — Heading, e.g. 'How can I help?'. Rendered on one line. _(minLen=1; maxLen=80)_
    - `subtitle` — string — Line under the heading, saying what this agent is for, e.g. 'Ask about your conversations, accounts and calls.'. _(minLen=1; maxLen=200)_
  - `commands` — array — Cards offered under the welcome message on an empty thread, in the order given. Empty or omitted shows no cards. _(maxItems=8)_
    - _array of_ `AssistantQuickCommand`
      - `title` — string **(required)** — Card label, e.g. 'Summarize my day'. Rendered on one line and truncated when it does not fit. _(minLen=1; maxLen=60)_
      - `description` — string — Optional line under the label. Also one line, so keep it to a short clarification of what the command does. _(minLen=1; maxLen=120)_
      - `prompt` — string **(required)** — The message actually sent when the card is picked. Usually longer and more explicit than the label, since it is what the model reads. _(minLen=1; maxLen=2000)_
  - `placeholder` — string — Placeholder text in the composer, e.g. 'Ask about an account…'. Defaults to the client's own placeholder when omitted. _(minLen=1; maxLen=100)_
- `latestVersion` — number — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_

**`AgentInlineSandboxOptions`**

_Sandbox configured inline on the agent, without a pre-built snapshot._

- `size` — string — Compute size of each sandbox launched from the snapshot. Each level maps to a platform-defined vCPU/memory/disk allocation. _(enum: `min`, `small`, `large`, `max`)_
- `network` — string — Network access policy for the sandbox. _(enum: `allow-all`, `deny-all`, `allowlist`)_
- `allowedDomains` — array — Domains allowed when network = ALLOWLIST.
  - _array of_ `string`

**`AgentKnowledgeBase`**

- `knowledgeBaseId` — string
- `instructions` — string — Additional instructions for when the agent should use this knowledge base. _(minLen=1; maxLen=60000)_
- `searchStrategy` — string — Search algorithm used to retrieve passages. _(enum: `bm25`, `vector`, `hybrid`)_
- `searchThreshold` — string — Minimum similarity a passage needs to be returned. Raising it trades recall for precision. _(enum: `low`, `medium`, `high`)_
- `searchLimit` — number — Maximum number of passages this capability returns. Defaults to the knowledge base service's own default (10) when omitted. Keep it low on voice: every passage is prompt the model reads before it can speak. _(min=1; max=50)_
- `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
  - _array of_ `ChannelType`
- `annotations` — array
  - _array of_ `AgentToolAnnotation`
    - _oneOf_ — exactly one of:
      - **`tag`**
        - `tag` — AgentToolTagAnnotation **(required)** — Tag annotation emitted after a tool completes.
          - _(nesting depth limit — see `AgentToolTagAnnotation` in the Schemas appendix)_
      - **`comment`**
        - `comment` — AgentToolCommentAnnotation **(required)** — Comment annotation emitted after a tool completes.
          - _(nesting depth limit — see `AgentToolCommentAnnotation` in the Schemas appendix)_
      - **`variables`**
        - `variables` — AgentToolVariablesAnnotation **(required)** — Variables annotation emitted after a tool completes.
      - **`result`**
        - `result` — AgentToolResultAnnotation **(required)** — Result annotation emitted after a tool completes.

**`AgentSandboxCapability`**

_Embedded sandbox: shell + file tools backed by an execution environment. The only capability with no `channels` list — being a union it has nowhere to carry one — so it is offered on every channel the agent serves._

- _oneOf_ — exactly one of:
  - **`inline`**
    - `inline` — AgentInlineSandboxOptions **(required)** — Sandbox configured inline on the agent, without a pre-built snapshot.
      - `size` — string — Compute size of each sandbox launched from the snapshot. Each level maps to a platform-defined vCPU/memory/disk allocation. _(enum: `min`, `small`, `large`, `max`)_
      - `network` — string — Network access policy for the sandbox. _(enum: `allow-all`, `deny-all`, `allowlist`)_
      - `allowedDomains` — array — Domains allowed when network = ALLOWLIST.
        - _array of_ `string`
  - **`snapshot`**
    - `snapshot` — AgentSnapshotSandboxOptions **(required)** — Sandbox launched from a pre-built snapshot managed by the wilma-sandbox service.
      - `snapshotId` — string **(required)** — Snapshot to launch sandboxes from. Managed in the wilma-sandbox service; must be READY. _(minLen=12; maxLen=12)_
      - `network` — string — Network access policy for the sandbox. _(enum: `allow-all`, `deny-all`, `allowlist`)_
      - `allowedDomains` — array — Domains allowed when network = ALLOWLIST.
        - _array of_ `string`
      - `size` — string — Compute size of each sandbox launched from the snapshot. Each level maps to a platform-defined vCPU/memory/disk allocation. _(enum: `min`, `small`, `large`, `max`)_

**`AgentSettings`**

_Agent-level settings shared across all channels._

- `pbxGroupId` — string — PBX group used for data ACL (e.g. Sales Intelligence lookups).

**`AgentSkillReference`**

_Reference to a skill attached to an agent._

- `id` — string **(required)** _(minLen=12; maxLen=12)_
- `skillVersion` — number — Pin a specific published skill version. When omitted, latestVersion is resolved. _(min=1)_
- `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
  - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
  - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
    - _array of_ `AgentGrantPrincipal`
      - _oneOf_ — exactly one of:
        - **`userId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`groupId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`department`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_

**`AgentSnapshotSandboxOptions`**

_Sandbox launched from a pre-built snapshot managed by the wilma-sandbox service._

- `snapshotId` — string **(required)** — Snapshot to launch sandboxes from. Managed in the wilma-sandbox service; must be READY. _(minLen=12; maxLen=12)_
- `network` — string — Network access policy for the sandbox. _(enum: `allow-all`, `deny-all`, `allowlist`)_
- `allowedDomains` — array — Domains allowed when network = ALLOWLIST.
  - _array of_ `string`
- `size` — string — Compute size of each sandbox launched from the snapshot. Each level maps to a platform-defined vCPU/memory/disk allocation. _(enum: `min`, `small`, `large`, `max`)_

**`AgentSpokenPhrase`**

_One phrase in one language, for a capability that speaks a fixed line on the voice channel. Which entry is spoken is decided by the call's current language — the one the call resolved to at connect, or the one automatic detection switched to — matched on `language` CASE-INSENSITIVELY, the same rule `VoiceBotSpokenPhrase` states for the legacy stack, so a code written in either case reaches the same entry on either. Blank `text` means the agent says nothing in that language; it does NOT fall back to the language-agnostic member beside the list, which would speak one language's text in another language's voice._

- `language` — string **(required)** — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `text` — string **(required)**

**`AgentSqsEngine`**

_Bring-your-own backend over SQS. The platform sends call events to the queue; the backend answers out of band through the channel's command API._

- `url` — string **(required)**
- `key` — string **(required)**
- `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
  - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_

**`AgentStatus`**

- string _(enum: `draft`, `active`)_

**`AgentSuggestionsCapability`**

_Emit suggested replies for human operators. Honoured on the chat channel._

- `name` — string — Tool name. Auto-generated when omitted.
- `instructions` — string — Steers what the suggestions say. Appended to the platform's own generation prompt rather than replacing it, so the shape of a suggestion — short, tappable, a plausible next thing to send — stays the platform's to keep, and this narrows the subject: 'offer a callback and a link to the status page, never a discount'. NOT a tool description, unlike the `description` every other capability carries: suggestions are not a tool the model chooses to call. They are generated from a reply that has already been written, so there is no decision to describe — only the generation to steer. Absent means the platform's prompt alone. _(minLen=1; maxLen=2000)_
- `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
  - _array of_ `ChannelType`
- `annotations` — array
  - _array of_ `AgentToolAnnotation`
    - _oneOf_ — exactly one of:
      - **`tag`**
        - `tag` — AgentToolTagAnnotation **(required)** — Tag annotation emitted after a tool completes.
          - _(nesting depth limit — see `AgentToolTagAnnotation` in the Schemas appendix)_
      - **`comment`**
        - `comment` — AgentToolCommentAnnotation **(required)** — Comment annotation emitted after a tool completes.
          - _(nesting depth limit — see `AgentToolCommentAnnotation` in the Schemas appendix)_
      - **`variables`**
        - `variables` — AgentToolVariablesAnnotation **(required)** — Variables annotation emitted after a tool completes.
      - **`result`**
        - `result` — AgentToolResultAnnotation **(required)** — Result annotation emitted after a tool completes.

**`AgentTool`**

- `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
- `toolVersion` — number — Pin a specific published tool version. When omitted, the tool's latestVersion is resolved at load, so a republished tool reaches this agent without a new agent version. Pin it when `fields` must keep aiming at an exact input schema. _(min=1)_
- `description` — string — Override the tool's description for this agent. When omitted, the tool's own description is used. _(minLen=1; maxLen=4096)_
- `fields` — array — Per-field overrides on the tool input schema: pin fixed values (hidden from the model) or refine field descriptions. Fields not listed are filled by the model per the tool schema. Paths are resolved against the input schema of the tool version in effect — pin `toolVersion` when they must not move.
  - _array of_ `AgentToolField`
    - `path` — string **(required)** — JSON Pointer to the target property in the tool input schema. _(pattern=^/.*$; minLen=1; maxLen=512)_
    - `handler` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`guided`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`predefined`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
- `startMessage` — string — Message spoken when the tool call starts. Honoured on the voice channel. Spoken in every language of the call while `startMessages` is absent or empty; not consulted once `startMessages` carries any entry.
- `startMessages` — array — Per-language start messages. When present and non-empty, the entry for the call's current language is spoken and `startMessage` is not consulted; a language with no entry is silent. When absent or empty, `startMessage` is spoken as before. On a call with no effective speech configuration — no configured languages, or a PBX below protocol 2 — `startMessage` is spoken regardless, because there is no current language to choose by.
  - _array of_ `AgentSpokenPhrase`
    - `language` — string **(required)** — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - `text` — string **(required)**
- `pipeline` — AgentToolPipeline
  - `type` — string — How the model waits for a tool and whether it synthesizes a reply from the result. _(enum: `blocking_request`, `blocking_request_guided`, `async_request`, `async_request_guided`)_
  - `instructions` — string — Reply instructions for the *_GUIDED pipeline types. Use {{response}} to reference the tool result.
- `approval` — AgentToolApproval — Human-in-the-loop confirmation for a tool. Presence requires approval: the agent pauses before running the tool and the session user (whoever controls the session) approves or denies inline.
  - `prompt` — string — Optional message shown in the confirmation prompt. Supports handlebars against agent variables and the pending tool arguments. When omitted, a default prompt is shown.
- `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
  - _array of_ `ChannelType`
- `annotations` — array
  - _array of_ `AgentToolAnnotation`
    - _oneOf_ — exactly one of:
      - **`tag`**
        - `tag` — AgentToolTagAnnotation **(required)** — Tag annotation emitted after a tool completes.
          - _(nesting depth limit — see `AgentToolTagAnnotation` in the Schemas appendix)_
      - **`comment`**
        - `comment` — AgentToolCommentAnnotation **(required)** — Comment annotation emitted after a tool completes.
          - _(nesting depth limit — see `AgentToolCommentAnnotation` in the Schemas appendix)_
      - **`variables`**
        - `variables` — AgentToolVariablesAnnotation **(required)** — Variables annotation emitted after a tool completes.
      - **`result`**
        - `result` — AgentToolResultAnnotation **(required)** — Result annotation emitted after a tool completes.

**`AgentToolAnnotation`**

_Configuration for annotations emitted after a tool completes._

- _oneOf_ — exactly one of:
  - **`tag`**
    - `tag` — AgentToolTagAnnotation **(required)** — Tag annotation emitted after a tool completes.
      - `value` — string — Static handlebars expression resolved against agent variables and helpers.
      - `applyOnSuccess` — boolean — Apply when the tool succeeds.
      - `applyOnFailure` — boolean — Apply when the tool fails.
  - **`comment`**
    - `comment` — AgentToolCommentAnnotation **(required)** — Comment annotation emitted after a tool completes.
      - `value` — string — Static handlebars expression resolved against agent variables and helpers.
      - `applyOnSuccess` — boolean — Apply when the tool succeeds.
      - `applyOnFailure` — boolean — Apply when the tool fails.
  - **`variables`**
    - `variables` — AgentToolVariablesAnnotation **(required)** — Variables annotation emitted after a tool completes.
  - **`result`**
    - `result` — AgentToolResultAnnotation **(required)** — Result annotation emitted after a tool completes.

**`AgentToolApproval`**

_Human-in-the-loop confirmation for a tool. Presence requires approval: the agent pauses before running the tool and the session user (whoever controls the session) approves or denies inline._

- `prompt` — string — Optional message shown in the confirmation prompt. Supports handlebars against agent variables and the pending tool arguments. When omitted, a default prompt is shown.

**`AgentToolCommentAnnotation`**

_Comment annotation emitted after a tool completes._

- `value` — string — Static handlebars expression resolved against agent variables and helpers.
- `applyOnSuccess` — boolean — Apply when the tool succeeds.
- `applyOnFailure` — boolean — Apply when the tool fails.

**`AgentToolField`**

_Per-field override applied to a shared tool's input schema for this agent._

- `path` — string **(required)** — JSON Pointer to the target property in the tool input schema. _(pattern=^/.*$; minLen=1; maxLen=512)_
- `handler` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`guided`**
      - `guided` — AgentToolFieldGuidedHandler **(required)** — Keeps the field model-fillable but overrides its description in the schema shown to the model.
        - `description` — string **(required)** _(minLen=1; maxLen=1024)_
    - **`predefined`**
      - `predefined` — AgentToolFieldPredefinedHandler **(required)** — A fixed value injected at the field path and excluded from the schema shown to the model, so the model neither sees nor sets it. A JSON value, or a string with handlebars templates resolved against agent variables and session context (e.g. '{{callerName}}').
        - `value` — any **(required)**

**`AgentToolFieldGuidedHandler`**

_Keeps the field model-fillable but overrides its description in the schema shown to the model._

- `description` — string **(required)** _(minLen=1; maxLen=1024)_

**`AgentToolFieldHandler`**

- _oneOf_ — exactly one of:
  - **`guided`**
    - `guided` — AgentToolFieldGuidedHandler **(required)** — Keeps the field model-fillable but overrides its description in the schema shown to the model.
      - `description` — string **(required)** _(minLen=1; maxLen=1024)_
  - **`predefined`**
    - `predefined` — AgentToolFieldPredefinedHandler **(required)** — A fixed value injected at the field path and excluded from the schema shown to the model, so the model neither sees nor sets it. A JSON value, or a string with handlebars templates resolved against agent variables and session context (e.g. '{{callerName}}').
      - `value` — any **(required)**

**`AgentToolFieldPredefinedHandler`**

_A fixed value injected at the field path and excluded from the schema shown to the model, so the model neither sees nor sets it. A JSON value, or a string with handlebars templates resolved against agent variables and session context (e.g. '{{callerName}}')._

- `value` — any **(required)**

**`AgentToolPipeline`**

- `type` — string — How the model waits for a tool and whether it synthesizes a reply from the result. _(enum: `blocking_request`, `blocking_request_guided`, `async_request`, `async_request_guided`)_
- `instructions` — string — Reply instructions for the *_GUIDED pipeline types. Use {{response}} to reference the tool result.

**`AgentToolPipelineType`**

_How the model waits for a tool and whether it synthesizes a reply from the result._

- string _(enum: `blocking_request`, `blocking_request_guided`, `async_request`, `async_request_guided`)_

**`AgentToolResultAnnotation`**

_Result annotation emitted after a tool completes._

- AgentToolResultAnnotation

**`AgentToolTagAnnotation`**

_Tag annotation emitted after a tool completes._

- `value` — string — Static handlebars expression resolved against agent variables and helpers.
- `applyOnSuccess` — boolean — Apply when the tool succeeds.
- `applyOnFailure` — boolean — Apply when the tool fails.

**`AgentToolVariable`**

- `name` — string **(required)** — Name of the tool variable, e.g.: 'myvar' _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
- `handler` — union
  - _oneOf_ — exactly one of:
    - **`auto`**
      - `auto` — AgentToolVariableAutoHandler **(required)** — The model fills this variable itself, from conversation context. Included in the tool's input schema.
    - **`guided`**
      - `guided` — AgentToolVariableGuidedHandler **(required)** — The model fills this variable, guided by this description. Included in the tool's input schema with the description attached.
        - `description` — string **(required)** _(minLen=1; maxLen=1024)_
    - **`predefined`**
      - `predefined` — AgentToolVariablePredefinedHandler **(required)** — A fixed value bound to the variable and injected directly into the tool call. Not exposed to the model (excluded from the tool's input schema). Supports handlebars templates resolved against agent variables and session context (e.g. '{{callerName}}').
        - `value` — string **(required)**

**`AgentToolVariableAutoHandler`**

_The model fills this variable itself, from conversation context. Included in the tool's input schema._

- AgentToolVariableAutoHandler

**`AgentToolVariableGuidedHandler`**

_The model fills this variable, guided by this description. Included in the tool's input schema with the description attached._

- `description` — string **(required)** _(minLen=1; maxLen=1024)_

**`AgentToolVariableHandler`**

- _oneOf_ — exactly one of:
  - **`auto`**
    - `auto` — AgentToolVariableAutoHandler **(required)** — The model fills this variable itself, from conversation context. Included in the tool's input schema.
  - **`guided`**
    - `guided` — AgentToolVariableGuidedHandler **(required)** — The model fills this variable, guided by this description. Included in the tool's input schema with the description attached.
      - `description` — string **(required)** _(minLen=1; maxLen=1024)_
  - **`predefined`**
    - `predefined` — AgentToolVariablePredefinedHandler **(required)** — A fixed value bound to the variable and injected directly into the tool call. Not exposed to the model (excluded from the tool's input schema). Supports handlebars templates resolved against agent variables and session context (e.g. '{{callerName}}').
      - `value` — string **(required)**

**`AgentToolVariablePredefinedHandler`**

_A fixed value bound to the variable and injected directly into the tool call. Not exposed to the model (excluded from the tool's input schema). Supports handlebars templates resolved against agent variables and session context (e.g. '{{callerName}}')._

- `value` — string **(required)**

**`AgentToolVariablesAnnotation`**

_Variables annotation emitted after a tool completes._

- AgentToolVariablesAnnotation

**`AgentTransferCapability`**

_Transfer the call to a PBX destination. Honoured on the voice channel. One capability entry per transfer target._

- `name` — string — Tool name exposed to the model. Auto-generated when omitted.
- `description` — string — Description for the model to decide when to transfer.
- `variant` — string _(enum: `predefined`, `dynamic`, `directory`)_
- `context` — string — Routing context for PREDEFINED transfers.
- `extension` — string — Extension or phone number for PREDEFINED transfers.
- `pipeline` — AgentTransferPipeline
  - `type` — string _(enum: `transfer`, `reply_and_transfer`, `reply_instructed_and_transfer`)_
  - `instructions` — string — Instructions for the model reply when type is REPLY_INSTRUCTED_AND_TRANSFER.
- `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
  - _array of_ `ChannelType`
- `annotations` — array
  - _array of_ `AgentToolAnnotation`
    - _oneOf_ — exactly one of:
      - **`tag`**
        - `tag` — AgentToolTagAnnotation **(required)** — Tag annotation emitted after a tool completes.
          - _(nesting depth limit — see `AgentToolTagAnnotation` in the Schemas appendix)_
      - **`comment`**
        - `comment` — AgentToolCommentAnnotation **(required)** — Comment annotation emitted after a tool completes.
          - _(nesting depth limit — see `AgentToolCommentAnnotation` in the Schemas appendix)_
      - **`variables`**
        - `variables` — AgentToolVariablesAnnotation **(required)** — Variables annotation emitted after a tool completes.
      - **`result`**
        - `result` — AgentToolResultAnnotation **(required)** — Result annotation emitted after a tool completes.

**`AgentTransferPipeline`**

- `type` — string _(enum: `transfer`, `reply_and_transfer`, `reply_instructed_and_transfer`)_
- `instructions` — string — Instructions for the model reply when type is REPLY_INSTRUCTED_AND_TRANSFER.

**`AgentTransferPipelineType`**

- string _(enum: `transfer`, `reply_and_transfer`, `reply_instructed_and_transfer`)_

**`AgentTransferVariant`**

- string _(enum: `predefined`, `dynamic`, `directory`)_

**`AgentVariable`**

- `name` — string **(required)** _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
- `type` — string **(required)** _(enum: `string`, `number`, `boolean`, `string_array`, `number_array`)_
- `optional` — boolean **(required)**
- `description` — string — What the variable means and how it should be filled.

**`AgentVariableType`**

- string _(enum: `string`, `number`, `boolean`, `string_array`, `number_array`)_

**`AgentVersion`**

- `agentId` — string **(required)** _(minLen=12; maxLen=12)_
- `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
- `basedOnVersion` — number — Published version from which the draft originated. Absent for the first version of a new agent. _(min=1)_
- `name` — string — Optional human-readable name supplied at publish time. _(minLen=1; maxLen=255)_
- `changelog` — string — What changed in this version, provided at publish time. _(minLen=1; maxLen=500)_
- `definition` — AgentDefinitionSnapshot **(required)** — The complete, versionable configuration of an agent. This is what gets snapshotted when a version is published.
  - `name` — string **(required)** _(minLen=3; maxLen=255)_
  - `description` — string _(minLen=1; maxLen=1000)_
  - `category` — string — Category of the agent, e.g.: 'Support'. _(minLen=1; maxLen=128)_
  - `picture` — string — Avatar URL.
  - `channels` — AgentChannels **(required)** — The channels an agent serves and their channel-specific settings. Presence of a member enables that channel. Empty means the agent serves no channel: it is not reachable on its own and runs only as an automation's task or when another agent calls it. Enabled channels are mirrored as ChannelType values on AgentInfo.
    - `voice` — VoiceChannelSettings — Voice channel settings. Note: a voice agent's AgentAccess.grants are ignored — inbound calls are routed by the PBX dialplan and data ACL is the agent-level `settings.pbxGroupId`, not per-user grants.
      - `greeting` — string — Message spoken when the call starts.
      - `backgroundSound` — VoiceBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT like `interruptions` and `endCall`, rather than a loose name on the channel: it is one switchable call behaviour, it reads the same way as its siblings, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
        - _(nesting depth limit — see `VoiceBackgroundSoundSettings` in the Schemas appendix)_
      - `speech` — VoiceSpeechSettings — Speech configuration for the voice channel. When present it WINS over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the single exception, because it is the channel's own input signal and the feature has no starting point without it.
        - _(nesting depth limit — see `VoiceSpeechSettings` in the Schemas appendix)_
      - `interruptions` — VoiceInterruptionSettings
        - _(nesting depth limit — see `VoiceInterruptionSettings` in the Schemas appendix)_
      - `silenceTimeout` — VoiceSilenceTimeoutSettings
        - _(nesting depth limit — see `VoiceSilenceTimeoutSettings` in the Schemas appendix)_
      - `maxDuration` — VoiceMaxDurationSettings
        - _(nesting depth limit — see `VoiceMaxDurationSettings` in the Schemas appendix)_
      - `endCall` — VoiceEndCallSettings
        - _(nesting depth limit — see `VoiceEndCallSettings` in the Schemas appendix)_
      - `callerMetadata` — VoiceCallerMetadataSettings — Caller context injected into the model prompt.
        - _(nesting depth limit — see `VoiceCallerMetadataSettings` in the Schemas appendix)_
    - `chat` — ChatChannelSettings
      - `discoverable` — boolean — Whether users can find and add this agent to conversations.
      - `sessionTimeoutMinutes` — number — Minutes a conversation can stay idle before the next message starts a new session. Omit to start a new session at the end of the agent's local day (`engine.ai.timeZone`). Allowed values: 15, 30, 60, 120. _(min=15; max=120)_
      - `verbosity` — string — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
    - `assistant` — AssistantChannelSettings — Assistant channel settings. Presence enables the in-app assistant surface; audio remains unavailable unless its separate settings are present and enabled.
      - `default` — boolean — Offer this agent as the default assistant for users covered by the agent access settings.
      - `ui` — AssistantUiSettings — How the agent presents itself in the assistant UI: what the user reads before typing anything, and what they can start from without typing at all. Everything here is presentation — it never changes what the agent can do.
        - _(nesting depth limit — see `AssistantUiSettings` in the Schemas appendix)_
      - `audio` — AssistantAudioSettings — Switchable audio for the assistant channel. The settings object keeps enablement beside its speech policy, matching the voice channel's switchable blocks so a disabled configuration can be retained without serving audio.
        - _(nesting depth limit — see `AssistantAudioSettings` in the Schemas appendix)_
  - `engine` — union **(required)** — How the agent produces replies. `ai` is the managed engine; `webhook` and `sqs` delegate to an external backend.
    - _oneOf_ — exactly one of:
      - **`ai`**
        - `ai` — AgentAiEngine **(required)** — Managed AI engine: the platform runs the model, tools and knowledge lookups.
          - _(nesting depth limit — see `AgentAiEngine` in the Schemas appendix)_
      - **`webhook`**
        - `webhook` — AgentWebhookEngine **(required)** — Bring-your-own backend over HTTPS. The platform POSTs call events to the URL; the backend answers out of band through the channel's command API. The response body is not read.
          - _(nesting depth limit — see `AgentWebhookEngine` in the Schemas appendix)_
      - **`sqs`**
        - `sqs` — AgentSqsEngine **(required)** — Bring-your-own backend over SQS. The platform sends call events to the queue; the backend answers out of band through the channel's command API.
          - _(nesting depth limit — see `AgentSqsEngine` in the Schemas appendix)_
  - `settings` — AgentSettings — Agent-level settings shared across all channels.
    - `pbxGroupId` — string — PBX group used for data ACL (e.g. Sales Intelligence lookups).
  - `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
    - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
    - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
      - _array of_ `AgentGrantPrincipal`
        - _(nesting depth limit — see `AgentGrantPrincipal` in the Schemas appendix)_
- `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
  - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
  - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
  - `name` — string — Human readable name of the actor at the time of the action.

**`AgentVersionChange`**

- `path` — string **(required)** — JSON pointer of the changed field within the agent definition, e.g. '/engine/ai/instructions'.
- `before` — any — Value before the change (absent when the field was added).
- `after` — any — Value after the change (absent when the field was removed).

**`AgentVersionInfo`**

_Version list entry without the full definition snapshot._

- `agentId` — string **(required)** _(minLen=12; maxLen=12)_
- `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
- `basedOnVersion` — number — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
- `name` — string _(minLen=1; maxLen=255)_
- `changelog` — string — Human-readable description of what changed in a published version. _(minLen=1; maxLen=500)_
- `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
  - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
  - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
  - `name` — string — Human readable name of the actor at the time of the action.

**`AgentVisibility`**

- string _(enum: `explicit`, `organization`, `public`)_

**`AgentWaitCapability`**

_Let the model hold the call while it works (e.g. a lookup), keeping the caller on the line. Honoured on the voice channel._

- `name` — string — Tool name exposed to the model. Auto-generated when omitted.
- `description` — string — Description for the model to decide when to wait.
- `message` — string — Message spoken when entering the wait state. Spoken in every language of the call while `messages` is absent or empty; not consulted once `messages` carries any entry.
- `messages` — array — Per-language wait messages. Same rule as `AgentTool.startMessages`: the entry for the call's current language is spoken, a language with no entry is silent, and with no effective speech configuration `message` is spoken.
  - _array of_ `AgentSpokenPhrase`
    - `language` — string **(required)** — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - `text` — string **(required)**
- `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
  - _array of_ `ChannelType`
- `annotations` — array
  - _array of_ `AgentToolAnnotation`
    - _oneOf_ — exactly one of:
      - **`tag`**
        - `tag` — AgentToolTagAnnotation **(required)** — Tag annotation emitted after a tool completes.
          - _(nesting depth limit — see `AgentToolTagAnnotation` in the Schemas appendix)_
      - **`comment`**
        - `comment` — AgentToolCommentAnnotation **(required)** — Comment annotation emitted after a tool completes.
          - _(nesting depth limit — see `AgentToolCommentAnnotation` in the Schemas appendix)_
      - **`variables`**
        - `variables` — AgentToolVariablesAnnotation **(required)** — Variables annotation emitted after a tool completes.
      - **`result`**
        - `result` — AgentToolResultAnnotation **(required)** — Result annotation emitted after a tool completes.

**`AgentWebFetchCapability`**

_Server-side fetch of a URL, returning its readable text/markdown to the model._

- `allowedDomains` — array — Restrict fetches to these domains. Empty list means any domain is allowed.
  - _array of_ `string`
- `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
  - _array of_ `ChannelType`

**`AgentWebSearchCapability`**

_Model-native web search. The provider tool is selected from the agent model._

- `contextSize` — string — Search depth/context hint, mapped per provider. _(enum: `low`, `medium`, `high`)_
- `allowedDomains` — array — Restrict results to these domains where the provider supports it.
  - _array of_ `string`
- `userLocation` — WebSearchUserLocation
  - `country` — string — ISO 3166-1 alpha-2 country code, e.g. 'US'.
  - `region` — string
  - `city` — string
  - `timezone` — string — IANA timezone, e.g. 'Europe/Rome'.
- `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
  - _array of_ `ChannelType`

**`AgentWebhookEngine`**

_Bring-your-own backend over HTTPS. The platform POSTs call events to the URL; the backend answers out of band through the channel's command API. The response body is not read._

- `url` — string **(required)**
- `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
  - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
- `timeout` — number — Timeout of one delivery, in milliseconds. _(default=10000; min=5000; max=120000)_

**`AgentWorkflow`**

_The agent's conversation as a graph: which step runs first, what each step does, and on what condition control moves on. Optional on AgentAiEngine — without one the agent is prompt-driven, steered by `instructions` and free to use its capabilities in any order. Versioned with the rest of the agent definition: publishing a version snapshots the graph, and a draft edit reaches no session until it is published and routed._

- `entry` — string **(required)** — Step the graph starts at. Must be one of `steps`. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
- `steps` — array **(required)** — Steps of one graph. Ids are unique within it. _(minItems=1; maxItems=200)_
  - _array of_ `AgentWorkflowStep`
    - `id` — string **(required)** — Identifier of a step within its workflow, unique per workflow (the main graph and each nested workflow are separate scopes). Stable and machine-facing: transitions reference it, and a result step's id is the name a caller branches on, so renaming a step's `label` never unwires the graph. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
    - `label` — string **(required)** — Human readable name of a step, e.g. 'Transfer to the sales desk'. Shown in the builder and in traces, and read by the model too: when this step is an exit of the live step, the label is the preview offered alongside the exit's condition. Never a routing key — see AgentWorkflowStepId — so renaming one never unwires a graph. _(minLen=1; maxLen=128)_
    - `stage` — string — The phase this step belongs to. Inherited by steps downstream, so a handful of tags organise a long graph. _(minLen=1; maxLen=64)_
    - `handler` — union **(required)** — What a step does. Exactly one member is set. `action` carries a capability; the others are workflow-only handlers with no capability equivalent.
      - _oneOf_ — exactly one of:
        - **`conversation`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`message`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`action`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`variables`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`workflow`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`result`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`end`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `transitions` — array — The ways out of this step. Must be non-empty on every step that stays in the session, since a step the runtime cannot leave is a dead end. On `result` and `end` it must be empty. On the `action` members that leave the session (`handover`, `delegation`, `transfer`, `hangup`) it may carry `failure` transitions and nothing else: an action that was supposed to leave and failed — a busy extension, a service desk with nobody on it — has not left, and a graph with no answer for that drops the caller.
      - _array of_ `AgentWorkflowTransition`
        - _(nesting depth limit — see `AgentWorkflowTransition` in the Schemas appendix)_
    - `position` — AgentWorkflowStepPosition — Canvas coordinates of a step in the builder. Authoring metadata: the runtime ignores it, and a workflow that arrives without positions is laid out automatically.
      - `x` — number **(required)**
      - `y` — number **(required)**
- `nested` — array — Graphs the main workflow can run, referenced by `workflow` steps.
  - _array of_ `AgentWorkflowNested`
    - `entry` — string **(required)** — Step the graph starts at. Must be one of `steps`. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
    - `steps` — array **(required)** — Steps of one graph. Ids are unique within it. _(minItems=1; maxItems=200)_
      - _array of_ `AgentWorkflowStep`
        - _(nesting depth limit — see `AgentWorkflowStep` in the Schemas appendix)_
    - `id` — string **(required)** — Identifier of a nested workflow within the agent's workflow. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
    - `name` — string **(required)** _(minLen=1; maxLen=128)_
    - `description` — string — One line saying what the nested workflow is for, shown on the step that runs it. _(minLen=1; maxLen=1000)_
- `settings` — AgentWorkflowSettings
  - `maxTransitions` — number — Give up after this many step transitions, so a cycle whose conditions all keep matching cannot run forever. Absent means no limit, which is the default: a deliberate loop — 'keep asking until you have the postcode' — is a normal shape, and silently capping it would be worse than making the author say so. _(min=1; max=500)_
  - `variables` — array — Workflow variables seeded before the first step runs. Agent input variables (`engine.ai.variables`) are already in scope and need no entry here.
    - _array of_ `AgentWorkflowAssignment`
      - `name` — string **(required)** _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
      - `value` — string — Text written to the variable, with handlebars resolved against workflow variables, agent variables and session context (e.g. '{{lookup.status}}'). Empty clears the variable. _(maxLen=4000)_
      - `expression` — any — A JsonLogic expression computing the value instead of rendering it, which is what makes arithmetic possible: `{ "+": [{ "var": "attempts" }, 1] }` is the retry counter a bounded loop needs, written with no model in the loop.
  - `layout` — string — How the builder arranges the graph. Authoring metadata: the runtime ignores it. `stages` bands the graph by `stage`, which is what a forty-step workflow needs. _(enum: `flow`, `compact`, `stages`)_

**`AgentWorkflowAction`**

_The capability a step performs, run by the runtime rather than chosen by the model. A subset of AgentCapability, reusing its structures verbatim: these are the members that describe a single action with a beginning and an end. The rest of AgentCapability (`kb`, `webSearch`, `webFetch`, `sandbox`, `suggestions`) describes reach the model draws on while it talks, so it belongs on a conversation step's `capabilities` rather than on a step of its own. Configuration comes from the capability itself and nothing is added here: a tool step's fixed arguments are `AgentTool.fields` predefined handlers, its spoken lead-in is `AgentTool.startMessage`, a transfer's line before the hand-off is `AgentTransferPipeline.instructions`, an invoked agent's inputs are `AgentCallCapability.variables`. Anything left unpinned is filled by the model at the step, per the tool's input schema._

- _oneOf_ — exactly one of:
  - **`tool`**
    - `tool` — AgentTool **(required)**
      - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `toolVersion` — number — Pin a specific published tool version. When omitted, the tool's latestVersion is resolved at load, so a republished tool reaches this agent without a new agent version. Pin it when `fields` must keep aiming at an exact input schema. _(min=1)_
      - `description` — string — Override the tool's description for this agent. When omitted, the tool's own description is used. _(minLen=1; maxLen=4096)_
      - `fields` — array — Per-field overrides on the tool input schema: pin fixed values (hidden from the model) or refine field descriptions. Fields not listed are filled by the model per the tool schema. Paths are resolved against the input schema of the tool version in effect — pin `toolVersion` when they must not move.
        - _array of_ `AgentToolField`
          - _(nesting depth limit — see `AgentToolField` in the Schemas appendix)_
      - `startMessage` — string — Message spoken when the tool call starts. Honoured on the voice channel. Spoken in every language of the call while `startMessages` is absent or empty; not consulted once `startMessages` carries any entry.
      - `startMessages` — array — Per-language start messages. When present and non-empty, the entry for the call's current language is spoken and `startMessage` is not consulted; a language with no entry is silent. When absent or empty, `startMessage` is spoken as before. On a call with no effective speech configuration — no configured languages, or a PBX below protocol 2 — `startMessage` is spoken regardless, because there is no current language to choose by.
        - _array of_ `AgentSpokenPhrase`
          - _(nesting depth limit — see `AgentSpokenPhrase` in the Schemas appendix)_
      - `pipeline` — AgentToolPipeline
        - `type` — string — How the model waits for a tool and whether it synthesizes a reply from the result. _(enum: `blocking_request`, `blocking_request_guided`, `async_request`, `async_request_guided`)_
        - `instructions` — string — Reply instructions for the *_GUIDED pipeline types. Use {{response}} to reference the tool result.
      - `approval` — AgentToolApproval — Human-in-the-loop confirmation for a tool. Presence requires approval: the agent pauses before running the tool and the session user (whoever controls the session) approves or denies inline.
        - `prompt` — string — Optional message shown in the confirmation prompt. Supports handlebars against agent variables and the pending tool arguments. When omitted, a default prompt is shown.
      - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
        - _array of_ `ChannelType`
      - `annotations` — array
        - _array of_ `AgentToolAnnotation`
          - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
  - **`connector`**
    - `connector` — AgentConnectorCapability **(required)** — A configured connector (wilma-tools) exposed to the model as a single meta-tool named after the connector. The model calls the reserved `help` action to learn the callable actions, then dispatches an action through the same tool. Progressive disclosure runs through the connector tool itself, not the skills catalogue.
      - `id` — string **(required)** — Configured connector instance in wilma-tools. Its pinned definition, permission `grant` and authorization govern what the model can discover via `help` and call. There is no version pin here, unlike `AgentTool.toolVersion`: the action catalogue and its schemas are already frozen by the connector's pinned definition, while `grant` and authorization are read live so permission changes apply at once. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `startMessage` — string — Message spoken when a connector action call starts. Honoured on the voice channel. Mirrors `AgentTool.startMessage`. Not applied to the read-only `help` action. Not consulted once `startMessages` carries any entry.
      - `startMessages` — array — Forward-compatible per-language connector start messages, mirroring `AgentTool.startMessages`. Accepted and stored so clients can configure connector and tool phrases consistently, but currently ignored at execution time because the voice runtime does not read connector start messages yet. Runtime enablement is tracked in wilma-services docs/todo.md item 8.
        - _array of_ `AgentSpokenPhrase`
          - _(nesting depth limit — see `AgentSpokenPhrase` in the Schemas appendix)_
      - `pipeline` — AgentToolPipeline
        - `type` — string — How the model waits for a tool and whether it synthesizes a reply from the result. _(enum: `blocking_request`, `blocking_request_guided`, `async_request`, `async_request_guided`)_
        - `instructions` — string — Reply instructions for the *_GUIDED pipeline types. Use {{response}} to reference the tool result.
      - `approval` — AgentToolApproval — Human-in-the-loop confirmation for a tool. Presence requires approval: the agent pauses before running the tool and the session user (whoever controls the session) approves or denies inline.
        - `prompt` — string — Optional message shown in the confirmation prompt. Supports handlebars against agent variables and the pending tool arguments. When omitted, a default prompt is shown.
      - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
        - _array of_ `ChannelType`
      - `annotations` — array
        - _array of_ `AgentToolAnnotation`
          - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
  - **`agent`**
    - `agent` — AgentCallCapability **(required)** — Invoke another agent as a dedicated execution with its own state. The called agent runs independently and returns its result.
      - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
      - `agentVersion` — number — Pin a specific published version of the called agent. When absent, the called agent's deployment configuration selects the version at invocation time. _(min=1)_
      - `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
        - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
        - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
          - _(nesting depth limit — see `AgentGrantPrincipal` in the Schemas appendix)_
      - `variables` — array
        - _array of_ `AgentToolVariable`
          - _(nesting depth limit — see `AgentToolVariable` in the Schemas appendix)_
      - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
        - _array of_ `ChannelType`
  - **`handover`**
    - `handover` — AgentHandoverCapability **(required)** — Hand the conversation over to a human and leave it. Honoured on conversation channels (chat, assistant).
      - `name` — string — Tool name exposed to the model. Auto-generated when omitted.
      - `description` — string — Description for the model to decide when to hand over.
      - `variant` — string _(enum: `agent`, `service`)_
      - `agent` — string — Wilma agent to hand over to when variant = AGENT. _(minLen=12; maxLen=12)_
      - `agentVersion` — number — Pin a specific published version of the target agent when variant = AGENT. When absent, the target's deployment configuration selects the version at handover time. _(min=1)_
      - `service` — string — x-bees service id to hand over to when variant = SERVICE.
      - `silent` — boolean — Hand over without posting a visible message to the user.
      - `pipeline` — AgentHandoverPipeline
        - `type` — string _(enum: `handover`, `reply_and_handover`, `reply_instructed_and_handover`)_
        - `instructions` — string — Instructions for the model reply when type is REPLY_INSTRUCTED_AND_HANDOVER.
      - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
        - _array of_ `ChannelType`
      - `annotations` — array
        - _array of_ `AgentToolAnnotation`
          - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
  - **`delegation`**
    - `delegation` — AgentDelegationCapability **(required)** — Delegate the conversation to another agent (max 3 transitions per turn). One capability entry per delegate target.
      - `name` — string — Tool name exposed to the model. Auto-generated when omitted.
      - `description` — string — Description for the model to decide when to delegate.
      - `id` — string **(required)** — Agent to delegate to. _(minLen=12; maxLen=12)_
      - `agentVersion` — number — Pin a specific published version of the delegate agent. When absent, the delegate's deployment configuration selects the version at delegation time. _(min=1)_
      - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
        - _array of_ `ChannelType`
      - `annotations` — array
        - _array of_ `AgentToolAnnotation`
          - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
  - **`transfer`**
    - `transfer` — AgentTransferCapability **(required)** — Transfer the call to a PBX destination. Honoured on the voice channel. One capability entry per transfer target.
      - `name` — string — Tool name exposed to the model. Auto-generated when omitted.
      - `description` — string — Description for the model to decide when to transfer.
      - `variant` — string _(enum: `predefined`, `dynamic`, `directory`)_
      - `context` — string — Routing context for PREDEFINED transfers.
      - `extension` — string — Extension or phone number for PREDEFINED transfers.
      - `pipeline` — AgentTransferPipeline
        - `type` — string _(enum: `transfer`, `reply_and_transfer`, `reply_instructed_and_transfer`)_
        - `instructions` — string — Instructions for the model reply when type is REPLY_INSTRUCTED_AND_TRANSFER.
      - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
        - _array of_ `ChannelType`
      - `annotations` — array
        - _array of_ `AgentToolAnnotation`
          - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
  - **`hangup`**
    - `hangup` — AgentHangupCapability **(required)** — Let the model end the call. Honoured on the voice channel.
      - `name` — string — Tool name exposed to the model. Auto-generated when omitted.
      - `description` — string — Description for the model to decide when to hang up.
      - `pipeline` — AgentHangupPipeline
        - `type` — string _(enum: `hangup`, `reply_and_hangup`, `reply_instructed_and_hangup`)_
        - `instructions` — string — Instructions for the model reply when type is REPLY_INSTRUCTED_AND_HANGUP.
      - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
        - _array of_ `ChannelType`
      - `annotations` — array
        - _array of_ `AgentToolAnnotation`
          - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
  - **`wait`**
    - `wait` — AgentWaitCapability **(required)** — Let the model hold the call while it works (e.g. a lookup), keeping the caller on the line. Honoured on the voice channel.
      - `name` — string — Tool name exposed to the model. Auto-generated when omitted.
      - `description` — string — Description for the model to decide when to wait.
      - `message` — string — Message spoken when entering the wait state. Spoken in every language of the call while `messages` is absent or empty; not consulted once `messages` carries any entry.
      - `messages` — array — Per-language wait messages. Same rule as `AgentTool.startMessages`: the entry for the call's current language is spoken, a language with no entry is silent, and with no effective speech configuration `message` is spoken.
        - _array of_ `AgentSpokenPhrase`
          - _(nesting depth limit — see `AgentSpokenPhrase` in the Schemas appendix)_
      - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
        - _array of_ `ChannelType`
      - `annotations` — array
        - _array of_ `AgentToolAnnotation`
          - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_

**`AgentWorkflowActionHandler`**

_A step that performs one capability. The runtime performs it on arrival — no model decision about *whether* to act, and no tool offered to the model for it. Which is the point: an action the graph reached is an action that happens, at the cost of nothing._

- `capability` — union **(required)** — The capability a step performs, run by the runtime rather than chosen by the model. A subset of AgentCapability, reusing its structures verbatim: these are the members that describe a single action with a beginning and an end. The rest of AgentCapability (`kb`, `webSearch`, `webFetch`, `sandbox`, `suggestions`) describes reach the model draws on while it talks, so it belongs on a conversation step's `capabilities` rather than on a step of its own. Configuration comes from the capability itself and nothing is added here: a tool step's fixed arguments are `AgentTool.fields` predefined handlers, its spoken lead-in is `AgentTool.startMessage`, a transfer's line before the hand-off is `AgentTransferPipeline.instructions`, an invoked agent's inputs are `AgentCallCapability.variables`. Anything left unpinned is filled by the model at the step, per the tool's input schema.
  - _oneOf_ — exactly one of:
    - **`tool`**
      - `tool` — AgentTool **(required)**
        - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
        - `toolVersion` — number — Pin a specific published tool version. When omitted, the tool's latestVersion is resolved at load, so a republished tool reaches this agent without a new agent version. Pin it when `fields` must keep aiming at an exact input schema. _(min=1)_
        - `description` — string — Override the tool's description for this agent. When omitted, the tool's own description is used. _(minLen=1; maxLen=4096)_
        - `fields` — array — Per-field overrides on the tool input schema: pin fixed values (hidden from the model) or refine field descriptions. Fields not listed are filled by the model per the tool schema. Paths are resolved against the input schema of the tool version in effect — pin `toolVersion` when they must not move.
          - _(nesting depth limit — see `AgentToolField` in the Schemas appendix)_
        - `startMessage` — string — Message spoken when the tool call starts. Honoured on the voice channel. Spoken in every language of the call while `startMessages` is absent or empty; not consulted once `startMessages` carries any entry.
        - `startMessages` — array — Per-language start messages. When present and non-empty, the entry for the call's current language is spoken and `startMessage` is not consulted; a language with no entry is silent. When absent or empty, `startMessage` is spoken as before. On a call with no effective speech configuration — no configured languages, or a PBX below protocol 2 — `startMessage` is spoken regardless, because there is no current language to choose by.
          - _(nesting depth limit — see `AgentSpokenPhrase` in the Schemas appendix)_
        - `pipeline` — AgentToolPipeline
          - _(nesting depth limit — see `AgentToolPipeline` in the Schemas appendix)_
        - `approval` — AgentToolApproval — Human-in-the-loop confirmation for a tool. Presence requires approval: the agent pauses before running the tool and the session user (whoever controls the session) approves or denies inline.
          - _(nesting depth limit — see `AgentToolApproval` in the Schemas appendix)_
        - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
          - _(nesting depth limit — see `ChannelType` in the Schemas appendix)_
        - `annotations` — array
          - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
    - **`connector`**
      - `connector` — AgentConnectorCapability **(required)** — A configured connector (wilma-tools) exposed to the model as a single meta-tool named after the connector. The model calls the reserved `help` action to learn the callable actions, then dispatches an action through the same tool. Progressive disclosure runs through the connector tool itself, not the skills catalogue.
        - `id` — string **(required)** — Configured connector instance in wilma-tools. Its pinned definition, permission `grant` and authorization govern what the model can discover via `help` and call. There is no version pin here, unlike `AgentTool.toolVersion`: the action catalogue and its schemas are already frozen by the connector's pinned definition, while `grant` and authorization are read live so permission changes apply at once. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
        - `startMessage` — string — Message spoken when a connector action call starts. Honoured on the voice channel. Mirrors `AgentTool.startMessage`. Not applied to the read-only `help` action. Not consulted once `startMessages` carries any entry.
        - `startMessages` — array — Forward-compatible per-language connector start messages, mirroring `AgentTool.startMessages`. Accepted and stored so clients can configure connector and tool phrases consistently, but currently ignored at execution time because the voice runtime does not read connector start messages yet. Runtime enablement is tracked in wilma-services docs/todo.md item 8.
          - _(nesting depth limit — see `AgentSpokenPhrase` in the Schemas appendix)_
        - `pipeline` — AgentToolPipeline
          - _(nesting depth limit — see `AgentToolPipeline` in the Schemas appendix)_
        - `approval` — AgentToolApproval — Human-in-the-loop confirmation for a tool. Presence requires approval: the agent pauses before running the tool and the session user (whoever controls the session) approves or denies inline.
          - _(nesting depth limit — see `AgentToolApproval` in the Schemas appendix)_
        - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
          - _(nesting depth limit — see `ChannelType` in the Schemas appendix)_
        - `annotations` — array
          - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
    - **`agent`**
      - `agent` — AgentCallCapability **(required)** — Invoke another agent as a dedicated execution with its own state. The called agent runs independently and returns its result.
        - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
        - `agentVersion` — number — Pin a specific published version of the called agent. When absent, the called agent's deployment configuration selects the version at invocation time. _(min=1)_
        - `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
          - _(nesting depth limit — see `AgentAccess` in the Schemas appendix)_
        - `variables` — array
          - _(nesting depth limit — see `AgentToolVariable` in the Schemas appendix)_
        - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
          - _(nesting depth limit — see `ChannelType` in the Schemas appendix)_
    - **`handover`**
      - `handover` — AgentHandoverCapability **(required)** — Hand the conversation over to a human and leave it. Honoured on conversation channels (chat, assistant).
        - `name` — string — Tool name exposed to the model. Auto-generated when omitted.
        - `description` — string — Description for the model to decide when to hand over.
        - `variant` — string _(enum: `agent`, `service`)_
        - `agent` — string — Wilma agent to hand over to when variant = AGENT. _(minLen=12; maxLen=12)_
        - `agentVersion` — number — Pin a specific published version of the target agent when variant = AGENT. When absent, the target's deployment configuration selects the version at handover time. _(min=1)_
        - `service` — string — x-bees service id to hand over to when variant = SERVICE.
        - `silent` — boolean — Hand over without posting a visible message to the user.
        - `pipeline` — AgentHandoverPipeline
          - _(nesting depth limit — see `AgentHandoverPipeline` in the Schemas appendix)_
        - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
          - _(nesting depth limit — see `ChannelType` in the Schemas appendix)_
        - `annotations` — array
          - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
    - **`delegation`**
      - `delegation` — AgentDelegationCapability **(required)** — Delegate the conversation to another agent (max 3 transitions per turn). One capability entry per delegate target.
        - `name` — string — Tool name exposed to the model. Auto-generated when omitted.
        - `description` — string — Description for the model to decide when to delegate.
        - `id` — string **(required)** — Agent to delegate to. _(minLen=12; maxLen=12)_
        - `agentVersion` — number — Pin a specific published version of the delegate agent. When absent, the delegate's deployment configuration selects the version at delegation time. _(min=1)_
        - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
          - _(nesting depth limit — see `ChannelType` in the Schemas appendix)_
        - `annotations` — array
          - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
    - **`transfer`**
      - `transfer` — AgentTransferCapability **(required)** — Transfer the call to a PBX destination. Honoured on the voice channel. One capability entry per transfer target.
        - `name` — string — Tool name exposed to the model. Auto-generated when omitted.
        - `description` — string — Description for the model to decide when to transfer.
        - `variant` — string _(enum: `predefined`, `dynamic`, `directory`)_
        - `context` — string — Routing context for PREDEFINED transfers.
        - `extension` — string — Extension or phone number for PREDEFINED transfers.
        - `pipeline` — AgentTransferPipeline
          - _(nesting depth limit — see `AgentTransferPipeline` in the Schemas appendix)_
        - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
          - _(nesting depth limit — see `ChannelType` in the Schemas appendix)_
        - `annotations` — array
          - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
    - **`hangup`**
      - `hangup` — AgentHangupCapability **(required)** — Let the model end the call. Honoured on the voice channel.
        - `name` — string — Tool name exposed to the model. Auto-generated when omitted.
        - `description` — string — Description for the model to decide when to hang up.
        - `pipeline` — AgentHangupPipeline
          - _(nesting depth limit — see `AgentHangupPipeline` in the Schemas appendix)_
        - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
          - _(nesting depth limit — see `ChannelType` in the Schemas appendix)_
        - `annotations` — array
          - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
    - **`wait`**
      - `wait` — AgentWaitCapability **(required)** — Let the model hold the call while it works (e.g. a lookup), keeping the caller on the line. Honoured on the voice channel.
        - `name` — string — Tool name exposed to the model. Auto-generated when omitted.
        - `description` — string — Description for the model to decide when to wait.
        - `message` — string — Message spoken when entering the wait state. Spoken in every language of the call while `messages` is absent or empty; not consulted once `messages` carries any entry.
        - `messages` — array — Per-language wait messages. Same rule as `AgentTool.startMessages`: the entry for the call's current language is spoken, a language with no entry is silent, and with no effective speech configuration `message` is spoken.
          - _(nesting depth limit — see `AgentSpokenPhrase` in the Schemas appendix)_
        - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
          - _(nesting depth limit — see `ChannelType` in the Schemas appendix)_
        - `annotations` — array
          - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
- `forceToolCall` — boolean — Run the step as one model call with the tool choice pinned to this capability, instead of calling it straight from the runtime. The model still cannot decide *whether* to call it — only what to put in the arguments left unpinned, which is what a lookup keyed on something nobody can template ('the symptom the caller just described') needs. Costs one model call where the default costs none, so it is opt-in. Honoured where the action has arguments a model can write — `tool`, `connector`, `agent`, and a `transfer` whose target the model chooses; ignored elsewhere. Leaving it false while a required argument is unpinned is an authoring error, not a runtime one: nothing would be there to fill it.
- `output` — string — Workflow variable the action's result is written to, so later `expression` conditions can branch on it and later steps can template it (e.g. capture a lookup into `policy`, then branch on `{ "==": [{ "var": "policy.status" }, "active"] }`). Absent means the result is not captured; the model still sees it in the conversation per the capability's own pipeline. Written on success only. A failed action leaves the variable as it was and takes a `failure` transition instead — see AgentWorkflowFailureCondition — so a graph can never mistake an error for a result. _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_

**`AgentWorkflowAlwaysCondition`**

_Unconditional. Only legal as a step's single transition: two unconditional exits are a coin toss, not a routing decision._

- AgentWorkflowAlwaysCondition

**`AgentWorkflowAssignment`**

_One `name = value` write. Exactly one of `value` or `expression` is set: `value` renders text, `expression` computes._

- `name` — string **(required)** _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
- `value` — string — Text written to the variable, with handlebars resolved against workflow variables, agent variables and session context (e.g. '{{lookup.status}}'). Empty clears the variable. _(maxLen=4000)_
- `expression` — any — A JsonLogic expression computing the value instead of rendering it, which is what makes arithmetic possible: `{ "+": [{ "var": "attempts" }, 1] }` is the retry counter a bounded loop needs, written with no model in the loop.

**`AgentWorkflowCondition`**

_How the runtime decides to take a transition. Exactly one member is set._

- _oneOf_ — exactly one of:
  - **`always`**
    - `always` — AgentWorkflowAlwaysCondition **(required)** — Unconditional. Only legal as a step's single transition: two unconditional exits are a coin toss, not a routing decision.
  - **`prompt`**
    - `prompt` — AgentWorkflowPromptCondition **(required)** — A condition the model judges against the conversation, e.g. 'the caller has said they will try the fix'. Phrase it as something the **caller** has done. A condition describing what the *agent* has done — 'the caller has a next step to try' — is true the instant the agent names one, so the model leaves before the caller has answered, and one early exit cascades through the rest of the graph. Rewording the same exits from agent actions to caller actions, changing nothing else, moved three models from 58–64 % of turns on the right step to 96–100 %, and removed every stray move. It is the single largest effect measured on this contract, so an authoring surface that accepts an agent-action condition is the defect, not the wording.
      - `instructions` — string **(required)** _(minLen=1; maxLen=2000)_
  - **`expression`**
    - `expression` — AgentWorkflowExpressionCondition **(required)** — A branch taken when workflow state satisfies the condition — no model judgement involved, which is what makes it the right condition after an `action` or `variables` step.
      - `conditions` — any **(required)** — A JsonLogic condition tree evaluated against workflow state, e.g. `{ "==": [ { "var": "lookup.status" }, "found" ] }`. The `var` namespace is the workflow variables written by `variables` steps and action `output` captures, the agent's input variables (`engine.ai.variables`), and the session context. An empty tree always matches. This is a separate language from the rule-tree AutomationConditions (wilma-workflows) and CopilotConditions (wilma-copilot).
  - **`result`**
    - `result` — AgentWorkflowResultCondition **(required)** — A branch on which result a nested workflow returned. Only meaningful on a `workflow` step; the referenced step must be a `result` step of the nested workflow that step runs.
      - `result` — string **(required)** — Id of the `result` step reached inside the nested workflow. An id rather than a name, so renaming a result from 'failed' to 'gave up' does not unwire every step that handles it. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
  - **`failure`**
    - `failure` — AgentWorkflowFailureCondition **(required)** — A branch taken when the step's action fails. Only meaningful on an `action` step, and the only condition a terminal action may carry: a transfer that finds the extension busy has not left the session, so a graph that cannot say what happens next simply drops the caller. Failure short-circuits — when an action fails, only `failure` transitions are considered, never the `expression` or `prompt` branches that were written for its result. If none matches, the session fails with the action's error, so a step whose capability can fail wants a catch-all last in the list.
      - `kinds` — array — Kinds this branch handles, evaluated as a set. Absent or empty catches **any** failure — the catch-all, which the list order must therefore place after the specific branches.
        - _array of_ `AgentWorkflowFailureKind`
  - **`fallback`**
    - `fallback` — AgentWorkflowFallbackCondition **(required)** — The else-branch, taken when no sibling matched. At most one per step, and reached last regardless of where it sits in the list.

**`AgentWorkflowConversationChannelsSettings`**

_Per-channel settings of a conversation step. Only voice has anything to say about a stretch of conversation today; the chat and assistant surfaces deliver it as they deliver every other reply._

- `voice` — AgentWorkflowConversationVoiceSettings — Voice-channel settings for a conversation step, overriding VoiceChannelSettings while it is live. Ignored on other channels.
  - `interruptions` — VoiceInterruptionSettings
    - `enabled` — boolean **(required)** — Whether the caller can interrupt the agent while it is speaking.
    - `minWords` — number — Minimum number of caller words that count as an interruption. _(min=1; max=10)_

**`AgentWorkflowConversationHandler`**

_A stretch of conversation with a goal: the model talks, may use the capabilities in scope, and the step's transitions are evaluated against what happens. This is the only handler that leaves control where it is until a transition matches — a step whose conditions all stay false simply keeps talking. Deliberately not configurable per step: the model, and how readily the step is left. The model is the agent's (`engine.ai.model`) because a session that swaps models mid-conversation swaps voice, latency and tool-calling behaviour with it. How readily a step is left is decided by how its transitions are worded — conditions describing what the *caller* has done keep a model on the step, and no eagerness dial moves that number._

- `goal` — string **(required)** — What the agent is trying to achieve here, appended to the agent's `engine.ai.instructions`. Never a replacement for them: identity, tone and standing rules hold across every step, and a step that needs different ones is a different agent. _(minLen=1; maxLen=10000)_
- `entry` — string — How a conversation step starts. _(enum: `auto`, `speak_first`, `listen_first`)_
- `channels` — AgentWorkflowConversationChannelsSettings — Per-channel settings of a conversation step. Only voice has anything to say about a stretch of conversation today; the chat and assistant surfaces deliver it as they deliver every other reply.
  - `voice` — AgentWorkflowConversationVoiceSettings — Voice-channel settings for a conversation step, overriding VoiceChannelSettings while it is live. Ignored on other channels.
    - `interruptions` — VoiceInterruptionSettings
      - `enabled` — boolean **(required)** — Whether the caller can interrupt the agent while it is speaking.
      - `minWords` — number — Minimum number of caller words that count as an interruption. _(min=1; max=10)_
- `capabilities` — array — Capabilities offered to the model *in addition* to `engine.ai.capabilities` while this step runs, configured exactly as they are there — the same union, the same structures. Use it to give a step reach it should not have everywhere: authoring the refund tool on the refund step, rather than on the agent, is also what keeps it out of every other step. Additive only, by design. A step cannot drop an agent-level capability, so it cannot strand a session by taking away the `handover` or `transfer` its channel needs, and the runtime keeps one rule for the turn's tool set. Skills the model loads (`engine.ai.skills`) and the channel's own built-ins join it either way.
  - _array of_ `AgentCapability`
    - _oneOf_ — exactly one of:
      - **`tool`**
        - `tool` — AgentTool **(required)**
          - _(nesting depth limit — see `AgentTool` in the Schemas appendix)_
      - **`connector`**
        - `connector` — AgentConnectorCapability **(required)** — A configured connector (wilma-tools) exposed to the model as a single meta-tool named after the connector. The model calls the reserved `help` action to learn the callable actions, then dispatches an action through the same tool. Progressive disclosure runs through the connector tool itself, not the skills catalogue.
          - _(nesting depth limit — see `AgentConnectorCapability` in the Schemas appendix)_
      - **`kb`**
        - `kb` — AgentKnowledgeBase **(required)**
          - _(nesting depth limit — see `AgentKnowledgeBase` in the Schemas appendix)_
      - **`sandbox`**
        - `sandbox` — union **(required)** — Embedded sandbox: shell + file tools backed by an execution environment. The only capability with no `channels` list — being a union it has nowhere to carry one — so it is offered on every channel the agent serves.
          - _(nesting depth limit — see `AgentSandboxCapability` in the Schemas appendix)_
      - **`webSearch`**
        - `webSearch` — AgentWebSearchCapability **(required)** — Model-native web search. The provider tool is selected from the agent model.
          - _(nesting depth limit — see `AgentWebSearchCapability` in the Schemas appendix)_
      - **`webFetch`**
        - `webFetch` — AgentWebFetchCapability **(required)** — Server-side fetch of a URL, returning its readable text/markdown to the model.
          - _(nesting depth limit — see `AgentWebFetchCapability` in the Schemas appendix)_
      - **`agent`**
        - `agent` — AgentCallCapability **(required)** — Invoke another agent as a dedicated execution with its own state. The called agent runs independently and returns its result.
          - _(nesting depth limit — see `AgentCallCapability` in the Schemas appendix)_
      - **`handover`**
        - `handover` — AgentHandoverCapability **(required)** — Hand the conversation over to a human and leave it. Honoured on conversation channels (chat, assistant).
          - _(nesting depth limit — see `AgentHandoverCapability` in the Schemas appendix)_
      - **`delegation`**
        - `delegation` — AgentDelegationCapability **(required)** — Delegate the conversation to another agent (max 3 transitions per turn). One capability entry per delegate target.
          - _(nesting depth limit — see `AgentDelegationCapability` in the Schemas appendix)_
      - **`transfer`**
        - `transfer` — AgentTransferCapability **(required)** — Transfer the call to a PBX destination. Honoured on the voice channel. One capability entry per transfer target.
          - _(nesting depth limit — see `AgentTransferCapability` in the Schemas appendix)_
      - **`suggestions`**
        - `suggestions` — AgentSuggestionsCapability **(required)** — Emit suggested replies for human operators. Honoured on the chat channel.
          - _(nesting depth limit — see `AgentSuggestionsCapability` in the Schemas appendix)_
      - **`hangup`**
        - `hangup` — AgentHangupCapability **(required)** — Let the model end the call. Honoured on the voice channel.
          - _(nesting depth limit — see `AgentHangupCapability` in the Schemas appendix)_
      - **`wait`**
        - `wait` — AgentWaitCapability **(required)** — Let the model hold the call while it works (e.g. a lookup), keeping the caller on the line. Honoured on the voice channel.
          - _(nesting depth limit — see `AgentWaitCapability` in the Schemas appendix)_

**`AgentWorkflowConversationVoiceSettings`**

_Voice-channel settings for a conversation step, overriding VoiceChannelSettings while it is live. Ignored on other channels._

- `interruptions` — VoiceInterruptionSettings
  - `enabled` — boolean **(required)** — Whether the caller can interrupt the agent while it is speaking.
  - `minWords` — number — Minimum number of caller words that count as an interruption. _(min=1; max=10)_

**`AgentWorkflowEndHandler`**

_The session is over. Terminal and configuration-free by design: a closing line is a `message` step in front of it, and releasing a call is the `hangup` action — both already exist, and neither needs restating here._

- AgentWorkflowEndHandler

**`AgentWorkflowEntryBehavior`**

_How a conversation step starts._

- string _(enum: `auto`, `speak_first`, `listen_first`)_

**`AgentWorkflowExpressionCondition`**

_A branch taken when workflow state satisfies the condition — no model judgement involved, which is what makes it the right condition after an `action` or `variables` step._

- `conditions` — any **(required)** — A JsonLogic condition tree evaluated against workflow state, e.g. `{ "==": [ { "var": "lookup.status" }, "found" ] }`. The `var` namespace is the workflow variables written by `variables` steps and action `output` captures, the agent's input variables (`engine.ai.variables`), and the session context. An empty tree always matches. This is a separate language from the rule-tree AutomationConditions (wilma-workflows) and CopilotConditions (wilma-copilot).

**`AgentWorkflowFailureCondition`**

_A branch taken when the step's action fails. Only meaningful on an `action` step, and the only condition a terminal action may carry: a transfer that finds the extension busy has not left the session, so a graph that cannot say what happens next simply drops the caller. Failure short-circuits — when an action fails, only `failure` transitions are considered, never the `expression` or `prompt` branches that were written for its result. If none matches, the session fails with the action's error, so a step whose capability can fail wants a catch-all last in the list._

- `kinds` — array — Kinds this branch handles, evaluated as a set. Absent or empty catches **any** failure — the catch-all, which the list order must therefore place after the specific branches.
  - _array of_ `AgentWorkflowFailureKind`

**`AgentWorkflowFailureKind`**

_How an action failed, as far as the runtime can tell. Deliberately a short list of kinds an author can write a different recovery for — a busy extension is a different flow from an expired credential — rather than a mirror of every provider's error codes. The message and the provider's own detail stay on the invocation event and the trace; a graph branches on the kind._

- string _(enum: `timeout`, `denied`, `unauthorized`, `not_found`, `invalid_input`, `rate_limited`, `unavailable`, `error`)_

**`AgentWorkflowFallbackCondition`**

_The else-branch, taken when no sibling matched. At most one per step, and reached last regardless of where it sits in the list._

- AgentWorkflowFallbackCondition

**`AgentWorkflowHandler`**

_What a step does. Exactly one member is set. `action` carries a capability; the others are workflow-only handlers with no capability equivalent._

- _oneOf_ — exactly one of:
  - **`conversation`**
    - `conversation` — AgentWorkflowConversationHandler **(required)** — A stretch of conversation with a goal: the model talks, may use the capabilities in scope, and the step's transitions are evaluated against what happens. This is the only handler that leaves control where it is until a transition matches — a step whose conditions all stay false simply keeps talking. Deliberately not configurable per step: the model, and how readily the step is left. The model is the agent's (`engine.ai.model`) because a session that swaps models mid-conversation swaps voice, latency and tool-calling behaviour with it. How readily a step is left is decided by how its transitions are worded — conditions describing what the *caller* has done keep a model on the step, and no eagerness dial moves that number.
      - `goal` — string **(required)** — What the agent is trying to achieve here, appended to the agent's `engine.ai.instructions`. Never a replacement for them: identity, tone and standing rules hold across every step, and a step that needs different ones is a different agent. _(minLen=1; maxLen=10000)_
      - `entry` — string — How a conversation step starts. _(enum: `auto`, `speak_first`, `listen_first`)_
      - `channels` — AgentWorkflowConversationChannelsSettings — Per-channel settings of a conversation step. Only voice has anything to say about a stretch of conversation today; the chat and assistant surfaces deliver it as they deliver every other reply.
        - `voice` — AgentWorkflowConversationVoiceSettings — Voice-channel settings for a conversation step, overriding VoiceChannelSettings while it is live. Ignored on other channels.
          - _(nesting depth limit — see `AgentWorkflowConversationVoiceSettings` in the Schemas appendix)_
      - `capabilities` — array — Capabilities offered to the model *in addition* to `engine.ai.capabilities` while this step runs, configured exactly as they are there — the same union, the same structures. Use it to give a step reach it should not have everywhere: authoring the refund tool on the refund step, rather than on the agent, is also what keeps it out of every other step. Additive only, by design. A step cannot drop an agent-level capability, so it cannot strand a session by taking away the `handover` or `transfer` its channel needs, and the runtime keeps one rule for the turn's tool set. Skills the model loads (`engine.ai.skills`) and the channel's own built-ins join it either way.
        - _array of_ `AgentCapability`
          - _(nesting depth limit — see `AgentCapability` in the Schemas appendix)_
  - **`message`**
    - `message` — AgentWorkflowMessageHandler **(required)** — Say one thing — spoken on voice, posted on chat / assistant — then move on. The line is either authored verbatim or generated at the step; either way the agent says it once and the transitions are evaluated, with no turn handed to the user.
      - `content` — union **(required)** — Where the step's line comes from. Exactly one member is set: `text` is authored, `generate` is written by the model at the step.
        - _oneOf_ — exactly one of:
          - **`text`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`generate`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `channels` — AgentWorkflowMessageChannelsSettings — Per-channel settings of a message step: how the line is protected when spoken, and what is offered with it when posted.
        - `voice` — AgentWorkflowMessageVoiceSettings — Voice-channel settings for a message step, honoured while the line is spoken. Ignored on other channels.
          - _(nesting depth limit — see `AgentWorkflowMessageVoiceSettings` in the Schemas appendix)_
        - `chat` — AgentWorkflowMessageChatSettings — Chat-channel settings for a message step, honoured where a line is posted rather than spoken. Ignored on voice.
          - _(nesting depth limit — see `AgentWorkflowMessageChatSettings` in the Schemas appendix)_
  - **`action`**
    - `action` — AgentWorkflowActionHandler **(required)** — A step that performs one capability. The runtime performs it on arrival — no model decision about *whether* to act, and no tool offered to the model for it. Which is the point: an action the graph reached is an action that happens, at the cost of nothing.
      - `capability` — union **(required)** — The capability a step performs, run by the runtime rather than chosen by the model. A subset of AgentCapability, reusing its structures verbatim: these are the members that describe a single action with a beginning and an end. The rest of AgentCapability (`kb`, `webSearch`, `webFetch`, `sandbox`, `suggestions`) describes reach the model draws on while it talks, so it belongs on a conversation step's `capabilities` rather than on a step of its own. Configuration comes from the capability itself and nothing is added here: a tool step's fixed arguments are `AgentTool.fields` predefined handlers, its spoken lead-in is `AgentTool.startMessage`, a transfer's line before the hand-off is `AgentTransferPipeline.instructions`, an invoked agent's inputs are `AgentCallCapability.variables`. Anything left unpinned is filled by the model at the step, per the tool's input schema.
        - _oneOf_ — exactly one of:
          - **`tool`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`connector`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`agent`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`handover`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`delegation`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`transfer`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`hangup`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`wait`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `forceToolCall` — boolean — Run the step as one model call with the tool choice pinned to this capability, instead of calling it straight from the runtime. The model still cannot decide *whether* to call it — only what to put in the arguments left unpinned, which is what a lookup keyed on something nobody can template ('the symptom the caller just described') needs. Costs one model call where the default costs none, so it is opt-in. Honoured where the action has arguments a model can write — `tool`, `connector`, `agent`, and a `transfer` whose target the model chooses; ignored elsewhere. Leaving it false while a required argument is unpinned is an authoring error, not a runtime one: nothing would be there to fill it.
      - `output` — string — Workflow variable the action's result is written to, so later `expression` conditions can branch on it and later steps can template it (e.g. capture a lookup into `policy`, then branch on `{ "==": [{ "var": "policy.status" }, "active"] }`). Absent means the result is not captured; the model still sees it in the conversation per the capability's own pipeline. Written on success only. A failed action leaves the variable as it was and takes a `failure` transition instead — see AgentWorkflowFailureCondition — so a graph can never mistake an error for a result. _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
  - **`variables`**
    - `variables` — AgentWorkflowVariablesHandler **(required)** — Write workflow variables. The step nobody asks for until the first time a graph has to remember something between two branches.
      - `assignments` — array **(required)** _(minItems=1; maxItems=50)_
        - _array of_ `AgentWorkflowAssignment`
          - _(nesting depth limit — see `AgentWorkflowAssignment` in the Schemas appendix)_
  - **`workflow`**
    - `workflow` — AgentWorkflowInvokeHandler **(required)** — Run a nested workflow and continue once it returns. The unit of decomposition: a twelve-step identity check is called from the front door, from the booking flow and from the complaints line, so it is authored once and referenced by a single step at each call site. The nested workflow shares this session and its variables; it returns through its `result` steps, which is what the calling step's `result` transitions branch on. A nested workflow that instead reaches an `end` or a terminal action does what it says — the session is over and nothing comes back.
      - `workflow` — string **(required)** — The nested workflow to run. Must be declared in `AgentWorkflow.nested`, and must not run itself directly or through a ring of nested workflows. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
      - `output` — string — Workflow variable the nested workflow's result `value` is written to. Absent means the value is discarded — which is the usual case when the branch taken is the whole answer. _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
  - **`result`**
    - `result` — AgentWorkflowResultHandler **(required)** — End this workflow and hand control back to whatever invoked it. In a nested workflow the invoking step resumes and branches on which result was reached (see AgentWorkflowResultCondition). In the main graph of a workflow-channel agent the run finishes and the result is returned to the caller — the agent, automation or API request that started it. In the main graph of a voice / chat / assistant agent there is no invoker, so it behaves as `end`.
      - `value` — string — What this result returns to the invoker. Supports handlebars resolved against workflow variables, agent variables and session context (e.g. '{{policy.number}}'). Absent returns the result's id alone, which is enough when the caller only branches on which result was reached. _(minLen=1; maxLen=8000)_
  - **`end`**
    - `end` — AgentWorkflowEndHandler **(required)** — The session is over. Terminal and configuration-free by design: a closing line is a `message` step in front of it, and releasing a call is the `hangup` action — both already exist, and neither needs restating here.

**`AgentWorkflowInvokeHandler`**

_Run a nested workflow and continue once it returns. The unit of decomposition: a twelve-step identity check is called from the front door, from the booking flow and from the complaints line, so it is authored once and referenced by a single step at each call site. The nested workflow shares this session and its variables; it returns through its `result` steps, which is what the calling step's `result` transitions branch on. A nested workflow that instead reaches an `end` or a terminal action does what it says — the session is over and nothing comes back._

- `workflow` — string **(required)** — The nested workflow to run. Must be declared in `AgentWorkflow.nested`, and must not run itself directly or through a ring of nested workflows. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
- `output` — string — Workflow variable the nested workflow's result `value` is written to. Absent means the value is discarded — which is the usual case when the branch taken is the whole answer. _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_

**`AgentWorkflowLayout`**

_How the builder arranges the graph. Authoring metadata: the runtime ignores it. `stages` bands the graph by `stage`, which is what a forty-step workflow needs._

- string _(enum: `flow`, `compact`, `stages`)_

**`AgentWorkflowMessageButton`**

_One button offered under the step's line._

- `text` — string **(required)** — Label shown on the button. Supports handlebars resolved against workflow variables, agent variables and session context. _(minLen=1; maxLen=96)_
- `handler` — union **(required)** — What tapping a button does.
  - _oneOf_ — exactly one of:
    - **`reply`**
      - `reply` — AgentWorkflowMessageButtonReplyHandler **(required)** — Tapping the button sends a reply on the user's behalf, which then drives this step's transitions like anything else the user says.
        - `text` — string — The text sent as the user's reply. Defaults to the button's own `text`. _(minLen=1; maxLen=128)_
    - **`link`**
      - `link` — AgentWorkflowMessageButtonLinkHandler **(required)** — Tapping the button opens a URL. The session stays where it is — a link is not an answer, so it cannot satisfy a transition on its own.
        - `url` — string **(required)** _(minLen=3; maxLen=2048)_
- `variant` — string — How a reply button is rendered. Matches the x-bees `ButtonVariant`. Defaults to the client's own default. _(enum: `contained`, `outlined`)_

**`AgentWorkflowMessageButtonHandler`**

_What tapping a button does._

- _oneOf_ — exactly one of:
  - **`reply`**
    - `reply` — AgentWorkflowMessageButtonReplyHandler **(required)** — Tapping the button sends a reply on the user's behalf, which then drives this step's transitions like anything else the user says.
      - `text` — string — The text sent as the user's reply. Defaults to the button's own `text`. _(minLen=1; maxLen=128)_
  - **`link`**
    - `link` — AgentWorkflowMessageButtonLinkHandler **(required)** — Tapping the button opens a URL. The session stays where it is — a link is not an answer, so it cannot satisfy a transition on its own.
      - `url` — string **(required)** _(minLen=3; maxLen=2048)_

**`AgentWorkflowMessageButtonLinkHandler`**

_Tapping the button opens a URL. The session stays where it is — a link is not an answer, so it cannot satisfy a transition on its own._

- `url` — string **(required)** _(minLen=3; maxLen=2048)_

**`AgentWorkflowMessageButtonReplyHandler`**

_Tapping the button sends a reply on the user's behalf, which then drives this step's transitions like anything else the user says._

- `text` — string — The text sent as the user's reply. Defaults to the button's own `text`. _(minLen=1; maxLen=128)_

**`AgentWorkflowMessageButtonVariant`**

_How a reply button is rendered. Matches the x-bees `ButtonVariant`. Defaults to the client's own default._

- string _(enum: `contained`, `outlined`)_

**`AgentWorkflowMessageChannelsSettings`**

_Per-channel settings of a message step: how the line is protected when spoken, and what is offered with it when posted._

- `voice` — AgentWorkflowMessageVoiceSettings — Voice-channel settings for a message step, honoured while the line is spoken. Ignored on other channels.
  - `interruptions` — VoiceInterruptionSettings
    - `enabled` — boolean **(required)** — Whether the caller can interrupt the agent while it is speaking.
    - `minWords` — number — Minimum number of caller words that count as an interruption. _(min=1; max=10)_
- `chat` — AgentWorkflowMessageChatSettings — Chat-channel settings for a message step, honoured where a line is posted rather than spoken. Ignored on voice.
  - `suggestions` — array — Reply buttons posted with the line, e.g. 'Yes, go ahead' / 'No, not now' under a confirmation. Delivered as an x-bees `actions` element of `button` elements, so a tap either sends a reply — which the step's transitions then read like any other user message — or opens a link. Only offered on a fixed line: a conversation step is the model's to word, and buttons authored under words it has not chosen yet would contradict each other. _(minItems=1; maxItems=10)_
    - _array of_ `AgentWorkflowMessageButton`
      - `text` — string **(required)** — Label shown on the button. Supports handlebars resolved against workflow variables, agent variables and session context. _(minLen=1; maxLen=96)_
      - `handler` — union **(required)** — What tapping a button does.
        - _(nesting depth limit — see `AgentWorkflowMessageButtonHandler` in the Schemas appendix)_
      - `variant` — string — How a reply button is rendered. Matches the x-bees `ButtonVariant`. Defaults to the client's own default. _(enum: `contained`, `outlined`)_

**`AgentWorkflowMessageChatSettings`**

_Chat-channel settings for a message step, honoured where a line is posted rather than spoken. Ignored on voice._

- `suggestions` — array — Reply buttons posted with the line, e.g. 'Yes, go ahead' / 'No, not now' under a confirmation. Delivered as an x-bees `actions` element of `button` elements, so a tap either sends a reply — which the step's transitions then read like any other user message — or opens a link. Only offered on a fixed line: a conversation step is the model's to word, and buttons authored under words it has not chosen yet would contradict each other. _(minItems=1; maxItems=10)_
  - _array of_ `AgentWorkflowMessageButton`
    - `text` — string **(required)** — Label shown on the button. Supports handlebars resolved against workflow variables, agent variables and session context. _(minLen=1; maxLen=96)_
    - `handler` — union **(required)** — What tapping a button does.
      - _oneOf_ — exactly one of:
        - **`reply`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`link`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `variant` — string — How a reply button is rendered. Matches the x-bees `ButtonVariant`. Defaults to the client's own default. _(enum: `contained`, `outlined`)_

**`AgentWorkflowMessageContent`**

_Where the step's line comes from. Exactly one member is set: `text` is authored, `generate` is written by the model at the step._

- _oneOf_ — exactly one of:
  - **`text`**
    - `text` — string **(required)** — The line, verbatim. No model in the loop, which is what makes it the right content for a disclosure, a policy sentence or a legally worded confirmation. _(minLen=1; maxLen=4000)_
  - **`generate`**
    - `generate` — AgentWorkflowMessageGeneration **(required)** — A line the model writes at this step, from the conversation and whatever the graph has gathered — 'greet the caller by the name on the contact record and mention any open orders'. One model call, no tools offered, no waiting for a reply: the agent says exactly one thing and the step's transitions are evaluated. The difference from a conversation step is that this is a *speech act*, not a stretch of conversation: the model cannot decide to stay quiet, cannot act, and cannot keep the step. Use it where the words must fit the data but the shape of the session must not depend on how they came out.
      - `instructions` — string **(required)** — What to say, as an instruction to the model rather than the words themselves. Supports handlebars resolved against workflow variables, agent variables and session context, so an action's `output` captured a step earlier is available verbatim (e.g. 'Greet {{contact.firstName}} and mention their {{contact.openOrders}} open orders'). _(minLen=1; maxLen=4000)_

**`AgentWorkflowMessageGeneration`**

_A line the model writes at this step, from the conversation and whatever the graph has gathered — 'greet the caller by the name on the contact record and mention any open orders'. One model call, no tools offered, no waiting for a reply: the agent says exactly one thing and the step's transitions are evaluated. The difference from a conversation step is that this is a *speech act*, not a stretch of conversation: the model cannot decide to stay quiet, cannot act, and cannot keep the step. Use it where the words must fit the data but the shape of the session must not depend on how they came out._

- `instructions` — string **(required)** — What to say, as an instruction to the model rather than the words themselves. Supports handlebars resolved against workflow variables, agent variables and session context, so an action's `output` captured a step earlier is available verbatim (e.g. 'Greet {{contact.firstName}} and mention their {{contact.openOrders}} open orders'). _(minLen=1; maxLen=4000)_

**`AgentWorkflowMessageHandler`**

_Say one thing — spoken on voice, posted on chat / assistant — then move on. The line is either authored verbatim or generated at the step; either way the agent says it once and the transitions are evaluated, with no turn handed to the user._

- `content` — union **(required)** — Where the step's line comes from. Exactly one member is set: `text` is authored, `generate` is written by the model at the step.
  - _oneOf_ — exactly one of:
    - **`text`**
      - `text` — string **(required)** — The line, verbatim. No model in the loop, which is what makes it the right content for a disclosure, a policy sentence or a legally worded confirmation. _(minLen=1; maxLen=4000)_
    - **`generate`**
      - `generate` — AgentWorkflowMessageGeneration **(required)** — A line the model writes at this step, from the conversation and whatever the graph has gathered — 'greet the caller by the name on the contact record and mention any open orders'. One model call, no tools offered, no waiting for a reply: the agent says exactly one thing and the step's transitions are evaluated. The difference from a conversation step is that this is a *speech act*, not a stretch of conversation: the model cannot decide to stay quiet, cannot act, and cannot keep the step. Use it where the words must fit the data but the shape of the session must not depend on how they came out.
        - `instructions` — string **(required)** — What to say, as an instruction to the model rather than the words themselves. Supports handlebars resolved against workflow variables, agent variables and session context, so an action's `output` captured a step earlier is available verbatim (e.g. 'Greet {{contact.firstName}} and mention their {{contact.openOrders}} open orders'). _(minLen=1; maxLen=4000)_
- `channels` — AgentWorkflowMessageChannelsSettings — Per-channel settings of a message step: how the line is protected when spoken, and what is offered with it when posted.
  - `voice` — AgentWorkflowMessageVoiceSettings — Voice-channel settings for a message step, honoured while the line is spoken. Ignored on other channels.
    - `interruptions` — VoiceInterruptionSettings
      - `enabled` — boolean **(required)** — Whether the caller can interrupt the agent while it is speaking.
      - `minWords` — number — Minimum number of caller words that count as an interruption. _(min=1; max=10)_
  - `chat` — AgentWorkflowMessageChatSettings — Chat-channel settings for a message step, honoured where a line is posted rather than spoken. Ignored on voice.
    - `suggestions` — array — Reply buttons posted with the line, e.g. 'Yes, go ahead' / 'No, not now' under a confirmation. Delivered as an x-bees `actions` element of `button` elements, so a tap either sends a reply — which the step's transitions then read like any other user message — or opens a link. Only offered on a fixed line: a conversation step is the model's to word, and buttons authored under words it has not chosen yet would contradict each other. _(minItems=1; maxItems=10)_
      - _array of_ `AgentWorkflowMessageButton`
        - _(nesting depth limit — see `AgentWorkflowMessageButton` in the Schemas appendix)_

**`AgentWorkflowMessageVoiceSettings`**

_Voice-channel settings for a message step, honoured while the line is spoken. Ignored on other channels._

- `interruptions` — VoiceInterruptionSettings
  - `enabled` — boolean **(required)** — Whether the caller can interrupt the agent while it is speaking.
  - `minWords` — number — Minimum number of caller words that count as an interruption. _(min=1; max=10)_

**`AgentWorkflowNested`**

_A named graph the main workflow — or another nested workflow — can run, referenced by AgentWorkflowInvokeHandler._

- `entry` — string **(required)** — Step the graph starts at. Must be one of `steps`. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
- `steps` — array **(required)** — Steps of one graph. Ids are unique within it. _(minItems=1; maxItems=200)_
  - _array of_ `AgentWorkflowStep`
    - `id` — string **(required)** — Identifier of a step within its workflow, unique per workflow (the main graph and each nested workflow are separate scopes). Stable and machine-facing: transitions reference it, and a result step's id is the name a caller branches on, so renaming a step's `label` never unwires the graph. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
    - `label` — string **(required)** — Human readable name of a step, e.g. 'Transfer to the sales desk'. Shown in the builder and in traces, and read by the model too: when this step is an exit of the live step, the label is the preview offered alongside the exit's condition. Never a routing key — see AgentWorkflowStepId — so renaming one never unwires a graph. _(minLen=1; maxLen=128)_
    - `stage` — string — The phase this step belongs to. Inherited by steps downstream, so a handful of tags organise a long graph. _(minLen=1; maxLen=64)_
    - `handler` — union **(required)** — What a step does. Exactly one member is set. `action` carries a capability; the others are workflow-only handlers with no capability equivalent.
      - _oneOf_ — exactly one of:
        - **`conversation`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`message`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`action`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`variables`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`workflow`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`result`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`end`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `transitions` — array — The ways out of this step. Must be non-empty on every step that stays in the session, since a step the runtime cannot leave is a dead end. On `result` and `end` it must be empty. On the `action` members that leave the session (`handover`, `delegation`, `transfer`, `hangup`) it may carry `failure` transitions and nothing else: an action that was supposed to leave and failed — a busy extension, a service desk with nobody on it — has not left, and a graph with no answer for that drops the caller.
      - _array of_ `AgentWorkflowTransition`
        - _(nesting depth limit — see `AgentWorkflowTransition` in the Schemas appendix)_
    - `position` — AgentWorkflowStepPosition — Canvas coordinates of a step in the builder. Authoring metadata: the runtime ignores it, and a workflow that arrives without positions is laid out automatically.
      - `x` — number **(required)**
      - `y` — number **(required)**
- `id` — string **(required)** — Identifier of a nested workflow within the agent's workflow. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
- `name` — string **(required)** _(minLen=1; maxLen=128)_
- `description` — string — One line saying what the nested workflow is for, shown on the step that runs it. _(minLen=1; maxLen=1000)_

**`AgentWorkflowPromptCondition`**

_A condition the model judges against the conversation, e.g. 'the caller has said they will try the fix'. Phrase it as something the **caller** has done. A condition describing what the *agent* has done — 'the caller has a next step to try' — is true the instant the agent names one, so the model leaves before the caller has answered, and one early exit cascades through the rest of the graph. Rewording the same exits from agent actions to caller actions, changing nothing else, moved three models from 58–64 % of turns on the right step to 96–100 %, and removed every stray move. It is the single largest effect measured on this contract, so an authoring surface that accepts an agent-action condition is the defect, not the wording._

- `instructions` — string **(required)** _(minLen=1; maxLen=2000)_

**`AgentWorkflowResultCondition`**

_A branch on which result a nested workflow returned. Only meaningful on a `workflow` step; the referenced step must be a `result` step of the nested workflow that step runs._

- `result` — string **(required)** — Id of the `result` step reached inside the nested workflow. An id rather than a name, so renaming a result from 'failed' to 'gave up' does not unwire every step that handles it. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_

**`AgentWorkflowResultHandler`**

_End this workflow and hand control back to whatever invoked it. In a nested workflow the invoking step resumes and branches on which result was reached (see AgentWorkflowResultCondition). In the main graph of a workflow-channel agent the run finishes and the result is returned to the caller — the agent, automation or API request that started it. In the main graph of a voice / chat / assistant agent there is no invoker, so it behaves as `end`._

- `value` — string — What this result returns to the invoker. Supports handlebars resolved against workflow variables, agent variables and session context (e.g. '{{policy.number}}'). Absent returns the result's id alone, which is enough when the caller only branches on which result was reached. _(minLen=1; maxLen=8000)_

**`AgentWorkflowSettings`**

- `maxTransitions` — number — Give up after this many step transitions, so a cycle whose conditions all keep matching cannot run forever. Absent means no limit, which is the default: a deliberate loop — 'keep asking until you have the postcode' — is a normal shape, and silently capping it would be worse than making the author say so. _(min=1; max=500)_
- `variables` — array — Workflow variables seeded before the first step runs. Agent input variables (`engine.ai.variables`) are already in scope and need no entry here.
  - _array of_ `AgentWorkflowAssignment`
    - `name` — string **(required)** _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
    - `value` — string — Text written to the variable, with handlebars resolved against workflow variables, agent variables and session context (e.g. '{{lookup.status}}'). Empty clears the variable. _(maxLen=4000)_
    - `expression` — any — A JsonLogic expression computing the value instead of rendering it, which is what makes arithmetic possible: `{ "+": [{ "var": "attempts" }, 1] }` is the retry counter a bounded loop needs, written with no model in the loop.
- `layout` — string — How the builder arranges the graph. Authoring metadata: the runtime ignores it. `stages` bands the graph by `stage`, which is what a forty-step workflow needs. _(enum: `flow`, `compact`, `stages`)_

**`AgentWorkflowStep`**

- `id` — string **(required)** — Identifier of a step within its workflow, unique per workflow (the main graph and each nested workflow are separate scopes). Stable and machine-facing: transitions reference it, and a result step's id is the name a caller branches on, so renaming a step's `label` never unwires the graph. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
- `label` — string **(required)** — Human readable name of a step, e.g. 'Transfer to the sales desk'. Shown in the builder and in traces, and read by the model too: when this step is an exit of the live step, the label is the preview offered alongside the exit's condition. Never a routing key — see AgentWorkflowStepId — so renaming one never unwires a graph. _(minLen=1; maxLen=128)_
- `stage` — string — The phase this step belongs to. Inherited by steps downstream, so a handful of tags organise a long graph. _(minLen=1; maxLen=64)_
- `handler` — union **(required)** — What a step does. Exactly one member is set. `action` carries a capability; the others are workflow-only handlers with no capability equivalent.
  - _oneOf_ — exactly one of:
    - **`conversation`**
      - `conversation` — AgentWorkflowConversationHandler **(required)** — A stretch of conversation with a goal: the model talks, may use the capabilities in scope, and the step's transitions are evaluated against what happens. This is the only handler that leaves control where it is until a transition matches — a step whose conditions all stay false simply keeps talking. Deliberately not configurable per step: the model, and how readily the step is left. The model is the agent's (`engine.ai.model`) because a session that swaps models mid-conversation swaps voice, latency and tool-calling behaviour with it. How readily a step is left is decided by how its transitions are worded — conditions describing what the *caller* has done keep a model on the step, and no eagerness dial moves that number.
        - `goal` — string **(required)** — What the agent is trying to achieve here, appended to the agent's `engine.ai.instructions`. Never a replacement for them: identity, tone and standing rules hold across every step, and a step that needs different ones is a different agent. _(minLen=1; maxLen=10000)_
        - `entry` — string — How a conversation step starts. _(enum: `auto`, `speak_first`, `listen_first`)_
        - `channels` — AgentWorkflowConversationChannelsSettings — Per-channel settings of a conversation step. Only voice has anything to say about a stretch of conversation today; the chat and assistant surfaces deliver it as they deliver every other reply.
          - _(nesting depth limit — see `AgentWorkflowConversationChannelsSettings` in the Schemas appendix)_
        - `capabilities` — array — Capabilities offered to the model *in addition* to `engine.ai.capabilities` while this step runs, configured exactly as they are there — the same union, the same structures. Use it to give a step reach it should not have everywhere: authoring the refund tool on the refund step, rather than on the agent, is also what keeps it out of every other step. Additive only, by design. A step cannot drop an agent-level capability, so it cannot strand a session by taking away the `handover` or `transfer` its channel needs, and the runtime keeps one rule for the turn's tool set. Skills the model loads (`engine.ai.skills`) and the channel's own built-ins join it either way.
          - _(nesting depth limit — see `AgentCapability` in the Schemas appendix)_
    - **`message`**
      - `message` — AgentWorkflowMessageHandler **(required)** — Say one thing — spoken on voice, posted on chat / assistant — then move on. The line is either authored verbatim or generated at the step; either way the agent says it once and the transitions are evaluated, with no turn handed to the user.
        - `content` — union **(required)** — Where the step's line comes from. Exactly one member is set: `text` is authored, `generate` is written by the model at the step.
          - _(nesting depth limit — see `AgentWorkflowMessageContent` in the Schemas appendix)_
        - `channels` — AgentWorkflowMessageChannelsSettings — Per-channel settings of a message step: how the line is protected when spoken, and what is offered with it when posted.
          - _(nesting depth limit — see `AgentWorkflowMessageChannelsSettings` in the Schemas appendix)_
    - **`action`**
      - `action` — AgentWorkflowActionHandler **(required)** — A step that performs one capability. The runtime performs it on arrival — no model decision about *whether* to act, and no tool offered to the model for it. Which is the point: an action the graph reached is an action that happens, at the cost of nothing.
        - `capability` — union **(required)** — The capability a step performs, run by the runtime rather than chosen by the model. A subset of AgentCapability, reusing its structures verbatim: these are the members that describe a single action with a beginning and an end. The rest of AgentCapability (`kb`, `webSearch`, `webFetch`, `sandbox`, `suggestions`) describes reach the model draws on while it talks, so it belongs on a conversation step's `capabilities` rather than on a step of its own. Configuration comes from the capability itself and nothing is added here: a tool step's fixed arguments are `AgentTool.fields` predefined handlers, its spoken lead-in is `AgentTool.startMessage`, a transfer's line before the hand-off is `AgentTransferPipeline.instructions`, an invoked agent's inputs are `AgentCallCapability.variables`. Anything left unpinned is filled by the model at the step, per the tool's input schema.
          - _(nesting depth limit — see `AgentWorkflowAction` in the Schemas appendix)_
        - `forceToolCall` — boolean — Run the step as one model call with the tool choice pinned to this capability, instead of calling it straight from the runtime. The model still cannot decide *whether* to call it — only what to put in the arguments left unpinned, which is what a lookup keyed on something nobody can template ('the symptom the caller just described') needs. Costs one model call where the default costs none, so it is opt-in. Honoured where the action has arguments a model can write — `tool`, `connector`, `agent`, and a `transfer` whose target the model chooses; ignored elsewhere. Leaving it false while a required argument is unpinned is an authoring error, not a runtime one: nothing would be there to fill it.
        - `output` — string — Workflow variable the action's result is written to, so later `expression` conditions can branch on it and later steps can template it (e.g. capture a lookup into `policy`, then branch on `{ "==": [{ "var": "policy.status" }, "active"] }`). Absent means the result is not captured; the model still sees it in the conversation per the capability's own pipeline. Written on success only. A failed action leaves the variable as it was and takes a `failure` transition instead — see AgentWorkflowFailureCondition — so a graph can never mistake an error for a result. _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
    - **`variables`**
      - `variables` — AgentWorkflowVariablesHandler **(required)** — Write workflow variables. The step nobody asks for until the first time a graph has to remember something between two branches.
        - `assignments` — array **(required)** _(minItems=1; maxItems=50)_
          - _(nesting depth limit — see `AgentWorkflowAssignment` in the Schemas appendix)_
    - **`workflow`**
      - `workflow` — AgentWorkflowInvokeHandler **(required)** — Run a nested workflow and continue once it returns. The unit of decomposition: a twelve-step identity check is called from the front door, from the booking flow and from the complaints line, so it is authored once and referenced by a single step at each call site. The nested workflow shares this session and its variables; it returns through its `result` steps, which is what the calling step's `result` transitions branch on. A nested workflow that instead reaches an `end` or a terminal action does what it says — the session is over and nothing comes back.
        - `workflow` — string **(required)** — The nested workflow to run. Must be declared in `AgentWorkflow.nested`, and must not run itself directly or through a ring of nested workflows. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
        - `output` — string — Workflow variable the nested workflow's result `value` is written to. Absent means the value is discarded — which is the usual case when the branch taken is the whole answer. _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
    - **`result`**
      - `result` — AgentWorkflowResultHandler **(required)** — End this workflow and hand control back to whatever invoked it. In a nested workflow the invoking step resumes and branches on which result was reached (see AgentWorkflowResultCondition). In the main graph of a workflow-channel agent the run finishes and the result is returned to the caller — the agent, automation or API request that started it. In the main graph of a voice / chat / assistant agent there is no invoker, so it behaves as `end`.
        - `value` — string — What this result returns to the invoker. Supports handlebars resolved against workflow variables, agent variables and session context (e.g. '{{policy.number}}'). Absent returns the result's id alone, which is enough when the caller only branches on which result was reached. _(minLen=1; maxLen=8000)_
    - **`end`**
      - `end` — AgentWorkflowEndHandler **(required)** — The session is over. Terminal and configuration-free by design: a closing line is a `message` step in front of it, and releasing a call is the `hangup` action — both already exist, and neither needs restating here.
- `transitions` — array — The ways out of this step. Must be non-empty on every step that stays in the session, since a step the runtime cannot leave is a dead end. On `result` and `end` it must be empty. On the `action` members that leave the session (`handover`, `delegation`, `transfer`, `hangup`) it may carry `failure` transitions and nothing else: an action that was supposed to leave and failed — a busy extension, a service desk with nobody on it — has not left, and a graph with no answer for that drops the caller.
  - _array of_ `AgentWorkflowTransition`
    - `target` — string **(required)** — Step to move to. Must be a step of the same workflow — a nested workflow is entered through a `workflow` step, not by pointing a transition into it. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
    - `condition` — union **(required)** — How the runtime decides to take a transition. Exactly one member is set.
      - _oneOf_ — exactly one of:
        - **`always`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`prompt`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`expression`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`result`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`failure`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`fallback`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
- `position` — AgentWorkflowStepPosition — Canvas coordinates of a step in the builder. Authoring metadata: the runtime ignores it, and a workflow that arrives without positions is laid out automatically.
  - `x` — number **(required)**
  - `y` — number **(required)**

**`AgentWorkflowStepPosition`**

_Canvas coordinates of a step in the builder. Authoring metadata: the runtime ignores it, and a workflow that arrives without positions is laid out automatically._

- `x` — number **(required)**
- `y` — number **(required)**

**`AgentWorkflowTransition`**

_One way out of a step._

- `target` — string **(required)** — Step to move to. Must be a step of the same workflow — a nested workflow is entered through a `workflow` step, not by pointing a transition into it. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
- `condition` — union **(required)** — How the runtime decides to take a transition. Exactly one member is set.
  - _oneOf_ — exactly one of:
    - **`always`**
      - `always` — AgentWorkflowAlwaysCondition **(required)** — Unconditional. Only legal as a step's single transition: two unconditional exits are a coin toss, not a routing decision.
    - **`prompt`**
      - `prompt` — AgentWorkflowPromptCondition **(required)** — A condition the model judges against the conversation, e.g. 'the caller has said they will try the fix'. Phrase it as something the **caller** has done. A condition describing what the *agent* has done — 'the caller has a next step to try' — is true the instant the agent names one, so the model leaves before the caller has answered, and one early exit cascades through the rest of the graph. Rewording the same exits from agent actions to caller actions, changing nothing else, moved three models from 58–64 % of turns on the right step to 96–100 %, and removed every stray move. It is the single largest effect measured on this contract, so an authoring surface that accepts an agent-action condition is the defect, not the wording.
        - `instructions` — string **(required)** _(minLen=1; maxLen=2000)_
    - **`expression`**
      - `expression` — AgentWorkflowExpressionCondition **(required)** — A branch taken when workflow state satisfies the condition — no model judgement involved, which is what makes it the right condition after an `action` or `variables` step.
        - `conditions` — any **(required)** — A JsonLogic condition tree evaluated against workflow state, e.g. `{ "==": [ { "var": "lookup.status" }, "found" ] }`. The `var` namespace is the workflow variables written by `variables` steps and action `output` captures, the agent's input variables (`engine.ai.variables`), and the session context. An empty tree always matches. This is a separate language from the rule-tree AutomationConditions (wilma-workflows) and CopilotConditions (wilma-copilot).
    - **`result`**
      - `result` — AgentWorkflowResultCondition **(required)** — A branch on which result a nested workflow returned. Only meaningful on a `workflow` step; the referenced step must be a `result` step of the nested workflow that step runs.
        - `result` — string **(required)** — Id of the `result` step reached inside the nested workflow. An id rather than a name, so renaming a result from 'failed' to 'gave up' does not unwire every step that handles it. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
    - **`failure`**
      - `failure` — AgentWorkflowFailureCondition **(required)** — A branch taken when the step's action fails. Only meaningful on an `action` step, and the only condition a terminal action may carry: a transfer that finds the extension busy has not left the session, so a graph that cannot say what happens next simply drops the caller. Failure short-circuits — when an action fails, only `failure` transitions are considered, never the `expression` or `prompt` branches that were written for its result. If none matches, the session fails with the action's error, so a step whose capability can fail wants a catch-all last in the list.
        - `kinds` — array — Kinds this branch handles, evaluated as a set. Absent or empty catches **any** failure — the catch-all, which the list order must therefore place after the specific branches.
          - _(nesting depth limit — see `AgentWorkflowFailureKind` in the Schemas appendix)_
    - **`fallback`**
      - `fallback` — AgentWorkflowFallbackCondition **(required)** — The else-branch, taken when no sibling matched. At most one per step, and reached last regardless of where it sits in the list.

**`AgentWorkflowVariablesHandler`**

_Write workflow variables. The step nobody asks for until the first time a graph has to remember something between two branches._

- `assignments` — array **(required)** _(minItems=1; maxItems=50)_
  - _array of_ `AgentWorkflowAssignment`
    - `name` — string **(required)** _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
    - `value` — string — Text written to the variable, with handlebars resolved against workflow variables, agent variables and session context (e.g. '{{lookup.status}}'). Empty clears the variable. _(maxLen=4000)_
    - `expression` — any — A JsonLogic expression computing the value instead of rendering it, which is what makes arithmetic possible: `{ "+": [{ "var": "attempts" }, 1] }` is the retry counter a bounded loop needs, written with no model in the loop.

**`AssistantAudioSettings`**

_Switchable audio for the assistant channel. The settings object keeps enablement beside its speech policy, matching the voice channel's switchable blocks so a disabled configuration can be retained without serving audio._

- `enabled` — boolean **(required)** — Whether the assistant accepts audio calls. Required so the presence of saved speech configuration is never mistaken for enablement.
- `speech` — AssistantSpeechSettings — Recognition and synthesis policy for assistant audio. This is assistant-owned rather than a VoiceSpeechSettings reuse so telephony and assistant audio can evolve independently. It has no language greeting and no greet-every-language switch because an assistant conversation is already open when its audio call starts, leaving nothing for the channel to greet.
  - `languages` — array **(required)** — Languages the assistant audio channel can recognise and speak. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once — unlike the voice channel, where a caller opts into identification with `autoDetect`, THIS channel derives identification from `languages` and turns it on whenever the recogniser can identify among more than one, so every one of the up to ten rows here can become a live candidate list. The service does not clamp that list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five); a caller configuring more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. _(minItems=1; maxItems=10)_
    - _array of_ `AssistantLanguage`
      - `code` — string **(required)** — BCP-47 code with locale, e.g. 'en-US', 'it-IT'. Reuses the channel-neutral language value so assistant and voice configuration accept the same codes without sharing policy structures. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `voice` — string **(required)** — Voice this language speaks with. Reuses the channel-neutral URI value so providers and synthesis parameters have the same representation in every channel. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
      - `isDefault` — boolean — Marks the language used when the caller's language matches nothing configured. THE FULL RESOLUTION ORDER, because a client author reading only this contract cannot otherwise find it: an exact match on the call's language, then a match on its primary subtag (`fr` finds `fr-FR`), then the language marked here, then a language whose primary subtag is `en`, then the first entry in the list. The same order the voice channel resolves by — the rule belongs to choosing a language, not to a channel. At most one language may carry it. A record with two — reachable through the API, where no form prevents it — resolves to the first marked one in list order: refusing an already-open assistant conversation over configuration drift is worse than serving it.
      - `pronunciations` — array — The rules this language is spoken with, same shape and same per-language ownership as VoiceLanguage.pronunciations — a respelling is about how a synthesized reply SOUNDS, not about how a conversation starts, so the rationale that leaves `greeting` off this structure does not apply here. Absent means no respellings for this language, distinct from the voice channel's OWN configured rules for the same language: an agent's assistant audio does not inherit them, so a name gets fixed once and read once, on whichever channel it is saved. _(maxItems=200)_
        - _(nesting depth limit — see `VoicePronunciation` in the Schemas appendix)_
  - `transcription` — AssistantTranscriptionSettings — Speech-to-text configuration owned by the assistant channel, so changes to assistant recognition policy cannot alter telephony calls. NO `autoDetect` HERE, unlike the voice channel: on this channel configuring a second language IS the request to recognise which one is being spoken — nobody lists two and then asks to be heard in only one — so the server derives identification from the language list and clamps it to false when the recogniser cannot identify among them, or there are too few to identify. The voice channel keeps the switch because a dialplan can hand a call its language, which is a choice an assistant conversation never has to make.
    - `engine` — string — Recogniser used for assistant audio. Absent resolves to the platform default, resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_

**`AssistantChannelSettings`**

_Assistant channel settings. Presence enables the in-app assistant surface; audio remains unavailable unless its separate settings are present and enabled._

- `default` — boolean — Offer this agent as the default assistant for users covered by the agent access settings.
- `ui` — AssistantUiSettings — How the agent presents itself in the assistant UI: what the user reads before typing anything, and what they can start from without typing at all. Everything here is presentation — it never changes what the agent can do.
  - `welcome` — AssistantWelcomeSettings — Greeting shown on an empty thread, above the quick commands.
    - `title` — string — Heading, e.g. 'How can I help?'. Rendered on one line. _(minLen=1; maxLen=80)_
    - `subtitle` — string — Line under the heading, saying what this agent is for, e.g. 'Ask about your conversations, accounts and calls.'. _(minLen=1; maxLen=200)_
  - `commands` — array — Cards offered under the welcome message on an empty thread, in the order given. Empty or omitted shows no cards. _(maxItems=8)_
    - _array of_ `AssistantQuickCommand`
      - `title` — string **(required)** — Card label, e.g. 'Summarize my day'. Rendered on one line and truncated when it does not fit. _(minLen=1; maxLen=60)_
      - `description` — string — Optional line under the label. Also one line, so keep it to a short clarification of what the command does. _(minLen=1; maxLen=120)_
      - `prompt` — string **(required)** — The message actually sent when the card is picked. Usually longer and more explicit than the label, since it is what the model reads. _(minLen=1; maxLen=2000)_
  - `placeholder` — string — Placeholder text in the composer, e.g. 'Ask about an account…'. Defaults to the client's own placeholder when omitted. _(minLen=1; maxLen=100)_
- `audio` — AssistantAudioSettings — Switchable audio for the assistant channel. The settings object keeps enablement beside its speech policy, matching the voice channel's switchable blocks so a disabled configuration can be retained without serving audio.
  - `enabled` — boolean **(required)** — Whether the assistant accepts audio calls. Required so the presence of saved speech configuration is never mistaken for enablement.
  - `speech` — AssistantSpeechSettings — Recognition and synthesis policy for assistant audio. This is assistant-owned rather than a VoiceSpeechSettings reuse so telephony and assistant audio can evolve independently. It has no language greeting and no greet-every-language switch because an assistant conversation is already open when its audio call starts, leaving nothing for the channel to greet.
    - `languages` — array **(required)** — Languages the assistant audio channel can recognise and speak. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once — unlike the voice channel, where a caller opts into identification with `autoDetect`, THIS channel derives identification from `languages` and turns it on whenever the recogniser can identify among more than one, so every one of the up to ten rows here can become a live candidate list. The service does not clamp that list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five); a caller configuring more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. _(minItems=1; maxItems=10)_
      - _array of_ `AssistantLanguage`
        - _(nesting depth limit — see `AssistantLanguage` in the Schemas appendix)_
    - `transcription` — AssistantTranscriptionSettings — Speech-to-text configuration owned by the assistant channel, so changes to assistant recognition policy cannot alter telephony calls. NO `autoDetect` HERE, unlike the voice channel: on this channel configuring a second language IS the request to recognise which one is being spoken — nobody lists two and then asks to be heard in only one — so the server derives identification from the language list and clamps it to false when the recogniser cannot identify among them, or there are too few to identify. The voice channel keeps the switch because a dialplan can hand a call its language, which is a choice an assistant conversation never has to make.
      - `engine` — string — Recogniser used for assistant audio. Absent resolves to the platform default, resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_

**`AssistantLanguage`**

_One language the assistant audio channel can recognise and speak. There is deliberately no greeting here: an assistant conversation is already open when its audio call starts, so there is no new conversation to welcome and no initial phrase for the runtime to choose or repeat._

- `code` — string **(required)** — BCP-47 code with locale, e.g. 'en-US', 'it-IT'. Reuses the channel-neutral language value so assistant and voice configuration accept the same codes without sharing policy structures. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `voice` — string **(required)** — Voice this language speaks with. Reuses the channel-neutral URI value so providers and synthesis parameters have the same representation in every channel. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
- `isDefault` — boolean — Marks the language used when the caller's language matches nothing configured. THE FULL RESOLUTION ORDER, because a client author reading only this contract cannot otherwise find it: an exact match on the call's language, then a match on its primary subtag (`fr` finds `fr-FR`), then the language marked here, then a language whose primary subtag is `en`, then the first entry in the list. The same order the voice channel resolves by — the rule belongs to choosing a language, not to a channel. At most one language may carry it. A record with two — reachable through the API, where no form prevents it — resolves to the first marked one in list order: refusing an already-open assistant conversation over configuration drift is worse than serving it.
- `pronunciations` — array — The rules this language is spoken with, same shape and same per-language ownership as VoiceLanguage.pronunciations — a respelling is about how a synthesized reply SOUNDS, not about how a conversation starts, so the rationale that leaves `greeting` off this structure does not apply here. Absent means no respellings for this language, distinct from the voice channel's OWN configured rules for the same language: an agent's assistant audio does not inherit them, so a name gets fixed once and read once, on whichever channel it is saved. _(maxItems=200)_
  - _array of_ `VoicePronunciation`
    - `phrase` — string **(required)** — The phrase as it appears in the text, e.g. 'Wildix'. Bounded because every rule is compiled into ONE regular expression — see the list below. _(maxLen=200)_
    - `as` — string **(required)** — Respelling (ALIAS) or phonetic transcription (IPA), e.g. 'Wil-dix'. _(maxLen=200)_
    - `encoding` — string — How the `as` member of a pronunciation rule is written. _(enum: `alias`, `ipa`)_

**`AssistantQuickCommand`**

_A starter prompt offered as a card on an empty thread. Picking it sends `prompt` as the user's first message, so the user never types it._

- `title` — string **(required)** — Card label, e.g. 'Summarize my day'. Rendered on one line and truncated when it does not fit. _(minLen=1; maxLen=60)_
- `description` — string — Optional line under the label. Also one line, so keep it to a short clarification of what the command does. _(minLen=1; maxLen=120)_
- `prompt` — string **(required)** — The message actually sent when the card is picked. Usually longer and more explicit than the label, since it is what the model reads. _(minLen=1; maxLen=2000)_

**`AssistantSpeechSettings`**

_Recognition and synthesis policy for assistant audio. This is assistant-owned rather than a VoiceSpeechSettings reuse so telephony and assistant audio can evolve independently. It has no language greeting and no greet-every-language switch because an assistant conversation is already open when its audio call starts, leaving nothing for the channel to greet._

- `languages` — array **(required)** — Languages the assistant audio channel can recognise and speak. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once — unlike the voice channel, where a caller opts into identification with `autoDetect`, THIS channel derives identification from `languages` and turns it on whenever the recogniser can identify among more than one, so every one of the up to ten rows here can become a live candidate list. The service does not clamp that list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five); a caller configuring more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. _(minItems=1; maxItems=10)_
  - _array of_ `AssistantLanguage`
    - `code` — string **(required)** — BCP-47 code with locale, e.g. 'en-US', 'it-IT'. Reuses the channel-neutral language value so assistant and voice configuration accept the same codes without sharing policy structures. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - `voice` — string **(required)** — Voice this language speaks with. Reuses the channel-neutral URI value so providers and synthesis parameters have the same representation in every channel. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
    - `isDefault` — boolean — Marks the language used when the caller's language matches nothing configured. THE FULL RESOLUTION ORDER, because a client author reading only this contract cannot otherwise find it: an exact match on the call's language, then a match on its primary subtag (`fr` finds `fr-FR`), then the language marked here, then a language whose primary subtag is `en`, then the first entry in the list. The same order the voice channel resolves by — the rule belongs to choosing a language, not to a channel. At most one language may carry it. A record with two — reachable through the API, where no form prevents it — resolves to the first marked one in list order: refusing an already-open assistant conversation over configuration drift is worse than serving it.
    - `pronunciations` — array — The rules this language is spoken with, same shape and same per-language ownership as VoiceLanguage.pronunciations — a respelling is about how a synthesized reply SOUNDS, not about how a conversation starts, so the rationale that leaves `greeting` off this structure does not apply here. Absent means no respellings for this language, distinct from the voice channel's OWN configured rules for the same language: an agent's assistant audio does not inherit them, so a name gets fixed once and read once, on whichever channel it is saved. _(maxItems=200)_
      - _array of_ `VoicePronunciation`
        - _(nesting depth limit — see `VoicePronunciation` in the Schemas appendix)_
- `transcription` — AssistantTranscriptionSettings — Speech-to-text configuration owned by the assistant channel, so changes to assistant recognition policy cannot alter telephony calls. NO `autoDetect` HERE, unlike the voice channel: on this channel configuring a second language IS the request to recognise which one is being spoken — nobody lists two and then asks to be heard in only one — so the server derives identification from the language list and clamps it to false when the recogniser cannot identify among them, or there are too few to identify. The voice channel keeps the switch because a dialplan can hand a call its language, which is a choice an assistant conversation never has to make.
  - `engine` — string — Recogniser used for assistant audio. Absent resolves to the platform default, resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_

**`AssistantTranscriptionSettings`**

_Speech-to-text configuration owned by the assistant channel, so changes to assistant recognition policy cannot alter telephony calls. NO `autoDetect` HERE, unlike the voice channel: on this channel configuring a second language IS the request to recognise which one is being spoken — nobody lists two and then asks to be heard in only one — so the server derives identification from the language list and clamps it to false when the recogniser cannot identify among them, or there are too few to identify. The voice channel keeps the switch because a dialplan can hand a call its language, which is a choice an assistant conversation never has to make._

- `engine` — string — Recogniser used for assistant audio. Absent resolves to the platform default, resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_

**`AssistantUiSettings`**

_How the agent presents itself in the assistant UI: what the user reads before typing anything, and what they can start from without typing at all. Everything here is presentation — it never changes what the agent can do._

- `welcome` — AssistantWelcomeSettings — Greeting shown on an empty thread, above the quick commands.
  - `title` — string — Heading, e.g. 'How can I help?'. Rendered on one line. _(minLen=1; maxLen=80)_
  - `subtitle` — string — Line under the heading, saying what this agent is for, e.g. 'Ask about your conversations, accounts and calls.'. _(minLen=1; maxLen=200)_
- `commands` — array — Cards offered under the welcome message on an empty thread, in the order given. Empty or omitted shows no cards. _(maxItems=8)_
  - _array of_ `AssistantQuickCommand`
    - `title` — string **(required)** — Card label, e.g. 'Summarize my day'. Rendered on one line and truncated when it does not fit. _(minLen=1; maxLen=60)_
    - `description` — string — Optional line under the label. Also one line, so keep it to a short clarification of what the command does. _(minLen=1; maxLen=120)_
    - `prompt` — string **(required)** — The message actually sent when the card is picked. Usually longer and more explicit than the label, since it is what the model reads. _(minLen=1; maxLen=2000)_
- `placeholder` — string — Placeholder text in the composer, e.g. 'Ask about an account…'. Defaults to the client's own placeholder when omitted. _(minLen=1; maxLen=100)_

**`AssistantVoiceSettings`**

_End-user view of an agent's assistant voice. New end-user voice parameters are added here rather than as AgentInfo members._

- `enabled` — boolean **(required)** — Whether a client should offer a voice call. True only when the definition the agent currently runs has assistant audio enabled and configured (`channels.assistant.audio.enabled` with at least one speech language); audio that is not configured counts as disabled. For a deployment that splits traffic, every routed version must qualify, so the answer holds whichever version a call lands on.

**`AssistantWelcomeSettings`**

_Greeting shown on an empty thread, above the quick commands._

- `title` — string — Heading, e.g. 'How can I help?'. Rendered on one line. _(minLen=1; maxLen=80)_
- `subtitle` — string — Line under the heading, saying what this agent is for, e.g. 'Ask about your conversations, accounts and calls.'. _(minLen=1; maxLen=200)_

**`ChannelType`**

_A channel an agent can serve (see AgentChannels for enablement). Also the runtime channel recorded by the channel runtimes / wilma-traces. A background task has no delivery surface and therefore no channel._

- string _(enum: `voice`, `chat`, `assistant`)_

**`ChatChannelSettings`**

- `discoverable` — boolean — Whether users can find and add this agent to conversations.
- `sessionTimeoutMinutes` — number — Minutes a conversation can stay idle before the next message starts a new session. Omit to start a new session at the end of the agent's local day (`engine.ai.timeZone`). Allowed values: 15, 30, 60, 120. _(min=15; max=120)_
- `verbosity` — string — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_

**`ChatVerbosity`**

_How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text._

- string _(enum: `none`, `simple`, `full`)_

**`CompareAgentVersionsResponseContent`**

- `changes` — array **(required)**
  - _array of_ `AgentVersionChange`
    - `path` — string **(required)** — JSON pointer of the changed field within the agent definition, e.g. '/engine/ai/instructions'.
    - `before` — any — Value before the change (absent when the field was added).
    - `after` — any — Value after the change (absent when the field was removed).

**`ConflictExceptionResponseContent`**

_The request conflicts with the current state of the resource, e.g. a duplicate name, a resource still in use, or an unmet precondition._

- `message` — string **(required)**

**`CreateAgentApiKeyRequestContent`**

- `name` — string _(minLen=1; maxLen=64)_
- `expiresAt` — string — Optional expiry; the key stops working after this time.

**`CreateAgentApiKeyResponseContent`**

- `key` — AgentApiKey **(required)**
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `name` — string _(minLen=1; maxLen=64)_
  - `prefix` — string **(required)** — Non-secret prefix of the key, e.g. 'sk-a1b2', for display purposes.
  - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
    - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
    - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
    - `name` — string — Human readable name of the actor at the time of the action.
  - `expiresAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `lastUsedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `secret` — string **(required)** — The full secret. Shown only once.

**`CreateAgentRequestContent`**

_The complete, versionable configuration of an agent. This is what gets snapshotted when a version is published._

- `name` — string **(required)** _(minLen=3; maxLen=255)_
- `description` — string _(minLen=1; maxLen=1000)_
- `category` — string — Category of the agent, e.g.: 'Support'. _(minLen=1; maxLen=128)_
- `picture` — string — Avatar URL.
- `channels` — AgentChannels **(required)** — The channels an agent serves and their channel-specific settings. Presence of a member enables that channel. Empty means the agent serves no channel: it is not reachable on its own and runs only as an automation's task or when another agent calls it. Enabled channels are mirrored as ChannelType values on AgentInfo.
  - `voice` — VoiceChannelSettings — Voice channel settings. Note: a voice agent's AgentAccess.grants are ignored — inbound calls are routed by the PBX dialplan and data ACL is the agent-level `settings.pbxGroupId`, not per-user grants.
    - `greeting` — string — Message spoken when the call starts.
    - `backgroundSound` — VoiceBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT like `interruptions` and `endCall`, rather than a loose name on the channel: it is one switchable call behaviour, it reads the same way as its siblings, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
      - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
      - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
    - `speech` — VoiceSpeechSettings — Speech configuration for the voice channel. When present it WINS over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the single exception, because it is the channel's own input signal and the feature has no starting point without it.
      - `languages` — array **(required)** — Configured languages. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once: automatic detection here is opt-in (`transcription.autoDetect`), and once a caller turns it on, the service does not clamp the resulting candidate list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five) — a caller who both opts in and configures more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. With detection off, only the single resolved language is ever sent, so the ceiling never becomes a candidate-list problem at all. _(minItems=1; maxItems=10)_
        - _(nesting depth limit — see `VoiceLanguage` in the Schemas appendix)_
      - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in the voice, provider account and pronunciation rules of its own language, instead of only the language the call resolved to. Languages whose first message is empty, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
      - `transcription` — VoiceTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
        - _(nesting depth limit — see `VoiceTranscriptionSettings` in the Schemas appendix)_
    - `interruptions` — VoiceInterruptionSettings
      - `enabled` — boolean **(required)** — Whether the caller can interrupt the agent while it is speaking.
      - `minWords` — number — Minimum number of caller words that count as an interruption. _(min=1; max=10)_
    - `silenceTimeout` — VoiceSilenceTimeoutSettings
      - `seconds` — number **(required)** — Seconds of caller silence before the action is taken. _(min=1; max=600)_
      - `action` — union **(required)**
        - _(nesting depth limit — see `VoiceTerminateAction` in the Schemas appendix)_
    - `maxDuration` — VoiceMaxDurationSettings
      - `seconds` — number **(required)** — Maximum call duration in seconds before the action is taken. _(min=10; max=14400)_
      - `action` — union **(required)**
        - _(nesting depth limit — see `VoiceTerminateAction` in the Schemas appendix)_
    - `endCall` — VoiceEndCallSettings
      - `enabled` — boolean **(required)**
      - `phrases` — string — Comma-separated phrases that end the call, e.g. 'goodbye,bye'.
    - `callerMetadata` — VoiceCallerMetadataSettings — Caller context injected into the model prompt.
      - `callerName` — boolean — Include the caller name. Defaults to true.
      - `callerNumber` — boolean — Include the caller phone number. Defaults to true.
      - `callerEmail` — boolean — Include the caller email when known. Defaults to false.
      - `callerCompany` — boolean — Include the caller company when known. Defaults to false.
      - `time` — boolean — Include the current time, rendered in the agent's `engine.ai.timeZone`. Defaults to false.
  - `chat` — ChatChannelSettings
    - `discoverable` — boolean — Whether users can find and add this agent to conversations.
    - `sessionTimeoutMinutes` — number — Minutes a conversation can stay idle before the next message starts a new session. Omit to start a new session at the end of the agent's local day (`engine.ai.timeZone`). Allowed values: 15, 30, 60, 120. _(min=15; max=120)_
    - `verbosity` — string — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
  - `assistant` — AssistantChannelSettings — Assistant channel settings. Presence enables the in-app assistant surface; audio remains unavailable unless its separate settings are present and enabled.
    - `default` — boolean — Offer this agent as the default assistant for users covered by the agent access settings.
    - `ui` — AssistantUiSettings — How the agent presents itself in the assistant UI: what the user reads before typing anything, and what they can start from without typing at all. Everything here is presentation — it never changes what the agent can do.
      - `welcome` — AssistantWelcomeSettings — Greeting shown on an empty thread, above the quick commands.
        - _(nesting depth limit — see `AssistantWelcomeSettings` in the Schemas appendix)_
      - `commands` — array — Cards offered under the welcome message on an empty thread, in the order given. Empty or omitted shows no cards. _(maxItems=8)_
        - _(nesting depth limit — see `AssistantQuickCommand` in the Schemas appendix)_
      - `placeholder` — string — Placeholder text in the composer, e.g. 'Ask about an account…'. Defaults to the client's own placeholder when omitted. _(minLen=1; maxLen=100)_
    - `audio` — AssistantAudioSettings — Switchable audio for the assistant channel. The settings object keeps enablement beside its speech policy, matching the voice channel's switchable blocks so a disabled configuration can be retained without serving audio.
      - `enabled` — boolean **(required)** — Whether the assistant accepts audio calls. Required so the presence of saved speech configuration is never mistaken for enablement.
      - `speech` — AssistantSpeechSettings — Recognition and synthesis policy for assistant audio. This is assistant-owned rather than a VoiceSpeechSettings reuse so telephony and assistant audio can evolve independently. It has no language greeting and no greet-every-language switch because an assistant conversation is already open when its audio call starts, leaving nothing for the channel to greet.
        - _(nesting depth limit — see `AssistantSpeechSettings` in the Schemas appendix)_
- `engine` — union **(required)** — How the agent produces replies. `ai` is the managed engine; `webhook` and `sqs` delegate to an external backend.
  - _oneOf_ — exactly one of:
    - **`ai`**
      - `ai` — AgentAiEngine **(required)** — Managed AI engine: the platform runs the model, tools and knowledge lookups.
        - `instructions` — string **(required)** _(minLen=1; maxLen=60000)_
        - `workflow` — AgentWorkflow — The agent's conversation as a graph: which step runs first, what each step does, and on what condition control moves on. Optional on AgentAiEngine — without one the agent is prompt-driven, steered by `instructions` and free to use its capabilities in any order. Versioned with the rest of the agent definition: publishing a version snapshots the graph, and a draft edit reaches no session until it is published and routed.
          - _(nesting depth limit — see `AgentWorkflow` in the Schemas appendix)_
        - `guardrails` — AgentGuardrails — Turn screening, by side. Only `input` exists: it guards what reaches the model, and output screening is a separate policy with different actions, added here when it is built.
          - _(nesting depth limit — see `AgentGuardrails` in the Schemas appendix)_
        - `model` — string — Defaults to the platform default model when omitted. _(pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
        - `timeZone` — string — IANA timezone the agent reasons about time in: it anchors the current date and time given to the model and how times are read from and written to tool arguments and replies. Shared by every channel the agent serves. Defaults to 'UTC'. _(minLen=1; maxLen=64)_
        - `artifacts` — boolean — Whether the agent can produce artifacts (wilma-artifacts): files it writes in its sandbox and shares back during a session — a document, a PDF, a spreadsheet, a chart, a multi-page web site, a folder of files. Needs the sandbox capability. An artifact starts private to the user the session runs for, who can share it company-wide from the viewer; on the chat channel the runtime shares each one company-wide as it is created, so the link posted into the conversation opens for every signed-in colleague. Artifacts are company-internal: recipients on external transports (sms / whatsapp) or outside the company cannot open the links, so keep this disabled for customer-facing agents. Defaults to false.
        - `skills` — array — Skills attached to this agent (progressive disclosure). A skill may carry its own tools, which join this agent's toolset while that skill is active.
          - _(nesting depth limit — see `AgentSkillReference` in the Schemas appendix)_
        - `capabilities` — array — Everything the agent can do. When a `workflow` is set these are the capabilities in scope at every step, and a step may add to them or narrow them with its own list of the same shape.
          - _(nesting depth limit — see `AgentCapability` in the Schemas appendix)_
        - `variables` — array
          - _(nesting depth limit — see `AgentVariable` in the Schemas appendix)_
    - **`webhook`**
      - `webhook` — AgentWebhookEngine **(required)** — Bring-your-own backend over HTTPS. The platform POSTs call events to the URL; the backend answers out of band through the channel's command API. The response body is not read.
        - `url` — string **(required)**
        - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
          - _(nesting depth limit — see `SecretRef` in the Schemas appendix)_
        - `timeout` — number — Timeout of one delivery, in milliseconds. _(default=10000; min=5000; max=120000)_
    - **`sqs`**
      - `sqs` — AgentSqsEngine **(required)** — Bring-your-own backend over SQS. The platform sends call events to the queue; the backend answers out of band through the channel's command API.
        - `url` — string **(required)**
        - `key` — string **(required)**
        - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
          - _(nesting depth limit — see `SecretRef` in the Schemas appendix)_
- `settings` — AgentSettings — Agent-level settings shared across all channels.
  - `pbxGroupId` — string — PBX group used for data ACL (e.g. Sales Intelligence lookups).
- `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
  - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
  - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
    - _array of_ `AgentGrantPrincipal`
      - _oneOf_ — exactly one of:
        - **`userId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`groupId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`department`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_

**`CreateAgentResponseContent`**

- `agent` — Agent **(required)** — The complete, versionable configuration of an agent. This is what gets snapshotted when a version is published.
  - `name` — string **(required)** _(minLen=3; maxLen=255)_
  - `description` — string _(minLen=1; maxLen=1000)_
  - `category` — string — Category of the agent, e.g.: 'Support'. _(minLen=1; maxLen=128)_
  - `picture` — string — Avatar URL.
  - `channels` — AgentChannels **(required)** — The channels an agent serves and their channel-specific settings. Presence of a member enables that channel. Empty means the agent serves no channel: it is not reachable on its own and runs only as an automation's task or when another agent calls it. Enabled channels are mirrored as ChannelType values on AgentInfo.
    - `voice` — VoiceChannelSettings — Voice channel settings. Note: a voice agent's AgentAccess.grants are ignored — inbound calls are routed by the PBX dialplan and data ACL is the agent-level `settings.pbxGroupId`, not per-user grants.
      - `greeting` — string — Message spoken when the call starts.
      - `backgroundSound` — VoiceBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT like `interruptions` and `endCall`, rather than a loose name on the channel: it is one switchable call behaviour, it reads the same way as its siblings, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
        - _(nesting depth limit — see `VoiceBackgroundSoundSettings` in the Schemas appendix)_
      - `speech` — VoiceSpeechSettings — Speech configuration for the voice channel. When present it WINS over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the single exception, because it is the channel's own input signal and the feature has no starting point without it.
        - _(nesting depth limit — see `VoiceSpeechSettings` in the Schemas appendix)_
      - `interruptions` — VoiceInterruptionSettings
        - _(nesting depth limit — see `VoiceInterruptionSettings` in the Schemas appendix)_
      - `silenceTimeout` — VoiceSilenceTimeoutSettings
        - _(nesting depth limit — see `VoiceSilenceTimeoutSettings` in the Schemas appendix)_
      - `maxDuration` — VoiceMaxDurationSettings
        - _(nesting depth limit — see `VoiceMaxDurationSettings` in the Schemas appendix)_
      - `endCall` — VoiceEndCallSettings
        - _(nesting depth limit — see `VoiceEndCallSettings` in the Schemas appendix)_
      - `callerMetadata` — VoiceCallerMetadataSettings — Caller context injected into the model prompt.
        - _(nesting depth limit — see `VoiceCallerMetadataSettings` in the Schemas appendix)_
    - `chat` — ChatChannelSettings
      - `discoverable` — boolean — Whether users can find and add this agent to conversations.
      - `sessionTimeoutMinutes` — number — Minutes a conversation can stay idle before the next message starts a new session. Omit to start a new session at the end of the agent's local day (`engine.ai.timeZone`). Allowed values: 15, 30, 60, 120. _(min=15; max=120)_
      - `verbosity` — string — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
    - `assistant` — AssistantChannelSettings — Assistant channel settings. Presence enables the in-app assistant surface; audio remains unavailable unless its separate settings are present and enabled.
      - `default` — boolean — Offer this agent as the default assistant for users covered by the agent access settings.
      - `ui` — AssistantUiSettings — How the agent presents itself in the assistant UI: what the user reads before typing anything, and what they can start from without typing at all. Everything here is presentation — it never changes what the agent can do.
        - _(nesting depth limit — see `AssistantUiSettings` in the Schemas appendix)_
      - `audio` — AssistantAudioSettings — Switchable audio for the assistant channel. The settings object keeps enablement beside its speech policy, matching the voice channel's switchable blocks so a disabled configuration can be retained without serving audio.
        - _(nesting depth limit — see `AssistantAudioSettings` in the Schemas appendix)_
  - `engine` — union **(required)** — How the agent produces replies. `ai` is the managed engine; `webhook` and `sqs` delegate to an external backend.
    - _oneOf_ — exactly one of:
      - **`ai`**
        - `ai` — AgentAiEngine **(required)** — Managed AI engine: the platform runs the model, tools and knowledge lookups.
          - _(nesting depth limit — see `AgentAiEngine` in the Schemas appendix)_
      - **`webhook`**
        - `webhook` — AgentWebhookEngine **(required)** — Bring-your-own backend over HTTPS. The platform POSTs call events to the URL; the backend answers out of band through the channel's command API. The response body is not read.
          - _(nesting depth limit — see `AgentWebhookEngine` in the Schemas appendix)_
      - **`sqs`**
        - `sqs` — AgentSqsEngine **(required)** — Bring-your-own backend over SQS. The platform sends call events to the queue; the backend answers out of band through the channel's command API.
          - _(nesting depth limit — see `AgentSqsEngine` in the Schemas appendix)_
  - `settings` — AgentSettings — Agent-level settings shared across all channels.
    - `pbxGroupId` — string — PBX group used for data ACL (e.g. Sales Intelligence lookups).
  - `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
    - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
    - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
      - _array of_ `AgentGrantPrincipal`
        - _(nesting depth limit — see `AgentGrantPrincipal` in the Schemas appendix)_
  - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
    - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
    - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
    - `name` — string — Human readable name of the actor at the time of the action.
  - `updatedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `updatedBy` — Actor — Who performed an action: an interactive user, an API key or an internal service.
    - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
    - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
    - `name` — string — Human readable name of the actor at the time of the action.
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `status` — string **(required)** _(enum: `draft`, `active`)_
  - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
  - `latestVersion` — number — Latest published version number; absent while the agent is still a draft. _(min=1)_
  - `draftBaseVersion` — number — Published version number from which the current draft originated. Absent before the first version is published. _(min=1)_
  - `deployment` — array — How new sessions are split across published versions. Absent while the agent is still a draft. _(minItems=1; maxItems=10)_
    - _array of_ `AgentDeploymentRoute`
      - `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
      - `percentage` — number **(required)** — Percentage of new sessions routed to this version. Percentages must sum to 100. _(min=1; max=100)_

**`GetAgentDeploymentResponseContent`**

- `deployment` — array — Absent while the agent has no published version serving traffic. _(minItems=1; maxItems=10)_
  - _array of_ `AgentDeploymentRoute`
    - `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
    - `percentage` — number **(required)** — Percentage of new sessions routed to this version. Percentages must sum to 100. _(min=1; max=100)_

**`GetAgentResponseContent`**

- `agent` — Agent **(required)** — The complete, versionable configuration of an agent. This is what gets snapshotted when a version is published.
  - `name` — string **(required)** _(minLen=3; maxLen=255)_
  - `description` — string _(minLen=1; maxLen=1000)_
  - `category` — string — Category of the agent, e.g.: 'Support'. _(minLen=1; maxLen=128)_
  - `picture` — string — Avatar URL.
  - `channels` — AgentChannels **(required)** — The channels an agent serves and their channel-specific settings. Presence of a member enables that channel. Empty means the agent serves no channel: it is not reachable on its own and runs only as an automation's task or when another agent calls it. Enabled channels are mirrored as ChannelType values on AgentInfo.
    - `voice` — VoiceChannelSettings — Voice channel settings. Note: a voice agent's AgentAccess.grants are ignored — inbound calls are routed by the PBX dialplan and data ACL is the agent-level `settings.pbxGroupId`, not per-user grants.
      - `greeting` — string — Message spoken when the call starts.
      - `backgroundSound` — VoiceBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT like `interruptions` and `endCall`, rather than a loose name on the channel: it is one switchable call behaviour, it reads the same way as its siblings, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
        - _(nesting depth limit — see `VoiceBackgroundSoundSettings` in the Schemas appendix)_
      - `speech` — VoiceSpeechSettings — Speech configuration for the voice channel. When present it WINS over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the single exception, because it is the channel's own input signal and the feature has no starting point without it.
        - _(nesting depth limit — see `VoiceSpeechSettings` in the Schemas appendix)_
      - `interruptions` — VoiceInterruptionSettings
        - _(nesting depth limit — see `VoiceInterruptionSettings` in the Schemas appendix)_
      - `silenceTimeout` — VoiceSilenceTimeoutSettings
        - _(nesting depth limit — see `VoiceSilenceTimeoutSettings` in the Schemas appendix)_
      - `maxDuration` — VoiceMaxDurationSettings
        - _(nesting depth limit — see `VoiceMaxDurationSettings` in the Schemas appendix)_
      - `endCall` — VoiceEndCallSettings
        - _(nesting depth limit — see `VoiceEndCallSettings` in the Schemas appendix)_
      - `callerMetadata` — VoiceCallerMetadataSettings — Caller context injected into the model prompt.
        - _(nesting depth limit — see `VoiceCallerMetadataSettings` in the Schemas appendix)_
    - `chat` — ChatChannelSettings
      - `discoverable` — boolean — Whether users can find and add this agent to conversations.
      - `sessionTimeoutMinutes` — number — Minutes a conversation can stay idle before the next message starts a new session. Omit to start a new session at the end of the agent's local day (`engine.ai.timeZone`). Allowed values: 15, 30, 60, 120. _(min=15; max=120)_
      - `verbosity` — string — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
    - `assistant` — AssistantChannelSettings — Assistant channel settings. Presence enables the in-app assistant surface; audio remains unavailable unless its separate settings are present and enabled.
      - `default` — boolean — Offer this agent as the default assistant for users covered by the agent access settings.
      - `ui` — AssistantUiSettings — How the agent presents itself in the assistant UI: what the user reads before typing anything, and what they can start from without typing at all. Everything here is presentation — it never changes what the agent can do.
        - _(nesting depth limit — see `AssistantUiSettings` in the Schemas appendix)_
      - `audio` — AssistantAudioSettings — Switchable audio for the assistant channel. The settings object keeps enablement beside its speech policy, matching the voice channel's switchable blocks so a disabled configuration can be retained without serving audio.
        - _(nesting depth limit — see `AssistantAudioSettings` in the Schemas appendix)_
  - `engine` — union **(required)** — How the agent produces replies. `ai` is the managed engine; `webhook` and `sqs` delegate to an external backend.
    - _oneOf_ — exactly one of:
      - **`ai`**
        - `ai` — AgentAiEngine **(required)** — Managed AI engine: the platform runs the model, tools and knowledge lookups.
          - _(nesting depth limit — see `AgentAiEngine` in the Schemas appendix)_
      - **`webhook`**
        - `webhook` — AgentWebhookEngine **(required)** — Bring-your-own backend over HTTPS. The platform POSTs call events to the URL; the backend answers out of band through the channel's command API. The response body is not read.
          - _(nesting depth limit — see `AgentWebhookEngine` in the Schemas appendix)_
      - **`sqs`**
        - `sqs` — AgentSqsEngine **(required)** — Bring-your-own backend over SQS. The platform sends call events to the queue; the backend answers out of band through the channel's command API.
          - _(nesting depth limit — see `AgentSqsEngine` in the Schemas appendix)_
  - `settings` — AgentSettings — Agent-level settings shared across all channels.
    - `pbxGroupId` — string — PBX group used for data ACL (e.g. Sales Intelligence lookups).
  - `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
    - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
    - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
      - _array of_ `AgentGrantPrincipal`
        - _(nesting depth limit — see `AgentGrantPrincipal` in the Schemas appendix)_
  - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
    - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
    - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
    - `name` — string — Human readable name of the actor at the time of the action.
  - `updatedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `updatedBy` — Actor — Who performed an action: an interactive user, an API key or an internal service.
    - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
    - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
    - `name` — string — Human readable name of the actor at the time of the action.
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `status` — string **(required)** _(enum: `draft`, `active`)_
  - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
  - `latestVersion` — number — Latest published version number; absent while the agent is still a draft. _(min=1)_
  - `draftBaseVersion` — number — Published version number from which the current draft originated. Absent before the first version is published. _(min=1)_
  - `deployment` — array — How new sessions are split across published versions. Absent while the agent is still a draft. _(minItems=1; maxItems=10)_
    - _array of_ `AgentDeploymentRoute`
      - `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
      - `percentage` — number **(required)** — Percentage of new sessions routed to this version. Percentages must sum to 100. _(min=1; max=100)_

**`GetAgentVersionResponseContent`**

- `version` — AgentVersion **(required)**
  - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
  - `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
  - `basedOnVersion` — number — Published version from which the draft originated. Absent for the first version of a new agent. _(min=1)_
  - `name` — string — Optional human-readable name supplied at publish time. _(minLen=1; maxLen=255)_
  - `changelog` — string — What changed in this version, provided at publish time. _(minLen=1; maxLen=500)_
  - `definition` — AgentDefinitionSnapshot **(required)** — The complete, versionable configuration of an agent. This is what gets snapshotted when a version is published.
    - `name` — string **(required)** _(minLen=3; maxLen=255)_
    - `description` — string _(minLen=1; maxLen=1000)_
    - `category` — string — Category of the agent, e.g.: 'Support'. _(minLen=1; maxLen=128)_
    - `picture` — string — Avatar URL.
    - `channels` — AgentChannels **(required)** — The channels an agent serves and their channel-specific settings. Presence of a member enables that channel. Empty means the agent serves no channel: it is not reachable on its own and runs only as an automation's task or when another agent calls it. Enabled channels are mirrored as ChannelType values on AgentInfo.
      - `voice` — VoiceChannelSettings — Voice channel settings. Note: a voice agent's AgentAccess.grants are ignored — inbound calls are routed by the PBX dialplan and data ACL is the agent-level `settings.pbxGroupId`, not per-user grants.
        - _(nesting depth limit — see `VoiceChannelSettings` in the Schemas appendix)_
      - `chat` — ChatChannelSettings
        - _(nesting depth limit — see `ChatChannelSettings` in the Schemas appendix)_
      - `assistant` — AssistantChannelSettings — Assistant channel settings. Presence enables the in-app assistant surface; audio remains unavailable unless its separate settings are present and enabled.
        - _(nesting depth limit — see `AssistantChannelSettings` in the Schemas appendix)_
    - `engine` — union **(required)** — How the agent produces replies. `ai` is the managed engine; `webhook` and `sqs` delegate to an external backend.
      - _oneOf_ — exactly one of:
        - **`ai`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`webhook`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sqs`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `settings` — AgentSettings — Agent-level settings shared across all channels.
      - `pbxGroupId` — string — PBX group used for data ACL (e.g. Sales Intelligence lookups).
    - `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
      - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
      - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
        - _(nesting depth limit — see `AgentGrantPrincipal` in the Schemas appendix)_
  - `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
    - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
    - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
    - `name` — string — Human readable name of the actor at the time of the action.

**`KnowledgeBaseSearchStrategy`**

_Search algorithm used to retrieve passages._

- string _(enum: `bm25`, `vector`, `hybrid`)_

**`KnowledgeBaseSearchThreshold`**

_Minimum similarity a passage needs to be returned. Raising it trades recall for precision._

- string _(enum: `low`, `medium`, `high`)_

**`ListAgentApiKeysResponseContent`**

- `keys` — array **(required)**
  - _array of_ `AgentApiKey`
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `name` — string _(minLen=1; maxLen=64)_
    - `prefix` — string **(required)** — Non-secret prefix of the key, e.g. 'sk-a1b2', for display purposes.
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
    - `expiresAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `lastUsedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.

**`ListAgentVersionsResponseContent`**

- `versions` — array **(required)**
  - _array of_ `AgentVersionInfo`
    - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
    - `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
    - `basedOnVersion` — number — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
    - `name` — string _(minLen=1; maxLen=255)_
    - `changelog` — string — Human-readable description of what changed in a published version. _(minLen=1; maxLen=500)_
    - `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
- `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_

**`ListAgentsNamesResponseContent`**

- `agents` — array **(required)**
  - _array of_ `AgentInfo`
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `name` — string **(required)** _(minLen=3; maxLen=255)_
    - `picture` — string — Avatar URL, from the agent definition.
    - `category` — string _(minLen=1; maxLen=128)_
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `channels` — array **(required)** — The channels this agent serves (voice / chat / assistant). Empty for an agent that serves none — one only an automation runs or another agent calls.
      - _array of_ `ChannelType`
    - `speechConfigured` — boolean — Whether the voice channel has at least one configured speech language. A dialplan form partitions its application lists on this, so the answer has to travel with the list rather than cost one lookup per entry — it is the reason this member exists and the reason removing it broke that form. Absent is read as false.
    - `engine` — string — Which member of AgentEngine an agent carries, without the engine's configuration. _(enum: `ai`, `webhook`, `sqs`)_
    - `assistantVoice` — AssistantVoiceSettings — End-user view of an agent's assistant voice. New end-user voice parameters are added here rather than as AgentInfo members.
      - `enabled` — boolean **(required)** — Whether a client should offer a voice call. True only when the definition the agent currently runs has assistant audio enabled and configured (`channels.assistant.audio.enabled` with at least one speech language); audio that is not configured counts as disabled. For a deployment that splits traffic, every routed version must qualify, so the answer holds whichever version a call lands on.
    - `skillIds` — array — Ids of the skills attached to this agent. Always active in this agent's sessions; user skill preferences cannot disable them.
      - _array of_ `string`
    - `connectorIds` — array — Ids of the connector instances attached to this agent, in capability order — the order an administrator sees on the agent's capabilities page. This is how a client knows which of the connectors in the assistant's settings catalogue this agent can call: filter that catalogue by these ids.
      - _array of_ `string`
    - `assistant` — AssistantUiSettings — How the agent presents itself in the assistant UI: what the user reads before typing anything, and what they can start from without typing at all. Everything here is presentation — it never changes what the agent can do.
      - `welcome` — AssistantWelcomeSettings — Greeting shown on an empty thread, above the quick commands.
        - _(nesting depth limit — see `AssistantWelcomeSettings` in the Schemas appendix)_
      - `commands` — array — Cards offered under the welcome message on an empty thread, in the order given. Empty or omitted shows no cards. _(maxItems=8)_
        - _(nesting depth limit — see `AssistantQuickCommand` in the Schemas appendix)_
      - `placeholder` — string — Placeholder text in the composer, e.g. 'Ask about an account…'. Defaults to the client's own placeholder when omitted. _(minLen=1; maxLen=100)_
    - `latestVersion` — number — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_

**`ListAgentsResponseContent`**

- `agents` — array **(required)**
  - _array of_ `Agent`
    - `name` — string **(required)** _(minLen=3; maxLen=255)_
    - `description` — string _(minLen=1; maxLen=1000)_
    - `category` — string — Category of the agent, e.g.: 'Support'. _(minLen=1; maxLen=128)_
    - `picture` — string — Avatar URL.
    - `channels` — AgentChannels **(required)** — The channels an agent serves and their channel-specific settings. Presence of a member enables that channel. Empty means the agent serves no channel: it is not reachable on its own and runs only as an automation's task or when another agent calls it. Enabled channels are mirrored as ChannelType values on AgentInfo.
      - `voice` — VoiceChannelSettings — Voice channel settings. Note: a voice agent's AgentAccess.grants are ignored — inbound calls are routed by the PBX dialplan and data ACL is the agent-level `settings.pbxGroupId`, not per-user grants.
        - _(nesting depth limit — see `VoiceChannelSettings` in the Schemas appendix)_
      - `chat` — ChatChannelSettings
        - _(nesting depth limit — see `ChatChannelSettings` in the Schemas appendix)_
      - `assistant` — AssistantChannelSettings — Assistant channel settings. Presence enables the in-app assistant surface; audio remains unavailable unless its separate settings are present and enabled.
        - _(nesting depth limit — see `AssistantChannelSettings` in the Schemas appendix)_
    - `engine` — union **(required)** — How the agent produces replies. `ai` is the managed engine; `webhook` and `sqs` delegate to an external backend.
      - _oneOf_ — exactly one of:
        - **`ai`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`webhook`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sqs`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `settings` — AgentSettings — Agent-level settings shared across all channels.
      - `pbxGroupId` — string — PBX group used for data ACL (e.g. Sales Intelligence lookups).
    - `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
      - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
      - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
        - _(nesting depth limit — see `AgentGrantPrincipal` in the Schemas appendix)_
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
    - `updatedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `updatedBy` — Actor — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
    - `latestVersion` — number — Latest published version number; absent while the agent is still a draft. _(min=1)_
    - `draftBaseVersion` — number — Published version number from which the current draft originated. Absent before the first version is published. _(min=1)_
    - `deployment` — array — How new sessions are split across published versions. Absent while the agent is still a draft. _(minItems=1; maxItems=10)_
      - _array of_ `AgentDeploymentRoute`
        - _(nesting depth limit — see `AgentDeploymentRoute` in the Schemas appendix)_
- `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_

**`NotFoundExceptionResponseContent`**

- `message` — string **(required)** _(default=Not found)_

**`PublishAgentVersionRequestContent`**

- `changelog` — string — What changed in this version. _(minLen=1; maxLen=500)_
- `name` — string — Optional human-readable name for this version. _(minLen=1; maxLen=255)_
- `revision` — number **(required)** — Draft revision this publish is based on (optimistic locking).

**`PublishAgentVersionResponseContent`**

- `version` — AgentVersion **(required)**
  - `agentId` — string **(required)** _(minLen=12; maxLen=12)_
  - `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
  - `basedOnVersion` — number — Published version from which the draft originated. Absent for the first version of a new agent. _(min=1)_
  - `name` — string — Optional human-readable name supplied at publish time. _(minLen=1; maxLen=255)_
  - `changelog` — string — What changed in this version, provided at publish time. _(minLen=1; maxLen=500)_
  - `definition` — AgentDefinitionSnapshot **(required)** — The complete, versionable configuration of an agent. This is what gets snapshotted when a version is published.
    - `name` — string **(required)** _(minLen=3; maxLen=255)_
    - `description` — string _(minLen=1; maxLen=1000)_
    - `category` — string — Category of the agent, e.g.: 'Support'. _(minLen=1; maxLen=128)_
    - `picture` — string — Avatar URL.
    - `channels` — AgentChannels **(required)** — The channels an agent serves and their channel-specific settings. Presence of a member enables that channel. Empty means the agent serves no channel: it is not reachable on its own and runs only as an automation's task or when another agent calls it. Enabled channels are mirrored as ChannelType values on AgentInfo.
      - `voice` — VoiceChannelSettings — Voice channel settings. Note: a voice agent's AgentAccess.grants are ignored — inbound calls are routed by the PBX dialplan and data ACL is the agent-level `settings.pbxGroupId`, not per-user grants.
        - _(nesting depth limit — see `VoiceChannelSettings` in the Schemas appendix)_
      - `chat` — ChatChannelSettings
        - _(nesting depth limit — see `ChatChannelSettings` in the Schemas appendix)_
      - `assistant` — AssistantChannelSettings — Assistant channel settings. Presence enables the in-app assistant surface; audio remains unavailable unless its separate settings are present and enabled.
        - _(nesting depth limit — see `AssistantChannelSettings` in the Schemas appendix)_
    - `engine` — union **(required)** — How the agent produces replies. `ai` is the managed engine; `webhook` and `sqs` delegate to an external backend.
      - _oneOf_ — exactly one of:
        - **`ai`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`webhook`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sqs`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `settings` — AgentSettings — Agent-level settings shared across all channels.
      - `pbxGroupId` — string — PBX group used for data ACL (e.g. Sales Intelligence lookups).
    - `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
      - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
      - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
        - _(nesting depth limit — see `AgentGrantPrincipal` in the Schemas appendix)_
  - `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
    - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
    - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
    - `name` — string — Human readable name of the actor at the time of the action.

**`PutAgentDeploymentRequestContent`**

- `deployment` — array **(required)** — Weighted routing over distinct published versions. Percentages must sum to 100; a single entry at 100 serves one version to everyone. _(minItems=1; maxItems=10)_
  - _array of_ `AgentDeploymentRoute`
    - `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
    - `percentage` — number **(required)** — Percentage of new sessions routed to this version. Percentages must sum to 100. _(min=1; max=100)_

**`PutAgentDeploymentResponseContent`**

- `deployment` — array **(required)** — Weighted routing over distinct published versions. Percentages must sum to 100; a single entry at 100 serves one version to everyone. _(minItems=1; maxItems=10)_
  - _array of_ `AgentDeploymentRoute`
    - `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
    - `percentage` — number **(required)** — Percentage of new sessions routed to this version. Percentages must sum to 100. _(min=1; max=100)_

**`ResetAgentDeploymentResponseContent`**

- `deployment` — array **(required)** — Weighted routing over distinct published versions. Percentages must sum to 100; a single entry at 100 serves one version to everyone. _(minItems=1; maxItems=10)_
  - _array of_ `AgentDeploymentRoute`
    - `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
    - `percentage` — number **(required)** — Percentage of new sessions routed to this version. Percentages must sum to 100. _(min=1; max=100)_

**`RestoreAgentVersionToDraftRequestContent`**

- `revision` — number **(required)** — Draft revision this restore is based on (optimistic locking).

**`RestoreAgentVersionToDraftResponseContent`**

- `agent` — Agent **(required)** — The complete, versionable configuration of an agent. This is what gets snapshotted when a version is published.
  - `name` — string **(required)** _(minLen=3; maxLen=255)_
  - `description` — string _(minLen=1; maxLen=1000)_
  - `category` — string — Category of the agent, e.g.: 'Support'. _(minLen=1; maxLen=128)_
  - `picture` — string — Avatar URL.
  - `channels` — AgentChannels **(required)** — The channels an agent serves and their channel-specific settings. Presence of a member enables that channel. Empty means the agent serves no channel: it is not reachable on its own and runs only as an automation's task or when another agent calls it. Enabled channels are mirrored as ChannelType values on AgentInfo.
    - `voice` — VoiceChannelSettings — Voice channel settings. Note: a voice agent's AgentAccess.grants are ignored — inbound calls are routed by the PBX dialplan and data ACL is the agent-level `settings.pbxGroupId`, not per-user grants.
      - `greeting` — string — Message spoken when the call starts.
      - `backgroundSound` — VoiceBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT like `interruptions` and `endCall`, rather than a loose name on the channel: it is one switchable call behaviour, it reads the same way as its siblings, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
        - _(nesting depth limit — see `VoiceBackgroundSoundSettings` in the Schemas appendix)_
      - `speech` — VoiceSpeechSettings — Speech configuration for the voice channel. When present it WINS over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the single exception, because it is the channel's own input signal and the feature has no starting point without it.
        - _(nesting depth limit — see `VoiceSpeechSettings` in the Schemas appendix)_
      - `interruptions` — VoiceInterruptionSettings
        - _(nesting depth limit — see `VoiceInterruptionSettings` in the Schemas appendix)_
      - `silenceTimeout` — VoiceSilenceTimeoutSettings
        - _(nesting depth limit — see `VoiceSilenceTimeoutSettings` in the Schemas appendix)_
      - `maxDuration` — VoiceMaxDurationSettings
        - _(nesting depth limit — see `VoiceMaxDurationSettings` in the Schemas appendix)_
      - `endCall` — VoiceEndCallSettings
        - _(nesting depth limit — see `VoiceEndCallSettings` in the Schemas appendix)_
      - `callerMetadata` — VoiceCallerMetadataSettings — Caller context injected into the model prompt.
        - _(nesting depth limit — see `VoiceCallerMetadataSettings` in the Schemas appendix)_
    - `chat` — ChatChannelSettings
      - `discoverable` — boolean — Whether users can find and add this agent to conversations.
      - `sessionTimeoutMinutes` — number — Minutes a conversation can stay idle before the next message starts a new session. Omit to start a new session at the end of the agent's local day (`engine.ai.timeZone`). Allowed values: 15, 30, 60, 120. _(min=15; max=120)_
      - `verbosity` — string — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
    - `assistant` — AssistantChannelSettings — Assistant channel settings. Presence enables the in-app assistant surface; audio remains unavailable unless its separate settings are present and enabled.
      - `default` — boolean — Offer this agent as the default assistant for users covered by the agent access settings.
      - `ui` — AssistantUiSettings — How the agent presents itself in the assistant UI: what the user reads before typing anything, and what they can start from without typing at all. Everything here is presentation — it never changes what the agent can do.
        - _(nesting depth limit — see `AssistantUiSettings` in the Schemas appendix)_
      - `audio` — AssistantAudioSettings — Switchable audio for the assistant channel. The settings object keeps enablement beside its speech policy, matching the voice channel's switchable blocks so a disabled configuration can be retained without serving audio.
        - _(nesting depth limit — see `AssistantAudioSettings` in the Schemas appendix)_
  - `engine` — union **(required)** — How the agent produces replies. `ai` is the managed engine; `webhook` and `sqs` delegate to an external backend.
    - _oneOf_ — exactly one of:
      - **`ai`**
        - `ai` — AgentAiEngine **(required)** — Managed AI engine: the platform runs the model, tools and knowledge lookups.
          - _(nesting depth limit — see `AgentAiEngine` in the Schemas appendix)_
      - **`webhook`**
        - `webhook` — AgentWebhookEngine **(required)** — Bring-your-own backend over HTTPS. The platform POSTs call events to the URL; the backend answers out of band through the channel's command API. The response body is not read.
          - _(nesting depth limit — see `AgentWebhookEngine` in the Schemas appendix)_
      - **`sqs`**
        - `sqs` — AgentSqsEngine **(required)** — Bring-your-own backend over SQS. The platform sends call events to the queue; the backend answers out of band through the channel's command API.
          - _(nesting depth limit — see `AgentSqsEngine` in the Schemas appendix)_
  - `settings` — AgentSettings — Agent-level settings shared across all channels.
    - `pbxGroupId` — string — PBX group used for data ACL (e.g. Sales Intelligence lookups).
  - `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
    - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
    - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
      - _array of_ `AgentGrantPrincipal`
        - _(nesting depth limit — see `AgentGrantPrincipal` in the Schemas appendix)_
  - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
    - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
    - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
    - `name` — string — Human readable name of the actor at the time of the action.
  - `updatedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `updatedBy` — Actor — Who performed an action: an interactive user, an API key or an internal service.
    - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
    - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
    - `name` — string — Human readable name of the actor at the time of the action.
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `status` — string **(required)** _(enum: `draft`, `active`)_
  - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
  - `latestVersion` — number — Latest published version number; absent while the agent is still a draft. _(min=1)_
  - `draftBaseVersion` — number — Published version number from which the current draft originated. Absent before the first version is published. _(min=1)_
  - `deployment` — array — How new sessions are split across published versions. Absent while the agent is still a draft. _(minItems=1; maxItems=10)_
    - _array of_ `AgentDeploymentRoute`
      - `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
      - `percentage` — number **(required)** — Percentage of new sessions routed to this version. Percentages must sum to 100. _(min=1; max=100)_

**`RevisionConflictExceptionResponseContent`**

_The resource was modified concurrently; re-read it and retry with the latest revision._

- `message` — string **(required)**
- `type` — string _(default=RevisionConflictException)_
- `currentRevision` — number — The current revision of the resource on the server.

**`SandboxNetworkAccess`**

_Network access policy for the sandbox._

- string _(enum: `allow-all`, `deny-all`, `allowlist`)_

**`SandboxSize`**

_Compute size of each sandbox launched from the snapshot. Each level maps to a platform-defined vCPU/memory/disk allocation._

- string _(enum: `min`, `small`, `large`, `max`)_

**`SecretRef`**

_A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value._

- `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_

**`UpdateAgentRequestContent`**

_The complete, versionable configuration of an agent. This is what gets snapshotted when a version is published._

- `name` — string **(required)** _(minLen=3; maxLen=255)_
- `description` — string _(minLen=1; maxLen=1000)_
- `category` — string — Category of the agent, e.g.: 'Support'. _(minLen=1; maxLen=128)_
- `picture` — string — Avatar URL.
- `channels` — AgentChannels **(required)** — The channels an agent serves and their channel-specific settings. Presence of a member enables that channel. Empty means the agent serves no channel: it is not reachable on its own and runs only as an automation's task or when another agent calls it. Enabled channels are mirrored as ChannelType values on AgentInfo.
  - `voice` — VoiceChannelSettings — Voice channel settings. Note: a voice agent's AgentAccess.grants are ignored — inbound calls are routed by the PBX dialplan and data ACL is the agent-level `settings.pbxGroupId`, not per-user grants.
    - `greeting` — string — Message spoken when the call starts.
    - `backgroundSound` — VoiceBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT like `interruptions` and `endCall`, rather than a loose name on the channel: it is one switchable call behaviour, it reads the same way as its siblings, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
      - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
      - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
    - `speech` — VoiceSpeechSettings — Speech configuration for the voice channel. When present it WINS over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the single exception, because it is the channel's own input signal and the feature has no starting point without it.
      - `languages` — array **(required)** — Configured languages. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once: automatic detection here is opt-in (`transcription.autoDetect`), and once a caller turns it on, the service does not clamp the resulting candidate list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five) — a caller who both opts in and configures more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. With detection off, only the single resolved language is ever sent, so the ceiling never becomes a candidate-list problem at all. _(minItems=1; maxItems=10)_
        - _(nesting depth limit — see `VoiceLanguage` in the Schemas appendix)_
      - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in the voice, provider account and pronunciation rules of its own language, instead of only the language the call resolved to. Languages whose first message is empty, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
      - `transcription` — VoiceTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
        - _(nesting depth limit — see `VoiceTranscriptionSettings` in the Schemas appendix)_
    - `interruptions` — VoiceInterruptionSettings
      - `enabled` — boolean **(required)** — Whether the caller can interrupt the agent while it is speaking.
      - `minWords` — number — Minimum number of caller words that count as an interruption. _(min=1; max=10)_
    - `silenceTimeout` — VoiceSilenceTimeoutSettings
      - `seconds` — number **(required)** — Seconds of caller silence before the action is taken. _(min=1; max=600)_
      - `action` — union **(required)**
        - _(nesting depth limit — see `VoiceTerminateAction` in the Schemas appendix)_
    - `maxDuration` — VoiceMaxDurationSettings
      - `seconds` — number **(required)** — Maximum call duration in seconds before the action is taken. _(min=10; max=14400)_
      - `action` — union **(required)**
        - _(nesting depth limit — see `VoiceTerminateAction` in the Schemas appendix)_
    - `endCall` — VoiceEndCallSettings
      - `enabled` — boolean **(required)**
      - `phrases` — string — Comma-separated phrases that end the call, e.g. 'goodbye,bye'.
    - `callerMetadata` — VoiceCallerMetadataSettings — Caller context injected into the model prompt.
      - `callerName` — boolean — Include the caller name. Defaults to true.
      - `callerNumber` — boolean — Include the caller phone number. Defaults to true.
      - `callerEmail` — boolean — Include the caller email when known. Defaults to false.
      - `callerCompany` — boolean — Include the caller company when known. Defaults to false.
      - `time` — boolean — Include the current time, rendered in the agent's `engine.ai.timeZone`. Defaults to false.
  - `chat` — ChatChannelSettings
    - `discoverable` — boolean — Whether users can find and add this agent to conversations.
    - `sessionTimeoutMinutes` — number — Minutes a conversation can stay idle before the next message starts a new session. Omit to start a new session at the end of the agent's local day (`engine.ai.timeZone`). Allowed values: 15, 30, 60, 120. _(min=15; max=120)_
    - `verbosity` — string — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
  - `assistant` — AssistantChannelSettings — Assistant channel settings. Presence enables the in-app assistant surface; audio remains unavailable unless its separate settings are present and enabled.
    - `default` — boolean — Offer this agent as the default assistant for users covered by the agent access settings.
    - `ui` — AssistantUiSettings — How the agent presents itself in the assistant UI: what the user reads before typing anything, and what they can start from without typing at all. Everything here is presentation — it never changes what the agent can do.
      - `welcome` — AssistantWelcomeSettings — Greeting shown on an empty thread, above the quick commands.
        - _(nesting depth limit — see `AssistantWelcomeSettings` in the Schemas appendix)_
      - `commands` — array — Cards offered under the welcome message on an empty thread, in the order given. Empty or omitted shows no cards. _(maxItems=8)_
        - _(nesting depth limit — see `AssistantQuickCommand` in the Schemas appendix)_
      - `placeholder` — string — Placeholder text in the composer, e.g. 'Ask about an account…'. Defaults to the client's own placeholder when omitted. _(minLen=1; maxLen=100)_
    - `audio` — AssistantAudioSettings — Switchable audio for the assistant channel. The settings object keeps enablement beside its speech policy, matching the voice channel's switchable blocks so a disabled configuration can be retained without serving audio.
      - `enabled` — boolean **(required)** — Whether the assistant accepts audio calls. Required so the presence of saved speech configuration is never mistaken for enablement.
      - `speech` — AssistantSpeechSettings — Recognition and synthesis policy for assistant audio. This is assistant-owned rather than a VoiceSpeechSettings reuse so telephony and assistant audio can evolve independently. It has no language greeting and no greet-every-language switch because an assistant conversation is already open when its audio call starts, leaving nothing for the channel to greet.
        - _(nesting depth limit — see `AssistantSpeechSettings` in the Schemas appendix)_
- `engine` — union **(required)** — How the agent produces replies. `ai` is the managed engine; `webhook` and `sqs` delegate to an external backend.
  - _oneOf_ — exactly one of:
    - **`ai`**
      - `ai` — AgentAiEngine **(required)** — Managed AI engine: the platform runs the model, tools and knowledge lookups.
        - `instructions` — string **(required)** _(minLen=1; maxLen=60000)_
        - `workflow` — AgentWorkflow — The agent's conversation as a graph: which step runs first, what each step does, and on what condition control moves on. Optional on AgentAiEngine — without one the agent is prompt-driven, steered by `instructions` and free to use its capabilities in any order. Versioned with the rest of the agent definition: publishing a version snapshots the graph, and a draft edit reaches no session until it is published and routed.
          - _(nesting depth limit — see `AgentWorkflow` in the Schemas appendix)_
        - `guardrails` — AgentGuardrails — Turn screening, by side. Only `input` exists: it guards what reaches the model, and output screening is a separate policy with different actions, added here when it is built.
          - _(nesting depth limit — see `AgentGuardrails` in the Schemas appendix)_
        - `model` — string — Defaults to the platform default model when omitted. _(pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
        - `timeZone` — string — IANA timezone the agent reasons about time in: it anchors the current date and time given to the model and how times are read from and written to tool arguments and replies. Shared by every channel the agent serves. Defaults to 'UTC'. _(minLen=1; maxLen=64)_
        - `artifacts` — boolean — Whether the agent can produce artifacts (wilma-artifacts): files it writes in its sandbox and shares back during a session — a document, a PDF, a spreadsheet, a chart, a multi-page web site, a folder of files. Needs the sandbox capability. An artifact starts private to the user the session runs for, who can share it company-wide from the viewer; on the chat channel the runtime shares each one company-wide as it is created, so the link posted into the conversation opens for every signed-in colleague. Artifacts are company-internal: recipients on external transports (sms / whatsapp) or outside the company cannot open the links, so keep this disabled for customer-facing agents. Defaults to false.
        - `skills` — array — Skills attached to this agent (progressive disclosure). A skill may carry its own tools, which join this agent's toolset while that skill is active.
          - _(nesting depth limit — see `AgentSkillReference` in the Schemas appendix)_
        - `capabilities` — array — Everything the agent can do. When a `workflow` is set these are the capabilities in scope at every step, and a step may add to them or narrow them with its own list of the same shape.
          - _(nesting depth limit — see `AgentCapability` in the Schemas appendix)_
        - `variables` — array
          - _(nesting depth limit — see `AgentVariable` in the Schemas appendix)_
    - **`webhook`**
      - `webhook` — AgentWebhookEngine **(required)** — Bring-your-own backend over HTTPS. The platform POSTs call events to the URL; the backend answers out of band through the channel's command API. The response body is not read.
        - `url` — string **(required)**
        - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
          - _(nesting depth limit — see `SecretRef` in the Schemas appendix)_
        - `timeout` — number — Timeout of one delivery, in milliseconds. _(default=10000; min=5000; max=120000)_
    - **`sqs`**
      - `sqs` — AgentSqsEngine **(required)** — Bring-your-own backend over SQS. The platform sends call events to the queue; the backend answers out of band through the channel's command API.
        - `url` — string **(required)**
        - `key` — string **(required)**
        - `secret` — SecretRef — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
          - _(nesting depth limit — see `SecretRef` in the Schemas appendix)_
- `settings` — AgentSettings — Agent-level settings shared across all channels.
  - `pbxGroupId` — string — PBX group used for data ACL (e.g. Sales Intelligence lookups).
- `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
  - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
  - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
    - _array of_ `AgentGrantPrincipal`
      - _oneOf_ — exactly one of:
        - **`userId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`groupId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`department`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
- `revision` — number **(required)** — Draft revision this update is based on (optimistic locking). When it does not match the current revision, RevisionConflictException is returned.

**`UpdateAgentResponseContent`**

- `agent` — Agent **(required)** — The complete, versionable configuration of an agent. This is what gets snapshotted when a version is published.
  - `name` — string **(required)** _(minLen=3; maxLen=255)_
  - `description` — string _(minLen=1; maxLen=1000)_
  - `category` — string — Category of the agent, e.g.: 'Support'. _(minLen=1; maxLen=128)_
  - `picture` — string — Avatar URL.
  - `channels` — AgentChannels **(required)** — The channels an agent serves and their channel-specific settings. Presence of a member enables that channel. Empty means the agent serves no channel: it is not reachable on its own and runs only as an automation's task or when another agent calls it. Enabled channels are mirrored as ChannelType values on AgentInfo.
    - `voice` — VoiceChannelSettings — Voice channel settings. Note: a voice agent's AgentAccess.grants are ignored — inbound calls are routed by the PBX dialplan and data ACL is the agent-level `settings.pbxGroupId`, not per-user grants.
      - `greeting` — string — Message spoken when the call starts.
      - `backgroundSound` — VoiceBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT like `interruptions` and `endCall`, rather than a loose name on the channel: it is one switchable call behaviour, it reads the same way as its siblings, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
        - _(nesting depth limit — see `VoiceBackgroundSoundSettings` in the Schemas appendix)_
      - `speech` — VoiceSpeechSettings — Speech configuration for the voice channel. When present it WINS over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the single exception, because it is the channel's own input signal and the feature has no starting point without it.
        - _(nesting depth limit — see `VoiceSpeechSettings` in the Schemas appendix)_
      - `interruptions` — VoiceInterruptionSettings
        - _(nesting depth limit — see `VoiceInterruptionSettings` in the Schemas appendix)_
      - `silenceTimeout` — VoiceSilenceTimeoutSettings
        - _(nesting depth limit — see `VoiceSilenceTimeoutSettings` in the Schemas appendix)_
      - `maxDuration` — VoiceMaxDurationSettings
        - _(nesting depth limit — see `VoiceMaxDurationSettings` in the Schemas appendix)_
      - `endCall` — VoiceEndCallSettings
        - _(nesting depth limit — see `VoiceEndCallSettings` in the Schemas appendix)_
      - `callerMetadata` — VoiceCallerMetadataSettings — Caller context injected into the model prompt.
        - _(nesting depth limit — see `VoiceCallerMetadataSettings` in the Schemas appendix)_
    - `chat` — ChatChannelSettings
      - `discoverable` — boolean — Whether users can find and add this agent to conversations.
      - `sessionTimeoutMinutes` — number — Minutes a conversation can stay idle before the next message starts a new session. Omit to start a new session at the end of the agent's local day (`engine.ai.timeZone`). Allowed values: 15, 30, 60, 120. _(min=15; max=120)_
      - `verbosity` — string — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
    - `assistant` — AssistantChannelSettings — Assistant channel settings. Presence enables the in-app assistant surface; audio remains unavailable unless its separate settings are present and enabled.
      - `default` — boolean — Offer this agent as the default assistant for users covered by the agent access settings.
      - `ui` — AssistantUiSettings — How the agent presents itself in the assistant UI: what the user reads before typing anything, and what they can start from without typing at all. Everything here is presentation — it never changes what the agent can do.
        - _(nesting depth limit — see `AssistantUiSettings` in the Schemas appendix)_
      - `audio` — AssistantAudioSettings — Switchable audio for the assistant channel. The settings object keeps enablement beside its speech policy, matching the voice channel's switchable blocks so a disabled configuration can be retained without serving audio.
        - _(nesting depth limit — see `AssistantAudioSettings` in the Schemas appendix)_
  - `engine` — union **(required)** — How the agent produces replies. `ai` is the managed engine; `webhook` and `sqs` delegate to an external backend.
    - _oneOf_ — exactly one of:
      - **`ai`**
        - `ai` — AgentAiEngine **(required)** — Managed AI engine: the platform runs the model, tools and knowledge lookups.
          - _(nesting depth limit — see `AgentAiEngine` in the Schemas appendix)_
      - **`webhook`**
        - `webhook` — AgentWebhookEngine **(required)** — Bring-your-own backend over HTTPS. The platform POSTs call events to the URL; the backend answers out of band through the channel's command API. The response body is not read.
          - _(nesting depth limit — see `AgentWebhookEngine` in the Schemas appendix)_
      - **`sqs`**
        - `sqs` — AgentSqsEngine **(required)** — Bring-your-own backend over SQS. The platform sends call events to the queue; the backend answers out of band through the channel's command API.
          - _(nesting depth limit — see `AgentSqsEngine` in the Schemas appendix)_
  - `settings` — AgentSettings — Agent-level settings shared across all channels.
    - `pbxGroupId` — string — PBX group used for data ACL (e.g. Sales Intelligence lookups).
  - `access` — AgentAccess — Who is allowed to use the agent. There is no view/edit dimension — access solely grants the ability to use the agent. Where it is applied, per channel: - `assistant` — enforced. GetAgent on wilma-assistant refuses an agent the caller is not granted. - `voice` — deliberately not applied. Inbound calls are routed by the PBX dialplan, and the data ACL is the agent-level `settings.pbxGroupId`, not per-user grants. - `chat` — enforced for COLLEAGUES ONLY. wilma-chat checks the sender against this block when the sender belongs to the agent's own company. A sender from outside it — a Kite website visitor, an SMS or WhatsApp contact — is not governed by this field at all and reaches the agent under every visibility; what exposes an agent to them is an administrator wiring it to that surface. A refused colleague receives one short refusal message and no turn is started. A `groupId` grant is weaker here than on the assistant: this channel reads the sender's group from their x-bees user record, which does not always carry one. When EVERY grant on the agent is a `groupId` grant and the sender's group is unknown, the sender is PASSED rather than refused — refusing would lock out everyone whose record lacks a group, which is a large minority. Adding a `userId` or `department` grant removes that waiver and the agent is enforced normally, so use one of those where the restriction must hold on chat. (x-bees chat bots are a separate stack with their own company-level `BotAccess`; it is not this field.) When an agent is invoked as a background task its agent-level access is not used — invocation access is configured per reference on the calling agent (see AgentCallCapability.access).
    - `visibility` — string _(enum: `explicit`, `organization`, `public`)_
    - `grants` — array — Users, groups and departments granted the ability to use the agent. Applies when visibility is `explicit`.
      - _array of_ `AgentGrantPrincipal`
        - _(nesting depth limit — see `AgentGrantPrincipal` in the Schemas appendix)_
  - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `createdBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
    - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
    - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
    - `name` — string — Human readable name of the actor at the time of the action.
  - `updatedAt` — string — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `updatedBy` — Actor — Who performed an action: an interactive user, an API key or an internal service.
    - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
    - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
    - `name` — string — Human readable name of the actor at the time of the action.
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `status` — string **(required)** _(enum: `draft`, `active`)_
  - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
  - `latestVersion` — number — Latest published version number; absent while the agent is still a draft. _(min=1)_
  - `draftBaseVersion` — number — Published version number from which the current draft originated. Absent before the first version is published. _(min=1)_
  - `deployment` — array — How new sessions are split across published versions. Absent while the agent is still a draft. _(minItems=1; maxItems=10)_
    - _array of_ `AgentDeploymentRoute`
      - `version` — number **(required)** — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_
      - `percentage` — number **(required)** — Percentage of new sessions routed to this version. Percentages must sum to 100. _(min=1; max=100)_

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

**`VoiceBackgroundSoundSettings`**

_Ambient background audio played under the call. A SETTINGS OBJECT like `interruptions` and `endCall`, rather than a loose name on the channel: it is one switchable call behaviour, it reads the same way as its siblings, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case._

- `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
- `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_

**`VoiceCallerMetadataSettings`**

_Caller context injected into the model prompt._

- `callerName` — boolean — Include the caller name. Defaults to true.
- `callerNumber` — boolean — Include the caller phone number. Defaults to true.
- `callerEmail` — boolean — Include the caller email when known. Defaults to false.
- `callerCompany` — boolean — Include the caller company when known. Defaults to false.
- `time` — boolean — Include the current time, rendered in the agent's `engine.ai.timeZone`. Defaults to false.

**`VoiceChannelSettings`**

_Voice channel settings. Note: a voice agent's AgentAccess.grants are ignored — inbound calls are routed by the PBX dialplan and data ACL is the agent-level `settings.pbxGroupId`, not per-user grants._

- `greeting` — string — Message spoken when the call starts.
- `backgroundSound` — VoiceBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT like `interruptions` and `endCall`, rather than a loose name on the channel: it is one switchable call behaviour, it reads the same way as its siblings, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
  - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
  - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
- `speech` — VoiceSpeechSettings — Speech configuration for the voice channel. When present it WINS over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the single exception, because it is the channel's own input signal and the feature has no starting point without it.
  - `languages` — array **(required)** — Configured languages. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once: automatic detection here is opt-in (`transcription.autoDetect`), and once a caller turns it on, the service does not clamp the resulting candidate list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five) — a caller who both opts in and configures more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. With detection off, only the single resolved language is ever sent, so the ceiling never becomes a candidate-list problem at all. _(minItems=1; maxItems=10)_
    - _array of_ `VoiceLanguage`
      - `code` — string **(required)** — BCP-47 code with locale, e.g. 'en-US', 'it-IT'. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `voice` — string **(required)** — Voice this language speaks with, as a URI — provider, voice id, synthesis parameters and, where the company uses its own provider account, an `apiKey=secrets:{secretId}` reference. See VoiceUri. PER LANGUAGE, and that is the whole reason the member is here rather than on the settings above: provider quality is not uniform across languages, a voice id belongs to exactly one provider, and a bot-wide provider made changing it invalidate every configured voice at once. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
      - `greeting` — string — Initial phrase spoken when the call starts in this language. Absent or empty means the agent says nothing and waits — it does NOT fall back to VoiceChannelSettings.greeting, which would speak one language's text in another language's voice.
      - `isDefault` — boolean — Marks the language a caller hears when their own matches nothing configured. THE FULL RESOLUTION ORDER, since a client author reading only this contract cannot otherwise find it: an exact match on the call's language, then a match on its primary subtag (`fr` finds `fr-FR`), then the language marked here, then a language whose primary subtag is `en`, then the first entry in the list. Marked is consulted BEFORE the English step, so a record with none marked resolves exactly as it did before this member existed. English is deliberate rather than arbitrary — it is the language a caller the agent was not built for is likeliest to understand — and the last step exists only to keep the rule total, which is why list order should not be treated as configuration. At most one language may carry it. A record with two — reachable through the API or the CLI, where no form prevents it — resolves to the first marked one in list order, because refusing a call over configuration drift is worse than serving it and saying so in the trace.
      - `pronunciations` — array — The rules this language is spoken with. THE WHOLE SET rather than an override layer: an agent's respellings are stored here and read from here, so what this list says is what the caller hears. THERE IS NOTHING ABOVE IT. An earlier draft of this contract carried a company-wide dictionary per language that every agent speaking it inherited, with a merge order over this member and an identity rule ('Wildix' -> 'Wildix') for declining an inherited respelling. It bought correcting a handful of names in one place, and cost a second store, a merge on every synthesis path, a screen of its own, and a reader who could not tell from an agent what that agent would actually say. Per language per agent is where the divergence that matters already lives. _(maxItems=200)_
        - _(nesting depth limit — see `VoicePronunciation` in the Schemas appendix)_
  - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in the voice, provider account and pronunciation rules of its own language, instead of only the language the call resolved to. Languages whose first message is empty, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
  - `transcription` — VoiceTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
    - `engine` — string — Recogniser to transcribe the caller with. Absent resolves to the platform default ('aws://transcribe' today), resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
    - `autoDetect` — boolean — Identify the caller's language per utterance and switch voice and reply language mid-call. HERE RATHER THAN ON `VoiceSpeechSettings`, because identifying a language is something the RECOGNISER does: it becomes identify-multiple-languages plus language-options on the recognition stream, and nothing about synthesis reads it. Requires at least two configured languages and a recogniser that can identify them; the server clamps it to false otherwise, because forwarding true with a single candidate makes Amazon reject the stream outright.
- `interruptions` — VoiceInterruptionSettings
  - `enabled` — boolean **(required)** — Whether the caller can interrupt the agent while it is speaking.
  - `minWords` — number — Minimum number of caller words that count as an interruption. _(min=1; max=10)_
- `silenceTimeout` — VoiceSilenceTimeoutSettings
  - `seconds` — number **(required)** — Seconds of caller silence before the action is taken. _(min=1; max=600)_
  - `action` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`hangup`**
        - `hangup` — VoiceTerminateHangupAction **(required)**
          - _(nesting depth limit — see `VoiceTerminateHangupAction` in the Schemas appendix)_
      - **`transfer`**
        - `transfer` — VoiceTransferTarget **(required)**
          - _(nesting depth limit — see `VoiceTransferTarget` in the Schemas appendix)_
- `maxDuration` — VoiceMaxDurationSettings
  - `seconds` — number **(required)** — Maximum call duration in seconds before the action is taken. _(min=10; max=14400)_
  - `action` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`hangup`**
        - `hangup` — VoiceTerminateHangupAction **(required)**
          - _(nesting depth limit — see `VoiceTerminateHangupAction` in the Schemas appendix)_
      - **`transfer`**
        - `transfer` — VoiceTransferTarget **(required)**
          - _(nesting depth limit — see `VoiceTransferTarget` in the Schemas appendix)_
- `endCall` — VoiceEndCallSettings
  - `enabled` — boolean **(required)**
  - `phrases` — string — Comma-separated phrases that end the call, e.g. 'goodbye,bye'.
- `callerMetadata` — VoiceCallerMetadataSettings — Caller context injected into the model prompt.
  - `callerName` — boolean — Include the caller name. Defaults to true.
  - `callerNumber` — boolean — Include the caller phone number. Defaults to true.
  - `callerEmail` — boolean — Include the caller email when known. Defaults to false.
  - `callerCompany` — boolean — Include the caller company when known. Defaults to false.
  - `time` — boolean — Include the current time, rendered in the agent's `engine.ai.timeZone`. Defaults to false.

**`VoiceEndCallSettings`**

- `enabled` — boolean **(required)**
- `phrases` — string — Comma-separated phrases that end the call, e.g. 'goodbye,bye'.

**`VoiceInterruptionSettings`**

- `enabled` — boolean **(required)** — Whether the caller can interrupt the agent while it is speaking.
- `minWords` — number — Minimum number of caller words that count as an interruption. _(min=1; max=10)_

**`VoiceLanguage`**

_One configured language: its voice, its initial phrase and its pronunciation rules._

- `code` — string **(required)** — BCP-47 code with locale, e.g. 'en-US', 'it-IT'. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `voice` — string **(required)** — Voice this language speaks with, as a URI — provider, voice id, synthesis parameters and, where the company uses its own provider account, an `apiKey=secrets:{secretId}` reference. See VoiceUri. PER LANGUAGE, and that is the whole reason the member is here rather than on the settings above: provider quality is not uniform across languages, a voice id belongs to exactly one provider, and a bot-wide provider made changing it invalidate every configured voice at once. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
- `greeting` — string — Initial phrase spoken when the call starts in this language. Absent or empty means the agent says nothing and waits — it does NOT fall back to VoiceChannelSettings.greeting, which would speak one language's text in another language's voice.
- `isDefault` — boolean — Marks the language a caller hears when their own matches nothing configured. THE FULL RESOLUTION ORDER, since a client author reading only this contract cannot otherwise find it: an exact match on the call's language, then a match on its primary subtag (`fr` finds `fr-FR`), then the language marked here, then a language whose primary subtag is `en`, then the first entry in the list. Marked is consulted BEFORE the English step, so a record with none marked resolves exactly as it did before this member existed. English is deliberate rather than arbitrary — it is the language a caller the agent was not built for is likeliest to understand — and the last step exists only to keep the rule total, which is why list order should not be treated as configuration. At most one language may carry it. A record with two — reachable through the API or the CLI, where no form prevents it — resolves to the first marked one in list order, because refusing a call over configuration drift is worse than serving it and saying so in the trace.
- `pronunciations` — array — The rules this language is spoken with. THE WHOLE SET rather than an override layer: an agent's respellings are stored here and read from here, so what this list says is what the caller hears. THERE IS NOTHING ABOVE IT. An earlier draft of this contract carried a company-wide dictionary per language that every agent speaking it inherited, with a merge order over this member and an identity rule ('Wildix' -> 'Wildix') for declining an inherited respelling. It bought correcting a handful of names in one place, and cost a second store, a merge on every synthesis path, a screen of its own, and a reader who could not tell from an agent what that agent would actually say. Per language per agent is where the divergence that matters already lives. _(maxItems=200)_
  - _array of_ `VoicePronunciation`
    - `phrase` — string **(required)** — The phrase as it appears in the text, e.g. 'Wildix'. Bounded because every rule is compiled into ONE regular expression — see the list below. _(maxLen=200)_
    - `as` — string **(required)** — Respelling (ALIAS) or phonetic transcription (IPA), e.g. 'Wil-dix'. _(maxLen=200)_
    - `encoding` — string — How the `as` member of a pronunciation rule is written. _(enum: `alias`, `ipa`)_

**`VoiceMaxDurationSettings`**

- `seconds` — number **(required)** — Maximum call duration in seconds before the action is taken. _(min=10; max=14400)_
- `action` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`hangup`**
      - `hangup` — VoiceTerminateHangupAction **(required)**
        - `message` — string — Message played before hanging up. Played in every language of the call while `messages` is absent or empty; not consulted once `messages` carries any entry.
        - `messages` — array — Per-language messages played before hanging up. Same rule as `AgentTool.startMessages`: the entry for the call's current language is played, a language with no entry is silent, and with no effective speech configuration `message` is played.
          - _(nesting depth limit — see `AgentSpokenPhrase` in the Schemas appendix)_
    - **`transfer`**
      - `transfer` — VoiceTransferTarget **(required)**
        - `name` — string **(required)** — Human readable name the model can refer to, e.g. 'Billing department'.
        - `description` — string — When this target should be chosen.
        - `context` — string **(required)**
        - `extension` — string **(required)**

**`VoicePronunciation`**

_A pronunciation rule for one phrase. Belongs to a LANGUAGE, not to the agent: 'Wildix' is respelled differently for an Italian and a German voice, so one list shared ACROSS languages would fight itself. That is why the rules hang off the language and nowhere else — there is no company-wide dictionary above them to inherit from, or to disagree with._

- `phrase` — string **(required)** — The phrase as it appears in the text, e.g. 'Wildix'. Bounded because every rule is compiled into ONE regular expression — see the list below. _(maxLen=200)_
- `as` — string **(required)** — Respelling (ALIAS) or phonetic transcription (IPA), e.g. 'Wil-dix'. _(maxLen=200)_
- `encoding` — string — How the `as` member of a pronunciation rule is written. _(enum: `alias`, `ipa`)_

**`VoicePronunciationEncoding`**

_How the `as` member of a pronunciation rule is written._

- string _(enum: `alias`, `ipa`)_

**`VoiceSilenceTimeoutSettings`**

- `seconds` — number **(required)** — Seconds of caller silence before the action is taken. _(min=1; max=600)_
- `action` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`hangup`**
      - `hangup` — VoiceTerminateHangupAction **(required)**
        - `message` — string — Message played before hanging up. Played in every language of the call while `messages` is absent or empty; not consulted once `messages` carries any entry.
        - `messages` — array — Per-language messages played before hanging up. Same rule as `AgentTool.startMessages`: the entry for the call's current language is played, a language with no entry is silent, and with no effective speech configuration `message` is played.
          - _(nesting depth limit — see `AgentSpokenPhrase` in the Schemas appendix)_
    - **`transfer`**
      - `transfer` — VoiceTransferTarget **(required)**
        - `name` — string **(required)** — Human readable name the model can refer to, e.g. 'Billing department'.
        - `description` — string — When this target should be chosen.
        - `context` — string **(required)**
        - `extension` — string **(required)**

**`VoiceSpeechSettings`**

_Speech configuration for the voice channel. When present it WINS over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the single exception, because it is the channel's own input signal and the feature has no starting point without it._

- `languages` — array **(required)** — Configured languages. The @length bound is a STORAGE ceiling, not a promise about what a recogniser accepts at once: automatic detection here is opt-in (`transcription.autoDetect`), and once a caller turns it on, the service does not clamp the resulting candidate list to a recogniser's own practical limit today (Amazon Transcribe's documented recommendation for streaming identification is five) — a caller who both opts in and configures more than a recogniser accepts should expect degraded identification or a rejected stream, not a refusal from this contract. With detection off, only the single resolved language is ever sent, so the ceiling never becomes a candidate-list problem at all. _(minItems=1; maxItems=10)_
  - _array of_ `VoiceLanguage`
    - `code` — string **(required)** — BCP-47 code with locale, e.g. 'en-US', 'it-IT'. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - `voice` — string **(required)** — Voice this language speaks with, as a URI — provider, voice id, synthesis parameters and, where the company uses its own provider account, an `apiKey=secrets:{secretId}` reference. See VoiceUri. PER LANGUAGE, and that is the whole reason the member is here rather than on the settings above: provider quality is not uniform across languages, a voice id belongs to exactly one provider, and a bot-wide provider made changing it invalidate every configured voice at once. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
    - `greeting` — string — Initial phrase spoken when the call starts in this language. Absent or empty means the agent says nothing and waits — it does NOT fall back to VoiceChannelSettings.greeting, which would speak one language's text in another language's voice.
    - `isDefault` — boolean — Marks the language a caller hears when their own matches nothing configured. THE FULL RESOLUTION ORDER, since a client author reading only this contract cannot otherwise find it: an exact match on the call's language, then a match on its primary subtag (`fr` finds `fr-FR`), then the language marked here, then a language whose primary subtag is `en`, then the first entry in the list. Marked is consulted BEFORE the English step, so a record with none marked resolves exactly as it did before this member existed. English is deliberate rather than arbitrary — it is the language a caller the agent was not built for is likeliest to understand — and the last step exists only to keep the rule total, which is why list order should not be treated as configuration. At most one language may carry it. A record with two — reachable through the API or the CLI, where no form prevents it — resolves to the first marked one in list order, because refusing a call over configuration drift is worse than serving it and saying so in the trace.
    - `pronunciations` — array — The rules this language is spoken with. THE WHOLE SET rather than an override layer: an agent's respellings are stored here and read from here, so what this list says is what the caller hears. THERE IS NOTHING ABOVE IT. An earlier draft of this contract carried a company-wide dictionary per language that every agent speaking it inherited, with a merge order over this member and an identity rule ('Wildix' -> 'Wildix') for declining an inherited respelling. It bought correcting a handful of names in one place, and cost a second store, a merge on every synthesis path, a screen of its own, and a reader who could not tell from an agent what that agent would actually say. Per language per agent is where the divergence that matters already lives. _(maxItems=200)_
      - _array of_ `VoicePronunciation`
        - _(nesting depth limit — see `VoicePronunciation` in the Schemas appendix)_
- `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in the voice, provider account and pronunciation rules of its own language, instead of only the language the call resolved to. Languages whose first message is empty, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
- `transcription` — VoiceTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
  - `engine` — string — Recogniser to transcribe the caller with. Absent resolves to the platform default ('aws://transcribe' today), resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
  - `autoDetect` — boolean — Identify the caller's language per utterance and switch voice and reply language mid-call. HERE RATHER THAN ON `VoiceSpeechSettings`, because identifying a language is something the RECOGNISER does: it becomes identify-multiple-languages plus language-options on the recognition stream, and nothing about synthesis reads it. Requires at least two configured languages and a recogniser that can identify them; the server clamps it to false otherwise, because forwarding true with a single candidate makes Amazon reject the stream outright.

**`VoiceTerminateAction`**

- _oneOf_ — exactly one of:
  - **`hangup`**
    - `hangup` — VoiceTerminateHangupAction **(required)**
      - `message` — string — Message played before hanging up. Played in every language of the call while `messages` is absent or empty; not consulted once `messages` carries any entry.
      - `messages` — array — Per-language messages played before hanging up. Same rule as `AgentTool.startMessages`: the entry for the call's current language is played, a language with no entry is silent, and with no effective speech configuration `message` is played.
        - _array of_ `AgentSpokenPhrase`
          - _(nesting depth limit — see `AgentSpokenPhrase` in the Schemas appendix)_
  - **`transfer`**
    - `transfer` — VoiceTransferTarget **(required)**
      - `name` — string **(required)** — Human readable name the model can refer to, e.g. 'Billing department'.
      - `description` — string — When this target should be chosen.
      - `context` — string **(required)**
      - `extension` — string **(required)**

**`VoiceTerminateHangupAction`**

- `message` — string — Message played before hanging up. Played in every language of the call while `messages` is absent or empty; not consulted once `messages` carries any entry.
- `messages` — array — Per-language messages played before hanging up. Same rule as `AgentTool.startMessages`: the entry for the call's current language is played, a language with no entry is silent, and with no effective speech configuration `message` is played.
  - _array of_ `AgentSpokenPhrase`
    - `language` — string **(required)** — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - `text` — string **(required)**

**`VoiceTranscriptionSettings`**

_Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does._

- `engine` — string — Recogniser to transcribe the caller with. Absent resolves to the platform default ('aws://transcribe' today), resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
- `autoDetect` — boolean — Identify the caller's language per utterance and switch voice and reply language mid-call. HERE RATHER THAN ON `VoiceSpeechSettings`, because identifying a language is something the RECOGNISER does: it becomes identify-multiple-languages plus language-options on the recognition stream, and nothing about synthesis reads it. Requires at least two configured languages and a recogniser that can identify them; the server clamps it to false otherwise, because forwarding true with a single candidate makes Amazon reject the stream outright.

**`VoiceTransferTarget`**

- `name` — string **(required)** — Human readable name the model can refer to, e.g. 'Billing department'.
- `description` — string — When this target should be chosen.
- `context` — string **(required)**
- `extension` — string **(required)**

**`WebSearchContextSize`**

_Search depth/context hint, mapped per provider._

- string _(enum: `low`, `medium`, `high`)_

**`WebSearchUserLocation`**

- `country` — string — ISO 3166-1 alpha-2 country code, e.g. 'US'.
- `region` — string
- `city` — string
- `timezone` — string — IANA timezone, e.g. 'Europe/Rome'.

</details>
