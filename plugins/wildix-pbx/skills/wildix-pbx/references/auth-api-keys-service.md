## Auth API Keys Service

_OpenAPI: Auth Api Keys — version —_

**Servers**

- `https://auth.wildix.com` — Production
- `https://auth-stable.wildix.com` — Stable
- `https://auth-stage.wildix.com` — Stage

### ApiKeys

#### `GET` `/api/v3/api-keys/`

List of Company API keys

- operationId: `ListApiKeys`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`ListApiKeysResponseContent`)
  - `apiKeys` — array **(required)**
    - _array of_ `ApiKey`
      - `id` — string **(required)** _(pattern=^[0-9a-zA-Z-]{40}$; minLen=40; maxLen=40)_
      - `companyId` — string **(required)**
      - `scopes` — array **(required)** _(maxItems=100)_
        - _array of_ `string`
      - `createdAt` — string **(required)**
      - `expiresAt` — string **(required)**
      - `updatedAt` — string **(required)**
      - `userExtension` — string — PBX user extension used to build user context for PBX-side Company API Key requests. _(pattern=^[0-9]+$; minLen=1; maxLen=64)_
      - `name` — string **(required)** — Human-readable name of the key (e.g., "Messaging ReadOnly", "Messaging ReadWrite, CloudAnalytics") _(minLen=3; maxLen=100)_
- Errors: `400`, `401`, `403`, `500`

#### `POST` `/api/v3/api-keys/`

Create an new Company API key.

- operationId: `CreateApiKey`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `CreateApiKeyRequestContent`) **(required)**
  - `name` — string **(required)** — Human-readable name of the key (e.g., "Messaging ReadOnly", "Messaging ReadWrite, CloudAnalytics") _(minLen=3; maxLen=100)_
  - `scopes` — array **(required)** _(maxItems=100)_
    - _array of_ `string`
  - `expiresAt` — string **(required)** — Api Key expire time (ISO 8601). Maximum value is now + 1 year.
  - `userExtension` — string — PBX user extension used to build user context for PBX-side Company API Key requests. _(pattern=^[0-9]+$; minLen=1; maxLen=64)_
- **Response 200** (`CreateApiKeyResponseContent`)
  - `apiKey` — ApiKeyFull **(required)**
    - `id` — string **(required)** _(pattern=^[0-9a-zA-Z-]{40}$; minLen=40; maxLen=40)_
    - `companyId` — string **(required)**
    - `scopes` — array **(required)** _(maxItems=100)_
      - _array of_ `string`
    - `createdAt` — string **(required)**
    - `expiresAt` — string **(required)**
    - `updatedAt` — string **(required)**
    - `userExtension` — string — PBX user extension used to build user context for PBX-side Company API Key requests. _(pattern=^[0-9]+$; minLen=1; maxLen=64)_
    - `name` — string **(required)** — Human-readable name of the key (e.g., "Messaging ReadOnly", "Messaging ReadWrite, CloudAnalytics") _(minLen=3; maxLen=100)_
    - `key` — string **(required)** — The key value is a 100-character string that starts with "wsk-v1-" followed by 93 alphanumeric characters. _(pattern=^wsk-v1-[0-9a-zA-Z]{93}$; minLen=100; maxLen=100)_
- Errors: `400`, `401`, `403`, `500`

#### `GET` `/api/v3/api-keys/self/data`

Get an Api key data by key value. This operation must be used for auth flow only with service auth.

- operationId: `GetApiKeyData`
- **Response 200** (`GetApiKeyDataResponseContent`)
  - `apiKey` — ApiKey **(required)**
    - `id` — string **(required)** _(pattern=^[0-9a-zA-Z-]{40}$; minLen=40; maxLen=40)_
    - `companyId` — string **(required)**
    - `scopes` — array **(required)** _(maxItems=100)_
      - _array of_ `string`
    - `createdAt` — string **(required)**
    - `expiresAt` — string **(required)**
    - `updatedAt` — string **(required)**
    - `userExtension` — string — PBX user extension used to build user context for PBX-side Company API Key requests. _(pattern=^[0-9]+$; minLen=1; maxLen=64)_
    - `name` — string **(required)** — Human-readable name of the key (e.g., "Messaging ReadOnly", "Messaging ReadWrite, CloudAnalytics") _(minLen=3; maxLen=100)_
- Errors: `400`, `401`, `403`, `404`, `500`

#### `GET` `/api/v3/api-keys/{id}`

Get an Company API key by its id. This operation must be used only for manage item.

- operationId: `GetApiKey`
- **Parameters**
  - `id` (path) — string **(required)** _(pattern=^[0-9a-zA-Z-]{40}$; minLen=40; maxLen=40)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetApiKeyResponseContent`)
  - `apiKey` — ApiKey **(required)**
    - `id` — string **(required)** _(pattern=^[0-9a-zA-Z-]{40}$; minLen=40; maxLen=40)_
    - `companyId` — string **(required)**
    - `scopes` — array **(required)** _(maxItems=100)_
      - _array of_ `string`
    - `createdAt` — string **(required)**
    - `expiresAt` — string **(required)**
    - `updatedAt` — string **(required)**
    - `userExtension` — string — PBX user extension used to build user context for PBX-side Company API Key requests. _(pattern=^[0-9]+$; minLen=1; maxLen=64)_
    - `name` — string **(required)** — Human-readable name of the key (e.g., "Messaging ReadOnly", "Messaging ReadWrite, CloudAnalytics") _(minLen=3; maxLen=100)_
- Errors: `400`, `401`, `403`, `404`, `500`

#### `PUT` `/api/v3/api-keys/{id}`

Update an Company API key.

- operationId: `UpdateApiKey`
- **Parameters**
  - `id` (path) — string **(required)** _(pattern=^[0-9a-zA-Z-]{40}$; minLen=40; maxLen=40)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `UpdateApiKeyRequestContent`) **(required)**
  - `name` — string **(required)** — Human-readable name of the key (e.g., "Messaging ReadOnly", "Messaging ReadWrite, CloudAnalytics") _(minLen=3; maxLen=100)_
- **Response 200** (`UpdateApiKeyResponseContent`)
  - `apiKey` — ApiKey **(required)**
    - `id` — string **(required)** _(pattern=^[0-9a-zA-Z-]{40}$; minLen=40; maxLen=40)_
    - `companyId` — string **(required)**
    - `scopes` — array **(required)** _(maxItems=100)_
      - _array of_ `string`
    - `createdAt` — string **(required)**
    - `expiresAt` — string **(required)**
    - `updatedAt` — string **(required)**
    - `userExtension` — string — PBX user extension used to build user context for PBX-side Company API Key requests. _(pattern=^[0-9]+$; minLen=1; maxLen=64)_
    - `name` — string **(required)** — Human-readable name of the key (e.g., "Messaging ReadOnly", "Messaging ReadWrite, CloudAnalytics") _(minLen=3; maxLen=100)_
- Errors: `400`, `401`, `403`, `404`, `500`

#### `DELETE` `/api/v3/api-keys/{id}`

Delete an Company API key.

- operationId: `DeleteApiKey`
- **Parameters**
  - `id` (path) — string **(required)** _(pattern=^[0-9a-zA-Z-]{40}$; minLen=40; maxLen=40)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- Errors: `400`, `401`, `403`, `404`, `500`

#### `GET` `/api/v3/scopes`

Get list of allowed authorization scopes.

- operationId: `ListScopes`
- **Response 200** (`ListScopesResponseContent`)
  - `scopes` — array
    - _array of_ `ScopeItem`
      - `scope` — string **(required)** _(pattern=^[0-9a-zA-Z_*]+:[0-9a-zA-Z-_*]+$; minLen=1; maxLen=100)_
      - `description` — string **(required)**
      - `group` — string **(required)**
      - `status` — string — Current scope status: future, deprecated etc.
- Errors: `400`, `401`, `403`, `500`

### Schemas appendix — Auth API Keys Service

<details><summary>16 component schemas</summary>

**`ApiKey`**

- `id` — string **(required)** _(pattern=^[0-9a-zA-Z-]{40}$; minLen=40; maxLen=40)_
- `companyId` — string **(required)**
- `scopes` — array **(required)** _(maxItems=100)_
  - _array of_ `string`
- `createdAt` — string **(required)**
- `expiresAt` — string **(required)**
- `updatedAt` — string **(required)**
- `userExtension` — string — PBX user extension used to build user context for PBX-side Company API Key requests. _(pattern=^[0-9]+$; minLen=1; maxLen=64)_
- `name` — string **(required)** — Human-readable name of the key (e.g., "Messaging ReadOnly", "Messaging ReadWrite, CloudAnalytics") _(minLen=3; maxLen=100)_

**`ApiKeyFull`**

- `id` — string **(required)** _(pattern=^[0-9a-zA-Z-]{40}$; minLen=40; maxLen=40)_
- `companyId` — string **(required)**
- `scopes` — array **(required)** _(maxItems=100)_
  - _array of_ `string`
- `createdAt` — string **(required)**
- `expiresAt` — string **(required)**
- `updatedAt` — string **(required)**
- `userExtension` — string — PBX user extension used to build user context for PBX-side Company API Key requests. _(pattern=^[0-9]+$; minLen=1; maxLen=64)_
- `name` — string **(required)** — Human-readable name of the key (e.g., "Messaging ReadOnly", "Messaging ReadWrite, CloudAnalytics") _(minLen=3; maxLen=100)_
- `key` — string **(required)** — The key value is a 100-character string that starts with "wsk-v1-" followed by 93 alphanumeric characters. _(pattern=^wsk-v1-[0-9a-zA-Z]{93}$; minLen=100; maxLen=100)_

**`ApiKeyNotFoundExceptionResponseContent`**

- `message` — string **(required)**

**`BadRequestExceptionResponseContent`**

- `message` — string **(required)**

**`CreateApiKeyRequestContent`**

- `name` — string **(required)** — Human-readable name of the key (e.g., "Messaging ReadOnly", "Messaging ReadWrite, CloudAnalytics") _(minLen=3; maxLen=100)_
- `scopes` — array **(required)** _(maxItems=100)_
  - _array of_ `string`
- `expiresAt` — string **(required)** — Api Key expire time (ISO 8601). Maximum value is now + 1 year.
- `userExtension` — string — PBX user extension used to build user context for PBX-side Company API Key requests. _(pattern=^[0-9]+$; minLen=1; maxLen=64)_

**`CreateApiKeyResponseContent`**

- `apiKey` — ApiKeyFull **(required)**
  - `id` — string **(required)** _(pattern=^[0-9a-zA-Z-]{40}$; minLen=40; maxLen=40)_
  - `companyId` — string **(required)**
  - `scopes` — array **(required)** _(maxItems=100)_
    - _array of_ `string`
  - `createdAt` — string **(required)**
  - `expiresAt` — string **(required)**
  - `updatedAt` — string **(required)**
  - `userExtension` — string — PBX user extension used to build user context for PBX-side Company API Key requests. _(pattern=^[0-9]+$; minLen=1; maxLen=64)_
  - `name` — string **(required)** — Human-readable name of the key (e.g., "Messaging ReadOnly", "Messaging ReadWrite, CloudAnalytics") _(minLen=3; maxLen=100)_
  - `key` — string **(required)** — The key value is a 100-character string that starts with "wsk-v1-" followed by 93 alphanumeric characters. _(pattern=^wsk-v1-[0-9a-zA-Z]{93}$; minLen=100; maxLen=100)_

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GetApiKeyDataResponseContent`**

- `apiKey` — ApiKey **(required)**
  - `id` — string **(required)** _(pattern=^[0-9a-zA-Z-]{40}$; minLen=40; maxLen=40)_
  - `companyId` — string **(required)**
  - `scopes` — array **(required)** _(maxItems=100)_
    - _array of_ `string`
  - `createdAt` — string **(required)**
  - `expiresAt` — string **(required)**
  - `updatedAt` — string **(required)**
  - `userExtension` — string — PBX user extension used to build user context for PBX-side Company API Key requests. _(pattern=^[0-9]+$; minLen=1; maxLen=64)_
  - `name` — string **(required)** — Human-readable name of the key (e.g., "Messaging ReadOnly", "Messaging ReadWrite, CloudAnalytics") _(minLen=3; maxLen=100)_

**`GetApiKeyResponseContent`**

- `apiKey` — ApiKey **(required)**
  - `id` — string **(required)** _(pattern=^[0-9a-zA-Z-]{40}$; minLen=40; maxLen=40)_
  - `companyId` — string **(required)**
  - `scopes` — array **(required)** _(maxItems=100)_
    - _array of_ `string`
  - `createdAt` — string **(required)**
  - `expiresAt` — string **(required)**
  - `updatedAt` — string **(required)**
  - `userExtension` — string — PBX user extension used to build user context for PBX-side Company API Key requests. _(pattern=^[0-9]+$; minLen=1; maxLen=64)_
  - `name` — string **(required)** — Human-readable name of the key (e.g., "Messaging ReadOnly", "Messaging ReadWrite, CloudAnalytics") _(minLen=3; maxLen=100)_

**`InternalServerErrorResponseContent`**

- `message` — string **(required)**

**`ListApiKeysResponseContent`**

- `apiKeys` — array **(required)**
  - _array of_ `ApiKey`
    - `id` — string **(required)** _(pattern=^[0-9a-zA-Z-]{40}$; minLen=40; maxLen=40)_
    - `companyId` — string **(required)**
    - `scopes` — array **(required)** _(maxItems=100)_
      - _array of_ `string`
    - `createdAt` — string **(required)**
    - `expiresAt` — string **(required)**
    - `updatedAt` — string **(required)**
    - `userExtension` — string — PBX user extension used to build user context for PBX-side Company API Key requests. _(pattern=^[0-9]+$; minLen=1; maxLen=64)_
    - `name` — string **(required)** — Human-readable name of the key (e.g., "Messaging ReadOnly", "Messaging ReadWrite, CloudAnalytics") _(minLen=3; maxLen=100)_

**`ListScopesResponseContent`**

- `scopes` — array
  - _array of_ `ScopeItem`
    - `scope` — string **(required)** _(pattern=^[0-9a-zA-Z_*]+:[0-9a-zA-Z-_*]+$; minLen=1; maxLen=100)_
    - `description` — string **(required)**
    - `group` — string **(required)**
    - `status` — string — Current scope status: future, deprecated etc.

**`ScopeItem`**

- `scope` — string **(required)** _(pattern=^[0-9a-zA-Z_*]+:[0-9a-zA-Z-_*]+$; minLen=1; maxLen=100)_
- `description` — string **(required)**
- `group` — string **(required)**
- `status` — string — Current scope status: future, deprecated etc.

**`UnauthorizedExceptionResponseContent`**

- `message` — string **(required)**

**`UpdateApiKeyRequestContent`**

- `name` — string **(required)** — Human-readable name of the key (e.g., "Messaging ReadOnly", "Messaging ReadWrite, CloudAnalytics") _(minLen=3; maxLen=100)_

**`UpdateApiKeyResponseContent`**

- `apiKey` — ApiKey **(required)**
  - `id` — string **(required)** _(pattern=^[0-9a-zA-Z-]{40}$; minLen=40; maxLen=40)_
  - `companyId` — string **(required)**
  - `scopes` — array **(required)** _(maxItems=100)_
    - _array of_ `string`
  - `createdAt` — string **(required)**
  - `expiresAt` — string **(required)**
  - `updatedAt` — string **(required)**
  - `userExtension` — string — PBX user extension used to build user context for PBX-side Company API Key requests. _(pattern=^[0-9]+$; minLen=1; maxLen=64)_
  - `name` — string **(required)** — Human-readable name of the key (e.g., "Messaging ReadOnly", "Messaging ReadWrite, CloudAnalytics") _(minLen=3; maxLen=100)_

</details>
