## Knowledge Base API

_OpenAPI: Wim Knowledge Base service — version v1_

**Servers**

- `https://kb.wim.wildix.com` — Production
- `https://kb.wim-stable.wildix.com` — Stable
- `https://kb.wim-stage.wildix.com` — Stage

### DataSources

#### `GET` `/api/v1/data-sources`

List all data sources for the current company

- operationId: `ListDataSources`
- **Scopes**: `kb:ListDataSources`, `kb:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`ListDataSourcesResponseContent`)
  - `dataSources` — array **(required)**
    - _array of_ `DataSourceItem`
      - `name` — string **(required)** — Descriptive name for the data source. Used for identification and display in the UI. Examples: 'Product Confluence', 'Customer Service Docs', 'Engineering Wikis'. Length: 2-100 characters _(minLen=2; maxLen=100)_
      - `description` — string — Optional detailed description of the data source content and purpose. Helps users understand what data is included. Examples: 'Contains product documentation and service guides from Confluence', 'Customer service articles synced from Zendesk'. Length: 0-1000 characters _(maxLen=1000)_
      - `type` — string **(required)** _(enum: `files`, `confluence`, `gdrive`, `website`)_
      - `config` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`confluence`**
            - `confluence` — ConfluenceConfig **(required)**
              - `baseUrl` — string **(required)** — The base URL of your Confluence Cloud or Server instance. Must be a valid HTTPS URL. Example: https://your-company.atlassian.net
              - `username` — string **(required)** — The email address or username associated with the Confluence account used for authentication
              - `apiKey` — string **(required)** — The API token or password for Confluence authentication. For Cloud instances, use an API token; for Server instances, use the account password
              - `spaceId` — string **(required)** — The Confluence space key or ID to synchronize. All pages within this space will be included unless explicitly excluded
              - `pages` — ConfluencePagesConfig
                - _(nesting depth limit — see `ConfluencePagesConfig` in the Schemas appendix)_
          - **`gdrive`**
            - `gdrive` — GDriveConfig **(required)**
              - `nangoConnectionId` — string **(required)** — The Nango integration connection ID for Google Drive. This establishes the OAuth connection to access the Drive account
              - `folders` — GDriveFoldersConfig **(required)**
                - _(nesting depth limit — see `GDriveFoldersConfig` in the Schemas appendix)_
          - **`website`**
            - `website` — WebsiteConfig **(required)**
              - `urls` — array **(required)** — Starting page URLs of the website to index. Must be https and resolve to a public address. The v1 console configures exactly one, but the field is a list so additional starting points can be added without a breaking change
                - _array of_ `string`
              - `maxPages` — number — Upper bound on how many pages may be selected for indexing. Server-side limits still apply and take precedence _(min=1; max=2000)_
              - `pages` — WebsitePagesConfig
                - _(nesting depth limit — see `WebsitePagesConfig` in the Schemas appendix)_
          - **`files`**
            - `files` — any **(required)**
      - `syncSchedule` — object
      - `id` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
      - `companyId` — string **(required)** — Company ID that owns this data source _(minLen=3; maxLen=30)_
      - `createdAt` — string **(required)** — Timestamp when the data source was created (ISO 8601 format). Example: 2025-01-01T00:00:00Z
      - `updatedAt` — string **(required)** — Timestamp when the data source was last updated (ISO 8601 format). Example: 2025-01-01T00:00:00Z
- Errors: `400`, `401`, `403`, `404`

#### `POST` `/api/v1/data-sources`

Register a new data source with minimal configuration. All other parameters will be set in update operation.

- operationId: `CreateDataSource`
- **Scopes**: `kb:CreateDataSource`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `CreateDataSourceRequestContent`) **(required)**
  - `name` — string **(required)** — Descriptive name for the data source. Used for identification and display in the UI. Examples: 'Product Confluence', 'Customer Service Docs', 'Engineering Wikis'. Length: 2-100 characters _(minLen=2; maxLen=100)_
  - `description` — string — Optional detailed description of the data source content and purpose. Helps users understand what data is included. Examples: 'Contains product documentation and service guides from Confluence', 'Customer service articles synced from Zendesk'. Length: 0-1000 characters _(maxLen=1000)_
  - `type` — string **(required)** _(enum: `files`, `confluence`, `gdrive`, `website`)_
- **Response 201** (`CreateDataSourceResponseContent`)
  - `dataSource` — DataSourceItem **(required)**
    - `name` — string **(required)** — Descriptive name for the data source. Used for identification and display in the UI. Examples: 'Product Confluence', 'Customer Service Docs', 'Engineering Wikis'. Length: 2-100 characters _(minLen=2; maxLen=100)_
    - `description` — string — Optional detailed description of the data source content and purpose. Helps users understand what data is included. Examples: 'Contains product documentation and service guides from Confluence', 'Customer service articles synced from Zendesk'. Length: 0-1000 characters _(maxLen=1000)_
    - `type` — string **(required)** _(enum: `files`, `confluence`, `gdrive`, `website`)_
    - `config` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`confluence`**
          - `confluence` — ConfluenceConfig **(required)**
            - `baseUrl` — string **(required)** — The base URL of your Confluence Cloud or Server instance. Must be a valid HTTPS URL. Example: https://your-company.atlassian.net
            - `username` — string **(required)** — The email address or username associated with the Confluence account used for authentication
            - `apiKey` — string **(required)** — The API token or password for Confluence authentication. For Cloud instances, use an API token; for Server instances, use the account password
            - `spaceId` — string **(required)** — The Confluence space key or ID to synchronize. All pages within this space will be included unless explicitly excluded
            - `pages` — ConfluencePagesConfig
              - `enabled` — array **(required)** — List of Confluence page IDs that should be included in the synchronization
                - _array of_ `string`
              - `disabled` — array **(required)** — List of Confluence page IDs that should be explicitly excluded from the synchronization
                - _array of_ `string`
        - **`gdrive`**
          - `gdrive` — GDriveConfig **(required)**
            - `nangoConnectionId` — string **(required)** — The Nango integration connection ID for Google Drive. This establishes the OAuth connection to access the Drive account
            - `folders` — GDriveFoldersConfig **(required)**
              - `enabled` — array **(required)** — List of Google Drive folder IDs that should be included in the synchronization
                - _array of_ `string`
              - `disabled` — array **(required)** — List of Google Drive folder IDs that should be explicitly excluded from the synchronization
                - _array of_ `string`
        - **`website`**
          - `website` — WebsiteConfig **(required)**
            - `urls` — array **(required)** — Starting page URLs of the website to index. Must be https and resolve to a public address. The v1 console configures exactly one, but the field is a list so additional starting points can be added without a breaking change
              - _array of_ `string`
            - `maxPages` — number — Upper bound on how many pages may be selected for indexing. Server-side limits still apply and take precedence _(min=1; max=2000)_
            - `pages` — WebsitePagesConfig
              - `enabled` — array **(required)** — Absolute page URLs that should be fetched and indexed. These are the pages the user selected from the discovery result, and the complete set: anything absent is not indexed
                - _array of_ `string`
        - **`files`**
          - `files` — any **(required)**
    - `syncSchedule` — object
    - `id` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `companyId` — string **(required)** — Company ID that owns this data source _(minLen=3; maxLen=30)_
    - `createdAt` — string **(required)** — Timestamp when the data source was created (ISO 8601 format). Example: 2025-01-01T00:00:00Z
    - `updatedAt` — string **(required)** — Timestamp when the data source was last updated (ISO 8601 format). Example: 2025-01-01T00:00:00Z
- Errors: `400`, `401`, `403`, `404`

#### `GET` `/api/v1/data-sources/{dataSourceId}`

Get a data source by its ID

- operationId: `GetDataSource`
- **Scopes**: `kb:GetDataSource`, `kb:read`
- **Parameters**
  - `dataSourceId` (path) — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetDataSourceResponseContent`)
  - `dataSource` — DataSourceItem **(required)**
    - `name` — string **(required)** — Descriptive name for the data source. Used for identification and display in the UI. Examples: 'Product Confluence', 'Customer Service Docs', 'Engineering Wikis'. Length: 2-100 characters _(minLen=2; maxLen=100)_
    - `description` — string — Optional detailed description of the data source content and purpose. Helps users understand what data is included. Examples: 'Contains product documentation and service guides from Confluence', 'Customer service articles synced from Zendesk'. Length: 0-1000 characters _(maxLen=1000)_
    - `type` — string **(required)** _(enum: `files`, `confluence`, `gdrive`, `website`)_
    - `config` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`confluence`**
          - `confluence` — ConfluenceConfig **(required)**
            - `baseUrl` — string **(required)** — The base URL of your Confluence Cloud or Server instance. Must be a valid HTTPS URL. Example: https://your-company.atlassian.net
            - `username` — string **(required)** — The email address or username associated with the Confluence account used for authentication
            - `apiKey` — string **(required)** — The API token or password for Confluence authentication. For Cloud instances, use an API token; for Server instances, use the account password
            - `spaceId` — string **(required)** — The Confluence space key or ID to synchronize. All pages within this space will be included unless explicitly excluded
            - `pages` — ConfluencePagesConfig
              - `enabled` — array **(required)** — List of Confluence page IDs that should be included in the synchronization
                - _array of_ `string`
              - `disabled` — array **(required)** — List of Confluence page IDs that should be explicitly excluded from the synchronization
                - _array of_ `string`
        - **`gdrive`**
          - `gdrive` — GDriveConfig **(required)**
            - `nangoConnectionId` — string **(required)** — The Nango integration connection ID for Google Drive. This establishes the OAuth connection to access the Drive account
            - `folders` — GDriveFoldersConfig **(required)**
              - `enabled` — array **(required)** — List of Google Drive folder IDs that should be included in the synchronization
                - _array of_ `string`
              - `disabled` — array **(required)** — List of Google Drive folder IDs that should be explicitly excluded from the synchronization
                - _array of_ `string`
        - **`website`**
          - `website` — WebsiteConfig **(required)**
            - `urls` — array **(required)** — Starting page URLs of the website to index. Must be https and resolve to a public address. The v1 console configures exactly one, but the field is a list so additional starting points can be added without a breaking change
              - _array of_ `string`
            - `maxPages` — number — Upper bound on how many pages may be selected for indexing. Server-side limits still apply and take precedence _(min=1; max=2000)_
            - `pages` — WebsitePagesConfig
              - `enabled` — array **(required)** — Absolute page URLs that should be fetched and indexed. These are the pages the user selected from the discovery result, and the complete set: anything absent is not indexed
                - _array of_ `string`
        - **`files`**
          - `files` — any **(required)**
    - `syncSchedule` — object
    - `id` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `companyId` — string **(required)** — Company ID that owns this data source _(minLen=3; maxLen=30)_
    - `createdAt` — string **(required)** — Timestamp when the data source was created (ISO 8601 format). Example: 2025-01-01T00:00:00Z
    - `updatedAt` — string **(required)** — Timestamp when the data source was last updated (ISO 8601 format). Example: 2025-01-01T00:00:00Z
- Errors: `400`, `401`, `403`, `404`

#### `PUT` `/api/v1/data-sources/{dataSourceId}`

Update a data source by its ID

- operationId: `UpdateDataSource`
- **Scopes**: `kb:UpdateDataSource`
- **Parameters**
  - `dataSourceId` (path) — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `UpdateDataSourceRequestContent`) **(required)**
  - `name` — string **(required)** — Updated descriptive name for the data source. Used for identification and display in the UI. Length: 2-100 characters _(minLen=2; maxLen=100)_
  - `description` — string — Updated detailed description of the data source content and purpose. Length: 0-1000 characters _(maxLen=1000)_
- **Response 200** (`UpdateDataSourceResponseContent`)
  - `dataSource` — DataSourceItem **(required)**
    - `name` — string **(required)** — Descriptive name for the data source. Used for identification and display in the UI. Examples: 'Product Confluence', 'Customer Service Docs', 'Engineering Wikis'. Length: 2-100 characters _(minLen=2; maxLen=100)_
    - `description` — string — Optional detailed description of the data source content and purpose. Helps users understand what data is included. Examples: 'Contains product documentation and service guides from Confluence', 'Customer service articles synced from Zendesk'. Length: 0-1000 characters _(maxLen=1000)_
    - `type` — string **(required)** _(enum: `files`, `confluence`, `gdrive`, `website`)_
    - `config` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`confluence`**
          - `confluence` — ConfluenceConfig **(required)**
            - `baseUrl` — string **(required)** — The base URL of your Confluence Cloud or Server instance. Must be a valid HTTPS URL. Example: https://your-company.atlassian.net
            - `username` — string **(required)** — The email address or username associated with the Confluence account used for authentication
            - `apiKey` — string **(required)** — The API token or password for Confluence authentication. For Cloud instances, use an API token; for Server instances, use the account password
            - `spaceId` — string **(required)** — The Confluence space key or ID to synchronize. All pages within this space will be included unless explicitly excluded
            - `pages` — ConfluencePagesConfig
              - `enabled` — array **(required)** — List of Confluence page IDs that should be included in the synchronization
                - _array of_ `string`
              - `disabled` — array **(required)** — List of Confluence page IDs that should be explicitly excluded from the synchronization
                - _array of_ `string`
        - **`gdrive`**
          - `gdrive` — GDriveConfig **(required)**
            - `nangoConnectionId` — string **(required)** — The Nango integration connection ID for Google Drive. This establishes the OAuth connection to access the Drive account
            - `folders` — GDriveFoldersConfig **(required)**
              - `enabled` — array **(required)** — List of Google Drive folder IDs that should be included in the synchronization
                - _array of_ `string`
              - `disabled` — array **(required)** — List of Google Drive folder IDs that should be explicitly excluded from the synchronization
                - _array of_ `string`
        - **`website`**
          - `website` — WebsiteConfig **(required)**
            - `urls` — array **(required)** — Starting page URLs of the website to index. Must be https and resolve to a public address. The v1 console configures exactly one, but the field is a list so additional starting points can be added without a breaking change
              - _array of_ `string`
            - `maxPages` — number — Upper bound on how many pages may be selected for indexing. Server-side limits still apply and take precedence _(min=1; max=2000)_
            - `pages` — WebsitePagesConfig
              - `enabled` — array **(required)** — Absolute page URLs that should be fetched and indexed. These are the pages the user selected from the discovery result, and the complete set: anything absent is not indexed
                - _array of_ `string`
        - **`files`**
          - `files` — any **(required)**
    - `syncSchedule` — object
    - `id` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `companyId` — string **(required)** — Company ID that owns this data source _(minLen=3; maxLen=30)_
    - `createdAt` — string **(required)** — Timestamp when the data source was created (ISO 8601 format). Example: 2025-01-01T00:00:00Z
    - `updatedAt` — string **(required)** — Timestamp when the data source was last updated (ISO 8601 format). Example: 2025-01-01T00:00:00Z
- Errors: `400`, `401`, `403`, `404`

#### `DELETE` `/api/v1/data-sources/{dataSourceId}`

Delete a data source by its ID

- operationId: `DeleteDataSource`
- **Scopes**: `kb:DeleteDataSource`
- **Parameters**
  - `dataSourceId` (path) — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- Errors: `400`, `401`, `403`, `404`

#### `POST` `/api/v1/data-sources/{dataSourceId}/clean`

Clean the data source by its ID. It will clean all documents and sync logs. This operation is irreversible.

- operationId: `CleanDataSource`
- **Scopes**: `kb:CleanDataSource`
- **Parameters**
  - `dataSourceId` (path) — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- Errors: `400`, `401`, `403`, `404`

#### `POST` `/api/v1/data-sources/{dataSourceId}/clone`

Clone a data source by its ID. Only configuration will be cloned, not the data.

- operationId: `CloneDataSource`
- **Scopes**: `kb:CloneDataSource`
- **Parameters**
  - `dataSourceId` (path) — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`CloneDataSourceResponseContent`)
  - `dataSourceId` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
- Errors: `400`, `401`, `403`, `404`

#### `PUT` `/api/v1/data-sources/{dataSourceId}/configure`

Configure a data source by its ID

- operationId: `ConfigureDataSource`
- **Scopes**: `kb:ConfigureDataSource`
- **Parameters**
  - `dataSourceId` (path) — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `ConfigureDataSourceRequestContent`) **(required)**
  - `config` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`confluence`**
        - `confluence` — ConfluenceConfig **(required)**
          - `baseUrl` — string **(required)** — The base URL of your Confluence Cloud or Server instance. Must be a valid HTTPS URL. Example: https://your-company.atlassian.net
          - `username` — string **(required)** — The email address or username associated with the Confluence account used for authentication
          - `apiKey` — string **(required)** — The API token or password for Confluence authentication. For Cloud instances, use an API token; for Server instances, use the account password
          - `spaceId` — string **(required)** — The Confluence space key or ID to synchronize. All pages within this space will be included unless explicitly excluded
          - `pages` — ConfluencePagesConfig
            - `enabled` — array **(required)** — List of Confluence page IDs that should be included in the synchronization
              - _array of_ `string`
            - `disabled` — array **(required)** — List of Confluence page IDs that should be explicitly excluded from the synchronization
              - _array of_ `string`
      - **`gdrive`**
        - `gdrive` — GDriveConfig **(required)**
          - `nangoConnectionId` — string **(required)** — The Nango integration connection ID for Google Drive. This establishes the OAuth connection to access the Drive account
          - `folders` — GDriveFoldersConfig **(required)**
            - `enabled` — array **(required)** — List of Google Drive folder IDs that should be included in the synchronization
              - _array of_ `string`
            - `disabled` — array **(required)** — List of Google Drive folder IDs that should be explicitly excluded from the synchronization
              - _array of_ `string`
      - **`website`**
        - `website` — WebsiteConfig **(required)**
          - `urls` — array **(required)** — Starting page URLs of the website to index. Must be https and resolve to a public address. The v1 console configures exactly one, but the field is a list so additional starting points can be added without a breaking change
            - _array of_ `string`
          - `maxPages` — number — Upper bound on how many pages may be selected for indexing. Server-side limits still apply and take precedence _(min=1; max=2000)_
          - `pages` — WebsitePagesConfig
            - `enabled` — array **(required)** — Absolute page URLs that should be fetched and indexed. These are the pages the user selected from the discovery result, and the complete set: anything absent is not indexed
              - _array of_ `string`
      - **`files`**
        - `files` — any **(required)**
  - `syncSchedule` — object
- **Response 200** (`ConfigureDataSourceResponseContent`)
  - `dataSource` — DataSourceItem **(required)**
    - `name` — string **(required)** — Descriptive name for the data source. Used for identification and display in the UI. Examples: 'Product Confluence', 'Customer Service Docs', 'Engineering Wikis'. Length: 2-100 characters _(minLen=2; maxLen=100)_
    - `description` — string — Optional detailed description of the data source content and purpose. Helps users understand what data is included. Examples: 'Contains product documentation and service guides from Confluence', 'Customer service articles synced from Zendesk'. Length: 0-1000 characters _(maxLen=1000)_
    - `type` — string **(required)** _(enum: `files`, `confluence`, `gdrive`, `website`)_
    - `config` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`confluence`**
          - `confluence` — ConfluenceConfig **(required)**
            - `baseUrl` — string **(required)** — The base URL of your Confluence Cloud or Server instance. Must be a valid HTTPS URL. Example: https://your-company.atlassian.net
            - `username` — string **(required)** — The email address or username associated with the Confluence account used for authentication
            - `apiKey` — string **(required)** — The API token or password for Confluence authentication. For Cloud instances, use an API token; for Server instances, use the account password
            - `spaceId` — string **(required)** — The Confluence space key or ID to synchronize. All pages within this space will be included unless explicitly excluded
            - `pages` — ConfluencePagesConfig
              - `enabled` — array **(required)** — List of Confluence page IDs that should be included in the synchronization
                - _array of_ `string`
              - `disabled` — array **(required)** — List of Confluence page IDs that should be explicitly excluded from the synchronization
                - _array of_ `string`
        - **`gdrive`**
          - `gdrive` — GDriveConfig **(required)**
            - `nangoConnectionId` — string **(required)** — The Nango integration connection ID for Google Drive. This establishes the OAuth connection to access the Drive account
            - `folders` — GDriveFoldersConfig **(required)**
              - `enabled` — array **(required)** — List of Google Drive folder IDs that should be included in the synchronization
                - _array of_ `string`
              - `disabled` — array **(required)** — List of Google Drive folder IDs that should be explicitly excluded from the synchronization
                - _array of_ `string`
        - **`website`**
          - `website` — WebsiteConfig **(required)**
            - `urls` — array **(required)** — Starting page URLs of the website to index. Must be https and resolve to a public address. The v1 console configures exactly one, but the field is a list so additional starting points can be added without a breaking change
              - _array of_ `string`
            - `maxPages` — number — Upper bound on how many pages may be selected for indexing. Server-side limits still apply and take precedence _(min=1; max=2000)_
            - `pages` — WebsitePagesConfig
              - `enabled` — array **(required)** — Absolute page URLs that should be fetched and indexed. These are the pages the user selected from the discovery result, and the complete set: anything absent is not indexed
                - _array of_ `string`
        - **`files`**
          - `files` — any **(required)**
    - `syncSchedule` — object
    - `id` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `companyId` — string **(required)** — Company ID that owns this data source _(minLen=3; maxLen=30)_
    - `createdAt` — string **(required)** — Timestamp when the data source was created (ISO 8601 format). Example: 2025-01-01T00:00:00Z
    - `updatedAt` — string **(required)** — Timestamp when the data source was last updated (ISO 8601 format). Example: 2025-01-01T00:00:00Z
- Errors: `400`, `401`, `403`, `404`

#### `POST` `/api/v1/data-sources/{dataSourceId}/describe`

Describe the data source by its ID. It will return additional information about the data source based on the parameters provided.

- operationId: `DescribeDataSource`
- **Scopes**: `kb:DescribeDataSource`, `kb:read`
- **Parameters**
  - `dataSourceId` (path) — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `DescribeDataSourceRequestContent`) **(required)**
  - `parameters` — DescribeDataSourceParameters **(required)**
    - `confluence` — DescribeDataSourceConfluenceParameters
      - `spaces` — DescribeDataSourceConfluenceSpacesParameters
        - `type` — string _(enum: `global`, `collaboration`, `knowledge_base`, `personal`, `system`, `onboarding`)_
      - `pages` — DescribeDataSourceConfluencePagesParameters
        - `spaceId` — string **(required)** — Confluence space ID to list pages from. Required when requesting page information _(minLen=1; maxLen=50)_
        - `parentId` — string — Optional parent page ID to retrieve only child pages under this page. If not specified, retrieves all pages in the space _(minLen=1; maxLen=50)_
        - `enabled` — array — Optional list of specific page IDs to include in the result. If provided, only these pages are returned
          - _array of_ `string`
    - `gdrive` — DescribeDataSourceGDriveParameters
      - `session` — DescribeDataSourceGDriveSessionParameters
        - `userId` — string **(required)** — User ID for the Google Drive session. Used to identify which user's drive context to use. Defaults to 'admin' for admin user context _(default=admin)_
      - `folders` — DescribeDataSourceGDriveFoldersParameters
        - `parentId` — string **(required)** — Parent folder ID to list folders from. Use 'root' to start from the Google Drive root directory. Any valid folder ID can be specified to browse subfolders _(default=root)_
        - `enabled` — array — Optional list of specific folder IDs to include in the result. If provided, only these folders are returned
          - _array of_ `string`
    - `website` — DescribeDataSourceWebsiteParameters
      - `discover` — DescribeDataSourceWebsiteDiscoverParameters
        - `url` — string **(required)** — Starting page URL of the website. Must be https and resolve to a public address _(minLen=1; maxLen=2048)_
    - `proxy` — any — Parameters for describing proxy data source (type-specific, implementation varies)
    - `files` — any — Parameters for describing file-based data source (type-specific, implementation varies)
- **Response 200** (`DescribeDataSourceResponseContent`)
  - `result` — DescribeDataSourceResult **(required)**
    - `confluence` — DescribeDataSourceConfluenceResult
      - `spaces` — array — List of Confluence spaces matching the requested type filter. Only present if spaces were requested in the describe parameters
        - _array of_ `DescribeDataSourceConfluenceSpaceResult`
          - `id` — string **(required)** — Unique identifier of the Confluence space
          - `name` — string **(required)** — Display name of the Confluence space
          - `key` — string — Space key (short identifier) used in Confluence URLs
          - `type` — string **(required)** _(enum: `global`, `collaboration`, `knowledge_base`, `personal`, `system`, `onboarding`)_
      - `pages` — array — List of Confluence pages from the requested space, with optional parent filtering. Only present if pages were requested in the describe parameters
        - _array of_ `DescribeDataSourceConfluencePageResult`
          - `id` — string **(required)** — Unique identifier of the Confluence page _(minLen=1; maxLen=50)_
          - `parentId` — string **(required)** — ID of the parent page. If this is a top-level page, parentId references the space _(minLen=1; maxLen=50)_
          - `title` — string **(required)** — Display title of the Confluence page
          - `position` — number — Position or order of the page within its parent. Used for determining page hierarchy
    - `gdrive` — DescribeDataSourceGDriveResult
      - `sessionId` — string — Nango session ID for the Google Drive integration. Used for OAuth authentication and drive access
      - `folders` — array — List of folders from the requested parent directory, including their IDs, parent references, and names
        - _array of_ `DescribeDataSourceGDriveFolderResult`
          - `id` — string **(required)** — Unique identifier of the Google Drive folder
          - `parentId` — string **(required)** — ID of the parent folder. Allows reconstructing the folder hierarchy
          - `name` — string **(required)** — Display name of the folder in Google Drive
    - `website` — DescribeDataSourceWebsiteResult
      - `pages` — array **(required)** — Pages discovered for the requested website
        - _array of_ `DescribeDataSourceWebsitePageResult`
          - `url` — string **(required)** — Absolute URL of the discovered page
          - `host` — string **(required)** — Host the page belongs to, so pages can be grouped by host in the UI
          - `path` — string **(required)** — Path (including query string) of the page, for display in the selection list
          - `lastModified` — string — Last modification time reported by the sitemap, in ISO 8601 format. Absent for crawl-discovered pages
      - `strategy` — string **(required)** — Which discovery strategy produced a page list. Sitemap discovery is free and usually more complete; crawl is the fallback for sites without a usable sitemap _(enum: `sitemap`, `crawl`)_
      - `truncated` — boolean **(required)** — True when discovery stopped at a limit, meaning the site has more pages than were returned
      - `canonicalUrl` — string **(required)** — The starting URL after redirects were followed. Differs from the requested URL when, for example, an apex domain redirects to www. Page scope is anchored to this URL
      - `limits` — DescribeDataSourceWebsiteLimits **(required)**
        - `maxSelectedPages` — number **(required)** — Maximum number of pages that may be selected for indexing
        - `maxDiscoveredPages` — number **(required)** — Maximum number of pages the discovery step returns
    - `proxy` — any — Result of describing proxy data source (type-specific results)
    - `files` — any — Result of describing file-based data source (type-specific results)
- Errors: `400`, `401`, `403`, `404`

#### `POST` `/api/v1/data-sources/{dataSourceId}/start-sync`

Start the sync of a data source by its ID

- operationId: `StartSyncDataSource`
- **Scopes**: `kb:StartSyncDataSource`
- **Parameters**
  - `dataSourceId` (path) — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `syncType` (query) — string — The synchronization mode to use. 'full' performs a complete re-sync of all data, 'incremental' syncs only new or modified data since the last sync. Defaults to 'full' if not specified _(enum: `full`, `incremental`)_
- Errors: `400`, `401`, `403`, `404`

#### `GET` `/api/v1/data-sources/{dataSourceId}/statistics`

List the statistics of a data source by its ID

- operationId: `ListDataSourceStatistics`
- **Scopes**: `kb:ListDataSourceStatistics`, `kb:read`
- **Parameters**
  - `dataSourceId` (path) — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`ListDataSourceStatisticsResponseContent`)
  - `documentsCount` — number **(required)**
  - `chunksCount` — number **(required)**
- Errors: `400`, `401`, `403`, `404`

#### `POST` `/api/v1/data-sources/{dataSourceId}/stop-sync`

Stop the sync of a data source by its ID

- operationId: `StopSyncDataSource`
- **Scopes**: `kb:StopSyncDataSource`
- **Parameters**
  - `dataSourceId` (path) — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- Errors: `400`, `401`, `403`, `404`

#### `GET` `/api/v1/data-sources/{dataSourceId}/sync-logs`

Get the sync logs of a data source by its ID

- operationId: `ListDataSourceSynchronizationLogs`
- **Scopes**: `kb:ListDataSourceSynchronizationLogs`, `kb:read`
- **Parameters**
  - `dataSourceId` (path) — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `limit` (query) — number _(default=50; min=1; max=500)_
  - `offset` (query) — number _(default=0; min=0)_
  - `sort` (query) — string — Sort order of the results. If there is a '-' prefix, the results will be sorted in descending order. Otherwise, the results will be sorted in ascending order. Example: '-createdAt' will sort the results by createdAt in descending order. 'createdAt' will sort the results by createdAt in ascending order. _(default=-createdAt; pattern=^-?[a-zA-Z0-9_]{1,32}$)_
  - `logLevel` (query) — string — The log level to filter the sync logs by. Possible values: 'debug', 'info', 'warn', 'error'. _(enum: `debug`, `info`, `warn`, `error`)_
  - `search` (query) — string — The search query string for filtering the history results. _(pattern=^[\p{L}0-9 \-_]{3,32}$)_
- **Response 200** (`ListDataSourceSynchronizationLogsResponseContent`)
  - `logs` — array **(required)**
    - _array of_ `SyncLogItem`
      - `timestamp` — string **(required)**
      - `level` — string **(required)** _(enum: `debug`, `info`, `warn`, `error`)_
      - `message` — string **(required)**
  - `metadata` — PaginationMetadata **(required)**
    - `total` — number **(required)** — The total number of results.
    - `limit` — number — The number of results per page.
    - `offset` — number — The offset from which to start the results.
- Errors: `400`, `401`, `403`, `404`

#### `GET` `/api/v1/data-sources/{dataSourceId}/sync-status`

Get the sync status of a data source by its ID

- operationId: `GetDataSourceSyncStatus`
- **Scopes**: `kb:GetDataSourceSyncStatus`, `kb:read`
- **Parameters**
  - `dataSourceId` (path) — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetDataSourceSyncStatusResponseContent`)
  - `status` — string **(required)** _(enum: `idle`, `running`, `success`, `failed`)_
  - `syncedAt` — string — Timestamp when the data source was last synced (ISO 8601 format). Example: 2021-01-01T00:00:00Z
  - `mode` — string _(enum: `full`, `incremental`)_
  - `error` — string — The error message from the last sync, if any.
  - `documentsStats` — SyncStatusStats
    - _map of_ `number`
- Errors: `400`, `401`, `403`, `404`

### Documents

#### `GET` `/api/v1/data-sources/{dataSourceId}/documents`

List all documents for a data source by its ID

- operationId: `ListDocuments`
- **Scopes**: `kb:ListDocuments`, `kb:read`
- **Parameters**
  - `dataSourceId` (path) — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `limit` (query) — number _(default=50; min=1; max=500)_
  - `offset` (query) — number _(default=0; min=0)_
  - `sort` (query) — string — Sort order of the results. If there is a '-' prefix, the results will be sorted in descending order. Otherwise, the results will be sorted in ascending order. Example: '-createdAt' will sort the results by createdAt in descending order. 'createdAt' will sort the results by createdAt in ascending order. _(default=-createdAt; pattern=^-?[a-zA-Z0-9_]{1,32}$)_
  - `search` (query) — string — The search query string for filtering the documents results. _(pattern=^[\p{L}0-9 \-_]{3,32}$)_
  - `originalId` (query) — string — Filter documents by original ID from the source system. _(minLen=1; maxLen=255)_
  - `status` (query) — string — Filter documents by status. _(enum: `draft`, `pending`, `processing`, `completed`, `failed`)_
- **Response 200** (`ListDocumentsResponseContent`)
  - `documents` — array **(required)**
    - _array of_ `DocumentItem`
      - `title` — string **(required)** — Display title of the document used in search results and UI. Can differ from originalName. Examples: 'Product Installation Guide', 'API Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
      - `url` — string — Optional URL where the document can be accessed or viewed. Used for providing direct links to the source. Example: https://confluence.company.com/wiki/Product_Documentation _(maxLen=1024)_
      - `content` — string — Optional document content in plain text or markdown format. For file uploads, can be the document content.
      - `description` — string — Optional detailed description of the document content and purpose. Helps users understand what the document is about. _(maxLen=2048)_
      - `originalFormat` — string **(required)** — File format/extension of the original document for reference. Examples: 'pdf', 'docx', 'md', 'html', 'txt'. Helps identify source document type _(minLen=1; maxLen=10)_
      - `originalName` — string **(required)** — Original filename or identifier of the source document. Preserves the source document name. Examples: 'product-knowledge-base.pdf', 'installation-guide.docx' _(minLen=1; maxLen=255)_
      - `originalId` — string — Original ID from the source system, preserving the reference to the source document. Examples: 'confluence-page-1234567890' (for Confluence), 'gdrive-file-abc123' (for Google Drive), sha1(original-file-content) (for file uploads) _(minLen=1; maxLen=255)_
      - `id` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
      - `companyId` — string **(required)** — Company ID that owns this document _(minLen=3; maxLen=30)_
      - `dataSourceId` — string **(required)** — ID of the data source containing this document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
      - `createdAt` — string **(required)** — Timestamp when the document was created (ISO 8601 format). Example: 2021-01-01T00:00:00Z
      - `updatedAt` — string **(required)** — Timestamp when the document was last updated (ISO 8601 format). Example: 2021-01-01T00:00:00Z
      - `status` — string **(required)** _(enum: `draft`, `pending`, `processing`, `completed`, `failed`)_
      - `chunksCount` — number — Total number of text chunks the document was split into for semantic search and embedding. Higher numbers indicate more detailed indexing
      - `convertingDuration` — number — Time in milliseconds spent converting the document from its original format to markdown. Only populated after processing
      - `processingDuration` — number — Time in milliseconds spent chunking the document and generating embeddings for semantic search. Only populated after processing completes
      - `errorMessage` — string — Error message describing why document processing failed, if applicable. Only present when status is 'failed'
  - `metadata` — PaginationMetadata **(required)**
    - `total` — number **(required)** — The total number of results.
    - `limit` — number — The number of results per page.
    - `offset` — number — The offset from which to start the results.
- Errors: `400`, `401`, `403`, `404`

#### `POST` `/api/v1/data-sources/{dataSourceId}/documents`

Create a new document for a data source by its ID

- operationId: `CreateDocument`
- **Scopes**: `kb:CreateDocument`
- **Parameters**
  - `dataSourceId` (path) — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `CreateDocumentRequestContent`) **(required)**
  - `title` — string **(required)** — Display title of the document used in search results and UI. Can differ from originalName. Examples: 'Product Installation Guide', 'API Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
  - `url` — string — Optional URL where the document can be accessed or viewed. Used for providing direct links to the source. Example: https://confluence.company.com/wiki/Product_Documentation _(maxLen=1024)_
  - `content` — string — Optional document content in plain text or markdown format. For file uploads, can be the document content.
  - `description` — string — Optional detailed description of the document content and purpose. Helps users understand what the document is about. _(maxLen=2048)_
  - `originalFormat` — string **(required)** — File format/extension of the original document for reference. Examples: 'pdf', 'docx', 'md', 'html', 'txt'. Helps identify source document type _(minLen=1; maxLen=10)_
  - `originalName` — string **(required)** — Original filename or identifier of the source document. Preserves the source document name. Examples: 'product-knowledge-base.pdf', 'installation-guide.docx' _(minLen=1; maxLen=255)_
  - `originalId` — string — Original ID from the source system, preserving the reference to the source document. Examples: 'confluence-page-1234567890' (for Confluence), 'gdrive-file-abc123' (for Google Drive), sha1(original-file-content) (for file uploads) _(minLen=1; maxLen=255)_
  - `metadata` — any — Additional metadata of the document. Example: `{ 'createdAt': '2025-01-01T00:00:00Z', 'updatedAt': '2025-05-01T00:00:00Z', 'createdBy': 'user@example.com' }`
- **Response 201** (`CreateDocumentResponseContent`)
  - `document` — DocumentItem **(required)**
    - `title` — string **(required)** — Display title of the document used in search results and UI. Can differ from originalName. Examples: 'Product Installation Guide', 'API Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
    - `url` — string — Optional URL where the document can be accessed or viewed. Used for providing direct links to the source. Example: https://confluence.company.com/wiki/Product_Documentation _(maxLen=1024)_
    - `content` — string — Optional document content in plain text or markdown format. For file uploads, can be the document content.
    - `description` — string — Optional detailed description of the document content and purpose. Helps users understand what the document is about. _(maxLen=2048)_
    - `originalFormat` — string **(required)** — File format/extension of the original document for reference. Examples: 'pdf', 'docx', 'md', 'html', 'txt'. Helps identify source document type _(minLen=1; maxLen=10)_
    - `originalName` — string **(required)** — Original filename or identifier of the source document. Preserves the source document name. Examples: 'product-knowledge-base.pdf', 'installation-guide.docx' _(minLen=1; maxLen=255)_
    - `originalId` — string — Original ID from the source system, preserving the reference to the source document. Examples: 'confluence-page-1234567890' (for Confluence), 'gdrive-file-abc123' (for Google Drive), sha1(original-file-content) (for file uploads) _(minLen=1; maxLen=255)_
    - `id` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `companyId` — string **(required)** — Company ID that owns this document _(minLen=3; maxLen=30)_
    - `dataSourceId` — string **(required)** — ID of the data source containing this document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `createdAt` — string **(required)** — Timestamp when the document was created (ISO 8601 format). Example: 2021-01-01T00:00:00Z
    - `updatedAt` — string **(required)** — Timestamp when the document was last updated (ISO 8601 format). Example: 2021-01-01T00:00:00Z
    - `status` — string **(required)** _(enum: `draft`, `pending`, `processing`, `completed`, `failed`)_
    - `chunksCount` — number — Total number of text chunks the document was split into for semantic search and embedding. Higher numbers indicate more detailed indexing
    - `convertingDuration` — number — Time in milliseconds spent converting the document from its original format to markdown. Only populated after processing
    - `processingDuration` — number — Time in milliseconds spent chunking the document and generating embeddings for semantic search. Only populated after processing completes
    - `errorMessage` — string — Error message describing why document processing failed, if applicable. Only present when status is 'failed'
- Errors: `400`, `401`, `403`, `404`

#### `GET` `/api/v1/data-sources/{dataSourceId}/documents/{documentId}`

Get a document by its ID

- operationId: `GetDocument`
- **Scopes**: `kb:GetDocument`, `kb:read`
- **Parameters**
  - `dataSourceId` (path) — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `documentId` (path) — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetDocumentResponseContent`)
  - `document` — DocumentItem **(required)**
    - `title` — string **(required)** — Display title of the document used in search results and UI. Can differ from originalName. Examples: 'Product Installation Guide', 'API Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
    - `url` — string — Optional URL where the document can be accessed or viewed. Used for providing direct links to the source. Example: https://confluence.company.com/wiki/Product_Documentation _(maxLen=1024)_
    - `content` — string — Optional document content in plain text or markdown format. For file uploads, can be the document content.
    - `description` — string — Optional detailed description of the document content and purpose. Helps users understand what the document is about. _(maxLen=2048)_
    - `originalFormat` — string **(required)** — File format/extension of the original document for reference. Examples: 'pdf', 'docx', 'md', 'html', 'txt'. Helps identify source document type _(minLen=1; maxLen=10)_
    - `originalName` — string **(required)** — Original filename or identifier of the source document. Preserves the source document name. Examples: 'product-knowledge-base.pdf', 'installation-guide.docx' _(minLen=1; maxLen=255)_
    - `originalId` — string — Original ID from the source system, preserving the reference to the source document. Examples: 'confluence-page-1234567890' (for Confluence), 'gdrive-file-abc123' (for Google Drive), sha1(original-file-content) (for file uploads) _(minLen=1; maxLen=255)_
    - `id` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `companyId` — string **(required)** — Company ID that owns this document _(minLen=3; maxLen=30)_
    - `dataSourceId` — string **(required)** — ID of the data source containing this document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `createdAt` — string **(required)** — Timestamp when the document was created (ISO 8601 format). Example: 2021-01-01T00:00:00Z
    - `updatedAt` — string **(required)** — Timestamp when the document was last updated (ISO 8601 format). Example: 2021-01-01T00:00:00Z
    - `status` — string **(required)** _(enum: `draft`, `pending`, `processing`, `completed`, `failed`)_
    - `chunksCount` — number — Total number of text chunks the document was split into for semantic search and embedding. Higher numbers indicate more detailed indexing
    - `convertingDuration` — number — Time in milliseconds spent converting the document from its original format to markdown. Only populated after processing
    - `processingDuration` — number — Time in milliseconds spent chunking the document and generating embeddings for semantic search. Only populated after processing completes
    - `errorMessage` — string — Error message describing why document processing failed, if applicable. Only present when status is 'failed'
- Errors: `400`, `401`, `403`, `404`

#### `PUT` `/api/v1/data-sources/{dataSourceId}/documents/{documentId}`

Update a document by its ID

- operationId: `UpdateDocument`
- **Scopes**: `kb:UpdateDocument`
- **Parameters**
  - `dataSourceId` (path) — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `documentId` (path) — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `UpdateDocumentRequestContent`)
  - `title` — string — Display title of the document used in search results and UI. Can differ from originalName. Examples: 'Product Installation Guide', 'API Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
  - `url` — string — Optional URL where the document can be accessed or viewed. Used for providing direct links to the source. Example: https://confluence.company.com/wiki/Product_Documentation _(maxLen=1024)_
  - `description` — string — Optional detailed description of the document content and purpose. Helps users understand what the document is about. _(maxLen=2048)_
  - `content` — string — Optional document content in plain text or markdown format. For file uploads, can be the document content.
  - `updatedAt` — string — Timestamp when the document was last updated (ISO 8601 format). Example: 2021-01-01T00:00:00Z
- **Response 200** (`UpdateDocumentResponseContent`)
  - `document` — DocumentItem **(required)**
    - `title` — string **(required)** — Display title of the document used in search results and UI. Can differ from originalName. Examples: 'Product Installation Guide', 'API Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
    - `url` — string — Optional URL where the document can be accessed or viewed. Used for providing direct links to the source. Example: https://confluence.company.com/wiki/Product_Documentation _(maxLen=1024)_
    - `content` — string — Optional document content in plain text or markdown format. For file uploads, can be the document content.
    - `description` — string — Optional detailed description of the document content and purpose. Helps users understand what the document is about. _(maxLen=2048)_
    - `originalFormat` — string **(required)** — File format/extension of the original document for reference. Examples: 'pdf', 'docx', 'md', 'html', 'txt'. Helps identify source document type _(minLen=1; maxLen=10)_
    - `originalName` — string **(required)** — Original filename or identifier of the source document. Preserves the source document name. Examples: 'product-knowledge-base.pdf', 'installation-guide.docx' _(minLen=1; maxLen=255)_
    - `originalId` — string — Original ID from the source system, preserving the reference to the source document. Examples: 'confluence-page-1234567890' (for Confluence), 'gdrive-file-abc123' (for Google Drive), sha1(original-file-content) (for file uploads) _(minLen=1; maxLen=255)_
    - `id` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `companyId` — string **(required)** — Company ID that owns this document _(minLen=3; maxLen=30)_
    - `dataSourceId` — string **(required)** — ID of the data source containing this document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `createdAt` — string **(required)** — Timestamp when the document was created (ISO 8601 format). Example: 2021-01-01T00:00:00Z
    - `updatedAt` — string **(required)** — Timestamp when the document was last updated (ISO 8601 format). Example: 2021-01-01T00:00:00Z
    - `status` — string **(required)** _(enum: `draft`, `pending`, `processing`, `completed`, `failed`)_
    - `chunksCount` — number — Total number of text chunks the document was split into for semantic search and embedding. Higher numbers indicate more detailed indexing
    - `convertingDuration` — number — Time in milliseconds spent converting the document from its original format to markdown. Only populated after processing
    - `processingDuration` — number — Time in milliseconds spent chunking the document and generating embeddings for semantic search. Only populated after processing completes
    - `errorMessage` — string — Error message describing why document processing failed, if applicable. Only present when status is 'failed'
- Errors: `400`, `401`, `403`, `404`

#### `DELETE` `/api/v1/data-sources/{dataSourceId}/documents/{documentId}`

Delete a document by its ID

- operationId: `DeleteDocument`
- **Scopes**: `kb:DeleteDocument`
- **Parameters**
  - `dataSourceId` (path) — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `documentId` (path) — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- Errors: `400`, `401`, `403`, `404`

#### `GET` `/api/v1/data-sources/{dataSourceId}/documents/{documentId}/chunks`

Get the chunks of a document by its ID

- operationId: `GetDocumentChunks`
- **Scopes**: `kb:GetDocumentChunks`, `kb:read`
- **Parameters**
  - `dataSourceId` (path) — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `documentId` (path) — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetDocumentChunksResponseContent`)
  - `chunks` — array **(required)**
    - _array of_ `ChunkItem`
      - `id` — string **(required)** — The ID of the chunk. Example: 123e4567-e89b-12d3-a456-426614174000 _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
      - `documentId` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
      - `content` — string **(required)**
      - `createdAt` — string **(required)**
      - `updatedAt` — string **(required)**
- Errors: `400`, `401`, `403`, `404`

#### `GET` `/api/v1/data-sources/{dataSourceId}/documents/{documentId}/download-url`

Get a presigned URL for downloading the original file of the document

- operationId: `GetDocumentDownloadUrl`
- **Scopes**: `kb:GetDocumentDownloadUrl`, `kb:read`
- **Parameters**
  - `dataSourceId` (path) — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `documentId` (path) — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetDocumentDownloadUrlResponseContent`)
  - `downloadUrl` — string **(required)**
- Errors: `400`, `401`, `403`, `404`

#### `GET` `/api/v1/data-sources/{dataSourceId}/documents/{documentId}/markdown`

Get the markdown content of a document by its ID

- operationId: `GetDocumentMarkdown`
- **Scopes**: `kb:GetDocumentMarkdown`, `kb:read`
- **Parameters**
  - `dataSourceId` (path) — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `documentId` (path) — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetDocumentMarkdownResponseContent`)
  - `markdown` — string **(required)**
- Errors: `400`, `401`, `403`, `404`

#### `GET` `/api/v1/data-sources/{dataSourceId}/documents/{documentId}/upload-url`

Get a presigned URL for uploading the original file of the document. You must upload the file to this URL using the PUT method.

- operationId: `GetDocumentUploadUrl`
- **Scopes**: `kb:GetDocumentUploadUrl`
- **Parameters**
  - `dataSourceId` (path) — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `documentId` (path) — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetDocumentUploadUrlResponseContent`)
  - `uploadUrl` — string **(required)**
- Errors: `400`, `401`, `403`, `404`

#### `GET` `/api/v1/data-sources/{dataSourceId}/documents/{documentId}/with-content-and-chunks`

Get a document by its ID with its content and chunks

- operationId: `GetDocumentWithContentAndChunks`
- **Scopes**: `kb:GetDocumentWithContentAndChunks`, `kb:read`
- **Parameters**
  - `dataSourceId` (path) — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `documentId` (path) — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetDocumentWithContentAndChunksResponseContent`)
  - `document` — DocumentItem **(required)**
    - `title` — string **(required)** — Display title of the document used in search results and UI. Can differ from originalName. Examples: 'Product Installation Guide', 'API Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
    - `url` — string — Optional URL where the document can be accessed or viewed. Used for providing direct links to the source. Example: https://confluence.company.com/wiki/Product_Documentation _(maxLen=1024)_
    - `content` — string — Optional document content in plain text or markdown format. For file uploads, can be the document content.
    - `description` — string — Optional detailed description of the document content and purpose. Helps users understand what the document is about. _(maxLen=2048)_
    - `originalFormat` — string **(required)** — File format/extension of the original document for reference. Examples: 'pdf', 'docx', 'md', 'html', 'txt'. Helps identify source document type _(minLen=1; maxLen=10)_
    - `originalName` — string **(required)** — Original filename or identifier of the source document. Preserves the source document name. Examples: 'product-knowledge-base.pdf', 'installation-guide.docx' _(minLen=1; maxLen=255)_
    - `originalId` — string — Original ID from the source system, preserving the reference to the source document. Examples: 'confluence-page-1234567890' (for Confluence), 'gdrive-file-abc123' (for Google Drive), sha1(original-file-content) (for file uploads) _(minLen=1; maxLen=255)_
    - `id` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `companyId` — string **(required)** — Company ID that owns this document _(minLen=3; maxLen=30)_
    - `dataSourceId` — string **(required)** — ID of the data source containing this document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `createdAt` — string **(required)** — Timestamp when the document was created (ISO 8601 format). Example: 2021-01-01T00:00:00Z
    - `updatedAt` — string **(required)** — Timestamp when the document was last updated (ISO 8601 format). Example: 2021-01-01T00:00:00Z
    - `status` — string **(required)** _(enum: `draft`, `pending`, `processing`, `completed`, `failed`)_
    - `chunksCount` — number — Total number of text chunks the document was split into for semantic search and embedding. Higher numbers indicate more detailed indexing
    - `convertingDuration` — number — Time in milliseconds spent converting the document from its original format to markdown. Only populated after processing
    - `processingDuration` — number — Time in milliseconds spent chunking the document and generating embeddings for semantic search. Only populated after processing completes
    - `errorMessage` — string — Error message describing why document processing failed, if applicable. Only present when status is 'failed'
  - `content` — string **(required)**
  - `chunks` — array **(required)**
    - _array of_ `ChunkItem`
      - `id` — string **(required)** — The ID of the chunk. Example: 123e4567-e89b-12d3-a456-426614174000 _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
      - `documentId` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
      - `content` — string **(required)**
      - `createdAt` — string **(required)**
      - `updatedAt` — string **(required)**
- Errors: `400`, `401`, `403`, `404`

### KnowledgeBases

#### `GET` `/api/v1/knowledge-bases`

List all knowledge bases for the current company

- operationId: `ListKnowledgeBases`
- **Scopes**: `kb:ListKnowledgeBases`, `kb:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`ListKnowledgeBasesResponseContent`)
  - `knowledgeBases` — array **(required)**
    - _array of_ `KnowledgeBaseItem`
      - `name` — string **(required)** — Descriptive name for the knowledge base. Used for identification in the UI and APIs. Examples: 'Product Knowledge Base', 'Support Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
      - `description` — string — Optional detailed description of the knowledge base content and purpose. Helps users understand what topics are covered. Examples: 'Comprehensive product documentation and service guides', 'Internal technical documentation'. Length: 0-1000 characters _(maxLen=1000)_
      - `dataSources` — array **(required)** — List of data source IDs that provide content for this knowledge base. Can include Confluence, Google Drive, file uploads, and proxy sources. Empty list results in no searchable content
        - _array of_ `string`
      - `id` — string **(required)** — Unique identifier of the knowledge base _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
      - `companyId` — string **(required)** — Company ID that owns this knowledge base _(minLen=3; maxLen=30)_
      - `createdAt` — string **(required)** — Timestamp when the knowledge base was created (ISO 8601 format). Example: 2021-01-01T00:00:00Z
      - `updatedAt` — string **(required)** — Timestamp when the knowledge base was last updated (ISO 8601 format). Example: 2021-01-01T00:00:00Z
- Errors: `400`, `401`, `403`, `404`

#### `POST` `/api/v1/knowledge-bases`

Create a new knowledge base

- operationId: `CreateKnowledgeBase`
- **Scopes**: `kb:CreateKnowledgeBase`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `CreateKnowledgeBaseRequestContent`) **(required)**
  - `name` — string **(required)** — Descriptive name for the knowledge base. Used for identification in the UI and APIs. Examples: 'Product Knowledge Base', 'Support Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
  - `description` — string — Optional detailed description of the knowledge base content and purpose. Helps users understand what topics are covered. Examples: 'Comprehensive product documentation and service guides', 'Internal technical documentation'. Length: 0-1000 characters _(maxLen=1000)_
  - `dataSources` — array **(required)** — List of data source IDs that provide content for this knowledge base. Can include Confluence, Google Drive, file uploads, and proxy sources. Empty list results in no searchable content
    - _array of_ `string`
- **Response 201** (`CreateKnowledgeBaseResponseContent`)
  - `knowledgeBase` — KnowledgeBaseItem **(required)**
    - `name` — string **(required)** — Descriptive name for the knowledge base. Used for identification in the UI and APIs. Examples: 'Product Knowledge Base', 'Support Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
    - `description` — string — Optional detailed description of the knowledge base content and purpose. Helps users understand what topics are covered. Examples: 'Comprehensive product documentation and service guides', 'Internal technical documentation'. Length: 0-1000 characters _(maxLen=1000)_
    - `dataSources` — array **(required)** — List of data source IDs that provide content for this knowledge base. Can include Confluence, Google Drive, file uploads, and proxy sources. Empty list results in no searchable content
      - _array of_ `string`
    - `id` — string **(required)** — Unique identifier of the knowledge base _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `companyId` — string **(required)** — Company ID that owns this knowledge base _(minLen=3; maxLen=30)_
    - `createdAt` — string **(required)** — Timestamp when the knowledge base was created (ISO 8601 format). Example: 2021-01-01T00:00:00Z
    - `updatedAt` — string **(required)** — Timestamp when the knowledge base was last updated (ISO 8601 format). Example: 2021-01-01T00:00:00Z
- Errors: `400`, `401`, `403`, `404`

#### `GET` `/api/v1/knowledge-bases/{knowledgeBaseId}`

Get a knowledge base by its ID

- operationId: `GetKnowledgeBase`
- **Scopes**: `kb:GetKnowledgeBase`, `kb:read`
- **Parameters**
  - `knowledgeBaseId` (path) — string **(required)** — Unique identifier of the knowledge base _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetKnowledgeBaseResponseContent`)
  - `knowledgeBase` — KnowledgeBaseItem **(required)**
    - `name` — string **(required)** — Descriptive name for the knowledge base. Used for identification in the UI and APIs. Examples: 'Product Knowledge Base', 'Support Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
    - `description` — string — Optional detailed description of the knowledge base content and purpose. Helps users understand what topics are covered. Examples: 'Comprehensive product documentation and service guides', 'Internal technical documentation'. Length: 0-1000 characters _(maxLen=1000)_
    - `dataSources` — array **(required)** — List of data source IDs that provide content for this knowledge base. Can include Confluence, Google Drive, file uploads, and proxy sources. Empty list results in no searchable content
      - _array of_ `string`
    - `id` — string **(required)** — Unique identifier of the knowledge base _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `companyId` — string **(required)** — Company ID that owns this knowledge base _(minLen=3; maxLen=30)_
    - `createdAt` — string **(required)** — Timestamp when the knowledge base was created (ISO 8601 format). Example: 2021-01-01T00:00:00Z
    - `updatedAt` — string **(required)** — Timestamp when the knowledge base was last updated (ISO 8601 format). Example: 2021-01-01T00:00:00Z
- Errors: `400`, `401`, `403`, `404`

#### `PUT` `/api/v1/knowledge-bases/{knowledgeBaseId}`

Update a knowledge base by its ID

- operationId: `UpdateKnowledgeBase`
- **Scopes**: `kb:UpdateKnowledgeBase`
- **Parameters**
  - `knowledgeBaseId` (path) — string **(required)** — Unique identifier of the knowledge base _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `UpdateKnowledgeBaseRequestContent`) **(required)**
  - `name` — string **(required)** — Descriptive name for the knowledge base. Used for identification in the UI and APIs. Examples: 'Product Knowledge Base', 'Support Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
  - `description` — string — Optional detailed description of the knowledge base content and purpose. Helps users understand what topics are covered. Examples: 'Comprehensive product documentation and service guides', 'Internal technical documentation'. Length: 0-1000 characters _(maxLen=1000)_
  - `dataSources` — array **(required)** — List of data source IDs that provide content for this knowledge base. Can include Confluence, Google Drive, file uploads, and proxy sources. Empty list results in no searchable content
    - _array of_ `string`
- **Response 200** (`UpdateKnowledgeBaseResponseContent`)
  - `knowledgeBase` — KnowledgeBaseItem **(required)**
    - `name` — string **(required)** — Descriptive name for the knowledge base. Used for identification in the UI and APIs. Examples: 'Product Knowledge Base', 'Support Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
    - `description` — string — Optional detailed description of the knowledge base content and purpose. Helps users understand what topics are covered. Examples: 'Comprehensive product documentation and service guides', 'Internal technical documentation'. Length: 0-1000 characters _(maxLen=1000)_
    - `dataSources` — array **(required)** — List of data source IDs that provide content for this knowledge base. Can include Confluence, Google Drive, file uploads, and proxy sources. Empty list results in no searchable content
      - _array of_ `string`
    - `id` — string **(required)** — Unique identifier of the knowledge base _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `companyId` — string **(required)** — Company ID that owns this knowledge base _(minLen=3; maxLen=30)_
    - `createdAt` — string **(required)** — Timestamp when the knowledge base was created (ISO 8601 format). Example: 2021-01-01T00:00:00Z
    - `updatedAt` — string **(required)** — Timestamp when the knowledge base was last updated (ISO 8601 format). Example: 2021-01-01T00:00:00Z
- Errors: `400`, `401`, `403`, `404`

#### `DELETE` `/api/v1/knowledge-bases/{knowledgeBaseId}`

Delete a knowledge base by its ID

- operationId: `DeleteKnowledgeBase`
- **Scopes**: `kb:DeleteKnowledgeBase`
- **Parameters**
  - `knowledgeBaseId` (path) — string **(required)** — Unique identifier of the knowledge base _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- Errors: `400`, `401`, `403`, `404`

### Search

#### `POST` `/api/v1/knowledge-bases/generate-answer`

Query a knowledge base by its ID and return the answer from the LLM

- operationId: `GenerateSearchAnswer`
- **Scopes**: `kb:GenerateSearchAnswer`, `kb:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `GenerateSearchAnswerRequestContent`) **(required)**
  - `searchQuery` — string **(required)** — The question or query to be answered using the knowledge base. The LLM will search the knowledge base and generate an answer based on found results. Example: 'What is the product knowledge base?'
  - `searchResults` — array **(required)** — The search results to be used to generate the answer. The LLM will use the search results to generate an answer based on the found results.
    - _array of_ `SearchKnowledgeBaseResultItem`
      - `chunkId` — string **(required)** — The ID of the chunk. Example: 123e4567-e89b-12d3-a456-426614174000 _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
      - `documentId` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
      - `documentTitle` — string **(required)**
      - `documentUrl` — string **(required)**
      - `dataSourceId` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
      - `dataSourceType` — string **(required)** _(enum: `files`, `confluence`, `gdrive`, `website`)_
      - `score` — number **(required)** — The total score of the result, calculated from the semantic search score and the full-text search score. _(format=double)_
      - `fullTextScore` — number — The score of the result, calculated from the full-text bm25 search score. _(format=double)_
      - `semanticScore` — number — The score of the result, calculated from the semantic vector search score. _(format=double)_
      - `documentHierarchy` — array — The hierarchy of the document. The hierarchy is a list of document IDs that are the parents of the current document. The hierarchy is used to build the document hierarchy in the search results.
        - _array of_ `string`
      - `content` — string **(required)**
      - `metadata` — any — The metadata of the document.
  - `model` — string — The specific provider and model identifier. Examples: 'openai://gpt-4o' or 'openai://gpt-4o-mini' for OpenAI, 'mistral://mistral-small-2506' for Mistral. Check provider documentation for available models
  - `temperature` — number — Controls answer randomness and creativity (0.0-1.0). Low values (0.0-0.3) produce consistent, deterministic answers. High values (0.7-1.0) produce more diverse and creative responses. Defaults to 0.3 for factual consistency _(default=0.3; format=double; min=0; max=1)_
  - `maxOutputTokens` — number — Maximum number of tokens in the generated answer (1-10000). Higher values allow longer, more detailed answers. Lower values force concise responses. Defaults to 1000 tokens. Note: higher values increase latency and cost _(default=1000; min=1; max=10000)_
  - `systemPrompt` — string — Optional system prompt to customize LLM behavior and context. Sets instructions for how the LLM should answer questions. Example: 'You are a helpful technical support assistant. Answer only based on the provided knowledge base. If information is not found, say "I don't have this information in the knowledge base."'
- **Response 200** (`GenerateSearchAnswerResponseContent`)
  - `answer` — string **(required)**
  - `metadata` — AnswerMetadata **(required)**
    - `model` — string **(required)**
    - `inputTokens` — number **(required)**
    - `outputTokens` — number **(required)**
    - `duration` — number **(required)**
  - `sources` — array **(required)**
    - _array of_ `SearchKnowledgeBaseResultItem`
      - `chunkId` — string **(required)** — The ID of the chunk. Example: 123e4567-e89b-12d3-a456-426614174000 _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
      - `documentId` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
      - `documentTitle` — string **(required)**
      - `documentUrl` — string **(required)**
      - `dataSourceId` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
      - `dataSourceType` — string **(required)** _(enum: `files`, `confluence`, `gdrive`, `website`)_
      - `score` — number **(required)** — The total score of the result, calculated from the semantic search score and the full-text search score. _(format=double)_
      - `fullTextScore` — number — The score of the result, calculated from the full-text bm25 search score. _(format=double)_
      - `semanticScore` — number — The score of the result, calculated from the semantic vector search score. _(format=double)_
      - `documentHierarchy` — array — The hierarchy of the document. The hierarchy is a list of document IDs that are the parents of the current document. The hierarchy is used to build the document hierarchy in the search results.
        - _array of_ `string`
      - `content` — string **(required)**
      - `metadata` — any — The metadata of the document.
- Errors: `400`, `401`, `403`, `404`

#### `POST` `/api/v1/knowledge-bases/{knowledgeBaseId}/search`

Search a knowledge base by its ID and return the chunks that match the query with its score

- operationId: `SearchKnowledgeBase`
- **Scopes**: `kb:SearchKnowledgeBase`, `kb:read`
- **Parameters**
  - `knowledgeBaseId` (path) — string **(required)** — Unique identifier of the knowledge base _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `SearchKnowledgeBaseRequestContent`) **(required)**
  - `query` — string **(required)** — The search query string. Can be a single keyword or a natural language question. Example: 'What is the product knowledge base?'
  - `searchStrategy` — object
  - `searchLimit` — number — Maximum number of search results to return. Controls the size of the result set. Valid range: 1-50. Defaults to 10 if not specified. Higher values return more results but may include less relevant matches _(default=10; min=1; max=50)_
  - `searchThreshold` — object
  - `useQueryOptimization` — boolean — Whether to optimize and transform the input query using advanced NLP techniques before searching. Improves search quality for complex or poorly phrased queries. Defaults to false. Set to true for better results with natural language questions _(default=False)_
  - `sessionUser` — string — The user who performs the search in the knowledge base. Example: user@example.com or Jon Doe _(default=unknown; minLen=1; maxLen=100)_
  - `sessionUri` — string — The session URI. Used for tracking and analytics purposes. Example: `chatbots://{agentId}/id-of-chat-session/id-of-message` _(default=unknown; minLen=1; maxLen=255)_
- **Response 200** (`SearchKnowledgeBaseResponseContent`)
  - `results` — array **(required)**
    - _array of_ `SearchKnowledgeBaseResultItem`
      - `chunkId` — string **(required)** — The ID of the chunk. Example: 123e4567-e89b-12d3-a456-426614174000 _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
      - `documentId` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
      - `documentTitle` — string **(required)**
      - `documentUrl` — string **(required)**
      - `dataSourceId` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
      - `dataSourceType` — string **(required)** _(enum: `files`, `confluence`, `gdrive`, `website`)_
      - `score` — number **(required)** — The total score of the result, calculated from the semantic search score and the full-text search score. _(format=double)_
      - `fullTextScore` — number — The score of the result, calculated from the full-text bm25 search score. _(format=double)_
      - `semanticScore` — number — The score of the result, calculated from the semantic vector search score. _(format=double)_
      - `documentHierarchy` — array — The hierarchy of the document. The hierarchy is a list of document IDs that are the parents of the current document. The hierarchy is used to build the document hierarchy in the search results.
        - _array of_ `string`
      - `content` — string **(required)**
      - `metadata` — any — The metadata of the document.
  - `metadata` — SearchResultMetadata **(required)**
    - `sessionId` — string **(required)**
    - `duration` — number **(required)**
- Errors: `400`, `401`, `403`, `404`

### History

#### `POST` `/api/v1/knowledge-bases/history/search-queries`

You can use this endpoint to retrieve the search history.

- operationId: `ListSearchQueriesHistory`
- **Scopes**: `kb:ListSearchQueriesHistory`, `kb:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `limit` (query) — number _(default=50; min=1; max=500)_
  - `offset` (query) — number _(default=0; min=0)_
  - `sort` (query) — string — Sort order of the results. If there is a '-' prefix, the results will be sorted in descending order. Otherwise, the results will be sorted in ascending order. Example: '-createdAt' will sort the results by createdAt in descending order. 'createdAt' will sort the results by createdAt in ascending order. _(default=-createdAt; pattern=^-?[a-zA-Z0-9_]{1,32}$)_
- **Request body** (`application/json` — `ListSearchQueriesHistoryRequestContent`) **(required)**
  - `filter` — SearchHistoryFilter **(required)**
    - `knowledgeBaseId` — string — Filter history by the knowledge base ID. _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `dataSourceId` — string — Filter history by the data source ID. _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `sessionId` — string — Filter history by the internal session ID. _(minLen=1; maxLen=255)_
    - `sessionUri` — string — Filter history by the session URI. Used for tracking and analytics purposes. Example: `chatbots://{agentId}/id-of-chat-session/id-of-message` _(minLen=1; maxLen=255)_
    - `sessionUser` — string — Filter history by the user who performs the search in the knowledge base. Example: user@example.com _(minLen=1; maxLen=100)_
    - `withEmptyResults` — boolean — Whether to include the history results with empty results. _(default=False)_
  - `search` — string — The search query string for filtering the history results. _(pattern=^[\p{L}0-9 \-_]{3,32}$)_
  - `withContent` — boolean — Whether to include the content of the chunks in the history results. _(default=False)_
- **Response 200** (`ListSearchQueriesHistoryResponseContent`)
  - `history` — array **(required)**
    - _array of_ `SearchHistoryItem`
      - `sessionId` — string **(required)**
      - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
      - `request` — SearchHistoryRequest **(required)**
        - `query` — string **(required)**
        - `sessionUser` — string **(required)** _(minLen=1; maxLen=100)_
        - `sessionUri` — string **(required)** _(minLen=1; maxLen=255)_
        - `knowledgeBaseId` — string **(required)** — Unique identifier of the knowledge base _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
        - `searchStrategy` — string **(required)** _(enum: `bm25`, `vector`, `hybrid`)_
        - `searchLimit` — number **(required)**
        - `searchThreshold` — number **(required)** _(format=double)_
      - `stages` — SearchHistoryStages **(required)**
        - `overall` — SearchHistoryOverallStage **(required)**
          - `startTime` — number **(required)**
          - `endTime` — number **(required)**
          - `duration` — number **(required)**
        - `transformQuery` — SearchHistoryTransformQueryStage
          - `startTime` — number **(required)**
          - `endTime` — number **(required)**
          - `duration` — number **(required)**
          - `model` — string **(required)**
          - `inputTokens` — number **(required)**
          - `outputTokens` — number **(required)**
          - `transformedQuery` — string **(required)**
        - `generateQueryEmbedding` — SearchHistoryEmbeddingStage **(required)**
          - `startTime` — number **(required)**
          - `endTime` — number **(required)**
          - `duration` — number **(required)**
          - `model` — string **(required)**
          - `inputTokens` — number **(required)**
          - `outputTokens` — number **(required)**
        - `search` — SearchHistorySearchStage **(required)**
          - `startTime` — number **(required)**
          - `endTime` — number **(required)**
          - `duration` — number **(required)**
        - `enrichData` — SearchEnrichDataStage
          - `startTime` — number **(required)**
          - `endTime` — number **(required)**
          - `duration` — number **(required)**
      - `results` — array **(required)**
        - _array of_ `SearchHistoryResultItem`
          - `chunkId` — string **(required)** — The ID of the chunk. Example: 123e4567-e89b-12d3-a456-426614174000 _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
          - `documentId` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
          - `documentTitle` — string **(required)**
          - `documentUrl` — string **(required)**
          - `dataSourceId` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
          - `dataSourceType` — string **(required)** _(enum: `files`, `confluence`, `gdrive`, `website`)_
          - `score` — number **(required)** — The total score of the result, calculated from the semantic search score and the full-text search score. _(format=double)_
          - `fullTextScore` — number — The score of the result, calculated from the full-text bm25 search score. _(format=double)_
          - `semanticScore` — number — The score of the result, calculated from the semantic vector search score. _(format=double)_
          - `documentHierarchy` — array — The hierarchy of the document. The hierarchy is a list of document IDs that are the parents of the current document. The hierarchy is used to build the document hierarchy in the search results.
            - _array of_ `string`
          - `content` — string
      - `createdAt` — string **(required)**
      - `totalDuration` — number **(required)**
      - `resultsCount` — number **(required)**
  - `metadata` — PaginationMetadata **(required)**
    - `total` — number **(required)** — The total number of results.
    - `limit` — number — The number of results per page.
    - `offset` — number — The offset from which to start the results.
- Errors: `400`, `401`, `403`, `404`

#### `POST` `/api/v1/knowledge-bases/history/statistics`

You can use this endpoint to retrieve the search history statistics.

- operationId: `ListHistoryStatistics`
- **Scopes**: `kb:ListHistoryStatistics`, `kb:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `ListHistoryStatisticsRequestContent`) **(required)**
  - `filter` — HistoryStatisticsFilter **(required)**
    - `knowledgeBaseIds` — array — Filter history by the knowledge base IDs.
      - _array of_ `string`
    - `dataSourceIds` — array — Filter history by the data source IDs.
      - _array of_ `string`
    - `daysBack` — number — Number of days to look back for recent statistics. If not specified, defaults to 7 days. _(default=7; min=1; max=30)_
- **Response 200** (`ListHistoryStatisticsResponseContent`)
  - `statistics` — HistoryStatistics **(required)**
    - `totalRequests` — number **(required)** — Total number of all search requests (all time)
    - `recentRequests` — number **(required)** — Number of search requests in the last N days (where N is daysBack)
    - `totalUniqueUsers` — number **(required)** — Total number of unique users (all time)
    - `recentUniqueUsers` — number **(required)** — Number of unique users in the last N days
    - `noResultsRequests` — number **(required)** — Number of requests with no results (in the last N days if daysBack specified, otherwise all time)
    - `dailyBreakdown` — array — Daily breakdown of statistics for the last N days. Only present if daysBack is specified.
      - _array of_ `DailyGlobalStatistics`
        - `date` — string **(required)** — Date in format yyyy-MM-dd
        - `requests` — number **(required)** — Number of search requests on this day
        - `uniqueUsers` — number **(required)** — Number of unique users on this day
        - `noResultsRequests` — number **(required)** — Number of requests with no results on this day
    - `knowledgeBases` — array — Statistics for each knowledge base
      - _array of_ `KnowledgeBaseStatistics`
        - `knowledgeBaseId` — string **(required)** — Unique identifier of the knowledge base _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
        - `searchDailyBreakdown` — array **(required)**
          - _array of_ `DailySearchStatistics`
            - `date` — string **(required)** — Date in format yyyy-MM-dd
            - `requests` — number **(required)** — Number of search requests
    - `dataSources` — array — Statistics for each data source
      - _array of_ `DataSourceStatistics`
        - `dataSourceId` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
        - `searchDailyBreakdown` — array **(required)**
          - _array of_ `DailySearchStatistics`
            - `date` — string **(required)** — Date in format yyyy-MM-dd
            - `requests` — number **(required)** — Number of search requests
        - `documentsCount` — number **(required)**
        - `documentsStatistics` — array **(required)**
          - _array of_ `DocumentsStatistics`
            - `status` — string **(required)** _(enum: `draft`, `pending`, `processing`, `completed`, `failed`)_
            - `count` — number **(required)**
        - `chunksCount` — number **(required)**
- Errors: `400`, `401`, `403`, `404`

### Schemas appendix — Knowledge Base API

<details><summary>106 component schemas</summary>

**`AnswerMetadata`**

- `model` — string **(required)**
- `inputTokens` — number **(required)**
- `outputTokens` — number **(required)**
- `duration` — number **(required)**

**`ChunkItem`**

- `id` — string **(required)** — The ID of the chunk. Example: 123e4567-e89b-12d3-a456-426614174000 _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
- `documentId` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
- `content` — string **(required)**
- `createdAt` — string **(required)**
- `updatedAt` — string **(required)**

**`CloneDataSourceResponseContent`**

- `dataSourceId` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_

**`ConfigureDataSourceRequestContent`**

- `config` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`confluence`**
      - `confluence` — ConfluenceConfig **(required)**
        - `baseUrl` — string **(required)** — The base URL of your Confluence Cloud or Server instance. Must be a valid HTTPS URL. Example: https://your-company.atlassian.net
        - `username` — string **(required)** — The email address or username associated with the Confluence account used for authentication
        - `apiKey` — string **(required)** — The API token or password for Confluence authentication. For Cloud instances, use an API token; for Server instances, use the account password
        - `spaceId` — string **(required)** — The Confluence space key or ID to synchronize. All pages within this space will be included unless explicitly excluded
        - `pages` — ConfluencePagesConfig
          - _(nesting depth limit — see `ConfluencePagesConfig` in the Schemas appendix)_
    - **`gdrive`**
      - `gdrive` — GDriveConfig **(required)**
        - `nangoConnectionId` — string **(required)** — The Nango integration connection ID for Google Drive. This establishes the OAuth connection to access the Drive account
        - `folders` — GDriveFoldersConfig **(required)**
          - _(nesting depth limit — see `GDriveFoldersConfig` in the Schemas appendix)_
    - **`website`**
      - `website` — WebsiteConfig **(required)**
        - `urls` — array **(required)** — Starting page URLs of the website to index. Must be https and resolve to a public address. The v1 console configures exactly one, but the field is a list so additional starting points can be added without a breaking change
          - _array of_ `string`
        - `maxPages` — number — Upper bound on how many pages may be selected for indexing. Server-side limits still apply and take precedence _(min=1; max=2000)_
        - `pages` — WebsitePagesConfig
          - _(nesting depth limit — see `WebsitePagesConfig` in the Schemas appendix)_
    - **`files`**
      - `files` — any **(required)**
- `syncSchedule` — object

**`ConfigureDataSourceResponseContent`**

- `dataSource` — DataSourceItem **(required)**
  - `name` — string **(required)** — Descriptive name for the data source. Used for identification and display in the UI. Examples: 'Product Confluence', 'Customer Service Docs', 'Engineering Wikis'. Length: 2-100 characters _(minLen=2; maxLen=100)_
  - `description` — string — Optional detailed description of the data source content and purpose. Helps users understand what data is included. Examples: 'Contains product documentation and service guides from Confluence', 'Customer service articles synced from Zendesk'. Length: 0-1000 characters _(maxLen=1000)_
  - `type` — string **(required)** _(enum: `files`, `confluence`, `gdrive`, `website`)_
  - `config` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`confluence`**
        - `confluence` — ConfluenceConfig **(required)**
          - _(nesting depth limit — see `ConfluenceConfig` in the Schemas appendix)_
      - **`gdrive`**
        - `gdrive` — GDriveConfig **(required)**
          - _(nesting depth limit — see `GDriveConfig` in the Schemas appendix)_
      - **`website`**
        - `website` — WebsiteConfig **(required)**
          - _(nesting depth limit — see `WebsiteConfig` in the Schemas appendix)_
      - **`files`**
        - `files` — any **(required)**
  - `syncSchedule` — object
  - `id` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `companyId` — string **(required)** — Company ID that owns this data source _(minLen=3; maxLen=30)_
  - `createdAt` — string **(required)** — Timestamp when the data source was created (ISO 8601 format). Example: 2025-01-01T00:00:00Z
  - `updatedAt` — string **(required)** — Timestamp when the data source was last updated (ISO 8601 format). Example: 2025-01-01T00:00:00Z

**`ConfluenceConfig`**

- `baseUrl` — string **(required)** — The base URL of your Confluence Cloud or Server instance. Must be a valid HTTPS URL. Example: https://your-company.atlassian.net
- `username` — string **(required)** — The email address or username associated with the Confluence account used for authentication
- `apiKey` — string **(required)** — The API token or password for Confluence authentication. For Cloud instances, use an API token; for Server instances, use the account password
- `spaceId` — string **(required)** — The Confluence space key or ID to synchronize. All pages within this space will be included unless explicitly excluded
- `pages` — ConfluencePagesConfig
  - `enabled` — array **(required)** — List of Confluence page IDs that should be included in the synchronization
    - _array of_ `string`
  - `disabled` — array **(required)** — List of Confluence page IDs that should be explicitly excluded from the synchronization
    - _array of_ `string`

**`ConfluencePagesConfig`**

- `enabled` — array **(required)** — List of Confluence page IDs that should be included in the synchronization
  - _array of_ `string`
- `disabled` — array **(required)** — List of Confluence page IDs that should be explicitly excluded from the synchronization
  - _array of_ `string`

**`ConfluenceSpaceType`**

- string _(enum: `global`, `collaboration`, `knowledge_base`, `personal`, `system`, `onboarding`)_

**`CreateDataSourceRequestContent`**

- `name` — string **(required)** — Descriptive name for the data source. Used for identification and display in the UI. Examples: 'Product Confluence', 'Customer Service Docs', 'Engineering Wikis'. Length: 2-100 characters _(minLen=2; maxLen=100)_
- `description` — string — Optional detailed description of the data source content and purpose. Helps users understand what data is included. Examples: 'Contains product documentation and service guides from Confluence', 'Customer service articles synced from Zendesk'. Length: 0-1000 characters _(maxLen=1000)_
- `type` — string **(required)** _(enum: `files`, `confluence`, `gdrive`, `website`)_

**`CreateDataSourceResponseContent`**

- `dataSource` — DataSourceItem **(required)**
  - `name` — string **(required)** — Descriptive name for the data source. Used for identification and display in the UI. Examples: 'Product Confluence', 'Customer Service Docs', 'Engineering Wikis'. Length: 2-100 characters _(minLen=2; maxLen=100)_
  - `description` — string — Optional detailed description of the data source content and purpose. Helps users understand what data is included. Examples: 'Contains product documentation and service guides from Confluence', 'Customer service articles synced from Zendesk'. Length: 0-1000 characters _(maxLen=1000)_
  - `type` — string **(required)** _(enum: `files`, `confluence`, `gdrive`, `website`)_
  - `config` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`confluence`**
        - `confluence` — ConfluenceConfig **(required)**
          - _(nesting depth limit — see `ConfluenceConfig` in the Schemas appendix)_
      - **`gdrive`**
        - `gdrive` — GDriveConfig **(required)**
          - _(nesting depth limit — see `GDriveConfig` in the Schemas appendix)_
      - **`website`**
        - `website` — WebsiteConfig **(required)**
          - _(nesting depth limit — see `WebsiteConfig` in the Schemas appendix)_
      - **`files`**
        - `files` — any **(required)**
  - `syncSchedule` — object
  - `id` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `companyId` — string **(required)** — Company ID that owns this data source _(minLen=3; maxLen=30)_
  - `createdAt` — string **(required)** — Timestamp when the data source was created (ISO 8601 format). Example: 2025-01-01T00:00:00Z
  - `updatedAt` — string **(required)** — Timestamp when the data source was last updated (ISO 8601 format). Example: 2025-01-01T00:00:00Z

**`CreateDocumentRequestContent`**

- `title` — string **(required)** — Display title of the document used in search results and UI. Can differ from originalName. Examples: 'Product Installation Guide', 'API Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
- `url` — string — Optional URL where the document can be accessed or viewed. Used for providing direct links to the source. Example: https://confluence.company.com/wiki/Product_Documentation _(maxLen=1024)_
- `content` — string — Optional document content in plain text or markdown format. For file uploads, can be the document content.
- `description` — string — Optional detailed description of the document content and purpose. Helps users understand what the document is about. _(maxLen=2048)_
- `originalFormat` — string **(required)** — File format/extension of the original document for reference. Examples: 'pdf', 'docx', 'md', 'html', 'txt'. Helps identify source document type _(minLen=1; maxLen=10)_
- `originalName` — string **(required)** — Original filename or identifier of the source document. Preserves the source document name. Examples: 'product-knowledge-base.pdf', 'installation-guide.docx' _(minLen=1; maxLen=255)_
- `originalId` — string — Original ID from the source system, preserving the reference to the source document. Examples: 'confluence-page-1234567890' (for Confluence), 'gdrive-file-abc123' (for Google Drive), sha1(original-file-content) (for file uploads) _(minLen=1; maxLen=255)_
- `metadata` — any — Additional metadata of the document. Example: `{ 'createdAt': '2025-01-01T00:00:00Z', 'updatedAt': '2025-05-01T00:00:00Z', 'createdBy': 'user@example.com' }`

**`CreateDocumentResponseContent`**

- `document` — DocumentItem **(required)**
  - `title` — string **(required)** — Display title of the document used in search results and UI. Can differ from originalName. Examples: 'Product Installation Guide', 'API Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
  - `url` — string — Optional URL where the document can be accessed or viewed. Used for providing direct links to the source. Example: https://confluence.company.com/wiki/Product_Documentation _(maxLen=1024)_
  - `content` — string — Optional document content in plain text or markdown format. For file uploads, can be the document content.
  - `description` — string — Optional detailed description of the document content and purpose. Helps users understand what the document is about. _(maxLen=2048)_
  - `originalFormat` — string **(required)** — File format/extension of the original document for reference. Examples: 'pdf', 'docx', 'md', 'html', 'txt'. Helps identify source document type _(minLen=1; maxLen=10)_
  - `originalName` — string **(required)** — Original filename or identifier of the source document. Preserves the source document name. Examples: 'product-knowledge-base.pdf', 'installation-guide.docx' _(minLen=1; maxLen=255)_
  - `originalId` — string — Original ID from the source system, preserving the reference to the source document. Examples: 'confluence-page-1234567890' (for Confluence), 'gdrive-file-abc123' (for Google Drive), sha1(original-file-content) (for file uploads) _(minLen=1; maxLen=255)_
  - `id` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `companyId` — string **(required)** — Company ID that owns this document _(minLen=3; maxLen=30)_
  - `dataSourceId` — string **(required)** — ID of the data source containing this document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `createdAt` — string **(required)** — Timestamp when the document was created (ISO 8601 format). Example: 2021-01-01T00:00:00Z
  - `updatedAt` — string **(required)** — Timestamp when the document was last updated (ISO 8601 format). Example: 2021-01-01T00:00:00Z
  - `status` — string **(required)** _(enum: `draft`, `pending`, `processing`, `completed`, `failed`)_
  - `chunksCount` — number — Total number of text chunks the document was split into for semantic search and embedding. Higher numbers indicate more detailed indexing
  - `convertingDuration` — number — Time in milliseconds spent converting the document from its original format to markdown. Only populated after processing
  - `processingDuration` — number — Time in milliseconds spent chunking the document and generating embeddings for semantic search. Only populated after processing completes
  - `errorMessage` — string — Error message describing why document processing failed, if applicable. Only present when status is 'failed'

**`CreateKnowledgeBaseRequestContent`**

- `name` — string **(required)** — Descriptive name for the knowledge base. Used for identification in the UI and APIs. Examples: 'Product Knowledge Base', 'Support Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
- `description` — string — Optional detailed description of the knowledge base content and purpose. Helps users understand what topics are covered. Examples: 'Comprehensive product documentation and service guides', 'Internal technical documentation'. Length: 0-1000 characters _(maxLen=1000)_
- `dataSources` — array **(required)** — List of data source IDs that provide content for this knowledge base. Can include Confluence, Google Drive, file uploads, and proxy sources. Empty list results in no searchable content
  - _array of_ `string`

**`CreateKnowledgeBaseResponseContent`**

- `knowledgeBase` — KnowledgeBaseItem **(required)**
  - `name` — string **(required)** — Descriptive name for the knowledge base. Used for identification in the UI and APIs. Examples: 'Product Knowledge Base', 'Support Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
  - `description` — string — Optional detailed description of the knowledge base content and purpose. Helps users understand what topics are covered. Examples: 'Comprehensive product documentation and service guides', 'Internal technical documentation'. Length: 0-1000 characters _(maxLen=1000)_
  - `dataSources` — array **(required)** — List of data source IDs that provide content for this knowledge base. Can include Confluence, Google Drive, file uploads, and proxy sources. Empty list results in no searchable content
    - _array of_ `string`
  - `id` — string **(required)** — Unique identifier of the knowledge base _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `companyId` — string **(required)** — Company ID that owns this knowledge base _(minLen=3; maxLen=30)_
  - `createdAt` — string **(required)** — Timestamp when the knowledge base was created (ISO 8601 format). Example: 2021-01-01T00:00:00Z
  - `updatedAt` — string **(required)** — Timestamp when the knowledge base was last updated (ISO 8601 format). Example: 2021-01-01T00:00:00Z

**`DailyGlobalStatistics`**

- `date` — string **(required)** — Date in format yyyy-MM-dd
- `requests` — number **(required)** — Number of search requests on this day
- `uniqueUsers` — number **(required)** — Number of unique users on this day
- `noResultsRequests` — number **(required)** — Number of requests with no results on this day

**`DailySearchStatistics`**

- `date` — string **(required)** — Date in format yyyy-MM-dd
- `requests` — number **(required)** — Number of search requests

**`DataSourceConfig`**

- _oneOf_ — exactly one of:
  - **`confluence`**
    - `confluence` — ConfluenceConfig **(required)**
      - `baseUrl` — string **(required)** — The base URL of your Confluence Cloud or Server instance. Must be a valid HTTPS URL. Example: https://your-company.atlassian.net
      - `username` — string **(required)** — The email address or username associated with the Confluence account used for authentication
      - `apiKey` — string **(required)** — The API token or password for Confluence authentication. For Cloud instances, use an API token; for Server instances, use the account password
      - `spaceId` — string **(required)** — The Confluence space key or ID to synchronize. All pages within this space will be included unless explicitly excluded
      - `pages` — ConfluencePagesConfig
        - `enabled` — array **(required)** — List of Confluence page IDs that should be included in the synchronization
          - _array of_ `string`
        - `disabled` — array **(required)** — List of Confluence page IDs that should be explicitly excluded from the synchronization
          - _array of_ `string`
  - **`gdrive`**
    - `gdrive` — GDriveConfig **(required)**
      - `nangoConnectionId` — string **(required)** — The Nango integration connection ID for Google Drive. This establishes the OAuth connection to access the Drive account
      - `folders` — GDriveFoldersConfig **(required)**
        - `enabled` — array **(required)** — List of Google Drive folder IDs that should be included in the synchronization
          - _array of_ `string`
        - `disabled` — array **(required)** — List of Google Drive folder IDs that should be explicitly excluded from the synchronization
          - _array of_ `string`
  - **`website`**
    - `website` — WebsiteConfig **(required)**
      - `urls` — array **(required)** — Starting page URLs of the website to index. Must be https and resolve to a public address. The v1 console configures exactly one, but the field is a list so additional starting points can be added without a breaking change
        - _array of_ `string`
      - `maxPages` — number — Upper bound on how many pages may be selected for indexing. Server-side limits still apply and take precedence _(min=1; max=2000)_
      - `pages` — WebsitePagesConfig
        - `enabled` — array **(required)** — Absolute page URLs that should be fetched and indexed. These are the pages the user selected from the discovery result, and the complete set: anything absent is not indexed
          - _array of_ `string`
  - **`files`**
    - `files` — any **(required)**

**`DataSourceItem`**

- `name` — string **(required)** — Descriptive name for the data source. Used for identification and display in the UI. Examples: 'Product Confluence', 'Customer Service Docs', 'Engineering Wikis'. Length: 2-100 characters _(minLen=2; maxLen=100)_
- `description` — string — Optional detailed description of the data source content and purpose. Helps users understand what data is included. Examples: 'Contains product documentation and service guides from Confluence', 'Customer service articles synced from Zendesk'. Length: 0-1000 characters _(maxLen=1000)_
- `type` — string **(required)** _(enum: `files`, `confluence`, `gdrive`, `website`)_
- `config` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`confluence`**
      - `confluence` — ConfluenceConfig **(required)**
        - `baseUrl` — string **(required)** — The base URL of your Confluence Cloud or Server instance. Must be a valid HTTPS URL. Example: https://your-company.atlassian.net
        - `username` — string **(required)** — The email address or username associated with the Confluence account used for authentication
        - `apiKey` — string **(required)** — The API token or password for Confluence authentication. For Cloud instances, use an API token; for Server instances, use the account password
        - `spaceId` — string **(required)** — The Confluence space key or ID to synchronize. All pages within this space will be included unless explicitly excluded
        - `pages` — ConfluencePagesConfig
          - _(nesting depth limit — see `ConfluencePagesConfig` in the Schemas appendix)_
    - **`gdrive`**
      - `gdrive` — GDriveConfig **(required)**
        - `nangoConnectionId` — string **(required)** — The Nango integration connection ID for Google Drive. This establishes the OAuth connection to access the Drive account
        - `folders` — GDriveFoldersConfig **(required)**
          - _(nesting depth limit — see `GDriveFoldersConfig` in the Schemas appendix)_
    - **`website`**
      - `website` — WebsiteConfig **(required)**
        - `urls` — array **(required)** — Starting page URLs of the website to index. Must be https and resolve to a public address. The v1 console configures exactly one, but the field is a list so additional starting points can be added without a breaking change
          - _array of_ `string`
        - `maxPages` — number — Upper bound on how many pages may be selected for indexing. Server-side limits still apply and take precedence _(min=1; max=2000)_
        - `pages` — WebsitePagesConfig
          - _(nesting depth limit — see `WebsitePagesConfig` in the Schemas appendix)_
    - **`files`**
      - `files` — any **(required)**
- `syncSchedule` — object
- `id` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
- `companyId` — string **(required)** — Company ID that owns this data source _(minLen=3; maxLen=30)_
- `createdAt` — string **(required)** — Timestamp when the data source was created (ISO 8601 format). Example: 2025-01-01T00:00:00Z
- `updatedAt` — string **(required)** — Timestamp when the data source was last updated (ISO 8601 format). Example: 2025-01-01T00:00:00Z

**`DataSourceNotFoundExceptionResponseContent`**

- `message` — string **(required)**

**`DataSourceStatistics`**

- `dataSourceId` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
- `searchDailyBreakdown` — array **(required)**
  - _array of_ `DailySearchStatistics`
    - `date` — string **(required)** — Date in format yyyy-MM-dd
    - `requests` — number **(required)** — Number of search requests
- `documentsCount` — number **(required)**
- `documentsStatistics` — array **(required)**
  - _array of_ `DocumentsStatistics`
    - `status` — string **(required)** _(enum: `draft`, `pending`, `processing`, `completed`, `failed`)_
    - `count` — number **(required)**
- `chunksCount` — number **(required)**

**`DataSourceType`**

- string _(enum: `files`, `confluence`, `gdrive`, `website`)_

**`DescribeDataSourceConfluencePageResult`**

- `id` — string **(required)** — Unique identifier of the Confluence page _(minLen=1; maxLen=50)_
- `parentId` — string **(required)** — ID of the parent page. If this is a top-level page, parentId references the space _(minLen=1; maxLen=50)_
- `title` — string **(required)** — Display title of the Confluence page
- `position` — number — Position or order of the page within its parent. Used for determining page hierarchy

**`DescribeDataSourceConfluencePagesParameters`**

- `spaceId` — string **(required)** — Confluence space ID to list pages from. Required when requesting page information _(minLen=1; maxLen=50)_
- `parentId` — string — Optional parent page ID to retrieve only child pages under this page. If not specified, retrieves all pages in the space _(minLen=1; maxLen=50)_
- `enabled` — array — Optional list of specific page IDs to include in the result. If provided, only these pages are returned
  - _array of_ `string`

**`DescribeDataSourceConfluenceParameters`**

- `spaces` — DescribeDataSourceConfluenceSpacesParameters
  - `type` — string _(enum: `global`, `collaboration`, `knowledge_base`, `personal`, `system`, `onboarding`)_
- `pages` — DescribeDataSourceConfluencePagesParameters
  - `spaceId` — string **(required)** — Confluence space ID to list pages from. Required when requesting page information _(minLen=1; maxLen=50)_
  - `parentId` — string — Optional parent page ID to retrieve only child pages under this page. If not specified, retrieves all pages in the space _(minLen=1; maxLen=50)_
  - `enabled` — array — Optional list of specific page IDs to include in the result. If provided, only these pages are returned
    - _array of_ `string`

**`DescribeDataSourceConfluenceResult`**

- `spaces` — array — List of Confluence spaces matching the requested type filter. Only present if spaces were requested in the describe parameters
  - _array of_ `DescribeDataSourceConfluenceSpaceResult`
    - `id` — string **(required)** — Unique identifier of the Confluence space
    - `name` — string **(required)** — Display name of the Confluence space
    - `key` — string — Space key (short identifier) used in Confluence URLs
    - `type` — string **(required)** _(enum: `global`, `collaboration`, `knowledge_base`, `personal`, `system`, `onboarding`)_
- `pages` — array — List of Confluence pages from the requested space, with optional parent filtering. Only present if pages were requested in the describe parameters
  - _array of_ `DescribeDataSourceConfluencePageResult`
    - `id` — string **(required)** — Unique identifier of the Confluence page _(minLen=1; maxLen=50)_
    - `parentId` — string **(required)** — ID of the parent page. If this is a top-level page, parentId references the space _(minLen=1; maxLen=50)_
    - `title` — string **(required)** — Display title of the Confluence page
    - `position` — number — Position or order of the page within its parent. Used for determining page hierarchy

**`DescribeDataSourceConfluenceSpaceResult`**

- `id` — string **(required)** — Unique identifier of the Confluence space
- `name` — string **(required)** — Display name of the Confluence space
- `key` — string — Space key (short identifier) used in Confluence URLs
- `type` — string **(required)** _(enum: `global`, `collaboration`, `knowledge_base`, `personal`, `system`, `onboarding`)_

**`DescribeDataSourceConfluenceSpacesParameters`**

- `type` — string _(enum: `global`, `collaboration`, `knowledge_base`, `personal`, `system`, `onboarding`)_

**`DescribeDataSourceGDriveFolderResult`**

- `id` — string **(required)** — Unique identifier of the Google Drive folder
- `parentId` — string **(required)** — ID of the parent folder. Allows reconstructing the folder hierarchy
- `name` — string **(required)** — Display name of the folder in Google Drive

**`DescribeDataSourceGDriveFoldersParameters`**

- `parentId` — string **(required)** — Parent folder ID to list folders from. Use 'root' to start from the Google Drive root directory. Any valid folder ID can be specified to browse subfolders _(default=root)_
- `enabled` — array — Optional list of specific folder IDs to include in the result. If provided, only these folders are returned
  - _array of_ `string`

**`DescribeDataSourceGDriveParameters`**

- `session` — DescribeDataSourceGDriveSessionParameters
  - `userId` — string **(required)** — User ID for the Google Drive session. Used to identify which user's drive context to use. Defaults to 'admin' for admin user context _(default=admin)_
- `folders` — DescribeDataSourceGDriveFoldersParameters
  - `parentId` — string **(required)** — Parent folder ID to list folders from. Use 'root' to start from the Google Drive root directory. Any valid folder ID can be specified to browse subfolders _(default=root)_
  - `enabled` — array — Optional list of specific folder IDs to include in the result. If provided, only these folders are returned
    - _array of_ `string`

**`DescribeDataSourceGDriveResult`**

- `sessionId` — string — Nango session ID for the Google Drive integration. Used for OAuth authentication and drive access
- `folders` — array — List of folders from the requested parent directory, including their IDs, parent references, and names
  - _array of_ `DescribeDataSourceGDriveFolderResult`
    - `id` — string **(required)** — Unique identifier of the Google Drive folder
    - `parentId` — string **(required)** — ID of the parent folder. Allows reconstructing the folder hierarchy
    - `name` — string **(required)** — Display name of the folder in Google Drive

**`DescribeDataSourceGDriveSessionParameters`**

- `userId` — string **(required)** — User ID for the Google Drive session. Used to identify which user's drive context to use. Defaults to 'admin' for admin user context _(default=admin)_

**`DescribeDataSourceParameters`**

- `confluence` — DescribeDataSourceConfluenceParameters
  - `spaces` — DescribeDataSourceConfluenceSpacesParameters
    - `type` — string _(enum: `global`, `collaboration`, `knowledge_base`, `personal`, `system`, `onboarding`)_
  - `pages` — DescribeDataSourceConfluencePagesParameters
    - `spaceId` — string **(required)** — Confluence space ID to list pages from. Required when requesting page information _(minLen=1; maxLen=50)_
    - `parentId` — string — Optional parent page ID to retrieve only child pages under this page. If not specified, retrieves all pages in the space _(minLen=1; maxLen=50)_
    - `enabled` — array — Optional list of specific page IDs to include in the result. If provided, only these pages are returned
      - _array of_ `string`
- `gdrive` — DescribeDataSourceGDriveParameters
  - `session` — DescribeDataSourceGDriveSessionParameters
    - `userId` — string **(required)** — User ID for the Google Drive session. Used to identify which user's drive context to use. Defaults to 'admin' for admin user context _(default=admin)_
  - `folders` — DescribeDataSourceGDriveFoldersParameters
    - `parentId` — string **(required)** — Parent folder ID to list folders from. Use 'root' to start from the Google Drive root directory. Any valid folder ID can be specified to browse subfolders _(default=root)_
    - `enabled` — array — Optional list of specific folder IDs to include in the result. If provided, only these folders are returned
      - _array of_ `string`
- `website` — DescribeDataSourceWebsiteParameters
  - `discover` — DescribeDataSourceWebsiteDiscoverParameters
    - `url` — string **(required)** — Starting page URL of the website. Must be https and resolve to a public address _(minLen=1; maxLen=2048)_
- `proxy` — any — Parameters for describing proxy data source (type-specific, implementation varies)
- `files` — any — Parameters for describing file-based data source (type-specific, implementation varies)

**`DescribeDataSourceRequestContent`**

- `parameters` — DescribeDataSourceParameters **(required)**
  - `confluence` — DescribeDataSourceConfluenceParameters
    - `spaces` — DescribeDataSourceConfluenceSpacesParameters
      - `type` — string _(enum: `global`, `collaboration`, `knowledge_base`, `personal`, `system`, `onboarding`)_
    - `pages` — DescribeDataSourceConfluencePagesParameters
      - `spaceId` — string **(required)** — Confluence space ID to list pages from. Required when requesting page information _(minLen=1; maxLen=50)_
      - `parentId` — string — Optional parent page ID to retrieve only child pages under this page. If not specified, retrieves all pages in the space _(minLen=1; maxLen=50)_
      - `enabled` — array — Optional list of specific page IDs to include in the result. If provided, only these pages are returned
        - _array of_ `string`
  - `gdrive` — DescribeDataSourceGDriveParameters
    - `session` — DescribeDataSourceGDriveSessionParameters
      - `userId` — string **(required)** — User ID for the Google Drive session. Used to identify which user's drive context to use. Defaults to 'admin' for admin user context _(default=admin)_
    - `folders` — DescribeDataSourceGDriveFoldersParameters
      - `parentId` — string **(required)** — Parent folder ID to list folders from. Use 'root' to start from the Google Drive root directory. Any valid folder ID can be specified to browse subfolders _(default=root)_
      - `enabled` — array — Optional list of specific folder IDs to include in the result. If provided, only these folders are returned
        - _array of_ `string`
  - `website` — DescribeDataSourceWebsiteParameters
    - `discover` — DescribeDataSourceWebsiteDiscoverParameters
      - `url` — string **(required)** — Starting page URL of the website. Must be https and resolve to a public address _(minLen=1; maxLen=2048)_
  - `proxy` — any — Parameters for describing proxy data source (type-specific, implementation varies)
  - `files` — any — Parameters for describing file-based data source (type-specific, implementation varies)

**`DescribeDataSourceResponseContent`**

- `result` — DescribeDataSourceResult **(required)**
  - `confluence` — DescribeDataSourceConfluenceResult
    - `spaces` — array — List of Confluence spaces matching the requested type filter. Only present if spaces were requested in the describe parameters
      - _array of_ `DescribeDataSourceConfluenceSpaceResult`
        - _(nesting depth limit — see `DescribeDataSourceConfluenceSpaceResult` in the Schemas appendix)_
    - `pages` — array — List of Confluence pages from the requested space, with optional parent filtering. Only present if pages were requested in the describe parameters
      - _array of_ `DescribeDataSourceConfluencePageResult`
        - _(nesting depth limit — see `DescribeDataSourceConfluencePageResult` in the Schemas appendix)_
  - `gdrive` — DescribeDataSourceGDriveResult
    - `sessionId` — string — Nango session ID for the Google Drive integration. Used for OAuth authentication and drive access
    - `folders` — array — List of folders from the requested parent directory, including their IDs, parent references, and names
      - _array of_ `DescribeDataSourceGDriveFolderResult`
        - _(nesting depth limit — see `DescribeDataSourceGDriveFolderResult` in the Schemas appendix)_
  - `website` — DescribeDataSourceWebsiteResult
    - `pages` — array **(required)** — Pages discovered for the requested website
      - _array of_ `DescribeDataSourceWebsitePageResult`
        - _(nesting depth limit — see `DescribeDataSourceWebsitePageResult` in the Schemas appendix)_
    - `strategy` — string **(required)** — Which discovery strategy produced a page list. Sitemap discovery is free and usually more complete; crawl is the fallback for sites without a usable sitemap _(enum: `sitemap`, `crawl`)_
    - `truncated` — boolean **(required)** — True when discovery stopped at a limit, meaning the site has more pages than were returned
    - `canonicalUrl` — string **(required)** — The starting URL after redirects were followed. Differs from the requested URL when, for example, an apex domain redirects to www. Page scope is anchored to this URL
    - `limits` — DescribeDataSourceWebsiteLimits **(required)**
      - `maxSelectedPages` — number **(required)** — Maximum number of pages that may be selected for indexing
      - `maxDiscoveredPages` — number **(required)** — Maximum number of pages the discovery step returns
  - `proxy` — any — Result of describing proxy data source (type-specific results)
  - `files` — any — Result of describing file-based data source (type-specific results)

**`DescribeDataSourceResult`**

- `confluence` — DescribeDataSourceConfluenceResult
  - `spaces` — array — List of Confluence spaces matching the requested type filter. Only present if spaces were requested in the describe parameters
    - _array of_ `DescribeDataSourceConfluenceSpaceResult`
      - `id` — string **(required)** — Unique identifier of the Confluence space
      - `name` — string **(required)** — Display name of the Confluence space
      - `key` — string — Space key (short identifier) used in Confluence URLs
      - `type` — string **(required)** _(enum: `global`, `collaboration`, `knowledge_base`, `personal`, `system`, `onboarding`)_
  - `pages` — array — List of Confluence pages from the requested space, with optional parent filtering. Only present if pages were requested in the describe parameters
    - _array of_ `DescribeDataSourceConfluencePageResult`
      - `id` — string **(required)** — Unique identifier of the Confluence page _(minLen=1; maxLen=50)_
      - `parentId` — string **(required)** — ID of the parent page. If this is a top-level page, parentId references the space _(minLen=1; maxLen=50)_
      - `title` — string **(required)** — Display title of the Confluence page
      - `position` — number — Position or order of the page within its parent. Used for determining page hierarchy
- `gdrive` — DescribeDataSourceGDriveResult
  - `sessionId` — string — Nango session ID for the Google Drive integration. Used for OAuth authentication and drive access
  - `folders` — array — List of folders from the requested parent directory, including their IDs, parent references, and names
    - _array of_ `DescribeDataSourceGDriveFolderResult`
      - `id` — string **(required)** — Unique identifier of the Google Drive folder
      - `parentId` — string **(required)** — ID of the parent folder. Allows reconstructing the folder hierarchy
      - `name` — string **(required)** — Display name of the folder in Google Drive
- `website` — DescribeDataSourceWebsiteResult
  - `pages` — array **(required)** — Pages discovered for the requested website
    - _array of_ `DescribeDataSourceWebsitePageResult`
      - `url` — string **(required)** — Absolute URL of the discovered page
      - `host` — string **(required)** — Host the page belongs to, so pages can be grouped by host in the UI
      - `path` — string **(required)** — Path (including query string) of the page, for display in the selection list
      - `lastModified` — string — Last modification time reported by the sitemap, in ISO 8601 format. Absent for crawl-discovered pages
  - `strategy` — string **(required)** — Which discovery strategy produced a page list. Sitemap discovery is free and usually more complete; crawl is the fallback for sites without a usable sitemap _(enum: `sitemap`, `crawl`)_
  - `truncated` — boolean **(required)** — True when discovery stopped at a limit, meaning the site has more pages than were returned
  - `canonicalUrl` — string **(required)** — The starting URL after redirects were followed. Differs from the requested URL when, for example, an apex domain redirects to www. Page scope is anchored to this URL
  - `limits` — DescribeDataSourceWebsiteLimits **(required)**
    - `maxSelectedPages` — number **(required)** — Maximum number of pages that may be selected for indexing
    - `maxDiscoveredPages` — number **(required)** — Maximum number of pages the discovery step returns
- `proxy` — any — Result of describing proxy data source (type-specific results)
- `files` — any — Result of describing file-based data source (type-specific results)

**`DescribeDataSourceWebsiteDiscoverParameters`**

- `url` — string **(required)** — Starting page URL of the website. Must be https and resolve to a public address _(minLen=1; maxLen=2048)_

**`DescribeDataSourceWebsiteLimits`**

- `maxSelectedPages` — number **(required)** — Maximum number of pages that may be selected for indexing
- `maxDiscoveredPages` — number **(required)** — Maximum number of pages the discovery step returns

**`DescribeDataSourceWebsitePageResult`**

- `url` — string **(required)** — Absolute URL of the discovered page
- `host` — string **(required)** — Host the page belongs to, so pages can be grouped by host in the UI
- `path` — string **(required)** — Path (including query string) of the page, for display in the selection list
- `lastModified` — string — Last modification time reported by the sitemap, in ISO 8601 format. Absent for crawl-discovered pages

**`DescribeDataSourceWebsiteParameters`**

- `discover` — DescribeDataSourceWebsiteDiscoverParameters
  - `url` — string **(required)** — Starting page URL of the website. Must be https and resolve to a public address _(minLen=1; maxLen=2048)_

**`DescribeDataSourceWebsiteResult`**

- `pages` — array **(required)** — Pages discovered for the requested website
  - _array of_ `DescribeDataSourceWebsitePageResult`
    - `url` — string **(required)** — Absolute URL of the discovered page
    - `host` — string **(required)** — Host the page belongs to, so pages can be grouped by host in the UI
    - `path` — string **(required)** — Path (including query string) of the page, for display in the selection list
    - `lastModified` — string — Last modification time reported by the sitemap, in ISO 8601 format. Absent for crawl-discovered pages
- `strategy` — string **(required)** — Which discovery strategy produced a page list. Sitemap discovery is free and usually more complete; crawl is the fallback for sites without a usable sitemap _(enum: `sitemap`, `crawl`)_
- `truncated` — boolean **(required)** — True when discovery stopped at a limit, meaning the site has more pages than were returned
- `canonicalUrl` — string **(required)** — The starting URL after redirects were followed. Differs from the requested URL when, for example, an apex domain redirects to www. Page scope is anchored to this URL
- `limits` — DescribeDataSourceWebsiteLimits **(required)**
  - `maxSelectedPages` — number **(required)** — Maximum number of pages that may be selected for indexing
  - `maxDiscoveredPages` — number **(required)** — Maximum number of pages the discovery step returns

**`DocumentItem`**

- `title` — string **(required)** — Display title of the document used in search results and UI. Can differ from originalName. Examples: 'Product Installation Guide', 'API Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
- `url` — string — Optional URL where the document can be accessed or viewed. Used for providing direct links to the source. Example: https://confluence.company.com/wiki/Product_Documentation _(maxLen=1024)_
- `content` — string — Optional document content in plain text or markdown format. For file uploads, can be the document content.
- `description` — string — Optional detailed description of the document content and purpose. Helps users understand what the document is about. _(maxLen=2048)_
- `originalFormat` — string **(required)** — File format/extension of the original document for reference. Examples: 'pdf', 'docx', 'md', 'html', 'txt'. Helps identify source document type _(minLen=1; maxLen=10)_
- `originalName` — string **(required)** — Original filename or identifier of the source document. Preserves the source document name. Examples: 'product-knowledge-base.pdf', 'installation-guide.docx' _(minLen=1; maxLen=255)_
- `originalId` — string — Original ID from the source system, preserving the reference to the source document. Examples: 'confluence-page-1234567890' (for Confluence), 'gdrive-file-abc123' (for Google Drive), sha1(original-file-content) (for file uploads) _(minLen=1; maxLen=255)_
- `id` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
- `companyId` — string **(required)** — Company ID that owns this document _(minLen=3; maxLen=30)_
- `dataSourceId` — string **(required)** — ID of the data source containing this document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
- `createdAt` — string **(required)** — Timestamp when the document was created (ISO 8601 format). Example: 2021-01-01T00:00:00Z
- `updatedAt` — string **(required)** — Timestamp when the document was last updated (ISO 8601 format). Example: 2021-01-01T00:00:00Z
- `status` — string **(required)** _(enum: `draft`, `pending`, `processing`, `completed`, `failed`)_
- `chunksCount` — number — Total number of text chunks the document was split into for semantic search and embedding. Higher numbers indicate more detailed indexing
- `convertingDuration` — number — Time in milliseconds spent converting the document from its original format to markdown. Only populated after processing
- `processingDuration` — number — Time in milliseconds spent chunking the document and generating embeddings for semantic search. Only populated after processing completes
- `errorMessage` — string — Error message describing why document processing failed, if applicable. Only present when status is 'failed'

**`DocumentNotFoundExceptionResponseContent`**

- `message` — string **(required)**

**`DocumentStatus`**

- string _(enum: `draft`, `pending`, `processing`, `completed`, `failed`)_

**`DocumentsStatistics`**

- `status` — string **(required)** _(enum: `draft`, `pending`, `processing`, `completed`, `failed`)_
- `count` — number **(required)**

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GDriveConfig`**

- `nangoConnectionId` — string **(required)** — The Nango integration connection ID for Google Drive. This establishes the OAuth connection to access the Drive account
- `folders` — GDriveFoldersConfig **(required)**
  - `enabled` — array **(required)** — List of Google Drive folder IDs that should be included in the synchronization
    - _array of_ `string`
  - `disabled` — array **(required)** — List of Google Drive folder IDs that should be explicitly excluded from the synchronization
    - _array of_ `string`

**`GDriveFoldersConfig`**

- `enabled` — array **(required)** — List of Google Drive folder IDs that should be included in the synchronization
  - _array of_ `string`
- `disabled` — array **(required)** — List of Google Drive folder IDs that should be explicitly excluded from the synchronization
  - _array of_ `string`

**`GenerateSearchAnswerRequestContent`**

- `searchQuery` — string **(required)** — The question or query to be answered using the knowledge base. The LLM will search the knowledge base and generate an answer based on found results. Example: 'What is the product knowledge base?'
- `searchResults` — array **(required)** — The search results to be used to generate the answer. The LLM will use the search results to generate an answer based on the found results.
  - _array of_ `SearchKnowledgeBaseResultItem`
    - `chunkId` — string **(required)** — The ID of the chunk. Example: 123e4567-e89b-12d3-a456-426614174000 _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `documentId` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `documentTitle` — string **(required)**
    - `documentUrl` — string **(required)**
    - `dataSourceId` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `dataSourceType` — string **(required)** _(enum: `files`, `confluence`, `gdrive`, `website`)_
    - `score` — number **(required)** — The total score of the result, calculated from the semantic search score and the full-text search score. _(format=double)_
    - `fullTextScore` — number — The score of the result, calculated from the full-text bm25 search score. _(format=double)_
    - `semanticScore` — number — The score of the result, calculated from the semantic vector search score. _(format=double)_
    - `documentHierarchy` — array — The hierarchy of the document. The hierarchy is a list of document IDs that are the parents of the current document. The hierarchy is used to build the document hierarchy in the search results.
      - _array of_ `string`
    - `content` — string **(required)**
    - `metadata` — any — The metadata of the document.
- `model` — string — The specific provider and model identifier. Examples: 'openai://gpt-4o' or 'openai://gpt-4o-mini' for OpenAI, 'mistral://mistral-small-2506' for Mistral. Check provider documentation for available models
- `temperature` — number — Controls answer randomness and creativity (0.0-1.0). Low values (0.0-0.3) produce consistent, deterministic answers. High values (0.7-1.0) produce more diverse and creative responses. Defaults to 0.3 for factual consistency _(default=0.3; format=double; min=0; max=1)_
- `maxOutputTokens` — number — Maximum number of tokens in the generated answer (1-10000). Higher values allow longer, more detailed answers. Lower values force concise responses. Defaults to 1000 tokens. Note: higher values increase latency and cost _(default=1000; min=1; max=10000)_
- `systemPrompt` — string — Optional system prompt to customize LLM behavior and context. Sets instructions for how the LLM should answer questions. Example: 'You are a helpful technical support assistant. Answer only based on the provided knowledge base. If information is not found, say "I don't have this information in the knowledge base."'

**`GenerateSearchAnswerResponseContent`**

- `answer` — string **(required)**
- `metadata` — AnswerMetadata **(required)**
  - `model` — string **(required)**
  - `inputTokens` — number **(required)**
  - `outputTokens` — number **(required)**
  - `duration` — number **(required)**
- `sources` — array **(required)**
  - _array of_ `SearchKnowledgeBaseResultItem`
    - `chunkId` — string **(required)** — The ID of the chunk. Example: 123e4567-e89b-12d3-a456-426614174000 _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `documentId` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `documentTitle` — string **(required)**
    - `documentUrl` — string **(required)**
    - `dataSourceId` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `dataSourceType` — string **(required)** _(enum: `files`, `confluence`, `gdrive`, `website`)_
    - `score` — number **(required)** — The total score of the result, calculated from the semantic search score and the full-text search score. _(format=double)_
    - `fullTextScore` — number — The score of the result, calculated from the full-text bm25 search score. _(format=double)_
    - `semanticScore` — number — The score of the result, calculated from the semantic vector search score. _(format=double)_
    - `documentHierarchy` — array — The hierarchy of the document. The hierarchy is a list of document IDs that are the parents of the current document. The hierarchy is used to build the document hierarchy in the search results.
      - _array of_ `string`
    - `content` — string **(required)**
    - `metadata` — any — The metadata of the document.

**`GetDataSourceResponseContent`**

- `dataSource` — DataSourceItem **(required)**
  - `name` — string **(required)** — Descriptive name for the data source. Used for identification and display in the UI. Examples: 'Product Confluence', 'Customer Service Docs', 'Engineering Wikis'. Length: 2-100 characters _(minLen=2; maxLen=100)_
  - `description` — string — Optional detailed description of the data source content and purpose. Helps users understand what data is included. Examples: 'Contains product documentation and service guides from Confluence', 'Customer service articles synced from Zendesk'. Length: 0-1000 characters _(maxLen=1000)_
  - `type` — string **(required)** _(enum: `files`, `confluence`, `gdrive`, `website`)_
  - `config` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`confluence`**
        - `confluence` — ConfluenceConfig **(required)**
          - _(nesting depth limit — see `ConfluenceConfig` in the Schemas appendix)_
      - **`gdrive`**
        - `gdrive` — GDriveConfig **(required)**
          - _(nesting depth limit — see `GDriveConfig` in the Schemas appendix)_
      - **`website`**
        - `website` — WebsiteConfig **(required)**
          - _(nesting depth limit — see `WebsiteConfig` in the Schemas appendix)_
      - **`files`**
        - `files` — any **(required)**
  - `syncSchedule` — object
  - `id` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `companyId` — string **(required)** — Company ID that owns this data source _(minLen=3; maxLen=30)_
  - `createdAt` — string **(required)** — Timestamp when the data source was created (ISO 8601 format). Example: 2025-01-01T00:00:00Z
  - `updatedAt` — string **(required)** — Timestamp when the data source was last updated (ISO 8601 format). Example: 2025-01-01T00:00:00Z

**`GetDataSourceSyncStatusResponseContent`**

- `status` — string **(required)** _(enum: `idle`, `running`, `success`, `failed`)_
- `syncedAt` — string — Timestamp when the data source was last synced (ISO 8601 format). Example: 2021-01-01T00:00:00Z
- `mode` — string _(enum: `full`, `incremental`)_
- `error` — string — The error message from the last sync, if any.
- `documentsStats` — SyncStatusStats
  - _map of_ `number`

**`GetDocumentChunksResponseContent`**

- `chunks` — array **(required)**
  - _array of_ `ChunkItem`
    - `id` — string **(required)** — The ID of the chunk. Example: 123e4567-e89b-12d3-a456-426614174000 _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `documentId` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `content` — string **(required)**
    - `createdAt` — string **(required)**
    - `updatedAt` — string **(required)**

**`GetDocumentDownloadUrlResponseContent`**

- `downloadUrl` — string **(required)**

**`GetDocumentMarkdownResponseContent`**

- `markdown` — string **(required)**

**`GetDocumentResponseContent`**

- `document` — DocumentItem **(required)**
  - `title` — string **(required)** — Display title of the document used in search results and UI. Can differ from originalName. Examples: 'Product Installation Guide', 'API Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
  - `url` — string — Optional URL where the document can be accessed or viewed. Used for providing direct links to the source. Example: https://confluence.company.com/wiki/Product_Documentation _(maxLen=1024)_
  - `content` — string — Optional document content in plain text or markdown format. For file uploads, can be the document content.
  - `description` — string — Optional detailed description of the document content and purpose. Helps users understand what the document is about. _(maxLen=2048)_
  - `originalFormat` — string **(required)** — File format/extension of the original document for reference. Examples: 'pdf', 'docx', 'md', 'html', 'txt'. Helps identify source document type _(minLen=1; maxLen=10)_
  - `originalName` — string **(required)** — Original filename or identifier of the source document. Preserves the source document name. Examples: 'product-knowledge-base.pdf', 'installation-guide.docx' _(minLen=1; maxLen=255)_
  - `originalId` — string — Original ID from the source system, preserving the reference to the source document. Examples: 'confluence-page-1234567890' (for Confluence), 'gdrive-file-abc123' (for Google Drive), sha1(original-file-content) (for file uploads) _(minLen=1; maxLen=255)_
  - `id` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `companyId` — string **(required)** — Company ID that owns this document _(minLen=3; maxLen=30)_
  - `dataSourceId` — string **(required)** — ID of the data source containing this document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `createdAt` — string **(required)** — Timestamp when the document was created (ISO 8601 format). Example: 2021-01-01T00:00:00Z
  - `updatedAt` — string **(required)** — Timestamp when the document was last updated (ISO 8601 format). Example: 2021-01-01T00:00:00Z
  - `status` — string **(required)** _(enum: `draft`, `pending`, `processing`, `completed`, `failed`)_
  - `chunksCount` — number — Total number of text chunks the document was split into for semantic search and embedding. Higher numbers indicate more detailed indexing
  - `convertingDuration` — number — Time in milliseconds spent converting the document from its original format to markdown. Only populated after processing
  - `processingDuration` — number — Time in milliseconds spent chunking the document and generating embeddings for semantic search. Only populated after processing completes
  - `errorMessage` — string — Error message describing why document processing failed, if applicable. Only present when status is 'failed'

**`GetDocumentUploadUrlResponseContent`**

- `uploadUrl` — string **(required)**

**`GetDocumentWithContentAndChunksResponseContent`**

- `document` — DocumentItem **(required)**
  - `title` — string **(required)** — Display title of the document used in search results and UI. Can differ from originalName. Examples: 'Product Installation Guide', 'API Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
  - `url` — string — Optional URL where the document can be accessed or viewed. Used for providing direct links to the source. Example: https://confluence.company.com/wiki/Product_Documentation _(maxLen=1024)_
  - `content` — string — Optional document content in plain text or markdown format. For file uploads, can be the document content.
  - `description` — string — Optional detailed description of the document content and purpose. Helps users understand what the document is about. _(maxLen=2048)_
  - `originalFormat` — string **(required)** — File format/extension of the original document for reference. Examples: 'pdf', 'docx', 'md', 'html', 'txt'. Helps identify source document type _(minLen=1; maxLen=10)_
  - `originalName` — string **(required)** — Original filename or identifier of the source document. Preserves the source document name. Examples: 'product-knowledge-base.pdf', 'installation-guide.docx' _(minLen=1; maxLen=255)_
  - `originalId` — string — Original ID from the source system, preserving the reference to the source document. Examples: 'confluence-page-1234567890' (for Confluence), 'gdrive-file-abc123' (for Google Drive), sha1(original-file-content) (for file uploads) _(minLen=1; maxLen=255)_
  - `id` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `companyId` — string **(required)** — Company ID that owns this document _(minLen=3; maxLen=30)_
  - `dataSourceId` — string **(required)** — ID of the data source containing this document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `createdAt` — string **(required)** — Timestamp when the document was created (ISO 8601 format). Example: 2021-01-01T00:00:00Z
  - `updatedAt` — string **(required)** — Timestamp when the document was last updated (ISO 8601 format). Example: 2021-01-01T00:00:00Z
  - `status` — string **(required)** _(enum: `draft`, `pending`, `processing`, `completed`, `failed`)_
  - `chunksCount` — number — Total number of text chunks the document was split into for semantic search and embedding. Higher numbers indicate more detailed indexing
  - `convertingDuration` — number — Time in milliseconds spent converting the document from its original format to markdown. Only populated after processing
  - `processingDuration` — number — Time in milliseconds spent chunking the document and generating embeddings for semantic search. Only populated after processing completes
  - `errorMessage` — string — Error message describing why document processing failed, if applicable. Only present when status is 'failed'
- `content` — string **(required)**
- `chunks` — array **(required)**
  - _array of_ `ChunkItem`
    - `id` — string **(required)** — The ID of the chunk. Example: 123e4567-e89b-12d3-a456-426614174000 _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `documentId` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `content` — string **(required)**
    - `createdAt` — string **(required)**
    - `updatedAt` — string **(required)**

**`GetKnowledgeBaseResponseContent`**

- `knowledgeBase` — KnowledgeBaseItem **(required)**
  - `name` — string **(required)** — Descriptive name for the knowledge base. Used for identification in the UI and APIs. Examples: 'Product Knowledge Base', 'Support Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
  - `description` — string — Optional detailed description of the knowledge base content and purpose. Helps users understand what topics are covered. Examples: 'Comprehensive product documentation and service guides', 'Internal technical documentation'. Length: 0-1000 characters _(maxLen=1000)_
  - `dataSources` — array **(required)** — List of data source IDs that provide content for this knowledge base. Can include Confluence, Google Drive, file uploads, and proxy sources. Empty list results in no searchable content
    - _array of_ `string`
  - `id` — string **(required)** — Unique identifier of the knowledge base _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `companyId` — string **(required)** — Company ID that owns this knowledge base _(minLen=3; maxLen=30)_
  - `createdAt` — string **(required)** — Timestamp when the knowledge base was created (ISO 8601 format). Example: 2021-01-01T00:00:00Z
  - `updatedAt` — string **(required)** — Timestamp when the knowledge base was last updated (ISO 8601 format). Example: 2021-01-01T00:00:00Z

**`HistoryStatistics`**

- `totalRequests` — number **(required)** — Total number of all search requests (all time)
- `recentRequests` — number **(required)** — Number of search requests in the last N days (where N is daysBack)
- `totalUniqueUsers` — number **(required)** — Total number of unique users (all time)
- `recentUniqueUsers` — number **(required)** — Number of unique users in the last N days
- `noResultsRequests` — number **(required)** — Number of requests with no results (in the last N days if daysBack specified, otherwise all time)
- `dailyBreakdown` — array — Daily breakdown of statistics for the last N days. Only present if daysBack is specified.
  - _array of_ `DailyGlobalStatistics`
    - `date` — string **(required)** — Date in format yyyy-MM-dd
    - `requests` — number **(required)** — Number of search requests on this day
    - `uniqueUsers` — number **(required)** — Number of unique users on this day
    - `noResultsRequests` — number **(required)** — Number of requests with no results on this day
- `knowledgeBases` — array — Statistics for each knowledge base
  - _array of_ `KnowledgeBaseStatistics`
    - `knowledgeBaseId` — string **(required)** — Unique identifier of the knowledge base _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `searchDailyBreakdown` — array **(required)**
      - _array of_ `DailySearchStatistics`
        - _(nesting depth limit — see `DailySearchStatistics` in the Schemas appendix)_
- `dataSources` — array — Statistics for each data source
  - _array of_ `DataSourceStatistics`
    - `dataSourceId` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `searchDailyBreakdown` — array **(required)**
      - _array of_ `DailySearchStatistics`
        - _(nesting depth limit — see `DailySearchStatistics` in the Schemas appendix)_
    - `documentsCount` — number **(required)**
    - `documentsStatistics` — array **(required)**
      - _array of_ `DocumentsStatistics`
        - _(nesting depth limit — see `DocumentsStatistics` in the Schemas appendix)_
    - `chunksCount` — number **(required)**

**`HistoryStatisticsFilter`**

- `knowledgeBaseIds` — array — Filter history by the knowledge base IDs.
  - _array of_ `string`
- `dataSourceIds` — array — Filter history by the data source IDs.
  - _array of_ `string`
- `daysBack` — number — Number of days to look back for recent statistics. If not specified, defaults to 7 days. _(default=7; min=1; max=30)_

**`KnowledgeBaseItem`**

- `name` — string **(required)** — Descriptive name for the knowledge base. Used for identification in the UI and APIs. Examples: 'Product Knowledge Base', 'Support Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
- `description` — string — Optional detailed description of the knowledge base content and purpose. Helps users understand what topics are covered. Examples: 'Comprehensive product documentation and service guides', 'Internal technical documentation'. Length: 0-1000 characters _(maxLen=1000)_
- `dataSources` — array **(required)** — List of data source IDs that provide content for this knowledge base. Can include Confluence, Google Drive, file uploads, and proxy sources. Empty list results in no searchable content
  - _array of_ `string`
- `id` — string **(required)** — Unique identifier of the knowledge base _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
- `companyId` — string **(required)** — Company ID that owns this knowledge base _(minLen=3; maxLen=30)_
- `createdAt` — string **(required)** — Timestamp when the knowledge base was created (ISO 8601 format). Example: 2021-01-01T00:00:00Z
- `updatedAt` — string **(required)** — Timestamp when the knowledge base was last updated (ISO 8601 format). Example: 2021-01-01T00:00:00Z

**`KnowledgeBaseStatistics`**

- `knowledgeBaseId` — string **(required)** — Unique identifier of the knowledge base _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
- `searchDailyBreakdown` — array **(required)**
  - _array of_ `DailySearchStatistics`
    - `date` — string **(required)** — Date in format yyyy-MM-dd
    - `requests` — number **(required)** — Number of search requests

**`ListDataSourceStatisticsResponseContent`**

- `documentsCount` — number **(required)**
- `chunksCount` — number **(required)**

**`ListDataSourceSynchronizationLogsResponseContent`**

- `logs` — array **(required)**
  - _array of_ `SyncLogItem`
    - `timestamp` — string **(required)**
    - `level` — string **(required)** _(enum: `debug`, `info`, `warn`, `error`)_
    - `message` — string **(required)**
- `metadata` — PaginationMetadata **(required)**
  - `total` — number **(required)** — The total number of results.
  - `limit` — number — The number of results per page.
  - `offset` — number — The offset from which to start the results.

**`ListDataSourcesResponseContent`**

- `dataSources` — array **(required)**
  - _array of_ `DataSourceItem`
    - `name` — string **(required)** — Descriptive name for the data source. Used for identification and display in the UI. Examples: 'Product Confluence', 'Customer Service Docs', 'Engineering Wikis'. Length: 2-100 characters _(minLen=2; maxLen=100)_
    - `description` — string — Optional detailed description of the data source content and purpose. Helps users understand what data is included. Examples: 'Contains product documentation and service guides from Confluence', 'Customer service articles synced from Zendesk'. Length: 0-1000 characters _(maxLen=1000)_
    - `type` — string **(required)** _(enum: `files`, `confluence`, `gdrive`, `website`)_
    - `config` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`confluence`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`gdrive`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`website`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`files`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `syncSchedule` — object
    - `id` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `companyId` — string **(required)** — Company ID that owns this data source _(minLen=3; maxLen=30)_
    - `createdAt` — string **(required)** — Timestamp when the data source was created (ISO 8601 format). Example: 2025-01-01T00:00:00Z
    - `updatedAt` — string **(required)** — Timestamp when the data source was last updated (ISO 8601 format). Example: 2025-01-01T00:00:00Z

**`ListDocumentsResponseContent`**

- `documents` — array **(required)**
  - _array of_ `DocumentItem`
    - `title` — string **(required)** — Display title of the document used in search results and UI. Can differ from originalName. Examples: 'Product Installation Guide', 'API Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
    - `url` — string — Optional URL where the document can be accessed or viewed. Used for providing direct links to the source. Example: https://confluence.company.com/wiki/Product_Documentation _(maxLen=1024)_
    - `content` — string — Optional document content in plain text or markdown format. For file uploads, can be the document content.
    - `description` — string — Optional detailed description of the document content and purpose. Helps users understand what the document is about. _(maxLen=2048)_
    - `originalFormat` — string **(required)** — File format/extension of the original document for reference. Examples: 'pdf', 'docx', 'md', 'html', 'txt'. Helps identify source document type _(minLen=1; maxLen=10)_
    - `originalName` — string **(required)** — Original filename or identifier of the source document. Preserves the source document name. Examples: 'product-knowledge-base.pdf', 'installation-guide.docx' _(minLen=1; maxLen=255)_
    - `originalId` — string — Original ID from the source system, preserving the reference to the source document. Examples: 'confluence-page-1234567890' (for Confluence), 'gdrive-file-abc123' (for Google Drive), sha1(original-file-content) (for file uploads) _(minLen=1; maxLen=255)_
    - `id` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `companyId` — string **(required)** — Company ID that owns this document _(minLen=3; maxLen=30)_
    - `dataSourceId` — string **(required)** — ID of the data source containing this document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `createdAt` — string **(required)** — Timestamp when the document was created (ISO 8601 format). Example: 2021-01-01T00:00:00Z
    - `updatedAt` — string **(required)** — Timestamp when the document was last updated (ISO 8601 format). Example: 2021-01-01T00:00:00Z
    - `status` — string **(required)** _(enum: `draft`, `pending`, `processing`, `completed`, `failed`)_
    - `chunksCount` — number — Total number of text chunks the document was split into for semantic search and embedding. Higher numbers indicate more detailed indexing
    - `convertingDuration` — number — Time in milliseconds spent converting the document from its original format to markdown. Only populated after processing
    - `processingDuration` — number — Time in milliseconds spent chunking the document and generating embeddings for semantic search. Only populated after processing completes
    - `errorMessage` — string — Error message describing why document processing failed, if applicable. Only present when status is 'failed'
- `metadata` — PaginationMetadata **(required)**
  - `total` — number **(required)** — The total number of results.
  - `limit` — number — The number of results per page.
  - `offset` — number — The offset from which to start the results.

**`ListHistoryStatisticsRequestContent`**

- `filter` — HistoryStatisticsFilter **(required)**
  - `knowledgeBaseIds` — array — Filter history by the knowledge base IDs.
    - _array of_ `string`
  - `dataSourceIds` — array — Filter history by the data source IDs.
    - _array of_ `string`
  - `daysBack` — number — Number of days to look back for recent statistics. If not specified, defaults to 7 days. _(default=7; min=1; max=30)_

**`ListHistoryStatisticsResponseContent`**

- `statistics` — HistoryStatistics **(required)**
  - `totalRequests` — number **(required)** — Total number of all search requests (all time)
  - `recentRequests` — number **(required)** — Number of search requests in the last N days (where N is daysBack)
  - `totalUniqueUsers` — number **(required)** — Total number of unique users (all time)
  - `recentUniqueUsers` — number **(required)** — Number of unique users in the last N days
  - `noResultsRequests` — number **(required)** — Number of requests with no results (in the last N days if daysBack specified, otherwise all time)
  - `dailyBreakdown` — array — Daily breakdown of statistics for the last N days. Only present if daysBack is specified.
    - _array of_ `DailyGlobalStatistics`
      - `date` — string **(required)** — Date in format yyyy-MM-dd
      - `requests` — number **(required)** — Number of search requests on this day
      - `uniqueUsers` — number **(required)** — Number of unique users on this day
      - `noResultsRequests` — number **(required)** — Number of requests with no results on this day
  - `knowledgeBases` — array — Statistics for each knowledge base
    - _array of_ `KnowledgeBaseStatistics`
      - `knowledgeBaseId` — string **(required)** — Unique identifier of the knowledge base _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
      - `searchDailyBreakdown` — array **(required)**
        - _(nesting depth limit — see `DailySearchStatistics` in the Schemas appendix)_
  - `dataSources` — array — Statistics for each data source
    - _array of_ `DataSourceStatistics`
      - `dataSourceId` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
      - `searchDailyBreakdown` — array **(required)**
        - _(nesting depth limit — see `DailySearchStatistics` in the Schemas appendix)_
      - `documentsCount` — number **(required)**
      - `documentsStatistics` — array **(required)**
        - _(nesting depth limit — see `DocumentsStatistics` in the Schemas appendix)_
      - `chunksCount` — number **(required)**

**`ListKnowledgeBasesResponseContent`**

- `knowledgeBases` — array **(required)**
  - _array of_ `KnowledgeBaseItem`
    - `name` — string **(required)** — Descriptive name for the knowledge base. Used for identification in the UI and APIs. Examples: 'Product Knowledge Base', 'Support Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
    - `description` — string — Optional detailed description of the knowledge base content and purpose. Helps users understand what topics are covered. Examples: 'Comprehensive product documentation and service guides', 'Internal technical documentation'. Length: 0-1000 characters _(maxLen=1000)_
    - `dataSources` — array **(required)** — List of data source IDs that provide content for this knowledge base. Can include Confluence, Google Drive, file uploads, and proxy sources. Empty list results in no searchable content
      - _array of_ `string`
    - `id` — string **(required)** — Unique identifier of the knowledge base _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `companyId` — string **(required)** — Company ID that owns this knowledge base _(minLen=3; maxLen=30)_
    - `createdAt` — string **(required)** — Timestamp when the knowledge base was created (ISO 8601 format). Example: 2021-01-01T00:00:00Z
    - `updatedAt` — string **(required)** — Timestamp when the knowledge base was last updated (ISO 8601 format). Example: 2021-01-01T00:00:00Z

**`ListSearchQueriesHistoryRequestContent`**

- `filter` — SearchHistoryFilter **(required)**
  - `knowledgeBaseId` — string — Filter history by the knowledge base ID. _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `dataSourceId` — string — Filter history by the data source ID. _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `sessionId` — string — Filter history by the internal session ID. _(minLen=1; maxLen=255)_
  - `sessionUri` — string — Filter history by the session URI. Used for tracking and analytics purposes. Example: `chatbots://{agentId}/id-of-chat-session/id-of-message` _(minLen=1; maxLen=255)_
  - `sessionUser` — string — Filter history by the user who performs the search in the knowledge base. Example: user@example.com _(minLen=1; maxLen=100)_
  - `withEmptyResults` — boolean — Whether to include the history results with empty results. _(default=False)_
- `search` — string — The search query string for filtering the history results. _(pattern=^[\p{L}0-9 \-_]{3,32}$)_
- `withContent` — boolean — Whether to include the content of the chunks in the history results. _(default=False)_

**`ListSearchQueriesHistoryResponseContent`**

- `history` — array **(required)**
  - _array of_ `SearchHistoryItem`
    - `sessionId` — string **(required)**
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `request` — SearchHistoryRequest **(required)**
      - `query` — string **(required)**
      - `sessionUser` — string **(required)** _(minLen=1; maxLen=100)_
      - `sessionUri` — string **(required)** _(minLen=1; maxLen=255)_
      - `knowledgeBaseId` — string **(required)** — Unique identifier of the knowledge base _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
      - `searchStrategy` — string **(required)** _(enum: `bm25`, `vector`, `hybrid`)_
      - `searchLimit` — number **(required)**
      - `searchThreshold` — number **(required)** _(format=double)_
    - `stages` — SearchHistoryStages **(required)**
      - `overall` — SearchHistoryOverallStage **(required)**
        - _(nesting depth limit — see `SearchHistoryOverallStage` in the Schemas appendix)_
      - `transformQuery` — SearchHistoryTransformQueryStage
        - _(nesting depth limit — see `SearchHistoryTransformQueryStage` in the Schemas appendix)_
      - `generateQueryEmbedding` — SearchHistoryEmbeddingStage **(required)**
        - _(nesting depth limit — see `SearchHistoryEmbeddingStage` in the Schemas appendix)_
      - `search` — SearchHistorySearchStage **(required)**
        - _(nesting depth limit — see `SearchHistorySearchStage` in the Schemas appendix)_
      - `enrichData` — SearchEnrichDataStage
        - _(nesting depth limit — see `SearchEnrichDataStage` in the Schemas appendix)_
    - `results` — array **(required)**
      - _array of_ `SearchHistoryResultItem`
        - _(nesting depth limit — see `SearchHistoryResultItem` in the Schemas appendix)_
    - `createdAt` — string **(required)**
    - `totalDuration` — number **(required)**
    - `resultsCount` — number **(required)**
- `metadata` — PaginationMetadata **(required)**
  - `total` — number **(required)** — The total number of results.
  - `limit` — number — The number of results per page.
  - `offset` — number — The offset from which to start the results.

**`PaginationMetadata`**

- `total` — number **(required)** — The total number of results.
- `limit` — number — The number of results per page.
- `offset` — number — The offset from which to start the results.

**`ScheduleConfiguration`**

- string _(enum: `DISABLED`, `EVERY_SIX_HOURS`, `EVERY_TWELVE_HOURS`, `EVERY_DAY`, `EVERY_WEEK`)_

**`SearchEnrichDataStage`**

- `startTime` — number **(required)**
- `endTime` — number **(required)**
- `duration` — number **(required)**

**`SearchHistoryEmbeddingStage`**

- `startTime` — number **(required)**
- `endTime` — number **(required)**
- `duration` — number **(required)**
- `model` — string **(required)**
- `inputTokens` — number **(required)**
- `outputTokens` — number **(required)**

**`SearchHistoryFilter`**

- `knowledgeBaseId` — string — Filter history by the knowledge base ID. _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
- `dataSourceId` — string — Filter history by the data source ID. _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
- `sessionId` — string — Filter history by the internal session ID. _(minLen=1; maxLen=255)_
- `sessionUri` — string — Filter history by the session URI. Used for tracking and analytics purposes. Example: `chatbots://{agentId}/id-of-chat-session/id-of-message` _(minLen=1; maxLen=255)_
- `sessionUser` — string — Filter history by the user who performs the search in the knowledge base. Example: user@example.com _(minLen=1; maxLen=100)_
- `withEmptyResults` — boolean — Whether to include the history results with empty results. _(default=False)_

**`SearchHistoryItem`**

- `sessionId` — string **(required)**
- `companyId` — string **(required)** _(minLen=3; maxLen=30)_
- `request` — SearchHistoryRequest **(required)**
  - `query` — string **(required)**
  - `sessionUser` — string **(required)** _(minLen=1; maxLen=100)_
  - `sessionUri` — string **(required)** _(minLen=1; maxLen=255)_
  - `knowledgeBaseId` — string **(required)** — Unique identifier of the knowledge base _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `searchStrategy` — string **(required)** _(enum: `bm25`, `vector`, `hybrid`)_
  - `searchLimit` — number **(required)**
  - `searchThreshold` — number **(required)** _(format=double)_
- `stages` — SearchHistoryStages **(required)**
  - `overall` — SearchHistoryOverallStage **(required)**
    - `startTime` — number **(required)**
    - `endTime` — number **(required)**
    - `duration` — number **(required)**
  - `transformQuery` — SearchHistoryTransformQueryStage
    - `startTime` — number **(required)**
    - `endTime` — number **(required)**
    - `duration` — number **(required)**
    - `model` — string **(required)**
    - `inputTokens` — number **(required)**
    - `outputTokens` — number **(required)**
    - `transformedQuery` — string **(required)**
  - `generateQueryEmbedding` — SearchHistoryEmbeddingStage **(required)**
    - `startTime` — number **(required)**
    - `endTime` — number **(required)**
    - `duration` — number **(required)**
    - `model` — string **(required)**
    - `inputTokens` — number **(required)**
    - `outputTokens` — number **(required)**
  - `search` — SearchHistorySearchStage **(required)**
    - `startTime` — number **(required)**
    - `endTime` — number **(required)**
    - `duration` — number **(required)**
  - `enrichData` — SearchEnrichDataStage
    - `startTime` — number **(required)**
    - `endTime` — number **(required)**
    - `duration` — number **(required)**
- `results` — array **(required)**
  - _array of_ `SearchHistoryResultItem`
    - `chunkId` — string **(required)** — The ID of the chunk. Example: 123e4567-e89b-12d3-a456-426614174000 _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `documentId` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `documentTitle` — string **(required)**
    - `documentUrl` — string **(required)**
    - `dataSourceId` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `dataSourceType` — string **(required)** _(enum: `files`, `confluence`, `gdrive`, `website`)_
    - `score` — number **(required)** — The total score of the result, calculated from the semantic search score and the full-text search score. _(format=double)_
    - `fullTextScore` — number — The score of the result, calculated from the full-text bm25 search score. _(format=double)_
    - `semanticScore` — number — The score of the result, calculated from the semantic vector search score. _(format=double)_
    - `documentHierarchy` — array — The hierarchy of the document. The hierarchy is a list of document IDs that are the parents of the current document. The hierarchy is used to build the document hierarchy in the search results.
      - _array of_ `string`
    - `content` — string
- `createdAt` — string **(required)**
- `totalDuration` — number **(required)**
- `resultsCount` — number **(required)**

**`SearchHistoryOverallStage`**

- `startTime` — number **(required)**
- `endTime` — number **(required)**
- `duration` — number **(required)**

**`SearchHistoryRequest`**

- `query` — string **(required)**
- `sessionUser` — string **(required)** _(minLen=1; maxLen=100)_
- `sessionUri` — string **(required)** _(minLen=1; maxLen=255)_
- `knowledgeBaseId` — string **(required)** — Unique identifier of the knowledge base _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
- `searchStrategy` — string **(required)** _(enum: `bm25`, `vector`, `hybrid`)_
- `searchLimit` — number **(required)**
- `searchThreshold` — number **(required)** _(format=double)_

**`SearchHistoryResultItem`**

- `chunkId` — string **(required)** — The ID of the chunk. Example: 123e4567-e89b-12d3-a456-426614174000 _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
- `documentId` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
- `documentTitle` — string **(required)**
- `documentUrl` — string **(required)**
- `dataSourceId` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
- `dataSourceType` — string **(required)** _(enum: `files`, `confluence`, `gdrive`, `website`)_
- `score` — number **(required)** — The total score of the result, calculated from the semantic search score and the full-text search score. _(format=double)_
- `fullTextScore` — number — The score of the result, calculated from the full-text bm25 search score. _(format=double)_
- `semanticScore` — number — The score of the result, calculated from the semantic vector search score. _(format=double)_
- `documentHierarchy` — array — The hierarchy of the document. The hierarchy is a list of document IDs that are the parents of the current document. The hierarchy is used to build the document hierarchy in the search results.
  - _array of_ `string`
- `content` — string

**`SearchHistorySearchStage`**

- `startTime` — number **(required)**
- `endTime` — number **(required)**
- `duration` — number **(required)**

**`SearchHistoryStages`**

- `overall` — SearchHistoryOverallStage **(required)**
  - `startTime` — number **(required)**
  - `endTime` — number **(required)**
  - `duration` — number **(required)**
- `transformQuery` — SearchHistoryTransformQueryStage
  - `startTime` — number **(required)**
  - `endTime` — number **(required)**
  - `duration` — number **(required)**
  - `model` — string **(required)**
  - `inputTokens` — number **(required)**
  - `outputTokens` — number **(required)**
  - `transformedQuery` — string **(required)**
- `generateQueryEmbedding` — SearchHistoryEmbeddingStage **(required)**
  - `startTime` — number **(required)**
  - `endTime` — number **(required)**
  - `duration` — number **(required)**
  - `model` — string **(required)**
  - `inputTokens` — number **(required)**
  - `outputTokens` — number **(required)**
- `search` — SearchHistorySearchStage **(required)**
  - `startTime` — number **(required)**
  - `endTime` — number **(required)**
  - `duration` — number **(required)**
- `enrichData` — SearchEnrichDataStage
  - `startTime` — number **(required)**
  - `endTime` — number **(required)**
  - `duration` — number **(required)**

**`SearchHistoryTransformQueryStage`**

- `startTime` — number **(required)**
- `endTime` — number **(required)**
- `duration` — number **(required)**
- `model` — string **(required)**
- `inputTokens` — number **(required)**
- `outputTokens` — number **(required)**
- `transformedQuery` — string **(required)**

**`SearchKnowledgeBaseRequestContent`**

- `query` — string **(required)** — The search query string. Can be a single keyword or a natural language question. Example: 'What is the product knowledge base?'
- `searchStrategy` — object
- `searchLimit` — number — Maximum number of search results to return. Controls the size of the result set. Valid range: 1-50. Defaults to 10 if not specified. Higher values return more results but may include less relevant matches _(default=10; min=1; max=50)_
- `searchThreshold` — object
- `useQueryOptimization` — boolean — Whether to optimize and transform the input query using advanced NLP techniques before searching. Improves search quality for complex or poorly phrased queries. Defaults to false. Set to true for better results with natural language questions _(default=False)_
- `sessionUser` — string — The user who performs the search in the knowledge base. Example: user@example.com or Jon Doe _(default=unknown; minLen=1; maxLen=100)_
- `sessionUri` — string — The session URI. Used for tracking and analytics purposes. Example: `chatbots://{agentId}/id-of-chat-session/id-of-message` _(default=unknown; minLen=1; maxLen=255)_

**`SearchKnowledgeBaseResponseContent`**

- `results` — array **(required)**
  - _array of_ `SearchKnowledgeBaseResultItem`
    - `chunkId` — string **(required)** — The ID of the chunk. Example: 123e4567-e89b-12d3-a456-426614174000 _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `documentId` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `documentTitle` — string **(required)**
    - `documentUrl` — string **(required)**
    - `dataSourceId` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `dataSourceType` — string **(required)** _(enum: `files`, `confluence`, `gdrive`, `website`)_
    - `score` — number **(required)** — The total score of the result, calculated from the semantic search score and the full-text search score. _(format=double)_
    - `fullTextScore` — number — The score of the result, calculated from the full-text bm25 search score. _(format=double)_
    - `semanticScore` — number — The score of the result, calculated from the semantic vector search score. _(format=double)_
    - `documentHierarchy` — array — The hierarchy of the document. The hierarchy is a list of document IDs that are the parents of the current document. The hierarchy is used to build the document hierarchy in the search results.
      - _array of_ `string`
    - `content` — string **(required)**
    - `metadata` — any — The metadata of the document.
- `metadata` — SearchResultMetadata **(required)**
  - `sessionId` — string **(required)**
  - `duration` — number **(required)**

**`SearchKnowledgeBaseResultItem`**

- `chunkId` — string **(required)** — The ID of the chunk. Example: 123e4567-e89b-12d3-a456-426614174000 _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
- `documentId` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
- `documentTitle` — string **(required)**
- `documentUrl` — string **(required)**
- `dataSourceId` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
- `dataSourceType` — string **(required)** _(enum: `files`, `confluence`, `gdrive`, `website`)_
- `score` — number **(required)** — The total score of the result, calculated from the semantic search score and the full-text search score. _(format=double)_
- `fullTextScore` — number — The score of the result, calculated from the full-text bm25 search score. _(format=double)_
- `semanticScore` — number — The score of the result, calculated from the semantic vector search score. _(format=double)_
- `documentHierarchy` — array — The hierarchy of the document. The hierarchy is a list of document IDs that are the parents of the current document. The hierarchy is used to build the document hierarchy in the search results.
  - _array of_ `string`
- `content` — string **(required)**
- `metadata` — any — The metadata of the document.

**`SearchResultMetadata`**

- `sessionId` — string **(required)**
- `duration` — number **(required)**

**`SearchStrategy`**

- string _(enum: `bm25`, `vector`, `hybrid`)_

**`SearchThresholdValue`**

- string _(enum: `low`, `medium`, `high`)_

**`SyncDataSourceMode`**

- string _(enum: `full`, `incremental`)_

**`SyncDataSourceStatus`**

- string _(enum: `idle`, `running`, `success`, `failed`)_

**`SyncLogItem`**

- `timestamp` — string **(required)**
- `level` — string **(required)** _(enum: `debug`, `info`, `warn`, `error`)_
- `message` — string **(required)**

**`SyncLogLevel`**

- string _(enum: `debug`, `info`, `warn`, `error`)_

**`SyncStatusStats`**

- _map of_ `number`

**`UnauthorizedExceptionResponseContent`**

- `message` — string **(required)**

**`UpdateDataSourceRequestContent`**

- `name` — string **(required)** — Updated descriptive name for the data source. Used for identification and display in the UI. Length: 2-100 characters _(minLen=2; maxLen=100)_
- `description` — string — Updated detailed description of the data source content and purpose. Length: 0-1000 characters _(maxLen=1000)_

**`UpdateDataSourceResponseContent`**

- `dataSource` — DataSourceItem **(required)**
  - `name` — string **(required)** — Descriptive name for the data source. Used for identification and display in the UI. Examples: 'Product Confluence', 'Customer Service Docs', 'Engineering Wikis'. Length: 2-100 characters _(minLen=2; maxLen=100)_
  - `description` — string — Optional detailed description of the data source content and purpose. Helps users understand what data is included. Examples: 'Contains product documentation and service guides from Confluence', 'Customer service articles synced from Zendesk'. Length: 0-1000 characters _(maxLen=1000)_
  - `type` — string **(required)** _(enum: `files`, `confluence`, `gdrive`, `website`)_
  - `config` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`confluence`**
        - `confluence` — ConfluenceConfig **(required)**
          - _(nesting depth limit — see `ConfluenceConfig` in the Schemas appendix)_
      - **`gdrive`**
        - `gdrive` — GDriveConfig **(required)**
          - _(nesting depth limit — see `GDriveConfig` in the Schemas appendix)_
      - **`website`**
        - `website` — WebsiteConfig **(required)**
          - _(nesting depth limit — see `WebsiteConfig` in the Schemas appendix)_
      - **`files`**
        - `files` — any **(required)**
  - `syncSchedule` — object
  - `id` — string **(required)** — Unique identifier of the data source _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `companyId` — string **(required)** — Company ID that owns this data source _(minLen=3; maxLen=30)_
  - `createdAt` — string **(required)** — Timestamp when the data source was created (ISO 8601 format). Example: 2025-01-01T00:00:00Z
  - `updatedAt` — string **(required)** — Timestamp when the data source was last updated (ISO 8601 format). Example: 2025-01-01T00:00:00Z

**`UpdateDocumentRequestContent`**

- `title` — string — Display title of the document used in search results and UI. Can differ from originalName. Examples: 'Product Installation Guide', 'API Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
- `url` — string — Optional URL where the document can be accessed or viewed. Used for providing direct links to the source. Example: https://confluence.company.com/wiki/Product_Documentation _(maxLen=1024)_
- `description` — string — Optional detailed description of the document content and purpose. Helps users understand what the document is about. _(maxLen=2048)_
- `content` — string — Optional document content in plain text or markdown format. For file uploads, can be the document content.
- `updatedAt` — string — Timestamp when the document was last updated (ISO 8601 format). Example: 2021-01-01T00:00:00Z

**`UpdateDocumentResponseContent`**

- `document` — DocumentItem **(required)**
  - `title` — string **(required)** — Display title of the document used in search results and UI. Can differ from originalName. Examples: 'Product Installation Guide', 'API Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
  - `url` — string — Optional URL where the document can be accessed or viewed. Used for providing direct links to the source. Example: https://confluence.company.com/wiki/Product_Documentation _(maxLen=1024)_
  - `content` — string — Optional document content in plain text or markdown format. For file uploads, can be the document content.
  - `description` — string — Optional detailed description of the document content and purpose. Helps users understand what the document is about. _(maxLen=2048)_
  - `originalFormat` — string **(required)** — File format/extension of the original document for reference. Examples: 'pdf', 'docx', 'md', 'html', 'txt'. Helps identify source document type _(minLen=1; maxLen=10)_
  - `originalName` — string **(required)** — Original filename or identifier of the source document. Preserves the source document name. Examples: 'product-knowledge-base.pdf', 'installation-guide.docx' _(minLen=1; maxLen=255)_
  - `originalId` — string — Original ID from the source system, preserving the reference to the source document. Examples: 'confluence-page-1234567890' (for Confluence), 'gdrive-file-abc123' (for Google Drive), sha1(original-file-content) (for file uploads) _(minLen=1; maxLen=255)_
  - `id` — string **(required)** — Unique identifier of the document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `companyId` — string **(required)** — Company ID that owns this document _(minLen=3; maxLen=30)_
  - `dataSourceId` — string **(required)** — ID of the data source containing this document _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `createdAt` — string **(required)** — Timestamp when the document was created (ISO 8601 format). Example: 2021-01-01T00:00:00Z
  - `updatedAt` — string **(required)** — Timestamp when the document was last updated (ISO 8601 format). Example: 2021-01-01T00:00:00Z
  - `status` — string **(required)** _(enum: `draft`, `pending`, `processing`, `completed`, `failed`)_
  - `chunksCount` — number — Total number of text chunks the document was split into for semantic search and embedding. Higher numbers indicate more detailed indexing
  - `convertingDuration` — number — Time in milliseconds spent converting the document from its original format to markdown. Only populated after processing
  - `processingDuration` — number — Time in milliseconds spent chunking the document and generating embeddings for semantic search. Only populated after processing completes
  - `errorMessage` — string — Error message describing why document processing failed, if applicable. Only present when status is 'failed'

**`UpdateKnowledgeBaseRequestContent`**

- `name` — string **(required)** — Descriptive name for the knowledge base. Used for identification in the UI and APIs. Examples: 'Product Knowledge Base', 'Support Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
- `description` — string — Optional detailed description of the knowledge base content and purpose. Helps users understand what topics are covered. Examples: 'Comprehensive product documentation and service guides', 'Internal technical documentation'. Length: 0-1000 characters _(maxLen=1000)_
- `dataSources` — array **(required)** — List of data source IDs that provide content for this knowledge base. Can include Confluence, Google Drive, file uploads, and proxy sources. Empty list results in no searchable content
  - _array of_ `string`

**`UpdateKnowledgeBaseResponseContent`**

- `knowledgeBase` — KnowledgeBaseItem **(required)**
  - `name` — string **(required)** — Descriptive name for the knowledge base. Used for identification in the UI and APIs. Examples: 'Product Knowledge Base', 'Support Documentation'. Length: 2-100 characters _(minLen=2; maxLen=100)_
  - `description` — string — Optional detailed description of the knowledge base content and purpose. Helps users understand what topics are covered. Examples: 'Comprehensive product documentation and service guides', 'Internal technical documentation'. Length: 0-1000 characters _(maxLen=1000)_
  - `dataSources` — array **(required)** — List of data source IDs that provide content for this knowledge base. Can include Confluence, Google Drive, file uploads, and proxy sources. Empty list results in no searchable content
    - _array of_ `string`
  - `id` — string **(required)** — Unique identifier of the knowledge base _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `companyId` — string **(required)** — Company ID that owns this knowledge base _(minLen=3; maxLen=30)_
  - `createdAt` — string **(required)** — Timestamp when the knowledge base was created (ISO 8601 format). Example: 2021-01-01T00:00:00Z
  - `updatedAt` — string **(required)** — Timestamp when the knowledge base was last updated (ISO 8601 format). Example: 2021-01-01T00:00:00Z

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

**`WebsiteConfig`**

- `urls` — array **(required)** — Starting page URLs of the website to index. Must be https and resolve to a public address. The v1 console configures exactly one, but the field is a list so additional starting points can be added without a breaking change
  - _array of_ `string`
- `maxPages` — number — Upper bound on how many pages may be selected for indexing. Server-side limits still apply and take precedence _(min=1; max=2000)_
- `pages` — WebsitePagesConfig
  - `enabled` — array **(required)** — Absolute page URLs that should be fetched and indexed. These are the pages the user selected from the discovery result, and the complete set: anything absent is not indexed
    - _array of_ `string`

**`WebsiteDiscoveryStrategy`**

_Which discovery strategy produced a page list. Sitemap discovery is free and usually more complete; crawl is the fallback for sites without a usable sitemap_

- string _(enum: `sitemap`, `crawl`)_

**`WebsitePagesConfig`**

- `enabled` — array **(required)** — Absolute page URLs that should be fetched and indexed. These are the pages the user selected from the discovery result, and the complete set: anything absent is not indexed
  - _array of_ `string`

</details>
