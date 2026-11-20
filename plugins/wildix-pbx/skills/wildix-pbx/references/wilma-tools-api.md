## Wilma Tools API

_OpenAPI: Wilma Tools Service — version v2_

**Servers**

- `https://api.wilma.wildix.com` — Production
- `https://api-stable.wilma.wildix.com` — Stable
- `https://api-stage.wilma.wildix.com` — Stage

### Other

#### `GET` `/v2/tools`

List all tools for the current company.

- operationId: `ListTools`
- **Scopes**: `tools:ListTools`, `tools:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `status` (query) — string — Only tools with this version state. _(enum: `draft`, `active`)_
  - `search` (query) — string — Filter by name, category or description.
  - `limit` (query) — number _(min=1; max=100)_
  - `cursor` (query) — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- **Response 200** (`ListToolsResponseContent`)
  - `tools` — array **(required)**
    - _array of_ `Tool`
      - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
      - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
      - `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
      - `input` — ToolInput
        - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
      - `handler` — union **(required)** — Handler of the tool. Every tool executes through one of three mechanisms: a pinned connector definition (built-in providers such as email, webhook, search, chat, sms, calendar — and external integrations — share the same contract), an MCP server registration, or a single tool on a registered MCP server.
        - _oneOf_ — exactly one of:
          - **`connector`**
            - `connector` — ToolConnectorHandler **(required)** — Handler for a connector-backed Tool created through `CreateTool`. Carries two configuration layers: `configuration` (from the mixin) holds definition-level values for the connector as a whole (validated against the definition `configuration.schema`), while `toolConfiguration` holds values specific to this created Tool (validated against the pinned connector tool's `configuration.schema`). `Tool.input` follows copy-at-create semantics: when `input` is omitted on create, the service snapshots the pinned connector tool's input schema into the Tool; callers may instead provide — and later edit — a custom schema. The Tool owns its copy; definition changes never propagate to existing tools. Reshaping the input of a tool whose handler does not consume input through configuration templates fails at execution, not at write.
              - `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
                - _(nesting depth limit — see `ConnectorDefinitionRef` in the Schemas appendix)_
              - `configuration` — any **(required)** — Values validated against the definition configuration schema.
              - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
                - _(nesting depth limit — see `ConnectorAuthorization` in the Schemas appendix)_
              - `toolId` — string **(required)** — Connector tool from the pinned definition executed by this Tool. _(pattern=^[a-zA-Z0-9._:-]+$; minLen=1; maxLen=256)_
              - `toolConfiguration` — any — Values validated against the pinned connector tool's per-tool configuration schema (`ConnectorTool.configuration.schema`). Omitted when that tool declares no per-tool configuration contract.
          - **`mcp`**
            - `mcp` — ToolMcpHandler **(required)**
              - `serverUrl` — string **(required)** — MCP server endpoint URL
              - `authorization` — union
                - _(nesting depth limit — see `ToolMcpAuthorization` in the Schemas appendix)_
              - `tools` — array **(required)** — Tools enabled for this MCP server.
                - _array of_ `string`
          - **`mcpTool`**
            - `mcpTool` — ToolMcpToolHandler **(required)**
              - `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
              - `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.
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
      - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
      - `status` — string **(required)** _(enum: `draft`, `active`)_
      - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
      - `latestVersion` — number — Latest published version number, resolved by capabilities that omit a version pin. Absent while the tool is still a draft. _(min=1)_
  - `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- Errors: `400`, `401`, `403`, `404`, `500`

#### `POST` `/v2/tools`

Create a new tool draft. The tool is offered to no model until PublishToolVersion snapshots the draft into its first version.

- operationId: `CreateTool`
- **Scopes**: `tools:CreateTool`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `CreateToolRequestContent`) **(required)**
  - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
  - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
  - `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
  - `input` — ToolInput
    - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
  - `handler` — union **(required)** — Handler of the tool. Every tool executes through one of three mechanisms: a pinned connector definition (built-in providers such as email, webhook, search, chat, sms, calendar — and external integrations — share the same contract), an MCP server registration, or a single tool on a registered MCP server.
    - _oneOf_ — exactly one of:
      - **`connector`**
        - `connector` — ToolConnectorHandler **(required)** — Handler for a connector-backed Tool created through `CreateTool`. Carries two configuration layers: `configuration` (from the mixin) holds definition-level values for the connector as a whole (validated against the definition `configuration.schema`), while `toolConfiguration` holds values specific to this created Tool (validated against the pinned connector tool's `configuration.schema`). `Tool.input` follows copy-at-create semantics: when `input` is omitted on create, the service snapshots the pinned connector tool's input schema into the Tool; callers may instead provide — and later edit — a custom schema. The Tool owns its copy; definition changes never propagate to existing tools. Reshaping the input of a tool whose handler does not consume input through configuration templates fails at execution, not at write.
          - `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
            - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
            - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
          - `configuration` — any **(required)** — Values validated against the definition configuration schema.
          - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
            - _oneOf_ — exactly one of:
              - **`shared`**
                - `shared` — ConnectorSharedAuthorization **(required)** — Company-managed connection resolved through wilma-secrets.
                  - _(nesting depth limit — see `ConnectorSharedAuthorization` in the Schemas appendix)_
              - **`user`**
                - `user` — ConnectorUserAuthorization **(required)** — Marker selecting per-user authorization. Carries no connection reference: at execution the executing user's own credential for this connector's provider is resolved through wilma-secrets (GetUserConnectionToken by provider + user).
          - `toolId` — string **(required)** — Connector tool from the pinned definition executed by this Tool. _(pattern=^[a-zA-Z0-9._:-]+$; minLen=1; maxLen=256)_
          - `toolConfiguration` — any — Values validated against the pinned connector tool's per-tool configuration schema (`ConnectorTool.configuration.schema`). Omitted when that tool declares no per-tool configuration contract.
      - **`mcp`**
        - `mcp` — ToolMcpHandler **(required)**
          - `serverUrl` — string **(required)** — MCP server endpoint URL
          - `authorization` — union
            - _oneOf_ — exactly one of:
              - **`connection`**
                - `connection` — ConnectionRef **(required)** — A reference to a connection, held by other services in place of the credential. Resolved to a short-lived token server-to-server via GetConnectionToken.
                  - _(nesting depth limit — see `ConnectionRef` in the Schemas appendix)_
              - **`customHeaders`**
                - `customHeaders` — ToolMcpHeadersMap **(required)**
                  - _(nesting depth limit — see `ToolMcpHeadersMap` in the Schemas appendix)_
              - **`apiKey`**
                - `apiKey` — ToolMcpApiKeyAuthorization **(required)** — A SecretRef plus the header it travels under. The referenced secret is expected to carry variant `auth_api_key`; the value is resolved server-to-server at execution and never stored on the tool.
                  - _(nesting depth limit — see `ToolMcpApiKeyAuthorization` in the Schemas appendix)_
              - **`user`**
                - `user` — ToolMcpUserAuthorization **(required)** — Marker selecting per-user MCP authorization. Carries no reference: the credential is keyed by server and user.
          - `tools` — array **(required)** — Tools enabled for this MCP server.
            - _array of_ `string`
      - **`mcpTool`**
        - `mcpTool` — ToolMcpToolHandler **(required)**
          - `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
          - `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.
- **Response 201** (`CreateToolResponseContent`)
  - `tool` — Tool **(required)** — A company-owned tool. UpdateTool edits the mutable draft; PublishToolVersion snapshots it into an immutable version that agent and skill capabilities resolve.
    - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
    - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
    - `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
    - `input` — ToolInput
      - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
    - `handler` — union **(required)** — Handler of the tool. Every tool executes through one of three mechanisms: a pinned connector definition (built-in providers such as email, webhook, search, chat, sms, calendar — and external integrations — share the same contract), an MCP server registration, or a single tool on a registered MCP server.
      - _oneOf_ — exactly one of:
        - **`connector`**
          - `connector` — ToolConnectorHandler **(required)** — Handler for a connector-backed Tool created through `CreateTool`. Carries two configuration layers: `configuration` (from the mixin) holds definition-level values for the connector as a whole (validated against the definition `configuration.schema`), while `toolConfiguration` holds values specific to this created Tool (validated against the pinned connector tool's `configuration.schema`). `Tool.input` follows copy-at-create semantics: when `input` is omitted on create, the service snapshots the pinned connector tool's input schema into the Tool; callers may instead provide — and later edit — a custom schema. The Tool owns its copy; definition changes never propagate to existing tools. Reshaping the input of a tool whose handler does not consume input through configuration templates fails at execution, not at write.
            - `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
              - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
              - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
            - `configuration` — any **(required)** — Values validated against the definition configuration schema.
            - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
              - _oneOf_ — exactly one of:
                - **`shared`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`user`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `toolId` — string **(required)** — Connector tool from the pinned definition executed by this Tool. _(pattern=^[a-zA-Z0-9._:-]+$; minLen=1; maxLen=256)_
            - `toolConfiguration` — any — Values validated against the pinned connector tool's per-tool configuration schema (`ConnectorTool.configuration.schema`). Omitted when that tool declares no per-tool configuration contract.
        - **`mcp`**
          - `mcp` — ToolMcpHandler **(required)**
            - `serverUrl` — string **(required)** — MCP server endpoint URL
            - `authorization` — union
              - _oneOf_ — exactly one of:
                - **`connection`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`customHeaders`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`apiKey`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`user`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `tools` — array **(required)** — Tools enabled for this MCP server.
              - _array of_ `string`
        - **`mcpTool`**
          - `mcpTool` — ToolMcpToolHandler **(required)**
            - `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
            - `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.
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
    - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
    - `latestVersion` — number — Latest published version number, resolved by capabilities that omit a version pin. Absent while the tool is still a draft. _(min=1)_
- Errors: `400`, `401`, `403`, `404`, `500`

#### `POST` `/v2/tools/capabilities/describe`

Describes an agent's wilma-tools-backed capabilities — standalone Tools and configured
Connectors — in a single request; callers pass only `companyId` and capability refs.

- operationId: `DescribeCapabilities`
- **Scopes**: `tools:DescribeCapabilities`, `tools:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `DescribeCapabilitiesRequestContent`) **(required)**
  - `capabilities` — array **(required)** — Tool and connector references to describe.
    - _array of_ `CapabilityRef`
      - _oneOf_ — exactly one of:
        - **`tool`**
          - `tool` — ToolRef **(required)** — Reference to one tool, optionally pinned to a published version. When `version` is omitted the tool's latestVersion is resolved.
            - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
            - `version` — number — Pin a specific published tool version. When omitted, latestVersion is resolved. _(min=1)_
        - **`connector`**
          - `connector` — string **(required)** — Configured connector instance identifier. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
- **Response 200** (`DescribeCapabilitiesResponseContent`)
  - `descriptions` — array **(required)** — Capability descriptions, corresponding positionally to the requested `capabilities`.
    - _array of_ `CapabilityDescription`
      - _oneOf_ — exactly one of:
        - **`tool`**
          - `tool` — ToolDescription **(required)**
            - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
            - `version` — number **(required)** — Published tool version this description was resolved from: the pinned version when the request carried one, otherwise the latestVersion at resolution time. Pass it back on ExecuteTool so the call runs against the same definition the model was shown. _(min=1)_
            - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
            - `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
            - `schema` — any — JSON Schema (2020-12) of the tool arguments, matching Tool.input.schema. Absent for tools that take no arguments.
        - **`connector`**
          - `connector` — ConnectorDescription **(required)** — Compact connector description used to build the model-facing connector meta-tool at agent load time. The detailed action catalogue and usage guidance are obtained at runtime via the connector's reserved `help` action (`ExecuteConnector`); the full definition is available from `GetConnectorDefinition`.
            - `id` — string **(required)** — Connector instance identifier. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
            - `name` — string **(required)** — Connector name exposed to administrators and AI agents. Used as the meta-tool name. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
            - `description` — string **(required)** — Connector description exposed to administrators and AI agents. Used as the meta-tool description, which points the model at the `help` action. _(minLen=1; maxLen=4096)_
- Errors: `400`, `401`, `403`, `404`, `500`

#### `GET` `/v2/tools/connector-definitions`

Lists immutable connector definitions available from the server catalog.

- operationId: `ListConnectorDefinitions`
- **Scopes**: `tools:ListConnectorDefinitions`, `tools:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `query` (query) — string — Case-insensitive filter applied to connector titles, keys, and descriptions.
  - `limit` (query) — number _(min=1; max=100)_
  - `cursor` (query) — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- **Response 200** (`ListConnectorDefinitionsResponseContent`)
  - `definitions` — array **(required)** — Connector definitions in the current page.
    - _array of_ `ConnectorDefinition`
      - `ref` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
        - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
        - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
      - `metadata` — ConnectorMetadata **(required)** — Display metadata for a connector catalog entry.
        - `title` — string **(required)** — Human-readable connector name.
        - `description` — string **(required)** — Summary of the external system and supported use cases.
        - `icon` — string — Icon URL or renderer-known icon key.
        - `category` — string — Catalog category used for discovery and filtering.
        - `documentationUrl` — string — Link to external connector documentation.
      - `configuration` — ConnectorConfigurationDefinition **(required)** — Configuration contract rendered by management clients and validated by the service.
        - `schema` — any **(required)** — JSON Schema 2020-12 document describing persisted configuration.
        - `uiSchema` — any — Presentation hints for a compatible JSON Schema form renderer.
      - `authorization` — ConnectorAuthorizationDefinition — Authorization requirements declared by a connector definition. Scopes are not declared here: the connection's OAuth scope set is derived from the tools the `ConnectorToolGrant` enables (the union of their `authorizationScopes`) plus the provider's default scopes.
        - `provider` — string **(required)** — Provider key the connector authenticates against, e.g. `salesforce`.
        - `modes` — array **(required)** — Credential resolution modes supported by this connector.
          - _array of_ `ConnectorAuthorizationMode`
        - `connectionConfiguration` — ConnectorConfigurationDefinition — Configuration contract rendered by management clients and validated by the service.
          - `schema` — any **(required)** — JSON Schema 2020-12 document describing persisted configuration.
          - `uiSchema` — any — Presentation hints for a compatible JSON Schema form renderer.
      - `instructions` — string — Main help document (Markdown), returned first via `{"help": {}}`: what the connector is for, how to work with it, and how its tools fit together. Orientation only — the service appends the per-grant action index and the list of reference documents automatically; deep material belongs in `references`. _(minLen=1; maxLen=60000)_
      - `references` — array — On-demand reference documents, listed (name + summary) in the `help` index and loaded individually by name.
        - _array of_ `ConnectorReference`
          - `name` — string **(required)** — Load key, unique within the definition. _(pattern=^[a-z][a-z0-9-]*$; minLen=1; maxLen=128)_
          - `title` — string **(required)** — Human-readable title.
          - `summary` — string **(required)** — One-line summary shown in the `help` index so the model can decide whether to load it.
          - `content` — string **(required)** — Full Markdown body, returned only when the model loads this reference by name. _(minLen=1; maxLen=60000)_
      - `tools` — array **(required)** — Tools available in this definition version.
        - _array of_ `ConnectorTool`
          - `id` — string **(required)** — Stable dispatch identifier used in `ExecuteConnector` input keys. _(pattern=^[a-zA-Z0-9._:-]+$; minLen=1; maxLen=256)_
          - `name` — string **(required)** — Agent-facing tool name. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
          - `description` — string **(required)** — One-line description used by people and AI agents to select the tool. Shown in the `help` index; extended guidance goes in `docs`. _(minLen=1; maxLen=4096)_
          - `access` — string **(required)** — Authoritative access class of a connector tool. Server-enforced: it drives the coarse `ConnectorToolGrant` (Allow read / Allow write / Full access), the scopes derived at connection time, and the default approval behavior. _(enum: `read`, `write`, `destructive`)_
          - `idempotent` — boolean — Whether repeating the call with identical arguments has no additional effect (retry-safe).
          - `category` — string — Optional grouping used to organize large catalogs in the `help` index and management UI (e.g. "Issues", "Pull requests"). Not an access control.
          - `input` — ToolInput **(required)**
            - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
          - `configuration` — ConnectorConfigurationDefinition — Configuration contract rendered by management clients and validated by the service.
            - `schema` — any **(required)** — JSON Schema 2020-12 document describing persisted configuration.
            - `uiSchema` — any — Presentation hints for a compatible JSON Schema form renderer.
          - `examples` — array — Worked examples returned in this tool's `help` detail. Teach argument shape and common call patterns; not shown in the `help` index.
            - _array of_ `string`
          - `docs` — string — Long-form Markdown usage notes returned in this tool's `help` detail (edge cases, field semantics, prerequisites such as "call `issues.list` first to get an id"). Loaded on demand, never in the index. _(minLen=1; maxLen=60000)_
          - `authorizationScopes` — array — Extra OAuth scopes this tool needs. The runtime unions these across the tools a grant enables to derive the connection's scope set; nothing is declared at the connector level.
            - _array of_ `string`
      - `deprecated` — boolean — Whether new instances should avoid this definition.
      - `replacedBy` — ConnectorDefinitionRef — Reference to one immutable connector definition.
        - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
        - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
  - `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- Errors: `400`, `401`, `403`, `404`, `500`

#### `GET` `/v2/tools/connector-definitions/{key}/versions/{version}`

Gets one immutable connector definition.

- operationId: `GetConnectorDefinition`
- **Scopes**: `tools:GetConnectorDefinition`, `tools:read`
- **Parameters**
  - `key` (path) — string **(required)** — Stable connector definition key. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
  - `version` (path) — string **(required)** — Exact immutable definition version. _(minLen=1; maxLen=64)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetConnectorDefinitionResponseContent`)
  - `definition` — ConnectorDefinition **(required)** — Immutable server-owned connector definition. Both external integrations (e.g. `sentry`) and built-in tool providers (e.g. `email`, `webhook`, `search`, `chat`, `sms`, `calendar`) are published through this shape and served from the same catalog. A breaking change to a configuration or input schema publishes a new version; tools pinned to older versions keep working.
    - `ref` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
      - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
      - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
    - `metadata` — ConnectorMetadata **(required)** — Display metadata for a connector catalog entry.
      - `title` — string **(required)** — Human-readable connector name.
      - `description` — string **(required)** — Summary of the external system and supported use cases.
      - `icon` — string — Icon URL or renderer-known icon key.
      - `category` — string — Catalog category used for discovery and filtering.
      - `documentationUrl` — string — Link to external connector documentation.
    - `configuration` — ConnectorConfigurationDefinition **(required)** — Configuration contract rendered by management clients and validated by the service.
      - `schema` — any **(required)** — JSON Schema 2020-12 document describing persisted configuration.
      - `uiSchema` — any — Presentation hints for a compatible JSON Schema form renderer.
    - `authorization` — ConnectorAuthorizationDefinition — Authorization requirements declared by a connector definition. Scopes are not declared here: the connection's OAuth scope set is derived from the tools the `ConnectorToolGrant` enables (the union of their `authorizationScopes`) plus the provider's default scopes.
      - `provider` — string **(required)** — Provider key the connector authenticates against, e.g. `salesforce`.
      - `modes` — array **(required)** — Credential resolution modes supported by this connector.
        - _array of_ `ConnectorAuthorizationMode`
      - `connectionConfiguration` — ConnectorConfigurationDefinition — Configuration contract rendered by management clients and validated by the service.
        - `schema` — any **(required)** — JSON Schema 2020-12 document describing persisted configuration.
        - `uiSchema` — any — Presentation hints for a compatible JSON Schema form renderer.
    - `instructions` — string — Main help document (Markdown), returned first via `{"help": {}}`: what the connector is for, how to work with it, and how its tools fit together. Orientation only — the service appends the per-grant action index and the list of reference documents automatically; deep material belongs in `references`. _(minLen=1; maxLen=60000)_
    - `references` — array — On-demand reference documents, listed (name + summary) in the `help` index and loaded individually by name.
      - _array of_ `ConnectorReference`
        - `name` — string **(required)** — Load key, unique within the definition. _(pattern=^[a-z][a-z0-9-]*$; minLen=1; maxLen=128)_
        - `title` — string **(required)** — Human-readable title.
        - `summary` — string **(required)** — One-line summary shown in the `help` index so the model can decide whether to load it.
        - `content` — string **(required)** — Full Markdown body, returned only when the model loads this reference by name. _(minLen=1; maxLen=60000)_
    - `tools` — array **(required)** — Tools available in this definition version.
      - _array of_ `ConnectorTool`
        - `id` — string **(required)** — Stable dispatch identifier used in `ExecuteConnector` input keys. _(pattern=^[a-zA-Z0-9._:-]+$; minLen=1; maxLen=256)_
        - `name` — string **(required)** — Agent-facing tool name. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
        - `description` — string **(required)** — One-line description used by people and AI agents to select the tool. Shown in the `help` index; extended guidance goes in `docs`. _(minLen=1; maxLen=4096)_
        - `access` — string **(required)** — Authoritative access class of a connector tool. Server-enforced: it drives the coarse `ConnectorToolGrant` (Allow read / Allow write / Full access), the scopes derived at connection time, and the default approval behavior. _(enum: `read`, `write`, `destructive`)_
        - `idempotent` — boolean — Whether repeating the call with identical arguments has no additional effect (retry-safe).
        - `category` — string — Optional grouping used to organize large catalogs in the `help` index and management UI (e.g. "Issues", "Pull requests"). Not an access control.
        - `input` — ToolInput **(required)**
          - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
        - `configuration` — ConnectorConfigurationDefinition — Configuration contract rendered by management clients and validated by the service.
          - `schema` — any **(required)** — JSON Schema 2020-12 document describing persisted configuration.
          - `uiSchema` — any — Presentation hints for a compatible JSON Schema form renderer.
        - `examples` — array — Worked examples returned in this tool's `help` detail. Teach argument shape and common call patterns; not shown in the `help` index.
          - _array of_ `string`
        - `docs` — string — Long-form Markdown usage notes returned in this tool's `help` detail (edge cases, field semantics, prerequisites such as "call `issues.list` first to get an id"). Loaded on demand, never in the index. _(minLen=1; maxLen=60000)_
        - `authorizationScopes` — array — Extra OAuth scopes this tool needs. The runtime unions these across the tools a grant enables to derive the connection's scope set; nothing is declared at the connector level.
          - _array of_ `string`
    - `deprecated` — boolean — Whether new instances should avoid this definition.
    - `replacedBy` — ConnectorDefinitionRef — Reference to one immutable connector definition.
      - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
      - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
- Errors: `400`, `401`, `403`, `404`, `500`

#### `POST` `/v2/tools/connector-definitions/{key}/versions/{version}/configuration`

Resolves account-dependent configuration fields from current form values. By default the
definition-level configuration contract is resolved; pass `toolId` to resolve a connector
tool's per-tool configuration contract instead.

- operationId: `ResolveConnectorConfiguration`
- **Scopes**: `tools:ResolveConnectorConfiguration`, `tools:read`
- **Parameters**
  - `key` (path) — string **(required)** — Stable connector definition key. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
  - `version` (path) — string **(required)** — Exact immutable definition version. _(minLen=1; maxLen=64)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `toolId` (query) — string — When set, resolve the per-tool configuration contract of this connector tool (`ConnectorTool.configuration`) instead of the definition-level configuration. _(pattern=^[a-zA-Z0-9._:-]+$; minLen=1; maxLen=256)_
- **Request body** (`application/json` — `ResolveConnectorConfigurationRequestContent`) **(required)**
  - `values` — any **(required)** — Current partial form values.
  - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
    - _oneOf_ — exactly one of:
      - **`shared`**
        - `shared` — ConnectorSharedAuthorization **(required)** — Company-managed connection resolved through wilma-secrets.
          - `connection` — ConnectionRef **(required)** — A reference to a connection, held by other services in place of the credential. Resolved to a short-lived token server-to-server via GetConnectionToken.
            - `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
      - **`user`**
        - `user` — ConnectorUserAuthorization **(required)** — Marker selecting per-user authorization. Carries no connection reference: at execution the executing user's own credential for this connector's provider is resolved through wilma-secrets (GetUserConnectionToken by provider + user).
  - `user` — string — Executing user when user authorization is selected. _(minLen=1; maxLen=256)_
- **Response 200** (`ResolveConnectorConfigurationResponseContent`)
  - `configuration` — ConnectorConfigurationDefinition **(required)** — Configuration contract rendered by management clients and validated by the service.
    - `schema` — any **(required)** — JSON Schema 2020-12 document describing persisted configuration.
    - `uiSchema` — any — Presentation hints for a compatible JSON Schema form renderer.
- Errors: `400`, `401`, `403`, `404`, `500`

#### `GET` `/v2/tools/connectors`

Lists configured connectors owned by the current company.

- operationId: `ListConnectors`
- **Scopes**: `tools:ListConnectors`, `tools:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `limit` (query) — number _(min=1; max=100)_
  - `cursor` (query) — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- **Response 200** (`ListConnectorsResponseContent`)
  - `connectors` — array **(required)** — Connectors in the current page.
    - _array of_ `Connector`
      - `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
        - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
        - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
      - `configuration` — any **(required)** — Values validated against the definition configuration schema.
      - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
        - _oneOf_ — exactly one of:
          - **`shared`**
            - `shared` — ConnectorSharedAuthorization **(required)** — Company-managed connection resolved through wilma-secrets.
              - `connection` — ConnectionRef **(required)** — A reference to a connection, held by other services in place of the credential. Resolved to a short-lived token server-to-server via GetConnectionToken.
                - _(nesting depth limit — see `ConnectionRef` in the Schemas appendix)_
          - **`user`**
            - `user` — ConnectorUserAuthorization **(required)** — Marker selecting per-user authorization. Carries no connection reference: at execution the executing user's own credential for this connector's provider is resolved through wilma-secrets (GetUserConnectionToken by provider + user).
      - `name` — string **(required)** — Name exposed to administrators and AI agents. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
      - `description` — string **(required)** — Description exposed to administrators and AI agents. _(minLen=1; maxLen=4096)_
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
      - `id` — string **(required)** — Unique connector instance identifier. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `companyId` — string **(required)** — Company that owns this connector. _(minLen=3; maxLen=30)_
      - `revision` — number **(required)** — Monotonic revision, incremented on every update. Pass it back on update for optimistic locking.
  - `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- Errors: `400`, `401`, `403`, `404`, `500`

#### `POST` `/v2/tools/connectors`

Creates a company-owned connector from a server definition.

- operationId: `CreateConnector`
- **Scopes**: `tools:CreateConnector`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `CreateConnectorRequestContent`) **(required)**
  - `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
    - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
    - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
  - `configuration` — any **(required)** — Values validated against the definition configuration schema.
  - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
    - _oneOf_ — exactly one of:
      - **`shared`**
        - `shared` — ConnectorSharedAuthorization **(required)** — Company-managed connection resolved through wilma-secrets.
          - `connection` — ConnectionRef **(required)** — A reference to a connection, held by other services in place of the credential. Resolved to a short-lived token server-to-server via GetConnectionToken.
            - `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
      - **`user`**
        - `user` — ConnectorUserAuthorization **(required)** — Marker selecting per-user authorization. Carries no connection reference: at execution the executing user's own credential for this connector's provider is resolved through wilma-secrets (GetUserConnectionToken by provider + user).
  - `name` — string **(required)** — Name exposed to administrators and AI agents. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
  - `description` — string **(required)** — Description exposed to administrators and AI agents. _(minLen=1; maxLen=4096)_
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
- **Response 201** (`CreateConnectorResponseContent`)
  - `connector` — Connector **(required)** — Company-owned configured connector. Edited in place: there is no draft/publish lifecycle and no version history, because the contract the model works against is already immutable — it comes from the pinned `definition` (see `ConnectorDefinitionRef`), not from this record. Config edits take effect immediately, and `grant` and `authorization` are always read live, so narrowing a permission or revoking a credential applies at once to every agent using the connector. Change history is available from wilma-audit.
    - `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
      - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
      - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
    - `configuration` — any **(required)** — Values validated against the definition configuration schema.
    - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
      - _oneOf_ — exactly one of:
        - **`shared`**
          - `shared` — ConnectorSharedAuthorization **(required)** — Company-managed connection resolved through wilma-secrets.
            - `connection` — ConnectionRef **(required)** — A reference to a connection, held by other services in place of the credential. Resolved to a short-lived token server-to-server via GetConnectionToken.
              - `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
        - **`user`**
          - `user` — ConnectorUserAuthorization **(required)** — Marker selecting per-user authorization. Carries no connection reference: at execution the executing user's own credential for this connector's provider is resolved through wilma-secrets (GetUserConnectionToken by provider + user).
    - `name` — string **(required)** — Name exposed to administrators and AI agents. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
    - `description` — string **(required)** — Description exposed to administrators and AI agents. _(minLen=1; maxLen=4096)_
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
    - `id` — string **(required)** — Unique connector instance identifier. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `companyId` — string **(required)** — Company that owns this connector. _(minLen=3; maxLen=30)_
    - `revision` — number **(required)** — Monotonic revision, incremented on every update. Pass it back on update for optimistic locking.
- Errors: `400`, `401`, `403`, `404`, `500`

#### `POST` `/v2/tools/connectors/describe`

Describes configured connectors by id for agent load; callers pass only `companyId` and
the connector ids. Returns the compact data needed to register each connector's meta-tool.

- operationId: `DescribeConnectors`
- **Scopes**: `tools:DescribeConnectors`, `tools:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `DescribeConnectorsRequestContent`) **(required)**
  - `ids` — array **(required)** — Configured connector instance identifiers.
    - _array of_ `string`
- **Response 200** (`DescribeConnectorsResponseContent`)
  - `descriptions` — array **(required)** — Connector descriptions, one per requested id.
    - _array of_ `ConnectorDescription`
      - `id` — string **(required)** — Connector instance identifier. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `name` — string **(required)** — Connector name exposed to administrators and AI agents. Used as the meta-tool name. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
      - `description` — string **(required)** — Connector description exposed to administrators and AI agents. Used as the meta-tool description, which points the model at the `help` action. _(minLen=1; maxLen=4096)_
- Errors: `400`, `401`, `403`, `404`, `500`

#### `GET` `/v2/tools/connectors/items/{connectorId}`

Gets a configured connector.

- operationId: `GetConnector`
- **Scopes**: `tools:GetConnector`, `tools:read`
- **Parameters**
  - `connectorId` (path) — string **(required)** — Connector instance identifier. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetConnectorResponseContent`)
  - `connector` — Connector **(required)** — Company-owned configured connector. Edited in place: there is no draft/publish lifecycle and no version history, because the contract the model works against is already immutable — it comes from the pinned `definition` (see `ConnectorDefinitionRef`), not from this record. Config edits take effect immediately, and `grant` and `authorization` are always read live, so narrowing a permission or revoking a credential applies at once to every agent using the connector. Change history is available from wilma-audit.
    - `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
      - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
      - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
    - `configuration` — any **(required)** — Values validated against the definition configuration schema.
    - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
      - _oneOf_ — exactly one of:
        - **`shared`**
          - `shared` — ConnectorSharedAuthorization **(required)** — Company-managed connection resolved through wilma-secrets.
            - `connection` — ConnectionRef **(required)** — A reference to a connection, held by other services in place of the credential. Resolved to a short-lived token server-to-server via GetConnectionToken.
              - `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
        - **`user`**
          - `user` — ConnectorUserAuthorization **(required)** — Marker selecting per-user authorization. Carries no connection reference: at execution the executing user's own credential for this connector's provider is resolved through wilma-secrets (GetUserConnectionToken by provider + user).
    - `name` — string **(required)** — Name exposed to administrators and AI agents. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
    - `description` — string **(required)** — Description exposed to administrators and AI agents. _(minLen=1; maxLen=4096)_
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
    - `id` — string **(required)** — Unique connector instance identifier. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `companyId` — string **(required)** — Company that owns this connector. _(minLen=3; maxLen=30)_
    - `revision` — number **(required)** — Monotonic revision, incremented on every update. Pass it back on update for optimistic locking.
- Errors: `400`, `401`, `403`, `404`, `500`

#### `PUT` `/v2/tools/connectors/items/{connectorId}`

Replaces the editable configuration of a connector.

- operationId: `UpdateConnector`
- **Scopes**: `tools:UpdateConnector`
- **Parameters**
  - `connectorId` (path) — string **(required)** — Connector instance identifier. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `UpdateConnectorRequestContent`) **(required)**
  - `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
    - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
    - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
  - `configuration` — any **(required)** — Values validated against the definition configuration schema.
  - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
    - _oneOf_ — exactly one of:
      - **`shared`**
        - `shared` — ConnectorSharedAuthorization **(required)** — Company-managed connection resolved through wilma-secrets.
          - `connection` — ConnectionRef **(required)** — A reference to a connection, held by other services in place of the credential. Resolved to a short-lived token server-to-server via GetConnectionToken.
            - `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
      - **`user`**
        - `user` — ConnectorUserAuthorization **(required)** — Marker selecting per-user authorization. Carries no connection reference: at execution the executing user's own credential for this connector's provider is resolved through wilma-secrets (GetUserConnectionToken by provider + user).
  - `name` — string **(required)** — Name exposed to administrators and AI agents. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
  - `description` — string **(required)** — Description exposed to administrators and AI agents. _(minLen=1; maxLen=4096)_
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
  - `revision` — number **(required)** — Connector revision this update is based on (optimistic locking). When it does not match the current revision, RevisionConflictException is returned.
- **Response 200** (`UpdateConnectorResponseContent`)
  - `connector` — Connector **(required)** — Company-owned configured connector. Edited in place: there is no draft/publish lifecycle and no version history, because the contract the model works against is already immutable — it comes from the pinned `definition` (see `ConnectorDefinitionRef`), not from this record. Config edits take effect immediately, and `grant` and `authorization` are always read live, so narrowing a permission or revoking a credential applies at once to every agent using the connector. Change history is available from wilma-audit.
    - `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
      - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
      - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
    - `configuration` — any **(required)** — Values validated against the definition configuration schema.
    - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
      - _oneOf_ — exactly one of:
        - **`shared`**
          - `shared` — ConnectorSharedAuthorization **(required)** — Company-managed connection resolved through wilma-secrets.
            - `connection` — ConnectionRef **(required)** — A reference to a connection, held by other services in place of the credential. Resolved to a short-lived token server-to-server via GetConnectionToken.
              - `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
        - **`user`**
          - `user` — ConnectorUserAuthorization **(required)** — Marker selecting per-user authorization. Carries no connection reference: at execution the executing user's own credential for this connector's provider is resolved through wilma-secrets (GetUserConnectionToken by provider + user).
    - `name` — string **(required)** — Name exposed to administrators and AI agents. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
    - `description` — string **(required)** — Description exposed to administrators and AI agents. _(minLen=1; maxLen=4096)_
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
    - `id` — string **(required)** — Unique connector instance identifier. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `companyId` — string **(required)** — Company that owns this connector. _(minLen=3; maxLen=30)_
    - `revision` — number **(required)** — Monotonic revision, incremented on every update. Pass it back on update for optimistic locking.
- Errors: `400`, `401`, `403`, `404`, `409`, `500`

#### `DELETE` `/v2/tools/connectors/items/{connectorId}`

Deletes a configured connector. Fails with ConflictException while the connector is referenced
by any agent or skill (see the wilma-audit QueryReferences operation for who references it).

- operationId: `DeleteConnector`
- **Scopes**: `tools:DeleteConnector`
- **Parameters**
  - `connectorId` (path) — string **(required)** — Connector instance identifier. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- Errors: `400`, `401`, `403`, `404`, `409`, `500`

#### `POST` `/v2/tools/connectors/items/{connectorId}/execute`

Executes a connector with the invocation payload supplied by the model or agent.

- operationId: `ExecuteConnector`
- **Scopes**: `tools:ExecuteConnector`
- **Parameters**
  - `connectorId` (path) — string **(required)** — Connector instance identifier. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `ExecuteConnectorRequestContent`) **(required)**
  - `input` — any **(required)** — Invocation payload from the model or agent. For multi-tool connectors this is typically an object with exactly one connector tool id key and argument object. `help` is a reserved action returning guidance in `result.output`; nothing external is dispatched, and a definition must not declare a tool with id `help`: - `{"help": {}}` — index: the connector's `instructions`, the enabled actions grouped by `category` (id, name, one-line description, access), and the list of reference documents (name + summary). - `{"help": {"action": "<toolId>"}}` — detail for one action: full input schema, `examples`, and `docs`. - `{"help": {"reference": "<name>"}}` — the full body of one reference document. - `{"help": {"category": "<name>"}}` — details for every action in a category.
  - `service` — string — Service executing the connector, such as `chatbots` or `voicebots`. _(minLen=1; maxLen=256)_
  - `user` — string — User identity required by user-authorized connectors. _(minLen=1; maxLen=256)_
- **Response 200** (`ExecuteConnectorResponseContent`)
  - `result` — ConnectorExecutionResult **(required)** — Result of executing a connector.
    - `output` — any **(required)** — Structured tool output.
    - `executionId` — string **(required)** — Identifier the connector broker stamps on this dispatch, for correlating its own logs. Distinct from `traceId`, which addresses the run recorded in wilma-traces.
    - `traceId` — string — Trace recording this execution in wilma-traces — the action dispatched, its input and its output. Read it with the wilma-traces GetTrace operation. Minted for this call and returned only here, so it is what ties an administrator's report of a misbehaving connector to the run behind it. `executionId` correlates the broker's own logs and is not accepted by the traces API. _(minLen=1; maxLen=128)_
    - `definitionVersion` — string **(required)** — Definition version used for validation and execution. _(minLen=1; maxLen=64)_
- Errors: `400`, `401`, `403`, `404`, `500`

#### `POST` `/v2/tools/describe`

Describe multiple tools for agent load. Each reference either pins a published version or resolves the tool's latestVersion; the resolved version is reported on every description. A tool with no published version is not describable.

- operationId: `DescribeTools`
- **Scopes**: `tools:DescribeTools`, `tools:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `DescribeToolsRequestContent`) **(required)**
  - `tools` — array **(required)** — Tools to describe, each optionally pinned to a published version.
    - _array of_ `ToolRef`
      - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `version` — number — Pin a specific published tool version. When omitted, latestVersion is resolved. _(min=1)_
- **Response 200** (`DescribeToolsResponseContent`)
  - `descriptions` — array **(required)** — Tool descriptions, corresponding positionally to the requested `tools`.
    - _array of_ `ToolDescription`
      - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `version` — number **(required)** — Published tool version this description was resolved from: the pinned version when the request carried one, otherwise the latestVersion at resolution time. Pass it back on ExecuteTool so the call runs against the same definition the model was shown. _(min=1)_
      - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
      - `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
      - `schema` — any — JSON Schema (2020-12) of the tool arguments, matching Tool.input.schema. Absent for tools that take no arguments.
- Errors: `400`, `401`, `403`, `404`, `500`

#### `POST` `/v2/tools/discover`

Discover tools from an MCP server.

- operationId: `DiscoverTools`
- **Scopes**: `tools:DiscoverTools`, `tools:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `DiscoverToolsRequestContent`) **(required)**
  - `serverUrl` — string **(required)** — MCP server endpoint URL
  - `authorization` — union
    - _oneOf_ — exactly one of:
      - **`connection`**
        - `connection` — ConnectionRef **(required)** — A reference to a connection, held by other services in place of the credential. Resolved to a short-lived token server-to-server via GetConnectionToken.
          - `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
      - **`customHeaders`**
        - `customHeaders` — ToolMcpHeadersMap **(required)**
          - _map of_ `string`
      - **`apiKey`**
        - `apiKey` — ToolMcpApiKeyAuthorization **(required)** — A SecretRef plus the header it travels under. The referenced secret is expected to carry variant `auth_api_key`; the value is resolved server-to-server at execution and never stored on the tool.
          - `secret` — SecretRef **(required)** — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
            - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
          - `headerName` — string **(required)** — Header the key is sent under, e.g. `X-API-Key` or `PRIVATE-TOKEN`. _(pattern=^[!#$%&'*+.^_`|~0-9A-Za-z-]+$; minLen=1; maxLen=128)_
          - `prefix` — string — Prepended to the value verbatim, for the rare API wanting `Token abc123`.
      - **`user`**
        - `user` — ToolMcpUserAuthorization **(required)** — Marker selecting per-user MCP authorization. Carries no reference: the credential is keyed by server and user.
- **Response 200** (`DiscoverToolsResponseContent`)
  - `tools` — array **(required)** — Tools discovered on the MCP server.
    - _array of_ `DiscoveredTool`
      - `name` — string **(required)** — Name of the tool on the MCP server
      - `description` — string **(required)** — Description of the tool
      - `inputSchema` — any **(required)** — JSON Schema for the tool's input parameters
- Errors: `400`, `401`, `403`, `404`, `500`

#### `POST` `/v2/tools/execute`

Execute a tool with the provided input.

- operationId: `ExecuteTool`
- **Scopes**: `tools:ExecuteTool`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `ExecuteToolRequestContent`) **(required)**
  - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `version` — number — Published tool version to execute. Mutually exclusive with draft. Pass the `version` reported by DescribeTools so the call runs against the definition the model was shown; when omitted, latestVersion is resolved at execution time. _(min=1)_
  - `draft` — boolean — Run the tool's current draft (for testing). Mutually exclusive with version. The draft is still never *offered* to a model — DescribeTools reports a tool with no published version as unresolvable either way — so only a caller that names this flag can reach one. It selects which definition executes and nothing else: a draft run of a write or destructive tool has exactly the effect a published run would, and is audited the same.
  - `input` — any **(required)** — Tool arguments, validated against the input schema of the executed version.
  - `service` — string — Service executing the tool, e.g. 'chatbots'. _(minLen=1; maxLen=256)_
  - `user` — string — User for whom the tool is executed, e.g. 'john.doe@example.com'. _(minLen=1; maxLen=256)_
- **Response 200** (`ExecuteToolResponseContent`)
  - `result` — ToolExecutionResult **(required)**
    - `traceId` — string — Trace recording this execution in wilma-traces — the handler that ran, the input it was called with and the output it returned. Read it with the wilma-traces GetTrace operation. Minted for this call and returned only here. Unlike a session's trace it cannot be reconstructed from any id the caller already holds, so a test run that does not keep this value can afterwards be found only by searching QueryTraces on `tool.id` and time. _(minLen=1; maxLen=128)_
    - `output` — any **(required)** — Output of the tool execution
    - `version` — number — Published tool version that executed: the pinned version when the call carried one, otherwise the latestVersion resolved at execution time. Absent when draft is true, because a draft has no version. _(min=1)_
    - `draft` — boolean — True when the call executed the tool's mutable draft (draft on ExecuteTool).
    - `revision` — number — Draft revision that executed when draft is true; correlates a run with the exact draft state, which `version` cannot because a draft moves under its own name.
- Errors: `400`, `401`, `403`, `404`, `500`

#### `GET` `/v2/tools/items/{toolId}`

Get a tool's draft by its ID, including its version state. Use GetToolVersion to read a published version's definition.

- operationId: `GetTool`
- **Scopes**: `tools:GetTool`, `tools:read`
- **Parameters**
  - `toolId` (path) — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetToolResponseContent`)
  - `tool` — Tool **(required)** — A company-owned tool. UpdateTool edits the mutable draft; PublishToolVersion snapshots it into an immutable version that agent and skill capabilities resolve.
    - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
    - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
    - `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
    - `input` — ToolInput
      - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
    - `handler` — union **(required)** — Handler of the tool. Every tool executes through one of three mechanisms: a pinned connector definition (built-in providers such as email, webhook, search, chat, sms, calendar — and external integrations — share the same contract), an MCP server registration, or a single tool on a registered MCP server.
      - _oneOf_ — exactly one of:
        - **`connector`**
          - `connector` — ToolConnectorHandler **(required)** — Handler for a connector-backed Tool created through `CreateTool`. Carries two configuration layers: `configuration` (from the mixin) holds definition-level values for the connector as a whole (validated against the definition `configuration.schema`), while `toolConfiguration` holds values specific to this created Tool (validated against the pinned connector tool's `configuration.schema`). `Tool.input` follows copy-at-create semantics: when `input` is omitted on create, the service snapshots the pinned connector tool's input schema into the Tool; callers may instead provide — and later edit — a custom schema. The Tool owns its copy; definition changes never propagate to existing tools. Reshaping the input of a tool whose handler does not consume input through configuration templates fails at execution, not at write.
            - `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
              - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
              - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
            - `configuration` — any **(required)** — Values validated against the definition configuration schema.
            - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
              - _oneOf_ — exactly one of:
                - **`shared`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`user`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `toolId` — string **(required)** — Connector tool from the pinned definition executed by this Tool. _(pattern=^[a-zA-Z0-9._:-]+$; minLen=1; maxLen=256)_
            - `toolConfiguration` — any — Values validated against the pinned connector tool's per-tool configuration schema (`ConnectorTool.configuration.schema`). Omitted when that tool declares no per-tool configuration contract.
        - **`mcp`**
          - `mcp` — ToolMcpHandler **(required)**
            - `serverUrl` — string **(required)** — MCP server endpoint URL
            - `authorization` — union
              - _oneOf_ — exactly one of:
                - **`connection`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`customHeaders`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`apiKey`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`user`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `tools` — array **(required)** — Tools enabled for this MCP server.
              - _array of_ `string`
        - **`mcpTool`**
          - `mcpTool` — ToolMcpToolHandler **(required)**
            - `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
            - `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.
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
    - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
    - `latestVersion` — number — Latest published version number, resolved by capabilities that omit a version pin. Absent while the tool is still a draft. _(min=1)_
- Errors: `400`, `401`, `403`, `404`, `500`

#### `PUT` `/v2/tools/items/{toolId}`

Update the draft definition of a tool. Published versions are never affected, so nothing the model sees changes until the draft is published.

- operationId: `UpdateTool`
- **Scopes**: `tools:UpdateTool`
- **Parameters**
  - `toolId` (path) — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `UpdateToolRequestContent`) **(required)**
  - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
  - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
  - `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
  - `input` — ToolInput
    - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
  - `handler` — union **(required)** — Handler of the tool. Every tool executes through one of three mechanisms: a pinned connector definition (built-in providers such as email, webhook, search, chat, sms, calendar — and external integrations — share the same contract), an MCP server registration, or a single tool on a registered MCP server.
    - _oneOf_ — exactly one of:
      - **`connector`**
        - `connector` — ToolConnectorHandler **(required)** — Handler for a connector-backed Tool created through `CreateTool`. Carries two configuration layers: `configuration` (from the mixin) holds definition-level values for the connector as a whole (validated against the definition `configuration.schema`), while `toolConfiguration` holds values specific to this created Tool (validated against the pinned connector tool's `configuration.schema`). `Tool.input` follows copy-at-create semantics: when `input` is omitted on create, the service snapshots the pinned connector tool's input schema into the Tool; callers may instead provide — and later edit — a custom schema. The Tool owns its copy; definition changes never propagate to existing tools. Reshaping the input of a tool whose handler does not consume input through configuration templates fails at execution, not at write.
          - `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
            - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
            - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
          - `configuration` — any **(required)** — Values validated against the definition configuration schema.
          - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
            - _oneOf_ — exactly one of:
              - **`shared`**
                - `shared` — ConnectorSharedAuthorization **(required)** — Company-managed connection resolved through wilma-secrets.
                  - _(nesting depth limit — see `ConnectorSharedAuthorization` in the Schemas appendix)_
              - **`user`**
                - `user` — ConnectorUserAuthorization **(required)** — Marker selecting per-user authorization. Carries no connection reference: at execution the executing user's own credential for this connector's provider is resolved through wilma-secrets (GetUserConnectionToken by provider + user).
          - `toolId` — string **(required)** — Connector tool from the pinned definition executed by this Tool. _(pattern=^[a-zA-Z0-9._:-]+$; minLen=1; maxLen=256)_
          - `toolConfiguration` — any — Values validated against the pinned connector tool's per-tool configuration schema (`ConnectorTool.configuration.schema`). Omitted when that tool declares no per-tool configuration contract.
      - **`mcp`**
        - `mcp` — ToolMcpHandler **(required)**
          - `serverUrl` — string **(required)** — MCP server endpoint URL
          - `authorization` — union
            - _oneOf_ — exactly one of:
              - **`connection`**
                - `connection` — ConnectionRef **(required)** — A reference to a connection, held by other services in place of the credential. Resolved to a short-lived token server-to-server via GetConnectionToken.
                  - _(nesting depth limit — see `ConnectionRef` in the Schemas appendix)_
              - **`customHeaders`**
                - `customHeaders` — ToolMcpHeadersMap **(required)**
                  - _(nesting depth limit — see `ToolMcpHeadersMap` in the Schemas appendix)_
              - **`apiKey`**
                - `apiKey` — ToolMcpApiKeyAuthorization **(required)** — A SecretRef plus the header it travels under. The referenced secret is expected to carry variant `auth_api_key`; the value is resolved server-to-server at execution and never stored on the tool.
                  - _(nesting depth limit — see `ToolMcpApiKeyAuthorization` in the Schemas appendix)_
              - **`user`**
                - `user` — ToolMcpUserAuthorization **(required)** — Marker selecting per-user MCP authorization. Carries no reference: the credential is keyed by server and user.
          - `tools` — array **(required)** — Tools enabled for this MCP server.
            - _array of_ `string`
      - **`mcpTool`**
        - `mcpTool` — ToolMcpToolHandler **(required)**
          - `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
          - `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.
  - `revision` — number **(required)** — Draft revision this update is based on (optimistic locking). When it does not match the current revision, RevisionConflictException is returned.
- **Response 200** (`UpdateToolResponseContent`)
  - `tool` — Tool **(required)** — A company-owned tool. UpdateTool edits the mutable draft; PublishToolVersion snapshots it into an immutable version that agent and skill capabilities resolve.
    - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
    - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
    - `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
    - `input` — ToolInput
      - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
    - `handler` — union **(required)** — Handler of the tool. Every tool executes through one of three mechanisms: a pinned connector definition (built-in providers such as email, webhook, search, chat, sms, calendar — and external integrations — share the same contract), an MCP server registration, or a single tool on a registered MCP server.
      - _oneOf_ — exactly one of:
        - **`connector`**
          - `connector` — ToolConnectorHandler **(required)** — Handler for a connector-backed Tool created through `CreateTool`. Carries two configuration layers: `configuration` (from the mixin) holds definition-level values for the connector as a whole (validated against the definition `configuration.schema`), while `toolConfiguration` holds values specific to this created Tool (validated against the pinned connector tool's `configuration.schema`). `Tool.input` follows copy-at-create semantics: when `input` is omitted on create, the service snapshots the pinned connector tool's input schema into the Tool; callers may instead provide — and later edit — a custom schema. The Tool owns its copy; definition changes never propagate to existing tools. Reshaping the input of a tool whose handler does not consume input through configuration templates fails at execution, not at write.
            - `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
              - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
              - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
            - `configuration` — any **(required)** — Values validated against the definition configuration schema.
            - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
              - _oneOf_ — exactly one of:
                - **`shared`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`user`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `toolId` — string **(required)** — Connector tool from the pinned definition executed by this Tool. _(pattern=^[a-zA-Z0-9._:-]+$; minLen=1; maxLen=256)_
            - `toolConfiguration` — any — Values validated against the pinned connector tool's per-tool configuration schema (`ConnectorTool.configuration.schema`). Omitted when that tool declares no per-tool configuration contract.
        - **`mcp`**
          - `mcp` — ToolMcpHandler **(required)**
            - `serverUrl` — string **(required)** — MCP server endpoint URL
            - `authorization` — union
              - _oneOf_ — exactly one of:
                - **`connection`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`customHeaders`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`apiKey`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`user`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `tools` — array **(required)** — Tools enabled for this MCP server.
              - _array of_ `string`
        - **`mcpTool`**
          - `mcpTool` — ToolMcpToolHandler **(required)**
            - `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
            - `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.
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
    - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
    - `latestVersion` — number — Latest published version number, resolved by capabilities that omit a version pin. Absent while the tool is still a draft. _(min=1)_
- Errors: `400`, `401`, `403`, `404`, `409`, `500`

#### `DELETE` `/v2/tools/items/{toolId}`

Delete a tool, its draft and its version history. Fails with ConflictException while the tool is referenced by any agent or skill (see the wilma-audit QueryReferences operation for who references it).

- operationId: `DeleteTool`
- **Scopes**: `tools:DeleteTool`
- **Parameters**
  - `toolId` (path) — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- Errors: `400`, `401`, `403`, `404`, `409`, `500`

### Versions

#### `GET` `/v2/tools/items/{toolId}/compare-versions`

Returns the field-level differences between two versions, or between a version and the current draft.

- operationId: `CompareToolVersions`
- **Scopes**: `tools:CompareToolVersions`, `tools:read`
- **Parameters**
  - `toolId` (path) — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `from` (query) — number — Base published version number. Omit when fromDraft is true. _(min=1)_
  - `fromDraft` (query) — boolean — Use the current draft as the base instead of a published version.
  - `to` (query) — number — Target published version number. Omit when toDraft is true. _(min=1)_
  - `toDraft` (query) — boolean — Compare against the current draft instead of a published version.
- **Response 200** (`CompareToolVersionsResponseContent`)
  - `changes` — array **(required)**
    - _array of_ `ToolVersionChange`
      - `path` — string **(required)** — JSON pointer of the changed field within the tool definition, e.g. '/description' or '/input/schema/properties/subject'.
      - `before` — any — Value before the change (absent when the field was added).
      - `after` — any — Value after the change (absent when the field was removed).
- Errors: `400`, `401`, `403`, `404`, `500`

#### `GET` `/v2/tools/items/{toolId}/versions`

Lists the published versions of a tool, newest first.

- operationId: `ListToolVersions`
- **Scopes**: `tools:ListToolVersions`, `tools:read`
- **Parameters**
  - `toolId` (path) — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `limit` (query) — number _(min=1; max=100)_
  - `cursor` (query) — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- **Response 200** (`ListToolVersionsResponseContent`)
  - `versions` — array **(required)**
    - _array of_ `ToolVersionInfo`
      - `toolId` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `version` — number **(required)** — Published tool version number. Monotonic within a tool's version history, starting at 1. _(min=1)_
      - `changelog` — string — Human-readable description of what changed in a published version. _(minLen=1; maxLen=500)_
      - `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
      - `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
        - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
        - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
        - `name` — string — Human readable name of the actor at the time of the action.
      - `latest` — boolean — True when this version is the tool's latestVersion.
  - `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- Errors: `400`, `401`, `403`, `404`, `500`

#### `POST` `/v2/tools/items/{toolId}/versions`

Publishes the current draft as a new immutable version and updates latestVersion. Agent and skill capabilities that omit a version pin resolve latestVersion on their next load.

- operationId: `PublishToolVersion`
- **Scopes**: `tools:PublishToolVersion`
- **Parameters**
  - `toolId` (path) — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `PublishToolVersionRequestContent`) **(required)**
  - `changelog` — string — What changed in this version. _(minLen=1; maxLen=500)_
  - `revision` — number **(required)** — Draft revision this publish is based on (optimistic locking).
- **Response 200** (`PublishToolVersionResponseContent`)
  - `version` — ToolVersion **(required)** — A published tool version: an immutable snapshot of the tool definition at publish time.
    - `toolId` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `version` — number **(required)** — Published tool version number. Monotonic within a tool's version history, starting at 1. _(min=1)_
    - `changelog` — string — What changed in this version, provided at publish time. _(minLen=1; maxLen=500)_
    - `definition` — ToolDefinitionSnapshot **(required)** — Immutable tool definition snapshot captured at publish time. A connector-backed handler carries its pinned ConnectorDefinitionRef, so the snapshot is self-contained; `authorization` is exempt — credentials are always resolved from the current connection at execution time, never pinned.
      - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
      - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
      - `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
      - `input` — ToolInput
        - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
      - `handler` — union **(required)** — Handler of the tool. Every tool executes through one of three mechanisms: a pinned connector definition (built-in providers such as email, webhook, search, chat, sms, calendar — and external integrations — share the same contract), an MCP server registration, or a single tool on a registered MCP server.
        - _oneOf_ — exactly one of:
          - **`connector`**
            - `connector` — ToolConnectorHandler **(required)** — Handler for a connector-backed Tool created through `CreateTool`. Carries two configuration layers: `configuration` (from the mixin) holds definition-level values for the connector as a whole (validated against the definition `configuration.schema`), while `toolConfiguration` holds values specific to this created Tool (validated against the pinned connector tool's `configuration.schema`). `Tool.input` follows copy-at-create semantics: when `input` is omitted on create, the service snapshots the pinned connector tool's input schema into the Tool; callers may instead provide — and later edit — a custom schema. The Tool owns its copy; definition changes never propagate to existing tools. Reshaping the input of a tool whose handler does not consume input through configuration templates fails at execution, not at write.
              - `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
                - _(nesting depth limit — see `ConnectorDefinitionRef` in the Schemas appendix)_
              - `configuration` — any **(required)** — Values validated against the definition configuration schema.
              - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
                - _(nesting depth limit — see `ConnectorAuthorization` in the Schemas appendix)_
              - `toolId` — string **(required)** — Connector tool from the pinned definition executed by this Tool. _(pattern=^[a-zA-Z0-9._:-]+$; minLen=1; maxLen=256)_
              - `toolConfiguration` — any — Values validated against the pinned connector tool's per-tool configuration schema (`ConnectorTool.configuration.schema`). Omitted when that tool declares no per-tool configuration contract.
          - **`mcp`**
            - `mcp` — ToolMcpHandler **(required)**
              - `serverUrl` — string **(required)** — MCP server endpoint URL
              - `authorization` — union
                - _(nesting depth limit — see `ToolMcpAuthorization` in the Schemas appendix)_
              - `tools` — array **(required)** — Tools enabled for this MCP server.
                - _array of_ `string`
          - **`mcpTool`**
            - `mcpTool` — ToolMcpToolHandler **(required)**
              - `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
              - `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.
    - `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
- Errors: `400`, `401`, `403`, `404`, `409`, `500`

#### `GET` `/v2/tools/items/{toolId}/versions/{version}`

Retrieves a published tool version, including its full immutable definition snapshot.

- operationId: `GetToolVersion`
- **Scopes**: `tools:GetToolVersion`, `tools:read`
- **Parameters**
  - `toolId` (path) — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `version` (path) — number **(required)** — Published tool version number. Monotonic within a tool's version history, starting at 1. _(min=1)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetToolVersionResponseContent`)
  - `version` — ToolVersion **(required)** — A published tool version: an immutable snapshot of the tool definition at publish time.
    - `toolId` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `version` — number **(required)** — Published tool version number. Monotonic within a tool's version history, starting at 1. _(min=1)_
    - `changelog` — string — What changed in this version, provided at publish time. _(minLen=1; maxLen=500)_
    - `definition` — ToolDefinitionSnapshot **(required)** — Immutable tool definition snapshot captured at publish time. A connector-backed handler carries its pinned ConnectorDefinitionRef, so the snapshot is self-contained; `authorization` is exempt — credentials are always resolved from the current connection at execution time, never pinned.
      - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
      - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
      - `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
      - `input` — ToolInput
        - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
      - `handler` — union **(required)** — Handler of the tool. Every tool executes through one of three mechanisms: a pinned connector definition (built-in providers such as email, webhook, search, chat, sms, calendar — and external integrations — share the same contract), an MCP server registration, or a single tool on a registered MCP server.
        - _oneOf_ — exactly one of:
          - **`connector`**
            - `connector` — ToolConnectorHandler **(required)** — Handler for a connector-backed Tool created through `CreateTool`. Carries two configuration layers: `configuration` (from the mixin) holds definition-level values for the connector as a whole (validated against the definition `configuration.schema`), while `toolConfiguration` holds values specific to this created Tool (validated against the pinned connector tool's `configuration.schema`). `Tool.input` follows copy-at-create semantics: when `input` is omitted on create, the service snapshots the pinned connector tool's input schema into the Tool; callers may instead provide — and later edit — a custom schema. The Tool owns its copy; definition changes never propagate to existing tools. Reshaping the input of a tool whose handler does not consume input through configuration templates fails at execution, not at write.
              - `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
                - _(nesting depth limit — see `ConnectorDefinitionRef` in the Schemas appendix)_
              - `configuration` — any **(required)** — Values validated against the definition configuration schema.
              - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
                - _(nesting depth limit — see `ConnectorAuthorization` in the Schemas appendix)_
              - `toolId` — string **(required)** — Connector tool from the pinned definition executed by this Tool. _(pattern=^[a-zA-Z0-9._:-]+$; minLen=1; maxLen=256)_
              - `toolConfiguration` — any — Values validated against the pinned connector tool's per-tool configuration schema (`ConnectorTool.configuration.schema`). Omitted when that tool declares no per-tool configuration contract.
          - **`mcp`**
            - `mcp` — ToolMcpHandler **(required)**
              - `serverUrl` — string **(required)** — MCP server endpoint URL
              - `authorization` — union
                - _(nesting depth limit — see `ToolMcpAuthorization` in the Schemas appendix)_
              - `tools` — array **(required)** — Tools enabled for this MCP server.
                - _array of_ `string`
          - **`mcpTool`**
            - `mcpTool` — ToolMcpToolHandler **(required)**
              - `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
              - `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.
    - `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
- Errors: `400`, `401`, `403`, `404`, `500`

#### `POST` `/v2/tools/items/{toolId}/versions/{version}/draft`

Replaces the mutable draft with a published version's definition. The draft revision is incremented; published versions and latestVersion are unchanged until the draft is published.

- operationId: `RestoreToolVersionToDraft`
- **Scopes**: `tools:RestoreToolVersionToDraft`
- **Parameters**
  - `toolId` (path) — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `version` (path) — number **(required)** — Published tool version number. Monotonic within a tool's version history, starting at 1. _(min=1)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `RestoreToolVersionToDraftRequestContent`) **(required)**
  - `revision` — number **(required)** — Draft revision this restore is based on (optimistic locking).
- **Response 200** (`RestoreToolVersionToDraftResponseContent`)
  - `tool` — Tool **(required)** — A company-owned tool. UpdateTool edits the mutable draft; PublishToolVersion snapshots it into an immutable version that agent and skill capabilities resolve.
    - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
    - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
    - `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
    - `input` — ToolInput
      - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
    - `handler` — union **(required)** — Handler of the tool. Every tool executes through one of three mechanisms: a pinned connector definition (built-in providers such as email, webhook, search, chat, sms, calendar — and external integrations — share the same contract), an MCP server registration, or a single tool on a registered MCP server.
      - _oneOf_ — exactly one of:
        - **`connector`**
          - `connector` — ToolConnectorHandler **(required)** — Handler for a connector-backed Tool created through `CreateTool`. Carries two configuration layers: `configuration` (from the mixin) holds definition-level values for the connector as a whole (validated against the definition `configuration.schema`), while `toolConfiguration` holds values specific to this created Tool (validated against the pinned connector tool's `configuration.schema`). `Tool.input` follows copy-at-create semantics: when `input` is omitted on create, the service snapshots the pinned connector tool's input schema into the Tool; callers may instead provide — and later edit — a custom schema. The Tool owns its copy; definition changes never propagate to existing tools. Reshaping the input of a tool whose handler does not consume input through configuration templates fails at execution, not at write.
            - `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
              - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
              - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
            - `configuration` — any **(required)** — Values validated against the definition configuration schema.
            - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
              - _oneOf_ — exactly one of:
                - **`shared`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`user`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `toolId` — string **(required)** — Connector tool from the pinned definition executed by this Tool. _(pattern=^[a-zA-Z0-9._:-]+$; minLen=1; maxLen=256)_
            - `toolConfiguration` — any — Values validated against the pinned connector tool's per-tool configuration schema (`ConnectorTool.configuration.schema`). Omitted when that tool declares no per-tool configuration contract.
        - **`mcp`**
          - `mcp` — ToolMcpHandler **(required)**
            - `serverUrl` — string **(required)** — MCP server endpoint URL
            - `authorization` — union
              - _oneOf_ — exactly one of:
                - **`connection`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`customHeaders`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`apiKey`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`user`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `tools` — array **(required)** — Tools enabled for this MCP server.
              - _array of_ `string`
        - **`mcpTool`**
          - `mcpTool` — ToolMcpToolHandler **(required)**
            - `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
            - `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.
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
    - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
    - `latestVersion` — number — Latest published version number, resolved by capabilities that omit a version pin. Absent while the tool is still a draft. _(min=1)_
- Errors: `400`, `401`, `403`, `404`, `409`, `500`

### Mentions

#### `GET` `/v2/tools/mentions/resolve`

Reads the current content of one referenced resource for an agent. Service-only. With `user`, the source is read with that user's permissions; without it, with company-wide access. Fails with `ValidationException` when the URI names no resource kind that can be read, `NotFoundException` when the resource does not exist, `ForbiddenException` when the user, or the company without a user, may not read it, and `ServiceUnavailableException` when its source failed to answer and a later read may succeed.

- operationId: `ResolveMention`
- **Scopes**: `tools:ResolveMention`, `tools:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `uri` (query) — string **(required)** — Canonical URI identifying one entity on the Wilma platform, e.g. 'wilma://agents/UXDT1W9fI3sj' or 'wilma://skills/aB3dE5fG7hJ9'. The path names the owning service and entity kind. Opaque to the contracts that carry it; non-Wilma schemes (records of external systems) fit the same shape. _(pattern=^[a-z][a-z0-9+.-]*://.+$; minLen=1; maxLen=512)_
  - `user` (query) — string — The user whose permissions apply. Omit for company-wide access. _(minLen=12; maxLen=12)_
- **Response 200** (`ResolveMentionResponseContent`)
  - `title` — string **(required)** — Display title of the resource.
  - `data` — any **(required)** — Resource content, one shape per resource kind, named by `data.kind`. Sections the source has not produced yet are listed in `data.unavailable`.
- Errors: `400`, `401`, `403`, `404`, `500`, `503`

### Schemas appendix — Wilma Tools API

<details><summary>89 component schemas</summary>

**`Actor`**

_Who performed an action: an interactive user, an API key or an internal service._

- `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
- `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
- `name` — string — Human readable name of the actor at the time of the action.

**`ActorType`**

- string _(enum: `user`, `api_key`, `service`)_

**`AlreadyExistExceptionResponseContent`**

- `message` — string **(required)**

**`CapabilityDescription`**

_Description of one wilma-tools-backed capability, tagged by kind. Entries correspond positionally to the requested `CapabilityRefs`._

- _oneOf_ — exactly one of:
  - **`tool`**
    - `tool` — ToolDescription **(required)**
      - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `version` — number **(required)** — Published tool version this description was resolved from: the pinned version when the request carried one, otherwise the latestVersion at resolution time. Pass it back on ExecuteTool so the call runs against the same definition the model was shown. _(min=1)_
      - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
      - `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
      - `schema` — any — JSON Schema (2020-12) of the tool arguments, matching Tool.input.schema. Absent for tools that take no arguments.
  - **`connector`**
    - `connector` — ConnectorDescription **(required)** — Compact connector description used to build the model-facing connector meta-tool at agent load time. The detailed action catalogue and usage guidance are obtained at runtime via the connector's reserved `help` action (`ExecuteConnector`); the full definition is available from `GetConnectorDefinition`.
      - `id` — string **(required)** — Connector instance identifier. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `name` — string **(required)** — Connector name exposed to administrators and AI agents. Used as the meta-tool name. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
      - `description` — string **(required)** — Connector description exposed to administrators and AI agents. Used as the meta-tool description, which points the model at the `help` action. _(minLen=1; maxLen=4096)_

**`CapabilityRef`**

_Reference to one wilma-tools-backed agent capability to describe: either a standalone Tool or a configured Connector. The two members are deliberately asymmetric. A Tool is a model-facing contract — its input schema is what the model fills, and agents pin JSON Pointers into it — so it is versioned and referenced by `ToolRef`. A Connector exposes no schema at reference time: the model discovers actions at runtime through the reserved `help` action, and every action, schema and document it can reach is already frozen by the connector's pinned `ConnectorDefinitionRef`. A configured connector therefore needs no version history of its own and is referenced by id._

- _oneOf_ — exactly one of:
  - **`tool`**
    - `tool` — ToolRef **(required)** — Reference to one tool, optionally pinned to a published version. When `version` is omitted the tool's latestVersion is resolved.
      - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `version` — number — Pin a specific published tool version. When omitted, latestVersion is resolved. _(min=1)_
  - **`connector`**
    - `connector` — string **(required)** — Configured connector instance identifier. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_

**`CompareToolVersionsResponseContent`**

- `changes` — array **(required)**
  - _array of_ `ToolVersionChange`
    - `path` — string **(required)** — JSON pointer of the changed field within the tool definition, e.g. '/description' or '/input/schema/properties/subject'.
    - `before` — any — Value before the change (absent when the field was added).
    - `after` — any — Value after the change (absent when the field was removed).

**`ConflictExceptionResponseContent`**

_The request conflicts with the current state of the resource, e.g. a duplicate name, a resource still in use, or an unmet precondition._

- `message` — string **(required)**

**`ConnectionRef`**

_A reference to a connection, held by other services in place of the credential. Resolved to a short-lived token server-to-server via GetConnectionToken._

- `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_

**`Connector`**

_Company-owned configured connector. Edited in place: there is no draft/publish lifecycle and no version history, because the contract the model works against is already immutable — it comes from the pinned `definition` (see `ConnectorDefinitionRef`), not from this record. Config edits take effect immediately, and `grant` and `authorization` are always read live, so narrowing a permission or revoking a credential applies at once to every agent using the connector. Change history is available from wilma-audit._

- `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
  - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
  - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
- `configuration` — any **(required)** — Values validated against the definition configuration schema.
- `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
  - _oneOf_ — exactly one of:
    - **`shared`**
      - `shared` — ConnectorSharedAuthorization **(required)** — Company-managed connection resolved through wilma-secrets.
        - `connection` — ConnectionRef **(required)** — A reference to a connection, held by other services in place of the credential. Resolved to a short-lived token server-to-server via GetConnectionToken.
          - _(nesting depth limit — see `ConnectionRef` in the Schemas appendix)_
    - **`user`**
      - `user` — ConnectorUserAuthorization **(required)** — Marker selecting per-user authorization. Carries no connection reference: at execution the executing user's own credential for this connector's provider is resolved through wilma-secrets (GetUserConnectionToken by provider + user).
- `name` — string **(required)** — Name exposed to administrators and AI agents. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
- `description` — string **(required)** — Description exposed to administrators and AI agents. _(minLen=1; maxLen=4096)_
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
- `id` — string **(required)** — Unique connector instance identifier. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
- `companyId` — string **(required)** — Company that owns this connector. _(minLen=3; maxLen=30)_
- `revision` — number **(required)** — Monotonic revision, incremented on every update. Pass it back on update for optimistic locking.

**`ConnectorAuthorization`**

_Credential selection for a configured connector. Credentials remain in wilma-secrets._

- _oneOf_ — exactly one of:
  - **`shared`**
    - `shared` — ConnectorSharedAuthorization **(required)** — Company-managed connection resolved through wilma-secrets.
      - `connection` — ConnectionRef **(required)** — A reference to a connection, held by other services in place of the credential. Resolved to a short-lived token server-to-server via GetConnectionToken.
        - `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - **`user`**
    - `user` — ConnectorUserAuthorization **(required)** — Marker selecting per-user authorization. Carries no connection reference: at execution the executing user's own credential for this connector's provider is resolved through wilma-secrets (GetUserConnectionToken by provider + user).

**`ConnectorAuthorizationDefinition`**

_Authorization requirements declared by a connector definition. Scopes are not declared here: the connection's OAuth scope set is derived from the tools the `ConnectorToolGrant` enables (the union of their `authorizationScopes`) plus the provider's default scopes._

- `provider` — string **(required)** — Provider key the connector authenticates against, e.g. `salesforce`.
- `modes` — array **(required)** — Credential resolution modes supported by this connector.
  - _array of_ `ConnectorAuthorizationMode`
- `connectionConfiguration` — ConnectorConfigurationDefinition — Configuration contract rendered by management clients and validated by the service.
  - `schema` — any **(required)** — JSON Schema 2020-12 document describing persisted configuration.
  - `uiSchema` — any — Presentation hints for a compatible JSON Schema form renderer.

**`ConnectorAuthorizationMode`**

_Supported credential resolution mode. Mirrors wilma-secrets `ConnectionType`._

- string _(enum: `shared`, `user`)_

**`ConnectorConfigurationDefinition`**

_Configuration contract rendered by management clients and validated by the service._

- `schema` — any **(required)** — JSON Schema 2020-12 document describing persisted configuration.
- `uiSchema` — any — Presentation hints for a compatible JSON Schema form renderer.

**`ConnectorDefinition`**

_Immutable server-owned connector definition. Both external integrations (e.g. `sentry`) and built-in tool providers (e.g. `email`, `webhook`, `search`, `chat`, `sms`, `calendar`) are published through this shape and served from the same catalog. A breaking change to a configuration or input schema publishes a new version; tools pinned to older versions keep working._

- `ref` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
  - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
  - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
- `metadata` — ConnectorMetadata **(required)** — Display metadata for a connector catalog entry.
  - `title` — string **(required)** — Human-readable connector name.
  - `description` — string **(required)** — Summary of the external system and supported use cases.
  - `icon` — string — Icon URL or renderer-known icon key.
  - `category` — string — Catalog category used for discovery and filtering.
  - `documentationUrl` — string — Link to external connector documentation.
- `configuration` — ConnectorConfigurationDefinition **(required)** — Configuration contract rendered by management clients and validated by the service.
  - `schema` — any **(required)** — JSON Schema 2020-12 document describing persisted configuration.
  - `uiSchema` — any — Presentation hints for a compatible JSON Schema form renderer.
- `authorization` — ConnectorAuthorizationDefinition — Authorization requirements declared by a connector definition. Scopes are not declared here: the connection's OAuth scope set is derived from the tools the `ConnectorToolGrant` enables (the union of their `authorizationScopes`) plus the provider's default scopes.
  - `provider` — string **(required)** — Provider key the connector authenticates against, e.g. `salesforce`.
  - `modes` — array **(required)** — Credential resolution modes supported by this connector.
    - _array of_ `ConnectorAuthorizationMode`
  - `connectionConfiguration` — ConnectorConfigurationDefinition — Configuration contract rendered by management clients and validated by the service.
    - `schema` — any **(required)** — JSON Schema 2020-12 document describing persisted configuration.
    - `uiSchema` — any — Presentation hints for a compatible JSON Schema form renderer.
- `instructions` — string — Main help document (Markdown), returned first via `{"help": {}}`: what the connector is for, how to work with it, and how its tools fit together. Orientation only — the service appends the per-grant action index and the list of reference documents automatically; deep material belongs in `references`. _(minLen=1; maxLen=60000)_
- `references` — array — On-demand reference documents, listed (name + summary) in the `help` index and loaded individually by name.
  - _array of_ `ConnectorReference`
    - `name` — string **(required)** — Load key, unique within the definition. _(pattern=^[a-z][a-z0-9-]*$; minLen=1; maxLen=128)_
    - `title` — string **(required)** — Human-readable title.
    - `summary` — string **(required)** — One-line summary shown in the `help` index so the model can decide whether to load it.
    - `content` — string **(required)** — Full Markdown body, returned only when the model loads this reference by name. _(minLen=1; maxLen=60000)_
- `tools` — array **(required)** — Tools available in this definition version.
  - _array of_ `ConnectorTool`
    - `id` — string **(required)** — Stable dispatch identifier used in `ExecuteConnector` input keys. _(pattern=^[a-zA-Z0-9._:-]+$; minLen=1; maxLen=256)_
    - `name` — string **(required)** — Agent-facing tool name. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
    - `description` — string **(required)** — One-line description used by people and AI agents to select the tool. Shown in the `help` index; extended guidance goes in `docs`. _(minLen=1; maxLen=4096)_
    - `access` — string **(required)** — Authoritative access class of a connector tool. Server-enforced: it drives the coarse `ConnectorToolGrant` (Allow read / Allow write / Full access), the scopes derived at connection time, and the default approval behavior. _(enum: `read`, `write`, `destructive`)_
    - `idempotent` — boolean — Whether repeating the call with identical arguments has no additional effect (retry-safe).
    - `category` — string — Optional grouping used to organize large catalogs in the `help` index and management UI (e.g. "Issues", "Pull requests"). Not an access control.
    - `input` — ToolInput **(required)**
      - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
    - `configuration` — ConnectorConfigurationDefinition — Configuration contract rendered by management clients and validated by the service.
      - `schema` — any **(required)** — JSON Schema 2020-12 document describing persisted configuration.
      - `uiSchema` — any — Presentation hints for a compatible JSON Schema form renderer.
    - `examples` — array — Worked examples returned in this tool's `help` detail. Teach argument shape and common call patterns; not shown in the `help` index.
      - _array of_ `string`
    - `docs` — string — Long-form Markdown usage notes returned in this tool's `help` detail (edge cases, field semantics, prerequisites such as "call `issues.list` first to get an id"). Loaded on demand, never in the index. _(minLen=1; maxLen=60000)_
    - `authorizationScopes` — array — Extra OAuth scopes this tool needs. The runtime unions these across the tools a grant enables to derive the connection's scope set; nothing is declared at the connector level.
      - _array of_ `string`
- `deprecated` — boolean — Whether new instances should avoid this definition.
- `replacedBy` — ConnectorDefinitionRef — Reference to one immutable connector definition.
  - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
  - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_

**`ConnectorDefinitionRef`**

_Reference to one immutable connector definition._

- `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
- `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_

**`ConnectorDescription`**

_Compact connector description used to build the model-facing connector meta-tool at agent load time. The detailed action catalogue and usage guidance are obtained at runtime via the connector's reserved `help` action (`ExecuteConnector`); the full definition is available from `GetConnectorDefinition`._

- `id` — string **(required)** — Connector instance identifier. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
- `name` — string **(required)** — Connector name exposed to administrators and AI agents. Used as the meta-tool name. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
- `description` — string **(required)** — Connector description exposed to administrators and AI agents. Used as the meta-tool description, which points the model at the `help` action. _(minLen=1; maxLen=4096)_

**`ConnectorExecutionResult`**

_Result of executing a connector._

- `output` — any **(required)** — Structured tool output.
- `executionId` — string **(required)** — Identifier the connector broker stamps on this dispatch, for correlating its own logs. Distinct from `traceId`, which addresses the run recorded in wilma-traces.
- `traceId` — string — Trace recording this execution in wilma-traces — the action dispatched, its input and its output. Read it with the wilma-traces GetTrace operation. Minted for this call and returned only here, so it is what ties an administrator's report of a misbehaving connector to the run behind it. `executionId` correlates the broker's own logs and is not accepted by the traces API. _(minLen=1; maxLen=128)_
- `definitionVersion` — string **(required)** — Definition version used for validation and execution. _(minLen=1; maxLen=64)_

**`ConnectorGrantAll`**

_Marker: grant every tool, including DESTRUCTIVE._

- ConnectorGrantAll

**`ConnectorGrantRead`**

_Marker: grant every READ tool._

- ConnectorGrantRead

**`ConnectorGrantReadWrite`**

_Marker: grant every READ and WRITE tool._

- ConnectorGrantReadWrite

**`ConnectorMetadata`**

_Display metadata for a connector catalog entry._

- `title` — string **(required)** — Human-readable connector name.
- `description` — string **(required)** — Summary of the external system and supported use cases.
- `icon` — string — Icon URL or renderer-known icon key.
- `category` — string — Catalog category used for discovery and filtering.
- `documentationUrl` — string — Link to external connector documentation.

**`ConnectorReference`**

_A named, on-demand help document. The `help` index lists each reference's `name` + `summary`; the model loads a document's `content` with `{"help": {"reference": "..."}}`._

- `name` — string **(required)** — Load key, unique within the definition. _(pattern=^[a-z][a-z0-9-]*$; minLen=1; maxLen=128)_
- `title` — string **(required)** — Human-readable title.
- `summary` — string **(required)** — One-line summary shown in the `help` index so the model can decide whether to load it.
- `content` — string **(required)** — Full Markdown body, returned only when the model loads this reference by name. _(minLen=1; maxLen=60000)_

**`ConnectorSharedAuthorization`**

_Company-managed connection resolved through wilma-secrets._

- `connection` — ConnectionRef **(required)** — A reference to a connection, held by other services in place of the credential. Resolved to a short-lived token server-to-server via GetConnectionToken.
  - `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_

**`ConnectorTool`**

_Tool exposed by a connector definition._

- `id` — string **(required)** — Stable dispatch identifier used in `ExecuteConnector` input keys. _(pattern=^[a-zA-Z0-9._:-]+$; minLen=1; maxLen=256)_
- `name` — string **(required)** — Agent-facing tool name. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
- `description` — string **(required)** — One-line description used by people and AI agents to select the tool. Shown in the `help` index; extended guidance goes in `docs`. _(minLen=1; maxLen=4096)_
- `access` — string **(required)** — Authoritative access class of a connector tool. Server-enforced: it drives the coarse `ConnectorToolGrant` (Allow read / Allow write / Full access), the scopes derived at connection time, and the default approval behavior. _(enum: `read`, `write`, `destructive`)_
- `idempotent` — boolean — Whether repeating the call with identical arguments has no additional effect (retry-safe).
- `category` — string — Optional grouping used to organize large catalogs in the `help` index and management UI (e.g. "Issues", "Pull requests"). Not an access control.
- `input` — ToolInput **(required)**
  - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
- `configuration` — ConnectorConfigurationDefinition — Configuration contract rendered by management clients and validated by the service.
  - `schema` — any **(required)** — JSON Schema 2020-12 document describing persisted configuration.
  - `uiSchema` — any — Presentation hints for a compatible JSON Schema form renderer.
- `examples` — array — Worked examples returned in this tool's `help` detail. Teach argument shape and common call patterns; not shown in the `help` index.
  - _array of_ `string`
- `docs` — string — Long-form Markdown usage notes returned in this tool's `help` detail (edge cases, field semantics, prerequisites such as "call `issues.list` first to get an id"). Loaded on demand, never in the index. _(minLen=1; maxLen=60000)_
- `authorizationScopes` — array — Extra OAuth scopes this tool needs. The runtime unions these across the tools a grant enables to derive the connection's scope set; nothing is declared at the connector level.
  - _array of_ `string`

**`ConnectorToolAccess`**

_Authoritative access class of a connector tool. Server-enforced: it drives the coarse `ConnectorToolGrant` (Allow read / Allow write / Full access), the scopes derived at connection time, and the default approval behavior._

- string _(enum: `read`, `write`, `destructive`)_

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

**`ConnectorUserAuthorization`**

_Marker selecting per-user authorization. Carries no connection reference: at execution the executing user's own credential for this connector's provider is resolved through wilma-secrets (GetUserConnectionToken by provider + user)._

- ConnectorUserAuthorization

**`CreateConnectorRequestContent`**

_Fields supplied when a connector is created or replaced._

- `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
  - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
  - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
- `configuration` — any **(required)** — Values validated against the definition configuration schema.
- `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
  - _oneOf_ — exactly one of:
    - **`shared`**
      - `shared` — ConnectorSharedAuthorization **(required)** — Company-managed connection resolved through wilma-secrets.
        - `connection` — ConnectionRef **(required)** — A reference to a connection, held by other services in place of the credential. Resolved to a short-lived token server-to-server via GetConnectionToken.
          - _(nesting depth limit — see `ConnectionRef` in the Schemas appendix)_
    - **`user`**
      - `user` — ConnectorUserAuthorization **(required)** — Marker selecting per-user authorization. Carries no connection reference: at execution the executing user's own credential for this connector's provider is resolved through wilma-secrets (GetUserConnectionToken by provider + user).
- `name` — string **(required)** — Name exposed to administrators and AI agents. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
- `description` — string **(required)** — Description exposed to administrators and AI agents. _(minLen=1; maxLen=4096)_
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

**`CreateConnectorResponseContent`**

- `connector` — Connector **(required)** — Company-owned configured connector. Edited in place: there is no draft/publish lifecycle and no version history, because the contract the model works against is already immutable — it comes from the pinned `definition` (see `ConnectorDefinitionRef`), not from this record. Config edits take effect immediately, and `grant` and `authorization` are always read live, so narrowing a permission or revoking a credential applies at once to every agent using the connector. Change history is available from wilma-audit.
  - `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
    - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
    - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
  - `configuration` — any **(required)** — Values validated against the definition configuration schema.
  - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
    - _oneOf_ — exactly one of:
      - **`shared`**
        - `shared` — ConnectorSharedAuthorization **(required)** — Company-managed connection resolved through wilma-secrets.
          - _(nesting depth limit — see `ConnectorSharedAuthorization` in the Schemas appendix)_
      - **`user`**
        - `user` — ConnectorUserAuthorization **(required)** — Marker selecting per-user authorization. Carries no connection reference: at execution the executing user's own credential for this connector's provider is resolved through wilma-secrets (GetUserConnectionToken by provider + user).
  - `name` — string **(required)** — Name exposed to administrators and AI agents. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
  - `description` — string **(required)** — Description exposed to administrators and AI agents. _(minLen=1; maxLen=4096)_
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
  - `id` — string **(required)** — Unique connector instance identifier. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `companyId` — string **(required)** — Company that owns this connector. _(minLen=3; maxLen=30)_
  - `revision` — number **(required)** — Monotonic revision, incremented on every update. Pass it back on update for optimistic locking.

**`CreateToolRequestContent`**

_The complete, versionable configuration of a tool. This is what gets snapshotted when a version is published._

- `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
- `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
- `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
- `input` — ToolInput
  - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
- `handler` — union **(required)** — Handler of the tool. Every tool executes through one of three mechanisms: a pinned connector definition (built-in providers such as email, webhook, search, chat, sms, calendar — and external integrations — share the same contract), an MCP server registration, or a single tool on a registered MCP server.
  - _oneOf_ — exactly one of:
    - **`connector`**
      - `connector` — ToolConnectorHandler **(required)** — Handler for a connector-backed Tool created through `CreateTool`. Carries two configuration layers: `configuration` (from the mixin) holds definition-level values for the connector as a whole (validated against the definition `configuration.schema`), while `toolConfiguration` holds values specific to this created Tool (validated against the pinned connector tool's `configuration.schema`). `Tool.input` follows copy-at-create semantics: when `input` is omitted on create, the service snapshots the pinned connector tool's input schema into the Tool; callers may instead provide — and later edit — a custom schema. The Tool owns its copy; definition changes never propagate to existing tools. Reshaping the input of a tool whose handler does not consume input through configuration templates fails at execution, not at write.
        - `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
          - _(nesting depth limit — see `ConnectorDefinitionRef` in the Schemas appendix)_
        - `configuration` — any **(required)** — Values validated against the definition configuration schema.
        - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
          - _(nesting depth limit — see `ConnectorAuthorization` in the Schemas appendix)_
        - `toolId` — string **(required)** — Connector tool from the pinned definition executed by this Tool. _(pattern=^[a-zA-Z0-9._:-]+$; minLen=1; maxLen=256)_
        - `toolConfiguration` — any — Values validated against the pinned connector tool's per-tool configuration schema (`ConnectorTool.configuration.schema`). Omitted when that tool declares no per-tool configuration contract.
    - **`mcp`**
      - `mcp` — ToolMcpHandler **(required)**
        - `serverUrl` — string **(required)** — MCP server endpoint URL
        - `authorization` — union
          - _(nesting depth limit — see `ToolMcpAuthorization` in the Schemas appendix)_
        - `tools` — array **(required)** — Tools enabled for this MCP server.
          - _array of_ `string`
    - **`mcpTool`**
      - `mcpTool` — ToolMcpToolHandler **(required)**
        - `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
        - `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.

**`CreateToolResponseContent`**

- `tool` — Tool **(required)** — A company-owned tool. UpdateTool edits the mutable draft; PublishToolVersion snapshots it into an immutable version that agent and skill capabilities resolve.
  - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
  - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
  - `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
  - `input` — ToolInput
    - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
  - `handler` — union **(required)** — Handler of the tool. Every tool executes through one of three mechanisms: a pinned connector definition (built-in providers such as email, webhook, search, chat, sms, calendar — and external integrations — share the same contract), an MCP server registration, or a single tool on a registered MCP server.
    - _oneOf_ — exactly one of:
      - **`connector`**
        - `connector` — ToolConnectorHandler **(required)** — Handler for a connector-backed Tool created through `CreateTool`. Carries two configuration layers: `configuration` (from the mixin) holds definition-level values for the connector as a whole (validated against the definition `configuration.schema`), while `toolConfiguration` holds values specific to this created Tool (validated against the pinned connector tool's `configuration.schema`). `Tool.input` follows copy-at-create semantics: when `input` is omitted on create, the service snapshots the pinned connector tool's input schema into the Tool; callers may instead provide — and later edit — a custom schema. The Tool owns its copy; definition changes never propagate to existing tools. Reshaping the input of a tool whose handler does not consume input through configuration templates fails at execution, not at write.
          - _(nesting depth limit — see `ToolConnectorHandler` in the Schemas appendix)_
      - **`mcp`**
        - `mcp` — ToolMcpHandler **(required)**
          - _(nesting depth limit — see `ToolMcpHandler` in the Schemas appendix)_
      - **`mcpTool`**
        - `mcpTool` — ToolMcpToolHandler **(required)**
          - _(nesting depth limit — see `ToolMcpToolHandler` in the Schemas appendix)_
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
  - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `status` — string **(required)** _(enum: `draft`, `active`)_
  - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
  - `latestVersion` — number — Latest published version number, resolved by capabilities that omit a version pin. Absent while the tool is still a draft. _(min=1)_

**`DescribeCapabilitiesRequestContent`**

- `capabilities` — array **(required)** — Tool and connector references to describe.
  - _array of_ `CapabilityRef`
    - _oneOf_ — exactly one of:
      - **`tool`**
        - `tool` — ToolRef **(required)** — Reference to one tool, optionally pinned to a published version. When `version` is omitted the tool's latestVersion is resolved.
          - _(nesting depth limit — see `ToolRef` in the Schemas appendix)_
      - **`connector`**
        - `connector` — string **(required)** — Configured connector instance identifier. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_

**`DescribeCapabilitiesResponseContent`**

- `descriptions` — array **(required)** — Capability descriptions, corresponding positionally to the requested `capabilities`.
  - _array of_ `CapabilityDescription`
    - _oneOf_ — exactly one of:
      - **`tool`**
        - `tool` — ToolDescription **(required)**
          - _(nesting depth limit — see `ToolDescription` in the Schemas appendix)_
      - **`connector`**
        - `connector` — ConnectorDescription **(required)** — Compact connector description used to build the model-facing connector meta-tool at agent load time. The detailed action catalogue and usage guidance are obtained at runtime via the connector's reserved `help` action (`ExecuteConnector`); the full definition is available from `GetConnectorDefinition`.
          - _(nesting depth limit — see `ConnectorDescription` in the Schemas appendix)_

**`DescribeConnectorsRequestContent`**

- `ids` — array **(required)** — Configured connector instance identifiers.
  - _array of_ `string`

**`DescribeConnectorsResponseContent`**

- `descriptions` — array **(required)** — Connector descriptions, one per requested id.
  - _array of_ `ConnectorDescription`
    - `id` — string **(required)** — Connector instance identifier. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `name` — string **(required)** — Connector name exposed to administrators and AI agents. Used as the meta-tool name. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
    - `description` — string **(required)** — Connector description exposed to administrators and AI agents. Used as the meta-tool description, which points the model at the `help` action. _(minLen=1; maxLen=4096)_

**`DescribeToolsRequestContent`**

- `tools` — array **(required)** — Tools to describe, each optionally pinned to a published version.
  - _array of_ `ToolRef`
    - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `version` — number — Pin a specific published tool version. When omitted, latestVersion is resolved. _(min=1)_

**`DescribeToolsResponseContent`**

- `descriptions` — array **(required)** — Tool descriptions, corresponding positionally to the requested `tools`.
  - _array of_ `ToolDescription`
    - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `version` — number **(required)** — Published tool version this description was resolved from: the pinned version when the request carried one, otherwise the latestVersion at resolution time. Pass it back on ExecuteTool so the call runs against the same definition the model was shown. _(min=1)_
    - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
    - `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
    - `schema` — any — JSON Schema (2020-12) of the tool arguments, matching Tool.input.schema. Absent for tools that take no arguments.

**`DiscoverToolsRequestContent`**

- `serverUrl` — string **(required)** — MCP server endpoint URL
- `authorization` — union
  - _oneOf_ — exactly one of:
    - **`connection`**
      - `connection` — ConnectionRef **(required)** — A reference to a connection, held by other services in place of the credential. Resolved to a short-lived token server-to-server via GetConnectionToken.
        - `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
    - **`customHeaders`**
      - `customHeaders` — ToolMcpHeadersMap **(required)**
        - _map of_ `string`
    - **`apiKey`**
      - `apiKey` — ToolMcpApiKeyAuthorization **(required)** — A SecretRef plus the header it travels under. The referenced secret is expected to carry variant `auth_api_key`; the value is resolved server-to-server at execution and never stored on the tool.
        - `secret` — SecretRef **(required)** — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
          - _(nesting depth limit — see `SecretRef` in the Schemas appendix)_
        - `headerName` — string **(required)** — Header the key is sent under, e.g. `X-API-Key` or `PRIVATE-TOKEN`. _(pattern=^[!#$%&'*+.^_`|~0-9A-Za-z-]+$; minLen=1; maxLen=128)_
        - `prefix` — string — Prepended to the value verbatim, for the rare API wanting `Token abc123`.
    - **`user`**
      - `user` — ToolMcpUserAuthorization **(required)** — Marker selecting per-user MCP authorization. Carries no reference: the credential is keyed by server and user.

**`DiscoverToolsResponseContent`**

- `tools` — array **(required)** — Tools discovered on the MCP server.
  - _array of_ `DiscoveredTool`
    - `name` — string **(required)** — Name of the tool on the MCP server
    - `description` — string **(required)** — Description of the tool
    - `inputSchema` — any **(required)** — JSON Schema for the tool's input parameters

**`DiscoveredTool`**

- `name` — string **(required)** — Name of the tool on the MCP server
- `description` — string **(required)** — Description of the tool
- `inputSchema` — any **(required)** — JSON Schema for the tool's input parameters

**`ExecuteConnectorRequestContent`**

- `input` — any **(required)** — Invocation payload from the model or agent. For multi-tool connectors this is typically an object with exactly one connector tool id key and argument object. `help` is a reserved action returning guidance in `result.output`; nothing external is dispatched, and a definition must not declare a tool with id `help`: - `{"help": {}}` — index: the connector's `instructions`, the enabled actions grouped by `category` (id, name, one-line description, access), and the list of reference documents (name + summary). - `{"help": {"action": "<toolId>"}}` — detail for one action: full input schema, `examples`, and `docs`. - `{"help": {"reference": "<name>"}}` — the full body of one reference document. - `{"help": {"category": "<name>"}}` — details for every action in a category.
- `service` — string — Service executing the connector, such as `chatbots` or `voicebots`. _(minLen=1; maxLen=256)_
- `user` — string — User identity required by user-authorized connectors. _(minLen=1; maxLen=256)_

**`ExecuteConnectorResponseContent`**

- `result` — ConnectorExecutionResult **(required)** — Result of executing a connector.
  - `output` — any **(required)** — Structured tool output.
  - `executionId` — string **(required)** — Identifier the connector broker stamps on this dispatch, for correlating its own logs. Distinct from `traceId`, which addresses the run recorded in wilma-traces.
  - `traceId` — string — Trace recording this execution in wilma-traces — the action dispatched, its input and its output. Read it with the wilma-traces GetTrace operation. Minted for this call and returned only here, so it is what ties an administrator's report of a misbehaving connector to the run behind it. `executionId` correlates the broker's own logs and is not accepted by the traces API. _(minLen=1; maxLen=128)_
  - `definitionVersion` — string **(required)** — Definition version used for validation and execution. _(minLen=1; maxLen=64)_

**`ExecuteToolRequestContent`**

- `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
- `version` — number — Published tool version to execute. Mutually exclusive with draft. Pass the `version` reported by DescribeTools so the call runs against the definition the model was shown; when omitted, latestVersion is resolved at execution time. _(min=1)_
- `draft` — boolean — Run the tool's current draft (for testing). Mutually exclusive with version. The draft is still never *offered* to a model — DescribeTools reports a tool with no published version as unresolvable either way — so only a caller that names this flag can reach one. It selects which definition executes and nothing else: a draft run of a write or destructive tool has exactly the effect a published run would, and is audited the same.
- `input` — any **(required)** — Tool arguments, validated against the input schema of the executed version.
- `service` — string — Service executing the tool, e.g. 'chatbots'. _(minLen=1; maxLen=256)_
- `user` — string — User for whom the tool is executed, e.g. 'john.doe@example.com'. _(minLen=1; maxLen=256)_

**`ExecuteToolResponseContent`**

- `result` — ToolExecutionResult **(required)**
  - `traceId` — string — Trace recording this execution in wilma-traces — the handler that ran, the input it was called with and the output it returned. Read it with the wilma-traces GetTrace operation. Minted for this call and returned only here. Unlike a session's trace it cannot be reconstructed from any id the caller already holds, so a test run that does not keep this value can afterwards be found only by searching QueryTraces on `tool.id` and time. _(minLen=1; maxLen=128)_
  - `output` — any **(required)** — Output of the tool execution
  - `version` — number — Published tool version that executed: the pinned version when the call carried one, otherwise the latestVersion resolved at execution time. Absent when draft is true, because a draft has no version. _(min=1)_
  - `draft` — boolean — True when the call executed the tool's mutable draft (draft on ExecuteTool).
  - `revision` — number — Draft revision that executed when draft is true; correlates a run with the exact draft state, which `version` cannot because a draft moves under its own name.

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GetConnectorDefinitionResponseContent`**

- `definition` — ConnectorDefinition **(required)** — Immutable server-owned connector definition. Both external integrations (e.g. `sentry`) and built-in tool providers (e.g. `email`, `webhook`, `search`, `chat`, `sms`, `calendar`) are published through this shape and served from the same catalog. A breaking change to a configuration or input schema publishes a new version; tools pinned to older versions keep working.
  - `ref` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
    - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
    - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
  - `metadata` — ConnectorMetadata **(required)** — Display metadata for a connector catalog entry.
    - `title` — string **(required)** — Human-readable connector name.
    - `description` — string **(required)** — Summary of the external system and supported use cases.
    - `icon` — string — Icon URL or renderer-known icon key.
    - `category` — string — Catalog category used for discovery and filtering.
    - `documentationUrl` — string — Link to external connector documentation.
  - `configuration` — ConnectorConfigurationDefinition **(required)** — Configuration contract rendered by management clients and validated by the service.
    - `schema` — any **(required)** — JSON Schema 2020-12 document describing persisted configuration.
    - `uiSchema` — any — Presentation hints for a compatible JSON Schema form renderer.
  - `authorization` — ConnectorAuthorizationDefinition — Authorization requirements declared by a connector definition. Scopes are not declared here: the connection's OAuth scope set is derived from the tools the `ConnectorToolGrant` enables (the union of their `authorizationScopes`) plus the provider's default scopes.
    - `provider` — string **(required)** — Provider key the connector authenticates against, e.g. `salesforce`.
    - `modes` — array **(required)** — Credential resolution modes supported by this connector.
      - _array of_ `ConnectorAuthorizationMode`
    - `connectionConfiguration` — ConnectorConfigurationDefinition — Configuration contract rendered by management clients and validated by the service.
      - `schema` — any **(required)** — JSON Schema 2020-12 document describing persisted configuration.
      - `uiSchema` — any — Presentation hints for a compatible JSON Schema form renderer.
  - `instructions` — string — Main help document (Markdown), returned first via `{"help": {}}`: what the connector is for, how to work with it, and how its tools fit together. Orientation only — the service appends the per-grant action index and the list of reference documents automatically; deep material belongs in `references`. _(minLen=1; maxLen=60000)_
  - `references` — array — On-demand reference documents, listed (name + summary) in the `help` index and loaded individually by name.
    - _array of_ `ConnectorReference`
      - `name` — string **(required)** — Load key, unique within the definition. _(pattern=^[a-z][a-z0-9-]*$; minLen=1; maxLen=128)_
      - `title` — string **(required)** — Human-readable title.
      - `summary` — string **(required)** — One-line summary shown in the `help` index so the model can decide whether to load it.
      - `content` — string **(required)** — Full Markdown body, returned only when the model loads this reference by name. _(minLen=1; maxLen=60000)_
  - `tools` — array **(required)** — Tools available in this definition version.
    - _array of_ `ConnectorTool`
      - `id` — string **(required)** — Stable dispatch identifier used in `ExecuteConnector` input keys. _(pattern=^[a-zA-Z0-9._:-]+$; minLen=1; maxLen=256)_
      - `name` — string **(required)** — Agent-facing tool name. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
      - `description` — string **(required)** — One-line description used by people and AI agents to select the tool. Shown in the `help` index; extended guidance goes in `docs`. _(minLen=1; maxLen=4096)_
      - `access` — string **(required)** — Authoritative access class of a connector tool. Server-enforced: it drives the coarse `ConnectorToolGrant` (Allow read / Allow write / Full access), the scopes derived at connection time, and the default approval behavior. _(enum: `read`, `write`, `destructive`)_
      - `idempotent` — boolean — Whether repeating the call with identical arguments has no additional effect (retry-safe).
      - `category` — string — Optional grouping used to organize large catalogs in the `help` index and management UI (e.g. "Issues", "Pull requests"). Not an access control.
      - `input` — ToolInput **(required)**
        - _(nesting depth limit — see `ToolInput` in the Schemas appendix)_
      - `configuration` — ConnectorConfigurationDefinition — Configuration contract rendered by management clients and validated by the service.
        - _(nesting depth limit — see `ConnectorConfigurationDefinition` in the Schemas appendix)_
      - `examples` — array — Worked examples returned in this tool's `help` detail. Teach argument shape and common call patterns; not shown in the `help` index.
        - _array of_ `string`
      - `docs` — string — Long-form Markdown usage notes returned in this tool's `help` detail (edge cases, field semantics, prerequisites such as "call `issues.list` first to get an id"). Loaded on demand, never in the index. _(minLen=1; maxLen=60000)_
      - `authorizationScopes` — array — Extra OAuth scopes this tool needs. The runtime unions these across the tools a grant enables to derive the connection's scope set; nothing is declared at the connector level.
        - _array of_ `string`
  - `deprecated` — boolean — Whether new instances should avoid this definition.
  - `replacedBy` — ConnectorDefinitionRef — Reference to one immutable connector definition.
    - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
    - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_

**`GetConnectorResponseContent`**

- `connector` — Connector **(required)** — Company-owned configured connector. Edited in place: there is no draft/publish lifecycle and no version history, because the contract the model works against is already immutable — it comes from the pinned `definition` (see `ConnectorDefinitionRef`), not from this record. Config edits take effect immediately, and `grant` and `authorization` are always read live, so narrowing a permission or revoking a credential applies at once to every agent using the connector. Change history is available from wilma-audit.
  - `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
    - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
    - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
  - `configuration` — any **(required)** — Values validated against the definition configuration schema.
  - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
    - _oneOf_ — exactly one of:
      - **`shared`**
        - `shared` — ConnectorSharedAuthorization **(required)** — Company-managed connection resolved through wilma-secrets.
          - _(nesting depth limit — see `ConnectorSharedAuthorization` in the Schemas appendix)_
      - **`user`**
        - `user` — ConnectorUserAuthorization **(required)** — Marker selecting per-user authorization. Carries no connection reference: at execution the executing user's own credential for this connector's provider is resolved through wilma-secrets (GetUserConnectionToken by provider + user).
  - `name` — string **(required)** — Name exposed to administrators and AI agents. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
  - `description` — string **(required)** — Description exposed to administrators and AI agents. _(minLen=1; maxLen=4096)_
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
  - `id` — string **(required)** — Unique connector instance identifier. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `companyId` — string **(required)** — Company that owns this connector. _(minLen=3; maxLen=30)_
  - `revision` — number **(required)** — Monotonic revision, incremented on every update. Pass it back on update for optimistic locking.

**`GetToolResponseContent`**

- `tool` — Tool **(required)** — A company-owned tool. UpdateTool edits the mutable draft; PublishToolVersion snapshots it into an immutable version that agent and skill capabilities resolve.
  - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
  - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
  - `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
  - `input` — ToolInput
    - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
  - `handler` — union **(required)** — Handler of the tool. Every tool executes through one of three mechanisms: a pinned connector definition (built-in providers such as email, webhook, search, chat, sms, calendar — and external integrations — share the same contract), an MCP server registration, or a single tool on a registered MCP server.
    - _oneOf_ — exactly one of:
      - **`connector`**
        - `connector` — ToolConnectorHandler **(required)** — Handler for a connector-backed Tool created through `CreateTool`. Carries two configuration layers: `configuration` (from the mixin) holds definition-level values for the connector as a whole (validated against the definition `configuration.schema`), while `toolConfiguration` holds values specific to this created Tool (validated against the pinned connector tool's `configuration.schema`). `Tool.input` follows copy-at-create semantics: when `input` is omitted on create, the service snapshots the pinned connector tool's input schema into the Tool; callers may instead provide — and later edit — a custom schema. The Tool owns its copy; definition changes never propagate to existing tools. Reshaping the input of a tool whose handler does not consume input through configuration templates fails at execution, not at write.
          - _(nesting depth limit — see `ToolConnectorHandler` in the Schemas appendix)_
      - **`mcp`**
        - `mcp` — ToolMcpHandler **(required)**
          - _(nesting depth limit — see `ToolMcpHandler` in the Schemas appendix)_
      - **`mcpTool`**
        - `mcpTool` — ToolMcpToolHandler **(required)**
          - _(nesting depth limit — see `ToolMcpToolHandler` in the Schemas appendix)_
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
  - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `status` — string **(required)** _(enum: `draft`, `active`)_
  - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
  - `latestVersion` — number — Latest published version number, resolved by capabilities that omit a version pin. Absent while the tool is still a draft. _(min=1)_

**`GetToolVersionResponseContent`**

- `version` — ToolVersion **(required)** — A published tool version: an immutable snapshot of the tool definition at publish time.
  - `toolId` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `version` — number **(required)** — Published tool version number. Monotonic within a tool's version history, starting at 1. _(min=1)_
  - `changelog` — string — What changed in this version, provided at publish time. _(minLen=1; maxLen=500)_
  - `definition` — ToolDefinitionSnapshot **(required)** — Immutable tool definition snapshot captured at publish time. A connector-backed handler carries its pinned ConnectorDefinitionRef, so the snapshot is self-contained; `authorization` is exempt — credentials are always resolved from the current connection at execution time, never pinned.
    - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
    - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
    - `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
    - `input` — ToolInput
      - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
    - `handler` — union **(required)** — Handler of the tool. Every tool executes through one of three mechanisms: a pinned connector definition (built-in providers such as email, webhook, search, chat, sms, calendar — and external integrations — share the same contract), an MCP server registration, or a single tool on a registered MCP server.
      - _oneOf_ — exactly one of:
        - **`connector`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`mcp`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`mcpTool`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
    - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
    - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
    - `name` — string — Human readable name of the actor at the time of the action.

**`ListConnectorDefinitionsResponseContent`**

- `definitions` — array **(required)** — Connector definitions in the current page.
  - _array of_ `ConnectorDefinition`
    - `ref` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
      - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
      - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
    - `metadata` — ConnectorMetadata **(required)** — Display metadata for a connector catalog entry.
      - `title` — string **(required)** — Human-readable connector name.
      - `description` — string **(required)** — Summary of the external system and supported use cases.
      - `icon` — string — Icon URL or renderer-known icon key.
      - `category` — string — Catalog category used for discovery and filtering.
      - `documentationUrl` — string — Link to external connector documentation.
    - `configuration` — ConnectorConfigurationDefinition **(required)** — Configuration contract rendered by management clients and validated by the service.
      - `schema` — any **(required)** — JSON Schema 2020-12 document describing persisted configuration.
      - `uiSchema` — any — Presentation hints for a compatible JSON Schema form renderer.
    - `authorization` — ConnectorAuthorizationDefinition — Authorization requirements declared by a connector definition. Scopes are not declared here: the connection's OAuth scope set is derived from the tools the `ConnectorToolGrant` enables (the union of their `authorizationScopes`) plus the provider's default scopes.
      - `provider` — string **(required)** — Provider key the connector authenticates against, e.g. `salesforce`.
      - `modes` — array **(required)** — Credential resolution modes supported by this connector.
        - _(nesting depth limit — see `ConnectorAuthorizationMode` in the Schemas appendix)_
      - `connectionConfiguration` — ConnectorConfigurationDefinition — Configuration contract rendered by management clients and validated by the service.
        - _(nesting depth limit — see `ConnectorConfigurationDefinition` in the Schemas appendix)_
    - `instructions` — string — Main help document (Markdown), returned first via `{"help": {}}`: what the connector is for, how to work with it, and how its tools fit together. Orientation only — the service appends the per-grant action index and the list of reference documents automatically; deep material belongs in `references`. _(minLen=1; maxLen=60000)_
    - `references` — array — On-demand reference documents, listed (name + summary) in the `help` index and loaded individually by name.
      - _array of_ `ConnectorReference`
        - _(nesting depth limit — see `ConnectorReference` in the Schemas appendix)_
    - `tools` — array **(required)** — Tools available in this definition version.
      - _array of_ `ConnectorTool`
        - _(nesting depth limit — see `ConnectorTool` in the Schemas appendix)_
    - `deprecated` — boolean — Whether new instances should avoid this definition.
    - `replacedBy` — ConnectorDefinitionRef — Reference to one immutable connector definition.
      - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
      - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
- `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_

**`ListConnectorsResponseContent`**

- `connectors` — array **(required)** — Connectors in the current page.
  - _array of_ `Connector`
    - `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
      - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
      - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
    - `configuration` — any **(required)** — Values validated against the definition configuration schema.
    - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
      - _oneOf_ — exactly one of:
        - **`shared`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`user`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `name` — string **(required)** — Name exposed to administrators and AI agents. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
    - `description` — string **(required)** — Description exposed to administrators and AI agents. _(minLen=1; maxLen=4096)_
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
    - `id` — string **(required)** — Unique connector instance identifier. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `companyId` — string **(required)** — Company that owns this connector. _(minLen=3; maxLen=30)_
    - `revision` — number **(required)** — Monotonic revision, incremented on every update. Pass it back on update for optimistic locking.
- `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_

**`ListToolVersionsResponseContent`**

- `versions` — array **(required)**
  - _array of_ `ToolVersionInfo`
    - `toolId` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `version` — number **(required)** — Published tool version number. Monotonic within a tool's version history, starting at 1. _(min=1)_
    - `changelog` — string — Human-readable description of what changed in a published version. _(minLen=1; maxLen=500)_
    - `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
    - `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
      - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
      - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
      - `name` — string — Human readable name of the actor at the time of the action.
    - `latest` — boolean — True when this version is the tool's latestVersion.
- `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_

**`ListToolsResponseContent`**

- `tools` — array **(required)**
  - _array of_ `Tool`
    - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
    - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
    - `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
    - `input` — ToolInput
      - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
    - `handler` — union **(required)** — Handler of the tool. Every tool executes through one of three mechanisms: a pinned connector definition (built-in providers such as email, webhook, search, chat, sms, calendar — and external integrations — share the same contract), an MCP server registration, or a single tool on a registered MCP server.
      - _oneOf_ — exactly one of:
        - **`connector`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`mcp`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`mcpTool`**
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
    - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `status` — string **(required)** _(enum: `draft`, `active`)_
    - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
    - `latestVersion` — number — Latest published version number, resolved by capabilities that omit a version pin. Absent while the tool is still a draft. _(min=1)_
- `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_

**`NotFoundExceptionResponseContent`**

- `message` — string **(required)** _(default=Not found)_

**`PublishToolVersionRequestContent`**

- `changelog` — string — What changed in this version. _(minLen=1; maxLen=500)_
- `revision` — number **(required)** — Draft revision this publish is based on (optimistic locking).

**`PublishToolVersionResponseContent`**

- `version` — ToolVersion **(required)** — A published tool version: an immutable snapshot of the tool definition at publish time.
  - `toolId` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `version` — number **(required)** — Published tool version number. Monotonic within a tool's version history, starting at 1. _(min=1)_
  - `changelog` — string — What changed in this version, provided at publish time. _(minLen=1; maxLen=500)_
  - `definition` — ToolDefinitionSnapshot **(required)** — Immutable tool definition snapshot captured at publish time. A connector-backed handler carries its pinned ConnectorDefinitionRef, so the snapshot is self-contained; `authorization` is exempt — credentials are always resolved from the current connection at execution time, never pinned.
    - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
    - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
    - `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
    - `input` — ToolInput
      - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
    - `handler` — union **(required)** — Handler of the tool. Every tool executes through one of three mechanisms: a pinned connector definition (built-in providers such as email, webhook, search, chat, sms, calendar — and external integrations — share the same contract), an MCP server registration, or a single tool on a registered MCP server.
      - _oneOf_ — exactly one of:
        - **`connector`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`mcp`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`mcpTool`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
  - `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
    - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
    - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
    - `name` — string — Human readable name of the actor at the time of the action.

**`ResolveConnectorConfigurationRequestContent`**

- `values` — any **(required)** — Current partial form values.
- `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
  - _oneOf_ — exactly one of:
    - **`shared`**
      - `shared` — ConnectorSharedAuthorization **(required)** — Company-managed connection resolved through wilma-secrets.
        - `connection` — ConnectionRef **(required)** — A reference to a connection, held by other services in place of the credential. Resolved to a short-lived token server-to-server via GetConnectionToken.
          - _(nesting depth limit — see `ConnectionRef` in the Schemas appendix)_
    - **`user`**
      - `user` — ConnectorUserAuthorization **(required)** — Marker selecting per-user authorization. Carries no connection reference: at execution the executing user's own credential for this connector's provider is resolved through wilma-secrets (GetUserConnectionToken by provider + user).
- `user` — string — Executing user when user authorization is selected. _(minLen=1; maxLen=256)_

**`ResolveConnectorConfigurationResponseContent`**

- `configuration` — ConnectorConfigurationDefinition **(required)** — Configuration contract rendered by management clients and validated by the service.
  - `schema` — any **(required)** — JSON Schema 2020-12 document describing persisted configuration.
  - `uiSchema` — any — Presentation hints for a compatible JSON Schema form renderer.

**`ResolveMentionResponseContent`**

- `title` — string **(required)** — Display title of the resource.
- `data` — any **(required)** — Resource content, one shape per resource kind, named by `data.kind`. Sections the source has not produced yet are listed in `data.unavailable`.

**`RestoreToolVersionToDraftRequestContent`**

- `revision` — number **(required)** — Draft revision this restore is based on (optimistic locking).

**`RestoreToolVersionToDraftResponseContent`**

- `tool` — Tool **(required)** — A company-owned tool. UpdateTool edits the mutable draft; PublishToolVersion snapshots it into an immutable version that agent and skill capabilities resolve.
  - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
  - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
  - `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
  - `input` — ToolInput
    - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
  - `handler` — union **(required)** — Handler of the tool. Every tool executes through one of three mechanisms: a pinned connector definition (built-in providers such as email, webhook, search, chat, sms, calendar — and external integrations — share the same contract), an MCP server registration, or a single tool on a registered MCP server.
    - _oneOf_ — exactly one of:
      - **`connector`**
        - `connector` — ToolConnectorHandler **(required)** — Handler for a connector-backed Tool created through `CreateTool`. Carries two configuration layers: `configuration` (from the mixin) holds definition-level values for the connector as a whole (validated against the definition `configuration.schema`), while `toolConfiguration` holds values specific to this created Tool (validated against the pinned connector tool's `configuration.schema`). `Tool.input` follows copy-at-create semantics: when `input` is omitted on create, the service snapshots the pinned connector tool's input schema into the Tool; callers may instead provide — and later edit — a custom schema. The Tool owns its copy; definition changes never propagate to existing tools. Reshaping the input of a tool whose handler does not consume input through configuration templates fails at execution, not at write.
          - _(nesting depth limit — see `ToolConnectorHandler` in the Schemas appendix)_
      - **`mcp`**
        - `mcp` — ToolMcpHandler **(required)**
          - _(nesting depth limit — see `ToolMcpHandler` in the Schemas appendix)_
      - **`mcpTool`**
        - `mcpTool` — ToolMcpToolHandler **(required)**
          - _(nesting depth limit — see `ToolMcpToolHandler` in the Schemas appendix)_
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
  - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `status` — string **(required)** _(enum: `draft`, `active`)_
  - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
  - `latestVersion` — number — Latest published version number, resolved by capabilities that omit a version pin. Absent while the tool is still a draft. _(min=1)_

**`RevisionConflictExceptionResponseContent`**

_The resource was modified concurrently; re-read it and retry with the latest revision._

- `message` — string **(required)**
- `type` — string _(default=RevisionConflictException)_
- `currentRevision` — number — The current revision of the resource on the server.

**`SecretRef`**

_A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value._

- `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_

**`ServiceUnavailableExceptionResponseContent`**

_The service is temporarily unable to handle the request; retry later._

- `message` — string **(required)**

**`Tool`**

_A company-owned tool. UpdateTool edits the mutable draft; PublishToolVersion snapshots it into an immutable version that agent and skill capabilities resolve._

- `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
- `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
- `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
- `input` — ToolInput
  - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
- `handler` — union **(required)** — Handler of the tool. Every tool executes through one of three mechanisms: a pinned connector definition (built-in providers such as email, webhook, search, chat, sms, calendar — and external integrations — share the same contract), an MCP server registration, or a single tool on a registered MCP server.
  - _oneOf_ — exactly one of:
    - **`connector`**
      - `connector` — ToolConnectorHandler **(required)** — Handler for a connector-backed Tool created through `CreateTool`. Carries two configuration layers: `configuration` (from the mixin) holds definition-level values for the connector as a whole (validated against the definition `configuration.schema`), while `toolConfiguration` holds values specific to this created Tool (validated against the pinned connector tool's `configuration.schema`). `Tool.input` follows copy-at-create semantics: when `input` is omitted on create, the service snapshots the pinned connector tool's input schema into the Tool; callers may instead provide — and later edit — a custom schema. The Tool owns its copy; definition changes never propagate to existing tools. Reshaping the input of a tool whose handler does not consume input through configuration templates fails at execution, not at write.
        - `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
          - _(nesting depth limit — see `ConnectorDefinitionRef` in the Schemas appendix)_
        - `configuration` — any **(required)** — Values validated against the definition configuration schema.
        - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
          - _(nesting depth limit — see `ConnectorAuthorization` in the Schemas appendix)_
        - `toolId` — string **(required)** — Connector tool from the pinned definition executed by this Tool. _(pattern=^[a-zA-Z0-9._:-]+$; minLen=1; maxLen=256)_
        - `toolConfiguration` — any — Values validated against the pinned connector tool's per-tool configuration schema (`ConnectorTool.configuration.schema`). Omitted when that tool declares no per-tool configuration contract.
    - **`mcp`**
      - `mcp` — ToolMcpHandler **(required)**
        - `serverUrl` — string **(required)** — MCP server endpoint URL
        - `authorization` — union
          - _(nesting depth limit — see `ToolMcpAuthorization` in the Schemas appendix)_
        - `tools` — array **(required)** — Tools enabled for this MCP server.
          - _array of_ `string`
    - **`mcpTool`**
      - `mcpTool` — ToolMcpToolHandler **(required)**
        - `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
        - `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.
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
- `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
- `companyId` — string **(required)** _(minLen=3; maxLen=30)_
- `status` — string **(required)** _(enum: `draft`, `active`)_
- `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
- `latestVersion` — number — Latest published version number, resolved by capabilities that omit a version pin. Absent while the tool is still a draft. _(min=1)_

**`ToolConnectorHandler`**

_Handler for a connector-backed Tool created through `CreateTool`. Carries two configuration layers: `configuration` (from the mixin) holds definition-level values for the connector as a whole (validated against the definition `configuration.schema`), while `toolConfiguration` holds values specific to this created Tool (validated against the pinned connector tool's `configuration.schema`). `Tool.input` follows copy-at-create semantics: when `input` is omitted on create, the service snapshots the pinned connector tool's input schema into the Tool; callers may instead provide — and later edit — a custom schema. The Tool owns its copy; definition changes never propagate to existing tools. Reshaping the input of a tool whose handler does not consume input through configuration templates fails at execution, not at write._

- `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
  - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
  - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
- `configuration` — any **(required)** — Values validated against the definition configuration schema.
- `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
  - _oneOf_ — exactly one of:
    - **`shared`**
      - `shared` — ConnectorSharedAuthorization **(required)** — Company-managed connection resolved through wilma-secrets.
        - `connection` — ConnectionRef **(required)** — A reference to a connection, held by other services in place of the credential. Resolved to a short-lived token server-to-server via GetConnectionToken.
          - _(nesting depth limit — see `ConnectionRef` in the Schemas appendix)_
    - **`user`**
      - `user` — ConnectorUserAuthorization **(required)** — Marker selecting per-user authorization. Carries no connection reference: at execution the executing user's own credential for this connector's provider is resolved through wilma-secrets (GetUserConnectionToken by provider + user).
- `toolId` — string **(required)** — Connector tool from the pinned definition executed by this Tool. _(pattern=^[a-zA-Z0-9._:-]+$; minLen=1; maxLen=256)_
- `toolConfiguration` — any — Values validated against the pinned connector tool's per-tool configuration schema (`ConnectorTool.configuration.schema`). Omitted when that tool declares no per-tool configuration contract.

**`ToolDefinitionSnapshot`**

_Immutable tool definition snapshot captured at publish time. A connector-backed handler carries its pinned ConnectorDefinitionRef, so the snapshot is self-contained; `authorization` is exempt — credentials are always resolved from the current connection at execution time, never pinned._

- `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
- `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
- `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
- `input` — ToolInput
  - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
- `handler` — union **(required)** — Handler of the tool. Every tool executes through one of three mechanisms: a pinned connector definition (built-in providers such as email, webhook, search, chat, sms, calendar — and external integrations — share the same contract), an MCP server registration, or a single tool on a registered MCP server.
  - _oneOf_ — exactly one of:
    - **`connector`**
      - `connector` — ToolConnectorHandler **(required)** — Handler for a connector-backed Tool created through `CreateTool`. Carries two configuration layers: `configuration` (from the mixin) holds definition-level values for the connector as a whole (validated against the definition `configuration.schema`), while `toolConfiguration` holds values specific to this created Tool (validated against the pinned connector tool's `configuration.schema`). `Tool.input` follows copy-at-create semantics: when `input` is omitted on create, the service snapshots the pinned connector tool's input schema into the Tool; callers may instead provide — and later edit — a custom schema. The Tool owns its copy; definition changes never propagate to existing tools. Reshaping the input of a tool whose handler does not consume input through configuration templates fails at execution, not at write.
        - `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
          - _(nesting depth limit — see `ConnectorDefinitionRef` in the Schemas appendix)_
        - `configuration` — any **(required)** — Values validated against the definition configuration schema.
        - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
          - _(nesting depth limit — see `ConnectorAuthorization` in the Schemas appendix)_
        - `toolId` — string **(required)** — Connector tool from the pinned definition executed by this Tool. _(pattern=^[a-zA-Z0-9._:-]+$; minLen=1; maxLen=256)_
        - `toolConfiguration` — any — Values validated against the pinned connector tool's per-tool configuration schema (`ConnectorTool.configuration.schema`). Omitted when that tool declares no per-tool configuration contract.
    - **`mcp`**
      - `mcp` — ToolMcpHandler **(required)**
        - `serverUrl` — string **(required)** — MCP server endpoint URL
        - `authorization` — union
          - _(nesting depth limit — see `ToolMcpAuthorization` in the Schemas appendix)_
        - `tools` — array **(required)** — Tools enabled for this MCP server.
          - _array of_ `string`
    - **`mcpTool`**
      - `mcpTool` — ToolMcpToolHandler **(required)**
        - `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
        - `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.

**`ToolDescription`**

- `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
- `version` — number **(required)** — Published tool version this description was resolved from: the pinned version when the request carried one, otherwise the latestVersion at resolution time. Pass it back on ExecuteTool so the call runs against the same definition the model was shown. _(min=1)_
- `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
- `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
- `schema` — any — JSON Schema (2020-12) of the tool arguments, matching Tool.input.schema. Absent for tools that take no arguments.

**`ToolExecutionExceptionResponseContent`**

- `message` — string **(required)**
- `details` — any — Details about the execution error, typically related to invalid configuration or input
- `traceId` — string — Trace recording the failed execution in wilma-traces — what the tool was called with, the handler that ran and where it stopped. Read it with the wilma-traces GetTrace operation. A failed call returns no ToolExecutionResult, so this is the only handle on the run, and `details` is a summary of what the trace holds in full. _(minLen=1; maxLen=128)_

**`ToolExecutionResult`**

- `traceId` — string — Trace recording this execution in wilma-traces — the handler that ran, the input it was called with and the output it returned. Read it with the wilma-traces GetTrace operation. Minted for this call and returned only here. Unlike a session's trace it cannot be reconstructed from any id the caller already holds, so a test run that does not keep this value can afterwards be found only by searching QueryTraces on `tool.id` and time. _(minLen=1; maxLen=128)_
- `output` — any **(required)** — Output of the tool execution
- `version` — number — Published tool version that executed: the pinned version when the call carried one, otherwise the latestVersion resolved at execution time. Absent when draft is true, because a draft has no version. _(min=1)_
- `draft` — boolean — True when the call executed the tool's mutable draft (draft on ExecuteTool).
- `revision` — number — Draft revision that executed when draft is true; correlates a run with the exact draft state, which `version` cannot because a draft moves under its own name.

**`ToolExecutionServerExceptionResponseContent`**

- `message` — string **(required)**
- `details` — any — Details about the server failure during tool execution
- `traceId` — string — Trace recording the failed execution in wilma-traces. Read it with the wilma-traces GetTrace operation, and quote it when reporting the failure: a server-side fault is diagnosed from the run, and this is what finds the run without correlating on time. Absent when the failure happened before the execution was traced at all. _(minLen=1; maxLen=128)_

**`ToolHandler`**

_Handler of the tool. Every tool executes through one of three mechanisms: a pinned connector definition (built-in providers such as email, webhook, search, chat, sms, calendar — and external integrations — share the same contract), an MCP server registration, or a single tool on a registered MCP server._

- _oneOf_ — exactly one of:
  - **`connector`**
    - `connector` — ToolConnectorHandler **(required)** — Handler for a connector-backed Tool created through `CreateTool`. Carries two configuration layers: `configuration` (from the mixin) holds definition-level values for the connector as a whole (validated against the definition `configuration.schema`), while `toolConfiguration` holds values specific to this created Tool (validated against the pinned connector tool's `configuration.schema`). `Tool.input` follows copy-at-create semantics: when `input` is omitted on create, the service snapshots the pinned connector tool's input schema into the Tool; callers may instead provide — and later edit — a custom schema. The Tool owns its copy; definition changes never propagate to existing tools. Reshaping the input of a tool whose handler does not consume input through configuration templates fails at execution, not at write.
      - `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
        - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
        - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
      - `configuration` — any **(required)** — Values validated against the definition configuration schema.
      - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
        - _oneOf_ — exactly one of:
          - **`shared`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`user`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `toolId` — string **(required)** — Connector tool from the pinned definition executed by this Tool. _(pattern=^[a-zA-Z0-9._:-]+$; minLen=1; maxLen=256)_
      - `toolConfiguration` — any — Values validated against the pinned connector tool's per-tool configuration schema (`ConnectorTool.configuration.schema`). Omitted when that tool declares no per-tool configuration contract.
  - **`mcp`**
    - `mcp` — ToolMcpHandler **(required)**
      - `serverUrl` — string **(required)** — MCP server endpoint URL
      - `authorization` — union
        - _oneOf_ — exactly one of:
          - **`connection`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`customHeaders`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`apiKey`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`user`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `tools` — array **(required)** — Tools enabled for this MCP server.
        - _array of_ `string`
  - **`mcpTool`**
    - `mcpTool` — ToolMcpToolHandler **(required)**
      - `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.

**`ToolInput`**

- `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.

**`ToolMcpApiKeyAuthorization`**

_A SecretRef plus the header it travels under. The referenced secret is expected to carry variant `auth_api_key`; the value is resolved server-to-server at execution and never stored on the tool._

- `secret` — SecretRef **(required)** — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
  - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
- `headerName` — string **(required)** — Header the key is sent under, e.g. `X-API-Key` or `PRIVATE-TOKEN`. _(pattern=^[!#$%&'*+.^_`|~0-9A-Za-z-]+$; minLen=1; maxLen=128)_
- `prefix` — string — Prepended to the value verbatim, for the rare API wanting `Token abc123`.

**`ToolMcpAuthorization`**

- _oneOf_ — exactly one of:
  - **`connection`**
    - `connection` — ConnectionRef **(required)** — A reference to a connection, held by other services in place of the credential. Resolved to a short-lived token server-to-server via GetConnectionToken.
      - `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - **`customHeaders`**
    - `customHeaders` — ToolMcpHeadersMap **(required)**
      - _map of_ `string`
  - **`apiKey`**
    - `apiKey` — ToolMcpApiKeyAuthorization **(required)** — A SecretRef plus the header it travels under. The referenced secret is expected to carry variant `auth_api_key`; the value is resolved server-to-server at execution and never stored on the tool.
      - `secret` — SecretRef **(required)** — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
        - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
      - `headerName` — string **(required)** — Header the key is sent under, e.g. `X-API-Key` or `PRIVATE-TOKEN`. _(pattern=^[!#$%&'*+.^_`|~0-9A-Za-z-]+$; minLen=1; maxLen=128)_
      - `prefix` — string — Prepended to the value verbatim, for the rare API wanting `Token abc123`.
  - **`user`**
    - `user` — ToolMcpUserAuthorization **(required)** — Marker selecting per-user MCP authorization. Carries no reference: the credential is keyed by server and user.

**`ToolMcpHandler`**

- `serverUrl` — string **(required)** — MCP server endpoint URL
- `authorization` — union
  - _oneOf_ — exactly one of:
    - **`connection`**
      - `connection` — ConnectionRef **(required)** — A reference to a connection, held by other services in place of the credential. Resolved to a short-lived token server-to-server via GetConnectionToken.
        - `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
    - **`customHeaders`**
      - `customHeaders` — ToolMcpHeadersMap **(required)**
        - _map of_ `string`
    - **`apiKey`**
      - `apiKey` — ToolMcpApiKeyAuthorization **(required)** — A SecretRef plus the header it travels under. The referenced secret is expected to carry variant `auth_api_key`; the value is resolved server-to-server at execution and never stored on the tool.
        - `secret` — SecretRef **(required)** — A reference to a stored secret, held by other services in place of the value. Resolved server-to-server via GetSecretValue at execution time — always to the current value.
          - _(nesting depth limit — see `SecretRef` in the Schemas appendix)_
        - `headerName` — string **(required)** — Header the key is sent under, e.g. `X-API-Key` or `PRIVATE-TOKEN`. _(pattern=^[!#$%&'*+.^_`|~0-9A-Za-z-]+$; minLen=1; maxLen=128)_
        - `prefix` — string — Prepended to the value verbatim, for the rare API wanting `Token abc123`.
    - **`user`**
      - `user` — ToolMcpUserAuthorization **(required)** — Marker selecting per-user MCP authorization. Carries no reference: the credential is keyed by server and user.
- `tools` — array **(required)** — Tools enabled for this MCP server.
  - _array of_ `string`

**`ToolMcpHeadersMap`**

- _map of_ `string`

**`ToolMcpToolHandler`**

- `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
- `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.

**`ToolMcpUserAuthorization`**

_Marker selecting per-user MCP authorization. Carries no reference: the credential is keyed by server and user._

- ToolMcpUserAuthorization

**`ToolRef`**

_Reference to one tool, optionally pinned to a published version. When `version` is omitted the tool's latestVersion is resolved._

- `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
- `version` — number — Pin a specific published tool version. When omitted, latestVersion is resolved. _(min=1)_

**`ToolStatus`**

- string _(enum: `draft`, `active`)_

**`ToolVersion`**

_A published tool version: an immutable snapshot of the tool definition at publish time._

- `toolId` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
- `version` — number **(required)** — Published tool version number. Monotonic within a tool's version history, starting at 1. _(min=1)_
- `changelog` — string — What changed in this version, provided at publish time. _(minLen=1; maxLen=500)_
- `definition` — ToolDefinitionSnapshot **(required)** — Immutable tool definition snapshot captured at publish time. A connector-backed handler carries its pinned ConnectorDefinitionRef, so the snapshot is self-contained; `authorization` is exempt — credentials are always resolved from the current connection at execution time, never pinned.
  - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
  - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
  - `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
  - `input` — ToolInput
    - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
  - `handler` — union **(required)** — Handler of the tool. Every tool executes through one of three mechanisms: a pinned connector definition (built-in providers such as email, webhook, search, chat, sms, calendar — and external integrations — share the same contract), an MCP server registration, or a single tool on a registered MCP server.
    - _oneOf_ — exactly one of:
      - **`connector`**
        - `connector` — ToolConnectorHandler **(required)** — Handler for a connector-backed Tool created through `CreateTool`. Carries two configuration layers: `configuration` (from the mixin) holds definition-level values for the connector as a whole (validated against the definition `configuration.schema`), while `toolConfiguration` holds values specific to this created Tool (validated against the pinned connector tool's `configuration.schema`). `Tool.input` follows copy-at-create semantics: when `input` is omitted on create, the service snapshots the pinned connector tool's input schema into the Tool; callers may instead provide — and later edit — a custom schema. The Tool owns its copy; definition changes never propagate to existing tools. Reshaping the input of a tool whose handler does not consume input through configuration templates fails at execution, not at write.
          - _(nesting depth limit — see `ToolConnectorHandler` in the Schemas appendix)_
      - **`mcp`**
        - `mcp` — ToolMcpHandler **(required)**
          - _(nesting depth limit — see `ToolMcpHandler` in the Schemas appendix)_
      - **`mcpTool`**
        - `mcpTool` — ToolMcpToolHandler **(required)**
          - _(nesting depth limit — see `ToolMcpToolHandler` in the Schemas appendix)_
- `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
  - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
  - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
  - `name` — string — Human readable name of the actor at the time of the action.

**`ToolVersionChange`**

_One field-level difference between the compared tool definitions._

- `path` — string **(required)** — JSON pointer of the changed field within the tool definition, e.g. '/description' or '/input/schema/properties/subject'.
- `before` — any — Value before the change (absent when the field was added).
- `after` — any — Value after the change (absent when the field was removed).

**`ToolVersionInfo`**

_Version list entry without the full definition snapshot._

- `toolId` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
- `version` — number **(required)** — Published tool version number. Monotonic within a tool's version history, starting at 1. _(min=1)_
- `changelog` — string — Human-readable description of what changed in a published version. _(minLen=1; maxLen=500)_
- `publishedAt` — string **(required)** — ISO-8601 timestamp with millisecond precision, e.g. '2026-07-10T14:12:30.123Z'.
- `publishedBy` — Actor **(required)** — Who performed an action: an interactive user, an API key or an internal service.
  - `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
  - `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
  - `name` — string — Human readable name of the actor at the time of the action.
- `latest` — boolean — True when this version is the tool's latestVersion.

**`UnauthorizedExceptionResponseContent`**

- `message` — string **(required)**

**`UpdateConnectorRequestContent`**

_Fields supplied when a connector is created or replaced._

- `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
  - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
  - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
- `configuration` — any **(required)** — Values validated against the definition configuration schema.
- `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
  - _oneOf_ — exactly one of:
    - **`shared`**
      - `shared` — ConnectorSharedAuthorization **(required)** — Company-managed connection resolved through wilma-secrets.
        - `connection` — ConnectionRef **(required)** — A reference to a connection, held by other services in place of the credential. Resolved to a short-lived token server-to-server via GetConnectionToken.
          - _(nesting depth limit — see `ConnectionRef` in the Schemas appendix)_
    - **`user`**
      - `user` — ConnectorUserAuthorization **(required)** — Marker selecting per-user authorization. Carries no connection reference: at execution the executing user's own credential for this connector's provider is resolved through wilma-secrets (GetUserConnectionToken by provider + user).
- `name` — string **(required)** — Name exposed to administrators and AI agents. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
- `description` — string **(required)** — Description exposed to administrators and AI agents. _(minLen=1; maxLen=4096)_
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
- `revision` — number **(required)** — Connector revision this update is based on (optimistic locking). When it does not match the current revision, RevisionConflictException is returned.

**`UpdateConnectorResponseContent`**

- `connector` — Connector **(required)** — Company-owned configured connector. Edited in place: there is no draft/publish lifecycle and no version history, because the contract the model works against is already immutable — it comes from the pinned `definition` (see `ConnectorDefinitionRef`), not from this record. Config edits take effect immediately, and `grant` and `authorization` are always read live, so narrowing a permission or revoking a credential applies at once to every agent using the connector. Change history is available from wilma-audit.
  - `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
    - `key` — string **(required)** — Stable definition identifier. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
    - `version` — string **(required)** — Exact definition version. _(minLen=1; maxLen=64)_
  - `configuration` — any **(required)** — Values validated against the definition configuration schema.
  - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
    - _oneOf_ — exactly one of:
      - **`shared`**
        - `shared` — ConnectorSharedAuthorization **(required)** — Company-managed connection resolved through wilma-secrets.
          - _(nesting depth limit — see `ConnectorSharedAuthorization` in the Schemas appendix)_
      - **`user`**
        - `user` — ConnectorUserAuthorization **(required)** — Marker selecting per-user authorization. Carries no connection reference: at execution the executing user's own credential for this connector's provider is resolved through wilma-secrets (GetUserConnectionToken by provider + user).
  - `name` — string **(required)** — Name exposed to administrators and AI agents. _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
  - `description` — string **(required)** — Description exposed to administrators and AI agents. _(minLen=1; maxLen=4096)_
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
  - `id` — string **(required)** — Unique connector instance identifier. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `companyId` — string **(required)** — Company that owns this connector. _(minLen=3; maxLen=30)_
  - `revision` — number **(required)** — Monotonic revision, incremented on every update. Pass it back on update for optimistic locking.

**`UpdateToolRequestContent`**

_The complete, versionable configuration of a tool. This is what gets snapshotted when a version is published._

- `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
- `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
- `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
- `input` — ToolInput
  - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
- `handler` — union **(required)** — Handler of the tool. Every tool executes through one of three mechanisms: a pinned connector definition (built-in providers such as email, webhook, search, chat, sms, calendar — and external integrations — share the same contract), an MCP server registration, or a single tool on a registered MCP server.
  - _oneOf_ — exactly one of:
    - **`connector`**
      - `connector` — ToolConnectorHandler **(required)** — Handler for a connector-backed Tool created through `CreateTool`. Carries two configuration layers: `configuration` (from the mixin) holds definition-level values for the connector as a whole (validated against the definition `configuration.schema`), while `toolConfiguration` holds values specific to this created Tool (validated against the pinned connector tool's `configuration.schema`). `Tool.input` follows copy-at-create semantics: when `input` is omitted on create, the service snapshots the pinned connector tool's input schema into the Tool; callers may instead provide — and later edit — a custom schema. The Tool owns its copy; definition changes never propagate to existing tools. Reshaping the input of a tool whose handler does not consume input through configuration templates fails at execution, not at write.
        - `definition` — ConnectorDefinitionRef **(required)** — Reference to one immutable connector definition.
          - _(nesting depth limit — see `ConnectorDefinitionRef` in the Schemas appendix)_
        - `configuration` — any **(required)** — Values validated against the definition configuration schema.
        - `authorization` — union — Credential selection for a configured connector. Credentials remain in wilma-secrets.
          - _(nesting depth limit — see `ConnectorAuthorization` in the Schemas appendix)_
        - `toolId` — string **(required)** — Connector tool from the pinned definition executed by this Tool. _(pattern=^[a-zA-Z0-9._:-]+$; minLen=1; maxLen=256)_
        - `toolConfiguration` — any — Values validated against the pinned connector tool's per-tool configuration schema (`ConnectorTool.configuration.schema`). Omitted when that tool declares no per-tool configuration contract.
    - **`mcp`**
      - `mcp` — ToolMcpHandler **(required)**
        - `serverUrl` — string **(required)** — MCP server endpoint URL
        - `authorization` — union
          - _(nesting depth limit — see `ToolMcpAuthorization` in the Schemas appendix)_
        - `tools` — array **(required)** — Tools enabled for this MCP server.
          - _array of_ `string`
    - **`mcpTool`**
      - `mcpTool` — ToolMcpToolHandler **(required)**
        - `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
        - `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.
- `revision` — number **(required)** — Draft revision this update is based on (optimistic locking). When it does not match the current revision, RevisionConflictException is returned.

**`UpdateToolResponseContent`**

- `tool` — Tool **(required)** — A company-owned tool. UpdateTool edits the mutable draft; PublishToolVersion snapshots it into an immutable version that agent and skill capabilities resolve.
  - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
  - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
  - `description` — string — Description of the tool for people and AI. Optional; can be overridden per agent via AgentTool.description. _(minLen=1; maxLen=4096)_
  - `input` — ToolInput
    - `schema` — any **(required)** — JSON Schema (2020-12) describing the tool arguments. The model is offered this schema (minus any agent-predefined fields); ExecuteTool input is validated against it.
  - `handler` — union **(required)** — Handler of the tool. Every tool executes through one of three mechanisms: a pinned connector definition (built-in providers such as email, webhook, search, chat, sms, calendar — and external integrations — share the same contract), an MCP server registration, or a single tool on a registered MCP server.
    - _oneOf_ — exactly one of:
      - **`connector`**
        - `connector` — ToolConnectorHandler **(required)** — Handler for a connector-backed Tool created through `CreateTool`. Carries two configuration layers: `configuration` (from the mixin) holds definition-level values for the connector as a whole (validated against the definition `configuration.schema`), while `toolConfiguration` holds values specific to this created Tool (validated against the pinned connector tool's `configuration.schema`). `Tool.input` follows copy-at-create semantics: when `input` is omitted on create, the service snapshots the pinned connector tool's input schema into the Tool; callers may instead provide — and later edit — a custom schema. The Tool owns its copy; definition changes never propagate to existing tools. Reshaping the input of a tool whose handler does not consume input through configuration templates fails at execution, not at write.
          - _(nesting depth limit — see `ToolConnectorHandler` in the Schemas appendix)_
      - **`mcp`**
        - `mcp` — ToolMcpHandler **(required)**
          - _(nesting depth limit — see `ToolMcpHandler` in the Schemas appendix)_
      - **`mcpTool`**
        - `mcpTool` — ToolMcpToolHandler **(required)**
          - _(nesting depth limit — see `ToolMcpToolHandler` in the Schemas appendix)_
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
  - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `status` — string **(required)** _(enum: `draft`, `active`)_
  - `revision` — number **(required)** — Monotonic revision of the draft, incremented on every update. Pass it back on update for optimistic locking.
  - `latestVersion` — number — Latest published version number, resolved by capabilities that omit a version pin. Absent while the tool is still a draft. _(min=1)_

</details>
