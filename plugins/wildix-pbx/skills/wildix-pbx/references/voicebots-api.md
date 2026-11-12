## VoiceBots API

_OpenAPI: WIM voicebots service — version v2_

**Servers**

- `https://wim.wildix.com` — Production
- `https://wim-stable.wildix.com` — Stable
- `https://wim-stage.wildix.com` — Stage

### VoiceBots

#### `GET` `/v2/voicebots/bots`

Retrieves a list of all voice bots for the specified company.

- operationId: `ListVoiceBots`
- **Scopes**: `voicebots:ListVoiceBots`, `voicebots:read`
- **Parameters**
  - `company` (query) — string
- **Response 200** (`ListVoiceBotsResponseContent`)
  - `bots` — array **(required)**
    - _array of_ `VoiceBot`
      - `name` — string **(required)** _(minLen=3; maxLen=255)_
      - `category` — string — Category of the bot _(minLen=1; maxLen=128)_
      - `message` — string — The initial message that will be played at the start of the session.
      - `pipeline` — VoiceBotPipelineSettings
        - `interuptionsEnabled` — boolean — If enabled the user can interrupt the the bot playback.
        - `maximumDuration` — number — The maximum number of seconds a call will last.
        - `maximumDurationAction` — union
          - _oneOf_ — exactly one of:
            - **`hangup`**
              - `hangup` — VoiceBotTerminateHangupAction **(required)**
            - **`transfer`**
              - `transfer` — VoiceBotTerminateTransferAction **(required)**
                - _(nesting depth limit — see `VoiceBotTerminateTransferAction` in the Schemas appendix)_
        - `silenceTimeout` — number — How long to wait before a call is automatically ended due to inactivity.
        - `silenceTimeoutAction` — union
          - _oneOf_ — exactly one of:
            - **`hangup`**
              - `hangup` — VoiceBotTerminateHangupAction **(required)**
            - **`transfer`**
              - `transfer` — VoiceBotTerminateTransferAction **(required)**
                - _(nesting depth limit — see `VoiceBotTerminateTransferAction` in the Schemas appendix)_
        - `endCallEnabled` — boolean — If enabled the bot can hangup the call.
        - `endCallPhases` — string — A list of phases separated by comma, which will end the call matched.
      - `speech` — VoiceBotSpeechSettings — Speech configuration. When present it wins over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the exception.
        - `languages` — array **(required)** — Configured languages. The @length bound is a storage ceiling; the real cap is the recogniser's own candidate limit, enforced in the service. _(minItems=1; maxItems=10)_
          - _array of_ `VoiceBotLanguage`
            - `code` — string **(required)** — BCP-47 code with locale, e.g. 'en-US'. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
            - `voice` — string **(required)** — Voice this language speaks with, as a URI — provider, voice id, synthesis parameters and, where the company uses its own provider account, its `apiKey` query parameter. See VoiceBotVoiceUri. PER LANGUAGE, and that is the whole reason the member is here rather than on the settings above: provider quality is not uniform across languages, a voice id belongs to exactly one provider, and a bot-wide provider made changing it invalidate every configured voice at once. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
            - `greeting` — string — Initial phrase for this language. Absent or empty means the agent says nothing and waits — it does NOT fall back to the agent-level message, which would speak one language's text in another language's voice.
            - `isDefault` — boolean — Marks the language a caller hears when their own matches nothing configured. THE FULL RESOLUTION ORDER, since a client author reading only this contract cannot otherwise find it: an exact match on the call's language, then a match on its primary subtag (`fr` finds `fr-FR`), then the language marked here, then a language whose primary subtag is `en`, then the first entry in the list. Marked is consulted BEFORE the English step, so a record with none marked resolves exactly as it did before this member existed. English is deliberate rather than arbitrary — it is the language a caller the agent was not built for is likeliest to understand — and the last step exists only to keep the rule total, which is why list order should not be treated as configuration. At most one language may carry it. A record with two — reachable through the API or the CLI, where no form prevents it — resolves to the first marked one in list order, because refusing a call over configuration drift is worse than serving it and saying so in the trace.
            - `pronunciations` — array — Pronunciation rules for one language. BOUNDED, and the bound is not decoration. `applyPronunciations` compiles every rule of a language into a SINGLE alternating regular expression, so the cost is the pattern's total size: measured against the real escaping and matching logic, 1,000 rules cost ~0.9 s of CPU per synthesized sentence, 5,000 cost ~4.9 s, and around 10,000 `new RegExp` throws V8's pattern-size error outright — from a call site outside the surrounding `try`, so a 500 rather than a degraded reply. Stored on a bot, that made every utterance of the agent fail. 200 is far above any real use — a product glossary is a handful of names — and far below where either cost begins. Found by a security review. NO LOWER BOUND on `phrase` or `as`, deliberately. Both consoles add an EMPTY rule row the moment someone clicks 'Add pronunciation', so a `min: 1` would make saving an agent with a half-typed row fail entirely — and the runtime already ignores a rule with no phrase. Dropping blank rows belongs in the consoles' save filters, not in a refusal here. _(maxItems=200)_
              - _(nesting depth limit — see `VoiceBotPronunciation` in the Schemas appendix)_
        - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in its own language's voice, provider account and pronunciation rules. Languages with an empty first message, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
        - `transcription` — VoiceBotTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
          - `engine` — string — Recogniser to transcribe the caller with. Absent resolves to the platform default ('aws://transcribe' today), resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
          - `autoDetect` — boolean — Identify the caller's language per utterance and switch voice and reply language mid-call. HERE RATHER THAN ON `VoiceBotSpeechSettings`, because identifying a language is something the RECOGNISER does: it becomes identify-multiple-languages plus language-options on the recognition stream, and nothing about synthesis reads it. Requires at least two configured languages and a recogniser that can identify them; the server clamps it to false otherwise, because forwarding true with a single candidate makes Amazon reject the stream outright.
      - `backgroundSound` — VoiceBotBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT rather than a loose name on the bot, matching `wildix.wilma.agents`: it is one switchable call behaviour, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
        - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
        - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
      - `endpoint` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`llm`**
            - `llm` — VoiceBotLlmEndpoint **(required)**
              - `prompt` — string **(required)** _(maxLen=40000)_
              - `model` — string — The AI model to use for generating responses. If not specified, uses the default model. _(default=default; pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
              - `guidelines` — array
                - _array of_ `string`
              - `metadata` — VoiceBotPromptMetadata
                - _(nesting depth limit — see `VoiceBotPromptMetadata` in the Schemas appendix)_
              - `embeddedTools` — array — Embedded functions to use within voice session.
                - _(nesting depth limit — see `VoiceBotEmbeddedTool` in the Schemas appendix)_
              - `tools` — array — Custom tools to be used within voice session.
                - _(nesting depth limit — see `VoiceBotTool` in the Schemas appendix)_
              - `capabilities` — array
                - _(nesting depth limit — see `VoiceBotCapability` in the Schemas appendix)_
              - `variables` — array — Variables such as dialplan variables that can be used in the bot.
                - _(nesting depth limit — see `VoiceBotVariable` in the Schemas appendix)_
          - **`dialogflowCx`**
            - `dialogflowCx` — BotDialogflowCxEndpoint **(required)**
              - `credentials` — any **(required)** — Dialogflow Service Account Credentials
              - `agent` — string **(required)** — Dialogflow Agent Id (example - 88ff4635-0852-4f97-ae44-b19ae9fa6ea1
              - `location` — string **(required)** — Dialogflow Agent Region (example: europe-west3)
              - `language` — string **(required)** — Language
          - **`openAiAssistant`**
            - `openAiAssistant` — BotOpenAiAssistantEndpoint **(required)**
              - `key` — string **(required)**
              - `assistantId` — string **(required)**
          - **`webhook`**
            - `webhook` — BotWebhookEndpoint **(required)**
              - `url` — string **(required)**
              - `secret` — string **(required)**
          - **`sqs`**
            - `sqs` — BotSqsEndpoint **(required)**
              - `url` — string **(required)**
              - `key` — string **(required)**
              - `secret` — string **(required)**
      - `capabilities` — array
        - _array of_ `VoiceBotCapability`
          - _oneOf_ — exactly one of:
            - **`tool`**
              - `tool` — VoiceBotCapabilityTool **(required)**
                - _(nesting depth limit — see `VoiceBotCapabilityTool` in the Schemas appendix)_
            - **`kb`**
              - `kb` — VoiceBotKnowledgeBase **(required)**
                - _(nesting depth limit — see `VoiceBotKnowledgeBase` in the Schemas appendix)_
      - `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
      - `id` — string **(required)** _(minLen=12; maxLen=12)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
- Errors: `400`, `403`

#### `POST` `/v2/voicebots/bots`

Creates a new voice bot with the specified configuration for the company.

- operationId: `CreateVoiceBot`
- **Scopes**: `voicebots:CreateVoiceBot`
- **Parameters**
  - `company` (query) — string
- **Request body** (`application/json` — `CreateVoiceBotRequestContent`) **(required)**
  - `name` — string **(required)** _(minLen=3; maxLen=255)_
  - `category` — string — Category of the bot _(minLen=1; maxLen=128)_
  - `message` — string — The initial message that will be played at the start of the session.
  - `pipeline` — VoiceBotPipelineSettings
    - `interuptionsEnabled` — boolean — If enabled the user can interrupt the the bot playback.
    - `maximumDuration` — number — The maximum number of seconds a call will last.
    - `maximumDurationAction` — union
      - _oneOf_ — exactly one of:
        - **`hangup`**
          - `hangup` — VoiceBotTerminateHangupAction **(required)**
        - **`transfer`**
          - `transfer` — VoiceBotTerminateTransferAction **(required)**
            - `context` — string **(required)**
            - `extension` — string **(required)**
    - `silenceTimeout` — number — How long to wait before a call is automatically ended due to inactivity.
    - `silenceTimeoutAction` — union
      - _oneOf_ — exactly one of:
        - **`hangup`**
          - `hangup` — VoiceBotTerminateHangupAction **(required)**
        - **`transfer`**
          - `transfer` — VoiceBotTerminateTransferAction **(required)**
            - `context` — string **(required)**
            - `extension` — string **(required)**
    - `endCallEnabled` — boolean — If enabled the bot can hangup the call.
    - `endCallPhases` — string — A list of phases separated by comma, which will end the call matched.
  - `speech` — VoiceBotSpeechSettings — Speech configuration. When present it wins over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the exception.
    - `languages` — array **(required)** — Configured languages. The @length bound is a storage ceiling; the real cap is the recogniser's own candidate limit, enforced in the service. _(minItems=1; maxItems=10)_
      - _array of_ `VoiceBotLanguage`
        - `code` — string **(required)** — BCP-47 code with locale, e.g. 'en-US'. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
        - `voice` — string **(required)** — Voice this language speaks with, as a URI — provider, voice id, synthesis parameters and, where the company uses its own provider account, its `apiKey` query parameter. See VoiceBotVoiceUri. PER LANGUAGE, and that is the whole reason the member is here rather than on the settings above: provider quality is not uniform across languages, a voice id belongs to exactly one provider, and a bot-wide provider made changing it invalidate every configured voice at once. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
        - `greeting` — string — Initial phrase for this language. Absent or empty means the agent says nothing and waits — it does NOT fall back to the agent-level message, which would speak one language's text in another language's voice.
        - `isDefault` — boolean — Marks the language a caller hears when their own matches nothing configured. THE FULL RESOLUTION ORDER, since a client author reading only this contract cannot otherwise find it: an exact match on the call's language, then a match on its primary subtag (`fr` finds `fr-FR`), then the language marked here, then a language whose primary subtag is `en`, then the first entry in the list. Marked is consulted BEFORE the English step, so a record with none marked resolves exactly as it did before this member existed. English is deliberate rather than arbitrary — it is the language a caller the agent was not built for is likeliest to understand — and the last step exists only to keep the rule total, which is why list order should not be treated as configuration. At most one language may carry it. A record with two — reachable through the API or the CLI, where no form prevents it — resolves to the first marked one in list order, because refusing a call over configuration drift is worse than serving it and saying so in the trace.
        - `pronunciations` — array — Pronunciation rules for one language. BOUNDED, and the bound is not decoration. `applyPronunciations` compiles every rule of a language into a SINGLE alternating regular expression, so the cost is the pattern's total size: measured against the real escaping and matching logic, 1,000 rules cost ~0.9 s of CPU per synthesized sentence, 5,000 cost ~4.9 s, and around 10,000 `new RegExp` throws V8's pattern-size error outright — from a call site outside the surrounding `try`, so a 500 rather than a degraded reply. Stored on a bot, that made every utterance of the agent fail. 200 is far above any real use — a product glossary is a handful of names — and far below where either cost begins. Found by a security review. NO LOWER BOUND on `phrase` or `as`, deliberately. Both consoles add an EMPTY rule row the moment someone clicks 'Add pronunciation', so a `min: 1` would make saving an agent with a half-typed row fail entirely — and the runtime already ignores a rule with no phrase. Dropping blank rows belongs in the consoles' save filters, not in a refusal here. _(maxItems=200)_
          - _array of_ `VoiceBotPronunciation`
            - `phrase` — string **(required)** — The written form to replace. Bounded because every rule is compiled into ONE regular expression — see the list below. _(maxLen=200)_
            - `as` — string **(required)** — Respelling (ALIAS) or phonetic transcription (IPA). _(maxLen=200)_
            - `encoding` — string _(enum: `alias`, `ipa`)_
    - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in its own language's voice, provider account and pronunciation rules. Languages with an empty first message, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
    - `transcription` — VoiceBotTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
      - `engine` — string — Recogniser to transcribe the caller with. Absent resolves to the platform default ('aws://transcribe' today), resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
      - `autoDetect` — boolean — Identify the caller's language per utterance and switch voice and reply language mid-call. HERE RATHER THAN ON `VoiceBotSpeechSettings`, because identifying a language is something the RECOGNISER does: it becomes identify-multiple-languages plus language-options on the recognition stream, and nothing about synthesis reads it. Requires at least two configured languages and a recogniser that can identify them; the server clamps it to false otherwise, because forwarding true with a single candidate makes Amazon reject the stream outright.
  - `backgroundSound` — VoiceBotBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT rather than a loose name on the bot, matching `wildix.wilma.agents`: it is one switchable call behaviour, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
    - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
    - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
  - `endpoint` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`llm`**
        - `llm` — VoiceBotLlmEndpoint **(required)**
          - `prompt` — string **(required)** _(maxLen=40000)_
          - `model` — string — The AI model to use for generating responses. If not specified, uses the default model. _(default=default; pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
          - `guidelines` — array
            - _array of_ `string`
          - `metadata` — VoiceBotPromptMetadata
            - `userName` — VoiceBotPromptMetadataEnabled
              - `enabled` — boolean **(required)** — Whether this metadata field is enabled _(default=True)_
            - `userPhoneNumber` — VoiceBotPromptMetadataEnabled
              - `enabled` — boolean **(required)** — Whether this metadata field is enabled _(default=True)_
            - `userEmail` — VoiceBotPromptMetadataDisabled
              - `enabled` — boolean **(required)** — Whether this metadata field is enabled _(default=False)_
            - `userCompany` — VoiceBotPromptMetadataDisabled
              - `enabled` — boolean **(required)** — Whether this metadata field is enabled _(default=False)_
            - `time` — VoiceBotPromptMetadataTime
              - `enabled` — boolean **(required)** — Whether this metadata field is enabled _(default=False)_
              - `timeZone` — string **(required)** — Timezone for time formatting (e.g., 'Europe/Rome', 'UTC') _(default=UTC)_
          - `embeddedTools` — array — Embedded functions to use within voice session.
            - _array of_ `VoiceBotEmbeddedTool`
              - `type` — string **(required)** _(enum: `HANGUP`, `TRANSFER`, `DELEGATE`, `WAIT`)_
              - `name` — string **(required)**
              - `parameters` — any — The parameters the functions accepts.
              - `annotations` — array
                - _(nesting depth limit — see `VoiceBotToolAnnotation` in the Schemas appendix)_
          - `tools` — array — Custom tools to be used within voice session.
            - _array of_ `VoiceBotTool`
              - `type` — string **(required)** _(enum: `function`)_
              - `function` — VoiceBotFunctionDefinition
                - _(nesting depth limit — see `VoiceBotFunctionDefinition` in the Schemas appendix)_
              - `annotations` — array
                - _(nesting depth limit — see `VoiceBotToolAnnotation` in the Schemas appendix)_
          - `capabilities` — array
            - _array of_ `VoiceBotCapability`
              - _oneOf_ — exactly one of:
                - **`tool`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`kb`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `variables` — array — Variables such as dialplan variables that can be used in the bot.
            - _array of_ `VoiceBotVariable`
              - `name` — string **(required)** _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
      - **`dialogflowCx`**
        - `dialogflowCx` — BotDialogflowCxEndpoint **(required)**
          - `credentials` — any **(required)** — Dialogflow Service Account Credentials
          - `agent` — string **(required)** — Dialogflow Agent Id (example - 88ff4635-0852-4f97-ae44-b19ae9fa6ea1
          - `location` — string **(required)** — Dialogflow Agent Region (example: europe-west3)
          - `language` — string **(required)** — Language
      - **`openAiAssistant`**
        - `openAiAssistant` — BotOpenAiAssistantEndpoint **(required)**
          - `key` — string **(required)**
          - `assistantId` — string **(required)**
      - **`webhook`**
        - `webhook` — BotWebhookEndpoint **(required)**
          - `url` — string **(required)**
          - `secret` — string **(required)**
      - **`sqs`**
        - `sqs` — BotSqsEndpoint **(required)**
          - `url` — string **(required)**
          - `key` — string **(required)**
          - `secret` — string **(required)**
  - `capabilities` — array
    - _array of_ `VoiceBotCapability`
      - _oneOf_ — exactly one of:
        - **`tool`**
          - `tool` — VoiceBotCapabilityTool **(required)**
            - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
            - `variables` — array
              - _array of_ `VoiceBotToolVariable`
                - _(nesting depth limit — see `VoiceBotToolVariable` in the Schemas appendix)_
            - `startMessage` — string — Message spoken when the tool call starts. Spoken in every language of the call while `startMessages` is absent or empty; not consulted once `startMessages` carries any entry.
            - `startMessages` — array — Per-language start messages. When present and non-empty, the entry for the call's current language is spoken and `startMessage` is not consulted; a language with no entry is silent. When absent or empty, `startMessage` is spoken as before. On a call with no effective speech configuration — no configured languages, or a PBX below protocol 2 — `startMessage` is spoken regardless, because there is no current language to choose by.
              - _array of_ `VoiceBotSpokenPhrase`
                - _(nesting depth limit — see `VoiceBotSpokenPhrase` in the Schemas appendix)_
            - `pipeline` — VoiceBotCapabilityToolPipeline
              - `type` — string _(enum: `blocking_request`, `blocking_request_guided`, `async_request`, `async_request_guided`)_
              - `instructions` — string — Instructions for generating a reply when using guided pipeline types. Use {{response}} to reference the tool response.
            - `annotations` — array
              - _array of_ `VoiceBotToolAnnotation`
                - _(nesting depth limit — see `VoiceBotToolAnnotation` in the Schemas appendix)_
        - **`kb`**
          - `kb` — VoiceBotKnowledgeBase **(required)**
            - `knowledgeBaseId` — string
            - `instructions` — string — Additional instructions for when the bot should use this knowledge base.
            - `searchStrategy` — string _(enum: `bm25`, `vector`, `hybrid`)_
            - `searchThreshold` — string _(enum: `low`, `medium`, `high`)_
            - `searchLimit` — number — Maximum number of search results returned by this knowledge base capability. _(min=1; max=50)_
            - `annotations` — array
              - _array of_ `VoiceBotToolAnnotation`
                - _(nesting depth limit — see `VoiceBotToolAnnotation` in the Schemas appendix)_
  - `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
- **Response 200** (`CreateVoiceBotResponseContent`)
  - `bot` — VoiceBot **(required)**
    - `name` — string **(required)** _(minLen=3; maxLen=255)_
    - `category` — string — Category of the bot _(minLen=1; maxLen=128)_
    - `message` — string — The initial message that will be played at the start of the session.
    - `pipeline` — VoiceBotPipelineSettings
      - `interuptionsEnabled` — boolean — If enabled the user can interrupt the the bot playback.
      - `maximumDuration` — number — The maximum number of seconds a call will last.
      - `maximumDurationAction` — union
        - _oneOf_ — exactly one of:
          - **`hangup`**
            - `hangup` — VoiceBotTerminateHangupAction **(required)**
          - **`transfer`**
            - `transfer` — VoiceBotTerminateTransferAction **(required)**
              - `context` — string **(required)**
              - `extension` — string **(required)**
      - `silenceTimeout` — number — How long to wait before a call is automatically ended due to inactivity.
      - `silenceTimeoutAction` — union
        - _oneOf_ — exactly one of:
          - **`hangup`**
            - `hangup` — VoiceBotTerminateHangupAction **(required)**
          - **`transfer`**
            - `transfer` — VoiceBotTerminateTransferAction **(required)**
              - `context` — string **(required)**
              - `extension` — string **(required)**
      - `endCallEnabled` — boolean — If enabled the bot can hangup the call.
      - `endCallPhases` — string — A list of phases separated by comma, which will end the call matched.
    - `speech` — VoiceBotSpeechSettings — Speech configuration. When present it wins over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the exception.
      - `languages` — array **(required)** — Configured languages. The @length bound is a storage ceiling; the real cap is the recogniser's own candidate limit, enforced in the service. _(minItems=1; maxItems=10)_
        - _array of_ `VoiceBotLanguage`
          - `code` — string **(required)** — BCP-47 code with locale, e.g. 'en-US'. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
          - `voice` — string **(required)** — Voice this language speaks with, as a URI — provider, voice id, synthesis parameters and, where the company uses its own provider account, its `apiKey` query parameter. See VoiceBotVoiceUri. PER LANGUAGE, and that is the whole reason the member is here rather than on the settings above: provider quality is not uniform across languages, a voice id belongs to exactly one provider, and a bot-wide provider made changing it invalidate every configured voice at once. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
          - `greeting` — string — Initial phrase for this language. Absent or empty means the agent says nothing and waits — it does NOT fall back to the agent-level message, which would speak one language's text in another language's voice.
          - `isDefault` — boolean — Marks the language a caller hears when their own matches nothing configured. THE FULL RESOLUTION ORDER, since a client author reading only this contract cannot otherwise find it: an exact match on the call's language, then a match on its primary subtag (`fr` finds `fr-FR`), then the language marked here, then a language whose primary subtag is `en`, then the first entry in the list. Marked is consulted BEFORE the English step, so a record with none marked resolves exactly as it did before this member existed. English is deliberate rather than arbitrary — it is the language a caller the agent was not built for is likeliest to understand — and the last step exists only to keep the rule total, which is why list order should not be treated as configuration. At most one language may carry it. A record with two — reachable through the API or the CLI, where no form prevents it — resolves to the first marked one in list order, because refusing a call over configuration drift is worse than serving it and saying so in the trace.
          - `pronunciations` — array — Pronunciation rules for one language. BOUNDED, and the bound is not decoration. `applyPronunciations` compiles every rule of a language into a SINGLE alternating regular expression, so the cost is the pattern's total size: measured against the real escaping and matching logic, 1,000 rules cost ~0.9 s of CPU per synthesized sentence, 5,000 cost ~4.9 s, and around 10,000 `new RegExp` throws V8's pattern-size error outright — from a call site outside the surrounding `try`, so a 500 rather than a degraded reply. Stored on a bot, that made every utterance of the agent fail. 200 is far above any real use — a product glossary is a handful of names — and far below where either cost begins. Found by a security review. NO LOWER BOUND on `phrase` or `as`, deliberately. Both consoles add an EMPTY rule row the moment someone clicks 'Add pronunciation', so a `min: 1` would make saving an agent with a half-typed row fail entirely — and the runtime already ignores a rule with no phrase. Dropping blank rows belongs in the consoles' save filters, not in a refusal here. _(maxItems=200)_
            - _array of_ `VoiceBotPronunciation`
              - _(nesting depth limit — see `VoiceBotPronunciation` in the Schemas appendix)_
      - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in its own language's voice, provider account and pronunciation rules. Languages with an empty first message, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
      - `transcription` — VoiceBotTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
        - `engine` — string — Recogniser to transcribe the caller with. Absent resolves to the platform default ('aws://transcribe' today), resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
        - `autoDetect` — boolean — Identify the caller's language per utterance and switch voice and reply language mid-call. HERE RATHER THAN ON `VoiceBotSpeechSettings`, because identifying a language is something the RECOGNISER does: it becomes identify-multiple-languages plus language-options on the recognition stream, and nothing about synthesis reads it. Requires at least two configured languages and a recogniser that can identify them; the server clamps it to false otherwise, because forwarding true with a single candidate makes Amazon reject the stream outright.
    - `backgroundSound` — VoiceBotBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT rather than a loose name on the bot, matching `wildix.wilma.agents`: it is one switchable call behaviour, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
      - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
      - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
    - `endpoint` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`llm`**
          - `llm` — VoiceBotLlmEndpoint **(required)**
            - `prompt` — string **(required)** _(maxLen=40000)_
            - `model` — string — The AI model to use for generating responses. If not specified, uses the default model. _(default=default; pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
            - `guidelines` — array
              - _array of_ `string`
            - `metadata` — VoiceBotPromptMetadata
              - `userName` — VoiceBotPromptMetadataEnabled
                - _(nesting depth limit — see `VoiceBotPromptMetadataEnabled` in the Schemas appendix)_
              - `userPhoneNumber` — VoiceBotPromptMetadataEnabled
                - _(nesting depth limit — see `VoiceBotPromptMetadataEnabled` in the Schemas appendix)_
              - `userEmail` — VoiceBotPromptMetadataDisabled
                - _(nesting depth limit — see `VoiceBotPromptMetadataDisabled` in the Schemas appendix)_
              - `userCompany` — VoiceBotPromptMetadataDisabled
                - _(nesting depth limit — see `VoiceBotPromptMetadataDisabled` in the Schemas appendix)_
              - `time` — VoiceBotPromptMetadataTime
                - _(nesting depth limit — see `VoiceBotPromptMetadataTime` in the Schemas appendix)_
            - `embeddedTools` — array — Embedded functions to use within voice session.
              - _array of_ `VoiceBotEmbeddedTool`
                - _(nesting depth limit — see `VoiceBotEmbeddedTool` in the Schemas appendix)_
            - `tools` — array — Custom tools to be used within voice session.
              - _array of_ `VoiceBotTool`
                - _(nesting depth limit — see `VoiceBotTool` in the Schemas appendix)_
            - `capabilities` — array
              - _array of_ `VoiceBotCapability`
                - _(nesting depth limit — see `VoiceBotCapability` in the Schemas appendix)_
            - `variables` — array — Variables such as dialplan variables that can be used in the bot.
              - _array of_ `VoiceBotVariable`
                - _(nesting depth limit — see `VoiceBotVariable` in the Schemas appendix)_
        - **`dialogflowCx`**
          - `dialogflowCx` — BotDialogflowCxEndpoint **(required)**
            - `credentials` — any **(required)** — Dialogflow Service Account Credentials
            - `agent` — string **(required)** — Dialogflow Agent Id (example - 88ff4635-0852-4f97-ae44-b19ae9fa6ea1
            - `location` — string **(required)** — Dialogflow Agent Region (example: europe-west3)
            - `language` — string **(required)** — Language
        - **`openAiAssistant`**
          - `openAiAssistant` — BotOpenAiAssistantEndpoint **(required)**
            - `key` — string **(required)**
            - `assistantId` — string **(required)**
        - **`webhook`**
          - `webhook` — BotWebhookEndpoint **(required)**
            - `url` — string **(required)**
            - `secret` — string **(required)**
        - **`sqs`**
          - `sqs` — BotSqsEndpoint **(required)**
            - `url` — string **(required)**
            - `key` — string **(required)**
            - `secret` — string **(required)**
    - `capabilities` — array
      - _array of_ `VoiceBotCapability`
        - _oneOf_ — exactly one of:
          - **`tool`**
            - `tool` — VoiceBotCapabilityTool **(required)**
              - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
              - `variables` — array
                - _(nesting depth limit — see `VoiceBotToolVariable` in the Schemas appendix)_
              - `startMessage` — string — Message spoken when the tool call starts. Spoken in every language of the call while `startMessages` is absent or empty; not consulted once `startMessages` carries any entry.
              - `startMessages` — array — Per-language start messages. When present and non-empty, the entry for the call's current language is spoken and `startMessage` is not consulted; a language with no entry is silent. When absent or empty, `startMessage` is spoken as before. On a call with no effective speech configuration — no configured languages, or a PBX below protocol 2 — `startMessage` is spoken regardless, because there is no current language to choose by.
                - _(nesting depth limit — see `VoiceBotSpokenPhrase` in the Schemas appendix)_
              - `pipeline` — VoiceBotCapabilityToolPipeline
                - _(nesting depth limit — see `VoiceBotCapabilityToolPipeline` in the Schemas appendix)_
              - `annotations` — array
                - _(nesting depth limit — see `VoiceBotToolAnnotation` in the Schemas appendix)_
          - **`kb`**
            - `kb` — VoiceBotKnowledgeBase **(required)**
              - `knowledgeBaseId` — string
              - `instructions` — string — Additional instructions for when the bot should use this knowledge base.
              - `searchStrategy` — string _(enum: `bm25`, `vector`, `hybrid`)_
              - `searchThreshold` — string _(enum: `low`, `medium`, `high`)_
              - `searchLimit` — number — Maximum number of search results returned by this knowledge base capability. _(min=1; max=50)_
              - `annotations` — array
                - _(nesting depth limit — see `VoiceBotToolAnnotation` in the Schemas appendix)_
    - `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `401`, `403`

#### `PUT` `/v2/voicebots/bots/{botId}`

Updates the configuration of an existing voice bot with new settings.

- operationId: `UpdateVoiceBot`
- **Scopes**: `voicebots:UpdateVoiceBot`
- **Parameters**
  - `botId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string
- **Request body** (`application/json` — `UpdateVoiceBotRequestContent`) **(required)**
  - `name` — string **(required)** _(minLen=3; maxLen=255)_
  - `category` — string — Category of the bot _(minLen=1; maxLen=128)_
  - `message` — string — The initial message that will be played at the start of the session.
  - `pipeline` — VoiceBotPipelineSettings
    - `interuptionsEnabled` — boolean — If enabled the user can interrupt the the bot playback.
    - `maximumDuration` — number — The maximum number of seconds a call will last.
    - `maximumDurationAction` — union
      - _oneOf_ — exactly one of:
        - **`hangup`**
          - `hangup` — VoiceBotTerminateHangupAction **(required)**
        - **`transfer`**
          - `transfer` — VoiceBotTerminateTransferAction **(required)**
            - `context` — string **(required)**
            - `extension` — string **(required)**
    - `silenceTimeout` — number — How long to wait before a call is automatically ended due to inactivity.
    - `silenceTimeoutAction` — union
      - _oneOf_ — exactly one of:
        - **`hangup`**
          - `hangup` — VoiceBotTerminateHangupAction **(required)**
        - **`transfer`**
          - `transfer` — VoiceBotTerminateTransferAction **(required)**
            - `context` — string **(required)**
            - `extension` — string **(required)**
    - `endCallEnabled` — boolean — If enabled the bot can hangup the call.
    - `endCallPhases` — string — A list of phases separated by comma, which will end the call matched.
  - `speech` — VoiceBotSpeechSettings — Speech configuration. When present it wins over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the exception.
    - `languages` — array **(required)** — Configured languages. The @length bound is a storage ceiling; the real cap is the recogniser's own candidate limit, enforced in the service. _(minItems=1; maxItems=10)_
      - _array of_ `VoiceBotLanguage`
        - `code` — string **(required)** — BCP-47 code with locale, e.g. 'en-US'. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
        - `voice` — string **(required)** — Voice this language speaks with, as a URI — provider, voice id, synthesis parameters and, where the company uses its own provider account, its `apiKey` query parameter. See VoiceBotVoiceUri. PER LANGUAGE, and that is the whole reason the member is here rather than on the settings above: provider quality is not uniform across languages, a voice id belongs to exactly one provider, and a bot-wide provider made changing it invalidate every configured voice at once. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
        - `greeting` — string — Initial phrase for this language. Absent or empty means the agent says nothing and waits — it does NOT fall back to the agent-level message, which would speak one language's text in another language's voice.
        - `isDefault` — boolean — Marks the language a caller hears when their own matches nothing configured. THE FULL RESOLUTION ORDER, since a client author reading only this contract cannot otherwise find it: an exact match on the call's language, then a match on its primary subtag (`fr` finds `fr-FR`), then the language marked here, then a language whose primary subtag is `en`, then the first entry in the list. Marked is consulted BEFORE the English step, so a record with none marked resolves exactly as it did before this member existed. English is deliberate rather than arbitrary — it is the language a caller the agent was not built for is likeliest to understand — and the last step exists only to keep the rule total, which is why list order should not be treated as configuration. At most one language may carry it. A record with two — reachable through the API or the CLI, where no form prevents it — resolves to the first marked one in list order, because refusing a call over configuration drift is worse than serving it and saying so in the trace.
        - `pronunciations` — array — Pronunciation rules for one language. BOUNDED, and the bound is not decoration. `applyPronunciations` compiles every rule of a language into a SINGLE alternating regular expression, so the cost is the pattern's total size: measured against the real escaping and matching logic, 1,000 rules cost ~0.9 s of CPU per synthesized sentence, 5,000 cost ~4.9 s, and around 10,000 `new RegExp` throws V8's pattern-size error outright — from a call site outside the surrounding `try`, so a 500 rather than a degraded reply. Stored on a bot, that made every utterance of the agent fail. 200 is far above any real use — a product glossary is a handful of names — and far below where either cost begins. Found by a security review. NO LOWER BOUND on `phrase` or `as`, deliberately. Both consoles add an EMPTY rule row the moment someone clicks 'Add pronunciation', so a `min: 1` would make saving an agent with a half-typed row fail entirely — and the runtime already ignores a rule with no phrase. Dropping blank rows belongs in the consoles' save filters, not in a refusal here. _(maxItems=200)_
          - _array of_ `VoiceBotPronunciation`
            - `phrase` — string **(required)** — The written form to replace. Bounded because every rule is compiled into ONE regular expression — see the list below. _(maxLen=200)_
            - `as` — string **(required)** — Respelling (ALIAS) or phonetic transcription (IPA). _(maxLen=200)_
            - `encoding` — string _(enum: `alias`, `ipa`)_
    - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in its own language's voice, provider account and pronunciation rules. Languages with an empty first message, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
    - `transcription` — VoiceBotTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
      - `engine` — string — Recogniser to transcribe the caller with. Absent resolves to the platform default ('aws://transcribe' today), resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
      - `autoDetect` — boolean — Identify the caller's language per utterance and switch voice and reply language mid-call. HERE RATHER THAN ON `VoiceBotSpeechSettings`, because identifying a language is something the RECOGNISER does: it becomes identify-multiple-languages plus language-options on the recognition stream, and nothing about synthesis reads it. Requires at least two configured languages and a recogniser that can identify them; the server clamps it to false otherwise, because forwarding true with a single candidate makes Amazon reject the stream outright.
  - `backgroundSound` — VoiceBotBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT rather than a loose name on the bot, matching `wildix.wilma.agents`: it is one switchable call behaviour, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
    - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
    - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
  - `endpoint` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`llm`**
        - `llm` — VoiceBotLlmEndpoint **(required)**
          - `prompt` — string **(required)** _(maxLen=40000)_
          - `model` — string — The AI model to use for generating responses. If not specified, uses the default model. _(default=default; pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
          - `guidelines` — array
            - _array of_ `string`
          - `metadata` — VoiceBotPromptMetadata
            - `userName` — VoiceBotPromptMetadataEnabled
              - `enabled` — boolean **(required)** — Whether this metadata field is enabled _(default=True)_
            - `userPhoneNumber` — VoiceBotPromptMetadataEnabled
              - `enabled` — boolean **(required)** — Whether this metadata field is enabled _(default=True)_
            - `userEmail` — VoiceBotPromptMetadataDisabled
              - `enabled` — boolean **(required)** — Whether this metadata field is enabled _(default=False)_
            - `userCompany` — VoiceBotPromptMetadataDisabled
              - `enabled` — boolean **(required)** — Whether this metadata field is enabled _(default=False)_
            - `time` — VoiceBotPromptMetadataTime
              - `enabled` — boolean **(required)** — Whether this metadata field is enabled _(default=False)_
              - `timeZone` — string **(required)** — Timezone for time formatting (e.g., 'Europe/Rome', 'UTC') _(default=UTC)_
          - `embeddedTools` — array — Embedded functions to use within voice session.
            - _array of_ `VoiceBotEmbeddedTool`
              - `type` — string **(required)** _(enum: `HANGUP`, `TRANSFER`, `DELEGATE`, `WAIT`)_
              - `name` — string **(required)**
              - `parameters` — any — The parameters the functions accepts.
              - `annotations` — array
                - _(nesting depth limit — see `VoiceBotToolAnnotation` in the Schemas appendix)_
          - `tools` — array — Custom tools to be used within voice session.
            - _array of_ `VoiceBotTool`
              - `type` — string **(required)** _(enum: `function`)_
              - `function` — VoiceBotFunctionDefinition
                - _(nesting depth limit — see `VoiceBotFunctionDefinition` in the Schemas appendix)_
              - `annotations` — array
                - _(nesting depth limit — see `VoiceBotToolAnnotation` in the Schemas appendix)_
          - `capabilities` — array
            - _array of_ `VoiceBotCapability`
              - _oneOf_ — exactly one of:
                - **`tool`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`kb`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `variables` — array — Variables such as dialplan variables that can be used in the bot.
            - _array of_ `VoiceBotVariable`
              - `name` — string **(required)** _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
      - **`dialogflowCx`**
        - `dialogflowCx` — BotDialogflowCxEndpoint **(required)**
          - `credentials` — any **(required)** — Dialogflow Service Account Credentials
          - `agent` — string **(required)** — Dialogflow Agent Id (example - 88ff4635-0852-4f97-ae44-b19ae9fa6ea1
          - `location` — string **(required)** — Dialogflow Agent Region (example: europe-west3)
          - `language` — string **(required)** — Language
      - **`openAiAssistant`**
        - `openAiAssistant` — BotOpenAiAssistantEndpoint **(required)**
          - `key` — string **(required)**
          - `assistantId` — string **(required)**
      - **`webhook`**
        - `webhook` — BotWebhookEndpoint **(required)**
          - `url` — string **(required)**
          - `secret` — string **(required)**
      - **`sqs`**
        - `sqs` — BotSqsEndpoint **(required)**
          - `url` — string **(required)**
          - `key` — string **(required)**
          - `secret` — string **(required)**
  - `capabilities` — array
    - _array of_ `VoiceBotCapability`
      - _oneOf_ — exactly one of:
        - **`tool`**
          - `tool` — VoiceBotCapabilityTool **(required)**
            - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
            - `variables` — array
              - _array of_ `VoiceBotToolVariable`
                - _(nesting depth limit — see `VoiceBotToolVariable` in the Schemas appendix)_
            - `startMessage` — string — Message spoken when the tool call starts. Spoken in every language of the call while `startMessages` is absent or empty; not consulted once `startMessages` carries any entry.
            - `startMessages` — array — Per-language start messages. When present and non-empty, the entry for the call's current language is spoken and `startMessage` is not consulted; a language with no entry is silent. When absent or empty, `startMessage` is spoken as before. On a call with no effective speech configuration — no configured languages, or a PBX below protocol 2 — `startMessage` is spoken regardless, because there is no current language to choose by.
              - _array of_ `VoiceBotSpokenPhrase`
                - _(nesting depth limit — see `VoiceBotSpokenPhrase` in the Schemas appendix)_
            - `pipeline` — VoiceBotCapabilityToolPipeline
              - `type` — string _(enum: `blocking_request`, `blocking_request_guided`, `async_request`, `async_request_guided`)_
              - `instructions` — string — Instructions for generating a reply when using guided pipeline types. Use {{response}} to reference the tool response.
            - `annotations` — array
              - _array of_ `VoiceBotToolAnnotation`
                - _(nesting depth limit — see `VoiceBotToolAnnotation` in the Schemas appendix)_
        - **`kb`**
          - `kb` — VoiceBotKnowledgeBase **(required)**
            - `knowledgeBaseId` — string
            - `instructions` — string — Additional instructions for when the bot should use this knowledge base.
            - `searchStrategy` — string _(enum: `bm25`, `vector`, `hybrid`)_
            - `searchThreshold` — string _(enum: `low`, `medium`, `high`)_
            - `searchLimit` — number — Maximum number of search results returned by this knowledge base capability. _(min=1; max=50)_
            - `annotations` — array
              - _array of_ `VoiceBotToolAnnotation`
                - _(nesting depth limit — see `VoiceBotToolAnnotation` in the Schemas appendix)_
  - `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
- **Response 200** (`UpdateVoiceBotResponseContent`)
  - `bot` — VoiceBot **(required)**
    - `name` — string **(required)** _(minLen=3; maxLen=255)_
    - `category` — string — Category of the bot _(minLen=1; maxLen=128)_
    - `message` — string — The initial message that will be played at the start of the session.
    - `pipeline` — VoiceBotPipelineSettings
      - `interuptionsEnabled` — boolean — If enabled the user can interrupt the the bot playback.
      - `maximumDuration` — number — The maximum number of seconds a call will last.
      - `maximumDurationAction` — union
        - _oneOf_ — exactly one of:
          - **`hangup`**
            - `hangup` — VoiceBotTerminateHangupAction **(required)**
          - **`transfer`**
            - `transfer` — VoiceBotTerminateTransferAction **(required)**
              - `context` — string **(required)**
              - `extension` — string **(required)**
      - `silenceTimeout` — number — How long to wait before a call is automatically ended due to inactivity.
      - `silenceTimeoutAction` — union
        - _oneOf_ — exactly one of:
          - **`hangup`**
            - `hangup` — VoiceBotTerminateHangupAction **(required)**
          - **`transfer`**
            - `transfer` — VoiceBotTerminateTransferAction **(required)**
              - `context` — string **(required)**
              - `extension` — string **(required)**
      - `endCallEnabled` — boolean — If enabled the bot can hangup the call.
      - `endCallPhases` — string — A list of phases separated by comma, which will end the call matched.
    - `speech` — VoiceBotSpeechSettings — Speech configuration. When present it wins over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the exception.
      - `languages` — array **(required)** — Configured languages. The @length bound is a storage ceiling; the real cap is the recogniser's own candidate limit, enforced in the service. _(minItems=1; maxItems=10)_
        - _array of_ `VoiceBotLanguage`
          - `code` — string **(required)** — BCP-47 code with locale, e.g. 'en-US'. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
          - `voice` — string **(required)** — Voice this language speaks with, as a URI — provider, voice id, synthesis parameters and, where the company uses its own provider account, its `apiKey` query parameter. See VoiceBotVoiceUri. PER LANGUAGE, and that is the whole reason the member is here rather than on the settings above: provider quality is not uniform across languages, a voice id belongs to exactly one provider, and a bot-wide provider made changing it invalidate every configured voice at once. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
          - `greeting` — string — Initial phrase for this language. Absent or empty means the agent says nothing and waits — it does NOT fall back to the agent-level message, which would speak one language's text in another language's voice.
          - `isDefault` — boolean — Marks the language a caller hears when their own matches nothing configured. THE FULL RESOLUTION ORDER, since a client author reading only this contract cannot otherwise find it: an exact match on the call's language, then a match on its primary subtag (`fr` finds `fr-FR`), then the language marked here, then a language whose primary subtag is `en`, then the first entry in the list. Marked is consulted BEFORE the English step, so a record with none marked resolves exactly as it did before this member existed. English is deliberate rather than arbitrary — it is the language a caller the agent was not built for is likeliest to understand — and the last step exists only to keep the rule total, which is why list order should not be treated as configuration. At most one language may carry it. A record with two — reachable through the API or the CLI, where no form prevents it — resolves to the first marked one in list order, because refusing a call over configuration drift is worse than serving it and saying so in the trace.
          - `pronunciations` — array — Pronunciation rules for one language. BOUNDED, and the bound is not decoration. `applyPronunciations` compiles every rule of a language into a SINGLE alternating regular expression, so the cost is the pattern's total size: measured against the real escaping and matching logic, 1,000 rules cost ~0.9 s of CPU per synthesized sentence, 5,000 cost ~4.9 s, and around 10,000 `new RegExp` throws V8's pattern-size error outright — from a call site outside the surrounding `try`, so a 500 rather than a degraded reply. Stored on a bot, that made every utterance of the agent fail. 200 is far above any real use — a product glossary is a handful of names — and far below where either cost begins. Found by a security review. NO LOWER BOUND on `phrase` or `as`, deliberately. Both consoles add an EMPTY rule row the moment someone clicks 'Add pronunciation', so a `min: 1` would make saving an agent with a half-typed row fail entirely — and the runtime already ignores a rule with no phrase. Dropping blank rows belongs in the consoles' save filters, not in a refusal here. _(maxItems=200)_
            - _array of_ `VoiceBotPronunciation`
              - _(nesting depth limit — see `VoiceBotPronunciation` in the Schemas appendix)_
      - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in its own language's voice, provider account and pronunciation rules. Languages with an empty first message, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
      - `transcription` — VoiceBotTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
        - `engine` — string — Recogniser to transcribe the caller with. Absent resolves to the platform default ('aws://transcribe' today), resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
        - `autoDetect` — boolean — Identify the caller's language per utterance and switch voice and reply language mid-call. HERE RATHER THAN ON `VoiceBotSpeechSettings`, because identifying a language is something the RECOGNISER does: it becomes identify-multiple-languages plus language-options on the recognition stream, and nothing about synthesis reads it. Requires at least two configured languages and a recogniser that can identify them; the server clamps it to false otherwise, because forwarding true with a single candidate makes Amazon reject the stream outright.
    - `backgroundSound` — VoiceBotBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT rather than a loose name on the bot, matching `wildix.wilma.agents`: it is one switchable call behaviour, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
      - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
      - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
    - `endpoint` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`llm`**
          - `llm` — VoiceBotLlmEndpoint **(required)**
            - `prompt` — string **(required)** _(maxLen=40000)_
            - `model` — string — The AI model to use for generating responses. If not specified, uses the default model. _(default=default; pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
            - `guidelines` — array
              - _array of_ `string`
            - `metadata` — VoiceBotPromptMetadata
              - `userName` — VoiceBotPromptMetadataEnabled
                - _(nesting depth limit — see `VoiceBotPromptMetadataEnabled` in the Schemas appendix)_
              - `userPhoneNumber` — VoiceBotPromptMetadataEnabled
                - _(nesting depth limit — see `VoiceBotPromptMetadataEnabled` in the Schemas appendix)_
              - `userEmail` — VoiceBotPromptMetadataDisabled
                - _(nesting depth limit — see `VoiceBotPromptMetadataDisabled` in the Schemas appendix)_
              - `userCompany` — VoiceBotPromptMetadataDisabled
                - _(nesting depth limit — see `VoiceBotPromptMetadataDisabled` in the Schemas appendix)_
              - `time` — VoiceBotPromptMetadataTime
                - _(nesting depth limit — see `VoiceBotPromptMetadataTime` in the Schemas appendix)_
            - `embeddedTools` — array — Embedded functions to use within voice session.
              - _array of_ `VoiceBotEmbeddedTool`
                - _(nesting depth limit — see `VoiceBotEmbeddedTool` in the Schemas appendix)_
            - `tools` — array — Custom tools to be used within voice session.
              - _array of_ `VoiceBotTool`
                - _(nesting depth limit — see `VoiceBotTool` in the Schemas appendix)_
            - `capabilities` — array
              - _array of_ `VoiceBotCapability`
                - _(nesting depth limit — see `VoiceBotCapability` in the Schemas appendix)_
            - `variables` — array — Variables such as dialplan variables that can be used in the bot.
              - _array of_ `VoiceBotVariable`
                - _(nesting depth limit — see `VoiceBotVariable` in the Schemas appendix)_
        - **`dialogflowCx`**
          - `dialogflowCx` — BotDialogflowCxEndpoint **(required)**
            - `credentials` — any **(required)** — Dialogflow Service Account Credentials
            - `agent` — string **(required)** — Dialogflow Agent Id (example - 88ff4635-0852-4f97-ae44-b19ae9fa6ea1
            - `location` — string **(required)** — Dialogflow Agent Region (example: europe-west3)
            - `language` — string **(required)** — Language
        - **`openAiAssistant`**
          - `openAiAssistant` — BotOpenAiAssistantEndpoint **(required)**
            - `key` — string **(required)**
            - `assistantId` — string **(required)**
        - **`webhook`**
          - `webhook` — BotWebhookEndpoint **(required)**
            - `url` — string **(required)**
            - `secret` — string **(required)**
        - **`sqs`**
          - `sqs` — BotSqsEndpoint **(required)**
            - `url` — string **(required)**
            - `key` — string **(required)**
            - `secret` — string **(required)**
    - `capabilities` — array
      - _array of_ `VoiceBotCapability`
        - _oneOf_ — exactly one of:
          - **`tool`**
            - `tool` — VoiceBotCapabilityTool **(required)**
              - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
              - `variables` — array
                - _(nesting depth limit — see `VoiceBotToolVariable` in the Schemas appendix)_
              - `startMessage` — string — Message spoken when the tool call starts. Spoken in every language of the call while `startMessages` is absent or empty; not consulted once `startMessages` carries any entry.
              - `startMessages` — array — Per-language start messages. When present and non-empty, the entry for the call's current language is spoken and `startMessage` is not consulted; a language with no entry is silent. When absent or empty, `startMessage` is spoken as before. On a call with no effective speech configuration — no configured languages, or a PBX below protocol 2 — `startMessage` is spoken regardless, because there is no current language to choose by.
                - _(nesting depth limit — see `VoiceBotSpokenPhrase` in the Schemas appendix)_
              - `pipeline` — VoiceBotCapabilityToolPipeline
                - _(nesting depth limit — see `VoiceBotCapabilityToolPipeline` in the Schemas appendix)_
              - `annotations` — array
                - _(nesting depth limit — see `VoiceBotToolAnnotation` in the Schemas appendix)_
          - **`kb`**
            - `kb` — VoiceBotKnowledgeBase **(required)**
              - `knowledgeBaseId` — string
              - `instructions` — string — Additional instructions for when the bot should use this knowledge base.
              - `searchStrategy` — string _(enum: `bm25`, `vector`, `hybrid`)_
              - `searchThreshold` — string _(enum: `low`, `medium`, `high`)_
              - `searchLimit` — number — Maximum number of search results returned by this knowledge base capability. _(min=1; max=50)_
              - `annotations` — array
                - _(nesting depth limit — see `VoiceBotToolAnnotation` in the Schemas appendix)_
    - `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `401`, `403`, `404`

#### `DELETE` `/v2/voicebots/bots/{botId}`

Deletes an existing voice bot and all its associated data.

- operationId: `DeleteVoiceBot`
- **Scopes**: `voicebots:DeleteVoiceBot`
- **Parameters**
  - `botId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string
- Errors: `400`, `403`

#### `GET` `/v2/voicebots/names`

Retrieves a list of voice bot names and basic information for the specified company.

- operationId: `ListVoiceBotsNames`
- **Scopes**: `voicebots:ListVoiceBotsNames`, `voicebots:read`
- **Parameters**
  - `company` (query) — string
- **Response 200** (`ListVoiceBotsNamesResponseContent`)
  - `bots` — array **(required)**
    - _array of_ `VoiceBotInfo`
      - `id` — string **(required)** _(minLen=12; maxLen=12)_
      - `name` — string **(required)** _(minLen=3; maxLen=255)_
      - `speechConfigured` — boolean — Whether the voice channel has at least one configured speech language. A dialplan form partitions its application lists on this, so the answer has to travel with the list rather than cost one lookup per entry — it is the reason this member exists and the reason removing it broke that form. Absent is read as false.
- Errors: `400`, `403`

### Other

#### `GET` `/v2/voicebots/bots/{botId}`

Retrieves details of a specific voice bot by its unique identifier.

- operationId: `GetVoiceBot`
- **Scopes**: `voicebots:GetVoiceBot`, `voicebots:read`
- **Parameters**
  - `botId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string
- **Response 200** (`GetVoiceBotResponseContent`)
  - `bot` — VoiceBot **(required)**
    - `name` — string **(required)** _(minLen=3; maxLen=255)_
    - `category` — string — Category of the bot _(minLen=1; maxLen=128)_
    - `message` — string — The initial message that will be played at the start of the session.
    - `pipeline` — VoiceBotPipelineSettings
      - `interuptionsEnabled` — boolean — If enabled the user can interrupt the the bot playback.
      - `maximumDuration` — number — The maximum number of seconds a call will last.
      - `maximumDurationAction` — union
        - _oneOf_ — exactly one of:
          - **`hangup`**
            - `hangup` — VoiceBotTerminateHangupAction **(required)**
          - **`transfer`**
            - `transfer` — VoiceBotTerminateTransferAction **(required)**
              - `context` — string **(required)**
              - `extension` — string **(required)**
      - `silenceTimeout` — number — How long to wait before a call is automatically ended due to inactivity.
      - `silenceTimeoutAction` — union
        - _oneOf_ — exactly one of:
          - **`hangup`**
            - `hangup` — VoiceBotTerminateHangupAction **(required)**
          - **`transfer`**
            - `transfer` — VoiceBotTerminateTransferAction **(required)**
              - `context` — string **(required)**
              - `extension` — string **(required)**
      - `endCallEnabled` — boolean — If enabled the bot can hangup the call.
      - `endCallPhases` — string — A list of phases separated by comma, which will end the call matched.
    - `speech` — VoiceBotSpeechSettings — Speech configuration. When present it wins over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the exception.
      - `languages` — array **(required)** — Configured languages. The @length bound is a storage ceiling; the real cap is the recogniser's own candidate limit, enforced in the service. _(minItems=1; maxItems=10)_
        - _array of_ `VoiceBotLanguage`
          - `code` — string **(required)** — BCP-47 code with locale, e.g. 'en-US'. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
          - `voice` — string **(required)** — Voice this language speaks with, as a URI — provider, voice id, synthesis parameters and, where the company uses its own provider account, its `apiKey` query parameter. See VoiceBotVoiceUri. PER LANGUAGE, and that is the whole reason the member is here rather than on the settings above: provider quality is not uniform across languages, a voice id belongs to exactly one provider, and a bot-wide provider made changing it invalidate every configured voice at once. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
          - `greeting` — string — Initial phrase for this language. Absent or empty means the agent says nothing and waits — it does NOT fall back to the agent-level message, which would speak one language's text in another language's voice.
          - `isDefault` — boolean — Marks the language a caller hears when their own matches nothing configured. THE FULL RESOLUTION ORDER, since a client author reading only this contract cannot otherwise find it: an exact match on the call's language, then a match on its primary subtag (`fr` finds `fr-FR`), then the language marked here, then a language whose primary subtag is `en`, then the first entry in the list. Marked is consulted BEFORE the English step, so a record with none marked resolves exactly as it did before this member existed. English is deliberate rather than arbitrary — it is the language a caller the agent was not built for is likeliest to understand — and the last step exists only to keep the rule total, which is why list order should not be treated as configuration. At most one language may carry it. A record with two — reachable through the API or the CLI, where no form prevents it — resolves to the first marked one in list order, because refusing a call over configuration drift is worse than serving it and saying so in the trace.
          - `pronunciations` — array — Pronunciation rules for one language. BOUNDED, and the bound is not decoration. `applyPronunciations` compiles every rule of a language into a SINGLE alternating regular expression, so the cost is the pattern's total size: measured against the real escaping and matching logic, 1,000 rules cost ~0.9 s of CPU per synthesized sentence, 5,000 cost ~4.9 s, and around 10,000 `new RegExp` throws V8's pattern-size error outright — from a call site outside the surrounding `try`, so a 500 rather than a degraded reply. Stored on a bot, that made every utterance of the agent fail. 200 is far above any real use — a product glossary is a handful of names — and far below where either cost begins. Found by a security review. NO LOWER BOUND on `phrase` or `as`, deliberately. Both consoles add an EMPTY rule row the moment someone clicks 'Add pronunciation', so a `min: 1` would make saving an agent with a half-typed row fail entirely — and the runtime already ignores a rule with no phrase. Dropping blank rows belongs in the consoles' save filters, not in a refusal here. _(maxItems=200)_
            - _array of_ `VoiceBotPronunciation`
              - _(nesting depth limit — see `VoiceBotPronunciation` in the Schemas appendix)_
      - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in its own language's voice, provider account and pronunciation rules. Languages with an empty first message, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
      - `transcription` — VoiceBotTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
        - `engine` — string — Recogniser to transcribe the caller with. Absent resolves to the platform default ('aws://transcribe' today), resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
        - `autoDetect` — boolean — Identify the caller's language per utterance and switch voice and reply language mid-call. HERE RATHER THAN ON `VoiceBotSpeechSettings`, because identifying a language is something the RECOGNISER does: it becomes identify-multiple-languages plus language-options on the recognition stream, and nothing about synthesis reads it. Requires at least two configured languages and a recogniser that can identify them; the server clamps it to false otherwise, because forwarding true with a single candidate makes Amazon reject the stream outright.
    - `backgroundSound` — VoiceBotBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT rather than a loose name on the bot, matching `wildix.wilma.agents`: it is one switchable call behaviour, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
      - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
      - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
    - `endpoint` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`llm`**
          - `llm` — VoiceBotLlmEndpoint **(required)**
            - `prompt` — string **(required)** _(maxLen=40000)_
            - `model` — string — The AI model to use for generating responses. If not specified, uses the default model. _(default=default; pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
            - `guidelines` — array
              - _array of_ `string`
            - `metadata` — VoiceBotPromptMetadata
              - `userName` — VoiceBotPromptMetadataEnabled
                - _(nesting depth limit — see `VoiceBotPromptMetadataEnabled` in the Schemas appendix)_
              - `userPhoneNumber` — VoiceBotPromptMetadataEnabled
                - _(nesting depth limit — see `VoiceBotPromptMetadataEnabled` in the Schemas appendix)_
              - `userEmail` — VoiceBotPromptMetadataDisabled
                - _(nesting depth limit — see `VoiceBotPromptMetadataDisabled` in the Schemas appendix)_
              - `userCompany` — VoiceBotPromptMetadataDisabled
                - _(nesting depth limit — see `VoiceBotPromptMetadataDisabled` in the Schemas appendix)_
              - `time` — VoiceBotPromptMetadataTime
                - _(nesting depth limit — see `VoiceBotPromptMetadataTime` in the Schemas appendix)_
            - `embeddedTools` — array — Embedded functions to use within voice session.
              - _array of_ `VoiceBotEmbeddedTool`
                - _(nesting depth limit — see `VoiceBotEmbeddedTool` in the Schemas appendix)_
            - `tools` — array — Custom tools to be used within voice session.
              - _array of_ `VoiceBotTool`
                - _(nesting depth limit — see `VoiceBotTool` in the Schemas appendix)_
            - `capabilities` — array
              - _array of_ `VoiceBotCapability`
                - _(nesting depth limit — see `VoiceBotCapability` in the Schemas appendix)_
            - `variables` — array — Variables such as dialplan variables that can be used in the bot.
              - _array of_ `VoiceBotVariable`
                - _(nesting depth limit — see `VoiceBotVariable` in the Schemas appendix)_
        - **`dialogflowCx`**
          - `dialogflowCx` — BotDialogflowCxEndpoint **(required)**
            - `credentials` — any **(required)** — Dialogflow Service Account Credentials
            - `agent` — string **(required)** — Dialogflow Agent Id (example - 88ff4635-0852-4f97-ae44-b19ae9fa6ea1
            - `location` — string **(required)** — Dialogflow Agent Region (example: europe-west3)
            - `language` — string **(required)** — Language
        - **`openAiAssistant`**
          - `openAiAssistant` — BotOpenAiAssistantEndpoint **(required)**
            - `key` — string **(required)**
            - `assistantId` — string **(required)**
        - **`webhook`**
          - `webhook` — BotWebhookEndpoint **(required)**
            - `url` — string **(required)**
            - `secret` — string **(required)**
        - **`sqs`**
          - `sqs` — BotSqsEndpoint **(required)**
            - `url` — string **(required)**
            - `key` — string **(required)**
            - `secret` — string **(required)**
    - `capabilities` — array
      - _array of_ `VoiceBotCapability`
        - _oneOf_ — exactly one of:
          - **`tool`**
            - `tool` — VoiceBotCapabilityTool **(required)**
              - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
              - `variables` — array
                - _(nesting depth limit — see `VoiceBotToolVariable` in the Schemas appendix)_
              - `startMessage` — string — Message spoken when the tool call starts. Spoken in every language of the call while `startMessages` is absent or empty; not consulted once `startMessages` carries any entry.
              - `startMessages` — array — Per-language start messages. When present and non-empty, the entry for the call's current language is spoken and `startMessage` is not consulted; a language with no entry is silent. When absent or empty, `startMessage` is spoken as before. On a call with no effective speech configuration — no configured languages, or a PBX below protocol 2 — `startMessage` is spoken regardless, because there is no current language to choose by.
                - _(nesting depth limit — see `VoiceBotSpokenPhrase` in the Schemas appendix)_
              - `pipeline` — VoiceBotCapabilityToolPipeline
                - _(nesting depth limit — see `VoiceBotCapabilityToolPipeline` in the Schemas appendix)_
              - `annotations` — array
                - _(nesting depth limit — see `VoiceBotToolAnnotation` in the Schemas appendix)_
          - **`kb`**
            - `kb` — VoiceBotKnowledgeBase **(required)**
              - `knowledgeBaseId` — string
              - `instructions` — string — Additional instructions for when the bot should use this knowledge base.
              - `searchStrategy` — string _(enum: `bm25`, `vector`, `hybrid`)_
              - `searchThreshold` — string _(enum: `low`, `medium`, `high`)_
              - `searchLimit` — number — Maximum number of search results returned by this knowledge base capability. _(min=1; max=50)_
              - `annotations` — array
                - _(nesting depth limit — see `VoiceBotToolAnnotation` in the Schemas appendix)_
    - `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`

#### `POST` `/v2/voicebots/describe`

Utility method to describe available events for websocket and webhook events.

- operationId: `DescribeEvent`
- **Scopes**: `voicebots:DescribeEvent`
- **Response 200** (`DescribeEventResponseContent`)
  - `SessionStartedWebsocketEvent` — SessionStartedWebsocketEvent
    - `type` — string **(required)** _(default=event)_
    - `event` — SessionStartedWebsocketEventData **(required)**
      - `type` — object **(required)**
      - `botId` — string **(required)**
      - `botName` — string **(required)**
      - `category` — string
      - `groupId` — string
      - `speech` — VoiceBotSpeechPayload — Recognition intent for the call, sent on `started` at protocol version >= 2. Not recogniser parameters: the PBX translates it into its provider's API. `engine` is always concrete and `autoDetect` is already clamped by the server, because forwarding true with a single candidate makes Amazon reject the stream outright.
        - `engine` — string **(required)** — Concrete recogniser URI, resolved from the bot or from the platform default; never absent. See VoiceBotTranscriptionUri. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
        - `languages` — array **(required)** — Every configured language, as candidates for identification.
          - _array of_ `string`
        - `preferredLanguage` — string **(required)** — The language the call starts in, resolved from the channel. Always a member of `languages`. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
        - `autoDetect` — boolean **(required)**
      - `backgroundSound` — string — Music-on-hold class the PBX should play under the call as ambient background. A BARE NAME, not the configuration object `VoiceBotBackgroundSoundSettings`: this is the RESOLVED outcome. The server has already applied `enabled` and the class default, so the PBX gets a name to play or nothing at all and needs no resolution rule of its own. TOP LEVEL, NOT INSIDE `speech`, because it is not recognition intent and must not inherit `speech`'s conditions: a call with no configured languages carries no `speech` payload and can still have background audio. ABSENT MEANS OFF, and absence is the only way to say it — there is no value for 'none'. A bot whose administrator never touched the setting sends nothing here, which is exactly what every call sent before it existed, so the PBX needs no new case. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
      - `time` — number **(required)**
  - `TranscriptionWebsocketEvent` — TranscriptionWebsocketEvent
    - `type` — string **(required)** _(default=event)_
    - `event` — TranscriptionEvent **(required)**
      - `type` — object **(required)**
      - `id` — string **(required)**
      - `text` — string **(required)**
      - `confidence` — number — Transcription confidence score (accuracy level) in range from 0.0 to 1.0. Value -1.0 indicates confidence is unavailable. _(format=double; min=-1; max=1)_
      - `final` — boolean
      - `language` — string — Language the recogniser identified for this chunk. Recorded in the trace only; drives no behavior. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `time` — number **(required)**
  - `ReplyWebsocketEvent` — ReplyWebsocketEvent
    - `type` — string **(required)** _(default=event)_
    - `event` — ReplyEvent **(required)**
      - `type` — object **(required)**
      - `id` — string **(required)**
      - `text` — string **(required)**
      - `language` — string — Language the recogniser identified for this completed utterance; drives the language switch. When several languages are reported inside one utterance the PBX sends the last labelled segment's. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `confidence` — number — Aggregated transcription confidence of the phrase this reply was built from, weighted by word count over the transcription chunks that carry a confidence value. Absent when no chunk had one, for example on DTMF input. _(format=double; min=-1; max=1)_
      - `startTime` — number **(required)**
      - `endTime` — number **(required)**
  - `PlaybackWebsocketEvent` — PlaybackWebsocketEvent
    - `type` — string **(required)** _(default=event)_
    - `event` — PlaybackEvent **(required)**
      - `type` — object **(required)**
      - `replyId` — string **(required)**
      - `text` — string **(required)**
      - `complete` — boolean **(required)**
      - `startTime` — number **(required)**
      - `endTime` — number
  - `InterruptionWebsocketEvent` — InterruptionWebsocketEvent
    - `type` — string **(required)** _(default=event)_
    - `event` — InterruptionEvent **(required)**
      - `type` — object **(required)**
      - `replyId` — string **(required)**
      - `playedText` — string **(required)**
      - `originalText` — string **(required)**
      - `time` — number **(required)**
  - `CompleteWebsocketEvent` — CompleteWebsocketEvent
    - `type` — string **(required)** _(default=event)_
    - `event` — CompleteEvent **(required)**
      - `type` — object **(required)**
      - `reason` — string **(required)**
      - `time` — number **(required)**
  - `SayWebsocketCommand` — SayWebsocketCommand
    - `type` — string **(required)** _(default=command)_
    - `command` — SayWebsocketCommandData **(required)**
      - `text` — string **(required)**
      - `replyId` — string **(required)**
      - `interruptible` — boolean
      - `voice` — string — Bare Amazon Polly voice id, e.g. 'Joanna' — NOT a URI. The PBX consumes this verbatim as the AMI `Voice=` action parameter, so it takes exactly what Polly names the voice, with the `amazon_polly://` scheme and any query parameters already stripped by whoever builds this command out of the bot's stored `VoiceBotVoiceUri`. Set only for a provider whose synthesis runs ON THE PBX (Amazon Polly); ElevenLabs and Google are synthesized in the cloud and streamed as PCM through `play` instead, and leave this absent. _(pattern=^[A-Za-z0-9]+$; minLen=1; maxLen=64)_
      - `audio` — SayCommandAudioOptions
        - `streamId` — string **(required)**
        - `sampleRate` — number **(required)**
      - `type` — object **(required)**
  - `PlayWebsocketCommand` — PlayWebsocketCommand
    - `type` — string **(required)** _(default=command)_
    - `command` — PlayWebsocketCommandData **(required)**
      - `replyId` — string **(required)**
      - `streamId` — string **(required)**
      - `data` — string **(required)** — The audio chunk is encoded in base64 and should be played in the stream. The chunk must use the sample rate specified in the "say" command and be PCM encoded.
      - `type` — object **(required)**
  - `StopWebsocketCommand` — StopWebsocketCommand
    - `type` — string **(required)** _(default=command)_
    - `command` — StopWebsocketCommandData **(required)**
      - `type` — object **(required)**
  - `HangupWebsocketCommand` — HangupWebsocketCommand
    - `type` — string **(required)** _(default=command)_
    - `command` — HangupWebsocketCommandData **(required)**
      - `reason` — string
      - `type` — object **(required)**
  - `TransferWebsocketCommand` — TransferWebsocketCommand
    - `type` — string **(required)** _(default=command)_
    - `command` — TransferWebsocketCommandData **(required)**
      - `context` — string **(required)**
      - `extension` — string **(required)**
      - `type` — object **(required)**
  - `SessionStartedWebhookEvent` — SessionStartedWebhookEvent
    - `sessionId` — string **(required)**
    - `botId` — string **(required)**
    - `callId` — string **(required)**
    - `flowIndex` — number **(required)**
    - `id` — string **(required)** — A unique identifier for the call, combined from companyID and callID. Uses the same format as "id" in calls webhooks.
    - `pbx` — string — PBX serial of the voicebot session source.
    - `company` — string — Company identifier of the voicebot session source. _(minLen=3; maxLen=30)_
    - `event` — SessionStartedEvent **(required)**
      - `type` — object **(required)**
      - `language` — string **(required)** — The language code that represents the language spoken in the session.
      - `callerNumber` — string — Caller's phone number.
      - `dialedNumber` — string — Number dialed to reach the voice bot.
      - `variables` — SessionVariables
        - _map of_ `string`
      - `time` — number **(required)**
  - `SessionEndedWebhookEvent` — SessionEndedWebhookEvent
    - `sessionId` — string **(required)**
    - `botId` — string **(required)**
    - `callId` — string **(required)**
    - `flowIndex` — number **(required)**
    - `id` — string **(required)** — A unique identifier for the call, combined from companyID and callID. Uses the same format as "id" in calls webhooks.
    - `pbx` — string — PBX serial of the voicebot session source.
    - `company` — string — Company identifier of the voicebot session source. _(minLen=3; maxLen=30)_
    - `event` — SessionEndedEvent **(required)**
      - `type` — object **(required)**
      - `error` — string
      - `time` — number **(required)**
  - `TranscriptionWebhookEvent` — TranscriptionWebhookEvent
    - `sessionId` — string **(required)**
    - `botId` — string **(required)**
    - `callId` — string **(required)**
    - `flowIndex` — number **(required)**
    - `id` — string **(required)** — A unique identifier for the call, combined from companyID and callID. Uses the same format as "id" in calls webhooks.
    - `pbx` — string — PBX serial of the voicebot session source.
    - `company` — string — Company identifier of the voicebot session source. _(minLen=3; maxLen=30)_
    - `event` — TranscriptionEvent **(required)**
      - `type` — object **(required)**
      - `id` — string **(required)**
      - `text` — string **(required)**
      - `confidence` — number — Transcription confidence score (accuracy level) in range from 0.0 to 1.0. Value -1.0 indicates confidence is unavailable. _(format=double; min=-1; max=1)_
      - `final` — boolean
      - `language` — string — Language the recogniser identified for this chunk. Recorded in the trace only; drives no behavior. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `time` — number **(required)**
  - `AudioWebhookEvent` — AudioWebhookEvent
    - `sessionId` — string **(required)**
    - `botId` — string **(required)**
    - `callId` — string **(required)**
    - `flowIndex` — number **(required)**
    - `id` — string **(required)** — A unique identifier for the call, combined from companyID and callID. Uses the same format as "id" in calls webhooks.
    - `pbx` — string — PBX serial of the voicebot session source.
    - `company` — string — Company identifier of the voicebot session source. _(minLen=3; maxLen=30)_
    - `event` — AudioEvent **(required)**
      - `type` — object **(required)**
      - `data` — string **(required)** — Audio chunk with a specified sample rate defined in the session.
  - `ReplyWebhookEvent` — ReplyWebhookEvent
    - `sessionId` — string **(required)**
    - `botId` — string **(required)**
    - `callId` — string **(required)**
    - `flowIndex` — number **(required)**
    - `id` — string **(required)** — A unique identifier for the call, combined from companyID and callID. Uses the same format as "id" in calls webhooks.
    - `pbx` — string — PBX serial of the voicebot session source.
    - `company` — string — Company identifier of the voicebot session source. _(minLen=3; maxLen=30)_
    - `event` — ReplyEvent **(required)**
      - `type` — object **(required)**
      - `id` — string **(required)**
      - `text` — string **(required)**
      - `language` — string — Language the recogniser identified for this completed utterance; drives the language switch. When several languages are reported inside one utterance the PBX sends the last labelled segment's. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `confidence` — number — Aggregated transcription confidence of the phrase this reply was built from, weighted by word count over the transcription chunks that carry a confidence value. Absent when no chunk had one, for example on DTMF input. _(format=double; min=-1; max=1)_
      - `startTime` — number **(required)**
      - `endTime` — number **(required)**
  - `PlaybackWebhookEvent` — PlaybackWebhookEvent
    - `sessionId` — string **(required)**
    - `botId` — string **(required)**
    - `callId` — string **(required)**
    - `flowIndex` — number **(required)**
    - `id` — string **(required)** — A unique identifier for the call, combined from companyID and callID. Uses the same format as "id" in calls webhooks.
    - `pbx` — string — PBX serial of the voicebot session source.
    - `company` — string — Company identifier of the voicebot session source. _(minLen=3; maxLen=30)_
    - `event` — PlaybackEvent **(required)**
      - `type` — object **(required)**
      - `replyId` — string **(required)**
      - `text` — string **(required)**
      - `complete` — boolean **(required)**
      - `startTime` — number **(required)**
      - `endTime` — number
  - `InterruptionWebhookEvent` — InterruptionWebhookEvent
    - `sessionId` — string **(required)**
    - `botId` — string **(required)**
    - `callId` — string **(required)**
    - `flowIndex` — number **(required)**
    - `id` — string **(required)** — A unique identifier for the call, combined from companyID and callID. Uses the same format as "id" in calls webhooks.
    - `pbx` — string — PBX serial of the voicebot session source.
    - `company` — string — Company identifier of the voicebot session source. _(minLen=3; maxLen=30)_
    - `event` — InterruptionEvent **(required)**
      - `type` — object **(required)**
      - `replyId` — string **(required)**
      - `playedText` — string **(required)**
      - `originalText` — string **(required)**
      - `time` — number **(required)**
  - `CompleteWebhookEvent` — CompleteWebhookEvent
    - `sessionId` — string **(required)**
    - `botId` — string **(required)**
    - `callId` — string **(required)**
    - `flowIndex` — number **(required)**
    - `id` — string **(required)** — A unique identifier for the call, combined from companyID and callID. Uses the same format as "id" in calls webhooks.
    - `pbx` — string — PBX serial of the voicebot session source.
    - `company` — string — Company identifier of the voicebot session source. _(minLen=3; maxLen=30)_
    - `event` — CompleteEvent **(required)**
      - `type` — object **(required)**
      - `reason` — string **(required)**
      - `time` — number **(required)**
  - `PubSubBroadcastWebsocketEvent` — PubSubBroadcastWebsocketEvent
    - `event` — string **(required)**
    - `topic` — string **(required)**
    - `items` — array **(required)**
      - _array of_ `PubSubBroadcastItem`
        - `session` — TraceSession
          - `sessionId` — string **(required)**
          - `connectionId` — string **(required)**
          - `company` — string **(required)**
          - `botId` — string **(required)**
          - `botName` — string **(required)**
          - `callId` — string **(required)**
          - `flowIndex` — number **(required)**
          - `language` — string
          - `callerName` — string
          - `callerNumber` — string
          - `status` — string **(required)** _(enum: `complete`, `complete_with_error`, `pending`)_
          - `start` — number **(required)** _(format=double)_
          - `duration` — number
        - `sessionId` — string
        - `activity` — TraceActivity
          - `id` — string **(required)**
          - `version` — number **(required)**
          - `status` — string **(required)** _(enum: `pending`, `error`, `complete`, `cancelled`)_
          - `trigger` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`connectEvent`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`disconnectEvent`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`replyEvent`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`completeEvent`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`interruptionEvent`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`playbackEvent`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`transcriptionEvent`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`sayCommand`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`hangupCommand`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`transferCommand`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`annotationCommand`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`silenceTimeoutTask`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`durationTimeoutTask`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `result` — union
            - _oneOf_ — exactly one of:
              - **`error`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`text`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `start` — number **(required)** _(format=double)_
          - `duration` — number
          - `timings` — TraceTimings
            - _map of_ `number`
          - `usage` — TraceUsage
            - `generation` — TraceGenerationUsage
              - _(nesting depth limit — see `TraceGenerationUsage` in the Schemas appendix)_
            - `transcribe` — TraceTranscribeUsage
              - _(nesting depth limit — see `TraceTranscribeUsage` in the Schemas appendix)_
            - `playback` — TracePlaybackUsage
              - _(nesting depth limit — see `TracePlaybackUsage` in the Schemas appendix)_
        - `segment` — TraceSegment
          - `id` — string **(required)**
          - `activityId` — string **(required)**
          - `version` — number **(required)**
          - `status` — string **(required)** _(enum: `pending`, `error`, `complete`)_
          - `input` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`completion`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`tool`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`oauth`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`generic`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `result` — union
            - _oneOf_ — exactly one of:
              - **`error`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`tools`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`text`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`json`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `start` — number **(required)** _(format=double)_
          - `duration` — number
  - `PubSubSubscribeWebsocketCommand` — PubSubSubscribeWebsocketCommand
    - `action` — string **(required)**
    - `topic` — string **(required)**
  - `PubSubSubscribedWebsocketEvent` — PubSubSubscribedWebsocketEvent
    - `event` — string **(required)**
    - `topic` — string **(required)**
  - `PubSubUnsubscribeWebsocketCommand` — PubSubUnsubscribeWebsocketCommand
    - `action` — string **(required)**
    - `topic` — string **(required)**
  - `PubSubUnsubscribedWebsocketEvent` — PubSubUnsubscribedWebsocketEvent
    - `event` — string **(required)**
    - `topic` — string **(required)**
- Errors: `400`, `403`

#### `GET` `/v2/voicebots/traces/{sessionId}`

Retrieves detailed trace information for a specific voice bot session.

- operationId: `GetTrace`
- **Scopes**: `voicebots:GetTrace`, `voicebots:read`
- **Parameters**
  - `sessionId` (path) — string **(required)**
  - `company` (query) — string
- **Response 200** (`GetTraceResponseContent`)
  - `trace` — Trace **(required)**
    - `session` — TraceSession **(required)**
      - `sessionId` — string **(required)**
      - `connectionId` — string **(required)**
      - `company` — string **(required)**
      - `botId` — string **(required)**
      - `botName` — string **(required)**
      - `callId` — string **(required)**
      - `flowIndex` — number **(required)**
      - `language` — string
      - `callerName` — string
      - `callerNumber` — string
      - `status` — string **(required)** _(enum: `complete`, `complete_with_error`, `pending`)_
      - `start` — number **(required)** _(format=double)_
      - `duration` — number
    - `activities` — array **(required)**
      - _array of_ `TraceActivity`
        - `id` — string **(required)**
        - `version` — number **(required)**
        - `status` — string **(required)** _(enum: `pending`, `error`, `complete`, `cancelled`)_
        - `trigger` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`connectEvent`**
              - `connectEvent` — TraceConnectEventTrigger **(required)**
                - _(nesting depth limit — see `TraceConnectEventTrigger` in the Schemas appendix)_
            - **`disconnectEvent`**
              - `disconnectEvent` — TraceDisconnectEventTrigger **(required)**
                - _(nesting depth limit — see `TraceDisconnectEventTrigger` in the Schemas appendix)_
            - **`replyEvent`**
              - `replyEvent` — ReplyWebsocketEvent **(required)**
                - _(nesting depth limit — see `ReplyWebsocketEvent` in the Schemas appendix)_
            - **`completeEvent`**
              - `completeEvent` — CompleteWebsocketEvent **(required)**
                - _(nesting depth limit — see `CompleteWebsocketEvent` in the Schemas appendix)_
            - **`interruptionEvent`**
              - `interruptionEvent` — InterruptionWebsocketEvent **(required)**
                - _(nesting depth limit — see `InterruptionWebsocketEvent` in the Schemas appendix)_
            - **`playbackEvent`**
              - `playbackEvent` — PlaybackWebsocketEvent **(required)**
                - _(nesting depth limit — see `PlaybackWebsocketEvent` in the Schemas appendix)_
            - **`transcriptionEvent`**
              - `transcriptionEvent` — TranscriptionWebsocketEvent **(required)**
                - _(nesting depth limit — see `TranscriptionWebsocketEvent` in the Schemas appendix)_
            - **`sayCommand`**
              - `sayCommand` — SayWebsocketCommand **(required)**
                - _(nesting depth limit — see `SayWebsocketCommand` in the Schemas appendix)_
            - **`hangupCommand`**
              - `hangupCommand` — HangupWebsocketCommand **(required)**
                - _(nesting depth limit — see `HangupWebsocketCommand` in the Schemas appendix)_
            - **`transferCommand`**
              - `transferCommand` — TransferWebsocketCommand **(required)**
                - _(nesting depth limit — see `TransferWebsocketCommand` in the Schemas appendix)_
            - **`annotationCommand`**
              - `annotationCommand` — TraceAnnotationCommand **(required)** — Trace activity written when the voicebot emits an annotation.
                - _(nesting depth limit — see `TraceAnnotationCommand` in the Schemas appendix)_
            - **`silenceTimeoutTask`**
              - `silenceTimeoutTask` — TraceSilenceTimeoutTaskTrigger **(required)**
                - _(nesting depth limit — see `TraceSilenceTimeoutTaskTrigger` in the Schemas appendix)_
            - **`durationTimeoutTask`**
              - `durationTimeoutTask` — TraceDurationTimeoutTaskTrigger **(required)**
                - _(nesting depth limit — see `TraceDurationTimeoutTaskTrigger` in the Schemas appendix)_
        - `result` — union
          - _oneOf_ — exactly one of:
            - **`error`**
              - `error` — TraceErrorResult **(required)**
                - _(nesting depth limit — see `TraceErrorResult` in the Schemas appendix)_
            - **`text`**
              - `text` — string **(required)**
        - `start` — number **(required)** _(format=double)_
        - `duration` — number
        - `timings` — TraceTimings
          - _map of_ `number`
        - `usage` — TraceUsage
          - `generation` — TraceGenerationUsage
            - `tokens` — number
            - `outputTokens` — number
            - `inputTokens` — number
            - `cachedInputTokens` — number
            - `reasoningTokens` — number
            - `category` — string
          - `transcribe` — TraceTranscribeUsage
            - `seconds` — number
            - `category` — string
          - `playback` — TracePlaybackUsage
            - `chars` — number
            - `category` — string
    - `segments` — array **(required)**
      - _array of_ `TraceSegment`
        - `id` — string **(required)**
        - `activityId` — string **(required)**
        - `version` — number **(required)**
        - `status` — string **(required)** _(enum: `pending`, `error`, `complete`)_
        - `input` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`completion`**
              - `completion` — TraceSegmentCompletionInput **(required)**
                - _(nesting depth limit — see `TraceSegmentCompletionInput` in the Schemas appendix)_
            - **`tool`**
              - `tool` — union **(required)**
                - _(nesting depth limit — see `TraceToolCall` in the Schemas appendix)_
            - **`oauth`**
              - `oauth` — TraceOAuthInput **(required)**
                - _(nesting depth limit — see `TraceOAuthInput` in the Schemas appendix)_
            - **`generic`**
              - `generic` — TraceGenericInput **(required)**
                - _(nesting depth limit — see `TraceGenericInput` in the Schemas appendix)_
        - `result` — union
          - _oneOf_ — exactly one of:
            - **`error`**
              - `error` — TraceErrorResult **(required)**
                - _(nesting depth limit — see `TraceErrorResult` in the Schemas appendix)_
            - **`tools`**
              - `tools` — array **(required)**
                - _(nesting depth limit — see `TraceToolCall` in the Schemas appendix)_
            - **`text`**
              - `text` — string **(required)**
            - **`json`**
              - `json` — any **(required)**
        - `start` — number **(required)** _(format=double)_
        - `duration` — number
    - `usage` — TraceUsage
      - `generation` — TraceGenerationUsage
        - `tokens` — number
        - `outputTokens` — number
        - `inputTokens` — number
        - `cachedInputTokens` — number
        - `reasoningTokens` — number
        - `category` — string
      - `transcribe` — TraceTranscribeUsage
        - `seconds` — number
        - `category` — string
      - `playback` — TracePlaybackUsage
        - `chars` — number
        - `category` — string
    - `cost` — number _(format=float)_
- Errors: `400`, `403`, `404`

### Session

#### `POST` `/v2/voicebots/sessions/{sessionId}/hangup`

Terminates the voice session and the call.

- operationId: `SendHangup`
- **Scopes**: `voicebots:SendHangup`
- **Parameters**
  - `sessionId` (path) — string **(required)**
- **Request body** (`application/json` — `SendHangupRequestContent`)
  - `reason` — string
- Errors: `400`, `403`, `404`

#### `POST` `/v2/voicebots/sessions/{sessionId}/play`

Plays the specified audio chunk through the audio stream of the voice session.

- operationId: `SendPlay`
- **Scopes**: `voicebots:SendPlay`
- **Parameters**
  - `sessionId` (path) — string **(required)**
- **Request body** (`application/json` — `SendPlayRequestContent`) **(required)**
  - `replyId` — string **(required)**
  - `streamId` — string **(required)**
  - `data` — string **(required)** — The audio chunk is encoded in base64 and should be played in the stream. The chunk must use the sample rate specified in the "say" command and be PCM encoded.
- Errors: `400`, `403`, `404`

#### `POST` `/v2/voicebots/sessions/{sessionId}/say`

Generates and plays the specified text through the audio stream of the voice session.

- operationId: `SendSay`
- **Scopes**: `voicebots:SendSay`
- **Parameters**
  - `sessionId` (path) — string **(required)**
- **Request body** (`application/json` — `SendSayRequestContent`) **(required)**
  - `text` — string **(required)**
  - `replyId` — string **(required)**
  - `interruptible` — boolean
  - `voice` — string — Bare Amazon Polly voice id, e.g. 'Joanna' — NOT a URI. The PBX consumes this verbatim as the AMI `Voice=` action parameter, so it takes exactly what Polly names the voice, with the `amazon_polly://` scheme and any query parameters already stripped by whoever builds this command out of the bot's stored `VoiceBotVoiceUri`. Set only for a provider whose synthesis runs ON THE PBX (Amazon Polly); ElevenLabs and Google are synthesized in the cloud and streamed as PCM through `play` instead, and leave this absent. _(pattern=^[A-Za-z0-9]+$; minLen=1; maxLen=64)_
  - `audio` — SayCommandAudioOptions
    - `streamId` — string **(required)**
    - `sampleRate` — number **(required)**
- Errors: `400`, `403`, `404`

#### `POST` `/v2/voicebots/sessions/{sessionId}/stop`

Stop playing and ongoing audio from the voice bot.

- operationId: `SendStop`
- **Scopes**: `voicebots:SendStop`
- **Parameters**
  - `sessionId` (path) — string **(required)**
- Errors: `400`, `403`, `404`

#### `POST` `/v2/voicebots/sessions/{sessionId}/transfer`

Transfers the call to the specified context and extension, and terminates the voice bot session.

- operationId: `SendTransfer`
- **Scopes**: `voicebots:SendTransfer`
- **Parameters**
  - `sessionId` (path) — string **(required)**
- **Request body** (`application/json` — `SendTransferRequestContent`) **(required)**
  - `context` — string **(required)**
  - `extension` — string **(required)**
- Errors: `400`, `403`, `404`

### Speech

#### `POST` `/v2/voicebots/text-to-speech`

Synthesizes one phrase and returns MP3.

    NOT NAMED FOR THE PREVIEW IT SERVES. Auditioning an unsaved voice in the console is the first
    caller, but nothing about the operation is preview-specific — it is the platform's
    text-to-speech, reachable by anything holding the scope, and a name naming one caller's screen
    would have to be worked around by the second one.

    The operation reads no stored bot for the audition itself: the exact voice URI, including any
    custom account key, travels in the request so the audition and runtime cannot diverge. `botId`
    is the one exception, for a language whose key is masked (`apiKey=stored`) in that URI: it
    lets the server resolve the bot's stored key server-side instead of the caller round-tripping
    a key it was never given back. It only substitutes which key authenticates the synthesis call
    — the response never carries the key either way.

- operationId: `TextToSpeech`
- **Scopes**: `voicebots:TextToSpeech`, `voicebots:UpdateVoiceBot`
- **Request body** (`application/json` — `TextToSpeechRequestContent`) **(required)**
  - `voice` — string **(required)** — Voice to speak with, as the URI a call would use — provider, voice id, synthesis parameters and, for a custom account, `apiKey`. Passing the call's own value is what keeps an audition from diverging from the call it is auditioning. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
  - `language` — string **(required)** — Language the phrase is in. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
  - `text` — string **(required)** — Text to speak, before pronunciation rules are applied. _(minLen=1; maxLen=2000)_
  - `pronunciations` — array — Pronunciation rules for this language, applied SERVER-SIDE by the same helper the call path uses — never pre-applied by the caller, or the form reimplements a rule the server owns and can silently diverge from the call. _(maxItems=200)_
    - _array of_ `VoiceBotPronunciation`
      - `phrase` — string **(required)** — The written form to replace. Bounded because every rule is compiled into ONE regular expression — see the list below. _(maxLen=200)_
      - `as` — string **(required)** — Respelling (ALIAS) or phonetic transcription (IPA). _(maxLen=200)_
      - `encoding` — string _(enum: `alias`, `ipa`)_
  - `botId` — string — The bot whose language this audition speaks for. Resolves the language's STORED private key server-side when that language's key is masked (`apiKey=stored`) rather than the caller round-tripping a key it was never given back. The key itself is never returned — it is used only to authenticate against the provider. _(minLen=12; maxLen=12)_
- **Response 200** (`TextToSpeechOutputPayload`)
  - string
- Errors: `400`, `403`

#### `GET` `/v2/voicebots/voices`

Lists the voices a synthesis provider offers, read from the provider's own API. Answers a URI
    per voice, so a picker stores what it selected rather than composing one.

    A catalog is a property of the provider and the account, not a stored bot: a form needs the
    speaker list before the bot it is configuring exists, and for that pre-bot case the caller
    supplies its key on `credential`, then appends it to the voice URI it stores. `botId` is the
    one exception, for an already-saved bot whose language key is masked (`apiKey=stored`): it
    lets the server resolve that stored key instead of the caller round-tripping a key it was
    never given back. It only substitutes which key authenticates the request — the response
    never carries the key either way.

- operationId: `ListVoices`
- **Scopes**: `voicebots:ListVoices`, `voicebots:read`
- **Parameters**
  - `provider` (query) — string **(required)** — Provider whose catalog to read: 'elevenlabs', 'google', 'amazon_polly'. This is the scheme of the URIs answered on `voices`. _(pattern=^[a-z0-9][a-z0-9_-]*$; minLen=1; maxLen=32)_
  - `language` (query) — string — Server-side filter for language-bound providers: only voices whose language SET CONTAINS this code. Ignored for ElevenLabs, whose voices are not language bound. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
  - `botId` (query) — string — The bot whose language this catalog request previews. Resolves the language's STORED private key server-side when that language's key is masked (`apiKey=stored`) rather than the caller round-tripping a key it was never given back. The key itself is never returned — it is used only to authenticate against the provider. When both `credential` and `botId` are sent, `credential` wins. _(minLen=12; maxLen=12)_
  - `x-wildix-provider-credential` (header) — string — The company's own provider key, used to list that account's voices including cloned ones. Absent means the platform account. A header avoids putting the key in this GET request's URL, browser history and ordinary access logs. It remains a secret at this boundary: never include it in a cache identity, response or trace attribute. The stored voice URI deliberately makes a different legacy trade-off; see VoiceBotVoiceUri. _(format=password; minLen=1; maxLen=16384)_
- **Response 200** (`ListVoicesResponseContent`)
  - `voices` — array **(required)**
    - _array of_ `VoiceBotVoice`
      - `uri` — string **(required)** — Voice URI, ready to store as `VoiceBotLanguage.voice` or send to TextToSpeech. The caller appends the synthesis parameters and, for a custom provider account, `apiKey=...` before storing it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
      - `name` — string **(required)** — Display name as the provider publishes it, e.g. 'Rachel'. A member rather than part of `metadata` because it is the one thing every provider has and every picker shows.
      - `metadata` — any — The provider's own metadata for this voice, for rendering and filtering only. See VoiceBotVoiceMetadata.
- Errors: `400`, `403`, `404`

### Traces

#### `GET` `/v2/voicebots/traces`

Retrieves a list of voice bot trace sessions for the specified company.

- operationId: `ListTraces`
- **Scopes**: `voicebots:ListTraces`, `voicebots:read`
- **Parameters**
  - `company` (query) — string
  - `search` (query) — string — Optional search query to filter traces by caller name, bot name, or session ID.
- **Response 200** (`ListTracesResponseContent`)
  - `traces` — array **(required)**
    - _array of_ `TraceSession`
      - `sessionId` — string **(required)**
      - `connectionId` — string **(required)**
      - `company` — string **(required)**
      - `botId` — string **(required)**
      - `botName` — string **(required)**
      - `callId` — string **(required)**
      - `flowIndex` — number **(required)**
      - `language` — string
      - `callerName` — string
      - `callerNumber` — string
      - `status` — string **(required)** _(enum: `complete`, `complete_with_error`, `pending`)_
      - `start` — number **(required)** _(format=double)_
      - `duration` — number
- Errors: `400`, `403`

### Schemas appendix — VoiceBots API

<details><summary>168 component schemas</summary>

**`Annotation`**

- `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
- `time` — number **(required)**
- `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
- `payload` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`tag`**
      - `tag` — string **(required)** _(maxLen=50)_
    - **`text`**
      - `text` — string **(required)** _(maxLen=4096)_
    - **`variables`**
      - `variables` — AnnotationVariablesValue **(required)** — Capability variable values captured for an annotation. Runtime services enforce serialized payload size limits.
        - `value` — any **(required)**
    - **`result`**
      - `result` — AnnotationResultValue **(required)** — Tool result captured for an annotation. Runtime services enforce serialized payload size limits.
        - `value` — any **(required)**
    - **`metric`**
      - `metric` — AnnotationMetricValue **(required)** — A named value observed during the conversation, and the reading it replaces — a CSAT score, a talk ratio, the outcome of an evaluation. Emitted with an `AnnotationKey`, which is what makes the newest reading addressable in `annotationsByKey` while the series stays in `annotations`. Runtime services enforce serialized payload size limits.
        - `value` — any **(required)** — The reading, as its producer models it: a score, a label, a number, or an object such as `{"customerRatio": 0.42, "agentRatio": 0.58}`.
        - `previous` — any — The reading this one replaces, so a consumer can render the change without loading the history. Absent on the first reading.
        - `label` — string — Human-readable name of the value, e.g. 'CSAT' or 'Talk ratio'. _(maxLen=100)_
- `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
  - `type` — string **(required)** _(enum: `chatbot`, `voicebot`, `user`, `system`, `copilot`)_
  - `id` — string — Stable identifier of the producer (e.g. tool id, user id, copilot session id).
  - `name` — string — Human-readable name of the producer (e.g. tool name, user display name).

**`AnnotationMetricValue`**

_A named value observed during the conversation, and the reading it replaces — a CSAT score, a talk ratio, the outcome of an evaluation. Emitted with an `AnnotationKey`, which is what makes the newest reading addressable in `annotationsByKey` while the series stays in `annotations`. Runtime services enforce serialized payload size limits._

- `value` — any **(required)** — The reading, as its producer models it: a score, a label, a number, or an object such as `{"customerRatio": 0.42, "agentRatio": 0.58}`.
- `previous` — any — The reading this one replaces, so a consumer can render the change without loading the history. Absent on the first reading.
- `label` — string — Human-readable name of the value, e.g. 'CSAT' or 'Talk ratio'. _(maxLen=100)_

**`AnnotationPayload`**

- _oneOf_ — exactly one of:
  - **`tag`**
    - `tag` — string **(required)** _(maxLen=50)_
  - **`text`**
    - `text` — string **(required)** _(maxLen=4096)_
  - **`variables`**
    - `variables` — AnnotationVariablesValue **(required)** — Capability variable values captured for an annotation. Runtime services enforce serialized payload size limits.
      - `value` — any **(required)**
  - **`result`**
    - `result` — AnnotationResultValue **(required)** — Tool result captured for an annotation. Runtime services enforce serialized payload size limits.
      - `value` — any **(required)**
  - **`metric`**
    - `metric` — AnnotationMetricValue **(required)** — A named value observed during the conversation, and the reading it replaces — a CSAT score, a talk ratio, the outcome of an evaluation. Emitted with an `AnnotationKey`, which is what makes the newest reading addressable in `annotationsByKey` while the series stays in `annotations`. Runtime services enforce serialized payload size limits.
      - `value` — any **(required)** — The reading, as its producer models it: a score, a label, a number, or an object such as `{"customerRatio": 0.42, "agentRatio": 0.58}`.
      - `previous` — any — The reading this one replaces, so a consumer can render the change without loading the history. Absent on the first reading.
      - `label` — string — Human-readable name of the value, e.g. 'CSAT' or 'Talk ratio'. _(maxLen=100)_

**`AnnotationResultValue`**

_Tool result captured for an annotation. Runtime services enforce serialized payload size limits._

- `value` — any **(required)**

**`AnnotationSource`**

_Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape._

- `type` — string **(required)** _(enum: `chatbot`, `voicebot`, `user`, `system`, `copilot`)_
- `id` — string — Stable identifier of the producer (e.g. tool id, user id, copilot session id).
- `name` — string — Human-readable name of the producer (e.g. tool name, user display name).

**`AnnotationSourceType`**

- string _(enum: `chatbot`, `voicebot`, `user`, `system`, `copilot`)_

**`AnnotationVariablesValue`**

_Capability variable values captured for an annotation. Runtime services enforce serialized payload size limits._

- `value` — any **(required)**

**`AudioEvent`**

- `type` — object **(required)**
- `data` — string **(required)** — Audio chunk with a specified sample rate defined in the session.

**`AudioWebhookEvent`**

- `sessionId` — string **(required)**
- `botId` — string **(required)**
- `callId` — string **(required)**
- `flowIndex` — number **(required)**
- `id` — string **(required)** — A unique identifier for the call, combined from companyID and callID. Uses the same format as "id" in calls webhooks.
- `pbx` — string — PBX serial of the voicebot session source.
- `company` — string — Company identifier of the voicebot session source. _(minLen=3; maxLen=30)_
- `event` — AudioEvent **(required)**
  - `type` — object **(required)**
  - `data` — string **(required)** — Audio chunk with a specified sample rate defined in the session.

**`BotDialogflowCxEndpoint`**

- `credentials` — any **(required)** — Dialogflow Service Account Credentials
- `agent` — string **(required)** — Dialogflow Agent Id (example - 88ff4635-0852-4f97-ae44-b19ae9fa6ea1
- `location` — string **(required)** — Dialogflow Agent Region (example: europe-west3)
- `language` — string **(required)** — Language

**`BotOpenAiAssistantEndpoint`**

- `key` — string **(required)**
- `assistantId` — string **(required)**

**`BotSqsEndpoint`**

- `url` — string **(required)**
- `key` — string **(required)**
- `secret` — string **(required)**

**`BotWebhookEndpoint`**

- `url` — string **(required)**
- `secret` — string **(required)**

**`CompleteEvent`**

- `type` — object **(required)**
- `reason` — string **(required)**
- `time` — number **(required)**

**`CompleteWebhookEvent`**

- `sessionId` — string **(required)**
- `botId` — string **(required)**
- `callId` — string **(required)**
- `flowIndex` — number **(required)**
- `id` — string **(required)** — A unique identifier for the call, combined from companyID and callID. Uses the same format as "id" in calls webhooks.
- `pbx` — string — PBX serial of the voicebot session source.
- `company` — string — Company identifier of the voicebot session source. _(minLen=3; maxLen=30)_
- `event` — CompleteEvent **(required)**
  - `type` — object **(required)**
  - `reason` — string **(required)**
  - `time` — number **(required)**

**`CompleteWebsocketEvent`**

- `type` — string **(required)** _(default=event)_
- `event` — CompleteEvent **(required)**
  - `type` — object **(required)**
  - `reason` — string **(required)**
  - `time` — number **(required)**

**`CreateVoiceBotRequestContent`**

- `name` — string **(required)** _(minLen=3; maxLen=255)_
- `category` — string — Category of the bot _(minLen=1; maxLen=128)_
- `message` — string — The initial message that will be played at the start of the session.
- `pipeline` — VoiceBotPipelineSettings
  - `interuptionsEnabled` — boolean — If enabled the user can interrupt the the bot playback.
  - `maximumDuration` — number — The maximum number of seconds a call will last.
  - `maximumDurationAction` — union
    - _oneOf_ — exactly one of:
      - **`hangup`**
        - `hangup` — VoiceBotTerminateHangupAction **(required)**
      - **`transfer`**
        - `transfer` — VoiceBotTerminateTransferAction **(required)**
          - _(nesting depth limit — see `VoiceBotTerminateTransferAction` in the Schemas appendix)_
  - `silenceTimeout` — number — How long to wait before a call is automatically ended due to inactivity.
  - `silenceTimeoutAction` — union
    - _oneOf_ — exactly one of:
      - **`hangup`**
        - `hangup` — VoiceBotTerminateHangupAction **(required)**
      - **`transfer`**
        - `transfer` — VoiceBotTerminateTransferAction **(required)**
          - _(nesting depth limit — see `VoiceBotTerminateTransferAction` in the Schemas appendix)_
  - `endCallEnabled` — boolean — If enabled the bot can hangup the call.
  - `endCallPhases` — string — A list of phases separated by comma, which will end the call matched.
- `speech` — VoiceBotSpeechSettings — Speech configuration. When present it wins over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the exception.
  - `languages` — array **(required)** — Configured languages. The @length bound is a storage ceiling; the real cap is the recogniser's own candidate limit, enforced in the service. _(minItems=1; maxItems=10)_
    - _array of_ `VoiceBotLanguage`
      - `code` — string **(required)** — BCP-47 code with locale, e.g. 'en-US'. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `voice` — string **(required)** — Voice this language speaks with, as a URI — provider, voice id, synthesis parameters and, where the company uses its own provider account, its `apiKey` query parameter. See VoiceBotVoiceUri. PER LANGUAGE, and that is the whole reason the member is here rather than on the settings above: provider quality is not uniform across languages, a voice id belongs to exactly one provider, and a bot-wide provider made changing it invalidate every configured voice at once. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
      - `greeting` — string — Initial phrase for this language. Absent or empty means the agent says nothing and waits — it does NOT fall back to the agent-level message, which would speak one language's text in another language's voice.
      - `isDefault` — boolean — Marks the language a caller hears when their own matches nothing configured. THE FULL RESOLUTION ORDER, since a client author reading only this contract cannot otherwise find it: an exact match on the call's language, then a match on its primary subtag (`fr` finds `fr-FR`), then the language marked here, then a language whose primary subtag is `en`, then the first entry in the list. Marked is consulted BEFORE the English step, so a record with none marked resolves exactly as it did before this member existed. English is deliberate rather than arbitrary — it is the language a caller the agent was not built for is likeliest to understand — and the last step exists only to keep the rule total, which is why list order should not be treated as configuration. At most one language may carry it. A record with two — reachable through the API or the CLI, where no form prevents it — resolves to the first marked one in list order, because refusing a call over configuration drift is worse than serving it and saying so in the trace.
      - `pronunciations` — array — Pronunciation rules for one language. BOUNDED, and the bound is not decoration. `applyPronunciations` compiles every rule of a language into a SINGLE alternating regular expression, so the cost is the pattern's total size: measured against the real escaping and matching logic, 1,000 rules cost ~0.9 s of CPU per synthesized sentence, 5,000 cost ~4.9 s, and around 10,000 `new RegExp` throws V8's pattern-size error outright — from a call site outside the surrounding `try`, so a 500 rather than a degraded reply. Stored on a bot, that made every utterance of the agent fail. 200 is far above any real use — a product glossary is a handful of names — and far below where either cost begins. Found by a security review. NO LOWER BOUND on `phrase` or `as`, deliberately. Both consoles add an EMPTY rule row the moment someone clicks 'Add pronunciation', so a `min: 1` would make saving an agent with a half-typed row fail entirely — and the runtime already ignores a rule with no phrase. Dropping blank rows belongs in the consoles' save filters, not in a refusal here. _(maxItems=200)_
        - _(nesting depth limit — see `VoiceBotPronunciation` in the Schemas appendix)_
  - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in its own language's voice, provider account and pronunciation rules. Languages with an empty first message, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
  - `transcription` — VoiceBotTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
    - `engine` — string — Recogniser to transcribe the caller with. Absent resolves to the platform default ('aws://transcribe' today), resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
    - `autoDetect` — boolean — Identify the caller's language per utterance and switch voice and reply language mid-call. HERE RATHER THAN ON `VoiceBotSpeechSettings`, because identifying a language is something the RECOGNISER does: it becomes identify-multiple-languages plus language-options on the recognition stream, and nothing about synthesis reads it. Requires at least two configured languages and a recogniser that can identify them; the server clamps it to false otherwise, because forwarding true with a single candidate makes Amazon reject the stream outright.
- `backgroundSound` — VoiceBotBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT rather than a loose name on the bot, matching `wildix.wilma.agents`: it is one switchable call behaviour, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
  - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
  - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
- `endpoint` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`llm`**
      - `llm` — VoiceBotLlmEndpoint **(required)**
        - `prompt` — string **(required)** _(maxLen=40000)_
        - `model` — string — The AI model to use for generating responses. If not specified, uses the default model. _(default=default; pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
        - `guidelines` — array
          - _array of_ `string`
        - `metadata` — VoiceBotPromptMetadata
          - _(nesting depth limit — see `VoiceBotPromptMetadata` in the Schemas appendix)_
        - `embeddedTools` — array — Embedded functions to use within voice session.
          - _(nesting depth limit — see `VoiceBotEmbeddedTool` in the Schemas appendix)_
        - `tools` — array — Custom tools to be used within voice session.
          - _(nesting depth limit — see `VoiceBotTool` in the Schemas appendix)_
        - `capabilities` — array
          - _(nesting depth limit — see `VoiceBotCapability` in the Schemas appendix)_
        - `variables` — array — Variables such as dialplan variables that can be used in the bot.
          - _(nesting depth limit — see `VoiceBotVariable` in the Schemas appendix)_
    - **`dialogflowCx`**
      - `dialogflowCx` — BotDialogflowCxEndpoint **(required)**
        - `credentials` — any **(required)** — Dialogflow Service Account Credentials
        - `agent` — string **(required)** — Dialogflow Agent Id (example - 88ff4635-0852-4f97-ae44-b19ae9fa6ea1
        - `location` — string **(required)** — Dialogflow Agent Region (example: europe-west3)
        - `language` — string **(required)** — Language
    - **`openAiAssistant`**
      - `openAiAssistant` — BotOpenAiAssistantEndpoint **(required)**
        - `key` — string **(required)**
        - `assistantId` — string **(required)**
    - **`webhook`**
      - `webhook` — BotWebhookEndpoint **(required)**
        - `url` — string **(required)**
        - `secret` — string **(required)**
    - **`sqs`**
      - `sqs` — BotSqsEndpoint **(required)**
        - `url` — string **(required)**
        - `key` — string **(required)**
        - `secret` — string **(required)**
- `capabilities` — array
  - _array of_ `VoiceBotCapability`
    - _oneOf_ — exactly one of:
      - **`tool`**
        - `tool` — VoiceBotCapabilityTool **(required)**
          - _(nesting depth limit — see `VoiceBotCapabilityTool` in the Schemas appendix)_
      - **`kb`**
        - `kb` — VoiceBotKnowledgeBase **(required)**
          - _(nesting depth limit — see `VoiceBotKnowledgeBase` in the Schemas appendix)_
- `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.

**`CreateVoiceBotResponseContent`**

- `bot` — VoiceBot **(required)**
  - `name` — string **(required)** _(minLen=3; maxLen=255)_
  - `category` — string — Category of the bot _(minLen=1; maxLen=128)_
  - `message` — string — The initial message that will be played at the start of the session.
  - `pipeline` — VoiceBotPipelineSettings
    - `interuptionsEnabled` — boolean — If enabled the user can interrupt the the bot playback.
    - `maximumDuration` — number — The maximum number of seconds a call will last.
    - `maximumDurationAction` — union
      - _oneOf_ — exactly one of:
        - **`hangup`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`transfer`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `silenceTimeout` — number — How long to wait before a call is automatically ended due to inactivity.
    - `silenceTimeoutAction` — union
      - _oneOf_ — exactly one of:
        - **`hangup`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`transfer`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `endCallEnabled` — boolean — If enabled the bot can hangup the call.
    - `endCallPhases` — string — A list of phases separated by comma, which will end the call matched.
  - `speech` — VoiceBotSpeechSettings — Speech configuration. When present it wins over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the exception.
    - `languages` — array **(required)** — Configured languages. The @length bound is a storage ceiling; the real cap is the recogniser's own candidate limit, enforced in the service. _(minItems=1; maxItems=10)_
      - _array of_ `VoiceBotLanguage`
        - _(nesting depth limit — see `VoiceBotLanguage` in the Schemas appendix)_
    - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in its own language's voice, provider account and pronunciation rules. Languages with an empty first message, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
    - `transcription` — VoiceBotTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
      - `engine` — string — Recogniser to transcribe the caller with. Absent resolves to the platform default ('aws://transcribe' today), resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
      - `autoDetect` — boolean — Identify the caller's language per utterance and switch voice and reply language mid-call. HERE RATHER THAN ON `VoiceBotSpeechSettings`, because identifying a language is something the RECOGNISER does: it becomes identify-multiple-languages plus language-options on the recognition stream, and nothing about synthesis reads it. Requires at least two configured languages and a recogniser that can identify them; the server clamps it to false otherwise, because forwarding true with a single candidate makes Amazon reject the stream outright.
  - `backgroundSound` — VoiceBotBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT rather than a loose name on the bot, matching `wildix.wilma.agents`: it is one switchable call behaviour, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
    - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
    - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
  - `endpoint` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`llm`**
        - `llm` — VoiceBotLlmEndpoint **(required)**
          - _(nesting depth limit — see `VoiceBotLlmEndpoint` in the Schemas appendix)_
      - **`dialogflowCx`**
        - `dialogflowCx` — BotDialogflowCxEndpoint **(required)**
          - _(nesting depth limit — see `BotDialogflowCxEndpoint` in the Schemas appendix)_
      - **`openAiAssistant`**
        - `openAiAssistant` — BotOpenAiAssistantEndpoint **(required)**
          - _(nesting depth limit — see `BotOpenAiAssistantEndpoint` in the Schemas appendix)_
      - **`webhook`**
        - `webhook` — BotWebhookEndpoint **(required)**
          - _(nesting depth limit — see `BotWebhookEndpoint` in the Schemas appendix)_
      - **`sqs`**
        - `sqs` — BotSqsEndpoint **(required)**
          - _(nesting depth limit — see `BotSqsEndpoint` in the Schemas appendix)_
  - `capabilities` — array
    - _array of_ `VoiceBotCapability`
      - _oneOf_ — exactly one of:
        - **`tool`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`kb`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`DescribeEventResponseContent`**

- `SessionStartedWebsocketEvent` — SessionStartedWebsocketEvent
  - `type` — string **(required)** _(default=event)_
  - `event` — SessionStartedWebsocketEventData **(required)**
    - `type` — object **(required)**
    - `botId` — string **(required)**
    - `botName` — string **(required)**
    - `category` — string
    - `groupId` — string
    - `speech` — VoiceBotSpeechPayload — Recognition intent for the call, sent on `started` at protocol version >= 2. Not recogniser parameters: the PBX translates it into its provider's API. `engine` is always concrete and `autoDetect` is already clamped by the server, because forwarding true with a single candidate makes Amazon reject the stream outright.
      - `engine` — string **(required)** — Concrete recogniser URI, resolved from the bot or from the platform default; never absent. See VoiceBotTranscriptionUri. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
      - `languages` — array **(required)** — Every configured language, as candidates for identification.
        - _array of_ `string`
      - `preferredLanguage` — string **(required)** — The language the call starts in, resolved from the channel. Always a member of `languages`. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `autoDetect` — boolean **(required)**
    - `backgroundSound` — string — Music-on-hold class the PBX should play under the call as ambient background. A BARE NAME, not the configuration object `VoiceBotBackgroundSoundSettings`: this is the RESOLVED outcome. The server has already applied `enabled` and the class default, so the PBX gets a name to play or nothing at all and needs no resolution rule of its own. TOP LEVEL, NOT INSIDE `speech`, because it is not recognition intent and must not inherit `speech`'s conditions: a call with no configured languages carries no `speech` payload and can still have background audio. ABSENT MEANS OFF, and absence is the only way to say it — there is no value for 'none'. A bot whose administrator never touched the setting sends nothing here, which is exactly what every call sent before it existed, so the PBX needs no new case. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
    - `time` — number **(required)**
- `TranscriptionWebsocketEvent` — TranscriptionWebsocketEvent
  - `type` — string **(required)** _(default=event)_
  - `event` — TranscriptionEvent **(required)**
    - `type` — object **(required)**
    - `id` — string **(required)**
    - `text` — string **(required)**
    - `confidence` — number — Transcription confidence score (accuracy level) in range from 0.0 to 1.0. Value -1.0 indicates confidence is unavailable. _(format=double; min=-1; max=1)_
    - `final` — boolean
    - `language` — string — Language the recogniser identified for this chunk. Recorded in the trace only; drives no behavior. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - `time` — number **(required)**
- `ReplyWebsocketEvent` — ReplyWebsocketEvent
  - `type` — string **(required)** _(default=event)_
  - `event` — ReplyEvent **(required)**
    - `type` — object **(required)**
    - `id` — string **(required)**
    - `text` — string **(required)**
    - `language` — string — Language the recogniser identified for this completed utterance; drives the language switch. When several languages are reported inside one utterance the PBX sends the last labelled segment's. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - `confidence` — number — Aggregated transcription confidence of the phrase this reply was built from, weighted by word count over the transcription chunks that carry a confidence value. Absent when no chunk had one, for example on DTMF input. _(format=double; min=-1; max=1)_
    - `startTime` — number **(required)**
    - `endTime` — number **(required)**
- `PlaybackWebsocketEvent` — PlaybackWebsocketEvent
  - `type` — string **(required)** _(default=event)_
  - `event` — PlaybackEvent **(required)**
    - `type` — object **(required)**
    - `replyId` — string **(required)**
    - `text` — string **(required)**
    - `complete` — boolean **(required)**
    - `startTime` — number **(required)**
    - `endTime` — number
- `InterruptionWebsocketEvent` — InterruptionWebsocketEvent
  - `type` — string **(required)** _(default=event)_
  - `event` — InterruptionEvent **(required)**
    - `type` — object **(required)**
    - `replyId` — string **(required)**
    - `playedText` — string **(required)**
    - `originalText` — string **(required)**
    - `time` — number **(required)**
- `CompleteWebsocketEvent` — CompleteWebsocketEvent
  - `type` — string **(required)** _(default=event)_
  - `event` — CompleteEvent **(required)**
    - `type` — object **(required)**
    - `reason` — string **(required)**
    - `time` — number **(required)**
- `SayWebsocketCommand` — SayWebsocketCommand
  - `type` — string **(required)** _(default=command)_
  - `command` — SayWebsocketCommandData **(required)**
    - `text` — string **(required)**
    - `replyId` — string **(required)**
    - `interruptible` — boolean
    - `voice` — string — Bare Amazon Polly voice id, e.g. 'Joanna' — NOT a URI. The PBX consumes this verbatim as the AMI `Voice=` action parameter, so it takes exactly what Polly names the voice, with the `amazon_polly://` scheme and any query parameters already stripped by whoever builds this command out of the bot's stored `VoiceBotVoiceUri`. Set only for a provider whose synthesis runs ON THE PBX (Amazon Polly); ElevenLabs and Google are synthesized in the cloud and streamed as PCM through `play` instead, and leave this absent. _(pattern=^[A-Za-z0-9]+$; minLen=1; maxLen=64)_
    - `audio` — SayCommandAudioOptions
      - `streamId` — string **(required)**
      - `sampleRate` — number **(required)**
    - `type` — object **(required)**
- `PlayWebsocketCommand` — PlayWebsocketCommand
  - `type` — string **(required)** _(default=command)_
  - `command` — PlayWebsocketCommandData **(required)**
    - `replyId` — string **(required)**
    - `streamId` — string **(required)**
    - `data` — string **(required)** — The audio chunk is encoded in base64 and should be played in the stream. The chunk must use the sample rate specified in the "say" command and be PCM encoded.
    - `type` — object **(required)**
- `StopWebsocketCommand` — StopWebsocketCommand
  - `type` — string **(required)** _(default=command)_
  - `command` — StopWebsocketCommandData **(required)**
    - `type` — object **(required)**
- `HangupWebsocketCommand` — HangupWebsocketCommand
  - `type` — string **(required)** _(default=command)_
  - `command` — HangupWebsocketCommandData **(required)**
    - `reason` — string
    - `type` — object **(required)**
- `TransferWebsocketCommand` — TransferWebsocketCommand
  - `type` — string **(required)** _(default=command)_
  - `command` — TransferWebsocketCommandData **(required)**
    - `context` — string **(required)**
    - `extension` — string **(required)**
    - `type` — object **(required)**
- `SessionStartedWebhookEvent` — SessionStartedWebhookEvent
  - `sessionId` — string **(required)**
  - `botId` — string **(required)**
  - `callId` — string **(required)**
  - `flowIndex` — number **(required)**
  - `id` — string **(required)** — A unique identifier for the call, combined from companyID and callID. Uses the same format as "id" in calls webhooks.
  - `pbx` — string — PBX serial of the voicebot session source.
  - `company` — string — Company identifier of the voicebot session source. _(minLen=3; maxLen=30)_
  - `event` — SessionStartedEvent **(required)**
    - `type` — object **(required)**
    - `language` — string **(required)** — The language code that represents the language spoken in the session.
    - `callerNumber` — string — Caller's phone number.
    - `dialedNumber` — string — Number dialed to reach the voice bot.
    - `variables` — SessionVariables
      - _map of_ `string`
    - `time` — number **(required)**
- `SessionEndedWebhookEvent` — SessionEndedWebhookEvent
  - `sessionId` — string **(required)**
  - `botId` — string **(required)**
  - `callId` — string **(required)**
  - `flowIndex` — number **(required)**
  - `id` — string **(required)** — A unique identifier for the call, combined from companyID and callID. Uses the same format as "id" in calls webhooks.
  - `pbx` — string — PBX serial of the voicebot session source.
  - `company` — string — Company identifier of the voicebot session source. _(minLen=3; maxLen=30)_
  - `event` — SessionEndedEvent **(required)**
    - `type` — object **(required)**
    - `error` — string
    - `time` — number **(required)**
- `TranscriptionWebhookEvent` — TranscriptionWebhookEvent
  - `sessionId` — string **(required)**
  - `botId` — string **(required)**
  - `callId` — string **(required)**
  - `flowIndex` — number **(required)**
  - `id` — string **(required)** — A unique identifier for the call, combined from companyID and callID. Uses the same format as "id" in calls webhooks.
  - `pbx` — string — PBX serial of the voicebot session source.
  - `company` — string — Company identifier of the voicebot session source. _(minLen=3; maxLen=30)_
  - `event` — TranscriptionEvent **(required)**
    - `type` — object **(required)**
    - `id` — string **(required)**
    - `text` — string **(required)**
    - `confidence` — number — Transcription confidence score (accuracy level) in range from 0.0 to 1.0. Value -1.0 indicates confidence is unavailable. _(format=double; min=-1; max=1)_
    - `final` — boolean
    - `language` — string — Language the recogniser identified for this chunk. Recorded in the trace only; drives no behavior. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - `time` — number **(required)**
- `AudioWebhookEvent` — AudioWebhookEvent
  - `sessionId` — string **(required)**
  - `botId` — string **(required)**
  - `callId` — string **(required)**
  - `flowIndex` — number **(required)**
  - `id` — string **(required)** — A unique identifier for the call, combined from companyID and callID. Uses the same format as "id" in calls webhooks.
  - `pbx` — string — PBX serial of the voicebot session source.
  - `company` — string — Company identifier of the voicebot session source. _(minLen=3; maxLen=30)_
  - `event` — AudioEvent **(required)**
    - `type` — object **(required)**
    - `data` — string **(required)** — Audio chunk with a specified sample rate defined in the session.
- `ReplyWebhookEvent` — ReplyWebhookEvent
  - `sessionId` — string **(required)**
  - `botId` — string **(required)**
  - `callId` — string **(required)**
  - `flowIndex` — number **(required)**
  - `id` — string **(required)** — A unique identifier for the call, combined from companyID and callID. Uses the same format as "id" in calls webhooks.
  - `pbx` — string — PBX serial of the voicebot session source.
  - `company` — string — Company identifier of the voicebot session source. _(minLen=3; maxLen=30)_
  - `event` — ReplyEvent **(required)**
    - `type` — object **(required)**
    - `id` — string **(required)**
    - `text` — string **(required)**
    - `language` — string — Language the recogniser identified for this completed utterance; drives the language switch. When several languages are reported inside one utterance the PBX sends the last labelled segment's. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - `confidence` — number — Aggregated transcription confidence of the phrase this reply was built from, weighted by word count over the transcription chunks that carry a confidence value. Absent when no chunk had one, for example on DTMF input. _(format=double; min=-1; max=1)_
    - `startTime` — number **(required)**
    - `endTime` — number **(required)**
- `PlaybackWebhookEvent` — PlaybackWebhookEvent
  - `sessionId` — string **(required)**
  - `botId` — string **(required)**
  - `callId` — string **(required)**
  - `flowIndex` — number **(required)**
  - `id` — string **(required)** — A unique identifier for the call, combined from companyID and callID. Uses the same format as "id" in calls webhooks.
  - `pbx` — string — PBX serial of the voicebot session source.
  - `company` — string — Company identifier of the voicebot session source. _(minLen=3; maxLen=30)_
  - `event` — PlaybackEvent **(required)**
    - `type` — object **(required)**
    - `replyId` — string **(required)**
    - `text` — string **(required)**
    - `complete` — boolean **(required)**
    - `startTime` — number **(required)**
    - `endTime` — number
- `InterruptionWebhookEvent` — InterruptionWebhookEvent
  - `sessionId` — string **(required)**
  - `botId` — string **(required)**
  - `callId` — string **(required)**
  - `flowIndex` — number **(required)**
  - `id` — string **(required)** — A unique identifier for the call, combined from companyID and callID. Uses the same format as "id" in calls webhooks.
  - `pbx` — string — PBX serial of the voicebot session source.
  - `company` — string — Company identifier of the voicebot session source. _(minLen=3; maxLen=30)_
  - `event` — InterruptionEvent **(required)**
    - `type` — object **(required)**
    - `replyId` — string **(required)**
    - `playedText` — string **(required)**
    - `originalText` — string **(required)**
    - `time` — number **(required)**
- `CompleteWebhookEvent` — CompleteWebhookEvent
  - `sessionId` — string **(required)**
  - `botId` — string **(required)**
  - `callId` — string **(required)**
  - `flowIndex` — number **(required)**
  - `id` — string **(required)** — A unique identifier for the call, combined from companyID and callID. Uses the same format as "id" in calls webhooks.
  - `pbx` — string — PBX serial of the voicebot session source.
  - `company` — string — Company identifier of the voicebot session source. _(minLen=3; maxLen=30)_
  - `event` — CompleteEvent **(required)**
    - `type` — object **(required)**
    - `reason` — string **(required)**
    - `time` — number **(required)**
- `PubSubBroadcastWebsocketEvent` — PubSubBroadcastWebsocketEvent
  - `event` — string **(required)**
  - `topic` — string **(required)**
  - `items` — array **(required)**
    - _array of_ `PubSubBroadcastItem`
      - `session` — TraceSession
        - _(nesting depth limit — see `TraceSession` in the Schemas appendix)_
      - `sessionId` — string
      - `activity` — TraceActivity
        - _(nesting depth limit — see `TraceActivity` in the Schemas appendix)_
      - `segment` — TraceSegment
        - _(nesting depth limit — see `TraceSegment` in the Schemas appendix)_
- `PubSubSubscribeWebsocketCommand` — PubSubSubscribeWebsocketCommand
  - `action` — string **(required)**
  - `topic` — string **(required)**
- `PubSubSubscribedWebsocketEvent` — PubSubSubscribedWebsocketEvent
  - `event` — string **(required)**
  - `topic` — string **(required)**
- `PubSubUnsubscribeWebsocketCommand` — PubSubUnsubscribeWebsocketCommand
  - `action` — string **(required)**
  - `topic` — string **(required)**
- `PubSubUnsubscribedWebsocketEvent` — PubSubUnsubscribedWebsocketEvent
  - `event` — string **(required)**
  - `topic` — string **(required)**

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GetTraceResponseContent`**

- `trace` — Trace **(required)**
  - `session` — TraceSession **(required)**
    - `sessionId` — string **(required)**
    - `connectionId` — string **(required)**
    - `company` — string **(required)**
    - `botId` — string **(required)**
    - `botName` — string **(required)**
    - `callId` — string **(required)**
    - `flowIndex` — number **(required)**
    - `language` — string
    - `callerName` — string
    - `callerNumber` — string
    - `status` — string **(required)** _(enum: `complete`, `complete_with_error`, `pending`)_
    - `start` — number **(required)** _(format=double)_
    - `duration` — number
  - `activities` — array **(required)**
    - _array of_ `TraceActivity`
      - `id` — string **(required)**
      - `version` — number **(required)**
      - `status` — string **(required)** _(enum: `pending`, `error`, `complete`, `cancelled`)_
      - `trigger` — union **(required)**
        - _(nesting depth limit — see `TraceActivityTrigger` in the Schemas appendix)_
      - `result` — union
        - _(nesting depth limit — see `TraceActivityResult` in the Schemas appendix)_
      - `start` — number **(required)** _(format=double)_
      - `duration` — number
      - `timings` — TraceTimings
        - _(nesting depth limit — see `TraceTimings` in the Schemas appendix)_
      - `usage` — TraceUsage
        - _(nesting depth limit — see `TraceUsage` in the Schemas appendix)_
  - `segments` — array **(required)**
    - _array of_ `TraceSegment`
      - `id` — string **(required)**
      - `activityId` — string **(required)**
      - `version` — number **(required)**
      - `status` — string **(required)** _(enum: `pending`, `error`, `complete`)_
      - `input` — union **(required)**
        - _(nesting depth limit — see `TraceSegmentInput` in the Schemas appendix)_
      - `result` — union
        - _(nesting depth limit — see `TraceSegmentResult` in the Schemas appendix)_
      - `start` — number **(required)** _(format=double)_
      - `duration` — number
  - `usage` — TraceUsage
    - `generation` — TraceGenerationUsage
      - `tokens` — number
      - `outputTokens` — number
      - `inputTokens` — number
      - `cachedInputTokens` — number
      - `reasoningTokens` — number
      - `category` — string
    - `transcribe` — TraceTranscribeUsage
      - `seconds` — number
      - `category` — string
    - `playback` — TracePlaybackUsage
      - `chars` — number
      - `category` — string
  - `cost` — number _(format=float)_

**`GetVoiceBotResponseContent`**

- `bot` — VoiceBot **(required)**
  - `name` — string **(required)** _(minLen=3; maxLen=255)_
  - `category` — string — Category of the bot _(minLen=1; maxLen=128)_
  - `message` — string — The initial message that will be played at the start of the session.
  - `pipeline` — VoiceBotPipelineSettings
    - `interuptionsEnabled` — boolean — If enabled the user can interrupt the the bot playback.
    - `maximumDuration` — number — The maximum number of seconds a call will last.
    - `maximumDurationAction` — union
      - _oneOf_ — exactly one of:
        - **`hangup`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`transfer`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `silenceTimeout` — number — How long to wait before a call is automatically ended due to inactivity.
    - `silenceTimeoutAction` — union
      - _oneOf_ — exactly one of:
        - **`hangup`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`transfer`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `endCallEnabled` — boolean — If enabled the bot can hangup the call.
    - `endCallPhases` — string — A list of phases separated by comma, which will end the call matched.
  - `speech` — VoiceBotSpeechSettings — Speech configuration. When present it wins over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the exception.
    - `languages` — array **(required)** — Configured languages. The @length bound is a storage ceiling; the real cap is the recogniser's own candidate limit, enforced in the service. _(minItems=1; maxItems=10)_
      - _array of_ `VoiceBotLanguage`
        - _(nesting depth limit — see `VoiceBotLanguage` in the Schemas appendix)_
    - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in its own language's voice, provider account and pronunciation rules. Languages with an empty first message, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
    - `transcription` — VoiceBotTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
      - `engine` — string — Recogniser to transcribe the caller with. Absent resolves to the platform default ('aws://transcribe' today), resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
      - `autoDetect` — boolean — Identify the caller's language per utterance and switch voice and reply language mid-call. HERE RATHER THAN ON `VoiceBotSpeechSettings`, because identifying a language is something the RECOGNISER does: it becomes identify-multiple-languages plus language-options on the recognition stream, and nothing about synthesis reads it. Requires at least two configured languages and a recogniser that can identify them; the server clamps it to false otherwise, because forwarding true with a single candidate makes Amazon reject the stream outright.
  - `backgroundSound` — VoiceBotBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT rather than a loose name on the bot, matching `wildix.wilma.agents`: it is one switchable call behaviour, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
    - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
    - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
  - `endpoint` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`llm`**
        - `llm` — VoiceBotLlmEndpoint **(required)**
          - _(nesting depth limit — see `VoiceBotLlmEndpoint` in the Schemas appendix)_
      - **`dialogflowCx`**
        - `dialogflowCx` — BotDialogflowCxEndpoint **(required)**
          - _(nesting depth limit — see `BotDialogflowCxEndpoint` in the Schemas appendix)_
      - **`openAiAssistant`**
        - `openAiAssistant` — BotOpenAiAssistantEndpoint **(required)**
          - _(nesting depth limit — see `BotOpenAiAssistantEndpoint` in the Schemas appendix)_
      - **`webhook`**
        - `webhook` — BotWebhookEndpoint **(required)**
          - _(nesting depth limit — see `BotWebhookEndpoint` in the Schemas appendix)_
      - **`sqs`**
        - `sqs` — BotSqsEndpoint **(required)**
          - _(nesting depth limit — see `BotSqsEndpoint` in the Schemas appendix)_
  - `capabilities` — array
    - _array of_ `VoiceBotCapability`
      - _oneOf_ — exactly one of:
        - **`tool`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`kb`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`HangupWebsocketCommand`**

- `type` — string **(required)** _(default=command)_
- `command` — HangupWebsocketCommandData **(required)**
  - `reason` — string
  - `type` — object **(required)**

**`HangupWebsocketCommandData`**

- `reason` — string
- `type` — object **(required)**

**`InterruptionEvent`**

- `type` — object **(required)**
- `replyId` — string **(required)**
- `playedText` — string **(required)**
- `originalText` — string **(required)**
- `time` — number **(required)**

**`InterruptionWebhookEvent`**

- `sessionId` — string **(required)**
- `botId` — string **(required)**
- `callId` — string **(required)**
- `flowIndex` — number **(required)**
- `id` — string **(required)** — A unique identifier for the call, combined from companyID and callID. Uses the same format as "id" in calls webhooks.
- `pbx` — string — PBX serial of the voicebot session source.
- `company` — string — Company identifier of the voicebot session source. _(minLen=3; maxLen=30)_
- `event` — InterruptionEvent **(required)**
  - `type` — object **(required)**
  - `replyId` — string **(required)**
  - `playedText` — string **(required)**
  - `originalText` — string **(required)**
  - `time` — number **(required)**

**`InterruptionWebsocketEvent`**

- `type` — string **(required)** _(default=event)_
- `event` — InterruptionEvent **(required)**
  - `type` — object **(required)**
  - `replyId` — string **(required)**
  - `playedText` — string **(required)**
  - `originalText` — string **(required)**
  - `time` — number **(required)**

**`ListTracesResponseContent`**

- `traces` — array **(required)**
  - _array of_ `TraceSession`
    - `sessionId` — string **(required)**
    - `connectionId` — string **(required)**
    - `company` — string **(required)**
    - `botId` — string **(required)**
    - `botName` — string **(required)**
    - `callId` — string **(required)**
    - `flowIndex` — number **(required)**
    - `language` — string
    - `callerName` — string
    - `callerNumber` — string
    - `status` — string **(required)** _(enum: `complete`, `complete_with_error`, `pending`)_
    - `start` — number **(required)** _(format=double)_
    - `duration` — number

**`ListVoiceBotsNamesResponseContent`**

- `bots` — array **(required)**
  - _array of_ `VoiceBotInfo`
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `name` — string **(required)** _(minLen=3; maxLen=255)_
    - `speechConfigured` — boolean — Whether the voice channel has at least one configured speech language. A dialplan form partitions its application lists on this, so the answer has to travel with the list rather than cost one lookup per entry — it is the reason this member exists and the reason removing it broke that form. Absent is read as false.

**`ListVoiceBotsResponseContent`**

- `bots` — array **(required)**
  - _array of_ `VoiceBot`
    - `name` — string **(required)** _(minLen=3; maxLen=255)_
    - `category` — string — Category of the bot _(minLen=1; maxLen=128)_
    - `message` — string — The initial message that will be played at the start of the session.
    - `pipeline` — VoiceBotPipelineSettings
      - `interuptionsEnabled` — boolean — If enabled the user can interrupt the the bot playback.
      - `maximumDuration` — number — The maximum number of seconds a call will last.
      - `maximumDurationAction` — union
        - _(nesting depth limit — see `VoiceBotPipelineTerminateAction` in the Schemas appendix)_
      - `silenceTimeout` — number — How long to wait before a call is automatically ended due to inactivity.
      - `silenceTimeoutAction` — union
        - _(nesting depth limit — see `VoiceBotPipelineTerminateAction` in the Schemas appendix)_
      - `endCallEnabled` — boolean — If enabled the bot can hangup the call.
      - `endCallPhases` — string — A list of phases separated by comma, which will end the call matched.
    - `speech` — VoiceBotSpeechSettings — Speech configuration. When present it wins over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the exception.
      - `languages` — array **(required)** — Configured languages. The @length bound is a storage ceiling; the real cap is the recogniser's own candidate limit, enforced in the service. _(minItems=1; maxItems=10)_
        - _(nesting depth limit — see `VoiceBotLanguage` in the Schemas appendix)_
      - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in its own language's voice, provider account and pronunciation rules. Languages with an empty first message, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
      - `transcription` — VoiceBotTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
        - _(nesting depth limit — see `VoiceBotTranscriptionSettings` in the Schemas appendix)_
    - `backgroundSound` — VoiceBotBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT rather than a loose name on the bot, matching `wildix.wilma.agents`: it is one switchable call behaviour, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
      - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
      - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
    - `endpoint` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`llm`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`dialogflowCx`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`openAiAssistant`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`webhook`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sqs`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `capabilities` — array
      - _array of_ `VoiceBotCapability`
        - _(nesting depth limit — see `VoiceBotCapability` in the Schemas appendix)_
    - `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string

**`ListVoicesResponseContent`**

- `voices` — array **(required)**
  - _array of_ `VoiceBotVoice`
    - `uri` — string **(required)** — Voice URI, ready to store as `VoiceBotLanguage.voice` or send to TextToSpeech. The caller appends the synthesis parameters and, for a custom provider account, `apiKey=...` before storing it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
    - `name` — string **(required)** — Display name as the provider publishes it, e.g. 'Rachel'. A member rather than part of `metadata` because it is the one thing every provider has and every picker shows.
    - `metadata` — any — The provider's own metadata for this voice, for rendering and filtering only. See VoiceBotVoiceMetadata.

**`PlayWebsocketCommand`**

- `type` — string **(required)** _(default=command)_
- `command` — PlayWebsocketCommandData **(required)**
  - `replyId` — string **(required)**
  - `streamId` — string **(required)**
  - `data` — string **(required)** — The audio chunk is encoded in base64 and should be played in the stream. The chunk must use the sample rate specified in the "say" command and be PCM encoded.
  - `type` — object **(required)**

**`PlayWebsocketCommandData`**

- `replyId` — string **(required)**
- `streamId` — string **(required)**
- `data` — string **(required)** — The audio chunk is encoded in base64 and should be played in the stream. The chunk must use the sample rate specified in the "say" command and be PCM encoded.
- `type` — object **(required)**

**`PlaybackEvent`**

- `type` — object **(required)**
- `replyId` — string **(required)**
- `text` — string **(required)**
- `complete` — boolean **(required)**
- `startTime` — number **(required)**
- `endTime` — number

**`PlaybackWebhookEvent`**

- `sessionId` — string **(required)**
- `botId` — string **(required)**
- `callId` — string **(required)**
- `flowIndex` — number **(required)**
- `id` — string **(required)** — A unique identifier for the call, combined from companyID and callID. Uses the same format as "id" in calls webhooks.
- `pbx` — string — PBX serial of the voicebot session source.
- `company` — string — Company identifier of the voicebot session source. _(minLen=3; maxLen=30)_
- `event` — PlaybackEvent **(required)**
  - `type` — object **(required)**
  - `replyId` — string **(required)**
  - `text` — string **(required)**
  - `complete` — boolean **(required)**
  - `startTime` — number **(required)**
  - `endTime` — number

**`PlaybackWebsocketEvent`**

- `type` — string **(required)** _(default=event)_
- `event` — PlaybackEvent **(required)**
  - `type` — object **(required)**
  - `replyId` — string **(required)**
  - `text` — string **(required)**
  - `complete` — boolean **(required)**
  - `startTime` — number **(required)**
  - `endTime` — number

**`PubSubBroadcastItem`**

- `session` — TraceSession
  - `sessionId` — string **(required)**
  - `connectionId` — string **(required)**
  - `company` — string **(required)**
  - `botId` — string **(required)**
  - `botName` — string **(required)**
  - `callId` — string **(required)**
  - `flowIndex` — number **(required)**
  - `language` — string
  - `callerName` — string
  - `callerNumber` — string
  - `status` — string **(required)** _(enum: `complete`, `complete_with_error`, `pending`)_
  - `start` — number **(required)** _(format=double)_
  - `duration` — number
- `sessionId` — string
- `activity` — TraceActivity
  - `id` — string **(required)**
  - `version` — number **(required)**
  - `status` — string **(required)** _(enum: `pending`, `error`, `complete`, `cancelled`)_
  - `trigger` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`connectEvent`**
        - `connectEvent` — TraceConnectEventTrigger **(required)**
          - _(nesting depth limit — see `TraceConnectEventTrigger` in the Schemas appendix)_
      - **`disconnectEvent`**
        - `disconnectEvent` — TraceDisconnectEventTrigger **(required)**
          - _(nesting depth limit — see `TraceDisconnectEventTrigger` in the Schemas appendix)_
      - **`replyEvent`**
        - `replyEvent` — ReplyWebsocketEvent **(required)**
          - _(nesting depth limit — see `ReplyWebsocketEvent` in the Schemas appendix)_
      - **`completeEvent`**
        - `completeEvent` — CompleteWebsocketEvent **(required)**
          - _(nesting depth limit — see `CompleteWebsocketEvent` in the Schemas appendix)_
      - **`interruptionEvent`**
        - `interruptionEvent` — InterruptionWebsocketEvent **(required)**
          - _(nesting depth limit — see `InterruptionWebsocketEvent` in the Schemas appendix)_
      - **`playbackEvent`**
        - `playbackEvent` — PlaybackWebsocketEvent **(required)**
          - _(nesting depth limit — see `PlaybackWebsocketEvent` in the Schemas appendix)_
      - **`transcriptionEvent`**
        - `transcriptionEvent` — TranscriptionWebsocketEvent **(required)**
          - _(nesting depth limit — see `TranscriptionWebsocketEvent` in the Schemas appendix)_
      - **`sayCommand`**
        - `sayCommand` — SayWebsocketCommand **(required)**
          - _(nesting depth limit — see `SayWebsocketCommand` in the Schemas appendix)_
      - **`hangupCommand`**
        - `hangupCommand` — HangupWebsocketCommand **(required)**
          - _(nesting depth limit — see `HangupWebsocketCommand` in the Schemas appendix)_
      - **`transferCommand`**
        - `transferCommand` — TransferWebsocketCommand **(required)**
          - _(nesting depth limit — see `TransferWebsocketCommand` in the Schemas appendix)_
      - **`annotationCommand`**
        - `annotationCommand` — TraceAnnotationCommand **(required)** — Trace activity written when the voicebot emits an annotation.
          - _(nesting depth limit — see `TraceAnnotationCommand` in the Schemas appendix)_
      - **`silenceTimeoutTask`**
        - `silenceTimeoutTask` — TraceSilenceTimeoutTaskTrigger **(required)**
          - _(nesting depth limit — see `TraceSilenceTimeoutTaskTrigger` in the Schemas appendix)_
      - **`durationTimeoutTask`**
        - `durationTimeoutTask` — TraceDurationTimeoutTaskTrigger **(required)**
          - _(nesting depth limit — see `TraceDurationTimeoutTaskTrigger` in the Schemas appendix)_
  - `result` — union
    - _oneOf_ — exactly one of:
      - **`error`**
        - `error` — TraceErrorResult **(required)**
          - _(nesting depth limit — see `TraceErrorResult` in the Schemas appendix)_
      - **`text`**
        - `text` — string **(required)**
  - `start` — number **(required)** _(format=double)_
  - `duration` — number
  - `timings` — TraceTimings
    - _map of_ `number`
  - `usage` — TraceUsage
    - `generation` — TraceGenerationUsage
      - `tokens` — number
      - `outputTokens` — number
      - `inputTokens` — number
      - `cachedInputTokens` — number
      - `reasoningTokens` — number
      - `category` — string
    - `transcribe` — TraceTranscribeUsage
      - `seconds` — number
      - `category` — string
    - `playback` — TracePlaybackUsage
      - `chars` — number
      - `category` — string
- `segment` — TraceSegment
  - `id` — string **(required)**
  - `activityId` — string **(required)**
  - `version` — number **(required)**
  - `status` — string **(required)** _(enum: `pending`, `error`, `complete`)_
  - `input` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`completion`**
        - `completion` — TraceSegmentCompletionInput **(required)**
          - _(nesting depth limit — see `TraceSegmentCompletionInput` in the Schemas appendix)_
      - **`tool`**
        - `tool` — union **(required)**
          - _(nesting depth limit — see `TraceToolCall` in the Schemas appendix)_
      - **`oauth`**
        - `oauth` — TraceOAuthInput **(required)**
          - _(nesting depth limit — see `TraceOAuthInput` in the Schemas appendix)_
      - **`generic`**
        - `generic` — TraceGenericInput **(required)**
          - _(nesting depth limit — see `TraceGenericInput` in the Schemas appendix)_
  - `result` — union
    - _oneOf_ — exactly one of:
      - **`error`**
        - `error` — TraceErrorResult **(required)**
          - _(nesting depth limit — see `TraceErrorResult` in the Schemas appendix)_
      - **`tools`**
        - `tools` — array **(required)**
          - _(nesting depth limit — see `TraceToolCall` in the Schemas appendix)_
      - **`text`**
        - `text` — string **(required)**
      - **`json`**
        - `json` — any **(required)**
  - `start` — number **(required)** _(format=double)_
  - `duration` — number

**`PubSubBroadcastWebsocketEvent`**

- `event` — string **(required)**
- `topic` — string **(required)**
- `items` — array **(required)**
  - _array of_ `PubSubBroadcastItem`
    - `session` — TraceSession
      - `sessionId` — string **(required)**
      - `connectionId` — string **(required)**
      - `company` — string **(required)**
      - `botId` — string **(required)**
      - `botName` — string **(required)**
      - `callId` — string **(required)**
      - `flowIndex` — number **(required)**
      - `language` — string
      - `callerName` — string
      - `callerNumber` — string
      - `status` — string **(required)** _(enum: `complete`, `complete_with_error`, `pending`)_
      - `start` — number **(required)** _(format=double)_
      - `duration` — number
    - `sessionId` — string
    - `activity` — TraceActivity
      - `id` — string **(required)**
      - `version` — number **(required)**
      - `status` — string **(required)** _(enum: `pending`, `error`, `complete`, `cancelled`)_
      - `trigger` — union **(required)**
        - _(nesting depth limit — see `TraceActivityTrigger` in the Schemas appendix)_
      - `result` — union
        - _(nesting depth limit — see `TraceActivityResult` in the Schemas appendix)_
      - `start` — number **(required)** _(format=double)_
      - `duration` — number
      - `timings` — TraceTimings
        - _(nesting depth limit — see `TraceTimings` in the Schemas appendix)_
      - `usage` — TraceUsage
        - _(nesting depth limit — see `TraceUsage` in the Schemas appendix)_
    - `segment` — TraceSegment
      - `id` — string **(required)**
      - `activityId` — string **(required)**
      - `version` — number **(required)**
      - `status` — string **(required)** _(enum: `pending`, `error`, `complete`)_
      - `input` — union **(required)**
        - _(nesting depth limit — see `TraceSegmentInput` in the Schemas appendix)_
      - `result` — union
        - _(nesting depth limit — see `TraceSegmentResult` in the Schemas appendix)_
      - `start` — number **(required)** _(format=double)_
      - `duration` — number

**`PubSubSubscribeWebsocketCommand`**

- `action` — string **(required)**
- `topic` — string **(required)**

**`PubSubSubscribedWebsocketEvent`**

- `event` — string **(required)**
- `topic` — string **(required)**

**`PubSubUnsubscribeWebsocketCommand`**

- `action` — string **(required)**
- `topic` — string **(required)**

**`PubSubUnsubscribedWebsocketEvent`**

- `event` — string **(required)**
- `topic` — string **(required)**

**`ReplyEvent`**

- `type` — object **(required)**
- `id` — string **(required)**
- `text` — string **(required)**
- `language` — string — Language the recogniser identified for this completed utterance; drives the language switch. When several languages are reported inside one utterance the PBX sends the last labelled segment's. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `confidence` — number — Aggregated transcription confidence of the phrase this reply was built from, weighted by word count over the transcription chunks that carry a confidence value. Absent when no chunk had one, for example on DTMF input. _(format=double; min=-1; max=1)_
- `startTime` — number **(required)**
- `endTime` — number **(required)**

**`ReplyWebhookEvent`**

- `sessionId` — string **(required)**
- `botId` — string **(required)**
- `callId` — string **(required)**
- `flowIndex` — number **(required)**
- `id` — string **(required)** — A unique identifier for the call, combined from companyID and callID. Uses the same format as "id" in calls webhooks.
- `pbx` — string — PBX serial of the voicebot session source.
- `company` — string — Company identifier of the voicebot session source. _(minLen=3; maxLen=30)_
- `event` — ReplyEvent **(required)**
  - `type` — object **(required)**
  - `id` — string **(required)**
  - `text` — string **(required)**
  - `language` — string — Language the recogniser identified for this completed utterance; drives the language switch. When several languages are reported inside one utterance the PBX sends the last labelled segment's. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
  - `confidence` — number — Aggregated transcription confidence of the phrase this reply was built from, weighted by word count over the transcription chunks that carry a confidence value. Absent when no chunk had one, for example on DTMF input. _(format=double; min=-1; max=1)_
  - `startTime` — number **(required)**
  - `endTime` — number **(required)**

**`ReplyWebsocketEvent`**

- `type` — string **(required)** _(default=event)_
- `event` — ReplyEvent **(required)**
  - `type` — object **(required)**
  - `id` — string **(required)**
  - `text` — string **(required)**
  - `language` — string — Language the recogniser identified for this completed utterance; drives the language switch. When several languages are reported inside one utterance the PBX sends the last labelled segment's. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
  - `confidence` — number — Aggregated transcription confidence of the phrase this reply was built from, weighted by word count over the transcription chunks that carry a confidence value. Absent when no chunk had one, for example on DTMF input. _(format=double; min=-1; max=1)_
  - `startTime` — number **(required)**
  - `endTime` — number **(required)**

**`SayCommandAudioOptions`**

- `streamId` — string **(required)**
- `sampleRate` — number **(required)**

**`SayWebsocketCommand`**

- `type` — string **(required)** _(default=command)_
- `command` — SayWebsocketCommandData **(required)**
  - `text` — string **(required)**
  - `replyId` — string **(required)**
  - `interruptible` — boolean
  - `voice` — string — Bare Amazon Polly voice id, e.g. 'Joanna' — NOT a URI. The PBX consumes this verbatim as the AMI `Voice=` action parameter, so it takes exactly what Polly names the voice, with the `amazon_polly://` scheme and any query parameters already stripped by whoever builds this command out of the bot's stored `VoiceBotVoiceUri`. Set only for a provider whose synthesis runs ON THE PBX (Amazon Polly); ElevenLabs and Google are synthesized in the cloud and streamed as PCM through `play` instead, and leave this absent. _(pattern=^[A-Za-z0-9]+$; minLen=1; maxLen=64)_
  - `audio` — SayCommandAudioOptions
    - `streamId` — string **(required)**
    - `sampleRate` — number **(required)**
  - `type` — object **(required)**

**`SayWebsocketCommandData`**

- `text` — string **(required)**
- `replyId` — string **(required)**
- `interruptible` — boolean
- `voice` — string — Bare Amazon Polly voice id, e.g. 'Joanna' — NOT a URI. The PBX consumes this verbatim as the AMI `Voice=` action parameter, so it takes exactly what Polly names the voice, with the `amazon_polly://` scheme and any query parameters already stripped by whoever builds this command out of the bot's stored `VoiceBotVoiceUri`. Set only for a provider whose synthesis runs ON THE PBX (Amazon Polly); ElevenLabs and Google are synthesized in the cloud and streamed as PCM through `play` instead, and leave this absent. _(pattern=^[A-Za-z0-9]+$; minLen=1; maxLen=64)_
- `audio` — SayCommandAudioOptions
  - `streamId` — string **(required)**
  - `sampleRate` — number **(required)**
- `type` — object **(required)**

**`SearchStrategy`**

- string _(enum: `bm25`, `vector`, `hybrid`)_

**`SearchThresholdValue`**

- string _(enum: `low`, `medium`, `high`)_

**`SendHangupRequestContent`**

- `reason` — string

**`SendPlayRequestContent`**

- `replyId` — string **(required)**
- `streamId` — string **(required)**
- `data` — string **(required)** — The audio chunk is encoded in base64 and should be played in the stream. The chunk must use the sample rate specified in the "say" command and be PCM encoded.

**`SendSayRequestContent`**

- `text` — string **(required)**
- `replyId` — string **(required)**
- `interruptible` — boolean
- `voice` — string — Bare Amazon Polly voice id, e.g. 'Joanna' — NOT a URI. The PBX consumes this verbatim as the AMI `Voice=` action parameter, so it takes exactly what Polly names the voice, with the `amazon_polly://` scheme and any query parameters already stripped by whoever builds this command out of the bot's stored `VoiceBotVoiceUri`. Set only for a provider whose synthesis runs ON THE PBX (Amazon Polly); ElevenLabs and Google are synthesized in the cloud and streamed as PCM through `play` instead, and leave this absent. _(pattern=^[A-Za-z0-9]+$; minLen=1; maxLen=64)_
- `audio` — SayCommandAudioOptions
  - `streamId` — string **(required)**
  - `sampleRate` — number **(required)**

**`SendTransferRequestContent`**

- `context` — string **(required)**
- `extension` — string **(required)**

**`SessionEndedEvent`**

- `type` — object **(required)**
- `error` — string
- `time` — number **(required)**

**`SessionEndedWebhookEvent`**

- `sessionId` — string **(required)**
- `botId` — string **(required)**
- `callId` — string **(required)**
- `flowIndex` — number **(required)**
- `id` — string **(required)** — A unique identifier for the call, combined from companyID and callID. Uses the same format as "id" in calls webhooks.
- `pbx` — string — PBX serial of the voicebot session source.
- `company` — string — Company identifier of the voicebot session source. _(minLen=3; maxLen=30)_
- `event` — SessionEndedEvent **(required)**
  - `type` — object **(required)**
  - `error` — string
  - `time` — number **(required)**

**`SessionStartedEvent`**

- `type` — object **(required)**
- `language` — string **(required)** — The language code that represents the language spoken in the session.
- `callerNumber` — string — Caller's phone number.
- `dialedNumber` — string — Number dialed to reach the voice bot.
- `variables` — SessionVariables
  - _map of_ `string`
- `time` — number **(required)**

**`SessionStartedWebhookEvent`**

- `sessionId` — string **(required)**
- `botId` — string **(required)**
- `callId` — string **(required)**
- `flowIndex` — number **(required)**
- `id` — string **(required)** — A unique identifier for the call, combined from companyID and callID. Uses the same format as "id" in calls webhooks.
- `pbx` — string — PBX serial of the voicebot session source.
- `company` — string — Company identifier of the voicebot session source. _(minLen=3; maxLen=30)_
- `event` — SessionStartedEvent **(required)**
  - `type` — object **(required)**
  - `language` — string **(required)** — The language code that represents the language spoken in the session.
  - `callerNumber` — string — Caller's phone number.
  - `dialedNumber` — string — Number dialed to reach the voice bot.
  - `variables` — SessionVariables
    - _map of_ `string`
  - `time` — number **(required)**

**`SessionStartedWebsocketEvent`**

- `type` — string **(required)** _(default=event)_
- `event` — SessionStartedWebsocketEventData **(required)**
  - `type` — object **(required)**
  - `botId` — string **(required)**
  - `botName` — string **(required)**
  - `category` — string
  - `groupId` — string
  - `speech` — VoiceBotSpeechPayload — Recognition intent for the call, sent on `started` at protocol version >= 2. Not recogniser parameters: the PBX translates it into its provider's API. `engine` is always concrete and `autoDetect` is already clamped by the server, because forwarding true with a single candidate makes Amazon reject the stream outright.
    - `engine` — string **(required)** — Concrete recogniser URI, resolved from the bot or from the platform default; never absent. See VoiceBotTranscriptionUri. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
    - `languages` — array **(required)** — Every configured language, as candidates for identification.
      - _array of_ `string`
    - `preferredLanguage` — string **(required)** — The language the call starts in, resolved from the channel. Always a member of `languages`. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - `autoDetect` — boolean **(required)**
  - `backgroundSound` — string — Music-on-hold class the PBX should play under the call as ambient background. A BARE NAME, not the configuration object `VoiceBotBackgroundSoundSettings`: this is the RESOLVED outcome. The server has already applied `enabled` and the class default, so the PBX gets a name to play or nothing at all and needs no resolution rule of its own. TOP LEVEL, NOT INSIDE `speech`, because it is not recognition intent and must not inherit `speech`'s conditions: a call with no configured languages carries no `speech` payload and can still have background audio. ABSENT MEANS OFF, and absence is the only way to say it — there is no value for 'none'. A bot whose administrator never touched the setting sends nothing here, which is exactly what every call sent before it existed, so the PBX needs no new case. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
  - `time` — number **(required)**

**`SessionStartedWebsocketEventData`**

- `type` — object **(required)**
- `botId` — string **(required)**
- `botName` — string **(required)**
- `category` — string
- `groupId` — string
- `speech` — VoiceBotSpeechPayload — Recognition intent for the call, sent on `started` at protocol version >= 2. Not recogniser parameters: the PBX translates it into its provider's API. `engine` is always concrete and `autoDetect` is already clamped by the server, because forwarding true with a single candidate makes Amazon reject the stream outright.
  - `engine` — string **(required)** — Concrete recogniser URI, resolved from the bot or from the platform default; never absent. See VoiceBotTranscriptionUri. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
  - `languages` — array **(required)** — Every configured language, as candidates for identification.
    - _array of_ `string`
  - `preferredLanguage` — string **(required)** — The language the call starts in, resolved from the channel. Always a member of `languages`. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
  - `autoDetect` — boolean **(required)**
- `backgroundSound` — string — Music-on-hold class the PBX should play under the call as ambient background. A BARE NAME, not the configuration object `VoiceBotBackgroundSoundSettings`: this is the RESOLVED outcome. The server has already applied `enabled` and the class default, so the PBX gets a name to play or nothing at all and needs no resolution rule of its own. TOP LEVEL, NOT INSIDE `speech`, because it is not recognition intent and must not inherit `speech`'s conditions: a call with no configured languages carries no `speech` payload and can still have background audio. ABSENT MEANS OFF, and absence is the only way to say it — there is no value for 'none'. A bot whose administrator never touched the setting sends nothing here, which is exactly what every call sent before it existed, so the PBX needs no new case. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
- `time` — number **(required)**

**`SessionVariables`**

- _map of_ `string`

**`StopWebsocketCommand`**

- `type` — string **(required)** _(default=command)_
- `command` — StopWebsocketCommandData **(required)**
  - `type` — object **(required)**

**`StopWebsocketCommandData`**

- `type` — object **(required)**

**`TextToSpeechOutputPayload`**

_The call path streams raw PCM to the PBX; this returns MP3 so a browser <audio> element plays it with no client-side decoding._

- string

**`TextToSpeechRequestContent`**

- `voice` — string **(required)** — Voice to speak with, as the URI a call would use — provider, voice id, synthesis parameters and, for a custom account, `apiKey`. Passing the call's own value is what keeps an audition from diverging from the call it is auditioning. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
- `language` — string **(required)** — Language the phrase is in. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `text` — string **(required)** — Text to speak, before pronunciation rules are applied. _(minLen=1; maxLen=2000)_
- `pronunciations` — array — Pronunciation rules for this language, applied SERVER-SIDE by the same helper the call path uses — never pre-applied by the caller, or the form reimplements a rule the server owns and can silently diverge from the call. _(maxItems=200)_
  - _array of_ `VoiceBotPronunciation`
    - `phrase` — string **(required)** — The written form to replace. Bounded because every rule is compiled into ONE regular expression — see the list below. _(maxLen=200)_
    - `as` — string **(required)** — Respelling (ALIAS) or phonetic transcription (IPA). _(maxLen=200)_
    - `encoding` — string _(enum: `alias`, `ipa`)_
- `botId` — string — The bot whose language this audition speaks for. Resolves the language's STORED private key server-side when that language's key is masked (`apiKey=stored`) rather than the caller round-tripping a key it was never given back. The key itself is never returned — it is used only to authenticate against the provider. _(minLen=12; maxLen=12)_

**`Trace`**

- `session` — TraceSession **(required)**
  - `sessionId` — string **(required)**
  - `connectionId` — string **(required)**
  - `company` — string **(required)**
  - `botId` — string **(required)**
  - `botName` — string **(required)**
  - `callId` — string **(required)**
  - `flowIndex` — number **(required)**
  - `language` — string
  - `callerName` — string
  - `callerNumber` — string
  - `status` — string **(required)** _(enum: `complete`, `complete_with_error`, `pending`)_
  - `start` — number **(required)** _(format=double)_
  - `duration` — number
- `activities` — array **(required)**
  - _array of_ `TraceActivity`
    - `id` — string **(required)**
    - `version` — number **(required)**
    - `status` — string **(required)** _(enum: `pending`, `error`, `complete`, `cancelled`)_
    - `trigger` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`connectEvent`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`disconnectEvent`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`replyEvent`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`completeEvent`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`interruptionEvent`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`playbackEvent`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`transcriptionEvent`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sayCommand`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`hangupCommand`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`transferCommand`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`annotationCommand`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`silenceTimeoutTask`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`durationTimeoutTask`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `result` — union
      - _oneOf_ — exactly one of:
        - **`error`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`text`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `start` — number **(required)** _(format=double)_
    - `duration` — number
    - `timings` — TraceTimings
      - _map of_ `number`
    - `usage` — TraceUsage
      - `generation` — TraceGenerationUsage
        - _(nesting depth limit — see `TraceGenerationUsage` in the Schemas appendix)_
      - `transcribe` — TraceTranscribeUsage
        - _(nesting depth limit — see `TraceTranscribeUsage` in the Schemas appendix)_
      - `playback` — TracePlaybackUsage
        - _(nesting depth limit — see `TracePlaybackUsage` in the Schemas appendix)_
- `segments` — array **(required)**
  - _array of_ `TraceSegment`
    - `id` — string **(required)**
    - `activityId` — string **(required)**
    - `version` — number **(required)**
    - `status` — string **(required)** _(enum: `pending`, `error`, `complete`)_
    - `input` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`completion`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`tool`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`oauth`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`generic`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `result` — union
      - _oneOf_ — exactly one of:
        - **`error`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`tools`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`text`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`json`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `start` — number **(required)** _(format=double)_
    - `duration` — number
- `usage` — TraceUsage
  - `generation` — TraceGenerationUsage
    - `tokens` — number
    - `outputTokens` — number
    - `inputTokens` — number
    - `cachedInputTokens` — number
    - `reasoningTokens` — number
    - `category` — string
  - `transcribe` — TraceTranscribeUsage
    - `seconds` — number
    - `category` — string
  - `playback` — TracePlaybackUsage
    - `chars` — number
    - `category` — string
- `cost` — number _(format=float)_

**`TraceActivity`**

- `id` — string **(required)**
- `version` — number **(required)**
- `status` — string **(required)** _(enum: `pending`, `error`, `complete`, `cancelled`)_
- `trigger` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`connectEvent`**
      - `connectEvent` — TraceConnectEventTrigger **(required)**
        - `parameters` — any
    - **`disconnectEvent`**
      - `disconnectEvent` — TraceDisconnectEventTrigger **(required)**
        - `parameters` — any
    - **`replyEvent`**
      - `replyEvent` — ReplyWebsocketEvent **(required)**
        - `type` — string **(required)** _(default=event)_
        - `event` — ReplyEvent **(required)**
          - _(nesting depth limit — see `ReplyEvent` in the Schemas appendix)_
    - **`completeEvent`**
      - `completeEvent` — CompleteWebsocketEvent **(required)**
        - `type` — string **(required)** _(default=event)_
        - `event` — CompleteEvent **(required)**
          - _(nesting depth limit — see `CompleteEvent` in the Schemas appendix)_
    - **`interruptionEvent`**
      - `interruptionEvent` — InterruptionWebsocketEvent **(required)**
        - `type` — string **(required)** _(default=event)_
        - `event` — InterruptionEvent **(required)**
          - _(nesting depth limit — see `InterruptionEvent` in the Schemas appendix)_
    - **`playbackEvent`**
      - `playbackEvent` — PlaybackWebsocketEvent **(required)**
        - `type` — string **(required)** _(default=event)_
        - `event` — PlaybackEvent **(required)**
          - _(nesting depth limit — see `PlaybackEvent` in the Schemas appendix)_
    - **`transcriptionEvent`**
      - `transcriptionEvent` — TranscriptionWebsocketEvent **(required)**
        - `type` — string **(required)** _(default=event)_
        - `event` — TranscriptionEvent **(required)**
          - _(nesting depth limit — see `TranscriptionEvent` in the Schemas appendix)_
    - **`sayCommand`**
      - `sayCommand` — SayWebsocketCommand **(required)**
        - `type` — string **(required)** _(default=command)_
        - `command` — SayWebsocketCommandData **(required)**
          - _(nesting depth limit — see `SayWebsocketCommandData` in the Schemas appendix)_
    - **`hangupCommand`**
      - `hangupCommand` — HangupWebsocketCommand **(required)**
        - `type` — string **(required)** _(default=command)_
        - `command` — HangupWebsocketCommandData **(required)**
          - _(nesting depth limit — see `HangupWebsocketCommandData` in the Schemas appendix)_
    - **`transferCommand`**
      - `transferCommand` — TransferWebsocketCommand **(required)**
        - `type` — string **(required)** _(default=command)_
        - `command` — TransferWebsocketCommandData **(required)**
          - _(nesting depth limit — see `TransferWebsocketCommandData` in the Schemas appendix)_
    - **`annotationCommand`**
      - `annotationCommand` — TraceAnnotationCommand **(required)** — Trace activity written when the voicebot emits an annotation.
        - `annotation` — Annotation **(required)**
          - _(nesting depth limit — see `Annotation` in the Schemas appendix)_
    - **`silenceTimeoutTask`**
      - `silenceTimeoutTask` — TraceSilenceTimeoutTaskTrigger **(required)**
        - `parameters` — any
    - **`durationTimeoutTask`**
      - `durationTimeoutTask` — TraceDurationTimeoutTaskTrigger **(required)**
        - `parameters` — any
- `result` — union
  - _oneOf_ — exactly one of:
    - **`error`**
      - `error` — TraceErrorResult **(required)**
        - `internal` — boolean **(required)**
        - `message` — string **(required)**
    - **`text`**
      - `text` — string **(required)**
- `start` — number **(required)** _(format=double)_
- `duration` — number
- `timings` — TraceTimings
  - _map of_ `number`
- `usage` — TraceUsage
  - `generation` — TraceGenerationUsage
    - `tokens` — number
    - `outputTokens` — number
    - `inputTokens` — number
    - `cachedInputTokens` — number
    - `reasoningTokens` — number
    - `category` — string
  - `transcribe` — TraceTranscribeUsage
    - `seconds` — number
    - `category` — string
  - `playback` — TracePlaybackUsage
    - `chars` — number
    - `category` — string

**`TraceActivityResult`**

- _oneOf_ — exactly one of:
  - **`error`**
    - `error` — TraceErrorResult **(required)**
      - `internal` — boolean **(required)**
      - `message` — string **(required)**
  - **`text`**
    - `text` — string **(required)**

**`TraceActivityStatus`**

- string _(enum: `pending`, `error`, `complete`, `cancelled`)_

**`TraceActivityTrigger`**

- _oneOf_ — exactly one of:
  - **`connectEvent`**
    - `connectEvent` — TraceConnectEventTrigger **(required)**
      - `parameters` — any
  - **`disconnectEvent`**
    - `disconnectEvent` — TraceDisconnectEventTrigger **(required)**
      - `parameters` — any
  - **`replyEvent`**
    - `replyEvent` — ReplyWebsocketEvent **(required)**
      - `type` — string **(required)** _(default=event)_
      - `event` — ReplyEvent **(required)**
        - `type` — object **(required)**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `id` — string **(required)**
        - `text` — string **(required)**
        - `language` — string — Language the recogniser identified for this completed utterance; drives the language switch. When several languages are reported inside one utterance the PBX sends the last labelled segment's. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
        - `confidence` — number — Aggregated transcription confidence of the phrase this reply was built from, weighted by word count over the transcription chunks that carry a confidence value. Absent when no chunk had one, for example on DTMF input. _(format=double; min=-1; max=1)_
        - `startTime` — number **(required)**
        - `endTime` — number **(required)**
  - **`completeEvent`**
    - `completeEvent` — CompleteWebsocketEvent **(required)**
      - `type` — string **(required)** _(default=event)_
      - `event` — CompleteEvent **(required)**
        - `type` — object **(required)**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `reason` — string **(required)**
        - `time` — number **(required)**
  - **`interruptionEvent`**
    - `interruptionEvent` — InterruptionWebsocketEvent **(required)**
      - `type` — string **(required)** _(default=event)_
      - `event` — InterruptionEvent **(required)**
        - `type` — object **(required)**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `replyId` — string **(required)**
        - `playedText` — string **(required)**
        - `originalText` — string **(required)**
        - `time` — number **(required)**
  - **`playbackEvent`**
    - `playbackEvent` — PlaybackWebsocketEvent **(required)**
      - `type` — string **(required)** _(default=event)_
      - `event` — PlaybackEvent **(required)**
        - `type` — object **(required)**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `replyId` — string **(required)**
        - `text` — string **(required)**
        - `complete` — boolean **(required)**
        - `startTime` — number **(required)**
        - `endTime` — number
  - **`transcriptionEvent`**
    - `transcriptionEvent` — TranscriptionWebsocketEvent **(required)**
      - `type` — string **(required)** _(default=event)_
      - `event` — TranscriptionEvent **(required)**
        - `type` — object **(required)**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `id` — string **(required)**
        - `text` — string **(required)**
        - `confidence` — number — Transcription confidence score (accuracy level) in range from 0.0 to 1.0. Value -1.0 indicates confidence is unavailable. _(format=double; min=-1; max=1)_
        - `final` — boolean
        - `language` — string — Language the recogniser identified for this chunk. Recorded in the trace only; drives no behavior. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
        - `time` — number **(required)**
  - **`sayCommand`**
    - `sayCommand` — SayWebsocketCommand **(required)**
      - `type` — string **(required)** _(default=command)_
      - `command` — SayWebsocketCommandData **(required)**
        - `text` — string **(required)**
        - `replyId` — string **(required)**
        - `interruptible` — boolean
        - `voice` — string — Bare Amazon Polly voice id, e.g. 'Joanna' — NOT a URI. The PBX consumes this verbatim as the AMI `Voice=` action parameter, so it takes exactly what Polly names the voice, with the `amazon_polly://` scheme and any query parameters already stripped by whoever builds this command out of the bot's stored `VoiceBotVoiceUri`. Set only for a provider whose synthesis runs ON THE PBX (Amazon Polly); ElevenLabs and Google are synthesized in the cloud and streamed as PCM through `play` instead, and leave this absent. _(pattern=^[A-Za-z0-9]+$; minLen=1; maxLen=64)_
        - `audio` — SayCommandAudioOptions
          - _(nesting depth limit — see `SayCommandAudioOptions` in the Schemas appendix)_
        - `type` — object **(required)**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - **`hangupCommand`**
    - `hangupCommand` — HangupWebsocketCommand **(required)**
      - `type` — string **(required)** _(default=command)_
      - `command` — HangupWebsocketCommandData **(required)**
        - `reason` — string
        - `type` — object **(required)**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - **`transferCommand`**
    - `transferCommand` — TransferWebsocketCommand **(required)**
      - `type` — string **(required)** _(default=command)_
      - `command` — TransferWebsocketCommandData **(required)**
        - `context` — string **(required)**
        - `extension` — string **(required)**
        - `type` — object **(required)**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - **`annotationCommand`**
    - `annotationCommand` — TraceAnnotationCommand **(required)** — Trace activity written when the voicebot emits an annotation.
      - `annotation` — Annotation **(required)**
        - `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
        - `time` — number **(required)**
        - `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
        - `payload` — union **(required)**
          - _(nesting depth limit — see `AnnotationPayload` in the Schemas appendix)_
        - `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
          - _(nesting depth limit — see `AnnotationSource` in the Schemas appendix)_
  - **`silenceTimeoutTask`**
    - `silenceTimeoutTask` — TraceSilenceTimeoutTaskTrigger **(required)**
      - `parameters` — any
  - **`durationTimeoutTask`**
    - `durationTimeoutTask` — TraceDurationTimeoutTaskTrigger **(required)**
      - `parameters` — any

**`TraceAnnotationCommand`**

_Trace activity written when the voicebot emits an annotation._

- `annotation` — Annotation **(required)**
  - `id` — string **(required)** — Identity of this emission. Annotations are applied once per id: re-sending one already recorded on the conversation is ignored.
  - `time` — number **(required)**
  - `key` — string — Identity of the value, when the annotation is one reading of something that changes over the conversation. See AnnotationKey. _(pattern=^[a-z0-9][a-z0-9_.-]*$; maxLen=100)_
  - `payload` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`tag`**
        - `tag` — string **(required)** _(maxLen=50)_
      - **`text`**
        - `text` — string **(required)** _(maxLen=4096)_
      - **`variables`**
        - `variables` — AnnotationVariablesValue **(required)** — Capability variable values captured for an annotation. Runtime services enforce serialized payload size limits.
          - _(nesting depth limit — see `AnnotationVariablesValue` in the Schemas appendix)_
      - **`result`**
        - `result` — AnnotationResultValue **(required)** — Tool result captured for an annotation. Runtime services enforce serialized payload size limits.
          - _(nesting depth limit — see `AnnotationResultValue` in the Schemas appendix)_
      - **`metric`**
        - `metric` — AnnotationMetricValue **(required)** — A named value observed during the conversation, and the reading it replaces — a CSAT score, a talk ratio, the outcome of an evaluation. Emitted with an `AnnotationKey`, which is what makes the newest reading addressable in `annotationsByKey` while the series stays in `annotations`. Runtime services enforce serialized payload size limits.
          - _(nesting depth limit — see `AnnotationMetricValue` in the Schemas appendix)_
  - `source` — AnnotationSource **(required)** — Producer of an annotation. Generic identifiers allow callers to attach context such as tool id/name, user id/name, etc., without constraining the source type to a fixed shape.
    - `type` — string **(required)** _(enum: `chatbot`, `voicebot`, `user`, `system`, `copilot`)_
    - `id` — string — Stable identifier of the producer (e.g. tool id, user id, copilot session id).
    - `name` — string — Human-readable name of the producer (e.g. tool name, user display name).

**`TraceCapabilityKbCall`**

_Knowledge base capability call segment for trace._

- `name` — string
- `args` — string

**`TraceCapabilityToolCall`**

_Capability tool call (wim-tools) segment for trace._

- `name` — string
- `args` — string

**`TraceConnectEventTrigger`**

- `parameters` — any

**`TraceDelegationToolCall`**

- `id` — string

**`TraceDisconnectEventTrigger`**

- `parameters` — any

**`TraceDurationTimeoutTaskTrigger`**

- `parameters` — any

**`TraceErrorResult`**

- `internal` — boolean **(required)**
- `message` — string **(required)**

**`TraceFunctionToolCall`**

- `name` — string
- `args` — string
- `request` — TraceFunctionToolCallRequest
  - `url` — string
  - `method` — string
  - `headers` — TraceSegmentRequestInputHeaders
    - _map of_ `string`
  - `body` — string

**`TraceFunctionToolCallRequest`**

- `url` — string
- `method` — string
- `headers` — TraceSegmentRequestInputHeaders
  - _map of_ `string`
- `body` — string

**`TraceGenerationUsage`**

- `tokens` — number
- `outputTokens` — number
- `inputTokens` — number
- `cachedInputTokens` — number
- `reasoningTokens` — number
- `category` — string

**`TraceGenericInput`**

- `title` — string **(required)**
- `blocks` — array
  - _array of_ `TraceGenericInputBlock`
    - `title` — string **(required)**
    - `content` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`text`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`json`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_

**`TraceGenericInputBlock`**

- `title` — string **(required)**
- `content` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`text`**
      - `text` — string **(required)**
    - **`json`**
      - `json` — any **(required)**

**`TraceGenericInputBlockContent`**

- _oneOf_ — exactly one of:
  - **`text`**
    - `text` — string **(required)**
  - **`json`**
    - `json` — any **(required)**

**`TraceHangupToolCall`**

- TraceHangupToolCall

**`TraceOAuthInput`**

- `clientId` — string
- `clientSecret` — string
- `endpointUrl` — string
- `scope` — string

**`TracePlaybackUsage`**

- `chars` — number
- `category` — string

**`TraceSegment`**

- `id` — string **(required)**
- `activityId` — string **(required)**
- `version` — number **(required)**
- `status` — string **(required)** _(enum: `pending`, `error`, `complete`)_
- `input` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`completion`**
      - `completion` — TraceSegmentCompletionInput **(required)**
        - `instructions` — string **(required)**
        - `messages` — array **(required)**
          - _(nesting depth limit — see `TraceSegmentCompletionMessageItem` in the Schemas appendix)_
        - `model` — string
    - **`tool`**
      - `tool` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`transfer`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`hangup`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`wait`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`delegation`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`function`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`capabilityTool`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`capabilityKb`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - **`oauth`**
      - `oauth` — TraceOAuthInput **(required)**
        - `clientId` — string
        - `clientSecret` — string
        - `endpointUrl` — string
        - `scope` — string
    - **`generic`**
      - `generic` — TraceGenericInput **(required)**
        - `title` — string **(required)**
        - `blocks` — array
          - _(nesting depth limit — see `TraceGenericInputBlock` in the Schemas appendix)_
- `result` — union
  - _oneOf_ — exactly one of:
    - **`error`**
      - `error` — TraceErrorResult **(required)**
        - `internal` — boolean **(required)**
        - `message` — string **(required)**
    - **`tools`**
      - `tools` — array **(required)**
        - _array of_ `TraceToolCall`
          - _(nesting depth limit — see `TraceToolCall` in the Schemas appendix)_
    - **`text`**
      - `text` — string **(required)**
    - **`json`**
      - `json` — any **(required)**
- `start` — number **(required)** _(format=double)_
- `duration` — number

**`TraceSegmentCompletionInput`**

- `instructions` — string **(required)**
- `messages` — array **(required)**
  - _array of_ `TraceSegmentCompletionMessageItem`
    - _oneOf_ — exactly one of:
      - **`user`**
        - `user` — union **(required)**
          - _(nesting depth limit — see `TraceSegmentCompletionMessage` in the Schemas appendix)_
      - **`bot`**
        - `bot` — union **(required)**
          - _(nesting depth limit — see `TraceSegmentCompletionMessage` in the Schemas appendix)_
- `model` — string

**`TraceSegmentCompletionMessage`**

- _oneOf_ — exactly one of:
  - **`text`**
    - `text` — string **(required)**
  - **`tools`**
    - `tools` — array **(required)**
      - _array of_ `TraceSegmentCompletionToolMessage`
        - `call` — union
          - _(nesting depth limit — see `TraceToolCall` in the Schemas appendix)_
        - `result` — string

**`TraceSegmentCompletionMessageItem`**

- _oneOf_ — exactly one of:
  - **`user`**
    - `user` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`text`**
          - `text` — string **(required)**
        - **`tools`**
          - `tools` — array **(required)**
            - _(nesting depth limit — see `TraceSegmentCompletionToolMessage` in the Schemas appendix)_
  - **`bot`**
    - `bot` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`text`**
          - `text` — string **(required)**
        - **`tools`**
          - `tools` — array **(required)**
            - _(nesting depth limit — see `TraceSegmentCompletionToolMessage` in the Schemas appendix)_

**`TraceSegmentCompletionToolMessage`**

- `call` — union
  - _oneOf_ — exactly one of:
    - **`transfer`**
      - `transfer` — TraceTransferToolCall **(required)**
        - `context` — string
        - `extension` — string
    - **`hangup`**
      - `hangup` — TraceHangupToolCall **(required)**
    - **`wait`**
      - `wait` — TraceWaitToolCall **(required)**
    - **`delegation`**
      - `delegation` — TraceDelegationToolCall **(required)**
        - `id` — string
    - **`function`**
      - `function` — TraceFunctionToolCall **(required)**
        - `name` — string
        - `args` — string
        - `request` — TraceFunctionToolCallRequest
          - _(nesting depth limit — see `TraceFunctionToolCallRequest` in the Schemas appendix)_
    - **`capabilityTool`**
      - `capabilityTool` — TraceCapabilityToolCall **(required)** — Capability tool call (wim-tools) segment for trace.
        - `name` — string
        - `args` — string
    - **`capabilityKb`**
      - `capabilityKb` — TraceCapabilityKbCall **(required)** — Knowledge base capability call segment for trace.
        - `name` — string
        - `args` — string
- `result` — string

**`TraceSegmentInput`**

- _oneOf_ — exactly one of:
  - **`completion`**
    - `completion` — TraceSegmentCompletionInput **(required)**
      - `instructions` — string **(required)**
      - `messages` — array **(required)**
        - _array of_ `TraceSegmentCompletionMessageItem`
          - _(nesting depth limit — see `TraceSegmentCompletionMessageItem` in the Schemas appendix)_
      - `model` — string
  - **`tool`**
    - `tool` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`transfer`**
          - `transfer` — TraceTransferToolCall **(required)**
            - _(nesting depth limit — see `TraceTransferToolCall` in the Schemas appendix)_
        - **`hangup`**
          - `hangup` — TraceHangupToolCall **(required)**
        - **`wait`**
          - `wait` — TraceWaitToolCall **(required)**
        - **`delegation`**
          - `delegation` — TraceDelegationToolCall **(required)**
            - _(nesting depth limit — see `TraceDelegationToolCall` in the Schemas appendix)_
        - **`function`**
          - `function` — TraceFunctionToolCall **(required)**
            - _(nesting depth limit — see `TraceFunctionToolCall` in the Schemas appendix)_
        - **`capabilityTool`**
          - `capabilityTool` — TraceCapabilityToolCall **(required)** — Capability tool call (wim-tools) segment for trace.
            - _(nesting depth limit — see `TraceCapabilityToolCall` in the Schemas appendix)_
        - **`capabilityKb`**
          - `capabilityKb` — TraceCapabilityKbCall **(required)** — Knowledge base capability call segment for trace.
            - _(nesting depth limit — see `TraceCapabilityKbCall` in the Schemas appendix)_
  - **`oauth`**
    - `oauth` — TraceOAuthInput **(required)**
      - `clientId` — string
      - `clientSecret` — string
      - `endpointUrl` — string
      - `scope` — string
  - **`generic`**
    - `generic` — TraceGenericInput **(required)**
      - `title` — string **(required)**
      - `blocks` — array
        - _array of_ `TraceGenericInputBlock`
          - _(nesting depth limit — see `TraceGenericInputBlock` in the Schemas appendix)_

**`TraceSegmentRequestInputHeaders`**

- _map of_ `string`

**`TraceSegmentResult`**

- _oneOf_ — exactly one of:
  - **`error`**
    - `error` — TraceErrorResult **(required)**
      - `internal` — boolean **(required)**
      - `message` — string **(required)**
  - **`tools`**
    - `tools` — array **(required)**
      - _array of_ `TraceToolCall`
        - _oneOf_ — exactly one of:
          - **`transfer`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`hangup`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`wait`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`delegation`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`function`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`capabilityTool`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`capabilityKb`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - **`text`**
    - `text` — string **(required)**
  - **`json`**
    - `json` — any **(required)**

**`TraceSegmentStatus`**

- string _(enum: `pending`, `error`, `complete`)_

**`TraceSession`**

- `sessionId` — string **(required)**
- `connectionId` — string **(required)**
- `company` — string **(required)**
- `botId` — string **(required)**
- `botName` — string **(required)**
- `callId` — string **(required)**
- `flowIndex` — number **(required)**
- `language` — string
- `callerName` — string
- `callerNumber` — string
- `status` — string **(required)** _(enum: `complete`, `complete_with_error`, `pending`)_
- `start` — number **(required)** _(format=double)_
- `duration` — number

**`TraceSessionStatus`**

- string _(enum: `complete`, `complete_with_error`, `pending`)_

**`TraceSilenceTimeoutTaskTrigger`**

- `parameters` — any

**`TraceTimings`**

- _map of_ `number`

**`TraceToolCall`**

- _oneOf_ — exactly one of:
  - **`transfer`**
    - `transfer` — TraceTransferToolCall **(required)**
      - `context` — string
      - `extension` — string
  - **`hangup`**
    - `hangup` — TraceHangupToolCall **(required)**
  - **`wait`**
    - `wait` — TraceWaitToolCall **(required)**
  - **`delegation`**
    - `delegation` — TraceDelegationToolCall **(required)**
      - `id` — string
  - **`function`**
    - `function` — TraceFunctionToolCall **(required)**
      - `name` — string
      - `args` — string
      - `request` — TraceFunctionToolCallRequest
        - `url` — string
        - `method` — string
        - `headers` — TraceSegmentRequestInputHeaders
          - _(nesting depth limit — see `TraceSegmentRequestInputHeaders` in the Schemas appendix)_
        - `body` — string
  - **`capabilityTool`**
    - `capabilityTool` — TraceCapabilityToolCall **(required)** — Capability tool call (wim-tools) segment for trace.
      - `name` — string
      - `args` — string
  - **`capabilityKb`**
    - `capabilityKb` — TraceCapabilityKbCall **(required)** — Knowledge base capability call segment for trace.
      - `name` — string
      - `args` — string

**`TraceTranscribeUsage`**

- `seconds` — number
- `category` — string

**`TraceTransferToolCall`**

- `context` — string
- `extension` — string

**`TraceUsage`**

- `generation` — TraceGenerationUsage
  - `tokens` — number
  - `outputTokens` — number
  - `inputTokens` — number
  - `cachedInputTokens` — number
  - `reasoningTokens` — number
  - `category` — string
- `transcribe` — TraceTranscribeUsage
  - `seconds` — number
  - `category` — string
- `playback` — TracePlaybackUsage
  - `chars` — number
  - `category` — string

**`TraceWaitToolCall`**

- TraceWaitToolCall

**`TranscriptionEvent`**

- `type` — object **(required)**
- `id` — string **(required)**
- `text` — string **(required)**
- `confidence` — number — Transcription confidence score (accuracy level) in range from 0.0 to 1.0. Value -1.0 indicates confidence is unavailable. _(format=double; min=-1; max=1)_
- `final` — boolean
- `language` — string — Language the recogniser identified for this chunk. Recorded in the trace only; drives no behavior. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `time` — number **(required)**

**`TranscriptionWebhookEvent`**

- `sessionId` — string **(required)**
- `botId` — string **(required)**
- `callId` — string **(required)**
- `flowIndex` — number **(required)**
- `id` — string **(required)** — A unique identifier for the call, combined from companyID and callID. Uses the same format as "id" in calls webhooks.
- `pbx` — string — PBX serial of the voicebot session source.
- `company` — string — Company identifier of the voicebot session source. _(minLen=3; maxLen=30)_
- `event` — TranscriptionEvent **(required)**
  - `type` — object **(required)**
  - `id` — string **(required)**
  - `text` — string **(required)**
  - `confidence` — number — Transcription confidence score (accuracy level) in range from 0.0 to 1.0. Value -1.0 indicates confidence is unavailable. _(format=double; min=-1; max=1)_
  - `final` — boolean
  - `language` — string — Language the recogniser identified for this chunk. Recorded in the trace only; drives no behavior. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
  - `time` — number **(required)**

**`TranscriptionWebsocketEvent`**

- `type` — string **(required)** _(default=event)_
- `event` — TranscriptionEvent **(required)**
  - `type` — object **(required)**
  - `id` — string **(required)**
  - `text` — string **(required)**
  - `confidence` — number — Transcription confidence score (accuracy level) in range from 0.0 to 1.0. Value -1.0 indicates confidence is unavailable. _(format=double; min=-1; max=1)_
  - `final` — boolean
  - `language` — string — Language the recogniser identified for this chunk. Recorded in the trace only; drives no behavior. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
  - `time` — number **(required)**

**`TransferWebsocketCommand`**

- `type` — string **(required)** _(default=command)_
- `command` — TransferWebsocketCommandData **(required)**
  - `context` — string **(required)**
  - `extension` — string **(required)**
  - `type` — object **(required)**

**`TransferWebsocketCommandData`**

- `context` — string **(required)**
- `extension` — string **(required)**
- `type` — object **(required)**

**`UpdateVoiceBotRequestContent`**

- `name` — string **(required)** _(minLen=3; maxLen=255)_
- `category` — string — Category of the bot _(minLen=1; maxLen=128)_
- `message` — string — The initial message that will be played at the start of the session.
- `pipeline` — VoiceBotPipelineSettings
  - `interuptionsEnabled` — boolean — If enabled the user can interrupt the the bot playback.
  - `maximumDuration` — number — The maximum number of seconds a call will last.
  - `maximumDurationAction` — union
    - _oneOf_ — exactly one of:
      - **`hangup`**
        - `hangup` — VoiceBotTerminateHangupAction **(required)**
      - **`transfer`**
        - `transfer` — VoiceBotTerminateTransferAction **(required)**
          - _(nesting depth limit — see `VoiceBotTerminateTransferAction` in the Schemas appendix)_
  - `silenceTimeout` — number — How long to wait before a call is automatically ended due to inactivity.
  - `silenceTimeoutAction` — union
    - _oneOf_ — exactly one of:
      - **`hangup`**
        - `hangup` — VoiceBotTerminateHangupAction **(required)**
      - **`transfer`**
        - `transfer` — VoiceBotTerminateTransferAction **(required)**
          - _(nesting depth limit — see `VoiceBotTerminateTransferAction` in the Schemas appendix)_
  - `endCallEnabled` — boolean — If enabled the bot can hangup the call.
  - `endCallPhases` — string — A list of phases separated by comma, which will end the call matched.
- `speech` — VoiceBotSpeechSettings — Speech configuration. When present it wins over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the exception.
  - `languages` — array **(required)** — Configured languages. The @length bound is a storage ceiling; the real cap is the recogniser's own candidate limit, enforced in the service. _(minItems=1; maxItems=10)_
    - _array of_ `VoiceBotLanguage`
      - `code` — string **(required)** — BCP-47 code with locale, e.g. 'en-US'. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `voice` — string **(required)** — Voice this language speaks with, as a URI — provider, voice id, synthesis parameters and, where the company uses its own provider account, its `apiKey` query parameter. See VoiceBotVoiceUri. PER LANGUAGE, and that is the whole reason the member is here rather than on the settings above: provider quality is not uniform across languages, a voice id belongs to exactly one provider, and a bot-wide provider made changing it invalidate every configured voice at once. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
      - `greeting` — string — Initial phrase for this language. Absent or empty means the agent says nothing and waits — it does NOT fall back to the agent-level message, which would speak one language's text in another language's voice.
      - `isDefault` — boolean — Marks the language a caller hears when their own matches nothing configured. THE FULL RESOLUTION ORDER, since a client author reading only this contract cannot otherwise find it: an exact match on the call's language, then a match on its primary subtag (`fr` finds `fr-FR`), then the language marked here, then a language whose primary subtag is `en`, then the first entry in the list. Marked is consulted BEFORE the English step, so a record with none marked resolves exactly as it did before this member existed. English is deliberate rather than arbitrary — it is the language a caller the agent was not built for is likeliest to understand — and the last step exists only to keep the rule total, which is why list order should not be treated as configuration. At most one language may carry it. A record with two — reachable through the API or the CLI, where no form prevents it — resolves to the first marked one in list order, because refusing a call over configuration drift is worse than serving it and saying so in the trace.
      - `pronunciations` — array — Pronunciation rules for one language. BOUNDED, and the bound is not decoration. `applyPronunciations` compiles every rule of a language into a SINGLE alternating regular expression, so the cost is the pattern's total size: measured against the real escaping and matching logic, 1,000 rules cost ~0.9 s of CPU per synthesized sentence, 5,000 cost ~4.9 s, and around 10,000 `new RegExp` throws V8's pattern-size error outright — from a call site outside the surrounding `try`, so a 500 rather than a degraded reply. Stored on a bot, that made every utterance of the agent fail. 200 is far above any real use — a product glossary is a handful of names — and far below where either cost begins. Found by a security review. NO LOWER BOUND on `phrase` or `as`, deliberately. Both consoles add an EMPTY rule row the moment someone clicks 'Add pronunciation', so a `min: 1` would make saving an agent with a half-typed row fail entirely — and the runtime already ignores a rule with no phrase. Dropping blank rows belongs in the consoles' save filters, not in a refusal here. _(maxItems=200)_
        - _(nesting depth limit — see `VoiceBotPronunciation` in the Schemas appendix)_
  - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in its own language's voice, provider account and pronunciation rules. Languages with an empty first message, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
  - `transcription` — VoiceBotTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
    - `engine` — string — Recogniser to transcribe the caller with. Absent resolves to the platform default ('aws://transcribe' today), resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
    - `autoDetect` — boolean — Identify the caller's language per utterance and switch voice and reply language mid-call. HERE RATHER THAN ON `VoiceBotSpeechSettings`, because identifying a language is something the RECOGNISER does: it becomes identify-multiple-languages plus language-options on the recognition stream, and nothing about synthesis reads it. Requires at least two configured languages and a recogniser that can identify them; the server clamps it to false otherwise, because forwarding true with a single candidate makes Amazon reject the stream outright.
- `backgroundSound` — VoiceBotBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT rather than a loose name on the bot, matching `wildix.wilma.agents`: it is one switchable call behaviour, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
  - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
  - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
- `endpoint` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`llm`**
      - `llm` — VoiceBotLlmEndpoint **(required)**
        - `prompt` — string **(required)** _(maxLen=40000)_
        - `model` — string — The AI model to use for generating responses. If not specified, uses the default model. _(default=default; pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
        - `guidelines` — array
          - _array of_ `string`
        - `metadata` — VoiceBotPromptMetadata
          - _(nesting depth limit — see `VoiceBotPromptMetadata` in the Schemas appendix)_
        - `embeddedTools` — array — Embedded functions to use within voice session.
          - _(nesting depth limit — see `VoiceBotEmbeddedTool` in the Schemas appendix)_
        - `tools` — array — Custom tools to be used within voice session.
          - _(nesting depth limit — see `VoiceBotTool` in the Schemas appendix)_
        - `capabilities` — array
          - _(nesting depth limit — see `VoiceBotCapability` in the Schemas appendix)_
        - `variables` — array — Variables such as dialplan variables that can be used in the bot.
          - _(nesting depth limit — see `VoiceBotVariable` in the Schemas appendix)_
    - **`dialogflowCx`**
      - `dialogflowCx` — BotDialogflowCxEndpoint **(required)**
        - `credentials` — any **(required)** — Dialogflow Service Account Credentials
        - `agent` — string **(required)** — Dialogflow Agent Id (example - 88ff4635-0852-4f97-ae44-b19ae9fa6ea1
        - `location` — string **(required)** — Dialogflow Agent Region (example: europe-west3)
        - `language` — string **(required)** — Language
    - **`openAiAssistant`**
      - `openAiAssistant` — BotOpenAiAssistantEndpoint **(required)**
        - `key` — string **(required)**
        - `assistantId` — string **(required)**
    - **`webhook`**
      - `webhook` — BotWebhookEndpoint **(required)**
        - `url` — string **(required)**
        - `secret` — string **(required)**
    - **`sqs`**
      - `sqs` — BotSqsEndpoint **(required)**
        - `url` — string **(required)**
        - `key` — string **(required)**
        - `secret` — string **(required)**
- `capabilities` — array
  - _array of_ `VoiceBotCapability`
    - _oneOf_ — exactly one of:
      - **`tool`**
        - `tool` — VoiceBotCapabilityTool **(required)**
          - _(nesting depth limit — see `VoiceBotCapabilityTool` in the Schemas appendix)_
      - **`kb`**
        - `kb` — VoiceBotKnowledgeBase **(required)**
          - _(nesting depth limit — see `VoiceBotKnowledgeBase` in the Schemas appendix)_
- `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.

**`UpdateVoiceBotResponseContent`**

- `bot` — VoiceBot **(required)**
  - `name` — string **(required)** _(minLen=3; maxLen=255)_
  - `category` — string — Category of the bot _(minLen=1; maxLen=128)_
  - `message` — string — The initial message that will be played at the start of the session.
  - `pipeline` — VoiceBotPipelineSettings
    - `interuptionsEnabled` — boolean — If enabled the user can interrupt the the bot playback.
    - `maximumDuration` — number — The maximum number of seconds a call will last.
    - `maximumDurationAction` — union
      - _oneOf_ — exactly one of:
        - **`hangup`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`transfer`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `silenceTimeout` — number — How long to wait before a call is automatically ended due to inactivity.
    - `silenceTimeoutAction` — union
      - _oneOf_ — exactly one of:
        - **`hangup`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`transfer`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `endCallEnabled` — boolean — If enabled the bot can hangup the call.
    - `endCallPhases` — string — A list of phases separated by comma, which will end the call matched.
  - `speech` — VoiceBotSpeechSettings — Speech configuration. When present it wins over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the exception.
    - `languages` — array **(required)** — Configured languages. The @length bound is a storage ceiling; the real cap is the recogniser's own candidate limit, enforced in the service. _(minItems=1; maxItems=10)_
      - _array of_ `VoiceBotLanguage`
        - _(nesting depth limit — see `VoiceBotLanguage` in the Schemas appendix)_
    - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in its own language's voice, provider account and pronunciation rules. Languages with an empty first message, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
    - `transcription` — VoiceBotTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
      - `engine` — string — Recogniser to transcribe the caller with. Absent resolves to the platform default ('aws://transcribe' today), resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
      - `autoDetect` — boolean — Identify the caller's language per utterance and switch voice and reply language mid-call. HERE RATHER THAN ON `VoiceBotSpeechSettings`, because identifying a language is something the RECOGNISER does: it becomes identify-multiple-languages plus language-options on the recognition stream, and nothing about synthesis reads it. Requires at least two configured languages and a recogniser that can identify them; the server clamps it to false otherwise, because forwarding true with a single candidate makes Amazon reject the stream outright.
  - `backgroundSound` — VoiceBotBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT rather than a loose name on the bot, matching `wildix.wilma.agents`: it is one switchable call behaviour, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
    - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
    - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
  - `endpoint` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`llm`**
        - `llm` — VoiceBotLlmEndpoint **(required)**
          - _(nesting depth limit — see `VoiceBotLlmEndpoint` in the Schemas appendix)_
      - **`dialogflowCx`**
        - `dialogflowCx` — BotDialogflowCxEndpoint **(required)**
          - _(nesting depth limit — see `BotDialogflowCxEndpoint` in the Schemas appendix)_
      - **`openAiAssistant`**
        - `openAiAssistant` — BotOpenAiAssistantEndpoint **(required)**
          - _(nesting depth limit — see `BotOpenAiAssistantEndpoint` in the Schemas appendix)_
      - **`webhook`**
        - `webhook` — BotWebhookEndpoint **(required)**
          - _(nesting depth limit — see `BotWebhookEndpoint` in the Schemas appendix)_
      - **`sqs`**
        - `sqs` — BotSqsEndpoint **(required)**
          - _(nesting depth limit — see `BotSqsEndpoint` in the Schemas appendix)_
  - `capabilities` — array
    - _array of_ `VoiceBotCapability`
      - _oneOf_ — exactly one of:
        - **`tool`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`kb`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

**`VoiceBot`**

- `name` — string **(required)** _(minLen=3; maxLen=255)_
- `category` — string — Category of the bot _(minLen=1; maxLen=128)_
- `message` — string — The initial message that will be played at the start of the session.
- `pipeline` — VoiceBotPipelineSettings
  - `interuptionsEnabled` — boolean — If enabled the user can interrupt the the bot playback.
  - `maximumDuration` — number — The maximum number of seconds a call will last.
  - `maximumDurationAction` — union
    - _oneOf_ — exactly one of:
      - **`hangup`**
        - `hangup` — VoiceBotTerminateHangupAction **(required)**
      - **`transfer`**
        - `transfer` — VoiceBotTerminateTransferAction **(required)**
          - _(nesting depth limit — see `VoiceBotTerminateTransferAction` in the Schemas appendix)_
  - `silenceTimeout` — number — How long to wait before a call is automatically ended due to inactivity.
  - `silenceTimeoutAction` — union
    - _oneOf_ — exactly one of:
      - **`hangup`**
        - `hangup` — VoiceBotTerminateHangupAction **(required)**
      - **`transfer`**
        - `transfer` — VoiceBotTerminateTransferAction **(required)**
          - _(nesting depth limit — see `VoiceBotTerminateTransferAction` in the Schemas appendix)_
  - `endCallEnabled` — boolean — If enabled the bot can hangup the call.
  - `endCallPhases` — string — A list of phases separated by comma, which will end the call matched.
- `speech` — VoiceBotSpeechSettings — Speech configuration. When present it wins over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the exception.
  - `languages` — array **(required)** — Configured languages. The @length bound is a storage ceiling; the real cap is the recogniser's own candidate limit, enforced in the service. _(minItems=1; maxItems=10)_
    - _array of_ `VoiceBotLanguage`
      - `code` — string **(required)** — BCP-47 code with locale, e.g. 'en-US'. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
      - `voice` — string **(required)** — Voice this language speaks with, as a URI — provider, voice id, synthesis parameters and, where the company uses its own provider account, its `apiKey` query parameter. See VoiceBotVoiceUri. PER LANGUAGE, and that is the whole reason the member is here rather than on the settings above: provider quality is not uniform across languages, a voice id belongs to exactly one provider, and a bot-wide provider made changing it invalidate every configured voice at once. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
      - `greeting` — string — Initial phrase for this language. Absent or empty means the agent says nothing and waits — it does NOT fall back to the agent-level message, which would speak one language's text in another language's voice.
      - `isDefault` — boolean — Marks the language a caller hears when their own matches nothing configured. THE FULL RESOLUTION ORDER, since a client author reading only this contract cannot otherwise find it: an exact match on the call's language, then a match on its primary subtag (`fr` finds `fr-FR`), then the language marked here, then a language whose primary subtag is `en`, then the first entry in the list. Marked is consulted BEFORE the English step, so a record with none marked resolves exactly as it did before this member existed. English is deliberate rather than arbitrary — it is the language a caller the agent was not built for is likeliest to understand — and the last step exists only to keep the rule total, which is why list order should not be treated as configuration. At most one language may carry it. A record with two — reachable through the API or the CLI, where no form prevents it — resolves to the first marked one in list order, because refusing a call over configuration drift is worse than serving it and saying so in the trace.
      - `pronunciations` — array — Pronunciation rules for one language. BOUNDED, and the bound is not decoration. `applyPronunciations` compiles every rule of a language into a SINGLE alternating regular expression, so the cost is the pattern's total size: measured against the real escaping and matching logic, 1,000 rules cost ~0.9 s of CPU per synthesized sentence, 5,000 cost ~4.9 s, and around 10,000 `new RegExp` throws V8's pattern-size error outright — from a call site outside the surrounding `try`, so a 500 rather than a degraded reply. Stored on a bot, that made every utterance of the agent fail. 200 is far above any real use — a product glossary is a handful of names — and far below where either cost begins. Found by a security review. NO LOWER BOUND on `phrase` or `as`, deliberately. Both consoles add an EMPTY rule row the moment someone clicks 'Add pronunciation', so a `min: 1` would make saving an agent with a half-typed row fail entirely — and the runtime already ignores a rule with no phrase. Dropping blank rows belongs in the consoles' save filters, not in a refusal here. _(maxItems=200)_
        - _(nesting depth limit — see `VoiceBotPronunciation` in the Schemas appendix)_
  - `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in its own language's voice, provider account and pronunciation rules. Languages with an empty first message, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
  - `transcription` — VoiceBotTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
    - `engine` — string — Recogniser to transcribe the caller with. Absent resolves to the platform default ('aws://transcribe' today), resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
    - `autoDetect` — boolean — Identify the caller's language per utterance and switch voice and reply language mid-call. HERE RATHER THAN ON `VoiceBotSpeechSettings`, because identifying a language is something the RECOGNISER does: it becomes identify-multiple-languages plus language-options on the recognition stream, and nothing about synthesis reads it. Requires at least two configured languages and a recogniser that can identify them; the server clamps it to false otherwise, because forwarding true with a single candidate makes Amazon reject the stream outright.
- `backgroundSound` — VoiceBotBackgroundSoundSettings — Ambient background audio played under the call. A SETTINGS OBJECT rather than a loose name on the bot, matching `wildix.wilma.agents`: it is one switchable call behaviour, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case.
  - `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
  - `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_
- `endpoint` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`llm`**
      - `llm` — VoiceBotLlmEndpoint **(required)**
        - `prompt` — string **(required)** _(maxLen=40000)_
        - `model` — string — The AI model to use for generating responses. If not specified, uses the default model. _(default=default; pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
        - `guidelines` — array
          - _array of_ `string`
        - `metadata` — VoiceBotPromptMetadata
          - _(nesting depth limit — see `VoiceBotPromptMetadata` in the Schemas appendix)_
        - `embeddedTools` — array — Embedded functions to use within voice session.
          - _(nesting depth limit — see `VoiceBotEmbeddedTool` in the Schemas appendix)_
        - `tools` — array — Custom tools to be used within voice session.
          - _(nesting depth limit — see `VoiceBotTool` in the Schemas appendix)_
        - `capabilities` — array
          - _(nesting depth limit — see `VoiceBotCapability` in the Schemas appendix)_
        - `variables` — array — Variables such as dialplan variables that can be used in the bot.
          - _(nesting depth limit — see `VoiceBotVariable` in the Schemas appendix)_
    - **`dialogflowCx`**
      - `dialogflowCx` — BotDialogflowCxEndpoint **(required)**
        - `credentials` — any **(required)** — Dialogflow Service Account Credentials
        - `agent` — string **(required)** — Dialogflow Agent Id (example - 88ff4635-0852-4f97-ae44-b19ae9fa6ea1
        - `location` — string **(required)** — Dialogflow Agent Region (example: europe-west3)
        - `language` — string **(required)** — Language
    - **`openAiAssistant`**
      - `openAiAssistant` — BotOpenAiAssistantEndpoint **(required)**
        - `key` — string **(required)**
        - `assistantId` — string **(required)**
    - **`webhook`**
      - `webhook` — BotWebhookEndpoint **(required)**
        - `url` — string **(required)**
        - `secret` — string **(required)**
    - **`sqs`**
      - `sqs` — BotSqsEndpoint **(required)**
        - `url` — string **(required)**
        - `key` — string **(required)**
        - `secret` — string **(required)**
- `capabilities` — array
  - _array of_ `VoiceBotCapability`
    - _oneOf_ — exactly one of:
      - **`tool`**
        - `tool` — VoiceBotCapabilityTool **(required)**
          - _(nesting depth limit — see `VoiceBotCapabilityTool` in the Schemas appendix)_
      - **`kb`**
        - `kb` — VoiceBotKnowledgeBase **(required)**
          - _(nesting depth limit — see `VoiceBotKnowledgeBase` in the Schemas appendix)_
- `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
- `id` — string **(required)** _(minLen=12; maxLen=12)_
- `createdAt` — string **(required)**
- `updatedAt` — string

**`VoiceBotBackgroundSoundSettings`**

_Ambient background audio played under the call. A SETTINGS OBJECT rather than a loose name on the bot, matching `wildix.wilma.agents`: it is one switchable call behaviour, and the volume and fade controls the console will want next have somewhere to go. ABSENT MEANS OFF — a bot that never touches it behaves exactly as every call did before this setting existed, and the PBX needs no new case._

- `enabled` — boolean **(required)** — Whether ambient background audio plays under the call.
- `sound` — string — Music-on-hold class the PBX plays. Absent with `enabled` true leaves the choice of class to the PBX. _(pattern=^[^\r\n]+$; minLen=1; maxLen=64)_

**`VoiceBotCapability`**

- _oneOf_ — exactly one of:
  - **`tool`**
    - `tool` — VoiceBotCapabilityTool **(required)**
      - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `variables` — array
        - _array of_ `VoiceBotToolVariable`
          - _(nesting depth limit — see `VoiceBotToolVariable` in the Schemas appendix)_
      - `startMessage` — string — Message spoken when the tool call starts. Spoken in every language of the call while `startMessages` is absent or empty; not consulted once `startMessages` carries any entry.
      - `startMessages` — array — Per-language start messages. When present and non-empty, the entry for the call's current language is spoken and `startMessage` is not consulted; a language with no entry is silent. When absent or empty, `startMessage` is spoken as before. On a call with no effective speech configuration — no configured languages, or a PBX below protocol 2 — `startMessage` is spoken regardless, because there is no current language to choose by.
        - _array of_ `VoiceBotSpokenPhrase`
          - _(nesting depth limit — see `VoiceBotSpokenPhrase` in the Schemas appendix)_
      - `pipeline` — VoiceBotCapabilityToolPipeline
        - `type` — string _(enum: `blocking_request`, `blocking_request_guided`, `async_request`, `async_request_guided`)_
        - `instructions` — string — Instructions for generating a reply when using guided pipeline types. Use {{response}} to reference the tool response.
      - `annotations` — array
        - _array of_ `VoiceBotToolAnnotation`
          - _(nesting depth limit — see `VoiceBotToolAnnotation` in the Schemas appendix)_
  - **`kb`**
    - `kb` — VoiceBotKnowledgeBase **(required)**
      - `knowledgeBaseId` — string
      - `instructions` — string — Additional instructions for when the bot should use this knowledge base.
      - `searchStrategy` — string _(enum: `bm25`, `vector`, `hybrid`)_
      - `searchThreshold` — string _(enum: `low`, `medium`, `high`)_
      - `searchLimit` — number — Maximum number of search results returned by this knowledge base capability. _(min=1; max=50)_
      - `annotations` — array
        - _array of_ `VoiceBotToolAnnotation`
          - _(nesting depth limit — see `VoiceBotToolAnnotation` in the Schemas appendix)_

**`VoiceBotCapabilityTool`**

- `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
- `variables` — array
  - _array of_ `VoiceBotToolVariable`
    - `name` — string **(required)** — Name of the tool variable, e.g.: 'myvar' _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
    - `handler` — union
      - _oneOf_ — exactly one of:
        - **`auto`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`guided`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`predefined`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
- `startMessage` — string — Message spoken when the tool call starts. Spoken in every language of the call while `startMessages` is absent or empty; not consulted once `startMessages` carries any entry.
- `startMessages` — array — Per-language start messages. When present and non-empty, the entry for the call's current language is spoken and `startMessage` is not consulted; a language with no entry is silent. When absent or empty, `startMessage` is spoken as before. On a call with no effective speech configuration — no configured languages, or a PBX below protocol 2 — `startMessage` is spoken regardless, because there is no current language to choose by.
  - _array of_ `VoiceBotSpokenPhrase`
    - `language` — string **(required)** — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - `text` — string **(required)**
- `pipeline` — VoiceBotCapabilityToolPipeline
  - `type` — string _(enum: `blocking_request`, `blocking_request_guided`, `async_request`, `async_request_guided`)_
  - `instructions` — string — Instructions for generating a reply when using guided pipeline types. Use {{response}} to reference the tool response.
- `annotations` — array
  - _array of_ `VoiceBotToolAnnotation`
    - _oneOf_ — exactly one of:
      - **`tag`**
        - `tag` — VoiceBotToolTagAnnotation **(required)** — Tag annotation emitted after a voice bot tool completes.
          - _(nesting depth limit — see `VoiceBotToolTagAnnotation` in the Schemas appendix)_
      - **`comment`**
        - `comment` — VoiceBotToolCommentAnnotation **(required)** — Comment annotation emitted after a voice bot tool completes.
          - _(nesting depth limit — see `VoiceBotToolCommentAnnotation` in the Schemas appendix)_
      - **`variables`**
        - `variables` — VoiceBotToolVariablesAnnotation **(required)** — Variables annotation emitted after a voice bot tool completes.
      - **`result`**
        - `result` — VoiceBotToolResultAnnotation **(required)** — Result annotation emitted after a voice bot tool completes.

**`VoiceBotCapabilityToolPipeline`**

- `type` — string _(enum: `blocking_request`, `blocking_request_guided`, `async_request`, `async_request_guided`)_
- `instructions` — string — Instructions for generating a reply when using guided pipeline types. Use {{response}} to reference the tool response.

**`VoiceBotCapabilityToolPipelineType`**

- string _(enum: `blocking_request`, `blocking_request_guided`, `async_request`, `async_request_guided`)_

**`VoiceBotCommandType`**

- string _(enum: `say`, `play`, `stop`, `hangup`, `transfer`)_

**`VoiceBotEmbeddedTool`**

- `type` — string **(required)** _(enum: `HANGUP`, `TRANSFER`, `DELEGATE`, `WAIT`)_
- `name` — string **(required)**
- `parameters` — any — The parameters the functions accepts.
- `annotations` — array
  - _array of_ `VoiceBotToolAnnotation`
    - _oneOf_ — exactly one of:
      - **`tag`**
        - `tag` — VoiceBotToolTagAnnotation **(required)** — Tag annotation emitted after a voice bot tool completes.
          - _(nesting depth limit — see `VoiceBotToolTagAnnotation` in the Schemas appendix)_
      - **`comment`**
        - `comment` — VoiceBotToolCommentAnnotation **(required)** — Comment annotation emitted after a voice bot tool completes.
          - _(nesting depth limit — see `VoiceBotToolCommentAnnotation` in the Schemas appendix)_
      - **`variables`**
        - `variables` — VoiceBotToolVariablesAnnotation **(required)** — Variables annotation emitted after a voice bot tool completes.
      - **`result`**
        - `result` — VoiceBotToolResultAnnotation **(required)** — Result annotation emitted after a voice bot tool completes.

**`VoiceBotEmbeddedToolType`**

- string _(enum: `HANGUP`, `TRANSFER`, `DELEGATE`, `WAIT`)_

**`VoiceBotEndpoint`**

- _oneOf_ — exactly one of:
  - **`llm`**
    - `llm` — VoiceBotLlmEndpoint **(required)**
      - `prompt` — string **(required)** _(maxLen=40000)_
      - `model` — string — The AI model to use for generating responses. If not specified, uses the default model. _(default=default; pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
      - `guidelines` — array
        - _array of_ `string`
      - `metadata` — VoiceBotPromptMetadata
        - `userName` — VoiceBotPromptMetadataEnabled
          - _(nesting depth limit — see `VoiceBotPromptMetadataEnabled` in the Schemas appendix)_
        - `userPhoneNumber` — VoiceBotPromptMetadataEnabled
          - _(nesting depth limit — see `VoiceBotPromptMetadataEnabled` in the Schemas appendix)_
        - `userEmail` — VoiceBotPromptMetadataDisabled
          - _(nesting depth limit — see `VoiceBotPromptMetadataDisabled` in the Schemas appendix)_
        - `userCompany` — VoiceBotPromptMetadataDisabled
          - _(nesting depth limit — see `VoiceBotPromptMetadataDisabled` in the Schemas appendix)_
        - `time` — VoiceBotPromptMetadataTime
          - _(nesting depth limit — see `VoiceBotPromptMetadataTime` in the Schemas appendix)_
      - `embeddedTools` — array — Embedded functions to use within voice session.
        - _array of_ `VoiceBotEmbeddedTool`
          - _(nesting depth limit — see `VoiceBotEmbeddedTool` in the Schemas appendix)_
      - `tools` — array — Custom tools to be used within voice session.
        - _array of_ `VoiceBotTool`
          - _(nesting depth limit — see `VoiceBotTool` in the Schemas appendix)_
      - `capabilities` — array
        - _array of_ `VoiceBotCapability`
          - _(nesting depth limit — see `VoiceBotCapability` in the Schemas appendix)_
      - `variables` — array — Variables such as dialplan variables that can be used in the bot.
        - _array of_ `VoiceBotVariable`
          - _(nesting depth limit — see `VoiceBotVariable` in the Schemas appendix)_
  - **`dialogflowCx`**
    - `dialogflowCx` — BotDialogflowCxEndpoint **(required)**
      - `credentials` — any **(required)** — Dialogflow Service Account Credentials
      - `agent` — string **(required)** — Dialogflow Agent Id (example - 88ff4635-0852-4f97-ae44-b19ae9fa6ea1
      - `location` — string **(required)** — Dialogflow Agent Region (example: europe-west3)
      - `language` — string **(required)** — Language
  - **`openAiAssistant`**
    - `openAiAssistant` — BotOpenAiAssistantEndpoint **(required)**
      - `key` — string **(required)**
      - `assistantId` — string **(required)**
  - **`webhook`**
    - `webhook` — BotWebhookEndpoint **(required)**
      - `url` — string **(required)**
      - `secret` — string **(required)**
  - **`sqs`**
    - `sqs` — BotSqsEndpoint **(required)**
      - `url` — string **(required)**
      - `key` — string **(required)**
      - `secret` — string **(required)**

**`VoiceBotEventType`**

- string _(enum: `started`, `ended`, `reply`, `audio`, `playback`, `transcription`, `interruption`, `complete`)_

**`VoiceBotFunctionDefinition`**

- `name` — string **(required)** — The name of the function to be called. Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length of 64.
- `description` — string — A description of what the function does, used by the model to choose when and how to call the function.
- `parameters` — any — The parameters the functions accepts, described as a JSON Schema object.
- `integration` — union
  - _oneOf_ — exactly one of:
    - **`webhook`**
      - `webhook` — VoiceBotFunctionIntegrationWebhook **(required)**
        - `url` — string **(required)**
        - `method` — string _(enum: `get`, `post`, `put`, `delete`, `patch`)_
        - `async` — boolean
        - `authorization` — union
          - _(nesting depth limit — see `VoiceBotFunctionIntegrationWebhookAuthorization` in the Schemas appendix)_
        - `headers` — array
          - _(nesting depth limit — see `VoiceBotFunctionIntegrationWebhookHeader` in the Schemas appendix)_
        - `timeout` — number — Timeout in milliseconds for the webhook request. _(min=5000; max=120000)_
        - `startMessage` — string — Message spoken when the function call starts.
        - `parameters` — any

**`VoiceBotFunctionIntegration`**

- _oneOf_ — exactly one of:
  - **`webhook`**
    - `webhook` — VoiceBotFunctionIntegrationWebhook **(required)**
      - `url` — string **(required)**
      - `method` — string _(enum: `get`, `post`, `put`, `delete`, `patch`)_
      - `async` — boolean
      - `authorization` — union
        - _oneOf_ — exactly one of:
          - **`bearer`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`basic`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`oauth`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `headers` — array
        - _array of_ `VoiceBotFunctionIntegrationWebhookHeader`
          - _(nesting depth limit — see `VoiceBotFunctionIntegrationWebhookHeader` in the Schemas appendix)_
      - `timeout` — number — Timeout in milliseconds for the webhook request. _(min=5000; max=120000)_
      - `startMessage` — string — Message spoken when the function call starts.
      - `parameters` — any

**`VoiceBotFunctionIntegrationMethod`**

- string _(enum: `get`, `post`, `put`, `delete`, `patch`)_

**`VoiceBotFunctionIntegrationWebhook`**

- `url` — string **(required)**
- `method` — string _(enum: `get`, `post`, `put`, `delete`, `patch`)_
- `async` — boolean
- `authorization` — union
  - _oneOf_ — exactly one of:
    - **`bearer`**
      - `bearer` — VoiceBotFunctionIntegrationWebhookAuthorizationBearer **(required)**
        - `token` — string **(required)**
    - **`basic`**
      - `basic` — VoiceBotFunctionIntegrationWebhookAuthorizationBasic **(required)**
        - `username` — string **(required)**
        - `password` — string **(required)**
    - **`oauth`**
      - `oauth` — VoiceBotFunctionIntegrationWebhookAuthorizationOAuth **(required)**
        - `clientId` — string **(required)**
        - `clientSecret` — string **(required)**
        - `endpointUrl` — string **(required)**
        - `scope` — string
- `headers` — array
  - _array of_ `VoiceBotFunctionIntegrationWebhookHeader`
    - `key` — string **(required)**
    - `value` — string **(required)**
- `timeout` — number — Timeout in milliseconds for the webhook request. _(min=5000; max=120000)_
- `startMessage` — string — Message spoken when the function call starts.
- `parameters` — any

**`VoiceBotFunctionIntegrationWebhookAuthorization`**

- _oneOf_ — exactly one of:
  - **`bearer`**
    - `bearer` — VoiceBotFunctionIntegrationWebhookAuthorizationBearer **(required)**
      - `token` — string **(required)**
  - **`basic`**
    - `basic` — VoiceBotFunctionIntegrationWebhookAuthorizationBasic **(required)**
      - `username` — string **(required)**
      - `password` — string **(required)**
  - **`oauth`**
    - `oauth` — VoiceBotFunctionIntegrationWebhookAuthorizationOAuth **(required)**
      - `clientId` — string **(required)**
      - `clientSecret` — string **(required)**
      - `endpointUrl` — string **(required)**
      - `scope` — string

**`VoiceBotFunctionIntegrationWebhookAuthorizationBasic`**

- `username` — string **(required)**
- `password` — string **(required)**

**`VoiceBotFunctionIntegrationWebhookAuthorizationBearer`**

- `token` — string **(required)**

**`VoiceBotFunctionIntegrationWebhookAuthorizationOAuth`**

- `clientId` — string **(required)**
- `clientSecret` — string **(required)**
- `endpointUrl` — string **(required)**
- `scope` — string

**`VoiceBotFunctionIntegrationWebhookHeader`**

- `key` — string **(required)**
- `value` — string **(required)**

**`VoiceBotInfo`**

- `id` — string **(required)** _(minLen=12; maxLen=12)_
- `name` — string **(required)** _(minLen=3; maxLen=255)_
- `speechConfigured` — boolean — Whether the voice channel has at least one configured speech language. A dialplan form partitions its application lists on this, so the answer has to travel with the list rather than cost one lookup per entry — it is the reason this member exists and the reason removing it broke that form. Absent is read as false.

**`VoiceBotKnowledgeBase`**

- `knowledgeBaseId` — string
- `instructions` — string — Additional instructions for when the bot should use this knowledge base.
- `searchStrategy` — string _(enum: `bm25`, `vector`, `hybrid`)_
- `searchThreshold` — string _(enum: `low`, `medium`, `high`)_
- `searchLimit` — number — Maximum number of search results returned by this knowledge base capability. _(min=1; max=50)_
- `annotations` — array
  - _array of_ `VoiceBotToolAnnotation`
    - _oneOf_ — exactly one of:
      - **`tag`**
        - `tag` — VoiceBotToolTagAnnotation **(required)** — Tag annotation emitted after a voice bot tool completes.
          - _(nesting depth limit — see `VoiceBotToolTagAnnotation` in the Schemas appendix)_
      - **`comment`**
        - `comment` — VoiceBotToolCommentAnnotation **(required)** — Comment annotation emitted after a voice bot tool completes.
          - _(nesting depth limit — see `VoiceBotToolCommentAnnotation` in the Schemas appendix)_
      - **`variables`**
        - `variables` — VoiceBotToolVariablesAnnotation **(required)** — Variables annotation emitted after a voice bot tool completes.
      - **`result`**
        - `result` — VoiceBotToolResultAnnotation **(required)** — Result annotation emitted after a voice bot tool completes.

**`VoiceBotLanguage`**

_One configured language: its voice, its initial phrase and its pronunciation rules._

- `code` — string **(required)** — BCP-47 code with locale, e.g. 'en-US'. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `voice` — string **(required)** — Voice this language speaks with, as a URI — provider, voice id, synthesis parameters and, where the company uses its own provider account, its `apiKey` query parameter. See VoiceBotVoiceUri. PER LANGUAGE, and that is the whole reason the member is here rather than on the settings above: provider quality is not uniform across languages, a voice id belongs to exactly one provider, and a bot-wide provider made changing it invalidate every configured voice at once. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
- `greeting` — string — Initial phrase for this language. Absent or empty means the agent says nothing and waits — it does NOT fall back to the agent-level message, which would speak one language's text in another language's voice.
- `isDefault` — boolean — Marks the language a caller hears when their own matches nothing configured. THE FULL RESOLUTION ORDER, since a client author reading only this contract cannot otherwise find it: an exact match on the call's language, then a match on its primary subtag (`fr` finds `fr-FR`), then the language marked here, then a language whose primary subtag is `en`, then the first entry in the list. Marked is consulted BEFORE the English step, so a record with none marked resolves exactly as it did before this member existed. English is deliberate rather than arbitrary — it is the language a caller the agent was not built for is likeliest to understand — and the last step exists only to keep the rule total, which is why list order should not be treated as configuration. At most one language may carry it. A record with two — reachable through the API or the CLI, where no form prevents it — resolves to the first marked one in list order, because refusing a call over configuration drift is worse than serving it and saying so in the trace.
- `pronunciations` — array — Pronunciation rules for one language. BOUNDED, and the bound is not decoration. `applyPronunciations` compiles every rule of a language into a SINGLE alternating regular expression, so the cost is the pattern's total size: measured against the real escaping and matching logic, 1,000 rules cost ~0.9 s of CPU per synthesized sentence, 5,000 cost ~4.9 s, and around 10,000 `new RegExp` throws V8's pattern-size error outright — from a call site outside the surrounding `try`, so a 500 rather than a degraded reply. Stored on a bot, that made every utterance of the agent fail. 200 is far above any real use — a product glossary is a handful of names — and far below where either cost begins. Found by a security review. NO LOWER BOUND on `phrase` or `as`, deliberately. Both consoles add an EMPTY rule row the moment someone clicks 'Add pronunciation', so a `min: 1` would make saving an agent with a half-typed row fail entirely — and the runtime already ignores a rule with no phrase. Dropping blank rows belongs in the consoles' save filters, not in a refusal here. _(maxItems=200)_
  - _array of_ `VoiceBotPronunciation`
    - `phrase` — string **(required)** — The written form to replace. Bounded because every rule is compiled into ONE regular expression — see the list below. _(maxLen=200)_
    - `as` — string **(required)** — Respelling (ALIAS) or phonetic transcription (IPA). _(maxLen=200)_
    - `encoding` — string _(enum: `alias`, `ipa`)_

**`VoiceBotLlmEndpoint`**

- `prompt` — string **(required)** _(maxLen=40000)_
- `model` — string — The AI model to use for generating responses. If not specified, uses the default model. _(default=default; pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
- `guidelines` — array
  - _array of_ `string`
- `metadata` — VoiceBotPromptMetadata
  - `userName` — VoiceBotPromptMetadataEnabled
    - `enabled` — boolean **(required)** — Whether this metadata field is enabled _(default=True)_
  - `userPhoneNumber` — VoiceBotPromptMetadataEnabled
    - `enabled` — boolean **(required)** — Whether this metadata field is enabled _(default=True)_
  - `userEmail` — VoiceBotPromptMetadataDisabled
    - `enabled` — boolean **(required)** — Whether this metadata field is enabled _(default=False)_
  - `userCompany` — VoiceBotPromptMetadataDisabled
    - `enabled` — boolean **(required)** — Whether this metadata field is enabled _(default=False)_
  - `time` — VoiceBotPromptMetadataTime
    - `enabled` — boolean **(required)** — Whether this metadata field is enabled _(default=False)_
    - `timeZone` — string **(required)** — Timezone for time formatting (e.g., 'Europe/Rome', 'UTC') _(default=UTC)_
- `embeddedTools` — array — Embedded functions to use within voice session.
  - _array of_ `VoiceBotEmbeddedTool`
    - `type` — string **(required)** _(enum: `HANGUP`, `TRANSFER`, `DELEGATE`, `WAIT`)_
    - `name` — string **(required)**
    - `parameters` — any — The parameters the functions accepts.
    - `annotations` — array
      - _array of_ `VoiceBotToolAnnotation`
        - _(nesting depth limit — see `VoiceBotToolAnnotation` in the Schemas appendix)_
- `tools` — array — Custom tools to be used within voice session.
  - _array of_ `VoiceBotTool`
    - `type` — string **(required)** _(enum: `function`)_
    - `function` — VoiceBotFunctionDefinition
      - `name` — string **(required)** — The name of the function to be called. Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length of 64.
      - `description` — string — A description of what the function does, used by the model to choose when and how to call the function.
      - `parameters` — any — The parameters the functions accepts, described as a JSON Schema object.
      - `integration` — union
        - _(nesting depth limit — see `VoiceBotFunctionIntegration` in the Schemas appendix)_
    - `annotations` — array
      - _array of_ `VoiceBotToolAnnotation`
        - _(nesting depth limit — see `VoiceBotToolAnnotation` in the Schemas appendix)_
- `capabilities` — array
  - _array of_ `VoiceBotCapability`
    - _oneOf_ — exactly one of:
      - **`tool`**
        - `tool` — VoiceBotCapabilityTool **(required)**
          - _(nesting depth limit — see `VoiceBotCapabilityTool` in the Schemas appendix)_
      - **`kb`**
        - `kb` — VoiceBotKnowledgeBase **(required)**
          - _(nesting depth limit — see `VoiceBotKnowledgeBase` in the Schemas appendix)_
- `variables` — array — Variables such as dialplan variables that can be used in the bot.
  - _array of_ `VoiceBotVariable`
    - `name` — string **(required)** _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_

**`VoiceBotNonUniqueNameExceptionResponseContent`**

- `message` — string **(required)**
- `type` — string _(default=VoiceBotNonUniqueNameException)_

**`VoiceBotNotFoundExceptionResponseContent`**

- `message` — string **(required)**
- `type` — string _(default=VoiceBotNotFoundException)_

**`VoiceBotPipelineSettings`**

- `interuptionsEnabled` — boolean — If enabled the user can interrupt the the bot playback.
- `maximumDuration` — number — The maximum number of seconds a call will last.
- `maximumDurationAction` — union
  - _oneOf_ — exactly one of:
    - **`hangup`**
      - `hangup` — VoiceBotTerminateHangupAction **(required)**
    - **`transfer`**
      - `transfer` — VoiceBotTerminateTransferAction **(required)**
        - `context` — string **(required)**
        - `extension` — string **(required)**
- `silenceTimeout` — number — How long to wait before a call is automatically ended due to inactivity.
- `silenceTimeoutAction` — union
  - _oneOf_ — exactly one of:
    - **`hangup`**
      - `hangup` — VoiceBotTerminateHangupAction **(required)**
    - **`transfer`**
      - `transfer` — VoiceBotTerminateTransferAction **(required)**
        - `context` — string **(required)**
        - `extension` — string **(required)**
- `endCallEnabled` — boolean — If enabled the bot can hangup the call.
- `endCallPhases` — string — A list of phases separated by comma, which will end the call matched.

**`VoiceBotPipelineTerminateAction`**

- _oneOf_ — exactly one of:
  - **`hangup`**
    - `hangup` — VoiceBotTerminateHangupAction **(required)**
  - **`transfer`**
    - `transfer` — VoiceBotTerminateTransferAction **(required)**
      - `context` — string **(required)**
      - `extension` — string **(required)**

**`VoiceBotPromptMetadata`**

- `userName` — VoiceBotPromptMetadataEnabled
  - `enabled` — boolean **(required)** — Whether this metadata field is enabled _(default=True)_
- `userPhoneNumber` — VoiceBotPromptMetadataEnabled
  - `enabled` — boolean **(required)** — Whether this metadata field is enabled _(default=True)_
- `userEmail` — VoiceBotPromptMetadataDisabled
  - `enabled` — boolean **(required)** — Whether this metadata field is enabled _(default=False)_
- `userCompany` — VoiceBotPromptMetadataDisabled
  - `enabled` — boolean **(required)** — Whether this metadata field is enabled _(default=False)_
- `time` — VoiceBotPromptMetadataTime
  - `enabled` — boolean **(required)** — Whether this metadata field is enabled _(default=False)_
  - `timeZone` — string **(required)** — Timezone for time formatting (e.g., 'Europe/Rome', 'UTC') _(default=UTC)_

**`VoiceBotPromptMetadataDisabled`**

- `enabled` — boolean **(required)** — Whether this metadata field is enabled _(default=False)_

**`VoiceBotPromptMetadataEnabled`**

- `enabled` — boolean **(required)** — Whether this metadata field is enabled _(default=True)_

**`VoiceBotPromptMetadataTime`**

- `enabled` — boolean **(required)** — Whether this metadata field is enabled _(default=False)_
- `timeZone` — string **(required)** — Timezone for time formatting (e.g., 'Europe/Rome', 'UTC') _(default=UTC)_

**`VoiceBotPronunciation`**

_A pronunciation rule for one phrase, belonging to one language._

- `phrase` — string **(required)** — The written form to replace. Bounded because every rule is compiled into ONE regular expression — see the list below. _(maxLen=200)_
- `as` — string **(required)** — Respelling (ALIAS) or phonetic transcription (IPA). _(maxLen=200)_
- `encoding` — string _(enum: `alias`, `ipa`)_

**`VoiceBotPronunciationEncoding`**

- string _(enum: `alias`, `ipa`)_

**`VoiceBotSpeechPayload`**

_Recognition intent for the call, sent on `started` at protocol version >= 2. Not recogniser parameters: the PBX translates it into its provider's API. `engine` is always concrete and `autoDetect` is already clamped by the server, because forwarding true with a single candidate makes Amazon reject the stream outright._

- `engine` — string **(required)** — Concrete recogniser URI, resolved from the bot or from the platform default; never absent. See VoiceBotTranscriptionUri. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
- `languages` — array **(required)** — Every configured language, as candidates for identification.
  - _array of_ `string`
- `preferredLanguage` — string **(required)** — The language the call starts in, resolved from the channel. Always a member of `languages`. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `autoDetect` — boolean **(required)**

**`VoiceBotSpeechSettings`**

_Speech configuration. When present it wins over the dialplan's `voice` and `initialMessage` connect parameters; `language` is the exception._

- `languages` — array **(required)** — Configured languages. The @length bound is a storage ceiling; the real cap is the recogniser's own candidate limit, enforced in the service. _(minItems=1; maxItems=10)_
  - _array of_ `VoiceBotLanguage`
    - `code` — string **(required)** — BCP-47 code with locale, e.g. 'en-US'. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
    - `voice` — string **(required)** — Voice this language speaks with, as a URI — provider, voice id, synthesis parameters and, where the company uses its own provider account, its `apiKey` query parameter. See VoiceBotVoiceUri. PER LANGUAGE, and that is the whole reason the member is here rather than on the settings above: provider quality is not uniform across languages, a voice id belongs to exactly one provider, and a bot-wide provider made changing it invalidate every configured voice at once. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
    - `greeting` — string — Initial phrase for this language. Absent or empty means the agent says nothing and waits — it does NOT fall back to the agent-level message, which would speak one language's text in another language's voice.
    - `isDefault` — boolean — Marks the language a caller hears when their own matches nothing configured. THE FULL RESOLUTION ORDER, since a client author reading only this contract cannot otherwise find it: an exact match on the call's language, then a match on its primary subtag (`fr` finds `fr-FR`), then the language marked here, then a language whose primary subtag is `en`, then the first entry in the list. Marked is consulted BEFORE the English step, so a record with none marked resolves exactly as it did before this member existed. English is deliberate rather than arbitrary — it is the language a caller the agent was not built for is likeliest to understand — and the last step exists only to keep the rule total, which is why list order should not be treated as configuration. At most one language may carry it. A record with two — reachable through the API or the CLI, where no form prevents it — resolves to the first marked one in list order, because refusing a call over configuration drift is worse than serving it and saying so in the trace.
    - `pronunciations` — array — Pronunciation rules for one language. BOUNDED, and the bound is not decoration. `applyPronunciations` compiles every rule of a language into a SINGLE alternating regular expression, so the cost is the pattern's total size: measured against the real escaping and matching logic, 1,000 rules cost ~0.9 s of CPU per synthesized sentence, 5,000 cost ~4.9 s, and around 10,000 `new RegExp` throws V8's pattern-size error outright — from a call site outside the surrounding `try`, so a 500 rather than a degraded reply. Stored on a bot, that made every utterance of the agent fail. 200 is far above any real use — a product glossary is a handful of names — and far below where either cost begins. Found by a security review. NO LOWER BOUND on `phrase` or `as`, deliberately. Both consoles add an EMPTY rule row the moment someone clicks 'Add pronunciation', so a `min: 1` would make saving an agent with a half-typed row fail entirely — and the runtime already ignores a rule with no phrase. Dropping blank rows belongs in the consoles' save filters, not in a refusal here. _(maxItems=200)_
      - _array of_ `VoiceBotPronunciation`
        - _(nesting depth limit — see `VoiceBotPronunciation` in the Schemas appendix)_
- `greetEveryLanguage` — boolean — Speak the first message of every configured language in turn when the call is answered, each in its own language's voice, provider account and pronunciation rules. Languages with an empty first message, and languages the PBX synthesizes itself, are skipped. Absent means off. Requires at least two languages carrying a first message; below that the runtime speaks only the resolved language's phrase, and the console clamps the member on save.
- `transcription` — VoiceBotTranscriptionSettings — Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does.
  - `engine` — string — Recogniser to transcribe the caller with. Absent resolves to the platform default ('aws://transcribe' today), resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
  - `autoDetect` — boolean — Identify the caller's language per utterance and switch voice and reply language mid-call. HERE RATHER THAN ON `VoiceBotSpeechSettings`, because identifying a language is something the RECOGNISER does: it becomes identify-multiple-languages plus language-options on the recognition stream, and nothing about synthesis reads it. Requires at least two configured languages and a recogniser that can identify them; the server clamps it to false otherwise, because forwarding true with a single candidate makes Amazon reject the stream outright.

**`VoiceBotSpokenPhrase`**

_One phrase in one language, for a tool that speaks a fixed line when its call starts. Which entry is spoken is decided by the call's current language — the one resolved at connect, or the one automatic detection switched to — matched on `language` CASE-INSENSITIVELY, because older records on this stack hold lower-cased codes; `AgentSpokenPhrase` matches the same way, so the two stacks cannot disagree about which entry a code reaches. Blank `text` means the agent says nothing in that language; it does NOT fall back to `startMessage`, which would speak one language's text in another language's voice._

- `language` — string **(required)** — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `text` — string **(required)**

**`VoiceBotTerminateHangupAction`**

- VoiceBotTerminateHangupAction

**`VoiceBotTerminateTransferAction`**

- `context` — string **(required)**
- `extension` — string **(required)**

**`VoiceBotTool`**

- `type` — string **(required)** _(enum: `function`)_
- `function` — VoiceBotFunctionDefinition
  - `name` — string **(required)** — The name of the function to be called. Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length of 64.
  - `description` — string — A description of what the function does, used by the model to choose when and how to call the function.
  - `parameters` — any — The parameters the functions accepts, described as a JSON Schema object.
  - `integration` — union
    - _oneOf_ — exactly one of:
      - **`webhook`**
        - `webhook` — VoiceBotFunctionIntegrationWebhook **(required)**
          - _(nesting depth limit — see `VoiceBotFunctionIntegrationWebhook` in the Schemas appendix)_
- `annotations` — array
  - _array of_ `VoiceBotToolAnnotation`
    - _oneOf_ — exactly one of:
      - **`tag`**
        - `tag` — VoiceBotToolTagAnnotation **(required)** — Tag annotation emitted after a voice bot tool completes.
          - _(nesting depth limit — see `VoiceBotToolTagAnnotation` in the Schemas appendix)_
      - **`comment`**
        - `comment` — VoiceBotToolCommentAnnotation **(required)** — Comment annotation emitted after a voice bot tool completes.
          - _(nesting depth limit — see `VoiceBotToolCommentAnnotation` in the Schemas appendix)_
      - **`variables`**
        - `variables` — VoiceBotToolVariablesAnnotation **(required)** — Variables annotation emitted after a voice bot tool completes.
      - **`result`**
        - `result` — VoiceBotToolResultAnnotation **(required)** — Result annotation emitted after a voice bot tool completes.

**`VoiceBotToolAnnotation`**

_Configuration for annotations emitted after a tool completes. Tag and comment annotations can provide a handlebars value, while variables and result annotations opt into logging runtime data._

- _oneOf_ — exactly one of:
  - **`tag`**
    - `tag` — VoiceBotToolTagAnnotation **(required)** — Tag annotation emitted after a voice bot tool completes.
      - `value` — string — Static handlebars expression resolved against bot variables and helpers.
      - `applyOnSuccess` — boolean — Apply when the tool succeeds.
      - `applyOnFailure` — boolean — Apply when the tool fails.
  - **`comment`**
    - `comment` — VoiceBotToolCommentAnnotation **(required)** — Comment annotation emitted after a voice bot tool completes.
      - `value` — string — Static handlebars expression resolved against bot variables and helpers.
      - `applyOnSuccess` — boolean — Apply when the tool succeeds.
      - `applyOnFailure` — boolean — Apply when the tool fails.
  - **`variables`**
    - `variables` — VoiceBotToolVariablesAnnotation **(required)** — Variables annotation emitted after a voice bot tool completes.
  - **`result`**
    - `result` — VoiceBotToolResultAnnotation **(required)** — Result annotation emitted after a voice bot tool completes.

**`VoiceBotToolCommentAnnotation`**

_Comment annotation emitted after a voice bot tool completes._

- `value` — string — Static handlebars expression resolved against bot variables and helpers.
- `applyOnSuccess` — boolean — Apply when the tool succeeds.
- `applyOnFailure` — boolean — Apply when the tool fails.

**`VoiceBotToolResultAnnotation`**

_Result annotation emitted after a voice bot tool completes._

- VoiceBotToolResultAnnotation

**`VoiceBotToolTagAnnotation`**

_Tag annotation emitted after a voice bot tool completes._

- `value` — string — Static handlebars expression resolved against bot variables and helpers.
- `applyOnSuccess` — boolean — Apply when the tool succeeds.
- `applyOnFailure` — boolean — Apply when the tool fails.

**`VoiceBotToolType`**

- string _(enum: `function`)_

**`VoiceBotToolVariable`**

- `name` — string **(required)** — Name of the tool variable, e.g.: 'myvar' _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
- `handler` — union
  - _oneOf_ — exactly one of:
    - **`auto`**
      - `auto` — VoiceBotToolVariableAutoHandler **(required)**
    - **`guided`**
      - `guided` — VoiceBotToolVariableGuidedHandler **(required)**
        - `description` — string **(required)** _(minLen=1; maxLen=1024)_
    - **`predefined`**
      - `predefined` — VoiceBotToolVariablePredefinedHandler **(required)**
        - `description` — string **(required)**

**`VoiceBotToolVariableAutoHandler`**

- VoiceBotToolVariableAutoHandler

**`VoiceBotToolVariableGuidedHandler`**

- `description` — string **(required)** _(minLen=1; maxLen=1024)_

**`VoiceBotToolVariableHandler`**

- _oneOf_ — exactly one of:
  - **`auto`**
    - `auto` — VoiceBotToolVariableAutoHandler **(required)**
  - **`guided`**
    - `guided` — VoiceBotToolVariableGuidedHandler **(required)**
      - `description` — string **(required)** _(minLen=1; maxLen=1024)_
  - **`predefined`**
    - `predefined` — VoiceBotToolVariablePredefinedHandler **(required)**
      - `description` — string **(required)**

**`VoiceBotToolVariablePredefinedHandler`**

- `description` — string **(required)**

**`VoiceBotToolVariablesAnnotation`**

_Variables annotation emitted after a voice bot tool completes._

- VoiceBotToolVariablesAnnotation

**`VoiceBotTranscriptionSettings`**

_Speech-to-text configuration: which recogniser listens to the caller, and whether it identifies the language while it does._

- `engine` — string — Recogniser to transcribe the caller with. Absent resolves to the platform default ('aws://transcribe' today), resolved by the server so exactly one component decides it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
- `autoDetect` — boolean — Identify the caller's language per utterance and switch voice and reply language mid-call. HERE RATHER THAN ON `VoiceBotSpeechSettings`, because identifying a language is something the RECOGNISER does: it becomes identify-multiple-languages plus language-options on the recognition stream, and nothing about synthesis reads it. Requires at least two configured languages and a recogniser that can identify them; the server clamps it to false otherwise, because forwarding true with a single candidate makes Amazon reject the stream outright.

**`VoiceBotVariable`**

- `name` — string **(required)** _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_

**`VoiceBotVoice`**

_One voice a provider offers: the URI to store it by, a name to show, and the provider's own metadata. `uri` IS THE RESULT. It is exactly what goes into `VoiceBotLanguage.voice`, so a form stores what it was given instead of assembling a string out of a provider name and an id — the one place a client could get the convention wrong._

- `uri` — string **(required)** — Voice URI, ready to store as `VoiceBotLanguage.voice` or send to TextToSpeech. The caller appends the synthesis parameters and, for a custom provider account, `apiKey=...` before storing it. _(pattern=^[a-z0-9][a-z0-9_-]*://[a-zA-Z0-9._~/-]+(\?[a-zA-Z0-9._~%&=+:/-]*)?$; minLen=1; maxLen=1024)_
- `name` — string **(required)** — Display name as the provider publishes it, e.g. 'Rachel'. A member rather than part of `metadata` because it is the one thing every provider has and every picker shows.
- `metadata` — any — The provider's own metadata for this voice, for rendering and filtering only. See VoiceBotVoiceMetadata.

**`VoiceSessionNotFoundExceptionResponseContent`**

- `message` — string **(required)**
- `type` — string _(default=VoiceSessionNotFoundException)_

</details>
