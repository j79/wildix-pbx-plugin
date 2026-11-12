## Wilma Assistant API 🆕

_OpenAPI: Wilma Assistant Service — version v2_

**Servers**

- `https://api.wilma.wildix.com` — Production
- `https://api-stable.wilma.wildix.com` — Stable
- `https://api-stage.wilma.wildix.com` — Stage

### Agents

#### `GET` `/v2/assistant/agents/items/{agentId}`

Gets the end-user view of one agent: its name, picture and the assistant presentation a client draws
    before the first turn (welcome message, quick commands, composer placeholder). This is the only agent
    read an end user needs — instructions, capabilities and access rules stay in wilma-agents, which serves
    the administrator.

    Authorization is optional, and what it changes is reach rather than shape. An authenticated caller
    resolves any agent they are granted. An anonymous caller resolves only an agent whose access visibility
    is `public`, and must name the tenant with `company` since the request carries none. Anything else
    answers NotFound rather than Forbidden, so an anonymous probe cannot use this operation to discover
    which agent ids exist.

- operationId: `GetAgent`
- **Scopes**: `wilma-assistant:GetAgent`, `wilma-assistant:read`
- **Parameters**
  - `agentId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string — The tenant the agent belongs to. Required when the call is anonymous, since there is no token to read it from; otherwise the unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The unique identifier of the user when a service or tenant token is used. Ignored on anonymous calls. _(minLen=12; maxLen=12)_
- **Response 200** (`GetAgentResponseContent`)
  - `agent` — AgentInfo **(required)** — What a client needs to render an agent, and nothing more: AgentInfo is the end-user view of an agent, served by the channel runtimes (e.g. GetAgent / GetSettings on wilma-assistant) to callers who must not see instructions, capabilities or access rules. Everything here is safe to show to whoever can use the agent.
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
- Errors: `400`, `403`, `404`

### Attachments

#### `POST` `/v2/assistant/attachments`

Registers an input attachment and returns a short-lived presigned PUT URL for its content.
    Upload the bytes to the URL, then pass the returned `attachmentId` in the `attachments` list
    of StartSession or ContinueSession. Attachments carry no session reference and can be uploaded
    before a session exists; content type, size and preview are recorded from the uploaded bytes,
    and the content becomes downloadable once the PUT completes.

- operationId: `UploadAttachment`
- **Scopes**: `wilma-assistant:UploadAttachment`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The user the attachment belongs to. Optional: identifies the user when a service or tenant token is used; when omitted the request is not scoped to a specific user. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `UploadAttachmentRequestContent`) **(required)**
  - `name` — string **(required)** — Filename shown to the user, e.g. 'quarterly-report.pdf'. _(minLen=1; maxLen=255)_
- **Response 200** (`UploadAttachmentResponseContent`)
  - `attachmentId` — string **(required)** — Identifier of the registered attachment. Pass it in the `attachments` list of StartSession or ContinueSession, and to the other Attachments operations. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
  - `uploadUrl` — string **(required)** — Presigned URL to PUT the attachment content to. Short-lived: upload the bytes right away rather than storing the URL.
- Errors: `400`, `403`

#### `GET` `/v2/assistant/attachments/items/{attachmentId}`

Gets the metadata of a single input attachment.

- operationId: `GetAttachment`
- **Scopes**: `wilma-assistant:GetAttachment`, `wilma-assistant:read`
- **Parameters**
  - `attachmentId` (path) — string **(required)** — Nano-id attachment identifier (12 characters). _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The user the attachment belongs to. Optional: identifies the user when a service or tenant token is used; when omitted the request is not scoped to a specific user. _(minLen=12; maxLen=12)_
- **Response 200** (`GetAttachmentResponseContent`)
  - `attachment` — Attachment **(required)** — An input file supplied with session input and included with a user message. Content lives in object storage; download via the owning channel's Attachments API. `contentType`, `size` and `thumbnailUrl` describe the stored content and are therefore absent until the upload has completed.
    - `id` — string **(required)** — Nano-id attachment identifier (12 characters). _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
    - `name` — string **(required)** — Filename shown to the user. Characters storage cannot represent are replaced with underscores. _(minLen=1; maxLen=255)_
    - `contentType` — string — MIME type recorded by storage from the uploaded content, e.g. 'application/pdf'. Absent until the upload completes.
    - `size` — number — Size in bytes recorded by storage from the uploaded content. Absent until the upload completes.
    - `thumbnailUrl` — string — URL of a generated preview image, for rendering a thumbnail without downloading the file. Best-effort: absent until the upload completes, and for content no preview can be generated from.
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- Errors: `400`, `403`, `404`

#### `DELETE` `/v2/assistant/attachments/items/{attachmentId}`

Deletes an attachment and its content.

- operationId: `DeleteAttachment`
- **Scopes**: `wilma-assistant:DeleteAttachment`
- **Parameters**
  - `attachmentId` (path) — string **(required)** — Nano-id attachment identifier (12 characters). _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The user the attachment belongs to. Optional: identifies the user when a service or tenant token is used; when omitted the request is not scoped to a specific user. _(minLen=12; maxLen=12)_
- Errors: `400`, `403`

#### `GET` `/v2/assistant/attachments/items/{attachmentId}/download`

Returns a short-lived presigned URL to download an attachment's content.

- operationId: `DownloadAttachment`
- **Scopes**: `wilma-assistant:DownloadAttachment`, `wilma-assistant:read`
- **Parameters**
  - `attachmentId` (path) — string **(required)** — Nano-id attachment identifier (12 characters). _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The user the attachment belongs to. Optional: identifies the user when a service or tenant token is used; when omitted the request is not scoped to a specific user. _(minLen=12; maxLen=12)_
- **Response 200** (`DownloadAttachmentResponseContent`)
  - `url` — string **(required)** — Presigned download URL. Short-lived: fetch the content right away rather than storing the URL.
  - `attachment` — Attachment **(required)** — An input file supplied with session input and included with a user message. Content lives in object storage; download via the owning channel's Attachments API. `contentType`, `size` and `thumbnailUrl` describe the stored content and are therefore absent until the upload has completed.
    - `id` — string **(required)** — Nano-id attachment identifier (12 characters). _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
    - `name` — string **(required)** — Filename shown to the user. Characters storage cannot represent are replaced with underscores. _(minLen=1; maxLen=255)_
    - `contentType` — string — MIME type recorded by storage from the uploaded content, e.g. 'application/pdf'. Absent until the upload completes.
    - `size` — number — Size in bytes recorded by storage from the uploaded content. Absent until the upload completes.
    - `thumbnailUrl` — string — URL of a generated preview image, for rendering a thumbnail without downloading the file. Best-effort: absent until the upload completes, and for content no preview can be generated from.
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- Errors: `400`, `403`, `404`

### Connectors

#### `GET` `/v2/assistant/connectors`

> ⚠️ Route marquée `deprecated` dans la spécification publiée.

Lists the connectors the current user can use in the assistant: every instance the company
    configured whose definition this deployment can execute, one entry per instance. Each entry
    says whether the connector needs the user's own authorization, whether the user has
    connected it yet, and whether it is enabled for them. The same list travels in GetSettings
    as `connectors`, next to the agents whose `connectorIds` select from it, so an assistant UI
    needs no separate call; this operation remains for a client that wants the list alone.
    Connect a not-yet-connected `user` connector via AuthorizeConnector.

- operationId: `ListConnectors`
- **Scopes**: `wilma-assistant:ListConnectors`, `wilma-assistant:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The unique identifier of the user when a service or tenant token is used. _(minLen=12; maxLen=12)_
- **Response 200** (`ListConnectorsResponseContent`)
  - `connectors` — array **(required)**
    - _array of_ `AvailableConnector`
      - `id` — string **(required)** — Connector instance id — the id an agent's capabilities and the user's `disabled` preference refer to. For an MCP server, the id of the Tool that registers it. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `key` — string **(required)** — Connector definition key, e.g. `salesforce`. Several instances may share one. For an MCP server, its provider key (`mcp_…`), which is also what AuthorizeConnector takes. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
      - `kind` — string — The kind of thing an AvailableConnector entry stands for. _(enum: `connector`, `mcp_server`)_
      - `grant` — union **(required)** — Coarse permission grant for a configured connector. The service computes the effective, server-enforced tool set by filtering the pinned definition's tools with this grant (using each tool's `ConnectorToolAccess`), and requests only the scopes the grant implies at connection time.
        - _oneOf_ — exactly one of:
          - **`read`**
            - `read` — ConnectorGrantRead **(required)** — Marker: grant every READ tool.
          - **`readWrite`**
            - `readWrite` — ConnectorGrantReadWrite **(required)** — Marker: grant every READ and WRITE tool.
          - **`all`**
            - `all` — ConnectorGrantAll **(required)** — Marker: grant every tool, including DESTRUCTIVE.
          - **`tools`**
            - `tools` — array **(required)** — Advanced: an explicit allowlist of tool ids, regardless of access class.
              - _array of_ `string`
      - `title` — string **(required)**
      - `icon` — string
      - `provider` — string **(required)** — Provider the connector authenticates against, e.g. `salesforce`. A user's consent is per provider, so connecting one instance connects every instance on the same provider.
      - `mode` — string **(required)** — Supported credential resolution mode. Mirrors wilma-secrets `ConnectionType`. _(enum: `shared`, `user`)_
      - `authorization` — string **(required)** — The current user's authorization status for a connector. Drives the Connect button: the connector is usable when NOT_REQUIRED or CONNECTED, and prompts the user to connect when NOT_CONNECTED or NEEDS_RECONNECT. _(enum: `not_required`, `not_connected`, `connected`, `needs_reconnect`)_
      - `enabled` — boolean **(required)** — Effective enablement for this user, after applying their disabled preferences.
- Errors: `400`

#### `POST` `/v2/assistant/connectors/{key}/authorize`

Starts connecting a `user`-mode connector for the current user. Returns a connect session
    the frontend uses to run the provider's authorization flow; on success the frontend calls
    ConfirmConnectorAuthorization.

- operationId: `AuthorizeConnector`
- **Scopes**: `wilma-assistant:AuthorizeConnector`
- **Parameters**
  - `key` (path) — string **(required)** — Stable identifier of a connector definition, such as `sentry`. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `user` (query) — string _(minLen=12; maxLen=12)_
- **Response 201** (`AuthorizeConnectorResponseContent`)
  - `session` — ConnectSession **(required)** — Session handshake for interactive (OAuth) authorization, completed by the frontend through Nango. A catalogue provider's session is run by handing `sessionToken` to Nango's Connect UI. An MCP server's (`mcp_*` provider) also carries `authorizationUrl`, which the frontend opens in a popup before polling the connection: nothing reports the outcome back, so the connection is adopted on its next read and there is nothing to confirm.
    - `sessionToken` — string **(required)** — Session token the frontend uses to run the authorization flow.
    - `expiresAt` — string — Absolute expiry of the session.
    - `authorizationUrl` — string — The Nango URL that starts an MCP server's authorization. Present only for an `mcp_*` provider.
- Errors: `400`, `404`

#### `DELETE` `/v2/assistant/connectors/{key}/authorize`

Disconnects a `user`-mode connector for the current user, revoking the stored credential
    for the connector's provider. Idempotent — succeeds even if the user was not connected.
    Returns the connector with its now-disconnected state.

- operationId: `RevokeConnectorAuthorization`
- **Scopes**: `wilma-assistant:RevokeConnectorAuthorization`
- **Parameters**
  - `key` (path) — string **(required)** — Stable identifier of a connector definition, such as `sentry`. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `user` (query) — string _(minLen=12; maxLen=12)_
- **Response 200** (`RevokeConnectorAuthorizationResponseContent`)
  - `connector` — AvailableConnector **(required)** — One configured connector instance the current user can use in the assistant, with their authorization and enablement state. The catalogue lists every instance the company configured and this deployment can execute; an agent's `connectorIds` say which of them that agent calls. Backs the connectors menu and its per-connector Connect button.
    - `id` — string **(required)** — Connector instance id — the id an agent's capabilities and the user's `disabled` preference refer to. For an MCP server, the id of the Tool that registers it. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `key` — string **(required)** — Connector definition key, e.g. `salesforce`. Several instances may share one. For an MCP server, its provider key (`mcp_…`), which is also what AuthorizeConnector takes. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
    - `kind` — string — The kind of thing an AvailableConnector entry stands for. _(enum: `connector`, `mcp_server`)_
    - `grant` — union **(required)** — Coarse permission grant for a configured connector. The service computes the effective, server-enforced tool set by filtering the pinned definition's tools with this grant (using each tool's `ConnectorToolAccess`), and requests only the scopes the grant implies at connection time.
      - _oneOf_ — exactly one of:
        - **`read`**
          - `read` — ConnectorGrantRead **(required)** — Marker: grant every READ tool.
        - **`readWrite`**
          - `readWrite` — ConnectorGrantReadWrite **(required)** — Marker: grant every READ and WRITE tool.
        - **`all`**
          - `all` — ConnectorGrantAll **(required)** — Marker: grant every tool, including DESTRUCTIVE.
        - **`tools`**
          - `tools` — array **(required)** — Advanced: an explicit allowlist of tool ids, regardless of access class.
            - _array of_ `string`
    - `title` — string **(required)**
    - `icon` — string
    - `provider` — string **(required)** — Provider the connector authenticates against, e.g. `salesforce`. A user's consent is per provider, so connecting one instance connects every instance on the same provider.
    - `mode` — string **(required)** — Supported credential resolution mode. Mirrors wilma-secrets `ConnectionType`. _(enum: `shared`, `user`)_
    - `authorization` — string **(required)** — The current user's authorization status for a connector. Drives the Connect button: the connector is usable when NOT_REQUIRED or CONNECTED, and prompts the user to connect when NOT_CONNECTED or NEEDS_RECONNECT. _(enum: `not_required`, `not_connected`, `connected`, `needs_reconnect`)_
    - `enabled` — boolean **(required)** — Effective enablement for this user, after applying their disabled preferences.
- Errors: `400`, `404`

#### `POST` `/v2/assistant/connectors/{key}/authorize/complete`

Completes connecting a `user`-mode connector after the authorization flow succeeds. Pass the
    connection id the flow returned. Returns the connector with its now-connected state.

- operationId: `ConfirmConnectorAuthorization`
- **Scopes**: `wilma-assistant:ConfirmConnectorAuthorization`
- **Parameters**
  - `key` (path) — string **(required)** — Stable identifier of a connector definition, such as `sentry`. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
  - `company` (query) — string _(minLen=3; maxLen=30)_
  - `user` (query) — string _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `ConfirmConnectorAuthorizationRequestContent`) **(required)**
  - `connectionId` — string **(required)** — Connection id returned by the authorization flow. _(minLen=1; maxLen=256)_
- **Response 200** (`ConfirmConnectorAuthorizationResponseContent`)
  - `connector` — AvailableConnector **(required)** — One configured connector instance the current user can use in the assistant, with their authorization and enablement state. The catalogue lists every instance the company configured and this deployment can execute; an agent's `connectorIds` say which of them that agent calls. Backs the connectors menu and its per-connector Connect button.
    - `id` — string **(required)** — Connector instance id — the id an agent's capabilities and the user's `disabled` preference refer to. For an MCP server, the id of the Tool that registers it. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `key` — string **(required)** — Connector definition key, e.g. `salesforce`. Several instances may share one. For an MCP server, its provider key (`mcp_…`), which is also what AuthorizeConnector takes. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
    - `kind` — string — The kind of thing an AvailableConnector entry stands for. _(enum: `connector`, `mcp_server`)_
    - `grant` — union **(required)** — Coarse permission grant for a configured connector. The service computes the effective, server-enforced tool set by filtering the pinned definition's tools with this grant (using each tool's `ConnectorToolAccess`), and requests only the scopes the grant implies at connection time.
      - _oneOf_ — exactly one of:
        - **`read`**
          - `read` — ConnectorGrantRead **(required)** — Marker: grant every READ tool.
        - **`readWrite`**
          - `readWrite` — ConnectorGrantReadWrite **(required)** — Marker: grant every READ and WRITE tool.
        - **`all`**
          - `all` — ConnectorGrantAll **(required)** — Marker: grant every tool, including DESTRUCTIVE.
        - **`tools`**
          - `tools` — array **(required)** — Advanced: an explicit allowlist of tool ids, regardless of access class.
            - _array of_ `string`
    - `title` — string **(required)**
    - `icon` — string
    - `provider` — string **(required)** — Provider the connector authenticates against, e.g. `salesforce`. A user's consent is per provider, so connecting one instance connects every instance on the same provider.
    - `mode` — string **(required)** — Supported credential resolution mode. Mirrors wilma-secrets `ConnectionType`. _(enum: `shared`, `user`)_
    - `authorization` — string **(required)** — The current user's authorization status for a connector. Drives the Connect button: the connector is usable when NOT_REQUIRED or CONNECTED, and prompts the user to connect when NOT_CONNECTED or NEEDS_RECONNECT. _(enum: `not_required`, `not_connected`, `connected`, `needs_reconnect`)_
    - `enabled` — boolean **(required)** — Effective enablement for this user, after applying their disabled preferences.
- Errors: `400`, `404`

### Sessions

#### `GET` `/v2/assistant/sessions`

Lists durable assistant sessions for the authenticated owner. Hidden sessions (started by integrations) are excluded unless an explicit `visibility` filter is passed.

- operationId: `ListSessions`
- **Scopes**: `wilma-assistant:ListSessions`, `wilma-assistant:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The user the session belongs to. Optional: identifies the user when a service or tenant token is used; when omitted the session is not scoped to a specific user. _(minLen=12; maxLen=12)_
  - `agentId` (query) — string _(minLen=12; maxLen=12)_
  - `agentVersion` (query) — number — Only sessions served by this published agent version (rollout inspection). _(min=1)_
  - `status` (query) — string _(enum: `running`, `idle`, `waiting`, `stopped`, `failed`, `terminated`)_
  - `visibility` (query) — string — Only sessions with this visibility. Defaults to `listed`; pass `hidden` to inspect integration-driven sessions. _(enum: `listed`, `hidden`)_
  - `target` (query) — string — Only sessions with this exact target, e.g. `inbox://channels/ch_123` for the history of one conversation. Mutually exclusive with targetPrefix. _(minLen=1; maxLen=1024)_
  - `targetPrefix` (query) — string — Only sessions whose target starts with this prefix: a scheme for every session of one surface or integration (`si://`, `copilot://`), or a deeper path for a subtree (`si://calls/`). Mutually exclusive with target. _(minLen=1; maxLen=1024)_
  - `from` (query) — string — Only sessions created at or after this time.
  - `to` (query) — string — Only sessions created before this time.
  - `limit` (query) — number _(min=1; max=100)_
  - `cursor` (query) — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- **Response 200** (`ListSessionsResponseContent`)
  - `sessions` — array **(required)**
    - _array of_ `SessionMeta`
      - `sessionId` — string **(required)** _(minLen=1; maxLen=128)_
      - `agentId` — string _(minLen=12; maxLen=12)_
      - `traceId` — string — Opaque trace identifier generated by the tracing runtime. _(minLen=1; maxLen=128)_
      - `agentVersion` — number — Published agent version serving this session, selected at session start. _(min=1)_
      - `agentDraft` — boolean — True when the session runs the agent's mutable draft (agentDraft on StartSession).
      - `agentDraftRevision` — number — Draft revision loaded at session start when agentDraft is true; correlates a run with the exact draft state.
      - `model` — string — Effective model resolved at session start (after 'default' resolution), e.g. 'google://gemini-3-flash-preview'.
      - `skillVersions` — array — Skill versions resolved at session start, one entry per attached skill (whether pinned or resolved via the skill's alias).
        - _array of_ `SessionSkillVersion`
          - `skillId` — string **(required)** _(minLen=12; maxLen=12)_
          - `version` — number **(required)** — Published skill version number. Monotonic within a skill's version history, starting at 1. _(min=1)_
      - `visibility` — string — Whether a session shows up in the user's assistant history. Integration-driven sessions (e.g. copilot asset generation) are started `hidden` so they do not pollute the history while staying reachable by id. _(enum: `listed`, `hidden`)_
      - `target` — string — What the session belongs to, as supplied on StartSession. Present for sessions started from a client surface or integration that identified itself. _(minLen=1; maxLen=1024)_
      - `metadata` — any — Host-defined metadata supplied on StartSession, returned verbatim.
      - `status` — string **(required)** _(enum: `running`, `idle`, `waiting`, `stopped`, `failed`, `terminated`)_
      - `version` — number **(required)** — Monotonic session state revision.
      - `title` — string
      - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `eventCount` — number **(required)**
  - `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- Errors: `400`, `403`

#### `POST` `/v2/assistant/sessions`

Starts a durable assistant session and returns the event index from which the caller should stream. Services integrating with the assistant (e.g. the copilot backend) start sessions on behalf of a user with `user`, a `target` naming the resource the session is for (e.g. `copilot://sessions/{copilotSessionId}`) and — for sessions that should not appear in the user's history — `visibility: hidden`.

- operationId: `StartSession`
- **Scopes**: `wilma-assistant:StartSession`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `StartSessionRequestContent`) **(required)**
  - `user` — string — The user the session belongs to. Optional: identifies the user when a service or tenant token is used; when omitted the session is not scoped to a specific user. _(minLen=12; maxLen=12)_
  - `message` — string **(required)** _(minLen=1; maxLen=100000)_
  - `attachments` — array — Ids of input attachments to include with the initial user message, as returned by UploadAttachment. Their stored metadata is reported back on the turn's MessageReceivedEvent.
    - _array of_ `string`
  - `sessionId` — string _(minLen=1; maxLen=128)_
  - `agentId` — string _(minLen=12; maxLen=12)_
  - `agentVersion` — number — Published agent version to run. Mutually exclusive with agentDraft. When neither is set, the agent's deployment configuration selects the version. _(min=1)_
  - `agentDraft` — boolean — Run the agent's current draft (for testing). Mutually exclusive with agentVersion.
  - `options` — any — Runtime options for the session, e.g. `{model: 'google://gemini-3-flash-preview', timeZone: 'Europe/Rome'}`. `timeZone` is the IANA time zone of the person asking: the session shows every time in it, fixed at start, and falls back to the agent's when omitted. Interpreted by the runtime, so only documented keys belong here: put values the client wants back unchanged in `metadata`, and what the session belongs to in `target`.
  - `context` — array — What the client has in view and the server cannot read for itself, such as the page or the agent being edited, as `{id, type, data}` documents.
    - _array of_ `any`
  - `mentions` — array — What the user attached for the agent to read, resolved with the session user's permissions, or company-wide when the session has no user. _(maxItems=20)_
    - _array of_ `Mention`
      - _oneOf_ — exactly one of:
        - **`reference`**
          - `reference` — MentionReference **(required)** — A resource selected as agent context, identified by its canonical URI, e.g. `wilma://insights/calls/{callId}/flows/{flowIndex}`. It is read with the permissions of the session or task it is attached to; the URI grants no access by itself.
            - `uri` — string **(required)** — Canonical URI identifying one entity on the Wilma platform, e.g. 'wilma://agents/UXDT1W9fI3sj' or 'wilma://skills/aB3dE5fG7hJ9'. The path names the owning service and entity kind. Opaque to the contracts that carry it; non-Wilma schemes (records of external systems) fit the same shape. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
            - `label` — string — Display name of the mention chip. The model sees it only to name a mention that could not be read or was removed. _(maxLen=256)_
  - `tools` — array
    - _array of_ `SessionClientTool`
      - `name` — string **(required)**
      - `description` — string
      - `schema` — any **(required)**
      - `fulfilment` — string — Who produces an invocation's result. `server` tools execute inside the agent runtime. `client` tools are executed by the caller, so the turn suspends until it answers. `synthetic` tools never execute at all — they exist to put something on screen, and the runtime supplies their result itself, so the turn does not suspend. _(enum: `server`, `client`, `synthetic`)_
      - `gate` — string — Whether the turn suspends on an invocation, and for what. Orthogonal to fulfilment: a `server` tool may be gated on a user decision (an approval), and a `synthetic` tool may be ungated (render and continue) or gated (an editable draft awaiting confirmation). _(enum: `none`, `result`, `decision`)_
      - `surface` — string — Where a client should surface an invocation. Affects placement only, never behaviour. _(enum: `hidden`, `activity`, `content`)_
      - `stream` — boolean — Emit InvocationDeltaEvent for calls to this tool, so the caller can render the input as the model writes it — useful when the input carries content rather than a lookup key. Defaults to false.
      - `ack` — any — Result handed back to the model for a `synthetic` tool, typically a short instruction telling the model what the user can now see. Ignored for `client` tools.
  - `visibility` — string — Whether a session shows up in the user's assistant history. Integration-driven sessions (e.g. copilot asset generation) are started `hidden` so they do not pollute the history while staying reachable by id. _(enum: `listed`, `hidden`)_
  - `target` — string — What this session belongs to: the client surface it is started on (`inbox://channels/ch_123`) or the resource an integration starts it for (`copilot://sessions/cs_123`). Returned on SessionMeta and filterable on ListSessions, so a client can reopen the session where it came from and list a per-surface history. Opaque to the service; immutable once set. _(minLen=1; maxLen=1024)_
  - `metadata` — any — Host-defined metadata to carry with the session and read back from SessionMeta. Not indexed; use `target` for anything a list must be filtered by.
  - `personalisation` — any
  - `skills` — array
    - _array of_ `SessionSkill`
      - `name` — string **(required)**
      - `description` — string **(required)**
      - `body` — string **(required)**
  - `connectors` — SessionConnectors — Per-session connector overrides, by connector instance id. `disabled` turns connectors off for this session only; `enabled` turns back on connectors the user disabled in their settings, for this session only.
    - `disabled` — array
      - _array of_ `string`
    - `enabled` — array
      - _array of_ `string`
- **Response 202** (`StartSessionResponseContent`)
  - `sessionId` — string **(required)** _(minLen=1; maxLen=128)_
  - `startIndex` — number **(required)**
  - `traceId` — string — Trace recording the session in wilma-traces — every turn, model call and tool execution the agent ran. Read it with the wilma-traces GetTrace operation, or tail it live with StreamTrace next to the event stream `startIndex` addresses. One id for the whole session, not for this turn: the handle a later ContinueSession returns names the same trace StartSession opened, and each turn appends to it. The trace row is written once the turn's first step completes, so GetTrace may report NotFound in the moment right after this call returns. Absent when the session's trace is not the caller's to read — a session served by a Wildix built-in agent is recorded for Wildix rather than for the tenant. _(minLen=1; maxLen=128)_
- Errors: `400`, `403`, `409`, `503`

#### `GET` `/v2/assistant/sessions/items/{sessionId}`

Gets the durable state of an assistant session.

- operationId: `GetSession`
- **Scopes**: `wilma-assistant:GetSession`, `wilma-assistant:read`
- **Parameters**
  - `sessionId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The user the session belongs to. Optional: identifies the user when a service or tenant token is used; when omitted the session is not scoped to a specific user. _(minLen=12; maxLen=12)_
- **Response 200** (`GetSessionResponseContent`)
  - `meta` — SessionMeta **(required)**
    - `sessionId` — string **(required)** _(minLen=1; maxLen=128)_
    - `agentId` — string _(minLen=12; maxLen=12)_
    - `traceId` — string — Opaque trace identifier generated by the tracing runtime. _(minLen=1; maxLen=128)_
    - `agentVersion` — number — Published agent version serving this session, selected at session start. _(min=1)_
    - `agentDraft` — boolean — True when the session runs the agent's mutable draft (agentDraft on StartSession).
    - `agentDraftRevision` — number — Draft revision loaded at session start when agentDraft is true; correlates a run with the exact draft state.
    - `model` — string — Effective model resolved at session start (after 'default' resolution), e.g. 'google://gemini-3-flash-preview'.
    - `skillVersions` — array — Skill versions resolved at session start, one entry per attached skill (whether pinned or resolved via the skill's alias).
      - _array of_ `SessionSkillVersion`
        - `skillId` — string **(required)** _(minLen=12; maxLen=12)_
        - `version` — number **(required)** — Published skill version number. Monotonic within a skill's version history, starting at 1. _(min=1)_
    - `visibility` — string — Whether a session shows up in the user's assistant history. Integration-driven sessions (e.g. copilot asset generation) are started `hidden` so they do not pollute the history while staying reachable by id. _(enum: `listed`, `hidden`)_
    - `target` — string — What the session belongs to, as supplied on StartSession. Present for sessions started from a client surface or integration that identified itself. _(minLen=1; maxLen=1024)_
    - `metadata` — any — Host-defined metadata supplied on StartSession, returned verbatim.
    - `status` — string **(required)** _(enum: `running`, `idle`, `waiting`, `stopped`, `failed`, `terminated`)_
    - `version` — number **(required)** — Monotonic session state revision.
    - `title` — string
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `eventCount` — number **(required)**
  - `status` — string **(required)** _(enum: `running`, `idle`, `waiting`, `stopped`, `failed`, `terminated`)_
  - `history` — array **(required)**
    - _array of_ `any`
  - `state` — any **(required)**
  - `mentions` — array — The session's current mentions. _(maxItems=20)_
    - _array of_ `Mention`
      - _oneOf_ — exactly one of:
        - **`reference`**
          - `reference` — MentionReference **(required)** — A resource selected as agent context, identified by its canonical URI, e.g. `wilma://insights/calls/{callId}/flows/{flowIndex}`. It is read with the permissions of the session or task it is attached to; the URI grants no access by itself.
            - `uri` — string **(required)** — Canonical URI identifying one entity on the Wilma platform, e.g. 'wilma://agents/UXDT1W9fI3sj' or 'wilma://skills/aB3dE5fG7hJ9'. The path names the owning service and entity kind. Opaque to the contracts that carry it; non-Wilma schemes (records of external systems) fit the same shape. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
            - `label` — string — Display name of the mention chip. The model sees it only to name a mention that could not be read or was removed. _(maxLen=256)_
- Errors: `400`, `403`, `404`

#### `DELETE` `/v2/assistant/sessions/items/{sessionId}`

Permanently deletes a durable assistant session and its event log. Idempotent: deleting an already-deleted session succeeds. Observability data recorded in wilma-traces is unaffected.

- operationId: `DeleteSession`
- **Scopes**: `wilma-assistant:DeleteSession`
- **Parameters**
  - `sessionId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The user the session belongs to. Optional: identifies the user when a service or tenant token is used; when omitted the session is not scoped to a specific user. _(minLen=12; maxLen=12)_
- Errors: `400`, `403`, `404`

#### `GET` `/v2/assistant/sessions/items/{sessionId}/events`

Returns recorded session events as a plain JSON page, without streaming. Use this to fetch the activity of past sessions or to catch up before subscribing to StreamSessionEvents. Events of a currently running turn become visible here at turn boundaries; subscribe to StreamSessionEvents for live delivery.

- operationId: `GetSessionEvents`
- **Scopes**: `wilma-assistant:GetSessionEvents`, `wilma-assistant:read`
- **Parameters**
  - `sessionId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The user the session belongs to. Optional: identifies the user when a service or tenant token is used; when omitted the session is not scoped to a specific user. _(minLen=12; maxLen=12)_
  - `startIndex` (query) — number — Return events with `index >= startIndex`. Defaults to 0. _(min=0)_
  - `limit` (query) — number — Maximum number of events to return. Defaults to 1000. _(min=1; max=1000)_
- **Response 200** (`GetSessionEventsResponseContent`)
  - `events` — array **(required)**
    - _array of_ `AssistantSessionEvent`
      - _oneOf_ — exactly one of:
        - **`sessionStarted`**
          - `sessionStarted` — SessionStartedEvent **(required)** — Emitted once as the very first event of a session, when it is created. Confirms the session id and the agent the session is bound to.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `sessionId` — string **(required)** _(minLen=1; maxLen=128)_
            - `agentId` — string _(minLen=12; maxLen=12)_
        - **`sessionIdle`**
          - `sessionIdle` — SessionIdleEvent **(required)** — Terminal event of a successful turn: the session is idle and ready for the next turn.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
        - **`sessionStopped`**
          - `sessionStopped` — SessionStoppedEvent **(required)** — Terminal event emitted when the active turn was cancelled via the channel's stop operation.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `reason` — string **(required)** _(enum: `user`)_
        - **`sessionTerminated`**
          - `sessionTerminated` — SessionTerminatedEvent **(required)** — Terminal event emitted when the platform ended the session rather than let it continue: the session is in `terminated` status. Distinct from SessionStoppedEvent, which records a user or operator asking to stop — folding the two together would leave a refused session indistinguishable from a clean finish in every completion-rate report. On voice the call is hung up as this is emitted; on the other channels there is nothing to hang up and termination is the status alone — history is kept, and the session simply accepts no further turns.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `reason` — string **(required)** _(enum: `guardrail`)_
            - `guardrail` — string — The check whose `end` action terminated the session, when `reason` is `guardrail`. _(minLen=1; maxLen=64)_
            - `message` — string — What the caller was told before the session ended.
        - **`sessionFailed`**
          - `sessionFailed` — SessionFailedEvent **(required)** — Terminal event emitted after TurnFailedEvent: the session is in `failed` status. A new turn starts from the last consistent snapshot.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `code` — string **(required)**
            - `message` — string **(required)**
        - **`turnStarted`**
          - `turnStarted` — TurnStartedEvent **(required)** — Emitted when a turn begins executing. All subsequent events up to the matching TurnCompletedEvent/TurnFailedEvent belong to this turn.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)** — 1-based turn number within the session.
        - **`turnCompleted`**
          - `turnCompleted` — TurnCompletedEvent **(required)** — Emitted when a turn finishes successfully, with aggregate token usage for the turn. Followed by SessionIdleEvent.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `usage` — SessionUsage
              - `inputTokens` — number
              - `cachedTokens` — number — The part of `inputTokens` served from the provider's prompt cache. Absent when the provider does not report it.
              - `outputTokens` — number
              - `reasoningTokens` — number — The part of `outputTokens` spent on reasoning. Absent when the provider does not report it, or when the model does not reason.
              - `totalTokens` — number
        - **`turnFailed`**
          - `turnFailed` — TurnFailedEvent **(required)** — Emitted when a turn fails with an unrecoverable error. Followed by SessionFailedEvent.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `code` — string **(required)** — Stable machine-readable error code.
            - `message` — string **(required)**
        - **`messageReceived`**
          - `messageReceived` — MessageReceivedEvent **(required)** — Emitted right after TurnStartedEvent with the user message that triggered the turn, so a reconnecting client can render the conversation without a separate history fetch.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `message` — string **(required)**
            - `attachments` — array — Input files supplied with this message, as stored — enough to render the attachment alongside the message (name, type, size, thumbnail) without a separate Attachments call. Absent when the turn carried no files.
              - _array of_ `Attachment`
                - _(nesting depth limit — see `Attachment` in the Schemas appendix)_
        - **`messageAppended`**
          - `messageAppended` — MessageAppendedEvent **(required)** — Emitted for every assistant text token chunk. High frequency; drives live rendering of the reply.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `step` — number **(required)**
            - `delta` — string **(required)** — The new text fragment.
            - `soFar` — string **(required)** — The full assistant text accumulated so far in this step.
        - **`messageCompleted`**
          - `messageCompleted` — MessageCompletedEvent **(required)** — Emitted once per step when the assistant message text is complete.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `step` — number **(required)**
            - `text` — string **(required)**
            - `finishReason` — string **(required)** — Model finish reason for the step, e.g. `stop` or `tool-calls`.
        - **`stepStarted`**
          - `stepStarted` — StepStartedEvent **(required)** — Emitted each time the model starts a new inference step within a turn (a turn spans multiple steps when the model calls tools).
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `step` — number **(required)** — 1-based step number within the turn.
        - **`stepCompleted`**
          - `stepCompleted` — StepCompletedEvent **(required)** — Emitted when an inference step finishes, with token usage for the step when the provider reports it.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `step` — number **(required)**
            - `finishReason` — string **(required)**
            - `usage` — SessionUsage
              - `inputTokens` — number
              - `cachedTokens` — number — The part of `inputTokens` served from the provider's prompt cache. Absent when the provider does not report it.
              - `outputTokens` — number
              - `reasoningTokens` — number — The part of `outputTokens` spent on reasoning. Absent when the provider does not report it, or when the model does not reason.
              - `totalTokens` — number
        - **`reasoningDelta`**
          - `reasoningDelta` — ReasoningDeltaEvent **(required)** — Emitted for every reasoning (thinking) token chunk the model produces, when the selected model exposes reasoning. High frequency; intended for live typing indicators.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `step` — number **(required)**
            - `delta` — string **(required)** — The new reasoning fragment.
            - `soFar` — string **(required)** — The full reasoning text accumulated so far in this step, so late subscribers do not need to replay every delta.
        - **`reasoningCompleted`**
          - `reasoningCompleted` — ReasoningCompletedEvent **(required)** — Emitted once per step after the model finishes its reasoning block, carrying the complete reasoning text.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `step` — number **(required)**
            - `reasoning` — string **(required)**
        - **`invocationStarted`**
          - `invocationStarted` — InvocationStartedEvent **(required)** — Emitted when the model begins one tool invocation, before its input is complete. Every invocation starts here, regardless of how it is fulfilled or whether it suspends the turn. Carries the routing facts needed to render it — who fulfils it, whether the turn suspends, where to surface it, whether the input streams — so a client holding no tool registry (a replay, a shared session, an inspector) still renders correctly.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `step` — number **(required)**
            - `callId` — string **(required)** — Stable id of this invocation, referenced by every later event about it.
            - `toolName` — string **(required)**
            - `toolId` — string — The wilma-tools Tool backing this invocation. Absent for built-in tools, connector meta-tools and other capabilities that are not shared Tools. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
            - `toolVersion` — number — Published tool version the model was offered, when `toolId` is set. Records which input schema the invocation was written against. _(min=1)_
            - `fulfilment` — string **(required)** — Who produces an invocation's result. `server` tools execute inside the agent runtime. `client` tools are executed by the caller, so the turn suspends until it answers. `synthetic` tools never execute at all — they exist to put something on screen, and the runtime supplies their result itself, so the turn does not suspend. _(enum: `server`, `client`, `synthetic`)_
            - `gate` — string **(required)** — Whether the turn suspends on an invocation, and for what. Orthogonal to fulfilment: a `server` tool may be gated on a user decision (an approval), and a `synthetic` tool may be ungated (render and continue) or gated (an editable draft awaiting confirmation). _(enum: `none`, `result`, `decision`)_
            - `surface` — string **(required)** — Where a client should surface an invocation. Affects placement only, never behaviour. _(enum: `hidden`, `activity`, `content`)_
            - `stream` — boolean **(required)** — True when the input arrives as InvocationDeltaEvent chunks ahead of InvocationInputCompletedEvent. Opt-in per tool, so tools with small inputs cost nothing.
        - **`invocationDelta`**
          - `invocationDelta` — InvocationDeltaEvent **(required)** — Emitted for each fragment of an invocation's input as the model writes it, when the tool opted into streamed input. The payload is raw partial JSON text exactly as the model emits it; clients parse it incrementally to render an invocation whose input is itself content — a drafted email, a chart spec, a shared document — while it is being written. High frequency.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `step` — number **(required)**
            - `callId` — string **(required)**
            - `delta` — string **(required)** — The new fragment of raw JSON input text.
            - `soFar` — string **(required)** — The raw JSON input text accumulated so far in this invocation, so late subscribers need not replay every delta. Being a prefix, it is not necessarily valid JSON on its own.
        - **`invocationInputCompleted`**
          - `invocationInputCompleted` — InvocationInputCompletedEvent **(required)** — Emitted once per invocation when its input is complete and parsed. Always emitted, whether or not the input streamed.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `step` — number **(required)**
            - `callId` — string **(required)**
            - `input` — any **(required)**
        - **`invocationResult`**
          - `invocationResult` — InvocationResultEvent **(required)** — Emitted when an invocation is resolved, however that happened: a server tool finishing, a caller returning a client tool's result on resume, a person answering a question or ruling on an approval, or the runtime supplying a `synthetic` tool's result. Emitted for every invocation without exception, so replaying the log from index 0 reconstructs the same state as watching it live.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `step` — number **(required)**
            - `callId` — string **(required)** — Id of the invocation this result answers, matching an InvocationStartedEvent.
            - `toolName` — string **(required)**
            - `toolId` — string — The wilma-tools Tool that executed, echoed from InvocationStartedEvent. Absent for invocations that are not backed by a shared Tool. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
            - `toolVersion` — number — Published tool version that executed, when `toolId` is set. _(min=1)_
            - `status` — string **(required)** _(enum: `completed`, `failed`)_
            - `resolvedBy` — string **(required)** — Who supplied the result recorded by an InvocationResultEvent. _(enum: `server`, `client`, `user`)_
            - `output` — any
            - `error` — string — Present when status is `failed`.
        - **`taskStarted`**
          - `taskStarted` — TaskStartedEvent **(required)** — Emitted when the agent delegates a subtask to a task execution: the `delegate` tool or an agent-call capability. Events emitted inside the task are re-published on the session stream with `origin` set to this task, until the matching TaskCompletedEvent.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `taskId` — string **(required)** — Unique id of this task execution; referenced by `origin.taskId` of nested events.
            - `name` — string **(required)** — Task tool name, e.g. `delegate` or the name of the called agent.
            - `agentId` — string — Agent executing the task, when the task is a called or delegated agent. _(minLen=12; maxLen=12)_
            - `agentVersion` — number — Published version of the agent executing the task, resolved when the task started; absent when the task runs a draft. _(min=1)_
            - `instructions` — string **(required)** — The self-contained instructions handed to the task.
        - **`taskCompleted`**
          - `taskCompleted` — TaskCompletedEvent **(required)** — Emitted when a delegated task execution finishes, carrying its final answer as returned to the parent agent.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `taskId` — string **(required)**
            - `name` — string **(required)**
            - `output` — string **(required)**
        - **`workflowStepEntered`**
          - `workflowStepEntered` — WorkflowStepEnteredEvent **(required)** — Emitted when the workflow cursor arrives at a step, before the step runs — so every later event in the log belongs to the step most recently entered. The first is the graph's `entry` step; the last is a terminal step, which is where the session left the graph.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number — The turn the step was entered during, when it was entered inside one. Absent when the cursor moved between turns: an `action`, `message` or `variables` step needs no model call, so a chain of them can advance before the next turn begins.
            - `workflow` — string — The nested workflow (AgentWorkflow.nested) this step belongs to. Absent for a step of the main graph, which is how nesting is read off the stream — no separate enter/return events. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
            - `stepId` — string **(required)** — Identifier of a step within its workflow, unique per workflow (the main graph and each nested workflow are separate scopes). Stable and machine-facing: transitions reference it, and a result step's id is the name a caller branches on, so renaming a step's `label` never unwires the graph. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
            - `label` — string — The step's authored label, so a reader needs no copy of the agent definition to render the stream. _(minLen=1; maxLen=128)_
            - `stage` — string — The step's stage, as authored on it or inherited from upstream. Absent when the graph uses no stages. _(minLen=1; maxLen=64)_
            - `type` — string **(required)** — Which handler a step carries, reported on the session event stream (WorkflowStepEnteredEvent) and in traces. Mirrors the members of AgentWorkflowHandler and exists so a reader does not have to load the agent version snapshot to tell a stretch of conversation from a runtime action: a trace is read long after the fact, by an operator who has the session and not the definition it ran against. `conversation` is the only member that hands the turn to the model; which capability an `action` step performed is named by the invocation events that follow it. _(enum: `conversation`, `message`, `action`, `variables`, `workflow`, `result`, `end`)_
        - **`workflowTransition`**
          - `workflowTransition` — WorkflowTransitionEvent **(required)** — Emitted when a transition is taken, naming the exit and what decided it. Not emitted on a terminal step, which has no exits — a session that ended inside the graph is read from the last WorkflowStepEnteredEvent — and not emitted when a conversation step's conditions all stay false, which is the step simply continuing.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number — The turn the transition was evaluated in. Absent when the cursor moved between turns.
            - `workflow` — string — The nested workflow both steps belong to. Absent in the main graph; a transition never crosses graphs. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
            - `stepId` — string **(required)** — Step being left. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
            - `target` — string **(required)** — Step being entered. A WorkflowStepEnteredEvent for it follows. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
            - `condition` — string **(required)** — Which kind of condition took a transition, as reported on the session event stream (WorkflowTransitionEvent) and in traces. Mirrors the members of AgentWorkflowCondition: `prompt` is the only one the model decides, every other was settled by the runtime with no model call. _(enum: `always`, `prompt`, `expression`, `result`, `failure`, `fallback`)_
            - `reason` — string — The model's one-line reason for the move, as it gave it to the steering tool. Present only for `prompt` conditions.
        - **`workflowMoveRefused`**
          - `workflowMoveRefused` — WorkflowMoveRefusedEvent **(required)** — Emitted when the model asks to move somewhere the live step does not declare as an exit. The runtime refuses, names the legal exits, and the session carries on from the same step, so this is not a failure of the turn: it is the record of what callers keep reaching for and the graph does not offer. Aggregated per step, it is the shortest route to the exit a graph is missing.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `workflow` — string — The nested workflow the live step belongs to. Absent in the main graph. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
            - `stepId` — string **(required)** — The step the session stayed on. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
            - `requested` — string **(required)** — What the model asked for, verbatim — not necessarily a step that exists.
            - `reason` — string — The model's stated reason for the move it was refused.
        - **`workflowVariablesWritten`**
          - `workflowVariablesWritten` — WorkflowVariablesWrittenEvent **(required)** — Emitted when workflow variables are written: a `variables` step's assignments, or an action step capturing its result into `output`. The only record of the state `expression` conditions branch on and handlebars resolve against, so replaying the log from index 0 reconstructs the same variables the runtime had.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number — The turn the write happened in, when it happened inside one.
            - `workflow` — string — The nested workflow the writing step belongs to. Absent in the main graph. Variables are shared with the main graph either way — a nested workflow has no scope of its own. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
            - `stepId` — string **(required)** — Step that wrote them. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
            - `values` — any **(required)** — The names written and their resolved values, as a JSON object. Only what this write touched, not the whole state; a variable cleared by an empty assignment is present with an empty value.
        - **`guardrailTripped`**
          - `guardrailTripped` — GuardrailTrippedEvent **(required)** — Emitted when a check trips, including when its action is `observe` and the turn proceeds untouched — that is what makes observe mode a way to tune a guardrail against real traffic rather than a switched-off check.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `check` — string **(required)** — The check's `name` in the agent definition. _(minLen=1; maxLen=64)_
            - `preset` — string — A prebuilt check. Each preset is a platform-maintained prompt shipped in code and versioned with the platform, not a tenant row — so a support question about what a preset caught has one answer. A preset check is otherwise an ordinary AgentGuardrailCheck: its sensitivity and action are the tenant's to set, and `notes` narrows its prompt without replacing it. _(enum: `jailbreak`, `offTopic`, `abuse`, `harmful`, `selfHarm`, `pii`, `secrets`, `regulatedAdvice`)_
            - `confidence` — string **(required)** — How much confidence a verdict needs before it counts as tripped. The checker reports a confidence per check and this is the threshold against it, so raising sensitivity catches more and costs more false positives without changing the prompt or the model: `low` trips only on high confidence, `medium` on high and medium, `high` on anything but a clear pass. Defaults to MEDIUM. _(enum: `low`, `medium`, `high`)_
            - `action` — string **(required)** — The action members by name, for reporting what actually ran. Session events carry this rather than AgentGuardrailAction because an event reports a decision, not a configuration. _(enum: `observe`, `redact`, `block`, `end`)_
            - `reason` — string — The checker's own account of why it tripped. Recorded for whoever tunes the guardrail, and never shown to the caller: telling someone which check caught them is a free oracle for the next attempt.
        - **`guardrailFailed`**
          - `guardrailFailed` — GuardrailFailedEvent **(required)** — Emitted when the checker itself errored or timed out. Carries the errorMode decision, so a reader can tell a turn that was screened and found clean from one that was never screened — without this event a fail-open guardrail would be indistinguishable from a guardrail that found nothing.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
            - `errorMode` — string **(required)** — What happens when the checker itself errors or times out. OPEN lets the turn through unscreened and records GuardrailFailedEvent, so an unscreened turn is a fact in the log rather than an absence; CLOSED refuses it. Defaults to OPEN: an agent that stops answering because a small model had a bad minute is a worse and far likelier outage than the rare turn that goes unscreened. Background tasks, where nobody is waiting and a retry is free, are the case for CLOSED. _(enum: `open`, `closed`)_
            - `proceeded` — boolean **(required)** — True when the turn was allowed through unscreened (`errorMode: open`), false when it was refused.
            - `reason` — string — Why the checker failed — a timeout, a provider error.
        - **`sandboxStarted`**
          - `sandboxStarted` — SandboxStartedEvent **(required)** — Emitted when the turn is attached to its sandbox, the first time a sandbox-backed tool is used in the turn. A session reuses one sandbox across turns whenever possible.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `sandboxId` — string **(required)** — Provider-side sandbox id, stable while the sandbox is reused across turns.
            - `resumed` — boolean **(required)** — True when an existing sandbox from a previous turn was reattached; false when a fresh sandbox was created.
        - **`sandboxFailed`**
          - `sandboxFailed` — SandboxFailedEvent **(required)** — Emitted when acquiring the sandbox fails; the turn then fails with the same cause. Provides sandbox-level observability distinct from the generic TurnFailedEvent.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `message` — string **(required)**
        - **`artifactShared`**
          - `artifactShared` — ArtifactSharedEvent **(required)** — Emitted when the agent shares an artifact via the `share_artifact` tool, after the revision has been uploaded. Carries the file list and card metadata; the viewer reads content URLs and sharing from the wilma-artifacts service. Sharing the same artifact again publishes a new `revision` under the same `artifactId` and emits this event again.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `artifactId` — string **(required)** — Id of the registered artifact; fetch it via wilma-artifacts (GetArtifact, GetArtifactContentUrl, DownloadArtifact). _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
            - `title` — string **(required)** — Human-readable title shown to the user.
            - `description` — string — One-line summary shown under the title.
            - `name` — string — Download filename shown to the user. _(minLen=1; maxLen=1024)_
            - `kind` — string **(required)** — Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest. _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_
            - `files` — array **(required)** — Files in this revision, with their paths, sizes and MIME types. _(minItems=1; maxItems=500)_
              - _array of_ `ArtifactFile`
                - _(nesting depth limit — see `ArtifactFile` in the Schemas appendix)_
            - `entry` — string — Path of the file the viewer opens first. When omitted, the first file in files is opened. _(minLen=1; maxLen=1024)_
            - `revision` — number — Revision this event published: 1 for a new artifact, higher when the agent republished it in place.
            - `path` — string — Sandbox path the artifact was shared from: the file, or the folder a bundle's paths are relative to, e.g. `/workspace/report.md` or `/workspace/site`.
            - `callId` — string — Id of the `share_artifact` tool call that produced the artifact.
        - **`compactionStarted`**
          - `compactionStarted` — CompactionStartedEvent **(required)** — Emitted before a turn when the conversation history exceeds the model context budget and is being summarized. The turn starts after CompactionCompletedEvent.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
        - **`compactionCompleted`**
          - `compactionCompleted` — CompactionCompletedEvent **(required)** — Emitted when history compaction finishes and the turn proceeds with the summarized history.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)**
        - **`steerReceived`**
          - `steerReceived` — SteerReceivedEvent **(required)** — Emitted when a steer request is accepted for the turn already running, before it reaches the model. A turn can therefore carry more than one user message; build transcripts from event order, not from turn structure. This is the only record of the steering text: a turn the steer was promoted into starts with TurnStartedEvent but emits no MessageReceivedEvent, so the message is never recorded twice.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)** — The turn the steer was accepted for.
            - `message` — string **(required)** _(minLen=1; maxLen=100000)_
            - `attachments` — array — Input files supplied with the steering message, as stored. Absent when it carried no files.
              - _array of_ `Attachment`
                - _(nesting depth limit — see `Attachment` in the Schemas appendix)_
        - **`steerApplied`**
          - `steerApplied` — SteerAppliedEvent **(required)** — Emitted when an accepted steer has reached the model, naming the turn and step boundary where it took effect. The gap between SteerReceivedEvent and this event is user-visible, so a client can show the steering message as pending until it lands. A steer never interrupts a tool call that is already running. `turn` differs from the SteerReceivedEvent's `turn` when the steer was promoted: the running turn finished before a boundary arrived, so the message became the input of the following turn.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `turn` — number **(required)** — The turn the steering message was injected into — the following turn when it was promoted.
            - `step` — number **(required)** — The step the steering message was injected ahead of.
        - **`inputRequested`**
          - `inputRequested` — InputRequestedEvent **(required)** — Emitted when the turn cannot proceed without the caller: client-fulfilled tools, `ask_question`, or approval-gated tools. Each request references an invocation the stream has already announced — this event routes, it does not introduce calls. Answer through the channel's resume operation using the same `pendingId`; each answered invocation then emits its own InvocationResultEvent. Followed by SessionWaitingEvent.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `pendingId` — string **(required)**
            - `requests` — array **(required)**
              - _array of_ `SessionPendingInput`
                - _(nesting depth limit — see `SessionPendingInput` in the Schemas appendix)_
        - **`sessionWaiting`**
          - `sessionWaiting` — SessionWaitingEvent **(required)** — Terminal event of a turn that paused for caller input. The session stays in `waiting` status until resumed with the `pendingId`.
            - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
            - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
            - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
              - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
              - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
            - `pendingId` — string **(required)**
  - `nextStartIndex` — number — Present when more events exist; pass it as `startIndex` of the next call.
- Errors: `400`, `403`, `404`

#### `GET` `/v2/assistant/sessions/items/{sessionId}/events/stream`

Replays and tails session events as Server-Sent Events (`text/event-stream`). Each frame carries one AssistantSessionEvent: `id:` is the event index, `event:` is the union member name, and `data:` is the JSON document of the union value. Reconnect by passing the last seen index + 1 as `startIndex`. The stream ends after a terminal event (idle / waiting / stopped / failed) of the tailed turn; for finished sessions the recorded events are replayed and the stream closes.

- operationId: `StreamSessionEvents`
- **Scopes**: `wilma-assistant:StreamSessionEvents`, `wilma-assistant:read`
- **Parameters**
  - `sessionId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The user the session belongs to. Optional: identifies the user when a service or tenant token is used; when omitted the session is not scoped to a specific user. _(minLen=12; maxLen=12)_
  - `startIndex` (query) — number — Replay recorded events with `index >= startIndex` before tailing live ones. Defaults to 0. _(min=0)_
- **Response 200** (`StreamSessionEventsOutputPayload`)
  - string
- Errors: `400`, `403`, `404`

#### `POST` `/v2/assistant/sessions/items/{sessionId}/resume`

Resolves pending session input and resumes agent execution.

- operationId: `ResumeSession`
- **Scopes**: `wilma-assistant:ResumeSession`
- **Parameters**
  - `sessionId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The user the session belongs to. Optional: identifies the user when a service or tenant token is used; when omitted the session is not scoped to a specific user. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `ResumeSessionRequestContent`) **(required)**
  - `pendingId` — string **(required)**
  - `inputResponses` — array **(required)**
    - _array of_ `SessionInputResponse`
      - `callId` — string **(required)**
      - `result` — any
      - `approved` — boolean
- **Response 202** (`ResumeSessionResponseContent`)
  - `sessionId` — string **(required)** _(minLen=1; maxLen=128)_
  - `startIndex` — number **(required)**
  - `traceId` — string — Trace recording the session in wilma-traces — every turn, model call and tool execution the agent ran. Read it with the wilma-traces GetTrace operation, or tail it live with StreamTrace next to the event stream `startIndex` addresses. One id for the whole session, not for this turn: the handle a later ContinueSession returns names the same trace StartSession opened, and each turn appends to it. The trace row is written once the turn's first step completes, so GetTrace may report NotFound in the moment right after this call returns. Absent when the session's trace is not the caller's to read — a session served by a Wildix built-in agent is recorded for Wildix rather than for the tenant. _(minLen=1; maxLen=128)_
- Errors: `400`, `403`, `404`, `409`, `503`

#### `POST` `/v2/assistant/sessions/items/{sessionId}/steer`

Adds a message to the turn already running, without discarding its work: the runtime injects
    it at the next model step boundary (a tool call already in flight finishes first). A session
    that is `waiting` on caller input cannot be steered and fails with a conflict — answer its
    pending invocations via ResumeSession; use ContinueSession for an `idle`, `stopped` or `failed`
    session. If the turn finishes before the steer is injected, the message runs as a new turn
    instead; `outcome` reports which happened, and the response carries the index to stream from.

- operationId: `SteerSession`
- **Scopes**: `wilma-assistant:SteerSession`
- **Parameters**
  - `sessionId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The user the session belongs to. Optional: identifies the user when a service or tenant token is used; when omitted the session is not scoped to a specific user. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `SteerSessionRequestContent`) **(required)**
  - `message` — string **(required)** _(minLen=1; maxLen=100000)_
  - `attachments` — array — Input attachments to include with the steering message. Fetch them via the Attachments API.
    - _array of_ `string`
  - `context` — array — Replaces the session's context documents, what the client has in view and the server cannot read for itself, from the next model step. Omit to keep them.
    - _array of_ `any`
  - `mentions` — array — Replaces the session's mentions from the next model step. Omit to keep them; pass an empty list to clear them. _(maxItems=20)_
    - _array of_ `Mention`
      - _oneOf_ — exactly one of:
        - **`reference`**
          - `reference` — MentionReference **(required)** — A resource selected as agent context, identified by its canonical URI, e.g. `wilma://insights/calls/{callId}/flows/{flowIndex}`. It is read with the permissions of the session or task it is attached to; the URI grants no access by itself.
            - `uri` — string **(required)** — Canonical URI identifying one entity on the Wilma platform, e.g. 'wilma://agents/UXDT1W9fI3sj' or 'wilma://skills/aB3dE5fG7hJ9'. The path names the owning service and entity kind. Opaque to the contracts that carry it; non-Wilma schemes (records of external systems) fit the same shape. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
            - `label` — string — Display name of the mention chip. The model sees it only to name a mention that could not be read or was removed. _(maxLen=256)_
- **Response 202** (`SteerSessionResponseContent`)
  - `sessionId` — string **(required)** _(minLen=1; maxLen=128)_
  - `startIndex` — number **(required)**
  - `traceId` — string — Trace recording the session in wilma-traces — every turn, model call and tool execution the agent ran. Read it with the wilma-traces GetTrace operation, or tail it live with StreamTrace next to the event stream `startIndex` addresses. One id for the whole session, not for this turn: the handle a later ContinueSession returns names the same trace StartSession opened, and each turn appends to it. The trace row is written once the turn's first step completes, so GetTrace may report NotFound in the moment right after this call returns. Absent when the session's trace is not the caller's to read — a session served by a Wildix built-in agent is recorded for Wildix rather than for the tenant. _(minLen=1; maxLen=128)_
  - `turn` — number **(required)** — The turn the message reached: the running turn when `steered`, the new turn when `promoted`.
  - `outcome` — string **(required)** — How a steer request was applied. `steered` means it reached the running turn at a step boundary with the turn's work intact. `promoted` means no step boundary remained, so the runtime ran the message as a new turn instead — a steer is never silently dropped. _(enum: `steered`, `promoted`)_
- Errors: `400`, `403`, `404`, `409`, `503`

#### `POST` `/v2/assistant/sessions/items/{sessionId}/stop`

Requests cancellation of the active turn in a durable assistant session.

- operationId: `StopSession`
- **Scopes**: `wilma-assistant:StopSession`
- **Parameters**
  - `sessionId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The user the session belongs to. Optional: identifies the user when a service or tenant token is used; when omitted the session is not scoped to a specific user. _(minLen=12; maxLen=12)_
- **Response 202** (`StopSessionResponseContent`)
  - `sessionId` — string **(required)** _(minLen=1; maxLen=128)_
  - `accepted` — boolean **(required)**
- Errors: `400`, `403`, `404`

#### `POST` `/v2/assistant/sessions/items/{sessionId}/turns`

Starts another turn in an existing durable assistant session.

- operationId: `ContinueSession`
- **Scopes**: `wilma-assistant:ContinueSession`
- **Parameters**
  - `sessionId` (path) — string **(required)** _(minLen=1; maxLen=128)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The user the session belongs to. Optional: identifies the user when a service or tenant token is used; when omitted the session is not scoped to a specific user. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `ContinueSessionRequestContent`) **(required)**
  - `message` — string **(required)** _(minLen=1; maxLen=100000)_
  - `attachments` — array — Ids of input attachments to include with this user message, as returned by UploadAttachment. Their stored metadata is reported back on the turn's MessageReceivedEvent.
    - _array of_ `string`
  - `context` — array — Replaces the session's context documents: what the client has in view and the server cannot read for itself. Omit to keep them.
    - _array of_ `any`
  - `mentions` — array — Replaces the session's mentions. Omit to keep them; pass an empty list to clear them. _(maxItems=20)_
    - _array of_ `Mention`
      - _oneOf_ — exactly one of:
        - **`reference`**
          - `reference` — MentionReference **(required)** — A resource selected as agent context, identified by its canonical URI, e.g. `wilma://insights/calls/{callId}/flows/{flowIndex}`. It is read with the permissions of the session or task it is attached to; the URI grants no access by itself.
            - `uri` — string **(required)** — Canonical URI identifying one entity on the Wilma platform, e.g. 'wilma://agents/UXDT1W9fI3sj' or 'wilma://skills/aB3dE5fG7hJ9'. The path names the owning service and entity kind. Opaque to the contracts that carry it; non-Wilma schemes (records of external systems) fit the same shape. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
            - `label` — string — Display name of the mention chip. The model sees it only to name a mention that could not be read or was removed. _(maxLen=256)_
  - `tools` — array
    - _array of_ `SessionClientTool`
      - `name` — string **(required)**
      - `description` — string
      - `schema` — any **(required)**
      - `fulfilment` — string — Who produces an invocation's result. `server` tools execute inside the agent runtime. `client` tools are executed by the caller, so the turn suspends until it answers. `synthetic` tools never execute at all — they exist to put something on screen, and the runtime supplies their result itself, so the turn does not suspend. _(enum: `server`, `client`, `synthetic`)_
      - `gate` — string — Whether the turn suspends on an invocation, and for what. Orthogonal to fulfilment: a `server` tool may be gated on a user decision (an approval), and a `synthetic` tool may be ungated (render and continue) or gated (an editable draft awaiting confirmation). _(enum: `none`, `result`, `decision`)_
      - `surface` — string — Where a client should surface an invocation. Affects placement only, never behaviour. _(enum: `hidden`, `activity`, `content`)_
      - `stream` — boolean — Emit InvocationDeltaEvent for calls to this tool, so the caller can render the input as the model writes it — useful when the input carries content rather than a lookup key. Defaults to false.
      - `ack` — any — Result handed back to the model for a `synthetic` tool, typically a short instruction telling the model what the user can now see. Ignored for `client` tools.
  - `skills` — array
    - _array of_ `SessionSkill`
      - `name` — string **(required)**
      - `description` — string **(required)**
      - `body` — string **(required)**
  - `connectors` — SessionConnectors — Per-session connector overrides, by connector instance id. `disabled` turns connectors off for this session only; `enabled` turns back on connectors the user disabled in their settings, for this session only.
    - `disabled` — array
      - _array of_ `string`
    - `enabled` — array
      - _array of_ `string`
- **Response 202** (`ContinueSessionResponseContent`)
  - `sessionId` — string **(required)** _(minLen=1; maxLen=128)_
  - `startIndex` — number **(required)**
  - `traceId` — string — Trace recording the session in wilma-traces — every turn, model call and tool execution the agent ran. Read it with the wilma-traces GetTrace operation, or tail it live with StreamTrace next to the event stream `startIndex` addresses. One id for the whole session, not for this turn: the handle a later ContinueSession returns names the same trace StartSession opened, and each turn appends to it. The trace row is written once the turn's first step completes, so GetTrace may report NotFound in the moment right after this call returns. Absent when the session's trace is not the caller's to read — a session served by a Wildix built-in agent is recorded for Wildix rather than for the tenant. _(minLen=1; maxLen=128)_
- Errors: `400`, `403`, `404`, `409`, `503`

### Settings

#### `GET` `/v2/assistant/settings`

Gets AI assistant settings for the user. Returns personalisation fields (style, about),
    the agents, skills and connectors available to the user, and per-user skill and connector
    preferences. Each agent's `connectorIds` say which of the `connectors` it calls, and
    `copilotSettings` says whether Copilot may assist the user.

- operationId: `GetSettings`
- **Scopes**: `wilma-assistant:GetSettings`, `wilma-assistant:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The unique identifier of the user when a service or tenant token is used. _(minLen=12; maxLen=12)_
- **Response 200** (`GetSettingsResponseContent`)
  - `style` — UserStyleSettings — How the assistant should communicate with this user.
    - `tone` — string _(minLen=1; maxLen=64)_
  - `about` — UserAboutSettings — Background the assistant may use to personalise replies for this user.
    - `description` — string _(minLen=1; maxLen=2000)_
  - `agents` — array — Agents available to the user for selection in the assistant UI.
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
  - `skills` — array — Skills available to the user. Manage skill definitions in wilma-skills.
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
  - `skillsSettings` — UserSkillsSettings — Per-user skill preferences. Skills the user has disabled are omitted from the effective skill set at runtime.
    - `disabled` — array
      - _array of_ `string`
  - `connectors` — array — Connectors configured for the company that this deployment can execute, one per instance, with this user's authorization and enablement state. Filter by an agent's `connectorIds` for the agent in use. Absent when the connector services could not be answered for: the rest of the settings still apply.
    - _array of_ `AvailableConnector`
      - `id` — string **(required)** — Connector instance id — the id an agent's capabilities and the user's `disabled` preference refer to. For an MCP server, the id of the Tool that registers it. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `key` — string **(required)** — Connector definition key, e.g. `salesforce`. Several instances may share one. For an MCP server, its provider key (`mcp_…`), which is also what AuthorizeConnector takes. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
      - `kind` — string — The kind of thing an AvailableConnector entry stands for. _(enum: `connector`, `mcp_server`)_
      - `grant` — union **(required)** — Coarse permission grant for a configured connector. The service computes the effective, server-enforced tool set by filtering the pinned definition's tools with this grant (using each tool's `ConnectorToolAccess`), and requests only the scopes the grant implies at connection time.
        - _oneOf_ — exactly one of:
          - **`read`**
            - `read` — ConnectorGrantRead **(required)** — Marker: grant every READ tool.
          - **`readWrite`**
            - `readWrite` — ConnectorGrantReadWrite **(required)** — Marker: grant every READ and WRITE tool.
          - **`all`**
            - `all` — ConnectorGrantAll **(required)** — Marker: grant every tool, including DESTRUCTIVE.
          - **`tools`**
            - `tools` — array **(required)** — Advanced: an explicit allowlist of tool ids, regardless of access class.
              - _array of_ `string`
      - `title` — string **(required)**
      - `icon` — string
      - `provider` — string **(required)** — Provider the connector authenticates against, e.g. `salesforce`. A user's consent is per provider, so connecting one instance connects every instance on the same provider.
      - `mode` — string **(required)** — Supported credential resolution mode. Mirrors wilma-secrets `ConnectionType`. _(enum: `shared`, `user`)_
      - `authorization` — string **(required)** — The current user's authorization status for a connector. Drives the Connect button: the connector is usable when NOT_REQUIRED or CONNECTED, and prompts the user to connect when NOT_CONNECTED or NEEDS_RECONNECT. _(enum: `not_required`, `not_connected`, `connected`, `needs_reconnect`)_
      - `enabled` — boolean **(required)** — Effective enablement for this user, after applying their disabled preferences.
  - `connectorsSettings` — UserConnectorsSettings — Per-user connector preferences, by connector instance id. Connectors the user has disabled are removed from the effective set at runtime, even when an admin enabled them.
    - `disabled` — array
      - _array of_ `string`
  - `copilotSettings` — UserCopilotSettings — Per-user Copilot settings. Resolved by the service; PatchSettings does not change them.
    - `availability` — CopilotAvailability — Whether Copilot (real-time agent-assist, wildix.wilma.copilot) may assist the user, resolved from the company's live profiles and their `audience`. Entries that need a conversation to decide (queue, service, trunk, agent) and department entries (PBX department ids, which no directory here exposes) count as matching, except in the `before` stage, where the user is the one who opens Copilot and conversation entries say nothing. A profile limited to the `before` stage enables Copilot but covers no channel.
      - `enabled` — boolean **(required)** — Whether at least one live profile may assist the user.
      - `channels` — array — Conversation channels covered by the profiles that may assist the user. Empty when `enabled` is false.
        - _array of_ `CopilotChannel`
      - `stages` — array — Stages covered by the profiles that may assist the user. `before` means Copilot can be opened without a call, chat or conference. Empty when `enabled` is false.
        - _array of_ `CopilotStage`
      - `reason` — string — Why Copilot is or is not available to the user. _(enum: `available`, `no_live_profile`, `not_in_audience`)_
- Errors: `400`, `403`

#### `PATCH` `/v2/assistant/settings`

Updates AI assistant settings for the user. Only supplied fields are changed.
    Returns the effective settings after the update, including the current agent and
    skill catalog.

- operationId: `PatchSettings`
- **Scopes**: `wilma-assistant:PatchSettings`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The unique identifier of the user when a service or tenant token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `PatchSettingsRequestContent`)
  - `style` — UserStyleSettings — How the assistant should communicate with this user.
    - `tone` — string _(minLen=1; maxLen=64)_
  - `about` — UserAboutSettings — Background the assistant may use to personalise replies for this user.
    - `description` — string _(minLen=1; maxLen=2000)_
  - `skills` — UserSkillsSettings — Per-user skill preferences. Skills the user has disabled are omitted from the effective skill set at runtime.
    - `disabled` — array
      - _array of_ `string`
  - `connectors` — UserConnectorsSettings — Per-user connector preferences, by connector instance id. Connectors the user has disabled are removed from the effective set at runtime, even when an admin enabled them.
    - `disabled` — array
      - _array of_ `string`
- **Response 200** (`PatchSettingsResponseContent`)
  - `style` — UserStyleSettings — How the assistant should communicate with this user.
    - `tone` — string _(minLen=1; maxLen=64)_
  - `about` — UserAboutSettings — Background the assistant may use to personalise replies for this user.
    - `description` — string _(minLen=1; maxLen=2000)_
  - `agents` — array
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
  - `skills` — array
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
  - `skillsSettings` — UserSkillsSettings — Per-user skill preferences. Skills the user has disabled are omitted from the effective skill set at runtime.
    - `disabled` — array
      - _array of_ `string`
  - `connectors` — array — Connectors configured for the company that this deployment can execute, one per instance, with this user's authorization and enablement state. Filter by an agent's `connectorIds` for the agent in use. Absent when the connector services could not be answered for: the rest of the settings still apply.
    - _array of_ `AvailableConnector`
      - `id` — string **(required)** — Connector instance id — the id an agent's capabilities and the user's `disabled` preference refer to. For an MCP server, the id of the Tool that registers it. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `key` — string **(required)** — Connector definition key, e.g. `salesforce`. Several instances may share one. For an MCP server, its provider key (`mcp_…`), which is also what AuthorizeConnector takes. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
      - `kind` — string — The kind of thing an AvailableConnector entry stands for. _(enum: `connector`, `mcp_server`)_
      - `grant` — union **(required)** — Coarse permission grant for a configured connector. The service computes the effective, server-enforced tool set by filtering the pinned definition's tools with this grant (using each tool's `ConnectorToolAccess`), and requests only the scopes the grant implies at connection time.
        - _oneOf_ — exactly one of:
          - **`read`**
            - `read` — ConnectorGrantRead **(required)** — Marker: grant every READ tool.
          - **`readWrite`**
            - `readWrite` — ConnectorGrantReadWrite **(required)** — Marker: grant every READ and WRITE tool.
          - **`all`**
            - `all` — ConnectorGrantAll **(required)** — Marker: grant every tool, including DESTRUCTIVE.
          - **`tools`**
            - `tools` — array **(required)** — Advanced: an explicit allowlist of tool ids, regardless of access class.
              - _array of_ `string`
      - `title` — string **(required)**
      - `icon` — string
      - `provider` — string **(required)** — Provider the connector authenticates against, e.g. `salesforce`. A user's consent is per provider, so connecting one instance connects every instance on the same provider.
      - `mode` — string **(required)** — Supported credential resolution mode. Mirrors wilma-secrets `ConnectionType`. _(enum: `shared`, `user`)_
      - `authorization` — string **(required)** — The current user's authorization status for a connector. Drives the Connect button: the connector is usable when NOT_REQUIRED or CONNECTED, and prompts the user to connect when NOT_CONNECTED or NEEDS_RECONNECT. _(enum: `not_required`, `not_connected`, `connected`, `needs_reconnect`)_
      - `enabled` — boolean **(required)** — Effective enablement for this user, after applying their disabled preferences.
  - `connectorsSettings` — UserConnectorsSettings — Per-user connector preferences, by connector instance id. Connectors the user has disabled are removed from the effective set at runtime, even when an admin enabled them.
    - `disabled` — array
      - _array of_ `string`
  - `copilotSettings` — UserCopilotSettings — Per-user Copilot settings. Resolved by the service; PatchSettings does not change them.
    - `availability` — CopilotAvailability — Whether Copilot (real-time agent-assist, wildix.wilma.copilot) may assist the user, resolved from the company's live profiles and their `audience`. Entries that need a conversation to decide (queue, service, trunk, agent) and department entries (PBX department ids, which no directory here exposes) count as matching, except in the `before` stage, where the user is the one who opens Copilot and conversation entries say nothing. A profile limited to the `before` stage enables Copilot but covers no channel.
      - `enabled` — boolean **(required)** — Whether at least one live profile may assist the user.
      - `channels` — array — Conversation channels covered by the profiles that may assist the user. Empty when `enabled` is false.
        - _array of_ `CopilotChannel`
      - `stages` — array — Stages covered by the profiles that may assist the user. `before` means Copilot can be opened without a call, chat or conference. Empty when `enabled` is false.
        - _array of_ `CopilotStage`
      - `reason` — string — Why Copilot is or is not available to the user. _(enum: `available`, `no_live_profile`, `not_in_audience`)_
- Errors: `400`, `403`

### Schemas appendix — Wilma Assistant API

<details><summary>132 component schemas</summary>

**`Actor`**

_Who performed an action: an interactive user, an API key or an internal service._

- `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
- `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
- `name` — string — Human readable name of the actor at the time of the action.

**`ActorType`**

- string _(enum: `user`, `api_key`, `service`)_

**`AgentEngineKind`**

_Which member of AgentEngine an agent carries, without the engine's configuration._

- string _(enum: `ai`, `webhook`, `sqs`)_

**`AgentGuardrailActionType`**

_The action members by name, for reporting what actually ran. Session events carry this rather than AgentGuardrailAction because an event reports a decision, not a configuration._

- string _(enum: `observe`, `redact`, `block`, `end`)_

**`AgentGuardrailErrorMode`**

_What happens when the checker itself errors or times out. OPEN lets the turn through unscreened and records GuardrailFailedEvent, so an unscreened turn is a fact in the log rather than an absence; CLOSED refuses it. Defaults to OPEN: an agent that stops answering because a small model had a bad minute is a worse and far likelier outage than the rare turn that goes unscreened. Background tasks, where nobody is waiting and a retry is free, are the case for CLOSED._

- string _(enum: `open`, `closed`)_

**`AgentGuardrailPreset`**

_A prebuilt check. Each preset is a platform-maintained prompt shipped in code and versioned with the platform, not a tenant row — so a support question about what a preset caught has one answer. A preset check is otherwise an ordinary AgentGuardrailCheck: its sensitivity and action are the tenant's to set, and `notes` narrows its prompt without replacing it._

- string _(enum: `jailbreak`, `offTopic`, `abuse`, `harmful`, `selfHarm`, `pii`, `secrets`, `regulatedAdvice`)_

**`AgentGuardrailSensitivity`**

_How much confidence a verdict needs before it counts as tripped. The checker reports a confidence per check and this is the threshold against it, so raising sensitivity catches more and costs more false positives without changing the prompt or the model: `low` trips only on high confidence, `medium` on high and medium, `high` on anything but a clear pass. Defaults to MEDIUM._

- string _(enum: `low`, `medium`, `high`)_

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

**`AgentStatus`**

- string _(enum: `draft`, `active`)_

**`AgentWorkflowConditionType`**

_Which kind of condition took a transition, as reported on the session event stream (WorkflowTransitionEvent) and in traces. Mirrors the members of AgentWorkflowCondition: `prompt` is the only one the model decides, every other was settled by the runtime with no model call._

- string _(enum: `always`, `prompt`, `expression`, `result`, `failure`, `fallback`)_

**`AgentWorkflowStepType`**

_Which handler a step carries, reported on the session event stream (WorkflowStepEnteredEvent) and in traces. Mirrors the members of AgentWorkflowHandler and exists so a reader does not have to load the agent version snapshot to tell a stretch of conversation from a runtime action: a trace is read long after the fact, by an operator who has the session and not the definition it ran against. `conversation` is the only member that hands the turn to the model; which capability an `action` step performed is named by the invocation events that follow it._

- string _(enum: `conversation`, `message`, `action`, `variables`, `workflow`, `result`, `end`)_

**`ArtifactFile`**

_A file available for preview or download: the single file of an artifact, or an entry inside its archive._

- `path` — string **(required)** — Path of one file inside an artifact, relative to the artifact's root and always with forward slashes: `index.html`, `assets/logo.png`. Never absolute, never containing `..`. _(minLen=1; maxLen=1024)_
- `size` — number **(required)** — Size of this file in bytes, uncompressed for an archive entry.
- `contentType` — string — MIME type the file is served with, e.g. 'text/html' or 'image/png'.

**`ArtifactKind`**

_Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest._

- string _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_

**`ArtifactSharedEvent`**

_Emitted when the agent shares an artifact via the `share_artifact` tool, after the revision has been uploaded. Carries the file list and card metadata; the viewer reads content URLs and sharing from the wilma-artifacts service. Sharing the same artifact again publishes a new `revision` under the same `artifactId` and emits this event again._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `artifactId` — string **(required)** — Id of the registered artifact; fetch it via wilma-artifacts (GetArtifact, GetArtifactContentUrl, DownloadArtifact). _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
- `title` — string **(required)** — Human-readable title shown to the user.
- `description` — string — One-line summary shown under the title.
- `name` — string — Download filename shown to the user. _(minLen=1; maxLen=1024)_
- `kind` — string **(required)** — Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest. _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_
- `files` — array **(required)** — Files in this revision, with their paths, sizes and MIME types. _(minItems=1; maxItems=500)_
  - _array of_ `ArtifactFile`
    - `path` — string **(required)** — Path of one file inside an artifact, relative to the artifact's root and always with forward slashes: `index.html`, `assets/logo.png`. Never absolute, never containing `..`. _(minLen=1; maxLen=1024)_
    - `size` — number **(required)** — Size of this file in bytes, uncompressed for an archive entry.
    - `contentType` — string — MIME type the file is served with, e.g. 'text/html' or 'image/png'.
- `entry` — string — Path of the file the viewer opens first. When omitted, the first file in files is opened. _(minLen=1; maxLen=1024)_
- `revision` — number — Revision this event published: 1 for a new artifact, higher when the agent republished it in place.
- `path` — string — Sandbox path the artifact was shared from: the file, or the folder a bundle's paths are relative to, e.g. `/workspace/report.md` or `/workspace/site`.
- `callId` — string — Id of the `share_artifact` tool call that produced the artifact.

**`AssistantQuickCommand`**

_A starter prompt offered as a card on an empty thread. Picking it sends `prompt` as the user's first message, so the user never types it._

- `title` — string **(required)** — Card label, e.g. 'Summarize my day'. Rendered on one line and truncated when it does not fit. _(minLen=1; maxLen=60)_
- `description` — string — Optional line under the label. Also one line, so keep it to a short clarification of what the command does. _(minLen=1; maxLen=120)_
- `prompt` — string **(required)** — The message actually sent when the card is picked. Usually longer and more explicit than the label, since it is what the model reads. _(minLen=1; maxLen=2000)_

**`AssistantSessionEvent`**

_A single typed event on the assistant channel. Exactly one member is set; the member name doubles as the `event:` field of the SSE frames. The assistant is the only channel with an interactive user attached to the session, so it is the only one that can suspend a turn for input — InputRequestedEvent and SessionWaitingEvent, answered through ResumeSession — or accept a steer into a running turn through SteerSession. Assistant invocations may carry any `fulfilment`: callers declare `client` and `synthetic` tools through SessionClientTool alongside the agent's own `server` tools._

- _oneOf_ — exactly one of:
  - **`sessionStarted`**
    - `sessionStarted` — SessionStartedEvent **(required)** — Emitted once as the very first event of a session, when it is created. Confirms the session id and the agent the session is bound to.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `sessionId` — string **(required)** _(minLen=1; maxLen=128)_
      - `agentId` — string _(minLen=12; maxLen=12)_
  - **`sessionIdle`**
    - `sessionIdle` — SessionIdleEvent **(required)** — Terminal event of a successful turn: the session is idle and ready for the next turn.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
  - **`sessionStopped`**
    - `sessionStopped` — SessionStoppedEvent **(required)** — Terminal event emitted when the active turn was cancelled via the channel's stop operation.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `reason` — string **(required)** _(enum: `user`)_
  - **`sessionTerminated`**
    - `sessionTerminated` — SessionTerminatedEvent **(required)** — Terminal event emitted when the platform ended the session rather than let it continue: the session is in `terminated` status. Distinct from SessionStoppedEvent, which records a user or operator asking to stop — folding the two together would leave a refused session indistinguishable from a clean finish in every completion-rate report. On voice the call is hung up as this is emitted; on the other channels there is nothing to hang up and termination is the status alone — history is kept, and the session simply accepts no further turns.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `reason` — string **(required)** _(enum: `guardrail`)_
      - `guardrail` — string — The check whose `end` action terminated the session, when `reason` is `guardrail`. _(minLen=1; maxLen=64)_
      - `message` — string — What the caller was told before the session ended.
  - **`sessionFailed`**
    - `sessionFailed` — SessionFailedEvent **(required)** — Terminal event emitted after TurnFailedEvent: the session is in `failed` status. A new turn starts from the last consistent snapshot.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `code` — string **(required)**
      - `message` — string **(required)**
  - **`turnStarted`**
    - `turnStarted` — TurnStartedEvent **(required)** — Emitted when a turn begins executing. All subsequent events up to the matching TurnCompletedEvent/TurnFailedEvent belong to this turn.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)** — 1-based turn number within the session.
  - **`turnCompleted`**
    - `turnCompleted` — TurnCompletedEvent **(required)** — Emitted when a turn finishes successfully, with aggregate token usage for the turn. Followed by SessionIdleEvent.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `usage` — SessionUsage
        - `inputTokens` — number
        - `cachedTokens` — number — The part of `inputTokens` served from the provider's prompt cache. Absent when the provider does not report it.
        - `outputTokens` — number
        - `reasoningTokens` — number — The part of `outputTokens` spent on reasoning. Absent when the provider does not report it, or when the model does not reason.
        - `totalTokens` — number
  - **`turnFailed`**
    - `turnFailed` — TurnFailedEvent **(required)** — Emitted when a turn fails with an unrecoverable error. Followed by SessionFailedEvent.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `code` — string **(required)** — Stable machine-readable error code.
      - `message` — string **(required)**
  - **`messageReceived`**
    - `messageReceived` — MessageReceivedEvent **(required)** — Emitted right after TurnStartedEvent with the user message that triggered the turn, so a reconnecting client can render the conversation without a separate history fetch.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `message` — string **(required)**
      - `attachments` — array — Input files supplied with this message, as stored — enough to render the attachment alongside the message (name, type, size, thumbnail) without a separate Attachments call. Absent when the turn carried no files.
        - _array of_ `Attachment`
          - _(nesting depth limit — see `Attachment` in the Schemas appendix)_
  - **`messageAppended`**
    - `messageAppended` — MessageAppendedEvent **(required)** — Emitted for every assistant text token chunk. High frequency; drives live rendering of the reply.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `step` — number **(required)**
      - `delta` — string **(required)** — The new text fragment.
      - `soFar` — string **(required)** — The full assistant text accumulated so far in this step.
  - **`messageCompleted`**
    - `messageCompleted` — MessageCompletedEvent **(required)** — Emitted once per step when the assistant message text is complete.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `step` — number **(required)**
      - `text` — string **(required)**
      - `finishReason` — string **(required)** — Model finish reason for the step, e.g. `stop` or `tool-calls`.
  - **`stepStarted`**
    - `stepStarted` — StepStartedEvent **(required)** — Emitted each time the model starts a new inference step within a turn (a turn spans multiple steps when the model calls tools).
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `step` — number **(required)** — 1-based step number within the turn.
  - **`stepCompleted`**
    - `stepCompleted` — StepCompletedEvent **(required)** — Emitted when an inference step finishes, with token usage for the step when the provider reports it.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `step` — number **(required)**
      - `finishReason` — string **(required)**
      - `usage` — SessionUsage
        - `inputTokens` — number
        - `cachedTokens` — number — The part of `inputTokens` served from the provider's prompt cache. Absent when the provider does not report it.
        - `outputTokens` — number
        - `reasoningTokens` — number — The part of `outputTokens` spent on reasoning. Absent when the provider does not report it, or when the model does not reason.
        - `totalTokens` — number
  - **`reasoningDelta`**
    - `reasoningDelta` — ReasoningDeltaEvent **(required)** — Emitted for every reasoning (thinking) token chunk the model produces, when the selected model exposes reasoning. High frequency; intended for live typing indicators.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `step` — number **(required)**
      - `delta` — string **(required)** — The new reasoning fragment.
      - `soFar` — string **(required)** — The full reasoning text accumulated so far in this step, so late subscribers do not need to replay every delta.
  - **`reasoningCompleted`**
    - `reasoningCompleted` — ReasoningCompletedEvent **(required)** — Emitted once per step after the model finishes its reasoning block, carrying the complete reasoning text.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `step` — number **(required)**
      - `reasoning` — string **(required)**
  - **`invocationStarted`**
    - `invocationStarted` — InvocationStartedEvent **(required)** — Emitted when the model begins one tool invocation, before its input is complete. Every invocation starts here, regardless of how it is fulfilled or whether it suspends the turn. Carries the routing facts needed to render it — who fulfils it, whether the turn suspends, where to surface it, whether the input streams — so a client holding no tool registry (a replay, a shared session, an inspector) still renders correctly.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `step` — number **(required)**
      - `callId` — string **(required)** — Stable id of this invocation, referenced by every later event about it.
      - `toolName` — string **(required)**
      - `toolId` — string — The wilma-tools Tool backing this invocation. Absent for built-in tools, connector meta-tools and other capabilities that are not shared Tools. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `toolVersion` — number — Published tool version the model was offered, when `toolId` is set. Records which input schema the invocation was written against. _(min=1)_
      - `fulfilment` — string **(required)** — Who produces an invocation's result. `server` tools execute inside the agent runtime. `client` tools are executed by the caller, so the turn suspends until it answers. `synthetic` tools never execute at all — they exist to put something on screen, and the runtime supplies their result itself, so the turn does not suspend. _(enum: `server`, `client`, `synthetic`)_
      - `gate` — string **(required)** — Whether the turn suspends on an invocation, and for what. Orthogonal to fulfilment: a `server` tool may be gated on a user decision (an approval), and a `synthetic` tool may be ungated (render and continue) or gated (an editable draft awaiting confirmation). _(enum: `none`, `result`, `decision`)_
      - `surface` — string **(required)** — Where a client should surface an invocation. Affects placement only, never behaviour. _(enum: `hidden`, `activity`, `content`)_
      - `stream` — boolean **(required)** — True when the input arrives as InvocationDeltaEvent chunks ahead of InvocationInputCompletedEvent. Opt-in per tool, so tools with small inputs cost nothing.
  - **`invocationDelta`**
    - `invocationDelta` — InvocationDeltaEvent **(required)** — Emitted for each fragment of an invocation's input as the model writes it, when the tool opted into streamed input. The payload is raw partial JSON text exactly as the model emits it; clients parse it incrementally to render an invocation whose input is itself content — a drafted email, a chart spec, a shared document — while it is being written. High frequency.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `step` — number **(required)**
      - `callId` — string **(required)**
      - `delta` — string **(required)** — The new fragment of raw JSON input text.
      - `soFar` — string **(required)** — The raw JSON input text accumulated so far in this invocation, so late subscribers need not replay every delta. Being a prefix, it is not necessarily valid JSON on its own.
  - **`invocationInputCompleted`**
    - `invocationInputCompleted` — InvocationInputCompletedEvent **(required)** — Emitted once per invocation when its input is complete and parsed. Always emitted, whether or not the input streamed.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `step` — number **(required)**
      - `callId` — string **(required)**
      - `input` — any **(required)**
  - **`invocationResult`**
    - `invocationResult` — InvocationResultEvent **(required)** — Emitted when an invocation is resolved, however that happened: a server tool finishing, a caller returning a client tool's result on resume, a person answering a question or ruling on an approval, or the runtime supplying a `synthetic` tool's result. Emitted for every invocation without exception, so replaying the log from index 0 reconstructs the same state as watching it live.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `step` — number **(required)**
      - `callId` — string **(required)** — Id of the invocation this result answers, matching an InvocationStartedEvent.
      - `toolName` — string **(required)**
      - `toolId` — string — The wilma-tools Tool that executed, echoed from InvocationStartedEvent. Absent for invocations that are not backed by a shared Tool. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `toolVersion` — number — Published tool version that executed, when `toolId` is set. _(min=1)_
      - `status` — string **(required)** _(enum: `completed`, `failed`)_
      - `resolvedBy` — string **(required)** — Who supplied the result recorded by an InvocationResultEvent. _(enum: `server`, `client`, `user`)_
      - `output` — any
      - `error` — string — Present when status is `failed`.
  - **`taskStarted`**
    - `taskStarted` — TaskStartedEvent **(required)** — Emitted when the agent delegates a subtask to a task execution: the `delegate` tool or an agent-call capability. Events emitted inside the task are re-published on the session stream with `origin` set to this task, until the matching TaskCompletedEvent.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `taskId` — string **(required)** — Unique id of this task execution; referenced by `origin.taskId` of nested events.
      - `name` — string **(required)** — Task tool name, e.g. `delegate` or the name of the called agent.
      - `agentId` — string — Agent executing the task, when the task is a called or delegated agent. _(minLen=12; maxLen=12)_
      - `agentVersion` — number — Published version of the agent executing the task, resolved when the task started; absent when the task runs a draft. _(min=1)_
      - `instructions` — string **(required)** — The self-contained instructions handed to the task.
  - **`taskCompleted`**
    - `taskCompleted` — TaskCompletedEvent **(required)** — Emitted when a delegated task execution finishes, carrying its final answer as returned to the parent agent.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `taskId` — string **(required)**
      - `name` — string **(required)**
      - `output` — string **(required)**
  - **`workflowStepEntered`**
    - `workflowStepEntered` — WorkflowStepEnteredEvent **(required)** — Emitted when the workflow cursor arrives at a step, before the step runs — so every later event in the log belongs to the step most recently entered. The first is the graph's `entry` step; the last is a terminal step, which is where the session left the graph.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number — The turn the step was entered during, when it was entered inside one. Absent when the cursor moved between turns: an `action`, `message` or `variables` step needs no model call, so a chain of them can advance before the next turn begins.
      - `workflow` — string — The nested workflow (AgentWorkflow.nested) this step belongs to. Absent for a step of the main graph, which is how nesting is read off the stream — no separate enter/return events. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
      - `stepId` — string **(required)** — Identifier of a step within its workflow, unique per workflow (the main graph and each nested workflow are separate scopes). Stable and machine-facing: transitions reference it, and a result step's id is the name a caller branches on, so renaming a step's `label` never unwires the graph. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
      - `label` — string — The step's authored label, so a reader needs no copy of the agent definition to render the stream. _(minLen=1; maxLen=128)_
      - `stage` — string — The step's stage, as authored on it or inherited from upstream. Absent when the graph uses no stages. _(minLen=1; maxLen=64)_
      - `type` — string **(required)** — Which handler a step carries, reported on the session event stream (WorkflowStepEnteredEvent) and in traces. Mirrors the members of AgentWorkflowHandler and exists so a reader does not have to load the agent version snapshot to tell a stretch of conversation from a runtime action: a trace is read long after the fact, by an operator who has the session and not the definition it ran against. `conversation` is the only member that hands the turn to the model; which capability an `action` step performed is named by the invocation events that follow it. _(enum: `conversation`, `message`, `action`, `variables`, `workflow`, `result`, `end`)_
  - **`workflowTransition`**
    - `workflowTransition` — WorkflowTransitionEvent **(required)** — Emitted when a transition is taken, naming the exit and what decided it. Not emitted on a terminal step, which has no exits — a session that ended inside the graph is read from the last WorkflowStepEnteredEvent — and not emitted when a conversation step's conditions all stay false, which is the step simply continuing.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number — The turn the transition was evaluated in. Absent when the cursor moved between turns.
      - `workflow` — string — The nested workflow both steps belong to. Absent in the main graph; a transition never crosses graphs. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
      - `stepId` — string **(required)** — Step being left. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
      - `target` — string **(required)** — Step being entered. A WorkflowStepEnteredEvent for it follows. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
      - `condition` — string **(required)** — Which kind of condition took a transition, as reported on the session event stream (WorkflowTransitionEvent) and in traces. Mirrors the members of AgentWorkflowCondition: `prompt` is the only one the model decides, every other was settled by the runtime with no model call. _(enum: `always`, `prompt`, `expression`, `result`, `failure`, `fallback`)_
      - `reason` — string — The model's one-line reason for the move, as it gave it to the steering tool. Present only for `prompt` conditions.
  - **`workflowMoveRefused`**
    - `workflowMoveRefused` — WorkflowMoveRefusedEvent **(required)** — Emitted when the model asks to move somewhere the live step does not declare as an exit. The runtime refuses, names the legal exits, and the session carries on from the same step, so this is not a failure of the turn: it is the record of what callers keep reaching for and the graph does not offer. Aggregated per step, it is the shortest route to the exit a graph is missing.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `workflow` — string — The nested workflow the live step belongs to. Absent in the main graph. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
      - `stepId` — string **(required)** — The step the session stayed on. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
      - `requested` — string **(required)** — What the model asked for, verbatim — not necessarily a step that exists.
      - `reason` — string — The model's stated reason for the move it was refused.
  - **`workflowVariablesWritten`**
    - `workflowVariablesWritten` — WorkflowVariablesWrittenEvent **(required)** — Emitted when workflow variables are written: a `variables` step's assignments, or an action step capturing its result into `output`. The only record of the state `expression` conditions branch on and handlebars resolve against, so replaying the log from index 0 reconstructs the same variables the runtime had.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number — The turn the write happened in, when it happened inside one.
      - `workflow` — string — The nested workflow the writing step belongs to. Absent in the main graph. Variables are shared with the main graph either way — a nested workflow has no scope of its own. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
      - `stepId` — string **(required)** — Step that wrote them. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
      - `values` — any **(required)** — The names written and their resolved values, as a JSON object. Only what this write touched, not the whole state; a variable cleared by an empty assignment is present with an empty value.
  - **`guardrailTripped`**
    - `guardrailTripped` — GuardrailTrippedEvent **(required)** — Emitted when a check trips, including when its action is `observe` and the turn proceeds untouched — that is what makes observe mode a way to tune a guardrail against real traffic rather than a switched-off check.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `check` — string **(required)** — The check's `name` in the agent definition. _(minLen=1; maxLen=64)_
      - `preset` — string — A prebuilt check. Each preset is a platform-maintained prompt shipped in code and versioned with the platform, not a tenant row — so a support question about what a preset caught has one answer. A preset check is otherwise an ordinary AgentGuardrailCheck: its sensitivity and action are the tenant's to set, and `notes` narrows its prompt without replacing it. _(enum: `jailbreak`, `offTopic`, `abuse`, `harmful`, `selfHarm`, `pii`, `secrets`, `regulatedAdvice`)_
      - `confidence` — string **(required)** — How much confidence a verdict needs before it counts as tripped. The checker reports a confidence per check and this is the threshold against it, so raising sensitivity catches more and costs more false positives without changing the prompt or the model: `low` trips only on high confidence, `medium` on high and medium, `high` on anything but a clear pass. Defaults to MEDIUM. _(enum: `low`, `medium`, `high`)_
      - `action` — string **(required)** — The action members by name, for reporting what actually ran. Session events carry this rather than AgentGuardrailAction because an event reports a decision, not a configuration. _(enum: `observe`, `redact`, `block`, `end`)_
      - `reason` — string — The checker's own account of why it tripped. Recorded for whoever tunes the guardrail, and never shown to the caller: telling someone which check caught them is a free oracle for the next attempt.
  - **`guardrailFailed`**
    - `guardrailFailed` — GuardrailFailedEvent **(required)** — Emitted when the checker itself errored or timed out. Carries the errorMode decision, so a reader can tell a turn that was screened and found clean from one that was never screened — without this event a fail-open guardrail would be indistinguishable from a guardrail that found nothing.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
      - `errorMode` — string **(required)** — What happens when the checker itself errors or times out. OPEN lets the turn through unscreened and records GuardrailFailedEvent, so an unscreened turn is a fact in the log rather than an absence; CLOSED refuses it. Defaults to OPEN: an agent that stops answering because a small model had a bad minute is a worse and far likelier outage than the rare turn that goes unscreened. Background tasks, where nobody is waiting and a retry is free, are the case for CLOSED. _(enum: `open`, `closed`)_
      - `proceeded` — boolean **(required)** — True when the turn was allowed through unscreened (`errorMode: open`), false when it was refused.
      - `reason` — string — Why the checker failed — a timeout, a provider error.
  - **`sandboxStarted`**
    - `sandboxStarted` — SandboxStartedEvent **(required)** — Emitted when the turn is attached to its sandbox, the first time a sandbox-backed tool is used in the turn. A session reuses one sandbox across turns whenever possible.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `sandboxId` — string **(required)** — Provider-side sandbox id, stable while the sandbox is reused across turns.
      - `resumed` — boolean **(required)** — True when an existing sandbox from a previous turn was reattached; false when a fresh sandbox was created.
  - **`sandboxFailed`**
    - `sandboxFailed` — SandboxFailedEvent **(required)** — Emitted when acquiring the sandbox fails; the turn then fails with the same cause. Provides sandbox-level observability distinct from the generic TurnFailedEvent.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `message` — string **(required)**
  - **`artifactShared`**
    - `artifactShared` — ArtifactSharedEvent **(required)** — Emitted when the agent shares an artifact via the `share_artifact` tool, after the revision has been uploaded. Carries the file list and card metadata; the viewer reads content URLs and sharing from the wilma-artifacts service. Sharing the same artifact again publishes a new `revision` under the same `artifactId` and emits this event again.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `artifactId` — string **(required)** — Id of the registered artifact; fetch it via wilma-artifacts (GetArtifact, GetArtifactContentUrl, DownloadArtifact). _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
      - `title` — string **(required)** — Human-readable title shown to the user.
      - `description` — string — One-line summary shown under the title.
      - `name` — string — Download filename shown to the user. _(minLen=1; maxLen=1024)_
      - `kind` — string **(required)** — Semantic classification driving the preview. Each revision is one CDS file; an archive may also carry a bundle manifest. _(enum: `document`, `code`, `html`, `svg`, `diagram`, `component`, `file`, `bundle`)_
      - `files` — array **(required)** — Files in this revision, with their paths, sizes and MIME types. _(minItems=1; maxItems=500)_
        - _array of_ `ArtifactFile`
          - _(nesting depth limit — see `ArtifactFile` in the Schemas appendix)_
      - `entry` — string — Path of the file the viewer opens first. When omitted, the first file in files is opened. _(minLen=1; maxLen=1024)_
      - `revision` — number — Revision this event published: 1 for a new artifact, higher when the agent republished it in place.
      - `path` — string — Sandbox path the artifact was shared from: the file, or the folder a bundle's paths are relative to, e.g. `/workspace/report.md` or `/workspace/site`.
      - `callId` — string — Id of the `share_artifact` tool call that produced the artifact.
  - **`compactionStarted`**
    - `compactionStarted` — CompactionStartedEvent **(required)** — Emitted before a turn when the conversation history exceeds the model context budget and is being summarized. The turn starts after CompactionCompletedEvent.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
  - **`compactionCompleted`**
    - `compactionCompleted` — CompactionCompletedEvent **(required)** — Emitted when history compaction finishes and the turn proceeds with the summarized history.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)**
  - **`steerReceived`**
    - `steerReceived` — SteerReceivedEvent **(required)** — Emitted when a steer request is accepted for the turn already running, before it reaches the model. A turn can therefore carry more than one user message; build transcripts from event order, not from turn structure. This is the only record of the steering text: a turn the steer was promoted into starts with TurnStartedEvent but emits no MessageReceivedEvent, so the message is never recorded twice.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)** — The turn the steer was accepted for.
      - `message` — string **(required)** _(minLen=1; maxLen=100000)_
      - `attachments` — array — Input files supplied with the steering message, as stored. Absent when it carried no files.
        - _array of_ `Attachment`
          - _(nesting depth limit — see `Attachment` in the Schemas appendix)_
  - **`steerApplied`**
    - `steerApplied` — SteerAppliedEvent **(required)** — Emitted when an accepted steer has reached the model, naming the turn and step boundary where it took effect. The gap between SteerReceivedEvent and this event is user-visible, so a client can show the steering message as pending until it lands. A steer never interrupts a tool call that is already running. `turn` differs from the SteerReceivedEvent's `turn` when the steer was promoted: the running turn finished before a boundary arrived, so the message became the input of the following turn.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `turn` — number **(required)** — The turn the steering message was injected into — the following turn when it was promoted.
      - `step` — number **(required)** — The step the steering message was injected ahead of.
  - **`inputRequested`**
    - `inputRequested` — InputRequestedEvent **(required)** — Emitted when the turn cannot proceed without the caller: client-fulfilled tools, `ask_question`, or approval-gated tools. Each request references an invocation the stream has already announced — this event routes, it does not introduce calls. Answer through the channel's resume operation using the same `pendingId`; each answered invocation then emits its own InvocationResultEvent. Followed by SessionWaitingEvent.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `pendingId` — string **(required)**
      - `requests` — array **(required)**
        - _array of_ `SessionPendingInput`
          - _(nesting depth limit — see `SessionPendingInput` in the Schemas appendix)_
  - **`sessionWaiting`**
    - `sessionWaiting` — SessionWaitingEvent **(required)** — Terminal event of a turn that paused for caller input. The session stays in `waiting` status until resumed with the `pendingId`.
      - `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
      - `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
      - `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
        - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
        - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
      - `pendingId` — string **(required)**

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

**`Attachment`**

_An input file supplied with session input and included with a user message. Content lives in object storage; download via the owning channel's Attachments API. `contentType`, `size` and `thumbnailUrl` describe the stored content and are therefore absent until the upload has completed._

- `id` — string **(required)** — Nano-id attachment identifier (12 characters). _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
- `name` — string **(required)** — Filename shown to the user. Characters storage cannot represent are replaced with underscores. _(minLen=1; maxLen=255)_
- `contentType` — string — MIME type recorded by storage from the uploaded content, e.g. 'application/pdf'. Absent until the upload completes.
- `size` — number — Size in bytes recorded by storage from the uploaded content. Absent until the upload completes.
- `thumbnailUrl` — string — URL of a generated preview image, for rendering a thumbnail without downloading the file. Best-effort: absent until the upload completes, and for content no preview can be generated from.
- `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.

**`AuthorizeConnectorResponseContent`**

- `session` — ConnectSession **(required)** — Session handshake for interactive (OAuth) authorization, completed by the frontend through Nango. A catalogue provider's session is run by handing `sessionToken` to Nango's Connect UI. An MCP server's (`mcp_*` provider) also carries `authorizationUrl`, which the frontend opens in a popup before polling the connection: nothing reports the outcome back, so the connection is adopted on its next read and there is nothing to confirm.
  - `sessionToken` — string **(required)** — Session token the frontend uses to run the authorization flow.
  - `expiresAt` — string — Absolute expiry of the session.
  - `authorizationUrl` — string — The Nango URL that starts an MCP server's authorization. Present only for an `mcp_*` provider.

**`AvailableConnector`**

_One configured connector instance the current user can use in the assistant, with their authorization and enablement state. The catalogue lists every instance the company configured and this deployment can execute; an agent's `connectorIds` say which of them that agent calls. Backs the connectors menu and its per-connector Connect button._

- `id` — string **(required)** — Connector instance id — the id an agent's capabilities and the user's `disabled` preference refer to. For an MCP server, the id of the Tool that registers it. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
- `key` — string **(required)** — Connector definition key, e.g. `salesforce`. Several instances may share one. For an MCP server, its provider key (`mcp_…`), which is also what AuthorizeConnector takes. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
- `kind` — string — The kind of thing an AvailableConnector entry stands for. _(enum: `connector`, `mcp_server`)_
- `grant` — union **(required)** — Coarse permission grant for a configured connector. The service computes the effective, server-enforced tool set by filtering the pinned definition's tools with this grant (using each tool's `ConnectorToolAccess`), and requests only the scopes the grant implies at connection time.
  - _oneOf_ — exactly one of:
    - **`read`**
      - `read` — ConnectorGrantRead **(required)** — Marker: grant every READ tool.
    - **`readWrite`**
      - `readWrite` — ConnectorGrantReadWrite **(required)** — Marker: grant every READ and WRITE tool.
    - **`all`**
      - `all` — ConnectorGrantAll **(required)** — Marker: grant every tool, including DESTRUCTIVE.
    - **`tools`**
      - `tools` — array **(required)** — Advanced: an explicit allowlist of tool ids, regardless of access class.
        - _array of_ `string`
- `title` — string **(required)**
- `icon` — string
- `provider` — string **(required)** — Provider the connector authenticates against, e.g. `salesforce`. A user's consent is per provider, so connecting one instance connects every instance on the same provider.
- `mode` — string **(required)** — Supported credential resolution mode. Mirrors wilma-secrets `ConnectionType`. _(enum: `shared`, `user`)_
- `authorization` — string **(required)** — The current user's authorization status for a connector. Drives the Connect button: the connector is usable when NOT_REQUIRED or CONNECTED, and prompts the user to connect when NOT_CONNECTED or NEEDS_RECONNECT. _(enum: `not_required`, `not_connected`, `connected`, `needs_reconnect`)_
- `enabled` — boolean **(required)** — Effective enablement for this user, after applying their disabled preferences.

**`AvailableConnectorKind`**

_The kind of thing an AvailableConnector entry stands for._

- string _(enum: `connector`, `mcp_server`)_

**`ChannelType`**

_A channel an agent can serve (see AgentChannels for enablement). Also the runtime channel recorded by the channel runtimes / wilma-traces. A background task has no delivery surface and therefore no channel._

- string _(enum: `voice`, `chat`, `assistant`)_

**`CompactionCompletedEvent`**

_Emitted when history compaction finishes and the turn proceeds with the summarized history._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**

**`CompactionStartedEvent`**

_Emitted before a turn when the conversation history exceeds the model context budget and is being summarized. The turn starts after CompactionCompletedEvent._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**

**`ConfirmConnectorAuthorizationRequestContent`**

- `connectionId` — string **(required)** — Connection id returned by the authorization flow. _(minLen=1; maxLen=256)_

**`ConfirmConnectorAuthorizationResponseContent`**

- `connector` — AvailableConnector **(required)** — One configured connector instance the current user can use in the assistant, with their authorization and enablement state. The catalogue lists every instance the company configured and this deployment can execute; an agent's `connectorIds` say which of them that agent calls. Backs the connectors menu and its per-connector Connect button.
  - `id` — string **(required)** — Connector instance id — the id an agent's capabilities and the user's `disabled` preference refer to. For an MCP server, the id of the Tool that registers it. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `key` — string **(required)** — Connector definition key, e.g. `salesforce`. Several instances may share one. For an MCP server, its provider key (`mcp_…`), which is also what AuthorizeConnector takes. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
  - `kind` — string — The kind of thing an AvailableConnector entry stands for. _(enum: `connector`, `mcp_server`)_
  - `grant` — union **(required)** — Coarse permission grant for a configured connector. The service computes the effective, server-enforced tool set by filtering the pinned definition's tools with this grant (using each tool's `ConnectorToolAccess`), and requests only the scopes the grant implies at connection time.
    - _oneOf_ — exactly one of:
      - **`read`**
        - `read` — ConnectorGrantRead **(required)** — Marker: grant every READ tool.
      - **`readWrite`**
        - `readWrite` — ConnectorGrantReadWrite **(required)** — Marker: grant every READ and WRITE tool.
      - **`all`**
        - `all` — ConnectorGrantAll **(required)** — Marker: grant every tool, including DESTRUCTIVE.
      - **`tools`**
        - `tools` — array **(required)** — Advanced: an explicit allowlist of tool ids, regardless of access class.
          - _array of_ `string`
  - `title` — string **(required)**
  - `icon` — string
  - `provider` — string **(required)** — Provider the connector authenticates against, e.g. `salesforce`. A user's consent is per provider, so connecting one instance connects every instance on the same provider.
  - `mode` — string **(required)** — Supported credential resolution mode. Mirrors wilma-secrets `ConnectionType`. _(enum: `shared`, `user`)_
  - `authorization` — string **(required)** — The current user's authorization status for a connector. Drives the Connect button: the connector is usable when NOT_REQUIRED or CONNECTED, and prompts the user to connect when NOT_CONNECTED or NEEDS_RECONNECT. _(enum: `not_required`, `not_connected`, `connected`, `needs_reconnect`)_
  - `enabled` — boolean **(required)** — Effective enablement for this user, after applying their disabled preferences.

**`ConflictExceptionResponseContent`**

_The request conflicts with the current state of the resource, e.g. a duplicate name, a resource still in use, or an unmet precondition._

- `message` — string **(required)**

**`ConnectSession`**

_Session handshake for interactive (OAuth) authorization, completed by the frontend through Nango. A catalogue provider's session is run by handing `sessionToken` to Nango's Connect UI. An MCP server's (`mcp_*` provider) also carries `authorizationUrl`, which the frontend opens in a popup before polling the connection: nothing reports the outcome back, so the connection is adopted on its next read and there is nothing to confirm._

- `sessionToken` — string **(required)** — Session token the frontend uses to run the authorization flow.
- `expiresAt` — string — Absolute expiry of the session.
- `authorizationUrl` — string — The Nango URL that starts an MCP server's authorization. Present only for an `mcp_*` provider.

**`ConnectorAuthorizationMode`**

_Supported credential resolution mode. Mirrors wilma-secrets `ConnectionType`._

- string _(enum: `shared`, `user`)_

**`ConnectorAuthorizationStatus`**

_The current user's authorization status for a connector. Drives the Connect button: the connector is usable when NOT_REQUIRED or CONNECTED, and prompts the user to connect when NOT_CONNECTED or NEEDS_RECONNECT._

- string _(enum: `not_required`, `not_connected`, `connected`, `needs_reconnect`)_

**`ConnectorGrantAll`**

_Marker: grant every tool, including DESTRUCTIVE._

- ConnectorGrantAll

**`ConnectorGrantRead`**

_Marker: grant every READ tool._

- ConnectorGrantRead

**`ConnectorGrantReadWrite`**

_Marker: grant every READ and WRITE tool._

- ConnectorGrantReadWrite

**`ConnectorToolGrant`**

_Coarse permission grant for a configured connector. The service computes the effective, server-enforced tool set by filtering the pinned definition's tools with this grant (using each tool's `ConnectorToolAccess`), and requests only the scopes the grant implies at connection time._

- _oneOf_ — exactly one of:
  - **`read`**
    - `read` — ConnectorGrantRead **(required)** — Marker: grant every READ tool.
  - **`readWrite`**
    - `readWrite` — ConnectorGrantReadWrite **(required)** — Marker: grant every READ and WRITE tool.
  - **`all`**
    - `all` — ConnectorGrantAll **(required)** — Marker: grant every tool, including DESTRUCTIVE.
  - **`tools`**
    - `tools` — array **(required)** — Advanced: an explicit allowlist of tool ids, regardless of access class.
      - _array of_ `string`

**`ContinueSessionRequestContent`**

- `message` — string **(required)** _(minLen=1; maxLen=100000)_
- `attachments` — array — Ids of input attachments to include with this user message, as returned by UploadAttachment. Their stored metadata is reported back on the turn's MessageReceivedEvent.
  - _array of_ `string`
- `context` — array — Replaces the session's context documents: what the client has in view and the server cannot read for itself. Omit to keep them.
  - _array of_ `any`
- `mentions` — array — Replaces the session's mentions. Omit to keep them; pass an empty list to clear them. _(maxItems=20)_
  - _array of_ `Mention`
    - _oneOf_ — exactly one of:
      - **`reference`**
        - `reference` — MentionReference **(required)** — A resource selected as agent context, identified by its canonical URI, e.g. `wilma://insights/calls/{callId}/flows/{flowIndex}`. It is read with the permissions of the session or task it is attached to; the URI grants no access by itself.
          - _(nesting depth limit — see `MentionReference` in the Schemas appendix)_
- `tools` — array
  - _array of_ `SessionClientTool`
    - `name` — string **(required)**
    - `description` — string
    - `schema` — any **(required)**
    - `fulfilment` — string — Who produces an invocation's result. `server` tools execute inside the agent runtime. `client` tools are executed by the caller, so the turn suspends until it answers. `synthetic` tools never execute at all — they exist to put something on screen, and the runtime supplies their result itself, so the turn does not suspend. _(enum: `server`, `client`, `synthetic`)_
    - `gate` — string — Whether the turn suspends on an invocation, and for what. Orthogonal to fulfilment: a `server` tool may be gated on a user decision (an approval), and a `synthetic` tool may be ungated (render and continue) or gated (an editable draft awaiting confirmation). _(enum: `none`, `result`, `decision`)_
    - `surface` — string — Where a client should surface an invocation. Affects placement only, never behaviour. _(enum: `hidden`, `activity`, `content`)_
    - `stream` — boolean — Emit InvocationDeltaEvent for calls to this tool, so the caller can render the input as the model writes it — useful when the input carries content rather than a lookup key. Defaults to false.
    - `ack` — any — Result handed back to the model for a `synthetic` tool, typically a short instruction telling the model what the user can now see. Ignored for `client` tools.
- `skills` — array
  - _array of_ `SessionSkill`
    - `name` — string **(required)**
    - `description` — string **(required)**
    - `body` — string **(required)**
- `connectors` — SessionConnectors — Per-session connector overrides, by connector instance id. `disabled` turns connectors off for this session only; `enabled` turns back on connectors the user disabled in their settings, for this session only.
  - `disabled` — array
    - _array of_ `string`
  - `enabled` — array
    - _array of_ `string`

**`ContinueSessionResponseContent`**

_Handle returned by operations that start or continue a turn: the session, the event index from which the caller should stream, and the trace recording it._

- `sessionId` — string **(required)** _(minLen=1; maxLen=128)_
- `startIndex` — number **(required)**
- `traceId` — string — Trace recording the session in wilma-traces — every turn, model call and tool execution the agent ran. Read it with the wilma-traces GetTrace operation, or tail it live with StreamTrace next to the event stream `startIndex` addresses. One id for the whole session, not for this turn: the handle a later ContinueSession returns names the same trace StartSession opened, and each turn appends to it. The trace row is written once the turn's first step completes, so GetTrace may report NotFound in the moment right after this call returns. Absent when the session's trace is not the caller's to read — a session served by a Wildix built-in agent is recorded for Wildix rather than for the tenant. _(minLen=1; maxLen=128)_

**`CopilotAvailability`**

_Whether Copilot (real-time agent-assist, wildix.wilma.copilot) may assist the user, resolved from the company's live profiles and their `audience`. Entries that need a conversation to decide (queue, service, trunk, agent) and department entries (PBX department ids, which no directory here exposes) count as matching, except in the `before` stage, where the user is the one who opens Copilot and conversation entries say nothing. A profile limited to the `before` stage enables Copilot but covers no channel._

- `enabled` — boolean **(required)** — Whether at least one live profile may assist the user.
- `channels` — array — Conversation channels covered by the profiles that may assist the user. Empty when `enabled` is false.
  - _array of_ `CopilotChannel`
- `stages` — array — Stages covered by the profiles that may assist the user. `before` means Copilot can be opened without a call, chat or conference. Empty when `enabled` is false.
  - _array of_ `CopilotStage`
- `reason` — string — Why Copilot is or is not available to the user. _(enum: `available`, `no_live_profile`, `not_in_audience`)_

**`CopilotAvailabilityReason`**

_Why Copilot is or is not available to the user._

- string _(enum: `available`, `no_live_profile`, `not_in_audience`)_

**`CopilotChannel`**

_The kind of conversation a copilot resource applies to. Singular members and no wildcard, unlike the `calls | chats | any` field this replaces - and `conference` is nameable for the first time. Note that this is the *conversation* channel, not the Wilma runtime channel (`assistant` / `chat` / `voice`) and not the messaging service a chat arrived on (which is `chat.service`)._

- string _(enum: `call`, `conference`, `chat`)_

**`CopilotStage`**

_Where in a conversation's life a copilot resource applies. `before` is the pre-conversation session copilot opens from a client lookup (`Open` in `wildix.wilma.copilot.sessions`): a customer is on screen and no call, conference or chat exists yet. `during` is a live conversation. `after` is everything from the conversation ending onwards - wrap-up, and the post-conversation summary that carries CSAT and topics. A conversation that has not started has no channel and no queue, which is the one rule the other two members of this triple follow from: see `CopilotChannelList` and `CopilotAudienceKind`._

- string _(enum: `before`, `during`, `after`)_

**`DownloadAttachmentResponseContent`**

- `url` — string **(required)** — Presigned download URL. Short-lived: fetch the content right away rather than storing the URL.
- `attachment` — Attachment **(required)** — An input file supplied with session input and included with a user message. Content lives in object storage; download via the owning channel's Attachments API. `contentType`, `size` and `thumbnailUrl` describe the stored content and are therefore absent until the upload has completed.
  - `id` — string **(required)** — Nano-id attachment identifier (12 characters). _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
  - `name` — string **(required)** — Filename shown to the user. Characters storage cannot represent are replaced with underscores. _(minLen=1; maxLen=255)_
  - `contentType` — string — MIME type recorded by storage from the uploaded content, e.g. 'application/pdf'. Absent until the upload completes.
  - `size` — number — Size in bytes recorded by storage from the uploaded content. Absent until the upload completes.
  - `thumbnailUrl` — string — URL of a generated preview image, for rendering a thumbnail without downloading the file. Best-effort: absent until the upload completes, and for content no preview can be generated from.
  - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GetAgentResponseContent`**

- `agent` — AgentInfo **(required)** — What a client needs to render an agent, and nothing more: AgentInfo is the end-user view of an agent, served by the channel runtimes (e.g. GetAgent / GetSettings on wilma-assistant) to callers who must not see instructions, capabilities or access rules. Everything here is safe to show to whoever can use the agent.
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
        - _(nesting depth limit — see `AssistantQuickCommand` in the Schemas appendix)_
    - `placeholder` — string — Placeholder text in the composer, e.g. 'Ask about an account…'. Defaults to the client's own placeholder when omitted. _(minLen=1; maxLen=100)_
  - `latestVersion` — number — Published agent version number. Monotonic within an agent's version history, starting at 1. _(min=1)_

**`GetAttachmentResponseContent`**

- `attachment` — Attachment **(required)** — An input file supplied with session input and included with a user message. Content lives in object storage; download via the owning channel's Attachments API. `contentType`, `size` and `thumbnailUrl` describe the stored content and are therefore absent until the upload has completed.
  - `id` — string **(required)** — Nano-id attachment identifier (12 characters). _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
  - `name` — string **(required)** — Filename shown to the user. Characters storage cannot represent are replaced with underscores. _(minLen=1; maxLen=255)_
  - `contentType` — string — MIME type recorded by storage from the uploaded content, e.g. 'application/pdf'. Absent until the upload completes.
  - `size` — number — Size in bytes recorded by storage from the uploaded content. Absent until the upload completes.
  - `thumbnailUrl` — string — URL of a generated preview image, for rendering a thumbnail without downloading the file. Best-effort: absent until the upload completes, and for content no preview can be generated from.
  - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.

**`GetSessionEventsResponseContent`**

- `events` — array **(required)**
  - _array of_ `AssistantSessionEvent`
    - _oneOf_ — exactly one of:
      - **`sessionStarted`**
        - `sessionStarted` — SessionStartedEvent **(required)** — Emitted once as the very first event of a session, when it is created. Confirms the session id and the agent the session is bound to.
          - _(nesting depth limit — see `SessionStartedEvent` in the Schemas appendix)_
      - **`sessionIdle`**
        - `sessionIdle` — SessionIdleEvent **(required)** — Terminal event of a successful turn: the session is idle and ready for the next turn.
          - _(nesting depth limit — see `SessionIdleEvent` in the Schemas appendix)_
      - **`sessionStopped`**
        - `sessionStopped` — SessionStoppedEvent **(required)** — Terminal event emitted when the active turn was cancelled via the channel's stop operation.
          - _(nesting depth limit — see `SessionStoppedEvent` in the Schemas appendix)_
      - **`sessionTerminated`**
        - `sessionTerminated` — SessionTerminatedEvent **(required)** — Terminal event emitted when the platform ended the session rather than let it continue: the session is in `terminated` status. Distinct from SessionStoppedEvent, which records a user or operator asking to stop — folding the two together would leave a refused session indistinguishable from a clean finish in every completion-rate report. On voice the call is hung up as this is emitted; on the other channels there is nothing to hang up and termination is the status alone — history is kept, and the session simply accepts no further turns.
          - _(nesting depth limit — see `SessionTerminatedEvent` in the Schemas appendix)_
      - **`sessionFailed`**
        - `sessionFailed` — SessionFailedEvent **(required)** — Terminal event emitted after TurnFailedEvent: the session is in `failed` status. A new turn starts from the last consistent snapshot.
          - _(nesting depth limit — see `SessionFailedEvent` in the Schemas appendix)_
      - **`turnStarted`**
        - `turnStarted` — TurnStartedEvent **(required)** — Emitted when a turn begins executing. All subsequent events up to the matching TurnCompletedEvent/TurnFailedEvent belong to this turn.
          - _(nesting depth limit — see `TurnStartedEvent` in the Schemas appendix)_
      - **`turnCompleted`**
        - `turnCompleted` — TurnCompletedEvent **(required)** — Emitted when a turn finishes successfully, with aggregate token usage for the turn. Followed by SessionIdleEvent.
          - _(nesting depth limit — see `TurnCompletedEvent` in the Schemas appendix)_
      - **`turnFailed`**
        - `turnFailed` — TurnFailedEvent **(required)** — Emitted when a turn fails with an unrecoverable error. Followed by SessionFailedEvent.
          - _(nesting depth limit — see `TurnFailedEvent` in the Schemas appendix)_
      - **`messageReceived`**
        - `messageReceived` — MessageReceivedEvent **(required)** — Emitted right after TurnStartedEvent with the user message that triggered the turn, so a reconnecting client can render the conversation without a separate history fetch.
          - _(nesting depth limit — see `MessageReceivedEvent` in the Schemas appendix)_
      - **`messageAppended`**
        - `messageAppended` — MessageAppendedEvent **(required)** — Emitted for every assistant text token chunk. High frequency; drives live rendering of the reply.
          - _(nesting depth limit — see `MessageAppendedEvent` in the Schemas appendix)_
      - **`messageCompleted`**
        - `messageCompleted` — MessageCompletedEvent **(required)** — Emitted once per step when the assistant message text is complete.
          - _(nesting depth limit — see `MessageCompletedEvent` in the Schemas appendix)_
      - **`stepStarted`**
        - `stepStarted` — StepStartedEvent **(required)** — Emitted each time the model starts a new inference step within a turn (a turn spans multiple steps when the model calls tools).
          - _(nesting depth limit — see `StepStartedEvent` in the Schemas appendix)_
      - **`stepCompleted`**
        - `stepCompleted` — StepCompletedEvent **(required)** — Emitted when an inference step finishes, with token usage for the step when the provider reports it.
          - _(nesting depth limit — see `StepCompletedEvent` in the Schemas appendix)_
      - **`reasoningDelta`**
        - `reasoningDelta` — ReasoningDeltaEvent **(required)** — Emitted for every reasoning (thinking) token chunk the model produces, when the selected model exposes reasoning. High frequency; intended for live typing indicators.
          - _(nesting depth limit — see `ReasoningDeltaEvent` in the Schemas appendix)_
      - **`reasoningCompleted`**
        - `reasoningCompleted` — ReasoningCompletedEvent **(required)** — Emitted once per step after the model finishes its reasoning block, carrying the complete reasoning text.
          - _(nesting depth limit — see `ReasoningCompletedEvent` in the Schemas appendix)_
      - **`invocationStarted`**
        - `invocationStarted` — InvocationStartedEvent **(required)** — Emitted when the model begins one tool invocation, before its input is complete. Every invocation starts here, regardless of how it is fulfilled or whether it suspends the turn. Carries the routing facts needed to render it — who fulfils it, whether the turn suspends, where to surface it, whether the input streams — so a client holding no tool registry (a replay, a shared session, an inspector) still renders correctly.
          - _(nesting depth limit — see `InvocationStartedEvent` in the Schemas appendix)_
      - **`invocationDelta`**
        - `invocationDelta` — InvocationDeltaEvent **(required)** — Emitted for each fragment of an invocation's input as the model writes it, when the tool opted into streamed input. The payload is raw partial JSON text exactly as the model emits it; clients parse it incrementally to render an invocation whose input is itself content — a drafted email, a chart spec, a shared document — while it is being written. High frequency.
          - _(nesting depth limit — see `InvocationDeltaEvent` in the Schemas appendix)_
      - **`invocationInputCompleted`**
        - `invocationInputCompleted` — InvocationInputCompletedEvent **(required)** — Emitted once per invocation when its input is complete and parsed. Always emitted, whether or not the input streamed.
          - _(nesting depth limit — see `InvocationInputCompletedEvent` in the Schemas appendix)_
      - **`invocationResult`**
        - `invocationResult` — InvocationResultEvent **(required)** — Emitted when an invocation is resolved, however that happened: a server tool finishing, a caller returning a client tool's result on resume, a person answering a question or ruling on an approval, or the runtime supplying a `synthetic` tool's result. Emitted for every invocation without exception, so replaying the log from index 0 reconstructs the same state as watching it live.
          - _(nesting depth limit — see `InvocationResultEvent` in the Schemas appendix)_
      - **`taskStarted`**
        - `taskStarted` — TaskStartedEvent **(required)** — Emitted when the agent delegates a subtask to a task execution: the `delegate` tool or an agent-call capability. Events emitted inside the task are re-published on the session stream with `origin` set to this task, until the matching TaskCompletedEvent.
          - _(nesting depth limit — see `TaskStartedEvent` in the Schemas appendix)_
      - **`taskCompleted`**
        - `taskCompleted` — TaskCompletedEvent **(required)** — Emitted when a delegated task execution finishes, carrying its final answer as returned to the parent agent.
          - _(nesting depth limit — see `TaskCompletedEvent` in the Schemas appendix)_
      - **`workflowStepEntered`**
        - `workflowStepEntered` — WorkflowStepEnteredEvent **(required)** — Emitted when the workflow cursor arrives at a step, before the step runs — so every later event in the log belongs to the step most recently entered. The first is the graph's `entry` step; the last is a terminal step, which is where the session left the graph.
          - _(nesting depth limit — see `WorkflowStepEnteredEvent` in the Schemas appendix)_
      - **`workflowTransition`**
        - `workflowTransition` — WorkflowTransitionEvent **(required)** — Emitted when a transition is taken, naming the exit and what decided it. Not emitted on a terminal step, which has no exits — a session that ended inside the graph is read from the last WorkflowStepEnteredEvent — and not emitted when a conversation step's conditions all stay false, which is the step simply continuing.
          - _(nesting depth limit — see `WorkflowTransitionEvent` in the Schemas appendix)_
      - **`workflowMoveRefused`**
        - `workflowMoveRefused` — WorkflowMoveRefusedEvent **(required)** — Emitted when the model asks to move somewhere the live step does not declare as an exit. The runtime refuses, names the legal exits, and the session carries on from the same step, so this is not a failure of the turn: it is the record of what callers keep reaching for and the graph does not offer. Aggregated per step, it is the shortest route to the exit a graph is missing.
          - _(nesting depth limit — see `WorkflowMoveRefusedEvent` in the Schemas appendix)_
      - **`workflowVariablesWritten`**
        - `workflowVariablesWritten` — WorkflowVariablesWrittenEvent **(required)** — Emitted when workflow variables are written: a `variables` step's assignments, or an action step capturing its result into `output`. The only record of the state `expression` conditions branch on and handlebars resolve against, so replaying the log from index 0 reconstructs the same variables the runtime had.
          - _(nesting depth limit — see `WorkflowVariablesWrittenEvent` in the Schemas appendix)_
      - **`guardrailTripped`**
        - `guardrailTripped` — GuardrailTrippedEvent **(required)** — Emitted when a check trips, including when its action is `observe` and the turn proceeds untouched — that is what makes observe mode a way to tune a guardrail against real traffic rather than a switched-off check.
          - _(nesting depth limit — see `GuardrailTrippedEvent` in the Schemas appendix)_
      - **`guardrailFailed`**
        - `guardrailFailed` — GuardrailFailedEvent **(required)** — Emitted when the checker itself errored or timed out. Carries the errorMode decision, so a reader can tell a turn that was screened and found clean from one that was never screened — without this event a fail-open guardrail would be indistinguishable from a guardrail that found nothing.
          - _(nesting depth limit — see `GuardrailFailedEvent` in the Schemas appendix)_
      - **`sandboxStarted`**
        - `sandboxStarted` — SandboxStartedEvent **(required)** — Emitted when the turn is attached to its sandbox, the first time a sandbox-backed tool is used in the turn. A session reuses one sandbox across turns whenever possible.
          - _(nesting depth limit — see `SandboxStartedEvent` in the Schemas appendix)_
      - **`sandboxFailed`**
        - `sandboxFailed` — SandboxFailedEvent **(required)** — Emitted when acquiring the sandbox fails; the turn then fails with the same cause. Provides sandbox-level observability distinct from the generic TurnFailedEvent.
          - _(nesting depth limit — see `SandboxFailedEvent` in the Schemas appendix)_
      - **`artifactShared`**
        - `artifactShared` — ArtifactSharedEvent **(required)** — Emitted when the agent shares an artifact via the `share_artifact` tool, after the revision has been uploaded. Carries the file list and card metadata; the viewer reads content URLs and sharing from the wilma-artifacts service. Sharing the same artifact again publishes a new `revision` under the same `artifactId` and emits this event again.
          - _(nesting depth limit — see `ArtifactSharedEvent` in the Schemas appendix)_
      - **`compactionStarted`**
        - `compactionStarted` — CompactionStartedEvent **(required)** — Emitted before a turn when the conversation history exceeds the model context budget and is being summarized. The turn starts after CompactionCompletedEvent.
          - _(nesting depth limit — see `CompactionStartedEvent` in the Schemas appendix)_
      - **`compactionCompleted`**
        - `compactionCompleted` — CompactionCompletedEvent **(required)** — Emitted when history compaction finishes and the turn proceeds with the summarized history.
          - _(nesting depth limit — see `CompactionCompletedEvent` in the Schemas appendix)_
      - **`steerReceived`**
        - `steerReceived` — SteerReceivedEvent **(required)** — Emitted when a steer request is accepted for the turn already running, before it reaches the model. A turn can therefore carry more than one user message; build transcripts from event order, not from turn structure. This is the only record of the steering text: a turn the steer was promoted into starts with TurnStartedEvent but emits no MessageReceivedEvent, so the message is never recorded twice.
          - _(nesting depth limit — see `SteerReceivedEvent` in the Schemas appendix)_
      - **`steerApplied`**
        - `steerApplied` — SteerAppliedEvent **(required)** — Emitted when an accepted steer has reached the model, naming the turn and step boundary where it took effect. The gap between SteerReceivedEvent and this event is user-visible, so a client can show the steering message as pending until it lands. A steer never interrupts a tool call that is already running. `turn` differs from the SteerReceivedEvent's `turn` when the steer was promoted: the running turn finished before a boundary arrived, so the message became the input of the following turn.
          - _(nesting depth limit — see `SteerAppliedEvent` in the Schemas appendix)_
      - **`inputRequested`**
        - `inputRequested` — InputRequestedEvent **(required)** — Emitted when the turn cannot proceed without the caller: client-fulfilled tools, `ask_question`, or approval-gated tools. Each request references an invocation the stream has already announced — this event routes, it does not introduce calls. Answer through the channel's resume operation using the same `pendingId`; each answered invocation then emits its own InvocationResultEvent. Followed by SessionWaitingEvent.
          - _(nesting depth limit — see `InputRequestedEvent` in the Schemas appendix)_
      - **`sessionWaiting`**
        - `sessionWaiting` — SessionWaitingEvent **(required)** — Terminal event of a turn that paused for caller input. The session stays in `waiting` status until resumed with the `pendingId`.
          - _(nesting depth limit — see `SessionWaitingEvent` in the Schemas appendix)_
- `nextStartIndex` — number — Present when more events exist; pass it as `startIndex` of the next call.

**`GetSessionResponseContent`**

- `meta` — SessionMeta **(required)**
  - `sessionId` — string **(required)** _(minLen=1; maxLen=128)_
  - `agentId` — string _(minLen=12; maxLen=12)_
  - `traceId` — string — Opaque trace identifier generated by the tracing runtime. _(minLen=1; maxLen=128)_
  - `agentVersion` — number — Published agent version serving this session, selected at session start. _(min=1)_
  - `agentDraft` — boolean — True when the session runs the agent's mutable draft (agentDraft on StartSession).
  - `agentDraftRevision` — number — Draft revision loaded at session start when agentDraft is true; correlates a run with the exact draft state.
  - `model` — string — Effective model resolved at session start (after 'default' resolution), e.g. 'google://gemini-3-flash-preview'.
  - `skillVersions` — array — Skill versions resolved at session start, one entry per attached skill (whether pinned or resolved via the skill's alias).
    - _array of_ `SessionSkillVersion`
      - `skillId` — string **(required)** _(minLen=12; maxLen=12)_
      - `version` — number **(required)** — Published skill version number. Monotonic within a skill's version history, starting at 1. _(min=1)_
  - `visibility` — string — Whether a session shows up in the user's assistant history. Integration-driven sessions (e.g. copilot asset generation) are started `hidden` so they do not pollute the history while staying reachable by id. _(enum: `listed`, `hidden`)_
  - `target` — string — What the session belongs to, as supplied on StartSession. Present for sessions started from a client surface or integration that identified itself. _(minLen=1; maxLen=1024)_
  - `metadata` — any — Host-defined metadata supplied on StartSession, returned verbatim.
  - `status` — string **(required)** _(enum: `running`, `idle`, `waiting`, `stopped`, `failed`, `terminated`)_
  - `version` — number **(required)** — Monotonic session state revision.
  - `title` — string
  - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `eventCount` — number **(required)**
- `status` — string **(required)** _(enum: `running`, `idle`, `waiting`, `stopped`, `failed`, `terminated`)_
- `history` — array **(required)**
  - _array of_ `any`
- `state` — any **(required)**
- `mentions` — array — The session's current mentions. _(maxItems=20)_
  - _array of_ `Mention`
    - _oneOf_ — exactly one of:
      - **`reference`**
        - `reference` — MentionReference **(required)** — A resource selected as agent context, identified by its canonical URI, e.g. `wilma://insights/calls/{callId}/flows/{flowIndex}`. It is read with the permissions of the session or task it is attached to; the URI grants no access by itself.
          - _(nesting depth limit — see `MentionReference` in the Schemas appendix)_

**`GetSettingsResponseContent`**

- `style` — UserStyleSettings — How the assistant should communicate with this user.
  - `tone` — string _(minLen=1; maxLen=64)_
- `about` — UserAboutSettings — Background the assistant may use to personalise replies for this user.
  - `description` — string _(minLen=1; maxLen=2000)_
- `agents` — array — Agents available to the user for selection in the assistant UI.
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
- `skills` — array — Skills available to the user. Manage skill definitions in wilma-skills.
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
- `skillsSettings` — UserSkillsSettings — Per-user skill preferences. Skills the user has disabled are omitted from the effective skill set at runtime.
  - `disabled` — array
    - _array of_ `string`
- `connectors` — array — Connectors configured for the company that this deployment can execute, one per instance, with this user's authorization and enablement state. Filter by an agent's `connectorIds` for the agent in use. Absent when the connector services could not be answered for: the rest of the settings still apply.
  - _array of_ `AvailableConnector`
    - `id` — string **(required)** — Connector instance id — the id an agent's capabilities and the user's `disabled` preference refer to. For an MCP server, the id of the Tool that registers it. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `key` — string **(required)** — Connector definition key, e.g. `salesforce`. Several instances may share one. For an MCP server, its provider key (`mcp_…`), which is also what AuthorizeConnector takes. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
    - `kind` — string — The kind of thing an AvailableConnector entry stands for. _(enum: `connector`, `mcp_server`)_
    - `grant` — union **(required)** — Coarse permission grant for a configured connector. The service computes the effective, server-enforced tool set by filtering the pinned definition's tools with this grant (using each tool's `ConnectorToolAccess`), and requests only the scopes the grant implies at connection time.
      - _oneOf_ — exactly one of:
        - **`read`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`readWrite`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`all`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`tools`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `title` — string **(required)**
    - `icon` — string
    - `provider` — string **(required)** — Provider the connector authenticates against, e.g. `salesforce`. A user's consent is per provider, so connecting one instance connects every instance on the same provider.
    - `mode` — string **(required)** — Supported credential resolution mode. Mirrors wilma-secrets `ConnectionType`. _(enum: `shared`, `user`)_
    - `authorization` — string **(required)** — The current user's authorization status for a connector. Drives the Connect button: the connector is usable when NOT_REQUIRED or CONNECTED, and prompts the user to connect when NOT_CONNECTED or NEEDS_RECONNECT. _(enum: `not_required`, `not_connected`, `connected`, `needs_reconnect`)_
    - `enabled` — boolean **(required)** — Effective enablement for this user, after applying their disabled preferences.
- `connectorsSettings` — UserConnectorsSettings — Per-user connector preferences, by connector instance id. Connectors the user has disabled are removed from the effective set at runtime, even when an admin enabled them.
  - `disabled` — array
    - _array of_ `string`
- `copilotSettings` — UserCopilotSettings — Per-user Copilot settings. Resolved by the service; PatchSettings does not change them.
  - `availability` — CopilotAvailability — Whether Copilot (real-time agent-assist, wildix.wilma.copilot) may assist the user, resolved from the company's live profiles and their `audience`. Entries that need a conversation to decide (queue, service, trunk, agent) and department entries (PBX department ids, which no directory here exposes) count as matching, except in the `before` stage, where the user is the one who opens Copilot and conversation entries say nothing. A profile limited to the `before` stage enables Copilot but covers no channel.
    - `enabled` — boolean **(required)** — Whether at least one live profile may assist the user.
    - `channels` — array — Conversation channels covered by the profiles that may assist the user. Empty when `enabled` is false.
      - _array of_ `CopilotChannel`
    - `stages` — array — Stages covered by the profiles that may assist the user. `before` means Copilot can be opened without a call, chat or conference. Empty when `enabled` is false.
      - _array of_ `CopilotStage`
    - `reason` — string — Why Copilot is or is not available to the user. _(enum: `available`, `no_live_profile`, `not_in_audience`)_

**`GuardrailFailedEvent`**

_Emitted when the checker itself errored or timed out. Carries the errorMode decision, so a reader can tell a turn that was screened and found clean from one that was never screened — without this event a fail-open guardrail would be indistinguishable from a guardrail that found nothing._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `errorMode` — string **(required)** — What happens when the checker itself errors or times out. OPEN lets the turn through unscreened and records GuardrailFailedEvent, so an unscreened turn is a fact in the log rather than an absence; CLOSED refuses it. Defaults to OPEN: an agent that stops answering because a small model had a bad minute is a worse and far likelier outage than the rare turn that goes unscreened. Background tasks, where nobody is waiting and a retry is free, are the case for CLOSED. _(enum: `open`, `closed`)_
- `proceeded` — boolean **(required)** — True when the turn was allowed through unscreened (`errorMode: open`), false when it was refused.
- `reason` — string — Why the checker failed — a timeout, a provider error.

**`GuardrailTrippedEvent`**

_Emitted when a check trips, including when its action is `observe` and the turn proceeds untouched — that is what makes observe mode a way to tune a guardrail against real traffic rather than a switched-off check._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `check` — string **(required)** — The check's `name` in the agent definition. _(minLen=1; maxLen=64)_
- `preset` — string — A prebuilt check. Each preset is a platform-maintained prompt shipped in code and versioned with the platform, not a tenant row — so a support question about what a preset caught has one answer. A preset check is otherwise an ordinary AgentGuardrailCheck: its sensitivity and action are the tenant's to set, and `notes` narrows its prompt without replacing it. _(enum: `jailbreak`, `offTopic`, `abuse`, `harmful`, `selfHarm`, `pii`, `secrets`, `regulatedAdvice`)_
- `confidence` — string **(required)** — How much confidence a verdict needs before it counts as tripped. The checker reports a confidence per check and this is the threshold against it, so raising sensitivity catches more and costs more false positives without changing the prompt or the model: `low` trips only on high confidence, `medium` on high and medium, `high` on anything but a clear pass. Defaults to MEDIUM. _(enum: `low`, `medium`, `high`)_
- `action` — string **(required)** — The action members by name, for reporting what actually ran. Session events carry this rather than AgentGuardrailAction because an event reports a decision, not a configuration. _(enum: `observe`, `redact`, `block`, `end`)_
- `reason` — string — The checker's own account of why it tripped. Recorded for whoever tunes the guardrail, and never shown to the caller: telling someone which check caught them is a free oracle for the next attempt.

**`InputRequestedEvent`**

_Emitted when the turn cannot proceed without the caller: client-fulfilled tools, `ask_question`, or approval-gated tools. Each request references an invocation the stream has already announced — this event routes, it does not introduce calls. Answer through the channel's resume operation using the same `pendingId`; each answered invocation then emits its own InvocationResultEvent. Followed by SessionWaitingEvent._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `pendingId` — string **(required)**
- `requests` — array **(required)**
  - _array of_ `SessionPendingInput`
    - `callId` — string **(required)** — Id of the invocation, matching an InvocationStartedEvent in this turn.
    - `kind` — string **(required)** _(enum: `client`, `question`, `approval`)_

**`InvocationDeltaEvent`**

_Emitted for each fragment of an invocation's input as the model writes it, when the tool opted into streamed input. The payload is raw partial JSON text exactly as the model emits it; clients parse it incrementally to render an invocation whose input is itself content — a drafted email, a chart spec, a shared document — while it is being written. High frequency._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `step` — number **(required)**
- `callId` — string **(required)**
- `delta` — string **(required)** — The new fragment of raw JSON input text.
- `soFar` — string **(required)** — The raw JSON input text accumulated so far in this invocation, so late subscribers need not replay every delta. Being a prefix, it is not necessarily valid JSON on its own.

**`InvocationInputCompletedEvent`**

_Emitted once per invocation when its input is complete and parsed. Always emitted, whether or not the input streamed._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `step` — number **(required)**
- `callId` — string **(required)**
- `input` — any **(required)**

**`InvocationResultEvent`**

_Emitted when an invocation is resolved, however that happened: a server tool finishing, a caller returning a client tool's result on resume, a person answering a question or ruling on an approval, or the runtime supplying a `synthetic` tool's result. Emitted for every invocation without exception, so replaying the log from index 0 reconstructs the same state as watching it live._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `step` — number **(required)**
- `callId` — string **(required)** — Id of the invocation this result answers, matching an InvocationStartedEvent.
- `toolName` — string **(required)**
- `toolId` — string — The wilma-tools Tool that executed, echoed from InvocationStartedEvent. Absent for invocations that are not backed by a shared Tool. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
- `toolVersion` — number — Published tool version that executed, when `toolId` is set. _(min=1)_
- `status` — string **(required)** _(enum: `completed`, `failed`)_
- `resolvedBy` — string **(required)** — Who supplied the result recorded by an InvocationResultEvent. _(enum: `server`, `client`, `user`)_
- `output` — any
- `error` — string — Present when status is `failed`.

**`InvocationStartedEvent`**

_Emitted when the model begins one tool invocation, before its input is complete. Every invocation starts here, regardless of how it is fulfilled or whether it suspends the turn. Carries the routing facts needed to render it — who fulfils it, whether the turn suspends, where to surface it, whether the input streams — so a client holding no tool registry (a replay, a shared session, an inspector) still renders correctly._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `step` — number **(required)**
- `callId` — string **(required)** — Stable id of this invocation, referenced by every later event about it.
- `toolName` — string **(required)**
- `toolId` — string — The wilma-tools Tool backing this invocation. Absent for built-in tools, connector meta-tools and other capabilities that are not shared Tools. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
- `toolVersion` — number — Published tool version the model was offered, when `toolId` is set. Records which input schema the invocation was written against. _(min=1)_
- `fulfilment` — string **(required)** — Who produces an invocation's result. `server` tools execute inside the agent runtime. `client` tools are executed by the caller, so the turn suspends until it answers. `synthetic` tools never execute at all — they exist to put something on screen, and the runtime supplies their result itself, so the turn does not suspend. _(enum: `server`, `client`, `synthetic`)_
- `gate` — string **(required)** — Whether the turn suspends on an invocation, and for what. Orthogonal to fulfilment: a `server` tool may be gated on a user decision (an approval), and a `synthetic` tool may be ungated (render and continue) or gated (an editable draft awaiting confirmation). _(enum: `none`, `result`, `decision`)_
- `surface` — string **(required)** — Where a client should surface an invocation. Affects placement only, never behaviour. _(enum: `hidden`, `activity`, `content`)_
- `stream` — boolean **(required)** — True when the input arrives as InvocationDeltaEvent chunks ahead of InvocationInputCompletedEvent. Opt-in per tool, so tools with small inputs cost nothing.

**`ListConnectorsResponseContent`**

- `connectors` — array **(required)**
  - _array of_ `AvailableConnector`
    - `id` — string **(required)** — Connector instance id — the id an agent's capabilities and the user's `disabled` preference refer to. For an MCP server, the id of the Tool that registers it. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `key` — string **(required)** — Connector definition key, e.g. `salesforce`. Several instances may share one. For an MCP server, its provider key (`mcp_…`), which is also what AuthorizeConnector takes. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
    - `kind` — string — The kind of thing an AvailableConnector entry stands for. _(enum: `connector`, `mcp_server`)_
    - `grant` — union **(required)** — Coarse permission grant for a configured connector. The service computes the effective, server-enforced tool set by filtering the pinned definition's tools with this grant (using each tool's `ConnectorToolAccess`), and requests only the scopes the grant implies at connection time.
      - _oneOf_ — exactly one of:
        - **`read`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`readWrite`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`all`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`tools`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `title` — string **(required)**
    - `icon` — string
    - `provider` — string **(required)** — Provider the connector authenticates against, e.g. `salesforce`. A user's consent is per provider, so connecting one instance connects every instance on the same provider.
    - `mode` — string **(required)** — Supported credential resolution mode. Mirrors wilma-secrets `ConnectionType`. _(enum: `shared`, `user`)_
    - `authorization` — string **(required)** — The current user's authorization status for a connector. Drives the Connect button: the connector is usable when NOT_REQUIRED or CONNECTED, and prompts the user to connect when NOT_CONNECTED or NEEDS_RECONNECT. _(enum: `not_required`, `not_connected`, `connected`, `needs_reconnect`)_
    - `enabled` — boolean **(required)** — Effective enablement for this user, after applying their disabled preferences.

**`ListSessionsResponseContent`**

- `sessions` — array **(required)**
  - _array of_ `SessionMeta`
    - `sessionId` — string **(required)** _(minLen=1; maxLen=128)_
    - `agentId` — string _(minLen=12; maxLen=12)_
    - `traceId` — string — Opaque trace identifier generated by the tracing runtime. _(minLen=1; maxLen=128)_
    - `agentVersion` — number — Published agent version serving this session, selected at session start. _(min=1)_
    - `agentDraft` — boolean — True when the session runs the agent's mutable draft (agentDraft on StartSession).
    - `agentDraftRevision` — number — Draft revision loaded at session start when agentDraft is true; correlates a run with the exact draft state.
    - `model` — string — Effective model resolved at session start (after 'default' resolution), e.g. 'google://gemini-3-flash-preview'.
    - `skillVersions` — array — Skill versions resolved at session start, one entry per attached skill (whether pinned or resolved via the skill's alias).
      - _array of_ `SessionSkillVersion`
        - _(nesting depth limit — see `SessionSkillVersion` in the Schemas appendix)_
    - `visibility` — string — Whether a session shows up in the user's assistant history. Integration-driven sessions (e.g. copilot asset generation) are started `hidden` so they do not pollute the history while staying reachable by id. _(enum: `listed`, `hidden`)_
    - `target` — string — What the session belongs to, as supplied on StartSession. Present for sessions started from a client surface or integration that identified itself. _(minLen=1; maxLen=1024)_
    - `metadata` — any — Host-defined metadata supplied on StartSession, returned verbatim.
    - `status` — string **(required)** _(enum: `running`, `idle`, `waiting`, `stopped`, `failed`, `terminated`)_
    - `version` — number **(required)** — Monotonic session state revision.
    - `title` — string
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `eventCount` — number **(required)**
- `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_

**`Mention`**

_Something attached to a message as agent context. A union, so a new kind of context is a new member rather than a change to every operation that carries mentions._

- _oneOf_ — exactly one of:
  - **`reference`**
    - `reference` — MentionReference **(required)** — A resource selected as agent context, identified by its canonical URI, e.g. `wilma://insights/calls/{callId}/flows/{flowIndex}`. It is read with the permissions of the session or task it is attached to; the URI grants no access by itself.
      - `uri` — string **(required)** — Canonical URI identifying one entity on the Wilma platform, e.g. 'wilma://agents/UXDT1W9fI3sj' or 'wilma://skills/aB3dE5fG7hJ9'. The path names the owning service and entity kind. Opaque to the contracts that carry it; non-Wilma schemes (records of external systems) fit the same shape. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
      - `label` — string — Display name of the mention chip. The model sees it only to name a mention that could not be read or was removed. _(maxLen=256)_

**`MentionReference`**

_A resource selected as agent context, identified by its canonical URI, e.g. `wilma://insights/calls/{callId}/flows/{flowIndex}`. It is read with the permissions of the session or task it is attached to; the URI grants no access by itself._

- `uri` — string **(required)** — Canonical URI identifying one entity on the Wilma platform, e.g. 'wilma://agents/UXDT1W9fI3sj' or 'wilma://skills/aB3dE5fG7hJ9'. The path names the owning service and entity kind. Opaque to the contracts that carry it; non-Wilma schemes (records of external systems) fit the same shape. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
- `label` — string — Display name of the mention chip. The model sees it only to name a mention that could not be read or was removed. _(maxLen=256)_

**`MessageAppendedEvent`**

_Emitted for every assistant text token chunk. High frequency; drives live rendering of the reply._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `step` — number **(required)**
- `delta` — string **(required)** — The new text fragment.
- `soFar` — string **(required)** — The full assistant text accumulated so far in this step.

**`MessageCompletedEvent`**

_Emitted once per step when the assistant message text is complete._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `step` — number **(required)**
- `text` — string **(required)**
- `finishReason` — string **(required)** — Model finish reason for the step, e.g. `stop` or `tool-calls`.

**`MessageReceivedEvent`**

_Emitted right after TurnStartedEvent with the user message that triggered the turn, so a reconnecting client can render the conversation without a separate history fetch._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `message` — string **(required)**
- `attachments` — array — Input files supplied with this message, as stored — enough to render the attachment alongside the message (name, type, size, thumbnail) without a separate Attachments call. Absent when the turn carried no files.
  - _array of_ `Attachment`
    - `id` — string **(required)** — Nano-id attachment identifier (12 characters). _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
    - `name` — string **(required)** — Filename shown to the user. Characters storage cannot represent are replaced with underscores. _(minLen=1; maxLen=255)_
    - `contentType` — string — MIME type recorded by storage from the uploaded content, e.g. 'application/pdf'. Absent until the upload completes.
    - `size` — number — Size in bytes recorded by storage from the uploaded content. Absent until the upload completes.
    - `thumbnailUrl` — string — URL of a generated preview image, for rendering a thumbnail without downloading the file. Best-effort: absent until the upload completes, and for content no preview can be generated from.
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.

**`NotFoundExceptionResponseContent`**

- `message` — string **(required)** _(default=Not found)_

**`PatchSettingsRequestContent`**

- `style` — UserStyleSettings — How the assistant should communicate with this user.
  - `tone` — string _(minLen=1; maxLen=64)_
- `about` — UserAboutSettings — Background the assistant may use to personalise replies for this user.
  - `description` — string _(minLen=1; maxLen=2000)_
- `skills` — UserSkillsSettings — Per-user skill preferences. Skills the user has disabled are omitted from the effective skill set at runtime.
  - `disabled` — array
    - _array of_ `string`
- `connectors` — UserConnectorsSettings — Per-user connector preferences, by connector instance id. Connectors the user has disabled are removed from the effective set at runtime, even when an admin enabled them.
  - `disabled` — array
    - _array of_ `string`

**`PatchSettingsResponseContent`**

- `style` — UserStyleSettings — How the assistant should communicate with this user.
  - `tone` — string _(minLen=1; maxLen=64)_
- `about` — UserAboutSettings — Background the assistant may use to personalise replies for this user.
  - `description` — string _(minLen=1; maxLen=2000)_
- `agents` — array
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
- `skills` — array
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
- `skillsSettings` — UserSkillsSettings — Per-user skill preferences. Skills the user has disabled are omitted from the effective skill set at runtime.
  - `disabled` — array
    - _array of_ `string`
- `connectors` — array — Connectors configured for the company that this deployment can execute, one per instance, with this user's authorization and enablement state. Filter by an agent's `connectorIds` for the agent in use. Absent when the connector services could not be answered for: the rest of the settings still apply.
  - _array of_ `AvailableConnector`
    - `id` — string **(required)** — Connector instance id — the id an agent's capabilities and the user's `disabled` preference refer to. For an MCP server, the id of the Tool that registers it. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `key` — string **(required)** — Connector definition key, e.g. `salesforce`. Several instances may share one. For an MCP server, its provider key (`mcp_…`), which is also what AuthorizeConnector takes. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
    - `kind` — string — The kind of thing an AvailableConnector entry stands for. _(enum: `connector`, `mcp_server`)_
    - `grant` — union **(required)** — Coarse permission grant for a configured connector. The service computes the effective, server-enforced tool set by filtering the pinned definition's tools with this grant (using each tool's `ConnectorToolAccess`), and requests only the scopes the grant implies at connection time.
      - _oneOf_ — exactly one of:
        - **`read`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`readWrite`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`all`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`tools`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `title` — string **(required)**
    - `icon` — string
    - `provider` — string **(required)** — Provider the connector authenticates against, e.g. `salesforce`. A user's consent is per provider, so connecting one instance connects every instance on the same provider.
    - `mode` — string **(required)** — Supported credential resolution mode. Mirrors wilma-secrets `ConnectionType`. _(enum: `shared`, `user`)_
    - `authorization` — string **(required)** — The current user's authorization status for a connector. Drives the Connect button: the connector is usable when NOT_REQUIRED or CONNECTED, and prompts the user to connect when NOT_CONNECTED or NEEDS_RECONNECT. _(enum: `not_required`, `not_connected`, `connected`, `needs_reconnect`)_
    - `enabled` — boolean **(required)** — Effective enablement for this user, after applying their disabled preferences.
- `connectorsSettings` — UserConnectorsSettings — Per-user connector preferences, by connector instance id. Connectors the user has disabled are removed from the effective set at runtime, even when an admin enabled them.
  - `disabled` — array
    - _array of_ `string`
- `copilotSettings` — UserCopilotSettings — Per-user Copilot settings. Resolved by the service; PatchSettings does not change them.
  - `availability` — CopilotAvailability — Whether Copilot (real-time agent-assist, wildix.wilma.copilot) may assist the user, resolved from the company's live profiles and their `audience`. Entries that need a conversation to decide (queue, service, trunk, agent) and department entries (PBX department ids, which no directory here exposes) count as matching, except in the `before` stage, where the user is the one who opens Copilot and conversation entries say nothing. A profile limited to the `before` stage enables Copilot but covers no channel.
    - `enabled` — boolean **(required)** — Whether at least one live profile may assist the user.
    - `channels` — array — Conversation channels covered by the profiles that may assist the user. Empty when `enabled` is false.
      - _array of_ `CopilotChannel`
    - `stages` — array — Stages covered by the profiles that may assist the user. `before` means Copilot can be opened without a call, chat or conference. Empty when `enabled` is false.
      - _array of_ `CopilotStage`
    - `reason` — string — Why Copilot is or is not available to the user. _(enum: `available`, `no_live_profile`, `not_in_audience`)_

**`ReasoningCompletedEvent`**

_Emitted once per step after the model finishes its reasoning block, carrying the complete reasoning text._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `step` — number **(required)**
- `reasoning` — string **(required)**

**`ReasoningDeltaEvent`**

_Emitted for every reasoning (thinking) token chunk the model produces, when the selected model exposes reasoning. High frequency; intended for live typing indicators._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `step` — number **(required)**
- `delta` — string **(required)** — The new reasoning fragment.
- `soFar` — string **(required)** — The full reasoning text accumulated so far in this step, so late subscribers do not need to replay every delta.

**`ResumeSessionRequestContent`**

- `pendingId` — string **(required)**
- `inputResponses` — array **(required)**
  - _array of_ `SessionInputResponse`
    - `callId` — string **(required)**
    - `result` — any
    - `approved` — boolean

**`ResumeSessionResponseContent`**

_Handle returned by operations that start or continue a turn: the session, the event index from which the caller should stream, and the trace recording it._

- `sessionId` — string **(required)** _(minLen=1; maxLen=128)_
- `startIndex` — number **(required)**
- `traceId` — string — Trace recording the session in wilma-traces — every turn, model call and tool execution the agent ran. Read it with the wilma-traces GetTrace operation, or tail it live with StreamTrace next to the event stream `startIndex` addresses. One id for the whole session, not for this turn: the handle a later ContinueSession returns names the same trace StartSession opened, and each turn appends to it. The trace row is written once the turn's first step completes, so GetTrace may report NotFound in the moment right after this call returns. Absent when the session's trace is not the caller's to read — a session served by a Wildix built-in agent is recorded for Wildix rather than for the tenant. _(minLen=1; maxLen=128)_

**`RevokeConnectorAuthorizationResponseContent`**

- `connector` — AvailableConnector **(required)** — One configured connector instance the current user can use in the assistant, with their authorization and enablement state. The catalogue lists every instance the company configured and this deployment can execute; an agent's `connectorIds` say which of them that agent calls. Backs the connectors menu and its per-connector Connect button.
  - `id` — string **(required)** — Connector instance id — the id an agent's capabilities and the user's `disabled` preference refer to. For an MCP server, the id of the Tool that registers it. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `key` — string **(required)** — Connector definition key, e.g. `salesforce`. Several instances may share one. For an MCP server, its provider key (`mcp_…`), which is also what AuthorizeConnector takes. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
  - `kind` — string — The kind of thing an AvailableConnector entry stands for. _(enum: `connector`, `mcp_server`)_
  - `grant` — union **(required)** — Coarse permission grant for a configured connector. The service computes the effective, server-enforced tool set by filtering the pinned definition's tools with this grant (using each tool's `ConnectorToolAccess`), and requests only the scopes the grant implies at connection time.
    - _oneOf_ — exactly one of:
      - **`read`**
        - `read` — ConnectorGrantRead **(required)** — Marker: grant every READ tool.
      - **`readWrite`**
        - `readWrite` — ConnectorGrantReadWrite **(required)** — Marker: grant every READ and WRITE tool.
      - **`all`**
        - `all` — ConnectorGrantAll **(required)** — Marker: grant every tool, including DESTRUCTIVE.
      - **`tools`**
        - `tools` — array **(required)** — Advanced: an explicit allowlist of tool ids, regardless of access class.
          - _array of_ `string`
  - `title` — string **(required)**
  - `icon` — string
  - `provider` — string **(required)** — Provider the connector authenticates against, e.g. `salesforce`. A user's consent is per provider, so connecting one instance connects every instance on the same provider.
  - `mode` — string **(required)** — Supported credential resolution mode. Mirrors wilma-secrets `ConnectionType`. _(enum: `shared`, `user`)_
  - `authorization` — string **(required)** — The current user's authorization status for a connector. Drives the Connect button: the connector is usable when NOT_REQUIRED or CONNECTED, and prompts the user to connect when NOT_CONNECTED or NEEDS_RECONNECT. _(enum: `not_required`, `not_connected`, `connected`, `needs_reconnect`)_
  - `enabled` — boolean **(required)** — Effective enablement for this user, after applying their disabled preferences.

**`SandboxFailedEvent`**

_Emitted when acquiring the sandbox fails; the turn then fails with the same cause. Provides sandbox-level observability distinct from the generic TurnFailedEvent._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `message` — string **(required)**

**`SandboxStartedEvent`**

_Emitted when the turn is attached to its sandbox, the first time a sandbox-backed tool is used in the turn. A session reuses one sandbox across turns whenever possible._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `sandboxId` — string **(required)** — Provider-side sandbox id, stable while the sandbox is reused across turns.
- `resumed` — boolean **(required)** — True when an existing sandbox from a previous turn was reattached; false when a fresh sandbox was created.

**`ServiceUnavailableExceptionResponseContent`**

_The service is temporarily unable to handle the request; retry later._

- `message` — string **(required)**

**`SessionClientTool`**

_A tool the caller supplies for this session, rather than one configured on the agent. The routing fields (`fulfilment`, `gate`, `surface`, `stream`) are stamped onto the turn's InvocationStartedEvent, so clients replaying the session render the call correctly._

- `name` — string **(required)**
- `description` — string
- `schema` — any **(required)**
- `fulfilment` — string — Who produces an invocation's result. `server` tools execute inside the agent runtime. `client` tools are executed by the caller, so the turn suspends until it answers. `synthetic` tools never execute at all — they exist to put something on screen, and the runtime supplies their result itself, so the turn does not suspend. _(enum: `server`, `client`, `synthetic`)_
- `gate` — string — Whether the turn suspends on an invocation, and for what. Orthogonal to fulfilment: a `server` tool may be gated on a user decision (an approval), and a `synthetic` tool may be ungated (render and continue) or gated (an editable draft awaiting confirmation). _(enum: `none`, `result`, `decision`)_
- `surface` — string — Where a client should surface an invocation. Affects placement only, never behaviour. _(enum: `hidden`, `activity`, `content`)_
- `stream` — boolean — Emit InvocationDeltaEvent for calls to this tool, so the caller can render the input as the model writes it — useful when the input carries content rather than a lookup key. Defaults to false.
- `ack` — any — Result handed back to the model for a `synthetic` tool, typically a short instruction telling the model what the user can now see. Ignored for `client` tools.

**`SessionConnectors`**

_Per-session connector overrides, by connector instance id. `disabled` turns connectors off for this session only; `enabled` turns back on connectors the user disabled in their settings, for this session only._

- `disabled` — array
  - _array of_ `string`
- `enabled` — array
  - _array of_ `string`

**`SessionFailedEvent`**

_Terminal event emitted after TurnFailedEvent: the session is in `failed` status. A new turn starts from the last consistent snapshot._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `code` — string **(required)**
- `message` — string **(required)**

**`SessionIdleEvent`**

_Terminal event of a successful turn: the session is idle and ready for the next turn._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.

**`SessionInputResponse`**

- `callId` — string **(required)**
- `result` — any
- `approved` — boolean

**`SessionInvocationFulfilment`**

_Who produces an invocation's result. `server` tools execute inside the agent runtime. `client` tools are executed by the caller, so the turn suspends until it answers. `synthetic` tools never execute at all — they exist to put something on screen, and the runtime supplies their result itself, so the turn does not suspend._

- string _(enum: `server`, `client`, `synthetic`)_

**`SessionInvocationGate`**

_Whether the turn suspends on an invocation, and for what. Orthogonal to fulfilment: a `server` tool may be gated on a user decision (an approval), and a `synthetic` tool may be ungated (render and continue) or gated (an editable draft awaiting confirmation)._

- string _(enum: `none`, `result`, `decision`)_

**`SessionInvocationResolver`**

_Who supplied the result recorded by an InvocationResultEvent._

- string _(enum: `server`, `client`, `user`)_

**`SessionInvocationStatus`**

- string _(enum: `completed`, `failed`)_

**`SessionInvocationSurface`**

_Where a client should surface an invocation. Affects placement only, never behaviour._

- string _(enum: `hidden`, `activity`, `content`)_

**`SessionMeta`**

- `sessionId` — string **(required)** _(minLen=1; maxLen=128)_
- `agentId` — string _(minLen=12; maxLen=12)_
- `traceId` — string — Opaque trace identifier generated by the tracing runtime. _(minLen=1; maxLen=128)_
- `agentVersion` — number — Published agent version serving this session, selected at session start. _(min=1)_
- `agentDraft` — boolean — True when the session runs the agent's mutable draft (agentDraft on StartSession).
- `agentDraftRevision` — number — Draft revision loaded at session start when agentDraft is true; correlates a run with the exact draft state.
- `model` — string — Effective model resolved at session start (after 'default' resolution), e.g. 'google://gemini-3-flash-preview'.
- `skillVersions` — array — Skill versions resolved at session start, one entry per attached skill (whether pinned or resolved via the skill's alias).
  - _array of_ `SessionSkillVersion`
    - `skillId` — string **(required)** _(minLen=12; maxLen=12)_
    - `version` — number **(required)** — Published skill version number. Monotonic within a skill's version history, starting at 1. _(min=1)_
- `visibility` — string — Whether a session shows up in the user's assistant history. Integration-driven sessions (e.g. copilot asset generation) are started `hidden` so they do not pollute the history while staying reachable by id. _(enum: `listed`, `hidden`)_
- `target` — string — What the session belongs to, as supplied on StartSession. Present for sessions started from a client surface or integration that identified itself. _(minLen=1; maxLen=1024)_
- `metadata` — any — Host-defined metadata supplied on StartSession, returned verbatim.
- `status` — string **(required)** _(enum: `running`, `idle`, `waiting`, `stopped`, `failed`, `terminated`)_
- `version` — number **(required)** — Monotonic session state revision.
- `title` — string
- `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `updatedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `eventCount` — number **(required)**

**`SessionPendingInput`**

_One invocation the turn is suspended on. References an invocation already announced by InvocationStartedEvent; the tool name and input are not repeated here._

- `callId` — string **(required)** — Id of the invocation, matching an InvocationStartedEvent in this turn.
- `kind` — string **(required)** _(enum: `client`, `question`, `approval`)_

**`SessionPendingInputKind`**

- string _(enum: `client`, `question`, `approval`)_

**`SessionSkill`**

_Ad-hoc skill supplied by the caller for this session only._

- `name` — string **(required)**
- `description` — string **(required)**
- `body` — string **(required)**

**`SessionSkillVersion`**

_Published skill version an agent skill attachment resolved to at session start._

- `skillId` — string **(required)** _(minLen=12; maxLen=12)_
- `version` — number **(required)** — Published skill version number. Monotonic within a skill's version history, starting at 1. _(min=1)_

**`SessionStartedEvent`**

_Emitted once as the very first event of a session, when it is created. Confirms the session id and the agent the session is bound to._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `sessionId` — string **(required)** _(minLen=1; maxLen=128)_
- `agentId` — string _(minLen=12; maxLen=12)_

**`SessionStatus`**

- string _(enum: `running`, `idle`, `waiting`, `stopped`, `failed`, `terminated`)_

**`SessionSteerOutcome`**

_How a steer request was applied. `steered` means it reached the running turn at a step boundary with the turn's work intact. `promoted` means no step boundary remained, so the runtime ran the message as a new turn instead — a steer is never silently dropped._

- string _(enum: `steered`, `promoted`)_

**`SessionStopReason`**

- string _(enum: `user`)_

**`SessionStoppedEvent`**

_Terminal event emitted when the active turn was cancelled via the channel's stop operation._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `reason` — string **(required)** _(enum: `user`)_

**`SessionTerminateReason`**

- string _(enum: `guardrail`)_

**`SessionTerminatedEvent`**

_Terminal event emitted when the platform ended the session rather than let it continue: the session is in `terminated` status. Distinct from SessionStoppedEvent, which records a user or operator asking to stop — folding the two together would leave a refused session indistinguishable from a clean finish in every completion-rate report. On voice the call is hung up as this is emitted; on the other channels there is nothing to hang up and termination is the status alone — history is kept, and the session simply accepts no further turns._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `reason` — string **(required)** _(enum: `guardrail`)_
- `guardrail` — string — The check whose `end` action terminated the session, when `reason` is `guardrail`. _(minLen=1; maxLen=64)_
- `message` — string — What the caller was told before the session ended.

**`SessionUsage`**

- `inputTokens` — number
- `cachedTokens` — number — The part of `inputTokens` served from the provider's prompt cache. Absent when the provider does not report it.
- `outputTokens` — number
- `reasoningTokens` — number — The part of `outputTokens` spent on reasoning. Absent when the provider does not report it, or when the model does not reason.
- `totalTokens` — number

**`SessionVisibility`**

_Whether a session shows up in the user's assistant history. Integration-driven sessions (e.g. copilot asset generation) are started `hidden` so they do not pollute the history while staying reachable by id._

- string _(enum: `listed`, `hidden`)_

**`SessionWaitingEvent`**

_Terminal event of a turn that paused for caller input. The session stays in `waiting` status until resumed with the `pendingId`._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `pendingId` — string **(required)**

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

**`SkillStatus`**

- string _(enum: `draft`, `active`)_

**`SkillVisibility`**

- string _(enum: `private`, `company`)_

**`StartSessionRequestContent`**

- `user` — string — The user the session belongs to. Optional: identifies the user when a service or tenant token is used; when omitted the session is not scoped to a specific user. _(minLen=12; maxLen=12)_
- `message` — string **(required)** _(minLen=1; maxLen=100000)_
- `attachments` — array — Ids of input attachments to include with the initial user message, as returned by UploadAttachment. Their stored metadata is reported back on the turn's MessageReceivedEvent.
  - _array of_ `string`
- `sessionId` — string _(minLen=1; maxLen=128)_
- `agentId` — string _(minLen=12; maxLen=12)_
- `agentVersion` — number — Published agent version to run. Mutually exclusive with agentDraft. When neither is set, the agent's deployment configuration selects the version. _(min=1)_
- `agentDraft` — boolean — Run the agent's current draft (for testing). Mutually exclusive with agentVersion.
- `options` — any — Runtime options for the session, e.g. `{model: 'google://gemini-3-flash-preview', timeZone: 'Europe/Rome'}`. `timeZone` is the IANA time zone of the person asking: the session shows every time in it, fixed at start, and falls back to the agent's when omitted. Interpreted by the runtime, so only documented keys belong here: put values the client wants back unchanged in `metadata`, and what the session belongs to in `target`.
- `context` — array — What the client has in view and the server cannot read for itself, such as the page or the agent being edited, as `{id, type, data}` documents.
  - _array of_ `any`
- `mentions` — array — What the user attached for the agent to read, resolved with the session user's permissions, or company-wide when the session has no user. _(maxItems=20)_
  - _array of_ `Mention`
    - _oneOf_ — exactly one of:
      - **`reference`**
        - `reference` — MentionReference **(required)** — A resource selected as agent context, identified by its canonical URI, e.g. `wilma://insights/calls/{callId}/flows/{flowIndex}`. It is read with the permissions of the session or task it is attached to; the URI grants no access by itself.
          - _(nesting depth limit — see `MentionReference` in the Schemas appendix)_
- `tools` — array
  - _array of_ `SessionClientTool`
    - `name` — string **(required)**
    - `description` — string
    - `schema` — any **(required)**
    - `fulfilment` — string — Who produces an invocation's result. `server` tools execute inside the agent runtime. `client` tools are executed by the caller, so the turn suspends until it answers. `synthetic` tools never execute at all — they exist to put something on screen, and the runtime supplies their result itself, so the turn does not suspend. _(enum: `server`, `client`, `synthetic`)_
    - `gate` — string — Whether the turn suspends on an invocation, and for what. Orthogonal to fulfilment: a `server` tool may be gated on a user decision (an approval), and a `synthetic` tool may be ungated (render and continue) or gated (an editable draft awaiting confirmation). _(enum: `none`, `result`, `decision`)_
    - `surface` — string — Where a client should surface an invocation. Affects placement only, never behaviour. _(enum: `hidden`, `activity`, `content`)_
    - `stream` — boolean — Emit InvocationDeltaEvent for calls to this tool, so the caller can render the input as the model writes it — useful when the input carries content rather than a lookup key. Defaults to false.
    - `ack` — any — Result handed back to the model for a `synthetic` tool, typically a short instruction telling the model what the user can now see. Ignored for `client` tools.
- `visibility` — string — Whether a session shows up in the user's assistant history. Integration-driven sessions (e.g. copilot asset generation) are started `hidden` so they do not pollute the history while staying reachable by id. _(enum: `listed`, `hidden`)_
- `target` — string — What this session belongs to: the client surface it is started on (`inbox://channels/ch_123`) or the resource an integration starts it for (`copilot://sessions/cs_123`). Returned on SessionMeta and filterable on ListSessions, so a client can reopen the session where it came from and list a per-surface history. Opaque to the service; immutable once set. _(minLen=1; maxLen=1024)_
- `metadata` — any — Host-defined metadata to carry with the session and read back from SessionMeta. Not indexed; use `target` for anything a list must be filtered by.
- `personalisation` — any
- `skills` — array
  - _array of_ `SessionSkill`
    - `name` — string **(required)**
    - `description` — string **(required)**
    - `body` — string **(required)**
- `connectors` — SessionConnectors — Per-session connector overrides, by connector instance id. `disabled` turns connectors off for this session only; `enabled` turns back on connectors the user disabled in their settings, for this session only.
  - `disabled` — array
    - _array of_ `string`
  - `enabled` — array
    - _array of_ `string`

**`StartSessionResponseContent`**

_Handle returned by operations that start or continue a turn: the session, the event index from which the caller should stream, and the trace recording it._

- `sessionId` — string **(required)** _(minLen=1; maxLen=128)_
- `startIndex` — number **(required)**
- `traceId` — string — Trace recording the session in wilma-traces — every turn, model call and tool execution the agent ran. Read it with the wilma-traces GetTrace operation, or tail it live with StreamTrace next to the event stream `startIndex` addresses. One id for the whole session, not for this turn: the handle a later ContinueSession returns names the same trace StartSession opened, and each turn appends to it. The trace row is written once the turn's first step completes, so GetTrace may report NotFound in the moment right after this call returns. Absent when the session's trace is not the caller's to read — a session served by a Wildix built-in agent is recorded for Wildix rather than for the tenant. _(minLen=1; maxLen=128)_

**`SteerAppliedEvent`**

_Emitted when an accepted steer has reached the model, naming the turn and step boundary where it took effect. The gap between SteerReceivedEvent and this event is user-visible, so a client can show the steering message as pending until it lands. A steer never interrupts a tool call that is already running. `turn` differs from the SteerReceivedEvent's `turn` when the steer was promoted: the running turn finished before a boundary arrived, so the message became the input of the following turn._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)** — The turn the steering message was injected into — the following turn when it was promoted.
- `step` — number **(required)** — The step the steering message was injected ahead of.

**`SteerReceivedEvent`**

_Emitted when a steer request is accepted for the turn already running, before it reaches the model. A turn can therefore carry more than one user message; build transcripts from event order, not from turn structure. This is the only record of the steering text: a turn the steer was promoted into starts with TurnStartedEvent but emits no MessageReceivedEvent, so the message is never recorded twice._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)** — The turn the steer was accepted for.
- `message` — string **(required)** _(minLen=1; maxLen=100000)_
- `attachments` — array — Input files supplied with the steering message, as stored. Absent when it carried no files.
  - _array of_ `Attachment`
    - `id` — string **(required)** — Nano-id attachment identifier (12 characters). _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
    - `name` — string **(required)** — Filename shown to the user. Characters storage cannot represent are replaced with underscores. _(minLen=1; maxLen=255)_
    - `contentType` — string — MIME type recorded by storage from the uploaded content, e.g. 'application/pdf'. Absent until the upload completes.
    - `size` — number — Size in bytes recorded by storage from the uploaded content. Absent until the upload completes.
    - `thumbnailUrl` — string — URL of a generated preview image, for rendering a thumbnail without downloading the file. Best-effort: absent until the upload completes, and for content no preview can be generated from.
    - `createdAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.

**`SteerSessionRequestContent`**

- `message` — string **(required)** _(minLen=1; maxLen=100000)_
- `attachments` — array — Input attachments to include with the steering message. Fetch them via the Attachments API.
  - _array of_ `string`
- `context` — array — Replaces the session's context documents, what the client has in view and the server cannot read for itself, from the next model step. Omit to keep them.
  - _array of_ `any`
- `mentions` — array — Replaces the session's mentions from the next model step. Omit to keep them; pass an empty list to clear them. _(maxItems=20)_
  - _array of_ `Mention`
    - _oneOf_ — exactly one of:
      - **`reference`**
        - `reference` — MentionReference **(required)** — A resource selected as agent context, identified by its canonical URI, e.g. `wilma://insights/calls/{callId}/flows/{flowIndex}`. It is read with the permissions of the session or task it is attached to; the URI grants no access by itself.
          - _(nesting depth limit — see `MentionReference` in the Schemas appendix)_

**`SteerSessionResponseContent`**

_Handle returned by operations that start or continue a turn: the session, the event index from which the caller should stream, and the trace recording it._

- `sessionId` — string **(required)** _(minLen=1; maxLen=128)_
- `startIndex` — number **(required)**
- `traceId` — string — Trace recording the session in wilma-traces — every turn, model call and tool execution the agent ran. Read it with the wilma-traces GetTrace operation, or tail it live with StreamTrace next to the event stream `startIndex` addresses. One id for the whole session, not for this turn: the handle a later ContinueSession returns names the same trace StartSession opened, and each turn appends to it. The trace row is written once the turn's first step completes, so GetTrace may report NotFound in the moment right after this call returns. Absent when the session's trace is not the caller's to read — a session served by a Wildix built-in agent is recorded for Wildix rather than for the tenant. _(minLen=1; maxLen=128)_
- `turn` — number **(required)** — The turn the message reached: the running turn when `steered`, the new turn when `promoted`.
- `outcome` — string **(required)** — How a steer request was applied. `steered` means it reached the running turn at a step boundary with the turn's work intact. `promoted` means no step boundary remained, so the runtime ran the message as a new turn instead — a steer is never silently dropped. _(enum: `steered`, `promoted`)_

**`StepCompletedEvent`**

_Emitted when an inference step finishes, with token usage for the step when the provider reports it._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `step` — number **(required)**
- `finishReason` — string **(required)**
- `usage` — SessionUsage
  - `inputTokens` — number
  - `cachedTokens` — number — The part of `inputTokens` served from the provider's prompt cache. Absent when the provider does not report it.
  - `outputTokens` — number
  - `reasoningTokens` — number — The part of `outputTokens` spent on reasoning. Absent when the provider does not report it, or when the model does not reason.
  - `totalTokens` — number

**`StepStartedEvent`**

_Emitted each time the model starts a new inference step within a turn (a turn spans multiple steps when the model calls tools)._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `step` — number **(required)** — 1-based step number within the turn.

**`StopSessionResponseContent`**

- `sessionId` — string **(required)** _(minLen=1; maxLen=128)_
- `accepted` — boolean **(required)**

**`StreamSessionEventsOutputPayload`**

_Raw Server-Sent Events byte stream (`text/event-stream`). Each frame carries one event of the channel's own union (AssistantSessionEvent / ChatSessionEvent / WorkflowTaskEvent): `id:` is the event index, `event:` is the union member name, and `data:` is the JSON document of the union value, e.g. `{"messageAppended": {...}}`._

- string

**`TaskCompletedEvent`**

_Emitted when a delegated task execution finishes, carrying its final answer as returned to the parent agent._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `taskId` — string **(required)**
- `name` — string **(required)**
- `output` — string **(required)**

**`TaskOrigin`**

_Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity._

- `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
- `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.

**`TaskStartedEvent`**

_Emitted when the agent delegates a subtask to a task execution: the `delegate` tool or an agent-call capability. Events emitted inside the task are re-published on the session stream with `origin` set to this task, until the matching TaskCompletedEvent._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `taskId` — string **(required)** — Unique id of this task execution; referenced by `origin.taskId` of nested events.
- `name` — string **(required)** — Task tool name, e.g. `delegate` or the name of the called agent.
- `agentId` — string — Agent executing the task, when the task is a called or delegated agent. _(minLen=12; maxLen=12)_
- `agentVersion` — number — Published version of the agent executing the task, resolved when the task started; absent when the task runs a draft. _(min=1)_
- `instructions` — string **(required)** — The self-contained instructions handed to the task.

**`TurnCompletedEvent`**

_Emitted when a turn finishes successfully, with aggregate token usage for the turn. Followed by SessionIdleEvent._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `usage` — SessionUsage
  - `inputTokens` — number
  - `cachedTokens` — number — The part of `inputTokens` served from the provider's prompt cache. Absent when the provider does not report it.
  - `outputTokens` — number
  - `reasoningTokens` — number — The part of `outputTokens` spent on reasoning. Absent when the provider does not report it, or when the model does not reason.
  - `totalTokens` — number

**`TurnFailedEvent`**

_Emitted when a turn fails with an unrecoverable error. Followed by SessionFailedEvent._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `code` — string **(required)** — Stable machine-readable error code.
- `message` — string **(required)**

**`TurnStartedEvent`**

_Emitted when a turn begins executing. All subsequent events up to the matching TurnCompletedEvent/TurnFailedEvent belong to this turn._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)** — 1-based turn number within the session.

**`UploadAttachmentRequestContent`**

- `name` — string **(required)** — Filename shown to the user, e.g. 'quarterly-report.pdf'. _(minLen=1; maxLen=255)_

**`UploadAttachmentResponseContent`**

- `attachmentId` — string **(required)** — Identifier of the registered attachment. Pass it in the `attachments` list of StartSession or ContinueSession, and to the other Attachments operations. _(pattern=^[A-Za-z0-9_-]{12}$; minLen=12; maxLen=12)_
- `uploadUrl` — string **(required)** — Presigned URL to PUT the attachment content to. Short-lived: upload the bytes right away rather than storing the URL.

**`UserAboutSettings`**

_Background the assistant may use to personalise replies for this user._

- `description` — string _(minLen=1; maxLen=2000)_

**`UserConnectorsSettings`**

_Per-user connector preferences, by connector instance id. Connectors the user has disabled are removed from the effective set at runtime, even when an admin enabled them._

- `disabled` — array
  - _array of_ `string`

**`UserCopilotSettings`**

_Per-user Copilot settings. Resolved by the service; PatchSettings does not change them._

- `availability` — CopilotAvailability — Whether Copilot (real-time agent-assist, wildix.wilma.copilot) may assist the user, resolved from the company's live profiles and their `audience`. Entries that need a conversation to decide (queue, service, trunk, agent) and department entries (PBX department ids, which no directory here exposes) count as matching, except in the `before` stage, where the user is the one who opens Copilot and conversation entries say nothing. A profile limited to the `before` stage enables Copilot but covers no channel.
  - `enabled` — boolean **(required)** — Whether at least one live profile may assist the user.
  - `channels` — array — Conversation channels covered by the profiles that may assist the user. Empty when `enabled` is false.
    - _array of_ `CopilotChannel`
  - `stages` — array — Stages covered by the profiles that may assist the user. `before` means Copilot can be opened without a call, chat or conference. Empty when `enabled` is false.
    - _array of_ `CopilotStage`
  - `reason` — string — Why Copilot is or is not available to the user. _(enum: `available`, `no_live_profile`, `not_in_audience`)_

**`UserSkillsSettings`**

_Per-user skill preferences. Skills the user has disabled are omitted from the effective skill set at runtime._

- `disabled` — array
  - _array of_ `string`

**`UserStyleSettings`**

_How the assistant should communicate with this user._

- `tone` — string _(minLen=1; maxLen=64)_

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

**`WorkflowMoveRefusedEvent`**

_Emitted when the model asks to move somewhere the live step does not declare as an exit. The runtime refuses, names the legal exits, and the session carries on from the same step, so this is not a failure of the turn: it is the record of what callers keep reaching for and the graph does not offer. Aggregated per step, it is the shortest route to the exit a graph is missing._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number **(required)**
- `workflow` — string — The nested workflow the live step belongs to. Absent in the main graph. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
- `stepId` — string **(required)** — The step the session stayed on. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
- `requested` — string **(required)** — What the model asked for, verbatim — not necessarily a step that exists.
- `reason` — string — The model's stated reason for the move it was refused.

**`WorkflowStepEnteredEvent`**

_Emitted when the workflow cursor arrives at a step, before the step runs — so every later event in the log belongs to the step most recently entered. The first is the graph's `entry` step; the last is a terminal step, which is where the session left the graph._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number — The turn the step was entered during, when it was entered inside one. Absent when the cursor moved between turns: an `action`, `message` or `variables` step needs no model call, so a chain of them can advance before the next turn begins.
- `workflow` — string — The nested workflow (AgentWorkflow.nested) this step belongs to. Absent for a step of the main graph, which is how nesting is read off the stream — no separate enter/return events. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
- `stepId` — string **(required)** — Identifier of a step within its workflow, unique per workflow (the main graph and each nested workflow are separate scopes). Stable and machine-facing: transitions reference it, and a result step's id is the name a caller branches on, so renaming a step's `label` never unwires the graph. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
- `label` — string — The step's authored label, so a reader needs no copy of the agent definition to render the stream. _(minLen=1; maxLen=128)_
- `stage` — string — The step's stage, as authored on it or inherited from upstream. Absent when the graph uses no stages. _(minLen=1; maxLen=64)_
- `type` — string **(required)** — Which handler a step carries, reported on the session event stream (WorkflowStepEnteredEvent) and in traces. Mirrors the members of AgentWorkflowHandler and exists so a reader does not have to load the agent version snapshot to tell a stretch of conversation from a runtime action: a trace is read long after the fact, by an operator who has the session and not the definition it ran against. `conversation` is the only member that hands the turn to the model; which capability an `action` step performed is named by the invocation events that follow it. _(enum: `conversation`, `message`, `action`, `variables`, `workflow`, `result`, `end`)_

**`WorkflowTransitionEvent`**

_Emitted when a transition is taken, naming the exit and what decided it. Not emitted on a terminal step, which has no exits — a session that ended inside the graph is read from the last WorkflowStepEnteredEvent — and not emitted when a conversation step's conditions all stay false, which is the step simply continuing._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number — The turn the transition was evaluated in. Absent when the cursor moved between turns.
- `workflow` — string — The nested workflow both steps belong to. Absent in the main graph; a transition never crosses graphs. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
- `stepId` — string **(required)** — Step being left. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
- `target` — string **(required)** — Step being entered. A WorkflowStepEnteredEvent for it follows. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
- `condition` — string **(required)** — Which kind of condition took a transition, as reported on the session event stream (WorkflowTransitionEvent) and in traces. Mirrors the members of AgentWorkflowCondition: `prompt` is the only one the model decides, every other was settled by the runtime with no model call. _(enum: `always`, `prompt`, `expression`, `result`, `failure`, `fallback`)_
- `reason` — string — The model's one-line reason for the move, as it gave it to the steering tool. Present only for `prompt` conditions.

**`WorkflowVariablesWrittenEvent`**

_Emitted when workflow variables are written: a `variables` step's assignments, or an action step capturing its result into `output`. The only record of the state `expression` conditions branch on and handlebars resolve against, so replaying the log from index 0 reconstructs the same variables the runtime had._

- `index` — number **(required)** — Monotonic per-session event index. Drives resumption: pass `index + 1` of the last seen event as `startIndex` when reconnecting.
- `timestamp` — string **(required)** — ISO-8601 time the event was recorded.
- `origin` — TaskOrigin — Identifies the delegated task that emitted an event. Top-level events carry no origin; events re-published from a child task execution (the `delegate` tool or an agent-call capability) carry the origin of that task so clients can render nested activity.
  - `taskId` — string **(required)** — Id of the task execution that emitted the event. Matches the `taskId` of the surrounding TaskStartedEvent/TaskCompletedEvent pair.
  - `taskName` — string **(required)** — Name of the task tool that emitted the event, e.g. `delegate` or the name of a called agent.
- `turn` — number — The turn the write happened in, when it happened inside one.
- `workflow` — string — The nested workflow the writing step belongs to. Absent in the main graph. Variables are shared with the main graph either way — a nested workflow has no scope of its own. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
- `stepId` — string **(required)** — Step that wrote them. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=64)_
- `values` — any **(required)** — The names written and their resolved values, as a JSON object. Only what this write touched, not the whole state; a variable cleared by an empty assignment is present with an empty value.

</details>
