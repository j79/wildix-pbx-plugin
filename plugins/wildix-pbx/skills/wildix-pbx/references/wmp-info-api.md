## WMP Info API

_OpenAPI: WMP API service (deprecated) — version —_

**Servers**

- `https://api.wildix.com` — Production
- `https://api-stage.wildix.com` — Stage

### Other

#### `GET` `/v2/PBXs/{domain}`

Get PBX information from portal

- operationId: `WmpGetPbxInfo`
- **Parameters**
  - `domain` (path) — string **(required)** — A doman of the PBX or it's serial. _(minLen=1; maxLen=100)_
- **Response 200** (`WmpGetPbxInfoResponseContent`)
  - `type` — object **(required)**
  - `result` — WmpGetPbxInfoResult **(required)**
    - `domain` — string **(required)**
    - `port` — number **(required)** _(default=443)_
    - `serial` — string **(required)**
    - `awsRegion` — string **(required)**
    - `id` — number **(required)**
    - `master` — string **(required)**
    - `version` — WmpPbxVersionInfo **(required)**
      - `wms` — string
    - `license` — WmpLicenseInfo **(required)**
      - `phones` — number
      - `calls` — number
      - `rooms` — number
      - `token` — string
      - `serial` — string
      - `pbxKey` — string
      - `perUserLicenses` — WmpPerUserLicenseMap
        - _map of_ `number`
      - `network` — boolean
      - `faxes` — WmpPerServiceLicenses
        - `state` — boolean
        - `until` — number
      - `redundancy` — WmpPerServiceLicenses
        - `state` — boolean
        - `until` — number
      - `perUser` — WmpPerServiceLicenses
        - `state` — boolean
        - `until` — number
      - `support` — WmpPerServiceLicenses
        - `state` — boolean
        - `until` — number
      - `hardware` — WmpPerServiceLicenses
        - `state` — boolean
        - `until` — number
      - `cdrView` — WmpPerServiceLicenses
        - `state` — boolean
        - `until` — number
      - `ctiConnectPro` — WmpPerServiceLicenses
        - `state` — boolean
        - `until` — number
      - `operatorPanel` — WmpPerServiceLicenses
        - `state` — boolean
        - `until` — number
      - `tapi` — WmpPerServiceLicenses
        - `state` — boolean
        - `until` — number
      - `conference` — WmpPerServiceLicenses
        - `state` — boolean
        - `until` — number
      - `upgrade2to3` — WmpPerServiceLicenses
        - `state` — boolean
        - `until` — number
      - `wgl` — WmpPerServiceLicenses
        - `state` — boolean
        - `until` — number
    - `companyId` — string **(required)**
    - `companyCode` — string **(required)**
    - `companyName` — string **(required)**
    - `identity` — string **(required)**
    - `key` — string **(required)**
- Errors: `401`, `403`, `404`

#### `GET` `/v2/companies/{companyId}`

Get information about company from WMP

- operationId: `WmpGetCompanyInfo`
- **Parameters**
  - `companyId` (path) — string **(required)** — A company ID number. _(minLen=1; maxLen=20)_
- **Response 200** (`WmpGetCompanyInfoResponseContent`)
  - `type` — object **(required)**
  - `result` — WmpGetCompanyInfoResult **(required)**
    - `companyId` — string **(required)**
    - `companyCode` — string **(required)**
    - `companyName` — string **(required)**
    - `licenses` — WmpPerUserLicenseMap **(required)**
      - _map of_ `number`
    - `pbxs` — array **(required)**
      - _array of_ `WmpPbxInfo`
        - `domain` — string **(required)**
        - `port` — number **(required)** _(default=443)_
        - `serial` — string **(required)**
        - `awsRegion` — string **(required)**
        - `isServer` — boolean **(required)**
        - `version` — string **(required)**
- Errors: `401`, `403`, `404`

### Routes non publiées — deprecated (en cours de décommissionnement)

> ⚠️ Les routes ci-dessous ont figuré dans une révision antérieure de la spécification publiée mais **n'y figurent plus**. Elles sont en cours de décommissionnement et peuvent encore répondre pendant quelques mois : leur description est conservée telle qu'elle était documentée, et la date de retrait est indiquée sur chacune. À ne pas utiliser pour de nouveaux développements.

#### `GET` `/v1/companies/{companyId}`

> ⚠️ **Statut : deprecated (non publiée)** — absente de la documentation depuis la révision du 2026-11-10 (groupe d'origine : _Company_). Description conservée telle que publiée au 2026-10-18.

Gets information about company.

- operationId: `GetCompanyInfo`
- **Scopes**: `company:GetCompanyInfo`, `company:read`
- **Parameters**
  - `companyId` (path) — string **(required)** — Company identification number. Example: it_123456 _(minLen=1; maxLen=20)_
- **Response 200** (`GetCompanyInfoResponseContent`)
  - `companyId` — string **(required)**
  - `companyCode` — string **(required)**
  - `companyName` — string **(required)**
  - `licenseType` — string **(required)** _(enum: `UC`, `X_BEES`, `X_HOPPERS`)_
  - `licenses` — array **(required)**
    - _array of_ `LicenseItem`
      - `name` — string **(required)**
      - `value` — number **(required)**
  - `pbxs` — array **(required)**
    - _array of_ `PbxInfo`
      - `domain` — string **(required)**
      - `port` — number **(required)** _(default=443)_
      - `serial` — string **(required)**
      - `wmsVersion` — string **(required)**
      - `awsRegion` — string **(required)**
      - `isServer` — boolean **(required)**
- Errors: `400`, `403`, `404`

#### `GET` `/v1/pbxs/{nameOrSerial}`

> ⚠️ **Statut : deprecated (non publiée)** — absente de la documentation depuis la révision du 2026-11-10 (groupe d'origine : _PBX_). Description conservée telle que publiée au 2026-10-18.

Gets information about PBX.

- operationId: `GetPbxInfo`
- **Scopes**: `company:GetPbxInfo`, `company:read`
- **Parameters**
  - `nameOrSerial` (path) — string **(required)** — A name or serial of the PBX. Example: test-tpx, test-tpx.wildixin.com, 22110000aaaa, 22110000aaaa.wildixin.com _(minLen=1; maxLen=100)_
- **Response 200** (`GetPbxInfoResponseContent`)
  - `domain` — string **(required)**
  - `port` — number **(required)** _(default=443)_
  - `serial` — string **(required)**
  - `wmsVersion` — string **(required)**
  - `awsRegion` — string **(required)**
  - `id` — number **(required)**
  - `master` — string **(required)**
  - `licenseType` — string **(required)** _(enum: `UC`, `X_BEES`, `X_HOPPERS`)_
  - `licenses` — array **(required)**
    - _array of_ `LicenseItem`
      - `name` — string **(required)**
      - `value` — number **(required)**
  - `companyId` — string **(required)**
  - `companyCode` — string **(required)**
  - `companyName` — string **(required)**
- Errors: `400`, `403`, `404`

#### `POST` `/v1/pbx-key/check`

> ⚠️ **Statut : deprecated (non publiée)** — absente de la documentation depuis la révision du 2026-11-10 (groupe d'origine : _PBX_). Description conservée telle que publiée au 2026-10-18.

Checking the validity of the PbxKey for this PBX. Temporary route. To be removed after remove PBX Auth

- operationId: `CheckPbxKey`
- **Request body** (`application/json` — `CheckPbxKeyRequestContent`)
  - `nameOrSerial` — string **(required)** — A name or serial of the PBX. Example: test-tpx, test-tpx.wildixin.com, 22110000aaaa, 22110000aaaa.wildixin.com _(minLen=1; maxLen=100)_
  - `pbxKey` — string **(required)** — PBX key. _(minLen=10; maxLen=100)_
- **Response 200** (`CheckPbxKeyResponseContent`)
  - `domain` — string **(required)**
  - `port` — number **(required)** _(default=443)_
  - `serial` — string **(required)**
  - `wmsVersion` — string **(required)**
  - `awsRegion` — string **(required)**
  - `id` — number **(required)**
  - `master` — string **(required)**
  - `licenseType` — string **(required)** _(enum: `UC`, `X_BEES`, `X_HOPPERS`)_
  - `licenses` — array **(required)**
    - _array of_ `LicenseItem`
      - `name` — string **(required)**
      - `value` — number **(required)**
  - `companyId` — string **(required)**
  - `companyCode` — string **(required)**
  - `companyName` — string **(required)**
- Errors: `400`, `403`, `404`

### Schemas appendix — WMP Info API

<details><summary>14 component schemas</summary>

**`ErrorData`**

- `reason` — string **(required)**
- `code` — string **(required)**

**`ForbidenExceptionResponseContent`**

- `type` — object **(required)**
- `result` — ErrorData **(required)**
  - `reason` — string **(required)**
  - `code` — string **(required)**

**`NotFoundExceptionResponseContent`**

- `type` — object **(required)**
- `result` — ErrorData **(required)**
  - `reason` — string **(required)**
  - `code` — string **(required)**

**`ResponseType`**

- string _(enum: `result`, `error`)_

**`UnauthorizedExceptionResponseContent`**

- `type` — object **(required)**
- `result` — ErrorData **(required)**
  - `reason` — string **(required)**
  - `code` — string **(required)**

**`WmpGetCompanyInfoResponseContent`**

- `type` — object **(required)**
- `result` — WmpGetCompanyInfoResult **(required)**
  - `companyId` — string **(required)**
  - `companyCode` — string **(required)**
  - `companyName` — string **(required)**
  - `licenses` — WmpPerUserLicenseMap **(required)**
    - _map of_ `number`
  - `pbxs` — array **(required)**
    - _array of_ `WmpPbxInfo`
      - `domain` — string **(required)**
      - `port` — number **(required)** _(default=443)_
      - `serial` — string **(required)**
      - `awsRegion` — string **(required)**
      - `isServer` — boolean **(required)**
      - `version` — string **(required)**

**`WmpGetCompanyInfoResult`**

- `companyId` — string **(required)**
- `companyCode` — string **(required)**
- `companyName` — string **(required)**
- `licenses` — WmpPerUserLicenseMap **(required)**
  - _map of_ `number`
- `pbxs` — array **(required)**
  - _array of_ `WmpPbxInfo`
    - `domain` — string **(required)**
    - `port` — number **(required)** _(default=443)_
    - `serial` — string **(required)**
    - `awsRegion` — string **(required)**
    - `isServer` — boolean **(required)**
    - `version` — string **(required)**

**`WmpGetPbxInfoResponseContent`**

- `type` — object **(required)**
- `result` — WmpGetPbxInfoResult **(required)**
  - `domain` — string **(required)**
  - `port` — number **(required)** _(default=443)_
  - `serial` — string **(required)**
  - `awsRegion` — string **(required)**
  - `id` — number **(required)**
  - `master` — string **(required)**
  - `version` — WmpPbxVersionInfo **(required)**
    - `wms` — string
  - `license` — WmpLicenseInfo **(required)**
    - `phones` — number
    - `calls` — number
    - `rooms` — number
    - `token` — string
    - `serial` — string
    - `pbxKey` — string
    - `perUserLicenses` — WmpPerUserLicenseMap
      - _map of_ `number`
    - `network` — boolean
    - `faxes` — WmpPerServiceLicenses
      - `state` — boolean
      - `until` — number
    - `redundancy` — WmpPerServiceLicenses
      - `state` — boolean
      - `until` — number
    - `perUser` — WmpPerServiceLicenses
      - `state` — boolean
      - `until` — number
    - `support` — WmpPerServiceLicenses
      - `state` — boolean
      - `until` — number
    - `hardware` — WmpPerServiceLicenses
      - `state` — boolean
      - `until` — number
    - `cdrView` — WmpPerServiceLicenses
      - `state` — boolean
      - `until` — number
    - `ctiConnectPro` — WmpPerServiceLicenses
      - `state` — boolean
      - `until` — number
    - `operatorPanel` — WmpPerServiceLicenses
      - `state` — boolean
      - `until` — number
    - `tapi` — WmpPerServiceLicenses
      - `state` — boolean
      - `until` — number
    - `conference` — WmpPerServiceLicenses
      - `state` — boolean
      - `until` — number
    - `upgrade2to3` — WmpPerServiceLicenses
      - `state` — boolean
      - `until` — number
    - `wgl` — WmpPerServiceLicenses
      - `state` — boolean
      - `until` — number
  - `companyId` — string **(required)**
  - `companyCode` — string **(required)**
  - `companyName` — string **(required)**
  - `identity` — string **(required)**
  - `key` — string **(required)**

**`WmpGetPbxInfoResult`**

- `domain` — string **(required)**
- `port` — number **(required)** _(default=443)_
- `serial` — string **(required)**
- `awsRegion` — string **(required)**
- `id` — number **(required)**
- `master` — string **(required)**
- `version` — WmpPbxVersionInfo **(required)**
  - `wms` — string
- `license` — WmpLicenseInfo **(required)**
  - `phones` — number
  - `calls` — number
  - `rooms` — number
  - `token` — string
  - `serial` — string
  - `pbxKey` — string
  - `perUserLicenses` — WmpPerUserLicenseMap
    - _map of_ `number`
  - `network` — boolean
  - `faxes` — WmpPerServiceLicenses
    - `state` — boolean
    - `until` — number
  - `redundancy` — WmpPerServiceLicenses
    - `state` — boolean
    - `until` — number
  - `perUser` — WmpPerServiceLicenses
    - `state` — boolean
    - `until` — number
  - `support` — WmpPerServiceLicenses
    - `state` — boolean
    - `until` — number
  - `hardware` — WmpPerServiceLicenses
    - `state` — boolean
    - `until` — number
  - `cdrView` — WmpPerServiceLicenses
    - `state` — boolean
    - `until` — number
  - `ctiConnectPro` — WmpPerServiceLicenses
    - `state` — boolean
    - `until` — number
  - `operatorPanel` — WmpPerServiceLicenses
    - `state` — boolean
    - `until` — number
  - `tapi` — WmpPerServiceLicenses
    - `state` — boolean
    - `until` — number
  - `conference` — WmpPerServiceLicenses
    - `state` — boolean
    - `until` — number
  - `upgrade2to3` — WmpPerServiceLicenses
    - `state` — boolean
    - `until` — number
  - `wgl` — WmpPerServiceLicenses
    - `state` — boolean
    - `until` — number
- `companyId` — string **(required)**
- `companyCode` — string **(required)**
- `companyName` — string **(required)**
- `identity` — string **(required)**
- `key` — string **(required)**

**`WmpLicenseInfo`**

- `phones` — number
- `calls` — number
- `rooms` — number
- `token` — string
- `serial` — string
- `pbxKey` — string
- `perUserLicenses` — WmpPerUserLicenseMap
  - _map of_ `number`
- `network` — boolean
- `faxes` — WmpPerServiceLicenses
  - `state` — boolean
  - `until` — number
- `redundancy` — WmpPerServiceLicenses
  - `state` — boolean
  - `until` — number
- `perUser` — WmpPerServiceLicenses
  - `state` — boolean
  - `until` — number
- `support` — WmpPerServiceLicenses
  - `state` — boolean
  - `until` — number
- `hardware` — WmpPerServiceLicenses
  - `state` — boolean
  - `until` — number
- `cdrView` — WmpPerServiceLicenses
  - `state` — boolean
  - `until` — number
- `ctiConnectPro` — WmpPerServiceLicenses
  - `state` — boolean
  - `until` — number
- `operatorPanel` — WmpPerServiceLicenses
  - `state` — boolean
  - `until` — number
- `tapi` — WmpPerServiceLicenses
  - `state` — boolean
  - `until` — number
- `conference` — WmpPerServiceLicenses
  - `state` — boolean
  - `until` — number
- `upgrade2to3` — WmpPerServiceLicenses
  - `state` — boolean
  - `until` — number
- `wgl` — WmpPerServiceLicenses
  - `state` — boolean
  - `until` — number

**`WmpPbxInfo`**

- `domain` — string **(required)**
- `port` — number **(required)** _(default=443)_
- `serial` — string **(required)**
- `awsRegion` — string **(required)**
- `isServer` — boolean **(required)**
- `version` — string **(required)**

**`WmpPbxVersionInfo`**

- `wms` — string

**`WmpPerServiceLicenses`**

- `state` — boolean
- `until` — number

**`WmpPerUserLicenseMap`**

- _map of_ `number`

</details>
