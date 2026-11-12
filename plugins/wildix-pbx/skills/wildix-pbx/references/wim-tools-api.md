## Wim Tools API

_OpenAPI: WIM Tools Service — version v1_

**Servers**

- `https://tools.wim.wildix.com` — Production
- `https://tools.wim-stable.wildix.com` — Stable
- `https://tools.wim-stage.wildix.com` — Stage

### Other

#### `GET` `/v1/tools`

List all tools for the current company.

- operationId: `ListTools`
- **Scopes**: `tools:ListTools`, `tools:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`ListToolsResponseContent`)
  - `tools` — array **(required)** — List of tools.
    - _array of_ `Tool`
      - `id` — string **(required)** — Unique identifier of the tool _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `companyId` — string **(required)** — Company ID that owns this tool _(minLen=3; maxLen=30)_
      - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
      - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
      - `description` — string **(required)** — Description of the tool, used by AI to understand the purpose of the tool _(minLen=1; maxLen=4096)_
      - `input` — ToolInput **(required)**
        - `variables` — array **(required)** — List of tool variables, used to pass data to the tool
          - _array of_ `ToolVariable`
            - `name` — string **(required)** — Name of the tool variable, e.g.: 'myvar' _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
            - `type` — string **(required)** _(enum: `string`, `number`, `boolean`, `string_array`, `number_array`, `schema`)_
            - `optional` — boolean **(required)** — Whether the variable is optional
            - `description` — string — Original description from MCP tool schema (preserved)
            - `schema` — any — JSON Schema in case if type is schema
      - `handler` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`email`**
            - `email` — union **(required)**
              - _oneOf_ — exactly one of:
                - **`wns`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`custom`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`webhook`**
            - `webhook` — ToolWebhookConfig **(required)**
              - `method` — string **(required)** _(enum: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`)_
              - `url` — string **(required)** — URL endpoint for the webhook, supports variables in path and query parameters using {{variable_name}}, e.g.: 'https://api.example.com/users/{{userId}}?filter={{filter}}&page={{page}}'
              - `headers` — array — HTTP headers for the webhook request. For custom authentication headers (e.g., X-API-Key), add them here instead of using auth.customHeader
                - _(nesting depth limit — see `ToolWebhookHeader` in the Schemas appendix)_
              - `body` — string — Request body for POST, PUT, or PATCH requests
              - `auth` — union
                - _(nesting depth limit — see `ToolWebhookAuth` in the Schemas appendix)_
              - `timeout` — number — Time before webhook execution is stopped _(min=5000; max=120000)_
          - **`search`**
            - `search` — ToolSearchConfig **(required)** — Search handler configuration. API key comes from AppConfig; query comes from tool input. Optionally refine results using Tavily include_domains and/or exclude_domains (see Tavily domain filtering).
              - `includeDomains` — array — When non-empty, only return results from these domains or hosts. Customers may enter plain hostnames (example.com) or full URLs (https://example.com/path) — URLs are normalized to hostnames before calling the search API. _(maxItems=300)_
                - _array of_ `string`
              - `excludeDomains` — array — When non-empty, omit results from these domains or hosts. Same hostname rules as includeDomains. Can be combined with includeDomains per Tavily API. _(maxItems=150)_
                - _array of_ `string`
          - **`chat`**
            - `chat` — ToolChatHandler **(required)**
              - `config` — ToolChatConfig **(required)**
                - _(nesting depth limit — see `ToolChatConfig` in the Schemas appendix)_
          - **`sms`**
            - `sms` — ToolSmsHandler **(required)**
              - `config` — ToolSmsConfig **(required)**
                - _(nesting depth limit — see `ToolSmsConfig` in the Schemas appendix)_
          - **`calendar`**
            - `calendar` — ToolCalendarConfig **(required)**
              - `operation` — string **(required)** _(enum: `get_slots`, `schedule`, `reschedule`, `cancel`, `list_resource_events`)_
          - **`mcp`**
            - `mcp` — ToolMcpHandler **(required)**
              - `serverUrl` — string **(required)** — MCP server endpoint URL
              - `authorization` — union
                - _(nesting depth limit — see `ToolMcpAuthorization` in the Schemas appendix)_
              - `tools` — array **(required)** — List of tools enabled for this MCP server.
                - _array of_ `string`
          - **`mcpTool`**
            - `mcpTool` — ToolMcpToolHandler **(required)**
              - `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
              - `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.
- Errors: `400`, `401`, `403`, `404`, `500`

#### `POST` `/v1/tools`

Create a new tool.

- operationId: `CreateTool`
- **Scopes**: `tools:CreateTool`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `CreateToolRequestContent`) **(required)**
  - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
  - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
  - `description` — string **(required)** — Description of the tool, used by AI to understand the purpose of the tool. _(minLen=1; maxLen=4096)_
  - `input` — ToolInput **(required)**
    - `variables` — array **(required)** — List of tool variables, used to pass data to the tool
      - _array of_ `ToolVariable`
        - `name` — string **(required)** — Name of the tool variable, e.g.: 'myvar' _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
        - `type` — string **(required)** _(enum: `string`, `number`, `boolean`, `string_array`, `number_array`, `schema`)_
        - `optional` — boolean **(required)** — Whether the variable is optional
        - `description` — string — Original description from MCP tool schema (preserved)
        - `schema` — any — JSON Schema in case if type is schema
  - `handler` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`email`**
        - `email` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`wns`**
              - `wns` — ToolWnsEmailConfig **(required)**
                - `to` — string **(required)** — To email address, e.g.: 'jane.doe@example.com'.
                - `subject` — string **(required)** — Subject of the email.
                - `text` — string **(required)** — Text of the email.
            - **`custom`**
              - `custom` — ToolCustomEmailConfig **(required)**
                - `smtp` — ToolSmtpConfig **(required)**
                  - _(nesting depth limit — see `ToolSmtpConfig` in the Schemas appendix)_
                - `from` — string **(required)** — From email address associated with the SMTP server, e.g.: 'john.doe@gmail.com'
                - `to` — string **(required)** — To email address, e.g.: 'jane.doe@example.com'
                - `subject` — string **(required)** — Subject of the email.
                - `text` — string **(required)** — Text of the email.
                - `html` — string — HTML content of the email
                - `cc` — string — CC email addresses
                - `bcc` — string — BCC email addresses
                - `replyTo` — string — Reply-to email address
      - **`webhook`**
        - `webhook` — ToolWebhookConfig **(required)**
          - `method` — string **(required)** _(enum: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`)_
          - `url` — string **(required)** — URL endpoint for the webhook, supports variables in path and query parameters using {{variable_name}}, e.g.: 'https://api.example.com/users/{{userId}}?filter={{filter}}&page={{page}}'
          - `headers` — array — HTTP headers for the webhook request. For custom authentication headers (e.g., X-API-Key), add them here instead of using auth.customHeader
            - _array of_ `ToolWebhookHeader`
              - `name` — string **(required)** — Header name, e.g.: 'X-Custom-Header'
              - `value` — string **(required)** — Header value, supports static, variable, or template syntax
          - `body` — string — Request body for POST, PUT, or PATCH requests
          - `auth` — union
            - _oneOf_ — exactly one of:
              - **`basic`**
                - `basic` — ToolWebhookAuthBasic **(required)**
                  - _(nesting depth limit — see `ToolWebhookAuthBasic` in the Schemas appendix)_
              - **`bearer`**
                - `bearer` — ToolWebhookAuthBearer **(required)**
                  - _(nesting depth limit — see `ToolWebhookAuthBearer` in the Schemas appendix)_
              - **`oauth`**
                - `oauth` — ToolWebhookAuthOAuth **(required)**
                  - _(nesting depth limit — see `ToolWebhookAuthOAuth` in the Schemas appendix)_
          - `timeout` — number — Time before webhook execution is stopped _(min=5000; max=120000)_
      - **`search`**
        - `search` — ToolSearchConfig **(required)** — Search handler configuration. API key comes from AppConfig; query comes from tool input. Optionally refine results using Tavily include_domains and/or exclude_domains (see Tavily domain filtering).
          - `includeDomains` — array — When non-empty, only return results from these domains or hosts. Customers may enter plain hostnames (example.com) or full URLs (https://example.com/path) — URLs are normalized to hostnames before calling the search API. _(maxItems=300)_
            - _array of_ `string`
          - `excludeDomains` — array — When non-empty, omit results from these domains or hosts. Same hostname rules as includeDomains. Can be combined with includeDomains per Tavily API. _(maxItems=150)_
            - _array of_ `string`
      - **`chat`**
        - `chat` — ToolChatHandler **(required)**
          - `config` — ToolChatConfig **(required)**
            - `recipient` — union **(required)**
              - _oneOf_ — exactly one of:
                - **`channelId`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`userId`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `text` — string **(required)** — Message text to send.
            - `botName` — string **(required)** — Name of the system bot that will send the message.
      - **`sms`**
        - `sms` — ToolSmsHandler **(required)**
          - `config` — ToolSmsConfig **(required)**
            - `from` — string **(required)** — Sender phone number in E.164 format (e.g., +1234567890). This is the phone number that will appear as the sender of the SMS. Supports template syntax with variables.
            - `to` — string **(required)** — Recipient phone number in E.164 format (e.g., +1234567890). Supports template syntax with variables.
            - `message` — string **(required)** — SMS message text to send. Supports template syntax with variables. Maximum length depends on carrier limits (typically 160 characters for single SMS, 1600 for concatenated).
      - **`calendar`**
        - `calendar` — ToolCalendarConfig **(required)**
          - `operation` — string **(required)** _(enum: `get_slots`, `schedule`, `reschedule`, `cancel`, `list_resource_events`)_
      - **`mcp`**
        - `mcp` — ToolMcpHandler **(required)**
          - `serverUrl` — string **(required)** — MCP server endpoint URL
          - `authorization` — union
            - _oneOf_ — exactly one of:
              - **`bearer`**
                - `bearer` — ToolWebhookAuthBearer **(required)**
                  - _(nesting depth limit — see `ToolWebhookAuthBearer` in the Schemas appendix)_
              - **`customHeaders`**
                - `customHeaders` — ToolMcpHeadersMap **(required)**
                  - _(nesting depth limit — see `ToolMcpHeadersMap` in the Schemas appendix)_
          - `tools` — array **(required)** — List of tools enabled for this MCP server.
            - _array of_ `string`
      - **`mcpTool`**
        - `mcpTool` — ToolMcpToolHandler **(required)**
          - `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
          - `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.
- **Response 201** (`CreateToolResponseContent`)
  - `tool` — Tool **(required)**
    - `id` — string **(required)** — Unique identifier of the tool _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `companyId` — string **(required)** — Company ID that owns this tool _(minLen=3; maxLen=30)_
    - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
    - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
    - `description` — string **(required)** — Description of the tool, used by AI to understand the purpose of the tool _(minLen=1; maxLen=4096)_
    - `input` — ToolInput **(required)**
      - `variables` — array **(required)** — List of tool variables, used to pass data to the tool
        - _array of_ `ToolVariable`
          - `name` — string **(required)** — Name of the tool variable, e.g.: 'myvar' _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
          - `type` — string **(required)** _(enum: `string`, `number`, `boolean`, `string_array`, `number_array`, `schema`)_
          - `optional` — boolean **(required)** — Whether the variable is optional
          - `description` — string — Original description from MCP tool schema (preserved)
          - `schema` — any — JSON Schema in case if type is schema
    - `handler` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`email`**
          - `email` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`wns`**
                - `wns` — ToolWnsEmailConfig **(required)**
                  - _(nesting depth limit — see `ToolWnsEmailConfig` in the Schemas appendix)_
              - **`custom`**
                - `custom` — ToolCustomEmailConfig **(required)**
                  - _(nesting depth limit — see `ToolCustomEmailConfig` in the Schemas appendix)_
        - **`webhook`**
          - `webhook` — ToolWebhookConfig **(required)**
            - `method` — string **(required)** _(enum: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`)_
            - `url` — string **(required)** — URL endpoint for the webhook, supports variables in path and query parameters using {{variable_name}}, e.g.: 'https://api.example.com/users/{{userId}}?filter={{filter}}&page={{page}}'
            - `headers` — array — HTTP headers for the webhook request. For custom authentication headers (e.g., X-API-Key), add them here instead of using auth.customHeader
              - _array of_ `ToolWebhookHeader`
                - _(nesting depth limit — see `ToolWebhookHeader` in the Schemas appendix)_
            - `body` — string — Request body for POST, PUT, or PATCH requests
            - `auth` — union
              - _oneOf_ — exactly one of:
                - **`basic`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`bearer`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`oauth`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `timeout` — number — Time before webhook execution is stopped _(min=5000; max=120000)_
        - **`search`**
          - `search` — ToolSearchConfig **(required)** — Search handler configuration. API key comes from AppConfig; query comes from tool input. Optionally refine results using Tavily include_domains and/or exclude_domains (see Tavily domain filtering).
            - `includeDomains` — array — When non-empty, only return results from these domains or hosts. Customers may enter plain hostnames (example.com) or full URLs (https://example.com/path) — URLs are normalized to hostnames before calling the search API. _(maxItems=300)_
              - _array of_ `string`
            - `excludeDomains` — array — When non-empty, omit results from these domains or hosts. Same hostname rules as includeDomains. Can be combined with includeDomains per Tavily API. _(maxItems=150)_
              - _array of_ `string`
        - **`chat`**
          - `chat` — ToolChatHandler **(required)**
            - `config` — ToolChatConfig **(required)**
              - `recipient` — union **(required)**
                - _(nesting depth limit — see `ToolChatRecipient` in the Schemas appendix)_
              - `text` — string **(required)** — Message text to send.
              - `botName` — string **(required)** — Name of the system bot that will send the message.
        - **`sms`**
          - `sms` — ToolSmsHandler **(required)**
            - `config` — ToolSmsConfig **(required)**
              - `from` — string **(required)** — Sender phone number in E.164 format (e.g., +1234567890). This is the phone number that will appear as the sender of the SMS. Supports template syntax with variables.
              - `to` — string **(required)** — Recipient phone number in E.164 format (e.g., +1234567890). Supports template syntax with variables.
              - `message` — string **(required)** — SMS message text to send. Supports template syntax with variables. Maximum length depends on carrier limits (typically 160 characters for single SMS, 1600 for concatenated).
        - **`calendar`**
          - `calendar` — ToolCalendarConfig **(required)**
            - `operation` — string **(required)** _(enum: `get_slots`, `schedule`, `reschedule`, `cancel`, `list_resource_events`)_
        - **`mcp`**
          - `mcp` — ToolMcpHandler **(required)**
            - `serverUrl` — string **(required)** — MCP server endpoint URL
            - `authorization` — union
              - _oneOf_ — exactly one of:
                - **`bearer`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`customHeaders`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `tools` — array **(required)** — List of tools enabled for this MCP server.
              - _array of_ `string`
        - **`mcpTool`**
          - `mcpTool` — ToolMcpToolHandler **(required)**
            - `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
            - `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.
- Errors: `400`, `401`, `403`, `404`, `500`

#### `POST` `/v1/tools/describe`

Describe multiple tools by their IDs.

- operationId: `DescribeTools`
- **Scopes**: `tools:DescribeTools`, `tools:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `DescribeToolsRequestContent`) **(required)**
  - `ids` — array **(required)** — List of tool IDs.
    - _array of_ `string`
- **Response 200** (`DescribeToolsResponseContent`)
  - `descriptions` — array **(required)** — List of tool descriptions.
    - _array of_ `ToolDescription`
      - `id` — string **(required)** — Unique identifier of the tool _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
      - `description` — string **(required)** — Description of the tool, used by AI to understand the purpose of the tool _(minLen=1; maxLen=4096)_
      - `variables` — array **(required)** — List of tool variables, used to pass data to the tool
        - _array of_ `ToolVariable`
          - `name` — string **(required)** — Name of the tool variable, e.g.: 'myvar' _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
          - `type` — string **(required)** _(enum: `string`, `number`, `boolean`, `string_array`, `number_array`, `schema`)_
          - `optional` — boolean **(required)** — Whether the variable is optional
          - `description` — string — Original description from MCP tool schema (preserved)
          - `schema` — any — JSON Schema in case if type is schema
- Errors: `400`, `401`, `403`, `404`, `500`

#### `POST` `/v1/tools/discover`

Discover tools from an MCP server.

- operationId: `DiscoverTools`
- **Scopes**: `tools:DiscoverTools`, `tools:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `DiscoverToolsRequestContent`) **(required)**
  - `serverUrl` — string **(required)** — MCP server endpoint URL
  - `authorization` — union
    - _oneOf_ — exactly one of:
      - **`bearer`**
        - `bearer` — ToolWebhookAuthBearer **(required)**
          - `token` — string **(required)** — Bearer token value, supports static, variable, or template syntax
      - **`customHeaders`**
        - `customHeaders` — ToolMcpHeadersMap **(required)**
          - _map of_ `string`
- **Response 200** (`DiscoverToolsResponseContent`)
  - `tools` — array **(required)** — List of discovered tools from the MCP server
    - _array of_ `DiscoveredTool`
      - `name` — string **(required)** — Name of the tool on the MCP server
      - `description` — string **(required)** — Description of the tool
      - `inputSchema` — any **(required)** — JSON Schema for the tool's input parameters
- Errors: `400`, `401`, `403`, `404`, `500`

#### `POST` `/v1/tools/execute`

Execute a tool with the provided input.

- operationId: `ExecuteTool`
- **Scopes**: `tools:ExecuteTool`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `ExecuteToolRequestContent`) **(required)**
  - `id` — string **(required)** — Unique identifier of the tool. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `input` — any **(required)** — Input of the tool, used to pass data to the tool.
  - `service` — string — Optional parameter, by which service the tool is executed, e.g. chatbots. _(minLen=1; maxLen=256)_
  - `user` — string — Optional parameter, for which user the tool is executed, e.g. john.doe@example.com. _(minLen=1; maxLen=256)_
- **Response 200** (`ExecuteToolResponseContent`)
  - `result` — ToolExecutionResult **(required)**
    - `output` — any **(required)** — Output of the tool execution
- Errors: `400`, `401`, `403`, `404`, `500`

#### `GET` `/v1/tools/{toolId}`

Get a tool by its ID.

- operationId: `GetTool`
- **Scopes**: `tools:GetTool`, `tools:read`
- **Parameters**
  - `toolId` (path) — string **(required)** — Unique identifier of the tool. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetToolResponseContent`)
  - `tool` — Tool **(required)**
    - `id` — string **(required)** — Unique identifier of the tool _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `companyId` — string **(required)** — Company ID that owns this tool _(minLen=3; maxLen=30)_
    - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
    - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
    - `description` — string **(required)** — Description of the tool, used by AI to understand the purpose of the tool _(minLen=1; maxLen=4096)_
    - `input` — ToolInput **(required)**
      - `variables` — array **(required)** — List of tool variables, used to pass data to the tool
        - _array of_ `ToolVariable`
          - `name` — string **(required)** — Name of the tool variable, e.g.: 'myvar' _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
          - `type` — string **(required)** _(enum: `string`, `number`, `boolean`, `string_array`, `number_array`, `schema`)_
          - `optional` — boolean **(required)** — Whether the variable is optional
          - `description` — string — Original description from MCP tool schema (preserved)
          - `schema` — any — JSON Schema in case if type is schema
    - `handler` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`email`**
          - `email` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`wns`**
                - `wns` — ToolWnsEmailConfig **(required)**
                  - _(nesting depth limit — see `ToolWnsEmailConfig` in the Schemas appendix)_
              - **`custom`**
                - `custom` — ToolCustomEmailConfig **(required)**
                  - _(nesting depth limit — see `ToolCustomEmailConfig` in the Schemas appendix)_
        - **`webhook`**
          - `webhook` — ToolWebhookConfig **(required)**
            - `method` — string **(required)** _(enum: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`)_
            - `url` — string **(required)** — URL endpoint for the webhook, supports variables in path and query parameters using {{variable_name}}, e.g.: 'https://api.example.com/users/{{userId}}?filter={{filter}}&page={{page}}'
            - `headers` — array — HTTP headers for the webhook request. For custom authentication headers (e.g., X-API-Key), add them here instead of using auth.customHeader
              - _array of_ `ToolWebhookHeader`
                - _(nesting depth limit — see `ToolWebhookHeader` in the Schemas appendix)_
            - `body` — string — Request body for POST, PUT, or PATCH requests
            - `auth` — union
              - _oneOf_ — exactly one of:
                - **`basic`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`bearer`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`oauth`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `timeout` — number — Time before webhook execution is stopped _(min=5000; max=120000)_
        - **`search`**
          - `search` — ToolSearchConfig **(required)** — Search handler configuration. API key comes from AppConfig; query comes from tool input. Optionally refine results using Tavily include_domains and/or exclude_domains (see Tavily domain filtering).
            - `includeDomains` — array — When non-empty, only return results from these domains or hosts. Customers may enter plain hostnames (example.com) or full URLs (https://example.com/path) — URLs are normalized to hostnames before calling the search API. _(maxItems=300)_
              - _array of_ `string`
            - `excludeDomains` — array — When non-empty, omit results from these domains or hosts. Same hostname rules as includeDomains. Can be combined with includeDomains per Tavily API. _(maxItems=150)_
              - _array of_ `string`
        - **`chat`**
          - `chat` — ToolChatHandler **(required)**
            - `config` — ToolChatConfig **(required)**
              - `recipient` — union **(required)**
                - _(nesting depth limit — see `ToolChatRecipient` in the Schemas appendix)_
              - `text` — string **(required)** — Message text to send.
              - `botName` — string **(required)** — Name of the system bot that will send the message.
        - **`sms`**
          - `sms` — ToolSmsHandler **(required)**
            - `config` — ToolSmsConfig **(required)**
              - `from` — string **(required)** — Sender phone number in E.164 format (e.g., +1234567890). This is the phone number that will appear as the sender of the SMS. Supports template syntax with variables.
              - `to` — string **(required)** — Recipient phone number in E.164 format (e.g., +1234567890). Supports template syntax with variables.
              - `message` — string **(required)** — SMS message text to send. Supports template syntax with variables. Maximum length depends on carrier limits (typically 160 characters for single SMS, 1600 for concatenated).
        - **`calendar`**
          - `calendar` — ToolCalendarConfig **(required)**
            - `operation` — string **(required)** _(enum: `get_slots`, `schedule`, `reschedule`, `cancel`, `list_resource_events`)_
        - **`mcp`**
          - `mcp` — ToolMcpHandler **(required)**
            - `serverUrl` — string **(required)** — MCP server endpoint URL
            - `authorization` — union
              - _oneOf_ — exactly one of:
                - **`bearer`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`customHeaders`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `tools` — array **(required)** — List of tools enabled for this MCP server.
              - _array of_ `string`
        - **`mcpTool`**
          - `mcpTool` — ToolMcpToolHandler **(required)**
            - `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
            - `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.
- Errors: `400`, `401`, `403`, `404`, `500`

#### `PUT` `/v1/tools/{toolId}`

Update a tool by its ID.

- operationId: `UpdateTool`
- **Scopes**: `tools:UpdateTool`
- **Parameters**
  - `toolId` (path) — string **(required)** — Unique identifier of the tool. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `UpdateToolRequestContent`) **(required)**
  - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
  - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
  - `description` — string **(required)** — Description of the tool, used by AI to understand the purpose of the tool. _(minLen=1; maxLen=4096)_
  - `input` — ToolInput **(required)**
    - `variables` — array **(required)** — List of tool variables, used to pass data to the tool
      - _array of_ `ToolVariable`
        - `name` — string **(required)** — Name of the tool variable, e.g.: 'myvar' _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
        - `type` — string **(required)** _(enum: `string`, `number`, `boolean`, `string_array`, `number_array`, `schema`)_
        - `optional` — boolean **(required)** — Whether the variable is optional
        - `description` — string — Original description from MCP tool schema (preserved)
        - `schema` — any — JSON Schema in case if type is schema
  - `handler` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`email`**
        - `email` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`wns`**
              - `wns` — ToolWnsEmailConfig **(required)**
                - `to` — string **(required)** — To email address, e.g.: 'jane.doe@example.com'.
                - `subject` — string **(required)** — Subject of the email.
                - `text` — string **(required)** — Text of the email.
            - **`custom`**
              - `custom` — ToolCustomEmailConfig **(required)**
                - `smtp` — ToolSmtpConfig **(required)**
                  - _(nesting depth limit — see `ToolSmtpConfig` in the Schemas appendix)_
                - `from` — string **(required)** — From email address associated with the SMTP server, e.g.: 'john.doe@gmail.com'
                - `to` — string **(required)** — To email address, e.g.: 'jane.doe@example.com'
                - `subject` — string **(required)** — Subject of the email.
                - `text` — string **(required)** — Text of the email.
                - `html` — string — HTML content of the email
                - `cc` — string — CC email addresses
                - `bcc` — string — BCC email addresses
                - `replyTo` — string — Reply-to email address
      - **`webhook`**
        - `webhook` — ToolWebhookConfig **(required)**
          - `method` — string **(required)** _(enum: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`)_
          - `url` — string **(required)** — URL endpoint for the webhook, supports variables in path and query parameters using {{variable_name}}, e.g.: 'https://api.example.com/users/{{userId}}?filter={{filter}}&page={{page}}'
          - `headers` — array — HTTP headers for the webhook request. For custom authentication headers (e.g., X-API-Key), add them here instead of using auth.customHeader
            - _array of_ `ToolWebhookHeader`
              - `name` — string **(required)** — Header name, e.g.: 'X-Custom-Header'
              - `value` — string **(required)** — Header value, supports static, variable, or template syntax
          - `body` — string — Request body for POST, PUT, or PATCH requests
          - `auth` — union
            - _oneOf_ — exactly one of:
              - **`basic`**
                - `basic` — ToolWebhookAuthBasic **(required)**
                  - _(nesting depth limit — see `ToolWebhookAuthBasic` in the Schemas appendix)_
              - **`bearer`**
                - `bearer` — ToolWebhookAuthBearer **(required)**
                  - _(nesting depth limit — see `ToolWebhookAuthBearer` in the Schemas appendix)_
              - **`oauth`**
                - `oauth` — ToolWebhookAuthOAuth **(required)**
                  - _(nesting depth limit — see `ToolWebhookAuthOAuth` in the Schemas appendix)_
          - `timeout` — number — Time before webhook execution is stopped _(min=5000; max=120000)_
      - **`search`**
        - `search` — ToolSearchConfig **(required)** — Search handler configuration. API key comes from AppConfig; query comes from tool input. Optionally refine results using Tavily include_domains and/or exclude_domains (see Tavily domain filtering).
          - `includeDomains` — array — When non-empty, only return results from these domains or hosts. Customers may enter plain hostnames (example.com) or full URLs (https://example.com/path) — URLs are normalized to hostnames before calling the search API. _(maxItems=300)_
            - _array of_ `string`
          - `excludeDomains` — array — When non-empty, omit results from these domains or hosts. Same hostname rules as includeDomains. Can be combined with includeDomains per Tavily API. _(maxItems=150)_
            - _array of_ `string`
      - **`chat`**
        - `chat` — ToolChatHandler **(required)**
          - `config` — ToolChatConfig **(required)**
            - `recipient` — union **(required)**
              - _oneOf_ — exactly one of:
                - **`channelId`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`userId`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `text` — string **(required)** — Message text to send.
            - `botName` — string **(required)** — Name of the system bot that will send the message.
      - **`sms`**
        - `sms` — ToolSmsHandler **(required)**
          - `config` — ToolSmsConfig **(required)**
            - `from` — string **(required)** — Sender phone number in E.164 format (e.g., +1234567890). This is the phone number that will appear as the sender of the SMS. Supports template syntax with variables.
            - `to` — string **(required)** — Recipient phone number in E.164 format (e.g., +1234567890). Supports template syntax with variables.
            - `message` — string **(required)** — SMS message text to send. Supports template syntax with variables. Maximum length depends on carrier limits (typically 160 characters for single SMS, 1600 for concatenated).
      - **`calendar`**
        - `calendar` — ToolCalendarConfig **(required)**
          - `operation` — string **(required)** _(enum: `get_slots`, `schedule`, `reschedule`, `cancel`, `list_resource_events`)_
      - **`mcp`**
        - `mcp` — ToolMcpHandler **(required)**
          - `serverUrl` — string **(required)** — MCP server endpoint URL
          - `authorization` — union
            - _oneOf_ — exactly one of:
              - **`bearer`**
                - `bearer` — ToolWebhookAuthBearer **(required)**
                  - _(nesting depth limit — see `ToolWebhookAuthBearer` in the Schemas appendix)_
              - **`customHeaders`**
                - `customHeaders` — ToolMcpHeadersMap **(required)**
                  - _(nesting depth limit — see `ToolMcpHeadersMap` in the Schemas appendix)_
          - `tools` — array **(required)** — List of tools enabled for this MCP server.
            - _array of_ `string`
      - **`mcpTool`**
        - `mcpTool` — ToolMcpToolHandler **(required)**
          - `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
          - `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.
- **Response 200** (`UpdateToolResponseContent`)
  - `tool` — Tool **(required)**
    - `id` — string **(required)** — Unique identifier of the tool _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `companyId` — string **(required)** — Company ID that owns this tool _(minLen=3; maxLen=30)_
    - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
    - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
    - `description` — string **(required)** — Description of the tool, used by AI to understand the purpose of the tool _(minLen=1; maxLen=4096)_
    - `input` — ToolInput **(required)**
      - `variables` — array **(required)** — List of tool variables, used to pass data to the tool
        - _array of_ `ToolVariable`
          - `name` — string **(required)** — Name of the tool variable, e.g.: 'myvar' _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
          - `type` — string **(required)** _(enum: `string`, `number`, `boolean`, `string_array`, `number_array`, `schema`)_
          - `optional` — boolean **(required)** — Whether the variable is optional
          - `description` — string — Original description from MCP tool schema (preserved)
          - `schema` — any — JSON Schema in case if type is schema
    - `handler` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`email`**
          - `email` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`wns`**
                - `wns` — ToolWnsEmailConfig **(required)**
                  - _(nesting depth limit — see `ToolWnsEmailConfig` in the Schemas appendix)_
              - **`custom`**
                - `custom` — ToolCustomEmailConfig **(required)**
                  - _(nesting depth limit — see `ToolCustomEmailConfig` in the Schemas appendix)_
        - **`webhook`**
          - `webhook` — ToolWebhookConfig **(required)**
            - `method` — string **(required)** _(enum: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`)_
            - `url` — string **(required)** — URL endpoint for the webhook, supports variables in path and query parameters using {{variable_name}}, e.g.: 'https://api.example.com/users/{{userId}}?filter={{filter}}&page={{page}}'
            - `headers` — array — HTTP headers for the webhook request. For custom authentication headers (e.g., X-API-Key), add them here instead of using auth.customHeader
              - _array of_ `ToolWebhookHeader`
                - _(nesting depth limit — see `ToolWebhookHeader` in the Schemas appendix)_
            - `body` — string — Request body for POST, PUT, or PATCH requests
            - `auth` — union
              - _oneOf_ — exactly one of:
                - **`basic`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`bearer`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`oauth`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `timeout` — number — Time before webhook execution is stopped _(min=5000; max=120000)_
        - **`search`**
          - `search` — ToolSearchConfig **(required)** — Search handler configuration. API key comes from AppConfig; query comes from tool input. Optionally refine results using Tavily include_domains and/or exclude_domains (see Tavily domain filtering).
            - `includeDomains` — array — When non-empty, only return results from these domains or hosts. Customers may enter plain hostnames (example.com) or full URLs (https://example.com/path) — URLs are normalized to hostnames before calling the search API. _(maxItems=300)_
              - _array of_ `string`
            - `excludeDomains` — array — When non-empty, omit results from these domains or hosts. Same hostname rules as includeDomains. Can be combined with includeDomains per Tavily API. _(maxItems=150)_
              - _array of_ `string`
        - **`chat`**
          - `chat` — ToolChatHandler **(required)**
            - `config` — ToolChatConfig **(required)**
              - `recipient` — union **(required)**
                - _(nesting depth limit — see `ToolChatRecipient` in the Schemas appendix)_
              - `text` — string **(required)** — Message text to send.
              - `botName` — string **(required)** — Name of the system bot that will send the message.
        - **`sms`**
          - `sms` — ToolSmsHandler **(required)**
            - `config` — ToolSmsConfig **(required)**
              - `from` — string **(required)** — Sender phone number in E.164 format (e.g., +1234567890). This is the phone number that will appear as the sender of the SMS. Supports template syntax with variables.
              - `to` — string **(required)** — Recipient phone number in E.164 format (e.g., +1234567890). Supports template syntax with variables.
              - `message` — string **(required)** — SMS message text to send. Supports template syntax with variables. Maximum length depends on carrier limits (typically 160 characters for single SMS, 1600 for concatenated).
        - **`calendar`**
          - `calendar` — ToolCalendarConfig **(required)**
            - `operation` — string **(required)** _(enum: `get_slots`, `schedule`, `reschedule`, `cancel`, `list_resource_events`)_
        - **`mcp`**
          - `mcp` — ToolMcpHandler **(required)**
            - `serverUrl` — string **(required)** — MCP server endpoint URL
            - `authorization` — union
              - _oneOf_ — exactly one of:
                - **`bearer`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
                - **`customHeaders`**
                  - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `tools` — array **(required)** — List of tools enabled for this MCP server.
              - _array of_ `string`
        - **`mcpTool`**
          - `mcpTool` — ToolMcpToolHandler **(required)**
            - `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
            - `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.
- Errors: `400`, `401`, `403`, `404`, `500`

#### `DELETE` `/v1/tools/{toolId}`

Delete a tool by its ID.

- operationId: `DeleteTool`
- **Scopes**: `tools:DeleteTool`
- **Parameters**
  - `toolId` (path) — string **(required)** — Unique identifier of the tool. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- Errors: `400`, `401`, `403`, `404`, `500`

### Schemas appendix — Wim Tools API

<details><summary>49 component schemas</summary>

**`AlreadyExistExceptionResponseContent`**

- `message` — string **(required)**

**`CreateToolRequestContent`**

- `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
- `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
- `description` — string **(required)** — Description of the tool, used by AI to understand the purpose of the tool. _(minLen=1; maxLen=4096)_
- `input` — ToolInput **(required)**
  - `variables` — array **(required)** — List of tool variables, used to pass data to the tool
    - _array of_ `ToolVariable`
      - `name` — string **(required)** — Name of the tool variable, e.g.: 'myvar' _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
      - `type` — string **(required)** _(enum: `string`, `number`, `boolean`, `string_array`, `number_array`, `schema`)_
      - `optional` — boolean **(required)** — Whether the variable is optional
      - `description` — string — Original description from MCP tool schema (preserved)
      - `schema` — any — JSON Schema in case if type is schema
- `handler` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`email`**
      - `email` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`wns`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`custom`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - **`webhook`**
      - `webhook` — ToolWebhookConfig **(required)**
        - `method` — string **(required)** _(enum: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`)_
        - `url` — string **(required)** — URL endpoint for the webhook, supports variables in path and query parameters using {{variable_name}}, e.g.: 'https://api.example.com/users/{{userId}}?filter={{filter}}&page={{page}}'
        - `headers` — array — HTTP headers for the webhook request. For custom authentication headers (e.g., X-API-Key), add them here instead of using auth.customHeader
          - _(nesting depth limit — see `ToolWebhookHeader` in the Schemas appendix)_
        - `body` — string — Request body for POST, PUT, or PATCH requests
        - `auth` — union
          - _(nesting depth limit — see `ToolWebhookAuth` in the Schemas appendix)_
        - `timeout` — number — Time before webhook execution is stopped _(min=5000; max=120000)_
    - **`search`**
      - `search` — ToolSearchConfig **(required)** — Search handler configuration. API key comes from AppConfig; query comes from tool input. Optionally refine results using Tavily include_domains and/or exclude_domains (see Tavily domain filtering).
        - `includeDomains` — array — When non-empty, only return results from these domains or hosts. Customers may enter plain hostnames (example.com) or full URLs (https://example.com/path) — URLs are normalized to hostnames before calling the search API. _(maxItems=300)_
          - _array of_ `string`
        - `excludeDomains` — array — When non-empty, omit results from these domains or hosts. Same hostname rules as includeDomains. Can be combined with includeDomains per Tavily API. _(maxItems=150)_
          - _array of_ `string`
    - **`chat`**
      - `chat` — ToolChatHandler **(required)**
        - `config` — ToolChatConfig **(required)**
          - _(nesting depth limit — see `ToolChatConfig` in the Schemas appendix)_
    - **`sms`**
      - `sms` — ToolSmsHandler **(required)**
        - `config` — ToolSmsConfig **(required)**
          - _(nesting depth limit — see `ToolSmsConfig` in the Schemas appendix)_
    - **`calendar`**
      - `calendar` — ToolCalendarConfig **(required)**
        - `operation` — string **(required)** _(enum: `get_slots`, `schedule`, `reschedule`, `cancel`, `list_resource_events`)_
    - **`mcp`**
      - `mcp` — ToolMcpHandler **(required)**
        - `serverUrl` — string **(required)** — MCP server endpoint URL
        - `authorization` — union
          - _(nesting depth limit — see `ToolMcpAuthorization` in the Schemas appendix)_
        - `tools` — array **(required)** — List of tools enabled for this MCP server.
          - _array of_ `string`
    - **`mcpTool`**
      - `mcpTool` — ToolMcpToolHandler **(required)**
        - `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
        - `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.

**`CreateToolResponseContent`**

- `tool` — Tool **(required)**
  - `id` — string **(required)** — Unique identifier of the tool _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `companyId` — string **(required)** — Company ID that owns this tool _(minLen=3; maxLen=30)_
  - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
  - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
  - `description` — string **(required)** — Description of the tool, used by AI to understand the purpose of the tool _(minLen=1; maxLen=4096)_
  - `input` — ToolInput **(required)**
    - `variables` — array **(required)** — List of tool variables, used to pass data to the tool
      - _array of_ `ToolVariable`
        - _(nesting depth limit — see `ToolVariable` in the Schemas appendix)_
  - `handler` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`email`**
        - `email` — union **(required)**
          - _(nesting depth limit — see `ToolEmailHandler` in the Schemas appendix)_
      - **`webhook`**
        - `webhook` — ToolWebhookConfig **(required)**
          - _(nesting depth limit — see `ToolWebhookConfig` in the Schemas appendix)_
      - **`search`**
        - `search` — ToolSearchConfig **(required)** — Search handler configuration. API key comes from AppConfig; query comes from tool input. Optionally refine results using Tavily include_domains and/or exclude_domains (see Tavily domain filtering).
          - _(nesting depth limit — see `ToolSearchConfig` in the Schemas appendix)_
      - **`chat`**
        - `chat` — ToolChatHandler **(required)**
          - _(nesting depth limit — see `ToolChatHandler` in the Schemas appendix)_
      - **`sms`**
        - `sms` — ToolSmsHandler **(required)**
          - _(nesting depth limit — see `ToolSmsHandler` in the Schemas appendix)_
      - **`calendar`**
        - `calendar` — ToolCalendarConfig **(required)**
          - _(nesting depth limit — see `ToolCalendarConfig` in the Schemas appendix)_
      - **`mcp`**
        - `mcp` — ToolMcpHandler **(required)**
          - _(nesting depth limit — see `ToolMcpHandler` in the Schemas appendix)_
      - **`mcpTool`**
        - `mcpTool` — ToolMcpToolHandler **(required)**
          - _(nesting depth limit — see `ToolMcpToolHandler` in the Schemas appendix)_

**`DescribeToolsRequestContent`**

- `ids` — array **(required)** — List of tool IDs.
  - _array of_ `string`

**`DescribeToolsResponseContent`**

- `descriptions` — array **(required)** — List of tool descriptions.
  - _array of_ `ToolDescription`
    - `id` — string **(required)** — Unique identifier of the tool _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
    - `description` — string **(required)** — Description of the tool, used by AI to understand the purpose of the tool _(minLen=1; maxLen=4096)_
    - `variables` — array **(required)** — List of tool variables, used to pass data to the tool
      - _array of_ `ToolVariable`
        - _(nesting depth limit — see `ToolVariable` in the Schemas appendix)_

**`DiscoverToolsRequestContent`**

- `serverUrl` — string **(required)** — MCP server endpoint URL
- `authorization` — union
  - _oneOf_ — exactly one of:
    - **`bearer`**
      - `bearer` — ToolWebhookAuthBearer **(required)**
        - `token` — string **(required)** — Bearer token value, supports static, variable, or template syntax
    - **`customHeaders`**
      - `customHeaders` — ToolMcpHeadersMap **(required)**
        - _map of_ `string`

**`DiscoverToolsResponseContent`**

- `tools` — array **(required)** — List of discovered tools from the MCP server
  - _array of_ `DiscoveredTool`
    - `name` — string **(required)** — Name of the tool on the MCP server
    - `description` — string **(required)** — Description of the tool
    - `inputSchema` — any **(required)** — JSON Schema for the tool's input parameters

**`DiscoveredTool`**

- `name` — string **(required)** — Name of the tool on the MCP server
- `description` — string **(required)** — Description of the tool
- `inputSchema` — any **(required)** — JSON Schema for the tool's input parameters

**`ExecuteToolRequestContent`**

- `id` — string **(required)** — Unique identifier of the tool. _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
- `input` — any **(required)** — Input of the tool, used to pass data to the tool.
- `service` — string — Optional parameter, by which service the tool is executed, e.g. chatbots. _(minLen=1; maxLen=256)_
- `user` — string — Optional parameter, for which user the tool is executed, e.g. john.doe@example.com. _(minLen=1; maxLen=256)_

**`ExecuteToolResponseContent`**

- `result` — ToolExecutionResult **(required)**
  - `output` — any **(required)** — Output of the tool execution

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GetToolResponseContent`**

- `tool` — Tool **(required)**
  - `id` — string **(required)** — Unique identifier of the tool _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `companyId` — string **(required)** — Company ID that owns this tool _(minLen=3; maxLen=30)_
  - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
  - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
  - `description` — string **(required)** — Description of the tool, used by AI to understand the purpose of the tool _(minLen=1; maxLen=4096)_
  - `input` — ToolInput **(required)**
    - `variables` — array **(required)** — List of tool variables, used to pass data to the tool
      - _array of_ `ToolVariable`
        - _(nesting depth limit — see `ToolVariable` in the Schemas appendix)_
  - `handler` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`email`**
        - `email` — union **(required)**
          - _(nesting depth limit — see `ToolEmailHandler` in the Schemas appendix)_
      - **`webhook`**
        - `webhook` — ToolWebhookConfig **(required)**
          - _(nesting depth limit — see `ToolWebhookConfig` in the Schemas appendix)_
      - **`search`**
        - `search` — ToolSearchConfig **(required)** — Search handler configuration. API key comes from AppConfig; query comes from tool input. Optionally refine results using Tavily include_domains and/or exclude_domains (see Tavily domain filtering).
          - _(nesting depth limit — see `ToolSearchConfig` in the Schemas appendix)_
      - **`chat`**
        - `chat` — ToolChatHandler **(required)**
          - _(nesting depth limit — see `ToolChatHandler` in the Schemas appendix)_
      - **`sms`**
        - `sms` — ToolSmsHandler **(required)**
          - _(nesting depth limit — see `ToolSmsHandler` in the Schemas appendix)_
      - **`calendar`**
        - `calendar` — ToolCalendarConfig **(required)**
          - _(nesting depth limit — see `ToolCalendarConfig` in the Schemas appendix)_
      - **`mcp`**
        - `mcp` — ToolMcpHandler **(required)**
          - _(nesting depth limit — see `ToolMcpHandler` in the Schemas appendix)_
      - **`mcpTool`**
        - `mcpTool` — ToolMcpToolHandler **(required)**
          - _(nesting depth limit — see `ToolMcpToolHandler` in the Schemas appendix)_

**`ListToolsResponseContent`**

- `tools` — array **(required)** — List of tools.
  - _array of_ `Tool`
    - `id` — string **(required)** — Unique identifier of the tool _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
    - `companyId` — string **(required)** — Company ID that owns this tool _(minLen=3; maxLen=30)_
    - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
    - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
    - `description` — string **(required)** — Description of the tool, used by AI to understand the purpose of the tool _(minLen=1; maxLen=4096)_
    - `input` — ToolInput **(required)**
      - `variables` — array **(required)** — List of tool variables, used to pass data to the tool
        - _(nesting depth limit — see `ToolVariable` in the Schemas appendix)_
    - `handler` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`email`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`webhook`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`search`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`chat`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sms`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`calendar`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`mcp`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`mcpTool`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_

**`NotFoundExceptionResponseContent`**

- `message` — string **(required)** _(default=Not found)_

**`Tool`**

- `id` — string **(required)** — Unique identifier of the tool _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
- `companyId` — string **(required)** — Company ID that owns this tool _(minLen=3; maxLen=30)_
- `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
- `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
- `description` — string **(required)** — Description of the tool, used by AI to understand the purpose of the tool _(minLen=1; maxLen=4096)_
- `input` — ToolInput **(required)**
  - `variables` — array **(required)** — List of tool variables, used to pass data to the tool
    - _array of_ `ToolVariable`
      - `name` — string **(required)** — Name of the tool variable, e.g.: 'myvar' _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
      - `type` — string **(required)** _(enum: `string`, `number`, `boolean`, `string_array`, `number_array`, `schema`)_
      - `optional` — boolean **(required)** — Whether the variable is optional
      - `description` — string — Original description from MCP tool schema (preserved)
      - `schema` — any — JSON Schema in case if type is schema
- `handler` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`email`**
      - `email` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`wns`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`custom`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - **`webhook`**
      - `webhook` — ToolWebhookConfig **(required)**
        - `method` — string **(required)** _(enum: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`)_
        - `url` — string **(required)** — URL endpoint for the webhook, supports variables in path and query parameters using {{variable_name}}, e.g.: 'https://api.example.com/users/{{userId}}?filter={{filter}}&page={{page}}'
        - `headers` — array — HTTP headers for the webhook request. For custom authentication headers (e.g., X-API-Key), add them here instead of using auth.customHeader
          - _(nesting depth limit — see `ToolWebhookHeader` in the Schemas appendix)_
        - `body` — string — Request body for POST, PUT, or PATCH requests
        - `auth` — union
          - _(nesting depth limit — see `ToolWebhookAuth` in the Schemas appendix)_
        - `timeout` — number — Time before webhook execution is stopped _(min=5000; max=120000)_
    - **`search`**
      - `search` — ToolSearchConfig **(required)** — Search handler configuration. API key comes from AppConfig; query comes from tool input. Optionally refine results using Tavily include_domains and/or exclude_domains (see Tavily domain filtering).
        - `includeDomains` — array — When non-empty, only return results from these domains or hosts. Customers may enter plain hostnames (example.com) or full URLs (https://example.com/path) — URLs are normalized to hostnames before calling the search API. _(maxItems=300)_
          - _array of_ `string`
        - `excludeDomains` — array — When non-empty, omit results from these domains or hosts. Same hostname rules as includeDomains. Can be combined with includeDomains per Tavily API. _(maxItems=150)_
          - _array of_ `string`
    - **`chat`**
      - `chat` — ToolChatHandler **(required)**
        - `config` — ToolChatConfig **(required)**
          - _(nesting depth limit — see `ToolChatConfig` in the Schemas appendix)_
    - **`sms`**
      - `sms` — ToolSmsHandler **(required)**
        - `config` — ToolSmsConfig **(required)**
          - _(nesting depth limit — see `ToolSmsConfig` in the Schemas appendix)_
    - **`calendar`**
      - `calendar` — ToolCalendarConfig **(required)**
        - `operation` — string **(required)** _(enum: `get_slots`, `schedule`, `reschedule`, `cancel`, `list_resource_events`)_
    - **`mcp`**
      - `mcp` — ToolMcpHandler **(required)**
        - `serverUrl` — string **(required)** — MCP server endpoint URL
        - `authorization` — union
          - _(nesting depth limit — see `ToolMcpAuthorization` in the Schemas appendix)_
        - `tools` — array **(required)** — List of tools enabled for this MCP server.
          - _array of_ `string`
    - **`mcpTool`**
      - `mcpTool` — ToolMcpToolHandler **(required)**
        - `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
        - `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.

**`ToolCalendarConfig`**

- `operation` — string **(required)** _(enum: `get_slots`, `schedule`, `reschedule`, `cancel`, `list_resource_events`)_

**`ToolCalendarOperation`**

- string _(enum: `get_slots`, `schedule`, `reschedule`, `cancel`, `list_resource_events`)_

**`ToolChatConfig`**

- `recipient` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`channelId`**
      - `channelId` — string **(required)** — Channel ID for group channels.
    - **`userId`**
      - `userId` — string **(required)** — User email address for direct messages.
- `text` — string **(required)** — Message text to send.
- `botName` — string **(required)** — Name of the system bot that will send the message.

**`ToolChatHandler`**

- `config` — ToolChatConfig **(required)**
  - `recipient` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`channelId`**
        - `channelId` — string **(required)** — Channel ID for group channels.
      - **`userId`**
        - `userId` — string **(required)** — User email address for direct messages.
  - `text` — string **(required)** — Message text to send.
  - `botName` — string **(required)** — Name of the system bot that will send the message.

**`ToolChatRecipient`**

- _oneOf_ — exactly one of:
  - **`channelId`**
    - `channelId` — string **(required)** — Channel ID for group channels.
  - **`userId`**
    - `userId` — string **(required)** — User email address for direct messages.

**`ToolCustomEmailConfig`**

- `smtp` — ToolSmtpConfig **(required)**
  - `host` — string **(required)** — SMTP server host, e.g.: 'smtp.gmail.com'
  - `port` — number **(required)** — SMTP server port, e.g.: 587 _(min=1; max=65535)_
  - `username` — string **(required)** — SMTP server username for authentication, e.g.: 'john.doe@gmail.com'
  - `password` — string **(required)** — SMTP server password
  - `secure` — boolean **(required)** — SMTP server secure connection
- `from` — string **(required)** — From email address associated with the SMTP server, e.g.: 'john.doe@gmail.com'
- `to` — string **(required)** — To email address, e.g.: 'jane.doe@example.com'
- `subject` — string **(required)** — Subject of the email.
- `text` — string **(required)** — Text of the email.
- `html` — string — HTML content of the email
- `cc` — string — CC email addresses
- `bcc` — string — BCC email addresses
- `replyTo` — string — Reply-to email address

**`ToolDescription`**

- `id` — string **(required)** — Unique identifier of the tool _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
- `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
- `description` — string **(required)** — Description of the tool, used by AI to understand the purpose of the tool _(minLen=1; maxLen=4096)_
- `variables` — array **(required)** — List of tool variables, used to pass data to the tool
  - _array of_ `ToolVariable`
    - `name` — string **(required)** — Name of the tool variable, e.g.: 'myvar' _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
    - `type` — string **(required)** _(enum: `string`, `number`, `boolean`, `string_array`, `number_array`, `schema`)_
    - `optional` — boolean **(required)** — Whether the variable is optional
    - `description` — string — Original description from MCP tool schema (preserved)
    - `schema` — any — JSON Schema in case if type is schema

**`ToolEmailHandler`**

- _oneOf_ — exactly one of:
  - **`wns`**
    - `wns` — ToolWnsEmailConfig **(required)**
      - `to` — string **(required)** — To email address, e.g.: 'jane.doe@example.com'.
      - `subject` — string **(required)** — Subject of the email.
      - `text` — string **(required)** — Text of the email.
  - **`custom`**
    - `custom` — ToolCustomEmailConfig **(required)**
      - `smtp` — ToolSmtpConfig **(required)**
        - `host` — string **(required)** — SMTP server host, e.g.: 'smtp.gmail.com'
        - `port` — number **(required)** — SMTP server port, e.g.: 587 _(min=1; max=65535)_
        - `username` — string **(required)** — SMTP server username for authentication, e.g.: 'john.doe@gmail.com'
        - `password` — string **(required)** — SMTP server password
        - `secure` — boolean **(required)** — SMTP server secure connection
      - `from` — string **(required)** — From email address associated with the SMTP server, e.g.: 'john.doe@gmail.com'
      - `to` — string **(required)** — To email address, e.g.: 'jane.doe@example.com'
      - `subject` — string **(required)** — Subject of the email.
      - `text` — string **(required)** — Text of the email.
      - `html` — string — HTML content of the email
      - `cc` — string — CC email addresses
      - `bcc` — string — BCC email addresses
      - `replyTo` — string — Reply-to email address

**`ToolExecutionExceptionResponseContent`**

- `message` — string **(required)**
- `details` — any — Details about the execution error, typically related to invalid configuration or input

**`ToolExecutionResult`**

- `output` — any **(required)** — Output of the tool execution

**`ToolExecutionServerExceptionResponseContent`**

- `message` — string **(required)**
- `details` — any — Details about the server failure during tool execution

**`ToolHandler`**

- _oneOf_ — exactly one of:
  - **`email`**
    - `email` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`wns`**
          - `wns` — ToolWnsEmailConfig **(required)**
            - _(nesting depth limit — see `ToolWnsEmailConfig` in the Schemas appendix)_
        - **`custom`**
          - `custom` — ToolCustomEmailConfig **(required)**
            - _(nesting depth limit — see `ToolCustomEmailConfig` in the Schemas appendix)_
  - **`webhook`**
    - `webhook` — ToolWebhookConfig **(required)**
      - `method` — string **(required)** _(enum: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`)_
      - `url` — string **(required)** — URL endpoint for the webhook, supports variables in path and query parameters using {{variable_name}}, e.g.: 'https://api.example.com/users/{{userId}}?filter={{filter}}&page={{page}}'
      - `headers` — array — HTTP headers for the webhook request. For custom authentication headers (e.g., X-API-Key), add them here instead of using auth.customHeader
        - _array of_ `ToolWebhookHeader`
          - _(nesting depth limit — see `ToolWebhookHeader` in the Schemas appendix)_
      - `body` — string — Request body for POST, PUT, or PATCH requests
      - `auth` — union
        - _oneOf_ — exactly one of:
          - **`basic`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`bearer`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`oauth`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `timeout` — number — Time before webhook execution is stopped _(min=5000; max=120000)_
  - **`search`**
    - `search` — ToolSearchConfig **(required)** — Search handler configuration. API key comes from AppConfig; query comes from tool input. Optionally refine results using Tavily include_domains and/or exclude_domains (see Tavily domain filtering).
      - `includeDomains` — array — When non-empty, only return results from these domains or hosts. Customers may enter plain hostnames (example.com) or full URLs (https://example.com/path) — URLs are normalized to hostnames before calling the search API. _(maxItems=300)_
        - _array of_ `string`
      - `excludeDomains` — array — When non-empty, omit results from these domains or hosts. Same hostname rules as includeDomains. Can be combined with includeDomains per Tavily API. _(maxItems=150)_
        - _array of_ `string`
  - **`chat`**
    - `chat` — ToolChatHandler **(required)**
      - `config` — ToolChatConfig **(required)**
        - `recipient` — union **(required)**
          - _(nesting depth limit — see `ToolChatRecipient` in the Schemas appendix)_
        - `text` — string **(required)** — Message text to send.
        - `botName` — string **(required)** — Name of the system bot that will send the message.
  - **`sms`**
    - `sms` — ToolSmsHandler **(required)**
      - `config` — ToolSmsConfig **(required)**
        - `from` — string **(required)** — Sender phone number in E.164 format (e.g., +1234567890). This is the phone number that will appear as the sender of the SMS. Supports template syntax with variables.
        - `to` — string **(required)** — Recipient phone number in E.164 format (e.g., +1234567890). Supports template syntax with variables.
        - `message` — string **(required)** — SMS message text to send. Supports template syntax with variables. Maximum length depends on carrier limits (typically 160 characters for single SMS, 1600 for concatenated).
  - **`calendar`**
    - `calendar` — ToolCalendarConfig **(required)**
      - `operation` — string **(required)** _(enum: `get_slots`, `schedule`, `reschedule`, `cancel`, `list_resource_events`)_
  - **`mcp`**
    - `mcp` — ToolMcpHandler **(required)**
      - `serverUrl` — string **(required)** — MCP server endpoint URL
      - `authorization` — union
        - _oneOf_ — exactly one of:
          - **`bearer`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`customHeaders`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `tools` — array **(required)** — List of tools enabled for this MCP server.
        - _array of_ `string`
  - **`mcpTool`**
    - `mcpTool` — ToolMcpToolHandler **(required)**
      - `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.

**`ToolInput`**

- `variables` — array **(required)** — List of tool variables, used to pass data to the tool
  - _array of_ `ToolVariable`
    - `name` — string **(required)** — Name of the tool variable, e.g.: 'myvar' _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
    - `type` — string **(required)** _(enum: `string`, `number`, `boolean`, `string_array`, `number_array`, `schema`)_
    - `optional` — boolean **(required)** — Whether the variable is optional
    - `description` — string — Original description from MCP tool schema (preserved)
    - `schema` — any — JSON Schema in case if type is schema

**`ToolMcpAuthorization`**

- _oneOf_ — exactly one of:
  - **`bearer`**
    - `bearer` — ToolWebhookAuthBearer **(required)**
      - `token` — string **(required)** — Bearer token value, supports static, variable, or template syntax
  - **`customHeaders`**
    - `customHeaders` — ToolMcpHeadersMap **(required)**
      - _map of_ `string`

**`ToolMcpHandler`**

- `serverUrl` — string **(required)** — MCP server endpoint URL
- `authorization` — union
  - _oneOf_ — exactly one of:
    - **`bearer`**
      - `bearer` — ToolWebhookAuthBearer **(required)**
        - `token` — string **(required)** — Bearer token value, supports static, variable, or template syntax
    - **`customHeaders`**
      - `customHeaders` — ToolMcpHeadersMap **(required)**
        - _map of_ `string`
- `tools` — array **(required)** — List of tools enabled for this MCP server.
  - _array of_ `string`

**`ToolMcpHeadersMap`**

- _map of_ `string`

**`ToolMcpToolHandler`**

- `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
- `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.

**`ToolSearchConfig`**

_Search handler configuration. API key comes from AppConfig; query comes from tool input. Optionally refine results using Tavily include_domains and/or exclude_domains (see Tavily domain filtering)._

- `includeDomains` — array — When non-empty, only return results from these domains or hosts. Customers may enter plain hostnames (example.com) or full URLs (https://example.com/path) — URLs are normalized to hostnames before calling the search API. _(maxItems=300)_
  - _array of_ `string`
- `excludeDomains` — array — When non-empty, omit results from these domains or hosts. Same hostname rules as includeDomains. Can be combined with includeDomains per Tavily API. _(maxItems=150)_
  - _array of_ `string`

**`ToolSmsConfig`**

- `from` — string **(required)** — Sender phone number in E.164 format (e.g., +1234567890). This is the phone number that will appear as the sender of the SMS. Supports template syntax with variables.
- `to` — string **(required)** — Recipient phone number in E.164 format (e.g., +1234567890). Supports template syntax with variables.
- `message` — string **(required)** — SMS message text to send. Supports template syntax with variables. Maximum length depends on carrier limits (typically 160 characters for single SMS, 1600 for concatenated).

**`ToolSmsHandler`**

- `config` — ToolSmsConfig **(required)**
  - `from` — string **(required)** — Sender phone number in E.164 format (e.g., +1234567890). This is the phone number that will appear as the sender of the SMS. Supports template syntax with variables.
  - `to` — string **(required)** — Recipient phone number in E.164 format (e.g., +1234567890). Supports template syntax with variables.
  - `message` — string **(required)** — SMS message text to send. Supports template syntax with variables. Maximum length depends on carrier limits (typically 160 characters for single SMS, 1600 for concatenated).

**`ToolSmtpConfig`**

- `host` — string **(required)** — SMTP server host, e.g.: 'smtp.gmail.com'
- `port` — number **(required)** — SMTP server port, e.g.: 587 _(min=1; max=65535)_
- `username` — string **(required)** — SMTP server username for authentication, e.g.: 'john.doe@gmail.com'
- `password` — string **(required)** — SMTP server password
- `secure` — boolean **(required)** — SMTP server secure connection

**`ToolVariable`**

- `name` — string **(required)** — Name of the tool variable, e.g.: 'myvar' _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
- `type` — string **(required)** _(enum: `string`, `number`, `boolean`, `string_array`, `number_array`, `schema`)_
- `optional` — boolean **(required)** — Whether the variable is optional
- `description` — string — Original description from MCP tool schema (preserved)
- `schema` — any — JSON Schema in case if type is schema

**`ToolVariableType`**

- string _(enum: `string`, `number`, `boolean`, `string_array`, `number_array`, `schema`)_

**`ToolWebhookAuth`**

- _oneOf_ — exactly one of:
  - **`basic`**
    - `basic` — ToolWebhookAuthBasic **(required)**
      - `username` — string **(required)** — Username for basic authentication
      - `password` — string **(required)** — Password for basic authentication
  - **`bearer`**
    - `bearer` — ToolWebhookAuthBearer **(required)**
      - `token` — string **(required)** — Bearer token value, supports static, variable, or template syntax
  - **`oauth`**
    - `oauth` — ToolWebhookAuthOAuth **(required)**
      - `clientId` — string **(required)** — OAuth client ID
      - `clientSecret` — string **(required)** — OAuth client secret
      - `endpointUrl` — string **(required)** — OAuth token endpoint URL
      - `scope` — string — OAuth scope

**`ToolWebhookAuthBasic`**

- `username` — string **(required)** — Username for basic authentication
- `password` — string **(required)** — Password for basic authentication

**`ToolWebhookAuthBearer`**

- `token` — string **(required)** — Bearer token value, supports static, variable, or template syntax

**`ToolWebhookAuthOAuth`**

- `clientId` — string **(required)** — OAuth client ID
- `clientSecret` — string **(required)** — OAuth client secret
- `endpointUrl` — string **(required)** — OAuth token endpoint URL
- `scope` — string — OAuth scope

**`ToolWebhookConfig`**

- `method` — string **(required)** _(enum: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`)_
- `url` — string **(required)** — URL endpoint for the webhook, supports variables in path and query parameters using {{variable_name}}, e.g.: 'https://api.example.com/users/{{userId}}?filter={{filter}}&page={{page}}'
- `headers` — array — HTTP headers for the webhook request. For custom authentication headers (e.g., X-API-Key), add them here instead of using auth.customHeader
  - _array of_ `ToolWebhookHeader`
    - `name` — string **(required)** — Header name, e.g.: 'X-Custom-Header'
    - `value` — string **(required)** — Header value, supports static, variable, or template syntax
- `body` — string — Request body for POST, PUT, or PATCH requests
- `auth` — union
  - _oneOf_ — exactly one of:
    - **`basic`**
      - `basic` — ToolWebhookAuthBasic **(required)**
        - `username` — string **(required)** — Username for basic authentication
        - `password` — string **(required)** — Password for basic authentication
    - **`bearer`**
      - `bearer` — ToolWebhookAuthBearer **(required)**
        - `token` — string **(required)** — Bearer token value, supports static, variable, or template syntax
    - **`oauth`**
      - `oauth` — ToolWebhookAuthOAuth **(required)**
        - `clientId` — string **(required)** — OAuth client ID
        - `clientSecret` — string **(required)** — OAuth client secret
        - `endpointUrl` — string **(required)** — OAuth token endpoint URL
        - `scope` — string — OAuth scope
- `timeout` — number — Time before webhook execution is stopped _(min=5000; max=120000)_

**`ToolWebhookHeader`**

- `name` — string **(required)** — Header name, e.g.: 'X-Custom-Header'
- `value` — string **(required)** — Header value, supports static, variable, or template syntax

**`ToolWebhookMethod`**

- string _(enum: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`)_

**`ToolWnsEmailConfig`**

- `to` — string **(required)** — To email address, e.g.: 'jane.doe@example.com'.
- `subject` — string **(required)** — Subject of the email.
- `text` — string **(required)** — Text of the email.

**`UnauthorizedExceptionResponseContent`**

- `message` — string **(required)**

**`UpdateToolRequestContent`**

- `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
- `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
- `description` — string **(required)** — Description of the tool, used by AI to understand the purpose of the tool. _(minLen=1; maxLen=4096)_
- `input` — ToolInput **(required)**
  - `variables` — array **(required)** — List of tool variables, used to pass data to the tool
    - _array of_ `ToolVariable`
      - `name` — string **(required)** — Name of the tool variable, e.g.: 'myvar' _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
      - `type` — string **(required)** _(enum: `string`, `number`, `boolean`, `string_array`, `number_array`, `schema`)_
      - `optional` — boolean **(required)** — Whether the variable is optional
      - `description` — string — Original description from MCP tool schema (preserved)
      - `schema` — any — JSON Schema in case if type is schema
- `handler` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`email`**
      - `email` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`wns`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`custom`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - **`webhook`**
      - `webhook` — ToolWebhookConfig **(required)**
        - `method` — string **(required)** _(enum: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`)_
        - `url` — string **(required)** — URL endpoint for the webhook, supports variables in path and query parameters using {{variable_name}}, e.g.: 'https://api.example.com/users/{{userId}}?filter={{filter}}&page={{page}}'
        - `headers` — array — HTTP headers for the webhook request. For custom authentication headers (e.g., X-API-Key), add them here instead of using auth.customHeader
          - _(nesting depth limit — see `ToolWebhookHeader` in the Schemas appendix)_
        - `body` — string — Request body for POST, PUT, or PATCH requests
        - `auth` — union
          - _(nesting depth limit — see `ToolWebhookAuth` in the Schemas appendix)_
        - `timeout` — number — Time before webhook execution is stopped _(min=5000; max=120000)_
    - **`search`**
      - `search` — ToolSearchConfig **(required)** — Search handler configuration. API key comes from AppConfig; query comes from tool input. Optionally refine results using Tavily include_domains and/or exclude_domains (see Tavily domain filtering).
        - `includeDomains` — array — When non-empty, only return results from these domains or hosts. Customers may enter plain hostnames (example.com) or full URLs (https://example.com/path) — URLs are normalized to hostnames before calling the search API. _(maxItems=300)_
          - _array of_ `string`
        - `excludeDomains` — array — When non-empty, omit results from these domains or hosts. Same hostname rules as includeDomains. Can be combined with includeDomains per Tavily API. _(maxItems=150)_
          - _array of_ `string`
    - **`chat`**
      - `chat` — ToolChatHandler **(required)**
        - `config` — ToolChatConfig **(required)**
          - _(nesting depth limit — see `ToolChatConfig` in the Schemas appendix)_
    - **`sms`**
      - `sms` — ToolSmsHandler **(required)**
        - `config` — ToolSmsConfig **(required)**
          - _(nesting depth limit — see `ToolSmsConfig` in the Schemas appendix)_
    - **`calendar`**
      - `calendar` — ToolCalendarConfig **(required)**
        - `operation` — string **(required)** _(enum: `get_slots`, `schedule`, `reschedule`, `cancel`, `list_resource_events`)_
    - **`mcp`**
      - `mcp` — ToolMcpHandler **(required)**
        - `serverUrl` — string **(required)** — MCP server endpoint URL
        - `authorization` — union
          - _(nesting depth limit — see `ToolMcpAuthorization` in the Schemas appendix)_
        - `tools` — array **(required)** — List of tools enabled for this MCP server.
          - _array of_ `string`
    - **`mcpTool`**
      - `mcpTool` — ToolMcpToolHandler **(required)**
        - `mcpToolId` — string **(required)** — ID of the Tool that represents the MCP server connection (the Tool with handler.mcp containing serverUrl and authorization) _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
        - `mcpToolName` — string **(required)** — Name of the tool on the MCP server. This matches the tool name returned from DiscoverTools operation.

**`UpdateToolResponseContent`**

- `tool` — Tool **(required)**
  - `id` — string **(required)** — Unique identifier of the tool _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
  - `companyId` — string **(required)** — Company ID that owns this tool _(minLen=3; maxLen=30)_
  - `name` — string **(required)** — Name of the tool, e.g.: 'send_email' _(pattern=^[a-zA-Z0-9_-]+$; minLen=1; maxLen=128)_
  - `category` — string **(required)** — Category of the tool, e.g.: 'Support' _(minLen=1; maxLen=128)_
  - `description` — string **(required)** — Description of the tool, used by AI to understand the purpose of the tool _(minLen=1; maxLen=4096)_
  - `input` — ToolInput **(required)**
    - `variables` — array **(required)** — List of tool variables, used to pass data to the tool
      - _array of_ `ToolVariable`
        - _(nesting depth limit — see `ToolVariable` in the Schemas appendix)_
  - `handler` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`email`**
        - `email` — union **(required)**
          - _(nesting depth limit — see `ToolEmailHandler` in the Schemas appendix)_
      - **`webhook`**
        - `webhook` — ToolWebhookConfig **(required)**
          - _(nesting depth limit — see `ToolWebhookConfig` in the Schemas appendix)_
      - **`search`**
        - `search` — ToolSearchConfig **(required)** — Search handler configuration. API key comes from AppConfig; query comes from tool input. Optionally refine results using Tavily include_domains and/or exclude_domains (see Tavily domain filtering).
          - _(nesting depth limit — see `ToolSearchConfig` in the Schemas appendix)_
      - **`chat`**
        - `chat` — ToolChatHandler **(required)**
          - _(nesting depth limit — see `ToolChatHandler` in the Schemas appendix)_
      - **`sms`**
        - `sms` — ToolSmsHandler **(required)**
          - _(nesting depth limit — see `ToolSmsHandler` in the Schemas appendix)_
      - **`calendar`**
        - `calendar` — ToolCalendarConfig **(required)**
          - _(nesting depth limit — see `ToolCalendarConfig` in the Schemas appendix)_
      - **`mcp`**
        - `mcp` — ToolMcpHandler **(required)**
          - _(nesting depth limit — see `ToolMcpHandler` in the Schemas appendix)_
      - **`mcpTool`**
        - `mcpTool` — ToolMcpToolHandler **(required)**
          - _(nesting depth limit — see `ToolMcpToolHandler` in the Schemas appendix)_

</details>
