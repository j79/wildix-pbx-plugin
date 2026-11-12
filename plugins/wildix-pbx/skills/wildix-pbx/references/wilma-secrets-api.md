## Wilma Secrets API (Credential Broker) 🆕

_OpenAPI: Wilma Credential Broker — version v2_

**Servers**

- `https://api.wilma.wildix.com` — Production
- `https://api-stable.wilma.wildix.com` — Stable
- `https://api-stage.wilma.wildix.com` — Stage

### Other

#### `GET` `/v2/secrets`

Lists company secrets (metadata only).

- operationId: `ListSecrets`
- **Scopes**: `wilma-secrets:ListSecrets`, `wilma-secrets:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `variant` (query) — string — Filter by the `variant` attribute, e.g. 'auth_client_credentials'. Omit to list every secret. _(minLen=1; maxLen=2048)_
  - `status` (query) — string — Filter by lifecycle state. Omit to list every secret. _(enum: `pending`, `active`)_
  - `search` (query) — string — Case-insensitive filter on the secret's name and description. Combined with the other filters by AND. Without it a console can only search the page it has already loaded, which in a company past one page answers "no such credential" for one that exists.
  - `limit` (query) — number _(min=1; max=100)_
  - `cursor` (query) — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- **Response 200** (`ListSecretsResponseContent`)
  - `secrets` — array **(required)** — Secrets returned by list operations (metadata only).
    - _array of_ `Secret`
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
      - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
      - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
      - `name` — string **(required)** — Human- and machine-readable secret name, unique per company. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
      - `description` — string _(minLen=1; maxLen=1024)_
      - `attributes` — SecretAttributes — Non-secret companion fields, returned on management responses (the sensitive half stays in `value`). An optional `variant` key classifies the secret's shape (e.g. 'auth_basic', 'auth_bearer', 'auth_client_credentials'); the remaining keys are the companions that shape implies (e.g. 'auth_client_credentials' → { clientId, endpointUrl, scope }). Variants are an open convention, not a fixed enum; ListSecrets can filter by `variant`.
        - _map of_ `string`
      - `revision` — number **(required)** — Current revision, bumped on every rotation. Informational only. _(min=1)_
      - `status` — string **(required)** — Lifecycle state of a secret. _(enum: `pending`, `active`)_
      - `expiresAt` — string — When the credential behind this secret stops working, if that is known. Absent means unknown, which is the common case — it is recorded by whoever files the secret, not discovered. Informational, and deliberately not enforced: nothing refuses to resolve a secret past this instant, because the platform cannot know the provider agrees and a wrong date would then take down a working integration. It exists so a console can warn before an API key with a known lifetime fails, rather than the platform learning it from a failed agent turn.
      - `lastUsedAt` — string — When a runtime last resolved this credential, to the minute. Absent means never. Written on the resolve path, not by a management edit: reading a credential is not changing it, so this moves independently of the audit fields. Coarsened to the minute because the question it answers is asked in days and weeks, and an agent in a tool loop would otherwise rewrite it on every outbound call. Absent rather than an epoch for a credential nothing has used, because "nothing has ever resolved this" is a different and more actionable fact than "a long time ago" — it is what lets a console say a credential is safe to delete.
  - `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- Errors: `400`, `404`, `409`

#### `POST` `/v2/secrets`

Creates a company secret. The value is stored envelope-encrypted and never returned.
`value` is optional: a secret created without one is referenceable immediately but stays
`PENDING` until `RotateSecret` supplies a value.

- operationId: `CreateSecret`
- **Scopes**: `wilma-secrets:CreateSecret`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `CreateSecretRequestContent`) **(required)**
  - `name` — string **(required)** — Human- and machine-readable secret name, unique per company. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
  - `description` — string _(minLen=1; maxLen=1024)_
  - `value` — string — Secret material. Write-only; stored envelope-encrypted. Omit to create the secret without one: it stays `PENDING` until `RotateSecret` supplies a value. _(format=password; minLen=1; maxLen=65536)_
  - `attributes` — SecretAttributes — Non-secret companion fields, returned on management responses (the sensitive half stays in `value`). An optional `variant` key classifies the secret's shape (e.g. 'auth_basic', 'auth_bearer', 'auth_client_credentials'); the remaining keys are the companions that shape implies (e.g. 'auth_client_credentials' → { clientId, endpointUrl, scope }). Variants are an open convention, not a fixed enum; ListSecrets can filter by `variant`.
    - _map of_ `string`
- **Response 201** (`CreateSecretResponseContent`)
  - `secret` — Secret **(required)** — A stored secret. The sensitive value is never included; non-secret attributes are.
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
    - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `name` — string **(required)** — Human- and machine-readable secret name, unique per company. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
    - `description` — string _(minLen=1; maxLen=1024)_
    - `attributes` — SecretAttributes — Non-secret companion fields, returned on management responses (the sensitive half stays in `value`). An optional `variant` key classifies the secret's shape (e.g. 'auth_basic', 'auth_bearer', 'auth_client_credentials'); the remaining keys are the companions that shape implies (e.g. 'auth_client_credentials' → { clientId, endpointUrl, scope }). Variants are an open convention, not a fixed enum; ListSecrets can filter by `variant`.
      - _map of_ `string`
    - `revision` — number **(required)** — Current revision, bumped on every rotation. Informational only. _(min=1)_
    - `status` — string **(required)** — Lifecycle state of a secret. _(enum: `pending`, `active`)_
    - `expiresAt` — string — When the credential behind this secret stops working, if that is known. Absent means unknown, which is the common case — it is recorded by whoever files the secret, not discovered. Informational, and deliberately not enforced: nothing refuses to resolve a secret past this instant, because the platform cannot know the provider agrees and a wrong date would then take down a working integration. It exists so a console can warn before an API key with a known lifetime fails, rather than the platform learning it from a failed agent turn.
    - `lastUsedAt` — string — When a runtime last resolved this credential, to the minute. Absent means never. Written on the resolve path, not by a management edit: reading a credential is not changing it, so this moves independently of the audit fields. Coarsened to the minute because the question it answers is asked in days and weeks, and an agent in a tool loop would otherwise rewrite it on every outbound call. Absent rather than an epoch for a credential nothing has used, because "nothing has ever resolved this" is a different and more actionable fact than "a long time ago" — it is what lets a console say a credential is safe to delete.
- Errors: `400`, `404`, `409`

#### `GET` `/v2/secrets/connections`

Lists the company's connections, SHARED and USER. Filter by `type`, `provider`, or `user`
(combined with AND).

- operationId: `ListConnections`
- **Scopes**: `wilma-secrets:ListConnections`, `wilma-secrets:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `provider` (query) — string — Filter by provider key, e.g. 'salesforce'. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
  - `type` (query) — string — Filter by connection type — SHARED (company) or USER (per-end-user). _(enum: `shared`, `user`)_
  - `user` (query) — string — Filter by owning end user; returns that user's USER connections. Ignored for SHARED connections, which have no owning user. _(minLen=12; maxLen=12)_
  - `serverUrl` (query) — string — Only connections to this remote MCP server. The service derives the server's provider key, so a client never has to; combined with `provider`, a key that disagrees matches nothing. _(minLen=1; maxLen=2048)_
  - `search` (query) — string — Case-insensitive filter on the connection's name and description, and on the owning user's name and email for a USER connection. Combined with the other filters by AND.
  - `limit` (query) — number _(min=1; max=100)_
  - `cursor` (query) — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- **Response 200** (`ListConnectionsResponseContent`)
  - `connections` — array **(required)** — Connections returned by list operations.
    - _array of_ `Connection`
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
      - `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
      - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
      - `type` — string **(required)** — Who a connection's credential belongs to. _(enum: `shared`, `user`)_
      - `provider` — string **(required)** — Provider key the connection authenticates against, e.g. "salesforce". A remote MCP server is created as `mcp`, with its URL in `connectionConfig.mcp_server_url`. The connection is filed under `mcp_` plus a digest of the server's canonical URL, which is the key every later operation uses: one key for every spelling of one server, and a key that keeps a URL carrying an access key out of request paths and audit rows. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
      - `name` — string — Admin-given name, unique per company. Set for SHARED connections; absent for USER connections, which are identified by provider + `actor`. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
      - `description` — string _(minLen=1; maxLen=1024)_
      - `status` — string **(required)** — Lifecycle state of a connection. For a SHARED connection it is the company credential's state; for a USER connection it is that user's authorization state (PENDING until the user authorizes). _(enum: `pending`, `active`, `expired`, `error`)_
      - `scopes` — array — OAuth scopes requested for the connection.
        - _array of_ `string`
      - `connectionConfig` — ConnectionConfig — Provider parameters the authorization flow itself needs, e.g. `{"hostname": "eu.app.clio.com"}`. A provider may template its OAuth endpoints on these — Clio's authorization and token URLs are both `https://${connectionConfig.hostname}/…` — so for those providers a connection simply cannot be authorized without one. Which fields a provider declares, and their allowed values, are published on the connector definition as `authorization.connectionConfiguration`. Configuration, never credentials. The keys a provider's broker reserves for swapping the OAuth application itself are refused rather than forwarded.
        - _map of_ `string`
      - `actor` — ConnectionActor — The end user who owns a USER connection. A display snapshot only; never used to resolve the credential (that is keyed by provider + user).
        - `id` — string **(required)** — Wildix user id of the owning end user. _(minLen=12; maxLen=12)_
        - `name` — string — Display name at the time the connection was recorded.
        - `email` — string — Email of the owning user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
        - `extension` — string — PBX extension of the owning user.
      - `serverUrl` — string — The remote MCP server this connection is for, as `connectionConfig.mcp_server_url` named it. Present only for an `mcp_*` provider. Read-only: the provider key is a digest of it, so it is what a person reads in place of that key. _(minLen=1; maxLen=2048)_
      - `lastUsedAt` — string — When a runtime last minted a token from this connection, to the minute. Absent means never. Written on the resolve path rather than by a management edit, so it moves independently of the audit fields — reading a credential is not changing it.
  - `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_
- Errors: `400`, `404`, `409`

#### `POST` `/v2/secrets/connections`

Creates a company-wide SHARED connection. It starts PENDING; authorize it with
CreateConnectSession, unless the provider resolves it non-interactively (client-credentials,
API key). USER connections are not created here — each user authorizes the provider themselves.

- operationId: `CreateConnection`
- **Scopes**: `wilma-secrets:CreateConnection`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `CreateConnectionRequestContent`) **(required)**
  - `name` — string **(required)** — Connection name, unique per company. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
  - `description` — string _(minLen=1; maxLen=1024)_
  - `provider` — string **(required)** — Provider key the connection authenticates against, e.g. "salesforce". A remote MCP server is created as `mcp`, with its URL in `connectionConfig.mcp_server_url`. The connection is filed under `mcp_` plus a digest of the server's canonical URL, which is the key every later operation uses: one key for every spelling of one server, and a key that keeps a URL carrying an access key out of request paths and audit rows. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
  - `scopes` — array — OAuth scopes requested for the connection.
    - _array of_ `string`
  - `connectionConfig` — ConnectionConfig — Provider parameters the authorization flow itself needs, e.g. `{"hostname": "eu.app.clio.com"}`. A provider may template its OAuth endpoints on these — Clio's authorization and token URLs are both `https://${connectionConfig.hostname}/…` — so for those providers a connection simply cannot be authorized without one. Which fields a provider declares, and their allowed values, are published on the connector definition as `authorization.connectionConfiguration`. Configuration, never credentials. The keys a provider's broker reserves for swapping the OAuth application itself are refused rather than forwarded.
    - _map of_ `string`
- **Response 201** (`CreateConnectionResponseContent`)
  - `connection` — Connection **(required)** — A configured connection: a company-wide SHARED credential, or a per-user USER credential. Holds registry and ownership metadata only, never the credential itself. `type` is the kind; `actor` is the owning user for USER connections.
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
    - `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `type` — string **(required)** — Who a connection's credential belongs to. _(enum: `shared`, `user`)_
    - `provider` — string **(required)** — Provider key the connection authenticates against, e.g. "salesforce". A remote MCP server is created as `mcp`, with its URL in `connectionConfig.mcp_server_url`. The connection is filed under `mcp_` plus a digest of the server's canonical URL, which is the key every later operation uses: one key for every spelling of one server, and a key that keeps a URL carrying an access key out of request paths and audit rows. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
    - `name` — string — Admin-given name, unique per company. Set for SHARED connections; absent for USER connections, which are identified by provider + `actor`. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
    - `description` — string _(minLen=1; maxLen=1024)_
    - `status` — string **(required)** — Lifecycle state of a connection. For a SHARED connection it is the company credential's state; for a USER connection it is that user's authorization state (PENDING until the user authorizes). _(enum: `pending`, `active`, `expired`, `error`)_
    - `scopes` — array — OAuth scopes requested for the connection.
      - _array of_ `string`
    - `connectionConfig` — ConnectionConfig — Provider parameters the authorization flow itself needs, e.g. `{"hostname": "eu.app.clio.com"}`. A provider may template its OAuth endpoints on these — Clio's authorization and token URLs are both `https://${connectionConfig.hostname}/…` — so for those providers a connection simply cannot be authorized without one. Which fields a provider declares, and their allowed values, are published on the connector definition as `authorization.connectionConfiguration`. Configuration, never credentials. The keys a provider's broker reserves for swapping the OAuth application itself are refused rather than forwarded.
      - _map of_ `string`
    - `actor` — ConnectionActor — The end user who owns a USER connection. A display snapshot only; never used to resolve the credential (that is keyed by provider + user).
      - `id` — string **(required)** — Wildix user id of the owning end user. _(minLen=12; maxLen=12)_
      - `name` — string — Display name at the time the connection was recorded.
      - `email` — string — Email of the owning user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `extension` — string — PBX extension of the owning user.
    - `serverUrl` — string — The remote MCP server this connection is for, as `connectionConfig.mcp_server_url` named it. Present only for an `mcp_*` provider. Read-only: the provider key is a digest of it, so it is what a person reads in place of that key. _(minLen=1; maxLen=2048)_
    - `lastUsedAt` — string — When a runtime last minted a token from this connection, to the minute. Absent means never. Written on the resolve path rather than by a management edit, so it moves independently of the audit fields — reading a credential is not changing it.
- Errors: `400`, `404`, `409`

#### `GET` `/v2/secrets/connections/{connectionId}`

Gets a connection by id — SHARED or USER (registry/ownership metadata; never the credential).

- operationId: `GetConnection`
- **Scopes**: `wilma-secrets:GetConnection`, `wilma-secrets:read`
- **Parameters**
  - `connectionId` (path) — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetConnectionResponseContent`)
  - `connection` — Connection **(required)** — A configured connection: a company-wide SHARED credential, or a per-user USER credential. Holds registry and ownership metadata only, never the credential itself. `type` is the kind; `actor` is the owning user for USER connections.
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
    - `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `type` — string **(required)** — Who a connection's credential belongs to. _(enum: `shared`, `user`)_
    - `provider` — string **(required)** — Provider key the connection authenticates against, e.g. "salesforce". A remote MCP server is created as `mcp`, with its URL in `connectionConfig.mcp_server_url`. The connection is filed under `mcp_` plus a digest of the server's canonical URL, which is the key every later operation uses: one key for every spelling of one server, and a key that keeps a URL carrying an access key out of request paths and audit rows. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
    - `name` — string — Admin-given name, unique per company. Set for SHARED connections; absent for USER connections, which are identified by provider + `actor`. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
    - `description` — string _(minLen=1; maxLen=1024)_
    - `status` — string **(required)** — Lifecycle state of a connection. For a SHARED connection it is the company credential's state; for a USER connection it is that user's authorization state (PENDING until the user authorizes). _(enum: `pending`, `active`, `expired`, `error`)_
    - `scopes` — array — OAuth scopes requested for the connection.
      - _array of_ `string`
    - `connectionConfig` — ConnectionConfig — Provider parameters the authorization flow itself needs, e.g. `{"hostname": "eu.app.clio.com"}`. A provider may template its OAuth endpoints on these — Clio's authorization and token URLs are both `https://${connectionConfig.hostname}/…` — so for those providers a connection simply cannot be authorized without one. Which fields a provider declares, and their allowed values, are published on the connector definition as `authorization.connectionConfiguration`. Configuration, never credentials. The keys a provider's broker reserves for swapping the OAuth application itself are refused rather than forwarded.
      - _map of_ `string`
    - `actor` — ConnectionActor — The end user who owns a USER connection. A display snapshot only; never used to resolve the credential (that is keyed by provider + user).
      - `id` — string **(required)** — Wildix user id of the owning end user. _(minLen=12; maxLen=12)_
      - `name` — string — Display name at the time the connection was recorded.
      - `email` — string — Email of the owning user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `extension` — string — PBX extension of the owning user.
    - `serverUrl` — string — The remote MCP server this connection is for, as `connectionConfig.mcp_server_url` named it. Present only for an `mcp_*` provider. Read-only: the provider key is a digest of it, so it is what a person reads in place of that key. _(minLen=1; maxLen=2048)_
    - `lastUsedAt` — string — When a runtime last minted a token from this connection, to the minute. Absent means never. Written on the resolve path rather than by a management edit, so it moves independently of the audit fields — reading a credential is not changing it.
- Errors: `400`, `404`, `409`

#### `PUT` `/v2/secrets/connections/{connectionId}`

Updates connection metadata (name, description, scopes).

- operationId: `UpdateConnection`
- **Scopes**: `wilma-secrets:UpdateConnection`
- **Parameters**
  - `connectionId` (path) — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `UpdateConnectionRequestContent`) **(required)**
  - `name` — string **(required)** — Connection name, unique per company. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
  - `description` — string _(minLen=1; maxLen=1024)_
  - `scopes` — array — OAuth scopes requested for the connection.
    - _array of_ `string`
- **Response 200** (`UpdateConnectionResponseContent`)
  - `connection` — Connection **(required)** — A configured connection: a company-wide SHARED credential, or a per-user USER credential. Holds registry and ownership metadata only, never the credential itself. `type` is the kind; `actor` is the owning user for USER connections.
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
    - `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `type` — string **(required)** — Who a connection's credential belongs to. _(enum: `shared`, `user`)_
    - `provider` — string **(required)** — Provider key the connection authenticates against, e.g. "salesforce". A remote MCP server is created as `mcp`, with its URL in `connectionConfig.mcp_server_url`. The connection is filed under `mcp_` plus a digest of the server's canonical URL, which is the key every later operation uses: one key for every spelling of one server, and a key that keeps a URL carrying an access key out of request paths and audit rows. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
    - `name` — string — Admin-given name, unique per company. Set for SHARED connections; absent for USER connections, which are identified by provider + `actor`. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
    - `description` — string _(minLen=1; maxLen=1024)_
    - `status` — string **(required)** — Lifecycle state of a connection. For a SHARED connection it is the company credential's state; for a USER connection it is that user's authorization state (PENDING until the user authorizes). _(enum: `pending`, `active`, `expired`, `error`)_
    - `scopes` — array — OAuth scopes requested for the connection.
      - _array of_ `string`
    - `connectionConfig` — ConnectionConfig — Provider parameters the authorization flow itself needs, e.g. `{"hostname": "eu.app.clio.com"}`. A provider may template its OAuth endpoints on these — Clio's authorization and token URLs are both `https://${connectionConfig.hostname}/…` — so for those providers a connection simply cannot be authorized without one. Which fields a provider declares, and their allowed values, are published on the connector definition as `authorization.connectionConfiguration`. Configuration, never credentials. The keys a provider's broker reserves for swapping the OAuth application itself are refused rather than forwarded.
      - _map of_ `string`
    - `actor` — ConnectionActor — The end user who owns a USER connection. A display snapshot only; never used to resolve the credential (that is keyed by provider + user).
      - `id` — string **(required)** — Wildix user id of the owning end user. _(minLen=12; maxLen=12)_
      - `name` — string — Display name at the time the connection was recorded.
      - `email` — string — Email of the owning user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `extension` — string — PBX extension of the owning user.
    - `serverUrl` — string — The remote MCP server this connection is for, as `connectionConfig.mcp_server_url` named it. Present only for an `mcp_*` provider. Read-only: the provider key is a digest of it, so it is what a person reads in place of that key. _(minLen=1; maxLen=2048)_
    - `lastUsedAt` — string — When a runtime last minted a token from this connection, to the minute. Absent means never. Written on the resolve path rather than by a management edit, so it moves independently of the audit fields — reading a credential is not changing it.
- Errors: `400`, `404`, `409`

#### `DELETE` `/v2/secrets/connections/{connectionId}`

Deletes a connection by id — SHARED or USER — and revokes its stored credential. Deleting a
USER connection disconnects that user from the provider. Usage is not checked: any dangling
reference fails to authorize on its next access.

- operationId: `DeleteConnection`
- **Scopes**: `wilma-secrets:DeleteConnection`
- **Parameters**
  - `connectionId` (path) — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- Errors: `400`, `404`, `409`

#### `POST` `/v2/secrets/connections/{connectionId}/confirm`

Records the connection a finished company authorization produced, and marks the row ACTIVE.

The SHARED counterpart of ConfirmUserConnection, and the only way a widened scope list can ever
be consented to. `UpdateConnection` returns a row to PENDING when its scopes widen, but nothing
could move it back: discovery gives up as soon as `externalId` is set, and a successful resolve
promotes only a row marked ERROR. Discovery cannot stand in for consent either — the credential
authorized under the narrower scopes is still in the vault under the same end-user id, so
re-discovering it would mark the row ACTIVE whether or not anybody re-authorized.

The browser reports the id the authorization flow returned, and the service verifies it against
the provider and against the end user the session was minted for before mapping it. That check
is what makes this consent rather than a claim.

- operationId: `ConfirmConnection`
- **Scopes**: `wilma-secrets:ConfirmConnection`
- **Parameters**
  - `connectionId` (path) — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `ConfirmConnectionRequestContent`) **(required)**
  - `externalConnectionId` — string **(required)** — Connection id returned by the authorization flow. Verified against the provider and the end user the connect session named before it is stored. _(minLen=1; maxLen=256)_
- **Response 200** (`ConfirmConnectionResponseContent`)
  - `connection` — Connection **(required)** — A configured connection: a company-wide SHARED credential, or a per-user USER credential. Holds registry and ownership metadata only, never the credential itself. `type` is the kind; `actor` is the owning user for USER connections.
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
    - `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `type` — string **(required)** — Who a connection's credential belongs to. _(enum: `shared`, `user`)_
    - `provider` — string **(required)** — Provider key the connection authenticates against, e.g. "salesforce". A remote MCP server is created as `mcp`, with its URL in `connectionConfig.mcp_server_url`. The connection is filed under `mcp_` plus a digest of the server's canonical URL, which is the key every later operation uses: one key for every spelling of one server, and a key that keeps a URL carrying an access key out of request paths and audit rows. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
    - `name` — string — Admin-given name, unique per company. Set for SHARED connections; absent for USER connections, which are identified by provider + `actor`. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
    - `description` — string _(minLen=1; maxLen=1024)_
    - `status` — string **(required)** — Lifecycle state of a connection. For a SHARED connection it is the company credential's state; for a USER connection it is that user's authorization state (PENDING until the user authorizes). _(enum: `pending`, `active`, `expired`, `error`)_
    - `scopes` — array — OAuth scopes requested for the connection.
      - _array of_ `string`
    - `connectionConfig` — ConnectionConfig — Provider parameters the authorization flow itself needs, e.g. `{"hostname": "eu.app.clio.com"}`. A provider may template its OAuth endpoints on these — Clio's authorization and token URLs are both `https://${connectionConfig.hostname}/…` — so for those providers a connection simply cannot be authorized without one. Which fields a provider declares, and their allowed values, are published on the connector definition as `authorization.connectionConfiguration`. Configuration, never credentials. The keys a provider's broker reserves for swapping the OAuth application itself are refused rather than forwarded.
      - _map of_ `string`
    - `actor` — ConnectionActor — The end user who owns a USER connection. A display snapshot only; never used to resolve the credential (that is keyed by provider + user).
      - `id` — string **(required)** — Wildix user id of the owning end user. _(minLen=12; maxLen=12)_
      - `name` — string — Display name at the time the connection was recorded.
      - `email` — string — Email of the owning user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `extension` — string — PBX extension of the owning user.
    - `serverUrl` — string — The remote MCP server this connection is for, as `connectionConfig.mcp_server_url` named it. Present only for an `mcp_*` provider. Read-only: the provider key is a digest of it, so it is what a person reads in place of that key. _(minLen=1; maxLen=2048)_
    - `lastUsedAt` — string — When a runtime last minted a token from this connection, to the minute. Absent means never. Written on the resolve path rather than by a management edit, so it moves independently of the audit fields — reading a credential is not changing it.
- Errors: `400`, `404`, `409`

#### `POST` `/v2/secrets/connections/{connectionId}/sessions`

Starts an interactive authorization session for a SHARED connection, returning a session token
the frontend uses to complete OAuth or collect an API key / basic credential. Per-user
authorization uses CreateUserConnectSession.

- operationId: `CreateConnectSession`
- **Scopes**: `wilma-secrets:CreateConnectSession`
- **Parameters**
  - `connectionId` (path) — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 201** (`CreateConnectSessionResponseContent`)
  - `session` — ConnectSession **(required)** — Session handshake for interactive (OAuth) authorization, completed by the frontend through Nango. A catalogue provider's session is run by handing `sessionToken` to Nango's Connect UI. An MCP server's (`mcp_*` provider) also carries `authorizationUrl`, which the frontend opens in a popup before polling the connection: nothing reports the outcome back, so the connection is adopted on its next read and there is nothing to confirm.
    - `sessionToken` — string **(required)** — Session token the frontend uses to run the authorization flow.
    - `expiresAt` — string — Absolute expiry of the session.
    - `authorizationUrl` — string — The Nango URL that starts an MCP server's authorization. Present only for an `mcp_*` provider.
- Errors: `400`, `404`, `409`

#### `POST` `/v2/secrets/connections/{connectionId}/token`

Resolves a short-lived access token for a SHARED connection at execution time; refresh is
handled transparently. Restricted to service tokens; every call is metered and audited.
For a USER connection, use GetUserConnectionToken.

- operationId: `GetConnectionToken`
- **Scopes**: `wilma-secrets:GetConnectionToken`
- **Parameters**
  - `connectionId` (path) — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetConnectionTokenResponseContent`)
  - `token` — ConnectionToken **(required)** — A short-lived credential resolved for injection at execution time. Contains no refresh token or client secret. _(format=password)_
    - `accessToken` — string **(required)** — Access token to inject into the outbound call or sandbox.
    - `tokenType` — string — Token type, e.g. "Bearer".
    - `expiresAt` — string — Absolute expiry; callers must not cache past this instant.
  - `connectionConfig` — ConnectionConfig — Provider parameters the authorization flow itself needs, e.g. `{"hostname": "eu.app.clio.com"}`. A provider may template its OAuth endpoints on these — Clio's authorization and token URLs are both `https://${connectionConfig.hostname}/…` — so for those providers a connection simply cannot be authorized without one. Which fields a provider declares, and their allowed values, are published on the connector definition as `authorization.connectionConfiguration`. Configuration, never credentials. The keys a provider's broker reserves for swapping the OAuth application itself are refused rather than forwarded.
    - _map of_ `string`
- Errors: `400`, `404`, `409`

#### `POST` `/v2/secrets/connections/{connectionId}/verify`

Checks whether a connection's credential actually works, without returning it.

Resolves a token server-side and reports only the outcome, so the write-only rule holds and an
administrator may call this — unlike GetConnectionToken, which is restricted to service tokens
because it hands back the credential itself. Until this existed, a connection's status only
moved when a real tool execution failed, which meant an agent was the thing that discovered a
broken credential.

Has the same side effects on the record as a resolve: a connection whose authorization
completed is adopted and becomes ACTIVE, one Nango no longer holds forgets its pointer and
returns to PENDING, and one whose credential is refused is marked ERROR.

- operationId: `VerifyConnection`
- **Scopes**: `wilma-secrets:VerifyConnection`
- **Parameters**
  - `connectionId` (path) — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`VerifyConnectionResponseContent`)
  - `status` — string **(required)** — Lifecycle state of a connection. For a SHARED connection it is the company credential's state; for a USER connection it is that user's authorization state (PENDING until the user authorizes). _(enum: `pending`, `active`, `expired`, `error`)_
  - `working` — boolean **(required)** — Whether a credential could actually be resolved just now.
  - `reason` — string — Why a verification did not produce a credential. _(enum: `not_authorized`, `revoked`, `unavailable`)_
- Errors: `400`, `404`, `409`

#### `POST` `/v2/secrets/items/values`

Resolves several secrets in one call, for a consumer holding more than one reference.

A sandbox launch is the case this exists for: a snapshot declaring five credential variables
otherwise makes five calls, each with its own round trip, before the sandbox can start. Resolving
them concurrently already removed the latency; this removes the calls.

Every property of GetSecretValue holds here unchanged — service tokens only, one audit record
per secret resolved, nothing cached on the consumer side. A secret that cannot be resolved does
not fail the call: it comes back carrying why, because the alternative is one deleted reference
denying a launch every other credential was ready for.

- operationId: `BatchGetSecretValues`
- **Scopes**: `wilma-secrets:GetSecretValue`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `BatchGetSecretValuesRequestContent`) **(required)**
  - `secretIds` — array **(required)** — Secrets to resolve. Duplicates are resolved once and answered once. _(minItems=1; maxItems=50)_
    - _array of_ `string`
- **Response 200** (`BatchGetSecretValuesResponseContent`)
  - `values` — array **(required)** — One entry per distinct requested id, in the order requested.
    - _array of_ `ResolvedSecret`
      - `secretId` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
      - `value` — string — Absent when `failure` is set. _(format=password; minLen=1; maxLen=65536)_
      - `attributes` — SecretAttributes — Non-secret companion fields, returned on management responses (the sensitive half stays in `value`). An optional `variant` key classifies the secret's shape (e.g. 'auth_basic', 'auth_bearer', 'auth_client_credentials'); the remaining keys are the companions that shape implies (e.g. 'auth_client_credentials' → { clientId, endpointUrl, scope }). Variants are an open convention, not a fixed enum; ListSecrets can filter by `variant`.
        - _map of_ `string`
      - `revision` — number — Revision of the value returned. Absent when `failure` is set. _(min=1)_
      - `failure` — string — Why a secret in a batch did not resolve — the batch equivalent of GetSecretValue's 404 and 409. _(enum: `not_found`, `pending`)_
- Errors: `400`, `404`, `409`

#### `GET` `/v2/secrets/items/{secretId}`

Gets secret metadata. Never returns the value.

- operationId: `GetSecret`
- **Scopes**: `wilma-secrets:GetSecret`, `wilma-secrets:read`
- **Parameters**
  - `secretId` (path) — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetSecretResponseContent`)
  - `secret` — Secret **(required)** — A stored secret. The sensitive value is never included; non-secret attributes are.
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
    - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `name` — string **(required)** — Human- and machine-readable secret name, unique per company. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
    - `description` — string _(minLen=1; maxLen=1024)_
    - `attributes` — SecretAttributes — Non-secret companion fields, returned on management responses (the sensitive half stays in `value`). An optional `variant` key classifies the secret's shape (e.g. 'auth_basic', 'auth_bearer', 'auth_client_credentials'); the remaining keys are the companions that shape implies (e.g. 'auth_client_credentials' → { clientId, endpointUrl, scope }). Variants are an open convention, not a fixed enum; ListSecrets can filter by `variant`.
      - _map of_ `string`
    - `revision` — number **(required)** — Current revision, bumped on every rotation. Informational only. _(min=1)_
    - `status` — string **(required)** — Lifecycle state of a secret. _(enum: `pending`, `active`)_
    - `expiresAt` — string — When the credential behind this secret stops working, if that is known. Absent means unknown, which is the common case — it is recorded by whoever files the secret, not discovered. Informational, and deliberately not enforced: nothing refuses to resolve a secret past this instant, because the platform cannot know the provider agrees and a wrong date would then take down a working integration. It exists so a console can warn before an API key with a known lifetime fails, rather than the platform learning it from a failed agent turn.
    - `lastUsedAt` — string — When a runtime last resolved this credential, to the minute. Absent means never. Written on the resolve path, not by a management edit: reading a credential is not changing it, so this moves independently of the audit fields. Coarsened to the minute because the question it answers is asked in days and weeks, and an agent in a tool loop would otherwise rewrite it on every outbound call. Absent rather than an epoch for a credential nothing has used, because "nothing has ever resolved this" is a different and more actionable fact than "a long time ago" — it is what lets a console say a credential is safe to delete.
- Errors: `400`, `404`, `409`

#### `PUT` `/v2/secrets/items/{secretId}`

Updates secret metadata (name, description). Use RotateSecret to change the value.

- operationId: `UpdateSecret`
- **Scopes**: `wilma-secrets:UpdateSecret`
- **Parameters**
  - `secretId` (path) — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `UpdateSecretRequestContent`) **(required)**
  - `name` — string **(required)** — Human- and machine-readable secret name, unique per company. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
  - `description` — string _(minLen=1; maxLen=1024)_
  - `attributes` — SecretAttributes — Non-secret companion fields, returned on management responses (the sensitive half stays in `value`). An optional `variant` key classifies the secret's shape (e.g. 'auth_basic', 'auth_bearer', 'auth_client_credentials'); the remaining keys are the companions that shape implies (e.g. 'auth_client_credentials' → { clientId, endpointUrl, scope }). Variants are an open convention, not a fixed enum; ListSecrets can filter by `variant`.
    - _map of_ `string`
- **Response 200** (`UpdateSecretResponseContent`)
  - `secret` — Secret **(required)** — A stored secret. The sensitive value is never included; non-secret attributes are.
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
    - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `name` — string **(required)** — Human- and machine-readable secret name, unique per company. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
    - `description` — string _(minLen=1; maxLen=1024)_
    - `attributes` — SecretAttributes — Non-secret companion fields, returned on management responses (the sensitive half stays in `value`). An optional `variant` key classifies the secret's shape (e.g. 'auth_basic', 'auth_bearer', 'auth_client_credentials'); the remaining keys are the companions that shape implies (e.g. 'auth_client_credentials' → { clientId, endpointUrl, scope }). Variants are an open convention, not a fixed enum; ListSecrets can filter by `variant`.
      - _map of_ `string`
    - `revision` — number **(required)** — Current revision, bumped on every rotation. Informational only. _(min=1)_
    - `status` — string **(required)** — Lifecycle state of a secret. _(enum: `pending`, `active`)_
    - `expiresAt` — string — When the credential behind this secret stops working, if that is known. Absent means unknown, which is the common case — it is recorded by whoever files the secret, not discovered. Informational, and deliberately not enforced: nothing refuses to resolve a secret past this instant, because the platform cannot know the provider agrees and a wrong date would then take down a working integration. It exists so a console can warn before an API key with a known lifetime fails, rather than the platform learning it from a failed agent turn.
    - `lastUsedAt` — string — When a runtime last resolved this credential, to the minute. Absent means never. Written on the resolve path, not by a management edit: reading a credential is not changing it, so this moves independently of the audit fields. Coarsened to the minute because the question it answers is asked in days and weeks, and an agent in a tool loop would otherwise rewrite it on every outbound call. Absent rather than an epoch for a credential nothing has used, because "nothing has ever resolved this" is a different and more actionable fact than "a long time ago" — it is what lets a console say a credential is safe to delete.
- Errors: `400`, `404`, `409`

#### `DELETE` `/v2/secrets/items/{secretId}`

Deletes a secret. Usage is not verified: any reference that still points at it fails to
resolve on its next access.

- operationId: `DeleteSecret`
- **Scopes**: `wilma-secrets:DeleteSecret`
- **Parameters**
  - `secretId` (path) — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- Errors: `400`, `404`, `409`

#### `POST` `/v2/secrets/items/{secretId}/rotate`

Rotates the secret to a new value in place and bumps its revision. References always
resolve to the current value; consumers pick up the new value on their next access.

- operationId: `RotateSecret`
- **Scopes**: `wilma-secrets:RotateSecret`
- **Parameters**
  - `secretId` (path) — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `RotateSecretRequestContent`) **(required)**
  - `value` — string **(required)** — Plaintext secret material. Accepted as input and returned only by GetSecretValue, never on management responses. Stored envelope-encrypted. For a structured secret (e.g. variant 'auth_client_credentials') this is the secret half; non-secret companions live in `attributes`. _(format=password; minLen=1; maxLen=65536)_
- **Response 200** (`RotateSecretResponseContent`)
  - `secret` — Secret **(required)** — A stored secret. The sensitive value is never included; non-secret attributes are.
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
    - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `name` — string **(required)** — Human- and machine-readable secret name, unique per company. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
    - `description` — string _(minLen=1; maxLen=1024)_
    - `attributes` — SecretAttributes — Non-secret companion fields, returned on management responses (the sensitive half stays in `value`). An optional `variant` key classifies the secret's shape (e.g. 'auth_basic', 'auth_bearer', 'auth_client_credentials'); the remaining keys are the companions that shape implies (e.g. 'auth_client_credentials' → { clientId, endpointUrl, scope }). Variants are an open convention, not a fixed enum; ListSecrets can filter by `variant`.
      - _map of_ `string`
    - `revision` — number **(required)** — Current revision, bumped on every rotation. Informational only. _(min=1)_
    - `status` — string **(required)** — Lifecycle state of a secret. _(enum: `pending`, `active`)_
    - `expiresAt` — string — When the credential behind this secret stops working, if that is known. Absent means unknown, which is the common case — it is recorded by whoever files the secret, not discovered. Informational, and deliberately not enforced: nothing refuses to resolve a secret past this instant, because the platform cannot know the provider agrees and a wrong date would then take down a working integration. It exists so a console can warn before an API key with a known lifetime fails, rather than the platform learning it from a failed agent turn.
    - `lastUsedAt` — string — When a runtime last resolved this credential, to the minute. Absent means never. Written on the resolve path, not by a management edit: reading a credential is not changing it, so this moves independently of the audit fields. Coarsened to the minute because the question it answers is asked in days and weeks, and an agent in a tool loop would otherwise rewrite it on every outbound call. Absent rather than an epoch for a credential nothing has used, because "nothing has ever resolved this" is a different and more actionable fact than "a long time ago" — it is what lets a console say a credential is safe to delete.
- Errors: `400`, `404`, `409`

#### `POST` `/v2/secrets/items/{secretId}/value`

Resolves and returns the current secret value for server-to-server use at execution time.
Restricted to service tokens; every call is metered and audited. Fails with
`NotFoundException` (404) when the secret does not exist, and with `ConflictException`
(409) when the secret is `PENDING` — it exists but no value has been supplied yet.

- operationId: `GetSecretValue`
- **Scopes**: `wilma-secrets:GetSecretValue`
- **Parameters**
  - `secretId` (path) — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetSecretValueResponseContent`)
  - `value` — string **(required)** — Plaintext secret material. Accepted as input and returned only by GetSecretValue, never on management responses. Stored envelope-encrypted. For a structured secret (e.g. variant 'auth_client_credentials') this is the secret half; non-secret companions live in `attributes`. _(format=password; minLen=1; maxLen=65536)_
  - `attributes` — SecretAttributes — Non-secret companion fields, returned on management responses (the sensitive half stays in `value`). An optional `variant` key classifies the secret's shape (e.g. 'auth_basic', 'auth_bearer', 'auth_client_credentials'); the remaining keys are the companions that shape implies (e.g. 'auth_client_credentials' → { clientId, endpointUrl, scope }). Variants are an open convention, not a fixed enum; ListSecrets can filter by `variant`.
    - _map of_ `string`
  - `revision` — number **(required)** — Revision of the value returned. Informational. _(min=1)_
- Errors: `400`, `404`, `409`

#### `POST` `/v2/secrets/user-connections/{provider}/confirm`

Completes per-user authorization by recording the connection id returned by the authorization
flow. The service validates it against the provider and user, maps (provider, user) →
connection, and marks the USER connection ACTIVE.

- operationId: `ConfirmUserConnection`
- **Scopes**: `wilma-secrets:ConfirmUserConnection`
- **Parameters**
  - `provider` (path) — string **(required)** — Provider key the connection authenticates against, e.g. "salesforce". A remote MCP server is created as `mcp`, with its URL in `connectionConfig.mcp_server_url`. The connection is filed under `mcp_` plus a digest of the server's canonical URL, which is the key every later operation uses: one key for every spelling of one server, and a key that keeps a URL carrying an access key out of request paths and audit rows. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — Subject user. Defaults to the caller for an xbs token; required for a service token. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `ConfirmUserConnectionRequestContent`) **(required)**
  - `connectionId` — string **(required)** — Connection id returned by the authorization flow. _(minLen=1; maxLen=256)_
- **Response 200** (`ConfirmUserConnectionResponseContent`)
  - `connection` — Connection **(required)** — A configured connection: a company-wide SHARED credential, or a per-user USER credential. Holds registry and ownership metadata only, never the credential itself. `type` is the kind; `actor` is the owning user for USER connections.
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
    - `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `type` — string **(required)** — Who a connection's credential belongs to. _(enum: `shared`, `user`)_
    - `provider` — string **(required)** — Provider key the connection authenticates against, e.g. "salesforce". A remote MCP server is created as `mcp`, with its URL in `connectionConfig.mcp_server_url`. The connection is filed under `mcp_` plus a digest of the server's canonical URL, which is the key every later operation uses: one key for every spelling of one server, and a key that keeps a URL carrying an access key out of request paths and audit rows. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
    - `name` — string — Admin-given name, unique per company. Set for SHARED connections; absent for USER connections, which are identified by provider + `actor`. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
    - `description` — string _(minLen=1; maxLen=1024)_
    - `status` — string **(required)** — Lifecycle state of a connection. For a SHARED connection it is the company credential's state; for a USER connection it is that user's authorization state (PENDING until the user authorizes). _(enum: `pending`, `active`, `expired`, `error`)_
    - `scopes` — array — OAuth scopes requested for the connection.
      - _array of_ `string`
    - `connectionConfig` — ConnectionConfig — Provider parameters the authorization flow itself needs, e.g. `{"hostname": "eu.app.clio.com"}`. A provider may template its OAuth endpoints on these — Clio's authorization and token URLs are both `https://${connectionConfig.hostname}/…` — so for those providers a connection simply cannot be authorized without one. Which fields a provider declares, and their allowed values, are published on the connector definition as `authorization.connectionConfiguration`. Configuration, never credentials. The keys a provider's broker reserves for swapping the OAuth application itself are refused rather than forwarded.
      - _map of_ `string`
    - `actor` — ConnectionActor — The end user who owns a USER connection. A display snapshot only; never used to resolve the credential (that is keyed by provider + user).
      - `id` — string **(required)** — Wildix user id of the owning end user. _(minLen=12; maxLen=12)_
      - `name` — string — Display name at the time the connection was recorded.
      - `email` — string — Email of the owning user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `extension` — string — PBX extension of the owning user.
    - `serverUrl` — string — The remote MCP server this connection is for, as `connectionConfig.mcp_server_url` named it. Present only for an `mcp_*` provider. Read-only: the provider key is a digest of it, so it is what a person reads in place of that key. _(minLen=1; maxLen=2048)_
    - `lastUsedAt` — string — When a runtime last minted a token from this connection, to the minute. Absent means never. Written on the resolve path rather than by a management edit, so it moves independently of the audit fields — reading a credential is not changing it.
- Errors: `400`, `404`, `409`

#### `POST` `/v2/secrets/user-connections/{provider}/sessions`

Starts an interactive authorization session for the calling user against a provider, returning
a session token the frontend uses to run the authorization flow. On success the frontend
reports the resulting connection id back via ConfirmUserConnection.

- operationId: `CreateUserConnectSession`
- **Scopes**: `wilma-secrets:CreateUserConnectSession`
- **Parameters**
  - `provider` (path) — string **(required)** — Provider key the connection authenticates against, e.g. "salesforce". A remote MCP server is created as `mcp`, with its URL in `connectionConfig.mcp_server_url`. The connection is filed under `mcp_` plus a digest of the server's canonical URL, which is the key every later operation uses: one key for every spelling of one server, and a key that keeps a URL carrying an access key out of request paths and audit rows. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — Subject user. Defaults to the caller for an xbs token; required for a service token. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `CreateUserConnectSessionRequestContent`)
  - `connectionConfig` — ConnectionConfig — Provider parameters the authorization flow itself needs, e.g. `{"hostname": "eu.app.clio.com"}`. A provider may template its OAuth endpoints on these — Clio's authorization and token URLs are both `https://${connectionConfig.hostname}/…` — so for those providers a connection simply cannot be authorized without one. Which fields a provider declares, and their allowed values, are published on the connector definition as `authorization.connectionConfiguration`. Configuration, never credentials. The keys a provider's broker reserves for swapping the OAuth application itself are refused rather than forwarded.
    - _map of_ `string`
- **Response 201** (`CreateUserConnectSessionResponseContent`)
  - `session` — ConnectSession **(required)** — Session handshake for interactive (OAuth) authorization, completed by the frontend through Nango. A catalogue provider's session is run by handing `sessionToken` to Nango's Connect UI. An MCP server's (`mcp_*` provider) also carries `authorizationUrl`, which the frontend opens in a popup before polling the connection: nothing reports the outcome back, so the connection is adopted on its next read and there is nothing to confirm.
    - `sessionToken` — string **(required)** — Session token the frontend uses to run the authorization flow.
    - `expiresAt` — string — Absolute expiry of the session.
    - `authorizationUrl` — string — The Nango URL that starts an MCP server's authorization. Present only for an `mcp_*` provider.
- Errors: `400`, `404`, `409`

#### `POST` `/v2/secrets/user-connections/{provider}/token`

Resolves a short-lived access token for a user's provider authorization at execution time;
refresh is handled transparently. Restricted to service tokens; every call is metered and
audited. Fails with ConflictException when the user has not connected the provider yet.

- operationId: `GetUserConnectionToken`
- **Scopes**: `wilma-secrets:GetUserConnectionToken`
- **Parameters**
  - `provider` (path) — string **(required)** — Provider key the connection authenticates against, e.g. "salesforce". A remote MCP server is created as `mcp`, with its URL in `connectionConfig.mcp_server_url`. The connection is filed under `mcp_` plus a digest of the server's canonical URL, which is the key every later operation uses: one key for every spelling of one server, and a key that keeps a URL carrying an access key out of request paths and audit rows. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string **(required)** — Executing end user whose credential is resolved. _(minLen=12; maxLen=12)_
- **Response 200** (`GetUserConnectionTokenResponseContent`)
  - `token` — ConnectionToken **(required)** — A short-lived credential resolved for injection at execution time. Contains no refresh token or client secret. _(format=password)_
    - `accessToken` — string **(required)** — Access token to inject into the outbound call or sandbox.
    - `tokenType` — string — Token type, e.g. "Bearer".
    - `expiresAt` — string — Absolute expiry; callers must not cache past this instant.
  - `connectionConfig` — ConnectionConfig — Provider parameters the authorization flow itself needs, e.g. `{"hostname": "eu.app.clio.com"}`. A provider may template its OAuth endpoints on these — Clio's authorization and token URLs are both `https://${connectionConfig.hostname}/…` — so for those providers a connection simply cannot be authorized without one. Which fields a provider declares, and their allowed values, are published on the connector definition as `authorization.connectionConfiguration`. Configuration, never credentials. The keys a provider's broker reserves for swapping the OAuth application itself are refused rather than forwarded.
    - _map of_ `string`
- Errors: `400`, `404`, `409`

### Schemas appendix — Wilma Secrets API (Credential Broker)

<details><summary>45 component schemas</summary>

**`Actor`**

_Who performed an action: an interactive user, an API key or an internal service._

- `type` — string **(required)** _(enum: `user`, `api_key`, `service`)_
- `id` — string **(required)** — User id, API key id or service name, depending on the actor type.
- `name` — string — Human readable name of the actor at the time of the action.

**`ActorType`**

- string _(enum: `user`, `api_key`, `service`)_

**`BatchGetSecretValuesRequestContent`**

- `secretIds` — array **(required)** — Secrets to resolve. Duplicates are resolved once and answered once. _(minItems=1; maxItems=50)_
  - _array of_ `string`

**`BatchGetSecretValuesResponseContent`**

- `values` — array **(required)** — One entry per distinct requested id, in the order requested.
  - _array of_ `ResolvedSecret`
    - `secretId` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
    - `value` — string — Absent when `failure` is set. _(format=password; minLen=1; maxLen=65536)_
    - `attributes` — SecretAttributes — Non-secret companion fields, returned on management responses (the sensitive half stays in `value`). An optional `variant` key classifies the secret's shape (e.g. 'auth_basic', 'auth_bearer', 'auth_client_credentials'); the remaining keys are the companions that shape implies (e.g. 'auth_client_credentials' → { clientId, endpointUrl, scope }). Variants are an open convention, not a fixed enum; ListSecrets can filter by `variant`.
      - _map of_ `string`
    - `revision` — number — Revision of the value returned. Absent when `failure` is set. _(min=1)_
    - `failure` — string — Why a secret in a batch did not resolve — the batch equivalent of GetSecretValue's 404 and 409. _(enum: `not_found`, `pending`)_

**`ConfirmConnectionRequestContent`**

- `externalConnectionId` — string **(required)** — Connection id returned by the authorization flow. Verified against the provider and the end user the connect session named before it is stored. _(minLen=1; maxLen=256)_

**`ConfirmConnectionResponseContent`**

- `connection` — Connection **(required)** — A configured connection: a company-wide SHARED credential, or a per-user USER credential. Holds registry and ownership metadata only, never the credential itself. `type` is the kind; `actor` is the owning user for USER connections.
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
  - `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `type` — string **(required)** — Who a connection's credential belongs to. _(enum: `shared`, `user`)_
  - `provider` — string **(required)** — Provider key the connection authenticates against, e.g. "salesforce". A remote MCP server is created as `mcp`, with its URL in `connectionConfig.mcp_server_url`. The connection is filed under `mcp_` plus a digest of the server's canonical URL, which is the key every later operation uses: one key for every spelling of one server, and a key that keeps a URL carrying an access key out of request paths and audit rows. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
  - `name` — string — Admin-given name, unique per company. Set for SHARED connections; absent for USER connections, which are identified by provider + `actor`. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
  - `description` — string _(minLen=1; maxLen=1024)_
  - `status` — string **(required)** — Lifecycle state of a connection. For a SHARED connection it is the company credential's state; for a USER connection it is that user's authorization state (PENDING until the user authorizes). _(enum: `pending`, `active`, `expired`, `error`)_
  - `scopes` — array — OAuth scopes requested for the connection.
    - _array of_ `string`
  - `connectionConfig` — ConnectionConfig — Provider parameters the authorization flow itself needs, e.g. `{"hostname": "eu.app.clio.com"}`. A provider may template its OAuth endpoints on these — Clio's authorization and token URLs are both `https://${connectionConfig.hostname}/…` — so for those providers a connection simply cannot be authorized without one. Which fields a provider declares, and their allowed values, are published on the connector definition as `authorization.connectionConfiguration`. Configuration, never credentials. The keys a provider's broker reserves for swapping the OAuth application itself are refused rather than forwarded.
    - _map of_ `string`
  - `actor` — ConnectionActor — The end user who owns a USER connection. A display snapshot only; never used to resolve the credential (that is keyed by provider + user).
    - `id` — string **(required)** — Wildix user id of the owning end user. _(minLen=12; maxLen=12)_
    - `name` — string — Display name at the time the connection was recorded.
    - `email` — string — Email of the owning user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `extension` — string — PBX extension of the owning user.
  - `serverUrl` — string — The remote MCP server this connection is for, as `connectionConfig.mcp_server_url` named it. Present only for an `mcp_*` provider. Read-only: the provider key is a digest of it, so it is what a person reads in place of that key. _(minLen=1; maxLen=2048)_
  - `lastUsedAt` — string — When a runtime last minted a token from this connection, to the minute. Absent means never. Written on the resolve path rather than by a management edit, so it moves independently of the audit fields — reading a credential is not changing it.

**`ConfirmUserConnectionRequestContent`**

- `connectionId` — string **(required)** — Connection id returned by the authorization flow. _(minLen=1; maxLen=256)_

**`ConfirmUserConnectionResponseContent`**

- `connection` — Connection **(required)** — A configured connection: a company-wide SHARED credential, or a per-user USER credential. Holds registry and ownership metadata only, never the credential itself. `type` is the kind; `actor` is the owning user for USER connections.
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
  - `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `type` — string **(required)** — Who a connection's credential belongs to. _(enum: `shared`, `user`)_
  - `provider` — string **(required)** — Provider key the connection authenticates against, e.g. "salesforce". A remote MCP server is created as `mcp`, with its URL in `connectionConfig.mcp_server_url`. The connection is filed under `mcp_` plus a digest of the server's canonical URL, which is the key every later operation uses: one key for every spelling of one server, and a key that keeps a URL carrying an access key out of request paths and audit rows. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
  - `name` — string — Admin-given name, unique per company. Set for SHARED connections; absent for USER connections, which are identified by provider + `actor`. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
  - `description` — string _(minLen=1; maxLen=1024)_
  - `status` — string **(required)** — Lifecycle state of a connection. For a SHARED connection it is the company credential's state; for a USER connection it is that user's authorization state (PENDING until the user authorizes). _(enum: `pending`, `active`, `expired`, `error`)_
  - `scopes` — array — OAuth scopes requested for the connection.
    - _array of_ `string`
  - `connectionConfig` — ConnectionConfig — Provider parameters the authorization flow itself needs, e.g. `{"hostname": "eu.app.clio.com"}`. A provider may template its OAuth endpoints on these — Clio's authorization and token URLs are both `https://${connectionConfig.hostname}/…` — so for those providers a connection simply cannot be authorized without one. Which fields a provider declares, and their allowed values, are published on the connector definition as `authorization.connectionConfiguration`. Configuration, never credentials. The keys a provider's broker reserves for swapping the OAuth application itself are refused rather than forwarded.
    - _map of_ `string`
  - `actor` — ConnectionActor — The end user who owns a USER connection. A display snapshot only; never used to resolve the credential (that is keyed by provider + user).
    - `id` — string **(required)** — Wildix user id of the owning end user. _(minLen=12; maxLen=12)_
    - `name` — string — Display name at the time the connection was recorded.
    - `email` — string — Email of the owning user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `extension` — string — PBX extension of the owning user.
  - `serverUrl` — string — The remote MCP server this connection is for, as `connectionConfig.mcp_server_url` named it. Present only for an `mcp_*` provider. Read-only: the provider key is a digest of it, so it is what a person reads in place of that key. _(minLen=1; maxLen=2048)_
  - `lastUsedAt` — string — When a runtime last minted a token from this connection, to the minute. Absent means never. Written on the resolve path rather than by a management edit, so it moves independently of the audit fields — reading a credential is not changing it.

**`ConflictExceptionResponseContent`**

_The request conflicts with the current state of the resource, e.g. a duplicate name, a resource still in use, or an unmet precondition._

- `message` — string **(required)**

**`ConnectSession`**

_Session handshake for interactive (OAuth) authorization, completed by the frontend through Nango. A catalogue provider's session is run by handing `sessionToken` to Nango's Connect UI. An MCP server's (`mcp_*` provider) also carries `authorizationUrl`, which the frontend opens in a popup before polling the connection: nothing reports the outcome back, so the connection is adopted on its next read and there is nothing to confirm._

- `sessionToken` — string **(required)** — Session token the frontend uses to run the authorization flow.
- `expiresAt` — string — Absolute expiry of the session.
- `authorizationUrl` — string — The Nango URL that starts an MCP server's authorization. Present only for an `mcp_*` provider.

**`Connection`**

_A configured connection: a company-wide SHARED credential, or a per-user USER credential. Holds registry and ownership metadata only, never the credential itself. `type` is the kind; `actor` is the owning user for USER connections._

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
- `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
- `companyId` — string **(required)** _(minLen=3; maxLen=30)_
- `type` — string **(required)** — Who a connection's credential belongs to. _(enum: `shared`, `user`)_
- `provider` — string **(required)** — Provider key the connection authenticates against, e.g. "salesforce". A remote MCP server is created as `mcp`, with its URL in `connectionConfig.mcp_server_url`. The connection is filed under `mcp_` plus a digest of the server's canonical URL, which is the key every later operation uses: one key for every spelling of one server, and a key that keeps a URL carrying an access key out of request paths and audit rows. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
- `name` — string — Admin-given name, unique per company. Set for SHARED connections; absent for USER connections, which are identified by provider + `actor`. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
- `description` — string _(minLen=1; maxLen=1024)_
- `status` — string **(required)** — Lifecycle state of a connection. For a SHARED connection it is the company credential's state; for a USER connection it is that user's authorization state (PENDING until the user authorizes). _(enum: `pending`, `active`, `expired`, `error`)_
- `scopes` — array — OAuth scopes requested for the connection.
  - _array of_ `string`
- `connectionConfig` — ConnectionConfig — Provider parameters the authorization flow itself needs, e.g. `{"hostname": "eu.app.clio.com"}`. A provider may template its OAuth endpoints on these — Clio's authorization and token URLs are both `https://${connectionConfig.hostname}/…` — so for those providers a connection simply cannot be authorized without one. Which fields a provider declares, and their allowed values, are published on the connector definition as `authorization.connectionConfiguration`. Configuration, never credentials. The keys a provider's broker reserves for swapping the OAuth application itself are refused rather than forwarded.
  - _map of_ `string`
- `actor` — ConnectionActor — The end user who owns a USER connection. A display snapshot only; never used to resolve the credential (that is keyed by provider + user).
  - `id` — string **(required)** — Wildix user id of the owning end user. _(minLen=12; maxLen=12)_
  - `name` — string — Display name at the time the connection was recorded.
  - `email` — string — Email of the owning user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
  - `extension` — string — PBX extension of the owning user.
- `serverUrl` — string — The remote MCP server this connection is for, as `connectionConfig.mcp_server_url` named it. Present only for an `mcp_*` provider. Read-only: the provider key is a digest of it, so it is what a person reads in place of that key. _(minLen=1; maxLen=2048)_
- `lastUsedAt` — string — When a runtime last minted a token from this connection, to the minute. Absent means never. Written on the resolve path rather than by a management edit, so it moves independently of the audit fields — reading a credential is not changing it.

**`ConnectionActor`**

_The end user who owns a USER connection. A display snapshot only; never used to resolve the credential (that is keyed by provider + user)._

- `id` — string **(required)** — Wildix user id of the owning end user. _(minLen=12; maxLen=12)_
- `name` — string — Display name at the time the connection was recorded.
- `email` — string — Email of the owning user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
- `extension` — string — PBX extension of the owning user.

**`ConnectionConfig`**

_Provider parameters the authorization flow itself needs, e.g. `{"hostname": "eu.app.clio.com"}`. A provider may template its OAuth endpoints on these — Clio's authorization and token URLs are both `https://${connectionConfig.hostname}/…` — so for those providers a connection simply cannot be authorized without one. Which fields a provider declares, and their allowed values, are published on the connector definition as `authorization.connectionConfiguration`. Configuration, never credentials. The keys a provider's broker reserves for swapping the OAuth application itself are refused rather than forwarded._

- _map of_ `string`

**`ConnectionStatus`**

_Lifecycle state of a connection. For a SHARED connection it is the company credential's state; for a USER connection it is that user's authorization state (PENDING until the user authorizes)._

- string _(enum: `pending`, `active`, `expired`, `error`)_

**`ConnectionToken`**

_A short-lived credential resolved for injection at execution time. Contains no refresh token or client secret._

- `accessToken` — string **(required)** — Access token to inject into the outbound call or sandbox.
- `tokenType` — string — Token type, e.g. "Bearer".
- `expiresAt` — string — Absolute expiry; callers must not cache past this instant.

**`ConnectionType`**

_Who a connection's credential belongs to._

- string _(enum: `shared`, `user`)_

**`CreateConnectSessionResponseContent`**

- `session` — ConnectSession **(required)** — Session handshake for interactive (OAuth) authorization, completed by the frontend through Nango. A catalogue provider's session is run by handing `sessionToken` to Nango's Connect UI. An MCP server's (`mcp_*` provider) also carries `authorizationUrl`, which the frontend opens in a popup before polling the connection: nothing reports the outcome back, so the connection is adopted on its next read and there is nothing to confirm.
  - `sessionToken` — string **(required)** — Session token the frontend uses to run the authorization flow.
  - `expiresAt` — string — Absolute expiry of the session.
  - `authorizationUrl` — string — The Nango URL that starts an MCP server's authorization. Present only for an `mcp_*` provider.

**`CreateConnectionRequestContent`**

- `name` — string **(required)** — Connection name, unique per company. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
- `description` — string _(minLen=1; maxLen=1024)_
- `provider` — string **(required)** — Provider key the connection authenticates against, e.g. "salesforce". A remote MCP server is created as `mcp`, with its URL in `connectionConfig.mcp_server_url`. The connection is filed under `mcp_` plus a digest of the server's canonical URL, which is the key every later operation uses: one key for every spelling of one server, and a key that keeps a URL carrying an access key out of request paths and audit rows. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
- `scopes` — array — OAuth scopes requested for the connection.
  - _array of_ `string`
- `connectionConfig` — ConnectionConfig — Provider parameters the authorization flow itself needs, e.g. `{"hostname": "eu.app.clio.com"}`. A provider may template its OAuth endpoints on these — Clio's authorization and token URLs are both `https://${connectionConfig.hostname}/…` — so for those providers a connection simply cannot be authorized without one. Which fields a provider declares, and their allowed values, are published on the connector definition as `authorization.connectionConfiguration`. Configuration, never credentials. The keys a provider's broker reserves for swapping the OAuth application itself are refused rather than forwarded.
  - _map of_ `string`

**`CreateConnectionResponseContent`**

- `connection` — Connection **(required)** — A configured connection: a company-wide SHARED credential, or a per-user USER credential. Holds registry and ownership metadata only, never the credential itself. `type` is the kind; `actor` is the owning user for USER connections.
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
  - `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `type` — string **(required)** — Who a connection's credential belongs to. _(enum: `shared`, `user`)_
  - `provider` — string **(required)** — Provider key the connection authenticates against, e.g. "salesforce". A remote MCP server is created as `mcp`, with its URL in `connectionConfig.mcp_server_url`. The connection is filed under `mcp_` plus a digest of the server's canonical URL, which is the key every later operation uses: one key for every spelling of one server, and a key that keeps a URL carrying an access key out of request paths and audit rows. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
  - `name` — string — Admin-given name, unique per company. Set for SHARED connections; absent for USER connections, which are identified by provider + `actor`. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
  - `description` — string _(minLen=1; maxLen=1024)_
  - `status` — string **(required)** — Lifecycle state of a connection. For a SHARED connection it is the company credential's state; for a USER connection it is that user's authorization state (PENDING until the user authorizes). _(enum: `pending`, `active`, `expired`, `error`)_
  - `scopes` — array — OAuth scopes requested for the connection.
    - _array of_ `string`
  - `connectionConfig` — ConnectionConfig — Provider parameters the authorization flow itself needs, e.g. `{"hostname": "eu.app.clio.com"}`. A provider may template its OAuth endpoints on these — Clio's authorization and token URLs are both `https://${connectionConfig.hostname}/…` — so for those providers a connection simply cannot be authorized without one. Which fields a provider declares, and their allowed values, are published on the connector definition as `authorization.connectionConfiguration`. Configuration, never credentials. The keys a provider's broker reserves for swapping the OAuth application itself are refused rather than forwarded.
    - _map of_ `string`
  - `actor` — ConnectionActor — The end user who owns a USER connection. A display snapshot only; never used to resolve the credential (that is keyed by provider + user).
    - `id` — string **(required)** — Wildix user id of the owning end user. _(minLen=12; maxLen=12)_
    - `name` — string — Display name at the time the connection was recorded.
    - `email` — string — Email of the owning user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `extension` — string — PBX extension of the owning user.
  - `serverUrl` — string — The remote MCP server this connection is for, as `connectionConfig.mcp_server_url` named it. Present only for an `mcp_*` provider. Read-only: the provider key is a digest of it, so it is what a person reads in place of that key. _(minLen=1; maxLen=2048)_
  - `lastUsedAt` — string — When a runtime last minted a token from this connection, to the minute. Absent means never. Written on the resolve path rather than by a management edit, so it moves independently of the audit fields — reading a credential is not changing it.

**`CreateSecretRequestContent`**

- `name` — string **(required)** — Human- and machine-readable secret name, unique per company. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
- `description` — string _(minLen=1; maxLen=1024)_
- `value` — string — Secret material. Write-only; stored envelope-encrypted. Omit to create the secret without one: it stays `PENDING` until `RotateSecret` supplies a value. _(format=password; minLen=1; maxLen=65536)_
- `attributes` — SecretAttributes — Non-secret companion fields, returned on management responses (the sensitive half stays in `value`). An optional `variant` key classifies the secret's shape (e.g. 'auth_basic', 'auth_bearer', 'auth_client_credentials'); the remaining keys are the companions that shape implies (e.g. 'auth_client_credentials' → { clientId, endpointUrl, scope }). Variants are an open convention, not a fixed enum; ListSecrets can filter by `variant`.
  - _map of_ `string`

**`CreateSecretResponseContent`**

- `secret` — Secret **(required)** — A stored secret. The sensitive value is never included; non-secret attributes are.
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
  - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `name` — string **(required)** — Human- and machine-readable secret name, unique per company. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
  - `description` — string _(minLen=1; maxLen=1024)_
  - `attributes` — SecretAttributes — Non-secret companion fields, returned on management responses (the sensitive half stays in `value`). An optional `variant` key classifies the secret's shape (e.g. 'auth_basic', 'auth_bearer', 'auth_client_credentials'); the remaining keys are the companions that shape implies (e.g. 'auth_client_credentials' → { clientId, endpointUrl, scope }). Variants are an open convention, not a fixed enum; ListSecrets can filter by `variant`.
    - _map of_ `string`
  - `revision` — number **(required)** — Current revision, bumped on every rotation. Informational only. _(min=1)_
  - `status` — string **(required)** — Lifecycle state of a secret. _(enum: `pending`, `active`)_
  - `expiresAt` — string — When the credential behind this secret stops working, if that is known. Absent means unknown, which is the common case — it is recorded by whoever files the secret, not discovered. Informational, and deliberately not enforced: nothing refuses to resolve a secret past this instant, because the platform cannot know the provider agrees and a wrong date would then take down a working integration. It exists so a console can warn before an API key with a known lifetime fails, rather than the platform learning it from a failed agent turn.
  - `lastUsedAt` — string — When a runtime last resolved this credential, to the minute. Absent means never. Written on the resolve path, not by a management edit: reading a credential is not changing it, so this moves independently of the audit fields. Coarsened to the minute because the question it answers is asked in days and weeks, and an agent in a tool loop would otherwise rewrite it on every outbound call. Absent rather than an epoch for a credential nothing has used, because "nothing has ever resolved this" is a different and more actionable fact than "a long time ago" — it is what lets a console say a credential is safe to delete.

**`CreateUserConnectSessionRequestContent`**

- `connectionConfig` — ConnectionConfig — Provider parameters the authorization flow itself needs, e.g. `{"hostname": "eu.app.clio.com"}`. A provider may template its OAuth endpoints on these — Clio's authorization and token URLs are both `https://${connectionConfig.hostname}/…` — so for those providers a connection simply cannot be authorized without one. Which fields a provider declares, and their allowed values, are published on the connector definition as `authorization.connectionConfiguration`. Configuration, never credentials. The keys a provider's broker reserves for swapping the OAuth application itself are refused rather than forwarded.
  - _map of_ `string`

**`CreateUserConnectSessionResponseContent`**

- `session` — ConnectSession **(required)** — Session handshake for interactive (OAuth) authorization, completed by the frontend through Nango. A catalogue provider's session is run by handing `sessionToken` to Nango's Connect UI. An MCP server's (`mcp_*` provider) also carries `authorizationUrl`, which the frontend opens in a popup before polling the connection: nothing reports the outcome back, so the connection is adopted on its next read and there is nothing to confirm.
  - `sessionToken` — string **(required)** — Session token the frontend uses to run the authorization flow.
  - `expiresAt` — string — Absolute expiry of the session.
  - `authorizationUrl` — string — The Nango URL that starts an MCP server's authorization. Present only for an `mcp_*` provider.

**`GetConnectionResponseContent`**

- `connection` — Connection **(required)** — A configured connection: a company-wide SHARED credential, or a per-user USER credential. Holds registry and ownership metadata only, never the credential itself. `type` is the kind; `actor` is the owning user for USER connections.
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
  - `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `type` — string **(required)** — Who a connection's credential belongs to. _(enum: `shared`, `user`)_
  - `provider` — string **(required)** — Provider key the connection authenticates against, e.g. "salesforce". A remote MCP server is created as `mcp`, with its URL in `connectionConfig.mcp_server_url`. The connection is filed under `mcp_` plus a digest of the server's canonical URL, which is the key every later operation uses: one key for every spelling of one server, and a key that keeps a URL carrying an access key out of request paths and audit rows. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
  - `name` — string — Admin-given name, unique per company. Set for SHARED connections; absent for USER connections, which are identified by provider + `actor`. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
  - `description` — string _(minLen=1; maxLen=1024)_
  - `status` — string **(required)** — Lifecycle state of a connection. For a SHARED connection it is the company credential's state; for a USER connection it is that user's authorization state (PENDING until the user authorizes). _(enum: `pending`, `active`, `expired`, `error`)_
  - `scopes` — array — OAuth scopes requested for the connection.
    - _array of_ `string`
  - `connectionConfig` — ConnectionConfig — Provider parameters the authorization flow itself needs, e.g. `{"hostname": "eu.app.clio.com"}`. A provider may template its OAuth endpoints on these — Clio's authorization and token URLs are both `https://${connectionConfig.hostname}/…` — so for those providers a connection simply cannot be authorized without one. Which fields a provider declares, and their allowed values, are published on the connector definition as `authorization.connectionConfiguration`. Configuration, never credentials. The keys a provider's broker reserves for swapping the OAuth application itself are refused rather than forwarded.
    - _map of_ `string`
  - `actor` — ConnectionActor — The end user who owns a USER connection. A display snapshot only; never used to resolve the credential (that is keyed by provider + user).
    - `id` — string **(required)** — Wildix user id of the owning end user. _(minLen=12; maxLen=12)_
    - `name` — string — Display name at the time the connection was recorded.
    - `email` — string — Email of the owning user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `extension` — string — PBX extension of the owning user.
  - `serverUrl` — string — The remote MCP server this connection is for, as `connectionConfig.mcp_server_url` named it. Present only for an `mcp_*` provider. Read-only: the provider key is a digest of it, so it is what a person reads in place of that key. _(minLen=1; maxLen=2048)_
  - `lastUsedAt` — string — When a runtime last minted a token from this connection, to the minute. Absent means never. Written on the resolve path rather than by a management edit, so it moves independently of the audit fields — reading a credential is not changing it.

**`GetConnectionTokenResponseContent`**

- `token` — ConnectionToken **(required)** — A short-lived credential resolved for injection at execution time. Contains no refresh token or client secret. _(format=password)_
  - `accessToken` — string **(required)** — Access token to inject into the outbound call or sandbox.
  - `tokenType` — string — Token type, e.g. "Bearer".
  - `expiresAt` — string — Absolute expiry; callers must not cache past this instant.
- `connectionConfig` — ConnectionConfig — Provider parameters the authorization flow itself needs, e.g. `{"hostname": "eu.app.clio.com"}`. A provider may template its OAuth endpoints on these — Clio's authorization and token URLs are both `https://${connectionConfig.hostname}/…` — so for those providers a connection simply cannot be authorized without one. Which fields a provider declares, and their allowed values, are published on the connector definition as `authorization.connectionConfiguration`. Configuration, never credentials. The keys a provider's broker reserves for swapping the OAuth application itself are refused rather than forwarded.
  - _map of_ `string`

**`GetSecretResponseContent`**

- `secret` — Secret **(required)** — A stored secret. The sensitive value is never included; non-secret attributes are.
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
  - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `name` — string **(required)** — Human- and machine-readable secret name, unique per company. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
  - `description` — string _(minLen=1; maxLen=1024)_
  - `attributes` — SecretAttributes — Non-secret companion fields, returned on management responses (the sensitive half stays in `value`). An optional `variant` key classifies the secret's shape (e.g. 'auth_basic', 'auth_bearer', 'auth_client_credentials'); the remaining keys are the companions that shape implies (e.g. 'auth_client_credentials' → { clientId, endpointUrl, scope }). Variants are an open convention, not a fixed enum; ListSecrets can filter by `variant`.
    - _map of_ `string`
  - `revision` — number **(required)** — Current revision, bumped on every rotation. Informational only. _(min=1)_
  - `status` — string **(required)** — Lifecycle state of a secret. _(enum: `pending`, `active`)_
  - `expiresAt` — string — When the credential behind this secret stops working, if that is known. Absent means unknown, which is the common case — it is recorded by whoever files the secret, not discovered. Informational, and deliberately not enforced: nothing refuses to resolve a secret past this instant, because the platform cannot know the provider agrees and a wrong date would then take down a working integration. It exists so a console can warn before an API key with a known lifetime fails, rather than the platform learning it from a failed agent turn.
  - `lastUsedAt` — string — When a runtime last resolved this credential, to the minute. Absent means never. Written on the resolve path, not by a management edit: reading a credential is not changing it, so this moves independently of the audit fields. Coarsened to the minute because the question it answers is asked in days and weeks, and an agent in a tool loop would otherwise rewrite it on every outbound call. Absent rather than an epoch for a credential nothing has used, because "nothing has ever resolved this" is a different and more actionable fact than "a long time ago" — it is what lets a console say a credential is safe to delete.

**`GetSecretValueResponseContent`**

- `value` — string **(required)** — Plaintext secret material. Accepted as input and returned only by GetSecretValue, never on management responses. Stored envelope-encrypted. For a structured secret (e.g. variant 'auth_client_credentials') this is the secret half; non-secret companions live in `attributes`. _(format=password; minLen=1; maxLen=65536)_
- `attributes` — SecretAttributes — Non-secret companion fields, returned on management responses (the sensitive half stays in `value`). An optional `variant` key classifies the secret's shape (e.g. 'auth_basic', 'auth_bearer', 'auth_client_credentials'); the remaining keys are the companions that shape implies (e.g. 'auth_client_credentials' → { clientId, endpointUrl, scope }). Variants are an open convention, not a fixed enum; ListSecrets can filter by `variant`.
  - _map of_ `string`
- `revision` — number **(required)** — Revision of the value returned. Informational. _(min=1)_

**`GetUserConnectionTokenResponseContent`**

- `token` — ConnectionToken **(required)** — A short-lived credential resolved for injection at execution time. Contains no refresh token or client secret. _(format=password)_
  - `accessToken` — string **(required)** — Access token to inject into the outbound call or sandbox.
  - `tokenType` — string — Token type, e.g. "Bearer".
  - `expiresAt` — string — Absolute expiry; callers must not cache past this instant.
- `connectionConfig` — ConnectionConfig — Provider parameters the authorization flow itself needs, e.g. `{"hostname": "eu.app.clio.com"}`. A provider may template its OAuth endpoints on these — Clio's authorization and token URLs are both `https://${connectionConfig.hostname}/…` — so for those providers a connection simply cannot be authorized without one. Which fields a provider declares, and their allowed values, are published on the connector definition as `authorization.connectionConfiguration`. Configuration, never credentials. The keys a provider's broker reserves for swapping the OAuth application itself are refused rather than forwarded.
  - _map of_ `string`

**`ListConnectionsResponseContent`**

- `connections` — array **(required)** — Connections returned by list operations.
  - _array of_ `Connection`
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
    - `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `type` — string **(required)** — Who a connection's credential belongs to. _(enum: `shared`, `user`)_
    - `provider` — string **(required)** — Provider key the connection authenticates against, e.g. "salesforce". A remote MCP server is created as `mcp`, with its URL in `connectionConfig.mcp_server_url`. The connection is filed under `mcp_` plus a digest of the server's canonical URL, which is the key every later operation uses: one key for every spelling of one server, and a key that keeps a URL carrying an access key out of request paths and audit rows. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
    - `name` — string — Admin-given name, unique per company. Set for SHARED connections; absent for USER connections, which are identified by provider + `actor`. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
    - `description` — string _(minLen=1; maxLen=1024)_
    - `status` — string **(required)** — Lifecycle state of a connection. For a SHARED connection it is the company credential's state; for a USER connection it is that user's authorization state (PENDING until the user authorizes). _(enum: `pending`, `active`, `expired`, `error`)_
    - `scopes` — array — OAuth scopes requested for the connection.
      - _array of_ `string`
    - `connectionConfig` — ConnectionConfig — Provider parameters the authorization flow itself needs, e.g. `{"hostname": "eu.app.clio.com"}`. A provider may template its OAuth endpoints on these — Clio's authorization and token URLs are both `https://${connectionConfig.hostname}/…` — so for those providers a connection simply cannot be authorized without one. Which fields a provider declares, and their allowed values, are published on the connector definition as `authorization.connectionConfiguration`. Configuration, never credentials. The keys a provider's broker reserves for swapping the OAuth application itself are refused rather than forwarded.
      - _map of_ `string`
    - `actor` — ConnectionActor — The end user who owns a USER connection. A display snapshot only; never used to resolve the credential (that is keyed by provider + user).
      - `id` — string **(required)** — Wildix user id of the owning end user. _(minLen=12; maxLen=12)_
      - `name` — string — Display name at the time the connection was recorded.
      - `email` — string — Email of the owning user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `extension` — string — PBX extension of the owning user.
    - `serverUrl` — string — The remote MCP server this connection is for, as `connectionConfig.mcp_server_url` named it. Present only for an `mcp_*` provider. Read-only: the provider key is a digest of it, so it is what a person reads in place of that key. _(minLen=1; maxLen=2048)_
    - `lastUsedAt` — string — When a runtime last minted a token from this connection, to the minute. Absent means never. Written on the resolve path rather than by a management edit, so it moves independently of the audit fields — reading a credential is not changing it.
- `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_

**`ListSecretsResponseContent`**

- `secrets` — array **(required)** — Secrets returned by list operations (metadata only).
  - _array of_ `Secret`
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
    - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `name` — string **(required)** — Human- and machine-readable secret name, unique per company. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
    - `description` — string _(minLen=1; maxLen=1024)_
    - `attributes` — SecretAttributes — Non-secret companion fields, returned on management responses (the sensitive half stays in `value`). An optional `variant` key classifies the secret's shape (e.g. 'auth_basic', 'auth_bearer', 'auth_client_credentials'); the remaining keys are the companions that shape implies (e.g. 'auth_client_credentials' → { clientId, endpointUrl, scope }). Variants are an open convention, not a fixed enum; ListSecrets can filter by `variant`.
      - _map of_ `string`
    - `revision` — number **(required)** — Current revision, bumped on every rotation. Informational only. _(min=1)_
    - `status` — string **(required)** — Lifecycle state of a secret. _(enum: `pending`, `active`)_
    - `expiresAt` — string — When the credential behind this secret stops working, if that is known. Absent means unknown, which is the common case — it is recorded by whoever files the secret, not discovered. Informational, and deliberately not enforced: nothing refuses to resolve a secret past this instant, because the platform cannot know the provider agrees and a wrong date would then take down a working integration. It exists so a console can warn before an API key with a known lifetime fails, rather than the platform learning it from a failed agent turn.
    - `lastUsedAt` — string — When a runtime last resolved this credential, to the minute. Absent means never. Written on the resolve path, not by a management edit: reading a credential is not changing it, so this moves independently of the audit fields. Coarsened to the minute because the question it answers is asked in days and weeks, and an agent in a tool loop would otherwise rewrite it on every outbound call. Absent rather than an epoch for a credential nothing has used, because "nothing has ever resolved this" is a different and more actionable fact than "a long time ago" — it is what lets a console say a credential is safe to delete.
- `nextCursor` — string — Opaque cursor returned by a previous page; pass it back to fetch the next page. _(minLen=1; maxLen=2048)_

**`NotFoundExceptionResponseContent`**

- `message` — string **(required)** _(default=Not found)_

**`ResolvedSecret`**

_One secret's resolution: its value, or the reason there is none._

- `secretId` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
- `value` — string — Absent when `failure` is set. _(format=password; minLen=1; maxLen=65536)_
- `attributes` — SecretAttributes — Non-secret companion fields, returned on management responses (the sensitive half stays in `value`). An optional `variant` key classifies the secret's shape (e.g. 'auth_basic', 'auth_bearer', 'auth_client_credentials'); the remaining keys are the companions that shape implies (e.g. 'auth_client_credentials' → { clientId, endpointUrl, scope }). Variants are an open convention, not a fixed enum; ListSecrets can filter by `variant`.
  - _map of_ `string`
- `revision` — number — Revision of the value returned. Absent when `failure` is set. _(min=1)_
- `failure` — string — Why a secret in a batch did not resolve — the batch equivalent of GetSecretValue's 404 and 409. _(enum: `not_found`, `pending`)_

**`ResolvedSecretFailure`**

_Why a secret in a batch did not resolve — the batch equivalent of GetSecretValue's 404 and 409._

- string _(enum: `not_found`, `pending`)_

**`RotateSecretRequestContent`**

- `value` — string **(required)** — Plaintext secret material. Accepted as input and returned only by GetSecretValue, never on management responses. Stored envelope-encrypted. For a structured secret (e.g. variant 'auth_client_credentials') this is the secret half; non-secret companions live in `attributes`. _(format=password; minLen=1; maxLen=65536)_

**`RotateSecretResponseContent`**

- `secret` — Secret **(required)** — A stored secret. The sensitive value is never included; non-secret attributes are.
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
  - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `name` — string **(required)** — Human- and machine-readable secret name, unique per company. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
  - `description` — string _(minLen=1; maxLen=1024)_
  - `attributes` — SecretAttributes — Non-secret companion fields, returned on management responses (the sensitive half stays in `value`). An optional `variant` key classifies the secret's shape (e.g. 'auth_basic', 'auth_bearer', 'auth_client_credentials'); the remaining keys are the companions that shape implies (e.g. 'auth_client_credentials' → { clientId, endpointUrl, scope }). Variants are an open convention, not a fixed enum; ListSecrets can filter by `variant`.
    - _map of_ `string`
  - `revision` — number **(required)** — Current revision, bumped on every rotation. Informational only. _(min=1)_
  - `status` — string **(required)** — Lifecycle state of a secret. _(enum: `pending`, `active`)_
  - `expiresAt` — string — When the credential behind this secret stops working, if that is known. Absent means unknown, which is the common case — it is recorded by whoever files the secret, not discovered. Informational, and deliberately not enforced: nothing refuses to resolve a secret past this instant, because the platform cannot know the provider agrees and a wrong date would then take down a working integration. It exists so a console can warn before an API key with a known lifetime fails, rather than the platform learning it from a failed agent turn.
  - `lastUsedAt` — string — When a runtime last resolved this credential, to the minute. Absent means never. Written on the resolve path, not by a management edit: reading a credential is not changing it, so this moves independently of the audit fields. Coarsened to the minute because the question it answers is asked in days and weeks, and an agent in a tool loop would otherwise rewrite it on every outbound call. Absent rather than an epoch for a credential nothing has used, because "nothing has ever resolved this" is a different and more actionable fact than "a long time ago" — it is what lets a console say a credential is safe to delete.

**`Secret`**

_A stored secret. The sensitive value is never included; non-secret attributes are._

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
- `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
- `companyId` — string **(required)** _(minLen=3; maxLen=30)_
- `name` — string **(required)** — Human- and machine-readable secret name, unique per company. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
- `description` — string _(minLen=1; maxLen=1024)_
- `attributes` — SecretAttributes — Non-secret companion fields, returned on management responses (the sensitive half stays in `value`). An optional `variant` key classifies the secret's shape (e.g. 'auth_basic', 'auth_bearer', 'auth_client_credentials'); the remaining keys are the companions that shape implies (e.g. 'auth_client_credentials' → { clientId, endpointUrl, scope }). Variants are an open convention, not a fixed enum; ListSecrets can filter by `variant`.
  - _map of_ `string`
- `revision` — number **(required)** — Current revision, bumped on every rotation. Informational only. _(min=1)_
- `status` — string **(required)** — Lifecycle state of a secret. _(enum: `pending`, `active`)_
- `expiresAt` — string — When the credential behind this secret stops working, if that is known. Absent means unknown, which is the common case — it is recorded by whoever files the secret, not discovered. Informational, and deliberately not enforced: nothing refuses to resolve a secret past this instant, because the platform cannot know the provider agrees and a wrong date would then take down a working integration. It exists so a console can warn before an API key with a known lifetime fails, rather than the platform learning it from a failed agent turn.
- `lastUsedAt` — string — When a runtime last resolved this credential, to the minute. Absent means never. Written on the resolve path, not by a management edit: reading a credential is not changing it, so this moves independently of the audit fields. Coarsened to the minute because the question it answers is asked in days and weeks, and an agent in a tool loop would otherwise rewrite it on every outbound call. Absent rather than an epoch for a credential nothing has used, because "nothing has ever resolved this" is a different and more actionable fact than "a long time ago" — it is what lets a console say a credential is safe to delete.

**`SecretAttributes`**

_Non-secret companion fields, returned on management responses (the sensitive half stays in `value`). An optional `variant` key classifies the secret's shape (e.g. 'auth_basic', 'auth_bearer', 'auth_client_credentials'); the remaining keys are the companions that shape implies (e.g. 'auth_client_credentials' → { clientId, endpointUrl, scope }). Variants are an open convention, not a fixed enum; ListSecrets can filter by `variant`._

- _map of_ `string`

**`SecretStatus`**

_Lifecycle state of a secret._

- string _(enum: `pending`, `active`)_

**`UpdateConnectionRequestContent`**

- `name` — string **(required)** — Connection name, unique per company. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
- `description` — string _(minLen=1; maxLen=1024)_
- `scopes` — array — OAuth scopes requested for the connection.
  - _array of_ `string`

**`UpdateConnectionResponseContent`**

- `connection` — Connection **(required)** — A configured connection: a company-wide SHARED credential, or a per-user USER credential. Holds registry and ownership metadata only, never the credential itself. `type` is the kind; `actor` is the owning user for USER connections.
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
  - `id` — string **(required)** — Unique identifier of a configured connection. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `type` — string **(required)** — Who a connection's credential belongs to. _(enum: `shared`, `user`)_
  - `provider` — string **(required)** — Provider key the connection authenticates against, e.g. "salesforce". A remote MCP server is created as `mcp`, with its URL in `connectionConfig.mcp_server_url`. The connection is filed under `mcp_` plus a digest of the server's canonical URL, which is the key every later operation uses: one key for every spelling of one server, and a key that keeps a URL carrying an access key out of request paths and audit rows. _(pattern=^[a-z][a-z0-9._-]*$; minLen=1; maxLen=128)_
  - `name` — string — Admin-given name, unique per company. Set for SHARED connections; absent for USER connections, which are identified by provider + `actor`. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
  - `description` — string _(minLen=1; maxLen=1024)_
  - `status` — string **(required)** — Lifecycle state of a connection. For a SHARED connection it is the company credential's state; for a USER connection it is that user's authorization state (PENDING until the user authorizes). _(enum: `pending`, `active`, `expired`, `error`)_
  - `scopes` — array — OAuth scopes requested for the connection.
    - _array of_ `string`
  - `connectionConfig` — ConnectionConfig — Provider parameters the authorization flow itself needs, e.g. `{"hostname": "eu.app.clio.com"}`. A provider may template its OAuth endpoints on these — Clio's authorization and token URLs are both `https://${connectionConfig.hostname}/…` — so for those providers a connection simply cannot be authorized without one. Which fields a provider declares, and their allowed values, are published on the connector definition as `authorization.connectionConfiguration`. Configuration, never credentials. The keys a provider's broker reserves for swapping the OAuth application itself are refused rather than forwarded.
    - _map of_ `string`
  - `actor` — ConnectionActor — The end user who owns a USER connection. A display snapshot only; never used to resolve the credential (that is keyed by provider + user).
    - `id` — string **(required)** — Wildix user id of the owning end user. _(minLen=12; maxLen=12)_
    - `name` — string — Display name at the time the connection was recorded.
    - `email` — string — Email of the owning user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `extension` — string — PBX extension of the owning user.
  - `serverUrl` — string — The remote MCP server this connection is for, as `connectionConfig.mcp_server_url` named it. Present only for an `mcp_*` provider. Read-only: the provider key is a digest of it, so it is what a person reads in place of that key. _(minLen=1; maxLen=2048)_
  - `lastUsedAt` — string — When a runtime last minted a token from this connection, to the minute. Absent means never. Written on the resolve path rather than by a management edit, so it moves independently of the audit fields — reading a credential is not changing it.

**`UpdateSecretRequestContent`**

- `name` — string **(required)** — Human- and machine-readable secret name, unique per company. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
- `description` — string _(minLen=1; maxLen=1024)_
- `attributes` — SecretAttributes — Non-secret companion fields, returned on management responses (the sensitive half stays in `value`). An optional `variant` key classifies the secret's shape (e.g. 'auth_basic', 'auth_bearer', 'auth_client_credentials'); the remaining keys are the companions that shape implies (e.g. 'auth_client_credentials' → { clientId, endpointUrl, scope }). Variants are an open convention, not a fixed enum; ListSecrets can filter by `variant`.
  - _map of_ `string`

**`UpdateSecretResponseContent`**

- `secret` — Secret **(required)** — A stored secret. The sensitive value is never included; non-secret attributes are.
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
  - `id` — string **(required)** — Unique identifier of a secret. _(pattern=^[0-9A-Za-z]{8}$; minLen=8; maxLen=8)_
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `name` — string **(required)** — Human- and machine-readable secret name, unique per company. _(pattern=^[a-zA-Z0-9_.-]+$; minLen=1; maxLen=128)_
  - `description` — string _(minLen=1; maxLen=1024)_
  - `attributes` — SecretAttributes — Non-secret companion fields, returned on management responses (the sensitive half stays in `value`). An optional `variant` key classifies the secret's shape (e.g. 'auth_basic', 'auth_bearer', 'auth_client_credentials'); the remaining keys are the companions that shape implies (e.g. 'auth_client_credentials' → { clientId, endpointUrl, scope }). Variants are an open convention, not a fixed enum; ListSecrets can filter by `variant`.
    - _map of_ `string`
  - `revision` — number **(required)** — Current revision, bumped on every rotation. Informational only. _(min=1)_
  - `status` — string **(required)** — Lifecycle state of a secret. _(enum: `pending`, `active`)_
  - `expiresAt` — string — When the credential behind this secret stops working, if that is known. Absent means unknown, which is the common case — it is recorded by whoever files the secret, not discovered. Informational, and deliberately not enforced: nothing refuses to resolve a secret past this instant, because the platform cannot know the provider agrees and a wrong date would then take down a working integration. It exists so a console can warn before an API key with a known lifetime fails, rather than the platform learning it from a failed agent turn.
  - `lastUsedAt` — string — When a runtime last resolved this credential, to the minute. Absent means never. Written on the resolve path, not by a management edit: reading a credential is not changing it, so this moves independently of the audit fields. Coarsened to the minute because the question it answers is asked in days and weeks, and an agent in a tool loop would otherwise rewrite it on every outbound call. Absent rather than an epoch for a credential nothing has used, because "nothing has ever resolved this" is a different and more actionable fact than "a long time ago" — it is what lets a console say a credential is safe to delete.

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

**`VerifyConnectionResponseContent`**

_The outcome of a verification. Never the credential, and never a token._

- `status` — string **(required)** — Lifecycle state of a connection. For a SHARED connection it is the company credential's state; for a USER connection it is that user's authorization state (PENDING until the user authorizes). _(enum: `pending`, `active`, `expired`, `error`)_
- `working` — boolean **(required)** — Whether a credential could actually be resolved just now.
- `reason` — string — Why a verification did not produce a credential. _(enum: `not_authorized`, `revoked`, `unavailable`)_

**`VerifyFailureReason`**

_Why a verification did not produce a credential._

- string _(enum: `not_authorized`, `revoked`, `unavailable`)_

</details>
