## Integrations API

_OpenAPI: WIM integrations service — version v2_

**Servers**

- `https://wim.wildix.com` — Production
- `https://wim-stable.wildix.com` — Stable
- `https://wim-stage.wildix.com` — Stage

### Other

#### `PUT` `/v2/integrations`

Creates multiple integrations in a single batch operation.

- operationId: `CreateIntegrations`
- **Scopes**: `integrations:CreateIntegrations`
- **Request body** (`application/json` — `CreateIntegrationsRequestContent`) **(required)**
  - `integrations` — array **(required)**
    - _array of_ `PutIntegrationDataItem`
      - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
      - `entityType` — string _(enum: `sf_partner`, `main`)_
      - `statusChangeDate` — string
      - `errorInfo` — any
      - `warningInfo` — any
      - `data` — any — Data for integration
      - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
      - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
      - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
- **Response 200** (`CreateIntegrationsResponseContent`)
  - `integrations` — array **(required)**
    - _array of_ `Integration`
      - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
      - `entityType` — string _(enum: `sf_partner`, `main`)_
      - `statusChangeDate` — string
      - `errorInfo` — any
      - `warningInfo` — any
      - `data` — any — Data for integration
      - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
      - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
      - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
      - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
      - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
      - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated
- Errors: `400`, `403`, `404`

#### `POST` `/v2/integrations/bulk/delete`

> ⚠️ Route marquée `deprecated` dans la spécification publiée.

Deletes multiple integrations in a single batch operation. This is a deprecated operation - use DeleteIntegrations instead.

- operationId: `BulkDeleteIntegrations`
- **Scopes**: `integrations:BulkDeleteIntegrations`
- **Request body** (`application/json` — `BulkDeleteIntegrationsRequestContent`) **(required)**
  - `keys` — array **(required)**
    - _array of_ `Keys`
      - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
      - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
- Errors: `400`, `403`, `404`

#### `PUT` `/v2/integrations/bulk/put`

> ⚠️ Route marquée `deprecated` dans la spécification publiée.

Creates multiple integrations in a single batch operation. This is a deprecated operation - use CreateIntegrations instead.

- operationId: `BulkPutIntegrations`
- **Scopes**: `integrations:BulkPutIntegrations`
- **Request body** (`application/json` — `BulkPutIntegrationsRequestContent`) **(required)**
  - `integrations` — array **(required)**
    - _array of_ `PutIntegrationDataItem`
      - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
      - `entityType` — string _(enum: `sf_partner`, `main`)_
      - `statusChangeDate` — string
      - `errorInfo` — any
      - `warningInfo` — any
      - `data` — any — Data for integration
      - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
      - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
      - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
- **Response 200** (`BulkPutIntegrationsResponseContent`)
  - `items` — array **(required)**
    - _array of_ `Integration`
      - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
      - `entityType` — string _(enum: `sf_partner`, `main`)_
      - `statusChangeDate` — string
      - `errorInfo` — any
      - `warningInfo` — any
      - `data` — any — Data for integration
      - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
      - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
      - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
      - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
      - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
      - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated
- Errors: `400`, `403`, `404`

#### `GET` `/v2/integrations/by-companys-and-services`

> ⚠️ Route marquée `deprecated` dans la spécification publiée.

Retrieves integrations filtered by multiple companies and services. This is a deprecated operation - use ListIntegrations instead.

- operationId: `GetIntegrationsByCompaniesAndServices`
- **Scopes**: `integrations:GetIntegrationsByCompaniesAndServices`, `integrations:read`
- **Parameters**
  - `companies` (query) — array _(minItems=1)_
  - `services` (query) — array _(minItems=1)_
- **Response 200** (`GetIntegrationsByCompaniesAndServicesResponseContent`)
  - `items` — array **(required)**
    - _array of_ `Integration`
      - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
      - `entityType` — string _(enum: `sf_partner`, `main`)_
      - `statusChangeDate` — string
      - `errorInfo` — any
      - `warningInfo` — any
      - `data` — any — Data for integration
      - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
      - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
      - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
      - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
      - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
      - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated
- Errors: `400`, `403`, `404`

#### `GET` `/v2/integrations/by-id/{integrationId}`

> ⚠️ Route marquée `deprecated` dans la spécification publiée.

Retrieves details of a specific integration by its unique identifier. This is a deprecated operation - use GetIntegration instead.

- operationId: `GetIntegrationById`
- **Scopes**: `integrations:GetIntegrationById`, `integrations:read`
- **Parameters**
  - `integrationId` (path) — string **(required)** _(minLen=6; maxLen=6)_
  - `companyId` (query) — string _(minLen=3; maxLen=30)_
- **Response 200** (`GetIntegrationByIdResponseContent`)
  - `item` — Integration **(required)**
    - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
    - `entityType` — string _(enum: `sf_partner`, `main`)_
    - `statusChangeDate` — string
    - `errorInfo` — any
    - `warningInfo` — any
    - `data` — any — Data for integration
    - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
    - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
    - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
    - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated
- Errors: `400`, `403`, `404`

#### `GET` `/v2/integrations/companies`

> ⚠️ Route marquée `deprecated` dans la spécification publiée.

Retrieves a list of all companies with their integration information. This is a deprecated operation - use ListIntegrations instead.

- operationId: `GetCompanyIntegrationList`
- **Scopes**: `integrations:GetCompanyIntegrationList`, `integrations:read`
- **Response 200** (`GetCompanyIntegrationListResponseContent`)
  - `items` — array **(required)**
    - _array of_ `CompanyIntegrations`
      - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
      - `briefIntegrationList` — array **(required)**
        - _array of_ `BriefIntegration`
          - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
          - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
- Errors: `400`, `403`, `404`

#### `GET` `/v2/integrations/companies/{companyId}`

> ⚠️ Route marquée `deprecated` dans la spécification publiée.

Retrieves all integrations for a specific company. This is a deprecated operation - use ListIntegrations instead.

- operationId: `GetIntegrationsByCompanyId`
- **Scopes**: `integrations:GetIntegrationsByCompanyId`, `integrations:read`
- **Parameters**
  - `companyId` (path) — string **(required)** _(minLen=3; maxLen=30)_
  - `onlyPublic` (query) — boolean
- **Response 200** (`GetIntegrationsByCompanyIdResponseContent`)
  - `items` — array **(required)**
    - _array of_ `Integration`
      - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
      - `entityType` — string _(enum: `sf_partner`, `main`)_
      - `statusChangeDate` — string
      - `errorInfo` — any
      - `warningInfo` — any
      - `data` — any — Data for integration
      - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
      - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
      - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
      - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
      - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
      - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated
- Errors: `400`, `403`, `404`

#### `PUT` `/v2/integrations/companies/{companyId}`

> ⚠️ Route marquée `deprecated` dans la spécification publiée.

Creates or updates an integration for a specific company. This is a deprecated operation - use CreateIntegration instead.

- operationId: `PutIntegration`
- **Scopes**: `integrations:PutIntegration`
- **Parameters**
  - `companyId` (path) — string **(required)** _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `PutIntegrationRequestContent`) **(required)**
  - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
  - `entityType` — string _(enum: `sf_partner`, `main`)_
  - `statusChangeDate` — string
  - `errorInfo` — any
  - `warningInfo` — any
  - `data` — any — Data for integration
  - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
  - `integrationId` — string _(minLen=6; maxLen=6)_
- **Response 200** (`PutIntegrationResponseContent`)
  - `item` — Integration **(required)**
    - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
    - `entityType` — string _(enum: `sf_partner`, `main`)_
    - `statusChangeDate` — string
    - `errorInfo` — any
    - `warningInfo` — any
    - `data` — any — Data for integration
    - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
    - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
    - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
    - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated
- Errors: `400`, `403`, `404`

#### `PATCH` `/v2/integrations/companies/{companyId}/integrations/{integrationId}`

> ⚠️ Route marquée `deprecated` dans la spécification publiée.

Updates an existing integration for a specific company. This is a deprecated operation - use UpdateIntegration instead.

- operationId: `PatchIntegration`
- **Scopes**: `integrations:PatchIntegration`
- **Parameters**
  - `companyId` (path) — string **(required)** _(minLen=3; maxLen=30)_
  - `integrationId` (path) — string **(required)** _(minLen=6; maxLen=6)_
- **Request body** (`application/json` — `PatchIntegrationRequestContent`)
  - `externalId` — string — Deprecated. Will use companyId instead This shape is deprecated. _(minLen=3; maxLen=30; deprecated)_
  - `service` — string _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
  - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
  - `entityType` — string _(enum: `sf_partner`, `main`)_
  - `statusChangeDate` — string
  - `errorInfo` — any
  - `warningInfo` — any
  - `data` — any — Data for integration
- **Response 200** (`PatchIntegrationResponseContent`)
  - `item` — Integration **(required)**
    - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
    - `entityType` — string _(enum: `sf_partner`, `main`)_
    - `statusChangeDate` — string
    - `errorInfo` — any
    - `warningInfo` — any
    - `data` — any — Data for integration
    - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
    - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
    - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
    - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated
- Errors: `400`, `403`, `404`

#### `DELETE` `/v2/integrations/companies/{companyId}/integrations/{integrationId}`

> ⚠️ Route marquée `deprecated` dans la spécification publiée.

Removes an existing integration for a specific company. This is a deprecated operation - use DeleteIntegration instead.

- operationId: `RemoveIntegration`
- **Scopes**: `integrations:RemoveIntegration`
- **Parameters**
  - `integrationId` (path) — string **(required)** _(minLen=6; maxLen=6)_
  - `companyId` (path) — string **(required)** _(minLen=3; maxLen=30)_
- Errors: `400`, `403`, `404`

#### `PUT` `/v2/integrations/company/{companyId}`

Creates a new integration for the specified company with the provided configuration.

- operationId: `CreateIntegration`
- **Scopes**: `integrations:CreateIntegration`
- **Parameters**
  - `companyId` (path) — string **(required)** _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `CreateIntegrationRequestContent`) **(required)**
  - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
  - `entityType` — string _(enum: `sf_partner`, `main`)_
  - `statusChangeDate` — string
  - `errorInfo` — any
  - `warningInfo` — any
  - `data` — any — Data for integration
  - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
- **Response 200** (`CreateIntegrationResponseContent`)
  - `integration` — Integration **(required)**
    - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
    - `entityType` — string _(enum: `sf_partner`, `main`)_
    - `statusChangeDate` — string
    - `errorInfo` — any
    - `warningInfo` — any
    - `data` — any — Data for integration
    - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
    - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
    - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
    - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated
- Errors: `400`, `403`, `404`

#### `PATCH` `/v2/integrations/company/{companyId}/integration/{integrationId}`

Updates the configuration of an existing integration for the specified company.

- operationId: `UpdateIntegration`
- **Scopes**: `integrations:UpdateIntegration`
- **Parameters**
  - `companyId` (path) — string **(required)** _(minLen=3; maxLen=30)_
  - `integrationId` (path) — string **(required)** _(minLen=6; maxLen=6)_
- **Request body** (`application/json` — `UpdateIntegrationRequestContent`)
  - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
  - `entityType` — string _(enum: `sf_partner`, `main`)_
  - `statusChangeDate` — string
  - `errorInfo` — any
  - `warningInfo` — any
  - `data` — any — Data for integration
  - `service` — string _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
- **Response 200** (`UpdateIntegrationResponseContent`)
  - `integration` — Integration **(required)**
    - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
    - `entityType` — string _(enum: `sf_partner`, `main`)_
    - `statusChangeDate` — string
    - `errorInfo` — any
    - `warningInfo` — any
    - `data` — any — Data for integration
    - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
    - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
    - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
    - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated
- Errors: `400`, `403`, `404`

#### `DELETE` `/v2/integrations/company/{companyId}/integration/{integrationId}`

Deletes an existing integration for the specified company and integration ID.

- operationId: `DeleteIntegration`
- **Scopes**: `integrations:DeleteIntegration`
- **Parameters**
  - `companyId` (path) — string **(required)** _(minLen=3; maxLen=30)_
  - `integrationId` (path) — string **(required)** _(minLen=6; maxLen=6)_
- Errors: `400`, `403`, `404`

#### `POST` `/v2/integrations/delete`

Deletes multiple integrations in a single batch operation, either by integration IDs or company IDs.

- operationId: `DeleteIntegrations`
- **Scopes**: `integrations:DeleteIntegrations`
- **Request body** (`application/json` — `DeleteIntegrationsRequestContent`)
  - `integrationIds` — array — If specified, `companyIds` is ignored.
    - _array of_ `string`
  - `companyIds` — array
    - _array of_ `string`
- Errors: `400`, `403`, `404`

#### `GET` `/v2/integrations/integration/{integrationId}`

Retrieves details of a specific integration by its unique identifier.

- operationId: `GetIntegration`
- **Scopes**: `integrations:GetIntegration`, `integrations:read`
- **Parameters**
  - `integrationId` (path) — string **(required)** _(minLen=6; maxLen=6)_
- **Response 200** (`GetIntegrationResponseContent`)
  - `integration` — Integration **(required)**
    - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
    - `entityType` — string _(enum: `sf_partner`, `main`)_
    - `statusChangeDate` — string
    - `errorInfo` — any
    - `warningInfo` — any
    - `data` — any — Data for integration
    - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
    - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
    - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
    - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated
- Errors: `400`, `403`, `404`

#### `POST` `/v2/integrations/list`

Retrieves a paginated list of integrations with optional filtering by company, service, status, and custom field filters.

- operationId: `ListIntegrations`
- **Scopes**: `integrations:ListIntegrations`, `integrations:read`
- **Request body** (`application/json` — `ListIntegrationsRequestContent`)
  - `integrationIds` — array — If specified, filters by `companyIds` and `services` are ignored.
    - _array of_ `string`
  - `companyIds` — array
    - _array of_ `string`
  - `services` — array
    - _array of_ `string`
  - `excludedStatuses` — array — List of integration statuses to ignore in the selection.
    - _array of_ `IntegrationStatusType`
  - `onlyPublic` — boolean — Filter public integrations.
  - `filters` — array — Advanced field filters using dot notation. Each filter should be in the format 'field=value'. Examples: 'data.hubspot_hub_id=12345', 'entityType=main', 'data.tenant=my_tenant'
    - _array of_ `string`
  - `pageSize` — number — The number of integrations to return per page. _(default=100; min=1; max=100)_
  - `nextToken` — string — The token to use to get the next page of results.
- **Response 200** (`ListIntegrationsResponseContent`)
  - `integrations` — array **(required)**
    - _array of_ `Integration`
      - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
      - `entityType` — string _(enum: `sf_partner`, `main`)_
      - `statusChangeDate` — string
      - `errorInfo` — any
      - `warningInfo` — any
      - `data` — any — Data for integration
      - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
      - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
      - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
      - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
      - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
      - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated
  - `nextToken` — string
- Errors: `400`, `403`, `404`

#### `GET` `/v2/integrations/services`

> ⚠️ Route marquée `deprecated` dans la spécification publiée.

Retrieves all integrations for multiple services. This is a deprecated operation - use ListIntegrations instead.

- operationId: `GetIntegrationsByServices`
- **Scopes**: `integrations:GetIntegrationsByServices`, `integrations:read`
- **Parameters**
  - `services` (query) — array **(required)**
- **Response 200** (`GetIntegrationsByServicesResponseContent`)
  - `items` — array **(required)**
    - _array of_ `Integration`
      - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
      - `entityType` — string _(enum: `sf_partner`, `main`)_
      - `statusChangeDate` — string
      - `errorInfo` — any
      - `warningInfo` — any
      - `data` — any — Data for integration
      - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
      - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
      - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
      - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
      - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
      - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated
- Errors: `400`, `403`, `404`

#### `GET` `/v2/integrations/services/{service}`

> ⚠️ Route marquée `deprecated` dans la spécification publiée.

Retrieves all integrations for a specific service with optional filtering. This is a deprecated operation - use ListIntegrations instead.

- operationId: `GetIntegrationsByService`
- **Scopes**: `integrations:GetIntegrationsByService`, `integrations:read`
- **Parameters**
  - `service` (path) — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
  - `filter[hubspot_hub_id]` (query) — number — Filter by hub_id for hubspot_backend integration.
  - `filter[tenant]` (query) — string — Filter by tenant for microsoft_presence integration.
  - `filter[entityType]` (query) — string — Filter by tenant for entityType integration. _(enum: `sf_partner`, `main`)_
- **Response 200** (`GetIntegrationsByServiceResponseContent`)
  - `items` — array **(required)**
    - _array of_ `Integration`
      - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
      - `entityType` — string _(enum: `sf_partner`, `main`)_
      - `statusChangeDate` — string
      - `errorInfo` — any
      - `warningInfo` — any
      - `data` — any — Data for integration
      - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
      - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
      - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
      - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
      - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
      - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated
- Errors: `400`, `403`, `404`

#### `GET` `/v2/integrations/webhook`

Fetch the whole list of webhook integrations

- operationId: `ListWebhookIntegrations`
- **Scopes**: `integrations:ListWebhookIntegrations`, `integrations:read`
- **Response 200** (`ListWebhookIntegrationsResponseContent`)
  - `integrations` — array **(required)**
    - _array of_ `WebhookIntegration`
      - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
      - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
      - `type` — string **(required)** _(enum: `sqs`, `webhook`)_
      - `url` — string **(required)**
      - `key` — string **(required)**
      - `secret` — string **(required)**
      - `filter` — array **(required)**
        - _array of_ `string`
- Errors: `400`, `403`, `404`

### Schemas appendix — Integrations API

<details><summary>37 component schemas</summary>

**`BriefIntegration`**

- `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
- `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_

**`BulkDeleteIntegrationsRequestContent`**

- `keys` — array **(required)**
  - _array of_ `Keys`
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_

**`BulkPutIntegrationsRequestContent`**

- `integrations` — array **(required)**
  - _array of_ `PutIntegrationDataItem`
    - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
    - `entityType` — string _(enum: `sf_partner`, `main`)_
    - `statusChangeDate` — string
    - `errorInfo` — any
    - `warningInfo` — any
    - `data` — any — Data for integration
    - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_

**`BulkPutIntegrationsResponseContent`**

- `items` — array **(required)**
  - _array of_ `Integration`
    - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
    - `entityType` — string _(enum: `sf_partner`, `main`)_
    - `statusChangeDate` — string
    - `errorInfo` — any
    - `warningInfo` — any
    - `data` — any — Data for integration
    - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
    - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
    - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
    - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated

**`CompanyIntegrations`**

- `companyId` — string **(required)** _(minLen=3; maxLen=30)_
- `briefIntegrationList` — array **(required)**
  - _array of_ `BriefIntegration`
    - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
    - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_

**`CreateIntegrationRequestContent`**

- `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
- `entityType` — string _(enum: `sf_partner`, `main`)_
- `statusChangeDate` — string
- `errorInfo` — any
- `warningInfo` — any
- `data` — any — Data for integration
- `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_

**`CreateIntegrationResponseContent`**

- `integration` — Integration **(required)**
  - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
  - `entityType` — string _(enum: `sf_partner`, `main`)_
  - `statusChangeDate` — string
  - `errorInfo` — any
  - `warningInfo` — any
  - `data` — any — Data for integration
  - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
  - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
  - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
  - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated

**`CreateIntegrationsRequestContent`**

- `integrations` — array **(required)**
  - _array of_ `PutIntegrationDataItem`
    - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
    - `entityType` — string _(enum: `sf_partner`, `main`)_
    - `statusChangeDate` — string
    - `errorInfo` — any
    - `warningInfo` — any
    - `data` — any — Data for integration
    - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_

**`CreateIntegrationsResponseContent`**

- `integrations` — array **(required)**
  - _array of_ `Integration`
    - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
    - `entityType` — string _(enum: `sf_partner`, `main`)_
    - `statusChangeDate` — string
    - `errorInfo` — any
    - `warningInfo` — any
    - `data` — any — Data for integration
    - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
    - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
    - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
    - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated

**`DeleteIntegrationsRequestContent`**

- `integrationIds` — array — If specified, `companyIds` is ignored.
  - _array of_ `string`
- `companyIds` — array
  - _array of_ `string`

**`EntityType`**

- string _(enum: `sf_partner`, `main`)_

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GetCompanyIntegrationListResponseContent`**

- `items` — array **(required)**
  - _array of_ `CompanyIntegrations`
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `briefIntegrationList` — array **(required)**
      - _array of_ `BriefIntegration`
        - _(nesting depth limit — see `BriefIntegration` in the Schemas appendix)_

**`GetIntegrationByIdResponseContent`**

- `item` — Integration **(required)**
  - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
  - `entityType` — string _(enum: `sf_partner`, `main`)_
  - `statusChangeDate` — string
  - `errorInfo` — any
  - `warningInfo` — any
  - `data` — any — Data for integration
  - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
  - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
  - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
  - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated

**`GetIntegrationResponseContent`**

- `integration` — Integration **(required)**
  - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
  - `entityType` — string _(enum: `sf_partner`, `main`)_
  - `statusChangeDate` — string
  - `errorInfo` — any
  - `warningInfo` — any
  - `data` — any — Data for integration
  - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
  - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
  - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
  - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated

**`GetIntegrationsByCompaniesAndServicesResponseContent`**

- `items` — array **(required)**
  - _array of_ `Integration`
    - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
    - `entityType` — string _(enum: `sf_partner`, `main`)_
    - `statusChangeDate` — string
    - `errorInfo` — any
    - `warningInfo` — any
    - `data` — any — Data for integration
    - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
    - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
    - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
    - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated

**`GetIntegrationsByCompanyIdResponseContent`**

- `items` — array **(required)**
  - _array of_ `Integration`
    - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
    - `entityType` — string _(enum: `sf_partner`, `main`)_
    - `statusChangeDate` — string
    - `errorInfo` — any
    - `warningInfo` — any
    - `data` — any — Data for integration
    - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
    - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
    - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
    - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated

**`GetIntegrationsByServiceResponseContent`**

- `items` — array **(required)**
  - _array of_ `Integration`
    - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
    - `entityType` — string _(enum: `sf_partner`, `main`)_
    - `statusChangeDate` — string
    - `errorInfo` — any
    - `warningInfo` — any
    - `data` — any — Data for integration
    - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
    - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
    - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
    - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated

**`GetIntegrationsByServicesResponseContent`**

- `items` — array **(required)**
  - _array of_ `Integration`
    - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
    - `entityType` — string _(enum: `sf_partner`, `main`)_
    - `statusChangeDate` — string
    - `errorInfo` — any
    - `warningInfo` — any
    - `data` — any — Data for integration
    - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
    - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
    - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
    - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated

**`Integration`**

- `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
- `entityType` — string _(enum: `sf_partner`, `main`)_
- `statusChangeDate` — string
- `errorInfo` — any
- `warningInfo` — any
- `data` — any — Data for integration
- `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
- `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
- `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
- `companyId` — string **(required)** _(minLen=3; maxLen=30)_
- `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
- `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated

**`IntegrationNotFoundExceptionResponseContent`**

- `message` — string **(required)**
- `type` — string _(default=IntegrationNotFoundException)_

**`IntegrationStatusType`**

- string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_

**`Keys`**

- `companyId` — string **(required)** _(minLen=3; maxLen=30)_
- `integrationId` — string **(required)** _(minLen=6; maxLen=6)_

**`ListIntegrationsRequestContent`**

- `integrationIds` — array — If specified, filters by `companyIds` and `services` are ignored.
  - _array of_ `string`
- `companyIds` — array
  - _array of_ `string`
- `services` — array
  - _array of_ `string`
- `excludedStatuses` — array — List of integration statuses to ignore in the selection.
  - _array of_ `IntegrationStatusType`
- `onlyPublic` — boolean — Filter public integrations.
- `filters` — array — Advanced field filters using dot notation. Each filter should be in the format 'field=value'. Examples: 'data.hubspot_hub_id=12345', 'entityType=main', 'data.tenant=my_tenant'
  - _array of_ `string`
- `pageSize` — number — The number of integrations to return per page. _(default=100; min=1; max=100)_
- `nextToken` — string — The token to use to get the next page of results.

**`ListIntegrationsResponseContent`**

- `integrations` — array **(required)**
  - _array of_ `Integration`
    - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
    - `entityType` — string _(enum: `sf_partner`, `main`)_
    - `statusChangeDate` — string
    - `errorInfo` — any
    - `warningInfo` — any
    - `data` — any — Data for integration
    - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
    - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
    - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
    - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated
- `nextToken` — string

**`ListWebhookIntegrationsResponseContent`**

- `integrations` — array **(required)**
  - _array of_ `WebhookIntegration`
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
    - `type` — string **(required)** _(enum: `sqs`, `webhook`)_
    - `url` — string **(required)**
    - `key` — string **(required)**
    - `secret` — string **(required)**
    - `filter` — array **(required)**
      - _array of_ `string`

**`PatchIntegrationRequestContent`**

- `externalId` — string — Deprecated. Will use companyId instead This shape is deprecated. _(minLen=3; maxLen=30; deprecated)_
- `service` — string _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
- `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
- `entityType` — string _(enum: `sf_partner`, `main`)_
- `statusChangeDate` — string
- `errorInfo` — any
- `warningInfo` — any
- `data` — any — Data for integration

**`PatchIntegrationResponseContent`**

- `item` — Integration **(required)**
  - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
  - `entityType` — string _(enum: `sf_partner`, `main`)_
  - `statusChangeDate` — string
  - `errorInfo` — any
  - `warningInfo` — any
  - `data` — any — Data for integration
  - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
  - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
  - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
  - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated

**`PutIntegrationDataItem`**

- `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
- `entityType` — string _(enum: `sf_partner`, `main`)_
- `statusChangeDate` — string
- `errorInfo` — any
- `warningInfo` — any
- `data` — any — Data for integration
- `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
- `companyId` — string **(required)** _(minLen=3; maxLen=30)_
- `integrationId` — string **(required)** _(minLen=6; maxLen=6)_

**`PutIntegrationRequestContent`**

- `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
- `entityType` — string _(enum: `sf_partner`, `main`)_
- `statusChangeDate` — string
- `errorInfo` — any
- `warningInfo` — any
- `data` — any — Data for integration
- `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
- `integrationId` — string _(minLen=6; maxLen=6)_

**`PutIntegrationResponseContent`**

- `item` — Integration **(required)**
  - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
  - `entityType` — string _(enum: `sf_partner`, `main`)_
  - `statusChangeDate` — string
  - `errorInfo` — any
  - `warningInfo` — any
  - `data` — any — Data for integration
  - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
  - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
  - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
  - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated

**`Service`**

- string _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_

**`UpdateIntegrationRequestContent`**

- `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
- `entityType` — string _(enum: `sf_partner`, `main`)_
- `statusChangeDate` — string
- `errorInfo` — any
- `warningInfo` — any
- `data` — any — Data for integration
- `service` — string _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_

**`UpdateIntegrationResponseContent`**

- `integration` — Integration **(required)**
  - `status` — string _(enum: `deleting`, `installing`, `warning`, `enabled`, `disabled`, `suspended`, `broken`)_
  - `entityType` — string _(enum: `sf_partner`, `main`)_
  - `statusChangeDate` — string
  - `errorInfo` — any
  - `warningInfo` — any
  - `data` — any — Data for integration
  - `service` — string **(required)** _(enum: `salesforce`, `hubspot`, `google_calendar`, `microsoft_calendar`, `salesforce_community`, `bamboo_hr`, `microsoft_presence`, `iframe_integration`, `webhook`, `hubspot_backend`, `salesforce_backend`, `salesforce_omni`, … (+5))_
  - `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
  - `externalId` — string — Deprecated. Will use companyId instead _(minLen=3; maxLen=30)_
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `createdAt` — string — Date and time (in ISO 8601 format) the integration was created
  - `updatedAt` — string — Date and time (in ISO 8601 format) the integration was last updated

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

**`WebhookEndpointType`**

- string _(enum: `sqs`, `webhook`)_

**`WebhookIntegration`**

- `companyId` — string **(required)** _(minLen=3; maxLen=30)_
- `integrationId` — string **(required)** _(minLen=6; maxLen=6)_
- `type` — string **(required)** _(enum: `sqs`, `webhook`)_
- `url` — string **(required)**
- `key` — string **(required)**
- `secret` — string **(required)**
- `filter` — array **(required)**
  - _array of_ `string`

</details>
