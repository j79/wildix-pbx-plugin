## Cache API

_OpenAPI: WIM Cache service — version v2_

**Servers**

- `https://wim.wildix.com` — Production
- `https://wim-stable.wildix.com` — Stable
- `https://wim-stage.wildix.com` — Stage

### Other

#### `PUT` `/v1/cache/general`

Adds entities to the general cache

- operationId: `PutEntitiesToGeneralCache`
- **Request body** (`application/json` — `PutEntitiesToGeneralCacheRequestContent`)
  - `items` — array _(minItems=1; maxItems=1000)_
    - _array of_ `GeneralEntityInputData`
      - `IntegrationId` — string **(required)**
      - `IntegrationOrder` — number **(required)**
      - `Name` — string
      - `Id` — string
      - `Phone` — string
      - `Email` — string
      - `OwnerId` — string
      - `Avatar` — string
      - `UpdatedAt` — string
      - `CustomData` — GeneralDataMap
        - _map of_ `string`
- Errors: `400`, `403`, `429`

#### `DELETE` `/v1/cache/general`

Deleting entities to the general cache, requires one of the parameters: email or phone or clean

- operationId: `DeleteEntitiesFromGeneralCache`
- **Parameters**
  - `email` (query) — string — Email for delete _(minLen=1; maxLen=50)_
  - `phone` (query) — string — Phone for delete _(minLen=1; maxLen=30)_
  - `clean` (query) — boolean — Delete all general cache for the current user _(default=False)_
- Errors: `400`, `403`, `429`

#### `PUT` `/v1/cache/integration-data`

Batch upsert operation for storing integration data records in the cache

- operationId: `PutIntegrationData`
- **Request body** (`application/json` — `PutIntegrationDataRequestContent`) **(required)**
  - `items` — array **(required)** — Integration data records to upsert _(minItems=1; maxItems=100)_
    - _array of_ `IntegrationDataItemWithId`
      - `type` — string **(required)** — Integration data type _(minLen=1; maxLen=32)_
      - `data` — any **(required)** — Integration data
      - `id` — string **(required)** — Unique identifier _(minLen=1; maxLen=32)_
  - `companyId` — string — Company identifier should be provided only for S2S authorization _(minLen=3; maxLen=30)_
  - `integrationId` — string **(required)** — Integration identifier _(minLen=6; maxLen=6)_
- Errors: `400`, `403`, `429`

#### `POST` `/v1/cache/integration-data/batch-write`

Batch writes and deletes integration data in a single request

- operationId: `BatchWriteIntegrationData`
- **Request body** (`application/json` — `BatchWriteIntegrationDataRequestContent`) **(required)**
  - `putItems` — array — Records to upsert (optional). At least one of putItems or deleteItems must be present and non-empty. _(maxItems=100)_
    - _array of_ `IntegrationDataItemWithId`
      - `type` — string **(required)** — Integration data type _(minLen=1; maxLen=32)_
      - `data` — any **(required)** — Integration data
      - `id` — string **(required)** — Unique identifier _(minLen=1; maxLen=32)_
  - `deleteItems` — array — Record keys to delete (optional). At least one of putItems or deleteItems must be present and non-empty. _(maxItems=100)_
    - _array of_ `IntegrationDataKey`
      - `id` — string **(required)** — Unique identifier _(minLen=1; maxLen=32)_
      - `type` — string — Integration data type _(minLen=1; maxLen=32)_
  - `integrationId` — string **(required)** — Integration identifier _(minLen=6; maxLen=6)_
  - `companyId` — string — Company identifier should be provided only for S2S authorization _(minLen=3; maxLen=30)_
- Errors: `400`, `403`, `429`

#### `POST` `/v1/cache/integration-data/delete`

Batch deletion of integration data by id with optional filters

- operationId: `DeleteIntegrationData`
- **Request body** (`application/json` — `DeleteIntegrationDataRequestContent`) **(required)**
  - `items` — array **(required)** — Identifiers to delete _(minItems=1; maxItems=100)_
    - _array of_ `IntegrationDataKey`
      - `id` — string **(required)** — Unique identifier _(minLen=1; maxLen=32)_
      - `type` — string — Integration data type _(minLen=1; maxLen=32)_
  - `companyId` — string — Company identifier should be provided only for S2S authorization _(minLen=3; maxLen=30)_
- Errors: `400`, `403`, `429`

#### `POST` `/v1/cache/integration-data/get`

Batch retrieval of integration data by id with optional filters

- operationId: `GetIntegrationData`
- **Request body** (`application/json` — `GetIntegrationDataRequestContent`) **(required)**
  - `items` — array **(required)** — Identifiers to retrieve _(minItems=1; maxItems=100)_
    - _array of_ `IntegrationDataKey`
      - `id` — string **(required)** — Unique identifier _(minLen=1; maxLen=32)_
      - `type` — string — Integration data type _(minLen=1; maxLen=32)_
  - `companyId` — string — Company identifier should be provided only for S2S authorization _(minLen=3; maxLen=30)_
- **Response 200** (`GetIntegrationDataResponseContent`)
  - `items` — array **(required)**
    - _array of_ `IntegrationDataItem`
      - `type` — string **(required)** — Integration data type _(minLen=1; maxLen=32)_
      - `data` — any **(required)** — Integration data
      - `id` — string **(required)** — Unique identifier _(minLen=1; maxLen=32)_
      - `integrationId` — string **(required)** — Integration identifier _(minLen=6; maxLen=6)_
- Errors: `400`, `403`, `429`

#### `POST` `/v1/cache/object`

Allows to retrieve entities by id, use only in backend integrations

- operationId: `GetEntitiesByIds`
- **Request body** (`application/json` — `GetEntitiesByIdsRequestContent`) **(required)**
  - `organizationId` — string — Organization identifier _(minLen=1; maxLen=30)_
  - `entityIds` — array **(required)** — Unique Entities identifiers _(minItems=1; maxItems=50)_
    - _array of_ `string`
- **Response 200** (`GetEntitiesByIdsResponseContent`)
  - `items` — array
    - _array of_ `Entity`
      - `integrationId` — string **(required)**
      - `entityType` — string **(required)**
      - `data` — EntityData **(required)**
        - `Id` — string
        - `Name` — string
        - `FirstName` — string
        - `LastName` — string
        - `Phone` — string
        - `Email` — string
        - `OwnerId` — string
        - `MobilePhone` — string
        - `AccountId` — string
        - `Company` — string
        - `IsConverted` — boolean
        - `LastModifiedDate` — string
        - `CompanyName` — string
        - `IsActive` — boolean
        - `TimeZoneSidKey` — string
        - `Extension` — string
        - `PersonMobilePhone` — string
        - `PersonOtherPhone` — string
        - `attributes` — SalesforceAttrubuteField
          - `url` — string
          - `type` — string
        - `CallPhone` — string
        - `Archived` — boolean
        - `Domain` — string
        - `UpdatedAt` — string
        - `Avatar` — string
        - `CustomData` — GeneralDataMap
          - _map of_ `string`
      - `weight` — number
      - `integrationOrder` — number
- Errors: `400`, `403`, `429`

#### `GET` `/v1/cache/search`

Searches for entities, unlike a POST request allows to specify additional parameters such as 'query', 'from', and 'size'. requires one of the parameters: query or email or phone

- operationId: `SearchEntitiesByParams`
- **Parameters**
  - `organizationId` (query) — string — Unique organization identifier _(minLen=1; maxLen=30)_
  - `phone` (query) — string — Phone for search _(minLen=1; maxLen=30)_
  - `email` (query) — string — Email for search _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
  - `query` (query) — string — Query string for search (use only for Backend auto loging integrations) _(minLen=1; maxLen=50)_
  - `from` (query) — number — Starting document offset. Needs to by non-negative and defaults to 0 _(min=1; max=1000)_
  - `size` (query) — number — Defines the number of hits to return. Defaults to 10 _(default=10; min=1; max=100)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `userId` (query) — string — The unique identifier of the user when a service or PBX token is used. _(minLen=12; maxLen=12)_
- **Response 200** (`SearchEntitiesByParamsResponseContent`)
  - `items` — array
    - _array of_ `SearchResult`
      - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `phone` — string
      - `items` — array
        - _array of_ `Entity`
          - `integrationId` — string **(required)**
          - `entityType` — string **(required)**
          - `data` — EntityData **(required)**
            - `Id` — string
            - `Name` — string
            - `FirstName` — string
            - `LastName` — string
            - `Phone` — string
            - `Email` — string
            - `OwnerId` — string
            - `MobilePhone` — string
            - `AccountId` — string
            - `Company` — string
            - `IsConverted` — boolean
            - `LastModifiedDate` — string
            - `CompanyName` — string
            - `IsActive` — boolean
            - `TimeZoneSidKey` — string
            - `Extension` — string
            - `PersonMobilePhone` — string
            - `PersonOtherPhone` — string
            - `attributes` — SalesforceAttrubuteField
              - _(nesting depth limit — see `SalesforceAttrubuteField` in the Schemas appendix)_
            - `CallPhone` — string
            - `Archived` — boolean
            - `Domain` — string
            - `UpdatedAt` — string
            - `Avatar` — string
            - `CustomData` — GeneralDataMap
              - _(nesting depth limit — see `GeneralDataMap` in the Schemas appendix)_
          - `weight` — number
          - `integrationOrder` — number
- Errors: `400`, `403`, `429`

#### `POST` `/v1/cache/search`

searches for entities, unlike a GET request, allows you to specify more matching parameters

- operationId: `SearchEntitiesByListParams`
- **Request body** (`application/json` — `SearchEntitiesByListParamsRequestContent`) **(required)**
  - `organizationId` — string — Organization identifier _(minLen=1; maxLen=30)_
  - `params` — array **(required)** — Params for search _(minItems=1; maxItems=100)_
    - _array of_ `SearchPostParams`
      - `phone` — string — Phone for search _(minLen=1; maxLen=30)_
      - `email` — string — Email for search _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
- **Response 200** (`SearchEntitiesByListParamsResponseContent`)
  - `items` — array
    - _array of_ `SearchResult`
      - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `phone` — string
      - `items` — array
        - _array of_ `Entity`
          - `integrationId` — string **(required)**
          - `entityType` — string **(required)**
          - `data` — EntityData **(required)**
            - `Id` — string
            - `Name` — string
            - `FirstName` — string
            - `LastName` — string
            - `Phone` — string
            - `Email` — string
            - `OwnerId` — string
            - `MobilePhone` — string
            - `AccountId` — string
            - `Company` — string
            - `IsConverted` — boolean
            - `LastModifiedDate` — string
            - `CompanyName` — string
            - `IsActive` — boolean
            - `TimeZoneSidKey` — string
            - `Extension` — string
            - `PersonMobilePhone` — string
            - `PersonOtherPhone` — string
            - `attributes` — SalesforceAttrubuteField
              - _(nesting depth limit — see `SalesforceAttrubuteField` in the Schemas appendix)_
            - `CallPhone` — string
            - `Archived` — boolean
            - `Domain` — string
            - `UpdatedAt` — string
            - `Avatar` — string
            - `CustomData` — GeneralDataMap
              - _(nesting depth limit — see `GeneralDataMap` in the Schemas appendix)_
          - `weight` — number
          - `integrationOrder` — number
- Errors: `400`, `403`, `429`

#### `POST` `/v1/cache/sync`

Allows to run target integration synchronization

- operationId: `SyncCache`
- **Request body** (`application/json` — `SyncCacheRequestContent`) **(required)**
  - `organizationId` — string **(required)** — Organization identifier _(minLen=1; maxLen=30)_
- **Response 200** (`SyncCacheResponseContent`)
  - `success` — boolean
- Errors: `400`, `403`, `429`

#### `POST` `/v1/cache/weight`

Allows for batch updating the weight property of multiple entities

- operationId: `UpdateEntitiesWeight`
- **Request body** (`application/json` — `UpdateEntitiesWeightRequestContent`) **(required)**
  - `organizationId` — string **(required)** — Organization identifier _(minLen=15; maxLen=18)_
  - `entityIds` — array **(required)** — Unique Entities identifiers _(minItems=1; maxItems=10)_
    - _array of_ `string`
- **Response 200** (`UpdateEntitiesWeightResponseContent`)
  - `success` — boolean **(required)**
- Errors: `400`, `403`, `429`

### Schemas appendix — Cache API

<details><summary>28 component schemas</summary>

**`BatchWriteIntegrationDataRequestContent`**

- `putItems` — array — Records to upsert (optional). At least one of putItems or deleteItems must be present and non-empty. _(maxItems=100)_
  - _array of_ `IntegrationDataItemWithId`
    - `type` — string **(required)** — Integration data type _(minLen=1; maxLen=32)_
    - `data` — any **(required)** — Integration data
    - `id` — string **(required)** — Unique identifier _(minLen=1; maxLen=32)_
- `deleteItems` — array — Record keys to delete (optional). At least one of putItems or deleteItems must be present and non-empty. _(maxItems=100)_
  - _array of_ `IntegrationDataKey`
    - `id` — string **(required)** — Unique identifier _(minLen=1; maxLen=32)_
    - `type` — string — Integration data type _(minLen=1; maxLen=32)_
- `integrationId` — string **(required)** — Integration identifier _(minLen=6; maxLen=6)_
- `companyId` — string — Company identifier should be provided only for S2S authorization _(minLen=3; maxLen=30)_

**`DeleteIntegrationDataRequestContent`**

- `items` — array **(required)** — Identifiers to delete _(minItems=1; maxItems=100)_
  - _array of_ `IntegrationDataKey`
    - `id` — string **(required)** — Unique identifier _(minLen=1; maxLen=32)_
    - `type` — string — Integration data type _(minLen=1; maxLen=32)_
- `companyId` — string — Company identifier should be provided only for S2S authorization _(minLen=3; maxLen=30)_

**`Entity`**

- `integrationId` — string **(required)**
- `entityType` — string **(required)**
- `data` — EntityData **(required)**
  - `Id` — string
  - `Name` — string
  - `FirstName` — string
  - `LastName` — string
  - `Phone` — string
  - `Email` — string
  - `OwnerId` — string
  - `MobilePhone` — string
  - `AccountId` — string
  - `Company` — string
  - `IsConverted` — boolean
  - `LastModifiedDate` — string
  - `CompanyName` — string
  - `IsActive` — boolean
  - `TimeZoneSidKey` — string
  - `Extension` — string
  - `PersonMobilePhone` — string
  - `PersonOtherPhone` — string
  - `attributes` — SalesforceAttrubuteField
    - `url` — string
    - `type` — string
  - `CallPhone` — string
  - `Archived` — boolean
  - `Domain` — string
  - `UpdatedAt` — string
  - `Avatar` — string
  - `CustomData` — GeneralDataMap
    - _map of_ `string`
- `weight` — number
- `integrationOrder` — number

**`EntityData`**

- `Id` — string
- `Name` — string
- `FirstName` — string
- `LastName` — string
- `Phone` — string
- `Email` — string
- `OwnerId` — string
- `MobilePhone` — string
- `AccountId` — string
- `Company` — string
- `IsConverted` — boolean
- `LastModifiedDate` — string
- `CompanyName` — string
- `IsActive` — boolean
- `TimeZoneSidKey` — string
- `Extension` — string
- `PersonMobilePhone` — string
- `PersonOtherPhone` — string
- `attributes` — SalesforceAttrubuteField
  - `url` — string
  - `type` — string
- `CallPhone` — string
- `Archived` — boolean
- `Domain` — string
- `UpdatedAt` — string
- `Avatar` — string
- `CustomData` — GeneralDataMap
  - _map of_ `string`

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GeneralDataMap`**

- _map of_ `string`

**`GeneralEntityInputData`**

- `IntegrationId` — string **(required)**
- `IntegrationOrder` — number **(required)**
- `Name` — string
- `Id` — string
- `Phone` — string
- `Email` — string
- `OwnerId` — string
- `Avatar` — string
- `UpdatedAt` — string
- `CustomData` — GeneralDataMap
  - _map of_ `string`

**`GetEntitiesByIdsRequestContent`**

- `organizationId` — string — Organization identifier _(minLen=1; maxLen=30)_
- `entityIds` — array **(required)** — Unique Entities identifiers _(minItems=1; maxItems=50)_
  - _array of_ `string`

**`GetEntitiesByIdsResponseContent`**

- `items` — array
  - _array of_ `Entity`
    - `integrationId` — string **(required)**
    - `entityType` — string **(required)**
    - `data` — EntityData **(required)**
      - `Id` — string
      - `Name` — string
      - `FirstName` — string
      - `LastName` — string
      - `Phone` — string
      - `Email` — string
      - `OwnerId` — string
      - `MobilePhone` — string
      - `AccountId` — string
      - `Company` — string
      - `IsConverted` — boolean
      - `LastModifiedDate` — string
      - `CompanyName` — string
      - `IsActive` — boolean
      - `TimeZoneSidKey` — string
      - `Extension` — string
      - `PersonMobilePhone` — string
      - `PersonOtherPhone` — string
      - `attributes` — SalesforceAttrubuteField
        - _(nesting depth limit — see `SalesforceAttrubuteField` in the Schemas appendix)_
      - `CallPhone` — string
      - `Archived` — boolean
      - `Domain` — string
      - `UpdatedAt` — string
      - `Avatar` — string
      - `CustomData` — GeneralDataMap
        - _(nesting depth limit — see `GeneralDataMap` in the Schemas appendix)_
    - `weight` — number
    - `integrationOrder` — number

**`GetIntegrationDataRequestContent`**

- `items` — array **(required)** — Identifiers to retrieve _(minItems=1; maxItems=100)_
  - _array of_ `IntegrationDataKey`
    - `id` — string **(required)** — Unique identifier _(minLen=1; maxLen=32)_
    - `type` — string — Integration data type _(minLen=1; maxLen=32)_
- `companyId` — string — Company identifier should be provided only for S2S authorization _(minLen=3; maxLen=30)_

**`GetIntegrationDataResponseContent`**

- `items` — array **(required)**
  - _array of_ `IntegrationDataItem`
    - `type` — string **(required)** — Integration data type _(minLen=1; maxLen=32)_
    - `data` — any **(required)** — Integration data
    - `id` — string **(required)** — Unique identifier _(minLen=1; maxLen=32)_
    - `integrationId` — string **(required)** — Integration identifier _(minLen=6; maxLen=6)_

**`IntegrationDataItem`**

- `type` — string **(required)** — Integration data type _(minLen=1; maxLen=32)_
- `data` — any **(required)** — Integration data
- `id` — string **(required)** — Unique identifier _(minLen=1; maxLen=32)_
- `integrationId` — string **(required)** — Integration identifier _(minLen=6; maxLen=6)_

**`IntegrationDataItemWithId`**

- `type` — string **(required)** — Integration data type _(minLen=1; maxLen=32)_
- `data` — any **(required)** — Integration data
- `id` — string **(required)** — Unique identifier _(minLen=1; maxLen=32)_

**`IntegrationDataKey`**

- `id` — string **(required)** — Unique identifier _(minLen=1; maxLen=32)_
- `type` — string — Integration data type _(minLen=1; maxLen=32)_

**`PutEntitiesToGeneralCacheRequestContent`**

- `items` — array _(minItems=1; maxItems=1000)_
  - _array of_ `GeneralEntityInputData`
    - `IntegrationId` — string **(required)**
    - `IntegrationOrder` — number **(required)**
    - `Name` — string
    - `Id` — string
    - `Phone` — string
    - `Email` — string
    - `OwnerId` — string
    - `Avatar` — string
    - `UpdatedAt` — string
    - `CustomData` — GeneralDataMap
      - _map of_ `string`

**`PutIntegrationDataRequestContent`**

- `items` — array **(required)** — Integration data records to upsert _(minItems=1; maxItems=100)_
  - _array of_ `IntegrationDataItemWithId`
    - `type` — string **(required)** — Integration data type _(minLen=1; maxLen=32)_
    - `data` — any **(required)** — Integration data
    - `id` — string **(required)** — Unique identifier _(minLen=1; maxLen=32)_
- `companyId` — string — Company identifier should be provided only for S2S authorization _(minLen=3; maxLen=30)_
- `integrationId` — string **(required)** — Integration identifier _(minLen=6; maxLen=6)_

**`RateLimitExceededExceptionResponseContent`**

- `message` — string **(required)** _(default=Too Many Requests)_

**`SalesforceAttrubuteField`**

- `url` — string
- `type` — string

**`SearchEntitiesByListParamsRequestContent`**

- `organizationId` — string — Organization identifier _(minLen=1; maxLen=30)_
- `params` — array **(required)** — Params for search _(minItems=1; maxItems=100)_
  - _array of_ `SearchPostParams`
    - `phone` — string — Phone for search _(minLen=1; maxLen=30)_
    - `email` — string — Email for search _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_

**`SearchEntitiesByListParamsResponseContent`**

- `items` — array
  - _array of_ `SearchResult`
    - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `phone` — string
    - `items` — array
      - _array of_ `Entity`
        - _(nesting depth limit — see `Entity` in the Schemas appendix)_

**`SearchEntitiesByParamsResponseContent`**

- `items` — array
  - _array of_ `SearchResult`
    - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `phone` — string
    - `items` — array
      - _array of_ `Entity`
        - _(nesting depth limit — see `Entity` in the Schemas appendix)_

**`SearchPostParams`**

- `phone` — string — Phone for search _(minLen=1; maxLen=30)_
- `email` — string — Email for search _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_

**`SearchResult`**

- `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
- `phone` — string
- `items` — array
  - _array of_ `Entity`
    - `integrationId` — string **(required)**
    - `entityType` — string **(required)**
    - `data` — EntityData **(required)**
      - `Id` — string
      - `Name` — string
      - `FirstName` — string
      - `LastName` — string
      - `Phone` — string
      - `Email` — string
      - `OwnerId` — string
      - `MobilePhone` — string
      - `AccountId` — string
      - `Company` — string
      - `IsConverted` — boolean
      - `LastModifiedDate` — string
      - `CompanyName` — string
      - `IsActive` — boolean
      - `TimeZoneSidKey` — string
      - `Extension` — string
      - `PersonMobilePhone` — string
      - `PersonOtherPhone` — string
      - `attributes` — SalesforceAttrubuteField
        - _(nesting depth limit — see `SalesforceAttrubuteField` in the Schemas appendix)_
      - `CallPhone` — string
      - `Archived` — boolean
      - `Domain` — string
      - `UpdatedAt` — string
      - `Avatar` — string
      - `CustomData` — GeneralDataMap
        - _(nesting depth limit — see `GeneralDataMap` in the Schemas appendix)_
    - `weight` — number
    - `integrationOrder` — number

**`SyncCacheRequestContent`**

- `organizationId` — string **(required)** — Organization identifier _(minLen=1; maxLen=30)_

**`SyncCacheResponseContent`**

- `success` — boolean

**`UpdateEntitiesWeightRequestContent`**

- `organizationId` — string **(required)** — Organization identifier _(minLen=15; maxLen=18)_
- `entityIds` — array **(required)** — Unique Entities identifiers _(minItems=1; maxItems=10)_
  - _array of_ `string`

**`UpdateEntitiesWeightResponseContent`**

- `success` — boolean **(required)**

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

</details>
