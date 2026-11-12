## CDS Console API

_OpenAPI: CDS - console api — version —_

**Servers**

- `https://cds-console-api.wildix.com` — Production
- `https://cds-console-api-stable.wildix.com` — Stable
- `https://cds-console-api-stage.wildix.com` — Stage

### Other

#### `DELETE` `/v1/category/{name}`

Remove all category data it's run rotation task with zero period.

- operationId: `ClearCategory`
- **Parameters**
  - `name` (path) — string **(required)** — Name of cleared category.
- **Response 200** (`ClearCategoryResponseContent`)
  - `success` — boolean **(required)**
- Errors: `400`, `403`, `404`, `500`

#### `GET` `/v1/companies`

Check fetch statistic status

- operationId: `GetCompaniesInfo`
- **Parameters**
  - `count` (query) — number — Maximum number of records in the response. _(default=100; min=1; max=100)_
  - `start` (query) — string — Link to the next page, provided in the response. _(default=)_
- **Response 200** (`GetCompaniesInfoResponseContent`)
  - `items` — array **(required)**
    - _array of_ `CompanyInfo`
      - `company` — string **(required)** — Company id
      - `items` — array **(required)** — List of files types in different regions
        - _array of_ `UsageItemInfo`
          - `type` — string **(required)** — File type
          - `region` — string **(required)** — Region where the file is located
          - `size` — number **(required)** — Total size of files of the same type
          - `oldestFileDate` — number **(required)** — Date of the oldest file
      - `rotation` — array **(required)** — List of rotation periods for each file type
        - _array of_ `RotationItemInfo`
          - `key` — string **(required)** — File type
          - `value` — number **(required)** — Rotation period. Valid values: 0.1, 0.25, 0.5, 0.75 and integers from 1 to 240 _(default=12; format=float)_
      - `trends` — UsageTrends **(required)**
        - `averageDay` — number **(required)** — Average space usage per day
        - `days` — number **(required)** — Amount of days
      - `ai` — array **(required)** — AI usage
        - _array of_ `AiUsage`
          - `month` — string **(required)** — Format: YYYY-MM
          - `usageTranscription` — number **(required)** — Real-time transcription in seconds
          - `usageVoiceBot` — number **(required)** — Total usage voice bot in seconds
          - `usagePostTranscription` — number **(required)** — Post-call transcription seconds
          - `usageBroadcasts` — number **(required)** — Broadcast transcription seconds
          - `currentBundle` — string **(required)** — Deprecated. At the moment, it is needed to display historical data about the bundle name — S, M, L, XL, 2XL, etc. This shape is deprecated. _(deprecated)_
          - `bundleCount` — number **(required)** — Number of bundles purchased
      - `storageSize` — number **(required)** — Total purchased space in MB
      - `licenseFamily` — string **(required)** _(enum: `UC`, `X_BEES`, `X_HOPPERS`)_
  - `nextPage` — string **(required)** — Link to the next page for implementing pagination.
- Errors: `400`, `403`, `500`

#### `POST` `/v1/refresh`

Refresh statistic usage

- operationId: `FetchStatistic`
- **Response 200** (`FetchStatisticResponseContent`)
  - `messageId` — string **(required)**
- Errors: `400`, `403`, `500`

#### `GET` `/v1/usage`

Get space usage

- operationId: `GetUsage`
- **Response 200** (`GetUsageResponseContent`)
  - `company` — string **(required)** — Company id
  - `items` — array **(required)** — List of files types in different regions
    - _array of_ `UsageItemInfo`
      - `type` — string **(required)** — File type
      - `region` — string **(required)** — Region where the file is located
      - `size` — number **(required)** — Total size of files of the same type
      - `oldestFileDate` — number **(required)** — Date of the oldest file
  - `rotation` — array **(required)** — List of rotation periods for each file type
    - _array of_ `RotationItemInfo`
      - `key` — string **(required)** — File type
      - `value` — number **(required)** — Rotation period. Valid values: 0.1, 0.25, 0.5, 0.75 and integers from 1 to 240 _(default=12; format=float)_
  - `trends` — UsageTrends **(required)**
    - `averageDay` — number **(required)** — Average space usage per day
    - `days` — number **(required)** — Amount of days
  - `ai` — array **(required)** — AI usage
    - _array of_ `AiUsage`
      - `month` — string **(required)** — Format: YYYY-MM
      - `usageTranscription` — number **(required)** — Real-time transcription in seconds
      - `usageVoiceBot` — number **(required)** — Total usage voice bot in seconds
      - `usagePostTranscription` — number **(required)** — Post-call transcription seconds
      - `usageBroadcasts` — number **(required)** — Broadcast transcription seconds
      - `currentBundle` — string **(required)** — Deprecated. At the moment, it is needed to display historical data about the bundle name — S, M, L, XL, 2XL, etc. This shape is deprecated. _(deprecated)_
      - `bundleCount` — number **(required)** — Number of bundles purchased
  - `storageSize` — number **(required)** — Total purchased space in MB
  - `licenseFamily` — string **(required)** _(enum: `UC`, `X_BEES`, `X_HOPPERS`)_
- Errors: `400`, `403`, `500`

#### `PUT` `/v1/usage`

Update usage data period

- operationId: `UpdateUsage`
- **Request body** (`application/json` — `UpdateUsageRequestContent`) **(required)**
  - `rotation` — array **(required)**
    - _array of_ `RotationItemInfo`
      - `key` — string **(required)** — File type
      - `value` — number **(required)** — Rotation period. Valid values: 0.1, 0.25, 0.5, 0.75 and integers from 1 to 240 _(default=12; format=float)_
- **Response 200** (`UpdateUsageResponseContent`)
  - `rotation` — array **(required)**
    - _array of_ `RotationItemInfo`
      - `key` — string **(required)** — File type
      - `value` — number **(required)** — Rotation period. Valid values: 0.1, 0.25, 0.5, 0.75 and integers from 1 to 240 _(default=12; format=float)_
- Errors: `400`, `403`, `500`

### Schemas appendix — CDS Console API

<details><summary>16 component schemas</summary>

**`AiUsage`**

- `month` — string **(required)** — Format: YYYY-MM
- `usageTranscription` — number **(required)** — Real-time transcription in seconds
- `usageVoiceBot` — number **(required)** — Total usage voice bot in seconds
- `usagePostTranscription` — number **(required)** — Post-call transcription seconds
- `usageBroadcasts` — number **(required)** — Broadcast transcription seconds
- `currentBundle` — string **(required)** — Deprecated. At the moment, it is needed to display historical data about the bundle name — S, M, L, XL, 2XL, etc. This shape is deprecated. _(deprecated)_
- `bundleCount` — number **(required)** — Number of bundles purchased

**`ClearCategoryResponseContent`**

- `success` — boolean **(required)**

**`CompanyInfo`**

- `company` — string **(required)** — Company id
- `items` — array **(required)** — List of files types in different regions
  - _array of_ `UsageItemInfo`
    - `type` — string **(required)** — File type
    - `region` — string **(required)** — Region where the file is located
    - `size` — number **(required)** — Total size of files of the same type
    - `oldestFileDate` — number **(required)** — Date of the oldest file
- `rotation` — array **(required)** — List of rotation periods for each file type
  - _array of_ `RotationItemInfo`
    - `key` — string **(required)** — File type
    - `value` — number **(required)** — Rotation period. Valid values: 0.1, 0.25, 0.5, 0.75 and integers from 1 to 240 _(default=12; format=float)_
- `trends` — UsageTrends **(required)**
  - `averageDay` — number **(required)** — Average space usage per day
  - `days` — number **(required)** — Amount of days
- `ai` — array **(required)** — AI usage
  - _array of_ `AiUsage`
    - `month` — string **(required)** — Format: YYYY-MM
    - `usageTranscription` — number **(required)** — Real-time transcription in seconds
    - `usageVoiceBot` — number **(required)** — Total usage voice bot in seconds
    - `usagePostTranscription` — number **(required)** — Post-call transcription seconds
    - `usageBroadcasts` — number **(required)** — Broadcast transcription seconds
    - `currentBundle` — string **(required)** — Deprecated. At the moment, it is needed to display historical data about the bundle name — S, M, L, XL, 2XL, etc. This shape is deprecated. _(deprecated)_
    - `bundleCount` — number **(required)** — Number of bundles purchased
- `storageSize` — number **(required)** — Total purchased space in MB
- `licenseFamily` — string **(required)** _(enum: `UC`, `X_BEES`, `X_HOPPERS`)_

**`FetchStatisticResponseContent`**

- `messageId` — string **(required)**

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GetCompaniesInfoResponseContent`**

- `items` — array **(required)**
  - _array of_ `CompanyInfo`
    - `company` — string **(required)** — Company id
    - `items` — array **(required)** — List of files types in different regions
      - _array of_ `UsageItemInfo`
        - _(nesting depth limit — see `UsageItemInfo` in the Schemas appendix)_
    - `rotation` — array **(required)** — List of rotation periods for each file type
      - _array of_ `RotationItemInfo`
        - _(nesting depth limit — see `RotationItemInfo` in the Schemas appendix)_
    - `trends` — UsageTrends **(required)**
      - `averageDay` — number **(required)** — Average space usage per day
      - `days` — number **(required)** — Amount of days
    - `ai` — array **(required)** — AI usage
      - _array of_ `AiUsage`
        - _(nesting depth limit — see `AiUsage` in the Schemas appendix)_
    - `storageSize` — number **(required)** — Total purchased space in MB
    - `licenseFamily` — string **(required)** _(enum: `UC`, `X_BEES`, `X_HOPPERS`)_
- `nextPage` — string **(required)** — Link to the next page for implementing pagination.

**`GetUsageResponseContent`**

- `company` — string **(required)** — Company id
- `items` — array **(required)** — List of files types in different regions
  - _array of_ `UsageItemInfo`
    - `type` — string **(required)** — File type
    - `region` — string **(required)** — Region where the file is located
    - `size` — number **(required)** — Total size of files of the same type
    - `oldestFileDate` — number **(required)** — Date of the oldest file
- `rotation` — array **(required)** — List of rotation periods for each file type
  - _array of_ `RotationItemInfo`
    - `key` — string **(required)** — File type
    - `value` — number **(required)** — Rotation period. Valid values: 0.1, 0.25, 0.5, 0.75 and integers from 1 to 240 _(default=12; format=float)_
- `trends` — UsageTrends **(required)**
  - `averageDay` — number **(required)** — Average space usage per day
  - `days` — number **(required)** — Amount of days
- `ai` — array **(required)** — AI usage
  - _array of_ `AiUsage`
    - `month` — string **(required)** — Format: YYYY-MM
    - `usageTranscription` — number **(required)** — Real-time transcription in seconds
    - `usageVoiceBot` — number **(required)** — Total usage voice bot in seconds
    - `usagePostTranscription` — number **(required)** — Post-call transcription seconds
    - `usageBroadcasts` — number **(required)** — Broadcast transcription seconds
    - `currentBundle` — string **(required)** — Deprecated. At the moment, it is needed to display historical data about the bundle name — S, M, L, XL, 2XL, etc. This shape is deprecated. _(deprecated)_
    - `bundleCount` — number **(required)** — Number of bundles purchased
- `storageSize` — number **(required)** — Total purchased space in MB
- `licenseFamily` — string **(required)** _(enum: `UC`, `X_BEES`, `X_HOPPERS`)_

**`InternalServerErrorResponseContent`**

- `message` — string **(required)**

**`LicenseType`**

- string _(enum: `UC`, `X_BEES`, `X_HOPPERS`)_

**`NotFoundExceptionResponseContent`**

- `message` — string **(required)** _(default=Not found)_

**`RotationItemInfo`**

- `key` — string **(required)** — File type
- `value` — number **(required)** — Rotation period. Valid values: 0.1, 0.25, 0.5, 0.75 and integers from 1 to 240 _(default=12; format=float)_

**`UpdateUsageRequestContent`**

- `rotation` — array **(required)**
  - _array of_ `RotationItemInfo`
    - `key` — string **(required)** — File type
    - `value` — number **(required)** — Rotation period. Valid values: 0.1, 0.25, 0.5, 0.75 and integers from 1 to 240 _(default=12; format=float)_

**`UpdateUsageResponseContent`**

- `rotation` — array **(required)**
  - _array of_ `RotationItemInfo`
    - `key` — string **(required)** — File type
    - `value` — number **(required)** — Rotation period. Valid values: 0.1, 0.25, 0.5, 0.75 and integers from 1 to 240 _(default=12; format=float)_

**`UsageItemInfo`**

- `type` — string **(required)** — File type
- `region` — string **(required)** — Region where the file is located
- `size` — number **(required)** — Total size of files of the same type
- `oldestFileDate` — number **(required)** — Date of the oldest file

**`UsageTrends`**

- `averageDay` — number **(required)** — Average space usage per day
- `days` — number **(required)** — Amount of days

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

</details>
