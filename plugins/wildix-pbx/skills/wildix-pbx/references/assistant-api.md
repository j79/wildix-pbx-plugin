## Assistant API

_OpenAPI: x-bees assistant service — version v2_

**Servers**

- `https://api.x-bees.com` — Production
- `https://api-stable.x-bees.com` — Stable
- `https://api-stage.x-bees.com` — Stage

### Other

#### `POST` `/v2/assistant/completion`

- operationId: `ProcessCompletion`
- **Request body** (`application/json` — `ProcessCompletionRequestContent`) **(required)**
  - `content` — array _(minItems=1)_
    - _array of_ `ContentItem`
      - `user` — string **(required)**
      - `text` — string **(required)**
  - `contentString` — string _(minLen=3)_
  - `command` — string **(required)** _(enum: `prompt`, `summary`, `rephrase`, `reply`, `expand`, `shorten`, `explain`, `translate`)_
  - `connection` — string
  - `request` — string
  - `options` — ComletionOptions
    - _map of_ `string`
- **Response 200** (`ProcessCompletionResponseContent`)
  - `completion` — array **(required)**
    - _array of_ `CompletionItem`
      - `slot` — string **(required)**
      - `content` — string **(required)**
- Errors: `400`, `401`, `429`

#### `GET` `/v2/assistant/settings`

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 10 |
| XBS | 3600 | 300 |
| PBX | 60 | 100 |
| XBS_BOT | 60 | 100 |

- operationId: `GetSettings`
- **Response 200** (`GetSettingsResponseContent`)
  - `system` — array **(required)**
    - _array of_ `SystemCommandData`
      - `id` — string **(required)**
      - `label` — string **(required)** _(minLen=1)_
      - `type` — string **(required)** _(enum: `system`)_
      - `compatibility` — array **(required)**
        - _array of_ `CompatibilityType`
  - `user` — array **(required)**
    - _array of_ `UserCommandData`
      - `id` — string **(required)**
      - `label` — string **(required)** _(minLen=1)_
      - `type` — string **(required)** _(enum: `prompt`, `summary`, `rephrase`, `reply`, `expand`, `shorten`, `explain`, `translate`)_
      - `prompt` — string **(required)** _(minLen=1)_
- Errors: `400`, `401`, `429`

#### `POST` `/v2/assistant/settings/command`

- operationId: `PostSettings`
- **Request body** (`application/json` — `PostSettingsRequestContent`) **(required)**
  - `label` — string **(required)** _(minLen=1)_
  - `prompt` — string **(required)** _(minLen=1)_
- **Response 201** (`PostSettingsResponseContent`)
  - `result` — UserCommandData **(required)**
    - `id` — string **(required)**
    - `label` — string **(required)** _(minLen=1)_
    - `type` — string **(required)** _(enum: `prompt`, `summary`, `rephrase`, `reply`, `expand`, `shorten`, `explain`, `translate`)_
    - `prompt` — string **(required)** _(minLen=1)_
- Errors: `400`, `401`, `429`

#### `PUT` `/v2/assistant/settings/command/{id}`

- operationId: `PutSettings`
- **Parameters**
  - `id` (path) — string **(required)** _(minLen=6; maxLen=6)_
- **Request body** (`application/json` — `PutSettingsRequestContent`) **(required)**
  - `label` — string **(required)** _(minLen=1)_
  - `prompt` — string **(required)** _(minLen=1)_
- Errors: `400`, `401`, `404`, `429`

#### `DELETE` `/v2/assistant/settings/command/{id}`

- operationId: `DeleteSettings`
- **Parameters**
  - `id` (path) — string **(required)** _(minLen=6; maxLen=6)_
- Errors: `400`, `401`, `429`

### Schemas appendix — Assistant API

<details><summary>18 component schemas</summary>

**`ComletionOptions`**

- _map of_ `string`

**`CommandNotFoundExceptionResponseContent`**

- `message` — string **(required)**

**`CommandType`**

- string _(enum: `prompt`, `summary`, `rephrase`, `reply`, `expand`, `shorten`, `explain`, `translate`)_

**`CompatibilityType`**

- string _(enum: `message`, `draft`, `history`)_

**`CompletionItem`**

- `slot` — string **(required)**
- `content` — string **(required)**

**`ContentItem`**

- `user` — string **(required)**
- `text` — string **(required)**

**`GetSettingsResponseContent`**

- `system` — array **(required)**
  - _array of_ `SystemCommandData`
    - `id` — string **(required)**
    - `label` — string **(required)** _(minLen=1)_
    - `type` — string **(required)** _(enum: `system`)_
    - `compatibility` — array **(required)**
      - _array of_ `CompatibilityType`
- `user` — array **(required)**
  - _array of_ `UserCommandData`
    - `id` — string **(required)**
    - `label` — string **(required)** _(minLen=1)_
    - `type` — string **(required)** _(enum: `prompt`, `summary`, `rephrase`, `reply`, `expand`, `shorten`, `explain`, `translate`)_
    - `prompt` — string **(required)** _(minLen=1)_

**`PostSettingsRequestContent`**

- `label` — string **(required)** _(minLen=1)_
- `prompt` — string **(required)** _(minLen=1)_

**`PostSettingsResponseContent`**

- `result` — UserCommandData **(required)**
  - `id` — string **(required)**
  - `label` — string **(required)** _(minLen=1)_
  - `type` — string **(required)** _(enum: `prompt`, `summary`, `rephrase`, `reply`, `expand`, `shorten`, `explain`, `translate`)_
  - `prompt` — string **(required)** _(minLen=1)_

**`ProcessCompletionRequestContent`**

- `content` — array _(minItems=1)_
  - _array of_ `ContentItem`
    - `user` — string **(required)**
    - `text` — string **(required)**
- `contentString` — string _(minLen=3)_
- `command` — string **(required)** _(enum: `prompt`, `summary`, `rephrase`, `reply`, `expand`, `shorten`, `explain`, `translate`)_
- `connection` — string
- `request` — string
- `options` — ComletionOptions
  - _map of_ `string`

**`ProcessCompletionResponseContent`**

- `completion` — array **(required)**
  - _array of_ `CompletionItem`
    - `slot` — string **(required)**
    - `content` — string **(required)**

**`PutSettingsRequestContent`**

- `label` — string **(required)** _(minLen=1)_
- `prompt` — string **(required)** _(minLen=1)_

**`RateLimitExceededExceptionResponseContent`**

- `message` — string **(required)** _(default=Too Many Requests)_

**`SystemCommandData`**

- `id` — string **(required)**
- `label` — string **(required)** _(minLen=1)_
- `type` — string **(required)** _(enum: `system`)_
- `compatibility` — array **(required)**
  - _array of_ `CompatibilityType`

**`SystemCommandType`**

- string _(enum: `system`)_

**`UnauthorizedExceptionResponseContent`**

- `message` — string **(required)**

**`UserCommandData`**

- `id` — string **(required)**
- `label` — string **(required)** _(minLen=1)_
- `type` — string **(required)** _(enum: `prompt`, `summary`, `rephrase`, `reply`, `expand`, `shorten`, `explain`, `translate`)_
- `prompt` — string **(required)** _(minLen=1)_

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

</details>
