## Wilma Skills API 🆕

_OpenAPI: Wilma Skills Service — version v2_

**Servers**

- `https://api.wilma.wildix.com` — Production
- `https://api-stable.wilma.wildix.com` — Stable
- `https://api-stage.wilma.wildix.com` — Stage

### Skills

#### `GET` `/v2/skills`

Lists skills visible to the calling user.

- operationId: `ListSkills`
- **Scopes**: `wilma-skills:ListSkills`, `wilma-skills:read`
- **Parameters**
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `user` (query) — string _(minLen=12; maxLen=12)_
  - `scope` (query) — string — Filter by visibility to the caller. Defaults to `all`. _(enum: `mine`, `company`, `all`, `everyone`)_
  - `status` (query) — string _(enum: `draft`, `active`)_
  - `search` (query) — string — Filter by name or description.
  - `limit` (query) — number _(min=1; max=100)_
  - `cursor` (query) — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- **Response 200** (`ListSkillsResponseContent`)
  - `skills` — array **(required)**
    - _array of_ `SkillInfo`
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
      - `name` — string **(required)** — The skill's name as people see it: free text, editable, not unique. The identifier the model loads a skill by is not stored — it is a slug derived from this name when an agent's tools are built for a session, transliterated and numbered (`booking`, `booking-2`) so it is unique among the skills attached to that agent. Renaming a skill changes that slug and nothing else. _(minLen=1; maxLen=255)_
      - `description` — string **(required)** — What the skill does and when to use it. Loaded at discovery time for progressive disclosure. _(maxLen=1024)_
      - `status` — string **(required)** _(enum: `draft`, `active`)_
      - `access` — SkillAccess **(required)** — Who can use and edit the skill. Usage for private skills is limited to the creator, editors and viewers; company skills are attachable by anyone in the organization.
        - `visibility` — string _(enum: `private`, `company`)_
        - `editors` — array — Users and groups that may edit the draft. The creator always has edit access.
          - _array of_ `SkillGrantPrincipal`
            - _oneOf_ — exactly one of:
              - **`userId`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`groupId`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `viewers` — array — Users and groups the skill is shared with: they may see and attach it, but not edit. Redundant under company visibility.
          - _array of_ `SkillGrantPrincipal`
            - _oneOf_ — exactly one of:
              - **`userId`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`groupId`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `latestVersion` — number — Published skill version number. Monotonic within a skill's version history, starting at 1. _(min=1)_
      - `owned` — boolean — True when the calling user is the creator.
      - `editable` — boolean — True when the calling user may edit the draft.
  - `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- Errors: `400`, `403`

#### `POST` `/v2/skills`

Creates a new skill draft owned by the caller, complete with its bundled files: upload them with UploadSkillFile first and pass the returned ids in `files`. Defaults to private visibility. The skill serves no traffic until its first version is published.

- operationId: `CreateSkill`
- **Scopes**: `wilma-skills:CreateSkill`
- **Parameters**
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `user` (query) — string _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `CreateSkillRequestContent`) **(required)**
  - `description` — string **(required)** — What the skill does and when to use it. Loaded at discovery time for progressive disclosure. _(maxLen=1024)_
  - `content` — string **(required)** — The SKILL.md markdown body: the instructions themselves. Progressive disclosure: loaded when the skill is activated. Keep it concise and move detail into bundled files the agent reads on demand. _(minLen=1; maxLen=204800)_
  - `tools` — array — Tools the skill's instructions depend on, merged into the agent's toolset while the skill is active.
    - _array of_ `SkillTool`
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
  - `files` — array — Files bundled with the skill: references to uploaded content (UploadSkillFile) placed at bundle paths. The list is the complete bundle — a file left out of an update is no longer part of the skill, and changing a file means uploading a new one and referencing it at the same path. _(maxItems=200)_
    - _array of_ `SkillFile`
      - `id` — string **(required)** — Uploaded content this entry points at, as returned by UploadSkillFile. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
      - `path` — string **(required)** — Path the file is materialised at inside the bundle. _(pattern=^[a-zA-Z0-9](?:[a-zA-Z0-9._/-]*[a-zA-Z0-9_])?$; minLen=1; maxLen=1024)_
      - `name` — string — File name shown to the user. Defaults to the name recorded at upload. _(minLen=1; maxLen=255)_
      - `size` — number — Size in bytes. Ignored on input; the service reports the size of the stored content.
      - `executable` — boolean — Marks the file executable when it is materialised in the sandbox. Set per skill, not per upload.
  - `name` — string **(required)** — The skill's name as people see it: free text, editable, not unique. The identifier the model loads a skill by is not stored — it is a slug derived from this name when an agent's tools are built for a session, transliterated and numbered (`booking`, `booking-2`) so it is unique among the skills attached to that agent. Renaming a skill changes that slug and nothing else. _(minLen=1; maxLen=255)_
  - `access` — SkillAccess — Who can use and edit the skill. Usage for private skills is limited to the creator, editors and viewers; company skills are attachable by anyone in the organization.
    - `visibility` — string _(enum: `private`, `company`)_
    - `editors` — array — Users and groups that may edit the draft. The creator always has edit access.
      - _array of_ `SkillGrantPrincipal`
        - _oneOf_ — exactly one of:
          - **`userId`**
            - `userId` — string **(required)** _(minLen=12; maxLen=12)_
          - **`groupId`**
            - `groupId` — string **(required)**
    - `viewers` — array — Users and groups the skill is shared with: they may see and attach it, but not edit. Redundant under company visibility.
      - _array of_ `SkillGrantPrincipal`
        - _oneOf_ — exactly one of:
          - **`userId`**
            - `userId` — string **(required)** _(minLen=12; maxLen=12)_
          - **`groupId`**
            - `groupId` — string **(required)**
- **Response 200** (`CreateSkillResponseContent`)
  - `skill` — Skill **(required)** — The complete, versionable configuration of a skill, including the references to its bundled files.
    - `description` — string **(required)** — What the skill does and when to use it. Loaded at discovery time for progressive disclosure. _(maxLen=1024)_
    - `content` — string **(required)** — The SKILL.md markdown body: the instructions themselves. Progressive disclosure: loaded when the skill is activated. Keep it concise and move detail into bundled files the agent reads on demand. _(minLen=1; maxLen=204800)_
    - `tools` — array — Tools the skill's instructions depend on, merged into the agent's toolset while the skill is active.
      - _array of_ `SkillTool`
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
          - **`kb`**
            - `kb` — AgentKnowledgeBase **(required)**
              - `knowledgeBaseId` — string
              - `instructions` — string — Additional instructions for when the agent should use this knowledge base. _(minLen=1; maxLen=60000)_
              - `searchStrategy` — string — Search algorithm used to retrieve passages. _(enum: `bm25`, `vector`, `hybrid`)_
              - `searchThreshold` — string — Minimum similarity a passage needs to be returned. Raising it trades recall for precision. _(enum: `low`, `medium`, `high`)_
              - `searchLimit` — number — Maximum number of passages this capability returns. Defaults to the knowledge base service's own default (10) when omitted. Keep it low on voice: every passage is prompt the model reads before it can speak. _(min=1; max=50)_
              - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
                - _(nesting depth limit — see `ChannelType` in the Schemas appendix)_
              - `annotations` — array
                - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
          - **`webSearch`**
            - `webSearch` — AgentWebSearchCapability **(required)** — Model-native web search. The provider tool is selected from the agent model.
              - `contextSize` — string — Search depth/context hint, mapped per provider. _(enum: `low`, `medium`, `high`)_
              - `allowedDomains` — array — Restrict results to these domains where the provider supports it.
                - _array of_ `string`
              - `userLocation` — WebSearchUserLocation
                - _(nesting depth limit — see `WebSearchUserLocation` in the Schemas appendix)_
              - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
                - _(nesting depth limit — see `ChannelType` in the Schemas appendix)_
          - **`webFetch`**
            - `webFetch` — AgentWebFetchCapability **(required)** — Server-side fetch of a URL, returning its readable text/markdown to the model.
              - `allowedDomains` — array — Restrict fetches to these domains. Empty list means any domain is allowed.
                - _array of_ `string`
              - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
                - _(nesting depth limit — see `ChannelType` in the Schemas appendix)_
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
    - `files` — array — Files bundled with the skill: references to uploaded content (UploadSkillFile) placed at bundle paths. The list is the complete bundle — a file left out of an update is no longer part of the skill, and changing a file means uploading a new one and referencing it at the same path. _(maxItems=200)_
      - _array of_ `SkillFile`
        - `id` — string **(required)** — Uploaded content this entry points at, as returned by UploadSkillFile. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
        - `path` — string **(required)** — Path the file is materialised at inside the bundle. _(pattern=^[a-zA-Z0-9](?:[a-zA-Z0-9._/-]*[a-zA-Z0-9_])?$; minLen=1; maxLen=1024)_
        - `name` — string — File name shown to the user. Defaults to the name recorded at upload. _(minLen=1; maxLen=255)_
        - `size` — number — Size in bytes. Ignored on input; the service reports the size of the stored content.
        - `executable` — boolean — Marks the file executable when it is materialised in the sandbox. Set per skill, not per upload.
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
    - `name` — string **(required)** — The skill's name as people see it: free text, editable, not unique. The identifier the model loads a skill by is not stored — it is a slug derived from this name when an agent's tools are built for a session, transliterated and numbered (`booking`, `booking-2`) so it is unique among the skills attached to that agent. Renaming a skill changes that slug and nothing else. _(minLen=1; maxLen=255)_
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `access` — SkillAccess **(required)** — Who can use and edit the skill. Usage for private skills is limited to the creator, editors and viewers; company skills are attachable by anyone in the organization.
      - `visibility` — string _(enum: `private`, `company`)_
      - `editors` — array — Users and groups that may edit the draft. The creator always has edit access.
        - _array of_ `SkillGrantPrincipal`
          - _oneOf_ — exactly one of:
            - **`userId`**
              - `userId` — string **(required)** _(minLen=12; maxLen=12)_
            - **`groupId`**
              - `groupId` — string **(required)**
      - `viewers` — array — Users and groups the skill is shared with: they may see and attach it, but not edit. Redundant under company visibility.
        - _array of_ `SkillGrantPrincipal`
          - _oneOf_ — exactly one of:
            - **`userId`**
              - `userId` — string **(required)** _(minLen=12; maxLen=12)_
            - **`groupId`**
              - `groupId` — string **(required)**
    - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
    - `latestVersion` — number — Latest published version number, resolved by agent attachments that omit a version pin. Absent while the skill is still a draft. _(min=1)_
- Errors: `400`, `403`, `409`

#### `GET` `/v2/skills/items/{skillId}`

Gets a skill draft: metadata, SKILL.md content, tools, bundled file references and version state.

- operationId: `GetSkill`
- **Scopes**: `wilma-skills:GetSkill`, `wilma-skills:read`
- **Parameters**
  - `skillId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `user` (query) — string _(minLen=12; maxLen=12)_
- **Response 200** (`GetSkillResponseContent`)
  - `skill` — Skill **(required)** — The complete, versionable configuration of a skill, including the references to its bundled files.
    - `description` — string **(required)** — What the skill does and when to use it. Loaded at discovery time for progressive disclosure. _(maxLen=1024)_
    - `content` — string **(required)** — The SKILL.md markdown body: the instructions themselves. Progressive disclosure: loaded when the skill is activated. Keep it concise and move detail into bundled files the agent reads on demand. _(minLen=1; maxLen=204800)_
    - `tools` — array — Tools the skill's instructions depend on, merged into the agent's toolset while the skill is active.
      - _array of_ `SkillTool`
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
          - **`kb`**
            - `kb` — AgentKnowledgeBase **(required)**
              - `knowledgeBaseId` — string
              - `instructions` — string — Additional instructions for when the agent should use this knowledge base. _(minLen=1; maxLen=60000)_
              - `searchStrategy` — string — Search algorithm used to retrieve passages. _(enum: `bm25`, `vector`, `hybrid`)_
              - `searchThreshold` — string — Minimum similarity a passage needs to be returned. Raising it trades recall for precision. _(enum: `low`, `medium`, `high`)_
              - `searchLimit` — number — Maximum number of passages this capability returns. Defaults to the knowledge base service's own default (10) when omitted. Keep it low on voice: every passage is prompt the model reads before it can speak. _(min=1; max=50)_
              - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
                - _(nesting depth limit — see `ChannelType` in the Schemas appendix)_
              - `annotations` — array
                - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
          - **`webSearch`**
            - `webSearch` — AgentWebSearchCapability **(required)** — Model-native web search. The provider tool is selected from the agent model.
              - `contextSize` — string — Search depth/context hint, mapped per provider. _(enum: `low`, `medium`, `high`)_
              - `allowedDomains` — array — Restrict results to these domains where the provider supports it.
                - _array of_ `string`
              - `userLocation` — WebSearchUserLocation
                - _(nesting depth limit — see `WebSearchUserLocation` in the Schemas appendix)_
              - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
                - _(nesting depth limit — see `ChannelType` in the Schemas appendix)_
          - **`webFetch`**
            - `webFetch` — AgentWebFetchCapability **(required)** — Server-side fetch of a URL, returning its readable text/markdown to the model.
              - `allowedDomains` — array — Restrict fetches to these domains. Empty list means any domain is allowed.
                - _array of_ `string`
              - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
                - _(nesting depth limit — see `ChannelType` in the Schemas appendix)_
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
    - `files` — array — Files bundled with the skill: references to uploaded content (UploadSkillFile) placed at bundle paths. The list is the complete bundle — a file left out of an update is no longer part of the skill, and changing a file means uploading a new one and referencing it at the same path. _(maxItems=200)_
      - _array of_ `SkillFile`
        - `id` — string **(required)** — Uploaded content this entry points at, as returned by UploadSkillFile. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
        - `path` — string **(required)** — Path the file is materialised at inside the bundle. _(pattern=^[a-zA-Z0-9](?:[a-zA-Z0-9._/-]*[a-zA-Z0-9_])?$; minLen=1; maxLen=1024)_
        - `name` — string — File name shown to the user. Defaults to the name recorded at upload. _(minLen=1; maxLen=255)_
        - `size` — number — Size in bytes. Ignored on input; the service reports the size of the stored content.
        - `executable` — boolean — Marks the file executable when it is materialised in the sandbox. Set per skill, not per upload.
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
    - `name` — string **(required)** — The skill's name as people see it: free text, editable, not unique. The identifier the model loads a skill by is not stored — it is a slug derived from this name when an agent's tools are built for a session, transliterated and numbered (`booking`, `booking-2`) so it is unique among the skills attached to that agent. Renaming a skill changes that slug and nothing else. _(minLen=1; maxLen=255)_
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `access` — SkillAccess **(required)** — Who can use and edit the skill. Usage for private skills is limited to the creator, editors and viewers; company skills are attachable by anyone in the organization.
      - `visibility` — string _(enum: `private`, `company`)_
      - `editors` — array — Users and groups that may edit the draft. The creator always has edit access.
        - _array of_ `SkillGrantPrincipal`
          - _oneOf_ — exactly one of:
            - **`userId`**
              - `userId` — string **(required)** _(minLen=12; maxLen=12)_
            - **`groupId`**
              - `groupId` — string **(required)**
      - `viewers` — array — Users and groups the skill is shared with: they may see and attach it, but not edit. Redundant under company visibility.
        - _array of_ `SkillGrantPrincipal`
          - _oneOf_ — exactly one of:
            - **`userId`**
              - `userId` — string **(required)** _(minLen=12; maxLen=12)_
            - **`groupId`**
              - `groupId` — string **(required)**
    - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
    - `latestVersion` — number — Latest published version number, resolved by agent attachments that omit a version pin. Absent while the skill is still a draft. _(min=1)_
- Errors: `400`, `403`, `404`

#### `PUT` `/v2/skills/items/{skillId}`

Updates the draft definition or access policy. Does not affect served traffic until the draft
    is published. `files` is the complete bundle: add a file by uploading it with UploadSkillFile
    and including its id, remove one by leaving it out, and replace one by uploading a new file and
    referencing it at the same path. Published versions are never affected.

- operationId: `UpdateSkill`
- **Scopes**: `wilma-skills:UpdateSkill`
- **Parameters**
  - `skillId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `user` (query) — string _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `UpdateSkillRequestContent`) **(required)**
  - `description` — string **(required)** — What the skill does and when to use it. Loaded at discovery time for progressive disclosure. _(maxLen=1024)_
  - `content` — string **(required)** — The SKILL.md markdown body: the instructions themselves. Progressive disclosure: loaded when the skill is activated. Keep it concise and move detail into bundled files the agent reads on demand. _(minLen=1; maxLen=204800)_
  - `tools` — array — Tools the skill's instructions depend on, merged into the agent's toolset while the skill is active.
    - _array of_ `SkillTool`
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
  - `files` — array — Files bundled with the skill: references to uploaded content (UploadSkillFile) placed at bundle paths. The list is the complete bundle — a file left out of an update is no longer part of the skill, and changing a file means uploading a new one and referencing it at the same path. _(maxItems=200)_
    - _array of_ `SkillFile`
      - `id` — string **(required)** — Uploaded content this entry points at, as returned by UploadSkillFile. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
      - `path` — string **(required)** — Path the file is materialised at inside the bundle. _(pattern=^[a-zA-Z0-9](?:[a-zA-Z0-9._/-]*[a-zA-Z0-9_])?$; minLen=1; maxLen=1024)_
      - `name` — string — File name shown to the user. Defaults to the name recorded at upload. _(minLen=1; maxLen=255)_
      - `size` — number — Size in bytes. Ignored on input; the service reports the size of the stored content.
      - `executable` — boolean — Marks the file executable when it is materialised in the sandbox. Set per skill, not per upload.
  - `name` — string **(required)** — The skill's name as people see it: free text, editable, not unique. The identifier the model loads a skill by is not stored — it is a slug derived from this name when an agent's tools are built for a session, transliterated and numbered (`booking`, `booking-2`) so it is unique among the skills attached to that agent. Renaming a skill changes that slug and nothing else. _(minLen=1; maxLen=255)_
  - `revision` — number **(required)** — Draft revision this update is based on (optimistic locking). When it does not match the current revision, RevisionConflictException is returned.
  - `access` — SkillAccess — Who can use and edit the skill. Usage for private skills is limited to the creator, editors and viewers; company skills are attachable by anyone in the organization.
    - `visibility` — string _(enum: `private`, `company`)_
    - `editors` — array — Users and groups that may edit the draft. The creator always has edit access.
      - _array of_ `SkillGrantPrincipal`
        - _oneOf_ — exactly one of:
          - **`userId`**
            - `userId` — string **(required)** _(minLen=12; maxLen=12)_
          - **`groupId`**
            - `groupId` — string **(required)**
    - `viewers` — array — Users and groups the skill is shared with: they may see and attach it, but not edit. Redundant under company visibility.
      - _array of_ `SkillGrantPrincipal`
        - _oneOf_ — exactly one of:
          - **`userId`**
            - `userId` — string **(required)** _(minLen=12; maxLen=12)_
          - **`groupId`**
            - `groupId` — string **(required)**
- **Response 200** (`UpdateSkillResponseContent`)
  - `skill` — Skill **(required)** — The complete, versionable configuration of a skill, including the references to its bundled files.
    - `description` — string **(required)** — What the skill does and when to use it. Loaded at discovery time for progressive disclosure. _(maxLen=1024)_
    - `content` — string **(required)** — The SKILL.md markdown body: the instructions themselves. Progressive disclosure: loaded when the skill is activated. Keep it concise and move detail into bundled files the agent reads on demand. _(minLen=1; maxLen=204800)_
    - `tools` — array — Tools the skill's instructions depend on, merged into the agent's toolset while the skill is active.
      - _array of_ `SkillTool`
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
          - **`kb`**
            - `kb` — AgentKnowledgeBase **(required)**
              - `knowledgeBaseId` — string
              - `instructions` — string — Additional instructions for when the agent should use this knowledge base. _(minLen=1; maxLen=60000)_
              - `searchStrategy` — string — Search algorithm used to retrieve passages. _(enum: `bm25`, `vector`, `hybrid`)_
              - `searchThreshold` — string — Minimum similarity a passage needs to be returned. Raising it trades recall for precision. _(enum: `low`, `medium`, `high`)_
              - `searchLimit` — number — Maximum number of passages this capability returns. Defaults to the knowledge base service's own default (10) when omitted. Keep it low on voice: every passage is prompt the model reads before it can speak. _(min=1; max=50)_
              - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
                - _(nesting depth limit — see `ChannelType` in the Schemas appendix)_
              - `annotations` — array
                - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
          - **`webSearch`**
            - `webSearch` — AgentWebSearchCapability **(required)** — Model-native web search. The provider tool is selected from the agent model.
              - `contextSize` — string — Search depth/context hint, mapped per provider. _(enum: `low`, `medium`, `high`)_
              - `allowedDomains` — array — Restrict results to these domains where the provider supports it.
                - _array of_ `string`
              - `userLocation` — WebSearchUserLocation
                - _(nesting depth limit — see `WebSearchUserLocation` in the Schemas appendix)_
              - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
                - _(nesting depth limit — see `ChannelType` in the Schemas appendix)_
          - **`webFetch`**
            - `webFetch` — AgentWebFetchCapability **(required)** — Server-side fetch of a URL, returning its readable text/markdown to the model.
              - `allowedDomains` — array — Restrict fetches to these domains. Empty list means any domain is allowed.
                - _array of_ `string`
              - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
                - _(nesting depth limit — see `ChannelType` in the Schemas appendix)_
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
    - `files` — array — Files bundled with the skill: references to uploaded content (UploadSkillFile) placed at bundle paths. The list is the complete bundle — a file left out of an update is no longer part of the skill, and changing a file means uploading a new one and referencing it at the same path. _(maxItems=200)_
      - _array of_ `SkillFile`
        - `id` — string **(required)** — Uploaded content this entry points at, as returned by UploadSkillFile. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
        - `path` — string **(required)** — Path the file is materialised at inside the bundle. _(pattern=^[a-zA-Z0-9](?:[a-zA-Z0-9._/-]*[a-zA-Z0-9_])?$; minLen=1; maxLen=1024)_
        - `name` — string — File name shown to the user. Defaults to the name recorded at upload. _(minLen=1; maxLen=255)_
        - `size` — number — Size in bytes. Ignored on input; the service reports the size of the stored content.
        - `executable` — boolean — Marks the file executable when it is materialised in the sandbox. Set per skill, not per upload.
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
    - `name` — string **(required)** — The skill's name as people see it: free text, editable, not unique. The identifier the model loads a skill by is not stored — it is a slug derived from this name when an agent's tools are built for a session, transliterated and numbered (`booking`, `booking-2`) so it is unique among the skills attached to that agent. Renaming a skill changes that slug and nothing else. _(minLen=1; maxLen=255)_
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `access` — SkillAccess **(required)** — Who can use and edit the skill. Usage for private skills is limited to the creator, editors and viewers; company skills are attachable by anyone in the organization.
      - `visibility` — string _(enum: `private`, `company`)_
      - `editors` — array — Users and groups that may edit the draft. The creator always has edit access.
        - _array of_ `SkillGrantPrincipal`
          - _oneOf_ — exactly one of:
            - **`userId`**
              - `userId` — string **(required)** _(minLen=12; maxLen=12)_
            - **`groupId`**
              - `groupId` — string **(required)**
      - `viewers` — array — Users and groups the skill is shared with: they may see and attach it, but not edit. Redundant under company visibility.
        - _array of_ `SkillGrantPrincipal`
          - _oneOf_ — exactly one of:
            - **`userId`**
              - `userId` — string **(required)** _(minLen=12; maxLen=12)_
            - **`groupId`**
              - `groupId` — string **(required)**
    - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
    - `latestVersion` — number — Latest published version number, resolved by agent attachments that omit a version pin. Absent while the skill is still a draft. _(min=1)_
- Errors: `400`, `403`, `404`, `409`

#### `DELETE` `/v2/skills/items/{skillId}`

Deletes a skill, its bundled files and version history. Agents that still reference the skill keep the reference as a soft link: they run without it, the runtime skips the attachment, and their session traces record the missing skill id (`skill.missingIds`). Query wilma-audit references first to see who still names it.

- operationId: `DeleteSkill`
- **Scopes**: `wilma-skills:DeleteSkill`
- **Parameters**
  - `skillId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `user` (query) — string _(minLen=12; maxLen=12)_
- Errors: `400`, `403`

### Files

#### `POST` `/v2/skills/files`

Registers a skill file and returns a short-lived presigned PUT URL for its content. The client
    uploads the bytes directly to storage, then passes the returned `fileId` in the `files` of
    CreateSkill or UpdateSkill, together with the path the file should occupy in the bundle. Files
    are addressed by id alone, so they can be uploaded before the skill exists; a file never
    referenced by a skill is reclaimed. Content is immutable: to replace a file, upload a new one
    and reference it at the same path.

- operationId: `UploadSkillFile`
- **Scopes**: `wilma-skills:UploadSkillFile`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The user the upload belongs to. Optional: identifies the user when a service or tenant token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `UploadSkillFileRequestContent`) **(required)**
  - `name` — string **(required)** — File name shown to the user, e.g. 'api-reference.md'. Used as the download file name and as the default `name` of a skill file referencing this id. _(minLen=1; maxLen=255)_
  - `size` — number **(required)** — Declared size in bytes. Used for quota checks before the presigned URL is issued.
  - `contentType` — string — MIME type the client must send as the Content-Type header on PUT, e.g. 'application/pdf'.
- **Response 200** (`UploadSkillFileResponseContent`)
  - `fileId` — string **(required)** — Identifier of the registered file. Reference it in the `files` of CreateSkill / UpdateSkill, and pass it to DownloadSkillFile. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
  - `uploadUrl` — string **(required)** — Presigned URL to PUT the file content to. Short-lived: upload the bytes right away rather than storing the URL.
  - `expiresAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- Errors: `400`, `403`, `413`, `415`

#### `GET` `/v2/skills/files/items/{fileId}/download`

Returns a short-lived presigned URL to download a skill file's content, addressed by file id
    alone. Callers who can view a skill referencing the file, and the user who uploaded it, may
    download it.

- operationId: `DownloadSkillFile`
- **Scopes**: `wilma-skills:DownloadSkillFile`, `wilma-skills:read`
- **Parameters**
  - `fileId` (path) — string **(required)** — Identifier of uploaded file content, minted by UploadSkillFile. The content behind an id is immutable; to change a file, upload a new one and reference it at the same path. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The user requesting the download. Optional: identifies the user when a service or tenant token is used. _(minLen=12; maxLen=12)_
- **Response 200** (`DownloadSkillFileResponseContent`)
  - `url` — string **(required)** — Presigned download URL. Short-lived: fetch the content right away rather than storing the URL.
  - `expiresAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- Errors: `400`, `403`, `404`

### Versions

#### `GET` `/v2/skills/items/{skillId}/compare-versions`

Returns the field-level differences between two versions, or between a version and the current draft.

- operationId: `CompareSkillVersions`
- **Scopes**: `wilma-skills:CompareSkillVersions`, `wilma-skills:read`
- **Parameters**
  - `skillId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `from` (query) — number — Base published version number. Omit when fromDraft is true. _(min=1)_
  - `fromDraft` (query) — boolean — Use the current draft as the base instead of a published version.
  - `to` (query) — number — Target published version number. Omit when toDraft is true. _(min=1)_
  - `toDraft` (query) — boolean — Compare against the current draft instead of a published version.
- **Response 200** (`CompareSkillVersionsResponseContent`)
  - `changes` — array **(required)**
    - _array of_ `SkillVersionChange`
      - `path` — string **(required)** — JSON pointer of the changed field within the skill definition, e.g. '/content'.
      - `before` — any — Value before the change (absent when the field was added).
      - `after` — any — Value after the change (absent when the field was removed).
- Errors: `400`, `404`

#### `GET` `/v2/skills/items/{skillId}/versions`

Lists the published versions of a skill, newest first.

- operationId: `ListSkillVersions`
- **Scopes**: `wilma-skills:ListSkillVersions`, `wilma-skills:read`
- **Parameters**
  - `skillId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `limit` (query) — number _(min=1; max=100)_
  - `cursor` (query) — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- **Response 200** (`ListSkillVersionsResponseContent`)
  - `versions` — array **(required)**
    - _array of_ `SkillVersionInfo`
      - `skillId` — string **(required)** _(minLen=12; maxLen=12)_
      - `version` — number **(required)** — Published skill version number. Monotonic within a skill's version history, starting at 1. _(min=1)_
      - `changelog` — string — Human-readable description of what changed in a published version. _(minLen=1; maxLen=500)_
      - `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
        - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
        - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
        - `name` — string — Human readable name of the actor at the time of the action.
      - `latest` — boolean — True when this version is the skill's latestVersion.
  - `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- Errors: `400`, `404`

#### `POST` `/v2/skills/items/{skillId}/versions`

Publishes the current draft as a new immutable version and updates latestVersion. Unpinned agent attachments resolve latestVersion on their next load.

- operationId: `PublishSkillVersion`
- **Scopes**: `wilma-skills:PublishSkillVersion`
- **Parameters**
  - `skillId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `PublishSkillVersionRequestContent`) **(required)**
  - `changelog` — string — What changed in this version. _(minLen=1; maxLen=500)_
  - `revision` — number **(required)** — Draft revision this publish is based on (optimistic locking).
- **Response 200** (`PublishSkillVersionResponseContent`)
  - `version` — SkillVersion **(required)**
    - `skillId` — string **(required)** _(minLen=12; maxLen=12)_
    - `version` — number **(required)** — Published skill version number. Monotonic within a skill's version history, starting at 1. _(min=1)_
    - `changelog` — string — What changed in this version, provided at publish time. _(minLen=1; maxLen=500)_
    - `definition` — SkillDefinitionSnapshot **(required)** — Immutable skill definition snapshot captured at publish time. Its `files` reference the exact content the version was published with, so restoring is lossless.
      - `description` — string **(required)** — What the skill does and when to use it. Loaded at discovery time for progressive disclosure. _(maxLen=1024)_
      - `content` — string **(required)** — The SKILL.md markdown body: the instructions themselves. Progressive disclosure: loaded when the skill is activated. Keep it concise and move detail into bundled files the agent reads on demand. _(minLen=1; maxLen=204800)_
      - `tools` — array — Tools the skill's instructions depend on, merged into the agent's toolset while the skill is active.
        - _array of_ `SkillTool`
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
            - **`webSearch`**
              - `webSearch` — AgentWebSearchCapability **(required)** — Model-native web search. The provider tool is selected from the agent model.
                - _(nesting depth limit — see `AgentWebSearchCapability` in the Schemas appendix)_
            - **`webFetch`**
              - `webFetch` — AgentWebFetchCapability **(required)** — Server-side fetch of a URL, returning its readable text/markdown to the model.
                - _(nesting depth limit — see `AgentWebFetchCapability` in the Schemas appendix)_
            - **`transfer`**
              - `transfer` — AgentTransferCapability **(required)** — Transfer the call to a PBX destination. Honoured on the voice channel. One capability entry per transfer target.
                - _(nesting depth limit — see `AgentTransferCapability` in the Schemas appendix)_
            - **`hangup`**
              - `hangup` — AgentHangupCapability **(required)** — Let the model end the call. Honoured on the voice channel.
                - _(nesting depth limit — see `AgentHangupCapability` in the Schemas appendix)_
            - **`wait`**
              - `wait` — AgentWaitCapability **(required)** — Let the model hold the call while it works (e.g. a lookup), keeping the caller on the line. Honoured on the voice channel.
                - _(nesting depth limit — see `AgentWaitCapability` in the Schemas appendix)_
      - `files` — array — Files bundled with the skill: references to uploaded content (UploadSkillFile) placed at bundle paths. The list is the complete bundle — a file left out of an update is no longer part of the skill, and changing a file means uploading a new one and referencing it at the same path. _(maxItems=200)_
        - _array of_ `SkillFile`
          - `id` — string **(required)** — Uploaded content this entry points at, as returned by UploadSkillFile. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
          - `path` — string **(required)** — Path the file is materialised at inside the bundle. _(pattern=^[a-zA-Z0-9](?:[a-zA-Z0-9._/-]*[a-zA-Z0-9_])?$; minLen=1; maxLen=1024)_
          - `name` — string — File name shown to the user. Defaults to the name recorded at upload. _(minLen=1; maxLen=255)_
          - `size` — number — Size in bytes. Ignored on input; the service reports the size of the stored content.
          - `executable` — boolean — Marks the file executable when it is materialised in the sandbox. Set per skill, not per upload.
      - `name` — string **(required)** — The skill's name as people see it: free text, editable, not unique. The identifier the model loads a skill by is not stored — it is a slug derived from this name when an agent's tools are built for a session, transliterated and numbered (`booking`, `booking-2`) so it is unique among the skills attached to that agent. Renaming a skill changes that slug and nothing else. _(minLen=1; maxLen=255)_
    - `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
- Errors: `400`, `404`, `409`

#### `GET` `/v2/skills/items/{skillId}/versions/{version}`

Retrieves a published skill version, including its full immutable definition snapshot.

- operationId: `GetSkillVersion`
- **Scopes**: `wilma-skills:GetSkillVersion`, `wilma-skills:read`
- **Parameters**
  - `skillId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `version` (path) — number **(required)** — Published skill version number. Monotonic within a skill's version history, starting at 1. _(min=1)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Response 200** (`GetSkillVersionResponseContent`)
  - `version` — SkillVersion **(required)**
    - `skillId` — string **(required)** _(minLen=12; maxLen=12)_
    - `version` — number **(required)** — Published skill version number. Monotonic within a skill's version history, starting at 1. _(min=1)_
    - `changelog` — string — What changed in this version, provided at publish time. _(minLen=1; maxLen=500)_
    - `definition` — SkillDefinitionSnapshot **(required)** — Immutable skill definition snapshot captured at publish time. Its `files` reference the exact content the version was published with, so restoring is lossless.
      - `description` — string **(required)** — What the skill does and when to use it. Loaded at discovery time for progressive disclosure. _(maxLen=1024)_
      - `content` — string **(required)** — The SKILL.md markdown body: the instructions themselves. Progressive disclosure: loaded when the skill is activated. Keep it concise and move detail into bundled files the agent reads on demand. _(minLen=1; maxLen=204800)_
      - `tools` — array — Tools the skill's instructions depend on, merged into the agent's toolset while the skill is active.
        - _array of_ `SkillTool`
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
            - **`webSearch`**
              - `webSearch` — AgentWebSearchCapability **(required)** — Model-native web search. The provider tool is selected from the agent model.
                - _(nesting depth limit — see `AgentWebSearchCapability` in the Schemas appendix)_
            - **`webFetch`**
              - `webFetch` — AgentWebFetchCapability **(required)** — Server-side fetch of a URL, returning its readable text/markdown to the model.
                - _(nesting depth limit — see `AgentWebFetchCapability` in the Schemas appendix)_
            - **`transfer`**
              - `transfer` — AgentTransferCapability **(required)** — Transfer the call to a PBX destination. Honoured on the voice channel. One capability entry per transfer target.
                - _(nesting depth limit — see `AgentTransferCapability` in the Schemas appendix)_
            - **`hangup`**
              - `hangup` — AgentHangupCapability **(required)** — Let the model end the call. Honoured on the voice channel.
                - _(nesting depth limit — see `AgentHangupCapability` in the Schemas appendix)_
            - **`wait`**
              - `wait` — AgentWaitCapability **(required)** — Let the model hold the call while it works (e.g. a lookup), keeping the caller on the line. Honoured on the voice channel.
                - _(nesting depth limit — see `AgentWaitCapability` in the Schemas appendix)_
      - `files` — array — Files bundled with the skill: references to uploaded content (UploadSkillFile) placed at bundle paths. The list is the complete bundle — a file left out of an update is no longer part of the skill, and changing a file means uploading a new one and referencing it at the same path. _(maxItems=200)_
        - _array of_ `SkillFile`
          - `id` — string **(required)** — Uploaded content this entry points at, as returned by UploadSkillFile. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
          - `path` — string **(required)** — Path the file is materialised at inside the bundle. _(pattern=^[a-zA-Z0-9](?:[a-zA-Z0-9._/-]*[a-zA-Z0-9_])?$; minLen=1; maxLen=1024)_
          - `name` — string — File name shown to the user. Defaults to the name recorded at upload. _(minLen=1; maxLen=255)_
          - `size` — number — Size in bytes. Ignored on input; the service reports the size of the stored content.
          - `executable` — boolean — Marks the file executable when it is materialised in the sandbox. Set per skill, not per upload.
      - `name` — string **(required)** — The skill's name as people see it: free text, editable, not unique. The identifier the model loads a skill by is not stored — it is a slug derived from this name when an agent's tools are built for a session, transliterated and numbered (`booking`, `booking-2`) so it is unique among the skills attached to that agent. Renaming a skill changes that slug and nothing else. _(minLen=1; maxLen=255)_
    - `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
- Errors: `400`, `404`

#### `POST` `/v2/skills/items/{skillId}/versions/{version}/draft`

Replaces the mutable draft with a published version's definition. The draft revision is incremented; published versions and latestVersion are unchanged until the draft is published.

- operationId: `RestoreSkillVersionToDraft`
- **Scopes**: `wilma-skills:RestoreSkillVersionToDraft`
- **Parameters**
  - `skillId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `version` (path) — number **(required)** — Published skill version number. Monotonic within a skill's version history, starting at 1. _(min=1)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `RestoreSkillVersionToDraftRequestContent`) **(required)**
  - `revision` — number **(required)** — Draft revision this restore is based on (optimistic locking).
- **Response 200** (`RestoreSkillVersionToDraftResponseContent`)
  - `skill` — Skill **(required)** — The complete, versionable configuration of a skill, including the references to its bundled files.
    - `description` — string **(required)** — What the skill does and when to use it. Loaded at discovery time for progressive disclosure. _(maxLen=1024)_
    - `content` — string **(required)** — The SKILL.md markdown body: the instructions themselves. Progressive disclosure: loaded when the skill is activated. Keep it concise and move detail into bundled files the agent reads on demand. _(minLen=1; maxLen=204800)_
    - `tools` — array — Tools the skill's instructions depend on, merged into the agent's toolset while the skill is active.
      - _array of_ `SkillTool`
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
          - **`kb`**
            - `kb` — AgentKnowledgeBase **(required)**
              - `knowledgeBaseId` — string
              - `instructions` — string — Additional instructions for when the agent should use this knowledge base. _(minLen=1; maxLen=60000)_
              - `searchStrategy` — string — Search algorithm used to retrieve passages. _(enum: `bm25`, `vector`, `hybrid`)_
              - `searchThreshold` — string — Minimum similarity a passage needs to be returned. Raising it trades recall for precision. _(enum: `low`, `medium`, `high`)_
              - `searchLimit` — number — Maximum number of passages this capability returns. Defaults to the knowledge base service's own default (10) when omitted. Keep it low on voice: every passage is prompt the model reads before it can speak. _(min=1; max=50)_
              - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
                - _(nesting depth limit — see `ChannelType` in the Schemas appendix)_
              - `annotations` — array
                - _(nesting depth limit — see `AgentToolAnnotation` in the Schemas appendix)_
          - **`webSearch`**
            - `webSearch` — AgentWebSearchCapability **(required)** — Model-native web search. The provider tool is selected from the agent model.
              - `contextSize` — string — Search depth/context hint, mapped per provider. _(enum: `low`, `medium`, `high`)_
              - `allowedDomains` — array — Restrict results to these domains where the provider supports it.
                - _array of_ `string`
              - `userLocation` — WebSearchUserLocation
                - _(nesting depth limit — see `WebSearchUserLocation` in the Schemas appendix)_
              - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
                - _(nesting depth limit — see `ChannelType` in the Schemas appendix)_
          - **`webFetch`**
            - `webFetch` — AgentWebFetchCapability **(required)** — Server-side fetch of a URL, returning its readable text/markdown to the model.
              - `allowedDomains` — array — Restrict fetches to these domains. Empty list means any domain is allowed.
                - _array of_ `string`
              - `channels` — array — Channels this capability is offered on. Absent or empty — the default — means every channel the agent serves that can honour it. Listing channels narrows that set and never widens it: a `transfer` listed for `chat` is still ignored there, because the chat channel has no call to transfer.
                - _(nesting depth limit — see `ChannelType` in the Schemas appendix)_
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
    - `files` — array — Files bundled with the skill: references to uploaded content (UploadSkillFile) placed at bundle paths. The list is the complete bundle — a file left out of an update is no longer part of the skill, and changing a file means uploading a new one and referencing it at the same path. _(maxItems=200)_
      - _array of_ `SkillFile`
        - `id` — string **(required)** — Uploaded content this entry points at, as returned by UploadSkillFile. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
        - `path` — string **(required)** — Path the file is materialised at inside the bundle. _(pattern=^[a-zA-Z0-9](?:[a-zA-Z0-9._/-]*[a-zA-Z0-9_])?$; minLen=1; maxLen=1024)_
        - `name` — string — File name shown to the user. Defaults to the name recorded at upload. _(minLen=1; maxLen=255)_
        - `size` — number — Size in bytes. Ignored on input; the service reports the size of the stored content.
        - `executable` — boolean — Marks the file executable when it is materialised in the sandbox. Set per skill, not per upload.
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
    - `name` — string **(required)** — The skill's name as people see it: free text, editable, not unique. The identifier the model loads a skill by is not stored — it is a slug derived from this name when an agent's tools are built for a session, transliterated and numbered (`booking`, `booking-2`) so it is unique among the skills attached to that agent. Renaming a skill changes that slug and nothing else. _(minLen=1; maxLen=255)_
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `access` — SkillAccess **(required)** — Who can use and edit the skill. Usage for private skills is limited to the creator, editors and viewers; company skills are attachable by anyone in the organization.
      - `visibility` — string _(enum: `private`, `company`)_
      - `editors` — array — Users and groups that may edit the draft. The creator always has edit access.
        - _array of_ `SkillGrantPrincipal`
          - _oneOf_ — exactly one of:
            - **`userId`**
              - `userId` — string **(required)** _(minLen=12; maxLen=12)_
            - **`groupId`**
              - `groupId` — string **(required)**
      - `viewers` — array — Users and groups the skill is shared with: they may see and attach it, but not edit. Redundant under company visibility.
        - _array of_ `SkillGrantPrincipal`
          - _oneOf_ — exactly one of:
            - **`userId`**
              - `userId` — string **(required)** _(minLen=12; maxLen=12)_
            - **`groupId`**
              - `groupId` — string **(required)**
    - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
    - `latestVersion` — number — Latest published version number, resolved by agent attachments that omit a version pin. Absent while the skill is still a draft. _(min=1)_
- Errors: `400`, `404`, `409`

### Schemas appendix — Wilma Skills API

<details><summary>69 component schemas</summary>

**`Actor`**

_Who performed an action: an interactive user, an API key or an internal service._

- `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
- `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
- `name` — string — Human readable name of the actor at the time of the action.

**`ActorType`**

- string _(enum: `user`, `api_key`, `service`)_

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

**`AgentSpokenPhrase`**

_One phrase in one language, for a capability that speaks a fixed line on the voice channel. Which entry is spoken is decided by the call's current language — the one the call resolved to at connect, or the one automatic detection switched to — matched on `language` CASE-INSENSITIVELY, the same rule `VoiceBotSpokenPhrase` states for the legacy stack, so a code written in either case reaches the same entry on either. Blank `text` means the agent says nothing in that language; it does NOT fall back to the language-agnostic member beside the list, which would speak one language's text in another language's voice._

- `language` — string **(required)** — BCP-47 language tag, optionally with a region subtag: 'en', 'en-US', 'pt-BR'. Deliberately a constrained string rather than an enum: the offerable set is a property of the selected recogniser and changes with it, so an enumeration here would cap the set at whatever was known when the model was released. _(pattern=^[a-z]{2,3}(-[A-Z]{2})?$; minLen=2; maxLen=8)_
- `text` — string **(required)**

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

**`ChannelType`**

_A channel an agent can serve (see AgentChannels for enablement). Also the runtime channel recorded by the channel runtimes / wilma-traces. A background task has no delivery surface and therefore no channel._

- string _(enum: `voice`, `chat`, `assistant`)_

**`CompareSkillVersionsResponseContent`**

- `changes` — array **(required)**
  - _array of_ `SkillVersionChange`
    - `path` — string **(required)** — JSON pointer of the changed field within the skill definition, e.g. '/content'.
    - `before` — any — Value before the change (absent when the field was added).
    - `after` — any — Value after the change (absent when the field was removed).

**`ConflictExceptionResponseContent`**

_The request conflicts with the current state of the resource, e.g. a duplicate name, a resource still in use, or an unmet precondition._

- `message` — string **(required)**

**`CreateSkillRequestContent`**

- `description` — string **(required)** — What the skill does and when to use it. Loaded at discovery time for progressive disclosure. _(maxLen=1024)_
- `content` — string **(required)** — The SKILL.md markdown body: the instructions themselves. Progressive disclosure: loaded when the skill is activated. Keep it concise and move detail into bundled files the agent reads on demand. _(minLen=1; maxLen=204800)_
- `tools` — array — Tools the skill's instructions depend on, merged into the agent's toolset while the skill is active.
  - _array of_ `SkillTool`
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
      - **`webSearch`**
        - `webSearch` — AgentWebSearchCapability **(required)** — Model-native web search. The provider tool is selected from the agent model.
          - _(nesting depth limit — see `AgentWebSearchCapability` in the Schemas appendix)_
      - **`webFetch`**
        - `webFetch` — AgentWebFetchCapability **(required)** — Server-side fetch of a URL, returning its readable text/markdown to the model.
          - _(nesting depth limit — see `AgentWebFetchCapability` in the Schemas appendix)_
      - **`transfer`**
        - `transfer` — AgentTransferCapability **(required)** — Transfer the call to a PBX destination. Honoured on the voice channel. One capability entry per transfer target.
          - _(nesting depth limit — see `AgentTransferCapability` in the Schemas appendix)_
      - **`hangup`**
        - `hangup` — AgentHangupCapability **(required)** — Let the model end the call. Honoured on the voice channel.
          - _(nesting depth limit — see `AgentHangupCapability` in the Schemas appendix)_
      - **`wait`**
        - `wait` — AgentWaitCapability **(required)** — Let the model hold the call while it works (e.g. a lookup), keeping the caller on the line. Honoured on the voice channel.
          - _(nesting depth limit — see `AgentWaitCapability` in the Schemas appendix)_
- `files` — array — Files bundled with the skill: references to uploaded content (UploadSkillFile) placed at bundle paths. The list is the complete bundle — a file left out of an update is no longer part of the skill, and changing a file means uploading a new one and referencing it at the same path. _(maxItems=200)_
  - _array of_ `SkillFile`
    - `id` — string **(required)** — Uploaded content this entry points at, as returned by UploadSkillFile. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
    - `path` — string **(required)** — Path the file is materialised at inside the bundle. _(pattern=^[a-zA-Z0-9](?:[a-zA-Z0-9._/-]*[a-zA-Z0-9_])?$; minLen=1; maxLen=1024)_
    - `name` — string — File name shown to the user. Defaults to the name recorded at upload. _(minLen=1; maxLen=255)_
    - `size` — number — Size in bytes. Ignored on input; the service reports the size of the stored content.
    - `executable` — boolean — Marks the file executable when it is materialised in the sandbox. Set per skill, not per upload.
- `name` — string **(required)** — The skill's name as people see it: free text, editable, not unique. The identifier the model loads a skill by is not stored — it is a slug derived from this name when an agent's tools are built for a session, transliterated and numbered (`booking`, `booking-2`) so it is unique among the skills attached to that agent. Renaming a skill changes that slug and nothing else. _(minLen=1; maxLen=255)_
- `access` — SkillAccess — Who can use and edit the skill. Usage for private skills is limited to the creator, editors and viewers; company skills are attachable by anyone in the organization.
  - `visibility` — string _(enum: `private`, `company`)_
  - `editors` — array — Users and groups that may edit the draft. The creator always has edit access.
    - _array of_ `SkillGrantPrincipal`
      - _oneOf_ — exactly one of:
        - **`userId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`groupId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `viewers` — array — Users and groups the skill is shared with: they may see and attach it, but not edit. Redundant under company visibility.
    - _array of_ `SkillGrantPrincipal`
      - _oneOf_ — exactly one of:
        - **`userId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`groupId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_

**`CreateSkillResponseContent`**

- `skill` — Skill **(required)** — The complete, versionable configuration of a skill, including the references to its bundled files.
  - `description` — string **(required)** — What the skill does and when to use it. Loaded at discovery time for progressive disclosure. _(maxLen=1024)_
  - `content` — string **(required)** — The SKILL.md markdown body: the instructions themselves. Progressive disclosure: loaded when the skill is activated. Keep it concise and move detail into bundled files the agent reads on demand. _(minLen=1; maxLen=204800)_
  - `tools` — array — Tools the skill's instructions depend on, merged into the agent's toolset while the skill is active.
    - _array of_ `SkillTool`
      - _oneOf_ — exactly one of:
        - **`tool`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`connector`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`kb`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`webSearch`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`webFetch`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`transfer`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`hangup`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`wait`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `files` — array — Files bundled with the skill: references to uploaded content (UploadSkillFile) placed at bundle paths. The list is the complete bundle — a file left out of an update is no longer part of the skill, and changing a file means uploading a new one and referencing it at the same path. _(maxItems=200)_
    - _array of_ `SkillFile`
      - `id` — string **(required)** — Uploaded content this entry points at, as returned by UploadSkillFile. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
      - `path` — string **(required)** — Path the file is materialised at inside the bundle. _(pattern=^[a-zA-Z0-9](?:[a-zA-Z0-9._/-]*[a-zA-Z0-9_])?$; minLen=1; maxLen=1024)_
      - `name` — string — File name shown to the user. Defaults to the name recorded at upload. _(minLen=1; maxLen=255)_
      - `size` — number — Size in bytes. Ignored on input; the service reports the size of the stored content.
      - `executable` — boolean — Marks the file executable when it is materialised in the sandbox. Set per skill, not per upload.
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
  - `name` — string **(required)** — The skill's name as people see it: free text, editable, not unique. The identifier the model loads a skill by is not stored — it is a slug derived from this name when an agent's tools are built for a session, transliterated and numbered (`booking`, `booking-2`) so it is unique among the skills attached to that agent. Renaming a skill changes that slug and nothing else. _(minLen=1; maxLen=255)_
  - `status` — string **(required)** _(enum: `draft`, `active`)_
  - `access` — SkillAccess **(required)** — Who can use and edit the skill. Usage for private skills is limited to the creator, editors and viewers; company skills are attachable by anyone in the organization.
    - `visibility` — string _(enum: `private`, `company`)_
    - `editors` — array — Users and groups that may edit the draft. The creator always has edit access.
      - _array of_ `SkillGrantPrincipal`
        - _(nesting depth limit — see `SkillGrantPrincipal` in the Schemas appendix)_
    - `viewers` — array — Users and groups the skill is shared with: they may see and attach it, but not edit. Redundant under company visibility.
      - _array of_ `SkillGrantPrincipal`
        - _(nesting depth limit — see `SkillGrantPrincipal` in the Schemas appendix)_
  - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
  - `latestVersion` — number — Latest published version number, resolved by agent attachments that omit a version pin. Absent while the skill is still a draft. _(min=1)_

**`DownloadSkillFileResponseContent`**

- `url` — string **(required)** — Presigned download URL. Short-lived: fetch the content right away rather than storing the URL.
- `expiresAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GetSkillResponseContent`**

- `skill` — Skill **(required)** — The complete, versionable configuration of a skill, including the references to its bundled files.
  - `description` — string **(required)** — What the skill does and when to use it. Loaded at discovery time for progressive disclosure. _(maxLen=1024)_
  - `content` — string **(required)** — The SKILL.md markdown body: the instructions themselves. Progressive disclosure: loaded when the skill is activated. Keep it concise and move detail into bundled files the agent reads on demand. _(minLen=1; maxLen=204800)_
  - `tools` — array — Tools the skill's instructions depend on, merged into the agent's toolset while the skill is active.
    - _array of_ `SkillTool`
      - _oneOf_ — exactly one of:
        - **`tool`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`connector`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`kb`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`webSearch`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`webFetch`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`transfer`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`hangup`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`wait`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `files` — array — Files bundled with the skill: references to uploaded content (UploadSkillFile) placed at bundle paths. The list is the complete bundle — a file left out of an update is no longer part of the skill, and changing a file means uploading a new one and referencing it at the same path. _(maxItems=200)_
    - _array of_ `SkillFile`
      - `id` — string **(required)** — Uploaded content this entry points at, as returned by UploadSkillFile. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
      - `path` — string **(required)** — Path the file is materialised at inside the bundle. _(pattern=^[a-zA-Z0-9](?:[a-zA-Z0-9._/-]*[a-zA-Z0-9_])?$; minLen=1; maxLen=1024)_
      - `name` — string — File name shown to the user. Defaults to the name recorded at upload. _(minLen=1; maxLen=255)_
      - `size` — number — Size in bytes. Ignored on input; the service reports the size of the stored content.
      - `executable` — boolean — Marks the file executable when it is materialised in the sandbox. Set per skill, not per upload.
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
  - `name` — string **(required)** — The skill's name as people see it: free text, editable, not unique. The identifier the model loads a skill by is not stored — it is a slug derived from this name when an agent's tools are built for a session, transliterated and numbered (`booking`, `booking-2`) so it is unique among the skills attached to that agent. Renaming a skill changes that slug and nothing else. _(minLen=1; maxLen=255)_
  - `status` — string **(required)** _(enum: `draft`, `active`)_
  - `access` — SkillAccess **(required)** — Who can use and edit the skill. Usage for private skills is limited to the creator, editors and viewers; company skills are attachable by anyone in the organization.
    - `visibility` — string _(enum: `private`, `company`)_
    - `editors` — array — Users and groups that may edit the draft. The creator always has edit access.
      - _array of_ `SkillGrantPrincipal`
        - _(nesting depth limit — see `SkillGrantPrincipal` in the Schemas appendix)_
    - `viewers` — array — Users and groups the skill is shared with: they may see and attach it, but not edit. Redundant under company visibility.
      - _array of_ `SkillGrantPrincipal`
        - _(nesting depth limit — see `SkillGrantPrincipal` in the Schemas appendix)_
  - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
  - `latestVersion` — number — Latest published version number, resolved by agent attachments that omit a version pin. Absent while the skill is still a draft. _(min=1)_

**`GetSkillVersionResponseContent`**

- `version` — SkillVersion **(required)**
  - `skillId` — string **(required)** _(minLen=12; maxLen=12)_
  - `version` — number **(required)** — Published skill version number. Monotonic within a skill's version history, starting at 1. _(min=1)_
  - `changelog` — string — What changed in this version, provided at publish time. _(minLen=1; maxLen=500)_
  - `definition` — SkillDefinitionSnapshot **(required)** — Immutable skill definition snapshot captured at publish time. Its `files` reference the exact content the version was published with, so restoring is lossless.
    - `description` — string **(required)** — What the skill does and when to use it. Loaded at discovery time for progressive disclosure. _(maxLen=1024)_
    - `content` — string **(required)** — The SKILL.md markdown body: the instructions themselves. Progressive disclosure: loaded when the skill is activated. Keep it concise and move detail into bundled files the agent reads on demand. _(minLen=1; maxLen=204800)_
    - `tools` — array — Tools the skill's instructions depend on, merged into the agent's toolset while the skill is active.
      - _array of_ `SkillTool`
        - _(nesting depth limit — see `SkillTool` in the Schemas appendix)_
    - `files` — array — Files bundled with the skill: references to uploaded content (UploadSkillFile) placed at bundle paths. The list is the complete bundle — a file left out of an update is no longer part of the skill, and changing a file means uploading a new one and referencing it at the same path. _(maxItems=200)_
      - _array of_ `SkillFile`
        - _(nesting depth limit — see `SkillFile` in the Schemas appendix)_
    - `name` — string **(required)** — The skill's name as people see it: free text, editable, not unique. The identifier the model loads a skill by is not stored — it is a slug derived from this name when an agent's tools are built for a session, transliterated and numbered (`booking`, `booking-2`) so it is unique among the skills attached to that agent. Renaming a skill changes that slug and nothing else. _(minLen=1; maxLen=255)_
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

**`ListSkillVersionsResponseContent`**

- `versions` — array **(required)**
  - _array of_ `SkillVersionInfo`
    - `skillId` — string **(required)** _(minLen=12; maxLen=12)_
    - `version` — number **(required)** — Published skill version number. Monotonic within a skill's version history, starting at 1. _(min=1)_
    - `changelog` — string — Human-readable description of what changed in a published version. _(minLen=1; maxLen=500)_
    - `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
    - `latest` — boolean — True when this version is the skill's latestVersion.
- `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_

**`ListSkillsResponseContent`**

- `skills` — array **(required)**
  - _array of_ `SkillInfo`
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
    - `name` — string **(required)** — The skill's name as people see it: free text, editable, not unique. The identifier the model loads a skill by is not stored — it is a slug derived from this name when an agent's tools are built for a session, transliterated and numbered (`booking`, `booking-2`) so it is unique among the skills attached to that agent. Renaming a skill changes that slug and nothing else. _(minLen=1; maxLen=255)_
    - `description` — string **(required)** — What the skill does and when to use it. Loaded at discovery time for progressive disclosure. _(maxLen=1024)_
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `access` — SkillAccess **(required)** — Who can use and edit the skill. Usage for private skills is limited to the creator, editors and viewers; company skills are attachable by anyone in the organization.
      - `visibility` — string _(enum: `private`, `company`)_
      - `editors` — array — Users and groups that may edit the draft. The creator always has edit access.
        - _(nesting depth limit — see `SkillGrantPrincipal` in the Schemas appendix)_
      - `viewers` — array — Users and groups the skill is shared with: they may see and attach it, but not edit. Redundant under company visibility.
        - _(nesting depth limit — see `SkillGrantPrincipal` in the Schemas appendix)_
    - `latestVersion` — number — Published skill version number. Monotonic within a skill's version history, starting at 1. _(min=1)_
    - `owned` — boolean — True when the calling user is the creator.
    - `editable` — boolean — True when the calling user may edit the draft.
- `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_

**`NotFoundExceptionResponseContent`**

- `message` — string **(required)** _(default=Not found)_

**`PayloadTooLargeExceptionResponseContent`**

_The request payload is larger than the service allows._

- `message` — string **(required)**

**`PublishSkillVersionRequestContent`**

- `changelog` — string — What changed in this version. _(minLen=1; maxLen=500)_
- `revision` — number **(required)** — Draft revision this publish is based on (optimistic locking).

**`PublishSkillVersionResponseContent`**

- `version` — SkillVersion **(required)**
  - `skillId` — string **(required)** _(minLen=12; maxLen=12)_
  - `version` — number **(required)** — Published skill version number. Monotonic within a skill's version history, starting at 1. _(min=1)_
  - `changelog` — string — What changed in this version, provided at publish time. _(minLen=1; maxLen=500)_
  - `definition` — SkillDefinitionSnapshot **(required)** — Immutable skill definition snapshot captured at publish time. Its `files` reference the exact content the version was published with, so restoring is lossless.
    - `description` — string **(required)** — What the skill does and when to use it. Loaded at discovery time for progressive disclosure. _(maxLen=1024)_
    - `content` — string **(required)** — The SKILL.md markdown body: the instructions themselves. Progressive disclosure: loaded when the skill is activated. Keep it concise and move detail into bundled files the agent reads on demand. _(minLen=1; maxLen=204800)_
    - `tools` — array — Tools the skill's instructions depend on, merged into the agent's toolset while the skill is active.
      - _array of_ `SkillTool`
        - _(nesting depth limit — see `SkillTool` in the Schemas appendix)_
    - `files` — array — Files bundled with the skill: references to uploaded content (UploadSkillFile) placed at bundle paths. The list is the complete bundle — a file left out of an update is no longer part of the skill, and changing a file means uploading a new one and referencing it at the same path. _(maxItems=200)_
      - _array of_ `SkillFile`
        - _(nesting depth limit — see `SkillFile` in the Schemas appendix)_
    - `name` — string **(required)** — The skill's name as people see it: free text, editable, not unique. The identifier the model loads a skill by is not stored — it is a slug derived from this name when an agent's tools are built for a session, transliterated and numbered (`booking`, `booking-2`) so it is unique among the skills attached to that agent. Renaming a skill changes that slug and nothing else. _(minLen=1; maxLen=255)_
  - `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
    - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
    - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
    - `name` — string — Human readable name of the actor at the time of the action.

**`RestoreSkillVersionToDraftRequestContent`**

- `revision` — number **(required)** — Draft revision this restore is based on (optimistic locking).

**`RestoreSkillVersionToDraftResponseContent`**

- `skill` — Skill **(required)** — The complete, versionable configuration of a skill, including the references to its bundled files.
  - `description` — string **(required)** — What the skill does and when to use it. Loaded at discovery time for progressive disclosure. _(maxLen=1024)_
  - `content` — string **(required)** — The SKILL.md markdown body: the instructions themselves. Progressive disclosure: loaded when the skill is activated. Keep it concise and move detail into bundled files the agent reads on demand. _(minLen=1; maxLen=204800)_
  - `tools` — array — Tools the skill's instructions depend on, merged into the agent's toolset while the skill is active.
    - _array of_ `SkillTool`
      - _oneOf_ — exactly one of:
        - **`tool`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`connector`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`kb`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`webSearch`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`webFetch`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`transfer`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`hangup`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`wait`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `files` — array — Files bundled with the skill: references to uploaded content (UploadSkillFile) placed at bundle paths. The list is the complete bundle — a file left out of an update is no longer part of the skill, and changing a file means uploading a new one and referencing it at the same path. _(maxItems=200)_
    - _array of_ `SkillFile`
      - `id` — string **(required)** — Uploaded content this entry points at, as returned by UploadSkillFile. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
      - `path` — string **(required)** — Path the file is materialised at inside the bundle. _(pattern=^[a-zA-Z0-9](?:[a-zA-Z0-9._/-]*[a-zA-Z0-9_])?$; minLen=1; maxLen=1024)_
      - `name` — string — File name shown to the user. Defaults to the name recorded at upload. _(minLen=1; maxLen=255)_
      - `size` — number — Size in bytes. Ignored on input; the service reports the size of the stored content.
      - `executable` — boolean — Marks the file executable when it is materialised in the sandbox. Set per skill, not per upload.
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
  - `name` — string **(required)** — The skill's name as people see it: free text, editable, not unique. The identifier the model loads a skill by is not stored — it is a slug derived from this name when an agent's tools are built for a session, transliterated and numbered (`booking`, `booking-2`) so it is unique among the skills attached to that agent. Renaming a skill changes that slug and nothing else. _(minLen=1; maxLen=255)_
  - `status` — string **(required)** _(enum: `draft`, `active`)_
  - `access` — SkillAccess **(required)** — Who can use and edit the skill. Usage for private skills is limited to the creator, editors and viewers; company skills are attachable by anyone in the organization.
    - `visibility` — string _(enum: `private`, `company`)_
    - `editors` — array — Users and groups that may edit the draft. The creator always has edit access.
      - _array of_ `SkillGrantPrincipal`
        - _(nesting depth limit — see `SkillGrantPrincipal` in the Schemas appendix)_
    - `viewers` — array — Users and groups the skill is shared with: they may see and attach it, but not edit. Redundant under company visibility.
      - _array of_ `SkillGrantPrincipal`
        - _(nesting depth limit — see `SkillGrantPrincipal` in the Schemas appendix)_
  - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
  - `latestVersion` — number — Latest published version number, resolved by agent attachments that omit a version pin. Absent while the skill is still a draft. _(min=1)_

**`RevisionConflictExceptionResponseContent`**

_The resource was modified concurrently; re-read it and retry with the latest revision._

- `message` — string **(required)**
- `type` — string _(default=RevisionConflictException)_
- `currentRevision` — number — The current revision of the resource on the server.

**`Skill`**

_The complete, versionable configuration of a skill, including the references to its bundled files._

- `description` — string **(required)** — What the skill does and when to use it. Loaded at discovery time for progressive disclosure. _(maxLen=1024)_
- `content` — string **(required)** — The SKILL.md markdown body: the instructions themselves. Progressive disclosure: loaded when the skill is activated. Keep it concise and move detail into bundled files the agent reads on demand. _(minLen=1; maxLen=204800)_
- `tools` — array — Tools the skill's instructions depend on, merged into the agent's toolset while the skill is active.
  - _array of_ `SkillTool`
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
      - **`webSearch`**
        - `webSearch` — AgentWebSearchCapability **(required)** — Model-native web search. The provider tool is selected from the agent model.
          - _(nesting depth limit — see `AgentWebSearchCapability` in the Schemas appendix)_
      - **`webFetch`**
        - `webFetch` — AgentWebFetchCapability **(required)** — Server-side fetch of a URL, returning its readable text/markdown to the model.
          - _(nesting depth limit — see `AgentWebFetchCapability` in the Schemas appendix)_
      - **`transfer`**
        - `transfer` — AgentTransferCapability **(required)** — Transfer the call to a PBX destination. Honoured on the voice channel. One capability entry per transfer target.
          - _(nesting depth limit — see `AgentTransferCapability` in the Schemas appendix)_
      - **`hangup`**
        - `hangup` — AgentHangupCapability **(required)** — Let the model end the call. Honoured on the voice channel.
          - _(nesting depth limit — see `AgentHangupCapability` in the Schemas appendix)_
      - **`wait`**
        - `wait` — AgentWaitCapability **(required)** — Let the model hold the call while it works (e.g. a lookup), keeping the caller on the line. Honoured on the voice channel.
          - _(nesting depth limit — see `AgentWaitCapability` in the Schemas appendix)_
- `files` — array — Files bundled with the skill: references to uploaded content (UploadSkillFile) placed at bundle paths. The list is the complete bundle — a file left out of an update is no longer part of the skill, and changing a file means uploading a new one and referencing it at the same path. _(maxItems=200)_
  - _array of_ `SkillFile`
    - `id` — string **(required)** — Uploaded content this entry points at, as returned by UploadSkillFile. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
    - `path` — string **(required)** — Path the file is materialised at inside the bundle. _(pattern=^[a-zA-Z0-9](?:[a-zA-Z0-9._/-]*[a-zA-Z0-9_])?$; minLen=1; maxLen=1024)_
    - `name` — string — File name shown to the user. Defaults to the name recorded at upload. _(minLen=1; maxLen=255)_
    - `size` — number — Size in bytes. Ignored on input; the service reports the size of the stored content.
    - `executable` — boolean — Marks the file executable when it is materialised in the sandbox. Set per skill, not per upload.
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
- `name` — string **(required)** — The skill's name as people see it: free text, editable, not unique. The identifier the model loads a skill by is not stored — it is a slug derived from this name when an agent's tools are built for a session, transliterated and numbered (`booking`, `booking-2`) so it is unique among the skills attached to that agent. Renaming a skill changes that slug and nothing else. _(minLen=1; maxLen=255)_
- `status` — string **(required)** _(enum: `draft`, `active`)_
- `access` — SkillAccess **(required)** — Who can use and edit the skill. Usage for private skills is limited to the creator, editors and viewers; company skills are attachable by anyone in the organization.
  - `visibility` — string _(enum: `private`, `company`)_
  - `editors` — array — Users and groups that may edit the draft. The creator always has edit access.
    - _array of_ `SkillGrantPrincipal`
      - _oneOf_ — exactly one of:
        - **`userId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`groupId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `viewers` — array — Users and groups the skill is shared with: they may see and attach it, but not edit. Redundant under company visibility.
    - _array of_ `SkillGrantPrincipal`
      - _oneOf_ — exactly one of:
        - **`userId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`groupId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
- `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
- `latestVersion` — number — Latest published version number, resolved by agent attachments that omit a version pin. Absent while the skill is still a draft. _(min=1)_

**`SkillAccess`**

_Who can use and edit the skill. Usage for private skills is limited to the creator, editors and viewers; company skills are attachable by anyone in the organization._

- `visibility` — string _(enum: `private`, `company`)_
- `editors` — array — Users and groups that may edit the draft. The creator always has edit access.
  - _array of_ `SkillGrantPrincipal`
    - _oneOf_ — exactly one of:
      - **`userId`**
        - `userId` — string **(required)** _(minLen=12; maxLen=12)_
      - **`groupId`**
        - `groupId` — string **(required)**
- `viewers` — array — Users and groups the skill is shared with: they may see and attach it, but not edit. Redundant under company visibility.
  - _array of_ `SkillGrantPrincipal`
    - _oneOf_ — exactly one of:
      - **`userId`**
        - `userId` — string **(required)** _(minLen=12; maxLen=12)_
      - **`groupId`**
        - `groupId` — string **(required)**

**`SkillDefinitionSnapshot`**

_Immutable skill definition snapshot captured at publish time. Its `files` reference the exact content the version was published with, so restoring is lossless._

- `description` — string **(required)** — What the skill does and when to use it. Loaded at discovery time for progressive disclosure. _(maxLen=1024)_
- `content` — string **(required)** — The SKILL.md markdown body: the instructions themselves. Progressive disclosure: loaded when the skill is activated. Keep it concise and move detail into bundled files the agent reads on demand. _(minLen=1; maxLen=204800)_
- `tools` — array — Tools the skill's instructions depend on, merged into the agent's toolset while the skill is active.
  - _array of_ `SkillTool`
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
      - **`webSearch`**
        - `webSearch` — AgentWebSearchCapability **(required)** — Model-native web search. The provider tool is selected from the agent model.
          - _(nesting depth limit — see `AgentWebSearchCapability` in the Schemas appendix)_
      - **`webFetch`**
        - `webFetch` — AgentWebFetchCapability **(required)** — Server-side fetch of a URL, returning its readable text/markdown to the model.
          - _(nesting depth limit — see `AgentWebFetchCapability` in the Schemas appendix)_
      - **`transfer`**
        - `transfer` — AgentTransferCapability **(required)** — Transfer the call to a PBX destination. Honoured on the voice channel. One capability entry per transfer target.
          - _(nesting depth limit — see `AgentTransferCapability` in the Schemas appendix)_
      - **`hangup`**
        - `hangup` — AgentHangupCapability **(required)** — Let the model end the call. Honoured on the voice channel.
          - _(nesting depth limit — see `AgentHangupCapability` in the Schemas appendix)_
      - **`wait`**
        - `wait` — AgentWaitCapability **(required)** — Let the model hold the call while it works (e.g. a lookup), keeping the caller on the line. Honoured on the voice channel.
          - _(nesting depth limit — see `AgentWaitCapability` in the Schemas appendix)_
- `files` — array — Files bundled with the skill: references to uploaded content (UploadSkillFile) placed at bundle paths. The list is the complete bundle — a file left out of an update is no longer part of the skill, and changing a file means uploading a new one and referencing it at the same path. _(maxItems=200)_
  - _array of_ `SkillFile`
    - `id` — string **(required)** — Uploaded content this entry points at, as returned by UploadSkillFile. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
    - `path` — string **(required)** — Path the file is materialised at inside the bundle. _(pattern=^[a-zA-Z0-9](?:[a-zA-Z0-9._/-]*[a-zA-Z0-9_])?$; minLen=1; maxLen=1024)_
    - `name` — string — File name shown to the user. Defaults to the name recorded at upload. _(minLen=1; maxLen=255)_
    - `size` — number — Size in bytes. Ignored on input; the service reports the size of the stored content.
    - `executable` — boolean — Marks the file executable when it is materialised in the sandbox. Set per skill, not per upload.
- `name` — string **(required)** — The skill's name as people see it: free text, editable, not unique. The identifier the model loads a skill by is not stored — it is a slug derived from this name when an agent's tools are built for a session, transliterated and numbered (`booking`, `booking-2`) so it is unique among the skills attached to that agent. Renaming a skill changes that slug and nothing else. _(minLen=1; maxLen=255)_

**`SkillFile`**

_A file bundled with a skill: a reference to immutable uploaded content, plus the path it is materialised at._

- `id` — string **(required)** — Uploaded content this entry points at, as returned by UploadSkillFile. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
- `path` — string **(required)** — Path the file is materialised at inside the bundle. _(pattern=^[a-zA-Z0-9](?:[a-zA-Z0-9._/-]*[a-zA-Z0-9_])?$; minLen=1; maxLen=1024)_
- `name` — string — File name shown to the user. Defaults to the name recorded at upload. _(minLen=1; maxLen=255)_
- `size` — number — Size in bytes. Ignored on input; the service reports the size of the stored content.
- `executable` — boolean — Marks the file executable when it is materialised in the sandbox. Set per skill, not per upload.

**`SkillGrantPrincipal`**

_A user or group granted edit access to the skill draft._

- _oneOf_ — exactly one of:
  - **`userId`**
    - `userId` — string **(required)** _(minLen=12; maxLen=12)_
  - **`groupId`**
    - `groupId` — string **(required)**

**`SkillInfo`**

_Summary entry returned by ListSkills._

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
- `name` — string **(required)** — The skill's name as people see it: free text, editable, not unique. The identifier the model loads a skill by is not stored — it is a slug derived from this name when an agent's tools are built for a session, transliterated and numbered (`booking`, `booking-2`) so it is unique among the skills attached to that agent. Renaming a skill changes that slug and nothing else. _(minLen=1; maxLen=255)_
- `description` — string **(required)** — What the skill does and when to use it. Loaded at discovery time for progressive disclosure. _(maxLen=1024)_
- `status` — string **(required)** _(enum: `draft`, `active`)_
- `access` — SkillAccess **(required)** — Who can use and edit the skill. Usage for private skills is limited to the creator, editors and viewers; company skills are attachable by anyone in the organization.
  - `visibility` — string _(enum: `private`, `company`)_
  - `editors` — array — Users and groups that may edit the draft. The creator always has edit access.
    - _array of_ `SkillGrantPrincipal`
      - _oneOf_ — exactly one of:
        - **`userId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`groupId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `viewers` — array — Users and groups the skill is shared with: they may see and attach it, but not edit. Redundant under company visibility.
    - _array of_ `SkillGrantPrincipal`
      - _oneOf_ — exactly one of:
        - **`userId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`groupId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
- `latestVersion` — number — Published skill version number. Monotonic within a skill's version history, starting at 1. _(min=1)_
- `owned` — boolean — True when the calling user is the creator.
- `editable` — boolean — True when the calling user may edit the draft.

**`SkillListScope`**

- string _(enum: `mine`, `company`, `all`, `everyone`)_

**`SkillStatus`**

- string _(enum: `draft`, `active`)_

**`SkillTool`**

_A tool a skill depends on. Uses the same references an agent uses in `engine.ai.capabilities`, so a tool is configured identically whether it hangs off an agent or off a skill._

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

**`SkillVersion`**

- `skillId` — string **(required)** _(minLen=12; maxLen=12)_
- `version` — number **(required)** — Published skill version number. Monotonic within a skill's version history, starting at 1. _(min=1)_
- `changelog` — string — What changed in this version, provided at publish time. _(minLen=1; maxLen=500)_
- `definition` — SkillDefinitionSnapshot **(required)** — Immutable skill definition snapshot captured at publish time. Its `files` reference the exact content the version was published with, so restoring is lossless.
  - `description` — string **(required)** — What the skill does and when to use it. Loaded at discovery time for progressive disclosure. _(maxLen=1024)_
  - `content` — string **(required)** — The SKILL.md markdown body: the instructions themselves. Progressive disclosure: loaded when the skill is activated. Keep it concise and move detail into bundled files the agent reads on demand. _(minLen=1; maxLen=204800)_
  - `tools` — array — Tools the skill's instructions depend on, merged into the agent's toolset while the skill is active.
    - _array of_ `SkillTool`
      - _oneOf_ — exactly one of:
        - **`tool`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`connector`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`kb`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`webSearch`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`webFetch`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`transfer`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`hangup`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`wait`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `files` — array — Files bundled with the skill: references to uploaded content (UploadSkillFile) placed at bundle paths. The list is the complete bundle — a file left out of an update is no longer part of the skill, and changing a file means uploading a new one and referencing it at the same path. _(maxItems=200)_
    - _array of_ `SkillFile`
      - `id` — string **(required)** — Uploaded content this entry points at, as returned by UploadSkillFile. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
      - `path` — string **(required)** — Path the file is materialised at inside the bundle. _(pattern=^[a-zA-Z0-9](?:[a-zA-Z0-9._/-]*[a-zA-Z0-9_])?$; minLen=1; maxLen=1024)_
      - `name` — string — File name shown to the user. Defaults to the name recorded at upload. _(minLen=1; maxLen=255)_
      - `size` — number — Size in bytes. Ignored on input; the service reports the size of the stored content.
      - `executable` — boolean — Marks the file executable when it is materialised in the sandbox. Set per skill, not per upload.
  - `name` — string **(required)** — The skill's name as people see it: free text, editable, not unique. The identifier the model loads a skill by is not stored — it is a slug derived from this name when an agent's tools are built for a session, transliterated and numbered (`booking`, `booking-2`) so it is unique among the skills attached to that agent. Renaming a skill changes that slug and nothing else. _(minLen=1; maxLen=255)_
- `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
  - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
  - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
  - `name` — string — Human readable name of the actor at the time of the action.

**`SkillVersionChange`**

- `path` — string **(required)** — JSON pointer of the changed field within the skill definition, e.g. '/content'.
- `before` — any — Value before the change (absent when the field was added).
- `after` — any — Value after the change (absent when the field was removed).

**`SkillVersionInfo`**

_Version list entry without the full definition snapshot._

- `skillId` — string **(required)** _(minLen=12; maxLen=12)_
- `version` — number **(required)** — Published skill version number. Monotonic within a skill's version history, starting at 1. _(min=1)_
- `changelog` — string — Human-readable description of what changed in a published version. _(minLen=1; maxLen=500)_
- `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
  - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
  - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
  - `name` — string — Human readable name of the actor at the time of the action.
- `latest` — boolean — True when this version is the skill's latestVersion.

**`SkillVisibility`**

- string _(enum: `private`, `company`)_

**`UnsupportedMediaTypeExceptionResponseContent`**

_The request payload has a content type or format the service does not accept._

- `message` — string **(required)**

**`UpdateSkillRequestContent`**

- `description` — string **(required)** — What the skill does and when to use it. Loaded at discovery time for progressive disclosure. _(maxLen=1024)_
- `content` — string **(required)** — The SKILL.md markdown body: the instructions themselves. Progressive disclosure: loaded when the skill is activated. Keep it concise and move detail into bundled files the agent reads on demand. _(minLen=1; maxLen=204800)_
- `tools` — array — Tools the skill's instructions depend on, merged into the agent's toolset while the skill is active.
  - _array of_ `SkillTool`
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
      - **`webSearch`**
        - `webSearch` — AgentWebSearchCapability **(required)** — Model-native web search. The provider tool is selected from the agent model.
          - _(nesting depth limit — see `AgentWebSearchCapability` in the Schemas appendix)_
      - **`webFetch`**
        - `webFetch` — AgentWebFetchCapability **(required)** — Server-side fetch of a URL, returning its readable text/markdown to the model.
          - _(nesting depth limit — see `AgentWebFetchCapability` in the Schemas appendix)_
      - **`transfer`**
        - `transfer` — AgentTransferCapability **(required)** — Transfer the call to a PBX destination. Honoured on the voice channel. One capability entry per transfer target.
          - _(nesting depth limit — see `AgentTransferCapability` in the Schemas appendix)_
      - **`hangup`**
        - `hangup` — AgentHangupCapability **(required)** — Let the model end the call. Honoured on the voice channel.
          - _(nesting depth limit — see `AgentHangupCapability` in the Schemas appendix)_
      - **`wait`**
        - `wait` — AgentWaitCapability **(required)** — Let the model hold the call while it works (e.g. a lookup), keeping the caller on the line. Honoured on the voice channel.
          - _(nesting depth limit — see `AgentWaitCapability` in the Schemas appendix)_
- `files` — array — Files bundled with the skill: references to uploaded content (UploadSkillFile) placed at bundle paths. The list is the complete bundle — a file left out of an update is no longer part of the skill, and changing a file means uploading a new one and referencing it at the same path. _(maxItems=200)_
  - _array of_ `SkillFile`
    - `id` — string **(required)** — Uploaded content this entry points at, as returned by UploadSkillFile. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
    - `path` — string **(required)** — Path the file is materialised at inside the bundle. _(pattern=^[a-zA-Z0-9](?:[a-zA-Z0-9._/-]*[a-zA-Z0-9_])?$; minLen=1; maxLen=1024)_
    - `name` — string — File name shown to the user. Defaults to the name recorded at upload. _(minLen=1; maxLen=255)_
    - `size` — number — Size in bytes. Ignored on input; the service reports the size of the stored content.
    - `executable` — boolean — Marks the file executable when it is materialised in the sandbox. Set per skill, not per upload.
- `name` — string **(required)** — The skill's name as people see it: free text, editable, not unique. The identifier the model loads a skill by is not stored — it is a slug derived from this name when an agent's tools are built for a session, transliterated and numbered (`booking`, `booking-2`) so it is unique among the skills attached to that agent. Renaming a skill changes that slug and nothing else. _(minLen=1; maxLen=255)_
- `revision` — number **(required)** — Draft revision this update is based on (optimistic locking). When it does not match the current revision, RevisionConflictException is returned.
- `access` — SkillAccess — Who can use and edit the skill. Usage for private skills is limited to the creator, editors and viewers; company skills are attachable by anyone in the organization.
  - `visibility` — string _(enum: `private`, `company`)_
  - `editors` — array — Users and groups that may edit the draft. The creator always has edit access.
    - _array of_ `SkillGrantPrincipal`
      - _oneOf_ — exactly one of:
        - **`userId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`groupId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `viewers` — array — Users and groups the skill is shared with: they may see and attach it, but not edit. Redundant under company visibility.
    - _array of_ `SkillGrantPrincipal`
      - _oneOf_ — exactly one of:
        - **`userId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`groupId`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_

**`UpdateSkillResponseContent`**

- `skill` — Skill **(required)** — The complete, versionable configuration of a skill, including the references to its bundled files.
  - `description` — string **(required)** — What the skill does and when to use it. Loaded at discovery time for progressive disclosure. _(maxLen=1024)_
  - `content` — string **(required)** — The SKILL.md markdown body: the instructions themselves. Progressive disclosure: loaded when the skill is activated. Keep it concise and move detail into bundled files the agent reads on demand. _(minLen=1; maxLen=204800)_
  - `tools` — array — Tools the skill's instructions depend on, merged into the agent's toolset while the skill is active.
    - _array of_ `SkillTool`
      - _oneOf_ — exactly one of:
        - **`tool`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`connector`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`kb`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`webSearch`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`webFetch`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`transfer`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`hangup`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`wait`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `files` — array — Files bundled with the skill: references to uploaded content (UploadSkillFile) placed at bundle paths. The list is the complete bundle — a file left out of an update is no longer part of the skill, and changing a file means uploading a new one and referencing it at the same path. _(maxItems=200)_
    - _array of_ `SkillFile`
      - `id` — string **(required)** — Uploaded content this entry points at, as returned by UploadSkillFile. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
      - `path` — string **(required)** — Path the file is materialised at inside the bundle. _(pattern=^[a-zA-Z0-9](?:[a-zA-Z0-9._/-]*[a-zA-Z0-9_])?$; minLen=1; maxLen=1024)_
      - `name` — string — File name shown to the user. Defaults to the name recorded at upload. _(minLen=1; maxLen=255)_
      - `size` — number — Size in bytes. Ignored on input; the service reports the size of the stored content.
      - `executable` — boolean — Marks the file executable when it is materialised in the sandbox. Set per skill, not per upload.
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
  - `name` — string **(required)** — The skill's name as people see it: free text, editable, not unique. The identifier the model loads a skill by is not stored — it is a slug derived from this name when an agent's tools are built for a session, transliterated and numbered (`booking`, `booking-2`) so it is unique among the skills attached to that agent. Renaming a skill changes that slug and nothing else. _(minLen=1; maxLen=255)_
  - `status` — string **(required)** _(enum: `draft`, `active`)_
  - `access` — SkillAccess **(required)** — Who can use and edit the skill. Usage for private skills is limited to the creator, editors and viewers; company skills are attachable by anyone in the organization.
    - `visibility` — string _(enum: `private`, `company`)_
    - `editors` — array — Users and groups that may edit the draft. The creator always has edit access.
      - _array of_ `SkillGrantPrincipal`
        - _(nesting depth limit — see `SkillGrantPrincipal` in the Schemas appendix)_
    - `viewers` — array — Users and groups the skill is shared with: they may see and attach it, but not edit. Redundant under company visibility.
      - _array of_ `SkillGrantPrincipal`
        - _(nesting depth limit — see `SkillGrantPrincipal` in the Schemas appendix)_
  - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
  - `latestVersion` — number — Latest published version number, resolved by agent attachments that omit a version pin. Absent while the skill is still a draft. _(min=1)_

**`UploadSkillFileRequestContent`**

- `name` — string **(required)** — File name shown to the user, e.g. 'api-reference.md'. Used as the download file name and as the default `name` of a skill file referencing this id. _(minLen=1; maxLen=255)_
- `size` — number **(required)** — Declared size in bytes. Used for quota checks before the presigned URL is issued.
- `contentType` — string — MIME type the client must send as the Content-Type header on PUT, e.g. 'application/pdf'.

**`UploadSkillFileResponseContent`**

- `fileId` — string **(required)** — Identifier of the registered file. Reference it in the `files` of CreateSkill / UpdateSkill, and pass it to DownloadSkillFile. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
- `uploadUrl` — string **(required)** — Presigned URL to PUT the file content to. Short-lived: upload the bytes right away rather than storing the URL.
- `expiresAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

**`WebSearchContextSize`**

_Search depth/context hint, mapped per provider._

- string _(enum: `low`, `medium`, `high`)_

**`WebSearchUserLocation`**

- `country` — string — ISO 3166-1 alpha-2 country code, e.g. 'US'.
- `region` — string
- `city` — string
- `timezone` — string — IANA timezone, e.g. 'Europe/Rome'.

</details>
